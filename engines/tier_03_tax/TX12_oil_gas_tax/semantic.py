"""
TX12 Oil & Gas Tax Engine — Semantic Normalization Layer
Deterministic term normalization for oil and gas taxation concepts.

GOVERNANCE NOTICE:
    Semantic normalization is a preprocessing layer.
    It must remain deterministic.
    Do not attach probabilistic models to this stage.
    No vector inference. No embeddings. No auto-learning.

Author: ECHO OMEGA PRIME
Engine: TX12 Oil & Gas Tax
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ==============================================================================
# NORMALIZATION RESULT
# ==============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on input text."""
    original_text: str
    normalized_text: str
    terms_normalized: List[Dict[str, str]]  # [{original, normalized, category}]
    domain_signals: List[str]  # Detected domain indicators
    ambiguities: List[Dict[str, Any]]  # Terms with multiple possible meanings
    confidence: float  # 0-1 confidence in normalization quality
    oil_gas_relevance: float  # 0-1 score of how O&G-specific the query is

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for response inclusion."""
        return {
            "original": self.original_text[:200],
            "normalized": self.normalized_text[:200],
            "terms_normalized": self.terms_normalized,
            "domain_signals": self.domain_signals,
            "ambiguities": self.ambiguities,
            "confidence": round(self.confidence, 3),
            "oil_gas_relevance": round(self.oil_gas_relevance, 3)
        }


# ==============================================================================
# CANONICAL TERM MAPPINGS — Oil & Gas Taxation
# ==============================================================================

# Interest type normalization
INTEREST_TYPE_MAP: Dict[str, str] = {
    "working interest": "working_interest",
    "wi": "working_interest",
    "w.i.": "working_interest",
    "operating interest": "working_interest",
    "leasehold interest": "working_interest",
    "royalty interest": "royalty_interest",
    "ri": "royalty_interest",
    "r.i.": "royalty_interest",
    "landowner royalty": "royalty_interest",
    "lessor royalty": "royalty_interest",
    "overriding royalty": "overriding_royalty_interest",
    "overriding royalty interest": "overriding_royalty_interest",
    "orri": "overriding_royalty_interest",
    "override": "overriding_royalty_interest",
    "o.r.r.i.": "overriding_royalty_interest",
    "carried interest": "carried_interest",
    "carry": "carried_interest",
    "carried working interest": "carried_interest",
    "reversionary interest": "reversionary_interest",
    "back-in": "reversionary_interest",
    "backin": "reversionary_interest",
    "back in interest": "reversionary_interest",
    "net profits interest": "net_profits_interest",
    "npi": "net_profits_interest",
    "n.p.i.": "net_profits_interest",
    "net revenue interest": "net_revenue_interest",
    "nri": "net_revenue_interest",
    "n.r.i.": "net_revenue_interest",
    "mineral interest": "mineral_interest",
    "mineral rights": "mineral_interest",
    "fee mineral": "mineral_interest",
    "fee mineral interest": "mineral_interest",
    "surface interest": "surface_interest",
    "surface rights": "surface_interest",
    "executive rights": "executive_rights",
    "bonus interest": "executive_rights",
    "undivided mineral interest": "undivided_mineral_interest",
    "umi": "undivided_mineral_interest",
}

# Depletion terminology
DEPLETION_MAP: Dict[str, str] = {
    "percentage depletion": "percentage_depletion",
    "statutory depletion": "percentage_depletion",
    "15% depletion": "percentage_depletion",
    "depletion allowance": "percentage_depletion",
    "section 613": "percentage_depletion",
    "613a": "percentage_depletion_small_producer",
    "section 613a": "percentage_depletion_small_producer",
    "small producer exemption": "percentage_depletion_small_producer",
    "independent producer depletion": "percentage_depletion_small_producer",
    "1000 barrel limit": "percentage_depletion_small_producer",
    "cost depletion": "cost_depletion",
    "basis depletion": "cost_depletion",
    "section 611": "cost_depletion",
    "depletable basis": "cost_depletion",
    "depletion base": "cost_depletion",
    "gross income from property": "gross_income_from_property",
    "gross income limitation": "gross_income_limitation_depletion",
    "65% limitation": "taxable_income_limitation_depletion",
    "65% taxable income": "taxable_income_limitation_depletion",
    "taxable income limitation": "taxable_income_limitation_depletion",
}

# Drilling cost terminology
DRILLING_COST_MAP: Dict[str, str] = {
    "intangible drilling cost": "idc",
    "intangible drilling costs": "idc",
    "idc": "idc",
    "i.d.c.": "idc",
    "idcs": "idc",
    "intangible drilling and development costs": "idc",
    "tangible drilling cost": "tangible_drilling_cost",
    "tangible equipment": "tangible_drilling_cost",
    "lease and well equipment": "tangible_drilling_cost",
    "downhole equipment": "tangible_drilling_cost",
    "casing": "tangible_drilling_cost",
    "tubing": "tangible_drilling_cost",
    "christmas tree": "tangible_drilling_cost",
    "wellhead": "tangible_drilling_cost",
    "geological costs": "geological_geophysical_costs",
    "geophysical costs": "geological_geophysical_costs",
    "g&g costs": "geological_geophysical_costs",
    "g and g": "geological_geophysical_costs",
    "seismic costs": "geological_geophysical_costs",
    "section 167h": "geological_geophysical_costs",
    "167(h)": "geological_geophysical_costs",
    "dry hole cost": "dry_hole_costs",
    "dry hole": "dry_hole_costs",
    "nonproductive well": "dry_hole_costs",
    "plugging cost": "abandonment_plugging_costs",
    "plugging and abandonment": "abandonment_plugging_costs",
    "p&a": "abandonment_plugging_costs",
    "aro": "asset_retirement_obligation",
    "asset retirement obligation": "asset_retirement_obligation",
    "abandonment cost": "abandonment_plugging_costs",
    "workover": "workover_costs",
    "workover costs": "workover_costs",
    "recompletion": "workover_costs",
    "reworking": "workover_costs",
}

# Agreement type normalization
AGREEMENT_MAP: Dict[str, str] = {
    "farmout": "farmout_agreement",
    "farm-out": "farmout_agreement",
    "farm out": "farmout_agreement",
    "farmout agreement": "farmout_agreement",
    "farmin": "farmout_agreement",
    "farm-in": "farmout_agreement",
    "farm in": "farmout_agreement",
    "farmee": "farmout_agreement",
    "farmor": "farmout_agreement",
    "joint operating agreement": "joa",
    "joa": "joa",
    "j.o.a.": "joa",
    "operating agreement": "joa",
    "joint venture": "joint_venture",
    "jv": "joint_venture",
    "participation agreement": "participation_agreement",
    "area of mutual interest": "ami_agreement",
    "ami": "ami_agreement",
    "production sharing agreement": "production_sharing_agreement",
    "psa": "production_sharing_agreement",
    "unitization agreement": "unitization_agreement",
    "unit agreement": "unitization_agreement",
    "pooling agreement": "pooling_agreement",
    "communitization agreement": "communitization_agreement",
}

# Payment type normalization
PAYMENT_MAP: Dict[str, str] = {
    "production payment": "production_payment",
    "carved-out production payment": "carved_out_production_payment",
    "carved out production payment": "carved_out_production_payment",
    "retained production payment": "retained_production_payment",
    "section 636": "production_payment_636",
    "636": "production_payment_636",
    "lease bonus": "lease_bonus",
    "bonus payment": "lease_bonus",
    "signing bonus": "lease_bonus",
    "delay rental": "delay_rental",
    "delay rentals": "delay_rental",
    "shut-in royalty": "shut_in_royalty",
    "shut in payment": "shut_in_royalty",
    "minimum royalty": "minimum_royalty",
    "advance royalty": "advance_royalty",
}

# Severance / production tax
SEVERANCE_MAP: Dict[str, str] = {
    "severance tax": "severance_tax",
    "production tax": "severance_tax",
    "gross production tax": "severance_tax",
    "extraction tax": "severance_tax",
    "texas severance tax": "texas_severance_tax",
    "texas production tax": "texas_severance_tax",
    "texas oil tax": "texas_severance_tax",
    "4.6%": "texas_oil_severance_rate",
    "7.5%": "texas_gas_severance_rate",
    "new mexico severance tax": "new_mexico_severance_tax",
    "oklahoma gross production tax": "oklahoma_gross_production_tax",
    "north dakota extraction tax": "north_dakota_extraction_tax",
    "wyoming severance tax": "wyoming_severance_tax",
    "louisiana severance tax": "louisiana_severance_tax",
    "colorado severance tax": "colorado_severance_tax",
    "ohio severance tax": "ohio_severance_tax",
    "west virginia severance tax": "west_virginia_severance_tax",
    "pennsylvania impact fee": "pennsylvania_impact_fee",
}

# Credit terminology
CREDIT_MAP: Dict[str, str] = {
    "enhanced oil recovery credit": "eor_credit_43",
    "eor credit": "eor_credit_43",
    "section 43": "eor_credit_43",
    "43 credit": "eor_credit_43",
    "tertiary recovery": "eor_credit_43",
    "marginal well credit": "marginal_well_credit_45i",
    "marginal well": "marginal_well_credit_45i",
    "section 45i": "marginal_well_credit_45i",
    "45i": "marginal_well_credit_45i",
    "stripper well": "marginal_well_credit_45i",
}

# Entity / structure terms
ENTITY_MAP: Dict[str, str] = {
    "operator": "well_operator",
    "working interest owner": "working_interest_owner",
    "non-operator": "non_operating_working_interest",
    "non-op": "non_operating_working_interest",
    "nonoperator": "non_operating_working_interest",
    "independent producer": "independent_producer",
    "independent": "independent_producer",
    "integrated oil company": "integrated_oil_company",
    "major oil company": "integrated_oil_company",
    "major": "integrated_oil_company",
    "refiner": "integrated_oil_company",
    "small producer": "independent_producer",
    "royalty owner": "royalty_owner",
    "mineral owner": "mineral_owner",
    "lessor": "lessor",
    "lessee": "lessee",
    "landman": "landman",
}

# IRC Section normalization
IRC_MAP: Dict[str, str] = {
    "section 611": "irc_611_cost_depletion",
    "section 613": "irc_613_percentage_depletion",
    "section 613a": "irc_613a_small_producer",
    "section 263c": "irc_263c_idc",
    "section 263(c)": "irc_263c_idc",
    "section 636": "irc_636_production_payments",
    "section 636(a)": "irc_636a_carved_out",
    "section 636(b)": "irc_636b_retained",
    "section 43": "irc_43_eor_credit",
    "section 45i": "irc_45i_marginal_well",
    "section 167h": "irc_167h_g_and_g",
    "section 167(h)": "irc_167h_g_and_g",
    "section 1254": "irc_1254_recapture",
    "section 1254 recapture": "irc_1254_recapture",
    "1254 recapture": "irc_1254_recapture",
    "idc recapture": "irc_1254_recapture",
    "section 469": "irc_469_passive_activity",
    "section 465": "irc_465_at_risk",
    "at-risk rules": "irc_465_at_risk",
    "at risk": "irc_465_at_risk",
    "section 199a": "irc_199a_qbi",
    "199a": "irc_199a_qbi",
    "qbi": "irc_199a_qbi",
    "qualified business income": "irc_199a_qbi",
    "section 59(e)": "irc_59e_idc_election",
    "59e election": "irc_59e_idc_election",
    "alternative minimum tax": "irc_55_amt",
    "amt": "irc_55_amt",
    "amt preference": "irc_57_preferences",
    "section 57": "irc_57_preferences",
}

# Basin / geography normalization
BASIN_MAP: Dict[str, str] = {
    "permian basin": "permian_basin",
    "permian": "permian_basin",
    "midland basin": "permian_basin_midland",
    "delaware basin": "permian_basin_delaware",
    "central basin platform": "permian_basin_central_platform",
    "eagle ford": "eagle_ford_shale",
    "eagle ford shale": "eagle_ford_shale",
    "bakken": "bakken_formation",
    "bakken shale": "bakken_formation",
    "marcellus": "marcellus_shale",
    "marcellus shale": "marcellus_shale",
    "haynesville": "haynesville_shale",
    "barnett shale": "barnett_shale",
    "woodford shale": "woodford_shale",
    "spraberry": "spraberry_trend",
    "wolfcamp": "wolfcamp_formation",
    "bone spring": "bone_spring_formation",
    "scoop": "scoop_play",
    "stack": "stack_play",
    "dj basin": "dj_basin",
    "denver julesburg": "dj_basin",
    "powder river": "powder_river_basin",
    "uinta basin": "uinta_basin",
    "williston basin": "williston_basin",
    "anadarko basin": "anadarko_basin",
}

# All maps combined for iteration
ALL_MAPS: List[Tuple[str, Dict[str, str]]] = [
    ("interest_type", INTEREST_TYPE_MAP),
    ("depletion", DEPLETION_MAP),
    ("drilling_cost", DRILLING_COST_MAP),
    ("agreement", AGREEMENT_MAP),
    ("payment", PAYMENT_MAP),
    ("severance", SEVERANCE_MAP),
    ("credit", CREDIT_MAP),
    ("entity", ENTITY_MAP),
    ("irc_section", IRC_MAP),
    ("basin", BASIN_MAP),
]


# ==============================================================================
# DOMAIN SIGNAL DETECTION
# ==============================================================================

OIL_GAS_SIGNALS: Set[str] = {
    "oil", "gas", "petroleum", "well", "drilling", "depletion",
    "working interest", "royalty", "overriding", "operator", "lease",
    "mineral", "reservoir", "production", "barrel", "boe",
    "mcf", "bbl", "severance", "farmout", "joa", "idc",
    "casing", "tubing", "wellhead", "spud", "completion",
    "fracking", "hydraulic fracturing", "horizontal", "vertical",
    "directional", "pad", "acreage", "field", "basin",
    "permian", "midland", "crude", "natural gas", "condensate",
    "ngl", "gathering", "pipeline", "midstream", "upstream",
    "downstream", "refining", "landman", "land man",
    "unitization", "pooling", "communitization", "plugging",
    "abandonment", "stripper", "marginal", "enhanced recovery",
    "waterflood", "co2 flood", "secondary recovery", "tertiary recovery",
    "overriding royalty", "net profits interest", "carried interest",
    "production payment", "delay rental", "shut-in", "bonus",
    "payout", "reversion", "back-in", "washout",
}


def detect_domain_signals(text: str) -> List[str]:
    """Detect oil and gas domain signals in query text.

    Returns list of detected signal terms.
    """
    text_lower = text.lower()
    detected: List[str] = []
    for signal in OIL_GAS_SIGNALS:
        if signal in text_lower:
            detected.append(signal)
    return detected


def calculate_oil_gas_relevance(signals: List[str], text_length: int) -> float:
    """Calculate 0-1 relevance score based on domain signal density.

    A query with 3+ O&G signals is strongly relevant (>0.8).
    A query with 1-2 signals may be tangentially related (0.3-0.7).
    Zero signals is likely a general tax query routed incorrectly (0.0-0.1).
    """
    if not signals:
        return 0.05
    signal_count = len(signals)
    word_count = max(len(text_length) if isinstance(text_length, str) else text_length // 5, 1)

    if signal_count >= 5:
        return min(0.99, 0.8 + (signal_count - 5) * 0.02)
    elif signal_count >= 3:
        return 0.7 + (signal_count - 3) * 0.05
    elif signal_count >= 2:
        return 0.5 + 0.1
    else:
        return 0.3


# ==============================================================================
# AMBIGUITY DETECTION
# ==============================================================================

AMBIGUOUS_TERMS: Dict[str, List[Dict[str, str]]] = {
    "interest": [
        {"meaning": "ownership_interest", "context": "oil & gas ownership stake"},
        {"meaning": "loan_interest", "context": "financing / debt interest expense"},
        {"meaning": "at_risk_interest", "context": "at-risk amount under IRC 465"}
    ],
    "deduction": [
        {"meaning": "idc_deduction", "context": "intangible drilling cost deduction"},
        {"meaning": "depletion_deduction", "context": "depletion allowance"},
        {"meaning": "operating_deduction", "context": "lease operating expense"},
        {"meaning": "depreciation_deduction", "context": "tangible equipment MACRS"}
    ],
    "basis": [
        {"meaning": "depletable_basis", "context": "cost depletion basis in mineral property"},
        {"meaning": "partnership_basis", "context": "partner's outside basis"},
        {"meaning": "adjusted_basis", "context": "asset basis for gain/loss computation"},
        {"meaning": "at_risk_basis", "context": "at-risk amount under IRC 465"}
    ],
    "production": [
        {"meaning": "oil_gas_production", "context": "physical extraction of hydrocarbons"},
        {"meaning": "production_payment", "context": "IRC 636 production payment"},
        {"meaning": "production_tax", "context": "state severance/production tax"}
    ],
    "carry": [
        {"meaning": "carried_interest", "context": "carried working interest in well"},
        {"meaning": "net_operating_loss_carry", "context": "NOL carryforward/carryback"},
        {"meaning": "credit_carry", "context": "tax credit carryforward"}
    ],
    "lease": [
        {"meaning": "oil_gas_lease", "context": "mineral lease granting exploration rights"},
        {"meaning": "equipment_lease", "context": "equipment operating/finance lease"},
        {"meaning": "office_lease", "context": "real property office lease"}
    ],
    "operator": [
        {"meaning": "well_operator", "context": "designated operator under JOA"},
        {"meaning": "business_operator", "context": "general business operations sense"}
    ],
    "unit": [
        {"meaning": "production_unit", "context": "unitized pool of mineral interests"},
        {"meaning": "partnership_unit", "context": "limited partnership interest unit"}
    ],
    "pool": [
        {"meaning": "pooling_oil_gas", "context": "mineral interest pooling/communitization"},
        {"meaning": "pool_of_capital", "context": "pool of capital doctrine for farmouts"}
    ],
}


def detect_ambiguities(text: str) -> List[Dict[str, Any]]:
    """Detect potentially ambiguous terms in query text.

    Returns list of ambiguity entries with possible meanings.
    """
    text_lower = text.lower()
    ambiguities: List[Dict[str, Any]] = []
    for term, meanings in AMBIGUOUS_TERMS.items():
        if term in text_lower:
            ambiguities.append({
                "term": term,
                "possible_meanings": meanings,
                "recommended": meanings[0]["meaning"]  # Default to O&G meaning
            })
    return ambiguities


# ==============================================================================
# MAIN NORMALIZATION FUNCTION
# ==============================================================================

def normalize_semantics(text: str) -> NormalizationResult:
    """Normalize oil and gas tax terminology in input text.

    This function is DETERMINISTIC. Same input always produces same output.
    No probabilistic models. No embeddings. No ML inference.

    Args:
        text: Raw query text from user.

    Returns:
        NormalizationResult with normalized text and metadata.
    """
    text_lower = text.lower()
    normalized = text_lower
    terms_normalized: List[Dict[str, str]] = []

    # Apply all normalization maps
    for category, term_map in ALL_MAPS:
        # Sort by length descending to match longest phrases first
        sorted_terms = sorted(term_map.keys(), key=len, reverse=True)
        for original_term in sorted_terms:
            if original_term in normalized:
                canonical = term_map[original_term]
                # Only record if not already the canonical form
                if original_term != canonical:
                    terms_normalized.append({
                        "original": original_term,
                        "normalized": canonical,
                        "category": category
                    })
                    normalized = normalized.replace(original_term, canonical)

    # Detect domain signals
    domain_signals = detect_domain_signals(text)

    # Detect ambiguities
    ambiguities = detect_ambiguities(text)

    # Calculate relevance
    oil_gas_relevance = calculate_oil_gas_relevance(domain_signals, len(text))

    # Calculate normalization confidence
    if terms_normalized:
        confidence = min(0.99, 0.7 + len(terms_normalized) * 0.03)
    elif domain_signals:
        confidence = 0.6
    else:
        confidence = 0.3

    result = NormalizationResult(
        original_text=text,
        normalized_text=normalized,
        terms_normalized=terms_normalized,
        domain_signals=domain_signals,
        ambiguities=ambiguities,
        confidence=confidence,
        oil_gas_relevance=oil_gas_relevance
    )

    logger.debug(
        f"Semantic normalization: {len(terms_normalized)} terms normalized, "
        f"{len(domain_signals)} domain signals, relevance={oil_gas_relevance:.2f}"
    )

    return result
