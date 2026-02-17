"""
LM15 Water Rights Engine - Search Module
==========================================

TF-IDF powered search index for water rights doctrines, permits,
aquifer data, disposal well compliance, and water rights records.

Author: ECHO OMEGA PRIME Build System
Engine: LM15 v2.0.0
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class WaterRightType(str, Enum):
    SURFACE_WATER_APPROPRIATION = "surface_water_appropriation"
    GCD_PRODUCTION_PERMIT = "gcd_production_permit"
    GCD_EXPORT_PERMIT = "gcd_export_permit"
    INJECTION_WELL_H1 = "injection_well_h1"
    INJECTION_WELL_EOR = "injection_well_eor"
    TPDES_DISCHARGE = "tpdes_discharge"
    EDWARDS_AQUIFER = "edwards_aquifer"
    TEMPORARY_PERMIT = "temporary_permit"
    WATER_TRANSPORT = "water_transport"
    BED_AND_BANKS = "bed_and_banks"
    RECYCLING_FACILITY = "recycling_facility"
    BRACKISH_DESALINATION = "brackish_desalination"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    MINOR_VIOLATION = "minor_violation"
    MAJOR_VIOLATION = "major_violation"
    ENFORCEMENT_ACTION = "enforcement_action"
    PERMIT_SUSPENDED = "permit_suspended"
    PERMIT_REVOKED = "permit_revoked"
    UNDER_REVIEW = "under_review"
    NOT_ASSESSED = "not_assessed"


class SortField(str, Enum):
    RELEVANCE = "relevance"
    DATE_ISSUED = "date_issued"
    DATE_EXPIRES = "date_expires"
    OPERATOR_NAME = "operator_name"
    COUNTY = "county"
    PERMIT_NUMBER = "permit_number"
    COMPLIANCE_SCORE = "compliance_score"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SearchQuery:
    query_text: str
    right_type: Optional[WaterRightType] = None
    county: Optional[str] = None
    operator: Optional[str] = None
    aquifer: Optional[str] = None
    compliance_status: Optional[ComplianceStatus] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    sort_by: SortField = SortField.RELEVANCE
    max_results: int = 25
    offset: int = 0

    def compute_hash(self) -> str:
        content = json.dumps({
            "q": self.query_text, "type": self.right_type.value if self.right_type else None,
            "county": self.county, "operator": self.operator,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class SearchResult:
    result_id: str
    score: float
    record_type: str
    title: str
    summary: str
    county: str = ""
    operator: str = ""
    permit_number: str = ""
    aquifer: str = ""
    right_type: str = ""
    compliance_status: str = ""
    date_issued: str = ""
    date_expires: str = ""
    citation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "id": self.result_id, "type": self.record_type,
            "title": self.title, "score": self.score,
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


@dataclass
class SearchResponse:
    query_hash: str
    total_results: int
    returned: int
    offset: int
    results: list[SearchResult]
    facets: dict[str, dict[str, int]] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    determinism_hash: str = ""

    def compute_hash(self) -> str:
        content = json.dumps({
            "query_hash": self.query_hash,
            "total": self.total_results,
            "result_ids": [r.result_id for r in self.results],
        }, sort_keys=True)
        self.determinism_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.determinism_hash


# ---------------------------------------------------------------------------
# TF-IDF Search Index
# ---------------------------------------------------------------------------

class DoctrineSearchIndex:
    """TF-IDF based search index for doctrine blocks and water rights records."""

    def __init__(self) -> None:
        self._documents: dict[str, dict[str, Any]] = {}
        self._term_doc_freq: dict[str, int] = defaultdict(int)
        self._doc_term_freq: dict[str, dict[str, int]] = {}
        self._doc_lengths: dict[str, int] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._built = False
        logger.info("DoctrineSearchIndex initialized")

    def _tokenize(self, text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "above",
            "below", "between", "under", "and", "but", "or", "nor", "not",
            "so", "yet", "both", "each", "every", "all", "any", "few",
            "more", "most", "other", "some", "such", "no", "only", "own",
            "same", "than", "too", "very", "this", "that", "these", "those",
            "it", "its", "if", "then", "also", "about", "up", "out",
        }
        return [t for t in tokens if t not in stop_words and len(t) > 1]

    def add_document(self, doc_id: str, content: str, metadata: Optional[dict[str, Any]] = None) -> None:
        tokens = self._tokenize(content)
        term_freq: dict[str, int] = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        self._doc_term_freq[doc_id] = dict(term_freq)
        self._doc_lengths[doc_id] = len(tokens)
        self._documents[doc_id] = {
            "content": content,
            "metadata": metadata or {},
            "term_count": len(tokens),
            "unique_terms": len(term_freq),
        }
        for term in term_freq:
            self._term_doc_freq[term] += 1
        self._total_docs += 1
        self._built = False

    def build(self) -> None:
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        self._built = True
        logger.info(f"Search index built: {self._total_docs} docs, {len(self._term_doc_freq)} unique terms")

    def search(self, query: str, max_results: int = 25) -> list[tuple[str, float]]:
        if not self._built:
            self.build()
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        scores: dict[str, float] = defaultdict(float)
        for token in query_tokens:
            if token not in self._term_doc_freq:
                continue
            df = self._term_doc_freq[token]
            idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)
            for doc_id, term_freqs in self._doc_term_freq.items():
                tf = term_freqs.get(token, 0)
                if tf == 0:
                    continue
                doc_len = self._doc_lengths[doc_id]
                k1 = 1.5
                b = 0.75
                tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / max(self._avg_doc_length, 1.0)))
                scores[doc_id] += idf * tf_norm
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:max_results]

    def index_doctrine_cache(self, cache: list[Any]) -> int:
        count = 0
        for doctrine in cache:
            content = (
                f"{doctrine.title} {doctrine.summary} {doctrine.detailed_analysis} "
                f"{doctrine.citation} {' '.join(doctrine.key_provisions)} "
                f"{' '.join(doctrine.tags)} {doctrine.permian_basin_notes}"
            )
            metadata = {
                "doctrine_id": doctrine.doctrine_id,
                "category": doctrine.category.value,
                "authority": doctrine.authority_level.value,
                "risk": doctrine.risk_if_violated.value,
                "citation": doctrine.citation,
                "title": doctrine.title,
            }
            self.add_document(doctrine.doctrine_id, content, metadata)
            count += 1
        self.build()
        logger.info(f"Indexed {count} doctrines into search index")
        return count

    @property
    def document_count(self) -> int:
        return self._total_docs


# ---------------------------------------------------------------------------
# Water Rights Searcher
# ---------------------------------------------------------------------------

class WaterRightsSearcher:
    """High-level search interface for water rights records."""

    def __init__(self) -> None:
        self._index = DoctrineSearchIndex()
        self._records: dict[str, dict[str, Any]] = {}
        logger.info("WaterRightsSearcher initialized")

    def add_record(self, record: dict[str, Any]) -> str:
        record_id = record.get("record_id", str(uuid.uuid4()))
        searchable = " ".join(str(v) for v in record.values() if isinstance(v, str))
        self._index.add_document(record_id, searchable, record)
        self._records[record_id] = record
        return record_id

    def index_doctrines(self, cache: list[Any]) -> int:
        return self._index.index_doctrine_cache(cache)

    def search(self, query: SearchQuery) -> SearchResponse:
        import time
        start = time.monotonic()
        raw_results = self._index.search(query.query_text, max_results=query.max_results * 3)
        filtered: list[tuple[str, float]] = []
        for doc_id, score in raw_results:
            meta = self._index._documents.get(doc_id, {}).get("metadata", {})
            if query.county and meta.get("county", "").lower() != query.county.lower():
                record = self._records.get(doc_id, {})
                if record.get("county", "").lower() != query.county.lower():
                    continue
            if query.operator and query.operator.lower() not in meta.get("operator", "").lower():
                record = self._records.get(doc_id, {})
                if query.operator.lower() not in record.get("operator", "").lower():
                    continue
            if query.aquifer and query.aquifer.lower() not in meta.get("aquifer", "").lower():
                record = self._records.get(doc_id, {})
                if query.aquifer.lower() not in record.get("aquifer", "").lower():
                    continue
            filtered.append((doc_id, score))
        paginated = filtered[query.offset:query.offset + query.max_results]
        results: list[SearchResult] = []
        for doc_id, score in paginated:
            meta = self._index._documents.get(doc_id, {}).get("metadata", {})
            record = self._records.get(doc_id, {})
            sr = SearchResult(
                result_id=doc_id,
                score=round(score, 4),
                record_type=meta.get("category", record.get("record_type", "water_right")),
                title=meta.get("title", record.get("title", doc_id)),
                summary=meta.get("summary", record.get("summary", "")),
                county=meta.get("county", record.get("county", "")),
                operator=meta.get("operator", record.get("operator", "")),
                permit_number=meta.get("permit_number", record.get("permit_number", "")),
                aquifer=meta.get("aquifer", record.get("aquifer", "")),
                right_type=meta.get("right_type", record.get("right_type", "")),
                compliance_status=meta.get("compliance_status", record.get("compliance_status", "")),
                date_issued=meta.get("date_issued", record.get("date_issued", "")),
                date_expires=meta.get("date_expires", record.get("date_expires", "")),
                citation=meta.get("citation", record.get("citation", "")),
                metadata=meta,
            )
            sr.compute_hash()
            results.append(sr)
        elapsed = (time.monotonic() - start) * 1000
        facets = self._compute_facets(filtered)
        response = SearchResponse(
            query_hash=query.compute_hash(),
            total_results=len(filtered),
            returned=len(results),
            offset=query.offset,
            results=results,
            facets=facets,
            execution_time_ms=round(elapsed, 2),
        )
        response.compute_hash()
        logger.debug(f"Search '{query.query_text}': {len(filtered)} total, {len(results)} returned in {elapsed:.1f}ms")
        return response

    def _compute_facets(self, results: list[tuple[str, float]]) -> dict[str, dict[str, int]]:
        facets: dict[str, dict[str, int]] = {
            "category": defaultdict(int),
            "risk": defaultdict(int),
            "county": defaultdict(int),
        }
        for doc_id, _ in results:
            meta = self._index._documents.get(doc_id, {}).get("metadata", {})
            record = self._records.get(doc_id, {})
            cat = meta.get("category", record.get("category", "unknown"))
            risk = meta.get("risk", record.get("risk", "unknown"))
            county = meta.get("county", record.get("county", "unknown"))
            if cat:
                facets["category"][cat] += 1
            if risk:
                facets["risk"][risk] += 1
            if county:
                facets["county"][county] += 1
        return {k: dict(v) for k, v in facets.items()}


# ---------------------------------------------------------------------------
# Disposal Well Compliance Checker
# ---------------------------------------------------------------------------

class DisposalWellComplianceChecker:
    """Check disposal well compliance against RRC and EPA standards."""

    def __init__(self) -> None:
        self._wells: dict[str, dict[str, Any]] = {}
        logger.info("DisposalWellComplianceChecker initialized")

    def register_well(self, well_id: str, well_data: dict[str, Any]) -> None:
        self._wells[well_id] = well_data
        logger.debug(f"Registered disposal well: {well_id}")

    def check_compliance(self, well_id: str) -> dict[str, Any]:
        well = self._wells.get(well_id)
        if not well:
            return {"well_id": well_id, "status": "not_found", "score": 0}
        score = 100.0
        violations: list[dict[str, Any]] = []
        warnings: list[str] = []
        permit_exp = well.get("permit_expiration")
        if permit_exp:
            from datetime import datetime as dt
            try:
                exp = dt.strptime(permit_exp, "%Y-%m-%d")
                now = dt.now()
                if exp < now:
                    score -= 30
                    violations.append({"type": "expired_permit", "severity": "critical", "details": f"Permit expired {permit_exp}"})
                elif (exp - now).days < 90:
                    warnings.append(f"Permit expires in {(exp - now).days} days")
            except ValueError:
                warnings.append("Could not parse permit expiration date")
        mit_date = well.get("last_mit_date")
        if mit_date:
            from datetime import datetime as dt
            try:
                last_mit = dt.strptime(mit_date, "%Y-%m-%d")
                years_since = (dt.now() - last_mit).days / 365.25
                if years_since > 5.0:
                    score -= 25
                    violations.append({"type": "mit_overdue", "severity": "high", "details": f"MIT overdue: {years_since:.1f} years since last test"})
                elif years_since > 4.0:
                    warnings.append(f"MIT due within {(5.0 - years_since) * 12:.0f} months")
            except ValueError:
                warnings.append("Could not parse MIT date")
        if well.get("daily_volume_bbls", 0) > well.get("permitted_volume_bbls", float("inf")):
            score -= 20
            violations.append({"type": "volume_exceeded", "severity": "high", "details": "Daily injection volume exceeds permitted limit"})
        if well.get("injection_pressure_psi", 0) > well.get("max_permitted_pressure_psi", float("inf")):
            score -= 25
            violations.append({"type": "pressure_exceeded", "severity": "critical", "details": "Injection pressure exceeds permitted maximum"})
        if not well.get("annual_report_filed", True):
            score -= 15
            violations.append({"type": "missing_report", "severity": "moderate", "details": "Annual monitoring report (H-10) not filed"})
        if well.get("seismic_event_nearby", False):
            score -= 10
            warnings.append("Seismic event detected within review radius")
        score = max(0.0, score)
        if score >= 80:
            status = ComplianceStatus.COMPLIANT
        elif score >= 60:
            status = ComplianceStatus.MINOR_VIOLATION
        elif score >= 40:
            status = ComplianceStatus.MAJOR_VIOLATION
        else:
            status = ComplianceStatus.ENFORCEMENT_ACTION
        result = {
            "well_id": well_id,
            "compliance_score": round(score, 1),
            "status": status.value,
            "violations": violations,
            "warnings": warnings,
            "violation_count": len(violations),
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        result["determinism_hash"] = hashlib.sha256(
            json.dumps({"id": well_id, "score": result["compliance_score"], "violations": len(violations)}, sort_keys=True).encode()
        ).hexdigest()
        return result

    def check_all(self) -> list[dict[str, Any]]:
        results = []
        for well_id in self._wells:
            results.append(self.check_compliance(well_id))
        results.sort(key=lambda x: x.get("compliance_score", 100))
        logger.info(f"Compliance check: {len(results)} wells evaluated")
        return results

    def get_critical_wells(self) -> list[dict[str, Any]]:
        all_results = self.check_all()
        return [r for r in all_results if r.get("compliance_score", 100) < 60]


# ---------------------------------------------------------------------------
# Water Permit Tracker
# ---------------------------------------------------------------------------

class WaterPermitTracker:
    """Track and manage water permits across agencies."""

    def __init__(self) -> None:
        self._permits: dict[str, dict[str, Any]] = {}
        logger.info("WaterPermitTracker initialized")

    def add_permit(self, permit: dict[str, Any]) -> str:
        permit_id = permit.get("permit_number", str(uuid.uuid4()))
        self._permits[permit_id] = permit
        logger.debug(f"Added permit: {permit_id}")
        return permit_id

    def get_permit(self, permit_id: str) -> Optional[dict[str, Any]]:
        return self._permits.get(permit_id)

    def search_permits(self, query: str, county: Optional[str] = None,
                       right_type: Optional[WaterRightType] = None,
                       max_results: int = 25) -> list[dict[str, Any]]:
        query_lower = query.lower()
        results: list[tuple[float, dict[str, Any]]] = []
        for permit_id, permit in self._permits.items():
            if county and permit.get("county", "").lower() != county.lower():
                continue
            if right_type and permit.get("right_type") != right_type.value:
                continue
            score = 0.0
            searchable = " ".join(str(v) for v in permit.values() if isinstance(v, str)).lower()
            for term in query_lower.split():
                if term in searchable:
                    score += 1.0
                if term in permit.get("permit_number", "").lower():
                    score += 3.0
                if term in permit.get("operator", "").lower():
                    score += 2.0
            if score > 0:
                results.append((score, permit))
        results.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in results[:max_results]]

    def get_expiring_permits(self, days_ahead: int = 90) -> list[dict[str, Any]]:
        from datetime import datetime as dt, timedelta
        cutoff = dt.now() + timedelta(days=days_ahead)
        expiring: list[dict[str, Any]] = []
        for permit in self._permits.values():
            exp_str = permit.get("expiration_date", "")
            if not exp_str:
                continue
            try:
                exp_date = dt.strptime(exp_str, "%Y-%m-%d")
                if exp_date <= cutoff:
                    remaining_days = (exp_date - dt.now()).days
                    expiring.append({**permit, "days_until_expiration": remaining_days, "expired": remaining_days < 0})
            except ValueError:
                continue
        expiring.sort(key=lambda x: x.get("days_until_expiration", 999))
        return expiring

    def get_stats(self) -> dict[str, Any]:
        total = len(self._permits)
        by_type: dict[str, int] = defaultdict(int)
        by_county: dict[str, int] = defaultdict(int)
        by_agency: dict[str, int] = defaultdict(int)
        for permit in self._permits.values():
            by_type[permit.get("right_type", "unknown")] += 1
            by_county[permit.get("county", "unknown")] += 1
            by_agency[permit.get("agency", "unknown")] += 1
        return {
            "total_permits": total,
            "by_type": dict(by_type),
            "by_county": dict(by_county),
            "by_agency": dict(by_agency),
        }


# ---------------------------------------------------------------------------
# Aquifer Data Searcher
# ---------------------------------------------------------------------------

class AquiferDataSearcher:
    """Search and retrieve aquifer data and statistics."""

    def __init__(self) -> None:
        self._aquifer_data: dict[str, dict[str, Any]] = {}
        self._well_data: dict[str, dict[str, Any]] = {}
        self._load_default_aquifers()
        logger.info("AquiferDataSearcher initialized with default aquifer data")

    def _load_default_aquifers(self) -> None:
        defaults = [
            {"name": "Ogallala", "type": "unconfined", "region": "Texas High Plains / West Texas", "area_sq_miles": 34000, "avg_saturated_thickness_ft": 95, "recharge_in_per_yr": 0.5, "tds_range": [300, 1500], "depletion_risk": "critical", "permian_relevance": "high"},
            {"name": "Edwards-Trinity (Plateau)", "type": "confined-unconfined", "region": "Central-West Texas", "area_sq_miles": 35700, "avg_saturated_thickness_ft": 400, "recharge_in_per_yr": 1.2, "tds_range": [250, 2000], "depletion_risk": "moderate", "permian_relevance": "moderate"},
            {"name": "Pecos Valley", "type": "unconfined", "region": "Trans-Pecos / Reeves-Ward-Pecos", "area_sq_miles": 6800, "avg_saturated_thickness_ft": 250, "recharge_in_per_yr": 0.3, "tds_range": [500, 5000], "depletion_risk": "high", "permian_relevance": "critical"},
            {"name": "Dockum", "type": "confined", "region": "West Texas / Eastern NM", "area_sq_miles": 18000, "avg_saturated_thickness_ft": 200, "recharge_in_per_yr": 0.1, "tds_range": [1000, 10000], "depletion_risk": "high", "permian_relevance": "high"},
            {"name": "Rustler", "type": "confined", "region": "Trans-Pecos", "area_sq_miles": 3500, "avg_saturated_thickness_ft": 150, "recharge_in_per_yr": 0.05, "tds_range": [3000, 35000], "depletion_risk": "low", "permian_relevance": "moderate"},
            {"name": "Santa Rosa", "type": "confined", "region": "Southern High Plains", "area_sq_miles": 8000, "avg_saturated_thickness_ft": 100, "recharge_in_per_yr": 0.2, "tds_range": [500, 3000], "depletion_risk": "moderate", "permian_relevance": "moderate"},
            {"name": "Edwards", "type": "confined", "region": "South-Central Texas", "area_sq_miles": 4350, "avg_saturated_thickness_ft": 500, "recharge_in_per_yr": 4.0, "tds_range": [200, 500], "depletion_risk": "moderate", "permian_relevance": "low"},
        ]
        for aq in defaults:
            self._aquifer_data[aq["name"].lower()] = aq

    def search_aquifer(self, query: str) -> list[dict[str, Any]]:
        query_lower = query.lower()
        results: list[tuple[float, dict[str, Any]]] = []
        for key, aq in self._aquifer_data.items():
            score = 0.0
            if query_lower in key:
                score += 5.0
            searchable = " ".join(str(v) for v in aq.values() if isinstance(v, str)).lower()
            for term in query_lower.split():
                if term in searchable:
                    score += 1.0
            if score > 0:
                results.append((score, aq))
        results.sort(key=lambda x: x[0], reverse=True)
        return [a for _, a in results]

    def get_aquifer(self, name: str) -> Optional[dict[str, Any]]:
        return self._aquifer_data.get(name.lower())

    def get_permian_aquifers(self) -> list[dict[str, Any]]:
        return [
            aq for aq in self._aquifer_data.values()
            if aq.get("permian_relevance") in ("high", "critical")
        ]

    def add_well_observation(self, well_id: str, data: dict[str, Any]) -> None:
        self._well_data[well_id] = data

    def get_well_observations(self, aquifer: Optional[str] = None, county: Optional[str] = None) -> list[dict[str, Any]]:
        results = list(self._well_data.values())
        if aquifer:
            results = [w for w in results if w.get("aquifer", "").lower() == aquifer.lower()]
        if county:
            results = [w for w in results if w.get("county", "").lower() == county.lower()]
        return results

    def get_depletion_summary(self) -> dict[str, Any]:
        summary: dict[str, Any] = {}
        for name, aq in self._aquifer_data.items():
            summary[aq["name"]] = {
                "depletion_risk": aq.get("depletion_risk", "unknown"),
                "avg_saturated_thickness_ft": aq.get("avg_saturated_thickness_ft", 0),
                "recharge_in_per_yr": aq.get("recharge_in_per_yr", 0),
                "tds_range": aq.get("tds_range", []),
                "permian_relevance": aq.get("permian_relevance", "unknown"),
            }
        return summary
