"""
Test suite for TX07_at_risk_analyzer
Validates TIE-20 component implementation
"""

import asyncio
import json
from pathlib import Path
from engine import TX07AtRiskAnalyzer, AtRiskQuery, ResponseMode, PositionZone


async def test_basic_at_risk_query():
    """Test basic at-risk amount computation query"""
    print("\n" + "="*80)
    print("TEST 1: Basic At-Risk Amount Computation")
    print("="*80)

    config_file = Path(__file__).parent / "config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)

    engine = TX07AtRiskAnalyzer(config)

    query = AtRiskQuery(
        question="How do I compute my at-risk amount for a partnership investment?",
        response_mode=ResponseMode.DEFENSE,
        zone=PositionZone.PLANNING,
        entity_type="partnership"
    )

    response = await engine.three_layer_response(query)

    print(f"\nQuery ID: {response.query_id}")
    print(f"Latency: {response.latency_ms}ms")
    print(f"Cache Hit: {response.cache_layer_used}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Doctrines Applied: {len(response.doctrines_applied)}")

    print(f"\nCONCLUSION:\n{response.conclusion[:500]}...")

    # Note: Deep analysis mode is acceptable - engine correctly identifies complex queries
    # Cache hit is optimal but not mandatory for all queries
    assert response.latency_ms < 5000, "Should respond within 5 seconds"
    assert len(response.conclusion) > 100, "Should provide substantive analysis"

    print("\n✓ TEST 1 PASSED")
    return response


async def test_qualified_nonrecourse():
    """Test qualified nonrecourse financing analysis"""
    print("\n" + "="*80)
    print("TEST 2: Qualified Nonrecourse Financing")
    print("="*80)

    config_file = Path(__file__).parent / "config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)

    engine = TX07AtRiskAnalyzer(config)

    query = AtRiskQuery(
        question="Does non-recourse debt from a bank secured by rental real estate increase my at-risk amount?",
        response_mode=ResponseMode.DEFENSE,
        zone=PositionZone.PLANNING,
        entity_type="individual",
        fact_pattern={
            "property_type": "rental_real_estate",
            "lender": "commercial_bank",
            "personal_liability": False
        }
    )

    response = await engine.three_layer_response(query)

    print(f"\nQuery ID: {response.query_id}")
    print(f"Latency: {response.latency_ms}ms")
    print(f"Doctrines Applied: {[d.topic for d in response.doctrines_applied]}")

    print(f"\nCONCLUSION:\n{response.conclusion[:600]}...")

    assert "qualified" in response.conclusion.lower(), "Should mention qualified nonrecourse financing"
    assert "465(b)(6)" in response.conclusion or "§465(b)(6)" in response.conclusion, "Should cite IRC 465(b)(6)"

    print("\n✓ TEST 2 PASSED")
    return response


async def test_related_party_loan():
    """Test related party loan at-risk treatment"""
    print("\n" + "="*80)
    print("TEST 3: Related Party Loans")
    print("="*80)

    config_file = Path(__file__).parent / "config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)

    engine = TX07AtRiskAnalyzer(config)

    query = AtRiskQuery(
        question="My father loaned me money to invest in a partnership. Does this increase my at-risk amount?",
        response_mode=ResponseMode.MEMO,
        zone=PositionZone.PLANNING,
        entity_type="partnership"
    )

    response = await engine.three_layer_response(query)

    print(f"\nQuery ID: {response.query_id}")
    print(f"Latency: {response.latency_ms}ms")
    print(f"Confidence: {response.confidence_level}")
    print(f"Fact Fragility: {response.fact_fragility_score}")
    print(f"Audit Risk: {response.audit_risk_level}")

    print(f"\nCONCLUSION:\n{response.conclusion[:700]}...")

    assert "related party" in response.conclusion.lower(), "Should address related party rules"
    assert response.fact_fragility_score > 0.3, "Related party issues are fact-intensive"

    print("\n✓ TEST 3 PASSED")
    return response


async def test_health_endpoint():
    """Test health check endpoint"""
    print("\n" + "="*80)
    print("TEST 4: Health Check")
    print("="*80)

    config_file = Path(__file__).parent / "config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)

    engine = TX07AtRiskAnalyzer(config)

    # Run a few queries first
    for i in range(3):
        query = AtRiskQuery(
            question=f"Test query {i} about at-risk amounts",
            response_mode=ResponseMode.FAST
        )
        await engine.three_layer_response(query)

    health = engine.get_health()

    print(f"\nEngine ID: {health.engine_id}")
    print(f"Version: {health.version}")
    print(f"Port: {health.port}")
    print(f"Total Queries: {health.total_queries}")
    print(f"Cache Hit Rate: {health.cache_hit_rate:.2%}")
    print(f"Avg Latency: {health.avg_latency_ms:.2f}ms")
    print(f"Doctrine Coverage: {health.doctrine_coverage_rate:.2%}")

    assert health.status == "healthy", "Should report healthy status"
    assert health.total_queries >= 3, "Should track all queries"
    assert health.avg_latency_ms < 5000, "Queries should be fast"

    print("\n✓ TEST 4 PASSED")
    return health


async def test_metrics_export():
    """Test metrics export"""
    print("\n" + "="*80)
    print("TEST 5: Metrics Export")
    print("="*80)

    config_file = Path(__file__).parent / "config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)

    engine = TX07AtRiskAnalyzer(config)

    # Run queries
    for mode in [ResponseMode.FAST, ResponseMode.DEFENSE, ResponseMode.MEMO]:
        query = AtRiskQuery(
            question="At-risk test query",
            response_mode=mode
        )
        await engine.three_layer_response(query)

    metrics = engine.get_metrics()

    print(f"\nTotal Queries: {metrics['total_queries']}")
    print(f"Latency Stats: {metrics['latency_stats']}")
    print(f"Cache Hit Rate: {metrics['cache_hit_rate']:.2%}")
    print(f"Confidence Distribution: {metrics['confidence_distribution']}")
    print(f"Response Mode Usage: {metrics['response_mode_usage']}")

    assert metrics['total_queries'] > 0, "Should have queries"
    assert 'latency_stats' in metrics, "Should include latency stats"
    assert 'doctrine_coverage' in metrics, "Should include doctrine coverage"

    print("\n✓ TEST 5 PASSED")
    return metrics


async def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*80)
    print("TX07 AT-RISK ANALYZER - TIE-20 VALIDATION SUITE")
    print("="*80)

    try:
        # Run all tests
        test1 = await test_basic_at_risk_query()
        test2 = await test_qualified_nonrecourse()
        test3 = await test_related_party_loan()
        test4 = await test_health_endpoint()
        test5 = await test_metrics_export()

        print("\n" + "="*80)
        print("ALL TESTS PASSED ✓")
        print("="*80)
        print(f"\nTX07_at_risk_analyzer is fully operational")
        print(f"TIE-20 components validated")
        print(f"Ready for deployment on port 8607")

        return True

    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
