"""
BLD03 Succession Protocol Engine
=================================
BLOODLINE tier engine for succession planning, inheritance protocols,
dynasty continuity management, power transfer, and legacy preservation.

TIE-20 compliant: All 20 mandatory components implemented.
Port: 8883 | Version: 1.0.0

Architecture:
    Three-layer response: Doctrine Cache (0-200ms) -> Semantic Retrieval -> Deep Analysis
    20+ doctrine blocks covering full succession domain
    Authority-hardened with confidence stratification
    Full telemetry, drift watching, coverage mapping, audit trail
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import statistics
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ── Cloud retriever import ──────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent / "_shared"))
from cloud_retriever import CognitionCloudRetriever, CloudKnowledge

# ═══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

ENGINE_ID = "BLD03"
ENGINE_NAME = "Succession Protocol Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8883
ENGINE_TIER = "BLOODLINE"
AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"
DRIFT_REGISTRY_PATH = Path(__file__).parent / "drift_registry.json"

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "i am an ai",
    "i cannot provide",
    "as a language model",
]

# ═══════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class ResponseLayer(str, Enum):
    DOCTRINE_CACHE = "DOCTRINE_CACHE"
    SEMANTIC_RETRIEVAL = "SEMANTIC_RETRIEVAL"
    DEEP_ANALYSIS = "DEEP_ANALYSIS"


class IssueCategory(str, Enum):
    LEADERSHIP_TRANSFER = "LEADERSHIP_TRANSFER"
    INHERITANCE_PLANNING = "INHERITANCE_PLANNING"
    DYNASTY_GOVERNANCE = "DYNASTY_GOVERNANCE"
    EMERGENCY_PROTOCOLS = "EMERGENCY_PROTOCOLS"
    TRUST_SUCCESSION = "TRUST_SUCCESSION"
    CORPORATE_SUCCESSION = "CORPORATE_SUCCESSION"
    COMPETENCY_VALIDATION = "COMPETENCY_VALIDATION"
    LEGACY_PRESERVATION = "LEGACY_PRESERVATION"
    STAKEHOLDER_MANAGEMENT = "STAKEHOLDER_MANAGEMENT"
    SUCCESSION_METRICS = "SUCCESSION_METRICS"


class AuthorityLevel(str, Enum):
    SOVEREIGN = "SOVEREIGN"
    CONSTITUTIONAL = "CONSTITUTIONAL"
    STATUTORY = "STATUTORY"
    REGULATORY = "REGULATORY"
    ADVISORY = "ADVISORY"
    CUSTOMARY = "CUSTOMARY"

AUTHORITY_WEIGHTS: Dict[str, float] = {
    AuthorityLevel.SOVEREIGN: 1.0,
    AuthorityLevel.CONSTITUTIONAL: 0.95,
    AuthorityLevel.STATUTORY: 0.85,
    AuthorityLevel.REGULATORY: 0.70,
    AuthorityLevel.ADVISORY: 0.50,
    AuthorityLevel.CUSTOMARY: 0.35,
}

# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Dict[str, Any] = Field(default_factory=dict)
    force_deep: bool = False
    session_id: Optional[str] = None


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    burden_holder: str = ""
    adversary_position: str = ""
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""
    entity_scope: str = "all"
    issue_category: IssueCategory = IssueCategory.LEADERSHIP_TRANSFER


class AuthorityCitation(BaseModel):
    source: str
    level: AuthorityLevel
    weight: float
    excerpt: str = ""
    year: Optional[int] = None


class FactFragilityScore(BaseModel):
    overall_score: float = Field(ge=0.0, le=1.0)
    verifiability: float = Field(ge=0.0, le=1.0)
    recharacterization_risk: float = Field(ge=0.0, le=1.0)
    testimony_dependence: float = Field(ge=0.0, le=1.0)
    documentary_support: float = Field(ge=0.0, le=1.0)
    narrative: str = ""


class TelemetryTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    engine_id: str = ENGINE_ID
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    query_hash: str = ""
    layer_hit: ResponseLayer = ResponseLayer.DOCTRINE_CACHE
    doctrine_topic: Optional[str] = None
    latency_ms: float = 0.0
    cache_hit: bool = False
    cloud_records: int = 0
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    zone: AnalysisZone = AnalysisZone.PLANNING
    mode: ResponseMode = ResponseMode.FAST
    error_domain: Optional[str] = None


class DriftEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    doctrine_topic: str
    original_confidence: ConfidenceLevel
    new_confidence: ConfidenceLevel
    trigger_query: str = ""
    reason: str = ""


class CoverageEntry(BaseModel):
    topic: str
    hit_count: int = 0
    last_hit: Optional[str] = None
    miss_count: int = 0


class DecomposedIssue(BaseModel):
    category: IssueCategory
    sub_issues: List[str]
    doctrine_topics: List[str]
    interaction_edges: List[Tuple[str, str]] = Field(default_factory=list)
    resolution_order: List[str] = Field(default_factory=list)


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    layer_hit: ResponseLayer
    confidence: ConfidenceLevel
    conclusion: str
    reasoning: str
    key_factors: List[str] = Field(default_factory=list)
    authorities: List[AuthorityCitation] = Field(default_factory=list)
    fact_fragility: Optional[FactFragilityScore] = None
    decomposition: Optional[DecomposedIssue] = None
    cloud_knowledge_summary: str = ""
    disclosure_caveat: str = ""
    determinism_hash: str = ""
    latency_ms: float = 0.0
    telemetry: TelemetryTrace = Field(default_factory=TelemetryTrace)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    engine_version: str = ENGINE_VERSION
    engine_tier: str = ENGINE_TIER
    port: int = ENGINE_PORT
    status: str = "healthy"
    uptime_seconds: float = 0.0
    total_queries: int = 0
    doctrine_count: int = 0
    coverage_stats: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    drift_events: int = 0
    cloud_retriever_stats: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ═══════════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZATION (Component 9)
# ═══════════════════════════════════════════════════════════════════════

SUCCESSION_SYNONYMS: Dict[str, str] = {
    "heir": "successor",
    "heirs": "successors",
    "inheritor": "successor",
    "beneficiary": "successor",
    "next in line": "designated successor",
    "crown prince": "designated successor",
    "acting leader": "regent",
    "interim ceo": "regent",
    "caretaker": "regent",
    "will": "testamentary instrument",
    "last testament": "testamentary instrument",
    "estate plan": "succession plan",
    "transition plan": "succession plan",
    "power handoff": "power transfer",
    "leadership change": "power transfer",
    "handover": "power transfer",
    "dynasty": "bloodline continuity",
    "family line": "bloodline continuity",
    "lineage": "bloodline continuity",
    "family office": "dynasty governance structure",
    "family council": "dynasty governance body",
    "trust fund": "succession trust vehicle",
    "generation skipping": "multi-generational transfer",
    "gst": "multi-generational transfer",
    "board transition": "corporate succession",
    "ceo replacement": "corporate succession",
    "key man risk": "succession vulnerability",
    "bus factor": "succession vulnerability",
    "grooming": "successor development",
    "mentoring": "successor development",
    "training pipeline": "successor development program",
    "contested will": "contested succession",
    "inheritance dispute": "contested succession",
    "disinheritance": "succession exclusion",
    "competency test": "competency assessment",
    "fitness evaluation": "competency assessment",
    "emergency plan": "emergency succession protocol",
    "crisis succession": "emergency succession protocol",
    "regent": "interim authority holder",
    "conservator": "interim authority holder",
    "guardian": "interim authority holder",
    "stakeholder buy-in": "stakeholder alignment",
    "family meeting": "succession communication event",
    "legacy": "legacy preservation",
    "family values": "legacy preservation",
    "succession kpi": "succession metric",
}


def normalize_succession_terms(text: str) -> str:
    """Apply deterministic semantic normalization to succession domain terms."""
    lowered = text.lower()
    for raw, normalized in sorted(SUCCESSION_SYNONYMS.items(), key=lambda x: -len(x[0])):
        lowered = lowered.replace(raw, normalized)
    return lowered


# ═══════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE (Component 3) — 20+ Real Blocks
# ═══════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="succession_planning_fundamentals",
        keywords=["succession plan", "succession planning", "continuity", "leadership pipeline", "planning framework"],
        conclusion_template=(
            "Effective succession planning requires a multi-year, documented process that identifies critical "
            "roles, develops internal candidates, establishes selection criteria, and creates transition "
            "timelines. Plans must address both planned and unplanned departures, include communication "
            "protocols for all stakeholders, and undergo regular review cycles."
        ),
        reasoning_framework=(
            "Succession planning is not a one-time event but an ongoing strategic process. The framework "
            "must identify key positions, assess current talent, develop high-potential candidates, create "
            "individual development plans, and establish readiness metrics. The plan must consider (1) "
            "timeline for transitions, (2) depth of successor bench, (3) cross-training requirements, "
            "(4) knowledge transfer protocols, (5) stakeholder communication cadence. A robust plan "
            "addresses the entire leadership ecosystem, not just the top position."
        ),
        key_factors=[
            "Identification of critical roles requiring succession coverage",
            "Assessment of internal talent pool depth and readiness",
            "Development timelines for potential successors",
            "Knowledge transfer and institutional memory protocols",
            "Stakeholder communication and change management approach",
            "Regular plan review and adaptation cycles",
        ],
        primary_authority=[
            "Rothwell, W. (2015) Effective Succession Planning, 5th Ed.",
            "NACD Blue Ribbon Commission on Board Governance (2020)",
            "Spencer Stuart Board Index annual governance reports",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="organization leadership",
        adversary_position="Ad-hoc leadership selection without formal planning creates unnecessary risk",
        counter_arguments=[
            "Formal succession plans create political dynamics and premature power struggles",
            "Over-planning reduces organizational agility in selecting the best available leader",
        ],
        resolution_strategy="Implement structured planning while maintaining confidentiality and flexibility",
        issue_category=IssueCategory.LEADERSHIP_TRANSFER,
    ),
    DoctrineBlock(
        topic="power_transfer_protocols",
        keywords=["power transfer", "transition", "handover", "authority transfer", "leadership transition"],
        conclusion_template=(
            "Power transfer protocols must define the precise moment authority shifts, the mechanism for "
            "validating the transfer, the scope of powers transferred versus retained, and the "
            "communication chain that activates upon transfer. Ambiguity in transfer triggers is the "
            "single greatest source of succession crises."
        ),
        reasoning_framework=(
            "A power transfer protocol specifies: (1) triggering events (voluntary retirement, death, "
            "incapacity, removal for cause), (2) validation mechanism (board vote, family council "
            "ratification, trustee certification), (3) interim authority during transfer gap, (4) scope "
            "of transferred powers (full vs. limited), (5) revocation conditions, (6) documentation "
            "requirements. The protocol must be legally binding, pre-signed, and accessible to relevant "
            "parties. Consider war-gaming each trigger scenario to identify gaps."
        ),
        key_factors=[
            "Clear trigger events defined with objective criteria",
            "Validation mechanism with quorum and authentication requirements",
            "Interim authority designation during any transfer gap",
            "Scope definition: which powers transfer and which terminate",
            "Communication cascade activation sequence",
            "Legal enforceability of transfer documents",
        ],
        primary_authority=[
            "Uniform Power of Attorney Act (UPOAA)",
            "Restatement (Third) of Trusts on trustee succession",
            "Delaware General Corporation Law Sec. 141-142 on board succession",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="transferor and designated successor",
        adversary_position="Contested transfers often arise from ambiguous trigger definitions",
        counter_arguments=[
            "Rigid protocols may not account for unprecedented circumstances",
            "Pre-defined transfers can be challenged as obtained under duress",
        ],
        resolution_strategy="Define triggers with objective standards while including a dispute resolution fallback",
        issue_category=IssueCategory.LEADERSHIP_TRANSFER,
    ),
    DoctrineBlock(
        topic="dynasty_continuity",
        keywords=["dynasty", "bloodline", "continuity", "multi-generational", "family legacy", "generational"],
        conclusion_template=(
            "Dynasty continuity requires structures that outlast any individual: irrevocable trusts, "
            "family constitutions, governance bodies with rotating membership, endowment models, and "
            "cultural transmission mechanisms. The goal is to create self-sustaining systems that "
            "preserve values, wealth, and influence across generations."
        ),
        reasoning_framework=(
            "Multi-generational continuity analysis examines: (1) wealth preservation vehicles (dynasty "
            "trusts, family LLCs, private foundations), (2) governance structures (family councils, "
            "constitutions, advisory boards), (3) cultural transmission (family history documentation, "
            "mentorship programs, gathering rituals), (4) conflict resolution (mediation clauses, "
            "buyout mechanisms, family courts), (5) external threat mitigation (prenuptial requirements, "
            "in-law integration protocols, asset protection). The greatest risk to dynasty continuity "
            "is generational disconnection from founding values."
        ),
        key_factors=[
            "Wealth preservation vehicles spanning multiple generations",
            "Governance structures with built-in renewal mechanisms",
            "Cultural transmission and value alignment programs",
            "Conflict resolution mechanisms preventing family fracture",
            "External threat mitigation including marital and creditor protection",
            "Succession of governance roles themselves (who governs the governors)",
        ],
        primary_authority=[
            "Hughes, J. (2004) Family Wealth: Keeping It in the Family",
            "Uniform Trust Code on dynasty trust provisions",
            "GST tax provisions (IRC Sec. 2601-2663)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="founding generation and governance body",
        adversary_position="Perpetual dynasty structures concentrate wealth and reduce social mobility",
        counter_arguments=[
            "Dynasty trusts face rule against perpetuities in some jurisdictions",
            "Multi-generational governance becomes unwieldy as family branches multiply",
        ],
        resolution_strategy="Use jurisdiction-specific trust vehicles with built-in governance evolution",
        issue_category=IssueCategory.DYNASTY_GOVERNANCE,
    ),
    DoctrineBlock(
        topic="heir_validation",
        keywords=["heir", "validate", "verification", "legitimacy", "successor qualification", "heir apparent"],
        conclusion_template=(
            "Heir validation requires objective criteria documented in advance: competency benchmarks, "
            "loyalty demonstrations, educational or experiential thresholds, and formal ratification "
            "by the governing body. Validation must be transparent to prevent challenges while "
            "maintaining the authority to disqualify unfit candidates."
        ),
        reasoning_framework=(
            "Heir validation involves: (1) baseline eligibility (bloodline, adoption, marriage), "
            "(2) competency thresholds (education, work experience, demonstrated judgment), (3) loyalty "
            "and alignment assessment (values, commitment, family participation), (4) developmental "
            "milestones (apprenticeship completion, mentorship benchmarks), (5) ratification process "
            "(governance body vote, elder approval, stakeholder input), (6) challenge and appeal "
            "mechanism for rejected candidates. The process must balance meritocracy with bloodline "
            "loyalty while remaining defensible against legal challenge."
        ),
        key_factors=[
            "Objective eligibility criteria documented in governing instruments",
            "Competency benchmarks with measurable outcomes",
            "Loyalty and alignment assessment methodology",
            "Formal ratification process with quorum requirements",
            "Appeal mechanism for disqualified candidates",
            "Protection against undue influence in validation process",
        ],
        primary_authority=[
            "Uniform Probate Code Sec. 2-101 through 2-114 on heirship",
            "Corporate governance best practices for CEO selection",
            "Trust instrument provisions on beneficiary qualification",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="validating authority",
        adversary_position="Subjective criteria allow manipulation of heir selection",
        counter_arguments=[
            "Overly rigid criteria may exclude the most capable successor",
            "Validation processes create family political dynamics",
        ],
        resolution_strategy="Combine objective thresholds with governance body discretion within documented bounds",
        issue_category=IssueCategory.COMPETENCY_VALIDATION,
    ),
    DoctrineBlock(
        topic="competency_assessment",
        keywords=["competency", "assessment", "fitness", "evaluation", "capability", "readiness"],
        conclusion_template=(
            "Competency assessment for succession requires multi-dimensional evaluation: cognitive "
            "ability, domain expertise, emotional intelligence, ethical judgment, and stress performance. "
            "Assessments must be conducted by independent evaluators using validated instruments "
            "with clear scoring rubrics and documented results."
        ),
        reasoning_framework=(
            "A defensible competency assessment framework includes: (1) cognitive and intellectual "
            "capacity (strategic thinking, analytical reasoning, learning agility), (2) domain "
            "expertise (industry knowledge, operational experience, financial literacy), (3) emotional "
            "intelligence (self-awareness, empathy, relationship management), (4) ethical judgment "
            "(integrity testing, scenario-based ethical dilemma evaluation), (5) stress and crisis "
            "performance (simulated crisis scenarios, historical performance under pressure), "
            "(6) leadership capability (team building, vision articulation, decision-making speed). "
            "Independent evaluators prevent bias. Longitudinal assessment over 2+ years is more "
            "reliable than single-point evaluation."
        ),
        key_factors=[
            "Multi-dimensional evaluation covering cognitive, emotional, and ethical domains",
            "Independent evaluators free from succession politics",
            "Validated assessment instruments with published reliability",
            "Longitudinal observation over multiple years",
            "Simulated crisis and pressure scenario testing",
            "Clear scoring rubrics with pass/fail thresholds",
        ],
        primary_authority=[
            "Center for Creative Leadership succession assessment framework",
            "Hogan Assessment Systems for executive evaluation",
            "APA Standards for Educational and Psychological Testing",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="assessment authority or governance body",
        adversary_position="Standardized assessments cannot capture the full complexity of leadership fitness",
        counter_arguments=[
            "Assessment results can be manipulated by coaching candidates to the test",
            "Cultural bias in assessment instruments may unfairly exclude qualified candidates",
        ],
        resolution_strategy="Use multiple validated instruments with cultural calibration over extended observation period",
        issue_category=IssueCategory.COMPETENCY_VALIDATION,
    ),
    DoctrineBlock(
        topic="emergency_succession",
        keywords=["emergency", "crisis", "sudden death", "incapacity", "immediate succession", "emergency protocol"],
        conclusion_template=(
            "Emergency succession protocols must activate automatically upon triggering events without "
            "requiring action by the incapacitated principal. Pre-signed documents, sealed succession "
            "envelopes, and automatic authority delegation chains are essential. The protocol must "
            "function even when communication channels are disrupted."
        ),
        reasoning_framework=(
            "Emergency succession addresses: (1) sudden death or total incapacity, (2) communication "
            "blackout scenarios, (3) simultaneous incapacity of multiple leaders, (4) time-critical "
            "decisions that cannot await formal succession, (5) temporary vs. permanent emergency "
            "authority. Required elements: pre-signed authority transfer documents held by trusted "
            "third party, sealed succession envelopes with chain-of-command instructions, automatic "
            "delegation triggers tied to absence duration thresholds, emergency communication "
            "cascade reaching at least three independent contacts, standing authority for interim "
            "leader to make binding decisions within defined scope."
        ),
        key_factors=[
            "Automatic activation without incapacitated party action",
            "Pre-signed documents held by independent custodian",
            "Sealed succession envelope protocol with multiple copies",
            "Absence duration thresholds triggering escalating authority",
            "Simultaneous incapacity (e.g., common disaster) protocols",
            "Temporary vs. permanent emergency authority scope limits",
        ],
        primary_authority=[
            "Uniform Durable Power of Attorney Act",
            "Presidential Succession Act of 1947 (analogy for organizational design)",
            "25th Amendment framework adapted for corporate use",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and custodian of succession documents",
        adversary_position="Emergency protocols can be exploited to seize power prematurely",
        counter_arguments=[
            "Automatic triggers may fire inappropriately during temporary unavailability",
            "Sealed envelopes create security risks if custody is compromised",
        ],
        resolution_strategy="Implement multi-factor trigger verification with rapid reversal mechanism",
        issue_category=IssueCategory.EMERGENCY_PROTOCOLS,
    ),
    DoctrineBlock(
        topic="regent_designation",
        keywords=["regent", "interim", "caretaker", "temporary authority", "acting", "stewardship"],
        conclusion_template=(
            "Regent designation establishes interim authority with explicitly limited scope, defined "
            "duration, accountability requirements, and automatic termination conditions. The regent "
            "must be bound by a stewardship duty that prohibits self-dealing and requires preservation "
            "of the principal's position for the permanent successor."
        ),
        reasoning_framework=(
            "Regent governance framework: (1) selection criteria (trusted advisor, senior family member, "
            "independent professional), (2) scope limitations (which powers the regent may exercise, "
            "which require governance body approval), (3) duration caps (maximum regency period before "
            "permanent succession must be resolved), (4) accountability mechanisms (regular reporting, "
            "financial audits, governance body oversight), (5) prohibited actions (asset sales above "
            "threshold, organizational restructuring, successor displacement), (6) compensation and "
            "indemnification, (7) termination triggers (permanent successor ready, regent breach, "
            "duration expiry)."
        ),
        key_factors=[
            "Explicit scope limitations on regent authority",
            "Maximum duration with mandatory review checkpoints",
            "Stewardship duty with prohibition on self-dealing",
            "Regular accountability reporting to governance body",
            "Prohibited action categories requiring full governance approval",
            "Termination triggers and handover protocol to permanent successor",
        ],
        primary_authority=[
            "Restatement (Third) of Trusts on trustee powers and duties",
            "Uniform Trust Code Sec. 801-817 on trustee administration",
            "Corporate bylaws models for interim CEO appointment",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="regent and oversight body",
        adversary_position="Regents accumulate power and resist transferring to the rightful successor",
        counter_arguments=[
            "Overly restrictive regent powers may prevent necessary crisis decisions",
            "Regent selection itself can become a contested power struggle",
        ],
        resolution_strategy="Pre-designate regent with clear scope document and automatic termination at defined milestone",
        issue_category=IssueCategory.EMERGENCY_PROTOCOLS,
    ),
    DoctrineBlock(
        topic="trust_succession",
        keywords=["trust", "trustee succession", "successor trustee", "trust continuity", "fiduciary succession"],
        conclusion_template=(
            "Trust succession must address trustee replacement, beneficiary generation transitions, "
            "trust protector succession, and trust purpose evolution. The trust instrument should "
            "contain a trustee succession ladder at least three deep, with institutional trustee "
            "as backstop, and trust protector authority to modify terms for changed circumstances."
        ),
        reasoning_framework=(
            "Trust succession planning covers: (1) trustee succession ladder (named individual "
            "successors, institutional backstop, court appointment as last resort), (2) trust "
            "protector succession (who appoints new protectors, scope of protector powers), "
            "(3) beneficiary class transitions (generational shifts, class closing rules, "
            "per stirpes vs. per capita distribution), (4) purpose evolution (trust modification "
            "power, cy pres doctrine applicability, decanting authority), (5) jurisdiction "
            "considerations (trust migration, governing law selection, situs change authority)."
        ),
        key_factors=[
            "Trustee succession ladder at least three named successors deep",
            "Institutional trustee as automatic backstop",
            "Trust protector with power to modify administrative terms",
            "Beneficiary class rules for generational transitions",
            "Trust purpose evolution mechanisms for changed circumstances",
            "Jurisdiction selection and migration authority",
        ],
        primary_authority=[
            "Uniform Trust Code Sec. 704 on trustee vacancy",
            "Restatement (Third) of Trusts Sec. 34-37",
            "IRC Sec. 2601-2663 (GST) for multi-generational trust tax",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="settlor or trust protector",
        adversary_position="Complex trust succession provisions create litigation vectors for disgruntled beneficiaries",
        counter_arguments=[
            "Over-specified trustee succession may lock in unqualified individuals",
            "Trust protector power can be used to override settlor intent",
        ],
        resolution_strategy="Layer individual trustees with institutional backstop and protector oversight",
        issue_category=IssueCategory.TRUST_SUCCESSION,
    ),
    DoctrineBlock(
        topic="corporate_succession",
        keywords=["corporate", "board", "ceo succession", "c-suite", "executive succession", "board succession"],
        conclusion_template=(
            "Corporate succession planning requires board-level oversight with a dedicated committee, "
            "annual CEO succession review, emergency CEO succession plan, independent director succession "
            "pipeline, and integration with strategic planning to ensure leadership continuity "
            "supports long-term business direction."
        ),
        reasoning_framework=(
            "Corporate succession framework: (1) board succession committee with independent chair, "
            "(2) annual CEO succession review including internal candidate assessment, (3) emergency "
            "CEO succession protocol with pre-authorized interim appointment, (4) C-suite pipeline "
            "development with rotation and stretch assignments, (5) board refreshment with staggered "
            "terms and skill matrix alignment, (6) succession integration with strategic plan "
            "(future leader profile derived from strategic direction), (7) external candidate "
            "monitoring and relationship building, (8) disclosure obligations under SEC rules."
        ),
        key_factors=[
            "Board succession committee with independent oversight",
            "Annual CEO succession review with documented outcomes",
            "Emergency CEO succession plan tested annually",
            "Internal candidate development pipeline with mentorship",
            "Board refreshment aligned with evolving skill requirements",
            "SEC disclosure compliance for material succession events",
        ],
        primary_authority=[
            "NYSE Listed Company Manual Sec. 303A.09 on CEO succession",
            "SEC Regulation S-K Item 407 on board governance disclosure",
            "NACD Report on CEO Succession Practices (2022)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="board of directors and governance committee",
        adversary_position="Imperial CEO who controls own succession undermines board independence",
        counter_arguments=[
            "External succession may be needed when internal pipeline is weak",
            "Public disclosure of succession planning can create market uncertainty",
        ],
        resolution_strategy="Board-controlled process with annual independent review and emergency protocol",
        issue_category=IssueCategory.CORPORATE_SUCCESSION,
    ),
    DoctrineBlock(
        topic="family_governance",
        keywords=["family governance", "family constitution", "family council", "family charter", "family assembly"],
        conclusion_template=(
            "Family governance structures formalize decision-making, conflict resolution, and succession "
            "within dynastic families. A family constitution, elected council, defined meeting cadence, "
            "and binding arbitration clauses create the institutional framework for multi-generational "
            "governance that survives individual family member transitions."
        ),
        reasoning_framework=(
            "Family governance architecture: (1) family constitution defining values, mission, membership "
            "criteria, and amendment process, (2) family council with elected representatives from each "
            "branch, (3) family assembly (all members) meeting annually, (4) specialized committees "
            "(investment, philanthropy, succession, education), (5) family office as administrative arm, "
            "(6) conflict resolution mechanism (mediation then binding arbitration), (7) membership "
            "rules (birth, marriage, adoption, divorce, expulsion), (8) voting rights allocation "
            "(per capita, per stirpes, branch-weighted)."
        ),
        key_factors=[
            "Written family constitution with formal amendment process",
            "Elected family council representing all branches",
            "Regular family assembly meetings for transparency",
            "Specialized committees for investment, succession, and philanthropy",
            "Binding conflict resolution mechanism preventing litigation",
            "Clear membership and voting rights allocation rules",
        ],
        primary_authority=[
            "Family Firm Institute governance framework",
            "Lansberg, I. (1999) Succeeding Generations on family governance",
            "IFC Family Business Governance Handbook (2011)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="founding generation and family council",
        adversary_position="Informal family decision-making works fine without bureaucratic structures",
        counter_arguments=[
            "Governance structures can become tools of control by dominant branch",
            "Younger generations may reject inherited governance frameworks",
        ],
        resolution_strategy="Build governance with evolution mechanisms and mandatory periodic constitutional review",
        issue_category=IssueCategory.DYNASTY_GOVERNANCE,
    ),
    DoctrineBlock(
        topic="succession_timeline",
        keywords=["timeline", "transition period", "handover schedule", "succession phasing", "transition calendar"],
        conclusion_template=(
            "Succession timelines must define preparation, transition, and consolidation phases. "
            "A minimum 12-month overlap period for planned successions allows knowledge transfer, "
            "relationship transition, and authority calibration. Critical milestones must be documented "
            "with go/no-go decision points at each phase gate."
        ),
        reasoning_framework=(
            "Succession timeline framework: Phase 1 - Preparation (6-24 months): identify successor, "
            "begin development program, announce internally. Phase 2 - Transition (6-12 months): "
            "parallel leadership, gradual authority transfer, stakeholder introduction. Phase 3 - "
            "Consolidation (3-6 months): full authority to successor, predecessor available for "
            "consultation, performance monitoring. Each phase has go/no-go gates where the governance "
            "body assesses readiness before advancing. Accelerated timeline for emergency succession "
            "compresses to days-to-weeks with post-hoc consolidation."
        ),
        key_factors=[
            "Three-phase framework: preparation, transition, consolidation",
            "Minimum overlap period for knowledge transfer",
            "Phase gate reviews with documented go/no-go decisions",
            "Accelerated timeline protocol for emergency succession",
            "Stakeholder communication milestones at each phase",
            "Predecessor role definition during and after transition",
        ],
        primary_authority=[
            "Harvard Business Review succession transition research (Ciampa & Watkins)",
            "McKinsey CEO Transition Best Practices",
            "Spencer Stuart CEO Succession Planning framework",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and transition steering committee",
        adversary_position="Extended timelines create uncertainty and power struggles",
        counter_arguments=["Short timelines may not allow adequate knowledge transfer"],
        resolution_strategy="Customize timeline length to context with mandatory minimum milestones",
        issue_category=IssueCategory.LEADERSHIP_TRANSFER,
    ),
    DoctrineBlock(
        topic="parallel_succession_tracks",
        keywords=["parallel tracks", "dual succession", "backup plan", "concurrent candidates", "succession pipeline"],
        conclusion_template=(
            "Parallel succession tracks develop multiple candidates simultaneously, creating competitive "
            "tension that improves readiness while providing backup options. Track design must balance "
            "candidate motivation against destructive competition and manage the eventual transition "
            "of non-selected candidates."
        ),
        reasoning_framework=(
            "Parallel track architecture: (1) identify 2-4 candidates per critical role, (2) assign "
            "differentiated development experiences (P&L ownership, geographic rotation, functional "
            "breadth), (3) assess independently against common criteria, (4) manage candidate expectations "
            "transparently about competitive process, (5) plan for non-selected candidates (retention "
            "package, alternative role, graceful exit), (6) avoid public horse race that destabilizes "
            "organization. The optimal parallel track window is 2-3 years before succession decision."
        ),
        key_factors=[
            "2-4 candidates developed per critical role",
            "Differentiated developmental assignments for each track",
            "Common assessment criteria applied independently",
            "Non-selected candidate retention or transition planning",
            "Organizational stability during competitive development",
            "Confidentiality management to prevent political coalitions",
        ],
        primary_authority=[
            "GE/Honeywell CEO succession model (multiple internal candidates)",
            "Charan, R. (2005) The Leadership Pipeline",
            "Corporate Leadership Council succession pipeline research",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="board succession committee",
        adversary_position="Parallel tracks create destructive internal competition",
        counter_arguments=["Single-track succession concentrates risk on one candidate"],
        resolution_strategy="Structured competitive development with clear decision criteria and retention plans",
        issue_category=IssueCategory.LEADERSHIP_TRANSFER,
    ),
    DoctrineBlock(
        topic="contested_succession",
        keywords=["contested", "dispute", "challenge", "rival claim", "succession conflict", "inheritance dispute"],
        conclusion_template=(
            "Contested successions must be resolved through pre-established dispute resolution mechanisms "
            "before they fracture the organization or family. Binding arbitration clauses in governing "
            "instruments, independent mediators, and clear evidentiary standards for validating claims "
            "are essential. Litigation should be the absolute last resort."
        ),
        reasoning_framework=(
            "Contest resolution framework: (1) identify the basis of contest (procedural defect, "
            "competency challenge, legitimacy dispute, undue influence claim), (2) apply the governing "
            "instrument's dispute resolution clause, (3) appoint independent mediator with domain "
            "expertise, (4) if mediation fails, proceed to binding arbitration per instrument terms, "
            "(5) preserve organizational/family operations during dispute via interim governance, "
            "(6) document all proceedings for potential judicial review, (7) implement outcome with "
            "reconciliation protocol for losing party."
        ),
        key_factors=[
            "Pre-established dispute resolution mechanisms in governing instruments",
            "Independent mediator appointment before escalation",
            "Binding arbitration as alternative to destructive litigation",
            "Interim governance during dispute resolution period",
            "Evidentiary standards for succession claims",
            "Reconciliation protocol for post-dispute family/organizational healing",
        ],
        primary_authority=[
            "Uniform Probate Code will contest provisions (Sec. 3-401 to 3-412)",
            "American Arbitration Association family business dispute rules",
            "Restatement (Third) of Property: Wills and Other Donative Transfers",
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        burden_holder="contestant bears burden of proof",
        adversary_position="Succession instruments were executed under undue influence or lack capacity",
        counter_arguments=[
            "Binding arbitration clauses may not be enforceable in all jurisdictions",
            "In terrorem (no-contest) clauses may be struck down as against public policy",
        ],
        resolution_strategy="Layer mediation, arbitration, and in terrorem clauses for maximum dispute deterrence",
        issue_category=IssueCategory.DYNASTY_GOVERNANCE,
    ),
    DoctrineBlock(
        topic="succession_documentation",
        keywords=["documentation", "records", "succession binder", "governance records", "succession artifacts"],
        conclusion_template=(
            "Succession documentation must include the succession plan itself, authority delegation "
            "instruments, competency assessments, training records, communication protocols, and "
            "emergency activation procedures. All documents require version control, authorized "
            "signatories, secure storage with redundant access, and scheduled review dates."
        ),
        reasoning_framework=(
            "Documentation requirements: (1) master succession plan document with roles, timelines, "
            "and triggers, (2) authority delegation instruments (powers of attorney, board resolutions, "
            "trust amendments), (3) candidate assessment portfolios with scoring matrices, (4) training "
            "and development records for each successor candidate, (5) communication plan templates "
            "for each succession scenario, (6) emergency succession packet (sealed envelope, digital "
            "vault access, contact cascades), (7) version control with change log and authorized "
            "reviewer sign-off, (8) secure storage in minimum two independent locations."
        ),
        key_factors=[
            "Master succession plan with complete scenario coverage",
            "Legal instruments with current signatures and notarization",
            "Candidate assessment documentation with scoring rubrics",
            "Version control and change management log",
            "Secure redundant storage in minimum two locations",
            "Scheduled review dates with designated reviewer accountability",
        ],
        primary_authority=[
            "ISO 30409:2016 Human Resource Management — Workforce planning",
            "SOX Section 302/906 on internal controls and officer certification",
            "NIST 800-53 contingency planning controls (CP-2, CP-6, CP-7)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and plan administrator",
        adversary_position="Documentation creates discoverable evidence in succession disputes",
        counter_arguments=["Over-documentation creates bureaucratic overhead"],
        resolution_strategy="Maintain essential documentation with privilege protections where applicable",
        issue_category=IssueCategory.LEADERSHIP_TRANSFER,
    ),
    DoctrineBlock(
        topic="succession_training",
        keywords=["training", "development", "mentorship", "grooming", "preparation", "successor development"],
        conclusion_template=(
            "Successor development programs must include operational immersion, strategic exposure, "
            "external network building, crisis simulation, and values alignment mentorship. The program "
            "should span 3-5 years for senior leadership roles with progressive responsibility "
            "increases and regular readiness assessment checkpoints."
        ),
        reasoning_framework=(
            "Development program architecture: (1) operational rotation through all critical functions, "
            "(2) strategic decision participation in board or leadership forums, (3) external network "
            "development (industry associations, customer relationships, advisor relationships), "
            "(4) crisis simulation exercises with post-mortem learning, (5) values and culture "
            "mentorship from outgoing leader and elders, (6) personal leadership development (executive "
            "coaching, 360-degree feedback, peer learning), (7) progressive responsibility increases "
            "with defined authority milestones, (8) regular readiness assessment against succession "
            "criteria matrix."
        ),
        key_factors=[
            "Multi-year development timeline with progressive responsibility",
            "Cross-functional operational rotation",
            "Strategic decision-making exposure and participation",
            "External network and relationship development",
            "Crisis simulation and pressure testing",
            "Values alignment mentorship from founding generation",
        ],
        primary_authority=[
            "Charan, R., Drotter, S., Noel, J. (2011) The Leadership Pipeline",
            "Center for Creative Leadership development assessment research",
            "Deloitte Global Human Capital Trends on succession development",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="successor candidate and mentoring authority",
        adversary_position="Designated successors develop entitlement mindset rather than earned competence",
        counter_arguments=["Structured programs may produce conformist rather than innovative leaders"],
        resolution_strategy="Combine structured development with external challenge assignments and independent assessment",
        issue_category=IssueCategory.COMPETENCY_VALIDATION,
    ),
    DoctrineBlock(
        topic="legacy_preservation",
        keywords=["legacy", "preservation", "heritage", "values", "founding vision", "institutional memory"],
        conclusion_template=(
            "Legacy preservation requires codification of founding values, documentation of institutional "
            "knowledge, creation of cultural artifacts, and establishment of review mechanisms that "
            "allow values evolution without values abandonment. The legacy must be a living guide, "
            "not a museum piece."
        ),
        reasoning_framework=(
            "Legacy preservation framework: (1) founding values codification in constitution or charter, "
            "(2) institutional history documentation (oral histories, decision archives, milestone records), "
            "(3) cultural artifact creation (family/organizational narratives, ritual preservation, "
            "symbolic assets), (4) mentorship programs transmitting tacit knowledge, (5) values alignment "
            "assessment for all succession candidates, (6) periodic values review allowing principled "
            "evolution while maintaining core identity, (7) external legacy (philanthropy, community "
            "engagement, public reputation management)."
        ),
        key_factors=[
            "Codified founding values in governing documents",
            "Institutional history and oral tradition documentation",
            "Cultural transmission through mentorship and ritual",
            "Values alignment integrated into succession criteria",
            "Periodic review allowing principled evolution",
            "External legacy through philanthropy and reputation",
        ],
        primary_authority=[
            "Collins, J. (2001) Good to Great on enduring institutional values",
            "Family Enterprise Consulting Group on legacy preservation",
            "Schein, E. (2010) Organizational Culture and Leadership",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and legacy committee",
        adversary_position="Rigid legacy preservation stifles innovation and adaptation",
        counter_arguments=["Values naturally evolve and forced preservation creates hypocrisy"],
        resolution_strategy="Distinguish immutable core values from adaptive practices, allow evolution of the latter",
        issue_category=IssueCategory.LEGACY_PRESERVATION,
    ),
    DoctrineBlock(
        topic="succession_communication",
        keywords=["communication", "announcement", "disclosure", "stakeholder notification", "messaging"],
        conclusion_template=(
            "Succession communication must be choreographed with precise timing, tailored messaging "
            "for each stakeholder group, consistent narrative across channels, and prepared responses "
            "for anticipated challenges. Premature or botched communication is the most common "
            "cause of succession plan derailment."
        ),
        reasoning_framework=(
            "Communication protocol: (1) identify all stakeholder groups (family, board, management, "
            "employees, customers, investors, regulators, media), (2) develop tailored messaging per "
            "group addressing their specific concerns, (3) establish communication sequence (inside-out: "
            "inner circle first, expanding outward), (4) prepare Q&A document for each stakeholder "
            "group, (5) designate spokesperson(s) with media training, (6) monitor reaction and "
            "prepare second-wave messaging, (7) embed succession narrative in ongoing organizational "
            "communication."
        ),
        key_factors=[
            "Stakeholder-specific messaging addressing unique concerns",
            "Communication sequence from inner circle outward",
            "Prepared Q&A for anticipated challenges per stakeholder",
            "Designated trained spokesperson(s)",
            "Reaction monitoring and second-wave messaging readiness",
            "Consistent core narrative across all channels",
        ],
        primary_authority=[
            "SEC Regulation FD on fair disclosure of material events",
            "Crisis Communication Institute succession communication framework",
            "McKinsey CEO succession communication best practices",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and communications team",
        adversary_position="Controlled succession messaging is manipulative and withholds material information",
        counter_arguments=["Delayed communication breeds rumors and uncertainty"],
        resolution_strategy="Timely, transparent communication with sequencing to ensure message control",
        issue_category=IssueCategory.STAKEHOLDER_MANAGEMENT,
    ),
    DoctrineBlock(
        topic="stakeholder_management",
        keywords=["stakeholder", "buy-in", "alignment", "resistance", "constituency management", "support building"],
        conclusion_template=(
            "Stakeholder management during succession requires mapping influence networks, identifying "
            "potential resistance sources, building coalitions of support, addressing concerns proactively, "
            "and creating incentive alignment between stakeholder interests and succession outcomes."
        ),
        reasoning_framework=(
            "Stakeholder management framework: (1) stakeholder mapping (influence, interest, position "
            "on succession), (2) resistance analysis (who opposes, why, what would change their mind), "
            "(3) coalition building (identify champions, give them role in transition), (4) incentive "
            "alignment (retention packages, role clarity, opportunity in new regime), (5) concern "
            "addressing (direct meetings, written commitments, transition guarantees), (6) monitoring "
            "sentiment through transition with feedback loops, (7) post-succession stakeholder "
            "re-engagement and relationship renewal."
        ),
        key_factors=[
            "Stakeholder influence and interest mapping",
            "Resistance source identification and mitigation planning",
            "Coalition building with identified succession champions",
            "Incentive alignment between stakeholder and succession interests",
            "Direct concern-addressing through meetings and commitments",
            "Post-succession relationship re-engagement protocols",
        ],
        primary_authority=[
            "Freeman, R.E. (2010) Strategic Management: A Stakeholder Approach",
            "NACD stakeholder engagement in CEO transitions report",
            "Kotter, J. (2012) Leading Change on coalition building",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="transition steering committee",
        adversary_position="Stakeholder management is manipulation designed to suppress legitimate opposition",
        counter_arguments=["Broad stakeholder engagement slows succession and creates veto points"],
        resolution_strategy="Proactive engagement with key stakeholders while maintaining governance body decision authority",
        issue_category=IssueCategory.STAKEHOLDER_MANAGEMENT,
    ),
    DoctrineBlock(
        topic="succession_metrics",
        keywords=["metrics", "kpi", "measurement", "succession scorecard", "readiness index", "pipeline strength"],
        conclusion_template=(
            "Succession effectiveness requires measurable KPIs: successor readiness index, pipeline "
            "depth ratio, time-to-fill for critical roles, retention rate of high-potentials, "
            "succession plan coverage percentage, and transition success rate. Metrics must be "
            "tracked longitudinally and reported to governance body quarterly."
        ),
        reasoning_framework=(
            "Succession metrics framework: (1) pipeline depth ratio (ready-now candidates per critical "
            "role, target >= 2.0), (2) successor readiness index (percentage of development plan "
            "completed by each candidate), (3) plan coverage (percentage of critical roles with "
            "documented succession plan), (4) time-to-fill (days from vacancy to successor in role), "
            "(5) high-potential retention rate (percentage of pipeline candidates retained year-over-year), "
            "(6) transition success rate (percentage of successions where successor remains in role "
            ">24 months), (7) diversity of pipeline, (8) development investment per successor candidate."
        ),
        key_factors=[
            "Pipeline depth ratio >= 2.0 for all critical roles",
            "Successor readiness index tracked per candidate",
            "Plan coverage percentage across all critical roles",
            "Time-to-fill benchmarked against industry standards",
            "High-potential retention rate as leading indicator",
            "Transition success rate measured at 24-month mark",
        ],
        primary_authority=[
            "SHRM Succession Planning Metrics Guide",
            "Bersin by Deloitte talent management benchmarking",
            "Corporate Leadership Council succession metrics research",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="HR leadership and governance body",
        adversary_position="Reducing succession to metrics loses the qualitative judgment required",
        counter_arguments=["Metrics create gaming behavior where candidates optimize for measurement not readiness"],
        resolution_strategy="Combine quantitative metrics with qualitative governance body assessment",
        issue_category=IssueCategory.SUCCESSION_METRICS,
    ),
    DoctrineBlock(
        topic="succession_review",
        keywords=["review", "audit", "assessment", "plan review", "annual review", "succession audit"],
        conclusion_template=(
            "Succession plans require formal annual review, triggered review upon material changes, "
            "and independent audit every 3-5 years. Reviews must assess plan currency, candidate "
            "readiness, environmental changes, and gap identification. Stale succession plans "
            "are worse than no plans because they create false confidence."
        ),
        reasoning_framework=(
            "Review protocol: (1) annual internal review by governance body covering plan currency, "
            "candidate status, and environmental changes, (2) triggered review upon material events "
            "(candidate departure, organizational restructuring, market shifts, health changes), "
            "(3) independent external audit every 3-5 years assessing plan quality against best "
            "practices, (4) tabletop exercise testing emergency succession activation, (5) gap "
            "analysis identifying uncovered roles and development deficiencies, (6) action plan "
            "generation with accountable owners and deadlines for each gap."
        ),
        key_factors=[
            "Annual formal review by governance body",
            "Triggered review upon material change events",
            "Independent external audit every 3-5 years",
            "Tabletop exercise of emergency succession activation",
            "Gap analysis with action plan and accountable owners",
            "Review documentation as part of succession record",
        ],
        primary_authority=[
            "NYSE Corporate Governance Standards on annual board evaluation",
            "COSO Internal Control Framework on monitoring activities",
            "ISO 31000 Risk Management on periodic risk review",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="governance body and plan administrator",
        adversary_position="Reviews become perfunctory check-the-box exercises without real impact",
        counter_arguments=["Frequent reviews consume leadership time with diminishing returns"],
        resolution_strategy="Differentiate between light-touch annual reviews and deep periodic audits",
        issue_category=IssueCategory.SUCCESSION_METRICS,
    ),
]

# Build keyword index for fast cache lookup
_KEYWORD_INDEX: Dict[str, List[int]] = defaultdict(list)
for _idx, _block in enumerate(DOCTRINE_CACHE):
    for _kw in _block.keywords:
        _KEYWORD_INDEX[_kw.lower()].append(_idx)


def search_doctrine_cache(query: str, top_k: int = 3) -> List[DoctrineBlock]:
    """Search doctrine cache by keyword matching. Returns top-k matches ranked by hit count."""
    normalized = normalize_succession_terms(query)
    tokens = set(normalized.lower().split())
    scores: Dict[int, int] = defaultdict(int)
    for token in tokens:
        for kw, indices in _KEYWORD_INDEX.items():
            if token in kw or kw in token:
                for idx in indices:
                    scores[idx] += 1
    if not scores:
        for idx, block in enumerate(DOCTRINE_CACHE):
            if any(t in block.topic.lower() for t in tokens):
                scores[idx] += 1
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [DOCTRINE_CACHE[idx] for idx, _ in ranked[:top_k]]


# ═══════════════════════════════════════════════════════════════════════
# AUTHORITY HARDENING (Component 7)
# ═══════════════════════════════════════════════════════════════════════

def harden_authorities(authorities: List[str]) -> List[AuthorityCitation]:
    """Convert raw authority strings into weighted, hierarchical citations."""
    citations: List[AuthorityCitation] = []
    for auth in authorities:
        auth_lower = auth.lower()
        if any(w in auth_lower for w in ["constitution", "sovereign", "fundamental"]):
            level = AuthorityLevel.CONSTITUTIONAL
        elif any(w in auth_lower for w in ["upc", "utc", "irc", "sec.", "act ", "code"]):
            level = AuthorityLevel.STATUTORY
        elif any(w in auth_lower for w in ["regulation", "rule", "standard", "iso", "nist"]):
            level = AuthorityLevel.REGULATORY
        elif any(w in auth_lower for w in ["restatement", "report", "guide", "framework"]):
            level = AuthorityLevel.ADVISORY
        else:
            level = AuthorityLevel.CUSTOMARY
        citations.append(AuthorityCitation(
            source=auth,
            level=level,
            weight=AUTHORITY_WEIGHTS.get(level, 0.35),
            excerpt="",
        ))
    citations.sort(key=lambda c: -c.weight)
    return citations


def resolve_authority_conflicts(citations: List[AuthorityCitation]) -> List[AuthorityCitation]:
    """When authorities conflict, higher-weight authorities prevail."""
    if len(citations) <= 1:
        return citations
    seen_levels: Set[str] = set()
    resolved: List[AuthorityCitation] = []
    for c in sorted(citations, key=lambda x: -x.weight):
        if c.level not in seen_levels:
            resolved.append(c)
            seen_levels.add(c.level)
        elif c.weight >= 0.70:
            resolved.append(c)
    return resolved


# ═══════════════════════════════════════════════════════════════════════
# CONFIDENCE STRATIFICATION (Component 8)
# ═══════════════════════════════════════════════════════════════════════

def stratify_confidence(
    doctrine_match_count: int,
    authority_weight_avg: float,
    cloud_records: int,
    zone: AnalysisZone,
) -> ConfidenceLevel:
    """Determine confidence level based on evidence strength and analysis zone."""
    if zone == AnalysisZone.AUDIT:
        if doctrine_match_count >= 2 and authority_weight_avg >= 0.80:
            return ConfidenceLevel.DEFENSIBLE
        return ConfidenceLevel.DISCLOSURE
    score = (doctrine_match_count * 0.3) + (authority_weight_avg * 0.4) + (min(cloud_records, 10) * 0.03)
    if score >= 0.9:
        return ConfidenceLevel.DEFENSIBLE
    if score >= 0.6:
        return ConfidenceLevel.AGGRESSIVE
    if score >= 0.3:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════
# FACT FRAGILITY SCORING (Component 15)
# ═══════════════════════════════════════════════════════════════════════

def score_fact_fragility(
    doctrine_count: int,
    cloud_records: int,
    has_statutory_authority: bool,
    zone: AnalysisZone,
) -> FactFragilityScore:
    """Score the fragility of factual assertions in the response."""
    verifiability = min(1.0, (doctrine_count * 0.25) + (0.15 if has_statutory_authority else 0.0))
    documentary_support = min(1.0, cloud_records * 0.1)
    testimony_dependence = max(0.0, 1.0 - verifiability - (documentary_support * 0.5))
    rechar_risk = 0.2 if zone == AnalysisZone.PLANNING else 0.5 if zone == AnalysisZone.AUDIT else 0.3
    overall = 1.0 - ((verifiability * 0.3) + (documentary_support * 0.3) + ((1.0 - testimony_dependence) * 0.2) + ((1.0 - rechar_risk) * 0.2))
    narratives = {
        (True, True): "Strong documentary and doctrinal support. Low fragility.",
        (True, False): "Doctrinal support present but limited external documentation.",
        (False, True): "External documentation present but no matching doctrine. Verify applicability.",
        (False, False): "Limited support. High fragility. Treat as preliminary analysis only.",
    }
    narrative = narratives[(doctrine_count > 0, cloud_records > 2)]
    return FactFragilityScore(
        overall_score=round(overall, 3),
        verifiability=round(verifiability, 3),
        recharacterization_risk=round(rechar_risk, 3),
        testimony_dependence=round(testimony_dependence, 3),
        documentary_support=round(documentary_support, 3),
        narrative=narrative,
    )


# ═══════════════════════════════════════════════════════════════════════
# ZONED ANALYSIS (Component 14)
# ═══════════════════════════════════════════════════════════════════════

ZONE_GUIDELINES: Dict[AnalysisZone, str] = {
    AnalysisZone.PLANNING: (
        "PLANNING ZONE: Forward-looking analysis for succession design and strategy. "
        "Recommendations may include aggressive positions where supported by authority. "
        "Focus on actionable implementation steps."
    ),
    AnalysisZone.REPORTING: (
        "REPORTING ZONE: Factual description of current succession state and gaps. "
        "Neutral tone. Document findings without advocacy. Suitable for board reporting."
    ),
    AnalysisZone.AUDIT: (
        "AUDIT ZONE: Defensive, evidence-based analysis. All assertions must have "
        "documented authority support. Disclose uncertainty. Suitable for regulatory "
        "examination or litigation discovery."
    ),
}


def apply_zone_framing(conclusion: str, reasoning: str, zone: AnalysisZone) -> Tuple[str, str]:
    """Apply zone-specific framing to response content."""
    guideline = ZONE_GUIDELINES[zone]
    if zone == AnalysisZone.AUDIT:
        conclusion = f"[AUDIT-GRADE] {conclusion}"
        reasoning = f"{guideline}\n\n{reasoning}"
    elif zone == AnalysisZone.REPORTING:
        conclusion = f"[REPORT] {conclusion}"
    return conclusion, reasoning


# ═══════════════════════════════════════════════════════════════════════
# MULTI-DOCTRINE DECOMPOSITION (Component 19)
# ═══════════════════════════════════════════════════════════════════════

INTERACTION_EDGES: List[Tuple[str, str]] = [
    ("succession_planning_fundamentals", "power_transfer_protocols"),
    ("succession_planning_fundamentals", "succession_timeline"),
    ("heir_validation", "competency_assessment"),
    ("heir_validation", "succession_training"),
    ("emergency_succession", "regent_designation"),
    ("dynasty_continuity", "family_governance"),
    ("dynasty_continuity", "legacy_preservation"),
    ("trust_succession", "dynasty_continuity"),
    ("corporate_succession", "succession_metrics"),
    ("corporate_succession", "stakeholder_management"),
    ("succession_communication", "stakeholder_management"),
    ("contested_succession", "family_governance"),
    ("parallel_succession_tracks", "competency_assessment"),
    ("succession_documentation", "succession_review"),
    ("succession_metrics", "succession_review"),
    ("succession_training", "parallel_succession_tracks"),
]


def decompose_multi_doctrine(query: str, matched_doctrines: List[DoctrineBlock]) -> DecomposedIssue:
    """Decompose a query touching multiple doctrines into structured sub-issues."""
    if not matched_doctrines:
        return DecomposedIssue(
            category=IssueCategory.LEADERSHIP_TRANSFER,
            sub_issues=["No matching doctrine found for decomposition"],
            doctrine_topics=[],
        )
    topics = [d.topic for d in matched_doctrines]
    categories = [d.issue_category for d in matched_doctrines]
    primary_category = max(set(categories), key=categories.count)
    relevant_edges = [(a, b) for a, b in INTERACTION_EDGES if a in topics or b in topics]
    sub_issues = [f"[{d.issue_category.value}] {d.topic}: {d.conclusion_template[:120]}..." for d in matched_doctrines]
    resolution_order = _topological_sort(topics, relevant_edges)
    return DecomposedIssue(
        category=primary_category,
        sub_issues=sub_issues,
        doctrine_topics=topics,
        interaction_edges=relevant_edges,
        resolution_order=resolution_order,
    )


def _topological_sort(nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
    """Topological sort for doctrine resolution order."""
    in_degree: Dict[str, int] = {n: 0 for n in nodes}
    adj: Dict[str, List[str]] = {n: [] for n in nodes}
    for a, b in edges:
        if a in adj and b in in_degree:
            adj[a].append(b)
            in_degree[b] += 1
    queue = [n for n in nodes if in_degree[n] == 0]
    result: List[str] = []
    while queue:
        queue.sort()
        node = queue.pop(0)
        result.append(node)
        for neighbor in adj.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    for n in nodes:
        if n not in result:
            result.append(n)
    return result


# ═══════════════════════════════════════════════════════════════════════
# DETERMINISM HASH (Component 17)
# ═══════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, conclusion: str, reasoning: str, mode: str, zone: str) -> str:
    """SHA-256 hash for response determinism verification."""
    payload = f"{query}|{conclusion}|{reasoning}|{mode}|{zone}|{ENGINE_VERSION}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════
# TELEMETRY (Component 10)
# ═══════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Collects and exposes query telemetry metrics."""

    def __init__(self) -> None:
        self._traces: List[TelemetryTrace] = []
        self._latencies: List[float] = []
        self._layer_counts: Dict[str, int] = defaultdict(int)
        self._error_domains: Dict[str, int] = defaultdict(int)
        self._total_queries: int = 0
        self._cache_hits: int = 0
        self._start_time: float = time.monotonic()

    def record(self, trace: TelemetryTrace) -> None:
        self._traces.append(trace)
        self._latencies.append(trace.latency_ms)
        self._layer_counts[trace.layer_hit.value] += 1
        self._total_queries += 1
        if trace.cache_hit:
            self._cache_hits += 1
        if trace.error_domain:
            self._error_domains[trace.error_domain] += 1

    @property
    def metrics(self) -> Dict[str, Any]:
        uptime = time.monotonic() - self._start_time
        qph = (self._total_queries / (uptime / 3600.0)) if uptime > 0 else 0.0
        return {
            "total_queries": self._total_queries,
            "cache_hit_rate": round(self._cache_hits / max(self._total_queries, 1), 3),
            "avg_latency_ms": round(statistics.mean(self._latencies), 2) if self._latencies else 0.0,
            "p95_latency_ms": round(sorted(self._latencies)[int(len(self._latencies) * 0.95)] if len(self._latencies) >= 20 else max(self._latencies, default=0.0), 2),
            "queries_per_hour": round(qph, 1),
            "layer_distribution": dict(self._layer_counts),
            "error_domains": dict(self._error_domains),
            "uptime_seconds": round(uptime, 1),
        }


# ═══════════════════════════════════════════════════════════════════════
# DRIFT WATCHER (Component 11)
# ═══════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detects confidence drift in doctrine responses over time."""

    def __init__(self) -> None:
        self._events: List[DriftEvent] = []
        self._topic_history: Dict[str, List[ConfidenceLevel]] = defaultdict(list)

    def check(self, topic: str, current_confidence: ConfidenceLevel, query: str) -> Optional[DriftEvent]:
        history = self._topic_history[topic]
        event: Optional[DriftEvent] = None
        if history and history[-1] != current_confidence:
            event = DriftEvent(
                doctrine_topic=topic,
                original_confidence=history[-1],
                new_confidence=current_confidence,
                trigger_query=query[:200],
                reason=f"Confidence shifted from {history[-1].value} to {current_confidence.value}",
            )
            self._events.append(event)
            logger.warning(f"DRIFT DETECTED: {topic} confidence {history[-1].value} -> {current_confidence.value}")
        history.append(current_confidence)
        return event

    @property
    def event_count(self) -> int:
        return len(self._events)

    @property
    def recent_events(self) -> List[DriftEvent]:
        return self._events[-20:]


# ═══════════════════════════════════════════════════════════════════════
# COVERAGE MAP (Component 12)
# ═══════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Tracks which doctrines are being triggered and which are gaps."""

    def __init__(self, doctrines: List[DoctrineBlock]) -> None:
        self._entries: Dict[str, CoverageEntry] = {
            d.topic: CoverageEntry(topic=d.topic) for d in doctrines
        }
        self._total_misses: int = 0

    def record_hit(self, topic: str) -> None:
        if topic in self._entries:
            self._entries[topic].hit_count += 1
            self._entries[topic].last_hit = datetime.now(timezone.utc).isoformat()

    def record_miss(self, query: str) -> None:
        self._total_misses += 1

    @property
    def stats(self) -> Dict[str, Any]:
        entries = list(self._entries.values())
        triggered = [e for e in entries if e.hit_count > 0]
        untriggered = [e for e in entries if e.hit_count == 0]
        return {
            "total_doctrines": len(entries),
            "triggered_count": len(triggered),
            "untriggered_count": len(untriggered),
            "untriggered_topics": [e.topic for e in untriggered],
            "total_cache_misses": self._total_misses,
            "most_hit": sorted(triggered, key=lambda e: -e.hit_count)[:5] if triggered else [],
            "coverage_percentage": round(len(triggered) / max(len(entries), 1) * 100, 1),
        }


# ═══════════════════════════════════════════════════════════════════════
# AUDIT TRAIL (Component 16)
# ═══════════════════════════════════════════════════════════════════════

class AuditTrail:
    """Append-only JSONL audit trail for every query."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, query_id: str, query: str, mode: str, zone: str, layer: str,
            confidence: str, determinism_hash: str, latency_ms: float) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine_id": ENGINE_ID,
            "query_id": query_id,
            "query_hash": hashlib.sha256(query.encode()).hexdigest(),
            "mode": mode,
            "zone": zone,
            "layer": layer,
            "confidence": confidence,
            "determinism_hash": determinism_hash,
            "latency_ms": latency_ms,
        }
        try:
            with open(self._path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            logger.error(f"Audit trail write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════
# DEEP ANALYSIS MODE (Component 20)
# ═══════════════════════════════════════════════════════════════════════

async def deep_analysis(
    query: str,
    doctrines: List[DoctrineBlock],
    cloud: CloudKnowledge,
    zone: AnalysisZone,
    mode: ResponseMode,
) -> Tuple[str, str, List[str], ConfidenceLevel]:
    """Multi-source synthesis with full reasoning chain for complex queries."""
    parts: List[str] = []
    all_factors: List[str] = []
    authority_weights: List[float] = []

    for d in doctrines:
        parts.append(f"DOCTRINE [{d.topic}]: {d.conclusion_template}")
        parts.append(f"FRAMEWORK: {d.reasoning_framework[:300]}")
        all_factors.extend(d.key_factors[:3])
        citations = harden_authorities(d.primary_authority)
        authority_weights.extend([c.weight for c in citations])

    if cloud.has_results:
        parts.append(f"CLOUD EVIDENCE ({cloud.total_records} records): {cloud.merged_text(1500)}")

    conclusion_parts: List[str] = []
    for d in doctrines:
        conclusion_parts.append(d.conclusion_template)

    if mode == ResponseMode.MEMO:
        conclusion = "MEMORANDUM ANALYSIS:\n\n" + "\n\n".join(conclusion_parts)
    elif mode == ResponseMode.DEFENSE:
        conclusion = "DEFENSIVE POSITION:\n\n" + "\n\n".join(
            f"- {c}" for c in conclusion_parts
        )
    else:
        conclusion = " ".join(conclusion_parts[:2])

    reasoning = "\n\n".join(parts)

    avg_weight = statistics.mean(authority_weights) if authority_weights else 0.3
    confidence = stratify_confidence(
        doctrine_match_count=len(doctrines),
        authority_weight_avg=avg_weight,
        cloud_records=cloud.total_records,
        zone=zone,
    )

    unique_factors = list(dict.fromkeys(all_factors))
    return conclusion, reasoning, unique_factors[:10], confidence


# ═══════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ENGINE (Component 1-3)
# ═══════════════════════════════════════════════════════════════════════

class SuccessionProtocolEngine:
    """Core engine orchestrating three-layer response with all TIE-20 components."""

    def __init__(self) -> None:
        self.cloud = CognitionCloudRetriever()
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap(DOCTRINE_CACHE)
        self.audit_trail = AuditTrail(AUDIT_LOG_PATH)
        self._start_time = time.monotonic()
        logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} initialized on port {ENGINE_PORT}")

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Three-layer response: doctrine cache -> semantic retrieval -> deep analysis."""
        start = time.monotonic()
        query_id = str(uuid.uuid4())
        normalized_query = normalize_succession_terms(request.query)

        # ── Layer 1: Doctrine Cache ──────────────────────────
        cache_matches = search_doctrine_cache(normalized_query, top_k=3)
        layer = ResponseLayer.DOCTRINE_CACHE
        cache_hit = len(cache_matches) > 0

        if cache_matches:
            for m in cache_matches:
                self.coverage_map.record_hit(m.topic)
        else:
            self.coverage_map.record_miss(normalized_query)

        # ── Layer 2: Semantic / Cloud Retrieval ──────────────
        cloud = CloudKnowledge()
        if not cache_hit or request.force_deep:
            layer = ResponseLayer.SEMANTIC_RETRIEVAL
            try:
                cloud = await self.cloud.retrieve_all(
                    normalized_query, category="succession", ekm_limit=10,
                )
            except Exception as exc:
                logger.warning(f"Cloud retrieval failed: {exc}")

        # ── Layer 3: Deep Analysis ───────────────────────────
        if request.force_deep or (not cache_hit and cloud.total_records < 3) or request.mode == ResponseMode.MEMO:
            layer = ResponseLayer.DEEP_ANALYSIS

        # ── Build Response ───────────────────────────────────
        if layer == ResponseLayer.DEEP_ANALYSIS or request.mode == ResponseMode.MEMO:
            conclusion, reasoning, key_factors, confidence = await deep_analysis(
                normalized_query,
                cache_matches if cache_matches else DOCTRINE_CACHE[:2],
                cloud, request.zone, request.mode,
            )
        elif cache_matches:
            primary = cache_matches[0]
            conclusion = primary.conclusion_template
            reasoning = primary.reasoning_framework
            key_factors = primary.key_factors
            citations = harden_authorities(primary.primary_authority)
            avg_w = statistics.mean([c.weight for c in citations]) if citations else 0.3
            confidence = stratify_confidence(len(cache_matches), avg_w, cloud.total_records, request.zone)
        else:
            conclusion = "No specific doctrine matched. General succession principles apply."
            reasoning = "Query did not match cached doctrine patterns. Cloud retrieval provided limited results."
            key_factors = ["Insufficient doctrine coverage for this query"]
            confidence = ConfidenceLevel.HIGH_RISK

        # ── Zone framing ─────────────────────────────────────
        conclusion, reasoning = apply_zone_framing(conclusion, reasoning, request.zone)

        # ── Authority hardening ──────────────────────────────
        all_auths: List[str] = []
        for d in cache_matches:
            all_auths.extend(d.primary_authority)
        authorities = resolve_authority_conflicts(harden_authorities(all_auths))

        # ── Fact fragility ───────────────────────────────────
        has_statutory = any(a.level in (AuthorityLevel.STATUTORY, AuthorityLevel.CONSTITUTIONAL) for a in authorities)
        fragility = score_fact_fragility(len(cache_matches), cloud.total_records, has_statutory, request.zone)

        # ── Multi-doctrine decomposition ─────────────────────
        decomposition = decompose_multi_doctrine(normalized_query, cache_matches) if len(cache_matches) > 1 else None

        # ── Determinism hash ─────────────────────────────────
        det_hash = compute_determinism_hash(request.query, conclusion, reasoning, request.mode.value, request.zone.value)

        # ── Drift check ──────────────────────────────────────
        for d in cache_matches:
            self.drift_watcher.check(d.topic, confidence, request.query)

        # ── Disclosure caveat ────────────────────────────────
        disclosure = ""
        if confidence in (ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK):
            disclosure = (
                "This analysis involves significant uncertainty. The conclusions should be treated "
                "as preliminary and verified against authoritative sources before reliance."
            )

        latency = round((time.monotonic() - start) * 1000, 2)

        # ── Telemetry trace ──────────────────────────────────
        trace = TelemetryTrace(
            query_hash=hashlib.sha256(request.query.encode()).hexdigest(),
            layer_hit=layer,
            doctrine_topic=cache_matches[0].topic if cache_matches else None,
            latency_ms=latency,
            cache_hit=cache_hit,
            cloud_records=cloud.total_records,
            confidence=confidence,
            zone=request.zone,
            mode=request.mode,
        )
        self.telemetry.record(trace)

        # ── Audit trail ──────────────────────────────────────
        self.audit_trail.log(
            query_id=query_id, query=request.query, mode=request.mode.value,
            zone=request.zone.value, layer=layer.value, confidence=confidence.value,
            determinism_hash=det_hash, latency_ms=latency,
        )

        return QueryResponse(
            query_id=query_id,
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            layer_hit=layer,
            confidence=confidence,
            conclusion=conclusion,
            reasoning=reasoning,
            key_factors=key_factors,
            authorities=authorities,
            fact_fragility=fragility,
            decomposition=decomposition,
            cloud_knowledge_summary=cloud.merged_text(800) if cloud.has_results else "",
            disclosure_caveat=disclosure,
            determinism_hash=det_hash,
            latency_ms=latency,
            telemetry=trace,
        )

    @property
    def health(self) -> HealthResponse:
        return HealthResponse(
            uptime_seconds=round(time.monotonic() - self._start_time, 1),
            total_queries=self.telemetry._total_queries,
            doctrine_count=len(DOCTRINE_CACHE),
            coverage_stats=self.coverage_map.stats,
            metrics=self.telemetry.metrics,
            drift_events=self.drift_watcher.event_count,
            cloud_retriever_stats=self.cloud.stats,
        )


# ═══════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (Component 1)
# ═══════════════════════════════════════════════════════════════════════

engine: Optional[SuccessionProtocolEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    global engine
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine = SuccessionProtocolEngine()
    yield
    if engine:
        await engine.cloud.close()
    logger.info(f"{ENGINE_NAME} shutdown complete")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="BLOODLINE tier succession planning, inheritance protocols, and dynasty continuity engine.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Endpoint (Component 2) ────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check returning engine status and metrics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.health


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "engine": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "tier": ENGINE_TIER,
        "status": "operational",
    }


# ── Query Endpoint (Component 3) ─────────────────────────────────────

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Process succession protocol query through three-layer response system."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return await engine.process_query(request)


# ── Metrics Endpoint ─────────────────────────────────────────────────

@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """Return engine telemetry metrics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.telemetry.metrics


# ── Coverage Endpoint ────────────────────────────────────────────────

@app.get("/coverage")
async def coverage_endpoint() -> Dict[str, Any]:
    """Return doctrine coverage map statistics."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.coverage_map.stats


# ── Drift Endpoint ───────────────────────────────────────────────────

@app.get("/drift")
async def drift_endpoint() -> Dict[str, Any]:
    """Return recent confidence drift events."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return {
        "total_drift_events": engine.drift_watcher.event_count,
        "recent_events": [e.model_dump() for e in engine.drift_watcher.recent_events],
    }


# ── Doctrines Endpoint ──────────────────────────────────────────────

@app.get("/doctrines")
async def doctrines_endpoint() -> Dict[str, Any]:
    """Return all loaded doctrine topics and their metadata."""
    return {
        "count": len(DOCTRINE_CACHE),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "category": d.issue_category.value,
            }
            for d in DOCTRINE_CACHE
        ],
    }


# ═══════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    logger.add(
        str(Path(__file__).parent / "engine.log"),
        rotation="50 MB",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
    )
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
