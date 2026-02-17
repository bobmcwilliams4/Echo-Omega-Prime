"""
LM02 Lease Analysis Engine - Semantic Dictionary
Oil and Gas Lease Terminology, Normalization, and Parsing

Comprehensive semantic mapping for lease analysis including:
    - Lessor/lessee nomenclature normalization
    - Interest type classification and parsing
    - Royalty fraction parsing (fraction and decimal)
    - Legal description parsing (Texas PLSS + abstract/survey)
    - Formation and depth terminology
    - Lease clause type identification
    - Permian Basin operator and field name normalization
    - Division order terminology

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

# ============================================================================
# SEMANTIC MAP VERSION
# ============================================================================

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_BUILD_DATE = "2026-02-10"

# ============================================================================
# ENUMERATIONS
# ============================================================================


class InterestType(str, Enum):
    """Types of oil and gas property interests."""
    MINERAL_INTEREST = "mineral_interest"
    ROYALTY_INTEREST = "royalty_interest"
    OVERRIDING_ROYALTY = "overriding_royalty"
    WORKING_INTEREST = "working_interest"
    NET_REVENUE_INTEREST = "net_revenue_interest"
    PRODUCTION_PAYMENT = "production_payment"
    NET_PROFITS_INTEREST = "net_profits_interest"
    CARRIED_INTEREST = "carried_interest"
    EXECUTIVE_RIGHT = "executive_right"
    BONUS_INTEREST = "bonus_interest"
    DELAY_RENTAL_INTEREST = "delay_rental_interest"
    SURFACE_INTEREST = "surface_interest"
    LEASEHOLD_INTEREST = "leasehold_interest"


class LeaseClauseType(str, Enum):
    """Classification of lease clause types."""
    HABENDUM = "habendum"
    GRANTING = "granting"
    DRILLING = "drilling"
    DELAY_RENTAL = "delay_rental"
    ROYALTY = "royalty"
    SHUT_IN = "shut_in"
    POOLING = "pooling"
    UNITIZATION = "unitization"
    PUGH = "pugh"
    FORCE_MAJEURE = "force_majeure"
    CONTINUOUS_DEVELOPMENT = "continuous_development"
    SURFACE_USE = "surface_use"
    DEPTH_LIMITATION = "depth_limitation"
    RETAINED_ACREAGE = "retained_acreage"
    TOP_LEASE = "top_lease"
    PREFERENTIAL_RIGHT = "preferential_right"
    ASSIGNMENT = "assignment"
    MOTHER_HUBBARD = "mother_hubbard"
    SURRENDER = "surrender"
    CESSATION = "cessation"
    COMMENCEMENT = "commencement"
    WARRANTY = "warranty"
    INDEMNITY = "indemnity"
    NOTICE = "notice"
    GOVERNING_LAW = "governing_law"
    ARBITRATION = "arbitration"


class PartyRole(str, Enum):
    """Roles in a lease transaction."""
    LESSOR = "lessor"
    LESSEE = "lessee"
    ASSIGNOR = "assignor"
    ASSIGNEE = "assignee"
    OPERATOR = "operator"
    NON_OPERATOR = "non_operator"
    ROYALTY_OWNER = "royalty_owner"
    OVERRIDING_ROYALTY_OWNER = "orri_owner"
    SURFACE_OWNER = "surface_owner"
    MINERAL_OWNER = "mineral_owner"


class FormationType(str, Enum):
    """Permian Basin geological formations."""
    SPRABERRY = "spraberry"
    WOLFCAMP = "wolfcamp"
    BONE_SPRING = "bone_spring"
    DELAWARE = "delaware"
    AVALON = "avalon"
    BRUSHY_CANYON = "brushy_canyon"
    CLINE = "cline"
    STRAWN = "strawn"
    ATOKA = "atoka"
    ELLENBURGER = "ellenburger"
    SAN_ANDRES = "san_andres"
    CLEAR_FORK = "clear_fork"
    GLORIETA = "glorieta"
    YESO = "yeso"
    QUEEN = "queen"
    GRAYBURG = "grayburg"
    DEVONIAN = "devonian"
    WOODFORD = "woodford"
    BARNETT = "barnett"
    MISSISSIPPIAN = "mississippian"


# ============================================================================
# DATA MODELS
# ============================================================================


@dataclass
class ParsedFraction:
    """Result of parsing a royalty or interest fraction."""
    original_text: str
    numerator: int
    denominator: int
    decimal_value: float
    fraction_str: str
    is_valid: bool
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "numerator": self.numerator,
            "denominator": self.denominator,
            "decimal_value": self.decimal_value,
            "fraction_str": self.fraction_str,
            "is_valid": self.is_valid,
            "error_message": self.error_message,
        }


@dataclass
class LegalDescription:
    """Parsed Texas legal description."""
    original_text: str
    survey_name: Optional[str] = None
    abstract_number: Optional[str] = None
    block: Optional[str] = None
    section: Optional[str] = None
    township: Optional[str] = None
    range_value: Optional[str] = None
    lot: Optional[str] = None
    subdivision: Optional[str] = None
    county: Optional[str] = None
    state: str = "Texas"
    acres: Optional[float] = None
    metes_and_bounds: bool = False
    partial_interest_description: Optional[str] = None
    confidence: float = 0.0
    parse_errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "survey_name": self.survey_name,
            "abstract_number": self.abstract_number,
            "block": self.block,
            "section": self.section,
            "township": self.township,
            "range_value": self.range_value,
            "lot": self.lot,
            "subdivision": self.subdivision,
            "county": self.county,
            "state": self.state,
            "acres": self.acres,
            "metes_and_bounds": self.metes_and_bounds,
            "partial_interest_description": self.partial_interest_description,
            "confidence": self.confidence,
            "parse_errors": self.parse_errors,
        }

    @property
    def short_description(self) -> str:
        """Generate a short-form legal description."""
        parts = []
        if self.section:
            parts.append(f"Sec {self.section}")
        if self.block:
            parts.append(f"Blk {self.block}")
        if self.township:
            parts.append(f"T{self.township}")
        if self.range_value:
            parts.append(f"R{self.range_value}")
        if self.survey_name:
            parts.append(f"{self.survey_name} Survey")
        if self.abstract_number:
            parts.append(f"A-{self.abstract_number}")
        if self.county:
            parts.append(f"{self.county} County")
        return ", ".join(parts) if parts else self.original_text[:80]


@dataclass
class NormalizationResult:
    """Result of normalizing a lease term or entity name."""
    original: str
    normalized: str
    category: str
    confidence: float
    aliases: List[str] = field(default_factory=list)
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "normalized": self.normalized,
            "category": self.category,
            "confidence": self.confidence,
            "aliases": self.aliases,
            "notes": self.notes,
        }


@dataclass
class DepthInterval:
    """A depth interval within a lease or well."""
    top_depth_ft: Optional[float] = None
    bottom_depth_ft: Optional[float] = None
    formation_name: Optional[str] = None
    formation_type: Optional[FormationType] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "top_depth_ft": self.top_depth_ft,
            "bottom_depth_ft": self.bottom_depth_ft,
            "formation_name": self.formation_name,
            "formation_type": self.formation_type.value if self.formation_type else None,
            "description": self.description,
        }

    @property
    def thickness_ft(self) -> Optional[float]:
        if self.top_depth_ft is not None and self.bottom_depth_ft is not None:
            return self.bottom_depth_ft - self.top_depth_ft
        return None


# ============================================================================
# SEMANTIC DICTIONARIES
# ============================================================================

# Party role synonyms
PARTY_ROLE_SYNONYMS: Dict[str, PartyRole] = {
    "lessor": PartyRole.LESSOR,
    "grantor": PartyRole.LESSOR,
    "landowner": PartyRole.LESSOR,
    "mineral owner": PartyRole.MINERAL_OWNER,
    "mineral interest owner": PartyRole.MINERAL_OWNER,
    "fee owner": PartyRole.MINERAL_OWNER,
    "surface owner": PartyRole.SURFACE_OWNER,
    "lessee": PartyRole.LESSEE,
    "grantee": PartyRole.LESSEE,
    "operator": PartyRole.OPERATOR,
    "designated operator": PartyRole.OPERATOR,
    "unit operator": PartyRole.OPERATOR,
    "non-operator": PartyRole.NON_OPERATOR,
    "non-operating working interest owner": PartyRole.NON_OPERATOR,
    "nowi": PartyRole.NON_OPERATOR,
    "assignor": PartyRole.ASSIGNOR,
    "assignee": PartyRole.ASSIGNEE,
    "royalty owner": PartyRole.ROYALTY_OWNER,
    "royalty interest owner": PartyRole.ROYALTY_OWNER,
    "overriding royalty owner": PartyRole.OVERRIDING_ROYALTY_OWNER,
    "orri owner": PartyRole.OVERRIDING_ROYALTY_OWNER,
}

# Interest type synonyms
INTEREST_TYPE_SYNONYMS: Dict[str, InterestType] = {
    "mineral interest": InterestType.MINERAL_INTEREST,
    "mineral estate": InterestType.MINERAL_INTEREST,
    "fee mineral": InterestType.MINERAL_INTEREST,
    "minerals in place": InterestType.MINERAL_INTEREST,
    "undivided mineral interest": InterestType.MINERAL_INTEREST,
    "royalty interest": InterestType.ROYALTY_INTEREST,
    "landowner royalty": InterestType.ROYALTY_INTEREST,
    "lessor royalty": InterestType.ROYALTY_INTEREST,
    "npri": InterestType.ROYALTY_INTEREST,
    "non-participating royalty": InterestType.ROYALTY_INTEREST,
    "non-participating royalty interest": InterestType.ROYALTY_INTEREST,
    "overriding royalty": InterestType.OVERRIDING_ROYALTY,
    "orri": InterestType.OVERRIDING_ROYALTY,
    "override": InterestType.OVERRIDING_ROYALTY,
    "overriding royalty interest": InterestType.OVERRIDING_ROYALTY,
    "working interest": InterestType.WORKING_INTEREST,
    "wi": InterestType.WORKING_INTEREST,
    "leasehold interest": InterestType.LEASEHOLD_INTEREST,
    "operating interest": InterestType.WORKING_INTEREST,
    "net revenue interest": InterestType.NET_REVENUE_INTEREST,
    "nri": InterestType.NET_REVENUE_INTEREST,
    "production payment": InterestType.PRODUCTION_PAYMENT,
    "oil payment": InterestType.PRODUCTION_PAYMENT,
    "net profits interest": InterestType.NET_PROFITS_INTEREST,
    "npi": InterestType.NET_PROFITS_INTEREST,
    "carried interest": InterestType.CARRIED_INTEREST,
    "carry": InterestType.CARRIED_INTEREST,
    "carried working interest": InterestType.CARRIED_INTEREST,
    "executive right": InterestType.EXECUTIVE_RIGHT,
    "executive rights": InterestType.EXECUTIVE_RIGHT,
    "leasing right": InterestType.EXECUTIVE_RIGHT,
    "bonus interest": InterestType.BONUS_INTEREST,
    "bonus": InterestType.BONUS_INTEREST,
    "delay rental interest": InterestType.DELAY_RENTAL_INTEREST,
    "delay rental": InterestType.DELAY_RENTAL_INTEREST,
    "rentals": InterestType.DELAY_RENTAL_INTEREST,
    "surface interest": InterestType.SURFACE_INTEREST,
    "surface estate": InterestType.SURFACE_INTEREST,
    "surface rights": InterestType.SURFACE_INTEREST,
}

# Lease clause type indicators (patterns in lease text)
CLAUSE_TYPE_INDICATORS: Dict[LeaseClauseType, List[str]] = {
    LeaseClauseType.HABENDUM: [
        "for a term of", "primary term", "years from date",
        "and as long thereafter as", "so long as produced",
    ],
    LeaseClauseType.GRANTING: [
        "do hereby grant", "lease and let", "grant, demise",
        "exclusive right", "right to explore",
    ],
    LeaseClauseType.DRILLING: [
        "commence drilling", "commence operations", "spud a well",
        "begin actual drilling", "drilling operations",
    ],
    LeaseClauseType.DELAY_RENTAL: [
        "delay rental", "annual rental", "unless lessee",
        "pay or tender", "rental payment",
    ],
    LeaseClauseType.ROYALTY: [
        "royalty", "lessor's share", "free of cost",
        "market value at the well", "amount realized",
    ],
    LeaseClauseType.SHUT_IN: [
        "shut-in", "shut in", "well capable of producing",
        "no market available", "shut-in royalty",
    ],
    LeaseClauseType.POOLING: [
        "pool", "pooling", "combine", "communitize",
        "drilling unit", "pooled unit",
    ],
    LeaseClauseType.UNITIZATION: [
        "unitize", "unitization", "unit agreement",
        "enhanced recovery", "secondary recovery",
    ],
    LeaseClauseType.PUGH: [
        "pugh", "freestone", "non-pooled acreage",
        "acreage not included", "released from this lease",
    ],
    LeaseClauseType.FORCE_MAJEURE: [
        "force majeure", "act of god", "beyond the control",
        "unable to perform", "excused from performance",
    ],
    LeaseClauseType.CONTINUOUS_DEVELOPMENT: [
        "continuous development", "continuous drilling",
        "commence a subsequent well", "within days after",
    ],
    LeaseClauseType.SURFACE_USE: [
        "surface use", "surface rights", "accommodation",
        "surface damage", "restoration", "location approval",
    ],
    LeaseClauseType.DEPTH_LIMITATION: [
        "depth", "formation", "feet below", "above or below",
        "restricted to", "deepest formation",
    ],
    LeaseClauseType.RETAINED_ACREAGE: [
        "retained acreage", "retained lands", "releasing all",
        "except the acreage", "held by production",
    ],
    LeaseClauseType.TOP_LEASE: [
        "top lease", "subject to", "upon expiration of",
        "existing lease", "bottom lease",
    ],
    LeaseClauseType.PREFERENTIAL_RIGHT: [
        "preferential right", "right of first refusal", "rofr",
        "first option", "matching right",
    ],
    LeaseClauseType.ASSIGNMENT: [
        "assign", "transfer", "convey", "sublease",
        "partial assignment", "right to assign",
    ],
    LeaseClauseType.MOTHER_HUBBARD: [
        "mother hubbard", "cover-all", "contiguous",
        "adjacent", "strips and gores",
    ],
    LeaseClauseType.SURRENDER: [
        "surrender", "release", "relinquish",
        "partial release", "partial surrender",
    ],
    LeaseClauseType.CESSATION: [
        "cessation of production", "temporary cessation",
        "production ceases", "well ceases to produce",
    ],
    LeaseClauseType.COMMENCEMENT: [
        "commence", "begin", "initiate",
        "starting operations", "on or before",
    ],
    LeaseClauseType.WARRANTY: [
        "warrant", "warrant and defend", "good title",
        "lawful owner", "right to lease",
    ],
    LeaseClauseType.INDEMNITY: [
        "indemnify", "hold harmless", "defend",
        "assume all liability", "responsible for",
    ],
    LeaseClauseType.NOTICE: [
        "notice", "notify", "written notice",
        "address for notice", "certified mail",
    ],
    LeaseClauseType.GOVERNING_LAW: [
        "governed by the laws", "governing law",
        "jurisdiction", "venue", "state of texas",
    ],
    LeaseClauseType.ARBITRATION: [
        "arbitration", "mediation", "dispute resolution",
        "binding arbitration", "alternative dispute",
    ],
}

# Common royalty fractions with their decimal equivalents
COMMON_ROYALTY_FRACTIONS: Dict[str, float] = {
    "1/8": 0.125,
    "3/16": 0.1875,
    "1/5": 0.20,
    "3/14": 0.214286,
    "15/64": 0.234375,
    "1/4": 0.25,
    "5/16": 0.3125,
    "1/3": 0.333333,
    "3/8": 0.375,
    "1/2": 0.50,
    "5/8": 0.625,
    "3/4": 0.75,
    "7/8": 0.875,
}

# Formation name normalization
FORMATION_ALIASES: Dict[str, FormationType] = {
    "spraberry": FormationType.SPRABERRY,
    "spray berry": FormationType.SPRABERRY,
    "sprayberry": FormationType.SPRABERRY,
    "dean": FormationType.SPRABERRY,
    "lower spraberry": FormationType.SPRABERRY,
    "upper spraberry": FormationType.SPRABERRY,
    "jo mill": FormationType.SPRABERRY,
    "wolfcamp": FormationType.WOLFCAMP,
    "wolf camp": FormationType.WOLFCAMP,
    "wolfcamp a": FormationType.WOLFCAMP,
    "wolfcamp b": FormationType.WOLFCAMP,
    "wolfcamp c": FormationType.WOLFCAMP,
    "wolfcamp d": FormationType.WOLFCAMP,
    "lower wolfcamp": FormationType.WOLFCAMP,
    "upper wolfcamp": FormationType.WOLFCAMP,
    "bone spring": FormationType.BONE_SPRING,
    "bone springs": FormationType.BONE_SPRING,
    "bonespring": FormationType.BONE_SPRING,
    "1st bone spring": FormationType.BONE_SPRING,
    "2nd bone spring": FormationType.BONE_SPRING,
    "3rd bone spring": FormationType.BONE_SPRING,
    "delaware": FormationType.DELAWARE,
    "delaware mountain": FormationType.DELAWARE,
    "delaware sand": FormationType.DELAWARE,
    "bell canyon": FormationType.DELAWARE,
    "cherry canyon": FormationType.DELAWARE,
    "avalon": FormationType.AVALON,
    "avalon shale": FormationType.AVALON,
    "brushy canyon": FormationType.BRUSHY_CANYON,
    "cline": FormationType.CLINE,
    "cline shale": FormationType.CLINE,
    "strawn": FormationType.STRAWN,
    "strawn lime": FormationType.STRAWN,
    "atoka": FormationType.ATOKA,
    "morrow": FormationType.ATOKA,
    "ellenburger": FormationType.ELLENBURGER,
    "san andres": FormationType.SAN_ANDRES,
    "san andres dolomite": FormationType.SAN_ANDRES,
    "san andres lime": FormationType.SAN_ANDRES,
    "clear fork": FormationType.CLEAR_FORK,
    "wichita albany": FormationType.CLEAR_FORK,
    "glorieta": FormationType.GLORIETA,
    "yeso": FormationType.YESO,
    "queen": FormationType.QUEEN,
    "queen sand": FormationType.QUEEN,
    "grayburg": FormationType.GRAYBURG,
    "devonian": FormationType.DEVONIAN,
    "thirtyone": FormationType.DEVONIAN,
    "woodford": FormationType.WOODFORD,
    "woodford shale": FormationType.WOODFORD,
    "barnett": FormationType.BARNETT,
    "barnett shale": FormationType.BARNETT,
    "mississippian": FormationType.MISSISSIPPIAN,
    "mississippian lime": FormationType.MISSISSIPPIAN,
}

# Texas county to RRC district mapping (Permian Basin)
COUNTY_TO_RRC_DISTRICT: Dict[str, str] = {
    "midland": "8",
    "ector": "8",
    "martin": "8",
    "andrews": "8",
    "howard": "8",
    "glasscock": "8",
    "upton": "8",
    "crane": "8",
    "reeves": "8",
    "ward": "8",
    "loving": "8",
    "winkler": "8",
    "pecos": "8",
    "terrell": "8",
    "crockett": "7C",
    "irion": "7C",
    "reagan": "7C",
    "sterling": "7C",
    "sutton": "7C",
    "schleicher": "7C",
    "tom green": "7C",
    "culberson": "8",
    "jeff davis": "8",
    "brewster": "8",
    "presidio": "8",
    "gaines": "8A",
    "dawson": "8A",
    "borden": "8A",
    "scurry": "8A",
    "lynn": "8A",
    "garza": "8A",
    "yoakum": "8A",
    "terry": "8A",
    "hockley": "8A",
    "lubbock": "8A",
    "cochran": "8A",
    "lamb": "8A",
    "lea": "NM",  # New Mexico — Permian Basin extends across state line
    "eddy": "NM",
    "chaves": "NM",
}

# Major Permian Basin operators (name normalization)
OPERATOR_ALIASES: Dict[str, str] = {
    "pioneer": "Pioneer Natural Resources",
    "pioneer natural resources": "Pioneer Natural Resources",
    "pxd": "Pioneer Natural Resources",
    "concho": "ConocoPhillips (fka Concho Resources)",
    "concho resources": "ConocoPhillips (fka Concho Resources)",
    "diamondback": "Diamondback Energy",
    "diamondback energy": "Diamondback Energy",
    "fang": "Diamondback Energy",
    "apache": "APA Corporation",
    "apa": "APA Corporation",
    "apa corp": "APA Corporation",
    "oxy": "Occidental Petroleum",
    "occidental": "Occidental Petroleum",
    "occidental petroleum": "Occidental Petroleum",
    "conocophillips": "ConocoPhillips",
    "conoco": "ConocoPhillips",
    "cop": "ConocoPhillips",
    "chevron": "Chevron Corporation",
    "cvx": "Chevron Corporation",
    "exxon": "ExxonMobil",
    "exxonmobil": "ExxonMobil",
    "xom": "ExxonMobil",
    "eog": "EOG Resources",
    "eog resources": "EOG Resources",
    "devon": "Devon Energy",
    "devon energy": "Devon Energy",
    "dvn": "Devon Energy",
    "coterra": "Coterra Energy",
    "coterra energy": "Coterra Energy",
    "callon": "APA Corporation (fka Callon Petroleum)",
    "callon petroleum": "APA Corporation (fka Callon Petroleum)",
    "centennial": "Ovintiv (fka Centennial Resource Dev.)",
    "ovintiv": "Ovintiv",
    "laredo": "Vital Energy (fka Laredo Petroleum)",
    "laredo petroleum": "Vital Energy (fka Laredo Petroleum)",
    "vital energy": "Vital Energy",
    "permian resources": "Permian Resources",
    "centennial resource development": "Permian Resources (fka Centennial)",
    "endeavor": "Diamondback Energy (fka Endeavor Energy)",
    "endeavor energy": "Diamondback Energy (fka Endeavor Energy)",
    "fasken": "Fasken Oil and Ranch",
    "fasken oil": "Fasken Oil and Ranch",
    "henry resources": "Henry Resources",
    "henry": "Henry Resources",
    "mewbourne": "Mewbourne Oil Company",
    "mewbourne oil": "Mewbourne Oil Company",
    "surge": "Surge Energy",
    "surge energy": "Surge Energy",
    "ring energy": "Ring Energy",
    "ring": "Ring Energy",
}

# Lease term glossary (plain English definitions)
LEASE_TERM_GLOSSARY: Dict[str, str] = {
    "habendum clause": "The 'to have and to hold' clause defining the duration of the lease grant, including primary and secondary terms.",
    "granting clause": "The clause that conveys the mineral rights from lessor to lessee, defining the scope of the lease.",
    "primary term": "The fixed period (typically 3-5 years) during which the lessee holds the lease without production.",
    "secondary term": "The indefinite period after the primary term, maintained by continued production or operations.",
    "delay rental": "Annual payment to keep the lease alive during the primary term without drilling.",
    "paid-up lease": "A lease where the entire delay rental obligation is included in the bonus payment.",
    "bonus consideration": "The upfront cash payment from lessee to lessor for executing the lease.",
    "royalty": "The lessor's share of production revenue, free of production costs.",
    "overriding royalty interest": "A non-cost-bearing interest carved from the working interest, terminating with the lease.",
    "working interest": "The cost-bearing interest that has the right to drill and operate on the lease.",
    "net revenue interest": "The share of production revenue actually received after all burdens are deducted.",
    "division order": "A document specifying each interest owner's share of production revenue from a well.",
    "pooling": "Combining two or more tracts into a single drilling or production unit.",
    "unitization": "Combining multiple leases into a single operating unit for enhanced recovery.",
    "Pugh clause": "Provision releasing non-pooled or non-producing acreage at end of primary term.",
    "shut-in royalty": "Payment to keep lease alive when a well is capable of producing but not producing.",
    "force majeure": "Clause excusing performance when prevented by events beyond reasonable control.",
    "continuous development": "Obligation to maintain an ongoing drilling program to hold acreage.",
    "cessation of production": "Clause providing a grace period if production temporarily stops.",
    "held by production": "Lease status when production maintains the lease in the secondary term.",
    "paying quantities": "Production sufficient to yield a profit to a reasonably prudent operator.",
    "depth limitation": "Clause restricting the lease to specific depth intervals or formations.",
    "retained acreage": "Land kept by the lessee after Pugh clause releases non-producing acreage.",
    "top lease": "A lease that takes effect upon expiration of an existing underlying lease.",
    "Mother Hubbard clause": "Clause covering small strips or tracts adjacent to the described lands.",
    "surrender clause": "Clause giving the lessee the right to release all or part of the lease.",
    "accommodation doctrine": "Limits mineral estate's surface use when alternative means are available.",
    "dominant estate": "The mineral estate, which has superior rights to use the surface for development.",
    "farmout agreement": "Agreement where one party earns interest by drilling a well on another's lease.",
    "farmin": "The party drilling the well and earning the interest under a farmout.",
    "farmor": "The party granting the farmout opportunity.",
    "farmee": "Synonym for farmin — the party earning the interest by drilling.",
    "back-in": "A right to convert a reserved ORRI into a working interest after payout.",
    "payout": "The point at which the working interest owner has recouped drilling and completion costs.",
    "dry hole clause": "Clause specifying what happens if the first well is a dry hole.",
    "offset well": "A well drilled to prevent drainage of leased minerals by an adjacent well.",
    "drainage": "Production from an adjacent tract that draws hydrocarbons from under the leased land.",
    "implied covenant to develop": "Unwritten obligation requiring lessee to develop as a prudent operator.",
    "implied covenant to protect": "Unwritten obligation to drill offset wells to prevent drainage.",
    "reasonably prudent operator": "The standard of care for lessee conduct — what a reasonable operator would do.",
    "severance tax": "State tax on oil and gas production at the wellhead (TX: 4.6% oil, 7.5% gas).",
    "ad valorem tax": "Property tax on mineral interests based on assessed value.",
    "lease form": "The standard form used for the lease (e.g., Producers 88, AAPL 610).",
    "Producers 88": "The most common oil and gas lease form in Texas, published by the Producers Association.",
    "AAPL 610": "Standard lease form published by the American Association of Professional Landmen.",
}


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_royalty_fraction(text: str) -> ParsedFraction:
    """Parse a royalty fraction from text, supporting fraction notation and decimal.

    Handles formats: '1/8', '3/16', '0.25', '25%', 'one-eighth', 'twenty-five percent'.

    Args:
        text: The text containing a royalty fraction.

    Returns:
        ParsedFraction with the parsed result.
    """
    text = text.strip()

    # Check for exact match in common fractions
    if text in COMMON_ROYALTY_FRACTIONS:
        frac = Fraction(text)
        return ParsedFraction(
            original_text=text,
            numerator=frac.numerator,
            denominator=frac.denominator,
            decimal_value=COMMON_ROYALTY_FRACTIONS[text],
            fraction_str=text,
            is_valid=True,
        )

    # Try fraction pattern: digits/digits
    fraction_match = re.match(r"(\d+)\s*/\s*(\d+)", text)
    if fraction_match:
        num = int(fraction_match.group(1))
        den = int(fraction_match.group(2))
        if den == 0:
            return ParsedFraction(
                original_text=text, numerator=0, denominator=0,
                decimal_value=0.0, fraction_str="0/0", is_valid=False,
                error_message="Division by zero in fraction",
            )
        decimal_val = num / den
        if decimal_val > 1.0:
            return ParsedFraction(
                original_text=text, numerator=num, denominator=den,
                decimal_value=decimal_val, fraction_str=f"{num}/{den}", is_valid=False,
                error_message=f"Fraction {num}/{den} exceeds 1.0 — likely invalid for royalty",
            )
        return ParsedFraction(
            original_text=text, numerator=num, denominator=den,
            decimal_value=decimal_val, fraction_str=f"{num}/{den}", is_valid=True,
        )

    # Try decimal pattern: 0.xxx
    decimal_match = re.match(r"(\d*\.\d+)", text)
    if decimal_match:
        decimal_val = float(decimal_match.group(1))
        if decimal_val > 1.0:
            return ParsedFraction(
                original_text=text, numerator=0, denominator=0,
                decimal_value=decimal_val, fraction_str="", is_valid=False,
                error_message=f"Decimal value {decimal_val} exceeds 1.0",
            )
        frac = Fraction(decimal_val).limit_denominator(1000)
        return ParsedFraction(
            original_text=text, numerator=frac.numerator, denominator=frac.denominator,
            decimal_value=decimal_val, fraction_str=f"{frac.numerator}/{frac.denominator}",
            is_valid=True,
        )

    # Try percentage pattern: xx%
    pct_match = re.match(r"(\d+(?:\.\d+)?)\s*%", text)
    if pct_match:
        pct_val = float(pct_match.group(1))
        decimal_val = pct_val / 100.0
        if decimal_val > 1.0:
            return ParsedFraction(
                original_text=text, numerator=0, denominator=0,
                decimal_value=decimal_val, fraction_str="", is_valid=False,
                error_message=f"Percentage {pct_val}% exceeds 100%",
            )
        frac = Fraction(decimal_val).limit_denominator(1000)
        return ParsedFraction(
            original_text=text, numerator=frac.numerator, denominator=frac.denominator,
            decimal_value=decimal_val, fraction_str=f"{frac.numerator}/{frac.denominator}",
            is_valid=True,
        )

    # Try word fractions
    word_fractions: Dict[str, Tuple[int, int]] = {
        "one-eighth": (1, 8), "one eighth": (1, 8),
        "three-sixteenths": (3, 16), "three sixteenths": (3, 16),
        "one-fifth": (1, 5), "one fifth": (1, 5),
        "one-fourth": (1, 4), "one fourth": (1, 4), "one quarter": (1, 4), "one-quarter": (1, 4),
        "one-third": (1, 3), "one third": (1, 3),
        "three-eighths": (3, 8), "three eighths": (3, 8),
        "one-half": (1, 2), "one half": (1, 2),
        "five-sixteenths": (5, 16), "five sixteenths": (5, 16),
    }
    text_lower = text.lower()
    for word, (num, den) in word_fractions.items():
        if word in text_lower:
            return ParsedFraction(
                original_text=text, numerator=num, denominator=den,
                decimal_value=num / den, fraction_str=f"{num}/{den}", is_valid=True,
            )

    return ParsedFraction(
        original_text=text, numerator=0, denominator=0,
        decimal_value=0.0, fraction_str="", is_valid=False,
        error_message=f"Could not parse fraction from: '{text}'",
    )


def parse_legal_description(text: str) -> LegalDescription:
    """Parse a Texas legal description from text.

    Supports multiple formats:
    - Section/Block/Township/Range (PLSS)
    - Abstract/Survey
    - Lot/Block/Subdivision
    - Metes and bounds (detected but not parsed)

    Args:
        text: The legal description text to parse.

    Returns:
        LegalDescription with parsed components.
    """
    result = LegalDescription(original_text=text)
    text_upper = text.upper().strip()
    confidence_points = 0
    max_confidence_points = 8

    # Detect metes and bounds
    metes_indicators = ["BEGINNING AT", "THENCE", "BEARING", "DEGREES", "MINUTES", "ALONG THE"]
    if any(ind in text_upper for ind in metes_indicators):
        result.metes_and_bounds = True
        result.confidence = 0.3
        result.parse_errors.append("Metes and bounds description detected but not fully parsed")
        return result

    # Parse Section
    section_patterns = [
        r"(?:SEC(?:TION)?\.?\s*|S(?:EC)?\.?\s+)(\d+)",
        r"SECTION\s+(\d+)",
    ]
    for pat in section_patterns:
        m = re.search(pat, text_upper)
        if m:
            result.section = m.group(1)
            confidence_points += 1
            break

    # Parse Block
    block_patterns = [
        r"(?:BL(?:OC)?K\.?\s*|BLK\.?\s+)([A-Z0-9\-]+)",
        r"BLOCK\s+([A-Z0-9\-]+)",
    ]
    for pat in block_patterns:
        m = re.search(pat, text_upper)
        if m:
            result.block = m.group(1)
            confidence_points += 1
            break

    # Parse Township
    township_match = re.search(r"T(?:OWN(?:SHIP)?)?\.?\s*(\d+[NS]?)", text_upper)
    if township_match:
        result.township = township_match.group(1)
        confidence_points += 1

    # Parse Range
    range_match = re.search(r"R(?:(?:AN)?GE)?\.?\s*(\d+[EW]?)", text_upper)
    if range_match:
        result.range_value = range_match.group(1)
        confidence_points += 1

    # Parse Abstract number
    abstract_patterns = [
        r"A(?:BSTRACT)?[\.\-\s]+(\d+)",
        r"ABS(?:T)?\.?\s*(?:#?\s*)?(\d+)",
    ]
    for pat in abstract_patterns:
        m = re.search(pat, text_upper)
        if m:
            result.abstract_number = m.group(1)
            confidence_points += 1
            break

    # Parse Survey name
    survey_patterns = [
        r"([A-Z][A-Z\.\s]+?)\s+SURV(?:EY)?",
        r"SURV(?:EY)?\s*[:\-]?\s*([A-Z][A-Z\.\s]+)",
        r"([A-Z&]+(?:\s+[A-Z&]+)*)\s+SUR(?:VEY)?",
    ]
    for pat in survey_patterns:
        m = re.search(pat, text_upper)
        if m:
            name = m.group(1).strip()
            if len(name) > 2 and name not in ("THE", "AND", "FOR"):
                result.survey_name = name.title()
                confidence_points += 1
                break

    # Parse Lot
    lot_match = re.search(r"LOT\s+(\d+)", text_upper)
    if lot_match:
        result.lot = lot_match.group(1)
        confidence_points += 0.5

    # Parse Subdivision
    subdiv_match = re.search(r"(?:SUBDIVISION|SUBD(?:IV)?\.?)\s+(.+?)(?:,|\.|$)", text_upper)
    if subdiv_match:
        result.subdivision = subdiv_match.group(1).strip().title()
        confidence_points += 0.5

    # Parse County
    county_match = re.search(r"([A-Z][A-Z\s]+?)\s+CO(?:UNTY)?\.?(?:\s*,\s*(?:TX|TEXAS))?", text_upper)
    if county_match:
        county_name = county_match.group(1).strip().title()
        if county_name.lower() in COUNTY_TO_RRC_DISTRICT:
            result.county = county_name
            confidence_points += 1
        elif len(county_name) > 2:
            result.county = county_name
            confidence_points += 0.5

    # Parse Acres
    acre_match = re.search(r"(\d+(?:\.\d+)?)\s+(?:AC(?:RES)?|ACRES?\b)", text_upper)
    if acre_match:
        result.acres = float(acre_match.group(1))
        confidence_points += 0.5

    result.confidence = min(confidence_points / max_confidence_points, 1.0)

    if confidence_points < 1:
        result.parse_errors.append("Could not parse any standard legal description components")

    return result


def normalize_lease_term(term: str) -> NormalizationResult:
    """Normalize an oil and gas lease term to its canonical form.

    Args:
        term: The term to normalize.

    Returns:
        NormalizationResult with canonical form and metadata.
    """
    term_stripped = term.strip()
    term_lower = term_stripped.lower()

    # Check interest type synonyms
    if term_lower in INTEREST_TYPE_SYNONYMS:
        interest_type = INTEREST_TYPE_SYNONYMS[term_lower]
        aliases = [k for k, v in INTEREST_TYPE_SYNONYMS.items() if v == interest_type and k != term_lower]
        return NormalizationResult(
            original=term_stripped,
            normalized=interest_type.value,
            category="interest_type",
            confidence=1.0,
            aliases=aliases,
        )

    # Check party role synonyms
    if term_lower in PARTY_ROLE_SYNONYMS:
        role = PARTY_ROLE_SYNONYMS[term_lower]
        aliases = [k for k, v in PARTY_ROLE_SYNONYMS.items() if v == role and k != term_lower]
        return NormalizationResult(
            original=term_stripped,
            normalized=role.value,
            category="party_role",
            confidence=1.0,
            aliases=aliases,
        )

    # Check formation aliases
    if term_lower in FORMATION_ALIASES:
        formation = FORMATION_ALIASES[term_lower]
        aliases = [k for k, v in FORMATION_ALIASES.items() if v == formation and k != term_lower]
        return NormalizationResult(
            original=term_stripped,
            normalized=formation.value,
            category="formation",
            confidence=1.0,
            aliases=aliases,
        )

    # Check operator aliases
    if term_lower in OPERATOR_ALIASES:
        operator = OPERATOR_ALIASES[term_lower]
        aliases = [k for k, v in OPERATOR_ALIASES.items() if v == operator and k != term_lower]
        return NormalizationResult(
            original=term_stripped,
            normalized=operator,
            category="operator",
            confidence=1.0,
            aliases=aliases,
        )

    # Check glossary terms
    if term_lower in LEASE_TERM_GLOSSARY:
        return NormalizationResult(
            original=term_stripped,
            normalized=term_lower,
            category="glossary_term",
            confidence=0.9,
            notes=LEASE_TERM_GLOSSARY[term_lower],
        )

    # Fuzzy matching — check for partial matches
    best_match: Optional[Tuple[str, str, float]] = None
    all_dicts: List[Tuple[Dict[str, Any], str]] = [
        (INTEREST_TYPE_SYNONYMS, "interest_type"),
        (PARTY_ROLE_SYNONYMS, "party_role"),
        (FORMATION_ALIASES, "formation"),
        (OPERATOR_ALIASES, "operator"),
    ]
    for d, cat in all_dicts:
        for key in d:
            if term_lower in key or key in term_lower:
                overlap = len(set(term_lower.split()) & set(key.split()))
                score = overlap / max(len(term_lower.split()), len(key.split()))
                if score > 0.5 and (best_match is None or score > best_match[2]):
                    val = d[key]
                    normalized = val.value if hasattr(val, "value") else str(val)
                    best_match = (normalized, cat, score)

    if best_match:
        return NormalizationResult(
            original=term_stripped,
            normalized=best_match[0],
            category=best_match[1],
            confidence=best_match[2],
            notes="Fuzzy match — verify correctness",
        )

    return NormalizationResult(
        original=term_stripped,
        normalized=term_stripped.lower(),
        category="unknown",
        confidence=0.0,
        notes="No match found in semantic dictionaries",
    )


def identify_clause_types(text: str) -> List[Tuple[LeaseClauseType, float, List[str]]]:
    """Identify lease clause types present in a block of text.

    Args:
        text: The lease text to analyze.

    Returns:
        List of (clause_type, confidence, matched_indicators) sorted by confidence descending.
    """
    text_lower = text.lower()
    results: List[Tuple[LeaseClauseType, float, List[str]]] = []

    for clause_type, indicators in CLAUSE_TYPE_INDICATORS.items():
        matched = [ind for ind in indicators if ind.lower() in text_lower]
        if matched:
            confidence = min(len(matched) / len(indicators), 1.0)
            results.append((clause_type, confidence, matched))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def normalize_formation_name(name: str) -> Optional[FormationType]:
    """Normalize a formation name to its canonical FormationType.

    Args:
        name: The formation name to normalize.

    Returns:
        The matching FormationType, or None if not recognized.
    """
    name_lower = name.strip().lower()
    return FORMATION_ALIASES.get(name_lower)


def normalize_operator_name(name: str) -> str:
    """Normalize an operator name to its canonical form.

    Args:
        name: The operator name to normalize.

    Returns:
        The canonical operator name, or the original if not recognized.
    """
    name_lower = name.strip().lower()
    return OPERATOR_ALIASES.get(name_lower, name.strip())


def get_rrc_district(county: str) -> Optional[str]:
    """Get the RRC district for a Texas county.

    Args:
        county: County name.

    Returns:
        RRC district string, or None if not in the Permian Basin.
    """
    return COUNTY_TO_RRC_DISTRICT.get(county.strip().lower())


def parse_depth_interval(text: str) -> Optional[DepthInterval]:
    """Parse a depth interval description from text.

    Handles formats like:
    - "from 5,000 feet to 10,000 feet"
    - "above 8000'"
    - "below the Wolfcamp formation"
    - "Spraberry through Wolfcamp"

    Args:
        text: Text containing a depth description.

    Returns:
        DepthInterval if parseable, None otherwise.
    """
    text_clean = text.strip()
    interval = DepthInterval(description=text_clean)

    # Pattern: "from X feet to Y feet"
    range_match = re.search(
        r"from\s+([\d,]+)\s*(?:feet|ft|')\s*to\s+([\d,]+)\s*(?:feet|ft|')",
        text_clean,
        re.IGNORECASE,
    )
    if range_match:
        interval.top_depth_ft = float(range_match.group(1).replace(",", ""))
        interval.bottom_depth_ft = float(range_match.group(2).replace(",", ""))
        return interval

    # Pattern: "above X feet" or "shallower than X feet"
    above_match = re.search(
        r"(?:above|shallower than)\s+([\d,]+)\s*(?:feet|ft|')",
        text_clean,
        re.IGNORECASE,
    )
    if above_match:
        interval.top_depth_ft = 0
        interval.bottom_depth_ft = float(above_match.group(1).replace(",", ""))
        return interval

    # Pattern: "below X feet" or "deeper than X feet"
    below_match = re.search(
        r"(?:below|deeper than)\s+([\d,]+)\s*(?:feet|ft|')",
        text_clean,
        re.IGNORECASE,
    )
    if below_match:
        interval.top_depth_ft = float(below_match.group(1).replace(",", ""))
        interval.bottom_depth_ft = 99999.0  # To center of earth
        return interval

    # Pattern: formation name
    text_lower = text_clean.lower()
    for alias, formation in FORMATION_ALIASES.items():
        if alias in text_lower:
            interval.formation_name = alias.title()
            interval.formation_type = formation
            return interval

    return None


def get_glossary_definition(term: str) -> Optional[str]:
    """Look up a lease term in the glossary.

    Args:
        term: The term to look up.

    Returns:
        The definition string, or None if not found.
    """
    return LEASE_TERM_GLOSSARY.get(term.strip().lower())


def verify_semantic_map_integrity() -> Dict[str, Any]:
    """Verify the integrity and completeness of all semantic maps.

    Returns:
        Dictionary with integrity check results.
    """
    results: Dict[str, Any] = {
        "version": SEMANTIC_MAP_VERSION,
        "build_date": SEMANTIC_MAP_BUILD_DATE,
        "checks": [],
        "all_passed": True,
    }

    # Check party role synonyms
    role_check = {
        "name": "party_role_synonyms",
        "total_entries": len(PARTY_ROLE_SYNONYMS),
        "unique_roles": len(set(PARTY_ROLE_SYNONYMS.values())),
        "passed": len(PARTY_ROLE_SYNONYMS) > 10,
    }
    results["checks"].append(role_check)

    # Check interest type synonyms
    interest_check = {
        "name": "interest_type_synonyms",
        "total_entries": len(INTEREST_TYPE_SYNONYMS),
        "unique_types": len(set(INTEREST_TYPE_SYNONYMS.values())),
        "passed": len(INTEREST_TYPE_SYNONYMS) > 15,
    }
    results["checks"].append(interest_check)

    # Check clause type indicators
    clause_check = {
        "name": "clause_type_indicators",
        "total_clause_types": len(CLAUSE_TYPE_INDICATORS),
        "total_indicators": sum(len(v) for v in CLAUSE_TYPE_INDICATORS.values()),
        "passed": len(CLAUSE_TYPE_INDICATORS) >= 20,
    }
    results["checks"].append(clause_check)

    # Check formation aliases
    formation_check = {
        "name": "formation_aliases",
        "total_entries": len(FORMATION_ALIASES),
        "unique_formations": len(set(FORMATION_ALIASES.values())),
        "passed": len(FORMATION_ALIASES) > 30,
    }
    results["checks"].append(formation_check)

    # Check operator aliases
    operator_check = {
        "name": "operator_aliases",
        "total_entries": len(OPERATOR_ALIASES),
        "unique_operators": len(set(OPERATOR_ALIASES.values())),
        "passed": len(OPERATOR_ALIASES) > 20,
    }
    results["checks"].append(operator_check)

    # Check county mapping
    county_check = {
        "name": "county_to_rrc_district",
        "total_counties": len(COUNTY_TO_RRC_DISTRICT),
        "unique_districts": len(set(COUNTY_TO_RRC_DISTRICT.values())),
        "passed": len(COUNTY_TO_RRC_DISTRICT) > 20,
    }
    results["checks"].append(county_check)

    # Check glossary
    glossary_check = {
        "name": "lease_term_glossary",
        "total_terms": len(LEASE_TERM_GLOSSARY),
        "passed": len(LEASE_TERM_GLOSSARY) > 30,
    }
    results["checks"].append(glossary_check)

    # Check common royalty fractions
    fraction_check = {
        "name": "common_royalty_fractions",
        "total_entries": len(COMMON_ROYALTY_FRACTIONS),
        "passed": len(COMMON_ROYALTY_FRACTIONS) > 8,
    }
    results["checks"].append(fraction_check)

    for check in results["checks"]:
        if not check["passed"]:
            results["all_passed"] = False

    # Compute hash
    hash_data = json.dumps({
        "party_roles": len(PARTY_ROLE_SYNONYMS),
        "interest_types": len(INTEREST_TYPE_SYNONYMS),
        "clause_indicators": len(CLAUSE_TYPE_INDICATORS),
        "formations": len(FORMATION_ALIASES),
        "operators": len(OPERATOR_ALIASES),
        "counties": len(COUNTY_TO_RRC_DISTRICT),
        "glossary": len(LEASE_TERM_GLOSSARY),
        "fractions": len(COMMON_ROYALTY_FRACTIONS),
    }, sort_keys=True)
    results["hash"] = hashlib.sha256(hash_data.encode()).hexdigest()

    return results


# Module load log
_integrity = verify_semantic_map_integrity()
logger.info(
    f"LM02 Semantic Map loaded: {_integrity['checks'][0]['total_entries']} party roles, "
    f"{_integrity['checks'][1]['total_entries']} interest types, "
    f"{_integrity['checks'][3]['total_entries']} formations, "
    f"{_integrity['checks'][6]['total_terms']} glossary terms, "
    f"hash={_integrity['hash'][:16]}..."
)
