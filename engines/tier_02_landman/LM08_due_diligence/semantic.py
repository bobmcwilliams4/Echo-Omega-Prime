"""
LM08 Due Diligence Engine - Semantic Normalization Module
==========================================================
Deterministic term normalization for oil & gas acquisition due diligence.
Maps colloquial, regional, and ambiguous terms to canonical representations.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from loguru import logger


class SemanticDomain(str, Enum):
    """Domains for semantic normalization in due diligence context."""
    TITLE = "title"
    ENVIRONMENTAL = "environmental"
    REGULATORY = "regulatory"
    PRODUCTION = "production"
    RESERVES = "reserves"
    LEASE = "lease"
    LIEN = "lien"
    LITIGATION = "litigation"
    PREFERENTIAL_RIGHTS = "preferential_rights"
    CONSENT = "consent"
    CHANGE_OF_CONTROL = "change_of_control"
    AMI = "ami"
    DEFICIENCY = "deficiency"
    PSA = "psa"
    REPS_WARRANTIES = "reps_warranties"
    INDEMNIFICATION = "indemnification"
    NRI_WI = "nri_wi"
    SUSPENSE = "suspense"
    OPERATOR = "operator"


@dataclass
class NormalizationResult:
    """Result of normalizing a term."""
    original: str
    canonical: str
    domain: SemanticDomain
    confidence: float
    aliases_matched: List[str] = field(default_factory=list)
    context_hints: List[str] = field(default_factory=list)
    determinism_hash: str = ""

    def __post_init__(self) -> None:
        raw = f"{self.original}|{self.canonical}|{self.domain.value}"
        self.determinism_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# CANONICAL TERM REGISTRY
# ---------------------------------------------------------------------------
# Each entry: canonical_term -> set of aliases/variants
TERM_REGISTRY: Dict[str, Dict] = {
    # ── TITLE DUE DILIGENCE ──────────────────────────────────────────────
    "title_opinion": {
        "domain": SemanticDomain.TITLE,
        "aliases": {
            "title opinion", "division order title opinion", "doto",
            "drilling title opinion", "dto", "acquisition title opinion",
            "ato", "supplemental title opinion", "sto", "stand-up opinion",
            "title exam", "title examination", "title review",
            "title abstract review", "title check", "preliminary title opinion",
        },
        "context": ["opinion letter from attorney examining chain of title"],
    },
    "chain_of_title": {
        "domain": SemanticDomain.TITLE,
        "aliases": {
            "chain of title", "title chain", "ownership chain",
            "conveyance chain", "title history", "ownership history",
            "succession of title", "derivation of title", "title linkage",
        },
        "context": ["sequential record of conveyances from sovereign to current owner"],
    },
    "title_defect": {
        "domain": SemanticDomain.TITLE,
        "aliases": {
            "title defect", "title requirement", "title objection",
            "title curative", "curative requirement", "deficiency",
            "cloud on title", "title cloud", "title issue",
            "title exception", "title encumbrance", "encumbrance",
            "outstanding interest", "unresolved interest",
        },
        "context": ["deficiency in chain of title requiring corrective action"],
    },
    "mineral_interest": {
        "domain": SemanticDomain.TITLE,
        "aliases": {
            "mineral interest", "mineral estate", "mineral rights",
            "mineral ownership", "subsurface rights", "mineral fee",
            "mineral fee simple", "undivided mineral interest", "umi",
            "severed mineral interest", "reserved mineral interest",
        },
        "context": ["ownership of subsurface minerals, typically severed from surface"],
    },
    "royalty_interest": {
        "domain": SemanticDomain.TITLE,
        "aliases": {
            "royalty interest", "royalty", "overriding royalty interest",
            "orri", "override", "npri", "non-participating royalty interest",
            "non-participating royalty", "carved-out royalty",
            "reserved royalty", "excess royalty", "sliding scale royalty",
        },
        "context": ["right to share in production revenue without cost-bearing obligation"],
    },
    "working_interest": {
        "domain": SemanticDomain.NRI_WI,
        "aliases": {
            "working interest", "wi", "operating interest",
            "leasehold interest", "cost-bearing interest",
            "participating interest", "lessee interest",
        },
        "context": ["right to explore, develop, and operate with proportional cost burden"],
    },
    "net_revenue_interest": {
        "domain": SemanticDomain.NRI_WI,
        "aliases": {
            "net revenue interest", "nri", "net interest",
            "net decimal interest", "revenue interest",
            "decimal interest", "net entitlement",
        },
        "context": ["proportional share of revenue after all burdens deducted from working interest"],
    },

    # ── ENVIRONMENTAL ────────────────────────────────────────────────────
    "phase_i_esa": {
        "domain": SemanticDomain.ENVIRONMENTAL,
        "aliases": {
            "phase i esa", "phase 1 esa", "phase i environmental site assessment",
            "phase 1 environmental", "phase one esa", "phase one environmental",
            "initial environmental assessment", "preliminary environmental review",
            "astm e1527", "astm e1527-21", "all appropriate inquiries", "aai",
            "environmental assessment", "desktop environmental review",
        },
        "context": ["initial assessment to identify recognized environmental conditions"],
    },
    "phase_ii_esa": {
        "domain": SemanticDomain.ENVIRONMENTAL,
        "aliases": {
            "phase ii esa", "phase 2 esa", "phase ii environmental",
            "phase 2 environmental", "phase two esa", "subsurface investigation",
            "soil sampling", "groundwater sampling", "environmental investigation",
            "astm e1903", "site characterization", "intrusive investigation",
        },
        "context": ["subsurface investigation to confirm or deny recognized environmental conditions"],
    },
    "recognized_environmental_condition": {
        "domain": SemanticDomain.ENVIRONMENTAL,
        "aliases": {
            "recognized environmental condition", "rec",
            "environmental condition", "contamination",
            "historical rec", "hrec", "controlled rec", "crec",
            "de minimis condition", "environmental liability",
            "environmental concern", "environmental risk",
        },
        "context": ["presence or likely presence of hazardous substances on a property"],
    },
    "plugging_abandonment": {
        "domain": SemanticDomain.ENVIRONMENTAL,
        "aliases": {
            "plugging and abandonment", "p&a", "pna", "well plugging",
            "well abandonment", "decommissioning", "ard",
            "asset retirement obligation", "aro", "abandonment liability",
            "plugging liability", "abandonment obligation", "plug cost",
            "plug and abandon", "plugging obligation",
        },
        "context": ["obligation to plug, abandon, and remediate well sites"],
    },

    # ── REGULATORY ───────────────────────────────────────────────────────
    "rrc_compliance": {
        "domain": SemanticDomain.REGULATORY,
        "aliases": {
            "rrc compliance", "railroad commission compliance",
            "texas railroad commission", "trrc", "rrc audit",
            "rrc violation", "rrc notice", "p-4 filing", "w-2 filing",
            "h-10 filing", "drilling permit", "rule 37 exception",
            "rule 38 exception", "statewide rule compliance",
        },
        "context": ["compliance with Texas Railroad Commission regulations"],
    },
    "blm_compliance": {
        "domain": SemanticDomain.REGULATORY,
        "aliases": {
            "blm compliance", "bureau of land management",
            "federal lease compliance", "blm audit", "apo",
            "application for permit to drill", "federal drilling permit",
            "federal unit", "communitization agreement", "federal coa",
            "onrr reporting", "onrr compliance",
        },
        "context": ["compliance with BLM and federal lease regulations"],
    },

    # ── PRODUCTION ANALYSIS ──────────────────────────────────────────────
    "decline_curve_analysis": {
        "domain": SemanticDomain.PRODUCTION,
        "aliases": {
            "decline curve analysis", "dca", "decline curve",
            "production decline", "hyperbolic decline",
            "exponential decline", "harmonic decline",
            "arps decline", "arps equation", "b-factor",
            "initial decline rate", "di", "production forecast",
            "type curve", "type curve analysis",
        },
        "context": ["analysis of production rate decline to forecast future production"],
    },
    "production_history": {
        "domain": SemanticDomain.PRODUCTION,
        "aliases": {
            "production history", "historical production",
            "production data", "production records",
            "run tickets", "pipeline statements", "sales volumes",
            "meter readings", "gas balancing", "production allocation",
            "commingled production", "well test data",
        },
        "context": ["historical record of oil, gas, and water production volumes"],
    },

    # ── RESERVE ESTIMATION ───────────────────────────────────────────────
    "proved_reserves": {
        "domain": SemanticDomain.RESERVES,
        "aliases": {
            "proved reserves", "proven reserves", "1p reserves",
            "proved developed producing", "pdp", "proved developed non-producing",
            "pdnp", "pud", "proved undeveloped", "sec reserves",
            "reasonable certainty", "p90 reserves",
        },
        "context": ["reserves estimated with reasonable certainty to be recoverable"],
    },
    "probable_reserves": {
        "domain": SemanticDomain.RESERVES,
        "aliases": {
            "probable reserves", "2p reserves", "p50 reserves",
            "prms probable", "reasonably probable",
            "probable undeveloped", "probable developed",
        },
        "context": ["reserves less certain than proved but more likely than not to be recovered"],
    },
    "reserve_report": {
        "domain": SemanticDomain.RESERVES,
        "aliases": {
            "reserve report", "reserve study", "reserve estimate",
            "reserve evaluation", "engineering report",
            "petroleum engineering report", "independent reserve report",
            "third-party reserve report", "d&m report",
            "ryder scott report", "nsai report", "cga report",
        },
        "context": ["independent engineering evaluation of oil and gas reserves"],
    },

    # ── LEASE STATUS ─────────────────────────────────────────────────────
    "held_by_production": {
        "domain": SemanticDomain.LEASE,
        "aliases": {
            "held by production", "hbp", "continuous production",
            "lease maintained by production", "production in paying quantities",
            "paying quantities", "production sufficient",
            "habendum clause", "secondary term",
        },
        "context": ["lease maintained beyond primary term by production in paying quantities"],
    },
    "lease_expiration": {
        "domain": SemanticDomain.LEASE,
        "aliases": {
            "lease expiration", "lease termination", "lease lapse",
            "primary term expiration", "end of primary term",
            "cessation of production", "cop clause", "temporary cessation",
            "60-day cessation", "90-day cessation", "shut-in royalty",
            "shut-in payment", "dry hole clause",
        },
        "context": ["lease termination due to expiration of primary term or cessation of production"],
    },
    "pooling_unitization": {
        "domain": SemanticDomain.LEASE,
        "aliases": {
            "pooling", "unitization", "pooled unit", "spacing unit",
            "proration unit", "voluntary pooling", "compulsory pooling",
            "force pooling", "forced pooling", "unit declaration",
            "unit agreement", "participating area", "pa designation",
        },
        "context": ["combining multiple leasehold tracts into a single drilling or production unit"],
    },

    # ── LIEN & ENCUMBRANCE ───────────────────────────────────────────────
    "lien_search": {
        "domain": SemanticDomain.LIEN,
        "aliases": {
            "lien search", "ucc search", "ucc filing", "ucc-1",
            "financing statement", "security interest",
            "judgment lien", "tax lien", "federal tax lien",
            "mechanics lien", "materialman's lien", "statutory lien",
            "mortgage", "deed of trust", "production payment lien",
        },
        "context": ["search for encumbrances, security interests, and liens against assets"],
    },

    # ── LITIGATION ───────────────────────────────────────────────────────
    "pending_litigation": {
        "domain": SemanticDomain.LITIGATION,
        "aliases": {
            "pending litigation", "outstanding litigation",
            "active lawsuits", "pending claims", "threatened litigation",
            "demand letters", "regulatory enforcement",
            "class action", "qui tam", "false claims act",
            "royalty dispute", "lease dispute", "title suit",
            "trespass to try title", "quiet title action",
        },
        "context": ["review of all pending, threatened, or anticipated legal proceedings"],
    },

    # ── PREFERENTIAL RIGHTS ──────────────────────────────────────────────
    "rofr": {
        "domain": SemanticDomain.PREFERENTIAL_RIGHTS,
        "aliases": {
            "right of first refusal", "rofr", "preferential purchase right",
            "ppr", "preferential right", "preemptive right",
            "first right of purchase", "right of first offer",
            "rofo", "tag-along right", "co-sale right",
        },
        "context": ["right to match a third-party offer before transfer to third party"],
    },

    # ── CONSENT TO ASSIGN ────────────────────────────────────────────────
    "consent_requirement": {
        "domain": SemanticDomain.CONSENT,
        "aliases": {
            "consent to assign", "assignment consent",
            "lessor consent", "landlord consent",
            "consent requirement", "transfer restriction",
            "anti-assignment clause", "assignment clause",
            "approval requirement", "operator approval",
        },
        "context": ["requirement to obtain lessor or counterparty consent before assignment"],
    },

    # ── CHANGE OF CONTROL ────────────────────────────────────────────────
    "change_of_control": {
        "domain": SemanticDomain.CHANGE_OF_CONTROL,
        "aliases": {
            "change of control", "coc", "change in control",
            "deemed assignment", "indirect assignment",
            "stock transfer", "membership interest transfer",
            "entity-level transaction", "upstream transfer",
            "beneficial ownership change",
        },
        "context": ["provisions triggered by changes in ownership or control of an entity"],
    },

    # ── AMI AGREEMENTS ───────────────────────────────────────────────────
    "ami_agreement": {
        "domain": SemanticDomain.AMI,
        "aliases": {
            "area of mutual interest", "ami", "ami agreement",
            "ami provision", "mutual interest area",
            "acquisition notification", "ami boundary",
            "ami obligation", "after-acquired interest",
            "ami election period",
        },
        "context": ["agreement requiring parties to offer jointly acquired interests within defined area"],
    },

    # ── PSA ───────────────────────────────────────────────────────────────
    "purchase_sale_agreement": {
        "domain": SemanticDomain.PSA,
        "aliases": {
            "purchase and sale agreement", "psa", "asset purchase agreement",
            "apa", "acquisition agreement", "buy-sell agreement",
            "stock purchase agreement", "spa", "membership interest purchase",
            "mipa", "contribution agreement",
        },
        "context": ["definitive agreement for acquisition or divestiture of oil and gas assets"],
    },
    "effective_date": {
        "domain": SemanticDomain.PSA,
        "aliases": {
            "effective date", "economic effective date",
            "effective time", "valuation date",
            "as-of date", "adjustment date",
        },
        "context": ["date from which economic benefits and burdens transfer to buyer"],
    },
    "closing_adjustments": {
        "domain": SemanticDomain.PSA,
        "aliases": {
            "closing adjustments", "purchase price adjustments",
            "preliminary settlement statement", "pss",
            "final settlement statement", "fss",
            "post-closing adjustments", "true-up",
            "proration of revenues", "proration of expenses",
        },
        "context": ["adjustments to purchase price for revenues and costs between effective and closing dates"],
    },

    # ── REPS & WARRANTIES ────────────────────────────────────────────────
    "representations_warranties": {
        "domain": SemanticDomain.REPS_WARRANTIES,
        "aliases": {
            "representations and warranties", "reps and warranties",
            "reps", "warranties", "seller representations",
            "buyer representations", "fundamental representations",
            "special representations", "environmental reps",
            "title reps", "material adverse effect", "mae",
        },
        "context": ["contractual statements of fact and promises regarding asset condition"],
    },

    # ── INDEMNIFICATION ──────────────────────────────────────────────────
    "indemnification": {
        "domain": SemanticDomain.INDEMNIFICATION,
        "aliases": {
            "indemnification", "indemnity", "hold harmless",
            "defense and indemnity", "special indemnity",
            "consequential damages waiver", "cap on liability",
            "basket", "deductible", "indemnity cap",
            "survival period", "indemnification claim",
            "escrow holdback", "indemnity escrow",
        },
        "context": ["contractual allocation of risk and liability between parties"],
    },

    # ── SUSPENSE ─────────────────────────────────────────────────────────
    "suspense_account": {
        "domain": SemanticDomain.SUSPENSE,
        "aliases": {
            "suspense", "suspense account", "suspended funds",
            "suspended revenue", "held in suspense",
            "unclaimed royalties", "undistributed revenue",
            "division order suspense", "title suspense",
            "address unknown suspense",
        },
        "context": ["revenue held pending resolution of title or payment issues"],
    },

    # ── OPERATOR QUALIFICATION ───────────────────────────────────────────
    "operator_qualification": {
        "domain": SemanticDomain.OPERATOR,
        "aliases": {
            "operator qualification", "operator review",
            "operator history", "operating agreement",
            "joint operating agreement", "joa", "aapl form 610",
            "copas", "accounting procedure", "afe process",
            "authorization for expenditure", "operator removal",
            "operator designation", "successor operator",
        },
        "context": ["review of operator competency, compliance history, and operating agreement terms"],
    },
}


class DueDiligenceSemanticNormalizer:
    """Deterministic semantic normalizer for oil & gas due diligence terms."""

    def __init__(self) -> None:
        self._lookup: Dict[str, Tuple[str, SemanticDomain, List[str]]] = {}
        self._build_lookup()
        logger.info(
            "DueDiligenceSemanticNormalizer initialized | terms={} | aliases={}",
            len(TERM_REGISTRY),
            len(self._lookup),
        )

    def _build_lookup(self) -> None:
        """Build reverse-lookup from every alias to canonical term."""
        for canonical, info in TERM_REGISTRY.items():
            domain = info["domain"]
            context = info.get("context", [])
            for alias in info["aliases"]:
                normalized_alias = self._normalize_key(alias)
                self._lookup[normalized_alias] = (canonical, domain, context)

    @staticmethod
    def _normalize_key(text: str) -> str:
        """Normalize text for lookup: lowercase, strip, collapse whitespace, remove punctuation."""
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def normalize(self, term: str) -> NormalizationResult:
        """Normalize a term to its canonical representation."""
        key = self._normalize_key(term)
        if key in self._lookup:
            canonical, domain, context = self._lookup[key]
            aliases = [a for a in TERM_REGISTRY[canonical]["aliases"] if self._normalize_key(a) != key]
            return NormalizationResult(
                original=term,
                canonical=canonical,
                domain=domain,
                confidence=1.0,
                aliases_matched=[key],
                context_hints=context,
            )

        # Fuzzy substring match
        best_match: Optional[Tuple[str, SemanticDomain, List[str], str]] = None
        best_score = 0.0
        for alias_key, (canonical, domain, context) in self._lookup.items():
            if alias_key in key or key in alias_key:
                overlap = len(set(key.split()) & set(alias_key.split()))
                total = max(len(key.split()), len(alias_key.split()))
                score = overlap / total if total > 0 else 0.0
                if score > best_score:
                    best_score = score
                    best_match = (canonical, domain, context, alias_key)

        if best_match and best_score >= 0.4:
            canonical, domain, context, matched_alias = best_match
            return NormalizationResult(
                original=term,
                canonical=canonical,
                domain=domain,
                confidence=round(best_score, 3),
                aliases_matched=[matched_alias],
                context_hints=context,
            )

        return NormalizationResult(
            original=term,
            canonical=term.lower().replace(" ", "_"),
            domain=SemanticDomain.TITLE,
            confidence=0.0,
            aliases_matched=[],
            context_hints=["No canonical match found — raw term used"],
        )

    def normalize_batch(self, terms: List[str]) -> List[NormalizationResult]:
        """Normalize a batch of terms."""
        return [self.normalize(t) for t in terms]

    def get_all_aliases(self, canonical: str) -> Set[str]:
        """Return all known aliases for a canonical term."""
        if canonical in TERM_REGISTRY:
            return TERM_REGISTRY[canonical]["aliases"]
        return set()

    def get_domain_terms(self, domain: SemanticDomain) -> List[str]:
        """Return all canonical terms in a domain."""
        return [k for k, v in TERM_REGISTRY.items() if v["domain"] == domain]

    def search_terms(self, query: str) -> List[NormalizationResult]:
        """Search for terms matching a query across all domains."""
        results: List[NormalizationResult] = []
        query_lower = query.lower()
        for canonical, info in TERM_REGISTRY.items():
            if query_lower in canonical:
                results.append(NormalizationResult(
                    original=query,
                    canonical=canonical,
                    domain=info["domain"],
                    confidence=0.9,
                    aliases_matched=[],
                    context_hints=info.get("context", []),
                ))
                continue
            for alias in info["aliases"]:
                if query_lower in alias.lower():
                    results.append(NormalizationResult(
                        original=query,
                        canonical=canonical,
                        domain=info["domain"],
                        confidence=0.8,
                        aliases_matched=[alias],
                        context_hints=info.get("context", []),
                    ))
                    break
        return sorted(results, key=lambda r: r.confidence, reverse=True)

    def get_registry_stats(self) -> Dict:
        """Return statistics about the term registry."""
        domain_counts: Dict[str, int] = {}
        total_aliases = 0
        for info in TERM_REGISTRY.values():
            domain = info["domain"].value
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            total_aliases += len(info["aliases"])
        return {
            "total_canonical_terms": len(TERM_REGISTRY),
            "total_aliases": total_aliases,
            "total_lookup_entries": len(self._lookup),
            "domains": domain_counts,
        }
