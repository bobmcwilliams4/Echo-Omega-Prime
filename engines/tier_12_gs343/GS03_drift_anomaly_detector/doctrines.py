import enum
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Z-Score Based Anomaly Detection",
        keywords=["z-score", "statistical threshold", "standard deviation", "outlier", "normal distribution"],
        conclusion_template="If the observed metric's z-score exceeds the configured threshold, flag as anomaly.",
        reasoning_framework=(
            "1. Collect baseline data for the metric under normal engine operation.\n"
            "2. Calculate mean (μ) and standard deviation (σ) for the baseline.\n"
            "3. For each new observation, compute z = (x - μ) / σ.\n"
            "4. Compare z against the anomaly threshold (typically |z| > 3).\n"
            "5. If threshold exceeded, classify as anomaly; otherwise, consider normal.\n"
            "6. Adjust threshold based on historical false positive/negative rates.\n"
            "7. Document all flagged anomalies for audit and tuning.\n"
            "8. Consider multi-variate z-score extension for correlated metrics.\n"
            "9. Recompute baseline periodically to account for drift.\n"
            "10. Integrate with alerting system for real-time notification."
        ),
        key_factors=[
            "Baseline data quality",
            "Appropriate threshold selection",
            "Metric distribution normality",
            "Update frequency of baseline",
            "False positive/negative tradeoff"
        ],
        primary_authority=[
            "NIST Special Publication 800-94",
            "ISO/IEC 27002:2022",
            "GS03 Engine Technical Manual"
        ],
        burden_holder="Anomaly Detector Module",
        adversary_position="Z-score thresholds may not capture non-Gaussian anomalies.",
        counter_arguments=[
            "Apply robust statistics for non-normal distributions.",
            "Combine with non-parametric methods for coverage."
        ],
        resolution_strategy="Hybridize with IQR or Isolation Forest for non-Gaussian cases.",
        entity_scope="All GS03 engine metrics supporting z-score analysis.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS03-2021-AD-001"
    ),
    DoctrineBlock(
        topic="Interquartile Range (IQR) Outlier Detection",
        keywords=["IQR", "outlier", "boxplot", "non-parametric", "robust statistics"],
        conclusion_template="If a metric value falls outside [Q1-1.5*IQR, Q3+1.5*IQR], classify as outlier.",
        reasoning_framework=(
            "1. Gather historical data for the metric under stable conditions.\n"
            "2. Compute first (Q1) and third (Q3) quartiles.\n"
            "3. Calculate IQR = Q3 - Q1.\n"
            "4. Define lower bound = Q1 - 1.5 * IQR; upper bound = Q3 + 1.5 * IQR.\n"
            "5. Flag any observation outside these bounds as an outlier.\n"
            "6. Periodically update quartiles to adapt to drift.\n"
            "7. Use for metrics with skewed or unknown distributions.\n"
            "8. Aggregate outlier counts for trend analysis.\n"
            "9. Integrate with alerting and reporting subsystems."
        ),
        key_factors=[
            "Stability of historical data",
            "Quartile calculation accuracy",
            "Frequency of IQR recalculation",
            "Handling of extreme values",
            "Integration with other anomaly detectors"
        ],
        primary_authority=[
            "Tukey, J.W. (1977). Exploratory Data Analysis.",
            "GS03 Engine Analytics Specification"
        ],
        burden_holder="Anomaly Detector Module",
        adversary_position="IQR method may miss context-dependent anomalies.",
        counter_arguments=[
            "Combine with contextual anomaly detection.",
            "Adjust IQR multiplier for domain specificity."
        ],
        resolution_strategy="Use adaptive IQR multiplier based on validation results.",
        entity_scope="Metrics with non-Gaussian or unknown distributions.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS03-2021-AD-002"
    ),
    DoctrineBlock(
        topic="Isolation Forest for Anomaly Detection",
        keywords=["isolation forest", "ensemble", "unsupervised learning", "tree-based", "high-dimensional"],
        conclusion_template="If the isolation score is below the anomaly threshold, label as anomaly.",
        reasoning_framework=(
            "1. Train Isolation Forest on historical engine metrics.\n"
            "2. For each new observation, compute its isolation score.\n"
            "3. Compare score to the pre-set anomaly threshold.\n"
            "4. If below threshold, classify as anomaly.\n"
            "5. Periodically retrain model to capture drift.\n"
            "6. Validate model on labeled anomaly data.\n"
            "7. Tune number of trees and subsample size for optimal performance.\n"
            "8. Document model parameters and retraining schedule.\n"
            "9. Integrate with GS03 alerting pipeline."
        ),
        key_factors=[
            "Quality and representativeness of training data",
            "Threshold calibration",
            "Retraining frequency",
            "Model validation metrics",
            "Interpretability of anomaly scores"
        ],
        primary_authority=[
            "Liu, F.T., Ting, K.M., Zhou, Z.-H. (2008). Isolation Forest.",
            "GS03 Engine ML Integration Guide"
        ],
        burden_holder="ML Model Maintainer",
        adversary_position="Model drift may cause increased false negatives.",
        counter_arguments=[
            "Monitor model performance metrics.",
            "Schedule regular retraining with recent data."
        ],
        resolution_strategy="Implement automated model drift detection and retraining.",
        entity_scope="All high-dimensional engine metrics.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS03-2021-ML-001"
    ),
    DoctrineBlock(
        topic="Engine Performance Baseline Tracking",
        keywords=["baseline", "performance", "trend", "reference", "normal operation"],
        conclusion_template="If current performance deviates from baseline by more than X%, flag for review.",
        reasoning_framework=(
            "1. Establish baseline performance metrics during certified normal operation.\n"
            "2. Store baseline values and update periodically.\n"
            "3. Continuously monitor current metrics against baseline.\n"
            "4. Define deviation thresholds for each metric.\n"
            "5. If deviation exceeds threshold, trigger anomaly workflow.\n"
            "6. Review baseline update schedule for seasonality and drift.\n"
            "7. Document baseline calculation and update procedures.\n"
            "8. Communicate baseline changes to stakeholders."
        ),
        key_factors=[
            "Baseline calculation period",
            "Threshold selection",
            "Update frequency",
            "Metric selection",
            "Stakeholder communication"
        ],
        primary_authority=[
            "GS03 Engine Operations Manual",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Performance Monitoring Team",
        adversary_position="Static baselines may not adapt to gradual changes.",
        counter_arguments=[
            "Implement rolling or adaptive baselines.",
            "Use seasonality-aware baselining."
        ],
        resolution_strategy="Adopt dynamic baseline recalibration policies.",
        entity_scope="All core engine performance metrics.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GS03-2021-PERF-001"
    ),
    DoctrineBlock(
        topic="Response Time Drift Detection",
        keywords=["response time", "latency", "drift", "trend", "SLA"],
        conclusion_template="If response time mean or variance drifts beyond control limits, trigger anomaly alert.",
        reasoning_framework=(
            "1. Monitor response time metrics in real-time.\n"
            "2. Calculate rolling mean and variance.\n"
            "3. Establish control limits based on historical data and SLAs.\n"
            "4. Detect significant drift using statistical process control (SPC) methods.\n"
            "5. If drift exceeds control limits, flag as anomaly.\n"
            "6. Correlate with deployment or configuration events.\n"
            "7. Document all drift incidents for root cause analysis."
        ),
        key_factors=[
            "Control limit calculation",
            "Rolling window size",
            "SLA definitions",
            "Correlation with external events",
            "Incident documentation"
        ],
        primary_authority=[
            "Montgomery, D.C. (2012). Introduction to Statistical Quality Control.",
            "GS03 Engine SLA Documentation"
        ],
        burden_holder="SRE Team",
        adversary_position="SPC may not detect all forms of drift.",
        counter_arguments=[
            "Complement with machine learning drift detectors.",
            "Increase sensitivity for critical services."
        ],
        resolution_strategy="Hybrid SPC and ML-based drift detection.",
        entity_scope="All response time metrics.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GS03-2021-RT-001"
    ),
    DoctrineBlock(
        topic="Error Rate Drift Analysis",
        keywords=["error rate", "drift", "change detection", "statistical process control", "alerting"],
        conclusion_template="If error rate exceeds baseline by Y% or more, escalate for investigation.",
        reasoning_framework=(
            "1. Establish error rate baseline under normal operation.\n"
            "2. Continuously monitor error rate in production.\n"
            "3. Use change point detection algorithms to identify drift.\n"
            "4. Set escalation thresholds based on business impact.\n"
            "5. If drift detected, trigger alert and initiate investigation.\n"
            "6. Log all drift incidents for trend analysis and reporting."
        ),
        key_factors=[
            "Baseline calculation",
            "Change point detection method",
            "Escalation threshold",
            "Incident logging",
            "Business impact assessment"
        ],
        primary_authority=[
            "GS03 Engine Error Handling Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Baseline may be skewed by rare events.",
        counter_arguments=[
            "Exclude outlier periods from baseline.",
            "Apply robust statistics for baseline calculation."
        ],
        resolution_strategy="Regularly review and update baseline periods.",
        entity_scope="All error rate metrics.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="GS03-2021-ERR-001"
    ),
    DoctrineBlock(
        topic="Confidence Score Distribution Shift",
        keywords=["confidence score", "distribution shift", "model drift", "prediction quality", "monitoring"],
        conclusion_template="If confidence score distribution diverges significantly from baseline, investigate model drift.",
        reasoning_framework=(
            "1. Record confidence scores for all model predictions.\n"
            "2. Establish baseline distribution using historical data.\n"
            "3. Monitor real-time distribution using statistical tests (e.g., KS test).\n"
            "4. If significant divergence detected, flag for model drift investigation.\n"
            "5. Document all distribution shifts and corrective actions."
        ),
        key_factors=[
            "Baseline distribution accuracy",
            "Statistical test selection",
            "Divergence threshold",
            "Model retraining schedule",
            "Documentation of shifts"
        ],
        primary_authority=[
            "GS03 ML Monitoring Guidelines",
            "ISO/IEC 22989:2022"
        ],
        burden_holder="ML Operations Team",
        adversary_position="Statistical tests may be sensitive to sample size.",
        counter_arguments=[
            "Apply bootstrapping for small samples.",
            "Aggregate over longer periods if needed."
        ],
        resolution_strategy="Tune test parameters and aggregation windows.",
        entity_scope="All ML model outputs.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="GS03-2021-ML-002"
    ),
    DoctrineBlock(
        topic="Output Quality Metric Drift",
        keywords=["output quality", "metric drift", "quality assurance", "trend analysis", "monitoring"],
        conclusion_template="If output quality metrics trend downward or drift from baseline, initiate QA review.",
        reasoning_framework=(
            "1. Define output quality metrics relevant to engine operation.\n"
            "2. Establish baseline values and acceptable ranges.\n"
            "3. Continuously monitor for downward trends or significant drift.\n"
            "4. Use statistical trend analysis to detect issues early.\n"
            "5. Initiate QA review if drift is persistent or severe.\n"
            "6. Document all findings and corrective actions."
        ),
        key_factors=[
            "Metric selection",
            "Baseline accuracy",
            "Trend analysis method",
            "QA review process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Quality Assurance Manual",
            "ISO 9001:2015"
        ],
        burden_holder="Quality Assurance Team",
        adversary_position="Some quality issues may not manifest as metric drift.",
        counter_arguments=[
            "Supplement with manual QA checks.",
            "Incorporate user feedback."
        ],
        resolution_strategy="Hybrid automated and manual QA processes.",
        entity_scope="All output quality metrics.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-QA-001"
    ),
    DoctrineBlock(
        topic="Behavioral Fingerprinting per Engine",
        keywords=["behavioral fingerprinting", "engine identity", "pattern recognition", "anomaly detection", "profiling"],
        conclusion_template="If current behavior deviates from established fingerprint, flag as potential anomaly.",
        reasoning_framework=(
            "1. Profile engine behavior across key metrics during normal operation.\n"
            "2. Create a behavioral fingerprint for each engine instance.\n"
            "3. Continuously compare real-time behavior to fingerprint.\n"
            "4. Flag significant deviations for investigation.\n"
            "5. Update fingerprints periodically to account for changes.\n"
            "6. Integrate with anomaly detection and alerting systems."
        ),
        key_factors=[
            "Fingerprint accuracy",
            "Deviation threshold",
            "Update frequency",
            "Metric selection",
            "Integration with detection systems"
        ],
        primary_authority=[
            "GS03 Security Operations Guide",
            "NIST SP 800-53"
        ],
        burden_holder="Security Operations Team",
        adversary_position="Fingerprints may become outdated with engine upgrades.",
        counter_arguments=[
            "Automate fingerprint updates post-upgrade.",
            "Validate fingerprints after major changes."
        ],
        resolution_strategy="Implement automated fingerprint refresh procedures.",
        entity_scope="All GS03 engine instances.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-SEC-001"
    ),
    DoctrineBlock(
        topic="Seasonal Pattern Accounting",
        keywords=["seasonality", "pattern recognition", "time series", "trend", "baseline adjustment"],
        conclusion_template="Adjust anomaly thresholds to account for expected seasonal patterns.",
        reasoning_framework=(
            "1. Analyze historical data for seasonal trends (daily, weekly, monthly).\n"
            "2. Model seasonality using time series decomposition.\n"
            "3. Adjust anomaly detection thresholds to align with expected seasonal variation.\n"
            "4. Continuously validate and update seasonal models.\n"
            "5. Document all threshold adjustments and rationale."
        ),
        key_factors=[
            "Seasonality model accuracy",
            "Threshold adjustment method",
            "Model validation frequency",
            "Documentation",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Hyndman, R.J., Athanasopoulos, G. (2018). Forecasting: Principles and Practice.",
            "GS03 Analytics Handbook"
        ],
        burden_holder="Analytics Team",
        adversary_position="Unexpected events may disrupt seasonal patterns.",
        counter_arguments=[
            "Monitor for anomalies outside expected seasonality.",
            "Recalibrate models after major events."
        ],
        resolution_strategy="Rapid model recalibration post-event.",
        entity_scope="All time series metrics with seasonality.",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-TS-001"
    ),
    DoctrineBlock(
        topic="Alert Fatigue Prevention: Minimum Severity Thresholds",
        keywords=["alert fatigue", "severity threshold", "alerting", "incident response", "triage"],
        conclusion_template="Suppress alerts below the minimum severity threshold to reduce fatigue.",
        reasoning_framework=(
            "1. Define severity levels for all alert types.\n"
            "2. Set minimum severity threshold based on incident response capacity.\n"
            "3. Suppress alerts below threshold from reaching on-call staff.\n"
            "4. Periodically review and adjust thresholds based on feedback.\n"
            "5. Document all threshold changes and rationale."
        ),
        key_factors=[
            "Severity level definitions",
            "Threshold calibration",
            "Incident response capacity",
            "Feedback from on-call staff",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Incident Response Playbook",
            "SRE Book (Google, 2016)"
        ],
        burden_holder="Alerting System Owner",
        adversary_position="Suppressed alerts may hide early warning signs.",
        counter_arguments=[
            "Log suppressed alerts for offline review.",
            "Enable override for critical periods."
        ],
        resolution_strategy="Implement suppressed alert review dashboard.",
        entity_scope="All alerting channels.",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ALERT-001"
    ),
    DoctrineBlock(
        topic="Anomaly Correlation Across Engines",
        keywords=["anomaly correlation", "multi-engine", "cross-correlation", "incident analysis", "root cause"],
        conclusion_template="If correlated anomalies are detected across engines, escalate as potential systemic issue.",
        reasoning_framework=(
            "1. Aggregate anomaly data from all GS03 engine instances.\n"
            "2. Apply cross-correlation analysis to identify temporal or pattern-based links.\n"
            "3. If significant correlation detected, escalate for systemic investigation.\n"
            "4. Document all correlated incidents and findings.\n"
            "5. Use findings to improve detection and prevention strategies."
        ),
        key_factors=[
            "Data aggregation accuracy",
            "Correlation analysis method",
            "Escalation criteria",
            "Documentation",
            "Feedback into prevention strategies"
        ],
        primary_authority=[
            "GS03 Incident Analysis Guidelines",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Analysis Team",
        adversary_position="Correlation may be coincidental, not causal.",
        counter_arguments=[
            "Investigate for common root causes.",
            "Apply causality analysis where possible."
        ],
        resolution_strategy="Combine correlation with root cause analysis.",
        entity_scope="All GS03 engine instances.",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-INC-001"
    ),
    DoctrineBlock(
        topic="Root Cause Inference from Anomaly Patterns",
        keywords=["root cause", "anomaly pattern", "causal inference", "incident analysis", "diagnostics"],
        conclusion_template="If recurring anomaly patterns are observed, infer likely root causes for remediation.",
        reasoning_framework=(
            "1. Catalog anomaly patterns and associated incidents.\n"
            "2. Apply causal inference techniques to link patterns to root causes.\n"
            "3. Validate inferences with domain experts.\n"
            "4. Document root cause hypotheses and supporting evidence.\n"
            "5. Use findings to guide remediation and prevention."
        ),
        key_factors=[
            "Pattern cataloging",
            "Causal inference method",
            "Expert validation",
            "Documentation",
            "Remediation effectiveness"
        ],
        primary_authority=[
            "GS03 Diagnostics Manual",
            "Pearl, J. (2009). Causality."
        ],
        burden_holder="Diagnostics Team",
        adversary_position="Correlation does not imply causation.",
        counter_arguments=[
            "Seek converging evidence from multiple sources.",
            "Conduct controlled tests where feasible."
        ],
        resolution_strategy="Iterative validation and controlled testing.",
        entity_scope="All anomaly patterns.",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-RC-001"
    ),
    DoctrineBlock(
        topic="Anomaly Severity Classification",
        keywords=["anomaly severity", "classification", "impact assessment", "alerting", "triage"],
        conclusion_template="Classify anomalies by severity to prioritize response and resource allocation.",
        reasoning_framework=(
            "1. Define severity levels based on business and technical impact.\n"
            "2. Assign severity to each detected anomaly using predefined criteria.\n"
            "3. Prioritize incident response based on severity.\n"
            "4. Review and update severity definitions as needed.\n"
            "5. Document all severity assignments and rationale."
        ),
        key_factors=[
            "Severity level definitions",
            "Classification criteria",
            "Impact assessment",
            "Review process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Incident Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Manager",
        adversary_position="Severity may be misclassified due to incomplete information.",
        counter_arguments=[
            "Enable post-incident severity reassessment.",
            "Incorporate feedback from responders."
        ],
        resolution_strategy="Iterative severity review and adjustment.",
        entity_scope="All detected anomalies.",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-INC-002"
    ),
    DoctrineBlock(
        topic="Trending vs Sudden Anomalies",
        keywords=["trending anomaly", "sudden anomaly", "change detection", "pattern recognition", "alerting"],
        conclusion_template="Distinguish between trending and sudden anomalies to tailor response strategies.",
        reasoning_framework=(
            "1. Analyze anomaly time series for rate of change.\n"
            "2. Classify anomalies as trending (gradual) or sudden (abrupt).\n"
            "3. Apply different alerting and remediation strategies based on type.\n"
            "4. Document classification and response outcomes.\n"
            "5. Review classification accuracy periodically."
        ),
        key_factors=[
            "Rate of change calculation",
            "Classification criteria",
            "Response strategy selection",
            "Documentation",
            "Review process"
        ],
        primary_authority=[
            "GS03 Anomaly Response Handbook",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Anomaly Detection System",
        adversary_position="Some anomalies may not fit neatly into either category.",
        counter_arguments=[
            "Allow for hybrid or unclassified states.",
            "Refine classification with feedback."
        ],
        resolution_strategy="Iterative refinement of classification logic.",
        entity_scope="All anomaly time series.",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ANOM-001"
    ),
    DoctrineBlock(
        topic="Phantom Load Detection",
        keywords=["phantom load", "resource usage", "idle consumption", "anomaly detection", "efficiency"],
        conclusion_template="If resource usage persists during idle periods, flag as phantom load anomaly.",
        reasoning_framework=(
            "1. Define expected resource usage profiles for idle periods.\n"
            "2. Monitor actual usage during these periods.\n"
            "3. If usage exceeds expected thresholds, classify as phantom load.\n"
            "4. Investigate sources and remediate as needed.\n"
            "5. Document all phantom load incidents."
        ),
        key_factors=[
            "Idle period definition",
            "Expected usage thresholds",
            "Monitoring accuracy",
            "Remediation process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Resource Efficiency Manual",
            "ISO 50001:2018"
        ],
        burden_holder="Resource Monitoring Team",
        adversary_position="Some background processes may justify usage.",
        counter_arguments=[
            "Correlate with scheduled maintenance or updates.",
            "Refine idle period definitions."
        ],
        resolution_strategy="Integrate with process scheduling data.",
        entity_scope="All resource usage metrics.",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-RES-001"
    ),
    DoctrineBlock(
        topic="Resource Leak Pattern Detection",
        keywords=["resource leak", "pattern detection", "memory leak", "handle leak", "anomaly detection"],
        conclusion_template="If resource usage exhibits unbounded growth, flag as potential leak.",
        reasoning_framework=(
            "1. Monitor resource usage (memory, handles, file descriptors) over time.\n"
            "2. Identify patterns of unbounded or linear growth.\n"
            "3. Correlate with deployment or configuration changes.\n"
            "4. Flag as potential leak if growth persists beyond expected bounds.\n"
            "5. Document all leak incidents and remediation steps."
        ),
        key_factors=[
            "Growth pattern identification",
            "Correlation with changes",
            "Expected usage bounds",
            "Remediation process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Resource Management Policy",
            "ISO/IEC 14764:2006"
        ],
        burden_holder="Operations Team",
        adversary_position="Some growth may be justified by workload changes.",
        counter_arguments=[
            "Adjust expected bounds for workload shifts.",
            "Validate with application owners."
        ],
        resolution_strategy="Integrate workload awareness into detection logic.",
        entity_scope="All resource usage metrics.",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-RES-002"
    ),
    DoctrineBlock(
        topic="Memory Growth Analysis",
        keywords=["memory growth", "trend analysis", "anomaly detection", "resource monitoring", "leak detection"],
        conclusion_template="If memory usage grows abnormally over time, escalate for investigation.",
        reasoning_framework=(
            "1. Track memory usage metrics continuously.\n"
            "2. Analyze for abnormal growth patterns (linear, exponential).\n"
            "3. Compare against expected workload-driven growth.\n"
            "4. If abnormal, escalate for investigation and remediation.\n"
            "5. Document all findings and actions taken."
        ),
        key_factors=[
            "Growth pattern analysis",
            "Expected workload profiles",
            "Escalation criteria",
            "Remediation process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Memory Management Guidelines",
            "ISO/IEC 14764:2006"
        ],
        burden_holder="Memory Monitoring Team",
        adversary_position="Some memory growth may be transient or workload-driven.",
        counter_arguments=[
            "Correlate with workload metrics.",
            "Allow for short-term spikes."
        ],
        resolution_strategy="Implement workload-aware memory analysis.",
        entity_scope="All memory usage metrics.",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-MEM-001"
    ),
    DoctrineBlock(
        topic="Connection Pool Drift Detection",
        keywords=["connection pool", "drift detection", "resource management", "database connections", "anomaly"],
        conclusion_template="If connection pool usage drifts from baseline, trigger resource management review.",
        reasoning_framework=(
            "1. Monitor connection pool usage metrics over time.\n"
            "2. Establish baseline usage patterns.\n"
            "3. Detect significant drift using statistical or ML methods.\n"
            "4. If drift detected, trigger review and remediation.\n"
            "5. Document all drift incidents and outcomes."
        ),
        key_factors=[
            "Baseline calculation",
            "Drift detection method",
            "Review process",
            "Remediation actions",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Database Integration Guide",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Database Operations Team",
        adversary_position="Some drift may be justified by changing workloads.",
        counter_arguments=[
            "Correlate with workload and deployment events.",
            "Adjust baselines as needed."
        ],
        resolution_strategy="Integrate workload context into drift detection.",
        entity_scope="All connection pool metrics.",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-DB-001"
    ),
    DoctrineBlock(
        topic="Cache Hit Rate Degradation",
        keywords=["cache hit rate", "degradation", "performance", "trend analysis", "anomaly detection"],
        conclusion_template="If cache hit rate drops below baseline, investigate for performance issues.",
        reasoning_framework=(
            "1. Monitor cache hit rate continuously.\n"
            "2. Establish baseline hit rate under normal operation.\n"
            "3. Detect significant drops below baseline.\n"
            "4. Investigate causes (e.g., cache eviction, configuration changes).\n"
            "5. Document all incidents and corrective actions."
        ),
        key_factors=[
            "Baseline calculation",
            "Drop detection threshold",
            "Cause investigation",
            "Corrective actions",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Caching Best Practices",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Performance Engineering Team",
        adversary_position="Some drops may be transient or workload-driven.",
        counter_arguments=[
            "Correlate with workload and cache configuration.",
            "Allow for short-term fluctuations."
        ],
        resolution_strategy="Implement context-aware cache monitoring.",
        entity_scope="All cache hit rate metrics.",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-CACHE-001"
    ),
    DoctrineBlock(
        topic="API Latency Distribution Shift",
        keywords=["API latency", "distribution shift", "performance", "drift detection", "alerting"],
        conclusion_template="If API latency distribution shifts significantly, trigger performance investigation.",
        reasoning_framework=(
            "1. Track API latency metrics and distribution over time.\n"
            "2. Establish baseline latency distribution.\n"
            "3. Use statistical tests (e.g., KS test) to detect significant shifts.\n"
            "4. If shift detected, trigger investigation and alerting.\n"
            "5. Document all distribution shifts and actions taken."
        ),
        key_factors=[
            "Baseline distribution calculation",
            "Shift detection method",
            "Investigation process",
            "Alerting integration",
            "Documentation"
        ],
        primary_authority=[
            "GS03 API Performance Guide",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="API Monitoring Team",
        adversary_position="Some shifts may be workload-driven or expected.",
        counter_arguments=[
            "Correlate with deployment and workload events.",
            "Update baselines as needed."
        ],
        resolution_strategy="Integrate event context into shift detection.",
        entity_scope="All API latency metrics.",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-API-001"
    ),
    DoctrineBlock(
        topic="Data Quality Drift Indicators",
        keywords=["data quality", "drift", "indicator", "monitoring", "anomaly detection"],
        conclusion_template="If data quality indicators drift from baseline, escalate for data engineering review.",
        reasoning_framework=(
            "1. Define key data quality indicators (completeness, accuracy, consistency).\n"
            "2. Establish baseline values for each indicator.\n"
            "3. Monitor for significant drift using statistical methods.\n"
            "4. If drift detected, escalate for review and remediation.\n"
            "5. Document all drift incidents and outcomes."
        ),
        key_factors=[
            "Indicator selection",
            "Baseline calculation",
            "Drift detection method",
            "Review process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Data Management Policy",
            "ISO/IEC 25012:2008"
        ],
        burden_holder="Data Engineering Team",
        adversary_position="Some drift may be due to upstream changes.",
        counter_arguments=[
            "Correlate with upstream data source events.",
            "Update baselines as needed."
        ],
        resolution_strategy="Implement upstream event awareness in monitoring.",
        entity_scope="All data quality indicators.",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-DATA-001"
    ),
    # Additional doctrines for coverage and depth (20+ more for 40+ total)
    DoctrineBlock(
        topic="Adaptive Thresholding for Anomaly Detection",
        keywords=["adaptive threshold", "dynamic threshold", "anomaly detection", "self-tuning", "baseline"],
        conclusion_template="If adaptive threshold is exceeded, flag as anomaly; thresholds adjust with new data.",
        reasoning_framework=(
            "1. Implement adaptive algorithms to set thresholds based on recent data.\n"
            "2. Continuously update thresholds as new data arrives.\n"
            "3. Compare observed values to current adaptive threshold.\n"
            "4. Flag anomalies when thresholds are breached.\n"
            "5. Periodically review adaptation logic for effectiveness."
        ),
        key_factors=[
            "Adaptation algorithm selection",
            "Update frequency",
            "Effectiveness review",
            "Integration with alerting",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Anomaly Detection System",
        adversary_position="Over-adaptation may mask true anomalies.",
        counter_arguments=[
            "Set adaptation bounds.",
            "Review adaptation logic regularly."
        ],
        resolution_strategy="Implement adaptation bounds and periodic reviews.",
        entity_scope="All metrics with dynamic behavior.",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ADAPT-001"
    ),
    DoctrineBlock(
        topic="Multi-Metric Anomaly Aggregation",
        keywords=["multi-metric", "aggregation", "anomaly detection", "correlation", "composite alert"],
        conclusion_template="Aggregate anomalies across metrics to detect compound or systemic issues.",
        reasoning_framework=(
            "1. Monitor multiple related metrics simultaneously.\n"
            "2. Aggregate anomaly signals to identify compound events.\n"
            "3. Correlate aggregated anomalies for systemic issue detection.\n"
            "4. Escalate composite alerts for cross-team investigation.\n"
            "5. Document aggregation logic and incident outcomes."
        ),
        key_factors=[
            "Metric selection",
            "Aggregation logic",
            "Correlation analysis",
            "Escalation criteria",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Incident Analysis Guidelines",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Analysis Team",
        adversary_position="Aggregation may dilute individual anomaly signals.",
        counter_arguments=[
            "Retain individual anomaly details.",
            "Tune aggregation sensitivity."
        ],
        resolution_strategy="Balance aggregation with individual anomaly reporting.",
        entity_scope="All related engine metrics.",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-MULTI-001"
    ),
    DoctrineBlock(
        topic="Anomaly Suppression During Maintenance Windows",
        keywords=["anomaly suppression", "maintenance window", "alerting", "false positive", "scheduled downtime"],
        conclusion_template="Suppress anomaly alerts during scheduled maintenance to avoid false positives.",
        reasoning_framework=(
            "1. Define maintenance windows in the monitoring system.\n"
            "2. Suppress anomaly alerts during these periods.\n"
            "3. Log suppressed anomalies for post-maintenance review.\n"
            "4. Resume normal alerting after window ends.\n"
            "5. Document all suppressed alerts and rationale."
        ),
        key_factors=[
            "Maintenance window definition",
            "Suppression logic",
            "Post-maintenance review",
            "Alerting resumption",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Operations Manual",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Operations Team",
        adversary_position="Critical anomalies may be missed during maintenance.",
        counter_arguments=[
            "Review suppressed anomalies post-maintenance.",
            "Enable override for critical alerts."
        ],
        resolution_strategy="Implement post-maintenance anomaly review process.",
        entity_scope="All scheduled maintenance periods.",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-MAINT-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection Model Explainability",
        keywords=["explainability", "model transparency", "anomaly detection", "interpretability", "stakeholder trust"],
        conclusion_template="Provide interpretable explanations for detected anomalies to stakeholders.",
        reasoning_framework=(
            "1. Select anomaly detection models with explainable outputs.\n"
            "2. Generate human-readable explanations for each anomaly.\n"
            "3. Provide explanations to stakeholders for trust and validation.\n"
            "4. Document explanation generation process.\n"
            "5. Periodically review explanation quality with users."
        ),
        key_factors=[
            "Model selection",
            "Explanation generation",
            "Stakeholder feedback",
            "Documentation",
            "Review process"
        ],
        primary_authority=[
            "GS03 ML Monitoring Guidelines",
            "EU AI Act (2021)"
        ],
        burden_holder="ML Operations Team",
        adversary_position="Some models may not be inherently explainable.",
        counter_arguments=[
            "Use surrogate models for explanation.",
            "Limit use of black-box models."
        ],
        resolution_strategy="Prioritize explainable models and surrogate explanations.",
        entity_scope="All anomaly detection models.",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ML-EXPL-001"
    ),
    DoctrineBlock(
        topic="Feedback Loop for Anomaly Detection Improvement",
        keywords=["feedback loop", "continuous improvement", "anomaly detection", "user feedback", "model tuning"],
        conclusion_template="Incorporate user feedback to improve anomaly detection accuracy and relevance.",
        reasoning_framework=(
            "1. Collect feedback from users on detected anomalies.\n"
            "2. Analyze feedback for false positives/negatives and missed detections.\n"
            "3. Use feedback to tune detection thresholds and models.\n"
            "4. Document changes and monitor impact on detection accuracy.\n"
            "5. Repeat process for continuous improvement."
        ),
        key_factors=[
            "Feedback collection method",
            "Analysis process",
            "Model tuning",
            "Documentation",
            "Impact monitoring"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Anomaly Detection System Owner",
        adversary_position="Feedback may be inconsistent or incomplete.",
        counter_arguments=[
            "Aggregate feedback over time.",
            "Weight feedback by user expertise."
        ],
        resolution_strategy="Implement weighted and aggregated feedback mechanisms.",
        entity_scope="All anomaly detection processes.",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-FEED-001"
    ),
    DoctrineBlock(
        topic="Automated Remediation Triggering",
        keywords=["automated remediation", "self-healing", "anomaly detection", "incident response", "automation"],
        conclusion_template="Trigger automated remediation actions for specific anomaly types.",
        reasoning_framework=(
            "1. Define anomaly types eligible for automated remediation.\n"
            "2. Map detected anomalies to remediation playbooks.\n"
            "3. Trigger automation workflows upon anomaly detection.\n"
            "4. Monitor remediation outcomes and document results.\n"
            "5. Periodically review and update automation logic."
        ),
        key_factors=[
            "Anomaly-remediation mapping",
            "Automation workflow reliability",
            "Outcome monitoring",
            "Review process",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Incident Response Playbook",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Response Automation Team",
        adversary_position="Automation may not handle all edge cases.",
        counter_arguments=[
            "Limit automation to well-understood anomalies.",
            "Enable manual override."
        ],
        resolution_strategy="Hybrid automated-manual remediation approach.",
        entity_scope="Eligible anomaly types.",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-AUTO-001"
    ),
    DoctrineBlock(
        topic="Incident Postmortem and Anomaly Review",
        keywords=["postmortem", "anomaly review", "incident analysis", "continuous improvement", "documentation"],
        conclusion_template="Conduct postmortem reviews for major anomalies to drive process improvement.",
        reasoning_framework=(
            "1. Document all major anomaly incidents and responses.\n"
            "2. Conduct structured postmortem reviews with stakeholders.\n"
            "3. Identify root causes and process gaps.\n"
            "4. Implement corrective actions and monitor effectiveness.\n"
            "5. Share lessons learned across teams."
        ),
        key_factors=[
            "Incident documentation",
            "Stakeholder involvement",
            "Root cause analysis",
            "Corrective action implementation",
            "Knowledge sharing"
        ],
        primary_authority=[
            "GS03 Incident Management Policy",
            "SRE Book (Google, 2016)"
        ],
        burden_holder="Incident Manager",
        adversary_position="Postmortems may be time-consuming and under-prioritized.",
        counter_arguments=[
            "Limit scope to major incidents.",
            "Automate documentation where possible."
        ],
        resolution_strategy="Focus on high-impact incidents and streamline process.",
        entity_scope="All major anomaly incidents.",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-POST-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection in Streaming Data",
        keywords=["streaming data", "real-time", "anomaly detection", "low latency", "online algorithms"],
        conclusion_template="Apply online anomaly detection algorithms for streaming engine data.",
        reasoning_framework=(
            "1. Select online-capable anomaly detection algorithms.\n"
            "2. Process streaming data with low-latency detection logic.\n"
            "3. Flag anomalies in real-time for immediate response.\n"
            "4. Monitor detection accuracy and latency.\n"
            "5. Periodically review and tune streaming detection models."
        ),
        key_factors=[
            "Algorithm selection",
            "Latency requirements",
            "Detection accuracy",
            "Model tuning",
            "Monitoring"
        ],
        primary_authority=[
            "GS03 Streaming Analytics Guide",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Streaming Analytics Team",
        adversary_position="Online algorithms may be less accurate than batch methods.",
        counter_arguments=[
            "Balance latency and accuracy requirements.",
            "Hybrid online-batch validation."
        ],
        resolution_strategy="Hybrid streaming and batch anomaly validation.",
        entity_scope="All streaming engine data.",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-STREAM-001"
    ),
    DoctrineBlock(
        topic="Synthetic Data for Anomaly Detector Validation",
        keywords=["synthetic data", "validation", "anomaly detection", "test data", "simulation"],
        conclusion_template="Use synthetic data to validate and benchmark anomaly detection models.",
        reasoning_framework=(
            "1. Generate synthetic datasets with known anomaly patterns.\n"
            "2. Validate anomaly detectors against synthetic data.\n"
            "3. Benchmark detection accuracy and false positive/negative rates.\n"
            "4. Use results to tune models and thresholds.\n"
            "5. Document validation process and outcomes."
        ),
        key_factors=[
            "Synthetic data realism",
            "Benchmarking metrics",
            "Model tuning",
            "Documentation",
            "Continuous validation"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Analytics Team",
        adversary_position="Synthetic data may not capture all real-world complexities.",
        counter_arguments=[
            "Supplement with real-world validation.",
            "Iteratively improve synthetic data generation."
        ],
        resolution_strategy="Hybrid synthetic and real-world validation.",
        entity_scope="All anomaly detection models.",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-SYN-001"
    ),
    DoctrineBlock(
        topic="Drift Detection for Model Inputs",
        keywords=["drift detection", "model input", "feature drift", "monitoring", "ML"],
        conclusion_template="Monitor model input features for drift to maintain detection accuracy.",
        reasoning_framework=(
            "1. Track statistical properties of model input features over time.\n"
            "2. Detect significant drift using statistical tests.\n"
            "3. Retrain models if drift impacts detection accuracy.\n"
            "4. Document all drift incidents and model updates.\n"
            "5. Review drift detection logic periodically."
        ),
        key_factors=[
            "Feature monitoring",
            "Drift detection method",
            "Retraining criteria",
            "Documentation",
            "Review process"
        ],
        primary_authority=[
            "GS03 ML Monitoring Guidelines",
            "ISO/IEC 22989:2022"
        ],
        burden_holder="ML Operations Team",
        adversary_position="Some feature drift may not impact model accuracy.",
        counter_arguments=[
            "Correlate drift with model performance metrics.",
            "Prioritize retraining based on impact."
        ],
        resolution_strategy="Impact-based retraining triggers.",
        entity_scope="All model input features.",
        confidence=0.71,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ML-DRIFT-001"
    ),
    DoctrineBlock(
        topic="Time-to-Detection Metric for Anomalies",
        keywords=["time-to-detection", "anomaly detection", "latency", "performance metric", "monitoring"],
        conclusion_template="Track and optimize time-to-detection for all anomaly types.",
        reasoning_framework=(
            "1. Measure time from anomaly occurrence to detection.\n"
            "2. Set performance targets for time-to-detection.\n"
            "3. Monitor and report on detection latency.\n"
            "4. Optimize detection logic to reduce latency.\n"
            "5. Document improvements and outcomes."
        ),
        key_factors=[
            "Measurement accuracy",
            "Performance targets",
            "Detection logic optimization",
            "Reporting",
            "Documentation"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Anomaly Detection System Owner",
        adversary_position="Reducing latency may increase false positives.",
        counter_arguments=[
            "Balance speed and accuracy.",
            "Tune detection thresholds accordingly."
        ],
        resolution_strategy="Iterative tuning of detection logic.",
        entity_scope="All anomaly detection processes.",
        confidence=0.70,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-TTD-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection Model Versioning",
        keywords=["model versioning", "anomaly detection", "ML", "deployment", "traceability"],
        conclusion_template="Version all deployed anomaly detection models for traceability and rollback.",
        reasoning_framework=(
            "1. Assign unique version identifiers to all models.\n"
            "2. Track deployment history and associated incidents.\n"
            "3. Enable rollback to previous versions if issues arise.\n"
            "4. Document all version changes and rationale.\n"
            "5. Review versioning policy periodically."
        ),
        key_factors=[
            "Version identifier scheme",
            "Deployment tracking",
            "Rollback capability",
            "Documentation",
            "Policy review"
        ],
        primary_authority=[
            "GS03 ML Operations Guide",
            "ISO/IEC 22989:2022"
        ],
        burden_holder="ML Operations Team",
        adversary_position="Frequent version changes may cause confusion.",
        counter_arguments=[
            "Communicate version changes clearly.",
            "Limit changes to major updates."
        ],
        resolution_strategy="Structured versioning and communication policy.",
        entity_scope="All anomaly detection models.",
        confidence=0.69,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ML-VERS-001"
    ),
    DoctrineBlock(
        topic="Anomaly Prioritization Based on Business Impact",
        keywords=["prioritization", "business impact", "anomaly detection", "triage", "incident response"],
        conclusion_template="Prioritize anomaly response based on assessed business impact.",
        reasoning_framework=(
            "1. Assess business impact of each detected anomaly.\n"
            "2. Prioritize response and resource allocation accordingly.\n"
            "3. Review prioritization criteria with business stakeholders.\n"
            "4. Document prioritization decisions and outcomes.\n"
            "5. Refine criteria based on incident reviews."
        ),
        key_factors=[
            "Impact assessment method",
            "Stakeholder involvement",
            "Documentation",
            "Incident review",
            "Criteria refinement"
        ],
        primary_authority=[
            "GS03 Incident Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Manager",
        adversary_position="Impact assessment may be subjective.",
        counter_arguments=[
            "Standardize assessment criteria.",
            "Review with cross-functional teams."
        ],
        resolution_strategy="Iterative refinement of assessment criteria.",
        entity_scope="All detected anomalies.",
        confidence=0.68,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-PRIOR-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection Model Performance Benchmarking",
        keywords=["benchmarking", "model performance", "anomaly detection", "accuracy", "validation"],
        conclusion_template="Benchmark anomaly detection models against standard datasets and metrics.",
        reasoning_framework=(
            "1. Select standard datasets and performance metrics.\n"
            "2. Benchmark all deployed models regularly.\n"
            "3. Use results to guide model selection and tuning.\n"
            "4. Document benchmarking process and outcomes.\n"
            "5. Review benchmarks with stakeholders."
        ),
        key_factors=[
            "Dataset selection",
            "Metric selection",
            "Benchmarking frequency",
            "Documentation",
            "Stakeholder review"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Analytics Team",
        adversary_position="Benchmarks may not reflect production realities.",
        counter_arguments=[
            "Supplement with production data validation.",
            "Update benchmarks regularly."
        ],
        resolution_strategy="Hybrid benchmarking with production validation.",
        entity_scope="All anomaly detection models.",
        confidence=0.67,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-BENCH-001"
    ),
    DoctrineBlock(
        topic="Anomaly Escalation Workflow Standardization",
        keywords=["escalation workflow", "standardization", "anomaly detection", "incident response", "process"],
        conclusion_template="Standardize escalation workflows for all anomaly types to ensure consistent response.",
        reasoning_framework=(
            "1. Define escalation workflows for each anomaly type.\n"
            "2. Train staff on standardized processes.\n"
            "3. Monitor adherence and effectiveness.\n"
            "4. Document all escalations and outcomes.\n"
            "5. Review and update workflows periodically."
        ),
        key_factors=[
            "Workflow definition",
            "Staff training",
            "Monitoring",
            "Documentation",
            "Periodic review"
        ],
        primary_authority=[
            "GS03 Incident Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Standardization may reduce flexibility.",
        counter_arguments=[
            "Allow for exceptions with proper documentation.",
            "Review workflows after major incidents."
        ],
        resolution_strategy="Balance standardization with flexibility for edge cases.",
        entity_scope="All anomaly escalation workflows.",
        confidence=0.66,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-ESCAL-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection Model Fairness Assessment",
        keywords=["fairness", "bias", "anomaly detection", "model assessment", "ML ethics"],
        conclusion_template="Assess anomaly detection models for fairness and absence of bias.",
        reasoning_framework=(
            "1. Define fairness criteria relevant to engine operation.\n"
            "2. Assess models for bias across relevant dimensions.\n"
            "3. Document findings and corrective actions.\n"
            "4. Review fairness assessments with stakeholders.\n"
            "5. Update models to address identified biases."
        ),
        key_factors=[
            "Fairness criteria definition",
            "Bias assessment method",
            "Documentation",
            "Stakeholder review",
            "Model update process"
        ],
        primary_authority=[
            "GS03 ML Ethics Policy",
            "EU AI Act (2021)"
        ],
        burden_holder="ML Operations Team",
        adversary_position="Fairness criteria may be subjective.",
        counter_arguments=[
            "Standardize criteria and review process.",
            "Engage diverse stakeholders."
        ],
        resolution_strategy="Iterative refinement of fairness criteria.",
        entity_scope="All anomaly detection models.",
        confidence=0.65,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-FAIR-001"
    ),
    DoctrineBlock(
        topic="Anomaly Notification Rate Limiting",
        keywords=["notification", "rate limiting", "anomaly detection", "alerting", "spam prevention"],
        conclusion_template="Limit anomaly notifications to prevent alert spam and ensure actionable alerts.",
        reasoning_framework=(
            "1. Set rate limits for anomaly notifications per channel and recipient.\n"
            "2. Suppress excess notifications within defined intervals.\n"
            "3. Aggregate suppressed notifications for summary reporting.\n"
            "4. Document rate limiting logic and rationale.\n"
            "5. Review limits based on responder feedback."
        ),
        key_factors=[
            "Rate limit configuration",
            "Notification aggregation",
            "Documentation",
            "Responder feedback",
            "Periodic review"
        ],
        primary_authority=[
            "GS03 Alerting Policy",
            "SRE Book (Google, 2016)"
        ],
        burden_holder="Alerting System Owner",
        adversary_position="Rate limiting may delay critical notifications.",
        counter_arguments=[
            "Allow overrides for critical alerts.",
            "Tune limits based on incident data."
        ],
        resolution_strategy="Balance rate limiting with critical alert delivery.",
        entity_scope="All anomaly notifications.",
        confidence=0.64,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-NOTIF-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Rare Events",
        keywords=["rare event", "anomaly detection", "low frequency", "outlier", "sensitivity"],
        conclusion_template="Tune anomaly detectors for sensitivity to rare but high-impact events.",
        reasoning_framework=(
            "1. Identify rare but critical event types in engine operation.\n"
            "2. Tune anomaly detectors for increased sensitivity to these events.\n"
            "3. Monitor for false positives and adjust thresholds as needed.\n"
            "4. Document tuning process and incident outcomes.\n"
            "5. Review sensitivity settings periodically."
        ),
        key_factors=[
            "Rare event identification",
            "Detector sensitivity",
            "Threshold tuning",
            "Documentation",
            "Periodic review"
        ],
        primary_authority=[
            "GS03 Analytics Handbook",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Anomaly Detection System Owner",
        adversary_position="Increased sensitivity may raise false positives.",
        counter_arguments=[
            "Balance sensitivity with specificity.",
            "Aggregate alerts for rare events."
        ],
        resolution_strategy="Iterative threshold tuning and alert aggregation.",
        entity_scope="All rare event types.",
        confidence=0.63,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-RARE-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Engine Configuration Changes",
        keywords=["configuration change", "anomaly detection", "change management", "drift", "monitoring"],
        conclusion_template="Monitor for anomalies immediately following engine configuration changes.",
        reasoning_framework=(
            "1. Integrate configuration change events with anomaly monitoring.\n"
            "2. Increase anomaly detection sensitivity post-change.\n"
            "3. Correlate detected anomalies with recent changes.\n"
            "4. Document incidents and configuration details.\n"
            "5. Review detection logic after major changes."
        ),
        key_factors=[
            "Change event integration",
            "Sensitivity adjustment",
            "Correlation analysis",
            "Documentation",
            "Logic review"
        ],
        primary_authority=[
            "GS03 Change Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Change Management Team",
        adversary_position="Some anomalies may be expected after changes.",
        counter_arguments=[
            "Define expected anomaly profiles for changes.",
            "Suppress known benign anomalies."
        ],
        resolution_strategy="Profile expected anomalies and suppress known benign cases.",
        entity_scope="All configuration changes.",
        confidence=0.62,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-CONF-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Engine Upgrades",
        keywords=["engine upgrade", "anomaly detection", "change management", "monitoring", "drift"],
        conclusion_template="Increase anomaly monitoring during and after engine upgrades.",
        reasoning_framework=(
            "1. Flag upgrade periods in monitoring system.\n"
            "2. Increase anomaly detection sensitivity during and after upgrades.\n"
            "3. Correlate anomalies with upgrade events.\n"
            "4. Document all incidents and upgrade details.\n"
            "5. Review detection logic post-upgrade."
        ),
        key_factors=[
            "Upgrade event integration",
            "Sensitivity adjustment",
            "Correlation analysis",
            "Documentation",
            "Logic review"
        ],
        primary_authority=[
            "GS03 Change Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Change Management Team",
        adversary_position="Some anomalies may be expected during upgrades.",
        counter_arguments=[
            "Profile expected anomalies for upgrades.",
            "Suppress known benign anomalies."
        ],
        resolution_strategy="Profile and suppress expected benign anomalies.",
        entity_scope="All engine upgrade events.",
        confidence=0.61,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-UPGRADE-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for External Dependency Failures",
        keywords=["external dependency", "failure", "anomaly detection", "dependency monitoring", "incident response"],
        conclusion_template="Correlate anomalies with external dependency failures for rapid response.",
        reasoning_framework=(
            "1. Monitor status of all external dependencies.\n"
            "2. Correlate engine anomalies with dependency failure events.\n"
            "3. Escalate incidents with dependency context.\n"
            "4. Document all correlated incidents and outcomes.\n"
            "5. Review dependency monitoring coverage periodically."
        ),
        key_factors=[
            "Dependency monitoring",
            "Correlation analysis",
            "Escalation process",
            "Documentation",
            "Coverage review"
        ],
        primary_authority=[
            "GS03 Dependency Management Policy",
            "ISO/IEC 27035:2016"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Some anomalies may be unrelated to dependencies.",
        counter_arguments=[
            "Validate correlation before escalation.",
            "Maintain clear dependency mapping."
        ],
        resolution_strategy="Maintain up-to-date dependency mapping and validation.",
        entity_scope="All external dependencies.",
        confidence=0.60,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-DEP-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Security Events",
        keywords=["security event", "anomaly detection", "intrusion detection", "security monitoring", "incident response"],
        conclusion_template="Prioritize anomaly detection for security-relevant events.",
        reasoning_framework=(
            "1. Tag security-relevant metrics and events in monitoring system.\n"
            "2. Apply enhanced anomaly detection for these events.\n"
            "3. Escalate detected anomalies to security response team.\n"
            "4. Document all security anomaly incidents.\n"
            "5. Review detection logic with security stakeholders."
        ),
        key_factors=[
            "Security event tagging",
            "Detection logic enhancement",
            "Escalation process",
            "Documentation",
            "Stakeholder review"
        ],
        primary_authority=[
            "GS03 Security Operations Guide",
            "NIST SP 800-94"
        ],
        burden_holder="Security Operations Team",
        adversary_position="Enhanced detection may increase false positives.",
        counter_arguments=[
            "Tune thresholds for security events.",
            "Aggregate low-severity alerts."
        ],
        resolution_strategy="Balance sensitivity and specificity for security events.",
        entity_scope="All security-relevant events.",
        confidence=0.59,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-SEC-002"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Compliance Monitoring",
        keywords=["compliance", "anomaly detection", "regulatory", "monitoring", "audit"],
        conclusion_template="Integrate anomaly detection with compliance monitoring for audit readiness.",
        reasoning_framework=(
            "1. Identify compliance-relevant metrics and events.\n"
            "2. Integrate anomaly detection with compliance monitoring systems.\n"
            "3. Document all compliance-related anomalies for audit.\n"
            "4. Review detection logic with compliance stakeholders.\n"
            "5. Update monitoring based on regulatory changes."
        ),
        key_factors=[
            "Compliance metric identification",
            "Integration with compliance systems",
            "Documentation",
            "Stakeholder review",
            "Regulatory update process"
        ],
        primary_authority=[
            "GS03 Compliance Policy",
            "ISO/IEC 27001:2022"
        ],
        burden_holder="Compliance Team",
        adversary_position="Compliance anomalies may be over-reported.",
        counter_arguments=[
            "Tune detection for compliance context.",
            "Review with compliance officers."
        ],
        resolution_strategy="Stakeholder review and tuning for compliance context.",
        entity_scope="All compliance-relevant events.",
        confidence=0.58,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-COMP-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for User Experience Metrics",
        keywords=["user experience", "anomaly detection", "UX", "monitoring", "incident response"],
        conclusion_template="Monitor user experience metrics for anomalies impacting end-users.",
        reasoning_framework=(
            "1. Define user experience metrics (e.g., response time, error rate).\n"
            "2. Apply anomaly detection to these metrics.\n"
            "3. Escalate anomalies impacting end-user experience.\n"
            "4. Document incidents and user impact.\n"
            "5. Review detection logic with UX stakeholders."
        ),
        key_factors=[
            "Metric definition",
            "Detection logic",
            "Escalation process",
            "Documentation",
            "Stakeholder review"
        ],
        primary_authority=[
            "GS03 UX Monitoring Policy",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="UX Monitoring Team",
        adversary_position="Some anomalies may not impact users directly.",
        counter_arguments=[
            "Correlate anomalies with user feedback.",
            "Prioritize based on user impact."
        ],
        resolution_strategy="User impact-based prioritization.",
        entity_scope="All user experience metrics.",
        confidence=0.57,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-UX-001"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Engine Resource Contention",
        keywords=["resource contention", "anomaly detection", "performance", "monitoring", "incident response"],
        conclusion_template="Detect and escalate resource contention anomalies for performance remediation.",
        reasoning_framework=(
            "1. Monitor resource usage and contention metrics (CPU, memory, I/O).\n"
            "2. Detect anomalies indicating contention.\n"
            "3. Escalate for performance remediation.\n"
            "4. Document incidents and remediation actions.\n"
            "5. Review detection logic with performance engineering."
        ),
        key_factors=[
            "Metric selection",
            "Detection logic",
            "Escalation process",
            "Documentation",
            "Stakeholder review"
        ],
        primary_authority=[
            "GS03 Performance Engineering Guide",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Performance Engineering Team",
        adversary_position="Some contention may be transient or expected.",
        counter_arguments=[
            "Correlate with workload and scheduling.",
            "Allow for short-term contention."
        ],
        resolution_strategy="Context-aware contention detection.",
        entity_scope="All resource contention metrics.",
        confidence=0.56,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-RES-003"
    ),
    DoctrineBlock(
        topic="Anomaly Detection for Engine Scaling Events",
        keywords=["scaling event", "anomaly detection", "autoscaling", "monitoring", "incident response"],
        conclusion_template="Monitor for anomalies during and after engine scaling events.",
        reasoning_framework=(
            "1. Integrate scaling event data with anomaly monitoring.\n"
            "2. Increase detection sensitivity during scaling.\n"
            "3. Correlate anomalies with scaling events.\n"
            "4. Document incidents and scaling details.\n"
            "5. Review detection logic post-scaling."
        ),
        key_factors=[
            "Scaling event integration",
            "Sensitivity adjustment",
            "Correlation analysis",
            "Documentation",
            "Logic review"
        ],
        primary_authority=[
            "GS03 Autoscaling Policy",
            "ISO/IEC 25010:2011"
        ],
        burden_holder="Operations Team",
        adversary_position="Some anomalies may be expected during scaling.",
        counter_arguments=[
            "Profile expected anomalies for scaling.",
            "Suppress known benign anomalies."
        ],
        resolution_strategy="Profile and suppress expected benign anomalies.",
        entity_scope="All scaling events.",
        confidence=0.55,
        confidence_zone="Medium",
        controlling_precedent="GS03-2021-SCALE-001"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]