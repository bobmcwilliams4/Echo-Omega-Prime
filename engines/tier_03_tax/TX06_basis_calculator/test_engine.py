"""
Quick test of TX06 Basis Calculator Engine
"""

import sys
from pathlib import Path

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent))

from engine import three_layer_engine

def test_cost_basis():
    """Test cost basis calculation"""
    result = three_layer_engine.process_query(
        query="What is the cost basis of property purchased for $500,000 with $50,000 in closing costs?",
        response_mode="FAST",
        entity_type="individual",
        property_details={
            "purchase_price": 500000,
            "acquisition_costs": 50000
        },
        context=None
    )

    print("=" * 80)
    print("TEST 1: Cost Basis Calculation")
    print("=" * 80)
    print(f"Query: {result['query']}")
    print(f"Calculated Basis: ${result['calculated_basis']:,.2f}" if result['calculated_basis'] else "N/A")
    print(f"Layer: {result['layer']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Confidence: {result['confidence_level']}")
    print(f"Doctrines Applied: {len(result['doctrines_applied'])}")
    print(f"\nConclusion: {result['conclusion'][:200]}...")
    print()

def test_inherited_basis():
    """Test stepped-up basis for inherited property"""
    result = three_layer_engine.process_query(
        query="What is the basis of real estate inherited from my father? FMV at death was $1,000,000.",
        response_mode="DEFENSE",
        entity_type="individual",
        property_details={
            "fmv_at_death": 1000000
        },
        context=None
    )

    print("=" * 80)
    print("TEST 2: Inherited Property Stepped-Up Basis")
    print("=" * 80)
    print(f"Query: {result['query']}")
    print(f"Calculated Basis: ${result['calculated_basis']:,.2f}" if result['calculated_basis'] else "N/A")
    print(f"Layer: {result['layer']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Confidence: {result['confidence_level']}")
    print(f"Doctrines Applied: {len(result['doctrines_applied'])}")
    for d in result['doctrines_applied']:
        print(f"  - {d['topic']}")
    print(f"\nConclusion: {result['conclusion'][:300]}...")
    print()

def test_gift_basis():
    """Test gift basis with gift tax adjustment"""
    result = three_layer_engine.process_query(
        query="What is my basis in stock received as a gift? Donor's basis was $200,000, FMV at gift was $500,000, gift tax paid was $60,000.",
        response_mode="MEMO",
        entity_type="individual",
        property_details={
            "donor_basis": 200000,
            "fmv_at_gift": 500000,
            "gift_tax_paid": 60000
        },
        context=None
    )

    print("=" * 80)
    print("TEST 3: Gift Basis with Gift Tax Adjustment")
    print("=" * 80)
    print(f"Query: {result['query']}")
    print(f"Calculated Basis: ${result['calculated_basis']:,.2f}" if result['calculated_basis'] else "N/A")
    print(f"Layer: {result['layer']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Confidence: {result['confidence_level']}")
    print(f"Response Mode: {result['response_mode']}")
    print(f"\nConclusion: {result['conclusion'][:400]}...")
    print()

def test_1031_exchange():
    """Test like-kind exchange basis"""
    result = three_layer_engine.process_query(
        query="What is my basis in replacement property received in a 1031 exchange?",
        response_mode="FAST",
        entity_type="individual",
        property_details={
            "relinquished_basis": 400000,
            "boot_received": 0,
            "boot_paid": 100000,
            "gain_recognized": 0
        },
        context=None
    )

    print("=" * 80)
    print("TEST 4: Like-Kind Exchange Basis (§1031)")
    print("=" * 80)
    print(f"Query: {result['query']}")
    print(f"Calculated Basis: ${result['calculated_basis']:,.2f}" if result['calculated_basis'] else "N/A")
    print(f"Layer: {result['layer']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Determinism Hash: {result['determinism_hash'][:16]}...")
    print()

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TX06 BASIS CALCULATOR ENGINE - VERIFICATION TESTS")
    print("=" * 80 + "\n")

    test_cost_basis()
    test_inherited_basis()
    test_gift_basis()
    test_1031_exchange()

    print("=" * 80)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)
