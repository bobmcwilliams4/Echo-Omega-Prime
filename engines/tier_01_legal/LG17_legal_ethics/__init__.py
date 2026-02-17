"""
LG17 Legal Ethics Engine
=========================
Comprehensive legal ethics analysis engine covering ABA Model Rules of
Professional Conduct (all 8 categories), attorney-client privilege, work
product doctrine, conflicts of interest (concurrent/successive/imputed),
client confidentiality, competence/diligence/communication, fees and
fee-splitting, advertising/solicitation, unauthorized practice of law,
multijurisdictional practice, lawyer discipline/sanctions, malpractice
liability, fiduciary duties, trust account management (IOLTA),
organization as client, diminished capacity clients, prosecutorial ethics
(Brady obligations), judicial ethics (CJC), mediator ethics, arbitrator
disclosure obligations, Texas Disciplinary Rules of Professional Conduct,
Sarbanes-Oxley attorney reporting (SEC Part 205), legal tech ethics
(AI-assisted practice, ghost-writing, metadata).

Port: 8407
Engine: LG17 Legal Ethics
Version: 2.0.0
TIE Components: 20/20
Architecture: TIE-20 Pattern
Mode: DET (Deterministic)
"""

__version__ = "2.0.0"
__engine_id__ = "LG17"
__engine_name__ = "Legal Ethics Engine"
__port__ = 8407

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
VECTOR_DB_DIR = ENGINE_ROOT / "vector_db"
TELEMETRY_DIR = ENGINE_ROOT / "telemetry_data"
LOGS_DIR = ENGINE_ROOT / "logs"

for _dir in [DOCTRINE_CACHE_DIR, VECTOR_DB_DIR, TELEMETRY_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# Export key identifiers for cross-engine resolution
ENGINE_META = {
    "engine_id": __engine_id__,
    "engine_name": __engine_name__,
    "version": __version__,
    "port": __port__,
    "tier": "LEGAL",
    "authority": 5.0,
    "mode": "DET",
    "tie_version": "20.0",
    "domain": "legal_ethics",
    "doctrine_domains": [
        "aba_model_rules", "attorney_client_privilege", "work_product_doctrine",
        "conflicts_of_interest", "client_confidentiality", "competence_diligence",
        "fees_reasonableness", "advertising_solicitation", "unauthorized_practice",
        "multijurisdictional_practice", "lawyer_discipline", "malpractice_liability",
        "fiduciary_duties", "trust_accounts_iolta", "organization_as_client",
        "diminished_capacity", "prosecutorial_ethics", "judicial_ethics",
        "mediator_ethics", "arbitrator_disclosure", "texas_disciplinary_rules",
        "sarbanes_oxley_205", "legal_tech_ethics",
    ],
}
