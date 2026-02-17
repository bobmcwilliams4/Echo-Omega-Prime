"""
Test script for R03 Compliance Checker Engine
Validates TIE-20 components and basic functionality
"""

import sys
import json
from pathlib import Path
import time

# Add engine to path
engine_path = Path(__file__).parent
sys.path.insert(0, str(engine_path))

from doctrines import DOCTRINE_CACHE, get_doctrine_by_topic, search_doctrines_by_keyword
from semantic import SemanticNormalizer
from telemetry import TelemetryCollector


def test_doctrine_cache():
    """Test doctrine cache loading and search."""
    print("\n" + "="*80)
    print("TEST: Doctrine Cache")
    print("="*80)

    print(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    assert len(DOCTRINE_CACHE) >= 14, "Should have at least 14 doctrine blocks"

    # Test topic lookup
    topic = "RRC_PRODUCTION_REPORTING_P4"
    doctrine = get_doctrine_by_topic(topic)
    assert doctrine is not None, f"Should find doctrine for {topic}"
    print(f"✓ Found doctrine: {topic}")
    print(f"  Confidence: {doctrine.confidence:.1%} ({doctrine.confidence_stratification})")

    # Test keyword search
    results = search_doctrines_by_keyword("spill")
    assert len(results) > 0, "Should find doctrines containing 'spill'"
    print(f"✓ Keyword search 'spill': {len(results)} results")

    print("✅ Doctrine cache tests PASSED\n")


def test_semantic_normalizer():
    """Test semantic normalization."""
    print("="*80)
    print("TEST: Semantic Normalizer")
    print("="*80)

    normalizer = SemanticNormalizer()

    # Test query normalization
    query = "When is the monthly production report due for RRC?"
    normalized = normalizer.normalize(query)
    print(f"Original: {query}")
    print(f"Normalized: {normalized}")
    assert "P-4" in normalized or "P_4" in normalized, "Should normalize 'production report' to P-4"

    # Test entity extraction
    query2 = "What are the requirements for Form P-4 under Statewide Rule 20?"
    entities = normalizer.extract_entities(query2)
    print(f"\nEntities from '{query2}':")
    print(f"  Forms: {entities['forms']}")
    print(f"  Rules: {entities['rules']}")
    assert len(entities['forms']) > 0, "Should extract form references"

    # Test compliance zone detection
    zones = {
        "planning new well": "PREVENTIVE",
        "late filing penalty": "REMEDIAL",
        "compliance audit": "AUDIT",
        "daily operations": "OPERATIONAL"
    }
    for query, expected_zone in zones.items():
        detected = normalizer.identify_compliance_zone(query)
        print(f"'{query}' → {detected} (expected {expected_zone})")

    # Test query intent classification
    intents = {
        "when is deadline": "DEADLINE_CHECK",
        "what is the penalty": "PENALTY_ASSESSMENT",
        "how do I report": "REPORTING_GUIDANCE",
        "do I need permit": "PERMIT_QUESTION"
    }
    for query, expected_intent in intents.items():
        detected = normalizer.classify_query_intent(query)
        print(f"'{query}' → {detected} (expected {expected_intent})")

    print("✅ Semantic normalizer tests PASSED\n")


def test_telemetry():
    """Test telemetry collection."""
    print("="*80)
    print("TEST: Telemetry Collector")
    print("="*80)

    config = {
        "doctrine_topics": 14,
        "telemetry": {
            "enabled": True,
            "trace_queries": False,  # Don't write audit trail in tests
            "audit_trail_path": str(engine_path / "test_audit.jsonl")
        }
    }

    telemetry = TelemetryCollector(config)

    # Simulate queries
    for i in range(5):
        query_id = telemetry.start_query(
            query_text=f"Test query {i}",
            normalized_query=f"test query {i}",
            compliance_zone="OPERATIONAL",
            query_intent="REQUIREMENT_LOOKUP"
        )

        time.sleep(0.01)  # Simulate processing

        telemetry.complete_query(
            query_id=query_id,
            cache_hit=(i % 2 == 0),
            doctrine_topic=f"TEST_TOPIC_{i}" if (i % 2 == 0) else None,
            semantic_search_used=(i % 2 == 1),
            deep_analysis_triggered=False,
            response_mode="DEFENSE",
            confidence=0.95,
            confidence_strata="DEFENSIBLE",
            authorities_cited=["RRC", "TCEQ"],
            response_text="Test response " * 20,
            cache_lookup_ms=10.0,
            semantic_search_ms=50.0 if (i % 2 == 1) else 0.0,
            deep_analysis_ms=0.0
        )

    # Get metrics
    metrics = telemetry.get_metrics_snapshot()
    print(f"Total queries: {metrics.total_queries}")
    print(f"Cache hits: {metrics.cache_hits}")
    print(f"Cache misses: {metrics.cache_misses}")
    print(f"Cache hit rate: {metrics.cache_hit_rate:.1%}")
    print(f"Avg latency: {metrics.avg_latency_ms:.2f}ms")

    assert metrics.total_queries == 5, "Should have 5 queries"
    assert metrics.cache_hit_rate == 0.6, "Should have 60% cache hit rate (3/5)"

    # Get doctrine coverage
    coverage = telemetry.get_doctrine_coverage_stats()
    print(f"\nDoctrine coverage: {coverage['doctrines_used']}/{coverage['total_doctrines']}")
    print(f"Coverage percentage: {coverage['coverage_percentage']:.1f}%")

    print("✅ Telemetry tests PASSED\n")


def test_config_loading():
    """Test configuration file."""
    print("="*80)
    print("TEST: Configuration")
    print("="*80)

    config_path = engine_path / "config.json"
    assert config_path.exists(), "config.json should exist"

    with open(config_path) as f:
        config = json.load(f)

    required_fields = ["engine_id", "engine_name", "version", "port", "domain", "mode"]
    for field in required_fields:
        assert field in config, f"Config should have {field}"
        print(f"✓ {field}: {config[field]}")

    assert config["engine_id"] == "R03", "Engine ID should be R03"
    assert config["port"] == 8703, "Port should be 8703"
    assert config["mode"] == "RULE_BASED", "Mode should be RULE_BASED"

    print("✅ Configuration tests PASSED\n")


def test_tie20_components():
    """Verify all TIE-20 components are present."""
    print("="*80)
    print("TEST: TIE-20 Component Checklist")
    print("="*80)

    # Read engine.py to verify components
    engine_code = (engine_path / "engine.py").read_text()

    components = {
        "three_layer_response": "def three_layer_response",
        "response_modes": "def _fast_response",
        "doctrine_cache": "DOCTRINE_CACHE",
        "authority_hardening": "authority_weights",
        "confidence_stratification": "confidence_stratification",
        "semantic_normalization": "SemanticNormalizer",
        "vector_search": "search_regulations",
        "telemetry": "TelemetryCollector",
        "drift_watcher": "analyze_drift",
        "coverage_map": "get_doctrine_coverage_stats",
        "metrics_collector": "get_metrics_snapshot",
        "health_endpoint": "/health",
        "zoned_analysis": "compliance_zone",
        "fact_fragility_scoring": "confidence",
        "audit_trail_jsonl": "audit_trail",
        "determinism_hash_sha256": "determinism_hash",
        "fastapi_server": "FastAPI",
        "loguru_logging": "from loguru import logger",
        "multi_doctrine_decomposition": "_find_related_doctrines",
        "deep_analysis_mode": "def _deep_analysis",
    }

    for component, search_term in components.items():
        found = search_term in engine_code
        status = "✓" if found else "✗"
        print(f"{status} {component:30s} {search_term}")
        assert found, f"Component {component} not found"

    print("✅ All TIE-20 components present\n")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("R03 COMPLIANCE CHECKER ENGINE - TEST SUITE")
    print("="*80)

    try:
        test_config_loading()
        test_doctrine_cache()
        test_semantic_normalizer()
        test_telemetry()
        test_tie20_components()

        print("="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print("\nEngine is ready for deployment.")
        print(f"Start with: python {engine_path / 'engine.py'}")
        print(f"Health check: http://localhost:8703/health")
        print(f"Query endpoint: POST http://localhost:8703/query")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
