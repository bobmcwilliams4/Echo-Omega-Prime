import hashlib
import re
import unicodedata

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "S08 Engine Team"
SEMANTIC_MAP_ENGINE = "S08_drift_detector"

# Domain: Statistical Process Control Charts, CUSUM, EWMA, Shewhart, Calibration Drift, Confidence Distribution, Inter-Engine Correlation, Seasonal Adjustment, Drift Attribution, Severity, Recalibration, Reporting, Baseline Comparison, Multivariate, Concept/Data Drift, KL Divergence, KS Test, Alert Thresholds, Root Cause, Correction, Watcher Baseline, Epistemic Gap, Fact Fragility, Zoned Analysis, Three-Layer Response, Multi-Doctrine Decomposition, Coverage Map, Audit Trail, Deep Analysis Composite

SEMANTIC_MAP = {
    # Statistical Process Control Charts
    "spc": "statistical_process_control_charts",
    "statistical process control": "statistical_process_control_charts",
    "process control chart": "statistical_process_control_charts",
    "control chart": "statistical_process_control_charts",
    "spc chart": "statistical_process_control_charts",
    "statistical process control chart": "statistical_process_control_charts",
    "process chart": "statistical_process_control_charts",
    "process monitoring chart": "statistical_process_control_charts",
    "statistical control chart": "statistical_process_control_charts",
    "statistical chart": "statistical_process_control_charts",
    "process monitoring": "statistical_process_control_charts",
    "monitoring chart": "statistical_process_control_charts",
    "spc charts": "statistical_process_control_charts",

    # CUSUM Change Point Detection
    "cusum": "cusum_change_point_detection",
    "cumulative sum": "cusum_change_point_detection",
    "cusum chart": "cusum_change_point_detection",
    "cusum test": "cusum_change_point_detection",
    "cusum detector": "cusum_change_point_detection",
    "cumulative sum chart": "cusum_change_point_detection",
    "cumulative sum test": "cusum_change_point_detection",
    "change point detection": "cusum_change_point_detection",
    "changepoint detection": "cusum_change_point_detection",
    "change-point detection": "cusum_change_point_detection",
    "cpd": "cusum_change_point_detection",
    "change point": "cusum_change_point_detection",
    "changepoint": "cusum_change_point_detection",
    "cusum algorithm": "cusum_change_point_detection",

    # EWMA Smoothing for Drift Detection
    "ewma": "ewma_smoothing_drift_detection",
    "exponentially weighted moving average": "ewma_smoothing_drift_detection",
    "ewma chart": "ewma_smoothing_drift_detection",
    "ewma smoothing": "ewma_smoothing_drift_detection",
    "ewma detector": "ewma_smoothing_drift_detection",
    "ewma test": "ewma_smoothing_drift_detection",
    "ewma drift detection": "ewma_smoothing_drift_detection",
    "ewma smoothing for drift": "ewma_smoothing_drift_detection",
    "exponential moving average": "ewma_smoothing_drift_detection",
    "ewma algorithm": "ewma_smoothing_drift_detection",

    # Shewhart Control Limits
    "shewhart": "shewhart_control_limits",
    "shewhart chart": "shewhart_control_limits",
    "shewhart control chart": "shewhart_control_limits",
    "shewhart limits": "shewhart_control_limits",
    "shewhart test": "shewhart_control_limits",
    "shewhart detector": "shewhart_control_limits",
    "shewhart control limits": "shewhart_control_limits",
    "shewhart algorithm": "shewhart_control_limits",
    "shewhart boundary": "shewhart_control_limits",

    # Calibration Drift Taxonomy
    "calibration drift": "calibration_drift_taxonomy",
    "calibration drift taxonomy": "calibration_drift_taxonomy",
    "calibration taxonomy": "calibration_drift_taxonomy",
    "calibration drift analysis": "calibration_drift_taxonomy",
    "calibration drift detection": "calibration_drift_taxonomy",
    "calibration drift classification": "calibration_drift_taxonomy",
    "calibration drift types": "calibration_drift_taxonomy",
    "calibration drift categories": "calibration_drift_taxonomy",
    "calibration drift taxonomy analysis": "calibration_drift_taxonomy",
    "calibration drift taxonomy classification": "calibration_drift_taxonomy",

    # Confidence Distribution Monitoring
    "confidence distribution": "confidence_distribution_monitoring",
    "confidence distribution monitoring": "confidence_distribution_monitoring",
    "confidence monitoring": "confidence_distribution_monitoring",
    "confidence distribution analysis": "confidence_distribution_monitoring",
    "confidence distribution detector": "confidence_distribution_monitoring",
    "confidence distribution test": "confidence_distribution_monitoring",
    "confidence distribution drift": "confidence_distribution_monitoring",
    "confidence distribution alert": "confidence_distribution_monitoring",
    "confidence distribution threshold": "confidence_distribution_monitoring",

    # Inter-Engine Correlation Drift
    "inter-engine correlation": "inter_engine_correlation_drift",
    "inter-engine correlation drift": "inter_engine_correlation_drift",
    "interengine correlation": "inter_engine_correlation_drift",
    "interengine correlation drift": "inter_engine_correlation_drift",
    "engine correlation drift": "inter_engine_correlation_drift",
    "inter-engine drift": "inter_engine_correlation_drift",
    "interengine drift": "inter_engine_correlation_drift",
    "correlation drift": "inter_engine_correlation_drift",
    "correlation drift detection": "inter_engine_correlation_drift",
    "correlation drift analysis": "inter_engine_correlation_drift",

    # Seasonal Adjustment in Drift Detection
    "seasonal adjustment": "seasonal_adjustment_drift_detection",
    "seasonal adjustment drift detection": "seasonal_adjustment_drift_detection",
    "seasonal drift detection": "seasonal_adjustment_drift_detection",
    "seasonal adjustment detection": "seasonal_adjustment_drift_detection",
    "seasonal adjustment analysis": "seasonal_adjustment_drift_detection",
    "seasonal adjustment drift": "seasonal_adjustment_drift_detection",
    "seasonal adjustment correction": "seasonal_adjustment_drift_detection",
    "seasonal adjustment algorithm": "seasonal_adjustment_drift_detection",

    # Drift Attribution Analysis
    "drift attribution": "drift_attribution_analysis",
    "drift attribution analysis": "drift_attribution_analysis",
    "drift attribution detector": "drift_attribution_analysis",
    "drift attribution test": "drift_attribution_analysis",
    "drift attribution classification": "drift_attribution_analysis",
    "drift attribution taxonomy": "drift_attribution_analysis",
    "drift attribution types": "drift_attribution_analysis",
    "drift attribution categories": "drift_attribution_analysis",
    "drift attribution root cause": "drift_attribution_analysis",

    # Drift Severity Classification
    "drift severity": "drift_severity_classification",
    "drift severity classification": "drift_severity_classification",
    "drift severity analysis": "drift_severity_classification",
    "drift severity detector": "drift_severity_classification",
    "drift severity test": "drift_severity_classification",
    "drift severity taxonomy": "drift_severity_classification",
    "drift severity types": "drift_severity_classification",
    "drift severity categories": "drift_severity_classification",
    "drift severity alert": "drift_severity_classification",

    # Automated Recalibration Triggers
    "automated recalibration": "automated_recalibration_triggers",
    "automated recalibration triggers": "automated_recalibration_triggers",
    "recalibration triggers": "automated_recalibration_triggers",
    "auto recalibration": "automated_recalibration_triggers",
    "auto recalibration triggers": "automated_recalibration_triggers",
    "recalibration automation": "automated_recalibration_triggers",
    "recalibration trigger": "automated_recalibration_triggers",
    "recalibration auto": "automated_recalibration_triggers",
    "recalibration automated": "automated_recalibration_triggers",

    # Drift Reporting Protocols
    "drift reporting": "drift_reporting_protocols",
    "drift reporting protocols": "drift_reporting_protocols",
    "drift reporting protocol": "drift_reporting_protocols",
    "drift report": "drift_reporting_protocols",
    "drift reports": "drift_reporting_protocols",
    "drift reporting analysis": "drift_reporting_protocols",
    "drift reporting taxonomy": "drift_reporting_protocols",
    "drift reporting classification": "drift_reporting_protocols",
    "drift reporting alert": "drift_reporting_protocols",

    # Historical Baseline Comparison
    "historical baseline": "historical_baseline_comparison",
    "historical baseline comparison": "historical_baseline_comparison",
    "baseline comparison": "historical_baseline_comparison",
    "historical comparison": "historical_baseline_comparison",
    "baseline comparison analysis": "historical_baseline_comparison",
    "historical baseline analysis": "historical_baseline_comparison",
    "historical baseline detector": "historical_baseline_comparison",
    "historical baseline test": "historical_baseline_comparison",

    # Multivariate Drift Detection
    "multivariate drift": "multivariate_drift_detection",
    "multivariate drift detection": "multivariate_drift_detection",
    "multivariate detection": "multivariate_drift_detection",
    "multivariate drift analysis": "multivariate_drift_detection",
    "multivariate drift detector": "multivariate_drift_detection",
    "multivariate drift test": "multivariate_drift_detection",
    "multivariate drift alert": "multivariate_drift_detection",
    "multivariate drift correction": "multivariate_drift_detection",

    # Concept Drift vs Data Drift
    "concept drift": "concept_drift_vs_data_drift",
    "data drift": "concept_drift_vs_data_drift",
    "concept drift vs data drift": "concept_drift_vs_data_drift",
    "concept drift detection": "concept_drift_vs_data_drift",
    "data drift detection": "concept_drift_vs_data_drift",
    "concept drift analysis": "concept_drift_vs_data_drift",
    "data drift analysis": "concept_drift_vs_data_drift",
    "concept drift taxonomy": "concept_drift_vs_data_drift",
    "data drift taxonomy": "concept_drift_vs_data_drift",

    # KL Divergence Monitoring
    "kl divergence": "kl_divergence_monitoring",
    "kullback-leibler divergence": "kl_divergence_monitoring",
    "kl divergence monitoring": "kl_divergence_monitoring",
    "kl divergence analysis": "kl_divergence_monitoring",
    "kl divergence detector": "kl_divergence_monitoring",
    "kl divergence test": "kl_divergence_monitoring",
    "kl divergence drift": "kl_divergence_monitoring",
    "kl divergence alert": "kl_divergence_monitoring",
    "kl divergence threshold": "kl_divergence_monitoring",

    # Kolmogorov-Smirnov Test for Drift
    "kolmogorov-smirnov": "kolmogorov_smirnov_test_drift",
    "kolmogorov-smirnov test": "kolmogorov_smirnov_test_drift",
    "ks test": "kolmogorov_smirnov_test_drift",
    "kolmogorov smirnov test": "kolmogorov_smirnov_test_drift",
    "ks drift test": "kolmogorov_smirnov_test_drift",
    "ks drift": "kolmogorov_smirnov_test_drift",
    "kolmogorov-smirnov drift": "kolmogorov_smirnov_test_drift",
    "kolmogorov smirnov drift": "kolmogorov_smirnov_test_drift",
    "ks test drift": "kolmogorov_smirnov_test_drift",

    # Drift Alert Thresholds
    "drift alert": "drift_alert_thresholds",
    "drift alert thresholds": "drift_alert_thresholds",
    "drift threshold": "drift_alert_thresholds",
    "drift thresholds": "drift_alert_thresholds",
    "drift alert threshold": "drift_alert_thresholds",
    "drift alert analysis": "drift_alert_thresholds",
    "drift alert detector": "drift_alert_thresholds",
    "drift alert test": "drift_alert_thresholds",
    "drift alert taxonomy": "drift_alert_thresholds",

    # Drift Root Cause Analysis
    "drift root cause": "drift_root_cause_analysis",
    "drift root cause analysis": "drift_root_cause_analysis",
    "drift root cause detector": "drift_root_cause_analysis",
    "drift root cause test": "drift_root_cause_analysis",
    "drift root cause classification": "drift_root_cause_analysis",
    "drift root cause taxonomy": "drift_root_cause_analysis",
    "drift root cause types": "drift_root_cause_analysis",
    "drift root cause categories": "drift_root_cause_analysis",
    "drift root cause alert": "drift_root_cause_analysis",

    # Drift Correction Strategies
    "drift correction": "drift_correction_strategies",
    "drift correction strategies": "drift_correction_strategies",
    "drift correction strategy": "drift_correction_strategies",
    "drift correction analysis": "drift_correction_strategies",
    "drift correction detector": "drift_correction_strategies",
    "drift correction test": "drift_correction_strategies",
    "drift correction taxonomy": "drift_correction_strategies",
    "drift correction classification": "drift_correction_strategies",
    "drift correction alert": "drift_correction_strategies",

    # Drift Watcher Baseline Comparison
    "drift watcher": "drift_watcher_baseline_comparison",
    "drift watcher baseline": "drift_watcher_baseline_comparison",
    "drift watcher baseline comparison": "drift_watcher_baseline_comparison",
    "drift watcher comparison": "drift_watcher_baseline_comparison",
    "drift watcher analysis": "drift_watcher_baseline_comparison",
    "drift watcher detector": "drift_watcher_baseline_comparison",
    "drift watcher test": "drift_watcher_baseline_comparison",
    "drift watcher taxonomy": "drift_watcher_baseline_comparison",

    # Epistemic Gap Detection
    "epistemic gap": "epistemic_gap_detection",
    "epistemic gap detection": "epistemic_gap_detection",
    "epistemic gap analysis": "epistemic_gap_detection",
    "epistemic gap detector": "epistemic_gap_detection",
    "epistemic gap test": "epistemic_gap_detection",
    "epistemic gap taxonomy": "epistemic_gap_detection",
    "epistemic gap classification": "epistemic_gap_detection",
    "epistemic gap alert": "epistemic_gap_detection",

    # Fact Fragility Scoring
    "fact fragility": "fact_fragility_scoring",
    "fact fragility scoring": "fact_fragility_scoring",
    "fact fragility score": "fact_fragility_scoring",
    "fact fragility analysis": "fact_fragility_scoring",
    "fact fragility detector": "fact_fragility_scoring",
    "fact fragility test": "fact_fragility_scoring",
    "fact fragility taxonomy": "fact_fragility_scoring",
    "fact fragility classification": "fact_fragility_scoring",

    # Zoned Analysis for Calibration Drift
    "zoned analysis": "zoned_analysis_calibration_drift",
    "zoned analysis calibration drift": "zoned_analysis_calibration_drift",
    "zoned calibration drift": "zoned_analysis_calibration_drift",
    "zoned analysis drift": "zoned_analysis_calibration_drift",
    "zoned analysis detector": "zoned_analysis_calibration_drift",
    "zoned analysis test": "zoned_analysis_calibration_drift",
    "zoned analysis taxonomy": "zoned_analysis_calibration_drift",
    "zoned analysis classification": "zoned_analysis_calibration_drift",

    # Three-Layer Response Architecture
    "three-layer response": "three_layer_response_architecture",
    "three-layer response architecture": "three_layer_response_architecture",
    "three layer response": "three_layer_response_architecture",
    "three layer response architecture": "three_layer_response_architecture",
    "three-layer response analysis": "three_layer_response_architecture",
    "three-layer response detector": "three_layer_response_architecture",
    "three-layer response test": "three_layer_response_architecture",
    "three-layer response taxonomy": "three_layer_response_architecture",

    # Multi-Doctrine Decomposition for Deep Analysis
    "multi-doctrine decomposition": "multi_doctrine_decomposition_deep_analysis",
    "multi-doctrine decomposition deep analysis": "multi_doctrine_decomposition_deep_analysis",
    "multi doctrine decomposition": "multi_doctrine_decomposition_deep_analysis",
    "multi doctrine decomposition deep analysis": "multi_doctrine_decomposition_deep_analysis",
    "multi-doctrine decomposition analysis": "multi_doctrine_decomposition_deep_analysis",
    "multi-doctrine decomposition detector": "multi_doctrine_decomposition_deep_analysis",
    "multi-doctrine decomposition test": "multi_doctrine_decomposition_deep_analysis",
    "multi-doctrine decomposition taxonomy": "multi_doctrine_decomposition_deep_analysis",

    # Coverage Map Construction
    "coverage map": "coverage_map_construction",
    "coverage map construction": "coverage_map_construction",
    "coverage map analysis": "coverage_map_construction",
    "coverage map detector": "coverage_map_construction",
    "coverage map test": "coverage_map_construction",
    "coverage map taxonomy": "coverage_map_construction",
    "coverage map classification": "coverage_map_construction",

    # Audit Trail Logging for Drift Detection
    "audit trail": "audit_trail_logging_drift_detection",
    "audit trail logging": "audit_trail_logging_drift_detection",
    "audit trail logging drift detection": "audit_trail_logging_drift_detection",
    "audit trail drift detection": "audit_trail_logging_drift_detection",
    "audit trail analysis": "audit_trail_logging_drift_detection",
    "audit trail detector": "audit_trail_logging_drift_detection",
    "audit trail test": "audit_trail_logging_drift_detection",
    "audit trail taxonomy": "audit_trail_logging_drift_detection",

    # Deep Analysis Composite
    "deep analysis": "deep_analysis_composite",
    "deep analysis composite": "deep_analysis_composite",
    "deep analysis detector": "deep_analysis_composite",
    "deep analysis test": "deep_analysis_composite",
    "deep analysis taxonomy": "deep_analysis_composite",
    "deep analysis classification": "deep_analysis_composite",
    "deep analysis alert": "deep_analysis_composite",

    # Misspellings, abbreviations, synonyms, related terms
    "statistical process control charts": "statistical_process_control_charts",
    "cusum change point detection": "cusum_change_point_detection",
    "ewma smoothing for drift detection": "ewma_smoothing_drift_detection",
    "shewhart control limits": "shewhart_control_limits",
    "calibration drift taxonomy": "calibration_drift_taxonomy",
    "confidence distribution monitoring": "confidence_distribution_monitoring",
    "inter engine correlation drift": "inter_engine_correlation_drift",
    "seasonal adjustment in drift detection": "seasonal_adjustment_drift_detection",
    "drift attribution analysis": "drift_attribution_analysis",
    "drift severity classification": "drift_severity_classification",
    "automated recalibration triggers": "automated_recalibration_triggers",
    "drift reporting protocols": "drift_reporting_protocols",
    "historical baseline comparison": "historical_baseline_comparison",
    "multivariate drift detection": "multivariate_drift_detection",
    "concept drift vs data drift": "concept_drift_vs_data_drift",
    "kl divergence monitoring": "kl_divergence_monitoring",
    "kolmogorov smirnov test for drift": "kolmogorov_smirnov_test_drift",
    "drift alert thresholds": "drift_alert_thresholds",
    "drift root cause analysis": "drift_root_cause_analysis",
    "drift correction strategies": "drift_correction_strategies",
    "drift watcher baseline comparison": "drift_watcher_baseline_comparison",
    "epistemic gap detection": "epistemic_gap_detection",
    "fact fragility scoring": "fact_fragility_scoring",
    "zoned analysis for calibration drift": "zoned_analysis_calibration_drift",
    "three layer response architecture": "three_layer_response_architecture",
    "multi doctrine decomposition for deep analysis": "multi_doctrine_decomposition_deep_analysis",
    "coverage map construction": "coverage_map_construction",
    "audit trail logging for drift detection": "audit_trail_logging_drift_detection",
    "deep analysis composite": "deep_analysis_composite",

    # Misspellings and abbreviations
    "statistical process control charrts": "statistical_process_control_charts",
    "statistical process control chars": "statistical_process_control_charts",
    "statistical process control chrt": "statistical_process_control_charts",
    "cusum change point detecton": "cusum_change_point_detection",
    "cusum change point detction": "cusum_change_point_detection",
    "ewma smoothing for drift detecton": "ewma_smoothing_drift_detection",
    "ewma smoothing for drift detction": "ewma_smoothing_drift_detection",
    "shewhart control limts": "shewhart_control_limits",
    "shewhart control limt": "shewhart_control_limits",
    "calibration drift taxonmy": "calibration_drift_taxonomy",
    "calibration drift taxonimy": "calibration_drift_taxonomy",
    "confidence distribution monitorng": "confidence_distribution_monitoring",
    "confidence distribution monitroing": "confidence_distribution_monitoring",
    "inter engine correlation drft": "inter_engine_correlation_drift",
    "inter engine correlation drfit": "inter_engine_correlation_drift",
    "seasonal adjustment in drift detecton": "seasonal_adjustment_drift_detection",
    "seasonal adjustment in drift detction": "seasonal_adjustment_drift_detection",
    "drift attribution analysys": "drift_attribution_analysis",
    "drift attribution analisis": "drift_attribution_analysis",
    "drift severity classificaton": "drift_severity_classification",
    "drift severity classfication": "drift_severity_classification",
    "automated recalibration triggrs": "automated_recalibration_triggers",
    "automated recalibration trigerrs": "automated_recalibration_triggers",
    "drift reporting protcols": "drift_reporting_protocols",
    "drift reporting protcols": "drift_reporting_protocols",
    "historical baseline comparson": "historical_baseline_comparison",
    "historical baseline comparision": "historical_baseline_comparison",
    "multivariate drift detecton": "multivariate_drift_detection",
    "multivariate drift detction": "multivariate_drift_detection",
    "concept drift vs data drft": "concept_drift_vs_data_drift",
    "concept drift vs data drfit": "concept_drift_vs_data_drift",
    "kl divergence monitorng": "kl_divergence_monitoring",
    "kl divergence monitroing": "kl_divergence_monitoring",
    "kolmogorov smirnov test for drft": "kolmogorov_smirnov_test_drift",
    "kolmogorov smirnov test for drfit": "kolmogorov_smirnov_test_drift",
    "drift alert threshlds": "drift_alert_thresholds",
    "drift alert threshhold": "drift_alert_thresholds",
    "drift root cause analysys": "drift_root_cause_analysis",
    "drift root cause analisis": "drift_root_cause_analysis",
    "drift correction stratgies": "drift_correction_strategies",
    "drift correction stratgeis": "drift_correction_strategies",
    "drift watcher baseline comparson": "drift_watcher_baseline_comparison",
    "drift watcher baseline comparision": "drift_watcher_baseline_comparison",
    "epistemic gap detecton": "epistemic_gap_detection",
    "epistemic gap detction": "epistemic_gap_detection",
    "fact fragility scorng": "fact_fragility_scoring",
    "fact fragility scroing": "fact_fragility_scoring",
    "zoned analysis for calibration drft": "zoned_analysis_calibration_drift",
    "zoned analysis for calibration drfit": "zoned_analysis_calibration_drift",
    "three layer response archtecture": "three_layer_response_architecture",
    "three layer response architecure": "three_layer_response_architecture",
    "multi doctrine decomposition for deep analysys": "multi_doctrine_decomposition_deep_analysis",
    "multi doctrine decomposition for deep analisis": "multi_doctrine_decomposition_deep_analysis",
    "coverage map constructon": "coverage_map_construction",
    "coverage map constrction": "coverage_map_construction",
    "audit trail logging for drift detecton": "audit_trail_logging_drift_detection",
    "audit trail logging for drift detction": "audit_trail_logging_drift_detection",
    "deep analysis composte": "deep_analysis_composite",
    "deep analysis composte": "deep_analysis_composite",

    # Acronyms and abbreviations
    "spcc": "statistical_process_control_charts",
    "ewma_sdd": "ewma_smoothing_drift_detection",
    "ks": "kolmogorov_smirnov_test_drift",
    "kl": "kl_divergence_monitoring",
    "cpd": "cusum_change_point_detection",
    "rc": "drift_correction_strategies",
    "da": "drift_attribution_analysis",
    "ds": "drift_severity_classification",
    "dr": "drift_reporting_protocols",
    "bc": "historical_baseline_comparison",
    "mv": "multivariate_drift_detection",
    "cd": "concept_drift_vs_data_drift",
    "cdt": "calibration_drift_taxonomy",
    "sd": "seasonal_adjustment_drift_detection",
    "ec": "epistemic_gap_detection",
    "ff": "fact_fragility_scoring",
    "za": "zoned_analysis_calibration_drift",
    "tlr": "three_layer_response_architecture",
    "md": "multi_doctrine_decomposition_deep_analysis",
    "cm": "coverage_map_construction",
    "at": "audit_trail_logging_drift_detection",
    "dac": "deep_analysis_composite",
    "iecd": "inter_engine_correlation_drift",
    "ar": "automated_recalibration_triggers",
    "dwt": "drift_watcher_baseline_comparison",
    "dat": "drift_alert_thresholds",
    "drt": "drift_root_cause_analysis",

    # Related terms
    "process monitoring": "statistical_process_control_charts",
    "change detection": "cusum_change_point_detection",
    "moving average": "ewma_smoothing_drift_detection",
    "control limits": "shewhart_control_limits",
    "calibration taxonomy": "calibration_drift_taxonomy",
    "distribution monitoring": "confidence_distribution_monitoring",
    "correlation monitoring": "inter_engine_correlation_drift",
    "seasonal adjustment": "seasonal_adjustment_drift_detection",
    "attribution analysis": "drift_attribution_analysis",
    "severity classification": "drift_severity_classification",
    "recalibration": "automated_recalibration_triggers",
    "reporting protocols": "drift_reporting_protocols",
    "baseline comparison": "historical_baseline_comparison",
    "multivariate detection": "multivariate_drift_detection",
    "drift detection": "concept_drift_vs_data_drift",
    "divergence monitoring": "kl_divergence_monitoring",
    "ks monitoring": "kolmogorov_smirnov_test_drift",
    "alert thresholds": "drift_alert_thresholds",
    "root cause analysis": "drift_root_cause_analysis",
    "correction strategies": "drift_correction_strategies",
    "watcher baseline": "drift_watcher_baseline_comparison",
    "gap detection": "epistemic_gap_detection",
    "fragility scoring": "fact_fragility_scoring",
    "zoned calibration": "zoned_analysis_calibration_drift",
    "response architecture": "three_layer_response_architecture",
    "doctrine decomposition": "multi_doctrine_decomposition_deep_analysis",
    "coverage map": "coverage_map_construction",
    "audit logging": "audit_trail_logging_drift_detection",
    "deep composite": "deep_analysis_composite",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    concat = "".join(f"{k}:{v};" for k, v in items)
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    hash_val = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (hash_val == _MAP_INTEGRITY_HASH)
    return {
        "status": "OK" if is_valid else "FAIL",
        "entries": actual_count,
        "hash": hash_val,
        "is_valid": is_valid
    }

def _normalize_string(s):
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^a-z0-9 _\-]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    return s

def normalize_term(term: str) -> str:
    t = _normalize_string(term)
    return SEMANTIC_MAP.get(t, t)

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)