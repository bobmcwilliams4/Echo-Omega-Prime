"""
LM17 Pipeline ROW Engine - Semantic Normalization Module
=========================================================
Domain-specific term normalization, synonym resolution, abbreviation
expansion, and deterministic text processing for pipeline right-of-way
intelligence queries.

Engine ID: LM17 | Port: 8517
TIE Gold Standard Semantic Normalization
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from enum import Enum
from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# CONSTANTS
# ============================================================================

ENGINE_ID: str = "LM17"
ENGINE_NAME: str = "Pipeline ROW"


class NormalizationMode(str, Enum):
    """Normalization strictness modes."""
    STRICT = "strict"
    STANDARD = "standard"
    PERMISSIVE = "permissive"


# ============================================================================
# SYNONYM / ABBREVIATION MAPS
# ============================================================================

PIPELINE_ROW_SYNONYMS: dict[str, str] = {
    # ROW terminology
    "right of way": "right-of-way",
    "right-of way": "right-of-way",
    "right of-way": "right-of-way",
    "r/w": "right-of-way",
    "r.o.w.": "right-of-way",
    "row easement": "right-of-way easement",
    "pipeline easement": "pipeline right-of-way easement",
    "pipe line": "pipeline",
    "pipe-line": "pipeline",
    # Regulatory bodies
    "ferc": "Federal Energy Regulatory Commission",
    "phmsa": "Pipeline and Hazardous Materials Safety Administration",
    "tceq": "Texas Commission on Environmental Quality",
    "usace": "United States Army Corps of Engineers",
    "usfws": "United States Fish and Wildlife Service",
    "epa": "Environmental Protection Agency",
    "txdot": "Texas Department of Transportation",
    "rrc": "Railroad Commission of Texas",
    "nrc": "Natural Resources Code",
    "txnrc": "Texas Natural Resources Code",
    "dot": "Department of Transportation",
    "osha": "Occupational Safety and Health Administration",
    "boe": "barrels of oil equivalent",
    "mcf": "thousand cubic feet",
    "mmcf": "million cubic feet",
    "bbls": "barrels",
    # Pipeline types
    "gathering line": "gathering pipeline",
    "transmission line": "transmission pipeline",
    "trunkline": "trunk pipeline",
    "trunk line": "trunk pipeline",
    "flowline": "flow line",
    "flow-line": "flow line",
    "lateral line": "lateral pipeline",
    "header system": "header pipeline system",
    # Crossing types
    "hdd": "horizontal directional drilling",
    "horizontal directional drill": "horizontal directional drilling",
    "open cut": "open-cut crossing",
    "open-cut": "open-cut crossing",
    "bore and jack": "bore-and-jack crossing",
    "jack and bore": "bore-and-jack crossing",
    "direct pipe": "direct pipe installation",
    # Legal terms
    "eminent domain": "eminent domain",
    "condemnation": "condemnation proceeding",
    "quick take": "quick-take condemnation",
    "common carrier": "common carrier pipeline",
    "certificate of convenience": "certificate of public convenience and necessity",
    "cpcn": "certificate of public convenience and necessity",
    "section 7": "Natural Gas Act Section 7 certificate",
    "nga section 7": "Natural Gas Act Section 7 certificate",
    "nga": "Natural Gas Act",
    # Environmental
    "section 404": "Clean Water Act Section 404 permit",
    "cwa 404": "Clean Water Act Section 404 permit",
    "section 106": "National Historic Preservation Act Section 106 review",
    "nhpa": "National Historic Preservation Act",
    "nepa": "National Environmental Policy Act",
    "esa section 7": "Endangered Species Act Section 7 consultation",
    "esa": "Endangered Species Act",
    "eis": "environmental impact statement",
    "ea": "environmental assessment",
    "fonsi": "finding of no significant impact",
    "biological assessment": "biological assessment",
    "ba": "biological assessment",
    "bo": "biological opinion",
    "nwp": "nationwide permit",
    "ip": "individual permit",
    "wetland delineation": "wetlands delineation",
    "wotus": "waters of the United States",
    # Easement terms
    "permanent easement": "permanent right-of-way easement",
    "temporary workspace": "temporary work space easement",
    "tws": "temporary work space easement",
    "atws": "additional temporary work space",
    "extra workspace": "additional temporary work space",
    "cathodic protection": "cathodic protection easement",
    "cp rectifier": "cathodic protection rectifier",
    "cp": "cathodic protection",
    # Damage terms
    "crop damage": "crop loss compensation",
    "surface damage": "surface damage compensation",
    "diminution in value": "diminution-in-value damages",
    "loss of use": "loss-of-use damages",
    "restoration": "surface restoration",
    # Pipeline operations
    "pig": "pipeline inspection gauge",
    "pigging": "pipeline inspection gauge run",
    "smart pig": "inline inspection tool",
    "ili": "inline inspection",
    "hydrostatic test": "hydrostatic pressure test",
    "hydrotest": "hydrostatic pressure test",
    "commissioning": "pipeline commissioning",
    "decommissioning": "pipeline decommissioning",
    "purge and fill": "purge-and-fill operation",
    # Abandonment
    "abandon in place": "abandonment in place",
    "aip": "abandonment in place",
    "abandon by removal": "abandonment by removal",
    "pipeline removal": "abandonment by removal",
}

ABBREVIATION_EXPANSIONS: dict[str, str] = {
    "ROW": "right-of-way",
    "FERC": "Federal Energy Regulatory Commission",
    "PHMSA": "Pipeline and Hazardous Materials Safety Administration",
    "TCEQ": "Texas Commission on Environmental Quality",
    "USACE": "United States Army Corps of Engineers",
    "CFR": "Code of Federal Regulations",
    "NGA": "Natural Gas Act",
    "CWA": "Clean Water Act",
    "ESA": "Endangered Species Act",
    "NEPA": "National Environmental Policy Act",
    "NHPA": "National Historic Preservation Act",
    "EIS": "Environmental Impact Statement",
    "EA": "Environmental Assessment",
    "FONSI": "Finding of No Significant Impact",
    "HDD": "horizontal directional drilling",
    "NWP": "Nationwide Permit",
    "IP": "Individual Permit",
    "TWS": "temporary work space",
    "ATWS": "additional temporary work space",
    "CP": "cathodic protection",
    "ILI": "inline inspection",
    "DOT": "Department of Transportation",
    "OSHA": "Occupational Safety and Health Administration",
    "CPCN": "certificate of public convenience and necessity",
    "RRC": "Railroad Commission of Texas",
    "NRC": "Natural Resources Code",
    "MAOP": "maximum allowable operating pressure",
    "MOP": "maximum operating pressure",
    "SMYS": "specified minimum yield strength",
    "OD": "outside diameter",
    "ID": "inside diameter",
    "WT": "wall thickness",
    "API": "American Petroleum Institute",
    "ASME": "American Society of Mechanical Engineers",
    "NACE": "National Association of Corrosion Engineers",
    "USDOT": "United States Department of Transportation",
    "AIP": "abandonment in place",
    "BLM": "Bureau of Land Management",
    "SCS": "Soil Conservation Service",
    "NRCS": "Natural Resources Conservation Service",
    "SHPO": "State Historic Preservation Officer",
    "THPO": "Tribal Historic Preservation Officer",
    "TCP": "traditional cultural property",
    "APE": "area of potential effects",
}

STATUTE_PATTERNS: dict[str, str] = {
    r"49\s*cfr\s*19[0-9]": "49 CFR Parts 190-199 (PHMSA Pipeline Safety Regulations)",
    r"49\s*cfr\s*192": "49 CFR Part 192 (Transportation of Natural and Other Gas by Pipeline)",
    r"49\s*cfr\s*195": "49 CFR Part 195 (Transportation of Hazardous Liquids by Pipeline)",
    r"tex\.?\s*nat\.?\s*res\.?\s*code.*111": "Texas Natural Resources Code Chapter 111 (Common Carrier Pipelines)",
    r"tex\.?\s*nat\.?\s*res\.?\s*code.*117": "Texas Natural Resources Code Chapter 117 (Gas Utilities Pipelines)",
    r"tex\.?\s*prop\.?\s*code.*21": "Texas Property Code Chapter 21 (Eminent Domain)",
    r"tex\.?\s*util\.?\s*code": "Texas Utilities Code",
    r"15\s*usc\s*717": "15 USC 717 (Natural Gas Act)",
    r"33\s*usc\s*1344": "33 USC 1344 (Clean Water Act Section 404)",
    r"16\s*usc\s*470": "16 USC 470 (National Historic Preservation Act)",
    r"16\s*usc\s*1536": "16 USC 1536 (Endangered Species Act Section 7)",
    r"42\s*usc\s*4321": "42 USC 4321 (National Environmental Policy Act)",
    r"18\s*cfr\s*157": "18 CFR Part 157 (FERC Applications for Certificates of Public Convenience)",
    r"18\s*cfr\s*380": "18 CFR Part 380 (FERC Environmental Review Regulations)",
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class NormalizationResult(BaseModel):
    """Result of semantic normalization."""
    original_text: str
    normalized_text: str
    mode: NormalizationMode
    synonyms_applied: list[dict[str, str]] = Field(default_factory=list)
    abbreviations_expanded: list[dict[str, str]] = Field(default_factory=list)
    statutes_identified: list[str] = Field(default_factory=list)
    normalization_hash: str = ""
    keyword_tokens: list[str] = Field(default_factory=list)
    domain_entities: list[str] = Field(default_factory=list)


class SemanticMatch(BaseModel):
    """A semantic match result for doctrine lookup."""
    query_normalized: str
    matched_keywords: list[str]
    match_score: float
    topic: str
    category: str


# ============================================================================
# NORMALIZER CLASS
# ============================================================================

class PipelineROWNormalizer:
    """
    Deterministic semantic normalizer for pipeline right-of-way domain queries.
    Handles synonym resolution, abbreviation expansion, statute identification,
    and keyword extraction specific to pipeline ROW acquisition and compliance.
    """

    def __init__(self, mode: NormalizationMode = NormalizationMode.STANDARD) -> None:
        self._mode = mode
        self._synonym_map = {k.lower(): v for k, v in PIPELINE_ROW_SYNONYMS.items()}
        self._abbreviation_map = dict(ABBREVIATION_EXPANSIONS)
        self._statute_patterns = {re.compile(k, re.IGNORECASE): v for k, v in STATUTE_PATTERNS.items()}
        self._stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "shall",
            "should", "may", "might", "can", "could", "must", "need", "to", "of",
            "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
            "during", "before", "after", "above", "below", "between", "under",
            "about", "than", "but", "or", "and", "not", "no", "nor", "if", "then",
            "that", "this", "these", "those", "it", "its", "we", "our", "you",
            "your", "they", "their", "what", "which", "who", "whom", "how", "when",
            "where", "why", "all", "each", "every", "both", "few", "more", "most",
            "other", "some", "such", "only", "same", "so", "very",
        }
        logger.debug("PipelineROWNormalizer initialized | mode={}", mode.value)

    def normalize(self, text: str) -> NormalizationResult:
        """Normalize a query text through the full pipeline."""
        original = text.strip()
        if not original:
            return NormalizationResult(
                original_text=original,
                normalized_text="",
                mode=self._mode,
                normalization_hash=hashlib.sha256(b"").hexdigest()[:16],
            )

        working = self._clean_unicode(original)
        working = self._normalize_whitespace(working)

        synonyms_applied: list[dict[str, str]] = []
        working, synonyms_applied = self._apply_synonyms(working)

        abbreviations_expanded: list[dict[str, str]] = []
        working, abbreviations_expanded = self._expand_abbreviations(working)

        statutes = self._identify_statutes(working)
        keywords = self._extract_keywords(working)
        entities = self._extract_domain_entities(working)
        norm_hash = hashlib.sha256(working.lower().encode()).hexdigest()[:16]

        result = NormalizationResult(
            original_text=original,
            normalized_text=working,
            mode=self._mode,
            synonyms_applied=synonyms_applied,
            abbreviations_expanded=abbreviations_expanded,
            statutes_identified=statutes,
            normalization_hash=norm_hash,
            keyword_tokens=keywords,
            domain_entities=entities,
        )
        logger.debug(
            "Normalization complete | synonyms={} abbrevs={} statutes={} keywords={}",
            len(synonyms_applied), len(abbreviations_expanded), len(statutes), len(keywords),
        )
        return result

    def _clean_unicode(self, text: str) -> str:
        """Normalize unicode characters to ASCII-compatible forms."""
        normalized = unicodedata.normalize("NFKD", text)
        cleaned = "".join(
            c for c in normalized
            if unicodedata.category(c) != "Mn" or c in ("-", "'", ".")
        )
        cleaned = re.sub(r'[\u2018\u2019\u201a\u201b]', "'", cleaned)
        cleaned = re.sub(r'[\u201c\u201d\u201e\u201f]', '"', cleaned)
        cleaned = re.sub(r'[\u2013\u2014]', "-", cleaned)
        cleaned = re.sub(r'\u00a7', "Section ", cleaned)
        return cleaned

    def _normalize_whitespace(self, text: str) -> str:
        """Collapse and normalize whitespace."""
        return re.sub(r"\s+", " ", text).strip()

    def _apply_synonyms(self, text: str) -> tuple[str, list[dict[str, str]]]:
        """Apply synonym replacements, longest match first."""
        applied: list[dict[str, str]] = []
        lower_text = text.lower()
        sorted_synonyms = sorted(self._synonym_map.keys(), key=len, reverse=True)
        for synonym in sorted_synonyms:
            if synonym in lower_text:
                replacement = self._synonym_map[synonym]
                pattern = re.compile(re.escape(synonym), re.IGNORECASE)
                if pattern.search(text):
                    text = pattern.sub(replacement, text)
                    applied.append({"original": synonym, "replacement": replacement})
                    lower_text = text.lower()
        return text, applied

    def _expand_abbreviations(self, text: str) -> tuple[str, list[dict[str, str]]]:
        """Expand known abbreviations when they appear as standalone tokens."""
        expanded: list[dict[str, str]] = []
        words = text.split()
        result_words: list[str] = []
        for word in words:
            clean = word.strip(".,;:!?()")
            upper_clean = clean.upper()
            if upper_clean in self._abbreviation_map and clean == clean.upper():
                expansion = self._abbreviation_map[upper_clean]
                expanded.append({"abbreviation": clean, "expansion": expansion})
                new_word = word.replace(clean, f"{clean} ({expansion})")
                result_words.append(new_word)
            else:
                result_words.append(word)
        return " ".join(result_words), expanded

    def _identify_statutes(self, text: str) -> list[str]:
        """Identify statutory references in the text."""
        found: list[str] = []
        for pattern, description in self._statute_patterns.items():
            if pattern.search(text):
                if description not in found:
                    found.append(description)
        return found

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract domain-relevant keywords from text."""
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]|[a-zA-Z]", text.lower())
        keywords: list[str] = []
        for token in tokens:
            if token not in self._stopwords and len(token) > 2:
                if token not in keywords:
                    keywords.append(token)
        return keywords

    def _extract_domain_entities(self, text: str) -> list[str]:
        """Extract pipeline ROW domain entities from text."""
        entities: list[str] = []
        entity_patterns = [
            (r"(?:pipeline|pipe\s*line)\s+(?:right-of-way|easement|crossing|safety)", "pipeline_concept"),
            (r"(?:gathering|transmission|trunk|lateral|flow)\s+(?:line|pipeline)", "pipeline_type"),
            (r"(?:permanent|temporary)\s+(?:easement|workspace|work\s+space)", "easement_type"),
            (r"(?:open-cut|hdd|bore-and-jack|direct\s+pipe)\s+(?:crossing|installation)?", "crossing_method"),
            (r"(?:cathodic\s+protection|inline\s+inspection|hydrostatic\s+test)", "pipeline_operation"),
            (r"(?:eminent\s+domain|condemnation|common\s+carrier)", "legal_concept"),
            (r"(?:section\s+7|section\s+404|section\s+106|section\s+7\s+esa)", "regulatory_section"),
            (r"(?:environmental\s+(?:impact|assessment)|biological\s+(?:assessment|opinion))", "environmental_doc"),
            (r"(?:crop\s+damage|surface\s+damage|diminution|loss\s+of\s+use)", "damage_type"),
            (r"(?:abandon(?:ment)?\s+(?:in\s+place|by\s+removal))", "abandonment_type"),
        ]
        for pattern, entity_type in entity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entity_str = f"{entity_type}:{match.lower().strip()}"
                if entity_str not in entities:
                    entities.append(entity_str)
        return entities

    def compute_semantic_similarity(
        self,
        query_keywords: list[str],
        target_keywords: list[str],
    ) -> float:
        """Compute keyword overlap similarity score between two keyword sets."""
        if not query_keywords or not target_keywords:
            return 0.0
        query_set = set(kw.lower() for kw in query_keywords)
        target_set = set(kw.lower() for kw in target_keywords)
        intersection = query_set & target_set
        union = query_set | target_set
        if not union:
            return 0.0
        jaccard = len(intersection) / len(union)
        coverage = len(intersection) / len(query_set) if query_set else 0.0
        return round(jaccard * 0.4 + coverage * 0.6, 4)

    def match_query_to_topics(
        self,
        query_text: str,
        topic_keyword_map: dict[str, list[str]],
        threshold: float = 0.15,
    ) -> list[SemanticMatch]:
        """Match a normalized query against a map of topic keywords."""
        norm_result = self.normalize(query_text)
        query_keywords = norm_result.keyword_tokens
        matches: list[SemanticMatch] = []
        for topic, keywords in topic_keyword_map.items():
            score = self.compute_semantic_similarity(query_keywords, keywords)
            if score >= threshold:
                matched_kws = [kw for kw in query_keywords if kw.lower() in {k.lower() for k in keywords}]
                matches.append(SemanticMatch(
                    query_normalized=norm_result.normalized_text,
                    matched_keywords=matched_kws,
                    match_score=score,
                    topic=topic,
                    category=self._infer_category(topic),
                ))
        matches.sort(key=lambda m: m.match_score, reverse=True)
        return matches

    def _infer_category(self, topic: str) -> str:
        """Infer issue category from topic name."""
        topic_lower = topic.lower()
        category_map = {
            "acquisition": "ROW_ACQUISITION",
            "easement": "EASEMENT_NEGOTIATION",
            "negotiat": "EASEMENT_NEGOTIATION",
            "ferc": "FERC_COMPLIANCE",
            "certificate": "FERC_COMPLIANCE",
            "eminent": "EMINENT_DOMAIN",
            "condemn": "EMINENT_DOMAIN",
            "crossing": "CROSSING_PERMITS",
            "railroad": "CROSSING_PERMITS",
            "highway": "CROSSING_PERMITS",
            "environment": "ENVIRONMENTAL_PERMITTING",
            "wetland": "ENVIRONMENTAL_PERMITTING",
            "species": "ENVIRONMENTAL_PERMITTING",
            "cultural": "ENVIRONMENTAL_PERMITTING",
            "surface damage": "SURFACE_DAMAGE",
            "crop": "SURFACE_DAMAGE",
            "restor": "SURFACE_DAMAGE",
            "safety": "PIPELINE_SAFETY",
            "phmsa": "PIPELINE_SAFETY",
            "abandon": "ABANDONMENT",
            "removal": "ABANDONMENT",
            "dispute": "DISPUTE_RESOLUTION",
            "complaint": "DISPUTE_RESOLUTION",
            "temporary": "TEMPORARY_WORKSPACE",
            "workspace": "TEMPORARY_WORKSPACE",
            "encroach": "ENCROACHMENT",
        }
        for key, category in category_map.items():
            if key in topic_lower:
                return category
        return "ROW_ACQUISITION"
