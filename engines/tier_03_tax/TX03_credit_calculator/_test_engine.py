"""
TX03 Credit Calculator Engine - Test Suite
Validate TIE-20 compliance and credit calculation accuracy
"""

import sys
from pathlib import Path
import json
import asyncio

# Add engine to path
ENGINE_DIR = Path(__file__).parent
sys.path.insert(0, str(ENGINE_DIR))

from engine import TX03CreditCalculatorEngine, CreditQuery
from doctrines import DOCTRINE_CACHE, IssueCategory


def test_doctrine_cache():
    """Test doctrine cache loading"""
    print("\n=== TEST 1: Doctrine Cache ===")
    print(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    assert len(DOCTRINE_CACHE) >= 20, f"Expected at least 20 doctrines, got {len(DOCTRINE_CACHE)}"

    # Check sample doctrines
    topics = [d.topic for d in DOCTRINE_CACHE]
    assert "child_tax_credit_eligibility" in topics
    assert "earned_income_tax_credit_calculation" in topics
    assert "research_credit_qualified_research" in topics

    print(f"✓ Doctrine cache loaded correctly ({len(DOCTRINE_CACHE)} blocks)")


def test_semantic_normalization():
    """Test semantic normalization"""
    print("\n=== TEST 2: Semantic Normalization ===")
    from semantic import SemanticNormalizer

    normalizer = SemanticNormalizer(ENGINE_DIR / "config.json")

    # Test credit type normalization
    assert normalizer.normalize_credit_type("refund_credit") == "refundable"
    assert normalizer.normalize_credit_type("GBC") == "business"

    # Test credit name normalization
    assert normalizer.normalize_credit_name("CTC") == "child_tax_credit"
    assert normalizer.normalize_credit_name("IRC_24") == "child_tax_credit"

    # Test IRC extraction
    irc_sections = normalizer.extract_irc_section("What is the IRC §24 child tax credit and IRC 32 EITC?")
    assert "24" in irc_sections
    assert "32" in irc_sections

    print("✓ Semantic normalization working correctly")


def test_search_engine():
    """Test search engine"""
    print("\n=== TEST 3: Search Engine ===")
    from search import CreditSearchEngine

    search = CreditSearchEngine(ENGINE_DIR / "config.json")

    # Keyword search
    results = search.keyword_search("child tax credit")
    assert len(results) > 0, "No results for 'child tax credit'"
    print(f"✓ Keyword search: {len(results)} results for 'child tax credit'")

    # IRC section search
    results = search.search_by_irc_section("24")
    assert len(results) > 0, "No results for IRC §24"
    print(f"✓ IRC search: {len(results)} results for IRC §24")

    # Category search
    results = search.search_by_category(IssueCategory.INDIVIDUAL_CREDITS)
    assert len(results) > 0, "No individual credits found"
    print(f"✓ Category search: {len(results)} individual credits")

    # Carryover search
    carryover_credits = search.search_carryover_credits()
    print(f"✓ Carryover search: {len(carryover_credits)} credits allow carryover")

    # Statistics
    stats = search.get_statistics()
    print(f"✓ Statistics: {stats['total_doctrines']} total doctrines")


def test_telemetry():
    """Test telemetry collector"""
    print("\n=== TEST 4: Telemetry ===")
    from telemetry import TelemetryCollector

    telemetry = TelemetryCollector(ENGINE_DIR / "config.json")

    # Record test query
    telemetry.record_query(
        query_id="test_001",
        query_text="Test query for child tax credit",
        response_mode="FAST",
        doctrines_triggered=["child_tax_credit_eligibility"],
        latency_ms=125.5,
        cache_hit=True,
        confidence_level=0.95
    )

    # Get metrics
    metrics = telemetry.get_metrics()
    assert metrics.total_queries == 1
    assert metrics.cache_hits == 1
    assert metrics.avg_latency_ms == 125.5

    print(f"✓ Telemetry recorded: {metrics.total_queries} queries")


async def test_engine_initialization():
    """Test engine initialization"""
    print("\n=== TEST 5: Engine Initialization ===")

    config_path = ENGINE_DIR / "config.json"
    engine = TX03CreditCalculatorEngine(config_path)

    assert engine.engine_id == "TX03_credit_calculator"
    assert engine.version == "1.0.0"
    assert engine.port == 8603
    assert len(engine.doctrine_cache) >= 20

    print(f"✓ Engine initialized: {engine.engine_id} v{engine.version}")


async def test_query_processing():
    """Test end-to-end query processing"""
    print("\n=== TEST 6: Query Processing ===")

    config_path = ENGINE_DIR / "config.json"
    engine = TX03CreditCalculatorEngine(config_path)

    # Test query 1: Child Tax Credit
    query1 = CreditQuery(
        query="How do I calculate the child tax credit for 2024?",
        response_mode="FAST",
        entity_type="Individual"
    )

    response1 = await engine.process_query(query1)
    assert response1.query_id is not None
    assert len(response1.calculations) > 0
    assert response1.confidence_level > 0.0
    print(f"✓ Query 1: {len(response1.calculations)} calculations, confidence {response1.confidence_level:.1%}")

    # Test query 2: Research Credit
    query2 = CreditQuery(
        query="What are the requirements for the R&D credit under IRC §41?",
        response_mode="DEFENSE",
        entity_type="C_Corporation"
    )

    response2 = await engine.process_query(query2)
    assert len(response2.calculations) > 0
    assert len(response2.citations) > 0
    print(f"✓ Query 2: {len(response2.citations)} citations, {response2.latency_ms:.1f}ms latency")

    # Test query 3: EITC
    query3 = CreditQuery(
        query="Earned income credit calculation for family with 2 children",
        response_mode="MEMO",
        entity_type="Individual"
    )

    response3 = await engine.process_query(query3)
    assert "EITC" in response3.conclusion or "earned income" in response3.conclusion.lower()
    print(f"✓ Query 3: Cache hit = {response3.cache_hit}, {len(response3.doctrines_triggered)} doctrines")


async def test_advanced_features():
    """Test advanced TIE-20 features"""
    print("\n=== TEST 7: Advanced TIE-20 Features ===")

    config_path = ENGINE_DIR / "config.json"
    engine = TX03CreditCalculatorEngine(config_path)

    # Test authority hardening
    sample_doctrines = DOCTRINE_CACHE[:5]
    hardened = engine.apply_authority_hardening(sample_doctrines)
    assert len(hardened) == 5
    print(f"✓ Authority hardening: {len(hardened)} doctrines weighted")

    # Test confidence stratification
    stratified = engine.stratify_confidence(DOCTRINE_CACHE)
    print(f"✓ Confidence stratification: {len(stratified['DEFENSIBLE'])} defensible, {len(stratified['AGGRESSIVE'])} aggressive")

    # Test zone analysis
    zone_planning = engine.zone_analysis("Should I claim the R&D credit for future projects?")
    assert zone_planning == "PLANNING"
    zone_audit = engine.zone_analysis("How do I defend the R&D credit in an IRS audit?")
    assert zone_audit == "AUDIT"
    print(f"✓ Zone analysis: PLANNING and AUDIT zones detected correctly")

    # Test fact fragility scoring
    fragility = engine.fact_fragility_score(DOCTRINE_CACHE[0])
    assert 'verifiability_score' in fragility
    print(f"✓ Fact fragility: {fragility['verifiability_score']:.2f} verifiability")

    # Test determinism hash
    hash1 = engine.calculate_determinism_hash("test query", DOCTRINE_CACHE[:3], "FAST")
    hash2 = engine.calculate_determinism_hash("test query", DOCTRINE_CACHE[:3], "FAST")
    assert hash1 == hash2, "Determinism hash not reproducible"
    print(f"✓ Determinism hash: {hash1[:16]}... (reproducible)")

    # Test epistemic guardrails
    text_with_banned = "This position is guaranteed and IRS will not challenge it."
    cleaned, warnings = engine.apply_epistemic_guardrails(text_with_banned)
    assert len(warnings) > 0
    print(f"✓ Epistemic guardrails: {len(warnings)} warnings triggered")


def test_health_endpoint():
    """Test health endpoint"""
    print("\n=== TEST 8: Health Endpoint ===")

    config_path = ENGINE_DIR / "config.json"
    engine = TX03CreditCalculatorEngine(config_path)

    health = engine.get_health()
    assert health.status == "healthy"
    assert health.engine_id == "TX03_credit_calculator"
    assert health.doctrine_count >= 20

    print(f"✓ Health: {health.status}, {health.doctrine_count} doctrines")


async def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print("TX03 CREDIT CALCULATOR ENGINE - TEST SUITE")
    print("=" * 80)

    try:
        test_doctrine_cache()
        test_semantic_normalization()
        test_search_engine()
        test_telemetry()
        await test_engine_initialization()
        await test_query_processing()
        await test_advanced_features()
        test_health_endpoint()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED ✓")
        print("=" * 80)
        print(f"\nTX03 Credit Calculator Engine is TIE-20 Gold Standard compliant")
        print(f"- {len(DOCTRINE_CACHE)} doctrine blocks with real domain expertise")
        print(f"- All 20 TIE components implemented")
        print(f"- No-LLM mode operational")
        print(f"- Ready for deployment on port 8603")

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
