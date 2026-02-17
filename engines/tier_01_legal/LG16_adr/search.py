"""
LG16 ADR Engine - Search Module
===================================
TF-IDF based vector search over ADR doctrine blocks, arbitration rules,
mediation processes, clause analysis, and dispute resolution references.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - ArbitrationRulesSearcher: search across AAA/JAMS/ICC/UNCITRAL/ICSID/FINRA rules
    - AwardEnforceabilityChecker: analyze award enforcement under FAA and NY Convention
    - ClauseValidator: validate arbitration clause completeness and unconscionability
    - DisputeResolutionAdvisor: recommend ADR process based on dispute characteristics

Version: 2.0.0
Engine: LG16 ADR Engine
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
    adr_category: str
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
            "adr_category": self.adr_category,
            "jurisdiction": self.jurisdiction,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# ARBITRATION RULES RESULT
# ============================================================================

@dataclass
class ArbitrationRulesResult:
    """Result of an arbitration rules search."""
    institution: str
    rule_set: str
    applicable_rules: List[Dict[str, Any]]
    filing_requirements: List[str]
    fee_schedule: Dict[str, Any]
    arbitrator_selection: str
    timeline_estimate: str
    discovery_provisions: str
    appeal_mechanism: str
    emergency_provisions: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "institution": self.institution,
            "rule_set": self.rule_set,
            "applicable_rules": self.applicable_rules,
            "filing_requirements": self.filing_requirements,
            "fee_schedule": self.fee_schedule,
            "arbitrator_selection": self.arbitrator_selection,
            "timeline_estimate": self.timeline_estimate,
            "discovery_provisions": self.discovery_provisions,
            "appeal_mechanism": self.appeal_mechanism,
            "emergency_provisions": self.emergency_provisions,
        }


# ============================================================================
# AWARD ENFORCEABILITY RESULT
# ============================================================================

@dataclass
class AwardEnforceabilityResult:
    """Result of an award enforceability analysis."""
    enforceable: bool
    enforcement_framework: str
    vacatur_grounds_present: List[Dict[str, str]]
    modification_grounds_present: List[Dict[str, str]]
    new_york_convention_defenses: List[Dict[str, str]]
    confirmation_requirements: List[str]
    risk_assessment: str
    recommended_actions: List[str]
    statute_of_limitations: str
    procedural_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "enforceable": self.enforceable,
            "enforcement_framework": self.enforcement_framework,
            "vacatur_grounds_present": self.vacatur_grounds_present,
            "modification_grounds_present": self.modification_grounds_present,
            "new_york_convention_defenses": self.new_york_convention_defenses,
            "confirmation_requirements": self.confirmation_requirements,
            "risk_assessment": self.risk_assessment,
            "recommended_actions": self.recommended_actions,
            "statute_of_limitations": self.statute_of_limitations,
            "procedural_notes": self.procedural_notes,
        }


# ============================================================================
# CLAUSE VALIDATION RESULT
# ============================================================================

@dataclass
class ClauseValidationResult:
    """Result of an arbitration clause validation."""
    overall_valid: bool
    completeness_score: float
    elements_present: Dict[str, bool]
    missing_elements: List[str]
    unconscionability_risks: List[Dict[str, str]]
    pathological_issues: List[Dict[str, str]]
    enforceability_assessment: str
    recommendations: List[str]
    model_clause_suggestion: str
    severability_analysis: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "overall_valid": self.overall_valid,
            "completeness_score": round(self.completeness_score, 4),
            "elements_present": self.elements_present,
            "missing_elements": self.missing_elements,
            "unconscionability_risks": self.unconscionability_risks,
            "pathological_issues": self.pathological_issues,
            "enforceability_assessment": self.enforceability_assessment,
            "recommendations": self.recommendations,
            "model_clause_suggestion": self.model_clause_suggestion,
            "severability_analysis": self.severability_analysis,
        }


# ============================================================================
# DISPUTE RESOLUTION ADVISORY RESULT
# ============================================================================

@dataclass
class DisputeResolutionAdvisory:
    """Result of a dispute resolution process recommendation."""
    recommended_process: str
    recommended_institution: str
    alternative_processes: List[Dict[str, Any]]
    rationale: List[str]
    estimated_cost_range: Dict[str, Any]
    estimated_duration: str
    confidentiality_level: str
    binding_nature: str
    preserves_relationship: bool
    recommended_rules: str
    clause_language: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "recommended_process": self.recommended_process,
            "recommended_institution": self.recommended_institution,
            "alternative_processes": self.alternative_processes,
            "rationale": self.rationale,
            "estimated_cost_range": self.estimated_cost_range,
            "estimated_duration": self.estimated_duration,
            "confidentiality_level": self.confidentiality_level,
            "binding_nature": self.binding_nature,
            "preserves_relationship": self.preserves_relationship,
            "recommended_rules": self.recommended_rules,
            "clause_language": self.clause_language,
        }


# ============================================================================
# TF-IDF SEARCH INDEX
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index over ADR doctrine blocks."""

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
        adr_category: str,
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
            "adr_category": adr_category,
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
        adr_category_filter: Optional[str] = None,
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

        if adr_category_filter:
            candidate_docs = {
                doc_id for doc_id in candidate_docs
                if self._documents[doc_id]["adr_category"] == adr_category_filter
            }

        if jurisdiction_filter:
            candidate_docs = {
                doc_id for doc_id in candidate_docs
                if self._documents[doc_id]["jurisdiction"] in (None, "federal", "international", jurisdiction_filter)
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
                    adr_category=doc_info["adr_category"],
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
# ARBITRATION RULES SEARCHER
# ============================================================================

class ArbitrationRulesSearcher:
    """Search across AAA/JAMS/ICC/UNCITRAL/ICSID/FINRA rules by topic, dispute type, amount."""

    INSTITUTION_RULES: Dict[str, Dict[str, Any]] = {
        "aaa_commercial": {
            "institution": "American Arbitration Association",
            "rule_set": "AAA Commercial Arbitration Rules (2013, as amended)",
            "dispute_types": ["commercial", "business", "contract", "partnership", "franchise", "construction", "real_estate"],
            "amount_thresholds": {"expedited": 100_000, "standard": 10_000_000, "large_complex": 10_000_001},
            "filing_requirements": [
                "Demand for Arbitration with copy of arbitration agreement",
                "Filing fee per AAA fee schedule (based on claim amount)",
                "Brief statement of dispute and relief sought",
                "Names, addresses, and contact info of all parties",
                "Copy of arbitration clause or separate agreement",
            ],
            "arbitrator_selection": "List method: AAA sends list of 10-15 arbitrators; parties strike and rank; AAA appoints from remaining. For large/complex: panel of 3.",
            "timeline": "Expedited (<$100K): 45-60 days hearing, 14 days to award. Standard: 6-12 months. Large/complex: 12-18 months.",
            "discovery": "Limited exchange of documents relevant to dispute. Depositions generally not allowed unless arbitrator grants for good cause. R-22(b).",
            "appeal": "AAA Optional Appellate Arbitration Rules allow appeal to three-arbitrator panel for error of law or clearly erroneous findings of fact.",
            "emergency": "Emergency Measures of Protection available within 24 hours. Emergency arbitrator appointed from special panel. R-38.",
            "fee_schedule": {"filing_min": 1975, "filing_max": 65_000, "hearing_daily": 1500, "admin_percent": 0.0},
            "rules": [
                {"rule_id": "R-1", "title": "Agreement of Parties", "summary": "Parties deemed to have agreed to the rules by incorporating AAA arbitration clause."},
                {"rule_id": "R-4", "title": "Filing Requirements", "summary": "Demand must include brief statement of dispute, amount, remedy, and hearing locale."},
                {"rule_id": "R-7", "title": "Consolidation", "summary": "Arbitrator may consolidate proceedings involving common questions of law or fact."},
                {"rule_id": "R-12", "title": "Appointment from National Roster", "summary": "AAA maintains national roster and appoints from proposed list."},
                {"rule_id": "R-17", "title": "Disclosure", "summary": "Arbitrator must disclose any circumstance likely to give rise to justifiable doubt regarding impartiality."},
                {"rule_id": "R-22", "title": "Exchange of Information", "summary": "Arbitrator manages exchange of information consistent with goal of just, efficient resolution."},
                {"rule_id": "R-34", "title": "Interim Measures", "summary": "Arbitrator may grant interim relief deemed necessary, including injunctive and conservatory measures."},
                {"rule_id": "R-47", "title": "Form of Award", "summary": "Award shall be in writing, signed, with brief statement of reasons unless parties agree otherwise."},
            ],
        },
        "aaa_employment": {
            "institution": "American Arbitration Association",
            "rule_set": "AAA Employment Arbitration Rules (2009, as amended)",
            "dispute_types": ["employment", "discrimination", "wrongful_termination", "wage_dispute", "harassment", "retaliation"],
            "amount_thresholds": {"standard": 0, "complex": 250_000},
            "filing_requirements": [
                "Demand for Arbitration describing nature of dispute",
                "Filing fee: employee $200, employer $1900",
                "Copy of arbitration agreement",
                "Names and addresses of parties",
            ],
            "arbitrator_selection": "AAA sends list of 7-11 neutral arbitrators with bios; parties strike and rank; AAA appoints most mutually acceptable. Due process protections per employer promulgated rules.",
            "timeline": "Standard: 4-8 months. Complex: 8-14 months.",
            "discovery": "Broader than commercial: each party may take at least one deposition. Document exchange is standard. Arbitrator manages scope consistent with due process.",
            "appeal": "Generally no appeal mechanism. Federal courts review under FAA Section 10 limited vacatur standard.",
            "emergency": "Emergency measures available. Emergency arbitrator from special panel appointed within 1 business day.",
            "fee_schedule": {"employee_filing": 200, "employer_filing": 1900, "hearing_daily": 1500, "admin_flat": 750},
            "rules": [
                {"rule_id": "ER-1", "title": "Applicability", "summary": "Applies to disputes arising out of employment relationships or termination."},
                {"rule_id": "ER-9", "title": "Discovery", "summary": "Arbitrator shall have authority to order reasonable discovery including depositions and document production."},
                {"rule_id": "ER-14", "title": "Due Process", "summary": "Arbitrator must ensure that employer-promulgated plans provide minimum due process protections."},
                {"rule_id": "ER-39", "title": "Remedies", "summary": "Arbitrator may grant any remedy available under applicable law including reinstatement and compensatory damages."},
            ],
        },
        "jams_comprehensive": {
            "institution": "JAMS",
            "rule_set": "JAMS Comprehensive Arbitration Rules & Procedures (2024)",
            "dispute_types": ["commercial", "business", "employment", "construction", "IP", "partnership", "securities"],
            "amount_thresholds": {"streamlined": 250_000, "standard": 10_000_000, "complex": 10_000_001},
            "filing_requirements": [
                "Demand for Arbitration with brief description of dispute",
                "Filing fee: $1,750 (non-refundable)",
                "Copy of arbitration agreement",
                "Identification of all parties and representatives",
            ],
            "arbitrator_selection": "JAMS provides list of 5 arbitrators from its panel. Parties may strike up to 2 each. JAMS selects from remaining based on expertise, availability, and disclosed conflicts.",
            "timeline": "Streamlined (<$250K): 3-6 months. Standard: 6-12 months. Complex: 12-24 months.",
            "discovery": "Rule 17: Arbitrator may permit discovery sufficient to allow a fair hearing. Includes document requests and depositions. Scope at arbitrator's discretion.",
            "appeal": "JAMS Optional Arbitration Appeal Procedure: panel of 3 reviews for material errors of law or manifest disregard. Must be agreed in writing.",
            "emergency": "Rule 2(c): emergency relief request can be filed before or after commencement. Emergency arbitrator appointed expeditiously.",
            "fee_schedule": {"filing": 1750, "case_management": 500, "hearing_daily": 2500, "admin_percent": 0.0},
            "rules": [
                {"rule_id": "Rule 11", "title": "Arbitrator Selection", "summary": "JAMS provides list of 5; parties may strike 2; JAMS appoints from remaining."},
                {"rule_id": "Rule 15", "title": "Scheduling and Location", "summary": "Preliminary conference within 14 days of appointment to set schedule and hearing dates."},
                {"rule_id": "Rule 17", "title": "Exchange of Information", "summary": "Arbitrator controls scope and timing of discovery to ensure fair resolution."},
                {"rule_id": "Rule 24", "title": "Awards", "summary": "Final award within 30 days of close of hearing. Reasoned award unless parties agree otherwise."},
            ],
        },
        "icc_arbitration": {
            "institution": "International Chamber of Commerce",
            "rule_set": "ICC Rules of Arbitration (2021)",
            "dispute_types": ["international_commercial", "cross_border", "trade", "investment", "infrastructure", "energy", "construction"],
            "amount_thresholds": {"expedited": 3_000_000, "standard": 100_000_000, "complex": 100_000_001},
            "filing_requirements": [
                "Request for Arbitration to ICC Secretariat",
                "Filing fee: $5,000 (non-refundable)",
                "Full description of nature and circumstances of dispute",
                "Statement of relief sought with amounts",
                "Copy of arbitration agreement and relevant contracts",
                "Comments on number of arbitrators, seat, applicable law",
            ],
            "arbitrator_selection": "ICC Court appoints arbitrators. Sole arbitrator or panel of 3. Parties may nominate co-arbitrators; ICC Court confirms. Chair appointed by ICC Court if parties' co-arbitrators cannot agree.",
            "timeline": "Expedited (<$3M): 6 months from case management conference. Standard: 12-18 months. Complex: 18-36 months.",
            "discovery": "Art. 22: Tribunal may order production of documents. IBA Rules on the Taking of Evidence frequently adopted. No depositions as of right.",
            "appeal": "No appeal mechanism under ICC Rules. Award is final and binding. Subject to annulment at seat of arbitration.",
            "emergency": "Art. 29 + Appendix V: Emergency Arbitrator Provisions. Application within 24 hours. Decision within 15 days.",
            "fee_schedule": {"registration": 5000, "admin_min": 5000, "admin_max": 150_000, "arbitrator_hourly": 500},
            "rules": [
                {"rule_id": "Art. 6", "title": "Effect of Arbitration Agreement", "summary": "Agreement valid even if contract containing it is alleged null or nonexistent (separability)."},
                {"rule_id": "Art. 12", "title": "Constitution of Tribunal", "summary": "Default 3 arbitrators unless expedited procedure or agreement for sole."},
                {"rule_id": "Art. 22", "title": "Case Management", "summary": "Tribunal convenes case management conference; establishes procedural timetable."},
                {"rule_id": "Art. 29", "title": "Emergency Arbitrator", "summary": "Available before constitution of tribunal for urgent interim/conservatory measures."},
                {"rule_id": "Art. 36", "title": "Scrutiny of Award", "summary": "ICC Court reviews all awards for form and substance before signing."},
            ],
        },
        "uncitral_2021": {
            "institution": "UNCITRAL",
            "rule_set": "UNCITRAL Arbitration Rules (2021 revision)",
            "dispute_types": ["international_commercial", "investment", "trade", "infrastructure", "ad_hoc", "treaty"],
            "amount_thresholds": {"standard": 0, "complex": 50_000_000},
            "filing_requirements": [
                "Notice of Arbitration to respondent",
                "No institutional filing fee (ad hoc rules)",
                "Brief description of claim and amounts",
                "Proposal regarding number of arbitrators",
                "Proposal on language and seat of arbitration",
            ],
            "arbitrator_selection": "Ad hoc: parties directly appoint. Default sole arbitrator unless parties agree on 3. Appointing authority (e.g., PCA Secretary-General) acts if parties cannot agree.",
            "timeline": "Flexible: typically 12-24 months depending on complexity and cooperation of parties.",
            "discovery": "Art. 27: Tribunal may require production of documents or other evidence. IBA Rules frequently adopted by reference.",
            "appeal": "None under rules. Award is final. Subject to annulment at seat under local arbitration law.",
            "emergency": "Art. 26: Interim measures available from tribunal. No formal emergency arbitrator procedure in UNCITRAL Rules (unlike institutional rules).",
            "fee_schedule": {"filing": 0, "arbitrator_hourly_typical": 400, "admin_appointing_authority": 2000, "hearing_room": 0},
            "rules": [
                {"rule_id": "Art. 1", "title": "Scope of Application", "summary": "Parties may agree to ad hoc arbitration under these rules without any institution."},
                {"rule_id": "Art. 17", "title": "General Provisions on Procedure", "summary": "Tribunal may conduct arbitration as it considers appropriate, ensuring equal treatment and reasonable opportunity to present case."},
                {"rule_id": "Art. 26", "title": "Interim Measures", "summary": "Tribunal may grant interim measures it deems necessary in respect of the subject matter of the dispute."},
                {"rule_id": "Art. 34", "title": "Form and Effect of Award", "summary": "Award in writing, signed, stating reasons. Final and binding."},
            ],
        },
        "icsid_convention": {
            "institution": "ICSID (World Bank)",
            "rule_set": "ICSID Convention Arbitration Rules (2022 amended)",
            "dispute_types": ["investor_state", "bilateral_investment_treaty", "investment", "sovereign", "expropriation", "concession"],
            "amount_thresholds": {"standard": 0, "typical_minimum": 10_000_000},
            "filing_requirements": [
                "Request for Arbitration to ICSID Secretary-General",
                "Registration fee: $25,000",
                "Identification of parties and nationality of investor",
                "Consent to jurisdiction (treaty or contract)",
                "Summary of dispute and amounts claimed",
            ],
            "arbitrator_selection": "Panel of 3 unless agreed otherwise. Each party appoints 1; parties agree on president, or ICSID Chairman appoints. Arbitrators must be from ICSID Panel of Arbitrators or meet qualifications.",
            "timeline": "18-36 months typical. Post-hearing briefs: 60-90 days. Deliberation: 120 days. Award rendered average 3.5 years from registration.",
            "discovery": "Rule 36 (2022): Tribunal manages document production. Witness statements and expert reports standard. Oral examination at hearing.",
            "appeal": "ICSID Annulment Committee (Art. 52): may annul for improper constitution, excess of powers, failure to state reasons, corruption, or serious departure from fundamental rule of procedure.",
            "emergency": "Rule 47 (2022): Provisional Measures available from tribunal. Also party may seek measures from domestic courts without waiving arbitration agreement.",
            "fee_schedule": {"registration": 25_000, "annual_admin": 42_000, "arbitrator_daily": 3000, "secretary_hourly": 200},
            "rules": [
                {"rule_id": "Art. 25", "title": "Jurisdiction", "summary": "Jurisdiction requires legal dispute, investment, between Contracting State and national of another Contracting State, written consent."},
                {"rule_id": "Art. 42", "title": "Applicable Law", "summary": "Tribunal applies law agreed by parties. In absence of agreement, law of host State and applicable rules of international law."},
                {"rule_id": "Art. 52", "title": "Annulment", "summary": "Either party may request annulment on five enumerated grounds within 120 days of award."},
                {"rule_id": "Art. 54", "title": "Enforcement", "summary": "Each Contracting State shall recognize and enforce pecuniary obligations of award as if final judgment of its courts."},
            ],
        },
        "finra_customer": {
            "institution": "FINRA (Financial Industry Regulatory Authority)",
            "rule_set": "FINRA Code of Arbitration Procedure for Customer Disputes (12000 Series)",
            "dispute_types": ["securities", "broker_dealer", "investment_fraud", "churning", "suitability", "margin", "unauthorized_trading"],
            "amount_thresholds": {"simplified": 50_000, "standard": 100_000, "large": 100_001},
            "filing_requirements": [
                "Statement of Claim filed through FINRA DR Portal",
                "Filing fee based on claim amount ($50-$2,225)",
                "Description of dispute and all relevant facts",
                "Relief sought with specific dollar amounts",
                "Identification of all parties (account holders, firms, registered reps)",
            ],
            "arbitrator_selection": "FINRA Neutral List Selection System (NLSS): computer-generated lists from FINRA roster. Simplified (<$50K): 1 public arbitrator. Standard ($50-100K): 1 public arbitrator. Large (>$100K): 3 arbitrators (2 public, 1 industry unless all-public panel elected by customer).",
            "timeline": "Simplified: 4-6 months (paper only). Standard: 10-14 months. Large: 14-18 months.",
            "discovery": "Discovery Guide: 13 standard document production lists. Parties must produce listed documents without request. Additional discovery at arbitrator's discretion.",
            "appeal": "None within FINRA. Judicial review under FAA Section 10 vacatur standard. Very limited grounds.",
            "emergency": "Temporary Injunctive Relief available through FINRA or court pending arbitration.",
            "fee_schedule": {"claimant_filing_min": 50, "claimant_filing_max": 2225, "forum_fee_per_session": 750, "member_surcharge": 1900},
            "rules": [
                {"rule_id": "12200", "title": "Required Submission", "summary": "Disputes between customer and member or associated person must be arbitrated if customer requests."},
                {"rule_id": "12206", "title": "Time Limits", "summary": "6-year eligibility rule: no claim shall be eligible if event giving rise to claim occurred more than 6 years before filing."},
                {"rule_id": "12403", "title": "Party Selection", "summary": "FINRA generates lists via NLSS; parties may strike and rank."},
                {"rule_id": "12506", "title": "Discovery", "summary": "Parties must produce documents per Discovery Guide without formal request."},
            ],
        },
    }

    def search_rules(
        self,
        dispute_type: str,
        institution: Optional[str] = None,
        amount_in_dispute: Optional[float] = None,
        topic_keywords: Optional[List[str]] = None,
    ) -> List[ArbitrationRulesResult]:
        """Search arbitration rules by dispute type, institution, and amount."""
        results: List[ArbitrationRulesResult] = []
        dispute_lower = dispute_type.lower().strip()
        topic_lower = [kw.lower() for kw in (topic_keywords or [])]

        for rule_key, rule_data in self.INSTITUTION_RULES.items():
            if institution and institution.lower() not in rule_key.lower() and institution.lower() not in rule_data["institution"].lower():
                continue

            type_match = any(dt in dispute_lower or dispute_lower in dt for dt in rule_data["dispute_types"])
            topic_match = not topic_lower or any(
                kw in rule_data["rule_set"].lower() or
                any(kw in r.get("summary", "").lower() for r in rule_data["rules"])
                for kw in topic_lower
            )

            if type_match or topic_match:
                applicable_rules = rule_data["rules"]
                if topic_lower:
                    scored_rules = []
                    for rule in applicable_rules:
                        rule_text = (rule.get("title", "") + " " + rule.get("summary", "")).lower()
                        match_count = sum(1 for kw in topic_lower if kw in rule_text)
                        scored_rules.append((match_count, rule))
                    scored_rules.sort(key=lambda x: x[0], reverse=True)
                    applicable_rules = [r for _, r in scored_rules]

                tier = "standard"
                if amount_in_dispute is not None:
                    thresholds = rule_data["amount_thresholds"]
                    sorted_thresholds = sorted(thresholds.items(), key=lambda x: x[1])
                    for tier_name, threshold in sorted_thresholds:
                        if amount_in_dispute <= threshold:
                            tier = tier_name
                            break
                    else:
                        tier = sorted_thresholds[-1][0] if sorted_thresholds else "standard"

                results.append(ArbitrationRulesResult(
                    institution=rule_data["institution"],
                    rule_set=rule_data["rule_set"],
                    applicable_rules=applicable_rules,
                    filing_requirements=rule_data["filing_requirements"],
                    fee_schedule=rule_data["fee_schedule"],
                    arbitrator_selection=rule_data["arbitrator_selection"],
                    timeline_estimate=rule_data["timeline"],
                    discovery_provisions=rule_data["discovery"],
                    appeal_mechanism=rule_data["appeal"],
                    emergency_provisions=rule_data["emergency"],
                ))

        logger.info(f"ArbitrationRulesSearcher found {len(results)} matching rule sets for dispute_type={dispute_type}")
        return results


# ============================================================================
# AWARD ENFORCEABILITY CHECKER
# ============================================================================

class AwardEnforceabilityChecker:
    """Analyze award enforcement under FAA Section 9 and New York Convention Article V."""

    FAA_SECTION_10_GROUNDS: List[Dict[str, str]] = [
        {"ground": "corruption", "section": "FAA 9 USC 10(a)(1)", "description": "Award procured by corruption, fraud, or undue means",
         "indicators": ["bribe", "fraud", "corruption", "undue means", "perjury", "falsified evidence", "concealment"]},
        {"ground": "evident_partiality", "section": "FAA 9 USC 10(a)(2)", "description": "Evident partiality or corruption in the arbitrators",
         "indicators": ["undisclosed relationship", "bias", "partiality", "conflict of interest", "financial interest", "prior representation"]},
        {"ground": "misconduct", "section": "FAA 9 USC 10(a)(3)", "description": "Arbitrators guilty of misconduct in refusing to hear evidence pertinent and material, or other misbehavior prejudicing rights of party",
         "indicators": ["refused evidence", "denied hearing", "ex parte communication", "procedural irregularity", "no notice", "denied continuance"]},
        {"ground": "excess_powers", "section": "FAA 9 USC 10(a)(4)", "description": "Arbitrators exceeded their powers or so imperfectly executed them that a mutual, final, and definite award was not made",
         "indicators": ["exceeded scope", "beyond agreement", "punitive damages not authorized", "class action not permitted", "indefinite award", "ambiguous relief"]},
    ]

    FAA_SECTION_11_GROUNDS: List[Dict[str, str]] = [
        {"ground": "material_miscalculation", "section": "FAA 9 USC 11(a)", "description": "Evident material miscalculation of figures or evident material mistake in description of person, thing, or property",
         "indicators": ["math error", "miscalculation", "wrong party named", "wrong property", "clerical error"]},
        {"ground": "excess_matter", "section": "FAA 9 USC 11(b)", "description": "Arbitrators have awarded upon a matter not submitted to them",
         "indicators": ["not submitted", "outside scope", "unpled claim", "exceeded submission"]},
        {"ground": "imperfect_form", "section": "FAA 9 USC 11(c)", "description": "Award is imperfect in matter of form not affecting merits",
         "indicators": ["formatting", "signature missing", "date error", "imperfect form"]},
    ]

    NY_CONVENTION_ART_V_DEFENSES: List[Dict[str, str]] = [
        {"defense": "incapacity_invalid_agreement", "article": "Art. V(1)(a)", "description": "Parties were under some incapacity or agreement is not valid under applicable law",
         "indicators": ["incapacity", "minor", "invalid agreement", "void", "not valid", "no authority"]},
        {"defense": "no_proper_notice", "article": "Art. V(1)(b)", "description": "Party not given proper notice of arbitrator appointment or proceedings, or unable to present case",
         "indicators": ["no notice", "inadequate notice", "unable to present", "denied hearing", "due process"]},
        {"defense": "excess_scope", "article": "Art. V(1)(c)", "description": "Award deals with matters beyond scope of submission to arbitration",
         "indicators": ["beyond scope", "not contemplated", "outside agreement", "exceeded submission"]},
        {"defense": "improper_composition", "article": "Art. V(1)(d)", "description": "Composition of tribunal or procedure not in accordance with agreement or law of seat",
         "indicators": ["wrong procedure", "tribunal composition", "not in accordance", "seat law violated"]},
        {"defense": "not_binding_set_aside", "article": "Art. V(1)(e)", "description": "Award not yet binding or has been set aside or suspended by authority of country where made",
         "indicators": ["set aside", "annulled", "suspended", "not binding", "vacated at seat"]},
        {"defense": "not_arbitrable", "article": "Art. V(2)(a)", "description": "Subject matter not capable of settlement by arbitration under enforcement country law",
         "indicators": ["not arbitrable", "non-arbitrable", "public policy subject", "statutory right"]},
        {"defense": "public_policy", "article": "Art. V(2)(b)", "description": "Recognition or enforcement would be contrary to public policy of enforcement country",
         "indicators": ["public policy", "contrary to policy", "fundamental rights", "due process violation"]},
    ]

    def check_enforceability(self, award_facts: Dict[str, Any]) -> AwardEnforceabilityResult:
        """Analyze whether an arbitration award is enforceable."""
        description = award_facts.get("description", "").lower()
        is_international = award_facts.get("international", False)
        seat = award_facts.get("seat", "")
        enforcement_country = award_facts.get("enforcement_country", "US")

        vacatur_grounds: List[Dict[str, str]] = []
        for ground in self.FAA_SECTION_10_GROUNDS:
            if any(ind in description for ind in ground["indicators"]):
                vacatur_grounds.append({
                    "ground": ground["ground"],
                    "section": ground["section"],
                    "description": ground["description"],
                })

        modification_grounds: List[Dict[str, str]] = []
        for ground in self.FAA_SECTION_11_GROUNDS:
            if any(ind in description for ind in ground["indicators"]):
                modification_grounds.append({
                    "ground": ground["ground"],
                    "section": ground["section"],
                    "description": ground["description"],
                })

        nyc_defenses: List[Dict[str, str]] = []
        if is_international:
            for defense in self.NY_CONVENTION_ART_V_DEFENSES:
                if any(ind in description for ind in defense["indicators"]):
                    nyc_defenses.append({
                        "defense": defense["defense"],
                        "article": defense["article"],
                        "description": defense["description"],
                    })

        enforceable = len(vacatur_grounds) == 0 and (not is_international or len(nyc_defenses) == 0)
        framework = "New York Convention (9 USC 201-208)" if is_international else "Federal Arbitration Act (9 USC 9-11)"

        if vacatur_grounds and nyc_defenses:
            risk = "HIGH"
        elif vacatur_grounds or nyc_defenses:
            risk = "MEDIUM"
        elif modification_grounds:
            risk = "LOW"
        else:
            risk = "MINIMAL"

        confirmation_reqs: List[str] = [
            "Application to confirm filed in federal or state court with jurisdiction",
            "Copy of arbitration agreement attached to application",
            "Copy of arbitration award attached to application",
        ]
        if is_international:
            confirmation_reqs.extend([
                "Authenticated original or certified copy of award (Art. IV NYC)",
                "Original or certified copy of arbitration agreement",
                "Translation if award not in English",
                "File within 3 years of award (9 USC 207)",
            ])
        else:
            confirmation_reqs.append("File within 1 year of award (9 USC 9)")

        sol = "Domestic: 1 year from award date (9 USC 9). Vacatur: 3 months from award (9 USC 12). International (NYC): 3 years (9 USC 207)."

        actions: List[str] = []
        if not enforceable:
            actions.append("Evaluate strength of vacatur/non-enforcement grounds before opposing confirmation")
            actions.append("Consider whether modification under FAA Section 11 is more appropriate than vacatur")
        if vacatur_grounds:
            actions.append("File motion to vacate within 3-month window under 9 USC 12")
            actions.append("Gather evidence supporting each vacatur ground identified")
        if nyc_defenses:
            actions.append("Prepare defense under Art. V at enforcement jurisdiction")
            actions.append("Consider whether award can be challenged at seat of arbitration")
        if not vacatur_grounds and not nyc_defenses:
            actions.append("Proceed with confirmation application promptly to preserve rights")
            actions.append("Identify proper court for confirmation (FAA 9 USC 9 or 207)")

        procedural: List[str] = [
            "Verify award is mutual, final, and definite before seeking confirmation",
            "Check whether arbitration agreement specifies court for confirmation",
            "Consider state vs. federal court for confirmation (removal possible under 9 USC 205 for international)",
            "If challenging: evaluate manifest disregard of law (judicially created ground, circuit split on viability post-Hall Street)",
        ]

        logger.info(f"AwardEnforceabilityChecker: enforceable={enforceable}, risk={risk}, vacatur_grounds={len(vacatur_grounds)}, nyc_defenses={len(nyc_defenses)}")

        return AwardEnforceabilityResult(
            enforceable=enforceable,
            enforcement_framework=framework,
            vacatur_grounds_present=vacatur_grounds,
            modification_grounds_present=modification_grounds,
            new_york_convention_defenses=nyc_defenses,
            confirmation_requirements=confirmation_reqs,
            risk_assessment=risk,
            recommended_actions=actions,
            statute_of_limitations=sol,
            procedural_notes=procedural,
        )


# ============================================================================
# CLAUSE VALIDATOR
# ============================================================================

class ClauseValidator:
    """Validate arbitration clause completeness and flag unconscionability risks."""

    ESSENTIAL_ELEMENTS: Dict[str, Dict[str, Any]] = {
        "scope": {
            "description": "Scope of disputes covered (arising out of, relating to, or in connection with)",
            "weight": 0.15,
            "keywords": ["arising out of", "relating to", "in connection with", "all disputes", "any controversy", "any claim"],
        },
        "seat": {
            "description": "Seat (place/venue) of arbitration",
            "weight": 0.12,
            "keywords": ["seat", "venue", "place of arbitration", "location", "city", "state"],
        },
        "rules": {
            "description": "Governing arbitration rules (AAA, JAMS, ICC, UNCITRAL, etc.)",
            "weight": 0.15,
            "keywords": ["aaa", "jams", "icc", "uncitral", "icsid", "finra", "rules", "procedures", "administered by"],
        },
        "governing_law": {
            "description": "Governing law / choice of law",
            "weight": 0.10,
            "keywords": ["governing law", "governed by", "laws of", "applicable law", "choice of law"],
        },
        "arbitrator_count": {
            "description": "Number of arbitrators (1 or 3)",
            "weight": 0.10,
            "keywords": ["sole arbitrator", "single arbitrator", "one arbitrator", "three arbitrators", "panel of three", "panel of 3", "tribunal of three"],
        },
        "language": {
            "description": "Language of arbitration proceedings",
            "weight": 0.08,
            "keywords": ["language", "conducted in english", "in the english language", "proceedings shall be in"],
        },
        "binding": {
            "description": "Statement that arbitration is final and binding",
            "weight": 0.10,
            "keywords": ["final and binding", "binding arbitration", "final award", "no appeal"],
        },
        "class_waiver": {
            "description": "Class action waiver (if applicable)",
            "weight": 0.05,
            "keywords": ["class action", "class arbitration", "waiver", "individual basis", "no class", "no representative"],
        },
        "confidentiality": {
            "description": "Confidentiality provisions",
            "weight": 0.05,
            "keywords": ["confidential", "confidentiality", "not disclose", "private", "non-disclosure"],
        },
        "costs": {
            "description": "Cost allocation / fee shifting provisions",
            "weight": 0.05,
            "keywords": ["costs", "fees", "expenses", "prevailing party", "fee shifting", "each party shall bear"],
        },
        "limitation_period": {
            "description": "Limitation period for filing claims",
            "weight": 0.05,
            "keywords": ["limitation", "time limit", "statute of limitations", "within one year", "within two years", "filing deadline"],
        },
    }

    UNCONSCIONABILITY_INDICATORS: List[Dict[str, Any]] = [
        {"id": "UC-01", "type": "procedural", "description": "Take-it-or-leave-it adhesion contract with no negotiation opportunity",
         "keywords": ["adhesion", "non-negotiable", "standard form", "take it or leave it"],
         "severity": "MEDIUM"},
        {"id": "UC-02", "type": "procedural", "description": "Arbitration clause buried in fine print or lengthy document",
         "keywords": ["fine print", "buried", "hidden", "inconspicuous", "small print"],
         "severity": "MEDIUM"},
        {"id": "UC-03", "type": "substantive", "description": "Excessive costs or fees imposed on weaker party",
         "keywords": ["excessive fees", "prohibitive cost", "unaffordable", "high filing fee"],
         "severity": "HIGH"},
        {"id": "UC-04", "type": "substantive", "description": "One-sided selection of arbitration forum or rules favoring drafter",
         "keywords": ["drafter selects", "one party chooses", "sole discretion", "unilateral selection"],
         "severity": "HIGH"},
        {"id": "UC-05", "type": "substantive", "description": "Waiver of substantive statutory rights or remedies",
         "keywords": ["waive rights", "no punitive", "cap damages", "limitation of remedies", "no statutory damages"],
         "severity": "HIGH"},
        {"id": "UC-06", "type": "substantive", "description": "Unreasonably short limitation period for claims",
         "keywords": ["30 days", "60 days", "90 days", "shortened limitation", "reduced period"],
         "severity": "HIGH"},
        {"id": "UC-07", "type": "procedural", "description": "Prohibitively inconvenient forum location",
         "keywords": ["distant forum", "inconvenient location", "remote venue", "across country"],
         "severity": "MEDIUM"},
        {"id": "UC-08", "type": "substantive", "description": "Carve-out allowing drafter to pursue claims in court while requiring other party to arbitrate",
         "keywords": ["carve-out", "exception for", "may pursue in court", "unilateral option"],
         "severity": "HIGH"},
        {"id": "UC-09", "type": "procedural", "description": "No meaningful opt-out opportunity",
         "keywords": ["no opt out", "no option", "mandatory", "compulsory", "cannot decline"],
         "severity": "MEDIUM"},
        {"id": "UC-10", "type": "substantive", "description": "Confidentiality provision prevents public accountability",
         "keywords": ["strict confidentiality", "cannot disclose", "gag clause", "no public disclosure"],
         "severity": "LOW"},
    ]

    PATHOLOGICAL_CLAUSE_ISSUES: List[Dict[str, Any]] = [
        {"id": "PC-01", "description": "Names non-existent or defunct institution",
         "keywords": ["national arbitration forum", "defunct institution", "non-existent body"],
         "severity": "CRITICAL"},
        {"id": "PC-02", "description": "Contradictory provisions (e.g., binding arbitration + right to jury trial)",
         "keywords": ["jury trial", "court action", "contradictory", "inconsistent"],
         "severity": "CRITICAL"},
        {"id": "PC-03", "description": "Ambiguous scope (unclear what disputes are covered)",
         "keywords": ["may arbitrate", "option to arbitrate", "either party may elect"],
         "severity": "HIGH"},
        {"id": "PC-04", "description": "References multiple conflicting rule sets",
         "keywords": ["aaa and jams", "icc or uncitral", "conflicting rules"],
         "severity": "HIGH"},
        {"id": "PC-05", "description": "Specifies impossible conditions for arbitration",
         "keywords": ["must agree on arbitrator", "unanimous selection", "impossible condition"],
         "severity": "HIGH"},
        {"id": "PC-06", "description": "Missing or incompatible seat designation for international arbitration",
         "keywords": ["no seat", "no venue", "international without seat"],
         "severity": "HIGH"},
    ]

    def validate_clause(self, clause_text: str, context: Optional[Dict[str, Any]] = None) -> ClauseValidationResult:
        """Validate an arbitration clause for completeness and enforceability."""
        clause_lower = clause_text.lower()
        ctx = context or {}
        is_consumer = ctx.get("consumer", False)
        is_employment = ctx.get("employment", False)
        is_international = ctx.get("international", False)

        elements_present: Dict[str, bool] = {}
        completeness_total = 0.0

        for element_key, element_info in self.ESSENTIAL_ELEMENTS.items():
            present = any(kw in clause_lower for kw in element_info["keywords"])
            elements_present[element_key] = present
            if present:
                completeness_total += element_info["weight"]

        missing = [
            self.ESSENTIAL_ELEMENTS[k]["description"]
            for k, v in elements_present.items() if not v
        ]

        unconscionability_risks: List[Dict[str, str]] = []
        for indicator in self.UNCONSCIONABILITY_INDICATORS:
            if any(kw in clause_lower for kw in indicator["keywords"]):
                unconscionability_risks.append({
                    "id": indicator["id"],
                    "type": indicator["type"],
                    "description": indicator["description"],
                    "severity": indicator["severity"],
                })

        if is_consumer or is_employment:
            if not elements_present.get("costs"):
                unconscionability_risks.append({
                    "id": "UC-CTX-01",
                    "type": "substantive",
                    "description": "Consumer/employment clause should address cost allocation to avoid prohibitive cost challenge (Green Tree v. Randolph)",
                    "severity": "MEDIUM",
                })

        pathological: List[Dict[str, str]] = []
        for issue in self.PATHOLOGICAL_CLAUSE_ISSUES:
            if any(kw in clause_lower for kw in issue["keywords"]):
                pathological.append({
                    "id": issue["id"],
                    "description": issue["description"],
                    "severity": issue["severity"],
                })

        if is_international and not elements_present.get("seat"):
            pathological.append({
                "id": "PC-INT-01",
                "description": "International arbitration clause must specify seat to determine procedural law and annulment jurisdiction",
                "severity": "CRITICAL",
            })

        critical_pathological = any(p["severity"] == "CRITICAL" for p in pathological)
        high_unconscionability = sum(1 for u in unconscionability_risks if u["severity"] == "HIGH")
        overall_valid = completeness_total >= 0.50 and not critical_pathological and high_unconscionability < 3

        if critical_pathological:
            enforceability = "UNENFORCEABLE: Critical pathological issues render clause inoperative"
        elif high_unconscionability >= 3:
            enforceability = "HIGH RISK: Multiple substantive unconscionability indicators present"
        elif completeness_total < 0.30:
            enforceability = "WEAK: Clause lacks essential elements; may fail to compel arbitration"
        elif completeness_total < 0.50:
            enforceability = "MODERATE: Missing important elements; court may need to fill gaps"
        elif unconscionability_risks:
            enforceability = "ENFORCEABLE WITH RISK: Clause is substantively complete but has unconscionability risk factors"
        else:
            enforceability = "STRONG: Clause contains essential elements with no significant enforceability risks"

        recommendations: List[str] = []
        if not elements_present.get("scope"):
            recommendations.append("Add broad scope language: 'Any dispute arising out of or relating to this Agreement'")
        if not elements_present.get("seat"):
            recommendations.append("Specify seat of arbitration (city and state/country)")
        if not elements_present.get("rules"):
            recommendations.append("Specify administering institution and rule set (e.g., AAA Commercial Rules)")
        if not elements_present.get("governing_law"):
            recommendations.append("Add governing law clause for the arbitration agreement itself")
        if not elements_present.get("arbitrator_count"):
            recommendations.append("Specify number of arbitrators (1 for smaller disputes, 3 for complex/high-value)")
        if is_international and not elements_present.get("language"):
            recommendations.append("Specify language of proceedings for international arbitration")
        if pathological:
            recommendations.append("URGENT: Resolve pathological clause issues before execution")

        model_clause = self._generate_model_clause(ctx, elements_present)

        severability = (
            "Under the separability doctrine (Prima Paint Corp. v. Flood & Conklin, 388 U.S. 395 (1967)), "
            "the arbitration clause is treated as a separate agreement from the container contract. "
            "A challenge to the validity of the overall contract does not defeat the arbitration clause. "
            "However, a challenge directed specifically at the arbitration clause itself (e.g., fraud in the inducement "
            "of the arbitration clause specifically) is for the court, not the arbitrator, unless a delegation clause is present."
        )

        logger.info(f"ClauseValidator: valid={overall_valid}, completeness={completeness_total:.3f}, unconscionability_risks={len(unconscionability_risks)}, pathological={len(pathological)}")

        return ClauseValidationResult(
            overall_valid=overall_valid,
            completeness_score=completeness_total,
            elements_present=elements_present,
            missing_elements=missing,
            unconscionability_risks=unconscionability_risks,
            pathological_issues=pathological,
            enforceability_assessment=enforceability,
            recommendations=recommendations,
            model_clause_suggestion=model_clause,
            severability_analysis=severability,
        )

    def _generate_model_clause(self, context: Dict[str, Any], present: Dict[str, bool]) -> str:
        """Generate a model arbitration clause based on context."""
        is_international = context.get("international", False)
        is_employment = context.get("employment", False)
        is_consumer = context.get("consumer", False)

        if is_international:
            return (
                "Any dispute arising out of or in connection with this Agreement, including any question regarding "
                "its existence, validity, or termination, shall be referred to and finally resolved by arbitration "
                "under the ICC Rules of Arbitration. The tribunal shall consist of [one/three] arbitrator(s). "
                "The seat of arbitration shall be [City, Country]. The language of the arbitration shall be English. "
                "The governing law of this Agreement shall be the substantive law of [jurisdiction]."
            )
        elif is_employment:
            return (
                "Any dispute arising out of or relating to this Agreement or the employment relationship, including "
                "claims of discrimination, harassment, wrongful termination, or wage disputes, shall be resolved by "
                "final and binding arbitration administered by the American Arbitration Association under its Employment "
                "Arbitration Rules. The arbitration shall be conducted by a single arbitrator in [City, State]. "
                "The arbitrator shall have authority to award any remedy available under applicable law. "
                "Each party shall bear its own costs, and the Company shall pay all AAA administrative fees and "
                "arbitrator compensation beyond what the employee would pay to file in court. "
                "This agreement does not waive any substantive rights under applicable law."
            )
        elif is_consumer:
            return (
                "Any dispute arising out of or relating to this Agreement shall be resolved by binding arbitration "
                "administered by the American Arbitration Association under its Consumer Arbitration Rules. "
                "The arbitration shall be conducted by a single arbitrator. The arbitration may be conducted "
                "in person, by telephone, or based on written submissions, at the consumer's election. "
                "The company shall pay all AAA administrative fees. The arbitrator may award any relief "
                "available in court. YOU ARE WAIVING YOUR RIGHT TO PARTICIPATE IN A CLASS ACTION."
            )
        else:
            return (
                "Any dispute, controversy, or claim arising out of or relating to this Agreement, or the breach, "
                "termination, or invalidity thereof, shall be settled by arbitration administered by the American "
                "Arbitration Association under its Commercial Arbitration Rules. The arbitration shall be conducted "
                "by [one/three] arbitrator(s) in [City, State]. The governing law shall be the laws of the State "
                "of [State]. The award rendered by the arbitrator(s) shall be final and binding and may be entered "
                "as a judgment in any court of competent jurisdiction."
            )


# ============================================================================
# DISPUTE RESOLUTION ADVISOR
# ============================================================================

class DisputeResolutionAdvisor:
    """Recommend ADR process based on dispute characteristics."""

    PROCESS_PROFILES: Dict[str, Dict[str, Any]] = {
        "arbitration": {
            "binding": True,
            "confidential": True,
            "preserves_relationship": False,
            "speed": "medium",
            "cost": "medium_high",
            "formality": "high",
            "best_for": ["complex commercial", "high value", "technical", "international", "securities", "construction"],
            "advantages": [
                "Final and binding resolution with limited judicial review",
                "Expert decision-maker (can select arbitrator with subject matter expertise)",
                "Confidential proceedings and award",
                "Generally faster than litigation (but slower than mediation)",
                "International enforceability under New York Convention",
                "Flexible procedural rules",
            ],
            "disadvantages": [
                "Limited discovery may disadvantage party without information",
                "Limited judicial review even for errors of law",
                "Can be expensive (arbitrator fees, institutional fees)",
                "No precedential value of award",
                "Difficulty with multi-party disputes",
                "No right to appeal on merits",
            ],
        },
        "mediation": {
            "binding": False,
            "confidential": True,
            "preserves_relationship": True,
            "speed": "fast",
            "cost": "low",
            "formality": "low",
            "best_for": ["ongoing relationship", "family", "employment", "neighbor", "partnership", "community"],
            "advantages": [
                "Preserves and can improve business/personal relationships",
                "Parties control outcome (voluntary agreement)",
                "Low cost compared to arbitration or litigation",
                "Fast resolution (often single day or session)",
                "Highly confidential under UMA and state statutes",
                "Creative solutions not available in adjudication",
                "Non-binding: no risk of adverse ruling",
            ],
            "disadvantages": [
                "Non-binding: party can walk away",
                "Depends on good faith participation of both parties",
                "Power imbalance can lead to unfair agreements",
                "No discovery mechanism to compel disclosure",
                "No precedent set",
                "May delay resolution if unsuccessful",
            ],
        },
        "med_arb": {
            "binding": True,
            "confidential": True,
            "preserves_relationship": True,
            "speed": "medium",
            "cost": "medium",
            "formality": "medium",
            "best_for": ["parties wanting to try negotiation first", "employment", "commercial with ongoing relationship"],
            "advantages": [
                "Best of both worlds: opportunity to settle before binding decision",
                "Incentivizes good-faith mediation participation",
                "Guaranteed resolution (arbitration backstop)",
                "Can preserve relationships through mediation phase",
            ],
            "disadvantages": [
                "Dual-role concern: mediator becoming arbitrator raises due process issues",
                "Parties may withhold information during mediation knowing arbitration follows",
                "Same neutral in both phases can create appearance of bias",
                "Complexity of transition between phases",
            ],
        },
        "early_neutral_evaluation": {
            "binding": False,
            "confidential": True,
            "preserves_relationship": True,
            "speed": "fast",
            "cost": "low",
            "formality": "low",
            "best_for": ["factual disputes", "damages quantification", "liability assessment", "pre-litigation"],
            "advantages": [
                "Expert assessment helps calibrate expectations early",
                "Low cost and time investment",
                "Can frame issues for subsequent ADR or litigation",
                "Neutral's assessment may prompt settlement",
            ],
            "disadvantages": [
                "Non-binding, advisory only",
                "Depends on neutral's expertise in subject matter",
                "Parties may disregard evaluation",
            ],
        },
        "mini_trial": {
            "binding": False,
            "confidential": True,
            "preserves_relationship": True,
            "speed": "medium",
            "cost": "medium",
            "formality": "medium",
            "best_for": ["large commercial disputes", "multi-issue cases", "disputes where executives need briefing"],
            "advantages": [
                "Executives hear abbreviated presentations and negotiate directly",
                "Neutral advisor can give non-binding opinion",
                "Preserves relationship by engaging decision-makers directly",
                "Efficient for complex multi-issue disputes",
            ],
            "disadvantages": [
                "Requires executive commitment and time",
                "Non-binding: may not resolve if executives disagree",
                "Preparation costs can be significant",
            ],
        },
        "dispute_review_board": {
            "binding": False,
            "confidential": True,
            "preserves_relationship": True,
            "speed": "fast",
            "cost": "low_per_dispute",
            "formality": "medium",
            "best_for": ["construction", "infrastructure", "long-term project", "ongoing contract"],
            "advantages": [
                "Real-time dispute resolution during project performance",
                "Board members develop deep project knowledge",
                "Prevents escalation and preserves working relationships",
                "High voluntary compliance rate (over 95%)",
            ],
            "disadvantages": [
                "Ongoing cost of maintaining board",
                "Typically non-binding (though can be contractually binding)",
                "Board members must remain neutral despite familiarity",
            ],
        },
    }

    COST_ESTIMATES: Dict[str, Dict[str, float]] = {
        "arbitration_small": {"min": 15_000, "max": 75_000, "currency": "USD"},
        "arbitration_medium": {"min": 75_000, "max": 350_000, "currency": "USD"},
        "arbitration_large": {"min": 350_000, "max": 2_000_000, "currency": "USD"},
        "arbitration_international": {"min": 200_000, "max": 5_000_000, "currency": "USD"},
        "mediation": {"min": 2_000, "max": 25_000, "currency": "USD"},
        "med_arb": {"min": 20_000, "max": 150_000, "currency": "USD"},
        "early_neutral_evaluation": {"min": 2_000, "max": 15_000, "currency": "USD"},
        "mini_trial": {"min": 25_000, "max": 100_000, "currency": "USD"},
        "dispute_review_board": {"min": 30_000, "max": 60_000, "currency": "USD"},
    }

    def recommend(self, dispute_facts: Dict[str, Any]) -> DisputeResolutionAdvisory:
        """Recommend an ADR process based on dispute characteristics."""
        amount = dispute_facts.get("amount", 0)
        complexity = dispute_facts.get("complexity", "medium").lower()
        relationship = dispute_facts.get("ongoing_relationship", False)
        confidentiality = dispute_facts.get("confidentiality_needed", True)
        speed = dispute_facts.get("speed_priority", "medium").lower()
        dispute_type = dispute_facts.get("dispute_type", "commercial").lower()
        international = dispute_facts.get("international", False)
        parties = dispute_facts.get("number_of_parties", 2)

        scores: Dict[str, float] = {}
        for process_name, profile in self.PROCESS_PROFILES.items():
            score = 50.0

            type_match = any(bt in dispute_type or dispute_type in bt for bt in profile["best_for"])
            if type_match:
                score += 20.0

            if relationship and profile["preserves_relationship"]:
                score += 15.0
            elif not relationship and not profile["preserves_relationship"]:
                score += 5.0

            if confidentiality and profile["confidential"]:
                score += 10.0

            if speed == "fast" and profile["speed"] == "fast":
                score += 15.0
            elif speed == "fast" and profile["speed"] == "medium":
                score += 5.0
            elif speed == "slow" and profile["speed"] in ("medium", "high"):
                score += 5.0

            if amount > 1_000_000 and process_name in ("arbitration", "mini_trial"):
                score += 15.0
            elif amount < 100_000 and process_name in ("mediation", "early_neutral_evaluation"):
                score += 15.0
            elif amount < 50_000 and process_name == "arbitration":
                score -= 10.0

            if complexity == "high" and process_name in ("arbitration", "mini_trial"):
                score += 10.0
            elif complexity == "low" and process_name in ("mediation", "early_neutral_evaluation"):
                score += 10.0

            if international and process_name == "arbitration":
                score += 20.0
            elif international and process_name not in ("arbitration", "med_arb"):
                score -= 15.0

            if parties > 2 and process_name in ("mediation", "mini_trial"):
                score += 5.0

            if process_name == "dispute_review_board" and dispute_type not in ("construction", "infrastructure"):
                score -= 30.0

            scores[process_name] = max(score, 0.0)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_process = ranked[0][0]
        best_profile = self.PROCESS_PROFILES[best_process]

        institution = self._recommend_institution(best_process, dispute_type, international, amount)
        cost_range = self._estimate_costs(best_process, amount, international)
        duration = self._estimate_duration(best_process, complexity, amount)
        rules = self._recommend_rules(best_process, institution, dispute_type)
        clause = self._generate_clause_language(best_process, institution, rules)

        alternatives: List[Dict[str, Any]] = []
        for proc_name, proc_score in ranked[1:4]:
            alt_profile = self.PROCESS_PROFILES[proc_name]
            alternatives.append({
                "process": proc_name,
                "score": round(proc_score, 1),
                "binding": alt_profile["binding"],
                "speed": alt_profile["speed"],
                "cost": alt_profile["cost"],
                "advantages": alt_profile["advantages"][:2],
            })

        rationale: List[str] = []
        if type_match:
            rationale.append(f"{best_process} is well-suited for {dispute_type} disputes")
        if relationship and best_profile["preserves_relationship"]:
            rationale.append("Process selected to preserve ongoing business/personal relationship")
        if international and best_process == "arbitration":
            rationale.append("Arbitration provides international enforceability under New York Convention")
        if amount > 1_000_000:
            rationale.append(f"High-value dispute (${amount:,.0f}) warrants formal adjudicatory process")
        elif amount < 100_000:
            rationale.append(f"Lower-value dispute (${amount:,.0f}) favors cost-efficient process")
        if speed == "fast":
            rationale.append("Speed priority factored into recommendation")
        if not rationale:
            rationale.append(f"{best_process} provides the best overall fit based on dispute characteristics")

        logger.info(f"DisputeResolutionAdvisor: recommended={best_process}, institution={institution}, score={ranked[0][1]:.1f}")

        return DisputeResolutionAdvisory(
            recommended_process=best_process,
            recommended_institution=institution,
            alternative_processes=alternatives,
            rationale=rationale,
            estimated_cost_range=cost_range,
            estimated_duration=duration,
            confidentiality_level="High" if best_profile["confidential"] else "Low",
            binding_nature="Binding" if best_profile["binding"] else "Non-binding",
            preserves_relationship=best_profile["preserves_relationship"],
            recommended_rules=rules,
            clause_language=clause,
        )

    def _recommend_institution(self, process: str, dispute_type: str, international: bool, amount: float) -> str:
        """Recommend an administering institution."""
        if process in ("mediation", "early_neutral_evaluation"):
            if dispute_type in ("securities", "broker_dealer"):
                return "FINRA Dispute Resolution Services"
            return "JAMS" if amount > 250_000 else "AAA"

        if process == "dispute_review_board":
            return "AAA (Dispute Resolution Board Foundation)"

        if international:
            if amount > 10_000_000:
                return "ICC International Court of Arbitration"
            return "ICDR (AAA International Division)"

        if dispute_type in ("securities", "broker_dealer", "investment_fraud"):
            return "FINRA Dispute Resolution Services"
        if dispute_type in ("employment", "discrimination", "wrongful_termination"):
            return "AAA (Employment Rules)" if amount < 500_000 else "JAMS"
        if dispute_type in ("construction", "infrastructure"):
            return "AAA (Construction Rules)"
        if amount > 5_000_000:
            return "JAMS"
        return "AAA (Commercial Rules)"

    def _estimate_costs(self, process: str, amount: float, international: bool) -> Dict[str, Any]:
        """Estimate costs for the recommended process."""
        if process == "arbitration":
            if international:
                key = "arbitration_international"
            elif amount > 1_000_000:
                key = "arbitration_large"
            elif amount > 100_000:
                key = "arbitration_medium"
            else:
                key = "arbitration_small"
        elif process in self.COST_ESTIMATES:
            key = process
        else:
            key = "mediation"

        estimate = self.COST_ESTIMATES.get(key, {"min": 5000, "max": 50_000, "currency": "USD"})
        return {
            "min": estimate["min"],
            "max": estimate["max"],
            "currency": estimate["currency"],
            "note": "Estimates include institutional fees, arbitrator/mediator compensation, and hearing facility costs. Attorney fees are additional.",
        }

    def _estimate_duration(self, process: str, complexity: str, amount: float) -> str:
        """Estimate duration for the recommended process."""
        durations: Dict[str, Dict[str, str]] = {
            "arbitration": {"low": "4-8 months", "medium": "8-14 months", "high": "14-24 months"},
            "mediation": {"low": "1-2 sessions (1-4 weeks)", "medium": "2-4 sessions (2-8 weeks)", "high": "3-6 sessions (4-12 weeks)"},
            "med_arb": {"low": "3-6 months", "medium": "6-10 months", "high": "10-18 months"},
            "early_neutral_evaluation": {"low": "2-4 weeks", "medium": "4-8 weeks", "high": "6-12 weeks"},
            "mini_trial": {"low": "2-4 months", "medium": "3-6 months", "high": "4-8 months"},
            "dispute_review_board": {"low": "30-60 days per dispute", "medium": "60-90 days per dispute", "high": "90-120 days per dispute"},
        }
        process_durations = durations.get(process, {"low": "3-6 months", "medium": "6-12 months", "high": "12-24 months"})
        return process_durations.get(complexity, process_durations["medium"])

    def _recommend_rules(self, process: str, institution: str, dispute_type: str) -> str:
        """Recommend specific rule set."""
        if "FINRA" in institution:
            return "FINRA Code of Arbitration Procedure for Customer Disputes (Rule 12000 Series)"
        if "ICC" in institution:
            return "ICC Rules of Arbitration (2021)"
        if "JAMS" in institution:
            if process == "mediation":
                return "JAMS Mediation Procedures"
            return "JAMS Comprehensive Arbitration Rules & Procedures"
        if "ICDR" in institution:
            return "ICDR International Arbitration Rules"
        if "Employment" in institution:
            return "AAA Employment Arbitration Rules and Mediation Procedures"
        if "Construction" in institution:
            return "AAA Construction Industry Arbitration Rules and Mediation Procedures"
        return "AAA Commercial Arbitration Rules and Mediation Procedures"

    def _generate_clause_language(self, process: str, institution: str, rules: str) -> str:
        """Generate recommended clause language."""
        if process == "mediation":
            return (
                f"Any dispute arising out of or relating to this Agreement shall first be submitted to "
                f"mediation administered by {institution} under its {rules}. If the dispute is not resolved "
                f"through mediation within 60 days after the commencement of mediation, either party may "
                f"pursue any remedy available at law or in equity."
            )
        elif process == "med_arb":
            return (
                f"Any dispute arising out of or relating to this Agreement shall first be submitted to "
                f"mediation administered by {institution}. If the dispute is not resolved through mediation "
                f"within 60 days, the dispute shall be settled by final and binding arbitration administered "
                f"by {institution} under its {rules}. The arbitration shall be conducted by a single "
                f"arbitrator in [City, State]."
            )
        else:
            return (
                f"Any dispute arising out of or relating to this Agreement, including the breach, termination, "
                f"or invalidity thereof, shall be settled by final and binding arbitration administered by "
                f"{institution} under its {rules}. The arbitration shall be conducted by [one/three] "
                f"arbitrator(s) in [City, State/Country]. Judgment on the award may be entered in any court "
                f"having jurisdiction thereof."
            )


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_SEARCH_INDEX: Optional[DoctrineSearchIndex] = None
_RULES_SEARCHER: Optional[ArbitrationRulesSearcher] = None
_ENFORCEABILITY_CHECKER: Optional[AwardEnforceabilityChecker] = None
_CLAUSE_VALIDATOR: Optional[ClauseValidator] = None
_DISPUTE_ADVISOR: Optional[DisputeResolutionAdvisor] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the search index."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        _SEARCH_INDEX = DoctrineSearchIndex()
        logger.info("DoctrineSearchIndex created for LG16")
    return _SEARCH_INDEX


def get_rules_searcher() -> ArbitrationRulesSearcher:
    """Get or create the arbitration rules searcher."""
    global _RULES_SEARCHER
    if _RULES_SEARCHER is None:
        _RULES_SEARCHER = ArbitrationRulesSearcher()
    return _RULES_SEARCHER


def get_enforceability_checker() -> AwardEnforceabilityChecker:
    """Get or create the award enforceability checker."""
    global _ENFORCEABILITY_CHECKER
    if _ENFORCEABILITY_CHECKER is None:
        _ENFORCEABILITY_CHECKER = AwardEnforceabilityChecker()
    return _ENFORCEABILITY_CHECKER


def get_clause_validator() -> ClauseValidator:
    """Get or create the clause validator."""
    global _CLAUSE_VALIDATOR
    if _CLAUSE_VALIDATOR is None:
        _CLAUSE_VALIDATOR = ClauseValidator()
    return _CLAUSE_VALIDATOR


def get_dispute_advisor() -> DisputeResolutionAdvisor:
    """Get or create the dispute resolution advisor."""
    global _DISPUTE_ADVISOR
    if _DISPUTE_ADVISOR is None:
        _DISPUTE_ADVISOR = DisputeResolutionAdvisor()
    return _DISPUTE_ADVISOR


def compute_query_hash(query: str) -> str:
    """Compute SHA-256 hash of a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
