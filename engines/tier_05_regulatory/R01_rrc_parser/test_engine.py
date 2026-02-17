"""
Quick test of R01_rrc_parser engine functionality
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from engine import RRCDoctrineCacheEngine, ResponseMode, PositionZone, IssueCategory
from doctrines import DOCTRINE_BLOCKS


async def test_engine():
    """Test basic engine functionality."""
    print(f"Testing R01_rrc_parser with {len(DOCTRINE_BLOCKS)} doctrine blocks\n")

    # Initialize engine
    engine = RRCDoctrineCacheEngine(
        doctrine_blocks=DOCTRINE_BLOCKS,
        cloud_retriever=None,  # No cloud for basic test
        telemetry=None,
    )

    # Test queries
    test_queries = [
        ("W-1 permit application deadline", ResponseMode.FAST, PositionZone.PLANNING),
        ("Rule 37 spacing requirements for horizontal well", ResponseMode.DEFENSE, PositionZone.PLANNING),
        ("P-4 production reporting late filing penalties", ResponseMode.FAST, PositionZone.REPORTING),
        ("Plugging requirements inactive well", ResponseMode.MEMO, PositionZone.AUDIT),
    ]

    for query, mode, zone in test_queries:
        print(f"Query: {query}")
        print(f"Mode: {mode.value} | Zone: {zone.value}")

        analysis = await engine.three_layer_response(
            query=query,
            mode=mode,
            zone=zone,
            include_cloud=False,
        )

        print(f"Tier: {analysis.response_tier}")
        print(f"Doctrines triggered: {len(analysis.triggered_doctrines)}")
        if analysis.triggered_doctrines:
            print(f"Top doctrine: {analysis.triggered_doctrines[0].topic}")
        print(f"Confidence: {analysis.confidence.value}")
        print(f"Latency: {analysis.latency_ms:.1f}ms")
        print(f"Hash: {analysis.determinism_hash[:16]}...")
        print(f"Synthesis: {analysis.synthesis[:200]}...")
        print("-" * 80)
        print()

    print("\nEngine test complete!")


if __name__ == "__main__":
    asyncio.run(test_engine())
