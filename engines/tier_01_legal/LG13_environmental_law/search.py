"""
LG13 Environmental Law Engine - Search Module
================================================
TF-IDF inverted index search over environmental law doctrine blocks,
plus domain-specific analyzers for permits, compliance, contamination
chain-of-custody, CERCLA PRP liability, penalty calculation, and
environmental site assessment workflows.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index with BM25 scoring
    - SearchResult: Ranked result with score, snippet, provenance
    - PermitAnalyzer: Analyze permit requirements across statutes
    - ComplianceChecker: Multi-statute compliance assessment
    - CERCLAPRPAnalyzer: PRP liability chain analysis
    - ContaminationTracker: Contaminant source / pathway / receptor
    - PenaltyCalculator: EPA/TCEQ penalty policy computation
    - PhaseIESAWorkflow: Phase I ESA checklist and REC identification
    - RemediationSelector: Remedy selection framework for CERCLA/RCRA

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEARCH RESULT
# ============================================================================

@dataclass
class SearchResult:
    """A single search result from the doctrine index."""
    topic: str
    category: str
    score: float
    snippet: str
    authority: str = ""
    statute: str = ""
    cfr_reference: str = ""
    jurisdiction: str = ""
    relevance_explanation: str = ""
    block_hash: str = ""
    result_hash: str = ""

    def __post_init__(self) -> None:
        if not self.result_hash:
            content = f"{self.topic}|{self.score}|{self.snippet[:100]}"
            self.result_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ============================================================================
# INVERTED INDEX (TF-IDF + BM25)
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index with BM25 scoring over doctrine blocks."""

    BM25_K1: ClassVar[float] = 1.5
    BM25_B: ClassVar[float] = 0.75

    def __init__(self) -> None:
        self._index: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._doc_lengths: Dict[str, int] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._doc_content: Dict[str, str] = {}
        self._total_docs: int = 0
        self._avg_doc_length: float = 0.0
        self._df: Counter = Counter()
        self._built: bool = False

    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a document to the index."""
        tokens = self._tokenize(content)
        self._doc_lengths[doc_id] = len(tokens)
        self._doc_content[doc_id] = content
        self._doc_metadata[doc_id] = metadata or {}
        tf: Counter = Counter(tokens)
        unique_terms: Set[str] = set()
        for term, count in tf.items():
            self._index[term][doc_id] = count / max(len(tokens), 1)
            unique_terms.add(term)
        for term in unique_terms:
            self._df[term] += 1
        self._total_docs += 1
        self._built = False

    def build(self) -> None:
        """Finalize index by computing average doc length."""
        if self._total_docs > 0:
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
        else:
            self._avg_doc_length = 1.0
        self._built = True
        logger.info(f"DoctrineSearchIndex built: {self._total_docs} docs, {len(self._index)} unique terms")

    def search(self, query: str, top_k: int = 20, min_score: float = 0.01) -> List[SearchResult]:
        """Search the index using BM25."""
        if not self._built:
            self.build()
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        for token in query_tokens:
            if token not in self._index:
                continue
            df = self._df.get(token, 0)
            idf = math.log((self._total_docs - df + 0.5) / (df + 0.5) + 1.0)
            for doc_id, tf in self._index[token].items():
                doc_len = self._doc_lengths.get(doc_id, 1)
                raw_tf = tf * doc_len
                numerator = raw_tf * (self.BM25_K1 + 1)
                denominator = raw_tf + self.BM25_K1 * (1 - self.BM25_B + self.BM25_B * doc_len / max(self._avg_doc_length, 1))
                scores[doc_id] += idf * (numerator / max(denominator, 0.001))
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: List[SearchResult] = []
        for doc_id, score in ranked[:top_k]:
            if score < min_score:
                break
            meta = self._doc_metadata.get(doc_id, {})
            content = self._doc_content.get(doc_id, "")
            snippet = self._extract_snippet(content, query_tokens)
            results.append(SearchResult(
                topic=meta.get("topic", doc_id),
                category=meta.get("category", ""),
                score=round(score, 4),
                snippet=snippet,
                authority=meta.get("authority", ""),
                statute=meta.get("statute", ""),
                cfr_reference=meta.get("cfr_reference", ""),
                jurisdiction=meta.get("jurisdiction", ""),
                relevance_explanation=meta.get("relevance_explanation", ""),
                block_hash=meta.get("block_hash", ""),
            ))
        return results

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into searchable terms."""
        text = text.lower()
        text = re.sub(r"[^\w\s\-/]", " ", text)
        tokens = text.split()
        stop_words = frozenset({"the", "a", "an", "is", "are", "was", "were", "be", "been",
                                "being", "have", "has", "had", "do", "does", "did", "will",
                                "would", "shall", "should", "may", "might", "can", "could",
                                "of", "in", "to", "for", "with", "on", "at", "by", "from",
                                "as", "into", "through", "during", "before", "after", "above",
                                "below", "between", "under", "over", "and", "but", "or", "not",
                                "no", "nor", "so", "if", "then", "that", "this", "these", "those",
                                "it", "its", "they", "their", "them", "we", "us", "our"})
        return [t for t in tokens if t not in stop_words and len(t) > 1]

    def _extract_snippet(self, content: str, query_tokens: List[str], max_len: int = 300) -> str:
        """Extract a relevant snippet from content around query terms."""
        lower_content = content.lower()
        best_pos = 0
        best_score = 0
        window = 200
        for i in range(0, len(lower_content), 50):
            chunk = lower_content[i:i + window]
            score = sum(1 for t in query_tokens if t in chunk)
            if score > best_score:
                best_score = score
                best_pos = i
        start = max(0, best_pos - 50)
        end = min(len(content), start + max_len)
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    @property
    def document_count(self) -> int:
        """Return total documents in the index."""
        return self._total_docs

    @property
    def term_count(self) -> int:
        """Return total unique terms in the index."""
        return len(self._index)

    def get_stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        return {
            "total_documents": self._total_docs,
            "unique_terms": len(self._index),
            "avg_doc_length": round(self._avg_doc_length, 1),
            "built": self._built,
        }


# ============================================================================
# PERMIT ANALYZER
# ============================================================================

class PermitType(Enum):
    """Environmental permit types."""
    TITLE_V = "title_v"
    NSR_PSD = "nsr_psd"
    NPDES = "npdes"
    TPDES = "tpdes"
    SECTION_404 = "section_404"
    SECTION_401 = "section_401"
    RCRA_PART_B = "rcra_part_b"
    UIC_CLASS_II = "uic_class_ii"
    UIC_CLASS_I = "uic_class_i"
    UST = "ust"
    SPCC = "spcc"
    STORMWATER = "stormwater"
    RRC_DRILLING = "rrc_drilling"
    RRC_DISPOSAL = "rrc_disposal"
    AIR_MINOR = "air_minor"
    TCEQ_AIR = "tceq_air"
    TCEQ_WATER = "tceq_water"
    TCEQ_WASTE = "tceq_waste"


@dataclass
class PermitRequirement:
    """A single permit requirement."""
    permit_type: PermitType
    statute: str
    regulatory_agency: str
    description: str
    triggers: List[str]
    key_conditions: List[str]
    typical_timeline_days: int
    estimated_cost_range: str
    penalties_for_noncompliance: str
    renewal_period_years: int
    applicable_cfr: str = ""
    texas_specific: bool = False


@dataclass
class PermitAnalysisResult:
    """Result of permit requirement analysis."""
    activity_description: str
    jurisdiction: str
    required_permits: List[PermitRequirement]
    potentially_required: List[PermitRequirement]
    recommended_sequence: List[str]
    total_estimated_timeline_days: int
    compliance_notes: List[str]
    result_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.activity_description}|{len(self.required_permits)}|{self.jurisdiction}"
        self.result_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class PermitAnalyzer:
    """Analyze environmental permit requirements for proposed activities."""

    PERMIT_CATALOG: ClassVar[Dict[str, PermitRequirement]] = {
        "title_v": PermitRequirement(
            permit_type=PermitType.TITLE_V,
            statute="CAA Title V (42 USC 7661-7661f)",
            regulatory_agency="EPA / TCEQ",
            description="Major source operating permit for facilities emitting 100+ tpy of any criteria pollutant or 10/25 tpy HAPs",
            triggers=["major source threshold", "100 tpy criteria pollutant", "10 tpy single HAP", "25 tpy combined HAPs"],
            key_conditions=["emission limits", "monitoring requirements", "recordkeeping", "reporting", "compliance certification"],
            typical_timeline_days=540,
            estimated_cost_range="$50,000 - $500,000+",
            penalties_for_noncompliance="Up to $109,024/day per violation (2024 adjusted)",
            renewal_period_years=5,
            applicable_cfr="40 CFR Part 70",
        ),
        "npdes": PermitRequirement(
            permit_type=PermitType.NPDES,
            statute="CWA Section 402 (33 USC 1342)",
            regulatory_agency="EPA / State delegated agency",
            description="National Pollutant Discharge Elimination System permit for point source discharges to waters of the US",
            triggers=["point source discharge", "industrial wastewater", "municipal wastewater", "stormwater discharge"],
            key_conditions=["effluent limitations", "monitoring frequency", "DMR reporting", "best management practices"],
            typical_timeline_days=365,
            estimated_cost_range="$10,000 - $200,000",
            penalties_for_noncompliance="Up to $64,618/day per violation (civil); criminal penalties possible",
            renewal_period_years=5,
            applicable_cfr="40 CFR Parts 122-125",
        ),
        "tpdes": PermitRequirement(
            permit_type=PermitType.TPDES,
            statute="Texas Water Code Chapter 26",
            regulatory_agency="TCEQ",
            description="Texas Pollutant Discharge Elimination System permit (state-delegated NPDES)",
            triggers=["discharge to Texas waters", "industrial facility", "municipal facility"],
            key_conditions=["effluent limits", "monitoring", "DMR submittal to TCEQ", "compliance history"],
            typical_timeline_days=365,
            estimated_cost_range="$10,000 - $150,000",
            penalties_for_noncompliance="Up to $25,000/day per violation (Texas Water Code 7.102)",
            renewal_period_years=5,
            applicable_cfr="30 TAC Chapter 305",
            texas_specific=True,
        ),
        "section_404": PermitRequirement(
            permit_type=PermitType.SECTION_404,
            statute="CWA Section 404 (33 USC 1344)",
            regulatory_agency="USACE / EPA",
            description="Permit for discharge of dredged or fill material into waters of the US including wetlands",
            triggers=["dredge material discharge", "fill material in waters", "wetland disturbance", "stream crossing"],
            key_conditions=["least environmentally damaging practicable alternative", "mitigation", "404(b)(1) guidelines"],
            typical_timeline_days=300,
            estimated_cost_range="$25,000 - $300,000+ (includes mitigation)",
            penalties_for_noncompliance="Up to $64,618/day; restoration order; criminal prosecution",
            renewal_period_years=5,
            applicable_cfr="33 CFR Parts 320-332",
        ),
        "rcra_part_b": PermitRequirement(
            permit_type=PermitType.RCRA_PART_B,
            statute="RCRA Subtitle C (42 USC 6924-6925)",
            regulatory_agency="EPA / State authorized agency",
            description="Permit for treatment, storage, or disposal of hazardous waste at a TSDF",
            triggers=["hazardous waste treatment", "hazardous waste storage >90 days", "hazardous waste disposal"],
            key_conditions=["groundwater monitoring", "closure plan", "post-closure plan", "financial assurance", "corrective action"],
            typical_timeline_days=730,
            estimated_cost_range="$100,000 - $1,000,000+",
            penalties_for_noncompliance="Up to $70,117/day per violation; criminal penalties",
            renewal_period_years=10,
            applicable_cfr="40 CFR Parts 264-266, 270",
        ),
        "uic_class_ii": PermitRequirement(
            permit_type=PermitType.UIC_CLASS_II,
            statute="SDWA Part C (42 USC 300h)",
            regulatory_agency="RRC (Texas) / EPA",
            description="Underground Injection Control Class II permit for oil/gas related injection wells (disposal, enhanced recovery)",
            triggers=["saltwater disposal well", "produced water injection", "enhanced oil recovery injection", "hydrocarbon storage"],
            key_conditions=["mechanical integrity test", "area of review", "well construction", "monitoring", "financial responsibility"],
            typical_timeline_days=180,
            estimated_cost_range="$15,000 - $75,000",
            penalties_for_noncompliance="Up to $25,000/day (SDWA); RRC enforcement actions",
            renewal_period_years=10,
            applicable_cfr="40 CFR Part 144-148; 16 TAC Chapter 3",
            texas_specific=True,
        ),
        "spcc": PermitRequirement(
            permit_type=PermitType.SPCC,
            statute="CWA Section 311; OPA (33 USC 2701+)",
            regulatory_agency="EPA",
            description="Spill Prevention, Control, and Countermeasure plan for facilities storing oil",
            triggers=["oil storage >1,320 gal aboveground", "oil storage >42,000 gal underground", "reasonable expectation of discharge"],
            key_conditions=["spill prevention measures", "containment", "countermeasures", "PE certification", "employee training"],
            typical_timeline_days=120,
            estimated_cost_range="$5,000 - $50,000",
            penalties_for_noncompliance="Up to $64,618/day; $2,582,462 per spill event",
            renewal_period_years=5,
            applicable_cfr="40 CFR Part 112",
        ),
        "rrc_drilling": PermitRequirement(
            permit_type=PermitType.RRC_DRILLING,
            statute="Texas Natural Resources Code; 16 TAC Chapter 3",
            regulatory_agency="RRC",
            description="Drilling permit (W-1) for oil, gas, or geothermal wells in Texas",
            triggers=["drilling new well", "reentry", "deepening", "sidetrack"],
            key_conditions=["well spacing", "density rule", "surface casing", "cementing", "H2S contingency plan if applicable"],
            typical_timeline_days=30,
            estimated_cost_range="$200 - $1,000 (permit fee; well cost separate)",
            penalties_for_noncompliance="$10,000/day/violation; well plugging order",
            renewal_period_years=2,
            applicable_cfr="16 TAC Chapter 3",
            texas_specific=True,
        ),
        "rrc_disposal": PermitRequirement(
            permit_type=PermitType.RRC_DISPOSAL,
            statute="Texas Natural Resources Code; 16 TAC Chapter 3",
            regulatory_agency="RRC",
            description="Disposal well permit (W-14) for injection of produced water or oil and gas waste",
            triggers=["saltwater disposal", "produced water injection", "oilfield waste disposal"],
            key_conditions=["geological survey", "area of review", "casing and cementing", "mechanical integrity", "seismicity review"],
            typical_timeline_days=120,
            estimated_cost_range="$5,000 - $25,000 (permit; well construction separate)",
            penalties_for_noncompliance="$10,000/day/violation; permit revocation; well plugging order",
            renewal_period_years=10,
            applicable_cfr="16 TAC Chapter 3 Rule 9, 46",
            texas_specific=True,
        ),
        "stormwater": PermitRequirement(
            permit_type=PermitType.STORMWATER,
            statute="CWA Section 402(p) / Texas Water Code",
            regulatory_agency="TCEQ / EPA",
            description="General permit for stormwater discharges associated with construction or industrial activity",
            triggers=["construction >1 acre", "industrial activity SIC codes", "ms4 discharge"],
            key_conditions=["SWPPP preparation", "erosion controls", "sediment controls", "inspection schedule", "NOT"],
            typical_timeline_days=30,
            estimated_cost_range="$2,000 - $20,000",
            penalties_for_noncompliance="Up to $25,000/day (state); $64,618/day (federal)",
            renewal_period_years=5,
            applicable_cfr="40 CFR 122.26; 30 TAC 305",
            texas_specific=True,
        ),
    }

    def analyze_permits(self, activity: str, jurisdiction: str = "TX", keywords: Optional[List[str]] = None) -> PermitAnalysisResult:
        """Analyze which permits are required for a given activity."""
        lowered = activity.lower()
        kw_set = set(k.lower() for k in (keywords or []))
        required: List[PermitRequirement] = []
        potential: List[PermitRequirement] = []
        for permit_key, permit in self.PERMIT_CATALOG.items():
            trigger_match = any(t.lower() in lowered or t.lower() in " ".join(kw_set) for t in permit.triggers)
            if trigger_match:
                if permit.texas_specific and jurisdiction != "TX":
                    potential.append(permit)
                else:
                    required.append(permit)
            else:
                partial_match = any(kw in lowered for kw in [permit.permit_type.value.replace("_", " ")])
                if partial_match:
                    potential.append(permit)
        sequence = [p.permit_type.value for p in sorted(required, key=lambda x: x.typical_timeline_days, reverse=True)]
        total_timeline = max((p.typical_timeline_days for p in required), default=0)
        notes: List[str] = []
        if jurisdiction == "TX":
            notes.append("Texas is an EPA-delegated state for CWA (TPDES), CAA, and RCRA programs")
            notes.append("RRC has primary jurisdiction over oil & gas environmental matters in Texas")
            notes.append("TCEQ handles non-oil/gas environmental permits")
        if any("disposal" in t for t in (keywords or [])):
            notes.append("Saltwater disposal wells in Texas require RRC Class II UIC permit with seismicity review since 2014")
        return PermitAnalysisResult(
            activity_description=activity,
            jurisdiction=jurisdiction,
            required_permits=required,
            potentially_required=potential,
            recommended_sequence=sequence,
            total_estimated_timeline_days=total_timeline,
            compliance_notes=notes,
        )


# ============================================================================
# CERCLA PRP LIABILITY ANALYZER
# ============================================================================

class PRPCategory(Enum):
    """CERCLA PRP categories."""
    CURRENT_OWNER_OPERATOR = "current_owner_operator"
    PAST_OWNER_OPERATOR = "past_owner_operator"
    ARRANGER = "arranger"
    TRANSPORTER = "transporter"


@dataclass
class PRPLiabilityAssessment:
    """Assessment of CERCLA PRP liability."""
    party_name: str
    prp_category: PRPCategory
    liability_basis: str
    potential_defenses: List[str]
    defense_viability: Dict[str, str]
    joint_several_exposure: bool
    estimated_share_range: str
    contribution_claim_targets: List[str]
    key_facts_needed: List[str]
    settlement_considerations: List[str]
    statutory_citations: List[str]
    risk_level: str
    analysis_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.party_name}|{self.prp_category.value}|{self.risk_level}"
        self.analysis_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class CERCLAPRPAnalyzer:
    """Analyze CERCLA Potentially Responsible Party liability."""

    DEFENSES: ClassVar[Dict[str, Dict[str, str]]] = {
        "innocent_purchaser": {
            "statute": "CERCLA 101(35)(A), 107(b)(3)",
            "requirements": "All appropriate inquiries before acquisition; no knowledge of contamination; due care after discovery",
            "post_2002": "Must comply with CERCLA 101(35)(B) AAI standards (ASTM E1527)",
        },
        "bfpp": {
            "statute": "CERCLA 101(40), 107(r)",
            "requirements": "All appropriate inquiries; no affiliation with PRP; compliance with land use restrictions; cooperation with response",
            "post_2002": "Added by 2002 Brownfields Amendments; strongest new defense",
        },
        "contiguous_property_owner": {
            "statute": "CERCLA 107(q)",
            "requirements": "Contamination solely from contiguous property; no contribution; AAI; due care; cooperation",
            "limitation": "Narrow application; contamination must migrate from adjacent property",
        },
        "third_party": {
            "statute": "CERCLA 107(b)(3)",
            "requirements": "Release caused solely by third party with no contractual relationship; due care exercised",
            "limitation": "Very difficult to establish; landlord-tenant and contractual privity defeat this defense",
        },
        "act_of_god": {
            "statute": "CERCLA 107(b)(1)",
            "requirements": "Release caused solely by act of God (exceptional natural event)",
            "limitation": "Extremely rare; courts interpret very narrowly",
        },
    }

    def assess_liability(
        self,
        party_name: str,
        category: PRPCategory,
        facts: Dict[str, Any],
    ) -> PRPLiabilityAssessment:
        """Assess CERCLA liability for a party."""
        defenses: List[str] = []
        defense_viability: Dict[str, str] = {}
        did_aai = facts.get("all_appropriate_inquiries", False)
        knew_contamination = facts.get("knew_contamination_at_acquisition", False)
        contributed = facts.get("contributed_to_contamination", False)
        contractual_relationship = facts.get("contractual_relationship_with_polluter", False)
        if category == PRPCategory.CURRENT_OWNER_OPERATOR:
            liability_basis = "CERCLA 107(a)(1): Current owner/operator of facility where hazardous substances released"
            if did_aai and not knew_contamination and not contributed:
                defenses.append("bfpp")
                defense_viability["bfpp"] = "Potentially viable if all AAI requirements met and no affiliation with PRP"
                defenses.append("innocent_purchaser")
                defense_viability["innocent_purchaser"] = "Potentially viable (pre-2002 acquisitions) if no knowledge and due care shown"
            if not contractual_relationship and not contributed:
                defenses.append("third_party")
                defense_viability["third_party"] = "Weak unless no contractual relationship exists with actual polluter"
        elif category == PRPCategory.PAST_OWNER_OPERATOR:
            liability_basis = "CERCLA 107(a)(2): Past owner/operator at time of disposal of hazardous substances"
            if facts.get("disposal_during_ownership", True):
                defense_viability["limited_options"] = "Liability attaches if disposal occurred during ownership period"
            else:
                defenses.append("no_disposal_during_ownership")
                defense_viability["no_disposal_during_ownership"] = "Strong defense: no disposal of hazardous substances during ownership period"
        elif category == PRPCategory.ARRANGER:
            liability_basis = "CERCLA 107(a)(3): Arranged for disposal/treatment of hazardous substances at facility"
            if not facts.get("arranged_for_disposal", True):
                defenses.append("useful_product_doctrine")
                defense_viability["useful_product_doctrine"] = "If substance was sold as useful product (not arranged for disposal), Burlington Northern may apply"
        else:
            liability_basis = "CERCLA 107(a)(4): Transported hazardous substances to facility selected by transporter"
            if not facts.get("selected_disposal_site", True):
                defenses.append("did_not_select_site")
                defense_viability["did_not_select_site"] = "If generator selected the site, transporter liability may be limited"
        key_facts = [
            "Date of property acquisition/disposal",
            "Phase I ESA results at time of acquisition",
            "Environmental condition records from regulatory agencies",
            "Chain of title and prior uses of the property",
            "Nature and extent of contamination",
            "Other PRPs and their relative contributions",
        ]
        if category in (PRPCategory.CURRENT_OWNER_OPERATOR, PRPCategory.PAST_OWNER_OPERATOR):
            key_facts.append("Evidence of disposal operations during ownership period")
            key_facts.append("Groundwater monitoring data and plume delineation")
        settlement_notes = [
            "CERCLA 122 authorizes EPA consent decrees and administrative settlements",
            "De minimis settlements available under 122(g) for parties with minimal contribution",
            "Contribution protection under 113(f)(2) upon settlement with EPA/state",
            "Orphan share allocation may reduce settlement demand",
            "Consider insurance coverage (CGL, EIL, PLL policies)",
        ]
        citations = [
            "42 USC 9607(a) - Liability",
            "42 USC 9613(f) - Contribution",
            "42 USC 9607(b) - Defenses",
            "Burlington Northern & Santa Fe Ry. Co. v. United States, 556 U.S. 599 (2009)",
            "United States v. Bestfoods, 524 U.S. 51 (1998)",
        ]
        risk = "HIGH" if not defenses else ("MEDIUM" if len(defenses) < 2 else "LOW")
        share = "0-5%" if not contributed else "proportionate based on equitable factors"
        if category == PRPCategory.CURRENT_OWNER_OPERATOR and not defenses:
            share = "Joint and several (potentially 100%)"
            risk = "CRITICAL"
        return PRPLiabilityAssessment(
            party_name=party_name,
            prp_category=category,
            liability_basis=liability_basis,
            potential_defenses=defenses,
            defense_viability=defense_viability,
            joint_several_exposure=not bool(defenses),
            estimated_share_range=share,
            contribution_claim_targets=facts.get("other_prps", []),
            key_facts_needed=key_facts,
            settlement_considerations=settlement_notes,
            statutory_citations=citations,
            risk_level=risk,
        )


# ============================================================================
# PENALTY CALCULATOR
# ============================================================================

@dataclass
class PenaltyEstimate:
    """Estimated penalty calculation."""
    statute: str
    violation_type: str
    base_penalty_per_day: float
    gravity_adjustment: float
    economic_benefit_component: float
    days_of_violation: int
    total_estimated_range_low: float
    total_estimated_range_high: float
    mitigating_factors: List[str]
    aggravating_factors: List[str]
    statutory_maximum: str
    calculation_notes: List[str]
    penalty_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.statute}|{self.violation_type}|{self.total_estimated_range_high}"
        self.penalty_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class PenaltyCalculator:
    """Calculate environmental penalty estimates using EPA and TCEQ methodologies."""

    STATUTORY_MAXIMA: ClassVar[Dict[str, float]] = {
        "caa": 109024.0,
        "cwa": 64618.0,
        "rcra": 70117.0,
        "cercla": 70117.0,
        "tsca": 47756.0,
        "sdwa": 64618.0,
        "fifra": 22021.0,
        "epcra": 64618.0,
        "opa": 64618.0,
        "tceq_water": 25000.0,
        "tceq_air": 25000.0,
        "tceq_waste": 25000.0,
        "rrc": 10000.0,
    }

    GRAVITY_MULTIPLIERS: ClassVar[Dict[str, float]] = {
        "major": 1.0,
        "moderate": 0.60,
        "minor": 0.25,
    }

    def calculate(
        self,
        statute: str,
        violation_type: str,
        days_of_violation: int = 1,
        gravity: str = "moderate",
        economic_benefit: float = 0.0,
        mitigating: Optional[List[str]] = None,
        aggravating: Optional[List[str]] = None,
    ) -> PenaltyEstimate:
        """Calculate penalty estimate."""
        stat_key = statute.lower().replace(" ", "_")
        max_daily = self.STATUTORY_MAXIMA.get(stat_key, 50000.0)
        gravity_mult = self.GRAVITY_MULTIPLIERS.get(gravity.lower(), 0.60)
        base_per_day = max_daily * gravity_mult
        mit_factors = mitigating or []
        agg_factors = aggravating or []
        adjustment = 1.0
        for _ in mit_factors:
            adjustment *= 0.85
        for _ in agg_factors:
            adjustment *= 1.25
        adjusted_per_day = base_per_day * adjustment
        total_gravity = adjusted_per_day * days_of_violation
        total_low = total_gravity * 0.5 + economic_benefit
        total_high = total_gravity * 1.5 + economic_benefit
        total_high = min(total_high, max_daily * days_of_violation)
        notes = [
            f"Based on {statute} penalty policy with {gravity} gravity",
            f"Statutory maximum: ${max_daily:,.0f}/day/violation",
            f"Economic benefit component: ${economic_benefit:,.0f}",
            f"Gravity adjustment factor: {gravity_mult:.2f} x penalty adjustments {adjustment:.2f}",
        ]
        if mit_factors:
            notes.append(f"Mitigating: {', '.join(mit_factors)} (15% reduction each)")
        if agg_factors:
            notes.append(f"Aggravating: {', '.join(agg_factors)} (25% increase each)")
        return PenaltyEstimate(
            statute=statute,
            violation_type=violation_type,
            base_penalty_per_day=round(base_per_day, 2),
            gravity_adjustment=gravity_mult,
            economic_benefit_component=economic_benefit,
            days_of_violation=days_of_violation,
            total_estimated_range_low=round(max(total_low, 0), 2),
            total_estimated_range_high=round(max(total_high, 0), 2),
            mitigating_factors=mit_factors,
            aggravating_factors=agg_factors,
            statutory_maximum=f"${max_daily:,.0f}/day/violation",
            calculation_notes=notes,
        )


# ============================================================================
# PHASE I ESA WORKFLOW
# ============================================================================

class RECType(Enum):
    """Recognized Environmental Condition types."""
    REC = "rec"
    CREC = "crec"
    HREC = "hrec"
    DE_MINIMIS = "de_minimis"
    BUSINESS_ENVIRONMENTAL_RISK = "ber"


@dataclass
class PhaseIESAResult:
    """Phase I Environmental Site Assessment result."""
    property_address: str
    assessment_date: str
    findings: List[Dict[str, Any]]
    recs_identified: List[Dict[str, str]]
    crecs_identified: List[Dict[str, str]]
    hrecs_identified: List[Dict[str, str]]
    de_minimis_conditions: List[Dict[str, str]]
    data_gaps: List[str]
    recommendation: str
    phase_ii_needed: bool
    standard_applied: str
    checklist_completion: Dict[str, bool]
    result_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.property_address}|{len(self.recs_identified)}|{self.phase_ii_needed}"
        self.result_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class PhaseIESAWorkflow:
    """Phase I Environmental Site Assessment workflow per ASTM E1527-21."""

    CHECKLIST_ITEMS: ClassVar[List[str]] = [
        "records_review_federal",
        "records_review_state",
        "records_review_local",
        "records_review_tribal",
        "historical_sources_review",
        "aerial_photographs",
        "fire_insurance_maps",
        "city_directories",
        "building_permits",
        "site_reconnaissance",
        "adjoining_property_observations",
        "interviews_owner",
        "interviews_occupants",
        "interviews_local_government",
        "title_records",
        "environmental_liens",
        "activity_use_limitations",
        "vapor_intrusion_screening",
        "edr_radius_report",
        "user_provided_information",
    ]

    DATABASE_SEARCHES: ClassVar[Dict[str, str]] = {
        "NPL": "National Priorities List (Superfund sites) - 1.0 mile",
        "CERCLIS/SEMS": "Superfund screening database - 0.5 mile",
        "RCRA_CORRACTS": "RCRA Corrective Action facilities - 1.0 mile",
        "RCRA_TSD": "RCRA Treatment/Storage/Disposal - 0.5 mile",
        "RCRA_GENERATORS": "RCRA Generators - subject property and adjoining",
        "ERNS": "Emergency Response Notification System - subject property",
        "STATE_EQUIVALENT_NPL": "State Superfund list - 1.0 mile",
        "STATE_LEAKING_UST": "State LUST sites - 0.5 mile",
        "STATE_UST": "Registered UST sites - subject property and adjoining",
        "STATE_VOLUNTARY_CLEANUP": "VCP/Brownfield sites - 0.5 mile",
        "TRIBAL_LANDS": "Tribal environmental databases - 1.0 mile",
        "BROWNFIELDS": "Federal/State Brownfield listings - 0.5 mile",
        "TCEQ_IHW": "TCEQ Industrial and Hazardous Waste sites (TX specific)",
        "TCEQ_PST": "TCEQ Petroleum Storage Tank registrations (TX specific)",
        "RRC_WELLS": "RRC oil/gas well database (TX specific)",
    }

    def generate_checklist(self, property_address: str, jurisdiction: str = "TX") -> Dict[str, Any]:
        """Generate Phase I ESA checklist for a property."""
        checklist: Dict[str, bool] = {item: False for item in self.CHECKLIST_ITEMS}
        databases = dict(self.DATABASE_SEARCHES)
        if jurisdiction != "TX":
            databases.pop("TCEQ_IHW", None)
            databases.pop("TCEQ_PST", None)
            databases.pop("RRC_WELLS", None)
        return {
            "property_address": property_address,
            "standard": "ASTM E1527-21",
            "jurisdiction": jurisdiction,
            "checklist": checklist,
            "database_searches_required": databases,
            "historical_review_period": "First developed use or 1940, whichever is earlier",
            "report_shelf_life": "180 days (may be updated within 1 year per E1527-21 Section 4.6)",
            "vapor_intrusion_note": "ASTM E1527-21 requires vapor intrusion screening as part of Phase I",
            "qualifications": "Environmental Professional as defined by 40 CFR 312.10",
        }

    def assess_findings(
        self,
        property_address: str,
        findings: List[Dict[str, Any]],
    ) -> PhaseIESAResult:
        """Assess Phase I ESA findings and classify RECs."""
        recs: List[Dict[str, str]] = []
        crecs: List[Dict[str, str]] = []
        hrecs: List[Dict[str, str]] = []
        de_minimis: List[Dict[str, str]] = []
        data_gaps: List[str] = []
        for finding in findings:
            condition_type = finding.get("type", "").lower()
            desc = finding.get("description", "")
            source = finding.get("source", "")
            entry = {"description": desc, "source": source, "basis": finding.get("basis", "")}
            if condition_type == "rec":
                recs.append(entry)
            elif condition_type == "crec":
                crecs.append(entry)
            elif condition_type == "hrec":
                hrecs.append(entry)
            elif condition_type == "de_minimis":
                de_minimis.append(entry)
            elif condition_type == "data_gap":
                data_gaps.append(desc)
        phase_ii_needed = len(recs) > 0
        if recs:
            recommendation = "Phase II ESA recommended to evaluate RECs through sampling and analysis"
        elif crecs:
            recommendation = "No Phase II needed; CRECs require continued monitoring and institutional controls"
        else:
            recommendation = "No RECs identified; no further investigation recommended at this time"
        checklist_completion = {item: True for item in self.CHECKLIST_ITEMS}
        return PhaseIESAResult(
            property_address=property_address,
            assessment_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            findings=findings,
            recs_identified=recs,
            crecs_identified=crecs,
            hrecs_identified=hrecs,
            de_minimis_conditions=de_minimis,
            data_gaps=data_gaps,
            recommendation=recommendation,
            phase_ii_needed=phase_ii_needed,
            standard_applied="ASTM E1527-21 / 40 CFR 312",
            checklist_completion=checklist_completion,
        )


# ============================================================================
# REMEDIATION SELECTOR
# ============================================================================

class RemediationTechnology(Enum):
    """Remediation technology categories."""
    PUMP_AND_TREAT = "pump_and_treat"
    SOIL_VAPOR_EXTRACTION = "soil_vapor_extraction"
    AIR_SPARGING = "air_sparging"
    BIOREMEDIATION = "bioremediation"
    CHEMICAL_OXIDATION = "chemical_oxidation"
    THERMAL_DESORPTION = "thermal_desorption"
    EXCAVATION_DISPOSAL = "excavation_disposal"
    MONITORED_NATURAL_ATTENUATION = "monitored_natural_attenuation"
    PERMEABLE_REACTIVE_BARRIER = "permeable_reactive_barrier"
    PHYTOREMEDIATION = "phytoremediation"
    SOLIDIFICATION_STABILIZATION = "solidification_stabilization"
    CAPPING = "capping"
    INSTITUTIONAL_CONTROLS = "institutional_controls"
    DUAL_PHASE_EXTRACTION = "dual_phase_extraction"
    ENHANCED_BIOREMEDIATION = "enhanced_bioremediation"
    SOIL_WASHING = "soil_washing"


@dataclass
class RemediationOption:
    """A remediation technology option with assessment."""
    technology: RemediationTechnology
    description: str
    applicability: str
    target_media: List[str]
    target_contaminants: List[str]
    estimated_duration_years: str
    estimated_cost_range: str
    effectiveness: str
    limitations: List[str]
    regulatory_acceptance: str


class RemediationSelector:
    """Select appropriate remediation technologies based on site conditions."""

    TECHNOLOGY_CATALOG: ClassVar[Dict[str, RemediationOption]] = {
        "pump_and_treat": RemediationOption(
            technology=RemediationTechnology.PUMP_AND_TREAT,
            description="Extract contaminated groundwater, treat ex-situ, discharge or reinject",
            applicability="Dissolved phase groundwater contaminant plumes",
            target_media=["groundwater"],
            target_contaminants=["VOCs", "metals", "petroleum", "PFAS"],
            estimated_duration_years="5-30+",
            estimated_cost_range="$500,000 - $10,000,000+",
            effectiveness="High for plume containment; slow for mass removal",
            limitations=["Long-term O&M costs", "Tailing effect", "Requires discharge permit", "Matrix diffusion"],
            regulatory_acceptance="Widely accepted; default remedy for many CERCLA sites",
        ),
        "soil_vapor_extraction": RemediationOption(
            technology=RemediationTechnology.SOIL_VAPOR_EXTRACTION,
            description="Extract VOCs from unsaturated soil using vacuum wells",
            applicability="VOC-contaminated vadose zone soils with adequate permeability",
            target_media=["soil_vadose"],
            target_contaminants=["VOCs", "petroleum hydrocarbons", "TCE", "PCE", "BTEX"],
            estimated_duration_years="1-5",
            estimated_cost_range="$100,000 - $2,000,000",
            effectiveness="High for volatile compounds in permeable soils",
            limitations=["Low permeability soils ineffective", "Requires vapor treatment", "Seasonal variation"],
            regulatory_acceptance="Widely accepted; EPA presumptive remedy for VOC sites",
        ),
        "bioremediation": RemediationOption(
            technology=RemediationTechnology.BIOREMEDIATION,
            description="Use microorganisms to degrade contaminants in-situ",
            applicability="Petroleum hydrocarbons, chlorinated solvents (with amendments)",
            target_media=["soil", "groundwater"],
            target_contaminants=["BTEX", "petroleum", "PAHs", "chlorinated ethenes"],
            estimated_duration_years="2-10",
            estimated_cost_range="$50,000 - $1,000,000",
            effectiveness="Moderate to high for biodegradable compounds",
            limitations=["Temperature dependent", "May produce toxic intermediates", "Requires monitoring"],
            regulatory_acceptance="Accepted for petroleum; emerging acceptance for chlorinated solvents",
        ),
        "monitored_natural_attenuation": RemediationOption(
            technology=RemediationTechnology.MONITORED_NATURAL_ATTENUATION,
            description="Monitor natural degradation, dispersion, and dilution processes",
            applicability="Low-level contamination with demonstrated natural attenuation",
            target_media=["groundwater", "soil"],
            target_contaminants=["petroleum", "BTEX", "some chlorinated solvents"],
            estimated_duration_years="5-30+",
            estimated_cost_range="$100,000 - $1,000,000 (monitoring)",
            effectiveness="Varies; requires demonstration of decreasing trends",
            limitations=["Long timeframe", "Requires extensive monitoring", "Not for high concentrations", "Receptor proximity"],
            regulatory_acceptance="EPA OSWER Directive 9200.4-17P; accepted as component of remedy",
        ),
        "excavation_disposal": RemediationOption(
            technology=RemediationTechnology.EXCAVATION_DISPOSAL,
            description="Excavate contaminated soil and transport to licensed disposal facility",
            applicability="Localized soil contamination; source removal",
            target_media=["soil"],
            target_contaminants=["all soil contaminants", "metals", "petroleum", "PCBs", "pesticides"],
            estimated_duration_years="<1",
            estimated_cost_range="$100 - $500+ per ton (plus transport and disposal fees)",
            effectiveness="Definitive source removal; immediate",
            limitations=["High volume = high cost", "Traffic/dust/noise", "Disposal facility capacity", "Deep contamination impractical"],
            regulatory_acceptance="Universally accepted; often preferred for small/accessible volumes",
        ),
        "chemical_oxidation": RemediationOption(
            technology=RemediationTechnology.CHEMICAL_OXIDATION,
            description="Inject oxidants (permanganate, persulfate, Fenton's reagent, ozone) to destroy contaminants in-situ",
            applicability="Source zones with chlorinated VOCs, BTEX, or other oxidizable contaminants",
            target_media=["soil", "groundwater"],
            target_contaminants=["TCE", "PCE", "BTEX", "PAHs", "1,4-dioxane"],
            estimated_duration_years="1-5",
            estimated_cost_range="$100,000 - $3,000,000",
            effectiveness="High for target compounds; may require multiple applications",
            limitations=["Non-selective oxidation", "Rebound possible", "Metal mobilization", "Exothermic reactions"],
            regulatory_acceptance="Widely accepted; growing use at CERCLA and RCRA sites",
        ),
    }

    def recommend(self, contaminants: List[str], media: List[str], site_factors: Optional[Dict[str, Any]] = None) -> List[RemediationOption]:
        """Recommend remediation technologies based on site conditions."""
        contam_lower = [c.lower() for c in contaminants]
        media_lower = [m.lower() for m in media]
        scored: List[Tuple[float, RemediationOption]] = []
        for key, option in self.TECHNOLOGY_CATALOG.items():
            score = 0.0
            media_match = any(m in " ".join(option.target_media).lower() for m in media_lower)
            if media_match:
                score += 2.0
            contam_match_count = sum(
                1 for c in contam_lower
                if any(c in tc.lower() for tc in option.target_contaminants)
            )
            score += contam_match_count * 1.5
            if site_factors:
                if site_factors.get("budget_limited") and "low" in option.estimated_cost_range.lower():
                    score += 1.0
                if site_factors.get("time_sensitive") and "<1" in option.estimated_duration_years:
                    score += 2.0
            if score > 0:
                scored.append((score, option))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [opt for _, opt in scored]


# ============================================================================
# COMPLIANCE CHECKER
# ============================================================================

@dataclass
class ComplianceCheckResult:
    """Result of multi-statute compliance check."""
    facility_type: str
    jurisdiction: str
    applicable_statutes: List[str]
    compliance_items: List[Dict[str, Any]]
    high_risk_items: List[str]
    permits_required: List[str]
    reporting_obligations: List[str]
    inspection_frequency: str
    overall_risk: str
    result_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.facility_type}|{len(self.compliance_items)}|{self.overall_risk}"
        self.result_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class ComplianceChecker:
    """Multi-statute environmental compliance assessment."""

    def check_facility(self, facility_type: str, activities: List[str], jurisdiction: str = "TX") -> ComplianceCheckResult:
        """Check compliance requirements for a facility."""
        applicable: List[str] = []
        items: List[Dict[str, Any]] = []
        high_risk: List[str] = []
        permits: List[str] = []
        reporting: List[str] = []
        activities_lower = [a.lower() for a in activities]
        all_text = " ".join(activities_lower) + " " + facility_type.lower()
        # Check each major statute
        if any(kw in all_text for kw in ["air", "emission", "stack", "combustion", "flare", "boiler", "paint", "voc"]):
            applicable.append("CAA")
            items.append({"statute": "CAA", "requirement": "Determine major/minor source status", "priority": "HIGH"})
            permits.append("Air quality permit (Title V or minor source)")
            reporting.append("Annual emissions inventory")
            if "major source" in all_text or "100 tpy" in all_text:
                high_risk.append("Major source air permit compliance")
        if any(kw in all_text for kw in ["discharge", "wastewater", "effluent", "outfall", "cooling water", "process water"]):
            applicable.append("CWA")
            items.append({"statute": "CWA", "requirement": "NPDES/TPDES permit for point source discharges", "priority": "HIGH"})
            permits.append("NPDES/TPDES discharge permit")
            reporting.append("Discharge Monitoring Reports (DMRs)")
        if any(kw in all_text for kw in ["stormwater", "construction", "earthmoving", "grading"]):
            applicable.append("CWA-Stormwater")
            items.append({"statute": "CWA", "requirement": "Stormwater general permit and SWPPP", "priority": "MEDIUM"})
            permits.append("Stormwater general permit (MSGP or CGP)")
            reporting.append("SWPPP inspections and documentation")
        if any(kw in all_text for kw in ["hazardous waste", "chemical", "solvent", "paint waste", "oil waste", "laboratory"]):
            applicable.append("RCRA")
            items.append({"statute": "RCRA", "requirement": "Hazardous waste generator determination", "priority": "HIGH"})
            reporting.append("Biennial hazardous waste report (LQG)")
            high_risk.append("Hazardous waste management compliance")
        if any(kw in all_text for kw in ["oil", "petroleum", "fuel", "diesel", "gasoline", "tank"]):
            applicable.append("OPA/SPCC")
            items.append({"statute": "OPA", "requirement": "SPCC Plan if >1,320 gal aboveground oil storage", "priority": "MEDIUM"})
            permits.append("SPCC Plan (PE certified)")
        if any(kw in all_text for kw in ["underground storage tank", "ust", "fuel tank underground"]):
            applicable.append("RCRA-UST")
            items.append({"statute": "RCRA Subtitle I", "requirement": "UST registration and leak detection", "priority": "HIGH"})
            permits.append("UST registration and financial responsibility")
            high_risk.append("UST leak detection and release reporting")
        if any(kw in all_text for kw in ["chemical storage", "extremely hazardous", "threshold planning"]):
            applicable.append("EPCRA")
            items.append({"statute": "EPCRA", "requirement": "Tier II reporting and TRI if applicable", "priority": "MEDIUM"})
            reporting.append("Tier II annual report")
            reporting.append("TRI Form R (if applicable)")
        if any(kw in all_text for kw in ["oil well", "gas well", "drilling", "production", "disposal well", "injection"]):
            applicable.append("RRC")
            if jurisdiction == "TX":
                items.append({"statute": "TX NRC / 16 TAC 3", "requirement": "RRC drilling/operating permits", "priority": "HIGH"})
                permits.append("RRC W-1 drilling permit")
                permits.append("RRC disposal well permit (if SWD)")
                reporting.append("RRC production reports (P-1, P-2)")
                high_risk.append("RRC environmental compliance (SWR 8, 9, 14)")
        # Overall risk
        if len(high_risk) >= 3:
            overall = "HIGH"
        elif len(high_risk) >= 1:
            overall = "MEDIUM"
        else:
            overall = "LOW"
        inspection_freq = "Annual (typical for major sources / RCRA TSDFs)"
        if overall == "LOW":
            inspection_freq = "Every 2-5 years (typical for minor sources)"
        return ComplianceCheckResult(
            facility_type=facility_type,
            jurisdiction=jurisdiction,
            applicable_statutes=applicable,
            compliance_items=items,
            high_risk_items=high_risk,
            permits_required=permits,
            reporting_obligations=reporting,
            inspection_frequency=inspection_freq,
            overall_risk=overall,
        )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def compute_query_hash(query: str, salt: str = "LG13_ENV_v1") -> str:
    """Compute a deterministic hash for a query."""
    content = f"{salt}:{query.strip().lower()}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_search_index(doctrine_blocks: List[Dict[str, Any]]) -> DoctrineSearchIndex:
    """Build a search index from doctrine blocks."""
    index = DoctrineSearchIndex()
    for block in doctrine_blocks:
        doc_id = block.get("topic", str(hash(str(block))))
        content_parts = [
            block.get("topic", ""),
            block.get("summary", ""),
            block.get("analysis", ""),
            block.get("authority", ""),
            " ".join(block.get("keywords", [])),
        ]
        content = " ".join(part for part in content_parts if part)
        metadata = {
            "topic": block.get("topic", ""),
            "category": block.get("category", ""),
            "authority": block.get("authority", ""),
            "statute": block.get("statute", ""),
            "cfr_reference": block.get("cfr_reference", ""),
            "jurisdiction": block.get("jurisdiction", ""),
            "block_hash": block.get("block_hash", ""),
        }
        index.add_document(doc_id, content, metadata)
    index.build()
    return index
