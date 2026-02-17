"""
LG18 Legislative Analysis Engine
===================================
TIE-20 compliant legislative analysis engine providing comprehensive
federal and state legislative process analysis, statutory construction,
bill drafting review, regulatory rulemaking analysis, and preemption
assessment.

Engine ID: LG18
Port: 8408
Tier: LEGAL (Authority 5.0)
Mode: EF (Expert Findings)
Version: 2.0.0

Domain Coverage:
    - Federal legislative process (Article I, Congressional procedure)
    - Committee structure, reconciliation, filibuster/cloture
    - State legislative process (Texas Legislature, bicameral procedure)
    - Bill drafting and analysis
    - Statutory construction canons (textualism, purposivism, plain meaning,
      ejusdem generis, noscitur a sociis, expressio unius)
    - Legislative history interpretation
    - Regulatory rulemaking (APA notice-and-comment, executive orders)
    - Chevron deference / Loper Bright Enterprises v. Ramos
    - Congressional oversight and appropriations
    - Legislative impact assessment
    - Lobbying regulation (LDA, FARA)
    - Ballot initiatives and referenda
    - Texas Sunset Review
    - Legislative redistricting
    - Constitutional amendments (Article V)
    - Preemption analysis (express, field, conflict)
    - Delegation doctrine
    - Enrolled bill doctrine
    - Pocket veto, signing statements
    - Legislative privilege (Speech or Debate Clause)

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, bill_analysis, regulatory_review)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_chromadb (TF-IDF inverted index implementation)
    8.  telemetry_module
    9.  doctrine_drift_watcher
    10. doctrine_coverage_map
    11. metrics_collector
    12. health_endpoint
    13. zoned_analysis
    14. fact_fragility_scoring
    15. audit_trail_jsonl
    16. determinism_hash_sha256
    17. fastapi_server
    18. loguru_logging
    19. multi_doctrine_decomposition
    20. deep_analysis_mode
"""

__version__ = "2.0.0"
__engine_id__ = "LG18"
__engine_name__ = "Legislative Analysis"
__port__ = 8408
__authority__ = 5.0
__tier__ = "LEGAL"
__mode__ = "EF"

__all__ = [
    "__version__",
    "__engine_id__",
    "__engine_name__",
    "__port__",
    "__authority__",
    "__tier__",
    "__mode__",
]
