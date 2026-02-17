import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import uuid
import time
import json
import statistics
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Set, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger
import enum

ENGINE_ID = "LIE"
ENGINE_PORT = 8419
ENGINE_NAME = "Legal Intelligence Engine — Domain Orchestrator"
ENGINE_VERSION = "1.0.0"

class ResponseMode(str, enum.Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, enum.Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, enum.Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, enum.Enum):
    CONTRACT_FORMATION = "CONTRACT_FORMATION"
    CONTRACT_BREACH = "CONTRACT_BREACH"
    TORT_LIABILITY = "TORT_LIABILITY"
    NEGLIGENCE = "NEGLIGENCE"
    INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY"
    TRADEMARK = "TRADEMARK"
    PATENT = "PATENT"
    COPYRIGHT = "COPYRIGHT"
    EMPLOYMENT_TERMINATION = "EMPLOYMENT_TERMINATION"
    DISCRIMINATION = "DISCRIMINATION"
    WAGE_HOUR = "WAGE_HOUR"
    REAL_ESTATE_TRANSFER = "REAL_ESTATE_TRANSFER"
    LANDLORD_TENANT = "LANDLORD_TENANT"
    ENVIRONMENTAL_PERMIT = "ENVIRONMENTAL_PERMIT"
    CONSTRUCTION_DEFECT = "CONSTRUCTION_DEFECT"
    INSURANCE_COVERAGE = "INSURANCE_COVERAGE"
    SECURITIES_FRAUD = "SECURITIES_FRAUD"
    TAX_EVASION = "TAX_EVASION"
    BANKRUPTCY_FILING = "BANKRUPTCY_FILING"
    IMMIGRATION_STATUS = "IMMIGRATION_STATUS"
    FAMILY_LAW_DIVORCE = "FAMILY_LAW_DIVORCE"
    CHILD_CUSTODY = "CHILD_CUSTODY"
    CRIMINAL_DEFENSE = "CRIMINAL_DEFENSE"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    LITIGATION_RISK = "LITIGATION_RISK"
    DATA_PRIVACY = "DATA_PRIVACY"
    CONSUMER_PROTECTION = "CONSUMER_PROTECTION"
    CORPORATE_GOVERNANCE = "CORPORATE_GOVERNANCE"
    ANTITRUST = "ANTITRUST"
    # Add more as needed

class SubEngineStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

class QueryRequest(BaseModel):
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    query_text: str
    context: Optional[Dict[str, Any]] = None
    response_mode: ResponseMode = ResponseMode.FAST
    position_zone: PositionZone = PositionZone.PLANNING
    confidence_zone: ConfidenceZone = ConfidenceZone.DEFENSIBLE
    issue_category: Optional[IssueCategory] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    engine_id: str
    sub_engine_id: Optional[str] = None
    result: Any
    status: str
    latency_ms: Optional[float] = None
    confidence: Optional[float] = None
    orchestration_trace: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

class SubEngineConfig(BaseModel):
    engine_id: str
    name: str
    port: int
    health_url: str
    capabilities: List[str]
    weight: float = 1.0
    domains: List[str]
    status: SubEngineStatus = SubEngineStatus.UNKNOWN

class RoutingDecision(BaseModel):
    query_id: str
    selected_engine_id: str
    reason: str
    rule_matched: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    score: Optional[float] = None

class OrchestrationResult(BaseModel):
    query_id: str
    routing_decision: RoutingDecision
    response: Optional[QueryResponse] = None
    orchestration_latency_ms: Optional[float] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

SUB_ENGINE_REGISTRY: Dict[str, SubEngineConfig] = {
    "LG01": SubEngineConfig(
        engine_id="LG01",
        name="Contract Analysis",
        port=8420,
        health_url="http://localhost:8420/health",
        capabilities=["contract", "agreement", "breach", "formation", "termination", "obligation", "force majeure"],
        weight=1.0,
        domains=["contract", "agreement", "obligation", "breach", "formation", "termination"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG02": SubEngineConfig(
        engine_id="LG02",
        name="Case Law Research",
        port=8421,
        health_url="http://localhost:8421/health",
        capabilities=["case law", "precedent", "jurisprudence", "court decision", "legal research"],
        weight=1.0,
        domains=["case law", "precedent", "jurisprudence", "court decision", "legal research"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG03": SubEngineConfig(
        engine_id="LG03",
        name="Regulatory Compliance",
        port=8422,
        health_url="http://localhost:8422/health",
        capabilities=["compliance", "regulation", "regulatory", "policy", "statute", "law"],
        weight=1.0,
        domains=["compliance", "regulation", "regulatory", "policy", "statute", "law"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG04": SubEngineConfig(
        engine_id="LG04",
        name="Legal Document Drafting",
        port=8423,
        health_url="http://localhost:8423/health",
        capabilities=["drafting", "document", "template", "agreement", "contract", "memorandum"],
        weight=1.0,
        domains=["drafting", "document", "template", "agreement", "contract", "memorandum"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG05": SubEngineConfig(
        engine_id="LG05",
        name="Litigation Risk Assessment",
        port=8424,
        health_url="http://localhost:8424/health",
        capabilities=["litigation", "risk", "assessment", "dispute", "lawsuit", "claim"],
        weight=1.0,
        domains=["litigation", "risk", "assessment", "dispute", "lawsuit", "claim"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG06": SubEngineConfig(
        engine_id="LG06",
        name="Intellectual Property",
        port=8425,
        health_url="http://localhost:8425/health",
        capabilities=["intellectual property", "patent", "trademark", "copyright", "trade secret"],
        weight=1.0,
        domains=["intellectual property", "patent", "trademark", "copyright", "trade secret"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG07": SubEngineConfig(
        engine_id="LG07",
        name="Employment Law",
        port=8426,
        health_url="http://localhost:8426/health",
        capabilities=["employment", "labor", "termination", "discrimination", "wage", "hour", "harassment"],
        weight=1.0,
        domains=["employment", "labor", "termination", "discrimination", "wage", "hour", "harassment"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG08": SubEngineConfig(
        engine_id="LG08",
        name="Real Estate Law",
        port=8427,
        health_url="http://localhost:8427/health",
        capabilities=["real estate", "property", "landlord", "tenant", "lease", "transfer", "title"],
        weight=1.0,
        domains=["real estate", "property", "landlord", "tenant", "lease", "transfer", "title"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG09": SubEngineConfig(
        engine_id="LG09",
        name="Criminal Law",
        port=8428,
        health_url="http://localhost:8428/health",
        capabilities=["criminal", "defense", "prosecution", "felony", "misdemeanor", "arrest", "charge"],
        weight=1.0,
        domains=["criminal", "defense", "prosecution", "felony", "misdemeanor", "arrest", "charge"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG10": SubEngineConfig(
        engine_id="LG10",
        name="Family Law",
        port=8429,
        health_url="http://localhost:8429/health",
        capabilities=["family", "divorce", "custody", "support", "marriage", "adoption", "alimony"],
        weight=1.0,
        domains=["family", "divorce", "custody", "support", "marriage", "adoption", "alimony"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG11": SubEngineConfig(
        engine_id="LG11",
        name="Immigration Law",
        port=8430,
        health_url="http://localhost:8430/health",
        capabilities=["immigration", "visa", "status", "citizenship", "green card", "deportation"],
        weight=1.0,
        domains=["immigration", "visa", "status", "citizenship", "green card", "deportation"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG12": SubEngineConfig(
        engine_id="LG12",
        name="Bankruptcy Law",
        port=8431,
        health_url="http://localhost:8431/health",
        capabilities=["bankruptcy", "chapter 7", "chapter 11", "chapter 13", "insolvency", "debt"],
        weight=1.0,
        domains=["bankruptcy", "chapter 7", "chapter 11", "chapter 13", "insolvency", "debt"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG13": SubEngineConfig(
        engine_id="LG13",
        name="Environmental Law",
        port=8432,
        health_url="http://localhost:8432/health",
        capabilities=["environmental", "permit", "compliance", "pollution", "conservation", "EPA"],
        weight=1.0,
        domains=["environmental", "permit", "compliance", "pollution", "conservation", "EPA"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG14": SubEngineConfig(
        engine_id="LG14",
        name="Construction Law",
        port=8433,
        health_url="http://localhost:8433/health",
        capabilities=["construction", "defect", "contract", "delay", "mechanic's lien", "bond"],
        weight=1.0,
        domains=["construction", "defect", "contract", "delay", "mechanic's lien", "bond"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG15": SubEngineConfig(
        engine_id="LG15",
        name="Insurance Law",
        port=8434,
        health_url="http://localhost:8434/health",
        capabilities=["insurance", "coverage", "claim", "policy", "denial", "subrogation"],
        weight=1.0,
        domains=["insurance", "coverage", "claim", "policy", "denial", "subrogation"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG16": SubEngineConfig(
        engine_id="LG16",
        name="Securities Law",
        port=8435,
        health_url="http://localhost:8435/health",
        capabilities=["securities", "fraud", "SEC", "registration", "disclosure", "insider trading"],
        weight=1.0,
        domains=["securities", "fraud", "SEC", "registration", "disclosure", "insider trading"],
        status=SubEngineStatus.HEALTHY
    ),
    "LG17": SubEngineConfig(
        engine_id="LG17",
        name="Tax Litigation",
        port=8436,
        health_url="http://localhost:8436/health",
        capabilities=["tax", "litigation", "evasion", "IRS", "audit", "penalty"],
        weight=1.0,
        domains=["tax", "litigation", "evasion", "IRS", "audit", "penalty"],
        status=SubEngineStatus.HEALTHY
    ),
}

ROUTING_RULES: Dict[str, str] = {
    # Contract Law
    "contract": "LG01",
    "agreement": "LG01",
    "breach": "LG01",
    "force majeure": "LG01",
    "obligation": "LG01",
    "termination": "LG01",
    "formation": "LG01",
    "indemnity": "LG01",
    "consideration": "LG01",
    "warranty": "LG01",
    "assignment": "LG01",
    "novation": "LG01",
    "rescission": "LG01",
    "liquidated damages": "LG01",
    "specific performance": "LG01",
    # Case Law
    "case law": "LG02",
    "precedent": "LG02",
    "jurisprudence": "LG02",
    "court decision": "LG02",
    "legal research": "LG02",
    "holding": "LG02",
    "dictum": "LG02",
    "stare decisis": "LG02",
    "opinion": "LG02",
    "dissent": "LG02",
    # Regulatory Compliance
    "compliance": "LG03",
    "regulation": "LG03",
    "regulatory": "LG03",
    "policy": "LG03",
    "statute": "LG03",
    "law": "LG03",
    "standard": "LG03",
    "guideline": "LG03",
    "rulemaking": "LG03",
    "enforcement": "LG03",
    # Document Drafting
    "drafting": "LG04",
    "document": "LG04",
    "template": "LG04",
    "memorandum": "LG04",
    "nda": "LG04",
    "contract template": "LG04",
    "agreement draft": "LG04",
    "clause": "LG04",
    "boilerplate": "LG04",
    "term sheet": "LG04",
    # Litigation Risk
    "litigation": "LG05",
    "risk": "LG05",
    "assessment": "LG05",
    "dispute": "LG05",
    "lawsuit": "LG05",
    "claim": "LG05",
    "exposure": "LG05",
    "settlement": "LG05",
    "arbitration": "LG05",
    "mediation": "LG05",
    "discovery": "LG05",
    # Intellectual Property
    "intellectual property": "LG06",
    "patent": "LG06",
    "trademark": "LG06",
    "copyright": "LG06",
    "trade secret": "LG06",
    "infringement": "LG06",
    "licensing": "LG06",
    "registration": "LG06",
    "prior art": "LG06",
    "non-disclosure": "LG06",
    # Employment Law
    "employment": "LG07",
    "labor": "LG07",
    "termination": "LG07",
    "discrimination": "LG07",
    "wage": "LG07",
    "hour": "LG07",
    "harassment": "LG07",
    "overtime": "LG07",
    "employee": "LG07",
    "employer": "LG07",
    "wrongful termination": "LG07",
    "severance": "LG07",
    "collective bargaining": "LG07",
    # Real Estate Law
    "real estate": "LG08",
    "property": "LG08",
    "landlord": "LG08",
    "tenant": "LG08",
    "lease": "LG08",
    "transfer": "LG08",
    "title": "LG08",
    "escrow": "LG08",
    "mortgage": "LG08",
    "foreclosure": "LG08",
    "easement": "LG08",
    "zoning": "LG08",
    "deed": "LG08",
    # Criminal Law
    "criminal": "LG09",
    "defense": "LG09",
    "prosecution": "LG09",
    "felony": "LG09",
    "misdemeanor": "LG09",
    "arrest": "LG09",
    "charge": "LG09",
    "indictment": "LG09",
    "plea": "LG09",
    "sentence": "LG09",
    "probation": "LG09",
    "parole": "LG09",
    "bail": "LG09",
    "conviction": "LG09",
    # Family Law
    "family": "LG10",
    "divorce": "LG10",
    "custody": "LG10",
    "support": "LG10",
    "marriage": "LG10",
    "adoption": "LG10",
    "alimony": "LG10",
    "paternity": "LG10",
    "child support": "LG10",
    "visitation": "LG10",
    "domestic violence": "LG10",
    # Immigration Law
    "immigration": "LG11",
    "visa": "LG11",
    "status": "LG11",
    "citizenship": "LG11",
    "green card": "LG11",
    "deportation": "LG11",
    "naturalization": "LG11",
    "asylum": "LG11",
    "refugee": "LG11",
    "removal": "LG11",
    # Bankruptcy Law
    "bankruptcy": "LG12",
    "chapter 7": "LG12",
    "chapter 11": "LG12",
    "chapter 13": "LG12",
    "insolvency": "LG12",
    "debt": "LG12",
    "creditor": "LG12",
    "debtor": "LG12",
    "reorganization": "LG12",
    "liquidation": "LG12",
    "automatic stay": "LG12",
    # Environmental Law
    "environmental": "LG13",
    "permit": "LG13",
    "compliance": "LG13",
    "pollution": "LG13",
    "conservation": "LG13",
    "EPA": "LG13",
    "hazardous waste": "LG13",
    "clean air": "LG13",
    "clean water": "LG13",
    "remediation": "LG13",
    # Construction Law
    "construction": "LG14",
    "defect": "LG14",
    "delay": "LG14",
    "mechanic's lien": "LG14",
    "bond": "LG14",
    "subcontractor": "LG14",
    "general contractor": "LG14",
    "change order": "LG14",
    "retainage": "LG14",
    # Insurance Law
    "insurance": "LG15",
    "coverage": "LG15",
    "claim": "LG15",
    "policy": "LG15",
    "denial": "LG15",
    "subrogation": "LG15",
    "premium": "LG15",
    "exclusion": "LG15",
    "endorsement": "LG15",
    "reinsurance": "LG15",
    # Securities Law
    "securities": "LG16",
    "fraud": "LG16",
    "SEC": "LG16",
    "registration": "LG16",
    "disclosure": "LG16",
    "insider trading": "LG16",
    "prospectus": "LG16",
    "offering": "LG16",
    "underwriter": "LG16",
    "compliance": "LG16",
    # Tax Litigation
    "tax": "LG17",
    "litigation": "LG17",
    "evasion": "LG17",
    "IRS": "LG17",
    "audit": "LG17",
    "penalty": "LG17",
    "deficiency": "LG17",
    "assessment": "LG17",
    "tax court": "LG17",
    # Miscellaneous (cross-mapped for coverage)
    "privacy": "LG03",
    "data protection": "LG03",
    "consumer protection": "LG03",
    "antitrust": "LG03",
    "corporate governance": "LG03",
    "shareholder": "LG16",
    "merger": "LG16",
    "acquisition": "LG16",
    "divestiture": "LG16",
    "joint venture": "LG16",
    "class action": "LG05",
    "qui tam": "LG05",
    "whistleblower": "LG05",
    "statute of limitations": "LG02",
    "venue": "LG02",
    "jurisdiction": "LG02",
    "removal": "LG02",
    "summary judgment": "LG02",
    "motion to dismiss": "LG02",
    "injunction": "LG02",
    "temporary restraining order": "LG02",
    "appeal": "LG02",
    "remand": "LG02",
    "en banc": "LG02",
    "amicus": "LG02",
    "interlocutory": "LG02",
    "mandamus": "LG02",
    "certiorari": "LG02",
    "habeas corpus": "LG09",
    "probate": "LG10",
    "estate": "LG10",
    "trust": "LG10",
    "will": "LG10",
    "guardianship": "LG10",
    "conservatorship": "LG10",
    "spousal support": "LG10",
    "child support": "LG10",
    "visitation": "LG10",
    "paternity": "LG10",
    "surrogacy": "LG10",
    "emancipation": "LG10",
    "immigration bond": "LG11",
    "removal proceedings": "LG11",
    "ICE": "LG11",
    "DACA": "LG11",
    "TPS": "LG11",
    "EB-5": "LG11",
    "H-1B": "LG11",
    "L-1": "LG11",
    "F-1": "LG11",
    "J-1": "LG11",
    "O-1": "LG11",
    "TN": "LG11",
    "asylum": "LG11",
    "refugee": "LG11",
    "naturalization": "LG11",
    "citizenship": "LG11",
    "chapter 7": "LG12",
    "chapter 11": "LG12",
    "chapter 13": "LG12",
    "automatic stay": "LG12",
    "discharge": "LG12",
    "reaffirmation": "LG12",
    "means test": "LG12",
    "trustee": "LG12",
    "creditor": "LG12",
    "debtor": "LG12",
    "reorganization": "LG12",
    "liquidation": "LG12",
    "EPA": "LG13",
    "clean air": "LG13",
    "clean water": "LG13",
    "remediation": "LG13",
    "hazardous waste": "LG13",
    "superfund": "LG13",
    "CERCLA": "LG13",
    "RCRA": "LG13",
    "NEPA": "LG13",
    "endangered species": "LG13",
    "wetlands": "LG13",
    "brownfield": "LG13",
    "mechanic's lien": "LG14",
    "retainage": "LG14",
    "change order": "LG14",
    "bond": "LG14",
    "general contractor": "LG14",
    "subcontractor": "LG14",
    "delay": "LG14",
    "defect": "LG14",
    "insurance": "LG15",
    "coverage": "LG15",
    "claim": "LG15",
    "denial": "LG15",
    "subrogation": "LG15",
    "premium": "LG15",
    "exclusion": "LG15",
    "endorsement": "LG15",
    "reinsurance": "LG15",
    "securities": "LG16",
    "fraud": "LG16",
    "SEC": "LG16",
    "registration": "LG16",
    "disclosure": "LG16",
    "insider trading": "LG16",
    "prospectus": "LG16",
    "offering": "LG16",
    "underwriter": "LG16",
    "tax": "LG17",
    "litigation": "LG17",
    "evasion": "LG17",
    "IRS": "LG17",
    "audit": "LG17",
    "penalty": "LG17",
    "deficiency": "LG17",
    "assessment": "LG17",
    "tax court": "LG17",
    # ... (continue to 200+ rules, add as needed for coverage)
}

class MetricsCollector:
    def __init__(self):
        self.query_times = deque()
        self.error_counts = defaultdict(int)
        self.latencies = []
        self.query_timestamps = deque()
        self.lock = asyncio.Lock()

    async def record_query(self, latency_ms: float):
        async with self.lock:
            now = datetime.utcnow()
            self.query_times.append((now, latency_ms))
            self.latencies.append(latency_ms)
            self.query_timestamps.append(now)
            # Purge old queries over 1 hour
            cutoff = now - timedelta(hours=1)
            while self.query_timestamps and self.query_timestamps[0] < cutoff:
                self.query_timestamps.popleft()
            while self.query_times and self.query_times[0][0] < cutoff:
                self.query_times.popleft()

    async def record_error(self, error_type: str):
        async with self.lock:
            self.error_counts[error_type] += 1

    async def get_latency_stats(self) -> Dict[str, float]:
        async with self.lock:
            if not self.latencies:
                return {"min": 0.0, "max": 0.0, "mean": 0.0, "median": 0.0}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "mean": statistics.mean(self.latencies),
                "median": statistics.median(self.latencies)
            }

    async def queries_last_hour(self) -> int:
        async with self.lock:
            now = datetime.utcnow()
            cutoff = now - timedelta(hours=1)
            return sum(1 for t in self.query_timestamps if t >= cutoff)

ENGINE_IDS = [
    "LG01", "LG02", "LG03", "LG04", "LG05", "LG06", "LG07", "LG08", "LG09",
    "LG10", "LG11", "LG12", "LG13", "LG14", "LG15", "LG16", "LG17"
]

ENGINE_URLS = {
    "LG01": "http://lg01.contract-analysis.local/api",
    "LG02": "http://lg02.case-law.local/api",
    "LG03": "http://lg03.regulatory.local/api",
    "LG04": "http://lg04.doc-drafting.local/api",
    "LG05": "http://lg05.litigation-risk.local/api",
    "LG06": "http://lg06.ip.local/api",
    "LG07": "http://lg07.employment.local/api",
    "LG08": "http://lg08.real-estate.local/api",
    "LG09": "http://lg09.criminal.local/api",
    "LG10": "http://lg10.family.local/api",
    "LG11": "http://lg11.immigration.local/api",
    "LG12": "http://lg12.bankruptcy.local/api",
    "LG13": "http://lg13.environmental.local/api",
    "LG14": "http://lg14.construction.local/api",
    "LG15": "http://lg15.insurance.local/api",
    "LG16": "http://lg16.securities.local/api",
    "LG17": "http://lg17.tax-litigation.local/api"
}

ENGINE_KEYWORDS = {
    "LG01": ["contract", "agreement", "term", "obligation", "party", "breach"],
    "LG02": ["case law", "precedent", "judgment", "court decision", "citation"],
    "LG03": ["regulation", "compliance", "statute", "rule", "policy"],
    "LG04": ["draft", "document", "template", "clause", "legal writing"],
    "LG05": ["litigation", "risk", "lawsuit", "claim", "dispute"],
    "LG06": ["intellectual property", "patent", "trademark", "copyright", "ip"],
    "LG07": ["employment", "employee", "labor", "workplace", "termination"],
    "LG08": ["real estate", "property", "lease", "title", "mortgage"],
    "LG09": ["criminal", "crime", "offense", "prosecution", "defense"],
    "LG10": ["family", "divorce", "custody", "marriage", "child support"],
    "LG11": ["immigration", "visa", "citizenship", "residency", "green card"],
    "LG12": ["bankruptcy", "insolvency", "debt", "chapter 11", "restructuring"],
    "LG13": ["environmental", "pollution", "regulation", "epa", "conservation"],
    "LG14": ["construction", "contractor", "building", "project", "permit"],
    "LG15": ["insurance", "policy", "claim", "coverage", "premium"],
    "LG16": ["securities", "stock", "bond", "market", "investment"],
    "LG17": ["tax", "litigation", "irs", "audit", "tax dispute"]
}

ENGINE_CATEGORIES = {
    "LG01": "Contract Analysis",
    "LG02": "Case Law Research",
    "LG03": "Regulatory Compliance",
    "LG04": "Legal Document Drafting",
    "LG05": "Litigation Risk Assessment",
    "LG06": "Intellectual Property",
    "LG07": "Employment Law",
    "LG08": "Real Estate Law",
    "LG09": "Criminal Law",
    "LG10": "Family Law",
    "LG11": "Immigration Law",
    "LG12": "Bankruptcy Law",
    "LG13": "Environmental Law",
    "LG14": "Construction Law",
    "LG15": "Insurance Law",
    "LG16": "Securities Law",
    "LG17": "Tax Litigation"
}

# --- Data Classes and Enums ---

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
    CONTRACT = auto()
    CASE_LAW = auto()
    REGULATORY = auto()
    DOCUMENT_DRAFTING = auto()
    LITIGATION_RISK = auto()
    INTELLECTUAL_PROPERTY = auto()
    EMPLOYMENT = auto()
    REAL_ESTATE = auto()
    CRIMINAL = auto()
    FAMILY = auto()
    IMMIGRATION = auto()
    BANKRUPTCY = auto()
    ENVIRONMENTAL = auto()
    CONSTRUCTION = auto()
    INSURANCE = auto()
    SECURITIES = auto()
    TAX = auto()

class RoutingMode(Enum):
    PARALLEL = auto()
    CASCADE = auto()
    SINGLE = auto()

class QueryRequest:
    def __init__(self, text: str, metadata: Dict[str, Any] = None, mode: RoutingMode = RoutingMode.PARALLEL):
        self.text = text
        self.metadata = metadata or {}
        self.mode = mode

class RoutingDecision:
    def __init__(self, engines: List[str], categories: List[IssueCategory], mode: RoutingMode):
        self.engines = engines
        self.categories = categories
        self.mode = mode

class SubEngineConfig:
    def __init__(self, engine_id: str, url: str, category: IssueCategory):
        self.engine_id = engine_id
        self.url = url
        self.category = category

class SubEngineResponse:
    def __init__(self, engine_id: str, response: Any, status: SubEngineStatus, error: Optional[str] = None):
        self.engine_id = engine_id
        self.response = response
        self.status = status
        self.error = error

# --- Circuit Breaker Implementation ---

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = None
        self.recovery_timeout = recovery_timeout

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def allow_request(self):
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            now = time.time()
            if self.last_failure_time and (now - self.last_failure_time) > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        return False

    def on_request_result(self, success: bool):
        if success:
            self.record_success()
        else:
            self.record_failure()

# --- SubEngineHealthMonitor ---

class SubEngineHealthMonitor:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self.health_cache: Dict[str, Tuple[SubEngineStatus, float]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            eid: CircuitBreaker() for eid in ENGINE_IDS
        }

    async def _ping_engine(self, url: str, timeout: int = 5) -> SubEngineStatus:
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

    def _get_cached_status(self, engine_id: str) -> Optional[SubEngineStatus]:
        entry = self.health_cache.get(engine_id)
        if entry:
            status, ts = entry
            if (time.time() - ts) < self.ttl:
                return status
        return None

    async def check_health(self, engine_id: str) -> SubEngineStatus:
        cached = self._get_cached_status(engine_id)
        if cached is not None:
            return cached
        url = ENGINE_URLS.get(engine_id)
        if not url:
            return SubEngineStatus.UNKNOWN
        status = await self._ping_engine(url)
        self.health_cache[engine_id] = (status, time.time())
        cb = self.circuit_breakers[engine_id]
        cb.on_request_result(status == SubEngineStatus.HEALTHY)
        return status

    async def check_all_health(self) -> Dict[str, SubEngineStatus]:
        results = {}
        tasks = []
        for eid in ENGINE_IDS:
            tasks.append(self.check_health(eid))
        statuses = await asyncio.gather(*tasks)
        for eid, status in zip(ENGINE_IDS, statuses):
            results[eid] = status
        return results

    def get_healthy_engines(self) -> List[str]:
        healthy = []
        for eid in ENGINE_IDS:
            cached = self._get_cached_status(eid)
            cb = self.circuit_breakers[eid]
            if cb.allow_request() and (cached == SubEngineStatus.HEALTHY):
                healthy.append(eid)
        return healthy

    def get_circuit_breaker(self, engine_id: str) -> CircuitBreaker:
        return self.circuit_breakers[engine_id]

# --- QueryRouter ---

class QueryRouter:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    def _classify_domain(self, text: str) -> List[IssueCategory]:
        text_lower = text.lower()
        matched_categories = set()
        for eid, keywords in ENGINE_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    matched_categories.add(self._engine_id_to_category(eid))
        if not matched_categories:
            # Fallback: try to match by category name
            for eid, cat_name in ENGINE_CATEGORIES.items():
                if cat_name.lower() in text_lower:
                    matched_categories.add(self._engine_id_to_category(eid))
        return list(matched_categories)

    def _engine_id_to_category(self, engine_id: str) -> IssueCategory:
        mapping = {
            "LG01": IssueCategory.CONTRACT,
            "LG02": IssueCategory.CASE_LAW,
            "LG03": IssueCategory.REGULATORY,
            "LG04": IssueCategory.DOCUMENT_DRAFTING,
            "LG05": IssueCategory.LITIGATION_RISK,
            "LG06": IssueCategory.INTELLECTUAL_PROPERTY,
            "LG07": IssueCategory.EMPLOYMENT,
            "LG08": IssueCategory.REAL_ESTATE,
            "LG09": IssueCategory.CRIMINAL,
            "LG10": IssueCategory.FAMILY,
            "LG11": IssueCategory.IMMIGRATION,
            "LG12": IssueCategory.BANKRUPTCY,
            "LG13": IssueCategory.ENVIRONMENTAL,
            "LG14": IssueCategory.CONSTRUCTION,
            "LG15": IssueCategory.INSURANCE,
            "LG16": IssueCategory.SECURITIES,
            "LG17": IssueCategory.TAX
        }
        return mapping[engine_id]

    def _select_engines(self, categories: List[IssueCategory], mode: RoutingMode) -> List[SubEngineConfig]:
        healthy_engines = self.health_monitor.get_healthy_engines()
        configs = []
        for cat in categories:
            for eid in ENGINE_IDS:
                if self._engine_id_to_category(eid) == cat and eid in healthy_engines:
                    configs.append(SubEngineConfig(
                        engine_id=eid,
                        url=ENGINE_URLS[eid],
                        category=cat
                    ))
        if mode == RoutingMode.SINGLE and configs:
            # Select highest relevance
            return [configs[0]]
        return configs

    def _apply_routing_rules(self, query: QueryRequest) -> List[str]:
        # Example: If query mentions "urgent", prioritize Litigation Risk
        text = query.text.lower()
        if "urgent" in text or "emergency" in text:
            return ["LG05"]
        # If query mentions "draft", prioritize Document Drafting
        if "draft" in text:
            return ["LG04"]
        # If query mentions "bankruptcy", prioritize Bankruptcy Law
        if "bankruptcy" in text:
            return ["LG12"]
        return []

    def _score_engine_relevance(self, engine: SubEngineConfig, query: QueryRequest) -> float:
        text = query.text.lower()
        keywords = ENGINE_KEYWORDS.get(engine.engine_id, [])
        score = 0.0
        for kw in keywords:
            if kw in text:
                score += 1.0
        # Boost by routing rules
        routing_rule_engines = self._apply_routing_rules(query)
        if engine.engine_id in routing_rule_engines:
            score += 2.0
        return score

    def _handle_engine_failure(self, engine_id: str, error: str) -> List[str]:
        # Fallback: Remove failed engine, try next best
        healthy = self.health_monitor.get_healthy_engines()
        fallback = [eid for eid in healthy if eid != engine_id]
        return fallback

    def route_query(self, query: QueryRequest) -> RoutingDecision:
        categories = self._classify_domain(query.text)
        routing_rule_engines = self._apply_routing_rules(query)
        mode = query.mode
        configs = self._select_engines(categories, mode)
        if routing_rule_engines:
            configs = [c for c in configs if c.engine_id in routing_rule_engines]
            if not configs:
                # If routing rule engine not healthy, fallback to others
                configs = self._select_engines(categories, mode)
        # Sort by relevance score
        configs.sort(key=lambda c: self._score_engine_relevance(c, query), reverse=True)
        engine_ids = [c.engine_id for c in configs]
        return RoutingDecision(engine_ids, categories, mode)

# --- SubEngineOrchestrator ---

class SubEngineOrchestrator:
    def __init__(self, health_monitor: SubEngineHealthMonitor):
        self.health_monitor = health_monitor

    async def _call_sub_engine(self, engine_config: SubEngineConfig, query: QueryRequest) -> SubEngineResponse:
        cb = self.health_monitor.get_circuit_breaker(engine_config.engine_id)
        if not cb.allow_request():
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error="Circuit open")
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "text": query.text,
                    "metadata": query.metadata
                }
                async with session.post(engine_config.url + "/query", json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        cb.on_request_result(True)
                        return SubEngineResponse(engine_config.engine_id, data, SubEngineStatus.HEALTHY)
                    else:
                        cb.on_request_result(False)
                        return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error=f"HTTP {resp.status}")
        except Exception as ex:
            cb.on_request_result(False)
            return SubEngineResponse(engine_config.engine_id, None, SubEngineStatus.UNHEALTHY, error=str(ex))

    async def dispatch_query(self, query: QueryRequest, engines: List[SubEngineConfig]) -> List[SubEngineResponse]:
        responses = []
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            responses.append(resp)
        return responses

    async def dispatch_parallel(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Dict[str, Any]:
        tasks = [self._call_sub_engine(engine, query) for engine in engines]
        responses = await asyncio.gather(*tasks)
        merged = self._merge_responses(responses)
        return merged

    async def dispatch_cascade(self, query: QueryRequest, engines: List[SubEngineConfig]) -> Any:
        for engine in engines:
            resp = await self._call_sub_engine(engine, query)
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                return resp.response
        return {"error": "No successful response from cascade"}

    def _merge_responses(self, responses: List[SubEngineResponse]) -> Dict[str, Any]:
        result = {}
        for resp in responses:
            if resp.status == SubEngineStatus.HEALTHY and resp.response is not None:
                result[resp.engine_id] = resp.response
            elif resp.error:
                result[resp.engine_id] = {"error": resp.error}
        return result

    def _resolve_conflicts(self, responses: List[SubEngineResponse]) -> Any:
        # Simple consensus: majority identical response, else aggregate
        healthy_resps = [r.response for r in responses if r.status == SubEngineStatus.HEALTHY and r.response is not None]
        if not healthy_resps:
            return {"error": "No healthy responses"}
        # Check for identical responses
        counts = {}
        for r in healthy_resps:
            key = str(r)
            counts[key] = counts.get(key, 0) + 1
        max_count = max(counts.values())
        consensus = [k for k, v in counts.items() if v == max_count]
        if len(consensus) == 1:
            return healthy_resps[0]
        else:
            return {"aggregate": healthy_resps}

# --- Example Usage (for integration) ---

# health_monitor = SubEngineHealthMonitor()
# router = QueryRouter(health_monitor)
# orchestrator = SubEngineOrchestrator(health_monitor)

# async def process_query(text: str):
#     query = QueryRequest(text)
#     decision = router.route_query(query)
#     configs = [SubEngineConfig(eid, ENGINE_URLS[eid], router._engine_id_to_category(eid)) for eid in decision.engines]
#     if decision.mode == RoutingMode.PARALLEL:
#         result = await orchestrator.dispatch_parallel(query, configs)
#     elif decision.mode == RoutingMode.CASCADE:
#         result = await orchestrator.dispatch_cascade(query, configs)
#     else:
#         result = await orchestrator.dispatch_query(query, configs)
#     return result

class AuthorityLevel(Enum):
    CONSTITUTIONAL = auto()
    STATUTORY = auto()
    REGULATORY = auto()
    CASE_LAW = auto()
    TREATISE = auto()
    PRACTICE = auto()

authority_weights = {
    AuthorityLevel.CONSTITUTIONAL: 100,
    AuthorityLevel.STATUTORY: 80,
    AuthorityLevel.REGULATORY: 60,
    AuthorityLevel.CASE_LAW: 70,
    AuthorityLevel.TREATISE: 50,
    AuthorityLevel.PRACTICE: 30,
}

def resolve_authority_conflict(sources):
    """
    sources: list of tuples (authority_level: AuthorityLevel, source_id: str)
    Returns dominant authority level and list of sources with that level
    """
    if not sources:
        return None, []

    max_weight = -1
    dominant_level = None
    for level, _ in sources:
        weight = authority_weights.get(level, 0)
        if weight > max_weight:
            max_weight = weight
            dominant_level = level

    dominant_sources = [src for lvl, src in sources if lvl == dominant_level]
    return dominant_level, dominant_sources

# ----------------------------------------
# EPISTEMIC GUARDRAILS
# ----------------------------------------

BANNED_PHRASES = [
    "clearly", "obviously", "without doubt", "undeniably", "unquestionably",
    "beyond question", "incontrovertibly", "manifestly", "patently", "plainly",
    "self-evidently", "categorically", "definitively", "decisively", "unequivocally",
    "incontestably", "indisputably", "inarguably", "beyond dispute", "without reservation",
    "unambiguously", "irrefutably", "conclusively", "beyond cavil", "beyond peradventure",
    "beyond controversy", "without exception", "without qualification", "without fail",
    "without hesitation", "without question"
]

EPISTEMIC_CONFIDENCE_LEVELS = Enum('ConfidenceLevel', 'DEFENSIBLE AGGRESSIVE DISCLOSURE HIGH_RISK')

def apply_epistemic_guardrails(text):
    """
    Removes banned phrases and appends disclosure caveat if needed.
    Returns cleaned text.
    """
    pattern = re.compile(r'\b(' + '|'.join(re.escape(p) for p in BANNED_PHRASES) + r')\b', re.IGNORECASE)
    cleaned_text = pattern.sub('', text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

    # Add disclosure caveat if any banned phrase was found and removed
    if cleaned_text != text:
        caveat = ("[Disclosure: Certain emphatic phrases were removed to maintain epistemic humility and guard against overstatement.]")
        cleaned_text = cleaned_text + " " + caveat
    return cleaned_text

def confidence_stratification(text):
    """
    Simple heuristic stratification based on presence of hedging or certainty words.
    Returns one of EPISTEMIC_CONFIDENCE_LEVELS
    """
    text_lower = text.lower()
    if any(w in text_lower for w in ['may', 'might', 'could', 'possible', 'suggests', 'appears']):
        return EPISTEMIC_CONFIDENCE_LEVELS.DEFENSIBLE
    if any(w in text_lower for w in ['likely', 'probable', 'reasonable', 'plausible']):
        return EPISTEMIC_CONFIDENCE_LEVELS.AGGRESSIVE
    if any(w in text_lower for w in ['uncertain', 'unknown', 'disputed', 'controversial']):
        return EPISTEMIC_CONFIDENCE_LEVELS.DISCLOSURE
    if any(w in text_lower for w in ['certain', 'definite', 'absolute', 'guaranteed']):
        return EPISTEMIC_CONFIDENCE_LEVELS.HIGH_RISK
    return EPISTEMIC_CONFIDENCE_LEVELS.DEFENSIBLE

# ----------------------------------------
# FACT FRAGILITY SCORING
# ----------------------------------------

def score_fact_fragility(fact):
    """
    fact: dict with keys 'verifiability', 'recharacterization_risk', 'testimony_dependence'
    Each key value expected between 0.0 and 1.0
    Returns dict with scores and overall fragility score (0-1)
    """
    verifiability = fact.get('verifiability', 0.5)  # 0 = unverifiable, 1 = fully verifiable
    recharacterization_risk = fact.get('recharacterization_risk', 0.5)  # 0 = no risk, 1 = high risk
    testimony_dependence = fact.get('testimony_dependence', 0.5)  # 0 = no dependence, 1 = full dependence

    # Fragility increases with lower verifiability, higher recharacterization risk, and higher testimony dependence
    fragility_score = (1 - verifiability) * 0.4 + recharacterization_risk * 0.4 + testimony_dependence * 0.2
    fragility_score = min(max(fragility_score, 0.0), 1.0)

    return {
        'verifiability': verifiability,
        'recharacterization_risk': recharacterization_risk,
        'testimony_dependence': testimony_dependence,
        'fragility_score': fragility_score
    }

# ----------------------------------------
# SEMANTIC NORMALIZATION
# ----------------------------------------

DOMAIN_TERM_MAPPINGS = {
    # 50+ domain term mappings
    'plaintiff': 'claimant',
    'defendant': 'respondent',
    'contractual agreement': 'contract',
    'breach of contract': 'contract breach',
    'intellectual property': 'IP',
    'statute of limitations': 'limitation period',
    'due diligence': 'careful investigation',
    'fiduciary duty': 'trust obligation',
    'negligence': 'carelessness',
    'tortious act': 'civil wrong',
    'damages': 'compensation',
    'injunction': 'court order',
    'jurisdiction': 'legal authority',
    'precedent': 'case law',
    'arbitration': 'dispute resolution',
    'mediation': 'negotiation',
    'settlement agreement': 'resolution contract',
    'litigation': 'legal proceeding',
    'statutory interpretation': 'law analysis',
    'due process': 'fair procedure',
    'burden of proof': 'evidentiary obligation',
    'beyond reasonable doubt': 'high standard',
    'preponderance of evidence': 'more likely than not',
    'summary judgment': 'early decision',
    'class action': 'group lawsuit',
    'discovery': 'evidence gathering',
    'plea bargain': 'negotiated plea',
    'indictment': 'formal charge',
    'subpoena': 'court summons',
    'affidavit': 'sworn statement',
    'testimony': 'witness statement',
    'cross-examination': 'witness questioning',
    'hearsay': 'secondhand evidence',
    'due care': 'reasonable caution',
    'liability': 'legal responsibility',
    'statutory duty': 'legal obligation',
    'mens rea': 'criminal intent',
    'actus reus': 'criminal act',
    'double jeopardy': 'retrial prohibition',
    'habeas corpus': 'detention challenge',
    'ex parte': 'one-sided',
    'amicus curiae': 'friend of court',
    'pro bono': 'free legal service',
    'voir dire': 'jury selection',
    'res judicata': 'case decided',
    'stare decisis': 'precedent adherence',
    'ultra vires': 'beyond powers',
    'force majeure': 'unforeseeable event',
    'quantum meruit': 'reasonable value',
    'ipso facto': 'by the fact itself',
    'prima facie': 'at first sight',
    'in camera': 'private session',
}

def normalize_query(text):
    """
    Replace domain terms in text with standardized mappings.
    Case-insensitive replacement.
    """
    def replacement(match):
        term = match.group(0).lower()
        return DOMAIN_TERM_MAPPINGS.get(term, term)

    # Build regex pattern for all keys
    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in DOMAIN_TERM_MAPPINGS.keys()) + r')\b', re.IGNORECASE)
    normalized_text = pattern.sub(replacement, text)
    return normalized_text

# ----------------------------------------
# DEEP ANALYSIS
# ----------------------------------------

def multi_doctrine_decomposition(query):
    """
    Decompose query into sub-issues based on doctrine keywords.
    Returns list of sub-issues (strings).
    """
    doctrine_keywords = [
        'contract', 'tort', 'property', 'criminal', 'constitutional',
        'statutory', 'regulatory', 'case law', 'treatise', 'practice',
        'negligence', 'liability', 'damages', 'injunction', 'jurisdiction',
        'precedent', 'arbitration', 'mediation', 'litigation', 'discovery',
        'burden of proof', 'mens rea', 'actus reus', 'due diligence',
        'fiduciary duty', 'statute of limitations', 'due process',
        'double jeopardy', 'habeas corpus', 'force majeure', 'quantum meruit'
    ]
    query_lower = query.lower()
    issues = []
    for keyword in doctrine_keywords:
        if keyword in query_lower:
            issues.append(keyword)
    if not issues:
        issues.append('general legal issue')
    return issues

def build_interaction_dag(issues):
    """
    Build a dependency graph (DAG) of issues.
    For simplicity, assume some fixed dependencies based on known doctrine relations.
    Returns dict: {issue: [dependent_issues]}
    """
    dag = defaultdict(list)
    # Example dependencies (simplified)
    dependencies = {
        'contract': ['breach of contract', 'damages'],
        'tort': ['negligence', 'liability', 'damages'],
        'criminal': ['mens rea', 'actus reus', 'burden of proof'],
        'statutory': ['statute of limitations', 'statutory interpretation'],
        'constitutional': ['due process', 'jurisdiction'],
        'case law': ['precedent', 'stare decisis'],
        'litigation': ['discovery', 'summary judgment'],
        'arbitration': ['mediation'],
    }
    for issue in issues:
        deps = dependencies.get(issue, [])
        for dep in deps:
            if dep in issues:
                dag[issue].append(dep)
    return dag

def eight_step_resolution(query, doctrines, sub_engine_results):
    """
    Perform full analysis in eight conceptual steps:
    1. Normalize query
    2. Decompose doctrines
    3. Build interaction DAG
    4. Aggregate sub-engine results
    5. Resolve conflicts with authority hardening
    6. Score fact fragility
    7. Apply epistemic guardrails
    8. Generate final conclusion with zoning
    Returns dict with detailed analysis
    """
    # Step 1: Normalize query
    normalized_query = normalize_query(query)

    # Step 2: Decompose doctrines (already provided)
    decomposed_issues = doctrines

    # Step 3: Build interaction DAG
    dag = build_interaction_dag(decomposed_issues)

    # Step 4: Aggregate sub-engine results
    # sub_engine_results: dict {issue: {'analysis': str, 'authority_sources': [(AuthorityLevel, str)], 'facts': [fact_dicts]}}
    aggregated_analysis = {}
    for issue in decomposed_issues:
        res = sub_engine_results.get(issue, {})
        aggregated_analysis[issue] = res.get('analysis', '')

    # Step 5: Resolve conflicts with authority hardening
    resolved_authorities = {}
    for issue in decomposed_issues:
        sources = sub_engine_results.get(issue, {}).get('authority_sources', [])
        dominant_level, dominant_sources = resolve_authority_conflict(sources)
        resolved_authorities[issue] = {
            'dominant_level': dominant_level,
            'dominant_sources': dominant_sources
        }

    # Step 6: Score fact fragility
    fact_fragility_scores = {}
    for issue in decomposed_issues:
        facts = sub_engine_results.get(issue, {}).get('facts', [])
        scores = [score_fact_fragility(f) for f in facts]
        fact_fragility_scores[issue] = scores

    # Step 7: Apply epistemic guardrails
    guarded_analysis = {}
    for issue, analysis_text in aggregated_analysis.items():
        guarded_text = apply_epistemic_guardrails(analysis_text)
        guarded_analysis[issue] = guarded_text

    # Step 8: Generate final conclusion with zoning
    conclusions = {}
    for issue, text in guarded_analysis.items():
        conclusion = zoned_analysis(text)
        conclusions[issue] = conclusion

    return {
        'normalized_query': normalized_query,
        'decomposed_issues': decomposed_issues,
        'interaction_dag': dag,
        'aggregated_analysis': aggregated_analysis,
        'resolved_authorities': resolved_authorities,
        'fact_fragility_scores': fact_fragility_scores,
        'guarded_analysis': guarded_analysis,
        'conclusions': conclusions,
    }

def zoned_analysis(conclusion_text):
    """
    Tag conclusion text with zones: PLANNING, REPORTING, AUDIT
    Simple heuristic tagging based on keywords.
    Returns dict with 'text' and 'zone'
    """
    text_lower = conclusion_text.lower()
    if any(k in text_lower for k in ['should consider', 'recommend', 'plan', 'strategy']):
        zone = 'PLANNING'
    elif any(k in text_lower for k in ['found', 'determined', 'concluded', 'established']):
        zone = 'REPORTING'
    elif any(k in text_lower for k in ['review', 'audit', 'examine', 'verify']):
        zone = 'AUDIT'
    else:
        zone = 'REPORTING'
    return {'text': conclusion_text, 'zone': zone}

# ----------------------------------------
# DOCTRINE BLOCK DATACLASS
# ----------------------------------------

@dataclass
class DoctrineBlock:
    """A structured knowledge block representing a specific legal doctrine."""
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

# ----------------------------------------
# THREE-LAYER RESPONSE SYSTEM
# ----------------------------------------

# Simulated doctrine cache for Layer 1 (keyword -> cached analysis)
DOCTRINE_CACHE = {
    'contract breach': "Cached analysis on contract breach: The breach must be material and affect the contract's core obligations.",
    'negligence': "Cached analysis on negligence: Duty, breach, causation, and damages must be established.",
    'statute of limitations': "Cached analysis on statute of limitations: Claims must be brought within the prescribed time limits.",
}

# Simulated sub-engines for Layer 2
def sub_engine_contract(query):
    time.sleep(0.1)  # Simulate processing delay
    return {
        'analysis': f"Contract sub-engine analysis for query: {query}",
        'authority_sources': [(AuthorityLevel.STATUTORY, 'Contract Statute 123')],
        'facts': [{'verifiability': 0.9, 'recharacterization_risk': 0.1, 'testimony_dependence': 0.2}]
    }

def sub_engine_tort(query):
    time.sleep(0.15)
    return {
        'analysis': f"Tort sub-engine analysis for query: {query}",
        'authority_sources': [(AuthorityLevel.CASE_LAW, 'Tort Case XYZ')],
        'facts': [{'verifiability': 0.7, 'recharacterization_risk': 0.3, 'testimony_dependence': 0.4}]
    }

def sub_engine_criminal(query):
    time.sleep(0.18)
    return {
        'analysis': f"Criminal sub-engine analysis for query: {query}",
        'authority_sources': [(AuthorityLevel.CONSTITUTIONAL, 'Constitution Article 5')],
        'facts': [{'verifiability': 0.8, 'recharacterization_risk': 0.2, 'testimony_dependence': 0.5}]
    }

SUB_ENGINES = {
    'contract': sub_engine_contract,
    'tort': sub_engine_tort,
    'criminal': sub_engine_criminal,
}

def doctrine_cache_lookup(query):
    """
    Layer 1: Lookup doctrine cache by matching keywords.
    Returns cached analysis or None.
    """
    start_time = time.time()
    query_lower = query.lower()
    for keyword, cached_analysis in DOCTRINE_CACHE.items():
        if keyword in query_lower:
            elapsed = (time.time() - start_time) * 1000
            if elapsed <= 200:
                return cached_analysis
    return None

def semantic_search_sub_engine_routing(query):
    """
    Layer 2: Semantic search to identify relevant sub-engines and dispatch.
    Returns dict {issue: sub-engine result}
    """
    issues = multi_doctrine_decomposition(query)
    results = {}
    for issue in issues:
        engine_key = None
        # Map issue to sub-engine keys
        if 'contract' in issue:
            engine_key = 'contract'
        elif 'tort' in issue or 'negligence' in issue or 'liability' in issue:
            engine_key = 'tort'
        elif 'criminal' in issue or 'mens rea' in issue or 'actus reus' in issue:
            engine_key = 'criminal'
        if engine_key and engine_key in SUB_ENGINES:
            results[issue] = SUB_ENGINES[engine_key](query)
        else:
            # Default fallback
            results[issue] = {
                'analysis': f"No specialized sub-engine available for issue '{issue}'.",
                'authority_sources': [],
                'facts': []
            }
    return results

def deep_multi_engine_analysis(query):
    """
    Layer 3: Parallel dispatch to multiple sub-engines, merge results, resolve conflicts.
    Returns full analysis dict.
    """
    issues = multi_doctrine_decomposition(query)
    results = {}

    def run_sub_engine(issue):
        engine_key = None
        if 'contract' in issue:
            engine_key = 'contract'
        elif 'tort' in issue or 'negligence' in issue or 'liability' in issue:
            engine_key = 'tort'
        elif 'criminal' in issue or 'mens rea' in issue or 'actus reus' in issue:
            engine_key = 'criminal'
        if engine_key and engine_key in SUB_ENGINES:
            return (issue, SUB_ENGINES[engine_key](query))
        else:
            return (issue, {
                'analysis': f"No specialized sub-engine available for issue '{issue}'.",
                'authority_sources': [],
                'facts': []
            })

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_sub_engine, issue) for issue in issues]
        for future in as_completed(futures):
            issue, res = future.result()
            results[issue] = res

    # Merge and resolve conflicts using eight_step_resolution
    full_analysis = eight_step_resolution(query, issues, results)
    return full_analysis

def three_layer_response(query):
    """
    Implements the three-layer response system:
    1. Doctrine cache lookup (0-200ms)
    2. Semantic search + sub-engine routing
    3. Deep multi-engine analysis
    Returns final analysis dict or cached string.
    """
    # Layer 1
    cached = doctrine_cache_lookup(query)
    if cached:
        return {'layer': 1, 'result': cached}

    # Layer 2
    layer2_results = semantic_search_sub_engine_routing(query)
    # If layer 2 results are shallow or incomplete, proceed to layer 3
    shallow = all(not res['analysis'] or 'No specialized' in res['analysis'] for res in layer2_results.values())
    if not shallow:
        return {'layer': 2, 'result': layer2_results}

    # Layer 3
    layer3_results = deep_multi_engine_analysis(query)
    return {'layer': 3, 'result': layer3_results}

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
        self._doctrine_hits: Dict[str, int] = {}
        self._doctrine_queries: Dict[str, int] = {}
        self._sub_engine_stats: Dict[str, List[QueryTelemetry]] = {}

    def record_query(self, telemetry: QueryTelemetry):
        with self._lock:
            self._queries.append(telemetry)
            for engine in telemetry.engines_invoked:
                if engine not in self._sub_engine_stats:
                    self._sub_engine_stats[engine] = []
                self._sub_engine_stats[engine].append(telemetry)
            for engine in telemetry.engines_invoked:
                self._doctrine_queries[engine] = self._doctrine_queries.get(engine, 0) + 1
            if telemetry.confidence > 0.7:
                for engine in telemetry.engines_invoked:
                    self._doctrine_hits[engine] = self._doctrine_hits.get(engine, 0) + 1

    def record_error(self, telemetry: QueryTelemetry):
        with self._lock:
            self._errors.append(telemetry)

    def get_latency_stats(self) -> Dict[str, float]:
        with self._lock:
            latencies = [q.latency_ms for q in self._queries]
        if not latencies:
            return dict(avg=0, p50=0, p95=0, p99=0, min=0, max=0)
        latencies_sorted = sorted(latencies)
        return {
            'avg': statistics.mean(latencies),
            'p50': statistics.median(latencies),
            'p95': latencies_sorted[int(len(latencies_sorted) * 0.95)-1],
            'p99': latencies_sorted[int(len(latencies_sorted) * 0.99)-1],
            'min': latencies_sorted[0],
            'max': latencies_sorted[-1]
        }

    def get_doctrine_hit_rate(self) -> Dict[str, float]:
        with self._lock:
            rates = {}
            for doctrine, hits in self._doctrine_hits.items():
                total = self._doctrine_queries.get(doctrine, 1)
                rates[doctrine] = hits / total
            return rates

    def queries_last_hour(self) -> List[QueryTelemetry]:
        cutoff = time.time() - 3600
        with self._lock:
            return [q for q in self._queries if q.timestamp >= cutoff]

    def get_sub_engine_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine, queries in self._sub_engine_stats.items():
                latencies = [q.latency_ms for q in queries]
                errors = [q for q in queries if q.error]
                stats[engine] = {
                    'count': len(queries),
                    'avg_latency': statistics.mean(latencies) if latencies else 0,
                    'error_rate': len(errors) / len(queries) if queries else 0,
                    'availability': 1 - (len(errors) / len(queries) if queries else 0)
                }
            return stats

# --- DRIFT WATCHER ---

class DriftWatcher:
    def __init__(self):
        self._lock = threading.Lock()
        self._baselines: Dict[str, List[float]] = {}
        self._drift_history: Dict[str, List[Tuple[float, float]]] = {}
        self._alerts: List[Dict[str, Any]] = []

    def record_baseline(self, doctrine: str, confidence: float):
        with self._lock:
            if doctrine not in self._baselines:
                self._baselines[doctrine] = []
            self._baselines[doctrine].append(confidence)
            timestamp = time.time()
            if doctrine not in self._drift_history:
                self._drift_history[doctrine] = []
            self._drift_history[doctrine].append((timestamp, confidence))

    def detect_drift(self, doctrine: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            history = self._drift_history.get(doctrine, [])
            if len(history) < 10:
                return None
            baseline_confidences = [c for _, c in history[:len(history)//2]]
            recent_confidences = [c for _, c in history[len(history)//2:]]
            baseline_avg = statistics.mean(baseline_confidences)
            recent_avg = statistics.mean(recent_confidences)
            drift = recent_avg - baseline_avg
            drift_pct = drift / baseline_avg if baseline_avg != 0 else 0
            if abs(drift_pct) > 0.10:
                alert = {
                    'doctrine': doctrine,
                    'baseline_avg': baseline_avg,
                    'recent_avg': recent_avg,
                    'drift_pct': drift_pct,
                    'timestamp': time.time()
                }
                self._alerts.append(alert)
                return alert
            return None

    def get_drift_report(self) -> List[Dict[str, Any]]:
        with self._lock:
            report = []
            for doctrine in self._drift_history:
                alert = self.detect_drift(doctrine)
                if alert:
                    report.append(alert)
            return report

# --- COVERAGE MAP ---

class CoverageTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._triggered: Dict[str, int] = {}
        self._missed: List[str] = []
        self._epistemic_gaps: List[str] = []
        self._sub_engine_coverage: Dict[str, Dict[str, int]] = {}

    def record_triggered(self, doctrine: str, sub_engine: str):
        with self._lock:
            self._triggered[doctrine] = self._triggered.get(doctrine, 0) + 1
            if sub_engine not in self._sub_engine_coverage:
                self._sub_engine_coverage[sub_engine] = {}
            self._sub_engine_coverage[sub_engine][doctrine] = self._sub_engine_coverage[sub_engine].get(doctrine, 0) + 1

    def record_missed(self, query_id: str):
        with self._lock:
            self._missed.append(query_id)

    def record_epistemic_gap(self, query_id: str):
        with self._lock:
            self._epistemic_gaps.append(query_id)

    def get_coverage_report(self) -> Dict[str, Any]:
        with self._lock:
            total_triggered = sum(self._triggered.values())
            total_missed = len(self._missed)
            total_gaps = len(self._epistemic_gaps)
            per_sub_engine = {}
            for sub_engine, doctrines in self._sub_engine_coverage.items():
                per_sub_engine[sub_engine] = {
                    'doctrines_triggered': sum(doctrines.values()),
                    'unique_doctrines': len(doctrines)
                }
            return {
                'total_triggered': total_triggered,
                'total_missed': total_missed,
                'epistemic_gaps': total_gaps,
                'per_sub_engine': per_sub_engine
            }

    def identify_epistemic_gaps(self, queries: List[QueryTelemetry], doctrine_matcher):
        with self._lock:
            for q in queries:
                matched = doctrine_matcher(q)
                if not matched:
                    self.record_epistemic_gap(q.query_id)

# --- DETERMINISM HASH ---

def compute_determinism_hash(query: Any, response: Any) -> str:
    query_bytes = json.dumps(query, sort_keys=True, default=str).encode('utf-8')
    response_bytes = json.dumps(response, sort_keys=True, default=str).encode('utf-8')
    m = hashlib.sha256()
    m.update(query_bytes)
    m.update(response_bytes)
    return m.hexdigest()

def verify_reproducibility(query: Any, response: Any, expected_hash: str) -> bool:
    actual_hash = compute_determinism_hash(query, response)
    return actual_hash == expected_hash

# --- AUDIT TRAIL ---

class AuditTrailWriter:
    def __init__(self, audit_dir: str):
        self.audit_dir = audit_dir
        self._lock = threading.Lock()
        self._current_date = datetime.date.today()
        self._current_file = self._get_file_path(self._current_date)
        os.makedirs(self.audit_dir, exist_ok=True)
        self._file_handle = open(self._current_file, 'a', encoding='utf-8')

    def _get_file_path(self, date: datetime.date) -> str:
        return os.path.join(self.audit_dir, f"audit_{date.isoformat()}.jsonl")

    def _rotate_file(self):
        with self._lock:
            today = datetime.date.today()
            if today != self._current_date:
                self._file_handle.close()
                self._current_date = today
                self._current_file = self._get_file_path(today)
                self._file_handle = open(self._current_file, 'a', encoding='utf-8')

    def write(self, query_id: str, timestamp: float, engine_id: str, engines_invoked: List[str], mode: str, confidence: float, latency: float, cache_hit: bool):
        self._rotate_file()
        record = {
            'query_id': query_id,
            'timestamp': timestamp,
            'engine_id': engine_id,
            'engines_invoked': engines_invoked,
            'mode': mode,
            'confidence': confidence,
            'latency': latency,
            'cache_hit': cache_hit
        }
        with self._lock:
            self._file_handle.write(json.dumps(record) + '\n')
            self._file_handle.flush()

    def forensic_replay(self, date: Optional[datetime.date] = None) -> List[Dict[str, Any]]:
        if date is None:
            date = self._current_date
        file_path = self._get_file_path(date)
        records = []
        if not os.path.exists(file_path):
            return records
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    records.append(json.loads(line.strip()))
                except Exception:
                    continue
        return records

# --- PERFORMANCE PROFILER ---

class PerformanceProfiler:
    def __init__(self):
        self._lock = threading.Lock()
        self._sub_engine_latencies: Dict[str, List[float]] = {}
        self._sub_engine_errors: Dict[str, int] = {}
        self._sub_engine_availability: Dict[str, int] = {}
        self._sub_engine_total: Dict[str, int] = {}
        self._sub_engine_sla: Dict[str, Dict[str, float]] = {}

    def record(self, sub_engine: str, latency: float, error: Optional[str]):
        with self._lock:
            if sub_engine not in self._sub_engine_latencies:
                self._sub_engine_latencies[sub_engine] = []
            self._sub_engine_latencies[sub_engine].append(latency)
            self._sub_engine_total[sub_engine] = self._sub_engine_total.get(sub_engine, 0) + 1
            if error:
                self._sub_engine_errors[sub_engine] = self._sub_engine_errors.get(sub_engine, 0) + 1
            else:
                self._sub_engine_availability[sub_engine] = self._sub_engine_availability.get(sub_engine, 0) + 1

    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            stats = {}
            for engine in self._sub_engine_latencies:
                latencies = self._sub_engine_latencies[engine]
                errors = self._sub_engine_errors.get(engine, 0)
                total = self._sub_engine_total.get(engine, 1)
                avail = self._sub_engine_availability.get(engine, 0)
                stats[engine] = {
                    'avg_latency': statistics.mean(latencies) if latencies else 0,
                    'error_rate': errors / total,
                    'availability': avail / total,
                    'sla': self._sub_engine_sla.get(engine, {})
                }
            return stats

    def set_sla(self, sub_engine: str, latency_ms: float, error_rate: float, availability: float):
        with self._lock:
            self._sub_engine_sla[sub_engine] = {
                'latency_ms': latency_ms,
                'error_rate': error_rate,
                'availability': availability
            }

    def check_sla(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            violations = {}
            stats = self.get_stats()
            for engine, stat in stats.items():
                sla = self._sub_engine_sla.get(engine, {})
                violation = {}
                if sla:
                    if stat['avg_latency'] > sla.get('latency_ms', float('inf')):
                        violation['latency'] = stat['avg_latency']
                    if stat['error_rate'] > sla.get('error_rate', float('inf')):
                        violation['error_rate'] = stat['error_rate']
                    if stat['availability'] < sla.get('availability', 0):
                        violation['availability'] = stat['availability']
                if violation:
                    violations[engine] = violation
            return violations

# --- DOMAIN ORCHESTRATOR ENGINE ---

class DomainOrchestrator:
    def __init__(self, audit_dir: str):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_tracker = CoverageTracker()
        self.audit_trail = AuditTrailWriter(audit_dir)
        self.performance_profiler = PerformanceProfiler()
        self._doctrine_matcher = self._default_doctrine_matcher

    def _default_doctrine_matcher(self, q: QueryTelemetry) -> List[str]:
        # Placeholder: match query to doctrines based on engines_invoked
        return q.engines_invoked

    def process_query(self, query_id: str, query: Any, response: Any, engines_invoked: List[str], mode: str, confidence: float, latency: float, cache_hit: bool, engine_id: str, error: Optional[str] = None):
        timestamp = time.time()
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=timestamp,
            latency_ms=latency,
            cache_hit=cache_hit,
            engines_invoked=engines_invoked,
            mode=mode,
            confidence=confidence,
            error=error
        )
        self.telemetry.record_query(telemetry)
        if error:
            self.telemetry.record_error(telemetry)
        for doctrine in engines_invoked:
            self.drift_watcher.record_baseline(doctrine, confidence)
            self.coverage_tracker.record_triggered(doctrine, engine_id)
        if not engines_invoked:
            self.coverage_tracker.record_epistemic_gap(query_id)
        self.audit_trail.write(query_id, timestamp, engine_id, engines_invoked, mode, confidence, latency, cache_hit)
        for engine in engines_invoked:
            self.performance_profiler.record(engine, latency, error)

    def get_latency_stats(self):
        return self.telemetry.get_latency_stats()

    def get_doctrine_hit_rate(self):
        return self.telemetry.get_doctrine_hit_rate()

    def get_drift_report(self):
        return self.drift_watcher.get_drift_report()

    def get_coverage_report(self):
        return self.coverage_tracker.get_coverage_report()

    def get_sub_engine_stats(self):
        return self.telemetry.get_sub_engine_stats()

    def get_performance_stats(self):
        return self.performance_profiler.get_stats()

    def check_sla(self):
        return self.performance_profiler.check_sla()

    def forensic_replay(self, date: Optional[datetime.date] = None):
        return self.audit_trail.forensic_replay(date)

    def verify_determinism(self, query: Any, response: Any, expected_hash: str) -> bool:
        return verify_reproducibility(query, response, expected_hash)

    def identify_epistemic_gaps(self):
        queries = self.telemetry.queries_last_hour()
        self.coverage_tracker.identify_epistemic_gaps(queries, self._doctrine_matcher)

    def set_doctrine_matcher(self, matcher_fn):
        self._doctrine_matcher = matcher_fn

    def set_sla(self, sub_engine: str, latency_ms: float, error_rate: float, availability: float):
        self.performance_profiler.set_sla(sub_engine, latency_ms, error_rate, availability)

# --- Example Usage (for integration testing) ---

if __name__ == "__main__":
    orchestrator = DomainOrchestrator(audit_dir="./audit_logs")
    for i in range(100):
        query_id = f"Q{i:04d}"
        query = {"text": f"Legal query {i}"}
        response = {"answer": f"Legal answer {i}", "confidence": 0.8 - (i % 10) * 0.01}
        engines_invoked = ["DoctrineA"] if i % 3 == 0 else ["DoctrineB"] if i % 5 == 0 else []
        mode = "production"
        confidence = response["confidence"]
        latency = 50 + (i % 10) * 5
        cache_hit = (i % 7 == 0)
        engine_id = engines_invoked[0] if engines_invoked else "None"
        error = None if i % 13 != 0 else "Timeout"
        orchestrator.process_query(query_id, query, response, engines_invoked, mode, confidence, latency, cache_hit, engine_id, error)
    print("Latency Stats:", orchestrator.get_latency_stats())
    print("Doctrine Hit Rate:", orchestrator.get_doctrine_hit_rate())
    print("Drift Report:", orchestrator.get_drift_report())
    print("Coverage Report:", orchestrator.get_coverage_report())
    print("Sub Engine Stats:", orchestrator.get_sub_engine_stats())
    print("Performance Stats:", orchestrator.get_performance_stats())
    print("SLA Violations:", orchestrator.check_sla())
    orchestrator.identify_epistemic_gaps()
    print("Epistemic Gaps:", orchestrator.get_coverage_report()['epistemic_gaps'])
    # Forensic replay for today
    replay = orchestrator.forensic_replay()
    print("Forensic Replay Records:", len(replay))
    # Determinism hash check
    q = {"text": "Sample legal query"}
    r = {"answer": "Sample legal answer", "confidence": 0.95}
    hash_val = compute_determinism_hash(q, r)
    assert orchestrator.verify_determinism(q, r, hash_val)

ENGINE_ID = "LIE"
ENGINE_PORT = 8419
SUB_ENGINES = {
    "LG01": "Contract Analysis",
    "LG02": "Case Law Research",
    "LG03": "Regulatory Compliance",
    "LG04": "Legal Document Drafting",
    "LG05": "Litigation Risk Assessment",
    "LG06": "Intellectual Property",
    "LG07": "Employment Law",
    "LG08": "Real Estate Law",
    "LG09": "Criminal Law",
    "LG10": "Family Law",
    "LG11": "Immigration Law",
    "LG12": "Bankruptcy Law",
    "LG13": "Environmental Law",
    "LG14": "Construction Law",
    "LG15": "Insurance Law",
    "LG16": "Securities Law",
    "LG17": "Tax Litigation",
}

# Logger setup
logger = logging.getLogger("LIE_Orchestrator")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Models

class QueryRequest(BaseModel):
    query: str = Field(..., description="User query text")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    response: str
    sub_engine_responses: Dict[str, Any]
    merged: bool = True
    cached: bool = False

class HealthStatus(BaseModel):
    status: str
    details: Dict[str, Any]

class MetricsResponse(BaseModel):
    latency_ms_avg: float
    latency_ms_p95: float
    cache_hit_rate: float
    queries_per_hour: float
    sub_engine_stats: Dict[str, Dict[str, Any]]

class CoverageReport(BaseModel):
    doctrine_coverage_percent: float
    epistemic_gaps: List[str]

class DriftReport(BaseModel):
    drift_detected: bool
    drift_score: float
    details: Dict[str, Any]

class DoctrinesList(BaseModel):
    doctrines: List[str]

class RoutingRules(BaseModel):
    rules: Dict[str, Any]
    engine_registry: Dict[str, str]

class SubEngineHealth(BaseModel):
    sub_engine: str
    status: str
    last_checked: datetime
    error: Optional[str] = None

class SubEnginesHealthDashboard(BaseModel):
    health: List[SubEngineHealth]

class RouteDryRunRequest(BaseModel):
    query: str

class RouteDryRunResponse(BaseModel):
    engines_to_invoke: List[str]

class AnalyzeRequest(BaseModel):
    query: str
    analysis_depth: Optional[int] = 3

class AnalyzeResponse(BaseModel):
    analysis_results: Dict[str, Any]

# Internal components and state

class DoctrineCache:
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def initialize(self):
        logger.info("Initializing doctrine cache...")
        # Simulate loading doctrines
        with self.lock:
            self.cache = {
                "contract_law": "Doctrine content for contract law...",
                "case_law": "Doctrine content for case law...",
                "regulatory": "Doctrine content for regulatory compliance...",
                # ... more doctrines
            }
        logger.info("Doctrine cache initialized with %d doctrines", len(self.cache))

    def get(self, key: str) -> Optional[str]:
        with self.lock:
            return self.cache.get(key)

    def list_doctrines(self) -> List[str]:
        with self.lock:
            return list(self.cache.keys())

doctrine_cache = DoctrineCache()

class HealthMonitor:
    def __init__(self):
        self.status = "starting"
        self.sub_engine_health = {}
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)

    def start(self):
        logger.info("Starting health monitor...")
        self.status = "running"
        self._thread.start()

    def stop(self):
        logger.info("Stopping health monitor...")
        self._stop_event.set()
        self._thread.join()
        self.status = "stopped"

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            self.check_sub_engines()
            time.sleep(10)

    def check_sub_engines(self):
        with self.lock:
            for engine_id in SUB_ENGINES.keys():
                # Simulate health check with random success/failure
                healthy = random.choices([True, False], weights=[0.95, 0.05])[0]
                error = None if healthy else "Timeout"
                self.sub_engine_health[engine_id] = {
                    "status": "healthy" if healthy else "unhealthy",
                    "last_checked": datetime.utcnow(),
                    "error": error,
                }
            logger.debug("Health monitor updated sub-engine statuses")

    def get_health(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "engine_status": self.status,
                "sub_engines": self.sub_engine_health.copy(),
            }

health_monitor = HealthMonitor()

class SearchIndex:
    def __init__(self):
        self.index = {}
        self.lock = threading.Lock()

    def seed(self):
        logger.info("Seeding search index...")
        with self.lock:
            # Simulate seeding index with doctrine keys and some keywords
            self.index = {
                "contract": ["LG01"],
                "case": ["LG02"],
                "regulatory": ["LG03"],
                "drafting": ["LG04"],
                "litigation": ["LG05"],
                "intellectual": ["LG06"],
                "employment": ["LG07"],
                "real estate": ["LG08"],
                "criminal": ["LG09"],
                "family": ["LG10"],
                "immigration": ["LG11"],
                "bankruptcy": ["LG12"],
                "environmental": ["LG13"],
                "construction": ["LG14"],
                "insurance": ["LG15"],
                "securities": ["LG16"],
                "tax": ["LG17"],
            }
        logger.info("Search index seeded with %d keywords", len(self.index))

    def query(self, text: str) -> List[str]:
        with self.lock:
            matched_engines = set()
            text_lower = text.lower()
            for keyword, engines in self.index.items():
                if keyword in text_lower:
                    matched_engines.update(engines)
            return list(matched_engines)

search_index = SearchIndex()

class Telemetry:
    def __init__(self):
        self.latencies = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.query_timestamps = []
        self.sub_engine_stats = {k: {"calls": 0, "failures": 0, "timeouts": 0} for k in SUB_ENGINES.keys()}
        self.lock = threading.Lock()

    def start(self):
        logger.info("Telemetry started")

    def record_latency(self, ms: float):
        with self.lock:
            self.latencies.append(ms)
            # Keep only last 1000 latencies
            if len(self.latencies) > 1000:
                self.latencies.pop(0)

    def record_cache_hit(self):
        with self.lock:
            self.cache_hits += 1

    def record_cache_miss(self):
        with self.lock:
            self.cache_misses += 1

    def record_query(self):
        with self.lock:
            self.query_timestamps.append(datetime.utcnow())
            # Keep only last 24 hours
            cutoff = datetime.utcnow() - timedelta(hours=24)
            self.query_timestamps = [t for t in self.query_timestamps if t > cutoff]

    def record_sub_engine_call(self, engine_id: str):
        with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["calls"] += 1

    def record_sub_engine_failure(self, engine_id: str):
        with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["failures"] += 1

    def record_sub_engine_timeout(self, engine_id: str):
        with self.lock:
            if engine_id in self.sub_engine_stats:
                self.sub_engine_stats[engine_id]["timeouts"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        with self.lock:
            latencies_sorted = sorted(self.latencies)
            count = len(latencies_sorted)
            avg_latency = sum(latencies_sorted) / count if count > 0 else 0.0
            p95_latency = latencies_sorted[int(0.95 * count)] if count > 0 else 0.0
            total_queries = len(self.query_timestamps)
            cache_total = self.cache_hits + self.cache_misses
            cache_hit_rate = (self.cache_hits / cache_total) if cache_total > 0 else 0.0
            queries_per_hour = total_queries / 24.0
            return {
                "latency_ms_avg": avg_latency,
                "latency_ms_p95": p95_latency,
                "cache_hit_rate": cache_hit_rate,
                "queries_per_hour": queries_per_hour,
                "sub_engine_stats": self.sub_engine_stats.copy(),
            }

telemetry = Telemetry()

# Circuit breaker implementation per sub-engine
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time_sec=60):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = threading.Lock()

    def record_failure(self):
        with self.lock:
            self.failures += 1
            self.last_failure_time = datetime.utcnow()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning("Circuit breaker OPEN due to failures")

    def record_success(self):
        with self.lock:
            self.failures = 0
            self.state = "CLOSED"

    def allow_request(self) -> bool:
        with self.lock:
            if self.state == "OPEN":
                if self.last_failure_time and (datetime.utcnow() - self.last_failure_time).total_seconds() > self.recovery_time_sec:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit breaker HALF_OPEN, testing service")
                    return True
                else:
                    return False
            return True

circuit_breakers = {engine_id: CircuitBreaker() for engine_id in SUB_ENGINES.keys()}

# Helper functions

def normalize_query(query: str) -> str:
    # Basic normalization: strip, lowercase, remove extra spaces
    normalized = ' '.join(query.strip().lower().split())
    logger.debug(f"Normalized query: {normalized}")
    return normalized

def classify_domain(query: str) -> List[str]:
    # Use search index to classify which sub-engines are relevant
    engines = search_index.query(query)
    logger.debug(f"Classified domain engines: {engines}")
    return engines

async def dispatch_to_sub_engine(engine_id: str, query: str, timeout_sec=5) -> Dict[str, Any]:
    # Simulate sub-engine dispatch with async sleep and random success/failure
    if not circuit_breakers[engine_id].allow_request():
        logger.warning(f"Circuit breaker OPEN for {engine_id}, skipping call")
        telemetry.record_sub_engine_failure(engine_id)
        return {"error": "Circuit breaker open", "engine_id": engine_id}

    telemetry.record_sub_engine_call(engine_id)
    try:
        # Simulate network call latency
        simulated_latency = random.uniform(0.1, 1.0)
        await asyncio.sleep(simulated_latency)

        # Simulate random failure
        if random.random() < 0.1:
            raise asyncio.TimeoutError("Simulated timeout")

        # Simulate sub-engine response
        response = {
            "engine_id": engine_id,
            "engine_name": SUB_ENGINES[engine_id],
            "result": f"Processed query '{query}' in {SUB_ENGINES[engine_id]}",
            "latency": simulated_latency,
        }
        circuit_breakers[engine_id].record_success()
        return response
    except asyncio.TimeoutError:
        telemetry.record_sub_engine_timeout(engine_id)
        circuit_breakers[engine_id].record_failure()
        logger.error(f"Timeout from sub-engine {engine_id}")
        return {"error": "Timeout", "engine_id": engine_id}
    except Exception as e:
        telemetry.record_sub_engine_failure(engine_id)
        circuit_breakers[engine_id].record_failure()
        logger.error(f"Error from sub-engine {engine_id}: {str(e)}")
        return {"error": str(e), "engine_id": engine_id}

def merge_responses(responses: List[Dict[str, Any]]) -> str:
    # Simple merge: concatenate results, skip errors
    merged_parts = []
    for resp in responses:
        if "result" in resp:
            merged_parts.append(resp["result"])
        elif "error" in resp:
            merged_parts.append(f"[{resp['engine_id']} error: {resp['error']}]")
    merged_text = "\n".join(merged_parts)
    logger.debug(f"Merged response: {merged_text}")
    return merged_text

def apply_guardrails(response_text: str) -> str:
    # Placeholder for guardrails: e.g. remove sensitive info, enforce length limits
    max_length = 2000
    guarded = response_text[:max_length]
    logger.debug("Applied guardrails to response")
    return guarded

def hash_response(response_text: str) -> str:
    h = hashlib.sha256(response_text.encode("utf-8")).hexdigest()
    logger.debug(f"Response hash: {h}")
    return h

def log_query(user_id: Optional[str], query: str, response_hash: str, engines_invoked: List[str]):
    logger.info(f"User: {user_id}, Query: '{query}', ResponseHash: {response_hash}, Engines: {engines_invoked}")

async def fallback_to_doctrine_cache(query: str) -> Optional[str]:
    # Attempt to find doctrine content matching query keywords
    doctrines = doctrine_cache.list_doctrines()
    for doctrine in doctrines:
        if doctrine in query.lower():
            content = doctrine_cache.get(doctrine)
            if content:
                logger.info(f"Fallback to doctrine cache for doctrine: {doctrine}")
                return content
    return None

# FastAPI app setup

app = FastAPI(title="Legal Intelligence Engine - Domain Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan management

@app.on_event("startup")
async def startup_event():
    # Initialize doctrine cache
    doctrine_cache.initialize()
    # Start health monitor
    health_monitor.start()
    # Seed search index
    search_index.seed()
    # Start telemetry
    telemetry.start()
    logger.info(f"{ENGINE_ID} started on port {ENGINE_PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    # Stop health monitor
    health_monitor.stop()
    logger.info(f"{ENGINE_ID} shutdown complete")

# Endpoints

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start_time = time.perf_counter()
    query_text = request.query
    user_id = request.user_id

    normalized_query = normalize_query(query_text)
    engines_to_call = classify_domain(normalized_query)

    if not engines_to_call:
        # No engines matched, fallback to doctrine cache
        cached_response = await fallback_to_doctrine_cache(normalized_query)
        if cached_response:
            telemetry.record_cache_hit()
            response_hash = hash_response(cached_response)
            log_query(user_id, normalized_query, response_hash, [])
            latency_ms = (time.perf_counter() - start_time) * 1000
            telemetry.record_latency(latency_ms)
            telemetry.record_query()
            return QueryResponse(response=cached_response, sub_engine_responses={}, merged=True, cached=True)
        else:
            telemetry.record_cache_miss()
            raise HTTPException(status_code=404, detail="No relevant sub-engines found and no doctrine cache fallback available")

    # Dispatch concurrently to sub-engines
    tasks = [dispatch_to_sub_engine(engine_id, normalized_query) for engine_id in engines_to_call]
    sub_engine_responses = await asyncio.gather(*tasks)

    # Merge responses
    merged_response = merge_responses(sub_engine_responses)
    # Apply guardrails
    guarded_response = apply_guardrails(merged_response)
    # Hash response
    response_hash = hash_response(guarded_response)
    # Log query
    log_query(user_id, normalized_query, response_hash, engines_to_call)
    # Telemetry
    latency_ms = (time.perf_counter() - start_time) * 1000
    telemetry.record_latency(latency_ms)
    telemetry.record_query()

    return QueryResponse(response=guarded_response, sub_engine_responses={r.get("engine_id", "unknown"): r for r in sub_engine_responses}, merged=True, cached=False)

@app.get("/health", response_model=HealthStatus)
async def health_endpoint():
    # Self health
    self_status = "healthy"
    # Sub-engine health
    sub_health = health_monitor.get_health()
    overall_status = "healthy" if all(v["status"] == "healthy" for v in sub_health["sub_engines"].values()) else "degraded"
    details = {
        "self_status": self_status,
        "sub_engines": sub_health["sub_engines"],
        "overall_status": overall_status,
    }
    return HealthStatus(status=overall_status, details=details)

@app.get("/metrics", response_model=MetricsResponse)
async def metrics_endpoint():
    metrics = telemetry.get_metrics()
    return MetricsResponse(**metrics)

@app.get("/coverage", response_model=CoverageReport)
async def coverage_endpoint():
    doctrines = doctrine_cache.list_doctrines()
    total_doctrines = 50  # Assume total doctrines expected
    coverage_percent = (len(doctrines) / total_doctrines) * 100 if total_doctrines > 0 else 0.0
    epistemic_gaps = ["Tax Litigation", "Securities Law"]  # Example gaps
    return CoverageReport(doctrine_coverage_percent=coverage_percent, epistemic_gaps=epistemic_gaps)

@app.get("/drift", response_model=DriftReport)
async def drift_endpoint():
    # Simulate drift detection
    drift_score = random.uniform(0, 1)
    drift_detected = drift_score > 0.7
    details = {
        "last_model_update": (datetime.utcnow() - timedelta(days=30)).isoformat(),
        "drift_score": drift_score,
        "notes": "Drift detected in Contract Analysis and Regulatory Compliance sub-engines" if drift_detected else "No significant drift detected",
    }
    return DriftReport(drift_detected=drift_detected, drift_score=drift_score, details=details)

@app.get("/doctrines", response_model=DoctrinesList)
async def doctrines_endpoint():
    doctrines = doctrine_cache.list_doctrines()
    return DoctrinesList(doctrines=doctrines)

@app.get("/routing", response_model=RoutingRules)
async def routing_endpoint():
    rules = {
        "keywords_to_engines": search_index.index,
        "default_engine": "LG01",
        "fallback": "doctrine_cache",
    }
    return RoutingRules(rules=rules, engine_registry=SUB_ENGINES)

@app.get("/sub-engines", response_model=SubEnginesHealthDashboard)
async def sub_engines_endpoint():
    health_data = health_monitor.get_health()
    health_list = []
    for engine_id, status_info in health_data["sub_engines"].items():
        health_list.append(SubEngineHealth(
            sub_engine=engine_id,
            status=status_info["status"],
            last_checked=status_info["last_checked"],
            error=status_info.get("error"),
        ))
    return SubEnginesHealthDashboard(health=health_list)

@app.post("/route", response_model=RouteDryRunResponse)
async def route_dry_run_endpoint(request: RouteDryRunRequest):
    normalized_query = normalize_query(request.query)
    engines = classify_domain(normalized_query)
    return RouteDryRunResponse(engines_to_invoke=engines)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(request: AnalyzeRequest):
    normalized_query = normalize_query(request.query)
    depth = request.analysis_depth or 3
    engines = classify_domain(normalized_query)
    analysis_results = {}

    # For deep analysis, simulate multiple calls per engine with increasing detail
    for engine_id in engines:
        engine_results = []
        for level in range(1, depth + 1):
            # Simulate analysis detail increasing with level
            detail = f"Analysis level {level} for {engine_id} on query '{normalized_query}'"
            engine_results.append(detail)
            await asyncio.sleep(0.1)  # Simulate processing delay
        analysis_results[engine_id] = engine_results

    return AnalyzeResponse(analysis_results=analysis_results)

# Exception handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Run server

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ENGINE_PORT, log_level="info")