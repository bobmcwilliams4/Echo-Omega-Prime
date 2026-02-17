"""
ECHO R06 ENVIRONMENTAL RULES ENGINE -- TIE-20 Gold Standard Production Architecture
Professional-grade environmental compliance analysis for oil & gas operations.

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning on TCEQ/EPA/RCRA/CWA/CAA
    Layer 2: Semantic Retrieval (200-700ms) - Fast RAG on cache miss
    Layer 3: Deep Analysis (on-demand) - Multi-source synthesis with full reasoning chain

Response Modes:
    FAST: Doctrine-driven, minimal citations, sub-2 seconds
    DEFENSE: Structured reasoning, audit-ready, penalty analysis
    MEMO: Long-form, citation-heavy, regulatory documentation

Domain: Environmental Regulations - TCEQ, EPA, RCRA, CWA, CAA, SPCC,
        stormwater, produced water, NORM, air permits, water discharge,
        waste disposal, endangered species, wetlands, coastal zone

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Port: 8706
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
from dataclasses import dataclass, field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import hashlib
import json
import time
import uuid
from pathlib import Path
from loguru import logger

# =============================================================================
# PATH SETUP (single canonical insert)
# =============================================================================

import sys

ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

# =============================================================================
# LOCAL MODULE IMPORTS
# =============================================================================

from telemetry import get_telemetry, trace_query, complete_trace, log_error, ErrorDomain
from semantic import normalize_semantics, NormalizationResult
from doctrines import DOCTRINE_CACHE, DoctrineBlock, match_doctrines, ConfidenceStratification
from search import vector_search

# Cloud retriever (optional, graceful degradation)
try:
    from cloud_retriever import cloud_retrieve
    _HAS_CLOUD_RETRIEVER = True
except ImportError:
    _HAS_CLOUD_RETRIEVER = False
    logger.warning("cloud_retriever not available; cloud-augmented retrieval disabled")

# =============================================================================
# CONSTANTS
# =============================================================================

ENGINE_NAME = "R06_environmental_rules"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8706
ENGINE_DOMAIN = "Environmental Compliance"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/R06_environmental_rules/logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

logger.add(
    LOG_DIR / "r06_engine_{time}.log",
    rotation="50 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)

AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

# =============================================================================
# ENVIRONMENTAL-SPECIFIC TERM NORMALIZATION MAP
# =============================================================================

ENVIRONMENTAL_TERM_MAP: Dict[str, str] = {
    "tceq": "Texas Commission on Environmental Quality",
    "epa": "Environmental Protection Agency",
    "rcra": "Resource Conservation and Recovery Act",
    "cercla": "Comprehensive Environmental Response Compensation and Liability Act",
    "spcc": "Spill Prevention Control and Countermeasure",
    "norm": "Naturally Occurring Radioactive Material",
    "tenorm": "Technologically Enhanced NORM",
    "npdes": "National Pollutant Discharge Elimination System",
    "tpdes": "Texas Pollutant Discharge Elimination System",
    "cwa": "Clean Water Act",
    "caa": "Clean Air Act",
    "nsr": "New Source Review",
    "psd": "Prevention of Significant Deterioration",
    "bact": "Best Available Control Technology",
    "laer": "Lowest Achievable Emission Rate",
    "ract": "Reasonably Available Control Technology",
    "swppp": "Stormwater Pollution Prevention Plan",
    "msgp": "Multi-Sector General Permit",
    "cgp": "Construction General Permit",
    "uic": "Underground Injection Control",
    "mit": "Mechanical Integrity Test",
    "swd": "Salt Water Disposal",
    "tsdf": "Treatment Storage and Disposal Facility",
    "rcra subtitle c": "RCRA Hazardous Waste (Subtitle C)",
    "rcra subtitle d": "RCRA Solid Waste (Subtitle D)",
    "e&p waste": "Exploration and Production Waste",
    "voc": "Volatile Organic Compound",
    "nox": "Nitrogen Oxides",
    "so2": "Sulfur Dioxide",
    "pm2.5": "Fine Particulate Matter",
    "pm10": "Coarse Particulate Matter",
    "h2s": "Hydrogen Sulfide",
    "tds": "Total Dissolved Solids",
    "bod": "Biological Oxygen Demand",
    "tss": "Total Suspended Solids",
    "wotus": "Waters of the United States",
    "jd": "Jurisdictional Determination",
    "nwp": "Nationwide Permit",
    "ipa": "Individual Permit Application",
    "esa": "Endangered Species Act",
    "nepa": "National Environmental Policy Act",
    "fonsi": "Finding of No Significant Impact",
    "eis": "Environmental Impact Statement",
    "ea": "Environmental Assessment",
    "pcl": "Protective Concentration Level",
    "msl": "Medium Specific Level",
    "opa": "Oil Pollution Act",
    "rrc": "Railroad Commission of Texas",
    "usace": "U.S. Army Corps of Engineers",
    "glo": "Texas General Land Office",
    "usfws": "U.S. Fish and Wildlife Service",
    "dshs": "Texas Department of State Health Services",
    "dot": "Department of Transportation",
    "osha": "Occupational Safety and Health Administration",
    "sara": "Superfund Amendments and Reauthorization Act",
    "epcra": "Emergency Planning and Community Right-to-Know Act",
    "tri": "Toxics Release Inventory",
    "tier ii": "EPCRA Tier II Chemical Inventory Report",
    "ldar": "Leak Detection and Repair",
    "cems": "Continuous Emission Monitoring System",
    "nsps": "New Source Performance Standards",
    "neshap": "National Emission Standards for Hazardous Air Pollutants",
    "mact": "Maximum Achievable Control Technology",
    "ghg": "Greenhouse Gas",
    "flp": "Facility Level Plan",
    "frp": "Facility Response Plan",
}

# =============================================================================
# ENVIRONMENTAL AUTHORITY WEIGHTS
# Hierarchical weighting: higher = more binding authority
# =============================================================================

AUTHORITY_WEIGHTS: Dict[str, int] = {
    # Federal statutes (highest)
    "Clean Water Act": 95,
    "Clean Air Act": 95,
    "RCRA": 95,
    "CERCLA/Superfund": 95,
    "Endangered Species Act": 95,
    "Oil Pollution Act 1990": 93,
    "NEPA": 90,
    "EPCRA/SARA Title III": 90,
    "Safe Drinking Water Act": 93,
    # Federal regulations (CFR)
    "40 CFR Part 112 (SPCC)": 90,
    "40 CFR Part 122 (NPDES)": 90,
    "40 CFR Part 144 (UIC Class II)": 90,
    "40 CFR Part 260-268 (RCRA Hazardous Waste)": 90,
    "40 CFR Part 261 (Hazardous Waste Identification)": 90,
    "40 CFR Part 264-265 (TSDF Standards)": 90,
    "40 CFR Part 279 (Used Oil)": 88,
    "40 CFR Part 300 (NCP/Superfund)": 90,
    "40 CFR Part 355 (Emergency Planning)": 88,
    "40 CFR Part 370 (Tier II Reporting)": 88,
    "40 CFR Part 372 (TRI Reporting)": 88,
    "40 CFR Part 52 (NSR)": 90,
    "40 CFR Part 60 (NSPS)": 90,
    "40 CFR Part 61-63 (NESHAP/MACT)": 90,
    "40 CFR Part 98 (GHG Reporting)": 88,
    "33 CFR Part 323 (Corps 404 Permits)": 90,
    "50 CFR Part 17 (Listed Species)": 90,
    "49 CFR Part 173 (Radioactive Materials Transport)": 88,
    # Texas state regulations (TAC)
    "30 TAC Chapter 106 (Permits by Rule)": 85,
    "30 TAC Chapter 116 (Air Permits)": 85,
    "30 TAC Chapter 213 (Edwards Aquifer)": 85,
    "30 TAC Chapter 290 (Public Water)": 85,
    "30 TAC Chapter 312 (Sludge/Beneficial Reuse)": 85,
    "30 TAC Chapter 321 (Wastewater)": 85,
    "30 TAC Chapter 330 (Municipal Solid Waste)": 85,
    "30 TAC Chapter 334 (UST)": 85,
    "30 TAC Chapter 335 (Industrial Solid Waste/Hazardous Waste)": 85,
    "30 TAC Chapter 350 (Contaminated Sites/TRRP)": 85,
    "16 TAC Section 3.8 (Water Protection/Disposal Wells)": 82,
    "16 TAC Section 3.46 (Oil Spills)": 82,
    "16 TAC Section 3.91 (Cleanup/Remediation)": 82,
    "16 TAC Section 3.98 (Standards for Waste Management)": 82,
    "25 TAC Section 289.252 (NORM)": 82,
    # Clean Air Act sections
    "CAA Section 109 (NAAQS)": 93,
    "CAA Section 111 (NSPS)": 93,
    "CAA Section 112 (HAPs/MACT)": 93,
    "CAA Section 160-169 (PSD)": 93,
    "CAA Section 171-193 (Nonattainment NSR)": 93,
    "CAA Section 502-507 (Title V Permits)": 93,
    # Clean Water Act sections
    "CWA Section 301 (Effluent Limitations)": 93,
    "CWA Section 311 (Oil/Hazardous Substance Spills)": 93,
    "CWA Section 402 (NPDES/TPDES)": 93,
    "CWA Section 404 (Dredge and Fill)": 93,
    # RCRA subtitles
    "RCRA Subtitle C (Hazardous Waste)": 93,
    "RCRA Subtitle D (Solid Waste)": 91,
    "RCRA Subtitle I (UST)": 91,
    # Agency guidance (lower weight)
    "TCEQ RG-209 (Air Permitting Guidance)": 70,
    "TCEQ RG-478 (Stormwater Guidance)": 70,
    "EPA SPCC Guidance for Regional Inspectors": 70,
    "RRC Oil and Gas Division Guidance": 70,
    "USFWS Biological Opinions": 80,
    "EPA Enforcement Response Policy": 75,
}

# =============================================================================
# ENVIRONMENTAL AGENCY DIRECTORY
# =============================================================================

AGENCY_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "TCEQ": {
        "full_name": "Texas Commission on Environmental Quality",
        "jurisdiction": "State of Texas",
        "domains": ["air quality", "water quality", "waste management", "stormwater",
                     "underground storage tanks", "contaminated sites", "edwards aquifer"],
        "penalty_authority": "$25,000/day per violation (TWC Section 7.102)",
        "website": "https://www.tceq.texas.gov",
    },
    "EPA": {
        "full_name": "Environmental Protection Agency",
        "jurisdiction": "Federal",
        "domains": ["all environmental media", "RCRA", "CERCLA", "CWA", "CAA",
                     "TSCA", "EPCRA", "FIFRA"],
        "penalty_authority": "Varies by statute (CWA: $64,618/day, CAA: $113,740/day, RCRA: $75,867/day)",
        "website": "https://www.epa.gov",
    },
    "RRC": {
        "full_name": "Railroad Commission of Texas",
        "jurisdiction": "State of Texas",
        "domains": ["oil and gas waste", "produced water disposal", "pit closure",
                     "oil spill cleanup", "well plugging", "surface casing"],
        "penalty_authority": "$10,000/day per violation (TNR Code Section 81.0531)",
        "website": "https://www.rrc.texas.gov",
    },
    "USACE": {
        "full_name": "U.S. Army Corps of Engineers",
        "jurisdiction": "Federal",
        "domains": ["wetlands permits (Section 404)", "navigable waters",
                     "jurisdictional determinations", "compensatory mitigation"],
        "penalty_authority": "$25,000-$50,000/day for unauthorized fill (CWA Section 404)",
        "website": "https://www.usace.army.mil",
    },
    "GLO": {
        "full_name": "Texas General Land Office",
        "jurisdiction": "State of Texas",
        "domains": ["coastal zone management", "oil spill response (coastal)",
                     "state submerged lands", "beach access"],
        "penalty_authority": "Varies under Texas Natural Resources Code",
        "website": "https://www.glo.texas.gov",
    },
    "USFWS": {
        "full_name": "U.S. Fish and Wildlife Service",
        "jurisdiction": "Federal",
        "domains": ["endangered species", "migratory birds", "habitat conservation",
                     "incidental take permits", "biological opinions"],
        "penalty_authority": "$50,000 civil per ESA violation, criminal penalties",
        "website": "https://www.fws.gov",
    },
    "DSHS": {
        "full_name": "Texas Department of State Health Services",
        "jurisdiction": "State of Texas",
        "domains": ["NORM licensing", "radioactive material", "radiation safety"],
        "penalty_authority": "$25,000/day for unlicensed NORM possession",
        "website": "https://www.dshs.texas.gov",
    },
}

# =============================================================================
# PENALTY SCHEDULE - KEY ENVIRONMENTAL VIOLATIONS
# =============================================================================

PENALTY_SCHEDULE: Dict[str, Dict[str, Any]] = {
    "CWA_unpermitted_discharge": {
        "statute": "Clean Water Act Section 309(d)",
        "max_per_day": 64_618,
        "criminal_knowing": "up to $50,000/day and/or 3 years imprisonment",
        "criminal_negligent": "up to $25,000/day and/or 1 year imprisonment",
        "notes": "Adjusted for inflation per 40 CFR Part 19",
    },
    "CAA_violation": {
        "statute": "Clean Air Act Section 113",
        "max_per_day": 113_740,
        "criminal_knowing": "up to $1,000,000 and/or 5 years imprisonment",
        "notes": "Knowing endangerment: up to $1M and 15 years",
    },
    "RCRA_hazardous_waste": {
        "statute": "RCRA Section 3008",
        "max_per_day": 75_867,
        "criminal_knowing": "up to $50,000/day and/or 5 years imprisonment",
        "notes": "Knowing endangerment: up to $250,000 and 15 years",
    },
    "TCEQ_general": {
        "statute": "Texas Water Code Section 7.102",
        "max_per_day": 25_000,
        "criminal": "Class A misdemeanor for knowing violations",
        "notes": "Each day of continuing violation is separate offense",
    },
    "SPCC_violation": {
        "statute": "CWA Section 311 / 40 CFR 112",
        "max_per_day": 25_000,
        "spill_liability": "Unlimited under OPA 90 for spill cleanup costs",
        "notes": "PE-certified plan required; inadequate plan = violation",
    },
    "ESA_take": {
        "statute": "Endangered Species Act Section 11",
        "max_civil": 50_000,
        "criminal_knowing": "$50,000 and/or 1 year imprisonment",
        "notes": "Injunctive relief can halt project entirely",
    },
    "Section_404_unauthorized_fill": {
        "statute": "CWA Section 404 / 33 USC 1344",
        "max_per_day": 50_000,
        "restoration": "Required removal of fill and wetland restoration at violator expense",
        "notes": "Corps can issue cease and desist without court order",
    },
    "NORM_unlicensed": {
        "statute": "25 TAC Section 289.252",
        "max_per_day": 25_000,
        "cercla_liability": "Superfund strict liability for improper disposal",
        "notes": "NORM threshold: >5,000 pCi/g Ra-226 or >50 pCi/g Ra-228",
    },
}

# =============================================================================
# ENVIRONMENTAL ISSUE CATEGORIES (for multi-doctrine decomposition)
# =============================================================================


class IssueCategory(str, Enum):
    """Environmental issue classification for multi-doctrine decomposition."""
    AIR_QUALITY = "air_quality"
    WATER_QUALITY = "water_quality"
    WASTE_MANAGEMENT = "waste_management"
    SPILL_PREVENTION = "spill_prevention"
    STORMWATER = "stormwater"
    PRODUCED_WATER = "produced_water"
    NORM_RADIATION = "norm_radiation"
    WETLANDS = "wetlands"
    ENDANGERED_SPECIES = "endangered_species"
    COASTAL_ZONE = "coastal_zone"
    CONTAMINATED_SITES = "contaminated_sites"
    UNDERGROUND_INJECTION = "underground_injection"
    EMERGENCY_PLANNING = "emergency_planning"
    GHG_REPORTING = "greenhouse_gas"
    REMEDIATION = "remediation"


# =============================================================================
# INTERACTION EDGES (multi-doctrine decomposition DAG)
# Cross-cutting regulatory interactions
# =============================================================================

INTERACTION_EDGES: List[Dict[str, Any]] = [
    {
        "from": IssueCategory.AIR_QUALITY,
        "to": IssueCategory.GHG_REPORTING,
        "interaction": "Facilities with Title V air permits typically trigger GHG Reporting Rule (40 CFR 98) "
                       "thresholds of 25,000 metric tons CO2e/year.",
        "weight": 0.85,
    },
    {
        "from": IssueCategory.PRODUCED_WATER,
        "to": IssueCategory.UNDERGROUND_INJECTION,
        "interaction": "Produced water disposal via Class II injection wells requires both RRC permits and EPA "
                       "UIC program compliance (40 CFR 144). Injection pressure/volume affect seismicity monitoring.",
        "weight": 0.95,
    },
    {
        "from": IssueCategory.PRODUCED_WATER,
        "to": IssueCategory.NORM_RADIATION,
        "interaction": "Produced water from high-salinity formations (especially Permian Basin) concentrates NORM "
                       "(Ra-226, Ra-228). Scale in tubing, tanks, and disposal equipment requires NORM surveys.",
        "weight": 0.80,
    },
    {
        "from": IssueCategory.SPILL_PREVENTION,
        "to": IssueCategory.WATER_QUALITY,
        "interaction": "SPCC violations that result in spills to navigable waters trigger CWA Section 311 "
                       "reporting (NRC notification within 24 hours) and potential NPDES/TPDES enforcement.",
        "weight": 0.90,
    },
    {
        "from": IssueCategory.SPILL_PREVENTION,
        "to": IssueCategory.CONTAMINATED_SITES,
        "interaction": "Spills that contaminate soil or groundwater trigger TCEQ TRRP (30 TAC 350) investigation "
                       "and remediation requirements. CERCLA liability may attach if hazardous substances involved.",
        "weight": 0.85,
    },
    {
        "from": IssueCategory.WASTE_MANAGEMENT,
        "to": IssueCategory.CONTAMINATED_SITES,
        "interaction": "Improper waste disposal (pit failures, tank leaks) creates contaminated sites requiring "
                       "TRRP assessment. E&P waste exemption under RCRA does not shield from state cleanup rules.",
        "weight": 0.80,
    },
    {
        "from": IssueCategory.STORMWATER,
        "to": IssueCategory.WATER_QUALITY,
        "interaction": "Stormwater discharges from industrial oil/gas facilities (TXR05 MSGP) must meet TPDES "
                       "effluent limits. Non-compliant discharges trigger both TCEQ and EPA enforcement authority.",
        "weight": 0.85,
    },
    {
        "from": IssueCategory.WETLANDS,
        "to": IssueCategory.ENDANGERED_SPECIES,
        "interaction": "Section 404 permits with federal nexus trigger ESA Section 7 consultation. Wetland habitat "
                       "for listed species (whooping crane, Texas hornshell) requires USFWS biological opinion.",
        "weight": 0.80,
    },
    {
        "from": IssueCategory.WETLANDS,
        "to": IssueCategory.COASTAL_ZONE,
        "interaction": "Coastal wetlands activities require both Section 404 permit and Texas Coastal Management "
                       "Program consistency determination (GLO review).",
        "weight": 0.75,
    },
    {
        "from": IssueCategory.AIR_QUALITY,
        "to": IssueCategory.WASTE_MANAGEMENT,
        "interaction": "Air emission control equipment (scrubbers, thermal oxidizers) generates secondary waste "
                       "streams requiring RCRA characterization and proper management.",
        "weight": 0.65,
    },
    {
        "from": IssueCategory.EMERGENCY_PLANNING,
        "to": IssueCategory.SPILL_PREVENTION,
        "interaction": "EPCRA Tier II reporting identifies chemical inventories that also inform SPCC plan "
                       "requirements. Facilities storing >10,000 lbs of hazardous chemicals trigger both.",
        "weight": 0.70,
    },
    {
        "from": IssueCategory.UNDERGROUND_INJECTION,
        "to": IssueCategory.WATER_QUALITY,
        "interaction": "Injection well failures (casing leaks, out-of-zone migration) contaminate USDWs, "
                       "triggering SDWA enforcement and potential CERCLA liability for aquifer remediation.",
        "weight": 0.85,
    },
    {
        "from": IssueCategory.REMEDIATION,
        "to": IssueCategory.WASTE_MANAGEMENT,
        "interaction": "Remediation activities generate investigation-derived waste (IDW) that must be characterized "
                       "and managed under RCRA. Contaminated soil/water may be RCRA hazardous waste.",
        "weight": 0.75,
    },
    {
        "from": IssueCategory.NORM_RADIATION,
        "to": IssueCategory.WASTE_MANAGEMENT,
        "interaction": "NORM-contaminated equipment and waste (scale, sludge, filters) requires characterization "
                       "and disposal at licensed LLRW facilities. DOT transport rules add complexity.",
        "weight": 0.80,
    },
]

# =============================================================================
# EPISTEMIC GUARDRAILS
# =============================================================================

BANNED_PHRASES: List[str] = [
    "you should be fine",
    "probably not a problem",
    "i wouldn't worry about",
    "no one ever gets caught",
    "just don't tell",
    "the agency won't find out",
    "it's just a technicality",
    "nobody enforces that",
    "you can ignore that requirement",
    "don't bother with the permit",
    "it's not a big deal",
    "everyone does it that way",
    "the regulation doesn't really apply",
    "you'll be grandfathered in",
    "just claim the E&P waste exemption",
    "dump it and move on",
    "the fine is just the cost of doing business",
    "self-report and they won't penalize you",
    "TCEQ is too busy to inspect your site",
    "EPA doesn't have jurisdiction in Texas",
]

DISCLOSURE_CAVEATS: Dict[str, str] = {
    "regulatory_change": (
        "Environmental regulations are subject to frequent amendment. Verify current requirements "
        "with TCEQ, EPA, or relevant agency before relying on this analysis."
    ),
    "site_specific": (
        "Environmental compliance determinations are inherently site-specific. Factors such as "
        "proximity to sensitive receptors, geology, hydrology, and existing contamination may "
        "alter obligations beyond general regulatory requirements."
    ),
    "enforcement_discretion": (
        "Regulatory agencies exercise enforcement discretion. The analysis of penalty exposure "
        "reflects statutory maximums; actual penalties consider violation history, gravity, "
        "ability to pay, and economic benefit of noncompliance."
    ),
    "multi_agency": (
        "Multiple agencies may have overlapping jurisdiction over environmental issues at oil "
        "and gas facilities. TCEQ, EPA, RRC, USACE, and USFWS authority may all apply to a "
        "single operation. Compliance with one agency does not ensure compliance with others."
    ),
    "permit_conditions": (
        "This analysis addresses general regulatory requirements. Individual permit conditions, "
        "consent orders, and agreed orders may impose stricter obligations than general regulations."
    ),
    "legal_advice": (
        "This environmental compliance analysis is informational only and does not constitute "
        "legal advice. Consult qualified environmental counsel for specific compliance decisions."
    ),
}


def apply_epistemic_guardrails(text: str) -> Dict[str, Any]:
    """Scan text for banned phrases and attach required disclosures.

    Returns:
        Dict with 'clean' bool, list of 'violations', and applicable 'disclosures'.
    """
    violations: List[str] = []
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            violations.append(phrase)

    # Determine which disclosure caveats are warranted
    applicable_disclosures: List[str] = []
    # Always include legal advice caveat
    applicable_disclosures.append(DISCLOSURE_CAVEATS["legal_advice"])
    # Site-specific caveat for most queries
    applicable_disclosures.append(DISCLOSURE_CAVEATS["site_specific"])
    # Multi-agency caveat if multiple agencies referenced
    agency_keywords = ["tceq", "epa", "rrc", "usace", "usfws", "glo", "dshs"]
    agency_count = sum(1 for kw in agency_keywords if kw in text_lower)
    if agency_count >= 2:
        applicable_disclosures.append(DISCLOSURE_CAVEATS["multi_agency"])
    # Enforcement discretion if penalties discussed
    penalty_keywords = ["penalty", "fine", "violation", "enforcement", "civil penalty"]
    if any(kw in text_lower for kw in penalty_keywords):
        applicable_disclosures.append(DISCLOSURE_CAVEATS["enforcement_discretion"])
    # Permit conditions if permits discussed
    permit_keywords = ["permit", "authorization", "approval", "license"]
    if any(kw in text_lower for kw in permit_keywords):
        applicable_disclosures.append(DISCLOSURE_CAVEATS["permit_conditions"])

    return {
        "clean": len(violations) == 0,
        "violations": violations,
        "disclosures": applicable_disclosures,
    }


# =============================================================================
# FACT FRAGILITY SCORING
# =============================================================================


@dataclass
class FragilityScore:
    """Quantifies how fragile (likely to change or be challenged) a factual assertion is."""
    verifiability: float  # 0-1: how easily the fact can be independently verified
    recharacterization_risk: float  # 0-1: risk that a different interpretation changes outcome
    testimony_dependence: float  # 0-1: how much the fact depends on witness/operator testimony
    regulatory_volatility: float  # 0-1: how likely the underlying regulation will change
    overall_fragility: float  # weighted composite

    def to_dict(self) -> Dict[str, float]:
        return {
            "verifiability": round(self.verifiability, 3),
            "recharacterization_risk": round(self.recharacterization_risk, 3),
            "testimony_dependence": round(self.testimony_dependence, 3),
            "regulatory_volatility": round(self.regulatory_volatility, 3),
            "overall_fragility": round(self.overall_fragility, 3),
        }


def compute_fact_fragility(
    doctrine_match: bool,
    confidence: float,
    category: IssueCategory,
    multi_agency: bool,
) -> FragilityScore:
    """Compute fragility score for an environmental compliance determination.

    Args:
        doctrine_match: Whether a doctrine cache hit occurred.
        confidence: Doctrine confidence score (0-1).
        category: Environmental issue category.
        multi_agency: Whether multiple agencies have overlapping jurisdiction.

    Returns:
        FragilityScore with component and composite scores.
    """
    # Verifiability: doctrine-backed assertions are more verifiable
    verifiability = 0.9 if doctrine_match else 0.5

    # Recharacterization risk: higher for ambiguous categories
    rechar_risk_map = {
        IssueCategory.WASTE_MANAGEMENT: 0.6,  # E&P waste exemption is contested
        IssueCategory.WETLANDS: 0.7,  # WOTUS definition constantly litigated
        IssueCategory.CONTAMINATED_SITES: 0.5,
        IssueCategory.AIR_QUALITY: 0.4,
        IssueCategory.ENDANGERED_SPECIES: 0.6,  # habitat definitions evolving
        IssueCategory.NORM_RADIATION: 0.3,  # thresholds are numerical/clear
    }
    recharacterization_risk = rechar_risk_map.get(category, 0.4)

    # Testimony dependence: operational facts often rely on self-reporting
    testimony_dependence = 0.5 if doctrine_match else 0.7

    # Regulatory volatility: some areas change more than others
    volatility_map = {
        IssueCategory.WETLANDS: 0.8,  # WOTUS rule has changed repeatedly
        IssueCategory.GHG_REPORTING: 0.7,  # political volatility
        IssueCategory.ENDANGERED_SPECIES: 0.6,  # listing decisions change
        IssueCategory.AIR_QUALITY: 0.5,
        IssueCategory.SPILL_PREVENTION: 0.3,
        IssueCategory.UNDERGROUND_INJECTION: 0.4,
        IssueCategory.NORM_RADIATION: 0.3,
    }
    regulatory_volatility = volatility_map.get(category, 0.4)

    # Multi-agency overlap increases fragility
    if multi_agency:
        recharacterization_risk = min(1.0, recharacterization_risk + 0.15)

    # Composite: weighted average
    overall = (
        (1.0 - verifiability) * 0.25
        + recharacterization_risk * 0.30
        + testimony_dependence * 0.20
        + regulatory_volatility * 0.25
    )

    return FragilityScore(
        verifiability=verifiability,
        recharacterization_risk=recharacterization_risk,
        testimony_dependence=testimony_dependence,
        regulatory_volatility=regulatory_volatility,
        overall_fragility=min(1.0, overall),
    )


# =============================================================================
# DRIFT WATCHER
# =============================================================================


class DriftWatcher:
    """Tracks doctrine cache drift over time -- detects when cached reasoning
    diverges from the latest regulatory landscape."""

    def __init__(self) -> None:
        self._drift_log: List[Dict[str, Any]] = []
        self._baseline_snapshot: Dict[str, float] = {}
        self._initialize_baseline()

    def _initialize_baseline(self) -> None:
        """Capture baseline confidence scores from current doctrine cache."""
        for doctrine in DOCTRINE_CACHE:
            self._baseline_snapshot[doctrine.topic] = doctrine.confidence

    def check_drift(self, topic: str, current_confidence: float) -> Dict[str, Any]:
        """Compare current doctrine confidence against baseline.

        Args:
            topic: Doctrine topic name.
            current_confidence: Current confidence score.

        Returns:
            Drift report dict.
        """
        baseline = self._baseline_snapshot.get(topic)
        if baseline is None:
            return {"topic": topic, "status": "new_topic", "drift": 0.0}

        drift = abs(current_confidence - baseline)
        status = "stable"
        if drift > 0.15:
            status = "significant_drift"
        elif drift > 0.05:
            status = "minor_drift"

        entry = {
            "topic": topic,
            "baseline_confidence": round(baseline, 3),
            "current_confidence": round(current_confidence, 3),
            "drift": round(drift, 3),
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._drift_log.append(entry)
        if len(self._drift_log) > 500:
            self._drift_log = self._drift_log[-500:]

        if status == "significant_drift":
            logger.warning(f"DRIFT ALERT: {topic} drifted {drift:.3f} from baseline")

        return entry

    def record_regulatory_update(self, topic: str, new_confidence: float, reason: str) -> None:
        """Record a regulatory change that updates the baseline."""
        old_confidence = self._baseline_snapshot.get(topic, 0.0)
        self._baseline_snapshot[topic] = new_confidence
        self._drift_log.append({
            "topic": topic,
            "type": "baseline_update",
            "old_confidence": round(old_confidence, 3),
            "new_confidence": round(new_confidence, 3),
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.info(f"DRIFT BASELINE UPDATE: {topic} -> {new_confidence:.3f} ({reason})")

    def get_drift_report(self) -> Dict[str, Any]:
        """Generate comprehensive drift report across all doctrines."""
        drift_entries = []
        for doctrine in DOCTRINE_CACHE:
            entry = self.check_drift(doctrine.topic, doctrine.confidence)
            drift_entries.append(entry)

        drifted = [e for e in drift_entries if e["status"] != "stable"]
        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "drifted_count": len(drifted),
            "stable_count": len(drift_entries) - len(drifted),
            "drift_entries": drift_entries,
            "last_check": datetime.now(timezone.utc).isoformat(),
        }

    def get_drift_log(self) -> List[Dict[str, Any]]:
        """Return the full drift observation log."""
        return list(self._drift_log)


# =============================================================================
# COVERAGE MAP
# =============================================================================


class CoverageMap:
    """Tracks which doctrines are triggered and identifies epistemic gaps."""

    def __init__(self) -> None:
        self._trigger_counts: Dict[str, int] = {d.topic: 0 for d in DOCTRINE_CACHE}
        self._miss_queries: List[Dict[str, Any]] = []
        self._gap_log: List[Dict[str, Any]] = []

    def record_hit(self, topics: List[str]) -> None:
        """Record doctrine hits for triggered topics."""
        for topic in topics:
            if topic in self._trigger_counts:
                self._trigger_counts[topic] += 1
            else:
                self._trigger_counts[topic] = 1

    def record_miss(self, query_text: str, keywords: List[str]) -> None:
        """Record a query that matched no doctrines."""
        entry = {
            "query": query_text[:200],
            "keywords": keywords[:10],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._miss_queries.append(entry)
        if len(self._miss_queries) > 200:
            self._miss_queries = self._miss_queries[-200:]
        self._detect_gap(keywords)

    def _detect_gap(self, keywords: List[str]) -> None:
        """Analyze missed keywords for potential gaps in doctrine coverage."""
        # Environmental-specific gap categories
        gap_indicators = {
            "air_quality_gap": ["emission", "air", "pollutant", "stack", "flare", "voc", "nox"],
            "water_quality_gap": ["discharge", "effluent", "water quality", "tpdes", "npdes"],
            "waste_gap": ["hazardous", "solid waste", "rcra", "manifest", "cradle to grave"],
            "remediation_gap": ["cleanup", "remediation", "trrp", "pcl", "contamination"],
            "emergency_gap": ["spill", "release", "emergency", "tier ii", "epcra"],
            "coastal_gap": ["coastal", "beach", "tidal", "glo", "cms"],
        }
        kw_set = set(k.lower() for k in keywords)
        for gap_name, indicators in gap_indicators.items():
            if any(ind in kw_set for ind in indicators):
                self._gap_log.append({
                    "gap_type": gap_name,
                    "triggering_keywords": [k for k in keywords if k.lower() in indicators],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                if len(self._gap_log) > 200:
                    self._gap_log = self._gap_log[-200:]

    def get_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report showing triggered/untriggered doctrines and gaps."""
        triggered = {k: v for k, v in self._trigger_counts.items() if v > 0}
        untriggered = [k for k, v in self._trigger_counts.items() if v == 0]
        total = sum(self._trigger_counts.values())

        return {
            "total_doctrines": len(DOCTRINE_CACHE),
            "triggered_doctrines": len(triggered),
            "untriggered_doctrines": untriggered,
            "trigger_counts": self._trigger_counts,
            "total_queries_processed": total,
            "miss_count": len(self._miss_queries),
            "recent_misses": self._miss_queries[-10:],
            "detected_gaps": self._gap_log[-20:],
            "coverage_ratio": round(len(triggered) / max(len(self._trigger_counts), 1), 3),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# =============================================================================
# METRICS COLLECTOR
# =============================================================================


class MetricsCollector:
    """Lightweight metrics for operational awareness. No external dependencies."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.errors: List[float] = []
        self.queries: List[float] = []
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.last_error: Optional[str] = None
        self.active_queries: int = 0
        self._max_latencies: int = 200

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a completed query with its latency and hit status."""
        now = time.time()
        self.latencies.append(latency_ms)
        if len(self.latencies) > self._max_latencies:
            self.latencies = self.latencies[-self._max_latencies:]
        self.queries.append(now)
        self.queries = [t for t in self.queries if t > now - 3600]
        if doctrine_hit:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

    def record_error(self, error_msg: str) -> None:
        """Record an error occurrence."""
        self.errors.append(time.time())
        self.last_error = f"{datetime.now(timezone.utc).isoformat()}: {error_msg[:200]}"
        self.errors = [t for t in self.errors if t > time.time() - 86400]

    def query_start(self) -> None:
        """Increment active query count."""
        self.active_queries += 1

    def query_end(self) -> None:
        """Decrement active query count."""
        self.active_queries = max(0, self.active_queries - 1)

    def get_latency_stats(self) -> Dict[str, float]:
        """Return latency percentile statistics."""
        if not self.latencies:
            return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "last_ms": 0.0}
        s = sorted(self.latencies)
        n = len(s)
        return {
            "avg_ms": round(sum(s) / n, 2),
            "p50_ms": round(s[int(n * 0.50)], 2),
            "p95_ms": round(s[min(int(n * 0.95), n - 1)], 2),
            "p99_ms": round(s[min(int(n * 0.99), n - 1)], 2),
            "last_ms": round(s[-1], 2),
        }

    def get_error_stats(self) -> Dict[str, Any]:
        """Return error frequency statistics."""
        now = time.time()
        return {
            "last_hour": sum(1 for t in self.errors if t > now - 3600),
            "last_24h": len(self.errors),
            "last_error": self.last_error,
        }

    def get_doctrine_hit_rate(self) -> float:
        """Return doctrine cache hit rate."""
        total = self.doctrine_hits + self.doctrine_misses
        return round(self.doctrine_hits / total, 4) if total > 0 else 1.0

    def queries_last_hour(self) -> int:
        """Count queries in the last hour."""
        return sum(1 for t in self.queries if t > time.time() - 3600)

    def to_dict(self) -> Dict[str, Any]:
        """Full metrics snapshot."""
        return {
            "latency": self.get_latency_stats(),
            "errors": self.get_error_stats(),
            "doctrine_hit_rate": self.get_doctrine_hit_rate(),
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "queries_last_hour": self.queries_last_hour(),
            "active_queries": self.active_queries,
            "total_queries": self.doctrine_hits + self.doctrine_misses,
        }


# =============================================================================
# AUDIT TRAIL
# =============================================================================


class AuditTrail:
    """Append-only JSONL audit trail for forensic review of every query."""

    def __init__(self, log_path: Path) -> None:
        self._path = log_path
        self._in_memory: List[Dict[str, Any]] = []
        self._max_memory = 500

    def record(
        self,
        trace_id: str,
        question: str,
        mode: str,
        jurisdiction: str,
        operator_type: Optional[str],
        doctrine_match: bool,
        response_layer: str,
        confidence_tier: str,
        confidence_strat: Optional[str],
        latency_ms: float,
        determinism_hash: Optional[str],
        guardrail_violations: List[str],
    ) -> None:
        """Write a single audit entry to disk and memory."""
        entry = {
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question[:500],
            "mode": mode,
            "jurisdiction": jurisdiction,
            "operator_type": operator_type,
            "doctrine_match": doctrine_match,
            "response_layer": response_layer,
            "confidence_tier": confidence_tier,
            "confidence_stratification": confidence_strat,
            "latency_ms": round(latency_ms, 2),
            "determinism_hash": determinism_hash,
            "guardrail_violations": guardrail_violations,
        }
        self._in_memory.append(entry)
        if len(self._in_memory) > self._max_memory:
            self._in_memory = self._in_memory[-self._max_memory:]
        try:
            with open(self._path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            logger.error(f"Audit trail write failed: {exc}")

    def recent(self, count: int = 50) -> List[Dict[str, Any]]:
        """Return recent audit entries from memory."""
        return list(self._in_memory[-count:])

    def stats(self) -> Dict[str, Any]:
        """Aggregate audit statistics."""
        if not self._in_memory:
            return {"total": 0}
        doctrine_hits = sum(1 for e in self._in_memory if e["doctrine_match"])
        layers = {}
        for e in self._in_memory:
            layers[e["response_layer"]] = layers.get(e["response_layer"], 0) + 1
        return {
            "total_entries": len(self._in_memory),
            "doctrine_hit_rate": round(doctrine_hits / len(self._in_memory), 3),
            "layer_distribution": layers,
            "guardrail_violation_count": sum(
                len(e["guardrail_violations"]) for e in self._in_memory
            ),
        }


# =============================================================================
# GLOBAL STATE INSTANCES
# =============================================================================

_metrics = MetricsCollector()
_drift_watcher = DriftWatcher()
_coverage_map = CoverageMap()
_audit_trail = AuditTrail(AUDIT_LOG)
_start_time = time.time()


def get_metrics() -> MetricsCollector:
    return _metrics


# =============================================================================
# PYDANTIC MODELS
# =============================================================================


class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class Complexity(str, Enum):
    STANDARD = "standard"
    ADVANCED = "advanced"


class OperatorType(str, Enum):
    PRODUCER = "producer"
    OPERATOR = "operator"
    FACILITY_OWNER = "facility_owner"
    PIPELINE_COMPANY = "pipeline_company"
    DISPOSAL_OPERATOR = "disposal_operator"
    SERVICE_COMPANY = "service_company"


class PositionZone(str, Enum):
    PLANNING = "planning"
    COMPLIANCE = "compliance"
    AUDIT = "audit"


@dataclass
class ZonedConclusion:
    """Position-zone-separated conclusion with confidence and caveats."""
    zone: PositionZone
    conclusion: str
    confidence: float
    caveats: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    responsible_agency: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone": self.zone.value,
            "conclusion": self.conclusion,
            "confidence": round(self.confidence, 3),
            "caveats": self.caveats,
            "action_items": self.action_items,
            "responsible_agency": self.responsible_agency,
        }


class EnvironmentalQuery(BaseModel):
    """Input model for environmental compliance queries."""
    question: str = Field(..., min_length=10, description="Environmental compliance question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    jurisdiction: str = Field(default="Texas", description="Regulatory jurisdiction")
    operator_type: Optional[OperatorType] = Field(default=None, description="Entity type")
    complexity: Complexity = Field(default=Complexity.STANDARD, description="Analysis depth")
    include_trace: bool = Field(default=False, description="Include telemetry trace")
    include_fragility: bool = Field(default=False, description="Include fact fragility scoring")


class Citation(BaseModel):
    """Regulatory citation with authority and relevance."""
    authority: str
    reference: str
    relevance: str
    weight: Optional[int] = None


class ReasoningStep(BaseModel):
    """Single step in a multi-step reasoning chain."""
    step: int
    analysis: str
    authority: Optional[str] = None
    confidence: Optional[float] = None


class EnvironmentalResponse(BaseModel):
    """Full response model for environmental compliance analysis."""
    query_id: str
    question: str
    mode: ResponseMode
    conclusion: str
    reasoning: str
    key_factors: List[str]
    citations: List[Citation]
    permit_requirements: Optional[List[str]] = None
    compliance_deadlines: Optional[List[str]] = None
    penalties_for_violation: Optional[str] = None
    responsible_agencies: Optional[List[str]] = None
    doctrine_match: bool
    confidence_tier: Literal["high", "moderate", "requires_review"]
    response_layer: Literal["doctrine", "retrieval", "deep_analysis"]
    latency_ms: float
    conflict_detected: bool = False
    authority_weight: Optional[int] = None
    confidence_stratification: Optional[str] = None
    controlling_precedent: Optional[str] = None
    determinism_hash: Optional[str] = None
    reasoning_trace: Optional[List[ReasoningStep]] = None
    zoned_analysis: Optional[List[Dict[str, Any]]] = None
    coverage_report: Optional[Dict[str, Any]] = None
    fact_fragility: Optional[Dict[str, float]] = None
    issue_categories: Optional[List[str]] = None
    interaction_edges: Optional[List[Dict[str, Any]]] = None
    epistemic_guardrails: Optional[Dict[str, Any]] = None
    disclosure_caveats: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    timestamp: str
    version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    """Health check response model."""
    status: Literal["healthy", "degraded", "unhealthy"]
    engine: str
    version: str
    uptime_seconds: float
    api_latency: Dict[str, float]
    doctrine_cache: Dict[str, Any]
    vector_db: Dict[str, Any]
    memory_mb: Dict[str, float]
    active_queries: int
    queries_last_hour: int
    error_rate: Dict[str, Any]
    coverage_ratio: float
    drift_status: str
    cloud_retriever_available: bool


# =============================================================================
# MULTI-DOCTRINE DECOMPOSITION
# =============================================================================


def classify_issue_categories(query_text: str, keywords: List[str]) -> List[IssueCategory]:
    """Classify a query into one or more environmental issue categories.

    Args:
        query_text: Original or normalized query text.
        keywords: Extracted keywords.

    Returns:
        List of matching IssueCategory enums.
    """
    text_lower = query_text.lower()
    kw_set = set(k.lower() for k in keywords)
    matches: List[IssueCategory] = []

    category_signals: Dict[IssueCategory, List[str]] = {
        IssueCategory.AIR_QUALITY: [
            "air permit", "nsr", "psd", "bact", "title v", "emission", "voc", "nox",
            "flare", "compressor", "dehydrator", "nsps", "neshap", "mact", "ldar",
            "cems", "air quality", "air pollution", "stack", "fugitive",
        ],
        IssueCategory.WATER_QUALITY: [
            "water quality", "discharge", "effluent", "npdes", "tpdes", "outfall",
            "water pollution", "bod", "tss", "tds", "water treatment",
        ],
        IssueCategory.WASTE_MANAGEMENT: [
            "waste", "rcra", "hazardous waste", "solid waste", "manifest",
            "tsdf", "generator", "cradle to grave", "e&p waste", "exploration waste",
            "used oil", "waste characterization",
        ],
        IssueCategory.SPILL_PREVENTION: [
            "spcc", "spill", "secondary containment", "oil spill", "spill plan",
            "frp", "facility response plan", "opa", "oil pollution",
        ],
        IssueCategory.STORMWATER: [
            "stormwater", "storm water", "txr05", "txr15", "msgp", "cgp",
            "swppp", "bmp", "erosion control", "sedimentation",
        ],
        IssueCategory.PRODUCED_WATER: [
            "produced water", "disposal well", "injection well", "salt water",
            "swd", "class ii", "brine", "formation water",
        ],
        IssueCategory.NORM_RADIATION: [
            "norm", "radioactive", "tenorm", "radium", "radiation", "pci/g",
            "radioactive scale", "llrw", "decontamination",
        ],
        IssueCategory.WETLANDS: [
            "wetland", "section 404", "404 permit", "wotus", "waters of the us",
            "corps permit", "jurisdictional determination", "mitigation bank",
            "compensatory mitigation", "nwp 12",
        ],
        IssueCategory.ENDANGERED_SPECIES: [
            "endangered", "threatened", "esa", "section 7", "incidental take",
            "biological opinion", "critical habitat", "listed species",
            "dunes sagebrush lizard", "lesser prairie chicken", "whooping crane",
        ],
        IssueCategory.COASTAL_ZONE: [
            "coastal", "coastal zone", "glo", "beach", "tidal", "cms",
            "coastal management", "submerged land",
        ],
        IssueCategory.CONTAMINATED_SITES: [
            "contamination", "remediation", "trrp", "pcl", "cleanup",
            "soil contamination", "groundwater contamination", "brownfield",
            "superfund", "cercla",
        ],
        IssueCategory.UNDERGROUND_INJECTION: [
            "injection", "uic", "class ii", "underground injection", "well integrity",
            "annular pressure", "mechanical integrity", "seismicity",
        ],
        IssueCategory.EMERGENCY_PLANNING: [
            "emergency", "epcra", "tier ii", "chemical inventory", "sara",
            "tri", "toxics release", "rmp", "risk management plan",
        ],
        IssueCategory.GHG_REPORTING: [
            "greenhouse gas", "ghg", "carbon", "co2", "methane", "ch4",
            "climate", "ghg reporting", "40 cfr 98",
        ],
        IssueCategory.REMEDIATION: [
            "remediation", "cleanup", "corrective action", "risk assessment",
            "soil removal", "pump and treat", "monitored natural attenuation",
            "institutional controls",
        ],
    }

    for category, signals in category_signals.items():
        for signal in signals:
            if signal in text_lower or signal in kw_set:
                if category not in matches:
                    matches.append(category)
                break

    if not matches:
        matches.append(IssueCategory.WASTE_MANAGEMENT)  # default for O&G queries

    return matches


def find_relevant_interactions(categories: List[IssueCategory]) -> List[Dict[str, Any]]:
    """Find interaction edges relevant to the given issue categories.

    Args:
        categories: List of classified issue categories.

    Returns:
        List of applicable interaction edge dicts.
    """
    cat_set = set(categories)
    relevant = []
    for edge in INTERACTION_EDGES:
        if edge["from"] in cat_set or edge["to"] in cat_set:
            relevant.append({
                "from": edge["from"].value,
                "to": edge["to"].value,
                "interaction": edge["interaction"],
                "weight": edge["weight"],
            })
    return relevant


# =============================================================================
# DEEP ANALYSIS MODE
# =============================================================================


def deep_analysis(
    query: "EnvironmentalQuery",
    normalized: NormalizationResult,
    categories: List[IssueCategory],
    interactions: List[Dict[str, Any]],
) -> List[ReasoningStep]:
    """Perform multi-step deep analysis when doctrine cache and retrieval both miss.

    Returns a full reasoning chain with 8 steps:
    1. Issue identification
    2. Regulatory framework mapping
    3. Authority hierarchy resolution
    4. Multi-agency jurisdiction analysis
    5. Penalty exposure assessment
    6. Interaction analysis (cross-cutting effects)
    7. Compliance pathway synthesis
    8. Confidence and limitation assessment
    """
    steps: List[ReasoningStep] = []

    # Step 1: Issue identification
    cat_names = [c.value for c in categories]
    steps.append(ReasoningStep(
        step=1,
        analysis=(
            f"Issue identification: Query classified into {len(categories)} environmental "
            f"category(ies): {', '.join(cat_names)}. Keywords extracted: "
            f"{', '.join(normalized.keywords[:10])}. Jurisdiction: {query.jurisdiction}."
        ),
        confidence=0.85,
    ))

    # Step 2: Regulatory framework mapping
    framework_lines = []
    for cat in categories:
        if cat == IssueCategory.AIR_QUALITY:
            framework_lines.append(
                "Air quality: 30 TAC 116 (TCEQ air permits), CAA Section 111/112 (NSPS/NESHAP), "
                "40 CFR 60/63, Title V operating permits"
            )
        elif cat == IssueCategory.WATER_QUALITY:
            framework_lines.append(
                "Water quality: CWA Section 301/402, 30 TAC 321 (wastewater), TPDES permits, "
                "effluent guidelines for oil and gas extraction"
            )
        elif cat == IssueCategory.WASTE_MANAGEMENT:
            framework_lines.append(
                "Waste management: RCRA Subtitle C (hazardous), Subtitle D (solid), "
                "E&P waste exemption under 40 CFR 261.4(b)(5), 30 TAC 335, 16 TAC 3.98"
            )
        elif cat == IssueCategory.SPILL_PREVENTION:
            framework_lines.append(
                "Spill prevention: 40 CFR 112 (SPCC), CWA Section 311, OPA 90, "
                "Facility Response Plans for substantial harm facilities"
            )
        elif cat == IssueCategory.STORMWATER:
            framework_lines.append(
                "Stormwater: CWA Section 402, TXR05 MSGP (Sector J), TXR15 CGP, "
                "30 TAC 213 (Edwards Aquifer), SWPPP requirements"
            )
        elif cat == IssueCategory.PRODUCED_WATER:
            framework_lines.append(
                "Produced water: 16 TAC 3.8 (disposal wells), 40 CFR 144 (UIC Class II), "
                "30 TAC 312 (beneficial reuse), SDWA"
            )
        elif cat == IssueCategory.NORM_RADIATION:
            framework_lines.append(
                "NORM: 25 TAC 289.252 (DSHS), DOT 49 CFR 173 (transport), "
                "CERCLA liability for improper disposal, LLRW disposal requirements"
            )
        elif cat == IssueCategory.WETLANDS:
            framework_lines.append(
                "Wetlands: CWA Section 404, 33 CFR 323 (Corps permits), NWP 12 (pipelines), "
                "WOTUS jurisdictional determination, compensatory mitigation"
            )
        elif cat == IssueCategory.ENDANGERED_SPECIES:
            framework_lines.append(
                "Endangered species: ESA Sections 7/9/10, 50 CFR Part 17, USFWS biological "
                "opinions, CCAAs, Incidental Take Permits, Habitat Conservation Plans"
            )
        elif cat == IssueCategory.CONTAMINATED_SITES:
            framework_lines.append(
                "Contaminated sites: 30 TAC 350 (TRRP), CERCLA Section 107 (strict liability), "
                "PCL/MSL risk-based standards, remediation/corrective action"
            )
        elif cat == IssueCategory.UNDERGROUND_INJECTION:
            framework_lines.append(
                "Underground injection: 40 CFR 144 (UIC), 16 TAC 3.8 (RRC), Class II wells, "
                "MIT every 5 years, induced seismicity monitoring"
            )
        elif cat == IssueCategory.EMERGENCY_PLANNING:
            framework_lines.append(
                "Emergency planning: EPCRA/SARA Title III, 40 CFR 355/370/372, Tier II reporting, "
                "TRI reporting, CAA Section 112(r) RMP"
            )
        elif cat == IssueCategory.GHG_REPORTING:
            framework_lines.append(
                "GHG reporting: 40 CFR Part 98, Subpart W (petroleum/natural gas), "
                "threshold 25,000 MT CO2e/year, EPA GHGRP"
            )
        elif cat == IssueCategory.REMEDIATION:
            framework_lines.append(
                "Remediation: 30 TAC 350 (TRRP), RCRA Corrective Action, "
                "risk-based closure standards, IDW management, institutional controls"
            )
        elif cat == IssueCategory.COASTAL_ZONE:
            framework_lines.append(
                "Coastal zone: Texas Coastal Management Program, GLO consistency determination, "
                "NRC Section 10/404 coordination, CMP federal consistency"
            )

    steps.append(ReasoningStep(
        step=2,
        analysis="Regulatory framework mapping:\n" + "\n".join(f"  - {fl}" for fl in framework_lines),
        confidence=0.80,
    ))

    # Step 3: Authority hierarchy
    steps.append(ReasoningStep(
        step=3,
        analysis=(
            "Authority hierarchy resolution: Federal statutes (CWA, CAA, RCRA, ESA) preempt "
            "state law where applicable. Texas has EPA-delegated programs for NPDES (TPDES), "
            "RCRA (30 TAC 335), and air quality (30 TAC 116). RRC retains jurisdiction over "
            "E&P waste and disposal wells under MOU with TCEQ. Conflicts between agencies "
            "resolved by: (1) federal preemption doctrine, (2) TCEQ-RRC MOU, (3) permit "
            "conditions taking precedence over general regulations."
        ),
        authority="Supremacy Clause, TCEQ-RRC MOU, EPA delegation agreements",
        confidence=0.85,
    ))

    # Step 4: Multi-agency jurisdiction
    relevant_agencies = []
    for cat in categories:
        if cat in (IssueCategory.AIR_QUALITY, IssueCategory.STORMWATER, IssueCategory.WATER_QUALITY):
            relevant_agencies.extend(["TCEQ", "EPA"])
        if cat in (IssueCategory.PRODUCED_WATER, IssueCategory.WASTE_MANAGEMENT):
            relevant_agencies.extend(["RRC", "TCEQ", "EPA"])
        if cat == IssueCategory.WETLANDS:
            relevant_agencies.extend(["USACE", "EPA"])
        if cat == IssueCategory.ENDANGERED_SPECIES:
            relevant_agencies.append("USFWS")
        if cat == IssueCategory.NORM_RADIATION:
            relevant_agencies.extend(["DSHS", "EPA"])
        if cat == IssueCategory.COASTAL_ZONE:
            relevant_agencies.append("GLO")
        if cat == IssueCategory.CONTAMINATED_SITES:
            relevant_agencies.extend(["TCEQ", "EPA"])
        if cat == IssueCategory.UNDERGROUND_INJECTION:
            relevant_agencies.extend(["RRC", "EPA"])
        if cat == IssueCategory.EMERGENCY_PLANNING:
            relevant_agencies.extend(["TCEQ", "EPA"])
    relevant_agencies = list(dict.fromkeys(relevant_agencies))  # dedupe preserving order

    steps.append(ReasoningStep(
        step=4,
        analysis=(
            f"Multi-agency jurisdiction: {len(relevant_agencies)} agencies with potential "
            f"jurisdiction: {', '.join(relevant_agencies)}. "
            "Compliance with one agency does not guarantee compliance with all. "
            "Overlapping enforcement authority means potential for parallel proceedings."
        ),
        confidence=0.80,
    ))

    # Step 5: Penalty exposure
    penalty_lines = []
    for cat in categories:
        if cat == IssueCategory.AIR_QUALITY:
            penalty_lines.append("CAA: up to $113,740/day per violation; TCEQ: up to $25,000/day")
        elif cat == IssueCategory.WATER_QUALITY:
            penalty_lines.append("CWA: up to $64,618/day per violation; TCEQ: up to $25,000/day")
        elif cat == IssueCategory.WASTE_MANAGEMENT:
            penalty_lines.append("RCRA: up to $75,867/day; criminal knowing: $50,000/day + 5 years")
        elif cat == IssueCategory.SPILL_PREVENTION:
            penalty_lines.append("SPCC: $25,000/day civil; OPA unlimited cleanup liability")
        elif cat == IssueCategory.WETLANDS:
            penalty_lines.append("Section 404: $25,000-$50,000/day; restoration orders")
        elif cat == IssueCategory.ENDANGERED_SPECIES:
            penalty_lines.append("ESA: $50,000 civil per violation; project injunctions")
        elif cat == IssueCategory.NORM_RADIATION:
            penalty_lines.append("NORM: $25,000/day unlicensed possession; CERCLA Superfund liability")
        elif cat == IssueCategory.CONTAMINATED_SITES:
            penalty_lines.append("CERCLA: strict, joint, and several liability; treble damages for non-cooperation")

    steps.append(ReasoningStep(
        step=5,
        analysis="Penalty exposure assessment:\n" + "\n".join(f"  - {pl}" for pl in penalty_lines),
        confidence=0.85,
    ))

    # Step 6: Interaction analysis
    if interactions:
        interaction_text = "\n".join(
            f"  - {i['from']} -> {i['to']}: {i['interaction'][:120]}" for i in interactions[:5]
        )
        steps.append(ReasoningStep(
            step=6,
            analysis=f"Cross-cutting interaction analysis ({len(interactions)} edges):\n{interaction_text}",
            confidence=0.75,
        ))
    else:
        steps.append(ReasoningStep(
            step=6,
            analysis="No significant cross-cutting regulatory interactions identified for this query.",
            confidence=0.80,
        ))

    # Step 7: Compliance pathway synthesis
    steps.append(ReasoningStep(
        step=7,
        analysis=(
            "Compliance pathway synthesis: (1) Identify all applicable permits and authorizations. "
            "(2) Determine which agency has primary jurisdiction for each requirement. "
            "(3) Prepare applications/plans in order of longest lead time first. "
            "(4) Implement best management practices during permitting process. "
            "(5) Establish internal compliance monitoring and recordkeeping. "
            "(6) Train personnel on regulatory obligations and reporting deadlines. "
            "(7) Budget for permit fees, monitoring costs, and potential mitigation."
        ),
        confidence=0.80,
    ))

    # Step 8: Confidence and limitations
    steps.append(ReasoningStep(
        step=8,
        analysis=(
            "Confidence assessment: This deep analysis is based on general regulatory framework "
            "knowledge. Site-specific factors (proximity to sensitive receptors, existing permits, "
            "violation history, specific emission/discharge quantities) may significantly alter "
            "compliance obligations. Recommend engaging qualified environmental consultant and "
            "legal counsel for site-specific compliance determination."
        ),
        confidence=0.65,
    ))

    return steps


# =============================================================================
# ZONED ANALYSIS (PLANNING / COMPLIANCE / AUDIT)
# =============================================================================


def build_zoned_analysis(
    query: EnvironmentalQuery,
    primary_doctrine: Optional[DoctrineBlock],
    categories: List[IssueCategory],
    agencies: List[str],
) -> List[ZonedConclusion]:
    """Generate position-zone-separated conclusions.

    Zones:
      PLANNING: Forward-looking, strategic compliance recommendations
      COMPLIANCE: Current regulatory requirements and obligations
      AUDIT: Retrospective, enforcement exposure, penalty analysis
    """
    conclusions: List[ZonedConclusion] = []

    topic = primary_doctrine.topic if primary_doctrine else "environmental compliance"
    conf = primary_doctrine.confidence if primary_doctrine else 0.6
    agency_str = ", ".join(agencies) if agencies else "TCEQ, EPA"

    # COMPLIANCE zone (always generated)
    compliance_caveats = [
        "Verify current regulatory requirements with applicable agency",
        "Individual permit conditions may impose stricter obligations",
    ]
    compliance_actions = []
    if primary_doctrine:
        compliance_actions = [
            f"Review {primary_doctrine.controlling_precedent or 'applicable regulation'}",
            "Confirm facility-specific applicability thresholds",
            "Document compliance status in facility records",
        ]
    else:
        compliance_actions = [
            "Research applicable regulations for identified issue categories",
            "Consult with regulatory agency for applicability determination",
            "Engage qualified environmental professional",
        ]
    conclusions.append(ZonedConclusion(
        zone=PositionZone.COMPLIANCE,
        conclusion=f"Environmental compliance requirement identified: {topic}. "
                    f"Regulated by {agency_str}.",
        confidence=conf,
        caveats=compliance_caveats,
        action_items=compliance_actions,
        responsible_agency=agencies[0] if agencies else "TCEQ",
    ))

    # PLANNING zone
    planning_caveats = [
        "Permit lead times can exceed 12-24 months for complex permits",
        "Regulatory requirements may change; monitor for updates",
    ]
    planning_actions = [
        "Conduct environmental due diligence before project commitment",
        f"Contact {agency_str} pre-application consultation",
        "Budget for environmental compliance costs (permits, monitoring, mitigation)",
        "Evaluate alternative project designs to minimize environmental impact",
    ]
    conclusions.append(ZonedConclusion(
        zone=PositionZone.PLANNING,
        conclusion=f"Planning consideration for {topic}: Proactive compliance strategy recommended. "
                    f"Engage environmental specialist early in project planning phase.",
        confidence=min(conf, 0.80),
        caveats=planning_caveats,
        action_items=planning_actions,
        responsible_agency=agencies[0] if agencies else "TCEQ",
    ))

    # AUDIT zone
    audit_caveats = [
        "Actual penalties depend on enforcement discretion factors",
        "Supplemental Environmental Projects (SEPs) may reduce penalties",
        "Compliance history affects penalty calculation",
    ]
    penalty_texts = []
    for cat in categories[:3]:
        if cat.value in ("air_quality",):
            penalty_texts.append("CAA: $113,740/day; TCEQ: $25,000/day")
        elif cat.value in ("water_quality", "stormwater"):
            penalty_texts.append("CWA: $64,618/day; TCEQ: $25,000/day")
        elif cat.value in ("waste_management",):
            penalty_texts.append("RCRA: $75,867/day")
        elif cat.value in ("spill_prevention",):
            penalty_texts.append("SPCC: $25,000/day + unlimited OPA cleanup")
        elif cat.value in ("wetlands",):
            penalty_texts.append("Section 404: $50,000/day + restoration")
    penalty_summary = "; ".join(penalty_texts) if penalty_texts else "Refer to penalty schedule"

    conclusions.append(ZonedConclusion(
        zone=PositionZone.AUDIT,
        conclusion=f"Enforcement exposure for {topic}: Penalty range: {penalty_summary}. "
                    f"Multi-agency enforcement risk from {agency_str}.",
        confidence=min(conf, 0.75),
        caveats=audit_caveats,
        action_items=[
            "Conduct internal environmental compliance audit",
            "Review inspection and violation history",
            "Assess potential penalty exposure using EPA BEN model",
            "Consider voluntary disclosure program if violations identified",
        ],
        responsible_agency=agencies[0] if agencies else "TCEQ",
    ))

    return conclusions


# =============================================================================
# THREE-LAYER RESPONSE ENGINE
# =============================================================================


def _compute_authority_weight(doctrine: DoctrineBlock) -> int:
    """Compute weighted authority score for a doctrine based on its primary authorities."""
    if not doctrine.primary_authority:
        return 50
    weights = []
    for auth in doctrine.primary_authority:
        best_match_weight = 50
        for key, weight in AUTHORITY_WEIGHTS.items():
            if key.lower() in auth.lower() or auth.lower() in key.lower():
                best_match_weight = max(best_match_weight, weight)
        weights.append(best_match_weight)
    return max(weights) if weights else 50


def _compute_determinism_hash(question: str, topic: str, confidence: float, mode: str) -> str:
    """Compute SHA-256 determinism hash for reproducibility."""
    payload = f"{question}|{topic}|{confidence}|{mode}|{ENGINE_VERSION}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _determine_responsible_agencies(doctrine: Optional[DoctrineBlock], categories: List[IssueCategory]) -> List[str]:
    """Determine responsible agencies from doctrine or issue categories."""
    agencies: List[str] = []
    if doctrine and doctrine.adversary_position:
        for name in ["TCEQ", "EPA", "RRC", "USACE", "USFWS", "GLO", "DSHS"]:
            if name.lower() in doctrine.adversary_position.lower():
                agencies.append(name)
    if not agencies:
        for cat in categories:
            if cat in (IssueCategory.AIR_QUALITY, IssueCategory.STORMWATER, IssueCategory.WATER_QUALITY):
                agencies.extend(["TCEQ", "EPA"])
            elif cat in (IssueCategory.PRODUCED_WATER, IssueCategory.WASTE_MANAGEMENT):
                agencies.extend(["RRC", "TCEQ"])
            elif cat == IssueCategory.WETLANDS:
                agencies.extend(["USACE", "EPA"])
            elif cat == IssueCategory.ENDANGERED_SPECIES:
                agencies.append("USFWS")
            elif cat == IssueCategory.NORM_RADIATION:
                agencies.extend(["DSHS", "EPA"])
            elif cat == IssueCategory.COASTAL_ZONE:
                agencies.append("GLO")
    return list(dict.fromkeys(agencies)) or ["TCEQ", "EPA"]


def _build_penalty_text(categories: List[IssueCategory]) -> str:
    """Build penalty summary text from issue categories."""
    penalty_parts = []
    for cat in categories[:3]:
        if cat == IssueCategory.AIR_QUALITY:
            penalty_parts.append("CAA: up to $113,740/day per violation")
        elif cat == IssueCategory.WATER_QUALITY:
            penalty_parts.append("CWA: up to $64,618/day per violation")
        elif cat == IssueCategory.WASTE_MANAGEMENT:
            penalty_parts.append("RCRA: up to $75,867/day per violation")
        elif cat == IssueCategory.SPILL_PREVENTION:
            penalty_parts.append("SPCC: $25,000/day + unlimited OPA 90 cleanup liability")
        elif cat == IssueCategory.WETLANDS:
            penalty_parts.append("Section 404: $25,000-$50,000/day + restoration orders")
        elif cat == IssueCategory.ENDANGERED_SPECIES:
            penalty_parts.append("ESA: $50,000 civil + criminal penalties + injunctions")
        elif cat == IssueCategory.NORM_RADIATION:
            penalty_parts.append("NORM: $25,000/day + CERCLA Superfund liability")
        elif cat == IssueCategory.CONTAMINATED_SITES:
            penalty_parts.append("CERCLA: strict, joint, and several liability")
    return "; ".join(penalty_parts) if penalty_parts else "TCEQ: $25,000/day per violation"


def three_layer_response(
    query: EnvironmentalQuery,
    normalized: NormalizationResult,
    trace_id: str,
) -> EnvironmentalResponse:
    """Execute the three-layer response engine.

    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning.
    Layer 2: Semantic Retrieval (200-700ms) - Vector/cloud search fallback.
    Layer 3: Deep Analysis (on-demand) - Multi-step reasoning chain.
    """
    start_time = time.time()
    metrics = get_metrics()
    metrics.query_start()

    try:
        # Classify issue categories for multi-doctrine decomposition
        categories = classify_issue_categories(normalized.normalized_text, normalized.keywords)
        interactions = find_relevant_interactions(categories)

        # --- LAYER 1: Doctrine Cache ---
        matched_doctrines = match_doctrines(normalized.normalized_text, normalized.keywords)
        if matched_doctrines:
            logger.info(f"[{trace_id}] Layer 1 HIT: {len(matched_doctrines)} doctrines matched")
            _coverage_map.record_hit([d.topic for d in matched_doctrines])
            response = _build_doctrine_response(
                query, matched_doctrines, normalized, trace_id, start_time, categories, interactions
            )
            metrics.record_query((time.time() - start_time) * 1000, True)
            metrics.query_end()
            return response

        # --- LAYER 2: Semantic Retrieval ---
        logger.info(f"[{trace_id}] Layer 1 MISS -> Layer 2 retrieval")
        _coverage_map.record_miss(query.question, normalized.keywords)

        search_results = vector_search(normalized.normalized_text, top_k=5)

        # Try cloud retriever if available and local search returned nothing
        if not search_results and _HAS_CLOUD_RETRIEVER:
            try:
                cloud_results = cloud_retrieve(normalized.normalized_text, top_k=5)
                if cloud_results:
                    search_results = cloud_results
                    logger.info(f"[{trace_id}] Cloud retriever returned {len(cloud_results)} results")
            except Exception as cloud_exc:
                logger.warning(f"[{trace_id}] Cloud retriever failed: {cloud_exc}")

        if search_results:
            logger.info(f"[{trace_id}] Layer 2 HIT: {len(search_results)} results")
            response = _build_retrieval_response(
                query, search_results, normalized, trace_id, start_time, categories, interactions
            )
            metrics.record_query((time.time() - start_time) * 1000, False)
            metrics.query_end()
            return response

        # --- LAYER 3: Deep Analysis ---
        logger.info(f"[{trace_id}] Layer 2 MISS -> Layer 3 deep analysis")
        response = _build_deep_analysis_response(
            query, normalized, trace_id, start_time, categories, interactions
        )
        metrics.record_query((time.time() - start_time) * 1000, False)
        metrics.query_end()
        return response

    except Exception as e:
        metrics.record_error(str(e))
        metrics.query_end()
        log_error(trace_id, ErrorDomain.QUERY_PROCESSING, str(e))
        raise


# =============================================================================
# LAYER 1: DOCTRINE RESPONSE BUILDER
# =============================================================================


def _build_doctrine_response(
    query: EnvironmentalQuery,
    doctrines: List[DoctrineBlock],
    normalized: NormalizationResult,
    trace_id: str,
    start_time: float,
    categories: List[IssueCategory],
    interactions: List[Dict[str, Any]],
) -> EnvironmentalResponse:
    """Build response from doctrine cache hit."""
    primary = doctrines[0]
    op_type = query.operator_type.value if query.operator_type else "operator"

    # Conclusion varies by response mode
    if query.mode == ResponseMode.FAST:
        conclusion = primary.conclusion_template
    elif query.mode == ResponseMode.DEFENSE:
        conclusion = (
            f"Regulatory analysis for {op_type} in {query.jurisdiction}: "
            f"{primary.conclusion_template} "
            f"Controlling authority: {primary.controlling_precedent or primary.primary_authority[0]}. "
            f"Confidence stratification: {primary.confidence_stratification.value}."
        )
    else:  # MEMO
        conclusion = (
            f"ENVIRONMENTAL COMPLIANCE MEMORANDUM\n"
            f"Re: {primary.topic}\n"
            f"Jurisdiction: {query.jurisdiction}\n"
            f"Operator Type: {op_type}\n\n"
            f"CONCLUSION: {primary.conclusion_template}\n\n"
            f"REGULATORY FRAMEWORK: {primary.reasoning_framework}\n\n"
            f"CONTROLLING AUTHORITY: {primary.controlling_precedent or 'See citations below'}"
        )

    reasoning = primary.reasoning_framework
    key_factors = primary.key_factors[:8]
    citations = [
        Citation(
            authority=auth.split("(")[0].strip() if "(" in auth else "Regulation",
            reference=auth,
            relevance="Primary environmental authority",
            weight=AUTHORITY_WEIGHTS.get(auth, 80),
        )
        for auth in primary.primary_authority
    ]

    # Additional citations from secondary doctrines
    for doctrine in doctrines[1:3]:
        for auth in doctrine.primary_authority[:1]:
            citations.append(Citation(
                authority=auth.split("(")[0].strip() if "(" in auth else "Regulation",
                reference=auth,
                relevance=f"Supporting authority ({doctrine.topic})",
                weight=AUTHORITY_WEIGHTS.get(auth, 70),
            ))

    permit_reqs = [f for f in primary.key_factors if any(
        kw in f.lower() for kw in ["permit", "authorization", "approval", "license", "noi"]
    )]
    deadlines = [f for f in primary.key_factors if any(
        kw in f.lower() for kw in ["deadline", "due", "within", "days", "year", "months", "annually"]
    )]

    agencies = _determine_responsible_agencies(primary, categories)
    penalty_text = _build_penalty_text(categories)
    auth_weight = _compute_authority_weight(primary)
    determinism_hash = _compute_determinism_hash(
        query.question, primary.topic, primary.confidence, query.mode.value
    )

    # Zoned analysis
    zoned = build_zoned_analysis(query, primary, categories, agencies)

    # Epistemic guardrails
    guardrail_result = apply_epistemic_guardrails(conclusion + " " + reasoning)

    # Drift check
    _drift_watcher.check_drift(primary.topic, primary.confidence)

    # Fact fragility
    fragility = None
    if query.include_fragility:
        fragility_score = compute_fact_fragility(
            doctrine_match=True,
            confidence=primary.confidence,
            category=categories[0],
            multi_agency=len(agencies) > 1,
        )
        fragility = fragility_score.to_dict()

    # Reasoning trace for defense/memo modes
    reasoning_trace = None
    if query.mode in (ResponseMode.DEFENSE, ResponseMode.MEMO) or query.include_trace:
        reasoning_trace = [
            ReasoningStep(step=1, analysis=f"Doctrine cache hit: {primary.topic}", confidence=primary.confidence),
            ReasoningStep(step=2, analysis=f"Matched {len(doctrines)} doctrine(s)", authority=primary.controlling_precedent),
            ReasoningStep(step=3, analysis=f"Authority weight: {auth_weight}/100"),
            ReasoningStep(step=4, analysis=f"Issue categories: {', '.join(c.value for c in categories)}"),
        ]

    # Coverage report
    coverage = {
        "triggered_doctrines": [d.topic for d in doctrines],
        "confidence_impact": "high" if len(doctrines) >= 2 else "moderate",
        "issue_categories": [c.value for c in categories],
        "interaction_count": len(interactions),
    }

    # Confidence tier
    conf_tier: Literal["high", "moderate", "requires_review"] = "high"
    if primary.confidence < 0.8:
        conf_tier = "moderate"
    if primary.confidence < 0.6:
        conf_tier = "requires_review"

    latency_ms = (time.time() - start_time) * 1000

    return EnvironmentalResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        citations=citations,
        permit_requirements=permit_reqs or None,
        compliance_deadlines=deadlines or None,
        penalties_for_violation=penalty_text,
        responsible_agencies=agencies,
        doctrine_match=True,
        confidence_tier=conf_tier,
        response_layer="doctrine",
        latency_ms=round(latency_ms, 2),
        conflict_detected=len(doctrines) > 1,
        authority_weight=auth_weight,
        confidence_stratification=primary.confidence_stratification.value,
        controlling_precedent=primary.controlling_precedent,
        determinism_hash=determinism_hash,
        reasoning_trace=reasoning_trace,
        zoned_analysis=[z.to_dict() for z in zoned],
        coverage_report=coverage,
        fact_fragility=fragility,
        issue_categories=[c.value for c in categories],
        interaction_edges=interactions[:5] if interactions else None,
        epistemic_guardrails=guardrail_result,
        disclosure_caveats=guardrail_result["disclosures"],
        limitations=[
            "Verify current regulations with applicable agency",
            "Site-specific conditions may alter compliance obligations",
            "This analysis does not constitute legal advice",
        ],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# =============================================================================
# LAYER 2: RETRIEVAL RESPONSE BUILDER
# =============================================================================


def _build_retrieval_response(
    query: EnvironmentalQuery,
    results: List[Dict[str, Any]],
    normalized: NormalizationResult,
    trace_id: str,
    start_time: float,
    categories: List[IssueCategory],
    interactions: List[Dict[str, Any]],
) -> EnvironmentalResponse:
    """Build response from semantic/cloud retrieval results."""
    top_result = results[0]
    content = top_result.get("content", "Environmental compliance analysis indicates specific obligations.")
    score = top_result.get("score", 0.0)

    conclusion = (
        f"Based on environmental regulatory database retrieval (relevance: {score:.3f}): {content}"
    )
    reasoning = (
        f"Analysis based on semantic retrieval from environmental knowledge base. "
        f"Matched {len(results)} relevant provisions across "
        f"{', '.join(c.value for c in categories)} categories."
    )
    key_factors = [
        "Environmental requirement identified through regulatory database",
        f"Top relevance score: {score:.3f}",
        f"Matched {len(results)} provisions",
        "Verify current regulatory status with applicable agency",
    ]
    citations = [
        Citation(
            authority="Regulation",
            reference=result.get("source", "Environmental Database"),
            relevance=f"Score: {result.get('score', 0.0):.3f}",
        )
        for result in results[:3]
    ]

    agencies = _determine_responsible_agencies(None, categories)
    penalty_text = _build_penalty_text(categories)
    determinism_hash = _compute_determinism_hash(
        query.question, "retrieval", score, query.mode.value
    )

    zoned = build_zoned_analysis(query, None, categories, agencies)
    guardrail_result = apply_epistemic_guardrails(conclusion)

    fragility = None
    if query.include_fragility:
        fragility_score = compute_fact_fragility(
            doctrine_match=False,
            confidence=score,
            category=categories[0],
            multi_agency=len(agencies) > 1,
        )
        fragility = fragility_score.to_dict()

    latency_ms = (time.time() - start_time) * 1000

    return EnvironmentalResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        citations=citations,
        penalties_for_violation=penalty_text,
        responsible_agencies=agencies,
        doctrine_match=False,
        confidence_tier="moderate",
        response_layer="retrieval",
        latency_ms=round(latency_ms, 2),
        confidence_stratification="best_practice",
        determinism_hash=determinism_hash,
        zoned_analysis=[z.to_dict() for z in zoned],
        fact_fragility=fragility,
        issue_categories=[c.value for c in categories],
        interaction_edges=interactions[:5] if interactions else None,
        epistemic_guardrails=guardrail_result,
        disclosure_caveats=guardrail_result["disclosures"],
        limitations=[
            "Based on semantic retrieval; requires verification with current regulations",
            "No doctrine cache match; confidence is moderate",
            "This analysis does not constitute legal advice",
        ],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# =============================================================================
# LAYER 3: DEEP ANALYSIS RESPONSE BUILDER
# =============================================================================


def _build_deep_analysis_response(
    query: EnvironmentalQuery,
    normalized: NormalizationResult,
    trace_id: str,
    start_time: float,
    categories: List[IssueCategory],
    interactions: List[Dict[str, Any]],
) -> EnvironmentalResponse:
    """Build response using multi-step deep analysis reasoning chain."""
    reasoning_steps = deep_analysis(query, normalized, categories, interactions)

    agencies = _determine_responsible_agencies(None, categories)
    penalty_text = _build_penalty_text(categories)

    cat_names = ", ".join(c.value.replace("_", " ") for c in categories)
    conclusion = (
        f"Deep analysis for environmental compliance query spanning {cat_names}. "
        f"Applicable agencies: {', '.join(agencies)}. "
        f"This query requires specific regulatory research with the applicable agencies. "
        f"Recommend engaging qualified environmental consultant for site-specific determination."
    )
    reasoning = (
        f"No direct doctrine match or semantic retrieval results. "
        f"8-step deep analysis performed covering issue identification, regulatory framework "
        f"mapping, authority hierarchy, multi-agency jurisdiction, penalty exposure, "
        f"cross-cutting interactions, compliance pathways, and confidence assessment. "
        f"Categories analyzed: {cat_names}."
    )
    key_factors = [
        f"Issue categories: {cat_names}",
        f"Jurisdiction: {query.jurisdiction}",
        f"Agencies with potential jurisdiction: {', '.join(agencies)}",
        f"Penalty exposure: {penalty_text}",
        "Site-specific assessment required",
        "Recommend qualified environmental consultant",
    ]
    citations = [
        Citation(
            authority="General Guidance",
            reference=f"{'TCEQ' if query.jurisdiction == 'Texas' else 'EPA'} Environmental Regulations",
            relevance="Primary environmental authority framework",
        )
    ]

    determinism_hash = _compute_determinism_hash(
        query.question, "deep_analysis", 0.5, query.mode.value
    )

    zoned = build_zoned_analysis(query, None, categories, agencies)
    guardrail_result = apply_epistemic_guardrails(conclusion)

    fragility = None
    if query.include_fragility:
        fragility_score = compute_fact_fragility(
            doctrine_match=False,
            confidence=0.5,
            category=categories[0],
            multi_agency=len(agencies) > 1,
        )
        fragility = fragility_score.to_dict()

    latency_ms = (time.time() - start_time) * 1000

    return EnvironmentalResponse(
        query_id=trace_id,
        question=query.question,
        mode=query.mode,
        conclusion=conclusion,
        reasoning=reasoning,
        key_factors=key_factors,
        citations=citations,
        penalties_for_violation=penalty_text,
        responsible_agencies=agencies,
        doctrine_match=False,
        confidence_tier="requires_review",
        response_layer="deep_analysis",
        latency_ms=round(latency_ms, 2),
        confidence_stratification="uncertain",
        determinism_hash=determinism_hash,
        reasoning_trace=reasoning_steps,
        zoned_analysis=[z.to_dict() for z in zoned],
        fact_fragility=fragility,
        issue_categories=[c.value for c in categories],
        interaction_edges=interactions[:5] if interactions else None,
        epistemic_guardrails=guardrail_result,
        disclosure_caveats=guardrail_result["disclosures"],
        limitations=[
            "No doctrine cache match or semantic retrieval results",
            "Deep analysis provides framework guidance only",
            "Requires regulatory consultation for compliance determination",
            "This analysis does not constitute legal advice",
        ],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# =============================================================================
# FASTAPI APPLICATION
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} topics loaded")
    logger.info(f"Authority weights: {len(AUTHORITY_WEIGHTS)} entries")
    logger.info(f"Agency directory: {len(AGENCY_DIRECTORY)} agencies")
    logger.info(f"Penalty schedule: {len(PENALTY_SCHEDULE)} violation types")
    logger.info(f"Interaction edges: {len(INTERACTION_EDGES)} cross-cutting rules")
    logger.info(f"Banned phrases: {len(BANNED_PHRASES)} epistemic guardrails")
    logger.info(f"Cloud retriever: {'available' if _HAS_CLOUD_RETRIEVER else 'unavailable'}")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_NAME} Engine",
    description=(
        "Professional-grade environmental compliance intelligence for oil and gas operations. "
        "Covers TCEQ, EPA, RCRA, CWA, CAA, SPCC, stormwater, produced water, NORM, "
        "air permits, water discharge, waste disposal, wetlands, and endangered species."
    ),
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


@app.post("/query", response_model=EnvironmentalResponse)
async def query_endpoint(query: EnvironmentalQuery):
    """Primary environmental compliance query endpoint."""
    trace_id = str(uuid.uuid4())
    telemetry = get_telemetry()
    tel_trace_id = trace_query(query.question)
    logger.info(f"[{trace_id}] Query: {query.question[:120]} | mode={query.mode.value}")

    try:
        normalized = normalize_semantics(query.question)
        logger.info(f"[{trace_id}] Normalized: {len(normalized.keywords)} keywords")
        response = three_layer_response(query, normalized, trace_id)

        # Record audit trail
        guardrail_result = response.epistemic_guardrails or {"violations": []}
        _audit_trail.record(
            trace_id=trace_id,
            question=query.question,
            mode=query.mode.value,
            jurisdiction=query.jurisdiction,
            operator_type=query.operator_type.value if query.operator_type else None,
            doctrine_match=response.doctrine_match,
            response_layer=response.response_layer,
            confidence_tier=response.confidence_tier,
            confidence_strat=response.confidence_stratification,
            latency_ms=response.latency_ms,
            determinism_hash=response.determinism_hash,
            guardrail_violations=guardrail_result.get("violations", []),
        )

        complete_trace(tel_trace_id)
        return response

    except Exception as e:
        logger.error(f"[{trace_id}] Error: {e}")
        log_error(tel_trace_id, ErrorDomain.QUERY_PROCESSING, str(e))
        complete_trace(tel_trace_id)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    metrics = get_metrics()
    uptime = time.time() - _start_time
    coverage = _coverage_map.get_coverage_report()
    drift_report = _drift_watcher.get_drift_report()
    drift_status = "stable" if drift_report["drifted_count"] == 0 else f"{drift_report['drifted_count']} drifted"

    try:
        import psutil
        proc = psutil.Process()
        mem_info = proc.memory_info()
        mem_used = round(mem_info.rss / 1024 / 1024, 2)
        mem_available = round(psutil.virtual_memory().available / 1024 / 1024, 2)
        mem_percent = round(proc.memory_percent(), 2)
    except ImportError:
        mem_used, mem_available, mem_percent = 0.0, 0.0, 0.0

    status: Literal["healthy", "degraded", "unhealthy"] = "healthy"
    error_stats = metrics.get_error_stats()
    if error_stats["last_hour"] > 10:
        status = "degraded"
    if error_stats["last_hour"] > 50:
        status = "unhealthy"

    return HealthResponse(
        status=status,
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        uptime_seconds=round(uptime, 2),
        api_latency=metrics.get_latency_stats(),
        doctrine_cache={
            "status": "operational",
            "topics": len(DOCTRINE_CACHE),
            "hit_rate": metrics.get_doctrine_hit_rate(),
            "hits": metrics.doctrine_hits,
            "misses": metrics.doctrine_misses,
        },
        vector_db={
            "status": "operational",
            "cloud_retriever": _HAS_CLOUD_RETRIEVER,
        },
        memory_mb={"used": mem_used, "available": mem_available, "percent": mem_percent},
        active_queries=metrics.active_queries,
        queries_last_hour=metrics.queries_last_hour(),
        error_rate=error_stats,
        coverage_ratio=coverage["coverage_ratio"],
        drift_status=drift_status,
        cloud_retriever_available=_HAS_CLOUD_RETRIEVER,
    )


@app.get("/metrics")
async def metrics_endpoint():
    """Full metrics snapshot."""
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "uptime_seconds": round(time.time() - _start_time, 2),
        "metrics": _metrics.to_dict(),
        "audit_stats": _audit_trail.stats(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/drift")
async def drift_endpoint():
    """Doctrine drift monitoring report."""
    return _drift_watcher.get_drift_report()


@app.get("/coverage")
async def coverage_endpoint():
    """Doctrine coverage map and gap detection."""
    return _coverage_map.get_coverage_report()


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics with metadata."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence,
                "confidence_stratification": d.confidence_stratification.value,
                "controlling_precedent": d.controlling_precedent,
                "burden_holder": d.burden_holder,
                "entity_scope": d.entity_scope,
                "authority_count": len(d.primary_authority),
            }
            for d in DOCTRINE_CACHE
        ],
    }


@app.get("/authorities")
async def list_authorities():
    """List all authority weights and agency directory."""
    return {
        "authority_weights": AUTHORITY_WEIGHTS,
        "agency_directory": AGENCY_DIRECTORY,
        "penalty_schedule": {
            k: {
                "statute": v["statute"],
                "max_per_day": v.get("max_per_day", "varies"),
                "notes": v.get("notes", ""),
            }
            for k, v in PENALTY_SCHEDULE.items()
        },
        "total_authorities": len(AUTHORITY_WEIGHTS),
        "total_agencies": len(AGENCY_DIRECTORY),
        "total_penalty_types": len(PENALTY_SCHEDULE),
    }


@app.get("/guardrails")
async def guardrails_endpoint():
    """Epistemic guardrails configuration."""
    return {
        "banned_phrases": BANNED_PHRASES,
        "disclosure_caveats": DISCLOSURE_CAVEATS,
        "total_banned": len(BANNED_PHRASES),
        "total_caveats": len(DISCLOSURE_CAVEATS),
    }


@app.get("/audit-trail")
async def audit_trail_endpoint(count: int = 50):
    """Recent audit trail entries."""
    return {
        "entries": _audit_trail.recent(min(count, 200)),
        "stats": _audit_trail.stats(),
    }


@app.get("/interactions")
async def interactions_endpoint():
    """Cross-cutting regulatory interaction edges."""
    return {
        "total_edges": len(INTERACTION_EDGES),
        "edges": [
            {
                "from": e["from"].value,
                "to": e["to"].value,
                "interaction": e["interaction"],
                "weight": e["weight"],
            }
            for e in INTERACTION_EDGES
        ],
        "issue_categories": [c.value for c in IssueCategory],
    }


@app.get("/term-map")
async def term_map_endpoint():
    """Environmental term normalization mapping."""
    return {
        "total_terms": len(ENVIRONMENTAL_TERM_MAP),
        "terms": ENVIRONMENTAL_TERM_MAP,
    }


@app.get("/penalties")
async def penalties_endpoint():
    """Full penalty schedule for environmental violations."""
    return {
        "total_violation_types": len(PENALTY_SCHEDULE),
        "schedule": PENALTY_SCHEDULE,
    }


# =============================================================================
# ENTRYPOINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT)
