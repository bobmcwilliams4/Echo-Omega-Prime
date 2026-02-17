"""
LG14 Healthcare Law Engine - Search Module
==============================================
TF-IDF based vector search over healthcare law doctrine blocks,
HIPAA compliance records, fraud analysis, and regulatory references.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - HIPAAComplianceChecker: HIPAA gap analysis and compliance scoring
    - MalpracticeAnalyzer: Malpractice claim element analysis
    - FDARegulationSearcher: FDA regulatory pathway analysis
    - MedicareFraudDetector: Medicare fraud risk indicator analysis

Version: 2.0.0
Engine: LG14 Healthcare Law
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
    hc_category: str
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
            "hc_category": self.hc_category,
            "jurisdiction": self.jurisdiction,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# HIPAA COMPLIANCE RESULT
# ============================================================================

@dataclass
class HIPAAComplianceResult:
    """Result of a HIPAA compliance gap analysis."""
    overall_score: float
    privacy_rule_score: float
    security_rule_score: float
    breach_notification_score: float
    gaps: List[Dict[str, Any]]
    recommendations: List[str]
    risk_level: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "overall_score": round(self.overall_score, 4),
            "privacy_rule_score": round(self.privacy_rule_score, 4),
            "security_rule_score": round(self.security_rule_score, 4),
            "breach_notification_score": round(self.breach_notification_score, 4),
            "gaps": self.gaps,
            "recommendations": self.recommendations,
            "risk_level": self.risk_level,
        }


# ============================================================================
# MALPRACTICE ANALYSIS RESULT
# ============================================================================

@dataclass
class MalpracticeAnalysisResult:
    """Result of a malpractice claim element analysis."""
    duty_established: bool
    breach_indicators: List[str]
    causation_strength: str
    damages_identified: List[str]
    defenses_available: List[str]
    risk_assessment: str
    statute_of_limitations_notes: str
    procedural_requirements: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "duty_established": self.duty_established,
            "breach_indicators": self.breach_indicators,
            "causation_strength": self.causation_strength,
            "damages_identified": self.damages_identified,
            "defenses_available": self.defenses_available,
            "risk_assessment": self.risk_assessment,
            "statute_of_limitations_notes": self.statute_of_limitations_notes,
            "procedural_requirements": self.procedural_requirements,
        }


# ============================================================================
# FDA REGULATION RESULT
# ============================================================================

@dataclass
class FDARegulationResult:
    """Result of an FDA regulatory pathway analysis."""
    product_type: str
    classification: str
    regulatory_pathway: str
    requirements: List[str]
    timeline_estimate: str
    key_regulations: List[str]
    post_market_obligations: List[str]
    preemption_analysis: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "product_type": self.product_type,
            "classification": self.classification,
            "regulatory_pathway": self.regulatory_pathway,
            "requirements": self.requirements,
            "timeline_estimate": self.timeline_estimate,
            "key_regulations": self.key_regulations,
            "post_market_obligations": self.post_market_obligations,
            "preemption_analysis": self.preemption_analysis,
        }


# ============================================================================
# FRAUD RISK RESULT
# ============================================================================

@dataclass
class FraudRiskResult:
    """Result of a Medicare fraud risk analysis."""
    risk_level: str
    risk_score: float
    indicators: List[Dict[str, Any]]
    applicable_statutes: List[str]
    enforcement_exposure: Dict[str, Any]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "risk_level": self.risk_level,
            "risk_score": round(self.risk_score, 4),
            "indicators": self.indicators,
            "applicable_statutes": self.applicable_statutes,
            "enforcement_exposure": self.enforcement_exposure,
            "recommendations": self.recommendations,
        }


# ============================================================================
# TF-IDF SEARCH INDEX
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index over healthcare law doctrine blocks."""

    def __init__(self) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._term_frequencies: Dict[str, Counter] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0

    def add_document(
        self,
        doc_id: str,
        topic: str,
        content: str,
        hc_category: str,
        authority_score: float = 0.75,
        jurisdiction: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a document to the search index."""
        tokens = self._tokenize(content)
        tf = Counter(tokens)

        self._documents[doc_id] = {
            "topic": topic,
            "content": content,
            "hc_category": hc_category,
            "authority_score": authority_score,
            "jurisdiction": jurisdiction,
            "metadata": metadata or {},
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }

        self._term_frequencies[doc_id] = tf
        self._doc_lengths[doc_id] = len(tokens)
        self._total_docs = len(self._documents)

        for token in set(tokens):
            self._inverted_index[token].add(doc_id)

        total_len = sum(self._doc_lengths.values())
        self._avg_doc_length = total_len / max(self._total_docs, 1)

    def search(
        self,
        query_tokens: List[str],
        top_k: int = 5,
        score_threshold: float = 0.1,
        hc_category_filter: Optional[str] = None,
        jurisdiction_filter: Optional[str] = None,
        authority_weight: float = 0.3,
        recency_weight: float = 0.1,
    ) -> List[SearchResult]:
        """Search the index using TF-IDF scoring with BM25 variant."""
        normalized_tokens = [t.lower() for t in query_tokens if len(t) >= 2]
        if not normalized_tokens:
            return []

        candidate_docs: Set[str] = set()
        for token in normalized_tokens:
            if token in self._inverted_index:
                candidate_docs.update(self._inverted_index[token])

        if hc_category_filter:
            candidate_docs = {
                doc_id for doc_id in candidate_docs
                if self._documents[doc_id]["hc_category"] == hc_category_filter
            }

        if jurisdiction_filter:
            candidate_docs = {
                doc_id for doc_id in candidate_docs
                if self._documents[doc_id]["jurisdiction"] in (None, "federal", jurisdiction_filter)
            }

        results: List[SearchResult] = []
        k1 = 1.5
        b = 0.75

        for doc_id in candidate_docs:
            doc_info = self._documents[doc_id]
            tf = self._term_frequencies[doc_id]
            doc_len = self._doc_lengths[doc_id]
            matched: List[str] = []

            tfidf_score = 0.0
            for token in normalized_tokens:
                if token not in self._inverted_index:
                    continue
                df = len(self._inverted_index[token])
                idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)
                term_freq = tf.get(token, 0)
                if term_freq > 0:
                    matched.append(token)
                    numerator = term_freq * (k1 + 1)
                    denominator = term_freq + k1 * (1 - b + b * (doc_len / max(self._avg_doc_length, 1)))
                    tfidf_score += idf * (numerator / denominator)

            if tfidf_score <= 0:
                continue

            auth_score = doc_info["authority_score"]
            recency_score = 1.0

            final_score = (
                tfidf_score * (1.0 - authority_weight - recency_weight)
                + auth_score * authority_weight
                + recency_score * recency_weight
            )

            if final_score >= score_threshold:
                results.append(SearchResult(
                    doc_id=doc_id,
                    topic=doc_info["topic"],
                    content=doc_info["content"][:500],
                    score=final_score,
                    tf_idf_score=tfidf_score,
                    authority_score=auth_score,
                    recency_score=recency_score,
                    hc_category=doc_info["hc_category"],
                    matched_tokens=matched,
                    source="doctrine_cache",
                    jurisdiction=doc_info["jurisdiction"],
                    metadata=doc_info["metadata"],
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for indexing."""
        tokens = re.split(r"[\s\-_/,;:()\[\]{}\"']+", text.lower())
        return [t for t in tokens if t and len(t) >= 2]

    @property
    def document_count(self) -> int:
        """Return total documents indexed."""
        return self._total_docs

    @property
    def vocabulary_size(self) -> int:
        """Return vocabulary size."""
        return len(self._inverted_index)


# ============================================================================
# HIPAA COMPLIANCE CHECKER
# ============================================================================

class HIPAAComplianceChecker:
    """Evaluates HIPAA compliance based on a checklist of requirements."""

    PRIVACY_REQUIREMENTS: List[Dict[str, str]] = [
        {"id": "PR-01", "requirement": "Notice of Privacy Practices (NPP) published and provided to individuals", "cfr": "45 CFR 164.520"},
        {"id": "PR-02", "requirement": "Written authorization obtained for non-TPO uses and disclosures", "cfr": "45 CFR 164.508"},
        {"id": "PR-03", "requirement": "Minimum necessary standard implemented for all roles", "cfr": "45 CFR 164.502(b)"},
        {"id": "PR-04", "requirement": "Individual right of access process established (30-day response)", "cfr": "45 CFR 164.524"},
        {"id": "PR-05", "requirement": "Amendment request process established", "cfr": "45 CFR 164.526"},
        {"id": "PR-06", "requirement": "Accounting of disclosures process established", "cfr": "45 CFR 164.528"},
        {"id": "PR-07", "requirement": "Business associate agreements in place for all BAs", "cfr": "45 CFR 164.502(e)"},
        {"id": "PR-08", "requirement": "De-identification methods documented (Safe Harbor or Expert)", "cfr": "45 CFR 164.514"},
        {"id": "PR-09", "requirement": "Marketing authorization requirements followed", "cfr": "45 CFR 164.508(a)(3)"},
        {"id": "PR-10", "requirement": "Personal representative policies established", "cfr": "45 CFR 164.502(g)"},
    ]

    SECURITY_REQUIREMENTS: List[Dict[str, str]] = [
        {"id": "SR-01", "requirement": "Risk analysis conducted and documented", "cfr": "45 CFR 164.308(a)(1)(ii)(A)"},
        {"id": "SR-02", "requirement": "Risk management plan implemented", "cfr": "45 CFR 164.308(a)(1)(ii)(B)"},
        {"id": "SR-03", "requirement": "Workforce security training program", "cfr": "45 CFR 164.308(a)(5)"},
        {"id": "SR-04", "requirement": "Access controls implemented (unique user ID, emergency access)", "cfr": "45 CFR 164.312(a)"},
        {"id": "SR-05", "requirement": "Audit controls implemented and reviewed", "cfr": "45 CFR 164.312(b)"},
        {"id": "SR-06", "requirement": "Integrity controls for ePHI", "cfr": "45 CFR 164.312(c)"},
        {"id": "SR-07", "requirement": "Transmission security (encryption in transit)", "cfr": "45 CFR 164.312(e)"},
        {"id": "SR-08", "requirement": "Facility access controls", "cfr": "45 CFR 164.310(a)"},
        {"id": "SR-09", "requirement": "Workstation use and security policies", "cfr": "45 CFR 164.310(b)-(c)"},
        {"id": "SR-10", "requirement": "Contingency plan (data backup, disaster recovery, emergency mode)", "cfr": "45 CFR 164.308(a)(7)"},
    ]

    BREACH_REQUIREMENTS: List[Dict[str, str]] = [
        {"id": "BN-01", "requirement": "Breach detection and investigation procedures", "cfr": "45 CFR 164.404"},
        {"id": "BN-02", "requirement": "Four-factor risk assessment process documented", "cfr": "45 CFR 164.402"},
        {"id": "BN-03", "requirement": "Individual notification within 60 days of discovery", "cfr": "45 CFR 164.404(b)"},
        {"id": "BN-04", "requirement": "HHS notification process (annual for <500, 60 days for 500+)", "cfr": "45 CFR 164.408"},
        {"id": "BN-05", "requirement": "Media notification for breaches affecting 500+ in a state", "cfr": "45 CFR 164.406"},
    ]

    def check_compliance(self, answers: Dict[str, bool]) -> HIPAAComplianceResult:
        """Evaluate HIPAA compliance based on requirement answers (requirement_id -> met)."""
        privacy_met = sum(1 for req in self.PRIVACY_REQUIREMENTS if answers.get(req["id"], False))
        security_met = sum(1 for req in self.SECURITY_REQUIREMENTS if answers.get(req["id"], False))
        breach_met = sum(1 for req in self.BREACH_REQUIREMENTS if answers.get(req["id"], False))

        privacy_score = privacy_met / max(len(self.PRIVACY_REQUIREMENTS), 1)
        security_score = security_met / max(len(self.SECURITY_REQUIREMENTS), 1)
        breach_score = breach_met / max(len(self.BREACH_REQUIREMENTS), 1)
        overall = (privacy_score * 0.35 + security_score * 0.40 + breach_score * 0.25)

        gaps: List[Dict[str, Any]] = []
        for req_list in [self.PRIVACY_REQUIREMENTS, self.SECURITY_REQUIREMENTS, self.BREACH_REQUIREMENTS]:
            for req in req_list:
                if not answers.get(req["id"], False):
                    gaps.append({
                        "requirement_id": req["id"],
                        "requirement": req["requirement"],
                        "cfr": req["cfr"],
                        "severity": "HIGH" if req["id"] in ("SR-01", "SR-02", "BN-01", "BN-03", "PR-04", "PR-07") else "MEDIUM",
                    })

        risk_level = "CRITICAL" if overall < 0.4 else "HIGH" if overall < 0.6 else "MEDIUM" if overall < 0.8 else "LOW"

        recommendations: List[str] = []
        if privacy_score < 0.7:
            recommendations.append("Prioritize Privacy Rule compliance: ensure NPP, authorization, and individual rights processes are operational")
        if security_score < 0.7:
            recommendations.append("Prioritize Security Rule compliance: conduct risk analysis and implement required safeguards")
        if breach_score < 0.7:
            recommendations.append("Establish breach notification procedures and test with tabletop exercises")
        if not answers.get("SR-01", False):
            recommendations.append("CRITICAL: Conduct enterprise-wide risk analysis immediately - most commonly cited HIPAA deficiency")
        if not answers.get("PR-07", False):
            recommendations.append("CRITICAL: Inventory all business associates and execute BAAs")

        return HIPAAComplianceResult(
            overall_score=overall,
            privacy_rule_score=privacy_score,
            security_rule_score=security_score,
            breach_notification_score=breach_score,
            gaps=gaps,
            recommendations=recommendations,
            risk_level=risk_level,
        )

    def get_requirements(self) -> Dict[str, List[Dict[str, str]]]:
        """Return all HIPAA compliance requirements."""
        return {
            "privacy_rule": self.PRIVACY_REQUIREMENTS,
            "security_rule": self.SECURITY_REQUIREMENTS,
            "breach_notification": self.BREACH_REQUIREMENTS,
        }


# ============================================================================
# MALPRACTICE ANALYZER
# ============================================================================

class MalpracticeAnalyzer:
    """Analyzes medical malpractice claim elements."""

    def analyze_claim(self, facts: Dict[str, Any]) -> MalpracticeAnalysisResult:
        """Analyze malpractice claim elements based on provided facts."""
        duty_indicators = ["physician", "doctor", "hospital", "provider", "patient",
                           "treatment", "surgery", "diagnosis", "care", "consultation"]
        breach_indicators_list = ["failed", "error", "mistake", "wrong", "delayed",
                                  "misdiagnosis", "missed", "negligent", "deviated",
                                  "inadequate", "improper", "omitted", "substandard"]
        causation_indicators = ["caused", "resulted", "because", "led to", "consequence",
                                "but for", "proximate", "direct result"]
        damage_indicators = ["injury", "death", "harm", "pain", "suffering", "disability",
                             "loss", "expense", "cost", "disfigurement", "impairment"]

        description = facts.get("description", "").lower()

        duty_established = any(ind in description for ind in duty_indicators)
        breach_found = [ind for ind in breach_indicators_list if ind in description]
        causation_found = any(ind in description for ind in causation_indicators)
        damages_found = [ind for ind in damage_indicators if ind in description]

        causation_strength = "STRONG" if causation_found and breach_found else \
                            "MODERATE" if breach_found else "WEAK"

        defenses: List[str] = []
        if "consent" in description:
            defenses.append("Informed consent defense: patient may have consented to known risks")
        if "emergency" in description:
            defenses.append("Emergency/Good Samaritan defense may apply")
        if "standard" in description or "guideline" in description:
            defenses.append("Compliance with clinical guidelines may support standard of care defense")
        if "contributory" in description or "patient non-compliance" in description:
            defenses.append("Contributory/comparative negligence of the patient")
        if not defenses:
            defenses.append("Standard defenses: no deviation from standard of care, lack of causation, contributory negligence")

        risk = "HIGH" if duty_established and breach_found and damages_found else \
               "MEDIUM" if duty_established and (breach_found or damages_found) else "LOW"

        sol_notes = facts.get("jurisdiction", "General") + ": Check applicable statute of limitations (typically 2-3 years from injury or discovery). Minor tolling and discovery rule may extend deadline."

        procedural: List[str] = [
            "Check certificate of merit / affidavit of merit requirement",
            "Identify screening panel or mandatory mediation requirement",
            "Obtain qualified expert witness in same specialty",
            "Review applicable damages cap and tort reform provisions",
        ]

        return MalpracticeAnalysisResult(
            duty_established=duty_established,
            breach_indicators=breach_found,
            causation_strength=causation_strength,
            damages_identified=damages_found,
            defenses_available=defenses,
            risk_assessment=risk,
            statute_of_limitations_notes=sol_notes,
            procedural_requirements=procedural,
        )


# ============================================================================
# FDA REGULATION SEARCHER
# ============================================================================

class FDARegulationSearcher:
    """Analyzes FDA regulatory pathways for drugs and devices."""

    PATHWAYS: Dict[str, Dict[str, Any]] = {
        "nda_505b1": {
            "name": "New Drug Application - 505(b)(1)",
            "product_type": "drug",
            "description": "Full NDA with complete reports of safety and efficacy studies",
            "timeline": "10-15 months standard review; 6-8 months priority review",
            "key_regulations": ["21 CFR 314", "21 USC 355(b)(1)"],
            "post_market": ["Adverse event reporting", "REMS if required", "Annual reports", "Labeling supplements"],
        },
        "anda": {
            "name": "Abbreviated New Drug Application (Generic)",
            "product_type": "drug",
            "description": "Generic drug application demonstrating bioequivalence to reference listed drug",
            "timeline": "10-15 months standard; Paragraph IV challenge may extend",
            "key_regulations": ["21 CFR 314.94", "21 USC 355(j)"],
            "post_market": ["Adverse event reporting", "Annual reports", "Labeling updates per reference"],
        },
        "bla": {
            "name": "Biologics License Application",
            "product_type": "biologic",
            "description": "Application for licensure of biologic product demonstrating safety, purity, and potency",
            "timeline": "10-12 months standard; 6 months priority review",
            "key_regulations": ["42 USC 262", "21 CFR 601"],
            "post_market": ["Adverse event reporting", "Lot release", "Annual reports", "Post-marketing studies"],
        },
        "510k": {
            "name": "510(k) Premarket Notification",
            "product_type": "device",
            "description": "Premarket notification demonstrating substantial equivalence to predicate device",
            "timeline": "3-6 months standard; 90-day statutory review clock",
            "key_regulations": ["21 CFR 807 Subpart E", "21 USC 360(k)"],
            "post_market": ["MDR reporting", "UDI compliance", "QSR compliance", "Corrections and removals"],
        },
        "pma": {
            "name": "Premarket Approval Application",
            "product_type": "device",
            "description": "Application for Class III device requiring valid scientific evidence of safety and effectiveness",
            "timeline": "12-18 months; 180-day statutory review",
            "key_regulations": ["21 CFR 814", "21 USC 360e"],
            "post_market": ["MDR reporting", "Post-approval studies", "PMA supplements", "Annual reports"],
        },
        "de_novo": {
            "name": "De Novo Classification",
            "product_type": "device",
            "description": "Alternative pathway for novel low-to-moderate risk devices without a predicate",
            "timeline": "6-12 months; 150-day statutory review",
            "key_regulations": ["21 CFR 860.260", "21 USC 360e-1"],
            "post_market": ["MDR reporting", "UDI compliance", "QSR compliance", "Special controls"],
        },
    }

    def analyze_pathway(self, product_type: str, product_description: str) -> FDARegulationResult:
        """Determine applicable FDA regulatory pathway for a product."""
        product_lower = product_description.lower()
        best_pathway = None

        if product_type == "drug":
            if any(kw in product_lower for kw in ["generic", "bioequivalent", "anda"]):
                best_pathway = self.PATHWAYS["anda"]
            else:
                best_pathway = self.PATHWAYS["nda_505b1"]
        elif product_type == "biologic":
            best_pathway = self.PATHWAYS["bla"]
        elif product_type == "device":
            if any(kw in product_lower for kw in ["class iii", "high risk", "life sustaining", "implant"]):
                best_pathway = self.PATHWAYS["pma"]
            elif any(kw in product_lower for kw in ["novel", "no predicate", "de novo", "new type"]):
                best_pathway = self.PATHWAYS["de_novo"]
            else:
                best_pathway = self.PATHWAYS["510k"]
        else:
            best_pathway = self.PATHWAYS["510k"]

        preemption = "Express preemption for PMA-approved devices (Riegel v. Medtronic). 510(k) devices not expressly preempted (Medtronic v. Lohr). Branded drugs not preempted for failure-to-warn (Wyeth v. Levine). Generic drugs preempted for failure-to-warn (PLIVA v. Mensing)."

        return FDARegulationResult(
            product_type=product_type,
            classification=best_pathway["name"],
            regulatory_pathway=best_pathway["description"],
            requirements=[
                f"Comply with {reg}" for reg in best_pathway["key_regulations"]
            ] + ["cGMP/QSR compliance required", "Pre-submission meeting recommended"],
            timeline_estimate=best_pathway["timeline"],
            key_regulations=best_pathway["key_regulations"],
            post_market_obligations=best_pathway["post_market"],
            preemption_analysis=preemption,
        )


# ============================================================================
# MEDICARE FRAUD DETECTOR
# ============================================================================

class MedicareFraudDetector:
    """Analyzes arrangements for Medicare fraud risk indicators."""

    RISK_INDICATORS: List[Dict[str, Any]] = [
        {"id": "FR-01", "indicator": "Compensation varies with volume or value of referrals", "statute": "42 USC 1320a-7b(b)", "weight": 0.9},
        {"id": "FR-02", "indicator": "Remuneration to physicians for referrals", "statute": "42 USC 1320a-7b(b)", "weight": 0.9},
        {"id": "FR-03", "indicator": "Physician self-referral for designated health services", "statute": "42 USC 1395nn", "weight": 0.85},
        {"id": "FR-04", "indicator": "Billing for services not rendered", "statute": "31 USC 3729", "weight": 1.0},
        {"id": "FR-05", "indicator": "Upcoding (billing at higher level than service provided)", "statute": "31 USC 3729", "weight": 0.9},
        {"id": "FR-06", "indicator": "Unbundling (billing separately for bundled services)", "statute": "31 USC 3729", "weight": 0.85},
        {"id": "FR-07", "indicator": "Medically unnecessary services ordered or provided", "statute": "42 USC 1320a-7a", "weight": 0.85},
        {"id": "FR-08", "indicator": "Compensation above fair market value for services", "statute": "42 USC 1320a-7b(b)", "weight": 0.8},
        {"id": "FR-09", "indicator": "Free or below-market items/services to referral sources", "statute": "42 USC 1320a-7b(b)", "weight": 0.85},
        {"id": "FR-10", "indicator": "Retention of identified overpayments beyond 60 days", "statute": "42 USC 1320a-7k(d)", "weight": 0.8},
        {"id": "FR-11", "indicator": "Excluded individuals involved in federal healthcare program", "statute": "42 USC 1320a-7", "weight": 0.95},
        {"id": "FR-12", "indicator": "Falsified documentation or medical records", "statute": "18 USC 1347", "weight": 1.0},
    ]

    def assess_risk(self, arrangement_facts: Dict[str, Any]) -> FraudRiskResult:
        """Assess fraud risk based on arrangement facts."""
        description = arrangement_facts.get("description", "").lower()
        triggered: List[Dict[str, Any]] = []

        indicator_keywords: Dict[str, List[str]] = {
            "FR-01": ["volume", "value", "per referral", "per click", "per patient sent"],
            "FR-02": ["payment for referral", "referral fee", "kickback", "remuneration"],
            "FR-03": ["self-referral", "own lab", "own imaging", "own clinic", "dhs"],
            "FR-04": ["not rendered", "phantom", "ghost patient", "fictitious"],
            "FR-05": ["upcoding", "higher level", "inflated", "level 5"],
            "FR-06": ["unbundling", "separate billing", "component billing"],
            "FR-07": ["unnecessary", "not medically necessary", "overutilization"],
            "FR-08": ["above market", "excessive compensation", "above fmv"],
            "FR-09": ["free", "below market", "complimentary", "no charge"],
            "FR-10": ["overpayment", "refund", "60 days", "identified overpayment"],
            "FR-11": ["excluded", "debarred", "OIG exclusion", "LEIE"],
            "FR-12": ["falsified", "forged", "fabricated", "altered records"],
        }

        for indicator in self.RISK_INDICATORS:
            keywords = indicator_keywords.get(indicator["id"], [])
            if any(kw in description for kw in keywords):
                triggered.append({
                    "indicator_id": indicator["id"],
                    "indicator": indicator["indicator"],
                    "statute": indicator["statute"],
                    "weight": indicator["weight"],
                })

        if triggered:
            risk_score = sum(t["weight"] for t in triggered) / len(triggered)
        else:
            risk_score = 0.1

        risk_level = "CRITICAL" if risk_score >= 0.9 else \
                     "HIGH" if risk_score >= 0.7 else \
                     "MEDIUM" if risk_score >= 0.4 else "LOW"

        statutes = list(set(t["statute"] for t in triggered))

        enforcement: Dict[str, Any] = {
            "fca_exposure": any(t["statute"] == "31 USC 3729" for t in triggered),
            "aks_exposure": any(t["statute"] == "42 USC 1320a-7b(b)" for t in triggered),
            "stark_exposure": any(t["statute"] == "42 USC 1395nn" for t in triggered),
            "criminal_exposure": any(t["statute"] == "18 USC 1347" for t in triggered),
            "exclusion_risk": any(t["indicator_id"] == "FR-11" for t in triggered),
        }

        recommendations: List[str] = []
        if enforcement["fca_exposure"]:
            recommendations.append("Evaluate voluntary self-disclosure to OIG. Treble damages and per-claim penalties create significant financial exposure.")
        if enforcement["aks_exposure"]:
            recommendations.append("Review arrangement against applicable AKS safe harbors. Consider restructuring to meet safe harbor requirements.")
        if enforcement["stark_exposure"]:
            recommendations.append("Map all physician financial relationships to applicable Stark Law exceptions. Consider CMS Self-Referral Disclosure Protocol.")
        if enforcement["exclusion_risk"]:
            recommendations.append("CRITICAL: Immediately screen all individuals and entities against OIG LEIE and SAM exclusion databases.")
        if not recommendations:
            recommendations.append("No significant fraud indicators detected. Maintain ongoing compliance monitoring.")

        return FraudRiskResult(
            risk_level=risk_level,
            risk_score=risk_score,
            indicators=triggered,
            applicable_statutes=statutes,
            enforcement_exposure=enforcement,
            recommendations=recommendations,
        )


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_SEARCH_INDEX: Optional[DoctrineSearchIndex] = None
_HIPAA_CHECKER: Optional[HIPAAComplianceChecker] = None
_MALPRACTICE_ANALYZER: Optional[MalpracticeAnalyzer] = None
_FDA_SEARCHER: Optional[FDARegulationSearcher] = None
_FRAUD_DETECTOR: Optional[MedicareFraudDetector] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the search index."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        _SEARCH_INDEX = DoctrineSearchIndex()
        logger.info("DoctrineSearchIndex created for LG14")
    return _SEARCH_INDEX


def get_hipaa_checker() -> HIPAAComplianceChecker:
    """Get or create the HIPAA compliance checker."""
    global _HIPAA_CHECKER
    if _HIPAA_CHECKER is None:
        _HIPAA_CHECKER = HIPAAComplianceChecker()
    return _HIPAA_CHECKER


def get_malpractice_analyzer() -> MalpracticeAnalyzer:
    """Get or create the malpractice analyzer."""
    global _MALPRACTICE_ANALYZER
    if _MALPRACTICE_ANALYZER is None:
        _MALPRACTICE_ANALYZER = MalpracticeAnalyzer()
    return _MALPRACTICE_ANALYZER


def get_fda_searcher() -> FDARegulationSearcher:
    """Get or create the FDA regulation searcher."""
    global _FDA_SEARCHER
    if _FDA_SEARCHER is None:
        _FDA_SEARCHER = FDARegulationSearcher()
    return _FDA_SEARCHER


def get_fraud_detector() -> MedicareFraudDetector:
    """Get or create the Medicare fraud detector."""
    global _FRAUD_DETECTOR
    if _FRAUD_DETECTOR is None:
        _FRAUD_DETECTOR = MedicareFraudDetector()
    return _FRAUD_DETECTOR


def compute_query_hash(query: str) -> str:
    """Compute SHA-256 hash of a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
