"""
Engine Validator — Runs quality gates on an engine directory.

Checks: syntax, placeholders, doctrine count, citation density, eval pack.
Returns exit code 0 if passes, 1 if fails.

Usage:
    python tools/validate_engine.py engines/tier_20_ofe/OFE01_mud_pump_analysis/
    python tools/validate_engine.py engines/tier_01_legal/LG01_contract_analysis/ --spec specs/tier_01_legal.json
"""
from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from pathlib import Path


PLACEHOLDER_PATTERNS = [
    (r"\bTODO\b", "TODO comment"),
    (r"(?m)^\s+pass\s*$", "standalone pass"),
    (r"NotImplementedError", "NotImplementedError"),
    (r'"""\.\.\."""', "ellipsis docstring"),
]

CITATION_PATTERNS = [
    r"IRC §", r"Rev\. Rul\.", r"API RP", r"SPE ", r"USC §", r"CFR §",
    r"OSHA", r"EPA", r"NIST", r"IEEE", r"ASTM", r"ANSI",
    r"Treas\. Reg\.", r"PLR \d", r"TAM \d",
]


def check_syntax(engine_dir: Path) -> tuple[bool, list[str]]:
    """py_compile all .py files. Returns (passed, errors)."""
    errors = []
    for py_file in engine_dir.rglob("*.py"):
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"{py_file.name}: {e}")
    return len(errors) == 0, errors


def check_placeholders(code: str) -> tuple[bool, list[str]]:
    """Check for placeholder code. Returns (passed, findings)."""
    findings = []
    for pattern, label in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, code)
        if matches:
            findings.append(f"{label}: {len(matches)} occurrences")
    return len(findings) == 0, findings


def count_doctrines(code: str) -> int:
    """Count DoctrineBlock instances."""
    return code.count("DoctrineBlock(")


def count_citations(code: str) -> int:
    """Count real citations across all patterns."""
    total = 0
    for pat in CITATION_PATTERNS:
        total += len(re.findall(pat, code))
    return total


def run_eval_pack(code: str, eval_pack: dict) -> tuple[float, list[dict]]:
    """
    Run eval pack golden queries against engine code.
    Checks if required_elements are present and failure_signals are absent.
    Returns (pass_rate, results).
    """
    queries = eval_pack.get("golden_queries", [])
    if not queries:
        return 1.0, []

    results = []
    passed = 0

    for q in queries:
        question = q["question"]
        required = q.get("required_elements", [])
        failures = q.get("failure_signals", [])

        # Check if engine code contains evidence it can handle this query
        code_lower = code.lower()
        required_found = sum(1 for r in required if r.lower() in code_lower)
        failure_found = sum(1 for f in failures if f.lower() in code_lower)

        # Pass if >50% of required elements found and <50% of failure signals
        req_rate = required_found / len(required) if required else 1.0
        fail_rate = failure_found / len(failures) if failures else 0.0

        q_passed = req_rate >= 0.5 and fail_rate < 0.5
        if q_passed:
            passed += 1

        results.append({
            "question": question[:80],
            "passed": q_passed,
            "required_found": f"{required_found}/{len(required)}",
            "failure_signals": f"{failure_found}/{len(failures)}",
        })

    pass_rate = passed / len(queries) if queries else 1.0
    return pass_rate, results


def validate(engine_dir: Path, spec_path: Path | None = None) -> dict:
    """Run all quality gates on an engine directory."""
    engine_dir = Path(engine_dir)
    results = {"engine_dir": str(engine_dir), "gates": [], "passed": True}

    # Find main engine file
    engine_py = engine_dir / "engine.py"
    if not engine_py.exists():
        candidates = list(engine_dir.glob("*_engine.py"))
        engine_py = candidates[0] if candidates else None

    if not engine_py or not engine_py.exists():
        results["gates"].append({"gate": "FILE_EXISTS", "passed": False, "detail": "No engine.py found"})
        results["passed"] = False
        return results

    code = engine_py.read_text(errors="ignore")

    # Gate 1: Syntax
    syntax_ok, syntax_errors = check_syntax(engine_dir)
    results["gates"].append({
        "gate": "SYNTAX", "weight": 10, "passed": syntax_ok,
        "detail": "OK" if syntax_ok else "; ".join(syntax_errors[:3]),
    })

    # Gate 2: Placeholders
    placeholder_ok, placeholder_findings = check_placeholders(code)
    results["gates"].append({
        "gate": "NO_PLACEHOLDERS", "weight": 5, "passed": placeholder_ok,
        "detail": "OK" if placeholder_ok else "; ".join(placeholder_findings),
    })

    # Gate 3: Doctrine count
    doctrine_count = count_doctrines(code)
    doctrine_ok = doctrine_count >= 10
    results["gates"].append({
        "gate": "DOCTRINE_COUNT", "weight": 20, "passed": doctrine_ok,
        "detail": f"{doctrine_count} DoctrineBlock instances (min 10)",
    })

    # Gate 4: Citation density
    citation_count = count_citations(code)
    citation_density = citation_count / max(doctrine_count, 1)
    citation_ok = citation_density >= 1.0
    results["gates"].append({
        "gate": "CITATION_DENSITY", "weight": 15, "passed": citation_ok,
        "detail": f"{citation_count} citations, {citation_density:.1f} per doctrine (min 1.0)",
    })

    # Gate 5: Eval pack (if spec provided)
    if spec_path and spec_path.exists():
        spec = json.loads(spec_path.read_text())
        engine_id = engine_dir.name.split("_")[0].upper()
        engine_spec = None
        for e in spec.get("engines", []):
            if e["engine_id"] == engine_id:
                engine_spec = e
                break

        if engine_spec and "eval_pack" in engine_spec:
            eval_pack = engine_spec["eval_pack"]
            pass_rate, eval_results = run_eval_pack(code, eval_pack)
            min_rate = eval_pack.get("min_pass_rate", 0.7)
            eval_ok = pass_rate >= min_rate
            results["gates"].append({
                "gate": "EVAL_PACK", "weight": 50, "passed": eval_ok,
                "detail": f"{pass_rate:.0%} pass rate (min {min_rate:.0%})",
                "queries": eval_results,
            })
        else:
            results["gates"].append({
                "gate": "EVAL_PACK", "weight": 50, "passed": True,
                "detail": "No eval pack in spec — skipped",
            })
    else:
        results["gates"].append({
            "gate": "EVAL_PACK", "weight": 50, "passed": True,
            "detail": "No spec provided — skipped",
        })

    # Calculate weighted score
    total_weight = sum(g["weight"] for g in results["gates"])
    weighted_score = sum(g["weight"] for g in results["gates"] if g["passed"])
    results["score"] = round(weighted_score / total_weight * 100) if total_weight else 0
    results["passed"] = all(g["passed"] for g in results["gates"] if g.get("weight", 0) >= 10)

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate engine quality")
    parser.add_argument("engine_dir", help="Path to engine directory")
    parser.add_argument("--spec", help="Path to tier spec JSON with eval packs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    spec_path = Path(args.spec) if args.spec else None
    result = validate(Path(args.engine_dir), spec_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"\n{'=' * 60}")
        print(f"  Engine: {result['engine_dir']}")
        print(f"  Status: {status}  Score: {result['score']}%")
        print(f"{'=' * 60}")
        for g in result["gates"]:
            icon = "+" if g["passed"] else "X"
            print(f"  [{icon}] {g['gate']:20s} (w={g['weight']:2d})  {g['detail']}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
