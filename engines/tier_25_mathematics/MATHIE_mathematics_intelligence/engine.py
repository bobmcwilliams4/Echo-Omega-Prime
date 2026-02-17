import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union, Set, Tuple
import enum
import datetime
import asyncio
import aiohttp
import json
import time
import statistics
import collections

# Engine constants
ENGINE_ID = "MATHIE"
ENGINE_PORT = 8861
ENGINE_NAME = "Mathematics Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# Enums
class ResponseMode(str, enum.Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, enum.Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, enum.Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, enum.Enum):
    LINEAR_ALGEBRA = "LINEAR_ALGEBRA"
    CALCULUS = "CALCULUS"
    STATISTICS = "STATISTICS"
    DIFFERENTIAL_EQUATIONS = "DIFFERENTIAL_EQUATIONS"
    NUMBER_THEORY = "NUMBER_THEORY"
    OPTIMIZATION = "OPTIMIZATION"
    NUMERICAL_METHODS = "NUMERICAL_METHODS"
    PROBABILITY = "PROBABILITY"
    DISCRETE_MATH = "DISCRETE_MATH"
    TOPOLOGY = "TOPOLOGY"
    ABSTRACT_ALGEBRA = "ABSTRACT_ALGEBRA"
    COMPLEX_ANALYSIS = "COMPLEX_ANALYSIS"
    FUNCTIONAL_ANALYSIS = "FUNCTIONAL_ANALYSIS"
    MATHEMATICAL_LOGIC = "MATHEMATICAL_LOGIC"
    COMBINATORICS = "COMBINATORICS"
    GRAPH_THEORY = "GRAPH_THEORY"
    GAME_THEORY = "GAME_THEORY"
    SET_THEORY = "SET_THEORY"
    MEASURE_THEORY = "MEASURE_THEORY"
    ERGODIC_THEORY = "ERGODIC_THEORY"
    DYNAMICAL_SYSTEMS = "DYNAMICAL_SYSTEMS"
    ALGEBRAIC_GEOMETRY = "ALGEBRAIC_GEOMETRY"
    GEOMETRY = "GEOMETRY"
    FRACTALS = "FRACTALS"
    MATHEMATICAL_PHYSICS = "MATHEMATICAL_PHYSICS"
    MATHEMATICAL_BIOLOGY = "MATHEMATICAL_BIOLOGY"
    MATHEMATICAL_FINANCE = "MATHEMATICAL_FINANCE"
    MATHEMATICAL_STATISTICS = "MATHEMATICAL_STATISTICS"
    STOCHASTIC_PROCESSES = "STOCHASTIC_PROCESSES"
    INFORMATION_THEORY = "INFORMATION_THEORY"
    LOGIC = "LOGIC"
    COMPUTATIONAL_MATH = "COMPUTATIONAL_MATH"
    MATHEMATICAL_PROGRAMMING = "MATHEMATICAL_PROGRAMMING"
    MATHEMATICAL_MODELING = "MATHEMATICAL_MODELING"
    MATHEMATICS_EDUCATION = "MATHEMATICS_EDUCATION"
    HISTORY_OF_MATH = "HISTORY_OF_MATH"
    MATHEMATICAL_FOUNDATIONS = "MATHEMATICAL_FOUNDATIONS"
    OTHER = "OTHER"

class SubEngineStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    question: str
    context: Optional[str] = None
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: Optional[IssueCategory] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: float = Field(default_factory=lambda: time.time())

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: str
    answer: str
    confidence: float
    status: str
    latency_ms: float
    issue_category: Optional[IssueCategory] = None
    routing_decision: Optional[str] = None
    orchestration_trace: Optional[List[str]] = None
    timestamp: float = Field(default_factory=lambda: time.time())
    metadata: Optional[Dict[str, Any]] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float
    domains: List[IssueCategory]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    rule_applied: str
    confidence: float
    timestamp: float = Field(default_factory=lambda: time.time())
    trace: Optional[List[str]] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    sub_engine_response: Optional[QueryResponse] = None
    orchestration_status: str
    orchestration_latency_ms: float
    orchestration_trace: Optional[List[str]] = None
    timestamp: float = Field(default_factory=lambda: time.time())
    errors: Optional[List[str]] = None

# Sub-engine registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "MATH01": SubEngineConfig(
        engine_id="MATH01",
        name="Linear Algebra Engine",
        port=8862,
        health_url="http://localhost:8862/health",
        capabilities=["matrix", "vector", "eigenvalue", "eigenvector", "linear_system", "determinant", "rank", "singular_value", "decomposition"],
        weight=1.0,
        domains=[IssueCategory.LINEAR_ALGEBRA]
    ),
    "MATH02": SubEngineConfig(
        engine_id="MATH02",
        name="Calculus Engine",
        port=8863,
        health_url="http://localhost:8863/health",
        capabilities=["derivative", "integral", "limit", "series", "multivariable", "partial_derivative", "gradient", "jacobian", "taylor"],
        weight=1.0,
        domains=[IssueCategory.CALCULUS]
    ),
    "MATH03": SubEngineConfig(
        engine_id="MATH03",
        name="Statistics Engine",
        port=8864,
        health_url="http://localhost:8864/health",
        capabilities=["mean", "variance", "standard_deviation", "distribution", "hypothesis_test", "regression", "anova", "correlation", "sampling"],
        weight=1.0,
        domains=[IssueCategory.STATISTICS, IssueCategory.MATHEMATICAL_STATISTICS]
    ),
    "MATH04": SubEngineConfig(
        engine_id="MATH04",
        name="Differential Equations Engine",
        port=8865,
        health_url="http://localhost:8865/health",
        capabilities=["ode", "pde", "laplace", "fourier", "boundary_value", "initial_value", "stability", "eigenfunction"],
        weight=1.0,
        domains=[IssueCategory.DIFFERENTIAL_EQUATIONS, IssueCategory.DYNAMICAL_SYSTEMS]
    ),
    "MATH05": SubEngineConfig(
        engine_id="MATH05",
        name="Number Theory Engine",
        port=8866,
        health_url="http://localhost:8866/health",
        capabilities=["prime", "divisor", "gcd", "modular", "congruence", "diophantine", "cryptography"],
        weight=1.0,
        domains=[IssueCategory.NUMBER_THEORY]
    ),
    "MATH06": SubEngineConfig(
        engine_id="MATH06",
        name="Optimization Engine",
        port=8867,
        health_url="http://localhost:8867/health",
        capabilities=["linear_programming", "nonlinear_programming", "integer_programming", "convex", "dual", "lagrange", "gradient_descent"],
        weight=1.0,
        domains=[IssueCategory.OPTIMIZATION, IssueCategory.MATHEMATICAL_PROGRAMMING]
    ),
    "MATH07": SubEngineConfig(
        engine_id="MATH07",
        name="Numerical Methods Engine",
        port=8868,
        health_url="http://localhost:8868/health",
        capabilities=["approximation", "numerical_integration", "numerical_differentiation", "root_finding", "finite_difference", "finite_element"],
        weight=1.0,
        domains=[IssueCategory.NUMERICAL_METHODS, IssueCategory.COMPUTATIONAL_MATH]
    ),
    "MATH08": SubEngineConfig(
        engine_id="MATH08",
        name="Probability Engine",
        port=8869,
        health_url="http://localhost:8869/health",
        capabilities=["probability", "random_variable", "expectation", "variance", "bayes", "markov", "stochastic"],
        weight=1.0,
        domains=[IssueCategory.PROBABILITY, IssueCategory.STOCHASTIC_PROCESSES]
    ),
    "MATH09": SubEngineConfig(
        engine_id="MATH09",
        name="Discrete Mathematics Engine",
        port=8870,
        health_url="http://localhost:8870/health",
        capabilities=["logic", "set", "combinatorics", "graph", "boolean", "recurrence", "counting"],
        weight=1.0,
        domains=[IssueCategory.DISCRETE_MATH, IssueCategory.COMBINATORICS, IssueCategory.GRAPH_THEORY, IssueCategory.LOGIC, IssueCategory.SET_THEORY]
    ),
    "MATH10": SubEngineConfig(
        engine_id="MATH10",
        name="Topology Engine",
        port=8871,
        health_url="http://localhost:8871/health",
        capabilities=["open_set", "closed_set", "continuity", "compactness", "connectedness", "homotopy", "homology"],
        weight=1.0,
        domains=[IssueCategory.TOPOLOGY]
    ),
    "MATH11": SubEngineConfig(
        engine_id="MATH11",
        name="Abstract Algebra Engine",
        port=8872,
        health_url="http://localhost:8872/health",
        capabilities=["group", "ring", "field", "module", "homomorphism", "isomorphism", "ideal", "representation"],
        weight=1.0,
        domains=[IssueCategory.ABSTRACT_ALGEBRA]
    ),
    "MATH12": SubEngineConfig(
        engine_id="MATH12",
        name="Complex Analysis Engine",
        port=8873,
        health_url="http://localhost:8873/health",
        capabilities=["analytic_function", "residue", "contour", "cauchy", "riemann", "laurent", "singularity"],
        weight=1.0,
        domains=[IssueCategory.COMPLEX_ANALYSIS]
    ),
}

# Routing rules: keyword to engine_id mapping (200+ rules)
ROUTING_RULES: Dict[str, str] = {
    # Linear Algebra
    "matrix": "MATH01",
    "vector": "MATH01",
    "eigenvalue": "MATH01",
    "eigenvector": "MATH01",
    "determinant": "MATH01",
    "rank": "MATH01",
    "singular value": "MATH01",
    "svd": "MATH01",
    "linear system": "MATH01",
    "row reduction": "MATH01",
    "basis": "MATH01",
    "null space": "MATH01",
    "column space": "MATH01",
    "orthogonal": "MATH01",
    "projection": "MATH01",
    "gram-schmidt": "MATH01",
    "diagonalization": "MATH01",
    "trace": "MATH01",
    "minor": "MATH01",
    "cayley-hamilton": "MATH01",
    "spectral theorem": "MATH01",
    "cholesky": "MATH01",
    "qr decomposition": "MATH01",
    "lu decomposition": "MATH01",
    "moore-penrose": "MATH01",
    "pseudoinverse": "MATH01",
    # Calculus
    "derivative": "MATH02",
    "integral": "MATH02",
    "definite integral": "MATH02",
    "indefinite integral": "MATH02",
    "partial derivative": "MATH02",
    "gradient": "MATH02",
    "divergence": "MATH02",
    "curl": "MATH02",
    "limit": "MATH02",
    "series": "MATH02",
    "taylor series": "MATH02",
    "maclaurin series": "MATH02",
    "fourier series": "MATH02",
    "laplace transform": "MATH02",
    "multiple integral": "MATH02",
    "double integral": "MATH02",
    "triple integral": "MATH02",
    "jacobian": "MATH02",
    "hessian": "MATH02",
    "critical point": "MATH02",
    "maxima": "MATH02",
    "minima": "MATH02",
    "saddle point": "MATH02",
    # Statistics
    "mean": "MATH03",
    "average": "MATH03",
    "median": "MATH03",
    "mode": "MATH03",
    "variance": "MATH03",
    "standard deviation": "MATH03",
    "skewness": "MATH03",
    "kurtosis": "MATH03",
    "distribution": "MATH03",
    "normal distribution": "MATH03",
    "binomial distribution": "MATH03",
    "poisson distribution": "MATH03",
    "chi-square": "MATH03",
    "t-test": "MATH03",
    "anova": "MATH03",
    "regression": "MATH03",
    "linear regression": "MATH03",
    "logistic regression": "MATH03",
    "correlation": "MATH03",
    "pearson": "MATH03",
    "spearman": "MATH03",
    "sampling": "MATH03",
    "confidence interval": "MATH03",
    "hypothesis test": "MATH03",
    "p-value": "MATH03",
    "z-score": "MATH03",
    "outlier": "MATH03",
    "boxplot": "MATH03",
    "histogram": "MATH03",
    # Differential Equations
    "ode": "MATH04",
    "ordinary differential equation": "MATH04",
    "pde": "MATH04",
    "partial differential equation": "MATH04",
    "laplace equation": "MATH04",
    "heat equation": "MATH04",
    "wave equation": "MATH04",
    "fourier transform": "MATH04",
    "boundary value": "MATH04",
    "initial value": "MATH04",
    "stability": "MATH04",
    "eigenfunction": "MATH04",
    "green's function": "MATH04",
    "separation of variables": "MATH04",
    "runge-kutta": "MATH04",
    "phase portrait": "MATH04",
    "bifurcation": "MATH04",
    "nonlinear dynamics": "MATH04",
    # Number Theory
    "prime": "MATH05",
    "gcd": "MATH05",
    "lcm": "MATH05",
    "modular": "MATH05",
    "congruence": "MATH05",
    "diophantine": "MATH05",
    "fermat": "MATH05",
    "euler": "MATH05",
    "totient": "MATH05",
    "primitive root": "MATH05",
    "quadratic residue": "MATH05",
    "modulo": "MATH05",
    "divisor": "MATH05",
    "perfect number": "MATH05",
    "amicable number": "MATH05",
    "twin prime": "MATH05",
    "goldbach": "MATH05",
    "rsa": "MATH05",
    "cryptography": "MATH05",
    # Optimization
    "optimization": "MATH06",
    "linear programming": "MATH06",
    "simplex": "MATH06",
    "integer programming": "MATH06",
    "convex optimization": "MATH06",
    "lagrange multiplier": "MATH06",
    "dual problem": "MATH06",
    "kkt": "MATH06",
    "gradient descent": "MATH06",
    "stochastic gradient": "MATH06",
    "conjugate gradient": "MATH06",
    "objective function": "MATH06",
    "constraint": "MATH06",
    "feasible region": "MATH06",
    "slack variable": "MATH06",
    "branch and bound": "MATH06",
    "cutting plane": "MATH06",
    # Numerical Methods
    "numerical integration": "MATH07",
    "trapezoidal rule": "MATH07",
    "simpson's rule": "MATH07",
    "root finding": "MATH07",
    "bisection method": "MATH07",
    "newton's method": "MATH07",
    "secant method": "MATH07",
    "fixed point": "MATH07",
    "finite difference": "MATH07",
    "finite element": "MATH07",
    "interpolation": "MATH07",
    "extrapolation": "MATH07",
    "approximation": "MATH07",
    "error analysis": "MATH07",
    "stability analysis": "MATH07",
    # Probability
    "probability": "MATH08",
    "random variable": "MATH08",
    "expectation": "MATH08",
    "variance": "MATH08",
    "bayes": "MATH08",
    "bayesian": "MATH08",
    "markov": "MATH08",
    "markov chain": "MATH08",
    "stochastic process": "MATH08",
    "law of large numbers": "MATH08",
    "central limit theorem": "MATH08",
    "conditional probability": "MATH08",
    "joint probability": "MATH08",
    "independence": "MATH08",
    "martingale": "MATH08",
    # Discrete Math
    "logic": "MATH09",
    "propositional logic": "MATH09",
    "predicate logic": "MATH09",
    "set": "MATH09",
    "set theory": "MATH09",
    "combinatorics": "MATH09",
    "permutation": "MATH09",
    "combination": "MATH09",
    "graph": "MATH09",
    "graph theory": "MATH09",
    "tree": "MATH09",
    "spanning tree": "MATH09",
    "planar graph": "MATH09",
    "coloring": "MATH09",
    "clique": "MATH09",
    "hamiltonian": "MATH09",
    "eulerian": "MATH09",
    "recurrence": "MATH09",
    "boolean algebra": "MATH09",
    "counting": "MATH09",
    "pigeonhole": "MATH09",
    "inclusion-exclusion": "MATH09",
    # Topology
    "topology": "MATH10",
    "open set": "MATH10",
    "closed set": "MATH10",
    "continuity": "MATH10",
    "compactness": "MATH10",
    "connectedness": "MATH10",
    "homotopy": "MATH10",
    "homology": "MATH10",
    "fundamental group": "MATH10",
    "covering space": "MATH10",
    "metric space": "MATH10",
    "quotient space": "MATH10",
    "manifold": "MATH10",
    "fiber bundle": "MATH10",
    # Abstract Algebra
    "group": "MATH11",
    "ring": "MATH11",
    "field": "MATH11",
    "module": "MATH11",
    "homomorphism": "MATH11",
    "isomorphism": "MATH11",
    "ideal": "MATH11",
    "representation": "MATH11",
    "normal subgroup": "MATH11",
    "simple group": "MATH11",
    "abelian": "MATH11",
    "nonabelian": "MATH11",
    "galois": "MATH11",
    "solvable group": "MATH11",
    "semisimple": "MATH11",
    # Complex Analysis
    "complex analysis": "MATH12",
    "analytic function": "MATH12",
    "residue": "MATH12",
    "contour": "MATH12",
    "cauchy": "MATH12",
    "riemann": "MATH12",
    "laurent": "MATH12",
    "singularity": "MATH12",
    "branch cut": "MATH12",
    "conformal": "MATH12",
    "mobius": "MATH12",
    "harmonic": "MATH12",
    # Additional rules for coverage (abbreviated for brevity)
    "functional analysis": "MATH01",
    "mathematical logic": "MATH09",
    "game theory": "MATH09",
    "measure theory": "MATH10",
    "ergodic theory": "MATH10",
    "dynamical system": "MATH04",
    "algebraic geometry": "MATH11",
    "geometry": "MATH10",
    "fractal": "MATH10",
    "mathematical physics": "MATH04",
    "mathematical biology": "MATH03",
    "mathematical finance": "MATH03",
    "information theory": "MATH08",
    "computational math": "MATH07",
    "mathematical modeling": "MATH07",
    "mathematics education": "MATH09",
    "history of math": "MATH09",
    "mathematical foundations": "MATH09",
    # ... (extend to 200+ rules as needed)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_log = collections.deque(maxlen=10000)
        self.error_log = collections.deque(maxlen=1000)
        self.latency_log = collections.deque(maxlen=10000)
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: float, timestamp: Optional[float] = None):
        if timestamp is None:
            timestamp = time.time()
        async with self.lock:
            self.query_log.append((query_id, latency_ms, timestamp))
            self.latency_log.append(latency_ms)

    async def record_error(self, query_id: str, error_msg: str, timestamp: Optional[float] = None):
        if timestamp is None:
            timestamp = time.time()
        async with self.lock:
            self.error_log.append((query_id, error_msg, timestamp))

    async def get_latency_stats(self) -> Dict[str, float]:
        async with self.lock:
            latencies = list(self.latency_log)
        if not latencies:
            return {"min": 0, "max": 0, "mean": 0, "stdev": 0}
        return {
            "min": min(latencies),
            "max": max(latencies),
            "mean": statistics.mean(latencies),
            "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0
        }

    async def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        async with self.lock:
            return sum(1 for _, _, t in self.query_log if t >= cutoff)

@dataclass
class DoctrineBlock:
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
    confidence_zone: str
    controlling_precedent: str


DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Linear Algebra: Matrix Eigenvalue Decomposition",
        keywords=["matrix", "eigenvalue", "eigenvector", "decomposition", "spectral theorem", "diagonalization", "hermitian", "symmetric"],
        conclusion_template=(
            "Eigenvalue decomposition provides a fundamental tool for understanding linear transformations. "
            "For diagonalizable matrices, the decomposition into eigenvalues and eigenvectors enables simplification "
            "of matrix functions and solution of linear systems. The spectral theorem guarantees orthonormal eigenbases "
            "for symmetric or Hermitian matrices, ensuring stability and interpretability in applications."
        ),
        reasoning_framework=(
            "Eigenvalue decomposition is central to linear algebra, allowing a matrix A ∈ ℝ^{n×n} to be expressed as A = PDP^{-1}, "
            "where D is diagonal with eigenvalues λ_i on the diagonal and P contains corresponding eigenvectors as columns. "
            "This decomposition is guaranteed for diagonalizable matrices, a class including all symmetric matrices over ℝ and Hermitian matrices over ℂ. "
            "The spectral theorem states that any real symmetric matrix can be diagonalized by an orthogonal matrix, implying P^{-1} = P^T. "
            "This orthogonality ensures numerical stability and simplifies computations such as matrix powers and exponentials. "
            "Eigenvalues provide insight into matrix properties: positive definiteness, rank, and conditioning. "
            "In applications like Principal Component Analysis (PCA), eigenvalue decomposition identifies directions of maximal variance. "
            "The Jordan canonical form generalizes eigenvalue decomposition to defective matrices but lacks the orthogonality property. "
            "Computational methods such as the QR algorithm efficiently approximate eigenvalues and eigenvectors. "
            "Perturbation theory analyzes sensitivity of eigenvalues to matrix changes, critical in numerical linear algebra. "
            "The decomposition also underpins solutions to differential equations, stability analysis, and quantum mechanics operators. "
            "Limitations arise for non-diagonalizable matrices or large sparse matrices where iterative methods are preferred. "
            "Overall, eigenvalue decomposition is a cornerstone of theoretical and applied linear algebra, enabling dimensionality reduction, system analysis, and more."
        ),
        key_factors=[
            "Matrix diagonalizability",
            "Symmetry or Hermitian property",
            "Orthogonality of eigenvectors",
            "Numerical stability",
            "Applications in PCA and system analysis"
        ],
        primary_authority=[
            "Horn, R. A., & Johnson, C. R. (2012). Matrix Analysis. Cambridge University Press.",
            "Strang, G. (2016). Introduction to Linear Algebra. Wellesley-Cambridge Press.",
            "Trefethen, L. N., & Bau, D. (1997). Numerical Linear Algebra. SIAM.",
            "Golub, G. H., & Van Loan, C. F. (2013). Matrix Computations. Johns Hopkins University Press.",
            "Axler, S. (2015). Linear Algebra Done Right. Springer."
        ],
        burden_holder="Proponent of matrix diagonalization applicability",
        adversary_position="Challenges on diagonalizability and numerical stability for defective or large sparse matrices",
        counter_arguments=[
            "Not all matrices are diagonalizable; Jordan form is required for defective matrices.",
            "Numerical instability can arise without orthogonality, especially in non-symmetric cases.",
            "Large sparse matrices require iterative eigenvalue methods rather than direct decomposition.",
            "Eigenvalue sensitivity to perturbations can limit practical use in noisy data.",
            "Computational cost may be prohibitive for very large matrices."
        ],
        resolution_strategy=(
            "Apply spectral theorem conditions to restrict to symmetric/Hermitian matrices for guaranteed orthogonal diagonalization. "
            "Use numerical algorithms like QR iteration for stable eigenvalue computation. "
            "For defective matrices, consider Jordan canonical form or Schur decomposition. "
            "Employ perturbation theory to assess eigenvalue stability. "
            "Utilize sparse matrix methods and iterative algorithms when dealing with large-scale problems."
        ),
        entity_scope="Matrices in finite-dimensional vector spaces over ℝ or ℂ",
        confidence=0.95,
        confidence_zone="High confidence for symmetric/Hermitian matrices; moderate for general matrices",
        controlling_precedent="Horn & Johnson (2012), Theorems 4.2.5 and 7.3.9 on spectral theorem and diagonalization"
    ),

    DoctrineBlock(
        topic="Calculus: Limit and Continuity",
        keywords=["limit", "continuity", "epsilon-delta", "function", "convergence", "real analysis", "topology", "uniform continuity"],
        conclusion_template=(
            "The concept of limits formalizes the behavior of functions near points, underpinning continuity and differentiability. "
            "Continuity ensures no abrupt changes, characterized by the epsilon-delta definition. "
            "Uniform continuity strengthens this by requiring a global delta for all points in the domain, critical in analysis and topology."
        ),
        reasoning_framework=(
            "Limits are foundational in calculus and analysis, defining the value a function approaches as its argument tends to a point. "
            "The epsilon-delta definition rigorously captures this: for every ε > 0, there exists δ > 0 such that for all x within δ of c, "
            "the function values are within ε of L. This formalism avoids ambiguity inherent in intuitive notions of limits. "
            "Continuity at a point c means the limit of f(x) as x approaches c equals f(c), ensuring no jumps or breaks. "
            "Uniform continuity extends this by requiring a single δ to work for all points in the domain, a stronger condition important for functions on closed intervals. "
            "The Heine-Cantor theorem states that continuous functions on compact sets are uniformly continuous, linking topology and analysis. "
            "Discontinuities are classified as removable, jump, or essential, each with distinct implications for function behavior and integrability. "
            "Limits also underpin derivative definitions and integral approximations, making them central to calculus. "
            "In metric spaces, limits generalize to sequences and nets, broadening applicability. "
            "The interplay between limits and topology is evident in the characterization of open and closed sets via limit points. "
            "Counterexamples such as Dirichlet’s function illustrate pathological cases where limits fail to exist or continuity is absent everywhere. "
            "Overall, limits and continuity form the bedrock of real analysis, enabling rigorous treatment of change and approximation."
        ),
        key_factors=[
            "Epsilon-delta formalism",
            "Pointwise vs uniform continuity",
            "Compactness and Heine-Cantor theorem",
            "Types of discontinuities",
            "Topological implications"
        ],
        primary_authority=[
            "Rudin, W. (1976). Principles of Mathematical Analysis. McGraw-Hill.",
            "Bartle, R. G., & Sherbert, D. R. (2011). Introduction to Real Analysis. Wiley.",
            "Abbott, S. (2015). Understanding Analysis. Springer.",
            "Munkres, J. R. (2000). Topology. Prentice Hall.",
            "Royden, H. L., & Fitzpatrick, P. M. (2010). Real Analysis. Pearson."
        ],
        burden_holder="Proponent of function continuity claims",
        adversary_position="Claims of discontinuities or failure of uniform continuity",
        counter_arguments=[
            "Function may have removable or jump discontinuities invalidating continuity claims.",
            "Uniform continuity fails on unbounded or non-compact domains.",
            "Epsilon-delta conditions may not be satisfied for pathological functions.",
            "Limits may not exist or differ from function value at points of discontinuity.",
            "Topological properties of domain affect continuity behavior."
        ],
        resolution_strategy=(
            "Use epsilon-delta proofs to verify continuity at points. "
            "Apply Heine-Cantor theorem to establish uniform continuity on compact domains. "
            "Classify discontinuities to understand function behavior. "
            "Employ counterexamples to test claims rigorously. "
            "Utilize topological tools to analyze limit points and continuity."
        ),
        entity_scope="Real-valued functions on subsets of ℝ or metric spaces",
        confidence=0.97,
        confidence_zone="Very high confidence in classical real analysis settings",
        controlling_precedent="Rudin (1976), Theorem 4.1 on limits and continuity; Munkres (2000), Theorem 4.19 on uniform continuity"
    ),

    DoctrineBlock(
        topic="Statistics: Hypothesis Testing",
        keywords=["hypothesis testing", "null hypothesis", "alternative hypothesis", "p-value", "type I error", "type II error", "significance level", "power"],
        conclusion_template=(
            "Hypothesis testing provides a structured framework for decision making under uncertainty. "
            "By formulating null and alternative hypotheses, and controlling error rates, it enables objective evaluation of evidence. "
            "P-values quantify evidence against the null, while power analysis guides test sensitivity."
        ),
        reasoning_framework=(
            "Hypothesis testing is a cornerstone of inferential statistics, allowing practitioners to assess claims about populations based on sample data. "
            "The null hypothesis (H0) represents a baseline or status quo, while the alternative hypothesis (H1) represents the claim under investigation. "
            "Test statistics are computed from data and compared against critical values derived from sampling distributions under H0. "
            "The p-value measures the probability of observing data as extreme or more so than the observed, assuming H0 is true. "
            "A significance level α is pre-specified to control the probability of Type I error (false positive), rejecting H0 when it is true. "
            "Type II error (false negative) occurs when H0 is not rejected despite H1 being true, with probability β. "
            "Power, defined as 1 - β, measures the test’s ability to detect true effects. "
            "Choosing appropriate tests (parametric or nonparametric) depends on data distribution, sample size, and assumptions. "
            "Multiple testing corrections (e.g., Bonferroni) address inflated Type I error rates when conducting many tests. "
            "Hypothesis testing frameworks extend to complex models including regression, ANOVA, and Bayesian approaches. "
            "Critiques include overreliance on p-values and neglect of effect sizes or confidence intervals. "
            "Robustness checks and replication are essential to validate findings. "
            "Overall, hypothesis testing remains a fundamental tool in statistics, balancing rigor and practical decision making."
        ),
        key_factors=[
            "Formulation of null and alternative hypotheses",
            "Control of Type I and Type II errors",
            "Calculation and interpretation of p-values",
            "Test selection and assumptions",
            "Power and sample size considerations"
        ],
        primary_authority=[
            "Casella, G., & Berger, R. L. (2002). Statistical Inference. Duxbury.",
            "Lehmann, E. L., & Romano, J. P. (2005). Testing Statistical Hypotheses. Springer.",
            "Wasserman, L. (2004). All of Statistics. Springer.",
            "Fisher, R. A. (1925). Statistical Methods for Research Workers. Oliver & Boyd.",
            "Neyman, J., & Pearson, E. S. (1933). On the Problem of the Most Efficient Tests of Statistical Hypotheses. Philosophical Transactions of the Royal Society A."
        ],
        burden_holder="Proponent of rejecting or accepting hypotheses",
        adversary_position="Skepticism about evidence sufficiency or test assumptions",
        counter_arguments=[
            "P-values do not measure probability that H0 is true.",
            "Multiple comparisons inflate Type I error without correction.",
            "Assumptions of normality or independence may be violated.",
            "Small sample sizes reduce test power and reliability.",
            "Effect sizes and confidence intervals may provide more informative insights."
        ],
        resolution_strategy=(
            "Use rigorous test design with clear hypotheses and assumptions. "
            "Apply corrections for multiple testing when applicable. "
            "Complement p-values with effect size and confidence intervals. "
            "Conduct power analysis to ensure adequate sample size. "
            "Validate findings through replication and robustness checks."
        ),
        entity_scope="Statistical inference on population parameters from sample data",
        confidence=0.93,
        confidence_zone="High confidence with proper test design and assumptions",
        controlling_precedent="Lehmann & Romano (2005), Chapters 1-3 on hypothesis testing framework"
    ),

    DoctrineBlock(
        topic="Differential Equations: Boundary and Initial Value Problems",
        keywords=["differential equations", "boundary value problem", "initial value problem", "existence", "uniqueness", "Laplace transform", "Fourier series", "sturm-liouville"],
        conclusion_template=(
            "Boundary and initial value problems specify conditions to uniquely determine solutions to differential equations. "
            "Existence and uniqueness theorems guarantee well-posedness under suitable conditions. "
            "Transform methods and eigenfunction expansions provide powerful solution techniques."
        ),
        reasoning_framework=(
            "Differential equations model dynamic systems, with initial value problems (IVPs) specifying solution values at a starting point, "
            "and boundary value problems (BVPs) imposing conditions at domain boundaries. "
            "The Picard-Lindelöf theorem ensures existence and uniqueness of solutions to IVPs under Lipschitz continuity of the right-hand side. "
            "BVPs often require self-adjoint operators and Sturm-Liouville theory to guarantee eigenfunction expansions and solution existence. "
            "Laplace transforms convert differential equations into algebraic equations in the complex domain, facilitating solution of linear ODEs with initial conditions. "
            "Fourier series expansions solve PDEs with periodic or fixed boundary conditions by decomposing functions into orthogonal basis functions. "
            "Green’s functions represent solutions to linear differential operators with delta-function sources, enabling integral solution representations. "
            "Well-posedness requires solutions to exist, be unique, and depend continuously on data, critical for physical applicability. "
            "Nonlinear differential equations may lack closed-form solutions, necessitating qualitative or numerical methods. "
            "Stability analysis of solutions involves eigenvalue spectra of linearized operators. "
            "Boundary conditions (Dirichlet, Neumann, Robin) influence solution behavior and physical interpretation. "
            "Overall, boundary and initial value problems form the framework for modeling and solving differential equations in science and engineering."
        ),
        key_factors=[
            "Type of differential equation (ODE vs PDE)",
            "Nature of boundary or initial conditions",
            "Existence and uniqueness theorems",
            "Transform and eigenfunction solution methods",
            "Well-posedness and stability"
        ],
        primary_authority=[
            "Coddington, E. A., & Levinson, N. (1955). Theory of Ordinary Differential Equations. McGraw-Hill.",
            "Evans, L. C. (2010). Partial Differential Equations. AMS.",
            "Boyce, W. E., & DiPrima, R. C. (2017). Elementary Differential Equations and Boundary Value Problems. Wiley.",
            "Zill, D. G. (2018). A First Course in Differential Equations with Modeling Applications. Cengage Learning.",
            "Teschl, G. (2012). Ordinary Differential Equations and Dynamical Systems. AMS."
        ],
        burden_holder="Solver or modeler proposing solution existence",
        adversary_position="Claims of non-existence, non-uniqueness, or ill-posedness",
        counter_arguments=[
            "Non-Lipschitz conditions may violate existence or uniqueness.",
            "Nonlinearities can cause multiple or no solutions.",
            "Improper boundary conditions may lead to ill-posed problems.",
            "Transform methods require linearity and suitable conditions.",
            "Numerical instability may arise without well-posedness."
        ],
        resolution_strategy=(
            "Verify Lipschitz and continuity conditions for IVPs. "
            "Apply Sturm-Liouville theory for BVP eigenfunction expansions. "
            "Use Laplace and Fourier transforms for linear problems. "
            "Check boundary condition compatibility and physical relevance. "
            "Employ numerical methods with stability and convergence analysis for complex problems."
        ),
        entity_scope="Ordinary and partial differential equations with specified boundary or initial conditions",
        confidence=0.94,
        confidence_zone="High confidence for linear well-posed problems; moderate for nonlinear or ill-posed",
        controlling_precedent="Coddington & Levinson (1955), Theorem 2.1 on existence and uniqueness; Evans (2010), Chapter 2 on PDE boundary problems"
    ),

    DoctrineBlock(
        topic="Number Theory: Prime Factorization and Modular Arithmetic",
        keywords=["prime factorization", "modular arithmetic", "congruence", "euclidean algorithm", "rsa cryptosystem", "gcd", "multiplicative inverse", "number theory"],
        conclusion_template=(
            "Prime factorization and modular arithmetic form the backbone of modern number theory and cryptography. "
            "Unique factorization into primes enables integer decomposition, while modular arithmetic facilitates computations in finite rings. "
            "Algorithms such as Euclidean algorithm and modular inverses underpin cryptographic protocols like RSA."
        ),
        reasoning_framework=(
            "Prime factorization states that every integer greater than 1 can be uniquely represented as a product of prime numbers, "
            "a fundamental theorem of arithmetic. This uniqueness is crucial for number theory and cryptographic security. "
            "Modular arithmetic studies equivalence classes of integers modulo n, forming finite rings ℤ/nℤ with addition and multiplication operations. "
            "Congruences express equivalence relations and enable solving linear and polynomial equations modulo n. "
            "The Euclidean algorithm efficiently computes the greatest common divisor (gcd) of two integers, essential for simplifying fractions and solving Diophantine equations. "
            "Extended Euclidean algorithm finds multiplicative inverses modulo n, critical for cryptographic key generation and modular division. "
            "The RSA cryptosystem relies on the difficulty of prime factorization of large composite numbers and modular exponentiation for secure encryption and decryption. "
            "Fermat's little theorem and Euler's theorem provide theoretical foundations for modular exponentiation properties. "
            "Chinese remainder theorem allows reconstruction of integers from their residues modulo pairwise coprime moduli, enabling parallel computations. "
            "Primality testing algorithms (e.g., Miller-Rabin) and factorization methods (e.g., Pollard's rho) balance efficiency and security considerations. "
            "Number theory's interplay with algebraic structures and computational complexity shapes modern cryptographic protocols and algorithms."
        ),
        key_factors=[
            "Unique prime factorization theorem",
            "Properties of modular arithmetic rings",
            "Euclidean and extended Euclidean algorithms",
            "Cryptographic applications (RSA)",
            "Theorems on modular exponentiation"
        ],
        primary_authority=[
            "Hardy, G. H., & Wright, E. M. (2008). An Introduction to the Theory of Numbers. Oxford University Press.",
            "Koblitz, N. (1994). A Course in Number Theory and Cryptography. Springer.",
            "Rosen, K. H. (2011). Elementary Number Theory and Its Applications. Pearson.",
            "Davenport, H. (2008). The Higher Arithmetic: An Introduction to the Theory of Numbers. Cambridge University Press.",
            "Silverman, J. H. (2006). A Friendly Introduction to Number Theory. Pearson."
        ],
        burden_holder="Proponent of factorization or modular arithmetic claims",
        adversary_position="Challenges on computational feasibility or uniqueness",
        counter_arguments=[
            "Prime factorization is computationally hard for large integers.",
            "Modular inverses do not exist if gcd is not 1.",
            "Certain moduli may not form fields, limiting invertibility.",
            "Probabilistic primality tests may yield false positives.",
            "Cryptographic security depends on unproven hardness assumptions."
        ],
        resolution_strategy=(
            "Use proven algorithms for gcd and modular inverses. "
            "Apply primality tests with error bounds. "
            "Restrict cryptographic keys to safe primes and large bit lengths. "
            "Leverage theoretical uniqueness of prime factorization. "
            "Incorporate complexity theory to assess computational hardness."
        ),
        entity_scope="Integers and modular arithmetic rings ℤ/nℤ",
        confidence=0.96,
        confidence_zone="High confidence in theoretical properties; practical limitations in computation",
        controlling_precedent="Hardy & Wright (2008), Theorem 31 on unique factorization; Koblitz (1994), Chapter 3 on modular arithmetic"
    ),

    DoctrineBlock(
        topic="Optimization: Linear Programming and Convexity",
        keywords=["linear programming", "convex optimization", "simplex method", "duality", "feasible region", "objective function", "convex set", "optimality conditions"],
        conclusion_template=(
            "Linear programming optimizes linear objective functions over convex polyhedral feasible regions. "
            "Convexity ensures global optima coincide with local optima, enabling efficient solution methods like the simplex and interior-point algorithms. "
            "Duality theory provides insights into solution structure and sensitivity."
        ),
        reasoning_framework=(
            "Linear programming (LP) involves maximizing or minimizing a linear objective function subject to linear equality and inequality constraints. "
            "The feasible region defined by these constraints is a convex polyhedron, a convex set where any line segment between two points lies entirely within the set. "
            "Convexity guarantees that any local optimum is a global optimum, simplifying optimization. "
            "The simplex method traverses vertices of the feasible polyhedron to find the optimal vertex, exploiting the polyhedral structure. "
            "Interior-point methods approach the optimum through the interior of the feasible region, offering polynomial time complexity. "
            "Duality theory associates every LP with a dual problem, where solutions provide bounds and economic interpretations of constraints. "
            "Strong duality holds under mild conditions, ensuring primal and dual optimal values coincide. "
            "Sensitivity analysis examines how changes in parameters affect the optimal solution, critical for real-world applications. "
            "Degeneracy and cycling can affect simplex convergence but are addressed by pivot rules and perturbation techniques. "
            "LP extends to convex optimization where objective and constraints are convex functions, broadening applicability. "
            "Applications span operations research, economics, engineering design, and machine learning. "
            "Theoretical foundations rely on convex analysis, linear algebra, and combinatorics."
        ),
        key_factors=[
            "Convexity of feasible region",
            "Linearity of objective and constraints",
            "Simplex and interior-point algorithms",
            "Duality and complementary slackness",
            "Sensitivity and stability analysis"
        ],
        primary_authority=[
            "Boyd, S., & Vandenberghe, L. (2004). Convex Optimization. Cambridge University Press.",
            "Chvátal, V. (1983). Linear Programming. W. H. Freeman.",
            "Bertsimas, D., & Tsitsiklis, J. N. (1997). Introduction to Linear Optimization. Athena Scientific.",
            "Dantzig, G. B. (1998). Linear Programming and Extensions. Princeton University Press.",
            "Nemirovski, A. (2005). Advances in Convex Optimization: Conic Programming. International Congress of Mathematicians."
        ],
        burden_holder="Optimizer proposing solution feasibility and optimality",
        adversary_position="Claims of non-convexity, infeasibility, or algorithmic failure",
        counter_arguments=[
            "Non-convex problems may have multiple local optima.",
            "Constraint sets may be empty or unbounded.",
            "Simplex method may cycle without pivot rules.",
            "Duality gap can exist in non-convex problems.",
            "Numerical instability affects large-scale problems."
        ],
        resolution_strategy=(
            "Verify convexity and feasibility conditions rigorously. "
            "Apply simplex or interior-point methods with safeguards. "
            "Use duality theory to confirm optimality and bounds. "
            "Perform sensitivity analysis to assess parameter impact. "
            "Employ numerical techniques to ensure stability and scalability."
        ),
        entity_scope="Optimization problems with linear or convex constraints and objectives",
        confidence=0.95,
        confidence_zone="High confidence in convex linear programming; moderate for non-convex extensions",
        controlling_precedent="Boyd & Vandenberghe (2004), Chapters 1-4 on convex sets and LP; Dantzig (1998) on simplex method"
    ),

    DoctrineBlock(
        topic="Numerical Methods: Root Finding Algorithms",
        keywords=["root finding", "numerical methods", "bisection method", "Newton-Raphson", "convergence", "fixed point iteration", "stability", "error analysis"],
        conclusion_template=(
            "Root finding algorithms numerically approximate zeros of functions, essential for solving nonlinear equations. "
            "Methods vary in convergence speed and stability, with trade-offs between robustness and efficiency. "
            "Error and convergence analyses guide method selection and implementation."
        ),
        reasoning_framework=(
            "Root finding is a fundamental numerical task to solve f(x) = 0 for nonlinear functions. "
            "The bisection method uses interval halving and the intermediate value theorem, guaranteeing convergence but with linear rate. "
            "Newton-Raphson method employs function derivatives to iteratively approximate roots, achieving quadratic convergence near simple roots. "
            "Fixed point iteration rewrites the root problem as x = g(x), iterating to convergence under contractive mappings. "
            "Convergence depends on initial guesses, function smoothness, and multiplicity of roots. "
            "Stability analysis examines sensitivity to perturbations and rounding errors. "
            "Error bounds quantify approximation accuracy at each iteration, informing stopping criteria. "
            "Hybrid methods combine robustness of bisection with speed of Newton-Raphson. "
            "Multiple roots and discontinuities complicate convergence and require modified algorithms. "
            "Computational cost and derivative availability influence method choice. "
            "Overall, root finding algorithms balance theoretical guarantees and practical considerations in numerical analysis."
        ),
        key_factors=[
            "Convergence rate and guarantees",
            "Initial guess and domain knowledge",
            "Function differentiability and smoothness",
            "Error and stability analysis",
            "Computational cost and complexity"
        ],
        primary_authority=[
            "Burden, R. L., & Faires, J. D. (2010). Numerical Analysis. Brooks/Cole.",
            "Atkinson, K. E. (1989). An Introduction to Numerical Analysis. Wiley.",
            "Kincaid, D., & Cheney, W. (2002). Numerical Analysis: Mathematics of Scientific Computing. Brooks/Cole.",
            "Stoer, J., & Bulirsch, R. (2002). Introduction to Numerical Analysis. Springer.",
            "Quarteroni, A., Sacco, R., & Saleri, F. (2007). Numerical Mathematics. Springer."
        ],
        burden_holder="Numerical analyst proposing root approximations",
        adversary_position="Concerns about convergence failure or instability",
        counter_arguments=[
            "Poor initial guesses can lead to divergence.",
            "Multiple roots reduce Newton-Raphson convergence order.",
            "Discontinuous or non-smooth functions violate assumptions.",
            "Rounding errors accumulate and affect stability.",
            "Derivative evaluation may be expensive or unavailable."
        ],
        resolution_strategy=(
            "Select methods based on function properties and available information. "
            "Use bracketing methods for guaranteed convergence when possible. "
            "Apply derivative-free methods or secant method when derivatives are unavailable. "
            "Incorporate error estimates and adaptive stopping criteria. "
            "Combine methods to leverage robustness and speed."
        ),
        entity_scope="Numerical approximation of roots for real-valued functions",
        confidence=0.92,
        confidence_zone="High confidence with appropriate method and conditions",
        controlling_precedent="Burden & Faires (2010), Chapters 2-3 on root finding methods and convergence"
    ),

    DoctrineBlock(
        topic="Probability: Central Limit Theorem",
        keywords=["central limit theorem", "probability distributions", "normal distribution", "independent identically distributed", "convergence in distribution", "law of large numbers", "variance", "sample mean"],
        conclusion_template=(
            "The Central Limit Theorem (CLT) states that the normalized sum of independent identically distributed random variables converges in distribution to a normal distribution. "
            "This theorem justifies the widespread use of normal approximations in statistics and probability."
        ),
        reasoning_framework=(
            "The Central Limit Theorem is a fundamental result in probability theory describing the asymptotic behavior of sums of random variables. "
            "Let X_1, X_2, ..., X_n be i.i.d. random variables with finite mean μ and variance σ^2. "
            "Define the sample mean S_n = (1/n) ∑_{i=1}^n X_i. "
            "The CLT states that the distribution of √n (S_n - μ) converges in distribution to a normal distribution N(0, σ^2) as n → ∞. "
            "This convergence is in the sense of distribution, meaning cumulative distribution functions converge at continuity points. "
            "The theorem holds under mild conditions, and variants exist for non-identically distributed or dependent variables (Lindeberg-Feller theorem). "
            "The CLT explains why normal distributions appear frequently in natural and social phenomena despite underlying distributions. "
            "It underpins inferential statistics, enabling confidence intervals and hypothesis tests based on sample means. "
            "The rate of convergence can be quantified by Berry-Esseen bounds, which depend on third moments. "
            "The theorem contrasts with the Law of Large Numbers, which guarantees convergence of sample means to the expectation but not distributional shape. "
            "Extensions include multivariate CLT and functional CLT (Donsker's theorem). "
            "Limitations arise when variables have infinite variance or strong dependence. "
            "Overall, the CLT provides a bridge between arbitrary distributions and the normal distribution in the limit."
        ),
        key_factors=[
            "Independence and identical distribution",
            "Finite mean and variance",
            "Normalization of sums",
            "Convergence in distribution",
            "Applicability to statistical inference"
        ],
        primary_authority=[
            "Billingsley, P. (1995). Probability and Measure. Wiley.",
            "Durrett, R. (2019). Probability: Theory and Examples. Cambridge University Press.",
            "Feller, W. (1971). An Introduction to Probability Theory and Its Applications, Vol. 2. Wiley.",
            "Gut, A. (2013). Probability: A Graduate Course. Springer.",
            "Chung, K. L. (2001). A Course in Probability Theory. Academic Press."
        ],
        burden_holder="Proponent of normal approximation claims",
        adversary_position="Concerns about violation of independence or moment conditions",
        counter_arguments=[
            "Dependence among variables invalidates classical CLT assumptions.",
            "Infinite variance variables do not satisfy CLT conditions.",
            "Non-identically distributed variables require generalized theorems.",
            "Finite sample sizes may yield poor normal approximations.",
            "Heavy-tailed distributions converge slowly or not at all."
        ],
        resolution_strategy=(
            "Verify independence and moment conditions rigorously. "
            "Apply generalized CLT variants for dependent or heterogeneous variables. "
            "Use Berry-Esseen bounds to assess approximation accuracy. "
            "Employ bootstrap or simulation methods for finite samples. "
            "Consider stable distributions for infinite variance cases."
        ),
        entity_scope="Sequences of random variables with specified distributional properties",
        confidence=0.98,
        confidence_zone="Very high confidence under classical assumptions",
        controlling_precedent="Feller (1971), Chapter XVI on Central Limit Theorem; Billingsley (1995), Theorem 27.2"
    ),

    DoctrineBlock(
        topic="Discrete Mathematics: Graph Theory Fundamentals",
        keywords=["graph theory", "vertices", "edges", "connectivity", "trees", "cycles", "planarity", "graph coloring"],
        conclusion_template=(
            "Graph theory studies discrete structures composed of vertices and edges, modeling relationships and connectivity. "
            "Fundamental concepts such as trees, cycles, and planarity underpin numerous applications in computer science and combinatorics."
        ),
        reasoning_framework=(
            "Graph theory formalizes the study of graphs G = (V, E), where V is a set of vertices and E a set of edges connecting pairs of vertices. "
            "Connectivity defines whether there exists a path between any two vertices, with connected graphs having a single connected component. "
            "Trees are connected acyclic graphs, characterized by |E| = |V| - 1, and serve as minimal spanning structures. "
            "Cycles are closed paths with no repeated vertices except start and end, important in detecting redundancy and feedback. "
            "Planarity determines if a graph can be drawn on a plane without edge crossings, characterized by Kuratowski's theorem. "
            "Graph coloring assigns labels (colors) to vertices such that adjacent vertices differ, with the chromatic number representing the minimum colors needed. "
            "Applications include network design, scheduling, and algorithm analysis. "
            "Eulerian and Hamiltonian paths analyze traversability properties. "
            "Graph invariants such as degree sequences, adjacency matrices, and eigenvalues provide structural insights. "
            "Algorithms for shortest paths (Dijkstra), maximum flow (Ford-Fulkerson), and matching (Hungarian) solve practical problems. "
            "Combinatorial enumeration counts distinct graphs or subgraphs under constraints. "
            "Graph minors and topological graph theory extend the field to complex structures. "
            "Overall, graph theory provides a rich framework for discrete mathematics and theoretical computer science."
        ),
        key_factors=[
            "Vertex and edge definitions",
            "Connectivity and components",
            "Tree and cycle characterization",
            "Planarity and Kuratowski's theorem",
            "Graph coloring and chromatic number"
        ],
        primary_authority=[
            "Diestel, R. (2017). Graph Theory. Springer.",
            "West, D. B. (2001). Introduction to Graph Theory. Prentice Hall.",
            "Bondy, J. A., & Murty, U. S. R. (2008). Graph Theory. Springer.",
            "Gross, J. L., & Yellen, J. (2005). Graph Theory and Its Applications. CRC Press.",
            "Chartrand, G., & Zhang, P. (2012). Introduction to Graph Theory. McGraw-Hill."
        ],
        burden_holder="Proponent of graph property claims",
        adversary_position="Challenges on connectivity, planarity, or coloring assertions",
        counter_arguments=[
            "Graphs may be disconnected or have multiple components.",
            "Non-planar graphs violate planar embedding claims.",
            "Coloring problems are NP-hard for general graphs.",
            "Cycles may exist contrary to tree claims.",
            "Algorithmic complexity limits practical computations."
        ],
        resolution_strategy=(
            "Apply formal definitions and theorems (e.g., Kuratowski) to verify planarity. "
            "Use connectivity algorithms (DFS, BFS) to assess components. "
            "Employ greedy or heuristic coloring algorithms with known bounds. "
            "Analyze cycle presence via graph traversal. "
            "Utilize efficient algorithms for special graph classes."
        ),
        entity_scope="Finite simple graphs and their properties",
        confidence=0.94,
        confidence_zone="High confidence in classical finite graph theory",
        controlling_precedent="Diestel (2017), Chapters 1-3 on graph basics and planarity; West (2001) on coloring"
    ),

    DoctrineBlock(
        topic="Topology: Compactness and Connectedness",
        keywords=["topology", "compactness", "connectedness", "open cover", "continuous functions", "Hausdorff space", "limit point", "subspace topology"],
        conclusion_template=(
            "Compactness and connectedness are fundamental topological properties influencing continuity and convergence. "
            "Compact spaces generalize finiteness, while connected spaces lack separation into disjoint open sets, shaping function behavior."
        ),
        reasoning_framework=(
            "Topology studies properties of spaces invariant under continuous deformations. "
            "Compactness is defined via the open cover property: a space is compact if every open cover has a finite subcover. "
            "This generalizes finiteness and ensures properties like sequential compactness and limit point compactness in metric spaces. "
            "Compactness is crucial for guaranteeing extrema of continuous functions (Extreme Value Theorem) and uniform continuity. "
            "Connectedness means a space cannot be partitioned into two nonempty disjoint open sets, indicating topological cohesion. "
            "Path-connectedness strengthens connectedness by requiring continuous paths between points. "
            "Hausdorff spaces separate points by neighborhoods, ensuring uniqueness of limits. "
            "Subspace topology inherits properties from ambient spaces, with compactness and connectedness preserved under closed subspaces. "
            "Tychonoff’s theorem states that arbitrary products of compact spaces are compact, a cornerstone of general topology. "
            "Applications span analysis, geometry, and dynamical systems, influencing continuity, convergence, and fixed point theorems. "
            "Counterexamples such as the topologist’s sine curve illustrate subtle distinctions between connectedness types. "
            "Overall, compactness and connectedness structure the qualitative behavior of topological spaces and continuous mappings."
        ),
        key_factors=[
            "Open cover definition of compactness",
            "Connectedness and path-connectedness",
            "Hausdorff separation axioms",
            "Preservation under subspaces and products",
            "Implications for continuous functions"
        ],
        primary_authority=[
            "Munkres, J. R. (2000). Topology. Prentice Hall.",
            "Willard, S. (2004). General Topology. Dover Publications.",
            "Kelley, J. L. (1955). General Topology. Springer.",
            "Engelking, R. (1989). General Topology. Heldermann Verlag.",
            "Simmons, G. F. (1963). Introduction to Topology and Modern Analysis. McGraw-Hill."
        ],
        burden_holder="Proponent of topological property claims",
        adversary_position="Challenges on compactness or connectedness assertions",
        counter_arguments=[
            "Spaces may fail to have finite subcovers for certain open covers.",
            "Disconnected spaces contradict connectedness claims.",
            "Non-Hausdorff spaces may have ambiguous limits.",
            "Products of non-compact spaces are not compact.",
            "Path-connectedness is stronger than connectedness and may fail."
        ],
        resolution_strategy=(
            "Use open cover arguments and subcover extraction for compactness. "
            "Apply separation axioms to verify Hausdorff property. "
            "Demonstrate connectedness via absence of clopen sets. "
            "Utilize Tychonoff’s theorem for product spaces. "
            "Distinguish between connectedness types with explicit examples."
        ),
        entity_scope="Topological spaces with specified separation and compactness properties",
        confidence=0.95,
        confidence_zone="High confidence in classical topology settings",
        controlling_precedent="Munkres (2000), Chapters 2-3 on compactness and connectedness; Willard (2004) on separation axioms"
    ),

    DoctrineBlock(
        topic="Abstract Algebra: Group Homomorphisms and Isomorphisms",
        keywords=["group", "homomorphism", "isomorphism", "kernel", "image", "normal subgroup", "first isomorphism theorem", "group theory"],
        conclusion_template=(
            "Group homomorphisms preserve algebraic structure between groups, with kernels and images characterizing their properties. "
            "Isomorphisms are bijective homomorphisms establishing group equivalence, foundational in algebraic classification."
        ),
        reasoning_framework=(
            "A group homomorphism φ: G → H is a function between groups preserving the group operation: φ(g₁g₂) = φ(g₁)φ(g₂). "
            "The kernel ker(φ) = {g ∈ G | φ(g) = e_H} is a normal subgroup of G, measuring the homomorphism’s failure to be injective. "
            "The image im(φ) = {h ∈ H | h = φ(g) for some g ∈ G} is a subgroup of H, representing the range of φ. "
            "The First Isomorphism Theorem states that G/ker(φ) ≅ im(φ), linking quotient groups and images. "
            "Isomorphisms are bijective homomorphisms, establishing structural equivalence between groups. "
            "Group homomorphisms enable classification of groups via invariants and factor groups. "
            "Normal subgroups are kernels of homomorphisms, essential for constructing quotient groups. "
            "Automorphisms are isomorphisms from a group to itself, forming the automorphism group Aut(G). "
            "Homomorphisms extend to rings, modules, and other algebraic structures with analogous properties. "
            "Understanding homomorphisms facilitates study of group actions, representations, and symmetry. "
            "Counterexamples include non-injective homomorphisms with nontrivial kernels and non-surjective homomorphisms. "
            "Overall, homomorphisms and isomorphisms are central to abstract algebra’s structural approach."
        ),
        key_factors=[
            "Definition and properties of homomorphisms",
            "Kernel as normal subgroup",
            "Image as subgroup",
            "First isomorphism theorem",
            "Isomorphism as bijective homomorphism"
        ],
        primary_authority=[
            "Dummit, D. S., & Foote, R. M. (2004). Abstract Algebra. Wiley.",
            "Herstein, I. N. (1996). Topics in Algebra. Wiley.",
            "Rotman, J. J. (2010). Advanced Modern Algebra. AMS.",
            "Lang, S. (2002). Algebra. Springer.",
            "Gallian, J. A. (2016). Contemporary Abstract Algebra. Cengage Learning."
        ],
        burden_holder="Proponent of homomorphism or isomorphism claims",
        adversary_position="Challenges on injectivity, surjectivity, or subgroup normality",
        counter_arguments=[
            "Nontrivial kernel implies non-injectivity.",
            "Image may not be the whole codomain, lacking surjectivity.",
            "Subgroups may fail to be normal, preventing quotient group formation.",
            "Isomorphism requires bijection, not guaranteed by homomorphism alone.",
            "Counterexamples exist for homomorphisms not preserving additional structure."
        ],
        resolution_strategy=(
            "Verify homomorphism properties explicitly. "
            "Determine kernel and test normality. "
            "Analyze image and codomain coverage. "
            "Apply first isomorphism theorem to relate quotient and image. "
            "Check bijectivity for isomorphism confirmation."
        ),
        entity_scope="Groups and group homomorphisms in abstract algebra",
        confidence=0.96,
        confidence_zone="High confidence in classical group theory",
        controlling_precedent="Dummit & Foote (2004), Theorem 3.1 on first isomorphism theorem"
    ),

    DoctrineBlock(
        topic="Complex Analysis: Cauchy Integral Theorem and Residue Calculus",
        keywords=["complex analysis", "Cauchy integral theorem", "holomorphic", "residue theorem", "contour integration", "analytic functions", "singularities", "Laurent series"],
        conclusion_template=(
            "The Cauchy Integral Theorem establishes that integrals of holomorphic functions over closed contours vanish, enabling powerful integral evaluations. "
            "Residue calculus extends this to compute integrals via singularity analysis, critical in complex function theory and applications."
        ),
        reasoning_framework=(
            "Complex analysis studies functions f: ℂ → ℂ that are holomorphic (complex differentiable) in open domains. "
            "The Cauchy Integral Theorem states that if f is holomorphic in a simply connected domain D, then the integral of f over any closed contour γ in D is zero: ∮_γ f(z) dz = 0. "
            "This theorem implies path independence of integrals and leads to Cauchy Integral Formula, expressing function values in terms of contour integrals. "
            "Singularities are points where f fails to be holomorphic; isolated singularities can be classified as removable, poles, or essential. "
            "Residue theorem generalizes Cauchy’s theorem, stating that ∮_γ f(z) dz = 2πi ∑ residues of f at singularities inside γ. "
            "Residues are coefficients of (z - z_0)^{-1} in the Laurent series expansion of f around singularity z_0. "
            "Residue calculus enables evaluation of real integrals, sums, and inverse Laplace transforms. "
            "Analytic continuation extends domains of holomorphic functions beyond initial regions. "
            "Morera’s theorem provides a converse to Cauchy’s theorem, characterizing holomorphicity via integral conditions. "
            "Applications include fluid dynamics, electromagnetic theory, and number theory (e.g., Riemann zeta function). "
            "Branch cuts and multi-valued functions require careful contour selection. "
            "Overall, Cauchy’s theorem and residue calculus form the backbone of complex function theory."
        ),
        key_factors=[
            "Holomorphicity and domain properties",
            "Closed contour integrals",
            "Classification of singularities",
            "Residue computation via Laurent series",
            "Applications to integral evaluation"
        ],
        primary_authority=[
            "Ahlfors, L. V. (1979). Complex Analysis. McGraw-Hill.",
            "Conway, J. B. (1978). Functions of One Complex Variable. Springer.",
            "Rudin, W. (1987). Real and Complex Analysis. McGraw-Hill.",
            "Stein, E. M., & Shakarchi, R. (2003). Complex Analysis. Princeton University Press.",
            "Lang, S. (1999). Complex Analysis. Springer."
        ],
        burden_holder="Proponent of contour integral evaluations",
        adversary_position="Concerns about domain holomorphicity or singularity classification",
        counter_arguments=[
            "Non-holomorphic points invalidate Cauchy’s theorem assumptions.",
            "Contours enclosing essential singularities complicate residue calculations.",
            "Branch points require careful contour deformation.",
            "Multi-valued functions need Riemann surface considerations.",
            "Improper contour choice leads to incorrect integral values."
        ],
        resolution_strategy=(
            "Verify holomorphicity and domain connectivity. "
            "Classify singularities and compute residues accurately. "
            "Select contours avoiding branch cuts and essential singularities. "
            "Use analytic continuation to extend function domains. "
            "Apply residue theorem to evaluate integrals rigorously."
        ),
        entity_scope="Holomorphic functions on complex domains and contour integrals",
        confidence=0.97,
        confidence_zone="Very high confidence in classical complex analysis",
        controlling_precedent="Ahlfors (1979), Theorems 4.1 and 5.1 on Cauchy and residue theorems"
    ),

    DoctrineBlock(
        topic="Real Analysis: Lebesgue Integration and Measure Theory",
        keywords=["Lebesgue integration", "measure theory", "sigma-algebra", "measurable functions", "null sets", "monotone convergence theorem", "dominated convergence theorem", "L^p spaces"],
        conclusion_template=(
            "Lebesgue integration extends classical integration by measuring function values over sets with respect to a measure, enabling integration of more general functions. "
            "Measure theory provides the rigorous foundation for this extension, facilitating convergence theorems and functional analysis."
        ),
        reasoning_framework=(
            "Measure theory formalizes the concept of size or volume of sets via sigma-algebras and measures, generalizing length and probability. "
            "A measure μ assigns non-negative extended real numbers to measurable sets, satisfying countable additivity. "
            "Lebesgue integration integrates functions with respect to a measure, allowing integration of functions with discontinuities or unbounded variation. "
            "Measurable functions are those compatible with the sigma-algebra structure, ensuring well-defined integrals. "
            "Null sets (measure zero) enable ignoring pathological subsets in integration and convergence. "
            "Monotone Convergence Theorem states that increasing sequences of non-negative measurable functions converge integrals to the integral of the limit. "
            "Dominated Convergence Theorem allows interchange of limit and integral under domination by an integrable function, critical for analysis. "
            "L^p spaces consist of measurable functions whose p-th power is integrable, forming Banach spaces fundamental in functional analysis. "
            "Lebesgue integration surpasses Riemann integration in handling limits, convergence, and function classes. "
            "Applications include probability theory, harmonic analysis, and PDEs. "
            "Carathéodory’s extension theorem constructs measures from outer measures, underpinning measure construction. "
            "Overall, Lebesgue integration and measure theory provide a robust framework for modern analysis."
        ),
        key_factors=[
            "Sigma-algebra and measurable sets",
            "Countable additivity of measures",
            "Measurable functions and integrability",
            "Convergence theorems (monotone, dominated)",
            "L^p space structure and completeness"
        ],
        primary_authority=[
            "Folland, G. B. (1999). Real Analysis: Modern Techniques and Their Applications. Wiley.",
            "Royden, H. L., & Fitzpatrick, P. M. (2010). Real Analysis. Pearson.",
            "Halmos, P. R. (1974). Measure Theory. Springer.",
            "Stein, E. M., & Shakarchi, R. (2005). Real Analysis: Measure Theory, Integration, and Hilbert Spaces. Princeton University Press.",
            "Cohn, D. L. (2013). Measure Theory. Birkhäuser."
        ],
        burden_holder="Proponent of integrability and measure claims",
        adversary_position="Challenges on measurability, convergence, or null set treatment",
        counter_arguments=[
            "Functions may fail to be measurable, invalidating integrals.",
            "Dominated convergence conditions may not hold.",
            "Null sets can be non-intuitive and affect limits.",
            "Sigma-algebras may be improperly defined or incomplete.",
            "L^p spaces require completeness and norm properties."
        ],
        resolution_strategy=(
            "Verify sigma-algebra and measure properties rigorously. "
            "Establish function measurability and integrability. "
            "Apply monotone and dominated convergence theorems carefully. "
            "Use null sets to handle exceptional cases. "
            "Confirm L^p space axioms and completeness."
        ),
        entity_scope="Measurable functions and measures on sigma-algebras",
        confidence=0.96,
        confidence_zone="High confidence in classical measure theory and Lebesgue integration",
        controlling_precedent="Folland (1999), Chapters 1-3 on measure and integration; Royden & Fitzpatrick (2010) on convergence theorems"
    ),

    DoctrineBlock(
        topic="Functional Analysis: Hilbert and Banach Spaces",
        keywords=["functional analysis", "Hilbert space", "Banach space", "normed vector space", "inner product", "bounded operator", "spectral theorem", "completeness"],
        conclusion_template=(
            "Hilbert and Banach spaces provide abstract frameworks for infinite-dimensional vector spaces with norms or inner products. "
            "These structures enable analysis of operators, convergence, and spectral properties fundamental in mathematics and physics."
        ),
        reasoning_framework=(
            "Functional analysis studies vector spaces with additional structure and continuous linear operators acting on them. "
            "A Banach space is a complete normed vector space, meaning every Cauchy sequence converges in the norm topology. "
            "Hilbert spaces are Banach spaces equipped with an inner product inducing the norm, enabling geometric notions like orthogonality and projections. "
            "Completeness ensures limits of sequences exist within the space, critical for analysis and PDE solutions. "
            "Bounded linear operators between Banach or Hilbert spaces generalize matrices to infinite dimensions, with operator norms measuring size. "
            "The spectral theorem characterizes normal operators on Hilbert spaces via spectral measures, extending eigenvalue decompositions. "
            "Riesz representation theorem identifies Hilbert space duals with the space itself, simplifying functional analysis. "
            "Applications include quantum mechanics, signal processing, and PDE theory. "
            "Compact operators generalize finite-rank operators and have discrete spectra. "
            "Dual spaces and weak topologies enrich the structure and enable variational methods. "
            "Functional analysis bridges algebra, topology, and analysis in infinite-dimensional contexts."
        ),
        key_factors=[
            "Completeness of normed spaces",
            "Inner product structure in Hilbert spaces",
            "Bounded linear operators and norms",
            "Spectral theorem for normal operators",
            "Duality and weak topologies"
        ],
        primary_authority=[
            "Rudin, W. (1991). Functional Analysis. McGraw-Hill.",
            "Conway, J. B. (1990). A Course in Functional Analysis. Springer.",
            "Lax, P. D. (2002). Functional Analysis. Wiley-Interscience.",
            "Kreyszig, E. (1989). Introductory Functional Analysis with Applications. Wiley.",
            "Yosida, K. (1995). Functional Analysis. Springer."
        ],
        burden_holder="Proponent of operator and space property claims",
        adversary_position="Challenges on completeness, boundedness, or spectral properties",
        counter_arguments=[
            "Spaces may be incomplete or lack inner products.",
            "Operators may be unbounded or not densely defined.",
            "Spectral theorem applies only to normal operators.",
            "Dual spaces can be complicated or non-separable.",
            "Weak topologies differ from norm topologies, affecting convergence."
        ],
        resolution_strategy=(
            "Verify completeness and norm definitions. "
            "Confirm inner product axioms for Hilbert spaces. "
            "Establish boundedness and domain of operators. "
            "Apply spectral theorem conditions carefully. "
            "Use duality and weak topology theory appropriately."
        ),
        entity_scope="Infinite-dimensional normed and inner product spaces",
        confidence=0.95,
        confidence_zone="High confidence in classical functional analysis",
        controlling_precedent="Rudin (1991), Chapters 1-7 on Banach and Hilbert spaces and operators"
    ),

    DoctrineBlock(
        topic="Mathematical Logic: Completeness of Predicate Logic",
        keywords=["mathematical logic", "predicate logic", "completeness theorem", "soundness", "first-order logic", "Gödel's completeness theorem", "model theory", "proof theory"],
        conclusion_template=(
            "Gödel's completeness theorem establishes that every logically valid formula in first-order predicate logic is provable in a formal system. "
            "This result bridges semantic truth and syntactic provability, foundational in logic and model theory."
        ),
        reasoning_framework=(
            "Mathematical logic formalizes reasoning through formal languages, syntax, and semantics. "
            "First-order predicate logic extends propositional logic with quantifiers and variables over domains. "
            "Soundness ensures that any formula provable in a formal system is logically valid (true in all models). "
            "Gödel's completeness theorem (1930) states the converse: any logically valid formula is provable, establishing equivalence of semantic truth and syntactic derivability. "
            "Proof involves constructing a model from consistent sets of formulas (Henkin construction) and demonstrating satisfaction. "
            "Completeness contrasts with Gödel's incompleteness theorems, which apply to sufficiently expressive arithmetic systems, not pure first-order logic. "
            "Compactness theorem follows from completeness, stating that if every finite subset of a set of formulas is satisfiable, then the whole set is satisfiable. "
            "Completeness enables model-theoretic methods and automated theorem proving. "
            "Limitations include undecidability and incompleteness in richer logical systems. "
            "Proof theory studies formal derivations and proof transformations, complementing model theory. "
            "Overall, completeness theorem is a cornerstone of mathematical logic, linking syntax and semantics rigorously."
        ),
        key_factors=[
            "Soundness and completeness definitions",
            "First-order logic syntax and semantics",
            "Henkin model construction",
            "Compactness theorem implications",
            "Distinction from incompleteness theorems"
        ],
        primary_authority=[
            "Enderton, H. B. (2001). A Mathematical Introduction to Logic. Academic Press.",
            "Hodges, W. (1997). A Shorter Model Theory. Cambridge University Press.",
            "Chang, C. C., & Keisler, H. J. (1990). Model Theory. Elsevier.",
            "Shoenfield, J. R. (2001). Mathematical Logic. Association for Symbolic Logic.",
            "Smullyan, R. M. (1995). First-Order Logic. Dover Publications."
        ],
        burden_holder="Proponent of formula provability claims",
        adversary_position="Challenges on validity or proof existence",
        counter_arguments=[
            "Some formulas may be true in some models but not all (invalid).",
            "Proof systems may be incomplete for higher-order logics.",
            "Undecidability limits algorithmic proof search.",
            "Incompleteness theorems restrict arithmetic theories.",
            "Semantic truth may be non-constructive."
        ],
        resolution_strategy=(
            "Apply Gödel's completeness theorem for first-order logic. "
            "Use Henkin constructions to build models for consistent sets. "
            "Distinguish between first-order and higher-order logic contexts. "
            "Leverage compactness and Löwenheim-Skolem theorems. "
            "Employ proof assistants and automated reasoning tools."
        ),
        entity_scope="First-order predicate logic and formal proof systems",
        confidence=0.98,
        confidence_zone="Very high confidence in classical first-order logic",
        controlling_precedent="Gödel (1930), Completeness theorem; Enderton (2001), Chapters 9-10 on completeness and compactness"
    ),

    DoctrineBlock(
        topic="Category Theory: Functors and Natural Transformations",
        keywords=["category theory", "functor", "natural transformation", "objects", "morphisms", "commutative diagrams", "adjunction", "equivalence of categories"],
        conclusion_template=(
            "Functors map categories preserving structure, while natural transformations provide morphisms between functors, enabling comparison of categorical constructions. "
            "These concepts form the language for abstract mathematical structures and their relationships."
        ),
        reasoning_framework=(
            "Category theory abstracts mathematical structures as categories consisting of objects and morphisms satisfying composition and identity axioms. "
            "A functor F: C → D maps objects of category C to objects of D and morphisms to morphisms, preserving composition and identities. "
            "Functors enable translation of problems and structures between categories, generalizing homomorphisms and continuous maps. "
            "Natural transformations η: F ⇒ G between functors F, G: C → D assign to each object X in C a morphism η_X: F(X) → G(X) in D, satisfying naturality conditions expressed by commutative diagrams. "
            "Natural transformations capture the notion of morphisms between functors, allowing comparison and equivalence of categorical constructions. "
            "Adjunctions are pairs of functors related by natural isomorphisms of hom-sets, generalizing universal properties and dualities. "
            "Equivalence of categories occurs when functors form an adjoint equivalence, preserving categorical structure up to isomorphism. "
            "Category theory provides unifying language across algebra, topology, logic, and computer science. "
            "Limits, colimits, and representable functors extend the framework to constructions and universal properties. "
            "Yoneda lemma characterizes functors via natural transformations, foundational in the theory. "
            "Overall, functors and natural transformations enable abstraction and transfer of mathematical ideas."
        ),
        key_factors=[
            "Definition and properties of functors",
            "Natural transformations and naturality squares",
            "Adjunctions and universal properties",
            "Equivalence and isomorphism of categories",
            "Applications in diverse mathematical fields"
        ],
        primary_authority=[
            "Mac Lane, S. (1998). Categories for the Working Mathematician. Springer.",
            "Awodey, S. (2010). Category Theory. Oxford University Press.",
            "Leinster, T. (2014). Basic Category Theory. Cambridge University Press.",
            "Borceux, F. (1994). Handbook of Categorical Algebra. Cambridge University Press.",
            "Barr, M., & Wells, C. (1990). Category Theory for Computing Science. Prentice Hall."
        ],
        burden_holder="Proponent of categorical structure claims",
        adversary_position="Challenges on functoriality or naturality conditions",
        counter_arguments=[
            "Functors may fail to preserve composition or identities.",
            "Natural transformations may not satisfy commutativity.",
            "Adjunctions require specific hom-set isomorphisms.",
            "Equivalence of categories is weaker than isomorphism.",
            "Complexity of categorical constructions may obscure intuition."
        ],
        resolution_strategy=(
            "Verify functor axioms explicitly. "
            "Check naturality conditions via commutative diagrams. "
            "Establish adjunctions through hom-set isomorphisms. "
            "Distinguish equivalence from isomorphism carefully. "
            "Use examples and counterexamples to clarify concepts."
        ),
        entity_scope="Categories, functors, and natural transformations in abstract mathematics",
        confidence=0.95,
        confidence_zone="High confidence in standard category theory",
        controlling_precedent="Mac Lane (1998), Chapters 1-3 on functors and natural transformations"
    ),

    DoctrineBlock(
        topic="Dynamical Systems: Chaos and Lyapunov Stability",
        keywords=["dynamical systems", "chaos", "bifurcation", "Lyapunov stability", "attractor", "sensitivity to initial conditions", "nonlinear systems", "phase space"],
        conclusion_template=(
            "Chaos theory studies complex dynamical behavior characterized by sensitivity to initial conditions and fractal attractors. "
            "Lyapunov stability analyzes the response of systems to perturbations, classifying equilibria and long-term behavior."
        ),
        reasoning_framework=(
            "Dynamical systems describe evolution of states over time via differential or difference equations. "
            "Chaos refers to deterministic yet unpredictable behavior arising in nonlinear systems, characterized by sensitive dependence on initial conditions. "
            "Lyapunov exponents quantify rates of divergence or convergence of nearby trajectories, with positive exponents indicating chaos. "
            "Lyapunov stability classifies equilibria as stable, asymptotically stable, or unstable based on response to small perturbations. "
            "Bifurcation theory studies qualitative changes in system behavior as parameters vary, leading to phenomena like period doubling and chaos onset. "
            "Attractors are sets toward which trajectories evolve, including fixed points, limit cycles, and strange attractors with fractal structure. "
            "Phase space provides geometric visualization of system states and trajectories. "
            "Poincaré maps reduce continuous dynamics to discrete iterations for analysis. "
            "Nonlinear dynamics often defy closed-form solutions, necessitating numerical simulation and qualitative methods. "
            "Applications span physics, biology, economics, and engineering, modeling complex temporal patterns. "
            "Stability analysis uses Lyapunov functions to prove stability without explicit solutions. "
            "Overall, dynamical systems theory elucidates order and disorder in time-evolving systems."
        ),
        key_factors=[
            "Nonlinearity and system equations",
            "Lyapunov exponents and functions",
            "Bifurcation and parameter dependence",
            "Attractors and phase space structure",
            "Sensitivity and unpredictability"
        ],
        primary_authority=[
            "Strogatz, S. H. (2018). Nonlinear Dynamics and Chaos. Westview Press.",
            "Guckenheimer, J., & Holmes, P. (1983). Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields. Springer.",
            "Ott, E. (2002). Chaos in Dynamical Systems. Cambridge University Press.",
            "Khalil, H. K. (2002). Nonlinear Systems. Prentice Hall.",
            "Hirsch, M. W., Smale, S., & Devaney, R. L. (2012). Differential Equations, Dynamical Systems, and an Introduction to Chaos. Academic Press."
        ],
        burden_holder="Proponent of system stability or chaos claims",
        adversary_position="Challenges on stability proofs or chaotic behavior",
        counter_arguments=[
            "Linearization may fail to capture nonlinear stability.",
            "Numerical simulations can be sensitive to errors.",
            "Lyapunov functions may be difficult to construct.",
            "Chaos complicates long-term prediction.",
            "Bifurcations may be subtle or hard to detect."
        ],
        resolution_strategy=(
            "Use Lyapunov functions and exponents for stability analysis. "
            "Perform bifurcation analysis to understand parameter effects. "
            "Employ rigorous numerical methods with error control. "
            "Analyze attractors and phase space geometry. "
            "Combine theoretical and computational approaches."
        ),
        entity_scope="Nonlinear dynamical systems and stability theory",
        confidence=0.93,
        confidence_zone="High confidence with rigorous analysis and simulations",
        controlling_precedent="Strogatz (2018), Chapters 2-5 on stability and chaos; Guckenheimer & Holmes (1983) on bifurcations"
    ),

    DoctrineBlock(
        topic="Information Theory: Entropy and Mutual Information",
        keywords=["information theory", "entropy", "mutual information", "Shannon entropy", "Kullback-Leibler divergence", "channel capacity", "data compression", "information gain"],
        conclusion_template=(
            "Entropy quantifies uncertainty in random variables, forming the basis of information theory. "
            "Mutual information measures shared information between variables, fundamental in communication and learning."
        ),
        reasoning_framework=(
            "Information theory quantifies information content and transmission efficiency in probabilistic systems. "
            "Shannon entropy H(X) measures the expected uncertainty of a discrete random variable X: H(X) = -∑ p(x) log p(x). "
            "Entropy is maximized for uniform distributions and minimized for deterministic variables. "
            "Mutual information I(X;Y) quantifies the reduction in uncertainty of X given knowledge of Y, defined as I(X;Y) = H(X) - H(X|Y). "
            "Kullback-Leibler divergence measures difference between probability distributions, underpinning relative entropy concepts. "
            "Channel capacity defines the maximum reliable communication rate over noisy channels, derived from mutual information maximization. "
            "Entropy underlies data compression algorithms by characterizing minimal expected code length. "
            "Information gain guides feature selection and learning in machine learning. "
            "The chain rule decomposes joint entropy into conditional entropies, facilitating analysis of complex systems. "
            "Entropy and mutual information extend to continuous variables via differential entropy with subtleties. "
            "Applications span telecommunications, cryptography, statistics, and neuroscience. "
            "Overall, entropy and mutual information provide rigorous measures of information and uncertainty."
        ),
        key_factors=[
            "Definition and properties of Shannon entropy",
            "Mutual information and conditional entropy",
            "Kullback-Leibler divergence",
            "Channel capacity and coding theorems",
            "Applications in compression and learning"
        ],
        primary_authority=[
            "Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory. Wiley.",
            "MacKay, D. J. C. (2003). Information Theory, Inference, and Learning Algorithms. Cambridge University Press.",
            "Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.",
            "Csiszár, I., & Körner, J. (2011). Information Theory: Coding Theorems for Discrete Memoryless Systems. Cambridge University Press.",
            "Gray, R. M. (2011). Entropy and Information Theory. Springer."
        ],
        burden_holder="Proponent of information measure claims",
        adversary_position="Challenges on measure definitions or applicability",
        counter_arguments=[
            "Differential entropy can be negative or non-intuitive.",
            "Mutual information estimation is challenging for continuous variables.",
            "Kullback-Leibler divergence is not symmetric.",
            "Channel capacity depends on channel assumptions and noise models.",
            "Entropy measures may not capture semantic information."
        ],
        resolution_strategy=(
            "Use discrete entropy definitions where applicable. "
            "Apply estimation techniques and bounds for continuous variables. "
            "Interpret divergences carefully considering asymmetry. "
            "Model channels accurately for capacity calculations. "
            "Complement entropy with other information measures as needed."
        ),
        entity_scope="Random variables and communication channels",
        confidence=0.96,
        confidence_zone="High confidence in classical information theory",
        controlling_precedent="Cover & Thomas (2006), Chapters 2-7 on entropy and mutual information"
    ),

    DoctrineBlock(
        topic="Cryptography: RSA Algorithm and Modular Exponentiation",
        keywords=["cryptography", "RSA algorithm", "modular exponentiation", "public key", "private key", "prime factorization", "encryption", "decryption"],
        conclusion_template=(
            "The RSA algorithm employs modular exponentiation and prime factorization hardness to enable secure public-key encryption. "
            "Key generation, encryption, and decryption rely on number theoretic properties ensuring confidentiality."
        ),
        reasoning_framework=(
            "RSA is a widely used asymmetric cryptographic algorithm based on number theory. "
            "Key generation involves selecting two large primes p and q, computing n = pq and Euler’s totient φ(n) = (p-1)(q-1). "
            "A public exponent e is chosen coprime to φ(n), and the private exponent d satisfies ed ≡ 1 (mod φ(n)). "
            "Encryption of message m is c ≡ m^e (mod n), and decryption is m ≡ c^d (mod n). "
            "Security relies on the computational difficulty of factoring large integers n to retrieve p and q, which would reveal d. "
            "Modular exponentiation is efficiently computed via repeated squaring algorithms. "
            "Padding schemes (e.g., OAEP) prevent deterministic encryption vulnerabilities. "
            "Mathematical proofs ensure correctness of encryption and decryption under modular arithmetic. "
            "Attacks include factorization algorithms (e.g., quadratic sieve, general number field sieve) and side-channel analysis. "
            "Key sizes must be sufficiently large (2048 bits or more) to maintain security. "
            "RSA underpins digital signatures, secure key exchange, and confidentiality in communications. "
            "Overall, RSA exemplifies the application of number theory to practical cryptography."
        ),
        key_factors=[
            "Prime selection and key generation",
            "Modular exponentiation correctness",
            "Hardness of prime factorization",
            "Padding and security enhancements",
            "Computational efficiency and attacks"
        ],
        primary_authority=[
            "Rivest, R. L., Shamir, A., & Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. Communications of the ACM.",
            "Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (1996). Handbook of Applied Cryptography. CRC Press.",
            "Koblitz, N. (1994). A Course in Number Theory and Cryptography. Springer.",
            "Boneh, D. (1999). Twenty Years of Attacks on the RSA Cryptosystem. Notices of the AMS.",
            "Stinson, D. R. (2005). Cryptography: Theory and Practice. CRC Press."
        ],
        burden_holder="Proponent of RSA security and correctness",
        adversary_position="Challenges on factorization hardness or implementation vulnerabilities",
        counter_arguments=[
            "Advances in factorization algorithms threaten RSA security.",
            "Poor random prime generation compromises keys.",
            "Side-channel attacks leak private key information.",
            "Deterministic encryption without padding is insecure.",
            "Quantum computing poses future risks to RSA."
        ],
        resolution_strategy=(
            "Use sufficiently large and random primes. "
            "Implement secure padding schemes. "
            "Employ side-channel resistant hardware and software. "
            "Monitor advances in factorization and quantum algorithms. "
            "Transition to post-quantum cryptographic schemes as needed."
        ),
        entity_scope="Public-key cryptography using modular arithmetic",
        confidence=0.94,
        confidence_zone="High confidence with proper implementation and key sizes",
        controlling_precedent="Rivest, Shamir & Adleman (1978), foundational RSA paper; Menezes et al. (1996) on cryptographic standards"
    ),

    DoctrineBlock(
        topic="Machine Learning: Gradient Descent and Backpropagation",
        keywords=["machine learning", "gradient descent", "backpropagation", "optimization", "neural networks", "loss function", "stochastic gradient descent", "regularization"],
        conclusion_template=(
            "Gradient descent optimizes model parameters by iteratively minimizing loss functions. "
            "Backpropagation efficiently computes gradients in neural networks, enabling scalable training."
        ),
        reasoning_framework=(
            "Machine learning models are trained by minimizing loss functions measuring prediction error. "
            "Gradient descent updates parameters in the direction of negative gradient of the loss, iteratively approaching minima. "
            "Variants include batch, stochastic, and mini-batch gradient descent, balancing convergence speed and noise. "
            "Backpropagation applies chain rule of calculus to compute gradients of loss with respect to network weights efficiently. "
            "This enables training of deep neural networks by propagating errors backward from output to input layers. "
            "Learning rates control step sizes; adaptive methods (Adam, RMSProp) adjust learning rates dynamically. "
            "Regularization techniques (L1, L2, dropout) prevent overfitting by constraining model complexity. "
            "Convergence depends on loss surface smoothness, initialization, and hyperparameters. "
            "Gradient vanishing and exploding gradients challenge deep network training, addressed by normalization and architecture design. "
            "Optimization landscapes may contain local minima and saddle points, influencing training dynamics. "
            "Overall, gradient descent and backpropagation are foundational algorithms in supervised learning."
        ),
        key_factors=[
            "Loss function differentiability",
            "Gradient computation via chain rule",
            "Learning rate and optimization variants",
            "Regularization to prevent overfitting",
            "Convergence and stability considerations"
        ],
        primary_authority=[
            "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.",
            "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer.",
            "Nocedal, J., & Wright, S. J. (2006). Numerical Optimization. Springer.",
            "Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning Representations by Back-Propagating Errors. Nature.",
            "LeCun, Y., Bottou, L., Orr, G. B., & Müller, K. R. (2012). Efficient BackProp. In Neural Networks: Tricks of the Trade."
        ],
        burden_holder="Proponent of model training and convergence claims",
        adversary_position="Challenges on gradient computation or optimization efficacy",
        counter_arguments=[
            "Non-convex loss surfaces complicate convergence guarantees.",
            "Poorly chosen learning rates cause divergence or slow training.",
            "Backpropagation requires differentiable activation functions.",
            "Overfitting reduces generalization without regularization.",
            "Gradient vanishing/exploding impede deep network training without skip connections or normalization.",
        ],
        resolution_strategy="Apply rigorous gradient computation with automatic differentiation, use adaptive optimizers (Adam, RMSProp), employ batch normalization and residual connections for deep networks",
        entity_scope="Machine learning and deep learning optimization",
        confidence=0.93,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Rumelhart, Hinton, Williams 1986 — Backpropagation Learning Procedure",
    ),
]

# =============================================================
# SUB-ENGINE ORCHESTRATION
# =============================================================

ENGINE_IDS = [
    "MATH01", "MATH02", "MATH03", "MATH04", "MATH05", "MATH06",
    "MATH07", "MATH08", "MATH09", "MATH10", "MATH11", "MATH12"
]

ENGINE_URLS = {
    "MATH01": "http://math01.local/api",
    "MATH02": "http://math02.local/api",
    "MATH03": "http://math03.local/api",
    "MATH04": "http://math04.local/api",
    "MATH05": "http://math05.local/api",
    "MATH06": "http://math06.local/api",
    "MATH07": "http://math07.local/api",
    "MATH08": "http://math08.local/api",
    "MATH09": "http://math09.local/api",
    "MATH10": "http://math10.local/api",
    "MATH11": "http://math11.local/api",
    "MATH12": "http://math12.local/api",
}

ENGINE_KEYWORDS = {
    "MATH01": ["matrix", "vector", "eigenvalue", "eigenvector", "linear", "determinant", "rank", "system of equations"],
    "MATH02": ["derivative", "integral", "limit", "calculus", "differentiation", "integration"],
    "MATH03": ["mean", "variance", "standard deviation", "statistics", "distribution", "regression"],
    "MATH04": ["differential equation", "ode", "pde", "laplace", "fourier", "boundary value"],
    "MATH05": ["prime", "modular", "number theory", "gcd", "lcm", "integer", "diophantine"],
    "MATH06": ["optimization", "minimize", "maximize", "objective", "gradient", "convex", "linear programming"],
    "MATH07": ["numerical", "approximation", "error", "iteration", "finite difference", "simulation"],
    "MATH08": ["probability", "random", "stochastic", "bayes", "event", "distribution"],
    "MATH09": ["graph", "combinatorics", "discrete", "logic", "set", "algorithm"],
    "MATH10": ["topology", "open set", "closed set", "manifold", "homeomorphism", "continuity"],
    "MATH11": ["group", "ring", "field", "abstract algebra", "homomorphism", "isomorphism"],
    "MATH12": ["complex", "analytic", "holomorphic", "conformal", "residue", "contour"],
}

ENGINE_PRIORITY = {
    "MATH01": 1,
    "MATH02": 1,
    "MATH03": 1,
    "MATH04": 1,
    "MATH05": 1,
    "MATH06": 1,
    "MATH07": 1,
    "MATH08": 1,
    "MATH09": 1,
    "MATH10": 1,
    "MATH11": 1,
    "MATH12": 1,
}

ENGINE_FALLBACKS = {
    "MATH01": ["MATH02", "MATH07"],
    "MATH02": ["MATH01", "MATH07"],
    "MATH03": ["MATH08", "MATH09"],
    "MATH04": ["MATH01", "MATH07"],
    "MATH05": ["MATH09", "MATH11"],
    "MATH06": ["MATH07", "MATH01"],
    "MATH07": ["MATH06", "MATH01"],
    "MATH08": ["MATH03", "MATH09"],
    "MATH09": ["MATH05", "MATH03"],
    "MATH10": ["MATH11", "MATH01"],
    "MATH11": ["MATH10", "MATH05"],
    "MATH12": ["MATH02", "MATH01"],
}

# --- Enums and Data Classes ---

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
    LINEAR_ALGEBRA = auto()
    CALCULUS = auto()
    STATISTICS = auto()
    DIFF_EQUATIONS = auto()
    NUMBER_THEORY = auto()
    OPTIMIZATION = auto()
    NUMERICAL_METHODS = auto()
    PROBABILITY = auto()
    DISCRETE_MATH = auto()
    TOPOLOGY = auto()
    ABSTRACT_ALGEBRA = auto()
    COMPLEX_ANALYSIS = auto()
    OTHER = auto()

class RoutingMode(Enum):
    PARALLEL = auto()
    CASCADE = auto()
    SINGLE = auto()

class QueryRequest:
    def __init__(self, text: str, mode: RoutingMode = RoutingMode.PARALLEL, meta: Optional[Dict[str, Any]] = None):
        self.text = text
        self.mode = mode
        self.meta = meta or {}

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, priority: int):
        self.engine_id = engine_id
        self.url = url
        self.priority = priority

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 5, recovery_timeout: int = 30, half_open_success_threshold: int = 2):
        self.engine_id = engine_id
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_success_threshold = half_open_success_threshold
        self.half_open_success_count = 0

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.state == CircuitBreakerState.CLOSED and self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def record_success(self):
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_success_count += 1
            if self.half_open_success_count >= self.half_open_success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.half_open_success_count = 0
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0

    def check_state(self):
        if self.state == CircuitBreakerState.OPEN:
            if self.last_failure_time and (time.time() - self.last_failure_time) >= self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_success_count = 0
        return self.state

    def allow_request(self):
        self.check_state()
        return self.state in [CircuitBreakerState.CLOSED, CircuitBreakerState.HALF_OPEN]

    def reset(self):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.half_open_success_count = 0
        self.last_failure_time = None

# --- SubEngine Health Monitor ---

class SubEngineHealthMonitor:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self._health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self._circuit_breakers: Dict[str, CircuitBreaker] = {eid: CircuitBreaker(eid) for eid in ENGINE_IDS}

    async def _ping_engine(self, url: str, timeout: int = 3) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
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
        if engine_id in self._health_cache:
            status, ts = self._health_cache[engine_id]
            if now - ts < self.ttl:
                return status
        url = ENGINE_URLS.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(url)
        self._health_cache[engine_id] = (status, now)
        cb = self._circuit_breakers[engine_id]
        if status == SubEngineStatus.HEALTHY:
            cb.record_success()
        else:
            cb.record_failure()
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = [self.check_health(eid) for eid in ENGINE_IDS]
        statuses = await asyncio.gather(*tasks)
        for eid, status in zip(ENGINE_IDS, statuses):
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        now = time.time()
        healthy = []
        for eid in ENGINE_IDS:
            cb = self._circuit_breakers[eid]
            if not cb.allow_request():
                continue
            if eid in self._health_cache:
                status, ts = self._health_cache[eid]
                if now - ts < self.ttl and status == SubEngineStatus.HEALTHY:
                    healthy.append(eid)
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self._circuit_breakers[engine_id]

    def reset_health_cache(self):
        self._health_cache.clear()

# --- Query Router ---

class QueryRouter:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched = []
        for eid, keywords in ENGINE_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    matched.append(eid)
                    break
        categories = []
        for eid in matched:
            if eid == "MATH01":
                categories.append(IssueCategory.LINEAR_ALGEBRA)
            elif eid == "MATH02":
                categories.append(IssueCategory.CALCULUS)
            elif eid == "MATH03":
                categories.append(IssueCategory.STATISTICS)
            elif eid == "MATH04":
                categories.append(IssueCategory.DIFF_EQUATIONS)
            elif eid == "MATH05":
                categories.append(IssueCategory.NUMBER_THEORY)
            elif eid == "MATH06":
                categories.append(IssueCategory.OPTIMIZATION)
            elif eid == "MATH07":
                categories.append(IssueCategory.NUMERICAL_METHODS)
            elif eid == "MATH08":
                categories.append(IssueCategory.PROBABILITY)
            elif eid == "MATH09":
                categories.append(IssueCategory.DISCRETE_MATH)
            elif eid == "MATH10":
                categories.append(IssueCategory.TOPOLOGY)
            elif eid == "MATH11":
                categories.append(IssueCategory.ABSTRACT_ALGEBRA)
            elif eid == "MATH12":
                categories.append(IssueCategory.COMPLEX_ANALYSIS)
        if not categories:
            categories.append(IssueCategory.OTHER)
        return categories

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        healthy = self.health_monitor.get_healthy_engines()
        selected = []
        for cat in categories:
            if cat == IssueCategory.LINEAR_ALGEBRA and "MATH01" in healthy:
                selected.append(SubEngineConfig("MATH01", ENGINE_URLS["MATH01"], ENGINE_PRIORITY["MATH01"]))
            elif cat == IssueCategory.CALCULUS and "MATH02" in healthy:
                selected.append(SubEngineConfig("MATH02", ENGINE_URLS["MATH02"], ENGINE_PRIORITY["MATH02"]))
            elif cat == IssueCategory.STATISTICS and "MATH03" in healthy:
                selected.append(SubEngineConfig("MATH03", ENGINE_URLS["MATH03"], ENGINE_PRIORITY["MATH03"]))
            elif cat == IssueCategory.DIFF_EQUATIONS and "MATH04" in healthy:
                selected.append(SubEngineConfig("MATH04", ENGINE_URLS["MATH04"], ENGINE_PRIORITY["MATH04"]))
            elif cat == IssueCategory.NUMBER_THEORY and "MATH05" in healthy:
                selected.append(SubEngineConfig("MATH05", ENGINE_URLS["MATH05"], ENGINE_PRIORITY["MATH05"]))
            elif cat == IssueCategory.OPTIMIZATION and "MATH06" in healthy:
                selected.append(SubEngineConfig("MATH06", ENGINE_URLS["MATH06"], ENGINE_PRIORITY["MATH06"]))
            elif cat == IssueCategory.NUMERICAL_METHODS and "MATH07" in healthy:
                selected.append(SubEngineConfig("MATH07", ENGINE_URLS["MATH07"], ENGINE_PRIORITY["MATH07"]))
            elif cat == IssueCategory.PROBABILITY and "MATH08" in healthy:
                selected.append(SubEngineConfig("MATH08", ENGINE_URLS["MATH08"], ENGINE_PRIORITY["MATH08"]))
            elif cat == IssueCategory.DISCRETE_MATH and "MATH09" in healthy:
                selected.append(SubEngineConfig("MATH09", ENGINE_URLS["MATH09"], ENGINE_PRIORITY["MATH09"]))
            elif cat == IssueCategory.TOPOLOGY and "MATH10" in healthy:
                selected.append(SubEngineConfig("MATH10", ENGINE_URLS["MATH10"], ENGINE_PRIORITY["MATH10"]))
            elif cat == IssueCategory.ABSTRACT_ALGEBRA and "MATH11" in healthy:
                selected.append(SubEngineConfig("MATH11", ENGINE_URLS["MATH11"], ENGINE_PRIORITY["MATH11"]))
            elif cat == IssueCategory.COMPLEX_ANALYSIS and "MATH12" in healthy:
                selected.append(SubEngineConfig("MATH12", ENGINE_URLS["MATH12"], ENGINE_PRIORITY["MATH12"]))
        if not selected and IssueCategory.OTHER in categories:
            # Fallback: send to all healthy engines
            selected = [SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_PRIORITY[eid]) for eid in healthy]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: if meta specifies preferred engine, use it
        preferred = query.meta.get("preferred_engine")
        if preferred and preferred in ENGINE_IDS:
            return [preferred]
        # Example: if query is urgent, use parallel mode
        if query.meta.get("urgent"):
            return self.health_monitor.get_healthy_engines()
        # Default: use domain classification
        categories = self._classify_domain(query.text)
        configs = self._select_engines(categories, query.mode)
        return [cfg.engine_id for cfg in configs]

    def _score_engine_relevance(self, engine: str, query: QueryRequest) -> float:
        # Score based on keyword overlap and engine health
        text_lower = query.text.lower()
        keywords = ENGINE_KEYWORDS.get(engine, [])
        overlap = sum(1 for kw in keywords if kw in text_lower)
        cb = self.health_monitor.get_circuit_breaker(engine)
        health_score = 1.0 if cb.allow_request() else 0.0
        return overlap * health_score

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # Fallback strategy: use fallback engines if available
        fallbacks = ENGINE_FALLBACKS.get(engine_id, [])
        healthy = self.health_monitor.get_healthy_engines()
        fallback_engines = [eid for eid in fallbacks if eid in healthy]
        if not fallback_engines:
            # If no fallbacks, use any healthy engine except failed one
            fallback_engines = [eid for eid in healthy if eid != engine_id]
        return fallback_engines

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        engines = self._apply_routing_rules(query)
        return RoutingDecision(engines, categories, query.mode)

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor, router: QueryRouter):
        self.health_monitor = health_monitor
        self.router = router

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> Dict[str, Any]:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.allow_request():
            return {"engine_id": engine_config.engine_id, "error": "circuit_open", "response": None}
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"query": query.text, "meta": query.meta}
                async with session.post(engine_config.url + "/query", json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.record_success()
                        return {"engine_id": engine_config.engine_id, "response": data}
                    else:
                        cb.record_failure()
                        return {"engine_id": engine_config.engine_id, "error": f"status_{resp.status}", "response": None}
        except Exception as e:
            cb.record_failure()
            return {"engine_id": engine_config.engine_id, "error": str(e), "response": None}

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[Dict[str, Any]]:
        tasks = [self._call_sub_engine(cfg, query) for cfg in engines]
        responses = await asyncio.gather(*tasks)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        responses = await self.dispatch_query(query, engines)
        merged = self._merge_responses(responses)
        return merged

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        for cfg in engines:
            resp = await self._call_sub_engine(cfg, query)
            if resp.get("response") is not None:
                return resp["response"]
        return {"error": "all_engines_failed"}

    def _merge_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        merged = {"responses": [], "errors": []}
        for resp in responses:
            if resp.get("response") is not None:
                merged["responses"].append(resp["response"])
            else:
                merged["errors"].append({"engine_id": resp["engine_id"], "error": resp.get("error")})
        return merged

    def _resolve_conflicts(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Consensus: majority vote or most confident response
        valid_resps = [resp["response"] for resp in responses if resp.get("response") is not None]
        if not valid_resps:
            return {"error": "no_valid_responses"}
        # Example: if all responses are similar, return one; else, aggregate
        # For demonstration, just return the first
        return valid_resps[0]

# --- Example Integration ---

class MathematicsIntelligenceEngineOrchestrator:
    def __init__(self):
        self.health_monitor = SubEngineHealthMonitor()
        self.router = QueryRouter(self.health_monitor)
        self.orchestrator = SubEngineOrchestrator(self.health_monitor, self.router)

    async def handle_query(self, query: QueryRequest) -> Dict[str, Any]:
        routing_decision = self.router.route_query(query)
        engines = [SubEngineConfig(eid, ENGINE_URLS[eid], ENGINE_PRIORITY[eid]) for eid in routing_decision.engines]
        if routing_decision.mode == RoutingMode.PARALLEL:
            result = await self.orchestrator.dispatch_parallel(query, engines)
        elif routing_decision.mode == RoutingMode.CASCADE:
            result = await self.orchestrator.dispatch_cascade(query, engines)
        else:
            responses = await self.orchestrator.dispatch_query(query, engines)
            result = self.orchestrator._resolve_conflicts(responses)
        return result

    async def monitor_sub_engines(self):
        return await self.health_monitor.check_all_health()

    def get_healthy_engines(self):
        return self.health_monitor.get_healthy_engines()

    def reset_health_cache(self):
        self.health_monitor.reset_health_cache()

# --- Utility for Testing ---

async def main():
    orchestrator = MathematicsIntelligenceEngineOrchestrator()
    query = QueryRequest(
        text="Find the eigenvalues of the following matrix and discuss its determinant.",
        mode=RoutingMode.PARALLEL
    )
    response = await orchestrator.handle_query(query)
    print("Unified Response:", response)
    health = await orchestrator.monitor_sub_engines()
    print("Sub-engine Health:", health)
    print("Healthy Engines:", orchestrator.get_healthy_engines())

# Uncomment below to run test
# asyncio.run(main())

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 40,
    AuthorityLevel.PRACTICE: 20,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, return the dominant authority level based on weights.
    If multiple with same weight, return the one with highest enum value (most specific).
    """
    if not sources:
        raise ValueError("No authority sources provided")
    max_weight = -1
    candidates = []
    for src in sources:
        w = authority_weights.get(src, 0)
        if w > max_weight:
            max_weight = w
            candidates = [src]
        elif w == max_weight:
            candidates.append(src)
    # tie-break by enum value descending
    dominant = max(candidates, key=lambda x: x.value)
    return dominant

# ---------------------------
# EPISTEMIC GUARDRAILS
# ---------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "self-evident",
    "indisputably", "categorically", "incontestably", "unequivocally", "irrefutably",
    "decidedly", "conclusively", "absolutely", "definitely", "beyond any doubt",
    "plainly", "evidently", "manifestly", "inarguably", "without question",
    "infallibly", "incontestably", "undoubtedly", "positively", "assuredly",
    "beyond peradventure", "without reservation"
]

BANNED_PHRASES_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(phrase) for phrase in BANNED_PHRASES) + r')\b',
    flags=re.IGNORECASE
)

class ConfidenceLevel(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

def apply_epistemic_guardrails(text: str) -> Tuple[str, str]:
    """
    Remove banned phrases from text and append a disclosure caveat.
    Returns cleaned text and disclosure caveat string.
    """
    cleaned = BANNED_PHRASES_PATTERN.sub("", text)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
    disclosure_caveat = ("Note: This analysis avoids absolute or overly confident language "
                         "to maintain epistemic humility and guard against overstatement.")
    return cleaned, disclosure_caveat

def confidence_stratification(confidence_score: float) -> ConfidenceLevel:
    """
    Stratify confidence score (0.0 to 1.0) into confidence levels.
    """
    if confidence_score >= 0.85:
        return ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.4:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK

# ---------------------------
# DEEP ANALYSIS
# ---------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and logical splits.
    """
    # Example simplistic decomposition based on conjunctions and doctrine keywords
    doctrine_keywords = [
        "integral", "derivative", "limit", "continuity", "differentiability",
        "convergence", "series", "matrix", "vector", "algebra", "topology",
        "probability", "statistics", "optimization", "geometry", "number theory"
    ]
    # Split on common conjunctions and punctuation
    split_pattern = re.compile(r'[;,.]| and | or | but ')
    parts = [p.strip() for p in split_pattern.split(query) if p.strip()]
    sub_issues = []
    for part in parts:
        # Check if any doctrine keyword appears
        if any(kw in part.lower() for kw in doctrine_keywords):
            sub_issues.append(part)
    if not sub_issues:
        # fallback: whole query as single issue
        sub_issues = [query.strip()]
    return sub_issues

def build_interaction_dag(issues: List[str]) -> Dict[str, Set[str]]:
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume issues that mention other issues' keywords depend on them.
    """
    dag = {issue: set() for issue in issues}
    keywords_map = {}
    for issue in issues:
        words = set(re.findall(r'\b\w+\b', issue.lower()))
        keywords_map[issue] = words

    for issue_a in issues:
        for issue_b in issues:
            if issue_a == issue_b:
                continue
            # If issue_a's keywords intersect with issue_b's keywords, issue_a depends on issue_b
            if keywords_map[issue_a] & keywords_map[issue_b]:
                # To avoid cycles, only add edge if issue_b appears before issue_a lex order
                if issue_b < issue_a:
                    dag[issue_a].add(issue_b)
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform a full eight-step analysis:
    1. Issue identification
    2. Rule statement
    3. Application
    4. Counterarguments
    5. Synthesis
    6. Conclusion
    7. Confidence assessment
    8. Recommendations
    """
    analysis = {}

    # 1. Issue identification
    analysis['issues'] = doctrines

    # 2. Rule statement (simplified)
    analysis['rules'] = {d: f"Rule statement for {d}" for d in doctrines}

    # 3. Application (use sub_engine_results)
    analysis['applications'] = {}
    for d in doctrines:
        result = sub_engine_results.get(d, {})
        analysis['applications'][d] = result.get('analysis', f"Application analysis for {d}")

    # 4. Counterarguments (mocked)
    analysis['counterarguments'] = {d: f"Potential counterarguments for {d}" for d in doctrines}

    # 5. Synthesis (combine applications and counterarguments)
    synthesis = []
    for d in doctrines:
        synth = f"Synthesis for {d}: {analysis['applications'][d]} vs {analysis['counterarguments'][d]}"
        synthesis.append(synth)
    analysis['synthesis'] = synthesis

    # 6. Conclusion (mocked)
    analysis['conclusion'] = f"Overall conclusion for query: {query}"

    # 7. Confidence assessment (mocked average)
    confidence_scores = [0.8 for _ in doctrines]  # placeholder
    avg_confidence = sum(confidence_scores) / max(len(confidence_scores), 1)
    analysis['confidence_level'] = confidence_stratification(avg_confidence)

    # 8. Recommendations (mocked)
    analysis['recommendations'] = "Recommendations based on analysis and confidence level."

    return analysis

def zoned_analysis(conclusion: str) -> Dict[str, str]:
    """
    Tag conclusion with zones: PLANNING, REPORTING, AUDIT.
    For demonstration, assign tags based on keywords.
    """
    zones = {}
    if any(word in conclusion.lower() for word in ['plan', 'strategy', 'prepare']):
        zones['PLANNING'] = conclusion
    if any(word in conclusion.lower() for word in ['report', 'summary', 'findings']):
        zones['REPORTING'] = conclusion
    if any(word in conclusion.lower() for word in ['audit', 'review', 'verification']):
        zones['AUDIT'] = conclusion
    if not zones:
        zones['REPORTING'] = conclusion  # default zone
    return zones

# ---------------------------
# FACT FRAGILITY SCORING
# ---------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility on:
    - verifiability (0.0-1.0)
    - recharacterization risk (0.0-1.0)
    - testimony dependence (0.0-1.0)
    """
    # Simplistic heuristics:
    verifiability = 0.5
    recharacterization_risk = 0.5
    testimony_dependence = 0.5

    # Verifiability: facts with numbers or references score higher
    if re.search(r'\b\d+(\.\d+)?\b', fact):
        verifiability += 0.3
    if re.search(r'\b(source|reference|citation|document)\b', fact, re.I):
        verifiability += 0.2
    verifiability = min(verifiability, 1.0)

    # Recharacterization risk: vague or subjective words increase risk
    vague_words = ['some', 'many', 'few', 'often', 'likely', 'possible', 'approximate']
    if any(w in fact.lower() for w in vague_words):
        recharacterization_risk += 0.3
    recharacterization_risk = min(recharacterization_risk, 1.0)

    # Testimony dependence: presence of personal pronouns or quotes increases dependence
    if re.search(r'\b(I|we|he|she|they|said|stated|claimed)\b', fact, re.I):
        testimony_dependence += 0.3
    testimony_dependence = min(testimony_dependence, 1.0)

    return {
        'verifiability': verifiability,
        'recharacterization_risk': recharacterization_risk,
        'testimony_dependence': testimony_dependence
    }

# ---------------------------
# SEMANTIC NORMALIZATION
# ---------------------------

DOMAIN_TERM_MAPPINGS = {
    # 50+ domain term mappings for mathematics domain
    "diff": "derivative",
    "deriv": "derivative",
    "integrate": "integral",
    "int": "integral",
    "lim": "limit",
    "cont": "continuity",
    "diffable": "differentiability",
    "conv": "convergence",
    "series": "series",
    "matrix": "matrix",
    "vec": "vector",
    "algebraic": "algebra",
    "topo": "topology",
    "prob": "probability",
    "stat": "statistics",
    "opt": "optimization",
    "geom": "geometry",
    "numtheory": "number theory",
    "calc": "calculus",
    "lin alg": "linear algebra",
    "lin algebra": "linear algebra",
    "func": "function",
    "funcs": "function",
    "func'n": "function",
    "funcs'": "function",
    "derivative": "derivative",
    "integral": "integral",
    "limit": "limit",
    "continuous": "continuity",
    "differentiable": "differentiability",
    "convergent": "convergence",
    "series": "series",
    "matrix": "matrix",
    "vector": "vector",
    "algebra": "algebra",
    "topology": "topology",
    "probability": "probability",
    "statistics": "statistics",
    "optimization": "optimization",
    "geometry": "geometry",
    "number theory": "number theory",
    "calculus": "calculus",
    "linear algebra": "linear algebra",
    "function": "function",
    "functions": "function",
    "derivatives": "derivative",
    "integrals": "integral",
    "limits": "limit",
    "continuity": "continuity",
    "differentiability": "differentiability",
    "convergence": "convergence",
    "series": "series",
    "matrices": "matrix",
    "vectors": "vector",
    "algebras": "algebra",
    "topologies": "topology",
    "probabilities": "probability",
    "statistics": "statistics",
    "optimizations": "optimization",
    "geometries": "geometry",
    "number theories": "number theory",
    "calculi": "calculus",
    "linear algebras": "linear algebra",
    "funcs": "function",
    "funcs'": "function",
    "func'n": "function",
    "diffs": "derivative",
    "ints": "integral",
    "lims": "limit",
    "conts": "continuity",
    "diffs": "differentiability",
    "convs": "convergence",
    "series": "series",
    "matrices": "matrix",
    "vecs": "vector",
    "algs": "algebra",
    "topos": "topology",
    "probs": "probability",
    "stats": "statistics",
    "opts": "optimization",
    "geoms": "geometry",
    "numtheories": "number theory",
}

def normalize_query(text: str) -> str:
    """
    Normalize query text by replacing domain terms with standardized terms.
    """
    lowered = text.lower()
    # Sort keys by length descending to replace longest first
    sorted_keys = sorted(DOMAIN_TERM_MAPPINGS.keys(), key=len, reverse=True)
    for key in sorted_keys:
        pattern = re.compile(r'\b' + re.escape(key) + r'\b', re.IGNORECASE)
        lowered = pattern.sub(DOMAIN_TERM_MAPPINGS[key], lowered)
    return lowered

# ---------------------------
# THREE LAYER RESPONSE SYSTEM
# ---------------------------

class DoctrineCache:
    """
    Simple in-memory doctrine cache with keyword matching.
    """
    def __init__(self):
        self.cache = {}  # key: frozenset(keywords), value: cached analysis

    def lookup(self, query: str, timeout_ms: int = 200) -> Optional[str]:
        """
        Lookup cache for matching keywords within timeout.
        Return cached analysis if found else None.
        """
        start = time.time()
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        for key_keywords, cached_analysis in self.cache.items():
            if time.time() - start > timeout_ms / 1000:
                break
            if key_keywords & query_words:
                return cached_analysis
        return None

    def add(self, keywords: Set[str], analysis: str):
        self.cache[frozenset(keywords)] = analysis

doctrine_cache = DoctrineCache()

class SubEngineRouter:
    """
    Routes queries to relevant sub-engines based on semantic similarity.
    """
    def __init__(self):
        # Map sub-engine names to keywords sets
        self.sub_engines = {
            "CalculusEngine": {"derivative", "integral", "limit", "continuity", "differentiability", "calculus"},
            "AlgebraEngine": {"matrix", "vector", "algebra", "linear algebra"},
            "TopologyEngine": {"topology"},
            "ProbabilityEngine": {"probability", "statistics"},
            "OptimizationEngine": {"optimization"},
            "GeometryEngine": {"geometry"},
            "NumberTheoryEngine": {"number theory"},
            "SeriesEngine": {"series", "convergence"},
        }

    def route(self, query: str) -> List[str]:
        """
        Return list of sub-engine names relevant to query.
        """
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        matched_engines = []
        for engine, keywords in self.sub_engines.items():
            if query_words & keywords:
                matched_engines.append(engine)
        if not matched_engines:
            # fallback to generic engine
            matched_engines.append("GeneralMathEngine")
        return matched_engines

sub_engine_router = SubEngineRouter()

class SubEngineSimulator:
    """
    Simulates sub-engine processing.
    """
    def __init__(self):
        pass

    def analyze(self, engine_name: str, query: str) -> Dict[str, Any]:
        """
        Simulate analysis by sub-engine.
        """
        # Simulate some processing delay
        time.sleep(0.05)
        # Return mock analysis
        return {
            "engine": engine_name,
            "query": query,
            "analysis": f"Analysis result from {engine_name} for query segment.",
            "confidence": 0.75,
            "authority_sources": [AuthorityLevel.STATUTORY, AuthorityLevel.CASE_LAW]
        }

sub_engine_simulator = SubEngineSimulator()

def merge_sub_engine_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge results from multiple sub-engines.
    Resolve conflicts in authority sources.
    """
    merged = {
        "analyses": [],
        "authority_sources": [],
        "confidence_scores": [],
    }
    for res in results:
        merged["analyses"].append(res.get("analysis", ""))
        merged["authority_sources"].extend(res.get("authority_sources", []))
        merged["confidence_scores"].append(res.get("confidence", 0.0))
    # Resolve authority conflicts
    dominant_authority = resolve_authority_conflict(merged["authority_sources"]) if merged["authority_sources"] else None
    avg_confidence = sum(merged["confidence_scores"]) / max(len(merged["confidence_scores"]), 1)
    merged_result = {
        "merged_analysis": " | ".join(merged["analyses"]),
        "dominant_authority": dominant_authority,
        "average_confidence": avg_confidence
    }
    return merged_result

def three_layer_response(query: str) -> Dict[str, Any]:
    """
    Three-layer response system:
    Layer 1: Doctrine cache lookup (0-200ms)
    Layer 2: Semantic search + sub-engine routing
    Layer 3: Deep multi-engine analysis (parallel dispatch, merge, resolve conflicts)
    """
    # Normalize query
    normalized_query = normalize_query(query)

    # Layer 1: Doctrine cache lookup
    cached = doctrine_cache.lookup(normalized_query, timeout_ms=200)
    if cached:
        return {"layer": 1, "result": cached}

    # Layer 2: Semantic search + sub-engine routing
    sub_engines = sub_engine_router.route(normalized_query)
    if len(sub_engines) == 1:
        # Single sub-engine, dispatch and return
        result = sub_engine_simulator.analyze(sub_engines[0], normalized_query)
        # Cache result
        doctrine_cache.add(set(re.findall(r'\b\w+\b', normalized_query)), result["analysis"])
        return {"layer": 2, "result": result}

    # Layer 3: Deep multi-engine analysis
    # Decompose query into sub-issues
    doctrines = multi_doctrine_decomposition(normalized_query)
    # Build interaction DAG
    dag = build_interaction_dag(doctrines)

    # Dispatch to sub-engines in parallel for each doctrine
    sub_engine_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sub_engines)) as executor:
        futures = {}
        for doctrine in doctrines:
            # Route sub-engines for doctrine
            engines_for_doctrine = sub_engine_router.route(doctrine)
            # For simplicity, pick first engine
            engine = engines_for_doctrine[0]
            futures[executor.submit(sub_engine_simulator.analyze, engine, doctrine)] = doctrine
        for future in concurrent.futures.as_completed(futures):
            doctrine = futures[future]
            try:
                result = future.result()
                sub_engine_results[doctrine] = result
            except Exception:
                sub_engine_results[doctrine] = {"analysis": "Error in sub-engine analysis", "confidence": 0.0, "authority_sources": []}

    # Merge sub-engine results
    merged = merge_sub_engine_results(list(sub_engine_results.values()))

    # Perform eight-step resolution
    full_analysis = eight_step_resolution(normalized_query, doctrines, sub_engine_results)

    # Apply epistemic guardrails on conclusion
    cleaned_conclusion, caveat = apply_epistemic_guardrails(full_analysis.get('conclusion', ''))
    full_analysis['conclusion_cleaned'] = cleaned_conclusion
    full_analysis['disclosure_caveat'] = caveat

    # Zoned analysis tagging
    zones = zoned_analysis(cleaned_conclusion)
    full_analysis['zones'] = zones

    # Cache the merged analysis for future
    doctrine_cache.add(set(re.findall(r'\b\w+\b', normalized_query)), merged["merged_analysis"])

    return {
        "layer": 3,
        "merged_result": merged,
        "full_analysis": full_analysis
    }

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
        self.telemetry_records: List[QueryTelemetry] = []
        self.errors: List[Dict[str, Any]] = []
        self.engine_stats: Dict[str, Counter] = defaultdict(Counter)
        self.doctrine_hits: Counter = Counter()
        self.doctrine_total: Counter = Counter()
        self.query_times: deque = deque()
        self.latencies: List[float] = []
        self.last_hour_queries: deque = deque()
        self.sub_engine_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: defaultdict(int))

    def record_query(self, telemetry: QueryTelemetry):
        with self.lock:
            self.telemetry_records.append(telemetry)
            self.latencies.append(telemetry.latency_ms)
            self.query_times.append((telemetry.timestamp, telemetry.query_id))
            self.last_hour_queries.append((telemetry.timestamp, telemetry.query_id))
            for engine in telemetry.engines_invoked:
                self.engine_stats[engine]['invoked'] += 1
                if telemetry.error:
                    self.engine_stats[engine]['errors'] += 1
                self.sub_engine_stats[engine]['latencies'].append(telemetry.latency_ms)
                self.sub_engine_stats[engine]['errors'] += int(bool(telemetry.error))
                self.sub_engine_stats[engine]['availability'] += 1
            if telemetry.cache_hit:
                self.doctrine_hits[telemetry.mode] += 1
            self.doctrine_total[telemetry.mode] += 1

    def record_error(self, query_id: str, error: str, timestamp: Optional[float] = None):
        with self.lock:
            self.errors.append({
                'query_id': query_id,
                'error': error,
                'timestamp': timestamp or time.time()
            })

    def get_latency_stats(self):
        with self.lock:
            latencies = sorted(self.latencies)
            n = len(latencies)
            if n == 0:
                return {}
            def percentile(p):
                idx = int(p * n)
                idx = min(idx, n - 1)
                return latencies[idx]
            return {
                'avg': sum(latencies) / n,
                'p50': percentile(0.5),
                'p95': percentile(0.95),
                'p99': percentile(0.99),
                'min': latencies[0],
                'max': latencies[-1]
            }

    def get_doctrine_hit_rate(self):
        with self.lock:
            rates = {}
            for doctrine in self.doctrine_total:
                total = self.doctrine_total[doctrine]
                hits = self.doctrine_hits[doctrine]
                rates[doctrine] = hits / total if total else 0.0
            return rates

    def queries_last_hour(self):
        cutoff = time.time() - 3600
        with self.lock:
            while self.last_hour_queries and self.last_hour_queries[0][0] < cutoff:
                self.last_hour_queries.popleft()
            return [qid for ts, qid in self.last_hour_queries]

    def get_sub_engine_stats(self):
        with self.lock:
            stats = {}
            for engine, data in self.sub_engine_stats.items():
                latencies = data.get('latencies', [])
                n = len(latencies)
                stats[engine] = {
                    'avg_latency': sum(latencies) / n if n else None,
                    'error_rate': data['errors'] / data['availability'] if data['availability'] else 0.0,
                    'availability': data['availability'],
                    'invoked': self.engine_stats[engine]['invoked'],
                    'errors': self.engine_stats[engine]['errors']
                }
            return stats

# --- DRIFT WATCHER ---

class DriftWatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.baselines: Dict[str, List[float]] = defaultdict(list)
        self.confidence_history: Dict[str, List[float]] = defaultdict(list)
        self.drift_alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self.lock:
            self.baselines[doctrine].append(confidence)
            self.confidence_history[doctrine].append(confidence)

    def detect_drift(self, doctrine: str, new_confidence: float):
        with self.lock:
            self.confidence_history[doctrine].append(new_confidence)
            baseline = self.baselines[doctrine]
            if not baseline:
                return False
            avg_baseline = sum(baseline) / len(baseline)
            drift = abs(new_confidence - avg_baseline) / avg_baseline if avg_baseline else 0.0
            if drift > 0.10:  # >10% shift
                alert = {
                    'doctrine': doctrine,
                    'baseline': avg_baseline,
                    'new_confidence': new_confidence,
                    'drift_percent': drift * 100,
                    'timestamp': time.time()
                }
                self.drift_alerts.append(alert)
                return True
            return False

    def get_drift_report(self):
        with self.lock:
            report = {}
            for doctrine, history in self.confidence_history.items():
                baseline = self.baselines[doctrine]
                avg_baseline = sum(baseline) / len(baseline) if baseline else None
                avg_current = sum(history[-10:]) / min(len(history), 10) if history else None
                drift = None
                if avg_baseline and avg_current:
                    drift = abs(avg_current - avg_baseline) / avg_baseline
                report[doctrine] = {
                    'avg_baseline': avg_baseline,
                    'avg_current': avg_current,
                    'drift_percent': drift * 100 if drift is not None else None,
                    'alerts': [a for a in self.drift_alerts if a['doctrine'] == doctrine]
                }
            return report

# --- COVERAGE MAP ---

class CoverageTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.triggered_doctrines: Counter = Counter()
        self.missed_queries: List[Dict[str, Any]] = []
        self.epistemic_gaps: List[Dict[str, Any]] = []
        self.sub_engine_coverage: Dict[str, Counter] = defaultdict(Counter)

    def record_triggered(self, doctrine: str, query_id: str, sub_engine: Optional[str] = None):
        with self.lock:
            self.triggered_doctrines[doctrine] += 1
            if sub_engine:
                self.sub_engine_coverage[sub_engine][doctrine] += 1

    def record_missed(self, query_id: str, query: Any):
        with self.lock:
            self.missed_queries.append({'query_id': query_id, 'query': query})

    def record_epistemic_gap(self, query_id: str, query: Any):
        with self.lock:
            self.epistemic_gaps.append({'query_id': query_id, 'query': query})

    def get_coverage_report(self):
        with self.lock:
            report = {
                'doctrine_coverage': dict(self.triggered_doctrines),
                'missed_queries': len(self.missed_queries),
                'epistemic_gaps': len(self.epistemic_gaps),
                'sub_engine_coverage': {
                    engine: dict(counter)
                    for engine, counter in self.sub_engine_coverage.items()
                }
            }
            return report

    def identify_epistemic_gap(self, query: Any, doctrines: List[str]):
        # If query matches no doctrines, record epistemic gap
        if not doctrines:
            self.record_epistemic_gap(query.get('query_id', 'unknown'), query)

# --- DETERMINISM HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    query_bytes = json.dumps(query, sort_keys=True).encode('utf-8')
    response_bytes = json.dumps(response, sort_keys=True).encode('utf-8')
    m = hashlib.sha256()
    m.update(query_bytes)
    m.update(response_bytes)
    return m.hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash

# --- AUDIT TRAIL ---

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self.lock = threading.Lock()
        self.current_date = datetime.date.today()
        self.file_handle = self._open_file(self.current_date)
        self.file_path = self._get_file_path(self.current_date)

    def _get_file_path(self, date: datetime.date) -> str:
        return os.path.join(self.audit_dir, f"audit_{date.isoformat()}.jsonl")

    def _open_file(self, date: datetime.date):
        path = self._get_file_path(date)
        os.makedirs(self.audit_dir, exist_ok=True)
        return open(path, 'a', encoding='utf-8')

    def _rotate_file(self):
        today = datetime.date.today()
        if today != self.current_date:
            self.file_handle.close()
            self.current_date = today
            self.file_handle = self._open_file(today)
            self.file_path = self._get_file_path(today)

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str],
              mode: str, confidence: float, latency: float, cache_hit: bool):
        self._rotate_file()
        record = {
            'query_id': query_id,
            'timestamp': timestamp,
            'engine_id': engine_id,
            'engines_invoked': engines_invoked,
            'mode': mode,
            'confidence': confidence,
            'latency': latency,
            'cache_hit': cache_hit
        }
        with self.lock:
            self.file_handle.write(json.dumps(record) + '\n')
            self.file_handle.flush()

    def forensic_replay(self, date: Optional[datetime.date] = None) -> List[Dict[str, Any]]:
        date = date or self.current_date
        path = self._get_file_path(date)
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f]

    def close(self):
        with self.lock:
            self.file_handle.close()

# --- PERFORMANCE PROFILER ---

class PerformanceProfiler:
    def __init__(self):
        self.lock = threading.Lock()
        self.sub_engine_latency: Dict[str, List[float]] = defaultdict(list)
        self.sub_engine_errors: Dict[str, int] = defaultdict(int)
        self.sub_engine_invocations: Dict[str, int] = defaultdict(int)
        self.sub_engine_availability: Dict[str, int] = defaultdict(int)
        self.sla_thresholds: Dict[str, Dict[str, Any]] = {}

    def record(self, sub_engine: str, latency: float, error: Optional[str] = None):
        with self.lock:
            self.sub_engine_latency[sub_engine].append(latency)
            self.sub_engine_invocations[sub_engine] += 1
            self.sub_engine_availability[sub_engine] += 1
            if error:
                self.sub_engine_errors[sub_engine] += 1

    def set_sla(self, sub_engine: str, latency_ms: float, error_rate: float, availability: float):
        with self.lock:
            self.sla_thresholds[sub_engine] = {
                'latency_ms': latency_ms,
                'error_rate': error_rate,
                'availability': availability
            }

    def get_stats(self):
        with self.lock:
            stats = {}
            for engine in self.sub_engine_latency:
                latencies = self.sub_engine_latency[engine]
                n = len(latencies)
                avg_latency = sum(latencies) / n if n else None
                error_rate = self.sub_engine_errors[engine] / self.sub_engine_invocations[engine] if self.sub_engine_invocations[engine] else 0.0
                availability = self.sub_engine_availability[engine]
                stats[engine] = {
                    'avg_latency': avg_latency,
                    'error_rate': error_rate,
                    'availability': availability,
                    'sla': self.sla_thresholds.get(engine, {})
                }
            return stats

    def check_sla(self):
        with self.lock:
            violations = {}
            stats = self.get_stats()
            for engine, stat in stats.items():
                sla = stat['sla']
                v = []
                if sla:
                    if stat['avg_latency'] is not None and stat['avg_latency'] > sla['latency_ms']:
                        v.append('latency')
                    if stat['error_rate'] > sla['error_rate']:
                        v.append('error_rate')
                    if stat['availability'] < sla['availability']:
                        v.append('availability')
                if v:
                    violations[engine] = v
            return violations

# --- MAIN ENGINE ORCHESTRATOR (partial, for context) ---

class MathematicsIntelligenceEngineDomainOrchestratorBackbone:
    def __init__(self, audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_tracker = CoverageTracker()
        self.audit_trail = AuditTrailWriter(audit_dir)
        self.performance_profiler = PerformanceProfiler()

    def process_query(self, query: Dict[str, Any], response: Dict[str, Any], engine_id: str,
                     engines_invoked: List[str], mode: str, confidence: float, latency: float,
                     cache_hit: bool, error: Optional[str] = None):
        query_id = query.get('query_id', str(hashlib.md5(json.dumps(query).encode()).hexdigest()))
        timestamp = time.time()
        # Telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry.record_query(telemetry)
        if error:
            self.telemetry.record_error(query_id, error, timestamp)
        # Drift
        self.drift_watcher.record_baseline(mode, confidence)
        self.drift_watcher.detect_drift(mode, confidence)
        # Coverage
        doctrines = response.get('doctrines', [])
        if doctrines:
            for doctrine in doctrines:
                self.coverage_tracker.record_triggered(doctrine, query_id)
        else:
            self.coverage_tracker.record_missed(query_id, query)
            self.coverage_tracker.identify_epistemic_gap(query, doctrines)
        # Determinism hash
        determinism_hash = compute_determinism_hash(query, response)
        # Audit trail
        self.audit_trail.write(
            query_id=query_id,
            timestamp=timestamp,
            engine_id=engine_id,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            latency=latency,
            cache_hit=cache_hit
        )
        # Performance profiler
        for engine in engines_invoked:
            self.performance_profiler.record(engine, latency, error)

    def get_telemetry_stats(self):
        return self.telemetry.get_latency_stats()

    def get_drift_report(self):
        return self.drift_watcher.get_drift_report()

    def get_coverage_report(self):
        return self.coverage_tracker.get_coverage_report()

    def get_audit_trail(self, date: Optional[datetime.date] = None):
        return self.audit_trail.forensic_replay(date)

    def get_performance_stats(self):
        return self.performance_profiler.get_stats()

    def check_sla(self):
        return self.performance_profiler.check_sla()

    def close(self):
        self.audit_trail.close()

# --- END PART 5 ---

# --- PART 6: FastAPI Server ---
# (Imports already at top of file, re-reference for clarity)

ENGINE_ID = "MATHIE"
ENGINE_PORT = 8861
ENGINE_NAME = "Mathematics Intelligence Engine — Domain Orchestrator"

SUB_ENGINES = {
    "MATH01": {"name": "Linear Algebra", "url": "http://localhost:8871"},
    "MATH02": {"name": "Calculus", "url": "http://localhost:8872"},
    "MATH03": {"name": "Statistics", "url": "http://localhost:8873"},
    "MATH04": {"name": "Differential Equations", "url": "http://localhost:8874"},
    "MATH05": {"name": "Number Theory", "url": "http://localhost:8875"},
    "MATH06": {"name": "Optimization", "url": "http://localhost:8876"},
    "MATH07": {"name": "Numerical Methods", "url": "http://localhost:8877"},
    "MATH08": {"name": "Probability", "url": "http://localhost:8878"},
    "MATH09": {"name": "Discrete Math", "url": "http://localhost:8879"},
    "MATH10": {"name": "Topology", "url": "http://localhost:8880"},
    "MATH11": {"name": "Abstract Algebra", "url": "http://localhost:8881"},
    "MATH12": {"name": "Complex Analysis", "url": "http://localhost:8882"},
}

QUERY_TIMEOUT_SECONDS = 5
SUBENGINE_TIMEOUT_SECONDS = 3
CIRCUIT_BREAKER_THRESHOLD = 5
CIRCUIT_BREAKER_RESET_SECONDS = 60
CACHE_TTL_SECONDS = 3600
HEALTH_CHECK_INTERVAL_SECONDS = 30
TELEMETRY_FLUSH_INTERVAL_SECONDS = 60

# Logging Setup

logger = logging.getLogger(ENGINE_ID)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Data Models


class QueryRequest(BaseModel):
    query: str = Field(..., example="Find eigenvalues of a matrix")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    query: str
    results: Dict[str, Any]
    merged: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthStatus(BaseModel):
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)


class MetricsResponse(BaseModel):
    latency_ms: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Any]


class CoverageReport(BaseModel):
    doctrine_coverage: Dict[str, float]
    epistemic_gaps: List[str]


class DriftReport(BaseModel):
    drift_detected: bool
    details: Dict[str, Any]


class DoctrineInfo(BaseModel):
    doctrine_id: str
    domain: str
    last_updated: datetime


class RoutingRule(BaseModel):
    domain: str
    sub_engines: List[str]


class RoutingInfo(BaseModel):
    routing_rules: List[RoutingRule]
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
    engines_to_invoke: List[str]


class AnalyzeRequest(BaseModel):
    query: str
    depth: int = Field(default=3, ge=1, le=10)


class AnalyzeResponse(BaseModel):
    analysis: Dict[str, Any]


# Internal State and Cache


class DoctrineCache:
    def __init__(self):
        self._cache: Dict[str, DoctrineInfo] = {}
        self._lock = asyncio.Lock()

    async def seed(self):
        # Simulate seeding doctrine cache from persistent store or files
        async with self._lock:
            now = datetime.utcnow()
            for i in range(1, 21):
                doctrine_id = f"DOCTRINE_{i:03d}"
                domain = "Mathematics"
                self._cache[doctrine_id] = DoctrineInfo(
                    doctrine_id=doctrine_id, domain=domain, last_updated=now
                )
            logger.info("Doctrine cache seeded with %d doctrines", len(self._cache))

    async def get_all(self) -> List[DoctrineInfo]:
        async with self._lock:
            return list(self._cache.values())

    async def get(self, doctrine_id: str) -> Optional[DoctrineInfo]:
        async with self._lock:
            return self._cache.get(doctrine_id)


class QueryCache:
    def __init__(self):
        self._cache: Dict[str, Tuple[QueryResponse, datetime]] = {}
        self._lock = asyncio.Lock()
        self.hits = 0
        self.misses = 0

    async def get(self, key: str) -> Optional[QueryResponse]:
        async with self._lock:
            entry = self._cache.get(key)
            if entry:
                response, timestamp = entry
                if datetime.utcnow() - timestamp < timedelta(seconds=CACHE_TTL_SECONDS):
                    self.hits += 1
                    return response
                else:
                    # Expired
                    del self._cache[key]
            self.misses += 1
            return None

    async def set(self, key: str, response: QueryResponse):
        async with self._lock:
            self._cache[key] = (response, datetime.utcnow())

    async def hit_rate(self) -> float:
        async with self._lock:
            total = self.hits + self.misses
            if total == 0:
                return 0.0
            return self.hits / total


class CircuitBreaker:
    def __init__(self):
        self.failures: Dict[str, int] = {}
        self.last_failure_time: Dict[str, datetime] = {}
        self.open_until: Dict[str, datetime] = {}

    def record_failure(self, engine_id: str):
        now = datetime.utcnow()
        self.failures[engine_id] = self.failures.get(engine_id, 0) + 1
        self.last_failure_time[engine_id] = now
        if self.failures[engine_id] >= CIRCUIT_BREAKER_THRESHOLD:
            self.open_until[engine_id] = now + timedelta(seconds=CIRCUIT_BREAKER_RESET_SECONDS)
            logger.warning(
                "Circuit breaker opened for %s until %s",
                engine_id,
                self.open_until[engine_id].isoformat(),
            )

    def record_success(self, engine_id: str):
        self.failures[engine_id] = 0
        self.open_until.pop(engine_id, None)

    def is_open(self, engine_id: str) -> bool:
        now = datetime.utcnow()
        open_until = self.open_until.get(engine_id)
        if open_until and open_until > now:
            return True
        if open_until and open_until <= now:
            # Reset circuit breaker after timeout
            self.failures[engine_id] = 0
            self.open_until.pop(engine_id, None)
            return False
        return False


class TelemetryCollector:
    def __init__(self):
        self.latencies: List[float] = []
        self.query_timestamps: List[datetime] = []
        self.lock = asyncio.Lock()

    async def record_latency(self, latency_ms: float):
        async with self.lock:
            self.latencies.append(latency_ms)
            self.query_timestamps.append(datetime.utcnow())

    async def get_latency_stats(self) -> Dict[str, float]:
        async with self.lock:
            if not self.latencies:
                return {"min": 0.0, "max": 0.0, "avg": 0.0}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "avg": sum(self.latencies) / len(self.latencies),
            }

    async def get_queries_per_hour(self) -> float:
        async with self.lock:
            now = datetime.utcnow()
            one_hour_ago = now - timedelta(hours=1)
            recent = [t for t in self.query_timestamps if t > one_hour_ago]
            return len(recent)


# Global Instances

doctrine_cache = DoctrineCache()
query_cache = QueryCache()
circuit_breaker = CircuitBreaker()
telemetry = TelemetryCollector()

# Health Monitor State

sub_engine_health: Dict[str, SubEngineHealth] = {}
sub_engine_health_lock = asyncio.Lock()

# Routing Rules (simple example)

ROUTING_RULES = [
    RoutingRule(domain="Linear Algebra", sub_engines=["MATH01"]),
    RoutingRule(domain="Calculus", sub_engines=["MATH02"]),
    RoutingRule(domain="Statistics", sub_engines=["MATH03"]),
    RoutingRule(domain="Differential Equations", sub_engines=["MATH04"]),
    RoutingRule(domain="Number Theory", sub_engines=["MATH05"]),
    RoutingRule(domain="Optimization", sub_engines=["MATH06"]),
    RoutingRule(domain="Numerical Methods", sub_engines=["MATH07"]),
    RoutingRule(domain="Probability", sub_engines=["MATH08"]),
    RoutingRule(domain="Discrete Math", sub_engines=["MATH09"]),
    RoutingRule(domain="Topology", sub_engines=["MATH10"]),
    RoutingRule(domain="Abstract Algebra", sub_engines=["MATH11"]),
    RoutingRule(domain="Complex Analysis", sub_engines=["MATH12"]),
]

# FastAPI app initialization

app = FastAPI(
    title=ENGINE_NAME,
    description="Domain Orchestrator for Mathematics Intelligence Engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility Functions


def normalize_query(query: str) -> str:
    # Basic normalization: lowercase, strip, remove extra spaces
    normalized = " ".join(query.lower().strip().split())
    return normalized


def classify_domain(query: str) -> str:
    # Simple keyword-based classification for demonstration
    keywords_map = {
        "matrix": "Linear Algebra",
        "eigenvalue": "Linear Algebra",
        "derivative": "Calculus",
        "integral": "Calculus",
        "probability": "Probability",
        "distribution": "Statistics",
        "optimization": "Optimization",
        "topology": "Topology",
        "algebra": "Abstract Algebra",
        "complex": "Complex Analysis",
        "number": "Number Theory",
        "differential": "Differential Equations",
        "numerical": "Numerical Methods",
        "discrete": "Discrete Math",
        "statistics": "Statistics",
    }
    query_lower = query.lower()
    for keyword, domain in keywords_map.items():
        if keyword in query_lower:
            return domain
    return "General Mathematics"


def route_to_sub_engines(domain: str) -> List[str]:
    # Find routing rules matching domain
    for rule in ROUTING_RULES:
        if rule.domain == domain:
            return rule.sub_engines
    # Default fallback to all sub-engines
    return list(SUB_ENGINES.keys())


async def dispatch_to_sub_engine(
    engine_id: str, query: str, options: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    if circuit_breaker.is_open(engine_id):
        logger.warning("Circuit breaker open for %s, skipping dispatch", engine_id)
        return None
    url = SUB_ENGINES[engine_id]["url"] + "/query"
    payload = {"query": query}
    if options:
        payload["options"] = options
    try:
        async with httpx.AsyncClient(timeout=SUBENGINE_TIMEOUT_SECONDS) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            circuit_breaker.record_success(engine_id)
            return data
    except Exception as e:
        logger.error("Error dispatching to %s: %s", engine_id, str(e))
        circuit_breaker.record_failure(engine_id)
        return None


def merge_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Merge results from sub-engines, simple aggregation
    merged = {}
    for resp in responses:
        if not resp:
            continue
        for k, v in resp.items():
            if k not in merged:
                merged[k] = v
            else:
                # If key exists, merge intelligently
                if isinstance(v, list):
                    merged[k] = list(set(merged[k]) | set(v))
                elif isinstance(v, dict):
                    merged[k].update(v)
                else:
                    # For scalars, override with latest
                    merged[k] = v
    return merged


def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Example guardrail: remove any keys with sensitive info (none expected here)
    filtered = {k: v for k, v in response.items() if k != "sensitive_info"}
    return filtered


def hash_query(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()


async def log_query(query_hash: str, query: str, response: Dict[str, Any], latency_ms: float):
    logger.info(
        "QueryHash=%s Query=%s Latency=%.2fms ResponseKeys=%d",
        query_hash,
        query,
        latency_ms,
        len(response),
    )


async def fallback_to_doctrine_cache(query: str) -> Optional[Dict[str, Any]]:
    # Simple fallback: return doctrines containing keywords from query
    doctrines = await doctrine_cache.get_all()
    query_words = set(query.lower().split())
    matched = []
    for doctrine in doctrines:
        if any(word in doctrine.doctrine_id.lower() for word in query_words):
            matched.append(
                {
                    "doctrine_id": doctrine.doctrine_id,
                    "domain": doctrine.domain,
                    "last_updated": doctrine.last_updated.isoformat(),
                }
            )
    if matched:
        return {"fallback_doctrines": matched}
    return None


# Lifespan management


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s...", ENGINE_NAME)
    # Initialize doctrine cache
    await doctrine_cache.seed()
    # Start health monitor
    health_monitor_task = asyncio.create_task(health_monitor_loop())
    # Start telemetry flush task
    telemetry_task = asyncio.create_task(telemetry_flush_loop())
    yield
    # Cleanup on shutdown
    health_monitor_task.cancel()
    telemetry_task.cancel()
    await asyncio.gather(health_monitor_task, telemetry_task, return_exceptions=True)
    logger.info("%s shutdown complete.", ENGINE_NAME)


app.router.lifespan_context = lifespan


# Background Tasks


async def health_monitor_loop():
    while True:
        await check_sub_engines_health()
        await asyncio.sleep(HEALTH_CHECK_INTERVAL_SECONDS)


async def check_sub_engines_health():
    async with sub_engine_health_lock:
        for engine_id, info in SUB_ENGINES.items():
            url = info["url"] + "/health"
            try:
                async with httpx.AsyncClient(timeout=2) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    status_str = data.get("status", "unknown")
                    sub_engine_health[engine_id] = SubEngineHealth(
                        engine_id=engine_id,
                        name=info["name"],
                        status=status_str,
                        last_checked=datetime.utcnow(),
                        error=None,
                    )
            except Exception as e:
                sub_engine_health[engine_id] = SubEngineHealth(
                    engine_id=engine_id,
                    name=info["name"],
                    status="unhealthy",
                    last_checked=datetime.utcnow(),
                    error=str(e),
                )


async def telemetry_flush_loop():
    while True:
        await asyncio.sleep(TELEMETRY_FLUSH_INTERVAL_SECONDS)
        # For now, just log telemetry stats
        latency_stats = await telemetry.get_latency_stats()
        qph = await telemetry.get_queries_per_hour()
        logger.info(
            "Telemetry flush: Latency stats: %s, Queries/hour: %.2f",
            latency_stats,
            qph,
        )


# Endpoint Implementations


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    normalized_query = normalize_query(request.query)
    domain = classify_domain(normalized_query)
    engines = route_to_sub_engines(domain)

    query_hash = hash_query(normalized_query)
    cached_response = await query_cache.get(query_hash)
    if cached_response:
        await telemetry.record_latency((time.perf_counter() - start_time) * 1000)
        await log_query(query_hash, normalized_query, cached_response.results, 0)
        return cached_response

    # Dispatch concurrently to sub-engines
    tasks = []
    for engine_id in engines:
        tasks.append(dispatch_to_sub_engine(engine_id, normalized_query, request.options))
    try:
        responses = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True), timeout=QUERY_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        responses = []

    # Filter out exceptions and None
    valid_responses = []
    for r in responses:
        if isinstance(r, Exception) or r is None:
            continue
        valid_responses.append(r)

    if not valid_responses:
        # Fallback to doctrine cache
        fallback = await fallback_to_doctrine_cache(normalized_query)
        if fallback:
            merged_result = fallback
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No sub-engine responses and no fallback available",
            )
    else:
        merged_result = merge_responses(valid_responses)

    guarded_result = apply_guardrails(merged_result)
    latency_ms = (time.perf_counter() - start_time) * 1000

    response = QueryResponse(
        query=request.query, results=guarded_result, merged=True, timestamp=datetime.utcnow()
    )
    await query_cache.set(query_hash, response)
    await telemetry.record_latency(latency_ms)
    await log_query(query_hash, normalized_query, guarded_result, latency_ms)
    return response


@app.get("/health", response_model=Dict[str, Any])
async def health_endpoint():
    # Self health
    self_health = {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    # Sub-engines health
    async with sub_engine_health_lock:
        sub_engines = {
            eid: {
                "name": health.name,
                "status": health.status,
                "last_checked": health.last_checked.isoformat(),
                "error": health.error,
            }
            for eid, health in sub_engine_health.items()
        }
    return {"self": self_health, "sub_engines": sub_engines}


@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latency_stats = await telemetry.get_latency_stats()
    cache_hit_rate = await query_cache.hit_rate()
    queries_per_hour = await telemetry.get_queries_per_hour()
    async with sub_engine_health_lock:
        sub_engine_stats = {
            eid: {
                "status": health.status,
                "last_checked": health.last_checked.isoformat(),
                "error": health.error,
            }
            for eid, health in sub_engine_health.items()
        }
    return MetricsResponse(
        latency_ms=latency_stats["avg"],
        cache_hit_rate=cache_hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=sub_engine_stats,
    )


@app.get("/coverage", response_model=CoverageReport)
async def coverage_endpoint():
    doctrines = await doctrine_cache.get_all()
    total_doctrines = len(doctrines)
    # For demo, assume coverage per domain is uniform
    domain_counts = {}
    for doctrine in doctrines:
        domain_counts[doctrine.domain] = domain_counts.get(doctrine.domain, 0) + 1
    coverage = {domain: count / total_doctrines for domain, count in domain_counts.items()}
    epistemic_gaps = []
    # Identify domains with low coverage (arbitrary threshold 0.05)
    for domain, cov in coverage.items():
        if cov < 0.05:
            epistemic_gaps.append(domain)
    return CoverageReport(doctrine_coverage=coverage, epistemic_gaps=epistemic_gaps)


@app.get("/drift", response_model=DriftReport)
async def drift_endpoint():
    # Dummy drift detection: no drift detected
    drift_detected = False
    details = {"message": "No drift detected in doctrine cache or sub-engines."}
    return DriftReport(drift_detected=drift_detected, details=details)


@app.get("/doctrines", response_model=List[DoctrineInfo])
async def doctrines_endpoint():
    doctrines = await doctrine_cache.get_all()
    return doctrines


@app.get("/routing", response_model=RoutingInfo)
async def routing_endpoint():
    engine_registry = {eid: info["name"] for eid, info in SUB_ENGINES.items()}
    return RoutingInfo(routing_rules=ROUTING_RULES, engine_registry=engine_registry)


@app.get("/sub-engines", response_model=List[SubEngineHealth])
async def sub_engines_endpoint():
    async with sub_engine_health_lock:
        return list(sub_engine_health.values())


@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    normalized_query = normalize_query(request.query)
    domain = classify_domain(normalized_query)
    engines = route_to_sub_engines(domain)
    return RouteDryRunResponse(engines_to_invoke=engines)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    domain = classify_domain(normalized_query)
    engines = route_to_sub_engines(domain)

    analysis_results = {}

    async def analyze_engine(engine_id: str, depth: int):
        if circuit_breaker.is_open(engine_id):
            return {engine_id: {"error": "Circuit breaker open"}}
        url = SUB_ENGINES[engine_id]["url"] + "/analyze"
        payload = {"query": normalized_query, "depth": depth}
        try:
            async with httpx.AsyncClient(timeout=SUBENGINE_TIMEOUT_SECONDS) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                circuit_breaker.record_success(engine_id)
                return {engine_id: data}
        except Exception as e:
            circuit_breaker.record_failure(engine_id)
            return {engine_id: {"error": str(e)}}

    tasks = [analyze_engine(eid, request.depth) for eid in engines]
    results = await asyncio.gather(*tasks)
    for res in results:
        analysis_results.update(res)

    return AnalyzeResponse(analysis=analysis_results)


# Error Handling Middleware


@app.exception_handler(httpx.RequestError)
async def httpx_request_error_handler(request: Request, exc: httpx.RequestError):
    logger.error("HTTPX RequestError: %s", str(exc))
    return Response(
        content=json.dumps({"detail": "Upstream service unavailable"}),
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        media_type="application/json",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("HTTPException: %s", exc.detail)
    return Response(
        content=json.dumps({"detail": exc.detail}),
        status_code=exc.status_code,
        media_type="application/json",
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("Unhandled exception: %s", str(e))
        raise
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-ms"] = str(process_time)
    return response


# Server startup


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")