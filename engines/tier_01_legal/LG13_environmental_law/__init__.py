"""
LG13 Environmental Law Engine
==============================
Comprehensive environmental law analysis engine covering NEPA, CAA, CWA,
RCRA, CERCLA/Superfund, TSCA, ESA, FIFRA, SDWA, OPA, environmental impact
assessment, permits, hazardous materials, brownfield redevelopment, Phase I/II
ESA, underground storage tanks, TCEQ, RRC environmental authority, Permian
Basin environmental issues, carbon credits, climate regulation, environmental
justice, and citizen suits.

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
TIE Components: 20/20
Architecture: TIE-20 Pattern
"""

__version__ = "1.0.0"
__engine_id__ = "LG13"
__engine_name__ = "Environmental Law Engine"
__port__ = 8403

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
VECTOR_DB_DIR = ENGINE_ROOT / "vector_db"
TELEMETRY_DIR = ENGINE_ROOT / "telemetry_data"
LOGS_DIR = ENGINE_ROOT / "logs"

for _dir in [DOCTRINE_CACHE_DIR, VECTOR_DB_DIR, TELEMETRY_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
