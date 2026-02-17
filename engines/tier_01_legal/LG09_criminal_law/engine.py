"""
LG09 Criminal Law Engine - Main FastAPI Application
====================================================
Full TIE-20 architecture criminal law analysis engine with 20 mandatory
components fully implemented.

Port: 8399
Domain: Criminal Law (Federal + Texas State)
Authority: 11.0 SOVEREIGN

TIE-20 Components:
    1.  three_layer_response         - Quick / Standard / Deep analysis
    2.  response_modes               - DET / EF / HYBRID
    3.  doctrine_cache               - Pre-loaded criminal law doctrines
    4.  authority_hardening          - Citation validation and source verification
    5.  confidence_stratification    - Multi-level confidence scoring
    6.  semantic_normalization       - Query term normalization
    7.  vector_search_chromadb       - Semantic similarity search
    8.  telemetry_module             - Performance telemetry
    9.  doctrine_drift_watcher       - Content change detection
    10. doctrine_coverage_map        - Topic coverage tracking
    11. metrics_collector            - System metrics aggregation
    12. health_endpoint              - Health check API
    13. zoned_analysis               - Jurisdiction-based analysis zones
    14. fact_fragility_scoring       - Fact confidence assessment
    15. audit_trail_jsonl            - Append-only JSONL audit log
    16. determinism_hash_sha256      - Reproducible response hashing
    17. fastapi_server               - HTTP API server
    18. loguru_logging               - Structured logging
    19. multi_doctrine_decomposition - Cross-domain doctrine analysis
    20. deep_analysis_mode           - Extended multi-source synthesis

Author: ECHO OMEGA PRIME
Engine: LG09 Criminal Law
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import threading
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Engine-local imports
# ---------------------------------------------------------------------------

# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DoctrineCacheManager,
    DoctrineBlock,
    get_doctrine_cache,
    get_doctrine,
    search_doctrines,
    get_doctrine_stats,
    ALL_DOCTRINE_LISTS,
)
from semantic import (
    SemanticNormalizer,
    NormalizationResult,
    CrimeCategory,
    get_normalizer,
    normalize_semantics,
)
from search import (
    ChromaSearchEngine,
    StructuredSearch,
    SearchResponse,
    SearchResult,
    get_search_engine,
    get_structured_search,
)
from telemetry import (
    TelemetryEngine,
    ResponseLayer,
    ErrorDomain,
    MutationType,
    MutationOrigin,
    QueryTrace,
    get_telemetry,
    trace_query as telem_trace_query,
    complete_trace as telem_complete_trace,
    log_error as telem_log_error,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

ENGINE_ID = "LG09"
ENGINE_NAME = "Criminal Law Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8399
ENGINE_HOST = "0.0.0.0"

CONFIG_PATH = Path(__file__).parent / "config.json"
LOG_DIR = Path(__file__).parent / "logs"
AUDIT_DIR = Path(__file__).parent / "audit"

LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Loguru configuration (TIE component 18: loguru_logging)
# ---------------------------------------------------------------------------

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>LG09</cyan> | {message}",
)
logger.add(
    LOG_DIR / "lg09_engine_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | LG09 | {message}",
)


def load_config() -> Dict[str, Any]:
    """Load engine configuration from config.json."""
    if CONFIG_PATH.exists():
        raw = CONFIG_PATH.read_text(encoding="utf-8")
        return json.loads(raw)
    logger.warning("config.json not found, using defaults")
    return {}


ENGINE_CONFIG = load_config()


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class ResponseMode(str, Enum):
    """Response mode enumeration."""
    DET = "DET"
    EF = "EF"
    HYBRID = "HYBRID"


class AnalysisLayer(str, Enum):
    """Analysis depth layer."""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class QueryRequest(BaseModel):
    """Incoming query request."""
    query: str = Field(..., min_length=1, max_length=10000, description="Criminal law query text")
    mode: ResponseMode = Field(default=ResponseMode.HYBRID, description="Response mode: DET, EF, or HYBRID")
    layer: Optional[AnalysisLayer] = Field(default=None, description="Force specific analysis layer")
    jurisdiction: Optional[str] = Field(default=None, description="Jurisdiction filter: federal, texas, model_penal_code")
    category: Optional[str] = Field(default=None, description="Crime category filter")
    max_results: int = Field(default=5, ge=1, le=50, description="Max doctrine results")
    include_cases: bool = Field(default=True, description="Include leading cases in response")
    include_statutes: bool = Field(default=True, description="Include key statutes in response")
    include_elements: bool = Field(default=True, description="Include elements in response")
    include_defenses: bool = Field(default=True, description="Include defenses in response")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the elements of felony murder in Texas?",
                "mode": "HYBRID",
                "jurisdiction": "texas",
                "category": "homicide",
                "max_results": 5,
            }
        }


class ConfidenceLevel(BaseModel):
    """Confidence level descriptor."""
    level: str
    score: float
    label: str
    factors: List[str] = Field(default_factory=list)


class CitationEntry(BaseModel):
    """A single citation with verification status."""
    citation: str
    source_type: str = Field(description="statute, case, regulation, constitutional")
    verified: bool = False
    jurisdiction: str = "unknown"


class DoctrineMatch(BaseModel):
    """A matched doctrine block."""
    cache_key: str
    topic: str
    summary: str
    key_statutes: List[str] = Field(default_factory=list)
    elements: List[str] = Field(default_factory=list)
    defenses: List[str] = Field(default_factory=list)
    remedies: List[str] = Field(default_factory=list)
    leading_cases: List[str] = Field(default_factory=list)
    jurisdiction: str = "unknown"
    category: str = "general"
    match_score: float = 0.0
    content_hash: str = ""


class FactFragilityAssessment(BaseModel):
    """Assessment of how fragile/reliable a fact is."""
    fact: str
    fragility_score: float = Field(ge=0.0, le=1.0, description="0=rock solid, 1=highly fragile")
    factors: List[str] = Field(default_factory=list)
    recommendation: str = ""


class AnalysisResponse(BaseModel):
    """Complete analysis response."""
    query_id: str
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str
    query: str
    normalized_query: str
    response_mode: str
    analysis_layer: str
    jurisdiction_detected: List[str] = Field(default_factory=list)
    categories_detected: List[str] = Field(default_factory=list)
    confidence: ConfidenceLevel
    doctrines: List[DoctrineMatch] = Field(default_factory=list)
    citations: List[CitationEntry] = Field(default_factory=list)
    analysis_text: str = ""
    fact_fragility: List[FactFragilityAssessment] = Field(default_factory=list)
    determinism_hash: str = ""
    latency_ms: float = 0.0
    semantic_mappings_applied: int = 0
    vector_results_count: int = 0
    doctrine_cache_hits: int = 0
    doctrine_cache_misses: int = 0
    disclosure_caveat: str = (
        "This analysis is for informational purposes only and does not constitute legal advice. "
        "Criminal law is jurisdiction-specific and fact-dependent. Consult a licensed attorney "
        "for advice on specific legal matters."
    )


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    components: Dict[str, Any]
    timestamp: str


class DriftReport(BaseModel):
    """Doctrine drift detection report."""
    checked_at: str
    total_doctrines: int
    drifted: List[Dict[str, Any]] = Field(default_factory=list)
    unchanged: int = 0
    status: str = "stable"


class CoverageReport(BaseModel):
    """Doctrine coverage map report."""
    total_topics: int
    covered_categories: Dict[str, int] = Field(default_factory=dict)
    covered_jurisdictions: Dict[str, int] = Field(default_factory=dict)
    gaps: List[str] = Field(default_factory=list)
    coverage_pct: float = 0.0


class MetricsSnapshot(BaseModel):
    """Metrics collection snapshot."""
    timestamp: str
    engine_id: str
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    doctrine_stats: Dict[str, Any] = Field(default_factory=dict)
    search_stats: Dict[str, Any] = Field(default_factory=dict)
    normalizer_stats: Dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# TIE COMPONENT 15: AUDIT TRAIL (JSONL)
# =============================================================================

class AuditTrail:
    """
    Append-only JSONL audit trail for every query processed.
    Each line is a complete JSON object with query, response, and metadata.
    """

    def __init__(self, audit_dir: Path) -> None:
        self._audit_dir = audit_dir
        self._audit_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._entry_count: int = 0

    def _current_file(self) -> Path:
        """Get the current day's audit file."""
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self._audit_dir / f"audit_{date_str}.jsonl"

    def record(self, entry: Dict[str, Any]) -> None:
        """Append an audit entry to the JSONL file."""
        entry["_audit_timestamp"] = datetime.now(timezone.utc).isoformat()
        entry["_audit_engine"] = ENGINE_ID
        line = json.dumps(entry, default=str, ensure_ascii=False)
        filepath = self._current_file()
        with self._lock:
            with filepath.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            self._entry_count += 1

    def read_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Read recent audit entries."""
        filepath = self._current_file()
        if not filepath.exists():
            return []
        entries: List[Dict[str, Any]] = []
        with self._lock:
            lines = filepath.read_text(encoding="utf-8").strip().split("\n")
        for line in lines[-limit:]:
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return entries

    @property
    def entry_count(self) -> int:
        """Total entries written this session."""
        return self._entry_count

    def health_check(self) -> Dict[str, Any]:
        """Check audit trail health."""
        filepath = self._current_file()
        return {
            "component": "audit_trail",
            "status": "healthy",
            "current_file": str(filepath),
            "file_exists": filepath.exists(),
            "session_entries": self._entry_count,
        }


# =============================================================================
# TIE COMPONENT 16: DETERMINISM HASH (SHA-256)
# =============================================================================

class DeterminismHasher:
    """
    Generate SHA-256 determinism hashes for response reproducibility.
    Given the same input and doctrine state, the hash must be identical.
    """

    @staticmethod
    def hash_response(
        query: str,
        mode: str,
        jurisdiction: List[str],
        doctrine_keys: List[str],
        doctrine_hashes: List[str],
        analysis_text: str,
    ) -> str:
        """Generate deterministic hash of a response."""
        content = json.dumps({
            "query": query.strip().lower(),
            "mode": mode,
            "jurisdiction": sorted(jurisdiction),
            "doctrine_keys": sorted(doctrine_keys),
            "doctrine_hashes": sorted(doctrine_hashes),
            "analysis_text": analysis_text.strip(),
        }, sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def hash_doctrine_state(cache: DoctrineCacheManager) -> str:
        """Hash the entire doctrine cache state for drift detection."""
        hashes = cache.export_hashes()
        sorted_pairs = sorted(hashes.items())
        content = json.dumps(sorted_pairs, sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# =============================================================================
# TIE COMPONENT 9: DOCTRINE DRIFT WATCHER
# =============================================================================

class DoctrineDriftWatcher:
    """
    Monitor doctrine cache for unexpected changes.
    Compares current hashes against a baseline snapshot.
    """

    def __init__(self, cache: DoctrineCacheManager) -> None:
        self._cache = cache
        self._baseline: Dict[str, str] = {}
        self._drift_events: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def take_baseline(self) -> int:
        """Snapshot current doctrine hashes as the baseline."""
        with self._lock:
            self._baseline = self._cache.export_hashes()
        logger.info(f"Drift watcher baseline captured: {len(self._baseline)} doctrines")
        return len(self._baseline)

    def check_drift(self) -> DriftReport:
        """Compare current state against baseline."""
        current_hashes = self._cache.export_hashes()
        drifted: List[Dict[str, Any]] = []
        unchanged = 0

        with self._lock:
            baseline = dict(self._baseline)

        for key, current_hash in current_hashes.items():
            baseline_hash = baseline.get(key)
            if baseline_hash is None:
                drifted.append({
                    "key": key,
                    "type": "new_doctrine",
                    "detail": "Doctrine added after baseline",
                })
            elif baseline_hash != current_hash:
                drifted.append({
                    "key": key,
                    "type": "content_changed",
                    "old_hash": baseline_hash[:16],
                    "new_hash": current_hash[:16],
                })
            else:
                unchanged += 1

        for key in baseline:
            if key not in current_hashes:
                drifted.append({
                    "key": key,
                    "type": "doctrine_removed",
                    "detail": "Doctrine present in baseline but missing now",
                })

        with self._lock:
            self._drift_events.extend(drifted)

        status = "stable" if len(drifted) == 0 else "drifted"
        return DriftReport(
            checked_at=datetime.now(timezone.utc).isoformat(),
            total_doctrines=len(current_hashes),
            drifted=drifted,
            unchanged=unchanged,
            status=status,
        )

    def get_drift_history(self) -> List[Dict[str, Any]]:
        """Return all recorded drift events."""
        with self._lock:
            return list(self._drift_events)


# =============================================================================
# TIE COMPONENT 10: DOCTRINE COVERAGE MAP
# =============================================================================

class DoctrineCoverageMap:
    """
    Track which criminal law topics are covered and identify gaps.
    Compares actual doctrine blocks against the config.json topic taxonomy.
    """

    def __init__(self, cache: DoctrineCacheManager, config: Dict[str, Any]) -> None:
        self._cache = cache
        self._config = config

    def generate_report(self) -> CoverageReport:
        """Generate a coverage report comparing doctrines against config topics."""
        configured_topics = self._config.get("doctrine_topics", {})
        all_configured: Set[str] = set()
        for category, subtopics in configured_topics.items():
            for sub in subtopics:
                all_configured.add(f"{category}.{sub}")

        cached_keys = set(self._cache.get_all_keys())
        stats = self._cache.get_stats()

        gaps: List[str] = []
        for required_key in sorted(all_configured):
            found = False
            for cached_key in cached_keys:
                if required_key in cached_key or cached_key.endswith(required_key.split(".")[-1]):
                    found = True
                    break
            if not found:
                gaps.append(required_key)

        total_required = len(all_configured)
        covered = total_required - len(gaps)
        coverage_pct = round((covered / total_required * 100) if total_required > 0 else 0.0, 1)

        return CoverageReport(
            total_topics=total_required,
            covered_categories=stats.get("categories", {}),
            covered_jurisdictions=stats.get("jurisdictions", {}),
            gaps=gaps,
            coverage_pct=coverage_pct,
        )


# =============================================================================
# TIE COMPONENT 4: AUTHORITY HARDENING
# =============================================================================

class AuthorityHardener:
    """
    Validate and harden citations and authority references.
    Ensures cited statutes and cases are in known-good lists.
    """

    KNOWN_STATUTES: Set[str] = {
        "18 USC 1111", "18 USC 1112", "18 USC 113", "18 USC 922", "18 USC 924",
        "18 USC 1341", "18 USC 1343", "18 USC 1344", "18 USC 1956", "18 USC 1957",
        "18 USC 1961", "18 USC 1962", "18 USC 1963", "18 USC 1964",
        "18 USC 3553", "18 USC 3591", "18 USC 17",
        "21 USC 841", "21 USC 844", "21 USC 846", "21 USC 848",
        "26 USC 7201", "28 USC 2254", "28 USC 2255",
        "15 USC 78j", "15 USC 78ff",
        "Texas Penal Code Section 6.01", "Texas Penal Code Section 6.02",
        "Texas Penal Code Section 6.03",
        "Texas Penal Code Section 8.01", "Texas Penal Code Section 8.05",
        "Texas Penal Code Section 8.06",
        "Texas Penal Code Section 9.22", "Texas Penal Code Section 9.31",
        "Texas Penal Code Section 9.32", "Texas Penal Code Section 9.33",
        "Texas Penal Code Section 15.01", "Texas Penal Code Section 15.02",
        "Texas Penal Code Section 19.02", "Texas Penal Code Section 19.03",
        "Texas Penal Code Section 19.04", "Texas Penal Code Section 19.05",
        "Texas Penal Code Section 22.01", "Texas Penal Code Section 22.02",
        "Texas Penal Code Section 25.11",
        "Texas Penal Code Section 28.02", "Texas Penal Code Section 29.02",
        "Texas Penal Code Section 29.03",
        "Texas Penal Code Section 30.02", "Texas Penal Code Section 31.03",
        "MPC Section 2.01", "MPC Section 2.02", "MPC Section 2.03",
        "MPC Section 2.09", "MPC Section 3.02", "MPC Section 3.04",
        "MPC Section 5.01", "MPC Section 5.03",
        "MPC Section 210.2", "MPC Section 210.3", "MPC Section 210.4",
        "MPC Section 211.1", "MPC Section 220.1", "MPC Section 221.1",
    }

    KNOWN_CASE_FRAGMENTS: Set[str] = {
        "miranda v arizona", "mapp v ohio", "terry v ohio", "gideon v wainwright",
        "katz v united states", "brady v maryland", "strickland v washington",
        "batson v kentucky", "furman v georgia", "gregg v georgia",
        "atkins v virginia", "roper v simmons", "miller v alabama",
        "riley v california", "carpenter v united states",
        "united states v booker", "united states v jones",
        "morissette v united states", "apprendi v new jersey",
        "wong sun v united states", "united states v leon",
        "boykin v alabama", "faretta v california",
        "new york v quarles", "edwards v arizona",
        "chimel v california", "robinson v california",
        "gonzales v raich", "heller", "bruen",
        "padilla v kentucky", "lafler v cooper",
    }

    def validate_citation(self, citation: str) -> CitationEntry:
        """Validate a single citation against known authorities."""
        citation_lower = citation.lower().strip()
        source_type = self._classify_source(citation)
        verified = False

        if source_type == "statute":
            for known in self.KNOWN_STATUTES:
                if known.lower() in citation_lower or citation_lower in known.lower():
                    verified = True
                    break
        elif source_type == "case":
            for known_fragment in self.KNOWN_CASE_FRAGMENTS:
                if known_fragment in citation_lower:
                    verified = True
                    break
        elif source_type == "constitutional":
            verified = any(
                term in citation_lower
                for term in ["amendment", "constitution", "bill of rights"]
            )

        jurisdiction = self._detect_jurisdiction(citation)

        return CitationEntry(
            citation=citation,
            source_type=source_type,
            verified=verified,
            jurisdiction=jurisdiction,
        )

    def validate_citations(self, citations: List[str]) -> List[CitationEntry]:
        """Validate multiple citations."""
        return [self.validate_citation(c) for c in citations]

    def harden_response(self, doctrines: List[DoctrineBlock]) -> List[CitationEntry]:
        """Extract and validate all citations from doctrine matches."""
        all_citations: List[str] = []
        for d in doctrines:
            all_citations.extend(d.key_statutes)
            all_citations.extend(d.leading_cases)
        unique_citations = list(dict.fromkeys(all_citations))
        return self.validate_citations(unique_citations)

    @staticmethod
    def _classify_source(citation: str) -> str:
        """Classify the type of legal source."""
        lower = citation.lower()
        if any(term in lower for term in ["usc", "section", "tpc", "mpc", "cfr", "act"]):
            return "statute"
        if any(term in lower for term in [" v ", " v. ", "re ", "ex parte"]):
            return "case"
        if any(term in lower for term in ["amendment", "constitution"]):
            return "constitutional"
        if any(term in lower for term in ["regulation", "rule", "cfr"]):
            return "regulation"
        return "other"

    @staticmethod
    def _detect_jurisdiction(citation: str) -> str:
        """Detect jurisdiction from citation text."""
        lower = citation.lower()
        if "texas" in lower or "tpc" in lower or "tccp" in lower:
            return "texas"
        if any(term in lower for term in ["usc", "federal", "united states"]):
            return "federal"
        if "mpc" in lower or "model penal" in lower:
            return "model_penal_code"
        return "unknown"


# =============================================================================
# TIE COMPONENT 5: CONFIDENCE STRATIFICATION
# =============================================================================

class ConfidenceStratifier:
    """
    Multi-factor confidence scoring for criminal law analysis.
    Factors: doctrine match quality, citation count, jurisdiction specificity,
    search result relevance, and coverage depth.
    """

    LEVELS = {
        "DEFINITIVE": (0.95, "Definitive — Settled law with clear precedent"),
        "HIGH": (0.80, "High — Strong authority, minor variations possible"),
        "MODERATE": (0.60, "Moderate — Multiple interpretations exist"),
        "LOW": (0.40, "Low — Evolving area, conflicting authority"),
        "SPECULATIVE": (0.0, "Speculative — Limited authority, novel question"),
    }

    def score(
        self,
        doctrine_matches: int,
        verified_citations: int,
        total_citations: int,
        search_score: float,
        jurisdiction_match: bool,
        category_match: bool,
        mode: ResponseMode,
    ) -> ConfidenceLevel:
        """Calculate confidence level based on multiple factors."""
        factors: List[str] = []
        score = 0.0

        # Doctrine match factor (0-0.30)
        if doctrine_matches >= 3:
            score += 0.30
            factors.append(f"Strong doctrine coverage ({doctrine_matches} matches)")
        elif doctrine_matches >= 1:
            score += 0.15
            factors.append(f"Partial doctrine coverage ({doctrine_matches} matches)")
        else:
            factors.append("No direct doctrine matches")

        # Citation verification factor (0-0.25)
        if total_citations > 0:
            verification_rate = verified_citations / total_citations
            citation_score = verification_rate * 0.25
            score += citation_score
            factors.append(f"Citation verification: {verified_citations}/{total_citations}")
        else:
            factors.append("No citations to verify")

        # Search relevance factor (0-0.20)
        search_contribution = min(search_score, 1.0) * 0.20
        score += search_contribution
        if search_score >= 0.7:
            factors.append(f"High search relevance ({search_score:.2f})")
        elif search_score >= 0.4:
            factors.append(f"Moderate search relevance ({search_score:.2f})")
        else:
            factors.append(f"Low search relevance ({search_score:.2f})")

        # Jurisdiction match factor (0-0.15)
        if jurisdiction_match:
            score += 0.15
            factors.append("Jurisdiction-specific analysis")
        else:
            score += 0.05
            factors.append("General jurisdiction analysis")

        # Category match factor (0-0.10)
        if category_match:
            score += 0.10
            factors.append("Category-specific analysis")

        # Mode adjustment
        if mode == ResponseMode.DET:
            # DET mode has higher confidence for cached results, lower for gaps
            if doctrine_matches >= 2:
                score = min(score + 0.05, 1.0)
                factors.append("DET mode boost for strong doctrine match")
            else:
                score = max(score - 0.10, 0.0)
                factors.append("DET mode penalty for weak doctrine match")

        score = min(max(score, 0.0), 1.0)

        # Determine level
        level_name = "SPECULATIVE"
        level_label = self.LEVELS["SPECULATIVE"][1]
        for name, (threshold, label) in self.LEVELS.items():
            if score >= threshold:
                level_name = name
                level_label = label
                break

        return ConfidenceLevel(
            level=level_name,
            score=round(score, 4),
            label=level_label,
            factors=factors,
        )


# =============================================================================
# TIE COMPONENT 13: ZONED ANALYSIS
# =============================================================================

class ZonedAnalyzer:
    """
    Jurisdiction-aware analysis zones.
    Routes queries to the appropriate jurisdiction zone for specialized handling.
    """

    ZONES = {
        "federal": {
            "label": "Federal Criminal Law",
            "primary_sources": ["Title 18 USC", "Title 21 USC", "Federal Sentencing Guidelines"],
            "courts": ["US Supreme Court", "Circuit Courts", "District Courts"],
        },
        "texas": {
            "label": "Texas Criminal Law",
            "primary_sources": ["Texas Penal Code", "Texas Code of Criminal Procedure"],
            "courts": ["Court of Criminal Appeals", "Courts of Appeals", "District Courts"],
        },
        "model_penal_code": {
            "label": "Model Penal Code",
            "primary_sources": ["MPC (ALI 1962)"],
            "courts": [],
        },
    }

    def analyze_zones(self, jurisdiction_hints: List[str]) -> Dict[str, Any]:
        """Determine applicable analysis zones from jurisdiction hints."""
        active_zones: List[Dict[str, Any]] = []
        for hint in jurisdiction_hints:
            zone_info = self.ZONES.get(hint)
            if zone_info:
                active_zones.append({
                    "zone": hint,
                    "label": zone_info["label"],
                    "primary_sources": zone_info["primary_sources"],
                    "courts": zone_info["courts"],
                })

        if not active_zones:
            active_zones.append({
                "zone": "federal",
                "label": "Federal Criminal Law (default)",
                "primary_sources": self.ZONES["federal"]["primary_sources"],
                "courts": self.ZONES["federal"]["courts"],
            })

        return {
            "active_zones": active_zones,
            "zone_count": len(active_zones),
            "multi_jurisdiction": len(active_zones) > 1,
        }


# =============================================================================
# TIE COMPONENT 14: FACT FRAGILITY SCORING
# =============================================================================

class FactFragilityScorer:
    """
    Assess how fragile or reliable facts and legal conclusions are.
    Higher fragility means more likely to change with new information or
    different judicial interpretation.
    """

    FRAGILITY_INDICATORS = {
        "circuit_split": 0.3,
        "evolving_standard": 0.25,
        "state_variation": 0.2,
        "recent_ruling": 0.15,
        "minority_view": 0.35,
        "dicta_only": 0.4,
        "statutory_interpretation": 0.15,
        "constitutional_question": 0.2,
        "fact_specific": 0.1,
        "legislative_change_pending": 0.3,
    }

    def score_facts(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        jurisdiction_count: int,
    ) -> List[FactFragilityAssessment]:
        """Score the fragility of key facts from matched doctrines."""
        assessments: List[FactFragilityAssessment] = []

        for doctrine in doctrines:
            base_fragility = 0.1
            factors: List[str] = []

            # Multi-jurisdiction increases fragility
            if jurisdiction_count > 1:
                base_fragility += self.FRAGILITY_INDICATORS["state_variation"]
                factors.append("Multiple jurisdictions may differ")

            # Constitutional topics are more interpretive
            if doctrine.category == "constitutional_rights":
                base_fragility += self.FRAGILITY_INDICATORS["constitutional_question"]
                factors.append("Constitutional interpretation may evolve")

            # Sentencing guidelines change frequently
            if doctrine.category == "sentencing":
                base_fragility += self.FRAGILITY_INDICATORS["evolving_standard"]
                factors.append("Sentencing law subject to frequent legislative changes")

            # Drug offenses have evolving standards
            if doctrine.category == "drug_offenses":
                base_fragility += self.FRAGILITY_INDICATORS["legislative_change_pending"]
                factors.append("Drug scheduling and penalties under active legislative review")

            # Fact-specific defenses
            if doctrine.category == "defenses":
                base_fragility += self.FRAGILITY_INDICATORS["fact_specific"]
                factors.append("Defense applicability is highly fact-specific")

            fragility = min(base_fragility, 1.0)
            recommendation = self._recommend(fragility)

            assessments.append(FactFragilityAssessment(
                fact=doctrine.topic,
                fragility_score=round(fragility, 3),
                factors=factors,
                recommendation=recommendation,
            ))

        return assessments

    @staticmethod
    def _recommend(fragility: float) -> str:
        """Generate recommendation based on fragility score."""
        if fragility < 0.2:
            return "Reliable — well-settled law, cite with confidence"
        elif fragility < 0.4:
            return "Generally reliable — verify jurisdiction-specific rules"
        elif fragility < 0.6:
            return "Use with caution — check for recent changes and local variations"
        elif fragility < 0.8:
            return "Fragile — significant risk of variation, conduct thorough research"
        else:
            return "Highly fragile — treat as preliminary; independent verification essential"


# =============================================================================
# TIE COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# =============================================================================

class MultiDoctrineDecomposer:
    """
    Decompose complex queries touching multiple doctrine areas.
    Identifies cross-cutting issues and synthesizes across domains.
    """

    def decompose(
        self,
        categories: List[str],
        doctrines: List[DoctrineBlock],
        query: str,
    ) -> Dict[str, Any]:
        """Break a query into its component doctrine domains."""
        domains: Dict[str, List[str]] = defaultdict(list)
        cross_cutting: List[str] = []

        for doctrine in doctrines:
            domains[doctrine.category].append(doctrine.topic)

        # Detect cross-cutting issues
        if len(domains) > 1:
            domain_names = list(domains.keys())
            for i, d1 in enumerate(domain_names):
                for d2 in domain_names[i + 1:]:
                    issue = self._find_cross_cutting(d1, d2, query)
                    if issue:
                        cross_cutting.append(issue)

        # Check for elements + defenses interaction
        if "elements_of_crime" in domains and "defenses" in domains:
            cross_cutting.append(
                "Elements analysis interacts with defense applicability — "
                "defense may negate specific element of the offense"
            )

        # Check for sentencing + offense interaction
        if "sentencing" in domains and any(
            cat in domains for cat in ["homicide", "drug_offenses", "property_crimes"]
        ):
            cross_cutting.append(
                "Sentencing analysis depends on specific offense elements and "
                "applicable enhancements"
            )

        return {
            "domains_involved": dict(domains),
            "domain_count": len(domains),
            "cross_cutting_issues": cross_cutting,
            "is_multi_domain": len(domains) > 1,
            "primary_domain": max(domains.keys(), key=lambda k: len(domains[k])) if domains else "unknown",
        }

    @staticmethod
    def _find_cross_cutting(domain1: str, domain2: str, query: str) -> Optional[str]:
        """Identify cross-cutting issues between two domains."""
        pairs = {
            ("constitutional_rights", "search_seizure"): (
                "Constitutional search/seizure issues may affect admissibility "
                "of evidence for the substantive offense"
            ),
            ("homicide", "defenses"): (
                "Homicide charge requires analysis of applicable defenses "
                "(self-defense, heat of passion, insanity)"
            ),
            ("drug_offenses", "constitutional_rights"): (
                "Drug cases frequently involve Fourth Amendment search issues "
                "and Fifth Amendment Miranda questions"
            ),
            ("fraud_white_collar", "sentencing"): (
                "White collar sentencing involves loss calculations, "
                "guidelines departures, and restitution"
            ),
            ("inchoate_crimes", "homicide"): (
                "Inchoate offense analysis (attempt, conspiracy) interacts "
                "with completed homicide analysis"
            ),
        }
        key = (domain1, domain2)
        reverse_key = (domain2, domain1)
        return pairs.get(key) or pairs.get(reverse_key)


# =============================================================================
# TIE COMPONENT 20: DEEP ANALYSIS MODE
# =============================================================================

class DeepAnalyzer:
    """
    Extended multi-source synthesis for deep analysis mode.
    Combines doctrine cache, vector search, semantic normalization,
    cross-jurisdiction comparison, and fact fragility into a comprehensive
    analysis narrative.
    """

    def __init__(
        self,
        cache: DoctrineCacheManager,
        normalizer: SemanticNormalizer,
        search_engine: ChromaSearchEngine,
        authority: AuthorityHardener,
        fragility: FactFragilityScorer,
        decomposer: MultiDoctrineDecomposer,
        zoned: ZonedAnalyzer,
    ) -> None:
        self._cache = cache
        self._normalizer = normalizer
        self._search = search_engine
        self._authority = authority
        self._fragility = fragility
        self._decomposer = decomposer
        self._zoned = zoned

    def analyze(
        self,
        query: str,
        norm_result: NormalizationResult,
        doctrine_matches: List[DoctrineBlock],
        search_results: SearchResponse,
        jurisdiction_hints: List[str],
    ) -> str:
        """Generate a deep analysis narrative."""
        parts: List[str] = []

        # Opening
        parts.append(f"DEEP ANALYSIS: {query}")
        parts.append("=" * 60)

        # Jurisdictions
        zones = self._zoned.analyze_zones(jurisdiction_hints)
        if zones["multi_jurisdiction"]:
            parts.append(
                f"\nMulti-Jurisdiction Analysis ({zones['zone_count']} zones): "
                + ", ".join(z["label"] for z in zones["active_zones"])
            )
        else:
            zone_label = zones["active_zones"][0]["label"] if zones["active_zones"] else "General"
            parts.append(f"\nJurisdiction: {zone_label}")

        # Semantic normalization summary
        if norm_result.was_normalized:
            parts.append(
                f"\nSemantic Normalization: {norm_result.mapping_count} terms normalized"
            )
            for mapping in norm_result.mappings_applied[:5]:
                parts.append(f"  - '{mapping['from']}' -> '{mapping['to']}'")

        # Category detection
        if norm_result.crime_categories:
            parts.append(f"\nCrime Categories Detected: {', '.join(norm_result.crime_categories)}")

        # Doctrine analysis
        parts.append(f"\n{'='*60}")
        parts.append("DOCTRINE ANALYSIS")
        parts.append(f"{'='*60}")

        for i, doctrine in enumerate(doctrine_matches, 1):
            parts.append(f"\n--- {i}. {doctrine.topic} ({doctrine.jurisdiction}) ---")
            parts.append(f"Summary: {doctrine.summary[:500]}")

            if doctrine.elements:
                parts.append("\nElements:")
                for elem in doctrine.elements:
                    parts.append(f"  * {elem}")

            if doctrine.defenses:
                parts.append("\nApplicable Defenses:")
                for defense in doctrine.defenses:
                    parts.append(f"  * {defense}")

            if doctrine.key_statutes:
                parts.append("\nKey Statutes:")
                for statute in doctrine.key_statutes:
                    parts.append(f"  * {statute}")

            if doctrine.leading_cases:
                parts.append("\nLeading Cases:")
                for case in doctrine.leading_cases:
                    parts.append(f"  * {case}")

            if doctrine.remedies:
                parts.append("\nRemedies/Penalties:")
                for remedy in doctrine.remedies:
                    parts.append(f"  * {remedy}")

        # Multi-doctrine decomposition
        categories_present = [d.category for d in doctrine_matches]
        decomp = self._decomposer.decompose(categories_present, doctrine_matches, query)
        if decomp["is_multi_domain"]:
            parts.append(f"\n{'='*60}")
            parts.append("CROSS-DOMAIN ANALYSIS")
            parts.append(f"{'='*60}")
            parts.append(f"Domains involved: {decomp['domain_count']}")
            for issue in decomp["cross_cutting_issues"]:
                parts.append(f"  - {issue}")

        # Vector search additional results
        if search_results.total_results > 0:
            parts.append(f"\n{'='*60}")
            parts.append(f"SEMANTIC SEARCH RESULTS ({search_results.total_results} matches)")
            parts.append(f"{'='*60}")
            for result in search_results.results[:3]:
                parts.append(
                    f"  [{result.score:.3f}] {result.doctrine_key}: {result.text[:200]}..."
                )

        # Fragility assessment
        if doctrine_matches:
            fragilities = self._fragility.score_facts(
                doctrine_matches, query, len(jurisdiction_hints)
            )
            parts.append(f"\n{'='*60}")
            parts.append("FACT FRAGILITY ASSESSMENT")
            parts.append(f"{'='*60}")
            for fa in fragilities:
                parts.append(f"  {fa.fact}: {fa.fragility_score:.3f} — {fa.recommendation}")

        parts.append(f"\n{'='*60}")
        parts.append("[END OF DEEP ANALYSIS]")

        return "\n".join(parts)


# =============================================================================
# CORE ANALYSIS PIPELINE
# =============================================================================

class CriminalLawPipeline:
    """
    Main analysis pipeline implementing all 20 TIE components.

    Orchestrates: normalization -> doctrine lookup -> vector search ->
    authority hardening -> confidence scoring -> fact fragility ->
    multi-doctrine decomposition -> response generation -> audit trail ->
    determinism hashing -> telemetry recording.
    """

    def __init__(self) -> None:
        # Core components
        self.doctrine_cache: DoctrineCacheManager = get_doctrine_cache()
        self.normalizer: SemanticNormalizer = get_normalizer()
        self.search_engine: ChromaSearchEngine = get_search_engine(
            collection_name=ENGINE_CONFIG.get("vector_search", {}).get("collection_name", "lg09_criminal_law"),
            persist_directory=ENGINE_CONFIG.get("vector_search", {}).get("persist_directory"),
        )
        self.structured_search: StructuredSearch = StructuredSearch(self.search_engine)
        self.telemetry: TelemetryEngine = get_telemetry(engine_id=ENGINE_ID)

        # TIE components
        self.authority: AuthorityHardener = AuthorityHardener()
        self.confidence: ConfidenceStratifier = ConfidenceStratifier()
        self.zoned: ZonedAnalyzer = ZonedAnalyzer()
        self.fragility: FactFragilityScorer = FactFragilityScorer()
        self.decomposer: MultiDoctrineDecomposer = MultiDoctrineDecomposer()
        self.audit_trail: AuditTrail = AuditTrail(AUDIT_DIR)
        self.hasher: DeterminismHasher = DeterminismHasher()
        self.drift_watcher: DoctrineDriftWatcher = DoctrineDriftWatcher(self.doctrine_cache)
        self.coverage_map: DoctrineCoverageMap = DoctrineCoverageMap(self.doctrine_cache, ENGINE_CONFIG)
        self.deep_analyzer: DeepAnalyzer = DeepAnalyzer(
            cache=self.doctrine_cache,
            normalizer=self.normalizer,
            search_engine=self.search_engine,
            authority=self.authority,
            fragility=self.fragility,
            decomposer=self.decomposer,
            zoned=self.zoned,
        )

        # Populate search index from doctrine cache
        self._populate_search_index()

        # Take drift baseline
        self.drift_watcher.take_baseline()

        # Boot timestamp
        self._boot_time = time.time()

        logger.info(
            f"CriminalLawPipeline initialized: {self.doctrine_cache.size} doctrines, "
            f"search index: {self.search_engine.collection_size} entries"
        )

    def _populate_search_index(self) -> None:
        """Load all doctrines into the vector/keyword search index."""
        entries = self.doctrine_cache.to_search_entries()
        indexed = self.search_engine.add_doctrines_bulk(entries)
        logger.info(f"Search index populated with {indexed} doctrine entries")

    # -------------------------------------------------------------------------
    # LAYER SELECTION (TIE Component 1: three_layer_response)
    # -------------------------------------------------------------------------

    def _select_layer(
        self,
        request: QueryRequest,
        norm_result: NormalizationResult,
    ) -> AnalysisLayer:
        """Select analysis layer based on query complexity and user preference."""
        if request.layer is not None:
            return request.layer

        query_len = len(request.query)
        has_jurisdiction = bool(norm_result.jurisdiction_hints)
        category_count = len(norm_result.crime_categories)
        mapping_count = norm_result.mapping_count

        # Quick: short simple queries with single category
        if query_len < 100 and category_count <= 1 and mapping_count <= 2:
            return AnalysisLayer.QUICK

        # Deep: long complex queries, multiple categories/jurisdictions
        if query_len > 500 or category_count >= 3 or (has_jurisdiction and category_count >= 2):
            return AnalysisLayer.DEEP

        return AnalysisLayer.STANDARD

    # -------------------------------------------------------------------------
    # MAIN ANALYSIS
    # -------------------------------------------------------------------------

    def analyze(self, request: QueryRequest) -> AnalysisResponse:
        """Execute the full analysis pipeline."""
        start_time = time.time()
        query_id = str(uuid.uuid4())

        # Start telemetry trace
        trace_id = self.telemetry.trace_query(
            query_text=request.query,
            response_mode=request.mode.value,
            jurisdiction=request.jurisdiction or "auto",
        )

        try:
            # STEP 1: Semantic normalization (TIE Component 6)
            norm_result = self.normalizer.normalize(request.query)
            self.telemetry.record_semantic_normalization(trace_id)

            # STEP 2: Layer selection (TIE Component 1)
            layer = self._select_layer(request, norm_result)

            # STEP 3: Determine effective jurisdiction
            jurisdictions = norm_result.jurisdiction_hints
            if request.jurisdiction and request.jurisdiction not in jurisdictions:
                jurisdictions.insert(0, request.jurisdiction)
            if not jurisdictions:
                jurisdictions = ["federal"]

            # STEP 4: Doctrine cache lookup (TIE Component 3)
            doctrine_matches = self._lookup_doctrines(
                norm_result, request.category, jurisdictions, request.max_results, trace_id
            )

            # STEP 5: Vector search (TIE Component 7)
            search_results = self.search_engine.search(
                query=norm_result.normalized_text,
                max_results=request.max_results,
                jurisdiction_filter=request.jurisdiction,
                category_filter=request.category,
            )
            self.telemetry.record_vector_search(trace_id, search_results.total_results)

            # Merge search results with doctrine matches (avoid duplicates)
            doctrine_matches = self._merge_search_results(
                doctrine_matches, search_results, request.max_results
            )

            # STEP 6: Authority hardening (TIE Component 4)
            citations = self.authority.harden_response(doctrine_matches)

            # STEP 7: Confidence stratification (TIE Component 5)
            verified_count = sum(1 for c in citations if c.verified)
            avg_search_score = (
                sum(r.score for r in search_results.results) / len(search_results.results)
                if search_results.results else 0.0
            )
            confidence = self.confidence.score(
                doctrine_matches=len(doctrine_matches),
                verified_citations=verified_count,
                total_citations=len(citations),
                search_score=avg_search_score,
                jurisdiction_match=bool(request.jurisdiction),
                category_match=bool(request.category),
                mode=request.mode,
            )

            # STEP 8: Fact fragility scoring (TIE Component 14)
            fragility_assessments = self.fragility.score_facts(
                doctrine_matches, request.query, len(jurisdictions)
            )

            # STEP 9: Analysis text generation
            if layer == AnalysisLayer.DEEP:
                analysis_text = self.deep_analyzer.analyze(
                    query=request.query,
                    norm_result=norm_result,
                    doctrine_matches=doctrine_matches,
                    search_results=search_results,
                    jurisdiction_hints=jurisdictions,
                )
            elif layer == AnalysisLayer.STANDARD:
                analysis_text = self._standard_analysis(
                    doctrine_matches, norm_result, jurisdictions
                )
            else:
                analysis_text = self._quick_analysis(doctrine_matches, norm_result)

            # STEP 10: Build doctrine match models
            doctrine_models = self._build_doctrine_models(
                doctrine_matches, search_results, request
            )

            # STEP 11: Determinism hash (TIE Component 16)
            determinism_hash = self.hasher.hash_response(
                query=request.query,
                mode=request.mode.value,
                jurisdiction=jurisdictions,
                doctrine_keys=[d.cache_key for d in doctrine_matches],
                doctrine_hashes=[d.content_hash for d in doctrine_matches],
                analysis_text=analysis_text,
            )

            # STEP 12: Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # STEP 13: Build response
            response = AnalysisResponse(
                query_id=query_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                query=request.query,
                normalized_query=norm_result.normalized_text,
                response_mode=request.mode.value,
                analysis_layer=layer.value,
                jurisdiction_detected=jurisdictions,
                categories_detected=norm_result.crime_categories,
                confidence=confidence,
                doctrines=doctrine_models,
                citations=citations,
                analysis_text=analysis_text,
                fact_fragility=fragility_assessments,
                determinism_hash=determinism_hash,
                latency_ms=round(latency_ms, 2),
                semantic_mappings_applied=norm_result.mapping_count,
                vector_results_count=search_results.total_results,
                doctrine_cache_hits=len(doctrine_matches),
                doctrine_cache_misses=max(0, request.max_results - len(doctrine_matches)),
            )

            # STEP 14: Complete telemetry trace
            response_layer = {
                AnalysisLayer.QUICK: ResponseLayer.QUICK,
                AnalysisLayer.STANDARD: ResponseLayer.STANDARD,
                AnalysisLayer.DEEP: ResponseLayer.DEEP,
            }.get(layer, ResponseLayer.STANDARD)
            self.telemetry.complete_trace(
                trace_id=trace_id,
                response_layer=response_layer,
                confidence_score=confidence.score,
            )

            # STEP 15: Audit trail (TIE Component 15)
            self.audit_trail.record({
                "query_id": query_id,
                "query": request.query[:500],
                "mode": request.mode.value,
                "layer": layer.value,
                "jurisdictions": jurisdictions,
                "categories": norm_result.crime_categories,
                "confidence_score": confidence.score,
                "confidence_level": confidence.level,
                "doctrine_count": len(doctrine_matches),
                "citation_count": len(citations),
                "verified_citations": verified_count,
                "latency_ms": round(latency_ms, 2),
                "determinism_hash": determinism_hash[:32],
            })

            return response

        except Exception as exc:
            self.telemetry.complete_trace(
                trace_id=trace_id,
                response_layer=ResponseLayer.FALLBACK,
                confidence_score=0.0,
                error=str(exc),
            )
            self.telemetry.log_error(
                ErrorDomain.RESPONSE_GENERATION, str(exc), trace_id
            )
            logger.exception(f"Pipeline error for query_id={query_id}")
            raise

    # -------------------------------------------------------------------------
    # DOCTRINE LOOKUP HELPERS
    # -------------------------------------------------------------------------

    def _lookup_doctrines(
        self,
        norm_result: NormalizationResult,
        category_filter: Optional[str],
        jurisdictions: List[str],
        max_results: int,
        trace_id: str,
    ) -> List[DoctrineBlock]:
        """Look up doctrines from cache using normalized query."""
        results: List[DoctrineBlock] = []

        # Direct cache search
        cache_results = self.doctrine_cache.search(
            norm_result.normalized_text, max_results=max_results * 2
        )

        for doctrine in cache_results:
            # Apply filters
            if category_filter and doctrine.category != category_filter:
                continue
            if jurisdictions and doctrine.jurisdiction not in jurisdictions and "general" not in jurisdictions:
                pass  # Don't filter by jurisdiction — return all matches

            results.append(doctrine)
            self.telemetry.record_doctrine_hit(trace_id, doctrine.cache_key)

        # If category filter yielded no results, try without it
        if not results and category_filter:
            results = cache_results[:max_results]
            for doctrine in results:
                self.telemetry.record_doctrine_hit(trace_id, doctrine.cache_key)

        # Record misses if we got fewer than requested
        if len(results) < max_results:
            self.telemetry.record_doctrine_miss(
                trace_id, f"_insufficient_results_{len(results)}"
            )

        return results[:max_results]

    def _merge_search_results(
        self,
        doctrine_matches: List[DoctrineBlock],
        search_results: SearchResponse,
        max_results: int,
    ) -> List[DoctrineBlock]:
        """Merge vector search results with doctrine cache matches."""
        existing_keys = {d.cache_key for d in doctrine_matches}

        for result in search_results.results:
            if len(doctrine_matches) >= max_results:
                break
            doctrine = self.doctrine_cache.get(result.doctrine_key)
            if doctrine and doctrine.cache_key not in existing_keys:
                doctrine_matches.append(doctrine)
                existing_keys.add(doctrine.cache_key)

        return doctrine_matches

    # -------------------------------------------------------------------------
    # ANALYSIS TEXT GENERATORS
    # -------------------------------------------------------------------------

    def _quick_analysis(
        self,
        doctrines: List[DoctrineBlock],
        norm_result: NormalizationResult,
    ) -> str:
        """Generate quick-layer analysis text."""
        if not doctrines:
            return (
                f"No direct doctrine matches found for: {norm_result.original_text}. "
                "Consider refining the query or specifying a jurisdiction."
            )
        parts = [f"Quick Analysis: {norm_result.original_text}"]
        parts.append("-" * 40)
        for d in doctrines[:3]:
            parts.append(f"\n{d.topic} ({d.jurisdiction}): {d.summary[:300]}...")
        return "\n".join(parts)

    def _standard_analysis(
        self,
        doctrines: List[DoctrineBlock],
        norm_result: NormalizationResult,
        jurisdictions: List[str],
    ) -> str:
        """Generate standard-layer analysis text."""
        if not doctrines:
            return (
                f"No doctrine matches for: {norm_result.original_text}. "
                f"Jurisdictions searched: {', '.join(jurisdictions)}."
            )
        parts = [f"Standard Analysis: {norm_result.original_text}"]
        parts.append(f"Jurisdictions: {', '.join(jurisdictions)}")
        parts.append("=" * 50)

        for i, d in enumerate(doctrines, 1):
            parts.append(f"\n{i}. {d.topic} [{d.jurisdiction}]")
            parts.append(f"   {d.summary[:500]}")
            if d.elements:
                parts.append("   Elements:")
                for elem in d.elements[:5]:
                    parts.append(f"     - {elem}")
            if d.key_statutes:
                parts.append(f"   Statutes: {', '.join(d.key_statutes[:3])}")
            if d.leading_cases:
                parts.append(f"   Cases: {', '.join(d.leading_cases[:3])}")

        return "\n".join(parts)

    def _build_doctrine_models(
        self,
        doctrines: List[DoctrineBlock],
        search_results: SearchResponse,
        request: QueryRequest,
    ) -> List[DoctrineMatch]:
        """Convert DoctrineBlocks to response models."""
        models: List[DoctrineMatch] = []
        search_score_map: Dict[str, float] = {}
        for r in search_results.results:
            search_score_map[r.doctrine_key] = r.score

        for d in doctrines:
            score = search_score_map.get(d.cache_key, 0.5)
            model = DoctrineMatch(
                cache_key=d.cache_key,
                topic=d.topic,
                summary=d.summary,
                key_statutes=d.key_statutes if request.include_statutes else [],
                elements=d.elements if request.include_elements else [],
                defenses=d.defenses if request.include_defenses else [],
                remedies=d.remedies,
                leading_cases=d.leading_cases if request.include_cases else [],
                jurisdiction=d.jurisdiction,
                category=d.category,
                match_score=round(score, 4),
                content_hash=d.content_hash,
            )
            models.append(model)

        return models

    # -------------------------------------------------------------------------
    # METRICS AND HEALTH
    # -------------------------------------------------------------------------

    def get_metrics(self) -> MetricsSnapshot:
        """Collect all system metrics (TIE Component 11)."""
        return MetricsSnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            engine_id=ENGINE_ID,
            telemetry=self.telemetry.get_full_metrics(),
            doctrine_stats=self.doctrine_cache.get_stats(),
            search_stats=self.search_engine.get_collection_stats(),
            normalizer_stats=self.normalizer.get_stats(),
        )

    def get_health(self) -> HealthResponse:
        """Health check across all components (TIE Component 12)."""
        uptime = time.time() - self._boot_time

        components = {
            "doctrine_cache": self.doctrine_cache.health_check(),
            "vector_search": self.search_engine.health_check(),
            "telemetry": self.telemetry.get_health_metrics(),
            "audit_trail": self.audit_trail.health_check(),
        }

        overall_status = "healthy"
        for comp_name, comp_data in components.items():
            comp_status = comp_data.get("status", "unknown")
            if comp_status == "degraded":
                overall_status = "degraded"
            elif comp_status == "unhealthy":
                overall_status = "unhealthy"

        return HealthResponse(
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            version=ENGINE_VERSION,
            status=overall_status,
            uptime_seconds=round(uptime, 1),
            components=components,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# =============================================================================
# FASTAPI APPLICATION (TIE Component 17)
# =============================================================================

pipeline: Optional[CriminalLawPipeline] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize pipeline on startup."""
    global pipeline
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    pipeline = CriminalLawPipeline()
    logger.info(
        f"{ENGINE_NAME} ready: {pipeline.doctrine_cache.size} doctrines loaded, "
        f"search index: {pipeline.search_engine.collection_size} entries"
    )
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"LG09 {ENGINE_NAME}",
    description="Full TIE-20 criminal law analysis engine covering federal and Texas state criminal law",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

# CORS
cors_config = ENGINE_CONFIG.get("cors", {})
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.get("allow_origins", ["*"]),
    allow_methods=cors_config.get("allow_methods", ["GET", "POST", "OPTIONS"]),
    allow_headers=cors_config.get("allow_headers", ["*"]),
    allow_credentials=True,
)


def get_pipeline() -> CriminalLawPipeline:
    """Get the initialized pipeline or raise."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return pipeline


# -------------------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------------------

@app.get("/", response_model=Dict[str, Any])
async def root() -> Dict[str, Any]:
    """Engine info endpoint."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": "criminal_law",
        "status": "operational",
        "endpoints": [
            "POST /analyze",
            "GET /health",
            "GET /metrics",
            "GET /doctrines",
            "GET /doctrine/{cache_key}",
            "GET /search",
            "GET /normalize",
            "GET /drift",
            "GET /coverage",
            "GET /audit",
            "GET /traces",
        ],
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_query(request: QueryRequest) -> AnalysisResponse:
    """
    Main analysis endpoint.

    Processes a criminal law query through the full TIE-20 pipeline:
    normalization, doctrine lookup, vector search, authority hardening,
    confidence scoring, and response generation.
    """
    pipe = get_pipeline()
    return pipe.analyze(request)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint (TIE Component 12)."""
    pipe = get_pipeline()
    return pipe.get_health()


@app.get("/metrics", response_model=MetricsSnapshot)
async def get_metrics() -> MetricsSnapshot:
    """Metrics collection endpoint (TIE Component 11)."""
    pipe = get_pipeline()
    return pipe.get_metrics()


@app.get("/doctrines", response_model=Dict[str, Any])
async def list_doctrines(
    category: Optional[str] = Query(None, description="Filter by category"),
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
) -> Dict[str, Any]:
    """List available doctrines with optional filtering."""
    pipe = get_pipeline()
    cache = pipe.doctrine_cache

    if category:
        doctrines = cache.get_by_category(category)
    elif jurisdiction:
        doctrines = cache.get_by_jurisdiction(jurisdiction)
    else:
        doctrines = [cache.get(key) for key in cache.get_all_keys()]
        doctrines = [d for d in doctrines if d is not None]

    return {
        "total": len(doctrines),
        "categories": cache.get_all_categories(),
        "jurisdictions": cache.get_all_jurisdictions(),
        "doctrines": [
            {
                "cache_key": d.cache_key,
                "topic": d.topic,
                "category": d.category,
                "jurisdiction": d.jurisdiction,
                "severity": d.severity,
            }
            for d in doctrines
        ],
    }


@app.get("/doctrine/{cache_key}", response_model=Dict[str, Any])
async def get_doctrine_detail(cache_key: str) -> Dict[str, Any]:
    """Get detailed information for a specific doctrine."""
    pipe = get_pipeline()
    doctrine = pipe.doctrine_cache.get(cache_key)
    if doctrine is None:
        raise HTTPException(status_code=404, detail=f"Doctrine not found: {cache_key}")
    return doctrine.to_dict()


@app.get("/search", response_model=SearchResponse)
async def search_endpoint(
    q: str = Query(..., min_length=1, description="Search query"),
    max_results: int = Query(10, ge=1, le=50),
    jurisdiction: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
) -> SearchResponse:
    """Vector/keyword search endpoint (TIE Component 7)."""
    pipe = get_pipeline()
    return pipe.search_engine.search(
        query=q,
        max_results=max_results,
        jurisdiction_filter=jurisdiction,
        category_filter=category,
    )


@app.get("/normalize", response_model=Dict[str, Any])
async def normalize_endpoint(
    q: str = Query(..., min_length=1, description="Text to normalize"),
) -> Dict[str, Any]:
    """Semantic normalization endpoint (TIE Component 6)."""
    pipe = get_pipeline()
    result = pipe.normalizer.normalize(q)
    return result.to_dict()


@app.get("/drift", response_model=DriftReport)
async def drift_check() -> DriftReport:
    """Doctrine drift detection endpoint (TIE Component 9)."""
    pipe = get_pipeline()
    return pipe.drift_watcher.check_drift()


@app.get("/coverage", response_model=CoverageReport)
async def coverage_report() -> CoverageReport:
    """Doctrine coverage map endpoint (TIE Component 10)."""
    pipe = get_pipeline()
    return pipe.coverage_map.generate_report()


@app.get("/audit", response_model=Dict[str, Any])
async def audit_endpoint(
    limit: int = Query(50, ge=1, le=500, description="Max entries to return"),
) -> Dict[str, Any]:
    """Audit trail endpoint (TIE Component 15)."""
    pipe = get_pipeline()
    entries = pipe.audit_trail.read_recent(limit)
    return {
        "total_session_entries": pipe.audit_trail.entry_count,
        "returned": len(entries),
        "entries": entries,
    }


@app.get("/traces", response_model=Dict[str, Any])
async def traces_endpoint(
    limit: int = Query(20, ge=1, le=100),
) -> Dict[str, Any]:
    """Telemetry traces endpoint (TIE Component 8)."""
    pipe = get_pipeline()
    traces = pipe.telemetry.recent_traces(limit)
    return {
        "returned": len(traces),
        "traces": traces,
    }


@app.get("/zones", response_model=Dict[str, Any])
async def zones_endpoint(
    jurisdiction: Optional[str] = Query(None, description="Jurisdiction to analyze"),
) -> Dict[str, Any]:
    """Zoned analysis endpoint (TIE Component 13)."""
    pipe = get_pipeline()
    hints = [jurisdiction] if jurisdiction else []
    return pipe.zoned.analyze_zones(hints)


@app.get("/fragility", response_model=Dict[str, Any])
async def fragility_endpoint(
    q: str = Query(..., min_length=1, description="Query for fragility assessment"),
    max_results: int = Query(5, ge=1, le=20),
) -> Dict[str, Any]:
    """Fact fragility scoring endpoint (TIE Component 14)."""
    pipe = get_pipeline()
    norm_result = pipe.normalizer.normalize(q)
    doctrines = pipe.doctrine_cache.search(norm_result.normalized_text, max_results)
    assessments = pipe.fragility.score_facts(
        doctrines, q, len(norm_result.jurisdiction_hints)
    )
    return {
        "query": q,
        "assessments": [a.model_dump() for a in assessments],
    }


@app.get("/decompose", response_model=Dict[str, Any])
async def decompose_endpoint(
    q: str = Query(..., min_length=1, description="Query to decompose"),
    max_results: int = Query(5, ge=1, le=20),
) -> Dict[str, Any]:
    """Multi-doctrine decomposition endpoint (TIE Component 19)."""
    pipe = get_pipeline()
    norm_result = pipe.normalizer.normalize(q)
    doctrines = pipe.doctrine_cache.search(norm_result.normalized_text, max_results)
    categories = [d.category for d in doctrines]
    result = pipe.decomposer.decompose(categories, doctrines, q)
    return result


@app.get("/determinism", response_model=Dict[str, Any])
async def determinism_endpoint() -> Dict[str, Any]:
    """Doctrine state determinism hash endpoint (TIE Component 16)."""
    pipe = get_pipeline()
    state_hash = DeterminismHasher.hash_doctrine_state(pipe.doctrine_cache)
    return {
        "engine_id": ENGINE_ID,
        "doctrine_state_hash": state_hash,
        "doctrine_count": pipe.doctrine_cache.size,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# -------------------------------------------------------------------------
# ERROR HANDLERS
# -------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with structured error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "engine_id": ENGINE_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(f"Unhandled exception: {exc}")
    if pipeline:
        pipeline.telemetry.log_error(
            ErrorDomain.UNKNOWN, f"Unhandled: {str(exc)[:500]}"
        )
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "detail": "Internal server error",
            "engine_id": ENGINE_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# =============================================================================
# BATCH ANALYSIS ENGINE
# =============================================================================

class BatchQueryRequest(BaseModel):
    """Request for batch analysis of multiple queries."""
    queries: List[QueryRequest] = Field(..., min_length=1, max_length=50)
    parallel: bool = Field(default=False, description="Run queries in parallel (async)")


class BatchQueryResponse(BaseModel):
    """Response for batch analysis."""
    batch_id: str
    total_queries: int
    completed: int
    failed: int
    results: List[AnalysisResponse] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    total_latency_ms: float = 0.0


class BatchAnalyzer:
    """
    Process multiple criminal law queries in a single request.
    Supports sequential and parallel execution modes.
    """

    def __init__(self, pipeline_ref: CriminalLawPipeline) -> None:
        self._pipeline = pipeline_ref

    def execute_sequential(self, batch: BatchQueryRequest) -> BatchQueryResponse:
        """Execute queries sequentially."""
        batch_id = str(uuid.uuid4())
        start_time = time.time()
        results: List[AnalysisResponse] = []
        errors: List[Dict[str, Any]] = []
        completed = 0
        failed = 0

        for i, query_req in enumerate(batch.queries):
            try:
                result = self._pipeline.analyze(query_req)
                results.append(result)
                completed += 1
            except Exception as exc:
                failed += 1
                errors.append({
                    "index": i,
                    "query": query_req.query[:200],
                    "error": str(exc)[:500],
                })
                logger.error(f"Batch query {i} failed: {exc}")

        total_latency = (time.time() - start_time) * 1000

        return BatchQueryResponse(
            batch_id=batch_id,
            total_queries=len(batch.queries),
            completed=completed,
            failed=failed,
            results=results,
            errors=errors,
            total_latency_ms=round(total_latency, 2),
        )

    async def execute_parallel(self, batch: BatchQueryRequest) -> BatchQueryResponse:
        """Execute queries in parallel using asyncio."""
        batch_id = str(uuid.uuid4())
        start_time = time.time()
        results: List[Optional[AnalysisResponse]] = [None] * len(batch.queries)
        errors: List[Dict[str, Any]] = []

        async def run_query(index: int, query_req: QueryRequest) -> None:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, self._pipeline.analyze, query_req
                )
                results[index] = result
            except Exception as exc:
                errors.append({
                    "index": index,
                    "query": query_req.query[:200],
                    "error": str(exc)[:500],
                })

        tasks = [
            run_query(i, qr) for i, qr in enumerate(batch.queries)
        ]
        await asyncio.gather(*tasks)

        completed_results = [r for r in results if r is not None]
        total_latency = (time.time() - start_time) * 1000

        return BatchQueryResponse(
            batch_id=batch_id,
            total_queries=len(batch.queries),
            completed=len(completed_results),
            failed=len(errors),
            results=completed_results,
            errors=errors,
            total_latency_ms=round(total_latency, 2),
        )


# =============================================================================
# JURISDICTION COMPARISON ENGINE
# =============================================================================

class JurisdictionComparisonRequest(BaseModel):
    """Request to compare treatment of a topic across jurisdictions."""
    topic: str = Field(..., min_length=1, max_length=500)
    jurisdictions: List[str] = Field(
        default=["federal", "texas"],
        description="Jurisdictions to compare",
    )
    max_results_per_jurisdiction: int = Field(default=5, ge=1, le=20)


class JurisdictionComparisonEntry(BaseModel):
    """Comparison entry for a single jurisdiction."""
    jurisdiction: str
    doctrines_found: int
    key_statutes: List[str] = Field(default_factory=list)
    elements_summary: List[str] = Field(default_factory=list)
    defenses_available: List[str] = Field(default_factory=list)
    remedies: List[str] = Field(default_factory=list)
    leading_cases: List[str] = Field(default_factory=list)
    notes: str = ""


class JurisdictionComparisonResponse(BaseModel):
    """Response from jurisdiction comparison."""
    topic: str
    jurisdictions_compared: List[str]
    entries: List[JurisdictionComparisonEntry] = Field(default_factory=list)
    key_differences: List[str] = Field(default_factory=list)
    timestamp: str


class JurisdictionComparator:
    """
    Compare how different jurisdictions handle the same criminal law topic.
    Identifies key differences in elements, penalties, and defenses.
    """

    def __init__(self, cache: DoctrineCacheManager, search_engine: ChromaSearchEngine) -> None:
        self._cache = cache
        self._search = search_engine

    def compare(self, request: JurisdictionComparisonRequest) -> JurisdictionComparisonResponse:
        """Compare a topic across jurisdictions."""
        entries: List[JurisdictionComparisonEntry] = []
        all_statutes: Dict[str, Set[str]] = defaultdict(set)
        all_defenses: Dict[str, Set[str]] = defaultdict(set)

        for jur in request.jurisdictions:
            # Search for topic within this jurisdiction
            search_query = f"{request.topic} {jur}"
            results = self._search.search(
                query=search_query,
                max_results=request.max_results_per_jurisdiction,
                jurisdiction_filter=jur,
            )

            # Also look in the doctrine cache
            cache_results = self._cache.get_by_jurisdiction(jur)
            topic_lower = request.topic.lower()
            matched_doctrines = [
                d for d in cache_results
                if topic_lower in d.topic.lower() or topic_lower in d.summary.lower()
            ]

            # Merge data
            all_statutes_list: List[str] = []
            all_elements: List[str] = []
            all_defenses_list: List[str] = []
            all_remedies: List[str] = []
            all_cases: List[str] = []

            for d in matched_doctrines[:request.max_results_per_jurisdiction]:
                all_statutes_list.extend(d.key_statutes)
                all_elements.extend(d.elements)
                all_defenses_list.extend(d.defenses)
                all_remedies.extend(d.remedies)
                all_cases.extend(d.leading_cases)

            # Deduplicate
            unique_statutes = list(dict.fromkeys(all_statutes_list))
            unique_elements = list(dict.fromkeys(all_elements))
            unique_defenses = list(dict.fromkeys(all_defenses_list))
            unique_remedies = list(dict.fromkeys(all_remedies))
            unique_cases = list(dict.fromkeys(all_cases))

            all_statutes[jur] = set(unique_statutes)
            all_defenses[jur] = set(unique_defenses)

            entry = JurisdictionComparisonEntry(
                jurisdiction=jur,
                doctrines_found=len(matched_doctrines),
                key_statutes=unique_statutes[:10],
                elements_summary=unique_elements[:10],
                defenses_available=unique_defenses[:10],
                remedies=unique_remedies[:10],
                leading_cases=unique_cases[:10],
            )
            entries.append(entry)

        # Identify key differences
        differences = self._find_differences(request.jurisdictions, all_statutes, all_defenses)

        return JurisdictionComparisonResponse(
            topic=request.topic,
            jurisdictions_compared=request.jurisdictions,
            entries=entries,
            key_differences=differences,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def _find_differences(
        jurisdictions: List[str],
        statutes: Dict[str, Set[str]],
        defenses: Dict[str, Set[str]],
    ) -> List[str]:
        """Identify notable differences between jurisdictions."""
        differences: List[str] = []

        if len(jurisdictions) >= 2:
            j1, j2 = jurisdictions[0], jurisdictions[1]
            s1 = statutes.get(j1, set())
            s2 = statutes.get(j2, set())
            d1 = defenses.get(j1, set())
            d2 = defenses.get(j2, set())

            only_s1 = s1 - s2
            only_s2 = s2 - s1
            only_d1 = d1 - d2
            only_d2 = d2 - d1

            if only_s1:
                differences.append(
                    f"Statutes unique to {j1}: {', '.join(list(only_s1)[:3])}"
                )
            if only_s2:
                differences.append(
                    f"Statutes unique to {j2}: {', '.join(list(only_s2)[:3])}"
                )
            if only_d1:
                differences.append(
                    f"Defenses unique to {j1}: {', '.join(list(only_d1)[:3])}"
                )
            if only_d2:
                differences.append(
                    f"Defenses unique to {j2}: {', '.join(list(only_d2)[:3])}"
                )

        return differences


# =============================================================================
# SENTENCING CALCULATOR
# =============================================================================

class SentencingInput(BaseModel):
    """Input for sentencing calculation."""
    offense: str = Field(..., description="Offense description or category")
    jurisdiction: str = Field(default="texas", description="Jurisdiction: texas or federal")
    felony_degree: Optional[str] = Field(
        default=None,
        description="Texas: capital, first, second, third, state_jail. Federal: class_a-e",
    )
    prior_convictions: int = Field(default=0, ge=0, description="Number of prior felony convictions")
    enhancement: bool = Field(default=False, description="Whether enhancement applies")
    deadly_weapon: bool = Field(default=False, description="Deadly weapon finding")
    drug_quantity_grams: Optional[float] = Field(default=None, description="Drug quantity in grams")
    drug_penalty_group: Optional[int] = Field(default=None, ge=1, le=4, description="Texas penalty group 1-4")


class SentencingRange(BaseModel):
    """Calculated sentencing range."""
    minimum: str
    maximum: str
    fine_maximum: str
    parole_eligibility: str
    probation_eligible: bool
    notes: List[str] = Field(default_factory=list)


class SentencingOutput(BaseModel):
    """Sentencing calculation output."""
    offense: str
    jurisdiction: str
    classification: str
    base_range: SentencingRange
    enhanced_range: Optional[SentencingRange] = None
    applicable_statutes: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    timestamp: str


class SentencingCalculator:
    """
    Calculate sentencing ranges for Texas and federal criminal offenses.
    Uses statutory ranges and enhancement provisions.
    """

    TEXAS_RANGES: Dict[str, Dict[str, Any]] = {
        "capital": {
            "min": "Life without parole",
            "max": "Death",
            "fine": "$0",
            "parole": "Not eligible",
            "probation": False,
            "notes": ["Bifurcated trial required", "Automatic appeal to Court of Criminal Appeals"],
        },
        "first": {
            "min": "5 years",
            "max": "99 years or life",
            "fine": "$10,000",
            "parole": "50% flat time if 3g offense",
            "probation": True,
            "notes": ["3g offenses require minimum 50% flat time before parole eligibility"],
        },
        "second": {
            "min": "2 years",
            "max": "20 years",
            "fine": "$10,000",
            "parole": "25% or actual time served",
            "probation": True,
            "notes": [],
        },
        "third": {
            "min": "2 years",
            "max": "10 years",
            "fine": "$10,000",
            "parole": "25% or actual time served",
            "probation": True,
            "notes": [],
        },
        "state_jail": {
            "min": "180 days",
            "max": "2 years",
            "fine": "$10,000",
            "parole": "Day-for-day, no good conduct time",
            "probation": True,
            "notes": ["Served in state jail facility, not TDCJ prison"],
        },
        "class_a_misdemeanor": {
            "min": "0 days",
            "max": "1 year",
            "fine": "$4,000",
            "parole": "N/A",
            "probation": True,
            "notes": ["County jail, not state prison"],
        },
        "class_b_misdemeanor": {
            "min": "0 days",
            "max": "180 days",
            "fine": "$2,000",
            "parole": "N/A",
            "probation": True,
            "notes": [],
        },
        "class_c_misdemeanor": {
            "min": "N/A",
            "max": "Fine only",
            "fine": "$500",
            "parole": "N/A",
            "probation": False,
            "notes": ["No jail time", "Typically handled in municipal or JP court"],
        },
    }

    TEXAS_ENHANCEMENT: Dict[str, str] = {
        "state_jail": "third",
        "third": "second",
        "second": "first",
        "first": "first",  # Enhanced first = 15-99 years or life
    }

    FEDERAL_DRUG_MANDATORY_MINS: Dict[str, Dict[str, Any]] = {
        "schedule_I_II_low": {
            "threshold_grams": {"powder_cocaine": 500, "crack_cocaine": 28, "heroin": 100, "methamphetamine": 5, "fentanyl": 40},
            "first_offense": "5 years",
            "second_offense": "10 years",
        },
        "schedule_I_II_high": {
            "threshold_grams": {"powder_cocaine": 5000, "crack_cocaine": 280, "heroin": 1000, "methamphetamine": 50, "fentanyl": 400},
            "first_offense": "10 years",
            "second_offense": "20 years",
        },
    }

    def calculate(self, sentencing_input: SentencingInput) -> SentencingOutput:
        """Calculate sentencing range for an offense."""
        warnings: List[str] = []
        applicable_statutes: List[str] = []

        if sentencing_input.jurisdiction == "texas":
            return self._calculate_texas(sentencing_input, warnings, applicable_statutes)
        elif sentencing_input.jurisdiction == "federal":
            return self._calculate_federal(sentencing_input, warnings, applicable_statutes)
        else:
            warnings.append(f"Unknown jurisdiction: {sentencing_input.jurisdiction}")
            return SentencingOutput(
                offense=sentencing_input.offense,
                jurisdiction=sentencing_input.jurisdiction,
                classification="unknown",
                base_range=SentencingRange(
                    minimum="Unknown",
                    maximum="Unknown",
                    fine_maximum="Unknown",
                    parole_eligibility="Unknown",
                    probation_eligible=False,
                ),
                warnings=warnings,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def _calculate_texas(
        self,
        inp: SentencingInput,
        warnings: List[str],
        statutes: List[str],
    ) -> SentencingOutput:
        """Calculate Texas sentencing range."""
        degree = inp.felony_degree or "second"
        classification = degree
        statutes.append("Texas Penal Code Chapter 12")

        base_info = self.TEXAS_RANGES.get(degree)
        if base_info is None:
            warnings.append(f"Unknown Texas offense level: {degree}")
            base_info = self.TEXAS_RANGES["second"]

        base_notes = list(base_info["notes"])

        if inp.deadly_weapon:
            base_notes.append("Deadly weapon finding: minimum 50% flat time before parole")
            statutes.append("Texas CCP Article 42A.054")

        base_range = SentencingRange(
            minimum=base_info["min"],
            maximum=base_info["max"],
            fine_maximum=base_info["fine"],
            parole_eligibility=base_info["parole"],
            probation_eligible=base_info["probation"],
            notes=base_notes,
        )

        enhanced_range = None
        if inp.enhancement or inp.prior_convictions >= 2:
            enhanced_degree = self.TEXAS_ENHANCEMENT.get(degree, degree)
            enhanced_info = self.TEXAS_RANGES.get(enhanced_degree, base_info)
            statutes.append("Texas Penal Code Section 12.42")

            enhanced_notes = list(enhanced_info["notes"])
            if inp.prior_convictions >= 2:
                enhanced_notes.append(
                    f"Habitual offender: {inp.prior_convictions} prior convictions"
                )
                if degree in ("first", "second"):
                    enhanced_notes.append("Habitual: 25-99 years or life")

            enhanced_range = SentencingRange(
                minimum=enhanced_info["min"],
                maximum=enhanced_info["max"],
                fine_maximum=enhanced_info["fine"],
                parole_eligibility=enhanced_info["parole"],
                probation_eligible=False,
                notes=enhanced_notes,
            )
            classification = f"{degree} (enhanced to {enhanced_degree})"

        return SentencingOutput(
            offense=inp.offense,
            jurisdiction="texas",
            classification=classification,
            base_range=base_range,
            enhanced_range=enhanced_range,
            applicable_statutes=statutes,
            warnings=warnings,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _calculate_federal(
        self,
        inp: SentencingInput,
        warnings: List[str],
        statutes: List[str],
    ) -> SentencingOutput:
        """Calculate federal sentencing range (simplified guidelines)."""
        statutes.append("18 USC 3553(a)")
        statutes.append("US Sentencing Guidelines Manual")

        if inp.drug_quantity_grams is not None and inp.drug_penalty_group:
            return self._calculate_federal_drug(inp, warnings, statutes)

        degree = inp.felony_degree or "class_c"
        classification = f"Federal {degree.replace('_', ' ').title()}"

        federal_ranges: Dict[str, Dict[str, Any]] = {
            "class_a": {"min": "More than 10 years", "max": "Life or death", "fine": "$250,000"},
            "class_b": {"min": "5 years", "max": "Less than 25 years", "fine": "$250,000"},
            "class_c": {"min": "1 year", "max": "Less than 12 years", "fine": "$250,000"},
            "class_d": {"min": "Less than 6 years", "max": "Less than 6 years", "fine": "$250,000"},
            "class_e": {"min": "More than 1 year", "max": "Less than 5 years", "fine": "$250,000"},
        }

        range_info = federal_ranges.get(degree, federal_ranges["class_c"])
        warnings.append("Federal sentencing is guidelines-based; this is a statutory maximum range")

        base_range = SentencingRange(
            minimum=range_info["min"],
            maximum=range_info["max"],
            fine_maximum=range_info["fine"],
            parole_eligibility="No federal parole — 85% time served required",
            probation_eligible=False,
            notes=["Federal sentencing requires guidelines calculation", "No parole in federal system since 1987"],
        )

        return SentencingOutput(
            offense=inp.offense,
            jurisdiction="federal",
            classification=classification,
            base_range=base_range,
            applicable_statutes=statutes,
            warnings=warnings,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _calculate_federal_drug(
        self,
        inp: SentencingInput,
        warnings: List[str],
        statutes: List[str],
    ) -> SentencingOutput:
        """Calculate federal drug sentencing range."""
        statutes.extend(["21 USC 841", "21 USC 846"])
        quantity = inp.drug_quantity_grams or 0.0
        classification = f"Federal drug offense (PG{inp.drug_penalty_group}, {quantity}g)"

        notes: List[str] = [
            "Federal drug sentencing depends on substance type, quantity, and criminal history",
            "Mandatory minimums may apply based on quantity thresholds",
            "Safety valve (18 USC 3553(f)) may allow below mandatory minimum for minimal participants",
        ]

        if quantity >= 5000:
            minimum = "10 years mandatory minimum (first offense)"
            maximum = "Life imprisonment"
            notes.append("High-quantity threshold: 10-year mandatory minimum")
        elif quantity >= 500:
            minimum = "5 years mandatory minimum (first offense)"
            maximum = "40 years"
            notes.append("Low-quantity threshold: 5-year mandatory minimum")
        elif quantity >= 100:
            minimum = "Up to guidelines calculation"
            maximum = "20 years"
        else:
            minimum = "Up to guidelines calculation"
            maximum = "Up to 20 years"

        if inp.prior_convictions > 0:
            notes.append(f"Prior convictions ({inp.prior_convictions}) may double mandatory minimums")
            warnings.append("Prior drug felonies trigger enhanced mandatory minimums under 21 USC 851")

        base_range = SentencingRange(
            minimum=minimum,
            maximum=maximum,
            fine_maximum="$10,000,000 (individual) / $50,000,000 (organization)",
            parole_eligibility="No federal parole — 85% time served required",
            probation_eligible=False,
            notes=notes,
        )

        return SentencingOutput(
            offense=inp.offense,
            jurisdiction="federal",
            classification=classification,
            base_range=base_range,
            applicable_statutes=statutes,
            warnings=warnings,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    """
    Token-bucket rate limiter for API endpoints.
    Thread-safe with configurable requests per minute and burst limit.
    """

    def __init__(self, requests_per_minute: int = 120, burst_limit: int = 20) -> None:
        self._rpm = requests_per_minute
        self._burst = burst_limit
        self._tokens: float = float(burst_limit)
        self._max_tokens: float = float(burst_limit)
        self._refill_rate: float = requests_per_minute / 60.0  # tokens per second
        self._last_refill: float = time.time()
        self._lock = threading.Lock()
        self._total_requests: int = 0
        self._total_rejected: int = 0

    def allow_request(self) -> bool:
        """Check if a request is allowed under rate limits."""
        with self._lock:
            now = time.time()
            elapsed = now - self._last_refill
            self._tokens = min(
                self._max_tokens,
                self._tokens + elapsed * self._refill_rate,
            )
            self._last_refill = now
            self._total_requests += 1

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            else:
                self._total_rejected += 1
                return False

    def get_stats(self) -> Dict[str, Any]:
        """Return rate limiter statistics."""
        return {
            "requests_per_minute_limit": self._rpm,
            "burst_limit": self._burst,
            "current_tokens": round(self._tokens, 2),
            "total_requests": self._total_requests,
            "total_rejected": self._total_rejected,
            "rejection_rate": (
                round(self._total_rejected / self._total_requests, 4)
                if self._total_requests > 0 else 0.0
            ),
        }


# =============================================================================
# CASE LAW CROSS-REFERENCE ENGINE
# =============================================================================

class CaseLawEntry(BaseModel):
    """A case law reference entry."""
    case_name: str
    citation: str
    year: int
    court: str
    holding: str
    relevance: List[str] = Field(default_factory=list)
    overruled: bool = False
    overruled_by: Optional[str] = None


class CaseLawIndex:
    """
    Cross-reference index of leading criminal law cases.
    Enables lookup by topic, holding, or citation.
    """

    def __init__(self) -> None:
        self._cases: Dict[str, CaseLawEntry] = {}
        self._by_topic: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.Lock()
        self._load_cases()

    def _load_cases(self) -> None:
        """Load leading criminal law cases into the index."""
        cases = [
            CaseLawEntry(
                case_name="Miranda v Arizona",
                citation="384 U.S. 436 (1966)",
                year=1966,
                court="US Supreme Court",
                holding="Custodial interrogation requires warnings of right to silence and counsel",
                relevance=["miranda_rights", "fifth_amendment", "custodial_interrogation"],
            ),
            CaseLawEntry(
                case_name="Mapp v Ohio",
                citation="367 U.S. 643 (1961)",
                year=1961,
                court="US Supreme Court",
                holding="Exclusionary rule applies to states through Fourteenth Amendment",
                relevance=["exclusionary_rule", "fourth_amendment", "search_seizure"],
            ),
            CaseLawEntry(
                case_name="Gideon v Wainwright",
                citation="372 U.S. 335 (1963)",
                year=1963,
                court="US Supreme Court",
                holding="Right to appointed counsel for indigent felony defendants",
                relevance=["sixth_amendment", "right_to_counsel", "indigent_defense"],
            ),
            CaseLawEntry(
                case_name="Terry v Ohio",
                citation="392 U.S. 1 (1968)",
                year=1968,
                court="US Supreme Court",
                holding="Officers may stop and frisk on reasonable suspicion of criminal activity",
                relevance=["terry_stop", "fourth_amendment", "reasonable_suspicion", "stop_and_frisk"],
            ),
            CaseLawEntry(
                case_name="Brady v Maryland",
                citation="373 U.S. 83 (1963)",
                year=1963,
                court="US Supreme Court",
                holding="Prosecution must disclose material exculpatory evidence to defense",
                relevance=["discovery", "due_process", "exculpatory_evidence", "prosecutorial_duty"],
            ),
            CaseLawEntry(
                case_name="Strickland v Washington",
                citation="466 U.S. 668 (1984)",
                year=1984,
                court="US Supreme Court",
                holding="Two-prong test for ineffective assistance: deficient performance + prejudice",
                relevance=["ineffective_assistance", "sixth_amendment", "right_to_counsel"],
            ),
            CaseLawEntry(
                case_name="Katz v United States",
                citation="389 U.S. 347 (1967)",
                year=1967,
                court="US Supreme Court",
                holding="Fourth Amendment protects reasonable expectations of privacy, not just places",
                relevance=["fourth_amendment", "privacy", "electronic_surveillance", "search_definition"],
            ),
            CaseLawEntry(
                case_name="Batson v Kentucky",
                citation="476 U.S. 79 (1986)",
                year=1986,
                court="US Supreme Court",
                holding="Racially discriminatory use of peremptory challenges violates Equal Protection",
                relevance=["jury_selection", "equal_protection", "peremptory_challenge", "racial_discrimination"],
            ),
            CaseLawEntry(
                case_name="Furman v Georgia",
                citation="408 U.S. 238 (1972)",
                year=1972,
                court="US Supreme Court",
                holding="Arbitrary and capricious death penalty application unconstitutional",
                relevance=["death_penalty", "eighth_amendment", "capital_punishment"],
            ),
            CaseLawEntry(
                case_name="Gregg v Georgia",
                citation="428 U.S. 153 (1976)",
                year=1976,
                court="US Supreme Court",
                holding="Death penalty with guided discretion is constitutional",
                relevance=["death_penalty", "eighth_amendment", "capital_punishment", "guided_discretion"],
            ),
            CaseLawEntry(
                case_name="Riley v California",
                citation="573 U.S. 373 (2014)",
                year=2014,
                court="US Supreme Court",
                holding="Police must obtain warrant before searching cell phone incident to arrest",
                relevance=["cell_phone_search", "fourth_amendment", "search_incident_to_arrest", "digital_privacy"],
            ),
            CaseLawEntry(
                case_name="Carpenter v United States",
                citation="585 U.S. 296 (2018)",
                year=2018,
                court="US Supreme Court",
                holding="Government access to historical cell phone location data is a Fourth Amendment search",
                relevance=["cell_site_location", "fourth_amendment", "digital_privacy", "third_party_doctrine"],
            ),
            CaseLawEntry(
                case_name="United States v Booker",
                citation="543 U.S. 220 (2005)",
                year=2005,
                court="US Supreme Court",
                holding="Federal sentencing guidelines are advisory, not mandatory",
                relevance=["sentencing_guidelines", "sixth_amendment", "jury_trial", "federal_sentencing"],
            ),
            CaseLawEntry(
                case_name="Roper v Simmons",
                citation="543 U.S. 551 (2005)",
                year=2005,
                court="US Supreme Court",
                holding="Death penalty for offenders under 18 at time of crime is unconstitutional",
                relevance=["juvenile_justice", "death_penalty", "eighth_amendment", "evolving_standards"],
            ),
            CaseLawEntry(
                case_name="Miller v Alabama",
                citation="567 U.S. 460 (2012)",
                year=2012,
                court="US Supreme Court",
                holding="Mandatory life without parole for juvenile homicide offenders unconstitutional",
                relevance=["juvenile_justice", "eighth_amendment", "lwop", "mandatory_sentencing"],
            ),
            CaseLawEntry(
                case_name="District of Columbia v Heller",
                citation="554 U.S. 570 (2008)",
                year=2008,
                court="US Supreme Court",
                holding="Second Amendment protects individual right to possess firearms for self-defense",
                relevance=["second_amendment", "firearms", "individual_right", "self_defense"],
            ),
            CaseLawEntry(
                case_name="New York State Rifle v Bruen",
                citation="597 U.S. 1 (2022)",
                year=2022,
                court="US Supreme Court",
                holding="Firearms regulations must be consistent with historical tradition of regulation",
                relevance=["second_amendment", "firearms", "text_history_tradition", "concealed_carry"],
            ),
            CaseLawEntry(
                case_name="Padilla v Kentucky",
                citation="559 U.S. 356 (2010)",
                year=2010,
                court="US Supreme Court",
                holding="Defense counsel must advise noncitizen clients of deportation risk from guilty plea",
                relevance=["immigration", "plea_bargaining", "ineffective_assistance", "deportation"],
            ),
            CaseLawEntry(
                case_name="Jackson v Virginia",
                citation="443 U.S. 307 (1979)",
                year=1979,
                court="US Supreme Court",
                holding="Sufficiency of evidence standard: rational trier of fact could find elements beyond reasonable doubt",
                relevance=["sufficiency_of_evidence", "due_process", "beyond_reasonable_doubt", "appellate_review"],
            ),
            CaseLawEntry(
                case_name="Crawford v Washington",
                citation="541 U.S. 36 (2004)",
                year=2004,
                court="US Supreme Court",
                holding="Testimonial hearsay inadmissible unless declarant unavailable and prior cross-examination",
                relevance=["confrontation_clause", "sixth_amendment", "testimonial_hearsay", "cross_examination"],
            ),
        ]

        for case in cases:
            key = case.case_name.lower().replace(" ", "_")
            self._cases[key] = case
            for topic in case.relevance:
                self._by_topic[topic].append(key)

        logger.info(f"Case law index loaded: {len(self._cases)} cases, {len(self._by_topic)} topics")

    def search_by_topic(self, topic: str, max_results: int = 10) -> List[CaseLawEntry]:
        """Find cases relevant to a topic."""
        topic_lower = topic.lower().replace(" ", "_")
        results: List[CaseLawEntry] = []

        # Direct topic match
        with self._lock:
            direct_keys = self._by_topic.get(topic_lower, [])
            for key in direct_keys:
                case = self._cases.get(key)
                if case:
                    results.append(case)

        # Substring match if needed
        if len(results) < max_results:
            with self._lock:
                for key, case in self._cases.items():
                    if case in results:
                        continue
                    if (topic_lower in case.holding.lower() or
                            topic_lower in case.case_name.lower() or
                            any(topic_lower in r for r in case.relevance)):
                        results.append(case)
                    if len(results) >= max_results:
                        break

        return results[:max_results]

    def get_case(self, case_name: str) -> Optional[CaseLawEntry]:
        """Get a specific case by name."""
        key = case_name.lower().replace(" ", "_")
        with self._lock:
            return self._cases.get(key)

    def get_all_topics(self) -> List[str]:
        """Return all indexed topics."""
        with self._lock:
            return sorted(self._by_topic.keys())

    @property
    def size(self) -> int:
        """Number of cases in the index."""
        with self._lock:
            return len(self._cases)


# =============================================================================
# STATUTE LOOKUP SYSTEM
# =============================================================================

class StatuteEntry(BaseModel):
    """A statutory reference entry."""
    code: str
    section: str
    title: str
    summary: str
    jurisdiction: str
    penalty_range: Optional[str] = None
    related_sections: List[str] = Field(default_factory=list)


class StatuteLookup:
    """
    Quick reference lookup for commonly cited criminal statutes.
    Provides code section, title, summary, and cross-references.
    """

    def __init__(self) -> None:
        self._statutes: Dict[str, StatuteEntry] = {}
        self._load_statutes()

    def _load_statutes(self) -> None:
        """Load common criminal statutes."""
        statutes = [
            StatuteEntry(
                code="18 USC", section="1111", title="Murder",
                summary="Federal first and second degree murder; malice aforethought",
                jurisdiction="federal",
                penalty_range="Death or life (1st degree), any term of years to life (2nd degree)",
                related_sections=["18 USC 1112", "18 USC 1113", "18 USC 3591"],
            ),
            StatuteEntry(
                code="18 USC", section="1112", title="Manslaughter",
                summary="Voluntary manslaughter (up to 15 years) and involuntary manslaughter (up to 8 years)",
                jurisdiction="federal",
                penalty_range="Up to 15 years (voluntary), up to 8 years (involuntary)",
                related_sections=["18 USC 1111"],
            ),
            StatuteEntry(
                code="18 USC", section="922(g)", title="Prohibited Persons — Firearms",
                summary="Prohibits firearm possession by felons, fugitives, drug users, and other categories",
                jurisdiction="federal",
                penalty_range="Up to 15 years (enhanced under ACCA: 15-year mandatory minimum)",
                related_sections=["18 USC 924(c)", "18 USC 921", "18 USC 924(e)"],
            ),
            StatuteEntry(
                code="18 USC", section="924(c)", title="Use of Firearm During Crime",
                summary="Mandatory consecutive sentences for using firearm during crime of violence or drug trafficking",
                jurisdiction="federal",
                penalty_range="5 years (possess), 7 years (brandish), 10 years (discharge), consecutive",
                related_sections=["18 USC 922(g)", "18 USC 924(e)"],
            ),
            StatuteEntry(
                code="18 USC", section="1341", title="Mail Fraud",
                summary="Scheme to defraud using postal service; broad federal fraud statute",
                jurisdiction="federal",
                penalty_range="Up to 20 years (30 years if financial institution victim)",
                related_sections=["18 USC 1343", "18 USC 1344", "18 USC 1346"],
            ),
            StatuteEntry(
                code="18 USC", section="1343", title="Wire Fraud",
                summary="Scheme to defraud using wire communications; parallel to mail fraud",
                jurisdiction="federal",
                penalty_range="Up to 20 years (30 years if financial institution victim)",
                related_sections=["18 USC 1341", "18 USC 1344"],
            ),
            StatuteEntry(
                code="18 USC", section="1956", title="Money Laundering",
                summary="Financial transactions with proceeds of unlawful activity",
                jurisdiction="federal",
                penalty_range="Up to 20 years, fine up to $500,000 or 2x amount laundered",
                related_sections=["18 USC 1957", "31 USC 5324"],
            ),
            StatuteEntry(
                code="18 USC", section="1962", title="RICO — Prohibited Activities",
                summary="Racketeering through pattern of criminal activity connected to enterprise",
                jurisdiction="federal",
                penalty_range="Up to 20 years (life if predicate carries life), mandatory forfeiture",
                related_sections=["18 USC 1961", "18 USC 1963", "18 USC 1964"],
            ),
            StatuteEntry(
                code="21 USC", section="841", title="Drug Manufacturing and Distribution",
                summary="Prohibited acts regarding controlled substances — manufacture, distribute, dispense",
                jurisdiction="federal",
                penalty_range="Varies by substance and quantity; mandatory minimums apply",
                related_sections=["21 USC 844", "21 USC 846", "21 USC 851"],
            ),
            StatuteEntry(
                code="TPC", section="19.02", title="Murder",
                summary="Texas murder: intentionally/knowingly causing death, or intending SBI causing death, or felony murder",
                jurisdiction="texas",
                penalty_range="First degree felony (5-99 years or life), second degree if sudden passion",
                related_sections=["TPC 19.03", "TPC 19.04", "TPC 19.05"],
            ),
            StatuteEntry(
                code="TPC", section="19.03", title="Capital Murder",
                summary="Texas capital murder: murder with enumerated aggravating factors",
                jurisdiction="texas",
                penalty_range="Death or life without parole",
                related_sections=["TPC 19.02", "TPC 12.31"],
            ),
            StatuteEntry(
                code="TPC", section="22.01", title="Assault",
                summary="Texas assault: causing bodily injury, threatening imminent bodily injury, or offensive contact",
                jurisdiction="texas",
                penalty_range="Class A misdemeanor (up to 1 year), enhanced for family violence",
                related_sections=["TPC 22.02", "TPC 25.11"],
            ),
            StatuteEntry(
                code="TPC", section="22.02", title="Aggravated Assault",
                summary="Texas aggravated assault: SBI or deadly weapon during assault",
                jurisdiction="texas",
                penalty_range="Second degree felony (2-20 years), first degree for certain victims",
                related_sections=["TPC 22.01", "TPC 1.07(a)(46)"],
            ),
            StatuteEntry(
                code="TPC", section="30.02", title="Burglary",
                summary="Texas burglary: entering building/habitation without consent to commit felony, theft, or assault",
                jurisdiction="texas",
                penalty_range="SJF (building), 2nd degree (habitation), 1st degree (habitation + felony other than theft)",
                related_sections=["TPC 31.03", "TPC 29.02"],
            ),
            StatuteEntry(
                code="TPC", section="31.03", title="Theft",
                summary="Texas theft: unlawful appropriation of property with intent to deprive",
                jurisdiction="texas",
                penalty_range="Class C misdemeanor (<$100) through first degree felony ($300K+)",
                related_sections=["TPC 31.04", "TPC 32.31"],
            ),
        ]

        for statute in statutes:
            key = f"{statute.code}_{statute.section}".lower().replace(" ", "_")
            self._statutes[key] = statute

        logger.info(f"Statute lookup loaded: {len(self._statutes)} statutes")

    def lookup(self, code: str, section: str) -> Optional[StatuteEntry]:
        """Look up a statute by code and section."""
        key = f"{code}_{section}".lower().replace(" ", "_")
        return self._statutes.get(key)

    def search(self, query: str, max_results: int = 10) -> List[StatuteEntry]:
        """Search statutes by keyword."""
        query_lower = query.lower()
        results: List[StatuteEntry] = []
        for statute in self._statutes.values():
            if (query_lower in statute.title.lower() or
                    query_lower in statute.summary.lower() or
                    query_lower in statute.section.lower()):
                results.append(statute)
            if len(results) >= max_results:
                break
        return results

    @property
    def size(self) -> int:
        return len(self._statutes)


# =============================================================================
# ADDITIONAL API ROUTES (Extended)
# =============================================================================

@app.post("/analyze/batch", response_model=BatchQueryResponse)
async def batch_analyze(request: BatchQueryRequest) -> BatchQueryResponse:
    """Batch analysis endpoint — process multiple queries at once."""
    pipe = get_pipeline()
    analyzer = BatchAnalyzer(pipe)
    if request.parallel:
        return await analyzer.execute_parallel(request)
    else:
        return analyzer.execute_sequential(request)


@app.post("/compare/jurisdictions", response_model=JurisdictionComparisonResponse)
async def compare_jurisdictions(request: JurisdictionComparisonRequest) -> JurisdictionComparisonResponse:
    """Compare treatment of a criminal law topic across jurisdictions."""
    pipe = get_pipeline()
    comparator = JurisdictionComparator(pipe.doctrine_cache, pipe.search_engine)
    return comparator.compare(request)


@app.post("/sentencing/calculate", response_model=SentencingOutput)
async def calculate_sentencing(request: SentencingInput) -> SentencingOutput:
    """Calculate sentencing ranges for criminal offenses."""
    calculator = SentencingCalculator()
    return calculator.calculate(request)


@app.get("/cases", response_model=Dict[str, Any])
async def list_cases(
    topic: Optional[str] = Query(None, description="Filter by topic"),
    max_results: int = Query(20, ge=1, le=100),
) -> Dict[str, Any]:
    """Case law cross-reference lookup."""
    index = CaseLawIndex()
    if topic:
        cases = index.search_by_topic(topic, max_results)
    else:
        cases = [index.get_case(key) for key in list(index._cases.keys())[:max_results]]
        cases = [c for c in cases if c is not None]
    return {
        "total": len(cases),
        "cases": [c.model_dump() for c in cases],
        "topics": index.get_all_topics(),
    }


@app.get("/statutes", response_model=Dict[str, Any])
async def lookup_statutes(
    q: Optional[str] = Query(None, description="Search query"),
    code: Optional[str] = Query(None, description="Statute code (e.g., '18 USC')"),
    section: Optional[str] = Query(None, description="Section number"),
) -> Dict[str, Any]:
    """Statute lookup endpoint."""
    lookup = StatuteLookup()

    if code and section:
        result = lookup.lookup(code, section)
        if result:
            return {"found": True, "statute": result.model_dump()}
        raise HTTPException(status_code=404, detail=f"Statute not found: {code} {section}")

    if q:
        results = lookup.search(q)
        return {"total": len(results), "statutes": [s.model_dump() for s in results]}

    # Return all
    all_statutes = lookup.search("", max_results=100)
    return {"total": len(all_statutes), "statutes": [s.model_dump() for s in all_statutes]}


@app.get("/rate-limit/stats", response_model=Dict[str, Any])
async def rate_limit_stats() -> Dict[str, Any]:
    """Rate limiter statistics."""
    rl_config = ENGINE_CONFIG.get("rate_limiting", {})
    rl = RateLimiter(
        requests_per_minute=rl_config.get("requests_per_minute", 120),
        burst_limit=rl_config.get("burst_limit", 20),
    )
    return rl.get_stats()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    """Launch the LG09 Criminal Law Engine."""
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on {ENGINE_HOST}:{ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host=ENGINE_HOST,
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
        workers=1,
    )


if __name__ == "__main__":
    main()
