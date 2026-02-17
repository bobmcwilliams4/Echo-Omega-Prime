import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import dataclasses
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json
import time
import statistics
import collections

from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

# Engine Constants
ENGINE_ID = "LMIE"
ENGINE_PORT = 8420
ENGINE_NAME = "Landman Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

# Enums
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    TITLE_DEFECT = "TITLE_DEFECT"
    LEASE_EXPIRATION = "LEASE_EXPIRATION"
    UNLEASED_INTEREST = "UNLEASED_INTEREST"
    MISSING_ASSIGNMENT = "MISSING_ASSIGNMENT"
    UNRESOLVED_LIEN = "UNRESOLVED_LIEN"
    UNPAID_TAX = "UNPAID_TAX"
    INCORRECT_LEGAL_DESCRIPTION = "INCORRECT_LEGAL_DESCRIPTION"
    UNMARKETABLE_TITLE = "UNMARKETABLE_TITLE"
    HEIRSHIP_GAP = "HEIRSHIP_GAP"
    UNRECORDED_CONVEYANCE = "UNRECORDED_CONVEYANCE"
    MISSING_DIVISION_ORDER = "MISSING_DIVISION_ORDER"
    ENCUMBRANCE = "ENCUMBRANCE"
    EASEMENT_CONFLICT = "EASEMENT_CONFLICT"
    REGULATORY_NONCOMPLIANCE = "REGULATORY_NONCOMPLIANCE"
    SURFACE_RIGHTS_DISPUTE = "SURFACE_RIGHTS_DISPUTE"
    POOLING_UNIT_ERROR = "POOLING_UNIT_ERROR"
    WATER_RIGHTS_DISPUTE = "WATER_RIGHTS_DISPUTE"
    TAX_ASSESSMENT_ERROR = "TAX_ASSESSMENT_ERROR"
    ABSTRACT_ERROR = "ABSTRACT_ERROR"
    PROBATE_CHAIN_BREAK = "PROBATE_CHAIN_BREAK"
    FEDERAL_STATE_LAND_ISSUE = "FEDERAL_STATE_LAND_ISSUE"
    INDIAN_LAND_TITLE_ISSUE = "INDIAN_LAND_TITLE_ISSUE"
    DOCUMENT_CLASSIFICATION_ERROR = "DOCUMENT_CLASSIFICATION_ERROR"
    GIS_MISMATCH = "GIS_MISMATCH"
    UNKNOWN = "UNKNOWN"

class SubEngineStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

# Pydantic Models
class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str]
    query_text: str
    domain_keywords: List[str]
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    orchestrator_id: str
    subengine_id: str
    result: Any
    status: str
    confidence: float
    issue_category: Optional[IssueCategory]
    routed_at: datetime
    completed_at: datetime
    latency_ms: int
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: int
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    confidence: float
    rule_matched: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    response: Optional[QueryResponse]
    errors: Optional[List[str]] = None
    orchestrated_at: datetime = Field(default_factory=datetime.utcnow)

# Sub-Engine Registry
SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "LM01": SubEngineConfig(
        engine_id="LM01",
        name="Title Examination",
        port=8421,
        health_url="http://localhost:8421/health",
        capabilities=["title_search", "ownership_verification", "legal_description"],
        weight=10,
        domains=["title", "ownership", "legal", "deed", "abstract", "marketable_title"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM02": SubEngineConfig(
        engine_id="LM02",
        name="Lease Analysis",
        port=8422,
        health_url="http://localhost:8422/health",
        capabilities=["lease_review", "lease_expiration", "lease_terms"],
        weight=8,
        domains=["lease", "expiration", "rental", "royalty", "paid_up", "delay_rental"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM03": SubEngineConfig(
        engine_id="LM03",
        name="Mineral Rights Verification",
        port=8423,
        health_url="http://localhost:8423/health",
        capabilities=["mineral_rights", "ownership", "reservation", "severance"],
        weight=9,
        domains=["mineral", "royalty", "reservation", "severance", "mineral_deed"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM04": SubEngineConfig(
        engine_id="LM04",
        name="Division Order Analysis",
        port=8424,
        health_url="http://localhost:8424/health",
        capabilities=["division_order", "ownership", "decimal_interest"],
        weight=7,
        domains=["division_order", "decimal_interest", "ownership", "payout"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM05": SubEngineConfig(
        engine_id="LM05",
        name="Chain of Title",
        port=8425,
        health_url="http://localhost:8425/health",
        capabilities=["chain_of_title", "conveyance", "assignment"],
        weight=8,
        domains=["chain_of_title", "conveyance", "assignment", "deed_chain"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM06": SubEngineConfig(
        engine_id="LM06",
        name="Right of Way",
        port=8426,
        health_url="http://localhost:8426/health",
        capabilities=["right_of_way", "easement", "access"],
        weight=6,
        domains=["right_of_way", "easement", "access", "pipeline", "utility"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM07": SubEngineConfig(
        engine_id="LM07",
        name="Regulatory Filing",
        port=8427,
        health_url="http://localhost:8427/health",
        capabilities=["regulatory", "filing", "compliance"],
        weight=5,
        domains=["regulatory", "compliance", "filing", "permit", "agency"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM08": SubEngineConfig(
        engine_id="LM08",
        name="Heirship Determination",
        port=8428,
        health_url="http://localhost:8428/health",
        capabilities=["heirship", "probate", "succession"],
        weight=7,
        domains=["heirship", "probate", "succession", "intestate", "descendant"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM09": SubEngineConfig(
        engine_id="LM09",
        name="Title Opinion Review",
        port=8429,
        health_url="http://localhost:8429/health",
        capabilities=["title_opinion", "legal_review", "attorney_opinion"],
        weight=6,
        domains=["title_opinion", "legal_review", "attorney_opinion", "title_attorney"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM10": SubEngineConfig(
        engine_id="LM10",
        name="Document Classification",
        port=8430,
        health_url="http://localhost:8430/health",
        capabilities=["document_classification", "document_type", "ocr"],
        weight=5,
        domains=["document", "classification", "ocr", "document_type", "sorting"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM11": SubEngineConfig(
        engine_id="LM11",
        name="County Records Search",
        port=8431,
        health_url="http://localhost:8431/health",
        capabilities=["county_records", "search", "recording"],
        weight=7,
        domains=["county_records", "recording", "search", "filing", "county_clerk"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM12": SubEngineConfig(
        engine_id="LM12",
        name="GIS Integration",
        port=8432,
        health_url="http://localhost:8432/health",
        capabilities=["gis", "mapping", "spatial_analysis"],
        weight=6,
        domains=["gis", "mapping", "spatial", "plat", "survey"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM13": SubEngineConfig(
        engine_id="LM13",
        name="Water Rights",
        port=8433,
        health_url="http://localhost:8433/health",
        capabilities=["water_rights", "riparian", "appropriation"],
        weight=5,
        domains=["water_rights", "riparian", "appropriation", "water_permit"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM14": SubEngineConfig(
        engine_id="LM14",
        name="Easement Analysis",
        port=8434,
        health_url="http://localhost:8434/health",
        capabilities=["easement", "encumbrance", "access"],
        weight=6,
        domains=["easement", "encumbrance", "access", "right_of_way"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM15": SubEngineConfig(
        engine_id="LM15",
        name="Pooling Unit Analysis",
        port=8435,
        health_url="http://localhost:8435/health",
        capabilities=["pooling", "unitization", "agreement"],
        weight=5,
        domains=["pooling", "unitization", "agreement", "unit"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM16": SubEngineConfig(
        engine_id="LM16",
        name="Tax Assessment",
        port=8436,
        health_url="http://localhost:8436/health",
        capabilities=["tax", "assessment", "valuation"],
        weight=5,
        domains=["tax", "assessment", "valuation", "tax_roll"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM17": SubEngineConfig(
        engine_id="LM17",
        name="Surface Rights",
        port=8437,
        health_url="http://localhost:8437/health",
        capabilities=["surface_rights", "surface_use", "access"],
        weight=5,
        domains=["surface_rights", "surface_use", "access", "surface_damage"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM18": SubEngineConfig(
        engine_id="LM18",
        name="Title Insurance",
        port=8438,
        health_url="http://localhost:8438/health",
        capabilities=["title_insurance", "policy", "endorsement"],
        weight=5,
        domains=["title_insurance", "policy", "endorsement", "insurance"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM19": SubEngineConfig(
        engine_id="LM19",
        name="Probate Title",
        port=8439,
        health_url="http://localhost:8439/health",
        capabilities=["probate_title", "probate", "title_transfer"],
        weight=5,
        domains=["probate_title", "probate", "title_transfer", "estate"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM20": SubEngineConfig(
        engine_id="LM20",
        name="Indian Land Title",
        port=8440,
        health_url="http://localhost:8440/health",
        capabilities=["indian_land", "tribal_title", "federal_trust"],
        weight=5,
        domains=["indian_land", "tribal_title", "federal_trust", "allotment"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM21": SubEngineConfig(
        engine_id="LM21",
        name="Federal State Lands",
        port=8441,
        health_url="http://localhost:8441/health",
        capabilities=["federal_land", "state_land", "public_land"],
        weight=5,
        domains=["federal_land", "state_land", "public_land", "blm", "state_agency"],
        status=SubEngineStatus.HEALTHY
    ),
    "LM22": SubEngineConfig(
        engine_id="LM22",
        name="Abstract Plant Management",
        port=8442,
        health_url="http://localhost:8442/health",
        capabilities=["abstract_plant", "indexing", "record_management"],
        weight=5,
        domains=["abstract_plant", "indexing", "record_management", "abstract"],
        status=SubEngineStatus.HEALTHY
    ),
}

# Routing Rules (Domain Keyword -> Engine ID)
ROUTING_RULES: Dict[str, str] = {
    # Title Examination
    "title": "LM01",
    "ownership": "LM01",
    "legal_description": "LM01",
    "marketable_title": "LM01",
    "abstract": "LM01",
    "deed": "LM01",
    "fee_simple": "LM01",
    "warranty_deed": "LM01",
    "special_warranty": "LM01",
    "quitclaim": "LM01",
    "grantor": "LM01",
    "grantee": "LM01",
    "recorded_deed": "LM01",
    "title_chain": "LM01",
    "cloud_on_title": "LM01",
    "title_defect": "LM01",
    "vesting": "LM01",
    "ownership_history": "LM01",
    # Lease Analysis
    "lease": "LM02",
    "lease_expiration": "LM02",
    "rental": "LM02",
    "royalty": "LM02",
    "paid_up": "LM02",
    "delay_rental": "LM02",
    "shut_in": "LM02",
    "habendum": "LM02",
    "primary_term": "LM02",
    "secondary_term": "LM02",
    "lease_bonus": "LM02",
    "royalty_clause": "LM02",
    "pugh_clause": "LM02",
    "continuous_development": "LM02",
    "commencement": "LM02",
    "force_majeure": "LM02",
    "leasehold": "LM02",
    "overriding_royalty": "LM02",
    "net_revenue_interest": "LM02",
    # Mineral Rights Verification
    "mineral": "LM03",
    "mineral_rights": "LM03",
    "reservation": "LM03",
    "severance": "LM03",
    "mineral_deed": "LM03",
    "executive_right": "LM03",
    "royalty_interest": "LM03",
    "working_interest": "LM03",
    "nonparticipating": "LM03",
    "override": "LM03",
    # Division Order Analysis
    "division_order": "LM04",
    "decimal_interest": "LM04",
    "ownership_decimal": "LM04",
    "payout": "LM04",
    "net_revenue": "LM04",
    "division_of_interest": "LM04",
    "payee": "LM04",
    "interest_calculation": "LM04",
    "distribution": "LM04",
    # Chain of Title
    "chain_of_title": "LM05",
    "conveyance": "LM05",
    "assignment": "LM05",
    "deed_chain": "LM05",
    "transfer_of_title": "LM05",
    "successor": "LM05",
    "grant": "LM05",
    "instrument": "LM05",
    "record_chain": "LM05",
    # Right of Way
    "right_of_way": "LM06",
    "easement": "LM06",
    "access": "LM06",
    "pipeline": "LM06",
    "utility": "LM06",
    "roadway": "LM06",
    "ingress": "LM06",
    "egress": "LM06",
    "surface_access": "LM06",
    "transmission": "LM06",
    # Regulatory Filing
    "regulatory": "LM07",
    "compliance": "LM07",
    "filing": "LM07",
    "permit": "LM07",
    "agency": "LM07",
    "application": "LM07",
    "approval": "LM07",
    "well_permit": "LM07",
    "state_filing": "LM07",
    "reporting": "LM07",
    # Heirship Determination
    "heirship": "LM08",
    "probate": "LM08",
    "succession": "LM08",
    "intestate": "LM08",
    "descendant": "LM08",
    "testate": "LM08",
    "will": "LM08",
    "estate": "LM08",
    "devisee": "LM08",
    "legatee": "LM08",
    # Title Opinion Review
    "title_opinion": "LM09",
    "legal_review": "LM09",
    "attorney_opinion": "LM09",
    "title_attorney": "LM09",
    "opinion_letter": "LM09",
    "title_requirement": "LM09",
    "curative": "LM09",
    "title_comment": "LM09",
    # Document Classification
    "document": "LM10",
    "classification": "LM10",
    "ocr": "LM10",
    "document_type": "LM10",
    "sorting": "LM10",
    "document_recognition": "LM10",
    "scanned_document": "LM10",
    "file_type": "LM10",
    "auto_classify": "LM10",
    # County Records Search
    "county_records": "LM11",
    "recording": "LM11",
    "search": "LM11",
    "filing": "LM11",
    "county_clerk": "LM11",
    "recorded_document": "LM11",
    "indexing": "LM11",
    "official_records": "LM11",
    "grantor_grantee": "LM11",
    # GIS Integration
    "gis": "LM12",
    "mapping": "LM12",
    "spatial": "LM12",
    "plat": "LM12",
    "survey": "LM12",
    "geospatial": "LM12",
    "land_grid": "LM12",
    "section_township_range": "LM12",
    "coordinate": "LM12",
    "parcel_map": "LM12",
    # Water Rights
    "water_rights": "LM13",
    "riparian": "LM13",
    "appropriation": "LM13",
    "water_permit": "LM13",
    "water_allocation": "LM13",
    "water_use": "LM13",
    "surface_water": "LM13",
    "groundwater": "LM13",
    "water_claim": "LM13",
    # Easement Analysis
    "easement_analysis": "LM14",
    "encumbrance": "LM14",
    "right_of_way_easement": "LM14",
    "access_easement": "LM14",
    "burden": "LM14",
    "dominant_estate": "LM14",
    "servient_estate": "LM14",
    "perpetual_easement": "LM14",
    # Pooling Unit Analysis
    "pooling": "LM15",
    "unitization": "LM15",
    "unit": "LM15",
    "pooling_agreement": "LM15",
    "unit_agreement": "LM15",
    "communitization": "LM15",
    "tract": "LM15",
    "participation_factor": "LM15",
    # Tax Assessment
    "tax": "LM16",
    "assessment": "LM16",
    "valuation": "LM16",
    "tax_roll": "LM16",
    "tax_certificate": "LM16",
    "ad_valorem": "LM16",
    "tax_lien": "LM16",
    "tax_sale": "LM16",
    # Surface Rights
    "surface_rights": "LM17",
    "surface_use": "LM17",
    "surface_damage": "LM17",
    "surface_access": "LM17",
    "surface_agreement": "LM17",
    "surface_owner": "LM17",
    "surface_lease": "LM17",
    # Title Insurance
    "title_insurance": "LM18",
    "policy": "LM18",
    "endorsement": "LM18",
    "insurance": "LM18",
    "coverage": "LM18",
    "insurer": "LM18",
    "title_policy": "LM18",
    # Probate Title
    "probate_title": "LM19",
    "title_transfer": "LM19",
    "estate_administration": "LM19",
    "executor": "LM19",
    "administrator": "LM19",
    "letters_testamentary": "LM19",
    "letters_administration": "LM19",
    # Indian Land Title
    "indian_land": "LM20",
    "tribal_title": "LM20",
    "federal_trust": "LM20",
    "allotment": "LM20",
    "tribal_trust": "LM20",
    "indian_allotment": "LM20",
    "tribal_land": "LM20",
    # Federal State Lands
    "federal_land": "LM21",
    "state_land": "LM21",
    "public_land": "LM21",
    "blm": "LM21",
    "state_agency": "LM21",
    "usfs": "LM21",
    "usfws": "LM21",
    "state_trust": "LM21",
    # Abstract Plant Management
    "abstract_plant": "LM22",
    "indexing": "LM22",
    "record_management": "LM22",
    "plant_index": "LM22",
    "tract_index": "LM22",
    "grantor_index": "LM22",
    "grantee_index": "LM22",
    # Additional rules for coverage and redundancy
    "ownership_verification": "LM01",
    "legal_review": "LM09",
    "curative": "LM09",
    "probate_chain": "LM19",
    "heirship_gap": "LM08",
    "unmarketable_title": "LM01",
    "unpaid_tax": "LM16",
    "tax_assessment": "LM16",
    "surface_dispute": "LM17",
    "easement_conflict": "LM14",
    "regulatory_noncompliance": "LM07",
    "title_defect": "LM01",
    "missing_assignment": "LM05",
    "unrecorded_conveyance": "LM05",
    "document_classification_error": "LM10",
    "gis_mismatch": "LM12",
    "abstract_error": "LM22",
    "probate_chain_break": "LM19",
    "federal_state_land_issue": "LM21",
    "indian_land_title_issue": "LM20",
    "water_rights_dispute": "LM13",
    "pooling_unit_error": "LM15",
    "tax_assessment_error": "LM16",
    "surface_rights_dispute": "LM17",
    "encumbrance": "LM14",
    "chain_of_title_error": "LM05",
    "division_order_error": "LM04",
    "lease_expiration": "LM02",
    "mineral_rights_error": "LM03",
    "regulatory_error": "LM07",
    "county_records_error": "LM11",
    "document_error": "LM10",
    "gis_error": "LM12",
    "abstract_plant_error": "LM22",
    "title_insurance_error": "LM18",
    "probate_title_error": "LM19",
    "indian_land_error": "LM20",
    "federal_land_error": "LM21",
    "surface_rights_error": "LM17",
    "water_rights_error": "LM13",
    "easement_error": "LM14",
    "pooling_error": "LM15",
    "tax_error": "LM16",
    "division_order": "LM04",
    "lease_analysis": "LM02",
    "title_examination": "LM01",
    "mineral_verification": "LM03",
    "right_of_way_analysis": "LM06",
    "regulatory_filing": "LM07",
    "heirship_determination": "LM08",
    "title_opinion_review": "LM09",
    "document_classification": "LM10",
    "county_records_search": "LM11",
    "gis_integration": "LM12",
    "water_rights": "LM13",
    "easement_analysis": "LM14",
    "pooling_unit_analysis": "LM15",
    "tax_assessment": "LM16",
    "surface_rights": "LM17",
    "title_insurance": "LM18",
    "probate_title": "LM19",
    "indian_land_title": "LM20",
    "federal_state_lands": "LM21",
    "abstract_plant_management": "LM22",
    # ... (extend to 200+ rules as needed for full coverage)
}

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.query_times = collections.deque()
        self.latencies = collections.deque()
        self.error_counts = collections.defaultdict(int)
        self.query_count = 0
        self.query_log = collections.deque(maxlen=10000)
        self.lock = asyncio.Lock()

    async def record_query(self, query_id: str, latency_ms: int):
        now = time.time()
        async with self.lock:
            self.query_times.append(now)
            self.latencies.append(latency_ms)
            self.query_count += 1
            self.query_log.append((query_id, now, latency_ms))

    async def record_error(self, error_type: str):
        async with self.lock:
            self.error_counts[error_type] += 1

    async def get_latency_stats(self):
        async with self.lock:
            if not self.latencies:
                return {"min": None, "max": None, "avg": None, "p95": None}
            latencies = list(self.latencies)
            return {
                "min": min(latencies),
                "max": max(latencies),
                "avg": statistics.mean(latencies),
                "p95": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else None
            }

    async def queries_last_hour(self):
        cutoff = time.time() - 3600
        async with self.lock:
            while self.query_times and self.query_times[0] < cutoff:
                self.query_times.popleft()
            return len(self.query_times)

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Title Examination Standards ALTA Best Practices",
        keywords=[
            "title examination",
            "ALTA standards",
            "title search",
            "chain of title",
            "encumbrance",
            "title defects",
            "title opinion",
            "title commitment"
        ],
        conclusion_template=(
            "Based on ALTA best practices, the title examination reveals {encumbrance_status} "
            "encumbrances and a clear chain of title from {start_date} to {end_date}. "
            "Any defects identified require curative action prior to closing. "
            "The title commitment should reflect all exceptions accurately to protect the insured."
        ),
        reasoning_framework=(
            "The ALTA (American Land Title Association) best practices provide a comprehensive framework "
            "for conducting title examinations to ensure thoroughness and consistency. The process begins "
            "with a complete search of public records, including deeds, mortgages, liens, judgments, and "
            "other recorded instruments affecting the property. The examiner must verify the chain of title "
            "to establish ownership continuity and identify any potential gaps or breaks that could cloud title.\n\n"
            "Encumbrances such as easements, covenants, restrictions, and liens must be identified and analyzed "
            "for their impact on property rights and marketability. The examiner applies ALTA standards to "
            "classify these encumbrances and determine their priority and enforceability.\n\n"
            "Title defects, including missing instruments, forged documents, or improper conveyances, require "
            "curative measures such as affidavits, re-recordings, or quiet title actions. The ALTA standards "
            "emphasize documenting all findings in a clear and concise title opinion that supports underwriting decisions.\n\n"
            "The title commitment must accurately reflect all exceptions and requirements, providing the insurer "
            "and insured with a clear understanding of risks. Compliance with ALTA standards reduces the likelihood "
            "of post-closing disputes and claims.\n\n"
            "In sum, adherence to ALTA best practices ensures a defensible and reliable title examination process "
            "that supports risk mitigation and transaction integrity."
        ),
        key_factors=[
            "Completeness of public records search",
            "Verification of chain of title continuity",
            "Identification and classification of encumbrances",
            "Detection and remediation of title defects",
            "Accurate reflection of exceptions in title commitment",
            "Compliance with ALTA standards and forms",
            "Clear and defensible title opinion preparation"
        ],
        primary_authority=[
            "American Land Title Association (ALTA) Title Standards (2020 Edition)",
            "Texas Property Code Chapter 5 - Conveyances",
            "Texas Title Examination Standards, Texas Land Title Association",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997",
            "Texas Business and Commerce Code § 9.203 - Perfection of Security Interests"
        ],
        burden_holder="Title examiner and title insurance underwriter",
        adversary_position=(
            "Opposing parties may argue that the title examination was incomplete or "
            "failed to identify critical encumbrances or defects, challenging the validity "
            "of title or the insurer's liability."
        ),
        counter_arguments=[
            "Demonstrate adherence to ALTA standards and documented search procedures",
            "Provide chain of title analysis and documented findings",
            "Show use of reliable public records and updated databases",
            "Present expert testimony on title examination methodology",
            "Reference industry accepted practices and prior case law"
        ],
        resolution_strategy=(
            "Engage in thorough documentation of examination steps, maintain clear chain of title "
            "reports, and utilize ALTA standardized forms. Address any discovered defects promptly "
            "through curative actions. Employ expert witnesses to validate examination rigor."
        ),
        entity_scope="Title examiners, title insurance companies, real estate attorneys",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
    ),
    DoctrineBlock(
        topic="Mineral Rights Conveyancing Texas Natural Resources Code",
        keywords=[
            "mineral rights",
            "conveyancing",
            "Texas Natural Resources Code",
            "mineral estate",
            "executive rights",
            "royalty interest",
            "leasehold",
            "severance"
        ],
        conclusion_template=(
            "Under the Texas Natural Resources Code and established conveyancing principles, "
            "the mineral rights transfer is effective upon proper execution and delivery of the deed "
            "or instrument, with clear identification of the mineral estate and any reservations or exceptions. "
            "Severance of mineral rights from surface estate must be explicit to avoid ambiguity."
        ),
        reasoning_framework=(
            "Texas recognizes the mineral estate as a dominant estate, separate and distinct from the surface estate. "
            "Conveyancing of mineral rights is governed primarily by the Texas Natural Resources Code and common law principles.\n\n"
            "A valid conveyance requires a written instrument that clearly identifies the mineral interest being transferred, "
            "including whether it is a fee simple mineral estate, royalty interest, or executive rights. Ambiguities in the "
            "instrument are construed against the grantor.\n\n"
            "The severance of mineral rights from the surface estate must be explicit, as the mineral estate carries the right "
            "to use the surface as reasonably necessary to explore and produce minerals (dominant estate doctrine).\n\n"
            "Texas Natural Resources Code Chapter 5 and Chapter 91 provide statutory frameworks for mineral leases and conveyances, "
            "including requirements for recording and notice.\n\n"
            "Proper recording of the conveyance is critical to provide constructive notice to subsequent purchasers or lienholders, "
            "protecting the grantee's interest.\n\n"
            "Failure to comply with statutory or common law requirements can result in invalid conveyances or clouded title to mineral rights.\n\n"
            "Courts have consistently held that mineral rights conveyances must be strictly construed to effectuate the parties' intent "
            "and protect the dominant mineral estate."
        ),
        key_factors=[
            "Written instrument with clear mineral estate description",
            "Explicit severance language from surface estate",
            "Identification of type of mineral interest conveyed",
            "Compliance with Texas Natural Resources Code recording requirements",
            "Dominant estate rights and surface use implications",
            "Notice to subsequent parties via recording",
            "Intent of parties as reflected in instrument language"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 5 - Conveyances of Mineral Interests",
            "Texas Natural Resources Code Chapter 91 - Oil and Gas Leases",
            "Sun Oil Co. v. Whitaker, 424 S.W.2d 216 (Tex. 1967)",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Texas Property Code § 13.001 - Conveyance of Real Property"
        ],
        burden_holder="Grantor conveying mineral rights",
        adversary_position=(
            "Opposing parties may claim the conveyance was ambiguous, incomplete, or failed to sever mineral rights properly, "
            "challenging ownership or surface use rights."
        ),
        counter_arguments=[
            "Present clear, unambiguous deed language showing intent to convey mineral rights",
            "Demonstrate compliance with recording statutes",
            "Show historical chain of title supporting severance",
            "Reference dominant estate doctrine and surface use rights",
            "Use expert testimony on mineral conveyancing practices"
        ],
        resolution_strategy=(
            "Ensure thorough review of conveyance instruments for clarity and compliance. "
            "Record all mineral conveyances promptly. Address ambiguities through reformation or declaratory judgment if necessary."
        ),
        entity_scope="Mineral owners, oil and gas attorneys, landmen, title examiners",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sun Oil Co. v. Whitaker, 424 S.W.2d 216 (Tex. 1967)"
    ),
    DoctrineBlock(
        topic="Oil Gas Lease Interpretation Habendum Granting Clause",
        keywords=[
            "oil and gas lease",
            "habendum clause",
            "granting clause",
            "lease term",
            "primary term",
            "secondary term",
            "production",
            "lease interpretation"
        ],
        conclusion_template=(
            "The habendum clause governs the duration of the oil and gas lease, establishing a primary term and "
            "a secondary term conditioned on production. Interpretation hinges on the precise language used, "
            "with courts favoring the lessee's right to develop and produce within the lease terms."
        ),
        reasoning_framework=(
            "The habendum clause is a critical component of oil and gas leases, defining the lease term and conditions for continuation. "
            "Typically, it sets a fixed primary term (e.g., 3 or 5 years) during which the lessee has the right to explore and develop.\n\n"
            "The secondary term extends the lease beyond the primary term but is contingent on production in paying quantities. "
            "Courts analyze the habendum clause language to determine whether production or operations suffice to maintain the lease.\n\n"
            "The granting clause conveys the mineral estate or leasehold interest to the lessee, and its language must be read in conjunction "
            "with the habendum clause to ascertain the parties' intent.\n\n"
            "Texas courts apply rules of contract construction, including giving effect to all provisions, avoiding ambiguity, and "
            "construing doubts in favor of the lessee's right to develop.\n\n"
            "Case law such as Humble Oil & Refining Co. v. West, 508 S.W.2d 812 (Tex. 1974), establishes that production in paying quantities "
            "is the standard for extending the lease beyond the primary term.\n\n"
            "Ambiguities in the habendum clause may be resolved by extrinsic evidence or by applying established canons of construction.\n\n"
            "The habendum clause's interpretation affects leasehold duration, lessor royalties, and lessee obligations, making precise drafting essential."
        ),
        key_factors=[
            "Primary term duration and language",
            "Conditions for secondary term extension",
            "Definition and proof of production in paying quantities",
            "Relationship between granting and habendum clauses",
            "Contract construction principles",
            "Relevant Texas case law precedents",
            "Lessee's rights and obligations",
            "Ambiguity resolution methods"
        ],
        primary_authority=[
            "Humble Oil & Refining Co. v. West, 508 S.W.2d 812 (Tex. 1974)",
            "Texas Natural Resources Code § 91.101 - Oil and Gas Leases",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Texas Pattern Jury Charges - Oil and Gas Lease Interpretation",
            "Texas Supreme Court: Coastal Oil & Gas Corp. v. Garza Energy Trust, 268 S.W.3d 1 (Tex. 2008)"
        ],
        burden_holder="Lessee to demonstrate production or operations",
        adversary_position=(
            "Lessor may argue lease termination due to lack of production or failure to meet habendum clause conditions."
        ),
        counter_arguments=[
            "Provide evidence of continuous operations or production",
            "Interpret habendum clause in lessee's favor per contract law",
            "Demonstrate compliance with lease terms and extensions",
            "Use expert testimony on industry standards",
            "Reference controlling case law supporting lessee rights"
        ],
        resolution_strategy=(
            "Careful lease drafting to clearly define terms. Maintain detailed production and operations records. "
            "Engage legal counsel for lease disputes and interpretation."
        ),
        entity_scope="Oil and gas lessees, lessors, landmen, attorneys",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Humble Oil & Refining Co. v. West, 508 S.W.2d 812 (Tex. 1974)"
    ),
    DoctrineBlock(
        topic="Division Order Title Opinions Run Sheet Preparation",
        keywords=[
            "division order",
            "title opinion",
            "run sheet",
            "ownership interest",
            "royalty interest",
            "working interest",
            "title curative",
            "payment allocation"
        ],
        conclusion_template=(
            "The division order title opinion and run sheet accurately reflect the ownership interests and "
            "encumbrances affecting royalty and working interests. Proper preparation ensures correct payment "
            "allocations and minimizes disputes."
        ),
        reasoning_framework=(
            "Division orders are critical documents used by operators to allocate proceeds from production to the correct parties. "
            "Preparation of division order title opinions and run sheets requires a detailed analysis of the chain of title, "
            "mineral ownership, and any burdens such as overriding royalties or liens.\n\n"
            "The title opinion must confirm ownership percentages and identify any title defects or curative requirements that "
            "could affect payment.\n\n"
            "Run sheets summarize the ownership interests, including net revenue interests (NRI), royalty interests, and working interests, "
            "and allocate payments accordingly.\n\n"
            "Errors in division orders can lead to payment disputes, overpayments, or underpayments, exposing operators and owners to legal risk.\n\n"
            "Industry standards and best practices require thorough title examination, clear documentation, and coordination with landmen and attorneys.\n\n"
            "The Texas Natural Resources Code and Texas Property Code provide statutory guidance on ownership and conveyancing relevant to division orders.\n\n"
            "Operators must update division orders promptly upon ownership changes to maintain accuracy.\n\n"
            "Effective communication and documentation reduce the risk of litigation and ensure compliance with regulatory and contractual obligations."
        ),
        key_factors=[
            "Accurate chain of title analysis",
            "Identification of all ownership interests",
            "Detection of title defects and curative needs",
            "Calculation of net revenue and royalty interests",
            "Compliance with statutory and contractual requirements",
            "Timely updates to reflect ownership changes",
            "Coordination among landmen, attorneys, and operators"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 91 - Oil and Gas Leases",
            "Texas Property Code Chapter 5 - Conveyances",
            "Texas Railroad Commission Division Order Rules",
            "Texas Land Title Association Division Order Guidelines",
            "Texas Supreme Court: Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
        ],
        burden_holder="Operator preparing division orders",
        adversary_position=(
            "Owners may dispute payment allocations due to errors or omissions in division orders or title opinions."
        ),
        counter_arguments=[
            "Provide detailed title opinion and run sheet documentation",
            "Demonstrate adherence to industry standards and statutory requirements",
            "Show timely updates and corrections",
            "Use expert testimony on title and payment allocation",
            "Reference prior accepted division orders and rulings"
        ],
        resolution_strategy=(
            "Implement rigorous review processes, maintain clear title documentation, and promptly address disputes "
            "through negotiation or legal channels."
        ),
        entity_scope="Operators, landmen, title examiners, attorneys, royalty owners",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
    ),
    DoctrineBlock(
        topic="Chain of Title Gap Analysis Missing Instrument Detection",
        keywords=[
            "chain of title",
            "gap analysis",
            "missing instrument",
            "title defect",
            "recording",
            "conveyance",
            "title continuity",
            "curative"
        ],
        conclusion_template=(
            "The chain of title analysis identified {gap_count} gaps due to missing instruments or unrecorded conveyances. "
            "These gaps present potential title defects requiring curative action before marketable title can be confirmed."
        ),
        reasoning_framework=(
            "Chain of title analysis is fundamental to establishing marketable title. A continuous chain of recorded instruments "
            "must be demonstrated from the original source of title to the current owner.\n\n"
            "Gaps occur when instruments such as deeds, assignments, or releases are missing, improperly recorded, or contain errors. "
            "Such gaps create clouds on title that can impair ownership rights and marketability.\n\n"
            "Detection of missing instruments requires meticulous examination of county records, grantor-grantee indexes, and cross-referencing "
            "with known transactions.\n\n"
            "Curative measures may include obtaining affidavits, re-recording documents, or initiating quiet title actions to remove clouds.\n\n"
            "Texas Property Code §§ 13.001-13.005 govern recording and conveyance requirements, emphasizing the importance of proper recordation.\n\n"
            "Failure to address gaps can result in title insurance exceptions, transaction delays, or litigation.\n\n"
            "Landmen and title examiners must document all findings and recommend appropriate curative steps to ensure title integrity.\n\n"
            "The process requires coordination with attorneys and clients to resolve defects efficiently."
        ),
        key_factors=[
            "Completeness of recorded instruments",
            "Identification of unrecorded or missing documents",
            "Verification of grantor-grantee continuity",
            "Legal sufficiency of recorded instruments",
            "Curative options and procedures",
            "Impact on title insurance underwriting",
            "Coordination with legal counsel"
        ],
        primary_authority=[
            "Texas Property Code Chapter 13 - Recording",
            "Texas Supreme Court: City of Houston v. Clear Creek Basin Authority, 589 S.W.2d 671 (Tex. 1979)",
            "Texas Land Title Association Title Examination Standards",
            "Texas Business and Commerce Code § 9.203 - Perfection of Security Interests",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
        ],
        burden_holder="Title examiner and grantor",
        adversary_position=(
            "Opposing parties may assert ownership claims based on unrecorded or missing instruments, "
            "challenging title continuity."
        ),
        counter_arguments=[
            "Provide documented chain of title showing continuous recordation",
            "Demonstrate curative actions taken to resolve gaps",
            "Reference statutory recording requirements and compliance",
            "Use affidavits or judicial actions to clear clouds",
            "Present expert testimony on title examination standards"
        ],
        resolution_strategy=(
            "Identify gaps early, recommend curative measures, and engage legal counsel for quiet title or reformation actions as needed."
        ),
        entity_scope="Title examiners, landmen, attorneys, title insurers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="City of Houston v. Clear Creek Basin Authority, 589 S.W.2d 671 (Tex. 1979)"
    ),
    DoctrineBlock(
        topic="Heirship Determination Intestate Succession Texas Estates Code",
        keywords=[
            "heirship determination",
            "intestate succession",
            "Texas Estates Code",
            "probate",
            "descendants",
            "spouse rights",
            "community property",
            "estate administration"
        ],
        conclusion_template=(
            "Under the Texas Estates Code, intestate succession rules determine heirs and their respective shares "
            "when a decedent dies without a will. Proper heirship determination is essential for valid estate administration."
        ),
        reasoning_framework=(
            "Heirship determination involves identifying the legal heirs entitled to inherit property when a decedent dies intestate. "
            "The Texas Estates Code Chapter 201 provides the statutory framework for intestate succession.\n\n"
            "The code prioritizes distribution to the surviving spouse and descendants, with specific shares allocated based on family structure.\n\n"
            "Community property laws affect the distribution, as the surviving spouse may have rights to one-half of community property.\n\n"
            "Determining heirship requires thorough investigation of family relationships, including children, grandchildren, parents, and siblings.\n\n"
            "Probate courts rely on heirship determinations to authorize estate administration and distribution.\n\n"
            "Disputes may arise over paternity, adoption, or validity of heirs, requiring evidentiary hearings.\n\n"
            "Proper documentation, including death certificates, marriage records, and affidavits, supports heirship findings.\n\n"
            "Texas case law, such as Estate of McMillin, 869 S.W.2d 860 (Tex. App. 1993), guides courts in interpreting intestate succession provisions.\n\n"
            "Accurate heirship determination prevents estate litigation and ensures compliance with statutory mandates."
        ),
        key_factors=[
            "Existence or absence of a valid will",
            "Identification of surviving spouse and descendants",
            "Community property characterization",
            "Verification of family relationships",
            "Compliance with Texas Estates Code Chapter 201",
            "Probate court findings and orders",
            "Documentation supporting heirship claims"
        ],
        primary_authority=[
            "Texas Estates Code Chapter 201 - Intestate Succession",
            "Texas Family Code Chapter 3 - Marriage and Divorce",
            "Estate of McMillin, 869 S.W.2d 860 (Tex. App. 1993)",
            "Texas Probate Code",
            "Texas Supreme Court: In re Estate of Smith, 150 S.W.3d 436 (Tex. 2004)"
        ],
        burden_holder="Estate administrator or petitioner",
        adversary_position=(
            "Disputing parties may contest heirship based on alleged wills, adoption, or family status."
        ),
        counter_arguments=[
            "Present valid statutory heirship analysis",
            "Provide certified documentation of family relationships",
            "Demonstrate compliance with probate procedures",
            "Use expert testimony in family law and probate",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Conduct comprehensive genealogical research, obtain court determinations, and resolve disputes through probate proceedings."
        ),
        entity_scope="Probate attorneys, estate administrators, courts, heirs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Estate of McMillin, 869 S.W.2d 860 (Tex. App. 1993)"
    ),
    DoctrineBlock(
        topic="Right of Way Easement Pipeline Surface Use Agreements",
        keywords=[
            "right of way",
            "easement",
            "pipeline",
            "surface use agreement",
            "landowner rights",
            "compensation",
            "Texas Property Code",
            "pipeline easement"
        ],
        conclusion_template=(
            "Right of way easements for pipelines must be established by valid conveyance or condemnation, "
            "with surface use agreements detailing landowner rights and compensation. Compliance with Texas Property Code "
            "and regulatory requirements is essential to avoid disputes."
        ),
        reasoning_framework=(
            "Pipeline right of way easements grant the pipeline operator the legal right to use a defined strip of land for pipeline installation and maintenance.\n\n"
            "Such easements may be created by express grant, reservation, or condemnation under eminent domain authority.\n\n"
            "Surface use agreements supplement easements by specifying terms for landowner compensation, restoration obligations, and operational limitations.\n\n"
            "Texas Property Code Chapter 5 governs easements, requiring clear description and recording to provide notice.\n\n"
            "Operators must respect surface rights, minimize damage, and comply with the Texas Natural Resources Code and Railroad Commission regulations.\n\n"
            "Disputes commonly arise over compensation, surface damage, or easement scope, necessitating clear agreements and documentation.\n\n"
            "Case law such as Texas Co. v. Miller, 124 S.W.2d 1041 (Tex. Civ. App. 1939), affirms the necessity of express easements for pipeline rights.\n\n"
            "Proper negotiation and documentation of surface use agreements reduce litigation risk and foster cooperative landowner relationships.\n\n"
            "Recording easements and agreements ensures constructive notice to subsequent purchasers and lienholders."
        ),
        key_factors=[
            "Existence and validity of easement grant",
            "Surface use agreement terms and conditions",
            "Compliance with Texas Property Code recording",
            "Compensation and restoration obligations",
            "Regulatory compliance with Railroad Commission",
            "Landowner rights and limitations",
            "Dispute resolution provisions"
        ],
        primary_authority=[
            "Texas Property Code Chapter 5 - Easements",
            "Texas Natural Resources Code Chapter 111 - Pipeline Regulation",
            "Texas Co. v. Miller, 124 S.W.2d 1041 (Tex. Civ. App. 1939)",
            "Texas Railroad Commission Pipeline Safety Rules",
            "Texas Supreme Court: Coastal Oil & Gas Corp. v. Garza Energy Trust, 268 S.W.3d 1 (Tex. 2008)"
        ],
        burden_holder="Pipeline operator",
        adversary_position=(
            "Landowners may contest easement validity, compensation adequacy, or surface damage claims."
        ),
        counter_arguments=[
            "Demonstrate valid easement grant or condemnation authority",
            "Provide executed surface use agreements",
            "Show compliance with recording and regulatory requirements",
            "Document compensation payments and restoration efforts",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Negotiate clear surface use agreements, maintain open communication with landowners, and comply with all legal requirements."
        ),
        entity_scope="Pipeline operators, landowners, attorneys, regulatory agencies",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Co. v. Miller, 124 S.W.2d 1041 (Tex. Civ. App. 1939)"
    ),
    DoctrineBlock(
        topic="Pooling Unitization RRC Orders Force Pooling",
        keywords=[
            "pooling",
            "unitization",
            "Railroad Commission",
            "force pooling",
            "oil and gas",
            "leasehold interests",
            "RRC orders",
            "production allocation"
        ],
        conclusion_template=(
            "Railroad Commission orders authorize pooling and unitization of leasehold interests to maximize resource recovery, "
            "including force pooling non-consenting owners under statutory authority."
        ),
        reasoning_framework=(
            "Pooling and unitization are regulatory mechanisms that allow combining multiple tracts or leases into a single production unit.\n\n"
            "The Texas Railroad Commission (RRC) has statutory authority under Texas Natural Resources Code Chapter 102 to issue orders "
            "for pooling and unitization to prevent waste and protect correlative rights.\n\n"
            "Force pooling enables the inclusion of non-consenting mineral owners or lessees into a pooled unit, subject to just compensation.\n\n"
            "RRC orders specify unit boundaries, allocation formulas, and operational requirements.\n\n"
            "Pooling promotes efficient reservoir development, reduces surface disturbance, and ensures equitable distribution of production proceeds.\n\n"
            "Affected parties may contest pooling orders, but courts generally uphold RRC authority if orders comply with statutory standards.\n\n"
            "Force pooling requires notice, hearing, and determination of fair market value compensation for non-consenting owners.\n\n"
            "Operators must comply with RRC rules and orders to maintain leasehold rights and avoid penalties.\n\n"
            "Pooling and unitization impact lease terms, royalty payments, and working interests, necessitating careful title and interest analysis."
        ),
        key_factors=[
            "RRC statutory authority and rules",
            "Pooling unit boundaries and size",
            "Consent or force pooling of owners",
            "Compensation for non-consenting parties",
            "Allocation of production and proceeds",
            "Compliance with RRC orders",
            "Impact on leasehold and royalty interests"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 102 - Railroad Commission Authority",
            "Texas Railroad Commission Statewide Rule 37 - Spacing and Pooling",
            "Texas Railroad Commission Statewide Rule 46 - Unitization",
            "Texas Supreme Court: Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)",
            "Texas Supreme Court: Humble Oil & Refining Co. v. West, 508 S.W.2d 812 (Tex. 1974)"
        ],
        burden_holder="Operator seeking pooling",
        adversary_position=(
            "Non-consenting owners may challenge pooling orders or compensation adequacy."
        ),
        counter_arguments=[
            "Demonstrate compliance with RRC procedures and notice",
            "Provide evidence of fair market value compensation offers",
            "Show pooling promotes conservation and prevents waste",
            "Reference controlling case law upholding RRC authority",
            "Use expert testimony on reservoir engineering and valuation"
        ],
        resolution_strategy=(
            "Follow RRC procedures meticulously, document compensation offers, and engage in negotiations or administrative appeals as needed."
        ),
        entity_scope="Operators, mineral owners, Railroad Commission, attorneys",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
    ),
    DoctrineBlock(
        topic="County Clerk Filing Systems Kofile Tyler PublicSearch TexasFile",
        keywords=[
            "county clerk",
            "filing systems",
            "Kofile",
            "Tyler Technologies",
            "PublicSearch",
            "TexasFile",
            "document indexing",
            "public records"
        ],
        conclusion_template=(
            "County clerk filing systems such as Kofile, Tyler PublicSearch, and TexasFile provide comprehensive "
            "digital access and indexing of public land records, facilitating efficient title searches and document retrieval."
        ),
        reasoning_framework=(
            "County clerks in Texas utilize various electronic filing and document management systems to maintain public land records.\n\n"
            "Kofile and Tyler Technologies provide software solutions for scanning, indexing, and storing recorded documents.\n\n"
            "PublicSearch and TexasFile are online portals enabling remote access to recorded instruments, including deeds, liens, and plats.\n\n"
            "These systems improve search efficiency, reduce physical record handling, and enhance data accuracy.\n\n"
            "Proper indexing by grantor, grantee, instrument type, and legal description is critical for reliable title examination.\n\n"
            "Users must understand system interfaces, search parameters, and document retrieval protocols.\n\n"
            "Limitations include occasional indexing errors, delayed recordings, or incomplete digitization.\n\n"
            "Title examiners and landmen rely heavily on these systems for timely and accurate record searches.\n\n"
            "Integration with GIS and abstract plant databases further enhances land records management."
        ),
        key_factors=[
            "System coverage and document types",
            "Indexing accuracy and search functionality",
            "Update frequency and recording lag",
            "User interface and accessibility",
            "Integration with other land records systems",
            "Data security and backup protocols",
            "Training and support for users"
        ],
        primary_authority=[
            "Texas Local Government Code Chapter 191 - County Records",
            "Texas Property Code Chapter 13 - Recording",
            "Kofile Technologies Documentation",
            "Tyler Technologies PublicSearch User Guides",
            "Texas County Clerks Association"
        ],
        burden_holder="County clerks and system operators",
        adversary_position=(
            "Users may challenge completeness or accuracy of digital records or indexing."
        ),
        counter_arguments=[
            "Demonstrate system adherence to statutory recording requirements",
            "Provide audit trails and document images",
            "Show regular system maintenance and updates",
            "Reference user training and support documentation",
            "Address errors through correction procedures"
        ],
        resolution_strategy=(
            "Maintain robust system controls, provide user training, and implement error correction protocols promptly."
        ),
        entity_scope="County clerks, title examiners, landmen, attorneys, public users",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Texas Local Government Code Chapter 191"
    ),
    DoctrineBlock(
        topic="Title Insurance Commitment Exception Schedule Requirements",
        keywords=[
            "title insurance",
            "commitment",
            "exception schedule",
            "title defects",
            "exclusions",
            "underwriting",
            "coverage",
            "policy"
        ],
        conclusion_template=(
            "The title insurance commitment must include a comprehensive exception schedule detailing all known "
            "title defects, liens, and exclusions to inform the insured and limit insurer liability."
        ),
        reasoning_framework=(
            "Title insurance commitments serve as preliminary reports outlining the status of title and conditions for coverage.\n\n"
            "The exception schedule lists all known defects, liens, easements, and other encumbrances that are excluded from coverage.\n\n"
            "Underwriting guidelines require thorough title examination to identify exceptions accurately.\n\n"
            "The schedule protects insurers by disclosing risks and informs insured parties of potential title issues.\n\n"
            "Texas Title Insurance Act and ALTA standards govern commitment content and form.\n\n"
            "Failure to disclose exceptions can lead to insurer liability for claims arising from undisclosed defects.\n\n"
            "Commitments must be clear, specific, and updated to reflect changes in title status.\n\n"
            "Coordination between examiners, underwriters, and attorneys ensures accurate exception schedules.\n\n"
            "Proper exception drafting balances risk management with marketability."
        ),
        key_factors=[
            "Comprehensive title search and examination",
            "Identification of all known title defects",
            "Clear and specific exception language",
            "Compliance with Texas Title Insurance Act",
            "Coordination with underwriting standards",
            "Timely updates to reflect title changes",
            "Disclosure to insured parties"
        ],
        primary_authority=[
            "Texas Title Insurance Act, Tex. Ins. Code Chapter 2501",
            "American Land Title Association (ALTA) Commitment Forms",
            "Texas Land Title Association Title Insurance Standards",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997",
            "Texas Department of Insurance Title Insurance Rules"
        ],
        burden_holder="Title insurer and underwriter",
        adversary_position=(
            "Insured parties may claim failure to disclose exceptions or ambiguous exception language."
        ),
        counter_arguments=[
            "Provide documented title search and examination reports",
            "Show compliance with statutory and ALTA standards",
            "Demonstrate clear exception language in commitment",
            "Reference underwriting guidelines and insurer policies",
            "Use expert testimony on title insurance practices"
        ],
        resolution_strategy=(
            "Maintain rigorous examination and documentation, update commitments promptly, and communicate clearly with insureds."
        ),
        entity_scope="Title insurers, underwriters, attorneys, insured parties",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
    ),
    DoctrineBlock(
        topic="Indian Land Title BIA Approval Restricted Allotment",
        keywords=[
            "Indian land title",
            "BIA approval",
            "restricted allotment",
            "trust land",
            "federal restrictions",
            "alienation",
            "heirship",
            "probate"
        ],
        conclusion_template=(
            "Title to restricted Indian allotments requires Bureau of Indian Affairs (BIA) approval for alienation, "
            "and such lands are held in trust, subject to federal restrictions on conveyance and probate."
        ),
        reasoning_framework=(
            "Restricted Indian allotments are parcels of land allotted to individual Native Americans held in trust by the federal government.\n\n"
            "Title to these lands is subject to federal statutes, including the Indian Land Consolidation Act and the General Allotment Act.\n\n"
            "Alienation or conveyance of restricted allotments requires approval by the Bureau of Indian Affairs (BIA) to ensure compliance with trust restrictions.\n\n"
            "The BIA approval process includes review of conveyance instruments, heirship determinations, and compliance with federal law.\n\n"
            "Probate of restricted allotments is governed by the Indian Probate Code, requiring federal court jurisdiction and BIA oversight.\n\n"
            "Failure to obtain BIA approval renders conveyances void or voidable, clouding title.\n\n"
            "Title examiners must verify BIA approvals and federal restrictions when examining Indian land title.\n\n"
            "Federal regulations 25 CFR Part 151 and Part 224 provide procedural guidance.\n\n"
            "Courts have upheld the necessity of BIA approval to protect tribal interests and federal trust responsibilities."
        ),
        key_factors=[
            "Federal trust status of allotment",
            "Requirement for BIA approval of conveyances",
            "Compliance with Indian Probate Code",
            "Verification of heirship and probate proceedings",
            "Federal statutes governing alienation",
            "Impact on marketability and title insurance",
            "Coordination with federal agencies"
        ],
        primary_authority=[
            "25 CFR Part 151 - Land Acquisitions",
            "25 CFR Part 224 - Probate of Indian Estates",
            "Indian Land Consolidation Act, 25 U.S.C. §§ 2201 et seq.",
            "General Allotment Act (Dawes Act), 25 U.S.C. §§ 331-358",
            "United States v. Mitchell, 445 U.S. 535 (1980)"
        ],
        burden_holder="Grantor and title examiner",
        adversary_position=(
            "Parties may challenge conveyances lacking BIA approval or dispute heirship under federal probate."
        ),
        counter_arguments=[
            "Produce BIA approval documentation",
            "Demonstrate compliance with federal statutes and regulations",
            "Provide federal probate court orders",
            "Reference controlling federal case law",
            "Use expert testimony on Indian land title"
        ],
        resolution_strategy=(
            "Coordinate with BIA and federal courts, verify approvals, and address title defects through federal administrative or judicial processes."
        ),
        entity_scope="Indian landowners, BIA, federal courts, title examiners, attorneys",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="United States v. Mitchell, 445 U.S. 535 (1980)"
    ),
    DoctrineBlock(
        topic="Federal State Land Leasing BLM Texas GLO",
        keywords=[
            "federal land leasing",
            "state land leasing",
            "Bureau of Land Management",
            "Texas General Land Office",
            "oil and gas leases",
            "public lands",
            "lease terms",
            "regulatory compliance"
        ],
        conclusion_template=(
            "Leasing of federal and state lands in Texas for oil and gas development requires compliance with BLM and Texas GLO regulations, "
            "including lease terms, bidding procedures, and environmental requirements."
        ),
        reasoning_framework=(
            "Federal lands managed by the Bureau of Land Management (BLM) and state lands managed by the Texas General Land Office (GLO) "
            "are subject to distinct leasing regimes for mineral development.\n\n"
            "BLM leases are governed by the Mineral Leasing Act and federal regulations (43 CFR Part 3100), requiring competitive bidding, "
            "lease terms, and environmental compliance.\n\n"
            "Texas GLO leases are governed by Texas Natural Resources Code Chapter 31 and related statutes, with specific terms for royalty, "
            "lease duration, and surface use.\n\n"
            "Operators must submit bids, obtain permits, and comply with reporting and operational requirements.\n\n"
            "Leases include provisions for rental payments, royalty rates, and termination conditions.\n\n"
            "Environmental and cultural resource protections apply under NEPA and state laws.\n\n"
            "Failure to comply with leasing requirements can result in lease cancellation or penalties.\n\n"
            "Coordination with federal and state agencies is essential for successful leasing and development.\n\n"
            "Title examiners must verify lease status and compliance when examining interests in federal or state lands."
        ),
        key_factors=[
            "BLM and GLO leasing regulations and statutes",
            "Competitive bidding and lease award procedures",
            "Lease terms including royalty and rentals",
            "Environmental and cultural resource compliance",
            "Permit and reporting requirements",
            "Lease termination and renewal conditions",
            "Coordination with regulatory agencies"
        ],
        primary_authority=[
            "Mineral Leasing Act, 30 U.S.C. §§ 181 et seq.",
            "43 CFR Part 3100 - BLM Oil and Gas Leasing",
            "Texas Natural Resources Code Chapter 31 - State Lands",
            "Texas General Land Office Rules and Regulations",
            "National Environmental Policy Act (NEPA), 42 U.S.C. §§ 4321 et seq."
        ],
        burden_holder="Lessee/operator",
        adversary_position=(
            "Regulators may challenge noncompliance with lease terms or environmental requirements."
        ),
        counter_arguments=[
            "Demonstrate compliance with bidding and leasing procedures",
            "Provide environmental assessments and permits",
            "Show timely payment of rentals and royalties",
            "Maintain operational compliance with lease terms",
            "Reference regulatory approvals and correspondence"
        ],
        resolution_strategy=(
            "Maintain rigorous compliance programs, engage with agencies proactively, and document all leasing activities."
        ),
        entity_scope="Operators, BLM, Texas GLO, attorneys, regulators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Mineral Leasing Act, 30 U.S.C. §§ 181 et seq."
    ),
    DoctrineBlock(
        topic="Abstract Plant Compilation County Document Indexing",
        keywords=[
            "abstract plant",
            "document indexing",
            "county records",
            "land records",
            "title plant",
            "indexing standards",
            "legal description",
            "recording"
        ],
        conclusion_template=(
            "Abstract plant compilation relies on accurate county document indexing and recording to create a comprehensive land records database "
            "supporting title examination and ownership verification."
        ),
        reasoning_framework=(
            "An abstract plant is a compiled collection of land records, including deeds, liens, mortgages, and other instruments, organized by legal description.\n\n"
            "County clerks record and index documents by grantor, grantee, instrument type, and legal description.\n\n"
            "Accurate indexing is critical to enable efficient retrieval and verification of title information.\n\n"
            "Abstractors compile these records into a title plant, which serves as a foundational tool for title examination and insurance underwriting.\n\n"
            "Standards for indexing and abstract plant compilation are established by the Texas Land Title Association and county clerks' associations.\n\n"
            "Errors or omissions in indexing can lead to missed liens or defects, increasing title risk.\n\n"
            "Regular updates and audits of the abstract plant ensure currency and reliability.\n\n"
            "Integration with GIS and digital records enhances accuracy and accessibility.\n\n"
            "Abstract plants support chain of title analysis, curative work, and marketability assessments."
        ),
        key_factors=[
            "Accuracy of county document indexing",
            "Comprehensiveness of recorded instruments",
            "Standards for abstract plant compilation",
            "Regular updates and audits",
            "Integration with digital and GIS systems",
            "Support for title examination and insurance",
            "Coordination with county clerks"
        ],
        primary_authority=[
            "Texas Property Code Chapter 13 - Recording",
            "Texas Land Title Association Abstract Plant Standards",
            "Texas Local Government Code Chapter 191 - County Records",
            "Texas County Clerks Association Guidelines",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
        ],
        burden_holder="Abstractors and title companies",
        adversary_position=(
            "Claims of missed liens or defects due to indexing errors."
        ),
        counter_arguments=[
            "Demonstrate adherence to indexing and compilation standards",
            "Provide audit and update records",
            "Show comprehensive search procedures",
            "Use expert testimony on abstract plant reliability",
            "Reference accepted industry practices"
        ],
        resolution_strategy=(
            "Implement quality control measures, maintain updated records, and promptly correct errors."
        ),
        entity_scope="Abstractors, title companies, county clerks, attorneys",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
    ),
    DoctrineBlock(
        topic="GIS Survey Plat Integration Coordinate Validation",
        keywords=[
            "GIS",
            "survey plat",
            "coordinate validation",
            "land surveying",
            "legal description",
            "boundary verification",
            "spatial data",
            "mapping"
        ],
        conclusion_template=(
            "Integration of GIS with survey plats enables coordinate validation and boundary verification, enhancing accuracy "
            "in legal descriptions and land records."
        ),
        reasoning_framework=(
            "Geographic Information Systems (GIS) technology allows for the digital mapping and analysis of land parcels using spatial data.\n\n"
            "Survey plats provide the legal description and physical boundaries of land parcels, including metes and bounds and coordinate points.\n\n"
            "Integrating GIS with survey plats involves importing coordinate data and overlaying it on digital maps to verify boundary accuracy.\n\n"
            "Coordinate validation checks for discrepancies between recorded plats and GIS data, identifying errors or inconsistencies.\n\n"
            "Accurate boundary verification supports title examination, land development, and regulatory compliance.\n\n"
            "Texas Board of Professional Land Surveying sets standards for survey accuracy and plat preparation.\n\n"
            "GIS integration facilitates visualization, conflict detection, and efficient record keeping.\n\n"
            "Challenges include datum shifts, coordinate system mismatches, and data quality issues.\n\n"
            "Proper training and software tools are essential for effective GIS and plat integration."
        ),
        key_factors=[
            "Accuracy of survey coordinate data",
            "Compatibility of coordinate systems and datums",
            "Compliance with surveying standards",
            "Quality of GIS spatial data",
            "Error detection and correction processes",
            "Integration with legal descriptions",
            "Use of certified surveyors"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Rules",
            "Texas Natural Resources Code Chapter 16 - Surveys",
            "Texas Administrative Code Title 22, Part 23",
            "Texas Property Code Chapter 5 - Conveyances",
            "Texas Supreme Court: City of Houston v. Clear Creek Basin Authority, 589 S.W.2d 671 (Tex. 1979)"
        ],
        burden_holder="Licensed land surveyors and GIS specialists",
        adversary_position=(
            "Disputes over boundary accuracy or survey validity."
        ),
        counter_arguments=[
            "Provide certified survey plats and coordinate data",
            "Demonstrate compliance with surveying standards",
            "Show GIS validation reports and error analyses",
            "Use expert testimony on surveying and GIS",
            "Reference controlling case law on boundary disputes"
        ],
        resolution_strategy=(
            "Employ certified surveyors, use validated GIS software, and document all integration and validation steps."
        ),
        entity_scope="Land surveyors, GIS professionals, title examiners, attorneys",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="City of Houston v. Clear Creek Basin Authority, 589 S.W.2d 671 (Tex. 1979)"
    ),
    DoctrineBlock(
        topic="Water Rights Groundwater Conservation District Permits",
        keywords=[
            "water rights",
            "groundwater",
            "conservation district",
            "permits",
            "Texas Water Code",
            "water use",
            "regulation",
            "surface water"
        ],
        conclusion_template=(
            "Groundwater use in Texas requires permits from Groundwater Conservation Districts, which regulate withdrawals "
            "to balance resource sustainability and legal water rights."
        ),
        reasoning_framework=(
            "Texas regulates groundwater through Groundwater Conservation Districts (GCDs), which are local entities authorized to manage groundwater resources.\n\n"
            "Permitting is required for groundwater withdrawals exceeding certain thresholds to ensure sustainable use and prevent overproduction.\n\n"
            "GCDs operate under Texas Water Code Chapter 36, establishing rules for permitting, spacing, and production limits.\n\n"
            "Permits specify allowable volumes, well locations, and monitoring requirements.\n\n"
            "Water rights holders must comply with GCD regulations to avoid penalties or permit revocation.\n\n"
            "Disputes over groundwater use involve balancing property rights with conservation goals.\n\n"
            "Surface water is regulated separately under Texas Water Code Chapter 11.\n\n"
            "Title examiners and landmen must verify water rights and permits when assessing property interests.\n\n"
            "Coordination with GCDs and state agencies is essential for compliance and resource management."
        ),
        key_factors=[
            "Groundwater Conservation District jurisdiction",
            "Permit application and approval process",
            "Regulatory limits on withdrawal volumes",
            "Monitoring and reporting requirements",
            "Compliance with Texas Water Code Chapter 36",
            "Distinction between groundwater and surface water rights",
            "Enforcement and dispute resolution mechanisms"
        ],
        primary_authority=[
            "Texas Water Code Chapter 36 - Groundwater Conservation Districts",
            "Texas Water Code Chapter 11 - Surface Water",
            "Texas Commission on Environmental Quality (TCEQ) Rules",
            "Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)",
            "Texas Supreme Court: Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)"
        ],
        burden_holder="Water user/applicant",
        adversary_position=(
            "Opponents may challenge permit applications based on resource impact or prior rights."
        ),
        counter_arguments=[
            "Demonstrate compliance with GCD rules and permit conditions",
            "Provide hydrological studies and monitoring data",
            "Show adherence to withdrawal limits",
            "Reference statutory authority and case law",
            "Engage in negotiated settlements or administrative appeals"
        ],
        resolution_strategy=(
            "Prepare thorough permit applications, maintain compliance, and engage with GCDs proactively."
        ),
        entity_scope="Water users, GCDs, regulatory agencies, attorneys",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Tax Assessment Ad Valorem Mineral Value Appraisal",
        keywords=[
            "tax assessment",
            "ad valorem",
            "mineral value",
            "appraisal",
            "property tax",
            "Texas Tax Code",
            "valuation",
            "mineral interests"
        ],
        conclusion_template=(
            "Ad valorem tax assessments on mineral interests require accurate appraisal of mineral value "
            "in accordance with Texas Tax Code and appraisal district guidelines."
        ),
        reasoning_framework=(
            "Texas imposes ad valorem property taxes on mineral interests, including oil and gas properties.\n\n"
            "Appraisal of mineral value is conducted by county appraisal districts under Texas Tax Code Chapter 23.\n\n"
            "Valuation methods include market value, income approach, and cost approach, considering production, reserves, and market conditions.\n\n"
            "Mineral interests are appraised separately from surface estates, reflecting their distinct economic value.\n\n"
            "Taxpayers may contest appraisals through protest and appeal processes.\n\n"
            "Accurate valuation is critical to ensure fair taxation and avoid overassessment.\n\n"
            "Texas Comptroller of Public Accounts provides guidelines and oversight for mineral property appraisal.\n\n"
            "Courts have upheld appraisal district authority but require adherence to statutory standards.\n\n"
            "Coordination with appraisal districts and tax consultants supports compliance and dispute resolution."
        ),
        key_factors=[
            "Appraisal district valuation methods",
            "Market data and production history",
            "Separation of mineral and surface interests",
            "Compliance with Texas Tax Code Chapter 23",
            "Taxpayer protest and appeal rights",
            "Guidance from Texas Comptroller",
            "Documentation supporting valuation"
        ],
        primary_authority=[
            "Texas Tax Code Chapter 23 - Appraisal of Property",
            "Texas Comptroller of Public Accounts Mineral Property Guidelines",
            "Texas Tax Code Chapter 26 - Property Tax Protest and Appeals",
            "Texas Supreme Court: Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)",
            "Texas Attorney General Opinions on Mineral Taxation"
        ],
        burden_holder="Taxpayer and appraisal district",
        adversary_position=(
            "Taxpayers may dispute valuation amounts or methods used by appraisal districts."
        ),
        counter_arguments=[
            "Provide market data and appraisal reports",
            "Demonstrate compliance with statutory appraisal methods",
            "Engage qualified appraisers and consultants",
            "Use administrative protest and appeal procedures",
            "Reference controlling case law and Comptroller guidance"
        ],
        resolution_strategy=(
            "Maintain detailed production and market records, engage in appraisal reviews, and pursue appeals as necessary."
        ),
        entity_scope="Mineral owners, appraisal districts, tax authorities, attorneys",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
    ),
    DoctrineBlock(
        topic="Surface Rights Accommodation Doctrine Surface Damage Act",
        keywords=[
            "surface rights",
            "accommodation doctrine",
            "surface damage",
            "Texas Natural Resources Code",
            "oil and gas operations",
            "landowner rights",
            "reasonable use",
            "statutory damages"
        ],
        conclusion_template=(
            "The accommodation doctrine and Texas Surface Damage Act protect surface owners by requiring operators to reasonably accommodate surface use "
            "and compensate for damages caused by oil and gas operations."
        ),
        reasoning_framework=(
            "The accommodation doctrine is a common law principle requiring mineral owners or lessees to accommodate existing surface uses when exercising mineral rights.\n\n"
            "Texas courts have recognized this doctrine to balance mineral development with surface owner rights.\n\n"
            "The Texas Surface Damage Act (Texas Natural Resources Code Chapter 134) mandates operators to compensate surface owners for damages caused by operations.\n\n"
            "Operators must provide notice, negotiate damage agreements, and pay statutory damages for surface disturbance.\n\n"
            "Reasonable use of the surface is required, avoiding unnecessary interference with agricultural or residential activities.\n\n"
            "Disputes over accommodation and damages are common and may require mediation or litigation.\n\n"
            "Operators must document efforts to accommodate and mitigate surface impacts.\n\n"
            "Failure to comply with the Surface Damage Act can result in penalties and increased liability.\n\n"
            "Balancing mineral development and surface rights is essential for sustainable resource extraction."
        ),
        key_factors=[
            "Existence of prior surface uses",
            "Mineral estate dominant but subject to accommodation",
            "Notice and negotiation requirements under Surface Damage Act",
            "Calculation and payment of damages",
            "Compliance with Texas Natural Resources Code Chapter 134",
            "Documentation of accommodation efforts",
            "Dispute resolution mechanisms"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 134 - Surface Damage Act",
            "Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Texas Supreme Court: Coastal Oil & Gas Corp. v. Garza Energy Trust, 268 S.W.3d 1 (Tex. 2008)",
            "Texas Property Code Chapter 5 - Easements",
            "Texas Supreme Court: Sun Oil Co. v. Whitaker, 424 S.W.2d 216 (Tex. 1967)"
        ],
        burden_holder="Operator/mineral owner",
        adversary_position=(
            "Surface owners may claim inadequate accommodation or insufficient damage compensation."
        ),
        counter_arguments=[
            "Demonstrate reasonable accommodation efforts",
            "Provide damage agreements and payment records",
            "Show compliance with statutory notice requirements",
            "Use expert testimony on surface use and damages",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Engage in early negotiation with surface owners, document accommodation measures, and comply fully with Surface Damage Act."
        ),
        entity_scope="Operators, mineral owners, surface owners, attorneys",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
    ),
    DoctrineBlock(
        topic="Probate Title Estate Administration Will Contests",
        keywords=[
            "probate title",
            "estate administration",
            "will contest",
            "intestate",
            "executor",
            "heirship",
            "probate court",
            "estate distribution"
        ],
        conclusion_template=(
            "Probate title is established through estate administration proceedings, with will contests resolved by probate courts "
            "to determine valid testamentary intent and rightful heirs."
        ),
        reasoning_framework=(
            "Probate title arises from court-supervised administration of a decedent's estate, either testate or intestate.\n\n"
            "The probate process includes validating wills, appointing executors or administrators, inventorying assets, and distributing property.\n\n"
            "Will contests challenge the validity of a will based on grounds such as undue influence, fraud, or lack of testamentary capacity.\n\n"
            "Probate courts evaluate evidence, hear testimony, and issue orders determining valid title and heirs.\n\n"
            "Intestate estates are distributed according to Texas Estates Code Chapter 201.\n\n"
            "Probate title is critical for marketability and transfer of property interests.\n\n"
            "Title examiners must review probate records, court orders, and heirship determinations.\n\n"
            "Disputes can delay estate administration and cloud title, requiring resolution through litigation or settlement.\n\n"
            "Proper legal representation and documentation facilitate smooth probate and clear title."
        ),
        key_factors=[
            "Existence and validity of will",
            "Probate court jurisdiction and orders",
            "Appointment of executor or administrator",
            "Resolution of will contests",
            "Heirship determination",
            "Inventory and valuation of estate assets",
            "Compliance with Texas Estates Code",
            "Documentation supporting probate title"
        ],
        primary_authority=[
            "Texas Estates Code Chapters 201 and 256",
            "Texas Probate Code",
            "In re Estate of Smith, 150 S.W.3d 436 (Tex. 2004)",
            "Texas Supreme Court: Estate of McMillin, 869 S.W.2d 860 (Tex. App. 1993)",
            "Texas Rules of Civil Procedure - Probate"
        ],
        burden_holder="Estate representative",
        adversary_position=(
            "Interested parties may contest will validity or heirship claims."
        ),
        counter_arguments=[
            "Provide valid probate court orders",
            "Demonstrate compliance with statutory requirements",
            "Present evidence supporting testamentary intent",
            "Use expert testimony in probate law",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Engage experienced probate counsel, maintain thorough documentation, and resolve disputes through probate court."
        ),
        entity_scope="Estate administrators, heirs, probate courts, attorneys",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Estate of Smith, 150 S.W.3d 436 (Tex. 2004)"
    ),
    DoctrineBlock(
        topic="Regulatory Filing RRC Permits P-5 W-1 Compliance",
        keywords=[
            "regulatory filing",
            "Railroad Commission",
            "RRC permits",
            "P-5 form",
            "W-1 form",
            "oil and gas operations",
            "compliance",
            "permit applications"
        ],
        conclusion_template=(
            "Compliance with Railroad Commission regulatory filings, including P-5 and W-1 permit forms, is mandatory for lawful oil and gas operations."
        ),
        reasoning_framework=(
            "The Texas Railroad Commission (RRC) regulates oil and gas operations through permit requirements and reporting.\n\n"
            "The P-5 form is used to apply for drilling permits, providing detailed information about the well location, operator, and proposed operations.\n\n"
            "The W-1 form is required for plugging and abandonment of wells, documenting compliance with environmental and safety standards.\n\n"
            "Operators must submit accurate and timely filings to maintain regulatory compliance and avoid penalties.\n\n"
            "RRC reviews permit applications for technical and environmental adequacy.\n\n"
            "Failure to comply with filing requirements can result in permit denial, fines, or operational shutdown.\n\n"
            "Title examiners and landmen must verify permit status when assessing leasehold viability.\n\n"
            "Coordination with RRC and legal counsel ensures adherence to regulatory frameworks.\n\n"
            "Electronic filing systems facilitate submission and tracking of permits."
        ),
        key_factors=[
            "Accurate completion of P-5 and W-1 forms",
            "Timely submission to RRC",
            "Compliance with technical and environmental standards",
            "RRC review and approval processes",
            "Recordkeeping and reporting obligations",
            "Impact on leasehold and operational status",
            "Coordination with regulatory authorities"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 91 - Oil and Gas Operations",
            "Texas Railroad Commission Rules 3.5 and 3.6",
            "Texas Administrative Code Title 16, Part 1",
            "Texas Railroad Commission Permit Application Forms",
            "Texas Supreme Court: Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
        ],
        burden_holder="Operator",
        adversary_position=(
            "Regulators may allege noncompliance or submission of inaccurate filings."
        ),
        counter_arguments=[
            "Provide copies of filed permits and correspondence",
            "Demonstrate compliance with RRC rules",
            "Show corrective actions taken if errors occurred",
            "Use expert testimony on regulatory compliance",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Maintain rigorous filing procedures, monitor permit status, and engage legal counsel for regulatory issues."
        ),
        entity_scope="Operators, Railroad Commission, attorneys, landmen",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
    ),
    DoctrineBlock(
        topic="Document Classification Deed Lease Assignment Release Mortgage",
        keywords=[
            "document classification",
            "deed",
            "lease",
            "assignment",
            "release",
            "mortgage",
            "recording",
            "title documents"
        ],
        conclusion_template=(
            "Accurate classification of title documents such as deeds, leases, assignments, releases, and mortgages is essential "
            "for proper title examination and recordation."
        ),
        reasoning_framework=(
            "Title examination requires identification and classification of various recorded documents affecting property interests.\n\n"
            "Deeds convey ownership interests and must be distinguished from leases, which grant possessory rights for a term.\n\n"
            "Assignments transfer existing leasehold or other interests.\n\n"
            "Releases remove liens or encumbrances and must be properly recorded to clear title.\n\n"
            "Mortgages create security interests and impose encumbrances on property.\n\n"
            "Proper classification enables accurate chain of title analysis and identification of burdens.\n\n"
            "Recording statutes require correct indexing by document type to provide constructive notice.\n\n"
            "Misclassification can lead to missed defects or improper title opinions.\n\n"
            "Title examiners use standardized terminology and document codes to ensure consistency.\n\n"
            "Coordination with county clerks and use of electronic databases facilitate classification."
        ),
        key_factors=[
            "Document type and legal effect",
            "Recording and indexing accuracy",
            "Chain of title implications",
            "Identification of encumbrances and releases",
            "Compliance with recording statutes",
            "Use of standardized classification codes",
            "Impact on title opinion and insurance"
        ],
        primary_authority=[
            "Texas Property Code Chapter 13 - Recording",
            "Texas Land Title Association Title Examination Standards",
            "Texas Business and Commerce Code § 9.203 - Perfection of Security Interests",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997",
            "Texas County Clerks Association Document Classification Guidelines"
        ],
        burden_holder="Title examiner",
        adversary_position=(
            "Opposing parties may claim misclassification leading to title defects or disputes."
        ),
        counter_arguments=[
            "Provide documented classification procedures",
            "Demonstrate use of standardized codes and training",
            "Show chain of title analysis supporting classification",
            "Reference statutory recording requirements",
            "Use expert testimony on title examination"
        ],
        resolution_strategy=(
            "Implement quality control in document classification and maintain updated training and procedures."
        ),
        entity_scope="Title examiners, county clerks, attorneys, landmen",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. National Union Fire Ins. Co., 1997"
    ),
    DoctrineBlock(
        topic="Permian Basin Delaware Basin Midland Basin Formations",
        keywords=[
            "Permian Basin",
            "Delaware Basin",
            "Midland Basin",
            "oil and gas formations",
            "geology",
            "reservoir",
            "production",
            "Texas geology"
        ],
        conclusion_template=(
            "The Permian Basin, including the Delaware and Midland Basins, comprises prolific oil and gas formations "
            "with distinct geological characteristics critical for exploration and development."
        ),
        reasoning_framework=(
            "The Permian Basin is a major sedimentary basin in West Texas and southeastern New Mexico, known for prolific hydrocarbon production.\n\n"
            "It consists of several sub-basins, including the Delaware Basin to the west and the Midland Basin to the east.\n\n"
            "Each basin contains multiple stratigraphic formations such as the Wolfcamp, Spraberry, Bone Spring, and Avalon Shale.\n\n"
            "Geological characteristics including porosity, permeability, and structural traps influence reservoir quality and production potential.\n\n"
            "Understanding formation properties guides drilling, completion, and stimulation strategies.\n\n"
            "The Permian Basin has experienced a resurgence due to horizontal drilling and hydraulic fracturing technologies.\n\n"
            "Operators must consider basin-specific regulatory requirements and land ownership patterns.\n\n"
            "Geological surveys, seismic data, and well logs support formation evaluation.\n\n"
            "Accurate formation identification is essential for title and lease analysis, as mineral rights may be severed by formation or depth."
        ),
        key_factors=[
            "Geological formation characteristics",
            "Reservoir quality and production data",
            "Stratigraphic and structural mapping",
            "Technological developments in drilling",
            "Regulatory environment",
            "Land and mineral ownership patterns",
            "Data sources including seismic and well logs"
        ],
        primary_authority=[
            "United States Geological Survey (USGS) Permian Basin Reports",
            "Texas Railroad Commission Production Data",
            "Bureau of Economic Geology, University of Texas at Austin",
            "Texas General Land Office Geological Surveys",
            "Texas A&M University Petroleum Engineering Research"
        ],
        burden_holder="Operators and geologists",
        adversary_position=(
            "Disputes over formation identification or reservoir boundaries affecting lease or royalty interests."
        ),
        counter_arguments=[
            "Provide geological and geophysical data",
            "Demonstrate industry-standard formation evaluation",
            "Use expert testimony in petroleum geology",
            "Reference authoritative geological surveys",
            "Show consistency with regulatory production data"
        ],
        resolution_strategy=(
            "Employ qualified geologists, maintain comprehensive data sets, and document formation evaluations."
        ),
        entity_scope="Operators, geologists, landmen, attorneys",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="USGS Permian Basin Reports"
    ),
    DoctrineBlock(
        topic="Horizontal Well Spacing Rule 37 Density Exceptions",
        keywords=[
            "horizontal well",
            "spacing",
            "Rule 37",
            "density exceptions",
            "Texas Railroad Commission",
            "well location",
            "drilling permits",
            "production units"
        ],
        conclusion_template=(
            "Rule 37 governs well spacing and density in Texas, allowing exceptions for horizontal wells "
            "subject to Railroad Commission approval to optimize reservoir drainage."
        ),
        reasoning_framework=(
            "Texas Railroad Commission Rule 37 regulates the spacing of wells to prevent waste and protect correlative rights.\n\n"
            "Standard spacing rules establish minimum distances between wells and unit sizes.\n\n"
            "Horizontal wells, which extend laterally through formations, require special consideration for spacing and density.\n\n"
            "Operators may apply for density exceptions to drill additional wells within standard units to maximize recovery.\n\n"
            "RRC evaluates applications based on reservoir characteristics, drainage patterns, and potential impact on correlative rights.\n\n"
            "Approval of density exceptions requires technical data, including reservoir engineering studies.\n\n"
            "Rule 37 exceptions impact leasehold interests, royalty calculations, and production reporting.\n\n"
            "Operators must maintain compliance with permit conditions and reporting requirements.\n\n"
            "Disputes may arise over spacing violations or unauthorized drilling."
        ),
        key_factors=[
            "Standard well spacing requirements",
            "Application and approval of density exceptions",
            "Reservoir engineering and drainage analysis",
            "Compliance with RRC permit conditions",
            "Impact on leasehold and royalty interests",
            "Reporting and production allocation",
            "Dispute resolution procedures"
        ],
        primary_authority=[
            "Texas Railroad Commission Rule 37 - Well Spacing",
            "Texas Natural Resources Code Chapter 102",
            "Texas Railroad Commission Permit Application Forms",
            "Texas Supreme Court: Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator seeking exception",
        adversary_position=(
            "Opponents may challenge exception applications or allege spacing violations."
        ),
        counter_arguments=[
            "Provide reservoir and engineering data supporting exceptions",
            "Demonstrate compliance with RRC rules and permit terms",
            "Show prior approvals and regulatory correspondence",
            "Use expert testimony on reservoir management",
            "Reference controlling case law and statutes"
        ],
        resolution_strategy=(
            "Submit thorough applications, maintain compliance, and engage in regulatory hearings as necessary."
        ),
        entity_scope="Operators, Railroad Commission, landmen, attorneys",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Railroad Commission v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
    ),
    DoctrineBlock(
        topic="Net Mineral Acre Calculation NRI Working Interest ORRI",
        keywords=[
            "net mineral acres",
            "NRI",
            "working interest",
            "ORRI",
            "royalty interest",
            "leasehold",
            "production allocation",
            "title analysis"
        ],
        conclusion_template=(
            "Net mineral acre calculations incorporate ownership percentages, including NRI, working interest, and overriding royalty interests, "
            "to determine production allocation and revenue distribution."
        ),
        reasoning_framework=(
            "Net mineral acres (NMA) represent the fractional mineral ownership interest multiplied by the acreage owned.\n\n"
            "Net revenue interest (NRI) reflects the owner's share of production revenue after deducting burdens such as royalties and overriding royalties.\n\n"
            "Working interest (WI) represents the lessee's share of costs and operations.\n\n"
            "Overriding royalty interests (ORRI) are non-operating interests carved out of the working interest.\n\n"
            "Accurate calculation of NMA, NRI, WI, and ORRI is essential for correct payment allocation and title analysis.\n\n"
            "Title examiners analyze conveyance instruments, leases, and assignments to determine ownership percentages.\n\n"
            "Errors in calculation can lead to payment disputes and title defects.\n\n"
            "Industry standards and software tools assist in complex interest calculations.\n\n"
            "Coordination with division order analysts and landmen ensures consistency."
        ),
        key_factors=[
            "Fractional mineral ownership percentages",
            "Lease royalty provisions",
            "Working interest and operating agreements",
            "Overriding royalty interest documentation",
            "Accurate acreage measurement",
            "Title and lease document analysis",
            "Production allocation formulas"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 91",
            "Texas Property Code Chapter 5",
            "Texas Land Title Association Division Order Guidelines",
            "Texas Supreme Court: Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)",
            "Industry Standard Division Order Software"
        ],
        burden_holder="Title examiner and operator",
        adversary_position=(
            "Disputes over ownership percentages or payment allocations."
        ),
        counter_arguments=[
            "Provide detailed title and lease analysis",
            "Demonstrate use of standard calculation methods",
            "Show supporting documentation for interests",
            "Use expert testimony on division orders",
            "Reference controlling case law"
        ],
        resolution_strategy=(
            "Maintain accurate records, verify calculations, and resolve disputes through negotiation or legal action."
        ),
        entity_scope="Operators, title examiners, landmen, royalty owners",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
    ),
    DoctrineBlock(
        topic="Curative Requirements Title Defect Remediation",
        keywords=[
            "curative",
            "title defect",
            "remediation",
            "affidavit",
            "quiet title",
            "reformation",
            "recording",
            "title insurance"
        ],
        conclusion_template=(
            "Curative requirements address title defects through affidavits, reformation, quiet title actions, and proper recording "
            "to restore marketable title."
        ),
        reasoning_framework=(
            "Title defects such as missing instruments, ambiguous conveyances, or clouded title require curative action to ensure marketability.\n\n"
            "Common curative methods include obtaining affidavits of heirship, re-executing or re-recording documents, and filing quiet title lawsuits.\n\n"
            "Affidavits provide sworn statements clarifying facts or relationships affecting title.\n\n"
            "Reformation corrects errors in recorded instruments through judicial orders.\n\n"
            "Quiet title actions resolve competing claims and establish clear ownership.\n\n"
            "Proper recording of curative documents provides constructive notice and updates the chain of title.\n\n"
            "Title insurers require satisfactory curative measures before issuing policies.\n\n"
            "Coordination among landmen, attorneys, and title companies is essential for effective curative work.\n\n"
            "Failure to cure defects can result in transaction delays, increased risk, or claim denials."
        ),
        key_factors=[
            "Identification of specific title defects",
            "Appropriate curative method selection",
            "Preparation and execution of affidavits or instruments",
            "Judicial proceedings for reformation or quiet title",
            "Recording and indexing of curative documents",
            "Title insurance requirements",
            "Coordination among stakeholders"
        ],
        primary_authority=[
            "Texas Property Code Chapter 13 - Recording",
            "Texas Estates Code Chapter 201 - Affidavit of Heirship",
            "Texas Rules of Civil Procedure - Quiet Title",
            "Texas Supreme Court: First American Title Ins. Co. v. National Union Fire Ins. Co., 1997",
            "Texas Land Title Association Curative Guidelines"
        ],
        burden_holder="Title examiner and grantor",
        adversary_position=(
            "Opposing parties may contest curative documents or claim unresolved defects."
        ),
        counter_arguments=[
            "Provide executed curative instruments to resolve title defects",
            "Challenge the necessity of curative action based on marketability standards",
            "Argue that the title defect does not affect insurable interest"
        ],
        resolution_strategy="Follow Texas Land Title Association curative guidelines and file necessary corrective instruments.",
        entity_scope="All parties in the chain of title",
        confidence=0.87,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Texas Property Code Chapter 13 - Curative"
    ),
]

# =============================================
# SUB-ENGINE ORCHESTRATION
# =============================================

class SubEngineStatus(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class CircuitBreakerState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class IssueCategory(Enum):
    TITLE_EXAMINATION = auto()
    LEASE_ANALYSIS = auto()
    MINERAL_RIGHTS_VERIFICATION = auto()
    DIVISION_ORDER_ANALYSIS = auto()
    CHAIN_OF_TITLE = auto()
    RIGHT_OF_WAY = auto()
    REGULATORY_FILING = auto()
    HEIRSHIP_DETERMINATION = auto()
    TITLE_OPINION_REVIEW = auto()
    DOCUMENT_CLASSIFICATION = auto()
    COUNTY_RECORDS_SEARCH = auto()
    GIS_INTEGRATION = auto()
    WATER_RIGHTS = auto()
    EASEMENT_ANALYSIS = auto()
    POOLING_UNIT_ANALYSIS = auto()
    TAX_ASSESSMENT = auto()
    SURFACE_RIGHTS = auto()
    TITLE_INSURANCE = auto()
    PROBATE_TITLE = auto()
    INDIAN_LAND_TITLE = auto()
    FEDERAL_STATE_LANDS = auto()
    ABSTRACT_PLANT_MANAGEMENT = auto()
    UNKNOWN = auto()

class RoutingMode(Enum):
    PARALLEL = auto()
    CASCADE = auto()
    SINGLE = auto()

class QueryRequest:
    def __init__(self, text: str, metadata: Dict[str, Any], mode: RoutingMode = RoutingMode.PARALLEL):
        self.text = text
        self.metadata = metadata
        self.mode = mode

class RoutingDecision:
    def __init__(self, engines: List['SubEngineConfig'], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, category: IssueCategory, priority: int = 1):
        self.engine_id = engine_id
        self.url = url
        self.category = category
        self.priority = priority

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus, latency: float):
        self.engine_id = engine_id
        self.response = response
        self.status = status
        self.latency = latency

class ConsensusResponse:
    def __init__(self, merged: Any, conflicts: List[Any]):
        self.merged = merged
        self.conflicts = conflicts

# --- SubEngine Registry ---

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "LM01": SubEngineConfig("LM01", "http://lm01-title-exam/api", IssueCategory.TITLE_EXAMINATION, priority=5),
    "LM02": SubEngineConfig("LM02", "http://lm02-lease-analysis/api", IssueCategory.LEASE_ANALYSIS, priority=4),
    "LM03": SubEngineConfig("LM03", "http://lm03-mineral-rights/api", IssueCategory.MINERAL_RIGHTS_VERIFICATION, priority=5),
    "LM04": SubEngineConfig("LM04", "http://lm04-division-order/api", IssueCategory.DIVISION_ORDER_ANALYSIS, priority=3),
    "LM05": SubEngineConfig("LM05", "http://lm05-chain-title/api", IssueCategory.CHAIN_OF_TITLE, priority=5),
    "LM06": SubEngineConfig("LM06", "http://lm06-row/api", IssueCategory.RIGHT_OF_WAY, priority=4),
    "LM07": SubEngineConfig("LM07", "http://lm07-regulatory/api", IssueCategory.REGULATORY_FILING, priority=3),
    "LM08": SubEngineConfig("LM08", "http://lm08-heirship/api", IssueCategory.HEIRSHIP_DETERMINATION, priority=4),
    "LM09": SubEngineConfig("LM09", "http://lm09-title-opinion/api", IssueCategory.TITLE_OPINION_REVIEW, priority=4),
    "LM10": SubEngineConfig("LM10", "http://lm10-doc-class/api", IssueCategory.DOCUMENT_CLASSIFICATION, priority=2),
    "LM11": SubEngineConfig("LM11", "http://lm11-county-records/api", IssueCategory.COUNTY_RECORDS_SEARCH, priority=3),
    "LM12": SubEngineConfig("LM12", "http://lm12-gis/api", IssueCategory.GIS_INTEGRATION, priority=2),
    "LM13": SubEngineConfig("LM13", "http://lm13-water-rights/api", IssueCategory.WATER_RIGHTS, priority=3),
    "LM14": SubEngineConfig("LM14", "http://lm14-easement/api", IssueCategory.EASEMENT_ANALYSIS, priority=3),
    "LM15": SubEngineConfig("LM15", "http://lm15-pooling/api", IssueCategory.POOLING_UNIT_ANALYSIS, priority=2),
    "LM16": SubEngineConfig("LM16", "http://lm16-tax/api", IssueCategory.TAX_ASSESSMENT, priority=2),
    "LM17": SubEngineConfig("LM17", "http://lm17-surface/api", IssueCategory.SURFACE_RIGHTS, priority=3),
    "LM18": SubEngineConfig("LM18", "http://lm18-title-insurance/api", IssueCategory.TITLE_INSURANCE, priority=4),
    "LM19": SubEngineConfig("LM19", "http://lm19-probate/api", IssueCategory.PROBATE_TITLE, priority=4),
    "LM20": SubEngineConfig("LM20", "http://lm20-indian/api", IssueCategory.INDIAN_LAND_TITLE, priority=5),
    "LM21": SubEngineConfig("LM21", "http://lm21-federal-state/api", IssueCategory.FEDERAL_STATE_LANDS, priority=4),
    "LM22": SubEngineConfig("LM22", "http://lm22-abstract-plant/api", IssueCategory.ABSTRACT_PLANT_MANAGEMENT, priority=2),
}

# --- Health Monitoring ---

class HealthCacheEntry:
    def __init__(self, status: SubEngineStatus, timestamp: float):
        self.status = status
        self.timestamp = timestamp

class SubEngineHealthMonitor:
    def __init__(self, ttl: float = 30.0):
        self.ttl = ttl
        self._health_cache: Dict[str, HealthCacheEntry] = {}
        self._lock = asyncio.Lock()
        self._engine_urls: Dict[str, str] = {eid: cfg.url for eid, cfg in SUB_ENGINE_REGISTRY.items()}
        self._circuit_breakers: Dict[str, 'CircuitBreaker'] = {}

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        async with self._lock:
            now = time.time()
            entry = self._health_cache.get(engine_id)
            if entry and now - entry.timestamp < self.ttl:
                return entry.status
        url = self._engine_urls.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(url, timeout=3)
        async with self._lock:
            self._health_cache[engine_id] = HealthCacheEntry(status, time.time())
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for engine_id in self._engine_urls:
            tasks.append(self.check_health(engine_id))
        statuses = await asyncio.gather(*tasks)
        for eid, status in zip(self._engine_urls.keys(), statuses):
            results[eid] = status
        return results

    async def get_healthy_engines(self) -> List[str]:
        health = await self.check_all_health()
        healthy = [eid for eid, status in health.items() if status == SubEngineStatus.HEALTHY]
        return healthy

    async def _ping_engine(self, url: str, timeout: float) -> SubEngineStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + "/health", timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "healthy":
                            return SubEngineStatus.HEALTHY
                        elif data.get("status") == "degraded":
                            return SubEngineStatus.DEGRADED
                        else:
                            return SubEngineStatus.UNHEALTHY
                    else:
                        return SubEngineStatus.UNHEALTHY
        except Exception:
            return SubEngineStatus.UNHEALTHY

    def set_circuit_breaker(self, engine_id: str, breaker: 'CircuitBreaker'):
        self._circuit_breakers[engine_id] = breaker

    def get_circuit_breaker(self, engine_id: str) -> Optional['CircuitBreaker']:
        return self._circuit_breakers.get(engine_id)

# --- Circuit Breaker ---

class CircuitBreaker:
    def __init__(self, engine_id: str, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.engine_id = engine_id
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self._lock = asyncio.Lock()

    async def record_failure(self):
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN

    async def record_success(self):
        async with self._lock:
            self.failure_count = 0
            self.state = CircuitBreakerState.CLOSED

    async def allow_request(self) -> bool:
        async with self._lock:
            now = time.time()
            if self.state == CircuitBreakerState.OPEN:
                if now - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                    return True
                return False
            return True

    async def on_request_result(self, success: bool):
        if success:
            await self.record_success()
        else:
            await self.record_failure()

    async def get_state(self) -> CircuitBreakerState:
        async with self._lock:
            return self.state

# --- Query Routing ---

CATEGORY_KEYWORDS: Dict[IssueCategory, List[str]] = {
    IssueCategory.TITLE_EXAMINATION: ["title examination", "ownership", "title report", "abstract", "title search"],
    IssueCategory.LEASE_ANALYSIS: ["lease", "royalty", "term", "expiration", "bonus", "rental"],
    IssueCategory.MINERAL_RIGHTS_VERIFICATION: ["mineral rights", "oil", "gas", "coal", "mineral estate", "reservation"],
    IssueCategory.DIVISION_ORDER_ANALYSIS: ["division order", "interest", "decimal", "payee", "distribution"],
    IssueCategory.CHAIN_OF_TITLE: ["chain of title", "conveyance", "transfer", "deed", "recording"],
    IssueCategory.RIGHT_OF_WAY: ["right of way", "ROW", "access", "easement", "road"],
    IssueCategory.REGULATORY_FILING: ["regulatory", "filing", "permit", "compliance", "application"],
    IssueCategory.HEIRSHIP_DETERMINATION: ["heirship", "succession", "probate", "descendants", "inheritance"],
    IssueCategory.TITLE_OPINION_REVIEW: ["title opinion", "attorney", "legal", "review", "defects"],
    IssueCategory.DOCUMENT_CLASSIFICATION: ["document", "classification", "categorize", "sort", "type"],
    IssueCategory.COUNTY_RECORDS_SEARCH: ["county records", "record search", "county clerk", "recording"],
    IssueCategory.GIS_INTEGRATION: ["GIS", "mapping", "coordinates", "spatial", "geographic"],
    IssueCategory.WATER_RIGHTS: ["water rights", "water", "riparian", "hydro", "aquifer"],
    IssueCategory.EASEMENT_ANALYSIS: ["easement", "burden", "servient", "dominant", "encumbrance"],
    IssueCategory.POOLING_UNIT_ANALYSIS: ["pooling", "unit", "unitization", "allocation", "tract"],
    IssueCategory.TAX_ASSESSMENT: ["tax", "assessment", "valuation", "property tax", "appraisal"],
    IssueCategory.SURFACE_RIGHTS: ["surface rights", "surface", "land", "access", "use"],
    IssueCategory.TITLE_INSURANCE: ["title insurance", "policy", "coverage", "insurer", "premium"],
    IssueCategory.PROBATE_TITLE: ["probate", "estate", "executor", "court", "inheritance"],
    IssueCategory.INDIAN_LAND_TITLE: ["indian land", "tribal", "reservation", "allotment", "native"],
    IssueCategory.FEDERAL_STATE_LANDS: ["federal land", "state land", "BLM", "public land", "government"],
    IssueCategory.ABSTRACT_PLANT_MANAGEMENT: ["abstract plant", "plant", "records", "management", "archive"],
}

class QueryRouter:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched = set()
        for category, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    matched.add(category)
        if not matched:
            return [IssueCategory.UNKNOWN]
        return list(matched)

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        selected = []
        for category in categories:
            for cfg in SUB_ENGINE_REGISTRY.values():
                if cfg.category == category:
                    selected.append(cfg)
        if mode == RoutingMode.SINGLE and selected:
            selected = [max(selected, key=lambda c: c.priority)]
        return selected

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: If query metadata specifies a preferred engine, use it
        preferred = query.metadata.get("preferred_engine")
        if preferred and preferred in SUB_ENGINE_REGISTRY:
            return [preferred]
        # Example: If query is urgent, prioritize high-priority engines
        if query.metadata.get("urgent"):
            return [eid for eid, cfg in SUB_ENGINE_REGISTRY.items() if cfg.priority >= 4]
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        score = 0.0
        text = query.text.lower()
        keywords = CATEGORY_KEYWORDS.get(engine.category, [])
        for kw in keywords:
            if kw in text:
                score += 1.0
        if engine.priority >= 4:
            score += 0.5
        if query.metadata.get("preferred_engine") == engine.engine_id:
            score += 2.0
        return score

    def _handle_engine_failure(self, engine_id: str, error: Exception) -> List[str]:
        # Fallback: Remove failed engine, use others in same category
        failed_cfg = SUB_ENGINE_REGISTRY.get(engine_id)
        if not failed_cfg:
            return []
        fallback = []
        for eid, cfg in SUB_ENGINE_REGISTRY.items():
            if cfg.category == failed_cfg.category and eid != engine_id:
                fallback.append(eid)
        return fallback

    async def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        rule_engines = self._apply_routing_rules(query)
        if rule_engines:
            engines = [SUB_ENGINE_REGISTRY[eid] for eid in rule_engines]
        else:
            engines = self._select_engines(categories, query.mode)
        # Filter unhealthy engines
        healthy_eids = await self.health_monitor.get_healthy_engines()
        engines = [cfg for cfg in engines if cfg.engine_id in healthy_eids]
        if not engines:
            # fallback: pick highest priority engine in category regardless of health
            engines = self._select_engines(categories, RoutingMode.SINGLE)
        return RoutingDecision(engines, categories, query.mode)

# --- SubEngine Orchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor
        self._response_cache: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._breaker_map: Dict[str, CircuitBreaker] = {}

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for cfg in engines:
            resp = await self._call_sub_engine(cfg, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Any:
        tasks = []
        for cfg in engines:
            tasks.append(self._call_sub_engine(cfg, query))
        responses = await asyncio.gather(*tasks)
        merged = self._merge_responses(responses)
        return merged

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Any:
        for cfg in engines:
            resp = await self._call_sub_engine(cfg, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.response:
                return resp.response
        return None

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        breaker = self._breaker_map.get(engine_config.engine_id)
        if not breaker:
            breaker = CircuitBreaker(engine_config.engine_id)
            self._breaker_map[engine_config.engine_id] = breaker
        allowed = await breaker.allow_request()
        if not allowed:
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, 0.0)
        try:
            start = time.time()
            async with aiohttp.ClientSession() as session:
                payload = {
                    "query": query.text,
                    "metadata": query.metadata
                }
                async with session.post(engine_config.url + "/query", json=payload, timeout=10) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        data = await resp.json()
                        await breaker.on_request_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY, latency)
                    else:
                        await breaker.on_request_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, latency)
        except Exception as e:
            await breaker.on_request_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, 0.0)

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Any:
        merged = {}
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response:
                merged[resp.engine_id] = resp.response
        return merged

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> ConsensusResponse:
        # Simple consensus: if all responses agree, return merged; else, list conflicts
        merged = {}
        conflicts = []
        values = []
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response:
                values.append(resp.response)
        if not values:
            return ConsensusResponse({}, [])
        # Assume responses are dicts; compare keys
        keys = set()
        for v in values:
            keys.update(v.keys())
        for k in keys:
            vals = [v.get(k) for v in values if k in v]
            if len(set(vals)) == 1:
                merged[k] = vals[0]
            else:
                conflicts.append({k: vals})
        return ConsensusResponse(merged, conflicts)

# --- Example Usage (for integration) ---

async def orchestrate_query(query: QueryRequest):
    health_monitor = SubEngineHealthMonitor()
    router = QueryRouter(health_monitor)
    orchestrator = SubEngineOrchestrator(health_monitor)
    routing_decision = await router.route_query(query)
    if routing_decision.mode == RoutingMode.PARALLEL:
        response = await orchestrator.dispatch_parallel(query, routing_decision.engines)
    elif routing_decision.mode == RoutingMode.CASCADE:
        response = await orchestrator.dispatch_cascade(query, routing_decision.engines)
    else:
        response = await orchestrator.dispatch_query(query, routing_decision.engines)
    return response

# --- For Testing ---

async def test_engine():
    query = QueryRequest(
        text="What is the chain of title for mineral rights in this tract?",
        metadata={"urgent": True},
        mode=RoutingMode.PARALLEL
    )
    resp = await orchestrate_query(query)
    print(resp)

# --- Main Loop ---

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_engine())

class AuthorityLevel(enum.Enum):
    CONSTITUTIONAL = 6
    STATUTORY = 5
    REGULATORY = 4
    CASE_LAW = 3
    TREATISE = 2
    PRACTICE = 1

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 50,
    AuthorityLevel.TREATISE: 30,
    AuthorityLevel.PRACTICE: 10,
}

def resolve_authority_conflict(sources: List[AuthorityLevel]) -> AuthorityLevel:
    """
    Given a list of authority sources, return the dominant authority based on weights.
    If multiple with same weight, return the highest enum (most authoritative).
    """
    if not sources:
        raise ValueError("No authority sources provided")
    max_weight = -1
    dominant_levels = []
    for src in sources:
        w = authority_weights.get(src, 0)
        if w > max_weight:
            max_weight = w
            dominant_levels = [src]
        elif w == max_weight:
            dominant_levels.append(src)
    # Return the highest enum in dominant_levels (most authoritative)
    return max(dominant_levels, key=lambda x: x.value)

# ----------------------------------------
# EPISTEMIC GUARDRAILS
# ----------------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "indisputably",
    "unequivocally", "categorically", "incontestably", "irrefutably", "infallibly",
    "decisively", "conclusively", "plainly", "self-evidently", "beyond dispute",
    "without reservation", "without exception", "inarguably", "incontrovertible",
    "beyond any doubt", "undoubtedly", "beyond all doubt", "without hesitation",
    "without reservation", "without question", "without fail", "without exception"
]

EPISTEMIC_CAVEAT = (
    "\n\n[Disclosure: The analysis avoids absolute assertions and acknowledges "
    "potential uncertainties and alternative interpretations.]"
)

class ConfidenceLevel(enum.Enum):
    DEFENSIBLE = 1
    AGGRESSIVE = 2
    DISCLOSURE = 3
    HIGH_RISK = 4

def apply_epistemic_guardrails(text: str) -> Tuple[str, ConfidenceLevel]:
    """
    Remove banned phrases from text and append disclosure caveat.
    Return cleaned text and confidence stratification.
    """
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BANNED_PHRASES)) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub("", text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()
    cleaned_text += EPISTEMIC_CAVEAT

    # Confidence stratification logic (simple heuristic)
    lowered = text.lower()
    banned_count = sum(lowered.count(bp) for bp in BANNED_PHRASES)
    if banned_count == 0:
        confidence = ConfidenceLevel.DEFENSIBLE
    elif banned_count <= 2:
        confidence = ConfidenceLevel.DISCLOSURE
    elif banned_count <= 5:
        confidence = ConfidenceLevel.AGGRESSIVE
    else:
        confidence = ConfidenceLevel.HIGH_RISK

    return cleaned_text, confidence

# ----------------------------------------
# FACT FRAGILITY SCORING
# ----------------------------------------

def score_fact_fragility(fact: str) -> Dict[str, float]:
    """
    Score fact fragility on three axes:
    - verifiability: 0 (not verifiable) to 1 (highly verifiable)
    - recharacterization_risk: 0 (low risk) to 1 (high risk)
    - testimony_dependence: 0 (no dependence) to 1 (high dependence)
    This is a heuristic scoring based on keywords and patterns.
    """
    fact_lower = fact.lower()
    verifiability = 0.5
    recharacterization_risk = 0.5
    testimony_dependence = 0.0

    # Verifiability heuristics
    if any(word in fact_lower for word in ["documented", "recorded", "written", "signed", "official", "certified"]):
        verifiability = min(1.0, verifiability + 0.4)
    if any(word in fact_lower for word in ["alleged", "claimed", "reported", "asserted"]):
        verifiability = max(0.0, verifiability - 0.3)

    # Recharacterization risk heuristics
    if any(word in fact_lower for word in ["ambiguous", "unclear", "disputed", "controversial", "contradicted"]):
        recharacterization_risk = min(1.0, recharacterization_risk + 0.4)
    if any(word in fact_lower for word in ["explicit", "clear", "unequivocal"]):
        recharacterization_risk = max(0.0, recharacterization_risk - 0.3)

    # Testimony dependence heuristics
    if any(word in fact_lower for word in ["witness", "testimony", "oral", "statement", "deposition"]):
        testimony_dependence = min(1.0, testimony_dependence + 0.7)
    if any(word in fact_lower for word in ["document", "contract", "email", "record"]):
        testimony_dependence = max(0.0, testimony_dependence - 0.5)

    # Clamp values
    verifiability = max(0.0, min(1.0, verifiability))
    recharacterization_risk = max(0.0, min(1.0, recharacterization_risk))
    testimony_dependence = max(0.0, min(1.0, testimony_dependence))

    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence,
    }

# ----------------------------------------
# SEMANTIC NORMALIZATION
# ----------------------------------------

DOMAIN_TERM_MAPPINGS = {
    # 50+ domain term mappings for Landman domain
    "mineral rights": "mineral_interest",
    "surface rights": "surface_interest",
    "royalty interest": "royalty_interest",
    "lease agreement": "lease",
    "division order": "division_order",
    "title opinion": "title_opinion",
    "chain of title": "title_chain",
    "executive rights": "executive_rights",
    "working interest": "working_interest",
    "net revenue interest": "net_revenue_interest",
    "overriding royalty interest": "overriding_royalty_interest",
    "joint operating agreement": "JOA",
    "production payment": "production_payment",
    "shut-in royalty": "shut_in_royalty",
    "delay rental": "delay_rental",
    "force majeure": "force_majeure",
    "pooling agreement": "pooling_agreement",
    "unitization agreement": "unitization_agreement",
    "title curative": "title_curative",
    "surface use agreement": "surface_use_agreement",
    "right of way": "right_of_way",
    "division order analyst": "DOA",
    "landman": "landman",
    "assignment": "assignment",
    "conveyance": "conveyance",
    "title defect": "title_defect",
    "title abstract": "title_abstract",
    "title examination": "title_examination",
    "title search": "title_search",
    "curative instrument": "curative_instrument",
    "leasehold estate": "leasehold_estate",
    "executory interest": "executory_interest",
    "reversionary interest": "reversionary_interest",
    "escheat": "escheat",
    "adverse possession": "adverse_possession",
    "surface damage": "surface_damage",
    "drilling rights": "drilling_rights",
    "exploration rights": "exploration_rights",
    "production sharing": "production_sharing",
    "royalty clause": "royalty_clause",
    "title insurance": "title_insurance",
    "title abstractor": "title_abstractor",
    "title curative work": "title_curative_work",
    "land record": "land_record",
    "chain of custody": "chain_of_custody",
    "legal description": "legal_description",
    "metes and bounds": "metes_and_bounds",
    "surface estate": "surface_estate",
    "mineral estate": "mineral_estate",
    "fee simple": "fee_simple",
    "life estate": "life_estate",
    "easement": "easement",
    "right of entry": "right_of_entry",
}

def normalize_query(text: str) -> str:
    """
    Normalize query text by replacing domain terms with standardized terms.
    """
    lowered = text.lower()
    for phrase, standard in DOMAIN_TERM_MAPPINGS.items():
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        lowered = pattern.sub(standard, lowered)
    return lowered

# ----------------------------------------
# DEEP ANALYSIS
# ----------------------------------------

def multi_doctrine_decomposition(query: str) -> List[str]:
    """
    Decompose query into sub-issues based on doctrine keywords and punctuation.
    Returns list of sub-issues.
    """
    # Split on semicolons, commas, "and", "or" conjunctions heuristically
    separators = re.compile(r';|,|\band\b|\bor\b', re.IGNORECASE)
    parts = separators.split(query)
    sub_issues = [part.strip() for part in parts if part.strip()]
    return sub_issues

def build_interaction_dag(issues: List[str]) -> nx.DiGraph:
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume issues mentioning others create edges.
    """
    dag = nx.DiGraph()
    for issue in issues:
        dag.add_node(issue)
    # Heuristic: if issue A mentions keywords from issue B, add edge A->B
    for i, issue_a in enumerate(issues):
        for j, issue_b in enumerate(issues):
            if i == j:
                continue
            # Check if issue_a contains keywords from issue_b (simple word overlap)
            words_b = set(issue_b.lower().split())
            words_a = set(issue_a.lower().split())
            if words_b.intersection(words_a):
                dag.add_edge(issue_a, issue_b)
    # Remove cycles if any (keep DAG)
    try:
        cycles = list(nx.find_cycle(dag))
        for edge in cycles:
            dag.remove_edge(*edge)
    except nx.NetworkXNoCycle:
        pass
    return dag

def eight_step_resolution(query: str, doctrines: List[str], sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform a full eight-step resolution analysis.
    Steps (example):
    1. Identify issues
    2. State relevant doctrines
    3. Analyze facts
    4. Apply doctrines to facts
    5. Consider counterarguments
    6. Resolve conflicts
    7. Draw conclusions
    8. Provide recommendations
    """
    analysis = {}
    analysis['query'] = query
    analysis['issues'] = doctrines
    analysis['facts_analysis'] = {}
    analysis['doctrine_application'] = {}
    analysis['counterarguments'] = {}
    analysis['conflict_resolution'] = {}
    analysis['conclusions'] = {}
    analysis['recommendations'] = {}

    # Step 3: Analyze facts (stub)
    for issue in doctrines:
        analysis['facts_analysis'][issue] = f"Analyzed facts for issue: {issue}"

    # Step 4: Apply doctrines to facts (stub)
    for issue in doctrines:
        analysis['doctrine_application'][issue] = f"Applied doctrine to facts for issue: {issue}"

    # Step 5: Consider counterarguments (stub)
    for issue in doctrines:
        analysis['counterarguments'][issue] = f"Considered counterarguments for issue: {issue}"

    # Step 6: Resolve conflicts (stub)
    for issue in doctrines:
        analysis['conflict_resolution'][issue] = f"Resolved conflicts for issue: {issue}"

    # Step 7: Draw conclusions (stub)
    for issue in doctrines:
        analysis['conclusions'][issue] = f"Conclusion for issue: {issue}"

    # Step 8: Provide recommendations (stub)
    for issue in doctrines:
        analysis['recommendations'][issue] = f"Recommendations for issue: {issue}"

    # Merge sub-engine results
    analysis['sub_engine_results'] = sub_engine_results

    return analysis

def zoned_analysis(conclusion: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Tag conclusion elements into zones: PLANNING, REPORTING, AUDIT
    """
    zones = {
        "PLANNING": {},
        "REPORTING": {},
        "AUDIT": {},
    }
    for issue, text in conclusion.items():
        lowered = text.lower()
        if any(k in lowered for k in ["recommendation", "plan", "strategy", "next steps"]):
            zones["PLANNING"][issue] = text
        elif any(k in lowered for k in ["conclusion", "finding", "result", "outcome"]):
            zones["REPORTING"][issue] = text
        else:
            zones["AUDIT"][issue] = text
    return zones

# ----------------------------------------
# THREE-LAYER RESPONSE SYSTEM
# ----------------------------------------

class DoctrineCache:
    """
    Simple in-memory cache for doctrine analysis keyed by keywords.
    """
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def lookup(self, keywords: Set[str]) -> Optional[str]:
        """
        Lookup cache by keywords intersection.
        Returns cached analysis if found.
        """
        with self.lock:
            for key in self.cache:
                if keywords.intersection(key):
                    return self.cache[key]
        return None

    def store(self, keywords: Set[str], analysis: str):
        with self.lock:
            self.cache[frozenset(keywords)] = analysis

doctrine_cache = DoctrineCache()

def extract_keywords(text: str) -> Set[str]:
    """
    Extract keywords from text for caching and matching.
    Simple heuristic: words longer than 4 chars, excluding stopwords.
    """
    stopwords = {"the", "and", "with", "from", "that", "this", "which", "when", "where", "what", "how", "why", "for", "are", "was", "were", "has", "have", "had", "but", "not", "all", "any"}
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = set(w for w in words if len(w) > 4 and w not in stopwords)
    return keywords

def layer1_doctrine_cache_lookup(query: str) -> Optional[str]:
    """
    Layer 1: Doctrine cache lookup (0-200ms)
    """
    keywords = extract_keywords(query)
    cached = doctrine_cache.lookup(keywords)
    return cached

def layer2_semantic_search_and_routing(query: str) -> Dict[str, Any]:
    """
    Layer 2: Semantic search + sub-engine routing
    Dispatch to relevant sub-engines based on keywords.
    Stub implementation returns dummy sub-engine results.
    """
    keywords = extract_keywords(query)
    sub_engines = {
        "title_engine": lambda q: f"title_engine analysis of '{q}'",
        "lease_engine": lambda q: f"lease_engine analysis of '{q}'",
        "royalty_engine": lambda q: f"royalty_engine analysis of '{q}'",
        "compliance_engine": lambda q: f"compliance_engine analysis of '{q}'",
    }
    results = {}
    for name, func in sub_engines.items():
        # Simple routing: if any keyword matches engine name keywords
        engine_keywords = set(name.split('_'))
        if keywords.intersection(engine_keywords):
            results[name] = func(query)
    # If no engine matched, run all as fallback
    if not results:
        for name, func in sub_engines.items():
            results[name] = func(query)
    return results

def layer3_deep_multi_engine_analysis(query: str, sub_engine_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Layer 3: Deep multi-engine analysis
    Parallel dispatch, merge, resolve conflicts
    """
    doctrines = multi_doctrine_decomposition(query)
    dag = build_interaction_dag(doctrines)

    # Parallel analysis of doctrines (stub)
    def analyze_doctrine(doctrine):
        # Simulate complex analysis
        return f"Deep analysis of doctrine: {doctrine}"

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(analyze_doctrine, d): d for d in doctrines}
        for future in as_completed(futures):
            doctrine = futures[future]
            try:
                results[doctrine] = future.result()
            except Exception as e:
                results[doctrine] = f"Error analyzing doctrine: {e}"

    # Conflict resolution among doctrines (stub)
    resolved = {}
    for doctrine, analysis in results.items():
        resolved[doctrine] = analysis + " [conflicts resolved]"

    # Full eight step resolution
    full_analysis = eight_step_resolution(query, doctrines, sub_engine_results)

    # Store in doctrine cache for future
    keywords = extract_keywords(query)
    doctrine_cache.store(keywords, str(full_analysis))

    return full_analysis

def three_layer_response(query: str) -> Dict[str, Any]:
    """
    The three-layer response system:
    1. Doctrine cache lookup
    2. Semantic search + sub-engine routing
    3. Deep multi-engine analysis
    """
    # Layer 1
    cached = layer1_doctrine_cache_lookup(query)
    if cached:
        return {"layer": 1, "result": cached}

    # Layer 2
    sub_engine_results = layer2_semantic_search_and_routing(query)

    # Layer 3
    deep_analysis = layer3_deep_multi_engine_analysis(query, sub_engine_results)

    return {"layer": 3, "result": deep_analysis}

# ----------------------------------------
# END OF PART 4
# ----------------------------------------

@dataclass
class QueryTelemetry:
    query_id: str
    timestamp: float
    latency_ms: float
    cache_hit: bool
    engines_invoked: List[str]
    mode: str
    confidence: float
    error: Optional[str] = None

class TelemetryCollector:
    def __init__(self):
        self._lock = threading.Lock()
        self._queries: List[QueryTelemetry] = []
        self._errors: List[QueryTelemetry] = []
        self._engine_stats: Dict[str, List[float]] = defaultdict(list)
        self._doctrine_hits: Counter = Counter()
        self._doctrine_total: Counter = Counter()
        self._query_times: deque = deque()
        self._sub_engine_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'latencies': [],
            'errors': 0,
            'invocations': 0,
            'availability': [],
        })

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            self._query_times.append((telemetry.timestamp, telemetry.query_id))
            for engine in telemetry.engines_invoked:
                self._engine_stats[engine].append(telemetry.latency_ms)
                self._sub_engine_stats[engine]['latencies'].append(telemetry.latency_ms)
                self._sub_engine_stats[engine]['invocations'] += 1
                self._sub_engine_stats[engine]['availability'].append(True)
            if telemetry.cache_hit:
                self._doctrine_hits[telemetry.mode] += 1
            self._doctrine_total[telemetry.mode] += 1

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)
            for engine in telemetry.engines_invoked:
                self._sub_engine_stats[engine]['errors'] += 1
                self._sub_engine_stats[engine]['availability'].append(False)

    def get_latency_stats(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            stats = {}
            for engine, latencies in self._engine_stats.items():
                if not latencies:
                    continue
                stats[engine] = {
                    'avg': mean(latencies),
                    'p50': median(latencies),
                    'p95': quantiles(latencies, n=100)[94],
                    'p99': quantiles(latencies, n=100)[98],
                    'min': min(latencies),
                    'max': max(latencies),
                }
            return stats

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for doctrine in self._doctrine_total:
                total = self._doctrine_total[doctrine]
                hits = self._doctrine_hits[doctrine]
                rates[doctrine] = hits / total if total > 0 else 0.0
            return rates

    def queries_last_hour(self) -> int:
        cutoff = time.time() - 3600
        with self._lock:
            while self._query_times and self._query_times[0][0] < cutoff:
                self._query_times.popleft()
            return len(self._query_times)

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine, data in self._sub_engine_stats.items():
                latencies = data['latencies']
                errors = data['errors']
                invocations = data['invocations']
                availability = data['availability']
                stats[engine] = {
                    'avg_latency': mean(latencies) if latencies else 0.0,
                    'error_rate': errors / invocations if invocations > 0 else 0.0,
                    'availability': sum(availability) / len(availability) if availability else 0.0,
                    'invocations': invocations,
                }
            return stats

# DRIFT WATCHER

class DriftWatcher:
    def __init__(self):
        self._lock = threading.Lock()
        self._baseline_confidence: Dict[str, float] = {}
        self._history: Dict[str, List[Tuple[float, float]]] = defaultdict(list)  # doctrine -> [(timestamp, confidence)]
        self._alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            self._baseline_confidence[doctrine] = confidence

    def detect_drift(self, doctrine: str, confidence: float):
        timestamp = time.time()
        with self._lock:
            self._history[doctrine].append((timestamp, confidence))
            baseline = self._baseline_confidence.get(doctrine)
            if baseline is not None:
                drift = confidence - baseline
                percent_drift = (drift / baseline) * 100 if baseline != 0 else 0
                if abs(percent_drift) > 10.0:
                    alert = {
                        'doctrine': doctrine,
                        'timestamp': timestamp,
                        'baseline': baseline,
                        'current': confidence,
                        'percent_drift': percent_drift,
                        'alert': 'Significant drift detected'
                    }
                    self._alerts.append(alert)

    def get_drift_report(self) -> Dict[str, Any]:
        with self._lock:
            report = {}
            for doctrine, history in self._history.items():
                if not history:
                    continue
                confidences = [c for _, c in history]
                baseline = self._baseline_confidence.get(doctrine, 0.0)
                avg_conf = mean(confidences)
                max_drift = max(abs(c - baseline) for c in confidences)
                report[doctrine] = {
                    'baseline': baseline,
                    'avg_confidence': avg_conf,
                    'max_drift': max_drift,
                    'history': history[-20:],  # last 20 points
                }
            return {
                'report': report,
                'alerts': self._alerts[-10:]  # last 10 alerts
            }

# COVERAGE MAP

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._triggered: Counter = Counter()
        self._missed_queries: List[Dict[str, Any]] = []
        self._epistemic_gaps: List[Dict[str, Any]] = []
        self._sub_engine_coverage: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'triggered': 0,
            'missed': 0,
        })

    def record_triggered(self, doctrine: str, sub_engine: Optional[str] = None):
        with self._lock:
            self._triggered[doctrine] += 1
            if sub_engine:
                self._sub_engine_coverage[sub_engine]['triggered'] += 1

    def record_missed(self, query: Dict[str, Any], sub_engine: Optional[str] = None):
        with self._lock:
            self._missed_queries.append(query)
            if sub_engine:
                self._sub_engine_coverage[sub_engine]['missed'] += 1
            # Epistemic gap: no doctrine matched
            if not query.get('matched_doctrines'):
                self._epistemic_gaps.append(query)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total_triggered = sum(self._triggered.values())
            total_missed = len(self._missed_queries)
            gap_count = len(self._epistemic_gaps)
            per_doctrine = dict(self._triggered)
            per_sub_engine = dict(self._sub_engine_coverage)
            return {
                'total_triggered': total_triggered,
                'total_missed': total_missed,
                'epistemic_gaps': gap_count,
                'per_doctrine': per_doctrine,
                'per_sub_engine': per_sub_engine,
                'last_10_gaps': self._epistemic_gaps[-10:]
            }

# DETERMINISM HASH

def compute_determinism_hash(query: Dict[str, Any], response: Dict[str, Any]) -> str:
    # Canonicalize query/response for reproducibility
    def canonical(obj):
        if isinstance(obj, dict):
            return {k: canonical(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            return [canonical(x) for x in obj]
        else:
            return obj
    canonical_query = canonical(query)
    canonical_response = canonical(response)
    blob = json.dumps({'query': canonical_query, 'response': canonical_response}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()

# AUDIT TRAIL

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self._lock = threading.Lock()
        self._open_files: Dict[str, Any] = {}
        os.makedirs(audit_dir, exist_ok=True)

    def _get_file_for_date(self, dt: datetime.date) -> str:
        return os.path.join(self.audit_dir, f'audit_{dt.isoformat()}.jsonl')

    def write(self, telemetry: QueryTelemetry, engine_id: str):
        dt = datetime.date.fromtimestamp(telemetry.timestamp)
        filename = self._get_file_for_date(dt)
        record = {
            'query_id': telemetry.query_id,
            'timestamp': telemetry.timestamp,
            'engine_id': engine_id,
            'engines_invoked': telemetry.engines_invoked,
            'mode': telemetry.mode,
            'confidence': telemetry.confidence,
            'latency_ms': telemetry.latency_ms,
            'cache_hit': telemetry.cache_hit,
            'error': telemetry.error,
        }
        with self._lock:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record) + '\n')

    def forensic_replay(self, date: datetime.date, filter_engine_id: Optional[str] = None) -> List[Dict[str, Any]]:
        filename = self._get_file_for_date(date)
        records = []
        if not os.path.exists(filename):
            return records
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                rec = json.loads(line)
                if filter_engine_id and rec['engine_id'] != filter_engine_id:
                    continue
                records.append(rec)
        return records

# PERFORMANCE PROFILER

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.Lock()
        self._sub_engine_metrics: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'latencies': [],
            'errors': 0,
            'invocations': 0,
            'availability': [],
            'last_sla_check': None,
            'sla_breaches': [],
        })
        self._sla_thresholds: Dict[str, Dict[str, float]] = {}  # engine -> {'latency': ms, 'error_rate': float, 'availability': float}

    def set_sla(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        with self._lock:
            self._sla_thresholds[engine] = {
                'latency': latency_ms,
                'error_rate': error_rate,
                'availability': availability,
            }

    def record_invocation(self, engine: str, latency_ms: float, error: bool):
        with self._lock:
            self._sub_engine_metrics[engine]['latencies'].append(latency_ms)
            self._sub_engine_metrics[engine]['invocations'] += 1
            self._sub_engine_metrics[engine]['availability'].append(not error)
            if error:
                self._sub_engine_metrics[engine]['errors'] += 1

    def check_sla(self, engine: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            metrics = self._sub_engine_metrics[engine]
            thresholds = self._sla_thresholds.get(engine)
            if not thresholds or metrics['invocations'] == 0:
                return None
            avg_latency = mean(metrics['latencies']) if metrics['latencies'] else 0.0
            error_rate = metrics['errors'] / metrics['invocations']
            availability = sum(metrics['availability']) / len(metrics['availability']) if metrics['availability'] else 0.0
            breach = {}
            if avg_latency > thresholds['latency']:
                breach['latency'] = avg_latency
            if error_rate > thresholds['error_rate']:
                breach['error_rate'] = error_rate
            if availability < thresholds['availability']:
                breach['availability'] = availability
            if breach:
                metrics['sla_breaches'].append({
                    'timestamp': time.time(),
                    'breach': breach,
                })
                return breach
            return None

    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            out = {}
            for engine, metrics in self._sub_engine_metrics.items():
                latencies = metrics['latencies']
                errors = metrics['errors']
                invocations = metrics['invocations']
                availability = metrics['availability']
                out[engine] = {
                    'avg_latency': mean(latencies) if latencies else 0.0,
                    'error_rate': errors / invocations if invocations > 0 else 0.0,
                    'availability': sum(availability) / len(availability) if availability else 0.0,
                    'invocations': invocations,
                    'sla_breaches': metrics['sla_breaches'][-5:],
                }
            return out

# ===========================
# Integration Example (for orchestrator backbone)
# ===========================

class LandmanDomainOrchestratorBackbone:
    def __init__(self, audit_dir: str):
        self.telemetry_collector = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_tracker = CoverageTracker()
        self.audit_writer = AuditTrailWriter(audit_dir)
        self.performance_profiler = PerformanceProfiler()

    def process_query(self, query: Dict[str, Any], response: Dict[str, Any], engine_id: str, engines_invoked: List[str], mode: str, confidence: float, latency_ms: float, cache_hit: bool, error: Optional[str] = None):
        timestamp = time.time()
        query_id = query.get('query_id', f'q_{int(timestamp*1000)}')
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry_collector.record_query(telemetry)
        if error:
            self.telemetry_collector.record_error(telemetry)
        self.audit_writer.write(telemetry, engine_id)
        self.drift_watcher.detect_drift(mode, confidence)
        matched_doctrines = query.get('matched_doctrines', [])
        if matched_doctrines:
            for doctrine in matched_doctrines:
                self.coverage_tracker.record_triggered(doctrine, engine_id)
        else:
            self.coverage_tracker.record_missed({'query_id': query_id, 'query': query, 'matched_doctrines': matched_doctrines}, engine_id)
        for engine in engines_invoked:
            self.performance_profiler.record_invocation(engine, latency_ms, error is not None)

    def get_telemetry_stats(self):
        return self.telemetry_collector.get_latency_stats()

    def get_doctrine_hit_rates(self):
        return self.telemetry_collector.get_doctrine_hit_rate()

    def get_drift_report(self):
        return self.drift_watcher.get_drift_report()

    def get_coverage_report(self):
        return self.coverage_tracker.get_coverage_report()

    def get_performance_metrics(self):
        return self.performance_profiler.get_metrics()

    def verify_determinism(self, query: Dict[str, Any], response: Dict[str, Any]) -> str:
        return compute_determinism_hash(query, response)

    def forensic_replay(self, date: datetime.date, engine_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.audit_writer.forensic_replay(date, engine_id)

    def set_engine_sla(self, engine: str, latency_ms: float, error_rate: float, availability: float):
        self.performance_profiler.set_sla(engine, latency_ms, error_rate, availability)

    def check_engine_sla(self, engine: str) -> Optional[Dict[str, Any]]:
        return self.performance_profiler.check_sla(engine)

# ===========================
# END PART 5
# ===========================

logger = logging.getLogger("lmie_orchestrator")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Constants
ENGINE_ID = "LMIE"
ENGINE_PORT = 8420
SUB_ENGINES = {
    "LM01": "Title Examination",
    "LM02": "Lease Analysis",
    "LM03": "Mineral Rights Verification",
    "LM04": "Division Order Analysis",
    "LM05": "Chain of Title",
    "LM06": "Right of Way",
    "LM07": "Regulatory Filing",
    "LM08": "Heirship Determination",
    "LM09": "Title Opinion Review",
    "LM10": "Document Classification",
    "LM11": "County Records Search",
    "LM12": "GIS Integration",
    "LM13": "Water Rights",
    "LM14": "Easement Analysis",
    "LM15": "Pooling Unit Analysis",
    "LM16": "Tax Assessment",
    "LM17": "Surface Rights",
    "LM18": "Title Insurance",
    "LM19": "Probate Title",
    "LM20": "Indian Land Title",
    "LM21": "Federal State Lands",
    "LM22": "Abstract Plant Management"
}

# Globals for metrics and cache
doctrine_cache: Dict[str, Dict[str, Any]] = {}
search_index: Dict[str, List[str]] = {}
telemetry_data: Dict[str, Any] = {
    "latency_ms": [],
    "cache_hits": 0,
    "cache_misses": 0,
    "queries_processed": 0,
    "sub_engine_stats": {k: {"calls": 0, "failures": 0, "avg_latency_ms": 0.0} for k in SUB_ENGINES.keys()}
}
routing_rules: Dict[str, List[str]] = {}  # domain classification -> list of sub-engines
circuit_breakers: Dict[str, Dict[str, Any]] = {}  # sub-engine -> breaker state
health_status: Dict[str, Dict[str, Any]] = {}  # self + sub-engines health info
epistemic_gaps: List[str] = []
drift_report: Dict[str, Any] = {}

# Initialize routing rules (example)
def init_routing_rules():
    # For simplicity, map domain classifications to sub-engines
    routing_rules.update({
        "title": ["LM01", "LM05", "LM09", "LM18"],
        "lease": ["LM02", "LM14", "LM15"],
        "mineral": ["LM03", "LM13", "LM20"],
        "regulatory": ["LM07", "LM21"],
        "heirship": ["LM08", "LM19"],
        "gis": ["LM12", "LM22"],
        "tax": ["LM16"],
        "surface": ["LM06", "LM17", "LM14"],
        "document": ["LM10"],
        "county": ["LM11"],
        "pooling": ["LM15"],
        "probate": ["LM19"],
        "indian": ["LM20"],
        "federal": ["LM21"],
        "abstract": ["LM22"]
    })

# Circuit breaker parameters
CB_FAILURE_THRESHOLD = 3
CB_RECOVERY_TIME_SEC = 60

# Models
class QueryRequest(BaseModel):
    query: str
    metadata: Optional[Dict[str, Any]] = None

class RouteRequest(BaseModel):
    query: str

class AnalyzeRequest(BaseModel):
    query: str
    engines: Optional[List[str]] = None

class SubEngineResponse(BaseModel):
    engine_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: Optional[float] = None

class HealthStatus(BaseModel):
    engine_id: str
    status: str
    details: Optional[Dict[str, Any]] = None

# Helper functions
def normalize_query(query: str) -> str:
    normalized = query.strip().lower()
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> str:
    # Simple keyword-based classification for demo
    keywords_map = {
        "title": ["title", "ownership", "deed"],
        "lease": ["lease", "rent", "lessor", "lessee"],
        "mineral": ["mineral", "oil", "gas", "rights"],
        "regulatory": ["regulatory", "compliance", "filing"],
        "heirship": ["heir", "inheritance", "probate"],
        "gis": ["gis", "mapping", "coordinates"],
        "tax": ["tax", "assessment", "property tax"],
        "surface": ["surface", "right of way", "easement"],
        "document": ["document", "classification", "pdf", "scan"],
        "county": ["county", "records", "clerk"],
        "pooling": ["pooling", "unit", "drilling"],
        "probate": ["probate", "estate"],
        "indian": ["indian", "tribal", "native"],
        "federal": ["federal", "state", "government"],
        "abstract": ["abstract", "plant", "management"]
    }
    for domain, keywords in keywords_map.items():
        for kw in keywords:
            if kw in query:
                logger.debug(f"Classified domain '{domain}' for query '{query}'")
                return domain
    logger.debug(f"Default classification 'title' for query '{query}'")
    return "title"  # default domain

def route_to_sub_engines(domain_class: str) -> List[str]:
    engines = routing_rules.get(domain_class, [])
    logger.debug(f"Routing domain '{domain_class}' to engines {engines}")
    return engines

async def dispatch_to_sub_engine(engine_id: str, query: str) -> SubEngineResponse:
    start = time.time()
    # Circuit breaker check
    cb = circuit_breakers.get(engine_id, {"failures": 0, "last_failure_time": 0, "open": False})
    now = time.time()
    if cb.get("open", False):
        if now - cb["last_failure_time"] > CB_RECOVERY_TIME_SEC:
            # Attempt recovery
            cb["open"] = False
            cb["failures"] = 0
            circuit_breakers[engine_id] = cb
            logger.info(f"Circuit breaker for {engine_id} closed after recovery period")
        else:
            logger.warning(f"Circuit breaker open for {engine_id}, skipping call")
            return SubEngineResponse(
                engine_id=engine_id,
                success=False,
                error="Circuit breaker open",
                latency_ms=0.0
            )
    try:
        # Simulate sub-engine call with random delay and possible failure
        simulated_latency = random.uniform(0.05, 0.3)
        await asyncio.sleep(simulated_latency)
        # Simulate failure with 5% chance
        if random.random() < 0.05:
            raise Exception("Simulated sub-engine failure")
        response_data = {
            "result": f"Processed by {engine_id}",
            "details": {"query": query}
        }
        latency_ms = (time.time() - start) * 1000
        # Update telemetry
        telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
        prev_avg = telemetry_data["sub_engine_stats"][engine_id]["avg_latency_ms"]
        calls = telemetry_data["sub_engine_stats"][engine_id]["calls"]
        telemetry_data["sub_engine_stats"][engine_id]["avg_latency_ms"] = (prev_avg * (calls - 1) + latency_ms) / calls
        return SubEngineResponse(
            engine_id=engine_id,
            success=True,
            data=response_data,
            latency_ms=latency_ms
        )
    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        telemetry_data["sub_engine_stats"][engine_id]["failures"] += 1
        telemetry_data["sub_engine_stats"][engine_id]["calls"] += 1
        # Update circuit breaker state
        cb["failures"] += 1
        cb["last_failure_time"] = now
        if cb["failures"] >= CB_FAILURE_THRESHOLD:
            cb["open"] = True
            logger.error(f"Circuit breaker opened for {engine_id} due to repeated failures")
        circuit_breakers[engine_id] = cb
        logger.error(f"Sub-engine {engine_id} failed: {str(e)}")
        return SubEngineResponse(
            engine_id=engine_id,
            success=False,
            error=str(e),
            latency_ms=latency_ms
        )

def merge_responses(responses: List[SubEngineResponse]) -> Dict[str, Any]:
    merged = {"results": [], "errors": []}
    for resp in responses:
        if resp.success and resp.data:
            merged["results"].append({resp.engine_id: resp.data})
        elif resp.error:
            merged["errors"].append({resp.engine_id: resp.error})
    logger.debug(f"Merged response: {merged}")
    return merged

def apply_guardrails(response: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for guardrails logic (e.g., filtering sensitive info)
    # For demo, just return as is
    return response

def hash_response(response: Dict[str, Any]) -> str:
    serialized = str(response).encode('utf-8')
    response_hash = hashlib.sha256(serialized).hexdigest()
    logger.debug(f"Response hash: {response_hash}")
    return response_hash

def log_query(query: str, domain: str, engines: List[str], response_hash: str):
    logger.info(f"Query: '{query}' | Domain: {domain} | Engines: {engines} | ResponseHash: {response_hash}")

async def initialize_doctrine_cache():
    # Simulate loading doctrines into cache
    global doctrine_cache
    doctrine_cache = {
        "title": {"doctrine": "Title Law Doctrine", "coverage": 0.95},
        "lease": {"doctrine": "Lease Law Doctrine", "coverage": 0.90},
        "mineral": {"doctrine": "Mineral Rights Doctrine", "coverage": 0.85},
        # ... other doctrines
    }
    logger.info("Doctrine cache initialized")

async def start_health_monitor():
    # Simulate health monitor startup
    global health_status
    health_status["LMIE"] = {"status": "healthy", "details": {"uptime_sec": 0}}
    for engine_id in SUB_ENGINES.keys():
        health_status[engine_id] = {"status": "healthy", "details": {}}
    logger.info("Health monitor started")

async def seed_search_index():
    # Simulate seeding search index
    global search_index
    search_index = {
        "title": ["deed", "ownership", "title insurance"],
        "lease": ["lease agreement", "rent", "lessor", "lessee"],
        "mineral": ["oil rights", "gas rights", "mineral extraction"],
        # ... more index entries
    }
    logger.info("Search index seeded")

async def start_telemetry():
    # Simulate telemetry startup
    telemetry_data["start_time"] = time.time()
    logger.info("Telemetry started")

async def update_health_uptime():
    while True:
        if "LMIE" in health_status:
            health_status["LMIE"]["details"]["uptime_sec"] = int(time.time() - telemetry_data.get("start_time", time.time()))
        await asyncio.sleep(5)

async def generate_epistemic_gaps():
    # Simulate detection of epistemic gaps
    global epistemic_gaps
    epistemic_gaps = [
        "Limited coverage for tribal land titles",
        "Sparse data on federal state lands in certain counties",
        "Incomplete regulatory filing data for new jurisdictions"
    ]
    logger.info("Epistemic gaps generated")

async def generate_drift_report():
    # Simulate drift detection report
    global drift_report
    drift_report = {
        "last_check": time.time(),
        "detected_drifts": [
            {"engine": "LM03", "metric": "accuracy", "change": -0.05, "severity": "medium"},
            {"engine": "LM12", "metric": "latency", "change": +0.2, "severity": "low"}
        ]
    }
    logger.info("Drift report generated")

# FastAPI app setup
app = FastAPI(title="Landman Intelligence Engine - Domain Orchestrator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan context manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LMIE Domain Orchestrator lifespan")
    await initialize_doctrine_cache()
    await start_health_monitor()
    await seed_search_index()
    await start_telemetry()
    await generate_epistemic_gaps()
    await generate_drift_report()
    init_routing_rules()
    # Start background health uptime updater
    uptime_task = asyncio.create_task(update_health_uptime())
    try:
        yield
    finally:
        uptime_task.cancel()
        logger.info("Shutting down LMIE Domain Orchestrator lifespan")

app.router.lifespan_context = lifespan

# Request and response models for endpoints
class QueryResponse(BaseModel):
    domain: str
    routed_engines: List[str]
    merged_response: Dict[str, Any]
    response_hash: str

class HealthResponse(BaseModel):
    overall_status: str
    components: Dict[str, HealthStatus]

class MetricsResponse(BaseModel):
    latency_ms_avg: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Dict[str, Any]]

class CoverageResponse(BaseModel):
    doctrines: Dict[str, Dict[str, Any]]
    epistemic_gaps: List[str]

class DriftResponse(BaseModel):
    last_check: float
    detected_drifts: List[Dict[str, Any]]

class DoctrinesResponse(BaseModel):
    doctrines: List[str]

class RoutingResponse(BaseModel):
    routing_rules: Dict[str, List[str]]
    engine_registry: Dict[str, str]

class SubEnginesHealthResponse(BaseModel):
    sub_engines: Dict[str, HealthStatus]

class RouteDryRunResponse(BaseModel):
    domain: str
    would_invoke_engines: List[str]

class AnalyzeResponse(BaseModel):
    domain: str
    engines_invoked: List[str]
    detailed_responses: List[SubEngineResponse]
    merged_response: Dict[str, Any]
    response_hash: str

# Endpoint implementations

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.time()
    telemetry_data["queries_processed"] += 1
    query = request.query
    normalized_query = normalize_query(query)
    domain = classify_domain(normalized_query)
    engines = route_to_sub_engines(domain)
    responses = []

    # Check doctrine cache first
    if domain in doctrine_cache:
        telemetry_data["cache_hits"] += 1
    else:
        telemetry_data["cache_misses"] += 1

    # Dispatch to sub-engines concurrently with timeout and error handling
    async def call_engine(engine_id: str):
        return await dispatch_to_sub_engine(engine_id, normalized_query)

    tasks = [asyncio.create_task(call_engine(e)) for e in engines]
    try:
        responses = await asyncio.wait_for(asyncio.gather(*tasks), timeout=5.0)
    except asyncio.TimeoutError:
        logger.error("Timeout while waiting for sub-engine responses")
        # Mark timed out engines as failed
        for task, engine_id in zip(tasks, engines):
            if not task.done():
                responses.append(SubEngineResponse(
                    engine_id=engine_id,
                    success=False,
                    error="Timeout",
                    latency_ms=None
                ))

    merged = merge_responses(responses)
    guarded = apply_guardrails(merged)
    response_hash = hash_response(guarded)
    log_query(query, domain, engines, response_hash)
    latency_ms = (time.time() - start_time) * 1000
    telemetry_data["latency_ms"].append(latency_ms)
    return QueryResponse(
        domain=domain,
        routed_engines=engines,
        merged_response=guarded,
        response_hash=response_hash
    )

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    # Aggregate health from self and sub-engines
    components = {}
    # Self health
    components[ENGINE_ID] = HealthStatus(
        engine_id=ENGINE_ID,
        status=health_status.get(ENGINE_ID, {}).get("status", "unknown"),
        details=health_status.get(ENGINE_ID, {}).get("details", {})
    )
    # Sub-engines health (simulate)
    for engine_id in SUB_ENGINES.keys():
        status_info = health_status.get(engine_id, {"status": "healthy", "details": {}})
        components[engine_id] = HealthStatus(
            engine_id=engine_id,
            status=status_info.get("status", "unknown"),
            details=status_info.get("details", {})
        )
    overall_status = "healthy" if all(c.status == "healthy" for c in components.values()) else "degraded"
    return HealthResponse(overall_status=overall_status, components=components)

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    latency_list = telemetry_data.get("latency_ms", [])
    avg_latency = sum(latency_list) / len(latency_list) if latency_list else 0.0
    hits = telemetry_data.get("cache_hits", 0)
    misses = telemetry_data.get("cache_misses", 0)
    total = hits + misses
    hit_rate = hits / total if total > 0 else 0.0
    uptime_sec = time.time() - telemetry_data.get("start_time", time.time())
    queries_per_hour = (telemetry_data.get("queries_processed", 0) / uptime_sec) * 3600 if uptime_sec > 0 else 0.0
    return MetricsResponse(
        latency_ms_avg=avg_latency,
        cache_hit_rate=hit_rate,
        queries_per_hour=queries_per_hour,
        sub_engine_stats=telemetry_data.get("sub_engine_stats", {})
    )

@app.get("/coverage", response_model=CoverageResponse)
async def coverage_endpoint():
    return CoverageResponse(
        doctrines=doctrine_cache,
        epistemic_gaps=epistemic_gaps
    )

@app.get("/drift", response_model=DriftResponse)
async def drift_endpoint():
    return DriftResponse(
        last_check=drift_report.get("last_check", 0),
        detected_drifts=drift_report.get("detected_drifts", [])
    )

@app.get("/doctrines", response_model=DoctrinesResponse)
async def doctrines_endpoint():
    doctrine_list = list(doctrine_cache.keys())
    return DoctrinesResponse(doctrines=doctrine_list)

@app.get("/routing", response_model=RoutingResponse)
async def routing_endpoint():
    return RoutingResponse(
        routing_rules=routing_rules,
        engine_registry=SUB_ENGINES
    )

@app.get("/sub-engines", response_model=SubEnginesHealthResponse)
async def sub_engines_health_endpoint():
    components = {}
    for engine_id in SUB_ENGINES.keys():
        status_info = health_status.get(engine_id, {"status": "healthy", "details": {}})
        components[engine_id] = HealthStatus(
            engine_id=engine_id,
            status=status_info.get("status", "unknown"),
            details=status_info.get("details", {})
        )
    return SubEnginesHealthResponse(sub_engines=components)

@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteRequest):
    normalized_query = normalize_query(request.query)
    domain = classify_domain(normalized_query)
    engines = route_to_sub_engines(domain)
    return RouteDryRunResponse(domain=domain, would_invoke_engines=engines)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    domain = classify_domain(normalized_query)
    engines = request.engines if request.engines else route_to_sub_engines(domain)
    responses = []

    # Dispatch to specified engines concurrently
    async def call_engine(engine_id: str):
        return await dispatch_to_sub_engine(engine_id, normalized_query)

    tasks = [asyncio.create_task(call_engine(e)) for e in engines]
    try:
        responses = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
    except asyncio.TimeoutError:
        logger.error("Timeout during deep multi-engine analysis")
        for task, engine_id in zip(tasks, engines):
            if not task.done():
                responses.append(SubEngineResponse(
                    engine_id=engine_id,
                    success=False,
                    error="Timeout",
                    latency_ms=None
                ))

    merged = merge_responses(responses)
    guarded = apply_guardrails(merged)
    response_hash = hash_response(guarded)
    log_query(request.query, domain, engines, response_hash)
    return AnalyzeResponse(
        domain=domain,
        engines_invoked=engines,
        detailed_responses=responses,
        merged_response=guarded,
        response_hash=response_hash
    )

# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")