"""
Quick test of P07 Fiduciary Duty Engine
"""

import sys
from pathlib import Path

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent))

from engine import FiduciaryDutyEngine

def test_basic_query():
    """Test basic fiduciary duty query"""
    engine = FiduciaryDutyEngine()

    # Test query
    query = "Can an executor purchase property from the estate they are administering?"

    print("Testing P07 Fiduciary Duty Engine")
    print("="* 60)
    print(f"Query: {query}\n")

    # Run query
    response = engine.three_layer_response(
        query=query,
        response_mode="DEFENSE",
        position_zone="AUDIT"
    )

    print(f"Response Mode: {response.response_mode}")
    print(f"Layer Used: {response.layer_used}")
    print(f"Latency: {response.latency_ms:.0f}ms")
    print(f"Confidence: {response.confidence_level}")
    print(f"Issue Categories: {', '.join(response.issue_categories)}")
    print(f"Doctrines Matched: {len(response.doctrine_matches)}")
    print(f"\nResponse:\n{response.response_text}")
    print(f"\nCitations: {response.citations[:3]}")
    print(f"\nDeterminism Hash: {response.determinism_hash}")

    print("\n" + "="* 60)
    print("ENGINE TEST PASSED")


if __name__ == "__main__":
    test_basic_query()
