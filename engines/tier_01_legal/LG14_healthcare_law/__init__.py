"""
LG14 Healthcare Law Engine
=============================
TIE-20 compliant healthcare law analysis engine.

Provides expert-finding analysis across HIPAA privacy/security/breach
notification, HITECH Act, ACA compliance, Medicare/Medicaid fraud (False
Claims Act, Anti-Kickback Statute, Stark Law), medical malpractice,
informed consent, patient rights, clinical trials/IRB, FDA drug/device
regulation, mental health parity (MHPAEA), EMTALA, telemedicine regulation,
state medical board licensing, healthcare entity M&A (CON laws), tax-exempt
hospital requirements (IRC 501(r)), pharmacy law, substance abuse
confidentiality (42 CFR Part 2), public health emergency law, and
healthcare data interoperability (21st Century Cures Act).

Engine ID: LG14
Port: 8404
Tier: LEGAL (Authority 5.0)
Mode: EF (Expert Findings)
Version: 2.0.0

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (fast, analysis, memo, compliance_audit, regulatory_review)
    3.  doctrine_cache
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search_tfidf (TF-IDF inverted index)
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
__engine_id__ = "LG14"
__engine_name__ = "Healthcare Law"
__port__ = 8404
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
    "doctrines",
    "semantic",
    "search",
    "telemetry",
    "engine",
]

HEALTHCARE_LAW_DOMAINS: list[str] = [
    "hipaa_privacy",
    "hipaa_security",
    "hipaa_breach_notification",
    "hitech_act",
    "aca_compliance",
    "medicare_fraud",
    "medicaid_fraud",
    "false_claims_act",
    "anti_kickback_statute",
    "stark_law",
    "medical_malpractice",
    "informed_consent",
    "patient_rights",
    "clinical_trials",
    "irb_review",
    "fda_drug_regulation",
    "fda_device_regulation",
    "mental_health_parity",
    "emtala",
    "telemedicine",
    "state_licensing",
    "healthcare_ma",
    "con_laws",
    "tax_exempt_hospitals",
    "pharmacy_law",
    "substance_abuse_confidentiality",
    "public_health_emergency",
    "healthcare_interoperability",
    "information_blocking",
]
