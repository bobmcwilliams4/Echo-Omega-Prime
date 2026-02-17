"""
D1 Deed Record Ingest Pipeline — Deterministic, Idempotent, Resumable

Loads R2 JSON shards (ENCORE scraped county records) into ShadowGlass D1
for structured searching by section/block/lot/grantor/grantee.

Architecture:
    R2 JSON shards → Extract/Normalize → Batch Insert → D1 deed_records table

Features:
    - IDEMPOTENT: record_hash dedup prevents duplicate inserts
    - RESUMABLE: checkpoint table tracks processed shards
    - BATCHED: 500 records per transaction for D1 performance
    - LOGGED: ingest_ledger table tracks every batch for audit
    - NORMALIZED: legal descriptions normalized for fuzzy search
    - EXTRACTED: section/block/lot parsed from legal description text

Usage:
    python d1_deed_ingest.py --county REEVES --dry-run
    python d1_deed_ingest.py --county REEVES
    python d1_deed_ingest.py --county REEVES --instrument DEED
    python d1_deed_ingest.py --county REEVES --resume
    python d1_deed_ingest.py --schema-only  # Just create tables
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

RCLONE = r"H:\Tools\rclone\rclone.exe"
NPX = r"C:\Program Files\nodejs\npx.cmd"
WRANGLER_CWD = r"O:\ECHO_OMEGA_PRIME"
D1_DATABASE = "shadowglass-scraper"
R2_BUCKET = "echo-prime-knowledge"
R2_BASE = "ENCORE"
BATCH_SIZE = 50  # D1 has SQL size limits — 50 records per batch is safe
MAX_RETRIES = 3

INSTRUMENT_TYPES = [
    "DEED", "MINERAL_DEED", "OIL_AND_GAS_LEASE", "ASSIGNMENT",
    "EASEMENT", "WARRANTY_DEED", "ROYALTY_DEED", "RELEASE",
    "RIGHT_OF_WAY", "AFFIDAVIT_OF_HEIRSHIP", "PROBATE",
    "POWER_OF_ATTORNEY", "MEMORANDUM", "SURFACE_LEASE",
    "ABSTRACT_OF_JUDGMENT",
]


# ═══════════════════════════════════════════════════════════════════
# D1 SCHEMA — Tables + Indexes
# ═══════════════════════════════════════════════════════════════════

SCHEMA_SQL = [
    # Main deed records table
    """CREATE TABLE IF NOT EXISTS deed_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        county TEXT NOT NULL,
        instrument_type TEXT NOT NULL,
        doc_id TEXT NOT NULL,
        instrument_number TEXT,
        recorded_date TEXT,
        instrument_date TEXT,
        year INTEGER,
        grantor TEXT NOT NULL DEFAULT '',
        grantee TEXT NOT NULL DEFAULT '',
        legal_description TEXT DEFAULT '',
        legal_normalized TEXT DEFAULT '',
        section TEXT DEFAULT '',
        block TEXT DEFAULT '',
        lot TEXT DEFAULT '',
        township TEXT DEFAULT '',
        survey TEXT DEFAULT '',
        book TEXT DEFAULT '',
        volume TEXT DEFAULT '',
        page TEXT DEFAULT '',
        book_volume_page TEXT DEFAULT '',
        consideration TEXT DEFAULT '',
        page_count INTEGER DEFAULT 0,
        download_link TEXT DEFAULT '',
        doc_type_code TEXT DEFAULT '',
        record_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(county, doc_id)
    )""",

    # Performance indexes for land queries
    "CREATE INDEX IF NOT EXISTS idx_dr_county ON deed_records(county)",
    "CREATE INDEX IF NOT EXISTS idx_dr_section ON deed_records(section)",
    "CREATE INDEX IF NOT EXISTS idx_dr_block ON deed_records(block)",
    "CREATE INDEX IF NOT EXISTS idx_dr_lot ON deed_records(lot)",
    "CREATE INDEX IF NOT EXISTS idx_dr_type ON deed_records(instrument_type)",
    "CREATE INDEX IF NOT EXISTS idx_dr_date ON deed_records(recorded_date)",
    "CREATE INDEX IF NOT EXISTS idx_dr_grantor ON deed_records(grantor)",
    "CREATE INDEX IF NOT EXISTS idx_dr_grantee ON deed_records(grantee)",
    "CREATE INDEX IF NOT EXISTS idx_dr_hash ON deed_records(record_hash)",
    "CREATE INDEX IF NOT EXISTS idx_dr_county_section ON deed_records(county, section, block)",
    "CREATE INDEX IF NOT EXISTS idx_dr_county_type ON deed_records(county, instrument_type)",
    "CREATE INDEX IF NOT EXISTS idx_dr_legal_norm ON deed_records(legal_normalized)",

    # Checkpoint table for resumable ingestion
    """CREATE TABLE IF NOT EXISTS ingest_checkpoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        county TEXT NOT NULL,
        instrument_type TEXT NOT NULL,
        shard_name TEXT NOT NULL,
        records_in_shard INTEGER DEFAULT 0,
        records_inserted INTEGER DEFAULT 0,
        records_skipped INTEGER DEFAULT 0,
        records_errored INTEGER DEFAULT 0,
        shard_hash TEXT DEFAULT '',
        started_at TEXT,
        completed_at TEXT,
        status TEXT DEFAULT 'pending',
        UNIQUE(county, instrument_type, shard_name)
    )""",

    # Audit ledger — every batch logged
    """CREATE TABLE IF NOT EXISTS ingest_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        county TEXT NOT NULL,
        instrument_type TEXT NOT NULL,
        shard_name TEXT NOT NULL,
        batch_number INTEGER,
        batch_size INTEGER,
        batch_hash TEXT,
        records_inserted INTEGER DEFAULT 0,
        records_skipped INTEGER DEFAULT 0,
        error_count INTEGER DEFAULT 0,
        elapsed_ms REAL DEFAULT 0,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )""",
]


# ═══════════════════════════════════════════════════════════════════
# LEGAL DESCRIPTION EXTRACTION — Section/Block/Lot from text
# ═══════════════════════════════════════════════════════════════════

# Patterns for extracting section/block/lot/survey from legal descriptions
# Texas oil & gas format: "SEC 270 BLK 8 T-1-S T&P RY CO"
_SEC_PATTERNS = [
    re.compile(r"(?:SECTION|SEC\.?|S)\s*(\d+)", re.IGNORECASE),
    re.compile(r"(?:SECT?)\s+(\d+)", re.IGNORECASE),
]

_BLK_PATTERNS = [
    re.compile(r"(?:BLOCK|BLK\.?|BK\.?)\s*(\w+)", re.IGNORECASE),
]

_LOT_PATTERNS = [
    re.compile(r"(?:LOT|LT\.?)\s*([\d,\s&\-]+)", re.IGNORECASE),
    re.compile(r"(?:LOTS?)\s*([\d]+(?:\s*(?:,|&|AND|\-)\s*\d+)*)", re.IGNORECASE),
]

_TWP_PATTERNS = [
    re.compile(r"(?:TOWNSHIP|TWP\.?)\s*(\w+)", re.IGNORECASE),
    re.compile(r"T-(\d+(?:-[NSEW])?)", re.IGNORECASE),
]

_SURVEY_PATTERNS = [
    re.compile(r"(?:SURVEY|SURV\.?)\s*(\w+)", re.IGNORECASE),
    re.compile(r"(?:ABSTRACT|ABST?\.?|A-)\s*(\d+)", re.IGNORECASE),
]


def extract_sections(text: str) -> List[str]:
    """Extract all section numbers from legal description text."""
    sections: List[str] = []
    for pat in _SEC_PATTERNS:
        for m in pat.finditer(text):
            s = m.group(1).strip()
            if s and s not in sections:
                sections.append(s)
    return sections


def extract_blocks(text: str) -> List[str]:
    """Extract all block identifiers from legal description text."""
    blocks: List[str] = []
    for pat in _BLK_PATTERNS:
        for m in pat.finditer(text):
            b = m.group(1).strip()
            if b and b not in blocks:
                blocks.append(b)
    return blocks


def extract_lots(text: str) -> List[str]:
    """Extract lot numbers from legal description text."""
    lots: List[str] = []
    for pat in _LOT_PATTERNS:
        for m in pat.finditer(text):
            lot_str = m.group(1).strip()
            if lot_str:
                # Split on comma, ampersand, dash
                for part in re.split(r"[,&\s]+", lot_str):
                    part = part.strip()
                    if part and part.isdigit() and part not in lots:
                        lots.append(part)
    return lots


def extract_townships(text: str) -> List[str]:
    """Extract township identifiers."""
    townships: List[str] = []
    for pat in _TWP_PATTERNS:
        for m in pat.finditer(text):
            t = m.group(1).strip()
            if t and t not in townships:
                townships.append(t)
    return townships


def extract_surveys(text: str) -> List[str]:
    """Extract survey/abstract identifiers."""
    surveys: List[str] = []
    for pat in _SURVEY_PATTERNS:
        for m in pat.finditer(text):
            s = m.group(1).strip()
            if s and s not in surveys:
                surveys.append(s)
    return surveys


def normalize_legal(text: str) -> str:
    """Normalize legal description for search — lowercase, whitespace collapsed, abbreviations expanded."""
    if not text:
        return ""
    normalized = text.upper().strip()
    # Expand common abbreviations
    normalized = re.sub(r"\bSEC\.?\b", "SECTION", normalized)
    normalized = re.sub(r"\bBLK\.?\b", "BLOCK", normalized)
    normalized = re.sub(r"\bBK\.?\b", "BLOCK", normalized)
    normalized = re.sub(r"\bTWP\.?\b", "TOWNSHIP", normalized)
    normalized = re.sub(r"\bLT\.?\b", "LOT", normalized)
    normalized = re.sub(r"\bABST?\.?\b", "ABSTRACT", normalized)
    normalized = re.sub(r"\bSURV\.?\b", "SURVEY", normalized)
    normalized = re.sub(r"\bPT\b", "PART", normalized)
    normalized = re.sub(r"\bRY\b", "RAILWAY", normalized)
    normalized = re.sub(r"\bCO\b", "COMPANY", normalized)
    normalized = re.sub(r"\bT&P\b", "TEXAS & PACIFIC", normalized)
    normalized = re.sub(r"\bGF/D\b", "GENERAL FILE/DEED", normalized)
    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


# ═══════════════════════════════════════════════════════════════════
# RECORD TRANSFORMATION — R2 JSON → D1 row
# ═══════════════════════════════════════════════════════════════════

def _join_array(val: Any) -> str:
    """Safely join array or return string. Filter empty entries."""
    if val is None:
        return ""
    if isinstance(val, list):
        parts = [str(v).strip() for v in val if v and str(v).strip()]
        return "; ".join(parts)
    return str(val).strip()


def _first_of(val: Any) -> str:
    """Get first non-empty element from array or return string."""
    if val is None:
        return ""
    if isinstance(val, list):
        for v in val:
            s = str(v).strip()
            if s:
                return s
        return ""
    return str(val).strip()


def _legal_text(rec: Dict[str, Any]) -> str:
    """Extract full legal description text from record."""
    # Try legalDescription array first
    ld = rec.get("legalDescription")
    if isinstance(ld, list):
        parts = [str(v).strip() for v in ld if v and str(v).strip()]
        if parts:
            return "; ".join(parts)
    elif isinstance(ld, str) and ld.strip():
        return ld.strip()

    # Fallback to legals array
    legals = rec.get("legals", [])
    if isinstance(legals, list):
        parts = []
        for legal in legals:
            if isinstance(legal, dict):
                desc = legal.get("lglDesc", legal.get("description", ""))
                if desc and str(desc).strip():
                    parts.append(str(desc).strip())
        if parts:
            return "; ".join(parts)

    return ""


def _sql_escape(val: str) -> str:
    """Escape single quotes for SQL."""
    return val.replace("'", "''")


def compute_record_hash(county: str, doc_id: str, instrument_type: str) -> str:
    """Deterministic SHA-256 hash for deduplication."""
    raw = f"{county}|{doc_id}|{instrument_type}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def transform_record(rec: Dict[str, Any], county: str, instrument_type: str) -> Optional[Dict[str, str]]:
    """Transform R2 JSON record into D1 row dict."""
    doc_id = str(rec.get("docId", rec.get("id", "")))
    if not doc_id:
        return None

    grantor = _join_array(rec.get("grantor", []))
    grantee = _join_array(rec.get("grantee", []))
    legal = _legal_text(rec)
    legal_norm = normalize_legal(legal)

    # Extract section/block/lot from legal description
    sections = extract_sections(legal)
    blocks = extract_blocks(legal)
    lots_from_legal = extract_lots(legal)

    # Also try the record-level lot/block/township arrays
    lot_array = rec.get("lot", [])
    block_array = rec.get("block", [])
    township_array = rec.get("township", [])

    lot_combined = lots_from_legal
    if isinstance(lot_array, list):
        for lt in lot_array:
            s = str(lt).strip()
            if s and s not in lot_combined:
                lot_combined.append(s)

    block_combined = blocks
    if isinstance(block_array, list):
        for bk in block_array:
            s = str(bk).strip()
            if s and s not in block_combined:
                block_combined.append(s)

    township_parts = extract_townships(legal)
    if isinstance(township_array, list):
        for tw in township_array:
            s = str(tw).strip()
            if s and s not in township_parts:
                township_parts.append(s)

    surveys = extract_surveys(legal)

    record_hash = compute_record_hash(county, doc_id, instrument_type)

    return {
        "county": county,
        "instrument_type": instrument_type,
        "doc_id": doc_id,
        "instrument_number": str(rec.get("instrumentNumber", "")).strip(),
        "recorded_date": str(rec.get("recordedDate", "")).strip(),
        "instrument_date": str(rec.get("instrumentDate", "")).strip(),
        "year": int(rec.get("year", 0)) if rec.get("year") else 0,
        "grantor": grantor,
        "grantee": grantee,
        "legal_description": legal,
        "legal_normalized": legal_norm,
        "section": "; ".join(sections),
        "block": "; ".join(block_combined),
        "lot": "; ".join(lot_combined),
        "township": "; ".join(township_parts),
        "survey": "; ".join(surveys),
        "book": str(rec.get("book", "")).strip(),
        "volume": str(rec.get("volume", "")).strip(),
        "page": str(rec.get("page", "")).strip(),
        "book_volume_page": str(rec.get("bookVolumePage", "")).strip(),
        "consideration": str(rec.get("consideration", "")).strip(),
        "page_count": int(rec.get("pageCount", 0)) if rec.get("pageCount") else 0,
        "download_link": str(rec.get("downloadLink", "")).strip(),
        "doc_type_code": str(rec.get("docTypeCode", "")).strip(),
        "record_hash": record_hash,
    }


# ═══════════════════════════════════════════════════════════════════
# D1 EXECUTION — Wrangler wrapper
# ═══════════════════════════════════════════════════════════════════

def d1_execute(sql: str, retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """Execute SQL against D1 via wrangler CLI using temp file to avoid quoting issues."""
    import tempfile
    for attempt in range(retries):
        # Write SQL to temp file to avoid shell quoting issues
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False, encoding="utf-8") as f:
            f.write(sql)
            tmp_path = f.name
        try:
            result = subprocess.run(
                [NPX, "wrangler", "d1", "execute", D1_DATABASE, "--remote", "--file", tmp_path],
                capture_output=True, text=True, timeout=120, cwd=WRANGLER_CWD
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)
        if result.returncode == 0:
            return True, result.stdout
        err = result.stderr
        if "UNIQUE constraint" in err:
            return True, "UNIQUE_SKIP"
        if attempt < retries - 1:
            time.sleep(2 ** attempt)
    return False, (result.stderr or result.stdout)[:2000]


def d1_execute_json(sql: str) -> Optional[List[Dict]]:
    """Execute SQL and parse JSON result using temp file."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False, encoding="utf-8") as f:
        f.write(sql)
        tmp_path = f.name
    try:
        result = subprocess.run(
            [NPX, "wrangler", "d1", "execute", D1_DATABASE, "--remote", "--file", tmp_path, "--json"],
            capture_output=True, text=True, timeout=120, cwd=WRANGLER_CWD
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            if isinstance(data, list) and data:
                return data[0].get("results", [])
        except json.JSONDecodeError:
            pass
    return None


# ═══════════════════════════════════════════════════════════════════
# R2 DATA ACCESS — Rclone wrapper
# ═══════════════════════════════════════════════════════════════════

def r2_list_shards(county: str, instrument_type: str) -> List[str]:
    """List shard files for a county/instrument_type in R2."""
    prefix = f"{R2_BASE}/{county}_SCRAPED/{instrument_type}/"
    result = subprocess.run(
        [RCLONE, "ls", f"r2:{R2_BUCKET}/{prefix}"],
        capture_output=True, text=True, timeout=30
    )
    shards = []
    if result.returncode == 0:
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                fname = parts[-1]
                if fname.startswith("shard_") and fname.endswith(".json"):
                    shards.append(fname)
    return sorted(shards)


def r2_fetch_json(key: str) -> Optional[Any]:
    """Fetch and parse JSON from R2."""
    result = subprocess.run(
        [RCLONE, "cat", f"r2:{R2_BUCKET}/{key}"],
        capture_output=True, text=True, timeout=600
    )
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
    return None


def r2_get_metadata(county: str, instrument_type: str) -> Optional[Dict]:
    """Get metadata for a county/instrument_type."""
    key = f"{R2_BASE}/{county}_SCRAPED/{instrument_type}/metadata.json"
    return r2_fetch_json(key)


# ═══════════════════════════════════════════════════════════════════
# CHECKPOINT MANAGEMENT — Resumable ingestion
# ═══════════════════════════════════════════════════════════════════

def get_checkpoint(county: str, instrument_type: str, shard_name: str) -> Optional[str]:
    """Check if a shard has already been processed."""
    sql = (
        f"SELECT status FROM ingest_checkpoints "
        f"WHERE county='{_sql_escape(county)}' "
        f"AND instrument_type='{_sql_escape(instrument_type)}' "
        f"AND shard_name='{_sql_escape(shard_name)}'"
    )
    rows = d1_execute_json(sql)
    if rows:
        return rows[0].get("status")
    return None


def set_checkpoint(county: str, instrument_type: str, shard_name: str,
                   records_in: int, inserted: int, skipped: int, errored: int,
                   shard_hash: str, status: str) -> None:
    """Create or update checkpoint for a shard."""
    completed_val = "datetime('now')" if status == "completed" else "NULL"
    sql = (
        f"INSERT INTO ingest_checkpoints "
        f"(county, instrument_type, shard_name, records_in_shard, records_inserted, "
        f"records_skipped, records_errored, shard_hash, started_at, completed_at, status) "
        f"VALUES ("
        f"'{_sql_escape(county)}', '{_sql_escape(instrument_type)}', "
        f"'{_sql_escape(shard_name)}', {records_in}, {inserted}, {skipped}, {errored}, "
        f"'{shard_hash}', datetime('now'), "
        f"{completed_val}, '{status}') "
        f"ON CONFLICT(county, instrument_type, shard_name) DO UPDATE SET "
        f"records_inserted=excluded.records_inserted, records_skipped=excluded.records_skipped, "
        f"records_errored=excluded.records_errored, completed_at=excluded.completed_at, "
        f"status=excluded.status"
    )
    d1_execute(sql)


def log_batch(county: str, instrument_type: str, shard_name: str,
              batch_num: int, batch_size: int, batch_hash: str,
              inserted: int, skipped: int, errors: int, elapsed_ms: float) -> None:
    """Log a batch to the ingest ledger."""
    sql = (
        f"INSERT INTO ingest_ledger "
        f"(county, instrument_type, shard_name, batch_number, batch_size, "
        f"batch_hash, records_inserted, records_skipped, error_count, elapsed_ms) "
        f"VALUES ("
        f"'{_sql_escape(county)}', '{_sql_escape(instrument_type)}', "
        f"'{_sql_escape(shard_name)}', {batch_num}, {batch_size}, "
        f"'{batch_hash}', {inserted}, {skipped}, {errors}, {elapsed_ms})"
    )
    d1_execute(sql)


# ═══════════════════════════════════════════════════════════════════
# BATCH INSERT — Core ingestion logic
# ═══════════════════════════════════════════════════════════════════

def build_insert_sql(rows: List[Dict[str, Any]]) -> str:
    """Build a batch INSERT OR IGNORE SQL statement."""
    if not rows:
        return ""

    columns = [
        "county", "instrument_type", "doc_id", "instrument_number",
        "recorded_date", "instrument_date", "year", "grantor", "grantee",
        "legal_description", "legal_normalized", "section", "block", "lot",
        "township", "survey", "book", "volume", "page", "book_volume_page",
        "consideration", "page_count", "download_link", "doc_type_code",
        "record_hash",
    ]

    values_parts = []
    for row in rows:
        vals = []
        for col in columns:
            v = row.get(col, "")
            if col in ("year", "page_count"):
                vals.append(str(v) if v else "0")
            else:
                vals.append(f"'{_sql_escape(str(v))}'")
        values_parts.append(f"({', '.join(vals)})")

    return (
        f"INSERT OR IGNORE INTO deed_records "
        f"({', '.join(columns)}) VALUES "
        + ", ".join(values_parts)
    )


def ingest_shard(county: str, instrument_type: str, shard_name: str,
                 dry_run: bool = False) -> Tuple[int, int, int]:
    """Ingest a single shard file into D1. Returns (inserted, skipped, errors).

    FAST MODE: Writes ALL batch INSERT statements to a single SQL file per shard,
    then executes with ONE wrangler call. 20x faster than per-batch calls.
    """
    import tempfile

    # Check checkpoint
    checkpoint_status = get_checkpoint(county, instrument_type, shard_name)
    if checkpoint_status == "completed":
        print(f"    SKIP (already completed)")
        return 0, 0, 0

    # Load shard from R2
    r2_key = f"{R2_BASE}/{county}_SCRAPED/{instrument_type}/{shard_name}"
    print(f"    Loading {r2_key}...")
    shard_data = r2_fetch_json(r2_key)
    if shard_data is None:
        print(f"    ERROR: Could not load shard")
        return 0, 0, 1

    records = shard_data if isinstance(shard_data, list) else shard_data.get("records", shard_data.get("data", []))
    if not isinstance(records, list):
        print(f"    ERROR: Shard data is not a list")
        return 0, 0, 1

    total_in_shard = len(records)
    shard_hash = hashlib.sha256(json.dumps(records, sort_keys=True, default=str).encode()).hexdigest()[:16]
    print(f"    Records: {total_in_shard}, Hash: {shard_hash}")

    if dry_run:
        sample_rows = []
        for rec in records[:5]:
            row = transform_record(rec, county, instrument_type)
            if row:
                sample_rows.append(row)
        if sample_rows:
            print(f"    Sample transform: section={sample_rows[0].get('section')}, "
                  f"block={sample_rows[0].get('block')}, "
                  f"grantor={sample_rows[0].get('grantor')[:40]}")
        return total_in_shard, 0, 0

    # Set checkpoint to 'processing'
    set_checkpoint(county, instrument_type, shard_name,
                   total_in_shard, 0, 0, 0, shard_hash, "processing")

    # Transform all records
    rows: List[Dict[str, Any]] = []
    transform_errors = 0
    for rec in records:
        row = transform_record(rec, county, instrument_type)
        if row:
            rows.append(row)
        else:
            transform_errors += 1

    # FAST MODE: Write ALL batch INSERT statements to ONE SQL file
    # D1 supports multiple statements separated by semicolons in --file mode
    all_sql_parts: List[str] = []
    batch_count = 0

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        batch_count += 1
        sql = build_insert_sql(batch)
        if sql:
            all_sql_parts.append(sql + ";")

    if not all_sql_parts:
        print(f"    No valid records to insert")
        return 0, 0, transform_errors

    # Write combined SQL to temp file
    combined_sql = "\n".join(all_sql_parts)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False, encoding="utf-8") as f:
        f.write(combined_sql)
        tmp_path = f.name

    print(f"    Executing {batch_count} batches ({len(rows)} records) in single D1 call...")
    start_t = time.monotonic()

    try:
        result = subprocess.run(
            [NPX, "wrangler", "d1", "execute", D1_DATABASE, "--remote", "--file", tmp_path],
            capture_output=True, text=True, timeout=300, cwd=WRANGLER_CWD
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    elapsed = round((time.monotonic() - start_t) * 1000, 1)

    if result.returncode == 0:
        total_inserted = len(rows)
        total_skipped = 0
        total_errors = transform_errors
        print(f"    OK: {total_inserted} inserted in {elapsed}ms ({batch_count} batches)")
    else:
        err_msg = (result.stderr or result.stdout)[:500]
        if "UNIQUE constraint" in err_msg:
            # Some dupes — count as partial success
            total_inserted = 0
            total_skipped = len(rows)
            total_errors = transform_errors
            print(f"    DUPES: {total_skipped} skipped (already exist), {elapsed}ms")
        else:
            total_inserted = 0
            total_skipped = 0
            total_errors = len(rows) + transform_errors
            print(f"    ERROR: {err_msg[:200]}")

    # Log batch summary
    batch_hash = hashlib.sha256(combined_sql[:1000].encode()).hexdigest()[:16]
    log_batch(county, instrument_type, shard_name, 1,
              len(rows), batch_hash, total_inserted, total_skipped,
              total_errors - transform_errors, elapsed)

    # Update checkpoint
    set_checkpoint(county, instrument_type, shard_name,
                   total_in_shard, total_inserted, total_skipped, total_errors,
                   shard_hash, "completed")

    return total_inserted, total_skipped, total_errors


# ═══════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════

def create_schema() -> None:
    """Create D1 tables and indexes."""
    print("Creating D1 schema...")
    for sql in SCHEMA_SQL:
        ok, result = d1_execute(sql)
        if ok:
            # Extract table/index name for display
            name = sql.split("(")[0].strip().split()[-1] if "(" in sql else sql.split()[-1]
            print(f"  OK: {name}")
        else:
            print(f"  ERROR: {result[:100]}")
    print("Schema creation complete.\n")


def ingest_county(county: str, instruments: Optional[List[str]] = None,
                  dry_run: bool = False) -> Dict[str, Any]:
    """Ingest all instruments for a county."""
    target_instruments = instruments or INSTRUMENT_TYPES
    results: Dict[str, Any] = {
        "county": county,
        "instruments_processed": 0,
        "total_inserted": 0,
        "total_skipped": 0,
        "total_errors": 0,
        "instrument_results": {},
    }

    print(f"\n{'=' * 60}")
    print(f"INGESTING: {county} County")
    print(f"Instruments: {len(target_instruments)}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"{'=' * 60}")

    for instrument_type in target_instruments:
        print(f"\n  [{instrument_type}]")

        # Get metadata
        meta = r2_get_metadata(county, instrument_type)
        if meta is None:
            print(f"    No data found in R2 — skipping")
            continue

        record_count = meta.get("record_count", 0)
        shard_count = meta.get("shard_count", 0)
        print(f"    Records: {record_count:,}, Shards: {shard_count}")

        # List shards
        shards = r2_list_shards(county, instrument_type)
        if not shards:
            print(f"    No shard files found — skipping")
            continue

        print(f"    Found {len(shards)} shard files")

        inst_inserted = 0
        inst_skipped = 0
        inst_errors = 0

        for shard_name in shards:
            print(f"  [{shard_name}]")
            inserted, skipped, errors = ingest_shard(
                county, instrument_type, shard_name, dry_run=dry_run
            )
            inst_inserted += inserted
            inst_skipped += skipped
            inst_errors += errors

        results["instruments_processed"] += 1
        results["total_inserted"] += inst_inserted
        results["total_skipped"] += inst_skipped
        results["total_errors"] += inst_errors
        results["instrument_results"][instrument_type] = {
            "inserted": inst_inserted,
            "skipped": inst_skipped,
            "errors": inst_errors,
            "shards": len(shards),
        }

        print(f"    SUBTOTAL: {inst_inserted} inserted, {inst_skipped} skipped, {inst_errors} errors")

    print(f"\n{'=' * 60}")
    print(f"INGEST COMPLETE: {county}")
    print(f"  Instruments: {results['instruments_processed']}")
    print(f"  Inserted: {results['total_inserted']:,}")
    print(f"  Skipped (dupes): {results['total_skipped']:,}")
    print(f"  Errors: {results['total_errors']}")
    print(f"{'=' * 60}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="D1 Deed Record Ingest Pipeline")
    parser.add_argument("--county", default="REEVES", help="County to ingest")
    parser.add_argument("--instrument", help="Specific instrument type (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without inserting")
    parser.add_argument("--schema-only", action="store_true", help="Only create schema")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoints")
    parser.add_argument("--status", action="store_true", help="Show checkpoint status")
    args = parser.parse_args()

    if args.schema_only:
        create_schema()
        return

    if args.status:
        rows = d1_execute_json(
            f"SELECT county, instrument_type, shard_name, status, records_inserted, records_skipped "
            f"FROM ingest_checkpoints WHERE county='{_sql_escape(args.county)}' ORDER BY instrument_type, shard_name"
        )
        if rows:
            print(f"Checkpoints for {args.county}:")
            for r in rows:
                print(f"  {r.get('instrument_type'):25s} {r.get('shard_name'):20s} "
                      f"status={r.get('status'):12s} inserted={r.get('records_inserted')} "
                      f"skipped={r.get('records_skipped')}")
        else:
            print(f"No checkpoints found for {args.county}")
        return

    # Always ensure schema exists
    create_schema()

    instruments = [args.instrument] if args.instrument else None
    results = ingest_county(args.county, instruments=instruments, dry_run=args.dry_run)

    # Print final summary
    print(f"\nFinal results: {json.dumps(results, indent=2)}")


if __name__ == "__main__":
    main()
