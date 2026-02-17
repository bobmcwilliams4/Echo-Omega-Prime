"""
Generate a self-contained task package for building an engine.

Reads the tier spec, extracts the engine definition, substitutes into
the build prompt, and produces a single JSON that any builder can consume.

Usage:
    python tools/generate_task_package.py --spec specs/tier_20_ofe.json --engine OFE01
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def generate_task_package(spec_path: Path, engine_id: str) -> dict:
    """Generate a complete, self-contained task package."""
    spec = json.loads(spec_path.read_text())

    # Find the engine in the spec
    engine = None
    for e in spec.get("engines", []):
        if e["engine_id"] == engine_id:
            engine = e
            break

    if not engine:
        raise ValueError(f"Engine {engine_id} not found in {spec_path}")

    tier_prefix = spec["tier_prefix"]
    tier_name = spec["tier_name"]
    eid_lower = engine_id.lower()

    build_prompt = f"""[SYSTEM DIRECTIVE — TIE-GRADE ENGINE BUILD]

Build engine {engine_id} ({engine['name']}) for ECHO OMEGA PRIME.
Tier: {tier_prefix} ({tier_name})
Domain: {spec['domain_description']}

AUTHORITY SOURCES: {', '.join(spec['authority_sources'])}

ENGINE FUNCTION: {engine['function']}

DOCTRINE TOPICS TO COVER:
{chr(10).join(f'  - {t}' for t in engine['doctrine_topics'])}

OUTPUT: Write complete Python engine file with ALL 20 TIE components.
Each file as a fenced code block with filename as info string.

FILES:
1. ```python:{eid_lower}_engine.py — Main engine (2000+ lines, 30+ DoctrineBlock, 100+ semantic entries)
2. ```json:{eid_lower}_config.json — Configuration
3. ```json:{eid_lower}_doctrines.json — Doctrine cache (50+ blocks)
4. ```python:{eid_lower}_telemetry.py — Telemetry module

THE 20 MANDATORY COMPONENTS: three_layer_response, response_modes, doctrine_cache,
authority_hardening, confidence_stratification, semantic_normalization, vector_search,
telemetry_module, doctrine_drift_watcher, doctrine_coverage_map, metrics_collector,
health_endpoint, zoned_analysis, fact_fragility_scoring, audit_trail_jsonl,
determinism_hash_sha256, fastapi_server, loguru_logging, multi_doctrine_decomposition,
deep_analysis_mode.

CODE STANDARDS: Python 3.11, type hints everywhere, Pydantic models, loguru logging,
pathlib paths. ZERO placeholders, ZERO TODOs, ZERO stubs.

CRITICAL: Every DoctrineBlock must have REAL domain content with REAL citations.
Output ONLY the code. No explanations."""

    task_package = {
        "task_id": f"build_{engine_id}_{datetime.now(timezone.utc).strftime('%Y%m%d')}",
        "engine_id": engine_id,
        "tier_prefix": tier_prefix,
        "tier_name": tier_name,
        "output_mode": "engine_files",
        "domain_context": {
            "function": engine["function"],
            "doctrine_topics": engine["doctrine_topics"],
            "authority_sources": spec["authority_sources"],
        },
        "build_prompt": build_prompt,
        "eval_pack": engine.get("eval_pack", {"golden_queries": [], "min_pass_rate": 0.7}),
        "quality_gates": [
            {"gate": "EVAL_PACK", "weight": 50, "criteria": "70%+ golden queries pass"},
            {"gate": "DOCTRINE_COUNT", "weight": 20, "criteria": ">= 30 blocks"},
            {"gate": "CITATION_DENSITY", "weight": 15, "criteria": ">= 2 citations/block avg"},
            {"gate": "SYNTAX", "weight": 10, "criteria": "py_compile passes"},
            {"gate": "NO_PLACEHOLDERS", "weight": 5, "criteria": "zero TODO/pass/NotImplementedError"},
        ],
        "callback_url": "https://echo-build-orchestrator.bmcii1976.workers.dev/build/complete",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    return task_package


def main():
    parser = argparse.ArgumentParser(description="Generate self-contained task package")
    parser.add_argument("--spec", required=True, help="Path to tier spec JSON")
    parser.add_argument("--engine", required=True, help="Engine ID (e.g., OFE01)")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    pkg = generate_task_package(Path(args.spec), args.engine)

    output = json.dumps(pkg, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Task package written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
