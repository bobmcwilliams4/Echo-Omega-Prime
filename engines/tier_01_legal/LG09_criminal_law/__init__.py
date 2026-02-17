"""
LG09 Criminal Law Engine - ECHO OMEGA PRIME
=============================================
Full TIE-20 architecture criminal law analysis engine.

Domain: Criminal Law (Federal + Texas State)
Port: 8399
Authority: 11.0 SOVEREIGN

Components:
    - engine.py: Main FastAPI application with 20 TIE components
    - doctrines.py: Pre-loaded criminal law doctrine cache
    - semantic.py: Criminal law semantic normalization
    - search.py: ChromaDB vector search integration
    - telemetry.py: Performance telemetry and metrics
    - config.json: Engine configuration

Author: ECHO OMEGA PRIME
"""

__version__ = "1.0.0"
__engine_id__ = "LG09"
__domain__ = "criminal_law"
__port__ = 8399
