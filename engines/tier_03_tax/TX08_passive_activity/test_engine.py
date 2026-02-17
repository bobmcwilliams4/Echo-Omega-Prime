"""
TX08 Passive Activity Loss Engine - Test Suite
"""

import asyncio
import sys
from pathlib import Path

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent))

from engine import PassiveActivityEngine, ResponseMode, AnalysisZone, QueryRequest
from loguru import logger


async def test_material_participation_500_hours():
    """Test material participation test 1 (500 hours)."""
    print("\n" + "="*80)
    print("TEST 1: Material Participation Test 1 (500 Hours)")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="How many hours do I need to work to materially participate in my S corporation?",
        mode=ResponseMode.FAST,
        zone=AnalysisZone.PLANNING
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nDoctrines Triggered: {len(response.doctrines_triggered)}")
    for doctrine in response.doctrines_triggered[:3]:
        print(f"  - {doctrine.topic}")

    assert response.confidence_level in ["DEFENSIBLE", "AGGRESSIVE"]
    assert response.latency_ms < 500
    assert len(response.doctrines_triggered) > 0

    print("\n✅ TEST 1 PASSED")


async def test_real_estate_professional():
    """Test real estate professional exception."""
    print("\n" + "="*80)
    print("TEST 2: Real Estate Professional Exception")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="What are the requirements to qualify as a real estate professional under IRC 469(c)(7)?",
        mode=ResponseMode.DEFENSE,
        zone=AnalysisZone.REPORTING
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nSubstantiation Requirements:")
    for req in response.substantiation_requirements[:3]:
        print(f"  - {req}")

    assert "750" in response.conclusion or "750" in response.reasoning
    assert len(response.substantiation_requirements) > 0

    print("\n✅ TEST 2 PASSED")


async def test_25k_allowance():
    """Test $25,000 rental loss allowance."""
    print("\n" + "="*80)
    print("TEST 3: $25,000 Rental Loss Allowance")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="Can I deduct rental losses against my W-2 income if my AGI is $120,000?",
        mode=ResponseMode.MEMO,
        zone=AnalysisZone.PLANNING
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nPlanning Opportunities:")
    for opp in response.planning_opportunities[:3]:
        print(f"  - {opp}")

    assert response.latency_ms < 2000  # MEMO mode should be <2s
    assert len(response.planning_opportunities) > 0

    print("\n✅ TEST 3 PASSED")


async def test_grouping_of_activities():
    """Test grouping of activities."""
    print("\n" + "="*80)
    print("TEST 4: Grouping of Activities")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="Can I group my three rental properties into one activity for material participation purposes?",
        mode=ResponseMode.FAST,
        zone=AnalysisZone.PLANNING
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nPrimary Authority:")
    for auth in response.primary_authority[:3]:
        print(f"  - {auth}")

    assert len(response.primary_authority) > 0
    assert response.latency_ms < 500

    print("\n✅ TEST 4 PASSED")


async def test_disposition_suspended_losses():
    """Test disposition of entire interest and suspended losses."""
    print("\n" + "="*80)
    print("TEST 5: Disposition of Entire Interest - Suspended Losses")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="If I sell my rental property with $50,000 of suspended passive losses, can I deduct them?",
        mode=ResponseMode.DEFENSE,
        zone=AnalysisZone.AUDIT
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nReasoning (first 300 chars):\n{response.reasoning[:300]}...")

    assert "469(g)" in str(response.primary_authority) or "disposition" in response.conclusion.lower()

    print("\n✅ TEST 5 PASSED")


async def test_self_rental():
    """Test self-rental recharacterization."""
    print("\n" + "="*80)
    print("TEST 6: Self-Rental Recharacterization")
    print("="*80)

    engine = PassiveActivityEngine()

    response = await engine.three_layer_response(
        query="I own a building and lease it to my S corporation where I materially participate. Is the rental income passive?",
        mode=ResponseMode.FAST,
        zone=AnalysisZone.REPORTING
    )

    print(f"\nQuery ID: {response.query_id}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Latency: {response.latency_ms:.1f}ms")
    print(f"\nConclusion:\n{response.conclusion}")
    print(f"\nFact Fragility Score: {response.fact_fragility_score:.2f}")

    assert response.fact_fragility_score >= 0.0 and response.fact_fragility_score <= 1.0

    print("\n✅ TEST 6 PASSED")


async def test_health_endpoint():
    """Test health endpoint."""
    print("\n" + "="*80)
    print("TEST 7: Health Endpoint")
    print("="*80)

    engine = PassiveActivityEngine()

    # Run a few queries first
    await engine.three_layer_response("test query 1", ResponseMode.FAST, AnalysisZone.PLANNING)
    await engine.three_layer_response("test query 2", ResponseMode.FAST, AnalysisZone.PLANNING)

    health = engine.health_check()

    print(f"\nStatus: {health.status}")
    print(f"Version: {health.version}")
    print(f"Port: {health.port}")
    print(f"Doctrine Count: {health.doctrine_count}")
    print(f"Total Queries: {health.total_queries}")
    print(f"Avg Latency: {health.avg_latency_ms:.1f}ms")
    print(f"Coverage: {health.coverage_percentage:.1f}%")
    print(f"Uptime: {health.uptime_seconds:.1f}s")

    assert health.status == "healthy"
    assert health.doctrine_count >= 15
    assert health.total_queries >= 2

    print("\n✅ TEST 7 PASSED")


async def test_metrics():
    """Test metrics collection."""
    print("\n" + "="*80)
    print("TEST 8: Metrics Collection")
    print("="*80)

    engine = PassiveActivityEngine()

    # Run queries
    await engine.three_layer_response("test query", ResponseMode.FAST, AnalysisZone.PLANNING)
    await engine.three_layer_response("test query", ResponseMode.DEFENSE, AnalysisZone.REPORTING)

    metrics = engine.get_metrics()

    print(f"\nTotal Queries: {metrics['total_queries']}")
    print(f"Avg Latency: {metrics['avg_latency_ms']:.1f}ms")
    print(f"Vector Search Rate: {metrics['vector_search_rate']*100:.1f}%")
    print(f"Error Rate: {metrics['error_rate']*100:.2f}%")
    print(f"\nQueries by Mode: {metrics['queries_by_mode']}")

    if metrics.get('latency_percentiles'):
        print(f"\nLatency Percentiles:")
        print(f"  P50: {metrics['latency_percentiles']['p50']:.1f}ms")
        print(f"  P90: {metrics['latency_percentiles']['p90']:.1f}ms")
        print(f"  P95: {metrics['latency_percentiles']['p95']:.1f}ms")

    assert metrics['total_queries'] >= 2
    assert metrics['error_rate'] == 0.0

    print("\n✅ TEST 8 PASSED")


async def test_coverage_map():
    """Test doctrine coverage map."""
    print("\n" + "="*80)
    print("TEST 9: Coverage Map")
    print("="*80)

    engine = PassiveActivityEngine()

    # Run diverse queries to trigger multiple doctrines
    queries = [
        "500 hours material participation",
        "real estate professional 750 hours",
        "$25,000 rental loss allowance",
        "grouping of activities",
        "disposition entire interest suspended losses"
    ]

    for query in queries:
        await engine.three_layer_response(query, ResponseMode.FAST, AnalysisZone.PLANNING)

    coverage = engine.get_coverage_map()

    print(f"\nTotal Doctrines: {coverage.total_doctrines}")
    print(f"Triggered: {len(coverage.triggered_doctrines)}")
    print(f"Never Triggered: {len(coverage.never_triggered)}")
    print(f"Coverage: {coverage.coverage_percentage:.1f}%")
    print(f"\nTop Doctrines:")
    for topic, count in coverage.top_doctrines[:5]:
        print(f"  {topic}: {count} hits")

    assert coverage.total_doctrines >= 15
    assert len(coverage.triggered_doctrines) > 0

    print("\n✅ TEST 9 PASSED")


async def test_semantic_normalization():
    """Test semantic normalization."""
    print("\n" + "="*80)
    print("TEST 10: Semantic Normalization")
    print("="*80)

    engine = PassiveActivityEngine()

    # Test various phrasings of same question
    queries = [
        "How do I materially participate?",
        "What is the material participation test?",
        "500 hour rule for passive activities",
        "IRC 469 material participation standard"
    ]

    hashes = []
    for query in queries:
        normalized = engine.semantic_normalizer.normalize(query)
        keywords = engine.semantic_normalizer.extract_keywords(query)
        print(f"\nOriginal: {query}")
        print(f"Normalized: {normalized}")
        print(f"Keywords: {keywords[:5]}")

        # All should trigger material participation doctrines
        response = await engine.three_layer_response(query, ResponseMode.FAST, AnalysisZone.PLANNING)
        hashes.append(response.determinism_hash)

    # Different phrasings may have different hashes (different doctrine matches)
    # but should all return material participation results
    print(f"\nDeterminism Hashes: {hashes}")

    print("\n✅ TEST 10 PASSED")


async def run_all_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("TX08 PASSIVE ACTIVITY LOSS ENGINE - TEST SUITE")
    print("="*80)

    tests = [
        test_material_participation_500_hours,
        test_real_estate_professional,
        test_25k_allowance,
        test_grouping_of_activities,
        test_disposition_suspended_losses,
        test_self_rental,
        test_health_endpoint,
        test_metrics,
        test_coverage_map,
        test_semantic_normalization
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test.__name__}")
            print(f"Error: {e}")
            failed += 1

    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n✅ ALL TESTS PASSED")
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
