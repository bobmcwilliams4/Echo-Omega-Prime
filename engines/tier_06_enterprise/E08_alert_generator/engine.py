"""
E08 Alert Generator Engine - ECHO OMEGA PRIME
===============================================
Generates alerts from document changes, filings, ownership transfers,
lease expirations, regulatory events, production changes, and other
significant events across monitored properties and entities.

TIE-20 Compliant | Port 8608 | v1.0.0 | Mode: Rule-Based
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

try:
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
ENGINE_ID = "E08"
ENGINE_NAME = "Alert Generator Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8608
ENGINE_DOMAIN = "alert_generation"

LOG_DIR = Path("O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/E08_alert_generator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "e08_audit.jsonl"

logger.add(LOG_DIR / "e08_engine.log", rotation="50 MB", retention="30 days", level="DEBUG")
logger.add(AUDIT_LOG, rotation="20 MB", retention="90 days", level="INFO", serialize=True)

BANNED_PHRASES = [
    "guaranteed", "always triggers", "never misses", "100% accurate",
    "no false positives", "perfect detection", "absolute certainty",
]

# ═══════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class AlertCategory(str, Enum):
    NEW_FILING = "NEW_FILING"
    OWNERSHIP_CHANGE = "OWNERSHIP_CHANGE"
    LEASE_EXPIRATION = "LEASE_EXPIRATION"
    LEASE_EXTENSION = "LEASE_EXTENSION"
    PERMIT_ISSUED = "PERMIT_ISSUED"
    PERMIT_EXPIRATION = "PERMIT_EXPIRATION"
    VIOLATION_FILED = "VIOLATION_FILED"
    PRODUCTION_CHANGE = "PRODUCTION_CHANGE"
    OPERATOR_CHANGE = "OPERATOR_CHANGE"
    LIEN_FILED = "LIEN_FILED"
    LIEN_RELEASED = "LIEN_RELEASED"
    PROBATE_FILED = "PROBATE_FILED"
    COURT_ORDER = "COURT_ORDER"
    TAX_DELINQUENT = "TAX_DELINQUENT"
    COMPETITIVE_ACTIVITY = "COMPETITIVE_ACTIVITY"
    PRICE_THRESHOLD = "PRICE_THRESHOLD"
    ROYALTY_PAYMENT = "ROYALTY_PAYMENT"
    SHUT_IN = "SHUT_IN"
    PLUGGING_NOTICE = "PLUGGING_NOTICE"
    UNITIZATION = "UNITIZATION"
    POOLING = "POOLING"
    SURFACE_DAMAGE = "SURFACE_DAMAGE"
    ENVIRONMENTAL_RELEASE = "ENVIRONMENTAL_RELEASE"
    BANKRUPTCY_FILED = "BANKRUPTCY_FILED"
    TITLE_DEFECT = "TITLE_DEFECT"
    ASSIGNMENT_RECORDED = "ASSIGNMENT_RECORDED"
    DIVISION_ORDER_CHANGE = "DIVISION_ORDER_CHANGE"
    WELL_COMPLETION = "WELL_COMPLETION"
    SPACING_ORDER = "SPACING_ORDER"
    FORCE_MAJEURE = "FORCE_MAJEURE"
    REGULATORY_CHANGE = "REGULATORY_CHANGE"


class AlertSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    WEBHOOK = "WEBHOOK"
    IN_APP = "IN_APP"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class AlertStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    SUPPRESSED = "SUPPRESSED"


# ═══════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    context: Dict[str, Any] = Field(default_factory=dict)
    property_id: Optional[str] = None
    user_id: Optional[str] = None


class EventInput(BaseModel):
    event_type: str
    source: str = "unknown"
    property_id: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = "TX"
    instrument_number: Optional[str] = None
    grantor: Optional[str] = None
    grantee: Optional[str] = None
    effective_date: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlertRule(BaseModel):
    rule_id: str
    category: AlertCategory
    severity: AlertSeverity
    description: str
    condition_keywords: List[str]
    instrument_types: List[str] = Field(default_factory=list)
    cooldown_minutes: int = 60
    dedup_window_minutes: int = 1440
    escalation_after_minutes: int = 480
    enabled: bool = True


class AlertOutput(BaseModel):
    alert_id: str
    category: AlertCategory
    severity: AlertSeverity
    title: str
    description: str
    property_id: Optional[str] = None
    county: Optional[str] = None
    triggered_by: str
    rule_id: str
    confidence: ConfidenceLevel
    recommended_action: str
    timestamp: str
    status: AlertStatus = AlertStatus.PENDING
    dedup_key: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SubscriptionConfig(BaseModel):
    subscription_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    user_id: str
    property_ids: List[str] = Field(default_factory=list)
    counties: List[str] = Field(default_factory=list)
    categories: List[AlertCategory] = Field(default_factory=list)
    min_severity: AlertSeverity = AlertSeverity.LOW
    channels: List[NotificationChannel] = Field(default_factory=lambda: [NotificationChannel.IN_APP])
    batch_interval_minutes: int = 60
    enabled: bool = True


class DoctrineBlock(BaseModel):
    topic: str
    category: AlertCategory
    keywords: List[str]
    severity_default: AlertSeverity
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    instrument_types: List[str] = Field(default_factory=list)
    cooldown_minutes: int = 60
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: str = ""


# ═══════════════════════════════════════════════════════════════
# TIE-3: DOCTRINE CACHE (30+ alert rule blocks)
# ═══════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="New Filing Detection",
        category=AlertCategory.NEW_FILING,
        keywords=["filing", "recorded", "instrument", "document", "deed", "new record"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="A new instrument has been filed in {county} County affecting monitored property. Instrument #{instrument_number} recorded on {date} should be reviewed for impact on title and interests.",
        reasoning_framework="When a new instrument is recorded in any county where monitored properties exist, the system cross-references the legal description, grantor/grantee names, and survey information against the monitored property database. A match on any of these vectors triggers an alert. The filing may affect ownership interests, encumbrances, or operational rights. Immediate review is warranted for deeds, assignments, and releases; lower priority for unrelated filings that happen to match on name only.",
        key_factors=["instrument_type", "legal_description_match", "name_match_confidence", "recording_date", "county"],
        primary_authority=["County Clerk recording statutes", "TX Property Code Ch. 13", "TX Business & Commerce Code Ch. 9 (UCC filings)"],
        instrument_types=["DEED", "ASSIGNMENT", "RELEASE", "MORTGAGE", "LIEN", "EASEMENT", "RIGHT_OF_WAY", "PLAT", "AFFIDAVIT"],
        cooldown_minutes=30,
        confidence=ConfidenceLevel.DEFENSIBLE,
        counter_arguments=["Name match may be coincidental", "Legal description overlap may be partial", "Instrument may not affect mineral estate"],
        resolution_strategy="Pull full instrument image, compare legal description against property database, verify grantor/grantee chain, determine if mineral or surface estate affected."
    ),
    DoctrineBlock(
        topic="Ownership Transfer Detection",
        category=AlertCategory.OWNERSHIP_CHANGE,
        keywords=["transfer", "conveyance", "deed", "assignment", "mineral deed", "royalty deed", "ownership"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="An ownership change has been detected for {property_id}. A {instrument_type} from {grantor} to {grantee} was recorded, potentially altering the division of interests. Division orders should be reviewed and updated.",
        reasoning_framework="Ownership changes are among the highest-priority events because they directly affect payment obligations, lease validity, and title insurance coverage. When a deed or assignment transfers mineral interests, royalty interests, or overriding royalty interests, all downstream obligations must be re-evaluated. This includes division order updates, suspense account reviews, and lessee notification requirements under TX Natural Resources Code Sec. 91.402.",
        key_factors=["interest_type_transferred", "fractional_interest", "effective_date", "consideration", "reservations_and_exceptions", "recording_lag"],
        primary_authority=["TX Natural Resources Code Sec. 91.402", "TX Property Code Ch. 5", "Division order statutes by state"],
        instrument_types=["MINERAL_DEED", "ROYALTY_DEED", "ASSIGNMENT", "QUIT_CLAIM", "WARRANTY_DEED", "SPECIAL_WARRANTY_DEED"],
        cooldown_minutes=15,
        confidence=ConfidenceLevel.DEFENSIBLE,
        counter_arguments=["Deed may be corrective only", "Transfer may be between related entities", "Reservation language may limit actual transfer"],
        resolution_strategy="Obtain full deed, extract interest fractions, update run sheet, flag for division order revision, notify operator if applicable."
    ),
    DoctrineBlock(
        topic="Lease Expiration Warning",
        category=AlertCategory.LEASE_EXPIRATION,
        keywords=["expiration", "primary term", "lease end", "habendum", "unless clause", "term expiring"],
        severity_default=AlertSeverity.CRITICAL,
        conclusion_template="Lease {lease_id} on {property_id} has a primary term expiring on {expiration_date}. If no operations are commenced or production established before expiration, the lease will terminate by its own terms. Immediate review of savings clauses is required.",
        reasoning_framework="Lease expiration is critical because it represents permanent loss of leasehold rights. Texas follows the 'unless' habendum clause doctrine strictly: if the lessee fails to commence operations or achieve production by the end of the primary term, the lease automatically terminates without notice from the lessor. Savings clauses (continuous drilling, shut-in royalty, force majeure, pooling) must each be evaluated individually. The 60-day, 30-day, and 7-day warning windows allow progressively urgent responses.",
        key_factors=["primary_term_end_date", "current_production_status", "drilling_operations_status", "savings_clauses_available", "shut_in_royalty_paid", "pooling_declarations"],
        primary_authority=["TX habendum clause jurisprudence", "Anadarko Petroleum v. Thompson (2015)", "Natural Gas Pipeline Co. v. Pool (Tex. 1953)", "Rogers v. Ricane Enterprises (Tex. App. 2004)"],
        instrument_types=["OIL_GAS_LEASE", "EXTENSION", "RATIFICATION"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.DEFENSIBLE,
        counter_arguments=["Savings clause may preserve lease", "Pooled production may hold lease", "Shut-in royalty may extend term", "Continuous drilling clause may apply"],
        resolution_strategy="Calculate exact days remaining, evaluate all savings clauses, check pooling declarations, verify production records, escalate to landman for immediate action if <30 days."
    ),
    DoctrineBlock(
        topic="Lease Extension Deadline",
        category=AlertCategory.LEASE_EXTENSION,
        keywords=["extension", "option", "renewal", "additional term", "extend", "continuation"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Extension option for lease {lease_id} must be exercised by {deadline}. The extension requires {consideration} and must comply with the specific notice provisions in the lease. Failure to exercise timely will result in loss of the extension right.",
        reasoning_framework="Extension options are contractual rights that expire if not timely exercised. Most oil and gas leases require written notice to the lessor and payment of additional consideration within a specified window. The exercise must strictly comply with the lease terms: wrong address, late payment, or insufficient consideration can void the extension. Calendar the deadline with buffer for mailing and banking delays.",
        key_factors=["option_exercise_deadline", "required_consideration", "notice_requirements", "lessor_contact_info", "extension_term_length"],
        primary_authority=["Contract law principles", "Lease-specific terms", "TX Property Code notice requirements"],
        instrument_types=["EXTENSION_AGREEMENT", "AMENDMENT", "MEMORANDUM"],
        cooldown_minutes=720,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Drilling Permit Issued",
        category=AlertCategory.PERMIT_ISSUED,
        keywords=["permit", "drilling permit", "W-1", "injection permit", "disposal permit", "RRC permit"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="A new {permit_type} permit has been issued in the vicinity of monitored properties. Permit #{permit_number} was issued to {operator} for {well_name} in {county} County. This may indicate competitive drilling activity or offset well obligations.",
        reasoning_framework="New permit issuance signals future drilling activity. For monitored properties, this triggers several analysis paths: (1) Is this an offset well requiring protective drilling? (2) Does the operator hold leases on our monitored tracts? (3) Does the permitted location fall within pooling distance? (4) Will the new well drain from our monitored reservoirs? RRC Form W-1 data includes location, depth, target formation, and operator identity.",
        key_factors=["permit_type", "operator_name", "proposed_depth", "target_formation", "distance_to_monitored_property", "lease_obligation_triggers"],
        primary_authority=["TX RRC Statewide Rules", "16 TAC Ch. 3", "RRC Form W-1 requirements"],
        instrument_types=["PERMIT", "W-1", "W-1A"],
        cooldown_minutes=60,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Permit Expiration Warning",
        category=AlertCategory.PERMIT_EXPIRATION,
        keywords=["permit expiring", "permit lapse", "permit renewal", "W-1 expiration"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Drilling permit #{permit_number} for {well_name} expires on {expiration_date}. If operations have not commenced, the permit must be renewed or the drilling authorization will lapse.",
        reasoning_framework="RRC drilling permits (W-1) are valid for two years from issuance. If spud has not occurred, an extension or new permit is required. Lapsed permits may indicate abandoned plans or operational delays. For our operations, monitor for expiration to prevent loss of drilling rights. For competitor permits, expiration may signal reduced competitive pressure.",
        key_factors=["permit_issue_date", "expiration_date", "spud_status", "renewal_availability", "operator_activity_level"],
        primary_authority=["16 TAC Sec. 3.5", "RRC permit validity rules"],
        instrument_types=["PERMIT"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="RRC Violation Detection",
        category=AlertCategory.VIOLATION_FILED,
        keywords=["violation", "notice of violation", "NOV", "enforcement", "penalty", "non-compliance", "citation"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="A violation has been filed against {operator} for {well_name} in {county} County. Violation type: {violation_type}. This may affect operations, permit renewals, and regulatory standing.",
        reasoning_framework="RRC violations carry significant consequences: financial penalties, operational restrictions, permit holds, and in severe cases, forced plugging orders. Violations against operators on monitored properties directly affect production continuity and royalty streams. Violations against our own operations require immediate remediation to avoid escalation. Track violation severity, response deadline, and operator compliance history.",
        key_factors=["violation_type", "severity_classification", "response_deadline", "operator_compliance_history", "remediation_requirements", "financial_penalty_range"],
        primary_authority=["TX Natural Resources Code Ch. 81", "16 TAC Ch. 3", "RRC enforcement procedures"],
        instrument_types=["NOTICE_OF_VIOLATION", "ENFORCEMENT_ORDER"],
        cooldown_minutes=30,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Production Change Detection",
        category=AlertCategory.PRODUCTION_CHANGE,
        keywords=["production", "decline", "increase", "volume change", "output", "rate change", "curtailment"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Significant production change detected for {well_name}: {direction} of {percentage}% compared to {comparison_period}. Current production: {current_volume}. Previous: {previous_volume}. This may indicate reservoir changes, mechanical issues, or operational adjustments.",
        reasoning_framework="Production changes exceeding threshold percentages (typically 20% month-over-month or 40% year-over-year) signal events requiring investigation. Declines may indicate mechanical failure, reservoir depletion, offset drainage, or curtailment. Increases may reflect workover success, infill drilling, or enhanced recovery. Both directions affect royalty projections, lease maintenance, and economic viability assessments.",
        key_factors=["production_direction", "percentage_change", "absolute_volume_change", "time_period", "well_type", "formation", "neighboring_well_activity"],
        primary_authority=["RRC production reporting requirements", "Lease production covenants", "Implied covenant of reasonable development"],
        cooldown_minutes=720,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
    DoctrineBlock(
        topic="Operator Change Detection",
        category=AlertCategory.OPERATOR_CHANGE,
        keywords=["operator change", "P-4", "transfer of operations", "new operator", "operator assignment"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Operator change detected: {old_operator} has transferred operations to {new_operator} for {well_name} in {county} County. RRC Form P-4 filed on {date}. Division orders, payment addresses, and operational contacts must be updated.",
        reasoning_framework="Operator changes affect every aspect of property management: who receives royalty payments changes, who is responsible for environmental compliance changes, who holds the insurance and bonding obligations changes. A P-4 filing at the RRC is the official transfer. However, the effective date of the transfer for payment purposes may differ from the recording date. All division orders must be re-executed with the new operator.",
        key_factors=["old_operator", "new_operator", "effective_date", "p4_filing_date", "affected_wells", "bond_transfer_status"],
        primary_authority=["RRC Form P-4 requirements", "16 TAC Sec. 3.1", "TX Natural Resources Code Sec. 89.002"],
        instrument_types=["P-4", "ASSIGNMENT_OF_OPERATIONS"],
        cooldown_minutes=60,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Lien Filed Detection",
        category=AlertCategory.LIEN_FILED,
        keywords=["lien", "mortgage", "deed of trust", "mechanic lien", "tax lien", "judgment lien", "encumbrance"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="A new lien has been recorded against property associated with {property_id}. {lien_type} filed by {lienholder} for {amount}. This encumbrance may affect title marketability, lease assignments, and lending transactions.",
        reasoning_framework="Liens create encumbrances that cloud title and may affect the priority of existing interests. Mechanic's liens in Texas must be filed within specific statutory periods (TX Property Code Ch. 53). Tax liens have super-priority and can extinguish junior interests. Judgment liens attach to all real property in the county of recording. Each lien type has different perfection requirements, priority rules, and foreclosure procedures.",
        key_factors=["lien_type", "amount", "lienholder", "recording_date", "priority_position", "statutory_deadline", "foreclosure_risk"],
        primary_authority=["TX Property Code Ch. 53 (mechanic's liens)", "TX Tax Code Ch. 32 (tax liens)", "TX Civil Practice & Remedies Code Ch. 52 (judgment liens)"],
        instrument_types=["LIEN", "DEED_OF_TRUST", "MORTGAGE", "MECHANICS_LIEN", "TAX_LIEN", "JUDGMENT_LIEN"],
        cooldown_minutes=30,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Lien Release Detection",
        category=AlertCategory.LIEN_RELEASED,
        keywords=["release", "satisfaction", "lien release", "release of lien", "discharge", "reconveyance"],
        severity_default=AlertSeverity.LOW,
        conclusion_template="A lien release has been recorded for property associated with {property_id}. {lien_type} originally filed by {lienholder} has been released/satisfied. Title is cleared of this specific encumbrance.",
        reasoning_framework="Lien releases are positive events that clear title encumbrances. However, they must be verified: is the release properly executed, does it reference the correct original instrument, and does it fully release all obligations? Partial releases may leave residual encumbrances. The release should be matched against the original lien in the title abstract.",
        key_factors=["original_lien_reference", "release_completeness", "proper_execution", "recording_verification"],
        primary_authority=["TX Property Code Sec. 12.014", "UCC Article 9 (secured transactions)"],
        instrument_types=["RELEASE_OF_LIEN", "SATISFACTION", "RECONVEYANCE"],
        cooldown_minutes=120,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Probate Filing Detection",
        category=AlertCategory.PROBATE_FILED,
        keywords=["probate", "heirship", "affidavit of heirship", "estate", "deceased", "intestate", "testate"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="A probate-related instrument has been filed affecting {property_id}. {instrument_type} for the estate of {decedent} may affect ownership interests. Title chain should be updated to reflect heirship or devises.",
        reasoning_framework="Probate events trigger complex title changes. In Texas, interests pass by law at death but the public record must be updated through probate proceedings (will admission, independent administration, dependent administration) or heirship affidavits (TX Estates Code Sec. 203.001). Until proper documentation is recorded, title is effectively unmarketable. Track probate proceedings through to final distribution and recording of muniments.",
        key_factors=["decedent_name", "probate_type", "court_jurisdiction", "interest_affected", "heirs_identified", "will_provisions"],
        primary_authority=["TX Estates Code", "TX Estates Code Sec. 203.001 (heirship affidavits)", "TX Property Code Ch. 5"],
        instrument_types=["AFFIDAVIT_OF_HEIRSHIP", "PROBATE_ORDER", "MUNIMENT_OF_TITLE", "LETTERS_TESTAMENTARY", "LETTERS_OF_ADMINISTRATION"],
        cooldown_minutes=60,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Court Order Detection",
        category=AlertCategory.COURT_ORDER,
        keywords=["court order", "judgment", "decree", "injunction", "partition", "quiet title"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="A court order has been recorded affecting property associated with {property_id}. {order_type} issued by {court} on {date}. The order may alter property rights, impose restrictions, or resolve title disputes.",
        reasoning_framework="Court orders carry the force of law and can fundamentally alter property rights. Partition orders divide co-tenancy interests. Quiet title decrees establish ownership against adverse claims. Injunctions restrict use or transfer. Receivership orders place property under court-appointed management. Each must be analyzed for its specific impact on monitored interests.",
        key_factors=["order_type", "issuing_court", "parties_affected", "property_impact", "appeal_status", "compliance_requirements"],
        primary_authority=["TX Civil Practice & Remedies Code", "TX Property Code Ch. 23 (partition)", "TX Property Code Ch. 64 (receivership)"],
        instrument_types=["COURT_ORDER", "JUDGMENT", "DECREE", "INJUNCTION"],
        cooldown_minutes=30,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Tax Delinquency Detection",
        category=AlertCategory.TAX_DELINQUENT,
        keywords=["tax delinquent", "delinquent taxes", "tax sale", "tax lien", "unpaid taxes", "tax foreclosure"],
        severity_default=AlertSeverity.CRITICAL,
        conclusion_template="Property tax delinquency detected for {property_id} in {county} County. Delinquent amount: {amount} for tax year {tax_year}. Tax sales can extinguish mineral interests in Texas. Immediate action required.",
        reasoning_framework="In Texas, ad valorem tax liens are super-priority and survive foreclosure of all junior interests, including mineral interests under certain conditions. Tax sales under TX Tax Code Sec. 34.01 can transfer property to the purchaser. The redemption period is 2 years for homestead, 180 days for other property. Mineral interest owners have independent duty to pay taxes on severed minerals. Delinquency should trigger immediate payment verification and potential intervention.",
        key_factors=["delinquent_amount", "tax_years_affected", "penalty_and_interest", "suit_filed_status", "redemption_period", "mineral_vs_surface_assessment"],
        primary_authority=["TX Tax Code Ch. 32-34", "TX Tax Code Sec. 34.01 (tax sales)", "Cabot Oil & Gas v. Healey (tax lien priority)"],
        instrument_types=["TAX_LIEN", "TAX_DEED"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Competitive Activity Detection",
        category=AlertCategory.COMPETITIVE_ACTIVITY,
        keywords=["competitor", "leasing activity", "new lease", "bonus", "competitive", "acreage acquisition"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Competitive activity detected near monitored properties. {operator} has filed {instrument_type} in {county} County, {distance} from {property_id}. This may indicate development plans that affect offset obligations or property values.",
        reasoning_framework="Competitor leasing and drilling activity near monitored properties serves as an early warning system for several scenarios: (1) offset well obligations under existing leases may be triggered, (2) competitive lease bonus rates may shift, (3) drainage from new wells may affect monitored reservoir pressure, (4) infrastructure development may create access opportunities. Track competitor activity by operator, formation, and proximity to build a competitive intelligence picture.",
        key_factors=["competitor_identity", "activity_type", "distance_to_property", "target_formation", "acreage_size", "trend_direction"],
        primary_authority=["Implied covenant of protection against drainage", "Offset well clauses", "Amoco Production Co. v. Alexander (drainage)"],
        cooldown_minutes=240,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
    DoctrineBlock(
        topic="Price Threshold Alert",
        category=AlertCategory.PRICE_THRESHOLD,
        keywords=["price", "WTI", "Henry Hub", "commodity price", "threshold", "price trigger", "breakeven"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Commodity price threshold crossed. {commodity} is now at ${current_price}, crossing the {direction} threshold of ${threshold_price}. This affects economic viability of {affected_count} monitored properties.",
        reasoning_framework="Commodity price movements trigger cascading decisions across the portfolio: lease economics change (some properties become sub-economic), drilling decisions are affected, shut-in decisions must be revisited, royalty projections need updating, and hedging strategies may need adjustment. The engine tracks user-configured price thresholds for WTI crude, Henry Hub natural gas, and NGL component prices.",
        key_factors=["commodity", "current_price", "threshold_price", "direction", "price_trend_30d", "affected_properties_count"],
        primary_authority=["Market data sources", "Lease economic threshold calculations"],
        cooldown_minutes=240,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
    DoctrineBlock(
        topic="Royalty Payment Alert",
        category=AlertCategory.ROYALTY_PAYMENT,
        keywords=["royalty", "payment", "check", "suspense", "underpayment", "late payment", "division order"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Royalty payment anomaly detected for {property_id}. Expected payment from {operator} for {production_month} has {issue_type}. TX statute requires payment within specified timeframes with interest penalties for late payment.",
        reasoning_framework="Texas Natural Resources Code Sec. 91.402 requires royalty payment within specific timeframes (120 days from first sale for new wells, 60 days from production month for established wells). Late payments accrue interest at the prime rate + 1%. Operators placing royalties in suspense must provide notice. Track payment patterns, flag anomalies (missed months, reduced amounts, unexpected suspense), and calculate statutory interest owed.",
        key_factors=["expected_payment_date", "actual_payment_date", "expected_amount", "actual_amount", "suspense_status", "operator_payment_history"],
        primary_authority=["TX Natural Resources Code Sec. 91.402", "TX Natural Resources Code Sec. 91.403 (penalties)", "Gavenda v. Strata Energy (royalty obligations)"],
        cooldown_minutes=720,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Well Shut-In Detection",
        category=AlertCategory.SHUT_IN,
        keywords=["shut-in", "shut in", "inactive", "no production", "suspended", "idle well"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Well {well_name} ({api_number}) has been shut in as of {date}. Shut-in duration affects lease maintenance obligations. If shut-in royalty clause exists, payment must be made to preserve the lease. Extended shut-in may trigger regulatory requirements.",
        reasoning_framework="A shut-in well creates multiple monitoring requirements: (1) If the lease is held by production, shut-in may terminate it unless a shut-in royalty clause exists and payment is made, (2) RRC requires reporting of shut-in wells, (3) Extended shut-in (>12 months) may trigger plugging requirements under Statewide Rule 14, (4) Shut-in gas wells have specific provisions under the 'cessation of production' doctrine.",
        key_factors=["shut_in_date", "shut_in_reason", "lease_shut_in_clause", "shut_in_royalty_paid", "rrc_reporting_status", "plugging_timeline"],
        primary_authority=["16 TAC Sec. 3.14 (inactive wells)", "TX Natural Resources Code Sec. 89.002", "Hydrocarbon Production & Shut-in provisions"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Plugging Notice Detection",
        category=AlertCategory.PLUGGING_NOTICE,
        keywords=["plugging", "P&A", "plug and abandon", "W-3A", "plugging report", "well closure"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Plugging notice filed for {well_name} ({api_number}) in {county} County. Operator {operator} has filed Form W-3A. This permanently removes the well from production capability and may affect lease maintenance if it is the sole producing well.",
        reasoning_framework="Well plugging is an irreversible event. If the plugged well is the only well holding an oil and gas lease, the lease may terminate. The plugging must comply with RRC Statewide Rule 14 and the operator must file Form W-3A within 30 days of completion. Environmental remediation of the well site is required. Surface owner has rights regarding site restoration under TX Natural Resources Code Sec. 91.112.",
        key_factors=["well_api_number", "plugging_reason", "is_sole_producing_well", "lease_impact", "surface_restoration_required", "environmental_status"],
        primary_authority=["16 TAC Sec. 3.14", "RRC Statewide Rule 14", "TX Natural Resources Code Sec. 89.011", "TX Natural Resources Code Sec. 91.112 (surface restoration)"],
        instrument_types=["W-3A", "PLUGGING_REPORT"],
        cooldown_minutes=120,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Unitization Application",
        category=AlertCategory.UNITIZATION,
        keywords=["unitization", "unit", "unit agreement", "unit application", "secondary recovery"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Unitization application filed affecting {property_id}. Operator {operator} is seeking to create a {unit_type} unit for {formation}. Unitization may alter working interest allocations and production sharing among tract owners.",
        reasoning_framework="Unitization combines multiple tracts into a single operational unit, typically for secondary or tertiary recovery operations. In Texas, voluntary unitization requires consent of owners of a majority of interests. RRC can order compulsory unitization under limited circumstances. Unitization changes the allocation of costs and production from a tract basis to a unit participation basis, which may increase or decrease individual owner returns depending on tract productivity factors.",
        key_factors=["unit_type", "participating_tracts", "allocation_formula", "consent_percentage", "compulsory_vs_voluntary", "enhanced_recovery_method"],
        primary_authority=["TX Natural Resources Code Ch. 101 (unitization)", "16 TAC Sec. 3.41-3.47", "Railroad Commission unitization rules"],
        instrument_types=["UNIT_AGREEMENT", "UNIT_DESIGNATION", "UNIT_AMENDMENT"],
        cooldown_minutes=120,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Force Pooling Application",
        category=AlertCategory.POOLING,
        keywords=["pooling", "force pooling", "compulsory pooling", "pooling order", "mineral pooling"],
        severity_default=AlertSeverity.CRITICAL,
        conclusion_template="Force pooling application filed affecting {property_id}. Operator {operator} has applied for compulsory pooling in {county} County for the {formation}. Affected mineral owners must respond within the statutory deadline or risk being pooled at default terms.",
        reasoning_framework="Force pooling in Texas is governed by the Mineral Interest Pooling Act (TX Natural Resources Code Ch. 102). An operator who cannot obtain voluntary pooling consent from all interest owners in a drilling unit can apply to the RRC for compulsory pooling. Affected owners who do not elect to participate may be made 'non-consenting' and subject to a risk penalty (typically 200-300% of costs before sharing in production). Response deadlines are strict. This is always a CRITICAL alert because failure to respond has severe financial consequences.",
        key_factors=["operator", "formation", "proposed_unit_size", "election_deadline", "participation_options", "risk_penalty_terms", "affected_interest_size"],
        primary_authority=["TX Natural Resources Code Ch. 102 (MIPA)", "16 TAC Sec. 3.40", "RRC pooling procedures"],
        instrument_types=["POOLING_APPLICATION", "POOLING_ORDER", "POOLING_DESIGNATION"],
        cooldown_minutes=60,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Surface Damage Claim",
        category=AlertCategory.SURFACE_DAMAGE,
        keywords=["surface damage", "surface use", "accommodation", "restoration", "road damage"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Surface damage or use issue detected for {property_id}. {issue_type} reported. The accommodation doctrine and surface use agreement terms govern the operator's obligations.",
        reasoning_framework="In Texas, the mineral estate is dominant, but the accommodation doctrine (Getty Oil v. Jones, 470 S.W.2d 618) requires the mineral lessee to accommodate existing surface uses when reasonable alternatives exist. Surface damage claims may arise from well pad construction, pipeline installation, road building, or salt water disposal. Track surface use agreements, damage complaints, and restoration timelines.",
        key_factors=["damage_type", "surface_use_agreement", "accommodation_doctrine_applicability", "restoration_timeline", "damage_amount"],
        primary_authority=["Getty Oil Co. v. Jones (Tex. 1971)", "TX Natural Resources Code Sec. 91.112", "Surface use agreements"],
        cooldown_minutes=240,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
    DoctrineBlock(
        topic="Environmental Release Detection",
        category=AlertCategory.ENVIRONMENTAL_RELEASE,
        keywords=["spill", "release", "contamination", "environmental", "TCEQ", "cleanup", "remediation"],
        severity_default=AlertSeverity.CRITICAL,
        conclusion_template="Environmental release reported near {property_id}. {release_type} involving {substance} reported by {responsible_party}. TCEQ and/or RRC notification may be required. Potential liability exposure for interest owners.",
        reasoning_framework="Environmental releases trigger immediate regulatory reporting obligations (TCEQ, RRC, EPA) and create long-term liability exposure. In Texas, the responsible party (typically the operator) bears primary cleanup responsibility, but CERCLA joint and several liability can reach other parties including mineral interest owners in certain circumstances. Track releases, remediation progress, and regulatory compliance status.",
        key_factors=["release_type", "substance_released", "volume", "affected_media", "reporting_status", "remediation_plan", "liability_exposure"],
        primary_authority=["TX Water Code Ch. 26", "TCEQ rules", "RRC Statewide Rule 8", "CERCLA Sec. 107"],
        cooldown_minutes=15,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Bankruptcy Filing Detection",
        category=AlertCategory.BANKRUPTCY_FILED,
        keywords=["bankruptcy", "Chapter 11", "Chapter 7", "debtor", "automatic stay", "trustee", "reorganization"],
        severity_default=AlertSeverity.CRITICAL,
        conclusion_template="Bankruptcy filing detected for entity with interests in {property_id}. {debtor} has filed {chapter} bankruptcy in {court}. Automatic stay is in effect. All collection and enforcement actions must cease immediately.",
        reasoning_framework="Bankruptcy filings trigger the automatic stay (11 USC Sec. 362), which halts all collection, foreclosure, and enforcement actions against the debtor and the debtor's property. For oil and gas interests, this affects: (1) Royalty payment obligations, (2) Lease forfeiture proceedings, (3) Lien enforcement, (4) Operator change requests. The bankruptcy estate includes all legal and equitable interests of the debtor, which may include oil and gas leases, mineral interests, and working interests. Track the case for plan confirmation, asset sales (363 sales), and rejection of executory contracts (including unexpired leases).",
        key_factors=["debtor_identity", "chapter_filed", "court_jurisdiction", "case_number", "assets_involved", "automatic_stay_scope", "key_dates"],
        primary_authority=["11 USC Sec. 362 (automatic stay)", "11 USC Sec. 365 (executory contracts)", "11 USC Sec. 363 (asset sales)", "In re ATP Oil & Gas (5th Cir. 2012)"],
        cooldown_minutes=30,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Title Defect Detection",
        category=AlertCategory.TITLE_DEFECT,
        keywords=["title defect", "cloud on title", "gap in chain", "missing heir", "wild deed", "forged instrument"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Potential title defect identified for {property_id}. {defect_type} detected in the chain of title. This defect may affect marketability and should be cured before any transaction or leasing activity.",
        reasoning_framework="Title defects reduce marketability and create risks for current and future transactions. Common defects include gaps in the chain of title, missing heirs, improperly acknowledged instruments, expired curative statutes, and unreleased liens. Each defect type has specific curative actions available under Texas law. The title opinion process requires identifying, classifying, and recommending curative action for each defect.",
        key_factors=["defect_type", "severity", "cure_method", "estimated_cure_timeline", "impact_on_current_operations", "title_insurance_coverage"],
        primary_authority=["TX Property Code", "TX title examination standards", "Title Standards Joint Editorial Board"],
        cooldown_minutes=240,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Assignment Recording",
        category=AlertCategory.ASSIGNMENT_RECORDED,
        keywords=["assignment", "partial assignment", "overriding royalty", "ORRI", "carried interest"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="An assignment has been recorded affecting {property_id}. {assignment_type} from {assignor} to {assignee} covering {interest_description}. Division of interests should be updated.",
        reasoning_framework="Assignments of oil and gas interests come in many forms: full working interest assignments, partial interest assignments, ORRI assignments, and carved-out interests. Each type has different tax implications, operational responsibilities, and payment obligations. The recording of an assignment should trigger a review of the run sheet and division orders to ensure accurate payment distribution.",
        key_factors=["assignment_type", "interest_conveyed", "effective_date", "retained_interests", "proportionate_reduction_clause", "depth_limitations"],
        primary_authority=["TX Property Code Ch. 5", "TX Natural Resources Code", "Assignment-specific terms"],
        instrument_types=["ASSIGNMENT", "PARTIAL_ASSIGNMENT", "ORRI_ASSIGNMENT"],
        cooldown_minutes=60,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Division Order Change",
        category=AlertCategory.DIVISION_ORDER_CHANGE,
        keywords=["division order", "decimal change", "interest change", "DO revision", "revenue distribution"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Division order change notification for {property_id}. Operator {operator} has issued revised division orders with decimal interest changes. New interest: {new_decimal}. Previous: {old_decimal}. Review and verification required before signing.",
        reasoning_framework="Division order changes directly affect revenue distribution. Under TX Natural Resources Code Sec. 91.402, division orders are binding on payment obligations but do not establish legal title. Interest owners are not required to sign division orders to receive payment. Changes should be verified against the title opinion and run sheet before acceptance. Discrepancies may indicate title changes the interest owner is unaware of or operator errors.",
        key_factors=["previous_decimal", "new_decimal", "change_reason", "title_opinion_match", "operator_explanation", "signing_deadline"],
        primary_authority=["TX Natural Resources Code Sec. 91.402", "TX division order statute"],
        cooldown_minutes=720,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Well Completion Notice",
        category=AlertCategory.WELL_COMPLETION,
        keywords=["completion", "W-2", "initial production", "IP", "completed", "first production"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Well completion reported: {well_name} ({api_number}) completed in {formation} with IP rate of {ip_rate}. RRC Form W-2 filed by {operator}. This triggers production reporting obligations and initial royalty payment timelines.",
        reasoning_framework="Well completion is a milestone event that transforms a drilling permit into a producing property. The completion report (W-2) provides formation details, completion method, initial production rates, and perforated intervals. Completion triggers: (1) 120-day clock for first royalty payment, (2) Production reporting obligations, (3) Lease-holding-by-production status, (4) Offset obligation evaluation for neighboring leases.",
        key_factors=["completion_date", "formation", "completion_method", "ip_oil_rate", "ip_gas_rate", "perforated_intervals", "offset_obligations_triggered"],
        primary_authority=["RRC Form W-2 requirements", "16 TAC Sec. 3.16", "TX Natural Resources Code Sec. 91.402"],
        instrument_types=["W-2", "COMPLETION_REPORT"],
        cooldown_minutes=120,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Spacing Order Detection",
        category=AlertCategory.SPACING_ORDER,
        keywords=["spacing", "density", "W-1X", "exception", "rule 37", "rule 38", "proration unit"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Spacing or density exception filed in {county} County for {formation}. Operator {operator} seeks {exception_type} for {well_name}. This may affect offset obligations and drainage patterns for monitored properties.",
        reasoning_framework="Spacing rules (Statewide Rules 37 and 38) govern well density and location within proration units. Exceptions allow wells closer to property lines or at higher density than standard rules permit. Spacing exceptions near monitored properties may indicate drainage risk or development intensity changes. Monitor for both the application and the final order.",
        key_factors=["rule_type", "exception_requested", "proposed_location", "distance_to_boundaries", "affected_tracts", "drainage_risk"],
        primary_authority=["16 TAC Sec. 3.37 (Rule 37)", "16 TAC Sec. 3.38 (Rule 38)", "RRC spacing procedures"],
        instrument_types=["SPACING_ORDER", "EXCEPTION_ORDER"],
        cooldown_minutes=240,
        confidence=ConfidenceLevel.DEFENSIBLE,
    ),
    DoctrineBlock(
        topic="Force Majeure Declaration",
        category=AlertCategory.FORCE_MAJEURE,
        keywords=["force majeure", "impossibility", "pandemic", "hurricane", "act of god", "supply chain"],
        severity_default=AlertSeverity.HIGH,
        conclusion_template="Force majeure declaration by {operator} affecting {property_id}. Declared event: {event_type}. This may toll lease obligations, suspend drilling requirements, or excuse performance under existing contracts. Duration: {estimated_duration}.",
        reasoning_framework="Force majeure clauses in oil and gas leases excuse performance when extraordinary events beyond the lessee's control prevent operations. Common triggering events include natural disasters, pandemics, government orders, equipment failures beyond reasonable control, and market disruptions. The clause must be specifically invoked, the event must be causally connected to the non-performance, and the lessee must demonstrate reasonable efforts to mitigate. Track the declaration, verify the triggering event, and monitor for expiration of the force majeure period.",
        key_factors=["triggering_event", "causal_connection", "mitigation_efforts", "lease_clause_language", "duration_estimate", "affected_obligations"],
        primary_authority=["TX contract law force majeure principles", "Virginia Power Energy Mktg v. Apache Corp. (2012)", "Lease-specific force majeure clauses"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
    DoctrineBlock(
        topic="Regulatory Change Detection",
        category=AlertCategory.REGULATORY_CHANGE,
        keywords=["regulation", "rule change", "new rule", "amendment", "effective date", "RRC rule", "TCEQ rule"],
        severity_default=AlertSeverity.MEDIUM,
        conclusion_template="Regulatory change detected: {agency} has {action_type} {rule_reference} effective {effective_date}. This change affects {impact_area} and may require compliance adjustments for monitored properties.",
        reasoning_framework="Regulatory changes at the state (RRC, TCEQ, GLO) and federal (EPA, BLM, FERC) level can create new compliance obligations, alter permitting requirements, change reporting deadlines, or affect operational practices. Track proposed rules through final adoption, monitor effective dates, and assess impact on monitored properties and operations. New regulations may require capital expenditure for compliance equipment, operational procedure changes, or additional reporting.",
        key_factors=["agency", "rule_reference", "change_type", "effective_date", "compliance_deadline", "estimated_compliance_cost", "affected_operations"],
        primary_authority=["TX Administrative Procedure Act", "16 TAC (RRC rules)", "30 TAC (TCEQ rules)", "Federal Register"],
        cooldown_minutes=1440,
        confidence=ConfidenceLevel.AGGRESSIVE,
    ),
]

# Build keyword index for fast lookup
_KEYWORD_INDEX: Dict[str, List[int]] = defaultdict(list)
for _i, _d in enumerate(DOCTRINE_CACHE):
    for _kw in _d.keywords:
        _KEYWORD_INDEX[_kw.lower()].append(_i)


# ═══════════════════════════════════════════════════════════════
# TIE-6: SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════

_NORMALIZATION_MAP: Dict[str, str] = {
    "mineral deed": "MINERAL_DEED", "royalty deed": "ROYALTY_DEED",
    "oil gas lease": "OIL_GAS_LEASE", "ogl": "OIL_GAS_LEASE",
    "dot": "DEED_OF_TRUST", "deed of trust": "DEED_OF_TRUST",
    "wd": "WARRANTY_DEED", "warranty deed": "WARRANTY_DEED",
    "swd": "SPECIAL_WARRANTY_DEED", "qcd": "QUIT_CLAIM",
    "aoh": "AFFIDAVIT_OF_HEIRSHIP", "affidavit of heirship": "AFFIDAVIT_OF_HEIRSHIP",
    "roi": "RELEASE_OF_LIEN", "release": "RELEASE_OF_LIEN",
    "assignment": "ASSIGNMENT", "partial assignment": "PARTIAL_ASSIGNMENT",
    "p-4": "P-4", "p4": "P-4", "w-1": "W-1", "w1": "W-1",
    "w-2": "W-2", "w2": "W-2", "w-3a": "W-3A", "w3a": "W-3A",
    "plugging": "PLUGGING_NOTICE", "plug and abandon": "PLUGGING_NOTICE",
    "p&a": "PLUGGING_NOTICE", "mechanic's lien": "MECHANICS_LIEN",
    "mechanics lien": "MECHANICS_LIEN", "tax lien": "TAX_LIEN",
    "judgment lien": "JUDGMENT_LIEN", "lis pendens": "LIS_PENDENS",
    "pooling": "POOLING_ORDER", "force pooling": "POOLING_ORDER",
    "unitization": "UNIT_AGREEMENT", "unit agreement": "UNIT_AGREEMENT",
    "spacing": "SPACING_ORDER", "rule 37": "RULE_37_EXCEPTION",
    "rule 38": "RULE_38_EXCEPTION", "force majeure": "FORCE_MAJEURE",
    "shut-in": "SHUT_IN", "shut in": "SHUT_IN",
    "completion": "COMPLETION", "ip": "INITIAL_PRODUCTION",
    "division order": "DIVISION_ORDER", "do": "DIVISION_ORDER",
}


def normalize_term(raw: str) -> str:
    """Normalize domain-specific terms to canonical form."""
    lower = raw.strip().lower()
    return _NORMALIZATION_MAP.get(lower, raw.upper().replace(" ", "_"))


# ═══════════════════════════════════════════════════════════════
# TIE-4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════

AUTHORITY_WEIGHTS: Dict[str, float] = {
    "TX_STATUTE": 1.0, "TX_ADMIN_CODE": 0.95, "RRC_RULE": 0.90,
    "CASE_LAW_TX_SUPREME": 0.95, "CASE_LAW_TX_APPEALS": 0.85,
    "CASE_LAW_FEDERAL": 0.80, "INDUSTRY_STANDARD": 0.65,
    "OPERATOR_PRACTICE": 0.50, "MARKET_DATA": 0.60,
}


def compute_authority_score(authorities: List[str]) -> float:
    """Score the authority backing of an alert based on source hierarchy."""
    if not authorities:
        return 0.3
    scores = []
    for auth in authorities:
        best = 0.4
        auth_lower = auth.lower()
        if "tx" in auth_lower and ("code" in auth_lower or "sec." in auth_lower):
            best = max(best, AUTHORITY_WEIGHTS["TX_STATUTE"])
        elif "tac" in auth_lower or "16 tac" in auth_lower:
            best = max(best, AUTHORITY_WEIGHTS["TX_ADMIN_CODE"])
        elif "rrc" in auth_lower or "statewide rule" in auth_lower:
            best = max(best, AUTHORITY_WEIGHTS["RRC_RULE"])
        elif "v." in auth_lower or "in re" in auth_lower:
            if "tex." in auth_lower and "app" not in auth_lower:
                best = max(best, AUTHORITY_WEIGHTS["CASE_LAW_TX_SUPREME"])
            elif "tex. app" in auth_lower:
                best = max(best, AUTHORITY_WEIGHTS["CASE_LAW_TX_APPEALS"])
            else:
                best = max(best, AUTHORITY_WEIGHTS["CASE_LAW_FEDERAL"])
        scores.append(best)
    return round(sum(scores) / len(scores), 3) if scores else 0.3


# ═══════════════════════════════════════════════════════════════
# TIE-5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════

def stratify_confidence(authority_score: float, data_completeness: float, rule_match_quality: float) -> ConfidenceLevel:
    """Assign confidence level based on authority, data, and match quality."""
    combined = (authority_score * 0.4) + (data_completeness * 0.35) + (rule_match_quality * 0.25)
    if combined >= 0.80:
        return ConfidenceLevel.DEFENSIBLE
    elif combined >= 0.60:
        return ConfidenceLevel.AGGRESSIVE
    elif combined >= 0.40:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════
# TIE-14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════

def score_fact_fragility(alert: AlertOutput, event: EventInput) -> Dict[str, Any]:
    """Score how fragile or robust the facts underlying an alert are."""
    verifiability = 0.5
    if event.instrument_number:
        verifiability += 0.3
    if event.county:
        verifiability += 0.1
    if event.effective_date:
        verifiability += 0.1

    recharacterization_risk = 0.3
    if alert.category in (AlertCategory.COMPETITIVE_ACTIVITY, AlertCategory.PRICE_THRESHOLD):
        recharacterization_risk = 0.6
    elif alert.category in (AlertCategory.PRODUCTION_CHANGE, AlertCategory.REGULATORY_CHANGE):
        recharacterization_risk = 0.5

    testimony_dependence = 0.2
    if not event.instrument_number and not event.effective_date:
        testimony_dependence = 0.7

    fragility_score = round(1.0 - (verifiability * 0.5 + (1 - recharacterization_risk) * 0.3 + (1 - testimony_dependence) * 0.2), 3)
    return {
        "fragility_score": fragility_score,
        "verifiability": round(verifiability, 3),
        "recharacterization_risk": round(recharacterization_risk, 3),
        "testimony_dependence": round(testimony_dependence, 3),
        "assessment": "ROBUST" if fragility_score < 0.3 else "MODERATE" if fragility_score < 0.6 else "FRAGILE",
    }


# ═══════════════════════════════════════════════════════════════
# TIE-16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════

def determinism_hash(content: str) -> str:
    """SHA-256 hash for reproducibility verification."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════
# TIE-11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════

class MetricsCollector:
    """Collects engine performance and alert generation metrics."""

    def __init__(self) -> None:
        self.queries_total: int = 0
        self.alerts_generated: int = 0
        self.alerts_by_category: Dict[str, int] = defaultdict(int)
        self.alerts_by_severity: Dict[str, int] = defaultdict(int)
        self.latencies: List[float] = []
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.errors: int = 0
        self.start_time: float = time.time()
        self.dedup_suppressed: int = 0

    def record_query(self, latency_ms: float) -> None:
        self.queries_total += 1
        self.latencies.append(latency_ms)
        if len(self.latencies) > 10000:
            self.latencies = self.latencies[-5000:]

    def record_alert(self, category: str, severity: str) -> None:
        self.alerts_generated += 1
        self.alerts_by_category[category] += 1
        self.alerts_by_severity[severity] += 1

    def record_cache_hit(self) -> None:
        self.cache_hits += 1

    def record_cache_miss(self) -> None:
        self.cache_misses += 1

    def record_dedup(self) -> None:
        self.dedup_suppressed += 1

    def record_error(self) -> None:
        self.errors += 1

    def snapshot(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_lat = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        p95_lat = sorted(self.latencies)[int(len(self.latencies) * 0.95)] if len(self.latencies) > 20 else avg_lat
        return {
            "queries_total": self.queries_total,
            "alerts_generated": self.alerts_generated,
            "alerts_by_category": dict(self.alerts_by_category),
            "alerts_by_severity": dict(self.alerts_by_severity),
            "dedup_suppressed": self.dedup_suppressed,
            "avg_latency_ms": round(avg_lat, 2),
            "p95_latency_ms": round(p95_lat, 2),
            "cache_hit_rate": round(self.cache_hits / max(self.cache_hits + self.cache_misses, 1), 3),
            "error_rate": round(self.errors / max(self.queries_total, 1), 4),
            "uptime_seconds": round(uptime, 1),
            "queries_per_hour": round(self.queries_total / max(uptime / 3600, 0.001), 1),
        }


METRICS = MetricsCollector()


# ═══════════════════════════════════════════════════════════════
# TIE-9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect drift in alert patterns and rule effectiveness over time."""

    def __init__(self) -> None:
        self.rule_trigger_counts: Dict[str, int] = defaultdict(int)
        self.rule_last_triggered: Dict[str, float] = {}
        self.baseline_distribution: Dict[str, float] = {}
        self.observations: List[Dict[str, Any]] = []

    def record_trigger(self, rule_id: str, category: str) -> None:
        self.rule_trigger_counts[rule_id] += 1
        self.rule_last_triggered[rule_id] = time.time()
        self.observations.append({"rule_id": rule_id, "category": category, "ts": time.time()})
        if len(self.observations) > 5000:
            self.observations = self.observations[-2500:]

    def set_baseline(self) -> None:
        total = sum(self.rule_trigger_counts.values()) or 1
        self.baseline_distribution = {k: v / total for k, v in self.rule_trigger_counts.items()}

    def detect_drift(self) -> List[Dict[str, Any]]:
        if not self.baseline_distribution or not self.rule_trigger_counts:
            return []
        total = sum(self.rule_trigger_counts.values()) or 1
        current = {k: v / total for k, v in self.rule_trigger_counts.items()}
        drifts = []
        for rule_id, baseline_pct in self.baseline_distribution.items():
            current_pct = current.get(rule_id, 0)
            delta = abs(current_pct - baseline_pct)
            if delta > 0.15:
                drifts.append({
                    "rule_id": rule_id,
                    "baseline_pct": round(baseline_pct, 4),
                    "current_pct": round(current_pct, 4),
                    "delta": round(delta, 4),
                    "direction": "INCREASED" if current_pct > baseline_pct else "DECREASED",
                })
        return drifts

    def report(self) -> Dict[str, Any]:
        return {
            "total_triggers": sum(self.rule_trigger_counts.values()),
            "rules_triggered": len(self.rule_trigger_counts),
            "drift_detected": self.detect_drift(),
            "stale_rules": [
                r for r, t in self.rule_last_triggered.items()
                if time.time() - t > 86400 * 7
            ],
        }


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════
# TIE-10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════

class CoverageMap:
    """Track which alert categories and rules have been triggered vs dormant."""

    def __init__(self) -> None:
        self.triggered: Dict[str, int] = defaultdict(int)
        self.all_categories = {c.value for c in AlertCategory}

    def record(self, category: str) -> None:
        self.triggered[category] += 1

    def gaps(self) -> List[str]:
        return sorted(self.all_categories - set(self.triggered.keys()))

    def report(self) -> Dict[str, Any]:
        coverage_pct = len(self.triggered) / max(len(self.all_categories), 1) * 100
        return {
            "total_categories": len(self.all_categories),
            "triggered_categories": len(self.triggered),
            "coverage_pct": round(coverage_pct, 1),
            "trigger_counts": dict(self.triggered),
            "untriggered_categories": self.gaps(),
        }


COVERAGE_MAP = CoverageMap()


# ═══════════════════════════════════════════════════════════════
# ALERT RULE ENGINE
# ═══════════════════════════════════════════════════════════════

class AlertRuleEngine:
    """Core rule-based alert generation engine with deduplication and batching."""

    def __init__(self) -> None:
        self.rules: List[AlertRule] = self._build_rules_from_doctrines()
        self.subscriptions: Dict[str, SubscriptionConfig] = {}
        self.alert_history: List[AlertOutput] = []
        self.dedup_cache: Dict[str, float] = {}
        self.cooldown_tracker: Dict[str, float] = {}
        self.pending_batch: Dict[str, List[AlertOutput]] = defaultdict(list)
        self.escalation_queue: List[Tuple[str, float]] = []

    def _build_rules_from_doctrines(self) -> List[AlertRule]:
        rules = []
        for i, doc in enumerate(DOCTRINE_CACHE):
            rules.append(AlertRule(
                rule_id=f"R{i+1:03d}_{doc.category.value}",
                category=doc.category,
                severity=doc.severity_default,
                description=doc.topic,
                condition_keywords=doc.keywords,
                instrument_types=doc.instrument_types,
                cooldown_minutes=doc.cooldown_minutes,
                enabled=True,
            ))
        return rules

    def _make_dedup_key(self, event: EventInput, rule: AlertRule) -> str:
        parts = [
            rule.category.value,
            event.property_id or "",
            event.instrument_number or "",
            event.county or "",
            event.grantor or "",
            event.grantee or "",
        ]
        raw = "|".join(parts)
        return hashlib.md5(raw.encode()).hexdigest()

    def _is_deduplicated(self, dedup_key: str, window_minutes: int) -> bool:
        if dedup_key in self.dedup_cache:
            last_time = self.dedup_cache[dedup_key]
            if time.time() - last_time < window_minutes * 60:
                return True
        return False

    def _is_cooled_down(self, rule_id: str, cooldown_minutes: int) -> bool:
        if rule_id in self.cooldown_tracker:
            last_fire = self.cooldown_tracker[rule_id]
            if time.time() - last_fire < cooldown_minutes * 60:
                return True
        return False

    def _match_event_to_rules(self, event: EventInput) -> List[Tuple[AlertRule, float]]:
        event_text = f"{event.event_type} {event.source} {event.metadata.get('description', '')}".lower()
        normalized_type = normalize_term(event.event_type)
        matches = []
        for rule in self.rules:
            if not rule.enabled:
                continue
            score = 0.0
            keyword_hits = 0
            for kw in rule.condition_keywords:
                if kw.lower() in event_text:
                    keyword_hits += 1
            if keyword_hits > 0:
                score += min(keyword_hits / len(rule.condition_keywords), 1.0) * 0.6
            if rule.instrument_types:
                for inst_type in rule.instrument_types:
                    if inst_type.upper() == normalized_type or inst_type.lower() in event_text:
                        score += 0.3
                        break
            cat_lower = rule.category.value.lower().replace("_", " ")
            if cat_lower in event_text or rule.category.value.lower() in event.event_type.lower():
                score += 0.3
            if score >= 0.3:
                matches.append((rule, min(score, 1.0)))
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _build_alert(self, event: EventInput, rule: AlertRule, match_score: float, doctrine: Optional[DoctrineBlock]) -> AlertOutput:
        title = f"[{rule.severity.value}] {rule.description}"
        if event.property_id:
            title += f" - {event.property_id}"
        desc_parts = [f"Alert triggered by {event.event_type} event from {event.source}."]
        if event.county:
            desc_parts.append(f"County: {event.county}, {event.state or 'TX'}.")
        if event.instrument_number:
            desc_parts.append(f"Instrument: #{event.instrument_number}.")
        if event.grantor:
            desc_parts.append(f"Grantor: {event.grantor}.")
        if event.grantee:
            desc_parts.append(f"Grantee: {event.grantee}.")
        if event.effective_date:
            desc_parts.append(f"Effective: {event.effective_date}.")
        description = " ".join(desc_parts)

        auth_score = 0.7
        if doctrine:
            auth_score = compute_authority_score(doctrine.primary_authority)
        confidence = stratify_confidence(auth_score, match_score, match_score)

        recommended = "Review the event details and take appropriate action."
        if doctrine and doctrine.resolution_strategy:
            recommended = doctrine.resolution_strategy

        dedup_key = self._make_dedup_key(event, rule)

        return AlertOutput(
            alert_id=f"ALR-{uuid.uuid4().hex[:12].upper()}",
            category=rule.category,
            severity=rule.severity,
            title=title,
            description=description,
            property_id=event.property_id,
            county=event.county,
            triggered_by=event.event_type,
            rule_id=rule.rule_id,
            confidence=confidence,
            recommended_action=recommended,
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=AlertStatus.PENDING,
            dedup_key=dedup_key,
            metadata={
                "match_score": round(match_score, 3),
                "authority_score": round(auth_score, 3),
                "source": event.source,
                "event_metadata": event.metadata,
            },
        )

    def evaluate_event(self, event: EventInput) -> List[AlertOutput]:
        """Evaluate an event against all rules and return generated alerts."""
        t0 = time.time()
        matches = self._match_event_to_rules(event)
        alerts: List[AlertOutput] = []
        for rule, score in matches:
            dedup_key = self._make_dedup_key(event, rule)
            if self._is_deduplicated(dedup_key, rule.dedup_window_minutes):
                METRICS.record_dedup()
                logger.debug(f"Dedup suppressed: {rule.rule_id} for event {event.event_type}")
                continue
            if self._is_cooled_down(rule.rule_id, rule.cooldown_minutes):
                logger.debug(f"Cooldown active: {rule.rule_id}")
                continue
            doctrine_idx = next(
                (i for i, d in enumerate(DOCTRINE_CACHE) if d.category == rule.category), None
            )
            doctrine = DOCTRINE_CACHE[doctrine_idx] if doctrine_idx is not None else None
            alert = self._build_alert(event, rule, score, doctrine)
            self.dedup_cache[dedup_key] = time.time()
            self.cooldown_tracker[rule.rule_id] = time.time()
            alerts.append(alert)
            self.alert_history.append(alert)
            METRICS.record_alert(rule.category.value, rule.severity.value)
            DRIFT_WATCHER.record_trigger(rule.rule_id, rule.category.value)
            COVERAGE_MAP.record(rule.category.value)
            logger.info(f"Alert generated: {alert.alert_id} [{alert.severity.value}] {alert.category.value}")

        if len(self.alert_history) > 10000:
            self.alert_history = self.alert_history[-5000:]
        self._clean_dedup_cache()

        elapsed = (time.time() - t0) * 1000
        METRICS.record_query(elapsed)
        return alerts

    def _clean_dedup_cache(self) -> None:
        now = time.time()
        expired = [k for k, v in self.dedup_cache.items() if now - v > 86400]
        for k in expired:
            del self.dedup_cache[k]

    def add_subscription(self, config: SubscriptionConfig) -> str:
        self.subscriptions[config.subscription_id] = config
        logger.info(f"Subscription added: {config.subscription_id} for user {config.user_id}")
        return config.subscription_id

    def remove_subscription(self, subscription_id: str) -> bool:
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            return True
        return False

    def get_alerts_for_user(self, user_id: str, limit: int = 50) -> List[AlertOutput]:
        user_subs = [s for s in self.subscriptions.values() if s.user_id == user_id and s.enabled]
        if not user_subs:
            return self.alert_history[-limit:]
        severity_order = {AlertSeverity.CRITICAL: 0, AlertSeverity.HIGH: 1, AlertSeverity.MEDIUM: 2, AlertSeverity.LOW: 3, AlertSeverity.INFO: 4}
        filtered = []
        for alert in reversed(self.alert_history):
            for sub in user_subs:
                if sub.categories and alert.category not in sub.categories:
                    continue
                if sub.property_ids and alert.property_id not in sub.property_ids:
                    continue
                if sub.counties and alert.county and alert.county not in sub.counties:
                    continue
                min_sev = severity_order.get(sub.min_severity, 4)
                alert_sev = severity_order.get(alert.severity, 4)
                if alert_sev > min_sev:
                    continue
                filtered.append(alert)
                break
            if len(filtered) >= limit:
                break
        return filtered

    def acknowledge_alert(self, alert_id: str) -> bool:
        for alert in self.alert_history:
            if alert.alert_id == alert_id:
                alert.status = AlertStatus.ACKNOWLEDGED
                return True
        return False

    def resolve_alert(self, alert_id: str) -> bool:
        for alert in self.alert_history:
            if alert.alert_id == alert_id:
                alert.status = AlertStatus.RESOLVED
                return True
        return False

    def check_escalations(self) -> List[AlertOutput]:
        """Find pending alerts past their escalation window."""
        now = time.time()
        escalated = []
        for alert in self.alert_history:
            if alert.status != AlertStatus.PENDING:
                continue
            alert_time = datetime.fromisoformat(alert.timestamp.replace("Z", "+00:00")).timestamp()
            rule = next((r for r in self.rules if r.rule_id == alert.rule_id), None)
            if rule and (now - alert_time) > rule.escalation_after_minutes * 60:
                alert.status = AlertStatus.ESCALATED
                alert.severity = AlertSeverity.CRITICAL
                escalated.append(alert)
                logger.warning(f"Alert escalated: {alert.alert_id}")
        return escalated

    def summary(self) -> Dict[str, Any]:
        status_counts: Dict[str, int] = defaultdict(int)
        for a in self.alert_history:
            status_counts[a.status.value] += 1
        return {
            "total_alerts": len(self.alert_history),
            "active_rules": sum(1 for r in self.rules if r.enabled),
            "subscriptions": len(self.subscriptions),
            "dedup_cache_size": len(self.dedup_cache),
            "status_breakdown": dict(status_counts),
        }


RULE_ENGINE = AlertRuleEngine()


# ═══════════════════════════════════════════════════════════════
# TIE-19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════

def decompose_event(event: EventInput) -> Dict[str, Any]:
    """Break a complex event into component alert categories and interaction edges."""
    event_text = f"{event.event_type} {json.dumps(event.metadata)}".lower()
    matched_categories: List[str] = []
    for doc in DOCTRINE_CACHE:
        hits = sum(1 for kw in doc.keywords if kw.lower() in event_text)
        if hits >= 2:
            matched_categories.append(doc.category.value)
    interactions = []
    interaction_map = {
        ("OWNERSHIP_CHANGE", "DIVISION_ORDER_CHANGE"): "Ownership transfer requires division order update",
        ("LEASE_EXPIRATION", "SHUT_IN"): "Shut-in well may fail to hold lease past primary term",
        ("VIOLATION_FILED", "PERMIT_EXPIRATION"): "Active violation may block permit renewal",
        ("BANKRUPTCY_FILED", "ROYALTY_PAYMENT"): "Bankruptcy stay may delay royalty payments",
        ("PLUGGING_NOTICE", "LEASE_EXPIRATION"): "Plugging sole well terminates lease",
        ("LIEN_FILED", "OWNERSHIP_CHANGE"): "Lien may cloud title for ownership transfer",
        ("PROBATE_FILED", "OWNERSHIP_CHANGE"): "Probate determines new ownership",
        ("ENVIRONMENTAL_RELEASE", "VIOLATION_FILED"): "Environmental release triggers regulatory violation",
        ("OPERATOR_CHANGE", "DIVISION_ORDER_CHANGE"): "New operator issues new division orders",
        ("FORCE_MAJEURE", "LEASE_EXPIRATION"): "Force majeure may toll lease obligations",
        ("POOLING", "SPACING_ORDER"): "Pooling and spacing often filed together",
    }
    for (cat_a, cat_b), desc in interaction_map.items():
        if cat_a in matched_categories and cat_b in matched_categories:
            interactions.append({"from": cat_a, "to": cat_b, "relationship": desc})
        elif cat_a in matched_categories or cat_b in matched_categories:
            if cat_a in matched_categories:
                interactions.append({"from": cat_a, "to": cat_b, "relationship": desc, "potential": True})
    return {
        "matched_categories": matched_categories,
        "category_count": len(matched_categories),
        "interactions": interactions,
        "complexity": "HIGH" if len(matched_categories) > 3 else "MEDIUM" if len(matched_categories) > 1 else "LOW",
    }


# ═══════════════════════════════════════════════════════════════
# TIE-20: DEEP ANALYSIS MODE
# ═══════════════════════════════════════════════════════════════

async def deep_analysis(event: EventInput, alerts: List[AlertOutput]) -> Dict[str, Any]:
    """Multi-source synthesis with full reasoning chain for complex events."""
    decomposition = decompose_event(event)
    fragility_scores = [score_fact_fragility(a, event) for a in alerts]
    authority_scores = []
    for a in alerts:
        doc = next((d for d in DOCTRINE_CACHE if d.category == a.category), None)
        if doc:
            authority_scores.append({
                "category": a.category.value,
                "authority_score": compute_authority_score(doc.primary_authority),
                "authorities": doc.primary_authority,
            })

    cloud_context: List[Dict[str, Any]] = []
    if CognitionCloudRetriever is not None:
        try:
            cloud = CognitionCloudRetriever()
            results = await asyncio.wait_for(
                cloud.retrieve_all(f"alert analysis {event.event_type} {event.county or ''}", category="alert_generation"),
                timeout=5.0,
            )
            if hasattr(results, "sources"):
                cloud_context = [{"source": s.source, "content": s.content[:300]} for s in results.sources[:5]]
        except Exception as exc:
            logger.warning(f"Cloud retrieval failed in deep analysis: {exc}")

    reasoning_chain = [
        f"1. Event received: {event.event_type} from {event.source}",
        f"2. Matched {len(alerts)} alert rules across {decomposition['category_count']} categories",
        f"3. Complexity assessment: {decomposition['complexity']}",
        f"4. Interaction edges found: {len(decomposition['interactions'])}",
        f"5. Authority backing: {len(authority_scores)} rules have statutory/case authority",
        f"6. Cloud knowledge sources consulted: {len(cloud_context)}",
    ]
    if decomposition["interactions"]:
        reasoning_chain.append("7. Cross-category interactions detected — cascading alert logic applied")

    return {
        "event_summary": f"{event.event_type} in {event.county or 'unknown'} county",
        "alerts_generated": len(alerts),
        "decomposition": decomposition,
        "fragility_analysis": fragility_scores,
        "authority_analysis": authority_scores,
        "cloud_context": cloud_context,
        "reasoning_chain": reasoning_chain,
        "recommendation": _synthesize_recommendation(alerts, decomposition),
        "hash": determinism_hash(json.dumps(reasoning_chain, sort_keys=True)),
    }


def _synthesize_recommendation(alerts: List[AlertOutput], decomposition: Dict[str, Any]) -> str:
    if not alerts:
        return "No alerts generated. Event does not match any active monitoring rules."
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    worst = min(alerts, key=lambda a: severity_order.get(a.severity.value, 5))
    parts = [f"Highest severity: {worst.severity.value} — {worst.title}."]
    if decomposition.get("interactions"):
        parts.append(f"{len(decomposition['interactions'])} cross-category interactions detected; review cascading effects.")
    if worst.severity in (AlertSeverity.CRITICAL, AlertSeverity.HIGH):
        parts.append("Immediate attention required. Recommend landman or legal review within 24 hours.")
    else:
        parts.append("Monitor situation. Schedule review within standard workflow cycle.")
    return " ".join(parts)


# ═══════════════════════════════════════════════════════════════
# TIE-1,2: THREE-LAYER RESPONSE + RESPONSE MODES
# ═══════════════════════════════════════════════════════════════

async def three_layer_response(request: QueryRequest) -> Dict[str, Any]:
    """Three-layer response: doctrine cache -> semantic retrieval -> deep analysis."""
    t0 = time.time()
    query_lower = request.query.lower()

    # Layer 1: Doctrine cache lookup (fast path, <200ms target)
    cache_results = []
    for doc in DOCTRINE_CACHE:
        hits = sum(1 for kw in doc.keywords if kw.lower() in query_lower)
        if hits >= 1:
            cache_results.append((doc, hits))
    cache_results.sort(key=lambda x: x[1], reverse=True)

    if cache_results:
        METRICS.record_cache_hit()
    else:
        METRICS.record_cache_miss()

    # Build event from query context for rule evaluation
    event = EventInput(
        event_type=request.context.get("event_type", request.query[:80]),
        source=request.context.get("source", "query"),
        property_id=request.property_id or request.context.get("property_id"),
        county=request.context.get("county"),
        instrument_number=request.context.get("instrument_number"),
        grantor=request.context.get("grantor"),
        grantee=request.context.get("grantee"),
        effective_date=request.context.get("effective_date"),
        metadata=request.context,
    )

    alerts = RULE_ENGINE.evaluate_event(event)

    # Layer 2: Semantic retrieval (cloud)
    cloud_knowledge: List[Dict[str, Any]] = []
    if CognitionCloudRetriever is not None and request.mode != ResponseMode.FAST:
        try:
            cloud = CognitionCloudRetriever()
            results = await asyncio.wait_for(
                cloud.retrieve_all(request.query, category="alert_generation"),
                timeout=5.0,
            )
            if hasattr(results, "sources"):
                cloud_knowledge = [{"source": s.source, "snippet": s.content[:200]} for s in results.sources[:5]]
        except Exception as exc:
            logger.warning(f"Cloud retrieval skipped: {exc}")

    # Layer 3: Deep analysis (MEMO mode only)
    deep = None
    if request.mode == ResponseMode.MEMO:
        deep = await deep_analysis(event, alerts)

    elapsed_ms = (time.time() - t0) * 1000

    # Format response per mode
    if request.mode == ResponseMode.FAST:
        response_text = _format_fast(alerts, cache_results)
    elif request.mode == ResponseMode.DEFENSE:
        response_text = _format_defense(alerts, cache_results, event)
    else:
        response_text = _format_memo(alerts, cache_results, event, deep)

    # Epistemic guardrails
    for phrase in BANNED_PHRASES:
        if phrase.lower() in response_text.lower():
            response_text = response_text.replace(phrase, "[CLAIM REMOVED — lacks epistemic basis]")

    content_hash = determinism_hash(response_text)

    result = {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "mode": request.mode.value,
        "zone": request.zone.value,
        "query": request.query,
        "response": response_text,
        "alerts": [a.dict() for a in alerts],
        "alert_count": len(alerts),
        "doctrine_matches": len(cache_results),
        "cloud_sources": len(cloud_knowledge),
        "cloud_knowledge": cloud_knowledge,
        "deep_analysis": deep,
        "confidence": alerts[0].confidence.value if alerts else ConfidenceLevel.DISCLOSURE.value,
        "determinism_hash": content_hash,
        "latency_ms": round(elapsed_ms, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # TIE-15: Audit trail
    _write_audit(request, result)
    return result


def _format_fast(alerts: List[AlertOutput], cache_hits: List[Tuple[DoctrineBlock, int]]) -> str:
    if not alerts:
        return "No alerts triggered for this event."
    lines = [f"{len(alerts)} alert(s) generated:"]
    for a in alerts[:10]:
        lines.append(f"  [{a.severity.value}] {a.category.value}: {a.title}")
    return "\n".join(lines)


def _format_defense(alerts: List[AlertOutput], cache_hits: List[Tuple[DoctrineBlock, int]], event: EventInput) -> str:
    parts = [f"ALERT ANALYSIS — {event.event_type}", f"Source: {event.source}", ""]
    if not alerts:
        parts.append("No alerts triggered. Event did not match any active monitoring rules.")
        return "\n".join(parts)
    parts.append(f"{len(alerts)} alert(s) triggered:\n")
    for a in alerts:
        parts.append(f"[{a.severity.value}] {a.category.value}")
        parts.append(f"  Rule: {a.rule_id}")
        parts.append(f"  Title: {a.title}")
        parts.append(f"  Confidence: {a.confidence.value}")
        parts.append(f"  Action: {a.recommended_action}")
        parts.append("")
    if cache_hits:
        parts.append("Authority Backing:")
        for doc, _ in cache_hits[:5]:
            for auth in doc.primary_authority[:2]:
                parts.append(f"  - {auth}")
    return "\n".join(parts)


def _format_memo(alerts: List[AlertOutput], cache_hits: List[Tuple[DoctrineBlock, int]], event: EventInput, deep: Optional[Dict[str, Any]]) -> str:
    parts = [
        "=" * 60,
        f"ALERT GENERATION MEMORANDUM",
        f"Engine: {ENGINE_ID} {ENGINE_NAME} v{ENGINE_VERSION}",
        f"Date: {datetime.utcnow().isoformat()}Z",
        f"Event: {event.event_type} | Source: {event.source}",
        "=" * 60,
        "",
        "I. EXECUTIVE SUMMARY",
        f"   {len(alerts)} alert(s) generated from {event.event_type} event.",
    ]
    if event.property_id:
        parts.append(f"   Property: {event.property_id}")
    if event.county:
        parts.append(f"   County: {event.county}, {event.state or 'TX'}")
    parts.append("")
    parts.append("II. ALERTS DETAIL")
    if not alerts:
        parts.append("   No alerts triggered.")
    for i, a in enumerate(alerts, 1):
        parts.append(f"   {i}. [{a.severity.value}] {a.category.value}")
        parts.append(f"      Rule: {a.rule_id}")
        parts.append(f"      Description: {a.description}")
        parts.append(f"      Confidence: {a.confidence.value}")
        parts.append(f"      Recommended Action: {a.recommended_action}")
        frag = score_fact_fragility(a, event)
        parts.append(f"      Fact Fragility: {frag['assessment']} (score={frag['fragility_score']})")
        parts.append("")
    if deep:
        parts.append("III. DEEP ANALYSIS")
        parts.append(f"   Complexity: {deep.get('decomposition', {}).get('complexity', 'N/A')}")
        for step in deep.get("reasoning_chain", []):
            parts.append(f"   {step}")
        parts.append("")
        parts.append(f"   Recommendation: {deep.get('recommendation', 'N/A')}")
        parts.append("")
    parts.append("IV. AUTHORITY")
    for doc, _ in cache_hits[:8]:
        parts.append(f"   Topic: {doc.topic}")
        for auth in doc.primary_authority:
            parts.append(f"     - {auth}")
    parts.append("")
    parts.append("V. DISCLOSURE")
    parts.append("   This analysis is generated by automated rule matching and should be")
    parts.append("   verified by qualified professionals before reliance. Alert confidence")
    parts.append("   levels reflect data quality and rule match strength, not legal certainty.")
    parts.append("=" * 60)
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════
# TIE-15: AUDIT TRAIL JSONL
# ═══════════════════════════════════════════════════════════════

def _write_audit(request: QueryRequest, result: Dict[str, Any]) -> None:
    try:
        record = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "engine_id": ENGINE_ID,
            "query": request.query[:200],
            "mode": request.mode.value,
            "zone": request.zone.value,
            "alert_count": result.get("alert_count", 0),
            "latency_ms": result.get("latency_ms", 0),
            "hash": result.get("determinism_hash", ""),
        }
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ═══════════════════════════════════════════════════════════════
# TIE-8: TELEMETRY
# ═══════════════════════════════════════════════════════════════

class TelemetryTracer:
    """Trace individual query execution for performance analysis."""

    def __init__(self) -> None:
        self.traces: List[Dict[str, Any]] = []

    def start_trace(self, query_id: str) -> Dict[str, Any]:
        trace = {"query_id": query_id, "start": time.time(), "spans": []}
        self.traces.append(trace)
        if len(self.traces) > 1000:
            self.traces = self.traces[-500:]
        return trace

    def add_span(self, trace: Dict[str, Any], name: str, duration_ms: float) -> None:
        trace["spans"].append({"name": name, "duration_ms": round(duration_ms, 2)})

    def close_trace(self, trace: Dict[str, Any]) -> None:
        trace["total_ms"] = round((time.time() - trace["start"]) * 1000, 2)

    def recent(self, n: int = 20) -> List[Dict[str, Any]]:
        return self.traces[-n:]


TELEMETRY = TelemetryTracer()


# ═══════════════════════════════════════════════════════════════
# TIE-7: VECTOR SEARCH (semantic fallback)
# ═══════════════════════════════════════════════════════════════

def keyword_vector_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Simple keyword-based vector search fallback over doctrine cache."""
    query_tokens = set(query.lower().split())
    scored = []
    for i, doc in enumerate(DOCTRINE_CACHE):
        doc_tokens = set()
        for kw in doc.keywords:
            doc_tokens.update(kw.lower().split())
        doc_tokens.update(doc.topic.lower().split())
        overlap = len(query_tokens & doc_tokens)
        if overlap > 0:
            score = overlap / max(len(query_tokens), 1)
            scored.append({"index": i, "topic": doc.topic, "category": doc.category.value, "score": round(score, 3)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ═══════════════════════════════════════════════════════════════
# TIE-13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════

def apply_zone_constraints(zone: AnalysisZone, alerts: List[AlertOutput]) -> List[AlertOutput]:
    """Filter and annotate alerts based on the analysis zone."""
    if zone == AnalysisZone.PLANNING:
        return [a for a in alerts if a.severity in (AlertSeverity.CRITICAL, AlertSeverity.HIGH, AlertSeverity.MEDIUM)]
    elif zone == AnalysisZone.AUDIT:
        for a in alerts:
            a.metadata["audit_zone"] = True
            a.metadata["requires_documentation"] = True
        return alerts
    return alerts


# ═══════════════════════════════════════════════════════════════
# TIE-17: FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks, {len(RULE_ENGINE.rules)} alert rules")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="Rule-based alert generation engine for document changes, filings, and significant events.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── TIE-12: Health Endpoint ───

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "active_rules": sum(1 for r in RULE_ENGINE.rules if r.enabled),
        "total_alerts": len(RULE_ENGINE.alert_history),
        "subscriptions": len(RULE_ENGINE.subscriptions),
        "metrics": METRICS.snapshot(),
        "uptime_seconds": round(time.time() - METRICS.start_time, 1),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/query")
async def query_endpoint(request: QueryRequest):
    """Primary query endpoint — three-layer response with alert generation."""
    logger.info(f"Query received: mode={request.mode.value} zone={request.zone.value} q={request.query[:80]}")
    result = await three_layer_response(request)
    return result


@app.post("/evaluate")
async def evaluate_event_endpoint(event: EventInput):
    """Evaluate a single event against all alert rules."""
    alerts = RULE_ENGINE.evaluate_event(event)
    return {
        "engine_id": ENGINE_ID,
        "event_type": event.event_type,
        "alerts": [a.dict() for a in alerts],
        "alert_count": len(alerts),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/evaluate/batch")
async def evaluate_batch_endpoint(events: List[EventInput]):
    """Evaluate multiple events in a single request."""
    all_alerts: List[Dict[str, Any]] = []
    for event in events:
        alerts = RULE_ENGINE.evaluate_event(event)
        all_alerts.extend([a.dict() for a in alerts])
    return {
        "engine_id": ENGINE_ID,
        "events_processed": len(events),
        "alerts": all_alerts,
        "total_alert_count": len(all_alerts),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/subscribe")
async def subscribe_endpoint(config: SubscriptionConfig):
    """Create or update an alert subscription."""
    sub_id = RULE_ENGINE.add_subscription(config)
    return {"subscription_id": sub_id, "status": "active"}


@app.delete("/subscribe/{subscription_id}")
async def unsubscribe_endpoint(subscription_id: str):
    removed = RULE_ENGINE.remove_subscription(subscription_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"subscription_id": subscription_id, "status": "removed"}


@app.get("/alerts")
async def get_alerts(user_id: Optional[str] = None, limit: int = Query(default=50, le=500)):
    """Get alerts, optionally filtered by user subscription."""
    if user_id:
        alerts = RULE_ENGINE.get_alerts_for_user(user_id, limit)
    else:
        alerts = RULE_ENGINE.alert_history[-limit:]
    return {
        "alerts": [a.dict() for a in alerts],
        "count": len(alerts),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    ok = RULE_ENGINE.acknowledge_alert(alert_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"alert_id": alert_id, "status": "acknowledged"}


@app.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    ok = RULE_ENGINE.resolve_alert(alert_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"alert_id": alert_id, "status": "resolved"}


@app.get("/alerts/escalated")
async def get_escalated():
    """Check for and return alerts that need escalation."""
    escalated = RULE_ENGINE.check_escalations()
    return {
        "escalated": [a.dict() for a in escalated],
        "count": len(escalated),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/rules")
async def list_rules():
    return {
        "rules": [r.dict() for r in RULE_ENGINE.rules],
        "count": len(RULE_ENGINE.rules),
    }


@app.post("/rules/{rule_id}/toggle")
async def toggle_rule(rule_id: str):
    for rule in RULE_ENGINE.rules:
        if rule.rule_id == rule_id:
            rule.enabled = not rule.enabled
            return {"rule_id": rule_id, "enabled": rule.enabled}
    raise HTTPException(status_code=404, detail="Rule not found")


@app.get("/search")
async def search_doctrines(q: str = Query(..., min_length=1), top_k: int = Query(default=5, le=20)):
    """Semantic search over doctrine cache."""
    results = keyword_vector_search(q, top_k)
    return {"query": q, "results": results, "count": len(results)}


@app.get("/decompose")
async def decompose_endpoint(event_type: str, metadata: str = "{}"):
    """Decompose an event into component categories and interactions."""
    event = EventInput(event_type=event_type, metadata=json.loads(metadata))
    result = decompose_event(event)
    return result


@app.get("/metrics")
async def metrics_endpoint():
    return METRICS.snapshot()


@app.get("/drift")
async def drift_endpoint():
    return DRIFT_WATCHER.report()


@app.get("/coverage")
async def coverage_endpoint():
    return COVERAGE_MAP.report()


@app.get("/telemetry")
async def telemetry_endpoint(n: int = Query(default=20, le=100)):
    return {"traces": TELEMETRY.recent(n)}


@app.get("/summary")
async def summary_endpoint():
    return {
        "engine": {"id": ENGINE_ID, "name": ENGINE_NAME, "version": ENGINE_VERSION},
        "rule_engine": RULE_ENGINE.summary(),
        "metrics": METRICS.snapshot(),
        "drift": DRIFT_WATCHER.report(),
        "coverage": COVERAGE_MAP.report(),
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
