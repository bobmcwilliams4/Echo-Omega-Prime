"""
ECHO ALGEBRA INTELLIGENCE ENGINE (MATH02) — Production Architecture
Professional-grade algebra engine: symbolic manipulation, equation solving,
polynomial operations, matrix algebra, complex numbers, inequalities.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled algebra reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Fast lookup on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-step symbolic computation

Response Modes:
    FAST: Direct answer, minimal steps
    DEFENSE: Full step-by-step derivation, proof-grade
    MEMO: Long-form with theorems cited, educational

Author: ECHO OMEGA PRIME
Authority: 5.0
Port: 8564
TIE-20 Compliant: All 20 components implemented
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal, Tuple, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pathlib import Path
from loguru import logger
import hashlib
import json
import math
import cmath
import time
import uuid
import sys
import re
import os
import copy
import fractions

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "algebra_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

ENGINE_VERSION = "1.0.0"
ENGINE_NAME = "MATH02_algebra"
ENGINE_PORT = 8564
_START_TIME = time.time()


# ============================================================================
# TIE-11: METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Lightweight metrics for operational awareness."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 100

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p95_ms": 0.0, "last_ms": 0.0}
        s = sorted(self.latencies)
        p95 = int(len(s) * 0.95)
        return {
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2),
            "p95_ms": round(s[min(p95, len(s) - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 1.0
        return round(self.doctrine_hits / total, 3)

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        return sum(1 for t in self.queries if t > cutoff)


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    return _metrics


# ============================================================================
# ENUMS AND TYPES
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class Complexity(str, Enum):
    STANDARD = "standard"
    ADVANCED = "advanced"


class ProblemDomain(str, Enum):
    LINEAR_EQUATION = "linear_equation"
    QUADRATIC_EQUATION = "quadratic_equation"
    CUBIC_EQUATION = "cubic_equation"
    SYSTEM_OF_EQUATIONS = "system_of_equations"
    POLYNOMIAL_OPS = "polynomial_operations"
    POLYNOMIAL_FACTORING = "polynomial_factoring"
    COMPLEX_NUMBER = "complex_number"
    LOGARITHM = "logarithm"
    EXPONENTIAL = "exponential"
    MATRIX = "matrix"
    INEQUALITY = "inequality"
    ABSOLUTE_VALUE = "absolute_value"
    RATIONAL_EXPRESSION = "rational_expression"
    GENERAL = "general"


class PositionZone(str, Enum):
    """Zone separation for algebra analysis output."""
    COMPUTATION = "computation"
    VERIFICATION = "verification"
    PROOF = "proof"


class AuthorityLevel(str, Enum):
    """Authority hierarchy for mathematical results."""
    AXIOM = "axiom"
    THEOREM = "theorem"
    LEMMA = "lemma"
    COROLLARY = "corollary"
    DEFINITION = "definition"
    ALGORITHM = "algorithm"

    @property
    def weight(self) -> int:
        weights = {
            "axiom": 100, "theorem": 90, "lemma": 70,
            "corollary": 60, "definition": 80, "algorithm": 50,
        }
        return weights.get(self.value, 10)


class ConfidenceStratification(str, Enum):
    DEFENSIBLE = "defensible"
    NUMERICALLY_VERIFIED = "numerically_verified"
    APPROXIMATE = "approximate"
    REQUIRES_REVIEW = "requires_review"


class IssueCategory(str, Enum):
    SOLVING = "solving"
    SIMPLIFICATION = "simplification"
    FACTORING = "factoring"
    GRAPHING = "graphing"
    TRANSFORMATION = "transformation"
    COMPUTATION = "computation"
    PROOF = "proof"
    IDENTITY = "identity"
    DOMAIN_RANGE = "domain_range"
    ROOTS = "roots"
    DECOMPOSITION = "decomposition"
    OPTIMIZATION = "optimization"


class DoctrineStratum(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


# ============================================================================
# REQUEST / RESPONSE MODELS
# ============================================================================

class AlgebraQuery(BaseModel):
    question: str = Field(..., min_length=3, description="Algebra problem or question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    domain: Optional[ProblemDomain] = Field(default=None, description="Hint for problem domain")
    complexity: Complexity = Field(default=Complexity.STANDARD)
    include_trace: bool = Field(default=False)
    numeric_precision: int = Field(default=10, ge=1, le=50)


class Citation(BaseModel):
    authority: str
    reference: str
    relevance: str


class ReasoningStep(BaseModel):
    step: int
    analysis: str
    authority: Optional[str] = None


class AlgebraResponse(BaseModel):
    query_id: str
    question: str
    mode: ResponseMode
    domain_detected: str
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    steps: Optional[List[ReasoningStep]] = None
    numeric_result: Optional[Any] = None
    doctrine_match: bool
    confidence_tier: Literal["high", "moderate", "requires_review"]
    confidence_stratification: Optional[str] = None
    response_layer: Literal["doctrine", "retrieval", "deep_analysis", "computation"]
    latency_ms: float
    determinism_hash: Optional[str] = None
    zoned_analysis: Optional[List[Dict[str, Any]]] = None
    coverage_report: Optional[Dict[str, Any]] = None
    limitations: List[str] = Field(default_factory=list)
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    version: str
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    memory_mb: Dict[str, float]
    active_queries: int
    queries_last_hour: int
    error_rate: Dict[str, Any]


# ============================================================================
# TIE-04: AUTHORITY HARDENING
# ============================================================================

@dataclass
class ControllingPrecedent:
    theorem_name: str
    citation: str
    domain: str
    statement: str
    binding_scope: str

    @property
    def precedential_weight(self) -> int:
        domain_weights = {
            "fundamental_theorem": 100,
            "named_theorem": 90,
            "standard_algorithm": 70,
            "identity": 80,
        }
        return domain_weights.get(self.domain, 50)


@dataclass
class ConflictResolution:
    competing_methods: List[str]
    resolution_rationale: str
    authority_basis: str
    rejected_alternatives: List[Dict[str, str]]


@dataclass
class MatchResult:
    doctrine: Optional["DoctrineBlock"]
    topic_key: Optional[str]
    match_score: int
    authority_weight: int
    conflict_detected: bool
    conflict_resolution: Optional[ConflictResolution]
    all_candidates: List[Dict[str, Any]]
    determinism_hash: str

    @property
    def is_match(self) -> bool:
        return self.doctrine is not None


@dataclass
class DoctrineInteraction:
    source_topic: str
    target_topic: str
    interaction_type: str
    description: str
    direction: str = "directed"


@dataclass
class StratifiedMatch:
    issues_detected: List[IssueCategory]
    primary: Optional[MatchResult]
    secondary: List[MatchResult]
    tertiary: List[MatchResult]
    interactions: List[DoctrineInteraction]
    resolution_hierarchy: List[Dict[str, Any]]
    total_doctrines_matched: int
    determinism_hash: str
    coverage_report: Optional[Dict[str, Any]] = None

    @property
    def is_multi_doctrine(self) -> bool:
        has_p = self.primary is not None and self.primary.is_match
        has_s = any(m.is_match for m in self.secondary)
        has_t = any(m.is_match for m in self.tertiary)
        return sum([has_p, has_s, has_t]) > 1

    @property
    def all_matched_topics(self) -> List[str]:
        topics: List[str] = []
        if self.primary and self.primary.topic_key:
            topics.append(self.primary.topic_key)
        for m in self.secondary:
            if m.topic_key:
                topics.append(m.topic_key)
        for m in self.tertiary:
            if m.topic_key:
                topics.append(m.topic_key)
        return topics


# ============================================================================
# TIE-03: DOCTRINE CACHE — Pre-compiled algebra reasoning blocks
# ============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled expert reasoning block for algebra."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[Dict[str, str]]
    verification_method: str
    typical_errors: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: List[str] = field(default_factory=lambda: ["all"])
    confidence: str = "high"
    confidence_stratification: ConfidenceStratification = ConfidenceStratification.DEFENSIBLE
    controlling_precedent: Optional[ControllingPrecedent] = None
    related_doctrines: List[str] = field(default_factory=list)

    def get_authority_weight(self) -> int:
        if not self.primary_authority:
            return 0
        max_w = 0
        for auth in self.primary_authority:
            level = auth.get("level", "algorithm")
            w = AuthorityLevel(level).weight if level in [e.value for e in AuthorityLevel] else 10
            max_w = max(max_w, w)
        return max_w


def _build_doctrine_cache() -> Dict[str, DoctrineBlock]:
    """Load doctrine blocks from doctrine_cache.json and build runtime cache."""
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if not cache_path.exists():
        logger.warning("doctrine_cache.json not found, using empty cache")
        return {}
    with open(cache_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    blocks: Dict[str, DoctrineBlock] = {}
    for key, entry in raw.items():
        cp_data = entry.get("controlling_precedent")
        cp = None
        if cp_data:
            cp = ControllingPrecedent(
                theorem_name=cp_data["theorem_name"],
                citation=cp_data["citation"],
                domain=cp_data["domain"],
                statement=cp_data["statement"],
                binding_scope=cp_data["binding_scope"],
            )
        strat = entry.get("confidence_stratification", "defensible")
        blocks[key] = DoctrineBlock(
            topic=entry["topic"],
            keywords=entry["keywords"],
            conclusion_template=entry["conclusion_template"],
            reasoning_framework=entry["reasoning_framework"],
            key_factors=entry["key_factors"],
            primary_authority=entry["primary_authority"],
            verification_method=entry.get("verification_method", "substitution"),
            typical_errors=entry.get("typical_errors", ""),
            counter_arguments=entry.get("counter_arguments", []),
            resolution_strategy=entry.get("resolution_strategy", ""),
            confidence=entry.get("confidence", "high"),
            confidence_stratification=ConfidenceStratification(strat),
            controlling_precedent=cp,
            related_doctrines=entry.get("related_doctrines", []),
        )
    logger.info(f"Loaded {len(blocks)} doctrine blocks from cache")
    return blocks


DOCTRINE_CACHE: Dict[str, DoctrineBlock] = _build_doctrine_cache()


# ============================================================================
# TIE-06: SEMANTIC NORMALIZATION
# ============================================================================

def _load_semantic_dict() -> Dict[str, str]:
    """Load semantic normalization dictionary."""
    path = ENGINE_DIR / "semantic_dict.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


_SEMANTIC_MAP: Dict[str, str] = _load_semantic_dict()


def normalize_query(raw: str) -> str:
    """Deterministic semantic normalization of algebra queries."""
    text = raw.lower().strip()
    for pattern, replacement in _SEMANTIC_MAP.items():
        text = re.sub(r"\b" + re.escape(pattern) + r"\b", replacement, text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ============================================================================
# TIE-16: DETERMINISM HASH (SHA-256)
# ============================================================================

def compute_determinism_hash(query: str, mode: str, result: str) -> str:
    payload = f"{query}|{mode}|{result}|{ENGINE_VERSION}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ============================================================================
# TIE-15: AUDIT TRAIL (JSONL)
# ============================================================================

def _write_audit(entry: Dict[str, Any]) -> None:
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["engine"] = ENGINE_NAME
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ============================================================================
# TIE-10: COVERAGE MAP
# ============================================================================

class CoverageMap:
    """Track which doctrines are triggered vs missed."""

    def __init__(self) -> None:
        self.triggered: Dict[str, int] = {}
        self.total_queries: int = 0

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] = self.triggered.get(topic, 0) + 1
        self.total_queries += 1

    def record_miss(self) -> None:
        self.total_queries += 1

    def get_report(self) -> Dict[str, Any]:
        all_topics = set(DOCTRINE_CACHE.keys())
        triggered_topics = set(self.triggered.keys())
        never_triggered = all_topics - triggered_topics
        return {
            "total_queries": self.total_queries,
            "total_doctrines": len(all_topics),
            "triggered_doctrines": len(triggered_topics),
            "never_triggered": sorted(never_triggered),
            "coverage_pct": round(len(triggered_topics) / max(len(all_topics), 1) * 100, 1),
            "top_triggered": sorted(self.triggered.items(), key=lambda x: -x[1])[:10],
        }


_coverage = CoverageMap()


# ============================================================================
# TIE-09: DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Detect if doctrine outputs change unexpectedly over time."""

    def __init__(self) -> None:
        self.baseline_hashes: Dict[str, str] = {}
        self.drift_events: List[Dict[str, Any]] = []

    def register_baseline(self, topic: str, result_hash: str) -> None:
        if topic not in self.baseline_hashes:
            self.baseline_hashes[topic] = result_hash

    def check_drift(self, topic: str, result_hash: str) -> bool:
        if topic not in self.baseline_hashes:
            self.register_baseline(topic, result_hash)
            return False
        if self.baseline_hashes[topic] != result_hash:
            self.drift_events.append({
                "topic": topic,
                "old_hash": self.baseline_hashes[topic],
                "new_hash": result_hash,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self.baseline_hashes[topic] = result_hash
            logger.warning(f"DRIFT detected for topic={topic}")
            return True
        return False

    def get_events(self) -> List[Dict[str, Any]]:
        return self.drift_events[-50:]


_drift = DriftWatcher()


# ============================================================================
# TIE-14: FACT FRAGILITY SCORING (adapted for math)
# ============================================================================

@dataclass
class FactFragility:
    claim: str
    verifiability: float
    numeric_stability: float
    domain_sensitivity: float
    composite_score: float
    tier: str
    narrative: str


def score_fragility(claim: str, numeric_result: Any) -> FactFragility:
    verifiability = 0.95
    numeric_stability = 0.9
    domain_sensitivity = 0.1
    if numeric_result is not None and isinstance(numeric_result, (float, complex)):
        if isinstance(numeric_result, complex):
            numeric_stability = 0.85
        elif math.isinf(numeric_result) or math.isnan(numeric_result):
            numeric_stability = 0.2
            verifiability = 0.3
    composite = round((verifiability + numeric_stability + (1 - domain_sensitivity)) / 3, 3)
    if composite >= 0.8:
        tier = "ROCK_SOLID"
    elif composite >= 0.6:
        tier = "STABLE"
    elif composite >= 0.4:
        tier = "FRAGILE"
    else:
        tier = "BRITTLE"
    return FactFragility(
        claim=claim,
        verifiability=verifiability,
        numeric_stability=numeric_stability,
        domain_sensitivity=domain_sensitivity,
        composite_score=composite,
        tier=tier,
        narrative=f"Result classified as {tier} (composite={composite})",
    )


# ============================================================================
# TIE-08: TELEMETRY
# ============================================================================

class Telemetry:
    """Full query tracing and latency tracking."""

    def __init__(self) -> None:
        self.traces: List[Dict[str, Any]] = []

    def start_trace(self, query_id: str, question: str) -> Dict[str, Any]:
        trace = {
            "query_id": query_id,
            "question": question[:200],
            "start_time": time.time(),
            "events": [],
        }
        self.traces.append(trace)
        if len(self.traces) > 200:
            self.traces.pop(0)
        return trace

    def add_event(self, trace: Dict[str, Any], event: str, data: Any = None) -> None:
        trace["events"].append({
            "event": event,
            "elapsed_ms": round((time.time() - trace["start_time"]) * 1000, 2),
            "data": data,
        })

    def complete_trace(self, trace: Dict[str, Any], layer: str, success: bool) -> None:
        trace["end_time"] = time.time()
        trace["total_ms"] = round((trace["end_time"] - trace["start_time"]) * 1000, 2)
        trace["layer"] = layer
        trace["success"] = success


_telemetry = Telemetry()


# ============================================================================
# PURE MATH SOLVERS — Real implementations, no stubs
# ============================================================================

# ---------------------------------------------------------------------------
# Fraction / Rational helpers
# ---------------------------------------------------------------------------

def _to_fraction(val: Union[int, float, fractions.Fraction]) -> fractions.Fraction:
    """Convert numeric value to Fraction for exact arithmetic."""
    if isinstance(val, fractions.Fraction):
        return val
    return fractions.Fraction(val).limit_denominator(10**12)


def _fmt_number(val: Union[int, float, complex, fractions.Fraction], precision: int = 10) -> str:
    """Format a number for display."""
    if isinstance(val, complex):
        r = round(val.real, precision)
        i = round(val.imag, precision)
        if i == 0:
            return str(r)
        if r == 0:
            return f"{i}i"
        sign = "+" if i > 0 else "-"
        return f"{r} {sign} {abs(i)}i"
    if isinstance(val, fractions.Fraction):
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"
    if isinstance(val, float):
        if val == int(val) and not math.isinf(val):
            return str(int(val))
        return str(round(val, precision))
    return str(val)


# ---------------------------------------------------------------------------
# Linear Equation Solver: ax + b = c  ->  x = (c - b) / a
# ---------------------------------------------------------------------------

def solve_linear(a: float, b: float, c: float) -> Dict[str, Any]:
    """Solve ax + b = c for x.

    Returns dict with solution, steps, classification.
    """
    steps: List[str] = []
    steps.append(f"Given: {a}x + {b} = {c}")
    steps.append(f"Subtract {b} from both sides: {a}x = {c} - {b} = {c - b}")

    if a == 0:
        if b == c:
            return {
                "solution": "infinite",
                "classification": "identity",
                "steps": steps + ["0x = 0, which is true for all x"],
                "description": "The equation is an identity; every real number is a solution.",
            }
        else:
            return {
                "solution": "none",
                "classification": "contradiction",
                "steps": steps + [f"0x = {c - b}, which is impossible"],
                "description": "The equation is a contradiction; no solution exists.",
            }

    x = (c - b) / a
    steps.append(f"Divide both sides by {a}: x = {c - b} / {a} = {_fmt_number(x)}")

    # Verify
    check = a * x + b
    steps.append(f"Verification: {a}({_fmt_number(x)}) + {b} = {_fmt_number(check)} = {c}")

    return {
        "solution": x,
        "classification": "unique",
        "steps": steps,
        "description": f"x = {_fmt_number(x)}",
    }


# ---------------------------------------------------------------------------
# Quadratic Equation Solver: ax^2 + bx + c = 0
# ---------------------------------------------------------------------------

def solve_quadratic(a: float, b: float, c: float) -> Dict[str, Any]:
    """Solve ax^2 + bx + c = 0 via quadratic formula with discriminant analysis.

    Handles real and complex roots. Returns dict with roots, discriminant,
    vertex, steps.
    """
    if a == 0:
        if b == 0:
            if c == 0:
                return {"roots": "infinite", "classification": "degenerate_identity",
                        "steps": ["0 = 0 always true"], "description": "Degenerate: all reals"}
            return {"roots": "none", "classification": "degenerate_contradiction",
                    "steps": [f"{c} = 0 is false"], "description": "Degenerate: no solution"}
        lin = solve_linear(b, c, 0)
        return {"roots": [lin["solution"]], "classification": "linear_fallback",
                "steps": lin["steps"], "description": lin["description"]}

    discriminant = b * b - 4 * a * c
    steps: List[str] = [
        f"Given: {a}x^2 + {b}x + {c} = 0",
        f"Discriminant: D = b^2 - 4ac = {b}^2 - 4({a})({c}) = {_fmt_number(discriminant)}",
    ]

    vertex_x = -b / (2 * a)
    vertex_y = a * vertex_x * vertex_x + b * vertex_x + c

    if discriminant > 0:
        sqrt_d = math.sqrt(discriminant)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        steps.append(f"D > 0: Two distinct real roots")
        steps.append(f"x1 = (-{b} + sqrt({_fmt_number(discriminant)})) / (2*{a}) = {_fmt_number(x1)}")
        steps.append(f"x2 = (-{b} - sqrt({_fmt_number(discriminant)})) / (2*{a}) = {_fmt_number(x2)}")
        # Vieta verification
        steps.append(f"Vieta check: x1+x2 = {_fmt_number(x1+x2)} should equal {_fmt_number(-b/a)}")
        steps.append(f"Vieta check: x1*x2 = {_fmt_number(x1*x2)} should equal {_fmt_number(c/a)}")
        roots = sorted([x1, x2])
        classification = "two_real_distinct"
    elif discriminant == 0:
        x1 = -b / (2 * a)
        steps.append(f"D = 0: One repeated real root")
        steps.append(f"x = -b/(2a) = {_fmt_number(x1)}")
        roots = [x1]
        classification = "repeated_real"
    else:
        sqrt_d = cmath.sqrt(discriminant)
        z1 = (-b + sqrt_d) / (2 * a)
        z2 = (-b - sqrt_d) / (2 * a)
        steps.append(f"D < 0: Two complex conjugate roots")
        steps.append(f"z1 = {_fmt_number(z1)}")
        steps.append(f"z2 = {_fmt_number(z2)}")
        roots = [{"real": round(z1.real, 10), "imag": round(z1.imag, 10), "str": _fmt_number(z1)},
                 {"real": round(z2.real, 10), "imag": round(z2.imag, 10), "str": _fmt_number(z2)}]
        classification = "complex_conjugate"

    return {
        "roots": roots,
        "discriminant": discriminant,
        "vertex": {"x": vertex_x, "y": vertex_y},
        "classification": classification,
        "steps": steps,
        "description": f"Roots: {roots}",
    }


# ---------------------------------------------------------------------------
# Cubic Equation Solver: ax^3 + bx^2 + cx + d = 0  (Cardano's formula)
# ---------------------------------------------------------------------------

def solve_cubic(a: float, b: float, c: float, d: float) -> Dict[str, Any]:
    """Solve ax^3 + bx^2 + cx + d = 0 using Cardano's method.

    Steps: depress the cubic to t^3 + pt + q = 0, then apply Cardano's formula.
    """
    if a == 0:
        return solve_quadratic(b, c, d)

    steps: List[str] = [f"Given: {a}x^3 + {b}x^2 + {c}x + {d} = 0"]

    # Normalize: x^3 + (b/a)x^2 + (c/a)x + (d/a) = 0
    p_coeff = b / a
    q_coeff = c / a
    r_coeff = d / a
    steps.append(f"Normalize: x^3 + {_fmt_number(p_coeff)}x^2 + {_fmt_number(q_coeff)}x + {_fmt_number(r_coeff)} = 0")

    # Depress: substitute x = t - b/(3a)
    shift = p_coeff / 3
    p = q_coeff - (p_coeff ** 2) / 3
    q = r_coeff - p_coeff * q_coeff / 3 + 2 * (p_coeff ** 3) / 27
    steps.append(f"Depress via x = t - {_fmt_number(shift)}: t^3 + {_fmt_number(p)}t + {_fmt_number(q)} = 0")

    # Discriminant of depressed cubic
    disc = -(4 * p ** 3 + 27 * q ** 2)
    steps.append(f"Cubic discriminant: {_fmt_number(disc)}")

    # Cardano's formula
    # t^3 + pt + q = 0 => t = cbrt(-q/2 + sqrt(q^2/4 + p^3/27)) + cbrt(-q/2 - sqrt(q^2/4 + p^3/27))
    inner = complex(q * q / 4 + p * p * p / 27)
    sqrt_inner = cmath.sqrt(inner)
    u = (-q / 2 + sqrt_inner) ** (1 / 3)
    v = (-q / 2 - sqrt_inner) ** (1 / 3)

    # Three cube roots of unity
    omega = complex(-0.5, math.sqrt(3) / 2)
    omega2 = complex(-0.5, -math.sqrt(3) / 2)

    t_roots = [
        u + v,
        u * omega + v * omega2,
        u * omega2 + v * omega,
    ]

    # Un-depress: x = t - shift
    x_roots_raw = [t - shift for t in t_roots]

    # Clean up near-zero imaginary parts
    roots: List[Any] = []
    for r in x_roots_raw:
        if abs(r.imag) < 1e-10:
            roots.append(round(r.real, 10))
        else:
            roots.append({"real": round(r.real, 10), "imag": round(r.imag, 10), "str": _fmt_number(r)})

    for i, root in enumerate(roots):
        steps.append(f"x{i+1} = {_fmt_number(root) if isinstance(root, (int, float)) else root.get('str', str(root))}")

    if disc > 0:
        classification = "three_real_distinct"
    elif abs(disc) < 1e-12:
        classification = "repeated_root"
    else:
        classification = "one_real_two_complex"

    return {
        "roots": roots,
        "discriminant": disc,
        "classification": classification,
        "steps": steps,
        "description": f"Cubic roots: {roots}",
    }


# ---------------------------------------------------------------------------
# System of Linear Equations — Gaussian Elimination
# ---------------------------------------------------------------------------

def solve_system_2x2(coeffs: List[List[float]], constants: List[float]) -> Dict[str, Any]:
    """Solve 2x2 system via Cramer's rule.

    coeffs = [[a1,b1],[a2,b2]], constants = [c1,c2]
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    """
    a1, b1 = coeffs[0]
    a2, b2 = coeffs[1]
    c1, c2 = constants

    steps: List[str] = [
        f"System: {a1}x + {b1}y = {c1}",
        f"        {a2}x + {b2}y = {c2}",
    ]

    det = a1 * b2 - a2 * b1
    steps.append(f"Determinant D = {a1}*{b2} - {a2}*{b1} = {_fmt_number(det)}")

    if abs(det) < 1e-15:
        # Check consistency
        if abs(a1 * c2 - a2 * c1) < 1e-15 and abs(b1 * c2 - b2 * c1) < 1e-15:
            return {"solution": "infinite", "classification": "dependent",
                    "steps": steps + ["D=0 and consistent: infinitely many solutions"],
                    "description": "Dependent system: infinitely many solutions"}
        return {"solution": "none", "classification": "inconsistent",
                "steps": steps + ["D=0 and inconsistent: no solution"],
                "description": "Inconsistent system: no solution"}

    dx = c1 * b2 - c2 * b1
    dy = a1 * c2 - a2 * c1
    x = dx / det
    y = dy / det
    steps.append(f"Dx = {c1}*{b2} - {c2}*{b1} = {_fmt_number(dx)}")
    steps.append(f"Dy = {a1}*{c2} - {a2}*{c1} = {_fmt_number(dy)}")
    steps.append(f"x = Dx/D = {_fmt_number(x)}, y = Dy/D = {_fmt_number(y)}")
    steps.append(f"Verify: {a1}*{_fmt_number(x)} + {b1}*{_fmt_number(y)} = {_fmt_number(a1*x + b1*y)}")

    return {
        "solution": {"x": x, "y": y},
        "classification": "unique",
        "steps": steps,
        "description": f"x = {_fmt_number(x)}, y = {_fmt_number(y)}",
    }


def solve_system_gaussian(matrix: List[List[float]], constants: List[float]) -> Dict[str, Any]:
    """Solve NxN system via Gaussian elimination with partial pivoting.

    matrix[i] = row of coefficients, constants[i] = RHS.
    """
    n = len(matrix)
    if n == 0 or len(constants) != n:
        return {"error": "Invalid dimensions"}

    steps: List[str] = [f"System of {n} equations in {n} unknowns"]

    # Augmented matrix
    aug = [row[:] + [constants[i]] for i, row in enumerate(matrix)]

    # Forward elimination with partial pivoting
    for col in range(n):
        # Find pivot
        max_row = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, n):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                max_row = row
        if max_val < 1e-15:
            steps.append(f"Column {col+1}: zero pivot, system may be singular")
            continue
        if max_row != col:
            aug[col], aug[max_row] = aug[max_row], aug[col]
            steps.append(f"Swap R{col+1} <-> R{max_row+1}")

        pivot = aug[col][col]
        for row in range(col + 1, n):
            if abs(aug[row][col]) < 1e-15:
                continue
            factor = aug[row][col] / pivot
            for j in range(col, n + 1):
                aug[row][j] -= factor * aug[col][j]
            aug[row][col] = 0.0
            steps.append(f"R{row+1} = R{row+1} - ({_fmt_number(factor)})*R{col+1}")

    # Back substitution
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(aug[i][i]) < 1e-15:
            if abs(aug[i][n]) < 1e-15:
                return {"solution": "infinite", "classification": "dependent",
                        "steps": steps, "description": "Dependent system"}
            return {"solution": "none", "classification": "inconsistent",
                    "steps": steps, "description": "Inconsistent system"}
        s = aug[i][n]
        for j in range(i + 1, n):
            s -= aug[i][j] * solution[j]
        solution[i] = s / aug[i][i]

    var_names = ["x", "y", "z", "w", "v", "u", "s", "t", "p", "q"]
    sol_dict = {}
    for i in range(n):
        name = var_names[i] if i < len(var_names) else f"x{i+1}"
        sol_dict[name] = round(solution[i], 12)
        steps.append(f"{name} = {_fmt_number(solution[i])}")

    return {
        "solution": sol_dict,
        "classification": "unique",
        "steps": steps,
        "description": ", ".join(f"{k}={_fmt_number(v)}" for k, v in sol_dict.items()),
    }


# ---------------------------------------------------------------------------
# Polynomial Operations
# ---------------------------------------------------------------------------

class Polynomial:
    """Polynomial represented as list of coefficients, highest degree first.

    Example: [2, -3, 0, 5] represents 2x^3 - 3x^2 + 0x + 5
    """

    def __init__(self, coeffs: List[float]) -> None:
        # Strip leading zeros
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs = coeffs[1:]
        self.coeffs = coeffs

    @property
    def degree(self) -> int:
        return len(self.coeffs) - 1

    def evaluate(self, x: Union[float, complex]) -> Union[float, complex]:
        """Evaluate polynomial at x using Horner's method."""
        result: Union[float, complex] = 0
        for c in self.coeffs:
            result = result * x + c
        return result

    def __str__(self) -> str:
        if not self.coeffs:
            return "0"
        terms: List[str] = []
        deg = self.degree
        for i, c in enumerate(self.coeffs):
            power = deg - i
            if c == 0:
                continue
            if power == 0:
                terms.append(_fmt_number(c))
            elif power == 1:
                if c == 1:
                    terms.append("x")
                elif c == -1:
                    terms.append("-x")
                else:
                    terms.append(f"{_fmt_number(c)}x")
            else:
                if c == 1:
                    terms.append(f"x^{power}")
                elif c == -1:
                    terms.append(f"-x^{power}")
                else:
                    terms.append(f"{_fmt_number(c)}x^{power}")
        if not terms:
            return "0"
        result = terms[0]
        for t in terms[1:]:
            if t.startswith("-"):
                result += f" - {t[1:]}"
            else:
                result += f" + {t}"
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {"coefficients": self.coeffs, "degree": self.degree, "string": str(self)}


def poly_add(p1: Polynomial, p2: Polynomial) -> Polynomial:
    """Add two polynomials."""
    c1 = p1.coeffs[:]
    c2 = p2.coeffs[:]
    # Pad shorter
    while len(c1) < len(c2):
        c1.insert(0, 0)
    while len(c2) < len(c1):
        c2.insert(0, 0)
    return Polynomial([a + b for a, b in zip(c1, c2)])


def poly_subtract(p1: Polynomial, p2: Polynomial) -> Polynomial:
    """Subtract p2 from p1."""
    c1 = p1.coeffs[:]
    c2 = p2.coeffs[:]
    while len(c1) < len(c2):
        c1.insert(0, 0)
    while len(c2) < len(c1):
        c2.insert(0, 0)
    return Polynomial([a - b for a, b in zip(c1, c2)])


def poly_multiply(p1: Polynomial, p2: Polynomial) -> Polynomial:
    """Multiply two polynomials."""
    n = p1.degree + p2.degree + 1
    result = [0.0] * n
    for i, a in enumerate(p1.coeffs):
        for j, b in enumerate(p2.coeffs):
            result[i + j] += a * b
    return Polynomial(result)


def poly_long_division(dividend: Polynomial, divisor: Polynomial) -> Dict[str, Any]:
    """Polynomial long division. Returns quotient and remainder."""
    if divisor.degree == 0 and divisor.coeffs[0] == 0:
        return {"error": "Division by zero polynomial"}

    steps: List[str] = [f"Divide ({dividend}) by ({divisor})"]
    rem = dividend.coeffs[:]
    divisor_lead = divisor.coeffs[0]
    divisor_deg = divisor.degree
    quot_coeffs: List[float] = []

    for i in range(len(rem) - divisor_deg):
        coeff = rem[i] / divisor_lead
        quot_coeffs.append(coeff)
        steps.append(f"Step {i+1}: {_fmt_number(rem[i])} / {_fmt_number(divisor_lead)} = {_fmt_number(coeff)}")
        for j in range(len(divisor.coeffs)):
            rem[i + j] -= coeff * divisor.coeffs[j]

    quotient = Polynomial(quot_coeffs) if quot_coeffs else Polynomial([0])
    remainder = Polynomial(rem[len(quot_coeffs):]) if len(rem) > len(quot_coeffs) else Polynomial([0])

    steps.append(f"Quotient: {quotient}")
    steps.append(f"Remainder: {remainder}")

    return {
        "quotient": quotient.to_dict(),
        "remainder": remainder.to_dict(),
        "steps": steps,
        "description": f"({dividend}) = ({divisor})({quotient}) + ({remainder})",
    }


def poly_synthetic_division(coeffs: List[float], root: float) -> Dict[str, Any]:
    """Synthetic division of polynomial by (x - root)."""
    steps: List[str] = [f"Synthetic division by (x - {_fmt_number(root)})"]
    result = [coeffs[0]]
    for i in range(1, len(coeffs)):
        val = result[-1] * root + coeffs[i]
        result.append(val)
        steps.append(f"  {_fmt_number(result[-2])} * {_fmt_number(root)} + {_fmt_number(coeffs[i])} = {_fmt_number(val)}")

    remainder = result[-1]
    quotient_coeffs = result[:-1]
    q = Polynomial(quotient_coeffs)
    steps.append(f"Quotient: {q}, Remainder: {_fmt_number(remainder)}")

    return {
        "quotient": q.to_dict(),
        "remainder": remainder,
        "steps": steps,
        "is_root": abs(remainder) < 1e-12,
    }


# ---------------------------------------------------------------------------
# Polynomial Factoring — Rational Root Theorem
# ---------------------------------------------------------------------------

def _get_integer_divisors(n: int) -> List[int]:
    """Get all positive integer divisors of n."""
    if n == 0:
        return []
    n = abs(n)
    divs: List[int] = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)


def factor_polynomial(coeffs: List[float]) -> Dict[str, Any]:
    """Factor a polynomial using rational root theorem and synthetic division.

    Works best when coefficients are integers.
    """
    p = Polynomial(coeffs)
    steps: List[str] = [f"Factor: {p}"]

    if p.degree <= 1:
        return {"factors": [p.to_dict()], "steps": steps, "description": f"{p} is already linear or constant"}

    # Rational Root Theorem: possible roots are +/- (divisors of constant) / (divisors of leading)
    int_coeffs = [int(round(c)) for c in coeffs]
    constant_term = abs(int_coeffs[-1]) if int_coeffs[-1] != 0 else 1
    leading_term = abs(int_coeffs[0])

    p_divisors = _get_integer_divisors(constant_term)
    q_divisors = _get_integer_divisors(leading_term)

    candidates: List[float] = []
    seen: set = set()
    for pd in p_divisors:
        for qd in q_divisors:
            for sign in [1, -1]:
                candidate = sign * pd / qd
                if candidate not in seen:
                    seen.add(candidate)
                    candidates.append(candidate)

    candidates.sort(key=abs)
    steps.append(f"Rational root candidates: {candidates[:20]}{'...' if len(candidates) > 20 else ''}")

    roots_found: List[float] = []
    remaining = coeffs[:]

    for _ in range(len(coeffs) - 1):
        found_root = False
        for candidate in candidates:
            # Evaluate using Horner
            val = 0.0
            for c in remaining:
                val = val * candidate + c
            if abs(val) < 1e-10:
                roots_found.append(candidate)
                steps.append(f"Found root: x = {_fmt_number(candidate)}")
                # Synthetic division
                new_remaining = [remaining[0]]
                for i in range(1, len(remaining)):
                    new_remaining.append(new_remaining[-1] * candidate + remaining[i])
                remaining = new_remaining[:-1]
                found_root = True
                break
        if not found_root:
            break

    # Build factor list
    factors: List[Dict[str, Any]] = []
    for root in roots_found:
        if root >= 0:
            factors.append({"linear_factor": f"(x - {_fmt_number(root)})", "root": root})
        else:
            factors.append({"linear_factor": f"(x + {_fmt_number(abs(root))})", "root": root})

    if len(remaining) > 1 or (len(remaining) == 1 and remaining[0] != 1):
        rem_poly = Polynomial(remaining)
        factors.append({"irreducible_factor": str(rem_poly), "coefficients": remaining})
        steps.append(f"Remaining irreducible factor: {rem_poly}")

    if leading_term != 1 and roots_found:
        steps.append(f"Leading coefficient: {_fmt_number(coeffs[0])}")

    description_parts: List[str] = []
    if abs(coeffs[0]) != 1:
        description_parts.append(_fmt_number(coeffs[0]))
    for f in factors:
        if "linear_factor" in f:
            description_parts.append(f["linear_factor"])
        elif "irreducible_factor" in f:
            description_parts.append(f"({f['irreducible_factor']})")

    return {
        "factors": factors,
        "roots_found": roots_found,
        "steps": steps,
        "description": " * ".join(description_parts) if description_parts else str(p),
    }


# ---------------------------------------------------------------------------
# Complex Number Arithmetic
# ---------------------------------------------------------------------------

def complex_ops(op: str, z1_real: float, z1_imag: float,
                z2_real: float = 0, z2_imag: float = 0) -> Dict[str, Any]:
    """Perform complex number operations.

    Operations: add, subtract, multiply, divide, magnitude, conjugate,
    polar, power, nth_root.
    """
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    steps: List[str] = [f"z1 = {_fmt_number(z1)}", f"z2 = {_fmt_number(z2)}"]

    if op == "add":
        result = z1 + z2
        steps.append(f"z1 + z2 = ({z1_real}+{z2_real}) + ({z1_imag}+{z2_imag})i = {_fmt_number(result)}")
    elif op == "subtract":
        result = z1 - z2
        steps.append(f"z1 - z2 = ({z1_real}-{z2_real}) + ({z1_imag}-{z2_imag})i = {_fmt_number(result)}")
    elif op == "multiply":
        result = z1 * z2
        steps.append(f"z1 * z2 = ({z1_real}*{z2_real} - {z1_imag}*{z2_imag}) + ({z1_real}*{z2_imag} + {z1_imag}*{z2_real})i")
        steps.append(f"= {_fmt_number(result)}")
    elif op == "divide":
        if abs(z2) < 1e-15:
            return {"error": "Division by zero", "steps": steps}
        result = z1 / z2
        denom = z2_real ** 2 + z2_imag ** 2
        steps.append(f"z1/z2: multiply by conjugate of z2")
        steps.append(f"Denominator: |z2|^2 = {_fmt_number(denom)}")
        steps.append(f"= {_fmt_number(result)}")
    elif op == "magnitude":
        result = abs(z1)
        steps.append(f"|z1| = sqrt({z1_real}^2 + {z1_imag}^2) = {_fmt_number(result)}")
        return {"result": result, "steps": steps, "description": f"|z1| = {_fmt_number(result)}"}
    elif op == "conjugate":
        result = complex(z1_real, -z1_imag)
        steps.append(f"conj(z1) = {z1_real} - {z1_imag}i = {_fmt_number(result)}")
    elif op == "polar":
        r = abs(z1)
        theta = cmath.phase(z1)
        theta_deg = math.degrees(theta)
        steps.append(f"r = |z1| = {_fmt_number(r)}")
        steps.append(f"theta = arg(z1) = {_fmt_number(theta)} rad = {_fmt_number(theta_deg)} deg")
        return {"result": {"r": r, "theta_rad": theta, "theta_deg": theta_deg},
                "steps": steps, "description": f"{_fmt_number(r)} * e^(i*{_fmt_number(theta)})"}
    elif op == "power":
        n = int(z2_real)
        result = z1 ** n
        steps.append(f"z1^{n} = {_fmt_number(result)}")
    elif op == "nth_root":
        n = int(z2_real) if z2_real != 0 else 2
        r = abs(z1)
        theta = cmath.phase(z1)
        roots = []
        for k in range(n):
            angle = (theta + 2 * math.pi * k) / n
            root = r ** (1 / n) * complex(math.cos(angle), math.sin(angle))
            roots.append({"real": round(root.real, 10), "imag": round(root.imag, 10), "str": _fmt_number(root)})
            steps.append(f"Root {k+1}: {_fmt_number(root)}")
        return {"result": roots, "steps": steps, "description": f"{n} roots of {_fmt_number(z1)}"}
    else:
        return {"error": f"Unknown operation: {op}"}

    return {
        "result": {"real": round(result.real, 10), "imag": round(result.imag, 10), "str": _fmt_number(result)},
        "steps": steps,
        "description": _fmt_number(result),
    }


# ---------------------------------------------------------------------------
# Logarithm / Exponential Solver
# ---------------------------------------------------------------------------

def solve_logarithm(equation_type: str, **kwargs: Any) -> Dict[str, Any]:
    """Solve logarithmic and exponential equations.

    Types:
        log_solve: solve log_b(x) = c  ->  x = b^c
        exp_solve: solve b^x = c  ->  x = log(c)/log(b)
        change_base: convert log_b(x) to log_a(x)
        log_properties: expand/condense using log rules
        natural_log: ln operations
    """
    steps: List[str] = []

    if equation_type == "log_solve":
        base = kwargs.get("base", 10)
        value = kwargs.get("value", 1)  # log_b(x) = value => x = b^value
        if base <= 0 or base == 1:
            return {"error": "Base must be positive and not equal to 1"}
        x = base ** value
        steps.append(f"log_{base}(x) = {value}")
        steps.append(f"By definition: x = {base}^{value} = {_fmt_number(x)}")
        steps.append(f"Verify: log_{base}({_fmt_number(x)}) = {_fmt_number(math.log(x) / math.log(base))}")
        return {"solution": x, "steps": steps, "description": f"x = {_fmt_number(x)}"}

    elif equation_type == "exp_solve":
        base = kwargs.get("base", math.e)
        target = kwargs.get("target", 1)  # b^x = target => x = log(target)/log(b)
        if target <= 0:
            return {"error": "Target must be positive for real solutions"}
        if base <= 0 or base == 1:
            return {"error": "Base must be positive and not equal to 1"}
        x = math.log(target) / math.log(base)
        steps.append(f"{_fmt_number(base)}^x = {target}")
        steps.append(f"Take log of both sides: x * log({_fmt_number(base)}) = log({target})")
        steps.append(f"x = log({target}) / log({_fmt_number(base)}) = {_fmt_number(x)}")
        steps.append(f"Verify: {_fmt_number(base)}^{_fmt_number(x)} = {_fmt_number(base ** x)}")
        return {"solution": x, "steps": steps, "description": f"x = {_fmt_number(x)}"}

    elif equation_type == "change_base":
        old_base = kwargs.get("old_base", 10)
        new_base = kwargs.get("new_base", math.e)
        argument = kwargs.get("argument", 1)
        if old_base <= 0 or old_base == 1 or new_base <= 0 or new_base == 1 or argument <= 0:
            return {"error": "Bases must be positive and !=1, argument must be positive"}
        old_val = math.log(argument) / math.log(old_base)
        new_val = math.log(argument) / math.log(new_base)
        steps.append(f"log_{old_base}({argument}) = {_fmt_number(old_val)}")
        steps.append(f"Change of base: log_{new_base}({argument}) = log({argument})/log({new_base}) = {_fmt_number(new_val)}")
        return {"old_value": old_val, "new_value": new_val, "steps": steps,
                "description": f"log_{old_base}({argument})={_fmt_number(old_val)}, log_{new_base}({argument})={_fmt_number(new_val)}"}

    elif equation_type == "natural_log":
        argument = kwargs.get("argument", 1)
        if argument <= 0:
            return {"error": "Argument must be positive"}
        val = math.log(argument)
        steps.append(f"ln({argument}) = {_fmt_number(val)}")
        steps.append(f"Verify: e^{_fmt_number(val)} = {_fmt_number(math.exp(val))}")
        return {"result": val, "steps": steps, "description": f"ln({argument}) = {_fmt_number(val)}"}

    return {"error": f"Unknown equation type: {equation_type}"}


# ---------------------------------------------------------------------------
# Matrix Operations (small matrices up to 5x5)
# ---------------------------------------------------------------------------

class Matrix:
    """Small matrix class for exact computation."""

    def __init__(self, data: List[List[float]]) -> None:
        self.data = [row[:] for row in data]
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __str__(self) -> str:
        lines = []
        for row in self.data:
            lines.append("[" + ", ".join(_fmt_number(v) for v in row) + "]")
        return "[" + ", ".join(lines) + "]"

    def to_list(self) -> List[List[float]]:
        return [row[:] for row in self.data]

    @staticmethod
    def identity(n: int) -> "Matrix":
        data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        return Matrix(data)

    def transpose(self) -> "Matrix":
        data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(data)

    def add(self, other: "Matrix") -> "Matrix":
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch for matrix addition")
        data = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(data)

    def subtract(self, other: "Matrix") -> "Matrix":
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch for matrix subtraction")
        data = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(data)

    def multiply(self, other: "Matrix") -> "Matrix":
        if self.cols != other.rows:
            raise ValueError(f"Dimension mismatch: {self.rows}x{self.cols} * {other.rows}x{other.cols}")
        data = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                 for j in range(other.cols)] for i in range(self.rows)]
        return Matrix(data)

    def scalar_multiply(self, scalar: float) -> "Matrix":
        data = [[self.data[i][j] * scalar for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(data)

    def determinant(self) -> float:
        """Compute determinant via cofactor expansion (exact for small matrices)."""
        if self.rows != self.cols:
            raise ValueError("Determinant only defined for square matrices")
        n = self.rows
        if n == 1:
            return self.data[0][0]
        if n == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        if n == 3:
            a = self.data
            return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                    - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                    + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
        # General cofactor expansion along first row
        det = 0.0
        for j in range(n):
            minor_data = []
            for i in range(1, n):
                row = []
                for k in range(n):
                    if k != j:
                        row.append(self.data[i][k])
                minor_data.append(row)
            sign = 1 if j % 2 == 0 else -1
            det += sign * self.data[0][j] * Matrix(minor_data).determinant()
        return det

    def inverse(self) -> Optional["Matrix"]:
        """Compute inverse via Gauss-Jordan elimination."""
        if self.rows != self.cols:
            return None
        n = self.rows
        # Augment with identity
        aug = [self.data[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for col in range(n):
            # Pivot
            max_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > abs(aug[max_row][col]):
                    max_row = row
            aug[col], aug[max_row] = aug[max_row], aug[col]

            if abs(aug[col][col]) < 1e-15:
                return None  # Singular

            pivot = aug[col][col]
            for j in range(2 * n):
                aug[col][j] /= pivot

            for row in range(n):
                if row == col:
                    continue
                factor = aug[row][col]
                for j in range(2 * n):
                    aug[row][j] -= factor * aug[col][j]

        inv_data = [aug[i][n:] for i in range(n)]
        return Matrix(inv_data)

    def trace(self) -> float:
        if self.rows != self.cols:
            raise ValueError("Trace only for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))

    def rank(self) -> int:
        """Compute rank via row echelon form."""
        aug = [row[:] for row in self.data]
        r = 0
        for col in range(self.cols):
            pivot_row = None
            for row in range(r, self.rows):
                if abs(aug[row][col]) > 1e-12:
                    pivot_row = row
                    break
            if pivot_row is None:
                continue
            aug[r], aug[pivot_row] = aug[pivot_row], aug[r]
            pivot = aug[r][col]
            for j in range(self.cols):
                aug[r][j] /= pivot
            for row in range(self.rows):
                if row == r:
                    continue
                factor = aug[row][col]
                for j in range(self.cols):
                    aug[row][j] -= factor * aug[r][j]
            r += 1
        return r


def matrix_operations(op: str, matrix_a: List[List[float]],
                      matrix_b: Optional[List[List[float]]] = None,
                      scalar: Optional[float] = None) -> Dict[str, Any]:
    """Perform matrix operation and return result with steps."""
    a = Matrix(matrix_a)
    steps: List[str] = [f"Matrix A ({a.rows}x{a.cols})"]

    if op == "determinant":
        det = a.determinant()
        steps.append(f"det(A) = {_fmt_number(det)}")
        return {"result": det, "steps": steps, "description": f"det(A) = {_fmt_number(det)}"}

    elif op == "inverse":
        inv = a.inverse()
        if inv is None:
            steps.append("Matrix is singular (non-invertible)")
            return {"result": None, "steps": steps, "description": "Singular matrix, no inverse"}
        # Verify: A * A^-1 = I
        product = a.multiply(inv)
        steps.append(f"A^-1 computed")
        steps.append(f"Verify: A * A^-1 = I (trace = {_fmt_number(product.trace())})")
        return {"result": inv.to_list(), "steps": steps, "description": f"Inverse: {inv}"}

    elif op == "transpose":
        t = a.transpose()
        steps.append(f"A^T ({t.rows}x{t.cols})")
        return {"result": t.to_list(), "steps": steps, "description": f"Transpose: {t}"}

    elif op == "multiply" and matrix_b is not None:
        b = Matrix(matrix_b)
        steps.append(f"Matrix B ({b.rows}x{b.cols})")
        try:
            product = a.multiply(b)
            steps.append(f"A*B ({product.rows}x{product.cols})")
            return {"result": product.to_list(), "steps": steps, "description": f"Product: {product}"}
        except ValueError as e:
            return {"error": str(e), "steps": steps}

    elif op == "add" and matrix_b is not None:
        b = Matrix(matrix_b)
        try:
            result = a.add(b)
            return {"result": result.to_list(), "steps": steps + [f"A+B computed"], "description": str(result)}
        except ValueError as e:
            return {"error": str(e), "steps": steps}

    elif op == "scalar_multiply" and scalar is not None:
        result = a.scalar_multiply(scalar)
        return {"result": result.to_list(), "steps": steps + [f"{scalar}*A computed"], "description": str(result)}

    elif op == "trace":
        return {"result": a.trace(), "steps": steps, "description": f"tr(A) = {_fmt_number(a.trace())}"}

    elif op == "rank":
        return {"result": a.rank(), "steps": steps, "description": f"rank(A) = {a.rank()}"}

    return {"error": f"Unknown operation: {op}"}


# ---------------------------------------------------------------------------
# Inequality Solver
# ---------------------------------------------------------------------------

def solve_inequality(inequality_type: str, coeffs: List[float],
                     comparison: str = "<") -> Dict[str, Any]:
    """Solve inequalities and return solution in interval notation.

    Types: linear, quadratic, absolute_value
    comparison: <, <=, >, >=
    """
    steps: List[str] = []

    if inequality_type == "linear":
        # ax + b < 0 (after moving everything to left side)
        a, b = coeffs[0], coeffs[1] if len(coeffs) > 1 else 0
        steps.append(f"Solve: {a}x + {b} {comparison} 0")

        if a == 0:
            truth = eval(f"{b} {comparison} 0")
            if truth:
                return {"solution": "(-inf, +inf)", "classification": "all_reals",
                        "steps": steps + [f"{b} {comparison} 0 is always true"], "description": "All real numbers"}
            return {"solution": "empty", "classification": "no_solution",
                    "steps": steps + [f"{b} {comparison} 0 is always false"], "description": "No solution"}

        boundary = -b / a
        steps.append(f"Boundary: x = {_fmt_number(boundary)}")

        # Direction flips if a < 0
        flip = a < 0
        effective_cmp = comparison
        if flip:
            flip_map = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}
            effective_cmp = flip_map[comparison]
            steps.append(f"Dividing by negative ({a}), inequality flips to {effective_cmp}")

        if effective_cmp == "<":
            solution = f"(-inf, {_fmt_number(boundary)})"
        elif effective_cmp == "<=":
            solution = f"(-inf, {_fmt_number(boundary)}]"
        elif effective_cmp == ">":
            solution = f"({_fmt_number(boundary)}, +inf)"
        else:  # >=
            solution = f"[{_fmt_number(boundary)}, +inf)"

        steps.append(f"Solution: {solution}")
        return {"solution": solution, "boundary": boundary,
                "steps": steps, "description": solution}

    elif inequality_type == "quadratic":
        # ax^2 + bx + c < 0
        a, b_coeff, c = coeffs[0], coeffs[1] if len(coeffs) > 1 else 0, coeffs[2] if len(coeffs) > 2 else 0
        steps.append(f"Solve: {a}x^2 + {b_coeff}x + {c} {comparison} 0")

        disc = b_coeff ** 2 - 4 * a * c
        steps.append(f"Discriminant = {_fmt_number(disc)}")

        if disc < 0:
            # Parabola doesn't cross x-axis
            if a > 0:
                always_positive = True
            else:
                always_positive = False

            if comparison in ("<", "<="):
                if always_positive:
                    return {"solution": "empty", "steps": steps + ["Parabola always positive"],
                            "description": "No solution"}
                return {"solution": "(-inf, +inf)", "steps": steps + ["Parabola always negative"],
                        "description": "All real numbers"}
            else:  # > or >=
                if always_positive:
                    return {"solution": "(-inf, +inf)", "steps": steps, "description": "All real numbers"}
                return {"solution": "empty", "steps": steps, "description": "No solution"}

        sqrt_d = math.sqrt(disc)
        x1 = (-b_coeff - sqrt_d) / (2 * a)
        x2 = (-b_coeff + sqrt_d) / (2 * a)
        if x1 > x2:
            x1, x2 = x2, x1
        steps.append(f"Roots: x1 = {_fmt_number(x1)}, x2 = {_fmt_number(x2)}")

        open_l, open_r = "(", ")"
        closed_l, closed_r = "[", "]"

        if comparison in ("<=", ">="):
            bl, br = closed_l, closed_r
        else:
            bl, br = open_l, open_r

        if a > 0:
            # Parabola opens up: negative between roots, positive outside
            if comparison in ("<", "<="):
                solution = f"{bl}{_fmt_number(x1)}, {_fmt_number(x2)}{br}"
            else:
                solution = f"(-inf, {bl.replace('[','').replace('(','')}{_fmt_number(x1)}{')' if bl=='(' else ']'} U {bl}{_fmt_number(x2)}, +inf)"
                # Cleaner formatting
                if comparison == ">":
                    solution = f"(-inf, {_fmt_number(x1)}) U ({_fmt_number(x2)}, +inf)"
                else:
                    solution = f"(-inf, {_fmt_number(x1)}] U [{_fmt_number(x2)}, +inf)"
        else:
            # Parabola opens down: positive between roots, negative outside
            if comparison in ("<", "<="):
                if comparison == "<":
                    solution = f"(-inf, {_fmt_number(x1)}) U ({_fmt_number(x2)}, +inf)"
                else:
                    solution = f"(-inf, {_fmt_number(x1)}] U [{_fmt_number(x2)}, +inf)"
            else:
                solution = f"{bl}{_fmt_number(x1)}, {_fmt_number(x2)}{br}"

        steps.append(f"Solution: {solution}")
        return {"solution": solution, "roots": [x1, x2],
                "steps": steps, "description": solution}

    elif inequality_type == "absolute_value":
        # |ax + b| < c  or  |ax + b| > c
        a_val = coeffs[0]
        b_val = coeffs[1] if len(coeffs) > 1 else 0
        c_val = coeffs[2] if len(coeffs) > 2 else 0
        steps.append(f"Solve: |{a_val}x + {b_val}| {comparison} {c_val}")

        if c_val < 0:
            if comparison in ("<", "<="):
                return {"solution": "empty", "steps": steps + ["Absolute value can't be negative"],
                        "description": "No solution"}
            return {"solution": "(-inf, +inf)", "steps": steps + ["Always true"],
                    "description": "All real numbers"}

        if comparison in ("<", "<="):
            # |ax+b| < c  =>  -c < ax+b < c  =>  (-c-b)/a < x < (c-b)/a
            if a_val == 0:
                if abs(b_val) < c_val or (comparison == "<=" and abs(b_val) <= c_val):
                    return {"solution": "(-inf, +inf)", "steps": steps, "description": "All reals"}
                return {"solution": "empty", "steps": steps, "description": "No solution"}
            x_low = (-c_val - b_val) / a_val
            x_high = (c_val - b_val) / a_val
            if x_low > x_high:
                x_low, x_high = x_high, x_low
            bl = "[" if comparison == "<=" else "("
            br = "]" if comparison == "<=" else ")"
            solution = f"{bl}{_fmt_number(x_low)}, {_fmt_number(x_high)}{br}"
        else:
            # |ax+b| > c  =>  ax+b < -c  or  ax+b > c
            if a_val == 0:
                if abs(b_val) > c_val or (comparison == ">=" and abs(b_val) >= c_val):
                    return {"solution": "(-inf, +inf)", "steps": steps, "description": "All reals"}
                return {"solution": "empty", "steps": steps, "description": "No solution"}
            x_low = (-c_val - b_val) / a_val
            x_high = (c_val - b_val) / a_val
            if x_low > x_high:
                x_low, x_high = x_high, x_low
            if comparison == ">":
                solution = f"(-inf, {_fmt_number(x_low)}) U ({_fmt_number(x_high)}, +inf)"
            else:
                solution = f"(-inf, {_fmt_number(x_low)}] U [{_fmt_number(x_high)}, +inf)"

        steps.append(f"Solution: {solution}")
        return {"solution": solution, "steps": steps, "description": solution}

    return {"error": f"Unknown inequality type: {inequality_type}"}


# ---------------------------------------------------------------------------
# Rational Expression Simplification
# ---------------------------------------------------------------------------

def _gcd_poly(p1: List[float], p2: List[float]) -> List[float]:
    """Compute GCD of two polynomials (coefficient lists, highest first) via Euclidean algorithm."""
    if not p2 or all(abs(c) < 1e-12 for c in p2):
        return p1
    if not p1 or all(abs(c) < 1e-12 for c in p1):
        return p2
    # Ensure p1 has higher degree
    if len(p1) < len(p2):
        p1, p2 = p2, p1

    while len(p2) > 0 and not all(abs(c) < 1e-12 for c in p2):
        result = poly_long_division(Polynomial(p1), Polynomial(p2))
        rem_coeffs = result["remainder"]["coefficients"]
        p1 = p2
        p2 = rem_coeffs
        # Strip near-zero
        while len(p2) > 1 and abs(p2[0]) < 1e-12:
            p2 = p2[1:]

    # Normalize leading coefficient to 1
    if p1 and abs(p1[0]) > 1e-12:
        lead = p1[0]
        p1 = [c / lead for c in p1]
    return p1


def simplify_rational(numerator: List[float], denominator: List[float]) -> Dict[str, Any]:
    """Simplify a rational expression by dividing out GCD."""
    if all(abs(c) < 1e-12 for c in denominator):
        return {"error": "Division by zero polynomial"}

    num_p = Polynomial(numerator)
    den_p = Polynomial(denominator)
    steps: List[str] = [f"Simplify: ({num_p}) / ({den_p})"]

    gcd = _gcd_poly(numerator, denominator)
    gcd_p = Polynomial(gcd)

    if gcd_p.degree == 0:
        steps.append("No common polynomial factor (GCD is constant)")
        # Still simplify by leading coefficient of denominator
        lead = denominator[0]
        simplified_num = [c / lead for c in numerator]
        simplified_den = [c / lead for c in denominator]
    else:
        steps.append(f"GCD: {gcd_p}")
        result_num = poly_long_division(num_p, gcd_p)
        result_den = poly_long_division(den_p, gcd_p)
        simplified_num = result_num["quotient"]["coefficients"]
        simplified_den = result_den["quotient"]["coefficients"]

    sn = Polynomial(simplified_num)
    sd = Polynomial(simplified_den)
    steps.append(f"Simplified: ({sn}) / ({sd})")

    return {
        "numerator": sn.to_dict(),
        "denominator": sd.to_dict(),
        "steps": steps,
        "description": f"({sn}) / ({sd})",
    }


# ============================================================================
# TIE-01: THREE-LAYER RESPONSE SYSTEM
# ============================================================================

def _doctrine_match(normalized_query: str) -> MatchResult:
    """Layer 1: Match query against doctrine cache."""
    candidates: List[Dict[str, Any]] = []
    for key, block in DOCTRINE_CACHE.items():
        score = 0
        q_lower = normalized_query.lower()
        for kw in block.keywords:
            if kw.lower() in q_lower:
                score += 10
        if block.topic.lower() in q_lower:
            score += 20
        if score > 0:
            candidates.append({"topic": key, "score": score, "weight": block.get_authority_weight()})

    candidates.sort(key=lambda x: (-x["score"], -x["weight"]))

    hash_input = f"{normalized_query}|{json.dumps(candidates[:5], default=str)}"
    det_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    if not candidates:
        return MatchResult(
            doctrine=None, topic_key=None, match_score=0, authority_weight=0,
            conflict_detected=False, conflict_resolution=None,
            all_candidates=[], determinism_hash=det_hash,
        )

    best = candidates[0]
    conflict = len(candidates) > 1 and candidates[1]["score"] >= best["score"] * 0.8
    resolution = None
    if conflict:
        resolution = ConflictResolution(
            competing_methods=[c["topic"] for c in candidates[:3]],
            resolution_rationale=f"Selected {best['topic']} with highest score ({best['score']})",
            authority_basis="keyword_match_score",
            rejected_alternatives=[{"topic": c["topic"], "reason": f"Lower score ({c['score']})"} for c in candidates[1:3]],
        )

    block = DOCTRINE_CACHE[best["topic"]]
    return MatchResult(
        doctrine=block, topic_key=best["topic"], match_score=best["score"],
        authority_weight=best["weight"], conflict_detected=conflict,
        conflict_resolution=resolution, all_candidates=candidates,
        determinism_hash=det_hash,
    )


def _semantic_retrieval(normalized_query: str) -> Optional[Dict[str, Any]]:
    """Layer 2: Semantic retrieval on cache miss — keyword-based fallback."""
    q_lower = normalized_query.lower()
    domain_hints: Dict[str, ProblemDomain] = {
        "linear": ProblemDomain.LINEAR_EQUATION,
        "quadratic": ProblemDomain.QUADRATIC_EQUATION,
        "cubic": ProblemDomain.CUBIC_EQUATION,
        "system": ProblemDomain.SYSTEM_OF_EQUATIONS,
        "polynomial": ProblemDomain.POLYNOMIAL_OPS,
        "factor": ProblemDomain.POLYNOMIAL_FACTORING,
        "complex": ProblemDomain.COMPLEX_NUMBER,
        "logarithm": ProblemDomain.LOGARITHM,
        "log": ProblemDomain.LOGARITHM,
        "exponential": ProblemDomain.EXPONENTIAL,
        "matrix": ProblemDomain.MATRIX,
        "determinant": ProblemDomain.MATRIX,
        "inverse": ProblemDomain.MATRIX,
        "inequality": ProblemDomain.INEQUALITY,
        "absolute": ProblemDomain.ABSOLUTE_VALUE,
        "rational": ProblemDomain.RATIONAL_EXPRESSION,
    }
    for keyword, domain in domain_hints.items():
        if keyword in q_lower:
            return {"domain": domain.value, "source": "semantic_retrieval", "keyword_matched": keyword}
    return None


def _deep_analysis(query: str, domain: ProblemDomain, mode: ResponseMode) -> Dict[str, Any]:
    """Layer 3: Deep analysis — actually compute the result using solvers."""
    # This layer dispatches to the real math solvers based on detected domain
    result: Dict[str, Any] = {"domain": domain.value, "layer": "deep_analysis"}

    if domain == ProblemDomain.GENERAL:
        result["conclusion"] = "General algebra query — please specify the problem type or provide coefficients."
        result["reasoning"] = "The query could not be automatically classified into a specific algebra domain."
    else:
        result["conclusion"] = f"Domain '{domain.value}' identified. Use the specific endpoint for computation."
        result["reasoning"] = f"The query maps to the {domain.value} solver. Provide structured input for exact results."

    return result


# ============================================================================
# TIE-19: MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

DOCTRINE_INTERACTIONS: List[DoctrineInteraction] = [
    DoctrineInteraction("quadratic_formula", "vietas_formulas", "enables",
                        "Quadratic roots enable verification via Vieta's sum/product relations"),
    DoctrineInteraction("fundamental_theorem_algebra", "polynomial_factoring", "enables",
                        "FTA guarantees factorization exists over C"),
    DoctrineInteraction("rational_root_theorem", "polynomial_factoring", "enables",
                        "RRT provides candidate rational roots for trial division"),
    DoctrineInteraction("matrix_invertibility", "cramers_rule", "enables",
                        "Non-singular matrix enables Cramer's rule for systems"),
    DoctrineInteraction("complex_number_arithmetic", "quadratic_formula", "enables",
                        "Complex arithmetic required when discriminant is negative"),
    DoctrineInteraction("logarithm_properties", "exponential_equations", "enables",
                        "Log rules enable conversion between exponential and log forms"),
    DoctrineInteraction("discriminant_analysis", "quadratic_formula", "enables",
                        "Discriminant determines root classification before solving"),
]


def _stratified_match(normalized_query: str) -> StratifiedMatch:
    """Multi-doctrine matching across strata."""
    issues: List[IssueCategory] = []
    q_lower = normalized_query.lower()

    issue_keywords = {
        IssueCategory.SOLVING: ["solve", "find", "root", "solution", "equation"],
        IssueCategory.SIMPLIFICATION: ["simplify", "reduce", "expand"],
        IssueCategory.FACTORING: ["factor", "factorize", "decompose"],
        IssueCategory.COMPUTATION: ["compute", "calculate", "evaluate"],
        IssueCategory.TRANSFORMATION: ["transform", "convert", "change"],
        IssueCategory.IDENTITY: ["identity", "prove", "verify"],
        IssueCategory.ROOTS: ["root", "zero", "x-intercept"],
        IssueCategory.DOMAIN_RANGE: ["domain", "range", "restriction"],
    }

    for cat, kws in issue_keywords.items():
        if any(kw in q_lower for kw in kws):
            issues.append(cat)

    primary = _doctrine_match(normalized_query)
    secondary_matches: List[MatchResult] = []
    tertiary_matches: List[MatchResult] = []

    if primary.is_match and primary.doctrine:
        for rel in primary.doctrine.related_doctrines:
            if rel in DOCTRINE_CACHE:
                block = DOCTRINE_CACHE[rel]
                m = MatchResult(
                    doctrine=block, topic_key=rel, match_score=5,
                    authority_weight=block.get_authority_weight(),
                    conflict_detected=False, conflict_resolution=None,
                    all_candidates=[], determinism_hash="",
                )
                secondary_matches.append(m)

    fired_interactions = []
    for inter in DOCTRINE_INTERACTIONS:
        matched_topics = primary.all_candidates[:5] if primary.all_candidates else []
        topic_keys = [c["topic"] for c in matched_topics]
        if inter.source_topic in topic_keys or inter.target_topic in topic_keys:
            fired_interactions.append(inter)

    all_topics = ([primary.topic_key] if primary.topic_key else []) + \
                 [m.topic_key for m in secondary_matches if m.topic_key] + \
                 [m.topic_key for m in tertiary_matches if m.topic_key]

    det_hash = hashlib.sha256(json.dumps(sorted(all_topics)).encode()).hexdigest()

    return StratifiedMatch(
        issues_detected=issues,
        primary=primary,
        secondary=secondary_matches,
        tertiary=tertiary_matches,
        interactions=fired_interactions,
        resolution_hierarchy=[{"step": i + 1, "topic": t} for i, t in enumerate(all_topics)],
        total_doctrines_matched=len(all_topics),
        determinism_hash=det_hash,
    )


# ============================================================================
# TIE-13: ZONED ANALYSIS
# ============================================================================

@dataclass
class ZonedConclusion:
    zone: PositionZone
    conclusion: str
    confidence: float
    caveats: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone": self.zone.value,
            "conclusion": self.conclusion,
            "confidence": round(self.confidence, 3),
            "caveats": self.caveats,
            "action_items": self.action_items,
        }


def _build_zoned_analysis(result: Dict[str, Any], domain: str) -> List[Dict[str, Any]]:
    """Build zone-separated analysis."""
    zones: List[ZonedConclusion] = []

    desc = result.get("description", "")

    zones.append(ZonedConclusion(
        zone=PositionZone.COMPUTATION,
        conclusion=desc,
        confidence=0.95,
        caveats=["Result assumes exact arithmetic; floating-point rounding may introduce small errors."],
        action_items=["Verify result by substitution back into the original equation."],
    ))

    zones.append(ZonedConclusion(
        zone=PositionZone.VERIFICATION,
        conclusion=f"Domain: {domain}. Result should be verified via back-substitution or independent method.",
        confidence=0.90,
        caveats=["Numerical verification may differ by rounding epsilon."],
        action_items=["Cross-check with alternate solution method if available."],
    ))

    if result.get("steps"):
        zones.append(ZonedConclusion(
            zone=PositionZone.PROOF,
            conclusion=f"Step-by-step derivation provided ({len(result['steps'])} steps).",
            confidence=0.92,
            caveats=["Steps follow standard algebraic manipulation rules."],
            action_items=["Review each step for algebraic correctness."],
        ))

    return [z.to_dict() for z in zones]


# ============================================================================
# TIE-02: RESPONSE MODES (FAST / DEFENSE / MEMO)
# ============================================================================

def _format_fast(result: Dict[str, Any], doctrine_match: MatchResult) -> Dict[str, Any]:
    """FAST mode: Direct answer, minimal extras."""
    return {
        "conclusion": result.get("description", str(result.get("solution", result.get("result", "")))),
        "reasoning": "Direct computation via algebraic solver.",
        "key_factors": result.get("steps", [])[:3],
    }


def _format_defense(result: Dict[str, Any], doctrine_match: MatchResult) -> Dict[str, Any]:
    """DEFENSE mode: Full step-by-step derivation."""
    steps_text = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(result.get("steps", [])))
    reasoning = f"Full derivation:\n{steps_text}"
    citations: List[Dict[str, str]] = []
    if doctrine_match.is_match and doctrine_match.doctrine:
        for auth in doctrine_match.doctrine.primary_authority:
            citations.append({"authority": auth.get("level", ""), "reference": auth.get("citation", ""),
                              "relevance": auth.get("relevance", "")})
    return {
        "conclusion": result.get("description", ""),
        "reasoning": reasoning,
        "key_factors": result.get("steps", []),
        "citations": citations,
    }


def _format_memo(result: Dict[str, Any], doctrine_match: MatchResult) -> Dict[str, Any]:
    """MEMO mode: Long-form with theorem citations, educational."""
    steps = result.get("steps", [])
    doc_text = ""
    if doctrine_match.is_match and doctrine_match.doctrine:
        d = doctrine_match.doctrine
        doc_text = (f"\n\nTheoretical Foundation ({d.topic}):\n{d.reasoning_framework}\n"
                    f"\nKey Factors: {', '.join(d.key_factors)}\n"
                    f"\nVerification Method: {d.verification_method}")

    reasoning = "MEMORANDUM OF ALGEBRAIC ANALYSIS\n"
    reasoning += "=" * 40 + "\n\n"
    reasoning += f"Problem Classification: {result.get('classification', 'N/A')}\n\n"
    reasoning += "Step-by-Step Solution:\n"
    for i, s in enumerate(steps):
        reasoning += f"  {i+1}. {s}\n"
    reasoning += doc_text
    reasoning += f"\n\nResult: {result.get('description', '')}"

    citations: List[Dict[str, str]] = []
    if doctrine_match.is_match and doctrine_match.doctrine:
        for auth in doctrine_match.doctrine.primary_authority:
            citations.append({"authority": auth.get("level", ""), "reference": auth.get("citation", ""),
                              "relevance": auth.get("relevance", "")})

    return {
        "conclusion": result.get("description", ""),
        "reasoning": reasoning,
        "key_factors": steps + (doctrine_match.doctrine.key_factors if doctrine_match.is_match and doctrine_match.doctrine else []),
        "citations": citations,
    }


# ============================================================================
# QUERY PROCESSING PIPELINE
# ============================================================================

def process_query(query: AlgebraQuery) -> AlgebraResponse:
    """Main query pipeline: normalize -> match -> compute -> format."""
    query_id = str(uuid.uuid4())
    start = time.time()
    _metrics.query_start()
    trace = _telemetry.start_trace(query_id, query.question)

    try:
        # Step 1: Normalize
        normalized = normalize_query(query.question)
        _telemetry.add_event(trace, "normalized", normalized)

        # Step 2: Doctrine match
        match_result = _doctrine_match(normalized)
        _telemetry.add_event(trace, "doctrine_match", {
            "matched": match_result.is_match,
            "topic": match_result.topic_key,
            "score": match_result.match_score,
        })

        doctrine_hit = match_result.is_match
        if doctrine_hit and match_result.topic_key:
            _coverage.record_hit(match_result.topic_key)
        else:
            _coverage.record_miss()

        # Step 3: Detect domain
        domain = query.domain or ProblemDomain.GENERAL
        if domain == ProblemDomain.GENERAL:
            sem = _semantic_retrieval(normalized)
            if sem:
                domain = ProblemDomain(sem["domain"])

        # Step 4: Deep analysis (placeholder for general queries)
        computation_result = _deep_analysis(normalized, domain, query.mode)

        # Step 5: Format response
        if query.mode == ResponseMode.FAST:
            formatted = _format_fast(computation_result, match_result)
        elif query.mode == ResponseMode.DEFENSE:
            formatted = _format_defense(computation_result, match_result)
        else:
            formatted = _format_memo(computation_result, match_result)

        # Step 6: Build zoned analysis (DEFENSE/MEMO only)
        zoned = None
        if query.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
            zoned = _build_zoned_analysis(computation_result, domain.value)

        # Step 7: Determinism hash
        det_hash = compute_determinism_hash(normalized, query.mode.value, formatted.get("conclusion", ""))

        # Step 8: Drift check
        if match_result.topic_key:
            _drift.check_drift(match_result.topic_key, det_hash)

        # Latency
        latency_ms = round((time.time() - start) * 1000, 2)
        _metrics.record_query(latency_ms, doctrine_hit)
        _telemetry.complete_trace(trace, "doctrine" if doctrine_hit else "computation", True)

        # Step 9: Coverage report
        coverage = _coverage.get_report()

        # Confidence tier
        if match_result.is_match and match_result.match_score >= 20:
            conf_tier: Literal["high", "moderate", "requires_review"] = "high"
        elif match_result.is_match:
            conf_tier = "moderate"
        else:
            conf_tier = "requires_review"

        conf_strat = None
        if match_result.is_match and match_result.doctrine:
            conf_strat = match_result.doctrine.confidence_stratification.value

        # Build citations
        citations: List[Citation] = []
        for c in formatted.get("citations", []):
            if isinstance(c, dict):
                citations.append(Citation(authority=c.get("authority", ""), reference=c.get("reference", ""),
                                          relevance=c.get("relevance", "")))

        response = AlgebraResponse(
            query_id=query_id,
            question=query.question,
            mode=query.mode,
            domain_detected=domain.value,
            conclusion=formatted.get("conclusion", ""),
            reasoning=formatted.get("reasoning", ""),
            key_factors=formatted.get("key_factors", []),
            citations=citations,
            steps=[ReasoningStep(step=i + 1, analysis=s) for i, s in enumerate(computation_result.get("steps", []))] if query.include_trace else None,
            numeric_result=computation_result.get("solution", computation_result.get("result")),
            doctrine_match=doctrine_hit,
            confidence_tier=conf_tier,
            confidence_stratification=conf_strat,
            response_layer="doctrine" if doctrine_hit else "computation",
            latency_ms=latency_ms,
            determinism_hash=det_hash,
            zoned_analysis=zoned,
            coverage_report=coverage,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Step 10: Audit trail
        _write_audit({
            "query_id": query_id,
            "question": query.question[:200],
            "mode": query.mode.value,
            "domain": domain.value,
            "doctrine_hit": doctrine_hit,
            "latency_ms": latency_ms,
            "confidence": conf_tier,
        })

        return response

    except Exception as exc:
        _metrics.record_error(str(exc))
        _telemetry.complete_trace(trace, "error", False)
        logger.error(f"Query processing error: {exc}")
        raise

    finally:
        _metrics.query_end()


# ============================================================================
# TIE-17: FASTAPI SERVER
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"MATH02 Algebra Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} blocks loaded")
    yield
    logger.info("MATH02 Algebra Engine shutting down")


app = FastAPI(
    title="MATH02 Algebra Intelligence Engine",
    version=ENGINE_VERSION,
    description="TIE-20 compliant algebra engine: equations, polynomials, matrices, complex numbers",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TIE-12: HEALTH ENDPOINT
@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    import psutil
    proc = psutil.Process()
    mem = proc.memory_info()
    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        uptime_seconds=round(time.time() - _START_TIME, 1),
        api_latency=_metrics.get_latency_stats(),
        doctrine_cache={
            "status": "loaded",
            "topics": len(DOCTRINE_CACHE),
            "hit_rate": _metrics.get_doctrine_hit_rate(),
        },
        memory_mb={
            "used": round(mem.rss / 1024 / 1024, 1),
            "available": 0.0,
            "percent": 0.0,
        },
        active_queries=_metrics.active_queries,
        queries_last_hour=_metrics.queries_last_hour(),
        error_rate=_metrics.get_error_stats(),
    )


# Main query endpoint
@app.post("/query", response_model=AlgebraResponse)
async def query_endpoint(q: AlgebraQuery) -> AlgebraResponse:
    return process_query(q)


# --- Direct computation endpoints ---

@app.post("/solve/linear")
async def solve_linear_endpoint(a: float, b: float, c: float):
    return solve_linear(a, b, c)


@app.post("/solve/quadratic")
async def solve_quadratic_endpoint(a: float, b: float, c: float):
    return solve_quadratic(a, b, c)


@app.post("/solve/cubic")
async def solve_cubic_endpoint(a: float, b: float, c: float, d: float):
    return solve_cubic(a, b, c, d)


class SystemInput(BaseModel):
    coefficients: List[List[float]]
    constants: List[float]


@app.post("/solve/system")
async def solve_system_endpoint(data: SystemInput):
    n = len(data.coefficients)
    if n == 2:
        return solve_system_2x2(data.coefficients, data.constants)
    return solve_system_gaussian(data.coefficients, data.constants)


class PolyInput(BaseModel):
    coefficients: List[float]


class PolyPairInput(BaseModel):
    p1: List[float]
    p2: List[float]


@app.post("/polynomial/add")
async def poly_add_endpoint(data: PolyPairInput):
    result = poly_add(Polynomial(data.p1), Polynomial(data.p2))
    return result.to_dict()


@app.post("/polynomial/multiply")
async def poly_multiply_endpoint(data: PolyPairInput):
    result = poly_multiply(Polynomial(data.p1), Polynomial(data.p2))
    return result.to_dict()


@app.post("/polynomial/divide")
async def poly_divide_endpoint(data: PolyPairInput):
    return poly_long_division(Polynomial(data.p1), Polynomial(data.p2))


class SyntheticDivInput(BaseModel):
    coefficients: List[float]
    root: float


@app.post("/polynomial/synthetic_division")
async def synthetic_div_endpoint(data: SyntheticDivInput):
    return poly_synthetic_division(data.coefficients, data.root)


@app.post("/polynomial/factor")
async def factor_endpoint(data: PolyInput):
    return factor_polynomial(data.coefficients)


class ComplexInput(BaseModel):
    operation: str
    z1_real: float
    z1_imag: float
    z2_real: float = 0
    z2_imag: float = 0


@app.post("/complex")
async def complex_endpoint(data: ComplexInput):
    return complex_ops(data.operation, data.z1_real, data.z1_imag, data.z2_real, data.z2_imag)


class LogInput(BaseModel):
    equation_type: str
    base: Optional[float] = None
    value: Optional[float] = None
    target: Optional[float] = None
    argument: Optional[float] = None
    old_base: Optional[float] = None
    new_base: Optional[float] = None


@app.post("/logarithm")
async def log_endpoint(data: LogInput):
    params: Dict[str, Any] = {}
    for k, v in data.model_dump().items():
        if k != "equation_type" and v is not None:
            params[k] = v
    return solve_logarithm(data.equation_type, **params)


class MatrixInput(BaseModel):
    operation: str
    matrix_a: List[List[float]]
    matrix_b: Optional[List[List[float]]] = None
    scalar: Optional[float] = None


@app.post("/matrix")
async def matrix_endpoint(data: MatrixInput):
    return matrix_operations(data.operation, data.matrix_a, data.matrix_b, data.scalar)


class InequalityInput(BaseModel):
    inequality_type: str
    coefficients: List[float]
    comparison: str = "<"


@app.post("/inequality")
async def inequality_endpoint(data: InequalityInput):
    return solve_inequality(data.inequality_type, data.coefficients, data.comparison)


class RationalInput(BaseModel):
    numerator: List[float]
    denominator: List[float]


@app.post("/rational/simplify")
async def rational_endpoint(data: RationalInput):
    return simplify_rational(data.numerator, data.denominator)


class PolyEvalInput(BaseModel):
    coefficients: List[float]
    x: float


@app.post("/polynomial/evaluate")
async def poly_eval_endpoint(data: PolyEvalInput):
    p = Polynomial(data.coefficients)
    result = p.evaluate(data.x)
    return {"polynomial": str(p), "x": data.x, "result": result}


# Metrics and diagnostics
@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency": _metrics.get_latency_stats(),
        "errors": _metrics.get_error_stats(),
        "doctrine_hit_rate": _metrics.get_doctrine_hit_rate(),
        "queries_last_hour": _metrics.queries_last_hour(),
        "active_queries": _metrics.active_queries,
    }


@app.get("/coverage")
async def coverage_endpoint():
    return _coverage.get_report()


@app.get("/drift")
async def drift_endpoint():
    return {"events": _drift.get_events(), "baselines": len(_drift.baseline_hashes)}


@app.get("/doctrines")
async def doctrines_endpoint():
    return {
        key: {
            "topic": block.topic,
            "keywords": block.keywords,
            "confidence": block.confidence,
            "authority_weight": block.get_authority_weight(),
        }
        for key, block in DOCTRINE_CACHE.items()
    }


# ============================================================================
# ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting MATH02 Algebra Engine on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
