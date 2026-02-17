"""
MATH15 — Financial Mathematics Engine
TIE-20 Compliant | ECHO OMEGA PRIME

Domain:
    Time Value of Money (PV/FV/PMT/NPER/RATE), Black-Scholes option pricing,
    Monte Carlo simulation (fixed seed deterministic), amortization schedules,
    bond pricing, yield calculations (YTM/YTC/current yield), interest rate
    conversions (nominal/effective/continuous), NPV/IRR/MIRR, annuity
    calculations (ordinary/due/growing/perpetuity), day count conventions.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) — Pre-compiled financial math reasoning
    Layer 2: Semantic Retrieval (200-700ms) — Normalized query matching
    Layer 3: Deep Analysis (on-demand) — Full computation + multi-source synthesis

Response Modes:
    FAST: Numeric result + brief context, sub-2 seconds
    DEFENSE: Full derivation, audit-ready, assumption disclosure
    MEMO: Long-form, citation-heavy, suitable for client delivery

Author: ECHO OMEGA PRIME
Authority: 5.0
Tier: 13 (Mathematics)
Mode: DET (Deterministic)
Port: 8577
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import uuid
from collections import deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from decimal import Decimal, ROUND_HALF_UP, getcontext
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path bootstrap — allow sibling-engine imports
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))

# ---------------------------------------------------------------------------
# Decimal precision for financial math
# ---------------------------------------------------------------------------
getcontext().prec = 28

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_NAME = "MATH15"
ENGINE_VERSION = "1.0.0"
ENGINE_DESCRIPTION = "Financial Mathematics Engine"
ENGINE_PORT = 8577
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = Path(__file__).parent / "doctrine_cache.json"
SEMANTIC_DICT_PATH = Path(__file__).parent / "semantic_dict.json"
COVERAGE_MAP_PATH = Path(__file__).parent / "coverage_map.json"

# ---------------------------------------------------------------------------
# Logging setup — loguru only, never print()
# ---------------------------------------------------------------------------
logger.add(
    LOG_DIR / "math15_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

# ===========================================================================
# COMPONENT 1: THREE-LAYER RESPONSE ARCHITECTURE
# ===========================================================================

class ResponseLayer(str, Enum):
    """Which layer satisfied the query."""
    DOCTRINE = "doctrine_cache"
    SEMANTIC = "semantic_retrieval"
    DEEP = "deep_analysis"


# ===========================================================================
# COMPONENT 2: RESPONSE MODES
# ===========================================================================

class ResponseMode(str, Enum):
    """Output modes controlling verbosity and structure."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ===========================================================================
# COMPONENT 3: DOCTRINE CACHE (loaded from JSON)
# ===========================================================================

@dataclass
class DoctrineBlock:
    """A single pre-compiled financial math reasoning block."""
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
    confidence_stratification: str
    controlling_precedent: str

    def matches(self, query_lower: str) -> float:
        """Score how well this block matches a query string. Returns 0.0-1.0."""
        score = 0.0
        hits = 0
        for kw in self.keywords:
            if kw.lower() in query_lower:
                hits += 1
        if hits == 0:
            return 0.0
        score = hits / len(self.keywords)
        if self.topic.lower() in query_lower:
            score = min(1.0, score + 0.3)
        return score


class DoctrineCacheManager:
    """Loads and queries the doctrine cache from JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.blocks: List[DoctrineBlock] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            logger.warning(f"Doctrine cache not found at {self.path}")
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            for entry in raw.get("doctrines", []):
                self.blocks.append(DoctrineBlock(
                    topic=entry["topic"],
                    keywords=entry["keywords"],
                    conclusion_template=entry["conclusion_template"],
                    reasoning_framework=entry["reasoning_framework"],
                    key_factors=entry["key_factors"],
                    primary_authority=entry["primary_authority"],
                    burden_holder=entry.get("burden_holder", "analyst"),
                    adversary_position=entry.get("adversary_position", ""),
                    counter_arguments=entry.get("counter_arguments", []),
                    resolution_strategy=entry.get("resolution_strategy", ""),
                    entity_scope=entry.get("entity_scope", "general"),
                    confidence=entry.get("confidence", 0.85),
                    confidence_stratification=entry.get("confidence_stratification", "DEFENSIBLE"),
                    controlling_precedent=entry.get("controlling_precedent", ""),
                ))
            logger.info(f"Loaded {len(self.blocks)} doctrine blocks from {self.path}")
        except Exception as exc:
            logger.error(f"Failed to load doctrine cache: {exc}")

    def lookup(self, query: str, threshold: float = 0.25) -> Optional[DoctrineBlock]:
        """Return best-matching doctrine block above threshold."""
        query_lower = query.lower()
        best_block: Optional[DoctrineBlock] = None
        best_score = 0.0
        for block in self.blocks:
            score = block.matches(query_lower)
            if score > best_score:
                best_score = score
                best_block = block
        if best_score >= threshold and best_block is not None:
            return best_block
        return None

    def all_topics(self) -> List[str]:
        return [b.topic for b in self.blocks]


# ===========================================================================
# COMPONENT 4: AUTHORITY HARDENING
# ===========================================================================

class AuthorityLevel(str, Enum):
    """Hierarchical authority levels for financial math assertions."""
    MATHEMATICAL_PROOF = "mathematical_proof"
    REGULATORY_STANDARD = "regulatory_standard"
    INDUSTRY_CONVENTION = "industry_convention"
    TEXTBOOK_REFERENCE = "textbook_reference"
    PRACTITIONER_HEURISTIC = "practitioner_heuristic"


AUTHORITY_WEIGHTS: Dict[AuthorityLevel, float] = {
    AuthorityLevel.MATHEMATICAL_PROOF: 1.0,
    AuthorityLevel.REGULATORY_STANDARD: 0.95,
    AuthorityLevel.INDUSTRY_CONVENTION: 0.85,
    AuthorityLevel.TEXTBOOK_REFERENCE: 0.80,
    AuthorityLevel.PRACTITIONER_HEURISTIC: 0.65,
}


def resolve_authority_conflict(
    authorities: List[Tuple[AuthorityLevel, str]],
) -> Tuple[AuthorityLevel, str]:
    """Given competing authority claims, return the highest-weighted one."""
    if not authorities:
        return AuthorityLevel.PRACTITIONER_HEURISTIC, "No authority cited."
    best = max(authorities, key=lambda a: AUTHORITY_WEIGHTS.get(a[0], 0.0))
    return best


# ===========================================================================
# COMPONENT 5: CONFIDENCE STRATIFICATION
# ===========================================================================

class ConfidenceStratification(str, Enum):
    """Risk tier for financial math results."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(confidence: float, has_proof: bool = False) -> ConfidenceStratification:
    """Map a confidence score to a stratification tier."""
    if has_proof and confidence >= 0.95:
        return ConfidenceStratification.DEFENSIBLE
    if confidence >= 0.85:
        return ConfidenceStratification.DEFENSIBLE
    if confidence >= 0.70:
        return ConfidenceStratification.AGGRESSIVE
    if confidence >= 0.50:
        return ConfidenceStratification.DISCLOSURE
    return ConfidenceStratification.HIGH_RISK


# ===========================================================================
# COMPONENT 6: SEMANTIC NORMALIZATION
# ===========================================================================

class SemanticNormalizer:
    """Normalize financial math terminology to canonical forms."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.mappings: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            logger.warning(f"Semantic dictionary not found at {self.path}")
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.mappings = raw.get("mappings", {})
            logger.info(f"Loaded {len(self.mappings)} semantic mappings")
        except Exception as exc:
            logger.error(f"Failed to load semantic dict: {exc}")

    def normalize(self, text: str) -> Tuple[str, List[str]]:
        """Normalize text. Returns (normalized_text, list_of_substitutions)."""
        result = text
        subs: List[str] = []
        for variant, canonical in self.mappings.items():
            if variant.lower() in result.lower():
                idx = result.lower().find(variant.lower())
                original_segment = result[idx:idx + len(variant)]
                result = result[:idx] + canonical + result[idx + len(variant):]
                subs.append(f"'{original_segment}' -> '{canonical}'")
        return result, subs


# ===========================================================================
# COMPONENT 7: VECTOR SEARCH (lightweight keyword-based fallback)
# ===========================================================================

class VectorSearchEngine:
    """Keyword-frequency fallback search when doctrine cache misses."""

    def __init__(self, doctrines: DoctrineCacheManager) -> None:
        self.doctrines = doctrines
        self._index: Dict[str, List[int]] = {}
        self._build_index()

    def _build_index(self) -> None:
        for i, block in enumerate(self.doctrines.blocks):
            tokens = set()
            tokens.update(w.lower() for w in block.topic.split())
            for kw in block.keywords:
                tokens.update(w.lower() for w in kw.split())
            for token in tokens:
                self._index.setdefault(token, []).append(i)
        logger.info(f"Vector search index: {len(self._index)} unique tokens across {len(self.doctrines.blocks)} blocks")

    def search(self, query: str, top_k: int = 3) -> List[Tuple[DoctrineBlock, float]]:
        """Return top_k doctrine blocks by keyword overlap score."""
        query_tokens = set(query.lower().split())
        scores: Dict[int, float] = {}
        for token in query_tokens:
            for idx in self._index.get(token, []):
                scores[idx] = scores.get(idx, 0.0) + 1.0
        if not scores:
            return []
        max_score = max(scores.values())
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.doctrines.blocks[idx], s / max(max_score, 1.0)) for idx, s in ranked]


# ===========================================================================
# COMPONENT 8: TELEMETRY
# ===========================================================================

class ErrorDomain(str, Enum):
    COMPUTATION = "computation"
    INPUT_VALIDATION = "input_validation"
    CONVERGENCE = "convergence"
    OVERFLOW = "overflow"
    DOCTRINE_LOOKUP = "doctrine_lookup"
    SYSTEM = "system"


@dataclass
class TraceRecord:
    """Full trace of a single query lifecycle."""
    trace_id: str
    query: str
    mode: str
    start_time: float
    end_time: Optional[float] = None
    layer: Optional[str] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    error_domain: Optional[str] = None
    doctrine_hit: bool = False
    computation_type: Optional[str] = None

    def complete(self, layer: str, doctrine_hit: bool, computation_type: str = "") -> None:
        self.end_time = time.time()
        self.layer = layer
        self.latency_ms = round((self.end_time - self.start_time) * 1000, 2)
        self.doctrine_hit = doctrine_hit
        self.computation_type = computation_type

    def fail(self, error: str, domain: ErrorDomain) -> None:
        self.end_time = time.time()
        self.latency_ms = round((self.end_time - self.start_time) * 1000, 2)
        self.error = error
        self.error_domain = domain.value


class TelemetryCollector:
    """Collects query traces and system metrics."""

    def __init__(self, max_traces: int = 500) -> None:
        self.traces: deque[TraceRecord] = deque(maxlen=max_traces)
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.computation_counts: Dict[str, int] = {}

    def start_trace(self, query: str, mode: str) -> TraceRecord:
        trace = TraceRecord(
            trace_id=str(uuid.uuid4()),
            query=query,
            mode=mode,
            start_time=time.time(),
        )
        self.total_queries += 1
        return trace

    def complete_trace(self, trace: TraceRecord) -> None:
        self.traces.append(trace)
        if trace.computation_type:
            self.computation_counts[trace.computation_type] = (
                self.computation_counts.get(trace.computation_type, 0) + 1
            )

    def record_error(self, trace: TraceRecord) -> None:
        self.traces.append(trace)
        self.total_errors += 1

    def get_summary(self) -> Dict[str, Any]:
        latencies = [t.latency_ms for t in self.traces if t.latency_ms is not None and t.error is None]
        sorted_lat = sorted(latencies) if latencies else []
        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "error_rate": round(self.total_errors / max(self.total_queries, 1), 4),
            "avg_latency_ms": round(sum(latencies) / max(len(latencies), 1), 2) if latencies else 0.0,
            "p95_latency_ms": round(sorted_lat[int(len(sorted_lat) * 0.95)] if sorted_lat else 0.0, 2),
            "computation_counts": dict(self.computation_counts),
            "recent_traces": len(self.traces),
        }


# ===========================================================================
# COMPONENT 9: DRIFT WATCHER
# ===========================================================================

class DoctrineDriftWatcher:
    """Detect changes in doctrine usage patterns over time."""

    def __init__(self) -> None:
        self.baseline_hits: Dict[str, int] = {}
        self.current_hits: Dict[str, int] = {}
        self.window_start: float = time.time()
        self.window_size_sec: float = 3600.0

    def record_hit(self, topic: str) -> None:
        self.current_hits[topic] = self.current_hits.get(topic, 0) + 1

    def check_drift(self) -> Dict[str, Any]:
        """Compare current hit distribution against baseline."""
        elapsed = time.time() - self.window_start
        if elapsed < self.window_size_sec:
            return {"status": "collecting", "elapsed_sec": round(elapsed, 1)}

        drifts: List[Dict[str, Any]] = []
        all_topics = set(list(self.baseline_hits.keys()) + list(self.current_hits.keys()))
        for topic in all_topics:
            base_count = self.baseline_hits.get(topic, 0)
            curr_count = self.current_hits.get(topic, 0)
            if base_count > 0:
                change_pct = ((curr_count - base_count) / base_count) * 100
            elif curr_count > 0:
                change_pct = 100.0
            else:
                change_pct = 0.0
            if abs(change_pct) > 30:
                drifts.append({
                    "topic": topic,
                    "baseline_hits": base_count,
                    "current_hits": curr_count,
                    "change_pct": round(change_pct, 1),
                })

        self.baseline_hits = dict(self.current_hits)
        self.current_hits = {}
        self.window_start = time.time()

        return {
            "status": "report",
            "window_sec": round(elapsed, 1),
            "drifts_detected": len(drifts),
            "drifts": drifts,
        }


# ===========================================================================
# COMPONENT 10: COVERAGE MAP
# ===========================================================================

class CoverageMapTracker:
    """Track which doctrines have been triggered and which have gaps."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.triggered: Dict[str, int] = {}
        self.missed_queries: List[str] = []
        self.gap_topics: List[str] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.gap_topics = raw.get("known_gaps", [])
            logger.info(f"Coverage map loaded: {len(self.gap_topics)} known gaps")
        except Exception as exc:
            logger.error(f"Failed to load coverage map: {exc}")

    def record_trigger(self, topic: str) -> None:
        self.triggered[topic] = self.triggered.get(topic, 0) + 1

    def record_miss(self, query: str) -> None:
        self.missed_queries.append(query)
        if len(self.missed_queries) > 200:
            self.missed_queries = self.missed_queries[-200:]

    def get_report(self, all_topics: List[str]) -> Dict[str, Any]:
        untriggered = [t for t in all_topics if t not in self.triggered]
        return {
            "total_doctrines": len(all_topics),
            "triggered_count": len(self.triggered),
            "untriggered_count": len(untriggered),
            "untriggered_topics": untriggered,
            "missed_queries_count": len(self.missed_queries),
            "recent_missed_queries": self.missed_queries[-10:],
            "known_gaps": self.gap_topics,
            "coverage_pct": round(
                len(self.triggered) / max(len(all_topics), 1) * 100, 1
            ),
        }


# ===========================================================================
# COMPONENT 11: METRICS COLLECTOR
# ===========================================================================

class MetricsCollector:
    """Lightweight operational metrics — no external dependencies."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200

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
        p95_idx = int(len(s) * 0.95)
        return {
            "avg_ms": round(sum(self.latencies) / len(self.latencies), 2),
            "p95_ms": round(s[min(p95_idx, len(s) - 1)], 2),
            "last_ms": round(self.latencies[-1], 2),
        }

    def get_doctrine_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 0.0
        return round(self.doctrine_hits / total, 4)

    def get_queries_per_hour(self) -> float:
        now = time.time()
        recent = [t for t in self.queries if t > now - 3600]
        return round(len(recent), 1)

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "latency": self.get_latency_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "queries_per_hour": self.get_queries_per_hour(),
            "active_queries": self.active_queries,
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "errors_24h": len(self.errors),
            "last_error": self.last_error,
        }


# ===========================================================================
# COMPONENT 13: ZONED ANALYSIS
# ===========================================================================

class AnalysisZone(str, Enum):
    """Position zones — never blur PLANNING with REPORTING or AUDIT."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


def enforce_zone_separation(zone: AnalysisZone, result: Dict[str, Any]) -> Dict[str, Any]:
    """Enforce zone boundaries in output. Prevents cross-contamination."""
    result["analysis_zone"] = zone.value
    if zone == AnalysisZone.PLANNING:
        result["zone_notice"] = (
            "PLANNING zone: Forward-looking analysis. Not suitable for regulatory filing without "
            "further verification. All projections depend on stated assumptions."
        )
    elif zone == AnalysisZone.REPORTING:
        result["zone_notice"] = (
            "REPORTING zone: Factual computation based on provided inputs. Verify inputs independently."
        )
    elif zone == AnalysisZone.AUDIT:
        result["zone_notice"] = (
            "AUDIT zone: Full derivation with assumption disclosure. Suitable for third-party review."
        )
    return result


# ===========================================================================
# COMPONENT 14: FACT FRAGILITY SCORING
# ===========================================================================

@dataclass
class FragilityScore:
    """How fragile is a financial math result?"""
    verifiability: float  # 0.0-1.0: how easily can this be independently verified
    assumption_sensitivity: float  # 0.0-1.0: how sensitive to input assumptions
    model_dependence: float  # 0.0-1.0: how much does this depend on a specific model
    data_recency_risk: float  # 0.0-1.0: how sensitive to stale data
    overall: float = 0.0

    def __post_init__(self) -> None:
        self.overall = round(
            0.35 * (1.0 - self.verifiability)
            + 0.30 * self.assumption_sensitivity
            + 0.20 * self.model_dependence
            + 0.15 * self.data_recency_risk,
            4,
        )


def compute_fragility(computation_type: str, inputs: Dict[str, Any]) -> FragilityScore:
    """Assign fragility score based on computation type."""
    profiles: Dict[str, Dict[str, float]] = {
        "tvm_pv": {"verifiability": 0.95, "assumption_sensitivity": 0.3, "model_dependence": 0.05, "data_recency_risk": 0.1},
        "tvm_fv": {"verifiability": 0.95, "assumption_sensitivity": 0.3, "model_dependence": 0.05, "data_recency_risk": 0.1},
        "tvm_pmt": {"verifiability": 0.95, "assumption_sensitivity": 0.3, "model_dependence": 0.05, "data_recency_risk": 0.1},
        "tvm_nper": {"verifiability": 0.90, "assumption_sensitivity": 0.35, "model_dependence": 0.05, "data_recency_risk": 0.15},
        "tvm_rate": {"verifiability": 0.80, "assumption_sensitivity": 0.45, "model_dependence": 0.15, "data_recency_risk": 0.2},
        "black_scholes": {"verifiability": 0.70, "assumption_sensitivity": 0.75, "model_dependence": 0.80, "data_recency_risk": 0.85},
        "monte_carlo": {"verifiability": 0.55, "assumption_sensitivity": 0.80, "model_dependence": 0.70, "data_recency_risk": 0.80},
        "bond_price": {"verifiability": 0.90, "assumption_sensitivity": 0.40, "model_dependence": 0.10, "data_recency_risk": 0.50},
        "ytm": {"verifiability": 0.85, "assumption_sensitivity": 0.45, "model_dependence": 0.15, "data_recency_risk": 0.55},
        "npv": {"verifiability": 0.85, "assumption_sensitivity": 0.50, "model_dependence": 0.10, "data_recency_risk": 0.35},
        "irr": {"verifiability": 0.80, "assumption_sensitivity": 0.55, "model_dependence": 0.15, "data_recency_risk": 0.35},
        "mirr": {"verifiability": 0.80, "assumption_sensitivity": 0.50, "model_dependence": 0.15, "data_recency_risk": 0.35},
        "amortization": {"verifiability": 0.95, "assumption_sensitivity": 0.20, "model_dependence": 0.05, "data_recency_risk": 0.10},
        "annuity": {"verifiability": 0.95, "assumption_sensitivity": 0.25, "model_dependence": 0.05, "data_recency_risk": 0.10},
        "day_count": {"verifiability": 1.0, "assumption_sensitivity": 0.05, "model_dependence": 0.0, "data_recency_risk": 0.0},
        "rate_conversion": {"verifiability": 1.0, "assumption_sensitivity": 0.05, "model_dependence": 0.0, "data_recency_risk": 0.0},
    }
    profile = profiles.get(computation_type, {
        "verifiability": 0.50,
        "assumption_sensitivity": 0.50,
        "model_dependence": 0.50,
        "data_recency_risk": 0.50,
    })
    return FragilityScore(**profile)


# ===========================================================================
# COMPONENT 15: AUDIT TRAIL (JSONL)
# ===========================================================================

def write_audit_entry(entry: Dict[str, Any]) -> None:
    """Append a JSON line to the audit trail."""
    try:
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        entry["engine"] = ENGINE_NAME
        with AUDIT_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ===========================================================================
# COMPONENT 16: DETERMINISM HASH (SHA-256)
# ===========================================================================

def determinism_hash(data: Any) -> str:
    """SHA-256 hash of result for reproducibility verification."""
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ===========================================================================
# COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ===========================================================================

class IssueCategory(str, Enum):
    """Top-level issue categories for financial math."""
    TIME_VALUE = "time_value_of_money"
    OPTION_PRICING = "option_pricing"
    BOND_VALUATION = "bond_valuation"
    CAPITAL_BUDGETING = "capital_budgeting"
    AMORTIZATION = "amortization"
    ANNUITIES = "annuities"
    RATE_CONVERSION = "rate_conversion"
    DAY_COUNT = "day_count_convention"
    SIMULATION = "simulation"
    RISK_METRICS = "risk_metrics"


INTERACTION_DAG: Dict[IssueCategory, List[IssueCategory]] = {
    IssueCategory.TIME_VALUE: [IssueCategory.RATE_CONVERSION, IssueCategory.DAY_COUNT],
    IssueCategory.OPTION_PRICING: [IssueCategory.RATE_CONVERSION, IssueCategory.SIMULATION, IssueCategory.RISK_METRICS],
    IssueCategory.BOND_VALUATION: [IssueCategory.TIME_VALUE, IssueCategory.RATE_CONVERSION, IssueCategory.DAY_COUNT],
    IssueCategory.CAPITAL_BUDGETING: [IssueCategory.TIME_VALUE, IssueCategory.RATE_CONVERSION],
    IssueCategory.AMORTIZATION: [IssueCategory.TIME_VALUE, IssueCategory.RATE_CONVERSION],
    IssueCategory.ANNUITIES: [IssueCategory.TIME_VALUE, IssueCategory.RATE_CONVERSION],
    IssueCategory.RATE_CONVERSION: [],
    IssueCategory.DAY_COUNT: [],
    IssueCategory.SIMULATION: [IssueCategory.OPTION_PRICING, IssueCategory.RISK_METRICS],
    IssueCategory.RISK_METRICS: [IssueCategory.OPTION_PRICING],
}


def decompose_query(query: str) -> List[IssueCategory]:
    """Classify which issue categories a query touches."""
    q = query.lower()
    categories: List[IssueCategory] = []
    kw_map: Dict[IssueCategory, List[str]] = {
        IssueCategory.TIME_VALUE: ["present value", "future value", "pv", "fv", "nper", "time value", "discount", "compound"],
        IssueCategory.OPTION_PRICING: ["option", "call", "put", "black-scholes", "black scholes", "strike", "greeks", "delta", "gamma", "theta", "vega", "rho"],
        IssueCategory.BOND_VALUATION: ["bond", "coupon", "par value", "yield", "ytm", "ytc", "duration", "convexity"],
        IssueCategory.CAPITAL_BUDGETING: ["npv", "irr", "mirr", "net present value", "internal rate", "capital budget", "project valuation"],
        IssueCategory.AMORTIZATION: ["amortiz", "loan schedule", "mortgage", "payment schedule", "principal", "interest breakdown"],
        IssueCategory.ANNUITIES: ["annuity", "perpetuity", "ordinary annuity", "annuity due", "growing annuity"],
        IssueCategory.RATE_CONVERSION: ["nominal rate", "effective rate", "continuous", "apr", "ear", "apy", "rate conver", "compounding frequency"],
        IssueCategory.DAY_COUNT: ["day count", "30/360", "act/365", "act/act", "actual/actual", "day convention"],
        IssueCategory.SIMULATION: ["monte carlo", "simulation", "random walk", "brownian", "stochastic"],
        IssueCategory.RISK_METRICS: ["risk", "var", "value at risk", "sharpe", "volatility", "standard deviation"],
    }
    for cat, keywords in kw_map.items():
        for kw in keywords:
            if kw in q:
                if cat not in categories:
                    categories.append(cat)
                break
    if not categories:
        categories.append(IssueCategory.TIME_VALUE)
    return categories


# ===========================================================================
# FINANCIAL MATH COMPUTATION ENGINE (REAL IMPLEMENTATIONS)
# ===========================================================================

# ---- HELPERS ----

def _norm_cdf(x: float) -> float:
    """Standard normal CDF using math.erf. Pure Python, no scipy."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    """Standard normal PDF."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---- TIME VALUE OF MONEY ----

def tvm_future_value(pv: float, rate: float, nper: float) -> float:
    """FV = PV * (1 + r)^n"""
    if rate <= -1.0:
        raise ValueError("Rate must be > -1.0 (i.e., greater than -100%)")
    return pv * math.pow(1.0 + rate, nper)


def tvm_present_value(fv: float, rate: float, nper: float) -> float:
    """PV = FV / (1 + r)^n"""
    if rate <= -1.0:
        raise ValueError("Rate must be > -1.0")
    return fv / math.pow(1.0 + rate, nper)


def tvm_payment(pv: float, rate: float, nper: float, fv: float = 0.0, annuity_due: bool = False) -> float:
    """
    PMT = [PV * r - FV * r / ((1+r)^n - 1)] / [1 - (1+r)^-n]
    Simplified standard formula:
        PMT = (PV * r * (1+r)^n) / ((1+r)^n - 1)  when FV=0
    General: PMT = -[PV * (1+r)^n + FV] * r / [((1+r)^n - 1) * (1 + r*due)]
    where due = 1 if annuity_due else 0
    """
    if abs(rate) < 1e-12:
        pmt = -(pv + fv) / nper
        return pmt
    due = 1.0 if annuity_due else 0.0
    factor = math.pow(1.0 + rate, nper)
    pmt = -(pv * factor + fv) * rate / ((factor - 1.0) * (1.0 + rate * due))
    return pmt


def tvm_nper(pv: float, rate: float, pmt: float, fv: float = 0.0, annuity_due: bool = False) -> float:
    """
    Solve for N in TVM equation using logarithms.
    FV + PV*(1+r)^n + PMT*((1+r)^n - 1)/r * (1 + r*due) = 0
    Let A = PMT*(1+r*due)/r, then solve for n.
    """
    if abs(rate) < 1e-12:
        if abs(pmt) < 1e-12:
            raise ValueError("Cannot solve NPER: both rate and PMT are zero")
        return -(pv + fv) / pmt
    due = 1.0 if annuity_due else 0.0
    a = pmt * (1.0 + rate * due) / rate
    numerator = math.log((-fv + a) / (pv + a))
    denominator = math.log(1.0 + rate)
    if denominator == 0.0:
        raise ValueError("Denominator is zero in NPER calculation")
    return numerator / denominator


def tvm_rate_solve(
    pv: float, fv: float, pmt: float, nper: float,
    annuity_due: bool = False,
    initial_guess: float = 0.05,
    max_iter: int = 200,
    tol: float = 1e-10,
) -> float:
    """
    Solve for rate using Newton-Raphson iteration.
    f(r) = PV*(1+r)^n + PMT*((1+r)^n -1)/r *(1+r*due) + FV = 0
    """
    r = initial_guess
    due = 1.0 if annuity_due else 0.0

    for iteration in range(max_iter):
        if abs(r) < 1e-14:
            r = 1e-10
        factor = math.pow(1.0 + r, nper)
        factor_m1 = factor - 1.0
        annuity_factor = factor_m1 / r
        f_val = pv * factor + pmt * annuity_factor * (1.0 + r * due) + fv

        # Derivative: df/dr
        d_factor = nper * math.pow(1.0 + r, nper - 1.0)
        d_annuity = (d_factor * r - factor_m1) / (r * r)
        df_val = (
            pv * d_factor
            + pmt * (1.0 + r * due) * d_annuity
            + pmt * annuity_factor * due
        )

        if abs(df_val) < 1e-20:
            logger.warning(f"RATE solver: derivative near zero at iteration {iteration}")
            break

        r_new = r - f_val / df_val

        if abs(r_new - r) < tol:
            return r_new
        r = r_new

    logger.warning(f"RATE solver did not converge after {max_iter} iterations, last r={r}")
    return r


# ---- INTEREST RATE CONVERSIONS ----

def nominal_to_effective(nominal_rate: float, compounding_periods: int) -> float:
    """EAR = (1 + r/m)^m - 1"""
    if compounding_periods <= 0:
        raise ValueError("Compounding periods must be positive")
    return math.pow(1.0 + nominal_rate / compounding_periods, compounding_periods) - 1.0


def effective_to_nominal(effective_rate: float, compounding_periods: int) -> float:
    """r_nominal = m * ((1 + EAR)^(1/m) - 1)"""
    if compounding_periods <= 0:
        raise ValueError("Compounding periods must be positive")
    return compounding_periods * (math.pow(1.0 + effective_rate, 1.0 / compounding_periods) - 1.0)


def nominal_to_continuous(nominal_rate: float, compounding_periods: int) -> float:
    """r_continuous = m * ln(1 + r/m)"""
    if compounding_periods <= 0:
        raise ValueError("Compounding periods must be positive")
    return compounding_periods * math.log(1.0 + nominal_rate / compounding_periods)


def continuous_to_effective(continuous_rate: float) -> float:
    """EAR = e^r - 1"""
    return math.exp(continuous_rate) - 1.0


def effective_to_continuous(effective_rate: float) -> float:
    """r_continuous = ln(1 + EAR)"""
    if effective_rate <= -1.0:
        raise ValueError("Effective rate must be > -1.0")
    return math.log(1.0 + effective_rate)


def continuous_to_nominal(continuous_rate: float, compounding_periods: int) -> float:
    """r_nominal = m * (e^(r_c/m) - 1)"""
    if compounding_periods <= 0:
        raise ValueError("Compounding periods must be positive")
    return compounding_periods * (math.exp(continuous_rate / compounding_periods) - 1.0)


# ---- DAY COUNT CONVENTIONS ----

def day_count_30_360(start: date, end: date) -> Tuple[int, int]:
    """
    30/360 US convention.
    Days = 360*(Y2-Y1) + 30*(M2-M1) + (D2-D1)
    Adjustments:
        If D1 = 31, set D1 = 30
        If D2 = 31 and D1 >= 30, set D2 = 30
    Returns (days, basis=360).
    """
    d1 = start.day
    d2 = end.day
    m1 = start.month
    m2 = end.month
    y1 = start.year
    y2 = end.year

    if d1 == 31:
        d1 = 30
    if d2 == 31 and d1 >= 30:
        d2 = 30

    days = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
    return days, 360


def day_count_act_365(start: date, end: date) -> Tuple[int, int]:
    """ACT/365 convention. Actual days, 365 basis."""
    delta = end - start
    return delta.days, 365


def day_count_act_act(start: date, end: date) -> Tuple[int, int]:
    """
    ACT/ACT ISDA: actual days / actual days in year.
    For simplicity, use actual days in the start year as denominator.
    Leap year = 366, else 365.
    """
    import calendar
    delta = end - start
    year_days = 366 if calendar.isleap(start.year) else 365
    return delta.days, year_days


def year_fraction(start: date, end: date, convention: str = "30/360") -> float:
    """Compute year fraction using specified day count convention."""
    convention_lower = convention.lower().replace(" ", "")
    if convention_lower in ("30/360", "30_360", "30360"):
        days, basis = day_count_30_360(start, end)
    elif convention_lower in ("act/365", "act_365", "actual/365", "actual365"):
        days, basis = day_count_act_365(start, end)
    elif convention_lower in ("act/act", "act_act", "actual/actual", "actualactual"):
        days, basis = day_count_act_act(start, end)
    else:
        days, basis = day_count_act_365(start, end)
    if basis == 0:
        return 0.0
    return days / basis


# ---- ANNUITY CALCULATIONS ----

def annuity_pv_ordinary(pmt: float, rate: float, nper: float) -> float:
    """PV of ordinary annuity = PMT * [1 - (1+r)^-n] / r"""
    if abs(rate) < 1e-12:
        return pmt * nper
    return pmt * (1.0 - math.pow(1.0 + rate, -nper)) / rate


def annuity_pv_due(pmt: float, rate: float, nper: float) -> float:
    """PV of annuity due = PV_ordinary * (1 + r)"""
    return annuity_pv_ordinary(pmt, rate, nper) * (1.0 + rate)


def annuity_fv_ordinary(pmt: float, rate: float, nper: float) -> float:
    """FV of ordinary annuity = PMT * [(1+r)^n - 1] / r"""
    if abs(rate) < 1e-12:
        return pmt * nper
    return pmt * (math.pow(1.0 + rate, nper) - 1.0) / rate


def annuity_fv_due(pmt: float, rate: float, nper: float) -> float:
    """FV of annuity due = FV_ordinary * (1 + r)"""
    return annuity_fv_ordinary(pmt, rate, nper) * (1.0 + rate)


def growing_annuity_pv(pmt: float, rate: float, growth: float, nper: float) -> float:
    """
    PV of growing annuity:
    PV = PMT / (r - g) * [1 - ((1+g)/(1+r))^n]  when r != g
    PV = PMT * n / (1 + r)                        when r == g
    """
    if abs(rate - growth) < 1e-12:
        return pmt * nper / (1.0 + rate)
    ratio = (1.0 + growth) / (1.0 + rate)
    return pmt / (rate - growth) * (1.0 - math.pow(ratio, nper))


def perpetuity_pv(pmt: float, rate: float) -> float:
    """PV of perpetuity = PMT / r"""
    if abs(rate) < 1e-12:
        raise ValueError("Rate must be non-zero for perpetuity")
    return pmt / rate


def growing_perpetuity_pv(pmt: float, rate: float, growth: float) -> float:
    """PV of growing perpetuity = PMT / (r - g), requires r > g"""
    if rate <= growth:
        raise ValueError("Rate must exceed growth rate for growing perpetuity to converge")
    return pmt / (rate - growth)


# ---- AMORTIZATION SCHEDULE ----

@dataclass
class AmortizationRow:
    """Single row in an amortization schedule."""
    period: int
    beginning_balance: float
    payment: float
    principal: float
    interest: float
    ending_balance: float


def amortization_schedule(
    principal: float,
    annual_rate: float,
    years: float,
    payments_per_year: int = 12,
) -> Tuple[List[AmortizationRow], Dict[str, float]]:
    """
    Generate full amortization schedule.
    Returns (rows, summary).
    """
    periodic_rate = annual_rate / payments_per_year
    total_payments = int(years * payments_per_year)
    if total_payments <= 0:
        raise ValueError("Total payments must be positive")

    pmt = -tvm_payment(principal, periodic_rate, total_payments)
    rows: List[AmortizationRow] = []
    balance = principal
    total_interest = 0.0
    total_principal = 0.0

    for period in range(1, total_payments + 1):
        interest = balance * periodic_rate
        princ = pmt - interest

        if period == total_payments:
            princ = balance
            pmt_actual = balance + interest
        else:
            pmt_actual = pmt

        ending = balance - princ
        if ending < 0.01:
            ending = 0.0

        rows.append(AmortizationRow(
            period=period,
            beginning_balance=round(balance, 2),
            payment=round(pmt_actual, 2),
            principal=round(princ, 2),
            interest=round(interest, 2),
            ending_balance=round(ending, 2),
        ))
        total_interest += interest
        total_principal += princ
        balance = ending

    summary = {
        "principal": round(principal, 2),
        "annual_rate": annual_rate,
        "years": years,
        "payments_per_year": payments_per_year,
        "total_payments": total_payments,
        "monthly_payment": round(pmt, 2),
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_interest + principal, 2),
    }
    return rows, summary


# ---- BOND PRICING ----

def bond_price(
    face_value: float,
    coupon_rate: float,
    yield_rate: float,
    periods: int,
    frequency: int = 2,
) -> float:
    """
    Bond price = PV of coupons + PV of par.
    P = C * [1 - (1+y)^-n] / y  +  F / (1+y)^n
    where C = coupon per period, y = yield per period, n = total periods.
    """
    coupon = face_value * coupon_rate / frequency
    y = yield_rate / frequency
    n = periods

    if abs(y) < 1e-12:
        return coupon * n + face_value

    pv_coupons = coupon * (1.0 - math.pow(1.0 + y, -n)) / y
    pv_par = face_value / math.pow(1.0 + y, n)
    return pv_coupons + pv_par


def bond_current_yield(face_value: float, coupon_rate: float, market_price: float) -> float:
    """Current yield = annual coupon / market price."""
    annual_coupon = face_value * coupon_rate
    if abs(market_price) < 1e-12:
        raise ValueError("Market price cannot be zero")
    return annual_coupon / market_price


def bond_ytm_solve(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    periods: int,
    frequency: int = 2,
    initial_guess: float = 0.05,
    max_iter: int = 300,
    tol: float = 1e-10,
) -> float:
    """
    Solve for yield-to-maturity using Newton-Raphson.
    Find y such that bond_price(face, coupon, y, periods, freq) = market_price.
    """
    coupon = face_value * coupon_rate / frequency
    y = initial_guess / frequency

    for iteration in range(max_iter):
        if abs(y) < 1e-14:
            y = 1e-10
        factor = math.pow(1.0 + y, -periods)
        pv_coupons = coupon * (1.0 - factor) / y
        pv_par = face_value * factor
        price = pv_coupons + pv_par
        f_val = price - market_price

        # Derivative of price w.r.t. y
        d_factor = -periods * math.pow(1.0 + y, -(periods + 1))
        d_pv_coupons = coupon * (-d_factor * y - (1.0 - factor)) / (y * y)
        d_pv_par = face_value * d_factor
        df_val = d_pv_coupons + d_pv_par

        if abs(df_val) < 1e-20:
            break

        y_new = y - f_val / df_val
        if abs(y_new - y) < tol:
            return y_new * frequency
        y = y_new

    return y * frequency


def bond_ytc_solve(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    call_price: float,
    periods_to_call: int,
    frequency: int = 2,
    initial_guess: float = 0.05,
    max_iter: int = 300,
    tol: float = 1e-10,
) -> float:
    """
    Yield-to-call: find y where PV(coupons to call) + PV(call price) = market price.
    """
    coupon = face_value * coupon_rate / frequency
    y = initial_guess / frequency

    for iteration in range(max_iter):
        if abs(y) < 1e-14:
            y = 1e-10
        factor = math.pow(1.0 + y, -periods_to_call)
        pv_coupons = coupon * (1.0 - factor) / y
        pv_call = call_price * factor
        price = pv_coupons + pv_call
        f_val = price - market_price

        d_factor = -periods_to_call * math.pow(1.0 + y, -(periods_to_call + 1))
        d_pv_coupons = coupon * (-d_factor * y - (1.0 - factor)) / (y * y)
        d_pv_call = call_price * d_factor
        df_val = d_pv_coupons + d_pv_call

        if abs(df_val) < 1e-20:
            break

        y_new = y - f_val / df_val
        if abs(y_new - y) < tol:
            return y_new * frequency
        y = y_new

    return y * frequency


# ---- NPV / IRR / MIRR ----

def npv_calculate(rate: float, cashflows: List[float]) -> float:
    """NPV = sum(CF_t / (1+r)^t) for t = 0, 1, 2, ..."""
    total = 0.0
    for t, cf in enumerate(cashflows):
        total += cf / math.pow(1.0 + rate, t)
    return total


def irr_solve(
    cashflows: List[float],
    initial_guess: float = 0.10,
    max_iter: int = 500,
    tol: float = 1e-10,
) -> float:
    """
    Solve for IRR using Newton-Raphson: find r where NPV(r, cashflows) = 0.
    """
    r = initial_guess

    for iteration in range(max_iter):
        npv_val = 0.0
        d_npv = 0.0
        for t, cf in enumerate(cashflows):
            factor = math.pow(1.0 + r, t)
            if abs(factor) < 1e-20:
                factor = 1e-20
            npv_val += cf / factor
            if t > 0:
                d_npv -= t * cf / math.pow(1.0 + r, t + 1)

        if abs(d_npv) < 1e-20:
            r += 0.001
            continue

        r_new = r - npv_val / d_npv
        if abs(r_new - r) < tol:
            return r_new
        r = r_new

    logger.warning(f"IRR did not converge after {max_iter} iterations, last r={r}")
    return r


def mirr_calculate(
    cashflows: List[float],
    finance_rate: float,
    reinvest_rate: float,
) -> float:
    """
    MIRR = (FV_positive / PV_negative)^(1/n) - 1
    FV_positive = sum of positive CFs compounded to end at reinvest_rate
    PV_negative = |sum of negative CFs discounted to time 0 at finance_rate|
    """
    n = len(cashflows) - 1
    if n <= 0:
        raise ValueError("Need at least 2 cashflows for MIRR")

    fv_positive = 0.0
    pv_negative = 0.0

    for t, cf in enumerate(cashflows):
        if cf >= 0:
            fv_positive += cf * math.pow(1.0 + reinvest_rate, n - t)
        else:
            pv_negative += abs(cf) / math.pow(1.0 + finance_rate, t)

    if pv_negative < 1e-12:
        raise ValueError("No negative cashflows — MIRR undefined without initial investment")
    if fv_positive < 1e-12:
        raise ValueError("No positive cashflows — MIRR undefined without returns")

    return math.pow(fv_positive / pv_negative, 1.0 / n) - 1.0


# ---- BLACK-SCHOLES OPTION PRICING ----

@dataclass
class BlackScholesResult:
    """Full Black-Scholes result including Greeks."""
    option_type: str
    price: float
    d1: float
    d2: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    intrinsic_value: float
    time_value: float


def black_scholes(
    spot: float,
    strike: float,
    time_years: float,
    rate: float,
    volatility: float,
    option_type: str = "call",
    dividend_yield: float = 0.0,
) -> BlackScholesResult:
    """
    Black-Scholes option pricing with full Greeks.
    Uses math.erf for normal CDF (pure Python, no scipy).

    d1 = [ln(S/K) + (r - q + sigma^2/2)*T] / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    Call = S*e^(-qT)*N(d1) - K*e^(-rT)*N(d2)
    Put  = K*e^(-rT)*N(-d2) - S*e^(-qT)*N(-d1)

    Greeks:
        Delta_call = e^(-qT) * N(d1)
        Delta_put  = e^(-qT) * (N(d1) - 1)
        Gamma = e^(-qT) * n(d1) / (S * sigma * sqrt(T))
        Theta_call = -[S*sigma*e^(-qT)*n(d1)] / (2*sqrt(T)) - r*K*e^(-rT)*N(d2) + q*S*e^(-qT)*N(d1)
        Theta_put  = -[S*sigma*e^(-qT)*n(d1)] / (2*sqrt(T)) + r*K*e^(-rT)*N(-d2) - q*S*e^(-qT)*N(-d1)
        Vega = S * e^(-qT) * n(d1) * sqrt(T)
        Rho_call = K * T * e^(-rT) * N(d2)
        Rho_put  = -K * T * e^(-rT) * N(-d2)
    """
    if time_years <= 0:
        raise ValueError("Time to expiration must be positive")
    if volatility <= 0:
        raise ValueError("Volatility must be positive")
    if spot <= 0:
        raise ValueError("Spot price must be positive")
    if strike <= 0:
        raise ValueError("Strike price must be positive")

    sqrt_t = math.sqrt(time_years)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility ** 2) * time_years) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t

    nd1 = _norm_cdf(d1)
    nd2 = _norm_cdf(d2)
    n_neg_d1 = _norm_cdf(-d1)
    n_neg_d2 = _norm_cdf(-d2)
    pdf_d1 = _norm_pdf(d1)

    discount_div = math.exp(-dividend_yield * time_years)
    discount_r = math.exp(-rate * time_years)

    is_call = option_type.lower() in ("call", "c")

    if is_call:
        price = spot * discount_div * nd1 - strike * discount_r * nd2
        delta = discount_div * nd1
        theta = (
            -(spot * volatility * discount_div * pdf_d1) / (2.0 * sqrt_t)
            - rate * strike * discount_r * nd2
            + dividend_yield * spot * discount_div * nd1
        )
        rho = strike * time_years * discount_r * nd2
        intrinsic = max(spot - strike, 0.0)
    else:
        price = strike * discount_r * n_neg_d2 - spot * discount_div * n_neg_d1
        delta = discount_div * (nd1 - 1.0)
        theta = (
            -(spot * volatility * discount_div * pdf_d1) / (2.0 * sqrt_t)
            + rate * strike * discount_r * n_neg_d2
            - dividend_yield * spot * discount_div * n_neg_d1
        )
        rho = -strike * time_years * discount_r * n_neg_d2
        intrinsic = max(strike - spot, 0.0)

    gamma = discount_div * pdf_d1 / (spot * volatility * sqrt_t)
    vega = spot * discount_div * pdf_d1 * sqrt_t

    return BlackScholesResult(
        option_type="call" if is_call else "put",
        price=round(price, 6),
        d1=round(d1, 6),
        d2=round(d2, 6),
        delta=round(delta, 6),
        gamma=round(gamma, 6),
        theta=round(theta / 365.0, 6),  # per-day theta
        vega=round(vega / 100.0, 6),  # per 1% vol change
        rho=round(rho / 100.0, 6),  # per 1% rate change
        intrinsic_value=round(intrinsic, 6),
        time_value=round(price - intrinsic, 6),
    )


# ---- MONTE CARLO SIMULATION ----

@dataclass
class MonteCarloResult:
    """Result of a deterministic Monte Carlo simulation."""
    mean_price: float
    median_price: float
    std_dev: float
    percentile_5: float
    percentile_25: float
    percentile_75: float
    percentile_95: float
    min_price: float
    max_price: float
    num_simulations: int
    seed: int
    sample_paths: List[List[float]]


def monte_carlo_gbm(
    spot: float,
    drift: float,
    volatility: float,
    time_years: float,
    steps: int = 252,
    simulations: int = 10000,
    seed: int = 42,
) -> MonteCarloResult:
    """
    Monte Carlo simulation using Geometric Brownian Motion.
    S_t = S_0 * exp((mu - sigma^2/2)*dt + sigma*sqrt(dt)*Z)
    FIXED seed for deterministic reproducibility.

    Uses Box-Muller transform for normal random numbers (pure Python).
    """
    import random
    rng = random.Random(seed)

    dt = time_years / steps
    sqrt_dt = math.sqrt(dt)
    drift_adj = (drift - 0.5 * volatility ** 2) * dt

    final_prices: List[float] = []
    sample_paths: List[List[float]] = []
    num_sample_paths = min(5, simulations)

    for sim in range(simulations):
        price = spot
        path: List[float] = [price] if sim < num_sample_paths else []

        for step in range(steps):
            # Box-Muller transform for standard normal
            u1 = rng.random()
            u2 = rng.random()
            while u1 < 1e-10:
                u1 = rng.random()
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            price = price * math.exp(drift_adj + volatility * sqrt_dt * z)
            if sim < num_sample_paths:
                path.append(round(price, 4))

        final_prices.append(price)
        if sim < num_sample_paths:
            sample_paths.append(path)

    final_prices.sort()
    n = len(final_prices)
    mean_p = sum(final_prices) / n
    variance = sum((p - mean_p) ** 2 for p in final_prices) / n
    std_p = math.sqrt(variance)

    return MonteCarloResult(
        mean_price=round(mean_p, 4),
        median_price=round(final_prices[n // 2], 4),
        std_dev=round(std_p, 4),
        percentile_5=round(final_prices[int(n * 0.05)], 4),
        percentile_25=round(final_prices[int(n * 0.25)], 4),
        percentile_75=round(final_prices[int(n * 0.75)], 4),
        percentile_95=round(final_prices[int(n * 0.95)], 4),
        min_price=round(final_prices[0], 4),
        max_price=round(final_prices[-1], 4),
        num_simulations=simulations,
        seed=seed,
        sample_paths=sample_paths,
    )


# ===========================================================================
# COMPONENT 20: DEEP ANALYSIS MODE
# ===========================================================================

def deep_analysis(
    query: str,
    categories: List[IssueCategory],
    doctrine_cache: DoctrineCacheManager,
    vector_search: VectorSearchEngine,
) -> Dict[str, Any]:
    """
    Multi-source synthesis engine.
    1. Identify all relevant doctrine blocks via vector search
    2. Map cross-category interactions via INTERACTION_DAG
    3. Synthesize a comprehensive analysis
    """
    related_blocks: List[Tuple[DoctrineBlock, float]] = vector_search.search(query, top_k=5)
    interaction_map: Dict[str, List[str]] = {}
    for cat in categories:
        deps = INTERACTION_DAG.get(cat, [])
        interaction_map[cat.value] = [d.value for d in deps]

    block_summaries = []
    for block, score in related_blocks:
        block_summaries.append({
            "topic": block.topic,
            "relevance_score": round(score, 3),
            "confidence": block.confidence,
            "stratification": block.confidence_stratification,
            "conclusion": block.conclusion_template,
            "key_factors": block.key_factors[:3],
        })

    return {
        "mode": "deep_analysis",
        "categories": [c.value for c in categories],
        "interaction_map": interaction_map,
        "related_doctrines": block_summaries,
        "synthesis": (
            f"Deep analysis across {len(categories)} categories with "
            f"{len(related_blocks)} related doctrine blocks. "
            f"Cross-category dependencies: {sum(len(v) for v in interaction_map.values())} edges."
        ),
    }


# ===========================================================================
# PYDANTIC MODELS (API I/O)
# ===========================================================================

class QueryRequest(BaseModel):
    """Generic query to the financial math engine."""
    query: str = Field(..., min_length=1, max_length=5000, description="Financial math question or computation request")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response verbosity mode")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis zone")


class TVMRequest(BaseModel):
    """Time Value of Money computation request."""
    solve_for: Literal["pv", "fv", "pmt", "nper", "rate"] = Field(..., description="Variable to solve for")
    pv: Optional[float] = Field(None, description="Present value")
    fv: Optional[float] = Field(None, description="Future value")
    pmt: Optional[float] = Field(None, description="Payment per period")
    rate: Optional[float] = Field(None, description="Interest rate per period (decimal)")
    nper: Optional[float] = Field(None, description="Number of periods")
    annuity_due: bool = Field(default=False, description="True for annuity due (payments at beginning)")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class RateConversionRequest(BaseModel):
    """Interest rate conversion request."""
    conversion: Literal[
        "nominal_to_effective",
        "effective_to_nominal",
        "nominal_to_continuous",
        "continuous_to_effective",
        "effective_to_continuous",
        "continuous_to_nominal",
    ] = Field(..., description="Type of conversion")
    rate: float = Field(..., description="Input rate (decimal)")
    compounding_periods: int = Field(default=12, ge=1, description="Compounding periods per year")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class DayCountRequest(BaseModel):
    """Day count convention calculation."""
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    convention: Literal["30/360", "ACT/365", "ACT/ACT"] = Field(default="30/360")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class AnnuityRequest(BaseModel):
    """Annuity / perpetuity calculation."""
    annuity_type: Literal["ordinary", "due", "fv_ordinary", "fv_due", "growing", "perpetuity", "growing_perpetuity"] = Field(...)
    pmt: float = Field(..., description="Payment amount")
    rate: float = Field(..., description="Interest rate per period (decimal)")
    nper: Optional[float] = Field(None, description="Number of periods (not needed for perpetuities)")
    growth: Optional[float] = Field(None, description="Growth rate per period (for growing types)")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class AmortizationRequest(BaseModel):
    """Amortization schedule request."""
    principal: float = Field(..., gt=0, description="Loan principal")
    annual_rate: float = Field(..., gt=0, description="Annual interest rate (decimal)")
    years: float = Field(..., gt=0, description="Loan term in years")
    payments_per_year: int = Field(default=12, ge=1, description="Payment frequency per year")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class BondPriceRequest(BaseModel):
    """Bond pricing request."""
    face_value: float = Field(default=1000.0, gt=0, description="Face/par value")
    coupon_rate: float = Field(..., ge=0, description="Annual coupon rate (decimal)")
    yield_rate: Optional[float] = Field(None, description="Annual yield rate (decimal) — for pricing")
    market_price: Optional[float] = Field(None, description="Market price — for yield solving")
    periods: int = Field(..., gt=0, description="Total coupon periods remaining")
    frequency: int = Field(default=2, ge=1, description="Coupon frequency per year")
    call_price: Optional[float] = Field(None, description="Call price — for YTC calculation")
    periods_to_call: Optional[int] = Field(None, description="Periods until first call — for YTC")
    solve_for: Literal["price", "ytm", "ytc", "current_yield"] = Field(default="price")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class NPVIRRRequest(BaseModel):
    """NPV / IRR / MIRR calculation request."""
    cashflows: List[float] = Field(..., min_length=2, description="Cashflows starting at t=0")
    calculation: Literal["npv", "irr", "mirr"] = Field(default="npv")
    discount_rate: Optional[float] = Field(None, description="Discount rate for NPV (decimal)")
    finance_rate: Optional[float] = Field(None, description="Finance rate for MIRR (decimal)")
    reinvest_rate: Optional[float] = Field(None, description="Reinvestment rate for MIRR (decimal)")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class BlackScholesRequest(BaseModel):
    """Black-Scholes option pricing request."""
    spot: float = Field(..., gt=0, description="Current stock price")
    strike: float = Field(..., gt=0, description="Strike price")
    time_years: float = Field(..., gt=0, description="Time to expiration in years")
    rate: float = Field(..., description="Risk-free rate (decimal)")
    volatility: float = Field(..., gt=0, description="Annual volatility (decimal)")
    option_type: Literal["call", "put"] = Field(default="call")
    dividend_yield: float = Field(default=0.0, ge=0, description="Continuous dividend yield")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class MonteCarloRequest(BaseModel):
    """Monte Carlo simulation request."""
    spot: float = Field(..., gt=0, description="Current price")
    drift: float = Field(..., description="Annual expected return (decimal)")
    volatility: float = Field(..., gt=0, description="Annual volatility (decimal)")
    time_years: float = Field(default=1.0, gt=0, description="Simulation horizon in years")
    steps: int = Field(default=252, ge=1, le=10000, description="Time steps (252 = daily for 1 year)")
    simulations: int = Field(default=10000, ge=100, le=100000, description="Number of simulation paths")
    seed: int = Field(default=42, description="Random seed for deterministic results")
    mode: ResponseMode = Field(default=ResponseMode.FAST)


class EngineResponse(BaseModel):
    """Standard engine response wrapper."""
    engine: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    trace_id: str
    mode: str
    zone: str
    layer: str
    computation_type: str
    result: Any
    confidence: float
    stratification: str
    fragility: Dict[str, Any]
    authorities: List[str]
    determinism_hash: str
    latency_ms: float
    categories: List[str]
    assumptions: List[str] = Field(default_factory=list)
    zone_notice: str = ""


# ===========================================================================
# APPLICATION STATE
# ===========================================================================

@dataclass
class AppState:
    """Global state for the engine."""
    doctrine_cache: DoctrineCacheManager = field(default_factory=lambda: DoctrineCacheManager(DOCTRINE_CACHE_PATH))
    semantic_normalizer: SemanticNormalizer = field(default_factory=lambda: SemanticNormalizer(SEMANTIC_DICT_PATH))
    vector_search: Optional[VectorSearchEngine] = None
    telemetry: TelemetryCollector = field(default_factory=TelemetryCollector)
    metrics: MetricsCollector = field(default_factory=MetricsCollector)
    drift_watcher: DoctrineDriftWatcher = field(default_factory=DoctrineDriftWatcher)
    coverage_map: CoverageMapTracker = field(default_factory=lambda: CoverageMapTracker(COVERAGE_MAP_PATH))
    start_time: float = field(default_factory=time.time)

    def initialize(self) -> None:
        self.vector_search = VectorSearchEngine(self.doctrine_cache)
        logger.info(f"AppState initialized: {len(self.doctrine_cache.blocks)} doctrines loaded")


state = AppState()


# ===========================================================================
# COMPONENT 17: FASTAPI SERVER
# ===========================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info(f"MATH15 Financial Mathematics Engine starting on port {ENGINE_PORT}")
    state.initialize()
    write_audit_entry({"event": "engine_start", "port": ENGINE_PORT, "version": ENGINE_VERSION})
    yield
    write_audit_entry({"event": "engine_shutdown"})
    logger.info("MATH15 shutting down")


app = FastAPI(
    title="MATH15 — Financial Mathematics Engine",
    description="TIE-20 compliant financial mathematics computation engine.",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================================
# COMPONENT 12: HEALTH ENDPOINT
# ===========================================================================

@app.get("/health")
async def health() -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    uptime = time.time() - state.start_time
    return {
        "status": "healthy",
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "auth_level": ENGINE_AUTH_LEVEL,
        "port": ENGINE_PORT,
        "uptime_seconds": round(uptime, 1),
        "doctrine_blocks_loaded": len(state.doctrine_cache.blocks),
        "semantic_mappings_loaded": len(state.semantic_normalizer.mappings),
        "telemetry_summary": state.telemetry.get_summary(),
        "metrics_snapshot": state.metrics.get_snapshot(),
        "drift_status": state.drift_watcher.check_drift(),
        "coverage": state.coverage_map.get_report(state.doctrine_cache.all_topics()),
        "components": {
            "three_layer_response": True,
            "response_modes": True,
            "doctrine_cache": True,
            "authority_hardening": True,
            "confidence_stratification": True,
            "semantic_normalization": True,
            "vector_search": state.vector_search is not None,
            "telemetry": True,
            "drift_watcher": True,
            "coverage_map": True,
            "metrics_collector": True,
            "health_endpoint": True,
            "zoned_analysis": True,
            "fact_fragility_scoring": True,
            "audit_trail_jsonl": True,
            "determinism_hash_sha256": True,
            "fastapi_server": True,
            "loguru_logging": True,
            "multi_doctrine_decomposition": True,
            "deep_analysis_mode": True,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Helper: build standard response
# ---------------------------------------------------------------------------

def _build_response(
    trace: TraceRecord,
    computation_type: str,
    result: Any,
    confidence: float,
    authorities: List[str],
    zone: AnalysisZone,
    mode: ResponseMode,
    categories: List[IssueCategory],
    assumptions: List[str],
    layer: ResponseLayer = ResponseLayer.DEEP,
    doctrine_hit: bool = False,
) -> Dict[str, Any]:
    """Construct a full TIE-compliant response."""
    trace.complete(layer.value, doctrine_hit, computation_type)
    state.telemetry.complete_trace(trace)
    state.metrics.record_query(trace.latency_ms or 0.0, doctrine_hit)

    fragility = compute_fragility(computation_type, {})
    strat = stratify_confidence(confidence, has_proof=(confidence >= 0.95))
    d_hash = determinism_hash(result)

    response = {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "trace_id": trace.trace_id,
        "mode": mode.value,
        "zone": zone.value,
        "layer": layer.value,
        "computation_type": computation_type,
        "result": result,
        "confidence": confidence,
        "stratification": strat.value,
        "fragility": {
            "verifiability": fragility.verifiability,
            "assumption_sensitivity": fragility.assumption_sensitivity,
            "model_dependence": fragility.model_dependence,
            "data_recency_risk": fragility.data_recency_risk,
            "overall_fragility": fragility.overall,
        },
        "authorities": authorities,
        "determinism_hash": d_hash,
        "latency_ms": trace.latency_ms,
        "categories": [c.value for c in categories],
        "assumptions": assumptions,
    }
    response = enforce_zone_separation(zone, response)

    write_audit_entry({
        "event": "query_complete",
        "trace_id": trace.trace_id,
        "computation_type": computation_type,
        "latency_ms": trace.latency_ms,
        "doctrine_hit": doctrine_hit,
        "confidence": confidence,
        "hash": d_hash,
    })

    return response


# ===========================================================================
# ENDPOINTS
# ===========================================================================

# ---- GENERIC QUERY ----

@app.post("/query")
async def query_endpoint(req: QueryRequest) -> Dict[str, Any]:
    """
    Generic query endpoint — routes to doctrine cache, semantic search, or deep analysis.
    """
    trace = state.telemetry.start_trace(req.query, req.mode.value)
    state.metrics.query_start()
    try:
        normalized_query, subs = state.semantic_normalizer.normalize(req.query)
        categories = decompose_query(normalized_query)

        # Layer 1: Doctrine cache lookup
        doctrine = state.doctrine_cache.lookup(normalized_query)
        if doctrine is not None:
            state.drift_watcher.record_hit(doctrine.topic)
            state.coverage_map.record_trigger(doctrine.topic)
            return _build_response(
                trace=trace,
                computation_type="doctrine_lookup",
                result={
                    "topic": doctrine.topic,
                    "conclusion": doctrine.conclusion_template,
                    "reasoning": doctrine.reasoning_framework if req.mode != ResponseMode.FAST else "",
                    "key_factors": doctrine.key_factors,
                    "primary_authority": doctrine.primary_authority,
                    "counter_arguments": doctrine.counter_arguments if req.mode == ResponseMode.MEMO else [],
                    "normalizations_applied": subs,
                },
                confidence=doctrine.confidence,
                authorities=doctrine.primary_authority,
                zone=req.zone,
                mode=req.mode,
                categories=categories,
                assumptions=[],
                layer=ResponseLayer.DOCTRINE,
                doctrine_hit=True,
            )

        # Layer 2: Semantic / vector search
        if state.vector_search is not None:
            results = state.vector_search.search(normalized_query, top_k=3)
            if results:
                best_block, best_score = results[0]
                state.drift_watcher.record_hit(best_block.topic)
                state.coverage_map.record_trigger(best_block.topic)
                return _build_response(
                    trace=trace,
                    computation_type="semantic_retrieval",
                    result={
                        "topic": best_block.topic,
                        "relevance_score": round(best_score, 3),
                        "conclusion": best_block.conclusion_template,
                        "reasoning": best_block.reasoning_framework if req.mode != ResponseMode.FAST else "",
                        "key_factors": best_block.key_factors,
                        "additional_matches": [
                            {"topic": b.topic, "score": round(s, 3)}
                            for b, s in results[1:]
                        ],
                        "normalizations_applied": subs,
                    },
                    confidence=best_block.confidence * best_score,
                    authorities=best_block.primary_authority,
                    zone=req.zone,
                    mode=req.mode,
                    categories=categories,
                    assumptions=[],
                    layer=ResponseLayer.SEMANTIC,
                    doctrine_hit=False,
                )

        # Layer 3: Deep analysis
        state.coverage_map.record_miss(normalized_query)
        analysis = deep_analysis(normalized_query, categories, state.doctrine_cache, state.vector_search or VectorSearchEngine(state.doctrine_cache))
        return _build_response(
            trace=trace,
            computation_type="deep_analysis",
            result=analysis,
            confidence=0.60,
            authorities=["Multi-source synthesis"],
            zone=req.zone,
            mode=req.mode,
            categories=categories,
            assumptions=["No direct doctrine match found; synthesized from related blocks"],
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.SYSTEM)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- TVM ----

@app.post("/tvm")
async def tvm_endpoint(req: TVMRequest) -> Dict[str, Any]:
    """Time Value of Money solver."""
    trace = state.telemetry.start_trace(f"TVM solve_for={req.solve_for}", req.mode.value)
    state.metrics.query_start()
    try:
        comp_type = f"tvm_{req.solve_for}"
        assumptions = []
        authorities = [
            AuthorityLevel.MATHEMATICAL_PROOF.value,
            "Brealey, Myers & Allen — Principles of Corporate Finance",
        ]

        if req.solve_for == "pv":
            if req.fv is None or req.rate is None or req.nper is None:
                raise ValueError("Solving for PV requires: fv, rate, nper")
            result_val = tvm_present_value(req.fv, req.rate, req.nper)
            assumptions.append(f"Discount rate = {req.rate} per period, compounded each period")
            result = {"present_value": round(result_val, 6), "fv": req.fv, "rate": req.rate, "nper": req.nper}

        elif req.solve_for == "fv":
            if req.pv is None or req.rate is None or req.nper is None:
                raise ValueError("Solving for FV requires: pv, rate, nper")
            result_val = tvm_future_value(req.pv, req.rate, req.nper)
            assumptions.append(f"Growth rate = {req.rate} per period, compounded each period")
            result = {"future_value": round(result_val, 6), "pv": req.pv, "rate": req.rate, "nper": req.nper}

        elif req.solve_for == "pmt":
            if req.pv is None or req.rate is None or req.nper is None:
                raise ValueError("Solving for PMT requires: pv, rate, nper")
            fv = req.fv if req.fv is not None else 0.0
            result_val = tvm_payment(req.pv, req.rate, req.nper, fv, req.annuity_due)
            assumptions.append(f"Annuity {'due' if req.annuity_due else 'ordinary'}")
            result = {"payment": round(result_val, 6), "pv": req.pv, "rate": req.rate, "nper": req.nper, "fv": fv, "annuity_due": req.annuity_due}

        elif req.solve_for == "nper":
            if req.pv is None or req.rate is None or req.pmt is None:
                raise ValueError("Solving for NPER requires: pv, rate, pmt")
            fv = req.fv if req.fv is not None else 0.0
            result_val = tvm_nper(req.pv, req.rate, req.pmt, fv, req.annuity_due)
            result = {"nper": round(result_val, 6), "pv": req.pv, "rate": req.rate, "pmt": req.pmt, "fv": fv}

        elif req.solve_for == "rate":
            if req.pv is None or req.nper is None or req.pmt is None:
                raise ValueError("Solving for RATE requires: pv, nper, pmt")
            fv = req.fv if req.fv is not None else 0.0
            result_val = tvm_rate_solve(req.pv, fv, req.pmt, req.nper, req.annuity_due)
            assumptions.append("Newton-Raphson iterative solution; convergence tolerance = 1e-10")
            result = {"rate_per_period": round(result_val, 8), "annual_rate_if_monthly": round(result_val * 12, 8), "pv": req.pv, "nper": req.nper, "pmt": req.pmt, "fv": fv}

        else:
            raise ValueError(f"Unknown solve_for: {req.solve_for}")

        return _build_response(
            trace=trace,
            computation_type=comp_type,
            result=result,
            confidence=0.98,
            authorities=authorities,
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.TIME_VALUE],
            assumptions=assumptions,
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- RATE CONVERSION ----

@app.post("/rate-conversion")
async def rate_conversion_endpoint(req: RateConversionRequest) -> Dict[str, Any]:
    """Interest rate conversion endpoint."""
    trace = state.telemetry.start_trace(f"rate_conversion: {req.conversion}", req.mode.value)
    state.metrics.query_start()
    try:
        conversion_funcs = {
            "nominal_to_effective": lambda: nominal_to_effective(req.rate, req.compounding_periods),
            "effective_to_nominal": lambda: effective_to_nominal(req.rate, req.compounding_periods),
            "nominal_to_continuous": lambda: nominal_to_continuous(req.rate, req.compounding_periods),
            "continuous_to_effective": lambda: continuous_to_effective(req.rate),
            "effective_to_continuous": lambda: effective_to_continuous(req.rate),
            "continuous_to_nominal": lambda: continuous_to_nominal(req.rate, req.compounding_periods),
        }
        result_val = conversion_funcs[req.conversion]()
        result = {
            "conversion": req.conversion,
            "input_rate": req.rate,
            "output_rate": round(result_val, 10),
            "compounding_periods": req.compounding_periods,
            "input_pct": f"{req.rate * 100:.4f}%",
            "output_pct": f"{result_val * 100:.4f}%",
        }
        return _build_response(
            trace=trace,
            computation_type="rate_conversion",
            result=result,
            confidence=1.0,
            authorities=[AuthorityLevel.MATHEMATICAL_PROOF.value],
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.RATE_CONVERSION],
            assumptions=[f"Compounding frequency: {req.compounding_periods} times per year"],
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- DAY COUNT ----

@app.post("/day-count")
async def day_count_endpoint(req: DayCountRequest) -> Dict[str, Any]:
    """Day count convention calculator."""
    trace = state.telemetry.start_trace(f"day_count: {req.convention}", req.mode.value)
    state.metrics.query_start()
    try:
        start = date.fromisoformat(req.start_date)
        end = date.fromisoformat(req.end_date)
        frac = year_fraction(start, end, req.convention)
        if req.convention == "30/360":
            days, basis = day_count_30_360(start, end)
        elif req.convention == "ACT/365":
            days, basis = day_count_act_365(start, end)
        else:
            days, basis = day_count_act_act(start, end)

        result = {
            "convention": req.convention,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "days": days,
            "basis": basis,
            "year_fraction": round(frac, 10),
            "actual_calendar_days": (end - start).days,
        }
        return _build_response(
            trace=trace,
            computation_type="day_count",
            result=result,
            confidence=1.0,
            authorities=[AuthorityLevel.REGULATORY_STANDARD.value, "ISDA Day Count Fraction definitions"],
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.DAY_COUNT],
            assumptions=[f"Convention: {req.convention}"],
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.INPUT_VALIDATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- ANNUITIES ----

@app.post("/annuity")
async def annuity_endpoint(req: AnnuityRequest) -> Dict[str, Any]:
    """Annuity and perpetuity calculator."""
    trace = state.telemetry.start_trace(f"annuity: {req.annuity_type}", req.mode.value)
    state.metrics.query_start()
    try:
        if req.annuity_type == "ordinary":
            if req.nper is None:
                raise ValueError("nper required for ordinary annuity PV")
            val = annuity_pv_ordinary(req.pmt, req.rate, req.nper)
            label = "pv_ordinary_annuity"
        elif req.annuity_type == "due":
            if req.nper is None:
                raise ValueError("nper required for annuity due PV")
            val = annuity_pv_due(req.pmt, req.rate, req.nper)
            label = "pv_annuity_due"
        elif req.annuity_type == "fv_ordinary":
            if req.nper is None:
                raise ValueError("nper required for ordinary annuity FV")
            val = annuity_fv_ordinary(req.pmt, req.rate, req.nper)
            label = "fv_ordinary_annuity"
        elif req.annuity_type == "fv_due":
            if req.nper is None:
                raise ValueError("nper required for annuity due FV")
            val = annuity_fv_due(req.pmt, req.rate, req.nper)
            label = "fv_annuity_due"
        elif req.annuity_type == "growing":
            if req.nper is None or req.growth is None:
                raise ValueError("nper and growth required for growing annuity")
            val = growing_annuity_pv(req.pmt, req.rate, req.growth, req.nper)
            label = "pv_growing_annuity"
        elif req.annuity_type == "perpetuity":
            val = perpetuity_pv(req.pmt, req.rate)
            label = "pv_perpetuity"
        elif req.annuity_type == "growing_perpetuity":
            if req.growth is None:
                raise ValueError("growth required for growing perpetuity")
            val = growing_perpetuity_pv(req.pmt, req.rate, req.growth)
            label = "pv_growing_perpetuity"
        else:
            raise ValueError(f"Unknown annuity_type: {req.annuity_type}")

        result = {
            "annuity_type": req.annuity_type,
            label: round(val, 6),
            "pmt": req.pmt,
            "rate": req.rate,
            "nper": req.nper,
            "growth": req.growth,
        }
        return _build_response(
            trace=trace,
            computation_type="annuity",
            result=result,
            confidence=0.98,
            authorities=[AuthorityLevel.MATHEMATICAL_PROOF.value, "Fabozzi — Fixed Income Mathematics"],
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.ANNUITIES],
            assumptions=[f"Rate = {req.rate} per period, payments {'at beginning' if req.annuity_type == 'due' else 'at end'} of period"],
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- AMORTIZATION ----

@app.post("/amortization")
async def amortization_endpoint(req: AmortizationRequest) -> Dict[str, Any]:
    """Generate full amortization schedule."""
    trace = state.telemetry.start_trace("amortization", req.mode.value)
    state.metrics.query_start()
    try:
        rows, summary = amortization_schedule(
            req.principal, req.annual_rate, req.years, req.payments_per_year,
        )
        schedule_data = [
            {
                "period": r.period,
                "beginning_balance": r.beginning_balance,
                "payment": r.payment,
                "principal": r.principal,
                "interest": r.interest,
                "ending_balance": r.ending_balance,
            }
            for r in rows
        ]

        if req.mode == ResponseMode.FAST and len(schedule_data) > 12:
            schedule_display = schedule_data[:6] + [{"...": f"{len(schedule_data) - 12} rows omitted"}] + schedule_data[-6:]
        else:
            schedule_display = schedule_data

        result = {
            "summary": summary,
            "schedule": schedule_display,
            "total_rows": len(schedule_data),
        }
        return _build_response(
            trace=trace,
            computation_type="amortization",
            result=result,
            confidence=0.99,
            authorities=[AuthorityLevel.MATHEMATICAL_PROOF.value, "Standard amortization formula"],
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.AMORTIZATION],
            assumptions=[
                f"Principal: ${req.principal:,.2f}",
                f"Annual rate: {req.annual_rate * 100:.4f}%",
                f"Term: {req.years} years, {req.payments_per_year} payments/year",
                "Level payment amortization (constant PMT)",
            ],
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- BOND PRICING ----

@app.post("/bond")
async def bond_endpoint(req: BondPriceRequest) -> Dict[str, Any]:
    """Bond pricing, YTM, YTC, current yield."""
    trace = state.telemetry.start_trace(f"bond: {req.solve_for}", req.mode.value)
    state.metrics.query_start()
    try:
        authorities = [
            AuthorityLevel.MATHEMATICAL_PROOF.value,
            "Fabozzi — Fixed Income Analysis",
            "CFA Institute — Fixed Income Readings",
        ]
        assumptions = [
            f"Face value: ${req.face_value:,.2f}",
            f"Coupon rate: {req.coupon_rate * 100:.4f}%",
            f"Frequency: {req.frequency} coupons/year",
            f"Periods: {req.periods}",
        ]

        if req.solve_for == "price":
            if req.yield_rate is None:
                raise ValueError("yield_rate required for bond pricing")
            price_val = bond_price(req.face_value, req.coupon_rate, req.yield_rate, req.periods, req.frequency)
            coupon_per_period = req.face_value * req.coupon_rate / req.frequency
            assumptions.append(f"Yield rate: {req.yield_rate * 100:.4f}%")
            result = {
                "bond_price": round(price_val, 6),
                "price_pct_of_par": round(price_val / req.face_value * 100, 4),
                "coupon_per_period": round(coupon_per_period, 4),
                "premium_discount": "premium" if price_val > req.face_value else ("discount" if price_val < req.face_value else "par"),
            }
            comp_type = "bond_price"

        elif req.solve_for == "ytm":
            if req.market_price is None:
                raise ValueError("market_price required for YTM calculation")
            ytm_val = bond_ytm_solve(req.face_value, req.coupon_rate, req.market_price, req.periods, req.frequency)
            assumptions.append(f"Market price: ${req.market_price:,.2f}")
            assumptions.append("Newton-Raphson iteration, tol=1e-10")
            result = {
                "yield_to_maturity": round(ytm_val, 8),
                "ytm_pct": f"{ytm_val * 100:.4f}%",
                "market_price": req.market_price,
            }
            comp_type = "ytm"

        elif req.solve_for == "ytc":
            if req.market_price is None or req.call_price is None or req.periods_to_call is None:
                raise ValueError("market_price, call_price, periods_to_call required for YTC")
            ytc_val = bond_ytc_solve(
                req.face_value, req.coupon_rate, req.market_price,
                req.call_price, req.periods_to_call, req.frequency,
            )
            assumptions.extend([
                f"Market price: ${req.market_price:,.2f}",
                f"Call price: ${req.call_price:,.2f}",
                f"Periods to call: {req.periods_to_call}",
            ])
            result = {
                "yield_to_call": round(ytc_val, 8),
                "ytc_pct": f"{ytc_val * 100:.4f}%",
                "call_price": req.call_price,
                "periods_to_call": req.periods_to_call,
            }
            comp_type = "ytm"

        elif req.solve_for == "current_yield":
            if req.market_price is None:
                raise ValueError("market_price required for current yield")
            cy = bond_current_yield(req.face_value, req.coupon_rate, req.market_price)
            result = {
                "current_yield": round(cy, 8),
                "current_yield_pct": f"{cy * 100:.4f}%",
                "annual_coupon": round(req.face_value * req.coupon_rate, 4),
                "market_price": req.market_price,
            }
            comp_type = "bond_price"

        else:
            raise ValueError(f"Unknown solve_for: {req.solve_for}")

        return _build_response(
            trace=trace,
            computation_type=comp_type,
            result=result,
            confidence=0.95,
            authorities=authorities,
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.BOND_VALUATION],
            assumptions=assumptions,
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- NPV / IRR / MIRR ----

@app.post("/npv-irr")
async def npv_irr_endpoint(req: NPVIRRRequest) -> Dict[str, Any]:
    """NPV, IRR, MIRR calculator."""
    trace = state.telemetry.start_trace(f"npv_irr: {req.calculation}", req.mode.value)
    state.metrics.query_start()
    try:
        authorities = [
            AuthorityLevel.MATHEMATICAL_PROOF.value,
            "Brealey, Myers & Allen — Principles of Corporate Finance",
        ]
        assumptions = [f"Cashflows: {req.cashflows}"]

        if req.calculation == "npv":
            if req.discount_rate is None:
                raise ValueError("discount_rate required for NPV")
            val = npv_calculate(req.discount_rate, req.cashflows)
            assumptions.append(f"Discount rate: {req.discount_rate * 100:.4f}%")
            result = {
                "npv": round(val, 6),
                "discount_rate": req.discount_rate,
                "num_periods": len(req.cashflows) - 1,
                "accept_reject": "ACCEPT (NPV > 0)" if val > 0 else "REJECT (NPV <= 0)",
            }
            comp_type = "npv"

        elif req.calculation == "irr":
            val = irr_solve(req.cashflows)
            npv_at_irr = npv_calculate(val, req.cashflows)
            assumptions.append("Newton-Raphson iteration, tol=1e-10")
            result = {
                "irr": round(val, 8),
                "irr_pct": f"{val * 100:.4f}%",
                "npv_at_irr": round(npv_at_irr, 6),
                "num_periods": len(req.cashflows) - 1,
            }
            comp_type = "irr"

        elif req.calculation == "mirr":
            if req.finance_rate is None or req.reinvest_rate is None:
                raise ValueError("finance_rate and reinvest_rate required for MIRR")
            val = mirr_calculate(req.cashflows, req.finance_rate, req.reinvest_rate)
            assumptions.extend([
                f"Finance rate: {req.finance_rate * 100:.4f}%",
                f"Reinvestment rate: {req.reinvest_rate * 100:.4f}%",
            ])
            result = {
                "mirr": round(val, 8),
                "mirr_pct": f"{val * 100:.4f}%",
                "finance_rate": req.finance_rate,
                "reinvest_rate": req.reinvest_rate,
                "num_periods": len(req.cashflows) - 1,
            }
            comp_type = "mirr"

        else:
            raise ValueError(f"Unknown calculation: {req.calculation}")

        return _build_response(
            trace=trace,
            computation_type=comp_type,
            result=result,
            confidence=0.95,
            authorities=authorities,
            zone=AnalysisZone.REPORTING,
            mode=req.mode,
            categories=[IssueCategory.CAPITAL_BUDGETING],
            assumptions=assumptions,
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- BLACK-SCHOLES ----

@app.post("/black-scholes")
async def black_scholes_endpoint(req: BlackScholesRequest) -> Dict[str, Any]:
    """Black-Scholes option pricing with full Greeks."""
    trace = state.telemetry.start_trace(f"black_scholes: {req.option_type}", req.mode.value)
    state.metrics.query_start()
    try:
        bs = black_scholes(
            spot=req.spot,
            strike=req.strike,
            time_years=req.time_years,
            rate=req.rate,
            volatility=req.volatility,
            option_type=req.option_type,
            dividend_yield=req.dividend_yield,
        )
        result = {
            "option_type": bs.option_type,
            "price": bs.price,
            "d1": bs.d1,
            "d2": bs.d2,
            "greeks": {
                "delta": bs.delta,
                "gamma": bs.gamma,
                "theta_per_day": bs.theta,
                "vega_per_pct": bs.vega,
                "rho_per_pct": bs.rho,
            },
            "intrinsic_value": bs.intrinsic_value,
            "time_value": bs.time_value,
            "inputs": {
                "spot": req.spot,
                "strike": req.strike,
                "time_years": req.time_years,
                "rate": req.rate,
                "volatility": req.volatility,
                "dividend_yield": req.dividend_yield,
            },
        }
        assumptions = [
            "Log-normal distribution of returns",
            "Constant volatility over option life",
            "Continuous trading, no transaction costs",
            "European-style exercise only",
            f"Risk-free rate: {req.rate * 100:.4f}%",
            f"Volatility: {req.volatility * 100:.2f}%",
        ]
        if req.dividend_yield > 0:
            assumptions.append(f"Continuous dividend yield: {req.dividend_yield * 100:.4f}%")

        return _build_response(
            trace=trace,
            computation_type="black_scholes",
            result=result,
            confidence=0.85,
            authorities=[
                AuthorityLevel.MATHEMATICAL_PROOF.value,
                "Black, F. & Scholes, M. (1973) — The Pricing of Options and Corporate Liabilities",
                "Hull, J. — Options, Futures, and Other Derivatives",
            ],
            zone=AnalysisZone.PLANNING,
            mode=req.mode,
            categories=[IssueCategory.OPTION_PRICING],
            assumptions=assumptions,
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- MONTE CARLO ----

@app.post("/monte-carlo")
async def monte_carlo_endpoint(req: MonteCarloRequest) -> Dict[str, Any]:
    """Monte Carlo GBM simulation (deterministic with fixed seed)."""
    trace = state.telemetry.start_trace("monte_carlo", req.mode.value)
    state.metrics.query_start()
    try:
        mc = monte_carlo_gbm(
            spot=req.spot,
            drift=req.drift,
            volatility=req.volatility,
            time_years=req.time_years,
            steps=req.steps,
            simulations=req.simulations,
            seed=req.seed,
        )
        result = {
            "statistics": {
                "mean_price": mc.mean_price,
                "median_price": mc.median_price,
                "std_dev": mc.std_dev,
                "percentile_5": mc.percentile_5,
                "percentile_25": mc.percentile_25,
                "percentile_75": mc.percentile_75,
                "percentile_95": mc.percentile_95,
                "min_price": mc.min_price,
                "max_price": mc.max_price,
            },
            "simulation_params": {
                "spot": req.spot,
                "drift": req.drift,
                "volatility": req.volatility,
                "time_years": req.time_years,
                "steps": req.steps,
                "simulations": req.simulations,
                "seed": req.seed,
            },
            "sample_paths_count": len(mc.sample_paths),
            "sample_paths": mc.sample_paths if req.mode != ResponseMode.FAST else [],
        }
        assumptions = [
            "Geometric Brownian Motion: dS = mu*S*dt + sigma*S*dW",
            f"Fixed random seed = {req.seed} for deterministic reproducibility",
            "Log-normal distribution of returns",
            "Independent increments (no autocorrelation)",
            f"Drift: {req.drift * 100:.2f}% annual, Volatility: {req.volatility * 100:.2f}% annual",
            "Box-Muller transform for normal random number generation",
        ]
        return _build_response(
            trace=trace,
            computation_type="monte_carlo",
            result=result,
            confidence=0.75,
            authorities=[
                AuthorityLevel.MATHEMATICAL_PROOF.value,
                "Glasserman, P. — Monte Carlo Methods in Financial Engineering",
                "Hull, J. — Options, Futures, and Other Derivatives",
            ],
            zone=AnalysisZone.PLANNING,
            mode=req.mode,
            categories=[IssueCategory.SIMULATION],
            assumptions=assumptions,
            layer=ResponseLayer.DEEP,
            doctrine_hit=False,
        )
    except Exception as exc:
        trace.fail(str(exc), ErrorDomain.COMPUTATION)
        state.telemetry.record_error(trace)
        state.metrics.record_error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        state.metrics.query_end()


# ---- TELEMETRY ENDPOINT ----

@app.get("/telemetry")
async def telemetry_endpoint() -> Dict[str, Any]:
    """Expose telemetry data."""
    return {
        "engine": ENGINE_NAME,
        "telemetry": state.telemetry.get_summary(),
        "metrics": state.metrics.get_snapshot(),
        "drift": state.drift_watcher.check_drift(),
        "coverage": state.coverage_map.get_report(state.doctrine_cache.all_topics()),
    }


# ---- DOCTRINES LIST ----

@app.get("/doctrines")
async def doctrines_endpoint() -> Dict[str, Any]:
    """List all loaded doctrine topics."""
    return {
        "engine": ENGINE_NAME,
        "count": len(state.doctrine_cache.blocks),
        "topics": [
            {
                "topic": b.topic,
                "confidence": b.confidence,
                "stratification": b.confidence_stratification,
                "keywords": b.keywords,
            }
            for b in state.doctrine_cache.blocks
        ],
    }


# ---- COVERAGE REPORT ----

@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """Coverage report — triggered vs untriggered doctrines."""
    return state.coverage_map.get_report(state.doctrine_cache.all_topics())


# ---- DRIFT REPORT ----

@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    """Doctrine drift detection report."""
    return state.drift_watcher.check_drift()


# ===========================================================================
# COMPONENT 18: LOGURU LOGGING (configured above, used everywhere)
# ===========================================================================
# Loguru is configured at module top. Every function uses logger.info/warning/error.
# Never print(). All output via structured logging.


# ===========================================================================
# ENTRYPOINT
# ===========================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting MATH15 Financial Mathematics Engine on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
