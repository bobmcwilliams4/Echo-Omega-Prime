"""
LM03 Division Order Engine
===========================

ECHO OMEGA PRIME - Landman Intelligence System
Engine ID: LM03
Category: LANDMAN / OIL & GAS
Version: 2.0.0
Mode: DET (Deterministic)
Port: 8411
Authority: 5.0

Production-grade division order engine for computing decimal interest
ownership (working interest, royalty interest, overriding royalty,
net revenue interest, cost-bearing interest), constructing pay decks,
tracing interests through chain of title, handling suspense/escheat
procedures, and generating division order title opinions.

Domain coverage:
- Division order title opinions
- Decimal interest calculation (WI, RI, ORRI, NRI, CBI)
- Division order ratification process
- Suspense/escheat procedures (Tex. Property Code Ch. 72)
- Interest owner identification and verification
- Pooling/unitization effects on interests
- JOA provisions and operator/non-operator accounting
- Texas Natural Resources Code Ch. 91 compliance
- Revenue distribution and pay deck construction
- Fractional mineral conveyances and decimal conversion
- Interest tracing through chain of title
- Duhig rule application and proportionate reduction
- After-acquired title doctrine effects
- Farmout agreement interests, carried interests, back-in rights

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

__version__ = "2.0.0"
__engine_id__ = "LM03"
__engine_name__ = "Division Order Engine"
__category__ = "LANDMAN"
__port__ = 8411
__mode__ = "DET"
__authority__ = 5.0

from pathlib import Path

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"

from .engine import (
    DivisionOrderEngine,
    InterestCalculator,
    DecimalConverter,
    ChainOfTitleTracer,
    PayDeckBuilder,
    SuspenseManager,
    RevenueDistributor,
    DuhigRuleEngine,
    PoolingUnitHandler,
    RatificationTracker,
)
from .doctrines import (
    DivisionOrderDoctrineCache,
    DoctrineCacheBlock,
    DoctrineCategory,
    build_doctrine_cache,
    search_doctrines,
    get_coverage_map,
    verify_doctrine_integrity,
)
from .semantic import (
    DivisionOrderSemanticDictionary,
    SemanticDomain,
    SemanticTerm,
    InterestTermNormalizer,
    DecimalFormatConverter,
    ChainOfTitleTerms,
)
from .search import (
    DoctrineSearchIndex,
    DivisionOrderSearcher,
    InterestTracer,
    RevenueDistributionCalculator,
    SuspenseAnalyzer,
)
from .telemetry import (
    DivisionOrderTelemetry,
    OperationType,
    AuditEventType,
    ErrorSeverity,
    compute_deterministic_hash,
    compute_interest_hash,
)

__all__ = [
    # Engine
    "DivisionOrderEngine",
    "InterestCalculator",
    "DecimalConverter",
    "ChainOfTitleTracer",
    "PayDeckBuilder",
    "SuspenseManager",
    "RevenueDistributor",
    "DuhigRuleEngine",
    "PoolingUnitHandler",
    "RatificationTracker",
    # Doctrines
    "DivisionOrderDoctrineCache",
    "DoctrineCacheBlock",
    "DoctrineCategory",
    "build_doctrine_cache",
    "search_doctrines",
    "get_coverage_map",
    "verify_doctrine_integrity",
    # Semantic
    "DivisionOrderSemanticDictionary",
    "SemanticDomain",
    "SemanticTerm",
    "InterestTermNormalizer",
    "DecimalFormatConverter",
    "ChainOfTitleTerms",
    # Search
    "DoctrineSearchIndex",
    "DivisionOrderSearcher",
    "InterestTracer",
    "RevenueDistributionCalculator",
    "SuspenseAnalyzer",
    # Telemetry
    "DivisionOrderTelemetry",
    "OperationType",
    "AuditEventType",
    "ErrorSeverity",
    "compute_deterministic_hash",
    "compute_interest_hash",
]
