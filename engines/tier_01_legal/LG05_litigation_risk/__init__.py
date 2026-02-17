"""
LG05 LITIGATION RISK ENGINE
TIE-20 compliant litigation risk assessment engine.

Engine ID: LG05
Tier: 1 (LEGAL)
Mode: DET (Deterministic)
Port: 8395
Authority: 5.0

Components:
    engine.py    - Main FastAPI application with all 20 TIE components
    doctrines.py - Litigation risk doctrine knowledge base (50+ blocks)
    semantic.py  - Semantic normalization for litigation terminology
    search.py    - Vector search for case law and precedent matching
    telemetry.py - Telemetry, metrics, audit trail infrastructure
    config.json  - Engine configuration

Author: ECHO OMEGA PRIME
"""

__version__ = "1.0.0"
__engine_id__ = "LG05"
__engine_name__ = "Litigation Risk Engine"
__port__ = 8395
