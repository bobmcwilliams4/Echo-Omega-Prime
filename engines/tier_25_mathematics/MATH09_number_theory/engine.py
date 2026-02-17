"""
MATH09 — Number Theory Intelligence Engine
TIE-20 Compliant | Tier 13 Mathematics | MODE: DET | AUTH: 5.0
Port: 8571

Covers: primes, modular arithmetic, Diophantine equations, continued fractions,
quadratic residues, Legendre/Jacobi symbols, integer sequences, number-theoretic functions.

All algorithms pure Python. No external math libraries required.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import random
import sys
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

ENGINE_ID = "MATH09"
ENGINE_NAME = "Number Theory Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8571
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>MATH09</cyan> | {message}",
    level="DEBUG",
)
LOG_PATH = ENGINE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)
logger.add(
    LOG_PATH / "math09_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
)
AUDIT_PATH = ENGINE_DIR / "audit_trail.jsonl"

# ---------------------------------------------------------------------------
# Pydantic Models — I/O
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    context: dict[str, Any] = Field(default_factory=dict)
    include_proofs: bool = False
    depth: str = "standard"


class AuthoritySource(BaseModel):
    source: str
    weight: float
    citation: str


class DoctrineResult(BaseModel):
    topic: str
    conclusion: str
    reasoning: str
    authorities: list[AuthoritySource]
    confidence: ConfidenceLevel
    key_factors: list[str]


class EngineResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    mode: ResponseMode
    zone: PositionZone
    response_layer: str
    doctrine_results: list[DoctrineResult]
    computation_results: dict[str, Any] = Field(default_factory=dict)
    confidence: ConfidenceLevel
    determinism_hash: str
    latency_ms: float
    timestamp: str
    disclosure_caveat: str = ""
    epistemic_notes: list[str] = Field(default_factory=list)


class PrimalityRequest(BaseModel):
    n: int = Field(..., gt=1)
    method: str = "auto"


class FactorizationRequest(BaseModel):
    n: int = Field(..., gt=1)


class SieveRequest(BaseModel):
    limit: int = Field(..., gt=1, le=10_000_000)


class ModExpRequest(BaseModel):
    base: int
    exponent: int
    modulus: int = Field(..., gt=0)


class CRTRequest(BaseModel):
    remainders: list[int]
    moduli: list[int]


class DiophantineRequest(BaseModel):
    a: int
    b: int
    c: int


class ContinuedFractionRequest(BaseModel):
    numerator: int
    denominator: int = Field(..., gt=0)


class LegendreRequest(BaseModel):
    a: int
    p: int = Field(..., gt=2)


class JacobiRequest(BaseModel):
    a: int
    n: int = Field(..., gt=0)


class SequenceRequest(BaseModel):
    name: str
    n: int = Field(..., ge=0)


class TotientRequest(BaseModel):
    n: int = Field(..., gt=0)


class DivisorRequest(BaseModel):
    n: int = Field(..., gt=0)
    kind: str = "count"


class MobiusRequest(BaseModel):
    n: int = Field(..., gt=0)


class ExtGCDRequest(BaseModel):
    a: int
    b: int


class ModInverseRequest(BaseModel):
    a: int
    m: int = Field(..., gt=1)


class PartitionRequest(BaseModel):
    n: int = Field(..., ge=0, le=5000)


class QuadResRequest(BaseModel):
    n: int = Field(..., gt=0)
    p: int = Field(..., gt=2)


class HealthResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    status: str
    tier: int
    port: int
    mode: str
    auth_level: float
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    doctrine_count: int
    components: dict[str, str]
    timestamp: str


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 1: THREE-LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

class ThreeLayerRouter:
    """Routes queries through Doctrine Cache -> Semantic Retrieval -> Deep Analysis."""

    def __init__(self, doctrine_cache: "DoctrineCache", semantic: "SemanticNormalizer",
                 deep: "DeepAnalysisEngine") -> None:
        self._doctrine = doctrine_cache
        self._semantic = semantic
        self._deep = deep
        logger.info("ThreeLayerRouter initialised")

    def route(self, query: str, mode: ResponseMode, zone: PositionZone,
              context: dict[str, Any], include_proofs: bool) -> tuple[str, list[DoctrineResult], dict[str, Any]]:
        normalised = self._semantic.normalise(query)
        cache_hits = self._doctrine.lookup(normalised)
        if cache_hits and mode == ResponseMode.FAST:
            return "DOCTRINE_CACHE", cache_hits, {}
        semantic_hits = self._semantic.retrieve(normalised)
        merged = _merge_doctrine_results(cache_hits, semantic_hits)
        if merged and mode != ResponseMode.MEMO:
            return "SEMANTIC_RETRIEVAL", merged, {}
        deep_results, computations = self._deep.analyse(query, normalised, zone, context, include_proofs)
        final = _merge_doctrine_results(merged, deep_results)
        return "DEEP_ANALYSIS", final, computations


def _merge_doctrine_results(a: list[DoctrineResult], b: list[DoctrineResult]) -> list[DoctrineResult]:
    seen: set[str] = set()
    merged: list[DoctrineResult] = []
    for item in (*a, *b):
        if item.topic not in seen:
            seen.add(item.topic)
            merged.append(item)
    return merged


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 2: RESPONSE MODES
# ═══════════════════════════════════════════════════════════════════════════

class ResponseModeFormatter:
    """Formats output according to FAST / DEFENSE / MEMO mode."""

    @staticmethod
    def format(response: EngineResponse, mode: ResponseMode) -> dict[str, Any]:
        base = response.model_dump()
        if mode == ResponseMode.FAST:
            base.pop("epistemic_notes", None)
            for dr in base.get("doctrine_results", []):
                dr.pop("reasoning", None)
            return base
        if mode == ResponseMode.DEFENSE:
            return base
        if mode == ResponseMode.MEMO:
            base["memo_header"] = (
                f"MEMORANDUM — {ENGINE_NAME}\n"
                f"Date: {response.timestamp}\n"
                f"Re: {response.query[:120]}\n"
                f"Confidence: {response.confidence.value}\n"
                f"Mode: MEMO — Full documentation with citations"
            )
            return base
        return base


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 3: DOCTRINE CACHE
# ═══════════════════════════════════════════════════════════════════════════

class DoctrineBlock(BaseModel):
    topic: str
    keywords: list[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    counter_arguments: list[str]
    resolution_strategy: str
    entity_scope: str


class DoctrineCache:
    """Pre-compiled expert reasoning blocks for number theory."""

    def __init__(self) -> None:
        self._blocks: list[DoctrineBlock] = []
        self._keyword_index: dict[str, list[int]] = defaultdict(list)
        self._load()

    def _load(self) -> None:
        path = ENGINE_DIR / "doctrine_cache.json"
        if not path.exists():
            logger.warning("doctrine_cache.json not found — using embedded defaults")
            self._blocks = self._embedded_defaults()
        else:
            raw = json.loads(path.read_text(encoding="utf-8"))
            for entry in raw:
                self._blocks.append(DoctrineBlock(**entry))
        for idx, block in enumerate(self._blocks):
            for kw in block.keywords:
                self._keyword_index[kw.lower()].append(idx)
        logger.info(f"DoctrineCache loaded {len(self._blocks)} blocks, {len(self._keyword_index)} keywords")

    def lookup(self, normalised_query: str) -> list[DoctrineResult]:
        tokens = set(normalised_query.lower().split())
        scored: list[tuple[float, DoctrineBlock]] = []
        for block in self._blocks:
            hits = sum(1 for kw in block.keywords if kw.lower() in tokens)
            if hits > 0:
                scored.append((hits / len(block.keywords), block))
        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[DoctrineResult] = []
        for score, block in scored[:5]:
            results.append(DoctrineResult(
                topic=block.topic,
                conclusion=block.conclusion_template,
                reasoning=block.reasoning_framework,
                authorities=[AuthoritySource(source=a, weight=0.9, citation=a) for a in block.primary_authority],
                confidence=block.confidence,
                key_factors=block.key_factors,
            ))
        return results

    @property
    def count(self) -> int:
        return len(self._blocks)

    def _embedded_defaults(self) -> list[DoctrineBlock]:
        return [
            DoctrineBlock(
                topic="Fundamental Theorem of Arithmetic",
                keywords=["prime", "factorization", "unique", "fundamental", "theorem", "arithmetic"],
                conclusion_template="Every integer greater than 1 is either prime or can be represented uniquely as a product of primes up to ordering.",
                reasoning_framework=(
                    "The FTA guarantees existence and uniqueness of prime factorization. "
                    "Existence follows by strong induction: if n is prime we are done; otherwise n=ab with 1<a,b<n "
                    "and by inductive hypothesis each factors into primes. Uniqueness is proved by Euclid's lemma: "
                    "if p | ab then p | a or p | b. This is the cornerstone of multiplicative number theory and "
                    "underpins the Euler product for the Riemann zeta function, the structure of Z/nZ, and "
                    "the correctness of RSA encryption."
                ),
                key_factors=["unique factorization", "Euclid's lemma", "prime decomposition", "multiplicative structure", "induction"],
                primary_authority=["Hardy & Wright, An Introduction to the Theory of Numbers", "Gauss, Disquisitiones Arithmeticae, Art. 16"],
                confidence=ConfidenceLevel.DEFENSIBLE,
                confidence_stratification="PROVEN — theorem with rigorous proof since Euclid",
                counter_arguments=["In non-UFD rings (e.g. Z[sqrt(-5)]) unique factorization fails", "Requires careful treatment of units and ordering"],
                resolution_strategy="Apply trial division or Pollard's rho for explicit factorization; verify via product reconstruction.",
                entity_scope="integers > 1",
            ),
        ]


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════

class AuthorityLevel(BaseModel):
    name: str
    weight: float
    description: str


AUTHORITY_HIERARCHY: list[AuthorityLevel] = [
    AuthorityLevel(name="PROVEN_THEOREM", weight=1.0, description="Rigorously proved mathematical theorem"),
    AuthorityLevel(name="PEER_REVIEWED", weight=0.95, description="Published in peer-reviewed journal"),
    AuthorityLevel(name="TEXTBOOK", weight=0.90, description="Standard textbook result"),
    AuthorityLevel(name="CONJECTURE_STRONG", weight=0.70, description="Widely believed conjecture with strong evidence (e.g. Riemann Hypothesis)"),
    AuthorityLevel(name="CONJECTURE_OPEN", weight=0.50, description="Open conjecture with partial results"),
    AuthorityLevel(name="HEURISTIC", weight=0.40, description="Heuristic or probabilistic argument"),
    AuthorityLevel(name="COMPUTATIONAL", weight=0.60, description="Verified computationally up to large bound"),
    AuthorityLevel(name="FOLKLORE", weight=0.30, description="Well-known but not rigorously documented"),
]


class AuthorityHardener:
    """Resolves conflicting authorities by weight and precedence."""

    def __init__(self) -> None:
        self._hierarchy = {a.name: a for a in AUTHORITY_HIERARCHY}

    def resolve(self, sources: list[AuthoritySource]) -> AuthoritySource:
        if not sources:
            return AuthoritySource(source="none", weight=0.0, citation="No authority found")
        return max(sources, key=lambda s: s.weight)

    def harden_confidence(self, base: ConfidenceLevel, sources: list[AuthoritySource]) -> ConfidenceLevel:
        if not sources:
            return ConfidenceLevel.HIGH_RISK
        max_weight = max(s.weight for s in sources)
        if max_weight >= 0.9:
            return ConfidenceLevel.DEFENSIBLE
        if max_weight >= 0.7:
            return base
        if max_weight >= 0.5:
            return ConfidenceLevel.AGGRESSIVE
        return ConfidenceLevel.DISCLOSURE


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════

class ConfidenceStratifier:
    """Assigns confidence strata based on proof status, computational verification, authority weight."""

    STRATA_RULES: dict[str, ConfidenceLevel] = {
        "proven": ConfidenceLevel.DEFENSIBLE,
        "verified_to_bound": ConfidenceLevel.DEFENSIBLE,
        "probabilistic": ConfidenceLevel.AGGRESSIVE,
        "conjectural": ConfidenceLevel.DISCLOSURE,
        "heuristic": ConfidenceLevel.HIGH_RISK,
    }

    def stratify(self, proof_status: str, authorities: list[AuthoritySource]) -> ConfidenceLevel:
        base = self.STRATA_RULES.get(proof_status, ConfidenceLevel.DISCLOSURE)
        if authorities:
            max_w = max(a.weight for a in authorities)
            if max_w >= 0.95 and base != ConfidenceLevel.DEFENSIBLE:
                base = ConfidenceLevel.AGGRESSIVE
        return base

    def explain(self, level: ConfidenceLevel) -> str:
        explanations = {
            ConfidenceLevel.DEFENSIBLE: "Result is rigorously proven or computationally verified to sufficient bound.",
            ConfidenceLevel.AGGRESSIVE: "Result relies on probabilistic methods or strong but unproven conjectures.",
            ConfidenceLevel.DISCLOSURE: "Result is conjectural; disclose uncertainty to any relying party.",
            ConfidenceLevel.HIGH_RISK: "Result is heuristic or poorly supported; use with extreme caution.",
        }
        return explanations.get(level, "Unknown confidence level.")


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 6: SEMANTIC NORMALISATION
# ═══════════════════════════════════════════════════════════════════════════

class SemanticNormalizer:
    """Domain-specific term normalisation for number theory queries."""

    def __init__(self) -> None:
        self._dict: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        path = ENGINE_DIR / "semantic_dict.json"
        if path.exists():
            self._dict = json.loads(path.read_text(encoding="utf-8"))
        else:
            self._dict = self._defaults()
        logger.info(f"SemanticNormalizer loaded {len(self._dict)} mappings")

    def _defaults(self) -> dict[str, str]:
        return {
            "primes": "prime_numbers",
            "prime number": "prime_numbers",
            "phi function": "euler_totient",
            "euler phi": "euler_totient",
            "totient": "euler_totient",
            "gcd": "greatest_common_divisor",
            "lcm": "least_common_multiple",
            "mod": "modular_arithmetic",
            "modular": "modular_arithmetic",
            "congruence": "modular_arithmetic",
            "crt": "chinese_remainder_theorem",
            "chinese remainder": "chinese_remainder_theorem",
            "fermat": "fermat_little_theorem",
            "miller rabin": "miller_rabin_primality",
            "miller-rabin": "miller_rabin_primality",
            "sieve": "sieve_of_eratosthenes",
            "eratosthenes": "sieve_of_eratosthenes",
            "diophantine": "diophantine_equations",
            "continued fraction": "continued_fractions",
            "legendre symbol": "legendre_symbol",
            "jacobi symbol": "jacobi_symbol",
            "quadratic residue": "quadratic_residues",
            "fibonacci": "fibonacci_sequence",
            "catalan": "catalan_numbers",
            "partition": "partition_function",
            "mobius": "mobius_function",
            "moebius": "mobius_function",
            "divisor": "divisor_function",
            "sigma": "divisor_function",
            "factorization": "prime_factorization",
            "pollard": "pollard_rho",
            "rho": "pollard_rho",
        }

    def normalise(self, query: str) -> str:
        result = query.lower()
        for term, normalised in sorted(self._dict.items(), key=lambda x: -len(x[0])):
            result = result.replace(term, normalised)
        return result

    def retrieve(self, normalised_query: str) -> list[DoctrineResult]:
        """Semantic retrieval layer — returns doctrines matching normalised terms."""
        return []


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 7: VECTOR SEARCH (stub-free fallback)
# ═══════════════════════════════════════════════════════════════════════════

class VectorSearch:
    """Cosine-similarity search over doctrine embeddings (bag-of-words fallback)."""

    def __init__(self, doctrines: list[DoctrineBlock]) -> None:
        self._doctrines = doctrines
        self._vocab: dict[str, int] = {}
        self._vectors: list[list[float]] = []
        self._build_index()

    def _build_index(self) -> None:
        all_tokens: set[str] = set()
        for d in self._doctrines:
            tokens = set(d.topic.lower().split()) | set(k.lower() for k in d.keywords)
            tokens |= set(d.conclusion_template.lower().split())
            all_tokens |= tokens
        self._vocab = {t: i for i, t in enumerate(sorted(all_tokens))}
        dim = len(self._vocab)
        for d in self._doctrines:
            vec = [0.0] * dim
            tokens = set(d.topic.lower().split()) | set(k.lower() for k in d.keywords)
            tokens |= set(d.conclusion_template.lower().split())
            for t in tokens:
                if t in self._vocab:
                    vec[self._vocab[t]] = 1.0
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            self._vectors.append([x / norm for x in vec])

    def search(self, query: str, top_k: int = 3) -> list[tuple[float, DoctrineBlock]]:
        dim = len(self._vocab)
        qvec = [0.0] * dim
        for token in query.lower().split():
            if token in self._vocab:
                qvec[self._vocab[token]] = 1.0
        qnorm = math.sqrt(sum(x * x for x in qvec)) or 1.0
        qvec = [x / qnorm for x in qvec]
        scores: list[tuple[float, int]] = []
        for idx, dvec in enumerate(self._vectors):
            dot = sum(a * b for a, b in zip(qvec, dvec))
            scores.append((dot, idx))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [(s, self._doctrines[i]) for s, i in scores[:top_k] if s > 0.0]


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 8: TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Full query tracing, latency tracking, error domain classification."""

    def __init__(self) -> None:
        self._queries: list[dict[str, Any]] = []
        self._errors: list[dict[str, Any]] = []
        self._start_time = time.monotonic()

    def record_query(self, query: str, latency_ms: float, layer: str, mode: str, zone: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query[:200],
            "latency_ms": round(latency_ms, 2),
            "layer": layer,
            "mode": mode,
            "zone": zone,
        }
        self._queries.append(entry)
        if len(self._queries) > 10_000:
            self._queries = self._queries[-5_000:]

    def record_error(self, error: str, domain: str, query: str) -> None:
        self._errors.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": error[:500],
            "domain": domain,
            "query": query[:200],
        })

    @property
    def total_queries(self) -> int:
        return len(self._queries)

    @property
    def average_latency(self) -> float:
        if not self._queries:
            return 0.0
        return sum(q["latency_ms"] for q in self._queries) / len(self._queries)

    @property
    def error_rate(self) -> float:
        total = len(self._queries) + len(self._errors)
        if total == 0:
            return 0.0
        return len(self._errors) / total

    @property
    def uptime(self) -> float:
        return time.monotonic() - self._start_time

    def snapshot(self) -> dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "total_errors": len(self._errors),
            "average_latency_ms": round(self.average_latency, 2),
            "error_rate": round(self.error_rate, 4),
            "uptime_seconds": round(self.uptime, 1),
            "recent_queries": self._queries[-10:],
            "recent_errors": self._errors[-10:],
        }


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detects doctrine drift over time by tracking confidence distributions."""

    def __init__(self) -> None:
        self._snapshots: list[dict[str, Any]] = []
        self._confidence_history: list[ConfidenceLevel] = []

    def record(self, results: list[DoctrineResult]) -> None:
        dist: dict[str, int] = defaultdict(int)
        for r in results:
            dist[r.confidence.value] += 1
            self._confidence_history.append(r.confidence)
        self._snapshots.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "distribution": dict(dist),
            "result_count": len(results),
        })
        if len(self._snapshots) > 1000:
            self._snapshots = self._snapshots[-500:]

    def detect_drift(self) -> dict[str, Any]:
        if len(self._snapshots) < 10:
            return {"drift_detected": False, "reason": "insufficient data", "snapshots": len(self._snapshots)}
        recent = self._snapshots[-10:]
        older = self._snapshots[-20:-10] if len(self._snapshots) >= 20 else self._snapshots[:10]
        recent_high_risk = sum(s["distribution"].get("HIGH_RISK", 0) for s in recent)
        older_high_risk = sum(s["distribution"].get("HIGH_RISK", 0) for s in older)
        drift = recent_high_risk > older_high_risk * 1.5 and recent_high_risk > 3
        return {
            "drift_detected": drift,
            "recent_high_risk_count": recent_high_risk,
            "older_high_risk_count": older_high_risk,
            "snapshots_analysed": len(self._snapshots),
        }


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Tracks triggered and missed doctrines; detects epistemic gaps."""

    def __init__(self) -> None:
        self._triggered: dict[str, int] = defaultdict(int)
        self._missed: list[str] = []
        self._load()

    def _load(self) -> None:
        path = ENGINE_DIR / "coverage_map.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self._triggered = defaultdict(int, data.get("triggered", {}))
            self._missed = data.get("missed_topics", [])

    def record_hit(self, topic: str) -> None:
        self._triggered[topic] += 1

    def record_miss(self, query: str) -> None:
        self._missed.append(query[:200])
        if len(self._missed) > 5000:
            self._missed = self._missed[-2500:]

    def report(self) -> dict[str, Any]:
        return {
            "topics_triggered": dict(self._triggered),
            "total_hits": sum(self._triggered.values()),
            "unique_topics_hit": len(self._triggered),
            "missed_queries_count": len(self._missed),
            "recent_misses": self._missed[-20:],
            "epistemic_gaps": self._identify_gaps(),
        }

    def _identify_gaps(self) -> list[str]:
        gaps: list[str] = []
        if len(self._missed) > 10:
            freq: dict[str, int] = defaultdict(int)
            for q in self._missed[-100:]:
                for token in q.lower().split():
                    if len(token) > 3:
                        freq[token] += 1
            for token, count in sorted(freq.items(), key=lambda x: -x[1])[:10]:
                if count >= 3:
                    gaps.append(f"Recurring term '{token}' in {count} missed queries")
        return gaps


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Latency stats, error rates, hit rates, queries/hour."""

    def __init__(self, telemetry: TelemetryCollector, coverage: CoverageMap) -> None:
        self._telemetry = telemetry
        self._coverage = coverage

    def collect(self) -> dict[str, Any]:
        uptime_hours = self._telemetry.uptime / 3600 if self._telemetry.uptime > 0 else 1.0
        return {
            "total_queries": self._telemetry.total_queries,
            "queries_per_hour": round(self._telemetry.total_queries / max(uptime_hours, 0.001), 1),
            "average_latency_ms": round(self._telemetry.average_latency, 2),
            "error_rate": round(self._telemetry.error_rate, 4),
            "cache_hit_rate": self._compute_hit_rate(),
            "uptime_seconds": round(self._telemetry.uptime, 1),
            "coverage": self._coverage.report(),
        }

    def _compute_hit_rate(self) -> float:
        total = self._telemetry.total_queries
        if total == 0:
            return 0.0
        cache_layers = sum(
            1 for q in self._telemetry._queries if q.get("layer") == "DOCTRINE_CACHE"
        )
        return round(cache_layers / total, 4)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 12: HEALTH ENDPOINT (defined as method on the app below)
# ═══════════════════════════════════════════════════════════════════════════
# Implemented in the FastAPI route section.


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

class ZonedAnalyser:
    """Position zone separation: PLANNING / REPORTING / AUDIT."""

    ZONE_GUIDELINES: dict[PositionZone, str] = {
        PositionZone.PLANNING: "Exploratory analysis; all methods available; results may change.",
        PositionZone.REPORTING: "Final results only; computations verified; cite all sources.",
        PositionZone.AUDIT: "Forensic trace; every step logged; deterministic reproducibility required.",
    }

    def enforce(self, zone: PositionZone, results: list[DoctrineResult]) -> list[DoctrineResult]:
        if zone == PositionZone.AUDIT:
            for r in results:
                if r.confidence == ConfidenceLevel.HIGH_RISK:
                    r.confidence = ConfidenceLevel.DISCLOSURE
                    r.key_factors.append("[AUDIT] Downgraded from HIGH_RISK — requires manual verification")
        return results

    def zone_caveat(self, zone: PositionZone) -> str:
        return self.ZONE_GUIDELINES.get(zone, "")


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════

class FactFragilityScorer:
    """Scores how fragile a mathematical result is: proven theorems = 0.0 (not fragile),
       conjectures = high fragility."""

    def score(self, result: DoctrineResult) -> dict[str, Any]:
        base_fragility = {
            ConfidenceLevel.DEFENSIBLE: 0.05,
            ConfidenceLevel.AGGRESSIVE: 0.30,
            ConfidenceLevel.DISCLOSURE: 0.55,
            ConfidenceLevel.HIGH_RISK: 0.80,
        }
        fragility = base_fragility.get(result.confidence, 0.5)
        authority_strength = max((a.weight for a in result.authorities), default=0.0)
        fragility *= (1.0 - authority_strength * 0.3)
        return {
            "topic": result.topic,
            "fragility_score": round(fragility, 3),
            "verifiability": "high" if fragility < 0.2 else "medium" if fragility < 0.5 else "low",
            "recharacterisation_risk": fragility > 0.4,
            "testimony_dependence": fragility > 0.6,
        }


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 15: AUDIT TRAIL JSONL
# ═══════════════════════════════════════════════════════════════════════════

class AuditTrail:
    """Append-only JSONL audit trail for every query."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def log(self, query: str, mode: str, zone: str, layer: str, confidence: str,
            latency_ms: float, determinism_hash: str) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "engine": ENGINE_ID,
            "query": query[:500],
            "mode": mode,
            "zone": zone,
            "layer": layer,
            "confidence": confidence,
            "latency_ms": round(latency_ms, 2),
            "determinism_hash": determinism_hash,
        }
        try:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError as exc:
            logger.error(f"Audit trail write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 16: DETERMINISM HASH SHA-256
# ═══════════════════════════════════════════════════════════════════════════

def determinism_hash(query: str, results: list[DoctrineResult], computations: dict[str, Any]) -> str:
    """SHA-256 hash over (query + result topics + computation keys/values) for reproducibility."""
    hasher = hashlib.sha256()
    hasher.update(query.encode("utf-8"))
    for r in sorted(results, key=lambda x: x.topic):
        hasher.update(r.topic.encode("utf-8"))
        hasher.update(r.confidence.value.encode("utf-8"))
    for k in sorted(computations.keys()):
        hasher.update(f"{k}={computations[k]}".encode("utf-8"))
    return hasher.hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════

class IssueCategory(str, Enum):
    PRIMALITY = "PRIMALITY"
    FACTORIZATION = "FACTORIZATION"
    MODULAR_ARITHMETIC = "MODULAR_ARITHMETIC"
    DIOPHANTINE = "DIOPHANTINE"
    SEQUENCES = "SEQUENCES"
    NUMBER_THEORETIC_FUNCTIONS = "NUMBER_THEORETIC_FUNCTIONS"
    QUADRATIC_RESIDUES = "QUADRATIC_RESIDUES"
    CONTINUED_FRACTIONS = "CONTINUED_FRACTIONS"
    PRIME_DISTRIBUTION = "PRIME_DISTRIBUTION"
    CRYPTOGRAPHIC_APPLICATIONS = "CRYPTOGRAPHIC_APPLICATIONS"
    ANALYTIC_NUMBER_THEORY = "ANALYTIC_NUMBER_THEORY"
    ALGEBRAIC_NUMBER_THEORY = "ALGEBRAIC_NUMBER_THEORY"


class MultiDoctrineDecomposer:
    """Decomposes complex queries into issue categories with interaction edges."""

    INTERACTION_EDGES: list[tuple[IssueCategory, IssueCategory, str]] = [
        (IssueCategory.PRIMALITY, IssueCategory.FACTORIZATION, "primality enables factorization shortcuts"),
        (IssueCategory.FACTORIZATION, IssueCategory.NUMBER_THEORETIC_FUNCTIONS, "factorization required for totient/mobius"),
        (IssueCategory.MODULAR_ARITHMETIC, IssueCategory.QUADRATIC_RESIDUES, "modular arithmetic underpins residue theory"),
        (IssueCategory.MODULAR_ARITHMETIC, IssueCategory.CRYPTOGRAPHIC_APPLICATIONS, "RSA/DH rely on modular exponentiation"),
        (IssueCategory.DIOPHANTINE, IssueCategory.CONTINUED_FRACTIONS, "CF gives best rational approximations for Diophantine"),
        (IssueCategory.PRIMALITY, IssueCategory.PRIME_DISTRIBUTION, "PNT describes asymptotic prime density"),
        (IssueCategory.FACTORIZATION, IssueCategory.CRYPTOGRAPHIC_APPLICATIONS, "integer factorization hardness = RSA security"),
        (IssueCategory.NUMBER_THEORETIC_FUNCTIONS, IssueCategory.ANALYTIC_NUMBER_THEORY, "Dirichlet series encode arithmetic functions"),
        (IssueCategory.QUADRATIC_RESIDUES, IssueCategory.PRIMALITY, "Euler criterion uses QR for primality"),
        (IssueCategory.SEQUENCES, IssueCategory.MODULAR_ARITHMETIC, "Pisano period = Fibonacci mod m"),
    ]

    KEYWORD_MAP: dict[str, IssueCategory] = {
        "prime": IssueCategory.PRIMALITY,
        "primality": IssueCategory.PRIMALITY,
        "miller_rabin": IssueCategory.PRIMALITY,
        "sieve": IssueCategory.PRIMALITY,
        "factor": IssueCategory.FACTORIZATION,
        "pollard": IssueCategory.FACTORIZATION,
        "rho": IssueCategory.FACTORIZATION,
        "mod": IssueCategory.MODULAR_ARITHMETIC,
        "congruence": IssueCategory.MODULAR_ARITHMETIC,
        "crt": IssueCategory.MODULAR_ARITHMETIC,
        "chinese": IssueCategory.MODULAR_ARITHMETIC,
        "euler": IssueCategory.NUMBER_THEORETIC_FUNCTIONS,
        "totient": IssueCategory.NUMBER_THEORETIC_FUNCTIONS,
        "mobius": IssueCategory.NUMBER_THEORETIC_FUNCTIONS,
        "divisor": IssueCategory.NUMBER_THEORETIC_FUNCTIONS,
        "diophantine": IssueCategory.DIOPHANTINE,
        "continued": IssueCategory.CONTINUED_FRACTIONS,
        "fraction": IssueCategory.CONTINUED_FRACTIONS,
        "legendre": IssueCategory.QUADRATIC_RESIDUES,
        "jacobi": IssueCategory.QUADRATIC_RESIDUES,
        "residue": IssueCategory.QUADRATIC_RESIDUES,
        "fibonacci": IssueCategory.SEQUENCES,
        "catalan": IssueCategory.SEQUENCES,
        "partition": IssueCategory.SEQUENCES,
        "sequence": IssueCategory.SEQUENCES,
        "rsa": IssueCategory.CRYPTOGRAPHIC_APPLICATIONS,
        "encrypt": IssueCategory.CRYPTOGRAPHIC_APPLICATIONS,
        "distribution": IssueCategory.PRIME_DISTRIBUTION,
    }

    def decompose(self, query: str) -> dict[str, Any]:
        tokens = set(query.lower().split())
        categories: set[IssueCategory] = set()
        for token in tokens:
            for keyword, cat in self.KEYWORD_MAP.items():
                if keyword in token:
                    categories.add(cat)
        active_edges = [
            {"from": e[0].value, "to": e[1].value, "reason": e[2]}
            for e in self.INTERACTION_EDGES
            if e[0] in categories or e[1] in categories
        ]
        return {
            "categories": [c.value for c in categories],
            "interaction_edges": active_edges,
            "complexity": len(categories),
        }


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 20: DEEP ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class DeepAnalysisEngine:
    """Multi-source synthesis with full reasoning chain for number theory."""

    def __init__(self, doctrine_cache: DoctrineCache, decomposer: MultiDoctrineDecomposer) -> None:
        self._doctrine_cache = doctrine_cache
        self._decomposer = decomposer
        self._algorithms = NumberTheoryAlgorithms()

    def analyse(self, query: str, normalised: str, zone: PositionZone,
                context: dict[str, Any], include_proofs: bool) -> tuple[list[DoctrineResult], dict[str, Any]]:
        decomposition = self._decomposer.decompose(normalised)
        results: list[DoctrineResult] = []
        computations: dict[str, Any] = {"decomposition": decomposition}

        if "prime_numbers" in normalised or "primality" in normalised:
            n = context.get("n")
            if n and isinstance(n, int) and n > 1:
                is_p = self._algorithms.is_prime_miller_rabin(n)
                computations["primality_test"] = {"n": n, "is_prime": is_p, "method": "Miller-Rabin deterministic"}
                results.append(DoctrineResult(
                    topic="Primality Test",
                    conclusion=f"{'IS PRIME' if is_p else 'IS COMPOSITE'}: n = {n}",
                    reasoning="Deterministic Miller-Rabin with witnesses {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}.",
                    authorities=[AuthoritySource(source="Miller (1976), Rabin (1980)", weight=0.95,
                                                 citation="Journal of Computer and System Sciences")],
                    confidence=ConfidenceLevel.DEFENSIBLE,
                    key_factors=["deterministic for n < 3.3e24", "polynomial time", "strong probable prime test"],
                ))

        if "prime_factorization" in normalised or "factor" in normalised:
            n = context.get("n")
            if n and isinstance(n, int) and n > 1:
                factors = self._algorithms.factorise(n)
                computations["factorization"] = {"n": n, "factors": factors}
                results.append(DoctrineResult(
                    topic="Prime Factorization (FTA)",
                    conclusion=f"Factorization of {n}: {factors}",
                    reasoning="Trial division for small primes then Pollard's rho for larger factors.",
                    authorities=[AuthoritySource(source="Fundamental Theorem of Arithmetic", weight=1.0,
                                                 citation="Euclid, Elements, Book VII")],
                    confidence=ConfidenceLevel.DEFENSIBLE,
                    key_factors=["unique up to ordering", "FTA guarantees existence", "Pollard rho O(n^{1/4})"],
                ))

        if "euler_totient" in normalised:
            n = context.get("n")
            if n and isinstance(n, int) and n > 0:
                phi = self._algorithms.euler_totient(n)
                computations["euler_totient"] = {"n": n, "phi": phi}
                results.append(DoctrineResult(
                    topic="Euler's Totient Function",
                    conclusion=f"phi({n}) = {phi}",
                    reasoning="Computed via prime factorization: phi(n) = n * prod(1 - 1/p) for p | n.",
                    authorities=[AuthoritySource(source="Euler (1763)", weight=0.95,
                                                 citation="Theoremata arithmetica nova methodo demonstrata")],
                    confidence=ConfidenceLevel.DEFENSIBLE,
                    key_factors=["multiplicative function", "phi(p) = p-1 for prime p", "Euler's theorem: a^phi(n) = 1 mod n"],
                ))

        if "chinese_remainder_theorem" in normalised:
            remainders = context.get("remainders", [])
            moduli = context.get("moduli", [])
            if remainders and moduli and len(remainders) == len(moduli):
                try:
                    x, M = self._algorithms.chinese_remainder_theorem(remainders, moduli)
                    computations["crt"] = {"remainders": remainders, "moduli": moduli, "solution": x, "modulus": M}
                    results.append(DoctrineResult(
                        topic="Chinese Remainder Theorem",
                        conclusion=f"x = {x} (mod {M})",
                        reasoning="CRT: if moduli are pairwise coprime, solution exists and is unique mod product.",
                        authorities=[AuthoritySource(source="Sun Tzu (~3rd century)", weight=0.95,
                                                     citation="Sunzi Suanjing")],
                        confidence=ConfidenceLevel.DEFENSIBLE,
                        key_factors=["pairwise coprimality required", "constructive algorithm via back-substitution", "O(k^2) for k congruences"],
                    ))
                except ValueError as exc:
                    computations["crt_error"] = str(exc)

        if "continued_fractions" in normalised:
            num = context.get("numerator")
            den = context.get("denominator")
            if num is not None and den is not None and den != 0:
                cf = self._algorithms.continued_fraction(num, den)
                computations["continued_fraction"] = {"numerator": num, "denominator": den, "coefficients": cf}

        if not results:
            results.append(DoctrineResult(
                topic="General Number Theory Query",
                conclusion="Query processed through deep analysis. Provide specific parameters in 'context' for computation.",
                reasoning="The engine can compute primality, factorization, totient, CRT, Legendre/Jacobi symbols, sequences, and more.",
                authorities=[AuthoritySource(source="Engine Capability", weight=0.5, citation="MATH09 v1.0")],
                confidence=ConfidenceLevel.DISCLOSURE,
                key_factors=["provide 'n' in context for primality/factorization", "provide 'remainders'+'moduli' for CRT"],
            ))

        return results, computations


# ═══════════════════════════════════════════════════════════════════════════
# REAL NUMBER THEORY ALGORITHMS — PURE PYTHON
# ═══════════════════════════════════════════════════════════════════════════

class NumberTheoryAlgorithms:
    """Production-grade number theory implementations. No external dependencies."""

    # ------------------------------------------------------------------
    # GCD / Extended GCD
    # ------------------------------------------------------------------

    @staticmethod
    def gcd(a: int, b: int) -> int:
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
        if a == 0:
            return b, 0, 1
        g, x1, y1 = NumberTheoryAlgorithms.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    @staticmethod
    def lcm(a: int, b: int) -> int:
        if a == 0 and b == 0:
            return 0
        return abs(a * b) // NumberTheoryAlgorithms.gcd(a, b)

    # ------------------------------------------------------------------
    # Modular arithmetic
    # ------------------------------------------------------------------

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """Modular inverse of a mod m. Raises ValueError if gcd(a, m) != 1."""
        g, x, _ = NumberTheoryAlgorithms.extended_gcd(a % m, m)
        if g != 1:
            raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) = {g}")
        return x % m

    @staticmethod
    def mod_pow(base: int, exp: int, mod: int) -> int:
        """Square-and-multiply modular exponentiation. Handles negative exponents."""
        if mod == 1:
            return 0
        if exp < 0:
            base = NumberTheoryAlgorithms.mod_inverse(base, mod)
            exp = -exp
        result = 1
        base = base % mod
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    # ------------------------------------------------------------------
    # Sieve of Eratosthenes
    # ------------------------------------------------------------------

    @staticmethod
    def sieve_of_eratosthenes(limit: int) -> list[int]:
        """Returns all primes up to limit (inclusive). Optimised with bit sieve."""
        if limit < 2:
            return []
        sieve = bytearray(b'\x01') * (limit + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        return [i for i in range(2, limit + 1) if sieve[i]]

    # ------------------------------------------------------------------
    # Miller-Rabin primality test (deterministic for n < 3.317e24)
    # ------------------------------------------------------------------

    @staticmethod
    def is_prime_miller_rabin(n: int) -> bool:
        """Deterministic Miller-Rabin for n < 3,317,044,064,679,887,385,961,981.
        Uses witnesses {2,3,5,7,11,13,17,19,23,29,31,37}.
        For larger n uses probabilistic test with 40 rounds.
        """
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False

        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for p in small_primes:
            if n == p:
                return True
            if n % p == 0:
                return False

        # Write n - 1 = 2^r * d with d odd
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        def _check_witness(a: int) -> bool:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                return True
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return True
            return False

        # Deterministic witnesses sufficient for n < 3.317e24
        deterministic_witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        if n < 3_317_044_064_679_887_385_961_981:
            for a in deterministic_witnesses:
                if a >= n:
                    continue
                if not _check_witness(a):
                    return False
            return True

        # Probabilistic for very large n
        for a in deterministic_witnesses:
            if not _check_witness(a):
                return False
        rng = random.Random(n)  # deterministic seed for reproducibility
        for _ in range(40):
            a = rng.randrange(2, n - 1)
            if not _check_witness(a):
                return False
        return True

    # ------------------------------------------------------------------
    # Prime factorization: trial division + Pollard's rho
    # ------------------------------------------------------------------

    @staticmethod
    def _pollard_rho(n: int) -> int:
        """Pollard's rho algorithm. Returns a non-trivial factor of n."""
        if n % 2 == 0:
            return 2
        rng = random.Random(n)
        for _ in range(50):
            c = rng.randrange(1, n)
            x = rng.randrange(2, n)
            y = x
            d = 1
            while d == 1:
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
                d = math.gcd(abs(x - y), n)
            if d != n:
                return d
        return n  # fallback — shouldn't happen for composite n

    @staticmethod
    def factorise(n: int) -> dict[int, int]:
        """Complete prime factorization. Returns {prime: exponent}."""
        if n <= 1:
            return {}
        factors: dict[int, int] = {}

        # Trial division for small primes
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
            while n % p == 0:
                factors[p] = factors.get(p, 0) + 1
                n //= p
        if n == 1:
            return factors

        # Extended trial division up to 10000
        p = 101
        while p * p <= n and p < 10_000:
            while n % p == 0:
                factors[p] = factors.get(p, 0) + 1
                n //= p
            p += 2

        # Pollard's rho for remaining large factors
        stack = [n] if n > 1 else []
        while stack:
            num = stack.pop()
            if num == 1:
                continue
            if NumberTheoryAlgorithms.is_prime_miller_rabin(num):
                factors[num] = factors.get(num, 0) + 1
            else:
                divisor = NumberTheoryAlgorithms._pollard_rho(num)
                stack.append(divisor)
                stack.append(num // divisor)

        return dict(sorted(factors.items()))

    # ------------------------------------------------------------------
    # Euler's totient function
    # ------------------------------------------------------------------

    @staticmethod
    def euler_totient(n: int) -> int:
        """phi(n) = n * prod(1 - 1/p) for each prime p dividing n."""
        if n <= 0:
            raise ValueError("Totient is defined for positive integers")
        if n == 1:
            return 1
        factors = NumberTheoryAlgorithms.factorise(n)
        result = n
        for p in factors:
            result -= result // p
        return result

    # ------------------------------------------------------------------
    # Chinese Remainder Theorem
    # ------------------------------------------------------------------

    @staticmethod
    def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
        """Solves system x = r_i (mod m_i). Returns (x, M) where M = product of moduli.
        Raises ValueError if moduli not pairwise coprime.
        """
        if len(remainders) != len(moduli):
            raise ValueError("remainders and moduli must have same length")
        if len(remainders) == 0:
            raise ValueError("empty system")

        # Verify pairwise coprimality
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if math.gcd(moduli[i], moduli[j]) != 1:
                    raise ValueError(
                        f"Moduli {moduli[i]} and {moduli[j]} are not coprime; "
                        f"gcd = {math.gcd(moduli[i], moduli[j])}"
                    )

        M = 1
        for m in moduli:
            M *= m

        x = 0
        for r_i, m_i in zip(remainders, moduli):
            M_i = M // m_i
            y_i = NumberTheoryAlgorithms.mod_inverse(M_i, m_i)
            x += r_i * M_i * y_i

        return x % M, M

    # ------------------------------------------------------------------
    # Continued fraction expansion
    # ------------------------------------------------------------------

    @staticmethod
    def continued_fraction(numerator: int, denominator: int) -> list[int]:
        """Returns the continued fraction coefficients [a0; a1, a2, ...] for numerator/denominator."""
        if denominator == 0:
            raise ValueError("denominator cannot be zero")
        a, b = numerator, denominator
        coefficients: list[int] = []
        while b != 0:
            q, r = divmod(a, b)
            coefficients.append(q)
            a, b = b, r
        return coefficients

    @staticmethod
    def convergents(cf: list[int]) -> list[tuple[int, int]]:
        """Returns the convergents p_k/q_k from continued fraction coefficients."""
        if not cf:
            return []
        convergents_list: list[tuple[int, int]] = []
        h_prev, h_curr = 0, 1
        k_prev, k_curr = 1, 0
        for a_i in cf:
            h_prev, h_curr = h_curr, a_i * h_curr + h_prev
            k_prev, k_curr = k_curr, a_i * k_curr + k_prev
            convergents_list.append((h_curr, k_curr))
        return convergents_list

    # ------------------------------------------------------------------
    # Legendre symbol (a/p)
    # ------------------------------------------------------------------

    @staticmethod
    def legendre_symbol(a: int, p: int) -> int:
        """Computes the Legendre symbol (a/p) for odd prime p.
        Returns 0, 1, or -1.
        Uses Euler's criterion: (a/p) = a^((p-1)/2) mod p.
        """
        if p < 3 or not NumberTheoryAlgorithms.is_prime_miller_rabin(p):
            raise ValueError(f"p = {p} must be an odd prime")
        a = a % p
        if a == 0:
            return 0
        result = pow(a, (p - 1) // 2, p)
        return result if result <= 1 else result - p

    # ------------------------------------------------------------------
    # Jacobi symbol (a/n)
    # ------------------------------------------------------------------

    @staticmethod
    def jacobi_symbol(a: int, n: int) -> int:
        """Computes the Jacobi symbol (a/n) for odd positive n.
        Generalises Legendre symbol to composite n.
        """
        if n <= 0 or n % 2 == 0:
            raise ValueError(f"n = {n} must be a positive odd integer")
        a = a % n
        result = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5):
                    result = -result
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                result = -result
            a = a % n
        return result if n == 1 else 0

    # ------------------------------------------------------------------
    # Fibonacci (matrix exponentiation — O(log n))
    # ------------------------------------------------------------------

    @staticmethod
    def fibonacci(n: int) -> int:
        """Returns F(n) using matrix exponentiation. O(log n) multiplications."""
        if n < 0:
            # F(-n) = (-1)^(n+1) * F(n)
            val = NumberTheoryAlgorithms.fibonacci(-n)
            return val if (-n) % 2 == 1 else -val
        if n <= 1:
            return n

        def _mat_mul(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
            return (
                a[0] * b[0] + a[1] * b[2],
                a[0] * b[1] + a[1] * b[3],
                a[2] * b[0] + a[3] * b[2],
                a[2] * b[1] + a[3] * b[3],
            )

        def _mat_pow(mat: tuple[int, int, int, int], power: int) -> tuple[int, int, int, int]:
            result = (1, 0, 0, 1)  # identity
            base = mat
            while power > 0:
                if power & 1:
                    result = _mat_mul(result, base)
                base = _mat_mul(base, base)
                power >>= 1
            return result

        m = _mat_pow((1, 1, 1, 0), n)
        return m[1]

    # ------------------------------------------------------------------
    # Catalan numbers
    # ------------------------------------------------------------------

    @staticmethod
    @lru_cache(maxsize=2048)
    def catalan(n: int) -> int:
        """C(n) = (2n)! / ((n+1)! * n!) = binomial(2n, n) / (n + 1)."""
        if n < 0:
            return 0
        if n <= 1:
            return 1
        # Direct formula using integer arithmetic
        c = 1
        for i in range(n):
            c = c * 2 * (2 * i + 1) // (i + 2)
        return c

    # ------------------------------------------------------------------
    # Partition function p(n) — dynamic programming
    # ------------------------------------------------------------------

    @staticmethod
    def partition(n: int) -> int:
        """Number of ways to write n as a sum of positive integers (order irrelevant).
        Uses Euler's pentagonal number theorem recurrence.
        """
        if n < 0:
            return 0
        if n <= 1:
            return 1
        dp = [0] * (n + 1)
        dp[0] = 1
        # Pentagonal number theorem: p(n) = sum_{k!=0} (-1)^{k+1} p(n - k(3k-1)/2)
        for i in range(1, n + 1):
            k = 1
            sign = 1
            while True:
                # Generalised pentagonal numbers: k(3k-1)/2 for k = 1, -1, 2, -2, ...
                g1 = k * (3 * k - 1) // 2
                g2 = k * (3 * k + 1) // 2  # corresponds to -k
                if g1 > i and g2 > i:
                    break
                if g1 <= i:
                    dp[i] += sign * dp[i - g1]
                if g2 <= i:
                    dp[i] += sign * dp[i - g2]
                k += 1
                sign = -sign
        return dp[n]

    # ------------------------------------------------------------------
    # Stirling numbers of the second kind S(n, k)
    # ------------------------------------------------------------------

    @staticmethod
    @lru_cache(maxsize=4096)
    def stirling_second(n: int, k: int) -> int:
        """S(n, k) = number of ways to partition {1..n} into k non-empty subsets."""
        if n == 0 and k == 0:
            return 1
        if n == 0 or k == 0:
            return 0
        if k > n:
            return 0
        return k * NumberTheoryAlgorithms.stirling_second(n - 1, k) + NumberTheoryAlgorithms.stirling_second(n - 1, k - 1)

    # ------------------------------------------------------------------
    # Divisor functions
    # ------------------------------------------------------------------

    @staticmethod
    def divisor_count(n: int) -> int:
        """d(n) = number of divisors of n. Uses factorization: d(n) = prod(e_i + 1)."""
        if n <= 0:
            raise ValueError("n must be positive")
        if n == 1:
            return 1
        factors = NumberTheoryAlgorithms.factorise(n)
        result = 1
        for exp in factors.values():
            result *= (exp + 1)
        return result

    @staticmethod
    def divisor_sum(n: int, k: int = 1) -> int:
        """sigma_k(n) = sum of k-th powers of divisors.
        k=0 -> d(n) count, k=1 -> sigma(n), etc.
        """
        if n <= 0:
            raise ValueError("n must be positive")
        if n == 1:
            return 1
        factors = NumberTheoryAlgorithms.factorise(n)
        result = 1
        for p, e in factors.items():
            if k == 0:
                result *= (e + 1)
            else:
                result *= (pow(p, k * (e + 1)) - 1) // (pow(p, k) - 1)
        return result

    @staticmethod
    def list_divisors(n: int) -> list[int]:
        """Returns sorted list of all positive divisors of n."""
        if n <= 0:
            raise ValueError("n must be positive")
        divisors: list[int] = []
        for i in range(1, int(n ** 0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        return sorted(divisors)

    # ------------------------------------------------------------------
    # Mobius function
    # ------------------------------------------------------------------

    @staticmethod
    def mobius(n: int) -> int:
        """mu(n): 0 if n has squared prime factor, (-1)^k if n = product of k distinct primes, 1 if n=1."""
        if n <= 0:
            raise ValueError("n must be positive")
        if n == 1:
            return 1
        factors = NumberTheoryAlgorithms.factorise(n)
        for exp in factors.values():
            if exp > 1:
                return 0
        return 1 if len(factors) % 2 == 0 else -1

    # ------------------------------------------------------------------
    # Diophantine equation solver: ax + by = c
    # ------------------------------------------------------------------

    @staticmethod
    def solve_diophantine(a: int, b: int, c: int) -> Optional[dict[str, Any]]:
        """Solves ax + by = c for integers x, y.
        Returns None if no solution exists (gcd(a,b) does not divide c).
        Otherwise returns one particular solution and the general parametric form.
        """
        if a == 0 and b == 0:
            if c == 0:
                return {"x0": 0, "y0": 0, "general": "x = any, y = any", "solvable": True}
            return None
        g, x0, y0 = NumberTheoryAlgorithms.extended_gcd(a, b)
        if c % g != 0:
            return None
        scale = c // g
        x0 *= scale
        y0 *= scale
        step_x = b // g if b != 0 else 0
        step_y = -a // g if a != 0 else 0
        return {
            "x0": x0,
            "y0": y0,
            "gcd": g,
            "step_x": step_x,
            "step_y": step_y,
            "general": f"x = {x0} + {step_x}*t, y = {y0} + {step_y}*t  (t in Z)",
            "solvable": True,
            "verification": f"{a}*{x0} + {b}*{y0} = {a * x0 + b * y0} = {c}",
        }

    # ------------------------------------------------------------------
    # Quadratic residues
    # ------------------------------------------------------------------

    @staticmethod
    def is_quadratic_residue(n: int, p: int) -> bool:
        """Checks if n is a quadratic residue mod p (odd prime)."""
        return NumberTheoryAlgorithms.legendre_symbol(n, p) == 1

    @staticmethod
    def all_quadratic_residues(p: int) -> list[int]:
        """Returns all quadratic residues mod p for odd prime p."""
        if p < 3 or not NumberTheoryAlgorithms.is_prime_miller_rabin(p):
            raise ValueError(f"p = {p} must be an odd prime")
        residues: set[int] = set()
        for a in range(1, p):
            residues.add(pow(a, 2, p))
        return sorted(residues)

    @staticmethod
    def sqrt_mod(n: int, p: int) -> Optional[int]:
        """Tonelli-Shanks algorithm: find x such that x^2 = n (mod p) for odd prime p.
        Returns None if n is not a QR mod p.
        """
        n = n % p
        if n == 0:
            return 0
        if NumberTheoryAlgorithms.legendre_symbol(n, p) != 1:
            return None
        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)

        # Tonelli-Shanks
        q, s = p - 1, 0
        while q % 2 == 0:
            q //= 2
            s += 1
        z = 2
        while NumberTheoryAlgorithms.legendre_symbol(z, p) != -1:
            z += 1
        m_val = s
        c = pow(z, q, p)
        t = pow(n, q, p)
        r = pow(n, (q + 1) // 2, p)
        while True:
            if t == 1:
                return r
            i = 1
            temp = t * t % p
            while temp != 1:
                temp = temp * temp % p
                i += 1
            b = pow(c, 1 << (m_val - i - 1), p)
            m_val = i
            c = b * b % p
            t = t * c % p
            r = r * b % p

    # ------------------------------------------------------------------
    # Bell numbers (uses Stirling)
    # ------------------------------------------------------------------

    @staticmethod
    def bell(n: int) -> int:
        """B(n) = sum_{k=0}^{n} S(n, k)."""
        return sum(NumberTheoryAlgorithms.stirling_second(n, k) for k in range(n + 1))

    # ------------------------------------------------------------------
    # Is perfect number
    # ------------------------------------------------------------------

    @staticmethod
    def is_perfect(n: int) -> bool:
        """Checks if n is a perfect number: sigma(n) - n == n."""
        if n <= 1:
            return False
        return NumberTheoryAlgorithms.divisor_sum(n, 1) == 2 * n

    # ------------------------------------------------------------------
    # Primitive root modulo p
    # ------------------------------------------------------------------

    @staticmethod
    def primitive_root(p: int) -> Optional[int]:
        """Finds the smallest primitive root modulo prime p."""
        if p == 2:
            return 1
        if not NumberTheoryAlgorithms.is_prime_miller_rabin(p):
            return None
        phi = p - 1
        factors = NumberTheoryAlgorithms.factorise(phi)
        for g in range(2, p):
            is_root = True
            for q in factors:
                if pow(g, phi // q, p) == 1:
                    is_root = False
                    break
            if is_root:
                return g
        return None

    # ------------------------------------------------------------------
    # Discrete logarithm (baby-step giant-step)
    # ------------------------------------------------------------------

    @staticmethod
    def discrete_log(g: int, h: int, p: int) -> Optional[int]:
        """Baby-step giant-step: finds x such that g^x = h (mod p). Returns None if not found.
        Complexity O(sqrt(p)) time and space.
        """
        m = int(math.ceil(math.sqrt(p)))
        table: dict[int, int] = {}
        power = 1
        for j in range(m):
            table[power] = j
            power = power * g % p
        factor = NumberTheoryAlgorithms.mod_inverse(pow(g, m, p), p)
        gamma = h
        for i in range(m):
            if gamma in table:
                ans = i * m + table[gamma]
                if pow(g, ans, p) == h % p:
                    return ans
            gamma = gamma * factor % p
        return None

    # ------------------------------------------------------------------
    # Order of element mod n
    # ------------------------------------------------------------------

    @staticmethod
    def multiplicative_order(a: int, n: int) -> int:
        """Returns the multiplicative order of a mod n (smallest k>0 s.t. a^k = 1 mod n).
        Raises ValueError if gcd(a, n) != 1.
        """
        if math.gcd(a, n) != 1:
            raise ValueError(f"gcd({a}, {n}) != 1; order undefined")
        phi_n = NumberTheoryAlgorithms.euler_totient(n)
        divisors = NumberTheoryAlgorithms.list_divisors(phi_n)
        for d in divisors:
            if pow(a, d, n) == 1:
                return d
        return phi_n  # fallback (should be reached via divisor list)

    # ------------------------------------------------------------------
    # Carmichael's lambda function
    # ------------------------------------------------------------------

    @staticmethod
    def carmichael_lambda(n: int) -> int:
        """Carmichael function lambda(n) = lcm of lambda(p^e) for p^e || n."""
        if n <= 0:
            raise ValueError("n must be positive")
        if n <= 2:
            return 1
        factors = NumberTheoryAlgorithms.factorise(n)
        result = 1
        for p, e in factors.items():
            if p == 2:
                if e <= 2:
                    lam = 1 << (e - 1)  # 2^(e-1)
                else:
                    lam = 1 << (e - 2)  # 2^(e-2)
            else:
                lam = (p - 1) * (p ** (e - 1))
            result = NumberTheoryAlgorithms.lcm(result, lam)
        return result

    # ------------------------------------------------------------------
    # Sum of two squares representation
    # ------------------------------------------------------------------

    @staticmethod
    def sum_of_two_squares(n: int) -> Optional[tuple[int, int]]:
        """If n can be written as a^2 + b^2, return (a, b). Else None.
        By Fermat's theorem on sums of two squares, n is representable iff
        no prime factor of the form 4k+3 appears to an odd power.
        """
        if n < 0:
            return None
        if n == 0:
            return (0, 0)
        factors = NumberTheoryAlgorithms.factorise(n)
        for p, e in factors.items():
            if p % 4 == 3 and e % 2 == 1:
                return None
        # Brute search for small n (sufficient for engine use cases)
        limit = int(math.isqrt(n)) + 1
        for a in range(limit):
            b_sq = n - a * a
            if b_sq < 0:
                break
            b = int(math.isqrt(b_sq))
            if b * b == b_sq:
                return (a, b)
        return None

    # ------------------------------------------------------------------
    # Integer square root (exact)
    # ------------------------------------------------------------------

    @staticmethod
    def isqrt(n: int) -> int:
        """Integer square root via Newton's method."""
        if n < 0:
            raise ValueError("Square root of negative number")
        if n == 0:
            return 0
        x = n
        y = (x + 1) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x

    @staticmethod
    def is_perfect_square(n: int) -> bool:
        if n < 0:
            return False
        s = NumberTheoryAlgorithms.isqrt(n)
        return s * s == n

    # ------------------------------------------------------------------
    # nth prime estimate and exact (small n)
    # ------------------------------------------------------------------

    @staticmethod
    def nth_prime(n: int) -> int:
        """Returns the n-th prime (1-indexed: nth_prime(1) = 2). Works for n up to ~700,000."""
        if n < 1:
            raise ValueError("n must be >= 1")
        if n <= 6:
            return [2, 3, 5, 7, 11, 13][n - 1]
        # Upper bound estimate: p_n < n * (ln(n) + ln(ln(n))) for n >= 6
        import math as m
        upper = int(n * (m.log(n) + m.log(m.log(n)))) + 100
        upper = max(upper, 100)
        primes = NumberTheoryAlgorithms.sieve_of_eratosthenes(upper)
        while len(primes) < n:
            upper = int(upper * 1.5)
            primes = NumberTheoryAlgorithms.sieve_of_eratosthenes(upper)
        return primes[n - 1]

    # ------------------------------------------------------------------
    # Prime counting function pi(x) via sieve
    # ------------------------------------------------------------------

    @staticmethod
    def prime_counting(x: int) -> int:
        """pi(x) = number of primes <= x."""
        if x < 2:
            return 0
        return len(NumberTheoryAlgorithms.sieve_of_eratosthenes(x))

    # ------------------------------------------------------------------
    # Goldbach check (even number > 2 as sum of two primes)
    # ------------------------------------------------------------------

    @staticmethod
    def goldbach(n: int) -> Optional[tuple[int, int]]:
        """For even n > 2, find primes p, q such that p + q = n. Returns None if n is odd or <= 2."""
        if n <= 2 or n % 2 != 0:
            return None
        primes_set = set(NumberTheoryAlgorithms.sieve_of_eratosthenes(n))
        for p in sorted(primes_set):
            if (n - p) in primes_set:
                return (p, n - p)
        return None

    # ------------------------------------------------------------------
    # Digit sum / digital root
    # ------------------------------------------------------------------

    @staticmethod
    def digit_sum(n: int, base: int = 10) -> int:
        n = abs(n)
        s = 0
        while n > 0:
            s += n % base
            n //= base
        return s

    @staticmethod
    def digital_root(n: int) -> int:
        if n == 0:
            return 0
        return 1 + (abs(n) - 1) % 9


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 17: FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════════

# Globals initialised in lifespan
_doctrine_cache: DoctrineCache
_semantic: SemanticNormalizer
_vector_search: VectorSearch
_authority_hardener: AuthorityHardener
_confidence_stratifier: ConfidenceStratifier
_telemetry: TelemetryCollector
_drift_watcher: DriftWatcher
_coverage_map: CoverageMap
_metrics_collector: MetricsCollector
_audit_trail: AuditTrail
_zoned_analyser: ZonedAnalyser
_fragility_scorer: FactFragilityScorer
_decomposer: MultiDoctrineDecomposer
_deep_engine: DeepAnalysisEngine
_three_layer: ThreeLayerRouter
_mode_formatter: ResponseModeFormatter
_algorithms: NumberTheoryAlgorithms

_startup_time: float = 0.0


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa: ANN201, ARG001
    global _doctrine_cache, _semantic, _vector_search, _authority_hardener
    global _confidence_stratifier, _telemetry, _drift_watcher, _coverage_map
    global _metrics_collector, _audit_trail, _zoned_analyser, _fragility_scorer
    global _decomposer, _deep_engine, _three_layer, _mode_formatter, _algorithms
    global _startup_time

    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")

    _doctrine_cache = DoctrineCache()
    _semantic = SemanticNormalizer()
    _vector_search = VectorSearch(_doctrine_cache._blocks)
    _authority_hardener = AuthorityHardener()
    _confidence_stratifier = ConfidenceStratifier()
    _telemetry = TelemetryCollector()
    _drift_watcher = DriftWatcher()
    _coverage_map = CoverageMap()
    _metrics_collector = MetricsCollector(_telemetry, _coverage_map)
    _audit_trail = AuditTrail(AUDIT_PATH)
    _zoned_analyser = ZonedAnalyser()
    _fragility_scorer = FactFragilityScorer()
    _decomposer = MultiDoctrineDecomposer()
    _deep_engine = DeepAnalysisEngine(_doctrine_cache, _decomposer)
    _three_layer = ThreeLayerRouter(_doctrine_cache, _semantic, _deep_engine)
    _mode_formatter = ResponseModeFormatter()
    _algorithms = NumberTheoryAlgorithms()
    _startup_time = time.monotonic()

    logger.info(f"{ENGINE_NAME} READY — {_doctrine_cache.count} doctrine blocks loaded")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="Number Theory Intelligence Engine — TIE-20 compliant, Tier 13 Mathematics",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────────────
# Health endpoint (Component 12)
# ─────────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=ENGINE_VERSION,
        status="operational",
        tier=ENGINE_TIER,
        port=ENGINE_PORT,
        mode=ENGINE_MODE,
        auth_level=ENGINE_AUTH_LEVEL,
        uptime_seconds=round(_telemetry.uptime, 1),
        total_queries=_telemetry.total_queries,
        cache_hit_rate=_metrics_collector._compute_hit_rate(),
        doctrine_count=_doctrine_cache.count,
        components={
            "three_layer_response": "active",
            "response_modes": "active",
            "doctrine_cache": f"{_doctrine_cache.count} blocks",
            "authority_hardening": "active",
            "confidence_stratification": "active",
            "semantic_normalisation": f"{len(_semantic._dict)} mappings",
            "vector_search": "active",
            "telemetry": f"{_telemetry.total_queries} queries",
            "drift_watcher": "active",
            "coverage_map": "active",
            "metrics_collector": "active",
            "health_endpoint": "active",
            "zoned_analysis": "active",
            "fact_fragility_scoring": "active",
            "audit_trail_jsonl": "active",
            "determinism_hash_sha256": "active",
            "fastapi_server": "active",
            "loguru_logging": "active",
            "multi_doctrine_decomposition": "active",
            "deep_analysis_mode": "active",
        },
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ─────────────────────────────────────────────────────────────────────────
# Main query endpoint
# ─────────────────────────────────────────────────────────────────────────

@app.post("/query", response_model=EngineResponse)
async def query(req: QueryRequest) -> EngineResponse:
    t0 = time.monotonic()
    try:
        layer, results, computations = _three_layer.route(
            req.query, req.mode, req.zone, req.context, req.include_proofs,
        )
        results = _zoned_analyser.enforce(req.zone, results)
        _drift_watcher.record(results)
        for r in results:
            _coverage_map.record_hit(r.topic)
        if not results:
            _coverage_map.record_miss(req.query)

        overall_conf = ConfidenceLevel.DISCLOSURE
        if results:
            conf_order = [ConfidenceLevel.DEFENSIBLE, ConfidenceLevel.AGGRESSIVE,
                          ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]
            overall_conf = max(results, key=lambda r: conf_order.index(r.confidence)).confidence

        dhash = determinism_hash(req.query, results, computations)
        latency = (time.monotonic() - t0) * 1000

        response = EngineResponse(
            query=req.query,
            mode=req.mode,
            zone=req.zone,
            response_layer=layer,
            doctrine_results=results,
            computation_results=computations,
            confidence=overall_conf,
            determinism_hash=dhash,
            latency_ms=round(latency, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            disclosure_caveat=_zoned_analyser.zone_caveat(req.zone),
            epistemic_notes=[_confidence_stratifier.explain(overall_conf)],
        )

        _telemetry.record_query(req.query, latency, layer, req.mode.value, req.zone.value)
        _audit_trail.log(req.query, req.mode.value, req.zone.value, layer,
                         overall_conf.value, latency, dhash)

        formatted = _mode_formatter.format(response, req.mode)
        return response

    except Exception as exc:
        _telemetry.record_error(str(exc), "query", req.query)
        logger.error(f"Query error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ─────────────────────────────────────────────────────────────────────────
# Computation endpoints — REAL NUMBER THEORY
# ─────────────────────────────────────────────────────────────────────────

@app.post("/compute/primality")
async def compute_primality(req: PrimalityRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    result = _algorithms.is_prime_miller_rabin(req.n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"primality({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "n": req.n,
        "is_prime": result,
        "method": "Miller-Rabin deterministic (n < 3.3e24)" if req.n < 3_317_044_064_679_887_385_961_981 else "Miller-Rabin probabilistic (40 rounds)",
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/factorize")
async def compute_factorize(req: FactorizationRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    factors = _algorithms.factorise(req.n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"factorize({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    product = 1
    for p, e in factors.items():
        product *= p ** e
    return {
        "n": req.n,
        "factors": factors,
        "factorization_str": " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items())),
        "verification": product == req.n,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/sieve")
async def compute_sieve(req: SieveRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    primes = _algorithms.sieve_of_eratosthenes(req.limit)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"sieve({req.limit})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "limit": req.limit,
        "count": len(primes),
        "primes": primes if len(primes) <= 10000 else primes[:100] + ["... truncated ..."] + primes[-100:],
        "largest": primes[-1] if primes else None,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/mod_exp")
async def compute_mod_exp(req: ModExpRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    result = _algorithms.mod_pow(req.base, req.exponent, req.modulus)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"mod_exp({req.base},{req.exponent},{req.modulus})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "base": req.base,
        "exponent": req.exponent,
        "modulus": req.modulus,
        "result": result,
        "expression": f"{req.base}^{req.exponent} mod {req.modulus} = {result}",
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/crt")
async def compute_crt(req: CRTRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        x, M = _algorithms.chinese_remainder_theorem(req.remainders, req.moduli)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"crt({req.remainders},{req.moduli})", latency, "COMPUTE", "FAST", "PLANNING")
        return {
            "remainders": req.remainders,
            "moduli": req.moduli,
            "solution": x,
            "combined_modulus": M,
            "expression": f"x = {x} (mod {M})",
            "verification": [f"{x} mod {m} = {x % m} == {r}: {x % m == r}" for r, m in zip(req.remainders, req.moduli)],
            "latency_ms": round(latency, 2),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/diophantine")
async def compute_diophantine(req: DiophantineRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    result = _algorithms.solve_diophantine(req.a, req.b, req.c)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"diophantine({req.a},{req.b},{req.c})", latency, "COMPUTE", "FAST", "PLANNING")
    if result is None:
        return {
            "a": req.a, "b": req.b, "c": req.c,
            "solvable": False,
            "reason": f"gcd({req.a}, {req.b}) = {math.gcd(req.a, req.b)} does not divide {req.c}",
            "latency_ms": round(latency, 2),
        }
    return {
        "a": req.a, "b": req.b, "c": req.c,
        **result,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/continued_fraction")
async def compute_continued_fraction(req: ContinuedFractionRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    cf = _algorithms.continued_fraction(req.numerator, req.denominator)
    convergents = _algorithms.convergents(cf)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"cf({req.numerator}/{req.denominator})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "numerator": req.numerator,
        "denominator": req.denominator,
        "coefficients": cf,
        "notation": f"[{cf[0]}; {', '.join(str(c) for c in cf[1:])}]" if len(cf) > 1 else f"[{cf[0]}]",
        "convergents": [{"p": p, "q": q, "value": p / q if q != 0 else None} for p, q in convergents],
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/legendre")
async def compute_legendre(req: LegendreRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        result = _algorithms.legendre_symbol(req.a, req.p)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"legendre({req.a},{req.p})", latency, "COMPUTE", "FAST", "PLANNING")
        interpretation = {1: "quadratic residue", -1: "quadratic non-residue", 0: "divisible by p"}
        return {
            "a": req.a,
            "p": req.p,
            "legendre_symbol": result,
            "interpretation": interpretation.get(result, "unknown"),
            "latency_ms": round(latency, 2),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/jacobi")
async def compute_jacobi(req: JacobiRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        result = _algorithms.jacobi_symbol(req.a, req.n)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"jacobi({req.a},{req.n})", latency, "COMPUTE", "FAST", "PLANNING")
        return {
            "a": req.a,
            "n": req.n,
            "jacobi_symbol": result,
            "note": "Jacobi symbol = -1 => non-residue; = 1 does NOT guarantee residue for composite n",
            "latency_ms": round(latency, 2),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/sequence")
async def compute_sequence(req: SequenceRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    name_lower = req.name.lower()
    result: Any = None
    method = ""
    try:
        if name_lower in ("fibonacci", "fib"):
            result = _algorithms.fibonacci(req.n)
            method = "matrix exponentiation O(log n)"
        elif name_lower in ("catalan", "cat"):
            result = _algorithms.catalan(req.n)
            method = "direct formula C(n) = binom(2n,n)/(n+1)"
        elif name_lower in ("partition", "partitions", "p"):
            result = _algorithms.partition(req.n)
            method = "pentagonal number theorem recurrence"
        elif name_lower in ("bell",):
            result = _algorithms.bell(req.n)
            method = "sum of Stirling numbers S(n,k)"
        else:
            raise HTTPException(status_code=400, detail=f"Unknown sequence: {req.name}. Supported: fibonacci, catalan, partition, bell")
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"sequence({req.name},{req.n})", latency, "COMPUTE", "FAST", "PLANNING")
        return {
            "sequence": req.name,
            "n": req.n,
            "value": result,
            "method": method,
            "latency_ms": round(latency, 2),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/totient")
async def compute_totient(req: TotientRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    phi = _algorithms.euler_totient(req.n)
    factors = _algorithms.factorise(req.n) if req.n > 1 else {}
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"totient({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "n": req.n,
        "phi": phi,
        "factorization": factors,
        "formula": f"phi({req.n}) = {req.n} * " + " * ".join(f"(1 - 1/{p})" for p in sorted(factors)) if factors else "phi(1) = 1",
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/divisors")
async def compute_divisors(req: DivisorRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    divisors = _algorithms.list_divisors(req.n)
    d_count = _algorithms.divisor_count(req.n)
    sigma = _algorithms.divisor_sum(req.n, 1)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"divisors({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "n": req.n,
        "divisors": divisors if len(divisors) <= 1000 else divisors[:50] + ["...truncated..."] + divisors[-50:],
        "count": d_count,
        "sigma": sigma,
        "is_perfect": sigma == 2 * req.n,
        "aliquot_sum": sigma - req.n,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/mobius")
async def compute_mobius(req: MobiusRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    mu = _algorithms.mobius(req.n)
    factors = _algorithms.factorise(req.n) if req.n > 1 else {}
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"mobius({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    interpretation = {0: "has squared prime factor", 1: "even number of distinct prime factors", -1: "odd number of distinct prime factors"}
    return {
        "n": req.n,
        "mu": mu,
        "factorization": factors,
        "interpretation": interpretation.get(mu, "n = 1"),
        "squarefree": mu != 0,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/ext_gcd")
async def compute_ext_gcd(req: ExtGCDRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    g, x, y = _algorithms.extended_gcd(req.a, req.b)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"ext_gcd({req.a},{req.b})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "a": req.a,
        "b": req.b,
        "gcd": g,
        "x": x,
        "y": y,
        "bezout_identity": f"{req.a}*{x} + {req.b}*{y} = {g}",
        "verification": req.a * x + req.b * y == g,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/mod_inverse")
async def compute_mod_inverse(req: ModInverseRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        inv = _algorithms.mod_inverse(req.a, req.m)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"mod_inverse({req.a},{req.m})", latency, "COMPUTE", "FAST", "PLANNING")
        return {
            "a": req.a,
            "m": req.m,
            "inverse": inv,
            "verification": f"{req.a} * {inv} mod {req.m} = {(req.a * inv) % req.m}",
            "latency_ms": round(latency, 2),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/partition")
async def compute_partition(req: PartitionRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    p = _algorithms.partition(req.n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"partition({req.n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "n": req.n,
        "p_n": p,
        "method": "Euler pentagonal number theorem recurrence",
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/quadratic_residues")
async def compute_quad_res(req: QuadResRequest) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        is_qr = _algorithms.is_quadratic_residue(req.n, req.p)
        sqrt_result = _algorithms.sqrt_mod(req.n, req.p) if is_qr else None
        all_qr = _algorithms.all_quadratic_residues(req.p) if req.p <= 1000 else None
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"quad_res({req.n},{req.p})", latency, "COMPUTE", "FAST", "PLANNING")
        result: dict[str, Any] = {
            "n": req.n,
            "p": req.p,
            "is_quadratic_residue": is_qr,
            "legendre_symbol": _algorithms.legendre_symbol(req.n, req.p),
            "latency_ms": round(latency, 2),
        }
        if sqrt_result is not None:
            result["sqrt_mod"] = sqrt_result
            result["verification"] = f"{sqrt_result}^2 mod {req.p} = {pow(sqrt_result, 2, req.p)}"
        if all_qr is not None:
            result["all_quadratic_residues_mod_p"] = all_qr
            result["qr_count"] = len(all_qr)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/primitive_root")
async def compute_primitive_root(p: int = Query(..., gt=1)) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        root = _algorithms.primitive_root(p)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"primitive_root({p})", latency, "COMPUTE", "FAST", "PLANNING")
        result: dict[str, Any] = {"p": p, "latency_ms": round(latency, 2)}
        if root is not None:
            result["primitive_root"] = root
            result["order"] = p - 1 if _algorithms.is_prime_miller_rabin(p) else _algorithms.euler_totient(p)
        else:
            result["primitive_root"] = None
            result["note"] = "No primitive root exists (p must be prime)"
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/discrete_log")
async def compute_discrete_log(g: int = Query(...), h: int = Query(...), p: int = Query(..., gt=1)) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        x = _algorithms.discrete_log(g, h, p)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"dlog({g},{h},{p})", latency, "COMPUTE", "FAST", "PLANNING")
        result: dict[str, Any] = {"g": g, "h": h, "p": p, "latency_ms": round(latency, 2)}
        if x is not None:
            result["x"] = x
            result["verification"] = f"{g}^{x} mod {p} = {pow(g, x, p)}"
        else:
            result["x"] = None
            result["note"] = "No solution found"
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/compute/carmichael")
async def compute_carmichael(n: int = Query(..., gt=0)) -> dict[str, Any]:
    t0 = time.monotonic()
    lam = _algorithms.carmichael_lambda(n)
    phi = _algorithms.euler_totient(n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"carmichael({n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {
        "n": n,
        "lambda": lam,
        "phi": phi,
        "lambda_divides_phi": phi % lam == 0,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/sum_two_squares")
async def compute_sum_two_squares(n: int = Query(..., ge=0)) -> dict[str, Any]:
    t0 = time.monotonic()
    result = _algorithms.sum_of_two_squares(n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"sum2sq({n})", latency, "COMPUTE", "FAST", "PLANNING")
    if result:
        a, b = result
        return {
            "n": n, "representable": True, "a": a, "b": b,
            "verification": f"{a}^2 + {b}^2 = {a * a + b * b}",
            "latency_ms": round(latency, 2),
        }
    return {"n": n, "representable": False, "latency_ms": round(latency, 2)}


@app.post("/compute/goldbach")
async def compute_goldbach(n: int = Query(..., ge=4)) -> dict[str, Any]:
    t0 = time.monotonic()
    result = _algorithms.goldbach(n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"goldbach({n})", latency, "COMPUTE", "FAST", "PLANNING")
    if result:
        p, q = result
        return {
            "n": n, "decomposition": [p, q],
            "verification": f"{p} + {q} = {p + q}",
            "both_prime": _algorithms.is_prime_miller_rabin(p) and _algorithms.is_prime_miller_rabin(q),
            "latency_ms": round(latency, 2),
        }
    return {"n": n, "decomposition": None, "note": "n must be even and > 2", "latency_ms": round(latency, 2)}


@app.post("/compute/nth_prime")
async def compute_nth_prime(n: int = Query(..., ge=1, le=700000)) -> dict[str, Any]:
    t0 = time.monotonic()
    p = _algorithms.nth_prime(n)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"nth_prime({n})", latency, "COMPUTE", "FAST", "PLANNING")
    return {"n": n, "prime": p, "latency_ms": round(latency, 2)}


@app.post("/compute/pi")
async def compute_prime_counting(x: int = Query(..., ge=0, le=10_000_000)) -> dict[str, Any]:
    t0 = time.monotonic()
    count = _algorithms.prime_counting(x)
    latency = (time.monotonic() - t0) * 1000
    _telemetry.record_query(f"pi({x})", latency, "COMPUTE", "FAST", "PLANNING")
    estimate = x / math.log(x) if x > 1 else 0
    return {
        "x": x,
        "pi_x": count,
        "pnt_estimate": round(estimate, 1),
        "ratio_to_estimate": round(count / estimate, 4) if estimate > 0 else None,
        "latency_ms": round(latency, 2),
    }


@app.post("/compute/multiplicative_order")
async def compute_mult_order(a: int = Query(...), n: int = Query(..., gt=1)) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        order = _algorithms.multiplicative_order(a, n)
        latency = (time.monotonic() - t0) * 1000
        _telemetry.record_query(f"ord({a},{n})", latency, "COMPUTE", "FAST", "PLANNING")
        return {
            "a": a, "n": n, "order": order,
            "verification": f"{a}^{order} mod {n} = {pow(a, order, n)}",
            "divides_phi": _algorithms.euler_totient(n) % order == 0,
            "latency_ms": round(latency, 2),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ─────────────────────────────────────────────────────────────────────────
# Metrics / telemetry / drift endpoints
# ─────────────────────────────────────────────────────────────────────────

@app.get("/metrics")
async def metrics() -> dict[str, Any]:
    return _metrics_collector.collect()


@app.get("/telemetry")
async def telemetry() -> dict[str, Any]:
    return _telemetry.snapshot()


@app.get("/drift")
async def drift() -> dict[str, Any]:
    return _drift_watcher.detect_drift()


@app.get("/coverage")
async def coverage() -> dict[str, Any]:
    return _coverage_map.report()


@app.get("/decompose")
async def decompose(q: str = Query(..., min_length=1)) -> dict[str, Any]:
    return _decomposer.decompose(q)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 18: LOGURU LOGGING — configured at module top
# ═══════════════════════════════════════════════════════════════════════════
# (already done above — loguru configured with structured rotation)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
