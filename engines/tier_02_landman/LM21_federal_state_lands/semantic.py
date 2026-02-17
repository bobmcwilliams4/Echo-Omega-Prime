"""
LM21 Federal/State Lands Engine - Semantic Normalization Module
================================================================
Domain-specific term normalization for federal and state land oil & gas
leasing, permitting, royalty compliance, environmental review, and
surface management terminology.

Deterministic normalization ensures consistent query routing regardless
of how the user phrases their question.
"""

from __future__ import annotations

import hashlib
import re
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Normalization Maps
# ---------------------------------------------------------------------------

ACRONYM_EXPANSIONS: Dict[str, str] = {
    "BLM": "Bureau of Land Management",
    "ONRR": "Office of Natural Resources Revenue",
    "MMS": "Minerals Management Service",
    "BSEE": "Bureau of Safety and Environmental Enforcement",
    "BOEM": "Bureau of Ocean Energy Management",
    "GLO": "General Land Office",
    "SLO": "State Land Office",
    "NEPA": "National Environmental Policy Act",
    "EA": "Environmental Assessment",
    "EIS": "Environmental Impact Statement",
    "FONSI": "Finding of No Significant Impact",
    "ROD": "Record of Decision",
    "APD": "Application for Permit to Drill",
    "SUPO": "Surface Use Plan of Operations",
    "NOS": "Notice of Staking",
    "CA": "Communitization Agreement",
    "UA": "Unit Agreement",
    "PA": "Participating Area",
    "SOP": "Suspension of Operations and Production",
    "SOO": "Suspension of Operations",
    "SOP_PROD": "Suspension of Production",
    "FLPMA": "Federal Land Policy and Management Act",
    "MLA": "Mineral Leasing Act",
    "ESA": "Endangered Species Act",
    "NHPA": "National Historic Preservation Act",
    "SHPO": "State Historic Preservation Office",
    "THPO": "Tribal Historic Preservation Office",
    "FWS": "Fish and Wildlife Service",
    "USFWS": "United States Fish and Wildlife Service",
    "NFS": "National Forest System",
    "USFS": "United States Forest Service",
    "IRA": "Inflation Reduction Act",
    "PUF": "Permanent University Fund",
    "AUF": "Available University Fund",
    "PSF": "Permanent School Fund",
    "OIG": "Office of Inspector General",
    "GAO": "Government Accountability Office",
    "IBLA": "Interior Board of Land Appeals",
    "CFR": "Code of Federal Regulations",
    "USC": "United States Code",
    "NTL": "Notice to Lessees",
    "OGOR": "Oil and Gas Operations Report",
    "OPR": "Oil and Gas Payor Report",
    "AFMSS": "Automated Fluid Minerals Support System",
    "WIS": "Well Information System",
    "LR2000": "Legacy Rehost 2000",
    "NFMA": "National Forest Management Act",
    "RMP": "Resource Management Plan",
    "AMS": "Allotment Management Plan",
    "COA": "Conditions of Approval",
    "RFD": "Reasonably Foreseeable Development",
    "CX": "Categorical Exclusion",
    "CatEx": "Categorical Exclusion",
    "DN": "Decision Notice",
    "BO": "Biological Opinion",
    "BA": "Biological Assessment",
    "ITS": "Incidental Take Statement",
    "TPWD": "Texas Parks and Wildlife Department",
    "RRC": "Railroad Commission of Texas",
    "NMSLO": "New Mexico State Land Office",
    "OCD": "Oil Conservation Division",
    "BIA": "Bureau of Indian Affairs",
    "AIPRA": "American Indian Probate Reform Act",
    "IOSEA": "Indian Oil and Gas Self-Employment Act",
    "NGL": "Natural Gas Liquids",
    "MCF": "Thousand Cubic Feet",
    "MMCF": "Million Cubic Feet",
    "BBL": "Barrel",
    "MBBL": "Thousand Barrels",
    "BOE": "Barrels of Oil Equivalent",
}

SYNONYM_CLUSTERS: Dict[str, List[str]] = {
    "federal_lease": [
        "federal oil and gas lease", "blm lease", "federal mineral lease",
        "government lease", "public domain lease", "federal onshore lease",
        "bureau of land management lease", "public land lease",
        "federal oil gas lease", "federal og lease",
    ],
    "competitive_lease_sale": [
        "competitive sale", "lease sale", "blm sale", "oral auction",
        "sealed bid sale", "competitive bid", "nomination",
        "expression of interest", "eoi", "competitive offering",
        "parcel nomination", "lease sale parcel",
    ],
    "noncompetitive_lease": [
        "noncompetitive offer", "noncompetitive filing", "over the counter lease",
        "otc lease", "noncompetitive application", "post-sale filing",
        "noncompetitive offer to lease", "noncomp lease",
    ],
    "royalty": [
        "royalty rate", "royalty payment", "royalty obligation",
        "mineral royalty", "production royalty", "overriding royalty",
        "royalty interest", "onrr royalty", "federal royalty",
        "royalty reporting", "royalty valuation",
    ],
    "unit_agreement": [
        "unit", "unitization", "unit agreement", "exploratory unit",
        "participating area", "unit pa", "federal unit",
        "unit expansion", "unit contraction", "committed lands",
    ],
    "communitization": [
        "communitization agreement", "ca", "spacing order",
        "communitized", "communitization application",
        "federal communitization", "state communitization",
    ],
    "apd": [
        "application for permit to drill", "drilling permit",
        "apd application", "permit to drill", "sundry notice",
        "notice of staking", "surface use plan",
        "drilling application", "well permit",
    ],
    "nepa_review": [
        "nepa", "environmental review", "environmental assessment",
        "environmental impact statement", "categorical exclusion",
        "finding of no significant impact", "record of decision",
        "environmental compliance", "nepa process",
    ],
    "split_estate": [
        "split estate", "federal minerals private surface",
        "surface owner notification", "surface owner rights",
        "surface damage", "surface use agreement",
        "split mineral estate", "severed minerals federal",
    ],
    "assignment": [
        "lease assignment", "transfer", "lease transfer",
        "assignment of record title", "operating rights transfer",
        "sublease", "overriding royalty assignment",
        "record title transfer", "partial assignment",
    ],
    "suspension": [
        "suspension", "sop", "suspension of operations",
        "suspension of production", "shut in", "temporarily abandoned",
        "lease suspension", "force majeure suspension",
    ],
    "texas_glo": [
        "texas general land office", "glo lease", "texas state lease",
        "glo mineral lease", "texas school land", "glo royalty",
        "texas state mineral lease", "glo upland lease",
    ],
    "relinquishment_act": [
        "relinquishment act", "texas relinquishment act",
        "relinquishment act lands", "ra lands", "surface owner lease",
        "relinquishment act lease", "surface owner mineral rights",
    ],
    "university_lands": [
        "university lands", "ut system lands", "puf lands",
        "permanent university fund", "university of texas lands",
        "ut land", "university mineral rights",
    ],
    "new_mexico_slo": [
        "new mexico state land office", "nm slo", "new mexico state lease",
        "nm state mineral lease", "new mexico school trust",
        "nm state land lease", "new mexico trust lands",
    ],
    "ira_reform": [
        "inflation reduction act", "ira 2022", "ira reform",
        "federal leasing reform", "royalty rate increase",
        "minimum bid increase", "rental rate increase",
        "bonding reform", "methane fee", "climate provisions",
    ],
    "idle_well": [
        "idle well", "orphaned well", "abandoned well",
        "idle iron", "nonproducing well", "plugging liability",
        "well plugging", "decommissioning", "orphan well program",
    ],
    "national_forest": [
        "national forest", "forest service", "usfs", "nfs lands",
        "forest service consent", "forest service stipulation",
        "national forest system lands", "forest plan",
    ],
    "esa_consultation": [
        "esa section 7", "section 7 consultation", "biological opinion",
        "biological assessment", "incidental take", "endangered species",
        "threatened species", "critical habitat", "jeopardy opinion",
    ],
    "section_106": [
        "section 106", "nhpa", "cultural resources", "historic preservation",
        "archaeological survey", "class iii survey", "cultural compliance",
        "tribal consultation", "traditional cultural property",
    ],
    "reclamation_bond": [
        "reclamation bond", "surface bond", "performance bond",
        "bonding requirement", "nationwide bond", "statewide bond",
        "individual lease bond", "supplemental bond", "idle well bond",
    ],
    "onrr_reporting": [
        "onrr reporting", "royalty reporting", "production reporting",
        "ogor report", "ogor-a", "ogor-b", "payor report",
        "royalty valuation", "arm length transaction",
        "index-based valuation", "gross proceeds",
    ],
}

TERM_NORMALIZATION: Dict[str, str] = {
    "bureau of land management": "BLM",
    "general land office": "GLO",
    "state land office": "SLO",
    "national environmental policy act": "NEPA",
    "endangered species act": "ESA",
    "national historic preservation act": "NHPA",
    "application for permit to drill": "APD",
    "environmental assessment": "EA",
    "environmental impact statement": "EIS",
    "categorical exclusion": "CX",
    "finding of no significant impact": "FONSI",
    "record of decision": "ROD",
    "communitization agreement": "CA",
    "unit agreement": "UA",
    "participating area": "PA",
    "suspension of operations": "SOO",
    "suspension of production": "SOP_PROD",
    "surface use plan of operations": "SUPO",
    "notice of staking": "NOS",
    "inflation reduction act": "IRA",
    "permanent university fund": "PUF",
    "permanent school fund": "PSF",
    "office of natural resources revenue": "ONRR",
    "biological opinion": "BO",
    "biological assessment": "BA",
    "incidental take statement": "ITS",
    "interior board of land appeals": "IBLA",
    "federal land policy and management act": "FLPMA",
    "mineral leasing act": "MLA",
    "resource management plan": "RMP",
    "conditions of approval": "COA",
    "reasonably foreseeable development": "RFD",
}

STATUTE_NORMALIZATION: Dict[str, str] = {
    "30 usc 181": "Mineral Leasing Act Sec 1",
    "30 usc 226": "MLA Sec 17 - Competitive Leasing",
    "30 usc 226-1": "MLA Sec 17 - Fee Increases (IRA)",
    "43 usc 1701": "FLPMA Sec 102 - Declaration of Policy",
    "43 usc 1732": "FLPMA Sec 302 - Management of Public Lands",
    "42 usc 4321": "NEPA Sec 2 - Purpose",
    "42 usc 4332": "NEPA Sec 102 - Policies and Goals",
    "16 usc 1536": "ESA Sec 7 - Interagency Cooperation",
    "54 usc 306108": "NHPA Sec 106 - Program Enhancement",
    "43 cfr 3100": "Oil and Gas Leasing General",
    "43 cfr 3101": "Land Available for Leasing",
    "43 cfr 3103": "Competitive Leasing Fees and Royalties",
    "43 cfr 3106": "Assignment and Transfer of Leases",
    "43 cfr 3107": "Continuation and Extension of Leases",
    "43 cfr 3108": "Lease Relinquishment and Cancellation",
    "43 cfr 3109": "Federal Lease Bonds",
    "43 cfr 3120": "Competitive Lease Sales",
    "43 cfr 3110": "Noncompetitive Leasing",
    "43 cfr 3130": "Oil and Gas Leasing National Petroleum Reserve",
    "43 cfr 3160": "Onshore Oil and Gas Operations",
    "43 cfr 3161": "Jurisdiction and Responsibility",
    "43 cfr 3162": "Requirements for Operating Rights Owners",
    "43 cfr 3165": "Relief Consent and Appeals",
    "43 cfr 3170": "Onshore Oil and Gas Production Accounting",
    "43 cfr 3171": "Measurement and Site Security",
    "43 cfr 3173": "Requirements for Measurement",
    "43 cfr 3174": "Oil Measurement",
    "43 cfr 3175": "Gas Measurement",
    "43 cfr 3180": "Exploratory Unitization Agreements",
    "30 cfr 1202": "Royalties",
    "30 cfr 1206": "Product Valuation",
    "30 cfr 1210": "Reporting and Paying Royalties",
    "30 cfr 1218": "Collection of Royalties Rentals and Other Payments",
    "30 cfr 1228": "Cooperative Activities with States and Indian Tribes",
    "40 cfr 1500": "CEQ NEPA Regulations Purpose Policy and Mandate",
    "40 cfr 1501": "NEPA and Agency Planning",
    "40 cfr 1502": "Environmental Impact Statement",
    "50 cfr 402": "ESA Section 7 Consultation",
    "36 cfr 800": "NHPA Section 106 Process",
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class NormalizationResult(BaseModel):
    """Result of normalizing a query string."""
    original_query: str = Field(description="The raw user query")
    normalized_query: str = Field(description="The cleaned/normalized query")
    detected_acronyms: List[str] = Field(default_factory=list)
    expanded_terms: Dict[str, str] = Field(default_factory=dict)
    matched_clusters: List[str] = Field(default_factory=list)
    detected_statutes: List[str] = Field(default_factory=list)
    keyword_tokens: List[str] = Field(default_factory=list)
    normalization_hash: str = Field(description="SHA-256 of normalized form")


class SemanticMatch(BaseModel):
    """A matched doctrine topic from semantic normalization."""
    cluster_id: str
    confidence: float = Field(ge=0.0, le=1.0)
    matched_terms: List[str] = Field(default_factory=list)
    canonical_form: str = ""


# ---------------------------------------------------------------------------
# Core Normalizer
# ---------------------------------------------------------------------------

class FederalStateLandsNormalizer:
    """
    Deterministic semantic normalizer for federal and state land
    oil & gas domain queries. Converts varied user phrasing into
    canonical forms for consistent doctrine routing.
    """

    def __init__(self) -> None:
        self._acronym_map = ACRONYM_EXPANSIONS
        self._synonym_clusters = SYNONYM_CLUSTERS
        self._term_norm = TERM_NORMALIZATION
        self._statute_norm = STATUTE_NORMALIZATION
        self._cluster_index: Dict[str, Set[str]] = {}
        self._build_cluster_index()
        logger.info(
            "FederalStateLandsNormalizer initialized | "
            f"acronyms={len(self._acronym_map)} | "
            f"clusters={len(self._synonym_clusters)} | "
            f"statutes={len(self._statute_norm)}"
        )

    def _build_cluster_index(self) -> None:
        """Build inverted index from individual tokens to cluster IDs."""
        for cluster_id, synonyms in self._synonym_clusters.items():
            token_set: Set[str] = set()
            for phrase in synonyms:
                for token in phrase.lower().split():
                    if len(token) > 2:
                        token_set.add(token)
            self._cluster_index[cluster_id] = token_set

    def normalize(self, query: str) -> NormalizationResult:
        """
        Full normalization pipeline:
        1. Lowercase and clean
        2. Expand acronyms
        3. Normalize known terms
        4. Match synonym clusters
        5. Detect statute references
        6. Tokenize for keyword matching
        7. Compute determinism hash
        """
        original = query
        cleaned = self._clean_query(query)
        acronyms_found, expanded = self._expand_acronyms(cleaned)
        normalized = self._normalize_terms(expanded)
        clusters = self._match_clusters(normalized)
        statutes = self._detect_statutes(normalized)
        tokens = self._tokenize(normalized)
        norm_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

        result = NormalizationResult(
            original_query=original,
            normalized_query=normalized,
            detected_acronyms=acronyms_found,
            expanded_terms={a: self._acronym_map[a] for a in acronyms_found},
            matched_clusters=[c.cluster_id for c in clusters],
            detected_statutes=statutes,
            keyword_tokens=tokens,
            normalization_hash=norm_hash,
        )
        logger.debug(
            f"Normalized query | clusters={len(clusters)} | "
            f"statutes={len(statutes)} | hash={norm_hash[:12]}"
        )
        return result

    def _clean_query(self, query: str) -> str:
        """Remove extraneous characters, collapse whitespace."""
        text = query.strip()
        text = re.sub(r"[^\w\s\-\.§/(),%]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _expand_acronyms(self, query: str) -> Tuple[List[str], str]:
        """Detect and optionally expand acronyms in the query."""
        found: List[str] = []
        words = query.split()
        for word in words:
            upper = word.upper().strip(".,;:()")
            if upper in self._acronym_map:
                found.append(upper)
        expanded = query
        for acr in found:
            pattern = re.compile(re.escape(acr), re.IGNORECASE)
            expansion = self._acronym_map[acr]
            expanded = pattern.sub(f"{acr} ({expansion})", expanded, count=1)
        return found, expanded

    def _normalize_terms(self, query: str) -> str:
        """Replace long-form terms with their canonical abbreviations."""
        normalized = query.lower()
        for long_form, short_form in sorted(
            self._term_norm.items(), key=lambda x: -len(x[0])
        ):
            normalized = normalized.replace(long_form, short_form.lower())
        return normalized

    def _match_clusters(self, query: str) -> List[SemanticMatch]:
        """Match query against synonym clusters and return ranked results."""
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        matches: List[SemanticMatch] = []

        for cluster_id, synonyms in self._synonym_clusters.items():
            best_score = 0.0
            matched_terms: List[str] = []

            for synonym in synonyms:
                syn_lower = synonym.lower()
                if syn_lower in query_lower:
                    syn_tokens = set(syn_lower.split())
                    score = len(syn_tokens) / max(len(query_tokens), 1)
                    score = min(score * 1.5, 1.0)
                    if score > best_score:
                        best_score = score
                    matched_terms.append(synonym)

            if not matched_terms:
                cluster_tokens = self._cluster_index.get(cluster_id, set())
                overlap = query_tokens & cluster_tokens
                if len(overlap) >= 2:
                    best_score = len(overlap) / max(len(cluster_tokens), 1)
                    best_score = min(best_score, 0.7)
                    matched_terms = list(overlap)

            if best_score > 0.15:
                matches.append(SemanticMatch(
                    cluster_id=cluster_id,
                    confidence=round(best_score, 4),
                    matched_terms=matched_terms,
                    canonical_form=cluster_id,
                ))

        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches[:5]

    def _detect_statutes(self, query: str) -> List[str]:
        """Detect statutory references in the query."""
        found: List[str] = []
        query_lower = query.lower()

        cfr_pattern = re.compile(r"(\d+)\s*cfr\s*([\d\.]+)", re.IGNORECASE)
        for match in cfr_pattern.finditer(query_lower):
            ref = f"{match.group(1)} cfr {match.group(2)}"
            if ref in self._statute_norm:
                found.append(self._statute_norm[ref])
            else:
                found.append(f"{match.group(1)} CFR {match.group(2)}")

        usc_pattern = re.compile(r"(\d+)\s*u\.?s\.?c\.?\s*([\d\-]+)", re.IGNORECASE)
        for match in usc_pattern.finditer(query_lower):
            ref = f"{match.group(1)} usc {match.group(2)}"
            if ref in self._statute_norm:
                found.append(self._statute_norm[ref])
            else:
                found.append(f"{match.group(1)} USC {match.group(2)}")

        section_pattern = re.compile(
            r"section\s+(\d+[a-z]?)\s+(?:of\s+)?(?:the\s+)?"
            r"(mineral leasing act|mla|nepa|esa|nhpa|flpma)",
            re.IGNORECASE,
        )
        for match in section_pattern.finditer(query_lower):
            found.append(f"Section {match.group(1)} of {match.group(2).upper()}")

        return found

    def _tokenize(self, query: str) -> List[str]:
        """Extract meaningful keyword tokens from normalized query."""
        stop_words: FrozenSet[str] = frozenset({
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "of", "in", "to", "for", "with", "on", "at", "from", "by",
            "about", "as", "into", "through", "during", "before", "after",
            "above", "below", "between", "under", "and", "but", "or",
            "not", "no", "nor", "if", "then", "than", "so", "very",
            "just", "also", "how", "what", "when", "where", "which",
            "who", "whom", "this", "that", "these", "those", "it", "its",
        })
        tokens = query.lower().split()
        return [t for t in tokens if t not in stop_words and len(t) > 1]

    def get_cluster_keywords(self, cluster_id: str) -> List[str]:
        """Return all synonyms for a given cluster ID."""
        return self._synonym_clusters.get(cluster_id, [])

    def expand_acronym(self, acronym: str) -> Optional[str]:
        """Expand a single acronym to its full form."""
        return self._acronym_map.get(acronym.upper())

    def get_statute_citation(self, ref: str) -> Optional[str]:
        """Look up a statute reference and return its canonical name."""
        return self._statute_norm.get(ref.lower())

    def compute_query_fingerprint(self, query: str) -> str:
        """
        Compute a deterministic fingerprint for a query that is
        invariant to minor phrasing changes.
        """
        result = self.normalize(query)
        canonical = " ".join(sorted(result.keyword_tokens))
        clusters_str = "|".join(sorted(result.matched_clusters))
        combined = f"{canonical}||{clusters_str}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()
