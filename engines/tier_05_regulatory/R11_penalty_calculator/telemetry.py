"""
R09 - Telemetry Module
Performance tracking and metrics collection
"""

from typing import Dict, Any, List
from datetime import datetime
import time
from collections import defaultdict
from loguru import logger


class TelemetryCollector:
    """Centralized telemetry collection"""

    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.error_count = 0
        self.latencies: Dict[str, List[float]] = defaultdict(list)
        self.events: List[Dict[str, Any]] = []
        self.error_domains: Dict[str, int] = defaultdict(int)

    def increment_query_count(self):
        """Increment total query counter"""
        self.query_count += 1

    def record_error(self, domain: str, message: str):
        """
        Record error event

        Args:
            domain: Error category
            message: Error message
        """
        self.error_count += 1
        self.error_domains[domain] += 1
        self.events.append({
            "type": "error",
            "domain": domain,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.error(f"[{domain}] {message}")

    def record_latency(self, operation: str, duration_seconds: float):
        """
        Record operation latency

        Args:
            operation: Operation name
            duration_seconds: Duration in seconds
        """
        self.latencies[operation].append(duration_seconds)

    def record_event(self, event_type: str, data: Dict[str, Any]):
        """
        Record custom event

        Args:
            event_type: Event category
            data: Event data
        """
        self.events.append({
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            **data
        })

    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time

    def get_query_count(self) -> int:
        """Get total query count"""
        return self.query_count

    def get_error_rate(self) -> float:
        """Calculate error rate"""
        if self.query_count == 0:
            return 0.0
        return self.error_count / self.query_count

    def get_avg_latency(self, operation: str = "total_response") -> float:
        """
        Get average latency for operation

        Args:
            operation: Operation name

        Returns:
            Average latency in milliseconds
        """
        if operation not in self.latencies or not self.latencies[operation]:
            return 0.0

        latencies = self.latencies[operation]
        return (sum(latencies) / len(latencies)) * 1000  # Convert to ms

    def get_percentile_latency(self, operation: str, percentile: int) -> float:
        """
        Get percentile latency

        Args:
            operation: Operation name
            percentile: Percentile (50, 95, 99)

        Returns:
            Latency in milliseconds
        """
        if operation not in self.latencies or not self.latencies[operation]:
            return 0.0

        latencies = sorted(self.latencies[operation])
        index = int(len(latencies) * (percentile / 100))
        index = min(index, len(latencies) - 1)

        return latencies[index] * 1000  # Convert to ms

    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive telemetry summary

        Returns:
            Dictionary with all metrics
        """
        summary = {
            "uptime_seconds": round(self.get_uptime(), 2),
            "total_queries": self.query_count,
            "total_errors": self.error_count,
            "error_rate": round(self.get_error_rate(), 4),
            "queries_per_second": round(self.query_count / max(self.get_uptime(), 1), 4),
        }

        # Latency stats
        if "total_response" in self.latencies:
            summary["total_response_ms"] = round(self.get_avg_latency("total_response"), 2)
            summary["total_response_p50"] = round(self.get_percentile_latency("total_response", 50), 2)
            summary["total_response_p95"] = round(self.get_percentile_latency("total_response", 95), 2)
            summary["total_response_p99"] = round(self.get_percentile_latency("total_response", 99), 2)

        # Error breakdown
        if self.error_domains:
            summary["error_domains"] = dict(self.error_domains)

        # Operation breakdown
        summary["operations"] = {}
        for operation, latencies in self.latencies.items():
            if latencies:
                summary["operations"][operation] = {
                    "count": len(latencies),
                    "avg_ms": round(sum(latencies) / len(latencies) * 1000, 2),
                    "min_ms": round(min(latencies) * 1000, 2),
                    "max_ms": round(max(latencies) * 1000, 2)
                }

        # Recent events (last 10)
        summary["recent_events"] = self.events[-10:]

        return summary

    def reset_metrics(self):
        """Reset all metrics (for testing or periodic reset)"""
        self.query_count = 0
        self.error_count = 0
        self.latencies.clear()
        self.events.clear()
        self.error_domains.clear()
        self.start_time = time.time()
        logger.info("Telemetry metrics reset")


class QueryMetrics:
    """Per-query metrics context manager"""

    def __init__(self, collector: TelemetryCollector, operation: str):
        self.collector = collector
        self.operation = operation
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.collector.record_latency(self.operation, duration)

        if exc_type is not None:
            self.collector.record_error(self.operation, str(exc_val))

        return False  # Don't suppress exceptions


def format_telemetry_report(summary: Dict[str, Any]) -> str:
    """
    Format telemetry summary as human-readable report

    Args:
        summary: Telemetry summary dict

    Returns:
        Formatted report string
    """
    lines = [
        "=" * 70,
        "R09 PLUGGING REQUIREMENTS ENGINE - TELEMETRY REPORT",
        "=" * 70,
        f"Uptime: {summary['uptime_seconds']:.2f} seconds",
        f"Total Queries: {summary['total_queries']}",
        f"Total Errors: {summary['total_errors']}",
        f"Error Rate: {summary['error_rate'] * 100:.2f}%",
        f"Queries/sec: {summary['queries_per_second']:.4f}",
        "",
        "LATENCY METRICS:",
        "-" * 70,
    ]

    if "total_response_ms" in summary:
        lines.extend([
            f"  Average Response Time: {summary['total_response_ms']:.2f} ms",
            f"  P50 (median): {summary['total_response_p50']:.2f} ms",
            f"  P95: {summary['total_response_p95']:.2f} ms",
            f"  P99: {summary['total_response_p99']:.2f} ms",
        ])

    if summary.get("operations"):
        lines.extend(["", "OPERATION BREAKDOWN:", "-" * 70])
        for op, metrics in summary["operations"].items():
            lines.append(f"  {op}:")
            lines.append(f"    Count: {metrics['count']}")
            lines.append(f"    Avg: {metrics['avg_ms']:.2f} ms")
            lines.append(f"    Min: {metrics['min_ms']:.2f} ms")
            lines.append(f"    Max: {metrics['max_ms']:.2f} ms")

    if summary.get("error_domains"):
        lines.extend(["", "ERROR BREAKDOWN:", "-" * 70])
        for domain, count in summary["error_domains"].items():
            lines.append(f"  {domain}: {count}")

    lines.append("=" * 70)

    return "\n".join(lines)
