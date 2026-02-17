"""
MATH08 — Graph Theory Intelligence Engine
TIE-20 Compliant | Tier 13 Mathematics | Port 8570
Authority: 5.0 | Mode: DET (Deterministic)

Full graph theory engine: representations, traversals, shortest paths,
MST, network flow, topological sort, cycle detection, centrality measures,
connected components, graph coloring, bipartite checking, clustering.

All algorithms are pure Python with real implementations — no stubs.
"""
from __future__ import annotations

import asyncio
import hashlib
import heapq
import json
import math
import sys
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_DIR))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "MATH08"
ENGINE_NAME = "Graph Theory Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8570
ENGINE_TIER = 13
ENGINE_DOMAIN = "mathematics.graph_theory"
ENGINE_MODE = "DET"
AUTHORITY_LEVEL = 5.0
MAX_GRAPH_NODES = 50_000
MAX_GRAPH_EDGES = 500_000
PAGERANK_DAMPING = 0.85
PAGERANK_ITERATIONS = 100
PAGERANK_TOLERANCE = 1e-8
FLOAT_INF = float("inf")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | <cyan>MATH08</cyan> | {message}",
    level="DEBUG",
)
LOG_PATH = ENGINE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)
logger.add(
    LOG_PATH / "math08_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
)

# ---------------------------------------------------------------------------
# Telemetry
# ---------------------------------------------------------------------------
class TelemetryCollector:
    """Collects query-level and engine-level metrics."""

    def __init__(self) -> None:
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.latencies: list[float] = []
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.queries_by_algorithm: dict[str, int] = defaultdict(int)
        self.start_time: float = time.time()

    def record_query(self, algorithm: str, latency_ms: float, from_cache: bool) -> None:
        self.total_queries += 1
        self.latencies.append(latency_ms)
        self.queries_by_algorithm[algorithm] += 1
        if from_cache:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_error(self) -> None:
        self.total_errors += 1

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time

    @property
    def avg_latency_ms(self) -> float:
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)

    @property
    def p95_latency_ms(self) -> float:
        if not self.latencies:
            return 0.0
        s = sorted(self.latencies)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    @property
    def error_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.total_errors / self.total_queries

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    def snapshot(self) -> dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "total_errors": self.total_errors,
            "avg_latency_ms": round(self.avg_latency_ms, 3),
            "p95_latency_ms": round(self.p95_latency_ms, 3),
            "cache_hit_rate": round(self.cache_hit_rate, 4),
            "error_rate": round(self.error_rate, 4),
            "uptime_seconds": round(self.uptime_seconds, 1),
            "queries_by_algorithm": dict(self.queries_by_algorithm),
        }


TELEMETRY = TelemetryCollector()

# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------
AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"


def write_audit_entry(entry: dict[str, Any]) -> None:
    """Append an entry to the JSONL audit trail."""
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["engine_id"] = ENGINE_ID
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


# ---------------------------------------------------------------------------
# Determinism hash
# ---------------------------------------------------------------------------
def determinism_hash(data: Any) -> str:
    """SHA-256 hash for reproducibility verification."""
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Doctrine Cache
# ---------------------------------------------------------------------------
class DoctrineBlock(BaseModel):
    topic: str
    keywords: list[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str]
    primary_authority: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_stratification: str = "DEFENSIBLE"
    entity_scope: str = "graph_theory"


DOCTRINE_CACHE: list[DoctrineBlock] = []


def load_doctrine_cache() -> None:
    """Load doctrine cache from JSON file on disk."""
    global DOCTRINE_CACHE
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if not cache_path.exists():
        logger.warning("doctrine_cache.json not found — running with empty cache")
        return
    with open(cache_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    DOCTRINE_CACHE = [DoctrineBlock(**entry) for entry in raw]
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks from cache")


def search_doctrine_cache(query: str) -> Optional[DoctrineBlock]:
    """O(n) keyword scan — returns best matching doctrine block."""
    query_lower = query.lower()
    best: Optional[DoctrineBlock] = None
    best_score = 0
    for block in DOCTRINE_CACHE:
        score = sum(1 for kw in block.keywords if kw.lower() in query_lower)
        if score > best_score:
            best_score = score
            best = block
    return best


# ---------------------------------------------------------------------------
# Semantic Normalization
# ---------------------------------------------------------------------------
SEMANTIC_DICT: dict[str, str] = {}


def load_semantic_dict() -> None:
    global SEMANTIC_DICT
    path = ENGINE_DIR / "semantic_dict.json"
    if not path.exists():
        logger.warning("semantic_dict.json not found")
        return
    with open(path, "r", encoding="utf-8") as fh:
        SEMANTIC_DICT = json.load(fh)
    logger.info(f"Loaded {len(SEMANTIC_DICT)} semantic normalization entries")


def normalize_term(term: str) -> str:
    """Normalize a graph-theory term to its canonical form."""
    lower = term.strip().lower()
    return SEMANTIC_DICT.get(lower, lower)


# ---------------------------------------------------------------------------
# Coverage Map
# ---------------------------------------------------------------------------
COVERAGE_MAP: dict[str, Any] = {}


def load_coverage_map() -> None:
    global COVERAGE_MAP
    path = ENGINE_DIR / "coverage_map.json"
    if not path.exists():
        logger.warning("coverage_map.json not found")
        return
    with open(path, "r", encoding="utf-8") as fh:
        COVERAGE_MAP = json.load(fh)
    logger.info(f"Loaded coverage map with {len(COVERAGE_MAP.get('domains', {}))} domains")


# ---------------------------------------------------------------------------
# Drift Watcher
# ---------------------------------------------------------------------------
class DriftWatcher:
    """Tracks doctrine drift — how query patterns shift over time."""

    def __init__(self) -> None:
        self.topic_counts: dict[str, int] = defaultdict(int)
        self.window: deque[tuple[float, str]] = deque(maxlen=1000)

    def record(self, topic: str) -> None:
        self.topic_counts[topic] += 1
        self.window.append((time.time(), topic))

    def recent_distribution(self, window_seconds: int = 3600) -> dict[str, int]:
        cutoff = time.time() - window_seconds
        counts: dict[str, int] = defaultdict(int)
        for ts, topic in self.window:
            if ts >= cutoff:
                counts[topic] += 1
        return dict(counts)

    def snapshot(self) -> dict[str, Any]:
        return {
            "all_time": dict(self.topic_counts),
            "last_hour": self.recent_distribution(3600),
        }


DRIFT = DriftWatcher()

# ---------------------------------------------------------------------------
# Confidence Stratification
# ---------------------------------------------------------------------------
class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(score: float) -> ConfidenceLevel:
    if score >= 0.9:
        return ConfidenceLevel.DEFENSIBLE
    elif score >= 0.7:
        return ConfidenceLevel.AGGRESSIVE
    elif score >= 0.5:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ---------------------------------------------------------------------------
# Authority Hardening
# ---------------------------------------------------------------------------
AUTHORITY_WEIGHTS: dict[str, float] = {
    "theorem": 1.0,
    "textbook": 0.95,
    "peer_reviewed_paper": 0.9,
    "lecture_notes": 0.7,
    "online_resource": 0.5,
    "heuristic": 0.3,
}


def compute_authority_score(sources: list[str]) -> float:
    """Weighted authority from source types."""
    if not sources:
        return 0.3
    total = sum(AUTHORITY_WEIGHTS.get(s, 0.4) for s in sources)
    return min(total / len(sources), 1.0)


# ---------------------------------------------------------------------------
# Fact Fragility Scoring
# ---------------------------------------------------------------------------
def fact_fragility_score(
    verifiability: float,
    recharacterization_risk: float,
    testimony_dependence: float,
) -> float:
    """Score 0..1 where higher means more fragile."""
    return round(
        (1.0 - verifiability) * 0.4
        + recharacterization_risk * 0.3
        + testimony_dependence * 0.3,
        4,
    )


# ---------------------------------------------------------------------------
# Zoned Analysis
# ---------------------------------------------------------------------------
class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ---------------------------------------------------------------------------
# Response Modes
# ---------------------------------------------------------------------------
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ---------------------------------------------------------------------------
# Pydantic Models — Request / Response
# ---------------------------------------------------------------------------
class GraphInput(BaseModel):
    """Graph specification for API input."""
    num_nodes: int = Field(ge=1, le=MAX_GRAPH_NODES)
    edges: list[tuple[int, int] | tuple[int, int, float]] = Field(default_factory=list)
    directed: bool = False
    weighted: bool = False


class AlgorithmRequest(BaseModel):
    """Request to run a specific graph algorithm."""
    graph: GraphInput
    algorithm: str
    source: Optional[int] = None
    target: Optional[int] = None
    params: dict[str, Any] = Field(default_factory=dict)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING


class QueryRequest(BaseModel):
    """Free-text query about graph theory."""
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING


class AlgorithmResponse(BaseModel):
    engine_id: str = ENGINE_ID
    algorithm: str
    result: Any
    determinism_hash: str
    confidence: float
    confidence_level: str
    latency_ms: float
    from_cache: bool = False
    mode: str
    zone: str
    authority_score: float = AUTHORITY_LEVEL
    audit_id: str = ""


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    query: str
    answer: str
    doctrine_topic: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: float
    confidence_level: str
    determinism_hash: str
    latency_ms: float
    mode: str
    zone: str


# ═══════════════════════════════════════════════════════════════════════════
# CORE: UnionFind (Disjoint Set) for Kruskal
# ═══════════════════════════════════════════════════════════════════════════
class UnionFind:
    """Disjoint-set / union-find with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n
        self.components: int = n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


# ═══════════════════════════════════════════════════════════════════════════
# CORE: Graph Class — adjacency list representation
# ═══════════════════════════════════════════════════════════════════════════
class Graph:
    """
    General-purpose graph with adjacency-list representation.
    Supports directed/undirected, weighted/unweighted.
    Nodes are integers 0..n-1.
    """

    def __init__(self, num_nodes: int, directed: bool = False, weighted: bool = False) -> None:
        self.n: int = num_nodes
        self.directed: bool = directed
        self.weighted: bool = weighted
        self.adj: dict[int, list[tuple[int, float]]] = defaultdict(list)
        self.edge_count: int = 0

    def add_edge(self, u: int, v: int, w: float = 1.0) -> None:
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
        self.edge_count += 1

    def neighbors(self, u: int) -> list[tuple[int, float]]:
        return self.adj.get(u, [])

    def degree(self, u: int) -> int:
        return len(self.adj.get(u, []))

    def nodes(self) -> range:
        return range(self.n)

    def edges(self) -> list[tuple[int, int, float]]:
        seen: set[tuple[int, int]] = set()
        result: list[tuple[int, int, float]] = []
        for u in range(self.n):
            for v, w in self.adj.get(u, []):
                key = (u, v) if self.directed else (min(u, v), max(u, v))
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def has_edge(self, u: int, v: int) -> bool:
        return any(nbr == v for nbr, _ in self.adj.get(u, []))

    def reverse(self) -> "Graph":
        """Return a new graph with all edges reversed (directed only)."""
        g = Graph(self.n, directed=True, weighted=self.weighted)
        for u in range(self.n):
            for v, w in self.adj.get(u, []):
                g.add_edge(v, u, w)
        return g

    def adjacency_matrix(self) -> list[list[float]]:
        mat = [[FLOAT_INF] * self.n for _ in range(self.n)]
        for i in range(self.n):
            mat[i][i] = 0.0
        for u in range(self.n):
            for v, w in self.adj.get(u, []):
                mat[u][v] = w
        return mat

    @staticmethod
    def from_input(inp: GraphInput) -> "Graph":
        g = Graph(inp.num_nodes, directed=inp.directed, weighted=inp.weighted)
        for edge in inp.edges:
            if len(edge) == 3:
                u, v, w = int(edge[0]), int(edge[1]), float(edge[2])
            else:
                u, v = int(edge[0]), int(edge[1])
                w = 1.0
            if 0 <= u < g.n and 0 <= v < g.n:
                g.add_edge(u, v, w)
        return g

    def summary(self) -> dict[str, Any]:
        return {
            "num_nodes": self.n,
            "num_edges": self.edge_count,
            "directed": self.directed,
            "weighted": self.weighted,
        }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: BFS (Breadth-First Search)
# ═══════════════════════════════════════════════════════════════════════════
def bfs(graph: Graph, source: int) -> dict[str, Any]:
    """
    BFS from source node. Returns distances, parent map, visit order.
    Time: O(V + E), Space: O(V).
    """
    if source < 0 or source >= graph.n:
        raise ValueError(f"Source {source} out of range [0, {graph.n})")

    dist: dict[int, int] = {source: 0}
    parent: dict[int, int] = {source: -1}
    order: list[int] = []
    queue: deque[int] = deque([source])

    while queue:
        u = queue.popleft()
        order.append(u)
        for v, _ in graph.neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)

    return {
        "algorithm": "bfs",
        "source": source,
        "distances": dist,
        "parent": parent,
        "visit_order": order,
        "nodes_reached": len(order),
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: DFS (Depth-First Search) — iterative
# ═══════════════════════════════════════════════════════════════════════════
def dfs(graph: Graph, source: int) -> dict[str, Any]:
    """
    Iterative DFS from source. Returns discovery/finish times, parent map, order.
    Uses explicit stack to avoid recursion limit issues.
    Time: O(V + E), Space: O(V).
    """
    if source < 0 or source >= graph.n:
        raise ValueError(f"Source {source} out of range [0, {graph.n})")

    visited: set[int] = set()
    parent: dict[int, int] = {source: -1}
    discovery: dict[int, int] = {}
    finish: dict[int, int] = {}
    order: list[int] = []
    timer = 0

    stack: list[tuple[int, bool]] = [(source, False)]

    while stack:
        node, returning = stack.pop()
        if returning:
            finish[node] = timer
            timer += 1
            continue
        if node in visited:
            continue
        visited.add(node)
        discovery[node] = timer
        timer += 1
        order.append(node)
        stack.append((node, True))
        for v, _ in reversed(graph.neighbors(node)):
            if v not in visited:
                parent[v] = node
                stack.append((v, False))

    return {
        "algorithm": "dfs",
        "source": source,
        "discovery_time": discovery,
        "finish_time": finish,
        "parent": parent,
        "visit_order": order,
        "nodes_reached": len(order),
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Dijkstra's Shortest Path
# ═══════════════════════════════════════════════════════════════════════════
def dijkstra(
    graph: Graph, source: int, target: Optional[int] = None
) -> dict[str, Any]:
    """
    Dijkstra's single-source shortest path using a min-heap.
    Requires non-negative edge weights.
    Time: O((V + E) log V), Space: O(V).
    """
    if source < 0 or source >= graph.n:
        raise ValueError(f"Source {source} out of range [0, {graph.n})")

    dist: list[float] = [FLOAT_INF] * graph.n
    dist[source] = 0.0
    parent: list[int] = [-1] * graph.n
    visited: list[bool] = [False] * graph.n
    heap: list[tuple[float, int]] = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        if target is not None and u == target:
            break
        for v, w in graph.neighbors(u):
            if w < 0:
                raise ValueError(f"Negative edge weight {w} on edge ({u},{v}). Use Bellman-Ford.")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    result: dict[str, Any] = {
        "algorithm": "dijkstra",
        "source": source,
        "distances": {i: dist[i] for i in range(graph.n) if dist[i] < FLOAT_INF},
        "complexity": "O((V+E) log V)",
    }

    if target is not None:
        path: list[int] = []
        if dist[target] < FLOAT_INF:
            cur = target
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
        result["target"] = target
        result["target_distance"] = dist[target] if dist[target] < FLOAT_INF else None
        result["path"] = path if path else None

    return result


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Bellman-Ford
# ═══════════════════════════════════════════════════════════════════════════
def bellman_ford(graph: Graph, source: int) -> dict[str, Any]:
    """
    Bellman-Ford single-source shortest path. Handles negative weights.
    Detects negative-weight cycles.
    Time: O(V * E), Space: O(V).
    """
    if source < 0 or source >= graph.n:
        raise ValueError(f"Source {source} out of range [0, {graph.n})")

    dist: list[float] = [FLOAT_INF] * graph.n
    dist[source] = 0.0
    parent: list[int] = [-1] * graph.n
    edge_list: list[tuple[int, int, float]] = []

    for u in range(graph.n):
        for v, w in graph.neighbors(u):
            edge_list.append((u, v, w))

    for _ in range(graph.n - 1):
        updated = False
        for u, v, w in edge_list:
            if dist[u] < FLOAT_INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    negative_cycle = False
    negative_cycle_nodes: list[int] = []
    for u, v, w in edge_list:
        if dist[u] < FLOAT_INF and dist[u] + w < dist[v]:
            negative_cycle = True
            visited_neg: set[int] = set()
            node = v
            while node not in visited_neg:
                visited_neg.add(node)
                node = parent[node]
            cycle_start = node
            cycle_node = parent[cycle_start]
            negative_cycle_nodes = [cycle_start]
            while cycle_node != cycle_start:
                negative_cycle_nodes.append(cycle_node)
                cycle_node = parent[cycle_node]
            negative_cycle_nodes.append(cycle_start)
            negative_cycle_nodes.reverse()
            break

    return {
        "algorithm": "bellman_ford",
        "source": source,
        "distances": {i: dist[i] for i in range(graph.n) if dist[i] < FLOAT_INF},
        "parent": {i: parent[i] for i in range(graph.n) if parent[i] != -1},
        "negative_cycle_detected": negative_cycle,
        "negative_cycle_nodes": negative_cycle_nodes if negative_cycle else [],
        "complexity": "O(V * E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Floyd-Warshall (All-Pairs Shortest Path)
# ═══════════════════════════════════════════════════════════════════════════
def floyd_warshall(graph: Graph) -> dict[str, Any]:
    """
    Floyd-Warshall all-pairs shortest path.
    Time: O(V^3), Space: O(V^2).
    Practical limit: ~2000 nodes.
    """
    n = graph.n
    if n > 2000:
        raise ValueError(f"Floyd-Warshall impractical for {n} nodes (limit 2000)")

    dist = graph.adjacency_matrix()
    nxt: list[list[int]] = [[-1] * n for _ in range(n)]

    for u in range(n):
        for v, _ in graph.neighbors(u):
            nxt[u][v] = v

    for k in range(n):
        for i in range(n):
            if dist[i][k] == FLOAT_INF:
                continue
            for j in range(n):
                if dist[k][j] == FLOAT_INF:
                    continue
                candidate = dist[i][k] + dist[k][j]
                if candidate < dist[i][j]:
                    dist[i][j] = candidate
                    nxt[i][j] = nxt[i][k]

    negative_cycle = any(dist[i][i] < 0 for i in range(n))

    pairs: dict[str, float] = {}
    for i in range(n):
        for j in range(n):
            if dist[i][j] < FLOAT_INF and i != j:
                pairs[f"{i}->{j}"] = round(dist[i][j], 10)

    return {
        "algorithm": "floyd_warshall",
        "all_pairs_distances": pairs,
        "negative_cycle_detected": negative_cycle,
        "num_nodes": n,
        "complexity": "O(V^3)",
    }


def floyd_warshall_path(
    graph: Graph, source: int, target: int
) -> dict[str, Any]:
    """Reconstruct shortest path between two nodes via Floyd-Warshall."""
    n = graph.n
    if n > 2000:
        raise ValueError(f"Floyd-Warshall impractical for {n} nodes")

    dist = graph.adjacency_matrix()
    nxt: list[list[int]] = [[-1] * n for _ in range(n)]

    for u in range(n):
        for v, _ in graph.neighbors(u):
            nxt[u][v] = v

    for k in range(n):
        for i in range(n):
            if dist[i][k] == FLOAT_INF:
                continue
            for j in range(n):
                if dist[k][j] == FLOAT_INF:
                    continue
                candidate = dist[i][k] + dist[k][j]
                if candidate < dist[i][j]:
                    dist[i][j] = candidate
                    nxt[i][j] = nxt[i][k]

    path: list[int] = []
    if nxt[source][target] != -1:
        cur = source
        while cur != target:
            path.append(cur)
            cur = nxt[cur][target]
            if cur == -1:
                path = []
                break
        if cur == target:
            path.append(target)

    return {
        "algorithm": "floyd_warshall_path",
        "source": source,
        "target": target,
        "distance": dist[source][target] if dist[source][target] < FLOAT_INF else None,
        "path": path if path else None,
        "complexity": "O(V^3)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Kruskal's MST (Union-Find)
# ═══════════════════════════════════════════════════════════════════════════
def kruskal_mst(graph: Graph) -> dict[str, Any]:
    """
    Kruskal's minimum spanning tree using union-find.
    Time: O(E log E), Space: O(V).
    """
    if graph.directed:
        raise ValueError("MST is defined for undirected graphs only")

    edges_sorted = sorted(graph.edges(), key=lambda e: e[2])
    uf = UnionFind(graph.n)
    mst_edges: list[tuple[int, int, float]] = []
    total_weight = 0.0

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == graph.n - 1:
                break

    is_connected = uf.components == 1 or (graph.n <= 1)

    return {
        "algorithm": "kruskal_mst",
        "mst_edges": [(u, v, round(w, 10)) for u, v, w in mst_edges],
        "total_weight": round(total_weight, 10),
        "num_mst_edges": len(mst_edges),
        "is_spanning": len(mst_edges) == graph.n - 1,
        "graph_connected": is_connected,
        "complexity": "O(E log E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Prim's MST (Priority Queue)
# ═══════════════════════════════════════════════════════════════════════════
def prim_mst(graph: Graph, start: int = 0) -> dict[str, Any]:
    """
    Prim's minimum spanning tree using a min-heap.
    Time: O((V + E) log V), Space: O(V).
    """
    if graph.directed:
        raise ValueError("MST is defined for undirected graphs only")
    if start < 0 or start >= graph.n:
        raise ValueError(f"Start node {start} out of range")

    in_mst: list[bool] = [False] * graph.n
    mst_edges: list[tuple[int, int, float]] = []
    total_weight = 0.0
    heap: list[tuple[float, int, int]] = [(0.0, start, -1)]

    while heap and len(mst_edges) < graph.n - 1:
        w, u, parent_node = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        if parent_node != -1:
            mst_edges.append((parent_node, u, w))
            total_weight += w
        for v, ew in graph.neighbors(u):
            if not in_mst[v]:
                heapq.heappush(heap, (ew, v, u))

    nodes_reached = sum(in_mst)

    return {
        "algorithm": "prim_mst",
        "mst_edges": [(u, v, round(w, 10)) for u, v, w in mst_edges],
        "total_weight": round(total_weight, 10),
        "num_mst_edges": len(mst_edges),
        "is_spanning": len(mst_edges) == graph.n - 1,
        "nodes_reached": nodes_reached,
        "complexity": "O((V+E) log V)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Ford-Fulkerson / Edmonds-Karp (Max Flow)
# ═══════════════════════════════════════════════════════════════════════════
def edmonds_karp(graph: Graph, source: int, sink: int) -> dict[str, Any]:
    """
    Edmonds-Karp implementation of Ford-Fulkerson max-flow.
    Uses BFS to find augmenting paths (guarantees O(V * E^2)).
    """
    if source < 0 or source >= graph.n:
        raise ValueError(f"Source {source} out of range")
    if sink < 0 or sink >= graph.n:
        raise ValueError(f"Sink {sink} out of range")
    if source == sink:
        raise ValueError("Source and sink must be different")

    n = graph.n
    capacity: list[list[float]] = [[0.0] * n for _ in range(n)]
    for u in range(n):
        for v, w in graph.neighbors(u):
            capacity[u][v] += w

    flow_matrix: list[list[float]] = [[0.0] * n for _ in range(n)]
    max_flow = 0.0
    augmenting_paths: list[dict[str, Any]] = []

    def bfs_augment() -> Optional[list[int]]:
        parent_arr = [-1] * n
        parent_arr[source] = source
        queue: deque[tuple[int, float]] = deque([(source, FLOAT_INF)])
        while queue:
            u, f = queue.popleft()
            for v in range(n):
                residual = capacity[u][v] - flow_matrix[u][v]
                if parent_arr[v] == -1 and residual > 0:
                    parent_arr[v] = u
                    new_flow = min(f, residual)
                    if v == sink:
                        path_list: list[int] = []
                        cur = v
                        while cur != source:
                            path_list.append(cur)
                            cur = parent_arr[cur]
                        path_list.append(source)
                        path_list.reverse()
                        return path_list
                    queue.append((v, new_flow))
        return None

    iteration = 0
    while True:
        path = bfs_augment()
        if path is None:
            break
        bottleneck = FLOAT_INF
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            bottleneck = min(bottleneck, capacity[u][v] - flow_matrix[u][v])

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow_matrix[u][v] += bottleneck
            flow_matrix[v][u] -= bottleneck

        max_flow += bottleneck
        iteration += 1
        augmenting_paths.append({"path": path, "flow": round(bottleneck, 10), "iteration": iteration})

    min_cut_nodes: set[int] = set()
    visited_cut: set[int] = {source}
    q: deque[int] = deque([source])
    while q:
        u = q.popleft()
        min_cut_nodes.add(u)
        for v in range(n):
            if v not in visited_cut and capacity[u][v] - flow_matrix[u][v] > 0:
                visited_cut.add(v)
                q.append(v)

    min_cut_edges: list[tuple[int, int, float]] = []
    for u in min_cut_nodes:
        for v in range(n):
            if v not in min_cut_nodes and capacity[u][v] > 0:
                min_cut_edges.append((u, v, round(capacity[u][v], 10)))

    return {
        "algorithm": "edmonds_karp",
        "source": source,
        "sink": sink,
        "max_flow": round(max_flow, 10),
        "augmenting_paths": augmenting_paths[:20],
        "num_augmenting_paths": len(augmenting_paths),
        "min_cut_source_side": sorted(min_cut_nodes),
        "min_cut_edges": min_cut_edges,
        "min_cut_value": round(max_flow, 10),
        "complexity": "O(V * E^2)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Topological Sort (Kahn's BFS-based)
# ═══════════════════════════════════════════════════════════════════════════
def topological_sort(graph: Graph) -> dict[str, Any]:
    """
    Kahn's algorithm for topological sorting of a DAG.
    Time: O(V + E), Space: O(V).
    """
    if not graph.directed:
        raise ValueError("Topological sort requires a directed graph")

    in_degree: list[int] = [0] * graph.n
    for u in range(graph.n):
        for v, _ in graph.neighbors(u):
            in_degree[v] += 1

    queue: deque[int] = deque(v for v in range(graph.n) if in_degree[v] == 0)
    order: list[int] = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v, _ in graph.neighbors(u):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    is_dag = len(order) == graph.n

    return {
        "algorithm": "topological_sort",
        "order": order if is_dag else [],
        "is_dag": is_dag,
        "nodes_processed": len(order),
        "total_nodes": graph.n,
        "has_cycle": not is_dag,
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Cycle Detection (DFS coloring)
# ═══════════════════════════════════════════════════════════════════════════
WHITE, GRAY, BLACK = 0, 1, 2


def detect_cycle(graph: Graph) -> dict[str, Any]:
    """
    DFS-based cycle detection using three-color marking.
    Works for both directed and undirected graphs.
    Time: O(V + E).
    """
    color: list[int] = [WHITE] * graph.n
    parent_arr: list[int] = [-1] * graph.n
    has_cycle = False
    cycle_nodes: list[int] = []

    if graph.directed:
        def _dfs_directed(start: int) -> bool:
            nonlocal has_cycle, cycle_nodes
            stack: list[tuple[int, int]] = [(start, 0)]
            color[start] = GRAY
            while stack:
                u, idx = stack.pop()
                nbrs = graph.neighbors(u)
                if idx < len(nbrs):
                    stack.append((u, idx + 1))
                    v, _ = nbrs[idx]
                    if color[v] == GRAY:
                        has_cycle = True
                        cycle = [v]
                        cur = u
                        while cur != v:
                            cycle.append(cur)
                            cur = parent_arr[cur]
                        cycle.append(v)
                        cycle.reverse()
                        cycle_nodes = cycle
                        return True
                    elif color[v] == WHITE:
                        color[v] = GRAY
                        parent_arr[v] = u
                        stack.append((v, 0))
                else:
                    color[u] = BLACK
            return False

        for node in range(graph.n):
            if color[node] == WHITE:
                if _dfs_directed(node):
                    break
    else:
        def _dfs_undirected(start: int) -> bool:
            nonlocal has_cycle, cycle_nodes
            stack: list[tuple[int, int, int]] = [(start, -1, 0)]
            color[start] = GRAY
            while stack:
                u, par, idx = stack.pop()
                nbrs = graph.neighbors(u)
                if idx < len(nbrs):
                    stack.append((u, par, idx + 1))
                    v, _ = nbrs[idx]
                    if v == par:
                        continue
                    if color[v] == GRAY:
                        has_cycle = True
                        cycle = [v, u]
                        cur = u
                        while parent_arr[cur] != -1 and parent_arr[cur] != v:
                            cur = parent_arr[cur]
                            cycle.append(cur)
                        if parent_arr[cur] == v:
                            cycle.append(v)
                        cycle_nodes = cycle
                        return True
                    elif color[v] == WHITE:
                        color[v] = GRAY
                        parent_arr[v] = u
                        stack.append((v, u, 0))
                else:
                    color[u] = BLACK
            return False

        for node in range(graph.n):
            if color[node] == WHITE:
                if _dfs_undirected(node):
                    break

    return {
        "algorithm": "cycle_detection",
        "has_cycle": has_cycle,
        "cycle_nodes": cycle_nodes if has_cycle else [],
        "directed": graph.directed,
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Connected Components (BFS)
# ═══════════════════════════════════════════════════════════════════════════
def connected_components(graph: Graph) -> dict[str, Any]:
    """
    Find connected components via BFS (undirected).
    For directed graphs, finds strongly connected components via Kosaraju.
    Time: O(V + E).
    """
    if graph.directed:
        return _strongly_connected_components(graph)

    visited: set[int] = set()
    components: list[list[int]] = []

    for start in range(graph.n):
        if start in visited:
            continue
        component: list[int] = []
        queue: deque[int] = deque([start])
        visited.add(start)
        while queue:
            u = queue.popleft()
            component.append(u)
            for v, _ in graph.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        components.append(sorted(component))

    return {
        "algorithm": "connected_components",
        "num_components": len(components),
        "components": components,
        "largest_component_size": max(len(c) for c in components) if components else 0,
        "is_connected": len(components) <= 1,
        "complexity": "O(V + E)",
    }


def _strongly_connected_components(graph: Graph) -> dict[str, Any]:
    """Kosaraju's algorithm for strongly connected components."""
    n = graph.n
    visited: set[int] = set()
    finish_order: list[int] = []

    for start in range(n):
        if start in visited:
            continue
        stack: list[tuple[int, int]] = [(start, 0)]
        visited.add(start)
        while stack:
            u, idx = stack.pop()
            nbrs = graph.neighbors(u)
            if idx < len(nbrs):
                stack.append((u, idx + 1))
                v, _ = nbrs[idx]
                if v not in visited:
                    visited.add(v)
                    stack.append((v, 0))
            else:
                finish_order.append(u)

    rev = graph.reverse()
    visited2: set[int] = set()
    sccs: list[list[int]] = []

    for node in reversed(finish_order):
        if node in visited2:
            continue
        scc: list[int] = []
        q: deque[int] = deque([node])
        visited2.add(node)
        while q:
            u = q.popleft()
            scc.append(u)
            for v, _ in rev.neighbors(u):
                if v not in visited2:
                    visited2.add(v)
                    q.append(v)
        sccs.append(sorted(scc))

    return {
        "algorithm": "strongly_connected_components",
        "num_components": len(sccs),
        "components": sccs,
        "largest_component_size": max(len(c) for c in sccs) if sccs else 0,
        "is_strongly_connected": len(sccs) <= 1,
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Bipartite Check (BFS 2-coloring)
# ═══════════════════════════════════════════════════════════════════════════
def is_bipartite(graph: Graph) -> dict[str, Any]:
    """
    Check bipartiteness via BFS 2-coloring.
    Time: O(V + E).
    """
    color_arr: list[int] = [-1] * graph.n
    bipartite = True
    partition_a: list[int] = []
    partition_b: list[int] = []
    odd_cycle: list[int] = []

    for start in range(graph.n):
        if color_arr[start] != -1:
            continue
        color_arr[start] = 0
        queue: deque[int] = deque([start])
        parent_map: dict[int, int] = {start: -1}
        while queue and bipartite:
            u = queue.popleft()
            for v, _ in graph.neighbors(u):
                if color_arr[v] == -1:
                    color_arr[v] = 1 - color_arr[u]
                    parent_map[v] = u
                    queue.append(v)
                elif color_arr[v] == color_arr[u]:
                    bipartite = False
                    path_u: list[int] = []
                    path_v: list[int] = []
                    a, b = u, v
                    while a != -1:
                        path_u.append(a)
                        a = parent_map.get(a, -1)
                    while b != -1:
                        path_v.append(b)
                        b = parent_map.get(b, -1)
                    set_u = set(path_u)
                    lca = -1
                    for node in path_v:
                        if node in set_u:
                            lca = node
                            break
                    if lca != -1:
                        cycle_part_1 = []
                        for node in path_u:
                            cycle_part_1.append(node)
                            if node == lca:
                                break
                        cycle_part_2 = []
                        for node in path_v:
                            if node == lca:
                                break
                            cycle_part_2.append(node)
                        cycle_part_2.reverse()
                        odd_cycle = cycle_part_1 + cycle_part_2
                    break

    if bipartite:
        for i in range(graph.n):
            if color_arr[i] == 0:
                partition_a.append(i)
            else:
                partition_b.append(i)

    return {
        "algorithm": "bipartite_check",
        "is_bipartite": bipartite,
        "partition_a": sorted(partition_a) if bipartite else [],
        "partition_b": sorted(partition_b) if bipartite else [],
        "odd_cycle": odd_cycle if not bipartite else [],
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Graph Coloring (Greedy)
# ═══════════════════════════════════════════════════════════════════════════
def greedy_coloring(graph: Graph, order: Optional[list[int]] = None) -> dict[str, Any]:
    """
    Greedy graph coloring. Uses given ordering or default (0..n-1).
    Not optimal but fast. Time: O(V + E).
    """
    n = graph.n
    if order is None:
        order = list(range(n))

    color_assignment: list[int] = [-1] * n
    num_colors = 0

    for u in order:
        neighbor_colors: set[int] = set()
        for v, _ in graph.neighbors(u):
            if color_assignment[v] != -1:
                neighbor_colors.add(color_assignment[v])
        c = 0
        while c in neighbor_colors:
            c += 1
        color_assignment[u] = c
        num_colors = max(num_colors, c + 1)

    color_classes: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        color_classes[color_assignment[i]].append(i)

    return {
        "algorithm": "greedy_coloring",
        "num_colors_used": num_colors,
        "coloring": {i: color_assignment[i] for i in range(n)},
        "color_classes": {str(k): v for k, v in sorted(color_classes.items())},
        "is_optimal": "unknown (greedy — may not be chromatic number)",
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Clustering Coefficient
# ═══════════════════════════════════════════════════════════════════════════
def clustering_coefficient(graph: Graph) -> dict[str, Any]:
    """
    Local and global clustering coefficients.
    Local: fraction of node's neighbor pairs that are connected.
    Global: 3 * triangles / triples.
    Time: O(V * d^2) where d is average degree.
    """
    local_cc: dict[int, float] = {}
    total_triangles = 0
    total_triples = 0

    for u in range(graph.n):
        neighbors_u = {v for v, _ in graph.neighbors(u)}
        k = len(neighbors_u)
        if k < 2:
            local_cc[u] = 0.0
            continue
        connected_pairs = 0
        for v in neighbors_u:
            for w, _ in graph.neighbors(v):
                if w in neighbors_u and w != v:
                    connected_pairs += 1
        if not graph.directed:
            connected_pairs //= 2
        possible = k * (k - 1) // 2
        local_cc[u] = connected_pairs / possible if possible > 0 else 0.0
        total_triangles += connected_pairs
        total_triples += possible

    if not graph.directed:
        total_triangles //= 3

    global_cc = (3 * total_triangles / total_triples) if total_triples > 0 else 0.0
    avg_cc = sum(local_cc.values()) / len(local_cc) if local_cc else 0.0

    return {
        "algorithm": "clustering_coefficient",
        "global_clustering_coefficient": round(global_cc, 8),
        "average_local_clustering_coefficient": round(avg_cc, 8),
        "local_coefficients": {k: round(v, 8) for k, v in local_cc.items()},
        "num_triangles": total_triangles,
        "complexity": "O(V * d^2)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# CENTRALITY: Degree Centrality
# ═══════════════════════════════════════════════════════════════════════════
def degree_centrality(graph: Graph) -> dict[str, Any]:
    """
    Degree centrality = degree(v) / (n - 1).
    Time: O(V + E).
    """
    n = graph.n
    denom = max(n - 1, 1)
    centrality: dict[int, float] = {}
    for v in range(n):
        centrality[v] = round(graph.degree(v) / denom, 8)

    ranked = sorted(centrality.items(), key=lambda x: -x[1])

    return {
        "algorithm": "degree_centrality",
        "centrality": centrality,
        "top_10": ranked[:10],
        "max_centrality_node": ranked[0][0] if ranked else None,
        "max_centrality_value": ranked[0][1] if ranked else 0.0,
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# CENTRALITY: Betweenness Centrality (Brandes' Algorithm)
# ═══════════════════════════════════════════════════════════════════════════
def betweenness_centrality(graph: Graph) -> dict[str, Any]:
    """
    Brandes' algorithm for betweenness centrality.
    Time: O(V * E) for unweighted, O(V * E + V^2 log V) weighted.
    """
    n = graph.n
    bc: list[float] = [0.0] * n

    for s in range(n):
        stack: list[int] = []
        pred: list[list[int]] = [[] for _ in range(n)]
        sigma: list[int] = [0] * n
        sigma[s] = 1
        dist_arr: list[float] = [FLOAT_INF] * n
        dist_arr[s] = 0.0

        if not graph.weighted:
            queue: deque[int] = deque([s])
            while queue:
                v = queue.popleft()
                stack.append(v)
                for w, _ in graph.neighbors(v):
                    if dist_arr[w] == FLOAT_INF:
                        dist_arr[w] = dist_arr[v] + 1
                        queue.append(w)
                    if dist_arr[w] == dist_arr[v] + 1:
                        sigma[w] += sigma[v]
                        pred[w].append(v)
        else:
            heap_b: list[tuple[float, int]] = [(0.0, s)]
            while heap_b:
                d, v = heapq.heappop(heap_b)
                if d > dist_arr[v]:
                    continue
                stack.append(v)
                for w, wt in graph.neighbors(v):
                    nd = dist_arr[v] + wt
                    if nd < dist_arr[w]:
                        dist_arr[w] = nd
                        sigma[w] = sigma[v]
                        pred[w] = [v]
                        heapq.heappush(heap_b, (nd, w))
                    elif abs(nd - dist_arr[w]) < 1e-12:
                        sigma[w] += sigma[v]
                        pred[w].append(v)

        delta: list[float] = [0.0] * n
        while stack:
            w = stack.pop()
            for v in pred[w]:
                ratio = sigma[v] / sigma[w] if sigma[w] > 0 else 0.0
                delta[v] += ratio * (1.0 + delta[w])
            if w != s:
                bc[w] += delta[w]

    if not graph.directed:
        for i in range(n):
            bc[i] /= 2.0

    centrality = {i: round(bc[i], 8) for i in range(n)}
    ranked = sorted(centrality.items(), key=lambda x: -x[1])

    return {
        "algorithm": "betweenness_centrality",
        "centrality": centrality,
        "top_10": ranked[:10],
        "max_centrality_node": ranked[0][0] if ranked else None,
        "max_centrality_value": ranked[0][1] if ranked else 0.0,
        "complexity": "O(V * E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# CENTRALITY: Closeness Centrality
# ═══════════════════════════════════════════════════════════════════════════
def closeness_centrality(graph: Graph) -> dict[str, Any]:
    """
    Closeness centrality = (n-1) / sum(d(v, u) for all u).
    Uses BFS (unweighted) or Dijkstra (weighted) for distances.
    Time: O(V * (V + E)) unweighted, O(V * (V + E) log V) weighted.
    """
    n = graph.n
    centrality: dict[int, float] = {}

    for v in range(n):
        if graph.weighted:
            d = dijkstra(graph, v)["distances"]
        else:
            d = bfs(graph, v)["distances"]

        reachable = {u: dist for u, dist in d.items() if u != v and dist < FLOAT_INF}
        if len(reachable) == 0:
            centrality[v] = 0.0
        else:
            total_dist = sum(reachable.values())
            if total_dist > 0:
                centrality[v] = round(len(reachable) / total_dist, 8)
            else:
                centrality[v] = 0.0

    ranked = sorted(centrality.items(), key=lambda x: -x[1])

    return {
        "algorithm": "closeness_centrality",
        "centrality": centrality,
        "top_10": ranked[:10],
        "max_centrality_node": ranked[0][0] if ranked else None,
        "max_centrality_value": ranked[0][1] if ranked else 0.0,
        "complexity": "O(V * (V + E))",
    }


# ═══════════════════════════════════════════════════════════════════════════
# CENTRALITY: PageRank (Power Iteration)
# ═══════════════════════════════════════════════════════════════════════════
def pagerank(
    graph: Graph,
    damping: float = PAGERANK_DAMPING,
    max_iter: int = PAGERANK_ITERATIONS,
    tol: float = PAGERANK_TOLERANCE,
) -> dict[str, Any]:
    """
    PageRank via power iteration.
    Time: O(iterations * (V + E)).
    """
    n = graph.n
    if n == 0:
        return {"algorithm": "pagerank", "scores": {}, "iterations": 0}

    rank: list[float] = [1.0 / n] * n
    out_degree: list[int] = [0] * n

    for u in range(n):
        out_degree[u] = graph.degree(u)

    converged = False
    actual_iters = 0

    for iteration in range(max_iter):
        new_rank: list[float] = [(1.0 - damping) / n] * n
        dangling_sum = 0.0

        for u in range(n):
            if out_degree[u] == 0:
                dangling_sum += rank[u]

        dangling_contrib = damping * dangling_sum / n

        for u in range(n):
            if out_degree[u] > 0:
                share = damping * rank[u] / out_degree[u]
                for v, _ in graph.neighbors(u):
                    new_rank[v] += share

        for u in range(n):
            new_rank[u] += dangling_contrib

        diff = sum(abs(new_rank[i] - rank[i]) for i in range(n))
        rank = new_rank
        actual_iters = iteration + 1

        if diff < tol:
            converged = True
            break

    scores = {i: round(rank[i], 10) for i in range(n)}
    ranked = sorted(scores.items(), key=lambda x: -x[1])

    return {
        "algorithm": "pagerank",
        "scores": scores,
        "top_10": ranked[:10],
        "damping_factor": damping,
        "iterations": actual_iters,
        "converged": converged,
        "max_rank_node": ranked[0][0] if ranked else None,
        "max_rank_value": ranked[0][1] if ranked else 0.0,
        "sum_ranks": round(sum(rank), 8),
        "complexity": f"O({actual_iters} * (V + E))",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Eulerian Path / Circuit Check
# ═══════════════════════════════════════════════════════════════════════════
def eulerian_check(graph: Graph) -> dict[str, Any]:
    """
    Check if graph has Eulerian path or circuit.
    Undirected: circuit if all even degree, path if exactly 2 odd.
    Directed: circuit if in-degree == out-degree for all, path if at most 1 difference.
    """
    n = graph.n
    if graph.directed:
        in_deg: list[int] = [0] * n
        out_deg: list[int] = [0] * n
        for u in range(n):
            for v, _ in graph.neighbors(u):
                out_deg[u] += 1
                in_deg[v] += 1

        start_nodes = 0
        end_nodes = 0
        has_circuit = True
        has_path = True

        for v in range(n):
            diff = out_deg[v] - in_deg[v]
            if diff == 1:
                start_nodes += 1
            elif diff == -1:
                end_nodes += 1
            elif diff != 0:
                has_circuit = False
                has_path = False

        if start_nodes == 0 and end_nodes == 0:
            has_circuit = True
            has_path = True
        elif start_nodes == 1 and end_nodes == 1:
            has_circuit = False
            has_path = True
        else:
            has_circuit = False
            has_path = False

        return {
            "algorithm": "eulerian_check",
            "directed": True,
            "has_eulerian_circuit": has_circuit,
            "has_eulerian_path": has_path,
            "in_degrees": {i: in_deg[i] for i in range(n)},
            "out_degrees": {i: out_deg[i] for i in range(n)},
        }
    else:
        degrees = [graph.degree(v) for v in range(n)]
        odd_count = sum(1 for d in degrees if d % 2 != 0)

        cc_result = connected_components(graph)
        non_isolated = [c for c in cc_result["components"] if len(c) > 1 or graph.degree(c[0]) > 0]
        is_connected_relevant = len(non_isolated) <= 1

        has_circuit = odd_count == 0 and is_connected_relevant
        has_path = odd_count in (0, 2) and is_connected_relevant

        return {
            "algorithm": "eulerian_check",
            "directed": False,
            "has_eulerian_circuit": has_circuit,
            "has_eulerian_path": has_path,
            "odd_degree_nodes": [v for v in range(n) if degrees[v] % 2 != 0],
            "odd_degree_count": odd_count,
            "is_connected": is_connected_relevant,
        }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Bridge Detection (Tarjan's)
# ═══════════════════════════════════════════════════════════════════════════
def find_bridges(graph: Graph) -> dict[str, Any]:
    """
    Find all bridges in an undirected graph using iterative Tarjan's.
    A bridge is an edge whose removal disconnects the graph.
    Time: O(V + E).
    """
    n = graph.n
    disc: list[int] = [-1] * n
    low: list[int] = [-1] * n
    bridges: list[tuple[int, int]] = []
    timer_val = 0

    for start in range(n):
        if disc[start] != -1:
            continue
        stack: list[tuple[int, int, int]] = [(start, -1, 0)]
        disc[start] = low[start] = timer_val
        timer_val += 1

        while stack:
            u, par, idx = stack.pop()
            nbrs = graph.neighbors(u)
            if idx < len(nbrs):
                stack.append((u, par, idx + 1))
                v, _ = nbrs[idx]
                if v == par:
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = timer_val
                    timer_val += 1
                    stack.append((v, u, 0))
                else:
                    low[u] = min(low[u], disc[v])
            else:
                if par != -1:
                    low[par] = min(low[par], low[u])
                    if low[u] > disc[par]:
                        bridges.append((par, u))

    return {
        "algorithm": "bridge_detection",
        "bridges": bridges,
        "num_bridges": len(bridges),
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Articulation Points
# ═══════════════════════════════════════════════════════════════════════════
def find_articulation_points(graph: Graph) -> dict[str, Any]:
    """
    Find all articulation points (cut vertices) in an undirected graph.
    Uses iterative approach. Time: O(V + E).
    """
    n = graph.n
    disc: list[int] = [-1] * n
    low: list[int] = [-1] * n
    parent_arr: list[int] = [-1] * n
    ap_set: set[int] = set()
    timer_val = 0

    for start in range(n):
        if disc[start] != -1:
            continue
        disc[start] = low[start] = timer_val
        timer_val += 1
        child_count: dict[int, int] = defaultdict(int)
        stack: list[tuple[int, int]] = [(start, 0)]

        while stack:
            u, idx = stack.pop()
            nbrs = graph.neighbors(u)
            if idx < len(nbrs):
                stack.append((u, idx + 1))
                v, _ = nbrs[idx]
                if disc[v] == -1:
                    parent_arr[v] = u
                    child_count[u] = child_count.get(u, 0) + 1
                    disc[v] = low[v] = timer_val
                    timer_val += 1
                    stack.append((v, 0))
                elif v != parent_arr[u]:
                    low[u] = min(low[u], disc[v])
            else:
                p = parent_arr[u]
                if p != -1:
                    low[p] = min(low[p], low[u])
                    if parent_arr[p] != -1 and low[u] >= disc[p]:
                        ap_set.add(p)
                    if parent_arr[p] == -1 and child_count.get(p, 0) > 1:
                        ap_set.add(p)

    return {
        "algorithm": "articulation_points",
        "articulation_points": sorted(ap_set),
        "num_articulation_points": len(ap_set),
        "complexity": "O(V + E)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM: Graph Diameter (BFS-based for unweighted)
# ═══════════════════════════════════════════════════════════════════════════
def graph_diameter(graph: Graph) -> dict[str, Any]:
    """
    Compute diameter (longest shortest path) of the graph.
    For small graphs, computes all-pairs BFS/Dijkstra.
    Time: O(V * (V + E)).
    """
    n = graph.n
    diameter = 0
    endpoints = (0, 0)
    eccentricities: dict[int, float] = {}

    for v in range(n):
        if graph.weighted:
            dists = dijkstra(graph, v)["distances"]
        else:
            dists = bfs(graph, v)["distances"]

        max_dist = 0
        for u, d in dists.items():
            if d < FLOAT_INF and d > max_dist:
                max_dist = d
        eccentricities[v] = max_dist
        if max_dist > diameter:
            diameter = max_dist
            endpoints = (v, max(dists, key=lambda k: dists[k]))

    radius = min(eccentricities.values()) if eccentricities else 0
    center = [v for v, e in eccentricities.items() if e == radius]

    return {
        "algorithm": "graph_diameter",
        "diameter": diameter,
        "radius": radius,
        "center": center,
        "endpoints": endpoints,
        "eccentricities": eccentricities,
        "complexity": "O(V * (V + E))",
    }


# ═══════════════════════════════════════════════════════════════════════════
# ALGORITHM DISPATCHER
# ═══════════════════════════════════════════════════════════════════════════
ALGORITHM_REGISTRY: dict[str, Any] = {
    "bfs": bfs,
    "dfs": dfs,
    "dijkstra": dijkstra,
    "bellman_ford": bellman_ford,
    "floyd_warshall": floyd_warshall,
    "floyd_warshall_path": floyd_warshall_path,
    "kruskal_mst": kruskal_mst,
    "prim_mst": prim_mst,
    "edmonds_karp": edmonds_karp,
    "max_flow": edmonds_karp,
    "ford_fulkerson": edmonds_karp,
    "topological_sort": topological_sort,
    "cycle_detection": detect_cycle,
    "connected_components": connected_components,
    "bipartite_check": is_bipartite,
    "greedy_coloring": greedy_coloring,
    "clustering_coefficient": clustering_coefficient,
    "degree_centrality": degree_centrality,
    "betweenness_centrality": betweenness_centrality,
    "closeness_centrality": closeness_centrality,
    "pagerank": pagerank,
    "eulerian_check": eulerian_check,
    "bridges": find_bridges,
    "articulation_points": find_articulation_points,
    "diameter": graph_diameter,
}


def dispatch_algorithm(
    algorithm: str,
    graph: Graph,
    source: Optional[int] = None,
    target: Optional[int] = None,
    params: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Route to the correct algorithm function with appropriate arguments."""
    normalized = normalize_term(algorithm)
    func = ALGORITHM_REGISTRY.get(normalized)
    if func is None:
        raise ValueError(
            f"Unknown algorithm: '{algorithm}'. Available: {sorted(ALGORITHM_REGISTRY.keys())}"
        )

    sig_needs_source = normalized in {
        "bfs", "dfs", "dijkstra", "bellman_ford", "prim_mst",
    }
    sig_needs_source_target = normalized in {
        "edmonds_karp", "max_flow", "ford_fulkerson", "floyd_warshall_path",
    }

    if sig_needs_source_target:
        if source is None or target is None:
            raise ValueError(f"Algorithm '{algorithm}' requires both source and target nodes")
        return func(graph, source, target)
    elif sig_needs_source:
        if source is None:
            source = 0
        if normalized == "dijkstra":
            return func(graph, source, target)
        return func(graph, source)
    elif normalized == "pagerank" and params:
        return func(
            graph,
            damping=params.get("damping", PAGERANK_DAMPING),
            max_iter=params.get("max_iter", PAGERANK_ITERATIONS),
            tol=params.get("tol", PAGERANK_TOLERANCE),
        )
    elif normalized == "greedy_coloring" and params and "order" in params:
        return func(graph, order=params["order"])
    else:
        return func(graph)


# ═══════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════
def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
    """
    Layer 1: Doctrine Cache lookup (0-200ms target)
    Layer 2: Semantic retrieval via normalized terms
    Layer 3: Deep analysis / multi-source synthesis
    """
    t0 = time.time()
    audit_id = str(uuid.uuid4())

    # Layer 1: Doctrine Cache
    doctrine = search_doctrine_cache(query)
    if doctrine:
        DRIFT.record(doctrine.topic)
        TELEMETRY.record_query("doctrine_cache", (time.time() - t0) * 1000, True)
        confidence = doctrine.confidence
        answer = doctrine.conclusion_template
        if mode == ResponseMode.DEFENSE:
            answer += f"\n\nReasoning Framework:\n{doctrine.reasoning_framework}"
            answer += f"\n\nKey Factors: {', '.join(doctrine.key_factors)}"
            answer += f"\n\nAuthority: {', '.join(doctrine.primary_authority)}"
        elif mode == ResponseMode.MEMO:
            answer += f"\n\n--- FULL MEMO ---"
            answer += f"\nTopic: {doctrine.topic}"
            answer += f"\nReasoning:\n{doctrine.reasoning_framework}"
            answer += f"\nKey Factors: {', '.join(doctrine.key_factors)}"
            answer += f"\nAuthority: {', '.join(doctrine.primary_authority)}"
            answer += f"\nConfidence: {confidence} ({doctrine.confidence_stratification})"
            answer += f"\nScope: {doctrine.entity_scope}"

        latency_ms = (time.time() - t0) * 1000
        write_audit_entry({
            "audit_id": audit_id, "query": query, "layer": "doctrine_cache",
            "topic": doctrine.topic, "confidence": confidence, "latency_ms": latency_ms,
        })
        return QueryResponse(
            query=query, answer=answer, doctrine_topic=doctrine.topic,
            reasoning=doctrine.reasoning_framework,
            confidence=confidence,
            confidence_level=stratify_confidence(confidence).value,
            determinism_hash=determinism_hash({"query": query, "answer": answer}),
            latency_ms=round(latency_ms, 3), mode=mode.value, zone=zone.value,
        )

    # Layer 2: Semantic normalization lookup
    normalized_query = " ".join(normalize_term(w) for w in query.split())
    doctrine2 = search_doctrine_cache(normalized_query)
    if doctrine2:
        DRIFT.record(doctrine2.topic)
        TELEMETRY.record_query("semantic_retrieval", (time.time() - t0) * 1000, True)
        answer = doctrine2.conclusion_template
        latency_ms = (time.time() - t0) * 1000
        write_audit_entry({
            "audit_id": audit_id, "query": query, "layer": "semantic_retrieval",
            "normalized": normalized_query, "topic": doctrine2.topic,
            "confidence": doctrine2.confidence, "latency_ms": latency_ms,
        })
        return QueryResponse(
            query=query, answer=answer, doctrine_topic=doctrine2.topic,
            reasoning=doctrine2.reasoning_framework,
            confidence=doctrine2.confidence,
            confidence_level=stratify_confidence(doctrine2.confidence).value,
            determinism_hash=determinism_hash({"query": query, "answer": answer}),
            latency_ms=round(latency_ms, 3), mode=mode.value, zone=zone.value,
        )

    # Layer 3: Deep analysis / knowledge synthesis
    DRIFT.record("deep_analysis")
    TELEMETRY.record_query("deep_analysis", (time.time() - t0) * 1000, False)

    answer = _deep_analysis(query, mode)
    latency_ms = (time.time() - t0) * 1000

    write_audit_entry({
        "audit_id": audit_id, "query": query, "layer": "deep_analysis",
        "latency_ms": latency_ms,
    })

    return QueryResponse(
        query=query, answer=answer, doctrine_topic=None,
        reasoning="Multi-source synthesis — no cached doctrine matched",
        confidence=0.6, confidence_level=ConfidenceLevel.DISCLOSURE.value,
        determinism_hash=determinism_hash({"query": query, "answer": answer}),
        latency_ms=round(latency_ms, 3), mode=mode.value, zone=zone.value,
    )


def _deep_analysis(query: str, mode: ResponseMode) -> str:
    """
    Deep analysis: synthesize answer from algorithm knowledge.
    Matches query keywords to known algorithm descriptions.
    """
    q = query.lower()
    segments: list[str] = []

    knowledge_map: dict[str, str] = {
        "shortest path": (
            "Shortest path algorithms find the minimum-weight path between vertices. "
            "Dijkstra's algorithm (O((V+E)logV)) works for non-negative weights using a min-heap. "
            "Bellman-Ford (O(VE)) handles negative weights and detects negative cycles. "
            "Floyd-Warshall (O(V^3)) computes all-pairs shortest paths."
        ),
        "minimum spanning tree": (
            "A minimum spanning tree connects all vertices with minimum total edge weight. "
            "Kruskal's algorithm (O(E log E)) sorts edges and uses union-find. "
            "Prim's algorithm (O((V+E) log V)) grows the MST from a starting vertex using a priority queue. "
            "Both produce optimal MSTs; Kruskal is better for sparse graphs, Prim for dense."
        ),
        "max flow": (
            "Maximum flow finds the greatest amount of flow from source to sink respecting capacities. "
            "Ford-Fulkerson uses augmenting paths; Edmonds-Karp (O(VE^2)) uses BFS specifically. "
            "The max-flow min-cut theorem states max flow equals the minimum cut capacity."
        ),
        "traversal": (
            "BFS explores level by level using a queue (O(V+E)), finding shortest unweighted paths. "
            "DFS explores as deep as possible using a stack (O(V+E)), useful for cycle detection, "
            "topological sorting, and connected component identification."
        ),
        "centrality": (
            "Centrality measures identify important vertices. Degree centrality counts connections. "
            "Betweenness centrality (Brandes O(VE)) measures how often a node lies on shortest paths. "
            "Closeness centrality measures average distance to all other nodes. "
            "PageRank (power iteration) models importance via random walks with damping."
        ),
        "cycle": (
            "Cycle detection uses DFS coloring (white/gray/black). A back edge to a gray node "
            "indicates a cycle in directed graphs. For undirected, a visited non-parent neighbor "
            "indicates a cycle. Topological sort fails if and only if the graph has a cycle."
        ),
        "coloring": (
            "Graph coloring assigns colors to vertices so no adjacent vertices share a color. "
            "The chromatic number is the minimum colors needed. Greedy coloring is O(V+E) but not "
            "optimal. Finding the chromatic number is NP-hard. Bipartite graphs are 2-colorable."
        ),
        "bipartite": (
            "A graph is bipartite if vertices can be split into two sets with all edges between sets. "
            "Equivalently, bipartite iff it contains no odd-length cycles. "
            "BFS 2-coloring checks bipartiteness in O(V+E)."
        ),
        "euler": (
            "An Eulerian circuit visits every edge exactly once and returns to start. "
            "An undirected graph has one iff connected and all vertices have even degree. "
            "An Eulerian path exists iff connected and exactly 0 or 2 vertices have odd degree."
        ),
        "bridge": (
            "A bridge is an edge whose removal disconnects the graph. "
            "Tarjan's algorithm finds all bridges in O(V+E) using DFS discovery/low values. "
            "An edge (u,v) is a bridge iff low[v] > disc[u]."
        ),
        "clustering": (
            "The clustering coefficient measures the degree to which neighbors of a vertex are connected. "
            "Local CC for vertex v = (edges among neighbors) / (possible edges among neighbors). "
            "Global CC = 3 * triangles / connected triples. High CC indicates community structure."
        ),
        "pagerank": (
            "PageRank models a random surfer who follows links with probability d (damping ~0.85) "
            "and jumps to a random page with probability 1-d. Computed via power iteration until convergence. "
            "Originally used by Google for web page importance ranking."
        ),
    }

    for topic, explanation in knowledge_map.items():
        words = topic.split()
        if any(w in q for w in words):
            segments.append(explanation)

    if not segments:
        segments.append(
            "Graph theory is the study of mathematical structures modeling pairwise relations. "
            "Key concepts include vertices, edges, paths, cycles, trees, and networks. "
            "This engine supports traversals, shortest paths, MST, max flow, centrality, "
            "coloring, bipartite checking, Eulerian paths, bridges, and more. "
            "Please refine your query or use the /algorithm endpoint for computation."
        )

    answer = "\n\n".join(segments)
    if mode == ResponseMode.MEMO:
        answer = f"=== GRAPH THEORY MEMO ===\n\n{answer}\n\n=== END MEMO ==="
    return answer


# ═══════════════════════════════════════════════════════════════════════════
# MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════
class IssueCategory(str, Enum):
    SHORTEST_PATH = "SHORTEST_PATH"
    SPANNING_TREE = "SPANNING_TREE"
    NETWORK_FLOW = "NETWORK_FLOW"
    TRAVERSAL = "TRAVERSAL"
    CYCLE_ANALYSIS = "CYCLE_ANALYSIS"
    CONNECTIVITY = "CONNECTIVITY"
    CENTRALITY = "CENTRALITY"
    COLORING = "COLORING"
    STRUCTURAL = "STRUCTURAL"
    COMBINATORIAL = "COMBINATORIAL"


ISSUE_CATEGORY_KEYWORDS: dict[IssueCategory, list[str]] = {
    IssueCategory.SHORTEST_PATH: ["shortest", "path", "distance", "dijkstra", "bellman", "floyd"],
    IssueCategory.SPANNING_TREE: ["spanning", "mst", "kruskal", "prim", "minimum"],
    IssueCategory.NETWORK_FLOW: ["flow", "capacity", "ford", "fulkerson", "edmonds", "cut"],
    IssueCategory.TRAVERSAL: ["bfs", "dfs", "breadth", "depth", "traversal", "search", "visit"],
    IssueCategory.CYCLE_ANALYSIS: ["cycle", "acyclic", "dag", "topological"],
    IssueCategory.CONNECTIVITY: ["connected", "component", "bridge", "articulation", "biconnected"],
    IssueCategory.CENTRALITY: ["centrality", "pagerank", "betweenness", "closeness", "degree", "importance"],
    IssueCategory.COLORING: ["color", "chromatic", "coloring", "bipartite", "partition"],
    IssueCategory.STRUCTURAL: ["bridge", "euler", "hamiltonian", "diameter", "radius", "clustering"],
    IssueCategory.COMBINATORIAL: ["matching", "cover", "independent", "clique", "dominating"],
}


def classify_query(query: str) -> list[IssueCategory]:
    """Classify a query into issue categories."""
    q = query.lower()
    matches: list[tuple[IssueCategory, int]] = []
    for cat, keywords in ISSUE_CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > 0:
            matches.append((cat, score))
    matches.sort(key=lambda x: -x[1])
    return [cat for cat, _ in matches] if matches else [IssueCategory.TRAVERSAL]


# ═══════════════════════════════════════════════════════════════════════════
# FastAPI Application
# ═══════════════════════════════════════════════════════════════════════════
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    load_doctrine_cache()
    load_semantic_dict()
    load_coverage_map()
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrines, {len(SEMANTIC_DICT)} semantic entries")
    yield
    logger.info(f"Shutting down {ENGINE_NAME}")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant graph theory intelligence engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════
@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Comprehensive health check endpoint (TIE component 12)."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "healthy",
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "domain": ENGINE_DOMAIN,
        "mode": ENGINE_MODE,
        "authority_level": AUTHORITY_LEVEL,
        "uptime_seconds": round(TELEMETRY.uptime_seconds, 1),
        "telemetry": TELEMETRY.snapshot(),
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "semantic_dict_size": len(SEMANTIC_DICT),
        "algorithms_available": sorted(ALGORITHM_REGISTRY.keys()),
        "num_algorithms": len(set(ALGORITHM_REGISTRY.values())),
        "drift": DRIFT.snapshot(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/algorithm", response_model=AlgorithmResponse)
async def run_algorithm(req: AlgorithmRequest) -> AlgorithmResponse:
    """Execute a graph algorithm on the provided graph."""
    t0 = time.time()
    audit_id = str(uuid.uuid4())
    try:
        graph = Graph.from_input(req.graph)
        result = dispatch_algorithm(
            req.algorithm, graph, req.source, req.target, req.params
        )
        latency_ms = (time.time() - t0) * 1000
        TELEMETRY.record_query(req.algorithm, latency_ms, False)

        confidence = 0.95
        det_hash = determinism_hash(result)

        write_audit_entry({
            "audit_id": audit_id, "type": "algorithm", "algorithm": req.algorithm,
            "graph_summary": graph.summary(), "latency_ms": latency_ms,
            "confidence": confidence,
        })

        return AlgorithmResponse(
            algorithm=req.algorithm,
            result=result,
            determinism_hash=det_hash,
            confidence=confidence,
            confidence_level=stratify_confidence(confidence).value,
            latency_ms=round(latency_ms, 3),
            mode=req.mode.value,
            zone=req.zone.value,
            audit_id=audit_id,
        )
    except ValueError as e:
        TELEMETRY.record_error()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        TELEMETRY.record_error()
        logger.error(f"Algorithm execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest) -> QueryResponse:
    """Free-text query about graph theory (three-layer response)."""
    try:
        return three_layer_response(req.query, req.mode, req.zone)
    except Exception as e:
        TELEMETRY.record_error()
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/algorithms")
async def list_algorithms() -> dict[str, Any]:
    """List all available algorithms."""
    algo_info: dict[str, str] = {
        "bfs": "Breadth-First Search — O(V + E)",
        "dfs": "Depth-First Search — O(V + E)",
        "dijkstra": "Dijkstra's Shortest Path — O((V+E) log V)",
        "bellman_ford": "Bellman-Ford Shortest Path — O(V * E)",
        "floyd_warshall": "Floyd-Warshall All-Pairs Shortest Path — O(V^3)",
        "floyd_warshall_path": "Floyd-Warshall with Path Reconstruction — O(V^3)",
        "kruskal_mst": "Kruskal's Minimum Spanning Tree — O(E log E)",
        "prim_mst": "Prim's Minimum Spanning Tree — O((V+E) log V)",
        "edmonds_karp": "Edmonds-Karp Max Flow — O(V * E^2)",
        "topological_sort": "Kahn's Topological Sort — O(V + E)",
        "cycle_detection": "DFS Cycle Detection — O(V + E)",
        "connected_components": "Connected/Strongly-Connected Components — O(V + E)",
        "bipartite_check": "Bipartite Check via 2-Coloring — O(V + E)",
        "greedy_coloring": "Greedy Graph Coloring — O(V + E)",
        "clustering_coefficient": "Local & Global Clustering Coefficient — O(V * d^2)",
        "degree_centrality": "Degree Centrality — O(V + E)",
        "betweenness_centrality": "Brandes Betweenness Centrality — O(V * E)",
        "closeness_centrality": "Closeness Centrality — O(V * (V + E))",
        "pagerank": "PageRank via Power Iteration — O(iter * (V + E))",
        "eulerian_check": "Eulerian Path/Circuit Check — O(V + E)",
        "bridges": "Bridge Detection (Tarjan's) — O(V + E)",
        "articulation_points": "Articulation Point Detection — O(V + E)",
        "diameter": "Graph Diameter — O(V * (V + E))",
    }
    return {"algorithms": algo_info, "count": len(algo_info)}


@app.get("/telemetry")
async def get_telemetry() -> dict[str, Any]:
    """Return engine telemetry snapshot."""
    return TELEMETRY.snapshot()


@app.get("/drift")
async def get_drift() -> dict[str, Any]:
    """Return doctrine drift report."""
    return DRIFT.snapshot()


@app.get("/doctrines")
async def get_doctrines() -> dict[str, Any]:
    """Return loaded doctrine cache summary."""
    return {
        "count": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
    }


@app.get("/coverage")
async def get_coverage() -> dict[str, Any]:
    """Return coverage map."""
    return COVERAGE_MAP if COVERAGE_MAP else {"status": "no coverage map loaded"}


# ═══════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
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
