"""
LM07 Regulatory Filing Engine - Semantic Normalization Module
=============================================================
Domain-specific term normalization for oil and gas regulatory filing,
RRC forms, statewide rules, multi-jurisdiction compliance terms.
Deterministic normalization ensures consistent doctrine cache lookups.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Jurisdiction Enum
# ---------------------------------------------------------------------------
class Jurisdiction(str, Enum):
    TEXAS_RRC = "TX_RRC"
    NEW_MEXICO_OCD = "NM_OCD"
    OKLAHOMA_OCC = "OK_OCC"
    BLM_FEDERAL = "BLM_FED"
    ONRR_FEDERAL = "ONRR_FED"
    TCEQ_STATE = "TCEQ_TX"
    EPA_FEDERAL = "EPA_FED"
    MULTI_JURISDICTION = "MULTI"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Form type classification
# ---------------------------------------------------------------------------
class FormCategory(str, Enum):
    DRILLING_PERMIT = "drilling_permit"
    COMPLETION_REPORT = "completion_report"
    PRODUCTION_REPORT = "production_report"
    INJECTION_DISPOSAL = "injection_disposal"
    PLUGGING_ABANDONMENT = "plugging_abandonment"
    ORGANIZATION = "organization"
    SPACING_EXCEPTION = "spacing_exception"
    FLARING_PERMIT = "flaring_permit"
    OPERATOR_TRANSFER = "operator_transfer"
    ENVIRONMENTAL = "environmental"
    H2S_SAFETY = "h2s_safety"
    PRORATION = "proration"
    FEDERAL_APD = "federal_apd"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Normalization maps
# ---------------------------------------------------------------------------
FORM_ALIASES: dict[str, str] = {
    # W-series (Drilling and Well Operations)
    "w1": "W-1", "w-1": "W-1", "form w-1": "W-1", "drilling permit": "W-1",
    "drill permit": "W-1", "permit to drill": "W-1", "drilling application": "W-1",
    "w1a": "W-1A", "w-1a": "W-1A", "amended drilling permit": "W-1A",
    "amended permit": "W-1A", "w-1 amendment": "W-1A",
    "w2": "W-2", "w-2": "W-2", "form w-2": "W-2", "completion report": "W-2",
    "oil well completion": "W-2", "potential test": "W-2", "well potential": "W-2",
    "recompletion": "W-2", "oil well recompletion": "W-2",
    "w3a": "W-3A", "w-3a": "W-3A", "plugging record": "W-3A",
    "plug record": "W-3A", "plugging report": "W-3A",
    "w3x": "W-3X", "w-3x": "W-3X", "notice of intent to plug": "W-3X",
    "plug notice": "W-3X", "intention to plug": "W-3X", "noi to plug": "W-3X",
    "w14": "W-14", "w-14": "W-14", "cement report": "W-14",
    "cementing report": "W-14",
    # G-series (Gas Wells)
    "g1": "G-1", "g-1": "G-1", "form g-1": "G-1", "gas well completion": "G-1",
    "gas completion": "G-1", "gas well report": "G-1",
    "g10": "G-10", "g-10": "G-10", "certificate of compliance": "G-10",
    "gas oil ratio": "G-10", "gor test": "G-10",
    # H-series (Injection/Disposal)
    "h1": "H-1", "h-1": "H-1", "form h-1": "H-1", "injection permit": "H-1",
    "disposal well permit": "H-1", "injection well permit": "H-1",
    "uic permit": "H-1", "saltwater disposal": "H-1", "swd permit": "H-1",
    "h10": "H-10", "h-10": "H-10", "disposal monitoring": "H-10",
    "monitoring report": "H-10", "injection monitoring": "H-10",
    "h15": "H-15", "h-15": "H-15", "disposal well test": "H-15",
    # P-series (Production and Organization)
    "p1": "P-1", "p-1": "P-1", "form p-1": "P-1", "production report": "P-1",
    "monthly production": "P-1", "lease production": "P-1",
    "p4": "P-4", "p-4": "P-4", "annual potential test": "P-4",
    "oil well potential": "P-4",
    "p5": "P-5", "p-5": "P-5", "organization report": "P-5",
    "org report": "P-5", "operator registration": "P-5",
    "p12": "P-12", "p-12": "P-12", "transfer of allowable": "P-12",
    "allowable transfer": "P-12",
    "p17": "P-17", "p-17": "P-17", "flaring exception": "P-17",
    "flaring permit": "P-17", "flare permit": "P-17",
    # Federal forms
    "apd": "APD", "application for permit to drill": "APD",
    "federal drilling permit": "APD", "blm apd": "APD",
    "sundry notice": "SUNDRY", "sundry": "SUNDRY",
    "form 3160-5": "SUNDRY",
}

RULE_ALIASES: dict[str, str] = {
    "rule 37": "RULE_37", "rule37": "RULE_37", "spacing rule": "RULE_37",
    "well spacing": "RULE_37", "statewide rule 37": "RULE_37",
    "swrule 37": "RULE_37", "spacing": "RULE_37", "minimum spacing": "RULE_37",
    "rule 38": "RULE_38", "rule38": "RULE_38", "density rule": "RULE_38",
    "well density": "RULE_38", "statewide rule 38": "RULE_38",
    "rule 10": "RULE_10", "rule10": "RULE_10", "pollution prevention": "RULE_10",
    "anti-pollution": "RULE_10", "pollution rule": "RULE_10",
    "rule 8": "RULE_8", "rule8": "RULE_8", "water protection": "RULE_8",
    "fresh water protection": "RULE_8",
    "rule 9": "RULE_9", "rule9": "RULE_9", "disposal wells rule": "RULE_9",
    "rule 13": "RULE_13", "rule13": "RULE_13", "casing": "RULE_13",
    "casing requirements": "RULE_13", "casing rule": "RULE_13",
    "rule 14a": "RULE_14A", "rule14a": "RULE_14A", "wellbore integrity": "RULE_14A",
    "rule 14b": "RULE_14B", "rule14b": "RULE_14B", "h2s rule": "RULE_14B",
    "hydrogen sulfide": "RULE_14B", "h2s": "RULE_14B",
    "rule 36": "RULE_36", "rule36": "RULE_36", "oil gas ratio": "RULE_36",
    "gor": "RULE_36",
    "rule 46": "RULE_46", "rule46": "RULE_46", "fluid injection": "RULE_46",
    "injection rule": "RULE_46",
    "rule 51": "RULE_51", "rule51": "RULE_51", "gas flaring": "RULE_51",
    "flaring restrictions": "RULE_51", "venting and flaring": "RULE_51",
}

JURISDICTION_ALIASES: dict[str, Jurisdiction] = {
    "rrc": Jurisdiction.TEXAS_RRC, "railroad commission": Jurisdiction.TEXAS_RRC,
    "texas rrc": Jurisdiction.TEXAS_RRC, "trrc": Jurisdiction.TEXAS_RRC,
    "tx rrc": Jurisdiction.TEXAS_RRC, "texas railroad commission": Jurisdiction.TEXAS_RRC,
    "commission": Jurisdiction.TEXAS_RRC,
    "ocd": Jurisdiction.NEW_MEXICO_OCD, "nm ocd": Jurisdiction.NEW_MEXICO_OCD,
    "new mexico ocd": Jurisdiction.NEW_MEXICO_OCD, "emnrd": Jurisdiction.NEW_MEXICO_OCD,
    "oil conservation division": Jurisdiction.NEW_MEXICO_OCD,
    "occ": Jurisdiction.OKLAHOMA_OCC, "ok occ": Jurisdiction.OKLAHOMA_OCC,
    "oklahoma corporation commission": Jurisdiction.OKLAHOMA_OCC,
    "oklahoma occ": Jurisdiction.OKLAHOMA_OCC,
    "blm": Jurisdiction.BLM_FEDERAL, "bureau of land management": Jurisdiction.BLM_FEDERAL,
    "federal lease": Jurisdiction.BLM_FEDERAL, "federal land": Jurisdiction.BLM_FEDERAL,
    "onrr": Jurisdiction.ONRR_FEDERAL,
    "office of natural resources revenue": Jurisdiction.ONRR_FEDERAL,
    "royalty reporting": Jurisdiction.ONRR_FEDERAL,
    "tceq": Jurisdiction.TCEQ_STATE, "texas commission on environmental quality": Jurisdiction.TCEQ_STATE,
    "epa": Jurisdiction.EPA_FEDERAL, "environmental protection agency": Jurisdiction.EPA_FEDERAL,
}

DOMAIN_SYNONYMS: dict[str, list[str]] = {
    "drilling_permit": ["drilling permit", "permit to drill", "drill permit", "w-1", "apd", "spud"],
    "completion": ["completion", "complete", "completed", "initial potential", "ip", "w-2", "g-1"],
    "production": ["production", "producing", "output", "p-1", "monthly report", "allowable"],
    "injection": ["injection", "disposal", "saltwater disposal", "swd", "uic", "h-1", "waterflood"],
    "plugging": ["plugging", "plug", "abandonment", "p&a", "pa", "inactive well", "w-3a", "w-3x"],
    "spacing": ["spacing", "rule 37", "distance", "setback", "offset", "density", "rule 38"],
    "flaring": ["flaring", "flare", "venting", "gas capture", "rule 51", "p-17", "curtailment"],
    "environmental": ["environmental", "spill", "leak", "contamination", "remediation", "tceq", "epa"],
    "h2s": ["h2s", "hydrogen sulfide", "sour gas", "sour well", "contingency plan", "rule 14b"],
    "operator": ["operator", "organization", "p-5", "transfer", "p-12", "operator number"],
    "proration": ["proration", "allowable", "schedule", "allocation", "curtailment"],
    "federal": ["federal", "blm", "onrr", "apd", "federal lease", "indian land", "tribal"],
    "casing": ["casing", "cementing", "surface casing", "production casing", "rule 13", "w-14"],
    "wellbore_integrity": ["wellbore integrity", "mit", "mechanical integrity", "rule 14a", "annular pressure"],
}


@dataclass
class NormalizedQuery:
    """Result of semantic normalization."""
    original: str
    normalized: str
    jurisdiction: Jurisdiction
    form_types: list[str]
    statewide_rules: list[str]
    form_category: FormCategory
    domain_topics: list[str]
    keywords: list[str]
    is_multi_jurisdiction: bool
    confidence: float


# ---------------------------------------------------------------------------
# Normalizer
# ---------------------------------------------------------------------------
class SemanticNormalizer:
    """Normalize regulatory filing queries for deterministic doctrine lookup."""

    def __init__(self) -> None:
        self._form_pattern = re.compile(
            r"\b(W-?1A?|W-?2|W-?3[AX]|W-?14|G-?1|G-?10|H-?1|H-?10|H-?15|"
            r"P-?1|P-?4|P-?5|P-?12|P-?17|APD|SUNDRY)\b",
            re.IGNORECASE,
        )
        self._rule_pattern = re.compile(
            r"\b(?:statewide\s+)?rule\s*(\d+[A-Z]?)\b",
            re.IGNORECASE,
        )
        self._api_pattern = re.compile(
            r"\b(\d{2}-\d{3}-\d{5})\b",
        )
        self._lease_pattern = re.compile(
            r"\b(\d{5,8})\b",
        )
        logger.info("LM07 SemanticNormalizer initialized with {} form aliases, {} rule aliases",
                     len(FORM_ALIASES), len(RULE_ALIASES))

    def normalize(self, query: str) -> NormalizedQuery:
        """Normalize a regulatory filing query."""
        lower = query.lower().strip()
        normalized = self._clean_text(lower)

        jurisdiction = self._detect_jurisdiction(normalized)
        form_types = self._extract_forms(normalized)
        rules = self._extract_rules(normalized)
        category = self._classify_form_category(form_types, normalized)
        topics = self._extract_domain_topics(normalized)
        keywords = self._extract_keywords(normalized)
        is_multi = self._check_multi_jurisdiction(normalized)

        if is_multi:
            jurisdiction = Jurisdiction.MULTI_JURISDICTION

        confidence = self._compute_normalization_confidence(
            form_types, rules, jurisdiction, topics
        )

        result = NormalizedQuery(
            original=query,
            normalized=normalized,
            jurisdiction=jurisdiction,
            form_types=form_types,
            statewide_rules=rules,
            form_category=category,
            domain_topics=topics,
            keywords=keywords,
            is_multi_jurisdiction=is_multi,
            confidence=confidence,
        )

        logger.debug(
            "Normalized query: forms={}, rules={}, jurisdiction={}, topics={}, confidence={}",
            form_types, rules, jurisdiction.value, topics, confidence,
        )
        return result

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s\-./]", "", text)
        return text.strip()

    def _detect_jurisdiction(self, text: str) -> Jurisdiction:
        for alias, jurisdiction in JURISDICTION_ALIASES.items():
            if alias in text:
                return jurisdiction
        # RRC forms imply Texas jurisdiction
        rrc_forms = {"w-1", "w-2", "w-3a", "w-3x", "g-1", "g-10", "h-1", "p-1", "p-4", "p-5"}
        for form in rrc_forms:
            if form in text:
                return Jurisdiction.TEXAS_RRC
        if "apd" in text or "blm" in text or "federal" in text:
            return Jurisdiction.BLM_FEDERAL
        return Jurisdiction.UNKNOWN

    def _extract_forms(self, text: str) -> list[str]:
        forms: list[str] = []
        # Check explicit pattern matches
        for match in self._form_pattern.finditer(text):
            raw = match.group(1).upper()
            normalized_form = raw.replace(" ", "")
            if not normalized_form.startswith("W-") and normalized_form.startswith("W"):
                normalized_form = "W-" + normalized_form[1:]
            if not normalized_form.startswith("G-") and normalized_form.startswith("G"):
                normalized_form = "G-" + normalized_form[1:]
            if not normalized_form.startswith("H-") and normalized_form.startswith("H"):
                normalized_form = "H-" + normalized_form[1:]
            if not normalized_form.startswith("P-") and normalized_form.startswith("P"):
                normalized_form = "P-" + normalized_form[1:]
            if normalized_form not in forms:
                forms.append(normalized_form)

        # Check aliases
        for alias, canonical in FORM_ALIASES.items():
            if alias in text and canonical not in forms:
                forms.append(canonical)

        return forms

    def _extract_rules(self, text: str) -> list[str]:
        rules: list[str] = []
        for match in self._rule_pattern.finditer(text):
            rule_num = match.group(1).upper()
            canonical = f"RULE_{rule_num}"
            if canonical not in rules:
                rules.append(canonical)
        for alias, canonical in RULE_ALIASES.items():
            if alias in text and canonical not in rules:
                rules.append(canonical)
        return rules

    def _classify_form_category(self, forms: list[str], text: str) -> FormCategory:
        if "W-1A" in forms:
            return FormCategory.DRILLING_PERMIT
        if "W-1" in forms:
            return FormCategory.DRILLING_PERMIT
        if "W-2" in forms or "G-1" in forms:
            return FormCategory.COMPLETION_REPORT
        if "P-1" in forms or "P-4" in forms:
            return FormCategory.PRODUCTION_REPORT
        if "H-1" in forms or "H-10" in forms:
            return FormCategory.INJECTION_DISPOSAL
        if "W-3A" in forms or "W-3X" in forms:
            return FormCategory.PLUGGING_ABANDONMENT
        if "P-5" in forms:
            return FormCategory.ORGANIZATION
        if "P-17" in forms:
            return FormCategory.FLARING_PERMIT
        if "P-12" in forms:
            return FormCategory.OPERATOR_TRANSFER
        if "APD" in forms:
            return FormCategory.FEDERAL_APD

        # Fallback to text analysis
        if any(w in text for w in ["drilling permit", "permit to drill", "spud"]):
            return FormCategory.DRILLING_PERMIT
        if any(w in text for w in ["completion", "ip test", "initial potential"]):
            return FormCategory.COMPLETION_REPORT
        if any(w in text for w in ["production report", "monthly production"]):
            return FormCategory.PRODUCTION_REPORT
        if any(w in text for w in ["injection", "disposal", "saltwater", "swd"]):
            return FormCategory.INJECTION_DISPOSAL
        if any(w in text for w in ["plugging", "abandonment", "p&a", "inactive"]):
            return FormCategory.PLUGGING_ABANDONMENT
        if any(w in text for w in ["spacing", "rule 37", "rule 38", "density"]):
            return FormCategory.SPACING_EXCEPTION
        if any(w in text for w in ["flaring", "flare", "venting", "curtailment"]):
            return FormCategory.FLARING_PERMIT
        if any(w in text for w in ["environmental", "spill", "tceq", "epa"]):
            return FormCategory.ENVIRONMENTAL
        if any(w in text for w in ["h2s", "hydrogen sulfide", "sour gas"]):
            return FormCategory.H2S_SAFETY
        if any(w in text for w in ["proration", "allowable", "schedule"]):
            return FormCategory.PRORATION

        return FormCategory.UNKNOWN

    def _extract_domain_topics(self, text: str) -> list[str]:
        topics: list[str] = []
        for topic, synonyms in DOMAIN_SYNONYMS.items():
            for syn in synonyms:
                if syn in text:
                    if topic not in topics:
                        topics.append(topic)
                    break
        return topics

    def _extract_keywords(self, text: str) -> list[str]:
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "under", "about",
            "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more", "most",
            "other", "some", "such", "no", "only", "own", "same", "than", "too",
            "very", "just", "because", "if", "when", "what", "how", "which",
            "who", "whom", "this", "that", "these", "those", "i", "me", "my",
            "we", "our", "you", "your", "he", "him", "his", "she", "her", "it",
            "its", "they", "them", "their",
        }
        words = re.findall(r"\b[a-z][a-z0-9\-]{2,}\b", text)
        return [w for w in words if w not in stop_words][:30]

    def _check_multi_jurisdiction(self, text: str) -> bool:
        jurisdictions_found: set[Jurisdiction] = set()
        for alias, jurisdiction in JURISDICTION_ALIASES.items():
            if alias in text:
                jurisdictions_found.add(jurisdiction)
        return len(jurisdictions_found) > 1

    def _compute_normalization_confidence(
        self,
        forms: list[str],
        rules: list[str],
        jurisdiction: Jurisdiction,
        topics: list[str],
    ) -> float:
        score = 0.3  # base
        if forms:
            score += 0.25
        if rules:
            score += 0.15
        if jurisdiction != Jurisdiction.UNKNOWN:
            score += 0.15
        if topics:
            score += min(0.15, len(topics) * 0.05)
        return min(1.0, score)

    def extract_api_numbers(self, text: str) -> list[str]:
        """Extract API well numbers (XX-XXX-XXXXX format)."""
        return self._api_pattern.findall(text)

    def normalize_form_name(self, form: str) -> Optional[str]:
        """Normalize a single form name to canonical form."""
        lower = form.lower().strip()
        if lower in FORM_ALIASES:
            return FORM_ALIASES[lower]
        upper = form.upper().strip().replace(" ", "")
        if re.match(r"^[WGHP]-?\d+[A-Z]?$", upper):
            return upper
        return None

    def normalize_rule_reference(self, rule: str) -> Optional[str]:
        """Normalize a statewide rule reference."""
        lower = rule.lower().strip()
        if lower in RULE_ALIASES:
            return RULE_ALIASES[lower]
        match = re.match(r"rule\s*(\d+[a-z]?)", lower)
        if match:
            return f"RULE_{match.group(1).upper()}"
        return None
