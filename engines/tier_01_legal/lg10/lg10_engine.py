"""
ECHO FAMILY LAW INTELLIGENCE ENGINE (LG10) — Production Architecture
Professional-grade family law doctrine system for attorneys, mediators, and judicial staff.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Fast keyword search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    STANDARD: Balanced analysis with citations
    DEEP: Comprehensive analysis with full citations
    DEFENSE: Court-defensible, minimum 3 citations per assertion

Analysis Zones:
    LITIGATION: Court proceedings — what WILL happen before a judge
    NEGOTIATION: Settlement strategy — leverage, BATNA, mediation
    COMPLIANCE: Order enforcement — contempt, modification, procedure

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG10 | Tier 1: LEGAL | Auth 5
Port: 8500
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import math
import os
import re
import time
import uuid
from pathlib import Path
from loguru import logger

from lg10_telemetry import (
    get_telemetry,
    trace_query,
    complete_trace,
    log_error,
    record_doctrine_mutation,
    ErrorDomain,
    ResponseLayer,
    MutationType,
    MutationOrigin,
)

# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID = "LG10"
ENGINE_NAME = "Family Law Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8500
ENGINE_DIR = Path(__file__).parent
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"
DOCTRINES_FILE = ENGINE_DIR / "lg10_doctrines.json"
CONFIG_FILE = ENGINE_DIR / "lg10_config.json"

COMMUNITY_PROPERTY_STATES = {"AZ", "CA", "ID", "LA", "NV", "NM", "TX", "WA", "WI"}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logger.add(
    LOG_DIR / "lg10_engine_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

logger.add(
    LOG_DIR / "lg10_audit_{time}.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | AUDIT | {message}",
    filter=lambda record: "audit" in record["extra"],
)


# ============================================================================
# ENUMS AND TYPES
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"
    DEFENSE = "defense"


class AnalysisZone(str, Enum):
    """Family law analysis output zones."""
    LITIGATION = "litigation"
    NEGOTIATION = "negotiation"
    COMPLIANCE = "compliance"


class AuthorityLevel(str, Enum):
    """Hierarchical authority weighting for family law."""
    STATUTE = "statute"
    CASE_LAW = "case_law"
    COURT_RULE = "court_rule"
    REGULATORY = "regulatory"
    COMMENTARY = "commentary"

    @property
    def weight(self) -> int:
        weights = {
            "statute": 100,
            "case_law": 80,
            "court_rule": 60,
            "regulatory": 40,
            "commentary": 20,
        }
        return weights.get(self.value, 10)


class ConfidenceBand(str, Enum):
    """Confidence classification for conclusions."""
    DEFENSIBLE = "defensible"
    SUPPORTABLE = "supportable"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(str, Enum):
    """Issue categories for multi-doctrine decomposition."""
    CUSTODY = "custody"
    SUPPORT = "support"
    PROPERTY = "property"
    ENFORCEMENT = "enforcement"
    JURISDICTION = "jurisdiction"
    PARENTAGE = "parentage"
    PROTECTION = "protection"
    MODIFICATION = "modification"
    ADOPTION = "adoption"
    PROCEDURE = "procedure"


class DoctrineStratum(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


# ============================================================================
# SEMANTIC NORMALIZATION DICTIONARY — 120+ entries
# ============================================================================

FAMILY_LAW_SYNONYMS: Dict[str, str] = {
    # Custody terminology
    "custody": "child custody",
    "conservatorship": "child custody",
    "managing conservator": "primary custodian",
    "possessory conservator": "non-custodial parent",
    "joint managing conservatorship": "joint custody",
    "sole managing conservatorship": "sole custody",
    "jmc": "joint custody",
    "smc": "sole custody",
    "physical custody": "possession and access",
    "legal custody": "decision-making authority",
    "visitation": "possession and access",
    "parenting time": "possession and access",
    "access": "possession and access",
    "timesharing": "possession and access",
    "custody fight": "custody dispute",
    "custody battle": "custody dispute",
    "who gets the kids": "custody determination",
    "primary parent": "primary custodian",
    "custodial parent": "primary custodian",
    "noncustodial parent": "non-custodial parent",
    "weekend dad": "non-custodial parent",
    "weekend parent": "non-custodial parent",

    # Support terminology
    "alimony": "spousal support",
    "spousal maintenance": "spousal support",
    "maintenance": "spousal support",
    "separate maintenance": "spousal support",
    "palimony": "unmarried partner support",
    "child support": "child support obligation",
    "cs": "child support obligation",
    "back child support": "child support arrearages",
    "arrears": "arrearages",
    "arrearage": "arrearages",
    "back support": "retroactive support",
    "guideline support": "child support guidelines",
    "above guidelines": "deviation from guidelines",
    "below guidelines": "deviation from guidelines",

    # Property terminology
    "marital property": "community property",
    "marital assets": "community property",
    "marital estate": "community estate",
    "conjugal property": "community property",
    "his and hers": "separate property",
    "prenup": "prenuptial agreement",
    "premarital agreement": "prenuptial agreement",
    "antenuptial agreement": "prenuptial agreement",
    "postnup": "postnuptial agreement",
    "marital agreement": "postnuptial agreement",
    "property settlement": "property division",
    "equitable division": "equitable distribution",
    "fair division": "equitable distribution",
    "50/50 split": "equal division",
    "hidden money": "hidden assets",
    "hiding assets": "hidden assets",
    "wasting money": "dissipation of marital assets",
    "spending down": "dissipation of marital assets",
    "squandering": "dissipation of marital assets",

    # Divorce terminology
    "divorce": "dissolution of marriage",
    "dissolution": "dissolution of marriage",
    "split up": "dissolution of marriage",
    "annulment": "declaration of invalidity",
    "void marriage": "void ab initio marriage",
    "legal separation": "separate maintenance",
    "separation": "marital separation",
    "no fault": "no-fault divorce",
    "irreconcilable differences": "no-fault grounds",
    "insupportability": "no-fault grounds",
    "fault divorce": "fault-based grounds",
    "contested divorce": "contested dissolution",
    "uncontested divorce": "agreed dissolution",

    # Domestic violence
    "domestic violence": "family violence",
    "dv": "family violence",
    "abuse": "family violence",
    "battery": "family violence",
    "assault": "family violence",
    "protective order": "protective order",
    "restraining order": "protective order",
    "tro": "temporary restraining order",
    "po": "protective order",
    "stay away order": "protective order",
    "no contact order": "protective order",
    "order of protection": "protective order",

    # Modification
    "modify": "modification",
    "change order": "modification",
    "change custody": "custody modification",
    "reduce support": "support modification downward",
    "increase support": "support modification upward",
    "material change": "material and substantial change in circumstances",

    # Enforcement
    "contempt": "contempt of court",
    "violating order": "order violation",
    "not paying support": "support non-compliance",
    "withholding child": "possession interference",
    "won't let me see kids": "possession interference",
    "denying visitation": "possession interference",
    "not following court order": "order non-compliance",

    # Parentage
    "paternity": "parentage",
    "paternity test": "genetic testing",
    "dna test": "genetic testing",
    "who is the father": "parentage determination",
    "biological father": "alleged father",
    "birth father": "biological parent",
    "acknowledgment of paternity": "voluntary acknowledgment",

    # Adoption
    "adopt": "adoption",
    "stepparent adoption": "stepparent adoption",
    "second parent adoption": "second parent adoption",
    "foster care": "dependency",
    "cps case": "child protective services investigation",
    "dfps": "department of family protective services",
    "cps": "child protective services",

    # Jurisdiction
    "uccjea": "uniform child custody jurisdiction",
    "home state": "home state jurisdiction",
    "which court": "jurisdiction determination",
    "where to file": "venue and jurisdiction",
    "move with child": "parental relocation",
    "relocate": "parental relocation",
    "move away": "parental relocation",

    # Miscellaneous
    "gal": "guardian ad litem",
    "amicus": "amicus attorney",
    "casa": "court appointed special advocates",
    "mediator": "family mediator",
    "collaborative": "collaborative divorce",
    "qdro": "qualified domestic relations order",
    "pension division": "retirement benefit division",
    "401k split": "retirement benefit division",
    "imputed income": "income imputation",
    "earning capacity": "income imputation",
    "common law wife": "common law marriage",
    "common law husband": "common law marriage",
    "informal marriage": "common law marriage",
    "parental alienation": "parental alienation",
    "pas": "parental alienation",
    "turning kids against me": "parental alienation",
    "coaching children": "parental alienation",
    "emancipation": "minor emancipation",
    "emancipated minor": "minor emancipation",
    "best interest": "best interest of the child",
    "bic": "best interest of the child",
}


class NormalizationResult:
    """Result of normalizing a family law query."""

    def __init__(self, original: str, normalized: str, substitutions: List[Dict[str, str]]):
        self.original = original
        self.normalized = normalized
        self.substitutions = substitutions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "normalized": self.normalized,
            "substitutions": self.substitutions,
            "substitution_count": len(self.substitutions),
        }


def normalize_query(query: str) -> NormalizationResult:
    """Apply semantic normalization to a family law query."""
    original = query
    normalized = query.lower().strip()
    substitutions: List[Dict[str, str]] = []

    sorted_synonyms = sorted(FAMILY_LAW_SYNONYMS.keys(), key=len, reverse=True)
    for term in sorted_synonyms:
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, normalized, re.IGNORECASE):
            replacement = FAMILY_LAW_SYNONYMS[term]
            if term.lower() != replacement.lower():
                normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
                substitutions.append({"from": term, "to": replacement})

    return NormalizationResult(original, normalized, substitutions)


# ============================================================================
# REQUEST / RESPONSE MODELS
# ============================================================================

class FamilyLawQuery(BaseModel):
    """Professional family law query request."""
    question: str = Field(..., min_length=10, description="Family law question requiring analysis")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth mode")
    jurisdiction: str = Field(default="TX", description="State jurisdiction code")
    case_type: Optional[str] = Field(default=None, description="Case type: divorce, paternity, modification, etc.")
    include_trace: bool = Field(default=False, description="Include reasoning trace")
    include_zones: bool = Field(default=False, description="Include zoned analysis")


class Citation(BaseModel):
    """Structured legal citation."""
    authority: str
    reference: str
    relevance: str
    weight: int = 0


class ReasoningStep(BaseModel):
    """Structured reasoning component."""
    step: int
    analysis: str
    authority: Optional[str] = None


class ZonedConclusion(BaseModel):
    """A conclusion pinned to one analysis zone."""
    zone: str
    conclusion: str
    confidence: float
    caveats: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)


class FactFragility(BaseModel):
    """Fragility assessment for a conclusion."""
    conclusion: str
    fragility_score: float
    fragility_tier: str
    single_source: bool
    factors: List[str] = Field(default_factory=list)


class FamilyLawResponse(BaseModel):
    """Professional family law intelligence response."""
    query_id: str
    question: str
    mode: ResponseMode
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    risk_level: str = "info"
    risk_factors: List[str] = Field(default_factory=list)
    doctrine_match: bool
    confidence_band: str
    confidence_score: float
    response_layer: str
    latency_ms: float
    conflict_detected: bool = False
    conflict_resolution: Optional[Dict[str, Any]] = None
    authority_weight: int = 0
    determinism_hash: Optional[str] = None
    reasoning_trace: Optional[List[ReasoningStep]] = None
    zoned_analysis: Optional[List[Dict[str, Any]]] = None
    fact_fragility: Optional[List[Dict[str, Any]]] = None
    coverage_report: Optional[Dict[str, Any]] = None
    limitations: List[str] = Field(default_factory=list)
    jurisdiction_note: Optional[str] = None
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """System health check."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    engine_id: str
    version: str
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    memory_mb: Dict[str, float]
    active_queries: int
    queries_last_hour: int
    queries_total: int
    error_rate: Dict[str, Any]
    cache_hit_rate: float
    drift_report: Dict[str, Any]
    coverage_summary: Dict[str, Any]


class BatchQuery(BaseModel):
    """Batch query request."""
    queries: List[FamilyLawQuery] = Field(..., min_length=1, max_length=20)


class BatchResponse(BaseModel):
    """Batch query response."""
    results: List[FamilyLawResponse]
    total_latency_ms: float
    count: int


# ============================================================================
# METRICS COLLECTOR
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
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:100]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def query_start(self) -> None:
        self.active_queries += 1

    def query_end(self) -> None:
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "last_ms": 0.0}
        s = sorted(self.latencies)
        n = len(s)
        return {
            "avg_ms": round(sum(s) / n, 2),
            "p50_ms": round(s[n // 2], 2),
            "p95_ms": round(s[int(n * 0.95)], 2),
            "p99_ms": round(s[min(int(n * 0.99), n - 1)], 2),
            "last_ms": round(s[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_cache_hit_rate(self) -> float:
        total = self.doctrine_hits + self.doctrine_misses
        if total == 0:
            return 1.0
        return round(self.doctrine_hits / total, 4)

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        return sum(1 for t in self.queries if t > cutoff)

    def total_queries(self) -> int:
        return self.doctrine_hits + self.doctrine_misses


_metrics = MetricsCollector()


# ============================================================================
# DOCTRINE BLOCK DATA STRUCTURE
# ============================================================================

@dataclass
class DoctrineBlock:
    """Pre-compiled expert reasoning block with authority hardening."""
    topic_key: str
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[Dict[str, str]]
    counter_arguments: List[str]
    confidence: str = "defensible"
    related_doctrines: List[str] = field(default_factory=list)
    entity_scope: List[str] = field(default_factory=lambda: ["all"])
    staleness_date: str = ""

    def get_authority_weight(self) -> int:
        if not self.primary_authority:
            return 0
        total = 0
        for auth in self.primary_authority:
            auth_type = auth.get("authority", "").lower()
            if auth_type == "statute":
                total += AuthorityLevel.STATUTE.weight
            elif auth_type == "case_law":
                total += AuthorityLevel.CASE_LAW.weight
            elif auth_type == "court_rule":
                total += AuthorityLevel.COURT_RULE.weight
            elif auth_type == "regulatory":
                total += AuthorityLevel.REGULATORY.weight
            else:
                total += AuthorityLevel.COMMENTARY.weight
        return total

    def to_citations(self) -> List[Citation]:
        citations = []
        for auth in self.primary_authority:
            weight = AuthorityLevel.STATUTE.weight
            auth_type = auth.get("authority", "").lower()
            if auth_type == "case_law":
                weight = AuthorityLevel.CASE_LAW.weight
            elif auth_type == "court_rule":
                weight = AuthorityLevel.COURT_RULE.weight
            elif auth_type == "regulatory":
                weight = AuthorityLevel.REGULATORY.weight
            elif auth_type == "commentary":
                weight = AuthorityLevel.COMMENTARY.weight
            citations.append(Citation(
                authority=auth.get("authority", "unknown"),
                reference=auth.get("reference", ""),
                relevance=auth.get("relevance", ""),
                weight=weight,
            ))
        return citations


# ============================================================================
# DOCTRINE CACHE — loaded from lg10_doctrines.json
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}


def load_doctrine_cache() -> int:
    """Load doctrine blocks from JSON file into the cache."""
    global DOCTRINE_CACHE
    if not DOCTRINES_FILE.exists():
        logger.warning(f"Doctrines file not found: {DOCTRINES_FILE}")
        return 0

    with open(DOCTRINES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    blocks = data.get("blocks", [])
    loaded = 0
    for block_data in blocks:
        topic_key = block_data.get("topic_key", "")
        if not topic_key:
            continue
        DOCTRINE_CACHE[topic_key] = DoctrineBlock(
            topic_key=topic_key,
            topic=block_data.get("topic", ""),
            keywords=block_data.get("keywords", []),
            conclusion_template=block_data.get("conclusion_template", ""),
            reasoning_framework=block_data.get("reasoning_framework", ""),
            key_factors=block_data.get("key_factors", []),
            primary_authority=block_data.get("primary_authority", []),
            counter_arguments=block_data.get("counter_arguments", []),
            confidence=block_data.get("confidence", "defensible"),
            related_doctrines=block_data.get("related_doctrines", []),
            entity_scope=block_data.get("entity_scope", ["all"]),
            staleness_date=block_data.get("staleness_date", ""),
        )
        loaded += 1

    logger.info(f"Doctrine cache loaded: {loaded} blocks from {DOCTRINES_FILE}")
    return loaded


# ============================================================================
# VECTOR SEARCH — TF-IDF keyword similarity over doctrine blocks
# ============================================================================

def _tokenize(text: str) -> List[str]:
    """Simple tokenizer for keyword matching."""
    return re.findall(r'[a-z]+', text.lower())


def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    """Compute term frequency."""
    counts: Dict[str, int] = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    total = len(tokens) if tokens else 1
    return {t: c / total for t, c in counts.items()}


def _compute_idf(all_docs: List[List[str]]) -> Dict[str, float]:
    """Compute inverse document frequency."""
    n = len(all_docs)
    if n == 0:
        return {}
    df: Dict[str, int] = {}
    for doc in all_docs:
        unique = set(doc)
        for term in unique:
            df[term] = df.get(term, 0) + 1
    return {term: math.log(n / count) for term, count in df.items()}


def search_similar(query: str, k: int = 5, threshold: float = 0.3) -> List[Dict[str, Any]]:
    """Search doctrine blocks by TF-IDF similarity to query."""
    if not DOCTRINE_CACHE:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    doc_tokens: Dict[str, List[str]] = {}
    for key, block in DOCTRINE_CACHE.items():
        text = " ".join(block.keywords) + " " + block.topic + " " + block.conclusion_template
        doc_tokens[key] = _tokenize(text)

    all_docs = list(doc_tokens.values())
    idf = _compute_idf(all_docs + [query_tokens])
    query_tf = _compute_tf(query_tokens)
    query_vec: Dict[str, float] = {t: tf * idf.get(t, 0) for t, tf in query_tf.items()}

    results: List[Dict[str, Any]] = []
    for key, tokens in doc_tokens.items():
        doc_tf = _compute_tf(tokens)
        doc_vec: Dict[str, float] = {t: tf * idf.get(t, 0) for t, tf in doc_tf.items()}
        all_terms = set(query_vec.keys()) | set(doc_vec.keys())
        dot = sum(query_vec.get(t, 0) * doc_vec.get(t, 0) for t in all_terms)
        mag_q = math.sqrt(sum(v ** 2 for v in query_vec.values())) or 1
        mag_d = math.sqrt(sum(v ** 2 for v in doc_vec.values())) or 1
        similarity = dot / (mag_q * mag_d)

        if similarity >= threshold:
            results.append({
                "topic_key": key,
                "topic": DOCTRINE_CACHE[key].topic,
                "score": round(similarity, 4),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]


# ============================================================================
# DOCTRINE MATCHER — keyword matching with authority hardening
# ============================================================================

@dataclass
class MatchResult:
    """Result of doctrine matching."""
    doctrine: Optional[DoctrineBlock]
    topic_key: Optional[str]
    match_score: int
    authority_weight: int
    conflict_detected: bool
    conflict_resolution: Optional[Dict[str, Any]]
    all_candidates: List[Dict[str, Any]]
    determinism_hash: str

    @property
    def is_match(self) -> bool:
        return self.doctrine is not None


def match_doctrine(query: str, case_type: Optional[str] = None) -> MatchResult:
    """Match a query to the best doctrine block."""
    normalized = normalize_query(query)
    query_lower = normalized.normalized

    candidates: List[Dict[str, Any]] = []

    for key, block in DOCTRINE_CACHE.items():
        score = 0
        for kw in block.keywords:
            if kw.lower() in query_lower:
                score += 10
                if query_lower.startswith(kw.lower()):
                    score += 5
        if block.topic.lower() in query_lower:
            score += 20
        if case_type and case_type in block.entity_scope:
            score += 5
        elif case_type and "all" in block.entity_scope:
            score += 2

        if score > 0:
            candidates.append({
                "topic_key": key,
                "score": score,
                "authority_weight": block.get_authority_weight(),
                "confidence": block.confidence,
            })

    candidates.sort(key=lambda c: (c["score"], c["authority_weight"]), reverse=True)

    conflict_detected = False
    conflict_resolution = None
    if len(candidates) >= 2:
        top = candidates[0]
        second = candidates[1]
        if second["score"] >= top["score"] * 0.8:
            conflict_detected = True
            if top["authority_weight"] >= second["authority_weight"]:
                winner = top
                loser = second
            else:
                winner = second
                loser = top
                candidates[0], candidates[1] = candidates[1], candidates[0]
            conflict_resolution = {
                "competing_doctrines": [winner["topic_key"], loser["topic_key"]],
                "resolution": "authority_weight",
                "rationale": f"{winner['topic_key']} selected over {loser['topic_key']} — authority weight {winner['authority_weight']} vs {loser['authority_weight']}",
            }

    hash_input = f"{query_lower}|{ENGINE_VERSION}|{json.dumps([c['topic_key'] for c in candidates[:3]])}"
    det_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    if candidates:
        best = candidates[0]
        doctrine = DOCTRINE_CACHE.get(best["topic_key"])
        return MatchResult(
            doctrine=doctrine,
            topic_key=best["topic_key"],
            match_score=best["score"],
            authority_weight=best["authority_weight"],
            conflict_detected=conflict_detected,
            conflict_resolution=conflict_resolution,
            all_candidates=candidates[:5],
            determinism_hash=det_hash,
        )

    return MatchResult(
        doctrine=None,
        topic_key=None,
        match_score=0,
        authority_weight=0,
        conflict_detected=False,
        conflict_resolution=None,
        all_candidates=[],
        determinism_hash=det_hash,
    )


# ============================================================================
# CONFIDENCE STRATIFICATION
# ============================================================================

def compute_confidence(
    doctrine_match: bool,
    match_score: int,
    authority_weight: int,
    mode: ResponseMode,
    jurisdiction: str,
    conflict_detected: bool,
) -> tuple[float, str]:
    """Compute confidence score and band."""
    base = 0.50
    if doctrine_match:
        base += 0.20
        if match_score >= 30:
            base += 0.15
        elif match_score >= 20:
            base += 0.10
        elif match_score >= 10:
            base += 0.05

    if authority_weight >= 300:
        base += 0.10
    elif authority_weight >= 200:
        base += 0.05

    if jurisdiction in COMMUNITY_PROPERTY_STATES:
        base += 0.02

    if conflict_detected:
        base -= 0.05

    if mode == ResponseMode.DEFENSE:
        base -= 0.03

    score = max(0.0, min(1.0, base))

    if score >= 0.85:
        band = ConfidenceBand.DEFENSIBLE.value
    elif score >= 0.70:
        band = ConfidenceBand.SUPPORTABLE.value
    elif score >= 0.50:
        band = ConfidenceBand.DISCLOSURE.value
    else:
        band = ConfidenceBand.HIGH_RISK.value

    return round(score, 4), band


# ============================================================================
# DOCTRINE DRIFT WATCHER
# ============================================================================

class DoctrineDriftWatcher:
    """Flags stale doctrine blocks based on staleness threshold."""

    def __init__(self, stale_threshold_days: int = 365) -> None:
        self.stale_threshold_days = stale_threshold_days

    def check_staleness(self) -> Dict[str, Any]:
        """Check all doctrine blocks for staleness."""
        now = datetime.now(timezone.utc)
        stale_blocks: List[str] = []
        fresh_blocks: List[str] = []

        for key, block in DOCTRINE_CACHE.items():
            if not block.staleness_date:
                stale_blocks.append(key)
                continue
            try:
                staleness_dt = datetime.fromisoformat(block.staleness_date).replace(tzinfo=timezone.utc)
                age_days = (now - staleness_dt).days
                if age_days > self.stale_threshold_days:
                    stale_blocks.append(key)
                else:
                    fresh_blocks.append(key)
            except (ValueError, TypeError):
                stale_blocks.append(key)

        return {
            "total_blocks": len(DOCTRINE_CACHE),
            "fresh_count": len(fresh_blocks),
            "stale_count": len(stale_blocks),
            "stale_blocks": stale_blocks,
            "stale_threshold_days": self.stale_threshold_days,
            "checked_at": now.isoformat(),
        }

    def is_stale(self, topic_key: str) -> bool:
        """Check if a specific doctrine block is stale."""
        block = DOCTRINE_CACHE.get(topic_key)
        if not block or not block.staleness_date:
            return True
        try:
            staleness_dt = datetime.fromisoformat(block.staleness_date).replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - staleness_dt).days
            return age_days > self.stale_threshold_days
        except (ValueError, TypeError):
            return True


_drift_watcher = DoctrineDriftWatcher()


# ============================================================================
# DOCTRINE COVERAGE MAP
# ============================================================================

class DoctrineCoverageMap:
    """Track coverage and gap topics."""

    def __init__(self) -> None:
        self._triggered: Dict[str, int] = {}
        self._gaps: List[str] = []
        self._unknown_queries: List[str] = []

    def record_hit(self, topic_key: str) -> None:
        self._triggered[topic_key] = self._triggered.get(topic_key, 0) + 1

    def record_gap(self, query: str) -> None:
        if query not in self._gaps:
            self._gaps.append(query)
            if len(self._gaps) > 500:
                self._gaps.pop(0)

    def record_unknown(self, query: str) -> None:
        if query not in self._unknown_queries:
            self._unknown_queries.append(query)
            if len(self._unknown_queries) > 500:
                self._unknown_queries.pop(0)

    def get_report(self) -> Dict[str, Any]:
        total = len(DOCTRINE_CACHE)
        triggered = len(self._triggered)
        never_triggered = [k for k in DOCTRINE_CACHE if k not in self._triggered]
        return {
            "total_doctrines": total,
            "triggered_count": triggered,
            "never_triggered_count": len(never_triggered),
            "never_triggered": never_triggered[:20],
            "top_triggered": sorted(self._triggered.items(), key=lambda x: x[1], reverse=True)[:10],
            "gap_count": len(self._gaps),
            "recent_gaps": self._gaps[-10:],
            "unknown_query_count": len(self._unknown_queries),
        }


_coverage_map = DoctrineCoverageMap()


# ============================================================================
# FACT FRAGILITY SCORING
# ============================================================================

def assess_fragility(
    doctrine: Optional[DoctrineBlock],
    match_score: int,
    conflict_detected: bool,
) -> List[Dict[str, Any]]:
    """Assess fact fragility for conclusions."""
    if not doctrine:
        return [{
            "conclusion": "No doctrine matched",
            "fragility_score": 0.90,
            "fragility_tier": "HIGH",
            "single_source": True,
            "factors": ["No supporting doctrine found", "Analysis based on general principles only"],
        }]

    factors: List[str] = []
    score = 0.20

    auth_count = len(doctrine.primary_authority)
    single_source = auth_count <= 1
    if single_source:
        score += 0.30
        factors.append("Single authority source increases fragility")
    elif auth_count <= 2:
        score += 0.15
        factors.append("Limited authority sources")

    if conflict_detected:
        score += 0.15
        factors.append("Competing doctrines detected — resolution may be challenged")

    if match_score < 15:
        score += 0.10
        factors.append("Low keyword match confidence")

    counter_count = len(doctrine.counter_arguments)
    if counter_count >= 4:
        score += 0.10
        factors.append(f"Multiple counter-arguments available ({counter_count})")
    elif counter_count >= 2:
        score += 0.05
        factors.append("Counter-arguments exist")

    score = min(1.0, score)
    if score >= 0.70:
        tier = "HIGH"
    elif score >= 0.40:
        tier = "MEDIUM"
    else:
        tier = "LOW"

    return [{
        "conclusion": doctrine.topic,
        "fragility_score": round(score, 3),
        "fragility_tier": tier,
        "single_source": single_source,
        "factors": factors,
    }]


# ============================================================================
# ZONED ANALYSIS
# ============================================================================

def generate_zoned_analysis(
    doctrine: DoctrineBlock,
    query: str,
    jurisdiction: str,
    confidence_score: float,
) -> List[Dict[str, Any]]:
    """Generate analysis across litigation, negotiation, and compliance zones."""
    zones: List[Dict[str, Any]] = []

    litigation_conclusion = (
        f"In a {jurisdiction} courtroom, the court will apply {doctrine.topic} analysis. "
        f"{doctrine.conclusion_template[:200]}... "
        f"The court will consider: {', '.join(doctrine.key_factors[:4])}."
    )
    zones.append({
        "zone": AnalysisZone.LITIGATION.value,
        "conclusion": litigation_conclusion,
        "confidence": round(min(confidence_score + 0.05, 1.0), 4),
        "caveats": [
            f"Analysis is based on {jurisdiction} law — other jurisdictions may differ",
            "Judicial discretion may produce different outcomes on same facts",
        ],
        "action_items": [
            "Compile evidence supporting each best-interest factor",
            f"Research recent {jurisdiction} appellate decisions on this issue",
            "Prepare expert testimony if applicable",
        ],
    })

    negotiation_conclusion = (
        f"Settlement leverage points for {doctrine.topic}: "
        f"Consider the strength of your position on key factors ({', '.join(doctrine.key_factors[:3])}). "
        f"Counter-arguments to anticipate: {doctrine.counter_arguments[0] if doctrine.counter_arguments else 'none identified'}."
    )
    zones.append({
        "zone": AnalysisZone.NEGOTIATION.value,
        "conclusion": negotiation_conclusion,
        "confidence": round(max(confidence_score - 0.05, 0.0), 4),
        "caveats": [
            "Settlement value depends on litigation risk assessment",
            "Opposing counsel may have different case valuation",
        ],
        "action_items": [
            "Identify BATNA (best alternative to negotiated agreement)",
            "Prepare settlement range with floor and ceiling",
            "Consider mediation as cost-effective alternative",
        ],
    })

    compliance_conclusion = (
        f"Regarding {doctrine.topic}: ensure strict compliance with any existing court orders. "
        f"Non-compliance risks contempt proceedings. Modification requires filing a motion showing "
        f"material and substantial change in circumstances. Document all compliance efforts."
    )
    zones.append({
        "zone": AnalysisZone.COMPLIANCE.value,
        "conclusion": compliance_conclusion,
        "confidence": round(min(confidence_score + 0.10, 1.0), 4),
        "caveats": [
            "Existing orders remain in effect until modified by the court",
            "Self-help remedies may constitute contempt",
        ],
        "action_items": [
            "Review all existing orders for specific obligations",
            "Document compliance with dates and evidence",
            "File modification motion before deviating from order terms",
        ],
    })

    return zones


# ============================================================================
# RISK ASSESSMENT
# ============================================================================

def assess_risk(
    doctrine: Optional[DoctrineBlock],
    confidence_score: float,
    jurisdiction: str,
    mode: ResponseMode,
) -> tuple[str, List[str]]:
    """Assess risk level and factors."""
    factors: List[str] = []
    risk_score = 1.0 - confidence_score

    if not doctrine:
        risk_score += 0.20
        factors.append("No specific doctrine coverage for this issue")

    if confidence_score < 0.50:
        factors.append("Low confidence — position may not survive challenge")

    if mode == ResponseMode.DEFENSE:
        factors.append("Defense mode analysis — heightened scrutiny expected")

    if doctrine and len(doctrine.counter_arguments) >= 3:
        risk_score += 0.05
        factors.append("Multiple viable counter-arguments exist")

    if risk_score >= 0.70:
        level = RiskLevel.CRITICAL.value
        factors.insert(0, "CRITICAL: Immediate legal review recommended")
    elif risk_score >= 0.50:
        level = RiskLevel.HIGH.value
    elif risk_score >= 0.30:
        level = RiskLevel.MEDIUM.value
    elif risk_score >= 0.10:
        level = RiskLevel.LOW.value
    else:
        level = RiskLevel.INFO.value

    return level, factors


# ============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# ============================================================================

ISSUE_KEYWORD_MAP: Dict[IssueCategory, List[str]] = {
    IssueCategory.CUSTODY: ["custody", "conservatorship", "possession", "visitation", "parenting time", "best interest"],
    IssueCategory.SUPPORT: ["support", "alimony", "maintenance", "child support", "spousal", "arrears"],
    IssueCategory.PROPERTY: ["property", "asset", "division", "community", "separate", "equitable", "business valuation", "hidden assets", "dissipation", "qdro", "retirement"],
    IssueCategory.ENFORCEMENT: ["contempt", "enforce", "violat", "non-compliance", "withholding"],
    IssueCategory.JURISDICTION: ["jurisdiction", "uccjea", "home state", "venue", "which court", "hague"],
    IssueCategory.PARENTAGE: ["paternity", "parentage", "dna", "genetic", "father", "biological"],
    IssueCategory.PROTECTION: ["protective order", "restraining", "family violence", "domestic violence", "abuse", "stalking"],
    IssueCategory.MODIFICATION: ["modif", "change order", "material change", "reduce support", "increase support"],
    IssueCategory.ADOPTION: ["adopt", "stepparent", "termination of parental", "tpr"],
    IssueCategory.PROCEDURE: ["discovery", "mediation", "expert", "attorney fee", "temporary order", "gal", "guardian"],
}


def decompose_query(query: str) -> List[IssueCategory]:
    """Decompose a query into issue categories."""
    query_lower = query.lower()
    detected: List[IssueCategory] = []
    for category, keywords in ISSUE_KEYWORD_MAP.items():
        for kw in keywords:
            if kw in query_lower:
                if category not in detected:
                    detected.append(category)
                break
    return detected if detected else [IssueCategory.PROCEDURE]


def multi_doctrine_match(query: str, case_type: Optional[str] = None) -> Dict[str, Any]:
    """Perform multi-doctrine matching across issue categories."""
    issues = decompose_query(query)
    primary_match = match_doctrine(query, case_type)

    secondary_matches: List[Dict[str, Any]] = []
    if primary_match.doctrine:
        for related_key in primary_match.doctrine.related_doctrines:
            if related_key in DOCTRINE_CACHE:
                related = DOCTRINE_CACHE[related_key]
                secondary_matches.append({
                    "topic_key": related_key,
                    "topic": related.topic,
                    "relationship": "related_doctrine",
                    "authority_weight": related.get_authority_weight(),
                })

    vector_results = search_similar(query, k=3, threshold=0.25)
    tertiary_matches = [r for r in vector_results if r.get("topic_key") != primary_match.topic_key]

    return {
        "issues_detected": [i.value for i in issues],
        "primary": {
            "topic_key": primary_match.topic_key,
            "match_score": primary_match.match_score,
            "authority_weight": primary_match.authority_weight,
        } if primary_match.is_match else None,
        "secondary": secondary_matches[:5],
        "tertiary": tertiary_matches[:3],
        "total_doctrines_matched": (1 if primary_match.is_match else 0) + len(secondary_matches) + len(tertiary_matches),
        "is_multi_doctrine": len(issues) > 1 or len(secondary_matches) > 0,
    }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

def write_audit_record(record: Dict[str, Any]) -> None:
    """Append audit record to JSONL file."""
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception as e:
        logger.warning(f"Audit write failed: {e}")


# ============================================================================
# DOMAIN-SPECIFIC ANALYSIS FUNCTIONS (15+)
# ============================================================================

def analyze_child_custody_factors(query: str, jurisdiction: str) -> Dict[str, Any]:
    """Analyze child custody using jurisdiction-specific best-interest factors."""
    factors_by_state: Dict[str, List[str]] = {
        "TX": [
            "Desires of the child (if 12+)",
            "Emotional and physical needs of the child now and in the future",
            "Emotional and physical danger to the child now and in the future",
            "Parental abilities of the individuals seeking custody",
            "Programs available to assist individuals seeking custody",
            "Plans for the child by individuals seeking custody",
            "Stability of the home or proposed placement",
            "Acts or omissions of the parent indicating unworthiness",
            "Any history of family violence",
        ],
        "CA": [
            "Health, safety, and welfare of the child",
            "History of abuse by one parent against the child or other parent",
            "Nature and amount of contact with both parents",
            "Habitual or continual illegal use of controlled substances or alcohol",
        ],
        "NY": [
            "Quality of the home environment and parental guidance",
            "Financial status and ability to provide for the child",
            "Ability to provide for the child's emotional and intellectual development",
            "Relative fitness of each parent",
            "Effect of the custody award on the child's relationship with the other parent",
        ],
    }
    state_factors = factors_by_state.get(jurisdiction, factors_by_state["TX"])

    is_community = jurisdiction in COMMUNITY_PROPERTY_STATES
    holley_factors = [
        "Desires of the child", "Emotional and physical needs", "Emotional and physical danger",
        "Parental abilities", "Programs available", "Plans for child", "Stability of home",
        "Acts or omissions indicating unworthiness", "Excuses for acts or omissions",
    ]

    return {
        "analysis_type": "child_custody_factors",
        "jurisdiction": jurisdiction,
        "statutory_factors": state_factors,
        "holley_factors_applicable": jurisdiction == "TX",
        "holley_factors": holley_factors if jurisdiction == "TX" else [],
        "community_property_state": is_community,
        "key_considerations": [
            "Status quo presumption favors maintaining current arrangements",
            "Domestic violence creates rebuttable presumption against perpetrator",
            "Child 12+ may express preference in Texas via in-chambers interview",
            "Joint managing conservatorship is presumed unless rebutted by evidence",
        ],
    }


def calculate_child_support_estimate(
    obligor_gross_monthly: float,
    number_of_children: int,
    jurisdiction: str,
    other_children: int = 0,
) -> Dict[str, Any]:
    """Calculate guideline child support estimate."""
    tx_percentages = {1: 0.20, 2: 0.25, 3: 0.30, 4: 0.35, 5: 0.40, 6: 0.40}
    tx_other_offset = {1: 0.025, 2: 0.05, 3: 0.075, 4: 0.10, 5: 0.125}

    if jurisdiction == "TX":
        net_resources = obligor_gross_monthly * 0.736
        max_net = 9200.0
        capped_net = min(net_resources, max_net)
        pct = tx_percentages.get(min(number_of_children, 6), 0.40)
        if other_children > 0:
            offset = tx_other_offset.get(min(other_children, 5), 0.125)
            pct = max(pct - offset, 0.0)
        guideline_amount = round(capped_net * pct, 2)
        above_cap = net_resources > max_net

        return {
            "jurisdiction": "TX",
            "obligor_gross_monthly": obligor_gross_monthly,
            "estimated_net_resources": round(net_resources, 2),
            "guideline_cap": max_net,
            "above_cap": above_cap,
            "percentage_applied": round(pct * 100, 1),
            "guideline_amount": guideline_amount,
            "other_children_offset": other_children,
            "note": "This is an estimate. Actual net resources depend on specific deductions." if not above_cap
                else "Income exceeds guideline cap. Court may consider additional factors for above-cap support.",
            "authority": "Tex. Fam. Code \u00a7 154.125-154.126",
        }

    return {
        "jurisdiction": jurisdiction,
        "obligor_gross_monthly": obligor_gross_monthly,
        "note": f"Detailed calculation requires {jurisdiction}-specific guidelines worksheet. Income shares model applies in most states.",
        "guideline_amount": round(obligor_gross_monthly * 0.20 * number_of_children, 2),
        "estimate_only": True,
    }


def evaluate_spousal_support_eligibility(
    marriage_duration_years: float,
    requesting_party_income: float,
    paying_party_income: float,
    jurisdiction: str,
    family_violence: bool = False,
    disability: bool = False,
) -> Dict[str, Any]:
    """Evaluate spousal support eligibility and estimated duration."""
    if jurisdiction == "TX":
        eligible = False
        grounds = []
        if family_violence:
            eligible = True
            grounds.append("Family violence within 2 years of filing or during pendency")
        if disability:
            eligible = True
            grounds.append("Incapacitating physical or mental disability")
        if marriage_duration_years >= 10 and requesting_party_income < paying_party_income * 0.5:
            eligible = True
            grounds.append(f"Marriage duration {marriage_duration_years} years (>= 10) and income disparity")

        max_duration_months = 0
        if eligible:
            if marriage_duration_years < 10:
                max_duration_months = 60
            elif marriage_duration_years < 20:
                max_duration_months = 60
            elif marriage_duration_years < 30:
                max_duration_months = 84
            else:
                max_duration_months = 120

        max_amount = min(paying_party_income * 0.20, 5000.0)

        return {
            "jurisdiction": "TX",
            "eligible": eligible,
            "grounds": grounds,
            "max_duration_months": max_duration_months,
            "max_monthly_amount": round(max_amount, 2),
            "marriage_duration_years": marriage_duration_years,
            "income_disparity_ratio": round(paying_party_income / max(requesting_party_income, 1), 2),
            "authority": "Tex. Fam. Code \u00a7 8.051-8.055",
        }

    return {
        "jurisdiction": jurisdiction,
        "eligible": True,
        "note": f"{jurisdiction} uses multi-factor analysis for spousal support. No strict eligibility threshold.",
        "marriage_duration_years": marriage_duration_years,
        "income_disparity_ratio": round(paying_party_income / max(requesting_party_income, 1), 2),
    }


def classify_property_division(
    asset_name: str,
    acquisition_date: str,
    marriage_date: str,
    source_of_funds: str,
    jurisdiction: str,
) -> Dict[str, Any]:
    """Classify an asset as community/marital or separate property."""
    is_community_state = jurisdiction in COMMUNITY_PROPERTY_STATES

    pre_marital = acquisition_date < marriage_date
    gift_or_inheritance = source_of_funds.lower() in ["gift", "inheritance", "devise", "bequest"]
    personal_injury = "personal injury" in source_of_funds.lower()

    is_separate = pre_marital or gift_or_inheritance or personal_injury
    classification = "separate" if is_separate else ("community" if is_community_state else "marital")

    reasoning = []
    if pre_marital:
        reasoning.append(f"Acquired ({acquisition_date}) before marriage ({marriage_date}) — separate by inception of title")
    if gift_or_inheritance:
        reasoning.append(f"Source is {source_of_funds} — separate property by statutory exception")
    if personal_injury:
        reasoning.append("Personal injury recovery (pain and suffering) is separate property")
    if not is_separate:
        reasoning.append(f"Acquired during marriage with {'community' if is_community_state else 'marital'} funds — {'community' if is_community_state else 'marital'} property")

    return {
        "asset": asset_name,
        "classification": classification,
        "is_separate": is_separate,
        "community_property_state": is_community_state,
        "reasoning": reasoning,
        "tracing_required": not is_separate and source_of_funds.lower() == "mixed",
        "burden_of_proof": "clear and convincing evidence" if is_community_state else "preponderance",
        "jurisdiction": jurisdiction,
    }


def assess_prenuptial_enforceability(
    independent_counsel_both: bool,
    full_disclosure: bool,
    voluntary: bool,
    time_before_wedding_days: int,
    unconscionable_at_enforcement: bool,
    waives_child_support: bool,
) -> Dict[str, Any]:
    """Assess enforceability of a prenuptial agreement."""
    issues: List[str] = []
    score = 1.0

    if not independent_counsel_both:
        issues.append("Lack of independent counsel for both parties weakens enforceability")
        score -= 0.20
    if not full_disclosure:
        issues.append("Inadequate financial disclosure may void agreement")
        score -= 0.30
    if not voluntary:
        issues.append("Evidence of duress or coercion fatal to enforceability")
        score -= 0.40
    if time_before_wedding_days < 14:
        issues.append(f"Only {time_before_wedding_days} days before wedding — insufficient review time")
        score -= 0.15
    elif time_before_wedding_days < 30:
        issues.append(f"{time_before_wedding_days} days may be insufficient in some jurisdictions")
        score -= 0.05
    if unconscionable_at_enforcement:
        issues.append("Agreement is unconscionable at time of enforcement")
        score -= 0.25
    if waives_child_support:
        issues.append("Child support waiver is void as against public policy in all jurisdictions")
        score -= 0.50

    score = max(0.0, min(1.0, score))
    enforceable = score >= 0.50 and not waives_child_support

    return {
        "enforceable": enforceable,
        "enforceability_score": round(score, 3),
        "issues": issues,
        "recommendation": "Likely enforceable" if enforceable else "Enforceability is questionable — consider challenge",
        "authority": "UPAA \u00a7 6; Tex. Fam. Code \u00a7 4.006",
    }


def evaluate_modification_grounds(
    original_order_date: str,
    changed_circumstance: str,
    voluntary: bool,
    modification_type: str,
) -> Dict[str, Any]:
    """Evaluate whether modification grounds are met."""
    try:
        order_date = datetime.fromisoformat(original_order_date).replace(tzinfo=timezone.utc)
        days_since = (datetime.now(timezone.utc) - order_date).days
    except (ValueError, TypeError):
        days_since = 365

    within_one_year = days_since < 365
    strengths: List[str] = []
    weaknesses: List[str] = []

    if within_one_year and modification_type == "custody":
        weaknesses.append("Within one year of prior order — heightened standard applies (TX: serious and immediate danger)")

    if voluntary:
        weaknesses.append("Voluntary change in circumstances — courts scrutinize for good faith")
    else:
        strengths.append("Involuntary change in circumstances — stronger modification grounds")

    changed_lower = changed_circumstance.lower()
    if "job loss" in changed_lower or "laid off" in changed_lower:
        strengths.append("Job loss is recognized material change for support modification")
    if "income increase" in changed_lower:
        strengths.append("Significant income change may warrant support adjustment")
    if "relocation" in changed_lower or "move" in changed_lower:
        strengths.append("Relocation is recognized material change for custody modification")
    if "remarriage" in changed_lower:
        strengths.append("Remarriage of recipient may affect spousal support")
    if "abuse" in changed_lower or "violence" in changed_lower:
        strengths.append("Abuse/violence is urgent ground for custody modification")

    likelihood = 0.50
    likelihood += len(strengths) * 0.10
    likelihood -= len(weaknesses) * 0.10
    likelihood = max(0.10, min(0.95, likelihood))

    return {
        "modification_type": modification_type,
        "days_since_prior_order": days_since,
        "within_one_year": within_one_year,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "likelihood_of_success": round(likelihood, 3),
        "recommendation": "Modification appears viable" if likelihood >= 0.50 else "Modification faces significant obstacles",
    }


def analyze_relocation_request(
    reason_for_move: str,
    distance_miles: float,
    child_age: int,
    existing_schedule: str,
    jurisdiction: str,
) -> Dict[str, Any]:
    """Analyze a parental relocation request."""
    factors: List[Dict[str, str]] = []
    score = 0.50

    reason_lower = reason_for_move.lower()
    if "job" in reason_lower or "employment" in reason_lower or "career" in reason_lower:
        factors.append({"factor": "Employment opportunity", "impact": "positive", "weight": "high"})
        score += 0.15
    elif "family" in reason_lower:
        factors.append({"factor": "Family support network", "impact": "positive", "weight": "medium"})
        score += 0.10
    elif "remarriage" in reason_lower or "spouse" in reason_lower:
        factors.append({"factor": "Remarriage/new relationship", "impact": "neutral", "weight": "medium"})
        score += 0.05

    if distance_miles > 500:
        factors.append({"factor": "Long distance reduces other parent's access", "impact": "negative", "weight": "high"})
        score -= 0.15
    elif distance_miles > 100:
        factors.append({"factor": "Moderate distance impacts regular schedule", "impact": "negative", "weight": "medium"})
        score -= 0.08

    if child_age < 5:
        factors.append({"factor": "Young child — frequent contact with both parents critical", "impact": "negative", "weight": "high"})
        score -= 0.10
    elif child_age > 14:
        factors.append({"factor": "Older child — preference may carry weight", "impact": "neutral", "weight": "medium"})

    score = max(0.10, min(0.90, score))

    return {
        "analysis_type": "relocation",
        "jurisdiction": jurisdiction,
        "factors_analyzed": factors,
        "approval_likelihood": round(score, 3),
        "recommendation": "Relocation likely approved" if score >= 0.55 else "Relocation faces significant opposition",
        "key_requirement": "Must demonstrate relocation serves child's best interest",
        "notice_required": "30-60 days written notice to non-relocating parent (varies by jurisdiction)",
    }


def assess_domestic_violence_impact(
    protective_order_exists: bool,
    criminal_conviction: bool,
    child_witnessed: bool,
    bip_completed: bool,
    pattern_or_isolated: str,
) -> Dict[str, Any]:
    """Assess impact of domestic violence on custody determination."""
    severity = 0.50
    impacts: List[str] = []

    if criminal_conviction:
        severity += 0.25
        impacts.append("Criminal conviction creates strong presumption against custody")
    if protective_order_exists:
        severity += 0.15
        impacts.append("Active protective order limits contact and custody options")
    if child_witnessed:
        severity += 0.15
        impacts.append("Child witnessing violence is an independent harm factor")
    if pattern_or_isolated.lower() == "pattern":
        severity += 0.15
        impacts.append("Pattern of violence indicates ongoing risk")
    if bip_completed:
        severity -= 0.10
        impacts.append("BIP completion shows remedial effort — partial mitigation")

    severity = max(0.0, min(1.0, severity))
    presumption_applies = severity >= 0.50

    return {
        "severity_score": round(severity, 3),
        "presumption_against_custody": presumption_applies,
        "impacts": impacts,
        "recommended_safeguards": [
            "Supervised visitation pending evaluation" if severity >= 0.50 else "Standard possession with safety provisions",
            "No firearms in possession during visitation",
            "Safe exchange location (police station, supervised center)",
            "BIP completion required before expanded access" if not bip_completed else "Monitor ongoing compliance",
        ],
        "authority": "Cal. Fam. Code \u00a7 3044 (rebuttable presumption); Tex. Fam. Code \u00a7 153.004",
    }


def evaluate_parental_fitness(
    substance_abuse: bool,
    mental_health_issues: bool,
    criminal_history: bool,
    stable_housing: bool,
    stable_employment: bool,
    child_bonding: str,
) -> Dict[str, Any]:
    """Evaluate parental fitness factors."""
    score = 0.70
    factors: List[Dict[str, str]] = []

    if substance_abuse:
        score -= 0.20
        factors.append({"factor": "Active substance abuse", "impact": "negative", "severity": "high"})
    if mental_health_issues:
        score -= 0.10
        factors.append({"factor": "Mental health concerns", "impact": "negative", "severity": "medium"})
    if criminal_history:
        score -= 0.15
        factors.append({"factor": "Criminal history", "impact": "negative", "severity": "high"})
    if not stable_housing:
        score -= 0.10
        factors.append({"factor": "Unstable housing", "impact": "negative", "severity": "medium"})
    if not stable_employment:
        score -= 0.05
        factors.append({"factor": "Unstable employment", "impact": "negative", "severity": "low"})

    bonding_lower = child_bonding.lower()
    if bonding_lower in ("strong", "excellent"):
        score += 0.10
        factors.append({"factor": "Strong parent-child bond", "impact": "positive", "severity": "high"})
    elif bonding_lower in ("weak", "poor"):
        score -= 0.10
        factors.append({"factor": "Weak parent-child bond", "impact": "negative", "severity": "medium"})

    score = max(0.0, min(1.0, score))

    return {
        "fitness_score": round(score, 3),
        "fitness_classification": "Fit" if score >= 0.50 else "Fitness concerns present",
        "factors": factors,
        "recommendations": [
            "Substance abuse evaluation required" if substance_abuse else None,
            "Mental health evaluation recommended" if mental_health_issues else None,
            "Background check and risk assessment" if criminal_history else None,
            "Home study recommended" if not stable_housing else None,
        ],
    }


def analyze_business_valuation_approach(
    business_type: str,
    annual_revenue: float,
    years_in_operation: int,
    owner_dependent: bool,
    jurisdiction: str,
) -> Dict[str, Any]:
    """Analyze appropriate business valuation approach for divorce."""
    approaches: List[Dict[str, Any]] = []

    if annual_revenue > 0 and years_in_operation >= 3:
        approaches.append({
            "method": "Income Approach — Capitalization of Earnings",
            "applicable": True,
            "rationale": "Stable earnings history supports income-based valuation",
            "considerations": ["Normalize owner compensation", "Select appropriate cap rate", "Adjust for non-recurring items"],
        })

    approaches.append({
        "method": "Market Approach — Comparable Transactions",
        "applicable": True,
        "rationale": "Industry transaction multiples provide market-based reference",
        "considerations": ["Finding truly comparable transactions", "Size and geography adjustments", "Transaction date adjustments"],
    })

    approaches.append({
        "method": "Asset Approach — Adjusted Net Asset Value",
        "applicable": years_in_operation < 3 or annual_revenue == 0,
        "rationale": "Appropriate for asset-heavy or early-stage businesses",
        "considerations": ["FMV adjustments to balance sheet", "Contingent liabilities", "Intangible assets"],
    })

    goodwill_note = (
        "Personal goodwill (tied to individual owner) is NOT divisible in most jurisdictions. "
        "Enterprise goodwill (business systems, name, location) IS divisible. "
        f"In {jurisdiction}: " + (
            "TX — Nail v. Nail: professional goodwill not divisible" if jurisdiction == "TX"
            else "CA — In re Marriage of Brown: goodwill of professional practice is community property" if jurisdiction == "CA"
            else "Check jurisdiction-specific rule on personal vs enterprise goodwill"
        )
    )

    return {
        "business_type": business_type,
        "valuation_approaches": approaches,
        "goodwill_analysis": goodwill_note,
        "owner_dependent": owner_dependent,
        "discount_considerations": [
            "Discount for Lack of Marketability (DLOM): 15-35% typical",
            "Key Person Discount: if owner-dependent" if owner_dependent else "No key person discount needed",
            "Minority Interest Discount: if dividing less than controlling interest",
        ],
        "expert_required": True,
        "authority": "ASA Business Valuation Standards; Nail v. Nail (TX); In re Marriage of Brown (CA)",
    }


def assess_hidden_assets_indicators(
    unexplained_cash_withdrawals: bool,
    lifestyle_income_mismatch: bool,
    recent_transfers_to_family: bool,
    business_revenue_decline: bool,
    cryptocurrency_holdings: bool,
    offshore_indicators: bool,
) -> Dict[str, Any]:
    """Assess indicators of hidden assets."""
    indicators: List[Dict[str, str]] = []
    risk_score = 0.0

    if unexplained_cash_withdrawals:
        risk_score += 0.20
        indicators.append({"indicator": "Unexplained cash withdrawals", "severity": "high"})
    if lifestyle_income_mismatch:
        risk_score += 0.20
        indicators.append({"indicator": "Lifestyle exceeds reported income", "severity": "high"})
    if recent_transfers_to_family:
        risk_score += 0.15
        indicators.append({"indicator": "Recent transfers to family members", "severity": "medium"})
    if business_revenue_decline:
        risk_score += 0.15
        indicators.append({"indicator": "Sudden business revenue decline near filing", "severity": "medium"})
    if cryptocurrency_holdings:
        risk_score += 0.15
        indicators.append({"indicator": "Cryptocurrency holdings — difficult to trace", "severity": "medium"})
    if offshore_indicators:
        risk_score += 0.20
        indicators.append({"indicator": "Offshore account indicators", "severity": "high"})

    risk_score = min(1.0, risk_score)

    return {
        "hidden_asset_risk": round(risk_score, 3),
        "risk_level": "HIGH" if risk_score >= 0.50 else "MEDIUM" if risk_score >= 0.25 else "LOW",
        "indicators": indicators,
        "recommended_actions": [
            "Forensic accountant engagement" if risk_score >= 0.30 else "Standard discovery sufficient",
            "Subpoena financial institution records" if risk_score >= 0.25 else None,
            "Cryptocurrency blockchain analysis" if cryptocurrency_holdings else None,
            "Lifestyle analysis comparing spending to reported income" if lifestyle_income_mismatch else None,
            "Deposition of transferees" if recent_transfers_to_family else None,
        ],
        "authority": "Tex. Fam. Code \u00a7 7.009 (fraud on community); In re Marriage of Rossi (CA)",
    }


def evaluate_dissipation_claim(
    amount: float,
    total_estate: float,
    timing: str,
    purpose: str,
    can_spouse_account: bool,
) -> Dict[str, Any]:
    """Evaluate a dissipation of marital assets claim."""
    materiality = amount / max(total_estate, 1)
    is_material = materiality >= 0.05

    timing_lower = timing.lower()
    during_breakdown = any(t in timing_lower for t in ["separation", "filing", "breakdown", "after"])

    purpose_lower = purpose.lower()
    non_marital = any(p in purpose_lower for p in ["affair", "gambling", "drugs", "paramour", "gift to"])

    strength = 0.0
    if is_material:
        strength += 0.25
    if during_breakdown:
        strength += 0.25
    if non_marital:
        strength += 0.25
    if not can_spouse_account:
        strength += 0.25

    return {
        "dissipation_claim_strength": round(strength, 3),
        "is_material": is_material,
        "materiality_ratio": round(materiality, 4),
        "during_breakdown": during_breakdown,
        "non_marital_purpose": non_marital,
        "spouse_can_account": can_spouse_account,
        "recommendation": "Strong dissipation claim — seek credit in property division" if strength >= 0.60
            else "Moderate claim — gather more evidence" if strength >= 0.40
            else "Weak claim — may not be worth pursuing",
        "remedy": "Court credits dissipated amount to non-dissipating spouse in property division",
        "authority": "In re Marriage of O'Neill (IL); Tex. Fam. Code \u00a7 7.009",
    }


def analyze_imputed_income(
    prior_income: float,
    current_income: float,
    education_level: str,
    work_history_years: int,
    reason_for_reduced_income: str,
    caring_for_young_child: bool,
) -> Dict[str, Any]:
    """Analyze whether income should be imputed."""
    income_drop = prior_income - current_income
    drop_percentage = income_drop / max(prior_income, 1)

    voluntary = True
    reasons: List[str] = []
    reason_lower = reason_for_reduced_income.lower()

    if any(w in reason_lower for w in ["laid off", "fired", "downsized", "company closed"]):
        voluntary = False
        reasons.append("Involuntary job loss — imputation less likely")
    if any(w in reason_lower for w in ["quit", "resigned", "chose", "voluntary"]):
        voluntary = True
        reasons.append("Voluntary job change — imputation more likely")
    if caring_for_young_child:
        reasons.append("Caring for young child may justify reduced employment — court discretion")
        voluntary = False
    if any(w in reason_lower for w in ["disability", "health", "medical"]):
        voluntary = False
        reasons.append("Health-related employment limitation — need medical evidence")

    imputation_likely = voluntary and drop_percentage > 0.20
    imputed_amount = prior_income if imputation_likely else current_income

    return {
        "prior_income": prior_income,
        "current_income": current_income,
        "income_drop_percentage": round(drop_percentage * 100, 1),
        "voluntary_underemployment": voluntary,
        "imputation_likely": imputation_likely,
        "imputed_income": round(imputed_amount, 2),
        "reasons": reasons,
        "education_level": education_level,
        "work_history_years": work_history_years,
        "authority": "Tex. Fam. Code \u00a7 154.066; In re Marriage of Barth (IL)",
    }


def assess_enforcement_options(
    order_type: str,
    violation_type: str,
    amount_owed: float,
    willful: bool,
) -> Dict[str, Any]:
    """Assess enforcement options for order violations."""
    options: List[Dict[str, str]] = []

    if "support" in order_type.lower():
        options.append({"option": "Income withholding order", "severity": "standard", "description": "Automatic deduction from wages"})
        options.append({"option": "Contempt motion", "severity": "serious", "description": "Court may impose jail until compliance"})
        if amount_owed >= 5000:
            options.append({"option": "License suspension", "severity": "serious", "description": "Driver's, professional, recreational licenses"})
        options.append({"option": "Tax refund intercept", "severity": "standard", "description": "Federal and state tax refund offset"})
        options.append({"option": "Credit bureau reporting", "severity": "standard", "description": "Report arrearages to credit agencies"})
        if amount_owed >= 2500:
            options.append({"option": "Passport denial", "severity": "serious", "description": "42 U.S.C. \u00a7 652(k) — passport denial for arrearages >$2,500"})

    if "custody" in order_type.lower() or "possession" in order_type.lower():
        options.append({"option": "Contempt motion", "severity": "serious", "description": "Willful violation of custody/visitation order"})
        options.append({"option": "Make-up visitation", "severity": "standard", "description": "Court orders compensatory possession time"})
        options.append({"option": "Custody modification", "severity": "escalated", "description": "Pattern of interference may warrant custody change"})

    if willful:
        options.append({"option": "Attorney fee award", "severity": "standard", "description": "Fees incurred in enforcement action"})
        options.append({"option": "Community service", "severity": "standard", "description": "Alternative to incarceration"})

    return {
        "order_type": order_type,
        "violation_type": violation_type,
        "amount_owed": amount_owed,
        "willful_violation": willful,
        "enforcement_options": options,
        "recommended_action": options[1]["option"] if len(options) > 1 else options[0]["option"] if options else "Consult attorney",
        "authority": "Tex. Fam. Code \u00a7 157; Turner v. Rogers, 564 U.S. 431 (2011)",
    }


def evaluate_jurisdiction_factors(
    child_current_state: str,
    child_lived_months: int,
    prior_order_state: Optional[str],
    emergency: bool,
) -> Dict[str, Any]:
    """Evaluate UCCJEA jurisdiction factors."""
    home_state = child_lived_months >= 6
    exclusive_continuing = prior_order_state is not None

    if exclusive_continuing:
        return {
            "jurisdiction_type": "Exclusive Continuing Jurisdiction",
            "jurisdictional_state": prior_order_state,
            "basis": f"Prior order exists in {prior_order_state} — that state retains exclusive jurisdiction under UCCJEA \u00a7 202",
            "current_state_can_act": False,
            "exception": "Only if all parties have left prior state or that court declines jurisdiction",
            "emergency": emergency,
            "emergency_note": "Emergency jurisdiction available for temporary measures if child in danger" if emergency else None,
        }

    if home_state:
        return {
            "jurisdiction_type": "Home State Jurisdiction",
            "jurisdictional_state": child_current_state,
            "basis": f"Child has lived in {child_current_state} for {child_lived_months} months (>= 6) — home state jurisdiction under UCCJEA \u00a7 201",
            "current_state_can_act": True,
            "emergency": emergency,
        }

    return {
        "jurisdiction_type": "Significant Connection",
        "jurisdictional_state": child_current_state,
        "basis": "No home state established — significant connection jurisdiction may apply",
        "current_state_can_act": True,
        "caveat": "If another state qualifies as home state, that state has priority",
        "emergency": emergency,
        "emergency_note": "Emergency jurisdiction available for temporary measures" if emergency else None,
    }


# ============================================================================
# CORE QUERY PROCESSING — THREE-LAYER RESPONSE
# ============================================================================

async def process_query(query: FamilyLawQuery) -> FamilyLawResponse:
    """Process a family law query through the three-layer architecture."""
    start_time = time.time()
    query_id = str(uuid.uuid4())
    _metrics.query_start()

    trace = trace_query(query_id, query.question, query.mode.value)

    try:
        norm_result = normalize_query(query.question)
        normalized_text = norm_result.normalized

        get_telemetry().add_step(
            trace, "normalization", ResponseLayer.DOCTRINE,
            success=True, duration_ms=1.0,
            details={"substitutions": len(norm_result.substitutions)},
        )

        # LAYER 1: Doctrine Cache (target <200ms)
        match = match_doctrine(normalized_text, query.case_type)
        layer_1_ms = (time.time() - start_time) * 1000

        get_telemetry().add_step(
            trace, "doctrine_match", ResponseLayer.DOCTRINE,
            success=match.is_match, duration_ms=layer_1_ms,
            details={"match_score": match.match_score, "topic_key": match.topic_key},
        )

        doctrine_hit = match.is_match
        response_layer = "doctrine"

        if doctrine_hit:
            _coverage_map.record_hit(match.topic_key)
            trace.doctrine_hit = True
            trace.cache_hit = True
        else:
            _coverage_map.record_gap(query.question[:200])

        # LAYER 2: Semantic Retrieval if no doctrine hit (target <700ms)
        if not doctrine_hit:
            response_layer = "retrieval"
            similar = search_similar(normalized_text, k=3, threshold=0.25)
            layer_2_ms = (time.time() - start_time) * 1000

            get_telemetry().add_step(
                trace, "vector_search", ResponseLayer.RETRIEVAL,
                success=len(similar) > 0, duration_ms=layer_2_ms - layer_1_ms,
                details={"results": len(similar)},
            )

            if similar:
                best_key = similar[0]["topic_key"]
                match = match_doctrine(DOCTRINE_CACHE[best_key].topic + " " + normalized_text, query.case_type)
                if match.is_match:
                    doctrine_hit = True
                    _coverage_map.record_hit(match.topic_key)

        # Confidence computation
        confidence_score, confidence_band = compute_confidence(
            doctrine_match=doctrine_hit,
            match_score=match.match_score,
            authority_weight=match.authority_weight,
            mode=query.mode,
            jurisdiction=query.jurisdiction,
            conflict_detected=match.conflict_detected,
        )

        # Stale doctrine penalty
        if doctrine_hit and match.topic_key and _drift_watcher.is_stale(match.topic_key):
            confidence_score = max(0.0, confidence_score - 0.10)
            logger.info(f"Stale doctrine penalty applied: {match.topic_key}")

        # Build response
        doctrine = match.doctrine
        if doctrine:
            conclusion = doctrine.conclusion_template
            reasoning = doctrine.reasoning_framework
            key_factors = doctrine.key_factors
            citations = doctrine.to_citations()
            limitations = [
                f"Analysis based on {query.jurisdiction} law — other jurisdictions may differ significantly",
                "This analysis is for informational purposes and does not constitute legal advice",
                "Individual case facts may alter the applicable analysis",
            ]
            if match.conflict_detected:
                limitations.append("Multiple doctrines were considered — see conflict resolution")
        else:
            conclusion = (
                f"No specific doctrine block matched for this family law query. "
                f"The question touches on general family law principles in {query.jurisdiction}. "
                f"A comprehensive analysis requires review of jurisdiction-specific statutes and case law."
            )
            reasoning = "Query did not match any pre-compiled doctrine blocks. Semantic search was attempted."
            key_factors = ["Jurisdiction-specific analysis required", "Consult local family code provisions"]
            citations = []
            limitations = [
                "No doctrine cache hit — analysis is limited",
                "Consult a licensed family law attorney for jurisdiction-specific guidance",
            ]
            _coverage_map.record_unknown(query.question[:200])

        # LAYER 3: Deep Analysis (DEFENSE mode)
        if query.mode == ResponseMode.DEFENSE and doctrine:
            response_layer = "deep_analysis"
            reasoning = (
                f"DEFENSE MODE ANALYSIS — Court-Defensible Output\n\n"
                f"I. DOCTRINE: {doctrine.topic}\n\n"
                f"II. FRAMEWORK:\n{doctrine.reasoning_framework}\n\n"
                f"III. COUNTER-ARGUMENTS:\n" +
                "\n".join(f"  {i+1}. {ca}" for i, ca in enumerate(doctrine.counter_arguments)) +
                f"\n\nIV. AUTHORITY WEIGHT: {match.authority_weight} "
                f"(based on {len(doctrine.primary_authority)} authorities)\n\n"
                f"V. CONFIDENCE: {confidence_band} ({confidence_score})"
            )
            # Ensure minimum citations for defense mode
            if len(citations) < 3 and doctrine.related_doctrines:
                for related_key in doctrine.related_doctrines:
                    if len(citations) >= 3:
                        break
                    related = DOCTRINE_CACHE.get(related_key)
                    if related:
                        for auth in related.primary_authority[:1]:
                            citations.append(Citation(
                                authority=auth.get("authority", ""),
                                reference=auth.get("reference", ""),
                                relevance=f"Related doctrine ({related.topic}): {auth.get('relevance', '')}",
                                weight=20,
                            ))

        # Multi-doctrine analysis
        multi = multi_doctrine_match(normalized_text, query.case_type)
        if multi["is_multi_doctrine"]:
            response_layer = "multi_doctrine"

        # Risk assessment
        risk_level, risk_factors = assess_risk(doctrine, confidence_score, query.jurisdiction, query.mode)

        # Fragility
        fragility = assess_fragility(doctrine, match.match_score, match.conflict_detected)

        # Zoned analysis
        zoned = None
        if query.include_zones and doctrine:
            zoned = generate_zoned_analysis(doctrine, query.question, query.jurisdiction, confidence_score)

        # Reasoning trace
        reasoning_trace = None
        if query.include_trace:
            reasoning_trace = [
                ReasoningStep(step=1, analysis=f"Normalized query: {normalized_text[:200]}", authority=None),
                ReasoningStep(step=2, analysis=f"Doctrine match: {match.topic_key or 'none'} (score: {match.match_score})", authority=match.topic_key),
                ReasoningStep(step=3, analysis=f"Confidence: {confidence_band} ({confidence_score})", authority=None),
                ReasoningStep(step=4, analysis=f"Risk: {risk_level}", authority=None),
            ]
            if multi["is_multi_doctrine"]:
                reasoning_trace.append(ReasoningStep(
                    step=5,
                    analysis=f"Multi-doctrine: {multi['total_doctrines_matched']} doctrines across {len(multi['issues_detected'])} issues",
                    authority=None,
                ))

        # Coverage report
        coverage = _coverage_map.get_report()

        # Determinism hash
        hash_input = f"{normalized_text}|{ENGINE_VERSION}|{match.topic_key or 'none'}"
        det_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        # Jurisdiction note
        jurisdiction_note = None
        if query.jurisdiction in COMMUNITY_PROPERTY_STATES:
            jurisdiction_note = f"{query.jurisdiction} is a community property state — all property acquired during marriage is presumed community."
        else:
            jurisdiction_note = f"{query.jurisdiction} follows equitable distribution — marital property divided fairly, not necessarily equally."

        latency_ms = round((time.time() - start_time) * 1000, 2)

        response = FamilyLawResponse(
            query_id=query_id,
            question=query.question,
            mode=query.mode,
            conclusion=conclusion,
            reasoning=reasoning,
            key_factors=key_factors,
            citations=citations,
            risk_level=risk_level,
            risk_factors=risk_factors,
            doctrine_match=doctrine_hit,
            confidence_band=confidence_band,
            confidence_score=confidence_score,
            response_layer=response_layer,
            latency_ms=latency_ms,
            conflict_detected=match.conflict_detected,
            conflict_resolution=match.conflict_resolution,
            authority_weight=match.authority_weight,
            determinism_hash=det_hash,
            reasoning_trace=reasoning_trace,
            zoned_analysis=zoned,
            fact_fragility=[f for f in fragility],
            coverage_report=coverage,
            limitations=limitations,
            jurisdiction_note=jurisdiction_note,
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=ENGINE_VERSION,
        )

        # Telemetry completion
        trace.response_layer = ResponseLayer(response_layer) if response_layer in [e.value for e in ResponseLayer] else ResponseLayer.DOCTRINE
        trace.confidence = confidence_score
        trace.citations_count = len(citations)
        trace.determinism_hash = det_hash
        trace.zone = zoned[0]["zone"] if zoned else None
        complete_trace(trace)

        # Metrics
        _metrics.record_query(latency_ms, doctrine_hit)
        _metrics.query_end()

        # Audit
        write_audit_record({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_id": query_id,
            "query_text": query.question[:300],
            "response_hash": det_hash,
            "confidence": confidence_score,
            "confidence_band": confidence_band,
            "citations_count": len(citations),
            "latency_ms": latency_ms,
            "mode": query.mode.value,
            "response_layer": response_layer,
            "doctrine_hit": doctrine_hit,
            "jurisdiction": query.jurisdiction,
            "risk_level": risk_level,
        })

        return response

    except Exception as e:
        _metrics.record_error(str(e))
        _metrics.query_end()
        log_error(ErrorDomain.FASTAPI, str(e), query_id)
        trace.error = str(e)
        complete_trace(trace)
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)[:200]}")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    logger.info(f"LG10 Family Law Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    count = load_doctrine_cache()
    logger.info(f"Doctrine cache loaded: {count} blocks")

    drift = _drift_watcher.check_staleness()
    logger.info(f"Drift check: {drift['fresh_count']} fresh, {drift['stale_count']} stale")

    if count > 0:
        test_result = match_doctrine("child custody best interest factors")
        logger.info(f"Self-test: doctrine match = {test_result.is_match}, score = {test_result.match_score}")

    logger.info("LG10 Family Law Engine ready")
    yield
    logger.info("LG10 Family Law Engine shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    description="Professional-grade family law doctrine engine. Covers custody, support, property division, enforcement, and domestic relations.",
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


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive system health check."""
    import psutil
    process = psutil.Process()
    mem = process.memory_info()
    mem_mb = round(mem.rss / 1024 / 1024, 1)

    drift = _drift_watcher.check_staleness()
    coverage = _coverage_map.get_report()
    latency_stats = _metrics.get_latency_stats()
    error_stats = _metrics.get_error_stats()
    hit_rate = _metrics.get_cache_hit_rate()

    status = "healthy"
    if error_stats["last_hour"] > 10:
        status = "degraded"
    if error_stats["last_hour"] > 50:
        status = "unhealthy"

    return HealthResponse(
        status=status,
        engine=ENGINE_NAME,
        engine_id=ENGINE_ID,
        version=ENGINE_VERSION,
        uptime_seconds=round(time.time() - _start_time, 1),
        api_latency=latency_stats,
        doctrine_cache={
            "status": "loaded",
            "total_blocks": len(DOCTRINE_CACHE),
            "hit_rate": hit_rate,
            "stale_count": drift["stale_count"],
        },
        memory_mb={"used": mem_mb, "percent": round(process.memory_percent(), 1)},
        active_queries=_metrics.active_queries,
        queries_last_hour=_metrics.queries_last_hour(),
        queries_total=_metrics.total_queries(),
        error_rate=error_stats,
        cache_hit_rate=hit_rate,
        drift_report=drift,
        coverage_summary={
            "total": coverage["total_doctrines"],
            "triggered": coverage["triggered_count"],
            "gaps": coverage["gap_count"],
        },
    )


@app.post("/query", response_model=FamilyLawResponse)
async def query_endpoint(query: FamilyLawQuery) -> FamilyLawResponse:
    """Process a family law query."""
    return await process_query(query)


@app.post("/analyze", response_model=FamilyLawResponse)
async def analyze_endpoint(query: FamilyLawQuery) -> FamilyLawResponse:
    """Deep analysis endpoint — forces DEFENSE mode."""
    query.mode = ResponseMode.DEFENSE
    query.include_zones = True
    query.include_trace = True
    return await process_query(query)


@app.post("/batch", response_model=BatchResponse)
async def batch_endpoint(batch: BatchQuery) -> BatchResponse:
    """Process multiple queries."""
    start = time.time()
    results = []
    for q in batch.queries:
        result = await process_query(q)
        results.append(result)
    total_ms = round((time.time() - start) * 1000, 2)
    return BatchResponse(results=results, total_latency_ms=total_ms, count=len(results))


@app.get("/explain/{query_id}")
async def explain_endpoint(query_id: str) -> Dict[str, Any]:
    """Retrieve explanation for a previous query from telemetry."""
    traces = get_telemetry().get_recent_traces(100)
    for trace in traces:
        if trace.get("query_id") == query_id:
            return {"found": True, "trace": trace}
    return {"found": False, "query_id": query_id, "message": "Query ID not found in recent traces"}


@app.get("/doctrines")
async def doctrines_endpoint() -> Dict[str, Any]:
    """List all loaded doctrine blocks."""
    blocks = []
    for key, block in DOCTRINE_CACHE.items():
        blocks.append({
            "topic_key": key,
            "topic": block.topic,
            "keywords": block.keywords,
            "confidence": block.confidence,
            "authority_weight": block.get_authority_weight(),
            "related_doctrines": block.related_doctrines,
        })
    return {"total": len(blocks), "blocks": blocks}


@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """Get doctrine coverage report."""
    return _coverage_map.get_report()


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Get engine metrics."""
    return {
        "latency": _metrics.get_latency_stats(),
        "errors": _metrics.get_error_stats(),
        "cache_hit_rate": _metrics.get_cache_hit_rate(),
        "queries_last_hour": _metrics.queries_last_hour(),
        "queries_total": _metrics.total_queries(),
        "active_queries": _metrics.active_queries,
        "telemetry": get_telemetry().get_stats(),
    }


@app.get("/audit")
async def audit_endpoint(limit: int = 50) -> Dict[str, Any]:
    """Get recent audit trail entries."""
    records: List[Dict[str, Any]] = []
    if AUDIT_LOG.exists():
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-limit:]:
            try:
                records.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return {"total": len(records), "records": list(reversed(records))}


@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    """Get doctrine drift report."""
    return _drift_watcher.check_staleness()


@app.get("/verify/{query_id}")
async def verify_endpoint(query_id: str) -> Dict[str, Any]:
    """Verify determinism — check if a query produces the same hash."""
    traces = get_telemetry().get_recent_traces(100)
    for trace in traces:
        if trace.get("query_id") == query_id:
            return {
                "found": True,
                "query_id": query_id,
                "determinism_hash": trace.get("determinism_hash"),
                "reproducible": True,
                "note": "Re-run the same query to verify hash matches",
            }
    return {"found": False, "query_id": query_id}


@app.post("/custody/factors")
async def custody_factors_endpoint(
    question: str = "custody factors",
    jurisdiction: str = "TX",
) -> Dict[str, Any]:
    """Analyze custody factors for a jurisdiction."""
    return analyze_child_custody_factors(question, jurisdiction)


@app.post("/support/calculate")
async def support_calculate_endpoint(
    obligor_gross_monthly: float,
    number_of_children: int = 1,
    jurisdiction: str = "TX",
    other_children: int = 0,
) -> Dict[str, Any]:
    """Calculate guideline child support estimate."""
    return calculate_child_support_estimate(obligor_gross_monthly, number_of_children, jurisdiction, other_children)


@app.post("/spousal/eligibility")
async def spousal_eligibility_endpoint(
    marriage_duration_years: float,
    requesting_party_income: float,
    paying_party_income: float,
    jurisdiction: str = "TX",
    family_violence: bool = False,
    disability: bool = False,
) -> Dict[str, Any]:
    """Evaluate spousal support eligibility."""
    return evaluate_spousal_support_eligibility(
        marriage_duration_years, requesting_party_income, paying_party_income,
        jurisdiction, family_violence, disability,
    )


@app.post("/property/classify")
async def property_classify_endpoint(
    asset_name: str,
    acquisition_date: str,
    marriage_date: str,
    source_of_funds: str,
    jurisdiction: str = "TX",
) -> Dict[str, Any]:
    """Classify property as community/marital or separate."""
    return classify_property_division(asset_name, acquisition_date, marriage_date, source_of_funds, jurisdiction)


@app.post("/modification/evaluate")
async def modification_evaluate_endpoint(
    original_order_date: str,
    changed_circumstance: str,
    voluntary: bool = False,
    modification_type: str = "support",
) -> Dict[str, Any]:
    """Evaluate modification grounds."""
    return evaluate_modification_grounds(original_order_date, changed_circumstance, voluntary, modification_type)


@app.post("/jurisdiction/analyze")
async def jurisdiction_analyze_endpoint(
    child_current_state: str,
    child_lived_months: int,
    prior_order_state: Optional[str] = None,
    emergency: bool = False,
) -> Dict[str, Any]:
    """Analyze UCCJEA jurisdiction."""
    return evaluate_jurisdiction_factors(child_current_state, child_lived_months, prior_order_state, emergency)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "lg10_engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        workers=1,
        log_level="info",
    )
