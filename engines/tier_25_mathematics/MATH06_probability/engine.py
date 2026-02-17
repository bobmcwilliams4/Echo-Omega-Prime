"""
MATH06 — Probability Intelligence Engine
TIE-20 Compliant | Port 8568 | Tier 13 Mathematics
Authority: 5.0 | Mode: DET (Deterministic)

Covers: Probability axioms, conditional probability, Bayes' theorem,
combinatorics, discrete/continuous distributions, expected value, variance,
moment generating functions, joint/marginal/conditional distributions,
law of large numbers, Markov chains.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
SYSTEMS_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(SYSTEMS_DIR))

getcontext().prec = 50

# ---------------------------------------------------------------------------
# Loguru config
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    ENGINE_DIR / "math06.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}",
)
logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {level:<8} | {message}")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "MATH06"
ENGINE_NAME = "Probability Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8568
ENGINE_TIER = 13
ENGINE_AUTHORITY = 5.0
ENGINE_MODE = "DET"

SQRT_2PI = math.sqrt(2.0 * math.pi)
LN2 = math.log(2.0)
EULER_MASCHERONI = 0.5772156649015329


# ===================================================================
# COMPONENT 1 — THREE LAYER RESPONSE
# ===================================================================
class ResponseLayer(str, Enum):
    """Three tiers of response depth."""
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class LayeredResponse(BaseModel):
    """Result container for the three-layer pipeline."""
    layer_used: ResponseLayer
    latency_ms: float
    content: dict[str, Any]
    confidence: float
    determinism_hash: str


def three_layer_response(query: str, keywords: list[str]) -> LayeredResponse:
    """Execute the three-layer resolution pipeline.

    Layer 1 — Doctrine Cache (0-200 ms): exact keyword match against
    pre-compiled doctrine blocks.
    Layer 2 — Semantic Retrieval: normalized term lookup then fuzzy
    doctrine scan.
    Layer 3 — Deep Analysis: full computational engine invocation.
    """
    t0 = time.perf_counter()

    # Layer 1 — Doctrine Cache
    cache_hit = _doctrine_cache_lookup(query, keywords)
    if cache_hit is not None:
        latency = (time.perf_counter() - t0) * 1000
        return LayeredResponse(
            layer_used=ResponseLayer.DOCTRINE_CACHE,
            latency_ms=latency,
            content=cache_hit,
            confidence=cache_hit.get("confidence", 0.92),
            determinism_hash=_sha256(json.dumps(cache_hit, sort_keys=True)),
        )

    # Layer 2 — Semantic Retrieval
    sem_hit = _semantic_retrieval(query, keywords)
    if sem_hit is not None:
        latency = (time.perf_counter() - t0) * 1000
        return LayeredResponse(
            layer_used=ResponseLayer.SEMANTIC_RETRIEVAL,
            latency_ms=latency,
            content=sem_hit,
            confidence=sem_hit.get("confidence", 0.80),
            determinism_hash=_sha256(json.dumps(sem_hit, sort_keys=True)),
        )

    # Layer 3 — Deep Analysis
    deep = _deep_analysis(query, keywords)
    latency = (time.perf_counter() - t0) * 1000
    return LayeredResponse(
        layer_used=ResponseLayer.DEEP_ANALYSIS,
        latency_ms=latency,
        content=deep,
        confidence=deep.get("confidence", 0.70),
        determinism_hash=_sha256(json.dumps(deep, sort_keys=True)),
    )


# ===================================================================
# COMPONENT 2 — RESPONSE MODES
# ===================================================================
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class FormattedResponse(BaseModel):
    mode: ResponseMode
    summary: str
    detail: str
    citations: list[str]
    confidence_band: str
    determinism_hash: str


def format_response(raw: LayeredResponse, mode: ResponseMode) -> FormattedResponse:
    """Shape a LayeredResponse into the requested output mode."""
    content = raw.content
    summary = content.get("conclusion", content.get("topic", ""))
    detail_parts: list[str] = []

    if mode == ResponseMode.FAST:
        detail_parts.append(summary)
    elif mode == ResponseMode.DEFENSE:
        detail_parts.append(f"AUTHORITY BASIS: {content.get('primary_authority', 'N/A')}")
        detail_parts.append(f"CONCLUSION: {summary}")
        detail_parts.append(f"COUNTER-ARGUMENTS: {content.get('counter_arguments', 'N/A')}")
        detail_parts.append(f"CONFIDENCE: {raw.confidence:.2f}")
    elif mode == ResponseMode.MEMO:
        detail_parts.append("=" * 60)
        detail_parts.append(f"MEMORANDUM — {ENGINE_NAME}")
        detail_parts.append("=" * 60)
        detail_parts.append(f"TOPIC: {content.get('topic', 'N/A')}")
        detail_parts.append(f"KEYWORDS: {content.get('keywords', [])}")
        detail_parts.append(f"REASONING: {content.get('reasoning_framework', 'N/A')}")
        detail_parts.append(f"CONCLUSION: {summary}")
        detail_parts.append(f"AUTHORITY: {content.get('primary_authority', 'N/A')}")
        detail_parts.append(f"COUNTER: {content.get('counter_arguments', 'N/A')}")
        detail_parts.append(f"CONFIDENCE: {raw.confidence:.2f} ({raw.content.get('confidence_stratification', 'N/A')})")
        detail_parts.append("=" * 60)

    detail_text = "\n".join(detail_parts)
    citations = content.get("primary_authority", [])
    if isinstance(citations, str):
        citations = [citations]

    band = _confidence_band(raw.confidence)
    return FormattedResponse(
        mode=mode,
        summary=summary,
        detail=detail_text,
        citations=citations,
        confidence_band=band,
        determinism_hash=raw.determinism_hash,
    )


# ===================================================================
# COMPONENT 3 — DOCTRINE CACHE (loaded from JSON)
# ===================================================================
_DOCTRINE_BLOCKS: list[dict[str, Any]] = []


def _load_doctrine_cache() -> None:
    global _DOCTRINE_BLOCKS
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as fh:
            _DOCTRINE_BLOCKS = json.load(fh)
        logger.info("Loaded {} doctrine blocks from cache", len(_DOCTRINE_BLOCKS))
    else:
        logger.warning("doctrine_cache.json not found — cache empty")


def _doctrine_cache_lookup(query: str, keywords: list[str]) -> dict[str, Any] | None:
    if not _DOCTRINE_BLOCKS:
        _load_doctrine_cache()
    q_lower = query.lower()
    kw_set = {k.lower() for k in keywords}
    best_score = 0
    best_block: dict[str, Any] | None = None
    for block in _DOCTRINE_BLOCKS:
        block_kws = {k.lower() for k in block.get("keywords", [])}
        overlap = len(kw_set & block_kws)
        topic_match = 1 if block.get("topic", "").lower() in q_lower else 0
        score = overlap * 2 + topic_match * 3
        if score > best_score and score >= 3:
            best_score = score
            best_block = block
    return best_block


# ===================================================================
# COMPONENT 4 — AUTHORITY HARDENING
# ===================================================================
class AuthorityLevel(str, Enum):
    AXIOMATIC = "AXIOMATIC"
    THEOREM = "THEOREM"
    COROLLARY = "COROLLARY"
    HEURISTIC = "HEURISTIC"
    CONJECTURE = "CONJECTURE"

AUTHORITY_WEIGHTS: dict[str, float] = {
    "AXIOMATIC": 1.00,
    "THEOREM": 0.95,
    "COROLLARY": 0.85,
    "HEURISTIC": 0.60,
    "CONJECTURE": 0.40,
}


def resolve_authority_conflict(
    levels: list[AuthorityLevel],
) -> tuple[AuthorityLevel, float]:
    """Given multiple authority levels, return the dominant one and its weight."""
    if not levels:
        return AuthorityLevel.HEURISTIC, 0.60
    best = max(levels, key=lambda lv: AUTHORITY_WEIGHTS[lv.value])
    return best, AUTHORITY_WEIGHTS[best.value]


# ===================================================================
# COMPONENT 5 — CONFIDENCE STRATIFICATION
# ===================================================================
class ConfidenceBand(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def _confidence_band(score: float) -> str:
    if score >= 0.85:
        return ConfidenceBand.DEFENSIBLE.value
    if score >= 0.65:
        return ConfidenceBand.AGGRESSIVE.value
    if score >= 0.45:
        return ConfidenceBand.DISCLOSURE.value
    return ConfidenceBand.HIGH_RISK.value


def stratify_confidence(
    authority_weight: float,
    evidence_count: int,
    has_counter: bool,
) -> tuple[float, str]:
    """Compute a confidence score and band from authority + evidence."""
    base = authority_weight * 0.6
    ev_bonus = min(evidence_count * 0.05, 0.3)
    penalty = 0.10 if has_counter else 0.0
    score = min(max(base + ev_bonus - penalty, 0.0), 1.0)
    return score, _confidence_band(score)


# ===================================================================
# COMPONENT 6 — SEMANTIC NORMALIZATION
# ===================================================================
_SEMANTIC_DICT: dict[str, str] = {}


def _load_semantic_dict() -> None:
    global _SEMANTIC_DICT
    sd_path = ENGINE_DIR / "semantic_dict.json"
    if sd_path.exists():
        with open(sd_path, "r", encoding="utf-8") as fh:
            _SEMANTIC_DICT = json.load(fh)
        logger.info("Loaded {} semantic mappings", len(_SEMANTIC_DICT))
    else:
        logger.warning("semantic_dict.json not found")


def normalize_term(term: str) -> str:
    """Map a user term to its canonical form."""
    if not _SEMANTIC_DICT:
        _load_semantic_dict()
    return _SEMANTIC_DICT.get(term.lower(), term.lower())


def normalize_query(query: str) -> str:
    """Normalize every token in a query string."""
    tokens = query.lower().split()
    return " ".join(normalize_term(t) for t in tokens)


# ===================================================================
# COMPONENT 7 — VECTOR / SEMANTIC SEARCH
# ===================================================================
def _semantic_retrieval(query: str, keywords: list[str]) -> dict[str, Any] | None:
    """Fallback semantic search when doctrine cache misses."""
    nq = normalize_query(query)
    nkw = [normalize_term(k) for k in keywords]

    if not _DOCTRINE_BLOCKS:
        _load_doctrine_cache()

    best_score = 0.0
    best_block: dict[str, Any] | None = None
    for block in _DOCTRINE_BLOCKS:
        block_text = " ".join([
            block.get("topic", ""),
            " ".join(block.get("keywords", [])),
            block.get("conclusion_template", ""),
        ]).lower()
        score = 0.0
        for tok in nq.split():
            if tok in block_text:
                score += 1.0
        for kw in nkw:
            if kw in block_text:
                score += 2.0
        if score > best_score and score >= 2.0:
            best_score = score
            best_block = block
    return best_block


# ===================================================================
# COMPONENT 8 — TELEMETRY
# ===================================================================
class TelemetryRecord(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_id: str = ENGINE_ID
    query: str = ""
    keywords: list[str] = Field(default_factory=list)
    layer_used: str = ""
    latency_ms: float = 0.0
    confidence: float = 0.0
    mode: str = ""
    error: str = ""


_TELEMETRY_LOG: list[TelemetryRecord] = []
_MAX_TELEMETRY = 5000


def record_telemetry(rec: TelemetryRecord) -> None:
    _TELEMETRY_LOG.append(rec)
    if len(_TELEMETRY_LOG) > _MAX_TELEMETRY:
        _TELEMETRY_LOG.pop(0)
    logger.debug("Telemetry recorded: query_id={}", rec.query_id)


def get_telemetry_snapshot() -> list[dict[str, Any]]:
    return [r.model_dump() for r in _TELEMETRY_LOG[-100:]]


# ===================================================================
# COMPONENT 9 — DRIFT WATCHER
# ===================================================================
_DRIFT_OBSERVATIONS: list[dict[str, Any]] = []


def observe_drift(topic: str, expected_confidence: float, actual_confidence: float) -> dict[str, Any]:
    """Record a drift observation when confidence deviates from expected."""
    delta = actual_confidence - expected_confidence
    observation = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "topic": topic,
        "expected": expected_confidence,
        "actual": actual_confidence,
        "delta": round(delta, 4),
        "drifted": abs(delta) > 0.10,
    }
    _DRIFT_OBSERVATIONS.append(observation)
    if observation["drifted"]:
        logger.warning("DRIFT detected on '{}': delta={:.4f}", topic, delta)
    return observation


def get_drift_report() -> list[dict[str, Any]]:
    return _DRIFT_OBSERVATIONS[-50:]


# ===================================================================
# COMPONENT 10 — COVERAGE MAP
# ===================================================================
_COVERAGE_MAP: dict[str, Any] = {}


def _load_coverage_map() -> None:
    global _COVERAGE_MAP
    cm_path = ENGINE_DIR / "coverage_map.json"
    if cm_path.exists():
        with open(cm_path, "r", encoding="utf-8") as fh:
            _COVERAGE_MAP = json.load(fh)
        logger.info("Coverage map loaded: {} domains", len(_COVERAGE_MAP.get("domains", {})))
    else:
        _COVERAGE_MAP = {"domains": {}, "hits": {}, "misses": {}}


def record_coverage_hit(domain: str, topic: str) -> None:
    if not _COVERAGE_MAP:
        _load_coverage_map()
    hits = _COVERAGE_MAP.setdefault("hits", {})
    hits[domain] = hits.get(domain, 0) + 1
    logger.debug("Coverage HIT: {}::{}", domain, topic)


def record_coverage_miss(domain: str, topic: str) -> None:
    if not _COVERAGE_MAP:
        _load_coverage_map()
    misses = _COVERAGE_MAP.setdefault("misses", {})
    key = f"{domain}::{topic}"
    misses[key] = misses.get(key, 0) + 1
    logger.warning("Coverage MISS: {}", key)


def get_coverage_summary() -> dict[str, Any]:
    if not _COVERAGE_MAP:
        _load_coverage_map()
    return {
        "total_domains": len(_COVERAGE_MAP.get("domains", {})),
        "total_hits": sum(_COVERAGE_MAP.get("hits", {}).values()),
        "total_misses": sum(_COVERAGE_MAP.get("misses", {}).values()),
        "top_misses": sorted(
            _COVERAGE_MAP.get("misses", {}).items(),
            key=lambda x: x[1],
            reverse=True,
        )[:10],
    }


# ===================================================================
# COMPONENT 11 — METRICS COLLECTOR
# ===================================================================
class EngineMetrics:
    def __init__(self) -> None:
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.latency_sum: float = 0.0
        self.latency_max: float = 0.0
        self.cache_hits: int = 0
        self.semantic_hits: int = 0
        self.deep_hits: int = 0
        self.start_time: float = time.time()

    def record_query(self, latency_ms: float, layer: str, error: bool = False) -> None:
        self.total_queries += 1
        self.latency_sum += latency_ms
        self.latency_max = max(self.latency_max, latency_ms)
        if error:
            self.total_errors += 1
        if layer == "doctrine_cache":
            self.cache_hits += 1
        elif layer == "semantic_retrieval":
            self.semantic_hits += 1
        else:
            self.deep_hits += 1

    def snapshot(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_latency = (self.latency_sum / self.total_queries) if self.total_queries > 0 else 0.0
        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": round(self.total_errors / max(self.total_queries, 1), 4),
            "avg_latency_ms": round(avg_latency, 2),
            "max_latency_ms": round(self.latency_max, 2),
            "cache_hit_rate": round(self.cache_hits / max(self.total_queries, 1), 4),
            "semantic_hit_rate": round(self.semantic_hits / max(self.total_queries, 1), 4),
            "deep_hit_rate": round(self.deep_hits / max(self.total_queries, 1), 4),
            "uptime_seconds": round(uptime, 1),
            "queries_per_minute": round(self.total_queries / max(uptime / 60, 0.01), 2),
        }


_METRICS = EngineMetrics()


# ===================================================================
# COMPONENT 12 — HEALTH ENDPOINT (implemented in FastAPI section)
# ===================================================================
def get_health() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "authority": ENGINE_AUTHORITY,
        "mode": ENGINE_MODE,
        "status": "OPERATIONAL",
        "uptime_seconds": round(time.time() - _METRICS.start_time, 1),
        "metrics": _METRICS.snapshot(),
        "doctrine_blocks_loaded": len(_DOCTRINE_BLOCKS),
        "semantic_mappings_loaded": len(_SEMANTIC_DICT),
        "telemetry_records": len(_TELEMETRY_LOG),
        "drift_observations": len(_DRIFT_OBSERVATIONS),
        "coverage": get_coverage_summary(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ===================================================================
# COMPONENT 13 — ZONED ANALYSIS
# ===================================================================
class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


def zoned_analysis(query: str, zone: AnalysisZone, data: dict[str, Any]) -> dict[str, Any]:
    """Apply zone-specific analysis framing.

    PLANNING — forward-looking, exploratory, risk-aware.
    REPORTING — factual, concise, evidence-based.
    AUDIT — exhaustive, adversarial, full citation.
    """
    base_result = _deep_analysis(query, list(data.get("keywords", [])))

    if zone == AnalysisZone.PLANNING:
        base_result["zone"] = "PLANNING"
        base_result["framing"] = "forward-looking risk assessment"
        base_result["recommendation"] = (
            "Consider distributional assumptions and sample-size requirements "
            "before committing to a probabilistic model."
        )
    elif zone == AnalysisZone.REPORTING:
        base_result["zone"] = "REPORTING"
        base_result["framing"] = "factual evidence summary"
        base_result["recommendation"] = (
            "Report point estimates alongside confidence intervals; "
            "state distribution assumptions explicitly."
        )
    elif zone == AnalysisZone.AUDIT:
        base_result["zone"] = "AUDIT"
        base_result["framing"] = "exhaustive adversarial review"
        base_result["recommendation"] = (
            "Verify axiom compliance, check independence assumptions, "
            "validate parameter estimation methodology, test for distribution fit."
        )
    return base_result


# ===================================================================
# COMPONENT 14 — FACT FRAGILITY SCORING
# ===================================================================
def fact_fragility_score(
    verifiability: float,
    recharacterization_risk: float,
    testimony_dependence: float,
) -> dict[str, Any]:
    """Score how fragile a probabilistic claim is.

    verifiability: 0-1 (1 = easily verified, e.g. axiom)
    recharacterization_risk: 0-1 (1 = easily re-framed)
    testimony_dependence: 0-1 (1 = depends entirely on testimony)
    """
    fragility = (
        (1.0 - verifiability) * 0.40
        + recharacterization_risk * 0.35
        + testimony_dependence * 0.25
    )
    label = "SOLID" if fragility < 0.3 else "MODERATE" if fragility < 0.6 else "FRAGILE"
    return {
        "fragility_score": round(fragility, 4),
        "label": label,
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }


# ===================================================================
# COMPONENT 15 — AUDIT TRAIL (JSONL)
# ===================================================================
_AUDIT_TRAIL: list[dict[str, Any]] = []


def append_audit(entry: dict[str, Any]) -> None:
    entry["audit_ts"] = datetime.now(timezone.utc).isoformat()
    entry["engine_id"] = ENGINE_ID
    _AUDIT_TRAIL.append(entry)
    if len(_AUDIT_TRAIL) > 10000:
        _AUDIT_TRAIL.pop(0)


def get_audit_trail(last_n: int = 50) -> list[dict[str, Any]]:
    return _AUDIT_TRAIL[-last_n:]


# ===================================================================
# COMPONENT 16 — DETERMINISM HASH (SHA-256)
# ===================================================================
def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def determinism_hash(payload: Any) -> str:
    """Produce a reproducible SHA-256 over the JSON-serialised payload."""
    canonical = json.dumps(payload, sort_keys=True, default=str)
    return _sha256(canonical)


# ===================================================================
# COMPONENT 19 — MULTI-DOCTRINE DECOMPOSITION
# ===================================================================
class IssueCategory(str, Enum):
    AXIOMS = "AXIOMS"
    COMBINATORICS = "COMBINATORICS"
    DISCRETE_DISTRIBUTIONS = "DISCRETE_DISTRIBUTIONS"
    CONTINUOUS_DISTRIBUTIONS = "CONTINUOUS_DISTRIBUTIONS"
    CONDITIONAL_PROBABILITY = "CONDITIONAL_PROBABILITY"
    BAYESIAN_INFERENCE = "BAYESIAN_INFERENCE"
    EXPECTATION_VARIANCE = "EXPECTATION_VARIANCE"
    MOMENT_GENERATING = "MOMENT_GENERATING"
    JOINT_DISTRIBUTIONS = "JOINT_DISTRIBUTIONS"
    LIMIT_THEOREMS = "LIMIT_THEOREMS"
    MARKOV_CHAINS = "MARKOV_CHAINS"
    INCLUSION_EXCLUSION = "INCLUSION_EXCLUSION"


INTERACTION_EDGES: list[tuple[str, str, str]] = [
    ("AXIOMS", "CONDITIONAL_PROBABILITY", "foundation_for"),
    ("AXIOMS", "DISCRETE_DISTRIBUTIONS", "foundation_for"),
    ("AXIOMS", "CONTINUOUS_DISTRIBUTIONS", "foundation_for"),
    ("CONDITIONAL_PROBABILITY", "BAYESIAN_INFERENCE", "enables"),
    ("COMBINATORICS", "DISCRETE_DISTRIBUTIONS", "counting_for"),
    ("DISCRETE_DISTRIBUTIONS", "EXPECTATION_VARIANCE", "defines"),
    ("CONTINUOUS_DISTRIBUTIONS", "EXPECTATION_VARIANCE", "defines"),
    ("EXPECTATION_VARIANCE", "MOMENT_GENERATING", "encoded_by"),
    ("DISCRETE_DISTRIBUTIONS", "JOINT_DISTRIBUTIONS", "extends_to"),
    ("CONTINUOUS_DISTRIBUTIONS", "JOINT_DISTRIBUTIONS", "extends_to"),
    ("LIMIT_THEOREMS", "CONTINUOUS_DISTRIBUTIONS", "convergence_to"),
    ("MARKOV_CHAINS", "LIMIT_THEOREMS", "applies"),
    ("CONDITIONAL_PROBABILITY", "JOINT_DISTRIBUTIONS", "marginalizes"),
    ("AXIOMS", "INCLUSION_EXCLUSION", "foundation_for"),
    ("COMBINATORICS", "INCLUSION_EXCLUSION", "counting_for"),
    ("BAYESIAN_INFERENCE", "MARKOV_CHAINS", "transition_priors"),
]


def decompose_issue(query: str, keywords: list[str]) -> dict[str, Any]:
    """Identify which issue categories a query touches and map the DAG."""
    q_lower = query.lower()
    kw_lower = {k.lower() for k in keywords}

    category_keywords: dict[str, set[str]] = {
        "AXIOMS": {"axiom", "kolmogorov", "sigma-algebra", "probability space", "sample space", "event"},
        "COMBINATORICS": {"permutation", "combination", "factorial", "multinomial", "binomial coefficient", "stars and bars", "stirling"},
        "DISCRETE_DISTRIBUTIONS": {"binomial", "poisson", "geometric", "hypergeometric", "negative binomial", "pmf", "discrete"},
        "CONTINUOUS_DISTRIBUTIONS": {"normal", "exponential", "gamma", "beta", "uniform", "pdf", "cdf", "continuous", "gaussian"},
        "CONDITIONAL_PROBABILITY": {"conditional", "given", "bayes", "posterior", "prior", "likelihood"},
        "BAYESIAN_INFERENCE": {"bayes", "bayesian", "posterior", "prior", "likelihood", "update"},
        "EXPECTATION_VARIANCE": {"expected value", "expectation", "variance", "standard deviation", "mean", "e(x)", "var(x)"},
        "MOMENT_GENERATING": {"mgf", "moment generating", "characteristic function", "moments", "cumulant"},
        "JOINT_DISTRIBUTIONS": {"joint", "marginal", "conditional distribution", "covariance", "correlation", "independence"},
        "LIMIT_THEOREMS": {"law of large numbers", "central limit", "convergence", "lln", "clt", "weak law", "strong law"},
        "MARKOV_CHAINS": {"markov", "transition matrix", "steady state", "stationary", "absorbing", "ergodic", "chain"},
        "INCLUSION_EXCLUSION": {"inclusion", "exclusion", "union", "intersection", "complement"},
    }

    triggered: list[str] = []
    for cat, cat_kws in category_keywords.items():
        if any(ck in q_lower for ck in cat_kws) or (kw_lower & cat_kws):
            triggered.append(cat)

    relevant_edges = [
        e for e in INTERACTION_EDGES if e[0] in triggered or e[1] in triggered
    ]

    return {
        "query": query,
        "triggered_categories": triggered,
        "interaction_edges": relevant_edges,
        "total_categories": len(IssueCategory),
        "coverage_ratio": round(len(triggered) / len(IssueCategory), 4),
    }


# ===================================================================
# COMPONENT 20 — DEEP ANALYSIS MODE
# ===================================================================
def _deep_analysis(query: str, keywords: list[str]) -> dict[str, Any]:
    """Full computational deep analysis — multi-source synthesis."""
    decomposition = decompose_issue(query, keywords)
    categories = decomposition["triggered_categories"]

    results: dict[str, Any] = {
        "topic": query,
        "keywords": keywords,
        "decomposition": decomposition,
        "computations": {},
        "confidence": 0.75,
        "confidence_stratification": "AGGRESSIVE",
        "reasoning_framework": (
            "Identify the probability domain (combinatorial, distributional, conditional, "
            "limit-theoretic, or Markov). Apply relevant axioms and theorems. "
            "Compute exact or approximate values. Validate via alternative methods."
        ),
        "primary_authority": [
            "Kolmogorov Axioms (1933)",
            "Feller, An Introduction to Probability Theory and Its Applications",
            "Ross, A First Course in Probability",
        ],
        "counter_arguments": "Verify independence assumptions; check for distributional misfit.",
    }

    q_lower = query.lower()

    # Attempt automatic computation based on detected categories
    if "COMBINATORICS" in categories:
        results["computations"]["combinatorics_note"] = (
            "Use /compute/combinatorics endpoint for nPr, nCr, factorial, multinomial."
        )
    if "DISCRETE_DISTRIBUTIONS" in categories or "CONTINUOUS_DISTRIBUTIONS" in categories:
        results["computations"]["distribution_note"] = (
            "Use /compute/distribution endpoint for PMF/PDF/CDF/quantile calculations."
        )
    if "BAYESIAN_INFERENCE" in categories or "CONDITIONAL_PROBABILITY" in categories:
        results["computations"]["bayes_note"] = (
            "Use /compute/bayes endpoint for posterior calculation."
        )
    if "MARKOV_CHAINS" in categories:
        results["computations"]["markov_note"] = (
            "Use /compute/markov/steady-state endpoint for equilibrium distribution."
        )
    if "EXPECTATION_VARIANCE" in categories:
        results["computations"]["ev_note"] = (
            "Use /compute/expectation endpoint for E[X], Var(X) from distribution parameters."
        )

    return results


# ===================================================================
# PROBABILITY COMPUTATION ENGINES (REAL IMPLEMENTATIONS)
# ===================================================================

# --------------- Pure-Python Math Helpers ---------------

def _factorial(n: int) -> int:
    """Exact factorial using math.factorial."""
    if n < 0:
        raise ValueError("Factorial undefined for negative integers")
    return math.factorial(n)


def _comb(n: int, k: int) -> int:
    """Exact binomial coefficient C(n, k)."""
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def _perm(n: int, k: int) -> int:
    """Exact permutation P(n, k) = n! / (n-k)!."""
    if k < 0 or k > n:
        return 0
    return math.perm(n, k)


def _multinomial_coeff(n: int, groups: list[int]) -> int:
    """Multinomial coefficient n! / (k1! * k2! * ... * km!)."""
    if sum(groups) != n:
        raise ValueError(f"Groups must sum to n={n}, got {sum(groups)}")
    result = _factorial(n)
    for g in groups:
        result //= _factorial(g)
    return result


def _stirling_approx(n: int) -> float:
    """Stirling's approximation: n! ~ sqrt(2*pi*n) * (n/e)^n."""
    if n <= 0:
        return 1.0
    return SQRT_2PI * math.sqrt(n) * ((n / math.e) ** n)


def _stars_and_bars(n: int, k: int) -> int:
    """Number of ways to distribute n identical items into k distinct bins.

    C(n + k - 1, k - 1).
    """
    if k <= 0 or n < 0:
        return 0
    return _comb(n + k - 1, k - 1)


# --------------- Combinatorics Compute ---------------

class CombinatoricsRequest(BaseModel):
    operation: str  # "factorial", "permutation", "combination", "multinomial", "stirling", "stars_and_bars"
    n: int
    k: Optional[int] = None
    groups: Optional[list[int]] = None


class CombinatoricsResult(BaseModel):
    operation: str
    n: int
    k: Optional[int] = None
    groups: Optional[list[int]] = None
    result: str  # string to handle huge numbers
    approximate: Optional[float] = None


def compute_combinatorics(req: CombinatoricsRequest) -> CombinatoricsResult:
    """Compute combinatorial quantities."""
    op = req.operation.lower()
    if op == "factorial":
        val = _factorial(req.n)
        return CombinatoricsResult(
            operation=op, n=req.n, result=str(val),
            approximate=_stirling_approx(req.n) if req.n > 20 else None,
        )
    elif op == "permutation":
        k = req.k if req.k is not None else req.n
        val = _perm(req.n, k)
        return CombinatoricsResult(operation=op, n=req.n, k=k, result=str(val))
    elif op == "combination":
        k = req.k if req.k is not None else 0
        val = _comb(req.n, k)
        return CombinatoricsResult(operation=op, n=req.n, k=k, result=str(val))
    elif op == "multinomial":
        groups = req.groups or []
        val = _multinomial_coeff(req.n, groups)
        return CombinatoricsResult(operation=op, n=req.n, groups=groups, result=str(val))
    elif op == "stirling":
        val = _stirling_approx(req.n)
        exact = _factorial(req.n) if req.n <= 170 else None
        return CombinatoricsResult(
            operation=op, n=req.n, result=str(exact) if exact else "too_large",
            approximate=val,
        )
    elif op == "stars_and_bars":
        k = req.k if req.k is not None else 1
        val = _stars_and_bars(req.n, k)
        return CombinatoricsResult(operation=op, n=req.n, k=k, result=str(val))
    else:
        raise ValueError(f"Unknown combinatorics operation: {op}")


# --------------- Distribution Calculations (Pure Python) ---------------

def _erf(x: float) -> float:
    """Error function via math.erf."""
    return math.erf(x)


def _normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal distribution PDF."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (SQRT_2PI * sigma)


def _normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal distribution CDF via erf."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    z = (x - mu) / sigma
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _normal_quantile(p: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal quantile (inverse CDF) via rational approximation (Beasley-Springer-Moro)."""
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    if sigma <= 0:
        raise ValueError("sigma must be positive")

    # Rational approximation for the standard normal quantile
    a = [
        -3.969683028665376e+01, 2.209460984245205e+02,
        -2.759285104469687e+02, 1.383577518672690e+02,
        -3.066479806614716e+01, 2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01, 1.615858368580409e+02,
        -1.556989798598866e+02, 6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03, -3.223964580411365e-01,
        -2.400758277161838e+00, -2.549732539343734e+00,
        4.374664141464968e+00, 2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03, 3.224671290700398e-01,
        2.445134137142996e+00, 3.754408661907416e+00,
    ]

    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        z = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
            ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        z = (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
            (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        z = -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
            ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)

    return mu + sigma * z


def _binomial_pmf(k: int, n: int, p: float) -> float:
    """Binomial PMF: C(n,k) * p^k * (1-p)^(n-k)."""
    if k < 0 or k > n:
        return 0.0
    if p < 0.0 or p > 1.0:
        raise ValueError("p must be in [0, 1]")
    coeff = _comb(n, k)
    return coeff * (p ** k) * ((1.0 - p) ** (n - k))


def _binomial_cdf(k: int, n: int, p: float) -> float:
    """Binomial CDF: sum of PMF from 0 to k."""
    return sum(_binomial_pmf(i, n, p) for i in range(k + 1))


def _poisson_pmf(k: int, lam: float) -> float:
    """Poisson PMF: e^(-lam) * lam^k / k!."""
    if k < 0:
        return 0.0
    if lam < 0:
        raise ValueError("lambda must be non-negative")
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    log_pmf = -lam + k * math.log(lam) - math.lgamma(k + 1)
    return math.exp(log_pmf)


def _poisson_cdf(k: int, lam: float) -> float:
    return sum(_poisson_pmf(i, lam) for i in range(k + 1))


def _geometric_pmf(k: int, p: float) -> float:
    """Geometric PMF (number of trials until first success): p*(1-p)^(k-1), k>=1."""
    if k < 1:
        return 0.0
    if p <= 0 or p > 1:
        raise ValueError("p must be in (0, 1]")
    return p * ((1.0 - p) ** (k - 1))


def _geometric_cdf(k: int, p: float) -> float:
    """Geometric CDF: 1 - (1-p)^k."""
    if k < 1:
        return 0.0
    return 1.0 - ((1.0 - p) ** k)


def _hypergeometric_pmf(k: int, N: int, K: int, n: int) -> float:
    """Hypergeometric PMF: C(K,k)*C(N-K,n-k)/C(N,n)."""
    if k < max(0, n - (N - K)) or k > min(n, K):
        return 0.0
    num = _comb(K, k) * _comb(N - K, n - k)
    den = _comb(N, n)
    if den == 0:
        return 0.0
    return num / den


def _hypergeometric_cdf(k: int, N: int, K: int, n: int) -> float:
    lo = max(0, n - (N - K))
    return sum(_hypergeometric_pmf(i, N, K, n) for i in range(lo, k + 1))


def _negative_binomial_pmf(k: int, r: int, p: float) -> float:
    """Negative binomial PMF: C(k+r-1, k) * p^r * (1-p)^k, k>=0 failures."""
    if k < 0 or r < 1:
        return 0.0
    if p <= 0 or p > 1:
        raise ValueError("p must be in (0, 1]")
    coeff = _comb(k + r - 1, k)
    return coeff * (p ** r) * ((1.0 - p) ** k)


def _negative_binomial_cdf(k: int, r: int, p: float) -> float:
    return sum(_negative_binomial_pmf(i, r, p) for i in range(k + 1))


def _uniform_pdf(x: float, a: float, b: float) -> float:
    """Continuous uniform PDF on [a, b]."""
    if b <= a:
        raise ValueError("b must be greater than a")
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0


def _uniform_cdf(x: float, a: float, b: float) -> float:
    if b <= a:
        raise ValueError("b must be greater than a")
    if x < a:
        return 0.0
    if x > b:
        return 1.0
    return (x - a) / (b - a)


def _exponential_pdf(x: float, lam: float) -> float:
    """Exponential PDF: lam * exp(-lam * x), x >= 0."""
    if lam <= 0:
        raise ValueError("lambda must be positive")
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def _exponential_cdf(x: float, lam: float) -> float:
    if lam <= 0:
        raise ValueError("lambda must be positive")
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-lam * x)


def _gamma_function(z: float) -> float:
    """Gamma function via Lanczos approximation."""
    if z <= 0 and z == int(z):
        raise ValueError("Gamma undefined for non-positive integers")
    if z < 0.5:
        return math.pi / (math.sin(math.pi * z) * _gamma_function(1.0 - z))
    z -= 1.0
    g = 7
    coefficients = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7,
    ]
    x = coefficients[0]
    for i in range(1, g + 2):
        x += coefficients[i] / (z + i)
    t = z + g + 0.5
    return math.sqrt(2.0 * math.pi) * (t ** (z + 0.5)) * math.exp(-t) * x


def _log_gamma(z: float) -> float:
    """Log of the gamma function."""
    return math.lgamma(z)


def _gamma_pdf(x: float, alpha: float, beta: float) -> float:
    """Gamma distribution PDF: beta^alpha * x^(alpha-1) * exp(-beta*x) / Gamma(alpha).

    Parameterization: shape=alpha, rate=beta.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")
    if x <= 0:
        return 0.0
    log_pdf = alpha * math.log(beta) + (alpha - 1) * math.log(x) - beta * x - _log_gamma(alpha)
    return math.exp(log_pdf)


def _gamma_cdf(x: float, alpha: float, beta: float, steps: int = 1000) -> float:
    """Gamma CDF via numerical integration (Simpson's rule)."""
    if x <= 0:
        return 0.0
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")
    h = x / steps
    total = _gamma_pdf(0.0001, alpha, beta) + _gamma_pdf(x, alpha, beta)
    for i in range(1, steps):
        xi = i * h
        weight = 4.0 if i % 2 == 1 else 2.0
        total += weight * _gamma_pdf(xi, alpha, beta)
    return total * h / 3.0


def _beta_pdf(x: float, alpha: float, beta: float) -> float:
    """Beta distribution PDF: x^(a-1)*(1-x)^(b-1) / B(a,b)."""
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")
    if x <= 0 or x >= 1:
        return 0.0
    log_beta_fn = _log_gamma(alpha) + _log_gamma(beta) - _log_gamma(alpha + beta)
    log_pdf = (alpha - 1) * math.log(x) + (beta - 1) * math.log(1 - x) - log_beta_fn
    return math.exp(log_pdf)


def _beta_cdf(x: float, alpha: float, beta_param: float, steps: int = 1000) -> float:
    """Beta CDF via numerical integration (Simpson's rule)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    h = x / steps
    total = _beta_pdf(0.0001, alpha, beta_param) + _beta_pdf(x, alpha, beta_param)
    for i in range(1, steps):
        xi = i * h
        weight = 4.0 if i % 2 == 1 else 2.0
        total += weight * _beta_pdf(xi, alpha, beta_param)
    return min(total * h / 3.0, 1.0)


# --------------- Distribution Dispatch ---------------

class DistributionRequest(BaseModel):
    distribution: str  # "binomial", "poisson", "geometric", "hypergeometric", "negative_binomial",
                       # "normal", "exponential", "gamma", "beta", "uniform"
    operation: str     # "pmf", "pdf", "cdf", "quantile", "stats"
    x: Optional[float] = None
    k: Optional[int] = None
    n: Optional[int] = None
    p: Optional[float] = None
    lam: Optional[float] = None  # lambda
    mu: Optional[float] = None
    sigma: Optional[float] = None
    alpha: Optional[float] = None
    beta_param: Optional[float] = None
    a: Optional[float] = None
    b: Optional[float] = None
    r: Optional[int] = None
    N_pop: Optional[int] = None  # population size for hypergeometric
    K_success: Optional[int] = None  # success states in population


class DistributionResult(BaseModel):
    distribution: str
    operation: str
    value: float
    parameters: dict[str, Any]
    interpretation: str


def compute_distribution(req: DistributionRequest) -> DistributionResult:
    """Unified distribution calculator."""
    dist = req.distribution.lower()
    op = req.operation.lower()

    if dist == "binomial":
        n_val = req.n or 10
        p_val = req.p if req.p is not None else 0.5
        k_val = req.k if req.k is not None else 0
        params = {"n": n_val, "p": p_val, "k": k_val}

        if op == "pmf":
            val = _binomial_pmf(k_val, n_val, p_val)
            interp = f"P(X = {k_val}) for Binomial(n={n_val}, p={p_val})"
        elif op == "cdf":
            val = _binomial_cdf(k_val, n_val, p_val)
            interp = f"P(X <= {k_val}) for Binomial(n={n_val}, p={p_val})"
        elif op == "stats":
            mean = n_val * p_val
            var = n_val * p_val * (1 - p_val)
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var, "std": math.sqrt(var)},
                interpretation=f"E[X]={mean}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for binomial")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "poisson":
        lam_val = req.lam if req.lam is not None else 1.0
        k_val = req.k if req.k is not None else 0
        params = {"lambda": lam_val, "k": k_val}

        if op == "pmf":
            val = _poisson_pmf(k_val, lam_val)
            interp = f"P(X = {k_val}) for Poisson(lambda={lam_val})"
        elif op == "cdf":
            val = _poisson_cdf(k_val, lam_val)
            interp = f"P(X <= {k_val}) for Poisson(lambda={lam_val})"
        elif op == "stats":
            return DistributionResult(
                distribution=dist, operation=op, value=lam_val,
                parameters={**params, "mean": lam_val, "variance": lam_val},
                interpretation=f"E[X]=Var(X)=lambda={lam_val}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for poisson")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "geometric":
        p_val = req.p if req.p is not None else 0.5
        k_val = req.k if req.k is not None else 1
        params = {"p": p_val, "k": k_val}

        if op == "pmf":
            val = _geometric_pmf(k_val, p_val)
            interp = f"P(X = {k_val}) for Geometric(p={p_val})"
        elif op == "cdf":
            val = _geometric_cdf(k_val, p_val)
            interp = f"P(X <= {k_val}) for Geometric(p={p_val})"
        elif op == "stats":
            mean = 1.0 / p_val
            var = (1.0 - p_val) / (p_val ** 2)
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for geometric")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "hypergeometric":
        N_val = req.N_pop if req.N_pop is not None else 50
        K_val = req.K_success if req.K_success is not None else 10
        n_val = req.n if req.n is not None else 5
        k_val = req.k if req.k is not None else 2
        params = {"N": N_val, "K": K_val, "n": n_val, "k": k_val}

        if op == "pmf":
            val = _hypergeometric_pmf(k_val, N_val, K_val, n_val)
            interp = f"P(X = {k_val}) for Hypergeometric(N={N_val}, K={K_val}, n={n_val})"
        elif op == "cdf":
            val = _hypergeometric_cdf(k_val, N_val, K_val, n_val)
            interp = f"P(X <= {k_val}) for Hypergeometric(N={N_val}, K={K_val}, n={n_val})"
        elif op == "stats":
            mean = n_val * K_val / N_val
            var = n_val * K_val * (N_val - K_val) * (N_val - n_val) / (N_val ** 2 * (N_val - 1))
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for hypergeometric")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "negative_binomial":
        r_val = req.r if req.r is not None else 1
        p_val = req.p if req.p is not None else 0.5
        k_val = req.k if req.k is not None else 0
        params = {"r": r_val, "p": p_val, "k": k_val}

        if op == "pmf":
            val = _negative_binomial_pmf(k_val, r_val, p_val)
            interp = f"P(X = {k_val}) for NegBinomial(r={r_val}, p={p_val})"
        elif op == "cdf":
            val = _negative_binomial_cdf(k_val, r_val, p_val)
            interp = f"P(X <= {k_val}) for NegBinomial(r={r_val}, p={p_val})"
        elif op == "stats":
            mean = r_val * (1 - p_val) / p_val
            var = r_val * (1 - p_val) / (p_val ** 2)
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for negative_binomial")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "normal":
        mu_val = req.mu if req.mu is not None else 0.0
        sigma_val = req.sigma if req.sigma is not None else 1.0
        x_val = req.x if req.x is not None else 0.0
        p_val = req.p  # for quantile
        params = {"mu": mu_val, "sigma": sigma_val}

        if op == "pdf":
            val = _normal_pdf(x_val, mu_val, sigma_val)
            interp = f"f({x_val}) for Normal(mu={mu_val}, sigma={sigma_val})"
            params["x"] = x_val
        elif op == "cdf":
            val = _normal_cdf(x_val, mu_val, sigma_val)
            interp = f"P(X <= {x_val}) for Normal(mu={mu_val}, sigma={sigma_val})"
            params["x"] = x_val
        elif op == "quantile":
            if p_val is None:
                raise ValueError("p required for quantile operation")
            val = _normal_quantile(p_val, mu_val, sigma_val)
            interp = f"Quantile({p_val}) for Normal(mu={mu_val}, sigma={sigma_val})"
            params["p"] = p_val
        elif op == "stats":
            return DistributionResult(
                distribution=dist, operation=op, value=mu_val,
                parameters={**params, "mean": mu_val, "variance": sigma_val ** 2},
                interpretation=f"E[X]={mu_val}, Var(X)={sigma_val**2}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for normal")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "exponential":
        lam_val = req.lam if req.lam is not None else 1.0
        x_val = req.x if req.x is not None else 0.0
        params = {"lambda": lam_val}

        if op == "pdf":
            val = _exponential_pdf(x_val, lam_val)
            interp = f"f({x_val}) for Exponential(lambda={lam_val})"
            params["x"] = x_val
        elif op == "cdf":
            val = _exponential_cdf(x_val, lam_val)
            interp = f"P(X <= {x_val}) for Exponential(lambda={lam_val})"
            params["x"] = x_val
        elif op == "quantile":
            p_val_q = req.p
            if p_val_q is None or p_val_q <= 0 or p_val_q >= 1:
                raise ValueError("p must be in (0, 1) for quantile")
            val = -math.log(1.0 - p_val_q) / lam_val
            interp = f"Quantile({p_val_q}) for Exponential(lambda={lam_val})"
            params["p"] = p_val_q
        elif op == "stats":
            mean = 1.0 / lam_val
            var = 1.0 / (lam_val ** 2)
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for exponential")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "gamma":
        alpha_val = req.alpha if req.alpha is not None else 1.0
        beta_val = req.beta_param if req.beta_param is not None else 1.0
        x_val = req.x if req.x is not None else 1.0
        params = {"alpha": alpha_val, "beta": beta_val}

        if op == "pdf":
            val = _gamma_pdf(x_val, alpha_val, beta_val)
            interp = f"f({x_val}) for Gamma(alpha={alpha_val}, beta={beta_val})"
            params["x"] = x_val
        elif op == "cdf":
            val = _gamma_cdf(x_val, alpha_val, beta_val)
            interp = f"P(X <= {x_val}) for Gamma(alpha={alpha_val}, beta={beta_val})"
            params["x"] = x_val
        elif op == "stats":
            mean = alpha_val / beta_val
            var = alpha_val / (beta_val ** 2)
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for gamma")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "beta":
        alpha_val = req.alpha if req.alpha is not None else 2.0
        beta_val = req.beta_param if req.beta_param is not None else 5.0
        x_val = req.x if req.x is not None else 0.5
        params = {"alpha": alpha_val, "beta": beta_val}

        if op == "pdf":
            val = _beta_pdf(x_val, alpha_val, beta_val)
            interp = f"f({x_val}) for Beta(alpha={alpha_val}, beta={beta_val})"
            params["x"] = x_val
        elif op == "cdf":
            val = _beta_cdf(x_val, alpha_val, beta_val)
            interp = f"P(X <= {x_val}) for Beta(alpha={alpha_val}, beta={beta_val})"
            params["x"] = x_val
        elif op == "stats":
            mean = alpha_val / (alpha_val + beta_val)
            var = (alpha_val * beta_val) / ((alpha_val + beta_val) ** 2 * (alpha_val + beta_val + 1))
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for beta")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    elif dist == "uniform":
        a_val = req.a if req.a is not None else 0.0
        b_val = req.b if req.b is not None else 1.0
        x_val = req.x if req.x is not None else 0.5
        params = {"a": a_val, "b": b_val}

        if op == "pdf":
            val = _uniform_pdf(x_val, a_val, b_val)
            interp = f"f({x_val}) for Uniform({a_val}, {b_val})"
            params["x"] = x_val
        elif op == "cdf":
            val = _uniform_cdf(x_val, a_val, b_val)
            interp = f"P(X <= {x_val}) for Uniform({a_val}, {b_val})"
            params["x"] = x_val
        elif op == "quantile":
            p_val_q = req.p
            if p_val_q is None or p_val_q < 0 or p_val_q > 1:
                raise ValueError("p must be in [0, 1]")
            val = a_val + p_val_q * (b_val - a_val)
            interp = f"Quantile({p_val_q}) for Uniform({a_val}, {b_val})"
            params["p"] = p_val_q
        elif op == "stats":
            mean = (a_val + b_val) / 2.0
            var = (b_val - a_val) ** 2 / 12.0
            return DistributionResult(
                distribution=dist, operation=op, value=mean,
                parameters={**params, "mean": mean, "variance": var},
                interpretation=f"E[X]={mean:.4f}, Var(X)={var:.4f}",
            )
        else:
            raise ValueError(f"Unsupported operation '{op}' for uniform")
        return DistributionResult(distribution=dist, operation=op, value=val, parameters=params, interpretation=interp)

    else:
        raise ValueError(f"Unknown distribution: {dist}")


# --------------- Bayes' Theorem ---------------

class BayesRequest(BaseModel):
    prior: float
    likelihood: float
    evidence: Optional[float] = None
    hypotheses: Optional[list[dict[str, float]]] = None  # [{"prior": 0.3, "likelihood": 0.8}, ...]


class BayesResult(BaseModel):
    posterior: float
    prior: float
    likelihood: float
    evidence: float
    interpretation: str


def compute_bayes(req: BayesRequest) -> BayesResult:
    """Compute posterior probability via Bayes' theorem.

    P(H|E) = P(E|H) * P(H) / P(E)

    If evidence is not provided, compute it via law of total probability
    using the hypotheses list.
    """
    prior = req.prior
    likelihood = req.likelihood

    if req.evidence is not None and req.evidence > 0:
        evidence = req.evidence
    elif req.hypotheses:
        evidence = sum(h["prior"] * h["likelihood"] for h in req.hypotheses)
    else:
        evidence = likelihood * prior + (1 - likelihood) * (1 - prior)

    if evidence == 0:
        raise ValueError("Evidence probability cannot be zero")

    posterior = (likelihood * prior) / evidence

    return BayesResult(
        posterior=round(posterior, 8),
        prior=prior,
        likelihood=likelihood,
        evidence=round(evidence, 8),
        interpretation=(
            f"Given prior P(H)={prior}, likelihood P(E|H)={likelihood}, "
            f"and evidence P(E)={evidence:.6f}, the posterior P(H|E)={posterior:.6f}"
        ),
    )


# --------------- Conditional Probability ---------------

class ConditionalRequest(BaseModel):
    p_a_and_b: float  # P(A ∩ B)
    p_b: float         # P(B)


class ConditionalResult(BaseModel):
    p_a_given_b: float
    p_a_and_b: float
    p_b: float
    interpretation: str


def compute_conditional(req: ConditionalRequest) -> ConditionalResult:
    """Compute P(A|B) = P(A ∩ B) / P(B)."""
    if req.p_b <= 0:
        raise ValueError("P(B) must be positive")
    result = req.p_a_and_b / req.p_b
    return ConditionalResult(
        p_a_given_b=round(result, 8),
        p_a_and_b=req.p_a_and_b,
        p_b=req.p_b,
        interpretation=f"P(A|B) = {req.p_a_and_b} / {req.p_b} = {result:.6f}",
    )


# --------------- Law of Total Probability ---------------

class TotalProbRequest(BaseModel):
    partitions: list[dict[str, float]]  # [{"p_bi": 0.3, "p_a_given_bi": 0.8}, ...]


class TotalProbResult(BaseModel):
    p_a: float
    partitions: list[dict[str, float]]
    interpretation: str


def compute_total_probability(req: TotalProbRequest) -> TotalProbResult:
    """P(A) = sum_i P(A|B_i) * P(B_i)."""
    total = sum(p["p_bi"] * p["p_a_given_bi"] for p in req.partitions)
    return TotalProbResult(
        p_a=round(total, 8),
        partitions=req.partitions,
        interpretation="P(A) = " + " + ".join(str(p["p_bi"]) + "*" + str(p["p_a_given_bi"]) for p in req.partitions) + f" = {total:.6f}",
    )


# --------------- Inclusion-Exclusion ---------------

class InclusionExclusionRequest(BaseModel):
    probabilities: list[float]  # P(A_i)
    pairwise_intersections: Optional[list[float]] = None  # P(A_i ∩ A_j)
    triple_intersections: Optional[list[float]] = None  # P(A_i ∩ A_j ∩ A_k)
    all_intersection: Optional[float] = None  # P(A_1 ∩ ... ∩ A_n)


class InclusionExclusionResult(BaseModel):
    p_union: float
    terms_used: dict[str, float]
    interpretation: str


def compute_inclusion_exclusion(req: InclusionExclusionRequest) -> InclusionExclusionResult:
    """Compute P(A_1 ∪ ... ∪ A_n) via inclusion-exclusion principle."""
    n = len(req.probabilities)
    terms: dict[str, float] = {}

    # Sum of individual probabilities
    s1 = sum(req.probabilities)
    terms["sum_singles"] = s1

    result = s1

    # Subtract pairwise intersections
    if req.pairwise_intersections:
        s2 = sum(req.pairwise_intersections)
        terms["sum_pairs"] = s2
        result -= s2

    # Add triple intersections
    if req.triple_intersections:
        s3 = sum(req.triple_intersections)
        terms["sum_triples"] = s3
        result += s3

    # Subtract/add all-intersection (sign depends on n)
    if req.all_intersection is not None and n > 3:
        sign = (-1) ** (n + 1)
        terms["all_intersection"] = req.all_intersection
        result += sign * req.all_intersection

    result = min(max(result, 0.0), 1.0)

    return InclusionExclusionResult(
        p_union=round(result, 8),
        terms_used=terms,
        interpretation=f"P(union of {n} events) = {result:.6f}",
    )


# --------------- Expectation & Variance ---------------

class ExpectationRequest(BaseModel):
    distribution: str
    n: Optional[int] = None
    p: Optional[float] = None
    lam: Optional[float] = None
    mu: Optional[float] = None
    sigma: Optional[float] = None
    alpha: Optional[float] = None
    beta_param: Optional[float] = None
    a: Optional[float] = None
    b: Optional[float] = None
    r: Optional[int] = None
    N_pop: Optional[int] = None
    K_success: Optional[int] = None


class ExpectationResult(BaseModel):
    distribution: str
    mean: float
    variance: float
    std_dev: float
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    mgf_formula: str
    parameters: dict[str, Any]


def compute_expectation(req: ExpectationRequest) -> ExpectationResult:
    """Compute E[X], Var(X), std dev, skewness, kurtosis, and MGF formula."""
    dist = req.distribution.lower()
    params: dict[str, Any] = {}
    mean = 0.0
    var = 0.0
    skew: float | None = None
    kurt: float | None = None
    mgf = ""

    if dist == "binomial":
        n, p = req.n or 10, req.p if req.p is not None else 0.5
        params = {"n": n, "p": p}
        mean = n * p
        var = n * p * (1 - p)
        q = 1 - p
        skew = (q - p) / math.sqrt(n * p * q) if n * p * q > 0 else 0.0
        kurt = (1 - 6 * p * q) / (n * p * q) if n * p * q > 0 else 0.0
        mgf = f"(({q} + {p}*e^t))^{n}"

    elif dist == "poisson":
        lam = req.lam if req.lam is not None else 1.0
        params = {"lambda": lam}
        mean = lam
        var = lam
        skew = 1.0 / math.sqrt(lam) if lam > 0 else float("inf")
        kurt = 1.0 / lam if lam > 0 else float("inf")
        mgf = f"exp({lam}*(e^t - 1))"

    elif dist == "geometric":
        p = req.p if req.p is not None else 0.5
        params = {"p": p}
        mean = 1.0 / p
        var = (1 - p) / (p ** 2)
        skew = (2 - p) / math.sqrt(1 - p) if p < 1 else 0.0
        mgf = f"({p}*e^t) / (1 - (1-{p})*e^t) for t < -ln(1-{p})"

    elif dist == "hypergeometric":
        N = req.N_pop or 50
        K = req.K_success or 10
        n = req.n or 5
        params = {"N": N, "K": K, "n": n}
        mean = n * K / N
        var = n * K * (N - K) * (N - n) / (N ** 2 * (N - 1)) if N > 1 else 0.0
        mgf = "No closed-form MGF for hypergeometric"

    elif dist == "negative_binomial":
        r_val = req.r or 1
        p = req.p if req.p is not None else 0.5
        params = {"r": r_val, "p": p}
        mean = r_val * (1 - p) / p
        var = r_val * (1 - p) / (p ** 2)
        skew = (2 - p) / math.sqrt(r_val * (1 - p)) if r_val * (1 - p) > 0 else 0.0
        mgf = f"({p} / (1 - (1-{p})*e^t))^{r_val} for t < -ln(1-{p})"

    elif dist == "normal":
        mu = req.mu if req.mu is not None else 0.0
        sigma = req.sigma if req.sigma is not None else 1.0
        params = {"mu": mu, "sigma": sigma}
        mean = mu
        var = sigma ** 2
        skew = 0.0
        kurt = 0.0
        mgf = f"exp({mu}*t + {sigma**2}*t^2/2)"

    elif dist == "exponential":
        lam = req.lam if req.lam is not None else 1.0
        params = {"lambda": lam}
        mean = 1.0 / lam
        var = 1.0 / (lam ** 2)
        skew = 2.0
        kurt = 6.0
        mgf = f"{lam}/({lam} - t) for t < {lam}"

    elif dist == "gamma":
        a = req.alpha if req.alpha is not None else 1.0
        b = req.beta_param if req.beta_param is not None else 1.0
        params = {"alpha": a, "beta": b}
        mean = a / b
        var = a / (b ** 2)
        skew = 2.0 / math.sqrt(a) if a > 0 else float("inf")
        kurt = 6.0 / a if a > 0 else float("inf")
        mgf = f"({b}/({b} - t))^{a} for t < {b}"

    elif dist == "beta":
        a = req.alpha if req.alpha is not None else 2.0
        b = req.beta_param if req.beta_param is not None else 5.0
        params = {"alpha": a, "beta": b}
        mean = a / (a + b)
        var = (a * b) / ((a + b) ** 2 * (a + b + 1))
        skew = 2 * (b - a) * math.sqrt(a + b + 1) / ((a + b + 2) * math.sqrt(a * b)) if a * b > 0 else 0.0
        mgf = "1 + sum_{k=1}^inf (prod_{r=0}^{k-1} (a+r)/(a+b+r)) * t^k/k!"

    elif dist == "uniform":
        a = req.a if req.a is not None else 0.0
        b = req.b if req.b is not None else 1.0
        params = {"a": a, "b": b}
        mean = (a + b) / 2.0
        var = (b - a) ** 2 / 12.0
        skew = 0.0
        kurt = -6.0 / 5.0
        mgf = f"(e^({b}*t) - e^({a}*t)) / (({b}-{a})*t) for t != 0"

    else:
        raise ValueError(f"Unknown distribution: {dist}")

    return ExpectationResult(
        distribution=dist,
        mean=round(mean, 8),
        variance=round(var, 8),
        std_dev=round(math.sqrt(max(var, 0)), 8),
        skewness=round(skew, 6) if skew is not None else None,
        kurtosis=round(kurt, 6) if kurt is not None else None,
        mgf_formula=mgf,
        parameters=params,
    )


# --------------- Markov Chain Steady State ---------------

class MarkovRequest(BaseModel):
    transition_matrix: list[list[float]]
    initial_state: Optional[list[float]] = None
    steps: Optional[int] = None


class MarkovResult(BaseModel):
    steady_state: list[float]
    transition_matrix: list[list[float]]
    is_ergodic: bool
    iterations_to_converge: int
    state_after_n_steps: Optional[list[float]] = None
    interpretation: str


def _mat_mul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Multiply two square matrices."""
    n = len(A)
    result = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k_idx in range(n):
                result[i][j] += A[i][k_idx] * B[k_idx][j]
    return result


def _vec_mat_mul(v: list[float], M: list[list[float]]) -> list[float]:
    """Multiply row vector by matrix."""
    n = len(v)
    result = [0.0] * n
    for j in range(n):
        for i in range(n):
            result[j] += v[i] * M[i][j]
    return result


def compute_markov_steady_state(req: MarkovRequest) -> MarkovResult:
    """Find the steady-state distribution of a Markov chain via power iteration."""
    P = req.transition_matrix
    n = len(P)

    # Validate: each row sums to ~1
    for i, row in enumerate(P):
        row_sum = sum(row)
        if abs(row_sum - 1.0) > 0.01:
            raise ValueError(f"Row {i} sums to {row_sum}, expected ~1.0")

    # Power iteration: start with uniform distribution
    pi = [1.0 / n] * n
    max_iter = 10000
    tol = 1e-10
    iterations = 0

    for it in range(max_iter):
        pi_new = _vec_mat_mul(pi, P)
        diff = max(abs(pi_new[j] - pi[j]) for j in range(n))
        pi = pi_new
        iterations = it + 1
        if diff < tol:
            break

    # Normalize to ensure sum = 1
    total = sum(pi)
    if total > 0:
        pi = [x / total for x in pi]

    # Check ergodicity: all steady-state probs positive
    is_ergodic = all(x > 1e-12 for x in pi)

    # If steps requested, compute state after n steps
    state_n: list[float] | None = None
    if req.steps is not None and req.initial_state is not None:
        state = req.initial_state[:]
        for _ in range(req.steps):
            state = _vec_mat_mul(state, P)
        state_n = [round(x, 8) for x in state]

    return MarkovResult(
        steady_state=[round(x, 8) for x in pi],
        transition_matrix=P,
        is_ergodic=is_ergodic,
        iterations_to_converge=iterations,
        state_after_n_steps=state_n,
        interpretation=(
            f"Steady-state distribution converged in {iterations} iterations. "
            f"Ergodic: {is_ergodic}. "
            f"pi = [{', '.join(f'{x:.6f}' for x in pi)}]"
        ),
    )


# ===================================================================
# COMPONENT 17 — FASTAPI SERVER
# ===================================================================
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load caches on startup, flush on shutdown."""
    logger.info("MATH06 Probability Engine starting on port {}", ENGINE_PORT)
    _load_doctrine_cache()
    _load_semantic_dict()
    _load_coverage_map()
    logger.info("Startup complete — {} doctrines, {} semantic mappings",
                len(_DOCTRINE_BLOCKS), len(_SEMANTIC_DICT))
    yield
    logger.info("MATH06 shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant probability intelligence engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Models ---

class QueryRequest(BaseModel):
    query: str
    keywords: list[str] = Field(default_factory=list)
    mode: ResponseMode = ResponseMode.FAST
    zone: Optional[AnalysisZone] = None


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    query_id: str
    response: FormattedResponse
    layer_used: str
    latency_ms: float
    determinism_hash: str


# --- Endpoints ---

@app.get("/health")
async def health_endpoint() -> dict[str, Any]:
    """COMPONENT 12 — Health check endpoint."""
    return get_health()


@app.post("/query")
async def query_endpoint(req: QueryRequest) -> QueryResponse:
    """Main query endpoint — three-layer resolution with response mode."""
    query_id = str(uuid.uuid4())
    t0 = time.perf_counter()

    try:
        if req.zone:
            raw_content = zoned_analysis(req.query, req.zone, {"keywords": req.keywords})
            latency = (time.perf_counter() - t0) * 1000
            raw = LayeredResponse(
                layer_used=ResponseLayer.DEEP_ANALYSIS,
                latency_ms=latency,
                content=raw_content,
                confidence=raw_content.get("confidence", 0.75),
                determinism_hash=determinism_hash(raw_content),
            )
        else:
            raw = three_layer_response(req.query, req.keywords)

        formatted = format_response(raw, req.mode)

        # Telemetry
        rec = TelemetryRecord(
            query_id=query_id,
            query=req.query,
            keywords=req.keywords,
            layer_used=raw.layer_used.value,
            latency_ms=raw.latency_ms,
            confidence=raw.confidence,
            mode=req.mode.value,
        )
        record_telemetry(rec)
        _METRICS.record_query(raw.latency_ms, raw.layer_used.value)

        # Coverage
        decomp = decompose_issue(req.query, req.keywords)
        for cat in decomp["triggered_categories"]:
            record_coverage_hit("probability", cat)

        # Audit
        append_audit({
            "query_id": query_id,
            "query": req.query,
            "mode": req.mode.value,
            "layer": raw.layer_used.value,
            "confidence": raw.confidence,
            "latency_ms": raw.latency_ms,
        })

        return QueryResponse(
            query_id=query_id,
            response=formatted,
            layer_used=raw.layer_used.value,
            latency_ms=raw.latency_ms,
            determinism_hash=raw.determinism_hash,
        )

    except Exception as exc:
        logger.error("Query failed: {}", exc)
        _METRICS.record_query(0, "error", error=True)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/compute/combinatorics")
async def combinatorics_endpoint(req: CombinatoricsRequest) -> CombinatoricsResult:
    """Compute factorial, permutation, combination, multinomial, stirling, stars_and_bars."""
    try:
        result = compute_combinatorics(req)
        append_audit({"operation": "combinatorics", "request": req.model_dump(), "result": result.result})
        return result
    except Exception as exc:
        logger.error("Combinatorics error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/distribution")
async def distribution_endpoint(req: DistributionRequest) -> DistributionResult:
    """Compute PMF/PDF/CDF/quantile/stats for any supported distribution."""
    try:
        result = compute_distribution(req)
        append_audit({"operation": "distribution", "dist": req.distribution, "op": req.operation, "value": result.value})
        return result
    except Exception as exc:
        logger.error("Distribution error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/bayes")
async def bayes_endpoint(req: BayesRequest) -> BayesResult:
    """Compute posterior probability via Bayes' theorem."""
    try:
        result = compute_bayes(req)
        append_audit({"operation": "bayes", "posterior": result.posterior})
        return result
    except Exception as exc:
        logger.error("Bayes error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/conditional")
async def conditional_endpoint(req: ConditionalRequest) -> ConditionalResult:
    """Compute P(A|B) = P(A ∩ B) / P(B)."""
    try:
        result = compute_conditional(req)
        append_audit({"operation": "conditional", "result": result.p_a_given_b})
        return result
    except Exception as exc:
        logger.error("Conditional error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/total-probability")
async def total_prob_endpoint(req: TotalProbRequest) -> TotalProbResult:
    """Compute P(A) via law of total probability."""
    try:
        result = compute_total_probability(req)
        append_audit({"operation": "total_probability", "result": result.p_a})
        return result
    except Exception as exc:
        logger.error("Total probability error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/inclusion-exclusion")
async def inclusion_exclusion_endpoint(req: InclusionExclusionRequest) -> InclusionExclusionResult:
    """Compute P(union) via inclusion-exclusion principle."""
    try:
        result = compute_inclusion_exclusion(req)
        append_audit({"operation": "inclusion_exclusion", "result": result.p_union})
        return result
    except Exception as exc:
        logger.error("Inclusion-exclusion error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/expectation")
async def expectation_endpoint(req: ExpectationRequest) -> ExpectationResult:
    """Compute E[X], Var(X), MGF formula for a distribution."""
    try:
        result = compute_expectation(req)
        append_audit({"operation": "expectation", "dist": req.distribution, "mean": result.mean, "var": result.variance})
        return result
    except Exception as exc:
        logger.error("Expectation error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/compute/markov/steady-state")
async def markov_endpoint(req: MarkovRequest) -> MarkovResult:
    """Find steady-state distribution of a Markov chain."""
    try:
        result = compute_markov_steady_state(req)
        append_audit({"operation": "markov_steady_state", "ergodic": result.is_ergodic, "iterations": result.iterations_to_converge})
        return result
    except Exception as exc:
        logger.error("Markov error: {}", exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/metrics")
async def metrics_endpoint() -> dict[str, Any]:
    return _METRICS.snapshot()


@app.get("/telemetry")
async def telemetry_endpoint(last_n: int = Query(default=50, ge=1, le=500)) -> list[dict[str, Any]]:
    return get_telemetry_snapshot()[-last_n:]


@app.get("/drift")
async def drift_endpoint() -> list[dict[str, Any]]:
    return get_drift_report()


@app.get("/coverage")
async def coverage_endpoint() -> dict[str, Any]:
    return get_coverage_summary()


@app.get("/audit")
async def audit_endpoint(last_n: int = Query(default=50, ge=1, le=500)) -> list[dict[str, Any]]:
    return get_audit_trail(last_n)


@app.post("/decompose")
async def decompose_endpoint(req: QueryRequest) -> dict[str, Any]:
    """Decompose a query into issue categories and interaction DAG."""
    return decompose_issue(req.query, req.keywords)


@app.post("/fragility")
async def fragility_endpoint(
    verifiability: float = Query(ge=0, le=1),
    recharacterization_risk: float = Query(ge=0, le=1),
    testimony_dependence: float = Query(ge=0, le=1),
) -> dict[str, Any]:
    return fact_fragility_score(verifiability, recharacterization_risk, testimony_dependence)


# ===================================================================
# COMPONENT 18 — LOGURU LOGGING (configured at top of file)
# ===================================================================
# Already configured above with rotation and structured format.


# ===================================================================
# MAIN ENTRY POINT
# ===================================================================
if __name__ == "__main__":
    import uvicorn

    logger.info("Launching {} v{} on port {}", ENGINE_NAME, ENGINE_VERSION, ENGINE_PORT)
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
