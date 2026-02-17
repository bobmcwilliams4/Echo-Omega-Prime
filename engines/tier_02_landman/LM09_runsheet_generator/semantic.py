"""
LM09 Runsheet Generator — Semantic Normalization Module
Engine ID: LM09 | Port: 8509
Domain-specific term normalization for oil & gas title examination,
run sheet generation, and landman terminology.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from loguru import logger


class InstrumentType(str, Enum):
    """Canonical instrument types for title examination."""
    WARRANTY_DEED = "WARRANTY_DEED"
    SPECIAL_WARRANTY_DEED = "SPECIAL_WARRANTY_DEED"
    QUITCLAIM_DEED = "QUITCLAIM_DEED"
    MINERAL_DEED = "MINERAL_DEED"
    ROYALTY_DEED = "ROYALTY_DEED"
    OIL_GAS_LEASE = "OIL_GAS_LEASE"
    ASSIGNMENT = "ASSIGNMENT"
    PARTIAL_ASSIGNMENT = "PARTIAL_ASSIGNMENT"
    RELEASE = "RELEASE"
    PARTIAL_RELEASE = "PARTIAL_RELEASE"
    RATIFICATION = "RATIFICATION"
    CORRECTION_DEED = "CORRECTION_DEED"
    AFFIDAVIT_OF_HEIRSHIP = "AFFIDAVIT_OF_HEIRSHIP"
    PROBATE = "PROBATE"
    PARTITION_DEED = "PARTITION_DEED"
    RIGHT_OF_WAY = "RIGHT_OF_WAY"
    EASEMENT = "EASEMENT"
    SURFACE_LEASE = "SURFACE_LEASE"
    DESIGNATION_OF_POOLED_UNIT = "DESIGNATION_OF_POOLED_UNIT"
    DIVISION_ORDER = "DIVISION_ORDER"
    MEMORANDUM_OF_LEASE = "MEMORANDUM_OF_LEASE"
    SUBORDINATION_AGREEMENT = "SUBORDINATION_AGREEMENT"


INSTRUMENT_ALIASES: dict[str, InstrumentType] = {
    "wd": InstrumentType.WARRANTY_DEED,
    "warranty deed": InstrumentType.WARRANTY_DEED,
    "general warranty deed": InstrumentType.WARRANTY_DEED,
    "gwd": InstrumentType.WARRANTY_DEED,
    "gen warranty deed": InstrumentType.WARRANTY_DEED,
    "swd": InstrumentType.SPECIAL_WARRANTY_DEED,
    "special warranty deed": InstrumentType.SPECIAL_WARRANTY_DEED,
    "spec wd": InstrumentType.SPECIAL_WARRANTY_DEED,
    "qcd": InstrumentType.QUITCLAIM_DEED,
    "quitclaim deed": InstrumentType.QUITCLAIM_DEED,
    "quit claim deed": InstrumentType.QUITCLAIM_DEED,
    "quit-claim deed": InstrumentType.QUITCLAIM_DEED,
    "md": InstrumentType.MINERAL_DEED,
    "mineral deed": InstrumentType.MINERAL_DEED,
    "min deed": InstrumentType.MINERAL_DEED,
    "mineral conveyance": InstrumentType.MINERAL_DEED,
    "rd": InstrumentType.ROYALTY_DEED,
    "royalty deed": InstrumentType.ROYALTY_DEED,
    "royalty conveyance": InstrumentType.ROYALTY_DEED,
    "npri deed": InstrumentType.ROYALTY_DEED,
    "ogl": InstrumentType.OIL_GAS_LEASE,
    "oil and gas lease": InstrumentType.OIL_GAS_LEASE,
    "oil & gas lease": InstrumentType.OIL_GAS_LEASE,
    "o&g lease": InstrumentType.OIL_GAS_LEASE,
    "mineral lease": InstrumentType.OIL_GAS_LEASE,
    "lease": InstrumentType.OIL_GAS_LEASE,
    "ogml": InstrumentType.OIL_GAS_LEASE,
    "asgn": InstrumentType.ASSIGNMENT,
    "assignment": InstrumentType.ASSIGNMENT,
    "assign": InstrumentType.ASSIGNMENT,
    "assignment of ogl": InstrumentType.ASSIGNMENT,
    "assignment of lease": InstrumentType.ASSIGNMENT,
    "partial assignment": InstrumentType.PARTIAL_ASSIGNMENT,
    "partial asgn": InstrumentType.PARTIAL_ASSIGNMENT,
    "pa": InstrumentType.PARTIAL_ASSIGNMENT,
    "rel": InstrumentType.RELEASE,
    "release": InstrumentType.RELEASE,
    "release of ogl": InstrumentType.RELEASE,
    "release of lease": InstrumentType.RELEASE,
    "partial release": InstrumentType.PARTIAL_RELEASE,
    "partial rel": InstrumentType.PARTIAL_RELEASE,
    "pr": InstrumentType.PARTIAL_RELEASE,
    "rat": InstrumentType.RATIFICATION,
    "ratification": InstrumentType.RATIFICATION,
    "ratification of lease": InstrumentType.RATIFICATION,
    "correction deed": InstrumentType.CORRECTION_DEED,
    "corrective deed": InstrumentType.CORRECTION_DEED,
    "cd": InstrumentType.CORRECTION_DEED,
    "aoh": InstrumentType.AFFIDAVIT_OF_HEIRSHIP,
    "affidavit of heirship": InstrumentType.AFFIDAVIT_OF_HEIRSHIP,
    "aff of heirship": InstrumentType.AFFIDAVIT_OF_HEIRSHIP,
    "heirship affidavit": InstrumentType.AFFIDAVIT_OF_HEIRSHIP,
    "heirship aff": InstrumentType.AFFIDAVIT_OF_HEIRSHIP,
    "probate": InstrumentType.PROBATE,
    "will": InstrumentType.PROBATE,
    "order admitting will": InstrumentType.PROBATE,
    "letters testamentary": InstrumentType.PROBATE,
    "muniment of title": InstrumentType.PROBATE,
    "admin deed": InstrumentType.PROBATE,
    "partition deed": InstrumentType.PARTITION_DEED,
    "partition": InstrumentType.PARTITION_DEED,
    "row": InstrumentType.RIGHT_OF_WAY,
    "right of way": InstrumentType.RIGHT_OF_WAY,
    "right-of-way": InstrumentType.RIGHT_OF_WAY,
    "pipeline row": InstrumentType.RIGHT_OF_WAY,
    "easement": InstrumentType.EASEMENT,
    "esmt": InstrumentType.EASEMENT,
    "pipeline easement": InstrumentType.EASEMENT,
    "surface lease": InstrumentType.SURFACE_LEASE,
    "sl": InstrumentType.SURFACE_LEASE,
    "surface use agreement": InstrumentType.SURFACE_LEASE,
    "dpu": InstrumentType.DESIGNATION_OF_POOLED_UNIT,
    "designation of pooled unit": InstrumentType.DESIGNATION_OF_POOLED_UNIT,
    "pooling designation": InstrumentType.DESIGNATION_OF_POOLED_UNIT,
    "unit designation": InstrumentType.DESIGNATION_OF_POOLED_UNIT,
    "do": InstrumentType.DIVISION_ORDER,
    "division order": InstrumentType.DIVISION_ORDER,
    "div order": InstrumentType.DIVISION_ORDER,
    "mol": InstrumentType.MEMORANDUM_OF_LEASE,
    "memorandum of lease": InstrumentType.MEMORANDUM_OF_LEASE,
    "memo of lease": InstrumentType.MEMORANDUM_OF_LEASE,
    "mem of ogl": InstrumentType.MEMORANDUM_OF_LEASE,
    "sub agreement": InstrumentType.SUBORDINATION_AGREEMENT,
    "subordination agreement": InstrumentType.SUBORDINATION_AGREEMENT,
    "subordination": InstrumentType.SUBORDINATION_AGREEMENT,
}


LEGAL_DESCRIPTION_TERMS: dict[str, str] = {
    "sec": "Section",
    "sec.": "Section",
    "section": "Section",
    "sect": "Section",
    "blk": "Block",
    "blk.": "Block",
    "block": "Block",
    "bl": "Block",
    "twp": "Township",
    "twp.": "Township",
    "township": "Township",
    "rng": "Range",
    "rng.": "Range",
    "range": "Range",
    "rge": "Range",
    "surv": "Survey",
    "surv.": "Survey",
    "survey": "Survey",
    "abs": "Abstract",
    "abs.": "Abstract",
    "abstract": "Abstract",
    "abst": "Abstract",
    "a-": "Abstract",
    "lot": "Lot",
    "lt": "Lot",
    "tract": "Tract",
    "tr": "Tract",
    "tr.": "Tract",
    "ptn": "Portion",
    "por": "Portion",
    "portion": "Portion",
    "pt": "Part",
    "n/2": "North Half",
    "s/2": "South Half",
    "e/2": "East Half",
    "w/2": "West Half",
    "ne/4": "Northeast Quarter",
    "nw/4": "Northwest Quarter",
    "se/4": "Southeast Quarter",
    "sw/4": "Southwest Quarter",
    "n 1/2": "North Half",
    "s 1/2": "South Half",
    "e 1/2": "East Half",
    "w 1/2": "West Half",
    "ne 1/4": "Northeast Quarter",
    "nw 1/4": "Northwest Quarter",
    "se 1/4": "Southeast Quarter",
    "sw 1/4": "Southwest Quarter",
    "m&b": "Metes and Bounds",
    "metes & bounds": "Metes and Bounds",
    "metes and bounds": "Metes and Bounds",
    "pob": "Point of Beginning",
    "p.o.b.": "Point of Beginning",
    "poc": "Point of Commencement",
    "p.o.c.": "Point of Commencement",
    "deg": "Degrees",
    "min": "Minutes",
    "ft": "Feet",
    "vrs": "Varas",
    "vr": "Varas",
    "ch": "Chains",
    "chn": "Chains",
    "ac": "Acres",
    "ac.": "Acres",
    "acres": "Acres",
    "nma": "Net Mineral Acres",
    "nra": "Net Royalty Acres",
    "nri": "Net Revenue Interest",
    "wri": "Working Interest",
    "wi": "Working Interest",
    "ori": "Overriding Royalty Interest",
    "orri": "Overriding Royalty Interest",
    "npri": "Non-Participating Royalty Interest",
    "pri": "Participating Royalty Interest",
    "mi": "Mineral Interest",
    "ri": "Royalty Interest",
    "si": "Surface Interest",
}


PARTY_TITLE_TERMS: dict[str, str] = {
    "etal": "et al.",
    "et al": "et al.",
    "et al.": "et al.",
    "etux": "et ux.",
    "et ux": "et ux.",
    "et ux.": "et ux.",
    "etvir": "et vir.",
    "et vir": "et vir.",
    "et vir.": "et vir.",
    "aka": "a/k/a",
    "a/k/a": "a/k/a",
    "also known as": "a/k/a",
    "fka": "f/k/a",
    "f/k/a": "f/k/a",
    "formerly known as": "f/k/a",
    "nka": "n/k/a",
    "n/k/a": "n/k/a",
    "now known as": "n/k/a",
    "dba": "d/b/a",
    "d/b/a": "d/b/a",
    "doing business as": "d/b/a",
    "indiv": "individually",
    "individually": "individually",
    "indv": "individually",
    "trustee": "Trustee",
    "tr": "Trustee",
    "trs": "Trustees",
    "trustees": "Trustees",
    "atty-in-fact": "Attorney-in-Fact",
    "attorney in fact": "Attorney-in-Fact",
    "poa": "Power of Attorney",
    "power of attorney": "Power of Attorney",
    "exec": "Executor",
    "executor": "Executor",
    "executrix": "Executrix",
    "admin": "Administrator",
    "administrator": "Administrator",
    "administratrix": "Administratrix",
    "guardian": "Guardian",
    "gdn": "Guardian",
    "receiver": "Receiver",
    "rcvr": "Receiver",
    "successor": "Successor",
    "succ": "Successor",
    "heir": "Heir",
    "heirs": "Heirs",
    "devisee": "Devisee",
    "devisees": "Devisees",
    "llc": "LLC",
    "l.l.c.": "LLC",
    "lp": "LP",
    "l.p.": "LP",
    "inc": "Inc.",
    "inc.": "Inc.",
    "corp": "Corp.",
    "corp.": "Corp.",
    "co": "Co.",
    "co.": "Co.",
    "ltd": "Ltd.",
    "ltd.": "Ltd.",
}


TITLE_CURATIVE_TERMS: dict[str, str] = {
    "cloud on title": "Cloud on Title",
    "title defect": "Title Defect",
    "curative": "Curative Requirement",
    "curative requirement": "Curative Requirement",
    "cure": "Curative Requirement",
    "gap in chain": "Gap in Chain of Title",
    "break in chain": "Gap in Chain of Title",
    "chain gap": "Gap in Chain of Title",
    "missing link": "Gap in Chain of Title",
    "wild deed": "Wild Deed",
    "wild instrument": "Wild Deed",
    "outside chain": "Instrument Outside Chain",
    "marketable title": "Marketable Title",
    "insurable title": "Insurable Title",
    "merchantable title": "Merchantable Title",
    "good and marketable": "Marketable Title",
    "record title": "Record Title",
    "record owner": "Record Title Owner",
    "apparent owner": "Apparent Owner",
    "common source": "Common Source",
    "sovereignty": "Sovereignty",
    "patent": "Patent from Sovereignty",
    "original grantee": "Original Grantee",
    "original patentee": "Original Patentee",
    "hbp": "Held by Production",
    "held by production": "Held by Production",
    "primary term": "Primary Term",
    "pugh clause": "Pugh Clause",
    "depth severance": "Depth Severance",
    "horizontal pugh": "Horizontal Pugh Clause",
    "vertical pugh": "Vertical Pugh Clause",
    "shut-in": "Shut-in Royalty",
    "cessation clause": "Cessation of Production Clause",
    "continuous drilling": "Continuous Drilling Clause",
    "force majeure": "Force Majeure",
    "top lease": "Top Lease",
    "bottom lease": "Bottom Lease",
    "extension": "Lease Extension",
    "renewal": "Lease Renewal",
    "pooling clause": "Pooling Clause",
    "unitization": "Unitization",
    "unit agreement": "Unit Agreement",
    "communitization": "Communitization Agreement",
    "comm agreement": "Communitization Agreement",
}


@dataclass
class NormalizationResult:
    """Result of normalizing a term or phrase."""
    original: str
    normalized: str
    category: str
    confidence: float
    match_type: str
    alternatives: list[str] = field(default_factory=list)


class SemanticNormalizer:
    """Normalizes landman and title examination terminology to canonical forms."""

    def __init__(self) -> None:
        self._instrument_aliases = {k.lower(): v for k, v in INSTRUMENT_ALIASES.items()}
        self._legal_terms = {k.lower(): v for k, v in LEGAL_DESCRIPTION_TERMS.items()}
        self._party_terms = {k.lower(): v for k, v in PARTY_TITLE_TERMS.items()}
        self._curative_terms = {k.lower(): v for k, v in TITLE_CURATIVE_TERMS.items()}
        self._all_terms: dict[str, tuple[str, str]] = {}
        for k, v in self._instrument_aliases.items():
            self._all_terms[k] = (v.value, "instrument_type")
        for k, v in self._legal_terms.items():
            self._all_terms[k] = (v, "legal_description")
        for k, v in self._party_terms.items():
            self._all_terms[k] = (v, "party_designation")
        for k, v in self._curative_terms.items():
            self._all_terms[k] = (v, "curative_term")
        logger.info("SemanticNormalizer initialized with {} total terms", len(self._all_terms))

    def normalize_instrument_type(self, raw: str) -> NormalizationResult:
        """Normalize an instrument type string to canonical form."""
        cleaned = raw.strip().lower()
        if cleaned in self._instrument_aliases:
            canon = self._instrument_aliases[cleaned]
            return NormalizationResult(
                original=raw,
                normalized=canon.value,
                category="instrument_type",
                confidence=1.0,
                match_type="exact",
            )
        for alias, inst_type in self._instrument_aliases.items():
            if alias in cleaned or cleaned in alias:
                return NormalizationResult(
                    original=raw,
                    normalized=inst_type.value,
                    category="instrument_type",
                    confidence=0.75,
                    match_type="partial",
                    alternatives=[inst_type.value],
                )
        return NormalizationResult(
            original=raw,
            normalized=raw.upper().replace(" ", "_"),
            category="instrument_type",
            confidence=0.3,
            match_type="fallback",
        )

    def normalize_legal_term(self, raw: str) -> NormalizationResult:
        """Normalize a legal description term."""
        cleaned = raw.strip().lower().rstrip(".")
        if cleaned in self._legal_terms:
            return NormalizationResult(
                original=raw,
                normalized=self._legal_terms[cleaned],
                category="legal_description",
                confidence=1.0,
                match_type="exact",
            )
        cleaned_dot = cleaned + "."
        if cleaned_dot in self._legal_terms:
            return NormalizationResult(
                original=raw,
                normalized=self._legal_terms[cleaned_dot],
                category="legal_description",
                confidence=0.95,
                match_type="punctuation_variant",
            )
        return NormalizationResult(
            original=raw,
            normalized=raw.title(),
            category="legal_description",
            confidence=0.3,
            match_type="fallback",
        )

    def normalize_party_designation(self, raw: str) -> NormalizationResult:
        """Normalize party title/designation terms."""
        cleaned = raw.strip().lower()
        if cleaned in self._party_terms:
            return NormalizationResult(
                original=raw,
                normalized=self._party_terms[cleaned],
                category="party_designation",
                confidence=1.0,
                match_type="exact",
            )
        return NormalizationResult(
            original=raw,
            normalized=raw.title(),
            category="party_designation",
            confidence=0.3,
            match_type="fallback",
        )

    def normalize_curative_term(self, raw: str) -> NormalizationResult:
        """Normalize curative/title requirement terms."""
        cleaned = raw.strip().lower()
        if cleaned in self._curative_terms:
            return NormalizationResult(
                original=raw,
                normalized=self._curative_terms[cleaned],
                category="curative_term",
                confidence=1.0,
                match_type="exact",
            )
        for alias, canon in self._curative_terms.items():
            if alias in cleaned:
                return NormalizationResult(
                    original=raw,
                    normalized=canon,
                    category="curative_term",
                    confidence=0.8,
                    match_type="substring",
                )
        return NormalizationResult(
            original=raw,
            normalized=raw.title(),
            category="curative_term",
            confidence=0.3,
            match_type="fallback",
        )

    def normalize_any(self, raw: str) -> NormalizationResult:
        """Attempt normalization across all categories."""
        cleaned = raw.strip().lower()
        if cleaned in self._all_terms:
            canonical, category = self._all_terms[cleaned]
            return NormalizationResult(
                original=raw,
                normalized=canonical,
                category=category,
                confidence=1.0,
                match_type="exact",
            )
        for alias, (canonical, category) in self._all_terms.items():
            if alias in cleaned or cleaned in alias:
                return NormalizationResult(
                    original=raw,
                    normalized=canonical,
                    category=category,
                    confidence=0.7,
                    match_type="partial",
                )
        return NormalizationResult(
            original=raw,
            normalized=raw,
            category="unknown",
            confidence=0.1,
            match_type="no_match",
        )

    def extract_legal_description_components(self, text: str) -> dict[str, Any]:
        """Parse a legal description string into structured components."""
        components: dict[str, Any] = {
            "raw_text": text,
            "section": None,
            "block": None,
            "township": None,
            "range": None,
            "survey": None,
            "abstract_number": None,
            "lot": None,
            "tract": None,
            "subdivision": None,
            "county": None,
            "state": None,
            "acreage": None,
            "aliquot_parts": [],
            "metes_and_bounds": False,
        }
        sec_match = re.search(r"(?:sec(?:tion)?\.?\s*)(\d+)", text, re.IGNORECASE)
        if sec_match:
            components["section"] = sec_match.group(1)
        blk_match = re.search(r"(?:bl(?:oc)?k\.?\s*)([A-Za-z0-9-]+)", text, re.IGNORECASE)
        if blk_match:
            components["block"] = blk_match.group(1)
        twp_match = re.search(r"(?:twp\.?\s*|township\s*)(\d+[NS]?)", text, re.IGNORECASE)
        if twp_match:
            components["township"] = twp_match.group(1)
        rng_match = re.search(r"(?:rng\.?\s*|rge\.?\s*|range\s*)(\d+[EW]?)", text, re.IGNORECASE)
        if rng_match:
            components["range"] = rng_match.group(1)
        surv_match = re.search(r"(?:surv(?:ey)?\.?\s*)([\w\s,]+?)(?:,|\.|$)", text, re.IGNORECASE)
        if surv_match:
            components["survey"] = surv_match.group(1).strip()
        abs_match = re.search(r"(?:abstract|abst|abs)\.?\s*(\d+)", text, re.IGNORECASE)
        if not abs_match:
            abs_match = re.search(r"(?<![A-Za-z])A-(\d+)", text)
        if abs_match:
            components["abstract_number"] = abs_match.group(1)
        lot_match = re.search(r"(?:lot|lt)\.?\s*(\d+)", text, re.IGNORECASE)
        if lot_match:
            components["lot"] = lot_match.group(1)
        tract_match = re.search(r"(?:tract|tr)\.?\s*(\d+)", text, re.IGNORECASE)
        if tract_match:
            components["tract"] = tract_match.group(1)
        ac_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:ac(?:res)?\.?|acres)", text, re.IGNORECASE)
        if ac_match:
            components["acreage"] = float(ac_match.group(1))
        county_match = re.search(r"(\w+)\s+County", text, re.IGNORECASE)
        if county_match:
            components["county"] = county_match.group(1).title()
        aliquot_patterns = [
            (r"[NS]/2", "Half"),
            (r"[EW]/2", "Half"),
            (r"[NS][EW]/4", "Quarter"),
        ]
        for pattern, _ in aliquot_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            components["aliquot_parts"].extend(matches)
        if re.search(r"metes\s*(?:and|&)\s*bounds|[Pp]\.?[Oo]\.?[Bb]\.?|thence|bearing", text, re.IGNORECASE):
            components["metes_and_bounds"] = True
        if "Texas" in text or "TX" in text:
            components["state"] = "Texas"
        return components

    def normalize_party_name(self, name: str) -> str:
        """Normalize a party name for consistent matching."""
        normalized = name.strip()
        normalized = re.sub(r"\s+", " ", normalized)
        for short, canon in self._party_terms.items():
            pattern = re.compile(r"\b" + re.escape(short) + r"\b", re.IGNORECASE)
            normalized = pattern.sub(canon, normalized)
        parts = normalized.split()
        result_parts = []
        for part in parts:
            if part in ("LLC", "LP", "Inc.", "Corp.", "Co.", "Ltd.", "et al.", "et ux.", "et vir.",
                        "a/k/a", "f/k/a", "n/k/a", "d/b/a", "Trustee", "Trustees",
                        "Attorney-in-Fact", "Executor", "Executrix", "Administrator",
                        "Administratrix", "Guardian", "Receiver", "Successor",
                        "Heir", "Heirs", "Devisee", "Devisees", "individually"):
                result_parts.append(part)
            else:
                result_parts.append(part.title() if not part.isupper() or len(part) > 3 else part)
        return " ".join(result_parts)

    def compute_normalization_hash(self, text: str) -> str:
        """Generate a deterministic hash for normalized text."""
        normalized = text.strip().lower()
        normalized = re.sub(r"\s+", " ", normalized)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
