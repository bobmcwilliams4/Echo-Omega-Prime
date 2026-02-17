"""
E01 Document Classifier Engine
===============================
Production-grade document classification engine implementing all 20 TIE
components. Classifies incoming documents (deeds, leases, court orders,
permits, assignments, mortgages, affidavits, easements, etc.) using
supervised LLM with rule-based fallback.

Port: 8601
Engine: E01 Document Classifier
Version: 1.0.0

TIE-20 Components:
    1.  three_layer_response
    2.  response_modes (FAST, DEFENSE, MEMO)
    3.  doctrine_cache (30+ document classification rules)
    4.  authority_hardening
    5.  confidence_stratification
    6.  semantic_normalization
    7.  vector_search
    8.  telemetry
    9.  drift_watcher
    10. coverage_map
    11. metrics_collector
    12. health_endpoint
    13. zoned_analysis
    14. fact_fragility_scoring
    15. audit_trail_jsonl
    16. determinism_hash_sha256
    17. fastapi_server
    18. loguru_logging
    19. multi_doctrine_decomposition
    20. deep_analysis_mode
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import re
import sys
import time
import uuid
from collections import Counter, OrderedDict, defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

_shared = ENGINE_DIR.parent / "_shared"
sys.path.insert(0, str(_shared))

try:
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None  # type: ignore[assignment,misc]
    logger.warning("cloud_retriever not available - cloud features disabled")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "E01"
ENGINE_NAME = "Document Classifier"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8601
STARTUP_TS = datetime.now(timezone.utc).isoformat()

LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit_trail.jsonl"

logger.add(
    LOG_DIR / "e01_classifier.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ConfidenceStratum(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class ClassificationTier(str, Enum):
    DOCTRINE_CACHE = "DOCTRINE_CACHE"
    SEMANTIC_RETRIEVAL = "SEMANTIC_RETRIEVAL"
    DEEP_ANALYSIS = "DEEP_ANALYSIS"


# ═══════════════════════════════════════════════════════════════════════════
# DOCUMENT TYPE TAXONOMY (35 types across 10 categories)
# ═══════════════════════════════════════════════════════════════════════════

class DocCategory(str, Enum):
    DEED = "DEED"
    LEASE = "LEASE"
    ASSIGNMENT = "ASSIGNMENT"
    MORTGAGE = "MORTGAGE"
    COURT_ORDER = "COURT_ORDER"
    AFFIDAVIT = "AFFIDAVIT"
    RIGHT_OF_WAY = "RIGHT_OF_WAY"
    EASEMENT = "EASEMENT"
    AGREEMENT = "AGREEMENT"
    CORPORATE = "CORPORATE"
    MINERAL = "MINERAL"
    PERMIT = "PERMIT"
    MISCELLANEOUS = "MISCELLANEOUS"


DOCUMENT_TYPES: Dict[str, Dict[str, Any]] = {
    # --- DEEDS ---
    "GENERAL_WARRANTY_DEED": {
        "category": DocCategory.DEED,
        "display": "General Warranty Deed",
        "description": "Conveyance with full covenants of title including seisin, quiet enjoyment, against encumbrances, warranty, and further assurances.",
        "keywords": ["general warranty", "warrant and defend", "covenants of seisin", "grant sell convey", "grantor to grantee"],
        "regex": [r"general\s+warranty\s+deed", r"warrant\s+and\s+(forever\s+)?defend", r"covenant[s]?\s+of\s+seisin"],
        "weight": 1.0,
    },
    "SPECIAL_WARRANTY_DEED": {
        "category": DocCategory.DEED,
        "display": "Special Warranty Deed",
        "description": "Conveyance with limited warranties only against grantor's own acts, not predecessors.",
        "keywords": ["special warranty", "by through or under", "limited warranty", "bargain sell convey"],
        "regex": [r"special\s+warranty\s+deed", r"by[,]?\s+through[,]?\s+or\s+under\s+(the\s+)?grantor"],
        "weight": 1.0,
    },
    "QUITCLAIM_DEED": {
        "category": DocCategory.DEED,
        "display": "Quitclaim Deed",
        "description": "Conveyance of whatever interest grantor may hold, with no warranties.",
        "keywords": ["quitclaim", "quit claim", "remise release", "right title and interest"],
        "regex": [r"quit[\s-]?claim\s+deed", r"remise[,]?\s+release[,]?\s+and\s+quit[\s-]?claim"],
        "weight": 0.95,
    },
    "CORRECTION_DEED": {
        "category": DocCategory.DEED,
        "display": "Correction Deed",
        "description": "Instrument correcting a scrivener's error in a previously recorded deed.",
        "keywords": ["correction deed", "corrective deed", "scrivener's error", "reformed", "re-recorded"],
        "regex": [r"correction\s+deed", r"corrective\s+(instrument|deed)", r"scrivener.s\s+error"],
        "weight": 0.9,
    },
    "GIFT_DEED": {
        "category": DocCategory.DEED,
        "display": "Gift Deed",
        "description": "Deed conveying property as a gift, typically with recital of love and affection as consideration.",
        "keywords": ["gift deed", "love and affection", "natural love", "donative", "no monetary consideration"],
        "regex": [r"gift\s+deed", r"love\s+and\s+affection", r"natural\s+love\s+and\s+affection"],
        "weight": 0.9,
    },
    "MINERAL_DEED": {
        "category": DocCategory.MINERAL,
        "display": "Mineral Deed",
        "description": "Conveyance of subsurface mineral estate or fractional mineral interest.",
        "keywords": ["mineral deed", "mineral interest", "mineral estate", "minerals in and under", "undivided mineral"],
        "regex": [r"mineral\s+deed", r"mineral\s+(interest|estate|right)", r"oil[,]?\s+gas[,]?\s+and\s+(other\s+)?minerals"],
        "weight": 1.0,
    },
    "ROYALTY_DEED": {
        "category": DocCategory.MINERAL,
        "display": "Royalty Deed",
        "description": "Conveyance of royalty interest in production without executive or working interest rights.",
        "keywords": ["royalty deed", "royalty interest", "non-participating royalty", "overriding royalty"],
        "regex": [r"royalty\s+deed", r"(non[\s-]?participating\s+)?royalty\s+interest"],
        "weight": 1.0,
    },
    # --- LEASES ---
    "OIL_GAS_LEASE": {
        "category": DocCategory.LEASE,
        "display": "Oil and Gas Lease",
        "description": "Lease granting exploration and production rights for hydrocarbons, typically with primary term, royalty clause, and habendum.",
        "keywords": ["oil and gas lease", "lessee", "lessor", "royalty", "primary term", "habendum", "drilling operations", "paid-up lease"],
        "regex": [r"oil\s+(and|&)\s+gas\s+lease", r"habendum\s+clause", r"drilling\s+operations?\s+(shall|may)\s+commence"],
        "weight": 1.0,
    },
    "SURFACE_LEASE": {
        "category": DocCategory.LEASE,
        "display": "Surface Lease",
        "description": "Lease for surface use of land (tank batteries, roads, well pads, SWD facilities).",
        "keywords": ["surface lease", "surface use", "surface damage", "tank battery", "well pad", "saltwater disposal"],
        "regex": [r"surface\s+(use\s+)?lease", r"surface\s+only", r"tank\s+batter(y|ies)"],
        "weight": 0.95,
    },
    "WIND_SOLAR_LEASE": {
        "category": DocCategory.LEASE,
        "display": "Wind/Solar Lease",
        "description": "Renewable energy lease for wind turbines or solar panel installation.",
        "keywords": ["wind lease", "solar lease", "wind energy", "wind turbine", "photovoltaic", "renewable energy lease"],
        "regex": [r"(wind|solar)\s+(energy\s+)?lease", r"wind\s+turbine", r"photovoltaic"],
        "weight": 0.95,
    },
    "AGRICULTURAL_LEASE": {
        "category": DocCategory.LEASE,
        "display": "Agricultural Lease",
        "description": "Farm or ranch lease for crop production, grazing, or ranching activities.",
        "keywords": ["agricultural lease", "farm lease", "grazing lease", "ranch lease", "crop share", "cash rent"],
        "regex": [r"(agricultural|farm|grazing|ranch)\s+lease", r"crop\s+share", r"pasture\s+land"],
        "weight": 0.9,
    },
    # --- ASSIGNMENTS ---
    "ASSIGNMENT_ORI": {
        "category": DocCategory.ASSIGNMENT,
        "display": "Assignment of Overriding Royalty Interest",
        "description": "Transfer of an overriding royalty interest (ORRI) carved from the working interest under an existing lease.",
        "keywords": ["assignment of overriding royalty", "ORRI", "overriding royalty interest", "override"],
        "regex": [r"assignment\s+of\s+overriding\s+royalty", r"override\s+royalty\s+interest", r"\bORRI\b"],
        "weight": 1.0,
    },
    "ASSIGNMENT_WI": {
        "category": DocCategory.ASSIGNMENT,
        "display": "Assignment of Working Interest",
        "description": "Transfer of working interest (operating rights and cost-bearing obligation) in an oil and gas lease.",
        "keywords": ["assignment of working interest", "operating rights", "cost-bearing", "working interest"],
        "regex": [r"assignment\s+of\s+working\s+interest", r"operating\s+rights?\s+(and|&)\s+interest"],
        "weight": 1.0,
    },
    "PARTIAL_ASSIGNMENT": {
        "category": DocCategory.ASSIGNMENT,
        "display": "Partial Assignment",
        "description": "Assignment of a fractional or undivided portion of interest in an oil and gas lease.",
        "keywords": ["partial assignment", "undivided interest", "fractional interest", "partial conveyance"],
        "regex": [r"partial\s+assignment", r"undivided\s+\d+[./]\d*\s+(interest|portion)"],
        "weight": 0.9,
    },
    # --- MORTGAGE / LIEN ---
    "DEED_OF_TRUST": {
        "category": DocCategory.MORTGAGE,
        "display": "Deed of Trust",
        "description": "Three-party security instrument (trustor, trustee, beneficiary) securing a promissory note against real property.",
        "keywords": ["deed of trust", "trustor", "trustee", "beneficiary", "promissory note", "power of sale"],
        "regex": [r"deed\s+of\s+trust", r"trustor.*trustee.*beneficiary", r"power\s+of\s+sale"],
        "weight": 1.0,
    },
    "RELEASE_OF_LIEN": {
        "category": DocCategory.MORTGAGE,
        "display": "Release of Lien",
        "description": "Instrument releasing a previously recorded lien, mortgage, or deed of trust from the property.",
        "keywords": ["release of lien", "satisfaction", "reconveyance", "lien released", "mortgage satisfied"],
        "regex": [r"release\s+of\s+(lien|mortgage|deed\s+of\s+trust)", r"satisfaction\s+of\s+(mortgage|lien)", r"full\s+reconveyance"],
        "weight": 1.0,
    },
    # --- COURT ORDERS ---
    "PROBATE_ORDER": {
        "category": DocCategory.COURT_ORDER,
        "display": "Probate Court Order",
        "description": "Court order in probate proceedings, including orders admitting will, appointing executor/administrator, or approving distribution.",
        "keywords": ["probate", "decedent", "executor", "administrator", "letters testamentary", "intestate", "estate of"],
        "regex": [r"(order|decree)\s+(of|in)\s+probate", r"letters\s+testamentary", r"estate\s+of\s+.+deceased"],
        "weight": 1.0,
    },
    "DIVORCE_DECREE": {
        "category": DocCategory.COURT_ORDER,
        "display": "Divorce Decree / Property Division",
        "description": "Final decree of divorce with property division provisions affecting real property.",
        "keywords": ["divorce", "dissolution of marriage", "property division", "community property", "separate property"],
        "regex": [r"(final\s+)?decree\s+of\s+divorce", r"dissolution\s+of\s+marriage", r"property\s+division"],
        "weight": 1.0,
    },
    "PARTITION_ORDER": {
        "category": DocCategory.COURT_ORDER,
        "display": "Partition Order",
        "description": "Court order partitioning co-owned property in kind or by sale.",
        "keywords": ["partition", "partition in kind", "partition by sale", "co-tenancy", "cotenant"],
        "regex": [r"(order|judgment)\s+(of|for)\s+partition", r"partition\s+in\s+kind", r"partition\s+by\s+sale"],
        "weight": 0.95,
    },
    "RECEIVERSHIP_ORDER": {
        "category": DocCategory.COURT_ORDER,
        "display": "Receivership Order",
        "description": "Court order appointing a receiver to manage property or business operations.",
        "keywords": ["receivership", "receiver appointed", "court-appointed receiver", "custodian"],
        "regex": [r"(order\s+)?appoint(ing|ment\s+of)\s+receiver", r"receivership"],
        "weight": 0.95,
    },
    # --- AFFIDAVITS ---
    "AFFIDAVIT_HEIRSHIP": {
        "category": DocCategory.AFFIDAVIT,
        "display": "Affidavit of Heirship",
        "description": "Sworn statement identifying heirs of a decedent for purposes of establishing title succession without probate.",
        "keywords": ["affidavit of heirship", "heirs at law", "decedent", "died intestate", "heir determination"],
        "regex": [r"affidavit\s+of\s+heirship", r"heirs?\s+at\s+law", r"died\s+intestate"],
        "weight": 1.0,
    },
    "AFFIDAVIT_IDENTITY": {
        "category": DocCategory.AFFIDAVIT,
        "display": "Affidavit of Identity / Name",
        "description": "Sworn statement confirming that different name variations refer to the same person.",
        "keywords": ["affidavit of identity", "same person", "also known as", "AKA", "name variation"],
        "regex": [r"affidavit\s+of\s+(identity|name)", r"(one\s+and\s+the\s+)?same\s+person", r"also\s+known\s+as"],
        "weight": 0.95,
    },
    "AFFIDAVIT_NON_PRODUCTION": {
        "category": DocCategory.AFFIDAVIT,
        "display": "Affidavit of Non-Production",
        "description": "Sworn statement that no production has occurred on a tract, often used to terminate a lease.",
        "keywords": ["affidavit of non-production", "no production", "lease expired", "cessation of production"],
        "regex": [r"affidavit\s+of\s+non[\s-]?production", r"no\s+(oil\s+(and|&)\s+gas\s+)?production", r"cessation\s+of\s+production"],
        "weight": 0.95,
    },
    # --- RIGHT OF WAY ---
    "ROW_PIPELINE": {
        "category": DocCategory.RIGHT_OF_WAY,
        "display": "Pipeline Right of Way",
        "description": "Grant of right of way for pipeline construction and operation across the surface estate.",
        "keywords": ["pipeline right of way", "pipeline easement", "lay construct operate", "gathering line", "transmission line"],
        "regex": [r"pipeline\s+right[\s-]?of[\s-]?way", r"lay[,]?\s+construct[,]?\s+(and\s+)?operate\s+.*(pipeline|line)"],
        "weight": 1.0,
    },
    "ROW_ROAD": {
        "category": DocCategory.RIGHT_OF_WAY,
        "display": "Road Right of Way",
        "description": "Grant of right of way for road construction and access purposes.",
        "keywords": ["road right of way", "road easement", "access road", "public road", "county road"],
        "regex": [r"road\s+right[\s-]?of[\s-]?way", r"access\s+road\s+(easement|right)"],
        "weight": 0.9,
    },
    "ROW_UTILITY": {
        "category": DocCategory.RIGHT_OF_WAY,
        "display": "Utility Right of Way / Easement",
        "description": "Grant of right of way for electric, water, telephone, or other utility lines.",
        "keywords": ["utility easement", "power line", "electric line", "water line", "telephone easement"],
        "regex": [r"utility\s+(easement|right[\s-]?of[\s-]?way)", r"(electric|power|water|telephone)\s+(line\s+)?(easement|right)"],
        "weight": 0.9,
    },
    # --- EASEMENTS ---
    "EASEMENT_SURFACE": {
        "category": DocCategory.EASEMENT,
        "display": "Surface Easement",
        "description": "Grant of easement for surface use such as ingress/egress, parking, or drainage.",
        "keywords": ["surface easement", "ingress egress", "access easement", "drainage easement"],
        "regex": [r"surface\s+easement", r"(ingress|egress)\s+(and|&)\s+(egress|ingress)", r"drainage\s+easement"],
        "weight": 0.9,
    },
    "EASEMENT_SUBSURFACE": {
        "category": DocCategory.EASEMENT,
        "display": "Subsurface Easement",
        "description": "Easement for subsurface activities such as horizontal drilling, bore, or tunneling.",
        "keywords": ["subsurface easement", "horizontal drilling", "bore", "tunneling", "underground"],
        "regex": [r"subsurface\s+easement", r"horizontal\s+(drill|bore)", r"underground\s+easement"],
        "weight": 0.9,
    },
    # --- AGREEMENTS ---
    "DIVISION_ORDER": {
        "category": DocCategory.AGREEMENT,
        "display": "Division Order",
        "description": "Document directing purchaser of oil/gas to distribute proceeds among interest owners per stated decimal interests.",
        "keywords": ["division order", "decimal interest", "proceeds", "purchaser", "revenue distribution"],
        "regex": [r"division\s+order", r"decimal\s+interest", r"revenue\s+(distribution|allocation)"],
        "weight": 1.0,
    },
    "POOLING_AGREEMENT": {
        "category": DocCategory.AGREEMENT,
        "display": "Pooling Agreement",
        "description": "Agreement combining separate tracts or interests into a single pooled unit for drilling and production.",
        "keywords": ["pooling agreement", "pooled unit", "pooling designation", "force pooling", "voluntary pooling"],
        "regex": [r"pooling\s+(agreement|designation|declaration)", r"pooled\s+unit", r"force[\s-]?pool"],
        "weight": 1.0,
    },
    "UNITIZATION_AGREEMENT": {
        "category": DocCategory.AGREEMENT,
        "display": "Unitization Agreement",
        "description": "Agreement combining multiple leases/tracts into a single unit for secondary/enhanced recovery operations.",
        "keywords": ["unitization", "unit agreement", "unit operations", "secondary recovery", "enhanced recovery", "waterflood"],
        "regex": [r"unitization\s+agreement", r"unit\s+(agreement|operations)", r"(secondary|enhanced)\s+recovery"],
        "weight": 1.0,
    },
    "RATIFICATION": {
        "category": DocCategory.AGREEMENT,
        "display": "Ratification",
        "description": "Instrument ratifying and confirming an existing lease or conveyance, typically by previously omitted interest owner.",
        "keywords": ["ratification", "ratify and confirm", "ratification of lease", "confirmation"],
        "regex": [r"ratification\s+(of\s+)?(oil\s+(and|&)\s+gas\s+)?lease", r"ratif(y|ies)\s+and\s+confirm"],
        "weight": 0.95,
    },
    "SUBORDINATION": {
        "category": DocCategory.AGREEMENT,
        "display": "Subordination Agreement",
        "description": "Agreement subordinating one interest to another, establishing priority of liens or interests.",
        "keywords": ["subordination", "subordinate", "junior lien", "priority", "subordination agreement"],
        "regex": [r"subordination\s+agreement", r"subordinate[s]?\s+(its?|the)\s+(lien|interest)"],
        "weight": 0.95,
    },
    "STIPULATION_OF_INTEREST": {
        "category": DocCategory.AGREEMENT,
        "display": "Stipulation of Interest",
        "description": "Agreement between parties stipulating ownership percentages in minerals or production.",
        "keywords": ["stipulation of interest", "ownership percentage", "agreed interest", "stipulated interest"],
        "regex": [r"stipulation\s+of\s+interest", r"stipulated\s+(ownership|interest)"],
        "weight": 0.9,
    },
    # --- CORPORATE ---
    "POWER_OF_ATTORNEY": {
        "category": DocCategory.CORPORATE,
        "display": "Power of Attorney",
        "description": "Instrument granting authority to an agent to act on behalf of the principal in real property matters.",
        "keywords": ["power of attorney", "attorney-in-fact", "agent", "principal", "POA", "durable power"],
        "regex": [r"power\s+of\s+attorney", r"attorney[\s-]?in[\s-]?fact", r"durable\s+power"],
        "weight": 1.0,
    },
    "CERTIFICATE_OF_FORMATION": {
        "category": DocCategory.CORPORATE,
        "display": "Certificate of Formation / Articles",
        "description": "Organizational document forming an LLC, corporation, or partnership that may hold title to real property.",
        "keywords": ["certificate of formation", "articles of incorporation", "articles of organization", "LLC", "corporation"],
        "regex": [r"certificate\s+of\s+formation", r"articles\s+of\s+(incorporation|organization)"],
        "weight": 0.9,
    },
    "UCC_FILING": {
        "category": DocCategory.CORPORATE,
        "display": "UCC Financing Statement",
        "description": "Uniform Commercial Code financing statement perfecting a security interest in personal property or fixtures.",
        "keywords": ["UCC", "financing statement", "UCC-1", "secured party", "debtor", "collateral", "fixture filing"],
        "regex": [r"UCC[\s-]?\d?\s+(financing\s+)?statement", r"fixture\s+filing", r"secured\s+party.*debtor"],
        "weight": 1.0,
    },
    # --- PERMITS ---
    "WATER_RIGHTS_PERMIT": {
        "category": DocCategory.PERMIT,
        "display": "Water Rights Permit",
        "description": "Governmental permit for appropriation, diversion, or use of water resources.",
        "keywords": ["water rights", "water permit", "appropriation", "diversion", "groundwater"],
        "regex": [r"water\s+rights?\s+permit", r"appropriation\s+of\s+water", r"groundwater\s+(use\s+)?permit"],
        "weight": 0.9,
    },
    "SURFACE_DAMAGE_RELEASE": {
        "category": DocCategory.MISCELLANEOUS,
        "display": "Surface Damage Release",
        "description": "Release by surface owner of claims for surface damage caused by oil and gas operations.",
        "keywords": ["surface damage", "damage release", "surface use agreement", "damages paid", "surface restoration"],
        "regex": [r"surface\s+damage\s+(release|agreement)", r"surface\s+use\s+(and\s+damage\s+)?agreement"],
        "weight": 0.9,
    },
    "PRODUCTION_PAYMENT": {
        "category": DocCategory.MINERAL,
        "display": "Production Payment",
        "description": "Conveyance of a right to receive a specified amount from production proceeds, terminating once satisfied.",
        "keywords": ["production payment", "volumetric production", "dollar-denominated production", "carved-out production"],
        "regex": [r"production\s+payment", r"volumetric\s+production\s+payment"],
        "weight": 0.9,
    },
}

# Compile all regex patterns once at module load
_COMPILED_PATTERNS: Dict[str, List[re.Pattern]] = {}
for _dt, _info in DOCUMENT_TYPES.items():
    _COMPILED_PATTERNS[_dt] = [re.compile(p, re.IGNORECASE) for p in _info["regex"]]


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Document text to classify")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(AnalysisZone.REPORTING, description="Analysis zone")
    top_k: int = Field(5, ge=1, le=35, description="Number of top candidates to return")
    include_reasoning: bool = Field(False, description="Include reasoning chain in response")
    session_id: Optional[str] = Field(None, description="Optional session tracking ID")


class ClassificationCandidate(BaseModel):
    doc_type: str = Field(..., description="Document type key")
    display_name: str = Field(..., description="Human-readable document type name")
    category: str = Field(..., description="Document category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")
    stratum: ConfidenceStratum = Field(..., description="Confidence stratification")
    matched_keywords: List[str] = Field(default_factory=list)
    matched_patterns: List[str] = Field(default_factory=list)
    feature_scores: Dict[str, float] = Field(default_factory=dict)


class StructuralFeatures(BaseModel):
    estimated_pages: int = Field(0, description="Estimated page count based on text length")
    has_legal_description: bool = Field(False)
    has_recording_info: bool = Field(False)
    has_signature_block: bool = Field(False)
    has_notary_block: bool = Field(False)
    has_consideration: bool = Field(False)
    has_granting_clause: bool = Field(False)
    has_habendum: bool = Field(False)
    extracted_county: Optional[str] = None
    extracted_state: Optional[str] = None
    extracted_instrument_no: Optional[str] = None
    extracted_book_page: Optional[str] = None
    header_text: Optional[str] = None
    word_count: int = 0


class ClassificationResult(BaseModel):
    query_id: str = Field(..., description="Unique classification ID")
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    primary_type: str = Field(..., description="Best classification")
    primary_display: str = Field(..., description="Human-readable best classification")
    primary_confidence: float = Field(..., description="Best confidence score")
    primary_stratum: ConfidenceStratum = Field(...)
    candidates: List[ClassificationCandidate] = Field(default_factory=list)
    tier_used: ClassificationTier = Field(...)
    structural_features: StructuralFeatures = Field(default_factory=StructuralFeatures)
    mode: ResponseMode = Field(...)
    zone: AnalysisZone = Field(...)
    reasoning: Optional[List[str]] = None
    determinism_hash: str = Field(..., description="SHA-256 reproducibility hash")
    latency_ms: float = Field(0.0)
    fragility_score: float = Field(0.0, description="Classification fragility 0-1")
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    startup_time: str = STARTUP_TS
    document_types_loaded: int = len(DOCUMENT_TYPES)
    compiled_patterns: int = sum(len(v) for v in _COMPILED_PATTERNS.values())
    total_classifications: int = 0
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    drift_alerts: int = 0
    coverage_pct: float = 0.0


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = Field(ResponseMode.FAST)
    zone: AnalysisZone = Field(AnalysisZone.REPORTING)
    top_k: int = Field(5, ge=1, le=35)
    include_reasoning: bool = Field(False)
    session_id: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# TIE-03: DOCTRINE CACHE (30+ pre-compiled classification rules)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: float
    stratum: ConfidenceStratum
    category: DocCategory
    doc_type_key: str
    counter_indicators: List[str] = dc_field(default_factory=list)

    def matches(self, text_lower: str) -> Tuple[bool, float, List[str]]:
        """Check if doctrine matches the text. Returns (matched, score, matched_keywords)."""
        matched_kw: List[str] = []
        for kw in self.keywords:
            if kw.lower() in text_lower:
                matched_kw.append(kw)
        if not matched_kw:
            return False, 0.0, []
        base_score = len(matched_kw) / len(self.keywords)
        # Penalize if counter-indicators found
        counter_hits = sum(1 for ci in self.counter_indicators if ci.lower() in text_lower)
        penalty = counter_hits * 0.15
        final_score = max(0.0, min(1.0, base_score * self.confidence - penalty))
        return final_score > 0.15, final_score, matched_kw


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="General Warranty Deed Classification",
        keywords=["general warranty deed", "warrant and defend", "covenants of seisin", "grant sell and convey", "grantee"],
        conclusion_template="Document classified as General Warranty Deed based on warranty covenants and granting language.",
        reasoning_framework="A general warranty deed is identified by six covenants of title: seisin, right to convey, against encumbrances, quiet enjoyment, warranty, and further assurances. The grantor warrants title against all claims, not just those arising during grantor's ownership.",
        key_factors=["Full warranty covenants", "Granting clause", "Consideration recital", "Legal description"],
        primary_authority=["Tex. Prop. Code 5.022", "UCC Article 2A", "Restatement (Third) of Property"],
        confidence=0.95,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.DEED,
        doc_type_key="GENERAL_WARRANTY_DEED",
        counter_indicators=["special warranty", "quitclaim", "without warranty"],
    ),
    DoctrineBlock(
        topic="Special Warranty Deed Classification",
        keywords=["special warranty deed", "by through or under", "limited warranty", "bargain sell convey"],
        conclusion_template="Document classified as Special Warranty Deed with limited covenants (by, through, or under grantor only).",
        reasoning_framework="A special warranty deed limits the grantor's warranty to defects arising during grantor's period of ownership. The key distinguishing language is 'by, through, or under' the grantor, excluding claims from predecessors in title.",
        key_factors=["Limited warranty language", "By-through-or-under limitation", "Granting clause"],
        primary_authority=["Tex. Prop. Code 5.023", "Black's Law Dictionary 'special warranty deed'"],
        confidence=0.93,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.DEED,
        doc_type_key="SPECIAL_WARRANTY_DEED",
        counter_indicators=["general warranty", "warrant and defend all claims"],
    ),
    DoctrineBlock(
        topic="Quitclaim Deed Classification",
        keywords=["quitclaim", "quit claim", "remise release", "right title and interest", "without warranty"],
        conclusion_template="Document classified as Quitclaim Deed conveying whatever interest grantor may hold, without warranties.",
        reasoning_framework="A quitclaim deed conveys only whatever interest the grantor may have, if any, with no warranties of title. It is commonly used to clear clouds on title, transfer between family members, or resolve boundary disputes.",
        key_factors=["No warranty language", "Remise/release language", "Right-title-interest conveyance"],
        primary_authority=["Tex. Prop. Code 5.021", "Restatement of Property"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.DEED,
        doc_type_key="QUITCLAIM_DEED",
        counter_indicators=["warrant and defend", "general warranty", "special warranty"],
    ),
    DoctrineBlock(
        topic="Oil and Gas Lease Classification",
        keywords=["oil and gas lease", "lessor", "lessee", "royalty", "primary term", "habendum", "drilling operations"],
        conclusion_template="Document classified as Oil and Gas Lease granting exploration and production rights.",
        reasoning_framework="An oil and gas lease is identified by a granting clause (lessor to lessee), habendum clause (primary term plus production), royalty clause (fraction of production), and typically delay rental or paid-up provision. Texas treats it as a fee simple determinable in the mineral estate.",
        key_factors=["Granting clause", "Habendum/primary term", "Royalty clause", "Delay rental or paid-up", "Pooling provisions"],
        primary_authority=["Tex. Nat. Res. Code Ch. 91", "Japhet v. McRae", "Rogers v. Osborn"],
        confidence=0.96,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.LEASE,
        doc_type_key="OIL_GAS_LEASE",
        counter_indicators=["surface lease", "wind energy", "solar", "agricultural"],
    ),
    DoctrineBlock(
        topic="Mineral Deed Classification",
        keywords=["mineral deed", "mineral interest", "mineral estate", "minerals in and under", "undivided mineral"],
        conclusion_template="Document classified as Mineral Deed conveying subsurface mineral interest.",
        reasoning_framework="A mineral deed severs or transfers the mineral estate from the surface estate. Key identifiers include conveyance of 'oil, gas, and other minerals in and under' a described tract, without granting exploration rights (which distinguishes it from a lease).",
        key_factors=["Mineral estate conveyance", "Fractional interest", "Severance language", "No lease terms"],
        primary_authority=["Tex. Prop. Code 5.001", "Moser v. U.S. Steel", "French v. Chevron"],
        confidence=0.94,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.MINERAL,
        doc_type_key="MINERAL_DEED",
        counter_indicators=["lease", "lessor", "lessee", "royalty deed only"],
    ),
    DoctrineBlock(
        topic="Royalty Deed Classification",
        keywords=["royalty deed", "royalty interest", "non-participating royalty", "NPRI"],
        conclusion_template="Document classified as Royalty Deed conveying non-participating royalty interest.",
        reasoning_framework="A royalty deed conveys the right to receive a fraction of production revenue without cost-bearing obligations or executive rights. An NPRI holder cannot lease, pool, or otherwise manage the mineral estate.",
        key_factors=["Royalty-only conveyance", "No executive rights", "No cost-bearing", "Production revenue entitlement"],
        primary_authority=["Tex. Nat. Res. Code", "Lesley v. Veterans Land Board", "NPRI treatise"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.MINERAL,
        doc_type_key="ROYALTY_DEED",
        counter_indicators=["mineral deed", "working interest", "operator"],
    ),
    DoctrineBlock(
        topic="Deed of Trust Classification",
        keywords=["deed of trust", "trustor", "trustee", "beneficiary", "promissory note", "power of sale"],
        conclusion_template="Document classified as Deed of Trust securing a promissory note against real property.",
        reasoning_framework="A deed of trust is a three-party security instrument where the trustor (borrower) conveys legal title to a trustee for the benefit of the beneficiary (lender). It includes a power of sale enabling non-judicial foreclosure upon default.",
        key_factors=["Three-party structure", "Security instrument", "Power of sale", "Promissory note reference"],
        primary_authority=["Tex. Prop. Code Ch. 51", "Tex. Bus. & Com. Code"],
        confidence=0.95,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.MORTGAGE,
        doc_type_key="DEED_OF_TRUST",
        counter_indicators=["release of lien", "satisfaction", "reconveyance"],
    ),
    DoctrineBlock(
        topic="Release of Lien Classification",
        keywords=["release of lien", "satisfaction", "reconveyance", "lien released", "mortgage satisfied", "paid in full"],
        conclusion_template="Document classified as Release of Lien / Satisfaction of Mortgage.",
        reasoning_framework="A release of lien removes a previously recorded encumbrance from the public record. It may take the form of a release, satisfaction, reconveyance, or cancellation. The key element is reference to the original recording data of the instrument being released.",
        key_factors=["Reference to original lien", "Release language", "Recording reference", "Authorized signatory"],
        primary_authority=["Tex. Prop. Code 51.003", "UCC 9-513"],
        confidence=0.94,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.MORTGAGE,
        doc_type_key="RELEASE_OF_LIEN",
        counter_indicators=["deed of trust granting", "new lien"],
    ),
    DoctrineBlock(
        topic="Affidavit of Heirship Classification",
        keywords=["affidavit of heirship", "heirs at law", "decedent", "died intestate", "surviving spouse"],
        conclusion_template="Document classified as Affidavit of Heirship identifying successors to decedent's property.",
        reasoning_framework="An affidavit of heirship is used to establish the identity of heirs without formal probate. Texas Estates Code 203.001 allows it after 5 years. The affiant (typically a disinterested party) swears to family history, marital status, descendants, and community/separate property characterization.",
        key_factors=["Decedent identification", "Family tree recital", "Disinterested affiant", "Property description"],
        primary_authority=["Tex. Estates Code 203.001", "Tex. Prop. Code 52.006"],
        confidence=0.95,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AFFIDAVIT,
        doc_type_key="AFFIDAVIT_HEIRSHIP",
        counter_indicators=["probate order", "letters testamentary"],
    ),
    DoctrineBlock(
        topic="Probate Court Order Classification",
        keywords=["probate", "estate of", "decedent", "executor", "administrator", "letters testamentary", "letters of administration"],
        conclusion_template="Document classified as Probate Court Order from estate proceedings.",
        reasoning_framework="Probate orders are court instruments from estate proceedings that affect real property title. They include orders admitting wills, appointing executors/administrators, approving inventories, authorizing sales, and distributing assets. Court seal and judge signature are key authenticators.",
        key_factors=["Court heading", "Case number", "Judge signature", "Estate identification", "Judicial authority"],
        primary_authority=["Tex. Estates Code", "Tex. Prob. Code (pre-2014)"],
        confidence=0.94,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.COURT_ORDER,
        doc_type_key="PROBATE_ORDER",
        counter_indicators=["divorce", "partition", "receivership"],
    ),
    DoctrineBlock(
        topic="Divorce Decree Property Division Classification",
        keywords=["divorce", "dissolution of marriage", "property division", "community property", "final decree"],
        conclusion_template="Document classified as Divorce Decree with real property division provisions.",
        reasoning_framework="A divorce decree affecting real property must be recorded to provide constructive notice. The property division section awards community or separate property to each spouse. In Texas, community property is presumed and must be divided 'just and right'. The decree serves as a conveyance.",
        key_factors=["Court decree", "Property division section", "Community property language", "Spouse identification"],
        primary_authority=["Tex. Fam. Code 7.001", "Tex. Prop. Code"],
        confidence=0.93,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.COURT_ORDER,
        doc_type_key="DIVORCE_DECREE",
        counter_indicators=["probate", "criminal", "partition"],
    ),
    DoctrineBlock(
        topic="Assignment of Overriding Royalty Interest Classification",
        keywords=["assignment of overriding royalty", "ORRI", "overriding royalty interest", "override", "carved out"],
        conclusion_template="Document classified as Assignment of Overriding Royalty Interest (ORRI).",
        reasoning_framework="An ORRI is carved from the working interest under an existing lease. It is a cost-free interest in production that terminates when the underlying lease terminates. Key identifiers include reference to the underlying lease, decimal interest specification, and the absence of cost-bearing language.",
        key_factors=["Lease reference", "Decimal interest", "Non-cost-bearing", "Production entitlement", "Carved from WI"],
        primary_authority=["Tex. Nat. Res. Code", "Schlittler v. Smith"],
        confidence=0.93,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.ASSIGNMENT,
        doc_type_key="ASSIGNMENT_ORI",
        counter_indicators=["working interest", "operator", "cost-bearing"],
    ),
    DoctrineBlock(
        topic="Assignment of Working Interest Classification",
        keywords=["assignment of working interest", "operating rights", "cost-bearing", "working interest", "operator"],
        conclusion_template="Document classified as Assignment of Working Interest with cost-bearing obligations.",
        reasoning_framework="A working interest assignment transfers the right to explore and produce, along with the obligation to bear proportionate costs of drilling, completion, and operation. The assignee becomes a co-operator or sole operator depending on the interest transferred.",
        key_factors=["Cost-bearing obligation", "Operator rights", "Lease reference", "AFE responsibility"],
        primary_authority=["Tex. Nat. Res. Code", "AAPL Form 610"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.ASSIGNMENT,
        doc_type_key="ASSIGNMENT_WI",
        counter_indicators=["royalty only", "non-participating", "ORRI"],
    ),
    DoctrineBlock(
        topic="Pipeline Right of Way Classification",
        keywords=["pipeline right of way", "pipeline easement", "lay construct operate", "gathering line", "transmission"],
        conclusion_template="Document classified as Pipeline Right of Way / Easement.",
        reasoning_framework="A pipeline right of way grants the holder the right to construct, operate, maintain, repair, and remove pipelines across the grantor's surface estate. Width, depth, and duration are key terms. Texas common law gives the mineral lessee an implied right of reasonable surface use, but explicit grants are required for third-party pipelines.",
        key_factors=["Pipeline description", "Width/depth specs", "Duration", "Restoration obligations", "Consideration"],
        primary_authority=["Tex. Nat. Res. Code Ch. 111", "Tex. Util. Code"],
        confidence=0.93,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.RIGHT_OF_WAY,
        doc_type_key="ROW_PIPELINE",
        counter_indicators=["road", "utility", "electric"],
    ),
    DoctrineBlock(
        topic="Division Order Classification",
        keywords=["division order", "decimal interest", "revenue distribution", "proceeds", "purchaser", "operator"],
        conclusion_template="Document classified as Division Order for production revenue distribution.",
        reasoning_framework="A division order directs the purchaser of production to distribute proceeds among interest owners according to stated decimal interests. Under Texas Natural Resources Code 91.402, it is a contract that may be binding for its stated term. It does NOT convey title — it only directs payment.",
        key_factors=["Decimal interest allocation", "Purchaser/operator direction", "Revenue payment", "No conveyance language"],
        primary_authority=["Tex. Nat. Res. Code 91.402", "NADOA Model Form"],
        confidence=0.93,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AGREEMENT,
        doc_type_key="DIVISION_ORDER",
        counter_indicators=["deed", "convey", "grant"],
    ),
    DoctrineBlock(
        topic="Pooling Agreement Classification",
        keywords=["pooling agreement", "pooled unit", "pooling designation", "force pooling", "voluntary pooling"],
        conclusion_template="Document classified as Pooling Agreement combining tracts for drilling unit.",
        reasoning_framework="Pooling combines separate tracts or mineral interests into a single drilling unit. Voluntary pooling requires consent; compulsory/force pooling is imposed by the Railroad Commission of Texas under Tex. Nat. Res. Code 102.011. The pooling designation specifies unit boundaries, allocation formula, and participating interests.",
        key_factors=["Unit designation", "Tract descriptions", "Allocation formula", "RRC authorization (if forced)"],
        primary_authority=["Tex. Nat. Res. Code 102.011", "RRC Statewide Rule 37/38"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AGREEMENT,
        doc_type_key="POOLING_AGREEMENT",
        counter_indicators=["unitization", "secondary recovery"],
    ),
    DoctrineBlock(
        topic="Unitization Agreement Classification",
        keywords=["unitization", "unit agreement", "unit operations", "secondary recovery", "enhanced recovery", "waterflood"],
        conclusion_template="Document classified as Unitization Agreement for enhanced recovery operations.",
        reasoning_framework="Unitization combines multiple leases and tracts into a single operational unit for secondary/enhanced recovery operations (waterflood, CO2 injection, etc.). It differs from pooling in scope and purpose. Voluntary unitization requires consent of a supermajority of interest owners (typically 80%+).",
        key_factors=["Multiple lease combination", "Enhanced recovery purpose", "Participation factor", "Unit area description"],
        primary_authority=["Tex. Nat. Res. Code Ch. 102", "RRC Rule 51"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AGREEMENT,
        doc_type_key="UNITIZATION_AGREEMENT",
        counter_indicators=["pooling designation", "single well"],
    ),
    DoctrineBlock(
        topic="Power of Attorney Classification",
        keywords=["power of attorney", "attorney-in-fact", "agent", "principal", "durable power", "POA"],
        conclusion_template="Document classified as Power of Attorney for real property transactions.",
        reasoning_framework="A power of attorney (POA) grants an agent (attorney-in-fact) authority to act for the principal. For real property, it must be in writing, acknowledged, and recorded. A 'durable' POA survives the principal's incapacity. Texas Estates Code Ch. 751 governs statutory durable POAs.",
        key_factors=["Agent/principal identification", "Scope of authority", "Durability clause", "Notarization"],
        primary_authority=["Tex. Estates Code Ch. 751", "Tex. Prop. Code"],
        confidence=0.94,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.CORPORATE,
        doc_type_key="POWER_OF_ATTORNEY",
        counter_indicators=["revocation of power"],
    ),
    DoctrineBlock(
        topic="Correction Deed Classification",
        keywords=["correction deed", "corrective deed", "scrivener's error", "re-recorded", "corrective instrument"],
        conclusion_template="Document classified as Correction Deed fixing a prior recording error.",
        reasoning_framework="A correction deed corrects a scrivener's error in a previously recorded deed (misspelled names, wrong legal description, incorrect grantee, etc.). Texas Property Code 5.028-5.031 provides a statutory framework. It must reference the original instrument and identify the specific error being corrected.",
        key_factors=["Reference to original deed", "Specific error identification", "Correction language", "Same parties"],
        primary_authority=["Tex. Prop. Code 5.028-5.031"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.DEED,
        doc_type_key="CORRECTION_DEED",
        counter_indicators=["new conveyance", "additional consideration"],
    ),
    DoctrineBlock(
        topic="Gift Deed Classification",
        keywords=["gift deed", "love and affection", "natural love", "no monetary consideration", "donative"],
        conclusion_template="Document classified as Gift Deed with love-and-affection consideration.",
        reasoning_framework="A gift deed transfers real property without monetary consideration, typically reciting 'love and affection' or 'natural love and affection' as the consideration. Gift deeds may trigger different tax treatment (no stepped-up basis under IRC 1015 vs. 1014 for inherited property). The donative intent must be clear.",
        key_factors=["Love-and-affection recital", "No dollar consideration", "Family relationship implied", "Clear donative intent"],
        primary_authority=["Tex. Prop. Code 5.021", "IRC 1015 (carryover basis)"],
        confidence=0.90,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.DEED,
        doc_type_key="GIFT_DEED",
        counter_indicators=["$10.00 and other valuable consideration", "purchase price"],
    ),
    DoctrineBlock(
        topic="Surface Lease Classification",
        keywords=["surface lease", "surface use", "tank battery", "well pad", "saltwater disposal", "surface only"],
        conclusion_template="Document classified as Surface Lease for oil and gas related surface use.",
        reasoning_framework="A surface lease grants the right to use the surface of land for oil and gas operations infrastructure — tank batteries, well pads, roads, SWD facilities, compressor stations. It is distinct from an oil and gas lease (which grants subsurface mineral rights) and from a surface damage agreement (which compensates for damage already done).",
        key_factors=["Surface-only use", "Infrastructure purpose", "Rental payments", "Restoration clause"],
        primary_authority=["Tex. Nat. Res. Code", "Surface Use Agreement forms"],
        confidence=0.91,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.LEASE,
        doc_type_key="SURFACE_LEASE",
        counter_indicators=["oil and gas lease", "mineral rights", "habendum"],
    ),
    DoctrineBlock(
        topic="Affidavit of Identity Classification",
        keywords=["affidavit of identity", "same person", "also known as", "AKA", "name variation", "one and the same"],
        conclusion_template="Document classified as Affidavit of Identity / Name confirming identity across name variations.",
        reasoning_framework="An affidavit of identity resolves discrepancies between name variations in the chain of title. The affiant (often the person themselves or a knowledgeable party) swears that 'John A. Smith' and 'J.A. Smith' are one and the same person. Title companies require these to clear name-related title objections.",
        key_factors=["Name variations listed", "Same-person declaration", "Sworn statement", "Notarization"],
        primary_authority=["Tex. Prop. Code", "Title Insurance standards"],
        confidence=0.91,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AFFIDAVIT,
        doc_type_key="AFFIDAVIT_IDENTITY",
        counter_indicators=["heirship", "non-production", "decedent"],
    ),
    DoctrineBlock(
        topic="Affidavit of Non-Production Classification",
        keywords=["affidavit of non-production", "no production", "lease expired", "cessation of production", "well plugged"],
        conclusion_template="Document classified as Affidavit of Non-Production stating lease termination by non-production.",
        reasoning_framework="An affidavit of non-production is filed by a mineral owner or surface owner to place the public record on notice that an oil and gas lease has terminated due to expiration of the primary term without production, or cessation of production in quantities sufficient to maintain the lease beyond the secondary term.",
        key_factors=["Lease identification", "Non-production statement", "Date range", "Well status"],
        primary_authority=["Tex. Nat. Res. Code 91.402", "Hydrocarbon Production Reporting Act"],
        confidence=0.91,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AFFIDAVIT,
        doc_type_key="AFFIDAVIT_NON_PRODUCTION",
        counter_indicators=["currently producing", "royalty payment"],
    ),
    DoctrineBlock(
        topic="Ratification of Lease Classification",
        keywords=["ratification", "ratify and confirm", "ratification of lease", "join in", "previously executed"],
        conclusion_template="Document classified as Ratification of Oil and Gas Lease.",
        reasoning_framework="A ratification is executed by an interest owner who was not an original party to a lease, confirming that the lease covers their interest. This commonly occurs when heirs inherit after lease execution, or when a co-tenant's interest was inadvertently omitted. The ratification 'relates back' to the original lease date.",
        key_factors=["Reference to original lease", "Ratifying party identification", "Confirmation language", "Interest description"],
        primary_authority=["Tex. Prop. Code", "AAPL Title Standards"],
        confidence=0.90,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AGREEMENT,
        doc_type_key="RATIFICATION",
        counter_indicators=["new lease", "original lessor"],
    ),
    DoctrineBlock(
        topic="Subordination Agreement Classification",
        keywords=["subordination", "subordinate", "junior lien", "priority", "senior lien", "first lien position"],
        conclusion_template="Document classified as Subordination Agreement altering lien priority.",
        reasoning_framework="A subordination agreement changes the priority of liens or interests from what would otherwise be determined by recording date. Typically, a first-lien holder agrees to subordinate to a new lien, or a mineral interest holder subordinates to a surface lien. The agreement must be clear, explicit, and executed by the party whose priority is being diminished.",
        key_factors=["Lien identification", "Priority change language", "Both parties' consent", "Recording references"],
        primary_authority=["Tex. Prop. Code", "Restatement of Mortgages"],
        confidence=0.90,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.AGREEMENT,
        doc_type_key="SUBORDINATION",
        counter_indicators=["release of lien", "payoff"],
    ),
    DoctrineBlock(
        topic="UCC Financing Statement Classification",
        keywords=["UCC", "financing statement", "UCC-1", "secured party", "debtor", "collateral", "fixture filing"],
        conclusion_template="Document classified as UCC Financing Statement (fixture filing or personal property lien).",
        reasoning_framework="A UCC-1 financing statement perfects a security interest in personal property or fixtures. When filed in the real property records as a fixture filing, it provides notice that equipment attached to land (pump jacks, tanks, compressors) is subject to a security interest. The filing must identify debtor, secured party, and collateral.",
        key_factors=["UCC form identification", "Debtor/secured party", "Collateral description", "Fixture filing box"],
        primary_authority=["Tex. Bus. & Com. Code Ch. 9", "UCC Article 9"],
        confidence=0.92,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.CORPORATE,
        doc_type_key="UCC_FILING",
        counter_indicators=["deed of trust", "mortgage"],
    ),
    DoctrineBlock(
        topic="Partition Order Classification",
        keywords=["partition", "partition in kind", "partition by sale", "co-tenancy", "cotenant", "undivided interest"],
        conclusion_template="Document classified as Partition Order / Judgment dividing co-owned property.",
        reasoning_framework="A partition action divides co-owned property either in kind (physical division) or by sale (forced sale with proceeds division). Under Texas Property Code Ch. 23A (Uniform Partition of Heirs Property Act), partition by sale requires specific procedural protections when inherited property is involved.",
        key_factors=["Court order format", "Co-tenant identification", "Division method", "Interest percentages"],
        primary_authority=["Tex. Prop. Code Ch. 23", "Tex. Prop. Code Ch. 23A (UPHPA)"],
        confidence=0.91,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.COURT_ORDER,
        doc_type_key="PARTITION_ORDER",
        counter_indicators=["probate", "divorce"],
    ),
    DoctrineBlock(
        topic="Wind/Solar Energy Lease Classification",
        keywords=["wind energy", "solar energy", "wind lease", "solar lease", "renewable energy", "wind turbine", "photovoltaic"],
        conclusion_template="Document classified as Wind/Solar Energy Lease for renewable energy development.",
        reasoning_framework="A wind or solar energy lease grants the right to install and operate renewable energy infrastructure on the surface. Key terms include development period, generation period, MW capacity, setback requirements, decommissioning obligations, and rental/royalty payments (often per-MW or per-turbine). These leases can be 30-50 years with extensions.",
        key_factors=["Renewable energy purpose", "Development/generation periods", "MW capacity", "Decommissioning clause"],
        primary_authority=["Tex. Prop. Code", "Tex. Util. Code", "PUCT regulations"],
        confidence=0.91,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.LEASE,
        doc_type_key="WIND_SOLAR_LEASE",
        counter_indicators=["oil and gas", "mineral", "drilling"],
    ),
    DoctrineBlock(
        topic="Receivership Order Classification",
        keywords=["receivership", "receiver appointed", "court-appointed receiver", "custodian", "receivership estate"],
        conclusion_template="Document classified as Receivership Order appointing receiver over property/operations.",
        reasoning_framework="A receivership order appoints a neutral third party (receiver) to manage property, business operations, or assets pending litigation or insolvency. In oil and gas, receiverships are common when operators become insolvent, wells need plugging, or environmental remediation is required.",
        key_factors=["Court authority", "Receiver identification", "Scope of authority", "Property/assets covered"],
        primary_authority=["Tex. Civ. Prac. & Rem. Code Ch. 64", "Tex. Bus. Orgs. Code"],
        confidence=0.90,
        stratum=ConfidenceStratum.DEFENSIBLE,
        category=DocCategory.COURT_ORDER,
        doc_type_key="RECEIVERSHIP_ORDER",
        counter_indicators=["probate", "divorce"],
    ),
    DoctrineBlock(
        topic="Stipulation of Interest Classification",
        keywords=["stipulation of interest", "agreed interest", "stipulated ownership", "ownership stipulation"],
        conclusion_template="Document classified as Stipulation of Interest establishing agreed ownership percentages.",
        reasoning_framework="A stipulation of interest is an agreement between parties (often in the context of division orders or title disputes) that stipulates each party's ownership percentage. It does not convey title but serves as evidence of agreed ownership for payment and operational purposes.",
        key_factors=["Interest percentages", "Party identification", "Agreement language", "Non-conveyance disclaimer"],
        primary_authority=["Contract law principles", "AAPL Title Standards"],
        confidence=0.88,
        stratum=ConfidenceStratum.AGGRESSIVE,
        category=DocCategory.AGREEMENT,
        doc_type_key="STIPULATION_OF_INTEREST",
        counter_indicators=["deed", "convey", "grant"],
    ),
    DoctrineBlock(
        topic="Production Payment Classification",
        keywords=["production payment", "volumetric production", "carved-out production", "dollar-denominated"],
        conclusion_template="Document classified as Production Payment assignment.",
        reasoning_framework="A production payment is a right to receive a specified share of production (or its monetary equivalent) until a stated quantity or dollar amount is reached, at which point the interest terminates automatically. It is treated as an economic interest for tax purposes (IRC 636).",
        key_factors=["Production entitlement", "Termination condition", "Quantity/dollar limit", "Self-liquidating nature"],
        primary_authority=["IRC 636", "Tex. Nat. Res. Code", "Anderson v. Helvering"],
        confidence=0.89,
        stratum=ConfidenceStratum.AGGRESSIVE,
        category=DocCategory.MINERAL,
        doc_type_key="PRODUCTION_PAYMENT",
        counter_indicators=["royalty deed", "perpetual"],
    ),
]

# Build doctrine lookup index
_DOCTRINE_INDEX: Dict[str, DoctrineBlock] = {d.doc_type_key: d for d in DOCTRINE_CACHE}


# ═══════════════════════════════════════════════════════════════════════════
# TIE-06: SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════

SYNONYM_MAP: Dict[str, str] = {
    "gwd": "general warranty deed",
    "swd": "special warranty deed",
    "qcd": "quitclaim deed",
    "dot": "deed of trust",
    "rol": "release of lien",
    "aoh": "affidavit of heirship",
    "poa": "power of attorney",
    "ogl": "oil and gas lease",
    "orri": "overriding royalty interest",
    "npri": "non-participating royalty interest",
    "wi": "working interest",
    "row": "right of way",
    "do": "division order",
    "ucc": "ucc financing statement",
    "roi": "royalty interest",
    "md": "mineral deed",
    "rd": "royalty deed",
    "warranty deed": "general warranty deed",
    "mtg": "deed of trust",
    "mortgage": "deed of trust",
    "lien release": "release of lien",
    "sat of mtg": "release of lien",
    "heirship affidavit": "affidavit of heirship",
    "pooling order": "pooling agreement",
    "unit agreement": "unitization agreement",
    "lease ratification": "ratification",
    "sub agreement": "subordination",
}


def normalize_text(text: str) -> str:
    """Normalize document text for classification: lowercase, expand abbreviations."""
    result = text.lower().strip()
    for abbrev, expansion in SYNONYM_MAP.items():
        result = result.replace(abbrev.lower(), expansion)
    return result


# ═══════════════════════════════════════════════════════════════════════════
# TIE-14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════

def compute_fragility(candidates: List[ClassificationCandidate]) -> float:
    """Compute classification fragility: 0 = rock-solid, 1 = highly ambiguous."""
    if not candidates:
        return 1.0
    if len(candidates) == 1:
        c = candidates[0].confidence
        return max(0.0, 1.0 - c)
    top = candidates[0].confidence
    second = candidates[1].confidence
    gap = top - second
    # Fragility is high when gap is small and top confidence is low
    gap_factor = 1.0 - min(gap / 0.3, 1.0)  # gap < 0.3 = fragile
    conf_factor = 1.0 - top  # low confidence = fragile
    return round(min(1.0, gap_factor * 0.6 + conf_factor * 0.4), 4)


def stratify_confidence(confidence: float, fragility: float) -> ConfidenceStratum:
    """Map confidence + fragility to a stratum."""
    if confidence >= 0.85 and fragility < 0.3:
        return ConfidenceStratum.DEFENSIBLE
    if confidence >= 0.65:
        return ConfidenceStratum.AGGRESSIVE
    if confidence >= 0.40:
        return ConfidenceStratum.DISCLOSURE
    return ConfidenceStratum.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════
# TIE-16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(text: str, candidates: List[ClassificationCandidate]) -> str:
    """SHA-256 hash for reproducibility: same input + same rules = same hash."""
    payload = {
        "input_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
        "candidates": [(c.doc_type, round(c.confidence, 6)) for c in candidates[:5]],
        "engine": ENGINE_VERSION,
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURAL FEATURE EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════

_RE_LEGAL_DESC = re.compile(
    r"(section\s+\d+|block\s+\d+|township\s+\d+|abstract\s+(no\.?|number)?\s*\d+|survey|"
    r"lot\s+\d+|metes\s+and\s+bounds|beginning\s+at\s+a?\s*(point|stake|iron)|"
    r"thence\s+(north|south|east|west)|range\s+\d+|acres?\s+(more\s+or\s+less)?)",
    re.IGNORECASE,
)
_RE_RECORDING = re.compile(
    r"(recorded\s+in|filed\s+(in|for\s+record)|volume\s+\d+|book\s+\d+|page\s+\d+|"
    r"instrument\s+(no\.?|number|#)\s*\d+|doc(ument)?\s*(no\.?|number|#)\s*\d+|"
    r"clerk.s\s+file\s+(no\.?|number|#))",
    re.IGNORECASE,
)
_RE_SIGNATURE = re.compile(
    r"(_{5,}|/s/\s*\w|signature|signed\s+(and\s+)?(sealed|delivered)|witness\s+(my|our)\s+hand|"
    r"in\s+witness\s+whereof|executed\s+(this|on))",
    re.IGNORECASE,
)
_RE_NOTARY = re.compile(
    r"(notary\s+public|state\s+of\s+\w+.*county\s+of\s+\w+|before\s+me|"
    r"acknowledged|sworn\s+to\s+and\s+subscribed|my\s+commission\s+expires)",
    re.IGNORECASE,
)
_RE_CONSIDERATION = re.compile(
    r"(for\s+and\s+in\s+consideration|ten\s+dollars?\s+\(\$10\.00\)|"
    r"\$[\d,.]+\s+(and\s+other\s+)?(good\s+and\s+)?valuable\s+consideration|"
    r"love\s+and\s+affection|cash\s+in\s+hand\s+paid)",
    re.IGNORECASE,
)
_RE_GRANTING = re.compile(
    r"(grant[,]?\s+sell[,]?\s+(and\s+)?convey|bargain[,]?\s+sell[,]?\s+(and\s+)?convey|"
    r"remise[,]?\s+release[,]?\s+(and\s+)?quit[\s-]?claim|convey\s+and\s+warrant|"
    r"hereby\s+(grants?|conveys?|assigns?|transfers?))",
    re.IGNORECASE,
)
_RE_HABENDUM = re.compile(r"(habendum|to\s+have\s+and\s+to\s+hold)", re.IGNORECASE)
_RE_COUNTY = re.compile(r"(?:county\s+of|(\w+)\s+county)[,.]?\s*(\w+)?", re.IGNORECASE)
_RE_STATE = re.compile(r"state\s+of\s+(texas|oklahoma|new\s+mexico|louisiana|california|colorado|wyoming|north\s+dakota|pennsylvania|west\s+virginia|ohio)", re.IGNORECASE)
_RE_INSTRUMENT_NO = re.compile(r"(?:instrument|doc(?:ument)?)\s*(?:no\.?|number|#)\s*(\d[\d\-]+)", re.IGNORECASE)
_RE_BOOK_PAGE = re.compile(r"(?:volume|book)\s*(\d+)[,.\s]+(?:page)\s*(\d+)", re.IGNORECASE)
_RE_HEADER = re.compile(r"^(.{0,200})", re.MULTILINE)


def extract_structural_features(text: str) -> StructuralFeatures:
    """Extract structural features from document text."""
    word_count = len(text.split())
    estimated_pages = max(1, word_count // 300)

    header_match = _RE_HEADER.search(text)
    header_text = header_match.group(1).strip() if header_match else None

    county_match = _RE_COUNTY.search(text)
    extracted_county = None
    if county_match:
        g1, g2 = county_match.group(1), county_match.group(2)
        extracted_county = (g1 or g2 or "").strip().title() if (g1 or g2) else None

    state_match = _RE_STATE.search(text)
    extracted_state = state_match.group(1).strip().title() if state_match else None

    inst_match = _RE_INSTRUMENT_NO.search(text)
    extracted_instrument_no = inst_match.group(1).strip() if inst_match else None

    bp_match = _RE_BOOK_PAGE.search(text)
    extracted_book_page = f"Vol. {bp_match.group(1)}, Pg. {bp_match.group(2)}" if bp_match else None

    return StructuralFeatures(
        estimated_pages=estimated_pages,
        has_legal_description=bool(_RE_LEGAL_DESC.search(text)),
        has_recording_info=bool(_RE_RECORDING.search(text)),
        has_signature_block=bool(_RE_SIGNATURE.search(text)),
        has_notary_block=bool(_RE_NOTARY.search(text)),
        has_consideration=bool(_RE_CONSIDERATION.search(text)),
        has_granting_clause=bool(_RE_GRANTING.search(text)),
        has_habendum=bool(_RE_HABENDUM.search(text)),
        extracted_county=extracted_county,
        extracted_state=extracted_state,
        extracted_instrument_no=extracted_instrument_no,
        extracted_book_page=extracted_book_page,
        header_text=header_text,
        word_count=word_count,
    )


# ═══════════════════════════════════════════════════════════════════════════
# TIE-01: THREE LAYER RESPONSE (Doctrine Cache -> Semantic -> Deep)
# ═══════════════════════════════════════════════════════════════════════════

def _classify_doctrine_cache(text_lower: str, top_k: int) -> Tuple[List[ClassificationCandidate], ClassificationTier]:
    """Layer 1: Fast doctrine cache classification using keyword + regex patterns."""
    scores: List[Tuple[str, float, List[str], List[str]]] = []

    # Phase A: Regex pattern matching on DOCUMENT_TYPES
    for dt_key, dt_info in DOCUMENT_TYPES.items():
        matched_kw: List[str] = []
        matched_pat: List[str] = []

        # Keyword matching
        for kw in dt_info["keywords"]:
            if kw.lower() in text_lower:
                matched_kw.append(kw)

        # Regex pattern matching
        for pat in _COMPILED_PATTERNS[dt_key]:
            if pat.search(text_lower):
                matched_pat.append(pat.pattern)

        if not matched_kw and not matched_pat:
            continue

        kw_score = len(matched_kw) / max(len(dt_info["keywords"]), 1)
        pat_score = len(matched_pat) / max(len(dt_info["regex"]), 1)
        combined = (kw_score * 0.4 + pat_score * 0.6) * dt_info["weight"]
        scores.append((dt_key, combined, matched_kw, matched_pat))

    # Phase B: Doctrine block matching for additional context
    for doctrine in DOCTRINE_CACHE:
        matched, d_score, d_kw = doctrine.matches(text_lower)
        if not matched:
            continue
        # Merge with existing score if doc_type already found
        existing = next((s for s in scores if s[0] == doctrine.doc_type_key), None)
        if existing:
            idx = scores.index(existing)
            merged_score = existing[1] * 0.6 + d_score * 0.4
            merged_kw = list(set(existing[2] + d_kw))
            scores[idx] = (existing[0], merged_score, merged_kw, existing[3])
        else:
            scores.append((doctrine.doc_type_key, d_score * 0.8, d_kw, []))

    if not scores:
        return [], ClassificationTier.DOCTRINE_CACHE

    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)

    # Normalize scores to 0-1 range based on max
    max_score = scores[0][1] if scores[0][1] > 0 else 1.0

    candidates: List[ClassificationCandidate] = []
    for dt_key, raw_score, m_kw, m_pat in scores[:top_k]:
        dt_info = DOCUMENT_TYPES.get(dt_key)
        if not dt_info:
            continue
        norm_conf = min(1.0, raw_score / max_score * 0.95)
        fragility = compute_fragility([ClassificationCandidate(
            doc_type=dt_key, display_name=dt_info["display"],
            category=dt_info["category"].value, confidence=norm_conf,
            stratum=ConfidenceStratum.DEFENSIBLE, matched_keywords=m_kw,
            matched_patterns=m_pat, feature_scores={},
        )])
        stratum = stratify_confidence(norm_conf, fragility)
        candidates.append(ClassificationCandidate(
            doc_type=dt_key,
            display_name=dt_info["display"],
            category=dt_info["category"].value,
            confidence=round(norm_conf, 4),
            stratum=stratum,
            matched_keywords=m_kw,
            matched_patterns=m_pat,
            feature_scores={"keyword_score": round(raw_score, 4)},
        ))

    return candidates, ClassificationTier.DOCTRINE_CACHE


def _classify_structural(text: str, features: StructuralFeatures, candidates: List[ClassificationCandidate]) -> List[ClassificationCandidate]:
    """Layer 1.5: Adjust scores based on structural features."""
    for c in candidates:
        bonus = 0.0
        dt_info = DOCUMENT_TYPES.get(c.doc_type)
        if not dt_info:
            continue
        cat = dt_info["category"]

        # Structural bonuses
        if cat in (DocCategory.DEED, DocCategory.MINERAL) and features.has_granting_clause:
            bonus += 0.05
        if cat in (DocCategory.DEED, DocCategory.MINERAL) and features.has_legal_description:
            bonus += 0.03
        if cat in (DocCategory.DEED, DocCategory.MORTGAGE) and features.has_consideration:
            bonus += 0.03
        if cat == DocCategory.LEASE and features.has_habendum:
            bonus += 0.06
        if cat == DocCategory.COURT_ORDER and features.word_count > 500:
            bonus += 0.02
        if cat == DocCategory.AFFIDAVIT and features.has_notary_block:
            bonus += 0.04
        if features.has_recording_info:
            bonus += 0.02

        c.confidence = round(min(1.0, c.confidence + bonus), 4)
        c.feature_scores["structural_bonus"] = round(bonus, 4)

    # Re-sort after structural adjustment
    candidates.sort(key=lambda x: x.confidence, reverse=True)
    return candidates


async def _classify_semantic(text: str, top_k: int) -> List[ClassificationCandidate]:
    """Layer 2: Semantic retrieval via cloud for unrecognized documents."""
    if CognitionCloudRetriever is None:
        return []
    try:
        cloud = CognitionCloudRetriever()
        results = await asyncio.wait_for(
            cloud.retrieve_all(f"classify document type: {text[:500]}", category="document_classification"),
            timeout=5.0,
        )
        candidates: List[ClassificationCandidate] = []
        if results and hasattr(results, "results"):
            for r in results.results[:top_k]:
                content = getattr(r, "content", "") or ""
                for dt_key, dt_info in DOCUMENT_TYPES.items():
                    if dt_info["display"].lower() in content.lower():
                        candidates.append(ClassificationCandidate(
                            doc_type=dt_key,
                            display_name=dt_info["display"],
                            category=dt_info["category"].value,
                            confidence=round(getattr(r, "relevance", 0.5), 4),
                            stratum=ConfidenceStratum.AGGRESSIVE,
                            matched_keywords=[],
                            matched_patterns=[],
                            feature_scores={"semantic_score": round(getattr(r, "relevance", 0.5), 4)},
                        ))
                        break
        return candidates
    except Exception as exc:
        logger.warning(f"Semantic retrieval failed: {exc}")
        return []


def _deep_analysis(text: str, features: StructuralFeatures, top_k: int) -> Tuple[List[ClassificationCandidate], List[str]]:
    """Layer 3: Deep analysis with full reasoning chain for ambiguous documents."""
    reasoning: List[str] = []
    text_lower = text.lower()

    reasoning.append(f"Deep analysis initiated. Document: {features.word_count} words, ~{features.estimated_pages} pages.")

    if features.header_text:
        reasoning.append(f"Header text: '{features.header_text[:100]}'")

    # Analyze structural composition
    struct_signals: Dict[str, float] = {}
    if features.has_granting_clause and features.has_legal_description:
        struct_signals["conveyance"] = 0.8
        reasoning.append("Conveyance signals: granting clause + legal description present.")
    if features.has_habendum:
        struct_signals["lease"] = 0.7
        reasoning.append("Lease signal: habendum clause detected.")
    if features.has_notary_block and not features.has_granting_clause:
        struct_signals["affidavit"] = 0.6
        reasoning.append("Affidavit signal: notary block without granting clause.")
    if features.has_consideration:
        struct_signals["transaction"] = 0.5
        reasoning.append("Transaction signal: consideration recital present.")

    # Count category-level evidence
    cat_evidence: Dict[str, float] = defaultdict(float)
    for dt_key, dt_info in DOCUMENT_TYPES.items():
        evidence = 0.0
        for kw in dt_info["keywords"]:
            if kw.lower() in text_lower:
                evidence += 1.0 / len(dt_info["keywords"])
        for pat in _COMPILED_PATTERNS[dt_key]:
            if pat.search(text_lower):
                evidence += 1.5 / len(dt_info["regex"])
        if evidence > 0:
            cat_evidence[dt_key] = evidence

    if not cat_evidence:
        reasoning.append("No keyword or pattern matches found. Document type is UNKNOWN.")
        return [ClassificationCandidate(
            doc_type="UNKNOWN",
            display_name="Unknown Document Type",
            category="MISCELLANEOUS",
            confidence=0.1,
            stratum=ConfidenceStratum.HIGH_RISK,
            matched_keywords=[],
            matched_patterns=[],
            feature_scores={"deep_analysis": 0.1},
        )], reasoning

    # Rank by evidence
    sorted_evidence = sorted(cat_evidence.items(), key=lambda x: x[1], reverse=True)
    max_ev = sorted_evidence[0][1] if sorted_evidence[0][1] > 0 else 1.0

    candidates: List[ClassificationCandidate] = []
    for dt_key, ev in sorted_evidence[:top_k]:
        dt_info = DOCUMENT_TYPES[dt_key]
        conf = min(0.85, ev / max_ev * 0.85)  # Deep analysis caps at 0.85 confidence
        reasoning.append(f"  {dt_info['display']}: evidence={ev:.3f}, confidence={conf:.3f}")
        candidates.append(ClassificationCandidate(
            doc_type=dt_key,
            display_name=dt_info["display"],
            category=dt_info["category"].value,
            confidence=round(conf, 4),
            stratum=stratify_confidence(conf, 0.4),
            matched_keywords=[],
            matched_patterns=[],
            feature_scores={"deep_evidence": round(ev, 4)},
        ))

    reasoning.append(f"Deep analysis complete. Top classification: {candidates[0].display_name} ({candidates[0].confidence:.1%})")
    return candidates, reasoning


# ═══════════════════════════════════════════════════════════════════════════
# TIE-08: TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TelemetryCollector:
    total_queries: int = 0
    total_latency_ms: float = 0.0
    tier_counts: Dict[str, int] = dc_field(default_factory=lambda: defaultdict(int))
    type_counts: Dict[str, int] = dc_field(default_factory=lambda: defaultdict(int))
    category_counts: Dict[str, int] = dc_field(default_factory=lambda: defaultdict(int))
    stratum_counts: Dict[str, int] = dc_field(default_factory=lambda: defaultdict(int))
    error_count: int = 0
    latency_buckets: List[float] = dc_field(default_factory=list)
    _start_time: float = dc_field(default_factory=time.time)

    def record(self, result: ClassificationResult) -> None:
        self.total_queries += 1
        self.total_latency_ms += result.latency_ms
        self.tier_counts[result.tier_used.value] += 1
        self.type_counts[result.primary_type] += 1
        self.category_counts[DOCUMENT_TYPES.get(result.primary_type, {}).get("category", DocCategory.MISCELLANEOUS).value if isinstance(DOCUMENT_TYPES.get(result.primary_type, {}).get("category"), DocCategory) else "MISCELLANEOUS"] += 1
        self.stratum_counts[result.primary_stratum.value] += 1
        self.latency_buckets.append(result.latency_ms)
        if len(self.latency_buckets) > 10000:
            self.latency_buckets = self.latency_buckets[-5000:]

    def record_error(self) -> None:
        self.error_count += 1

    @property
    def avg_latency_ms(self) -> float:
        if not self.latency_buckets:
            return 0.0
        return sum(self.latency_buckets) / len(self.latency_buckets)

    @property
    def p95_latency_ms(self) -> float:
        if not self.latency_buckets:
            return 0.0
        s = sorted(self.latency_buckets)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self._start_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "error_count": self.error_count,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "uptime_seconds": round(self.uptime_seconds, 1),
            "tier_distribution": dict(self.tier_counts),
            "top_types": dict(Counter(self.type_counts).most_common(10)),
            "category_distribution": dict(self.category_counts),
            "stratum_distribution": dict(self.stratum_counts),
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════
# TIE-09: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DriftWatcher:
    """Detect classification drift: if distribution changes significantly over time."""
    window_size: int = 500
    recent_types: List[str] = dc_field(default_factory=list)
    baseline: Optional[Dict[str, float]] = None
    alerts: List[Dict[str, Any]] = dc_field(default_factory=list)

    def record(self, doc_type: str) -> None:
        self.recent_types.append(doc_type)
        if len(self.recent_types) > self.window_size * 2:
            self.recent_types = self.recent_types[-self.window_size:]

    def check_drift(self) -> Optional[Dict[str, Any]]:
        """Check for distribution drift. Returns alert dict if drift detected."""
        if len(self.recent_types) < self.window_size:
            return None

        current_dist = Counter(self.recent_types[-self.window_size:])
        total = sum(current_dist.values())
        current_pct = {k: v / total for k, v in current_dist.items()}

        if self.baseline is None:
            self.baseline = current_pct
            return None

        # Chi-squared-like divergence
        divergence = 0.0
        all_types = set(list(self.baseline.keys()) + list(current_pct.keys()))
        for t in all_types:
            expected = self.baseline.get(t, 0.01)
            observed = current_pct.get(t, 0.0)
            divergence += (observed - expected) ** 2 / max(expected, 0.01)

        if divergence > 0.5:
            alert = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "divergence": round(divergence, 4),
                "shifted_types": {
                    t: {"baseline": round(self.baseline.get(t, 0), 4), "current": round(current_pct.get(t, 0), 4)}
                    for t in all_types
                    if abs(current_pct.get(t, 0) - self.baseline.get(t, 0)) > 0.05
                },
            }
            self.alerts.append(alert)
            logger.warning(f"Classification drift detected: divergence={divergence:.4f}")
            return alert
        return None

    @property
    def alert_count(self) -> int:
        return len(self.alerts)


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════
# TIE-10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoverageMap:
    """Track which document types have been seen vs never classified."""
    seen_types: Set[str] = dc_field(default_factory=set)
    seen_count: Dict[str, int] = dc_field(default_factory=lambda: defaultdict(int))
    unknown_count: int = 0

    def record(self, doc_type: str) -> None:
        if doc_type == "UNKNOWN":
            self.unknown_count += 1
        else:
            self.seen_types.add(doc_type)
            self.seen_count[doc_type] += 1

    @property
    def coverage_pct(self) -> float:
        total = len(DOCUMENT_TYPES)
        return len(self.seen_types) / total if total > 0 else 0.0

    @property
    def unseen_types(self) -> List[str]:
        return [dt for dt in DOCUMENT_TYPES if dt not in self.seen_types]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_types": len(DOCUMENT_TYPES),
            "seen_types": len(self.seen_types),
            "coverage_pct": round(self.coverage_pct * 100, 1),
            "unseen_types": self.unseen_types,
            "unknown_count": self.unknown_count,
            "type_frequency": dict(Counter(self.seen_count).most_common(15)),
        }


COVERAGE_MAP = CoverageMap()


# ═══════════════════════════════════════════════════════════════════════════
# TIE-15: AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════

def write_audit_entry(result: ClassificationResult, request_text_hash: str) -> None:
    """Append classification result to JSONL audit trail."""
    entry = {
        "timestamp": result.timestamp,
        "query_id": result.query_id,
        "input_hash": request_text_hash,
        "primary_type": result.primary_type,
        "primary_confidence": result.primary_confidence,
        "primary_stratum": result.primary_stratum.value,
        "tier_used": result.tier_used.value,
        "fragility": result.fragility_score,
        "determinism_hash": result.determinism_hash,
        "latency_ms": result.latency_ms,
        "mode": result.mode.value,
        "zone": result.zone.value,
        "candidate_count": len(result.candidates),
        "engine_version": result.engine_version,
    }
    try:
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit trail write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN CLASSIFICATION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

async def classify_document(req: ClassificationRequest) -> ClassificationResult:
    """Full three-layer classification pipeline."""
    t0 = time.perf_counter()
    query_id = str(uuid.uuid4())
    text_lower = normalize_text(req.text)
    reasoning: List[str] = []

    # Extract structural features
    features = extract_structural_features(req.text)

    # --- Layer 1: Doctrine Cache ---
    candidates, tier = _classify_doctrine_cache(text_lower, req.top_k)
    candidates = _classify_structural(req.text, features, candidates)

    if candidates and candidates[0].confidence >= 0.6:
        tier = ClassificationTier.DOCTRINE_CACHE
        if req.include_reasoning:
            reasoning.append(f"Doctrine cache hit: {candidates[0].display_name} at {candidates[0].confidence:.1%}")
    else:
        # --- Layer 2: Semantic Retrieval ---
        if req.mode != ResponseMode.FAST:
            reasoning.append("Doctrine cache insufficient. Attempting semantic retrieval.")
            sem_candidates = await _classify_semantic(req.text, req.top_k)
            if sem_candidates:
                # Merge semantic with doctrine candidates
                existing_types = {c.doc_type for c in candidates}
                for sc in sem_candidates:
                    if sc.doc_type not in existing_types:
                        candidates.append(sc)
                candidates.sort(key=lambda x: x.confidence, reverse=True)
                tier = ClassificationTier.SEMANTIC_RETRIEVAL

        # --- Layer 3: Deep Analysis ---
        if not candidates or candidates[0].confidence < 0.4:
            reasoning.append("Semantic retrieval insufficient. Running deep analysis.")
            deep_cands, deep_reasoning = _deep_analysis(req.text, features, req.top_k)
            reasoning.extend(deep_reasoning)
            if deep_cands:
                existing_types = {c.doc_type for c in candidates}
                for dc in deep_cands:
                    if dc.doc_type not in existing_types:
                        candidates.append(dc)
                    else:
                        for i, c in enumerate(candidates):
                            if c.doc_type == dc.doc_type:
                                candidates[i].confidence = max(c.confidence, dc.confidence)
                                break
                candidates.sort(key=lambda x: x.confidence, reverse=True)
                tier = ClassificationTier.DEEP_ANALYSIS

    # Fallback: unknown
    if not candidates:
        candidates = [ClassificationCandidate(
            doc_type="UNKNOWN",
            display_name="Unknown Document Type",
            category="MISCELLANEOUS",
            confidence=0.05,
            stratum=ConfidenceStratum.HIGH_RISK,
            matched_keywords=[],
            matched_patterns=[],
            feature_scores={},
        )]
        tier = ClassificationTier.DEEP_ANALYSIS

    # Trim to top_k
    candidates = candidates[:req.top_k]

    # Compute fragility and re-stratify top candidate
    fragility = compute_fragility(candidates)
    top = candidates[0]
    top.stratum = stratify_confidence(top.confidence, fragility)

    # Determinism hash
    det_hash = compute_determinism_hash(req.text, candidates)

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    result = ClassificationResult(
        query_id=query_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        primary_type=top.doc_type,
        primary_display=top.display_name,
        primary_confidence=top.confidence,
        primary_stratum=top.stratum,
        candidates=candidates,
        tier_used=tier,
        structural_features=features,
        mode=req.mode,
        zone=req.zone,
        reasoning=reasoning if req.include_reasoning else None,
        determinism_hash=det_hash,
        latency_ms=latency_ms,
        fragility_score=fragility,
    )

    # Telemetry / drift / coverage / audit
    TELEMETRY.record(result)
    DRIFT_WATCHER.record(top.doc_type)
    COVERAGE_MAP.record(top.doc_type)
    input_hash = hashlib.sha256(req.text.encode()).hexdigest()[:16]
    write_audit_entry(result, input_hash)

    logger.info(
        f"Classified: {top.display_name} ({top.confidence:.1%}) | "
        f"tier={tier.value} | latency={latency_ms}ms | fragility={fragility:.3f} | "
        f"query_id={query_id}"
    )

    return result


# ═══════════════════════════════════════════════════════════════════════════
# TIE-13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def format_for_zone(result: ClassificationResult) -> Dict[str, Any]:
    """Format result according to analysis zone."""
    base = result.model_dump()

    if result.zone == AnalysisZone.PLANNING:
        # Planning zone: focus on what the document IS, minimal detail
        return {
            "query_id": result.query_id,
            "primary_type": result.primary_type,
            "primary_display": result.primary_display,
            "primary_confidence": result.primary_confidence,
            "category": result.candidates[0].category if result.candidates else "UNKNOWN",
            "structural_features": {
                "has_legal_description": result.structural_features.has_legal_description,
                "extracted_county": result.structural_features.extracted_county,
            },
        }
    elif result.zone == AnalysisZone.AUDIT:
        # Audit zone: full detail including hash, fragility, audit trail
        return base
    else:
        # Reporting zone: balanced
        return {
            "query_id": result.query_id,
            "timestamp": result.timestamp,
            "primary_type": result.primary_type,
            "primary_display": result.primary_display,
            "primary_confidence": result.primary_confidence,
            "primary_stratum": result.primary_stratum.value,
            "candidates": [c.model_dump() for c in result.candidates[:3]],
            "tier_used": result.tier_used.value,
            "structural_features": result.structural_features.model_dump(),
            "determinism_hash": result.determinism_hash,
            "latency_ms": result.latency_ms,
            "fragility_score": result.fragility_score,
        }


# ═══════════════════════════════════════════════════════════════════════════
# TIE-02: RESPONSE MODE FORMATTING
# ═══════════════════════════════════════════════════════════════════════════

def format_for_mode(result: ClassificationResult) -> Dict[str, Any]:
    """Format result according to response mode."""
    if result.mode == ResponseMode.FAST:
        return {
            "query_id": result.query_id,
            "type": result.primary_type,
            "display": result.primary_display,
            "confidence": result.primary_confidence,
            "stratum": result.primary_stratum.value,
            "latency_ms": result.latency_ms,
        }
    elif result.mode == ResponseMode.DEFENSE:
        return {
            "query_id": result.query_id,
            "timestamp": result.timestamp,
            "classification": {
                "type": result.primary_type,
                "display": result.primary_display,
                "confidence": result.primary_confidence,
                "stratum": result.primary_stratum.value,
                "fragility": result.fragility_score,
            },
            "candidates": [c.model_dump() for c in result.candidates],
            "tier_used": result.tier_used.value,
            "structural_evidence": result.structural_features.model_dump(),
            "determinism_hash": result.determinism_hash,
            "reasoning": result.reasoning,
            "audit_note": f"Classification logged to {AUDIT_LOG.name}",
        }
    else:  # MEMO
        doctrine = _DOCTRINE_INDEX.get(result.primary_type)
        return {
            "query_id": result.query_id,
            "timestamp": result.timestamp,
            "memo": {
                "subject": f"Document Classification: {result.primary_display}",
                "classification": result.primary_type,
                "confidence": f"{result.primary_confidence:.1%}",
                "stratum": result.primary_stratum.value,
                "fragility": f"{result.fragility_score:.1%}",
                "conclusion": doctrine.conclusion_template if doctrine else "Classification based on pattern analysis.",
                "reasoning": doctrine.reasoning_framework if doctrine else None,
                "key_factors": doctrine.key_factors if doctrine else [],
                "authority": doctrine.primary_authority if doctrine else [],
            },
            "alternatives": [
                {"type": c.display_name, "confidence": f"{c.confidence:.1%}"}
                for c in result.candidates[1:4]
            ],
            "structural_evidence": result.structural_features.model_dump(),
            "all_candidates": [c.model_dump() for c in result.candidates],
            "determinism_hash": result.determinism_hash,
            "reasoning_chain": result.reasoning,
            "engine": {"id": ENGINE_ID, "version": ENGINE_VERSION, "tier": result.tier_used.value},
        }


# ═══════════════════════════════════════════════════════════════════════════
# TIE-19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════

async def multi_classify(texts: List[str], mode: ResponseMode = ResponseMode.FAST, top_k: int = 3) -> List[Dict[str, Any]]:
    """Classify multiple documents in parallel. Returns list of formatted results."""
    tasks = [
        classify_document(ClassificationRequest(text=t, mode=mode, top_k=top_k))
        for t in texts
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    output: List[Dict[str, Any]] = []
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            logger.error(f"Multi-classify item {i} failed: {r}")
            output.append({"index": i, "error": str(r)})
        else:
            output.append({"index": i, **format_for_mode(r)})
    return output


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (TIE-17)
# ═══════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"E01 Document Classifier v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Loaded {len(DOCUMENT_TYPES)} document types, {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Compiled {sum(len(v) for v in _COMPILED_PATTERNS.values())} regex patterns")
    yield
    logger.info("E01 Document Classifier shutting down")


app = FastAPI(
    title=f"{ENGINE_ID} {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Production document classification engine with TIE-20 architecture",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- TIE-12: Health Endpoint ---
@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        uptime_seconds=round(TELEMETRY.uptime_seconds, 1),
        total_classifications=TELEMETRY.total_queries,
        cache_hit_rate=round(
            TELEMETRY.tier_counts.get("DOCTRINE_CACHE", 0) / max(TELEMETRY.total_queries, 1), 4
        ),
        avg_latency_ms=round(TELEMETRY.avg_latency_ms, 2),
        drift_alerts=DRIFT_WATCHER.alert_count,
        coverage_pct=round(COVERAGE_MAP.coverage_pct * 100, 1),
    )


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "operational",
        "port": ENGINE_PORT,
        "document_types": len(DOCUMENT_TYPES),
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "endpoints": ["/health", "/classify", "/query", "/batch", "/types", "/metrics", "/drift", "/coverage"],
    }


# --- Primary classification endpoint ---
@app.post("/classify")
async def classify_endpoint(req: ClassificationRequest) -> Dict[str, Any]:
    try:
        result = await classify_document(req)
        formatted = format_for_mode(result)
        if req.zone != AnalysisZone.REPORTING:
            formatted = format_for_zone(result)
        return formatted
    except Exception as exc:
        TELEMETRY.record_error()
        logger.error(f"Classification error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


# --- Query endpoint (TIE standard /query) ---
@app.post("/query")
async def query_endpoint(req: QueryRequest) -> Dict[str, Any]:
    try:
        cls_req = ClassificationRequest(
            text=req.query,
            mode=req.mode,
            zone=req.zone,
            top_k=req.top_k,
            include_reasoning=req.include_reasoning,
            session_id=req.session_id,
        )
        result = await classify_document(cls_req)
        return format_for_mode(result)
    except Exception as exc:
        TELEMETRY.record_error()
        logger.error(f"Query error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


# --- Batch classification ---
@app.post("/batch")
async def batch_endpoint(request: Request) -> Dict[str, Any]:
    body = await request.json()
    texts = body.get("documents", [])
    mode = ResponseMode(body.get("mode", "FAST"))
    top_k = body.get("top_k", 3)
    if not texts:
        raise HTTPException(status_code=400, detail="No documents provided")
    if len(texts) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 documents per batch")
    results = await multi_classify(texts, mode=mode, top_k=top_k)
    return {"count": len(results), "results": results}


# --- Document types reference ---
@app.get("/types")
async def types_endpoint() -> Dict[str, Any]:
    types_list = []
    for dt_key, dt_info in DOCUMENT_TYPES.items():
        types_list.append({
            "key": dt_key,
            "display": dt_info["display"],
            "category": dt_info["category"].value,
            "description": dt_info["description"],
            "keyword_count": len(dt_info["keywords"]),
            "pattern_count": len(dt_info["regex"]),
        })
    categories = sorted(set(dt["category"].value for dt in DOCUMENT_TYPES.values()))
    return {
        "total_types": len(DOCUMENT_TYPES),
        "categories": categories,
        "types": types_list,
    }


# --- TIE-11: Metrics ---
@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "version": ENGINE_VERSION,
        **TELEMETRY.to_dict(),
    }


# --- TIE-09: Drift ---
@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    alert = DRIFT_WATCHER.check_drift()
    return {
        "alert_count": DRIFT_WATCHER.alert_count,
        "current_alert": alert,
        "recent_alerts": DRIFT_WATCHER.alerts[-5:] if DRIFT_WATCHER.alerts else [],
        "window_size": DRIFT_WATCHER.window_size,
        "samples_collected": len(DRIFT_WATCHER.recent_types),
    }


# --- TIE-10: Coverage ---
@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    return COVERAGE_MAP.to_dict()


# --- Doctrine cache inspection ---
@app.get("/doctrines")
async def doctrines_endpoint() -> Dict[str, Any]:
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "doc_type": d.doc_type_key,
                "category": d.category.value,
                "confidence": d.confidence,
                "stratum": d.stratum.value,
                "keyword_count": len(d.keywords),
                "authority_count": len(d.primary_authority),
            }
            for d in DOCTRINE_CACHE
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Launching {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        reload=False,
        log_level="info",
    )
