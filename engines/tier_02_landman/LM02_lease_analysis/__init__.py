"""
LM02 Lease Analysis Engine
Tier: T2_LANDMAN | Mode: DET | Port: 8402

Professional-grade oil and gas lease analysis engine for the Permian Basin.
Parses, analyzes, and evaluates oil and gas leases covering:
    - Habendum clause analysis (primary/secondary term)
    - Drilling and delay rental clause interpretation
    - Royalty and overriding royalty provision computation
    - Pooling and unitization clause evaluation
    - Pugh clause impact analysis
    - Shut-in royalty, force majeure, continuous development
    - Surface use rights, depth limitations, retained acreage
    - Top lease provisions, preferential rights, assignments
    - Mother Hubbard clause, surrender clause
    - Net revenue interest calculation across pooled units
    - Lease expiration tracking and alert generation
    - Depth severance handling for stacked pay zones
    - Integration with ENCORE county scraping and ShadowGlass

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
"""

__version__ = "1.0.0"
__engine_id__ = "LM02"
__engine_name__ = "Lease Analysis Engine"
__tier__ = "T2_LANDMAN"
__mode__ = "DET"
__port__ = 8402

from .engine import (
    LM02LeaseAnalysisEngine,
    LeaseAnalysisRequest,
    LeaseAnalysisResponse,
    LeaseComparisonRequest,
    LeaseComparisonResponse,
    LeaseExpirationAlert,
    LeaseRecord,
    NRICalculationRequest,
    NRICalculationResponse,
    PughClauseAnalysis,
    RoyaltyCalculation,
    TermAnalysis,
)
from .doctrines import (
    DOCTRINE_CACHE,
    DOCTRINE_CACHE_VERSION,
    LeaseDoctrineBlock,
    get_doctrine,
    list_doctrine_keys,
    match_doctrine,
)
from .semantic import (
    normalize_lease_term,
    parse_legal_description,
    parse_royalty_fraction,
    verify_semantic_map_integrity,
)
from .search import (
    SearchResponse,
    search_leases,
    search_by_legal_description,
    search_by_lessor_lessee,
    search_expiring_leases,
)
from .telemetry import (
    TelemetryManager,
    get_telemetry,
    trace_query,
    complete_trace,
)

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__tier__",
    "__mode__",
    "__port__",
    "LM02LeaseAnalysisEngine",
    "LeaseAnalysisRequest",
    "LeaseAnalysisResponse",
    "LeaseRecord",
    "TermAnalysis",
    "RoyaltyCalculation",
    "PughClauseAnalysis",
    "LeaseExpirationAlert",
    "LeaseComparisonRequest",
    "LeaseComparisonResponse",
    "NRICalculationRequest",
    "NRICalculationResponse",
    "DOCTRINE_CACHE",
    "DOCTRINE_CACHE_VERSION",
    "LeaseDoctrineBlock",
    "get_doctrine",
    "list_doctrine_keys",
    "match_doctrine",
    "normalize_lease_term",
    "parse_legal_description",
    "parse_royalty_fraction",
    "verify_semantic_map_integrity",
    "SearchResponse",
    "search_leases",
    "search_by_legal_description",
    "search_by_lessor_lessee",
    "search_expiring_leases",
    "TelemetryManager",
    "get_telemetry",
    "trace_query",
    "complete_trace",
]
