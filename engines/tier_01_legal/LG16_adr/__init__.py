"""
LG16 ADR Engine (Alternative Dispute Resolution)
==================================================
Comprehensive alternative dispute resolution analysis engine covering
arbitration (FAA 9 USC 1-16, RUAA, AAA Commercial/Construction/Employment
Rules, JAMS, FINRA, ICSID, UNCITRAL, ICC), mediation (UMA, court-annexed,
facilitative/evaluative/transformative), negotiation theory (BATNA/WATNA/ZOPA),
online dispute resolution (ODR), med-arb/arb-med hybrid processes, class action
arbitration, arbitrability of claims, arbitration clause drafting/enforceability,
judicial review of arbitration awards (vacatur under FAA Section 10),
confirmation/enforcement of awards (New York Convention), discovery in
arbitration, emergency arbitrator provisions, multi-party arbitration,
Texas ADR Act (CPRC Ch. 154), securities arbitration, employment arbitration
(Epic Systems), consumer arbitration, construction disputes (AIA contracts),
real estate disputes, oil and gas disputes (JOA arbitration clauses),
international commercial arbitration, and investment treaty arbitration.

Port: 8406
Engine: LG16 ADR Engine
Version: 2.0.0
TIE Components: 20/20
Architecture: TIE-20 Pattern
Mode: DET (Deterministic)
Authority: 5.0
Tier: LEGAL
"""

__version__ = "2.0.0"
__engine_id__ = "LG16"
__engine_name__ = "ADR Engine (Alternative Dispute Resolution)"
__port__ = 8406
__authority__ = 5.0
__mode__ = "DET"
__tier__ = "LEGAL"

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
VECTOR_DB_DIR = ENGINE_ROOT / "vector_db"
TELEMETRY_DIR = ENGINE_ROOT / "telemetry_data"
LOGS_DIR = ENGINE_ROOT / "logs"
AUDIT_DIR = ENGINE_ROOT / "audit"

for _dir in [DOCTRINE_CACHE_DIR, VECTOR_DB_DIR, TELEMETRY_DIR, LOGS_DIR, AUDIT_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__port__",
    "__authority__",
    "__mode__",
    "__tier__",
    "ENGINE_ROOT",
    "CONFIG_PATH",
    "DOCTRINE_CACHE_DIR",
    "VECTOR_DB_DIR",
    "TELEMETRY_DIR",
    "LOGS_DIR",
    "AUDIT_DIR",
]
