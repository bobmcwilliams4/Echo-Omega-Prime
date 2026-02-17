"""
LM01 Title Examination Engine
==============================

ECHO OMEGA PRIME - Landman Intelligence System
Engine ID: LM01
Category: LANDMAN / OIL & GAS
Version: 1.0.0

Full title examination engine for constructing chains of title,
detecting defects, generating title opinions, calculating mineral
and surface ownership interests, and producing run sheets.

Texas-specific title standards implemented with support for:
- Chain of title construction from recorded instruments
- Defect detection (gap in chain, missing heir, expired lien, etc.)
- Title opinion generation (preliminary, supplemental, final)
- Curative requirement identification
- Mineral/surface ownership split tracking
- Interest calculation through conveyance chain
- Run sheet generation
- After-acquired title doctrine
- Estoppel by deed
- Shelter rule / Bona fide purchaser
- Recording act priorities (race-notice)

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

__version__ = "1.0.0"
__engine_id__ = "LM01"
__engine_name__ = "Title Examination Engine"
__category__ = "LANDMAN"
__port__ = 8421

from .engine import (
    TitleExaminationEngine,
    TitleChainBuilder,
    DefectDetector,
    TitleOpinionGenerator,
    CurativeAnalyzer,
    InterestCalculator,
    RunSheetBuilder,
)
from .doctrines import (
    TitleDoctrineCache,
    TexasTitleStandard,
    DefectClassification,
    CurativeStandard,
    RecordingActRule,
    TEXAS_TITLE_STANDARDS,
    DEFECT_CLASSIFICATIONS,
    CURATIVE_STANDARDS,
)
from .semantic import (
    TitleSemanticDictionary,
    InstrumentTerms,
    LegalDescriptionTerms,
    ConveyanceLanguage,
    ReservationLanguage,
)
from .search import (
    TitleSearchEngine,
    SearchResult,
    SearchQuery,
    GrantorGranteeIndex,
)
from .telemetry import (
    TitleExamTelemetry,
    ExamMetrics,
    QueryTracker,
    AuditTrail,
)

__all__ = [
    # Engine
    "TitleExaminationEngine",
    "TitleChainBuilder",
    "DefectDetector",
    "TitleOpinionGenerator",
    "CurativeAnalyzer",
    "InterestCalculator",
    "RunSheetBuilder",
    # Doctrines
    "TitleDoctrineCache",
    "TexasTitleStandard",
    "DefectClassification",
    "CurativeStandard",
    "RecordingActRule",
    "TEXAS_TITLE_STANDARDS",
    "DEFECT_CLASSIFICATIONS",
    "CURATIVE_STANDARDS",
    # Semantic
    "TitleSemanticDictionary",
    "InstrumentTerms",
    "LegalDescriptionTerms",
    "ConveyanceLanguage",
    "ReservationLanguage",
    # Search
    "TitleSearchEngine",
    "SearchResult",
    "SearchQuery",
    "GrantorGranteeIndex",
    # Telemetry
    "TitleExamTelemetry",
    "ExamMetrics",
    "QueryTracker",
    "AuditTrail",
]
