"""
LM15 Water Rights Engine
=========================

ECHO OMEGA PRIME - Landman Intelligence System
Engine ID: LM15
Category: LANDMAN / WATER_RIGHTS
Mode: DET (Deterministic)
Version: 2.0.0
Port: 8413
Authority: 5.0

Comprehensive Texas water rights analysis engine covering:
- Groundwater law (rule of capture, East v Pecos County, EAA v Day)
- Groundwater conservation districts (GCDs, TWC Chapter 36)
- Surface water rights (prior appropriation, TWC Chapter 11)
- Produced water management in oil & gas operations
- Saltwater disposal wells (SWD, UIC Class II)
- Water recycling in hydraulic fracturing
- TCEQ water permits and surface water appropriation
- Edwards Aquifer Authority regulation
- Ogallala Aquifer depletion and management
- Water rights conveyancing (severance from surface estate)
- Groundwater marketing, export, and conjunctive use
- Desalination law and brackish water development
- Interstate water compacts (Pecos River, Rio Grande, Red River)
- Federal Clean Water Act Section 404 (dredge and fill)
- Safe Drinking Water Act (UIC program)
- Texas Water Development Board planning and data
- Drought contingency planning and water district taxation
- Produced water beneficial reuse regulations
- Flowback water handling and freshwater sourcing for fracking
- Pipeline right-of-way for water transport
- Surface owner water rights vs mineral lessee water use
- Accommodation doctrine applied to water
- RRC Statewide Rule 8 (protection of fresh water in drilling)

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

__version__ = "2.0.0"
__engine_id__ = "LM15"
__engine_name__ = "Water Rights Engine"
__category__ = "LANDMAN"
__port__ = 8413
__mode__ = "DET"
__authority__ = 5.0

from .engine import (
    WaterRightsEngine,
    WaterRightClassifier,
    GroundwaterAnalyzer,
    SurfaceWaterAnalyzer,
    ProducedWaterManager,
    DisposalWellComplianceAnalyzer,
    AquiferAnalysisEngine,
    WaterConveyanceTracker,
    AccommodationDoctrineEvaluator,
    FreshwaterProtectionChecker,
)
from .doctrines import (
    DoctrineCacheBlock,
    DoctrineCategory,
    AuthorityLevel,
    JurisdictionScope,
    RiskLevel,
    GroundwaterRule,
    SurfaceWaterRule,
    ProducedWaterRegulation,
    InjectionWellStandard,
    AquiferProtectionRule,
    InterstateCompactProvision,
    build_doctrine_cache,
    search_doctrines,
    get_coverage_map,
    verify_doctrine_integrity,
)
from .semantic import (
    WaterRightsSemanticDictionary,
    GroundwaterRightsAnalyzer,
    SurfaceWaterPermitChecker,
    ProducedWaterComplianceEngine,
    AquiferAnalyzer,
    SemanticTerm,
    TermCategory,
)
from .search import (
    DoctrineSearchIndex,
    WaterRightsSearcher,
    DisposalWellComplianceChecker,
    WaterPermitTracker,
    AquiferDataSearcher,
    SearchResult,
    SearchQuery,
)
from .telemetry import (
    WaterRightsTelemetry,
    DriftWatcher,
    AnalysisMetrics,
    AuditTrail,
    PerformanceMonitor,
    OperationType,
    AuditAction,
    MetricLevel,
)

__all__ = [
    # Engine
    "WaterRightsEngine",
    "WaterRightClassifier",
    "GroundwaterAnalyzer",
    "SurfaceWaterAnalyzer",
    "ProducedWaterManager",
    "DisposalWellComplianceAnalyzer",
    "AquiferAnalysisEngine",
    "WaterConveyanceTracker",
    "AccommodationDoctrineEvaluator",
    "FreshwaterProtectionChecker",
    # Doctrines
    "DoctrineCacheBlock",
    "DoctrineCategory",
    "AuthorityLevel",
    "JurisdictionScope",
    "RiskLevel",
    "GroundwaterRule",
    "SurfaceWaterRule",
    "ProducedWaterRegulation",
    "InjectionWellStandard",
    "AquiferProtectionRule",
    "InterstateCompactProvision",
    "build_doctrine_cache",
    "search_doctrines",
    "get_coverage_map",
    "verify_doctrine_integrity",
    # Semantic
    "WaterRightsSemanticDictionary",
    "GroundwaterRightsAnalyzer",
    "SurfaceWaterPermitChecker",
    "ProducedWaterComplianceEngine",
    "AquiferAnalyzer",
    "SemanticTerm",
    "TermCategory",
    # Search
    "DoctrineSearchIndex",
    "WaterRightsSearcher",
    "DisposalWellComplianceChecker",
    "WaterPermitTracker",
    "AquiferDataSearcher",
    "SearchResult",
    "SearchQuery",
    # Telemetry
    "WaterRightsTelemetry",
    "DriftWatcher",
    "AnalysisMetrics",
    "AuditTrail",
    "PerformanceMonitor",
    "OperationType",
    "AuditAction",
    "MetricLevel",
]
