"""
LM04 Mineral Interest Tracker Engine
=====================================

ECHO OMEGA PRIME - Landman Intelligence Division
Engine ID: LM04
Port: 8434
Version: 1.0.0

Tracks mineral interest ownership through time, conveyances, probate,
and other transfers. Computes net mineral acres, classifies interest
types, detects conflicts, and provides timeline visualization data.

Integrates with:
    - LM01 Title Examination Engine (title chain data)
    - LM02 Lease Analysis Engine (lease burden data)
    - LM03 Due Diligence Engine (validation data)
    - ShadowGlass (document retrieval)
    - ENCORE (county scraping)

Author: ECHO OMEGA PRIME
Authority: Commander Bobby Don McWilliams II
"""

__version__ = "1.0.0"
__engine_id__ = "LM04"
__engine_name__ = "Mineral Interest Tracker"
__port__ = 8434

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DOCTRINE_PATH = ENGINE_ROOT / "doctrines.py"

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__port__",
    "ENGINE_ROOT",
    "CONFIG_PATH",
    "DOCTRINE_PATH",
]
