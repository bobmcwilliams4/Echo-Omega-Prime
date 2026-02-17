"""
FORGE-X Autonomous Launcher — Wires everything together for 24/7 autonomous building.

Usage:
  python forge_x_launcher.py                  # Start FORGE-X API server (port 8875)
  python forge_x_launcher.py --daemon         # Start API + autonomous build daemon
  python forge_x_launcher.py --build OFE01    # Build a single engine immediately
  python forge_x_launcher.py --batch CHEM     # Build all engines in a category
  python forge_x_launcher.py --scan           # Scan fleet and report status
  python forge_x_launcher.py --plan           # Parse master build plan, queue all unbuilt
"""
import sys
import os
import re
import asyncio
import json
import time
from pathlib import Path

# Ensure engine dir is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load Azure key from environment (set via .env or vault — never hardcode)
AZURE_KEY = os.environ.get("AZURE_ECHOOMEGA_KEY", "")

# Also load from .env if it exists (override)
ENV_PATH = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/deepseek-proxy/.env")
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("AZURE_ECHOOMEGA_KEY="):
            os.environ["AZURE_ECHOOMEGA_KEY"] = line.split("=", 1)[1].strip().strip('"')

from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}")
logger.add("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/_forge_x_logs/forge_x_{time:YYYY-MM-DD}.log",
           rotation="10 MB", retention="30 days", level="DEBUG")


# ═══════════════════════════════════════════════════════════════════════════
# MASTER BUILD PLAN PARSER — Reads the 2000-engine plan and extracts specs
# ═══════════════════════════════════════════════════════════════════════════

MASTER_PLAN_PATH = Path("O:/ECHO_OMEGA_PRIME/_DOCS/GPT_KNOWLEDGE/master_build_plan.md")
ENGINES_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines")

# Port assignment ranges per category
PORT_RANGES = {
    "LG": (8400, 8449), "LM": (8450, 8499), "TX": (8500, 8549),
    "P": (8550, 8569), "PRB": (8550, 8569), "R": (8570, 8599), "REG": (8570, 8599),
    "E": (8600, 8629), "ENT": (8600, 8629), "S": (8630, 8659), "SYN": (8630, 8659),
    "W": (8660, 8679), "G": (8680, 8699), "GEO": (8680, 8699),
    "I": (8700, 8719), "INT": (8700, 8719), "ET": (8720, 8739),
    "GS": (8740, 8749), "GOV": (8750, 8769), "MATH": (8770, 8799),
    "BLD": (8800, 8819), "CHEM": (8820, 8859), "DRL": (8860, 8889),
    "MECH": (8890, 8919), "AUTO": (8920, 8949), "AERO": (8950, 8969),
    "ENRG": (8970, 8999), "MED": (9000, 9029), "OFE": (9030, 9069),
    "RAIL": (9070, 9089), "FRAC": (9090, 9119), "PROD": (9120, 9149),
    "AGI": (8870, 8889),
}


def get_existing_engines() -> set:
    """Scan disk for existing engine directories."""
    existing = set()
    for d in ENGINES_DIR.iterdir():
        if d.is_dir() and (d / "engine.py").exists():
            # Extract engine_id prefix (e.g., "CHEM01" from "CHEM01_chemical_analysis")
            name = d.name.upper()
            parts = name.split("_")
            if parts:
                existing.add(parts[0])
    return existing


def parse_master_plan() -> list:
    """Parse the master build plan and extract engine specs.

    The plan uses category-level entries like:
        | Chemistry | CHEM | 20 | 29,374 | ... | COMPLETE |
    We expand "CHEM 20" into CHEM01, CHEM02, ... CHEM20.
    """
    if not MASTER_PLAN_PATH.exists():
        logger.warning(f"Master plan not found: {MASTER_PLAN_PATH}")
        return _hardcoded_engine_list()

    content = MASTER_PLAN_PATH.read_text(encoding="utf-8", errors="replace")
    specs = []
    seen_codes = set()

    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| -") or line.startswith("| Tier") or line.startswith("| Category") or line.startswith("| Engine") or line.startswith("| Domain"):
            continue

        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3:
            continue

        # Look for pattern: | Name | CODE | COUNT |
        code = None
        count = 0
        name = ""

        for i, part in enumerate(parts):
            # Code is 2-6 uppercase letters
            clean = part.strip().replace("*", "")
            if re.match(r'^[A-Z]{1,6}$', clean) and clean in PORT_RANGES:
                code = clean
                name = parts[i - 1] if i > 0 else clean
                # Count is usually next field
                for j in range(i + 1, len(parts)):
                    try:
                        count = int(parts[j].replace(",", "").strip())
                        if 1 <= count <= 50:
                            break
                    except ValueError:
                        continue
                break

            # Also match backbone entries: | Tax Intelligence Engine | TIE | 16,367 | ...
            if re.match(r'^[A-Z]{2,8}$', clean) and len(clean) >= 2:
                # Check if it's a known backbone
                backbone_ids = {"TIE", "PIE", "ARCS", "LIE", "LMIE", "CHEMIE", "DRLIE",
                               "MECHIE", "AUTOIE", "AEROIE", "ENRGIE", "MEDIE", "OFEIE",
                               "RAILIE", "FRACIE", "PRODIE", "MATHIE"}
                if clean in backbone_ids:
                    if clean not in seen_codes:
                        seen_codes.add(clean)
                        specs.append({
                            "engine_id": clean,
                            "name": parts[0] if parts[0] != clean else clean,
                            "port": 8391,
                            "category": "backbone",
                            "domain": clean.lower(),
                        })

        if code and count > 0 and code not in seen_codes:
            seen_codes.add(code)
            port_range = PORT_RANGES.get(code, (9200, 9999))
            for n in range(1, count + 1):
                eid = f"{code}{n:02d}"
                specs.append({
                    "engine_id": eid,
                    "name": f"{name} {n:02d}".strip(),
                    "port": port_range[0] + n,
                    "category": name,
                    "domain": name.lower().replace(" ", "_"),
                })

    if not specs:
        return _hardcoded_engine_list()
    return specs


def _hardcoded_engine_list() -> list:
    """Fallback engine list based on known categories and counts."""
    categories = {
        "LG": ("Legal", 18), "LM": ("Landman", 24), "TX": ("Tax", 14),
        "P": ("Probate", 8), "REG": ("Regulatory", 12), "ENT": ("Enterprise", 12),
        "SYN": ("Synthesis", 8), "W": ("Water/Environmental", 6),
        "GEO": ("Geospatial", 5), "INT": ("Intelligence", 7),
        "ET": ("Echo Talk", 8), "GS": ("GS343", 4), "GOV": ("Governance", 4),
        "MATH": ("Mathematics", 12), "BLD": ("Bloodline", 6),
        "CHEM": ("Chemistry", 20), "DRL": ("Drilling", 15),
        "MECH": ("Mechanical", 15), "AUTO": ("Automotive", 15),
        "AERO": ("Aviation", 10), "ENRG": ("Energy", 15),
        "MED": ("Medical", 15), "OFE": ("Oilfield Equipment", 15),
        "RAIL": ("Railroad", 8), "FRAC": ("Fracturing", 10),
        "PROD": ("Production", 10), "AGI": ("AGI", 8),
    }
    specs = []
    for code, (name, count) in categories.items():
        port_range = PORT_RANGES.get(code, (9200, 9999))
        for n in range(1, count + 1):
            eid = f"{code}{n:02d}"
            specs.append({
                "engine_id": eid,
                "name": f"{name} {n:02d}",
                "port": port_range[0] + n,
                "category": name,
                "domain": name.lower().replace(" ", "_"),
            })
    return specs


def get_unbuilt_engines() -> list:
    """Compare master plan to disk, return unbuilt engine specs."""
    existing = get_existing_engines()
    all_specs = parse_master_plan()
    unbuilt = [s for s in all_specs if s["engine_id"] not in existing]
    logger.info(f"Master plan: {len(all_specs)} engines, {len(existing)} on disk, {len(unbuilt)} unbuilt")
    return unbuilt


# ═══════════════════════════════════════════════════════════════════════════
# ENHANCED DAEMON — Reads master plan + orchestrator, builds autonomously
# ═══════════════════════════════════════════════════════════════════════════

async def run_autonomous_daemon(max_concurrent: int = 3, poll_interval: int = 60):
    """Run the autonomous build daemon.

    Flow:
    1. Parse master build plan for unbuilt engines
    2. Also poll orchestrator for PLANNED engines
    3. Merge and deduplicate
    4. Build with priority ordering
    5. Report results to orchestrator + OmniSync + Brain
    6. Generate support files for completed engines
    7. Loop forever
    """
    from engine import (EngineBuilder, AutoBuildDaemon, BuildRequest, BuildReporter,
                        BuildPriority, EngineType, BuildStatus, SyntaxValidator,
                        TIEComplianceChecker, SecretScanner, FleetScanner)
    import aiohttp

    builder = EngineBuilder(azure_key=os.environ["AZURE_ECHOOMEGA_KEY"])
    logger.info("=" * 60)
    logger.info("FORGE-X AUTONOMOUS BUILD DAEMON v2.0")
    logger.info(f"Azure Key: ...{os.environ['AZURE_ECHOOMEGA_KEY'][-8:]}")
    logger.info(f"Max Concurrent: {max_concurrent}")
    logger.info(f"Poll Interval: {poll_interval}s")
    logger.info("=" * 60)

    # Initial scan
    fleet = FleetScanner.scan()
    logger.info(f"Fleet: {fleet['total']} engines, {fleet['valid']} valid, {fleet['total_lines']:,} lines")

    # Parse master plan
    unbuilt = get_unbuilt_engines()
    if unbuilt:
        logger.info(f"Queuing {len(unbuilt)} unbuilt engines from master plan")

    builds_completed = 0
    builds_failed = 0
    total_lines = 0

    while True:
        try:
            # Refresh unbuilt list periodically
            if builds_completed % 10 == 0:
                unbuilt = get_unbuilt_engines()

            if not unbuilt:
                logger.info("All engines built! Sleeping 5 minutes...")
                await asyncio.sleep(300)
                unbuilt = get_unbuilt_engines()
                continue

            # Pick next engine
            spec = unbuilt.pop(0)
            engine_id = spec["engine_id"]
            logger.info(f"[{engine_id}] Building: {spec['name']} (port {spec['port']})")

            # Create build request
            request = BuildRequest(
                engine_id=engine_id,
                engine_name=spec["name"],
                domain=spec.get("domain", "general"),
                port=spec["port"],
                priority=BuildPriority.MEDIUM,
                target_lines=4000,
                max_retries=3,
            )

            # Build
            result = await builder.build_engine(request)

            if result.status == BuildStatus.COMPLETE:
                builds_completed += 1
                total_lines += result.lines_written
                logger.info(f"[{engine_id}] COMPLETE — {result.lines_written} lines, "
                           f"{result.build_time_seconds:.0f}s, {len(result.fixes_applied)} fixes")

                # Report to all systems
                try:
                    await BuildReporter.report_to_orchestrator(engine_id, result)
                    await BuildReporter.notify_omnisync(engine_id, result)
                    await BuildReporter.store_to_brain(engine_id, result)
                except Exception as e:
                    logger.warning(f"Report failed: {e}")

            else:
                builds_failed += 1
                logger.error(f"[{engine_id}] {result.status.value}: {result.error_message}")

            # Progress report every 10 engines
            if (builds_completed + builds_failed) % 10 == 0:
                logger.info(f"PROGRESS: {builds_completed} built, {builds_failed} failed, "
                           f"{total_lines:,} lines, {len(unbuilt)} remaining")

            # Rate limit awareness
            await asyncio.sleep(poll_interval)

        except KeyboardInterrupt:
            logger.info("Daemon stopped by user")
            break
        except Exception as e:
            logger.error(f"Daemon error: {e}")
            await asyncio.sleep(30)

    # Final report
    logger.info("=" * 60)
    logger.info(f"DAEMON SESSION COMPLETE")
    logger.info(f"  Built: {builds_completed}")
    logger.info(f"  Failed: {builds_failed}")
    logger.info(f"  Lines: {total_lines:,}")
    logger.info("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════
# SINGLE ENGINE BUILD — Quick CLI build
# ═══════════════════════════════════════════════════════════════════════════

async def build_single(engine_id: str, name: str = "", port: int = 0):
    """Build a single engine by ID."""
    from engine import EngineBuilder, BuildRequest, BuildReporter, BuildStatus

    if not name:
        name = engine_id.lower()
    if not port:
        prefix = ''.join(c for c in engine_id if c.isalpha())
        port_range = PORT_RANGES.get(prefix, (9200, 9999))
        num = int(''.join(c for c in engine_id if c.isdigit()) or "0")
        port = port_range[0] + num

    builder = EngineBuilder(azure_key=os.environ["AZURE_ECHOOMEGA_KEY"])
    request = BuildRequest(engine_id=engine_id, engine_name=name, port=port, target_lines=4000)
    result = await builder.build_engine(request)

    if result.status == BuildStatus.COMPLETE:
        logger.info(f"SUCCESS: {engine_id} — {result.lines_written} lines in {result.build_time_seconds:.0f}s")
        await BuildReporter.report_to_orchestrator(engine_id, result)
    else:
        logger.error(f"FAILED: {engine_id} — {result.error_message}")

    return result


async def build_batch(category: str):
    """Build all unbuilt engines in a category."""
    unbuilt = get_unbuilt_engines()
    category_engines = [e for e in unbuilt if e["engine_id"].startswith(category.upper())]
    logger.info(f"Building {len(category_engines)} {category} engines")

    for spec in category_engines:
        result = await build_single(spec["engine_id"], spec["name"], spec["port"])
        await asyncio.sleep(30)  # Rate limit buffer


# ═══════════════════════════════════════════════════════════════════════════
# FLEET SCAN — Quick status report
# ═══════════════════════════════════════════════════════════════════════════

def scan_fleet():
    """Scan and report fleet status."""
    from engine import FleetScanner, TIEComplianceChecker

    fleet = FleetScanner.scan()
    print(f"\n{'='*60}")
    print(f"FORGE-X FLEET SCAN")
    print(f"{'='*60}")
    print(f"  Engines: {fleet['total']} ({fleet['valid']} valid, {fleet['invalid']} invalid)")
    print(f"  Lines:   {fleet['total_lines']:,}")
    print(f"\n  By Domain:")
    for domain, info in sorted(fleet['by_domain'].items()):
        print(f"    {domain:<10} {info['count']:>3} engines  {info['lines']:>8,} lines")

    unbuilt = get_unbuilt_engines()
    print(f"\n  Unbuilt (from master plan): {len(unbuilt)}")
    if unbuilt:
        categories = {}
        for e in unbuilt:
            prefix = ''.join(c for c in e["engine_id"] if c.isalpha())
            categories.setdefault(prefix, []).append(e["engine_id"])
        for cat in sorted(categories):
            print(f"    {cat}: {len(categories[cat])} — {', '.join(categories[cat][:5])}"
                  f"{'...' if len(categories[cat]) > 5 else ''}")
    print(f"{'='*60}\n")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="FORGE-X Autonomous Engine Factory")
    parser.add_argument("--daemon", action="store_true", help="Start autonomous build daemon")
    parser.add_argument("--build", type=str, help="Build single engine by ID (e.g., OFE01)")
    parser.add_argument("--batch", type=str, help="Build all engines in category (e.g., CHEM)")
    parser.add_argument("--scan", action="store_true", help="Scan fleet and report")
    parser.add_argument("--plan", action="store_true", help="Parse master plan, show unbuilt")
    parser.add_argument("--server", action="store_true", help="Start FastAPI server only")
    parser.add_argument("--concurrent", type=int, default=3, help="Max concurrent builds (daemon)")
    parser.add_argument("--interval", type=int, default=60, help="Poll interval seconds (daemon)")
    args = parser.parse_args()

    if args.scan:
        scan_fleet()
        return

    if args.plan:
        unbuilt = get_unbuilt_engines()
        for e in unbuilt:
            print(f"  {e['engine_id']:<12} {e['name']:<40} port={e['port']}")
        return

    if args.build:
        asyncio.run(build_single(args.build))
        return

    if args.batch:
        asyncio.run(build_batch(args.batch))
        return

    if args.daemon:
        logger.info("Starting FORGE-X in DAEMON mode")
        asyncio.run(run_autonomous_daemon(
            max_concurrent=args.concurrent,
            poll_interval=args.interval,
        ))
        return

    # Default: start FastAPI server
    import uvicorn
    from engine import app, ENGINE_NAME, ENGINE_VERSION, ENGINE_PORT
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")


if __name__ == "__main__":
    main()
