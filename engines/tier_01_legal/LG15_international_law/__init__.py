"""
LG15 International Law Engine
================================
Comprehensive international law analysis engine covering public international law
(UN Charter, ICJ Statute, Vienna Convention on Treaties), international trade law
(WTO/GATT, TRIPS, ICSID), international humanitarian law (Geneva Conventions,
Hague Conventions), international human rights (ICCPR, ICESCR, ECHR), foreign
sovereign immunity (FSIA), international arbitration (UNCITRAL, ICC, ICSID),
cross-border transactions (CISG, Incoterms, UCP 600), sanctions and export
controls (OFAC, EAR, ITAR), extraterritorial jurisdiction, treaty interpretation,
diplomatic and consular law, international criminal law (ICC Rome Statute), law
of the sea (UNCLOS), international environmental law (Paris Agreement, Montreal
Protocol), bilateral investment treaties, conflict of laws and choice of law,
foreign judgments recognition and enforcement, anti-corruption (FCPA, UK Bribery
Act), and international tax treaties (OECD Model Convention).

Port: 8405
Engine: LG15 International Law
Version: 2.0.0
Mode: EF (Expert Findings)
Authority: 5.0
TIE Components: 20/20
Architecture: TIE-20 Pattern
"""

__version__ = "2.0.0"
__engine_id__ = "LG15"
__engine_name__ = "International Law Engine"
__port__ = 8405
__mode__ = "EF"
__authority__ = 5.0

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"
DOCTRINE_CACHE_DIR = ENGINE_ROOT / "doctrine_cache"
VECTOR_DB_DIR = ENGINE_ROOT / "vector_db"
TELEMETRY_DIR = ENGINE_ROOT / "telemetry_data"
LOGS_DIR = ENGINE_ROOT / "logs"

for _dir in [DOCTRINE_CACHE_DIR, VECTOR_DB_DIR, TELEMETRY_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__port__",
    "__mode__",
    "__authority__",
    "ENGINE_ROOT",
    "CONFIG_PATH",
    "DOCTRINE_CACHE_DIR",
    "VECTOR_DB_DIR",
    "TELEMETRY_DIR",
    "LOGS_DIR",
]
