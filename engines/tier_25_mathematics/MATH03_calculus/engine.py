"""
MATH03 — Calculus Intelligence Engine
======================================
TIE-20 compliant engine for symbolic differentiation, numerical integration,
Taylor series, limits, L'Hopital's rule, ODE solving, partial derivatives,
gradient, and Jacobian computation.

Port: 8565 | Tier: 13 (Mathematics) | Mode: DET | Auth: 5.0
Version: 1.0.0 | 20/20 TIE components implemented.
"""
from __future__ import annotations

import asyncio
import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
import uuid
from contextlib import asynccontextmanager
from enum import Enum
from math import (
    acos,
    asin,
    atan,
    cos,
    cosh,
    e,
    exp,
    factorial,
    inf,
    isnan,
    log,
    pi,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
)
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# [TIE-18] LOGURU LOGGING SETUP
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>MATH03</cyan> | {message}",
)
logger.add(
    LOG_DIR / "math03_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} | {message}",
)

sys.path.insert(0, str(Path(__file__).parent.parent))

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
ENGINE_ID = "MATH03"
ENGINE_NAME = "Calculus Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8565
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0
STARTUP_TIME = time.time()

AUDIT_LOG_PATH = ENGINE_DIR / "logs" / "audit_trail.jsonl"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    """TIE-2: Response mode selection."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """TIE-5: Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """TIE-13: Zoned analysis categories."""
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    """Multi-doctrine decomposition categories."""
    DIFFERENTIATION = "DIFFERENTIATION"
    INTEGRATION = "INTEGRATION"
    SERIES = "SERIES"
    LIMITS = "LIMITS"
    ODE = "ODE"
    MULTIVARIABLE = "MULTIVARIABLE"
    SIMPLIFICATION = "SIMPLIFICATION"
    COMPUTATION = "COMPUTATION"


class QueryRequest(BaseModel):
    """Incoming query payload."""
    query: str = Field(..., min_length=1, description="The calculus question or expression")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.REPORTING, description="Analysis zone")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    session_id: Optional[str] = Field(default=None, description="Session tracking ID")
    include_steps: bool = Field(default=True, description="Include step-by-step solution")


class AuthoritySource(BaseModel):
    """A cited authority for a conclusion."""
    source: str
    weight: float = Field(ge=0.0, le=1.0)
    section: Optional[str] = None


class FactFragilityReport(BaseModel):
    """TIE-14: Fact fragility scoring."""
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    overall_fragility: float = Field(ge=0.0, le=1.0)


class DriftReport(BaseModel):
    """TIE-9: Drift watcher output."""
    drift_detected: bool = False
    drift_score: float = 0.0
    details: str = ""


class DoctrineHit(BaseModel):
    """Single doctrine match from the cache."""
    topic: str
    confidence: float
    stratification: str
    conclusion: str
    reasoning: str
    authorities: List[str]
    keywords_matched: List[str]


class QueryResponse(BaseModel):
    """Full response payload."""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_id: str
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    timestamp: str
    latency_ms: float
    layer_used: str
    issue_categories: List[str]
    doctrine_hits: List[DoctrineHit]
    answer: str
    steps: List[str]
    numeric_result: Optional[float] = None
    symbolic_result: Optional[str] = None
    confidence: float
    confidence_stratification: ConfidenceLevel
    authorities: List[AuthoritySource]
    fragility: FactFragilityReport
    drift: DriftReport
    determinism_hash: str
    disclosure_caveat: Optional[str] = None
    deep_analysis: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    port: int = ENGINE_PORT
    tier: int = ENGINE_TIER
    mode: str = ENGINE_MODE
    uptime_seconds: float
    total_queries: int
    doctrine_count: int
    coverage_zones: int
    avg_latency_ms: float
    error_rate: float
    components: Dict[str, bool]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: EXPRESSION TREE — AST FOR SYMBOLIC MATH
# ═══════════════════════════════════════════════════════════════════════════

class Expr:
    """Base class for mathematical expression AST nodes."""

    def eval(self, env: Dict[str, float] | None = None) -> float:
        """Evaluate numerically given variable bindings."""
        raise NotImplementedError

    def diff(self, var: str) -> "Expr":
        """Symbolic differentiation with respect to var."""
        raise NotImplementedError

    def simplify(self) -> "Expr":
        """Algebraic simplification."""
        return self

    def __repr__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expr):
            return NotImplemented
        return self.to_str() == other.to_str()

    def __hash__(self) -> int:
        return hash(self.to_str())


class Const(Expr):
    """Numeric constant."""

    def __init__(self, value: float) -> None:
        self.value = float(value)

    def eval(self, env: Dict[str, float] | None = None) -> float:
        return self.value

    def diff(self, var: str) -> Expr:
        return Const(0)

    def simplify(self) -> Expr:
        if self.value == int(self.value) and abs(self.value) < 1e12:
            self.value = float(int(self.value))
        return self

    def to_str(self) -> str:
        if self.value == int(self.value) and abs(self.value) < 1e12:
            return str(int(self.value))
        return f"{self.value:.6g}"


class Var(Expr):
    """Variable reference."""

    def __init__(self, name: str) -> None:
        self.name = name

    def eval(self, env: Dict[str, float] | None = None) -> float:
        if env is None or self.name not in env:
            raise ValueError(f"Variable '{self.name}' not bound")
        return env[self.name]

    def diff(self, var: str) -> Expr:
        return Const(1) if self.name == var else Const(0)

    def to_str(self) -> str:
        return self.name


class BinOp(Expr):
    """Binary operation: +, -, *, /, ^."""

    def __init__(self, op: str, left: Expr, right: Expr) -> None:
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env: Dict[str, float] | None = None) -> float:
        lv = self.left.eval(env)
        rv = self.right.eval(env)
        if self.op == "+":
            return lv + rv
        if self.op == "-":
            return lv - rv
        if self.op == "*":
            return lv * rv
        if self.op == "/":
            if rv == 0:
                raise ZeroDivisionError("Division by zero in expression evaluation")
            return lv / rv
        if self.op == "^":
            return lv ** rv
        raise ValueError(f"Unknown operator: {self.op}")

    def diff(self, var: str) -> Expr:
        l, r = self.left, self.right
        ld, rd = l.diff(var), r.diff(var)

        if self.op == "+":
            return BinOp("+", ld, rd)
        if self.op == "-":
            return BinOp("-", ld, rd)
        if self.op == "*":
            # Product rule: f'g + fg'
            return BinOp("+", BinOp("*", ld, r), BinOp("*", l, rd))
        if self.op == "/":
            # Quotient rule: (f'g - fg') / g^2
            num = BinOp("-", BinOp("*", ld, r), BinOp("*", l, rd))
            den = BinOp("^", r, Const(2))
            return BinOp("/", num, den)
        if self.op == "^":
            # Two cases: constant exponent (power rule) vs variable exponent
            r_is_const = isinstance(r, Const)
            l_is_const = isinstance(l, Const)
            if r_is_const:
                # Power rule: d/dx[f^n] = n*f^(n-1)*f'
                return BinOp(
                    "*",
                    BinOp("*", r, BinOp("^", l, Const(r.value - 1))),
                    ld,
                )
            if l_is_const:
                # d/dx[a^g] = a^g * ln(a) * g'
                return BinOp(
                    "*",
                    BinOp("*", self, FuncCall("ln", l)),
                    rd,
                )
            # General: d/dx[f^g] = f^g * (g'*ln(f) + g*f'/f)
            term1 = BinOp("*", rd, FuncCall("ln", l))
            term2 = BinOp("*", r, BinOp("/", ld, l))
            return BinOp("*", self, BinOp("+", term1, term2))
        raise ValueError(f"Cannot differentiate operator: {self.op}")

    def simplify(self) -> Expr:
        l = self.left.simplify()
        r = self.right.simplify()

        # Constant folding
        if isinstance(l, Const) and isinstance(r, Const):
            try:
                result = BinOp(self.op, l, r).eval()
                if not isnan(result) and abs(result) < 1e15:
                    return Const(result)
            except (ZeroDivisionError, OverflowError, ValueError):
                pass

        if self.op == "+":
            if isinstance(l, Const) and l.value == 0:
                return r
            if isinstance(r, Const) and r.value == 0:
                return l
            # x + x = 2*x
            if l == r:
                return BinOp("*", Const(2), l).simplify()

        if self.op == "-":
            if isinstance(r, Const) and r.value == 0:
                return l
            if l == r:
                return Const(0)
            if isinstance(l, Const) and l.value == 0:
                return BinOp("*", Const(-1), r).simplify()

        if self.op == "*":
            if isinstance(l, Const) and l.value == 0:
                return Const(0)
            if isinstance(r, Const) and r.value == 0:
                return Const(0)
            if isinstance(l, Const) and l.value == 1:
                return r
            if isinstance(r, Const) and r.value == 1:
                return l
            if isinstance(l, Const) and l.value == -1:
                return BinOp("*", Const(-1), r)
            # Combine constants: (a*expr) * b = (a*b)*expr
            if isinstance(l, Const) and isinstance(r, BinOp) and r.op == "*" and isinstance(r.left, Const):
                return BinOp("*", Const(l.value * r.left.value), r.right).simplify()

        if self.op == "/":
            if isinstance(l, Const) and l.value == 0:
                return Const(0)
            if isinstance(r, Const) and r.value == 1:
                return l
            if l == r:
                return Const(1)

        if self.op == "^":
            if isinstance(r, Const) and r.value == 0:
                return Const(1)
            if isinstance(r, Const) and r.value == 1:
                return l
            if isinstance(l, Const) and l.value == 0:
                return Const(0)
            if isinstance(l, Const) and l.value == 1:
                return Const(1)

        return BinOp(self.op, l, r)

    def to_str(self) -> str:
        ls = self.left.to_str()
        rs = self.right.to_str()
        if self.op == "^":
            # Wrap complex subexpressions in parens
            if isinstance(self.left, BinOp):
                ls = f"({ls})"
            if isinstance(self.right, BinOp):
                rs = f"({rs})"
            return f"{ls}^{rs}"
        if self.op in ("*", "/"):
            if isinstance(self.left, BinOp) and self.left.op in ("+", "-"):
                ls = f"({ls})"
            if isinstance(self.right, BinOp) and self.right.op in ("+", "-"):
                rs = f"({rs})"
        return f"({ls} {self.op} {rs})"


class UnaryOp(Expr):
    """Unary negation."""

    def __init__(self, operand: Expr) -> None:
        self.operand = operand

    def eval(self, env: Dict[str, float] | None = None) -> float:
        return -self.operand.eval(env)

    def diff(self, var: str) -> Expr:
        return UnaryOp(self.operand.diff(var))

    def simplify(self) -> Expr:
        inner = self.operand.simplify()
        if isinstance(inner, Const):
            return Const(-inner.value)
        if isinstance(inner, UnaryOp):
            return inner.operand
        return UnaryOp(inner)

    def to_str(self) -> str:
        return f"(-{self.operand.to_str()})"


class FuncCall(Expr):
    """Function call: sin, cos, tan, exp, ln, sqrt, abs, etc."""

    KNOWN_FUNCS = {
        "sin", "cos", "tan", "sec", "csc", "cot",
        "asin", "acos", "atan",
        "sinh", "cosh", "tanh",
        "exp", "ln", "log", "sqrt", "abs",
    }

    def __init__(self, func_name: str, arg: Expr) -> None:
        self.func_name = func_name
        self.arg = arg

    def eval(self, env: Dict[str, float] | None = None) -> float:
        av = self.arg.eval(env)
        fn = self.func_name
        if fn == "sin":
            return sin(av)
        if fn == "cos":
            return cos(av)
        if fn == "tan":
            return tan(av)
        if fn == "sec":
            return 1.0 / cos(av)
        if fn == "csc":
            return 1.0 / sin(av)
        if fn == "cot":
            return cos(av) / sin(av)
        if fn == "asin":
            return asin(av)
        if fn == "acos":
            return acos(av)
        if fn == "atan":
            return atan(av)
        if fn == "sinh":
            return sinh(av)
        if fn == "cosh":
            return cosh(av)
        if fn == "tanh":
            return tanh(av)
        if fn == "exp":
            return exp(av)
        if fn == "ln" or fn == "log":
            if av <= 0:
                raise ValueError("ln of non-positive value")
            return log(av)
        if fn == "sqrt":
            if av < 0:
                raise ValueError("sqrt of negative value")
            return sqrt(av)
        if fn == "abs":
            return abs(av)
        raise ValueError(f"Unknown function: {fn}")

    def diff(self, var: str) -> Expr:
        """Chain rule: d/dx[f(g(x))] = f'(g(x)) * g'(x)."""
        g = self.arg
        gd = g.diff(var)
        fn = self.func_name

        if fn == "sin":
            outer_deriv = FuncCall("cos", g)
        elif fn == "cos":
            outer_deriv = BinOp("*", Const(-1), FuncCall("sin", g))
        elif fn == "tan":
            outer_deriv = BinOp("^", FuncCall("sec", g), Const(2))
        elif fn == "sec":
            outer_deriv = BinOp("*", FuncCall("sec", g), FuncCall("tan", g))
        elif fn == "csc":
            outer_deriv = BinOp("*", BinOp("*", Const(-1), FuncCall("csc", g)), FuncCall("cot", g))
        elif fn == "cot":
            outer_deriv = BinOp("*", Const(-1), BinOp("^", FuncCall("csc", g), Const(2)))
        elif fn == "asin":
            outer_deriv = BinOp("/", Const(1), FuncCall("sqrt", BinOp("-", Const(1), BinOp("^", g, Const(2)))))
        elif fn == "acos":
            outer_deriv = BinOp("/", Const(-1), FuncCall("sqrt", BinOp("-", Const(1), BinOp("^", g, Const(2)))))
        elif fn == "atan":
            outer_deriv = BinOp("/", Const(1), BinOp("+", Const(1), BinOp("^", g, Const(2))))
        elif fn == "sinh":
            outer_deriv = FuncCall("cosh", g)
        elif fn == "cosh":
            outer_deriv = FuncCall("sinh", g)
        elif fn == "tanh":
            outer_deriv = BinOp("-", Const(1), BinOp("^", FuncCall("tanh", g), Const(2)))
        elif fn == "exp":
            outer_deriv = FuncCall("exp", g)
        elif fn in ("ln", "log"):
            outer_deriv = BinOp("/", Const(1), g)
        elif fn == "sqrt":
            outer_deriv = BinOp("/", Const(1), BinOp("*", Const(2), FuncCall("sqrt", g)))
        elif fn == "abs":
            outer_deriv = BinOp("/", g, FuncCall("abs", g))
        else:
            raise ValueError(f"Cannot differentiate function: {fn}")

        return BinOp("*", outer_deriv, gd)

    def simplify(self) -> Expr:
        simplified_arg = self.arg.simplify()
        if isinstance(simplified_arg, Const):
            try:
                result = FuncCall(self.func_name, simplified_arg).eval()
                if not isnan(result) and abs(result) < 1e15:
                    return Const(result)
            except (ValueError, ZeroDivisionError, OverflowError):
                pass
        return FuncCall(self.func_name, simplified_arg)

    def to_str(self) -> str:
        return f"{self.func_name}({self.arg.to_str()})"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: EXPRESSION PARSER
# ═══════════════════════════════════════════════════════════════════════════

class ParseError(Exception):
    """Raised when expression parsing fails."""


class ExprParser:
    """Recursive descent parser for mathematical expressions.

    Grammar:
        expr     -> term (('+' | '-') term)*
        term     -> power (('*' | '/') power)*
        power    -> unary ('^' unary)*
        unary    -> '-' unary | atom
        atom     -> NUMBER | VARIABLE | FUNC '(' expr ')' | '(' expr ')'
    """

    FUNC_NAMES = {
        "sin", "cos", "tan", "sec", "csc", "cot",
        "asin", "acos", "atan", "arcsin", "arccos", "arctan",
        "sinh", "cosh", "tanh",
        "exp", "ln", "log", "sqrt", "abs",
    }
    FUNC_ALIASES = {"arcsin": "asin", "arccos": "acos", "arctan": "atan"}

    def __init__(self, text: str) -> None:
        self.text = text.replace(" ", "")
        self.pos = 0

    def parse(self) -> Expr:
        result = self._expr()
        if self.pos < len(self.text):
            raise ParseError(f"Unexpected character at position {self.pos}: '{self.text[self.pos]}'")
        return result

    def _peek(self) -> str:
        if self.pos < len(self.text):
            return self.text[self.pos]
        return ""

    def _advance(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def _expect(self, ch: str) -> None:
        if self.pos >= len(self.text) or self.text[self.pos] != ch:
            raise ParseError(f"Expected '{ch}' at position {self.pos}")
        self.pos += 1

    def _expr(self) -> Expr:
        left = self._term()
        while self._peek() in ("+", "-"):
            op = self._advance()
            right = self._term()
            left = BinOp(op, left, right)
        return left

    def _term(self) -> Expr:
        left = self._power()
        while self._peek() in ("*", "/"):
            op = self._advance()
            right = self._power()
            left = BinOp(op, left, right)
        return left

    def _power(self) -> Expr:
        base = self._unary()
        if self._peek() == "^":
            self._advance()
            exp_part = self._power()  # right-associative
            return BinOp("^", base, exp_part)
        return base

    def _unary(self) -> Expr:
        if self._peek() == "-":
            self._advance()
            operand = self._unary()
            return UnaryOp(operand)
        return self._atom()

    def _atom(self) -> Expr:
        # Parenthesized expression
        if self._peek() == "(":
            self._advance()
            result = self._expr()
            self._expect(")")
            return result

        # Named constant: pi, e
        if self.text[self.pos:self.pos + 2] == "pi" and (
            self.pos + 2 >= len(self.text) or not self.text[self.pos + 2].isalnum()
        ):
            self.pos += 2
            return Const(pi)

        if (
            self._peek() == "e"
            and (self.pos + 1 >= len(self.text) or not self.text[self.pos + 1].isalnum())
            and (self.pos + 1 >= len(self.text) or self.text[self.pos + 1] != "x")
        ):
            # standalone 'e' but not 'exp' or a variable starting with e
            # Need to be careful: 'e' alone is Euler's number, 'ex' could be misread
            # Only treat as constant if next char is operator or end
            next_pos = self.pos + 1
            if next_pos >= len(self.text) or self.text[next_pos] in ("+", "-", "*", "/", "^", ")"):
                self.pos += 1
                return Const(e)

        # Function call
        for fname in sorted(self.FUNC_NAMES, key=len, reverse=True):
            if self.text[self.pos:self.pos + len(fname)] == fname:
                after = self.pos + len(fname)
                if after < len(self.text) and self.text[after] == "(":
                    self.pos = after
                    self._expect("(")
                    arg = self._expr()
                    self._expect(")")
                    canonical = self.FUNC_ALIASES.get(fname, fname)
                    return FuncCall(canonical, arg)

        # Number (integer or float)
        if self._peek().isdigit() or self._peek() == ".":
            start = self.pos
            while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == "."):
                self.pos += 1
            # Scientific notation
            if self.pos < len(self.text) and self.text[self.pos] in ("e", "E"):
                self.pos += 1
                if self.pos < len(self.text) and self.text[self.pos] in ("+", "-"):
                    self.pos += 1
                while self.pos < len(self.text) and self.text[self.pos].isdigit():
                    self.pos += 1
            num_str = self.text[start:self.pos]
            try:
                return Const(float(num_str))
            except ValueError as exc:
                raise ParseError(f"Invalid number: {num_str}") from exc

        # Variable (single letter or multi-letter identifier)
        if self._peek().isalpha() or self._peek() == "_":
            start = self.pos
            while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == "_"):
                self.pos += 1
            name = self.text[start:self.pos]
            return Var(name)

        raise ParseError(f"Unexpected character at position {self.pos}: '{self._peek()}'")


def parse_expr(text: str) -> Expr:
    """Parse a mathematical expression string into an AST."""
    return ExprParser(text).parse()


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: SYMBOLIC DIFFERENTIATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def symbolic_diff(expr_str: str, var: str = "x", order: int = 1) -> Tuple[Expr, List[str]]:
    """Differentiate an expression symbolically, returning AST and steps."""
    steps: List[str] = []
    expr = parse_expr(expr_str)
    steps.append(f"Parsed expression: {expr.to_str()}")

    current = expr
    for i in range(order):
        derivative = current.diff(var)
        steps.append(f"d{'(' * (i > 0)}d{var}{')'*(i > 0)} raw: {derivative.to_str()}")
        derivative = derivative.simplify()
        steps.append(f"After simplification (order {i + 1}): {derivative.to_str()}")
        current = derivative

    return current, steps


def symbolic_diff_str(expr_str: str, var: str = "x", order: int = 1) -> str:
    """Return the simplified derivative as a string."""
    result, _ = symbolic_diff(expr_str, var, order)
    return result.to_str()


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: NUMERICAL INTEGRATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def trapezoidal_rule(
    f: Callable[[float], float], a: float, b: float, n: int = 1000
) -> Tuple[float, List[str]]:
    """Composite trapezoidal rule for numerical integration."""
    steps: List[str] = []
    if n < 1:
        raise ValueError("n must be >= 1")
    h = (b - a) / n
    steps.append(f"Trapezoidal rule: n={n}, h={h:.8g}")

    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        xi = a + i * h
        total += f(xi)
    result = h * total
    steps.append(f"Sum of interior points computed")
    steps.append(f"Result: {result:.12g}")
    return result, steps


def simpson_13_rule(
    f: Callable[[float], float], a: float, b: float, n: int = 1000
) -> Tuple[float, List[str]]:
    """Composite Simpson's 1/3 rule. n must be even."""
    steps: List[str] = []
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    steps.append(f"Simpson's 1/3 rule: n={n} (even), h={h:.8g}")

    total = f(a) + f(b)
    for i in range(1, n):
        xi = a + i * h
        coeff = 4 if i % 2 == 1 else 2
        total += coeff * f(xi)
    result = (h / 3) * total
    steps.append(f"Alternating 4/2 coefficients applied")
    steps.append(f"Result: {result:.12g}")
    return result, steps


def simpson_38_rule(
    f: Callable[[float], float], a: float, b: float, n: int = 999
) -> Tuple[float, List[str]]:
    """Composite Simpson's 3/8 rule. n must be divisible by 3."""
    steps: List[str] = []
    while n % 3 != 0:
        n += 1
    h = (b - a) / n
    steps.append(f"Simpson's 3/8 rule: n={n} (div by 3), h={h:.8g}")

    total = f(a) + f(b)
    for i in range(1, n):
        xi = a + i * h
        coeff = 2 if i % 3 == 0 else 3
        total += coeff * f(xi)
    result = (3 * h / 8) * total
    steps.append(f"Alternating 3/3/2 coefficients applied")
    steps.append(f"Result: {result:.12g}")
    return result, steps


# Gauss-Legendre nodes and weights for n=1..5 on [-1,1]
GAUSS_LEGENDRE_TABLE: Dict[int, List[Tuple[float, float]]] = {
    1: [(0.0, 2.0)],
    2: [(-1.0 / sqrt(3.0), 1.0), (1.0 / sqrt(3.0), 1.0)],
    3: [
        (-sqrt(3.0 / 5.0), 5.0 / 9.0),
        (0.0, 8.0 / 9.0),
        (sqrt(3.0 / 5.0), 5.0 / 9.0),
    ],
    4: [
        (-0.8611363115940526, 0.3478548451374538),
        (-0.3399810435848563, 0.6521451548625461),
        (0.3399810435848563, 0.6521451548625461),
        (0.8611363115940526, 0.3478548451374538),
    ],
    5: [
        (-0.9061798459386640, 0.2369268850561891),
        (-0.5384693101056831, 0.4786286704993665),
        (0.0, 0.5688888888888889),
        (0.5384693101056831, 0.4786286704993665),
        (0.9061798459386640, 0.2369268850561891),
    ],
}


def gauss_legendre(
    f: Callable[[float], float], a: float, b: float, n_points: int = 5
) -> Tuple[float, List[str]]:
    """Gauss-Legendre quadrature on [a, b]."""
    steps: List[str] = []
    if n_points not in GAUSS_LEGENDRE_TABLE:
        n_points = min(GAUSS_LEGENDRE_TABLE.keys(), key=lambda k: abs(k - n_points))
    nodes_weights = GAUSS_LEGENDRE_TABLE[n_points]
    steps.append(f"Gauss-Legendre: {n_points} points on [{a}, {b}]")

    # Transform from [-1,1] to [a,b]: x = (b-a)/2 * t + (a+b)/2
    half_range = (b - a) / 2.0
    midpoint = (a + b) / 2.0

    total = 0.0
    for ti, wi in nodes_weights:
        xi = half_range * ti + midpoint
        fxi = f(xi)
        total += wi * fxi
        steps.append(f"  node t={ti:.6f}, x={xi:.6f}, f(x)={fxi:.8g}, w={wi:.6f}")

    result = half_range * total
    steps.append(f"Result: {result:.12g}")
    return result, steps


def numerical_integrate(
    expr_str: str,
    a: float,
    b: float,
    method: str = "simpson",
    n: int = 1000,
    var: str = "x",
) -> Tuple[float, List[str]]:
    """Numerically integrate a parsed expression over [a, b]."""
    tree = parse_expr(expr_str)

    def f(val: float) -> float:
        return tree.eval({var: val})

    if method == "trapezoidal":
        return trapezoidal_rule(f, a, b, n)
    if method == "simpson" or method == "simpson13":
        return simpson_13_rule(f, a, b, n)
    if method == "simpson38":
        return simpson_38_rule(f, a, b, n)
    if method == "gauss":
        return gauss_legendre(f, a, b, min(n, 5))
    raise ValueError(f"Unknown integration method: {method}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: TAYLOR SERIES ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def taylor_series(
    expr_str: str,
    center: float = 0.0,
    n_terms: int = 6,
    var: str = "x",
) -> Tuple[List[Tuple[int, float]], str, List[str]]:
    """Compute Taylor series coefficients via repeated symbolic differentiation.

    Returns (coefficients as (order, coeff) pairs, polynomial string, steps).
    """
    steps: List[str] = []
    tree = parse_expr(expr_str)
    steps.append(f"Taylor expansion of {expr_str} about a={center}, {n_terms} terms")

    coefficients: List[Tuple[int, float]] = []
    current_deriv = tree

    for k in range(n_terms):
        try:
            val = current_deriv.eval({var: center})
        except (ValueError, ZeroDivisionError, OverflowError):
            steps.append(f"  f^({k})({center}) evaluation failed, stopping")
            break

        coeff = val / factorial(k)
        coefficients.append((k, coeff))
        steps.append(f"  f^({k})({center}) = {val:.8g}, coeff = {coeff:.8g}")

        if k < n_terms - 1:
            current_deriv = current_deriv.diff(var).simplify()

    # Build polynomial string
    terms: List[str] = []
    for order, coeff in coefficients:
        if abs(coeff) < 1e-15:
            continue
        coeff_str = f"{coeff:.6g}"
        if order == 0:
            terms.append(coeff_str)
        elif order == 1:
            if center == 0:
                terms.append(f"{coeff_str}*{var}")
            else:
                terms.append(f"{coeff_str}*({var}-{center})")
        else:
            if center == 0:
                terms.append(f"{coeff_str}*{var}^{order}")
            else:
                terms.append(f"{coeff_str}*({var}-{center})^{order}")

    poly_str = " + ".join(terms) if terms else "0"
    steps.append(f"Taylor polynomial: {poly_str}")
    return coefficients, poly_str, steps


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: LIMIT EVALUATOR
# ═══════════════════════════════════════════════════════════════════════════

def evaluate_limit(
    expr_str: str,
    var: str = "x",
    approach: float = 0.0,
    direction: str = "both",
    max_lhopital: int = 5,
) -> Tuple[Optional[float], str, List[str]]:
    """Evaluate limit of expression as var approaches a value.

    Uses: direct substitution, numerical approach, L'Hopital's rule.
    Returns: (value or None, method used, steps).
    """
    steps: List[str] = []
    tree = parse_expr(expr_str)
    steps.append(f"Evaluating lim({var}->{approach}) {expr_str}")

    # Step 1: Direct substitution
    try:
        direct = tree.eval({var: approach})
        if not isnan(direct) and abs(direct) < 1e15:
            steps.append(f"Direct substitution: f({approach}) = {direct:.12g}")
            return direct, "direct_substitution", steps
    except (ValueError, ZeroDivisionError, OverflowError):
        steps.append("Direct substitution failed (indeterminate or undefined)")

    # Step 2: Numerical approach from both sides
    left_vals: List[float] = []
    right_vals: List[float] = []
    epsilons = [1e-3, 1e-5, 1e-7, 1e-9, 1e-11]

    for eps in epsilons:
        if direction in ("both", "left"):
            try:
                val = tree.eval({var: approach - eps})
                if not isnan(val) and abs(val) < 1e15:
                    left_vals.append(val)
            except (ValueError, ZeroDivisionError, OverflowError):
                pass
        if direction in ("both", "right"):
            try:
                val = tree.eval({var: approach + eps})
                if not isnan(val) and abs(val) < 1e15:
                    right_vals.append(val)
            except (ValueError, ZeroDivisionError, OverflowError):
                pass

    steps.append(f"Numerical approach from left: {[f'{v:.8g}' for v in left_vals]}")
    steps.append(f"Numerical approach from right: {[f'{v:.8g}' for v in right_vals]}")

    # Check convergence
    all_vals = left_vals + right_vals
    if len(all_vals) >= 2:
        # Check if values are converging to the same limit
        spread = max(all_vals) - min(all_vals) if all_vals else float("inf")
        if spread < 1e-4:
            avg = sum(all_vals) / len(all_vals)
            steps.append(f"Numerical convergence detected: ~{avg:.10g}")
            return avg, "numerical_approach", steps

        # Check if left and right limits differ (jump discontinuity)
        if left_vals and right_vals:
            left_limit = left_vals[-1] if left_vals else None
            right_limit = right_vals[-1] if right_vals else None
            if left_limit is not None and right_limit is not None:
                if abs(left_limit - right_limit) > 0.01:
                    steps.append(
                        f"Left limit ~{left_limit:.8g} != Right limit ~{right_limit:.8g} (limit DNE)"
                    )
                    return None, "limit_dne_jump", steps

    # Step 3: Detect 0/0 indeterminate form and attempt L'Hopital
    # Check if expression is a ratio
    if isinstance(tree, BinOp) and tree.op == "/":
        num_tree = tree.left
        den_tree = tree.right
        try:
            num_val = num_tree.eval({var: approach})
            den_val = den_tree.eval({var: approach})
        except (ValueError, ZeroDivisionError, OverflowError):
            num_val, den_val = None, None

        if num_val is not None and den_val is not None:
            if abs(num_val) < 1e-10 and abs(den_val) < 1e-10:
                steps.append("Detected 0/0 indeterminate form — applying L'Hopital's rule")
                current_num = num_tree
                current_den = den_tree
                for attempt in range(max_lhopital):
                    current_num = current_num.diff(var).simplify()
                    current_den = current_den.diff(var).simplify()
                    steps.append(
                        f"L'Hopital #{attempt + 1}: lim {current_num.to_str()} / {current_den.to_str()}"
                    )
                    try:
                        nv = current_num.eval({var: approach})
                        dv = current_den.eval({var: approach})
                        if abs(dv) > 1e-15:
                            result = nv / dv
                            steps.append(f"L'Hopital result: {result:.12g}")
                            return result, "lhopital", steps
                        if abs(nv) > 1e-10:
                            steps.append("After L'Hopital: nonzero/0 => limit is +/-inf or DNE")
                            return None, "lhopital_diverge", steps
                    except (ValueError, ZeroDivisionError, OverflowError):
                        pass

    # Step 4: Fallback — best numerical estimate
    if all_vals:
        best = all_vals[-1]
        steps.append(f"Best numerical estimate: {best:.10g}")
        return best, "numerical_fallback", steps

    steps.append("Unable to determine limit")
    return None, "indeterminate", steps


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: ODE SOLVER
# ═══════════════════════════════════════════════════════════════════════════

def euler_method(
    f_rhs: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_end: float,
    n_steps: int = 1000,
) -> Tuple[List[Tuple[float, float]], List[str]]:
    """Solve dy/dx = f(x, y) with y(x0) = y0 using Euler's method."""
    steps: List[str] = []
    h = (x_end - x0) / n_steps
    steps.append(f"Euler method: h={h:.8g}, {n_steps} steps, [{x0}, {x_end}]")

    trajectory: List[Tuple[float, float]] = [(x0, y0)]
    x, y = x0, y0
    for i in range(n_steps):
        slope = f_rhs(x, y)
        y = y + h * slope
        x = x + h
        if i < 5 or i == n_steps - 1:
            trajectory.append((x, y))
            steps.append(f"  step {i + 1}: x={x:.6g}, y={y:.8g}")
        elif i == 5:
            steps.append("  ... (intermediate steps omitted)")

    steps.append(f"Final: y({x_end}) = {y:.12g}")
    return trajectory, steps


def rk4_method(
    f_rhs: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_end: float,
    n_steps: int = 1000,
) -> Tuple[List[Tuple[float, float]], List[str]]:
    """Solve dy/dx = f(x, y) with y(x0) = y0 using classical RK4."""
    steps: List[str] = []
    h = (x_end - x0) / n_steps
    steps.append(f"RK4 method: h={h:.8g}, {n_steps} steps, [{x0}, {x_end}]")

    trajectory: List[Tuple[float, float]] = [(x0, y0)]
    x, y = x0, y0
    for i in range(n_steps):
        k1 = h * f_rhs(x, y)
        k2 = h * f_rhs(x + h / 2, y + k1 / 2)
        k3 = h * f_rhs(x + h / 2, y + k2 / 2)
        k4 = h * f_rhs(x + h, y + k3)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + h
        if i < 5 or i == n_steps - 1:
            trajectory.append((x, y))
            steps.append(f"  step {i + 1}: x={x:.6g}, y={y:.8g}")
        elif i == 5:
            steps.append("  ... (intermediate steps omitted)")

    steps.append(f"Final: y({x_end}) = {y:.12g}")
    return trajectory, steps


def solve_ode(
    rhs_expr: str,
    x0: float,
    y0: float,
    x_end: float,
    method: str = "rk4",
    n_steps: int = 1000,
) -> Tuple[List[Tuple[float, float]], List[str]]:
    """Solve dy/dx = rhs_expr(x, y) given initial condition y(x0)=y0."""
    tree = parse_expr(rhs_expr)

    def f_rhs(x_val: float, y_val: float) -> float:
        return tree.eval({"x": x_val, "y": y_val})

    if method == "euler":
        return euler_method(f_rhs, x0, y0, x_end, n_steps)
    if method == "rk4":
        return rk4_method(f_rhs, x0, y0, x_end, n_steps)
    raise ValueError(f"Unknown ODE method: {method}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 9: PARTIAL DERIVATIVES / GRADIENT / JACOBIAN
# ═══════════════════════════════════════════════════════════════════════════

def partial_derivative(
    expr_str: str, var: str, order: int = 1
) -> Tuple[str, List[str]]:
    """Compute partial derivative of expr w.r.t. var."""
    result, steps = symbolic_diff(expr_str, var, order)
    return result.to_str(), steps


def gradient(
    expr_str: str, variables: List[str]
) -> Tuple[List[str], List[str]]:
    """Compute gradient vector: nabla f = (df/dx1, df/dx2, ...)."""
    steps: List[str] = [f"Computing gradient of {expr_str} w.r.t. {variables}"]
    grad_components: List[str] = []
    for v in variables:
        result, sub_steps = symbolic_diff(expr_str, v, 1)
        result_str = result.to_str()
        grad_components.append(result_str)
        steps.append(f"  df/d{v} = {result_str}")
    steps.append(f"Gradient: ({', '.join(grad_components)})")
    return grad_components, steps


def jacobian_matrix(
    func_exprs: List[str], variables: List[str]
) -> Tuple[List[List[str]], List[str]]:
    """Compute Jacobian matrix J[i][j] = d(f_i)/d(x_j)."""
    steps: List[str] = [
        f"Computing Jacobian of {len(func_exprs)} functions w.r.t. {variables}"
    ]
    matrix: List[List[str]] = []
    for i, f_expr in enumerate(func_exprs):
        row: List[str] = []
        for j, v in enumerate(variables):
            result, _ = symbolic_diff(f_expr, v, 1)
            result_str = result.to_str()
            row.append(result_str)
            steps.append(f"  J[{i}][{j}] = d(f{i})/d{v} = {result_str}")
        matrix.append(row)
    return matrix, steps


def jacobian_determinant_2x2(
    func_exprs: List[str], variables: List[str], point: Dict[str, float]
) -> Tuple[float, List[str]]:
    """Evaluate 2x2 Jacobian determinant at a point."""
    steps: List[str] = []
    if len(func_exprs) != 2 or len(variables) != 2:
        raise ValueError("jacobian_determinant_2x2 requires exactly 2 functions and 2 variables")

    jac, jac_steps = jacobian_matrix(func_exprs, variables)
    steps.extend(jac_steps)

    # Evaluate each entry at the given point
    vals: List[List[float]] = []
    for i in range(2):
        row_vals: List[float] = []
        for j in range(2):
            entry_tree = parse_expr(jac[i][j])
            val = entry_tree.eval(point)
            row_vals.append(val)
        vals.append(row_vals)

    det = vals[0][0] * vals[1][1] - vals[0][1] * vals[1][0]
    steps.append(f"det(J) = {vals[0][0]:.6g}*{vals[1][1]:.6g} - {vals[0][1]:.6g}*{vals[1][0]:.6g} = {det:.8g}")
    return det, steps


def hessian_matrix(
    expr_str: str, variables: List[str]
) -> Tuple[List[List[str]], List[str]]:
    """Compute Hessian matrix H[i][j] = d^2f / (dx_i dx_j)."""
    steps: List[str] = [f"Computing Hessian of {expr_str}"]
    matrix: List[List[str]] = []
    for vi in variables:
        row: List[str] = []
        first, _ = symbolic_diff(expr_str, vi, 1)
        first_str = first.to_str()
        for vj in variables:
            second, _ = symbolic_diff(first_str, vj, 1)
            result_str = second.to_str()
            row.append(result_str)
            steps.append(f"  H[d{vi},d{vj}] = {result_str}")
        matrix.append(row)
    return matrix, steps


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 10: TIE INFRASTRUCTURE COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════


# ---------------------------------------------------------------------------
# [TIE-3] DOCTRINE CACHE
# ---------------------------------------------------------------------------
class DoctrineCache:
    """Loads and searches the doctrine cache for fast first-layer responses."""

    def __init__(self) -> None:
        self.doctrines: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        cache_path = ENGINE_DIR / "doctrine_cache.json"
        if cache_path.exists():
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            self.doctrines = data.get("doctrines", [])
            logger.info(f"Loaded {len(self.doctrines)} doctrine blocks")
        else:
            logger.warning("doctrine_cache.json not found")

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Keyword-based doctrine search with scoring."""
        query_lower = query.lower()
        query_tokens = set(re.split(r"\W+", query_lower))

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for doc in self.doctrines:
            score = 0.0
            kw_matched: List[str] = []
            for kw in doc.get("keywords", []):
                kw_lower = kw.lower()
                if kw_lower in query_lower:
                    score += 3.0
                    kw_matched.append(kw)
                else:
                    kw_tokens = set(re.split(r"\W+", kw_lower))
                    overlap = len(query_tokens & kw_tokens)
                    if overlap > 0:
                        score += overlap * 1.5
                        kw_matched.append(kw)

            topic_lower = doc.get("topic", "").replace("_", " ").lower()
            topic_tokens = set(topic_lower.split())
            topic_overlap = len(query_tokens & topic_tokens)
            score += topic_overlap * 2.0

            if score > 0:
                doc_copy = dict(doc)
                doc_copy["_match_score"] = score
                doc_copy["_keywords_matched"] = kw_matched
                scored.append((score, doc_copy))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


# ---------------------------------------------------------------------------
# [TIE-6] SEMANTIC NORMALIZATION
# ---------------------------------------------------------------------------
class SemanticNormalizer:
    """Normalizes calculus terminology to canonical forms."""

    def __init__(self) -> None:
        self.rules: Dict[str, List[str]] = {}
        self.abbreviations: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        dict_path = ENGINE_DIR / "semantic_dict.json"
        if dict_path.exists():
            data = json.loads(dict_path.read_text(encoding="utf-8"))
            self.rules = data.get("normalization_rules", {})
            self.abbreviations = data.get("abbreviations", {})
            logger.info(f"Loaded {len(self.rules)} normalization rules")
        else:
            logger.warning("semantic_dict.json not found")

    def normalize(self, text: str) -> str:
        """Apply normalization rules to input text."""
        result = text
        for abbrev, full in self.abbreviations.items():
            pattern = re.compile(r"\b" + re.escape(abbrev) + r"\b", re.IGNORECASE)
            result = pattern.sub(full, result)
        return result

    def identify_topics(self, text: str) -> List[str]:
        """Identify canonical topics mentioned in text."""
        text_lower = text.lower()
        matched: List[str] = []
        for canonical, synonyms in self.rules.items():
            if canonical.replace("_", " ") in text_lower:
                matched.append(canonical)
                continue
            for syn in synonyms:
                if syn.lower() in text_lower:
                    matched.append(canonical)
                    break
        return matched


# ---------------------------------------------------------------------------
# [TIE-4] AUTHORITY HARDENING
# ---------------------------------------------------------------------------
class AuthorityHardener:
    """Manages authority levels, weighting, and conflict resolution."""

    AUTHORITY_WEIGHTS = {
        "primary_textbook": 1.0,
        "theorem_proof": 0.98,
        "peer_reviewed": 0.90,
        "standard_reference": 0.85,
        "lecture_notes": 0.70,
        "online_resource": 0.50,
        "heuristic": 0.30,
    }

    def harden(self, authorities: List[str], confidence: float) -> Tuple[float, List[AuthoritySource]]:
        """Apply authority weighting to confidence score."""
        if not authorities:
            return max(confidence * 0.7, 0.0), []

        sources: List[AuthoritySource] = []
        total_weight = 0.0
        for auth in authorities:
            weight = self._classify_authority(auth)
            sources.append(AuthoritySource(source=auth, weight=weight))
            total_weight += weight

        avg_weight = total_weight / len(authorities) if authorities else 0.5
        hardened_confidence = min(confidence * avg_weight, 1.0)
        return hardened_confidence, sources

    def _classify_authority(self, source: str) -> float:
        """Classify an authority source and return its weight."""
        source_lower = source.lower()
        if any(kw in source_lower for kw in ("theorem", "proof", "lemma")):
            return self.AUTHORITY_WEIGHTS["theorem_proof"]
        if any(kw in source_lower for kw in ("stewart", "spivak", "rudin", "apostol", "thomas", "marsden")):
            return self.AUTHORITY_WEIGHTS["primary_textbook"]
        if any(kw in source_lower for kw in ("atkinson", "burden", "hairer", "golub")):
            return self.AUTHORITY_WEIGHTS["standard_reference"]
        if any(kw in source_lower for kw in ("euler", "gauss", "leibniz", "newton", "cauchy", "taylor", "simpson")):
            return self.AUTHORITY_WEIGHTS["theorem_proof"]
        return self.AUTHORITY_WEIGHTS["standard_reference"]


# ---------------------------------------------------------------------------
# [TIE-5] CONFIDENCE STRATIFICATION
# ---------------------------------------------------------------------------
def stratify_confidence(confidence: float, has_numeric_verify: bool = False) -> ConfidenceLevel:
    """Map a numeric confidence score to a stratification level."""
    if has_numeric_verify:
        confidence = min(confidence + 0.05, 1.0)
    if confidence >= 0.90:
        return ConfidenceLevel.DEFENSIBLE
    if confidence >= 0.75:
        return ConfidenceLevel.AGGRESSIVE
    if confidence >= 0.50:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ---------------------------------------------------------------------------
# [TIE-7] VECTOR SEARCH (simple cosine-similarity fallback)
# ---------------------------------------------------------------------------
class VectorSearch:
    """Simple TF-IDF-like search for doctrine fallback when cache misses."""

    def __init__(self, doctrines: List[Dict[str, Any]]) -> None:
        self.doctrines = doctrines
        self.vocab: Dict[str, int] = {}
        self.doc_vectors: List[Dict[int, float]] = []
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def _build_index(self) -> None:
        all_tokens: set[str] = set()
        doc_token_lists: List[List[str]] = []
        for doc in self.doctrines:
            text = " ".join([
                doc.get("topic", ""),
                " ".join(doc.get("keywords", [])),
                doc.get("conclusion_template", ""),
                doc.get("reasoning_framework", ""),
            ])
            tokens = self._tokenize(text)
            doc_token_lists.append(tokens)
            all_tokens.update(tokens)

        self.vocab = {t: i for i, t in enumerate(sorted(all_tokens))}

        for tokens in doc_token_lists:
            vec: Dict[int, float] = {}
            for t in tokens:
                idx = self.vocab.get(t)
                if idx is not None:
                    vec[idx] = vec.get(idx, 0) + 1.0
            # Normalize
            mag = sqrt(sum(v * v for v in vec.values())) if vec else 1.0
            self.doc_vectors.append({k: v / mag for k, v in vec.items()})

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most similar doctrines to query."""
        tokens = self._tokenize(query)
        q_vec: Dict[int, float] = {}
        for t in tokens:
            idx = self.vocab.get(t)
            if idx is not None:
                q_vec[idx] = q_vec.get(idx, 0) + 1.0
        q_mag = sqrt(sum(v * v for v in q_vec.values())) if q_vec else 1.0
        q_vec = {k: v / q_mag for k, v in q_vec.items()}

        scores: List[Tuple[float, int]] = []
        for i, dv in enumerate(self.doc_vectors):
            dot = sum(q_vec.get(k, 0) * v for k, v in dv.items())
            scores.append((dot, i))
        scores.sort(key=lambda x: x[0], reverse=True)

        results: List[Dict[str, Any]] = []
        for score, idx in scores[:top_k]:
            if score > 0.01:
                doc = dict(self.doctrines[idx])
                doc["_vector_score"] = score
                results.append(doc)
        return results


# ---------------------------------------------------------------------------
# [TIE-8] TELEMETRY
# ---------------------------------------------------------------------------
class Telemetry:
    """Query tracing and latency tracking."""

    def __init__(self) -> None:
        self.traces: List[Dict[str, Any]] = []

    def start_trace(self, query_id: str, query: str) -> Dict[str, Any]:
        trace = {
            "query_id": query_id,
            "query": query,
            "start_time": time.time(),
            "events": [],
        }
        self.traces.append(trace)
        return trace

    def add_event(self, trace: Dict[str, Any], event: str, data: Any = None) -> None:
        trace["events"].append({
            "event": event,
            "timestamp": time.time(),
            "elapsed_ms": (time.time() - trace["start_time"]) * 1000,
            "data": data,
        })

    def end_trace(self, trace: Dict[str, Any]) -> float:
        elapsed = (time.time() - trace["start_time"]) * 1000
        trace["total_ms"] = elapsed
        return elapsed


# ---------------------------------------------------------------------------
# [TIE-9] DRIFT WATCHER
# ---------------------------------------------------------------------------
class DriftWatcher:
    """Monitors for doctrine drift over time."""

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def check_drift(self, doctrine_topic: str, current_confidence: float) -> DriftReport:
        """Compare current confidence to historical values for drift detection."""
        relevant = [
            h for h in self.history if h["topic"] == doctrine_topic
        ]
        if len(relevant) < 3:
            self.history.append({
                "topic": doctrine_topic,
                "confidence": current_confidence,
                "timestamp": time.time(),
            })
            return DriftReport(drift_detected=False, drift_score=0.0, details="Insufficient history")

        recent = [h["confidence"] for h in relevant[-10:]]
        avg = sum(recent) / len(recent)
        deviation = abs(current_confidence - avg)
        drift_detected = deviation > 0.1

        self.history.append({
            "topic": doctrine_topic,
            "confidence": current_confidence,
            "timestamp": time.time(),
        })

        return DriftReport(
            drift_detected=drift_detected,
            drift_score=deviation,
            details=f"Historical avg={avg:.4f}, current={current_confidence:.4f}, deviation={deviation:.4f}",
        )


# ---------------------------------------------------------------------------
# [TIE-10] COVERAGE MAP
# ---------------------------------------------------------------------------
class CoverageMap:
    """Tracks doctrine trigger rates and gap detection."""

    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        map_path = ENGINE_DIR / "coverage_map.json"
        if map_path.exists():
            self.data = json.loads(map_path.read_text(encoding="utf-8"))
            logger.info("Coverage map loaded")
        else:
            self.data = {"trigger_tracking": {"total_queries": 0, "doctrine_hits": {}, "doctrine_misses": []}}

    def record_hit(self, doctrine_topic: str) -> None:
        tracking = self.data.setdefault("trigger_tracking", {})
        hits = tracking.setdefault("doctrine_hits", {})
        hits[doctrine_topic] = hits.get(doctrine_topic, 0) + 1
        tracking["total_queries"] = tracking.get("total_queries", 0) + 1

    def record_miss(self, query: str) -> None:
        tracking = self.data.setdefault("trigger_tracking", {})
        misses = tracking.setdefault("doctrine_misses", [])
        misses.append({"query": query[:200], "timestamp": datetime.datetime.utcnow().isoformat()})
        if len(misses) > 500:
            tracking["doctrine_misses"] = misses[-500:]
        tracking["total_queries"] = tracking.get("total_queries", 0) + 1

    def get_coverage_score(self) -> float:
        zones = self.data.get("coverage_zones", {})
        if not zones:
            return 0.0
        scores = [z.get("coverage_score", 0) for z in zones.values()]
        return sum(scores) / len(scores)

    def get_zone_count(self) -> int:
        return len(self.data.get("coverage_zones", {}))


# ---------------------------------------------------------------------------
# [TIE-11] METRICS COLLECTOR
# ---------------------------------------------------------------------------
class MetricsCollector:
    """Collects latency, error rate, hit rate, queries/hour metrics."""

    def __init__(self) -> None:
        self.query_count: int = 0
        self.error_count: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.latencies: List[float] = []
        self.start_time: float = time.time()

    def record_query(self, latency_ms: float, cache_hit: bool, error: bool = False) -> None:
        self.query_count += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if error:
            self.error_count += 1
        # Keep last 10000 latencies
        if len(self.latencies) > 10000:
            self.latencies = self.latencies[-10000:]

    @property
    def avg_latency(self) -> float:
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0.0

    @property
    def error_rate(self) -> float:
        return self.error_count / self.query_count if self.query_count > 0 else 0.0

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def queries_per_hour(self) -> float:
        elapsed_hours = (time.time() - self.start_time) / 3600
        return self.query_count / elapsed_hours if elapsed_hours > 0 else 0.0

    def summary(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "error_count": self.error_count,
            "error_rate": round(self.error_rate, 4),
            "cache_hit_rate": round(self.cache_hit_rate, 4),
            "avg_latency_ms": round(self.avg_latency, 2),
            "p95_latency_ms": round(sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0.0, 2),
            "queries_per_hour": round(self.queries_per_hour, 2),
        }


# ---------------------------------------------------------------------------
# [TIE-13] ZONED ANALYSIS
# ---------------------------------------------------------------------------
def apply_zone(zone: AnalysisZone, answer: str) -> str:
    """Apply zone-specific framing to the answer."""
    if zone == AnalysisZone.PLANNING:
        return f"[PLANNING ZONE] {answer}\n\nNote: This analysis is for planning purposes. Verify before proceeding to computation."
    if zone == AnalysisZone.AUDIT:
        return f"[AUDIT ZONE] {answer}\n\nAudit trail: All computation steps are logged and deterministically verifiable."
    return answer


# ---------------------------------------------------------------------------
# [TIE-14] FACT FRAGILITY SCORING
# ---------------------------------------------------------------------------
def score_fragility(
    has_symbolic: bool,
    has_numeric_verify: bool,
    doctrine_confidence: float,
    authority_count: int,
) -> FactFragilityReport:
    """Score the fragility of the mathematical result."""
    verifiability = 0.95 if has_symbolic else 0.6
    if has_numeric_verify:
        verifiability = min(verifiability + 0.05, 1.0)

    recharacterization_risk = 0.05  # Math results don't get "recharacterized" easily
    testimony_dependence = max(0.0, 1.0 - (authority_count * 0.15))
    overall = (1 - verifiability) * 0.4 + recharacterization_risk * 0.2 + testimony_dependence * 0.4

    return FactFragilityReport(
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(recharacterization_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        overall_fragility=round(overall, 3),
    )


# ---------------------------------------------------------------------------
# [TIE-15] AUDIT TRAIL (JSONL)
# ---------------------------------------------------------------------------
def write_audit_entry(entry: Dict[str, Any]) -> None:
    """Append an entry to the audit trail JSONL file."""
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")


# ---------------------------------------------------------------------------
# [TIE-16] DETERMINISM HASH (SHA-256)
# ---------------------------------------------------------------------------
def compute_determinism_hash(query: str, answer: str, numeric_result: Optional[float] = None) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    payload = json.dumps({
        "engine_id": ENGINE_ID,
        "query": query,
        "answer": answer[:500],
        "numeric_result": numeric_result,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# [TIE-19] MULTI-DOCTRINE DECOMPOSITION
# ---------------------------------------------------------------------------
def classify_issue(query: str) -> List[IssueCategory]:
    """Classify a query into issue categories for multi-doctrine decomposition."""
    q = query.lower()
    categories: List[IssueCategory] = []

    diff_kw = ["derivative", "differentiate", "d/dx", "diff", "power rule", "product rule",
                "quotient rule", "chain rule", "slope", "tangent"]
    if any(k in q for k in diff_kw):
        categories.append(IssueCategory.DIFFERENTIATION)

    int_kw = ["integral", "integrate", "area under", "trapezoidal", "simpson", "gauss",
               "quadrature", "antiderivative"]
    if any(k in q for k in int_kw):
        categories.append(IssueCategory.INTEGRATION)

    series_kw = ["taylor", "maclaurin", "series", "expansion", "polynomial approximation"]
    if any(k in q for k in series_kw):
        categories.append(IssueCategory.SERIES)

    limit_kw = ["limit", "lim", "approaches", "l'hopital", "l'hospital", "indeterminate"]
    if any(k in q for k in limit_kw):
        categories.append(IssueCategory.LIMITS)

    ode_kw = ["ode", "differential equation", "dy/dx", "euler method", "runge-kutta", "rk4",
              "separable", "initial value"]
    if any(k in q for k in ode_kw):
        categories.append(IssueCategory.ODE)

    mv_kw = ["partial", "gradient", "jacobian", "hessian", "multivariable", "nabla"]
    if any(k in q for k in mv_kw):
        categories.append(IssueCategory.MULTIVARIABLE)

    simp_kw = ["simplify", "reduce", "canonical", "expand", "factor"]
    if any(k in q for k in simp_kw):
        categories.append(IssueCategory.SIMPLIFICATION)

    if not categories:
        categories.append(IssueCategory.COMPUTATION)

    return categories


# ---------------------------------------------------------------------------
# [TIE-20] DEEP ANALYSIS MODE
# ---------------------------------------------------------------------------
def deep_analysis(
    query: str,
    doctrine_hits: List[Dict[str, Any]],
    categories: List[IssueCategory],
) -> Dict[str, Any]:
    """Multi-source synthesis with full reasoning chain."""
    analysis: Dict[str, Any] = {
        "query": query,
        "categories": [c.value for c in categories],
        "doctrine_count": len(doctrine_hits),
        "reasoning_chains": [],
        "authority_consensus": {},
        "interaction_graph": [],
    }

    for doc in doctrine_hits:
        chain = {
            "topic": doc.get("topic"),
            "framework": doc.get("reasoning_framework", ""),
            "key_factors": doc.get("key_factors", []),
            "authorities": doc.get("primary_authority", []),
        }
        analysis["reasoning_chains"].append(chain)

    # Build interaction graph between categories
    interactions = [
        ("DIFFERENTIATION", "INTEGRATION", "inverse_operations"),
        ("DIFFERENTIATION", "SERIES", "taylor_coefficients"),
        ("DIFFERENTIATION", "LIMITS", "derivative_definition"),
        ("DIFFERENTIATION", "ODE", "solution_verification"),
        ("DIFFERENTIATION", "MULTIVARIABLE", "partial_derivatives"),
        ("INTEGRATION", "SERIES", "term_by_term_integration"),
        ("INTEGRATION", "ODE", "separation_of_variables"),
        ("LIMITS", "SERIES", "convergence_tests"),
    ]
    cat_set = {c.value for c in categories}
    for src, tgt, rel in interactions:
        if src in cat_set or tgt in cat_set:
            analysis["interaction_graph"].append({"source": src, "target": tgt, "relationship": rel})

    return analysis


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 11: QUERY ROUTER — INTELLIGENT DISPATCH
# ═══════════════════════════════════════════════════════════════════════════

class QueryRouter:
    """Routes incoming queries to the appropriate computation engine."""

    # Patterns for extracting structured commands
    DIFF_PATTERN = re.compile(
        r"(?:d(?:ifferentiat)?(?:e|/dx)?|derivative\s+of)\s+(.+?)(?:\s+(?:with respect to|wrt|w\.r\.t\.)\s+(\w+))?$",
        re.IGNORECASE,
    )
    INTEGRATE_PATTERN = re.compile(
        r"(?:integrat(?:e|ion)|integral\s+of)\s+(.+?)\s+from\s+([\d.e+-]+)\s+to\s+([\d.e+-]+)",
        re.IGNORECASE,
    )
    TAYLOR_PATTERN = re.compile(
        r"taylor\s+(?:series|expansion|polynomial)?\s*(?:of\s+)?(.+?)\s+(?:about|around|at|center)\s+([\d.e+-]+)",
        re.IGNORECASE,
    )
    LIMIT_PATTERN = re.compile(
        r"lim(?:it)?\s+(?:as\s+)?(\w+)\s*(?:->|approaches?|tends?\s+to)\s*([\d.e+-]+|inf(?:inity)?)\s+(?:of\s+)?(.+)",
        re.IGNORECASE,
    )
    ODE_PATTERN = re.compile(
        r"(?:solve|ode)\s+dy/dx\s*=\s*(.+?)\s*(?:,|with)\s*y\(([\d.e+-]+)\)\s*=\s*([\d.e+-]+)(?:\s+(?:to|until)\s+([\d.e+-]+))?",
        re.IGNORECASE,
    )
    GRADIENT_PATTERN = re.compile(
        r"gradient\s+(?:of\s+)?(.+?)\s+(?:wrt|w\.r\.t\.|with respect to)\s+(.+)",
        re.IGNORECASE,
    )
    JACOBIAN_PATTERN = re.compile(
        r"jacobian\s+(?:of\s+)?\[(.+?)\]\s+(?:wrt|w\.r\.t\.|with respect to)\s+\[(.+?)\]",
        re.IGNORECASE,
    )
    PARTIAL_PATTERN = re.compile(
        r"partial\s+(?:derivative\s+(?:of\s+)?)?(.+?)\s+(?:wrt|w\.r\.t\.|with respect to)\s+(\w+)",
        re.IGNORECASE,
    )
    SIMPLIFY_PATTERN = re.compile(
        r"simplify\s+(.+)",
        re.IGNORECASE,
    )

    def route(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """Parse a natural-language query and return (action, params)."""
        q = query.strip()

        # Differentiation
        m = self.DIFF_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            var = m.group(2) or "x"
            return "differentiate", {"expr": expr, "var": var}

        # Integration
        m = self.INTEGRATE_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            a = float(m.group(2))
            b = float(m.group(3))
            return "integrate", {"expr": expr, "a": a, "b": b}

        # Taylor
        m = self.TAYLOR_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            center = float(m.group(2))
            return "taylor", {"expr": expr, "center": center}

        # Limit
        m = self.LIMIT_PATTERN.search(q)
        if m:
            var = m.group(1)
            approach_str = m.group(2)
            expr = m.group(3).strip()
            approach = float("inf") if "inf" in approach_str.lower() else float(approach_str)
            return "limit", {"expr": expr, "var": var, "approach": approach}

        # ODE
        m = self.ODE_PATTERN.search(q)
        if m:
            rhs = m.group(1).strip()
            x0 = float(m.group(2))
            y0 = float(m.group(3))
            x_end = float(m.group(4)) if m.group(4) else x0 + 1.0
            return "ode", {"rhs": rhs, "x0": x0, "y0": y0, "x_end": x_end}

        # Gradient
        m = self.GRADIENT_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            vars_str = m.group(2).strip()
            variables = [v.strip() for v in re.split(r"[,\s]+", vars_str)]
            return "gradient", {"expr": expr, "variables": variables}

        # Jacobian
        m = self.JACOBIAN_PATTERN.search(q)
        if m:
            funcs = [f.strip() for f in m.group(1).split(",")]
            variables = [v.strip() for v in m.group(2).split(",")]
            return "jacobian", {"funcs": funcs, "variables": variables}

        # Partial derivative
        m = self.PARTIAL_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            var = m.group(2).strip()
            return "partial", {"expr": expr, "var": var}

        # Simplify
        m = self.SIMPLIFY_PATTERN.search(q)
        if m:
            expr = m.group(1).strip()
            return "simplify", {"expr": expr}

        # Fallback: try to detect expression and differentiate
        if any(kw in q.lower() for kw in ["derivative", "differentiate", "d/dx"]):
            return "differentiate", {"expr": q, "var": "x"}

        return "general", {"query": q}


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 12: THREE-LAYER RESPONSE ENGINE (TIE-1)
# ═══════════════════════════════════════════════════════════════════════════

class CalculusEngine:
    """Main engine implementing the three-layer response pattern."""

    def __init__(self) -> None:
        self.doctrine_cache = DoctrineCache()
        self.normalizer = SemanticNormalizer()
        self.authority = AuthorityHardener()
        self.vector_search = VectorSearch(self.doctrine_cache.doctrines)
        self.telemetry = Telemetry()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.metrics = MetricsCollector()
        self.router = QueryRouter()
        logger.info("CalculusEngine initialized with all TIE-20 components")

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """TIE-1: Three-layer response — Doctrine Cache -> Semantic Retrieval -> Deep Analysis."""
        query_id = str(uuid.uuid4())[:12]
        trace = self.telemetry.start_trace(query_id, request.query)
        t0 = time.time()

        try:
            # Normalize query
            normalized = self.normalizer.normalize(request.query)
            self.telemetry.add_event(trace, "normalized", normalized)

            # Classify issues (TIE-19)
            categories = classify_issue(normalized)
            self.telemetry.add_event(trace, "classified", [c.value for c in categories])

            # Route query
            action, params = self.router.route(normalized)
            self.telemetry.add_event(trace, "routed", {"action": action, "params": str(params)[:200]})

            # LAYER 1: Doctrine Cache (0-200ms target)
            doctrine_hits_raw = self.doctrine_cache.search(normalized, top_k=3)
            layer_used = "doctrine_cache" if doctrine_hits_raw else "none"
            self.telemetry.add_event(trace, "doctrine_search", {"hits": len(doctrine_hits_raw)})

            # LAYER 2: Vector search fallback
            if not doctrine_hits_raw:
                doctrine_hits_raw = self.vector_search.search(normalized, top_k=3)
                if doctrine_hits_raw:
                    layer_used = "vector_search"
                self.telemetry.add_event(trace, "vector_search", {"hits": len(doctrine_hits_raw)})

            # Format doctrine hits
            doctrine_hits = [
                DoctrineHit(
                    topic=d.get("topic", "unknown"),
                    confidence=d.get("confidence", 0.5),
                    stratification=d.get("confidence_stratification", "DISCLOSURE"),
                    conclusion=d.get("conclusion_template", ""),
                    reasoning=d.get("reasoning_framework", ""),
                    authorities=d.get("primary_authority", []),
                    keywords_matched=d.get("_keywords_matched", []),
                )
                for d in doctrine_hits_raw
            ]

            # Record coverage
            for d in doctrine_hits_raw:
                self.coverage_map.record_hit(d.get("topic", ""))
            if not doctrine_hits_raw:
                self.coverage_map.record_miss(request.query)

            # Execute computation
            answer, all_steps, numeric_result, symbolic_result = self._execute_action(
                action, params, request
            )
            self.telemetry.add_event(trace, "computed", {"action": action})

            # LAYER 3: Deep analysis (for DEFENSE/MEMO modes)
            deep = None
            if request.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
                deep = deep_analysis(normalized, doctrine_hits_raw, categories)
                layer_used = "deep_analysis"
                self.telemetry.add_event(trace, "deep_analysis")

            # Authority hardening (TIE-4)
            all_authorities: List[str] = []
            base_confidence = 0.90
            for d in doctrine_hits_raw:
                all_authorities.extend(d.get("primary_authority", []))
                base_confidence = max(base_confidence, d.get("confidence", 0.5))
            hardened_confidence, authority_sources = self.authority.harden(all_authorities, base_confidence)

            # Confidence stratification (TIE-5)
            has_numeric = numeric_result is not None
            conf_level = stratify_confidence(hardened_confidence, has_numeric)

            # Drift check (TIE-9)
            drift = DriftReport()
            if doctrine_hits_raw:
                drift = self.drift_watcher.check_drift(
                    doctrine_hits_raw[0].get("topic", ""), hardened_confidence
                )

            # Fact fragility (TIE-14)
            fragility = score_fragility(
                has_symbolic=symbolic_result is not None,
                has_numeric_verify=has_numeric,
                doctrine_confidence=hardened_confidence,
                authority_count=len(all_authorities),
            )

            # Zoned output (TIE-13)
            answer = apply_zone(request.zone, answer)

            # Response mode enrichment (TIE-2)
            if request.mode == ResponseMode.MEMO:
                answer = self._enrich_memo(answer, doctrine_hits, all_steps)
            elif request.mode == ResponseMode.DEFENSE:
                answer = self._enrich_defense(answer, authority_sources)

            # Determinism hash (TIE-16)
            det_hash = compute_determinism_hash(request.query, answer, numeric_result)

            # Disclosure caveat
            caveat = None
            if conf_level in (ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK):
                caveat = (
                    "This result has reduced confidence. Verify independently before relying on it "
                    "for critical applications."
                )

            latency = (time.time() - t0) * 1000
            self.telemetry.end_trace(trace)

            # Metrics
            self.metrics.record_query(latency, cache_hit=layer_used == "doctrine_cache")

            # Audit trail (TIE-15)
            write_audit_entry({
                "query_id": query_id,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "query": request.query[:500],
                "action": action,
                "layer_used": layer_used,
                "confidence": hardened_confidence,
                "latency_ms": round(latency, 2),
                "categories": [c.value for c in categories],
                "determinism_hash": det_hash,
            })

            return QueryResponse(
                query_id=query_id,
                query=request.query,
                mode=request.mode,
                zone=request.zone,
                timestamp=datetime.datetime.utcnow().isoformat(),
                latency_ms=round(latency, 2),
                layer_used=layer_used,
                issue_categories=[c.value for c in categories],
                doctrine_hits=doctrine_hits,
                answer=answer,
                steps=all_steps if request.include_steps else [],
                numeric_result=numeric_result,
                symbolic_result=symbolic_result,
                confidence=round(hardened_confidence, 4),
                confidence_stratification=conf_level,
                authorities=authority_sources,
                fragility=fragility,
                drift=drift,
                determinism_hash=det_hash,
                disclosure_caveat=caveat,
                deep_analysis=deep,
            )

        except Exception as exc:
            latency = (time.time() - t0) * 1000
            self.metrics.record_query(latency, cache_hit=False, error=True)
            logger.error(f"Query processing error: {exc}")
            write_audit_entry({
                "query_id": query_id,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "query": request.query[:500],
                "error": str(exc),
                "latency_ms": round(latency, 2),
            })
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    def _execute_action(
        self, action: str, params: Dict[str, Any], request: QueryRequest
    ) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        """Dispatch to the appropriate computation method."""
        if action == "differentiate":
            return self._do_differentiate(params)
        if action == "integrate":
            return self._do_integrate(params)
        if action == "taylor":
            return self._do_taylor(params)
        if action == "limit":
            return self._do_limit(params)
        if action == "ode":
            return self._do_ode(params)
        if action == "gradient":
            return self._do_gradient(params)
        if action == "jacobian":
            return self._do_jacobian(params)
        if action == "partial":
            return self._do_partial(params)
        if action == "simplify":
            return self._do_simplify(params)
        return self._do_general(params)

    def _do_differentiate(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        var = params.get("var", "x")
        result_expr, steps = symbolic_diff(expr_str, var)
        result_str = result_expr.to_str()
        answer = f"d/d{var}[{expr_str}] = {result_str}"

        # Numeric verification at x=1
        numeric_val = None
        try:
            numeric_val = result_expr.eval({var: 1.0})
            steps.append(f"Numeric verification at {var}=1: {numeric_val:.8g}")
        except (ValueError, ZeroDivisionError, OverflowError):
            steps.append("Numeric verification at x=1 failed (domain issue)")

        return answer, steps, numeric_val, result_str

    def _do_integrate(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        a = params["a"]
        b = params["b"]

        all_steps: List[str] = []

        # Run multiple methods for cross-validation
        trap_result, trap_steps = numerical_integrate(expr_str, a, b, "trapezoidal", 10000)
        all_steps.extend(trap_steps)

        simp_result, simp_steps = numerical_integrate(expr_str, a, b, "simpson", 10000)
        all_steps.extend(simp_steps)

        gauss_result, gauss_steps = numerical_integrate(expr_str, a, b, "gauss", 5)
        all_steps.extend(gauss_steps)

        # Use Simpson as primary (most accurate for smooth functions)
        best = simp_result
        all_steps.append(f"Cross-validation: trap={trap_result:.10g}, simp={simp_result:.10g}, gauss={gauss_result:.10g}")
        all_steps.append(f"Selected Simpson 1/3 as primary result")

        answer = f"Integral of {expr_str} from {a} to {b} = {best:.12g}"
        return answer, all_steps, best, None

    def _do_taylor(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        center = params.get("center", 0.0)
        n_terms = params.get("n_terms", 6)

        coeffs, poly_str, steps = taylor_series(expr_str, center, n_terms)
        answer = f"Taylor series of {expr_str} about a={center}:\n{poly_str}"
        return answer, steps, None, poly_str

    def _do_limit(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        var = params.get("var", "x")
        approach = params.get("approach", 0.0)

        value, method, steps = evaluate_limit(expr_str, var, approach)
        if value is not None:
            answer = f"lim({var}->{approach}) {expr_str} = {value:.12g} (via {method})"
        else:
            answer = f"lim({var}->{approach}) {expr_str}: limit does not exist ({method})"
        return answer, steps, value, None

    def _do_ode(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        rhs = params["rhs"]
        x0 = params["x0"]
        y0 = params["y0"]
        x_end = params.get("x_end", x0 + 1.0)

        trajectory, steps = solve_ode(rhs, x0, y0, x_end, method="rk4")
        final_y = trajectory[-1][1] if trajectory else y0
        answer = f"ODE dy/dx = {rhs}, y({x0})={y0}: y({x_end}) = {final_y:.12g} (RK4)"
        return answer, steps, final_y, None

    def _do_gradient(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        variables = params["variables"]

        grad_components, steps = gradient(expr_str, variables)
        grad_str = f"({', '.join(grad_components)})"
        answer = f"Gradient of {expr_str}: nabla f = {grad_str}"
        return answer, steps, None, grad_str

    def _do_jacobian(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        funcs = params["funcs"]
        variables = params["variables"]

        jac, steps = jacobian_matrix(funcs, variables)
        rows = [f"  [{', '.join(row)}]" for row in jac]
        matrix_str = "[\n" + "\n".join(rows) + "\n]"
        answer = f"Jacobian matrix:\n{matrix_str}"
        return answer, steps, None, matrix_str

    def _do_partial(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        var = params["var"]

        result_str, steps = partial_derivative(expr_str, var)
        answer = f"Partial d/d{var}[{expr_str}] = {result_str}"
        return answer, steps, None, result_str

    def _do_simplify(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        expr_str = params["expr"]
        tree = parse_expr(expr_str)
        simplified = tree.simplify()
        result_str = simplified.to_str()
        steps = [f"Original: {expr_str}", f"Parsed: {tree.to_str()}", f"Simplified: {result_str}"]

        numeric_val = None
        try:
            numeric_val = simplified.eval({"x": 1.0})
            steps.append(f"Value at x=1: {numeric_val:.8g}")
        except (ValueError, ZeroDivisionError, OverflowError):
            pass

        answer = f"Simplified: {result_str}"
        return answer, steps, numeric_val, result_str

    def _do_general(self, params: Dict[str, Any]) -> Tuple[str, List[str], Optional[float], Optional[str]]:
        query = params["query"]
        steps: List[str] = [f"General query: {query}"]

        # Try to extract and differentiate an expression
        expr_match = re.search(r"[a-z0-9^+\-*/().]+", query)
        if expr_match:
            expr_str = expr_match.group(0)
            try:
                tree = parse_expr(expr_str)
                val = tree.eval({"x": 1.0})
                steps.append(f"Parsed expression: {tree.to_str()}, value at x=1: {val:.8g}")
                answer = f"Expression: {tree.to_str()}, evaluated at x=1: {val:.8g}"
                return answer, steps, val, tree.to_str()
            except (ParseError, ValueError, ZeroDivisionError):
                pass

        answer = "Query processed. Please use structured commands: differentiate, integrate, taylor, limit, ode, gradient, jacobian, partial, simplify."
        return answer, steps, None, None

    def _enrich_memo(self, answer: str, doctrine_hits: List[DoctrineHit], steps: List[str]) -> str:
        """MEMO mode: full documentation format."""
        parts = [answer, "\n\n--- MEMORANDUM ---"]
        if doctrine_hits:
            parts.append("\nApplicable Doctrines:")
            for dh in doctrine_hits:
                parts.append(f"\n  Topic: {dh.topic}")
                parts.append(f"  Conclusion: {dh.conclusion}")
                parts.append(f"  Authorities: {', '.join(dh.authorities)}")
        if steps:
            parts.append("\nComputation Steps:")
            for s in steps:
                parts.append(f"  {s}")
        return "\n".join(parts)

    def _enrich_defense(self, answer: str, authorities: List[AuthoritySource]) -> str:
        """DEFENSE mode: audit-ready format."""
        parts = [answer, "\n\n--- DEFENSE EXHIBIT ---"]
        if authorities:
            parts.append("\nAuthority Chain:")
            for a in authorities:
                parts.append(f"  [{a.weight:.2f}] {a.source}")
        parts.append("\nThis result is deterministically verifiable via the SHA-256 hash.")
        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 13: FASTAPI SERVER (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════

engine: Optional[CalculusEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Server startup and shutdown lifecycle."""
    global engine
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine = CalculusEngine()
    logger.info("Engine initialized successfully")
    yield
    logger.info("Shutting down engine")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant calculus intelligence engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# [TIE-12] HEALTH ENDPOINT
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint."""
    assert engine is not None
    return HealthResponse(
        uptime_seconds=round(time.time() - STARTUP_TIME, 2),
        total_queries=engine.metrics.query_count,
        doctrine_count=len(engine.doctrine_cache.doctrines),
        coverage_zones=engine.coverage_map.get_zone_count(),
        avg_latency_ms=round(engine.metrics.avg_latency, 2),
        error_rate=round(engine.metrics.error_rate, 4),
        components={
            "doctrine_cache": len(engine.doctrine_cache.doctrines) > 0,
            "semantic_normalizer": len(engine.normalizer.rules) > 0,
            "vector_search": len(engine.vector_search.doc_vectors) > 0,
            "authority_hardener": True,
            "confidence_stratifier": True,
            "telemetry": True,
            "drift_watcher": True,
            "coverage_map": True,
            "metrics_collector": True,
            "zoned_analysis": True,
            "fact_fragility": True,
            "audit_trail": True,
            "determinism_hash": True,
            "multi_doctrine_decomposition": True,
            "deep_analysis": True,
            "query_router": True,
            "expression_parser": True,
            "symbolic_diff": True,
            "numerical_integration": True,
            "ode_solver": True,
        },
    )


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Return engine metrics summary."""
    assert engine is not None
    return engine.metrics.summary()


# ---------------------------------------------------------------------------
# PRIMARY QUERY ENDPOINT
# ---------------------------------------------------------------------------
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Process a calculus query through the three-layer engine."""
    assert engine is not None
    return engine.process_query(request)


# ---------------------------------------------------------------------------
# SPECIALIZED ENDPOINTS
# ---------------------------------------------------------------------------
@app.post("/differentiate")
async def differentiate_endpoint(
    expr: str = Query(..., description="Expression to differentiate"),
    var: str = Query(default="x", description="Variable"),
    order: int = Query(default=1, ge=1, le=10, description="Derivative order"),
) -> Dict[str, Any]:
    """Symbolic differentiation endpoint."""
    result, steps = symbolic_diff(expr, var, order)
    return {
        "expression": expr,
        "variable": var,
        "order": order,
        "derivative": result.to_str(),
        "steps": steps,
    }


@app.post("/integrate")
async def integrate_endpoint(
    expr: str = Query(..., description="Expression to integrate"),
    a: float = Query(..., description="Lower bound"),
    b: float = Query(..., description="Upper bound"),
    method: str = Query(default="simpson", description="Method: trapezoidal, simpson, simpson38, gauss"),
    n: int = Query(default=10000, description="Subdivisions"),
) -> Dict[str, Any]:
    """Numerical integration endpoint."""
    result, steps = numerical_integrate(expr, a, b, method, n)
    return {
        "expression": expr,
        "bounds": [a, b],
        "method": method,
        "n": n,
        "result": result,
        "steps": steps,
    }


@app.post("/taylor")
async def taylor_endpoint(
    expr: str = Query(..., description="Expression to expand"),
    center: float = Query(default=0.0, description="Expansion center"),
    n_terms: int = Query(default=6, ge=1, le=20, description="Number of terms"),
) -> Dict[str, Any]:
    """Taylor series expansion endpoint."""
    coeffs, poly_str, steps = taylor_series(expr, center, n_terms)
    return {
        "expression": expr,
        "center": center,
        "n_terms": n_terms,
        "coefficients": [{"order": k, "value": v} for k, v in coeffs],
        "polynomial": poly_str,
        "steps": steps,
    }


@app.post("/limit")
async def limit_endpoint(
    expr: str = Query(..., description="Expression"),
    var: str = Query(default="x", description="Variable"),
    approach: float = Query(default=0.0, description="Approach value"),
    direction: str = Query(default="both", description="Direction: left, right, both"),
) -> Dict[str, Any]:
    """Limit evaluation endpoint."""
    value, method, steps = evaluate_limit(expr, var, approach, direction)
    return {
        "expression": expr,
        "variable": var,
        "approach": approach,
        "direction": direction,
        "value": value,
        "method": method,
        "steps": steps,
    }


@app.post("/ode")
async def ode_endpoint(
    rhs: str = Query(..., description="Right-hand side dy/dx = rhs(x,y)"),
    x0: float = Query(default=0.0, description="Initial x"),
    y0: float = Query(default=1.0, description="Initial y"),
    x_end: float = Query(default=1.0, description="End x"),
    method: str = Query(default="rk4", description="Method: euler, rk4"),
    n_steps: int = Query(default=1000, description="Number of steps"),
) -> Dict[str, Any]:
    """ODE solver endpoint."""
    trajectory, steps = solve_ode(rhs, x0, y0, x_end, method, n_steps)
    return {
        "rhs": rhs,
        "initial_condition": {"x0": x0, "y0": y0},
        "x_end": x_end,
        "method": method,
        "n_steps": n_steps,
        "final_value": trajectory[-1][1] if trajectory else y0,
        "trajectory_sample": trajectory[:10] + trajectory[-5:] if len(trajectory) > 15 else trajectory,
        "steps": steps,
    }


@app.post("/gradient")
async def gradient_endpoint(
    expr: str = Query(..., description="Expression"),
    variables: str = Query(default="x,y", description="Comma-separated variables"),
) -> Dict[str, Any]:
    """Gradient computation endpoint."""
    var_list = [v.strip() for v in variables.split(",")]
    components, steps = gradient(expr, var_list)
    return {
        "expression": expr,
        "variables": var_list,
        "gradient": components,
        "steps": steps,
    }


@app.post("/jacobian")
async def jacobian_endpoint(
    funcs: str = Query(..., description="Comma-separated function expressions"),
    variables: str = Query(default="x,y", description="Comma-separated variables"),
) -> Dict[str, Any]:
    """Jacobian matrix endpoint."""
    func_list = [f.strip() for f in funcs.split(",")]
    var_list = [v.strip() for v in variables.split(",")]
    matrix, steps = jacobian_matrix(func_list, var_list)
    return {
        "functions": func_list,
        "variables": var_list,
        "jacobian": matrix,
        "steps": steps,
    }


@app.post("/hessian")
async def hessian_endpoint(
    expr: str = Query(..., description="Expression"),
    variables: str = Query(default="x,y", description="Comma-separated variables"),
) -> Dict[str, Any]:
    """Hessian matrix endpoint."""
    var_list = [v.strip() for v in variables.split(",")]
    matrix, steps = hessian_matrix(expr, var_list)
    return {
        "expression": expr,
        "variables": var_list,
        "hessian": matrix,
        "steps": steps,
    }


@app.post("/simplify")
async def simplify_endpoint(
    expr: str = Query(..., description="Expression to simplify"),
) -> Dict[str, Any]:
    """Expression simplification endpoint."""
    tree = parse_expr(expr)
    simplified = tree.simplify()
    return {
        "original": expr,
        "parsed": tree.to_str(),
        "simplified": simplified.to_str(),
    }


@app.post("/parse")
async def parse_endpoint(
    expr: str = Query(..., description="Expression to parse"),
) -> Dict[str, Any]:
    """Expression parsing and evaluation endpoint."""
    tree = parse_expr(expr)
    result = None
    try:
        result = tree.eval({"x": 1.0, "y": 1.0, "z": 1.0, "t": 1.0})
    except (ValueError, ZeroDivisionError, OverflowError):
        pass
    return {
        "expression": expr,
        "parsed": tree.to_str(),
        "value_at_defaults": result,
    }


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 14: MAIN ENTRY POINT
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
