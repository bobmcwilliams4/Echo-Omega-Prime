"""
LM05 Chain of Title Builder Engine
====================================
ECHO OMEGA PRIME - Landman Intelligence Division

Constructs, validates, and analyzes chains of title from recorded instruments.
The backbone of title examination for oil and gas land operations.

Features:
    - Chain construction from sovereign patent to current owner
    - Link validation (execution, acknowledgment, delivery)
    - Gap detection and classification (temporal, conveyance, recording)
    - Branch handling for fractional conveyances and multiple grantees
    - Merger detection when fee simple reconstitutes
    - Timeline visualization data generation
    - Integration with Reeves County data (G: drive 415K files)
    - Integration with ENCORE scraper and ShadowGlass
    - Texas recording act (race-notice) analysis
    - After-acquired title and estoppel by deed tracking

Engine Architecture:
    - doctrines.py: 92+ chain of title doctrines and legal frameworks
    - semantic.py: Chain terminology dictionary and normalization
    - search.py: Instrument search by grantor, grantee, legal, date, doc#
    - telemetry.py: Performance metrics, audit trail, deterministic hashing
    - engine.py: Core chain building, validation, and analysis logic
    - config.json: Configuration for chain rules, thresholds, integrations

Authority: Bobby Don McWilliams II (11.0 SUPREME SOVEREIGN)
Build System: ECHO OMEGA PRIME Cloudflare Architecture
"""

__version__ = "1.0.0"
__engine_id__ = "LM05"
__engine_name__ = "Chain of Title Builder"
__category__ = "LANDMAN"
__subcategory__ = "CHAIN_OF_TITLE"
__port__ = 8405
__author__ = "ECHO OMEGA PRIME Build System"

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__category__",
    "__subcategory__",
    "__port__",
    "ENGINE_ROOT",
    "CONFIG_PATH",
]
