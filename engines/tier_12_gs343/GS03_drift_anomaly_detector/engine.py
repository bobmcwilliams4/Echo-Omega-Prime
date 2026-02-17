import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# Enums

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    Z_SCORE_ANOMALY = "Z_SCORE_ANOMALY"
    IQR_OUTLIER = "IQR_OUTLIER"
    ISOLATION_FOREST = "ISOLATION_FOREST"
    BASELINE_DRIFT = "BASELINE_DRIFT"
    RESPONSE_TIME_DRIFT = "RESPONSE_TIME_DRIFT"
    ERROR_RATE_DRIFT = "ERROR_RATE_DRIFT"
    CONFIDENCE_SCORE_SHIFT = "CONFIDENCE_SCORE_SHIFT"
    QUALITY_METRIC_DRIFT = "QUALITY_METRIC_DRIFT"
    BEHAVIORAL_FINGERPRINT = "BEHAVIORAL_FINGERPRINT"
    SEASONAL_PATTERN = "SEASONAL_PATTERN"
    ALERT_FATIGUE = "ALERT_FATIGUE"
    ANOMALY_CORRELATION = "ANOMALY_CORRELATION"
    ROOT_CAUSE_INFERENCE = "ROOT_CAUSE_INFERENCE"
    ANOMALY_SEVERITY = "ANOMALY_SEVERITY"
    TRENDING_ANOMALY = "TRENDING_ANOMALY"
    SUDDEN_ANOMALY = "SUDDEN_ANOMALY"
    PHANTOM_LOAD = "PHANTOM_LOAD"
    RESOURCE_LEAK = "RESOURCE_LEAK"
    MEMORY_GROWTH = "MEMORY_GROWTH"
    CONNECTION_POOL_DRIFT = "CONNECTION_POOL_DRIFT"
    CACHE_HIT_DRIFT = "CACHE_HIT_DRIFT"
    API_LATENCY_DRIFT = "API_LATENCY_DRIFT"
    DATA_QUALITY_DRIFT = "DATA_QUALITY_DRIFT"
    OTHER = "OTHER"

# Metrics Collector

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []

    def record_query(self, query_id: str, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.queries.append({
                "query_id": query_id,
                "doctrine_ids": doctrine_ids,
                "timestamp": datetime.utcnow().isoformat(),
                "latency": latency
            })
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1
            self.latencies.append(latency)
            if len(self.latencies) > 1000:
                self.latencies = self.latencies[-1000:]

    def record_error(self, query_id: str, error: str):
        with self.lock:
            self.errors.append({
                "query_id": query_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.latencies:
                return {"min": 0, "max": 0, "avg": 0}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "avg": sum(self.latencies) / len(self.latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.queries if datetime.fromisoformat(q["timestamp"]) >= cutoff)

metrics_collector = MetricsCollector()

# Pydantic Models

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Description of the drift scenario or anomaly context")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of engine or entity under analysis")
    complexity: int = Field(..., ge=1, le=10, description="Complexity level of the analysis")

class QueryResponse(BaseModel):
    engine_id: str
    query_id: str
    mode: ResponseMode
    confidence: float
    confidence_zone: ConfidenceZone
    position_zone: PositionZone
    primary_conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str

# Doctrine Block

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
    confidence_zone: ConfidenceZone
    controlling_precedent: List[str]
    position_zone: PositionZone
    issue_category: IssueCategory

# Doctrine Cache

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Z-Score Based Anomaly Detection",
        keywords=["z-score", "standard deviation", "outlier", "statistical anomaly", "threshold"],
        conclusion_template="Z-score based anomaly detection is effective for identifying outliers in normally distributed engine performance metrics. It is recommended for baseline drift monitoring when the underlying data distribution is stable.",
        reasoning_framework=(
            "The Z-score method computes the number of standard deviations a data point is from the mean. "
            "For engine performance metrics (e.g., response time, error rate), calculate the mean (μ) and standard deviation (σ) over a rolling window. "
            "For each new observation x, compute z = (x - μ) / σ. "
            "Flag anomalies where |z| > threshold (commonly 2 or 3). "
            "This method assumes data is approximately normal; for skewed distributions, consider log-transforming the data. "
            "Monitor for changes in μ and σ over time to detect baseline drift. "
            "If the standard deviation increases, the anomaly threshold should be recalibrated. "
            "Aggregate flagged anomalies to distinguish between isolated outliers and systemic drift. "
            "Correlate z-score anomalies with operational events to reduce false positives. "
            "Document all threshold changes and rationale for auditability. "
            "Compare z-score findings with other methods (e.g., IQR, isolation forest) for triangulation. "
            "Ensure that alerting is rate-limited to prevent fatigue. "
            "Cite: Chandola et al., 'Anomaly Detection: A Survey', ACM Computing Surveys, 2009."
        ),
        key_factors=[
            "Normality of metric distribution",
            "Rolling window size",
            "Threshold calibration",
            "Baseline stability",
            "Alert rate"
        ],
        primary_authority=[
            "Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly Detection: A Survey. ACM Computing Surveys.",
            "Barnett, V., & Lewis, T. (1994). Outliers in Statistical Data. Wiley.",
            "Aggarwal, C.C. (2017). Outlier Analysis. Springer."
        ],
        burden_holder="System operator",
        adversary_position="Z-score is sensitive to non-normality and may miss anomalies in heavy-tailed distributions.",
        counter_arguments=[
            "Z-score assumes normality; real-world data may be skewed.",
            "Thresholds may not adapt to changing baselines.",
            "High variance can mask anomalies.",
            "Manual calibration required.",
            "Not robust to seasonality."
        ],
        resolution_strategy="Apply normality tests; use robust statistics if needed; combine with other methods for coverage.",
        entity_scope="All engines with numeric performance metrics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Chandola et al., 2009",
            "Barnett & Lewis, 1994"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.Z_SCORE_ANOMALY
    ),
    DoctrineBlock(
        topic="Interquartile Range (IQR) Outlier Detection",
        keywords=["IQR", "outlier", "robust statistics", "boxplot", "non-parametric"],
        conclusion_template="IQR-based outlier detection is robust to non-normal distributions and effective for identifying extreme values in engine performance metrics. Recommended for environments with frequent distributional shifts.",
        reasoning_framework=(
            "The IQR method calculates the range between the 25th (Q1) and 75th (Q3) percentiles. "
            "For each metric, compute Q1 and Q3 over a rolling window. "
            "The IQR is Q3 - Q1. Outliers are defined as points below Q1 - 1.5*IQR or above Q3 + 1.5*IQR. "
            "This method is robust to non-normality and less sensitive to extreme values than Z-score. "
            "Apply to error rates, latency, and quality scores. "
            "Monitor the frequency of outliers as an indicator of drift. "
            "If the IQR itself changes significantly, investigate for systemic shifts. "
            "Document all detected outliers for audit trail. "
            "Combine with Z-score for improved coverage. "
            "Reference: Tukey, J.W. (1977). Exploratory Data Analysis."
        ),
        key_factors=[
            "Percentile estimation accuracy",
            "Window size",
            "Sensitivity to distribution shifts",
            "Robustness to outliers",
            "Auditability"
        ],
        primary_authority=[
            "Tukey, J.W. (1977). Exploratory Data Analysis.",
            "Leys, C. et al. (2013). Detecting outliers: Do not use standard deviation around the mean, use absolute deviation around the median. Journal of Experimental Social Psychology.",
            "Aggarwal, C.C. (2017). Outlier Analysis. Springer."
        ],
        burden_holder="System analyst",
        adversary_position="IQR method may miss subtle anomalies within the interquartile range.",
        counter_arguments=[
            "Insensitive to anomalies within IQR.",
            "Requires sufficient data for percentile estimation.",
            "May not detect gradual drift.",
            "Not adaptive to rapid baseline changes.",
            "Potential for masking in multimodal distributions."
        ],
        resolution_strategy="Supplement with trend analysis; adjust window size dynamically.",
        entity_scope="All engines with numeric metrics",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Tukey, 1977",
            "Leys et al., 2013"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.IQR_OUTLIER
    ),
    DoctrineBlock(
        topic="Isolation Forest for Anomaly Detection",
        keywords=["isolation forest", "ensemble", "unsupervised", "tree-based", "multivariate"],
        conclusion_template="Isolation Forest is suitable for multivariate anomaly detection in engine telemetry. It isolates anomalies with fewer splits, making it effective for complex, high-dimensional data.",
        reasoning_framework=(
            "Isolation Forest builds an ensemble of random trees to partition the data. "
            "Anomalies are isolated with fewer splits due to their rarity. "
            "Apply to multidimensional engine metrics (e.g., latency, error rate, memory usage). "
            "Train the model on historical baseline data. "
            "Score new observations by their average path length in the trees. "
            "Shorter paths indicate anomalies. "
            "Thresholds are set based on contamination parameter (expected proportion of anomalies). "
            "Monitor model drift by evaluating path length distributions over time. "
            "Retrain periodically to adapt to new baselines. "
            "Correlate isolation forest findings with univariate methods for validation. "
            "Reference: Liu, F.T., Ting, K.M., & Zhou, Z.-H. (2008). Isolation Forest. ICDM."
        ),
        key_factors=[
            "Contamination parameter",
            "Retraining frequency",
            "Feature selection",
            "Model drift",
            "Correlation with univariate methods"
        ],
        primary_authority=[
            "Liu, F.T., Ting, K.M., & Zhou, Z.-H. (2008). Isolation Forest. ICDM.",
            "Hariri, S. et al. (2019). Extended Isolation Forest. IEEE Transactions on Knowledge and Data Engineering.",
            "Aggarwal, C.C. (2017). Outlier Analysis. Springer."
        ],
        burden_holder="Model maintainer",
        adversary_position="Isolation Forest may overfit to noise or underperform with small sample sizes.",
        counter_arguments=[
            "Requires careful feature selection.",
            "Sensitive to contamination parameter.",
            "Retraining is resource-intensive.",
            "Interpretability is limited.",
            "May miss context-specific anomalies."
        ],
        resolution_strategy="Combine with explainable models; validate with domain knowledge.",
        entity_scope="Engines with multivariate telemetry",
        confidence=0.89,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "Liu et al., 2008",
            "Hariri et al., 2019"
        ],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.ISOLATION_FOREST
    ),
    DoctrineBlock(
        topic="Engine Performance Baseline Tracking",
        keywords=["baseline", "performance", "tracking", "reference window", "drift"],
        conclusion_template="Baseline tracking is essential for distinguishing between expected variation and true anomalies in engine performance. Use adaptive reference windows to account for gradual drift.",
        reasoning_framework=(
            "Establish a rolling baseline for each key metric (e.g., mean response time, error rate) using a reference window (e.g., last 7 days). "
            "Compare current observations to the baseline to detect deviations. "
            "Adapt the window size based on seasonality and workload changes. "
            "If the baseline shifts persistently, update the reference window. "
            "Document all baseline recalibrations for auditability. "
            "Apply statistical tests (e.g., CUSUM, Page-Hinkley) to detect significant shifts. "
            "Correlate baseline drift with deployment events or configuration changes. "
            "Alert only on deviations exceeding both statistical and operational thresholds. "
            "Reference: Adams, R.P., & MacKay, D.J.C. (2007). Bayesian Online Changepoint Detection."
        ),
        key_factors=[
            "Reference window size",
            "Seasonality adjustment",
            "Recalibration policy",
            "Change detection test",
            "Audit documentation"
        ],
        primary_authority=[
            "Adams, R.P., & MacKay, D.J.C. (2007). Bayesian Online Changepoint Detection.",
            "Basseville, M., & Nikiforov, I.V. (1993). Detection of Abrupt Changes: Theory and Application. Prentice Hall.",
            "Page, E.S. (1954). Continuous Inspection Schemes. Biometrika."
        ],
        burden_holder="Performance engineer",
        adversary_position="Static baselines may not adapt to gradual changes, leading to missed anomalies.",
        counter_arguments=[
            "Baseline recalibration can mask slow drift.",
            "Reference window selection is subjective.",
            "Seasonal effects may confound detection.",
            "Operational events may not be documented.",
            "Statistical tests may be sensitive to noise."
        ],
        resolution_strategy="Automate baseline updates; integrate with deployment logs.",
        entity_scope="All engines with time-series metrics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Adams & MacKay, 2007",
            "Basseville & Nikiforov, 1993"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.BASELINE_DRIFT
    ),
    DoctrineBlock(
        topic="Response Time Drift Detection",
        keywords=["response time", "latency", "drift", "distribution shift", "SLA"],
        conclusion_template="Monitor response time distributions for drift using statistical tests and SLA thresholds. Identify both gradual and sudden increases to prevent SLA violations.",
        reasoning_framework=(
            "Collect response time data over fixed intervals. "
            "Compute summary statistics (mean, median, percentiles) and compare to historical baselines. "
            "Apply statistical tests (e.g., Kolmogorov-Smirnov, Mann-Whitney U) to detect distributional shifts. "
            "Flag both gradual increases (trending drift) and sudden spikes. "
            "Correlate drift events with deployment or infrastructure changes. "
            "Set alert thresholds based on SLA requirements. "
            "Document all detected drifts and remediation actions. "
            "Reference: Jain, R. (1991). The Art of Computer Systems Performance Analysis."
        ),
        key_factors=[
            "Interval selection",
            "SLA thresholds",
            "Statistical test choice",
            "Correlation with events",
            "Remediation documentation"
        ],
        primary_authority=[
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill.",
            "Kolmogorov, A.N. (1933). Sulla determinazione empirica di una legge di distribuzione."
        ],
        burden_holder="SRE team",
        adversary_position="Statistical tests may be confounded by workload changes.",
        counter_arguments=[
            "Workload variability can trigger false positives.",
            "SLA thresholds may be too rigid.",
            "Manual correlation with events is error-prone.",
            "Gradual drift may go undetected.",
            "Remediation actions may not be timely."
        ],
        resolution_strategy="Automate event correlation; tune thresholds dynamically.",
        entity_scope="Latency-sensitive engines",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jain, 1991",
            "Kolmogorov, 1933"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.RESPONSE_TIME_DRIFT
    ),
    DoctrineBlock(
        topic="Error Rate Drift Analysis",
        keywords=["error rate", "drift", "change detection", "CUSUM", "quality"],
        conclusion_template="Track error rates over time to detect drift. Use CUSUM or similar tests for early detection of persistent increases.",
        reasoning_framework=(
            "Monitor error rates at regular intervals (e.g., per hour). "
            "Apply CUSUM (Cumulative Sum Control Chart) to detect sustained increases. "
            "Set control limits based on historical error rate variance. "
            "Flag anomalies where CUSUM exceeds control limits. "
            "Correlate error rate drift with recent deployments or configuration changes. "
            "Document all drift events and root cause analyses. "
            "Reference: Basseville, M., & Nikiforov, I.V. (1993). Detection of Abrupt Changes."
        ),
        key_factors=[
            "Interval granularity",
            "CUSUM parameterization",
            "Control limit calibration",
            "Root cause analysis",
            "Documentation"
        ],
        primary_authority=[
            "Basseville, M., & Nikiforov, I.V. (1993). Detection of Abrupt Changes. Prentice Hall.",
            "Page, E.S. (1954). Continuous Inspection Schemes. Biometrika.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley."
        ],
        burden_holder="Quality assurance",
        adversary_position="CUSUM may be sensitive to noise and require careful tuning.",
        counter_arguments=[
            "False positives from transient spikes.",
            "Parameter tuning is non-trivial.",
            "Requires accurate error logging.",
            "Root cause may not be clear.",
            "Documentation burden."
        ],
        resolution_strategy="Automate parameter tuning; integrate with error logging system.",
        entity_scope="All engines with error metrics",
        confidence=0.88,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "Basseville & Nikiforov, 1993",
            "Page, 1954"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.ERROR_RATE_DRIFT
    ),
    DoctrineBlock(
        topic="Confidence Score Distribution Shift",
        keywords=["confidence score", "distribution shift", "calibration", "drift", "ECE"],
        conclusion_template="Monitor confidence score distributions for shifts using statistical divergence measures. Recalibrate models if significant drift is detected.",
        reasoning_framework=(
            "Collect confidence scores from engine outputs over time. "
            "Compute distribution statistics (mean, variance, histogram). "
            "Apply divergence measures (e.g., Kullback-Leibler, Jensen-Shannon) to compare current and baseline distributions. "
            "Flag significant shifts exceeding predefined thresholds. "
            "Evaluate Expected Calibration Error (ECE) to assess model calibration. "
            "If drift is persistent, retrain or recalibrate the model. "
            "Document all recalibration events. "
            "Reference: Guo, C. et al. (2017). On Calibration of Modern Neural Networks."
        ),
        key_factors=[
            "Divergence metric selection",
            "Threshold calibration",
            "ECE computation",
            "Recalibration policy",
            "Documentation"
        ],
        primary_authority=[
            "Guo, C. et al. (2017). On Calibration of Modern Neural Networks. ICML.",
            "Kullback, S., & Leibler, R.A. (1951). On Information and Sufficiency. Annals of Mathematical Statistics.",
            "Bröcker, J. (2009). Reliability, sufficiency, and the decomposition of proper scores. Quarterly Journal of the Royal Meteorological Society."
        ],
        burden_holder="Model owner",
        adversary_position="Divergence metrics may be unstable with small samples.",
        counter_arguments=[
            "Sample size sensitivity.",
            "Thresholds may not generalize.",
            "ECE requires ground truth.",
            "Recalibration may not address root cause.",
            "Documentation overhead."
        ],
        resolution_strategy="Aggregate over longer windows; automate ECE computation.",
        entity_scope="Engines with probabilistic outputs",
        confidence=0.87,
        confidence_zone=ConfidenceZone.DISCLOSURE,
        controlling_precedent=[
            "Guo et al., 2017",
            "Kullback & Leibler, 1951"
        ],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.CONFIDENCE_SCORE_SHIFT
    ),
    DoctrineBlock(
        topic="Output Quality Metric Drift",
        keywords=["output quality", "metric drift", "reference distribution", "quality score", "degradation"],
        conclusion_template="Track output quality metrics over time to detect degradation. Use reference distributions and alert on significant deviations.",
        reasoning_framework=(
            "Define key output quality metrics (e.g., accuracy, F1, BLEU). "
            "Establish reference distributions from historical data. "
            "Monitor current metrics and compare to reference using statistical tests (e.g., t-test, KS test). "
            "Flag significant deviations for investigation. "
            "Correlate quality drift with upstream data or model changes. "
            "Document all drift events and corrective actions. "
            "Reference: Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems."
        ),
        key_factors=[
            "Metric selection",
            "Reference distribution stability",
            "Test selection",
            "Correlation with changes",
            "Documentation"
        ],
        primary_authority=[
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="Quality engineer",
        adversary_position="Reference distributions may become stale, masking real drift.",
        counter_arguments=[
            "Stale references mask drift.",
            "Metric selection bias.",
            "Test sensitivity to sample size.",
            "Correlation may be spurious.",
            "Documentation burden."
        ],
        resolution_strategy="Refresh references regularly; automate metric tracking.",
        entity_scope="All engines with quality metrics",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Sculley et al., 2015"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.QUALITY_METRIC_DRIFT
    ),
    DoctrineBlock(
        topic="Behavioral Fingerprinting per Engine",
        keywords=["behavioral fingerprint", "engine", "profile", "anomaly", "pattern recognition"],
        conclusion_template="Establish behavioral fingerprints for each engine to detect deviations from typical patterns. Use unsupervised clustering and time-series analysis.",
        reasoning_framework=(
            "Collect multivariate time-series data for each engine (e.g., latency, error rate, resource usage). "
            "Apply unsupervised clustering (e.g., k-means, DBSCAN) to group similar behavioral patterns. "
            "Establish a fingerprint for each engine based on cluster centroids and temporal features. "
            "Monitor for deviations from the established fingerprint. "
            "Flag significant deviations as potential anomalies. "
            "Correlate with operational events for context. "
            "Document all fingerprint updates and anomaly events. "
            "Reference: Ahmed, M. et al. (2016). A Survey of Network Anomaly Detection Techniques."
        ),
        key_factors=[
            "Clustering algorithm selection",
            "Feature engineering",
            "Temporal granularity",
            "Deviation threshold",
            "Documentation"
        ],
        primary_authority=[
            "Ahmed, M. et al. (2016). A Survey of Network Anomaly Detection Techniques. Journal of Network and Computer Applications.",
            "Aggarwal, C.C. (2017). Outlier Analysis. Springer.",
            "Chandola, V. et al. (2009). Anomaly Detection: A Survey. ACM Computing Surveys."
        ],
        burden_holder="System architect",
        adversary_position="Clustering may not capture rare but valid behaviors.",
        counter_arguments=[
            "Rare behaviors may be misclassified.",
            "Feature selection bias.",
            "Cluster drift over time.",
            "Manual labeling required.",
            "Documentation overhead."
        ],
        resolution_strategy="Review clusters periodically; involve domain experts.",
        entity_scope="All engines",
        confidence=0.88,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "Ahmed et al., 2016"
        ],
        position_zone=PositionZone.PLANNING,
        issue_category=IssueCategory.BEHAVIORAL_FINGERPRINT
    ),
    DoctrineBlock(
        topic="Seasonal Pattern Accounting",
        keywords=["seasonality", "pattern", "time-series", "trend", "anomaly detection"],
        conclusion_template="Account for seasonal patterns in engine metrics to reduce false positives. Use decomposition methods to separate trend, seasonality, and residuals.",
        reasoning_framework=(
            "Decompose time-series metrics into trend, seasonal, and residual components (e.g., STL decomposition). "
            "Model the seasonal component to set dynamic anomaly thresholds. "
            "Monitor residuals for anomalies rather than raw values. "
            "Update seasonal models periodically to adapt to changing patterns. "
            "Correlate anomalies with known seasonal events (e.g., traffic surges). "
            "Document all model updates and detected anomalies. "
            "Reference: Hyndman, R.J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice."
        ),
        key_factors=[
            "Decomposition method",
            "Model update frequency",
            "Threshold adaptation",
            "Event correlation",
            "Documentation"
        ],
        primary_authority=[
            "Hyndman, R.J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice. OTexts.",
            "Cleveland, R.B. et al. (1990). STL: A Seasonal-Trend Decomposition Procedure. Journal of Official Statistics.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley."
        ],
        burden_holder="Data scientist",
        adversary_position="Seasonal models may lag behind rapid pattern changes.",
        counter_arguments=[
            "Model lag during rapid change.",
            "Complexity in decomposition.",
            "Manual event annotation.",
            "Residuals may still contain drift.",
            "Documentation burden."
        ],
        resolution_strategy="Automate model updates; integrate with event logs.",
        entity_scope="Engines with seasonal metrics",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Hyndman & Athanasopoulos, 2018"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.SEASONAL_PATTERN
    ),
    DoctrineBlock(
        topic="Alert Fatigue Prevention: Minimum Severity Thresholds",
        keywords=["alert fatigue", "minimum severity", "threshold", "alerting", "false positive"],
        conclusion_template="Set minimum severity thresholds for anomaly alerts to prevent fatigue. Prioritize actionable alerts and suppress low-impact events.",
        reasoning_framework=(
            "Define severity levels for anomalies based on impact (e.g., SLA violation, resource exhaustion). "
            "Set minimum thresholds for alert generation. "
            "Suppress alerts for events below the threshold. "
            "Aggregate similar low-severity anomalies and report as summary. "
            "Monitor alert volume and adjust thresholds to maintain manageable levels. "
            "Document all threshold changes. "
            "Reference: Kim, S. et al. (2018). Reducing Alert Fatigue in IT Operations."
        ),
        key_factors=[
            "Severity definition",
            "Threshold calibration",
            "Alert aggregation",
            "Volume monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Kim, S. et al. (2018). Reducing Alert Fatigue in IT Operations. IEEE Cloud Computing.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS."
        ],
        burden_holder="Operations team",
        adversary_position="High thresholds may suppress important early warnings.",
        counter_arguments=[
            "Suppressed alerts may hide issues.",
            "Thresholds require tuning.",
            "Aggregation may obscure root cause.",
            "Documentation overhead.",
            "Alert volume metrics may lag."
        ],
        resolution_strategy="Review suppressed alerts periodically; adjust thresholds as needed.",
        entity_scope="All engines",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kim et al., 2018"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ALERT_FATIGUE
    ),
    DoctrineBlock(
        topic="Anomaly Correlation Across Engines",
        keywords=["anomaly correlation", "cross-engine", "root cause", "event correlation", "systemic"],
        conclusion_template="Correlate anomalies across engines to identify systemic issues. Use event correlation and graph-based analysis.",
        reasoning_framework=(
            "Collect anomaly events from all engines with timestamps and context. "
            "Apply event correlation algorithms (e.g., temporal, causal) to group related anomalies. "
            "Construct a correlation graph to visualize relationships. "
            "Identify root causes affecting multiple engines. "
            "Prioritize investigation of systemic anomalies over isolated events. "
            "Document all correlation findings and remediation actions. "
            "Reference: Steinder, M., & Sethi, A.S. (2004). Fault Localization in Distributed Systems."
        ),
        key_factors=[
            "Event correlation algorithm",
            "Timestamp accuracy",
            "Contextual information",
            "Graph construction",
            "Documentation"
        ],
        primary_authority=[
            "Steinder, M., & Sethi, A.S. (2004). Fault Localization in Distributed Systems. IEEE Transactions on Parallel and Distributed Systems.",
            "Ahmed, M. et al. (2016). A Survey of Network Anomaly Detection Techniques. Journal of Network and Computer Applications.",
            "Aggarwal, C.C. (2017). Outlier Analysis. Springer."
        ],
        burden_holder="Incident response",
        adversary_position="Correlation may be confounded by unrelated simultaneous events.",
        counter_arguments=[
            "Spurious correlations.",
            "Timestamp drift.",
            "Lack of context.",
            "Graph complexity.",
            "Documentation burden."
        ],
        resolution_strategy="Validate correlations with domain experts; automate context enrichment.",
        entity_scope="All engines",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Steinder & Sethi, 2004"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ANOMALY_CORRELATION
    ),
    DoctrineBlock(
        topic="Root Cause Inference from Anomaly Patterns",
        keywords=["root cause", "anomaly pattern", "inference", "causal analysis", "diagnosis"],
        conclusion_template="Infer root causes from anomaly patterns using causal analysis and dependency graphs. Prioritize causes affecting multiple metrics or engines.",
        reasoning_framework=(
            "Aggregate anomaly events by time and context. "
            "Construct dependency graphs of metrics and engines. "
            "Apply causal inference methods (e.g., Granger causality, Bayesian networks) to identify likely root causes. "
            "Prioritize causes that explain multiple anomalies. "
            "Validate findings with operational data and domain experts. "
            "Document all inference steps and outcomes. "
            "Reference: Pearl, J. (2009). Causality: Models, Reasoning, and Inference."
        ),
        key_factors=[
            "Dependency graph accuracy",
            "Causal inference method",
            "Validation process",
            "Prioritization criteria",
            "Documentation"
        ],
        primary_authority=[
            "Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press.",
            "Steinder, M., & Sethi, A.S. (2004). Fault Localization in Distributed Systems. IEEE Transactions on Parallel and Distributed Systems.",
            "Ahmed, M. et al. (2016). A Survey of Network Anomaly Detection Techniques."
        ],
        burden_holder="Incident analyst",
        adversary_position="Causal inference may be confounded by unobserved variables.",
        counter_arguments=[
            "Unobserved confounders.",
            "Graph construction complexity.",
            "Validation requires expertise.",
            "Prioritization may be subjective.",
            "Documentation overhead."
        ],
        resolution_strategy="Iterate with domain experts; automate graph construction.",
        entity_scope="All engines",
        confidence=0.89,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "Pearl, 2009"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.ROOT_CAUSE_INFERENCE
    ),
    DoctrineBlock(
        topic="Anomaly Severity Classification",
        keywords=["anomaly severity", "classification", "impact", "priority", "alerting"],
        conclusion_template="Classify anomalies by severity based on impact and likelihood. Use multi-factor scoring to prioritize response.",
        reasoning_framework=(
            "Define severity levels (e.g., critical, major, minor) based on impact metrics (e.g., SLA breach, user impact). "
            "Score anomalies using multiple factors: magnitude, duration, affected entities, recurrence. "
            "Assign severity based on aggregate score. "
            "Prioritize response to high-severity anomalies. "
            "Document all severity assignments and response actions. "
            "Reference: Kim, S. et al. (2018). Reducing Alert Fatigue in IT Operations."
        ),
        key_factors=[
            "Severity definition",
            "Scoring factors",
            "Assignment process",
            "Response prioritization",
            "Documentation"
        ],
        primary_authority=[
            "Kim, S. et al. (2018). Reducing Alert Fatigue in IT Operations. IEEE Cloud Computing.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley."
        ],
        burden_holder="Incident manager",
        adversary_position="Severity scoring may be subjective and inconsistent.",
        counter_arguments=[
            "Subjectivity in scoring.",
            "Inconsistent assignments.",
            "Over-prioritization of minor events.",
            "Documentation burden.",
            "Response delays."
        ],
        resolution_strategy="Standardize scoring criteria; automate assignments.",
        entity_scope="All engines",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Kim et al., 2018"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.ANOMALY_SEVERITY
    ),
    DoctrineBlock(
        topic="Trending vs Sudden Anomalies",
        keywords=["trending anomaly", "sudden anomaly", "drift", "change detection", "alerting"],
        conclusion_template="Distinguish between trending and sudden anomalies to tailor response strategies. Trending anomalies indicate gradual drift; sudden anomalies require immediate attention.",
        reasoning_framework=(
            "Analyze time-series data for both gradual and abrupt changes. "
            "Apply trend detection methods (e.g., moving average, regression) for trending anomalies. "
            "Use change point detection (e.g., CUSUM, Page-Hinkley) for sudden anomalies. "
            "Classify anomalies based on rate of change and duration. "
            "Prioritize immediate investigation for sudden anomalies. "
            "Document all detected trends and change points. "
            "Reference: Adams, R.P., & MacKay, D.J.C. (2007). Bayesian Online Changepoint Detection."
        ),
        key_factors=[
            "Trend detection method",
            "Change point algorithm",
            "Classification criteria",
            "Response prioritization",
            "Documentation"
        ],
        primary_authority=[
            "Adams, R.P., & MacKay, D.J.C. (2007). Bayesian Online Changepoint Detection.",
            "Page, E.S. (1954). Continuous Inspection Schemes. Biometrika.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley."
        ],
        burden_holder="Monitoring team",
        adversary_position="Trending anomalies may be overlooked if thresholds are too high.",
        counter_arguments=[
            "Threshold sensitivity.",
            "Trend misclassification.",
            "Delayed detection.",
            "Documentation burden.",
            "Response prioritization errors."
        ],
        resolution_strategy="Review thresholds regularly; automate trend classification.",
        entity_scope="All engines",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Adams & MacKay, 2007"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.TRENDING_ANOMALY
    ),
    DoctrineBlock(
        topic="Phantom Load Detection",
        keywords=["phantom load", "resource usage", "baseline", "anomaly", "hidden process"],
        conclusion_template="Detect phantom load by comparing observed resource usage to expected baselines. Investigate unexplained increases for hidden processes or leaks.",
        reasoning_framework=(
            "Establish expected resource usage baselines for each engine. "
            "Monitor for unexplained increases in CPU, memory, or I/O. "
            "Correlate with known workload and scheduled tasks. "
            "Flag deviations as potential phantom load. "
            "Investigate for hidden processes, memory leaks, or configuration drift. "
            "Document all findings and remediation steps. "
            "Reference: Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems."
        ),
        key_factors=[
            "Baseline accuracy",
            "Correlation with workload",
            "Investigation process",
            "Remediation documentation",
            "Detection frequency"
        ],
        primary_authority=[
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="Operations engineer",
        adversary_position="Phantom load may be intermittent and hard to reproduce.",
        counter_arguments=[
            "Intermittent issues.",
            "Baseline drift.",
            "Hidden processes evade detection.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Automate baseline comparison; schedule periodic resource audits.",
        entity_scope="All engines",
        confidence=0.88,
        confidence_zone=ConfidenceZone.AGGRESSIVE,
        controlling_precedent=[
            "Sculley et al., 2015"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.PHANTOM_LOAD
    ),
    DoctrineBlock(
        topic="Resource Leak Pattern Detection",
        keywords=["resource leak", "pattern", "memory", "file handle", "connection"],
        conclusion_template="Detect resource leaks by monitoring for monotonically increasing resource usage over time. Use statistical tests to confirm non-random growth.",
        reasoning_framework=(
            "Monitor resource usage metrics (e.g., memory, file handles, connections) over time. "
            "Apply monotonicity tests and trend analysis to detect persistent increases. "
            "Correlate with deployment events and workload changes. "
            "Flag sustained upward trends as potential leaks. "
            "Document all detected leaks and remediation actions. "
            "Reference: Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems."
        ),
        key_factors=[
            "Metric selection",
            "Trend detection method",
            "Correlation with events",
            "Remediation documentation",
            "Detection frequency"
        ],
        primary_authority=[
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="DevOps",
        adversary_position="Trend may be confounded by legitimate workload growth.",
        counter_arguments=[
            "Workload growth confounds detection.",
            "Metric selection bias.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Correlate with workload metrics; automate trend analysis.",
        entity_scope="All engines",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Sculley et al., 2015"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.RESOURCE_LEAK
    ),
    DoctrineBlock(
        topic="Memory Growth Analysis",
        keywords=["memory growth", "analysis", "trend", "leak", "baseline"],
        conclusion_template="Analyze memory usage trends to detect abnormal growth. Compare to baseline and correlate with application changes.",
        reasoning_framework=(
            "Collect memory usage metrics over time. "
            "Establish baseline from historical data. "
            "Apply trend analysis (e.g., linear regression) to detect upward drift. "
            "Correlate with application deployments and configuration changes. "
            "Flag sustained growth exceeding baseline as potential memory leak. "
            "Document all findings and remediation actions. "
            "Reference: Jain, R. (1991). The Art of Computer Systems Performance Analysis."
        ),
        key_factors=[
            "Baseline accuracy",
            "Trend detection method",
            "Correlation with changes",
            "Remediation documentation",
            "Detection frequency"
        ],
        primary_authority=[
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="DevOps",
        adversary_position="Memory growth may be workload-driven rather than anomalous.",
        counter_arguments=[
            "Workload-driven growth.",
            "Baseline drift.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Correlate with workload metrics; automate trend analysis.",
        entity_scope="All engines",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jain, 1991"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.MEMORY_GROWTH
    ),
    DoctrineBlock(
        topic="Connection Pool Drift Detection",
        keywords=["connection pool", "drift", "resource usage", "baseline", "anomaly"],
        conclusion_template="Monitor connection pool usage for drift from baseline. Investigate sustained increases for leaks or configuration issues.",
        reasoning_framework=(
            "Collect connection pool usage metrics over time. "
            "Establish baseline from historical data. "
            "Monitor for sustained increases above baseline. "
            "Correlate with application changes and workload. "
            "Flag persistent drift as potential leak or misconfiguration. "
            "Document all findings and remediation actions. "
            "Reference: Jain, R. (1991). The Art of Computer Systems Performance Analysis."
        ),
        key_factors=[
            "Baseline accuracy",
            "Correlation with changes",
            "Detection frequency",
            "Remediation documentation",
            "Metric selection"
        ],
        primary_authority=[
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="Database administrator",
        adversary_position="Workload changes may explain pool drift.",
        counter_arguments=[
            "Workload-driven drift.",
            "Baseline drift.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Correlate with workload metrics; automate drift detection.",
        entity_scope="All engines with connection pools",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jain, 1991"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.CONNECTION_POOL_DRIFT
    ),
    DoctrineBlock(
        topic="Cache Hit Rate Degradation",
        keywords=["cache hit rate", "degradation", "drift", "performance", "anomaly"],
        conclusion_template="Monitor cache hit rates for degradation. Investigate sustained decreases for configuration or workload issues.",
        reasoning_framework=(
            "Collect cache hit rate metrics over time. "
            "Establish baseline from historical data. "
            "Monitor for sustained decreases below baseline. "
            "Correlate with application changes and workload. "
            "Flag persistent degradation as potential configuration or workload issue. "
            "Document all findings and remediation actions. "
            "Reference: Jain, R. (1991). The Art of Computer Systems Performance Analysis."
        ),
        key_factors=[
            "Baseline accuracy",
            "Detection frequency",
            "Correlation with changes",
            "Remediation documentation",
            "Metric selection"
        ],
        primary_authority=[
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="Cache administrator",
        adversary_position="Workload changes may explain hit rate degradation.",
        counter_arguments=[
            "Workload-driven degradation.",
            "Baseline drift.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Correlate with workload metrics; automate degradation detection.",
        entity_scope="All engines with caches",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jain, 1991"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.CACHE_HIT_DRIFT
    ),
    DoctrineBlock(
        topic="API Latency Distribution Shift",
        keywords=["API latency", "distribution shift", "drift", "performance", "anomaly"],
        conclusion_template="Monitor API latency distributions for shifts. Use statistical tests to detect significant changes.",
        reasoning_framework=(
            "Collect API latency metrics over time. "
            "Compute summary statistics and compare to historical baselines. "
            "Apply statistical tests (e.g., KS test) to detect distributional shifts. "
            "Flag significant changes for investigation. "
            "Correlate with application changes and workload. "
            "Document all findings and remediation actions. "
            "Reference: Jain, R. (1991). The Art of Computer Systems Performance Analysis."
        ),
        key_factors=[
            "Baseline accuracy",
            "Test selection",
            "Detection frequency",
            "Correlation with changes",
            "Remediation documentation"
        ],
        primary_authority=[
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill.",
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS."
        ],
        burden_holder="API owner",
        adversary_position="Workload changes may explain latency shifts.",
        counter_arguments=[
            "Workload-driven shifts.",
            "Baseline drift.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Correlate with workload metrics; automate shift detection.",
        entity_scope="All engines with APIs",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Jain, 1991"
        ],
        position_zone=PositionZone.REPORTING,
        issue_category=IssueCategory.API_LATENCY_DRIFT
    ),
    DoctrineBlock(
        topic="Data Quality Drift Indicators",
        keywords=["data quality", "drift", "indicator", "metric", "anomaly"],
        conclusion_template="Monitor data quality metrics for drift. Flag significant changes for investigation.",
        reasoning_framework=(
            "Define data quality metrics (e.g., completeness, consistency, accuracy). "
            "Monitor metrics over time and compare to historical baselines. "
            "Flag significant deviations as potential drift. "
            "Correlate with upstream data changes. "
            "Document all findings and remediation actions. "
            "Reference: Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems."
        ),
        key_factors=[
            "Metric selection",
            "Baseline accuracy",
            "Detection frequency",
            "Correlation with changes",
            "Remediation documentation"
        ],
        primary_authority=[
            "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.",
            "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.",
            "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill."
        ],
        burden_holder="Data engineer",
        adversary_position="Metric selection may miss important quality issues.",
        counter_arguments=[
            "Metric selection bias.",
            "Baseline drift.",
            "False positives from transient spikes.",
            "Documentation burden.",
            "Remediation delays."
        ],
        resolution_strategy="Review metrics regularly; automate drift detection.",
        entity_scope="All engines with data quality metrics",
        confidence=0.87,
        confidence_zone=ConfidenceZone.DISCLOSURE,
        controlling_precedent=[
            "Sculley et al., 2015"
        ],
        position_zone=PositionZone.AUDIT,
        issue_category=IssueCategory.DATA_QUALITY_DRIFT
    ),
    # ... (Add at least 10 more DoctrineBlock instances with real content for full coverage)
]

# Authority Hardening

AUTHORITY_WEIGHTS: Dict[str, float] = {
    "Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly Detection: A Survey. ACM Computing Surveys.": 1.0,
    "Barnett, V., & Lewis, T. (1994). Outliers in Statistical Data. Wiley.": 0.9,
    "Aggarwal, C.C. (2017). Outlier Analysis. Springer.": 0.9,
    "Tukey, J.W. (1977). Exploratory Data Analysis.": 1.0,
    "Liu, F.T., Ting, K.M., & Zhou, Z.-H. (2008). Isolation Forest. ICDM.": 1.0,
    "Hariri, S. et al. (2019). Extended Isolation Forest. IEEE Transactions on Knowledge and Data Engineering.": 0.9,
    "Adams, R.P., & MacKay, D.J.C. (2007). Bayesian Online Changepoint Detection.": 1.0,
    "Basseville, M., & Nikiforov, I.V. (1993). Detection of Abrupt Changes: Theory and Application. Prentice Hall.": 1.0,
    "Page, E.S. (1954). Continuous Inspection Schemes. Biometrika.": 0.9,
    "Jain, R. (1991). The Art of Computer Systems Performance Analysis. Wiley.": 1.0,
    "Guo, C. et al. (2017). On Calibration of Modern Neural Networks. ICML.": 1.0,
    "Kullback, S., & Leibler, R.A. (1951). On Information and Sufficiency. Annals of Mathematical Statistics.": 1.0,
    "Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. NIPS.": 1.0,
    "Ahmed, M. et al. (2016). A Survey of Network Anomaly Detection Techniques. Journal of Network and Computer Applications.": 1.0,
    "Kim, S. et al. (2018). Reducing Alert Fatigue in IT Operations. IEEE Cloud Computing.": 1.0,
    "Steinder, M., & Sethi, A.S. (2004). Fault Localization in Distributed Systems. IEEE Transactions on Parallel and Distributed Systems.": 1.0,
    "Pearl, J. (2009). Causality: Models, Reasoning, and Inference. Cambridge University Press.": 1.0,
    "Hyndman, R.J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice. OTexts.": 1.0,
    "Cleveland, R.B. et al. (1990). STL: A Seasonal-Trend Decomposition Procedure. Journal of Official Statistics.": 0.9,
    "Papoulis, A. (1991). Probability, Random Variables, and Stochastic Processes. McGraw-Hill.": 0.9,
    # ... extend as needed
}

def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    max_weight = -1
    selected = ""
    for auth in authorities:
        weight = AUTHORITY_WEIGHTS.get(auth, 0.5)
        if weight > max_weight:
            max_weight = weight
            selected = auth
    return selected, max_weight

# Semantic Normalization

SEMANTIC_MAP: Dict[str, str] = {
    "outlier": "anomaly",
    "drift": "distribution shift",
    "CUSUM": "cumulative sum control chart",
    "SLA": "service level agreement",
    "baseline": "reference window",
    "IQR": "interquartile range",
    "KS test": "Kolmogorov-Smirnov test",
    "memory leak": "resource leak",
    "root cause": "primary cause",
    "alert": "notification",
    "event": "incident",
    "trend": "pattern",
    "fingerprint": "behavioral profile",
    "quality": "output quality",
    "confidence": "certainty",
    "degradation": "performance loss",
    "phantom load": "unexplained resource usage",
    "cache": "temporary storage",
    "connection pool": "resource pool",
    "API": "application programming interface",
    "seasonality": "periodic pattern",
    "audit": "review",
    "incident": "issue",
    "metric": "measurement",
    "test": "statistical test",
    "severity": "impact level",
    "classification": "categorization",
    "correlation": "relationship",
    "detection": "identification",
    "documentation": "record keeping",
    "remediation": "corrective action",
    # ... extend to 30+ mappings
}

def semantic_normalize(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# Epistemic Guardrails

BANNED_PHRASES = [
    "always",
    "never",
    "cannot fail",
    "guaranteed",
    "impossible",
    "perfect",
    "no risk",
    "certainly",
    "absolutely",
    "flawless",
    "undetectable",
    "infallible",
    "foolproof",
    "without exception",
    "no uncertainty",
    "error-free",
    "100% accurate"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# Fact Fragility Scoring

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in AUTHORITY_WEIGHTS) else 0.5
    recharacterization_risk = 0.2 if "baseline" in fact or "trend" in fact else 0.7
    testimony_dependence = 0.3 if "document" in fact or "record" in fact else 0.7
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# Three Layer Response

def doctrine_cache_layer(query: QueryRequest) -> List[DoctrineBlock]:
    hits = []
    for db in DOCTRINE_CACHE:
        if any(k in query.scenario.lower() for k in db.keywords):
            hits.append(db)
    return hits

def semantic_search_layer(query: QueryRequest) -> List[DoctrineBlock]:
    hits = []
    for db in DOCTRINE_CACHE:
        for kw in db.keywords:
            if kw.lower() in query.scenario.lower():
                hits.append(db)
                break
    return hits

def deep_analysis_layer(query: QueryRequest) -> List[DoctrineBlock]:
    # For demonstration, return all doctrines with matching issue_category in scenario
    hits = []
    for db in DOCTRINE_CACHE:
        if db.issue_category.value.lower() in query.scenario.lower():
            hits.append(db)
    return hits

# Deep Analysis

def multi_doctrine_decomposition(doctrines: List[DoctrineBlock], query: QueryRequest) -> Dict[str, Any]:
    dag = {}
    for db in doctrines:
        dag[db.topic] = {
            "dependencies": [a for a in db.primary_authority],
            "counter_arguments": db.counter_arguments,
            "resolution": db.resolution_strategy
        }
    # 8-step resolution (simplified)
    steps = [
        "Aggregate relevant doctrines",
        "Extract key factors",
        "Assess authority weights",
        "Identify counter-arguments",
        "Apply semantic normalization",
        "Score fact fragility",
        "Resolve conflicts",
        "Synthesize conclusion"
    ]
    return {
        "interaction_dag": dag,
        "resolution_steps": steps
    }

# Coverage Map

def coverage_map(query: QueryRequest, doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    triggered = [db.topic for db in doctrines]
    missed = [db.topic for db in DOCTRINE_CACHE if db not in doctrines]
    epistemic_gap = len(missed) / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

# Drift Watcher

def drift_watcher(query: QueryRequest, doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    # For demonstration, check for "drift" in scenario
    drift_detected = "drift" in query.scenario.lower()
    baseline_comparison = "baseline" in query.scenario.lower()
    return {
        "drift_detected": drift_detected,
        "baseline_comparison": baseline_comparison,
        "doctrines_considered": [db.topic for db in doctrines]
    }

# Audit Trail

AUDIT_LOG_PATH = Path(__file__).parent / "drift_anomaly_audit.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit(query_id: str, request: QueryRequest, response: QueryResponse):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "request": request.dict(),
        "response": response.dict()
    }
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

# Determinism Hash

def compute_determinism_hash(response: QueryResponse) -> str:
    m = hashlib.sha256()
    canonical = json.dumps(response.dict(), sort_keys=True).encode("utf-8")
    m.update(canonical)
    return m.hexdigest()

# FastAPI App

app = FastAPI(title="Drift Anomaly Detector", version="1.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    logger.info("Drift Anomaly Detector started on port 8753")

@app.get("/health")
def health():
    return {"status": "ok", "engine_id": "GS03", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
def coverage():
    # Return doctrine coverage stats
    return {
        "doctrine_count": len(DOCTRINE_CACHE),
        "topics": [db.topic for db in DOCTRINE_CACHE]
    }

@app.get("/drift")
def drift():
    # Return drift-related doctrine topics
    return {
        "drift_doctrines": [db.topic for db in DOCTRINE_CACHE if "drift" in db.keywords]
    }

@app.get("/doctrines")
def doctrines():
    # Return all doctrines
    return [
        {
            "topic": db.topic,
            "keywords": db.keywords,
            "confidence": db.confidence,
            "confidence_zone": db.confidence_zone.value,
            "position_zone": db.position_zone.value,
            "issue_category": db.issue_category.value
        }
        for db in DOCTRINE_CACHE
    ]

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        # Layer 1: Doctrine cache
        doctrine_hits = doctrine_cache_layer(request)
        # Layer 2: Semantic search
        if not doctrine_hits:
            doctrine_hits = semantic_search_layer(request)
        # Layer 3: Deep analysis
        if not doctrine_hits:
            doctrine_hits = deep_analysis_layer(request)
        if not doctrine_hits:
            raise HTTPException(status_code=404, detail="No relevant doctrines found")

        # Multi-doctrine decomposition
        analysis = multi_doctrine_decomposition(doctrine_hits, request)
        # Coverage map
        coverage = coverage_map(request, doctrine_hits)
        # Drift watcher
        drift_info = drift_watcher(request, doctrine_hits)

        # Synthesize conclusion
        primary = doctrine_hits[0]
        conclusion = apply_epistemic_guardrails(semantic_normalize(primary.conclusion_template))
        reasoning = apply_epistemic_guardrails(semantic_normalize(primary.reasoning_framework))
        key_factors = [semantic_normalize(f) for f in primary.key_factors]
        primary_authority = primary.primary_authority
        counter_arguments = [semantic_normalize(ca) for ca in primary.counter_arguments]
        resolution_strategy = semantic_normalize(primary.resolution_strategy)
        confidence = primary.confidence
        confidence_zone = primary.confidence_zone
        position_zone = primary.position_zone

        # Fact fragility scoring
        fragility = score_fact_fragility(conclusion)
        # Determinism hash
        response = QueryResponse(
            engine_id="GS03",
            query_id=query_id,
            mode=request.mode,
            confidence=confidence,
            confidence_zone=confidence_zone,
            position_zone=position_zone,
            primary_conclusion=conclusion,
            reasoning_framework=reasoning,
            key_factors=key_factors,
            primary_authority=primary_authority,
            counter_arguments=counter_arguments,
            resolution_strategy=resolution_strategy,
            determinism_hash=""
        )
        response.determinism_hash = compute_determinism_hash(response)
        # Audit log
        log_audit(query_id, request, response)
        # Metrics
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query(query_id, [primary.topic], latency)
        return response
    except Exception as e:
        logger.exception(f"Error in /query: {e}")
        metrics_collector.record_error(query_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))
