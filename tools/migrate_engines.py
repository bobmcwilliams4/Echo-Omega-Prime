"""
Engine Migration Tool — Quality-scored dedupe + tier restructure.

Reads engine dirs from source, scores by quality (not size), deduplicates,
and copies winners into the monorepo tier structure.

Usage:
    python tools/migrate_engines.py --source O:/ECHO_OMEGA_PRIME/SYSTEMS/engines --dest engines/ --report
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


class EngineScore(NamedTuple):
    engine_id: str
    path: Path
    score: int
    lines: int
    doctrine_count: int
    citation_count: int
    has_health: bool
    has_fastapi: bool
    placeholder_count: int


# Map tier prefix → (tier_number, tier_name)
TIER_MAP: dict[str, tuple[int, str]] = {
    "LG": (1, "legal"), "LIE": (1, "legal"),
    "LM": (2, "landman"), "LMIE": (2, "landman"),
    "TX": (3, "tax"),
    "PRB": (4, "probate"), "P": (4, "probate"),
    "REG": (5, "regulatory"), "R": (5, "regulatory"),
    "ENT": (6, "enterprise"), "E": (6, "enterprise"),
    "SYN": (7, "synthesis"), "S": (7, "synthesis"), "SYNTIE": (7, "synthesis"),
    "W": (8, "water_env"),
    "G": (9, "geospatial"), "GEO": (9, "geospatial"),
    "I": (10, "intelligence"), "INT": (10, "intelligence"),
    "ET": (11, "echo_talk"),
    "GS": (12, "gs343"),
    "GOV": (13, "governance"),
    "DRL": (14, "drilling"), "DRLIE": (14, "drilling"),
    "MECH": (15, "mechanical"), "MECHIE": (15, "mechanical"),
    "AUTO": (16, "automotive"), "AUTOIE": (16, "automotive"),
    "AERO": (17, "aerospace"), "AEROIE": (17, "aerospace"),
    "ENRG": (18, "energy"), "ENRGIE": (18, "energy"),
    "MED": (19, "medical"), "MEDIE": (19, "medical"),
    "OFE": (20, "oilfield_equipment"), "OFEIE": (20, "oilfield_equipment"),
    "RAIL": (21, "railroad"), "RAILIE": (21, "railroad"),
    "FRAC": (22, "fracturing"), "FRACIE": (22, "fracturing"),
    "PROD": (23, "production"), "PRODIE": (23, "production"),
    "CHEM": (24, "chemistry"), "CHEMIE": (24, "chemistry"),
    "MATH": (25, "mathematics"), "MATHIE": (25, "mathematics"),
    "AGI": (26, "agi"), "AGIIE": (26, "agi"),
    "BLD": (27, "bloodline"), "BLDIE": (27, "bloodline"),
    "ENCORE": (28, "encore"),
}

CITATION_PATTERNS = [
    r"IRC §", r"Rev\. Rul\.", r"API RP", r"SPE ", r"USC §", r"CFR §",
    r"OSHA", r"EPA", r"NIST", r"IEEE", r"ASTM", r"ANSI",
    r"Treas\. Reg\.", r"PLR \d", r"TAM \d", r"GCM \d",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b", r"(?m)^\s+pass\s*$", r"NotImplementedError", r'"""\.\.\."""',
    r"raise\s+NotImplementedError",
]


def score_engine(engine_dir: Path) -> EngineScore | None:
    """Score an engine by quality, not size."""
    engine_py = engine_dir / "engine.py"
    if not engine_py.exists():
        # Try alternate names
        candidates = list(engine_dir.glob("*_engine.py")) + list(engine_dir.glob("*engine*.py"))
        if not candidates:
            return None
        engine_py = candidates[0]

    try:
        code = engine_py.read_text(errors="ignore")
    except Exception:
        return None

    lines = len(code.splitlines())
    if lines < 50:
        return None

    score = 0

    # Real DoctrineBlock instances (+2 each, max 20)
    doctrine_count = code.count("DoctrineBlock(")
    score += min(20, doctrine_count * 2)

    # Placeholder penalty (-2 each)
    placeholder_count = 0
    for pat in PLACEHOLDER_PATTERNS:
        hits = len(re.findall(pat, code))
        placeholder_count += hits
        score -= hits * 2

    # Real citations (+1 each, max 15)
    citation_count = 0
    for pat in CITATION_PATTERNS:
        hits = len(re.findall(pat, code))
        citation_count += hits
        score += min(3, hits)

    # Import sanity (+3 each)
    has_fastapi = "from fastapi" in code or "import fastapi" in code
    score += has_fastapi * 3
    score += ("from loguru" in code) * 3
    score += ("from pydantic" in code) * 3

    # Health endpoint (+5)
    has_health = '"/health"' in code or "'/health'" in code
    score += has_health * 5

    # Lines bonus (diminishing returns)
    if lines >= 2000:
        score += 10
    elif lines >= 1000:
        score += 7
    elif lines >= 500:
        score += 4
    elif lines >= 200:
        score += 2

    # Extract engine_id from dir name
    dir_name = engine_dir.name
    engine_id = dir_name.split("_")[0].upper() if "_" in dir_name else dir_name.upper()

    return EngineScore(
        engine_id=engine_id,
        path=engine_dir,
        score=score,
        lines=lines,
        doctrine_count=doctrine_count,
        citation_count=citation_count,
        has_health=has_health,
        has_fastapi=has_fastapi,
        placeholder_count=placeholder_count,
    )


def get_tier_dir(engine_id: str) -> str:
    """Map engine ID to tier directory name."""
    # Try progressively shorter prefixes
    for length in range(len(engine_id), 0, -1):
        prefix = engine_id[:length]
        # Remove trailing digits
        alpha = re.sub(r"\d+$", "", prefix)
        if alpha in TIER_MAP:
            num, name = TIER_MAP[alpha]
            return f"tier_{num:02d}_{name}"
    return "tier_99_unclassified"


def migrate(source: Path, dest: Path, dry_run: bool = False) -> dict:
    """Run the full migration with quality-scored deduplication."""
    # Scan all engine dirs
    all_scores: list[EngineScore] = []
    skipped: list[str] = []

    for entry in sorted(source.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_") or entry.name.startswith("."):
            continue

        result = score_engine(entry)
        if result:
            all_scores.append(result)
        else:
            skipped.append(entry.name)

    # Group by engine_id — keep highest score (dedupe)
    by_id: dict[str, list[EngineScore]] = defaultdict(list)
    for s in all_scores:
        by_id[s.engine_id].append(s)

    winners: list[EngineScore] = []
    duplicates: list[tuple[str, int]] = []  # (id, count)
    for eid, scores in by_id.items():
        scores.sort(key=lambda x: x.score, reverse=True)
        winners.append(scores[0])
        if len(scores) > 1:
            duplicates.append((eid, len(scores)))

    # Organize into tier dirs
    tier_counts: dict[str, int] = defaultdict(int)
    copied = 0

    for w in winners:
        tier_dir_name = get_tier_dir(w.engine_id)
        target = dest / tier_dir_name / w.path.name
        tier_counts[tier_dir_name] += 1

        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copytree(w.path, target, dirs_exist_ok=True)
                copied += 1

    # Copy _shared dir
    shared_src = source / "_shared"
    if shared_src.exists() and not dry_run:
        shared_dest = dest / "_shared"
        shared_dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(shared_src, shared_dest, dirs_exist_ok=True)

    return {
        "total_scanned": len(all_scores) + len(skipped),
        "scored": len(all_scores),
        "skipped": len(skipped),
        "unique_engines": len(winners),
        "duplicates_found": len(duplicates),
        "duplicate_details": duplicates,
        "tiers": dict(tier_counts),
        "copied": copied,
        "top_engines": sorted(winners, key=lambda x: x.score, reverse=True)[:20],
        "bottom_engines": sorted(winners, key=lambda x: x.score)[:10],
        "skipped_dirs": skipped[:20],
    }


def main():
    parser = argparse.ArgumentParser(description="Migrate engines with quality-scored dedup")
    parser.add_argument("--source", required=True, help="Source engine directory")
    parser.add_argument("--dest", required=True, help="Destination engines/ in monorepo")
    parser.add_argument("--dry-run", action="store_true", help="Score only, don't copy")
    parser.add_argument("--report", action="store_true", help="Write migration report")
    args = parser.parse_args()

    source = Path(args.source)
    dest = Path(args.dest)

    if not source.exists():
        print(f"Source not found: {source}")
        return

    result = migrate(source, dest, dry_run=args.dry_run)

    print(f"\n{'DRY RUN' if args.dry_run else 'MIGRATION'} COMPLETE")
    print(f"  Scanned:    {result['total_scanned']}")
    print(f"  Scored:     {result['scored']}")
    print(f"  Unique:     {result['unique_engines']}")
    print(f"  Duplicates: {result['duplicates_found']}")
    print(f"  Copied:     {result['copied']}")
    print(f"\n  Tiers:")
    for tier, count in sorted(result["tiers"].items()):
        print(f"    {tier}: {count}")

    if result["duplicates_found"]:
        print(f"\n  Duplicate IDs (kept highest score):")
        for eid, count in result["duplicate_details"][:20]:
            print(f"    {eid}: {count} copies")

    print(f"\n  Top 10 by quality score:")
    for e in result["top_engines"][:10]:
        print(f"    {e.engine_id:12s} score={e.score:3d}  lines={e.lines:6d}  doctrines={e.doctrine_count:3d}  citations={e.citation_count:3d}")

    print(f"\n  Bottom 5 by quality score:")
    for e in result["bottom_engines"][:5]:
        print(f"    {e.engine_id:12s} score={e.score:3d}  lines={e.lines:6d}  placeholders={e.placeholder_count:3d}")

    if args.report:
        report_path = dest.parent / "config" / "engine_migration_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_data = {
            "total_scanned": result["total_scanned"],
            "unique_engines": result["unique_engines"],
            "duplicates_found": result["duplicates_found"],
            "tiers": result["tiers"],
            "engines": [
                {
                    "engine_id": e.engine_id,
                    "score": e.score,
                    "lines": e.lines,
                    "doctrine_count": e.doctrine_count,
                    "citation_count": e.citation_count,
                    "has_health": e.has_health,
                    "has_fastapi": e.has_fastapi,
                    "placeholder_count": e.placeholder_count,
                    "source_path": str(e.path),
                }
                for e in sorted(result["top_engines"], key=lambda x: x.engine_id)
            ],
        }
        report_path.write_text(json.dumps(report_data, indent=2))
        print(f"\n  Report written to: {report_path}")


if __name__ == "__main__":
    main()
