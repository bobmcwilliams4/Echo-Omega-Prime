import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

# ENGINE CONSTANTS
ENGINE_ID = "AGI08"
ENGINE_PORT = 8877
ENGINE_NAME = "SENTINEL-X — Security and Integrity Engine"
ENGINE_VERSION = "1.0.0"

# ENUMS

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
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    DATA_LEAKAGE = "DATA_LEAKAGE"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    MALWARE_DETECTION = "MALWARE_DETECTION"
    PHISHING_ATTEMPT = "PHISHING_ATTEMPT"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    SYSTEM_DRIFT = "SYSTEM_DRIFT"
    AUDIT_TRAIL_MISSING = "AUDIT_TRAIL_MISSING"
    ANOMALOUS_BEHAVIOR = "ANOMALOUS_BEHAVIOR"
    ERROR_HEALING = "ERROR_HEALING"
    INTEGRITY_CHECK_FAILURE = "INTEGRITY_CHECK_FAILURE"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"
    CONFIGURATION_DRIFT = "CONFIGURATION_DRIFT"
    NETWORK_INTRUSION = "NETWORK_INTRUSION"
    API_ABUSE = "API_ABUSE"
    COMPLIANCE_GAP = "COMPLIANCE_GAP"
    THREAT_INTELLIGENCE = "THREAT_INTELLIGENCE"
    SYSTEM_COMPROMISE = "SYSTEM_COMPROMISE"
    UNKNOWN = "UNKNOWN"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# PYDANTIC MODELS

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    domain: str
    payload: Dict[str, Any]
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    issue_category: IssueCategory = IssueCategory.UNKNOWN

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    status: str
    result: Any
    latency_ms: float
    confidence_zone: ConfidenceZone
    issue_category: IssueCategory
    orchestration_trace: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float = 1.0
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    engine_id: str
    reason: str
    domain: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence_zone: ConfidenceZone
    issue_category: IssueCategory

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decisions: List[RoutingDecision]
    responses: List[QueryResponse]
    overall_status: str
    latency_ms: float
    orchestration_trace: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# SUB_ENGINE_REGISTRY

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "AGI01": SubEngineConfig(
        engine_id="AGI01",
        name="CORTEX",
        port=8801,
        health_url="http://localhost:8801/health",
        capabilities=["planning", "reporting", "audit", "policy", "drift-detection"],
        weight=1.0,
        domains=["planning", "policy", "drift", "audit", "reporting"],
        status=SubEngineStatus.HEALTHY
    ),
    "AGI04": SubEngineConfig(
        engine_id="AGI04",
        name="REFLEX",
        port=8804,
        health_url="http://localhost:8804/health",
        capabilities=["incident-response", "defense", "anomaly-detection", "threat-intelligence"],
        weight=1.2,
        domains=["incident", "defense", "anomaly", "threat", "response"],
        status=SubEngineStatus.HEALTHY
    ),
    "GS343": SubEngineConfig(
        engine_id="GS343",
        name="Error Healing",
        port=8343,
        health_url="http://localhost:8343/health",
        capabilities=["error-healing", "integrity-check", "auto-remediation"],
        weight=0.9,
        domains=["error", "healing", "integrity", "remediation"],
        status=SubEngineStatus.HEALTHY
    ),
    "DRIFT_WATCHER": SubEngineConfig(
        engine_id="DRIFT_WATCHER",
        name="Drift Watcher",
        port=8899,
        health_url="http://localhost:8899/health",
        capabilities=["drift-detection", "configuration-monitoring"],
        weight=0.8,
        domains=["drift", "configuration", "monitoring"],
        status=SubEngineStatus.HEALTHY
    ),
    "AUDIT_TRAIL": SubEngineConfig(
        engine_id="AUDIT_TRAIL",
        name="Audit Trail",
        port=8888,
        health_url="http://localhost:8888/health",
        capabilities=["audit", "trail", "compliance", "reporting"],
        weight=1.1,
        domains=["audit", "trail", "compliance", "reporting"],
        status=SubEngineStatus.HEALTHY
    ),
    "ALL_ENGINES": SubEngineConfig(
        engine_id="ALL_ENGINES",
        name="All Engines",
        port=0,
        health_url="http://localhost:8877/monitor",
        capabilities=["monitoring", "aggregation", "status"],
        weight=1.0,
        domains=["monitoring", "aggregation", "status"],
        status=SubEngineStatus.HEALTHY
    ),
}

# ROUTING_RULES (200+ domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    "planning": "AGI01",
    "policy": "AGI01",
    "drift": "DRIFT_WATCHER",
    "configuration": "DRIFT_WATCHER",
    "audit": "AUDIT_TRAIL",
    "reporting": "AUDIT_TRAIL",
    "incident": "AGI04",
    "defense": "AGI04",
    "anomaly": "AGI04",
    "threat": "AGI04",
    "response": "AGI04",
    "error": "GS343",
    "healing": "GS343",
    "integrity": "GS343",
    "remediation": "GS343",
    "monitoring": "ALL_ENGINES",
    "aggregation": "ALL_ENGINES",
    "status": "ALL_ENGINES",
    "compliance": "AUDIT_TRAIL",
    "trail": "AUDIT_TRAIL",
    "authentication": "AGI04",
    "privilege": "AGI04",
    "malware": "AGI04",
    "phishing": "AGI04",
    "system": "DRIFT_WATCHER",
    "resource": "DRIFT_WATCHER",
    "exhaustion": "DRIFT_WATCHER",
    "network": "AGI04",
    "intrusion": "AGI04",
    "api": "AGI04",
    "abuse": "AGI04",
    "gap": "AUDIT_TRAIL",
    "compromise": "AGI04",
    "leakage": "GS343",
    "escalation": "AGI04",
    "access": "AGI04",
    "behavior": "AGI04",
    "missing": "AUDIT_TRAIL",
    "failure": "GS343",
    "auto-remediation": "GS343",
    "configuration-monitoring": "DRIFT_WATCHER",
    "threat-intelligence": "AGI04",
    "policy-violation": "AGI01",
    "drift-detection": "DRIFT_WATCHER",
    "audit-trail": "AUDIT_TRAIL",
    "report": "AUDIT_TRAIL",
    "incident-response": "AGI04",
    "defensive": "AGI04",
    "aggressive": "AGI04",
    "disclosure": "AUDIT_TRAIL",
    "high-risk": "AGI04",
    "planning-zone": "AGI01",
    "reporting-zone": "AUDIT_TRAIL",
    "audit-zone": "AUDIT_TRAIL",
    "defensible-zone": "AGI01",
    "aggressive-zone": "AGI04",
    "disclosure-zone": "AUDIT_TRAIL",
    "high-risk-zone": "AGI04",
    "authentication-failure": "AGI04",
    "data-leakage": "GS343",
    "privilege-escalation": "AGI04",
    "malware-detection": "AGI04",
    "phishing-attempt": "AGI04",
    "policy-violation": "AGI01",
    "system-drift": "DRIFT_WATCHER",
    "audit-trail-missing": "AUDIT_TRAIL",
    "anomalous-behavior": "AGI04",
    "error-healing": "GS343",
    "integrity-check-failure": "GS343",
    "unauthorized-access": "AGI04",
    "resource-exhaustion": "DRIFT_WATCHER",
    "configuration-drift": "DRIFT_WATCHER",
    "network-intrusion": "AGI04",
    "api-abuse": "AGI04",
    "compliance-gap": "AUDIT_TRAIL",
    "threat-intelligence": "AGI04",
    "system-compromise": "AGI04",
    "unknown": "ALL_ENGINES",
    "planning-reporting": "AGI01",
    "planning-audit": "AGI01",
    "reporting-audit": "AUDIT_TRAIL",
    "audit-reporting": "AUDIT_TRAIL",
    "audit-planning": "AGI01",
    "reporting-planning": "AGI01",
    "incident-planning": "AGI04",
    "incident-audit": "AGI04",
    "incident-reporting": "AGI04",
    "incident-policy": "AGI04",
    "incident-drift": "AGI04",
    "incident-error": "AGI04",
    "incident-healing": "AGI04",
    "incident-integrity": "AGI04",
    "incident-remediation": "AGI04",
    "incident-monitoring": "AGI04",
    "incident-aggregation": "AGI04",
    "incident-status": "AGI04",
    "incident-compliance": "AGI04",
    "incident-trail": "AGI04",
    "incident-authentication": "AGI04",
    "incident-privilege": "AGI04",
    "incident-malware": "AGI04",
    "incident-phishing": "AGI04",
    "incident-system": "AGI04",
    "incident-resource": "AGI04",
    "incident-exhaustion": "AGI04",
    "incident-network": "AGI04",
    "incident-intrusion": "AGI04",
    "incident-api": "AGI04",
    "incident-abuse": "AGI04",
    "incident-gap": "AGI04",
    "incident-compromise": "AGI04",
    "incident-leakage": "AGI04",
    "incident-escalation": "AGI04",
    "incident-access": "AGI04",
    "incident-behavior": "AGI04",
    "incident-missing": "AGI04",
    "incident-failure": "AGI04",
    "incident-auto-remediation": "AGI04",
    "incident-configuration-monitoring": "AGI04",
    "incident-threat-intelligence": "AGI04",
    "incident-policy-violation": "AGI04",
    "incident-drift-detection": "AGI04",
    "incident-audit-trail": "AGI04",
    "incident-report": "AGI04",
    "incident-incident-response": "AGI04",
    "incident-defensive": "AGI04",
    "incident-aggressive": "AGI04",
    "incident-disclosure": "AGI04",
    "incident-high-risk": "AGI04",
    "incident-planning-zone": "AGI04",
    "incident-reporting-zone": "AGI04",
    "incident-audit-zone": "AGI04",
    "incident-defensible-zone": "AGI04",
    "incident-aggressive-zone": "AGI04",
    "incident-disclosure-zone": "AGI04",
    "incident-high-risk-zone": "AGI04",
    "incident-authentication-failure": "AGI04",
    "incident-data-leakage": "AGI04",
    "incident-privilege-escalation": "AGI04",
    "incident-malware-detection": "AGI04",
    "incident-phishing-attempt": "AGI04",
    "incident-policy-violation": "AGI04",
    "incident-system-drift": "AGI04",
    "incident-audit-trail-missing": "AGI04",
    "incident-anomalous-behavior": "AGI04",
    "incident-error-healing": "AGI04",
    "incident-integrity-check-failure": "AGI04",
    "incident-unauthorized-access": "AGI04",
    "incident-resource-exhaustion": "AGI04",
    "incident-configuration-drift": "AGI04",
    "incident-network-intrusion": "AGI04",
    "incident-api-abuse": "AGI04",
    "incident-compliance-gap": "AGI04",
    "incident-threat-intelligence": "AGI04",
    "incident-system-compromise": "AGI04",
    "incident-unknown": "AGI04",
    "drift-planning": "DRIFT_WATCHER",
    "drift-audit": "DRIFT_WATCHER",
    "drift-reporting": "DRIFT_WATCHER",
    "drift-policy": "DRIFT_WATCHER",
    "drift-error": "DRIFT_WATCHER",
    "drift-healing": "DRIFT_WATCHER",
    "drift-integrity": "DRIFT_WATCHER",
    "drift-remediation": "DRIFT_WATCHER",
    "drift-monitoring": "DRIFT_WATCHER",
    "drift-aggregation": "DRIFT_WATCHER",
    "drift-status": "DRIFT_WATCHER",
    "drift-compliance": "DRIFT_WATCHER",
    "drift-trail": "DRIFT_WATCHER",
    "drift-authentication": "DRIFT_WATCHER",
    "drift-privilege": "DRIFT_WATCHER",
    "drift-malware": "DRIFT_WATCHER",
    "drift-phishing": "DRIFT_WATCHER",
    "drift-system": "DRIFT_WATCHER",
    "drift-resource": "DRIFT_WATCHER",
    "drift-exhaustion": "DRIFT_WATCHER",
    "drift-network": "DRIFT_WATCHER",
    "drift-intrusion": "DRIFT_WATCHER",
    "drift-api": "DRIFT_WATCHER",
    "drift-abuse": "DRIFT_WATCHER",
    "drift-gap": "DRIFT_WATCHER",
    "drift-compromise": "DRIFT_WATCHER",
    "drift-leakage": "DRIFT_WATCHER",
    "drift-escalation": "DRIFT_WATCHER",
    "drift-access": "DRIFT_WATCHER",
    "drift-behavior": "DRIFT_WATCHER",
    "drift-missing": "DRIFT_WATCHER",
    "drift-failure": "DRIFT_WATCHER",
    "drift-auto-remediation": "DRIFT_WATCHER",
    "drift-configuration-monitoring": "DRIFT_WATCHER",
    "drift-threat-intelligence": "DRIFT_WATCHER",
    "drift-policy-violation": "DRIFT_WATCHER",
    "drift-drift-detection": "DRIFT_WATCHER",
    "drift-audit-trail": "DRIFT_WATCHER",
    "drift-report": "DRIFT_WATCHER",
    "drift-incident-response": "DRIFT_WATCHER",
    "drift-defensive": "DRIFT_WATCHER",
    "drift-aggressive": "DRIFT_WATCHER",
    "drift-disclosure": "DRIFT_WATCHER",
    "drift-high-risk": "DRIFT_WATCHER",
    "drift-planning-zone": "DRIFT_WATCHER",
    "drift-reporting-zone": "DRIFT_WATCHER",
    "drift-audit-zone": "DRIFT_WATCHER",
    "drift-defensible-zone": "DRIFT_WATCHER",
    "drift-aggressive-zone": "DRIFT_WATCHER",
    "drift-disclosure-zone": "DRIFT_WATCHER",
    "drift-high-risk-zone": "DRIFT_WATCHER",
    "drift-authentication-failure": "DRIFT_WATCHER",
    "drift-data-leakage": "DRIFT_WATCHER",
    "drift-privilege-escalation": "DRIFT_WATCHER",
    "drift-malware-detection": "DRIFT_WATCHER",
    "drift-phishing-attempt": "DRIFT_WATCHER",
    "drift-policy-violation": "DRIFT_WATCHER",
    "drift-system-drift": "DRIFT_WATCHER",
    "drift-audit-trail-missing": "DRIFT_WATCHER",
    "drift-anomalous-behavior": "DRIFT_WATCHER",
    "drift-error-healing": "DRIFT_WATCHER",
    "drift-integrity-check-failure": "DRIFT_WATCHER",
    "drift-unauthorized-access": "DRIFT_WATCHER",
    "drift-resource-exhaustion": "DRIFT_WATCHER",
    "drift-configuration-drift": "DRIFT_WATCHER",
    "drift-network-intrusion": "DRIFT_WATCHER",
    "drift-api-abuse": "DRIFT_WATCHER",
    "drift-compliance-gap": "DRIFT_WATCHER",
    "drift-threat-intelligence": "DRIFT_WATCHER",
    "drift-system-compromise": "DRIFT_WATCHER",
    "drift-unknown": "DRIFT_WATCHER",
    "error-planning": "GS343",
    "error-audit": "GS343",
    "error-reporting": "GS343",
    "error-policy": "GS343",
    "error-drift": "GS343",
    "error-healing": "GS343",
    "error-integrity": "GS343",
    "error-remediation": "GS343",
    "error-monitoring": "GS343",
    "error-aggregation": "GS343",
    "error-status": "GS343",
    "error-compliance": "GS343",
    "error-trail": "GS343",
    "error-authentication": "GS343",
    "error-privilege": "GS343",
    "error-malware": "GS343",
    "error-phishing": "GS343",
    "error-system": "GS343",
    "error-resource": "GS343",
    "error-exhaustion": "GS343",
    "error-network": "GS343",
    "error-intrusion": "GS343",
    "error-api": "GS343",
    "error-abuse": "GS343",
    "error-gap": "GS343",
    "error-compromise": "GS343",
    "error-leakage": "GS343",
    "error-escalation": "GS343",
    "error-access": "GS343",
    "error-behavior": "GS343",
    "error-missing": "GS343",
    "error-failure": "GS343",
    "error-auto-remediation": "GS343",
    "error-configuration-monitoring": "GS343",
    "error-threat-intelligence": "GS343",
    "error-policy-violation": "GS343",
    "error-drift-detection": "GS343",
    "error-audit-trail": "GS343",
    "error-report": "GS343",
    "error-incident-response": "GS343",
    "error-defensive": "GS343",
    "error-aggressive": "GS343",
    "error-disclosure": "GS343",
    "error-high-risk": "GS343",
    "error-planning-zone": "GS343",
    "error-reporting-zone": "GS343",
    "error-audit-zone": "GS343",
    "error-defensible-zone": "GS343",
    "error-aggressive-zone": "GS343",
    "error-disclosure-zone": "GS343",
    "error-high-risk-zone": "GS343",
    "error-authentication-failure": "GS343",
    "error-data-leakage": "GS343",
    "error-privilege-escalation": "GS343",
    "error-malware-detection": "GS343",
    "error-phishing-attempt": "GS343",
    "error-policy-violation": "GS343",
    "error-system-drift": "GS343",
    "error-audit-trail-missing": "GS343",
    "error-anomalous-behavior": "GS343",
    "error-error-healing": "GS343",
    "error-integrity-check-failure": "GS343",
    "error-unauthorized-access": "GS343",
    "error-resource-exhaustion": "GS343",
    "error-configuration-drift": "GS343",
    "error-network-intrusion": "GS343",
    "error-api-abuse": "GS343",
    "error-compliance-gap": "GS343",
    "error-threat-intelligence": "GS343",
    "error-system-compromise": "GS343",
    "error-unknown": "GS343",
    # Add more domain keywords as needed to reach 200+ rules
}

# METRICS COLLECTOR

class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_times = collections.deque(maxlen=10000)
        self.latencies = collections.deque(maxlen=10000)
        self.query_count_hour = collections.defaultdict(int)
        self.error_count_hour = collections.defaultdict(int)
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: float):
        now = datetime.utcnow()
        hour_key = now.strftime("%Y-%m-%d-%H")
        async with self.lock:
            self.query_times.append((query_id, now))
            self.latencies.append(latency_ms)
            self.query_count_hour[hour_key] += 1

    async def record_error(self, query_id: str, error_msg: str):
        now = datetime.utcnow()
        hour_key = now.strftime("%Y-%m-%d-%H")
        async with self.lock:
            self.error_times.append((query_id, now, error_msg))
            self.error_count_hour[hour_key] += 1

    async def get_latency_stats(self) -> Dict[str, Any]:
        async with self.lock:
            latencies = list(self.latencies)
        if not latencies:
            return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
        return {
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "min": min(latencies),
            "max": max(latencies)
        }

    async def queries_last_hour(self) -> int:
        now = datetime.utcnow()
        hour_key = now.strftime("%Y-%m-%d-%H")
        async with self.lock:
            return self.query_count_hour.get(hour_key, 0)

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
        topic="Doctrine Drift Detection",
        keywords=["drift detection", "model deviation", "output monitoring", "anomaly detection", "statistical control", "machine learning", "concept drift", "data distribution"],
        conclusion_template=(
            "Continuous monitoring for doctrine drift is essential to maintain engine integrity. "
            "When output patterns deviate beyond statistically defined thresholds, alerts must be triggered. "
            "Timely detection enables corrective recalibration or retraining, preserving system reliability."
        ),
        reasoning_framework=(
            "Doctrine drift detection involves identifying when the outputs of AI engines deviate from established expected patterns. "
            "This is critical because drift can indicate degradation in model performance or external changes in data distributions. "
            "Techniques include statistical process control methods such as control charts, hypothesis testing for distributional changes, "
            "and embedding-based similarity metrics. Concept drift can be sudden, incremental, or recurring, requiring adaptive detection methods. "
            "Monitoring should incorporate both input feature distributions and output confidence scores to triangulate drift events. "
            "Failure to detect drift can lead to erroneous outputs, security vulnerabilities, and loss of trustworthiness. "
            "The doctrine must define thresholds for acceptable variation and specify automated triggers for human review or model retraining. "
            "Integration with audit trail systems ensures traceability of drift events and responses. "
            "Cross-engine consistency checks can corroborate drift detection by comparing outputs on identical queries across multiple engines. "
            "Drift detection also supports compliance monitoring by ensuring models remain within validated operational parameters. "
            "Incorporating domain-specific knowledge enhances sensitivity to meaningful deviations versus noise. "
            "Overall, a robust doctrine drift detection framework is foundational for maintaining the security and integrity of AI systems."
        ),
        key_factors=[
            "Statistical thresholds for drift",
            "Input and output distribution monitoring",
            "Concept drift types (sudden, incremental, recurring)",
            "Cross-engine output consistency",
            "Audit trail integration",
            "Automated alerting and retraining triggers"
        ],
        primary_authority=[
            "Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014). A survey on concept drift adaptation. ACM Computing Surveys (CSUR), 46(4), 1-37.",
            "Lu, J., Liu, A., Dong, F., Gu, F., Gama, J., & Zhang, G. (2018). Learning under concept drift: A review. IEEE Transactions on Knowledge and Data Engineering, 31(12), 2346-2363.",
            "Widmer, G., & Kubat, M. (1996). Learning in the presence of concept drift and hidden contexts. Machine learning, 23(1), 69-101.",
            "ISO/IEC 27001:2013 - Information security management systems — Requirements.",
            "NIST SP 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations."
        ],
        burden_holder="Engine developers and monitoring teams",
        adversary_position="Adversaries may attempt to induce drift via data poisoning or adversarial inputs to degrade model performance undetected.",
        counter_arguments=[
            "Drift detection thresholds may generate false positives due to natural data variability.",
            "Overly sensitive drift detection can cause unnecessary retraining, increasing operational costs.",
            "Some drifts are benign and do not affect critical outputs, making detection less urgent.",
            "Cross-engine consistency may not always be feasible due to differing model architectures.",
            "Audit trail data may be incomplete or delayed, hindering timely detection."
        ],
        resolution_strategy=(
            "Implement multi-layered drift detection combining statistical, behavioral, and cross-engine methods. "
            "Calibrate thresholds using historical data to balance sensitivity and specificity. "
            "Incorporate human-in-the-loop review for ambiguous drift alerts. "
            "Ensure audit trails are comprehensive and real-time accessible. "
            "Deploy adversarial training and data sanitization to mitigate induced drift."
        ),
        entity_scope="All AI engines within SENTINEL-X ecosystem",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Gama et al., ACM Computing Surveys, 2014"
    ),
    DoctrineBlock(
        topic="Hallucination Detection",
        keywords=["hallucination", "false assertions", "doctrine cache", "fact verification", "knowledge validation", "natural language generation", "AI reliability", "misinformation"],
        conclusion_template=(
            "Hallucination detection is vital to prevent the engine from asserting unsupported facts. "
            "By cross-referencing outputs against the doctrine cache and authoritative sources, hallucinations can be flagged and mitigated. "
            "This preserves trust and reduces misinformation risks."
        ),
        reasoning_framework=(
            "Hallucination in AI systems refers to the generation of outputs that are not grounded in factual data or the knowledge base. "
            "Detecting hallucinations requires comparing generated assertions against a trusted doctrine cache containing validated domain knowledge. "
            "Techniques include semantic similarity analysis, fact-checking algorithms, and citation verification. "
            "Natural language generation models may produce plausible but incorrect statements due to probabilistic sampling or training data biases. "
            "Hallucination detection must operate in real-time to prevent dissemination of false information. "
            "Incorporating epistemic guardrails that restrict output to verified knowledge domains reduces hallucination risk. "
            "Confidence calibration aids in identifying low-confidence assertions prone to hallucination. "
            "Audit trails documenting source references and validation steps enhance accountability. "
            "Cross-engine consistency checks can identify hallucinations when outputs diverge significantly on identical queries. "
            "Hallucination detection is critical in high-stakes domains such as healthcare, finance, and legal applications where misinformation can cause harm."
        ),
        key_factors=[
            "Comparison with doctrine cache",
            "Semantic and factual verification",
            "Confidence score thresholds",
            "Citation and source validation",
            "Epistemic guardrails enforcement",
            "Cross-engine output consistency",
            "Audit trail documentation"
        ],
        primary_authority=[
            "Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., ... & Fung, P. (2022). Survey of hallucination in natural language generation. ACM Computing Surveys (CSUR), 55(12), 1-38.",
            "Thorne, J., Vlachos, A., Christodoulopoulos, C., & Mittal, A. (2018). FEVER: a large-scale dataset for fact extraction and verification. Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics.",
            "NIST SP 800-171 Rev. 2 - Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations.",
            "ISO/IEC 2382-37:2017 - Information technology — Vocabulary — Part 37: Artificial intelligence.",
            "Marcus, G. (2020). The next decade in AI: four steps towards robust artificial intelligence. arXiv preprint arXiv:2002.06177."
        ],
        burden_holder="Engine output validation modules and knowledge engineers",
        adversary_position="Adversaries may exploit hallucination vulnerabilities to inject misinformation or manipulate outputs.",
        counter_arguments=[
            "Strict hallucination detection may limit creative or generative capabilities of AI.",
            "Some factual assertions may be novel and not yet present in doctrine cache, causing false positives.",
            "Real-time detection can introduce latency impacting user experience.",
            "Semantic similarity measures may fail on nuanced or ambiguous language.",
            "Cross-engine consistency is challenged by model diversity and update cycles."
        ],
        resolution_strategy=(
            "Employ multi-modal verification combining semantic, factual, and citation checks. "
            "Maintain an up-to-date and comprehensive doctrine cache. "
            "Use confidence calibration to prioritize review of low-confidence outputs. "
            "Implement human oversight for flagged hallucinations. "
            "Continuously update epistemic guardrails and audit trails to enhance detection fidelity."
        ),
        entity_scope="Natural Language Generation engines and output validation layers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Ji et al., ACM Computing Surveys, 2022"
    ),
    DoctrineBlock(
        topic="Data Poisoning Prevention",
        keywords=["data poisoning", "adversarial attack", "training data integrity", "model robustness", "input sanitization", "anomaly detection", "security", "machine learning"],
        conclusion_template=(
            "Preventing data poisoning is critical to safeguard model integrity. "
            "Robust data validation, anomaly detection, and training pipeline security must be enforced to mitigate poisoning risks. "
            "Proactive defenses reduce vulnerability to adversarial manipulation."
        ),
        reasoning_framework=(
            "Data poisoning attacks aim to corrupt the training data or doctrine cache to degrade model performance or induce malicious behavior. "
            "Such attacks can be targeted (backdoor insertion) or indiscriminate (label flipping). "
            "Prevention requires securing data ingestion pipelines with rigorous validation, provenance tracking, and anomaly detection. "
            "Techniques include statistical outlier detection, clustering-based anomaly identification, and robust learning algorithms resilient to corrupted samples. "
            "Access control enforcement limits unauthorized data modifications. "
            "Continuous monitoring of model performance metrics can reveal poisoning-induced degradation. "
            "Audit trail integrity ensures traceability of data provenance and modifications. "
            "Patch management and dependency vulnerability scanning reduce risk of exploitation via third-party components. "
            "Collaboration with forensic analysis teams enables rapid investigation and remediation of poisoning incidents. "
            "A layered defense combining technical, procedural, and organizational controls is essential for effective data poisoning prevention."
        ),
        key_factors=[
            "Data ingestion validation",
            "Anomaly and outlier detection",
            "Access control and provenance tracking",
            "Robust learning algorithms",
            "Audit trail completeness",
            "Patch and dependency management",
            "Forensic readiness"
        ],
        primary_authority=[
            "Steinhardt, J., Koh, P. W., & Liang, P. (2017). Certified defenses for data poisoning attacks. Advances in Neural Information Processing Systems, 30.",
            "Biggio, B., & Roli, F. (2018). Wild patterns: Ten years after the rise of adversarial machine learning. Pattern Recognition, 84, 317-331.",
            "NIST SP 800-160 Vol. 2 - Developing Cyber Resilient Systems.",
            "ISO/IEC 27034-1:2011 - Information technology — Security techniques — Application security — Part 1: Overview and concepts.",
            "Barreno, M., Nelson, B., Joseph, A. D., & Tygar, J. D. (2010). The security of machine learning. Machine Learning, 81(2), 121-148."
        ],
        burden_holder="Data engineers, security teams, and model trainers",
        adversary_position="Attackers seek to inject malicious data to manipulate model outputs or degrade performance stealthily.",
        counter_arguments=[
            "Overly strict data validation may reject legitimate but novel data, reducing model adaptability.",
            "Anomaly detection can produce false positives, increasing operational overhead.",
            "Resource constraints may limit continuous monitoring and forensic capabilities.",
            "Sophisticated poisoning attacks may evade detection by mimicking legitimate data.",
            "Dependency vulnerabilities may be unknown or undisclosed, complicating patch management."
        ],
        resolution_strategy=(
            "Implement multi-tiered data validation combining automated and manual review. "
            "Deploy robust anomaly detection tuned to domain-specific data characteristics. "
            "Enforce strict access controls and maintain detailed provenance records. "
            "Use robust training algorithms with certified defenses. "
            "Maintain up-to-date patching and vulnerability scanning processes. "
            "Prepare forensic analysis playbooks for rapid incident response."
        ),
        entity_scope="Training data pipelines and doctrine caches across all engines",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Steinhardt et al., NeurIPS, 2017"
    ),
    DoctrineBlock(
        topic="Input Validation",
        keywords=["input validation", "sanitization", "security", "data integrity", "injection prevention", "API security", "boundary checking", "malformed input"],
        conclusion_template=(
            "Comprehensive input validation is mandatory to prevent injection attacks and data corruption. "
            "All external inputs must be sanitized and verified before processing to maintain system integrity and security."
        ),
        reasoning_framework=(
            "Input validation is the first line of defense against a wide range of security threats including injection attacks, buffer overflows, and malformed data processing. "
            "It involves verifying that all external inputs conform to expected formats, types, lengths, and value ranges before being processed by the engine. "
            "Sanitization removes or encodes potentially dangerous characters or constructs to prevent code injection or command execution. "
            "Boundary checking ensures inputs do not exceed allocated buffer sizes, preventing memory corruption. "
            "Input validation must be context-aware, adapting rules based on input source and expected usage. "
            "APIs exposed to external users require strict validation to prevent abuse and unauthorized access. "
            "Failure to validate inputs can lead to security breaches, data corruption, and system crashes. "
            "Input validation complements other security controls such as access control and rate limiting. "
            "Automated testing and fuzzing help identify input validation gaps. "
            "Standards such as OWASP Top Ten emphasize input validation as a critical security practice."
        ),
        key_factors=[
            "Format and type checking",
            "Sanitization and encoding",
            "Boundary and length checks",
            "Context-aware validation",
            "API input controls",
            "Automated testing and fuzzing",
            "Integration with access control"
        ],
        primary_authority=[
            "OWASP Foundation. (2021). OWASP Top Ten Web Application Security Risks.",
            "NIST SP 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations.",
            "CERT Secure Coding Standards - Input Validation.",
            "ISO/IEC 27034-1:2011 - Application security overview.",
            "Howard, M., & LeBlanc, D. (2003). Writing Secure Code. Microsoft Press."
        ],
        burden_holder="Engine interface developers and security engineers",
        adversary_position="Attackers exploit input validation weaknesses to inject malicious payloads or cause denial of service.",
        counter_arguments=[
            "Strict input validation may reject legitimate but unusual inputs, impacting usability.",
            "Complex validation rules increase development and maintenance overhead.",
            "Some input attacks may bypass validation via encoding or protocol manipulation.",
            "Performance overhead from validation may affect system responsiveness.",
            "Incomplete validation coverage leaves residual vulnerabilities."
        ],
        resolution_strategy=(
            "Adopt a whitelist approach for input validation wherever feasible. "
            "Employ layered validation including client-side and server-side checks. "
            "Use standardized libraries and frameworks for sanitization. "
            "Continuously test validation logic with fuzzing and penetration testing. "
            "Integrate validation with logging and alerting for suspicious inputs."
        ),
        entity_scope="All external input interfaces across SENTINEL-X engines",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="OWASP Top Ten, 2021"
    ),
    DoctrineBlock(
        topic="Output Validation",
        keywords=["output validation", "response integrity", "accuracy assurance", "sanitization", "quality control", "error handling", "security", "data leakage prevention"],
        conclusion_template=(
            "Output validation ensures that engine responses meet defined quality and security standards. "
            "Sanitizing outputs prevents data leakage and maintains response integrity."
        ),
        reasoning_framework=(
            "Output validation is essential to verify that the responses generated by AI engines are accurate, complete, and free from sensitive data leakage. "
            "It involves checking that outputs conform to expected formats, do not contain banned phrases or confidential information, and meet confidence thresholds. "
            "Sanitization of outputs prevents injection of malicious content or unintended information disclosure. "
            "Quality control mechanisms detect anomalies such as incomplete responses, hallucinations, or inconsistent data. "
            "Error handling ensures that failures produce safe and informative outputs without exposing system internals. "
            "Output validation supports compliance with regulatory requirements such as GDPR and HIPAA by preventing unauthorized data exposure. "
            "Integration with audit trail systems documents output validation results for accountability. "
            "Cross-engine consistency checks can validate output correctness by comparing responses to the same query. "
            "Automated testing and monitoring detect regression or degradation in output quality over time. "
            "Output validation complements input validation and access control to maintain overall system security."
        ),
        key_factors=[
            "Format and content verification",
            "Sanitization against injection and leakage",
            "Confidence threshold enforcement",
            "Error handling and safe failure modes",
            "Regulatory compliance adherence",
            "Audit trail documentation",
            "Cross-engine consistency"
        ],
        primary_authority=[
            "NIST SP 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "HIPAA Security Rule - Protection of electronic protected health information.",
            "OWASP Foundation. (2021). OWASP API Security Top 10.",
            "Goodman, B., & Flaxman, S. (2017). European Union regulations on algorithmic decision-making and a “right to explanation”. AI Magazine, 38(3), 50-57."
        ],
        burden_holder="Engine output modules and compliance teams",
        adversary_position="Adversaries may attempt to extract sensitive data or inject malicious content via outputs.",
        counter_arguments=[
            "Overly restrictive output validation may limit expressiveness or utility of responses.",
            "Sanitization may inadvertently remove useful information.",
            "Complex validation logic can introduce bugs or performance overhead.",
            "Some output errors may be subtle and hard to detect automatically.",
            "Cross-engine consistency may be difficult due to model differences."
        ],
        resolution_strategy=(
            "Define clear output format and content policies. "
            "Implement layered sanitization and validation checks. "
            "Use confidence calibration to filter low-quality outputs. "
            "Incorporate human review for flagged outputs. "
            "Maintain audit trails and compliance documentation."
        ),
        entity_scope="All engine response generation components",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 Rev. 5"
    ),
    DoctrineBlock(
        topic="Confidence Calibration",
        keywords=["confidence calibration", "probabilistic reliability", "uncertainty quantification", "model confidence", "output trustworthiness", "statistical calibration", "AI reliability", "error rates"],
        conclusion_template=(
            "Accurate confidence calibration ensures that confidence scores reflect true output reliability. "
            "Proper calibration enables informed decision-making and risk management."
        ),
        reasoning_framework=(
            "Confidence calibration refers to aligning the predicted confidence scores of AI models with the actual likelihood of correctness. "
            "Well-calibrated confidence scores allow users and downstream systems to interpret model outputs appropriately. "
            "Mis-calibrated models may be overconfident or underconfident, leading to misplaced trust or unnecessary skepticism. "
            "Calibration techniques include Platt scaling, isotonic regression, and temperature scaling applied post-training. "
            "Evaluation metrics such as Expected Calibration Error (ECE) and Brier score quantify calibration quality. "
            "Calibration must be maintained across different data distributions and over time, requiring continuous monitoring. "
            "Confidence calibration supports output validation, hallucination detection, and audit trail integrity by providing reliable uncertainty estimates. "
            "In safety-critical applications, calibrated confidence scores inform fallback strategies and human intervention thresholds. "
            "Cross-engine consistency in confidence scoring enhances robustness and comparability. "
            "Calibration also aids compliance by demonstrating model reliability and transparency."
        ),
        key_factors=[
            "Alignment of confidence scores with true correctness",
            "Calibration techniques (Platt scaling, isotonic regression)",
            "Evaluation metrics (ECE, Brier score)",
            "Continuous monitoring and recalibration",
            "Integration with output validation and audit trails",
            "Cross-engine confidence consistency",
            "Impact on decision-making and risk management"
        ],
        primary_authority=[
            "Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. Proceedings of the 34th International Conference on Machine Learning.",
            "Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. Proceedings of the 22nd International Conference on Machine Learning.",
            "NIST SP 1270 - AI Risk Management Framework (Draft).",
            "Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. Proceedings of the 35th International Conference on Machine Learning.",
            "ISO/IEC 2382-37:2017 - Artificial intelligence vocabulary."
        ],
        burden_holder="Model developers and validation teams",
        adversary_position="Adversaries may exploit mis-calibrated confidence to manipulate trust or evade detection.",
        counter_arguments=[
            "Calibration methods may reduce model accuracy if not carefully applied.",
            "Calibration can degrade over time due to drift or data changes.",
            "Complex calibration adds computational overhead.",
            "Confidence scores may be misinterpreted by end-users.",
            "Cross-engine calibration consistency is challenging."
        ],
        resolution_strategy=(
            "Incorporate calibration in model training and validation pipelines. "
            "Monitor calibration metrics continuously and recalibrate as needed. "
            "Educate users on interpreting confidence scores. "
            "Use ensemble and cross-engine methods to improve calibration robustness. "
            "Document calibration procedures in audit trails."
        ),
        entity_scope="All AI models generating probabilistic outputs",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Guo et al., ICML, 2017"
    ),
    DoctrineBlock(
        topic="Citation Verification",
        keywords=["citation verification", "source validation", "authority checking", "reference integrity", "knowledge base", "fact-checking", "document provenance", "information trustworthiness"],
        conclusion_template=(
            "Verifying citations ensures that referenced authorities exist, are current, and support assertions. "
            "This maintains knowledge base integrity and output credibility."
        ),
        reasoning_framework=(
            "Citation verification is the process of confirming that all references and authorities cited in engine outputs or doctrine caches are valid, accessible, and up-to-date. "
            "It prevents propagation of outdated, incorrect, or fabricated information. "
            "Verification involves automated checks against authoritative databases, digital object identifiers (DOIs), and trusted repositories. "
            "Provenance metadata and timestamps help assess currency and relevance. "
            "Incorporating citation verification into output validation and audit trails enhances transparency and accountability. "
            "Citation verification supports compliance with intellectual property and academic standards. "
            "Cross-referencing multiple sources can corroborate information and detect inconsistencies. "
            "Failure to verify citations risks misinformation, legal liability, and erosion of user trust. "
            "Citation verification must be scalable and integrated into continuous update cycles of doctrine caches. "
            "Human oversight remains critical for ambiguous or novel citations."
        ),
        key_factors=[
            "Existence and accessibility of cited sources",
            "Currency and relevance of references",
            "Automated verification against authoritative databases",
            "Provenance and metadata tracking",
            "Integration with output validation and audit trails",
            "Cross-source corroboration",
            "Compliance with IP and academic standards"
        ],
        primary_authority=[
            "ISO 690:2010 - Guidelines for bibliographic references and citations to information resources.",
            "CrossRef Metadata Search - https://search.crossref.org/",
            "NISO RP-8-2008 - Journal Article Versions (JAV): Recommendations of the NISO/ALPSP JAV Technical Working Group.",
            "COPE (Committee on Publication Ethics) Guidelines.",
            "NIST SP 800-171 Rev. 2 - Protecting Controlled Unclassified Information."
        ],
        burden_holder="Knowledge engineers and output validation systems",
        adversary_position="Adversaries may insert fabricated or outdated citations to mislead or evade detection.",
        counter_arguments=[
            "Automated citation verification may fail on non-standard or proprietary sources.",
            "Some authoritative sources may be behind paywalls or restricted access.",
            "Citation databases may have latency in updating records.",
            "Human review is resource-intensive and may not scale.",
            "False negatives may occur if citations are formatted incorrectly."
        ],
        resolution_strategy=(
            "Combine automated verification with periodic human audits. "
            "Maintain updated access to authoritative citation databases. "
            "Standardize citation formats and metadata capture. "
            "Use cross-referencing and redundancy to improve verification accuracy. "
            "Document verification results in audit trails."
        ),
        entity_scope="Doctrine caches and engine output referencing external authorities",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 690:2010"
    ),
    DoctrineBlock(
        topic="Epistemic Guardrail Enforcement",
        keywords=["epistemic guardrails", "banned phrases", "content filtering", "ethical AI", "output constraints", "language safety", "policy enforcement", "AI ethics"],
        conclusion_template=(
            "Enforcing epistemic guardrails prevents usage of banned phrases and unsafe content. "
            "This ensures ethical compliance and reduces risk of harmful outputs."
        ),
        reasoning_framework=(
            "Epistemic guardrails are predefined constraints embedded within AI engines to restrict outputs containing banned phrases or disallowed content. "
            "They serve to enforce ethical guidelines, legal compliance, and organizational policies. "
            "Guardrails are implemented via content filtering, pattern matching, and semantic analysis. "
            "They must be comprehensive, regularly updated, and context-aware to avoid over-blocking or under-blocking. "
            "Guardrails reduce risks of generating hate speech, disallowed advice, or sensitive information leakage. "
            "Integration with output validation and audit trails ensures enforcement transparency and accountability. "
            "Guardrails support compliance with regulations such as GDPR, CCPA, and industry-specific ethical standards. "
            "Balancing guardrail strictness with model utility requires continuous tuning and stakeholder engagement. "
            "Guardrail breaches trigger alerts, human review, and potential engine retraining. "
            "Effective epistemic guardrails are foundational for trustworthy AI deployment."
        ),
        key_factors=[
            "Definition and maintenance of banned phrase lists",
            "Context-aware content filtering",
            "Integration with output validation",
            "Compliance with ethical and legal standards",
            "Audit trail documentation",
            "Alerting and human review mechanisms",
            "Balance between restriction and utility"
        ],
        primary_authority=[
            "IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems (2019). Ethically Aligned Design.",
            "European Commission. (2021). Proposal for a Regulation laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).",
            "NIST AI Risk Management Framework (Draft).",
            "OpenAI Usage Policies.",
            "ISO/IEC 2382-37:2017 - Artificial intelligence vocabulary."
        ],
        burden_holder="AI ethics teams and output validation modules",
        adversary_position="Adversaries may attempt to circumvent guardrails to generate harmful or disallowed content.",
        counter_arguments=[
            "Guardrails may limit freedom of expression or useful information.",
            "Overly broad banned phrase lists can cause false positives.",
            "Contextual nuances may evade simple pattern matching.",
            "Guardrail updates may lag behind emerging threats.",
            "Enforcement may introduce latency or reduce model responsiveness."
        ],
        resolution_strategy=(
            "Implement multi-layered guardrails combining lexical, semantic, and contextual analysis. "
            "Regularly update banned phrase lists with expert input. "
            "Incorporate user feedback and incident analysis to refine guardrails. "
            "Balance enforcement with transparency and appeal mechanisms. "
            "Maintain audit trails and conduct periodic compliance reviews."
        ),
        entity_scope="All AI output generation components",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEEE Ethically Aligned Design, 2019"
    ),
    DoctrineBlock(
        topic="Audit Trail Integrity",
        keywords=["audit trail", "integrity verification", "JSONL logs", "tamper detection", "forensic readiness", "traceability", "security logging", "compliance"],
        conclusion_template=(
            "Ensuring audit trail integrity is critical for security and forensic investigations. "
            "JSONL audit logs must be complete, tamper-evident, and securely stored."
        ),
        reasoning_framework=(
            "Audit trails provide a chronological record of system activities, essential for security monitoring, compliance, and forensic analysis. "
            "Integrity of audit logs must be guaranteed to prevent tampering or deletion that could obscure malicious activities. "
            "Techniques include cryptographic hashing, digital signatures, and append-only storage mechanisms. "
            "JSONL (JSON Lines) format facilitates structured, line-delimited logging suitable for large-scale ingestion and analysis. "
            "Audit logs should capture sufficient detail including timestamps, user identities, actions performed, and system responses. "
            "Secure storage with access controls and redundancy prevents unauthorized modifications and data loss. "
            "Regular integrity checks and automated alerts detect anomalies or potential tampering. "
            "Audit trails support incident response, forensic investigations, and regulatory compliance such as SOX, HIPAA, and GDPR. "
            "Integration with SIEM (Security Information and Event Management) systems enhances real-time monitoring. "
            "Comprehensive audit trail integrity policies underpin trustworthiness and accountability in AI systems."
        ),
        key_factors=[
            "Cryptographic integrity mechanisms",
            "Structured JSONL logging format",
            "Access control and secure storage",
            "Comprehensive event capture",
            "Regular integrity verification",
            "Integration with SIEM and forensic tools",
            "Compliance with regulatory standards"
        ],
        primary_authority=[
            "NIST SP 800-92 - Guide to Computer Security Log Management.",
            "ISO/IEC 27037:2012 - Guidelines for identification, collection, acquisition and preservation of digital evidence.",
            "Sarbanes-Oxley Act (SOX) - Section 404 Internal Control Requirements.",
            "HIPAA Security Rule - Audit Controls.",
            "General Data Protection Regulation (GDPR) - Article 30 Records of Processing Activities."
        ],
        burden_holder="Security operations and compliance teams",
        adversary_position="Attackers may attempt to delete or alter audit logs to hide malicious actions.",
        counter_arguments=[
            "Cryptographic methods may add processing overhead.",
            "Large audit logs require significant storage and management resources.",
            "Incomplete logging may miss critical events.",
            "Access controls may be bypassed by insider threats.",
            "Integration complexity with diverse systems."
        ],
        resolution_strategy=(
            "Implement cryptographic chaining of log entries. "
            "Use append-only, write-once storage solutions. "
            "Enforce strict access controls and multi-factor authentication. "
            "Automate integrity verification and alerting. "
            "Maintain redundant backups and conduct periodic audits."
        ),
        entity_scope="All audit logging systems within SENTINEL-X",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-92"
    ),
    DoctrineBlock(
        topic="Determinism Verification",
        keywords=["determinism", "SHA-256 hash", "query reproducibility", "output consistency", "model versioning", "hash validation", "system integrity", "traceability"],
        conclusion_template=(
            "Determinism verification via SHA-256 hashing ensures reproducible query outputs. "
            "This supports system integrity, debugging, and compliance."
        ),
        reasoning_framework=(
            "Determinism verification involves confirming that identical queries produce identical outputs across engine runs, ensuring reproducibility and reliability. "
            "SHA-256 cryptographic hashes of query inputs and outputs provide a tamper-evident fingerprint for validation. "
            "Deterministic behavior is critical for debugging, auditability, and regulatory compliance. "
            "Non-determinism can arise from model stochasticity, version mismatches, or environmental differences. "
            "Version control and environment standardization mitigate non-determinism. "
            "Hash comparisons detect output deviations indicating drift, hallucination, or tampering. "
            "Determinism verification integrates with audit trails to link queries, outputs, and hashes. "
            "Cross-engine consistency checks further validate determinism across models. "
            "Automated alerts on hash mismatches trigger investigations and corrective actions. "
            "Maintaining determinism enhances user trust and system transparency."
        ),
        key_factors=[
            "SHA-256 hashing of inputs and outputs",
            "Version and environment control",
            "Integration with audit trails",
            "Cross-engine consistency",
            "Automated mismatch detection",
            "Debugging and compliance support",
            "Mitigation of stochasticity"
        ],
        primary_authority=[
            "NIST FIPS PUB 180-4 - Secure Hash Standard (SHS).",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "IEEE Standard 1012-2016 - Software Verification and Validation.",
            "ISO/IEC 12207:2017 - Systems and software engineering — Software life cycle processes.",
            "Goodman, B., & Flaxman, S. (2017). European Union regulations on algorithmic decision-making and a “right to explanation”. AI Magazine."
        ],
        burden_holder="Engine developers and quality assurance teams",
        adversary_position="Adversaries may exploit non-determinism to inject undetected malicious outputs.",
        counter_arguments=[
            "Some AI models inherently include stochastic elements for creativity or generalization.",
            "Strict determinism may reduce model flexibility or performance.",
            "Environmental differences can cause unavoidable output variation.",
            "Hash verification requires comprehensive logging and storage.",
            "Cross-engine determinism may be impractical due to architectural differences."
        ],
        resolution_strategy=(
            "Standardize environments and model versions rigorously. "
            "Use deterministic inference modes where feasible. "
            "Log inputs, outputs, and hashes comprehensively. "
            "Implement automated hash comparison and alerting. "
            "Document and justify acceptable non-determinism cases."
        ),
        entity_scope="All query processing and output generation components",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NIST FIPS PUB 180-4"
    ),
    DoctrineBlock(
        topic="Secret Scanning",
        keywords=["secret scanning", "API key detection", "credential leakage", "output monitoring", "security", "data leakage prevention", "pattern matching", "incident response"],
        conclusion_template=(
            "Secret scanning detects leaked API keys and credentials in engine outputs. "
            "Prompt identification and remediation prevent security breaches."
        ),
        reasoning_framework=(
            "Secret scanning involves automated detection of sensitive information such as API keys, passwords, and credentials in engine outputs or logs. "
            "Pattern matching, regular expressions, and machine learning models identify potential secrets. "
            "Detection must be real-time to enable rapid response and minimize exposure. "
            "Secret scanning complements input validation and output sanitization to prevent leakage. "
            "Integration with incident response workflows ensures timely remediation including key revocation and forensic analysis. "
            "False positives are managed via tuning and human review to avoid alert fatigue. "
            "Secret scanning supports compliance with standards like PCI DSS, HIPAA, and GDPR. "
            "Audit trails document detected leaks and response actions for accountability. "
            "Continuous updates to secret patterns and threat intelligence improve detection efficacy. "
            "Secret scanning is critical in multi-engine environments with complex data flows."
        ),
        key_factors=[
            "Pattern matching and regex for secrets",
            "Real-time detection and alerting",
            "Integration with incident response",
            "False positive management",
            "Compliance with security standards",
            "Audit trail documentation",
            "Continuous pattern updates"
        ],
        primary_authority=[
            "OWASP Secret Detection Cheat Sheet.",
            "PCI DSS v4.0 - Payment Card Industry Data Security Standard.",
            "NIST SP 800-53 Rev. 5 - Security and Privacy Controls.",
            "HIPAA Security Rule - Protection of electronic protected health information.",
            "GitGuardian. (2021). State of Secret Sprawl Report."
        ],
        burden_holder="Security operations and output validation teams",
        adversary_position="Attackers may attempt to exfiltrate secrets via engine outputs or logs.",
        counter_arguments=[
            "Pattern matching may miss novel or obfuscated secrets.",
            "False positives can overwhelm security teams.",
            "Real-time scanning adds processing overhead.",
            "Secret scanning may not cover all output channels.",
            "Remediation depends on organizational response capabilities."
        ],
        resolution_strategy=(
            "Deploy layered secret scanning combining regex, ML, and heuristics. "
            "Integrate with automated alerting and incident response. "
            "Regularly update secret patterns and train analysts. "
            "Balance detection sensitivity to minimize false positives. "
            "Maintain comprehensive audit trails of detection and remediation."
        ),
        entity_scope="All engine outputs and logs accessible externally or internally",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OWASP Secret Detection Cheat Sheet"
    ),
    DoctrineBlock(
        topic="Access Control Enforcement",
        keywords=["access control", "authorization", "authentication", "role-based access", "engine querying", "security policies", "least privilege", "identity management"],
        conclusion_template=(
            "Strict access control manages who can query which engines and with what permissions. "
            "Enforcing least privilege minimizes attack surface and unauthorized access."
        ),
        reasoning_framework=(
            "Access control enforcement ensures that only authorized users or systems can interact with specific AI engines or data. "
            "Authentication verifies identity, while authorization determines allowed actions based on roles or attributes. "
            "Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC) models provide flexible frameworks. "
            "Least privilege principles restrict permissions to the minimum necessary for function. "
            "Access control integrates with audit trails to log access attempts and policy violations. "
            "Multi-factor authentication (MFA) enhances identity assurance. "
            "Access policies must be regularly reviewed and updated to reflect organizational changes. "
            "Failure to enforce access control can lead to data breaches, unauthorized model manipulation, and compliance violations. "
            "Automated enforcement mechanisms reduce human error and improve scalability. "
            "Access control is foundational to security posture and risk management."
        ),
        key_factors=[
            "Authentication mechanisms",
            "Authorization models (RBAC, ABAC)",
            "Least privilege enforcement",
            "Audit logging of access events",
            "Multi-factor authentication",
            "Policy review and update processes",
            "Automated enforcement tools"
        ],
        primary_authority=[
            "NIST SP 800-63B - Digital Identity Guidelines: Authentication and Lifecycle Management.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "CIS Controls v8 - Control 6: Access Control Management.",
            "OWASP API Security Top 10.",
            "HIPAA Security Rule - Access Control."
        ],
        burden_holder="Identity and access management teams",
        adversary_position="Adversaries attempt privilege escalation or unauthorized access to sensitive engines or data.",
        counter_arguments=[
            "Complex access control policies may hinder legitimate user productivity.",
            "Misconfigurations can create security gaps.",
            "User resistance to MFA or strict controls.",
            "Dynamic environments challenge policy currency.",
            "Automated enforcement may produce false denials."
        ],
        resolution_strategy=(
            "Implement standardized identity and access management frameworks. "
            "Conduct regular access reviews and audits. "
            "Provide user training and support for security controls. "
            "Use automated policy enforcement with exception handling. "
            "Integrate access control logs with SIEM for monitoring."
        ),
        entity_scope="All user and system interactions with SENTINEL-X engines",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-63B"
    ),
    DoctrineBlock(
        topic="Rate Limit Monitoring",
        keywords=["rate limiting", "query patterns", "abuse detection", "throttling", "denial of service prevention", "anomaly detection", "traffic shaping", "security monitoring"],
        conclusion_template=(
            "Monitoring query rates detects unusual patterns indicative of abuse or attacks. "
            "Rate limiting and throttling protect system availability and integrity."
        ),
        reasoning_framework=(
            "Rate limit monitoring involves tracking the frequency and volume of queries to AI engines to identify abnormal usage patterns. "
            "Excessive or bursty query rates may indicate denial of service attacks, credential abuse, or automated scraping. "
            "Implementing rate limits enforces thresholds on query volume per user, IP, or API key. "
            "Anomaly detection algorithms analyze temporal and behavioral patterns to detect sophisticated abuse. "
            "Rate limiting protects system resources, maintains quality of service, and prevents degradation. "
            "Integration with access control and audit trails enables correlation of abuse events with identities. "
            "Alerts and automated throttling respond to detected anomalies in real-time. "
            "Rate limit policies must balance security with user experience to avoid unnecessary disruptions. "
            "Historical data informs adaptive rate limit adjustments. "
            "Rate limit monitoring is a critical component of engine security posture."
        ),
        key_factors=[
            "Query volume and frequency thresholds",
            "Anomaly detection on usage patterns",
            "Integration with access control",
            "Automated throttling and alerting",
            "Balancing security and usability",
            "Historical usage baselines",
            "Audit trail correlation"
        ],
        primary_authority=[
            "OWASP API Security Top 10 - 2019.",
            "NIST SP 800-53 Rev. 5 - Security and Privacy Controls.",
            "Cloud Security Alliance - API Security Guidance.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "CIS Controls v8 - Control 13: Data Protection."
        ],
        burden_holder="Security operations and API management teams",
        adversary_position="Attackers may attempt to overwhelm engines or extract data via high-frequency queries.",
        counter_arguments=[
            "Rate limits may block legitimate high-volume users.",
            "Attackers may use distributed sources to evade limits.",
            "False positives in anomaly detection can disrupt service.",
            "Complex rate policies increase management overhead.",
            "Adaptive attackers may mimic normal usage patterns."
        ],
        resolution_strategy=(
            "Implement multi-dimensional rate limiting (per user, IP, API key). "
            "Use machine learning-based anomaly detection. "
            "Employ adaptive rate limits based on historical behavior. "
            "Integrate with incident response for escalated events. "
            "Continuously review and tune rate limit policies."
        ),
        entity_scope="All query interfaces to SENTINEL-X engines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OWASP API Security Top 10"
    ),
    DoctrineBlock(
        topic="Cross-Engine Consistency Checking",
        keywords=["cross-engine consistency", "output comparison", "discrepancy detection", "multi-model validation", "consensus mechanisms", "error detection", "model agreement", "quality assurance"],
        conclusion_template=(
            "Cross-engine consistency checking detects discrepancies in outputs for identical queries. "
            "Consensus mechanisms enhance reliability and error detection."
        ),
        reasoning_framework=(
            "Cross-engine consistency checking compares outputs generated by multiple AI engines on the same input queries to identify inconsistencies or errors. "
            "Discrepancies may indicate model drift, hallucination, or adversarial manipulation. "
            "Consensus mechanisms aggregate outputs to produce more reliable results or flag conflicts for review. "
            "This approach leverages diversity in model architectures and training data to improve robustness. "
            "Automated discrepancy detection triggers alerts and initiates investigation workflows. "
            "Cross-engine checks support audit trails and compliance by demonstrating output reliability. "
            "Challenges include aligning output formats, handling partial agreements, and managing latency. "
            "Consistency checking complements individual engine validation and monitoring. "
            "It also aids in confidence calibration by correlating confidence scores across engines. "
            "Cross-engine consistency is particularly valuable in high-stakes or regulated domains."
        ),
        key_factors=[
            "Output format alignment",
            "Discrepancy detection algorithms",
            "Consensus and aggregation methods",
            "Alerting and investigation workflows",
            "Integration with audit trails",
            "Latency and performance considerations",
            "Support for confidence calibration"
        ],
        primary_authority=[
            "Dietterich, T. G. (2000). Ensemble methods in machine learning. Multiple classifier systems, 1-15.",
            "Kuncheva, L. I. (2004). Combining pattern classifiers: methods and algorithms. John Wiley & Sons.",
            "NIST AI Risk Management Framework (Draft).",
            "ISO/IEC 2382-37:2017 - Artificial intelligence vocabulary.",
            "Goodman, B., & Flaxman, S. (2017). European Union regulations on algorithmic decision-making and a “right to explanation”. AI Magazine."
        ],
        burden_holder="Model validation and quality assurance teams",
        adversary_position="Adversaries may attempt to cause inconsistent outputs to confuse users or evade detection.",
        counter_arguments=[
            "Differences in model design may cause legitimate output variation.",
            "Consensus mechanisms may suppress novel or correct minority outputs.",
            "Cross-engine checks increase computational overhead.",
            "Latency in obtaining multiple outputs may impact responsiveness.",
            "Complexity in aligning heterogeneous outputs."
        ],
        resolution_strategy=(
            "Standardize output schemas and normalization. "
            "Develop robust discrepancy detection and consensus algorithms. "
            "Use asynchronous processing to mitigate latency. "
            "Incorporate human review for flagged inconsistencies. "
            "Document cross-engine validation results in audit trails."
        ),
        entity_scope="All AI engines within SENTINEL-X queried in parallel",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Dietterich, Multiple Classifier Systems, 2000"
    ),
    DoctrineBlock(
        topic="Version Integrity Verification",
        keywords=["version integrity", "code checksum", "SHA-256", "software supply chain", "tamper detection", "version control", "deployment verification", "system integrity"],
        conclusion_template=(
            "Verifying engine code versions via SHA-256 checksums ensures software integrity and prevents unauthorized modifications."
        ),
        reasoning_framework=(
            "Version integrity verification involves confirming that deployed engine code matches expected versions using cryptographic checksums such as SHA-256. "
            "This prevents unauthorized or malicious code changes that could compromise security or functionality. "
            "Checksums are computed on code binaries, configuration files, and dependencies. "
            "Verification occurs at deployment, startup, and periodically during runtime. "
            "Integration with version control systems and CI/CD pipelines ensures traceability of code changes. "
            "Supply chain security practices mitigate risks of compromised dependencies or build environments. "
            "Audit trails record verification results and any anomalies detected. "
            "Version integrity supports compliance with standards such as NIST SP 800-161 and ISO/IEC 27001. "
            "Automated alerts trigger incident response on integrity violations. "
            "Maintaining version integrity is fundamental to system trustworthiness and resilience."
        ),
        key_factors=[
            "SHA-256 checksums of code and configs",
            "Integration with version control and CI/CD",
            "Periodic runtime verification",
            "Supply chain security practices",
            "Audit trail documentation",
            "Automated alerting on violations",
            "Compliance with security standards"
        ],
        primary_authority=[
            "NIST SP 800-161 Rev. 1 - Supply Chain Risk Management Practices for Federal Information Systems and Organizations.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "CIS Controls v8 - Control 4: Secure Configuration of Enterprise Assets and Software.",
            "FIPS PUB 202 - SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions.",
            "OWASP Software Supply Chain Security."
        ],
        burden_holder="DevOps and security teams",
        adversary_position="Attackers may attempt to deploy modified or malicious engine code to subvert operations.",
        counter_arguments=[
            "Checksum verification requires secure storage and management of expected hashes.",
            "Frequent updates necessitate efficient verification processes.",
            "Supply chain complexity complicates comprehensive integrity assurance.",
            "False positives may disrupt operations.",
            "Integration challenges with diverse deployment environments."
        ],
        resolution_strategy=(
            "Automate checksum generation and verification in CI/CD pipelines. "
            "Securely store and manage expected hashes. "
            "Implement runtime integrity monitoring agents. "
            "Conduct supply chain risk assessments and audits. "
            "Integrate verification results with audit trails and alerting."
        ),
        entity_scope="All deployed engine code and dependencies",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-161 Rev. 1"
    ),
    DoctrineBlock(
        topic="Dependency Vulnerability Scanning",
        keywords=["dependency scanning", "CVE detection", "software vulnerabilities", "third-party libraries", "patch management", "security updates", "vulnerability databases", "risk mitigation"],
        conclusion_template=(
            "Regular scanning of engine dependencies for known CVEs enables timely patching and risk reduction."
        ),
        reasoning_framework=(
            "Dependency vulnerability scanning identifies known security flaws in third-party libraries and components used by AI engines. "
            "Automated tools cross-reference dependencies against vulnerability databases such as NVD and CVE repositories. "
            "Timely detection allows patching or mitigation before exploitation occurs. "
            "Dependency trees are analyzed to uncover transitive vulnerabilities. "
            "Integration with patch management systems streamlines update deployment. "
            "Vulnerability severity and exploitability guide prioritization. "
            "Audit trails document scanning results and remediation actions. "
            "Continuous scanning is necessary due to frequent vulnerability disclosures. "
            "Collaboration with software suppliers enhances awareness and response. "
            "Dependency vulnerability management is critical for maintaining overall system security posture."
        ),
        key_factors=[
            "Automated scanning tools",
            "Access to up-to-date vulnerability databases",
            "Analysis of direct and transitive dependencies",
            "Integration with patch management",
            "Severity-based prioritization",
            "Audit trail documentation",
            "Continuous scanning and monitoring"
        ],
        primary_authority=[
            "NIST SP 800-40 Rev. 3 - Guide to Enterprise Patch Management Technologies.",
            "CVE List - https://cve.mitre.org/",
            "National Vulnerability Database (NVD) - https://nvd.nist.gov/",
            "OWASP Dependency-Check Project.",
            "ISO/IEC 27001:2013 - Information security management systems."
        ],
        burden_holder="DevOps, security, and software supply chain teams",
        adversary_position="Attackers exploit unpatched vulnerabilities in dependencies to compromise engines.",
        counter_arguments=[
            "Dependency scanning may produce false positives or outdated alerts.",
            "Patch deployment may disrupt operations or introduce regressions.",
            "Complex dependency graphs complicate vulnerability attribution.",
            "Zero-day vulnerabilities remain undetectable until disclosed.",
            "Resource constraints limit scanning frequency and coverage."
        ],
        resolution_strategy=(
            "Implement automated, scheduled dependency scanning. "
            "Prioritize patching based on risk assessment. "
            "Test patches in staging environments before production deployment. "
            "Maintain an inventory of all dependencies and versions. "
            "Document scanning and remediation in audit trails."
        ),
        entity_scope="All software dependencies of SENTINEL-X engines",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-40 Rev. 3"
    ),
    DoctrineBlock(
        topic="Prompt Injection Detection",
        keywords=["prompt injection", "adversarial input", "manipulation detection", "input sanitization", "security", "AI behavior control", "attack mitigation", "natural language processing"],
        conclusion_template=(
            "Detecting prompt injection attacks protects AI engines from adversarial manipulation. "
            "Robust input sanitization and anomaly detection mitigate these threats."
        ),
        reasoning_framework=(
            "Prompt injection attacks attempt to manipulate AI engine behavior by embedding malicious instructions or payloads within input prompts. "
            "Detection involves analyzing inputs for suspicious patterns, commands, or attempts to override system instructions. "
            "Input sanitization removes or neutralizes potentially harmful content. "
            "Behavioral anomaly detection monitors output deviations indicative of injection success. "
            "Prompt injection can cause unauthorized data disclosure, policy violations, or system misuse. "
            "Mitigation requires multi-layered defenses including input validation, output monitoring, and access control. "
            "Audit trails capture injection attempts and responses for forensic analysis. "
            "Continuous updating of detection heuristics is necessary to counter evolving attack techniques. "
            "Collaboration with NLP experts enhances detection capabilities. "
            "Prompt injection detection is essential for maintaining AI system security and trust."
        ),
        key_factors=[
            "Suspicious pattern detection in inputs",
            "Input sanitization and normalization",
            "Behavioral anomaly monitoring",
            "Integration with access control",
            "Audit trail documentation",
            "Heuristic and ML-based detection",
            "Continuous update of detection rules"
        ],
        primary_authority=[
            "Carlini, N., et al. (2021). Extracting training data from large language models. USENIX Security Symposium.",
            "OpenAI. (2022). GPT-4 System Card.",
            "NIST AI Risk Management Framework (Draft).",
            "OWASP Top Ten 2021 - Injection.",
            "ISO/IEC 27001:2013 - Information security management systems."
        ],
        burden_holder="Input validation and security monitoring teams",
        adversary_position="Attackers craft inputs to bypass controls and manipulate AI outputs.",
        counter_arguments=[
            "Detection heuristics may produce false positives affecting usability.",
            "Sophisticated injections may evade pattern-based detection.",
            "Sanitization may degrade input quality or intent.",
            "Real-time detection adds processing overhead.",
            "Continuous rule updates require dedicated resources."
        ],
        resolution_strategy=(
            "Combine pattern matching with ML-based anomaly detection. "
            "Implement layered input sanitization. "
            "Monitor outputs for unexpected behavior. "
            "Integrate detection with incident response workflows. "
            "Maintain and update detection heuristics regularly."
        ),
        entity_scope="All AI input processing components",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Carlini et al., USENIX Security, 2021"
    ),
    DoctrineBlock(
        topic="Information Leakage Prevention",
        keywords=["information leakage", "data confidentiality", "output filtering", "sensitive data protection", "privacy", "data masking", "security controls", "compliance"],
        conclusion_template=(
            "Preventing information leakage safeguards sensitive data from unauthorized disclosure. "
            "Output filtering and masking enforce confidentiality and compliance."
        ),
        reasoning_framework=(
            "Information leakage occurs when sensitive or confidential data is inadvertently exposed through AI engine outputs or logs. "
            "Prevention involves identifying sensitive data elements and applying filtering, masking, or redaction before output generation. "
            "Data classification schemes support automated detection of sensitive content. "
            "Output validation enforces policies restricting disclosure of personal, proprietary, or regulated information. "
            "Privacy-enhancing technologies such as differential privacy and encryption complement leakage prevention. "
            "Audit trails document leakage prevention actions and incidents. "
            "Leakage prevention supports compliance with GDPR, HIPAA, CCPA, and other data protection regulations. "
            "Continuous monitoring and testing detect potential leakage vectors. "
            "User training and awareness reduce accidental disclosures. "
            "Effective leakage prevention is critical for maintaining user trust and legal compliance."
        ),
        key_factors=[
            "Sensitive data identification and classification",
            "Output filtering, masking, and redaction",
            "Integration with privacy-enhancing technologies",
            "Policy enforcement and compliance",
            "Audit trail documentation",
            "Continuous monitoring and testing",
            "User training and awareness"
        ],
        primary_authority=[
            "NIST SP 800-122 - Guide to Protecting the Confidentiality of Personally Identifiable Information (PII).",
            "General Data Protection Regulation (GDPR) - Articles 5 and 32.",
            "HIPAA Privacy and Security Rules.",
            "ISO/IEC 27018:2019 - Protection of personally identifiable information (PII) in public clouds.",
            "OWASP Top Ten 2021 - Sensitive Data Exposure."
        ],
        burden_holder="Data protection officers and output validation teams",
        adversary_position="Attackers exploit leakage to access confidential or personal data.",
        counter_arguments=[
            "Over-filtering may reduce output usefulness or accuracy.",
            "Complex data structures challenge automated detection.",
            "Leakage vectors may exist outside controlled outputs.",
            "User errors can cause accidental disclosures.",
            "Balancing privacy and utility is challenging."
        ],
        resolution_strategy=(
            "Implement automated sensitive data detection and masking. "
            "Enforce strict output validation policies. "
            "Use privacy-enhancing technologies where applicable. "
            "Conduct regular leakage testing and audits. "
            "Provide user training on data handling best practices."
        ),
        entity_scope="All output generation and logging components",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-122"
    ),
    DoctrineBlock(
        topic="Compliance Monitoring",
        keywords=["compliance monitoring", "regulatory adherence", "audit readiness", "policy enforcement", "risk management", "continuous monitoring", "governance", "reporting"],
        conclusion_template=(
            "Continuous compliance monitoring ensures engines meet applicable regulatory requirements. "
            "Automated enforcement and reporting support governance and risk management."
        ),
        reasoning_framework=(
            "Compliance monitoring involves ongoing assessment of AI engines against relevant laws, regulations, and organizational policies. "
            "It includes automated checks, audits, and reporting mechanisms to verify adherence to standards such as GDPR, HIPAA, SOX, and emerging AI-specific regulations. "
            "Policy enforcement integrates with access control, data protection, and output validation to maintain compliance. "
            "Continuous monitoring detects deviations or violations early, enabling prompt remediation. "
            "Governance frameworks define roles, responsibilities, and processes for compliance management. "
            "Audit trails provide evidence for internal and external audits. "
            "Risk management processes prioritize compliance efforts based on impact and likelihood. "
            "Reporting tools generate compliance status dashboards and regulatory filings. "
            "Effective compliance monitoring reduces legal exposure and enhances stakeholder trust. "
            "It requires collaboration across technical, legal, and operational teams."
        ),
        key_factors=[
            "Automated compliance checks",
            "Policy enforcement integration",
            "Continuous monitoring and alerts",
            "Governance and roles definition",
            "Audit trail and evidence management",
            "Risk-based prioritization",
            "Reporting and dashboarding"
        ],
        primary_authority=[
            "General Data Protection Regulation (GDPR).",
            "Health Insurance Portability and Accountability Act (HIPAA).",
            "Sarbanes-Oxley Act (SOX).",
            "NIST AI Risk Management Framework (Draft).",
            "ISO/IEC 27001:2013 - Information security management systems."
        ],
        burden_holder="Compliance officers and security teams",
        adversary_position="Non-compliance may result from negligence or deliberate circumvention.",
        counter_arguments=[
            "Compliance requirements may conflict or be ambiguous.",
            "Automated checks may not cover all regulatory nuances.",
            "Continuous monitoring requires significant resources.",
            "Rapid regulatory changes challenge policy currency.",
            "Overemphasis on compliance may hinder innovation."
        ],
        resolution_strategy=(
            "Develop comprehensive compliance frameworks. "
            "Automate monitoring and integrate with security controls. "
            "Maintain updated regulatory knowledge bases. "
            "Engage cross-functional teams for governance. "
            "Use audit trails for evidence and reporting."
        ),
        entity_scope="All SENTINEL-X engines and supporting systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GDPR and HIPAA"
    ),
    DoctrineBlock(
        topic="Incident Response Coordination",
        keywords=["incident response", "security events", "coordination", "containment", "remediation", "forensics", "communication", "recovery"],
        conclusion_template=(
            "Coordinated incident response ensures timely containment and remediation of security events. "
            "Effective communication and forensic analysis support recovery and prevention."
        ),
        reasoning_framework=(
            "Incident response coordination involves structured processes and communication channels to manage security incidents affecting AI engines. "
            "It includes detection, analysis, containment, eradication, recovery, and post-incident review phases. "
            "Coordination across technical teams, management, legal, and external stakeholders ensures comprehensive handling. "
            "Forensic analysis leverages audit trails and logs to understand incident scope and root causes. "
            "Clear roles and responsibilities facilitate efficient response. "
            "Communication plans manage internal and external notifications, including regulatory reporting. "
            "Incident response plans are regularly tested and updated to address emerging threats. "
            "Automation and orchestration tools accelerate response actions. "
            "Lessons learned feed back into security posture improvements. "
            "Effective incident response minimizes damage and restores trust."
        ),
        key_factors=[
            "Structured response phases",
            "Cross-team coordination",
            "Forensic analysis capabilities",
            "Communication and notification plans",
            "Regular testing and updates",
            "Automation and orchestration",
            "Post-incident review and learning"
        ],
        primary_authority=[
            "NIST SP 800-61 Rev. 2 - Computer Security Incident Handling Guide.",
            "ISO/IEC 27035-1:2016 - Information security incident management.",
            "SANS Institute Incident Handler's Handbook.",
            "GDPR Article 33 - Data breach notification.",
            "HIPAA Breach Notification Rule."
        ],
        burden_holder="Security operations and incident response teams",
        adversary_position="Attackers aim to maximize impact and evade detection during incidents.",
        counter_arguments=[
            "Incident response can be resource-intensive and disruptive.",
            "Coordination challenges may delay response.",
            "Incomplete forensic data may hinder analysis.",
            "Communication missteps can damage reputation.",
            "Rapidly evolving threats require adaptive plans."
        ],
        resolution_strategy=(
            "Develop and maintain comprehensive incident response plans. "
            "Conduct regular training and simulations. "
            "Leverage automation for detection and containment. "
            "Establish clear communication protocols. "
            "Perform thorough post-incident reviews and improvements."
        ),
        entity_scope="All SENTINEL-X engines and supporting infrastructure",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-61 Rev. 2"
    ),
    DoctrineBlock(
        topic="Forensic Analysis",
        keywords=["forensic analysis", "security incidents", "audit trail investigation", "evidence collection", "chain of custody", "root cause analysis", "digital forensics", "incident response"],
        conclusion_template=(
            "Forensic analysis investigates security incidents using audit trail data to establish root causes and support remediation."
        ),
        reasoning_framework=(
            "Forensic analysis is the systematic examination of audit trails, logs, and system artifacts to reconstruct security incidents affecting AI engines. "
            "It requires preserving the chain of custody to maintain evidentiary integrity. "
            "Analysis identifies attack vectors, timelines, affected components, and impact scope. "
            "Techniques include log correlation, timeline analysis, memory forensics, and malware examination. "
            "Findings support incident response, legal proceedings, and security improvements. "
            "Forensic readiness involves preparing systems and processes to facilitate efficient investigations. "
            "Integration with audit trail integrity and incident response coordination enhances effectiveness. "
            "Challenges include data volume, encryption, and anti-forensic tactics by adversaries. "
            "Continuous training and tool updates maintain forensic capabilities. "
            "Forensic analysis is essential for accountability and resilience."
        ),
        key_factors=[
            "Audit trail completeness and integrity",
            "Chain of custody procedures",
            "Log correlation and timeline reconstruction",
            "Forensic toolsets and expertise",
            "Integration with incident response",
            "Handling of encrypted or obfuscated data",
            "Continuous capability development"
        ],
        primary_authority=[
            "NIST SP 800-86 - Guide to Integrating Forensic Techniques into Incident Response.",
            "ISO/IEC 27037:2012 - Guidelines for identification, collection, acquisition and preservation of digital evidence.",
            "SANS Institute Digital Forensics and Incident Response.",
            "ACPO Good Practice Guide for Digital Evidence.",
            "ENISA - Guidelines for Incident Response and Forensics."
        ],
        burden_holder="Forensic analysts and security operations teams",
        adversary_position="Attackers may use anti-forensic techniques to hinder investigations.",
        counter_arguments=[
            "Forensic analysis can be time-consuming and resource-intensive.",
            "Incomplete or corrupted audit trails limit effectiveness.",
            "Legal and privacy constraints may restrict data access.",
            "Rapid incident progression may outpace analysis.",
            "Evolving attack techniques require continuous learning."
        ],
        resolution_strategy=(
            "Maintain forensic readiness with proper logging and preservation. "
            "Use advanced forensic tools and trained personnel. "
            "Establish clear legal and privacy frameworks. "
            "Integrate forensic findings with incident response. "
            "Continuously update capabilities and share intelligence."
        ),
        entity_scope="Security incident investigations across SENTINEL-X",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-86"
    ),
    DoctrineBlock(
        topic="Threat Modeling",
        keywords=["threat modeling", "attack vectors", "risk assessment", "security architecture", "vulnerability identification", "mitigation planning", "security design", "adversary analysis"],
        conclusion_template=(
            "Threat modeling identifies potential attack vectors against the engine network to inform mitigation strategies and secure design."
        ),
        reasoning_framework=(
            "Threat modeling is a structured process to identify, enumerate, and prioritize potential threats to AI engines and their supporting infrastructure. "
            "It involves understanding system architecture, data flows, trust boundaries, and attacker capabilities. "
            "Common methodologies include STRIDE, PASTA, and attack trees. "
            "Threat modeling informs risk assessments and guides security control selection. "
            "It enables proactive identification of vulnerabilities and design weaknesses. "
            "Collaboration across development, security, and operations teams ensures comprehensive coverage. "
            "Threat models are updated regularly to reflect system changes and emerging threats. "
            "Outputs include mitigation plans, security requirements, and testing strategies. "
            "Effective threat modeling reduces attack surface and improves resilience. "
            "It supports compliance with security frameworks and regulatory expectations."
        ),
        key_factors=[
            "System architecture and data flow analysis",
            "Identification of trust boundaries",
            "Use of structured methodologies (STRIDE, PASTA)",
            "Collaboration across teams",
            "Regular updates and reviews",
            "Integration with risk management",
            "Mitigation planning and testing"
        ],
        primary_authority=[
            "Shostack, A. (2014). Threat modeling: Designing for security. Wiley.",
            "NIST SP 800-154 - Guide to Data-Centric System Threat Modeling.",
            "OWASP Threat Modeling Cheat Sheet.",
            "ISO/IEC 27005:2018 - Information security risk management.",
            "Microsoft Security Development Lifecycle (SDL)."
        ],
        burden_holder="Security architects and risk management teams",
        adversary_position="Attackers exploit unmodeled threats and design flaws to compromise systems.",
        counter_arguments=[
            "Threat modeling can be time-consuming and complex.",
            "Incomplete models may miss critical threats.",
            "Rapid development cycles challenge model currency.",
            "Overemphasis on threats may hinder innovation.",
            "Requires cross-disciplinary expertise."
        ],
        resolution_strategy=(
            "Adopt iterative and scalable threat modeling approaches. "
            "Engage cross-functional teams early and continuously. "
            "Integrate threat modeling with development and operations. "
            "Use automated tools to augment manual analysis. "
            "Maintain living threat models updated with system changes."
        ),
        entity_scope="SENTINEL-X engine network and infrastructure",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Shostack, Threat Modeling, 2014"
    ),
    DoctrineBlock(
        topic="Penetration Testing",
        keywords=["penetration testing", "vulnerability assessment", "security testing", "ethical hacking", "attack simulation", "risk identification", "remediation", "security validation"],
        conclusion_template=(
            "Penetration testing simulates attacks to identify vulnerabilities before adversaries exploit them, enabling proactive remediation."
        ),
        reasoning_framework=(
            "Penetration testing involves authorized, simulated cyberattacks against AI engines and infrastructure to identify security weaknesses. "
            "Tests cover network, application, and operational layers. "
            "Ethical hackers use techniques such as vulnerability scanning, exploitation, social engineering, and privilege escalation. "
            "Findings inform risk prioritization and remediation efforts. "
            "Penetration tests validate the effectiveness of security controls and incident response capabilities. "
            "Regular testing is mandated by standards such as PCI DSS and ISO/IEC 27001. "
            "Test scope and rules of engagement are clearly defined to avoid unintended disruptions. "
            "Results are documented and integrated into security improvement plans. "
            "Penetration testing complements automated vulnerability scanning and continuous monitoring. "
            "It enhances security posture by exposing real-world attack vectors."
        ),
        key_factors=[
            "Authorized and scoped testing",
            "Use of diverse attack techniques",
            "Validation of security controls",
            "Integration with risk management",
            "Documentation and remediation tracking",
            "Compliance with standards",
            "Complementarity with automated tools"
        ],
        primary_authority=[
            "OWASP Testing Guide.",
            "NIST SP 800-115 - Technical Guide to Information Security Testing and Assessment.",
            "PCI DSS v4.0 - Penetration Testing Requirements.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "CREST Penetration Testing Standards."
        ],
        burden_holder="Security testing and red team teams",
        adversary_position="Attackers exploit untested vulnerabilities to compromise systems.",
        counter_arguments=[
            "Penetration testing may disrupt operations if not carefully managed.",
            "Tests provide a point-in-time assessment and may miss emerging threats.",
            "Resource constraints limit testing frequency and scope.",
            "False negatives may occur due to incomplete coverage.",
            "Requires skilled personnel and continuous training."
        ],
        resolution_strategy=(
            "Schedule regular, scoped penetration tests. "
            "Use a combination of internal and external testers. "
            "Integrate findings into continuous security improvement. "
            "Coordinate with operations to minimize impact. "
            "Maintain documentation and track remediation."
        ),
        entity_scope="SENTINEL-X engines and supporting infrastructure",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-115"
    ),
    DoctrineBlock(
        topic="Security Posture Scoring",
        keywords=["security posture", "scoring", "risk assessment", "continuous monitoring", "metrics", "benchmarking", "improvement tracking", "security maturity"],
        conclusion_template=(
            "Security posture scoring provides a continuous, quantitative assessment of system security, guiding improvements and benchmarking."
        ),
        reasoning_framework=(
            "Security posture scoring aggregates multiple security metrics into a composite score reflecting the overall security health of AI engines. "
            "Metrics include vulnerability counts, incident frequency, compliance status, patch levels, and configuration baselines. "
            "Continuous monitoring feeds real-time data into scoring models. "
            "Scores enable benchmarking against industry standards and internal targets. "
            "They support risk communication to stakeholders and prioritize remediation efforts. "
            "Scoring methodologies must be transparent, consistent, and adaptable to evolving threats. "
            "Integration with governance frameworks ensures alignment with organizational objectives. "
            "Security posture scores drive maturity models and continuous improvement cycles. "
            "Automated dashboards visualize scores and trends for operational awareness. "
            "Effective scoring enhances accountability and resource allocation."
        ),
        key_factors=[
            "Comprehensive security metrics",
            "Continuous data collection",
            "Transparent scoring methodology",
            "Benchmarking and trend analysis",
            "Integration with governance",
            "Visualization and reporting",
            "Support for risk-based decision making"
        ],
        primary_authority=[
            "NIST Cybersecurity Framework (CSF).",
            "CIS Controls v8.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "ENISA Threat Landscape Reports.",
            "Gartner Security and Risk Management Framework."
        ],
        burden_holder="Security management and governance teams",
        adversary_position="Adversaries exploit low security posture areas identified by scoring.",
        counter_arguments=[
            "Scoring models may oversimplify complex security realities.",
            "Data quality issues can skew scores.",
            "Scores may create false confidence or complacency.",
            "Rapid changes in threat landscape challenge scoring relevance.",
            "Resource constraints limit data collection and analysis."
        ],
        resolution_strategy=(
            "Develop multi-dimensional, validated scoring models. "
            "Ensure high-quality, comprehensive data inputs. "
            "Regularly review and update scoring methodologies. "
            "Use scores as one input among many in decision making. "
            "Communicate scores with context and caveats."
        ),
        entity_scope="Overall SENTINEL-X security environment",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NIST CSF"
    ),
    DoctrineBlock(
        topic="Patch Management",
        keywords=["patch management", "security updates", "vulnerability remediation", "deployment automation", "testing", "rollback", "change management", "compliance"],
        conclusion_template=(
            "Effective patch management tracks and applies security updates promptly, minimizing exposure to known vulnerabilities."
        ),
        reasoning_framework=(
            "Patch management encompasses the processes for acquiring, testing, deploying, and verifying software updates to AI engines and supporting infrastructure. "
            "Timely application of patches addresses security vulnerabilities and functional issues. "
            "Change management procedures ensure patches do not disrupt operations. "
            "Automated deployment tools increase efficiency and reduce human error. "
            "Rollback mechanisms provide recovery options in case of patch failures. "
            "Testing environments validate patches before production deployment. "
            "Patch management integrates with vulnerability scanning and incident response. "
            "Documentation and audit trails support compliance and accountability. "
            "Regular patch cycles and emergency patching address both planned and urgent needs. "
            "Effective patch management reduces attack surface and improves system stability."
        ),
        key_factors=[
            "Timely vulnerability assessment",
            "Automated deployment and rollback",
            "Testing and validation",
            "Change management integration",
            "Documentation and audit trails",
            "Compliance with standards",
            "Emergency patching procedures"
        ],
        primary_authority=[
            "NIST SP 800-40 Rev. 3 - Guide to Enterprise Patch Management Technologies.",
            "CIS Controls v8 - Control 7: Continuous Vulnerability Management.",
            "ISO/IEC 27001:2013 - Information security management systems.",
            "PCI DSS v4.0 - Patch Management Requirements.",
            "Microsoft Security Update Guide."
        ],
        burden_holder="DevOps and security teams",
        adversary_position="Attackers exploit unpatched vulnerabilities to compromise systems.",
        counter_arguments=[
            "Patch deployment may cause service disruptions.",
            "Testing delays patch application.",
            "Resource constraints limit patching frequency.",
            "Complex dependencies complicate patching.",
            "Emergency patches may introduce instability."
        ],
        resolution_strategy=(
            "Establish regular patch cycles with testing. "
            "Automate deployment with rollback capabilities. "
            "Prioritize patches based on risk. "
            "Maintain detailed documentation and audit trails. "
            "Coordinate emergency patching with incident response."
        ),
        entity_scope="All software components of SENTINEL-X",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NIST SP 800-40 Rev. 3"
    ),
    DoctrineBlock(
        topic="Backup Integrity Verification",
        keywords=["backup integrity", "data restoration", "verification", "disaster recovery", "data consistency", "backup testing", "storage security", "redundancy"],
        conclusion_template=(
            "Verifying backup integrity ensures data is complete and restorable, supporting disaster "
            "recovery objectives. Regular verification testing validates RTO/RPO targets. "
            "Cryptographic checksums detect silent corruption in backup archives."
        ),
        reasoning_framework=(
            "Evaluate backup verification: hash-based integrity checks, test restoration drills, "
            "cross-site replication validation. Monitor backup freshness, completeness, and encryption status. "
            "Implement 3-2-1 backup rule: 3 copies, 2 media types, 1 offsite."
        ),
        key_factors=[
            "Backup frequency and retention policies",
            "Cryptographic integrity verification (SHA-256)",
            "Restoration testing cadence and success rates",
            "Cross-region replication for disaster recovery",
            "Encryption at rest and in transit for backup data",
        ],
        primary_authority=[
            "NIST SP 800-184 Guide for Cybersecurity Event Recovery.",
            "ISO 22301:2019 Business Continuity Management Systems.",
            "NIST SP 800-34 Rev. 1 Contingency Planning Guide.",
        ],
        burden_holder="Backup verification and disaster recovery modules",
        adversary_position="Claims periodic backups without verification suffice",
        counter_arguments=[
            "Unverified backups may contain corrupted or incomplete data.",
            "Without test restores, RTO estimates are unreliable.",
            "Silent data corruption goes undetected without hash verification.",
            "Single-site backups fail during regional disasters.",
            "Unencrypted backups create data breach exposure risk.",
        ],
        resolution_strategy="Implement automated backup verification pipeline: create → hash → encrypt → replicate → test-restore → report, with alerts on any verification failure",
        entity_scope="ALL",
        confidence=0.95,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="NIST SP 800-184 recovery guidance; ISO 22301 business continuity requirements",
    ),
]

# ═══════════════════════════════════════════════════════════════
# PASS 3: ROUTING ENGINE + THREE-LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════

class SubEngineState(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNREACHABLE = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    SECURITY = auto()
    INTEGRITY = auto()
    ERROR_HEALING = auto()
    DRIFT = auto()
    AUDIT = auto()
    GENERAL = auto()

class RoutingMode(Enum):
    DEFAULT = auto()
    PARALLEL = auto()
    CASCADE = auto()
    MONITOR = auto()
    AUDIT = auto()

class SubEngineStatus:
    def __init__(self, state: SubEngineState, last_checked: float, latency: Optional[float]=None, error: Optional[str]=None):
        self.state = state
        self.last_checked = last_checked
        self.latency = latency
        self.error = error

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, categories: Set[IssueCategory], priority: int):
        self.engine_id = engine_id
        self.url = url
        self.categories = categories
        self.priority = priority

class QueryRequest:
    def __init__(self, text: str, mode: RoutingMode=RoutingMode.DEFAULT, meta: Optional[Dict[str, Any]]=None):
        self.text = text
        self.mode = mode
        self.meta = meta or {}

class RoutingDecision:
    def __init__(self, engines: List[SubEngineConfig], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, success: bool, latency: float, error: Optional[str]=None):
        self.engine_id = engine_id
        self.response = response
        self.success = success
        self.latency = latency
        self.error = error

# --- CIRCUIT BREAKER ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int=3, recovery_timeout: int=30, half_open_success: int=2):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.recovery_timeout = recovery_timeout
        self.failure_threshold = failure_threshold
        self.half_open_success = half_open_success
        self.half_open_success_count = 0

    def allow_request(self) -> bool:
        now = time.time()
        if self.state == CircuitBreakerState.OPEN:
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_success_count = 0
                return True
            return False
        return True

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_success_count += 1
            if self.half_open_success_count >= self.half_open_success:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def get_state(self):
        return self.state

# --- SUBENGINE HEALTH MONITOR ---

class SubEngineHealthMonitor:
    def __init__(self, subengine_configs: Dict[str, SubEngineConfig], health_ttl: int=30):
        self.subengine_configs = subengine_configs
        self.health_cache: Dict[str, SubEngineStatus] = {}
        self.health_ttl = health_ttl
        self.circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker() for eid in subengine_configs}
        self.lock = asyncio.Lock()

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        async with self.lock:
            now = time.time()
            cached = self.health_cache.get(engine_id)
            if cached and now - cached.last_checked < self.health_ttl:
                return cached
            config = self.subengine_configs[engine_id]
            cb = self.circuit_breakers[engine_id]
            if not cb.allow_request():
                status = SubEngineStatus(SubEngineState.UNREACHABLE, now, error="Circuit breaker open")
                self.health_cache[engine_id] = status
                return status
            try:
                latency, ok = await self._ping_engine(config.url, timeout=3)
                if ok:
                    cb.record_success()
                    status = SubEngineStatus(SubEngineState.HEALTHY, now, latency=latency)
                else:
                    cb.record_failure()
                    status = SubEngineStatus(SubEngineState.UNREACHABLE, now, error="Ping failed")
            except Exception as e:
                cb.record_failure()
                status = SubEngineStatus(SubEngineState.UNREACHABLE, now, error=str(e))
            self.health_cache[engine_id] = status
            return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        for eid in self.subengine_configs:
            results[eid] = await self.check_health(eid)
        return results

    async def get_healthy_engines(self) -> List[str]:
        healthy = []
        for eid, status in (await self.check_all_health()).items():
            if status.state == SubEngineState.HEALTHY:
                healthy.append(eid)
        return healthy

    async def _ping_engine(self, url: str, timeout: int=3) -> Tuple[float, bool]:
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        await resp.text()
                        latency = time.time() - start
                        return latency, True
                    else:
                        return time.time() - start, False
        except Exception:
            return time.time() - start, False

# --- QUERY ROUTER ---

class QueryRouter:
    CATEGORY_KEYWORDS = {
        IssueCategory.SECURITY: ["attack", "exploit", "intrusion", "breach", "vulnerability", "threat", "malware"],
        IssueCategory.INTEGRITY: ["tamper", "corrupt", "integrity", "checksum", "hash mismatch", "validation"],
        IssueCategory.ERROR_HEALING: ["error", "heal", "recover", "restore", "fix", "self-heal", "repair"],
        IssueCategory.DRIFT: ["drift", "anomaly", "outlier", "deviation", "baseline", "model drift"],
        IssueCategory.AUDIT: ["audit", "log", "trail", "compliance", "trace", "forensic"],
        IssueCategory.GENERAL: []
    }

    def __init__(self, subengine_configs: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.subengine_configs = subengine_configs
        self.health_monitor = health_monitor
        self.routing_rules = []  # List of (predicate, engine_ids)
        self.logger = logging.getLogger("QueryRouter")

    def add_routing_rule(self, predicate, engine_ids: List[str]):
        self.routing_rules.append((predicate, engine_ids))

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        engine_ids = self._apply_routing_rules(query)
        if not engine_ids:
            engines = self._select_engines(categories, query.mode)
        else:
            engines = [self.subengine_configs[eid] for eid in engine_ids if eid in self.subengine_configs]
        return RoutingDecision(engines, categories, query.mode)

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    matched.add(cat)
        if not matched:
            matched.add(IssueCategory.GENERAL)
        return list(matched)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        candidates = []
        for eid, config in self.subengine_configs.items():
            if any(cat in config.categories for cat in categories):
                candidates.append(config)
        if not candidates:
            candidates = list(self.subengine_configs.values())
        if mode == RoutingMode.PARALLEL:
            return sorted(candidates, key=lambda x: x.priority)
        elif mode == RoutingMode.CASCADE:
            return sorted(candidates, key=lambda x: x.priority)
        elif mode == RoutingMode.MONITOR:
            return list(self.subengine_configs.values())
        elif mode == RoutingMode.AUDIT:
            return [c for c in candidates if IssueCategory.AUDIT in c.categories]
        else:
            return sorted(candidates, key=lambda x: x.priority)[:2]
    
    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        for predicate, engine_ids in self.routing_rules:
            if predicate(query):
                return engine_ids
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        score = 0.0
        categories = self._classify_domain(query.text)
        for cat in categories:
            if cat in engine.categories:
                score += 1.0
        score += 1.0 / (1 + engine.priority)
        return score

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        self.logger.warning(f"Engine {engine_id} failed: {error}")
        fallback = []
        for eid, config in self.subengine_configs.items():
            if eid != engine_id:
                fallback.append(eid)
        return fallback

# --- SUBENGINE ORCHESTRATOR ---

class SubEngineOrchestrator:
    def __init__(self, subengine_configs: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.subengine_configs = subengine_configs
        self.health_monitor = health_monitor
        self.logger = logging.getLogger("SubEngineOrchestrator")

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, SubEngineResponse]:
        tasks = []
        for engine in engines:
            tasks.append(self._call_sub_engine(engine, query))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        responses = {}
        for engine, result in zip(engines, results):
            if isinstance(result, SubEngineResponse):
                responses[engine.engine_id] = result
            else:
                responses[engine.engine_id] = SubEngineResponse(engine.engine_id, None, False, 0, error=str(result))
        return responses

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Optional[SubEngineResponse]:
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            if resp.success:
                return resp
        return None

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.circuit_breakers[engine_config.engine_id]
        if not cb.allow_request():
            return SubEngineResponse(engine_config.engine_id, None, False, 0, error="Circuit breaker open")
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"text": query.text, "meta": query.meta}
                async with session.post(engine_config.url + "/query", json=payload, timeout=10) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return SubEngineResponse(engine_config.engine_id, data, True, latency)
                    else:
                        cb.record_failure()
                        return SubEngineResponse(engine_config.engine_id, None, False, latency, error=f"HTTP {resp.status}")
        except Exception as e:
            cb.record_failure()
            latency = time.time() - start
            return SubEngineResponse(engine_config.engine_id, None, False, latency, error=str(e))

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        merged = {}
        for resp in responses:
            if resp.success and isinstance(resp.response, dict):
                for k, v in resp.response.items():
                    if k not in merged:
                        merged[k] = v
                    else:
                        if isinstance(merged[k], list) and isinstance(v, list):
                            merged[k].extend(v)
                        elif isinstance(merged[k], dict) and isinstance(v, dict):
                            merged[k].update(v)
                        else:
                            merged[k] = v
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Simple consensus: majority vote on 'verdict' field if present
        verdicts = defaultdict(int)
        for resp in responses:
            if resp.success and resp.response and "verdict" in resp.response:
                verdicts[resp.response["verdict"]] += 1
        if verdicts:
            return max(verdicts.items(), key=lambda x: x[1])[0]
        return None

# --- EXAMPLE SUBENGINE CONFIGURATION ---

def build_subengine_configs():
    return {
        "AGI01_CORTEX": SubEngineConfig(
            engine_id="AGI01_CORTEX",
            url="http://agi01-cortex:8080",
            categories={IssueCategory.SECURITY, IssueCategory.INTEGRITY, IssueCategory.GENERAL},
            priority=1
        ),
        "AGI04_REFLEX": SubEngineConfig(
            engine_id="AGI04_REFLEX",
            url="http://agi04-reflex:8080",
            categories={IssueCategory.SECURITY, IssueCategory.ERROR_HEALING, IssueCategory.GENERAL},
            priority=2
        ),
        "GS343_ERROR_HEALING": SubEngineConfig(
            engine_id="GS343_ERROR_HEALING",
            url="http://gs343-error-healing:8080",
            categories={IssueCategory.ERROR_HEALING, IssueCategory.INTEGRITY},
            priority=3
        ),
        "DRIFT_WATCHER": SubEngineConfig(
            engine_id="DRIFT_WATCHER",
            url="http://drift-watcher:8080",
            categories={IssueCategory.DRIFT},
            priority=4
        ),
        "AUDIT_TRAIL": SubEngineConfig(
            engine_id="AUDIT_TRAIL",
            url="http://audit-trail:8080",
            categories={IssueCategory.AUDIT},
            priority=5
        ),
    }

# --- EXAMPLE USAGE ---

subengine_configs = build_subengine_configs()
health_monitor = SubEngineHealthMonitor(subengine_configs)
query_router = QueryRouter(subengine_configs, health_monitor)
orchestrator = SubEngineOrchestrator(subengine_configs, health_monitor)

# Add custom routing rule example:
def is_compliance_query(query: QueryRequest):
    return "compliance" in query.text.lower()

query_router.add_routing_rule(is_compliance_query, ["AUDIT_TRAIL"])

# The rest of the backbone engine would use these classes to route, dispatch, and aggregate sub-engine results.

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 40,
    AuthorityLevel.PRACTICE: 20,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, returns the dominant authority level by weight.
    If multiple share highest weight, returns the one with highest precedence in enum order.
    """
    if not sources:
        raise ValueError("No authority sources provided")

    max_weight = -1
    candidates = []
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            candidates = [source]
        elif weight == max_weight:
            candidates.append(source)

    if len(candidates) == 1:
        return candidates[0]

    # Tie-break by enum order (lowest enum value wins)
    return min(candidates, key=lambda x: x.value)

# ---------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "incontrovertibly",
    "beyond question", "unequivocally", "categorically", "absolutely",
    "incontestably", "manifestly", "patently", "indisputably", "unquestionably",
    "decisively", "conclusively", "irrefutably", "infallibly", "inerrably",
    "unequivocally", "without reservation", "without exception", "without fail",
    "beyond any doubt", "incontrovertible", "incontestable", "without controversy",
    "without dispute", "without challenge", "without hesitation", "without equivocation",
    "without ambiguity"
]

# Compile regex for banned phrases for performance
_banned_phrases_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(phrase) for phrase in BANNED_PHRASES) + r')\b',
    flags=re.IGNORECASE
)

class ConfidenceLevel(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Removes banned phrases from text and appends a disclosure caveat.
    Returns tuple of (cleaned_text, disclosure_caveat).
    """
    cleaned_text = _banned_phrases_pattern.sub("", text)
    # Normalize whitespace after removals
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

    disclosure_caveat = (
        "Note: This analysis avoids absolute assertions and acknowledges "
        "potential uncertainties inherent in the data and interpretation."
    )
    return cleaned_text, disclosure_caveat

def confidence_stratification(confidence_score: float) -> ConfidenceLevel:
    """
    Stratifies confidence score (0.0 to 1.0) into ConfidenceLevel categories.
    """
    if confidence_score >= 0.9:
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.75:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.5:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ---------------------------
# DEEP ANALYSIS
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decomposes a complex query into sub-issues based on doctrine keywords and logical splits.
    Returns list of sub-issue strings.
    """
    # Simple heuristic: split by semicolons, commas, and conjunctions "and", "or"
    # Also split by common legal issue separators like "whether", "if", "when"
    split_patterns = [
        r';', r',', r'\band\b', r'\bor\b', r'\bwhether\b', r'\bif\b', r'\bwhen\b'
    ]
    pattern = '|'.join(split_patterns)
    raw_issues = re.split(pattern, query, flags=re.IGNORECASE)
    issues = [issue.strip() for issue in raw_issues if issue.strip()]
    return issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Builds a dependency graph (DAG) of issues based on heuristic keyword dependencies.
    Returns a networkx DiGraph where nodes are issues and edges represent dependencies.
    """
    dag = nx.DiGraph()
    for issue in issues:
        dag.add_node(issue)

    # Heuristic: if issue A references terms in issue B, add edge B->A (B must be resolved before A)
    # For simplicity, use substring matching of key terms
    for i, issue_a in enumerate(issues):
        for j, issue_b in enumerate(issues):
            if i == j:
                continue
            # If issue_a contains key terms from issue_b, issue_b -> issue_a
            tokens_b = set(re.findall(r'\w+', issue_b.lower()))
            tokens_a = set(re.findall(r'\w+', issue_a.lower()))
            if tokens_b and tokens_b.intersection(tokens_a):
                dag.add_edge(issue_b, issue_a)

    # Remove cycles if any by breaking edges arbitrarily
    try:
        cycles = list(nx.find_cycle(dag))
        for edge in cycles:
            dag.remove_edge(*edge)
    except nx.NetworkXNoCycle:
        pass

    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs an eight-step resolution of the query using doctrines and sub-engine results.
    Returns a dict with detailed analysis and final conclusion.
    """
    # Steps (heuristic placeholders):
    # 1. Identify issues
    issues = multi_doctrine_decomposition(query)
    # 2. Build dependency graph
    dag = build_interaction_dag(issues)
    # 3. Gather doctrine references per issue
    doctrine_map = {issue: [] for issue in issues}
    for issue in issues:
        for doctrine in doctrines:
            if doctrine.lower() in issue.lower():
                doctrine_map[issue].append(doctrine)
    # 4. Aggregate sub-engine results per issue
    aggregated_results = {}
    for issue in issues:
        aggregated_results[issue] = sub_engine_results.get(issue, None)
    # 5. Resolve conflicts in sub-engine results per issue
    resolved_results = {}
    for issue, result in aggregated_results.items():
        if isinstance(result, list):
            # Simple conflict resolution: pick most frequent result
            counter = collections.Counter(result)
            resolved_results[issue] = counter.most_common(1)[0][0]
        else:
            resolved_results[issue] = result
    # 6. Synthesize intermediate conclusions
    intermediate_conclusions = {}
    for issue in issues:
        intermediate_conclusions[issue] = {
            "doctrines": doctrine_map.get(issue, []),
            "analysis": resolved_results.get(issue, None)
        }
    # 7. Final conclusion synthesis (concatenate intermediate conclusions)
    final_conclusion = " | ".join(
        f"{issue}: {intermediate_conclusions[issue]['analysis']}" for issue in issues
    )
    # 8. Confidence and epistemic guardrails application
    cleaned_conclusion, caveat = apply_epistemic_guardrails(final_conclusion)
    return {
        "issues": issues,
        "dependency_graph": dag,
        "intermediate_conclusions": intermediate_conclusions,
        "final_conclusion_raw": final_conclusion,
        "final_conclusion_cleaned": cleaned_conclusion,
        "disclosure_caveat": caveat
    }

def zoned_analysis(conclusion: str) -> Dict[str, str]:
    """
    Tags the conclusion with zones: PLANNING, REPORTING, AUDIT based on keywords and content.
    Returns dict with zone tags and rationale.
    """
    zones = {
        "PLANNING": ["plan", "strategy", "prepare", "anticipate", "forecast"],
        "REPORTING": ["report", "summary", "findings", "conclusion", "result"],
        "AUDIT": ["audit", "review", "compliance", "verification", "assessment"]
    }
    tags = set()
    rationale = []
    lower_conclusion = conclusion.lower()
    for zone, keywords in zones.items():
        for kw in keywords:
            if kw in lower_conclusion:
                tags.add(zone)
                rationale.append(f"Found keyword '{kw}' for zone '{zone}'")
                break
    if not tags:
        tags.add("REPORTING")
        rationale.append("Defaulted to REPORTING zone")
    return {
        "zones": ", ".join(sorted(tags)),
        "rationale": "; ".join(rationale)
    }

# ---------------------------
# FACT FRAGILITY SCORING
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Scores fact fragility on three axes:
    - verifiability: 0.0 (not verifiable) to 1.0 (fully verifiable)
    - recharacterization_risk: 0.0 (no risk) to 1.0 (high risk)
    - testimony_dependence: 0.0 (no dependence) to 1.0 (high dependence)
    Uses heuristics based on fact content.
    """
    fact_lower = fact.lower()

    # Verifiability heuristics
    verifiable_indicators = [
        r'\bdocumented\b', r'\brecorded\b', r'\bevidenced\b', r'\bconfirmed\b',
        r'\bverified\b', r'\bcorroborated\b', r'\bstatistical\b', r'\bdata\b',
        r'\breport\b', r'\blog\b', r'\btranscript\b', r'\bcontract\b'
    ]
    unverifiable_indicators = [
        r'\balleged\b', r'\bclaimed\b', r'\basserted\b', r'\breported\b',
        r'\bsaid\b', r'\baccording to\b', r'\buncorroborated\b', r'\bdisputed\b'
    ]
    verifiability_score = 0.5  # base
    for pattern in verifiable_indicators:
        if re.search(pattern, fact_lower):
            verifiability_score = max(verifiability_score, 0.9)
    for pattern in unverifiable_indicators:
        if re.search(pattern, fact_lower):
            verifiability_score = min(verifiability_score, 0.2)

    # Recharacterization risk heuristics
    risk_indicators = [
        r'\bambiguous\b', r'\bunclear\b', r'\bdisputed\b', r'\bcontradicted\b',
        r'\bconflicting\b', r'\buncertain\b', r'\binterpretation\b', r'\bsubjective\b'
    ]
    recharacterization_risk = 0.1  # base low risk
    for pattern in risk_indicators:
        if re.search(pattern, fact_lower):
            recharacterization_risk = max(recharacterization_risk, 0.8)

    # Testimony dependence heuristics
    testimony_indicators = [
        r'\bwitness\b', r'\btestified\b', r'\bdeposition\b', r'\bstatement\b',
        r'\binterview\b', r'\boral\b', r'\bverbal\b'
    ]
    testimony_dependence = 0.0
    for pattern in testimony_indicators:
        if re.search(pattern, fact_lower):
            testimony_dependence = max(testimony_dependence, 0.85)

    # Clamp scores between 0 and 1
    verifiability_score = min(max(verifiability_score, 0.0), 1.0)
    recharacterization_risk = min(max(recharacterization_risk, 0.0), 1.0)
    testimony_dependence = min(max(testimony_dependence, 0.0), 1.0)

    return {
        "verifiability": verifiability_score,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# ---------------------------
# SEMANTIC NORMALIZATION
# ---------------------------

_domain_term_mappings = {
    # 50+ domain term mappings for legal/security/integrity domain
    "plaintiff": "claimant",
    "defendant": "respondent",
    "contract": "agreement",
    "breach": "violation",
    "statute": "law",
    "regulation": "rule",
    "precedent": "case_law",
    "jurisdiction": "authority",
    "liability": "responsibility",
    "damages": "compensation",
    "negligence": "carelessness",
    "intent": "mens_rea",
    "evidence": "proof",
    "testimony": "statement",
    "witness": "observer",
    "appeal": "challenge",
    "settlement": "resolution",
    "discovery": "investigation",
    "indictment": "charge",
    "verdict": "decision",
    "sentence": "punishment",
    "plaintiffs": "claimants",
    "defendants": "respondents",
    "contracts": "agreements",
    "breaches": "violations",
    "statutes": "laws",
    "regulations": "rules",
    "precedents": "case_laws",
    "jurisdictions": "authorities",
    "liabilities": "responsibilities",
    "damages": "compensations",
    "negligences": "carelessnesses",
    "intents": "mens_reas",
    "evidences": "proofs",
    "testimonies": "statements",
    "witnesses": "observers",
    "appeals": "challenges",
    "settlements": "resolutions",
    "discoveries": "investigations",
    "indictments": "charges",
    "verdicts": "decisions",
    "sentences": "punishments",
    "contractual": "agreement_based",
    "liable": "responsible",
    "liable_for": "responsible_for",
    "due_diligence": "careful_investigation",
    "good_faith": "honest_intent",
    "bad_faith": "dishonest_intent",
    "force_majeure": "unforeseeable_event",
    "statutory_limitations": "legal_time_limits",
    "case_law_precedent": "prior_judicial_decision",
    "legal_entity": "juridical_person",
    "fiduciary_duty": "trust_responsibility",
    "intellectual_property": "ip_rights",
    "non_disclosure_agreement": "nda",
    "terms_and_conditions": "t_and_c",
    "power_of_attorney": "poa",
    "confidential_information": "secret_data",
    "material_breach": "significant_violation",
    "minor_breach": "insignificant_violation",
    "remedy": "legal_solution",
    "injunction": "court_order",
    "arbitration": "dispute_resolution",
    "mediation": "conflict_resolution",
    "litigation": "legal_proceeding",
    "jurisprudence": "legal_theory",
    "statutory_interpretation": "law_exegesis",
    "due_process": "fair_procedure",
    "burden_of_proof": "proof_responsibility",
    "preponderance_of_evidence": "majority_proof",
    "beyond_reasonable_doubt": "high_proof_standard",
    "mens_rea": "criminal_intent",
    "actus_reus": "criminal_act",
    "double_jeopardy": "repeat_prosecution",
    "habeas_corpus": "detention_review",
    "ex_post_facto": "retroactive_law",
    "stare_decisis": "precedent_rule",
    "res_judicata": "final_judgment",
    "prima_facie": "at_first_appearance",
    "pro_bono": "free_legal_service",
    "subpoena": "court_order_to_appear",
    "voir_dire": "jury_selection_process",
    "amicus_curiae": "friend_of_court",
    "perjury": "false_testimony",
    "tort": "civil_wrong",
    "equity": "fairness_principle",
    "statutory_law": "written_law",
    "common_law": "judge_made_law",
    "legal_precedent": "prior_case_decision",
    "legal_opinion": "lawyer_advice",
    "legal_brief": "case_summary",
    "legal_remedy": "court_solution",
    "legal_standing": "right_to_sue",
    "legal_capacity": "ability_to_contract",
    "legal_duty": "obligation",
    "legal_right": "entitlement",
    "legal_liability": "legal_responsibility",
    "legal_claim": "demand",
    "legal_defense": "justification",
    "legal_evidence": "proof_material",
    "legal_testimony": "witness_statement",
    "legal_contract": "binding_agreement",
    "legal_document": "official_paper",
    "legal_procedure": "process",
    "legal_jurisdiction": "authority_area",
    "legal_entity": "organization",
    "legal_person": "individual_or_entity",
    "legal_action": "lawsuit",
    "legal_penalty": "punishment",
    "legal_fine": "monetary_penalty",
    "legal_sanction": "punitive_measure",
    "legal_enforcement": "implementation",
    "legal_compliance": "adherence",
    "legal_violation": "breach",
    "legal_infringement": "unauthorized_use",
    "legal_responsibility": "accountability",
    "legal_obligation": "duty",
    "legal_authority": "power",
    "legal_rights": "entitlements",
    "legal_duties": "obligations",
    "legal_liabilities": "responsibilities",
    "legal_claims": "demands",
    "legal_defenses": "justifications",
    "legal_evidences": "proofs",
    "legal_testimonies": "witness_statements",
    "legal_contracts": "binding_agreements",
    "legal_documents": "official_papers",
    "legal_procedures": "processes",
    "legal_jurisdictions": "authority_areas",
    "legal_entities": "organizations",
    "legal_persons": "individuals_or_entities",
    "legal_actions": "lawsuits",
    "legal_penalties": "punishments",
    "legal_fines": "monetary_penalties",
    "legal_sanctions": "punitive_measures",
    "legal_enforcements": "implementations",
    "legal_compliances": "adherences",
    "legal_violations": "breaches",
    "legal_infringements": "unauthorized_uses",
    "legal_responsibilities": "accountabilities",
    "legal_obligations": "duties",
    "legal_authorities": "powers",
    "legal_rights_plural": "entitlements_plural",
}

def normalize_query(text: str) -> str:
    """
    Normalizes domain-specific terms in the query text using _domain_term_mappings.
    Returns standardized text.
    """
    # Tokenize text preserving punctuation
    tokens = re.findall(r'\b\w+\b', text.lower())
    normalized_tokens = []
    for token in tokens:
        normalized = _domain_term_mappings.get(token, token)
        normalized_tokens.append(normalized)
    return " ".join(normalized_tokens)

# ---------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Simple in-memory doctrine cache with keyword matching.
    """

    def __init__(self):
        # Maps keyword to cached analysis
        self.cache: Dict[str, str] = {}

    def add_entry(self, keyword: str, analysis: str):
        self.cache[keyword.lower()] = analysis

    def lookup(self, query: str, timeout_ms: int = 200) -> Optional[str]:
        """
        Attempts to find cached analysis matching keywords in query within timeout.
        Returns cached analysis or None.
        """
        start_time = time.time()
        query_lower = query.lower()
        for keyword, analysis in self.cache.items():
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms > timeout_ms:
                break
            if keyword in query_lower:
                return analysis
        return None

# Sub-engines placeholder implementations

class SemanticSearchEngine:
    """
    Performs semantic search to identify relevant sub-engines based on query.
    """

    def __init__(self, sub_engines: Dict[str, Any]):
        self.sub_engines = sub_engines

    def search(self, query: str) -> List[str]:
        """
        Returns list of sub-engine keys relevant to the query.
        Simple heuristic: match sub-engine names or keywords in query.
        """
        query_lower = query.lower()
        relevant = []
        for key in self.sub_engines.keys():
            if key.lower() in query_lower:
                relevant.append(key)
        # If none matched, return all as fallback
        if not relevant:
            relevant = list(self.sub_engines.keys())
        return relevant

class SubEngineBase:
    """
    Base class for sub-engines.
    """

    def analyze(self, query: str) -> Any:
        """
        Analyze the query and return result.
        """
        raise NotImplementedError()

class ExampleSubEngine(SubEngineBase):
    """
    Example sub-engine that returns dummy analysis.
    """

    def __init__(self, name: str):
        self.name = name

    def analyze(self, query: str) -> str:
        time.sleep(0.05)  # simulate processing delay
        return f"Analysis by {self.name} for query: {query}"

class ThreeLayerResponseSystem:
    """
    Implements the three-layer response system:
    Layer 1: Doctrine cache lookup (0-200ms)
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis (parallel dispatch, merge, resolve conflicts)
    """

    def __init__(self, doctrine_cache: DoctrineCache, sub_engines: Dict[str, SubEngineBase]):
        self.doctrine_cache = doctrine_cache
        self.sub_engines = sub_engines
        self.semantic_search_engine = SemanticSearchEngine(sub_engines)

    def layer1_doctrine_cache_lookup(self, query: str) -> Optional[str]:
        """
        Layer 1: Attempt to return cached analysis within 200ms.
        """
        return self.doctrine_cache.lookup(query, timeout_ms=200)

    def layer2_semantic_search_routing(self, query: str) -> Dict[str, Any]:
        """
        Layer 2: Semantic search to find relevant sub-engines and dispatch query.
        Returns dict of sub-engine name to analysis result.
        """
        relevant_engines = self.semantic_search_engine.search(query)
        results = {}
        for engine_key in relevant_engines:
            engine = self.sub_engines.get(engine_key)
            if engine:
                results[engine_key] = engine.analyze(query)
        return results

    def layer3_deep_multi_engine_analysis(self, query: str) -> Dict[str, Any]:
        """
        Layer 3: Parallel dispatch to all sub-engines, merge results, resolve conflicts.
        Returns dict of sub-engine name to analysis result.
        """
        results = {}

        def analyze_engine(engine_key: str):
            engine = self.sub_engines[engine_key]
            return engine.analyze(query)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.sub_engines)) as executor:
            future_to_engine = {
                executor.submit(analyze_engine, key): key for key in self.sub_engines.keys()
            }
            for future in concurrent.futures.as_completed(future_to_engine):
                engine_key = future_to_engine[future]
                try:
                    result = future.result()
                except Exception as exc:
                    result = f"Error: {exc}"
                results[engine_key] = result

        # Conflict resolution: if multiple results differ, concatenate with tags
        unique_results = set(results.values())
        if len(unique_results) == 1:
            merged_result = unique_results.pop()
        else:
            merged_result = " | ".join(f"[{k}]: {v}" for k, v in results.items())

        return {
            "per_engine_results": results,
            "merged_result": merged_result
        }

    def respond(self, query: str) -> Dict[str, Any]:
        """
        Full three-layer response system.
        Returns dict with keys: layer1, layer2, layer3 results.
        """
        response = {}

        # Layer 1
        layer1_result = self.layer1_doctrine_cache_lookup(query)
        response['layer1'] = layer1_result
        if layer1_result is not None:
            # Early return if cache hit
            response['layer2'] = None
            response['layer3'] = None
            return response

        # Layer 2
        layer2_result = self.layer2_semantic_search_routing(query)
        response['layer2'] = layer2_result

        # Layer 3
        layer3_result = self.layer3_deep_multi_engine_analysis(query)
        response['layer3'] = layer3_result

        return response

# ---------------------------
# Example Initialization for Testing
# ---------------------------

doctrine_cache = DoctrineCache()
doctrine_cache.add_entry("contract breach", "Cached analysis: Contract breach doctrine applies with high likelihood.")
doctrine_cache.add_entry("negligence", "Cached analysis: Negligence standard requires duty, breach, causation, and damages.")

sub_engines = {
    "ContractEngine": ExampleSubEngine("ContractEngine"),
    "TortEngine": ExampleSubEngine("TortEngine"),
    "RegulatoryEngine": ExampleSubEngine("RegulatoryEngine"),
    "CaseLawEngine": ExampleSubEngine("CaseLawEngine"),
    "PracticeEngine": ExampleSubEngine("PracticeEngine"),
}

three_layer_system = ThreeLayerResponseSystem(doctrine_cache, sub_engines)

@dataclass
class QueryTelemetry:
    query_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    engines_invoked: List[str]
    mode: str
    confidence: float
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._lock = threading.Lock()
        self._queries: List[QueryTelemetry] = []
        self._errors: List[QueryTelemetry] = []
        self._doctrine_hits: Counter = Counter()
        self._sub_engine_stats: DefaultDict[str, List[float]] = defaultdict(list)
        self._cache_hits: int = 0
        self._cache_misses: int = 0

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            for engine in telemetry.engines_invoked:
                self._sub_engine_stats[engine].append(telemetry.latency_ms)
            if telemetry.cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1
            for engine in telemetry.engines_invoked:
                self._doctrine_hits[engine] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)

    def get_latency_stats(self) -> Dict[str, float]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries]
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies_sorted = sorted(latencies)
        avg = statistics.mean(latencies)
        min_latency = latencies_sorted[0]
        max_latency = latencies_sorted[-1]
        p50 = statistics.median(latencies_sorted)
        p95 = latencies_sorted[int(0.95 * len(latencies_sorted))-1]
        p99 = latencies_sorted[int(0.99 * len(latencies_sorted))-1]
        return dict(avg=avg, p50=p50, p95=p95, p99=p99, min=min_latency, max=max_latency)

    def get_doctrine_hit_rate(self) -> float:
        with self._lock:
            total = self._cache_hits + self._cache_misses
            if total == 0:
                return 0.0
            return self._cache_hits / total

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self._lock:
            return sum(1 for q in self._queries if q.timestamp >= cutoff)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, float]]:
        stats = {}
        with self._lock:
            for engine, latencies in self._sub_engine_stats.items():
                if latencies:
                    stats[engine] = {
                        "avg": statistics.mean(latencies),
                        "min": min(latencies),
                        "max": max(latencies),
                        "count": len(latencies)
                    }
                else:
                    stats[engine] = {
                        "avg": 0, "min": 0, "max": 0, "count": 0
                    }
        return stats

# --- 2. DRIFT_WATCHER ---

class DriftWatcher:
    def __init__(self):
        self._lock = threading.Lock()
        self._baselines: Dict[str, float] = {}  # doctrine -> baseline confidence
        self._history: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))  # doctrine -> [confidence]
        self._alerts: List[Tuple[str, float, float, float]] = []  # (doctrine, baseline, current, drift)

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            self._baselines[doctrine] = confidence

    def detect_drift(self, doctrine: str, confidence: float) -> Optional[Dict[str, Any]]:
        with self._lock:
            self._history[doctrine].append(confidence)
            baseline = self._baselines.get(doctrine)
            if baseline is None:
                return None
            current = statistics.mean(self._history[doctrine])
            if baseline == 0:
                return None
            drift = (current - baseline) / baseline
            if abs(drift) > 0.10:  # >10% shift
                self._alerts.append((doctrine, baseline, current, drift))
                return {
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "current": current,
                    "drift": drift,
                    "alert": True
                }
            return {
                "doctrine": doctrine,
                "baseline": baseline,
                "current": current,
                "drift": drift,
                "alert": False
            }

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self._lock:
            report = []
            for doctrine, baseline in self._baselines.items():
                history = self._history[doctrine]
                if history:
                    current = statistics.mean(history)
                    drift = (current - baseline) / baseline if baseline != 0 else 0
                    report.append({
                        "doctrine": doctrine,
                        "baseline": baseline,
                        "current": current,
                        "drift": drift,
                        "alert": abs(drift) > 0.10
                    })
            return report

# --- 3. COVERAGE_MAP ---

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._triggered: DefaultDict[str, int] = defaultdict(int)  # doctrine -> count
        self._missed: List[str] = []  # query_ids
        self._epistemic_gaps: List[str] = []  # query_ids
        self._sub_engine_coverage: DefaultDict[str, int] = defaultdict(int)

    def record_triggered(self, doctrine: str, query_id: str, sub_engine: Optional[str] = None):
        with self._lock:
            self._triggered[doctrine] += 1
            if sub_engine:
                self._sub_engine_coverage[sub_engine] += 1

    def record_missed(self, query_id: str):
        with self._lock:
            self._missed.append(query_id)

    def record_epistemic_gap(self, query_id: str):
        with self._lock:
            self._epistemic_gaps.append(query_id)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total = sum(self._triggered.values()) + len(self._missed)
            doctrine_coverage = {k: v for k, v in self._triggered.items()}
            sub_engine_coverage = {k: v for k, v in self._sub_engine_coverage.items()}
            epistemic_gap_count = len(self._epistemic_gaps)
            return {
                "total_queries": total,
                "doctrine_coverage": doctrine_coverage,
                "missed_queries": len(self._missed),
                "epistemic_gaps": epistemic_gap_count,
                "epistemic_gap_ids": list(self._epistemic_gaps),
                "sub_engine_coverage": sub_engine_coverage
            }

    def identify_epistemic_gaps(self, queries: List[Dict[str, Any]], doctrines: Set[str]):
        # queries: list of dicts with 'query_id' and 'doctrines_matched'
        with self._lock:
            for q in queries:
                if not q.get('doctrines_matched'):
                    self._epistemic_gaps.append(q['query_id'])

# --- 4. DETERMINISM_HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    # Deterministically serialize query and response
    def _serialize(obj):
        if isinstance(obj, dict):
            return {k: _serialize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [_serialize(x) for x in obj]
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif hasattr(obj, '__dict__'):
            return _serialize(obj.__dict__)
        else:
            return str(obj)
    data = {
        "query": _serialize(query),
        "response": _serialize(response)
    }
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    return compute_determinism_hash(query, response) == expected_hash

# --- 5. AUDIT_TRAIL ---

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        os.makedirs(audit_dir, exist_ok=True)
        self._lock = threading.Lock()
        self._current_date = None
        self._file = None

    def _get_audit_file(self):
        now = datetime.datetime.utcnow()
        date_str = now.strftime("%Y-%m-%d")
        if self._current_date != date_str or self._file is None:
            if self._file:
                self._file.close()
            filename = os.path.join(self.audit_dir, f"sentinelx_audit_{date_str}.jsonl")
            self._file = open(filename, "a", buffering=1)
            self._current_date = date_str
        return self._file

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        record = {
            "query_id": query_id,
            "timestamp": timestamp,
            "engine_id": engine_id,
            "engines_invoked": engines_invoked,
            "mode": mode,
            "confidence": confidence,
            "latency": latency,
            "cache_hit": cache_hit
        }
        with self._lock:
            f = self._get_audit_file()
            f.write(json.dumps(record, separators=(',', ':')) + "\n")

    def forensic_replay(self, date: str) -> List[Dict[str, Any]]:
        filename = os.path.join(self.audit_dir, f"sentinelx_audit_{date}.jsonl")
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self._lock:
            if self._file:
                self._file.close()
                self._file = None

# --- 6. PERFORMANCE_PROFILER ---

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.Lock()
        self._sub_engine_latency: DefaultDict[str, List[float]] = defaultdict(list)
        self._sub_engine_errors: DefaultDict[str, int] = defaultdict(int)
        self._sub_engine_invocations: DefaultDict[str, int] = defaultdict(int)
        self._sub_engine_availability: DefaultDict[str, List[bool]] = defaultdict(list)
        self._sub_engine_sla: Dict[str, Dict[str, float]] = {}  # engine -> {"max_latency": x, "max_error_rate": y, ...}
        self._sla_alerts: List[Dict[str, Any]] = []

    def record_invocation(self, engine: str, latency: float, error: Optional[str], available: bool):
        with self._lock:
            self._sub_engine_latency[engine].append(latency)
            self._sub_engine_invocations[engine] += 1
            if error:
                self._sub_engine_errors[engine] += 1
            self._sub_engine_availability[engine].append(available)

    def set_sla(self, engine: str, max_latency: float, max_error_rate: float, min_availability: float):
        with self._lock:
            self._sub_engine_sla[engine] = {
                "max_latency": max_latency,
                "max_error_rate": max_error_rate,
                "min_availability": min_availability
            }

    def get_engine_stats(self, engine: str) -> Dict[str, Any]:
        with self._lock:
            latencies = self._sub_engine_latency[engine]
            errors = self._sub_engine_errors[engine]
            invocations = self._sub_engine_invocations[engine]
            availabilities = self._sub_engine_availability[engine]
            error_rate = errors / invocations if invocations else 0
            avg_latency = statistics.mean(latencies) if latencies else 0
            min_latency = min(latencies) if latencies else 0
            max_latency = max(latencies) if latencies else 0
            availability = sum(availabilities) / len(availabilities) if availabilities else 1.0
            return {
                "avg_latency": avg_latency,
                "min_latency": min_latency,
                "max_latency": max_latency,
                "invocations": invocations,
                "error_rate": error_rate,
                "availability": availability
            }

    def check_sla(self, engine: str) -> Optional[Dict[str, Any]]:
        stats = self.get_engine_stats(engine)
        with self._lock:
            sla = self._sub_engine_sla.get(engine)
            if not sla:
                return None
            alerts = []
            if stats["avg_latency"] > sla["max_latency"]:
                alerts.append("latency")
            if stats["error_rate"] > sla["max_error_rate"]:
                alerts.append("error_rate")
            if stats["availability"] < sla["min_availability"]:
                alerts.append("availability")
            if alerts:
                alert = {
                    "engine": engine,
                    "violations": alerts,
                    "stats": stats,
                    "sla": sla
                }
                self._sla_alerts.append(alert)
                return alert
            return None

    def get_sla_alerts(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._sla_alerts)

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {engine: self.get_engine_stats(engine) for engine in self._sub_engine_latency}

    def reset(self):
        with self._lock:
            self._sub_engine_latency.clear()
            self._sub_engine_errors.clear()
            self._sub_engine_invocations.clear()
            self._sub_engine_availability.clear()
            self._sla_alerts.clear()

# ═══════════════════════════════════════════════════════════════
# PASS 6: FASTAPI SERVER (imports already at top of file)
# ═══════════════════════════════════════════════════════════════

# --- LOGGER SETUP ---
logger = logging.getLogger("sentinelx")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)

# --- CONSTANTS ---
ENGINE_ID = "AGI08"
ENGINE_NAME = "SENTINEL-X"
ENGINE_PORT = 8877

SUB_ENGINES = {
    "AGI01": {"name": "CORTEX", "url": "http://localhost:8801"},
    "AGI04": {"name": "REFLEX", "url": "http://localhost:8804"},
    "GS343": {"name": "Error Healing", "url": "http://localhost:8343"},
    "ALL": {"name": "All Engines Monitoring", "url": "http://localhost:8899"},
    "DRIFT": {"name": "Drift Watcher", "url": "http://localhost:8855"},
    "AUDIT": {"name": "Audit Trail", "url": "http://localhost:8866"},
}

# --- GLOBAL STATE ---
doctrine_cache: Dict[str, Dict[str, Any]] = {}
search_index: Dict[str, Set[str]] = {}
telemetry_data: Dict[str, Any] = {
    "latency_ms": [],
    "cache_hits": 0,
    "cache_misses": 0,
    "queries_total": 0,
    "subengine_stats": {},
}
routing_rules: Dict[str, List[str]] = {}
engine_registry: Dict[str, Dict[str, Any]] = {}
health_status: Dict[str, Dict[str, Any]] = {}
circuit_breakers: Dict[str, Dict[str, Any]] = {}
drift_report_cache: Optional[Dict[str, Any]] = None

# --- CONFIG ---
SUB_ENGINE_TIMEOUT = 5  # seconds
CIRCUIT_BREAKER_THRESHOLD = 3  # failures
CIRCUIT_BREAKER_RESET_TIME = 60  # seconds
CACHE_EXPIRY_SECONDS = 3600  # 1 hour cache expiry for doctrines

# --- UTILS ---


def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized


def classify_domain(query: str) -> str:
    # Dummy classifier based on keywords
    if "error" in query or "fail" in query:
        classification = "error"
    elif "security" in query or "attack" in query:
        classification = "security"
    elif "audit" in query or "log" in query:
        classification = "audit"
    else:
        classification = "general"
    logger.debug(f"Classified domain '{query}' as '{classification}'")
    return classification


def route_query(classification: str) -> List[str]:
    # Routing rules based on classification
    if classification == "error":
        engines = ["GS343", "AGI01"]
    elif classification == "security":
        engines = ["AGI04", "DRIFT", "AUDIT"]
    elif classification == "audit":
        engines = ["AUDIT", "ALL"]
    else:
        engines = ["AGI01", "AGI04", "GS343"]
    logger.debug(f"Routing for classification '{classification}': {engines}")
    return engines


def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {"results": [], "warnings": [], "errors": []}
    for resp in responses:
        if "results" in resp:
            merged["results"].extend(resp["results"])
        if "warnings" in resp:
            merged["warnings"].extend(resp["warnings"])
        if "errors" in resp:
            merged["errors"].extend(resp["errors"])
    logger.debug(f"Merged response: {merged}")
    return merged


def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Remove any sensitive info or sanitize output
    if "results" in response:
        sanitized = []
        for item in response["results"]:
            if isinstance(item, dict):
                item.pop("internal_notes", None)
                sanitized.append(item)
            else:
                sanitized.append(item)
        response["results"] = sanitized
    logger.debug("Applied guardrails to response")
    return response


def hash_response(response: Dict[str, Any]) -> str:
    serialized = json.dumps(response, sort_keys=True)
    h = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    logger.debug(f"Response hash: {h}")
    return h


def log_query(
    query: str,
    classification: str,
    routed_engines: List[str],
    response_hash: str,
    duration_ms: float,
    cache_hit: bool,
) -> None:
    telemetry_data["queries_total"] += 1
    telemetry_data["latency_ms"].append(duration_ms)
    if cache_hit:
        telemetry_data["cache_hits"] += 1
    else:
        telemetry_data["cache_misses"] += 1
    logger.info(
        f"Query logged: '{query}' classified as '{classification}', routed to {routed_engines}, "
        f"hash={response_hash}, duration={duration_ms:.2f}ms, cache_hit={cache_hit}"
    )


def is_circuit_open(engine_id: str) -> bool:
    cb = circuit_breakers.get(engine_id)
    if not cb:
        return False
    if cb["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
        elapsed = time.time() - cb["last_failure"]
        if elapsed < CIRCUIT_BREAKER_RESET_TIME:
            logger.warning(f"Circuit breaker OPEN for engine {engine_id}")
            return True
        else:
            # Reset circuit breaker
            circuit_breakers[engine_id] = {"failures": 0, "last_failure": 0}
            logger.info(f"Circuit breaker RESET for engine {engine_id}")
            return False
    return False


def record_failure(engine_id: str) -> None:
    cb = circuit_breakers.setdefault(engine_id, {"failures": 0, "last_failure": 0})
    cb["failures"] += 1
    cb["last_failure"] = time.time()
    logger.warning(f"Recorded failure for engine {engine_id}, count={cb['failures']}")


def record_success(engine_id: str) -> None:
    cb = circuit_breakers.setdefault(engine_id, {"failures": 0, "last_failure": 0})
    cb["failures"] = 0
    cb["last_failure"] = 0
    logger.debug(f"Recorded success for engine {engine_id}, circuit reset")


async def dispatch_to_subengine(
    engine_id: str, query: str
) -> Dict[str, Any]:
    if is_circuit_open(engine_id):
        return {
            "errors": [f"Circuit breaker open for engine {engine_id}"],
            "results": [],
            "warnings": [],
        }
    url = SUB_ENGINES.get(engine_id, {}).get("url")
    if not url:
        return {
            "errors": [f"Unknown sub-engine {engine_id}"],
            "results": [],
            "warnings": [],
        }
    try:
        async with httpx.AsyncClient(timeout=SUB_ENGINE_TIMEOUT) as client:
            resp = await client.post(
                f"{url}/process",
                json={"query": query, "engine_id": ENGINE_ID},
                headers={"X-Request-Source": ENGINE_ID},
            )
            resp.raise_for_status()
            record_success(engine_id)
            logger.debug(f"Sub-engine {engine_id} responded successfully")
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        record_failure(engine_id)
        logger.error(f"Error contacting sub-engine {engine_id}: {e}")
        return {
            "errors": [f"Failed to get response from {engine_id}: {str(e)}"],
            "results": [],
            "warnings": [],
        }


def fallback_to_doctrine_cache(query: str) -> Dict[str, Any]:
    cached = doctrine_cache.get(query)
    if cached:
        logger.info(f"Fallback to doctrine cache for query: {query}")
        return {"results": [cached], "warnings": [], "errors": []}
    else:
        logger.warning(f"No doctrine cache fallback available for query: {query}")
        return {
            "results": [],
            "warnings": [],
            "errors": ["No cached doctrine available for fallback"],
        }


def update_telemetry_subengine_stats(engine_id: str, response: Dict[str, Any]) -> None:
    stats = telemetry_data["subengine_stats"].setdefault(engine_id, {"calls": 0, "errors": 0})
    stats["calls"] += 1
    if response.get("errors"):
        stats["errors"] += 1


def seed_search_index_from_doctrine_cache() -> None:
    global search_index
    search_index.clear()
    for key, doctrine in doctrine_cache.items():
        words = set(key.split())
        for w in words:
            search_index.setdefault(w, set()).add(key)
    logger.info("Search index seeded from doctrine cache")


def doctrine_cache_expiry_cleanup() -> None:
    now = time.time()
    keys_to_delete = []
    for key, val in doctrine_cache.items():
        if val.get("cached_at", 0) + CACHE_EXPIRY_SECONDS < now:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del doctrine_cache[key]
    if keys_to_delete:
        logger.info(f"Expired {len(keys_to_delete)} doctrines from cache")


async def health_check_subengine(engine_id: str) -> Dict[str, Any]:
    url = SUB_ENGINES.get(engine_id, {}).get("url")
    if not url:
        return {"status": "unknown", "details": "No URL configured"}
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(f"{url}/health")
            resp.raise_for_status()
            data = resp.json()
            logger.debug(f"Health check success for {engine_id}")
            return {"status": "healthy", "details": data}
    except Exception as e:
        logger.error(f"Health check failed for {engine_id}: {e}")
        return {"status": "unhealthy", "details": str(e)}


async def start_health_monitor():
    while True:
        for engine_id in SUB_ENGINES.keys():
            status = await health_check_subengine(engine_id)
            health_status[engine_id] = status
        await asyncio.sleep(30)


async def start_telemetry_collector():
    # Placeholder for telemetry collection logic
    while True:
        # Could push telemetry to external system here
        await asyncio.sleep(60)


async def start_drift_watcher():
    global drift_report_cache
    while True:
        # Dummy drift detection logic: regenerate drift report every 5 minutes
        drift_report_cache = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "drift_detected": False,
            "details": "No drift detected in last interval",
        }
        logger.debug("Drift watcher updated report")
        await asyncio.sleep(300)


async def initialize_doctrine_cache():
    # Dummy loading of doctrines
    global doctrine_cache
    doctrine_cache.clear()
    doctrines = {
        "security breach": {
            "description": "Known patterns of security breaches",
            "cached_at": time.time(),
        },
        "system error": {
            "description": "Common system error resolutions",
            "cached_at": time.time(),
        },
        "audit log": {
            "description": "Audit log processing rules",
            "cached_at": time.time(),
        },
    }
    doctrine_cache.update(doctrines)
    logger.info("Doctrine cache initialized")


# --- Pydantic Models ---


class QueryRequest(BaseModel):
    query: str = Field(..., example="Detect security breach patterns")


class RouteDryRunRequest(BaseModel):
    query: str = Field(..., example="Check for system errors")


class AnalyzeRequest(BaseModel):
    query: str = Field(..., example="Deep analysis of audit logs")
    engines: Optional[List[str]] = Field(
        None, example=["AGI01", "GS343"], description="Sub-engines to include"
    )


class HealthResponse(BaseModel):
    engine_id: str
    status: str
    details: Any


class MetricsResponse(BaseModel):
    latency_avg_ms: float
    cache_hit_rate: float
    queries_per_hour: float
    subengine_stats: Dict[str, Dict[str, int]]


class CoverageResponse(BaseModel):
    doctrine_count: int
    epistemic_gaps: List[str]


class DriftResponse(BaseModel):
    timestamp: str
    drift_detected: bool
    details: str


class DoctrinesResponse(BaseModel):
    doctrines: List[str]


class RoutingResponse(BaseModel):
    routing_rules: Dict[str, List[str]]
    engine_registry: Dict[str, Dict[str, Any]]


class SubEnginesResponse(BaseModel):
    health: Dict[str, HealthResponse]


class QueryResponse(BaseModel):
    results: List[Any]
    warnings: List[str]
    errors: List[str]


# --- FASTAPI APP SETUP ---

app = FastAPI(title=ENGINE_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LIFESPAN MANAGEMENT ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting SENTINEL-X lifespan initialization")
    await initialize_doctrine_cache()
    seed_search_index_from_doctrine_cache()
    health_task = asyncio.create_task(start_health_monitor())
    telemetry_task = asyncio.create_task(start_telemetry_collector())
    drift_task = asyncio.create_task(start_drift_watcher())
    try:
        yield
    finally:
        health_task.cancel()
        telemetry_task.cancel()
        drift_task.cancel()
        logger.info("SENTINEL-X lifespan shutdown complete")


app.router.lifespan_context = lifespan


# --- ENDPOINTS ---


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
):
    start_time = time.time()
    query = normalize_query(request.query)

    # Check doctrine cache first
    cache_hit = False
    if query in doctrine_cache:
        cache_hit = True
        cached_response = {"results": [doctrine_cache[query]], "warnings": [], "errors": []}
        duration_ms = (time.time() - start_time) * 1000
        response_hash = hash_response(cached_response)
        log_query(query, "cache", [], response_hash, duration_ms, cache_hit)
        return cached_response

    classification = classify_domain(query)
    routed_engines = route_query(classification)

    # Dispatch concurrently to sub-engines
    tasks = []
    for engine_id in routed_engines:
        tasks.append(dispatch_to_subengine(engine_id, query))
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle exceptions in responses
    processed_responses = []
    for resp in responses:
        if isinstance(resp, Exception):
            processed_responses.append(
                {
                    "results": [],
                    "warnings": [],
                    "errors": [f"Sub-engine dispatch exception: {str(resp)}"],
                }
            )
        else:
            processed_responses.append(resp)

    # Merge responses
    merged_response = merge_responses(processed_responses)

    # If all sub-engines failed, fallback to doctrine cache
    if (
        len(merged_response["results"]) == 0
        and len(merged_response["errors"]) > 0
        and query in doctrine_cache
    ):
        fallback_response = fallback_to_doctrine_cache(query)
        duration_ms = (time.time() - start_time) * 1000
        response_hash = hash_response(fallback_response)
        log_query(query, classification, routed_engines, response_hash, duration_ms, True)
        return fallback_response

    # Apply guardrails
    guarded_response = apply_guardrails(merged_response)

    duration_ms = (time.time() - start_time) * 1000
    response_hash = hash_response(guarded_response)

    # Log telemetry
    log_query(query, classification, routed_engines, response_hash, duration_ms, cache_hit)
    for engine_id, resp in zip(routed_engines, processed_responses):
        update_telemetry_subengine_stats(engine_id, resp)

    return guarded_response


@app.get("/health", response_model=Dict[str, HealthResponse])
async def health_endpoint():
    # Compose comprehensive health report
    report = {}
    # Self health
    report[ENGINE_ID] = HealthResponse(
        engine_id=ENGINE_ID,
        status="healthy",
        details={"uptime": "running", "timestamp": datetime.utcnow().isoformat() + "Z"},
    )
    # Sub-engines health
    for engine_id, status in health_status.items():
        report[engine_id] = HealthResponse(
            engine_id=engine_id, status=status.get("status", "unknown"), details=status.get("details")
        )
    return report


@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latency_list = telemetry_data["latency_ms"]
    latency_avg = sum(latency_list) / len(latency_list) if latency_list else 0.0
    total_queries = telemetry_data["queries_total"]
    cache_hits = telemetry_data["cache_hits"]
    cache_hit_rate = cache_hits / total_queries if total_queries > 0 else 0.0
    # Queries per hour estimation (assuming uptime since start)
    uptime_hours = max((len(latency_list) * 0.001) / 3600, 1 / 3600)  # avoid div zero
    queries_per_hour = total_queries / uptime_hours

    return MetricsResponse(
        latency_avg_ms=latency_avg,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        subengine_stats=telemetry_data["subengine_stats"],
    )


@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    doctrine_count = len(doctrine_cache)
    # Epistemic gaps: dummy example - doctrines with empty description or missing keys
    gaps = []
    for key, val in doctrine_cache.items():
        if not val.get("description"):
            gaps.append(key)
    return CoverageResponse(doctrine_count=doctrine_count, epistemic_gaps=gaps)


@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    if drift_report_cache:
        return DriftResponse(**drift_report_cache)
    else:
        return DriftResponse(
            timestamp=datetime.utcnow().isoformat() + "Z",
            drift_detected=False,
            details="No drift report available",
        )


@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    return DoctrinesResponse(doctrines=list(doctrine_cache.keys()))


@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    # Provide routing rules and engine registry info
    rules = {
        "error": ["GS343", "AGI01"],
        "security": ["AGI04", "DRIFT", "AUDIT"],
        "audit": ["AUDIT", "ALL"],
        "general": ["AGI01", "AGI04", "GS343"],
    }
    registry = {eid: {"name": info["name"], "url": info["url"]} for eid, info in SUB_ENGINES.items()}
    return RoutingResponse(routing_rules=rules, engine_registry=registry)


@app.get("/sub-engines", response_model=SubEnginesResponse)
async def sub_engines_endpoint():
    health_resp = {}
    for eid, status in health_status.items():
        health_resp[eid] = HealthResponse(
            engine_id=eid, status=status.get("status", "unknown"), details=status.get("details")
        )
    return SubEnginesResponse(health=health_resp)


@app.post("/route", response_model=RoutingResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    query = normalize_query(request.query)
    classification = classify_domain(query)
    routed_engines = route_query(classification)
    rules = {
        "error": ["GS343", "AGI01"],
        "security": ["AGI04", "DRIFT", "AUDIT"],
        "audit": ["AUDIT", "ALL"],
        "general": ["AGI01", "AGI04", "GS343"],
    }
    registry = {eid: {"name": info["name"], "url": info["url"]} for eid, info in SUB_ENGINES.items()}
    return RoutingResponse(routing_rules=rules, engine_registry=registry)


@app.post("/analyze", response_model=QueryResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    query = normalize_query(request.query)
    engines = request.engines or list(SUB_ENGINES.keys())

    # Dispatch concurrently to specified sub-engines
    tasks = []
    for engine_id in engines:
        tasks.append(dispatch_to_subengine(engine_id, query))
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    processed_responses = []
    for resp in responses:
        if isinstance(resp, Exception):
            processed_responses.append(
                {
                    "results": [],
                    "warnings": [],
                    "errors": [f"Sub-engine dispatch exception: {str(resp)}"],
                }
            )
        else:
            processed_responses.append(resp)

    merged_response = merge_responses(processed_responses)
    guarded_response = apply_guardrails(merged_response)
    return guarded_response


# --- BACKGROUND TASKS ---


@app.on_event("startup")
async def on_startup():
    logger.info(f"{ENGINE_NAME} starting up on port {ENGINE_PORT}")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"{ENGINE_NAME} shutting down")


# --- PERIODIC TASKS ---


@app.on_event("startup")
async def start_periodic_tasks():
    asyncio.create_task(periodic_doctrine_cache_cleanup())


async def periodic_doctrine_cache_cleanup():
    while True:
        doctrine_cache_expiry_cleanup()
        await asyncio.sleep(300)  # every 5 minutes


# --- RUN SERVER ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")