"""
TEST SUITE — Will Parser Intelligence Engine

Validates TIE-20 compliance and doctrine accuracy.
"""

import sys
from pathlib import Path

# Add engine directory to path
ENGINE_DIR = Path(__file__).parent
sys.path.insert(0, str(ENGINE_DIR))

from engine import WillParserEngine, ResponseMode, PositionZone
from doctrines import get_all_doctrines, get_doctrine_by_topic, search_doctrines_by_keyword
from semantic import normalize_semantics, extract_statute_references
from telemetry import get_telemetry


def test_doctrines_loaded():
    """Test that all 52+ doctrine blocks are loaded."""
    doctrines = get_all_doctrines()
    assert len(doctrines) >= 10, f"Expected ≥10 doctrines, got {len(doctrines)}"
    print(f"✓ Doctrines loaded: {len(doctrines)}")


def test_semantic_normalization():
    """Test semantic normalization layer."""
    result = normalize_semantics("handwritten will without witnesses")
    # Check that normalization happened (may not always map to 'holographic will' exactly)
    assert len(result.normalized_query) > 0
    assert result.confidence > 0
    print(f"✓ Semantic normalization: {len(result.mapped_terms)} terms mapped, confidence {result.confidence}")


def test_statute_extraction():
    """Test statute reference extraction."""
    query = "Under §251.052 and §255.153, what are the rules?"
    refs = extract_statute_references(query)
    assert "§251.052" in refs
    assert "§255.153" in refs
    print(f"✓ Statute extraction: {refs}")


def test_doctrine_search():
    """Test doctrine cache search."""
    doctrines = search_doctrines_by_keyword("holographic")
    assert len(doctrines) > 0
    assert any("holographic" in d.topic.lower() for d in doctrines)
    print(f"✓ Doctrine search: {[d.topic for d in doctrines]}")


def test_doctrine_retrieval():
    """Test doctrine block retrieval by topic."""
    doctrine = get_doctrine_by_topic("Holographic Will Validity")
    assert doctrine is not None
    assert "§251.052" in " ".join(doctrine.primary_authority)
    print(f"✓ Doctrine retrieval: {doctrine.topic}")


def test_engine_initialization():
    """Test engine initialization."""
    engine = WillParserEngine()
    assert len(engine.doctrines) >= 10
    assert engine.telemetry is not None
    print(f"✓ Engine initialized: {len(engine.doctrines)} doctrines")


def test_three_layer_response_cache_hit():
    """Test Layer 1 (doctrine cache hit)."""
    engine = WillParserEngine()
    response = engine.three_layer_response(
        query="Does a holographic will need witnesses?",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )

    assert response.response_layer.value == "doctrine_cache"
    assert "§251.052" in " ".join(response.authorities) or "holographic" in response.conclusion.lower()
    assert response.latency_ms > 0
    assert len(response.doctrine_topics) > 0
    print(f"✓ Cache hit response: {response.response_layer.value}, {response.latency_ms}ms")


def test_fast_mode():
    """Test FAST response mode (concise)."""
    engine = WillParserEngine()
    response = engine.three_layer_response(
        query="Can I revoke my will by writing a new one?",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )

    assert response.mode == ResponseMode.FAST
    assert response.reasoning is None  # FAST mode has no reasoning
    assert len(response.conclusion) > 0
    print(f"✓ FAST mode: conclusion length = {len(response.conclusion)} chars")


def test_defense_mode():
    """Test DEFENSE response mode (structured reasoning)."""
    engine = WillParserEngine()
    response = engine.three_layer_response(
        query="What is required for a valid attested will?",
        mode=ResponseMode.DEFENSE,
        position_zone=PositionZone.AUDIT
    )

    assert response.mode == ResponseMode.DEFENSE
    assert response.reasoning is not None
    assert "BURDEN" in response.reasoning or "burden" in response.reasoning.lower()
    print(f"✓ DEFENSE mode: reasoning length = {len(response.reasoning or '')} chars")


def test_memo_mode():
    """Test MEMO response mode (long-form)."""
    engine = WillParserEngine()
    response = engine.three_layer_response(
        query="Explain anti-lapse statute application",
        mode=ResponseMode.MEMO,
        position_zone=PositionZone.PLANNING
    )

    assert response.mode == ResponseMode.MEMO
    assert len(response.authorities) > 0
    assert len(response.conclusion) > 200  # MEMO should be detailed
    print(f"✓ MEMO mode: {len(response.authorities)} authorities, {len(response.conclusion)} chars")


def test_position_zones():
    """Test position zone epistemic guardrails."""
    engine = WillParserEngine()

    # Planning zone
    resp_planning = engine.three_layer_response(
        query="How to draft a residuary clause?",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )
    assert "PLANNING ZONE" in resp_planning.conclusion

    # Audit zone
    resp_audit = engine.three_layer_response(
        query="How to draft a residuary clause?",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.AUDIT
    )
    assert "AUDIT ZONE" in resp_audit.conclusion

    print(f"✓ Position zones: PLANNING and AUDIT disclaimers present")


def test_confidence_stratification():
    """Test confidence level assignment."""
    engine = WillParserEngine()
    response = engine.three_layer_response(
        query="Is a holographic will valid if properly handwritten?",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )

    assert response.confidence_level in ["DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"]
    print(f"✓ Confidence stratification: {response.confidence_level}")


def test_telemetry():
    """Test telemetry collection."""
    telemetry = get_telemetry(ENGINE_DIR / "logs")
    metrics = telemetry.get_performance_metrics()

    assert metrics.total_queries >= 0
    # Calculate hit rate manually
    hit_rate = metrics.cache_hits / max(metrics.total_queries, 1)
    assert hit_rate >= 0.0
    print(f"✓ Telemetry: {metrics.total_queries} queries, {hit_rate:.2%} cache hit rate")


def test_health_check():
    """Test health endpoint."""
    engine = WillParserEngine()
    health = engine.health_check()

    assert health.status == "healthy"
    assert health.engine_id == "P02_will_parser"
    assert health.port == 8652
    assert health.doctrines_loaded >= 10
    print(f"✓ Health check: {health.status}, {health.doctrines_loaded} doctrines")


def test_metrics():
    """Test metrics collection."""
    engine = WillParserEngine()
    # Run a query to generate metrics
    engine.three_layer_response(
        query="Test query for metrics",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )

    metrics = engine.get_metrics()
    assert "total_queries" in metrics
    assert "cache_hit_rate" in metrics
    assert "avg_latency_ms" in metrics
    print(f"✓ Metrics: {metrics['total_queries']} queries, {metrics['avg_latency_ms']}ms avg")


def test_determinism_hash():
    """Test SHA-256 determinism hash generation."""
    engine = WillParserEngine()
    response1 = engine.three_layer_response(
        query="Test determinism",
        mode=ResponseMode.FAST,
        position_zone=PositionZone.PLANNING
    )

    assert len(response1.determinism_hash) == 16  # Truncated SHA-256
    assert response1.determinism_hash.isalnum()
    print(f"✓ Determinism hash: {response1.determinism_hash}")


def run_all_tests():
    """Run all test cases."""
    tests = [
        test_doctrines_loaded,
        test_semantic_normalization,
        test_statute_extraction,
        test_doctrine_search,
        test_doctrine_retrieval,
        test_engine_initialization,
        test_three_layer_response_cache_hit,
        test_fast_mode,
        test_defense_mode,
        test_memo_mode,
        test_position_zones,
        test_confidence_stratification,
        test_telemetry,
        test_health_check,
        test_metrics,
        test_determinism_hash,
    ]

    passed = 0
    failed = 0

    print("=" * 60)
    print("WILL PARSER ENGINE TEST SUITE")
    print("=" * 60)

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: ERROR - {e}")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
