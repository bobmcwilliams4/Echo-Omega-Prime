"""
LG08 Real Estate Law Engine - Search Module
==============================================
TF-IDF based vector search over real estate doctrine blocks,
title records, deed analysis, and property law references.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - TitleChainAnalyzer: Chain of title examination simulation
    - DeedInterpreter: Deed type identification and covenant analysis
    - ZoningComplianceChecker: Zoning classification and compliance
    - EncumbranceDetector: Lien and encumbrance identification
    - TransactionChecklist: Due diligence checklist generator
    - Exchange1031Validator: 1031 exchange requirement validation

Version: 2.0.0
Engine: LG08 Real Estate Law
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEARCH RESULT
# ============================================================================

@dataclass
class SearchResult:
    """A single search result with scoring breakdown."""
    doc_id: str
    topic: str
    content: str
    score: float
    tf_idf_score: float
    authority_score: float
    recency_score: float
    re_category: str
    matched_tokens: List[str]
    source: str = "doctrine_cache"
    jurisdiction: Optional[str] = None
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "doc_id": self.doc_id,
            "topic": self.topic,
            "content": self.content[:500],
            "score": round(self.score, 6),
            "tf_idf_score": round(self.tf_idf_score, 6),
            "authority_score": round(self.authority_score, 6),
            "recency_score": round(self.recency_score, 6),
            "re_category": self.re_category,
            "jurisdiction": self.jurisdiction,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# TITLE CHAIN ENTRY
# ============================================================================

@dataclass
class TitleChainEntry:
    """A single entry in a chain of title."""
    instrument_number: str
    instrument_type: str
    grantor: str
    grantee: str
    recording_date: str
    book_page: Optional[str] = None
    legal_description: Optional[str] = None
    consideration: Optional[str] = None
    encumbrances_noted: List[str] = dc_field(default_factory=list)
    issues_detected: List[str] = dc_field(default_factory=list)
    confidence: float = 0.8

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "instrument_number": self.instrument_number,
            "instrument_type": self.instrument_type,
            "grantor": self.grantor,
            "grantee": self.grantee,
            "recording_date": self.recording_date,
            "book_page": self.book_page,
            "legal_description": self.legal_description,
            "consideration": self.consideration,
            "encumbrances_noted": self.encumbrances_noted,
            "issues_detected": self.issues_detected,
            "confidence": round(self.confidence, 4),
        }


# ============================================================================
# ENCUMBRANCE RECORD
# ============================================================================

@dataclass
class EncumbranceRecord:
    """A detected encumbrance on a property."""
    encumbrance_type: str
    description: str
    recorded_reference: str
    priority_position: int
    amount: Optional[float] = None
    holder: Optional[str] = None
    status: str = "active"
    affects_marketability: bool = True
    cure_method: Optional[str] = None
    severity: str = "medium"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "encumbrance_type": self.encumbrance_type,
            "description": self.description,
            "recorded_reference": self.recorded_reference,
            "priority_position": self.priority_position,
            "amount": self.amount,
            "holder": self.holder,
            "status": self.status,
            "affects_marketability": self.affects_marketability,
            "cure_method": self.cure_method,
            "severity": self.severity,
        }


# ============================================================================
# ZONING COMPLIANCE RESULT
# ============================================================================

@dataclass
class ZoningComplianceResult:
    """Result of a zoning compliance analysis."""
    current_zoning: str
    proposed_use: str
    compliant: bool
    issues: List[str]
    required_permits: List[str]
    variance_needed: bool
    variance_type: Optional[str] = None
    setback_requirements: Dict[str, float] = dc_field(default_factory=dict)
    density_limit: Optional[str] = None
    parking_requirements: Optional[str] = None
    recommendation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "current_zoning": self.current_zoning,
            "proposed_use": self.proposed_use,
            "compliant": self.compliant,
            "issues": self.issues,
            "required_permits": self.required_permits,
            "variance_needed": self.variance_needed,
            "variance_type": self.variance_type,
            "setback_requirements": self.setback_requirements,
            "density_limit": self.density_limit,
            "parking_requirements": self.parking_requirements,
            "recommendation": self.recommendation,
        }


# ============================================================================
# EXCHANGE 1031 VALIDATION RESULT
# ============================================================================

@dataclass
class Exchange1031Result:
    """Result of a 1031 exchange validation."""
    qualifies: bool
    exchange_type: str
    issues: List[str]
    requirements_met: Dict[str, bool]
    timeline: Dict[str, str]
    boot_amount: float
    tax_deferred: bool
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "qualifies": self.qualifies,
            "exchange_type": self.exchange_type,
            "issues": self.issues,
            "requirements_met": self.requirements_met,
            "timeline": self.timeline,
            "boot_amount": self.boot_amount,
            "tax_deferred": self.tax_deferred,
            "recommendations": self.recommendations,
        }


# ============================================================================
# DOCTRINE SEARCH INDEX (TF-IDF)
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index for searching over real estate doctrine blocks.

    Supports boosted search with authority weighting, jurisdiction
    filtering, and recency scoring.
    """

    def __init__(self, min_token_length: int = 2, max_token_length: int = 50) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._term_freq: Dict[str, Counter] = {}
        self._doc_freq: Counter = Counter()
        self._doc_count: int = 0
        self._min_token_length: int = min_token_length
        self._max_token_length: int = max_token_length
        self._idf_cache: Dict[str, float] = {}
        self._dirty: bool = False
        logger.info("DoctrineSearchIndex initialized")

    def add_document(
        self,
        doc_id: str,
        topic: str,
        content: str,
        re_category: str = "general",
        authority_score: float = 0.5,
        jurisdiction: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the search index."""
        tokens = self._tokenize(content)
        tf = Counter(tokens)
        unique_tokens = set(tokens)

        self._documents[doc_id] = {
            "topic": topic,
            "content": content,
            "re_category": re_category,
            "authority_score": authority_score,
            "jurisdiction": jurisdiction,
            "tokens": tokens,
            "unique_tokens": unique_tokens,
            "metadata": metadata or {},
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._term_freq[doc_id] = tf
        for token in unique_tokens:
            self._inverted_index[token].add(doc_id)
            self._doc_freq[token] += 1
        self._doc_count += 1
        self._dirty = True

    def search(
        self,
        query_tokens: List[str],
        top_k: int = 5,
        score_threshold: float = 0.1,
        re_category_filter: Optional[str] = None,
        jurisdiction_filter: Optional[str] = None,
        authority_weight: float = 0.3,
        recency_weight: float = 0.1,
    ) -> List[SearchResult]:
        """Search the index with TF-IDF scoring."""
        if self._dirty:
            self._rebuild_idf_cache()

        candidate_docs: Set[str] = set()
        for token in query_tokens:
            normalized = token.lower()
            if normalized in self._inverted_index:
                candidate_docs.update(self._inverted_index[normalized])

        if not candidate_docs:
            return []

        results: List[SearchResult] = []
        for doc_id in candidate_docs:
            doc = self._documents[doc_id]

            if re_category_filter and doc["re_category"] != re_category_filter:
                continue
            if jurisdiction_filter and doc.get("jurisdiction") and doc["jurisdiction"] != jurisdiction_filter:
                continue

            tf_idf = self._compute_tf_idf(doc_id, query_tokens)
            auth_score = doc["authority_score"]
            recency = self._compute_recency_score(doc.get("indexed_at", ""))

            combined = (
                tf_idf * (1.0 - authority_weight - recency_weight) +
                auth_score * authority_weight +
                recency * recency_weight
            )

            if combined < score_threshold:
                continue

            matched = [t for t in query_tokens if t.lower() in doc["unique_tokens"]]

            results.append(SearchResult(
                doc_id=doc_id,
                topic=doc["topic"],
                content=doc["content"],
                score=combined,
                tf_idf_score=tf_idf,
                authority_score=auth_score,
                recency_score=recency,
                re_category=doc["re_category"],
                matched_tokens=matched,
                source="doctrine_cache",
                jurisdiction=doc.get("jurisdiction"),
                metadata=doc.get("metadata", {}),
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for indexing."""
        tokens = re.findall(r"[\w]+(?:[-_][\w]+)*", text.lower())
        return [
            t for t in tokens
            if self._min_token_length <= len(t) <= self._max_token_length
        ]

    def _compute_tf_idf(self, doc_id: str, query_tokens: List[str]) -> float:
        """Compute TF-IDF score for a document against query tokens."""
        if doc_id not in self._term_freq:
            return 0.0
        tf = self._term_freq[doc_id]
        doc_length = sum(tf.values())
        if doc_length == 0:
            return 0.0

        score = 0.0
        for token in query_tokens:
            normalized = token.lower()
            term_count = tf.get(normalized, 0)
            if term_count == 0:
                continue
            tf_val = term_count / doc_length
            idf_val = self._idf_cache.get(normalized, 0.0)
            score += tf_val * idf_val
        return score

    def _rebuild_idf_cache(self) -> None:
        """Rebuild the IDF cache."""
        self._idf_cache.clear()
        for term, df in self._doc_freq.items():
            self._idf_cache[term] = math.log((self._doc_count + 1) / (df + 1)) + 1.0
        self._dirty = False

    def _compute_recency_score(self, indexed_at: str) -> float:
        """Compute recency score based on indexing time."""
        if not indexed_at:
            return 0.5
        try:
            dt = datetime.fromisoformat(indexed_at.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
            return max(0.0, 1.0 - (age_days / 365.0))
        except (ValueError, TypeError):
            return 0.5

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            "document_count": self._doc_count,
            "unique_terms": len(self._inverted_index),
            "avg_doc_length": (
                sum(len(d["tokens"]) for d in self._documents.values()) / max(self._doc_count, 1)
            ),
            "categories": list(set(d["re_category"] for d in self._documents.values())),
            "jurisdictions": list(set(d.get("jurisdiction", "general") for d in self._documents.values())),
        }


# ============================================================================
# TITLE CHAIN ANALYZER
# ============================================================================

class TitleChainAnalyzer:
    """Simulates chain of title examination with gap detection and encumbrance identification."""

    COMMON_TITLE_ISSUES: ClassVar[Dict[str, str]] = {
        "gap_in_chain": "Missing link in chain of title between consecutive owners",
        "unreleased_lien": "Recorded lien without corresponding satisfaction or release",
        "boundary_dispute": "Conflicting legal descriptions in successive conveyances",
        "forged_instrument": "Instrument with suspected forgery or unauthorized signature",
        "missing_spousal_joinder": "Conveyance without required spousal consent in community property state",
        "defective_acknowledgment": "Notary acknowledgment missing or defective",
        "undisclosed_heir": "Potential claim by undisclosed heir of deceased owner",
        "tax_lien_outstanding": "Unpaid property taxes creating senior lien",
        "mechanics_lien": "Filed mechanics/materialman lien for unpaid construction work",
        "lis_pendens": "Recorded notice of pending litigation affecting title",
        "judgment_lien": "Abstract of judgment creating lien against property",
        "federal_tax_lien": "IRS tax lien recorded against property owner",
        "easement_not_disclosed": "Easement discovered during examination not previously disclosed",
        "mineral_reservation": "Prior deed reserved mineral rights creating split estate",
    }

    SAMPLE_CHAIN: ClassVar[List[Dict[str, Any]]] = [
        {
            "inst": "2005-0012345", "type": "General Warranty Deed", "date": "2005-03-15",
            "grantor": "Smith Family Trust", "grantee": "Johnson, Robert & Mary",
            "book_page": "Vol 1234/567", "consideration": "$185,000",
        },
        {
            "inst": "2005-0012400", "type": "Deed of Trust", "date": "2005-03-15",
            "grantor": "Johnson, Robert & Mary", "grantee": "First National Bank",
            "book_page": "Vol 1234/580", "consideration": "$148,000",
        },
        {
            "inst": "2010-0045678", "type": "Release of Lien", "date": "2010-06-20",
            "grantor": "First National Bank", "grantee": "Johnson, Robert & Mary",
            "book_page": "Vol 2345/123", "consideration": "N/A",
        },
        {
            "inst": "2012-0078901", "type": "General Warranty Deed", "date": "2012-09-01",
            "grantor": "Johnson, Robert & Mary", "grantee": "Williams Development LLC",
            "book_page": "Vol 2567/890", "consideration": "$225,000",
        },
        {
            "inst": "2012-0078950", "type": "Deed of Trust", "date": "2012-09-01",
            "grantor": "Williams Development LLC", "grantee": "Regional Savings Bank",
            "book_page": "Vol 2567/910", "consideration": "$180,000",
        },
        {
            "inst": "2018-0034567", "type": "Special Warranty Deed", "date": "2018-04-10",
            "grantor": "Williams Development LLC", "grantee": "Current Owner, Jane",
            "book_page": "Vol 3456/234", "consideration": "$310,000",
        },
        {
            "inst": "2018-0034600", "type": "Deed of Trust", "date": "2018-04-10",
            "grantor": "Current Owner, Jane", "grantee": "Mortgage Corp of America",
            "book_page": "Vol 3456/260", "consideration": "$248,000",
        },
    ]

    def analyze_chain(self, chain_data: Optional[List[Dict[str, Any]]] = None) -> List[TitleChainEntry]:
        """Analyze a chain of title for issues."""
        data = chain_data or self.SAMPLE_CHAIN
        entries: List[TitleChainEntry] = []

        for i, record in enumerate(data):
            issues: List[str] = []
            encumbrances: List[str] = []

            # Check for chain continuity
            if i > 0:
                prev = data[i - 1]
                if record["type"] not in ("Release of Lien", "Deed of Trust", "Mechanic's Lien"):
                    if prev["grantee"] != record["grantor"] and prev["grantor"] != record["grantor"]:
                        issues.append("gap_in_chain")

            # Check deed type for warranty concerns
            if record["type"] == "Special Warranty Deed":
                issues.append("limited_warranty_only")
            elif record["type"] == "Quitclaim Deed":
                issues.append("no_warranty_protection")

            # Identify encumbrances
            if record["type"] == "Deed of Trust":
                encumbrances.append(f"Mortgage lien: {record.get('consideration', 'unknown amount')}")
            if record["type"] == "Mechanic's Lien":
                encumbrances.append("Mechanics lien filed")

            confidence = 0.9 if not issues else max(0.5, 0.9 - len(issues) * 0.1)

            entries.append(TitleChainEntry(
                instrument_number=record["inst"],
                instrument_type=record["type"],
                grantor=record["grantor"],
                grantee=record["grantee"],
                recording_date=record["date"],
                book_page=record.get("book_page"),
                legal_description=record.get("legal_desc"),
                consideration=record.get("consideration"),
                encumbrances_noted=encumbrances,
                issues_detected=issues,
                confidence=confidence,
            ))

        return entries

    def identify_encumbrances(self, chain: List[TitleChainEntry]) -> List[EncumbranceRecord]:
        """Identify active encumbrances from chain analysis."""
        encumbrances: List[EncumbranceRecord] = []
        active_liens: Dict[str, TitleChainEntry] = {}
        position = 1

        for entry in chain:
            if entry.instrument_type in ("Deed of Trust", "Mortgage"):
                active_liens[entry.instrument_number] = entry
                encumbrances.append(EncumbranceRecord(
                    encumbrance_type="mortgage_lien",
                    description=f"Mortgage/DOT from {entry.grantor} to {entry.grantee}",
                    recorded_reference=f"{entry.instrument_number} ({entry.book_page or 'N/A'})",
                    priority_position=position,
                    amount=self._parse_amount(entry.consideration),
                    holder=entry.grantee,
                    status="active",
                    affects_marketability=True,
                    cure_method="Payoff at closing or obtain release/satisfaction",
                    severity="high",
                ))
                position += 1
            elif entry.instrument_type == "Release of Lien":
                # Mark corresponding lien as released
                for enc in encumbrances:
                    if enc.holder == entry.grantor and enc.status == "active":
                        enc.status = "released"
                        enc.affects_marketability = False
                        enc.severity = "none"

        return [e for e in encumbrances if e.status == "active"]

    def _parse_amount(self, consideration: Optional[str]) -> Optional[float]:
        """Parse dollar amount from consideration string."""
        if not consideration:
            return None
        cleaned = re.sub(r"[^\d.]", "", consideration)
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return None

    def generate_title_opinion(self, chain: List[TitleChainEntry], encumbrances: List[EncumbranceRecord]) -> Dict[str, Any]:
        """Generate a preliminary title opinion."""
        total_issues = sum(len(e.issues_detected) for e in chain)
        active_encumbrances = [e for e in encumbrances if e.status == "active"]
        marketable = total_issues == 0 and len(active_encumbrances) == 0
        insurable = total_issues <= 1 and all(e.severity != "critical" for e in active_encumbrances)

        requirements: List[str] = []
        if active_encumbrances:
            for enc in active_encumbrances:
                if enc.cure_method:
                    requirements.append(f"Cure {enc.encumbrance_type}: {enc.cure_method}")
        for entry in chain:
            for issue in entry.issues_detected:
                if issue == "gap_in_chain":
                    requirements.append(f"Resolve chain gap at instrument {entry.instrument_number}")
                elif issue == "limited_warranty_only":
                    requirements.append(f"Consider title insurance endorsement for limited warranty at {entry.instrument_number}")

        return {
            "marketable_title": marketable,
            "insurable_title": insurable,
            "chain_length": len(chain),
            "total_issues": total_issues,
            "active_encumbrances": len(active_encumbrances),
            "requirements_to_cure": requirements,
            "recommendation": (
                "Title appears marketable and insurable." if marketable
                else f"Title has {total_issues} issues and {len(active_encumbrances)} active encumbrances requiring resolution."
            ),
        }


# ============================================================================
# DEED INTERPRETER
# ============================================================================

class DeedInterpreter:
    """Interprets deed types and their legal implications."""

    DEED_TYPES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "general_warranty": {
            "name": "General Warranty Deed",
            "protection_level": "full",
            "covenants": [
                "Covenant of Seisin - Grantor warrants they own the property and have right to convey",
                "Covenant of Right to Convey - Grantor has authority to transfer title",
                "Covenant Against Encumbrances - No undisclosed liens, easements, or restrictions",
                "Covenant of Quiet Enjoyment - Grantee will not be disturbed by superior claims",
                "Covenant of Warranty - Grantor will defend title against all claims",
                "Covenant of Further Assurances - Grantor will execute additional documents if needed",
            ],
            "risk_to_buyer": "low",
            "covers_period": "all_time",
        },
        "special_warranty": {
            "name": "Special Warranty Deed",
            "protection_level": "limited",
            "covenants": [
                "Covenant of Seisin (during grantor's ownership only)",
                "Covenant Against Encumbrances (created during grantor's ownership only)",
            ],
            "risk_to_buyer": "medium",
            "covers_period": "grantor_ownership_only",
        },
        "quitclaim": {
            "name": "Quitclaim Deed",
            "protection_level": "none",
            "covenants": [],
            "risk_to_buyer": "high",
            "covers_period": "none",
        },
        "deed_of_trust": {
            "name": "Deed of Trust",
            "protection_level": "security_instrument",
            "covenants": ["Power of sale clause", "Acceleration clause", "Due on sale clause"],
            "risk_to_buyer": "n/a_security_instrument",
            "covers_period": "until_satisfaction",
        },
        "bargain_and_sale": {
            "name": "Bargain and Sale Deed",
            "protection_level": "implied",
            "covenants": ["Implied covenant that grantor has not encumbered the property"],
            "risk_to_buyer": "medium_high",
            "covers_period": "implied_only",
        },
        "grant_deed": {
            "name": "Grant Deed",
            "protection_level": "statutory",
            "covenants": [
                "Grantor has not previously conveyed the property",
                "Property is free from encumbrances made by grantor",
            ],
            "risk_to_buyer": "medium",
            "covers_period": "grantor_actions_only",
        },
    }

    def interpret_deed(self, deed_type: str) -> Dict[str, Any]:
        """Interpret a deed type and its legal implications."""
        normalized = deed_type.lower().replace(" ", "_").replace("-", "_")
        for key, info in self.DEED_TYPES.items():
            if key in normalized or normalized in key:
                return {
                    "deed_type": info["name"],
                    "protection_level": info["protection_level"],
                    "covenants": info["covenants"],
                    "risk_to_buyer": info["risk_to_buyer"],
                    "covers_period": info["covers_period"],
                    "recommendation": self._get_recommendation(key),
                }
        return {
            "deed_type": deed_type,
            "protection_level": "unknown",
            "covenants": [],
            "risk_to_buyer": "unknown",
            "covers_period": "unknown",
            "recommendation": "Deed type not recognized. Consult with a real estate attorney for interpretation.",
        }

    def _get_recommendation(self, deed_key: str) -> str:
        """Get recommendation based on deed type."""
        recommendations: Dict[str, str] = {
            "general_warranty": "This deed provides the highest level of protection. Standard for residential purchases. Verify all covenants are present and grantor has authority.",
            "special_warranty": "This deed only warrants against defects during grantor's ownership period. Common in commercial transactions and REO sales. Consider enhanced title insurance.",
            "quitclaim": "This deed provides NO warranties. Only transfers whatever interest grantor may have. NOT suitable for purchase transactions. Common for inter-family transfers, divorce settlements, and clearing title defects.",
            "deed_of_trust": "This is a security instrument, not a conveyance. Creates lien on property to secure debt. Review power of sale, acceleration, and due-on-sale clauses carefully.",
            "bargain_and_sale": "This deed implies grantor has title but makes no express warranties. Title insurance is strongly recommended. Common in tax sales and foreclosure conveyances.",
            "grant_deed": "This deed provides statutory warranties that grantor has not previously conveyed and has not encumbered the property. Standard in California. Title insurance recommended.",
        }
        return recommendations.get(deed_key, "Review deed carefully with legal counsel.")

    def compare_deeds(self, deed_type_a: str, deed_type_b: str) -> Dict[str, Any]:
        """Compare two deed types."""
        info_a = self.interpret_deed(deed_type_a)
        info_b = self.interpret_deed(deed_type_b)
        protection_ranking = {"full": 5, "statutory": 4, "limited": 3, "implied": 2, "none": 1, "security_instrument": 0, "unknown": 0}
        rank_a = protection_ranking.get(info_a["protection_level"], 0)
        rank_b = protection_ranking.get(info_b["protection_level"], 0)
        return {
            "deed_a": info_a,
            "deed_b": info_b,
            "stronger_protection": deed_type_a if rank_a >= rank_b else deed_type_b,
            "covenant_difference": len(info_a.get("covenants", [])) - len(info_b.get("covenants", [])),
        }


# ============================================================================
# ZONING COMPLIANCE CHECKER
# ============================================================================

class ZoningComplianceChecker:
    """Checks proposed use against zoning classifications."""

    ZONING_CATEGORIES: ClassVar[Dict[str, Dict[str, Any]]] = {
        "R-1": {"name": "Single Family Residential", "permitted": ["single_family_home", "home_office", "garden"],
                "conditional": ["adu", "daycare_home", "group_home"], "prohibited": ["commercial", "industrial", "multi_family"],
                "setbacks": {"front": 25.0, "rear": 20.0, "side": 7.5}, "max_height_ft": 35, "max_lot_coverage": 0.40},
        "R-2": {"name": "Two Family Residential", "permitted": ["single_family", "duplex", "home_office"],
                "conditional": ["triplex", "daycare_home", "church"], "prohibited": ["commercial", "industrial", "hotel"],
                "setbacks": {"front": 20.0, "rear": 15.0, "side": 5.0}, "max_height_ft": 35, "max_lot_coverage": 0.45},
        "R-3": {"name": "Multi Family Residential", "permitted": ["apartment", "condo", "townhouse", "single_family"],
                "conditional": ["assisted_living", "church", "school"], "prohibited": ["industrial", "heavy_commercial"],
                "setbacks": {"front": 15.0, "rear": 15.0, "side": 5.0}, "max_height_ft": 45, "max_lot_coverage": 0.55},
        "C-1": {"name": "Neighborhood Commercial", "permitted": ["retail", "office", "restaurant", "personal_service"],
                "conditional": ["drive_through", "gas_station", "liquor_store"], "prohibited": ["industrial", "heavy_commercial", "adult"],
                "setbacks": {"front": 10.0, "rear": 10.0, "side": 0.0}, "max_height_ft": 40, "max_lot_coverage": 0.70},
        "C-2": {"name": "General Commercial", "permitted": ["retail", "office", "hotel", "entertainment", "auto_sales"],
                "conditional": ["nightclub", "gun_range", "storage_facility"], "prohibited": ["industrial", "manufacturing"],
                "setbacks": {"front": 10.0, "rear": 10.0, "side": 0.0}, "max_height_ft": 60, "max_lot_coverage": 0.80},
        "I-1": {"name": "Light Industrial", "permitted": ["warehouse", "light_manufacturing", "office", "research"],
                "conditional": ["heavy_manufacturing", "recycling", "trucking"], "prohibited": ["residential", "school", "church"],
                "setbacks": {"front": 25.0, "rear": 20.0, "side": 10.0}, "max_height_ft": 50, "max_lot_coverage": 0.65},
        "I-2": {"name": "Heavy Industrial", "permitted": ["manufacturing", "warehouse", "processing", "utilities"],
                "conditional": ["hazardous_materials", "mining", "landfill"], "prohibited": ["residential", "school", "hospital"],
                "setbacks": {"front": 50.0, "rear": 50.0, "side": 25.0}, "max_height_ft": 75, "max_lot_coverage": 0.60},
        "AG": {"name": "Agricultural", "permitted": ["farming", "ranching", "single_family", "barn"],
               "conditional": ["wind_farm", "solar_farm", "agritourism", "oil_gas"], "prohibited": ["commercial", "industrial", "multi_family"],
               "setbacks": {"front": 50.0, "rear": 50.0, "side": 25.0}, "max_height_ft": 35, "max_lot_coverage": 0.20},
        "PUD": {"name": "Planned Unit Development", "permitted": ["mixed_use", "residential", "commercial", "open_space"],
                "conditional": ["industrial", "high_density"], "prohibited": [],
                "setbacks": {"front": 0.0, "rear": 0.0, "side": 0.0}, "max_height_ft": 0, "max_lot_coverage": 0.0},
    }

    def check_compliance(self, zoning_code: str, proposed_use: str) -> ZoningComplianceResult:
        """Check if a proposed use complies with the zoning code."""
        zone = self.ZONING_CATEGORIES.get(zoning_code.upper())
        if not zone:
            return ZoningComplianceResult(
                current_zoning=zoning_code,
                proposed_use=proposed_use,
                compliant=False,
                issues=[f"Zoning classification '{zoning_code}' not recognized"],
                required_permits=[],
                variance_needed=True,
                variance_type="use_variance",
                recommendation="Verify the correct zoning classification with the local planning department.",
            )

        use_lower = proposed_use.lower().replace(" ", "_")
        is_permitted = any(use_lower in p or p in use_lower for p in zone["permitted"])
        is_conditional = any(use_lower in c or c in use_lower for c in zone["conditional"])
        is_prohibited = any(use_lower in p or p in use_lower for p in zone["prohibited"])

        issues: List[str] = []
        permits: List[str] = []
        variance_needed = False
        variance_type = None

        if is_prohibited:
            issues.append(f"Proposed use '{proposed_use}' is prohibited in {zone['name']} ({zoning_code})")
            variance_needed = True
            variance_type = "use_variance"
        elif is_conditional:
            permits.append("Conditional Use Permit (CUP)")
            issues.append(f"Proposed use '{proposed_use}' requires conditional approval in {zone['name']}")
        elif not is_permitted:
            issues.append(f"Proposed use '{proposed_use}' not explicitly listed in {zone['name']} permitted uses")
            variance_needed = True
            variance_type = "use_variance"

        permits.append("Building Permit") if not is_prohibited else None

        compliant = is_permitted and not issues
        recommendation = self._generate_recommendation(compliant, is_conditional, is_prohibited, zone, zoning_code, proposed_use)

        return ZoningComplianceResult(
            current_zoning=zoning_code,
            proposed_use=proposed_use,
            compliant=compliant,
            issues=issues,
            required_permits=[p for p in permits if p],
            variance_needed=variance_needed,
            variance_type=variance_type,
            setback_requirements=zone["setbacks"],
            density_limit=f"Max lot coverage: {zone['max_lot_coverage']:.0%}",
            parking_requirements=f"Per local ordinance (varies by use and jurisdiction)",
            recommendation=recommendation,
        )

    def _generate_recommendation(
        self,
        compliant: bool,
        conditional: bool,
        prohibited: bool,
        zone: Dict[str, Any],
        code: str,
        use: str,
    ) -> str:
        """Generate a zoning recommendation."""
        if compliant:
            return f"Proposed use is permitted by right in {zone['name']} ({code}). Proceed with standard building permit application."
        if conditional:
            return f"Proposed use requires a Conditional Use Permit (CUP) in {zone['name']} ({code}). Apply through local planning commission. Expect 60-120 day review process. Public hearing may be required."
        if prohibited:
            return f"Proposed use is prohibited in {zone['name']} ({code}). Options: (1) Seek rezoning to appropriate classification, (2) Apply for use variance demonstrating unique hardship (high bar), (3) Consider alternative locations zoned for {use}."
        return f"Proposed use status unclear in {zone['name']} ({code}). Consult local planning department for determination. May require text amendment or interpretation."


# ============================================================================
# EXCHANGE 1031 VALIDATOR
# ============================================================================

class Exchange1031Validator:
    """Validates 1031 exchange requirements."""

    REQUIREMENTS: ClassVar[Dict[str, str]] = {
        "like_kind": "Both relinquished and replacement properties must be like-kind (real property for real property under TCJA 2017)",
        "held_for_investment": "Both properties must be held for productive use in trade/business or investment (not personal use)",
        "qualified_intermediary": "Must use a qualified intermediary (QI) to hold exchange funds - cannot touch proceeds",
        "identification_45_day": "Must identify replacement property within 45 calendar days of closing relinquished property",
        "closing_180_day": "Must close on replacement property within 180 calendar days of relinquished closing",
        "same_taxpayer": "Same taxpayer must sell relinquished and acquire replacement (entity changes may disqualify)",
        "no_related_party": "Related party exchanges have additional 2-year holding requirements under IRC 1031(f)",
        "us_property": "Both properties must be located within the United States",
    }

    def validate(
        self,
        relinquished_type: str,
        replacement_type: str,
        held_for_investment: bool,
        using_qi: bool,
        days_since_relinquished_close: int,
        replacement_identified: bool,
        same_taxpayer: bool,
        related_party: bool,
        exchange_type: str = "delayed",
    ) -> Exchange1031Result:
        """Validate a 1031 exchange against requirements."""
        requirements_met: Dict[str, bool] = {}
        issues: List[str] = []
        recommendations: List[str] = []

        # Like-kind check
        real_property_types = {"residential", "commercial", "industrial", "land", "ranch", "farm", "apartment", "office", "retail", "warehouse", "mixed_use"}
        relin_is_real = any(t in relinquished_type.lower() for t in real_property_types)
        repl_is_real = any(t in replacement_type.lower() for t in real_property_types)
        like_kind = relin_is_real and repl_is_real
        requirements_met["like_kind"] = like_kind
        if not like_kind:
            issues.append("Properties may not qualify as like-kind. Post-TCJA, only real property qualifies for 1031.")

        # Held for investment
        requirements_met["held_for_investment"] = held_for_investment
        if not held_for_investment:
            issues.append("Property must be held for investment or business use. Personal-use property does not qualify.")

        # QI
        requirements_met["qualified_intermediary"] = using_qi
        if not using_qi:
            issues.append("Must use a qualified intermediary. Taxpayer cannot take constructive receipt of proceeds.")
            recommendations.append("Engage a qualified intermediary BEFORE closing on relinquished property.")

        # 45-day identification
        within_45 = days_since_relinquished_close <= 45
        requirements_met["identification_45_day"] = replacement_identified or within_45
        if days_since_relinquished_close > 45 and not replacement_identified:
            issues.append(f"45-day identification period expired ({days_since_relinquished_close} days since close). Exchange fails.")

        # 180-day closing
        within_180 = days_since_relinquished_close <= 180
        requirements_met["closing_180_day"] = within_180
        if not within_180:
            issues.append(f"180-day exchange period expired ({days_since_relinquished_close} days). Exchange fails.")

        # Same taxpayer
        requirements_met["same_taxpayer"] = same_taxpayer
        if not same_taxpayer:
            issues.append("Different taxpayer on replacement. Exchange may be disqualified.")

        # Related party
        requirements_met["no_related_party"] = not related_party
        if related_party:
            issues.append("Related party transaction. Must hold replacement for 2+ years under IRC 1031(f).")
            recommendations.append("Document the business purpose for related-party exchange.")

        # US property (assumed true for now)
        requirements_met["us_property"] = True

        qualifies = all(requirements_met.values())
        boot_amount = 0.0  # Simplified - in production would calculate from values

        timeline = {
            "relinquished_close": "Day 0",
            "identification_deadline": "Day 45",
            "exchange_deadline": "Day 180",
            "current_day": f"Day {days_since_relinquished_close}",
            "days_remaining_identification": str(max(0, 45 - days_since_relinquished_close)),
            "days_remaining_closing": str(max(0, 180 - days_since_relinquished_close)),
        }

        if qualifies:
            recommendations.append("All requirements appear satisfied. Document exchange thoroughly for IRS audit defense.")
        else:
            recommendations.append("One or more requirements not met. Consult tax counsel before proceeding.")

        return Exchange1031Result(
            qualifies=qualifies,
            exchange_type=exchange_type,
            issues=issues,
            requirements_met=requirements_met,
            timeline=timeline,
            boot_amount=boot_amount,
            tax_deferred=qualifies and boot_amount == 0,
            recommendations=recommendations,
        )


# ============================================================================
# TRANSACTION CHECKLIST GENERATOR
# ============================================================================

class TransactionChecklistGenerator:
    """Generates due diligence checklists for real estate transactions."""

    PURCHASE_CHECKLIST: ClassVar[List[Dict[str, Any]]] = [
        {"item": "Executed Purchase Agreement", "category": "contract", "priority": "critical", "typical_timeline": "Day 0"},
        {"item": "Earnest Money Deposit", "category": "contract", "priority": "critical", "typical_timeline": "Within 3 days"},
        {"item": "Title Commitment/Search", "category": "title", "priority": "critical", "typical_timeline": "Days 5-10"},
        {"item": "Property Survey", "category": "due_diligence", "priority": "high", "typical_timeline": "Days 7-14"},
        {"item": "Property Inspection", "category": "due_diligence", "priority": "high", "typical_timeline": "Days 5-10"},
        {"item": "Environmental Assessment", "category": "due_diligence", "priority": "medium", "typical_timeline": "Days 10-20"},
        {"item": "Appraisal", "category": "financing", "priority": "critical", "typical_timeline": "Days 7-14"},
        {"item": "Loan Application", "category": "financing", "priority": "critical", "typical_timeline": "Days 1-5"},
        {"item": "Loan Approval/Commitment", "category": "financing", "priority": "critical", "typical_timeline": "Days 21-30"},
        {"item": "HOA Documents Review", "category": "due_diligence", "priority": "medium", "typical_timeline": "Days 5-10"},
        {"item": "Zoning Verification", "category": "due_diligence", "priority": "medium", "typical_timeline": "Days 5-10"},
        {"item": "Property Tax Review", "category": "due_diligence", "priority": "medium", "typical_timeline": "Days 5-10"},
        {"item": "Insurance Binder", "category": "insurance", "priority": "high", "typical_timeline": "Days 20-25"},
        {"item": "Final Walk-Through", "category": "closing", "priority": "high", "typical_timeline": "Day before closing"},
        {"item": "Closing Disclosure (3 days before)", "category": "closing", "priority": "critical", "typical_timeline": "3 days before"},
        {"item": "Wire Transfer Funds", "category": "closing", "priority": "critical", "typical_timeline": "Day of closing"},
        {"item": "Sign Closing Documents", "category": "closing", "priority": "critical", "typical_timeline": "Closing day"},
        {"item": "Record Deed", "category": "post_closing", "priority": "critical", "typical_timeline": "Same day as closing"},
        {"item": "Title Policy Issuance", "category": "post_closing", "priority": "high", "typical_timeline": "30-60 days post-closing"},
    ]

    def generate_checklist(self, transaction_type: str = "purchase") -> List[Dict[str, Any]]:
        """Generate a due diligence checklist for a transaction type."""
        if transaction_type.lower() in ("purchase", "buy", "acquisition"):
            return self.PURCHASE_CHECKLIST
        if transaction_type.lower() in ("sale", "sell", "disposition"):
            return [
                {"item": "Executed Listing Agreement", "category": "pre_sale", "priority": "critical", "typical_timeline": "Before marketing"},
                {"item": "Property Disclosure Statement", "category": "disclosure", "priority": "critical", "typical_timeline": "Before marketing"},
                {"item": "Lead-Based Paint Disclosure (if pre-1978)", "category": "disclosure", "priority": "critical", "typical_timeline": "Before marketing"},
                {"item": "Executed Purchase Agreement", "category": "contract", "priority": "critical", "typical_timeline": "Day 0"},
                {"item": "Title Commitment Ordered", "category": "title", "priority": "critical", "typical_timeline": "Days 1-3"},
                {"item": "Cure Title Issues", "category": "title", "priority": "high", "typical_timeline": "Days 5-20"},
                {"item": "Provide HOA Documents", "category": "hoa", "priority": "medium", "typical_timeline": "Days 3-7"},
                {"item": "Cooperate with Buyer Inspections", "category": "due_diligence", "priority": "high", "typical_timeline": "As scheduled"},
                {"item": "Negotiate Inspection Response", "category": "contract", "priority": "high", "typical_timeline": "Per contract"},
                {"item": "Obtain Payoff Statement", "category": "financing", "priority": "critical", "typical_timeline": "Days 20-25"},
                {"item": "Review Closing Statement", "category": "closing", "priority": "critical", "typical_timeline": "Before closing"},
                {"item": "Execute Deed", "category": "closing", "priority": "critical", "typical_timeline": "Closing day"},
                {"item": "Deliver Possession", "category": "post_closing", "priority": "critical", "typical_timeline": "Per contract"},
            ]
        if transaction_type.lower() in ("lease", "rental"):
            return [
                {"item": "Verify Tenant Application/Credit", "category": "screening", "priority": "critical", "typical_timeline": "Before lease"},
                {"item": "Execute Lease Agreement", "category": "contract", "priority": "critical", "typical_timeline": "Day 0"},
                {"item": "Collect Security Deposit", "category": "financial", "priority": "critical", "typical_timeline": "Before move-in"},
                {"item": "Move-In Condition Report", "category": "documentation", "priority": "high", "typical_timeline": "Move-in day"},
                {"item": "Provide Lead-Based Paint Disclosure (if applicable)", "category": "disclosure", "priority": "critical", "typical_timeline": "Before lease"},
                {"item": "Verify Insurance Requirements", "category": "insurance", "priority": "medium", "typical_timeline": "Before move-in"},
                {"item": "Deliver Keys/Access", "category": "operational", "priority": "critical", "typical_timeline": "Move-in day"},
            ]
        return self.PURCHASE_CHECKLIST


# ============================================================================
# MODULE-LEVEL SINGLETONS AND CONVENIENCE FUNCTIONS
# ============================================================================

_search_index: Optional[DoctrineSearchIndex] = None
_title_analyzer: Optional[TitleChainAnalyzer] = None
_deed_interpreter: Optional[DeedInterpreter] = None
_zoning_checker: Optional[ZoningComplianceChecker] = None
_exchange_validator: Optional[Exchange1031Validator] = None
_checklist_generator: Optional[TransactionChecklistGenerator] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the search index singleton."""
    global _search_index
    if _search_index is None:
        _search_index = DoctrineSearchIndex()
    return _search_index


def get_title_analyzer() -> TitleChainAnalyzer:
    """Get or create the title chain analyzer singleton."""
    global _title_analyzer
    if _title_analyzer is None:
        _title_analyzer = TitleChainAnalyzer()
    return _title_analyzer


def get_deed_interpreter() -> DeedInterpreter:
    """Get or create the deed interpreter singleton."""
    global _deed_interpreter
    if _deed_interpreter is None:
        _deed_interpreter = DeedInterpreter()
    return _deed_interpreter


def get_zoning_checker() -> ZoningComplianceChecker:
    """Get or create the zoning compliance checker singleton."""
    global _zoning_checker
    if _zoning_checker is None:
        _zoning_checker = ZoningComplianceChecker()
    return _zoning_checker


def get_exchange_validator() -> Exchange1031Validator:
    """Get or create the 1031 exchange validator singleton."""
    global _exchange_validator
    if _exchange_validator is None:
        _exchange_validator = Exchange1031Validator()
    return _exchange_validator


def get_checklist_generator() -> TransactionChecklistGenerator:
    """Get or create the transaction checklist generator singleton."""
    global _checklist_generator
    if _checklist_generator is None:
        _checklist_generator = TransactionChecklistGenerator()
    return _checklist_generator


def compute_query_hash(query: str) -> str:
    """Compute a deterministic hash for a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
