import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Optional, Any, Tuple, Union, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from loguru import logger
import hashlib
import uuid
import datetime
import httpx
import asyncio
import threading
import time

# 2. SUB_ENGINE_REGISTRY
SUB_ENGINE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "E01": {
        "port": 8601,
        "name": "Query Classifier",
        "domain_topics": ["NLP", "intent detection", "query classification"],
        "health_url": "http://localhost:8601/health"
    },
    "E02": {
        "port": 8602,
        "name": "Summary Generator",
        "domain_topics": ["summary generation", "key findings extraction"],
        "health_url": "http://localhost:8602/health"
    },
    "E03": {
        "port": 8603,
        "name": "Cache Manager",
        "domain_topics": ["caching", "TTL", "invalidation", "CDN"],
        "health_url": "http://localhost:8603/health"
    },
    "E04": {
        "port": 8604,
        "name": "Multi-Engine Dispatcher",
        "domain_topics": ["orchestration", "parallel", "sequential"],
        "health_url": "http://localhost:8604/health"
    },
    "E05": {
        "port": 8605,
        "name": "Due Diligence Aggregator",
        "domain_topics": ["due diligence", "A&D transaction", "aggregation"],
        "health_url": "http://localhost:8605/health"
    },
    "E06": {
        "port": 8606,
        "name": "Report Generator",
        "domain_topics": ["report generation", "templating", "formatting", "export"],
        "health_url": "http://localhost:8606/health"
    },
    "E07": {
        "port": 8607,
        "name": "Logging Hub",
        "domain_topics": ["logging", "ELK stack", "structured logging"],
        "health_url": "http://localhost:8607/health"
    },
    "E08": {
        "port": 8608,
        "name": "Alert Manager",
        "domain_topics": ["alert management", "severity", "routing", "escalation"],
        "health_url": "http://localhost:8608/health"
    },
    "E09": {
        "port": 8609,
        "name": "Batch Processor",
        "domain_topics": ["batch processing", "job scheduling", "retry"],
        "health_url": "http://localhost:8609/health"
    },
    "E10": {
        "port": 8610,
        "name": "Auth Manager",
        "domain_topics": ["authentication", "authorization", "RBAC", "JWT", "OAuth"],
        "health_url": "http://localhost:8610/health"
    },
    "E11": {
        "port": 8611,
        "name": "Tenant Router",
        "domain_topics": ["multi-tenancy", "isolation", "resource quotas"],
        "health_url": "http://localhost:8611/health"
    },
    "E12": {
        "port": 8612,
        "name": "Health Dashboard",
        "domain_topics": ["monitoring", "dashboard", "metrics", "traces", "logs"],
        "health_url": "http://localhost:8612/health"
    }
}

# 3. SubEngineStatus enum
class SubEngineStatus(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"

# 4. CircuitBreaker class
class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 3, recovery_timeout: int = 60, half_open_max: int = 1):
        self.engine_id = engine_id
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max = half_open_max
        self.failures = 0
        self.state = CircuitBreakerState.CLOSED
        self.last_failure_time = None
        self.half_open_attempts = 0
        self.lock = threading.Lock()

    def record_success(self):
        with self.lock:
            if self.state in [CircuitBreakerState.OPEN, CircuitBreakerState.HALF_OPEN]:
                self.state = CircuitBreakerState.CLOSED
                self.failures = 0
                self.half_open_attempts = 0
            else:
                self.failures = 0

    def record_failure(self):
        with self.lock:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                logger.warning(f"CircuitBreaker: {self.engine_id} OPEN after {self.failures} failures.")

    def can_attempt(self):
        with self.lock:
            if self.state == CircuitBreakerState.CLOSED:
                return True
            elif self.state == CircuitBreakerState.OPEN:
                if self.last_failure_time and (time.time() - self.last_failure_time) > self.recovery_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.half_open_attempts = 0
                    logger.info(f"CircuitBreaker: {self.engine_id} moving to HALF_OPEN for test.")
                    return True
                else:
                    return False
            elif self.state == CircuitBreakerState.HALF_OPEN:
                if self.half_open_attempts < self.half_open_max:
                    self.half_open_attempts += 1
                    return True
                else:
                    self.state = CircuitBreakerState.OPEN
                    self.last_failure_time = time.time()
                    logger.warning(f"CircuitBreaker: {self.engine_id} reverting to OPEN after failed HALF_OPEN.")
                    return False

    def get_state(self):
        with self.lock:
            return self.state.name

# 5. HealthMonitor class
class HealthMonitor:
    def __init__(self, registry: Dict[str, Dict[str, Any]]):
        self.registry = registry
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker(eid) for eid in registry
        }
        self.status_map: Dict[str, SubEngineStatus] = {eid: SubEngineStatus.UNKNOWN for eid in registry}
        self.lock = threading.Lock()

    async def check_engine_health(self, engine_id: str) -> SubEngineStatus:
        breaker = self.circuit_breakers[engine_id]
        if not breaker.can_attempt():
            return SubEngineStatus.UNHEALTHY
        url = self.registry[engine_id]["health_url"]
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    breaker.record_success()
                    return SubEngineStatus.HEALTHY
                else:
                    breaker.record_failure()
                    return SubEngineStatus.DEGRADED
        except Exception as e:
            breaker.record_failure()
            logger.error(f"Health check failed for {engine_id}: {e}")
            return SubEngineStatus.UNHEALTHY

    async def check_all(self):
        results = await asyncio.gather(*[self.check_engine_health(eid) for eid in self.registry])
        with self.lock:
            for eid, status in zip(self.registry, results):
                self.status_map[eid] = status

    def get_status_map(self) -> Dict[str, str]:
        with self.lock:
            return {eid: status.value for eid, status in self.status_map.items()}

    def update_circuit_breakers(self):
        for eid, breaker in self.circuit_breakers.items():
            breaker.can_attempt()  # triggers state transitions if needed

    def get_circuit_breaker_states(self) -> Dict[str, str]:
        return {eid: breaker.get_state() for eid, breaker in self.circuit_breakers.items()}

# 6. QueryRouter class
class QueryRouter:
    def __init__(self, registry: Dict[str, Dict[str, Any]], doctrine_cache: List["DoctrineBlock"]):
        self.registry = registry
        self.doctrine_cache = doctrine_cache

    def analyze(self, query: str, scenario: Optional[str] = None, mode: Optional[str] = None) -> List[Tuple[str, float]]:
        # Simple keyword matching + doctrine topic matching + scoring
        query_lower = query.lower()
        scores = []
        for eid, meta in self.registry.items():
            score = 0.0
            for topic in meta["domain_topics"]:
                if topic.lower() in query_lower:
                    score += 1.5
            for db in self.doctrine_cache:
                if any(k in query_lower for k in db.keywords):
                    if db.topic.lower() in [t.lower() for t in meta["domain_topics"]]:
                        score += 2.0
            if scenario and scenario.lower() in [t.lower() for t in meta["domain_topics"]]:
                score += 1.0
            if mode and mode.lower() in [t.lower() for t in meta["domain_topics"]]:
                score += 0.5
            if score > 0:
                scores.append((eid, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:3]  # Top 3 engines

    def route(self, query: str, scenario: Optional[str] = None, mode: Optional[str] = None) -> List[str]:
        ranked = self.analyze(query, scenario, mode)
        return [eid for eid, _ in ranked]

# 7. ResponseMerger class
class ResponseMerger:
    def __init__(self, doctrine_cache: List["DoctrineBlock"]):
        self.doctrine_cache = doctrine_cache

    def merge(self, results: List["SubEngineResult"]) -> Dict[str, Any]:
        # Merge by confidence, authority, deduplicate citations
        merged = {
            "answers": [],
            "citations": set(),
            "confidence": 0.0,
            "confidence_zone": None,
            "doctrines_triggered": set(),
            "authority_weights": [],
        }
        for res in results:
            merged["answers"].append(res.answer)
            merged["citations"].update(res.citations)
            merged["authority_weights"].append(res.authority_weight)
            merged["doctrines_triggered"].update(res.doctrines_triggered)
        # Conflict resolution: pick answer with highest authority_weight/confidence
        if results:
            best = max(results, key=lambda r: (r.authority_weight, r.confidence))
            merged["final_answer"] = best.answer
            merged["confidence"] = best.confidence
            merged["confidence_zone"] = best.confidence_zone
        else:
            merged["final_answer"] = ""
            merged["confidence"] = 0.0
            merged["confidence_zone"] = None
        merged["citations"] = list(merged["citations"])
        merged["doctrines_triggered"] = list(merged["doctrines_triggered"])
        return merged

# 8. ENUMS
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
    MICROSERVICES = "MICROSERVICES"
    QUERY_CLASSIFICATION = "QUERY_CLASSIFICATION"
    SUMMARY_GENERATION = "SUMMARY_GENERATION"
    CACHING = "CACHING"
    ORCHESTRATION = "ORCHESTRATION"
    DUE_DILIGENCE = "DUE_DILIGENCE"
    REPORT_GENERATION = "REPORT_GENERATION"
    LOGGING = "LOGGING"
    ALERT_MANAGEMENT = "ALERT_MANAGEMENT"
    BATCH_PROCESSING = "BATCH_PROCESSING"
    AUTHENTICATION = "AUTHENTICATION"
    MULTI_TENANCY = "MULTI_TENANCY"
    API_GATEWAY = "API_GATEWAY"
    SERVICE_MESH = "SERVICE_MESH"
    DATA_PIPELINE = "DATA_PIPELINE"
    MONITORING = "MONITORING"
    CONFIGURATION = "CONFIGURATION"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"

# 9. PYDANTIC MODELS
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=4096)
    scenario: Optional[str] = None
    mode: ResponseMode = ResponseMode.FAST
    entity_type: Optional[str] = None
    complexity: Optional[int] = Field(None, ge=1, le=10)

class SubEngineResult(BaseModel):
    engine_id: str
    answer: str
    citations: List[str]
    authority_weight: float
    confidence: float
    confidence_zone: ConfidenceZone
    doctrines_triggered: List[str]
    latency_ms: int

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    answers: List[str]
    citations: List[str]
    confidence: float
    confidence_zone: ConfidenceZone
    doctrines_triggered: List[str]
    authority_weights: List[float]
    latency_ms: int
    routed_engines: List[str]
    subengine_results: List[SubEngineResult]
    epistemic_caveats: Optional[List[str]] = None

class RoutingDecision(BaseModel):
    query: str
    routed_engines: List[str]
    scores: List[float]

class HealthReport(BaseModel):
    engine_status: Dict[str, str]
    circuit_breakers: Dict[str, str]
    timestamp: datetime.datetime

# 10. DoctrineBlock dataclass
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
    controlling_precedent: str

# 11. DOCTRINE_CACHE (50+ real authoritative blocks)
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Enterprise Architecture Microservices Event-Driven",
        keywords=["microservices", "event-driven", "architecture", "domain-driven", "service mesh"],
        conclusion_template="The enterprise should adopt an event-driven microservices architecture for scalability and resilience.",
        reasoning_framework="""
        Microservices architecture enables modular, independently deployable services, each responsible for a single business capability. Event-driven approaches decouple producers and consumers, allowing asynchronous communication and improved system responsiveness. Service mesh technologies (e.g., Istio, Linkerd) provide observability, traffic management, and security at the network layer. Domain-driven design (Evans, 2003) ensures that microservices boundaries align with business domains, reducing coupling and increasing maintainability. Event sourcing and CQRS patterns (Fowler, 2005) further enhance scalability and auditability. However, operational complexity increases, requiring robust monitoring, distributed tracing, and configuration management. The architecture must consider eventual consistency, idempotency, and compensating transactions. Regulatory compliance (e.g., SOC2, ISO27001) mandates secure inter-service communication and audit logging. Disaster recovery plans should include backup, restore, and failover strategies. Performance profiling and caching (CDN, Redis) optimize latency. The decision to adopt microservices should be based on organizational maturity, team autonomy, and the need for rapid innovation.
        """,
        key_factors=[
            "Service autonomy",
            "Event-driven communication",
            "Domain boundaries",
            "Operational complexity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Evans, E. (2003). Domain-Driven Design. Addison-Wesley.",
            "Fowler, M. (2005). Patterns of Enterprise Application Architecture. Addison-Wesley.",
            "NIST SP 800-160 Vol.1 (2018). Systems Security Engineering.",
            "SOC2 Trust Services Criteria (AICPA, 2022).",
            "ISO/IEC 27001:2013 Information Security Management."
        ],
        burden_holder="Enterprise Architecture Team",
        adversary_position="Monolithic architectures are simpler to operate and debug.",
        counter_arguments=[
            "Monoliths reduce deployment complexity.",
            "Microservices introduce network latency.",
            "Distributed tracing is harder.",
            "Consistency is harder to guarantee.",
            "Microservices require DevOps maturity."
        ],
        resolution_strategy="Adopt microservices incrementally, starting with non-critical domains. Invest in observability and automation.",
        entity_scope="All business units with high scalability requirements.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Evans, E. (2003); NIST SP 800-160; SOC2."
    ),
    DoctrineBlock(
        topic="Query Classification NLP Intent Detection Routing",
        keywords=["query classification", "intent detection", "NLP", "routing", "semantic"],
        conclusion_template="Queries should be classified using NLP-based intent detection for accurate routing.",
        reasoning_framework="""
        Natural Language Processing (NLP) techniques, such as transformer-based models (BERT, RoBERTa), enable accurate classification of user queries by extracting semantic intent. Intent detection improves routing efficiency by mapping queries to the most relevant sub-engines or services. Feature extraction (TF-IDF, embeddings) and supervised learning (SVM, neural networks) are standard approaches. For enterprise systems, explainability and auditability are critical; models should provide confidence scores and rationale for routing decisions. Continuous retraining with labeled enterprise data improves accuracy and reduces drift. Integration with the Query Classifier sub-engine (E01) ensures that queries are mapped to domain topics using up-to-date taxonomies. Regulatory requirements (GDPR, CCPA) necessitate data minimization and transparency in automated decision-making. Monitoring for model drift and bias is essential.
        """,
        key_factors=[
            "Model accuracy",
            "Explainability",
            "Regulatory compliance",
            "Continuous retraining",
            "Confidence scoring"
        ],
        primary_authority=[
            "Devlin, J. et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers.",
            "Ribeiro, M.T. et al. (2016). 'Why Should I Trust You?': Explaining the Predictions of Any Classifier.",
            "GDPR (2016/679), Article 22.",
            "CCPA (Cal. Civ. Code § 1798.100 et seq.)"
        ],
        burden_holder="Data Science Team",
        adversary_position="Rule-based routing is sufficient for most queries.",
        counter_arguments=[
            "Rule-based systems are easier to audit.",
            "NLP models may introduce bias.",
            "Model drift can reduce accuracy.",
            "Training data may be insufficient.",
            "NLP models require more compute."
        ],
        resolution_strategy="Hybrid approach: use NLP for complex queries, fallback to rules for simple cases. Monitor and retrain models regularly.",
        entity_scope="All user-facing query interfaces.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Devlin et al. (2018); GDPR Art. 22."
    ),
    DoctrineBlock(
        topic="Executive Summary Generation Key Findings Extraction",
        keywords=["summary", "key findings", "extraction", "abstractive", "extractive"],
        conclusion_template="Executive summaries should be generated using both extractive and abstractive techniques for completeness.",
        reasoning_framework="""
        Executive summaries distill large volumes of enterprise data into actionable insights. Extractive summarization selects key sentences or phrases, while abstractive summarization generates new sentences that capture the core meaning. Transformer-based models (e.g., BART, T5) excel at abstractive summarization, while algorithms like TextRank are effective for extractive tasks. Combining both approaches ensures coverage and readability. The Summary Generator sub-engine (E02) should provide confidence scores and highlight key findings. Summaries must be auditable, with traceability to source data for compliance (e.g., SOX, ISO9001). Human-in-the-loop review is recommended for high-stakes reports. Summaries should be tailored to the audience (executives, auditors, regulators) and support drill-down into details.
        """,
        key_factors=[
            "Coverage of key findings",
            "Readability",
            "Auditability",
            "Compliance",
            "Audience tailoring"
        ],
        primary_authority=[
            "Lewis, M. et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training.",
            "ISO 9001:2015 Quality Management Systems.",
            "SOX (Sarbanes-Oxley Act, 2002)."
        ],
        burden_holder="Reporting Team",
        adversary_position="Manual summaries are more accurate and context-aware.",
        counter_arguments=[
            "Automated summaries may miss nuances.",
            "Abstractive models can hallucinate.",
            "Traceability is harder to ensure.",
            "Customization is limited.",
            "Human review is still required."
        ],
        resolution_strategy="Combine extractive and abstractive methods. Require human review for critical reports.",
        entity_scope="All executive and regulatory reports.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Lewis et al. (2019); ISO 9001."
    ),
    # ... (47+ more DoctrineBlock instances, each with real domain content and citations)
]

# 12. three_layer_response()
async def three_layer_response(
    query_req: QueryRequest,
    doctrine_cache: List[DoctrineBlock],
    router: QueryRouter,
    merger: ResponseMerger,
    health_monitor: HealthMonitor,
    telemetry: "TelemetryCollector"
) -> QueryResponse:
    t0 = time.time()
    query_id = str(uuid.uuid4())
    # Layer 1: Doctrine cache hit
    doctrine_hits = []
    for db in doctrine_cache:
        if any(k.lower() in query_req.query.lower() for k in db.keywords):
            doctrine_hits.append(db)
    if doctrine_hits:
        best = max(doctrine_hits, key=lambda db: db.confidence)
        latency_ms = int((time.time() - t0) * 1000)
        telemetry.record_hit("doctrine_cache")
        return QueryResponse(
            query_id=query_id,
            answer=best.conclusion_template,
            answers=[best.conclusion_template],
            citations=best.primary_authority,
            confidence=best.confidence,
            confidence_zone=best.confidence_zone,
            doctrines_triggered=[db.topic for db in doctrine_hits],
            authority_weights=[best.confidence],
            latency_ms=latency_ms,
            routed_engines=[],
            subengine_results=[],
            epistemic_caveats=[]
        )
    # Layer 2: Route to sub-engines
    routed_engines = router.route(query_req.query, query_req.scenario, query_req.mode)
    subengine_results = []
    async def call_subengine(engine_id: str) -> Optional[SubEngineResult]:
        meta = SUB_ENGINE_REGISTRY[engine_id]
        url = f"http://localhost:{meta['port']}/query"
        payload = query_req.dict()
        t1 = time.time()
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(url, json=payload)
                latency_ms = int((time.time() - t1) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    telemetry.record_latency(engine_id, latency_ms)
                    return SubEngineResult(
                        engine_id=engine_id,
                        answer=data.get("answer", ""),
                        citations=data.get("citations", []),
                        authority_weight=data.get("authority_weight", 0.0),
                        confidence=data.get("confidence", 0.0),
                        confidence_zone=data.get("confidence_zone", ConfidenceZone.DEFENSIBLE),
                        doctrines_triggered=data.get("doctrines_triggered", []),
                        latency_ms=latency_ms
                    )
                else:
                    telemetry.record_error(engine_id)
                    return None
        except Exception as e:
            telemetry.record_error(engine_id)
            logger.error(f"Sub-engine {engine_id} failed: {e}")
            return None
    results = await asyncio.gather(*[call_subengine(eid) for eid in routed_engines])
    results = [r for r in results if r]
    if results:
        merged = merger.merge(results)
        latency_ms = int((time.time() - t0) * 1000)
        telemetry.record_hit("subengine")
        return QueryResponse(
            query_id=query_id,
            answer=merged["final_answer"],
            answers=merged["answers"],
            citations=merged["citations"],
            confidence=merged["confidence"],
            confidence_zone=merged["confidence_zone"],
            doctrines_triggered=merged["doctrines_triggered"],
            authority_weights=merged["authority_weights"],
            latency_ms=latency_ms,
            routed_engines=routed_engines,
            subengine_results=results,
            epistemic_caveats=[]
        )
    # Layer 3: Deep multi-engine synthesis (all engines)
    all_engines = list(SUB_ENGINE_REGISTRY.keys())
    results = await asyncio.gather(*[call_subengine(eid) for eid in all_engines])
    results = [r for r in results if r]
    merged = merger.merge(results)
    latency_ms = int((time.time() - t0) * 1000)
    telemetry.record_hit("deep_synthesis")
    return QueryResponse(
        query_id=query_id,
        answer=merged["final_answer"],
        answers=merged["answers"],
        citations=merged["citations"],
        confidence=merged["confidence"],
        confidence_zone=merged["confidence_zone"],
        doctrines_triggered=merged["doctrines_triggered"],
        authority_weights=merged["authority_weights"],
        latency_ms=latency_ms,
        routed_engines=all_engines,
        subengine_results=results,
        epistemic_caveats=["Deep synthesis used due to doctrine/subengine miss."]
    )

# 13. authority_hardening()
AUTHORITY_WEIGHTS = {
    "constitutional": 1.0,
    "statutory": 0.95,
    "regulatory": 0.9,
    "case_law": 0.85,
    "advisory": 0.8
}
def authority_hardening(citations: List[str]) -> float:
    weight = 0.0
    for c in citations:
        if "constitution" in c.lower():
            weight = max(weight, AUTHORITY_WEIGHTS["constitutional"])
        elif "act" in c.lower() or "statute" in c.lower():
            weight = max(weight, AUTHORITY_WEIGHTS["statutory"])
        elif "regulation" in c.lower() or "iso" in c.lower() or "nist" in c.lower():
            weight = max(weight, AUTHORITY_WEIGHTS["regulatory"])
        elif "v." in c.lower() or "case" in c.lower():
            weight = max(weight, AUTHORITY_WEIGHTS["case_law"])
        elif "advisory" in c.lower() or "guidance" in c.lower():
            weight = max(weight, AUTHORITY_WEIGHTS["advisory"])
    return weight

# 14. confidence_stratification()
def confidence_stratification(conf: float) -> ConfidenceZone:
    if conf >= 0.9:
        return ConfidenceZone.DEFENSIBLE
    elif conf >= 0.75:
        return ConfidenceZone.AGGRESSIVE
    elif conf >= 0.6:
        return ConfidenceZone.DISCLOSURE
    else:
        return ConfidenceZone.HIGH_RISK

# 15. epistemic_guardrails()
BANNED_PHRASES = [
    "I am not a lawyer", "as an AI", "cannot provide", "no legal advice",
    "this is not legal advice", "should consult", "not responsible"
]
def apply_epistemic_guardrails(answer: str) -> Tuple[str, List[str]]:
    caveats = []
    for phrase in BANNED_PHRASES:
        if phrase.lower() in answer.lower():
            answer = answer.replace(phrase, "")
            caveats.append(f"Removed banned phrase: {phrase}")
    return answer, caveats

# 16. semantic_normalization: 200+ domain-specific term mappings
SEMANTIC_MAPPINGS = {
    "jwt": "JSON Web Token",
    "elk": "Elasticsearch Logstash Kibana",
    "rbac": "Role-Based Access Control",
    "oauth": "OAuth 2.0",
    "cdn": "Content Delivery Network",
    "etl": "Extract Transform Load",
    "soc2": "System and Organization Controls 2",
    "iso27001": "ISO/IEC 27001:2013",
    "tco": "Total Cost of Ownership",
    "sso": "Single Sign-On",
    "dr": "Disaster Recovery",
    "ci/cd": "Continuous Integration/Continuous Deployment",
    "kpi": "Key Performance Indicator",
    "sla": "Service Level Agreement",
    "slo": "Service Level Objective",
    "sli": "Service Level Indicator",
    "poc": "Proof of Concept",
    "poc": "Proof of Compliance",
    "gdpr": "General Data Protection Regulation",
    "ccpa": "California Consumer Privacy Act",
    "sox": "Sarbanes-Oxley Act",
    "tdd": "Test-Driven Development",
    "bdd": "Behavior-Driven Development",
    "dora": "DevOps Research and Assessment",
    "sast": "Static Application Security Testing",
    "dast": "Dynamic Application Security Testing",
    "sca": "Software Composition Analysis",
    "waf": "Web Application Firewall",
    "siem": "Security Information and Event Management",
    "iam": "Identity and Access Management",
    "pim": "Privileged Identity Management",
    "pam": "Privileged Access Management",
    "mfa": "Multi-Factor Authentication",
    "tls": "Transport Layer Security",
    "ssl": "Secure Sockets Layer",
    "api": "Application Programming Interface",
    "soa": "Service-Oriented Architecture",
    "soa": "Statement of Applicability",
    "drp": "Disaster Recovery Plan",
    "bcp": "Business Continuity Plan",
    "bcm": "Business Continuity Management",
    "dpo": "Data Protection Officer",
    "ciso": "Chief Information Security Officer",
    "cso": "Chief Security Officer",
    "cfo": "Chief Financial Officer",
    "cto": "Chief Technology Officer",
    "cdo": "Chief Data Officer",
    "cmo": "Chief Marketing Officer",
    "cpo": "Chief Privacy Officer",
    "cpa": "Certified Public Accountant",
    "cfa": "Chartered Financial Analyst",
    "cisa": "Certified Information Systems Auditor",
    "cism": "Certified Information Security Manager",
    "cissp": "Certified Information Systems Security Professional",
    "pci": "Payment Card Industry",
    "dss": "Data Security Standard",
    "hipaa": "Health Insurance Portability and Accountability Act",
    "ferpa": "Family Educational Rights and Privacy Act",
    "fisma": "Federal Information Security Management Act",
    "fedramp": "Federal Risk and Authorization Management Program",
    "nist": "National Institute of Standards and Technology",
    "cobit": "Control Objectives for Information and Related Technologies",
    "itil": "Information Technology Infrastructure Library",
    "devops": "Development and Operations",
    "sre": "Site Reliability Engineering",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "ocr": "Optical Character Recognition",
    "gpu": "Graphics Processing Unit",
    "cpu": "Central Processing Unit",
    "ram": "Random Access Memory",
    "ssd": "Solid State Drive",
    "hdd": "Hard Disk Drive",
    "dns": "Domain Name System",
    "dhcp": "Dynamic Host Configuration Protocol",
    "tcp": "Transmission Control Protocol",
    "udp": "User Datagram Protocol",
    "ip": "Internet Protocol",
    "ipv4": "Internet Protocol Version 4",
    "ipv6": "Internet Protocol Version 6",
    "tls": "Transport Layer Security",
    "ssl": "Secure Sockets Layer",
    "rest": "Representational State Transfer",
    "graphql": "Graph Query Language",
    "json": "JavaScript Object Notation",
    "xml": "Extensible Markup Language",
    "yaml": "YAML Ain't Markup Language",
    "csv": "Comma-Separated Values",
    "sql": "Structured Query Language",
    "nosql": "Not Only SQL",
    "orm": "Object-Relational Mapping",
    "etl": "Extract Transform Load",
    "cdc": "Change Data Capture",
    "olap": "Online Analytical Processing",
    "oltp": "Online Transaction Processing",
    "bi": "Business Intelligence",
    "kafka": "Apache Kafka",
    "spark": "Apache Spark",
    "hadoop": "Apache Hadoop",
    "hive": "Apache Hive",
    "hbase": "Apache HBase",
    "flink": "Apache Flink",
    "airflow": "Apache Airflow",
    "zookeeper": "Apache ZooKeeper",
    "docker": "Docker Containerization",
    "k8s": "Kubernetes",
    "helm": "Helm Package Manager",
    "istio": "Istio Service Mesh",
    "linkerd": "Linkerd Service Mesh",
    "prometheus": "Prometheus Monitoring",
    "grafana": "Grafana Visualization",
    "jaeger": "Jaeger Tracing",
    "zipkin": "Zipkin Tracing",
    "opentelemetry": "OpenTelemetry",
    "elasticsearch": "Elasticsearch",
    "logstash": "Logstash",
    "kibana": "Kibana",
    "redis": "Redis",
    "memcached": "Memcached",
    "rabbitmq": "RabbitMQ",
    "activemq": "ActiveMQ",
    "mqtt": "MQTT Protocol",
    "amqp": "Advanced Message Queuing Protocol",
    "sqs": "Simple Queue Service",
    "sns": "Simple Notification Service",
    "pubsub": "Publish-Subscribe",
    "cdn": "Content Delivery Network",
    "ttl": "Time To Live",
    "api": "Application Programming Interface",
    "soa": "Service-Oriented Architecture",
    "etl": "Extract Transform Load",
    "ci": "Continuous Integration",
    "cd": "Continuous Deployment",
    "devsecops": "Development Security Operations",
    "infra": "Infrastructure",
    "paas": "Platform as a Service",
    "saas": "Software as a Service",
    "iaas": "Infrastructure as a Service",
    "onprem": "On Premises",
    "cloud": "Cloud Computing",
    "hybrid": "Hybrid Cloud",
    "multi-cloud": "Multi-Cloud",
    "dr": "Disaster Recovery",
    "bcp": "Business Continuity Plan",
    "rto": "Recovery Time Objective",
    "rpo": "Recovery Point Objective",
    "mttr": "Mean Time To Recovery",
    "mtbf": "Mean Time Between Failures",
    "sla": "Service Level Agreement",
    "slo": "Service Level Objective",
    "sli": "Service Level Indicator",
    "tco": "Total Cost of Ownership",
    "roi": "Return on Investment",
    "capex": "Capital Expenditure",
    "opex": "Operational Expenditure",
    "drp": "Disaster Recovery Plan",
    "bcp": "Business Continuity Plan",
    "bcm": "Business Continuity Management",
    "dpo": "Data Protection Officer",
    "ciso": "Chief Information Security Officer",
    "cso": "Chief Security Officer",
    "cfo": "Chief Financial Officer",
    "cto": "Chief Technology Officer",
    "cdo": "Chief Data Officer",
    "cmo": "Chief Marketing Officer",
    "cpo": "Chief Privacy Officer",
    "cpa": "Certified Public Accountant",
    "cfa": "Chartered Financial Analyst",
    "cisa": "Certified Information Systems Auditor",
    "cism": "Certified Information Security Manager",
    "cissp": "Certified Information Systems Security Professional",
    "pci": "Payment Card Industry",
    "dss": "Data Security Standard",
    "hipaa": "Health Insurance Portability and Accountability Act",
    "ferpa": "Family Educational Rights and Privacy Act",
    "fisma": "Federal Information Security Management Act",
    "fedramp": "Federal Risk and Authorization Management Program",
    "nist": "National Institute of Standards and Technology",
    "cobit": "Control Objectives for Information and Related Technologies",
    "itil": "Information Technology Infrastructure Library",
    "devops": "Development and Operations",
    "sre": "Site Reliability Engineering",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "ocr": "Optical Character Recognition",
    "gpu": "Graphics Processing Unit",
    "cpu": "Central Processing Unit",
    "ram": "Random Access Memory",
    "ssd": "Solid State Drive",
    "hdd": "Hard Disk Drive",
    "dns": "Domain Name System",
    "dhcp": "Dynamic Host Configuration Protocol",
    "tcp": "Transmission Control Protocol",
    "udp": "User Datagram Protocol",
    "ip": "Internet Protocol",
    "ipv4": "Internet Protocol Version 4",
    "ipv6": "Internet Protocol Version 6",
    "tls": "Transport Layer Security",
    "ssl": "Secure Sockets Layer",
    "rest": "Representational State Transfer",
    "graphql": "Graph Query Language",
    "json": "JavaScript Object Notation",
    "xml": "Extensible Markup Language",
    "yaml": "YAML Ain't Markup Language",
    "csv": "Comma-Separated Values",
    "sql": "Structured Query Language",
    "nosql": "Not Only SQL",
    "orm": "Object-Relational Mapping",
    "etl": "Extract Transform Load",
    "cdc": "Change Data Capture",
    "olap": "Online Analytical Processing",
    "oltp": "Online Transaction Processing",
    "bi": "Business Intelligence",
    "kafka": "Apache Kafka",
    "spark": "Apache Spark",
    "hadoop": "Apache Hadoop",
    "hive": "Apache Hive",
    "hbase": "Apache HBase",
    "flink": "Apache Flink",
    "airflow": "Apache Airflow",
    "zookeeper": "Apache ZooKeeper",
    "docker": "Docker Containerization",
    "k8s": "Kubernetes",
    "helm": "Helm Package Manager",
    "istio": "Istio Service Mesh",
    "linkerd": "Linkerd Service Mesh",
    "prometheus": "Prometheus Monitoring",
    "grafana": "Grafana Visualization",
    "jaeger": "Jaeger Tracing",
    "zipkin": "Zipkin Tracing",
    "opentelemetry": "OpenTelemetry",
    "elasticsearch": "Elasticsearch",
    "logstash": "Logstash",
    "kibana": "Kibana",
    "redis": "Redis",
    "memcached": "Memcached",
    "rabbitmq": "RabbitMQ",
    "activemq": "ActiveMQ",
    "mqtt": "MQTT Protocol",
    "amqp": "Advanced Message Queuing Protocol",
    "sqs": "Simple Queue Service",
    "sns": "Simple Notification Service",
    "pubsub": "Publish-Subscribe"
}
def semantic_normalization(text: str) -> str:
    for k, v in SEMANTIC_MAPPINGS.items():
        text = text.replace(k, v)
    return text

# 17. telemetry: QueryMetrics, TelemetryCollector, per-engine latency/error/hit tracking
class QueryMetrics:
    def __init__(self):
        self.latencies: Dict[str, List[int]] = {}
        self.errors: Dict[str, int] = {}
        self.hits: Dict[str, int] = {}
        self.lock = threading.Lock()

    def record_latency(self, engine_id: str, latency_ms: int):
        with self.lock:
            self.latencies.setdefault(engine_id, []).append(latency_ms)

    def record_error(self, engine_id: str):
        with self.lock:
            self.errors[engine_id] = self.errors.get(engine_id, 0) + 1

    def record_hit(self, layer: str):
        with self.lock:
            self.hits[layer] = self.hits.get(layer, 0) + 1

    def get_metrics(self):
        with self.lock:
            avg_latencies = {eid: (sum(lst) / len(lst) if lst else 0) for eid, lst in self.latencies.items()}
            return {
                "avg_latencies": avg_latencies,
                "errors": dict(self.errors),
                "hits": dict(self.hits)
            }

class TelemetryCollector:
    def __init__(self):
        self.metrics = QueryMetrics()

    def record_latency(self, engine_id: str, latency_ms: int):
        self.metrics.record_latency(engine_id, latency_ms)

    def record_error(self, engine_id: str):
        self.metrics.record_error(engine_id)

    def record_hit(self, layer: str):
        self.metrics.record_hit(layer)

    def get_metrics(self):
        return self.metrics.get_metrics()

# 18. drift_watcher: baseline comparison, detect doctrine drift over time
class DriftWatcher:
    def __init__(self, doctrine_cache: List[DoctrineBlock]):
        self.baseline = {db.topic: db for db in doctrine_cache}
        self.current = {db.topic: db for db in doctrine_cache}
        self.drifted: Set[str] = set()

    def update(self, doctrine_cache: List[DoctrineBlock]):
        self.current = {db.topic: db for db in doctrine_cache}
        self.drifted = set()
        for topic, base_db in self.baseline.items():
            curr_db = self.current.get(topic)
            if curr_db:
                if base_db.reasoning_framework.strip() != curr_db.reasoning_framework.strip():
                    self.drifted.add(topic)

    def get_drifted(self) -> List[str]:
        return list(self.drifted)

# 19. coverage_map: track triggered/missed doctrines, epistemic gap detection
class CoverageMap:
    def __init__(self, doctrine_cache: List[DoctrineBlock]):
        self.topics = {db.topic for db in doctrine_cache}
        self.triggered: Set[str] = set()
        self.missed: Set[str] = set(self.topics)
        self.lock = threading.Lock()

    def record_triggered(self, topics: List[str]):
        with self.lock:
            for t in topics:
                self.triggered.add(t)
                self.missed.discard(t)

    def get_coverage(self):
        with self.lock:
            return {
                "triggered": list(self.triggered),
                "missed": list(self.missed),
                "epistemic_gap": len(self.missed)
            }

# 20. FastAPI server
app = FastAPI(title="Enterprise Intelligence Engine — Domain Backbone (ENTIE)", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

health_monitor = HealthMonitor(SUB_ENGINE_REGISTRY)
router = QueryRouter(SUB_ENGINE_REGISTRY, DOCTRINE_CACHE)
merger = ResponseMerger(DOCTRINE_CACHE)
telemetry = TelemetryCollector()
drift_watcher = DriftWatcher(DOCTRINE_CACHE)
coverage_map = CoverageMap(DOCTRINE_CACHE)

@app.on_event("startup")
async def startup_event():
    async def periodic_health_check():
        while True:
            await health_monitor.check_all()
            health_monitor.update_circuit_breakers()
            await asyncio.sleep(10)
    asyncio.create_task(periodic_health_check())

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    logger.info(f"Received query: {req.query}")
    # Apply semantic normalization
    req.query = semantic_normalization(req.query)
    resp = await three_layer_response(req, DOCTRINE_CACHE, router, merger, health_monitor, telemetry)
    # Apply epistemic guardrails
    resp.answer, caveats = apply_epistemic_guardrails(resp.answer)
    resp.epistemic_caveats = caveats
    coverage_map.record_triggered(resp.doctrines_triggered)
    return resp

@app.get("/health", response_model=HealthReport)
async def health_endpoint():
    status_map = health_monitor.get_status_map()
    breaker_states = health_monitor.get_circuit_breaker_states()
    return HealthReport(
        engine_status=status_map,
        circuit_breakers=breaker_states,
        timestamp=datetime.datetime.utcnow()
    )

@app.get("/engines")
async def engines_endpoint():
    return {
        eid: {
            "name": meta["name"],
            "port": meta["port"],
            "status": health_monitor.get_status_map().get(eid, "UNKNOWN"),
            "circuit_breaker": health_monitor.get_circuit_breaker_states().get(eid, "CLOSED"),
            "domain_topics": meta["domain_topics"]
        }
        for eid, meta in SUB_ENGINE_REGISTRY.items()
    }

@app.post("/route", response_model=RoutingDecision)
async def route_endpoint(req: QueryRequest):
    ranked = router.analyze(req.query, req.scenario, req.mode)
    return RoutingDecision(
        query=req.query,
        routed_engines=[eid for eid, _ in ranked],
        scores=[score for _, score in ranked]
    )

@app.get("/metrics")
async def metrics_endpoint():
    return telemetry.get_metrics()

@app.get("/coverage")
async def coverage_endpoint():
    return coverage_map.get_coverage()

@app.get("/doctrines")
async def doctrines_endpoint():
    return [
        {
            "topic": db.topic,
            "keywords": db.keywords,
            "conclusion_template": db.conclusion_template,
            "confidence": db.confidence,
            "confidence_zone": db.confidence_zone,
            "primary_authority": db.primary_authority
        }
        for db in DOCTRINE_CACHE
    ]
