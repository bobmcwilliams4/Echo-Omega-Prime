"""
Simple TIE-20 Compliance Verification (AST-based, no imports)
"""
import ast
from pathlib import Path

def check_tie20_compliance():
    """Parse engine.py and check for TIE-20 component presence."""

    engine_path = Path(__file__).parent / "engine.py"
    with open(engine_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    # Extract all class and function names
    classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    components = {
        "1. three_layer_response": "three_layer_response" in functions,
        "2. response_modes (FAST/DEFENSE/MEMO)": "ResponseMode" in classes,
        "3. doctrine_cache": "TitleDoctrineCache" in source,
        "4. authority_hardening": "authority" in source.lower(),
        "5. confidence_stratification": "ConfidenceZone" in classes,
        "6. semantic_normalization": "TitleSemanticDictionary" in source,
        "7. vector_search": "cloud_retriever" in source,
        "8. telemetry": "TitleExamTelemetry" in source,
        "9. drift_watcher": "DoctrineDriftWatcher" in classes,
        "10. coverage_map": "DoctrineCoverageMap" in classes,
        "11. metrics_collector": "TitleMetricsCollector" in classes,
        "12. health_endpoint": "health_check" in functions,
        "13. zoned_analysis (PLANNING/REPORTING/AUDIT)": "AnalysisZone" in classes,
        "14. fact_fragility_scoring": "FactFragilityScorer" in classes,
        "15. audit_trail_jsonl": "audit" in source.lower(),
        "16. determinism_hash_sha256": "sha256" in source.lower(),
        "17. fastapi_server": "FastAPI" in source,
        "18. loguru_logging": "logger" in source,
        "19. multi_doctrine_decomposition": "MultiDoctrineDecomposer" in classes,
        "20. deep_analysis_mode": "_deep_analysis_mode" in functions,
    }

    print("=" * 70)
    print("TIE-20 COMPLIANCE CHECK: LM01 Title Examination Engine")
    print("=" * 70)
    print()

    passed = 0
    for component, present in components.items():
        status = "✓" if present else "✗"
        print(f"{status} {component}")
        if present:
            passed += 1

    total = len(components)
    print()
    print("=" * 70)
    print(f"RESULT: {passed}/{total} components present ({passed/total*100:.0f}%)")

    if passed == total:
        print("STATUS: ✓ FULLY TIE-20 COMPLIANT")
    else:
        print(f"STATUS: ✗ PARTIAL COMPLIANCE")

    print("=" * 70)
    print()

    # Line count
    lines = source.count('\n')
    print(f"Total lines: {lines:,}")
    print(f"Target: 2,000+ lines")
    print(f"Status: {'✓ PASS' if lines >= 2000 else '✗ BELOW TARGET'}")
    print()

    return passed, total


if __name__ == "__main__":
    passed, total = check_tie20_compliance()
    exit(0 if passed == total else 1)
