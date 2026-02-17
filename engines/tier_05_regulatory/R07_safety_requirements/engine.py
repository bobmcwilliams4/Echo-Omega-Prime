"""
ECHO R07 SAFETY REQUIREMENTS ENGINE -- TIE-20 Gold Standard
============================================================
Professional-grade safety compliance intelligence for oil & gas operations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled OSHA/BSEE/EPA reasoning
    Layer 2: Semantic Retrieval (200-700ms) - Vector search on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source regulatory synthesis

Response Modes:
    FAST:    Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, penalty analysis
    MEMO:    Long-form, citation-heavy, regulatory memorandum

Domain: OSHA 1910/1926, H2S (ANSI Z390.1), BOP (API Spec 53), PSM (29 CFR
         1910.119), RMP (40 CFR Part 68), well control, confined space entry,
         fall protection, PPE, lockout/tagout, electrical safety

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8707
Version: 2.0.0
"""

# =============================================================================
# IMPORTS
# =============================================================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import time
import uuid
from pathlib import Path
from loguru import logger
import sys

# =============================================================================
# PATH SETUP - Must precede local imports
# =============================================================================

ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

# =============================================================================
# LOCAL IMPORTS - from sibling modules
# =============================================================================

from telemetry import get_telemetry, trace_query, complete_trace, log_error, ErrorDomain
from semantic import normalize_semantics, NormalizationResult
from doctrines import DOCTRINE_CACHE, DoctrineBlock, match_doctrines, ConfidenceStratification
from search import vector_search

# =============================================================================
# CLOUD RETRIEVER - optional enrichment from Cloudflare R2
# =============================================================================

try:
    from cloud_retriever import cloud_retrieve, CloudResult
    CLOUD_RETRIEVER_AVAILABLE = True
    logger.info("Cloud retriever loaded successfully")
except ImportError:
    CLOUD_RETRIEVER_AVAILABLE = False
    logger.info("Cloud retriever not available -- operating in local mode")

# =============================================================================
# CONSTANTS
# =============================================================================

ENGINE_NAME = "R07_safety_requirements"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8707
ENGINE_DOMAIN = "Safety Compliance for Oil & Gas Operations"

# OSHA penalty rates (2024 adjusted annually)
OSHA_PENALTY_SERIOUS = 15_653
OSHA_PENALTY_WILLFUL = 156_529
OSHA_PENALTY_REPEAT = 156_529
OSHA_PENALTY_FAILURE_TO_ABATE = 15_653  # per day
BSEE_PENALTY_PER_DAY = 46_000
EPA_RMP_PENALTY = 69_733  # per day per violation

BANNED_PHRASES = [
    "this is not legal advice",
    "consult a lawyer",
    "I am an AI",
    "as a language model",
    "I cannot provide",
    "in my opinion",
    "I think",
    "I believe",
    "it depends",
    "generally speaking",
]

# =============================================================================
# LOGGING
# =============================================================================

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/R07_safety_requirements/logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

logger.add(
    LOG_DIR / "r07_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# =============================================================================
# [TIE-04] AUTHORITY HARDENING
# =============================================================================

class AuthorityLevel(str, Enum):
    """Regulatory authority hierarchy for safety compliance."""
    FEDERAL_STATUTE = "federal_statute"
    FEDERAL_REGULATION = "federal_regulation"
    ANSI_STANDARD = "ansi_standard"
    API_STANDARD = "api_standard"
    STATE_REGULATION = "state_regulation"
    BSEE_REGULATION = "bsee_regulation"
    EPA_REGULATION = "epa_regulation"
    AGENCY_GUIDANCE = "agency_guidance"
    INDUSTRY_BEST_PRACTICE = "industry_best_practice"
    COMPANY_POLICY = "company_policy"

AUTHORITY_WEIGHTS: Dict[str, float] = {
    # Federal statutes -- highest weight
    "OSH Act of 1970": 1.00,
    "Clean Air Act Section 112(r)": 1.00,
    "OPA 90": 0.98,
    # Federal regulations -- OSHA
    "29 CFR 1910.119": 0.97,       # PSM
    "29 CFR 1910.146": 0.97,       # Confined Spaces
    "29 CFR 1910.134": 0.96,       # Respiratory Protection
    "29 CFR 1910.147": 0.96,       # LOTO
    "29 CFR 1910.1200": 0.96,      # HazCom
    "29 CFR 1910.28": 0.95,        # Fall Protection General Industry
    "29 CFR 1910.132": 0.95,       # PPE General
    "29 CFR 1910.1000": 0.94,      # Air Contaminants (PELs)
    "29 CFR 1926.501": 0.95,       # Fall Protection Construction
    "29 CFR 1926.1101": 0.94,      # Asbestos
    "29 CFR 1926.1153": 0.94,      # Silica
    # OSHA General Duty Clause
    "29 CFR 5(a)(1)": 0.99,        # General Duty Clause
    # EPA RMP
    "40 CFR Part 68": 0.96,        # Risk Management Plans
    # BSEE regulations -- offshore
    "30 CFR 250": 0.96,            # BSEE Oil and Gas Sulphur Operations
    "30 CFR 250.198": 0.95,        # Equipment testing
    "30 CFR 250.1628": 0.94,       # BOP testing offshore
    # ANSI standards
    "ANSI Z390.1": 0.93,           # H2S
    "ANSI Z359.1": 0.92,           # Fall Protection
    "ANSI Z87.1": 0.90,            # Eye Protection
    "ANSI Z88.2": 0.91,            # Respiratory Protection
    # API standards
    "API Spec 53": 0.92,           # BOP
    "API RP 53": 0.91,             # BOP Testing
    "API RP 54": 0.90,             # Occupational Safety for O&G
    "API RP 75": 0.91,             # SEMS (Safety and Environmental Management)
    "API RP 2003": 0.89,           # Protection Against Ignitions
    "API RP 2201": 0.88,           # Hot Tapping/Welding
    "API RP 2210": 0.87,           # Flame Arrestors
    "API RP 2350": 0.88,           # Overfill Protection
    # State regulations -- Texas
    "16 TAC Chapter 3": 0.88,      # Texas RRC
    "16 TAC 3.13": 0.86,           # Casing/Cementing
    "16 TAC 3.17": 0.85,           # Statewide Rule 17 - Pressure
    # NFPA
    "NFPA 70E": 0.90,              # Electrical Safety
    "NFPA 30": 0.88,               # Flammable Liquids
    "NFPA 51B": 0.87,              # Hot Work
    # General
    "Agency Guidance": 0.50,
    "Industry Best Practice": 0.40,
    "Company Policy": 0.30,
}


def classify_authority(reference: str) -> AuthorityLevel:
    """Classify a regulatory reference into its authority level."""
    ref_lower = reference.lower()
    if "osh act" in ref_lower or "clean air act" in ref_lower or "opa 90" in ref_lower:
        return AuthorityLevel.FEDERAL_STATUTE
    if "29 cfr" in ref_lower:
        return AuthorityLevel.FEDERAL_REGULATION
    if "30 cfr" in ref_lower:
        return AuthorityLevel.BSEE_REGULATION
    if "40 cfr" in ref_lower:
        return AuthorityLevel.EPA_REGULATION
    if "ansi" in ref_lower:
        return AuthorityLevel.ANSI_STANDARD
    if "api" in ref_lower:
        return AuthorityLevel.API_STANDARD
    if "tac" in ref_lower or "rrc" in ref_lower:
        return AuthorityLevel.STATE_REGULATION
    if "nfpa" in ref_lower:
        return AuthorityLevel.ANSI_STANDARD
    if "guidance" in ref_lower or "letter" in ref_lower:
        return AuthorityLevel.AGENCY_GUIDANCE
    if "best practice" in ref_lower or "recommended" in ref_lower:
        return AuthorityLevel.INDUSTRY_BEST_PRACTICE
    return AuthorityLevel.COMPANY_POLICY


def get_authority_weight(reference: str) -> float:
    """Get the numerical weight for a regulatory reference."""
    for key, weight in AUTHORITY_WEIGHTS.items():
        if key.lower() in reference.lower():
            return weight
    level = classify_authority(reference)
    level_defaults = {
        AuthorityLevel.FEDERAL_STATUTE: 0.98,
        AuthorityLevel.FEDERAL_REGULATION: 0.93,
        AuthorityLevel.BSEE_REGULATION: 0.92,
        AuthorityLevel.EPA_REGULATION: 0.92,
        AuthorityLevel.ANSI_STANDARD: 0.88,
        AuthorityLevel.API_STANDARD: 0.85,
        AuthorityLevel.STATE_REGULATION: 0.80,
        AuthorityLevel.AGENCY_GUIDANCE: 0.50,
        AuthorityLevel.INDUSTRY_BEST_PRACTICE: 0.40,
        AuthorityLevel.COMPANY_POLICY: 0.30,
    }
    return level_defaults.get(level, 0.30)


def resolve_authority_conflict(authorities: List[str]) -> Dict[str, Any]:
    """Resolve conflicts between multiple regulatory authorities.

    When OSHA, BSEE, EPA, and state regs overlap on the same topic,
    determine which controls and how they interact.

    Args:
        authorities: List of regulatory references to evaluate.

    Returns:
        Dict with controlling authority, hierarchy, and conflict analysis.
    """
    if not authorities:
        return {"controlling": None, "hierarchy": [], "conflicts": []}

    weighted = []
    for auth in authorities:
        weight = get_authority_weight(auth)
        level = classify_authority(auth)
        weighted.append({"authority": auth, "weight": weight, "level": level.value})

    weighted.sort(key=lambda x: x["weight"], reverse=True)

    conflicts = []
    # Detect federal vs state conflicts
    federal_refs = [w for w in weighted if w["level"] in (
        "federal_statute", "federal_regulation", "bsee_regulation", "epa_regulation"
    )]
    state_refs = [w for w in weighted if w["level"] == "state_regulation"]
    if federal_refs and state_refs:
        conflicts.append({
            "type": "federal_vs_state",
            "resolution": "Federal regulation preempts state where directly conflicting. "
                          "State regulations may impose ADDITIONAL requirements but cannot "
                          "reduce federal minimums. OSHA-approved state plans may enforce "
                          "equivalent or stricter standards.",
            "federal": [f["authority"] for f in federal_refs],
            "state": [s["authority"] for s in state_refs],
        })

    # Detect OSHA vs BSEE overlap (onshore vs offshore jurisdiction)
    osha_refs = [w for w in weighted if "29 cfr" in w["authority"].lower()]
    bsee_refs = [w for w in weighted if "30 cfr" in w["authority"].lower()]
    if osha_refs and bsee_refs:
        conflicts.append({
            "type": "osha_vs_bsee",
            "resolution": "Offshore operations: BSEE has primary jurisdiction for "
                          "drilling/production safety under 30 CFR 250. OSHA retains "
                          "jurisdiction for occupational safety (PPE, confined space, "
                          "fall protection) even offshore. MOUs between agencies define "
                          "boundaries. Operators must comply with BOTH.",
            "osha": [o["authority"] for o in osha_refs],
            "bsee": [b["authority"] for b in bsee_refs],
        })

    # Detect PSM vs RMP overlap
    psm_refs = [w for w in weighted if "1910.119" in w["authority"]]
    rmp_refs = [w for w in weighted if "40 cfr" in w["authority"].lower() or "rmp" in w["authority"].lower()]
    if psm_refs and rmp_refs:
        conflicts.append({
            "type": "psm_vs_rmp",
            "resolution": "PSM (OSHA 29 CFR 1910.119) and RMP (EPA 40 CFR Part 68) "
                          "apply concurrently to facilities with threshold quantities of "
                          "hazardous chemicals. PSM focuses on worker protection; RMP on "
                          "public/environmental protection. Both require PHA and similar "
                          "management systems. Compliance with one does NOT satisfy the other.",
            "psm": [p["authority"] for p in psm_refs],
            "rmp": [r["authority"] for r in rmp_refs],
        })

    return {
        "controlling": weighted[0]["authority"] if weighted else None,
        "hierarchy": weighted,
        "conflicts": conflicts,
        "total_authorities": len(weighted),
    }


# =============================================================================
# [TIE-05] CONFIDENCE STRATIFICATION
# =============================================================================

class ConfidenceTier(str, Enum):
    """Confidence stratification for safety compliance conclusions."""
    DEFENSIBLE = "defensible"
    AGGRESSIVE = "aggressive"
    DISCLOSURE = "disclosure"
    HIGH_RISK = "high_risk"


def classify_confidence(confidence: float, has_controlling_precedent: bool,
                        stratification: ConfidenceStratification) -> ConfidenceTier:
    """Classify the confidence level of a safety compliance conclusion.

    Args:
        confidence: Numerical confidence score (0.0-1.0).
        has_controlling_precedent: Whether a controlling regulation exists.
        stratification: The doctrine's own confidence stratification.

    Returns:
        ConfidenceTier indicating defensibility of the conclusion.
    """
    if stratification == ConfidenceStratification.MANDATORY:
        if confidence >= 0.85 and has_controlling_precedent:
            return ConfidenceTier.DEFENSIBLE
        if confidence >= 0.70:
            return ConfidenceTier.AGGRESSIVE
        return ConfidenceTier.DISCLOSURE

    if stratification == ConfidenceStratification.CLEARLY_REQUIRED:
        if confidence >= 0.80 and has_controlling_precedent:
            return ConfidenceTier.DEFENSIBLE
        if confidence >= 0.65:
            return ConfidenceTier.AGGRESSIVE
        return ConfidenceTier.DISCLOSURE

    # BEST_PRACTICE
    if confidence >= 0.90 and has_controlling_precedent:
        return ConfidenceTier.DEFENSIBLE
    if confidence >= 0.75:
        return ConfidenceTier.AGGRESSIVE
    if confidence >= 0.50:
        return ConfidenceTier.DISCLOSURE
    return ConfidenceTier.HIGH_RISK


# =============================================================================
# [TIE-06] SEMANTIC NORMALIZATION -- Safety-specific term mapping
# =============================================================================

SAFETY_TERM_NORMALIZATION: Dict[str, str] = {
    # OSHA terms
    "osha": "occupational safety and health administration",
    "general duty clause": "29 cfr 5(a)(1)",
    "gdc": "29 cfr 5(a)(1)",
    "pel": "permissible exposure limit",
    "stel": "short-term exposure limit",
    "twa": "time-weighted average",
    "hazcom": "hazard communication 29 cfr 1910.1200",
    "hazwoper": "hazardous waste operations 29 cfr 1910.120",
    "sds": "safety data sheet",
    "msds": "safety data sheet",
    "ghs": "globally harmonized system",
    "loto": "lockout tagout 29 cfr 1910.147",
    "lockout tagout": "lockout tagout 29 cfr 1910.147",
    "lock out tag out": "lockout tagout 29 cfr 1910.147",
    "ppe": "personal protective equipment 29 cfr 1910.132",
    "frc": "flame resistant clothing",
    "fpe": "fall protection equipment",
    "pfas": "personal fall arrest system",
    # H2S terms
    "h2s": "hydrogen sulfide",
    "sour gas": "hydrogen sulfide",
    "sour": "hydrogen sulfide",
    "sweet gas": "non-hydrogen-sulfide gas",
    "scba": "self-contained breathing apparatus",
    "sar": "supplied air respirator",
    "wind sock": "wind direction indicator h2s",
    "z390": "ansi z390.1 hydrogen sulfide",
    "z390.1": "ansi z390.1 hydrogen sulfide",
    # BOP terms
    "bop": "blowout preventer",
    "annular preventer": "annular blowout preventer",
    "rams": "ram blowout preventer",
    "blind ram": "blind ram bop",
    "shear ram": "shear ram bop",
    "pipe ram": "pipe ram bop",
    "diverter": "diverter system well control",
    "choke manifold": "choke manifold well control",
    "kill line": "kill line well control",
    "well kick": "well control kick detection",
    "kick": "well control kick detection",
    "blowout": "well control blowout event",
    # PSM terms
    "psm": "process safety management 29 cfr 1910.119",
    "pha": "process hazard analysis",
    "hazop": "hazard and operability study",
    "lopa": "layers of protection analysis",
    "moc": "management of change",
    "pssr": "pre-startup safety review",
    "mi": "mechanical integrity",
    "sil": "safety integrity level",
    "sis": "safety instrumented system",
    # RMP terms
    "rmp": "risk management plan 40 cfr part 68",
    "worst case scenario": "rmp worst case release scenario",
    "offsite consequence": "rmp offsite consequence analysis",
    # Well Control terms
    "well control": "well control operations",
    "iadc": "international association of drilling contractors",
    "wellcap": "well control certification program",
    "iwcf": "international well control forum",
    # Confined Space
    "permit required confined space": "permit-required confined space 29 cfr 1910.146",
    "prcs": "permit-required confined space 29 cfr 1910.146",
    "lel": "lower explosive limit",
    "uel": "upper explosive limit",
    # Fall Protection
    "guardrail": "guardrail system fall protection",
    "safety net": "safety net system fall protection",
    "srl": "self-retracting lifeline",
    "full body harness": "full-body harness fall arrest",
    # BSEE
    "bsee": "bureau of safety and environmental enforcement",
    "sems": "safety and environmental management system api rp 75",
    "sems ii": "safety and environmental management system final rule",
    # Electrical
    "arc flash": "arc flash hazard nfpa 70e",
    "gfci": "ground fault circuit interrupter",
    "nfpa 70e": "electrical safety workplace nfpa 70e",
    # Fire
    "hot work": "hot work permit nfpa 51b",
    "hot work permit": "hot work permit nfpa 51b",
    "fire watch": "fire watch hot work",
    # Agencies
    "rrc": "railroad commission of texas",
    "tceq": "texas commission on environmental quality",
    "epa": "environmental protection agency",
    "niosh": "national institute for occupational safety and health",
    "csb": "chemical safety board",
    "msha": "mine safety and health administration",
}


def normalize_safety_terms(text: str) -> str:
    """Apply safety-domain-specific term normalization on top of base normalization.

    Args:
        text: Text after base semantic normalization.

    Returns:
        Text with safety-specific terms expanded/normalized.
    """
    result = text.lower()
    for term, expansion in sorted(SAFETY_TERM_NORMALIZATION.items(),
                                   key=lambda x: len(x[0]), reverse=True):
        if term in result:
            result = result.replace(term, expansion)
    return result


# =============================================================================
# [TIE-19] MULTI-DOCTRINE DECOMPOSITION -- Safety Issue Categories
# =============================================================================

class SafetyIssueCategory(str, Enum):
    """Top-level safety issue classification for O&G operations."""
    OSHA_GENERAL_INDUSTRY = "osha_general_industry"
    OSHA_CONSTRUCTION = "osha_construction"
    H2S_SAFETY = "h2s_safety"
    BOP_WELL_CONTROL = "bop_well_control"
    PSM = "process_safety_management"
    RMP = "risk_management_plan"
    CONFINED_SPACE = "confined_space"
    FALL_PROTECTION = "fall_protection"
    PPE = "personal_protective_equipment"
    LOCKOUT_TAGOUT = "lockout_tagout"
    ELECTRICAL_SAFETY = "electrical_safety"
    HOT_WORK = "hot_work"
    RESPIRATORY_PROTECTION = "respiratory_protection"
    FIRE_PREVENTION = "fire_prevention"
    HAZCOM = "hazard_communication"
    BSEE_OFFSHORE = "bsee_offshore"
    ENVIRONMENTAL_COMPLIANCE = "environmental_compliance"
    TRANSPORTATION_SAFETY = "transportation_safety"
    CRANE_RIGGING = "crane_rigging"
    EXCAVATION_TRENCHING = "excavation_trenching"


INTERACTION_EDGES: List[Dict[str, Any]] = [
    {
        "from": SafetyIssueCategory.H2S_SAFETY,
        "to": SafetyIssueCategory.RESPIRATORY_PROTECTION,
        "relationship": "requires",
        "description": "H2S operations require respiratory protection program per 29 CFR 1910.134. "
                       "SCBA mandatory for concentrations above 20 ppm or unknown atmospheres.",
    },
    {
        "from": SafetyIssueCategory.H2S_SAFETY,
        "to": SafetyIssueCategory.CONFINED_SPACE,
        "relationship": "compound_hazard",
        "description": "H2S is primary atmospheric hazard in O&G confined spaces (tanks, vessels). "
                       "Confined space entry where H2S is possible triggers BOTH 1910.146 and Z390.1.",
    },
    {
        "from": SafetyIssueCategory.PSM,
        "to": SafetyIssueCategory.RMP,
        "relationship": "concurrent",
        "description": "PSM and RMP apply concurrently at facilities with threshold quantities. "
                       "PSM protects workers; RMP protects the public. Both require PHA.",
    },
    {
        "from": SafetyIssueCategory.PSM,
        "to": SafetyIssueCategory.HOT_WORK,
        "relationship": "requires",
        "description": "PSM element 8 requires hot work permits. Hot work in PSM-covered "
                       "areas requires PHA review and management of change (MOC) evaluation.",
    },
    {
        "from": SafetyIssueCategory.PSM,
        "to": SafetyIssueCategory.LOCKOUT_TAGOUT,
        "relationship": "requires",
        "description": "PSM mechanical integrity element requires LOTO for equipment maintenance. "
                       "29 CFR 1910.147 LOTO applies to all energy isolation in PSM facilities.",
    },
    {
        "from": SafetyIssueCategory.BOP_WELL_CONTROL,
        "to": SafetyIssueCategory.H2S_SAFETY,
        "relationship": "compound_hazard",
        "description": "Well control events in sour formations release H2S. BOP failure in "
                       "H2S zones creates immediate life-threatening exposure. Dual contingency required.",
    },
    {
        "from": SafetyIssueCategory.BOP_WELL_CONTROL,
        "to": SafetyIssueCategory.BSEE_OFFSHORE,
        "relationship": "regulated_by",
        "description": "Offshore BOP operations regulated by BSEE under 30 CFR 250. "
                       "Testing intervals, equipment specifications, and reporting all under BSEE jurisdiction.",
    },
    {
        "from": SafetyIssueCategory.FALL_PROTECTION,
        "to": SafetyIssueCategory.PPE,
        "relationship": "requires",
        "description": "Fall protection requires PPE: full-body harness, shock-absorbing lanyard, "
                       "anchorage. PPE inspection per 1910.132 and ANSI Z359.1 applies.",
    },
    {
        "from": SafetyIssueCategory.CONFINED_SPACE,
        "to": SafetyIssueCategory.RESPIRATORY_PROTECTION,
        "relationship": "requires",
        "description": "Permit-required confined space entry requires respiratory protection "
                       "when atmospheric hazards are present or potentially present.",
    },
    {
        "from": SafetyIssueCategory.CONFINED_SPACE,
        "to": SafetyIssueCategory.LOCKOUT_TAGOUT,
        "relationship": "requires",
        "description": "Confined space entry requires LOTO of all energy sources that could "
                       "create hazards within the space (mechanical, electrical, hydraulic, chemical).",
    },
    {
        "from": SafetyIssueCategory.HOT_WORK,
        "to": SafetyIssueCategory.FIRE_PREVENTION,
        "relationship": "requires",
        "description": "Hot work requires fire watch, fire extinguishers within 35 feet, "
                       "atmospheric testing for flammables, and fire watch for 60 minutes after.",
    },
    {
        "from": SafetyIssueCategory.ELECTRICAL_SAFETY,
        "to": SafetyIssueCategory.LOCKOUT_TAGOUT,
        "relationship": "requires",
        "description": "Electrical maintenance requires LOTO per 1910.147 and NFPA 70E "
                       "arc flash protection. Energized work permits required for live work.",
    },
    {
        "from": SafetyIssueCategory.HAZCOM,
        "to": SafetyIssueCategory.H2S_SAFETY,
        "relationship": "informs",
        "description": "HazCom SDS for H2S provides exposure limits, first aid, PPE requirements. "
                       "HazCom training must cover H2S-specific hazards in sour operations.",
    },
    {
        "from": SafetyIssueCategory.BSEE_OFFSHORE,
        "to": SafetyIssueCategory.ENVIRONMENTAL_COMPLIANCE,
        "relationship": "concurrent",
        "description": "BSEE offshore operations have concurrent environmental requirements "
                       "under NEPA, OPA 90, and Clean Water Act. Spill prevention plans required.",
    },
    {
        "from": SafetyIssueCategory.OSHA_CONSTRUCTION,
        "to": SafetyIssueCategory.EXCAVATION_TRENCHING,
        "relationship": "includes",
        "description": "Construction safety per 1926 Subpart P covers excavation and trenching. "
                       "Pipeline construction, tank foundations trigger excavation standards.",
    },
    {
        "from": SafetyIssueCategory.CRANE_RIGGING,
        "to": SafetyIssueCategory.FALL_PROTECTION,
        "relationship": "compound_hazard",
        "description": "Crane operations involve fall hazards for riggers and signal persons. "
                       "Work at height on crane components requires fall arrest per 1926.502.",
    },
]


def detect_safety_categories(query_text: str, keywords: List[str]) -> List[SafetyIssueCategory]:
    """Detect which safety issue categories are implicated by a query.

    Args:
        query_text: The normalized query text.
        keywords: Extracted keywords from normalization.

    Returns:
        List of detected SafetyIssueCategory values.
    """
    text_lower = query_text.lower()
    keyword_set = {k.lower() for k in keywords}
    detected = []

    category_indicators = {
        SafetyIssueCategory.H2S_SAFETY: ["hydrogen sulfide", "h2s", "sour gas", "z390", "scba"],
        SafetyIssueCategory.BOP_WELL_CONTROL: ["blowout preventer", "bop", "well control", "kick", "blowout", "api spec 53"],
        SafetyIssueCategory.PSM: ["process safety management", "psm", "1910.119", "pha", "hazop", "management of change"],
        SafetyIssueCategory.RMP: ["risk management plan", "rmp", "40 cfr part 68", "offsite consequence"],
        SafetyIssueCategory.CONFINED_SPACE: ["confined space", "permit-required", "1910.146", "tank entry", "vessel entry"],
        SafetyIssueCategory.FALL_PROTECTION: ["fall protection", "fall arrest", "guardrail", "safety harness", "working at heights", "1910.28", "1926.501"],
        SafetyIssueCategory.PPE: ["ppe", "personal protective equipment", "hard hat", "safety glasses", "steel toe", "frc", "fire resistant"],
        SafetyIssueCategory.LOCKOUT_TAGOUT: ["lockout", "tagout", "loto", "1910.147", "energy isolation"],
        SafetyIssueCategory.ELECTRICAL_SAFETY: ["electrical", "arc flash", "nfpa 70e", "gfci", "energized work"],
        SafetyIssueCategory.HOT_WORK: ["hot work", "welding", "cutting", "brazing", "fire watch", "nfpa 51b"],
        SafetyIssueCategory.RESPIRATORY_PROTECTION: ["respiratory", "respirator", "1910.134", "scba", "air purifying", "fit test"],
        SafetyIssueCategory.FIRE_PREVENTION: ["fire prevention", "fire extinguisher", "fire suppression", "flammable", "combustible"],
        SafetyIssueCategory.HAZCOM: ["hazard communication", "hazcom", "1910.1200", "sds", "safety data sheet", "ghs", "chemical labeling"],
        SafetyIssueCategory.BSEE_OFFSHORE: ["bsee", "offshore", "outer continental shelf", "30 cfr 250", "sems"],
        SafetyIssueCategory.ENVIRONMENTAL_COMPLIANCE: ["environmental", "epa", "spill prevention", "opa 90", "clean water", "stormwater"],
        SafetyIssueCategory.OSHA_GENERAL_INDUSTRY: ["general industry", "1910", "osha general"],
        SafetyIssueCategory.OSHA_CONSTRUCTION: ["construction", "1926", "subpart"],
        SafetyIssueCategory.TRANSPORTATION_SAFETY: ["transportation", "dot", "hazmat transport", "placarding"],
        SafetyIssueCategory.CRANE_RIGGING: ["crane", "rigging", "lifting", "sling", "1926.1400"],
        SafetyIssueCategory.EXCAVATION_TRENCHING: ["excavation", "trenching", "shoring", "benching", "1926 subpart p"],
    }

    for category, indicators in category_indicators.items():
        for indicator in indicators:
            if indicator in text_lower or indicator in keyword_set:
                detected.append(category)
                break

    return detected


def get_interaction_edges_for_categories(categories: List[SafetyIssueCategory]) -> List[Dict[str, Any]]:
    """Get interaction edges relevant to the detected categories.

    Args:
        categories: List of detected safety issue categories.

    Returns:
        List of relevant interaction edge definitions.
    """
    cat_set = set(categories)
    relevant = []
    for edge in INTERACTION_EDGES:
        if edge["from"] in cat_set or edge["to"] in cat_set:
            relevant.append(edge)
    return relevant


def decompose_multi_doctrine(query_text: str, doctrines: List[DoctrineBlock],
                             categories: List[SafetyIssueCategory]) -> Dict[str, Any]:
    """Decompose a query that spans multiple safety doctrines.

    Args:
        query_text: The normalized query text.
        doctrines: Matched doctrine blocks.
        categories: Detected safety issue categories.

    Returns:
        Decomposition with strata, interactions, and resolution strategy.
    """
    strata = []
    for doctrine in doctrines:
        stratum = {
            "topic": doctrine.topic,
            "confidence": doctrine.confidence,
            "burden_holder": doctrine.burden_holder,
            "adversary_position": doctrine.adversary_position,
            "authorities": doctrine.primary_authority,
            "stratification": doctrine.confidence_stratification.value,
        }
        strata.append(stratum)

    edges = get_interaction_edges_for_categories(categories)

    resolution_steps = []
    for edge in edges:
        if edge["relationship"] == "requires":
            resolution_steps.append(f"MANDATORY: {edge['from'].value} triggers {edge['to'].value} requirement")
        elif edge["relationship"] == "compound_hazard":
            resolution_steps.append(f"COMPOUND HAZARD: {edge['from'].value} + {edge['to'].value} -- both must be addressed simultaneously")
        elif edge["relationship"] == "concurrent":
            resolution_steps.append(f"CONCURRENT: {edge['from'].value} and {edge['to'].value} apply independently -- compliance with one does not satisfy the other")

    return {
        "categories_detected": [c.value for c in categories],
        "doctrine_strata": strata,
        "interaction_edges": [
            {"from": e["from"].value, "to": e["to"].value,
             "relationship": e["relationship"], "description": e["description"]}
            for e in edges
        ],
        "resolution_steps": resolution_steps,
        "compound_risk": len(edges) > 2,
    }


# =============================================================================
# [TIE-09] DRIFT WATCHER
# =============================================================================

class DriftWatcher:
    """Monitor doctrine drift over time by tracking query patterns and matches."""

    def __init__(self):
        self._observations: List[Dict[str, Any]] = []
        self._max_observations = 5000
        self._drift_threshold = 0.15

    def observe(self, query_text: str, matched_topics: List[str],
                confidence: float, layer: str) -> None:
        """Record a query observation for drift analysis.

        Args:
            query_text: The query text.
            matched_topics: Topics matched from doctrine cache.
            confidence: Overall confidence of the response.
            layer: Response layer used (doctrine/retrieval/deep_analysis).
        """
        observation = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_hash": hashlib.sha256(query_text.encode()).hexdigest()[:12],
            "matched_topics": matched_topics,
            "confidence": confidence,
            "layer": layer,
            "topic_count": len(matched_topics),
        }
        self._observations.append(observation)
        if len(self._observations) > self._max_observations:
            self._observations = self._observations[-self._max_observations:]

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate a drift analysis report.

        Returns:
            Dict with drift metrics, coverage gaps, and recommendations.
        """
        if len(self._observations) < 10:
            return {
                "status": "insufficient_data",
                "observations": len(self._observations),
                "minimum_required": 10,
            }

        total = len(self._observations)
        doctrine_hits = sum(1 for o in self._observations if o["layer"] == "doctrine")
        retrieval_hits = sum(1 for o in self._observations if o["layer"] == "retrieval")
        deep_analysis = sum(1 for o in self._observations if o["layer"] == "deep_analysis")

        doctrine_rate = doctrine_hits / total if total else 0.0
        miss_rate = (retrieval_hits + deep_analysis) / total if total else 0.0

        # Topic frequency analysis
        topic_freq: Dict[str, int] = {}
        for obs in self._observations:
            for topic in obs["matched_topics"]:
                topic_freq[topic] = topic_freq.get(topic, 0) + 1

        unmatched_rate = deep_analysis / total if total else 0.0

        # Average confidence over time windows
        recent = self._observations[-50:] if len(self._observations) >= 50 else self._observations
        older = self._observations[:50] if len(self._observations) >= 100 else []

        recent_conf = sum(o["confidence"] for o in recent) / len(recent) if recent else 0.0
        older_conf = sum(o["confidence"] for o in older) / len(older) if older else recent_conf

        confidence_drift = recent_conf - older_conf

        drifting = abs(confidence_drift) > self._drift_threshold or miss_rate > 0.30

        return {
            "status": "drift_detected" if drifting else "stable",
            "observations": total,
            "doctrine_hit_rate": round(doctrine_rate, 3),
            "retrieval_rate": round(retrieval_hits / total, 3) if total else 0.0,
            "deep_analysis_rate": round(unmatched_rate, 3),
            "confidence_drift": round(confidence_drift, 4),
            "recent_avg_confidence": round(recent_conf, 3),
            "topic_frequency": dict(sorted(topic_freq.items(), key=lambda x: x[1], reverse=True)[:20]),
            "recommendations": self._generate_recommendations(doctrine_rate, miss_rate, confidence_drift, topic_freq),
        }

    def _generate_recommendations(self, doctrine_rate: float, miss_rate: float,
                                   confidence_drift: float, topic_freq: Dict[str, int]) -> List[str]:
        """Generate drift mitigation recommendations."""
        recs = []
        if doctrine_rate < 0.60:
            recs.append("Doctrine cache hit rate below 60% -- consider adding more doctrine blocks for frequently queried topics.")
        if miss_rate > 0.30:
            recs.append("Over 30% of queries fall through to deep analysis -- review coverage gaps.")
        if confidence_drift < -0.10:
            recs.append(f"Confidence declining ({confidence_drift:.3f}) -- possible regulatory changes not reflected in doctrines.")
        if confidence_drift > 0.10:
            recs.append(f"Confidence increasing ({confidence_drift:.3f}) -- doctrines may be overfitting to narrow query patterns.")
        if not topic_freq:
            recs.append("No topic frequency data -- system may need more query volume for meaningful drift analysis.")
        return recs if recs else ["No drift concerns detected. Doctrine cache is stable."]


_drift_watcher = DriftWatcher()


# =============================================================================
# [TIE-10] COVERAGE MAP
# =============================================================================

class CoverageMap:
    """Track which doctrines have been triggered and identify epistemic gaps."""

    def __init__(self, doctrine_topics: List[str]):
        self._all_topics = set(doctrine_topics)
        self._triggered: Dict[str, int] = {t: 0 for t in doctrine_topics}
        self._gap_queries: List[Dict[str, Any]] = []
        self._max_gap_queries = 500

    def record_trigger(self, topic: str) -> None:
        """Record that a doctrine was triggered by a query.

        Args:
            topic: The doctrine topic that matched.
        """
        if topic in self._triggered:
            self._triggered[topic] += 1
        else:
            self._triggered[topic] = 1
            self._all_topics.add(topic)

    def record_gap(self, query_text: str, keywords: List[str]) -> None:
        """Record a query that found no doctrine match (epistemic gap).

        Args:
            query_text: The query that had no match.
            keywords: Keywords extracted from the query.
        """
        gap = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_hash": hashlib.sha256(query_text.encode()).hexdigest()[:12],
            "keywords": keywords[:10],
            "query_preview": query_text[:200],
        }
        self._gap_queries.append(gap)
        if len(self._gap_queries) > self._max_gap_queries:
            self._gap_queries = self._gap_queries[-self._max_gap_queries:]

    def get_report(self) -> Dict[str, Any]:
        """Generate coverage report.

        Returns:
            Dict with triggered topics, untriggered topics, and gap analysis.
        """
        triggered = {t: c for t, c in self._triggered.items() if c > 0}
        untriggered = [t for t, c in self._triggered.items() if c == 0]
        total_triggers = sum(self._triggered.values())
        coverage_pct = (len(triggered) / len(self._all_topics) * 100) if self._all_topics else 0.0

        # Gap keyword frequency
        gap_keyword_freq: Dict[str, int] = {}
        for gap in self._gap_queries:
            for kw in gap["keywords"]:
                gap_keyword_freq[kw] = gap_keyword_freq.get(kw, 0) + 1

        return {
            "total_doctrines": len(self._all_topics),
            "triggered_count": len(triggered),
            "untriggered_count": len(untriggered),
            "coverage_percentage": round(coverage_pct, 1),
            "total_trigger_events": total_triggers,
            "triggered_topics": dict(sorted(triggered.items(), key=lambda x: x[1], reverse=True)),
            "untriggered_topics": untriggered,
            "gap_queries_recorded": len(self._gap_queries),
            "gap_keyword_frequency": dict(sorted(gap_keyword_freq.items(), key=lambda x: x[1], reverse=True)[:20]),
            "recent_gaps": self._gap_queries[-10:],
        }


_coverage_map = CoverageMap([d.topic for d in DOCTRINE_CACHE])


# =============================================================================
# [TIE-11] METRICS COLLECTOR
# =============================================================================

class MetricsCollector:
    """Lightweight operational metrics. No external dependencies."""

    def __init__(self):
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._lock_latencies = 200
        self.total_queries: int = 0
        self.layer_counts: Dict[str, int] = {"doctrine": 0, "retrieval": 0, "deep_analysis": 0}
        self.category_counts: Dict[str, int] = {}

    def record_query(self, latency_ms: float, doctrine_hit: bool, layer: str = "doctrine") -> None:
        """Record a completed query with latency and outcome.

        Args:
            latency_ms: Query processing time in milliseconds.
            doctrine_hit: Whether the doctrine cache was hit.
            layer: Response layer used.
        """
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._lock_latencies:
            self.latencies.pop(0)
        self.queries.append(now)
        cutoff = now - 3600
        self.queries = [t for t in self.queries if t > cutoff]
        self.total_queries += 1
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1
        self.layer_counts[layer] = self.layer_counts.get(layer, 0) + 1

    def record_error(self, error_msg: str) -> None:
        """Record an error occurrence.

        Args:
            error_msg: Error message string.
        """
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        cutoff = time.time() - 86400
        self.errors = [t for t in self.errors if t > cutoff]

    def record_category(self, category: str) -> None:
        """Record a detected safety category.

        Args:
            category: Safety issue category name.
        """
        self.category_counts[category] = self.category_counts.get(category, 0) + 1

    def query_start(self) -> None:
        """Mark the start of a query."""
        self.active_queries += 1

    def query_end(self) -> None:
        """Mark the end of a query."""
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        """Get latency statistics.

        Returns:
            Dict with avg, p50, p95, p99, min, max latency in ms.
        """
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)
        return {
            "avg_ms": round(sum(sorted_lat) / n, 2),
            "p50_ms": round(sorted_lat[int(n * 0.50)], 2),
            "p95_ms": round(sorted_lat[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(sorted_lat[min(int(n * 0.99), n - 1)], 2),
            "min_ms": round(sorted_lat[0], 2),
            "max_ms": round(sorted_lat[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics.

        Returns:
            Dict with error counts and last error info.
        """
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        """Get doctrine cache hit rate.

        Returns:
            Float between 0.0 and 1.0 representing hit rate.
        """
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / total, 3) if total > 0 else 1.0

    def queries_last_hour(self) -> int:
        """Get query count in the last hour.

        Returns:
            Integer count of queries in the last 3600 seconds.
        """
        return sum(1 for t in self.queries if t > time.time() - 3600)

    def get_full_report(self) -> Dict[str, Any]:
        """Get complete metrics report.

        Returns:
            Dict with all metrics data.
        """
        return {
            "total_queries": self.total_queries,
            "active_queries": self.active_queries,
            "queries_last_hour": self.queries_last_hour(),
            "latency": self.get_latency_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "errors": self.get_error_stats(),
            "layer_distribution": self.layer_counts,
            "category_distribution": dict(sorted(self.category_counts.items(), key=lambda x: x[1], reverse=True)),
        }


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _metrics


# =============================================================================
# [TIE-13] ZONED ANALYSIS
# =============================================================================

class AnalysisZone(str, Enum):
    """Position zones -- never blur planning, reporting, and audit."""
    PLANNING = "planning"
    REPORTING = "reporting"
    AUDIT = "audit"


def detect_analysis_zone(query_text: str) -> AnalysisZone:
    """Detect which analysis zone a query falls into.

    PLANNING: Forward-looking compliance design and hazard assessment.
    REPORTING: Current-state compliance status and required filings.
    AUDIT: Historical review, violation analysis, penalty assessment.

    Args:
        query_text: The normalized query text.

    Returns:
        The detected AnalysisZone.
    """
    text_lower = query_text.lower()

    audit_signals = [
        "audit", "violation", "citation", "penalty", "fine", "investigation",
        "incident", "fatality", "willful", "repeat violation", "abatement",
        "settlement", "consent order", "enforcement", "noncompliance",
        "deficiency", "corrective action", "root cause", "lessons learned",
    ]
    for signal in audit_signals:
        if signal in text_lower:
            return AnalysisZone.AUDIT

    planning_signals = [
        "plan", "design", "implement", "develop", "create", "establish",
        "new facility", "new operation", "startup", "pre-startup", "hazard assessment",
        "risk assessment", "what do i need", "requirements for", "how to comply",
        "steps to", "checklist", "program development", "setting up",
    ]
    for signal in planning_signals:
        if signal in text_lower:
            return AnalysisZone.PLANNING

    return AnalysisZone.REPORTING


def apply_zone_framing(zone: AnalysisZone, conclusion: str, reasoning: str) -> Dict[str, str]:
    """Apply zone-appropriate framing to response content.

    Args:
        zone: The detected analysis zone.
        conclusion: Raw conclusion text.
        reasoning: Raw reasoning text.

    Returns:
        Dict with zone-framed conclusion and reasoning.
    """
    zone_prefixes = {
        AnalysisZone.PLANNING: {
            "conclusion_prefix": "COMPLIANCE PLANNING: ",
            "reasoning_prefix": "Planning analysis: ",
            "caveat": "This planning guidance identifies applicable requirements. Verify current regulatory status before implementation.",
        },
        AnalysisZone.REPORTING: {
            "conclusion_prefix": "COMPLIANCE STATUS: ",
            "reasoning_prefix": "Regulatory analysis: ",
            "caveat": "This analysis reflects current regulatory requirements. Confirm deadlines and filing requirements with the relevant agency.",
        },
        AnalysisZone.AUDIT: {
            "conclusion_prefix": "AUDIT FINDING: ",
            "reasoning_prefix": "Enforcement analysis: ",
            "caveat": "This audit analysis examines compliance history. Penalty amounts reflect current OSHA/BSEE rates and may vary by specific circumstances.",
        },
    }

    framing = zone_prefixes[zone]
    return {
        "conclusion": framing["conclusion_prefix"] + conclusion,
        "reasoning": framing["reasoning_prefix"] + reasoning,
        "zone": zone.value,
        "caveat": framing["caveat"],
    }


# =============================================================================
# [TIE-14] FACT FRAGILITY SCORING
# =============================================================================

def score_fact_fragility(doctrine: DoctrineBlock, zone: AnalysisZone) -> Dict[str, Any]:
    """Score the fragility of facts in a doctrine response.

    Fragility dimensions:
    - Verifiability: Can the conclusion be independently verified?
    - Regulatory stability: How likely is the regulation to change?
    - Testimony dependence: Does the conclusion depend on factual testimony?
    - Recharacterization risk: Could the situation be reframed to a different conclusion?

    Args:
        doctrine: The matched doctrine block.
        zone: The analysis zone.

    Returns:
        Dict with fragility scores and risk assessment.
    """
    # Verifiability: mandatory regulations are highly verifiable
    verifiability = 0.95 if doctrine.confidence_stratification == ConfidenceStratification.MANDATORY else (
        0.80 if doctrine.confidence_stratification == ConfidenceStratification.CLEARLY_REQUIRED else 0.60
    )

    # Regulatory stability: OSHA standards are relatively stable, BSEE changes more
    stability = 0.90
    for auth in doctrine.primary_authority:
        auth_lower = auth.lower()
        if "30 cfr" in auth_lower:
            stability = min(stability, 0.75)  # BSEE regs change more often
        if "ansi" in auth_lower or "api" in auth_lower:
            stability = min(stability, 0.80)  # Standards update on revision cycles
        if "tac" in auth_lower:
            stability = min(stability, 0.82)  # State regs can change with political shifts

    # Testimony dependence: safety cases rarely depend on testimony alone
    testimony_dependence = 0.15  # Low for regulatory compliance (regulation is the fact)
    if zone == AnalysisZone.AUDIT:
        testimony_dependence = 0.35  # Audit cases may involve factual disputes

    # Recharacterization risk: could OSHA recharacterize the violation?
    rechar_risk = 0.10 if doctrine.confidence_stratification == ConfidenceStratification.MANDATORY else (
        0.25 if doctrine.confidence_stratification == ConfidenceStratification.CLEARLY_REQUIRED else 0.40
    )

    # Aggregate fragility (lower = more robust)
    fragility_score = 1.0 - (
        verifiability * 0.35 +
        stability * 0.25 +
        (1.0 - testimony_dependence) * 0.20 +
        (1.0 - rechar_risk) * 0.20
    )

    risk_level = "low" if fragility_score < 0.20 else ("moderate" if fragility_score < 0.40 else "high")

    return {
        "fragility_score": round(fragility_score, 3),
        "risk_level": risk_level,
        "verifiability": round(verifiability, 3),
        "regulatory_stability": round(stability, 3),
        "testimony_dependence": round(testimony_dependence, 3),
        "recharacterization_risk": round(rechar_risk, 3),
        "assessment": f"Fragility {risk_level}: Conclusion is {'well-supported by regulatory text' if risk_level == 'low' else 'moderately dependent on interpretation' if risk_level == 'moderate' else 'subject to factual dispute or regulatory change'}.",
    }


# =============================================================================
# [TIE-15] AUDIT TRAIL -- JSONL
# =============================================================================

def write_audit_entry(trace_id: str, query: str, response_layer: str,
                      doctrine_match: bool, confidence_tier: str,
                      categories: List[str], latency_ms: float,
                      determinism_hash: str, zone: str,
                      error: Optional[str] = None) -> None:
    """Write an audit entry to the JSONL audit trail.

    Args:
        trace_id: Unique query trace identifier.
        query: The original query text.
        response_layer: Which layer produced the response.
        doctrine_match: Whether a doctrine was matched.
        confidence_tier: Confidence classification.
        categories: Detected safety issue categories.
        latency_ms: Processing time in milliseconds.
        determinism_hash: SHA-256 determinism hash.
        zone: Analysis zone (planning/reporting/audit).
        error: Optional error message.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace_id": trace_id,
        "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
        "query_preview": query[:100],
        "response_layer": response_layer,
        "doctrine_match": doctrine_match,
        "confidence_tier": confidence_tier,
        "categories": categories,
        "latency_ms": round(latency_ms, 2),
        "determinism_hash": determinism_hash,
        "zone": zone,
        "error": error,
        "engine_version": ENGINE_VERSION,
    }
    try:
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.error(f"Failed to write audit entry: {exc}")


# =============================================================================
# [TIE-16] DETERMINISM HASH (SHA-256)
# =============================================================================

def compute_determinism_hash(query: str, doctrine_topics: List[str],
                              confidence: float, layer: str, zone: str) -> str:
    """Compute SHA-256 determinism hash for response reproducibility.

    Given the same inputs, the hash must be identical. This enables
    regression testing and audit verification.

    Args:
        query: Original query text.
        doctrine_topics: Matched doctrine topic names.
        confidence: Response confidence score.
        layer: Response layer used.
        zone: Analysis zone.

    Returns:
        16-character hex prefix of SHA-256 hash.
    """
    hash_input = "|".join([
        query.strip().lower(),
        ",".join(sorted(doctrine_topics)),
        f"{confidence:.4f}",
        layer,
        zone,
        ENGINE_VERSION,
    ])
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16]


# =============================================================================
# [TIE-18] LOGURU LOGGING -- Epistemic Guardrails
# =============================================================================

def apply_epistemic_guardrails(text: str) -> str:
    """Strip banned phrases and apply epistemic discipline to output text.

    Safety compliance responses must be authoritative. No hedging,
    no AI self-references, no vague qualifiers.

    Args:
        text: Response text to cleanse.

    Returns:
        Cleansed text with banned phrases removed.
    """
    result = text
    for phrase in BANNED_PHRASES:
        if phrase.lower() in result.lower():
            idx = result.lower().index(phrase.lower())
            # Remove the sentence containing the banned phrase
            start = result.rfind(".", 0, idx) + 1
            end = result.find(".", idx)
            if end == -1:
                end = len(result)
            else:
                end += 1
            result = result[:start].rstrip() + " " + result[end:].lstrip()
    return result.strip()


# =============================================================================
# PYDANTIC MODELS -- Request / Response
# =============================================================================

class ResponseMode(str, Enum):
    """Response verbosity modes."""
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class Complexity(str, Enum):
    """Query complexity classification."""
    STANDARD = "standard"
    ADVANCED = "advanced"


class SafetyQuery(BaseModel):
    """Incoming safety compliance query."""
    question: str = Field(..., min_length=10, description="Safety compliance question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    jurisdiction: str = Field(default="Federal", description="Regulatory jurisdiction")
    complexity: Complexity = Field(default=Complexity.STANDARD, description="Query complexity")
    include_trace: bool = Field(default=False, description="Include telemetry trace")
    include_fragility: bool = Field(default=False, description="Include fact fragility scores")
    include_decomposition: bool = Field(default=False, description="Include multi-doctrine decomposition")


class Citation(BaseModel):
    """Regulatory citation with authority classification."""
    authority: str
    reference: str
    relevance: str
    weight: float = Field(default=0.5, description="Authority weight 0-1")
    level: str = Field(default="unknown", description="Authority level classification")


class SafetyResponse(BaseModel):
    """Complete safety compliance response."""
    query_id: str
    question: str
    mode: ResponseMode
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    safety_requirements: Optional[List[str]] = None
    compliance_deadlines: Optional[List[str]] = None
    penalties_for_violation: Optional[str] = None
    responsible_agencies: Optional[List[str]] = None
    doctrine_match: bool
    confidence_tier: str
    confidence_stratification: Optional[str] = None
    response_layer: Literal["doctrine", "retrieval", "deep_analysis"]
    analysis_zone: str = "reporting"
    categories_detected: List[str] = Field(default_factory=list)
    interaction_edges: Optional[List[Dict[str, str]]] = None
    authority_hierarchy: Optional[List[Dict[str, Any]]] = None
    fragility: Optional[Dict[str, Any]] = None
    decomposition: Optional[Dict[str, Any]] = None
    disclosure_caveat: Optional[str] = None
    latency_ms: float
    determinism_hash: Optional[str] = None
    limitations: List[str] = Field(default_factory=list)
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """Comprehensive health check response."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    version: str
    domain: str
    port: int
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    coverage: Dict[str, Any]
    drift_status: str
    active_queries: int
    queries_last_hour: int
    total_queries: int
    error_rate: Dict[str, Any]
    layer_distribution: Dict[str, int]
    cloud_retriever: bool
    telemetry_summary: Dict[str, Any]


# =============================================================================
# [TIE-01] THREE-LAYER RESPONSE ENGINE
# =============================================================================

def three_layer_response(query: SafetyQuery, normalized: NormalizationResult,
                         trace_id: str) -> SafetyResponse:
    """Execute three-layer response: doctrine cache -> semantic retrieval -> deep analysis.

    Layer 1 (0-200ms): Check doctrine cache for pre-compiled expert reasoning.
    Layer 2 (200-700ms): Fall back to vector/semantic search.
    Layer 3 (on-demand): Deep analysis with multi-source synthesis.

    Args:
        query: The incoming safety query.
        normalized: Semantic normalization result.
        trace_id: Telemetry trace identifier.

    Returns:
        SafetyResponse with complete safety compliance analysis.
    """
    start_time = time.time()
    metrics = get_metrics()
    metrics.query_start()

    # Apply safety-specific normalization
    safety_normalized_text = normalize_safety_terms(normalized.normalized_text)
    all_keywords = list(set(normalized.keywords))

    # Detect safety categories
    categories = detect_safety_categories(safety_normalized_text, all_keywords)
    for cat in categories:
        metrics.record_category(cat.value)

    # Detect analysis zone
    zone = detect_analysis_zone(safety_normalized_text)

    try:
        # LAYER 1: Doctrine Cache
        matched_doctrines = match_doctrines(safety_normalized_text, all_keywords)
        if matched_doctrines:
            logger.info(f"[{trace_id}] Layer 1 HIT: {len(matched_doctrines)} doctrines matched")
            response = _build_doctrine_response(
                query, matched_doctrines, normalized, trace_id, start_time,
                categories, zone, safety_normalized_text, all_keywords,
            )
            latency = (time.time() - start_time) * 1000
            metrics.record_query(latency, True, "doctrine")
            metrics.query_end()

            for d in matched_doctrines:
                _coverage_map.record_trigger(d.topic)
            _drift_watcher.observe(
                query.question, [d.topic for d in matched_doctrines],
                matched_doctrines[0].confidence, "doctrine",
            )
            return response

        # LAYER 2: Semantic / Vector Retrieval
        logger.info(f"[{trace_id}] Layer 1 MISS -> Layer 2 semantic retrieval")
        search_results = vector_search(safety_normalized_text, top_k=5)

        if CLOUD_RETRIEVER_AVAILABLE:
            try:
                cloud_results = cloud_retrieve(safety_normalized_text, top_k=3)
                if cloud_results:
                    search_results.extend([
                        {"content": cr.content, "score": cr.score, "source": cr.source}
                        for cr in cloud_results
                    ])
            except Exception as cloud_err:
                logger.warning(f"[{trace_id}] Cloud retriever error: {cloud_err}")

        if search_results:
            logger.info(f"[{trace_id}] Layer 2 HIT: {len(search_results)} results")
            response = _build_retrieval_response(
                query, search_results, normalized, trace_id, start_time,
                categories, zone, all_keywords,
            )
            latency = (time.time() - start_time) * 1000
            metrics.record_query(latency, False, "retrieval")
            metrics.query_end()
            _coverage_map.record_gap(query.question, all_keywords)
            _drift_watcher.observe(query.question, [], 0.5, "retrieval")
            return response

        # LAYER 3: Deep Analysis
        logger.info(f"[{trace_id}] Layer 2 MISS -> Layer 3 deep analysis")
        response = _build_deep_analysis_response(
            query, normalized, trace_id, start_time,
            categories, zone, safety_normalized_text, all_keywords,
        )
        latency = (time.time() - start_time) * 1000
        metrics.record_query(latency, False, "deep_analysis")
        metrics.query_end()
        _coverage_map.record_gap(query.question, all_keywords)
        _drift_watcher.observe(query.question, [], 0.3, "deep_analysis")
        return response

    except Exception as exc:
        latency = (time.time() - start_time) * 1000
        metrics.record_error(str(exc))
        metrics.query_end()
        log_error(trace_id, ErrorDomain.QUERY_PROCESSING, str(exc))
        write_audit_entry(
            trace_id, query.question, "error", False, "error",
            [c.value for c in categories], latency, "", zone.value, str(exc),
        )
        raise


# =============================================================================
# [TIE-02] RESPONSE MODE BUILDERS
# =============================================================================

def _format_by_mode(mode: ResponseMode, conclusion: str, reasoning: str,
                    key_factors: List[str], citations: List[Citation],
                    doctrine: Optional[DoctrineBlock] = None) -> Dict[str, Any]:
    """Format response content according to the requested mode.

    FAST: Concise conclusion with top citations. Sub-2 second target.
    DEFENSE: Structured reasoning with burden analysis and adversary positions.
    MEMO: Full regulatory memorandum with comprehensive citation chain.

    Args:
        mode: The requested response mode.
        conclusion: Raw conclusion text.
        reasoning: Raw reasoning text.
        key_factors: List of key compliance factors.
        citations: List of regulatory citations.
        doctrine: Optional doctrine block for extended content.

    Returns:
        Dict with mode-formatted conclusion, reasoning, key_factors, and citations.
    """
    if mode == ResponseMode.FAST:
        return {
            "conclusion": conclusion,
            "reasoning": reasoning[:500] if len(reasoning) > 500 else reasoning,
            "key_factors": key_factors[:5],
            "citations": citations[:3],
        }

    if mode == ResponseMode.DEFENSE:
        defense_reasoning = reasoning
        if doctrine:
            defense_reasoning += (
                f"\n\nBURDEN ANALYSIS: The burden of compliance falls on the {doctrine.burden_holder}. "
                f"The adversary position ({doctrine.adversary_position}) may pursue enforcement "
                f"through inspection, citation, or investigation. "
                f"\n\nADVERSARY POSITION: {doctrine.adversary_position} enforcement focus: "
                + "; ".join(doctrine.counter_arguments[:3])
                + f"\n\nRESOLUTION STRATEGY: {doctrine.resolution_strategy}"
            )
        return {
            "conclusion": conclusion,
            "reasoning": defense_reasoning,
            "key_factors": key_factors,
            "citations": citations,
        }

    # MEMO mode: full regulatory memorandum
    memo_conclusion = f"SAFETY COMPLIANCE MEMORANDUM\n{'='*40}\n\n{conclusion}"
    memo_reasoning = reasoning
    if doctrine:
        memo_reasoning += (
            f"\n\n{'='*40}\nDETAILED REGULATORY ANALYSIS\n{'='*40}\n\n"
            f"Topic: {doctrine.topic}\n"
            f"Controlling Precedent: {doctrine.controlling_precedent or 'N/A'}\n"
            f"Confidence: {doctrine.confidence:.2%}\n"
            f"Stratification: {doctrine.confidence_stratification.value}\n"
            f"Burden Holder: {doctrine.burden_holder}\n"
            f"Adversary: {doctrine.adversary_position}\n\n"
            f"COUNTER-ARGUMENTS AND RISK FACTORS:\n"
            + "\n".join(f"  - {ca}" for ca in doctrine.counter_arguments)
            + f"\n\nRESOLUTION STRATEGY:\n  {doctrine.resolution_strategy}\n"
            f"\nENTITY SCOPE: {', '.join(doctrine.entity_scope)}\n"
            f"\nPENALTY EXPOSURE:\n"
            f"  - OSHA Serious: ${OSHA_PENALTY_SERIOUS:,} per violation\n"
            f"  - OSHA Willful: ${OSHA_PENALTY_WILLFUL:,} per violation\n"
            f"  - OSHA Repeat: ${OSHA_PENALTY_REPEAT:,} per violation\n"
            f"  - OSHA Failure to Abate: ${OSHA_PENALTY_FAILURE_TO_ABATE:,}/day\n"
            f"  - BSEE: ${BSEE_PENALTY_PER_DAY:,}/day per violation\n"
            f"  - EPA RMP: ${EPA_RMP_PENALTY:,}/day per violation\n"
        )
    return {
        "conclusion": memo_conclusion,
        "reasoning": memo_reasoning,
        "key_factors": key_factors,
        "citations": citations,
    }


def _build_doctrine_response(query: SafetyQuery, doctrines: List[DoctrineBlock],
                              normalized: NormalizationResult, trace_id: str,
                              start_time: float, categories: List[SafetyIssueCategory],
                              zone: AnalysisZone, safety_text: str,
                              keywords: List[str]) -> SafetyResponse:
    """Build response from doctrine cache match (Layer 1).

    Args:
        query: Original query.
        doctrines: Matched doctrine blocks.
        normalized: Normalization result.
        trace_id: Trace identifier.
        start_time: Query start timestamp.
        categories: Detected safety categories.
        zone: Detected analysis zone.
        safety_text: Safety-normalized query text.
        keywords: Extracted keywords.

    Returns:
        Complete SafetyResponse.
    """
    primary = doctrines[0]

    # Build conclusion from template
    conclusion = primary.conclusion_template
    if "{jurisdiction}" in conclusion:
        conclusion = conclusion.format(jurisdiction=query.jurisdiction)

    reasoning = primary.reasoning_framework
    key_factors = list(primary.key_factors)

    # Build citations with authority weights
    citations = []
    for auth in primary.primary_authority:
        level = classify_authority(auth)
        weight = get_authority_weight(auth)
        citations.append(Citation(
            authority=auth.split(":")[0] if ":" in auth else auth.split("(")[0].strip(),
            reference=auth,
            relevance="Primary controlling authority",
            weight=weight,
            level=level.value,
        ))

    # Secondary doctrine citations
    for secondary in doctrines[1:3]:
        for auth in secondary.primary_authority[:1]:
            level = classify_authority(auth)
            weight = get_authority_weight(auth)
            citations.append(Citation(
                authority=auth.split(":")[0] if ":" in auth else auth.split("(")[0].strip(),
                reference=auth,
                relevance="Supporting authority",
                weight=weight,
                level=level.value,
            ))

    # Authority conflict resolution
    all_authorities = []
    for d in doctrines:
        all_authorities.extend(d.primary_authority)
    authority_resolution = resolve_authority_conflict(all_authorities)

    # Confidence stratification
    conf_tier = classify_confidence(
        primary.confidence,
        primary.controlling_precedent is not None,
        primary.confidence_stratification,
    )

    # Zone framing
    zone_framing = apply_zone_framing(zone, conclusion, reasoning)

    # Apply mode formatting
    formatted = _format_by_mode(query.mode, zone_framing["conclusion"],
                                 zone_framing["reasoning"], key_factors, citations, primary)

    # Safety requirements extraction
    safety_reqs = [f for f in primary.key_factors if any(
        kw in f.lower() for kw in ["required", "must", "shall", "mandatory"]
    )]

    # Penalty string
    penalties = (
        f"OSHA Serious: ${OSHA_PENALTY_SERIOUS:,}/violation; "
        f"Willful: ${OSHA_PENALTY_WILLFUL:,}/violation; "
        f"BSEE: ${BSEE_PENALTY_PER_DAY:,}/day"
    )

    # Responsible agencies
    agencies = set()
    for auth in all_authorities:
        auth_lower = auth.lower()
        if "29 cfr" in auth_lower or "osha" in auth_lower:
            agencies.add("OSHA")
        if "30 cfr" in auth_lower or "bsee" in auth_lower:
            agencies.add("BSEE")
        if "40 cfr" in auth_lower or "epa" in auth_lower:
            agencies.add("EPA")
        if "ansi" in auth_lower:
            agencies.add("ANSI")
        if "api" in auth_lower:
            agencies.add("API")
        if "tac" in auth_lower or "rrc" in auth_lower:
            agencies.add("Railroad Commission of Texas")
        if "nfpa" in auth_lower:
            agencies.add("NFPA")

    # Fragility scoring
    fragility = None
    if query.include_fragility:
        fragility = score_fact_fragility(primary, zone)

    # Multi-doctrine decomposition
    decomposition = None
    if query.include_decomposition and len(doctrines) > 1:
        decomposition = decompose_multi_doctrine(safety_text, doctrines, categories)

    # Interaction edges for categories
    edges = get_interaction_edges_for_categories(categories)
    edge_dicts = [
        {"from": e["from"].value, "to": e["to"].value,
         "relationship": e["relationship"], "description": e["description"]}
        for e in edges
    ] if edges else None

    # Epistemic guardrails
    final_conclusion = apply_epistemic_guardrails(formatted["conclusion"])
    final_reasoning = apply_epistemic_guardrails(formatted["reasoning"])

    # Determinism hash
    det_hash = compute_determinism_hash(
        query.question,
        [d.topic for d in doctrines],
        primary.confidence,
        "doctrine",
        zone.value,
    )

    latency_ms = (time.time() - start_time) * 1000

    # Disclosure caveat for non-DEFENSIBLE tiers
    disclosure = None
    if conf_tier != ConfidenceTier.DEFENSIBLE:
        disclosure = (
            f"Confidence tier: {conf_tier.value}. "
            "Verify current regulatory requirements with the applicable agency before relying on this analysis."
        )

    # Audit trail
    write_audit_entry(
        trace_id, query.question, "doctrine", True, conf_tier.value,
        [c.value for c in categories], latency_ms, det_hash, zone.value,
    )

    return SafetyResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=final_conclusion,
        reasoning=final_reasoning,
        key_factors=formatted["key_factors"],
        citations=formatted["citations"],
        safety_requirements=safety_reqs if safety_reqs else None,
        compliance_deadlines=None,
        penalties_for_violation=penalties,
        responsible_agencies=sorted(agencies) if agencies else None,
        doctrine_match=True,
        confidence_tier=conf_tier.value,
        confidence_stratification=primary.confidence_stratification.value,
        response_layer="doctrine",
        analysis_zone=zone.value,
        categories_detected=[c.value for c in categories],
        interaction_edges=edge_dicts,
        authority_hierarchy=authority_resolution.get("hierarchy"),
        fragility=fragility,
        decomposition=decomposition,
        disclosure_caveat=disclosure,
        latency_ms=round(latency_ms, 2),
        determinism_hash=det_hash,
        limitations=[zone_framing["caveat"]],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def _build_retrieval_response(query: SafetyQuery, results: List[Dict[str, Any]],
                               normalized: NormalizationResult, trace_id: str,
                               start_time: float, categories: List[SafetyIssueCategory],
                               zone: AnalysisZone, keywords: List[str]) -> SafetyResponse:
    """Build response from semantic/vector retrieval (Layer 2).

    Args:
        query: Original query.
        results: Vector search results.
        normalized: Normalization result.
        trace_id: Trace identifier.
        start_time: Query start timestamp.
        categories: Detected safety categories.
        zone: Detected analysis zone.
        keywords: Extracted keywords.

    Returns:
        Complete SafetyResponse.
    """
    top_result = results[0]
    content = top_result.get("content", "Safety compliance requirement identified.")
    score = top_result.get("score", 0.0)

    conclusion = f"Based on regulatory database retrieval (relevance {score:.3f}): {content}"
    reasoning = (
        f"Semantic retrieval matched {len(results)} safety provisions from the regulatory database. "
        f"Top match relevance: {score:.3f}. No pre-compiled doctrine was available for this specific query. "
        f"The retrieved content should be verified against current regulatory text."
    )
    key_factors = [
        f"Retrieval matched {len(results)} regulatory provisions",
        f"Top relevance score: {score:.3f}",
        "Verify against current regulatory text",
    ]

    citations = []
    for result in results[:3]:
        source = result.get("source", "Regulatory Database")
        citations.append(Citation(
            authority="Safety Regulation",
            reference=source,
            relevance=f"Retrieval score: {result.get('score', 0.0):.3f}",
            weight=result.get("score", 0.5),
            level="database_retrieval",
        ))

    zone_framing = apply_zone_framing(zone, conclusion, reasoning)
    formatted = _format_by_mode(query.mode, zone_framing["conclusion"],
                                 zone_framing["reasoning"], key_factors, citations)

    det_hash = compute_determinism_hash(query.question, [], score, "retrieval", zone.value)
    latency_ms = (time.time() - start_time) * 1000

    write_audit_entry(
        trace_id, query.question, "retrieval", False, "moderate",
        [c.value for c in categories], latency_ms, det_hash, zone.value,
    )

    return SafetyResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=apply_epistemic_guardrails(formatted["conclusion"]),
        reasoning=apply_epistemic_guardrails(formatted["reasoning"]),
        key_factors=formatted["key_factors"],
        citations=formatted["citations"],
        doctrine_match=False,
        confidence_tier="moderate",
        response_layer="retrieval",
        analysis_zone=zone.value,
        categories_detected=[c.value for c in categories],
        disclosure_caveat="Response based on semantic retrieval, not pre-compiled doctrine. Verify with current regulations.",
        latency_ms=round(latency_ms, 2),
        determinism_hash=det_hash,
        limitations=[zone_framing["caveat"], "Retrieval-based response -- confirm with regulatory authority."],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# =============================================================================
# [TIE-20] DEEP ANALYSIS MODE
# =============================================================================

def _build_deep_analysis_response(query: SafetyQuery, normalized: NormalizationResult,
                                   trace_id: str, start_time: float,
                                   categories: List[SafetyIssueCategory],
                                   zone: AnalysisZone, safety_text: str,
                                   keywords: List[str]) -> SafetyResponse:
    """Build response from deep analysis when both cache and retrieval miss (Layer 3).

    Deep analysis synthesizes from:
    1. Query keyword decomposition and category detection.
    2. Interaction edge analysis for compound hazards.
    3. General regulatory framework knowledge.
    4. Penalty and enforcement pattern analysis.

    Args:
        query: Original query.
        normalized: Normalization result.
        trace_id: Trace identifier.
        start_time: Query start timestamp.
        categories: Detected safety categories.
        zone: Detected analysis zone.
        safety_text: Safety-normalized query text.
        keywords: Extracted keywords.

    Returns:
        Complete SafetyResponse with deep analysis.
    """
    # Build category-based analysis
    category_analyses = []
    for cat in categories:
        category_analyses.append(f"Detected safety domain: {cat.value}")

    edges = get_interaction_edges_for_categories(categories)
    compound_analyses = []
    for edge in edges:
        compound_analyses.append(
            f"INTERACTION: {edge['from'].value} <-> {edge['to'].value} "
            f"({edge['relationship']}): {edge['description']}"
        )

    # Build conclusion based on detected categories
    if categories:
        cat_list = ", ".join(c.value for c in categories[:5])
        conclusion = (
            f"Safety compliance query implicates the following regulatory domains: {cat_list}. "
            f"No pre-compiled doctrine matched this specific query. Consult the applicable "
            f"regulatory standards directly. "
        )
        if any(c in (SafetyIssueCategory.H2S_SAFETY, SafetyIssueCategory.CONFINED_SPACE,
                      SafetyIssueCategory.BOP_WELL_CONTROL, SafetyIssueCategory.PSM)
               for c in categories):
            conclusion += (
                f"CRITICAL: The detected categories include life-safety-critical domains. "
                f"Non-compliance may result in fatalities and penalties up to "
                f"${OSHA_PENALTY_WILLFUL:,} per willful violation."
            )
    else:
        conclusion = (
            "Safety compliance query does not match specific doctrine patterns. "
            "Consult OSHA regulations (29 CFR 1910/1926) and applicable BSEE/EPA standards."
        )

    reasoning = (
        f"Deep analysis performed on query with {len(keywords)} extracted keywords "
        f"across {len(categories)} detected safety domains. "
        + (" ".join(category_analyses) + " " if category_analyses else "")
        + (" ".join(compound_analyses) + " " if compound_analyses else "")
        + f"Jurisdiction: {query.jurisdiction}. "
        f"Analysis zone: {zone.value}. "
        f"No doctrine cache match -- this query may represent a coverage gap "
        f"requiring new doctrine development."
    )

    key_factors = [
        f"Detected {len(categories)} safety domains",
        f"Identified {len(edges)} regulatory interactions",
        f"Jurisdiction: {query.jurisdiction}",
        "No doctrine cache match -- verify with regulatory agency",
    ]
    if edges:
        key_factors.append(f"Compound hazard interactions detected: {len(edges)}")

    citations = [
        Citation(
            authority="OSHA",
            reference="29 CFR 1910/1926" if query.jurisdiction == "Federal" else "State Safety Regulations",
            relevance="Primary safety regulatory framework",
            weight=0.93,
            level="federal_regulation",
        ),
    ]
    if any(c == SafetyIssueCategory.BSEE_OFFSHORE for c in categories):
        citations.append(Citation(
            authority="BSEE",
            reference="30 CFR 250",
            relevance="Offshore safety regulation",
            weight=0.92,
            level="bsee_regulation",
        ))

    zone_framing = apply_zone_framing(zone, conclusion, reasoning)
    formatted = _format_by_mode(query.mode, zone_framing["conclusion"],
                                 zone_framing["reasoning"], key_factors, citations)

    det_hash = compute_determinism_hash(query.question, [], 0.3, "deep_analysis", zone.value)
    latency_ms = (time.time() - start_time) * 1000

    edge_dicts = [
        {"from": e["from"].value, "to": e["to"].value,
         "relationship": e["relationship"], "description": e["description"]}
        for e in edges
    ] if edges else None

    write_audit_entry(
        trace_id, query.question, "deep_analysis", False, "requires_review",
        [c.value for c in categories], latency_ms, det_hash, zone.value,
    )

    return SafetyResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=apply_epistemic_guardrails(formatted["conclusion"]),
        reasoning=apply_epistemic_guardrails(formatted["reasoning"]),
        key_factors=formatted["key_factors"],
        citations=formatted["citations"],
        doctrine_match=False,
        confidence_tier="requires_review",
        response_layer="deep_analysis",
        analysis_zone=zone.value,
        categories_detected=[c.value for c in categories],
        interaction_edges=edge_dicts,
        disclosure_caveat="Deep analysis response -- no doctrine match. Verify all requirements with the applicable regulatory agency.",
        latency_ms=round(latency_ms, 2),
        determinism_hash=det_hash,
        limitations=[
            zone_framing["caveat"],
            "No pre-compiled doctrine matched -- this is a coverage gap.",
            "Consult regulatory authority for definitive compliance guidance.",
        ],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# =============================================================================
# [TIE-17] FASTAPI SERVER
# =============================================================================

_engine_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager -- startup and shutdown hooks."""
    logger.info(f"R07 Safety Requirements Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} topics loaded")
    logger.info(f"Safety term normalization: {len(SAFETY_TERM_NORMALIZATION)} terms")
    logger.info(f"Authority weights: {len(AUTHORITY_WEIGHTS)} authorities")
    logger.info(f"Interaction edges: {len(INTERACTION_EDGES)} edges")
    logger.info(f"Cloud retriever: {'available' if CLOUD_RETRIEVER_AVAILABLE else 'not available'}")
    yield
    logger.info("R07 Safety Requirements Engine shutting down")


app = FastAPI(
    title="ECHO R07 Safety Requirements Engine",
    description="TIE-20 Gold Standard safety compliance intelligence for oil & gas operations. "
                "Covers OSHA 1910/1926, H2S, BOP, PSM, RMP, confined space, fall protection, PPE.",
    version=ENGINE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.post("/query", response_model=SafetyResponse)
async def query_endpoint(query: SafetyQuery):
    """Process a safety compliance query through the three-layer engine.

    Accepts a safety question and returns a comprehensive compliance analysis
    with citations, authority hierarchy, confidence stratification, and optional
    fact fragility scoring and multi-doctrine decomposition.
    """
    trace_id = trace_query(query.question)
    logger.info(f"[{trace_id}] Query received: {query.question[:120]}")
    try:
        normalized = normalize_semantics(query.question)
        response = three_layer_response(query, normalized, trace_id)
        complete_trace(trace_id)
        return response
    except Exception as exc:
        logger.error(f"[{trace_id}] Query processing error: {exc}")
        complete_trace(trace_id)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check with metrics, coverage, drift, and telemetry."""
    metrics = get_metrics()
    drift_report = _drift_watcher.get_drift_report()
    coverage_report = _coverage_map.get_report()
    telemetry = get_telemetry()

    error_stats = metrics.get_error_stats()
    status = "healthy"
    if error_stats["last_hour"] > 10:
        status = "degraded"
    if error_stats["last_hour"] > 50 or metrics.active_queries > 100:
        status = "unhealthy"

    return HealthResponse(
        status=status,
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        domain=ENGINE_DOMAIN,
        port=ENGINE_PORT,
        uptime_seconds=round(time.time() - _engine_start_time, 2),
        api_latency=metrics.get_latency_stats(),
        doctrine_cache={
            "status": "operational",
            "topics": len(DOCTRINE_CACHE),
            "hit_rate": metrics.get_doctrine_hit_rate(),
            "topics_list": [d.topic for d in DOCTRINE_CACHE],
        },
        coverage={
            "total_doctrines": coverage_report["total_doctrines"],
            "triggered_count": coverage_report["triggered_count"],
            "coverage_percentage": coverage_report["coverage_percentage"],
            "gap_queries": coverage_report["gap_queries_recorded"],
        },
        drift_status=drift_report.get("status", "unknown"),
        active_queries=metrics.active_queries,
        queries_last_hour=metrics.queries_last_hour(),
        total_queries=metrics.total_queries,
        error_rate=error_stats,
        layer_distribution=metrics.layer_counts,
        cloud_retriever=CLOUD_RETRIEVER_AVAILABLE,
        telemetry_summary=telemetry.get_trace_summary(),
    )


@app.get("/metrics")
async def metrics_endpoint():
    """Full metrics report including latency, hit rates, and category distribution."""
    return get_metrics().get_full_report()


@app.get("/drift")
async def drift_endpoint():
    """Doctrine drift analysis report."""
    return _drift_watcher.get_drift_report()


@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage map with triggered/untriggered topics and gap analysis."""
    return _coverage_map.get_report()


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics with confidence and stratification."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "stratification": d.confidence_stratification.value,
                "burden_holder": d.burden_holder,
                "adversary_position": d.adversary_position,
                "controlling_precedent": d.controlling_precedent,
                "authority_count": len(d.primary_authority),
                "authorities": d.primary_authority,
            }
            for d in DOCTRINE_CACHE
        ],
    }


@app.get("/authorities")
async def authorities_endpoint():
    """List all authority weights and classification system."""
    return {
        "total_authorities": len(AUTHORITY_WEIGHTS),
        "weights": {k: v for k, v in sorted(AUTHORITY_WEIGHTS.items(), key=lambda x: x[1], reverse=True)},
        "levels": [level.value for level in AuthorityLevel],
        "penalty_rates": {
            "osha_serious": OSHA_PENALTY_SERIOUS,
            "osha_willful": OSHA_PENALTY_WILLFUL,
            "osha_repeat": OSHA_PENALTY_REPEAT,
            "osha_failure_to_abate_per_day": OSHA_PENALTY_FAILURE_TO_ABATE,
            "bsee_per_day": BSEE_PENALTY_PER_DAY,
            "epa_rmp_per_day": EPA_RMP_PENALTY,
        },
    }


@app.get("/guardrails")
async def guardrails_endpoint():
    """Show epistemic guardrails configuration."""
    return {
        "banned_phrases": BANNED_PHRASES,
        "confidence_tiers": [t.value for t in ConfidenceTier],
        "analysis_zones": [z.value for z in AnalysisZone],
        "safety_categories": [c.value for c in SafetyIssueCategory],
        "interaction_edges": len(INTERACTION_EDGES),
        "safety_term_mappings": len(SAFETY_TERM_NORMALIZATION),
    }


@app.get("/audit-trail")
async def audit_trail_endpoint(limit: int = 50):
    """Read recent audit trail entries.

    Args:
        limit: Maximum entries to return (default 50, max 500).
    """
    limit = min(limit, 500)
    entries = []
    if AUDIT_LOG.exists():
        try:
            lines = AUDIT_LOG.read_text(encoding="utf-8").strip().split("\n")
            for line in lines[-limit:]:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception as exc:
            logger.error(f"Failed to read audit trail: {exc}")
    return {
        "total_entries": len(entries),
        "entries": entries,
    }


@app.get("/categories")
async def categories_endpoint():
    """List all safety issue categories and interaction edges."""
    return {
        "categories": [c.value for c in SafetyIssueCategory],
        "total_categories": len(SafetyIssueCategory),
        "interaction_edges": [
            {
                "from": e["from"].value,
                "to": e["to"].value,
                "relationship": e["relationship"],
                "description": e["description"],
            }
            for e in INTERACTION_EDGES
        ],
        "total_edges": len(INTERACTION_EDGES),
    }


@app.post("/resolve-authority-conflict")
async def resolve_conflict_endpoint(authorities: List[str]):
    """Resolve conflicts between multiple regulatory authorities."""
    return resolve_authority_conflict(authorities)


@app.post("/classify-confidence")
async def classify_confidence_endpoint(
    confidence: float,
    has_controlling_precedent: bool = True,
    stratification: str = "mandatory",
):
    """Classify confidence tier for a given confidence score."""
    strat_map = {
        "mandatory": ConfidenceStratification.MANDATORY,
        "clearly_required": ConfidenceStratification.CLEARLY_REQUIRED,
        "best_practice": ConfidenceStratification.BEST_PRACTICE,
    }
    strat = strat_map.get(stratification, ConfidenceStratification.MANDATORY)
    tier = classify_confidence(confidence, has_controlling_precedent, strat)
    return {"confidence": confidence, "tier": tier.value, "stratification": strat.value}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)
