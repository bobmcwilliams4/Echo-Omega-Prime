"""
LM14 Easement Analyzer Engine
================================

ECHO OMEGA PRIME - Landman Intelligence Division

Analyzes easements, rights-of-way, surface use agreements, and pipeline
corridors relevant to oil and gas operations. Covers express easements,
implied easements, easements by necessity, prescriptive easements,
appurtenant vs in gross, dominant/servient estate analysis, pipeline ROW
agreements, surface use agreements, road easements, utility easements,
Texas accommodation doctrine, reasonable use doctrine, surface damage acts,
pipeline condemnation (eminent domain), Texas Natural Resources Code
surface use provisions, abandonment/extinguishment, overburdening, scope
limitations, vertical and horizontal limits.

Engine ID: LM14
Port: 8434
Version: 1.0.0
Authority: 7.0 (LANDMAN TIER)
Mode: DET (Deterministic)
"""

__version__ = "1.0.0"
__engine_id__ = "LM14"
__engine_name__ = "Easement Analyzer"
__port__ = 8434
__authority__ = 7.0
__tier__ = "LANDMAN"
__mode__ = "DET"

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__port__",
    "__authority__",
    "__tier__",
    "__mode__",
    "ENGINE_ROOT",
    "CONFIG_PATH",
]
