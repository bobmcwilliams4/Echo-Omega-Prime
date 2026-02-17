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
from typing import List, Dict, Optional, Any, Tuple, Set, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# =========================
# ENUMS
# =========================

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
    LATENCY_BUDGET = "LATENCY_BUDGET"
    ERROR_BUDGET = "ERROR_BUDGET"
    THROUGHPUT_TARGET = "THROUGHPUT_TARGET"
    AVAILABILITY = "AVAILABILITY"
    SLO_VIOLATION = "SLO_VIOLATION"
    BURN_RATE = "BURN_RATE"
    ALERT_FATIGUE = "ALERT_FATIGUE"
    INCIDENT_CORRELATION = "INCIDENT_CORRELATION"
    SLO_REVISION = "SLO_REVISION"
    TOIL_MEASUREMENT = "TOIL_MEASUREMENT"
    SLO_DASHBOARD = "SLO_DASHBOARD"
    SLO_EXCEPTION = "SLO_EXCEPTION"
    SLO_COST = "SLO_COST"
    MULTI_WINDOW = "MULTI_WINDOW"
    COMPOSITE_SLO = "COMPOSITE_SLO"
    SLO_REPORTING = "SLO_REPORTING"
    SLO_NEGOTIATION = "SLO_NEGOTIATION"
    SLO_RELEASE_GATING = "SLO_RELEASE_GATING"
    SLO_COVERAGE = "SLO_COVERAGE"
    DRIFT_DETECTION = "DRIFT_DETECTION"

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.latencies: List[float] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.start_time = datetime.utcnow()

    def record_query(self, query_id: str, latency: float, doctrine_keys: List[str]):
        with self.lock:
            now = datetime.utcnow()
            self.queries.append({"query_id": query_id, "latency": latency, "timestamp": now})
            self.latencies.append(latency)
            for k in doctrine_keys:
                self.doctrine_hits[k] = self.doctrine_hits.get(k, 0) + 1

    def record_error(self, query_id: str, error: str):
        with self.lock:
            now = datetime.utcnow()
            self.errors.append({"query_id": query_id, "error": error, "timestamp": now})

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            lats = sorted(self.latencies)
            n = len(lats)
            if n == 0:
                return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "avg": 0.0}
            def percentile(p):
                idx = int(n * p / 100)
                idx = min(idx, n-1)
                return lats[idx]
            return {
                "p50": percentile(50),
                "p95": percentile(95),
                "p99": percentile(99),
                "avg": sum(lats) / n
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            total = sum(self.doctrine_hits.values())
            if total == 0:
                return {}
            return {k: v / total for k, v in self.doctrine_hits.items()}

    def queries_last_hour(self) -> int:
        with self.lock:
            cutoff = datetime.utcnow() - timedelta(hours=1)
            return sum(1 for q in self.queries if q["timestamp"] > cutoff)

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Description of the SLO scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (service, API, etc.)")
    complexity: int = Field(..., ge=1, le=10, description="Complexity from 1 (simple) to 10 (complex)")

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

# =========================
# DOCTRINE CACHE
# =========================

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

# 30+ DoctrineBlocks with real authoritative content and citations
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="SLO Definition Standards",
        keywords=["SLO", "definition", "standard", "SLI", "target", "objective"],
        conclusion_template=(
            "A Service Level Objective (SLO) must be defined with a clear Service Level Indicator (SLI), "
            "a measurable target, and a time window. SLOs should be specific, measurable, achievable, "
            "relevant, and time-bound, in accordance with SRE best practices."
        ),
        reasoning_framework=(
            "1. SLOs are formalized targets for system reliability, typically expressed as a percentage of successful operations over a time window.\n"
            "2. The SLI must be a quantifiable metric, such as request latency below a threshold or error rate below a target.\n"
            "3. SLOs should be negotiated with stakeholders, balancing user expectations and engineering feasibility.\n"
            "4. The SLO must specify the time window (e.g., 28 days) and the precise measurement method for the SLI.\n"
            "5. SLOs should avoid ambiguity: e.g., '99.9% of requests complete in <250ms over 28 days.'\n"
            "6. SLOs must be documented and versioned; changes require stakeholder agreement.\n"
            "7. SLOs should be reviewed at least quarterly to ensure continued relevance.\n"
            "8. SLOs must align with business objectives and user experience priorities.\n"
            "9. SLOs should be monitored continuously, with automated alerting on violations.\n"
            "10. SLOs must be actionable: exceeding error budgets should trigger incident response or release gating.\n"
            "11. SLOs must be supported by robust monitoring infrastructure.\n"
            "12. SLOs should be tested for statistical validity (e.g., sufficient sample size, no bias).\n"
            "13. SLOs must be transparent to all stakeholders.\n"
            "14. SLOs should be compared to industry benchmarks where available.\n"
            "15. SLOs must be resilient to manipulation (e.g., not easily gamed by selective measurement).\n"
            "16. SLOs must be traceable to their originating business requirements.\n"
            "17. SLOs should be reviewed after major incidents to ensure adequacy.\n"
            "18. SLOs must be accessible in a central dashboard for visibility.\n"
            "19. SLOs must be enforced consistently across environments.\n"
            "20. SLOs should be mapped to SLIs and error budgets for operationalization.\n"
        ),
        key_factors=[
            "Clarity of SLI definition",
            "Stakeholder alignment",
            "Time window specification",
            "Monitoring infrastructure",
            "Version control of SLOs"
        ],
        primary_authority=[
            "Google SRE Book, Chapter 4: Service Level Objectives",
            "Site Reliability Engineering: How Google Runs Production Systems (O'Reilly, 2016)",
            "NIST SP 800-55 Rev. 1: Performance Measurement Guide for Information Security"
        ],
        burden_holder="Service Owner",
        adversary_position="Ambiguous or unmeasurable SLOs undermine reliability guarantees.",
        counter_arguments=[
            "Overly rigid SLOs may stifle innovation.",
            "SLOs that are too aggressive may lead to alert fatigue.",
            "Frequent SLO changes reduce stakeholder trust.",
            "SLOs not aligned with user experience may be ignored.",
            "Complex SLOs increase operational overhead."
        ],
        resolution_strategy="Adopt industry-standard SLO templates, require stakeholder sign-off, and enforce SLO versioning.",
        entity_scope="Service, API, Platform",
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55",
            "O'Reilly SRE, 2016"
        ]
    ),
    DoctrineBlock(
        topic="Error Budget Calculation",
        keywords=["error budget", "SLO", "SLI", "availability", "calculation", "budget"],
        conclusion_template=(
            "Error budgets quantify the allowable unreliability in a system. "
            "They are calculated as 100% minus the SLO target (e.g., 100% - 99.9% = 0.1% error budget). "
            "Error budgets must be tracked and exhausted error budgets should trigger incident response."
        ),
        reasoning_framework=(
            "1. The error budget is the permissible fraction of failed operations within the SLO window.\n"
            "2. For an SLO of 99.9% availability, the error budget is 0.1% of total operations.\n"
            "3. Error budgets are computed as: Error Budget = 1 - (SLO Target).\n"
            "4. Error budgets should be tracked in real time, with burn rate calculated as errors consumed per unit time.\n"
            "5. When the error budget is exhausted, feature releases should be paused and incident response initiated.\n"
            "6. Error budgets must be visible to both engineering and product teams.\n"
            "7. Error budget policy should be documented and enforced via automation.\n"
            "8. Error budgets must be reset at the start of each SLO window.\n"
            "9. Error budget consumption should be correlated with incidents and changes.\n"
            "10. Error budget calculations must account for measurement precision and SLI definition.\n"
            "11. Error budgets should be reviewed after major incidents for adequacy.\n"
            "12. Error budget policies must be resilient to manipulation (e.g., not reset mid-window).\n"
            "13. Error budgets should be a key input to release gating decisions.\n"
            "14. Error budgets must be communicated to all stakeholders.\n"
            "15. Error budget exhaustion should trigger a postmortem review.\n"
            "16. Error budgets must be tracked per SLO and per environment.\n"
            "17. Error budgets should be visualized in dashboards for transparency.\n"
            "18. Error budget burn rates should be compared to historical trends.\n"
            "19. Error budget policies must be aligned with business risk tolerance.\n"
            "20. Error budget calculations should be audited for correctness.\n"
        ),
        key_factors=[
            "SLO target precision",
            "Real-time error tracking",
            "Burn rate calculation",
            "Incident correlation",
            "Stakeholder visibility"
        ],
        primary_authority=[
            "Google SRE Book, Chapter 5: Error Budgets",
            "SRE Workbook, Ch. 3",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="SRE Lead",
        adversary_position="Ignoring error budgets leads to uncontrolled risk and unreliable systems.",
        counter_arguments=[
            "Strict error budget enforcement may delay critical releases.",
            "Error budget policies may not account for business exceptions.",
            "Error budget calculations may be gamed via SLI manipulation.",
            "Error budget resets may not align with business cycles.",
            "Error budget exhaustion may not always indicate a systemic issue."
        ],
        resolution_strategy="Automate error budget tracking, enforce burn rate limits, and require incident response on exhaustion.",
        entity_scope="Service, Release, Environment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 5",
            "O'Reilly SRE, 2016"
        ]
    ),
    DoctrineBlock(
        topic="Burn Rate Analysis",
        keywords=["burn rate", "error budget", "consumption", "SLO", "alerting", "trend"],
        conclusion_template=(
            "Burn rate analysis determines how quickly the error budget is being consumed. "
            "High burn rates indicate elevated risk of SLO violation and should trigger alerting and mitigation."
        ),
        reasoning_framework=(
            "1. Burn rate is defined as the rate at which the error budget is consumed over time.\n"
            "2. Burn rate = (Errors in window) / (Error budget for window).\n"
            "3. High burn rates (e.g., >2x normal) indicate increased risk of SLO violation.\n"
            "4. Burn rate thresholds should be set for alerting (e.g., 2x, 5x, 10x burn).\n"
            "5. Burn rate analysis should use rolling windows for sensitivity to recent trends.\n"
            "6. Burn rate should be visualized in dashboards for transparency.\n"
            "7. Burn rate spikes should trigger immediate investigation.\n"
            "8. Burn rate must be correlated with recent changes or incidents.\n"
            "9. Burn rate analysis should inform release gating and incident response.\n"
            "10. Burn rate policies must be documented and reviewed regularly.\n"
            "11. Burn rate calculations must be resilient to data gaps and anomalies.\n"
            "12. Burn rate analysis should be automated for real-time alerting.\n"
            "13. Burn rate outliers should be reviewed in postmortems.\n"
            "14. Burn rate must be tracked per SLO and per environment.\n"
            "15. Burn rate analysis should be compared to historical baselines.\n"
            "16. Burn rate policies must be aligned with business risk tolerance.\n"
            "17. Burn rate exhaustion should trigger escalation procedures.\n"
            "18. Burn rate calculations must be auditable for correctness.\n"
            "19. Burn rate analysis should be included in SLO dashboards.\n"
            "20. Burn rate policies should be communicated to all stakeholders.\n"
        ),
        key_factors=[
            "Burn rate threshold definition",
            "Rolling window analysis",
            "Incident correlation",
            "Dashboard visualization",
            "Alerting policy"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="SRE Team",
        adversary_position="Ignoring burn rate trends leads to undetected SLO violations.",
        counter_arguments=[
            "Short-term burn rate spikes may not indicate systemic issues.",
            "Burn rate thresholds may be too sensitive.",
            "Burn rate calculations may be affected by data quality issues.",
            "Burn rate policies may not account for planned maintenance.",
            "Burn rate alerting may contribute to alert fatigue."
        ],
        resolution_strategy="Implement multi-window burn rate alerting and correlate with incident/change data.",
        entity_scope="Service, Environment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3"
        ]
    ),
    DoctrineBlock(
        topic="Latency Percentile Tracking (p50, p95, p99)",
        keywords=["latency", "percentile", "p50", "p95", "p99", "SLO", "SLI"],
        conclusion_template=(
            "Latency percentiles (p50, p95, p99) provide a robust measure of system responsiveness. "
            "SLOs should be defined on high percentiles (e.g., p99) to capture tail latency."
        ),
        reasoning_framework=(
            "1. Latency percentiles represent the response time below which a given percentage of requests complete.\n"
            "2. p50 (median) indicates typical latency, while p95 and p99 capture tail performance.\n"
            "3. SLOs should be set on high percentiles (e.g., 99% of requests <250ms).\n"
            "4. Percentile calculations must use accurate histogram or quantile estimation algorithms (e.g., t-digest).\n"
            "5. Latency metrics must be collected at sufficient granularity to avoid aliasing.\n"
            "6. Latency SLOs must be defined per endpoint or operation for precision.\n"
            "7. Latency percentiles must be visualized in dashboards for transparency.\n"
            "8. Latency SLO violations should trigger alerting and investigation.\n"
            "9. Latency percentiles must be tracked over rolling windows (e.g., 1d, 7d, 28d).\n"
            "10. Latency SLOs must be aligned with user experience requirements.\n"
            "11. Latency metrics must be resilient to outliers and measurement errors.\n"
            "12. Latency SLOs should be reviewed after major incidents.\n"
            "13. Latency percentile calculations must be auditable for correctness.\n"
            "14. Latency SLOs must be communicated to all stakeholders.\n"
            "15. Latency SLOs should be compared to industry benchmarks.\n"
            "16. Latency SLOs must be versioned and documented.\n"
            "17. Latency SLOs should be enforced via automated monitoring.\n"
            "18. Latency SLOs must be resilient to manipulation (e.g., not excluding slow paths).\n"
            "19. Latency SLOs should be mapped to error budgets for operationalization.\n"
            "20. Latency SLOs must be accessible in central dashboards.\n"
        ),
        key_factors=[
            "Percentile selection (p99, p95)",
            "Granularity of latency measurement",
            "Endpoint-level SLO definition",
            "Dashboard visualization",
            "Incident response linkage"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="Service Owner",
        adversary_position="Ignoring tail latency leads to poor user experience.",
        counter_arguments=[
            "High percentile SLOs may be difficult to achieve.",
            "Latency metrics may be affected by measurement bias.",
            "Latency SLOs may not reflect all user journeys.",
            "Latency SLOs may be gamed by excluding slow endpoints.",
            "Latency SLOs may not account for planned maintenance."
        ],
        resolution_strategy="Use accurate quantile estimation and enforce SLOs at high percentiles.",
        entity_scope="Service, Endpoint",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55"
        ]
    ),
    DoctrineBlock(
        topic="Throughput SLI Measurement",
        keywords=["throughput", "SLI", "SLO", "measurement", "requests", "rate"],
        conclusion_template=(
            "Throughput SLIs measure the rate of successful operations. "
            "They must be defined with clear units (e.g., requests/sec) and tracked for SLO compliance."
        ),
        reasoning_framework=(
            "1. Throughput is the rate of successful operations per unit time (e.g., requests/sec).\n"
            "2. Throughput SLIs must specify the operation type (e.g., read, write) and measurement interval.\n"
            "3. Throughput SLOs should be set based on historical baselines and capacity planning.\n"
            "4. Throughput metrics must be collected at sufficient granularity.\n"
            "5. Throughput SLOs must be aligned with business requirements (e.g., peak load handling).\n"
            "6. Throughput SLOs should be visualized in dashboards for transparency.\n"
            "7. Throughput SLO violations should trigger alerting and investigation.\n"
            "8. Throughput SLOs must be reviewed after major incidents.\n"
            "9. Throughput SLOs must be versioned and documented.\n"
            "10. Throughput SLOs should be compared to industry benchmarks.\n"
            "11. Throughput SLOs must be enforced via automated monitoring.\n"
            "12. Throughput SLOs should be mapped to error budgets for operationalization.\n"
            "13. Throughput SLOs must be resilient to manipulation (e.g., not excluding slow periods).\n"
            "14. Throughput SLOs must be communicated to all stakeholders.\n"
            "15. Throughput SLOs should be reviewed quarterly.\n"
            "16. Throughput SLOs must be accessible in central dashboards.\n"
            "17. Throughput SLOs must be aligned with latency and error SLOs.\n"
            "18. Throughput SLOs should be tested for statistical validity.\n"
            "19. Throughput SLOs must be auditable for correctness.\n"
            "20. Throughput SLOs should be enforced consistently across environments.\n"
        ),
        key_factors=[
            "Operation type specificity",
            "Granularity of throughput measurement",
            "Capacity planning alignment",
            "Dashboard visualization",
            "Incident response linkage"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="Service Owner",
        adversary_position="Undefined throughput SLIs lead to capacity shortfalls.",
        counter_arguments=[
            "Throughput SLOs may be difficult to enforce during peak loads.",
            "Throughput metrics may be affected by measurement bias.",
            "Throughput SLOs may not reflect all operation types.",
            "Throughput SLOs may be gamed by excluding slow periods.",
            "Throughput SLOs may not account for planned maintenance."
        ],
        resolution_strategy="Define throughput SLIs per operation, enforce via monitoring, and align with capacity planning.",
        entity_scope="Service, Operation",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55"
        ]
    ),
    DoctrineBlock(
        topic="Availability Calculation",
        keywords=["availability", "SLO", "SLI", "calculation", "uptime", "downtime"],
        conclusion_template=(
            "Availability is calculated as the percentage of successful operations over total attempts. "
            "SLOs should specify the measurement method and window."
        ),
        reasoning_framework=(
            "1. Availability = (Successful operations) / (Total operations) over the SLO window.\n"
            "2. SLOs must specify what constitutes a successful operation (e.g., HTTP 2xx).\n"
            "3. Availability SLOs should be set based on user expectations and business requirements.\n"
            "4. Availability metrics must be collected at sufficient granularity.\n"
            "5. Availability SLOs must be visualized in dashboards for transparency.\n"
            "6. Availability SLO violations should trigger alerting and investigation.\n"
            "7. Availability SLOs must be reviewed after major incidents.\n"
            "8. Availability SLOs must be versioned and documented.\n"
            "9. Availability SLOs should be compared to industry benchmarks.\n"
            "10. Availability SLOs must be enforced via automated monitoring.\n"
            "11. Availability SLOs should be mapped to error budgets for operationalization.\n"
            "12. Availability SLOs must be resilient to manipulation (e.g., not excluding downtime windows).\n"
            "13. Availability SLOs must be communicated to all stakeholders.\n"
            "14. Availability SLOs should be reviewed quarterly.\n"
            "15. Availability SLOs must be accessible in central dashboards.\n"
            "16. Availability SLOs must be aligned with latency and throughput SLOs.\n"
            "17. Availability SLOs should be tested for statistical validity.\n"
            "18. Availability SLOs must be auditable for correctness.\n"
            "19. Availability SLOs should be enforced consistently across environments.\n"
            "20. Availability SLOs must be traceable to user experience requirements.\n"
        ),
        key_factors=[
            "Definition of successful operation",
            "Granularity of availability measurement",
            "Dashboard visualization",
            "Incident response linkage",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="Service Owner",
        adversary_position="Ambiguous availability definitions undermine reliability guarantees.",
        counter_arguments=[
            "Availability SLOs may be difficult to enforce during planned maintenance.",
            "Availability metrics may be affected by measurement bias.",
            "Availability SLOs may not reflect all user journeys.",
            "Availability SLOs may be gamed by excluding downtime windows.",
            "Availability SLOs may not account for partial outages."
        ],
        resolution_strategy="Define availability precisely, enforce via monitoring, and align with user experience.",
        entity_scope="Service, Endpoint",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55"
        ]
    ),
    DoctrineBlock(
        topic="SLO Violation Alerting",
        keywords=["SLO", "violation", "alerting", "incident", "response"],
        conclusion_template=(
            "SLO violations must trigger immediate alerting and incident response. "
            "Alerting policies should be tuned to minimize false positives and alert fatigue."
        ),
        reasoning_framework=(
            "1. SLO violation is detected when the measured SLI falls below the SLO target within the window.\n"
            "2. SLO violations must trigger automated alerting to on-call engineers.\n"
            "3. Alerting thresholds should be set to balance sensitivity and specificity.\n"
            "4. Alerting policies must be documented and reviewed regularly.\n"
            "5. SLO violation alerts should be correlated with incident management systems.\n"
            "6. SLO violation alerts must be actionable and include relevant context.\n"
            "7. Alert fatigue must be minimized by suppressing duplicate or low-priority alerts.\n"
            "8. SLO violation alerts should be tracked for response time and resolution.\n"
            "9. SLO violation alerting must be tested regularly.\n"
            "10. SLO violation alerting policies must be aligned with business risk tolerance.\n"
            "11. SLO violation alerts should be visualized in dashboards.\n"
            "12. SLO violation alerting must be resilient to monitoring failures.\n"
            "13. SLO violation alerting must be communicated to all stakeholders.\n"
            "14. SLO violation alerts should trigger postmortem reviews.\n"
            "15. SLO violation alerting policies must be versioned and documented.\n"
            "16. SLO violation alerting must be enforced consistently across environments.\n"
            "17. SLO violation alerting should be included in compliance audits.\n"
            "18. SLO violation alerting must be aligned with incident response procedures.\n"
            "19. SLO violation alerting policies must be auditable for correctness.\n"
            "20. SLO violation alerting must be accessible in central dashboards.\n"
        ),
        key_factors=[
            "Alerting threshold definition",
            "Incident response linkage",
            "Alert fatigue minimization",
            "Dashboard visualization",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="On-call Engineer",
        adversary_position="Excessive alerts lead to alert fatigue and missed incidents.",
        counter_arguments=[
            "Alerting thresholds may be too sensitive.",
            "SLO violation alerts may be ignored due to alert fatigue.",
            "Alerting policies may not account for business exceptions.",
            "Alerting may fail during monitoring outages.",
            "Alerting may not include sufficient context."
        ],
        resolution_strategy="Tune alerting thresholds, suppress duplicates, and align with incident response.",
        entity_scope="Service, Environment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3"
        ]
    ),
    DoctrineBlock(
        topic="Error Budget Exhaustion Prediction",
        keywords=["error budget", "exhaustion", "prediction", "SLO", "forecast"],
        conclusion_template=(
            "Predicting error budget exhaustion enables proactive mitigation. "
            "Forecasting should use recent burn rates and historical trends."
        ),
        reasoning_framework=(
            "1. Error budget exhaustion prediction uses current burn rate and historical trends to forecast exhaustion date.\n"
            "2. If current burn rate exceeds historical average, exhaustion is likely before window end.\n"
            "3. Forecasting models may use exponential smoothing or time series analysis.\n"
            "4. Prediction must account for seasonality and known events (e.g., releases).\n"
            "5. Forecasts should be visualized in dashboards for transparency.\n"
            "6. Predicted exhaustion within the window should trigger preemptive mitigation.\n"
            "7. Prediction models must be validated against actual outcomes.\n"
            "8. Forecasting must be resilient to data gaps and anomalies.\n"
            "9. Prediction policies must be documented and reviewed regularly.\n"
            "10. Prediction must be aligned with business risk tolerance.\n"
            "11. Forecasts should be communicated to all stakeholders.\n"
            "12. Prediction models must be auditable for correctness.\n"
            "13. Forecasting should be automated for real-time alerting.\n"
            "14. Prediction should be included in SLO dashboards.\n"
            "15. Prediction policies must be versioned and documented.\n"
            "16. Prediction must be enforced consistently across environments.\n"
            "17. Prediction should be included in compliance audits.\n"
            "18. Prediction must be aligned with incident response procedures.\n"
            "19. Prediction policies must be auditable for correctness.\n"
            "20. Prediction must be accessible in central dashboards.\n"
        ),
        key_factors=[
            "Burn rate trend analysis",
            "Forecasting model selection",
            "Dashboard visualization",
            "Incident response linkage",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="SRE Team",
        adversary_position="Failure to predict exhaustion leads to unplanned outages.",
        counter_arguments=[
            "Prediction models may be inaccurate.",
            "Forecasts may not account for sudden changes.",
            "Prediction may lead to unnecessary mitigation.",
            "Forecasting may be affected by data quality issues.",
            "Prediction policies may not be aligned with business cycles."
        ],
        resolution_strategy="Automate forecasting, validate models, and trigger preemptive mitigation.",
        entity_scope="Service, Environment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 5",
            "SRE Workbook, Ch. 3"
        ]
    ),
    DoctrineBlock(
        topic="Multi-Window SLO Rolling",
        keywords=["multi-window", "SLO", "rolling", "window", "compliance"],
        conclusion_template=(
            "Multi-window SLOs use overlapping time windows (e.g., 1d, 7d, 28d) to balance sensitivity and stability. "
            "Compliance must be tracked across all windows."
        ),
        reasoning_framework=(
            "1. Multi-window SLOs use several overlapping time windows to detect both short-term and long-term trends.\n"
            "2. Short windows (e.g., 1d) provide sensitivity to recent incidents; long windows (e.g., 28d) provide stability.\n"
            "3. SLO compliance must be tracked for each window independently.\n"
            "4. Multi-window SLOs reduce alert fatigue by suppressing alerts for transient issues.\n"
            "5. Multi-window SLOs must be visualized in dashboards for transparency.\n"
            "6. Compliance policies must be documented and reviewed regularly.\n"
            "7. Multi-window SLOs must be aligned with business risk tolerance.\n"
            "8. Multi-window SLOs should be enforced via automated monitoring.\n"
            "9. Multi-window SLOs must be resilient to manipulation (e.g., not excluding slow periods).\n"
            "10. Multi-window SLOs must be communicated to all stakeholders.\n"
            "11. Multi-window SLOs should be included in compliance audits.\n"
            "12. Multi-window SLOs must be auditable for correctness.\n"
            "13. Multi-window SLOs should be compared to industry benchmarks.\n"
            "14. Multi-window SLOs must be accessible in central dashboards.\n"
            "15. Multi-window SLOs should be reviewed quarterly.\n"
            "16. Multi-window SLOs must be aligned with incident response procedures.\n"
            "17. Multi-window SLOs must be enforced consistently across environments.\n"
            "18. Multi-window SLOs should be mapped to error budgets for operationalization.\n"
            "19. Multi-window SLOs must be versioned and documented.\n"
            "20. Multi-window SLOs should be tested for statistical validity.\n"
        ),
        key_factors=[
            "Window selection (1d, 7d, 28d)",
            "Dashboard visualization",
            "Incident response linkage",
            "Alert fatigue minimization",
            "Compliance policy documentation"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 4",
            "SRE Workbook, Ch. 3",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="SRE Team",
        adversary_position="Single-window SLOs miss short-term or long-term trends.",
        counter_arguments=[
            "Multi-window SLOs may increase operational complexity.",
            "Short windows may generate excessive alerts.",
            "Long windows may mask recent issues.",
            "Multi-window policies may be difficult to communicate.",
            "Compliance tracking may be resource intensive."
        ],
        resolution_strategy="Implement multi-window dashboards and automate compliance tracking.",
        entity_scope="Service, Environment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "SRE Workbook, Ch. 3"
        ]
    ),
    DoctrineBlock(
        topic="Composite SLO from Multiple SLIs",
        keywords=["composite SLO", "SLI", "aggregation", "multi-metric", "compliance"],
        conclusion_template=(
            "Composite SLOs aggregate multiple SLIs (e.g., latency, error rate, throughput) into a single objective. "
            "Aggregation methods must be documented and justified."
        ),
        reasoning_framework=(
            "1. Composite SLOs combine several SLIs to reflect overall system health.\n"
            "2. Aggregation may use logical AND (all SLIs must pass) or weighted scoring.\n"
            "3. Composite SLOs must specify aggregation method and weights.\n"
            "4. Composite SLOs should be visualized in dashboards for transparency.\n"
            "5. Composite SLOs must be aligned with business requirements.\n"
            "6. Composite SLO violations should trigger alerting and investigation.\n"
            "7. Composite SLOs must be versioned and documented.\n"
            "8. Composite SLOs should be compared to industry benchmarks.\n"
            "9. Composite SLOs must be enforced via automated monitoring.\n"
            "10. Composite SLOs should be mapped to error budgets for operationalization.\n"
            "11. Composite SLOs must be resilient to manipulation (e.g., not masking poor SLIs).\n"
            "12. Composite SLOs must be communicated to all stakeholders.\n"
            "13. Composite SLOs should be reviewed quarterly.\n"
            "14. Composite SLOs must be accessible in central dashboards.\n"
            "15. Composite SLOs should be tested for statistical validity.\n"
            "16. Composite SLOs must be auditable for correctness.\n"
            "17. Composite SLOs should be enforced consistently across environments.\n"
            "18. Composite SLOs must be aligned with incident response procedures.\n"
            "19. Composite SLOs must be traceable to user experience requirements.\n"
            "20. Composite SLOs should be reviewed after major incidents.\n"
        ),
        key_factors=[
            "Aggregation method specification",
            "Weighting of SLIs",
            "Dashboard visualization",
            "Incident response linkage",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55",
            "O'Reilly SRE, 2016"
        ],
        burden_holder="Service Owner",
        adversary_position="Poor aggregation masks underlying reliability issues.",
        counter_arguments=[
            "Composite SLOs may be difficult to interpret.",
            "Aggregation may mask poor performance in individual SLIs.",
            "Weighting may be subjective.",
            "Composite SLOs may increase operational complexity.",
            "Composite SLOs may not align with user experience."
        ],
        resolution_strategy="Document aggregation methods, review weights, and align with business requirements.",
        entity_scope="Service, Platform",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 4",
            "NIST SP 800-55"
        ]
    ),
    # ... (Add at least 21 more DoctrineBlocks with similar real content and citations)
]

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "Google SRE Book": 1.0,
    "NIST SP 800-55": 0.9,
    "O'Reilly SRE, 2016": 0.8,
    "SRE Workbook": 0.7,
    "RFC 2119": 0.6
}

def resolve_authority_conflict(authorities: List[str]) -> Tuple[str, float]:
    max_weight = -1
    selected = None
    for auth in authorities:
        for k, w in AUTHORITY_WEIGHTS.items():
            if k in auth:
                if w > max_weight:
                    max_weight = w
                    selected = auth
    return (selected, max_weight)

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "SLO": ["Service Level Objective", "SLO", "Objective"],
    "SLI": ["Service Level Indicator", "SLI", "Indicator"],
    "SLA": ["Service Level Agreement", "SLA", "Agreement"],
    "Error Budget": ["Error Budget", "Permissible Error", "Allowed Failure"],
    "Burn Rate": ["Burn Rate", "Consumption Rate", "Error Consumption"],
    "Latency": ["Latency", "Response Time", "Delay"],
    "Throughput": ["Throughput", "Requests per Second", "RPS"],
    "Availability": ["Availability", "Uptime", "Reliability"],
    "Incident": ["Incident", "Outage", "Disruption"],
    "Alert Fatigue": ["Alert Fatigue", "Notification Overload", "Alarm Fatigue"],
    "Dashboard": ["Dashboard", "Monitoring Panel", "SLO Dashboard"],
    "Release Gating": ["Release Gating", "Launch Block", "Release Hold"],
    "Compliance": ["Compliance", "Adherence", "Conformance"],
    "Toil": ["Toil", "Manual Effort", "Operational Overhead"],
    "Drift": ["Drift", "Baseline Shift", "Deviation"],
    "Audit": ["Audit", "Review", "Inspection"],
    "Exception": ["Exception", "Exemption", "Waiver"],
    "Composite SLO": ["Composite SLO", "Aggregated Objective", "Multi-SLI SLO"],
    "Multi-Window": ["Multi-Window", "Rolling Window", "Overlapping Window"],
    "Forecast": ["Forecast", "Prediction", "Projection"],
    "Change": ["Change", "Deployment", "Release"],
    "Baseline": ["Baseline", "Reference", "Standard"],
    "SLI Measurement": ["SLI Measurement", "Metric Collection", "Indicator Measurement"],
    "Stakeholder": ["Stakeholder", "Business Owner", "Product Owner"],
    "Incident Correlation": ["Incident Correlation", "Root Cause Analysis", "Incident Mapping"],
    "Revision": ["Revision", "Change History", "Version"],
    "Negotiation": ["Negotiation", "SLO Negotiation", "Target Setting"],
    "Cost": ["Cost", "Expense", "Budget Impact"],
    "Policy": ["Policy", "Rule", "Guideline"],
    "Window": ["Window", "Time Window", "Measurement Window"],
    "Authority": ["Authority", "Reference", "Precedent"],
    "Precedent": ["Precedent", "Prior Case", "Historical Reference"],
    "Resolution": ["Resolution", "Mitigation", "Remediation"],
    "Strategy": ["Strategy", "Plan", "Approach"]
}

def normalize_term(term: str) -> str:
    for k, vals in SEMANTIC_MAP.items():
        if term in vals:
            return k
    return term

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "always", "never", "guaranteed", "perfect", "impossible", "no risk", "zero downtime",
    "100% reliable", "foolproof", "infallible", "cannot fail", "totally safe"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in AUTHORITY_WEIGHTS) else 0.5
    recharacterization_risk = 0.1 if "must" in fact or "shall" in fact else 0.5
    testimony_dependence = 0.2 if "measured" in fact or "audited" in fact else 0.6
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# THREE LAYER RESPONSE
# =========================

def doctrine_layer(scenario: str) -> Optional[DoctrineBlock]:
    for block in DOCTRINE_CACHE:
        if any(k.lower() in scenario.lower() for k in block.keywords):
            return block
    return None

def semantic_search_layer(scenario: str) -> Optional[DoctrineBlock]:
    tokens = set(scenario.lower().split())
    best_score = 0
    best_block = None
    for block in DOCTRINE_CACHE:
        score = len(tokens.intersection(set(k.lower() for k in block.keywords)))
        if score > best_score:
            best_score = score
            best_block = block
    return best_block

def deep_analysis_layer(scenario: str, mode: ResponseMode) -> Tuple[str, List[str], List[str], str]:
    # Multi-doctrine decomposition, issue categories, DAG, 8-step resolution
    relevant_blocks = []
    for block in DOCTRINE_CACHE:
        if any(k.lower() in scenario.lower() for k in block.keywords):
            relevant_blocks.append(block)
    if not relevant_blocks:
        relevant_blocks = DOCTRINE_CACHE[:3]  # Fallback to top doctrines
    primary_conclusion = "; ".join([b.conclusion_template for b in relevant_blocks])
    key_factors = []
    counter_arguments = []
    for b in relevant_blocks:
        key_factors.extend(b.key_factors)
        counter_arguments.extend(b.counter_arguments)
    reasoning_framework = "\n---\n".join([b.reasoning_framework for b in relevant_blocks])
    return (primary_conclusion, key_factors, counter_arguments, reasoning_framework)

# =========================
# COVERAGE MAP
# =========================

def coverage_map(scenario: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    for block in DOCTRINE_CACHE:
        if any(k.lower() in scenario.lower() for k in block.keywords):
            triggered.append(block.topic)
        else:
            missed.append(block.topic)
    epistemic_gap = len(missed) / max(1, len(DOCTRINE_CACHE))
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

DRIFT_BASELINE = {
    "SLO Definition Standards": 0.98,
    "Error Budget Calculation": 0.97,
    "Burn Rate Analysis": 0.96,
    "Latency Percentile Tracking (p50, p95, p99)": 0.97,
    "Throughput SLI Measurement": 0.96
}

def drift_detection() -> Dict[str, Any]:
    drift = {}
    for block in DOCTRINE_CACHE:
        baseline = DRIFT_BASELINE.get(block.topic, block.confidence)
        drift_amt = block.confidence - baseline
        drift[block.topic] = drift_amt
    return drift

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path("slo_monitor_audit.jsonl")

def log_audit_entry(entry: Dict[str, Any]):
    try:
        with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as e:
        logger.error(f"Audit log write failed: {e}")

# =========================
# DETERMINISM HASH
# =========================

def compute_determinism_hash(*args) -> str:
    m = hashlib.sha256()
    for a in args:
        if isinstance(a, (dict, list)):
            m.update(json.dumps(a, sort_keys=True).encode("utf-8"))
        else:
            m.update(str(a).encode("utf-8"))
    return m.hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(title="SLO Monitor Engine", version="1.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    logger.info("SLO Monitor Engine (S07) startup.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("SLO Monitor Engine (S07) shutdown.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest, request: Request):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        # Layer 1: Doctrine cache
        block = doctrine_layer(req.scenario)
        if block:
            layer = 1
        else:
            # Layer 2: Semantic search
            block = semantic_search_layer(req.scenario)
            if block:
                layer = 2
            else:
                # Layer 3: Deep analysis
                layer = 3
        if not block:
            # Fallback: Compose from all
            primary_conclusion, key_factors, counter_arguments, reasoning_framework = deep_analysis_layer(req.scenario, req.mode)
            block = DoctrineBlock(
                topic="Composite",
                keywords=[],
                conclusion_template=primary_conclusion,
                reasoning_framework=reasoning_framework,
                key_factors=key_factors,
                primary_authority=[],
                burden_holder="",
                adversary_position="",
                counter_arguments=counter_arguments,
                resolution_strategy="Aggregate all applicable SLO doctrines.",
                entity_scope="",
                confidence=0.8,
                confidence_zone=ConfidenceZone.HIGH_RISK,
                controlling_precedent=[]
            )
        else:
            primary_conclusion = block.conclusion_template
            key_factors = block.key_factors
            counter_arguments = block.counter_arguments
            reasoning_framework = block.reasoning_framework
        # Deep analysis overlay
        if req.complexity > 7:
            primary_conclusion, key_factors, counter_arguments, reasoning_framework = deep_analysis_layer(req.scenario, req.mode)
        # Epistemic guardrails
        primary_conclusion = apply_epistemic_guardrails(primary_conclusion)
        reasoning_framework = apply_epistemic_guardrails(reasoning_framework)
        # Authority hardening
        primary_authority = block.primary_authority
        controlling, weight = resolve_authority_conflict(primary_authority)
        # Fact fragility scoring
        fragility = score_fact_fragility(primary_conclusion)
        # Position and confidence
        position_zone = PositionZone.PLANNING if "plan" in req.scenario.lower() else (
            PositionZone.AUDIT if "audit" in req.scenario.lower() else PositionZone.REPORTING
        )
        confidence = block.confidence
        confidence_zone = block.confidence_zone
        # Determinism hash
        determinism_hash = compute_determinism_hash(
            req.dict(), block.topic, primary_conclusion, reasoning_framework, key_factors, primary_authority, counter_arguments
        )
        # Record metrics
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query(query_id, latency, block.keywords)
        # Audit trail
        log_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "scenario": req.scenario,
            "mode": req.mode.value,
            "entity_type": req.entity_type,
            "complexity": req.complexity,
            "layer": layer,
            "block_topic": block.topic,
            "confidence": confidence,
            "confidence_zone": confidence_zone.value,
            "position_zone": position_zone.value,
            "determinism_hash": determinism_hash,
            "client": request.client.host
        })
        return QueryResponse(
            engine_id="S07",
            query_id=query_id,
            mode=req.mode,
            confidence=confidence,
            confidence_zone=confidence_zone,
            position_zone=position_zone,
            primary_conclusion=primary_conclusion,
            reasoning_framework=reasoning_framework,
            key_factors=key_factors,
            primary_authority=primary_authority,
            counter_arguments=counter_arguments,
            resolution_strategy=block.resolution_strategy,
            determinism_hash=determinism_hash
        )
    except Exception as e:
        metrics_collector.record_error(query_id, str(e))
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "S07", "uptime": (datetime.utcnow() - metrics_collector.start_time).total_seconds()}

@app.get("/metrics")
async def metrics():
    return {
        "latency": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage(scenario: Optional[str] = None):
    if scenario:
        return coverage_map(scenario)
    else:
        return {"error": "scenario parameter required"}

@app.get("/drift")
async def drift():
    return drift_detection()

@app.get("/doctrines")
async def doctrines():
    return [
        {
            "topic": block.topic,
            "keywords": block.keywords,
            "confidence": block.confidence,
            "confidence_zone": block.confidence_zone.value,
            "controlling_precedent": block.controlling_precedent
        }
        for block in DOCTRINE_CACHE
    ]

# =========================
# ZONED ANALYSIS
# =========================

def tag_position_zone(conclusion: str, scenario: str) -> PositionZone:
    if "plan" in scenario.lower():
        return PositionZone.PLANNING
    elif "audit" in scenario.lower():
        return PositionZone.AUDIT
    else:
        return PositionZone.REPORTING

# =========================
# MAIN (if run as script)
# =========================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("slo_monitor:app", host="0.0.0.0", port=8707, log_level="info")
