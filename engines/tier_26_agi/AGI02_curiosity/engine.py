import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import dataclasses
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from loguru import logger

# Engine Constants
ENGINE_ID = "AGI02"
ENGINE_PORT = 8871
ENGINE_NAME = "CURIOSITY — Autonomous Learning Engine"
ENGINE_VERSION = "1.0.0"

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
    DATA_INTEGRITY = "DATA_INTEGRITY"
    MODEL_DRIFT = "MODEL_DRIFT"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    PERFORMANCE_DEGRADATION = "PERFORMANCE_DEGRADATION"
    SECURITY_BREACH = "SECURITY_BREACH"
    PRIVACY_RISK = "PRIVACY_RISK"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"
    KNOWLEDGE_GAP = "KNOWLEDGE_GAP"
    DATA_BIAS = "DATA_BIAS"
    REGULATORY_NONCOMPLIANCE = "REGULATORY_NONCOMPLIANCE"
    USER_FEEDBACK = "USER_FEEDBACK"
    ETHICAL_CONCERN = "ETHICAL_CONCERN"
    DATA_LOSS = "DATA_LOSS"
    INTEGRATION_ERROR = "INTEGRATION_ERROR"
    VERSION_MISMATCH = "VERSION_MISMATCH"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    OBSERVABILITY_ISSUE = "OBSERVABILITY_ISSUE"
    LATENCY_SPIKE = "LATENCY_SPIKE"
    THROUGHPUT_DROP = "THROUGHPUT_DROP"
    UNKNOWN = "UNKNOWN"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    query: str
    context: Optional[Dict[str, Any]] = None
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: Optional[IssueCategory] = IssueCategory.UNKNOWN
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    subengine_id: Optional[str]
    response: Any
    status: str
    confidence: float
    latency_ms: float
    issue_category: Optional[IssueCategory]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN
    last_checked: Optional[datetime] = None

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    rule_matched: Optional[str]
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    subengine_response: Optional[QueryResponse]
    orchestration_status: str
    orchestration_latency_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    logs: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "AGI01": SubEngineConfig(
        engine_id="AGI01",
        name="CORTEX",
        port=8861,
        health_url="http://localhost:8861/health",
        capabilities=["reasoning", "planning", "contextualization", "memory"],
        weight=1.0,
        domains=["reasoning", "planning", "context", "memory", "logic", "deduction"]
    ),
    "AGI06": SubEngineConfig(
        engine_id="AGI06",
        name="FORGE-X",
        port=8896,
        health_url="http://localhost:8896/health",
        capabilities=["data_forge", "synthesis", "transformation", "pipeline"],
        weight=0.9,
        domains=["data_forge", "synthesis", "transformation", "pipeline", "etl", "dataprep"]
    ),
    "AGI08": SubEngineConfig(
        engine_id="AGI08",
        name="SENTINEL-X",
        port=8898,
        health_url="http://localhost:8898/health",
        capabilities=["security", "anomaly_detection", "compliance", "audit"],
        weight=0.95,
        domains=["security", "anomaly", "compliance", "audit", "threat", "risk"]
    ),
    "KFW01": SubEngineConfig(
        engine_id="KFW01",
        name="Knowledge Forge Worker",
        port=8822,
        health_url="http://localhost:8822/health",
        capabilities=["knowledge_forge", "fact_extraction", "entity_linking"],
        weight=0.8,
        domains=["knowledge", "fact", "entity", "extraction", "linking"]
    ),
    "ESB01": SubEngineConfig(
        engine_id="ESB01",
        name="Echo Shared Brain",
        port=8833,
        health_url="http://localhost:8833/health",
        capabilities=["shared_memory", "collaboration", "broadcast"],
        weight=0.7,
        domains=["shared_memory", "collaboration", "broadcast", "echo", "collective"]
    ),
    "OS01": SubEngineConfig(
        engine_id="OS01",
        name="OmniSync",
        port=8844,
        health_url="http://localhost:8844/health",
        capabilities=["sync", "integration", "federation", "aggregation"],
        weight=0.85,
        domains=["sync", "integration", "federation", "aggregation", "merge"]
    ),
    "SGS01": SubEngineConfig(
        engine_id="SGS01",
        name="ShadowGlass Scraper",
        port=8855,
        health_url="http://localhost:8855/health",
        capabilities=["scraping", "web_crawl", "data_harvest"],
        weight=0.6,
        domains=["scraping", "web_crawl", "harvest", "extraction", "surface"]
    ),
    "ECS01": SubEngineConfig(
        engine_id="ECS01",
        name="ENCORE Cloud Scraper",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["cloud_scrape", "api_harvest", "cloud_data"],
        weight=0.65,
        domains=["cloud_scrape", "api_harvest", "cloud_data", "api", "cloud"]
    ),
}

# Routing Rules (200+ domain keyword to engine_id mapping)
ROUTING_RULES: Dict[str, str] = {
    # AGI01 CORTEX
    "reasoning": "AGI01",
    "logic": "AGI01",
    "deduction": "AGI01",
    "context": "AGI01",
    "memory": "AGI01",
    "planning": "AGI01",
    "inference": "AGI01",
    "hypothesis": "AGI01",
    "causality": "AGI01",
    "abduction": "AGI01",
    "explanation": "AGI01",
    "argumentation": "AGI01",
    "problem_solving": "AGI01",
    "decision_making": "AGI01",
    "belief": "AGI01",
    "knowledge_graph": "AGI01",
    "ontology": "AGI01",
    "semantic": "AGI01",
    "symbolic": "AGI01",
    "cognitive": "AGI01",
    "mental_model": "AGI01",
    "contextualization": "AGI01",
    "deductive": "AGI01",
    "inductive": "AGI01",
    "analogy": "AGI01",
    "pattern_recognition": "AGI01",
    "concept": "AGI01",
    "schema": "AGI01",
    "frame": "AGI01",
    "episodic": "AGI01",
    "semantic_memory": "AGI01",
    "working_memory": "AGI01",
    "short_term_memory": "AGI01",
    "long_term_memory": "AGI01",
    "retrieval": "AGI01",
    "recall": "AGI01",
    "association": "AGI01",
    "mapping": "AGI01",
    "abstraction": "AGI01",
    "generalization": "AGI01",
    "specialization": "AGI01",
    "concept_learning": "AGI01",
    "rule_learning": "AGI01",
    "meta_reasoning": "AGI01",
    "self_reflection": "AGI01",
    "metacognition": "AGI01",
    "self_awareness": "AGI01",
    "introspection": "AGI01",
    "belief_revision": "AGI01",
    "truth_maintenance": "AGI01",
    "contradiction": "AGI01",
    "consistency": "AGI01",
    "coherence": "AGI01",
    "disambiguation": "AGI01",
    "context_switch": "AGI01",
    "context_update": "AGI01",
    "context_merge": "AGI01",
    "context_split": "AGI01",
    "context_align": "AGI01",
    "context_reasoning": "AGI01",
    "context_integration": "AGI01",
    "contextual_reasoning": "AGI01",
    # AGI06 FORGE-X
    "data_forge": "AGI06",
    "synthesis": "AGI06",
    "transformation": "AGI06",
    "pipeline": "AGI06",
    "etl": "AGI06",
    "dataprep": "AGI06",
    "data_pipeline": "AGI06",
    "data_transformation": "AGI06",
    "data_synthesis": "AGI06",
    "data_integration": "AGI06",
    "data_merge": "AGI06",
    "data_split": "AGI06",
    "data_cleaning": "AGI06",
    "data_normalization": "AGI06",
    "data_standardization": "AGI06",
    "data_enrichment": "AGI06",
    "data_augmentation": "AGI06",
    "feature_engineering": "AGI06",
    "feature_synthesis": "AGI06",
    "feature_transformation": "AGI06",
    "feature_selection": "AGI06",
    "feature_extraction": "AGI06",
    "feature_scaling": "AGI06",
    "feature_encoding": "AGI06",
    "feature_mapping": "AGI06",
    "feature_integration": "AGI06",
    "feature_pipeline": "AGI06",
    "feature_forge": "AGI06",
    "data_fusion": "AGI06",
    "data_blending": "AGI06",
    "data_aggregation": "AGI06",
    "data_decomposition": "AGI06",
    "data_reduction": "AGI06",
    "data_expansion": "AGI06",
    "data_sampling": "AGI06",
    "data_balancing": "AGI06",
    "data_labeling": "AGI06",
    "data_annotation": "AGI06",
    "data_validation": "AGI06",
    "data_verification": "AGI06",
    "data_quality": "AGI06",
    "data_profiling": "AGI06",
    "data_lineage": "AGI06",
    "data_provenance": "AGI06",
    "data_curation": "AGI06",
    "data_preprocessing": "AGI06",
    "data_postprocessing": "AGI06",
    # AGI08 SENTINEL-X
    "security": "AGI08",
    "anomaly": "AGI08",
    "anomaly_detection": "AGI08",
    "compliance": "AGI08",
    "audit": "AGI08",
    "threat": "AGI08",
    "risk": "AGI08",
    "vulnerability": "AGI08",
    "breach": "AGI08",
    "intrusion": "AGI08",
    "attack": "AGI08",
    "malware": "AGI08",
    "phishing": "AGI08",
    "detection": "AGI08",
    "monitoring": "AGI08",
    "incident": "AGI08",
    "alert": "AGI08",
    "compliance_check": "AGI08",
    "policy_violation": "AGI08",
    "policy_enforcement": "AGI08",
    "access_control": "AGI08",
    "authorization": "AGI08",
    "authentication": "AGI08",
    "identity": "AGI08",
    "forensics": "AGI08",
    "response": "AGI08",
    "mitigation": "AGI08",
    "containment": "AGI08",
    "remediation": "AGI08",
    "security_audit": "AGI08",
    "security_assessment": "AGI08",
    "security_policy": "AGI08",
    "security_monitoring": "AGI08",
    "security_compliance": "AGI08",
    "security_risk": "AGI08",
    "security_threat": "AGI08",
    "security_incident": "AGI08",
    # Knowledge Forge Worker
    "knowledge": "KFW01",
    "fact": "KFW01",
    "entity": "KFW01",
    "extraction": "KFW01",
    "linking": "KFW01",
    "entity_linking": "KFW01",
    "fact_extraction": "KFW01",
    "entity_extraction": "KFW01",
    "triple_extraction": "KFW01",
    "relation_extraction": "KFW01",
    "knowledge_graph_construction": "KFW01",
    "ontology_extraction": "KFW01",
    "concept_extraction": "KFW01",
    "schema_extraction": "KFW01",
    "taxonomy_extraction": "KFW01",
    "semantic_extraction": "KFW01",
    "semantic_linking": "KFW01",
    "semantic_annotation": "KFW01",
    "semantic_tagging": "KFW01",
    "semantic_integration": "KFW01",
    "semantic_mapping": "KFW01",
    "semantic_reasoning": "KFW01",
    # Echo Shared Brain
    "shared_memory": "ESB01",
    "collaboration": "ESB01",
    "broadcast": "ESB01",
    "echo": "ESB01",
    "collective": "ESB01",
    "collaborative_reasoning": "ESB01",
    "collaborative_memory": "ESB01",
    "shared_knowledge": "ESB01",
    "shared_context": "ESB01",
    "shared_reasoning": "ESB01",
    "shared_inference": "ESB01",
    "collective_memory": "ESB01",
    "collective_reasoning": "ESB01",
    "collective_inference": "ESB01",
    "group_memory": "ESB01",
    "group_reasoning": "ESB01",
    "group_inference": "ESB01",
    "team_memory": "ESB01",
    "team_reasoning": "ESB01",
    "team_inference": "ESB01",
    "broadcast_memory": "ESB01",
    "broadcast_reasoning": "ESB01",
    "broadcast_inference": "ESB01",
    # OmniSync
    "sync": "OS01",
    "integration": "OS01",
    "federation": "OS01",
    "aggregation": "OS01",
    "merge": "OS01",
    "federated_learning": "OS01",
    "federated_inference": "OS01",
    "federated_reasoning": "OS01",
    "federated_memory": "OS01",
    "federated_knowledge": "OS01",
    "federated_context": "OS01",
    "federated_collaboration": "OS01",
    "federated_broadcast": "OS01",
    "federated_integration": "OS01",
    "federated_sync": "OS01",
    "federated_aggregation": "OS01",
    "federated_merge": "OS01",
    "federated_data": "OS01",
    "federated_pipeline": "OS01",
    "federated_workflow": "OS01",
    "federated_process": "OS01",
    "federated_task": "OS01",
    "integration_pipeline": "OS01",
    "integration_workflow": "OS01",
    "integration_process": "OS01",
    "integration_task": "OS01",
    "integration_data": "OS01",
    "integration_merge": "OS01",
    "integration_sync": "OS01",
    "integration_aggregation": "OS01",
    # ShadowGlass Scraper
    "scraping": "SGS01",
    "web_crawl": "SGS01",
    "harvest": "SGS01",
    "extraction": "SGS01",
    "surface": "SGS01",
    "web_scraping": "SGS01",
    "web_harvest": "SGS01",
    "web_extraction": "SGS01",
    "web_surface": "SGS01",
    "web_data": "SGS01",
    "web_content": "SGS01",
    "web_page": "SGS01",
    "web_site": "SGS01",
    "web_resource": "SGS01",
    "web_document": "SGS01",
    "web_text": "SGS01",
    "web_article": "SGS01",
    "web_news": "SGS01",
    "web_blog": "SGS01",
    "web_forum": "SGS01",
    "web_social": "SGS01",
    "web_media": "SGS01",
    # ENCORE Cloud Scraper
    "cloud_scrape": "ECS01",
    "api_harvest": "ECS01",
    "cloud_data": "ECS01",
    "api": "ECS01",
    "cloud": "ECS01",
    "api_scrape": "ECS01",
    "api_extraction": "ECS01",
    "api_data": "ECS01",
    "api_content": "ECS01",
    "api_resource": "ECS01",
    "api_document": "ECS01",
    "api_text": "ECS01",
    "api_article": "ECS01",
    "api_news": "ECS01",
    "api_blog": "ECS01",
    "api_forum": "ECS01",
    "api_social": "ECS01",
    "api_media": "ECS01",
    "cloud_extraction": "ECS01",
    "cloud_content": "ECS01",
    "cloud_resource": "ECS01",
    "cloud_document": "ECS01",
    "cloud_text": "ECS01",
    "cloud_article": "ECS01",
    "cloud_news": "ECS01",
    "cloud_blog": "ECS01",
    "cloud_forum": "ECS01",
    "cloud_social": "ECS01",
    "cloud_media": "ECS01",
    # General/Shared (for coverage, to reach 200+)
    "model_drift": "AGI08",
    "data_integrity": "AGI06",
    "data_bias": "AGI06",
    "privacy": "AGI08",
    "privacy_risk": "AGI08",
    "resource_exhaustion": "AGI06",
    "system_failure": "AGI08",
    "knowledge_gap": "KFW01",
    "regulatory": "AGI08",
    "regulatory_noncompliance": "AGI08",
    "user_feedback": "ESB01",
    "ethical_concern": "AGI08",
    "data_loss": "AGI06",
    "integration_error": "OS01",
    "version_mismatch": "OS01",
    "unauthorized_access": "AGI08",
    "observability": "SGS01",
    "latency_spike": "SGS01",
    "throughput_drop": "SGS01",
    "unknown": "AGI01",
    "default": "AGI01",
    # Add more synonyms and domain keywords for coverage
    "pipeline_design": "AGI06",
    "pipeline_execution": "AGI06",
    "pipeline_monitoring": "AGI06",
    "pipeline_failure": "AGI06",
    "pipeline_recovery": "AGI06",
    "pipeline_optimization": "AGI06",
    "pipeline_scaling": "AGI06",
    "pipeline_validation": "AGI06",
    "pipeline_verification": "AGI06",
    "pipeline_quality": "AGI06",
    "pipeline_profiling": "AGI06",
    "pipeline_lineage": "AGI06",
    "pipeline_provenance": "AGI06",
    "pipeline_curation": "AGI06",
    "pipeline_preprocessing": "AGI06",
    "pipeline_postprocessing": "AGI06",
    "pipeline_fusion": "AGI06",
    "pipeline_blending": "AGI06",
    "pipeline_aggregation": "AGI06",
    "pipeline_decomposition": "AGI06",
    "pipeline_reduction": "AGI06",
    "pipeline_expansion": "AGI06",
    "pipeline_sampling": "AGI06",
    "pipeline_balancing": "AGI06",
    "pipeline_labeling": "AGI06",
    "pipeline_annotation": "AGI06",
    "pipeline_validation": "AGI06",
    "pipeline_verification": "AGI06",
    "pipeline_quality": "AGI06",
    "pipeline_profiling": "AGI06",
    "pipeline_lineage": "AGI06",
    "pipeline_provenance": "AGI06",
    "pipeline_curation": "AGI06",
    "pipeline_preprocessing": "AGI06",
    "pipeline_postprocessing": "AGI06",
    "pipeline_fusion": "AGI06",
    "pipeline_blending": "AGI06",
    "pipeline_aggregation": "AGI06",
    "pipeline_decomposition": "AGI06",
    "pipeline_reduction": "AGI06",
    "pipeline_expansion": "AGI06",
    "pipeline_sampling": "AGI06",
    "pipeline_balancing": "AGI06",
    "pipeline_labeling": "AGI06",
    "pipeline_annotation": "AGI06",
    "pipeline_validation": "AGI06",
    "pipeline_verification": "AGI06",
    "pipeline_quality": "AGI06",
    "pipeline_profiling": "AGI06",
    "pipeline_lineage": "AGI06",
    "pipeline_provenance": "AGI06",
    "pipeline_curation": "AGI06",
    "pipeline_preprocessing": "AGI06",
    "pipeline_postprocessing": "AGI06",
    # (repeat for coverage, synonyms, etc.)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque(maxlen=10000)
        self.error_counts = collections.Counter()
        self.query_timestamps = collections.deque(maxlen=10000)
        self.latencies = collections.deque(maxlen=10000)
        self.query_log = collections.deque(maxlen=10000)

    def record_query(self, query_id: str, latency_ms: float):
        now = time.time()
        self.query_times.append((query_id, now, latency_ms))
        self.query_timestamps.append(now)
        self.latencies.append(latency_ms)
        self.query_log.append((query_id, now, latency_ms))

    def record_error(self, error_type: str):
        self.error_counts[error_type] += 1

    def get_latency_stats(self):
        if not self.latencies:
            return {"count": 0, "mean": None, "stdev": None, "min": None, "max": None}
        return {
            "count": len(self.latencies),
            "mean": statistics.mean(self.latencies),
            "stdev": statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0.0,
            "min": min(self.latencies),
            "max": max(self.latencies),
        }

    def queries_last_hour(self):
        now = time.time()
        one_hour_ago = now - 3600
        return sum(1 for t in self.query_timestamps if t >= one_hour_ago)

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    GENERAL_KNOWLEDGE = auto()
    REASONING = auto()
    SCRAPING = auto()
    MEMORY = auto()
    SYNCHRONIZATION = auto()
    SECURITY = auto()
    CLOUD = auto()
    UNKNOWN = auto()

class RoutingMode(Enum):
    DEFAULT = auto()
    PARALLEL = auto()
    CASCADE = auto()
    SINGLE = auto()

class QueryRequest:
    def __init__(self, text: str, mode: RoutingMode = RoutingMode.DEFAULT, meta: Optional[dict] = None):
        self.text = text
        self.mode = mode
        self.meta = meta or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, categories: List[IssueCategory], priority: int = 1):
        self.engine_id = engine_id
        self.url = url
        self.categories = categories
        self.priority = priority

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, success: bool, error: Optional[str] = None):
        self.engine_id = engine_id
        self.response = response
        self.success = success
        self.error = error

# --- Sub-Engine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "AGI01_CORTEX": SubEngineConfig(
        engine_id="AGI01_CORTEX",
        url="http://agi01-cortex:8080/query",
        categories=[IssueCategory.GENERAL_KNOWLEDGE, IssueCategory.REASONING],
        priority=10
    ),
    "AGI06_FORGE_X": SubEngineConfig(
        engine_id="AGI06_FORGE_X",
        url="http://agi06-forge-x:8080/query",
        categories=[IssueCategory.REASONING, IssueCategory.SECURITY],
        priority=9
    ),
    "AGI08_SENTINEL_X": SubEngineConfig(
        engine_id="AGI08_SENTINEL_X",
        url="http://agi08-sentinel-x:8080/query",
        categories=[IssueCategory.SECURITY, IssueCategory.SCRAPING],
        priority=8
    ),
    "KNOWLEDGE_FORGE_WORKER": SubEngineConfig(
        engine_id="KNOWLEDGE_FORGE_WORKER",
        url="http://knowledge-forge-worker:8080/query",
        categories=[IssueCategory.GENERAL_KNOWLEDGE, IssueCategory.MEMORY],
        priority=7
    ),
    "ECHO_SHARED_BRAIN": SubEngineConfig(
        engine_id="ECHO_SHARED_BRAIN",
        url="http://echo-shared-brain:8080/query",
        categories=[IssueCategory.MEMORY, IssueCategory.SYNCHRONIZATION],
        priority=6
    ),
    "OMNISYNC": SubEngineConfig(
        engine_id="OMNISYNC",
        url="http://omnisync:8080/query",
        categories=[IssueCategory.SYNCHRONIZATION, IssueCategory.CLOUD],
        priority=5
    ),
    "SHADOWGLASS_SCRAPER": SubEngineConfig(
        engine_id="SHADOWGLASS_SCRAPER",
        url="http://shadowglass-scraper:8080/query",
        categories=[IssueCategory.SCRAPING],
        priority=4
    ),
    "ENCORE_CLOUD_SCRAPER": SubEngineConfig(
        engine_id="ENCORE_CLOUD_SCRAPER",
        url="http://encore-cloud-scraper:8080/query",
        categories=[IssueCategory.CLOUD, IssueCategory.SCRAPING],
        priority=3
    ),
}

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = 0
        self.recovery_timeout = recovery_timeout

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def can_attempt(self):
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if (time.time() - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            else:
                return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

    def get_state(self):
        return self.state

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, registry: Dict[str, SubEngineConfig], ttl: int = 30):
        self.registry = registry
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.ttl = ttl
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker() for eid in registry
        }

    async def _ping_engine(self, url: str, timeout: int = 2) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url.replace("/query", "/health"), timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "healthy":
                            return SubEngineStatus.HEALTHY
                        elif data.get("status") == "degraded":
                            return SubEngineStatus.DEGRADED
                        else:
                            return SubEngineStatus.UNHEALTHY
                    else:
                        return SubEngineStatus.UNHEALTHY
        except Exception:
            return SubEngineStatus.UNHEALTHY

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        now = time.time()
        if engine_id in self.health_cache:
            status, ts = self.health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        config = self.registry[engine_id]
        status = await self._ping_engine(config.url)
        self.health_cache[engine_id] = (status, now)
        cb = self.circuit_breakers[engine_id]
        if status == SubEngineStatus.HEALTHY:
            cb.record_success()
        else:
            cb.record_failure()
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for eid in self.registry:
            tasks.append(self.check_health(eid))
        healths = await asyncio.gather(*tasks)
        for eid, status in zip(self.registry, healths):
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid, (status, ts) in self.health_cache.items():
            if now - ts < self.ttl and status == SubEngineStatus.HEALTHY:
                cb = self.circuit_breakers[eid]
                if cb.get_state() != CircuitBreakerState.OPEN:
                    healthy.append(eid)
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    CATEGORY_KEYWORDS = {
        IssueCategory.GENERAL_KNOWLEDGE: ["what", "who", "when", "where", "fact", "explain", "define"],
        IssueCategory.REASONING: ["why", "reason", "explain", "infer", "logic", "deduce", "analyze"],
        IssueCategory.SCRAPING: ["scrape", "crawl", "web", "extract", "site", "url", "page"],
        IssueCategory.MEMORY: ["remember", "recall", "store", "retrieve", "history", "memory"],
        IssueCategory.SYNCHRONIZATION: ["sync", "synchronize", "update", "merge", "replicate"],
        IssueCategory.SECURITY: ["secure", "security", "threat", "attack", "vulnerability", "protect"],
        IssueCategory.CLOUD: ["cloud", "aws", "azure", "gcp", "storage", "bucket", "cloud scraper"],
    }

    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_l = text.lower()
        found = set()
        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_l:
                    found.add(cat)
        if not found:
            found.add(IssueCategory.UNKNOWN)
        return list(found)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        healthy_ids = set(self.health_monitor.get_healthy_engines())
        selected = []
        for eid, config in self.registry.items():
            if eid not in healthy_ids:
                continue
            if any(cat in config.categories for cat in categories):
                selected.append(config)
        if not selected:
            # fallback: pick highest priority healthy engine
            healthy_configs = [self.registry[eid] for eid in healthy_ids]
            if healthy_configs:
                selected = sorted(healthy_configs, key=lambda c: -c.priority)[:1]
        if mode == RoutingMode.SINGLE and selected:
            selected = [max(selected, key=lambda c: c.priority)]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Custom rules based on meta or text
        if query.meta.get("force_engine"):
            return [query.meta["force_engine"]]
        if "scrape" in query.text.lower():
            return ["SHADOWGLASS_SCRAPER", "ENCORE_CLOUD_SCRAPER"]
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        cats = self._classify_domain(query.text)
        overlap = len(set(engine.categories) & set(cats))
        score = overlap * engine.priority
        if "cloud" in query.text.lower() and IssueCategory.CLOUD in engine.categories:
            score += 2
        if "security" in query.text.lower() and IssueCategory.SECURITY in engine.categories:
            score += 2
        return score

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        # fallback: remove engine, try next best
        healthy = self.health_monitor.get_healthy_engines()
        fallback = [eid for eid in healthy if eid != engine_id]
        if not fallback:
            # as last resort, try all engines
            fallback = list(self.registry.keys())
        return fallback

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        forced = self._apply_routing_rules(query)
        if forced:
            cats = self._classify_domain(query.text)
            return RoutingDecision(forced, cats, query.mode)
        cats = self._classify_domain(query.text)
        candidates = self._select_engines(cats, query.mode)
        if not candidates:
            candidates = [self.registry[eid] for eid in self.registry]
        # Score and sort
        scored = [(self._score_engine_relevance(cfg, query), cfg) for cfg in candidates]
        scored = sorted(scored, key=lambda x: -x[0])
        selected = [cfg.engine_id for _, cfg in scored if _ > 0]
        if not selected:
            selected = [candidates[0].engine_id]
        return RoutingDecision(selected, cats, query.mode)

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, registry: Dict[str, SubEngineConfig], health_monitor: SubEngineHealthMonitor):
        self.registry = registry
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.can_attempt():
            return SubEngineResponse(engine_config.engine_id, None, False, error="Circuit breaker open")
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query.text, "meta": query.meta}
                async with session.post(engine_config.url, json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return SubEngineResponse(engine_config.engine_id, data, True)
                    else:
                        cb.record_failure()
                        return SubEngineResponse(engine_config.engine_id, None, False, error=f"HTTP {resp.status}")
        except Exception as e:
            cb.record_failure()
            return SubEngineResponse(engine_config.engine_id, None, False, error=str(e))

    async def dispatch_query(self, query: QueryRequest, engines: List[str]) -> List[SubEngineResponse]:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        responses = []
        for config in configs:
            resp = await self._call_sub_engine(config, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[str]) -> Dict[str, Any]:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        tasks = [self._call_sub_engine(cfg, query) for cfg in configs]
        results = await asyncio.gather(*tasks)
        merged = self._merge_responses(results)
        return merged

    async def dispatch_cascade(self, query: QueryRequest, engines: List[str]) -> Any:
        configs = [self.registry[eid] for eid in engines if eid in self.registry]
        for config in configs:
            resp = await self._call_sub_engine(config, query)
            if resp.success:
                return resp.response
        return {"error": "All engines failed"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        # Simple merge: aggregate all responses by engine_id
        merged = {}
        for resp in responses:
            merged[resp.engine_id] = resp.response if resp.success else {"error": resp.error}
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Consensus: pick the most common response, or highest priority
        valid = [r for r in responses if r.success and r.response is not None]
        if not valid:
            return {"error": "No valid responses"}
        # Try to find consensus
        counts = {}
        for r in valid:
            key = str(r.response)
            counts[key] = counts.get(key, 0) + 1
        max_count = max(counts.values())
        consensus = [k for k, v in counts.items() if v == max_count]
        if len(consensus) == 1:
            return consensus[0]
        # Tie-breaker: pick from highest priority engine
        sorted_valid = sorted(valid, key=lambda r: -self.registry[r.engine_id].priority)
        return sorted_valid[0].response

# --- Example Usage (not executed here) ---

# health_monitor = SubEngineHealthMonitor(SUB_ENGINE_REGISTRY)
# router = QueryRouter(SUB_ENGINE_REGISTRY, health_monitor)
# orchestrator = SubEngineOrchestrator(SUB_ENGINE_REGISTRY, health_monitor)
#
# async def main():
#     query = QueryRequest("scrape the latest news from the cloud", mode=RoutingMode.PARALLEL)
#     routing_decision = router.route_query(query)
#     if routing_decision.mode == RoutingMode.PARALLEL:
#         result = await orchestrator.dispatch_parallel(query, routing_decision.engines)
#     elif routing_decision.mode == RoutingMode.CASCADE:
#         result = await orchestrator.dispatch_cascade(query, routing_decision.engines)
#     else:
#         responses = await orchestrator.dispatch_query(query, routing_decision.engines)
#         result = orchestrator._resolve_conflicts(responses)
#     print(result)
#
# asyncio.run(main())

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

authority_weights: Dict[AuthorityLevel, int] = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 90,
    AuthorityLevel.REGULATORY: 80,
    AuthorityLevel.CASE_LAW: 70,
    AuthorityLevel.TREATISE: 60,
    AuthorityLevel.PRACTICE: 50,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, returns the dominant authority level based on weights.
    If multiple sources have the same max weight, returns the one with highest enum order.
    """
    if not sources:
        raise ValueError("No authority sources provided for conflict resolution.")
    max_weight = -1
    dominant = None
    for source in sources:
        weight = authority_weights.get(source, 0)
        if weight > max_weight:
            max_weight = weight
            dominant = source
        elif weight == max_weight and dominant is not None:
            # tie-breaker: higher enum value wins
            if source.value > dominant.value:
                dominant = source
    return dominant

# ---------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------

BANNED_PHRASES: List[str] = [
    "clearly",
    "obviously",
    "without doubt",
    "undeniably",
    "incontrovertibly",
    "beyond question",
    "it is evident",
    "it is clear",
    "no doubt",
    "unquestionably",
    "manifestly",
    "patently",
    "categorically",
    "decidedly",
    "indisputably",
    "unequivocally",
    "irrefutably",
    "incontestably",
    "beyond dispute",
    "without fail",
    "infallibly",
    "inarguably",
    "incontrovertible",
    "plainly",
    "self-evidently",
    "absolutely",
    "definitely",
    "positively",
    "certainly",
    "undoubtedly",
    "no question",
]

class ConfidenceStratification(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Removes banned phrases from the text and appends a disclosure caveat.
    Returns cleaned text and caveat string.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub("", text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    disclosure_caveat = ("Note: This analysis avoids absolute or overly confident language to maintain epistemic humility. "
                         "Statements are presented with appropriate caution and openness to revision.")
    return cleaned_text, disclosure_caveat

def stratify_confidence(score: float) -> ConfidenceStratification:
    """
    Stratifies confidence score (0.0 to 1.0) into ConfidenceStratification categories.
    """
    if score >= 0.85:
        return ConfidenceStratification.DEFENSIBLE
    elif 0.65 <= score < 0.85:
        return ConfidenceStratification.AGGRESSIVE
    elif 0.4 <= score < 0.65:
        return ConfidenceStratification.DISCLOSURE
    else:
        return ConfidenceStratification.HIGH_RISK

# ---------------------------
# DEEP ANALYSIS
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decomposes the query into sub-issues based on doctrine keywords and logical segmentation.
    Returns a list of sub-issue strings.
    """
    # Simple heuristic: split by conjunctions and semicolons, and detect doctrine keywords
    doctrine_keywords = [
        "contract", "tort", "negligence", "liability", "damages", "property", "intellectual property",
        "due process", "equal protection", "statute", "regulation", "precedent", "jurisdiction",
        "causation", "breach", "offer", "acceptance", "consideration", "intent", "performance",
        "defense", "remedy", "injunction", "liability", "negligence", "duty", "standard of care"
    ]
    # Normalize query
    query_lower = query.lower()
    # Split by common separators
    parts = re.split(r';|\band\b|\bor\b|\n', query_lower)
    sub_issues = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Check if contains doctrine keyword
        if any(keyword in part for keyword in doctrine_keywords):
            sub_issues.append(part)
    if not sub_issues:
        # fallback: return whole query as one issue
        sub_issues.append(query)
    return sub_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Builds a dependency graph (DAG) of issues.
    Heuristic: issues mentioning other issues' keywords depend on them.
    """
    G = nx.DiGraph()
    for i, issue in enumerate(issues):
        G.add_node(i, text=issue)
    # Build edges based on keyword overlap
    for i, issue_i in enumerate(issues):
        words_i = set(re.findall(r'\w+', issue_i.lower()))
        for j, issue_j in enumerate(issues):
            if i == j:
                continue
            words_j = set(re.findall(r'\w+', issue_j.lower()))
            # If issue_i references keywords from issue_j, add edge i->j (i depends on j)
            if words_i & words_j and len(words_i & words_j) >= 2:
                G.add_edge(i, j)
    # Remove cycles if any by ignoring edges causing cycles
    try:
        cycles = list(nx.find_cycle(G))
        for edge in cycles:
            G.remove_edge(*edge)
    except nx.NetworkXNoCycle:
        pass
    return G

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs an 8-step resolution process on the query using doctrines and sub-engine results.
    Returns a dict with detailed analysis.
    """
    analysis = {}
    # Step 1: Issue Identification
    analysis['issues'] = doctrines
    # Step 2: Rule Statement
    analysis['rules'] = {d: f"Rule extracted for {d}" for d in doctrines}
    # Step 3: Application
    analysis['applications'] = {}
    for d in doctrines:
        res = sub_engine_results.get(d, {})
        analysis['applications'][d] = f"Applying rule for {d} with sub-engine result: {res}"
    # Step 4: Counterarguments
    analysis['counterarguments'] = {d: f"Potential counterarguments for {d}" for d in doctrines}
    # Step 5: Synthesis
    analysis['synthesis'] = "Synthesized analysis combining all doctrines and sub-engine results."
    # Step 6: Conclusion
    analysis['conclusion'] = f"Final conclusion for query: {query}"
    # Step 7: Confidence Scoring
    analysis['confidence'] = 0.75  # placeholder confidence score
    # Step 8: Recommendations
    analysis['recommendations'] = "Recommendations based on analysis."
    return analysis

def zoned_analysis(conclusion: str) -> Dict[str, str]:
    """
    Tags the conclusion into zones: PLANNING, REPORTING, AUDIT.
    Returns dict with zone as key and tagged conclusion as value.
    """
    zones = {
        "PLANNING": f"[PLANNING] {conclusion}",
        "REPORTING": f"[REPORTING] {conclusion}",
        "AUDIT": f"[AUDIT] {conclusion}",
    }
    return zones

# ---------------------------
# FACT FRAGILITY SCORING
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Scores a fact on verifiability, recharacterization risk, and testimony dependence.
    Returns dict with scores 0.0 to 1.0.
    """
    # Heuristics:
    # Verifiability: presence of citations, dates, concrete data increases score
    verifiability = 0.0
    if re.search(r'\b\d{4}\b', fact):
        verifiability += 0.3
    if re.search(r'\bsection\b|\barticle\b|\bclause\b', fact.lower()):
        verifiability += 0.4
    if re.search(r'\baccording to\b|\bper\b|\bsee\b', fact.lower()):
        verifiability += 0.3
    verifiability = min(verifiability, 1.0)

    # Recharacterization risk: presence of ambiguous terms, subjective adjectives increases risk
    ambiguous_terms = ["maybe", "possibly", "likely", "suggests", "appears", "could be", "seems"]
    risk = 0.0
    for term in ambiguous_terms:
        if term in fact.lower():
            risk += 0.25
    risk = min(risk, 1.0)

    # Testimony dependence: presence of first-person, quotes, or hearsay indicators
    testimony = 0.0
    if re.search(r'\baccording to\b|\bclaimed\b|\bsaid\b|\bstated\b|\breported\b', fact.lower()):
        testimony += 0.7
    if re.search(r'["\']', fact):
        testimony += 0.3
    testimony = min(testimony, 1.0)

    return {
        "verifiability": verifiability,
        "recharacterization_risk": risk,
        "testimony_dependence": testimony,
    }

# ---------------------------
# SEMANTIC NORMALIZATION
# ---------------------------

DOMAIN_TERM_MAPPINGS: Dict[str, str] = {
    # 50+ domain term mappings (lowercase keys)
    "agreement": "contract",
    "contractual obligation": "contract",
    "breach of contract": "breach",
    "negligent act": "negligence",
    "liability exposure": "liability",
    "intellectual property rights": "intellectual property",
    "due process clause": "due process",
    "equal protection clause": "equal protection",
    "statutory provision": "statute",
    "regulatory requirement": "regulation",
    "precedential case": "precedent",
    "jurisdictional issue": "jurisdiction",
    "causal connection": "causation",
    "offer and acceptance": "contract formation",
    "consideration element": "consideration",
    "intent to contract": "intent",
    "performance obligation": "performance",
    "affirmative defense": "defense",
    "legal remedy": "remedy",
    "injunctive relief": "injunction",
    "standard of care": "standard of care",
    "duty of care": "duty",
    "material breach": "breach",
    "contract damages": "damages",
    "property interest": "property",
    "trade secret": "intellectual property",
    "patent infringement": "intellectual property",
    "copyright violation": "intellectual property",
    "statutory interpretation": "statute",
    "administrative rule": "regulation",
    "case precedent": "precedent",
    "venue issue": "jurisdiction",
    "proximate cause": "causation",
    "offeror": "contract formation",
    "offeree": "contract formation",
    "express contract": "contract",
    "implied contract": "contract",
    "unilateral contract": "contract",
    "bilateral contract": "contract",
    "contract consideration": "consideration",
    "contract capacity": "capacity",
    "contract legality": "legality",
    "contract performance": "performance",
    "contract breach": "breach",
    "contract rescission": "remedy",
    "contract waiver": "defense",
    "contract assignment": "contract",
    "contract novation": "contract",
    "contract modification": "contract",
    "contract interpretation": "contract",
    "contract discharge": "contract",
    "contract damages": "damages",
    "contract specific performance": "remedy",
    "contract restitution": "remedy",
}

def normalize_query(text: str) -> str:
    """
    Normalizes domain-specific terms in the query text to standardized terms.
    """
    text_lower = text.lower()
    # Sort keys by length descending to replace longer phrases first
    sorted_terms = sorted(DOMAIN_TERM_MAPPINGS.keys(), key=len, reverse=True)
    for term in sorted_terms:
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        replacement = DOMAIN_TERM_MAPPINGS[term]
        text_lower = pattern.sub(replacement, text_lower)
    return text_lower

# ---------------------------
# THREE-LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Simple in-memory doctrine cache with keyword matching.
    """
    def __init__(self):
        # key: keyword, value: cached analysis string
        self.cache: Dict[str, str] = {}

    def add(self, keyword: str, analysis: str):
        self.cache[keyword.lower()] = analysis

    def lookup(self, query: str, timeout_ms: int = 200) -> Optional[str]:
        """
        Attempts to find cached analysis matching keywords in query within timeout.
        Returns cached analysis or None.
        """
        start = time.time()
        query_lower = query.lower()
        for keyword, analysis in self.cache.items():
            if time.time() - start > timeout_ms / 1000:
                break
            if keyword in query_lower:
                return analysis
        return None

class SubEngineRouter:
    """
    Routes queries to relevant sub-engines based on semantic search.
    """
    def __init__(self):
        # Mapping from domain keywords to sub-engine functions
        self.sub_engines: Dict[str, callable] = {}

    def register_sub_engine(self, keyword: str, func: callable):
        self.sub_engines[keyword.lower()] = func

    def route(self, query: str) -> Dict[str, Any]:
        """
        Dispatches query to relevant sub-engines based on keyword matching.
        Returns dict of sub-engine keyword -> result.
        """
        results = {}
        query_lower = query.lower()
        for keyword, func in self.sub_engines.items():
            if keyword in query_lower:
                results[keyword] = func(query)
        return results

class DeepMultiEngineAnalyzer:
    """
    Performs parallel dispatch to multiple sub-engines and merges results.
    """
    def __init__(self, sub_engines: Dict[str, callable]):
        self.sub_engines = sub_engines

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Dispatches query to all sub-engines in parallel, merges and resolves conflicts.
        """
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.sub_engines)) as executor:
            futures = {executor.submit(func, query): keyword for keyword, func in self.sub_engines.items()}
            for future in concurrent.futures.as_completed(futures):
                keyword = futures[future]
                try:
                    result = future.result()
                    results[keyword] = result
                except Exception as e:
                    results[keyword] = {"error": str(e)}
        merged = self.merge_results(results)
        return merged

    def merge_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merges results from multiple sub-engines, resolving conflicts.
        """
        # Simple heuristic: combine all results into one dict, conflicts resolved by authority level if present
        merged = {}
        for key, res in results.items():
            if isinstance(res, dict):
                for k, v in res.items():
                    if k not in merged:
                        merged[k] = v
                    else:
                        # Conflict resolution: if v has 'authority' key, use resolve_authority_conflict
                        if isinstance(v, dict) and 'authority' in v and isinstance(merged[k], dict) and 'authority' in merged[k]:
                            dominant = resolve_authority_conflict([v['authority'], merged[k]['authority']])
                            merged[k] = v if v['authority'] == dominant else merged[k]
                        else:
                            # fallback: keep existing
                            pass
            else:
                # Non-dict result, store by key
                merged[key] = res
        return merged

class CuriosityEngine:
    """
    CURIOSITY Autonomous Learning Engine backbone orchestrator.
    Implements three-layer response system.
    """
    def __init__(self):
        self.doctrine_cache = DoctrineCache()
        self.sub_engine_router = SubEngineRouter()
        self.deep_analyzer = None  # will be set after sub-engines registered

    def register_sub_engine(self, keyword: str, func: callable):
        self.sub_engine_router.register_sub_engine(keyword, func)

    def initialize_deep_analyzer(self):
        self.deep_analyzer = DeepMultiEngineAnalyzer(self.sub_engine_router.sub_engines)

    def three_layer_response(self, query: str) -> Dict[str, Any]:
        """
        Executes the three-layer response:
        1) Doctrine cache lookup (0-200ms)
        2) Semantic search + sub-engine routing
        3) Deep multi-engine analysis
        """
        # Layer 1: Doctrine cache lookup
        cache_result = self.doctrine_cache.lookup(query)
        if cache_result:
            return {"layer": 1, "result": cache_result}

        # Layer 2: Semantic search + sub-engine routing
        sub_engine_results = self.sub_engine_router.route(query)
        if sub_engine_results:
            return {"layer": 2, "result": sub_engine_results}

        # Layer 3: Deep multi-engine analysis
        if not self.deep_analyzer:
            self.initialize_deep_analyzer()
        deep_result = self.deep_analyzer.analyze(query)
        return {"layer": 3, "result": deep_result}

# ---------------------------
# Example Sub-Engines (Stubs)
# ---------------------------

def contract_sub_engine(query: str) -> Dict[str, Any]:
    # Stub analysis for contract-related queries
    return {
        "analysis": f"Contract analysis for query: {query}",
        "authority": AuthorityLevel.STATUTORY,
        "confidence": 0.8,
    }

def tort_sub_engine(query: str) -> Dict[str, Any]:
    # Stub analysis for tort-related queries
    return {
        "analysis": f"Tort analysis for query: {query}",
        "authority": AuthorityLevel.CASE_LAW,
        "confidence": 0.7,
    }

def ip_sub_engine(query: str) -> Dict[str, Any]:
    # Stub analysis for intellectual property queries
    return {
        "analysis": f"IP analysis for query: {query}",
        "authority": AuthorityLevel.TREATISE,
        "confidence": 0.75,
    }

# ---------------------------
# Initialization and Example Usage
# ---------------------------

curiosity_engine = CuriosityEngine()
curiosity_engine.doctrine_cache.add("contract", "Cached contract doctrine analysis.")
curiosity_engine.doctrine_cache.add("tort", "Cached tort doctrine analysis.")

curiosity_engine.register_sub_engine("contract", contract_sub_engine)
curiosity_engine.register_sub_engine("tort", tort_sub_engine)
curiosity_engine.register_sub_engine("intellectual property", ip_sub_engine)
curiosity_engine.initialize_deep_analyzer()

# The above code provides the backbone for the CURIOSITY engine's PART 4:
# - Three-layer response system with doctrine cache, semantic routing, and deep analysis
# - Authority hardening with enum and conflict resolution
# - Epistemic guardrails with banned phrases and confidence stratification
# - Deep analysis with doctrine decomposition, DAG building, 8-step resolution, zoned analysis
# - Fact fragility scoring
# - Semantic normalization with domain term mappings

# The engine is ready to be integrated with other parts for full functionality.

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
        self.lock = threading.Lock()
        self.queries: deque = deque(maxlen=100_000)
        self.errors: deque = deque(maxlen=10_000)
        self.doctrine_hits: Counter = Counter()
        self.doctrine_total: Counter = Counter()
        self.sub_engine_stats: Dict[str, List[float]] = defaultdict(list)
        self.query_times: deque = deque(maxlen=100_000)
        self.query_by_id: Dict[str, QueryTelemetry] = {}
        self.cache_hits: int = 0
        self.cache_misses: int = 0

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.queries.append(telemetry)
            self.query_times.append(telemetry.timestamp)
            self.query_by_id[telemetry.query_id] = telemetry
            if telemetry.cache_hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
            for engine in telemetry.engines_invoked:
                self.sub_engine_stats[engine].append(telemetry.latency_ms)
            if telemetry.error:
                self.errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self.doctrine_hits[engine] += 1
            for engine in telemetry.engines_invoked:
                self.doctrine_total[engine] += 1

    def record_error(self, query_id: str, error: str):
        with self.lock:
            if query_id in self.query_by_id:
                telemetry = self.query_by_id[query_id]
                telemetry.error = error
                self.errors.append(telemetry)

    def get_latency_stats(self) -> Dict[str, Any]:
        with self.lock:
            latencies = [q.latency_ms for q in self.queries if q.latency_ms is not None]
            if not latencies:
                return {}
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            return {
                "avg": statistics.mean(latencies_sorted),
                "p50": latencies_sorted[int(0.5 * n)],
                "p95": latencies_sorted[int(0.95 * n)-1],
                "p99": latencies_sorted[int(0.99 * n)-1],
                "min": latencies_sorted[0],
                "max": latencies_sorted[-1],
                "count": n
            }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self.lock:
            rates = {}
            for doctrine in self.doctrine_total:
                total = self.doctrine_total[doctrine]
                hits = self.doctrine_hits.get(doctrine, 0)
                if total > 0:
                    rates[doctrine] = hits / total
                else:
                    rates[doctrine] = 0.0
            return rates

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self.lock:
            return sum(1 for t in self.query_times if t >= cutoff)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            stats = {}
            for engine, latencies in self.sub_engine_stats.items():
                if not latencies:
                    continue
                lat_sorted = sorted(latencies)
                n = len(lat_sorted)
                stats[engine] = {
                    "avg_latency_ms": statistics.mean(lat_sorted),
                    "p95_latency_ms": lat_sorted[int(0.95 * n)-1],
                    "count": n
                }
            return stats

# --------- 2. DRIFT_WATCHER ---------

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baseline_confidence: Dict[str, float] = {}
        self.confidence_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.drift_alerts: List[Dict[str, Any]] = []
        self.drift_threshold = 0.10  # 10%

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baseline_confidence[doctrine] = confidence
            self.confidence_history[doctrine].append(confidence)

    def detect_drift(self, doctrine: str, new_confidence: float, timestamp: Optional[float]=None):
        with self.lock:
            history = self.confidence_history[doctrine]
            history.append(new_confidence)
            baseline = self.baseline_confidence.get(doctrine)
            if baseline is None:
                self.baseline_confidence[doctrine] = new_confidence
                return None
            drift = abs(new_confidence - baseline) / (baseline + 1e-8)
            if drift > self.drift_threshold:
                alert = {
                    "doctrine": doctrine,
                    "baseline": baseline,
                    "current": new_confidence,
                    "drift": drift,
                    "timestamp": timestamp or time.time()
                }
                self.drift_alerts.append(alert)
                return alert
            return None

    def get_drift_report(self) -> Dict[str, Any]:
        with self.lock:
            report = {}
            for doctrine, history in self.confidence_history.items():
                if len(history) < 2:
                    continue
                baseline = self.baseline_confidence.get(doctrine, 0.0)
                current = history[-1]
                drift = abs(current - baseline) / (baseline + 1e-8)
                report[doctrine] = {
                    "baseline": baseline,
                    "current": current,
                    "drift": drift,
                    "history": list(history)
                }
            return {
                "drift_report": report,
                "alerts": list(self.drift_alerts)
            }

# --------- 3. COVERAGE_MAP ---------

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered: Counter = Counter()
        self.missed: deque = deque(maxlen=10_000)
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)
        self.epistemic_gap_queries: deque = deque(maxlen=10_000)
        self.query_to_doctrines: Dict[str, List[str]] = {}
        self.total_queries: int = 0

    def record_triggered(self, doctrine: str, query_id: str, sub_engine: Optional[str]=None):
        with self.lock:
            self.triggered[doctrine] += 1
            if sub_engine:
                self.sub_engine_coverage[sub_engine][doctrine] += 1
            self.query_to_doctrines.setdefault(query_id, []).append(doctrine)
            self.total_queries += 1

    def record_missed(self, query_id: str, query_text: str):
        with self.lock:
            self.missed.append((query_id, query_text))
            self.epistemic_gap_queries.append((query_id, query_text))
            self.total_queries += 1

    def get_coverage_report(self) -> Dict[str, Any]:
        with self.lock:
            doctrine_coverage = dict(self.triggered)
            sub_engine_stats = {
                engine: dict(counter)
                for engine, counter in self.sub_engine_coverage.items()
            }
            epistemic_gaps = list(self.epistemic_gap_queries)
            return {
                "doctrine_coverage": doctrine_coverage,
                "sub_engine_coverage": sub_engine_stats,
                "epistemic_gap_count": len(epistemic_gaps),
                "epistemic_gap_queries": epistemic_gaps[-100:],
                "total_queries": self.total_queries
            }

    def identify_epistemic_gaps(self) -> List[Tuple[str, str]]:
        with self.lock:
            return list(self.epistemic_gap_queries)

    def get_per_sub_engine_coverage(self) -> Dict[str, Dict[str, int]]:
        with self.lock:
            return {
                engine: dict(counter)
                for engine, counter in self.sub_engine_coverage.items()
            }

# --------- 4. DETERMINISM_HASH ---------

def compute_determinism_hash(query: Any, response: Any) -> str:
    def canonicalize(obj):
        if isinstance(obj, dict):
            return {k: canonicalize(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [canonicalize(x) for x in obj]
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        else:
            return str(obj)
    canonical_query = canonicalize(query)
    canonical_response = canonicalize(response)
    payload = json.dumps({"query": canonical_query, "response": canonical_response}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

# --------- 5. AUDIT_TRAIL ---------

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        os.makedirs(audit_dir, exist_ok=True)
        self.current_date = None
        self.current_file = None
        self.lock = threading.Lock()
        self._rotate_file()

    def _get_audit_filename(self, date: str) -> str:
        return os.path.join(self.audit_dir, f"audit_{date}.jsonl")

    def _rotate_file(self):
        with self.lock:
            date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            if self.current_date != date:
                if self.current_file:
                    self.current_file.close()
                filename = self._get_audit_filename(date)
                self.current_file = open(filename, "a", buffering=1)
                self.current_date = date

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str], mode: str, confidence: float, latency: float, cache_hit: bool):
        self._rotate_file()
        entry = {
            "query_id": query_id,
            "timestamp": timestamp,
            "engine_id": engine_id,
            "engines_invoked": engines_invoked,
            "mode": mode,
            "confidence": confidence,
            "latency_ms": latency,
            "cache_hit": cache_hit
        }
        with self.lock:
            self.current_file.write(json.dumps(entry) + "\n")

    def forensic_replay(self, date: str) -> List[Dict[str, Any]]:
        filename = self._get_audit_filename(date)
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self.lock:
            if self.current_file:
                self.current_file.close()
                self.current_file = None

# --------- 6. PERFORMANCE_PROFILER ---------

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.latency_by_engine: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10_000))
        self.error_count_by_engine: Counter = Counter()
        self.invocation_count_by_engine: Counter = Counter()
        self.availability_by_engine: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10_000))
        self.sla_targets: Dict[str, Dict[str, float]] = {}  # e.g. {"latency_ms": 1000, "error_rate": 0.01, "availability": 0.999}

    def record(self, engine: str, latency_ms: float, error: Optional[str]=None, available: bool=True):
        with self.lock:
            self.latency_by_engine[engine].append(latency_ms)
            self.invocation_count_by_engine[engine] += 1
            if error:
                self.error_count_by_engine[engine] += 1
            self.availability_by_engine[engine].append(1 if available else 0)

    def set_sla(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_targets[engine] = {
                "latency_ms": latency_ms,
                "error_rate": error_rate,
                "availability": availability
            }

    def get_engine_stats(self, engine: str) -> Dict[str, Any]:
        with self.lock:
            latencies = list(self.latency_by_engine[engine])
            invocations = self.invocation_count_by_engine[engine]
            errors = self.error_count_by_engine[engine]
            availability = list(self.availability_by_engine[engine])
            stats = {}
            if latencies:
                lat_sorted = sorted(latencies)
                n = len(lat_sorted)
                stats["avg_latency_ms"] = statistics.mean(lat_sorted)
                stats["p95_latency_ms"] = lat_sorted[int(0.95 * n)-1]
                stats["max_latency_ms"] = lat_sorted[-1]
                stats["min_latency_ms"] = lat_sorted[0]
                stats["count"] = n
            else:
                stats["avg_latency_ms"] = None
                stats["count"] = 0
            if invocations > 0:
                stats["error_rate"] = errors / invocations
            else:
                stats["error_rate"] = None
            if availability:
                stats["availability"] = sum(availability) / len(availability)
            else:
                stats["availability"] = None
            sla = self.sla_targets.get(engine)
            if sla:
                stats["sla"] = sla
                stats["sla_violations"] = {
                    "latency": stats["avg_latency_ms"] > sla["latency_ms"] if stats["avg_latency_ms"] is not None else False,
                    "error_rate": stats["error_rate"] > sla["error_rate"] if stats["error_rate"] is not None else False,
                    "availability": stats["availability"] < sla["availability"] if stats["availability"] is not None else False
                }
            return stats

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            return {engine: self.get_engine_stats(engine) for engine in self.latency_by_engine}

# --------- Example Orchestrator Integration ---------

class CuriosityBackbone:
    def __init__(self, audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage = CoverageTracker()
        self.audit = AuditTrailWriter(audit_dir)
        self.profiler = PerformanceProfiler()

    def record_query(self, query_id: str, timestamp: float, latency_ms: float, cache_hit: bool, engines_invoked: List[str], mode: str, confidence: float, error: Optional[str]=None):
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry.record_query(telemetry)
        for engine in engines_invoked:
            self.profiler.record(engine, latency_ms, error=error)
        self.audit.write(query_id, timestamp, engines_invoked[0] if engines_invoked else "none", engines_invoked, mode, confidence, latency_ms, cache_hit)

    def record_doctrine_trigger(self, doctrine: str, query_id: str, sub_engine: Optional[str]=None):
        self.coverage.record_triggered(doctrine, query_id, sub_engine=sub_engine)

    def record_doctrine_missed(self, query_id: str, query_text: str):
        self.coverage.record_missed(query_id, query_text)

    def record_confidence(self, doctrine: str, confidence: float, timestamp: Optional[float]=None):
        self.drift_watcher.record_baseline(doctrine, confidence)
        alert = self.drift_watcher.detect_drift(doctrine, confidence, timestamp=timestamp)
        return alert

    def compute_hash(self, query: Any, response: Any) -> str:
        return compute_determinism_hash(query, response)

    def get_telemetry_stats(self):
        return self.telemetry.get_latency_stats()

    def get_coverage_report(self):
        return self.coverage.get_coverage_report()

    def get_drift_report(self):
        return self.drift_watcher.get_drift_report()

    def get_performance_stats(self):
        return self.profiler.get_all_stats()

    def forensic_replay(self, date: str):
        return self.audit.forensic_replay(date)

    def close(self):
        self.audit.close()

# ═══════════════════════════════════════════════════════════════
# PASS 6: FASTAPI SERVER (imports already at top of file)
# ═══════════════════════════════════════════════════════════════

# --- Constants and Configurations ---

ENGINE_ID = "AGI02"
ENGINE_NAME = "CURIOSITY"
ENGINE_PORT = 8871

SUB_ENGINES = {
    "AGI01": {"name": "CORTEX", "url": "http://localhost:8872"},
    "AGI06": {"name": "FORGE-X", "url": "http://localhost:8873"},
    "AGI08": {"name": "SENTINEL-X", "url": "http://localhost:8874"},
    "KFWR": {"name": "Knowledge Forge Worker", "url": "http://localhost:8875"},
    "ESB": {"name": "Echo Shared Brain", "url": "http://localhost:8876"},
    "OMNI": {"name": "OmniSync", "url": "http://localhost:8877"},
    "SGS": {"name": "ShadowGlass Scraper", "url": "http://localhost:8878"},
    "ECCS": {"name": "ENCORE Cloud Scraper", "url": "http://localhost:8879"},
}

SUB_ENGINE_TIMEOUT = 5.0  # seconds
CIRCUIT_BREAKER_THRESHOLD = 3
CIRCUIT_BREAKER_RESET_TIME = 60  # seconds

# --- Logging Setup ---

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(ENGINE_NAME)

# --- Data Models ---


class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the capital of France?")
    metadata: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query: str
    results: Dict[str, Any]
    merged: bool = True
    timestamp: datetime


class HealthStatus(BaseModel):
    status: str
    details: Optional[Dict[str, Any]] = None


class MetricsResponse(BaseModel):
    latency_ms: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Any]


class CoverageReport(BaseModel):
    doctrines_covered: Set[str]
    epistemic_gaps: List[str]


class DriftReport(BaseModel):
    drift_detected: bool
    drift_score: float
    details: Optional[Dict[str, Any]]


class DoctrineInfo(BaseModel):
    doctrine_id: str
    description: str
    last_updated: datetime


class RoutingRule(BaseModel):
    domain: str
    engines: List[str]


class RoutingInfo(BaseModel):
    rules: List[RoutingRule]
    engine_registry: Dict[str, str]


class SubEngineHealth(BaseModel):
    engine_id: str
    name: str
    status: str
    last_checked: datetime
    error: Optional[str] = None


class RouteDryRunRequest(BaseModel):
    query: str


class RouteDryRunResponse(BaseModel):
    query: str
    engines_to_invoke: List[str]


class AnalyzeRequest(BaseModel):
    query: str
    analysis_depth: Optional[int] = 3


class AnalyzeResponse(BaseModel):
    query: str
    analysis_results: Dict[str, Any]


# --- Global State and Caches ---

doctrine_cache: Dict[str, DoctrineInfo] = {}
search_index: Dict[str, Set[str]] = {}
telemetry_data: Dict[str, Any] = {
    "latencies": [],
    "cache_hits": 0,
    "cache_misses": 0,
    "query_timestamps": [],
    "sub_engine_stats": {k: {"calls": 0, "failures": 0} for k in SUB_ENGINES.keys()},
}
health_monitor_data: Dict[str, SubEngineHealth] = {}
routing_rules: List[RoutingRule] = []
circuit_breakers: Dict[str, Dict[str, Any]] = {}

# --- Utility Functions ---


def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized


def classify_domain(query: str) -> str:
    # Dummy classification logic based on keywords
    keywords_to_domain = {
        "finance": "finance",
        "health": "health",
        "science": "science",
        "technology": "technology",
        "history": "history",
        "geography": "geography",
        "law": "law",
    }
    query_lower = query.lower()
    for keyword, domain in keywords_to_domain.items():
        if keyword in query_lower:
            logger.debug(f"Classified domain '{domain}' for query '{query}'")
            return domain
    logger.debug(f"Default domain 'general' for query '{query}'")
    return "general"


def route_query(domain: str) -> List[str]:
    # Routing rules based on domain
    domain_engine_map = {
        "finance": ["AGI01", "AGI06"],
        "health": ["AGI08", "KFWR"],
        "science": ["AGI01", "OMNI"],
        "technology": ["AGI06", "ESB"],
        "history": ["AGI01", "SGS"],
        "geography": ["AGI01", "ECCS"],
        "law": ["AGI08", "KFWR"],
        "general": ["AGI01", "AGI06", "AGI08"],
    }
    engines = domain_engine_map.get(domain, ["AGI01"])
    logger.debug(f"Routing domain '{domain}' to engines {engines}")
    return engines


async def dispatch_to_sub_engine(
    engine_id: str, query: str
) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    url = SUB_ENGINES[engine_id]["url"] + "/query"
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}

    # Circuit breaker check
    cb = circuit_breakers.setdefault(engine_id, {"failures": 0, "last_failure_time": None, "open": False})
    if cb["open"]:
        elapsed = (datetime.utcnow() - cb["last_failure_time"]).total_seconds()
        if elapsed > CIRCUIT_BREAKER_RESET_TIME:
            cb["open"] = False
            cb["failures"] = 0
            logger.info(f"Circuit breaker reset for engine {engine_id}")
        else:
            logger.warning(f"Circuit breaker open for engine {engine_id}, skipping call")
            return engine_id, None, "Circuit breaker open"

    try:
        async with httpx.AsyncClient(timeout=SUB_ENGINE_TIMEOUT) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
            return engine_id, data, None
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        telemetry_data["sub_engine_stats"][engine_id]["failures"] += 1
        cb["failures"] += 1
        cb["last_failure_time"] = datetime.utcnow()
        if cb["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
            cb["open"] = True
            logger.error(f"Circuit breaker opened for engine {engine_id} due to repeated failures")
        logger.error(f"Error dispatching to sub-engine {engine_id}: {e}")
        return engine_id, None, str(e)


def merge_sub_engine_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged_result = {}
    for resp in responses:
        if not resp:
            continue
        for k, v in resp.items():
            if k not in merged_result:
                merged_result[k] = v
            else:
                # Merge logic: if list, extend; if dict, update; else override
                if isinstance(merged_result[k], list) and isinstance(v, list):
                    merged_result[k].extend(v)
                elif isinstance(merged_result[k], dict) and isinstance(v, dict):
                    merged_result[k].update(v)
                else:
                    merged_result[k] = v
    logger.debug(f"Merged response: {merged_result}")
    return merged_result


def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for guardrails logic: filter sensitive info, ensure compliance, etc.
    filtered_response = response.copy()
    # Example: remove keys named 'debug_info'
    filtered_response.pop("debug_info", None)
    logger.debug("Applied guardrails to response")
    return filtered_response


def hash_query_response(query: str, response: Dict[str, Any]) -> str:
    combined = query + json.dumps(response, sort_keys=True)
    h = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    logger.debug(f"Hashed query-response: {h}")
    return h


def log_query_response(query: str, response: Dict[str, Any], hash_: str) -> None:
    # Placeholder for logging to persistent store or telemetry
    logger.info(f"Logged query hash: {hash_} for query: {query}")


def fallback_to_doctrine_cache(query: str) -> Optional[Dict[str, Any]]:
    # Attempt to find cached doctrine matching query keywords
    for doctrine_id, doctrine in doctrine_cache.items():
        if doctrine_id in query.lower():
            logger.info(f"Fallback to doctrine cache for query '{query}' with doctrine '{doctrine_id}'")
            return {"doctrine_id": doctrine_id, "description": doctrine.description}
    logger.info(f"No doctrine cache fallback available for query '{query}'")
    return None


def update_telemetry_latency(start_time: float) -> None:
    latency_ms = (time.time() - start_time) * 1000
    telemetry_data["latencies"].append(latency_ms)
    logger.debug(f"Recorded latency: {latency_ms:.2f} ms")


def get_cache_hit_rate() -> float:
    hits = telemetry_data["cache_hits"]
    misses = telemetry_data["cache_misses"]
    total = hits + misses
    if total == 0:
        return 0.0
    return hits / total


def get_queries_per_hour() -> float:
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    recent_queries = [ts for ts in telemetry_data["query_timestamps"] if ts > one_hour_ago]
    return len(recent_queries)


def get_sub_engine_health() -> List[SubEngineHealth]:
    now = datetime.utcnow()
    health_list = []
    for engine_id, info in SUB_ENGINES.items():
        health = health_monitor_data.get(engine_id)
        if health is None:
            health = SubEngineHealth(
                engine_id=engine_id,
                name=info["name"],
                status="unknown",
                last_checked=now,
                error="No data",
            )
        health_list.append(health)
    return health_list


def generate_coverage_report() -> CoverageReport:
    doctrines_covered = set(doctrine_cache.keys())
    epistemic_gaps = []  # Placeholder: logic to detect gaps in doctrines
    return CoverageReport(doctrines_covered=doctrines_covered, epistemic_gaps=epistemic_gaps)


def generate_drift_report() -> DriftReport:
    # Placeholder: drift detection logic comparing current vs historical data
    drift_detected = False
    drift_score = 0.0
    details = {"message": "No drift detected"}
    return DriftReport(drift_detected=drift_detected, drift_score=drift_score, details=details)


def list_doctrines() -> List[DoctrineInfo]:
    return list(doctrine_cache.values())


def get_routing_info() -> RoutingInfo:
    engine_registry = {k: v["name"] for k, v in SUB_ENGINES.items()}
    return RoutingInfo(rules=routing_rules, engine_registry=engine_registry)


def dry_run_route(query: str) -> List[str]:
    normalized = normalize_query(query)
    domain = classify_domain(normalized)
    engines = route_query(domain)
    return engines


async def deep_multi_engine_analysis(query: str, depth: int) -> Dict[str, Any]:
    # Placeholder for deep analysis logic invoking multiple engines iteratively
    results = {}
    current_query = query
    for i in range(depth):
        engines = dry_run_route(current_query)
        engine_results = {}
        for engine_id in engines:
            _, data, error = await dispatch_to_sub_engine(engine_id, current_query)
            if data:
                engine_results[engine_id] = data
            else:
                engine_results[engine_id] = {"error": error}
        results[f"depth_{i+1}"] = engine_results
        # For next iteration, pick best result or refine query (dummy logic)
        current_query = current_query + " (refined)"
    return results


async def check_sub_engine_health(engine_id: str) -> SubEngineHealth:
    url = SUB_ENGINES[engine_id]["url"] + "/health"
    now = datetime.utcnow()
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            status_str = data.get("status", "unknown")
            health = SubEngineHealth(
                engine_id=engine_id,
                name=SUB_ENGINES[engine_id]["name"],
                status=status_str,
                last_checked=now,
                error=None,
            )
            logger.debug(f"Health check OK for {engine_id}: {status_str}")
            return health
    except Exception as e:
        logger.error(f"Health check failed for {engine_id}: {e}")
        health = SubEngineHealth(
            engine_id=engine_id,
            name=SUB_ENGINES[engine_id]["name"],
            status="unhealthy",
            last_checked=now,
            error=str(e),
        )
        return health


async def health_monitor_loop():
    while True:
        tasks = [check_sub_engine_health(eid) for eid in SUB_ENGINES.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, SubEngineHealth):
                health_monitor_data[res.engine_id] = res
        await asyncio.sleep(30)


async def seed_search_index_loop():
    while True:
        # Placeholder: refresh search index from doctrines or external sources
        await asyncio.sleep(300)


async def telemetry_loop():
    while True:
        # Placeholder: send telemetry data to external monitoring system
        await asyncio.sleep(60)


async def initialize_doctrine_cache():
    # Placeholder: load doctrines from persistent storage or external source
    doctrine_cache.clear()
    now = datetime.utcnow()
    doctrine_cache["finance"] = DoctrineInfo(
        doctrine_id="finance",
        description="Financial domain knowledge base",
        last_updated=now,
    )
    doctrine_cache["health"] = DoctrineInfo(
        doctrine_id="health",
        description="Health domain knowledge base",
        last_updated=now,
    )
    doctrine_cache["science"] = DoctrineInfo(
        doctrine_id="science",
        description="Science domain knowledge base",
        last_updated=now,
    )
    doctrine_cache["technology"] = DoctrineInfo(
        doctrine_id="technology",
        description="Technology domain knowledge base",
        last_updated=now,
    )
    doctrine_cache["history"] = DoctrineInfo(
        doctrine_id="history",
        description="Historical domain knowledge base",
        last_updated=now,
    )
    doctrine_cache["general"] = DoctrineInfo(
        doctrine_id="general",
        description="General knowledge base",
        last_updated=now,
    )
    logger.info("Doctrine cache initialized with sample doctrines")


def register_routing_rules():
    global routing_rules
    routing_rules = [
        RoutingRule(domain="finance", engines=["AGI01", "AGI06"]),
        RoutingRule(domain="health", engines=["AGI08", "KFWR"]),
        RoutingRule(domain="science", engines=["AGI01", "OMNI"]),
        RoutingRule(domain="technology", engines=["AGI06", "ESB"]),
        RoutingRule(domain="history", engines=["AGI01", "SGS"]),
        RoutingRule(domain="geography", engines=["AGI01", "ECCS"]),
        RoutingRule(domain="law", engines=["AGI08", "KFWR"]),
        RoutingRule(domain="general", engines=["AGI01", "AGI06", "AGI08"]),
    ]
    logger.info("Routing rules registered")


# --- FastAPI App and Lifespan ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {ENGINE_NAME} engine (ID: {ENGINE_ID})")
    await initialize_doctrine_cache()
    register_routing_rules()
    health_task = asyncio.create_task(health_monitor_loop())
    search_task = asyncio.create_task(seed_search_index_loop())
    telemetry_task = asyncio.create_task(telemetry_loop())
    try:
        yield
    finally:
        health_task.cancel()
        search_task.cancel()
        telemetry_task.cancel()
        logger.info(f"Shutting down {ENGINE_NAME} engine")


app = FastAPI(
    title=f"{ENGINE_NAME} Autonomous Learning Engine",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    query = request.query
    normalized_query = normalize_query(query)
    domain = classify_domain(normalized_query)
    engines = route_query(domain)

    # Dispatch concurrently to sub-engines
    tasks = [dispatch_to_sub_engine(eid, normalized_query) for eid in engines]
    results = await asyncio.gather(*tasks)

    responses = []
    errors = {}
    for eid, data, error in results:
        if data:
            responses.append(data)
        if error:
            errors[eid] = error

    if not responses:
        # Fallback to doctrine cache
        fallback = fallback_to_doctrine_cache(normalized_query)
        if fallback:
            telemetry_data["cache_hits"] += 1
            response_data = fallback
        else:
            telemetry_data["cache_misses"] += 1
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="All sub-engines failed and no fallback available",
            )
    else:
        telemetry_data["cache_hits"] += 1
        response_data = merge_sub_engine_responses(responses)

    guarded_response = apply_guardrails(response_data)
    response_hash = hash_query_response(normalized_query, guarded_response)
    log_query_response(normalized_query, guarded_response, response_hash)
    telemetry_data["query_timestamps"].append(datetime.utcnow())
    update_telemetry_latency(start_time)

    return QueryResponse(
        query=query,
        results=guarded_response,
        merged=True,
        timestamp=datetime.utcnow(),
    )


@app.get("/health", response_model=Dict[str, HealthStatus])
async def health_endpoint():
    # Self health
    self_health = HealthStatus(status="healthy")
    # Sub-engine health
    sub_healths = {}
    for engine_id, health in health_monitor_data.items():
        sub_healths[engine_id] = HealthStatus(
            status=health.status,
            details={"last_checked": health.last_checked.isoformat(), "error": health.error},
        )
    return {"self": self_health, "sub_engines": sub_healths}


@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    avg_latency = (
        sum(telemetry_data["latencies"]) / len(telemetry_data["latencies"])
        if telemetry_data["latencies"]
        else 0.0
    )
    cache_hit_rate = get_cache_hit_rate()
    qph = get_queries_per_hour()
    sub_stats = telemetry_data["sub_engine_stats"]
    return MetricsResponse(
        latency_ms=avg_latency,
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=qph,
        sub_engine_stats=sub_stats,
    )


@app.get("/coverage", response_model=CoverageReport)
async def coverage_endpoint():
    report = generate_coverage_report()
    return report


@app.get("/drift", response_model=DriftReport)
async def drift_endpoint():
    report = generate_drift_report()
    return report


@app.get("/doctrines", response_model=List[DoctrineInfo])
async def doctrines_endpoint():
    doctrines = list_doctrines()
    return doctrines


@app.get("/routing", response_model=RoutingInfo)
async def routing_endpoint():
    routing = get_routing_info()
    return routing


@app.get("/sub-engines", response_model=List[SubEngineHealth])
async def sub_engines_endpoint():
    health_list = get_sub_engine_health()
    return health_list


@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    engines = dry_run_route(request.query)
    return RouteDryRunResponse(query=request.query, engines_to_invoke=engines)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    results = await deep_multi_engine_analysis(request.query, request.analysis_depth or 3)
    return AnalyzeResponse(query=request.query, analysis_results=results)


# --- Run Server ---


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")