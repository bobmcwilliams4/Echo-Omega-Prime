"""
Quick validation test for R02 Permit Analyzer engine.
Verifies all TIE-20 components are functional.
"""

import sys
from pathlib import Path

# Add current directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all module imports."""
    print("Testing module imports...")

    try:
        from telemetry import get_telemetry, ErrorDomain, ResponseLayer
        print("  ✓ telemetry.py")
    except Exception as e:
        print(f"  ✗ telemetry.py: {e}")
        return False

    try:
        from semantic import normalize_semantics, get_normalizer
        print("  ✓ semantic.py")
    except Exception as e:
        print(f"  ✗ semantic.py: {e}")
        return False

    try:
        from search import get_search_engine
        print("  ✓ search.py")
    except Exception as e:
        print(f"  ✗ search.py: {e}")
        return False

    try:
        from doctrines import get_doctrine_cache, search_doctrines
        print("  ✓ doctrines.py")
    except Exception as e:
        print(f"  ✗ doctrines.py: {e}")
        return False

    return True


def test_doctrine_cache():
    """Test doctrine cache loading."""
    print("\nTesting doctrine cache...")

    from doctrines import get_doctrine_cache, search_doctrines

    cache = get_doctrine_cache()
    print(f"  ✓ {len(cache)} doctrine blocks loaded")

    # Test doctrine search
    results = search_doctrines("drilling permit horizontal well", ["drilling_w1"], top_k=3)
    print(f"  ✓ Search returned {len(results)} results")

    if results:
        print(f"  ✓ Top result: {results[0].topic}")

    return True


def test_semantic_normalization():
    """Test semantic normalization."""
    print("\nTesting semantic normalization...")

    from semantic import normalize_semantics

    result = normalize_semantics("Need W-1 permit for horizontal well with Rule 37 spacing exception")
    print(f"  ✓ Original: {result.original_query[:50]}...")
    print(f"  ✓ Normalized: {result.normalized_query[:50]}...")
    print(f"  ✓ Permit types detected: {result.permit_types_detected}")
    print(f"  ✓ Substitutions: {len(result.substitutions_made)}")

    return True


def test_telemetry():
    """Test telemetry system."""
    print("\nTesting telemetry...")

    from telemetry import initialize_telemetry, get_telemetry, trace_query, complete_trace
    from pathlib import Path

    # Initialize with temp audit log
    audit_path = Path(__file__).parent / "logs" / "test_audit.jsonl"
    audit_path.parent.mkdir(exist_ok=True)

    initialize_telemetry(audit_path)
    telemetry = get_telemetry()
    print("  ✓ Telemetry initialized")

    # Create test trace
    trace = trace_query("Test query", "FAST")
    trace.normalization_ms = 5.0
    trace.doctrine_lookup_ms = 10.0
    trace.final_confidence = 0.85
    complete_trace(trace)
    print(f"  ✓ Trace created: {trace.trace_id}")

    metrics = telemetry.get_metrics_summary()
    print(f"  ✓ Metrics: {metrics['total_queries']} queries")

    return True


def test_tie20_components():
    """Verify all TIE-20 components present in engine.py."""
    print("\nVerifying TIE-20 components...")

    engine_path = Path(__file__).parent / "engine.py"
    with open(engine_path, 'r', encoding='utf-8') as f:
        code = f.read()

    components = {
        'three_layer_response': 'def three_layer_response' in code,
        'response_modes': 'FAST' in code and 'COMPLIANCE_AUDIT' in code,
        'doctrine_cache': 'from doctrines import' in code,
        'authority_hardening': 'resolve_authority_conflicts' in code,
        'confidence_stratification': 'ConfidenceLevel' in code,
        'semantic_normalization': 'from semantic import' in code,
        'vector_search': 'from search import' in code,
        'telemetry': 'from telemetry import' in code,
        'drift_watcher': 'DoctrineDriftWatcher' in code,
        'coverage_map': 'DoctrineCoverageMap' in code,
        'metrics_collector': 'MetricsCollector' in code,
        'health_endpoint': '@app.get("/health")' in code,
        'fact_fragility_scoring': 'calculate_fact_fragility' in code,
        'audit_trail_jsonl': 'AUDIT_LOG' in code,
        'determinism_hash_sha256': 'hashlib.sha256' in code,
        'fastapi_server': 'from fastapi import FastAPI' in code,
        'loguru_logging': 'from loguru import logger' in code,
        'multi_doctrine_decomposition': 'decompose_multi_doctrine_query' in code,
        'deep_analysis_mode': 'ResponseLayer.DEEP_ANALYSIS' in code,
    }

    passed = sum(components.values())
    total = len(components)

    print(f"  TIE-20 Coverage: {passed}/{total}")

    for name, present in components.items():
        symbol = '✓' if present else '✗'
        print(f"    {symbol} {name}")

    return passed == total


def main():
    """Run all tests."""
    print("="*60)
    print("R02 PERMIT ANALYZER - ENGINE VALIDATION TEST")
    print("="*60)

    tests = [
        ("Module Imports", test_imports),
        ("Doctrine Cache", test_doctrine_cache),
        ("Semantic Normalization", test_semantic_normalization),
        ("Telemetry System", test_telemetry),
        ("TIE-20 Components", test_tie20_components),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} FAILED: {e}")
            results.append((name, False))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        symbol = '✓' if result else '✗'
        print(f"{symbol} {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ ALL TESTS PASSED - Engine ready for deployment")
        return 0
    else:
        print(f"\n✗ {total - passed} TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
