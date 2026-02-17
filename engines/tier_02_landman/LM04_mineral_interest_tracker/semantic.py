"""
LM04 Mineral Interest Tracker - Semantic Dictionary
=====================================================

Comprehensive mineral interest terminology covering:
- Net mineral acres, mineral deed, royalty deed
- NPRI, ORRI, WI, NRI, executive rights
- Surface estate, mineral estate, severed minerals
- Unleased minerals, leased minerals
- Conveyance terminology
- Pooling and unitization terms
- Probate and inheritance terms
- Fractional interest terms
- Texas-specific legal terms

Engine: LM04 | Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SemanticDomain(str, Enum):
    """Domain classification for semantic terms."""
    INTEREST_TYPE = "interest_type"
    CONVEYANCE = "conveyance"
    OWNERSHIP = "ownership"
    FRACTIONAL = "fractional"
    POOLING = "pooling"
    PROBATE = "probate"
    LEASING = "leasing"
    SURFACE_MINERAL = "surface_mineral"
    REGULATORY = "regulatory"
    FINANCIAL = "financial"
    TEMPORAL = "temporal"
    RIGHTS = "rights"
    CONFLICT = "conflict"
    MEASUREMENT = "measurement"
    TEXAS_SPECIFIC = "texas_specific"
    LOUISIANA_SPECIFIC = "louisiana_specific"


class TermComplexity(str, Enum):
    """Complexity level of a term."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TermUsage(str, Enum):
    """Primary usage context for a term."""
    LEGAL = "legal"
    INDUSTRY = "industry"
    REGULATORY = "regulatory"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    COLLOQUIAL = "colloquial"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SemanticTerm:
    """A single semantic dictionary entry."""
    term_id: str
    canonical_term: str
    domain: SemanticDomain
    definition: str
    aliases: list[str] = field(default_factory=list)
    abbreviations: list[str] = field(default_factory=list)
    related_terms: list[str] = field(default_factory=list)
    antonyms: list[str] = field(default_factory=list)
    usage_context: TermUsage = TermUsage.LEGAL
    complexity: TermComplexity = TermComplexity.INTERMEDIATE
    examples: list[str] = field(default_factory=list)
    legal_significance: str = ""
    common_mistakes: list[str] = field(default_factory=list)
    texas_specific_notes: str = ""
    hash_digest: str = ""

    def __post_init__(self) -> None:
        if not self.hash_digest:
            payload = f"{self.term_id}|{self.canonical_term}|{self.definition}"
            self.hash_digest = hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "term_id": self.term_id,
            "canonical_term": self.canonical_term,
            "domain": self.domain.value,
            "definition": self.definition,
            "aliases": self.aliases,
            "abbreviations": self.abbreviations,
            "related_terms": self.related_terms,
            "antonyms": self.antonyms,
            "usage_context": self.usage_context.value,
            "complexity": self.complexity.value,
            "examples": self.examples,
            "legal_significance": self.legal_significance,
            "common_mistakes": self.common_mistakes,
            "texas_specific_notes": self.texas_specific_notes,
            "hash_digest": self.hash_digest,
        }

    def matches(self, query: str) -> bool:
        """Check if this term matches a search query."""
        q = query.lower().strip()
        if q in self.canonical_term.lower():
            return True
        for alias in self.aliases:
            if q in alias.lower():
                return True
        for abbr in self.abbreviations:
            if q == abbr.lower():
                return True
        return False


# ---------------------------------------------------------------------------
# Semantic Dictionary
# ---------------------------------------------------------------------------

class MineralSemanticDictionary:
    """Full semantic dictionary for LM04 Mineral Interest Tracker."""

    def __init__(self) -> None:
        self._terms: dict[str, SemanticTerm] = {}
        self._domain_index: dict[str, list[str]] = {}
        self._alias_index: dict[str, str] = {}
        self._abbreviation_index: dict[str, str] = {}
        self._load_all_terms()
        logger.info(
            "LM04 SemanticDictionary loaded: {} terms across {} domains",
            len(self._terms),
            len(self._domain_index),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def lookup(self, query: str) -> SemanticTerm | None:
        """Look up a term by canonical name, alias, or abbreviation."""
        q = query.lower().strip()
        # Direct ID lookup
        if q in self._terms:
            return self._terms[q]
        # Canonical name lookup
        for tid, term in self._terms.items():
            if term.canonical_term.lower() == q:
                return term
        # Abbreviation lookup
        tid = self._abbreviation_index.get(q.upper())
        if tid and tid in self._terms:
            return self._terms[tid]
        # Alias lookup
        tid = self._alias_index.get(q)
        if tid and tid in self._terms:
            return self._terms[tid]
        return None

    def search(self, query: str) -> list[SemanticTerm]:
        """Search for terms matching the query."""
        results: list[SemanticTerm] = []
        seen: set[str] = set()
        q = query.lower().strip()
        # Exact matches first
        for tid, term in self._terms.items():
            if term.matches(q) and tid not in seen:
                results.append(term)
                seen.add(tid)
        # Content matches
        for tid, term in self._terms.items():
            if tid not in seen and q in term.definition.lower():
                results.append(term)
                seen.add(tid)
        return results

    def get_by_domain(self, domain: SemanticDomain) -> list[SemanticTerm]:
        """Get all terms in a specific domain."""
        ids = self._domain_index.get(domain.value, [])
        return [self._terms[tid] for tid in ids if tid in self._terms]

    def get_all_terms(self) -> list[SemanticTerm]:
        """Return all terms in the dictionary."""
        return list(self._terms.values())

    def get_related(self, term_id: str) -> list[SemanticTerm]:
        """Get terms related to the given term."""
        term = self._terms.get(term_id)
        if not term:
            return []
        results: list[SemanticTerm] = []
        for rt in term.related_terms:
            for tid, t in self._terms.items():
                if t.canonical_term.lower() == rt.lower() or tid == rt:
                    results.append(t)
                    break
        return results

    def normalize_term(self, raw_text: str) -> str | None:
        """Normalize raw text to a canonical term if possible."""
        term = self.lookup(raw_text)
        return term.canonical_term if term else None

    def normalize_interest_type(self, raw_type: str) -> str:
        """Normalize a raw interest type string to standard abbreviation."""
        mapping = self._build_interest_type_normalization_map()
        normalized = raw_type.strip().upper()
        if normalized in mapping:
            return mapping[normalized]
        # Try fuzzy matching
        raw_lower = raw_type.lower().strip()
        for key, value in mapping.items():
            if raw_lower in key.lower() or key.lower() in raw_lower:
                return value
        return raw_type.upper()

    def extract_interest_types(self, text: str) -> list[str]:
        """Extract interest type references from free text."""
        found: list[str] = []
        seen: set[str] = set()
        text_upper = text.upper()
        type_patterns = [
            (r'\bWI\b', 'WI'), (r'\bRI\b', 'RI'), (r'\bORRI\b', 'ORRI'),
            (r'\bNPRI\b', 'NPRI'), (r'\bNRI\b', 'NRI'), (r'\bNMA\b', 'NMA'),
            (r'\bMI\b', 'MI'), (r'\bNEMI\b', 'NEMI'), (r'\bFSD\b', 'FSD'),
            (r'WORKING\s+INTEREST', 'WI'), (r'ROYALTY\s+INTEREST', 'RI'),
            (r'OVERRIDING\s+ROYALTY', 'ORRI'), (r'NON.?PARTICIPATING\s+ROYALTY', 'NPRI'),
            (r'NET\s+REVENUE\s+INTEREST', 'NRI'), (r'NET\s+MINERAL\s+ACRES?', 'NMA'),
            (r'MINERAL\s+INTEREST', 'MI'), (r'NON.?EXECUTIVE\s+MINERAL', 'NEMI'),
            (r'FEE\s+SIMPLE\s+DETERMINABLE', 'FSD'), (r'EXECUTIVE\s+RIGHT', 'EXEC'),
            (r'TERM\s+MINERAL', 'TERM_MI'), (r'LIFE\s+ESTATE\s+MINERAL', 'LIFE_MI'),
        ]
        for pattern, code in type_patterns:
            if re.search(pattern, text_upper) and code not in seen:
                found.append(code)
                seen.add(code)
        return found

    def export_json(self) -> str:
        """Export entire dictionary as JSON."""
        return json.dumps(
            [t.to_dict() for t in self._terms.values()],
            indent=2,
        )

    @property
    def term_count(self) -> int:
        return len(self._terms)

    @property
    def domain_counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._domain_index.items()}

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _register(self, term: SemanticTerm) -> None:
        self._terms[term.term_id] = term
        dom = term.domain.value
        self._domain_index.setdefault(dom, []).append(term.term_id)
        for alias in term.aliases:
            self._alias_index[alias.lower()] = term.term_id
        for abbr in term.abbreviations:
            self._abbreviation_index[abbr.upper()] = term.term_id

    def _build_interest_type_normalization_map(self) -> dict[str, str]:
        return {
            "WI": "WI", "WORKING INTEREST": "WI", "WORKING INT": "WI",
            "WORKING INT.": "WI", "W.I.": "WI", "W/I": "WI",
            "RI": "RI", "ROYALTY INTEREST": "RI", "ROYALTY INT": "RI",
            "ROYALTY INT.": "RI", "R.I.": "RI", "R/I": "RI", "ROY": "RI",
            "ORRI": "ORRI", "OVERRIDING ROYALTY INTEREST": "ORRI",
            "OVERRIDING ROYALTY": "ORRI", "OVERRIDE": "ORRI", "ORI": "ORRI",
            "O.R.R.I.": "ORRI", "OVERRIDING ROY": "ORRI", "OVER-RIDING ROYALTY": "ORRI",
            "NPRI": "NPRI", "NON-PARTICIPATING ROYALTY INTEREST": "NPRI",
            "NON-PARTICIPATING ROYALTY": "NPRI", "NONPARTICIPATING ROYALTY": "NPRI",
            "NON PARTICIPATING ROYALTY": "NPRI", "N.P.R.I.": "NPRI",
            "NRI": "NRI", "NET REVENUE INTEREST": "NRI", "NET REV INT": "NRI",
            "N.R.I.": "NRI", "NET REVENUE": "NRI",
            "MI": "MI", "MINERAL INTEREST": "MI", "MINERAL INT": "MI",
            "M.I.": "MI", "MIN INT": "MI", "MINERAL FEE": "MI",
            "NMA": "NMA", "NET MINERAL ACRES": "NMA", "NET MINERAL ACRE": "NMA",
            "N.M.A.": "NMA", "NET MIN ACRES": "NMA",
            "NEMI": "NEMI", "NON-EXECUTIVE MINERAL INTEREST": "NEMI",
            "NON EXECUTIVE MINERAL": "NEMI", "NONEXECUTIVE MINERAL": "NEMI",
            "FSD": "FSD", "FEE SIMPLE DETERMINABLE": "FSD",
            "DETERMINABLE FEE": "FSD",
            "EXEC": "EXEC", "EXECUTIVE RIGHT": "EXEC",
            "EXECUTIVE RIGHTS": "EXEC", "EXEC RIGHT": "EXEC",
            "TERM_MI": "TERM_MI", "TERM MINERAL INTEREST": "TERM_MI",
            "TERM MINERAL": "TERM_MI",
            "LIFE_MI": "LIFE_MI", "LIFE ESTATE MINERAL": "LIFE_MI",
            "LIFE ESTATE MINERAL INTEREST": "LIFE_MI",
        }

    # ------------------------------------------------------------------
    # Term definitions
    # ------------------------------------------------------------------

    def _load_all_terms(self) -> None:
        self._load_interest_type_terms()
        self._load_ownership_terms()
        self._load_conveyance_terms()
        self._load_fractional_terms()
        self._load_pooling_terms()
        self._load_probate_terms()
        self._load_leasing_terms()
        self._load_rights_terms()
        self._load_measurement_terms()
        self._load_financial_terms()
        self._load_regulatory_terms()
        self._load_surface_mineral_terms()
        self._load_temporal_terms()
        self._load_conflict_terms()
        self._load_texas_specific_terms()
        self._load_louisiana_terms()

    # === INTEREST TYPE TERMS ==========================================

    def _load_interest_type_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-INT-001",
            canonical_term="Working Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "The operating interest in an oil and gas lease that bears the costs of exploration, "
                "development, and production. The working interest holder has the right to drill and "
                "produce. The WI bears 100% of costs and receives 100% of revenue less all burdens "
                "(royalty, ORRI, etc.). The net revenue interest to the WI equals WI minus total burdens."
            ),
            aliases=["operating interest", "lessee's interest", "developer's interest"],
            abbreviations=["WI", "W.I.", "W/I"],
            related_terms=["Net Revenue Interest", "Overriding Royalty Interest", "Royalty Interest"],
            antonyms=["Royalty Interest", "Non-Participating Royalty Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=[
                "The operator holds a 75% working interest in the unit",
                "WI bears all drilling and completion costs proportionally",
            ],
            legal_significance="Only interest type that bears costs; created by oil and gas lease",
            common_mistakes=[
                "Confusing WI with NRI - WI is before deducting burdens, NRI is after",
                "Assuming WI always equals 100% - it can be fractional when assigned",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-002",
            canonical_term="Royalty Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "A non-operating interest entitling the holder to a share of production free of "
                "production costs. The lessor's royalty is the most common form, created by the oil "
                "and gas lease. The royalty interest does not bear costs and does not carry executive "
                "rights. Royalty is typically expressed as a fraction of production (e.g., 1/8, 3/16, 1/4)."
            ),
            aliases=["landowner's royalty", "lessor's royalty", "royalty"],
            abbreviations=["RI", "R.I.", "R/I"],
            related_terms=["Working Interest", "Non-Participating Royalty Interest", "Overriding Royalty Interest"],
            antonyms=["Working Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=[
                "The lease provides a 1/4 royalty to the mineral owner",
                "Landowner receives royalty free of all production costs",
            ],
            legal_significance="Created by lease; does not bear costs; terminates with lease",
            common_mistakes=[
                "Confusing royalty interest with mineral interest - royalty has no executive rights",
                "Assuming royalty always means 1/8 - modern leases commonly provide 1/4 or 3/16",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-003",
            canonical_term="Overriding Royalty Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "A non-operating, non-cost-bearing interest carved from the working interest that "
                "terminates when the underlying lease terminates. ORRIs are commonly assigned to "
                "landmen, geologists, brokers, and other industry participants as compensation. "
                "Unlike NPRI, ORRI is lease-dependent and does not survive lease expiration."
            ),
            aliases=["override", "overriding royalty", "carved-out interest"],
            abbreviations=["ORRI", "ORI", "O.R.R.I."],
            related_terms=["Working Interest", "Non-Participating Royalty Interest", "Net Revenue Interest"],
            antonyms=["Working Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.INTERMEDIATE,
            examples=[
                "Landman retained a 2% ORRI on the lease he brokered",
                "Total ORRIs burden the working interest and reduce the operator's NRI",
            ],
            legal_significance="Carved from WI, terminates with lease; not a mineral fee interest",
            common_mistakes=[
                "Confusing ORRI with NPRI - ORRI terminates with lease, NPRI survives",
                "Thinking ORRI is carved from royalty - it's carved from working interest",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-004",
            canonical_term="Non-Participating Royalty Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "A royalty interest carved from the mineral estate that entitles the holder to a "
                "share of production free of costs but without executive rights, bonus participation, "
                "or delay rental participation. Unlike ORRI, NPRI survives lease termination because "
                "it is carved from the mineral fee. The NPRI holder receives royalty from any lease "
                "executed on the tract."
            ),
            aliases=[
                "non-participating royalty", "NPRI", "non-participating interest",
                "nonparticipating royalty interest", "perpetual royalty interest",
            ],
            abbreviations=["NPRI", "N.P.R.I."],
            related_terms=["Royalty Interest", "Mineral Interest", "Executive Right", "Non-Executive Mineral Interest"],
            antonyms=["Mineral Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=[
                "Grantor reserved a 1/16 NPRI in the mineral deed",
                "NPRI holder receives royalty regardless of who executes the lease",
            ],
            legal_significance="Carved from mineral fee, survives lease termination; no executive rights",
            common_mistakes=[
                "Confusing NPRI with ORRI - NPRI survives lease, ORRI does not",
                "Assuming NPRI holder can participate in bonus negotiations",
                "Not accounting for NPRI as a burden on the mineral interest",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-005",
            canonical_term="Net Revenue Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "The share of production revenue an interest holder actually receives after "
                "deducting all burdens. For a working interest holder: NRI = WI minus royalty "
                "minus ORRI minus other burdens. NRI represents the bottom-line revenue share "
                "and is the basis for division order preparation and revenue distribution. "
                "NRI is always expressed as a decimal fraction of total production."
            ),
            aliases=["net revenue", "NRI", "revenue interest", "net interest"],
            abbreviations=["NRI", "N.R.I."],
            related_terms=["Working Interest", "Royalty Interest", "Division Order"],
            usage_context=TermUsage.FINANCIAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=[
                "Operator's NRI is 0.75000 (75% of production after burdens)",
                "Division order must reflect each party's NRI precisely",
            ],
            legal_significance="Foundation of revenue distribution; basis for division orders",
            common_mistakes=[
                "Confusing NRI with WI - NRI is after deducting burdens",
                "Forgetting to include NPRI and ORRI when calculating NRI",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-006",
            canonical_term="Mineral Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "Full ownership of the mineral estate including all five constituent rights: "
                "the right to develop (ingress/egress), the executive right (to lease), the right "
                "to bonus, the right to delay rentals, and the right to royalties. A mineral "
                "interest is a real property interest that can be severed from the surface estate "
                "and independently conveyed, inherited, and encumbered."
            ),
            aliases=["mineral estate", "mineral fee", "mineral ownership", "severed minerals"],
            abbreviations=["MI", "M.I."],
            related_terms=["Royalty Interest", "Non-Participating Royalty Interest", "Executive Right", "Surface Estate"],
            antonyms=["Surface Estate"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=[
                "A owns an undivided 1/2 mineral interest in the NW/4 of Section 10",
                "The mineral interest was severed from the surface in 1952",
            ],
            legal_significance="Highest form of mineral ownership; includes full bundle of rights",
            common_mistakes=[
                "Confusing mineral interest with royalty interest",
                "Assuming mineral interest always includes all five rights",
                "Not recognizing that minerals include hydrocarbons and potentially other substances",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-007",
            canonical_term="Non-Executive Mineral Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "A mineral interest from which the executive right has been severed. The holder "
                "retains all mineral interest rights except the right to execute leases. Unlike "
                "NPRI holders, NEMI holders receive bonus, delay rentals, AND royalties. The "
                "executive right holder owes a duty of utmost fair dealing to NEMI holders."
            ),
            aliases=["non-executive mineral", "NEMI", "mineral interest without executive rights"],
            abbreviations=["NEMI"],
            related_terms=["Mineral Interest", "Executive Right", "Non-Participating Royalty Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=[
                "B holds a non-executive mineral interest: receives bonus, rentals, and royalty but cannot lease",
                "Executive right holder must negotiate lease terms with due regard for NEMI holders",
            ],
            legal_significance="Mineral fee interest without executive power; entitled to bonus and delay rentals",
            common_mistakes=[
                "Confusing NEMI with NPRI - NEMI gets bonus and rentals, NPRI does not",
                "Thinking NEMI holder has no rights beyond royalty",
            ],
        ))

        self._register(SemanticTerm(
            term_id="SEM-INT-008",
            canonical_term="Fee Simple Determinable Mineral Interest",
            domain=SemanticDomain.INTEREST_TYPE,
            definition=(
                "A mineral interest that automatically terminates upon the occurrence of a "
                "stated event. The grantor retains a possibility of reverter that becomes "
                "possessory automatically. Common determinable events include cessation of "
                "production or failure to develop within a specified period. Created by language "
                "such as 'so long as,' 'during,' or 'until.'"
            ),
            aliases=["determinable fee minerals", "defeasible minerals", "conditional mineral interest"],
            abbreviations=["FSD"],
            related_terms=["Term Mineral Interest", "Possibility of Reverter", "Mineral Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=[
                "Minerals conveyed 'so long as used for oil and gas purposes'",
                "Upon cessation of production, minerals revert to grantor automatically",
            ],
            legal_significance="Automatic reverter; possibility of reverter exempt from RAP",
            common_mistakes=[
                "Confusing FSD with FSSCS - FSD reverter is automatic, FSSCS requires reentry",
                "Not calendaring the determinable event for monitoring",
            ],
        ))

    # === OWNERSHIP TERMS ==============================================

    def _load_ownership_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-OWN-001",
            canonical_term="Severed Minerals",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "Mineral interests that have been separated from the surface estate through "
                "an express grant or reservation. Once severed, the mineral estate and surface "
                "estate are independently alienable. The mineral estate is dominant over the "
                "surface estate for development purposes."
            ),
            aliases=["separated minerals", "mineral severance", "split estate"],
            related_terms=["Mineral Interest", "Surface Estate", "Accommodation Doctrine"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["Minerals were severed from the surface by the 1948 deed"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-OWN-002",
            canonical_term="Undivided Interest",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "A fractional ownership in the entire mineral estate of a tract, not a specific "
                "geographic portion. Each co-owner of an undivided interest holds a proportionate "
                "share of every mineral beneath the entire tract."
            ),
            aliases=["undivided mineral interest", "fractional undivided interest", "UMI"],
            related_terms=["Partition", "Net Mineral Acres", "Concurrent Ownership"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["A holds an undivided 1/4 interest in all minerals beneath the 640-acre section"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-OWN-003",
            canonical_term="Unleased Minerals",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "Mineral interests that are not currently subject to an oil and gas lease. The "
                "mineral owner holds the full bundle of rights and the executive right is currently "
                "exercisable. Unleased minerals generate no royalty income until a lease is executed."
            ),
            aliases=["open minerals", "unencumbered minerals", "available minerals"],
            antonyms=["Leased Minerals"],
            related_terms=["Mineral Interest", "Executive Right", "Oil and Gas Lease"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["The NE/4 minerals are currently unleased and available for leasing"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-OWN-004",
            canonical_term="Leased Minerals",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "Mineral interests currently subject to an active oil and gas lease. The mineral "
                "owner's rights are limited to receiving royalty, bonus, and delay rentals per "
                "the lease terms. The executive right is not currently exercisable until the "
                "lease terminates."
            ),
            aliases=["encumbered minerals", "minerals under lease", "burdened minerals"],
            antonyms=["Unleased Minerals"],
            related_terms=["Oil and Gas Lease", "Royalty Interest", "Working Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["All minerals in Section 10 are currently leased to XYZ Energy"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-OWN-005",
            canonical_term="Surface Estate",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "The ownership interest in the surface of the land, as distinguished from the "
                "mineral estate. After severance, the surface estate is the servient estate and "
                "must accommodate reasonable mineral operations. The surface owner has no right "
                "to minerals, bonus, delay rentals, or royalty unless specifically provided."
            ),
            aliases=["surface ownership", "surface rights", "surface interest"],
            antonyms=["Mineral Estate"],
            related_terms=["Severed Minerals", "Accommodation Doctrine", "Surface Damage Act"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["Surface estate was sold in 1960 while minerals were reserved"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-OWN-006",
            canonical_term="Community Property Minerals",
            domain=SemanticDomain.OWNERSHIP,
            definition=(
                "Mineral interests acquired during marriage in Texas are presumed community "
                "property. Both spouses must join in conveying community minerals. Income from "
                "separate property minerals is community property. Upon death, surviving spouse "
                "retains their 1/2 and decedent's 1/2 passes by will or intestacy."
            ),
            aliases=["marital minerals", "community mineral interest"],
            related_terms=["Separate Property Minerals", "Probate", "Intestate Succession"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            texas_specific_notes="Texas is a community property state per Tex. Fam. Code \u00a73.002",
            examples=["Minerals acquired by either spouse during marriage are community property"],
        ))

    # === CONVEYANCE TERMS =============================================

    def _load_conveyance_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-CONV-001",
            canonical_term="Mineral Deed",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A deed that conveys a mineral interest including the full bundle of rights: "
                "executive rights, bonus rights, delay rental rights, royalty rights, and "
                "development rights. Distinguished from a royalty deed which conveys only "
                "the right to receive a share of production."
            ),
            aliases=["mineral conveyance", "mineral grant", "deed of minerals"],
            related_terms=["Royalty Deed", "Mineral Interest", "Reservation"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["The 1955 mineral deed conveyed an undivided 1/2 mineral interest to B"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-002",
            canonical_term="Royalty Deed",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A deed that conveys a royalty interest only - the right to receive a share of "
                "production free of costs, without executive rights or participation in bonus "
                "and delay rentals. Critically different from a mineral deed despite sometimes "
                "similar language."
            ),
            aliases=["royalty conveyance", "royalty grant", "deed of royalty"],
            related_terms=["Mineral Deed", "Royalty Interest", "NPRI"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["The royalty deed conveyed a 1/16 royalty interest in all production"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-003",
            canonical_term="Reservation",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A clause in a deed that retains or creates an interest in the grantor. In mineral "
                "law, a reservation creates a new interest in the grantor (e.g., 'reserving unto "
                "grantor 1/2 of all oil, gas, and other minerals'). Distinguished from an exception "
                "which withholds an already-existing interest from the conveyance."
            ),
            aliases=["mineral reservation", "reserved interest", "grantor's reservation"],
            antonyms=["Grant", "Conveyance"],
            related_terms=["Exception", "Mineral Deed", "Duhig Rule"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Grantor reserved 1/2 of the minerals when conveying the surface"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-004",
            canonical_term="Exception",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A clause in a deed that withholds an existing interest from the conveyance. "
                "Distinguished from a reservation which creates a new interest. An exception "
                "recognizes a previously conveyed interest that is not being transferred."
            ),
            aliases=["excepted interest", "excluded interest"],
            related_terms=["Reservation", "Mineral Deed", "Prior Conveyance"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Subject to and excepting the 1/4 mineral interest previously conveyed to C"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-005",
            canonical_term="Assignment",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "The transfer of an interest in an oil and gas lease, typically the working "
                "interest or overriding royalty interest. Assignments may be partial (fractional "
                "or geographic) and may retain overriding royalties. The assignee steps into "
                "the shoes of the assignor with respect to lease obligations."
            ),
            aliases=["lease assignment", "interest assignment", "transfer of interest"],
            related_terms=["Working Interest", "Overriding Royalty Interest", "Oil and Gas Lease"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["Operator assigned 25% of the working interest to a joint venture partner"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-006",
            canonical_term="Quitclaim Deed",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A deed that conveys whatever interest the grantor may have, without warranty "
                "of title. The grantor makes no representation that they own the interest or "
                "that the interest is free of encumbrances. Commonly used in curative work "
                "to clear title defects."
            ),
            aliases=["quit claim", "quitclaim", "release deed"],
            related_terms=["Warranty Deed", "Special Warranty Deed", "Curative"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["Heir executed quitclaim deed to clear title to the mineral interest"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONV-007",
            canonical_term="Duhig Rule",
            domain=SemanticDomain.CONVEYANCE,
            definition=(
                "A rule of deed construction established in Duhig v. Peavy-Moore Lumber Co. "
                "that estops a grantor from claiming a previously reserved mineral interest "
                "when they have conveyed by warranty deed and the warranty would be breached. "
                "If a grantor owns 1/1 minerals, reserves 1/2, conveys by warranty deed without "
                "excepting the prior reservation, the warranty requires the grantor to deliver "
                "clear title; thus the grantor's reservation may be reduced to cure the warranty breach."
            ),
            aliases=["Duhig doctrine", "Duhig estoppel", "warranty deed estoppel"],
            related_terms=["Warranty Deed", "Reservation", "Over-Conveyance"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.EXPERT,
            texas_specific_notes="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            examples=["Duhig analysis required because grantor used warranty deed after prior mineral reservation"],
        ))

    # === FRACTIONAL TERMS =============================================

    def _load_fractional_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-FRAC-001",
            canonical_term="Net Mineral Acres",
            domain=SemanticDomain.MEASUREMENT,
            definition=(
                "The standard unit of measure for mineral ownership. Calculated as gross surface "
                "acres multiplied by the mineral interest fraction. For example, a 1/4 mineral "
                "interest in 640 gross acres equals 160 net mineral acres. NMA represents the "
                "economic value of the mineral ownership position."
            ),
            aliases=["net mineral acre", "mineral acreage", "mineral acre equivalent"],
            abbreviations=["NMA", "N.M.A."],
            related_terms=["Gross Acres", "Mineral Interest", "Net Revenue Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["The interest represents 40 NMA in the 640-acre unit"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-FRAC-002",
            canonical_term="Fractional Interest",
            domain=SemanticDomain.FRACTIONAL,
            definition=(
                "A mineral interest expressed as a fraction of the whole mineral estate. Each "
                "conveyance in the chain of title either creates or modifies fractional interests. "
                "Fractions are multiplicative through the chain: if A owns 1/2 and conveys 1/4 "
                "of their interest to B, B holds 1/8 of the whole."
            ),
            aliases=["fractional mineral interest", "undivided fraction", "aliquot interest"],
            related_terms=["Net Mineral Acres", "Undivided Interest", "Chain of Title"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["B holds a 3/32 fractional mineral interest"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-FRAC-003",
            canonical_term="Double Fraction Problem",
            domain=SemanticDomain.FRACTIONAL,
            definition=(
                "An interpretive problem arising when a deed uses fractional language that could "
                "describe either a fraction of the whole mineral estate or a fraction of a "
                "previously fractional interest. For example, '1/2 of 1/4' could mean 1/8 or "
                "could mean the instrument is trying to convey 1/2 of the grantor's 1/4 interest."
            ),
            aliases=["double fraction", "fraction-of-a-fraction", "stacked fractions"],
            related_terms=["Two-Grant Doctrine", "Mineral Deed Construction", "Fractional Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["Deed language '1/2 of the 1/8 royalty' creates a double fraction problem"],
        ))

    # === POOLING TERMS ================================================

    def _load_pooling_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-POOL-001",
            canonical_term="Pooling",
            domain=SemanticDomain.POOLING,
            definition=(
                "Combining two or more tracts or mineral interests into a single unit for "
                "drilling and production purposes. Pooling dilutes each tract's interest "
                "proportional to its acreage contribution to the unit. Can be voluntary, "
                "compulsory (by RRC order), or pursuant to lease pooling clauses."
            ),
            aliases=["unitization", "communitization", "combining interests"],
            related_terms=["Pooling Clause", "Pugh Clause", "Proration Unit"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["The 160-acre tract was pooled into a 640-acre spacing unit"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-POOL-002",
            canonical_term="Pugh Clause",
            domain=SemanticDomain.POOLING,
            definition=(
                "A lease provision that severs pooled acreage from unpooled acreage so that "
                "production from a pooled unit only holds the pooled portion of the lease. "
                "Without a Pugh clause, production from any part of a pooled unit holds the "
                "entire lease. Horizontal Pugh severs by depth; vertical Pugh severs by area."
            ),
            aliases=["Pugh provision", "freestone rider", "release clause"],
            related_terms=["Pooling", "Depth Severance", "Lease Maintenance"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["Pugh clause requires release of unpooled acreage after primary term"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-POOL-003",
            canonical_term="Proration Unit",
            domain=SemanticDomain.POOLING,
            definition=(
                "The area allocated to a well for production purposes, as designated by the "
                "Railroad Commission of Texas. Typically 40 acres for oil wells and 640 acres "
                "for gas wells, though exceptions are common."
            ),
            aliases=["spacing unit", "drilling unit", "well unit"],
            related_terms=["Pooling", "Spacing Rule", "Railroad Commission"],
            usage_context=TermUsage.REGULATORY,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["RRC assigned a 640-acre proration unit to the gas well"],
        ))

    # === PROBATE TERMS ================================================

    def _load_probate_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-PROB-001",
            canonical_term="Heirship Affidavit",
            domain=SemanticDomain.PROBATE,
            definition=(
                "A sworn statement filed in county deed records identifying the heirs of a "
                "deceased mineral interest owner. Becomes prima facie evidence after 5 years "
                "of record. Not conclusive; weaker than a judicial Determination of Heirship."
            ),
            aliases=["affidavit of heirship", "heirship declaration"],
            related_terms=["Determination of Heirship", "Probate", "Intestate Succession"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            texas_specific_notes="Tex. Est. Code \u00a7203.001",
            examples=["Heirship affidavit identifies three children as sole heirs"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-PROB-002",
            canonical_term="Determination of Heirship",
            domain=SemanticDomain.PROBATE,
            definition=(
                "A judicial proceeding under Tex. Est. Code \u00a7202 to determine the identity "
                "and shares of a decedent's heirs. Provides stronger evidence than an heirship "
                "affidavit and is generally binding on the parties."
            ),
            aliases=["judicial determination", "heirship proceeding", "DHR"],
            related_terms=["Heirship Affidavit", "Probate", "Intestate Succession"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["Court entered Determination of Heirship identifying six heirs"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-PROB-003",
            canonical_term="Per Stirpes Distribution",
            domain=SemanticDomain.PROBATE,
            definition=(
                "A method of distributing a deceased person's estate where each branch of the "
                "family receives an equal share. If a descendant predeceases the decedent, that "
                "descendant's share passes to their children. For mineral interests, this is "
                "the default distribution method under Texas intestacy."
            ),
            aliases=["per stirpes", "by right of representation", "by the branch"],
            related_terms=["Intestate Succession", "Per Capita Distribution"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Three children inherit per stirpes: each receives 1/3 of decedent's mineral interest"],
        ))

    # === LEASING TERMS ================================================

    def _load_leasing_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-LEASE-001",
            canonical_term="Oil and Gas Lease",
            domain=SemanticDomain.LEASING,
            definition=(
                "An agreement granting the lessee the right to explore, develop, and produce "
                "oil and gas from the lessor's mineral interest. Creates a determinable fee in "
                "the lessee (working interest). Has a primary term and continues so long as "
                "production occurs."
            ),
            aliases=["OGL", "mineral lease", "petroleum lease", "oil lease"],
            related_terms=["Working Interest", "Royalty Interest", "Primary Term", "Habendum Clause"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["The 2020 lease provides a 3-year primary term and 1/4 royalty"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-LEASE-002",
            canonical_term="Primary Term",
            domain=SemanticDomain.LEASING,
            definition=(
                "The initial fixed period of an oil and gas lease, typically 3-5 years, during "
                "which the lessee must either begin production or make required delay rental "
                "payments to keep the lease in force. If the lessee fails to act, the lease "
                "terminates at the end of the primary term."
            ),
            aliases=["initial term", "fixed term", "exploration period"],
            related_terms=["Secondary Term", "Delay Rental", "Habendum Clause"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["The 5-year primary term expires on December 31, 2025"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-LEASE-003",
            canonical_term="Division Order",
            domain=SemanticDomain.LEASING,
            definition=(
                "A document specifying the proportionate share of production revenue to which "
                "each interest owner is entitled. Prepared by the operator or purchaser based "
                "on NRI calculations from the title examination. Each interest owner must sign "
                "before receiving revenue."
            ),
            aliases=["DO", "division of interest", "revenue distribution order"],
            related_terms=["Net Revenue Interest", "Title Opinion", "Revenue Distribution"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["Division order reflects each party's decimal interest for revenue distribution"],
        ))

    # === RIGHTS TERMS =================================================

    def _load_rights_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-RIGHT-001",
            canonical_term="Executive Right",
            domain=SemanticDomain.RIGHTS,
            definition=(
                "The right to execute oil and gas leases on the mineral estate. One of the five "
                "constituent rights of mineral ownership. Can be severed and held separately. "
                "When separated, the holder owes a duty of utmost fair dealing to non-executive "
                "mineral and royalty interest holders."
            ),
            aliases=["leasing right", "executive power", "right to lease"],
            abbreviations=["EXEC"],
            related_terms=["Mineral Interest", "Non-Executive Mineral Interest", "Manges v. Guerra"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Executive right holder controls leasing decisions for all mineral interest owners"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-RIGHT-002",
            canonical_term="Bonus Right",
            domain=SemanticDomain.RIGHTS,
            definition=(
                "The right to receive bonus payments upon execution of an oil and gas lease. "
                "One of the five constituent rights of mineral ownership. Bonus is typically "
                "expressed as a per-acre payment (e.g., $5,000/NMA). NPRI holders do not "
                "participate in bonus; NEMI holders do."
            ),
            aliases=["bonus payment right", "lease bonus right"],
            related_terms=["Executive Right", "Delay Rental Right", "Mineral Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["Mineral owner received $5,000/NMA bonus upon executing the lease"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-RIGHT-003",
            canonical_term="Delay Rental Right",
            domain=SemanticDomain.RIGHTS,
            definition=(
                "The right to receive delay rental payments during the primary term of a lease "
                "when the lessee is not drilling. One of the five constituent rights. NPRI "
                "holders do not participate in delay rentals; NEMI holders do."
            ),
            aliases=["rental right", "delay rental payment right"],
            related_terms=["Bonus Right", "Primary Term", "Mineral Interest"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["Annual delay rental of $10/acre maintains the lease during primary term"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-RIGHT-004",
            canonical_term="Development Right",
            domain=SemanticDomain.RIGHTS,
            definition=(
                "The right of ingress and egress to explore, develop, and produce minerals. "
                "Also called the right to develop or the right of entry. Includes the implied "
                "easement to use reasonable amounts of the surface for mineral operations."
            ),
            aliases=["right to develop", "right of ingress and egress", "exploration right"],
            related_terms=["Mineral Interest", "Surface Estate", "Accommodation Doctrine"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.BASIC,
            examples=["Mineral owner exercises development right by entering land to drill"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-RIGHT-005",
            canonical_term="Possibility of Reverter",
            domain=SemanticDomain.RIGHTS,
            definition=(
                "A future interest retained by the grantor of a fee simple determinable estate. "
                "When the determinable event occurs, the interest automatically reverts to the "
                "grantor or their successors. Exempt from the Rule Against Perpetuities in Texas."
            ),
            aliases=["reverter", "right of reverter", "automatic reverter"],
            related_terms=["Fee Simple Determinable", "Term Mineral Interest", "Future Interest"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["Upon cessation of production, the possibility of reverter becomes possessory"],
        ))

    # === MEASUREMENT TERMS ============================================

    def _load_measurement_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-MEAS-001",
            canonical_term="Gross Acres",
            domain=SemanticDomain.MEASUREMENT,
            definition=(
                "The total surface acreage of a tract as described in the legal description, "
                "without regard to fractional mineral ownership. Gross acres multiplied by "
                "mineral interest fraction equals net mineral acres."
            ),
            aliases=["gross surface acres", "total acreage", "survey acreage"],
            related_terms=["Net Mineral Acres", "Legal Description", "Survey"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.BASIC,
            examples=["The NW/4 of Section 10 contains 160 gross acres"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-MEAS-002",
            canonical_term="Royalty Acres",
            domain=SemanticDomain.MEASUREMENT,
            definition=(
                "Net mineral acres multiplied by the applicable lease royalty rate. Represents "
                "the acreage equivalent of the royalty revenue entitlement. Used to compare "
                "royalty positions across tracts with different lease terms."
            ),
            aliases=["royalty acre equivalent", "net royalty acres"],
            abbreviations=["RA"],
            related_terms=["Net Mineral Acres", "Royalty Interest", "Lease Royalty"],
            usage_context=TermUsage.INDUSTRY,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["40 NMA under a 1/4 royalty lease equals 10 royalty acres"],
        ))

    # === FINANCIAL TERMS ==============================================

    def _load_financial_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-FIN-001",
            canonical_term="Bonus Payment",
            domain=SemanticDomain.FINANCIAL,
            definition=(
                "A lump-sum payment made by the lessee to the mineral owner upon execution "
                "of an oil and gas lease. Typically expressed per net mineral acre (e.g., "
                "$5,000/NMA). Paid to mineral interest owners proportionally; NPRI holders "
                "do not participate."
            ),
            aliases=["lease bonus", "signing bonus", "bonus consideration"],
            related_terms=["Bonus Right", "Delay Rental", "Oil and Gas Lease"],
            usage_context=TermUsage.FINANCIAL,
            complexity=TermComplexity.BASIC,
            examples=["$10,000/NMA bonus paid upon lease execution for Wolfcamp A rights"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-FIN-002",
            canonical_term="Delay Rental Payment",
            domain=SemanticDomain.FINANCIAL,
            definition=(
                "A periodic payment made by the lessee to the mineral owner during the primary "
                "term to maintain the lease in force when no drilling operations are being "
                "conducted. Typically paid annually per net mineral acre."
            ),
            aliases=["delay rental", "rental payment", "annual rental"],
            related_terms=["Delay Rental Right", "Primary Term", "Paid-Up Lease"],
            usage_context=TermUsage.FINANCIAL,
            complexity=TermComplexity.BASIC,
            examples=["Annual delay rental of $10/acre keeps the lease alive during year 2"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-FIN-003",
            canonical_term="Shut-In Royalty Payment",
            domain=SemanticDomain.FINANCIAL,
            definition=(
                "A payment made by the lessee to the mineral owner when a well capable of "
                "production is shut in (not producing). Maintains the lease in force during "
                "shut-in periods. The lease must contain a shut-in royalty clause."
            ),
            aliases=["shut-in royalty", "shut-in payment", "SIR"],
            related_terms=["Oil and Gas Lease", "Habendum Clause", "Production"],
            usage_context=TermUsage.FINANCIAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Shut-in royalty of $100/year paid to maintain lease on shut-in gas well"],
        ))

    # === REGULATORY TERMS =============================================

    def _load_regulatory_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-REG-001",
            canonical_term="Railroad Commission of Texas",
            domain=SemanticDomain.REGULATORY,
            definition=(
                "The state agency that regulates oil and gas production in Texas. Administers "
                "spacing rules, pooling orders, production allowables, well permits, and "
                "environmental compliance. Does not determine ownership but its records are "
                "valuable for verification."
            ),
            aliases=["RRC", "Texas Railroad Commission", "TRRC"],
            abbreviations=["RRC", "TRRC"],
            related_terms=["Spacing Rule", "Pooling", "Well Permit"],
            usage_context=TermUsage.REGULATORY,
            complexity=TermComplexity.BASIC,
            texas_specific_notes="Primary oil and gas regulatory authority in Texas",
            examples=["RRC granted spacing exception for horizontal well in Section 10"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-REG-002",
            canonical_term="General Land Office",
            domain=SemanticDomain.REGULATORY,
            definition=(
                "Texas state agency that manages state-owned lands and mineral interests. "
                "Administers the Relinquishment Act and issues mineral leases on state lands. "
                "Maintains land grant and patent records for original Texas land titles."
            ),
            aliases=["GLO", "Texas GLO", "Texas General Land Office"],
            abbreviations=["GLO"],
            related_terms=["Relinquishment Act", "State Mineral Ownership", "Land Patent"],
            usage_context=TermUsage.REGULATORY,
            complexity=TermComplexity.INTERMEDIATE,
            texas_specific_notes="Manages state mineral interests and land patents",
            examples=["GLO records confirm State mineral ownership on the school land tract"],
        ))

    # === SURFACE/MINERAL TERMS ========================================

    def _load_surface_mineral_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-SURMIN-001",
            canonical_term="Accommodation Doctrine",
            domain=SemanticDomain.SURFACE_MINERAL,
            definition=(
                "Legal doctrine requiring the mineral estate owner to accommodate existing "
                "surface uses when reasonable alternative methods of mineral operations exist. "
                "Mineral estate remains dominant but must use due regard for surface rights."
            ),
            aliases=["Getty doctrine", "surface accommodation"],
            related_terms=["Surface Estate", "Mineral Estate", "Surface Damage Act"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            texas_specific_notes="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            examples=["Operator must accommodate existing irrigation use per Getty doctrine"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-SURMIN-002",
            canonical_term="Surface Damage Act",
            domain=SemanticDomain.SURFACE_MINERAL,
            definition=(
                "Texas statute requiring compensation to surface owners for damage caused by "
                "mineral operations. Applies to agricultural land and requires the operator to "
                "negotiate or arbitrate surface damage payments."
            ),
            aliases=["SDA", "surface damage compensation"],
            related_terms=["Accommodation Doctrine", "Surface Estate", "Mineral Operations"],
            usage_context=TermUsage.REGULATORY,
            complexity=TermComplexity.INTERMEDIATE,
            texas_specific_notes="Tex. Nat. Res. Code Ann. \u00a791.402",
            examples=["Operator paid surface damage compensation before drilling operations"],
        ))

    # === TEMPORAL TERMS ===============================================

    def _load_temporal_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-TEMP-001",
            canonical_term="Term Mineral Interest",
            domain=SemanticDomain.TEMPORAL,
            definition=(
                "A mineral interest limited to a specific time duration, after which it "
                "automatically reverts to the grantor. May be fixed term, term-plus-production, "
                "or defeasible term."
            ),
            aliases=["term minerals", "temporary mineral interest", "time-limited minerals"],
            abbreviations=["TERM_MI"],
            related_terms=["Fee Simple Determinable", "Possibility of Reverter", "Life Estate Mineral"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["20-year term mineral interest expires in 2035 unless production saving clause applies"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-TEMP-002",
            canonical_term="Life Estate Mineral Interest",
            domain=SemanticDomain.TEMPORAL,
            definition=(
                "A mineral interest limited to the lifetime of a specified person (measuring "
                "life). Upon the measuring life's death, minerals pass to the remainderman. "
                "Life tenant has limited development rights under the open mine doctrine."
            ),
            aliases=["life estate minerals", "life tenant minerals"],
            abbreviations=["LIFE_MI"],
            related_terms=["Term Mineral Interest", "Remainderman", "Open Mine Doctrine"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            examples=["Mother holds life estate in minerals; upon her death, children take as remaindermen"],
        ))

    # === CONFLICT TERMS ===============================================

    def _load_conflict_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-CONF-001",
            canonical_term="Over-Conveyance",
            domain=SemanticDomain.CONFLICT,
            definition=(
                "A situation where the total mineral interests conveyed from a common source "
                "exceed 100%. Indicates mathematical error, overlapping grants, or Duhig rule "
                "complications. Requires title curative resolution."
            ),
            aliases=["overconveyance", "excess conveyance", "title conflict"],
            related_terms=["Duhig Rule", "Conflict Detection", "Curative"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Interests sum to 108% - over-conveyance detected requiring Duhig analysis"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-CONF-002",
            canonical_term="Title Curative",
            domain=SemanticDomain.CONFLICT,
            definition=(
                "Corrective action taken to resolve title defects in mineral ownership. "
                "Common curative instruments include correction deeds, ratification deeds, "
                "quitclaim deeds, heirship affidavits, and quiet title suits."
            ),
            aliases=["curative", "title correction", "chain repair"],
            related_terms=["Over-Conveyance", "Gap Detection", "Quiet Title"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.INTERMEDIATE,
            examples=["Curative requirement: obtain quitclaim deed from missing heir"],
        ))

    # === TEXAS-SPECIFIC TERMS =========================================

    def _load_texas_specific_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-TX-001",
            canonical_term="Relinquishment Act",
            domain=SemanticDomain.TEXAS_SPECIFIC,
            definition=(
                "Texas statute relinquishing State mineral interests to surface owners for "
                "leasing purposes, with the State retaining a royalty (typically 1/16). Surface "
                "owner acts as State's agent for leasing free royalty lands."
            ),
            aliases=["RA", "free royalty act", "state relinquishment"],
            related_terms=["General Land Office", "State Mineral Ownership", "Free Royalty Land"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.ADVANCED,
            texas_specific_notes="Tex. Nat. Res. Code Ann. \u00a752.171 et seq.",
            examples=["Relinquishment Act allows surface owner to lease State minerals"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-TX-002",
            canonical_term="Mineral Interest Pooling Act",
            domain=SemanticDomain.TEXAS_SPECIFIC,
            definition=(
                "Texas statute authorizing the Railroad Commission to order compulsory pooling "
                "of mineral interests when voluntary pooling cannot be achieved and pooling is "
                "necessary to prevent waste or protect correlative rights."
            ),
            aliases=["MIPA", "forced pooling", "compulsory pooling statute"],
            related_terms=["Pooling", "Railroad Commission", "Correlative Rights"],
            usage_context=TermUsage.REGULATORY,
            complexity=TermComplexity.ADVANCED,
            texas_specific_notes="Tex. Nat. Res. Code Ann. \u00a7102.011 et seq.",
            examples=["RRC entered MIPA order pooling unleased minerals into the spacing unit"],
        ))

    # === LOUISIANA TERMS ==============================================

    def _load_louisiana_terms(self) -> None:
        self._register(SemanticTerm(
            term_id="SEM-LA-001",
            canonical_term="Mineral Servitude",
            domain=SemanticDomain.LOUISIANA_SPECIFIC,
            definition=(
                "A Louisiana civil law concept: a real right to explore, develop, and produce "
                "minerals from another's land. Unlike Texas permanent mineral severance, a "
                "mineral servitude prescribes (extinguishes) after 10 years of non-use."
            ),
            aliases=["servitude minerale", "mineral right (Louisiana)"],
            related_terms=["Prescription", "Mineral Royalty (Louisiana)", "Civil Code"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.EXPERT,
            examples=["The mineral servitude prescribed after 10 years without drilling activity"],
        ))

        self._register(SemanticTerm(
            term_id="SEM-LA-002",
            canonical_term="Prescription",
            domain=SemanticDomain.LOUISIANA_SPECIFIC,
            definition=(
                "In Louisiana civil law, the extinction of a mineral servitude through "
                "non-use for 10 years. Analogous to but fundamentally different from Texas "
                "adverse possession or dormant mineral acts."
            ),
            aliases=["liberative prescription", "prescriptive extinction"],
            related_terms=["Mineral Servitude", "Non-Use", "Louisiana Mineral Code"],
            usage_context=TermUsage.LEGAL,
            complexity=TermComplexity.EXPERT,
            examples=["Mineral servitude prescribed after no operations for 10 years"],
        ))


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_semantic_dict: MineralSemanticDictionary | None = None


def get_semantic_dictionary() -> MineralSemanticDictionary:
    """Get or create the singleton semantic dictionary."""
    global _semantic_dict
    if _semantic_dict is None:
        _semantic_dict = MineralSemanticDictionary()
    return _semantic_dict


def lookup_term(query: str) -> dict[str, Any] | None:
    """Look up a term and return dict representation."""
    d = get_semantic_dictionary()
    term = d.lookup(query)
    return term.to_dict() if term else None


def search_terms(query: str) -> list[dict[str, Any]]:
    """Search for terms matching query."""
    d = get_semantic_dictionary()
    terms = d.search(query)
    return [t.to_dict() for t in terms]


def normalize_interest_type(raw_type: str) -> str:
    """Normalize a raw interest type string to standard abbreviation."""
    d = get_semantic_dictionary()
    return d.normalize_interest_type(raw_type)


def extract_interest_types_from_text(text: str) -> list[str]:
    """Extract interest type references from free text."""
    d = get_semantic_dictionary()
    return d.extract_interest_types(text)


def get_semantic_stats() -> dict[str, Any]:
    """Get statistics about the semantic dictionary."""
    d = get_semantic_dictionary()
    return {
        "total_terms": d.term_count,
        "domains": d.domain_counts,
        "engine": "LM04",
        "version": "1.0.0",
    }
