"""
TX02 Deduction Analyzer — Telemetry Module

Tracks all query operations, doctrine cache hits, confidence distributions,
position zones, TCJA impact queries, and performance metrics.

Full audit trail with JSONL logging for forensic review.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# TELEMETRY TYPES
# ═══════════════════════════════════════════════════════════════════

class QueryType(str, Enum):
    BUSINESS_DEDUCTION = "business_deduction"
    ITEMIZED_DEDUCTION = "itemized_deduction"
    ABOVE_THE_LINE = "above_the_line"
    DEPRECIATION = "depreciation"
    INTEREST = "interest"
    CHARITABLE = "charitable"
    MEDICAL = "medical"
    HOME_OFFICE = "home_office"
    QBI_ANALYSIS = "qbi_analysis"
    PASSIVE_LOSS = "passive_loss"
    TCJA_IMPACT = "tcja_impact"
    LIMITATION_ANALYSIS = "limitation_analysis"
    OTHER = "other"


class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    query_id: str
    query_text: str
    query_type: QueryType
    response_mode: ResponseMode
    position_zone: PositionZone

    # Timing
    start_time: float
    end_time: float
    latency_ms: float

    # Doctrine usage
    doctrines_triggered: List[str] = field(default_factory=list)
    doctrines_missed: List[str] = field(default_factory=list)
    cache_hit: bool = False
    semantic_fallback: bool = False

    # Confidence
    confidence_score: float = 0.0
    confidence_stratification: str = ""

    # Output
    response_length: int = 0
    citations_count: int = 0

    # Flags
    tcja_impact_analyzed: bool = False
    aggressive_position: bool = False
    disclosure_triggered: bool = False
    error_occurred: bool = False
    error_message: str = ""

    # Determinism
    determinism_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TelemetrySnapshot:
    """Aggregate telemetry snapshot."""
    timestamp: str
    uptime_seconds: float

    # Query stats
    total_queries: int = 0
    queries_by_type: Dict[str, int] = field(default_factory=dict)
    queries_by_mode: Dict[str, int] = field(default_factory=dict)
    queries_by_zone: Dict[str, int] = field(default_factory=dict)

    # Performance
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0

    # Cache
    cache_hit_rate: float = 0.0
    semantic_fallback_rate: float = 0.0

    # Doctrine coverage
    doctrine_hit_count: Dict[str, int] = field(default_factory=dict)
    doctrine_miss_count: Dict[str, int] = field(default_factory=dict)
    top_doctrines: List[str] = field(default_factory=list)
    gap_doctrines: List[str] = field(default_factory=list)

    # Confidence
    avg_confidence: float = 0.0
    confidence_distribution: Dict[str, int] = field(default_factory=dict)

    # Flags
    tcja_queries: int = 0
    aggressive_positions: int = 0
    disclosures_triggered: int = 0
    errors: int = 0
    error_rate: float = 0.0


# ═══════════════════════════════════════════════════════════════════
# TELEMETRY COLLECTOR
# ═══════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """
    Centralized telemetry tracking for TX02 engine.

    Tracks:
        - Query types, response modes, position zones
        - Latency percentiles (p50/p95/p99)
        - Doctrine cache hits/misses, coverage gaps
        - Confidence score distribution
        - TCJA impact query frequency
        - Error rates and audit trail

    Persistence:
        - In-memory ring buffer (last 10K queries)
        - JSONL audit log (append-only)
        - Periodic snapshots to disk
    """

    def __init__(
        self,
        audit_log_path: Path,
        snapshot_path: Path,
        ring_buffer_size: int = 10000,
    ) -> None:
        self._audit_log_path = audit_log_path
        self._snapshot_path = snapshot_path
        self._ring_buffer_size = ring_buffer_size

        self._start_time = time.monotonic()
        self._query_buffer: List[QueryMetrics] = []
        self._total_queries = 0

        # Counters
        self._query_type_counter: Counter = Counter()
        self._mode_counter: Counter = Counter()
        self._zone_counter: Counter = Counter()
        self._doctrine_hit_counter: Counter = Counter()
        self._doctrine_miss_counter: Counter = Counter()
        self._confidence_counter: Counter = Counter()

        # Latency tracking
        self._latencies: List[float] = []

        # Flags
        self._cache_hits = 0
        self._semantic_fallbacks = 0
        self._tcja_queries = 0
        self._aggressive_positions = 0
        self._disclosures = 0
        self._errors = 0

        # Ensure paths exist
        self._audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        self._snapshot_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Telemetry initialized: audit={self._audit_log_path}, snapshot={self._snapshot_path}")

    def record_query(self, metrics: QueryMetrics) -> None:
        """Record a completed query."""
        self._total_queries += 1

        # Update counters
        self._query_type_counter[metrics.query_type.value] += 1
        self._mode_counter[metrics.response_mode.value] += 1
        self._zone_counter[metrics.position_zone.value] += 1

        for doctrine in metrics.doctrines_triggered:
            self._doctrine_hit_counter[doctrine] += 1
        for doctrine in metrics.doctrines_missed:
            self._doctrine_miss_counter[doctrine] += 1

        self._confidence_counter[metrics.confidence_stratification] += 1

        # Latency
        self._latencies.append(metrics.latency_ms)
        if len(self._latencies) > self._ring_buffer_size:
            self._latencies.pop(0)

        # Flags
        if metrics.cache_hit:
            self._cache_hits += 1
        if metrics.semantic_fallback:
            self._semantic_fallbacks += 1
        if metrics.tcja_impact_analyzed:
            self._tcja_queries += 1
        if metrics.aggressive_position:
            self._aggressive_positions += 1
        if metrics.disclosure_triggered:
            self._disclosures += 1
        if metrics.error_occurred:
            self._errors += 1

        # Ring buffer
        self._query_buffer.append(metrics)
        if len(self._query_buffer) > self._ring_buffer_size:
            self._query_buffer.pop(0)

        # Append to audit log
        self._write_audit_entry(metrics)

    def _write_audit_entry(self, metrics: QueryMetrics) -> None:
        """Append query metrics to JSONL audit log."""
        try:
            with self._audit_log_path.open("a", encoding="utf-8") as f:
                entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    **metrics.to_dict(),
                }
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.warning(f"Failed to write audit log: {e}")

    def snapshot(self) -> TelemetrySnapshot:
        """Generate current telemetry snapshot."""
        uptime = time.monotonic() - self._start_time

        # Latency percentiles
        sorted_latencies = sorted(self._latencies)
        p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0.0
        p95 = sorted_latencies[int(len(sorted_latencies) * 0.95)] if sorted_latencies else 0.0
        p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)] if sorted_latencies else 0.0
        avg_latency = sum(self._latencies) / len(self._latencies) if self._latencies else 0.0

        # Cache hit rate
        cache_hit_rate = self._cache_hits / max(self._total_queries, 1)
        semantic_fallback_rate = self._semantic_fallbacks / max(self._total_queries, 1)

        # Top doctrines (most frequently triggered)
        top_doctrines = [d for d, _ in self._doctrine_hit_counter.most_common(10)]

        # Gap doctrines (missed more than hit)
        gap_doctrines = [
            d for d, miss_count in self._doctrine_miss_counter.items()
            if miss_count > self._doctrine_hit_counter.get(d, 0)
        ][:10]

        # Avg confidence
        total_conf = sum(m.confidence_score for m in self._query_buffer)
        avg_confidence = total_conf / len(self._query_buffer) if self._query_buffer else 0.0

        # Error rate
        error_rate = self._errors / max(self._total_queries, 1)

        snapshot = TelemetrySnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            uptime_seconds=round(uptime, 2),
            total_queries=self._total_queries,
            queries_by_type=dict(self._query_type_counter),
            queries_by_mode=dict(self._mode_counter),
            queries_by_zone=dict(self._zone_counter),
            avg_latency_ms=round(avg_latency, 2),
            p50_latency_ms=round(p50, 2),
            p95_latency_ms=round(p95, 2),
            p99_latency_ms=round(p99, 2),
            cache_hit_rate=round(cache_hit_rate, 3),
            semantic_fallback_rate=round(semantic_fallback_rate, 3),
            doctrine_hit_count=dict(self._doctrine_hit_counter),
            doctrine_miss_count=dict(self._doctrine_miss_counter),
            top_doctrines=top_doctrines,
            gap_doctrines=gap_doctrines,
            avg_confidence=round(avg_confidence, 3),
            confidence_distribution=dict(self._confidence_counter),
            tcja_queries=self._tcja_queries,
            aggressive_positions=self._aggressive_positions,
            disclosures_triggered=self._disclosures,
            errors=self._errors,
            error_rate=round(error_rate, 3),
        )

        # Write snapshot to disk
        try:
            with self._snapshot_path.open("w", encoding="utf-8") as f:
                json.dump(asdict(snapshot), f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to write snapshot: {e}")

        return snapshot

    def reset(self) -> None:
        """Reset all counters (for testing or fresh start)."""
        self._start_time = time.monotonic()
        self._query_buffer.clear()
        self._total_queries = 0
        self._query_type_counter.clear()
        self._mode_counter.clear()
        self._zone_counter.clear()
        self._doctrine_hit_counter.clear()
        self._doctrine_miss_counter.clear()
        self._confidence_counter.clear()
        self._latencies.clear()
        self._cache_hits = 0
        self._semantic_fallbacks = 0
        self._tcja_queries = 0
        self._aggressive_positions = 0
        self._disclosures = 0
        self._errors = 0
        logger.info("Telemetry reset")


# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def generate_query_id(query_text: str, mode: str, zone: str) -> str:
    """Generate deterministic query ID."""
    raw = f"{query_text}|{mode}|{zone}|{time.time_ns()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def generate_determinism_hash(response_text: str, doctrines: List[str]) -> str:
    """Generate SHA-256 hash for response determinism verification."""
    doctrine_str = "|".join(sorted(doctrines))
    raw = f"{response_text}|{doctrine_str}"
    return hashlib.sha256(raw.encode()).hexdigest()
