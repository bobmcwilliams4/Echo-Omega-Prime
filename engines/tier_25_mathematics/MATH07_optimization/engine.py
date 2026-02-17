"""
MATH07 — Optimization Engine
TIE-20 Compliant | Tier 13 Mathematics | Port 8569
Linear programming, nonlinear optimization, constrained optimization,
integer programming, convex optimization, portfolio optimization,
multi-objective optimization, sensitivity analysis.
All solvers are pure-Python implementations.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
sys.path.insert(0, str(ENGINE_DIR.parent))

# ---------------------------------------------------------------------------
# Loguru config
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}",
)
LOG_FILE = ENGINE_DIR / "math07.log"
logger.add(str(LOG_FILE), rotation="10 MB", retention="7 days", level="DEBUG")
AUDIT_FILE = ENGINE_DIR / "audit_trail.jsonl"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "MATH07_optimization"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8569
ENGINE_TIER = 13
ENGINE_DOMAIN = "Mathematics — Optimization"
ENGINE_MODE = "DET"
ENGINE_AUTH = 5.0
FLOAT_TOL = 1e-10
MAX_SIMPLEX_ITERS = 50_000
MAX_GD_ITERS = 100_000
MAX_NEWTON_ITERS = 5_000
MAX_BB_NODES = 100_000
MAX_GOLDEN_ITERS = 1_000
MAX_CG_ITERS = 50_000

# ---------------------------------------------------------------------------
# Enums
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


class OptimizationSense(str, Enum):
    MINIMIZE = "MINIMIZE"
    MAXIMIZE = "MAXIMIZE"


class ConstraintType(str, Enum):
    LEQ = "LEQ"
    GEQ = "GEQ"
    EQ = "EQ"


class SolverStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    INFEASIBLE = "INFEASIBLE"
    UNBOUNDED = "UNBOUNDED"
    MAX_ITER = "MAX_ITER"
    ERROR = "ERROR"


# ---------------------------------------------------------------------------
# Pydantic models — inputs
# ---------------------------------------------------------------------------

class LPConstraint(BaseModel):
    coefficients: list[float]
    constraint_type: ConstraintType = ConstraintType.LEQ
    rhs: float


class LPProblem(BaseModel):
    objective: list[float]
    constraints: list[LPConstraint]
    sense: OptimizationSense = OptimizationSense.MAXIMIZE
    variable_names: Optional[list[str]] = None


class UnconstrainedProblem(BaseModel):
    method: str = "gradient_descent"
    x0: list[float]
    learning_rate: float = 0.01
    max_iter: int = 10000
    tol: float = 1e-8
    function_expr: str = ""
    gradient_expr: Optional[str] = None
    hessian_expr: Optional[str] = None


class GoldenSectionProblem(BaseModel):
    a: float
    b: float
    function_expr: str
    tol: float = 1e-8
    max_iter: int = 500


class LagrangeProblem(BaseModel):
    x0: list[float]
    objective_expr: str
    constraint_exprs: list[str]
    tol: float = 1e-8
    max_iter: int = 1000


class PortfolioProblem(BaseModel):
    expected_returns: list[float]
    covariance_matrix: list[list[float]]
    target_return: Optional[float] = None
    risk_free_rate: float = 0.0
    num_frontier_points: int = 50
    allow_short: bool = False
    asset_names: Optional[list[str]] = None


class MultiObjectiveProblem(BaseModel):
    method: str = "weighted_sum"
    objective_exprs: list[str]
    constraints: list[LPConstraint] = []
    weights: Optional[list[float]] = None
    epsilon_levels: Optional[list[float]] = None
    num_points: int = 20
    x0: Optional[list[float]] = None
    n_vars: int = 2


class IntegerProgramProblem(BaseModel):
    objective: list[float]
    constraints: list[LPConstraint]
    sense: OptimizationSense = OptimizationSense.MAXIMIZE
    integer_vars: Optional[list[int]] = None
    max_nodes: int = 10000


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    context: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Pydantic models — outputs
# ---------------------------------------------------------------------------

class LPResult(BaseModel):
    status: SolverStatus
    objective_value: Optional[float] = None
    solution: Optional[list[float]] = None
    variable_names: Optional[list[str]] = None
    shadow_prices: Optional[list[float]] = None
    reduced_costs: Optional[list[float]] = None
    iterations: int = 0
    sensitivity: Optional[dict[str, Any]] = None
    elapsed_ms: float = 0.0
    determinism_hash: str = ""


class OptimizationResult(BaseModel):
    status: SolverStatus
    x_optimal: Optional[list[float]] = None
    f_optimal: Optional[float] = None
    iterations: int = 0
    gradient_norm: Optional[float] = None
    converged: bool = False
    elapsed_ms: float = 0.0
    determinism_hash: str = ""
    method: str = ""
    trajectory: Optional[list[list[float]]] = None


class PortfolioResult(BaseModel):
    status: SolverStatus
    weights: Optional[list[float]] = None
    expected_return: Optional[float] = None
    volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    efficient_frontier: Optional[list[dict[str, float]]] = None
    min_variance_weights: Optional[list[float]] = None
    tangency_weights: Optional[list[float]] = None
    elapsed_ms: float = 0.0
    determinism_hash: str = ""


class ParetoPoint(BaseModel):
    x: list[float]
    objectives: list[float]


class MultiObjectiveResult(BaseModel):
    status: SolverStatus
    pareto_points: list[ParetoPoint] = []
    method: str = ""
    elapsed_ms: float = 0.0
    determinism_hash: str = ""


class IntegerResult(BaseModel):
    status: SolverStatus
    objective_value: Optional[float] = None
    solution: Optional[list[float]] = None
    nodes_explored: int = 0
    elapsed_ms: float = 0.0
    determinism_hash: str = ""


class EngineResponse(BaseModel):
    engine_id: str = ENGINE_ID
    version: str = ENGINE_VERSION
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    answer: str = ""
    doctrine_hits: list[str] = Field(default_factory=list)
    authority_chain: list[str] = Field(default_factory=list)
    reasoning_trace: list[str] = Field(default_factory=list)
    determinism_hash: str = ""
    elapsed_ms: float = 0.0
    fragility_score: float = 0.0
    disclosure_caveat: str = ""


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    version: str = ENGINE_VERSION
    status: str = "healthy"
    tier: int = ENGINE_TIER
    domain: str = ENGINE_DOMAIN
    port: int = ENGINE_PORT
    mode: str = ENGINE_MODE
    authority: float = ENGINE_AUTH
    uptime_seconds: float = 0.0
    queries_served: int = 0
    doctrines_loaded: int = 0
    semantic_terms: int = 0
    coverage_domains: int = 0
    components_active: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# TIE Component 16: Determinism hash
# ---------------------------------------------------------------------------

def determinism_hash(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# TIE Component 15: Audit trail
# ---------------------------------------------------------------------------

def audit_log(event: str, payload: dict[str, Any]) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "engine": ENGINE_ID,
        "event": event,
        **payload,
    }
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.warning("Audit write failed: {}", exc)


# ---------------------------------------------------------------------------
# TIE Component 11: Metrics collector
# ---------------------------------------------------------------------------

class MetricsCollector:
    def __init__(self) -> None:
        self.queries_total: int = 0
        self.errors_total: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.latency_sum_ms: float = 0.0
        self.latency_max_ms: float = 0.0
        self.method_counts: dict[str, int] = {}
        self._start = time.time()

    def record_query(self, method: str, latency_ms: float, error: bool = False) -> None:
        self.queries_total += 1
        self.latency_sum_ms += latency_ms
        if latency_ms > self.latency_max_ms:
            self.latency_max_ms = latency_ms
        self.method_counts[method] = self.method_counts.get(method, 0) + 1
        if error:
            self.errors_total += 1

    def record_cache(self, hit: bool) -> None:
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    @property
    def uptime(self) -> float:
        return time.time() - self._start

    @property
    def avg_latency(self) -> float:
        if self.queries_total == 0:
            return 0.0
        return self.latency_sum_ms / self.queries_total

    @property
    def error_rate(self) -> float:
        if self.queries_total == 0:
            return 0.0
        return self.errors_total / self.queries_total

    def snapshot(self) -> dict[str, Any]:
        return {
            "queries_total": self.queries_total,
            "errors_total": self.errors_total,
            "error_rate": round(self.error_rate, 4),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": round(
                self.cache_hits / max(1, self.cache_hits + self.cache_misses), 4
            ),
            "avg_latency_ms": round(self.avg_latency, 2),
            "max_latency_ms": round(self.latency_max_ms, 2),
            "uptime_s": round(self.uptime, 1),
            "method_counts": dict(self.method_counts),
        }


METRICS = MetricsCollector()

# ---------------------------------------------------------------------------
# TIE Component 8: Telemetry
# ---------------------------------------------------------------------------

class TelemetrySpan:
    def __init__(self, operation: str) -> None:
        self.operation = operation
        self.trace_id = uuid.uuid4().hex[:12]
        self.start_time = time.perf_counter()
        self.end_time: Optional[float] = None
        self.error: Optional[str] = None
        self.metadata: dict[str, Any] = {}

    def finish(self, error: Optional[str] = None) -> float:
        self.end_time = time.perf_counter()
        self.error = error
        elapsed = (self.end_time - self.start_time) * 1000
        logger.debug(
            "[telemetry] {} trace={} elapsed={:.1f}ms err={}",
            self.operation, self.trace_id, elapsed, error,
        )
        return elapsed


# ---------------------------------------------------------------------------
# TIE Component 9: Drift watcher
# ---------------------------------------------------------------------------

class DriftWatcher:
    def __init__(self) -> None:
        self._observations: list[dict[str, Any]] = []

    def observe(self, topic: str, confidence: str, result_hash: str) -> None:
        self._observations.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "topic": topic,
            "confidence": confidence,
            "hash": result_hash,
        })
        if len(self._observations) > 10000:
            self._observations = self._observations[-5000:]

    def check_drift(self, topic: str) -> dict[str, Any]:
        topic_obs = [o for o in self._observations if o["topic"] == topic]
        if len(topic_obs) < 2:
            return {"drifted": False, "observations": len(topic_obs)}
        hashes = [o["hash"] for o in topic_obs[-20:]]
        unique = len(set(hashes))
        return {
            "drifted": unique > 1,
            "unique_hashes": unique,
            "observations": len(topic_obs),
            "latest": topic_obs[-1],
        }

    def report(self) -> dict[str, Any]:
        topics = set(o["topic"] for o in self._observations)
        return {
            "total_observations": len(self._observations),
            "topics_tracked": len(topics),
            "per_topic": {t: self.check_drift(t) for t in list(topics)[:50]},
        }


DRIFT = DriftWatcher()

# ---------------------------------------------------------------------------
# TIE Component 10: Coverage map
# ---------------------------------------------------------------------------

class CoverageTracker:
    def __init__(self) -> None:
        self._triggered: dict[str, int] = {}
        self._missed: list[str] = []

    def trigger(self, doctrine: str) -> None:
        self._triggered[doctrine] = self._triggered.get(doctrine, 0) + 1

    def miss(self, query: str) -> None:
        self._missed.append(query)
        if len(self._missed) > 5000:
            self._missed = self._missed[-2500:]

    def report(self) -> dict[str, Any]:
        return {
            "triggered_doctrines": dict(self._triggered),
            "total_triggered": sum(self._triggered.values()),
            "unique_triggered": len(self._triggered),
            "missed_queries": len(self._missed),
            "recent_misses": self._missed[-10:],
        }


COVERAGE = CoverageTracker()


# ===========================================================================
# PURE-PYTHON MATRIX UTILITIES
# ===========================================================================

def mat_zeros(rows: int, cols: int) -> list[list[float]]:
    return [[0.0] * cols for _ in range(rows)]


def mat_identity(n: int) -> list[list[float]]:
    m = mat_zeros(n, n)
    for i in range(n):
        m[i][i] = 1.0
    return m


def mat_copy(m: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in m]


def mat_transpose(m: list[list[float]]) -> list[list[float]]:
    if not m:
        return []
    rows, cols = len(m), len(m[0])
    t = mat_zeros(cols, rows)
    for i in range(rows):
        for j in range(cols):
            t[j][i] = m[i][j]
    return t


def mat_mult(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    if ca != rb:
        raise ValueError(f"mat_mult dimension mismatch: {ra}x{ca} * {rb}x{cb}")
    c = mat_zeros(ra, cb)
    for i in range(ra):
        for j in range(cb):
            s = 0.0
            for k in range(ca):
                s += a[i][k] * b[k][j]
            c[i][j] = s
    return c


def mat_vec_mult(m: list[list[float]], v: list[float]) -> list[float]:
    n = len(m)
    result = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(len(v)):
            s += m[i][j] * v[j]
        result[i] = s
    return result


def vec_dot(a: list[float], b: list[float]) -> float:
    s = 0.0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s


def vec_norm(v: list[float]) -> float:
    return math.sqrt(vec_dot(v, v))


def vec_add(a: list[float], b: list[float]) -> list[float]:
    return [a[i] + b[i] for i in range(len(a))]


def vec_sub(a: list[float], b: list[float]) -> list[float]:
    return [a[i] - b[i] for i in range(len(a))]


def vec_scale(v: list[float], s: float) -> list[float]:
    return [x * s for x in v]


def mat_lu_decompose(a: list[list[float]]) -> tuple[list[list[float]], list[list[float]], list[int]]:
    """LU decomposition with partial pivoting. Returns (L, U, perm)."""
    n = len(a)
    u = mat_copy(a)
    l_mat = mat_identity(n)
    perm = list(range(n))
    for k in range(n):
        max_val = abs(u[k][k])
        max_row = k
        for i in range(k + 1, n):
            if abs(u[i][k]) > max_val:
                max_val = abs(u[i][k])
                max_row = i
        if max_val < FLOAT_TOL:
            continue
        if max_row != k:
            u[k], u[max_row] = u[max_row], u[k]
            perm[k], perm[max_row] = perm[max_row], perm[k]
            for j in range(k):
                l_mat[k][j], l_mat[max_row][j] = l_mat[max_row][j], l_mat[k][j]
        for i in range(k + 1, n):
            factor = u[i][k] / u[k][k]
            l_mat[i][k] = factor
            for j in range(k, n):
                u[i][j] -= factor * u[k][j]
    return l_mat, u, perm


def mat_solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b using LU decomposition with partial pivoting."""
    n = len(a)
    l_mat, u, perm = mat_lu_decompose(a)
    pb = [b[perm[i]] for i in range(n)]
    # Forward substitution: Ly = Pb
    y = [0.0] * n
    for i in range(n):
        s = pb[i]
        for j in range(i):
            s -= l_mat[i][j] * y[j]
        y[i] = s
    # Back substitution: Ux = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= u[i][j] * x[j]
        if abs(u[i][i]) < FLOAT_TOL:
            x[i] = 0.0
        else:
            x[i] = s / u[i][i]
    return x


def mat_inverse(a: list[list[float]]) -> list[list[float]]:
    """Invert a square matrix via LU decomposition."""
    n = len(a)
    inv = mat_zeros(n, n)
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        col = mat_solve(a, e)
        for i in range(n):
            inv[i][j] = col[i]
    return inv


def mat_det(a: list[list[float]]) -> float:
    """Determinant via LU decomposition."""
    n = len(a)
    _, u, perm = mat_lu_decompose(a)
    d = 1.0
    for i in range(n):
        d *= u[i][i]
    swaps = sum(1 for i in range(n) if perm[i] != i)
    if swaps % 2 == 1:
        d = -d
    return d


def mat_eigenvalues_2x2(a: list[list[float]]) -> list[float]:
    """Eigenvalues of a 2x2 matrix (closed form)."""
    tr = a[0][0] + a[1][1]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    disc = tr * tr - 4.0 * det
    if disc < 0:
        return []
    sq = math.sqrt(disc)
    return [(tr + sq) / 2.0, (tr - sq) / 2.0]


def mat_is_positive_definite(a: list[list[float]]) -> bool:
    """Check positive definiteness via Cholesky attempt."""
    n = len(a)
    l_mat = mat_zeros(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j]
            for k in range(j):
                s -= l_mat[i][k] * l_mat[j][k]
            if i == j:
                if s <= FLOAT_TOL:
                    return False
                l_mat[i][j] = math.sqrt(s)
            else:
                if abs(l_mat[j][j]) < FLOAT_TOL:
                    return False
                l_mat[i][j] = s / l_mat[j][j]
    return True


def mat_cholesky(a: list[list[float]]) -> list[list[float]]:
    """Cholesky decomposition: A = L L^T. Returns L."""
    n = len(a)
    l_mat = mat_zeros(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j]
            for k in range(j):
                s -= l_mat[i][k] * l_mat[j][k]
            if i == j:
                if s <= 0:
                    raise ValueError("Matrix not positive definite for Cholesky")
                l_mat[i][j] = math.sqrt(s)
            else:
                l_mat[i][j] = s / l_mat[j][j]
    return l_mat


def mat_solve_cholesky(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b via Cholesky when A is symmetric positive definite."""
    n = len(a)
    l_mat = mat_cholesky(a)
    # Ly = b
    y = [0.0] * n
    for i in range(n):
        s = b[i]
        for j in range(i):
            s -= l_mat[i][j] * y[j]
        y[i] = s / l_mat[i][i]
    # L^T x = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= l_mat[j][i] * x[j]
        x[i] = s / l_mat[i][i]
    return x


# ===========================================================================
# SIMPLEX SOLVER (Tableau-based, two-phase)
# ===========================================================================

class SimplexSolver:
    """Full tableau-based simplex method with two-phase support and sensitivity."""

    def __init__(self, c: list[float], a: list[list[float]],
                 b: list[float], constraint_types: list[ConstraintType],
                 sense: OptimizationSense = OptimizationSense.MAXIMIZE) -> None:
        self.orig_c = c[:]
        self.orig_a = [row[:] for row in a]
        self.orig_b = b[:]
        self.orig_types = constraint_types[:]
        self.sense = sense
        self.n_vars = len(c)
        self.n_constraints = len(a)
        self.status = SolverStatus.ERROR
        self.iterations = 0
        self.solution: list[float] = []
        self.obj_value: float = 0.0
        self.shadow_prices: list[float] = []
        self.reduced_costs: list[float] = []
        self.basis: list[int] = []
        self._tableau: list[list[float]] = []
        self._n_total: int = 0
        self._slack_start: int = 0
        self._surplus_start: int = 0
        self._artificial_start: int = 0
        self._artificial_indices: list[int] = []

    def solve(self) -> None:
        span = TelemetrySpan("simplex_solve")
        try:
            self._build_tableau()
            if self._artificial_indices:
                self._phase_one()
                if self.status == SolverStatus.INFEASIBLE:
                    span.finish()
                    return
                self._prepare_phase_two()
            self._phase_two()
            self._extract_solution()
            self._compute_sensitivity()
        except Exception as exc:
            logger.error("Simplex error: {}", exc)
            self.status = SolverStatus.ERROR
            span.finish(str(exc))
            return
        span.finish()

    def _build_tableau(self) -> None:
        m = self.n_constraints
        n = self.n_vars
        # Count slack, surplus, artificial variables
        n_slack = 0
        n_surplus = 0
        n_artificial = 0
        for ct in self.orig_types:
            if ct == ConstraintType.LEQ:
                n_slack += 1
            elif ct == ConstraintType.GEQ:
                n_surplus += 1
                n_artificial += 1
            else:  # EQ
                n_artificial += 1

        self._slack_start = n
        self._surplus_start = n + n_slack
        self._artificial_start = n + n_slack + n_surplus
        self._n_total = n + n_slack + n_surplus + n_artificial
        total_cols = self._n_total + 1  # +1 for RHS

        # Build tableau: m rows + 1 objective row
        self._tableau = mat_zeros(m + 1, total_cols)
        self._artificial_indices = []
        self.basis = [0] * m

        slack_idx = self._slack_start
        surplus_idx = self._surplus_start
        art_idx = self._artificial_start

        for i in range(m):
            # Ensure RHS is non-negative
            sign = 1.0
            if self.orig_b[i] < 0:
                sign = -1.0
                # Flip constraint type
                if self.orig_types[i] == ConstraintType.LEQ:
                    self.orig_types[i] = ConstraintType.GEQ
                elif self.orig_types[i] == ConstraintType.GEQ:
                    self.orig_types[i] = ConstraintType.LEQ

            for j in range(n):
                self._tableau[i][j] = sign * self.orig_a[i][j]
            self._tableau[i][-1] = abs(self.orig_b[i])

            ct = self.orig_types[i]
            if ct == ConstraintType.LEQ:
                self._tableau[i][slack_idx] = 1.0
                self.basis[i] = slack_idx
                slack_idx += 1
            elif ct == ConstraintType.GEQ:
                self._tableau[i][surplus_idx] = -1.0
                surplus_idx += 1
                self._tableau[i][art_idx] = 1.0
                self._artificial_indices.append(art_idx)
                self.basis[i] = art_idx
                art_idx += 1
            else:  # EQ
                self._tableau[i][art_idx] = 1.0
                self._artificial_indices.append(art_idx)
                self.basis[i] = art_idx
                art_idx += 1

    def _phase_one(self) -> None:
        """Minimize sum of artificial variables."""
        m = self.n_constraints
        total_cols = len(self._tableau[0])
        # Set phase-1 objective: minimize sum of artificials
        obj_row = [0.0] * total_cols
        for ai in self._artificial_indices:
            obj_row[ai] = 1.0
        # Subtract basis rows for artificial variables already in basis
        for i in range(m):
            if self.basis[i] in self._artificial_indices:
                for j in range(total_cols):
                    obj_row[j] -= self._tableau[i][j]
        self._tableau[m] = obj_row

        self._pivot_loop(max_iter=MAX_SIMPLEX_ITERS)

        # Check if artificials are zero
        rhs_sum = 0.0
        for i in range(m):
            if self.basis[i] in self._artificial_indices:
                rhs_sum += abs(self._tableau[i][-1])
        if rhs_sum > FLOAT_TOL:
            self.status = SolverStatus.INFEASIBLE
            logger.info("LP infeasible (phase-1 residual={:.2e})", rhs_sum)

    def _prepare_phase_two(self) -> None:
        """Set up phase-2 objective and remove artificial columns logically."""
        m = self.n_constraints
        total_cols = len(self._tableau[0])
        # Restore original objective
        c_sign = 1.0 if self.sense == OptimizationSense.MAXIMIZE else -1.0
        obj_row = [0.0] * total_cols
        for j in range(self.n_vars):
            obj_row[j] = -c_sign * self.orig_c[j]
        # Zero out artificial columns with big penalty
        for ai in self._artificial_indices:
            obj_row[ai] = 0.0
        # Subtract basis rows to make basis columns zero in objective
        for i in range(m):
            bv = self.basis[i]
            if abs(obj_row[bv]) > FLOAT_TOL:
                ratio = obj_row[bv]
                for j in range(total_cols):
                    obj_row[j] -= ratio * self._tableau[i][j]
        self._tableau[m] = obj_row

    def _phase_two(self) -> None:
        self._pivot_loop(max_iter=MAX_SIMPLEX_ITERS)

    def _pivot_loop(self, max_iter: int) -> None:
        m = self.n_constraints
        total_cols = len(self._tableau[0])
        for _ in range(max_iter):
            self.iterations += 1
            # Find entering variable (most negative in obj row) - Bland's rule
            pivot_col = -1
            for j in range(self._n_total):
                if j in self._artificial_indices:
                    continue
                if self._tableau[m][j] < -FLOAT_TOL:
                    pivot_col = j
                    break  # Bland's rule: first negative
            if pivot_col == -1:
                self.status = SolverStatus.OPTIMAL
                return

            # Minimum ratio test
            pivot_row = -1
            min_ratio = float("inf")
            for i in range(m):
                if self._tableau[i][pivot_col] > FLOAT_TOL:
                    ratio = self._tableau[i][-1] / self._tableau[i][pivot_col]
                    if ratio < min_ratio - FLOAT_TOL:
                        min_ratio = ratio
                        pivot_row = i
                    elif abs(ratio - min_ratio) < FLOAT_TOL and pivot_row >= 0:
                        # Bland's rule: choose smallest index
                        if self.basis[i] < self.basis[pivot_row]:
                            pivot_row = i

            if pivot_row == -1:
                self.status = SolverStatus.UNBOUNDED
                logger.info("LP unbounded at iteration {}", self.iterations)
                return

            # Pivot
            pivot_val = self._tableau[pivot_row][pivot_col]
            for j in range(total_cols):
                self._tableau[pivot_row][j] /= pivot_val
            for i in range(m + 1):
                if i == pivot_row:
                    continue
                factor = self._tableau[i][pivot_col]
                if abs(factor) > FLOAT_TOL:
                    for j in range(total_cols):
                        self._tableau[i][j] -= factor * self._tableau[pivot_row][j]
            self.basis[pivot_row] = pivot_col

        self.status = SolverStatus.MAX_ITER
        logger.warning("Simplex hit max iterations ({})", max_iter)

    def _extract_solution(self) -> None:
        if self.status not in (SolverStatus.OPTIMAL,):
            return
        m = self.n_constraints
        self.solution = [0.0] * self.n_vars
        for i in range(m):
            bv = self.basis[i]
            if bv < self.n_vars:
                self.solution[bv] = self._tableau[i][-1]
        c_sign = 1.0 if self.sense == OptimizationSense.MAXIMIZE else -1.0
        self.obj_value = -c_sign * self._tableau[m][-1]

    def _compute_sensitivity(self) -> None:
        if self.status != SolverStatus.OPTIMAL:
            return
        m = self.n_constraints
        c_sign = 1.0 if self.sense == OptimizationSense.MAXIMIZE else -1.0
        # Shadow prices: dual variables from objective row of slack columns
        self.shadow_prices = []
        for i in range(m):
            slack_col = self._slack_start + i
            if slack_col < self._n_total:
                self.shadow_prices.append(-c_sign * self._tableau[m][slack_col])
            else:
                self.shadow_prices.append(0.0)
        # Reduced costs for original variables
        self.reduced_costs = []
        for j in range(self.n_vars):
            self.reduced_costs.append(-c_sign * self._tableau[m][j])


# ===========================================================================
# GRADIENT DESCENT SOLVER
# ===========================================================================

def _safe_eval_function(expr: str, x: list[float]) -> float:
    """Evaluate a math expression with x as variable vector."""
    ns: dict[str, Any] = {"math": math, "sqrt": math.sqrt, "exp": math.exp,
                           "log": math.log, "sin": math.sin, "cos": math.cos,
                           "tan": math.tan, "abs": abs, "pi": math.pi, "e": math.e}
    for i, val in enumerate(x):
        ns[f"x{i}"] = val
        ns[f"x_{i}"] = val
    if len(x) >= 1:
        ns["x"] = x[0]
    if len(x) >= 2:
        ns["y"] = x[1]
    if len(x) >= 3:
        ns["z"] = x[2]
    try:
        return float(eval(expr, {"__builtins__": {}}, ns))  # noqa: S307
    except Exception as exc:
        raise ValueError(f"Cannot evaluate function '{expr}': {exc}") from exc


def _numerical_gradient(expr: str, x: list[float], h: float = 1e-7) -> list[float]:
    """Central difference gradient."""
    n = len(x)
    grad = [0.0] * n
    for i in range(n):
        xp = x[:]
        xm = x[:]
        xp[i] += h
        xm[i] -= h
        fp = _safe_eval_function(expr, xp)
        fm = _safe_eval_function(expr, xm)
        grad[i] = (fp - fm) / (2.0 * h)
    return grad


def _numerical_hessian(expr: str, x: list[float], h: float = 1e-5) -> list[list[float]]:
    """Central difference Hessian."""
    n = len(x)
    hess = mat_zeros(n, n)
    f0 = _safe_eval_function(expr, x)
    for i in range(n):
        for j in range(i, n):
            xpp = x[:]
            xpm = x[:]
            xmp = x[:]
            xmm = x[:]
            xpp[i] += h
            xpp[j] += h
            xpm[i] += h
            xpm[j] -= h
            xmp[i] -= h
            xmp[j] += h
            xmm[i] -= h
            xmm[j] -= h
            fpp = _safe_eval_function(expr, xpp)
            fpm = _safe_eval_function(expr, xpm)
            fmp = _safe_eval_function(expr, xmp)
            fmm = _safe_eval_function(expr, xmm)
            hess[i][j] = (fpp - fpm - fmp + fmm) / (4.0 * h * h)
            hess[j][i] = hess[i][j]
    return hess


def gradient_descent_solve(
    expr: str, x0: list[float], lr: float = 0.01,
    max_iter: int = 10000, tol: float = 1e-8,
) -> OptimizationResult:
    span = TelemetrySpan("gradient_descent")
    x = x0[:]
    trajectory: list[list[float]] = [x[:]]
    iters = 0
    for k in range(max_iter):
        iters = k + 1
        grad = _numerical_gradient(expr, x)
        gnorm = vec_norm(grad)
        if gnorm < tol:
            elapsed = span.finish()
            return OptimizationResult(
                status=SolverStatus.OPTIMAL, x_optimal=x,
                f_optimal=_safe_eval_function(expr, x),
                iterations=iters, gradient_norm=gnorm, converged=True,
                elapsed_ms=elapsed, method="gradient_descent",
                determinism_hash=determinism_hash(x),
                trajectory=trajectory[-20:],
            )
        x = vec_sub(x, vec_scale(grad, lr))
        if k % 100 == 0:
            trajectory.append(x[:])
    f_val = _safe_eval_function(expr, x)
    gnorm = vec_norm(_numerical_gradient(expr, x))
    elapsed = span.finish()
    return OptimizationResult(
        status=SolverStatus.MAX_ITER, x_optimal=x, f_optimal=f_val,
        iterations=iters, gradient_norm=gnorm, converged=False,
        elapsed_ms=elapsed, method="gradient_descent",
        determinism_hash=determinism_hash(x),
        trajectory=trajectory[-20:],
    )


# ===========================================================================
# NEWTON'S METHOD SOLVER
# ===========================================================================

def newton_optimize(
    expr: str, x0: list[float], max_iter: int = 500, tol: float = 1e-10,
) -> OptimizationResult:
    span = TelemetrySpan("newton_optimize")
    x = x0[:]
    trajectory: list[list[float]] = [x[:]]
    iters = 0
    for k in range(max_iter):
        iters = k + 1
        grad = _numerical_gradient(expr, x)
        gnorm = vec_norm(grad)
        if gnorm < tol:
            elapsed = span.finish()
            return OptimizationResult(
                status=SolverStatus.OPTIMAL, x_optimal=x,
                f_optimal=_safe_eval_function(expr, x),
                iterations=iters, gradient_norm=gnorm, converged=True,
                elapsed_ms=elapsed, method="newton",
                determinism_hash=determinism_hash(x),
                trajectory=trajectory[-20:],
            )
        hess = _numerical_hessian(expr, x)
        try:
            step = mat_solve(hess, grad)
        except Exception:
            # Hessian singular — fall back to gradient step
            step = vec_scale(grad, 0.01)
        # Damped Newton with backtracking
        alpha = 1.0
        f_curr = _safe_eval_function(expr, x)
        for _ in range(30):
            x_new = vec_sub(x, vec_scale(step, alpha))
            f_new = _safe_eval_function(expr, x_new)
            if f_new < f_curr - 1e-4 * alpha * vec_dot(grad, step):
                break
            alpha *= 0.5
        else:
            x_new = vec_sub(x, vec_scale(step, alpha))
        x = x_new
        trajectory.append(x[:])
    f_val = _safe_eval_function(expr, x)
    gnorm = vec_norm(_numerical_gradient(expr, x))
    elapsed = span.finish()
    return OptimizationResult(
        status=SolverStatus.MAX_ITER, x_optimal=x, f_optimal=f_val,
        iterations=iters, gradient_norm=gnorm, converged=False,
        elapsed_ms=elapsed, method="newton",
        determinism_hash=determinism_hash(x),
        trajectory=trajectory[-20:],
    )


# ===========================================================================
# CONJUGATE GRADIENT SOLVER (nonlinear, Polak-Ribiere)
# ===========================================================================

def conjugate_gradient_solve(
    expr: str, x0: list[float], max_iter: int = 10000, tol: float = 1e-8,
) -> OptimizationResult:
    span = TelemetrySpan("conjugate_gradient")
    x = x0[:]
    n = len(x)
    grad = _numerical_gradient(expr, x)
    d = vec_scale(grad, -1.0)
    gnorm = vec_norm(grad)
    trajectory: list[list[float]] = [x[:]]
    iters = 0
    for k in range(max_iter):
        iters = k + 1
        if gnorm < tol:
            elapsed = span.finish()
            return OptimizationResult(
                status=SolverStatus.OPTIMAL, x_optimal=x,
                f_optimal=_safe_eval_function(expr, x),
                iterations=iters, gradient_norm=gnorm, converged=True,
                elapsed_ms=elapsed, method="conjugate_gradient",
                determinism_hash=determinism_hash(x),
                trajectory=trajectory[-20:],
            )
        # Line search (backtracking Armijo)
        alpha = 1.0
        f_curr = _safe_eval_function(expr, x)
        dir_deriv = vec_dot(grad, d)
        if dir_deriv > 0:
            d = vec_scale(grad, -1.0)
            dir_deriv = vec_dot(grad, d)
        for _ in range(40):
            x_new = vec_add(x, vec_scale(d, alpha))
            f_new = _safe_eval_function(expr, x_new)
            if f_new <= f_curr + 1e-4 * alpha * dir_deriv:
                break
            alpha *= 0.5
        x = vec_add(x, vec_scale(d, alpha))
        grad_new = _numerical_gradient(expr, x)
        gnorm_new = vec_norm(grad_new)
        # Polak-Ribiere beta
        gg = vec_dot(grad_new, grad_new)
        dg = vec_dot(grad_new, grad)
        gg_old = vec_dot(grad, grad)
        if gg_old < FLOAT_TOL:
            beta = 0.0
        else:
            beta = max(0.0, (gg - dg) / gg_old)  # PR+
        d = vec_add(vec_scale(grad_new, -1.0), vec_scale(d, beta))
        grad = grad_new
        gnorm = gnorm_new
        # Restart every n iterations
        if (k + 1) % n == 0:
            d = vec_scale(grad, -1.0)
        if k % 100 == 0:
            trajectory.append(x[:])
    f_val = _safe_eval_function(expr, x)
    elapsed = span.finish()
    return OptimizationResult(
        status=SolverStatus.MAX_ITER, x_optimal=x, f_optimal=f_val,
        iterations=iters, gradient_norm=gnorm, converged=False,
        elapsed_ms=elapsed, method="conjugate_gradient",
        determinism_hash=determinism_hash(x),
        trajectory=trajectory[-20:],
    )


# ===========================================================================
# GOLDEN SECTION SEARCH (1D)
# ===========================================================================

def golden_section_minimize(
    expr: str, a: float, b: float, tol: float = 1e-8, max_iter: int = 500,
) -> OptimizationResult:
    span = TelemetrySpan("golden_section")
    phi = (math.sqrt(5.0) - 1.0) / 2.0  # ~0.618
    x1 = a + (1 - phi) * (b - a)
    x2 = a + phi * (b - a)
    f1 = _safe_eval_function(expr, [x1])
    f2 = _safe_eval_function(expr, [x2])
    iters = 0
    for k in range(max_iter):
        iters = k + 1
        if abs(b - a) < tol:
            break
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (1 - phi) * (b - a)
            f1 = _safe_eval_function(expr, [x1])
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + phi * (b - a)
            f2 = _safe_eval_function(expr, [x2])
    x_opt = (a + b) / 2.0
    f_opt = _safe_eval_function(expr, [x_opt])
    elapsed = span.finish()
    return OptimizationResult(
        status=SolverStatus.OPTIMAL, x_optimal=[x_opt], f_optimal=f_opt,
        iterations=iters, converged=abs(b - a) < tol,
        elapsed_ms=elapsed, method="golden_section",
        determinism_hash=determinism_hash([x_opt]),
    )


# ===========================================================================
# LAGRANGE MULTIPLIER SOLVER (equality constraints)
# ===========================================================================

def lagrange_solve(
    obj_expr: str, constraint_exprs: list[str], x0: list[float],
    tol: float = 1e-8, max_iter: int = 1000,
) -> OptimizationResult:
    """Solve min f(x) s.t. g_i(x)=0 via augmented Lagrangian method."""
    span = TelemetrySpan("lagrange_solve")
    n = len(x0)
    m = len(constraint_exprs)
    x = x0[:]
    lam = [0.0] * m
    mu = 10.0  # penalty parameter
    iters = 0
    for outer in range(max_iter):
        iters = outer + 1
        # Build augmented Lagrangian: f + sum lambda_i g_i + (mu/2) sum g_i^2
        def aug_lag_val(xv: list[float]) -> float:
            fv = _safe_eval_function(obj_expr, xv)
            for j in range(m):
                gj = _safe_eval_function(constraint_exprs[j], xv)
                fv += lam[j] * gj + (mu / 2.0) * gj * gj
            return fv

        # Minimize augmented Lagrangian with gradient descent
        for inner in range(200):
            grad = [0.0] * n
            h = 1e-7
            f0 = aug_lag_val(x)
            for i in range(n):
                xp = x[:]
                xp[i] += h
                grad[i] = (aug_lag_val(xp) - f0) / h
            gnorm = vec_norm(grad)
            if gnorm < tol * 0.1:
                break
            lr = min(0.01, 1.0 / (mu + 1.0))
            x = vec_sub(x, vec_scale(grad, lr))

        # Update multipliers
        max_viol = 0.0
        for j in range(m):
            gj = _safe_eval_function(constraint_exprs[j], x)
            lam[j] += mu * gj
            max_viol = max(max_viol, abs(gj))
        if max_viol < tol:
            f_opt = _safe_eval_function(obj_expr, x)
            elapsed = span.finish()
            return OptimizationResult(
                status=SolverStatus.OPTIMAL, x_optimal=x, f_optimal=f_opt,
                iterations=iters, converged=True,
                elapsed_ms=elapsed, method="augmented_lagrangian",
                determinism_hash=determinism_hash(x),
            )
        mu *= 2.0  # increase penalty

    f_opt = _safe_eval_function(obj_expr, x)
    elapsed = span.finish()
    return OptimizationResult(
        status=SolverStatus.MAX_ITER, x_optimal=x, f_optimal=f_opt,
        iterations=iters, converged=False,
        elapsed_ms=elapsed, method="augmented_lagrangian",
        determinism_hash=determinism_hash(x),
    )


# ===========================================================================
# PORTFOLIO OPTIMIZATION (Markowitz mean-variance)
# ===========================================================================

class PortfolioSolver:
    """Mean-variance portfolio optimization with efficient frontier."""

    def __init__(self, mu: list[float], sigma: list[list[float]],
                 rf: float = 0.0, allow_short: bool = False) -> None:
        self.n = len(mu)
        self.mu = mu[:]
        self.sigma = [row[:] for row in sigma]
        self.rf = rf
        self.allow_short = allow_short

    def minimum_variance(self) -> tuple[list[float], float, float]:
        """Compute the global minimum variance portfolio (analytical)."""
        n = self.n
        sigma_inv = mat_inverse(self.sigma)
        ones = [1.0] * n
        sig_inv_ones = mat_vec_mult(sigma_inv, ones)
        denom = vec_dot(ones, sig_inv_ones)
        if abs(denom) < FLOAT_TOL:
            raise ValueError("Singular covariance — cannot compute min variance")
        w = vec_scale(sig_inv_ones, 1.0 / denom)
        if not self.allow_short:
            w = self._project_simplex(w)
        ret = vec_dot(w, self.mu)
        var = 0.0
        for i in range(n):
            for j in range(n):
                var += w[i] * self.sigma[i][j] * w[j]
        vol = math.sqrt(max(0.0, var))
        return w, ret, vol

    def optimal_for_target(self, target_ret: float) -> tuple[list[float], float, float]:
        """Min variance portfolio achieving target_ret (analytical with 2 Lagrange multipliers)."""
        n = self.n
        sigma_inv = mat_inverse(self.sigma)
        ones = [1.0] * n
        # Compute key scalars
        a_val = vec_dot(ones, mat_vec_mult(sigma_inv, ones))
        b_val = vec_dot(self.mu, mat_vec_mult(sigma_inv, ones))
        c_val = vec_dot(self.mu, mat_vec_mult(sigma_inv, self.mu))
        det = a_val * c_val - b_val * b_val
        if abs(det) < FLOAT_TOL:
            return self.minimum_variance()
        lam1 = (c_val - b_val * target_ret) / det
        lam2 = (a_val * target_ret - b_val) / det
        # w = sigma_inv (lam1 * ones + lam2 * mu)
        rhs = vec_add(vec_scale(ones, lam1), vec_scale(self.mu, lam2))
        w = mat_vec_mult(sigma_inv, rhs)
        if not self.allow_short:
            w = self._project_simplex(w)
        ret = vec_dot(w, self.mu)
        var = 0.0
        for i in range(n):
            for j in range(n):
                var += w[i] * self.sigma[i][j] * w[j]
        vol = math.sqrt(max(0.0, var))
        return w, ret, vol

    def tangency_portfolio(self) -> tuple[list[float], float, float, float]:
        """Max Sharpe ratio portfolio (analytical)."""
        n = self.n
        excess = [self.mu[i] - self.rf for i in range(n)]
        sigma_inv = mat_inverse(self.sigma)
        sig_inv_exc = mat_vec_mult(sigma_inv, excess)
        denom = sum(sig_inv_exc)
        if abs(denom) < FLOAT_TOL:
            w, r, v = self.minimum_variance()
            sr = (r - self.rf) / max(v, FLOAT_TOL)
            return w, r, v, sr
        w = vec_scale(sig_inv_exc, 1.0 / denom)
        if not self.allow_short:
            w = self._project_simplex(w)
        ret = vec_dot(w, self.mu)
        var = 0.0
        for i in range(n):
            for j in range(n):
                var += w[i] * self.sigma[i][j] * w[j]
        vol = math.sqrt(max(0.0, var))
        sharpe = (ret - self.rf) / max(vol, FLOAT_TOL)
        return w, ret, vol, sharpe

    def efficient_frontier(self, num_points: int = 50) -> list[dict[str, float]]:
        """Trace the efficient frontier from min-var to max-return."""
        _, min_ret, _ = self.minimum_variance()
        max_ret = max(self.mu)
        if max_ret <= min_ret:
            max_ret = min_ret + 1.0
        frontier: list[dict[str, float]] = []
        for i in range(num_points):
            t = i / max(1, num_points - 1)
            target = min_ret + t * (max_ret - min_ret)
            w, ret, vol = self.optimal_for_target(target)
            sharpe = (ret - self.rf) / max(vol, FLOAT_TOL)
            frontier.append({
                "target_return": round(target, 8),
                "actual_return": round(ret, 8),
                "volatility": round(vol, 8),
                "sharpe_ratio": round(sharpe, 6),
            })
        return frontier

    @staticmethod
    def _project_simplex(w: list[float]) -> list[float]:
        """Project weights onto the unit simplex (no short selling)."""
        n = len(w)
        u = sorted(range(n), key=lambda i: w[i], reverse=True)
        cumsum = 0.0
        rho = 0
        for j in range(n):
            cumsum += w[u[j]]
            if w[u[j]] - (cumsum - 1.0) / (j + 1) > 0:
                rho = j + 1
        cumsum = sum(w[u[j]] for j in range(rho))
        theta = (cumsum - 1.0) / rho
        result = [max(0.0, w[i] - theta) for i in range(n)]
        s = sum(result)
        if s > FLOAT_TOL:
            result = [r / s for r in result]
        return result


# ===========================================================================
# BRANCH AND BOUND (Integer Programming)
# ===========================================================================

def branch_and_bound_solve(
    c: list[float], a: list[list[float]], b: list[float],
    constraint_types: list[ConstraintType],
    sense: OptimizationSense, integer_vars: list[int],
    max_nodes: int = 10000,
) -> IntegerResult:
    """Branch and bound for mixed-integer linear programming."""
    span = TelemetrySpan("branch_and_bound")
    n = len(c)
    best_obj = float("-inf") if sense == OptimizationSense.MAXIMIZE else float("inf")
    best_sol: Optional[list[float]] = None
    nodes_explored = 0

    # Node: (extra_constraints_leq, extra_constraints_geq)
    # Each is list of (var_index, bound)
    stack: list[tuple[list[tuple[int, float]], list[tuple[int, float]]]] = [([], [])]

    while stack and nodes_explored < max_nodes:
        nodes_explored += 1
        leq_bounds, geq_bounds = stack.pop()

        # Build augmented LP
        a_aug = [row[:] for row in a]
        b_aug = b[:]
        ct_aug = constraint_types[:]
        for var_idx, bnd in leq_bounds:
            row = [0.0] * n
            row[var_idx] = 1.0
            a_aug.append(row)
            b_aug.append(bnd)
            ct_aug.append(ConstraintType.LEQ)
        for var_idx, bnd in geq_bounds:
            row = [0.0] * n
            row[var_idx] = 1.0
            a_aug.append(row)
            b_aug.append(bnd)
            ct_aug.append(ConstraintType.GEQ)

        solver = SimplexSolver(c, a_aug, b_aug, ct_aug, sense)
        solver.solve()
        if solver.status != SolverStatus.OPTIMAL:
            continue  # Pruned (infeasible)

        # Bound check
        if sense == OptimizationSense.MAXIMIZE:
            if solver.obj_value <= best_obj + FLOAT_TOL:
                continue  # Pruned (bound)
        else:
            if solver.obj_value >= best_obj - FLOAT_TOL:
                continue

        # Check integrality
        all_integer = True
        branch_var = -1
        max_frac = 0.0
        for vi in integer_vars:
            if vi < len(solver.solution):
                frac = solver.solution[vi] - math.floor(solver.solution[vi])
                if frac > FLOAT_TOL and frac < 1.0 - FLOAT_TOL:
                    all_integer = False
                    if abs(frac - 0.5) < abs(max_frac - 0.5) or branch_var == -1:
                        max_frac = frac
                        branch_var = vi

        if all_integer:
            # Integer feasible — update incumbent
            if sense == OptimizationSense.MAXIMIZE:
                if solver.obj_value > best_obj:
                    best_obj = solver.obj_value
                    best_sol = solver.solution[:]
            else:
                if solver.obj_value < best_obj:
                    best_obj = solver.obj_value
                    best_sol = solver.solution[:]
            continue

        # Branch
        val = solver.solution[branch_var]
        floor_val = math.floor(val)
        ceil_val = math.ceil(val)
        # Left: x_j <= floor
        stack.append((leq_bounds + [(branch_var, floor_val)], geq_bounds[:]))
        # Right: x_j >= ceil
        stack.append((leq_bounds[:], geq_bounds + [(branch_var, ceil_val)]))

    elapsed = span.finish()
    if best_sol is not None:
        return IntegerResult(
            status=SolverStatus.OPTIMAL, objective_value=best_obj,
            solution=best_sol, nodes_explored=nodes_explored,
            elapsed_ms=elapsed, determinism_hash=determinism_hash(best_sol),
        )
    return IntegerResult(
        status=SolverStatus.INFEASIBLE, nodes_explored=nodes_explored,
        elapsed_ms=elapsed, determinism_hash="",
    )


# ===========================================================================
# MULTI-OBJECTIVE OPTIMIZATION
# ===========================================================================

def weighted_sum_multi_objective(
    obj_exprs: list[str], weights: list[float], x0: list[float],
    max_iter: int = 5000, tol: float = 1e-7,
) -> ParetoPoint:
    """Weighted-sum scalarization of multi-objective problem."""
    k = len(obj_exprs)
    combined = " + ".join(f"({weights[i]}) * ({obj_exprs[i]})" for i in range(k))
    result = gradient_descent_solve(combined, x0, lr=0.01, max_iter=max_iter, tol=tol)
    if result.x_optimal is None:
        return ParetoPoint(x=x0, objectives=[0.0] * k)
    obj_vals = [_safe_eval_function(e, result.x_optimal) for e in obj_exprs]
    return ParetoPoint(x=result.x_optimal, objectives=obj_vals)


def epsilon_constraint_multi_objective(
    obj_exprs: list[str], epsilon_levels: list[float],
    x0: list[float], max_iter: int = 5000, tol: float = 1e-7,
) -> ParetoPoint:
    """Epsilon-constraint: min f1 s.t. f_j <= eps_j for j>=2."""
    k = len(obj_exprs)
    # Build penalty for constraint violations
    penalty_terms: list[str] = []
    for j in range(1, k):
        eps = epsilon_levels[j - 1] if j - 1 < len(epsilon_levels) else 0.0
        penalty_terms.append(f"max(0, ({obj_exprs[j]}) - ({eps}))**2")
    mu = 1000.0
    combined = f"({obj_exprs[0]})"
    if penalty_terms:
        combined += f" + {mu} * (" + " + ".join(penalty_terms) + ")"
    result = gradient_descent_solve(combined, x0, lr=0.001, max_iter=max_iter, tol=tol)
    if result.x_optimal is None:
        return ParetoPoint(x=x0, objectives=[0.0] * k)
    obj_vals = [_safe_eval_function(e, result.x_optimal) for e in obj_exprs]
    return ParetoPoint(x=result.x_optimal, objectives=obj_vals)


def approximate_pareto_front(
    obj_exprs: list[str], x0: list[float], num_points: int = 20,
    method: str = "weighted_sum",
) -> list[ParetoPoint]:
    """Approximate Pareto front by varying weights or epsilon."""
    k = len(obj_exprs)
    points: list[ParetoPoint] = []
    if method == "weighted_sum" and k == 2:
        for i in range(num_points):
            w1 = i / max(1, num_points - 1)
            w2 = 1.0 - w1
            pt = weighted_sum_multi_objective(obj_exprs, [w1, w2], x0)
            points.append(pt)
    elif method == "epsilon_constraint" and k >= 2:
        # Vary epsilon for objectives 2..k
        obj2_range = [
            _safe_eval_function(obj_exprs[1], x0) * (0.5 + i / max(1, num_points - 1))
            for i in range(num_points)
        ]
        for eps in obj2_range:
            pt = epsilon_constraint_multi_objective(
                obj_exprs, [eps] * (k - 1), x0,
            )
            points.append(pt)
    else:
        # General: random weight sampling
        import random
        rng = random.Random(42)
        for _ in range(num_points):
            raw = [rng.random() for _ in range(k)]
            s = sum(raw)
            ws = [r / s for r in raw]
            pt = weighted_sum_multi_objective(obj_exprs, ws, x0)
            points.append(pt)
    # Filter dominated points
    non_dominated: list[ParetoPoint] = []
    for p in points:
        dominated = False
        for q in points:
            if q is p:
                continue
            if all(q.objectives[i] <= p.objectives[i] for i in range(k)) and \
               any(q.objectives[i] < p.objectives[i] for i in range(k)):
                dominated = True
                break
        if not dominated:
            non_dominated.append(p)
    return non_dominated


# ===========================================================================
# TIE Component 3: Doctrine cache loader
# ===========================================================================

def _load_json(filename: str) -> Any:
    path = ENGINE_DIR / filename
    if path.exists():
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


DOCTRINE_CACHE: dict[str, Any] = {}
SEMANTIC_DICT: dict[str, str] = {}
COVERAGE_MAP: dict[str, Any] = {}


def load_knowledge_base() -> None:
    global DOCTRINE_CACHE, SEMANTIC_DICT, COVERAGE_MAP
    dc = _load_json("doctrine_cache.json")
    if "doctrines" in dc:
        for d in dc["doctrines"]:
            DOCTRINE_CACHE[d["topic"]] = d
    sd = _load_json("semantic_dict.json")
    if "normalization_rules" in sd:
        SEMANTIC_DICT.update(sd["normalization_rules"])
    COVERAGE_MAP = _load_json("coverage_map.json")
    logger.info(
        "Knowledge loaded: {} doctrines, {} semantic terms",
        len(DOCTRINE_CACHE), len(SEMANTIC_DICT),
    )


# ===========================================================================
# TIE Component 6: Semantic normalization
# ===========================================================================

def normalize_query(query: str) -> list[str]:
    tokens = query.lower().replace(",", " ").replace(".", " ").split()
    normalized: list[str] = []
    for tok in tokens:
        if tok in SEMANTIC_DICT:
            normalized.append(SEMANTIC_DICT[tok])
        else:
            normalized.append(tok)
    # Also check multi-word phrases
    q_lower = query.lower()
    for phrase, norm in SEMANTIC_DICT.items():
        if phrase.lower() in q_lower:
            if norm not in normalized:
                normalized.append(norm)
    return normalized


# ===========================================================================
# TIE Component 7: Vector search (keyword-based fallback)
# ===========================================================================

def vector_search(query: str, top_k: int = 5) -> list[tuple[str, float]]:
    tokens = set(normalize_query(query))
    scores: list[tuple[str, float]] = []
    for topic, doc in DOCTRINE_CACHE.items():
        kw_set = set(k.lower() for k in doc.get("keywords", []))
        overlap = len(tokens & kw_set)
        topic_tokens = set(topic.lower().replace("_", " ").split())
        overlap += len(tokens & topic_tokens) * 2
        if overlap > 0:
            scores.append((topic, float(overlap)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


# ===========================================================================
# TIE Component 4: Authority hardening
# ===========================================================================

AUTHORITY_WEIGHTS = {
    "primary_textbook": 1.0,
    "peer_reviewed": 0.95,
    "established_algorithm": 0.90,
    "practitioner_consensus": 0.75,
    "heuristic": 0.50,
}


def authority_chain(doctrine: dict[str, Any]) -> list[str]:
    return doctrine.get("primary_authority", [])


# ===========================================================================
# TIE Component 5: Confidence stratification
# ===========================================================================

def classify_confidence(doctrine: dict[str, Any], query: str) -> ConfidenceLevel:
    conf = doctrine.get("confidence", "DEFENSIBLE")
    if conf in ("DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"):
        return ConfidenceLevel(conf)
    return ConfidenceLevel.DEFENSIBLE


# ===========================================================================
# TIE Component 13: Zoned analysis
# ===========================================================================

ZONE_PREFIXES = {
    PositionZone.PLANNING: "For planning purposes: ",
    PositionZone.REPORTING: "For reporting: ",
    PositionZone.AUDIT: "For audit documentation: ",
}


# ===========================================================================
# TIE Component 14: Fact fragility scoring
# ===========================================================================

def fragility_score(doctrine: dict[str, Any]) -> float:
    conf = doctrine.get("confidence", "DEFENSIBLE")
    base = {"DEFENSIBLE": 0.1, "AGGRESSIVE": 0.4, "DISCLOSURE": 0.6, "HIGH_RISK": 0.85}
    return base.get(conf, 0.5)


# ===========================================================================
# TIE Component 19: Multi-doctrine decomposition
# ===========================================================================

def decompose_query(query: str) -> list[str]:
    tokens = normalize_query(query)
    matched: list[str] = []
    for topic in DOCTRINE_CACHE:
        topic_tokens = set(topic.lower().replace("_", " ").split())
        if topic_tokens & set(tokens):
            matched.append(topic)
    if not matched:
        hits = vector_search(query, top_k=3)
        matched = [h[0] for h in hits]
    return matched


# ===========================================================================
# TIE Component 1 + 20: Three-layer response + deep analysis
# ===========================================================================

def three_layer_response(query: str, mode: ResponseMode, zone: PositionZone) -> EngineResponse:
    span = TelemetrySpan("three_layer_response")
    t0 = time.perf_counter()

    # Layer 1: Doctrine cache lookup
    topics = decompose_query(query)
    doctrine_hits: list[str] = []
    authorities: list[str] = []
    reasoning: list[str] = []
    answer_parts: list[str] = []
    frag = 0.0

    for topic in topics:
        doc = DOCTRINE_CACHE.get(topic)
        if doc:
            COVERAGE.trigger(topic)
            METRICS.record_cache(True)
            doctrine_hits.append(topic)
            authorities.extend(authority_chain(doc))
            reasoning.append(doc.get("reasoning_framework", ""))
            answer_parts.append(doc.get("conclusion_template", ""))
            frag = max(frag, fragility_score(doc))
        else:
            METRICS.record_cache(False)

    if not doctrine_hits:
        COVERAGE.miss(query)
        # Layer 2: Vector search fallback
        hits = vector_search(query, top_k=3)
        for topic, score in hits:
            doc = DOCTRINE_CACHE.get(topic)
            if doc:
                doctrine_hits.append(topic)
                answer_parts.append(doc.get("conclusion_template", ""))
                authorities.extend(authority_chain(doc))
                frag = max(frag, fragility_score(doc))

    if not answer_parts:
        # Layer 3: Deep analysis
        answer_parts.append(
            f"No pre-compiled doctrine matched query '{query}'. "
            "Deep analysis: this query touches optimization concepts not yet "
            "in the doctrine cache. A manual analysis is recommended using "
            "the solver endpoints (/solve/lp, /solve/gradient_descent, etc.)."
        )
        frag = 0.7

    # Compose answer based on mode
    zone_prefix = ZONE_PREFIXES.get(zone, "")
    if mode == ResponseMode.FAST:
        answer = zone_prefix + " ".join(answer_parts[:2])
    elif mode == ResponseMode.DEFENSE:
        answer = zone_prefix + "\n\n".join(answer_parts)
        if reasoning:
            answer += "\n\nReasoning Framework:\n" + reasoning[0][:500]
    else:  # MEMO
        answer = zone_prefix + "MEMORANDUM\n\n"
        answer += "Subject: " + query + "\n\n"
        answer += "Analysis:\n" + "\n\n".join(answer_parts) + "\n\n"
        if reasoning:
            answer += "Detailed Reasoning:\n" + "\n\n".join(reasoning) + "\n\n"
        answer += "Authorities:\n" + "\n".join(f"- {a}" for a in authorities)

    conf = ConfidenceLevel.DEFENSIBLE
    if doctrine_hits:
        doc0 = DOCTRINE_CACHE.get(doctrine_hits[0], {})
        conf = classify_confidence(doc0, query)

    elapsed = (time.perf_counter() - t0) * 1000
    dhash = determinism_hash({"query": query, "hits": doctrine_hits, "answer": answer})

    DRIFT.observe(
        topic=doctrine_hits[0] if doctrine_hits else "unknown",
        confidence=conf.value, result_hash=dhash,
    )

    resp = EngineResponse(
        mode=mode, zone=zone, confidence=conf,
        answer=answer, doctrine_hits=doctrine_hits,
        authority_chain=authorities[:10], reasoning_trace=reasoning[:3],
        determinism_hash=dhash, elapsed_ms=round(elapsed, 2),
        fragility_score=round(frag, 3),
        disclosure_caveat="Mathematical results assume exact arithmetic; numerical solvers have finite precision."
            if frag > 0.3 else "",
    )
    METRICS.record_query("three_layer", elapsed)
    audit_log("query", {"query": query, "mode": mode.value, "hits": doctrine_hits, "elapsed_ms": elapsed})
    span.finish()
    return resp


# ===========================================================================
# TIE Component 2: Response modes — handled in three_layer_response
# TIE Component 17: FastAPI server
# TIE Component 18: Loguru logging — configured at top
# ===========================================================================

# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="MATH07 Optimization Engine",
    version=ENGINE_VERSION,
    description="TIE-20 compliant optimization engine — LP, NLP, IP, portfolio, multi-objective",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()


@app.on_event("startup")
async def startup() -> None:
    load_knowledge_base()
    logger.info("MATH07 Optimization Engine v{} starting on port {}", ENGINE_VERSION, ENGINE_PORT)


# ---------------------------------------------------------------------------
# TIE Component 12: Health endpoint
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        uptime_seconds=round(time.time() - START_TIME, 1),
        queries_served=METRICS.queries_total,
        doctrines_loaded=len(DOCTRINE_CACHE),
        semantic_terms=len(SEMANTIC_DICT),
        coverage_domains=len(COVERAGE_MAP.get("coverage_domains", {})),
        components_active=[
            "three_layer_response", "response_modes", "doctrine_cache",
            "authority_hardening", "confidence_stratification",
            "semantic_normalization", "vector_search", "telemetry",
            "drift_watcher", "coverage_map", "metrics_collector",
            "health_endpoint", "zoned_analysis", "fact_fragility_scoring",
            "audit_trail_jsonl", "determinism_hash_sha256",
            "fastapi_server", "loguru_logging",
            "multi_doctrine_decomposition", "deep_analysis_mode",
        ],
    )


@app.get("/metrics")
async def metrics() -> dict[str, Any]:
    return METRICS.snapshot()


@app.get("/drift")
async def drift_report() -> dict[str, Any]:
    return DRIFT.report()


@app.get("/coverage")
async def coverage_report() -> dict[str, Any]:
    return COVERAGE.report()


# ---------------------------------------------------------------------------
# Query endpoint
# ---------------------------------------------------------------------------

@app.post("/query", response_model=EngineResponse)
async def query(req: QueryRequest) -> EngineResponse:
    logger.info("Query: mode={} zone={} q='{}'", req.mode.value, req.zone.value, req.query[:80])
    return three_layer_response(req.query, req.mode, req.zone)


# ---------------------------------------------------------------------------
# LP solver endpoint
# ---------------------------------------------------------------------------

@app.post("/solve/lp", response_model=LPResult)
async def solve_lp(problem: LPProblem) -> LPResult:
    span = TelemetrySpan("solve_lp_endpoint")
    logger.info("LP solve: {} vars, {} constraints", len(problem.objective), len(problem.constraints))
    a = [c.coefficients for c in problem.constraints]
    b_vec = [c.rhs for c in problem.constraints]
    ct = [c.constraint_type for c in problem.constraints]
    solver = SimplexSolver(problem.objective, a, b_vec, ct, problem.sense)
    solver.solve()
    elapsed = span.finish()
    METRICS.record_query("lp", elapsed, error=solver.status != SolverStatus.OPTIMAL)
    audit_log("lp_solve", {"status": solver.status.value, "vars": len(problem.objective)})
    vnames = problem.variable_names or [f"x{i}" for i in range(len(problem.objective))]
    sensitivity = None
    if solver.status == SolverStatus.OPTIMAL:
        sensitivity = {
            "shadow_prices": dict(zip([f"c{i}" for i in range(len(solver.shadow_prices))], solver.shadow_prices)),
            "reduced_costs": dict(zip(vnames, solver.reduced_costs)),
        }
    return LPResult(
        status=solver.status,
        objective_value=round(solver.obj_value, 10) if solver.status == SolverStatus.OPTIMAL else None,
        solution=[round(v, 10) for v in solver.solution] if solver.solution else None,
        variable_names=vnames,
        shadow_prices=solver.shadow_prices if solver.shadow_prices else None,
        reduced_costs=solver.reduced_costs if solver.reduced_costs else None,
        iterations=solver.iterations,
        sensitivity=sensitivity,
        elapsed_ms=round(elapsed, 2),
        determinism_hash=determinism_hash(solver.solution) if solver.solution else "",
    )


# ---------------------------------------------------------------------------
# Unconstrained optimization endpoints
# ---------------------------------------------------------------------------

@app.post("/solve/gradient_descent", response_model=OptimizationResult)
async def solve_gd(problem: UnconstrainedProblem) -> OptimizationResult:
    logger.info("GD solve: expr='{}' x0={}", problem.function_expr[:60], problem.x0)
    result = gradient_descent_solve(
        problem.function_expr, problem.x0, problem.learning_rate,
        problem.max_iter, problem.tol,
    )
    METRICS.record_query("gradient_descent", result.elapsed_ms, error=not result.converged)
    return result


@app.post("/solve/newton", response_model=OptimizationResult)
async def solve_newton(problem: UnconstrainedProblem) -> OptimizationResult:
    logger.info("Newton solve: expr='{}' x0={}", problem.function_expr[:60], problem.x0)
    result = newton_optimize(problem.function_expr, problem.x0, problem.max_iter, problem.tol)
    METRICS.record_query("newton", result.elapsed_ms, error=not result.converged)
    return result


@app.post("/solve/conjugate_gradient", response_model=OptimizationResult)
async def solve_cg(problem: UnconstrainedProblem) -> OptimizationResult:
    logger.info("CG solve: expr='{}' x0={}", problem.function_expr[:60], problem.x0)
    result = conjugate_gradient_solve(
        problem.function_expr, problem.x0, problem.max_iter, problem.tol,
    )
    METRICS.record_query("conjugate_gradient", result.elapsed_ms, error=not result.converged)
    return result


@app.post("/solve/golden_section", response_model=OptimizationResult)
async def solve_golden(problem: GoldenSectionProblem) -> OptimizationResult:
    logger.info("Golden section: expr='{}' [{}, {}]", problem.function_expr[:60], problem.a, problem.b)
    result = golden_section_minimize(
        problem.function_expr, problem.a, problem.b, problem.tol, problem.max_iter,
    )
    METRICS.record_query("golden_section", result.elapsed_ms)
    return result


# ---------------------------------------------------------------------------
# Constrained optimization endpoint
# ---------------------------------------------------------------------------

@app.post("/solve/lagrange", response_model=OptimizationResult)
async def solve_lagrange(problem: LagrangeProblem) -> OptimizationResult:
    logger.info("Lagrange solve: obj='{}' constraints={}", problem.objective_expr[:60], len(problem.constraint_exprs))
    result = lagrange_solve(
        problem.objective_expr, problem.constraint_exprs,
        problem.x0, problem.tol, problem.max_iter,
    )
    METRICS.record_query("lagrange", result.elapsed_ms, error=not result.converged)
    return result


# ---------------------------------------------------------------------------
# Portfolio optimization endpoint
# ---------------------------------------------------------------------------

@app.post("/solve/portfolio", response_model=PortfolioResult)
async def solve_portfolio(problem: PortfolioProblem) -> PortfolioResult:
    span = TelemetrySpan("portfolio_solve")
    logger.info("Portfolio: {} assets, rf={}", len(problem.expected_returns), problem.risk_free_rate)
    try:
        ps = PortfolioSolver(
            problem.expected_returns, problem.covariance_matrix,
            problem.risk_free_rate, problem.allow_short,
        )
        mv_w, mv_r, mv_v = ps.minimum_variance()
        frontier = ps.efficient_frontier(problem.num_frontier_points)
        tang_w, tang_r, tang_v, tang_sr = ps.tangency_portfolio()

        if problem.target_return is not None:
            opt_w, opt_r, opt_v = ps.optimal_for_target(problem.target_return)
            opt_sr = (opt_r - problem.risk_free_rate) / max(opt_v, FLOAT_TOL)
        else:
            opt_w, opt_r, opt_v, opt_sr = tang_w, tang_r, tang_v, tang_sr

        elapsed = span.finish()
        METRICS.record_query("portfolio", elapsed)
        return PortfolioResult(
            status=SolverStatus.OPTIMAL,
            weights=[round(w, 8) for w in opt_w],
            expected_return=round(opt_r, 8),
            volatility=round(opt_v, 8),
            sharpe_ratio=round(opt_sr, 6),
            efficient_frontier=frontier,
            min_variance_weights=[round(w, 8) for w in mv_w],
            tangency_weights=[round(w, 8) for w in tang_w],
            elapsed_ms=round(elapsed, 2),
            determinism_hash=determinism_hash(opt_w),
        )
    except Exception as exc:
        elapsed = span.finish(str(exc))
        logger.error("Portfolio solve error: {}", exc)
        METRICS.record_query("portfolio", elapsed, error=True)
        return PortfolioResult(
            status=SolverStatus.ERROR, elapsed_ms=round(elapsed, 2),
            determinism_hash="",
        )


# ---------------------------------------------------------------------------
# Integer programming endpoint
# ---------------------------------------------------------------------------

@app.post("/solve/integer", response_model=IntegerResult)
async def solve_integer(problem: IntegerProgramProblem) -> IntegerResult:
    logger.info("IP solve: {} vars, {} constraints", len(problem.objective), len(problem.constraints))
    a = [c.coefficients for c in problem.constraints]
    b_vec = [c.rhs for c in problem.constraints]
    ct = [c.constraint_type for c in problem.constraints]
    int_vars = problem.integer_vars or list(range(len(problem.objective)))
    result = branch_and_bound_solve(
        problem.objective, a, b_vec, ct, problem.sense, int_vars, problem.max_nodes,
    )
    METRICS.record_query("integer", result.elapsed_ms, error=result.status != SolverStatus.OPTIMAL)
    return result


# ---------------------------------------------------------------------------
# Multi-objective endpoint
# ---------------------------------------------------------------------------

@app.post("/solve/multi_objective", response_model=MultiObjectiveResult)
async def solve_multi_objective(problem: MultiObjectiveProblem) -> MultiObjectiveResult:
    span = TelemetrySpan("multi_objective_solve")
    logger.info("Multi-obj: {} objectives, method={}", len(problem.objective_exprs), problem.method)
    try:
        x0 = problem.x0 or [0.0] * problem.n_vars
        points = approximate_pareto_front(
            problem.objective_exprs, x0, problem.num_points, problem.method,
        )
        elapsed = span.finish()
        METRICS.record_query("multi_objective", elapsed)
        return MultiObjectiveResult(
            status=SolverStatus.OPTIMAL,
            pareto_points=points,
            method=problem.method,
            elapsed_ms=round(elapsed, 2),
            determinism_hash=determinism_hash([p.objectives for p in points]),
        )
    except Exception as exc:
        elapsed = span.finish(str(exc))
        logger.error("Multi-objective error: {}", exc)
        METRICS.record_query("multi_objective", elapsed, error=True)
        return MultiObjectiveResult(
            status=SolverStatus.ERROR, method=problem.method,
            elapsed_ms=round(elapsed, 2), determinism_hash="",
        )


# ---------------------------------------------------------------------------
# Utility endpoints
# ---------------------------------------------------------------------------

@app.post("/util/check_convexity")
async def check_convexity(payload: dict[str, Any]) -> dict[str, Any]:
    """Check if a function's Hessian is PSD at a given point."""
    expr = payload.get("function_expr", "")
    x = payload.get("x", [0.0, 0.0])
    hess = _numerical_hessian(expr, x)
    is_pd = mat_is_positive_definite(hess)
    return {
        "function": expr,
        "point": x,
        "hessian": hess,
        "positive_definite": is_pd,
        "conclusion": "Function appears convex at this point" if is_pd else "Function may be non-convex at this point",
    }


@app.post("/util/matrix_inverse")
async def matrix_inverse_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
    m = payload.get("matrix", [])
    try:
        inv = mat_inverse(m)
        d = mat_det(m)
        return {"inverse": inv, "determinant": d, "success": True}
    except Exception as exc:
        return {"error": str(exc), "success": False}


@app.post("/util/solve_linear_system")
async def solve_linear_system(payload: dict[str, Any]) -> dict[str, Any]:
    a = payload.get("A", [])
    b = payload.get("b", [])
    try:
        x = mat_solve(a, b)
        residual = vec_sub(mat_vec_mult(a, x), b)
        return {"solution": x, "residual": residual, "residual_norm": vec_norm(residual), "success": True}
    except Exception as exc:
        return {"error": str(exc), "success": False}


# ---------------------------------------------------------------------------
# Doctrine listing
# ---------------------------------------------------------------------------

@app.get("/doctrines")
async def list_doctrines() -> dict[str, Any]:
    return {
        "engine": ENGINE_ID,
        "count": len(DOCTRINE_CACHE),
        "topics": list(DOCTRINE_CACHE.keys()),
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> dict[str, Any]:
    doc = DOCTRINE_CACHE.get(topic)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Doctrine '{topic}' not found")
    return doc


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    load_knowledge_base()
    logger.info("Starting MATH07 on port {}", ENGINE_PORT)
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
