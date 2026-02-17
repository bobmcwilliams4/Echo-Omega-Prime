"""
LM13 Water Rights Analyzer Engine
===================================

ECHO OMEGA PRIME - Landman Intelligence System
Engine ID: LM13
Category: LANDMAN / OIL & GAS / WATER RIGHTS
Version: 1.0.0

Comprehensive water rights analysis engine for oil and gas operations,
surface use, and environmental compliance in Texas.

Core capabilities:
- Water right identification and classification (surface vs groundwater)
- Groundwater conservation district rule analysis (100+ Texas GCDs)
- Produced water disposal permit tracking (UIC Class II)
- Injection well compliance monitoring (Railroad Commission H-1/H-1A)
- Surface use agreement water provisions analysis
- Freshwater source identification and protection zone mapping
- Water transport and sale agreement analysis
- Environmental compliance risk scoring
- Texas Water Code provision mapping
- Rule of capture (East doctrine) analysis
- Prior appropriation (surface water) right chain
- Edwards Aquifer Authority rule compliance
- Brackish water desalination rights
- Water recycling/reuse in hydraulic fracturing
- Saltwater disposal well regulation (SWD)
- Ogallala / Pecos Valley aquifer considerations for Permian Basin
- Produced water midstream infrastructure analysis

Texas-specific implementation covering:
- Texas Water Code (TWC) Chapters 11-36
- Texas Administrative Code Title 30 (TCEQ) and Title 16 (RRC)
- Texas Natural Resources Code Chapter 122
- Railroad Commission Statewide Rule 9 (disposal/injection wells)
- TCEQ Chapter 297 (water rights permits)
- Edwards Aquifer Authority Act
- Groundwater Conservation District enabling statutes

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

__version__ = "1.0.0"
__engine_id__ = "LM13"
__engine_name__ = "Water Rights Analyzer Engine"
__category__ = "LANDMAN"
__port__ = 8413

from .engine import (
    WaterRightsAnalyzerEngine,
    WaterRightClassifier,
    GroundwaterDistrictAnalyzer,
    ProducedWaterTracker,
    InjectionWellMonitor,
    SurfaceUseWaterAnalyzer,
    FreshwaterSourceIdentifier,
    WaterTransportAnalyzer,
    ComplianceRiskScorer,
)
from .doctrines import (
    WaterDoctrineCache,
    TexasWaterDoctrine,
    GroundwaterRule,
    SurfaceWaterRule,
    ProducedWaterRegulation,
    InjectionWellStandard,
    AquiferProtectionRule,
    TEXAS_WATER_DOCTRINES,
    GROUNDWATER_RULES,
    SURFACE_WATER_RULES,
    PRODUCED_WATER_REGULATIONS,
    INJECTION_WELL_STANDARDS,
    AQUIFER_PROTECTION_RULES,
)
from .semantic import (
    WaterRightsSemanticDictionary,
    GroundwaterTerms,
    SurfaceWaterTerms,
    ProducedWaterTerms,
    InjectionWellTerms,
    AquiferTerms,
    PermitTerms,
    ComplianceTerms,
)
from .search import (
    WaterRightsSearchEngine,
    WaterSearchResult,
    WaterSearchQuery,
    PermitIndex,
    AquiferIndex,
    OperatorIndex,
)
from .telemetry import (
    WaterRightsTelemetry,
    AnalysisMetrics,
    ComplianceTracker,
    AuditTrail,
    PerformanceMonitor,
)

__all__ = [
    # Engine
    "WaterRightsAnalyzerEngine",
    "WaterRightClassifier",
    "GroundwaterDistrictAnalyzer",
    "ProducedWaterTracker",
    "InjectionWellMonitor",
    "SurfaceUseWaterAnalyzer",
    "FreshwaterSourceIdentifier",
    "WaterTransportAnalyzer",
    "ComplianceRiskScorer",
    # Doctrines
    "WaterDoctrineCache",
    "TexasWaterDoctrine",
    "GroundwaterRule",
    "SurfaceWaterRule",
    "ProducedWaterRegulation",
    "InjectionWellStandard",
    "AquiferProtectionRule",
    "TEXAS_WATER_DOCTRINES",
    "GROUNDWATER_RULES",
    "SURFACE_WATER_RULES",
    "PRODUCED_WATER_REGULATIONS",
    "INJECTION_WELL_STANDARDS",
    "AQUIFER_PROTECTION_RULES",
    # Semantic
    "WaterRightsSemanticDictionary",
    "GroundwaterTerms",
    "SurfaceWaterTerms",
    "ProducedWaterTerms",
    "InjectionWellTerms",
    "AquiferTerms",
    "PermitTerms",
    "ComplianceTerms",
    # Search
    "WaterRightsSearchEngine",
    "WaterSearchResult",
    "WaterSearchQuery",
    "PermitIndex",
    "AquiferIndex",
    "OperatorIndex",
    # Telemetry
    "WaterRightsTelemetry",
    "AnalysisMetrics",
    "ComplianceTracker",
    "AuditTrail",
    "PerformanceMonitor",
]
