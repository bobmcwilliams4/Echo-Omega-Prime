"""
MATH01 — Arithmetic Engine (TIE-20 Compliant)
═══════════════════════════════════════════════
Tier 13 (Mathematics) | MODE: DET | AUTH: 5.0 | PORT: 8563

Capabilities:
  - Arbitrary precision arithmetic via Python Decimal
  - Expression parsing with operator precedence (shunting-yard)
  - Number base conversion (binary/octal/hex/decimal/arbitrary)
  - GCD (Euclidean) and LCM computation
  - Prime factorization (trial division + Pollard rho)
  - Primality testing (Miller-Rabin)
  - Fraction arithmetic (Python Fraction)
  - Significant figures tracking and propagation
  - Unit conversion (length, mass, volume, temperature)
  - Modular arithmetic (mod, modpow, modinv)

TIE-20 Components:
  1. three_layer_response    2. response_modes         3. doctrine_cache
  4. authority_hardening     5. confidence_stratification
  6. semantic_normalization  7. vector_search           8. telemetry
  9. drift_watcher          10. coverage_map           11. metrics_collector
 12. health_endpoint        13. zoned_analysis         14. fact_fragility_scoring
 15. audit_trail_jsonl      16. determinism_hash_sha256
 17. fastapi_server         18. loguru_logging
 19. multi_doctrine_decomposition  20. deep_analysis_mode
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import sys
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext, ROUND_HALF_EVEN
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ─── Path setup ───────────────────────────────────────────────────────────────
ENGINE_DIR = Path(__file__).parent
SYSTEMS_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(SYSTEMS_DIR))

# ─── Loguru config ────────────────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>MATH01</cyan> | {message}",
    level="DEBUG",
)
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger.add(
    str(LOG_DIR / "math01_{time:YYYY-MM-DD}.log"),
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# ─── Decimal precision ────────────────────────────────────────────────────────
getcontext().prec = 50
getcontext().rounding = ROUND_HALF_EVEN

# ─── Constants ────────────────────────────────────────────────────────────────
ENGINE_ID = "MATH01"
ENGINE_NAME = "Arithmetic"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8563
ENGINE_TIER = 13
ENGINE_MODE = "DET"
AUTHORITY_REQUIRED = Decimal("5.0")
MAX_INPUT_LENGTH = 10_000
MAX_FACTORIZATION_LIMIT = 10**18
MILLER_RABIN_ROUNDS = 20


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Pydantic Models
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    STANDARD = "STANDARD"
    DEEP = "DEEP"
    DEFENSE = "DEFENSE"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    SUPPORTABLE = "SUPPORTABLE"
    ADVISORY = "ADVISORY"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    COMPUTATION = "COMPUTATION"
    VERIFICATION = "VERIFICATION"
    EXPLANATION = "EXPLANATION"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=MAX_INPUT_LENGTH, description="The math query to process")
    mode: ResponseMode = Field(default=ResponseMode.STANDARD, description="Response depth mode")
    authority_level: float = Field(default=5.0, ge=0.0, le=11.0, description="Caller authority level")
    session_id: Optional[str] = Field(default=None, description="Optional session tracking ID")
    precision: int = Field(default=50, ge=1, le=500, description="Decimal precision digits")
    track_sig_figs: bool = Field(default=False, description="Enable significant figures tracking")


class DoctrineHit(BaseModel):
    topic: str
    confidence: str
    keywords_matched: list[str]
    conclusion: str


class ComputationResult(BaseModel):
    raw_result: str
    formatted_result: str
    result_type: str
    precision_used: int
    significant_figures: Optional[int] = None
    steps: list[str] = Field(default_factory=list)


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query: str
    mode: str
    result: ComputationResult
    doctrine_hits: list[DoctrineHit] = Field(default_factory=list)
    confidence: str
    zone: str
    analysis: Optional[str] = None
    deep_analysis: Optional[dict[str, Any]] = None
    fragility_score: Optional[float] = None
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str
    port: int = ENGINE_PORT
    tier: int = ENGINE_TIER
    mode: str = ENGINE_MODE
    authority_required: float
    uptime_seconds: float
    total_queries: int
    error_count: int
    doctrine_count: int
    coverage_domains: list[str]
    avg_latency_ms: float
    timestamp: str


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Doctrine Cache Loader
# ═══════════════════════════════════════════════════════════════════════════════

class DoctrineCache:
    """Loads and indexes doctrine blocks from doctrine_cache.json."""

    def __init__(self) -> None:
        self.doctrines: list[dict[str, Any]] = []
        self.keyword_index: dict[str, list[int]] = defaultdict(list)
        self._load()

    def _load(self) -> None:
        cache_path = ENGINE_DIR / "doctrine_cache.json"
        if not cache_path.exists():
            logger.error("doctrine_cache.json not found at {}", cache_path)
            return
        raw = json.loads(cache_path.read_text(encoding="utf-8"))
        for idx, block in enumerate(raw):
            self.doctrines.append(block)
            for kw in block.get("keywords", []):
                self.keyword_index[kw.lower()].append(idx)
        logger.info("Loaded {} doctrine blocks, {} keywords indexed", len(self.doctrines), len(self.keyword_index))

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        tokens = set(re.findall(r"[a-z]+", query.lower()))
        scores: dict[int, float] = defaultdict(float)
        matched_kw: dict[int, list[str]] = defaultdict(list)
        for token in tokens:
            for kw, indices in self.keyword_index.items():
                if token in kw or kw in token:
                    for idx in indices:
                        scores[idx] += 1.0 if token == kw else 0.5
                        if kw not in matched_kw[idx]:
                            matched_kw[idx].append(kw)
        ranked = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)[:top_k]
        results = []
        for idx in ranked:
            doc = dict(self.doctrines[idx])
            doc["_score"] = scores[idx]
            doc["_matched_keywords"] = matched_kw[idx]
            results.append(doc)
        return results

    @property
    def count(self) -> int:
        return len(self.doctrines)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Semantic Normalizer
# ═══════════════════════════════════════════════════════════════════════════════

class SemanticNormalizer:
    """Normalizes math terminology to canonical forms."""

    def __init__(self) -> None:
        self.synonyms: dict[str, str] = {}
        self.unit_aliases: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        dict_path = ENGINE_DIR / "semantic_dict.json"
        if not dict_path.exists():
            logger.warning("semantic_dict.json not found at {}", dict_path)
            return
        data = json.loads(dict_path.read_text(encoding="utf-8"))
        self.synonyms = {k.lower(): v.lower() for k, v in data.get("synonyms", {}).items()}
        self.unit_aliases = {k.lower(): v.lower() for k, v in data.get("unit_aliases", {}).items()}
        logger.info("Loaded {} synonyms, {} unit aliases", len(self.synonyms), len(self.unit_aliases))

    def normalize_query(self, query: str) -> str:
        normalized = query.lower().strip()
        for phrase, canonical in sorted(self.synonyms.items(), key=lambda x: -len(x[0])):
            normalized = normalized.replace(phrase, canonical)
        return normalized

    def normalize_unit(self, unit: str) -> str:
        return self.unit_aliases.get(unit.lower().strip(), unit.lower().strip())


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Coverage Map
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Tracks which doctrines have been triggered and which remain untouched."""

    def __init__(self, doctrine_count: int) -> None:
        self.triggered: dict[str, int] = defaultdict(int)
        self.total_doctrines = doctrine_count

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] += 1

    def get_coverage_stats(self) -> dict[str, Any]:
        return {
            "total_doctrines": self.total_doctrines,
            "triggered_count": len(self.triggered),
            "untriggered_count": self.total_doctrines - len(self.triggered),
            "coverage_pct": round(len(self.triggered) / max(self.total_doctrines, 1) * 100, 2),
            "hit_distribution": dict(self.triggered),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Telemetry & Metrics
# ═══════════════════════════════════════════════════════════════════════════════

class Telemetry:
    """Per-query latency and error tracking."""

    def __init__(self) -> None:
        self.query_count: int = 0
        self.error_count: int = 0
        self.total_latency_ms: float = 0.0
        self.latencies: list[float] = []
        self.error_domains: dict[str, int] = defaultdict(int)

    def record_query(self, latency_ms: float) -> None:
        self.query_count += 1
        self.total_latency_ms += latency_ms
        self.latencies.append(latency_ms)
        if len(self.latencies) > 1000:
            self.latencies = self.latencies[-500:]

    def record_error(self, domain: str) -> None:
        self.error_count += 1
        self.error_domains[domain] += 1

    @property
    def avg_latency_ms(self) -> float:
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)

    def get_metrics(self) -> dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "total_errors": self.error_count,
            "error_rate": round(self.error_count / max(self.query_count, 1), 4),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "p50_latency_ms": round(sorted(self.latencies)[len(self.latencies) // 2], 2) if self.latencies else 0.0,
            "p99_latency_ms": round(sorted(self.latencies)[int(len(self.latencies) * 0.99)] if self.latencies else 0.0, 2),
            "error_domains": dict(self.error_domains),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Drift Watcher
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Monitors doctrine response consistency over time."""

    def __init__(self) -> None:
        self.baseline_hashes: dict[str, str] = {}
        self.drift_events: list[dict[str, Any]] = []

    def record_response_hash(self, query_normalized: str, response_hash: str) -> Optional[dict[str, Any]]:
        if query_normalized in self.baseline_hashes:
            if self.baseline_hashes[query_normalized] != response_hash:
                event = {
                    "query": query_normalized,
                    "expected_hash": self.baseline_hashes[query_normalized],
                    "actual_hash": response_hash,
                    "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                }
                self.drift_events.append(event)
                logger.warning("DRIFT DETECTED for query '{}': {} -> {}", query_normalized[:60], event["expected_hash"][:16], response_hash[:16])
                return event
        else:
            self.baseline_hashes[query_normalized] = response_hash
        return None

    def get_drift_summary(self) -> dict[str, Any]:
        return {
            "baselines_tracked": len(self.baseline_hashes),
            "drift_events": len(self.drift_events),
            "recent_drifts": self.drift_events[-10:],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Audit Trail
# ═══════════════════════════════════════════════════════════════════════════════

def write_audit_entry(entry: dict[str, Any]) -> None:
    """Append a JSON line to the audit trail file."""
    entry["timestamp"] = datetime.now(tz=timezone.utc).isoformat()
    entry["engine_id"] = ENGINE_ID
    try:
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.error("Failed to write audit entry: {}", exc)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Determinism Hash
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, result: str, mode: str) -> str:
    """SHA-256 hash of (query, result, mode) for reproducibility verification."""
    payload = f"{ENGINE_ID}|{query}|{result}|{mode}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: Authority Hardening
# ═══════════════════════════════════════════════════════════════════════════════

def check_authority(caller_level: float) -> None:
    """Reject requests from callers below the required authority level."""
    if Decimal(str(caller_level)) < AUTHORITY_REQUIRED:
        logger.warning("Authority rejected: caller={} required={}", caller_level, AUTHORITY_REQUIRED)
        raise HTTPException(
            status_code=403,
            detail=f"Authority level {caller_level} insufficient. Required: {AUTHORITY_REQUIRED}",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: Confidence Stratification
# ═══════════════════════════════════════════════════════════════════════════════

def classify_confidence(result_type: str, has_doctrine: bool, computation_exact: bool) -> ConfidenceLevel:
    """Determine confidence level based on computation characteristics."""
    if computation_exact and has_doctrine:
        return ConfidenceLevel.DEFENSIBLE
    if computation_exact and not has_doctrine:
        return ConfidenceLevel.SUPPORTABLE
    if not computation_exact and has_doctrine:
        return ConfidenceLevel.ADVISORY
    if result_type in ("approximation", "sig_figs"):
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11: Fact Fragility Scoring
# ═══════════════════════════════════════════════════════════════════════════════

def compute_fragility_score(
    computation_exact: bool,
    precision_digits: int,
    involves_approximation: bool,
    involves_external_data: bool,
) -> float:
    """Score from 0.0 (rock-solid) to 1.0 (highly fragile).

    Factors:
      - Exact integer arithmetic = low fragility
      - High-precision decimal = slightly higher
      - Approximations (sig figs, irrational) = moderate
      - External data dependency (unit factors) = slightly higher
    """
    score = 0.0
    if not computation_exact:
        score += 0.3
    if involves_approximation:
        score += 0.25
    if involves_external_data:
        score += 0.15
    if precision_digits < 15:
        score += 0.1
    return min(round(score, 3), 1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12: Zoned Analysis
# ═══════════════════════════════════════════════════════════════════════════════

def determine_zone(mode: ResponseMode) -> AnalysisZone:
    """Map response mode to analysis zone — never blur boundaries."""
    if mode == ResponseMode.FAST:
        return AnalysisZone.COMPUTATION
    if mode in (ResponseMode.STANDARD, ResponseMode.DEFENSE):
        return AnalysisZone.VERIFICATION
    return AnalysisZone.EXPLANATION


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13: Expression Tokenizer
# ═══════════════════════════════════════════════════════════════════════════════

class TokenType(str, Enum):
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    FUNCTION = "FUNCTION"
    COMMA = "COMMA"


class Token(BaseModel):
    type: TokenType
    value: str


OPERATOR_PRECEDENCE: dict[str, int] = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
    "**": 4,
    "^": 4,
}

RIGHT_ASSOCIATIVE = {"**", "^"}

FUNCTIONS = {"abs", "sqrt", "floor", "ceil", "factorial", "log2", "log10"}


def tokenize_expression(expr: str) -> list[Token]:
    """Convert a math expression string into a list of tokens.

    Handles:
      - Integer and decimal numbers (including scientific notation like 1.5e3)
      - Operators: + - * / // % ** ^
      - Parentheses
      - Function names: abs, sqrt, floor, ceil, factorial
      - Implicit multiplication: 2(3) becomes 2 * (3)
      - Unary minus: converts to (0 - x) form
    """
    tokens: list[Token] = []
    i = 0
    expr = expr.replace(" ", "")
    length = len(expr)

    while i < length:
        ch = expr[i]

        # Numbers (including decimals and scientific notation)
        if ch.isdigit() or (ch == "." and i + 1 < length and expr[i + 1].isdigit()):
            start = i
            while i < length and (expr[i].isdigit() or expr[i] == "."):
                i += 1
            # Scientific notation
            if i < length and expr[i] in ("e", "E"):
                i += 1
                if i < length and expr[i] in ("+", "-"):
                    i += 1
                while i < length and expr[i].isdigit():
                    i += 1
            num_str = expr[start:i]
            # Implicit multiplication: number followed by '(' or function
            if tokens and tokens[-1].type == TokenType.RPAREN:
                pass  # already handled
            tokens.append(Token(type=TokenType.NUMBER, value=num_str))
            # Check for implicit multiplication: 2( or 2sqrt
            if i < length and (expr[i] == "(" or expr[i].isalpha()):
                tokens.append(Token(type=TokenType.OPERATOR, value="*"))
            continue

        # Function names or constants
        if ch.isalpha() or ch == "_":
            start = i
            while i < length and (expr[i].isalnum() or expr[i] == "_"):
                i += 1
            name = expr[start:i]
            if name.lower() in FUNCTIONS:
                tokens.append(Token(type=TokenType.FUNCTION, value=name.lower()))
            elif name.lower() == "pi":
                tokens.append(Token(type=TokenType.NUMBER, value=str(Decimal("3.14159265358979323846264338327950288419716939937510"))))
                if i < length and (expr[i] == "(" or expr[i].isalpha()):
                    tokens.append(Token(type=TokenType.OPERATOR, value="*"))
            elif name.lower() == "e":
                tokens.append(Token(type=TokenType.NUMBER, value=str(Decimal("2.71828182845904523536028747135266249775724709369995"))))
                if i < length and (expr[i] == "(" or expr[i].isalpha()):
                    tokens.append(Token(type=TokenType.OPERATOR, value="*"))
            else:
                raise ValueError(f"Unknown identifier: '{name}'")
            continue

        # Parentheses
        if ch == "(":
            # Implicit multiplication: )(
            if tokens and tokens[-1].type in (TokenType.NUMBER, TokenType.RPAREN):
                tokens.append(Token(type=TokenType.OPERATOR, value="*"))
            tokens.append(Token(type=TokenType.LPAREN, value="("))
            i += 1
            continue

        if ch == ")":
            tokens.append(Token(type=TokenType.RPAREN, value=")"))
            i += 1
            # Implicit multiplication: )( or )number or )func
            if i < length and (expr[i].isdigit() or expr[i].isalpha() or expr[i] == "("):
                if i < length and expr[i] != ")" and not (i < length and expr[i] in "+-*/%^,"):
                    # Check it's not an operator next
                    if expr[i] not in "+-*/%^,)":
                        tokens.append(Token(type=TokenType.OPERATOR, value="*"))
            continue

        # Two-character operators
        if ch == "*" and i + 1 < length and expr[i + 1] == "*":
            tokens.append(Token(type=TokenType.OPERATOR, value="**"))
            i += 2
            continue

        if ch == "/" and i + 1 < length and expr[i + 1] == "/":
            tokens.append(Token(type=TokenType.OPERATOR, value="//"))
            i += 2
            continue

        # Unary minus/plus handling
        if ch in "+-":
            is_unary = (
                not tokens
                or tokens[-1].type == TokenType.OPERATOR
                or tokens[-1].type == TokenType.LPAREN
                or tokens[-1].type == TokenType.COMMA
            )
            if is_unary:
                # Convert unary -x to (0-x) and unary +x to (0+x)
                tokens.append(Token(type=TokenType.LPAREN, value="("))
                tokens.append(Token(type=TokenType.NUMBER, value="0"))
                tokens.append(Token(type=TokenType.OPERATOR, value=ch))
                # We need to find the extent of the unary operand
                # For simplicity, just push the operator; the closing paren
                # will be added after the next number/subexpression
                i += 1
                # Read the next token, then close paren
                # Actually, let the shunting-yard handle it by wrapping
                # We'll use a simpler approach: just treat it as 0+/- and continue
                # The paren will need to be closed — track depth
                # Simpler: just insert 0 and the operator, no extra parens needed
                # if expression is like -3+2, it becomes (0-3)+2 which is wrong
                # We need: just let it be 0-3+2 which evaluates correctly as (-3)+2
                # So remove the lparen we just added
                tokens.pop(0 if len(tokens) == 1 else -3)  # remove the LPAREN
                # Actually let's redo this cleanly:
                tokens_to_remove = 3  # lparen, 0, operator
                for _ in range(tokens_to_remove):
                    tokens.pop()
                # Simple approach: just insert "0" before the minus
                tokens.append(Token(type=TokenType.NUMBER, value="0"))
                tokens.append(Token(type=TokenType.OPERATOR, value=ch))
                i += 0  # already incremented
                continue
            else:
                tokens.append(Token(type=TokenType.OPERATOR, value=ch))
                i += 1
                continue

        # Single-character operators
        if ch in "*/%" or ch == "^":
            tokens.append(Token(type=TokenType.OPERATOR, value=ch))
            i += 1
            continue

        if ch == ",":
            tokens.append(Token(type=TokenType.COMMA, value=","))
            i += 1
            continue

        raise ValueError(f"Unexpected character: '{ch}' at position {i}")

    return tokens


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14: Shunting-Yard Parser + Evaluator
# ═══════════════════════════════════════════════════════════════════════════════

def shunting_yard(tokens: list[Token]) -> list[Token]:
    """Convert infix tokens to postfix (RPN) using the shunting-yard algorithm."""
    output: list[Token] = []
    op_stack: list[Token] = []

    for token in tokens:
        if token.type == TokenType.NUMBER:
            output.append(token)

        elif token.type == TokenType.FUNCTION:
            op_stack.append(token)

        elif token.type == TokenType.COMMA:
            while op_stack and op_stack[-1].type != TokenType.LPAREN:
                output.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Mismatched parentheses or misplaced comma")

        elif token.type == TokenType.OPERATOR:
            while (
                op_stack
                and op_stack[-1].type == TokenType.OPERATOR
                and (
                    (token.value not in RIGHT_ASSOCIATIVE and OPERATOR_PRECEDENCE.get(token.value, 0) <= OPERATOR_PRECEDENCE.get(op_stack[-1].value, 0))
                    or (token.value in RIGHT_ASSOCIATIVE and OPERATOR_PRECEDENCE.get(token.value, 0) < OPERATOR_PRECEDENCE.get(op_stack[-1].value, 0))
                )
            ):
                output.append(op_stack.pop())
            op_stack.append(token)

        elif token.type == TokenType.LPAREN:
            op_stack.append(token)

        elif token.type == TokenType.RPAREN:
            while op_stack and op_stack[-1].type != TokenType.LPAREN:
                output.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Mismatched parentheses: extra closing ')'")
            op_stack.pop()  # Remove the LPAREN
            if op_stack and op_stack[-1].type == TokenType.FUNCTION:
                output.append(op_stack.pop())

    while op_stack:
        if op_stack[-1].type == TokenType.LPAREN:
            raise ValueError("Mismatched parentheses: unclosed '('")
        output.append(op_stack.pop())

    return output


def evaluate_rpn(rpn_tokens: list[Token], precision: int = 50) -> Decimal:
    """Evaluate a postfix (RPN) token list and return a Decimal result."""
    ctx = getcontext()
    old_prec = ctx.prec
    ctx.prec = precision
    try:
        stack: list[Decimal] = []

        for token in rpn_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(Decimal(token.value))

            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator '{token.value}'")
                b = stack.pop()
                a = stack.pop()
                if token.value == "+":
                    stack.append(a + b)
                elif token.value == "-":
                    stack.append(a - b)
                elif token.value == "*":
                    stack.append(a * b)
                elif token.value == "/":
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif token.value == "//":
                    if b == 0:
                        raise ZeroDivisionError("Floor division by zero")
                    stack.append(Decimal(int(a // b)))
                elif token.value == "%":
                    if b == 0:
                        raise ZeroDivisionError("Modulo by zero")
                    stack.append(a % b)
                elif token.value in ("**", "^"):
                    if a == 0 and b < 0:
                        raise ZeroDivisionError("0 raised to negative power")
                    # For integer exponents, compute exactly
                    if b == int(b) and abs(int(b)) <= 10000:
                        stack.append(a ** int(b))
                    else:
                        # Use ln/exp approximation for non-integer exponents
                        if a <= 0:
                            raise ValueError(f"Cannot raise non-positive {a} to non-integer power {b}")
                        result = Decimal(str(float(a) ** float(b)))
                        stack.append(result)
                else:
                    raise ValueError(f"Unknown operator: '{token.value}'")

            elif token.type == TokenType.FUNCTION:
                if not stack:
                    raise ValueError(f"No argument for function '{token.value}'")
                arg = stack.pop()
                if token.value == "abs":
                    stack.append(abs(arg))
                elif token.value == "sqrt":
                    if arg < 0:
                        raise ValueError("Square root of negative number")
                    stack.append(arg.sqrt())
                elif token.value == "floor":
                    stack.append(Decimal(math.floor(arg)))
                elif token.value == "ceil":
                    stack.append(Decimal(math.ceil(arg)))
                elif token.value == "factorial":
                    if arg < 0 or arg != int(arg):
                        raise ValueError("Factorial requires non-negative integer")
                    if int(arg) > 10000:
                        raise ValueError("Factorial argument too large (max 10000)")
                    stack.append(Decimal(math.factorial(int(arg))))
                elif token.value == "log2":
                    if arg <= 0:
                        raise ValueError("log2 requires positive argument")
                    stack.append(Decimal(str(math.log2(float(arg)))))
                elif token.value == "log10":
                    if arg <= 0:
                        raise ValueError("log10 requires positive argument")
                    stack.append(Decimal(str(math.log10(float(arg)))))
                else:
                    raise ValueError(f"Unknown function: '{token.value}'")

        if len(stack) != 1:
            raise ValueError(f"Invalid expression: stack has {len(stack)} values after evaluation")

        return stack[0]
    finally:
        ctx.prec = old_prec


def evaluate_expression(expr: str, precision: int = 50) -> tuple[Decimal, list[str]]:
    """Full pipeline: tokenize -> shunting-yard -> evaluate. Returns (result, steps)."""
    steps: list[str] = []
    steps.append(f"Input expression: {expr}")

    tokens = tokenize_expression(expr)
    steps.append(f"Tokenized: {len(tokens)} tokens")

    rpn = shunting_yard(tokens)
    rpn_str = " ".join(t.value for t in rpn)
    steps.append(f"RPN (postfix): {rpn_str}")

    result = evaluate_rpn(rpn, precision)
    steps.append(f"Result: {result}")

    return result, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15: Number Base Conversion
# ═══════════════════════════════════════════════════════════════════════════════

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base_10(value_str: str, from_base: int) -> int:
    """Convert a string in a given base to a base-10 integer."""
    if from_base < 2 or from_base > 36:
        raise ValueError(f"Base must be 2-36, got {from_base}")
    value_str = value_str.upper().strip()
    negative = value_str.startswith("-")
    if negative:
        value_str = value_str[1:]
    # Remove common prefixes
    if from_base == 16 and value_str.startswith("0X"):
        value_str = value_str[2:]
    elif from_base == 8 and value_str.startswith("0O"):
        value_str = value_str[2:]
    elif from_base == 2 and value_str.startswith("0B"):
        value_str = value_str[2:]

    result = 0
    for char in value_str:
        digit_val = DIGITS.index(char)
        if digit_val >= from_base:
            raise ValueError(f"Digit '{char}' is invalid for base {from_base}")
        result = result * from_base + digit_val
    return -result if negative else result


def from_base_10(value: int, to_base: int) -> str:
    """Convert a base-10 integer to a string in the target base."""
    if to_base < 2 or to_base > 36:
        raise ValueError(f"Base must be 2-36, got {to_base}")
    if value == 0:
        return "0"
    negative = value < 0
    value = abs(value)
    result_digits: list[str] = []
    while value > 0:
        result_digits.append(DIGITS[value % to_base])
        value //= to_base
    result = "".join(reversed(result_digits))
    return f"-{result}" if negative else result


def convert_base(value_str: str, from_base: int, to_base: int) -> tuple[str, list[str]]:
    """Convert a number between arbitrary bases. Returns (result, steps)."""
    steps: list[str] = []
    steps.append(f"Converting '{value_str}' from base {from_base} to base {to_base}")

    base10_val = to_base_10(value_str, from_base)
    steps.append(f"Base-10 intermediate: {base10_val}")

    result = from_base_10(base10_val, to_base)
    prefix = ""
    if to_base == 2:
        prefix = "0b"
    elif to_base == 8:
        prefix = "0o"
    elif to_base == 16:
        prefix = "0x"
    display = f"{prefix}{result}"
    steps.append(f"Base-{to_base} result: {display}")

    return display, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 16: GCD, LCM, Extended Euclidean
# ═══════════════════════════════════════════════════════════════════════════════

def gcd(a: int, b: int) -> int:
    """Euclidean algorithm for GCD."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm. Returns (gcd, x, y) where a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def lcm(a: int, b: int) -> int:
    """Least common multiple via GCD."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)


def multi_gcd(values: list[int]) -> int:
    """GCD of multiple values."""
    result = values[0]
    for v in values[1:]:
        result = gcd(result, v)
    return result


def multi_lcm(values: list[int]) -> int:
    """LCM of multiple values."""
    result = values[0]
    for v in values[1:]:
        result = lcm(result, v)
    return result


def compute_gcd_lcm(a: int, b: int) -> tuple[dict[str, Any], list[str]]:
    """Compute GCD and LCM with full steps."""
    steps: list[str] = []
    steps.append(f"Computing GCD({a}, {b}) and LCM({a}, {b})")

    # Show Euclidean algorithm steps
    x, y = abs(a), abs(b)
    steps.append(f"Euclidean algorithm on ({x}, {y}):")
    while y:
        steps.append(f"  {x} = {y} * {x // y} + {x % y}")
        x, y = y, x % y
    g = x
    steps.append(f"GCD = {g}")

    l = lcm(a, b)
    steps.append(f"LCM = |{a} * {b}| / GCD = {abs(a * b)} / {g} = {l}")

    # Extended Euclidean
    g2, bx, by = extended_gcd(a, b)
    steps.append(f"Bezout: {a}*({bx}) + {b}*({by}) = {g2}")

    return {
        "gcd": g,
        "lcm": l,
        "bezout_x": bx,
        "bezout_y": by,
        "coprime": g == 1,
    }, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17: Primality Testing (Miller-Rabin)
# ═══════════════════════════════════════════════════════════════════════════════

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
    317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
    607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
    701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
    811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
    911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997,
]
SMALL_PRIMES_SET = set(SMALL_PRIMES)


def miller_rabin_test(n: int, rounds: int = MILLER_RABIN_ROUNDS) -> bool:
    """Miller-Rabin probabilistic primality test. Returns True if probably prime."""
    if n < 2:
        return False
    if n in SMALL_PRIMES_SET:
        return True
    if any(n % p == 0 for p in SMALL_PRIMES if p < n):
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Deterministic witnesses for small n
    if n < 3_317_044_064_679_887_385_961_981:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        witnesses = [random.randrange(2, n - 1) for _ in range(rounds)]

    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        found = False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                found = True
                break
        if not found:
            return False
    return True


def is_prime(n: int) -> tuple[bool, list[str]]:
    """Check primality with step tracking."""
    steps: list[str] = []
    steps.append(f"Testing primality of {n}")

    if n < 2:
        steps.append(f"{n} < 2, not prime by definition")
        return False, steps

    if n in SMALL_PRIMES_SET:
        steps.append(f"{n} found in small primes lookup table")
        return True, steps

    for p in SMALL_PRIMES:
        if n % p == 0:
            steps.append(f"{n} is divisible by {p}, composite")
            return False, steps

    steps.append(f"No small prime divisor found, running Miller-Rabin ({MILLER_RABIN_ROUNDS} rounds)")
    result = miller_rabin_test(n, MILLER_RABIN_ROUNDS)
    steps.append(f"Miller-Rabin result: {'probably prime' if result else 'composite'}")
    return result, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 18: Prime Factorization (Trial Division + Pollard Rho)
# ═══════════════════════════════════════════════════════════════════════════════

def pollard_rho(n: int) -> int:
    """Pollard's rho algorithm to find a non-trivial factor of n."""
    if n % 2 == 0:
        return 2
    for attempt in range(50):
        c = random.randrange(1, n)
        f = lambda x: (x * x + c) % n  # noqa: E731
        x = random.randrange(2, n)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        if d != n:
            return d
    return n  # Failed


def prime_factorization(n: int) -> tuple[list[tuple[int, int]], list[str]]:
    """Return sorted list of (prime, exponent) pairs with steps."""
    steps: list[str] = []
    steps.append(f"Factoring {n}")

    if n < 2:
        steps.append("No prime factorization for n < 2")
        return [], steps

    factors: dict[int, int] = {}
    original = n

    # Extract powers of 2
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    if 2 in factors:
        steps.append(f"Extracted 2^{factors[2]}")

    # Trial division by odd numbers up to sqrt or 10^6
    trial_limit = min(int(n**0.5) + 1, 1_000_000)
    d = 3
    while d <= trial_limit and n > 1:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
            steps.append(f"Found factor {d} (trial division)")
        d += 2
        if d * d > n:
            break

    # If remaining n is composite and large, use Pollard's rho
    if n > 1:
        if miller_rabin_test(n):
            factors[n] = factors.get(n, 0) + 1
            steps.append(f"Remaining {n} is prime")
        else:
            steps.append(f"Remaining {n} is composite, applying Pollard's rho")
            to_factor = [n]
            while to_factor:
                val = to_factor.pop()
                if miller_rabin_test(val):
                    factors[val] = factors.get(val, 0) + 1
                    steps.append(f"  Prime factor found: {val}")
                elif val > 1:
                    divisor = pollard_rho(val)
                    if divisor == val:
                        # Fallback: brute force
                        for dd in range(3, int(val**0.5) + 1, 2):
                            if val % dd == 0:
                                divisor = dd
                                break
                    if divisor != val:
                        steps.append(f"  Pollard rho split {val} -> {divisor} * {val // divisor}")
                        to_factor.append(divisor)
                        to_factor.append(val // divisor)
                    else:
                        factors[val] = factors.get(val, 0) + 1
                        steps.append(f"  Treating {val} as prime (rho exhausted)")

    result = sorted(factors.items())
    factored_str = " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in result)
    steps.append(f"Factorization of {original} = {factored_str}")
    return result, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 19: Fraction Arithmetic
# ═══════════════════════════════════════════════════════════════════════════════

def parse_fraction(s: str) -> Fraction:
    """Parse a string into a Fraction. Supports: '3/4', '1 3/4' (mixed), '0.75', '3'."""
    s = s.strip()
    # Mixed number: "1 3/4"
    mixed_match = re.match(r"^(-?\d+)\s+(\d+)/(\d+)$", s)
    if mixed_match:
        whole = int(mixed_match.group(1))
        num = int(mixed_match.group(2))
        den = int(mixed_match.group(3))
        if den == 0:
            raise ValueError("Denominator cannot be zero")
        sign = -1 if whole < 0 else 1
        return Fraction(sign * (abs(whole) * den + num), den)

    # Simple fraction: "3/4"
    frac_match = re.match(r"^(-?\d+)/(-?\d+)$", s)
    if frac_match:
        num = int(frac_match.group(1))
        den = int(frac_match.group(2))
        if den == 0:
            raise ValueError("Denominator cannot be zero")
        return Fraction(num, den)

    # Decimal or integer
    return Fraction(s)


def fraction_operation(op: str, operands: list[str]) -> tuple[dict[str, Any], list[str]]:
    """Perform a fraction arithmetic operation. op: add, sub, mul, div, simplify, to_mixed."""
    steps: list[str] = []
    fractions = [parse_fraction(o) for o in operands]
    steps.append(f"Parsed fractions: {[str(f) for f in fractions]}")

    if op == "simplify" and len(fractions) >= 1:
        f = fractions[0]
        steps.append(f"Simplifying {operands[0]} -> {f}")
        return {
            "result": str(f),
            "numerator": f.numerator,
            "denominator": f.denominator,
            "decimal": float(f),
        }, steps

    if op == "to_mixed" and len(fractions) >= 1:
        f = fractions[0]
        whole = int(f)
        remainder = abs(f) - abs(whole)
        if remainder == 0:
            result_str = str(whole)
        else:
            rem_frac = Fraction(remainder).limit_denominator(10000)
            sign = "-" if f < 0 else ""
            result_str = f"{sign}{abs(whole)} {rem_frac}" if whole != 0 else f"{sign}{rem_frac}"
        steps.append(f"Mixed number: {result_str}")
        return {"result": result_str, "decimal": float(f)}, steps

    if len(fractions) < 2:
        raise ValueError("Binary fraction operations require at least 2 operands")

    a, b = fractions[0], fractions[1]
    if op == "add":
        result = a + b
        steps.append(f"{a} + {b} = {result}")
    elif op == "sub":
        result = a - b
        steps.append(f"{a} - {b} = {result}")
    elif op == "mul":
        result = a * b
        steps.append(f"{a} * {b} = {result}")
    elif op == "div":
        if b == 0:
            raise ZeroDivisionError("Division by zero fraction")
        result = a / b
        steps.append(f"{a} / {b} = {result}")
    else:
        raise ValueError(f"Unknown fraction operation: '{op}'")

    # Chain remaining operands
    for extra in fractions[2:]:
        if op == "add":
            result = result + extra
        elif op == "sub":
            result = result - extra
        elif op == "mul":
            result = result * extra
        elif op == "div":
            if extra == 0:
                raise ZeroDivisionError("Division by zero fraction")
            result = result / extra
        steps.append(f"  -> {result}")

    return {
        "result": str(result),
        "numerator": result.numerator,
        "denominator": result.denominator,
        "decimal": float(result),
    }, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 20: Modular Arithmetic
# ═══════════════════════════════════════════════════════════════════════════════

def mod_inverse(a: int, m: int) -> int:
    """Modular inverse of a mod m using extended Euclidean algorithm."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"Modular inverse of {a} mod {m} does not exist (GCD={g})")
    return x % m


def modular_operation(op: str, a: int, b: int, m: int) -> tuple[dict[str, Any], list[str]]:
    """Perform modular arithmetic. op: mod, add, mul, pow, inv."""
    steps: list[str] = []

    if m <= 0:
        raise ValueError("Modulus must be positive")

    if op == "mod":
        result = a % m
        steps.append(f"{a} mod {m} = {result}")
    elif op == "add":
        result = (a + b) % m
        steps.append(f"({a} + {b}) mod {m} = {result}")
    elif op == "mul":
        result = (a * b) % m
        steps.append(f"({a} * {b}) mod {m} = {result}")
    elif op == "pow":
        result = pow(a, b, m)
        steps.append(f"pow({a}, {b}, {m}) = {result} (square-and-multiply)")
    elif op == "inv":
        result = mod_inverse(a, m)
        steps.append(f"Modular inverse of {a} mod {m} = {result}")
        steps.append(f"Verification: {a} * {result} mod {m} = {(a * result) % m}")
    else:
        raise ValueError(f"Unknown modular operation: '{op}'")

    return {"result": result, "a": a, "b": b, "modulus": m, "operation": op}, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 21: Significant Figures
# ═══════════════════════════════════════════════════════════════════════════════

def count_sig_figs(value_str: str) -> int:
    """Count the number of significant figures in a numeric string."""
    value_str = value_str.strip()
    # Remove sign
    if value_str.startswith(("+", "-")):
        value_str = value_str[1:]
    # Handle scientific notation
    if "e" in value_str.lower():
        mantissa = value_str.lower().split("e")[0]
        return count_sig_figs(mantissa)
    # Remove leading zeros (not significant)
    if "." in value_str:
        # Has decimal point
        integer_part, decimal_part = value_str.split(".", 1)
        if integer_part.lstrip("0") == "" or integer_part == "":
            # Like 0.0045 — leading zeros in decimal not significant
            stripped = decimal_part.lstrip("0")
            return len(stripped) if stripped else 1
        else:
            # Like 12.340 — all digits count, trailing zeros after decimal are significant
            combined = integer_part.lstrip("0") + decimal_part
            return len(combined)
    else:
        # No decimal point — trailing zeros are ambiguous, count them as NOT significant
        stripped = value_str.lstrip("0")
        if not stripped:
            return 1
        return len(stripped.rstrip("0")) if stripped.rstrip("0") else len(stripped)


def apply_sig_figs(value: Decimal, sig_figs: int) -> str:
    """Round a Decimal to the specified number of significant figures."""
    if value == 0:
        return "0"
    if sig_figs < 1:
        sig_figs = 1

    # Use scientific notation approach
    sign = "-" if value < 0 else ""
    abs_val = abs(value)
    # Number of digits before decimal
    if abs_val >= 1:
        digits_before = len(str(int(abs_val)))
    else:
        digits_before = 0
        temp = abs_val
        while temp < 1:
            temp *= 10
            digits_before -= 1
        digits_before += 1  # adjust

    # Round to sig_figs significant figures
    if abs_val == 0:
        return "0"

    from decimal import ROUND_HALF_EVEN as RHE
    shift = sig_figs - 1 - int(abs_val.log10()) if abs_val > 0 else 0
    factor = Decimal(10) ** shift
    rounded = (abs_val * factor).quantize(Decimal("1"), rounding=RHE) / factor

    # Format with appropriate decimal places
    result = f"{sign}{rounded}"
    return result


def sig_figs_propagation(operation: str, operands: list[str]) -> tuple[dict[str, Any], list[str]]:
    """Compute result with significant figures propagation."""
    steps: list[str] = []
    sf_counts = [count_sig_figs(o) for o in operands]
    values = [Decimal(o) for o in operands]
    steps.append(f"Operands: {operands}")
    steps.append(f"Sig figs: {sf_counts}")

    if operation in ("add", "sub"):
        # Result has decimal places of least precise operand
        # Find the operand with fewest decimal places
        decimal_places = []
        for o in operands:
            if "." in o:
                dp = len(o.split(".")[1].rstrip("0")) if o.split(".")[1].rstrip("0") else 0
                decimal_places.append(dp)
            else:
                decimal_places.append(0)
        min_dp = min(decimal_places) if decimal_places else 0
        steps.append(f"Decimal places: {decimal_places}, using min={min_dp}")
        if operation == "add":
            raw = sum(values)
        else:
            raw = values[0] - values[1]
        result = raw.quantize(Decimal(10) ** (-min_dp), rounding=ROUND_HALF_EVEN)
        steps.append(f"Result rounded to {min_dp} decimal places: {result}")

    elif operation in ("mul", "div"):
        # Result has sig figs of least precise operand
        min_sf = min(sf_counts)
        steps.append(f"Using minimum sig figs: {min_sf}")
        if operation == "mul":
            raw = values[0] * values[1]
            for v in values[2:]:
                raw *= v
        else:
            if values[1] == 0:
                raise ZeroDivisionError("Division by zero")
            raw = values[0] / values[1]
        result_str = apply_sig_figs(raw, min_sf)
        result = Decimal(result_str)
        steps.append(f"Result with {min_sf} sig figs: {result}")
    else:
        raise ValueError(f"Unknown sig figs operation: '{operation}'")
        result = Decimal("0")

    return {
        "result": str(result),
        "sig_figs_input": sf_counts,
        "sig_figs_output": count_sig_figs(str(result)),
        "operation": operation,
    }, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 22: Unit Conversion
# ═══════════════════════════════════════════════════════════════════════════════

# All length factors are to meters
LENGTH_TO_METERS: dict[str, Decimal] = {
    "meter": Decimal("1"),
    "kilometer": Decimal("1000"),
    "centimeter": Decimal("0.01"),
    "millimeter": Decimal("0.001"),
    "micrometer": Decimal("0.000001"),
    "nanometer": Decimal("0.000000001"),
    "mile": Decimal("1609.344"),
    "yard": Decimal("0.9144"),
    "foot": Decimal("0.3048"),
    "inch": Decimal("0.0254"),
    "nautical_mile": Decimal("1852"),
    "light_year": Decimal("9460730472580800"),
    "astronomical_unit": Decimal("149597870700"),
}

# All mass factors are to kilograms
MASS_TO_KG: dict[str, Decimal] = {
    "kilogram": Decimal("1"),
    "gram": Decimal("0.001"),
    "milligram": Decimal("0.000001"),
    "microgram": Decimal("0.000000001"),
    "metric_ton": Decimal("1000"),
    "pound": Decimal("0.45359237"),
    "ounce": Decimal("0.028349523125"),
    "stone": Decimal("6.35029318"),
    "short_ton": Decimal("907.18474"),
    "long_ton": Decimal("1016.0469088"),
    "troy_ounce": Decimal("0.0311035"),
}

# All volume factors are to liters
VOLUME_TO_LITERS: dict[str, Decimal] = {
    "liter": Decimal("1"),
    "milliliter": Decimal("0.001"),
    "cubic_meter": Decimal("1000"),
    "cubic_centimeter": Decimal("0.001"),
    "cubic_inch": Decimal("0.016387064"),
    "cubic_foot": Decimal("28.316846592"),
    "us_gallon": Decimal("3.785411784"),
    "us_quart": Decimal("0.946352946"),
    "us_pint": Decimal("0.473176473"),
    "us_cup": Decimal("0.2365882365"),
    "us_fluid_ounce": Decimal("0.0295735295625"),
    "tablespoon": Decimal("0.01478676478125"),
    "teaspoon": Decimal("0.00492892159375"),
    "imperial_gallon": Decimal("4.54609"),
    "imperial_pint": Decimal("0.56826125"),
    "imperial_fluid_ounce": Decimal("0.0284130625"),
}

UNIT_DIMENSIONS: dict[str, str] = {}
for u in LENGTH_TO_METERS:
    UNIT_DIMENSIONS[u] = "length"
for u in MASS_TO_KG:
    UNIT_DIMENSIONS[u] = "mass"
for u in VOLUME_TO_LITERS:
    UNIT_DIMENSIONS[u] = "volume"
for u in ("celsius", "fahrenheit", "kelvin", "rankine"):
    UNIT_DIMENSIONS[u] = "temperature"


def convert_temperature(value: Decimal, from_unit: str, to_unit: str) -> Decimal:
    """Convert between temperature scales."""
    # First convert to Kelvin
    if from_unit == "celsius":
        kelvin = value + Decimal("273.15")
    elif from_unit == "fahrenheit":
        kelvin = (value - Decimal("32")) * Decimal("5") / Decimal("9") + Decimal("273.15")
    elif from_unit == "kelvin":
        kelvin = value
    elif from_unit == "rankine":
        kelvin = value * Decimal("5") / Decimal("9")
    else:
        raise ValueError(f"Unknown temperature unit: '{from_unit}'")

    if kelvin < 0:
        raise ValueError(f"Temperature {value} {from_unit} is below absolute zero")

    # Convert from Kelvin to target
    if to_unit == "celsius":
        return kelvin - Decimal("273.15")
    if to_unit == "fahrenheit":
        return (kelvin - Decimal("273.15")) * Decimal("9") / Decimal("5") + Decimal("32")
    if to_unit == "kelvin":
        return kelvin
    if to_unit == "rankine":
        return kelvin * Decimal("9") / Decimal("5")
    raise ValueError(f"Unknown temperature unit: '{to_unit}'")


def convert_units(value: Decimal, from_unit: str, to_unit: str) -> tuple[dict[str, Any], list[str]]:
    """Convert value between units. Returns (result_dict, steps)."""
    steps: list[str] = []
    steps.append(f"Converting {value} {from_unit} to {to_unit}")

    from_dim = UNIT_DIMENSIONS.get(from_unit)
    to_dim = UNIT_DIMENSIONS.get(to_unit)

    if from_dim is None:
        raise ValueError(f"Unknown unit: '{from_unit}'")
    if to_dim is None:
        raise ValueError(f"Unknown unit: '{to_unit}'")
    if from_dim != to_dim:
        raise ValueError(f"Cannot convert between dimensions: {from_dim} and {to_dim}")

    if from_dim == "temperature":
        result = convert_temperature(value, from_unit, to_unit)
        steps.append(f"Temperature conversion: {value} {from_unit} = {result} {to_unit}")
    elif from_dim == "length":
        meters = value * LENGTH_TO_METERS[from_unit]
        result = meters / LENGTH_TO_METERS[to_unit]
        steps.append(f"{value} {from_unit} -> {meters} meters -> {result} {to_unit}")
    elif from_dim == "mass":
        kg = value * MASS_TO_KG[from_unit]
        result = kg / MASS_TO_KG[to_unit]
        steps.append(f"{value} {from_unit} -> {kg} kg -> {result} {to_unit}")
    elif from_dim == "volume":
        liters = value * VOLUME_TO_LITERS[from_unit]
        result = liters / VOLUME_TO_LITERS[to_unit]
        steps.append(f"{value} {from_unit} -> {liters} liters -> {result} {to_unit}")
    else:
        raise ValueError(f"Unsupported dimension: {from_dim}")

    return {
        "result": str(result),
        "from_value": str(value),
        "from_unit": from_unit,
        "to_unit": to_unit,
        "dimension": from_dim,
    }, steps


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 23: Query Classifier / Router
# ═══════════════════════════════════════════════════════════════════════════════

class QueryType(str, Enum):
    EXPRESSION = "expression"
    BASE_CONVERSION = "base_conversion"
    PRIME_FACTORIZATION = "prime_factorization"
    PRIMALITY_TEST = "primality_test"
    GCD_LCM = "gcd_lcm"
    FRACTION = "fraction"
    MODULAR = "modular"
    SIG_FIGS = "sig_figs"
    UNIT_CONVERSION = "unit_conversion"
    GENERAL = "general"


def classify_query(query: str, normalized: str) -> QueryType:
    """Determine the type of math query to route to the correct handler."""
    q = normalized.lower()

    # Unit conversion patterns
    unit_patterns = [
        r"\b\d+\.?\d*\s*(meter|kilometer|mile|foot|feet|inch|yard|cm|mm|km|mi|ft|in|yd)\b.*\bto\b",
        r"\b\d+\.?\d*\s*(kilogram|gram|pound|ounce|lb|kg|oz|mg|stone|ton)\b.*\bto\b",
        r"\b\d+\.?\d*\s*(liter|gallon|cup|quart|pint|ml|fl oz|tbsp|tsp)\b.*\bto\b",
        r"\b\d+\.?\d*\s*(celsius|fahrenheit|kelvin|rankine)\b.*\bto\b",
        r"\bunit_conversion\b",
        r"\bconversion\b.*\bunit\b",
    ]
    for pat in unit_patterns:
        if re.search(pat, q):
            return QueryType.UNIT_CONVERSION

    # Sig figs
    if re.search(r"\bsig(nificant)?\s*(fig(ure)?s?|digit)", q) or "significant_figures" in q:
        return QueryType.SIG_FIGS

    # Base conversion
    if re.search(r"\b(binary|octal|hex(adecimal)?|base_conversion|base\s*\d+)\b", q):
        return QueryType.BASE_CONVERSION
    if re.search(r"\bbase\s*\d+\s*(to|->)\s*base\s*\d+", q):
        return QueryType.BASE_CONVERSION
    if re.search(r"\b0[xXbBoO][0-9a-fA-F]+\b", query):
        return QueryType.BASE_CONVERSION

    # Prime factorization
    if re.search(r"\b(prime_factorization|factor(ize)?|prime\s*factor|decompose)\b", q):
        return QueryType.PRIME_FACTORIZATION

    # Primality test
    if re.search(r"\b(is\s*prime|primality|primality_testing|prime\s*test)\b", q):
        return QueryType.PRIMALITY_TEST

    # GCD / LCM
    if re.search(r"\b(greatest_common_divisor|least_common_multiple|gcd|lcm|gcf|hcf|coprime)\b", q):
        return QueryType.GCD_LCM

    # Fraction
    if re.search(r"\b(fraction_arithmetic|fraction|numerator|denominator|simplify|mixed\s*number)\b", q):
        return QueryType.FRACTION
    if re.search(r"\d+/\d+\s*[+\-*/]\s*\d+/\d+", query):
        return QueryType.FRACTION

    # Modular arithmetic
    if re.search(r"\b(modular_arithmetic|modular|modulo|congruence)\b", q):
        return QueryType.MODULAR
    if re.search(r"\bmod\s+\d+", q):
        return QueryType.MODULAR

    # Default: expression evaluation
    if re.search(r"[\d\.\+\-\*/\^\(\)%]", query):
        return QueryType.EXPRESSION

    return QueryType.GENERAL


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 24: Multi-Doctrine Decomposition
# ═══════════════════════════════════════════════════════════════════════════════

def decompose_query(query: str, query_type: QueryType, doctrine_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Break a complex query into sub-issues and map to doctrine topics."""
    sub_issues: list[dict[str, str]] = []

    if query_type == QueryType.EXPRESSION:
        sub_issues.append({"category": "parsing", "description": "Tokenize and parse expression with operator precedence"})
        sub_issues.append({"category": "evaluation", "description": "Evaluate parsed expression with arbitrary precision"})
        if "%" in query or "mod" in query.lower():
            sub_issues.append({"category": "modular", "description": "Modular arithmetic component detected"})

    elif query_type == QueryType.PRIME_FACTORIZATION:
        sub_issues.append({"category": "factorization", "description": "Decompose integer into prime factors"})
        sub_issues.append({"category": "primality", "description": "Verify each factor is prime via Miller-Rabin"})

    elif query_type == QueryType.GCD_LCM:
        sub_issues.append({"category": "gcd", "description": "Compute GCD via Euclidean algorithm"})
        sub_issues.append({"category": "lcm", "description": "Derive LCM from GCD relationship"})
        sub_issues.append({"category": "bezout", "description": "Compute Bezout coefficients via extended Euclidean"})

    elif query_type == QueryType.UNIT_CONVERSION:
        sub_issues.append({"category": "unit_parsing", "description": "Identify source and target units"})
        sub_issues.append({"category": "dimension_check", "description": "Verify units are in the same dimension"})
        sub_issues.append({"category": "conversion", "description": "Apply conversion factor chain"})

    elif query_type == QueryType.FRACTION:
        sub_issues.append({"category": "parsing", "description": "Parse fraction notation (simple, mixed, decimal)"})
        sub_issues.append({"category": "operation", "description": "Perform arithmetic operation"})
        sub_issues.append({"category": "simplification", "description": "Reduce result to lowest terms"})

    elif query_type == QueryType.SIG_FIGS:
        sub_issues.append({"category": "counting", "description": "Count significant figures in each operand"})
        sub_issues.append({"category": "propagation", "description": "Apply appropriate propagation rule"})
        sub_issues.append({"category": "rounding", "description": "Round result per sig figs rules"})

    else:
        sub_issues.append({"category": "general", "description": "Process general arithmetic query"})

    doctrine_topics = [d.get("topic", "unknown") for d in doctrine_hits]

    return {
        "query_type": query_type.value,
        "sub_issues": sub_issues,
        "doctrine_topics_matched": doctrine_topics,
        "interaction_count": len(sub_issues),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 25: Deep Analysis Mode
# ═══════════════════════════════════════════════════════════════════════════════

def deep_analysis(
    query: str,
    query_type: QueryType,
    result: ComputationResult,
    doctrine_hits: list[dict[str, Any]],
    decomposition: dict[str, Any],
) -> dict[str, Any]:
    """Multi-source synthesis with full reasoning chain for DEEP / DEFENSE modes."""
    analysis: dict[str, Any] = {
        "reasoning_chain": [],
        "authority_citations": [],
        "alternative_methods": [],
        "edge_cases_considered": [],
        "verification": {},
    }

    # Build reasoning chain from doctrine frameworks
    for doc in doctrine_hits:
        framework = doc.get("reasoning_framework", [])
        for step in framework[:5]:
            analysis["reasoning_chain"].append(step)
        for auth in doc.get("primary_authority", []):
            if auth not in analysis["authority_citations"]:
                analysis["authority_citations"].append(auth)

    # Alternative methods by query type
    if query_type == QueryType.PRIME_FACTORIZATION:
        analysis["alternative_methods"] = [
            "Trial division (guaranteed for small factors)",
            "Pollard's rho (probabilistic, fast for medium factors)",
            "Quadratic sieve (efficient for 50-100 digit numbers)",
            "General number field sieve (state of art for 100+ digits)",
        ]
    elif query_type == QueryType.GCD_LCM:
        analysis["alternative_methods"] = [
            "Euclidean algorithm (standard, O(log min(a,b)))",
            "Binary GCD / Stein's algorithm (avoids division)",
            "Prime factorization comparison (educational, less efficient)",
        ]
    elif query_type == QueryType.EXPRESSION:
        analysis["alternative_methods"] = [
            "Shunting-yard algorithm (this engine's method)",
            "Recursive descent parser",
            "Pratt parser (top-down operator precedence)",
        ]

    # Edge cases
    if query_type == QueryType.EXPRESSION:
        analysis["edge_cases_considered"] = [
            "Division by zero",
            "Overflow for large exponents",
            "Unary minus handling",
            "Empty parentheses",
            "Implicit multiplication",
        ]
    elif query_type == QueryType.UNIT_CONVERSION:
        analysis["edge_cases_considered"] = [
            "Cross-dimension conversion rejection",
            "Below absolute zero for temperature",
            "US vs Imperial unit disambiguation",
            "Precision preservation through conversion chain",
        ]

    # Verification
    analysis["verification"] = {
        "determinism_hash": result.raw_result,
        "computation_type": result.result_type,
        "precision_digits": result.precision_used,
    }

    return analysis


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 26: Three-Layer Response Engine
# ═══════════════════════════════════════════════════════════════════════════════

def extract_numbers_from_query(query: str) -> list[int]:
    """Extract integer values from a query string."""
    return [int(x) for x in re.findall(r"-?\d+", query)]


def extract_decimal_operands(query: str) -> list[str]:
    """Extract decimal number strings from a query."""
    return re.findall(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?", query)


def detect_fraction_operation(query: str) -> tuple[str, list[str]]:
    """Detect fraction operation and operands from query."""
    q = query.lower()
    # Pattern: fraction add 1/3 2/3
    match = re.match(r"(add|sub|mul|div|simplify|to_mixed)\s+(.*)", q)
    if match:
        op = match.group(1)
        operand_str = match.group(2).strip()
        operands = re.split(r"\s+", operand_str)
        return op, operands

    # Pattern: 1/3 + 2/3
    frac_op_match = re.search(r"(\d+/\d+)\s*([+\-*/])\s*(\d+/\d+)", query)
    if frac_op_match:
        op_map = {"+": "add", "-": "sub", "*": "mul", "/": "div"}
        return op_map.get(frac_op_match.group(2), "add"), [frac_op_match.group(1), frac_op_match.group(3)]

    return "simplify", re.findall(r"\d+/\d+|\d+\s+\d+/\d+", query)[:1] or ["1/1"]


def detect_base_conversion(query: str) -> tuple[str, int, int]:
    """Detect base conversion parameters from query."""
    # Pattern: convert 255 base 10 to base 16
    m = re.search(r"(\w+)\s+base\s*(\d+)\s*(?:to|->)\s*base\s*(\d+)", query, re.IGNORECASE)
    if m:
        return m.group(1), int(m.group(2)), int(m.group(3))

    # Pattern: 0xFF to binary / decimal / octal
    hex_m = re.search(r"0[xX]([0-9a-fA-F]+)", query)
    if hex_m:
        target = 10
        if "binary" in query.lower():
            target = 2
        elif "octal" in query.lower():
            target = 8
        return hex_m.group(1), 16, target

    bin_m = re.search(r"0[bB]([01]+)", query)
    if bin_m:
        target = 10
        if "hex" in query.lower():
            target = 16
        elif "octal" in query.lower():
            target = 8
        return bin_m.group(1), 2, target

    oct_m = re.search(r"0[oO]([0-7]+)", query)
    if oct_m:
        target = 10
        if "hex" in query.lower():
            target = 16
        elif "binary" in query.lower():
            target = 2
        return oct_m.group(1), 8, target

    # Pattern: 255 to hex / binary / octal
    num_m = re.search(r"(\d+)\s+to\s+(hex|binary|octal|decimal)", query, re.IGNORECASE)
    if num_m:
        base_map = {"hex": 16, "binary": 2, "octal": 8, "decimal": 10}
        return num_m.group(1), 10, base_map.get(num_m.group(2).lower(), 10)

    return "0", 10, 10


def detect_unit_conversion(query: str, normalizer: SemanticNormalizer) -> tuple[Decimal, str, str]:
    """Parse unit conversion query. Returns (value, from_unit, to_unit)."""
    # Pattern: 100 celsius to fahrenheit
    m = re.search(
        r"(-?\d+\.?\d*)\s*(\w[\w\s]*?)\s+to\s+(\w[\w\s]*?)(?:\s|$)",
        query.strip(),
        re.IGNORECASE,
    )
    if m:
        value = Decimal(m.group(1))
        from_unit = normalizer.normalize_unit(m.group(2).strip())
        to_unit = normalizer.normalize_unit(m.group(3).strip())
        return value, from_unit, to_unit

    raise ValueError(f"Could not parse unit conversion from: '{query}'")


def detect_modular_params(query: str) -> tuple[str, int, int, int]:
    """Parse modular arithmetic parameters. Returns (op, a, b, m)."""
    q = query.lower()

    # Pattern: 7 mod 3
    simple_mod = re.search(r"(-?\d+)\s+mod\s+(\d+)", q)
    if simple_mod:
        return "mod", int(simple_mod.group(1)), 0, int(simple_mod.group(2))

    # Pattern: modpow(a, b, m) or pow(a, b, m)
    pow_m = re.search(r"(?:mod\s*)?pow\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", q)
    if pow_m:
        return "pow", int(pow_m.group(1)), int(pow_m.group(2)), int(pow_m.group(3))

    # Pattern: modinv(a, m)
    inv_m = re.search(r"(?:mod\s*)?inv(?:erse)?\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", q)
    if inv_m:
        return "inv", int(inv_m.group(1)), 0, int(inv_m.group(2))

    # Pattern: (a + b) mod m or (a * b) mod m
    arith_mod = re.search(r"\(?\s*(\d+)\s*([+*])\s*(\d+)\s*\)?\s*mod\s+(\d+)", q)
    if arith_mod:
        op_map = {"+": "add", "*": "mul"}
        return op_map[arith_mod.group(2)], int(arith_mod.group(1)), int(arith_mod.group(3)), int(arith_mod.group(4))

    nums = extract_numbers_from_query(query)
    if len(nums) >= 2:
        return "mod", nums[0], 0, nums[1]
    raise ValueError(f"Could not parse modular arithmetic from: '{query}'")


def three_layer_response(
    request: QueryRequest,
    doctrine_cache: DoctrineCache,
    normalizer: SemanticNormalizer,
    coverage: CoverageMap,
) -> QueryResponse:
    """Main response engine implementing the three-layer TIE pattern.

    Layer 1 (FAST): Doctrine cache lookup, 0-200ms target
    Layer 2 (RETRIEVAL): Semantic search + computation
    Layer 3 (DEEP): Full analysis with reasoning chain
    """
    start_time = time.perf_counter()
    query = request.query.strip()
    normalized = normalizer.normalize_query(query)
    mode = request.mode
    precision = request.precision

    # ── Classify query ────────────────────────────────────────────────────
    query_type = classify_query(query, normalized)
    logger.info("Query classified as {} | mode={}", query_type.value, mode.value)

    # ── Layer 1: Doctrine cache lookup ────────────────────────────────────
    hits = doctrine_cache.search(normalized, top_k=3)
    doctrine_hit_models: list[DoctrineHit] = []
    for h in hits:
        topic = h.get("topic", "unknown")
        coverage.record_hit(topic)
        doctrine_hit_models.append(DoctrineHit(
            topic=topic,
            confidence=h.get("confidence", "ADVISORY"),
            keywords_matched=h.get("_matched_keywords", []),
            conclusion=h.get("conclusion_template", ""),
        ))

    # ── Layer 2: Computation ──────────────────────────────────────────────
    raw_result = ""
    formatted_result = ""
    result_type = "exact"
    steps: list[str] = []
    computation_exact = True
    involves_approximation = False
    involves_external = False
    sig_figs_out: Optional[int] = None

    try:
        if query_type == QueryType.EXPRESSION:
            # Strip any leading text like "calculate", "compute", "what is"
            expr = re.sub(r"^(calculate|compute|evaluate|what\s+is|expression_evaluation)\s*:?\s*", "", query, flags=re.IGNORECASE).strip()
            if not expr:
                expr = query
            val, steps = evaluate_expression(expr, precision)
            raw_result = str(val)
            # Clean trailing zeros for display
            if "." in raw_result:
                formatted_result = raw_result.rstrip("0").rstrip(".")
            else:
                formatted_result = raw_result
            result_type = "exact"

        elif query_type == QueryType.BASE_CONVERSION:
            val_str, from_b, to_b = detect_base_conversion(query)
            formatted_result, steps = convert_base(val_str, from_b, to_b)
            raw_result = formatted_result
            result_type = "base_conversion"

        elif query_type == QueryType.PRIME_FACTORIZATION:
            nums = extract_numbers_from_query(query)
            if not nums:
                raise ValueError("No integer found for factorization")
            n = abs(nums[0])
            if n > MAX_FACTORIZATION_LIMIT:
                raise ValueError(f"Number {n} exceeds factorization limit ({MAX_FACTORIZATION_LIMIT})")
            factors, steps = prime_factorization(n)
            factored_str = " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors)
            raw_result = factored_str
            formatted_result = f"{n} = {factored_str}" if factors else f"{n} has no prime factorization"
            result_type = "factorization"

        elif query_type == QueryType.PRIMALITY_TEST:
            nums = extract_numbers_from_query(query)
            if not nums:
                raise ValueError("No integer found for primality test")
            n = abs(nums[0])
            prime_result, steps = is_prime(n)
            raw_result = str(prime_result)
            formatted_result = f"{n} is {'prime' if prime_result else 'composite'}"
            result_type = "primality"

        elif query_type == QueryType.GCD_LCM:
            nums = extract_numbers_from_query(query)
            if len(nums) < 2:
                raise ValueError("GCD/LCM requires at least 2 integers")
            if len(nums) == 2:
                result_dict, steps = compute_gcd_lcm(nums[0], nums[1])
            else:
                g = multi_gcd(nums)
                l = multi_lcm(nums)
                result_dict = {"gcd": g, "lcm": l, "coprime": g == 1}
                steps = [f"GCD({nums}) = {g}", f"LCM({nums}) = {l}"]
            raw_result = json.dumps(result_dict, default=str)
            formatted_result = f"GCD = {result_dict['gcd']}, LCM = {result_dict['lcm']}"
            if result_dict.get("coprime"):
                formatted_result += " (coprime)"
            result_type = "gcd_lcm"

        elif query_type == QueryType.FRACTION:
            op, operands = detect_fraction_operation(query)
            result_dict, steps = fraction_operation(op, operands)
            raw_result = result_dict["result"]
            formatted_result = f"{raw_result} (decimal: {result_dict.get('decimal', 'N/A')})"
            result_type = "fraction"

        elif query_type == QueryType.MODULAR:
            op, a, b, m = detect_modular_params(query)
            result_dict, steps = modular_operation(op, a, b, m)
            raw_result = str(result_dict["result"])
            formatted_result = raw_result
            result_type = "modular"

        elif query_type == QueryType.SIG_FIGS:
            operands = extract_decimal_operands(query)
            if not operands:
                raise ValueError("No numeric operands found for sig figs calculation")
            if len(operands) == 1:
                sf = count_sig_figs(operands[0])
                raw_result = str(sf)
                formatted_result = f"'{operands[0]}' has {sf} significant figure(s)"
                steps = [f"Counting sig figs in '{operands[0]}': {sf}"]
                result_type = "sig_figs_count"
            else:
                op = "mul"
                for token in ("add", "sub", "mul", "div", "+", "-", "*", "/"):
                    if token in query.lower():
                        op_map = {"+": "add", "-": "sub", "*": "mul", "/": "div"}
                        op = op_map.get(token, token)
                        break
                result_dict, steps = sig_figs_propagation(op, operands[:2])
                raw_result = result_dict["result"]
                formatted_result = f"{raw_result} ({result_dict['sig_figs_output']} sig figs)"
                result_type = "sig_figs"
                involves_approximation = True
                sig_figs_out = result_dict["sig_figs_output"]

        elif query_type == QueryType.UNIT_CONVERSION:
            value, from_u, to_u = detect_unit_conversion(query, normalizer)
            result_dict, steps = convert_units(value, from_u, to_u)
            raw_result = result_dict["result"]
            # Format nicely
            try:
                dec_result = Decimal(raw_result)
                if dec_result == int(dec_result):
                    formatted_result = f"{int(dec_result)} {to_u}"
                else:
                    formatted_result = f"{dec_result} {to_u}"
            except (InvalidOperation, ValueError):
                formatted_result = f"{raw_result} {to_u}"
            result_type = "unit_conversion"
            involves_external = True

        else:
            # General: try expression evaluation as fallback
            try:
                val, steps = evaluate_expression(query, precision)
                raw_result = str(val)
                formatted_result = raw_result
                result_type = "expression_fallback"
            except (ValueError, ZeroDivisionError):
                raw_result = "Unable to compute"
                formatted_result = raw_result
                result_type = "error"
                computation_exact = False
                steps = [f"Could not parse query: {query}"]

    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raw_result = f"ERROR: {exc}"
        formatted_result = raw_result
        result_type = "error"
        computation_exact = False
        steps.append(f"Error: {exc}")
        logger.error("Computation error for '{}': {}", query[:80], exc)

    # ── Build result model ────────────────────────────────────────────────
    comp_result = ComputationResult(
        raw_result=raw_result,
        formatted_result=formatted_result,
        result_type=result_type,
        precision_used=precision,
        significant_figures=sig_figs_out,
        steps=steps if mode != ResponseMode.FAST else steps[:3],
    )

    # ── Confidence ────────────────────────────────────────────────────────
    confidence = classify_confidence(result_type, len(hits) > 0, computation_exact)

    # ── Zone ──────────────────────────────────────────────────────────────
    zone = determine_zone(mode)

    # ── Fragility ─────────────────────────────────────────────────────────
    fragility = compute_fragility_score(computation_exact, precision, involves_approximation, involves_external)

    # ── Deep analysis (DEEP and DEFENSE modes only) ───────────────────────
    decomposition = decompose_query(query, query_type, hits)
    deep = None
    analysis_text: Optional[str] = None
    if mode in (ResponseMode.DEEP, ResponseMode.DEFENSE):
        deep = deep_analysis(query, query_type, comp_result, hits, decomposition)
        analysis_text = f"Query decomposed into {decomposition['interaction_count']} sub-issues across {len(hits)} doctrine topics."
    elif mode == ResponseMode.STANDARD:
        analysis_text = f"Computed via {query_type.value} handler with {confidence.value} confidence."

    # ── Determinism hash ──────────────────────────────────────────────────
    det_hash = compute_determinism_hash(query, raw_result, mode.value)

    # ── Latency ───────────────────────────────────────────────────────────
    latency_ms = (time.perf_counter() - start_time) * 1000

    # ── Build response ────────────────────────────────────────────────────
    return QueryResponse(
        query=query,
        mode=mode.value,
        result=comp_result,
        doctrine_hits=doctrine_hit_models,
        confidence=confidence.value,
        zone=zone.value,
        analysis=analysis_text,
        deep_analysis=deep,
        fragility_score=fragility,
        determinism_hash=det_hash,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 27: Global State
# ═══════════════════════════════════════════════════════════════════════════════

START_TIME = time.time()
doctrine_cache_instance = DoctrineCache()
semantic_normalizer = SemanticNormalizer()
coverage_map = CoverageMap(doctrine_cache_instance.count)
telemetry = Telemetry()
drift_watcher = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 28: FastAPI Application
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    logger.info("MATH01 Arithmetic Engine v{} starting on port {}", ENGINE_VERSION, ENGINE_PORT)
    logger.info("Loaded {} doctrines, {} semantic synonyms", doctrine_cache_instance.count, len(semantic_normalizer.synonyms))
    yield
    logger.info("MATH01 shutting down. Total queries: {}", telemetry.query_count)


app = FastAPI(
    title=f"ECHO PRIME — {ENGINE_ID} {ENGINE_NAME}",
    description="TIE-20 compliant arithmetic engine: expression parsing, base conversion, primes, GCD/LCM, fractions, sig figs, unit conversion, modular arithmetic.",
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


# ─── Health endpoint ──────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    coverage_stats = coverage_map.get_coverage_stats()
    cov_path = ENGINE_DIR / "coverage_map.json"
    domains: list[str] = []
    if cov_path.exists():
        cov_data = json.loads(cov_path.read_text(encoding="utf-8"))
        domains = list(cov_data.get("covered_domains", {}).keys())
    return HealthResponse(
        status="healthy",
        authority_required=float(AUTHORITY_REQUIRED),
        uptime_seconds=round(time.time() - START_TIME, 1),
        total_queries=telemetry.query_count,
        error_count=telemetry.error_count,
        doctrine_count=doctrine_cache_instance.count,
        coverage_domains=domains,
        avg_latency_ms=round(telemetry.avg_latency_ms, 2),
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
    )


# ─── Query endpoint ──────────────────────────────────────────────────────────
@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest) -> QueryResponse:
    check_authority(request.authority_level)

    response = three_layer_response(
        request,
        doctrine_cache_instance,
        semantic_normalizer,
        coverage_map,
    )

    telemetry.record_query(response.latency_ms)
    if response.result.result_type == "error":
        telemetry.record_error("computation")

    drift_watcher.record_response_hash(
        semantic_normalizer.normalize_query(request.query),
        response.determinism_hash,
    )

    write_audit_entry({
        "query": request.query,
        "mode": request.mode.value,
        "result_type": response.result.result_type,
        "confidence": response.confidence,
        "latency_ms": response.latency_ms,
        "determinism_hash": response.determinism_hash,
        "session_id": request.session_id,
    })

    return response


# ─── Metrics endpoint ─────────────────────────────────────────────────────────
@app.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "telemetry": telemetry.get_metrics(),
        "coverage": coverage_map.get_coverage_stats(),
        "drift": drift_watcher.get_drift_summary(),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


# ─── Coverage endpoint ────────────────────────────────────────────────────────
@app.get("/coverage")
async def get_coverage() -> dict[str, Any]:
    return coverage_map.get_coverage_stats()


# ─── Doctrine list endpoint ──────────────────────────────────────────────────
@app.get("/doctrines")
async def list_doctrines() -> list[dict[str, Any]]:
    return [
        {"topic": d["topic"], "confidence": d.get("confidence", "ADVISORY"), "keywords": d.get("keywords", [])}
        for d in doctrine_cache_instance.doctrines
    ]


# ─── Direct computation endpoints (convenience) ──────────────────────────────
@app.get("/compute/evaluate")
async def compute_evaluate(expr: str, precision: int = 50) -> dict[str, Any]:
    """Direct expression evaluation endpoint."""
    val, steps = evaluate_expression(expr, precision)
    return {"expression": expr, "result": str(val), "steps": steps}


@app.get("/compute/base")
async def compute_base(value: str, from_base: int = 10, to_base: int = 16) -> dict[str, Any]:
    """Direct base conversion endpoint."""
    result, steps = convert_base(value, from_base, to_base)
    return {"value": value, "from_base": from_base, "to_base": to_base, "result": result, "steps": steps}


@app.get("/compute/factor")
async def compute_factor(n: int) -> dict[str, Any]:
    """Direct prime factorization endpoint."""
    if abs(n) > MAX_FACTORIZATION_LIMIT:
        raise HTTPException(400, f"Number exceeds limit ({MAX_FACTORIZATION_LIMIT})")
    factors, steps = prime_factorization(abs(n))
    return {"n": n, "factors": [{"prime": p, "exponent": e} for p, e in factors], "steps": steps}


@app.get("/compute/isprime")
async def compute_isprime(n: int) -> dict[str, Any]:
    """Direct primality test endpoint."""
    result, steps = is_prime(abs(n))
    return {"n": n, "is_prime": result, "steps": steps}


@app.get("/compute/gcd")
async def compute_gcd_endpoint(a: int, b: int) -> dict[str, Any]:
    """Direct GCD/LCM endpoint."""
    result, steps = compute_gcd_lcm(a, b)
    return {"a": a, "b": b, **result, "steps": steps}


@app.get("/compute/fraction")
async def compute_fraction(op: str, operands: str) -> dict[str, Any]:
    """Direct fraction operation. operands is comma-separated (e.g., '1/3,2/3')."""
    ops = [o.strip() for o in operands.split(",")]
    result, steps = fraction_operation(op, ops)
    return {"operation": op, "operands": ops, **result, "steps": steps}


@app.get("/compute/convert")
async def compute_convert(value: float, from_unit: str, to_unit: str) -> dict[str, Any]:
    """Direct unit conversion endpoint."""
    from_u = semantic_normalizer.normalize_unit(from_unit)
    to_u = semantic_normalizer.normalize_unit(to_unit)
    result, steps = convert_units(Decimal(str(value)), from_u, to_u)
    return {"value": value, "from_unit": from_u, "to_unit": to_u, **result, "steps": steps}


@app.get("/compute/mod")
async def compute_mod(a: int, m: int, op: str = "mod", b: int = 0) -> dict[str, Any]:
    """Direct modular arithmetic endpoint."""
    result, steps = modular_operation(op, a, b, m)
    return {**result, "steps": steps}


@app.get("/compute/sigfigs")
async def compute_sigfigs(value: str) -> dict[str, Any]:
    """Count significant figures in a value."""
    sf = count_sig_figs(value)
    return {"value": value, "significant_figures": sf}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 29: Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("Launching {} v{} on port {}", ENGINE_ID, ENGINE_VERSION, ENGINE_PORT)
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
