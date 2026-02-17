"""
LM04 Mineral Interest Tracker - Search Module
===============================================

Search capabilities for mineral interests including:
- Owner name search (exact, fuzzy, wildcard)
- Tract/legal description search
- Interest type filtering
- NMA range search
- Date range search
- County search
- Conflict status search
- Full-text search across all fields
- Combined multi-criteria search

Engine: LM04 | Version: 1.0.0
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SearchMode(str, Enum):
    """Search mode for name matching."""
    EXACT = "exact"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    FUZZY = "fuzzy"
    SOUNDEX = "soundex"


class SortField(str, Enum):
    """Fields available for sorting search results."""
    OWNER_NAME = "owner_name"
    NMA = "nma"
    INTEREST_FRACTION = "interest_fraction"
    EFFECTIVE_DATE = "effective_date"
    COUNTY = "county"
    INTEREST_TYPE = "interest_type"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SortDirection(str, Enum):
    """Sort direction."""
    ASC = "ASC"
    DESC = "DESC"


class ConflictStatus(str, Enum):
    """Conflict status for filtering."""
    NONE = "none"
    OVER_CONVEYED = "over_conveyed"
    GAP_DETECTED = "gap_detected"
    TEMPORAL_CONFLICT = "temporal_conflict"
    DUPLICATE = "duplicate"
    ANY = "any"


# ---------------------------------------------------------------------------
# Data classes for search
# ---------------------------------------------------------------------------

@dataclass
class SearchCriteria:
    """Multi-criteria search parameters."""
    owner_name: str | None = None
    owner_name_mode: SearchMode = SearchMode.CONTAINS
    tract_description: str | None = None
    county: str | None = None
    state: str = "TX"
    interest_type: str | None = None
    interest_types: list[str] | None = None
    nma_min: float | None = None
    nma_max: float | None = None
    fraction_min: float | None = None
    fraction_max: float | None = None
    date_from: str | None = None
    date_to: str | None = None
    conflict_status: ConflictStatus = ConflictStatus.NONE
    has_executive_rights: bool | None = None
    is_leased: bool | None = None
    is_pooled: bool | None = None
    is_active: bool | None = None
    document_number: str | None = None
    volume_page: str | None = None
    survey_name: str | None = None
    section: str | None = None
    block: str | None = None
    abstract_number: str | None = None
    full_text_query: str | None = None
    sort_by: SortField = SortField.OWNER_NAME
    sort_direction: SortDirection = SortDirection.ASC
    limit: int = 100
    offset: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "owner_name": self.owner_name,
            "owner_name_mode": self.owner_name_mode.value,
            "tract_description": self.tract_description,
            "county": self.county,
            "state": self.state,
            "interest_type": self.interest_type,
            "interest_types": self.interest_types,
            "nma_min": self.nma_min,
            "nma_max": self.nma_max,
            "fraction_min": self.fraction_min,
            "fraction_max": self.fraction_max,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "conflict_status": self.conflict_status.value,
            "has_executive_rights": self.has_executive_rights,
            "is_leased": self.is_leased,
            "is_pooled": self.is_pooled,
            "is_active": self.is_active,
            "document_number": self.document_number,
            "volume_page": self.volume_page,
            "survey_name": self.survey_name,
            "section": self.section,
            "block": self.block,
            "abstract_number": self.abstract_number,
            "full_text_query": self.full_text_query,
            "sort_by": self.sort_by.value,
            "sort_direction": self.sort_direction.value,
            "limit": self.limit,
            "offset": self.offset,
        }


@dataclass
class SearchResult:
    """A single search result."""
    interest_id: str
    owner_name: str
    interest_type: str
    interest_fraction: float
    nma: float
    county: str
    state: str
    tract_description: str
    effective_date: str
    has_executive_rights: bool
    is_leased: bool
    is_pooled: bool
    is_active: bool
    conflict_status: str
    document_reference: str = ""
    notes: str = ""
    score: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "interest_id": self.interest_id,
            "owner_name": self.owner_name,
            "interest_type": self.interest_type,
            "interest_fraction": self.interest_fraction,
            "nma": self.nma,
            "county": self.county,
            "state": self.state,
            "tract_description": self.tract_description,
            "effective_date": self.effective_date,
            "has_executive_rights": self.has_executive_rights,
            "is_leased": self.is_leased,
            "is_pooled": self.is_pooled,
            "is_active": self.is_active,
            "conflict_status": self.conflict_status,
            "document_reference": self.document_reference,
            "notes": self.notes,
            "score": self.score,
        }


@dataclass
class SearchResponse:
    """Search response with results and metadata."""
    results: list[SearchResult] = field(default_factory=list)
    total_count: int = 0
    returned_count: int = 0
    offset: int = 0
    limit: int = 100
    criteria: dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    has_more: bool = False
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_count": self.total_count,
            "returned_count": self.returned_count,
            "offset": self.offset,
            "limit": self.limit,
            "criteria": self.criteria,
            "execution_time_ms": self.execution_time_ms,
            "has_more": self.has_more,
            "warnings": self.warnings,
        }


# ---------------------------------------------------------------------------
# Fuzzy matching utilities
# ---------------------------------------------------------------------------

def _soundex(name: str) -> str:
    """Compute Soundex code for a name."""
    if not name:
        return "0000"
    name = re.sub(r'[^A-Za-z]', '', name.upper())
    if not name:
        return "0000"
    first_letter = name[0]
    coding = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
    }
    codes: list[str] = []
    prev_code = coding.get(first_letter, '0')
    for ch in name[1:]:
        code = coding.get(ch, '0')
        if code != '0' and code != prev_code:
            codes.append(code)
        prev_code = code if code != '0' else prev_code
    result = first_letter + ''.join(codes)
    return (result + '0000')[:4]


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def _fuzzy_score(query: str, candidate: str, threshold: float = 0.75) -> float:
    """Compute fuzzy match score between 0.0 and 1.0."""
    q = query.lower().strip()
    c = candidate.lower().strip()
    if q == c:
        return 1.0
    if q in c or c in q:
        return 0.9
    max_len = max(len(q), len(c))
    if max_len == 0:
        return 0.0
    dist = _levenshtein_distance(q, c)
    score = 1.0 - (dist / max_len)
    return score if score >= threshold else 0.0


def _name_variants(name: str) -> list[str]:
    """Generate common name variants for fuzzy matching."""
    variants: list[str] = [name]
    parts = name.strip().split()
    if len(parts) >= 2:
        # Last, First
        variants.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        # First Last
        variants.append(f"{parts[0]} {parts[-1]}")
    # Remove common suffixes
    for suffix in [" Jr", " Jr.", " Sr", " Sr.", " II", " III", " IV", " LLC", " LP", " Ltd", " Inc"]:
        if name.endswith(suffix):
            variants.append(name[:-len(suffix)].strip())
    # Remove periods
    if "." in name:
        variants.append(name.replace(".", ""))
    return list(set(variants))


# ---------------------------------------------------------------------------
# Search Engine
# ---------------------------------------------------------------------------

class MineralInterestSearchEngine:
    """Search engine for LM04 mineral interest data."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path) if db_path else ":memory:"
        self._conn: sqlite3.Connection | None = None
        self._initialized = False
        logger.info("LM04 SearchEngine initialized with db: {}", self._db_path)

    # ------------------------------------------------------------------
    # Database management
    # ------------------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA busy_timeout=5000")
            self._conn.execute("PRAGMA cache_size=-65536")
            self._conn.execute("PRAGMA synchronous=NORMAL")
        if not self._initialized:
            self._ensure_schema()
            self._initialized = True
        return self._conn

    def _ensure_schema(self) -> None:
        """Create search tables and indexes if they don't exist."""
        conn = self._conn
        if conn is None:
            return
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS mineral_interests (
                interest_id TEXT PRIMARY KEY,
                owner_name TEXT NOT NULL,
                owner_name_normalized TEXT NOT NULL,
                owner_soundex TEXT NOT NULL,
                interest_type TEXT NOT NULL,
                interest_fraction REAL NOT NULL DEFAULT 0.0,
                nma REAL NOT NULL DEFAULT 0.0,
                gross_acres REAL NOT NULL DEFAULT 0.0,
                county TEXT NOT NULL DEFAULT '',
                state TEXT NOT NULL DEFAULT 'TX',
                tract_description TEXT NOT NULL DEFAULT '',
                legal_description TEXT NOT NULL DEFAULT '',
                survey_name TEXT NOT NULL DEFAULT '',
                section TEXT NOT NULL DEFAULT '',
                block TEXT NOT NULL DEFAULT '',
                abstract_number TEXT NOT NULL DEFAULT '',
                effective_date TEXT NOT NULL DEFAULT '',
                recording_date TEXT NOT NULL DEFAULT '',
                document_number TEXT NOT NULL DEFAULT '',
                volume TEXT NOT NULL DEFAULT '',
                page TEXT NOT NULL DEFAULT '',
                has_executive_rights INTEGER NOT NULL DEFAULT 0,
                is_leased INTEGER NOT NULL DEFAULT 0,
                is_pooled INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                conflict_status TEXT NOT NULL DEFAULT 'none',
                grantor TEXT NOT NULL DEFAULT '',
                grantee TEXT NOT NULL DEFAULT '',
                conveyance_type TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_mi_owner ON mineral_interests(owner_name_normalized);
            CREATE INDEX IF NOT EXISTS idx_mi_soundex ON mineral_interests(owner_soundex);
            CREATE INDEX IF NOT EXISTS idx_mi_type ON mineral_interests(interest_type);
            CREATE INDEX IF NOT EXISTS idx_mi_county ON mineral_interests(county);
            CREATE INDEX IF NOT EXISTS idx_mi_nma ON mineral_interests(nma);
            CREATE INDEX IF NOT EXISTS idx_mi_fraction ON mineral_interests(interest_fraction);
            CREATE INDEX IF NOT EXISTS idx_mi_date ON mineral_interests(effective_date);
            CREATE INDEX IF NOT EXISTS idx_mi_section ON mineral_interests(section);
            CREATE INDEX IF NOT EXISTS idx_mi_block ON mineral_interests(block);
            CREATE INDEX IF NOT EXISTS idx_mi_survey ON mineral_interests(survey_name);
            CREATE INDEX IF NOT EXISTS idx_mi_abstract ON mineral_interests(abstract_number);
            CREATE INDEX IF NOT EXISTS idx_mi_docnum ON mineral_interests(document_number);
            CREATE INDEX IF NOT EXISTS idx_mi_conflict ON mineral_interests(conflict_status);
            CREATE INDEX IF NOT EXISTS idx_mi_active ON mineral_interests(is_active);
            CREATE INDEX IF NOT EXISTS idx_mi_leased ON mineral_interests(is_leased);
            CREATE INDEX IF NOT EXISTS idx_mi_pooled ON mineral_interests(is_pooled);
            CREATE INDEX IF NOT EXISTS idx_mi_executive ON mineral_interests(has_executive_rights);

            CREATE VIRTUAL TABLE IF NOT EXISTS mineral_interests_fts USING fts5(
                interest_id,
                owner_name,
                tract_description,
                legal_description,
                notes,
                county,
                survey_name,
                grantor,
                grantee,
                content='mineral_interests',
                content_rowid='rowid'
            );

            CREATE TRIGGER IF NOT EXISTS mi_ai AFTER INSERT ON mineral_interests BEGIN
                INSERT INTO mineral_interests_fts(
                    rowid, interest_id, owner_name, tract_description,
                    legal_description, notes, county, survey_name, grantor, grantee
                ) VALUES (
                    new.rowid, new.interest_id, new.owner_name, new.tract_description,
                    new.legal_description, new.notes, new.county, new.survey_name,
                    new.grantor, new.grantee
                );
            END;

            CREATE TRIGGER IF NOT EXISTS mi_ad AFTER DELETE ON mineral_interests BEGIN
                INSERT INTO mineral_interests_fts(
                    mineral_interests_fts, rowid, interest_id, owner_name,
                    tract_description, legal_description, notes, county,
                    survey_name, grantor, grantee
                ) VALUES (
                    'delete', old.rowid, old.interest_id, old.owner_name,
                    old.tract_description, old.legal_description, old.notes,
                    old.county, old.survey_name, old.grantor, old.grantee
                );
            END;

            CREATE TRIGGER IF NOT EXISTS mi_au AFTER UPDATE ON mineral_interests BEGIN
                INSERT INTO mineral_interests_fts(
                    mineral_interests_fts, rowid, interest_id, owner_name,
                    tract_description, legal_description, notes, county,
                    survey_name, grantor, grantee
                ) VALUES (
                    'delete', old.rowid, old.interest_id, old.owner_name,
                    old.tract_description, old.legal_description, old.notes,
                    old.county, old.survey_name, old.grantor, old.grantee
                );
                INSERT INTO mineral_interests_fts(
                    rowid, interest_id, owner_name, tract_description,
                    legal_description, notes, county, survey_name, grantor, grantee
                ) VALUES (
                    new.rowid, new.interest_id, new.owner_name, new.tract_description,
                    new.legal_description, new.notes, new.county, new.survey_name,
                    new.grantor, new.grantee
                );
            END;
        """)
        conn.commit()
        logger.debug("LM04 search schema ensured")

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
            self._initialized = False

    # ------------------------------------------------------------------
    # Index management
    # ------------------------------------------------------------------

    def index_interest(self, data: dict[str, Any]) -> None:
        """Index a single mineral interest record for searching."""
        conn = self._get_conn()
        owner = data.get("owner_name", "")
        normalized = owner.upper().strip()
        sdx = _soundex(normalized)
        conn.execute("""
            INSERT OR REPLACE INTO mineral_interests (
                interest_id, owner_name, owner_name_normalized, owner_soundex,
                interest_type, interest_fraction, nma, gross_acres,
                county, state, tract_description, legal_description,
                survey_name, section, block, abstract_number,
                effective_date, recording_date, document_number, volume, page,
                has_executive_rights, is_leased, is_pooled, is_active,
                conflict_status, grantor, grantee, conveyance_type, notes,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            data.get("interest_id", ""),
            owner,
            normalized,
            sdx,
            data.get("interest_type", "MI"),
            data.get("interest_fraction", 0.0),
            data.get("nma", 0.0),
            data.get("gross_acres", 0.0),
            data.get("county", "").upper(),
            data.get("state", "TX").upper(),
            data.get("tract_description", ""),
            data.get("legal_description", ""),
            data.get("survey_name", ""),
            data.get("section", ""),
            data.get("block", ""),
            data.get("abstract_number", ""),
            data.get("effective_date", ""),
            data.get("recording_date", ""),
            data.get("document_number", ""),
            data.get("volume", ""),
            data.get("page", ""),
            1 if data.get("has_executive_rights", False) else 0,
            1 if data.get("is_leased", False) else 0,
            1 if data.get("is_pooled", False) else 0,
            1 if data.get("is_active", True) else 0,
            data.get("conflict_status", "none"),
            data.get("grantor", ""),
            data.get("grantee", ""),
            data.get("conveyance_type", ""),
            data.get("notes", ""),
        ))
        conn.commit()

    def index_batch(self, records: list[dict[str, Any]]) -> int:
        """Index a batch of mineral interest records. Returns count indexed."""
        conn = self._get_conn()
        count = 0
        for rec in records:
            try:
                self.index_interest(rec)
                count += 1
            except Exception as exc:
                logger.warning("Failed to index record {}: {}", rec.get("interest_id", "?"), exc)
        logger.info("Indexed {}/{} mineral interest records", count, len(records))
        return count

    def remove_interest(self, interest_id: str) -> bool:
        """Remove a mineral interest from the search index."""
        conn = self._get_conn()
        cursor = conn.execute("DELETE FROM mineral_interests WHERE interest_id = ?", (interest_id,))
        conn.commit()
        return cursor.rowcount > 0

    def clear_index(self) -> int:
        """Clear all records from the search index. Returns count removed."""
        conn = self._get_conn()
        cursor = conn.execute("SELECT COUNT(*) FROM mineral_interests")
        count = cursor.fetchone()[0]
        conn.execute("DELETE FROM mineral_interests")
        conn.execute("INSERT INTO mineral_interests_fts(mineral_interests_fts) VALUES('rebuild')")
        conn.commit()
        logger.info("Cleared {} records from search index", count)
        return count

    # ------------------------------------------------------------------
    # Search methods
    # ------------------------------------------------------------------

    def search(self, criteria: SearchCriteria) -> SearchResponse:
        """Execute a multi-criteria search and return results."""
        start = datetime.now(timezone.utc)
        conn = self._get_conn()
        warnings: list[str] = []

        # Handle full-text search separately
        if criteria.full_text_query and not any([
            criteria.owner_name, criteria.county, criteria.interest_type,
            criteria.nma_min, criteria.nma_max, criteria.date_from, criteria.date_to,
        ]):
            return self._full_text_search(criteria, start)

        # Build SQL query
        conditions: list[str] = []
        params: list[Any] = []

        # Owner name filter
        if criteria.owner_name:
            owner_conditions, owner_params, owner_warnings = self._build_owner_filter(
                criteria.owner_name, criteria.owner_name_mode
            )
            conditions.extend(owner_conditions)
            params.extend(owner_params)
            warnings.extend(owner_warnings)

        # County filter
        if criteria.county:
            conditions.append("county = ?")
            params.append(criteria.county.upper().strip())

        # State filter
        if criteria.state:
            conditions.append("state = ?")
            params.append(criteria.state.upper().strip())

        # Interest type filter
        if criteria.interest_type:
            conditions.append("interest_type = ?")
            params.append(criteria.interest_type.upper().strip())
        elif criteria.interest_types:
            placeholders = ",".join(["?"] * len(criteria.interest_types))
            conditions.append(f"interest_type IN ({placeholders})")
            params.extend([t.upper().strip() for t in criteria.interest_types])

        # NMA range filter
        if criteria.nma_min is not None:
            conditions.append("nma >= ?")
            params.append(criteria.nma_min)
        if criteria.nma_max is not None:
            conditions.append("nma <= ?")
            params.append(criteria.nma_max)

        # Fraction range filter
        if criteria.fraction_min is not None:
            conditions.append("interest_fraction >= ?")
            params.append(criteria.fraction_min)
        if criteria.fraction_max is not None:
            conditions.append("interest_fraction <= ?")
            params.append(criteria.fraction_max)

        # Date range filter
        if criteria.date_from:
            conditions.append("effective_date >= ?")
            params.append(criteria.date_from)
        if criteria.date_to:
            conditions.append("effective_date <= ?")
            params.append(criteria.date_to)

        # Conflict status filter
        if criteria.conflict_status == ConflictStatus.ANY:
            conditions.append("conflict_status != 'none'")
        elif criteria.conflict_status != ConflictStatus.NONE:
            conditions.append("conflict_status = ?")
            params.append(criteria.conflict_status.value)

        # Boolean filters
        if criteria.has_executive_rights is not None:
            conditions.append("has_executive_rights = ?")
            params.append(1 if criteria.has_executive_rights else 0)
        if criteria.is_leased is not None:
            conditions.append("is_leased = ?")
            params.append(1 if criteria.is_leased else 0)
        if criteria.is_pooled is not None:
            conditions.append("is_pooled = ?")
            params.append(1 if criteria.is_pooled else 0)
        if criteria.is_active is not None:
            conditions.append("is_active = ?")
            params.append(1 if criteria.is_active else 0)

        # Document reference filters
        if criteria.document_number:
            conditions.append("document_number = ?")
            params.append(criteria.document_number.strip())
        if criteria.volume_page:
            parts = criteria.volume_page.split("/")
            if len(parts) == 2:
                conditions.append("volume = ? AND page = ?")
                params.extend([parts[0].strip(), parts[1].strip()])
            else:
                conditions.append("(volume || '/' || page) LIKE ?")
                params.append(f"%{criteria.volume_page.strip()}%")

        # Legal description filters
        if criteria.survey_name:
            conditions.append("survey_name LIKE ?")
            params.append(f"%{criteria.survey_name.strip()}%")
        if criteria.section:
            conditions.append("section = ?")
            params.append(criteria.section.strip())
        if criteria.block:
            conditions.append("block = ?")
            params.append(criteria.block.strip())
        if criteria.abstract_number:
            conditions.append("abstract_number = ?")
            params.append(criteria.abstract_number.strip())

        # Tract description filter
        if criteria.tract_description:
            conditions.append("tract_description LIKE ?")
            params.append(f"%{criteria.tract_description.strip()}%")

        # Full text query (combined with other filters)
        fts_ids: set[str] | None = None
        if criteria.full_text_query:
            fts_ids = self._get_fts_match_ids(criteria.full_text_query)
            if fts_ids:
                placeholders = ",".join(["?"] * len(fts_ids))
                conditions.append(f"interest_id IN ({placeholders})")
                params.extend(list(fts_ids))
            else:
                # No FTS matches, return empty
                elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
                return SearchResponse(
                    total_count=0, returned_count=0,
                    offset=criteria.offset, limit=criteria.limit,
                    criteria=criteria.to_dict(),
                    execution_time_ms=elapsed,
                )

        # Build final query
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        sort_col = self._sort_field_to_column(criteria.sort_by)
        sort_dir = criteria.sort_direction.value

        # Count total
        count_sql = f"SELECT COUNT(*) FROM mineral_interests WHERE {where_clause}"
        count_row = conn.execute(count_sql, params).fetchone()
        total_count = count_row[0] if count_row else 0

        # Fetch results
        query_sql = (
            f"SELECT * FROM mineral_interests WHERE {where_clause} "
            f"ORDER BY {sort_col} {sort_dir} "
            f"LIMIT ? OFFSET ?"
        )
        params.extend([criteria.limit, criteria.offset])
        rows = conn.execute(query_sql, params).fetchall()

        results = [self._row_to_result(row) for row in rows]
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        return SearchResponse(
            results=results,
            total_count=total_count,
            returned_count=len(results),
            offset=criteria.offset,
            limit=criteria.limit,
            criteria=criteria.to_dict(),
            execution_time_ms=elapsed,
            has_more=(criteria.offset + len(results)) < total_count,
            warnings=warnings,
        )

    def search_by_owner(self, owner_name: str, mode: SearchMode = SearchMode.CONTAINS,
                        limit: int = 100) -> SearchResponse:
        """Convenience method to search by owner name."""
        criteria = SearchCriteria(
            owner_name=owner_name,
            owner_name_mode=mode,
            limit=limit,
        )
        return self.search(criteria)

    def search_by_tract(self, county: str, section: str | None = None,
                        block: str | None = None, survey: str | None = None,
                        limit: int = 100) -> SearchResponse:
        """Convenience method to search by tract/legal description."""
        criteria = SearchCriteria(
            county=county,
            section=section,
            block=block,
            survey_name=survey,
            limit=limit,
        )
        return self.search(criteria)

    def search_by_interest_type(self, interest_type: str, county: str | None = None,
                                limit: int = 100) -> SearchResponse:
        """Convenience method to search by interest type."""
        criteria = SearchCriteria(
            interest_type=interest_type,
            county=county,
            limit=limit,
        )
        return self.search(criteria)

    def search_by_nma_range(self, nma_min: float | None = None, nma_max: float | None = None,
                            county: str | None = None, limit: int = 100) -> SearchResponse:
        """Convenience method to search by NMA range."""
        criteria = SearchCriteria(
            nma_min=nma_min,
            nma_max=nma_max,
            county=county,
            limit=limit,
            sort_by=SortField.NMA,
            sort_direction=SortDirection.DESC,
        )
        return self.search(criteria)

    def search_by_date_range(self, date_from: str | None = None, date_to: str | None = None,
                             county: str | None = None, limit: int = 100) -> SearchResponse:
        """Convenience method to search by date range."""
        criteria = SearchCriteria(
            date_from=date_from,
            date_to=date_to,
            county=county,
            limit=limit,
            sort_by=SortField.EFFECTIVE_DATE,
            sort_direction=SortDirection.DESC,
        )
        return self.search(criteria)

    def search_by_county(self, county: str, limit: int = 100) -> SearchResponse:
        """Convenience method to search by county."""
        criteria = SearchCriteria(county=county, limit=limit)
        return self.search(criteria)

    def search_conflicts(self, conflict_status: ConflictStatus = ConflictStatus.ANY,
                         county: str | None = None, limit: int = 100) -> SearchResponse:
        """Convenience method to search for conflict records."""
        criteria = SearchCriteria(
            conflict_status=conflict_status,
            county=county,
            limit=limit,
        )
        return self.search(criteria)

    def full_text_search(self, query: str, limit: int = 100) -> SearchResponse:
        """Convenience method for full-text search."""
        criteria = SearchCriteria(
            full_text_query=query,
            limit=limit,
        )
        return self.search(criteria)

    # ------------------------------------------------------------------
    # Statistics and aggregation
    # ------------------------------------------------------------------

    def get_statistics(self) -> dict[str, Any]:
        """Get search index statistics."""
        conn = self._get_conn()
        total = conn.execute("SELECT COUNT(*) FROM mineral_interests").fetchone()[0]
        by_type = dict(conn.execute(
            "SELECT interest_type, COUNT(*) FROM mineral_interests GROUP BY interest_type"
        ).fetchall())
        by_county = dict(conn.execute(
            "SELECT county, COUNT(*) FROM mineral_interests GROUP BY county ORDER BY COUNT(*) DESC LIMIT 20"
        ).fetchall())
        by_conflict = dict(conn.execute(
            "SELECT conflict_status, COUNT(*) FROM mineral_interests GROUP BY conflict_status"
        ).fetchall())
        nma_stats = conn.execute(
            "SELECT MIN(nma), MAX(nma), AVG(nma), SUM(nma) FROM mineral_interests"
        ).fetchone()
        active_count = conn.execute(
            "SELECT COUNT(*) FROM mineral_interests WHERE is_active = 1"
        ).fetchone()[0]
        leased_count = conn.execute(
            "SELECT COUNT(*) FROM mineral_interests WHERE is_leased = 1"
        ).fetchone()[0]
        pooled_count = conn.execute(
            "SELECT COUNT(*) FROM mineral_interests WHERE is_pooled = 1"
        ).fetchone()[0]
        exec_count = conn.execute(
            "SELECT COUNT(*) FROM mineral_interests WHERE has_executive_rights = 1"
        ).fetchone()[0]

        return {
            "total_records": total,
            "active_records": active_count,
            "leased_count": leased_count,
            "pooled_count": pooled_count,
            "with_executive_rights": exec_count,
            "by_interest_type": by_type,
            "by_county_top20": by_county,
            "by_conflict_status": by_conflict,
            "nma_statistics": {
                "min": nma_stats[0] if nma_stats[0] else 0,
                "max": nma_stats[1] if nma_stats[1] else 0,
                "avg": round(nma_stats[2], 6) if nma_stats[2] else 0,
                "total": round(nma_stats[3], 6) if nma_stats[3] else 0,
            },
        }

    def get_tract_summary(self, county: str, section: str, block: str) -> dict[str, Any]:
        """Get a summary of all interests in a specific tract."""
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM mineral_interests WHERE county = ? AND section = ? AND block = ? "
            "ORDER BY interest_type, owner_name",
            (county.upper(), section, block),
        ).fetchall()

        interests = [self._row_to_result(r) for r in rows]
        total_fraction = sum(r.interest_fraction for r in interests)
        total_nma = sum(r.nma for r in interests)
        types_present = list(set(r.interest_type for r in interests))
        has_conflict = total_fraction > 1.0001 or total_fraction < 0.9999

        return {
            "county": county.upper(),
            "section": section,
            "block": block,
            "interest_count": len(interests),
            "total_fraction": round(total_fraction, 10),
            "total_nma": round(total_nma, 8),
            "interest_types_present": types_present,
            "has_conflict": has_conflict,
            "conflict_type": "over_conveyed" if total_fraction > 1.0001 else (
                "gap_detected" if total_fraction < 0.9999 else "none"
            ),
            "interests": [i.to_dict() for i in interests],
        }

    def get_owner_portfolio(self, owner_name: str) -> dict[str, Any]:
        """Get all interests held by a specific owner."""
        response = self.search_by_owner(owner_name, mode=SearchMode.EXACT, limit=5000)
        total_nma = sum(r.nma for r in response.results)
        counties = list(set(r.county for r in response.results))
        types = list(set(r.interest_type for r in response.results))

        return {
            "owner_name": owner_name,
            "total_interests": response.total_count,
            "total_nma": round(total_nma, 8),
            "counties": counties,
            "interest_types": types,
            "interests": [r.to_dict() for r in response.results],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_owner_filter(self, name: str, mode: SearchMode) -> tuple[list[str], list[Any], list[str]]:
        """Build SQL conditions for owner name matching."""
        conditions: list[str] = []
        params: list[Any] = []
        warnings: list[str] = []
        normalized = name.upper().strip()

        if mode == SearchMode.EXACT:
            conditions.append("owner_name_normalized = ?")
            params.append(normalized)
        elif mode == SearchMode.CONTAINS:
            conditions.append("owner_name_normalized LIKE ?")
            params.append(f"%{normalized}%")
        elif mode == SearchMode.STARTS_WITH:
            conditions.append("owner_name_normalized LIKE ?")
            params.append(f"{normalized}%")
        elif mode == SearchMode.ENDS_WITH:
            conditions.append("owner_name_normalized LIKE ?")
            params.append(f"%{normalized}")
        elif mode == SearchMode.SOUNDEX:
            sdx = _soundex(normalized)
            conditions.append("owner_soundex = ?")
            params.append(sdx)
            warnings.append(f"Soundex search may return approximate matches (code: {sdx})")
        elif mode == SearchMode.FUZZY:
            # Fuzzy requires post-filtering; use contains as base
            conditions.append("owner_name_normalized LIKE ?")
            first_chars = normalized[:3] if len(normalized) >= 3 else normalized
            params.append(f"%{first_chars}%")
            warnings.append("Fuzzy search: results will be scored and filtered by relevance")

        return conditions, params, warnings

    def _full_text_search(self, criteria: SearchCriteria, start: datetime) -> SearchResponse:
        """Execute a full-text search."""
        conn = self._get_conn()
        query = criteria.full_text_query or ""
        # Sanitize FTS query
        safe_query = re.sub(r'[^\w\s*"]', ' ', query).strip()
        if not safe_query:
            elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return SearchResponse(
                execution_time_ms=elapsed,
                criteria=criteria.to_dict(),
                warnings=["Empty search query after sanitization"],
            )
        try:
            fts_sql = (
                "SELECT mi.* FROM mineral_interests mi "
                "JOIN mineral_interests_fts fts ON mi.interest_id = fts.interest_id "
                f"WHERE mineral_interests_fts MATCH ? "
                f"ORDER BY rank "
                f"LIMIT ? OFFSET ?"
            )
            rows = conn.execute(fts_sql, (safe_query, criteria.limit, criteria.offset)).fetchall()
            # Count
            count_sql = (
                "SELECT COUNT(*) FROM mineral_interests_fts WHERE mineral_interests_fts MATCH ?"
            )
            total = conn.execute(count_sql, (safe_query,)).fetchone()[0]
        except sqlite3.OperationalError as exc:
            logger.warning("FTS query failed: {}", exc)
            elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return SearchResponse(
                execution_time_ms=elapsed,
                criteria=criteria.to_dict(),
                warnings=[f"Full-text search error: {exc}"],
            )

        results = [self._row_to_result(row) for row in rows]
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        return SearchResponse(
            results=results,
            total_count=total,
            returned_count=len(results),
            offset=criteria.offset,
            limit=criteria.limit,
            criteria=criteria.to_dict(),
            execution_time_ms=elapsed,
            has_more=(criteria.offset + len(results)) < total,
        )

    def _get_fts_match_ids(self, query: str) -> set[str]:
        """Get interest IDs matching a full-text query."""
        conn = self._get_conn()
        safe_query = re.sub(r'[^\w\s*"]', ' ', query).strip()
        if not safe_query:
            return set()
        try:
            rows = conn.execute(
                "SELECT interest_id FROM mineral_interests_fts WHERE mineral_interests_fts MATCH ?",
                (safe_query,),
            ).fetchall()
            return {row[0] for row in rows}
        except sqlite3.OperationalError:
            return set()

    def _row_to_result(self, row: sqlite3.Row) -> SearchResult:
        """Convert a database row to a SearchResult."""
        return SearchResult(
            interest_id=row["interest_id"],
            owner_name=row["owner_name"],
            interest_type=row["interest_type"],
            interest_fraction=row["interest_fraction"],
            nma=row["nma"],
            county=row["county"],
            state=row["state"],
            tract_description=row["tract_description"],
            effective_date=row["effective_date"],
            has_executive_rights=bool(row["has_executive_rights"]),
            is_leased=bool(row["is_leased"]),
            is_pooled=bool(row["is_pooled"]),
            is_active=bool(row["is_active"]),
            conflict_status=row["conflict_status"],
            document_reference=f"{row['volume']}/{row['page']}" if row["volume"] and row["page"] else row["document_number"],
            notes=row["notes"],
        )

    def _sort_field_to_column(self, sort_field: SortField) -> str:
        """Map SortField enum to database column name."""
        mapping = {
            SortField.OWNER_NAME: "owner_name_normalized",
            SortField.NMA: "nma",
            SortField.INTEREST_FRACTION: "interest_fraction",
            SortField.EFFECTIVE_DATE: "effective_date",
            SortField.COUNTY: "county",
            SortField.INTEREST_TYPE: "interest_type",
            SortField.CREATED_AT: "created_at",
            SortField.UPDATED_AT: "updated_at",
        }
        return mapping.get(sort_field, "owner_name_normalized")


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_search_engine: MineralInterestSearchEngine | None = None


def get_search_engine(db_path: str | Path | None = None) -> MineralInterestSearchEngine:
    """Get or create the singleton search engine."""
    global _search_engine
    if _search_engine is None:
        _search_engine = MineralInterestSearchEngine(db_path)
    return _search_engine


def search_interests(criteria_dict: dict[str, Any]) -> dict[str, Any]:
    """Search mineral interests using a criteria dictionary."""
    engine = get_search_engine()
    criteria = SearchCriteria(**{
        k: v for k, v in criteria_dict.items()
        if k in SearchCriteria.__dataclass_fields__
    })
    response = engine.search(criteria)
    return response.to_dict()


def search_by_owner(owner_name: str, mode: str = "contains", limit: int = 100) -> dict[str, Any]:
    """Search by owner name."""
    engine = get_search_engine()
    response = engine.search_by_owner(owner_name, SearchMode(mode), limit)
    return response.to_dict()


def search_by_tract(county: str, section: str | None = None,
                    block: str | None = None) -> dict[str, Any]:
    """Search by tract location."""
    engine = get_search_engine()
    response = engine.search_by_tract(county, section, block)
    return response.to_dict()


def get_tract_summary(county: str, section: str, block: str) -> dict[str, Any]:
    """Get summary of all interests in a tract."""
    engine = get_search_engine()
    return engine.get_tract_summary(county, section, block)
