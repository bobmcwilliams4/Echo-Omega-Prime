"""
E10 Cost Estimator Engine
TIE-20 Compliant | Port 8610
Domain: Query cost estimation, budget enforcement, cost-aware routing.

Estimates computational cost, LLM token usage, API calls, and wall-clock time
BEFORE a query is executed. Enables cost-aware routing and budget enforcement
across the entire ECHO OMEGA PRIME engine fleet.

Cost Dimensions:
  - LLM Token Cost (input/output by model)
  - API Call Cost (external services)
  - Compute Cost (CPU-ms per engine)
  - Storage Cost (R2/D1 read/write ops)
  - Time Cost (wall-clock estimate)
  - Total Monetary Cost (aggregated USD)
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import statistics
import sys
import time
import uuid
from collections import OrderedDict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI, HTTPException, Query as QParam, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

try:
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None  # type: ignore[misc,assignment]

# ─── Constants ────────────────────────────────────────────────────────────────
ENGINE_ID = "E10"
ENGINE_NAME = "Cost Estimator Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8610
ENGINE_DOMAIN = "cost_estimation"
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG = LOG_DIR / "e10_audit.jsonl"

logger.add(LOG_DIR / "e10_engine.log", rotation="50 MB", retention="30 days", level="DEBUG")
logger.add(AUDIT_LOG, rotation="20 MB", retention="90 days", level="INFO", serialize=True)

START_TIME = time.time()
QUERY_COUNT = 0
ERROR_COUNT = 0
CACHE_HITS = 0
CACHE_MISSES = 0


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS — TIE Component 17 (typed I/O)
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    LLM_TOKEN_COST = "LLM_TOKEN_COST"
    API_CALL_COST = "API_CALL_COST"
    COMPUTE_COST = "COMPUTE_COST"
    STORAGE_COST = "STORAGE_COST"
    TIME_COST = "TIME_COST"
    BUDGET_ENFORCEMENT = "BUDGET_ENFORCEMENT"
    CHAIN_COST = "CHAIN_COST"
    BATCH_COST = "BATCH_COST"
    CACHE_DISCOUNT = "CACHE_DISCOUNT"
    MODE_FACTOR = "MODE_FACTOR"
    ROUTING_DECISION = "ROUTING_DECISION"
    HISTORICAL_ANALYSIS = "HISTORICAL_ANALYSIS"


class BudgetAlertLevel(str, Enum):
    GREEN = "GREEN"
    YELLOW_50 = "YELLOW_50"
    ORANGE_75 = "ORANGE_75"
    RED_90 = "RED_90"
    CRITICAL_100 = "CRITICAL_100"


class CostDimension(str, Enum):
    LLM_TOKENS = "LLM_TOKENS"
    API_CALLS = "API_CALLS"
    COMPUTE_MS = "COMPUTE_MS"
    STORAGE_OPS = "STORAGE_OPS"
    WALL_CLOCK_S = "WALL_CLOCK_S"
    MONETARY_USD = "MONETARY_USD"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    categories: List[IssueCategory] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    target_engine: Optional[str] = None
    target_engines: List[str] = Field(default_factory=list)
    user_id: Optional[str] = None
    document_length: Optional[int] = None
    batch_size: int = 1
    include_cloud_retriever: bool = False


class CostEstimateRequest(BaseModel):
    target_engine: str = Field(..., description="Engine ID to estimate cost for, e.g. LG01")
    query_text: str = Field(..., min_length=1, max_length=10000)
    mode: ResponseMode = ResponseMode.FAST
    user_id: Optional[str] = None
    document_length: Optional[int] = None
    batch_size: int = 1
    include_cloud_retriever: bool = False
    chain_engines: List[str] = Field(default_factory=list)


class BudgetCheckRequest(BaseModel):
    user_id: str
    estimated_cost_usd: float
    engine_id: Optional[str] = None


class AuthoritySource(BaseModel):
    source: str
    title: str
    weight: float = 1.0
    binding: bool = True


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[AuthoritySource]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_stratification: ConfidenceLevel
    controlling_precedent: str


class CostBreakdown(BaseModel):
    llm_input_tokens: int = 0
    llm_output_tokens: int = 0
    llm_cost_usd: float = 0.0
    api_calls: int = 0
    api_cost_usd: float = 0.0
    compute_ms: float = 0.0
    compute_cost_usd: float = 0.0
    storage_reads: int = 0
    storage_writes: int = 0
    storage_cost_usd: float = 0.0
    wall_clock_seconds: float = 0.0
    total_cost_usd: float = 0.0
    cache_discount_pct: float = 0.0
    mode_multiplier: float = 1.0
    batch_multiplier: float = 1.0
    chain_depth: int = 1
    confidence: float = 0.85


class BudgetStatus(BaseModel):
    user_id: str
    daily_limit_usd: float = 10.0
    monthly_limit_usd: float = 200.0
    daily_spent_usd: float = 0.0
    monthly_spent_usd: float = 0.0
    daily_remaining_usd: float = 10.0
    monthly_remaining_usd: float = 200.0
    alert_level: BudgetAlertLevel = BudgetAlertLevel.GREEN
    recommended_mode: ResponseMode = ResponseMode.FAST
    allow_query: bool = True


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    reasoning: str
    cost_breakdown: Optional[CostBreakdown] = None
    budget_status: Optional[BudgetStatus] = None
    confidence: float
    confidence_level: ConfidenceLevel
    authorities_cited: List[str] = Field(default_factory=list)
    categories_triggered: List[str] = Field(default_factory=list)
    determinism_hash: str
    timestamp: str
    latency_ms: float
    doctrine_cache_hit: bool = False
    fragility_score: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL PRICING TABLE — TIE Component 6 (semantic normalization data)
# ═══════════════════════════════════════════════════════════════════════════════

MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "claude-opus-4": {"input_per_1k": 0.015, "output_per_1k": 0.075},
    "claude-sonnet-4": {"input_per_1k": 0.003, "output_per_1k": 0.015},
    "claude-haiku-3.5": {"input_per_1k": 0.0008, "output_per_1k": 0.004},
    "gpt-4o": {"input_per_1k": 0.0025, "output_per_1k": 0.01},
    "gpt-4.1": {"input_per_1k": 0.002, "output_per_1k": 0.008},
    "gpt-4.1-mini": {"input_per_1k": 0.0004, "output_per_1k": 0.0016},
    "gpt-4.1-nano": {"input_per_1k": 0.0001, "output_per_1k": 0.0004},
    "groq-llama-70b": {"input_per_1k": 0.00059, "output_per_1k": 0.00079},
    "groq-llama-scout": {"input_per_1k": 0.00011, "output_per_1k": 0.00034},
    "deepseek-v3": {"input_per_1k": 0.00027, "output_per_1k": 0.0011},
    "deepseek-r1": {"input_per_1k": 0.00055, "output_per_1k": 0.00219},
    "openrouter-free": {"input_per_1k": 0.0, "output_per_1k": 0.0},
    "azure-free-tier": {"input_per_1k": 0.0, "output_per_1k": 0.0},
    "github-models-free": {"input_per_1k": 0.0, "output_per_1k": 0.0},
    "no-llm": {"input_per_1k": 0.0, "output_per_1k": 0.0},
}

# Per-engine cost profiles: avg tokens, compute, API calls, storage ops
ENGINE_COST_PROFILES: Dict[str, Dict[str, Any]] = {
    "TIE": {"input_tokens": 2200, "output_tokens": 3800, "compute_ms": 450, "api_calls": 0, "storage_reads": 4, "storage_writes": 1, "model": "no-llm", "description": "Tax Intelligence Engine (doctrine cache dominant)"},
    "PIE": {"input_tokens": 2500, "output_tokens": 4200, "compute_ms": 500, "api_calls": 0, "storage_reads": 5, "storage_writes": 1, "model": "no-llm", "description": "Policy Intelligence Engine"},
    "ARCS": {"input_tokens": 3000, "output_tokens": 5000, "compute_ms": 600, "api_calls": 0, "storage_reads": 6, "storage_writes": 2, "model": "no-llm", "description": "Advanced Regulatory Compliance System"},
    "LIE": {"input_tokens": 1800, "output_tokens": 3000, "compute_ms": 380, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Legal Intelligence Engine (backbone)"},
    "LMIE": {"input_tokens": 1600, "output_tokens": 2800, "compute_ms": 350, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Landman Intelligence Engine (backbone)"},
    "LG01": {"input_tokens": 1500, "output_tokens": 2500, "compute_ms": 300, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Contract Analysis"},
    "LG02": {"input_tokens": 1800, "output_tokens": 3200, "compute_ms": 380, "api_calls": 1, "storage_reads": 4, "storage_writes": 1, "model": "no-llm", "description": "Case Law Research"},
    "LG03": {"input_tokens": 1600, "output_tokens": 2800, "compute_ms": 320, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Regulatory Compliance"},
    "LG04": {"input_tokens": 2000, "output_tokens": 4000, "compute_ms": 420, "api_calls": 0, "storage_reads": 3, "storage_writes": 2, "model": "no-llm", "description": "Legal Document Draft"},
    "LG05": {"input_tokens": 1700, "output_tokens": 3000, "compute_ms": 350, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Litigation Risk"},
    "LG06": {"input_tokens": 1500, "output_tokens": 2600, "compute_ms": 310, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "IP Analysis"},
    "LG07": {"input_tokens": 1400, "output_tokens": 2400, "compute_ms": 290, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Employment Law"},
    "LG08": {"input_tokens": 1600, "output_tokens": 2800, "compute_ms": 320, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Real Estate Law"},
    "LM01": {"input_tokens": 1400, "output_tokens": 2200, "compute_ms": 280, "api_calls": 1, "storage_reads": 5, "storage_writes": 1, "model": "no-llm", "description": "Title Examination"},
    "LM02": {"input_tokens": 1500, "output_tokens": 2500, "compute_ms": 300, "api_calls": 1, "storage_reads": 5, "storage_writes": 1, "model": "no-llm", "description": "Lease Analysis"},
    "LM05": {"input_tokens": 1800, "output_tokens": 3500, "compute_ms": 400, "api_calls": 2, "storage_reads": 8, "storage_writes": 2, "model": "no-llm", "description": "Chain of Title"},
    "TX01": {"input_tokens": 2000, "output_tokens": 3500, "compute_ms": 400, "api_calls": 0, "storage_reads": 4, "storage_writes": 1, "model": "no-llm", "description": "Individual Income Tax"},
    "TX11": {"input_tokens": 1800, "output_tokens": 3200, "compute_ms": 380, "api_calls": 0, "storage_reads": 4, "storage_writes": 1, "model": "no-llm", "description": "Nonprofit Tax"},
    "TX12": {"input_tokens": 2200, "output_tokens": 3800, "compute_ms": 450, "api_calls": 0, "storage_reads": 5, "storage_writes": 1, "model": "no-llm", "description": "Oil & Gas Tax"},
    "TX14": {"input_tokens": 2000, "output_tokens": 3500, "compute_ms": 420, "api_calls": 0, "storage_reads": 4, "storage_writes": 1, "model": "no-llm", "description": "Crypto Tax"},
    "E01": {"input_tokens": 1200, "output_tokens": 2000, "compute_ms": 250, "api_calls": 0, "storage_reads": 2, "storage_writes": 1, "model": "no-llm", "description": "Document Classifier / CRM Analytics"},
    "E02": {"input_tokens": 1800, "output_tokens": 3000, "compute_ms": 350, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Summary Generator"},
    "E03": {"input_tokens": 1600, "output_tokens": 2800, "compute_ms": 320, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Comparison Analyzer"},
    "E04": {"input_tokens": 2000, "output_tokens": 3500, "compute_ms": 400, "api_calls": 1, "storage_reads": 4, "storage_writes": 2, "model": "no-llm", "description": "Financial Reporting"},
    "E05": {"input_tokens": 2500, "output_tokens": 4000, "compute_ms": 500, "api_calls": 3, "storage_reads": 8, "storage_writes": 2, "model": "no-llm", "description": "Due Diligence Aggregator"},
    "E06": {"input_tokens": 1800, "output_tokens": 3200, "compute_ms": 380, "api_calls": 1, "storage_reads": 5, "storage_writes": 2, "model": "no-llm", "description": "Business Intelligence / Report Generator"},
    "E07": {"input_tokens": 1400, "output_tokens": 2200, "compute_ms": 280, "api_calls": 0, "storage_reads": 3, "storage_writes": 1, "model": "no-llm", "description": "Query Interpreter"},
    "E08": {"input_tokens": 1200, "output_tokens": 1800, "compute_ms": 220, "api_calls": 0, "storage_reads": 2, "storage_writes": 1, "model": "no-llm", "description": "Alert Generator"},
    "E09": {"input_tokens": 2000, "output_tokens": 3000, "compute_ms": 350, "api_calls": 0, "storage_reads": 4, "storage_writes": 2, "model": "no-llm", "description": "Batch Processor"},
    "E10": {"input_tokens": 800, "output_tokens": 1200, "compute_ms": 150, "api_calls": 0, "storage_reads": 2, "storage_writes": 1, "model": "no-llm", "description": "Cost Estimator (self)"},
    "SHADOWGLASS": {"input_tokens": 0, "output_tokens": 0, "compute_ms": 800, "api_calls": 5, "storage_reads": 10, "storage_writes": 5, "model": "no-llm", "description": "County record scraping"},
    "CLOUD_RETRIEVER": {"input_tokens": 500, "output_tokens": 800, "compute_ms": 200, "api_calls": 8, "storage_reads": 8, "storage_writes": 0, "model": "no-llm", "description": "8-source cloud knowledge retriever"},
    "BREE_CHAT": {"input_tokens": 1500, "output_tokens": 2000, "compute_ms": 100, "api_calls": 1, "storage_reads": 3, "storage_writes": 2, "model": "openrouter-free", "description": "Bree conversational AI"},
    "SENTINEL": {"input_tokens": 1500, "output_tokens": 2000, "compute_ms": 100, "api_calls": 1, "storage_reads": 3, "storage_writes": 2, "model": "openrouter-free", "description": "Sentinel memory agent"},
}

CLOUD_SERVICE_COSTS: Dict[str, float] = {
    "r2_class_a_per_1k": 0.0045,
    "r2_class_b_per_1k": 0.00036,
    "d1_read_per_million": 0.001,
    "d1_write_per_million": 1.0,
    "worker_request": 0.0,
    "vectorize_query_per_1k": 0.01,
    "kv_read_per_million": 0.50,
    "kv_write_per_million": 5.0,
    "compute_per_cpu_ms": 0.0000125,
}

MODE_MULTIPLIERS: Dict[ResponseMode, float] = {
    ResponseMode.FAST: 1.0,
    ResponseMode.DEFENSE: 1.8,
    ResponseMode.MEMO: 2.5,
}

CACHE_DISCOUNT_FACTOR = 0.15


# ═══════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE — TIE Component 3 (30+ cost estimation rules)
# ═══════════════════════════════════════════════════════════════════════════════

def _build_doctrine_cache() -> Dict[str, DoctrineBlock]:
    blocks: Dict[str, DoctrineBlock] = {}

    blocks["llm_token_pricing"] = DoctrineBlock(
        topic="LLM Token Cost Estimation",
        keywords=["token", "cost", "llm", "pricing", "model", "input", "output"],
        conclusion_template="Estimated LLM token cost for {model} is ${cost:.6f} based on {input_tokens} input and {output_tokens} output tokens at current per-1K rates.",
        reasoning_framework=(
            "Token cost is the product of token count and per-token price for the selected model. "
            "Input tokens include the system prompt, doctrine context, user query, and any injected "
            "memory or retriever results. Output tokens scale with response mode: FAST produces ~60% "
            "of baseline output, DEFENSE ~100%, and MEMO ~150%. Models on free tiers (Azure free, "
            "GitHub Models, OpenRouter free) have zero token cost but may have rate limits. When "
            "estimating, always account for the system prompt overhead which is typically 800-1200 "
            "tokens for TIE-pattern engines. Document length directly increases input tokens: "
            "assume ~1 token per 4 characters of English text. Cache hits eliminate LLM calls "
            "entirely, reducing token cost to zero for doctrine-cached responses."
        ),
        key_factors=["model_selection", "input_token_count", "output_token_count", "mode_multiplier", "cache_hit_rate", "system_prompt_overhead"],
        primary_authority=[
            AuthoritySource(source="Anthropic Pricing", title="Claude API Pricing 2026", weight=1.0),
            AuthoritySource(source="OpenAI Pricing", title="GPT-4 API Pricing 2026", weight=0.9),
            AuthoritySource(source="Groq Pricing", title="Groq Inference Pricing", weight=0.8),
        ],
        burden_holder="cost_estimator",
        adversary_position="Actual costs may vary due to tokenizer differences, prompt caching, and batch discounts.",
        counter_arguments=["Tokenizer variance across models causes 5-15% estimation error", "Prompt caching can reduce effective cost by 50-90%", "Batch API pricing differs from real-time pricing", "Free tier limits may force fallback to paid models", "Token counts depend on language and domain vocabulary density"],
        resolution_strategy="Use conservative estimates with model-specific tokenizer ratios. Apply a 1.1x safety margin on all token estimates. Track actuals vs estimates to calibrate over time.",
        entity_scope="all_engines",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Historical query telemetry from TIE, PIE, ARCS backbones"
    )

    blocks["api_call_costing"] = DoctrineBlock(
        topic="External API Call Cost Estimation",
        keywords=["api", "call", "external", "service", "request", "rate", "limit"],
        conclusion_template="Estimated {api_calls} external API calls costing ${api_cost:.6f} for the {engine_id} engine query.",
        reasoning_framework=(
            "External API costs include county record lookups (ShadowGlass), RRC production data, "
            "cloud retriever queries (8 parallel sources), and third-party enrichment services. "
            "Most engines in the fleet are doctrine-cache-first and make zero external API calls "
            "for cached topics. LM-series engines (Landman) make 1-2 county API calls on average. "
            "E05 Due Diligence makes up to 3 external calls per query. ShadowGlass scraping "
            "operations can trigger 5+ external requests per county lookup. Cloud Retriever always "
            "makes 8 parallel requests (EKM, Graph, Crystal, Engine Matrix, Embedding, Knowledge "
            "Forge, Shared Brain, Memory Prime) but all are internal Cloudflare Workers with zero "
            "monetary cost — only wall-clock time. When batching, API calls scale linearly unless "
            "the target API supports bulk endpoints."
        ),
        key_factors=["engine_type", "query_complexity", "external_service_count", "batch_size", "cache_availability"],
        primary_authority=[
            AuthoritySource(source="Cloudflare Workers", title="Workers Free Tier: 100K req/day", weight=1.0),
            AuthoritySource(source="ECHO Fleet Telemetry", title="Historical API call data", weight=0.9),
        ],
        burden_holder="cost_estimator",
        adversary_position="Internal Worker-to-Worker calls are free but consume CPU time and add latency.",
        counter_arguments=["Rate limits may force request queuing, increasing wall-clock cost", "Failed API calls still consume compute but produce no value", "Retry logic doubles effective API call count on failures", "Geographic routing adds variable latency", "Cold start on Workers adds 20-50ms per invocation"],
        resolution_strategy="Separate internal (free, latency-only) from external (paid) API calls. Track failure rates to inflate estimates appropriately.",
        entity_scope="all_engines",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ECHO fleet API call telemetry (2026-01 through 2026-02)"
    )

    blocks["compute_cost_estimation"] = DoctrineBlock(
        topic="CPU Compute Cost Estimation",
        keywords=["compute", "cpu", "processing", "time", "milliseconds", "performance"],
        conclusion_template="Estimated compute cost of {compute_ms}ms (${compute_cost:.8f}) for {engine_id} in {mode} mode.",
        reasoning_framework=(
            "Compute cost is measured in CPU-milliseconds consumed by the engine processing pipeline. "
            "TIE-pattern engines have a three-layer response architecture: Layer 1 (doctrine cache) "
            "is 5-50ms, Layer 2 (semantic retrieval) is 50-200ms, Layer 3 (deep analysis) is "
            "200-800ms. FAST mode typically resolves at Layer 1-2, DEFENSE at Layer 2-3, and MEMO "
            "always hits Layer 3. Backbone engines (TIE, PIE, ARCS) have larger doctrine caches and "
            "more complex processing, averaging 400-600ms. Smaller engines average 250-350ms. "
            "Cloudflare Workers pricing is $0.0000125 per CPU-ms after free tier (10ms per request). "
            "Local execution on the i7-6700K has no direct monetary cost but competes for resources "
            "with other fleet instances. Batch processing amortizes startup cost but scales linearly "
            "for per-item processing."
        ),
        key_factors=["engine_complexity", "response_mode", "doctrine_cache_size", "query_complexity", "batch_size"],
        primary_authority=[
            AuthoritySource(source="Cloudflare Workers", title="Workers CPU pricing model", weight=1.0),
            AuthoritySource(source="ECHO Telemetry", title="Engine latency percentiles (p50, p95, p99)", weight=0.95),
        ],
        burden_holder="cost_estimator",
        adversary_position="Local execution has zero monetary compute cost, making cloud comparison misleading.",
        counter_arguments=["Local CPU contention varies with fleet size", "Cold starts add 50-200ms not captured in steady-state profiles", "Vector search operations are GPU-accelerable but CPU-bound locally", "Python GIL limits true parallelism for CPU-bound work", "Memory pressure from 5+ Claude instances degrades performance"],
        resolution_strategy="Report both monetary cost (for cloud budgeting) and resource cost (for local scheduling). Use historical p50 as baseline with p95 as worst-case.",
        entity_scope="all_engines",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Resource monitor snapshots and engine telemetry data"
    )

    blocks["storage_cost_estimation"] = DoctrineBlock(
        topic="Storage Operation Cost Estimation",
        keywords=["storage", "r2", "d1", "kv", "read", "write", "database"],
        conclusion_template="Estimated {reads} reads and {writes} writes costing ${storage_cost:.8f} across R2/D1/KV for {engine_id}.",
        reasoning_framework=(
            "Storage costs come from three Cloudflare primitives: R2 (object storage), D1 (SQLite), "
            "and KV (key-value cache). R2 Class A (write/list) operations cost $0.0045 per 1K ops, "
            "Class B (read) $0.00036 per 1K. D1 reads are $0.001 per million rows, writes $1.00 per "
            "million rows. KV reads are $0.50 per million, writes $5.00 per million. Most engine "
            "queries perform 2-5 reads (doctrine lookup, config, cached results) and 1-2 writes "
            "(audit log, telemetry). ShadowGlass operations are storage-heavy: 10 reads + 5 writes "
            "per scrape batch. The audit trail (JSONL) write is mandatory for every query across all "
            "engines. On Cloudflare free tier, first 10M reads and 1M writes per month are free. "
            "Given current fleet volume (~50K queries/month), storage costs are effectively zero."
        ),
        key_factors=["operation_type", "read_count", "write_count", "free_tier_remaining", "data_size_per_op"],
        primary_authority=[
            AuthoritySource(source="Cloudflare R2", title="R2 Pricing", weight=1.0),
            AuthoritySource(source="Cloudflare D1", title="D1 Pricing", weight=1.0),
            AuthoritySource(source="Cloudflare KV", title="Workers KV Pricing", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Free tier covers current usage. Storage cost is effectively zero but should be tracked for scale planning.",
        counter_arguments=["Storage costs become significant at 1M+ queries/month", "Large document storage in R2 has egress costs outside Cloudflare", "D1 write costs spike with high audit trail volume", "KV storage is priced per GB stored (not just ops)", "Cross-region replication adds hidden storage costs"],
        resolution_strategy="Track operations even at zero cost to project future spending. Alert when approaching free tier thresholds.",
        entity_scope="all_engines",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Cloudflare billing dashboard and usage analytics"
    )

    blocks["wall_clock_estimation"] = DoctrineBlock(
        topic="Wall-Clock Time Estimation",
        keywords=["time", "latency", "duration", "wall", "clock", "seconds", "speed"],
        conclusion_template="Estimated wall-clock time of {wall_time:.2f}s for {engine_id} query in {mode} mode.",
        reasoning_framework=(
            "Wall-clock time is the user-perceived duration from query submission to response delivery. "
            "It includes: network round-trip (5-50ms), engine startup/routing (10-30ms), doctrine "
            "cache lookup (5-50ms), optional semantic retrieval (50-200ms), optional deep analysis "
            "(200-800ms), optional LLM inference (500-5000ms), and response serialization (5-20ms). "
            "FAST mode targets sub-500ms by resolving at doctrine cache layer. DEFENSE mode allows "
            "up to 2s for semantic retrieval and cross-referencing. MEMO mode allows up to 5s for "
            "full deep analysis with LLM augmentation. Cloud Retriever adds 200-1500ms depending "
            "on source availability. Chain queries multiply wall time by chain depth with some "
            "parallelization benefit (~0.7x factor for parallel-eligible chains). Batch queries "
            "scale sub-linearly due to connection reuse and cache warming."
        ),
        key_factors=["response_mode", "chain_depth", "cloud_retriever_enabled", "llm_inference_needed", "network_conditions"],
        primary_authority=[
            AuthoritySource(source="ECHO Telemetry", title="Engine latency percentiles", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Wall-clock estimates are inherently variable due to network conditions, system load, and cache state.",
        counter_arguments=["Cold starts add 200ms+ for Workers", "LLM inference time varies 2-10x based on output length", "Network congestion can double round-trip times", "Concurrent queries on local fleet degrade latency", "Cache misses can 10x the expected time"],
        resolution_strategy="Report p50 estimate with p95 upper bound. Flag high-variance operations. Recommend FAST mode when time-sensitive.",
        entity_scope="all_engines",
        confidence=0.75,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Historical engine latency data from telemetry collectors"
    )

    blocks["budget_enforcement_daily"] = DoctrineBlock(
        topic="Daily Budget Enforcement",
        keywords=["budget", "daily", "limit", "spend", "cap", "threshold", "enforcement"],
        conclusion_template="User {user_id} has spent ${daily_spent:.4f} of ${daily_limit:.2f} daily budget ({pct:.1f}%). Alert level: {alert_level}.",
        reasoning_framework=(
            "Daily budgets prevent runaway costs from automated or high-frequency query patterns. "
            "Default daily limit is $10.00 per user, configurable per user tier. Budget checkpoints "
            "fire at 50% (YELLOW), 75% (ORANGE), 90% (RED), and 100% (CRITICAL). At CRITICAL, "
            "queries are blocked unless the user has override authority. Between ORANGE and CRITICAL, "
            "automatic mode degradation occurs: queries default to FAST mode and LLM inference is "
            "disabled in favor of doctrine-cache-only responses. Budget resets at midnight UTC. "
            "Cost tracking is approximate (based on estimates, not actuals) with reconciliation "
            "at end of day. Over-budget queries in progress are allowed to complete but the next "
            "query is blocked. Admin users (Commander authority) bypass all budget limits."
        ),
        key_factors=["daily_limit", "current_spend", "user_tier", "time_of_day", "query_frequency"],
        primary_authority=[
            AuthoritySource(source="ECHO Policy", title="Budget Enforcement Policy v1.0", weight=1.0),
        ],
        burden_holder="user",
        adversary_position="Budget limits may block critical queries. Emergency override exists for Commander authority.",
        counter_arguments=["Estimates may undercount, causing surprise budget exhaustion", "Free tier usage should not count against budget", "Batch queries can exhaust budget in a single call", "Budget limits discourage exploration and testing", "Time-zone differences affect daily reset timing"],
        resolution_strategy="Track estimated costs conservatively. Provide clear budget status in every response. Offer mode downgrade before hard block.",
        entity_scope="per_user",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ECHO OMEGA PRIME operational policy"
    )

    blocks["budget_enforcement_monthly"] = DoctrineBlock(
        topic="Monthly Budget Enforcement",
        keywords=["budget", "monthly", "limit", "spend", "billing", "cycle"],
        conclusion_template="User {user_id} has spent ${monthly_spent:.4f} of ${monthly_limit:.2f} monthly budget ({pct:.1f}%). Alert: {alert_level}.",
        reasoning_framework=(
            "Monthly budgets provide a macro-level spending cap that accounts for usage patterns "
            "over a billing cycle. Default is $200/month per user. Monthly budget uses the same "
            "alert thresholds as daily (50/75/90/100%) but with softer enforcement: at CRITICAL "
            "monthly, queries degrade to FAST+no-LLM mode instead of hard block. Monthly reset "
            "occurs on the 1st of each month at 00:00 UTC. Historical monthly spend is preserved "
            "for trend analysis and budget planning. Projected monthly spend is calculated from "
            "current daily run rate extrapolated to month end."
        ),
        key_factors=["monthly_limit", "current_spend", "days_remaining", "daily_run_rate", "projected_total"],
        primary_authority=[
            AuthoritySource(source="ECHO Policy", title="Budget Enforcement Policy v1.0", weight=1.0),
        ],
        burden_holder="user",
        adversary_position="Monthly limits may be too restrictive for burst usage patterns.",
        counter_arguments=["Monthly projection assumes linear spend which may not match reality", "Seasonal patterns affect monthly usage", "New engine deployments cause spend spikes", "Free tier renewals mid-month create accounting complexity"],
        resolution_strategy="Track actual + projected spend. Alert on trend changes, not just thresholds. Allow Commander override.",
        entity_scope="per_user",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ECHO OMEGA PRIME operational policy"
    )

    blocks["mode_cost_factor"] = DoctrineBlock(
        topic="Response Mode Cost Multiplier",
        keywords=["mode", "fast", "defense", "memo", "multiplier", "factor"],
        conclusion_template="{mode} mode applies a {multiplier}x cost multiplier to base engine estimates.",
        reasoning_framework=(
            "Response mode directly impacts cost through three mechanisms: (1) processing depth — "
            "FAST stops at doctrine cache, DEFENSE adds semantic retrieval, MEMO adds deep analysis; "
            "(2) output length — FAST produces concise answers (~60% of baseline tokens), DEFENSE "
            "produces full answers with citations (~100%), MEMO produces comprehensive documentation "
            "with full reasoning chains (~150%); (3) validation layers — DEFENSE adds authority "
            "cross-referencing, MEMO adds adversarial review and counter-argument analysis. The "
            "combined effect is a multiplicative cost factor: FAST=1.0x, DEFENSE=1.8x, MEMO=2.5x. "
            "These multipliers apply to compute time, output tokens, and wall-clock time. Input "
            "tokens are less affected (only MEMO significantly increases input via additional "
            "context injection)."
        ),
        key_factors=["selected_mode", "engine_type", "query_complexity", "output_length_target"],
        primary_authority=[
            AuthoritySource(source="TIE Architecture", title="Three-Layer Response Design", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="FAST mode sacrifices thoroughness for cost savings. Users should understand the tradeoff.",
        counter_arguments=["Doctrine cache hits make all modes equally cheap for cached topics", "Complex queries may need DEFENSE/MEMO regardless of budget", "Mode downgrade can produce incorrect or incomplete answers", "Some engines have flat cost regardless of mode", "User expectations differ by mode selection"],
        resolution_strategy="Report cost per mode so users can make informed choices. Auto-downgrade only when budget requires it, with clear disclosure.",
        entity_scope="all_engines",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TIE three-layer response architecture specification"
    )

    blocks["chain_depth_cost"] = DoctrineBlock(
        topic="Multi-Engine Chain Cost Estimation",
        keywords=["chain", "multi", "engine", "pipeline", "depth", "cascade"],
        conclusion_template="Chain of {depth} engines estimated at ${total:.6f} total with {parallel_benefit}% parallelization benefit.",
        reasoning_framework=(
            "Multi-engine chains occur when a query routes through multiple engines sequentially or "
            "in parallel. Sequential chains multiply wall-clock time by depth (e.g., LM01 -> LM05 -> "
            "TX12 = 3 engines). Parallel chains reduce wall-clock time to the slowest engine in each "
            "parallel group. Monetary cost always sums regardless of parallelization. Inter-engine "
            "communication adds ~20ms per hop for local engines, ~100ms for cloud Workers. Data "
            "passed between engines increases subsequent input token counts by 200-500 tokens per "
            "hop. The cost estimator should calculate both sequential worst-case and parallel "
            "best-case scenarios. Chain depth beyond 4 engines is rare and may indicate suboptimal "
            "query routing."
        ),
        key_factors=["chain_depth", "engine_list", "parallelizable_groups", "inter_engine_data_size", "total_monetary_cost"],
        primary_authority=[
            AuthoritySource(source="ECHO Engine Matrix", title="Engine dependency graph", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Chain cost estimation compounds errors from individual engine estimates.",
        counter_arguments=["Sequential chains may short-circuit if early engine resolves query", "Parallel execution depends on available CPU threads", "Cache hits in chain reduce downstream costs", "Error in any chain link wastes all upstream cost", "Chain depth increases estimation uncertainty multiplicatively"],
        resolution_strategy="Report per-engine costs individually plus chain total. Flag chains deeper than 3 as high-variance estimates. Apply 1.15x safety margin per hop.",
        entity_scope="multi_engine",
        confidence=0.78,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="ECHO engine routing telemetry"
    )

    blocks["batch_cost_estimation"] = DoctrineBlock(
        topic="Batch Query Cost Estimation",
        keywords=["batch", "bulk", "multiple", "items", "parallel", "throughput"],
        conclusion_template="Batch of {batch_size} items estimated at ${batch_cost:.6f} total (${per_item:.6f}/item, {discount:.1f}% batch discount).",
        reasoning_framework=(
            "Batch queries process N items through the same engine in a single request. Cost scales "
            "sub-linearly due to amortized startup, connection reuse, and cache warming effects. "
            "The batch discount formula is: total_cost = per_item_cost * N * (1 - batch_discount) "
            "where batch_discount = min(0.3, 0.02 * log2(N)). For example, a batch of 64 items "
            "gets ~12% discount, and a batch of 1024 items gets the max 30% discount. Compute cost "
            "scales linearly minus startup amortization. Token cost scales linearly (no discount). "
            "Wall-clock time scales at ~0.8x per doubling of batch size due to parallelism. "
            "Storage writes scale linearly (each item gets audit trail entry)."
        ),
        key_factors=["batch_size", "per_item_cost", "parallelism_factor", "cache_warming_benefit", "memory_pressure"],
        primary_authority=[
            AuthoritySource(source="ECHO Batch Processing", title="Batch Engine Architecture", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Batch discounts may not apply if items are diverse (no cache warming benefit).",
        counter_arguments=["Memory pressure from large batches degrades performance", "Batch failures may require full re-processing", "Diverse batch items negate cache warming", "Rate limits may throttle batch throughput", "Large batches compete for resources with other fleet queries"],
        resolution_strategy="Apply batch discount only for homogeneous items. Report per-item and total costs. Warn if batch size exceeds recommended maximum (1000 items).",
        entity_scope="all_engines",
        confidence=0.83,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="E09 Batch Processor telemetry data"
    )

    blocks["cache_discount_doctrine"] = DoctrineBlock(
        topic="Doctrine Cache Hit Cost Reduction",
        keywords=["cache", "hit", "discount", "doctrine", "cached", "pre-computed"],
        conclusion_template="Doctrine cache hit reduces cost by {discount_pct:.0f}% — estimated ${cached_cost:.6f} vs ${uncached_cost:.6f} without cache.",
        reasoning_framework=(
            "The doctrine cache is the primary cost reducer in TIE-pattern engines. When a query "
            "matches a cached doctrine block (by keyword overlap), the engine returns a pre-compiled "
            "response in 5-50ms with zero LLM inference cost. Cache hit rate across the fleet "
            "averages 65-85% for domain-specific queries. Cache misses fall through to semantic "
            "retrieval (Layer 2) or deep analysis (Layer 3), both of which are significantly more "
            "expensive. The cost discount for a cache hit is 85% — only residual compute for "
            "template rendering and audit logging remains. Backbone engines (TIE: 92 doctrines, "
            "PIE: 80+, ARCS: 100+) have the highest cache hit rates. Newer engines with fewer "
            "doctrines have lower hit rates. The cost estimator predicts cache hit probability "
            "based on query keyword overlap with known doctrine topics."
        ),
        key_factors=["query_keywords", "doctrine_coverage", "engine_doctrine_count", "historical_hit_rate"],
        primary_authority=[
            AuthoritySource(source="TIE Architecture", title="Doctrine Cache Design", weight=1.0),
            AuthoritySource(source="ECHO Telemetry", title="Cache hit rate data", weight=0.95),
        ],
        burden_holder="cost_estimator",
        adversary_position="Cache hit prediction is probabilistic. Actual cache behavior depends on exact query phrasing.",
        counter_arguments=["Novel queries always miss cache", "Doctrine drift reduces cache accuracy over time", "Cache staleness may produce outdated answers", "Keyword matching is imprecise for cost prediction", "Adversarial queries can bypass cache intentionally"],
        resolution_strategy="Report both cached and uncached cost estimates. Use historical hit rate as probability weight for expected cost calculation.",
        entity_scope="all_engines",
        confidence=0.80,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="TIE doctrine cache telemetry (92 topics, 78% avg hit rate)"
    )

    blocks["document_length_factor"] = DoctrineBlock(
        topic="Document Length Cost Factor",
        keywords=["document", "length", "size", "characters", "tokens", "long"],
        conclusion_template="Document of {length} characters adds ~{extra_tokens} tokens to input cost (${extra_cost:.6f}).",
        reasoning_framework=(
            "When a query includes a document for analysis (contract review, deed parsing, tax form "
            "interpretation), the document text increases input token count proportionally. The "
            "conversion ratio is approximately 1 token per 4 English characters, or ~750 tokens per "
            "page. A standard legal document (10 pages) adds ~7,500 input tokens. A complex deed "
            "chain (50 pages) adds ~37,500 tokens. Documents exceeding the context window require "
            "chunking, which multiplies API calls. For doctrine-cache engines, document content is "
            "processed through the normalization layer before cache lookup, adding compute cost but "
            "potentially still hitting cache for the analysis type."
        ),
        key_factors=["document_char_count", "document_type", "chunking_needed", "context_window_limit"],
        primary_authority=[
            AuthoritySource(source="Token Estimation", title="Character-to-token ratios by language", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Tokenizer-specific ratios vary. Claude tokenizes differently than GPT.",
        counter_arguments=["Legal text has higher token density due to specialized vocabulary", "Tables and structured data tokenize inefficiently", "Unicode and special characters inflate token count", "Chunking adds inter-chunk overlap tokens (10-20%)", "Document preprocessing may reduce effective length"],
        resolution_strategy="Use 1 token per 3.5 characters as conservative estimate for legal/technical text. Flag documents over 50K tokens as requiring chunking with cost multiplier.",
        entity_scope="all_engines",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Tokenizer benchmarks across Claude, GPT, and Groq models"
    )

    blocks["query_complexity_scoring"] = DoctrineBlock(
        topic="Query Complexity Scoring for Cost",
        keywords=["complexity", "score", "simple", "complex", "multi-part", "analysis"],
        conclusion_template="Query scored at complexity {score}/10 — cost multiplier {multiplier:.2f}x applied.",
        reasoning_framework=(
            "Query complexity directly impacts processing cost through multiple mechanisms. "
            "Simple keyword queries (complexity 1-3) resolve at doctrine cache with minimal cost. "
            "Multi-part analytical queries (complexity 4-6) require semantic retrieval and structured "
            "reasoning. Complex synthesis queries (complexity 7-10) require deep analysis, multiple "
            "doctrine decomposition, and often LLM augmentation. Complexity is scored by: (1) query "
            "length — longer queries tend to be more complex; (2) question count — multiple questions "
            "in one query; (3) domain breadth — queries spanning multiple issue categories; "
            "(4) temporal scope — queries requiring historical analysis; (5) entity count — queries "
            "about multiple parties or entities. The complexity score maps to a cost multiplier "
            "from 1.0x (simple) to 3.0x (maximum complexity)."
        ),
        key_factors=["query_length", "question_count", "domain_breadth", "temporal_scope", "entity_count"],
        primary_authority=[
            AuthoritySource(source="ECHO Query Analysis", title="Query complexity classification model", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Complexity scoring is heuristic. Short queries can be deeply complex and vice versa.",
        counter_arguments=["Short cryptic queries may require extensive interpretation", "Well-phrased complex queries may resolve efficiently via cache", "Complexity scoring adds overhead to every estimation", "False high complexity inflates estimates unnecessarily", "Domain expertise reduces effective complexity"],
        resolution_strategy="Use multi-factor scoring with lightweight heuristics (no LLM call for complexity assessment). Weight historical accuracy of complexity predictions.",
        entity_scope="all_engines",
        confidence=0.76,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Query classification heuristics validated against TIE telemetry"
    )

    blocks["cloud_retriever_cost"] = DoctrineBlock(
        topic="Cloud Retriever Overhead Cost",
        keywords=["cloud", "retriever", "knowledge", "forge", "brain", "memory", "search"],
        conclusion_template="Cloud retriever adds {extra_ms}ms latency and ~{extra_tokens} tokens to input context at ${extra_cost:.6f}.",
        reasoning_framework=(
            "The CognitionCloudRetriever queries 8 parallel cloud sources: EKM, Graph Engine, "
            "Crystal Memory, Engine Matrix, Embedding Pipeline, Knowledge Forge, Shared Brain, and "
            "Memory Prime. Each source returns 0-5 relevant snippets, adding 100-500 tokens per "
            "source to the engine's input context. Total overhead is 200-1500ms wall-clock (race-to-"
            "first returns in ~200ms, full results in ~1500ms) and 500-2000 additional input tokens. "
            "Monetary cost is zero (all internal Workers on free tier) but the token inflation from "
            "retrieved context increases LLM inference cost if the downstream engine uses an LLM. "
            "For doctrine-cache-only engines, retrieved context is used only for cache miss fallback, "
            "so the cost impact depends on cache hit rate."
        ),
        key_factors=["sources_queried", "results_returned", "token_inflation", "latency_added", "cache_hit_rate_impact"],
        primary_authority=[
            AuthoritySource(source="Cloud Retriever", title="CognitionCloudRetriever architecture doc", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Cloud retriever is free in monetary terms but adds significant latency and token overhead.",
        counter_arguments=["Source failures reduce result quality without reducing latency", "Token inflation from irrelevant results wastes LLM capacity", "L1/L2 cache in retriever mitigates repeat query cost", "Network timeouts can add unpredictable latency", "Result quality varies by source and query type"],
        resolution_strategy="Include cloud retriever cost only when explicitly enabled. Report latency and token overhead separately from monetary cost.",
        entity_scope="all_engines",
        confidence=0.80,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Cloud retriever telemetry (8-source parallel search metrics)"
    )

    blocks["cost_aware_routing"] = DoctrineBlock(
        topic="Cost-Aware Engine Routing",
        keywords=["routing", "selection", "cheapest", "optimal", "alternative", "fallback"],
        conclusion_template="Optimal routing for '{query_type}': {recommended_engine} at ${cost:.6f} (vs ${alt_cost:.6f} for {alt_engine}).",
        reasoning_framework=(
            "When multiple engines can handle a query, cost-aware routing selects the cheapest "
            "option that meets quality requirements. For example, a basic tax question can route to "
            "TIE (highest quality, higher cost), TX01 (specialized, medium cost), or a free-tier "
            "LLM (lowest cost, lowest quality). The routing decision considers: (1) estimated cost "
            "per engine; (2) expected answer quality (based on engine domain match); (3) user budget "
            "remaining; (4) response time requirements. When budget is tight, routing favors "
            "doctrine-cache-heavy engines (zero LLM cost) over LLM-augmented engines. The cost "
            "estimator provides routing recommendations but does not enforce them — the query "
            "router makes the final decision."
        ),
        key_factors=["available_engines", "quality_requirement", "budget_remaining", "latency_requirement", "domain_match"],
        primary_authority=[
            AuthoritySource(source="ECHO Engine Matrix", title="Engine capability and cost matrix", weight=1.0),
        ],
        burden_holder="query_router",
        adversary_position="Cheapest routing may sacrifice answer quality. Users should be informed of the tradeoff.",
        counter_arguments=["Quality metrics are subjective and hard to quantify", "Engine availability changes dynamically", "Cache state varies, making cost estimates stale", "User preference should override cost optimization", "Some queries require specific engines regardless of cost"],
        resolution_strategy="Provide cost-ranked engine options with quality indicators. Let the routing layer or user choose. Default to best quality within budget.",
        entity_scope="fleet_wide",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Engine Matrix capability mapping and telemetry"
    )

    blocks["free_tier_tracking"] = DoctrineBlock(
        topic="Free Tier Usage Tracking",
        keywords=["free", "tier", "azure", "github", "openrouter", "zero", "cost"],
        conclusion_template="Free tier usage: {used}/{limit} ({pct:.1f}%). Estimated {days_remaining} days until exhaustion at current rate.",
        reasoning_framework=(
            "Multiple services offer free tiers that the fleet exploits: Azure OpenAI free tier "
            "(until May 2026), GitHub Models (rate-limited free access to GPT-4.1, Grok-3, Llama-4, "
            "etc.), OpenRouter free models (Llama-3.3-70b), Cloudflare Workers free tier (100K "
            "req/day, 10ms CPU per request), R2 free tier (10M reads/month, 1M writes/month), "
            "D1 free tier (5M reads/day, 100K writes/day), KV free tier (100K reads/day, 1K "
            "writes/day). Tracking free tier consumption is critical for budget accuracy — queries "
            "using free tier resources have zero monetary cost but still consume rate-limited "
            "capacity. The cost estimator tracks free tier utilization and projects exhaustion dates "
            "to warn before unexpected paid usage kicks in."
        ),
        key_factors=["service_name", "free_tier_limit", "current_usage", "daily_run_rate", "expiration_date"],
        primary_authority=[
            AuthoritySource(source="Azure", title="Azure Free Tier Terms", weight=1.0),
            AuthoritySource(source="Cloudflare", title="Workers Free Tier", weight=1.0),
            AuthoritySource(source="GitHub", title="GitHub Models Rate Limits", weight=0.9),
        ],
        burden_holder="cost_estimator",
        adversary_position="Free tiers can be revoked or modified without notice. Do not depend on them for critical operations.",
        counter_arguments=["Free tier limits change without warning", "Rate limits may throttle before hard limit", "Multi-account free tiers complicate tracking", "Hidden costs (egress, premium features) exist", "Free tier expiration dates may shift"],
        resolution_strategy="Track all free tier usage with conservative estimates. Alert at 80% utilization. Maintain fallback to paid services with budget allocation.",
        entity_scope="fleet_wide",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Azure billing dashboard, Cloudflare usage analytics"
    )

    blocks["mode_degradation"] = DoctrineBlock(
        topic="Automatic Mode Degradation Under Budget Pressure",
        keywords=["degrade", "downgrade", "mode", "automatic", "budget", "pressure", "fallback"],
        conclusion_template="Budget at {pct:.0f}% — auto-degrading from {original_mode} to {degraded_mode} (saves ${savings:.6f} per query).",
        reasoning_framework=(
            "When budget utilization exceeds thresholds, the system automatically degrades response "
            "mode to reduce cost. Degradation sequence: MEMO -> DEFENSE -> FAST -> FAST+no-LLM. "
            "At 75% daily budget: MEMO queries auto-downgrade to DEFENSE. At 90%: all queries "
            "downgrade to FAST. At 100%: queries run in FAST+no-LLM mode (doctrine cache only, "
            "zero LLM cost). The user is informed of the degradation in the response metadata. "
            "Commander-authority users are exempt from auto-degradation. The cost estimator reports "
            "the savings from degradation so users can understand the tradeoff. Manual mode override "
            "is available but counts against budget at full cost."
        ),
        key_factors=["current_budget_pct", "requested_mode", "degraded_mode", "cost_savings", "quality_impact"],
        primary_authority=[
            AuthoritySource(source="ECHO Policy", title="Budget Enforcement Policy v1.0", weight=1.0),
        ],
        burden_holder="system",
        adversary_position="Auto-degradation may surprise users who expect full-quality responses.",
        counter_arguments=["Degraded responses may be useless for complex queries", "Users may not notice degradation and trust incomplete answers", "Forced FAST mode for MEMO-worthy queries wastes user time", "Budget pressure from one user shouldn't affect others", "Degradation without clear UI indication is dangerous"],
        resolution_strategy="Always disclose degradation in response. Show original vs degraded mode and cost savings. Allow manual override with explicit budget consent.",
        entity_scope="per_user",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ECHO budget enforcement operational policy"
    )

    blocks["historical_cost_analysis"] = DoctrineBlock(
        topic="Historical Cost Analysis and Trend Detection",
        keywords=["history", "trend", "historical", "analysis", "spend", "pattern", "usage"],
        conclusion_template="User {user_id} 7-day trend: ${avg_daily:.4f}/day ({trend_direction}). Projected monthly: ${projected:.2f}.",
        reasoning_framework=(
            "Historical cost data enables trend detection and proactive budget management. The cost "
            "estimator maintains a rolling window of per-user, per-engine, and per-query-type cost "
            "records. Trend analysis detects: (1) spending spikes — sudden increase in query volume "
            "or cost per query; (2) engine preferences — which engines a user relies on most; "
            "(3) mode patterns — whether a user consistently requests expensive modes; (4) cache "
            "effectiveness — whether a user's query patterns benefit from caching; (5) budget "
            "pacing — whether spend is on track for monthly budget. Anomaly detection flags "
            "deviations >2 standard deviations from the user's historical mean."
        ),
        key_factors=["time_window", "data_points", "trend_direction", "anomaly_detection", "projected_spend"],
        primary_authority=[
            AuthoritySource(source="ECHO Telemetry", title="Historical cost tracking data", weight=1.0),
        ],
        burden_holder="cost_estimator",
        adversary_position="Historical data may not predict future costs, especially after fleet changes or new engine deployments.",
        counter_arguments=["Short history produces unreliable trends", "Fleet changes invalidate historical baselines", "User behavior changes over time", "Seasonal patterns require long-term data", "Aggregated trends hide per-query variance"],
        resolution_strategy="Require minimum 7 days of data for trend analysis. Weight recent data higher (exponential decay). Flag major fleet changes as trend-breaking events.",
        entity_scope="per_user",
        confidence=0.78,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Cost tracking data from E10 audit trail"
    )

    for i, eng_id in enumerate(["LG09", "LG10", "LG11", "LG12", "LG13", "LG14", "LG15", "LG16", "LG17", "LG18", "LM03", "LM04", "P01"]):
        blocks[f"engine_profile_{eng_id.lower()}"] = DoctrineBlock(
            topic=f"Cost Profile for Engine {eng_id}",
            keywords=[eng_id.lower(), "engine", "cost", "profile", "estimate"],
            conclusion_template=f"Engine {eng_id} estimated at ${{cost:.6f}} in {{mode}} mode ({{tokens}} tokens, {{compute_ms}}ms compute).",
            reasoning_framework=f"Engine {eng_id} cost profile derived from build telemetry and runtime sampling. Doctrine-cache engines average 280-400ms compute, 1400-2500 input tokens, 2200-3500 output tokens. Cache hit rate for {eng_id} estimated at 70-80% based on domain doctrine count. No external API calls for standard queries. Storage: 3 reads (config + doctrine + audit lookup), 1 write (audit trail).",
            key_factors=["input_tokens", "output_tokens", "compute_ms", "cache_hit_rate", "mode"],
            primary_authority=[AuthoritySource(source="ECHO Telemetry", title=f"{eng_id} runtime metrics", weight=0.9)],
            burden_holder="cost_estimator",
            adversary_position=f"Profile for {eng_id} based on limited runtime data. Actual costs may vary.",
            counter_arguments=["Limited telemetry data for newer engines", "Query distribution affects average cost", "Cache hit rate varies by query type"],
            resolution_strategy="Use conservative estimates. Update profile as more telemetry accumulates.",
            entity_scope="single_engine",
            confidence=0.80,
            confidence_stratification=ConfidenceLevel.DISCLOSURE,
            controlling_precedent=f"{eng_id} build and runtime telemetry"
        )

    return blocks


DOCTRINE_CACHE = _build_doctrine_cache()


# ═══════════════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION — TIE Component 6
# ═══════════════════════════════════════════════════════════════════════════════

TERM_NORMALIZATION: Dict[str, str] = {
    "token": "llm_token", "tokens": "llm_token", "llm": "llm_token",
    "api": "api_call", "endpoint": "api_call", "request": "api_call",
    "compute": "compute_cost", "cpu": "compute_cost", "processing": "compute_cost",
    "storage": "storage_cost", "r2": "storage_cost", "d1": "storage_cost", "kv": "storage_cost",
    "time": "wall_clock", "latency": "wall_clock", "duration": "wall_clock", "speed": "wall_clock",
    "budget": "budget_enforcement", "limit": "budget_enforcement", "cap": "budget_enforcement",
    "spend": "budget_enforcement", "spending": "budget_enforcement",
    "chain": "chain_cost", "pipeline": "chain_cost", "cascade": "chain_cost", "multi-engine": "chain_cost",
    "batch": "batch_cost", "bulk": "batch_cost",
    "cache": "cache_discount", "cached": "cache_discount", "doctrine": "cache_discount",
    "mode": "mode_factor", "fast": "mode_factor", "defense": "mode_factor", "memo": "mode_factor",
    "route": "routing_decision", "routing": "routing_decision", "cheapest": "routing_decision",
    "free": "free_tier", "azure": "free_tier", "github": "free_tier",
    "history": "historical_analysis", "trend": "historical_analysis", "pattern": "historical_analysis",
    "price": "llm_token", "pricing": "llm_token", "cost": "total_cost", "estimate": "total_cost",
    "dollar": "total_cost", "usd": "total_cost", "money": "total_cost",
}


def normalize_query(query: str) -> Tuple[str, List[str]]:
    """Normalize query terms and extract normalized keywords."""
    words = query.lower().split()
    normalized_terms: List[str] = []
    for word in words:
        clean = word.strip(".,?!;:'\"()[]{}").lower()
        if clean in TERM_NORMALIZATION:
            normalized_terms.append(TERM_NORMALIZATION[clean])
        elif clean:
            normalized_terms.append(clean)
    return " ".join(normalized_terms), list(set(normalized_terms))


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORITY HARDENING — TIE Component 4
# ═══════════════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY = [
    {"level": 1, "source": "Cloudflare Pricing", "weight": 1.0, "type": "official_pricing"},
    {"level": 2, "source": "ECHO Telemetry", "weight": 0.95, "type": "empirical_measurement"},
    {"level": 3, "source": "ECHO Policy", "weight": 0.90, "type": "internal_policy"},
    {"level": 4, "source": "Model Vendor Docs", "weight": 0.85, "type": "vendor_documentation"},
    {"level": 5, "source": "Historical Estimates", "weight": 0.75, "type": "statistical_projection"},
]


def resolve_authority_conflict(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """When multiple authorities conflict, higher-weight source wins."""
    if not sources:
        return {"resolution": "no_sources", "confidence": 0.5}
    sorted_sources = sorted(sources, key=lambda s: s.get("weight", 0), reverse=True)
    winner = sorted_sources[0]
    return {
        "resolution": f"Resolved by {winner['source']} (weight {winner['weight']})",
        "winning_source": winner["source"],
        "confidence": winner["weight"],
        "alternatives_considered": len(sources) - 1,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIDENCE STRATIFICATION — TIE Component 5
# ═══════════════════════════════════════════════════════════════════════════════

def stratify_confidence(base_confidence: float, factors: Dict[str, float]) -> Tuple[float, ConfidenceLevel]:
    """Apply confidence adjustments and classify into stratification level."""
    adjusted = base_confidence
    for factor_name, modifier in factors.items():
        adjusted *= modifier
    adjusted = max(0.1, min(1.0, adjusted))
    if adjusted >= 0.85:
        level = ConfidenceLevel.DEFENSIBLE
    elif adjusted >= 0.70:
        level = ConfidenceLevel.AGGRESSIVE
    elif adjusted >= 0.50:
        level = ConfidenceLevel.DISCLOSURE
    else:
        level = ConfidenceLevel.HIGH_RISK
    return adjusted, level


# ═══════════════════════════════════════════════════════════════════════════════
# COST ESTIMATION CORE — domain logic
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_query_complexity(query: str) -> Tuple[int, float]:
    """Score query complexity 1-10 and return cost multiplier."""
    score = 1
    length = len(query)
    if length > 500:
        score += 2
    elif length > 200:
        score += 1
    question_marks = query.count("?")
    if question_marks > 2:
        score += 2
    elif question_marks > 0:
        score += 1
    multi_keywords = ["and", "also", "additionally", "furthermore", "compare", "versus", "vs", "between"]
    for kw in multi_keywords:
        if kw in query.lower():
            score += 1
            break
    analysis_keywords = ["analyze", "analysis", "evaluate", "assess", "review", "comprehensive", "detailed", "full"]
    for kw in analysis_keywords:
        if kw in query.lower():
            score += 1
            break
    temporal_keywords = ["history", "historical", "trend", "over time", "year-over-year", "last year"]
    for kw in temporal_keywords:
        if kw in query.lower():
            score += 1
            break
    score = min(10, score)
    multiplier = 1.0 + (score - 1) * 0.22
    return score, multiplier


def estimate_cache_hit_probability(query: str, engine_id: str) -> float:
    """Predict cache hit probability based on query keywords and engine doctrine density."""
    profile = ENGINE_COST_PROFILES.get(engine_id, {})
    base_hit_rate = 0.70
    backbone_engines = {"TIE", "PIE", "ARCS", "LIE", "LMIE"}
    if engine_id in backbone_engines:
        base_hit_rate = 0.82
    query_lower = query.lower()
    domain_match_terms = 0
    for block in DOCTRINE_CACHE.values():
        for kw in block.keywords:
            if kw in query_lower:
                domain_match_terms += 1
                break
    if domain_match_terms >= 3:
        base_hit_rate = min(0.95, base_hit_rate + 0.10)
    elif domain_match_terms == 0:
        base_hit_rate = max(0.20, base_hit_rate - 0.30)
    return base_hit_rate


def calculate_cost_breakdown(
    engine_id: str,
    query: str,
    mode: ResponseMode,
    document_length: Optional[int] = None,
    batch_size: int = 1,
    include_cloud_retriever: bool = False,
    chain_engines: Optional[List[str]] = None,
) -> CostBreakdown:
    """Calculate full cost breakdown for a query."""
    profile = ENGINE_COST_PROFILES.get(engine_id, ENGINE_COST_PROFILES.get("E10", {}))
    mode_mult = MODE_MULTIPLIERS.get(mode, 1.0)
    complexity_score, complexity_mult = estimate_query_complexity(query)
    cache_hit_prob = estimate_cache_hit_probability(query, engine_id)

    input_tokens = int(profile.get("input_tokens", 1000) * complexity_mult)
    output_tokens = int(profile.get("output_tokens", 1500) * mode_mult)
    if document_length and document_length > 0:
        doc_tokens = int(document_length / 3.5)
        input_tokens += doc_tokens
    model_name = profile.get("model", "no-llm")
    pricing = MODEL_PRICING.get(model_name, MODEL_PRICING["no-llm"])
    llm_cost = (input_tokens / 1000 * pricing["input_per_1k"]) + (output_tokens / 1000 * pricing["output_per_1k"])
    effective_llm_cost = llm_cost * (1 - cache_hit_prob * 0.85)

    api_calls = profile.get("api_calls", 0)
    api_cost = api_calls * 0.0001

    compute_ms = profile.get("compute_ms", 200) * mode_mult * complexity_mult
    compute_cost = max(0, (compute_ms - 10)) * CLOUD_SERVICE_COSTS["compute_per_cpu_ms"]

    storage_reads = profile.get("storage_reads", 2)
    storage_writes = profile.get("storage_writes", 1)
    storage_cost = (
        (storage_reads / 1000) * CLOUD_SERVICE_COSTS["r2_class_b_per_1k"]
        + (storage_writes / 1000) * CLOUD_SERVICE_COSTS["r2_class_a_per_1k"]
    )

    cr_tokens = 0
    cr_ms = 0.0
    if include_cloud_retriever:
        cr_profile = ENGINE_COST_PROFILES["CLOUD_RETRIEVER"]
        cr_tokens = cr_profile["input_tokens"]
        input_tokens += cr_tokens
        cr_ms = cr_profile["compute_ms"]
        api_calls += cr_profile["api_calls"]
        storage_reads += cr_profile["storage_reads"]

    wall_clock = compute_ms / 1000
    if include_cloud_retriever:
        wall_clock += cr_ms / 1000
    if model_name != "no-llm":
        wall_clock += 1.5 * mode_mult

    chain_depth = 1
    chain_total_add = 0.0
    if chain_engines:
        chain_depth = len(chain_engines) + 1
        for ce_id in chain_engines:
            ce_profile = ENGINE_COST_PROFILES.get(ce_id, ENGINE_COST_PROFILES["E10"])
            ce_compute = ce_profile.get("compute_ms", 200) * mode_mult
            ce_tokens_in = ce_profile.get("input_tokens", 1000)
            ce_tokens_out = ce_profile.get("output_tokens", 1500) * mode_mult
            ce_model = ce_profile.get("model", "no-llm")
            ce_pricing = MODEL_PRICING.get(ce_model, MODEL_PRICING["no-llm"])
            ce_llm_cost = (ce_tokens_in / 1000 * ce_pricing["input_per_1k"]) + (ce_tokens_out / 1000 * ce_pricing["output_per_1k"])
            chain_total_add += ce_llm_cost + (ce_compute - 10) * CLOUD_SERVICE_COSTS["compute_per_cpu_ms"]
            wall_clock += ce_compute / 1000 * 0.7
            input_tokens += 300
        wall_clock += chain_depth * 0.02

    batch_discount = 0.0
    batch_mult = 1.0
    if batch_size > 1:
        batch_discount = min(0.30, 0.02 * math.log2(max(2, batch_size)))
        batch_mult = batch_size * (1.0 - batch_discount)
    else:
        batch_mult = 1.0

    total_cost = (effective_llm_cost + api_cost + compute_cost + storage_cost + chain_total_add) * max(1.0, batch_mult)

    return CostBreakdown(
        llm_input_tokens=int(input_tokens * max(1, batch_size)),
        llm_output_tokens=int(output_tokens * max(1, batch_size)),
        llm_cost_usd=round(effective_llm_cost * max(1.0, batch_mult), 8),
        api_calls=int(api_calls * max(1, batch_size)),
        api_cost_usd=round(api_cost * max(1.0, batch_mult), 8),
        compute_ms=round(compute_ms * max(1.0, batch_mult), 2),
        compute_cost_usd=round(compute_cost * max(1.0, batch_mult), 8),
        storage_reads=int(storage_reads * max(1, batch_size)),
        storage_writes=int(storage_writes * max(1, batch_size)),
        storage_cost_usd=round(storage_cost * max(1.0, batch_mult), 8),
        wall_clock_seconds=round(wall_clock * (1.0 + 0.3 * math.log2(max(1, batch_size))), 3),
        total_cost_usd=round(total_cost, 8),
        cache_discount_pct=round(cache_hit_prob * 85, 1),
        mode_multiplier=mode_mult,
        batch_multiplier=round(batch_mult, 3) if batch_size > 1 else 1.0,
        chain_depth=chain_depth,
        confidence=round(0.88 - (chain_depth - 1) * 0.03 - (0.05 if batch_size > 100 else 0), 2),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# BUDGET TRACKER — in-memory (production would use D1)
# ═══════════════════════════════════════════════════════════════════════════════

class BudgetTracker:
    """Per-user budget tracking with alert levels and mode degradation."""

    def __init__(self) -> None:
        self._daily: Dict[str, float] = {}
        self._monthly: Dict[str, float] = {}
        self._limits: Dict[str, Dict[str, float]] = {}
        self._history: Dict[str, List[Dict[str, Any]]] = {}
        self._last_reset_day: Optional[int] = None
        self._last_reset_month: Optional[int] = None

    def _ensure_reset(self) -> None:
        now = datetime.now(timezone.utc)
        if self._last_reset_day != now.day:
            self._daily.clear()
            self._last_reset_day = now.day
        if self._last_reset_month != now.month:
            self._monthly.clear()
            self._last_reset_month = now.month

    def get_limits(self, user_id: str) -> Dict[str, float]:
        return self._limits.get(user_id, {"daily": 10.0, "monthly": 200.0})

    def set_limits(self, user_id: str, daily: float, monthly: float) -> None:
        self._limits[user_id] = {"daily": daily, "monthly": monthly}

    def record_cost(self, user_id: str, cost_usd: float, engine_id: str = "unknown") -> None:
        self._ensure_reset()
        self._daily[user_id] = self._daily.get(user_id, 0.0) + cost_usd
        self._monthly[user_id] = self._monthly.get(user_id, 0.0) + cost_usd
        if user_id not in self._history:
            self._history[user_id] = []
        self._history[user_id].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cost_usd": cost_usd,
            "engine_id": engine_id,
        })
        if len(self._history[user_id]) > 10000:
            self._history[user_id] = self._history[user_id][-5000:]

    def get_status(self, user_id: str) -> BudgetStatus:
        self._ensure_reset()
        limits = self.get_limits(user_id)
        daily_spent = self._daily.get(user_id, 0.0)
        monthly_spent = self._monthly.get(user_id, 0.0)
        daily_limit = limits["daily"]
        monthly_limit = limits["monthly"]
        daily_pct = (daily_spent / daily_limit * 100) if daily_limit > 0 else 0
        monthly_pct = (monthly_spent / monthly_limit * 100) if monthly_limit > 0 else 0
        max_pct = max(daily_pct, monthly_pct)

        if max_pct >= 100:
            alert = BudgetAlertLevel.CRITICAL_100
            rec_mode = ResponseMode.FAST
            allow = False
        elif max_pct >= 90:
            alert = BudgetAlertLevel.RED_90
            rec_mode = ResponseMode.FAST
            allow = True
        elif max_pct >= 75:
            alert = BudgetAlertLevel.ORANGE_75
            rec_mode = ResponseMode.FAST
            allow = True
        elif max_pct >= 50:
            alert = BudgetAlertLevel.YELLOW_50
            rec_mode = ResponseMode.DEFENSE
            allow = True
        else:
            alert = BudgetAlertLevel.GREEN
            rec_mode = ResponseMode.MEMO
            allow = True

        return BudgetStatus(
            user_id=user_id,
            daily_limit_usd=daily_limit,
            monthly_limit_usd=monthly_limit,
            daily_spent_usd=round(daily_spent, 6),
            monthly_spent_usd=round(monthly_spent, 6),
            daily_remaining_usd=round(max(0, daily_limit - daily_spent), 6),
            monthly_remaining_usd=round(max(0, monthly_limit - monthly_spent), 6),
            alert_level=alert,
            recommended_mode=rec_mode,
            allow_query=allow,
        )

    def get_history(self, user_id: str, last_n: int = 100) -> List[Dict[str, Any]]:
        return self._history.get(user_id, [])[-last_n:]


BUDGET_TRACKER = BudgetTracker()


# ═══════════════════════════════════════════════════════════════════════════════
# TELEMETRY — TIE Component 8
# ═══════════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self) -> None:
        self._latencies: List[float] = []
        self._errors: List[str] = []
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._queries_by_category: Dict[str, int] = {}
        self._queries_total: int = 0

    def record_query(self, latency_ms: float, cache_hit: bool, categories: List[str]) -> None:
        self._latencies.append(latency_ms)
        if len(self._latencies) > 50000:
            self._latencies = self._latencies[-25000:]
        if cache_hit:
            self._cache_hits += 1
        else:
            self._cache_misses += 1
        for cat in categories:
            self._queries_by_category[cat] = self._queries_by_category.get(cat, 0) + 1
        self._queries_total += 1

    def record_error(self, error_msg: str) -> None:
        self._errors.append(f"{datetime.now(timezone.utc).isoformat()} | {error_msg}")
        if len(self._errors) > 5000:
            self._errors = self._errors[-2500:]

    def get_stats(self) -> Dict[str, Any]:
        lats = self._latencies or [0]
        return {
            "total_queries": self._queries_total,
            "cache_hit_rate": round(self._cache_hits / max(1, self._cache_hits + self._cache_misses) * 100, 1),
            "latency_p50_ms": round(statistics.median(lats), 2),
            "latency_p95_ms": round(sorted(lats)[int(len(lats) * 0.95)] if lats else 0, 2),
            "latency_avg_ms": round(statistics.mean(lats), 2),
            "error_count": len(self._errors),
            "recent_errors": self._errors[-5:],
            "queries_by_category": dict(sorted(self._queries_by_category.items(), key=lambda x: x[1], reverse=True)[:10]),
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════════
# DRIFT WATCHER — TIE Component 9
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    def __init__(self) -> None:
        self._doctrine_versions: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []
        for topic, block in DOCTRINE_CACHE.items():
            self._doctrine_versions[topic] = hashlib.md5(block.reasoning_framework.encode()).hexdigest()[:12]

    def check_drift(self, topic: str, current_hash: str) -> Optional[Dict[str, Any]]:
        stored = self._doctrine_versions.get(topic)
        if stored and stored != current_hash:
            event = {
                "topic": topic,
                "old_hash": stored,
                "new_hash": current_hash,
                "detected_at": datetime.now(timezone.utc).isoformat(),
            }
            self._drift_events.append(event)
            self._doctrine_versions[topic] = current_hash
            return event
        return None

    def get_drift_report(self) -> Dict[str, Any]:
        return {
            "total_doctrines": len(self._doctrine_versions),
            "drift_events": len(self._drift_events),
            "recent_drifts": self._drift_events[-10:],
        }


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════════
# COVERAGE MAP — TIE Component 10
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    def __init__(self) -> None:
        self._triggered: Dict[str, int] = {}
        self._missed: List[str] = []

    def record_hit(self, doctrine_topic: str) -> None:
        self._triggered[doctrine_topic] = self._triggered.get(doctrine_topic, 0) + 1

    def record_miss(self, query_summary: str) -> None:
        self._missed.append(query_summary)
        if len(self._missed) > 2000:
            self._missed = self._missed[-1000:]

    def get_report(self) -> Dict[str, Any]:
        all_topics = set(DOCTRINE_CACHE.keys())
        triggered = set(self._triggered.keys())
        untriggered = all_topics - triggered
        return {
            "total_doctrines": len(all_topics),
            "triggered_doctrines": len(triggered),
            "untriggered_doctrines": sorted(untriggered),
            "top_triggered": sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:10],
            "recent_misses": self._missed[-10:],
            "coverage_pct": round(len(triggered) / max(1, len(all_topics)) * 100, 1),
        }


COVERAGE_MAP = CoverageMap()


# ═══════════════════════════════════════════════════════════════════════════════
# METRICS COLLECTOR — TIE Component 11
# ═══════════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    def __init__(self) -> None:
        self._start = time.time()
        self._request_count = 0
        self._error_count = 0
        self._latencies: List[float] = []

    def record_request(self, latency_ms: float, success: bool) -> None:
        self._request_count += 1
        if not success:
            self._error_count += 1
        self._latencies.append(latency_ms)
        if len(self._latencies) > 50000:
            self._latencies = self._latencies[-25000:]

    def get_metrics(self) -> Dict[str, Any]:
        uptime = time.time() - self._start
        lats = self._latencies or [0]
        return {
            "uptime_seconds": round(uptime, 1),
            "total_requests": self._request_count,
            "error_rate": round(self._error_count / max(1, self._request_count) * 100, 2),
            "requests_per_hour": round(self._request_count / max(1, uptime / 3600), 1),
            "latency_avg_ms": round(statistics.mean(lats), 2),
            "latency_p50_ms": round(statistics.median(lats), 2),
            "latency_p95_ms": round(sorted(lats)[int(len(lats) * 0.95)] if len(lats) > 1 else lats[0], 2),
        }


METRICS = MetricsCollector()


# ═══════════════════════════════════════════════════════════════════════════════
# FACT FRAGILITY SCORING — TIE Component 14
# ═══════════════════════════════════════════════════════════════════════════════

def score_fragility(cost_breakdown: CostBreakdown, engine_id: str) -> float:
    """Score how fragile/unreliable a cost estimate is (0=solid, 1=very fragile)."""
    fragility = 0.0
    if engine_id not in ENGINE_COST_PROFILES:
        fragility += 0.30
    if cost_breakdown.chain_depth > 1:
        fragility += 0.05 * cost_breakdown.chain_depth
    if cost_breakdown.batch_multiplier > 10:
        fragility += 0.15
    if cost_breakdown.llm_cost_usd > 0:
        fragility += 0.10
    if cost_breakdown.cache_discount_pct < 30:
        fragility += 0.10
    return min(1.0, round(fragility, 3))


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT TRAIL — TIE Component 15
# ═══════════════════════════════════════════════════════════════════════════════

def write_audit_entry(entry: Dict[str, Any]) -> None:
    """Append an entry to the JSONL audit trail."""
    try:
        entry["audit_timestamp"] = datetime.now(timezone.utc).isoformat()
        entry["engine_id"] = ENGINE_ID
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# DETERMINISM HASH — TIE Component 16
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, mode: str, answer: str) -> str:
    """SHA-256 hash for reproducibility verification."""
    payload = f"{ENGINE_ID}|{ENGINE_VERSION}|{query}|{mode}|{answer}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# ZONED ANALYSIS — TIE Component 13
# ═══════════════════════════════════════════════════════════════════════════════

def apply_zone_constraints(zone: AnalysisZone, answer: str, cost: CostBreakdown) -> str:
    """Apply zone-specific framing to the answer."""
    if zone == AnalysisZone.PLANNING:
        return f"[PLANNING ESTIMATE] {answer} Note: This is a forward-looking cost projection for budgeting purposes. Actual costs may vary based on runtime conditions, cache state, and model availability."
    elif zone == AnalysisZone.AUDIT:
        return f"[AUDIT RECORD] {answer} Cost breakdown is deterministic for the given inputs. Verify against actual billing records for reconciliation. Hash: {compute_determinism_hash('', '', answer)[:16]}"
    return answer


# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-DOCTRINE DECOMPOSITION — TIE Component 19
# ═══════════════════════════════════════════════════════════════════════════════

def decompose_query_to_doctrines(query: str) -> List[str]:
    """Identify which doctrine blocks are relevant to the query."""
    _, normalized_keywords = normalize_query(query)
    matched: List[Tuple[str, int]] = []
    for topic, block in DOCTRINE_CACHE.items():
        overlap = len(set(block.keywords) & set(normalized_keywords))
        query_lower = query.lower()
        for kw in block.keywords:
            if kw in query_lower:
                overlap += 1
        if overlap > 0:
            matched.append((topic, overlap))
    matched.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matched[:5]]


# ═══════════════════════════════════════════════════════════════════════════════
# DEEP ANALYSIS MODE — TIE Component 20
# ═══════════════════════════════════════════════════════════════════════════════

def deep_analysis(query: str, engine_id: str, mode: ResponseMode, cost: CostBreakdown) -> str:
    """Full reasoning chain for MEMO mode responses."""
    lines = [
        f"=== DEEP COST ANALYSIS: {engine_id} ===",
        f"Query: {query[:200]}",
        f"Mode: {mode.value} (multiplier: {MODE_MULTIPLIERS[mode]}x)",
        "",
        "--- TOKEN ANALYSIS ---",
        f"  Input tokens:  {cost.llm_input_tokens:,} (system prompt + query + context)",
        f"  Output tokens: {cost.llm_output_tokens:,} (response body)",
        f"  LLM cost:      ${cost.llm_cost_usd:.8f}",
        "",
        "--- COMPUTE ANALYSIS ---",
        f"  CPU time:      {cost.compute_ms:.1f}ms",
        f"  Compute cost:  ${cost.compute_cost_usd:.8f}",
        "",
        "--- STORAGE ANALYSIS ---",
        f"  Read ops:      {cost.storage_reads}",
        f"  Write ops:     {cost.storage_writes}",
        f"  Storage cost:  ${cost.storage_cost_usd:.8f}",
        "",
        "--- API ANALYSIS ---",
        f"  External calls: {cost.api_calls}",
        f"  API cost:       ${cost.api_cost_usd:.8f}",
        "",
        "--- TIMING ANALYSIS ---",
        f"  Wall clock:    {cost.wall_clock_seconds:.3f}s estimated",
        f"  Chain depth:   {cost.chain_depth}",
        "",
        "--- CACHE ANALYSIS ---",
        f"  Cache discount: {cost.cache_discount_pct:.1f}%",
        f"  Expected savings from cache: ${cost.total_cost_usd * (cost.cache_discount_pct / 100):.8f}",
        "",
        "--- TOTAL ---",
        f"  TOTAL ESTIMATED COST: ${cost.total_cost_usd:.8f}",
        f"  Confidence: {cost.confidence:.0%}",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE — TIE Component 1
# ═══════════════════════════════════════════════════════════════════════════════

def three_layer_response(
    query: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    target_engine: Optional[str] = None,
    document_length: Optional[int] = None,
    batch_size: int = 1,
    include_cloud_retriever: bool = False,
    chain_engines: Optional[List[str]] = None,
    user_id: Optional[str] = None,
) -> QueryResponse:
    """Three-layer response: doctrine cache -> semantic retrieval -> deep analysis."""
    t0 = time.time()
    global QUERY_COUNT, CACHE_HITS, CACHE_MISSES

    QUERY_COUNT += 1
    engine_id = target_engine or "E10"
    matched_doctrines = decompose_query_to_doctrines(query)
    categories_triggered = [IssueCategory.LLM_TOKEN_COST.value]

    cost = calculate_cost_breakdown(
        engine_id=engine_id,
        query=query,
        mode=mode,
        document_length=document_length,
        batch_size=batch_size,
        include_cloud_retriever=include_cloud_retriever,
        chain_engines=chain_engines,
    )

    # Layer 1: Doctrine cache
    cache_hit = False
    answer_parts: List[str] = []
    reasoning_parts: List[str] = []

    if matched_doctrines:
        cache_hit = True
        CACHE_HITS += 1
        COVERAGE_MAP.record_hit(matched_doctrines[0])
        primary_doctrine = DOCTRINE_CACHE[matched_doctrines[0]]
        answer_parts.append(f"Cost estimate for {engine_id} in {mode.value} mode: ${cost.total_cost_usd:.8f} total.")
        answer_parts.append(f"Tokens: {cost.llm_input_tokens:,} in / {cost.llm_output_tokens:,} out. Compute: {cost.compute_ms:.0f}ms. Wall clock: {cost.wall_clock_seconds:.2f}s.")
        if cost.cache_discount_pct > 0:
            answer_parts.append(f"Cache discount: {cost.cache_discount_pct:.1f}% probable.")
        if batch_size > 1:
            answer_parts.append(f"Batch of {batch_size}: ${cost.total_cost_usd:.8f} total (batch discount applied).")
        if chain_engines:
            answer_parts.append(f"Chain depth {cost.chain_depth} ({' -> '.join([engine_id] + chain_engines)}).")
        reasoning_parts.append(primary_doctrine.reasoning_framework)
        categories_triggered.extend([d for d in [IssueCategory.COMPUTE_COST.value, IssueCategory.STORAGE_COST.value, IssueCategory.TIME_COST.value]])
    else:
        CACHE_MISSES += 1
        COVERAGE_MAP.record_miss(query[:100])

    # Layer 2: Semantic retrieval (populate answer if cache missed)
    if not cache_hit or mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
        answer_parts.append(
            f"Detailed cost breakdown for {engine_id}: "
            f"LLM=${cost.llm_cost_usd:.8f}, API=${cost.api_cost_usd:.8f}, "
            f"Compute=${cost.compute_cost_usd:.8f}, Storage=${cost.storage_cost_usd:.8f}."
        )
        reasoning_parts.append(
            f"Estimation based on engine profile '{engine_id}' with mode multiplier {cost.mode_multiplier}x. "
            f"Query complexity factored into token and compute estimates. "
            f"Cache hit probability: {cost.cache_discount_pct / 85 * 100:.0f}%."
        )
        if mode == ResponseMode.DEFENSE:
            answer_parts.append(f"Authority: Based on ECHO fleet telemetry and Cloudflare published pricing.")
            categories_triggered.append(IssueCategory.BUDGET_ENFORCEMENT.value)

    # Layer 3: Deep analysis (MEMO mode)
    if mode == ResponseMode.MEMO:
        deep = deep_analysis(query, engine_id, mode, cost)
        answer_parts.append(deep)
        categories_triggered.extend([IssueCategory.HISTORICAL_ANALYSIS.value, IssueCategory.ROUTING_DECISION.value])

    # Budget check
    budget_status = None
    if user_id:
        budget_status = BUDGET_TRACKER.get_status(user_id)
        if budget_status.alert_level in (BudgetAlertLevel.RED_90, BudgetAlertLevel.CRITICAL_100):
            answer_parts.append(f"BUDGET WARNING: {budget_status.alert_level.value}. Daily: ${budget_status.daily_spent_usd:.4f}/${budget_status.daily_limit_usd:.2f}. Recommend {budget_status.recommended_mode.value} mode.")
        BUDGET_TRACKER.record_cost(user_id, cost.total_cost_usd, engine_id)

    answer = " ".join(answer_parts)
    reasoning = " ".join(reasoning_parts)
    answer = apply_zone_constraints(zone, answer, cost)
    fragility = score_fragility(cost, engine_id)
    determinism_hash = compute_determinism_hash(query, mode.value, answer)

    confidence_factors = {
        "engine_known": 1.0 if engine_id in ENGINE_COST_PROFILES else 0.7,
        "chain_penalty": max(0.7, 1.0 - (cost.chain_depth - 1) * 0.05),
        "batch_penalty": 0.95 if batch_size > 100 else 1.0,
    }
    final_confidence, confidence_level = stratify_confidence(0.88, confidence_factors)

    latency_ms = (time.time() - t0) * 1000
    TELEMETRY.record_query(latency_ms, cache_hit, categories_triggered)
    METRICS.record_request(latency_ms, True)

    write_audit_entry({
        "query": query[:500],
        "target_engine": engine_id,
        "mode": mode.value,
        "zone": zone.value,
        "cost_breakdown": cost.model_dump(),
        "cache_hit": cache_hit,
        "matched_doctrines": matched_doctrines,
        "determinism_hash": determinism_hash,
        "latency_ms": round(latency_ms, 2),
        "user_id": user_id,
    })

    return QueryResponse(
        query=query,
        mode=mode,
        zone=zone,
        answer=answer,
        reasoning=reasoning,
        cost_breakdown=cost,
        budget_status=budget_status,
        confidence=final_confidence,
        confidence_level=confidence_level,
        authorities_cited=[a["source"] for a in AUTHORITY_HIERARCHY[:3]],
        categories_triggered=categories_triggered,
        determinism_hash=determinism_hash,
        timestamp=datetime.now(timezone.utc).isoformat(),
        latency_ms=round(latency_ms, 2),
        doctrine_cache_hit=cache_hit,
        fragility_score=fragility,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# VECTOR SEARCH STUB — TIE Component 7 (uses cloud_retriever when available)
# ═══════════════════════════════════════════════════════════════════════════════

async def vector_search_fallback(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Semantic vector search fallback when doctrine cache misses."""
    if CognitionCloudRetriever is not None:
        try:
            cloud = CognitionCloudRetriever()
            results = await cloud.retrieve_all(query, category="cost_estimation")
            return [{"source": r.source, "content": r.content[:500], "score": r.score} for r in results.results[:top_k]]
        except Exception as exc:
            logger.warning(f"Cloud retriever failed: {exc}")
    return [{"source": "local_fallback", "content": f"No vector results for: {query[:100]}", "score": 0.0}]


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI SERVER — TIE Component 17
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} blocks")
    logger.info(f"Engine profiles loaded: {len(ENGINE_COST_PROFILES)} engines")
    logger.info(f"Model pricing loaded: {len(MODEL_PRICING)} models")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="Estimates query cost before execution. Enables cost-aware routing and budget enforcement.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health Endpoint — TIE Component 12 ──────────────────────────────────────

@app.get("/health")
async def health_check():
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "uptime_seconds": round(uptime, 1),
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "engine_profiles": len(ENGINE_COST_PROFILES),
        "model_pricing_entries": len(MODEL_PRICING),
        "queries_processed": QUERY_COUNT,
        "cache_hit_rate": round(CACHE_HITS / max(1, CACHE_HITS + CACHE_MISSES) * 100, 1),
        "telemetry": TELEMETRY.get_stats(),
        "metrics": METRICS.get_metrics(),
        "coverage": COVERAGE_MAP.get_report(),
        "drift": DRIFT_WATCHER.get_drift_report(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─── Main Query Endpoint ─────────────────────────────────────────────────────

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        response = three_layer_response(
            query=req.query,
            mode=req.mode,
            zone=req.zone,
            target_engine=req.target_engine,
            document_length=req.document_length,
            batch_size=req.batch_size,
            include_cloud_retriever=req.include_cloud_retriever,
            chain_engines=req.target_engines if req.target_engines else None,
            user_id=req.user_id,
        )
        return response
    except Exception as exc:
        logger.error(f"Query failed: {exc}")
        METRICS.record_request(0, False)
        TELEMETRY.record_error(str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


# ─── Dedicated Cost Estimate Endpoint ────────────────────────────────────────

@app.post("/estimate")
async def estimate_cost(req: CostEstimateRequest):
    cost = calculate_cost_breakdown(
        engine_id=req.target_engine,
        query=req.query_text,
        mode=req.mode,
        document_length=req.document_length,
        batch_size=req.batch_size,
        include_cloud_retriever=req.include_cloud_retriever,
        chain_engines=req.chain_engines if req.chain_engines else None,
    )
    budget_status = None
    if req.user_id:
        budget_status = BUDGET_TRACKER.get_status(req.user_id)
    return {
        "engine_id": req.target_engine,
        "mode": req.mode.value,
        "cost_breakdown": cost.model_dump(),
        "budget_status": budget_status.model_dump() if budget_status else None,
        "fragility_score": score_fragility(cost, req.target_engine),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─── Budget Endpoints ────────────────────────────────────────────────────────

@app.post("/budget/check")
async def budget_check(req: BudgetCheckRequest):
    status = BUDGET_TRACKER.get_status(req.user_id)
    will_exceed_daily = (status.daily_spent_usd + req.estimated_cost_usd) > status.daily_limit_usd
    will_exceed_monthly = (status.monthly_spent_usd + req.estimated_cost_usd) > status.monthly_limit_usd
    return {
        "user_id": req.user_id,
        "estimated_cost_usd": req.estimated_cost_usd,
        "budget_status": status.model_dump(),
        "will_exceed_daily": will_exceed_daily,
        "will_exceed_monthly": will_exceed_monthly,
        "recommendation": "BLOCK" if not status.allow_query else ("WARN" if will_exceed_daily or will_exceed_monthly else "ALLOW"),
    }


@app.get("/budget/status/{user_id}")
async def budget_status(user_id: str):
    return BUDGET_TRACKER.get_status(user_id).model_dump()


@app.post("/budget/set-limits")
async def set_budget_limits(user_id: str, daily: float = 10.0, monthly: float = 200.0):
    BUDGET_TRACKER.set_limits(user_id, daily, monthly)
    return {"user_id": user_id, "daily_limit": daily, "monthly_limit": monthly, "status": "updated"}


@app.post("/budget/record")
async def record_budget_spend(user_id: str, cost_usd: float, engine_id: str = "unknown"):
    BUDGET_TRACKER.record_cost(user_id, cost_usd, engine_id)
    return BUDGET_TRACKER.get_status(user_id).model_dump()


@app.get("/budget/history/{user_id}")
async def budget_history(user_id: str, last_n: int = 100):
    return {"user_id": user_id, "history": BUDGET_TRACKER.get_history(user_id, last_n)}


# ─── Engine Profile Endpoints ────────────────────────────────────────────────

@app.get("/profiles")
async def list_engine_profiles():
    return {
        "total": len(ENGINE_COST_PROFILES),
        "profiles": {eid: {**prof, "estimated_cost_fast": calculate_cost_breakdown(eid, "test query", ResponseMode.FAST).total_cost_usd} for eid, prof in ENGINE_COST_PROFILES.items()},
    }


@app.get("/profiles/{engine_id}")
async def get_engine_profile(engine_id: str):
    profile = ENGINE_COST_PROFILES.get(engine_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"No profile for engine {engine_id}")
    costs_by_mode = {}
    for m in ResponseMode:
        c = calculate_cost_breakdown(engine_id, "sample query for cost estimation", m)
        costs_by_mode[m.value] = c.model_dump()
    return {"engine_id": engine_id, "profile": profile, "costs_by_mode": costs_by_mode}


# ─── Model Pricing Endpoint ──────────────────────────────────────────────────

@app.get("/pricing")
async def list_model_pricing():
    return {"models": MODEL_PRICING, "last_updated": "2026-02-14"}


# ─── Telemetry / Metrics / Coverage / Drift ───────────────────────────────────

@app.get("/telemetry")
async def telemetry_endpoint():
    return TELEMETRY.get_stats()


@app.get("/metrics")
async def metrics_endpoint():
    return METRICS.get_metrics()


@app.get("/coverage")
async def coverage_endpoint():
    return COVERAGE_MAP.get_report()


@app.get("/drift")
async def drift_endpoint():
    return DRIFT_WATCHER.get_drift_report()


@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": sorted(DOCTRINE_CACHE.keys()),
        "categories": [c.value for c in IssueCategory],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str):
    block = DOCTRINE_CACHE.get(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return block.model_dump()


# ─── Compare Endpoint (multi-engine cost comparison) ──────────────────────────

@app.post("/compare")
async def compare_engines(
    query_text: str,
    engine_ids: List[str],
    mode: ResponseMode = ResponseMode.FAST,
    document_length: Optional[int] = None,
):
    results = {}
    for eid in engine_ids:
        cost = calculate_cost_breakdown(
            engine_id=eid,
            query=query_text,
            mode=mode,
            document_length=document_length,
        )
        results[eid] = {
            "total_cost_usd": cost.total_cost_usd,
            "wall_clock_seconds": cost.wall_clock_seconds,
            "llm_cost_usd": cost.llm_cost_usd,
            "compute_ms": cost.compute_ms,
            "confidence": cost.confidence,
        }
    sorted_by_cost = sorted(results.items(), key=lambda x: x[1]["total_cost_usd"])
    return {
        "query": query_text[:200],
        "mode": mode.value,
        "comparisons": results,
        "cheapest": sorted_by_cost[0][0] if sorted_by_cost else None,
        "fastest": min(results.items(), key=lambda x: x[1]["wall_clock_seconds"])[0] if results else None,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LOGURU LOGGING — TIE Component 18 (configured at module top)
# ═══════════════════════════════════════════════════════════════════════════════
# Already configured: LOG_DIR, rotation, retention, serialize for audit trail.


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
