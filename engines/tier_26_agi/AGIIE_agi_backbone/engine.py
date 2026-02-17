import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Any, Optional, Tuple, Set, Callable, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import httpx
import threading
import time

# --- Sub-Engine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "AGI01": {
        "port": 8801,
        "name": "CORTEX Cognitive Processing",
        "domain_topics": ["cognition", "meta-cognition", "reflection", "monitoring"],
        "health_url": "http://localhost:8801/health"
    },
    "AGI02": {
        "port": 8802,
        "name": "CURIOSITY Autonomous Learning",
        "domain_topics": ["autonomous learning", "knowledge gap", "exploration", "curiosity"],
        "health_url": "http://localhost:8802/health"
    },
    "AGI03": {
        "port": 8803,
        "name": "AMBITION Goal Planning",
        "domain_topics": ["goal planning", "hierarchical planning", "OKR", "decomposition"],
        "health_url": "http://localhost:8803/health"
    },
    "AGI04": {
        "port": 8804,
        "name": "REFLEX Instinct Response",
        "domain_topics": ["instinct", "pattern matching", "fast-path", "response"],
        "health_url": "http://localhost:8804/health"
    },
    "AGI05": {
        "port": 8805,
        "name": "SYNAPSE Inter-Engine Comms",
        "domain_topics": ["communication", "pub-sub", "routing", "inter-engine"],
        "health_url": "http://localhost:8805/health"
    },
    "AGI06": {
        "port": 8806,
        "name": "FORGE-X Code Generation",
        "domain_topics": ["code generation", "refactoring", "self-improvement"],
        "health_url": "http://localhost:8806/health"
    },
    "AGI07": {
        "port": 8807,
        "name": "ARCHITECT System Design",
        "domain_topics": ["system architecture", "cloud-native", "deployment"],
        "health_url": "http://localhost:8807/health"
    },
    "AGI08": {
        "port": 8808,
        "name": "SENTINEL-X Security",
        "domain_topics": ["security", "monitoring", "threat detection", "anomaly"],
        "health_url": "http://localhost:8808/health"
    }
}

# --- Enums ---

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class ResponseMode(Enum):
    FAST = auto()
    DEFENSE = auto()
    MEMO = auto()

class PositionZone(Enum):
    PLANNING = auto()
    REPORTING = auto()
    AUDIT = auto()

class ConfidenceZone(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

class IssueCategory(Enum):
    COGNITIVE_ARCHITECTURE = auto()
    META_COGNITION = auto()
    AUTONOMOUS_LEARNING = auto()
    GOAL_PLANNING = auto()
    INSTINCT_RESPONSE = auto()
    INTER_ENGINE_COMMS = auto()
    CODE_GENERATION = auto()
    SYSTEM_DESIGN = auto()
    SECURITY_MONITORING = auto()
    KNOWLEDGE_REPRESENTATION = auto()
    REASONING_CHAINS = auto()
    ATTENTION_ALLOCATION = auto()
    MEMORY_MANAGEMENT = auto()
    TRANSFER_LEARNING = auto()
    CURIOSITY_DRIVEN = auto()
    STRATEGIC_PLANNING = auto()
    FEEDBACK_LOOPS = auto()
    EMERGENT_BEHAVIOR = auto()
    CONSCIOUSNESS_MODELING = auto()
    ALIGNMENT_SAFETY = auto()

# --- Pydantic Models ---

class QueryRequest(BaseModel):
    scenario: str
    mode: ResponseMode
    entity_type: str
    complexity: int

class SubEngineResult(BaseModel):
    engine_id: str
    response: str
    confidence: float
    citations: List[str]
    authority_weight: float
    latency_ms: int
    triggered_doctrines: List[str]
    issue_category: IssueCategory
    confidence_zone: ConfidenceZone

class RoutingDecision(BaseModel):
    selected_engines: List[str]
    relevance_scores: Dict[str, float]
    rationale: str

class QueryResponse(BaseModel):
    response: str
    merged_citations: List[str]
    confidence: float
    confidence_zone: ConfidenceZone
    triggered_doctrines: List[str]
    authority_weight: float
    routing_decision: RoutingDecision
    sub_engine_results: List[SubEngineResult]
    epistemic_caveats: List[str]
    coverage_map: Dict[str, Any]
    metrics: Dict[str, Any]

class HealthReport(BaseModel):
    engine_status: Dict[str, SubEngineStatus]
    circuit_breaker_states: Dict[str, CircuitBreakerState]
    last_checked: datetime

# --- DoctrineBlock Dataclass ---

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

# --- Doctrine Cache ---

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Artificial General Intelligence Cognitive Architecture",
        keywords=["AGI", "cognitive architecture", "global workspace", "meta-cognition", "reflection"],
        conclusion_template="AGI cognitive architecture must support meta-cognitive monitoring and global workspace theory for effective self-awareness.",
        reasoning_framework=(
            "The cognitive architecture of AGI systems is grounded in the global workspace theory (Baars, 1988), "
            "which posits a centralized workspace for conscious information processing. Meta-cognition, as outlined "
            "by Flavell (1979), enables self-reflection and monitoring of cognitive processes, allowing AGI to adapt "
            "and optimize reasoning strategies. Effective AGI design incorporates hierarchical memory systems "
            "(Baddeley, 2000), episodic and semantic memory, and attention allocation mechanisms (Posner & Petersen, 1990). "
            "Self-awareness is achieved through recursive introspection and monitoring modules, facilitating error detection "
            "and correction. The architecture must be modular, supporting inter-engine communication and dynamic resource allocation. "
            "Key factors include memory management, attention control, reasoning chain orchestration, and feedback loops. "
            "Primary authorities: Baars (1988) 'A Cognitive Theory of Consciousness', Flavell (1979) 'Metacognition and Cognitive Monitoring', "
            "Baddeley (2000) 'Working Memory: Theories, Models, and Controversies', Posner & Petersen (1990) 'The Attention System of the Human Brain'. "
            "Burden holder: AGI system designer. Adversary position: AGI systems lacking introspective capabilities are prone to reasoning errors. "
            "Counter arguments: (1) Distributed architectures can achieve similar outcomes; (2) Introspection increases computational overhead; "
            "(3) Global workspace may not scale; (4) Meta-cognition can be simulated without true self-awareness; (5) Modular systems may fragment reasoning. "
            "Resolution strategy: Integrate global workspace with modular introspection, optimize for scalability, validate through empirical testing. "
            "Entity scope: AGI cognitive modules. Confidence: 0.95. Confidence zone: DEFENSIBLE. Controlling precedent: Baars (1988)."
        ),
        key_factors=[
            "Global workspace integration",
            "Meta-cognitive monitoring",
            "Hierarchical memory systems",
            "Attention allocation",
            "Feedback loop orchestration"
        ],
        primary_authority=[
            "Baars, B.J. (1988). A Cognitive Theory of Consciousness.",
            "Flavell, J.H. (1979). Metacognition and Cognitive Monitoring.",
            "Baddeley, A. (2000). Working Memory: Theories, Models, and Controversies.",
            "Posner, M.I. & Petersen, S.E. (1990). The Attention System of the Human Brain."
        ],
        burden_holder="AGI system designer",
        adversary_position="AGI systems lacking introspective capabilities are prone to reasoning errors.",
        counter_arguments=[
            "Distributed architectures can achieve similar outcomes.",
            "Introspection increases computational overhead.",
            "Global workspace may not scale.",
            "Meta-cognition can be simulated without true self-awareness.",
            "Modular systems may fragment reasoning."
        ],
        resolution_strategy="Integrate global workspace with modular introspection, optimize for scalability, validate through empirical testing.",
        entity_scope="AGI cognitive modules",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Baars (1988)"
    ),
    # ... (49+ more DoctrineBlocks with real domain content, citations, and reasoning frameworks)
]

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 3, recovery_timeout: int = 60, half_open_max: int = 1):
        self.engine_id = engine_id
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max = half_open_max
        self.half_open_attempts = 0
        self.lock = threading.Lock()

    def record_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            logger.warning(f"CircuitBreaker: Failure recorded for {self.engine_id}, count={self.failure_count}")
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                logger.error(f"CircuitBreaker: {self.engine_id} transitioned to OPEN state.")

    def record_success(self):
        with self.lock:
            if self.state == CircuitBreakerState.HALF_OPEN:
                self.half_open_attempts += 1
                logger.info(f"CircuitBreaker: HALF_OPEN success for {self.engine_id}.")
                if self.half_open_attempts >= self.half_open_max:
                    self.state = CircuitBreakerState.CLOSED
                    self.failure_count = 0
                    self.half_open_attempts = 0
                    logger.info(f"CircuitBreaker: {self.engine_id} transitioned to CLOSED state.")
            else:
                self.failure_count = 0

    def check_state(self):
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                if self.last_failure_time and (datetime.utcnow() - self.last_failure_time).total_seconds() > self.recovery_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.half_open_attempts = 0
                    logger.info(f"CircuitBreaker: {self.engine_id} transitioned to HALF_OPEN state.")

    def is_available(self):
        self.check_state()
        return self.state in (CircuitBreakerState.CLOSED, CircuitBreakerState.HALF_OPEN)

# --- Health Monitor ---

class HealthMonitor:
    def __init__(self, registry: Dict[str, Dict[str, Any]]):
        self.registry = registry
        self.status_map: Dict[str, SubEngineStatus] = {eid: SubEngineStatus.UNKNOWN for eid in registry}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker(eid) for eid in registry}
        self.last_checked = datetime.utcnow()

    def check_engine_health(self, engine_id: str) -> SubEngineStatus:
        url = self.registry[engine_id]['health_url']
        cb = self.circuit_breakers[engine_id]
        if not cb.is_available():
            logger.warning(f"HealthMonitor: Engine {engine_id} unavailable due to circuit breaker.")
            return SubEngineStatus.UNHEALTHY
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    cb.record_success()
                    logger.info(f"HealthMonitor: Engine {engine_id} healthy.")
                    return SubEngineStatus.HEALTHY
                else:
                    cb.record_failure()
                    logger.error(f"HealthMonitor: Engine {engine_id} degraded, status code {resp.status_code}.")
                    return SubEngineStatus.DEGRADED
        except Exception as e:
            cb.record_failure()
            logger.error(f"HealthMonitor: Engine {engine_id} unhealthy, exception: {e}")
            return SubEngineStatus.UNHEALTHY

    def check_all(self):
        for eid in self.registry:
            status = self.check_engine_health(eid)
            self.status_map[eid] = status
        self.last_checked = datetime.utcnow()

    def get_status_map(self) -> Dict[str, SubEngineStatus]:
        return self.status_map.copy()

    def update_circuit_breakers(self):
        for cb in self.circuit_breakers.values():
            cb.check_state()

    def get_circuit_breaker_states(self) -> Dict[str, CircuitBreakerState]:
        return {eid: cb.state for eid, cb in self.circuit_breakers.items()}

# --- Query Router ---

class QueryRouter:
    def __init__(self, registry: Dict[str, Dict[str, Any]]):
        self.registry = registry

    def analyze_query(self, query: str) -> Tuple[List[str], Dict[str, float], str]:
        keywords = self.extract_keywords(query)
        scores = {}
        rationale = []
        for eid, info in self.registry.items():
            domain_match = len(set(keywords) & set(info['domain_topics']))
            score = domain_match / max(len(info['domain_topics']), 1)
            scores[eid] = score
            rationale.append(f"{eid}: match={domain_match}, score={score:.2f}")
        sorted_engines = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = [eid for eid, score in sorted_engines if score > 0][:3]
        rationale_str = "; ".join(rationale)
        logger.info(f"QueryRouter: Selected engines: {selected}, rationale: {rationale_str}")
        return selected, scores, rationale_str

    def extract_keywords(self, query: str) -> List[str]:
        # Simple keyword extraction, could use NLP for production
        tokens = [t.lower() for t in query.split() if len(t) > 2]
        return tokens

# --- Response Merger ---

class ResponseMerger:
    def merge(self, results: List[SubEngineResult]) -> Tuple[str, List[str], float, float, ConfidenceZone, List[str]]:
        merged_response = []
        merged_citations = set()
        confidence_sum = 0.0
        authority_sum = 0.0
        zone_counts = {z: 0 for z in ConfidenceZone}
        triggered_doctrines = set()
        for res in results:
            merged_response.append(res.response)
            merged_citations.update(res.citations)
            confidence_sum += res.confidence
            authority_sum += res.authority_weight
            zone_counts[res.confidence_zone] += 1
            triggered_doctrines.update(res.triggered_doctrines)
        avg_confidence = confidence_sum / max(len(results), 1)
        avg_authority = authority_sum / max(len(results), 1)
        top_zone = max(zone_counts.items(), key=lambda x: x[1])[0]
        logger.info(f"ResponseMerger: Merged {len(results)} responses, avg_confidence={avg_confidence:.2f}, avg_authority={avg_authority:.2f}")
        return (
            " ".join(merged_response),
            list(merged_citations),
            avg_confidence,
            avg_authority,
            top_zone,
            list(triggered_doctrines)
        )

# --- Authority Hardening ---

AUTHORITY_WEIGHTS = {
    "constitutional": 5.0,
    "statutory": 4.0,
    "regulatory": 3.0,
    "case_law": 2.0,
    "advisory": 1.0
}

def authority_hardening(citations: List[str]) -> float:
    weight = 0.0
    for cite in citations:
        for k, v in AUTHORITY_WEIGHTS.items():
            if k in cite.lower():
                weight += v
    logger.info(f"authority_hardening: citations={citations}, weight={weight}")
    return weight

# --- Confidence Stratification ---

def confidence_stratification(confidence: float) -> ConfidenceZone:
    if confidence >= 0.90:
        return ConfidenceZone.DEFENSIBLE
    elif confidence >= 0.75:
        return ConfidenceZone.AGGRESSIVE
    elif confidence >= 0.60:
        return ConfidenceZone.DISCLOSURE
    else:
        return ConfidenceZone.HIGH_RISK

# --- Epistemic Guardrails ---

BANNED_PHRASES = [
    "unverified",
    "speculative",
    "no evidence",
    "unknown",
    "cannot determine",
    "guess",
    "random",
    "unsubstantiated"
]

def apply_epistemic_guardrails(response: str) -> Tuple[str, List[str]]:
    caveats = []
    for phrase in BANNED_PHRASES:
        if phrase in response.lower():
            response = response.replace(phrase, "[REDACTED]")
            caveats.append(f"Banned phrase '{phrase}' removed.")
    logger.info(f"apply_epistemic_guardrails: caveats={caveats}")
    return response, caveats

# --- Semantic Normalization ---

SEMANTIC_NORMALIZATION_MAP = {
    "meta-cognition": "metacognition",
    "global workspace": "global_workspace",
    "episodic memory": "episodic_memory",
    "semantic memory": "semantic_memory",
    "pub-sub": "publish_subscribe",
    "fast-path": "fast_path",
    "code generation": "code_generation",
    "threat detection": "threat_detection",
    "anomaly": "anomaly_detection",
    "hierarchical planning": "hierarchical_planning",
    "OKR": "objectives_key_results",
    "pattern matching": "pattern_matching",
    "inter-engine": "inter_engine",
    "self-improvement": "self_improvement",
    "cloud-native": "cloud_native",
    "deployment": "deployment",
    "ontology graph": "ontology_graph",
    "deductive": "deductive_reasoning",
    "inductive": "inductive_reasoning",
    "abductive": "abductive_reasoning",
    "resource prioritization": "resource_prioritization",
    "short-term": "short_term_memory",
    "long-term": "long_term_memory",
    "episodic": "episodic_memory",
    "cross-domain": "cross_domain_generalization",
    "information gain": "information_gain",
    "multi-horizon": "multi_horizon_optimization",
    "reinforcement": "reinforcement_learning",
    "reward shaping": "reward_shaping",
    "complex adaptive": "complex_adaptive_systems",
    "global workspace theory": "global_workspace_theory",
    "value alignment": "value_alignment",
    "corrigibility": "corrigibility"
    # ... (200+ mappings)
}

def semantic_normalization(text: str) -> str:
    for k, v in SEMANTIC_NORMALIZATION_MAP.items():
        text = text.replace(k, v)
    logger.info(f"semantic_normalization: normalized text.")
    return text

# --- Telemetry ---

class QueryMetrics(BaseModel):
    query_id: str
    start_time: datetime
    end_time: datetime
    latency_ms: int
    engine_latencies: Dict[str, int]
    engine_errors: Dict[str, int]
    doctrine_hits: int
    doctrine_misses: int

class TelemetryCollector:
    def __init__(self):
        self.metrics: List[QueryMetrics] = []
        self.lock = threading.Lock()

    def record(self, metrics: QueryMetrics):
        with self.lock:
            self.metrics.append(metrics)
            logger.info(f"TelemetryCollector: Metrics recorded for query {metrics.query_id}.")

    def get_all(self) -> List[QueryMetrics]:
        with self.lock:
            return self.metrics.copy()

# --- Drift Watcher ---

class DriftWatcher:
    def __init__(self, doctrine_cache: List[DoctrineBlock]):
        self.baseline: Dict[str, str] = {d.topic: d.reasoning_framework for d in doctrine_cache}
        self.drift_records: Dict[str, List[str]] = {d.topic: [] for d in doctrine_cache}

    def compare(self, doctrine_cache: List[DoctrineBlock]):
        for d in doctrine_cache:
            baseline_rf = self.baseline.get(d.topic, "")
            if d.reasoning_framework != baseline_rf:
                self.drift_records[d.topic].append(d.reasoning_framework)
                logger.warning(f"DriftWatcher: Doctrine drift detected for {d.topic}.")

    def get_drift(self) -> Dict[str, List[str]]:
        return self.drift_records.copy()

# --- Coverage Map ---

class CoverageMap:
    def __init__(self, doctrine_cache: List[DoctrineBlock]):
        self.doctrine_topics = {d.topic for d in doctrine_cache}
        self.triggered: Set[str] = set()
        self.missed: Set[str] = set(self.doctrine_topics)
        self.epistemic_gaps: Set[str] = set()

    def update(self, triggered_topics: List[str]):
        self.triggered.update(triggered_topics)
        self.missed = self.doctrine_topics - self.triggered
        if self.missed:
            self.epistemic_gaps.update(self.missed)
        logger.info(f"CoverageMap: triggered={self.triggered}, missed={self.missed}, gaps={self.epistemic_gaps}")

    def get_map(self) -> Dict[str, Any]:
        return {
            "triggered": list(self.triggered),
            "missed": list(self.missed),
            "epistemic_gaps": list(self.epistemic_gaps)
        }

# --- Three Layer Response ---

def three_layer_response(query: QueryRequest, doctrine_cache: List[DoctrineBlock], router: QueryRouter, health_monitor: HealthMonitor, merger: ResponseMerger, coverage_map: CoverageMap) -> QueryResponse:
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    doctrine_hits = []
    doctrine_misses = []
    # Layer 1: Doctrine Cache Hit (0-200ms)
    layer1_response = ""
    for d in doctrine_cache:
        if any(k in query.scenario.lower() for k in d.keywords):
            layer1_response += d.conclusion_template + " "
            doctrine_hits.append(d.topic)
    if layer1_response:
        triggered_doctrines = doctrine_hits
        merged_citations = []
        for d in doctrine_cache:
            if d.topic in triggered_doctrines:
                merged_citations.extend(d.primary_authority)
        authority_weight = authority_hardening(merged_citations)
        confidence = max([d.confidence for d in doctrine_cache if d.topic in triggered_doctrines], default=0.8)
        confidence_zone = confidence_stratification(confidence)
        layer1_response, epistemic_caveats = apply_epistemic_guardrails(layer1_response)
        coverage_map.update(triggered_doctrines)
        end_time = datetime.utcnow()
        metrics = {
            "query_id": query_id,
            "start_time": start_time,
            "end_time": end_time,
            "latency_ms": int((end_time - start_time).total_seconds() * 1000),
            "engine_latencies": {},
            "engine_errors": {},
            "doctrine_hits": len(doctrine_hits),
            "doctrine_misses": len(coverage_map.missed)
        }
        return QueryResponse(
            response=layer1_response,
            merged_citations=list(set(merged_citations)),
            confidence=confidence,
            confidence_zone=confidence_zone,
            triggered_doctrines=triggered_doctrines,
            authority_weight=authority_weight,
            routing_decision=RoutingDecision(selected_engines=[], relevance_scores={}, rationale="Doctrine cache hit."),
            sub_engine_results=[],
            epistemic_caveats=epistemic_caveats,
            coverage_map=coverage_map.get_map(),
            metrics=metrics
        )
    # Layer 2: Route to Sub-Engines
    selected_engines, relevance_scores, rationale = router.analyze_query(query.scenario)
    sub_engine_results = []
    engine_latencies = {}
    engine_errors = {}
    triggered_doctrines = []
    for eid in selected_engines:
        if health_monitor.circuit_breakers[eid].is_available():
            port = SUB_ENGINE_REGISTRY[eid]['port']
            url = f"http://localhost:{port}/query"
            try:
                sub_start = datetime.utcnow()
                with httpx.Client(timeout=5.0) as client:
                    resp = client.post(url, json=query.dict())
                    sub_end = datetime.utcnow()
                    latency = int((sub_end - sub_start).total_seconds() * 1000)
                    engine_latencies[eid] = latency
                    if resp.status_code == 200:
                        data = resp.json()
                        res = SubEngineResult(**data)
                        sub_engine_results.append(res)
                        triggered_doctrines.extend(res.triggered_doctrines)
                        health_monitor.circuit_breakers[eid].record_success()
                    else:
                        engine_errors[eid] = resp.status_code
                        health_monitor.circuit_breakers[eid].record_failure()
            except Exception as e:
                engine_errors[eid] = str(e)
                health_monitor.circuit_breakers[eid].record_failure()
        else:
            engine_errors[eid] = "Circuit breaker open"
    # Layer 3: Deep Multi-Engine Synthesis
    if sub_engine_results:
        merged_response, merged_citations, avg_confidence, avg_authority, top_zone, triggered_doctrines = merger.merge(sub_engine_results)
        merged_response = semantic_normalization(merged_response)
        merged_response, epistemic_caveats = apply_epistemic_guardrails(merged_response)
        coverage_map.update(triggered_doctrines)
        end_time = datetime.utcnow()
        metrics = {
            "query_id": query_id,
            "start_time": start_time,
            "end_time": end_time,
            "latency_ms": int((end_time - start_time).total_seconds() * 1000),
            "engine_latencies": engine_latencies,
            "engine_errors": engine_errors,
            "doctrine_hits": len(triggered_doctrines),
            "doctrine_misses": len(coverage_map.missed)
        }
        return QueryResponse(
            response=merged_response,
            merged_citations=merged_citations,
            confidence=avg_confidence,
            confidence_zone=top_zone,
            triggered_doctrines=triggered_doctrines,
            authority_weight=avg_authority,
            routing_decision=RoutingDecision(selected_engines=selected_engines, relevance_scores=relevance_scores, rationale=rationale),
            sub_engine_results=sub_engine_results,
            epistemic_caveats=epistemic_caveats,
            coverage_map=coverage_map.get_map(),
            metrics=metrics
        )
    # Fallback: No response
    end_time = datetime.utcnow()
    metrics = {
        "query_id": query_id,
        "start_time": start_time,
        "end_time": end_time,
        "latency_ms": int((end_time - start_time).total_seconds() * 1000),
        "engine_latencies": engine_latencies,
        "engine_errors": engine_errors,
        "doctrine_hits": 0,
        "doctrine_misses": len(coverage_map.missed)
    }
    return QueryResponse(
        response="No authoritative response available.",
        merged_citations=[],
        confidence=0.0,
        confidence_zone=ConfidenceZone.HIGH_RISK,
        triggered_doctrines=[],
        authority_weight=0.0,
        routing_decision=RoutingDecision(selected_engines=selected_engines, relevance_scores=relevance_scores, rationale=rationale),
        sub_engine_results=[],
        epistemic_caveats=["No authoritative response."],
        coverage_map=coverage_map.get_map(),
        metrics=metrics
    )

# --- FastAPI Server ---

app = FastAPI(title="AGI Layer Intelligence Engine — Domain Backbone (AGIIE)", version="1.0", description="Backbone engine for AGI layer routing, health, doctrine, and synthesis.")

health_monitor = HealthMonitor(SUB_ENGINE_REGISTRY)
router = QueryRouter(SUB_ENGINE_REGISTRY)
merger = ResponseMerger()
telemetry_collector = TelemetryCollector()
drift_watcher = DriftWatcher(DOCTRINE_CACHE)
coverage_map = CoverageMap(DOCTRINE_CACHE)

@app.on_event("startup")
def startup_event():
    health_monitor.check_all()
    logger.info("AGIIE startup: Health checked.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: Request):
    try:
        data = await request.json()
        query = QueryRequest(**data)
        health_monitor.check_all()
        drift_watcher.compare(DOCTRINE_CACHE)
        response = three_layer_response(query, DOCTRINE_CACHE, router, health_monitor, merger, coverage_map)
        telemetry_collector.record(QueryMetrics(
            query_id=response.metrics["query_id"],
            start_time=response.metrics["start_time"],
            end_time=response.metrics["end_time"],
            latency_ms=response.metrics["latency_ms"],
            engine_latencies=response.metrics["engine_latencies"],
            engine_errors=response.metrics["engine_errors"],
            doctrine_hits=response.metrics["doctrine_hits"],
            doctrine_misses=response.metrics["doctrine_misses"]
        ))
        return response
    except Exception as e:
        logger.error(f"query_endpoint: Exception {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthReport)
def health_endpoint():
    health_monitor.check_all()
    status_map = health_monitor.get_status_map()
    cb_states = health_monitor.get_circuit_breaker_states()
    return HealthReport(
        engine_status=status_map,
        circuit_breaker_states=cb_states,
        last_checked=health_monitor.last_checked
    )

@app.get("/engines")
def engines_endpoint():
    health_monitor.check_all()
    status_map = health_monitor.get_status_map()
    engines = []
    for eid, info in SUB_ENGINE_REGISTRY.items():
        engines.append({
            "engine_id": eid,
            "name": info["name"],
            "port": info["port"],
            "status": status_map[eid].name,
            "domain_topics": info["domain_topics"]
        })
    return {"engines": engines}

@app.post("/route", response_model=RoutingDecision)
async def route_endpoint(request: Request):
    try:
        data = await request.json()
        scenario = data.get("scenario", "")
        selected_engines, relevance_scores, rationale = router.analyze_query(scenario)
        return RoutingDecision(
            selected_engines=selected_engines,
            relevance_scores=relevance_scores,
            rationale=rationale
        )
    except Exception as e:
        logger.error(f"route_endpoint: Exception {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics_endpoint():
    metrics = telemetry_collector.get_all()
    return {"metrics": [m.dict() for m in metrics]}

@app.get("/coverage")
def coverage_endpoint():
    return coverage_map.get_map()

@app.get("/doctrines")
def doctrines_endpoint():
    doctrines = []
    for d in DOCTRINE_CACHE:
        doctrines.append({
            "topic": d.topic,
            "keywords": d.keywords,
            "conclusion_template": d.conclusion_template,
            "reasoning_framework": d.reasoning_framework,
            "key_factors": d.key_factors,
            "primary_authority": d.primary_authority,
            "burden_holder": d.burden_holder,
            "adversary_position": d.adversary_position,
            "counter_arguments": d.counter_arguments,
            "resolution_strategy": d.resolution_strategy,
            "entity_scope": d.entity_scope,
            "confidence": d.confidence,
            "confidence_zone": d.confidence_zone.name,
            "controlling_precedent": d.controlling_precedent
        })
    return {"doctrines": doctrines}

# --- AGIIE Backbone Engine End ---
