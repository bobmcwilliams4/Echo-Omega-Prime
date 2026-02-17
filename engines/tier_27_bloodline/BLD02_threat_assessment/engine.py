"""
BLD02 — Threat Assessment Engine
ECHO OMEGA PRIME | Bloodline Tier | Authority 11.0 SOVEREIGN
Port: 8894 | Mode: DET (Detection)

Full TIE-20 compliant threat assessment engine for McWilliams Bloodline
and ECHO PRIME system protection. Covers PHYSICAL, CYBER, FINANCIAL,
LEGAL, REPUTATIONAL, INSIDER, SUPPLY_CHAIN, and GEOPOLITICAL domains.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import statistics
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "BLD02"
ENGINE_NAME = "Threat Assessment"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "BLD"
ENGINE_PORT = 8894
ENGINE_MODE = "DET"
AUTHORITY_LEVEL = 11.0
COMMANDER = "Bobby Don McWilliams II"

DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"
AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"

MAX_THREAT_HISTORY = 5000
DRIFT_WINDOW_SECONDS = 3600
HEALTH_CHECK_INTERVAL = 60

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>BLD02</cyan> | {message}",
    level="DEBUG",
)
logger.add(
    ENGINE_DIR / "bld02.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. ENUMS & PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ThreatDomain(str, Enum):
    """Eight threat domains assessed by BLD02."""
    PHYSICAL = "PHYSICAL"
    CYBER = "CYBER"
    FINANCIAL = "FINANCIAL"
    LEGAL = "LEGAL"
    REPUTATIONAL = "REPUTATIONAL"
    INSIDER = "INSIDER"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    GEOPOLITICAL = "GEOPOLITICAL"


class RiskLevel(str, Enum):
    """Composite risk classification."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    ELEVATED = "ELEVATED"
    MODERATE = "MODERATE"
    LOW = "LOW"
    MINIMAL = "MINIMAL"


class ConfidenceStratification(str, Enum):
    """Confidence tiers for threat assessments."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class ResponseMode(str, Enum):
    """Response formatting modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class PositionZone(str, Enum):
    """Analysis zone separation — never blur boundaries."""
    DETECTION = "DETECTION"
    ASSESSMENT = "ASSESSMENT"
    MITIGATION = "MITIGATION"


class ThreatIndicator(BaseModel):
    """Single threat signal from any source."""
    indicator_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    domain: ThreatDomain
    source: str
    description: str
    raw_score: float = Field(ge=0.0, le=10.0)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = Field(default_factory=dict)


class ThreatScoring(BaseModel):
    """Composite threat score using likelihood × impact × proximity."""
    likelihood: float = Field(ge=1.0, le=10.0, description="Probability of occurrence 1-10")
    impact: float = Field(ge=1.0, le=10.0, description="Severity if occurs 1-10")
    proximity: float = Field(ge=1.0, le=10.0, description="Temporal/spatial closeness 1-10")
    composite: float = Field(default=0.0, description="Computed: likelihood × impact × proximity / 100")
    risk_level: RiskLevel = RiskLevel.LOW
    color_code: str = "green"

    def compute(self) -> "ThreatScoring":
        """Compute composite score and classify risk."""
        self.composite = round((self.likelihood * self.impact * self.proximity) / 100.0, 3)
        if self.composite >= 7.0:
            self.risk_level = RiskLevel.CRITICAL
            self.color_code = "red"
        elif self.composite >= 5.0:
            self.risk_level = RiskLevel.HIGH
            self.color_code = "red"
        elif self.composite >= 3.5:
            self.risk_level = RiskLevel.ELEVATED
            self.color_code = "orange"
        elif self.composite >= 2.0:
            self.risk_level = RiskLevel.MODERATE
            self.color_code = "yellow"
        elif self.composite >= 1.0:
            self.risk_level = RiskLevel.LOW
            self.color_code = "green"
        else:
            self.risk_level = RiskLevel.MINIMAL
            self.color_code = "green"
        return self


class MitigationAction(BaseModel):
    """Recommended mitigation for a detected threat."""
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    priority: int = Field(ge=1, le=5, description="1=immediate, 5=low priority")
    description: str
    responsible_party: str = "ECHO PRIME"
    estimated_effort: str = "unknown"
    status: str = "PENDING"


class ThreatAssessmentRequest(BaseModel):
    """Input for /assess endpoint."""
    domain: ThreatDomain
    details: str
    indicators: list[ThreatIndicator] = Field(default_factory=list)
    mode: ResponseMode = ResponseMode.FAST
    context: dict[str, Any] = Field(default_factory=dict)


class ThreatAssessmentResponse(BaseModel):
    """Output from /assess endpoint."""
    assessment_id: str
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str
    domain: ThreatDomain
    scoring: ThreatScoring
    risk_level: RiskLevel
    confidence: ConfidenceStratification
    zone: PositionZone
    summary: str
    analysis: str
    mitigations: list[MitigationAction]
    doctrine_hits: list[str]
    determinism_hash: str
    response_mode: ResponseMode
    latency_ms: float
    authority_chain: list[str]


class DashboardEntry(BaseModel):
    """Single threat on dashboard."""
    assessment_id: str
    domain: ThreatDomain
    risk_level: RiskLevel
    composite_score: float
    summary: str
    timestamp: str
    color_code: str


class HealthResponse(BaseModel):
    """Health check response."""
    engine_id: str
    engine_name: str
    version: str
    status: str
    uptime_seconds: float
    total_assessments: int
    active_threats: int
    doctrine_count: int
    semantic_terms: int
    coverage_topics: int
    last_assessment: Optional[str]
    port: int
    tier: str
    mode: str
    authority: float


# ═══════════════════════════════════════════════════════════════════════════
# 2. DOCTRINE CACHE (TIE Component #3)
# ═══════════════════════════════════════════════════════════════════════════

class DoctrineBlock:
    """Single doctrine entry with full reasoning framework."""

    def __init__(
        self,
        topic: str,
        keywords: list[str],
        conclusion_template: str,
        reasoning_framework: str,
        key_factors: list[str],
        primary_authority: list[str],
        burden_holder: str,
        adversary_position: str,
        counter_arguments: list[str],
        resolution_strategy: str,
        entity_scope: str,
        confidence: ConfidenceStratification,
        domain: ThreatDomain,
        threat_indicators: list[str],
        mitigation_templates: list[str],
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.burden_holder = burden_holder
        self.adversary_position = adversary_position
        self.counter_arguments = counter_arguments
        self.resolution_strategy = resolution_strategy
        self.entity_scope = entity_scope
        self.confidence = confidence
        self.domain = domain
        self.threat_indicators = threat_indicators
        self.mitigation_templates = mitigation_templates

    def matches(self, query: str) -> tuple[bool, float]:
        """Check if query matches this doctrine. Returns (matched, relevance_score)."""
        query_lower = query.lower()
        hits = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        topic_match = 1.0 if self.topic.lower() in query_lower else 0.0
        score = (hits / max(len(self.keywords), 1)) * 0.7 + topic_match * 0.3
        return score > 0.15, round(score, 4)

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "confidence": self.confidence.value,
            "domain": self.domain.value,
            "key_factors_count": len(self.key_factors),
            "authority_count": len(self.primary_authority),
        }


def build_doctrine_cache() -> list[DoctrineBlock]:
    """Construct the full doctrine cache with real threat assessment frameworks."""
    doctrines: list[DoctrineBlock] = []

    # -- DOCTRINE 1: Physical Security Threat Assessment --
    doctrines.append(DoctrineBlock(
        topic="physical_security_threat",
        keywords=["physical", "security", "break-in", "intrusion", "surveillance", "trespass", "assault", "stalking"],
        conclusion_template=(
            "Physical security threats to the McWilliams Bloodline require layered defense: "
            "perimeter hardening, access control, surveillance systems, and personal security protocols. "
            "The Permian Basin operating environment presents unique physical risks including "
            "remote site vulnerability, equipment theft, and confrontation with hostile parties."
        ),
        reasoning_framework=(
            "Physical threat assessment follows the CARVER matrix methodology: "
            "Criticality (how vital is the target), Accessibility (how easy to reach), "
            "Recuperability (how quickly can target recover), Vulnerability (how susceptible "
            "to attack), Effect (what is the broader impact), Recognizability (how identifiable "
            "is the target). Each factor scored 1-10. Combined score determines threat priority. "
            "For personal protection: assess routine patterns, public exposure, travel routes, "
            "residence security, and known adversaries. For site security: perimeter integrity, "
            "lighting, camera coverage, access control logs, and guard force adequacy."
        ),
        key_factors=[
            "Perimeter integrity and access control effectiveness",
            "Surveillance system coverage gaps",
            "Personal routine predictability",
            "Known adversary capability and intent",
            "Remote site vulnerability in Permian Basin",
            "Local law enforcement response time",
            "Emergency communication reliability",
        ],
        primary_authority=[
            "ASIS International Physical Security Standards",
            "NIST SP 800-116 Guidelines for Physical Security",
            "CARVER Target Analysis Methodology (DoD)",
            "Texas Penal Code Ch. 9 — Justification of Force",
        ],
        burden_holder="Security Operations",
        adversary_position="Hostile actors may exploit routine patterns, remote locations, or lax access control",
        counter_arguments=[
            "Over-investment in physical security diverts resources from other threat domains",
            "Visible security measures may attract attention rather than deter",
            "Remote monitoring may fail during communication outages",
            "Personal security detail creates dependency and schedule constraints",
            "Insurance may cover most physical loss scenarios adequately",
        ],
        resolution_strategy=(
            "Implement layered defense-in-depth: outer perimeter detection, mid-zone delay mechanisms, "
            "inner zone hardened access. Randomize routines. Maintain emergency protocols. "
            "Coordinate with local law enforcement for rapid response agreements."
        ),
        entity_scope="McWilliams Bloodline, ECHO PRIME facilities, Permian Basin sites",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.PHYSICAL,
        threat_indicators=[
            "Unusual vehicles near residence or office",
            "Social media posts revealing location patterns",
            "Unfamiliar persons photographing facilities",
            "Access control system anomalies",
            "Increased crime reports in operational areas",
        ],
        mitigation_templates=[
            "Deploy additional cameras at identified blind spots",
            "Randomize daily travel routes and schedules",
            "Install perimeter intrusion detection at remote sites",
            "Conduct quarterly security audit of all facilities",
            "Establish panic button and rapid response protocol",
        ],
    ))

    # -- DOCTRINE 2: Cybersecurity Threat Framework --
    doctrines.append(DoctrineBlock(
        topic="cybersecurity_threat_framework",
        keywords=["cyber", "hack", "malware", "phishing", "ransomware", "breach", "exploit", "vulnerability", "network"],
        conclusion_template=(
            "Cybersecurity threats to ECHO PRIME infrastructure require continuous monitoring across "
            "all attack surfaces: network perimeter, endpoints, cloud services (Cloudflare Workers, R2, D1), "
            "credentials, and social engineering vectors. The NIST Cybersecurity Framework provides "
            "the authoritative structure: Identify, Protect, Detect, Respond, Recover."
        ),
        reasoning_framework=(
            "Cyber threat assessment uses the MITRE ATT&CK framework to map adversary tactics, "
            "techniques, and procedures (TTPs). For ECHO PRIME: primary attack surface includes "
            "26 Cloudflare Workers, 10 R2 buckets, 10 D1 databases, 20 KV namespaces, Vercel "
            "deployments, GitHub repositories, and the Commander's local infrastructure (4 monitors, "
            "multi-drive system, 37K+ tools). Assessment protocol: (1) Enumerate all assets and "
            "their exposure level, (2) Map known vulnerabilities per asset, (3) Assess adversary "
            "capability targeting those vulnerabilities, (4) Score likelihood and impact per "
            "attack vector, (5) Prioritize defenses by composite risk score. Critical attention "
            "to credential security — Master Vault contains 1,527 credentials."
        ),
        key_factors=[
            "Cloudflare Worker API key exposure risk",
            "Master Vault credential security (1,527 entries)",
            "Phishing targeting Commander's email accounts",
            "GitHub repository secrets scanning",
            "Local network segmentation adequacy",
            "Endpoint protection on development machines",
            "Cloud service misconfiguration risks",
            "Supply chain attacks via npm/pip dependencies",
        ],
        primary_authority=[
            "NIST Cybersecurity Framework v2.0",
            "MITRE ATT&CK Enterprise Matrix v14",
            "OWASP Top 10 (2025 Edition)",
            "CIS Critical Security Controls v8.1",
            "Cloudflare Security Best Practices",
        ],
        burden_holder="ECHO PRIME Security Operations",
        adversary_position="Attackers target the weakest link — often credentials, phishing, or misconfigured cloud services",
        counter_arguments=[
            "Over-restrictive security hampers development velocity",
            "Zero-trust architecture adds latency to every request",
            "Frequent password rotation causes weaker password selection",
            "Air-gapping critical systems limits operational capability",
            "Security monitoring generates alert fatigue if poorly tuned",
        ],
        resolution_strategy=(
            "Defense in depth: WAF at edge (Cloudflare), endpoint detection, credential rotation, "
            "MFA on all accounts, automated secret scanning in CI/CD, network segmentation, "
            "regular penetration testing, and incident response playbooks."
        ),
        entity_scope="ECHO PRIME infrastructure, all cloud services, local development environment",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Failed login attempts exceeding baseline by 3x",
            "Port scanning activity on local network",
            "Unusual outbound connections to unknown IPs",
            "New device connections not in asset inventory",
            "API key usage from unexpected geographic regions",
            "Dependency vulnerability alerts from npm/pip audit",
        ],
        mitigation_templates=[
            "Enable MFA on all Cloudflare, GitHub, Vercel accounts",
            "Run automated secret scanning on all repositories",
            "Deploy network intrusion detection on local subnet",
            "Rotate all API keys older than 90 days",
            "Conduct phishing awareness training quarterly",
            "Audit Cloudflare Worker permissions and bindings",
        ],
    ))

    # -- DOCTRINE 3: Financial Threat Detection --
    doctrines.append(DoctrineBlock(
        topic="financial_threat_detection",
        keywords=["financial", "fraud", "unauthorized", "transaction", "embezzlement", "theft", "payment", "invoice"],
        conclusion_template=(
            "Financial threats encompass unauthorized transactions, invoice fraud, identity theft, "
            "embezzlement, and market manipulation affecting Bloodline assets. Detection relies on "
            "pattern analysis: transaction velocity, amount anomalies, new payee verification, "
            "and geographic inconsistencies. Permian Basin operations add complexity with "
            "high-value equipment purchases, royalty payments, and joint venture accounting."
        ),
        reasoning_framework=(
            "Financial threat detection uses a multi-layered approach: (1) Transaction monitoring — "
            "flag amounts exceeding historical norms by >2 standard deviations, (2) Velocity analysis — "
            "detect unusual frequency of transactions within time windows, (3) Payee verification — "
            "new payees require secondary confirmation, (4) Geographic analysis — transactions from "
            "unexpected locations flagged for review, (5) Pattern matching — known fraud patterns "
            "(invoice splitting, round-number manipulation, weekend transactions) scored against "
            "activity stream. Oil & gas specific: watch for phantom invoices from non-existent vendors, "
            "royalty underpayment schemes, joint interest billing manipulation, and equipment "
            "procurement kickback patterns."
        ),
        key_factors=[
            "Transaction amount deviation from 90-day moving average",
            "New payee introduction without prior relationship",
            "Transaction velocity exceeding historical baseline",
            "Geographic origin inconsistency with known operations",
            "Round-number transactions suggesting manual manipulation",
            "Weekend or holiday transaction timing anomalies",
            "Invoice splitting to stay below approval thresholds",
            "Royalty payment discrepancies vs production reports",
        ],
        primary_authority=[
            "ACFE Fraud Examiners Manual (2025)",
            "FinCEN Suspicious Activity Report Guidelines",
            "AICPA AU-C 240 — Fraud in Financial Statement Audits",
            "Texas Business & Commerce Code Ch. 35 — Financial Crimes",
        ],
        burden_holder="Financial Operations / CFO function",
        adversary_position="Fraudsters exploit trust, complexity, and high transaction volumes to hide illicit activity",
        counter_arguments=[
            "Aggressive fraud detection creates false positives that slow legitimate business",
            "Dual-approval requirements delay time-sensitive transactions",
            "Vendor onboarding verification adds procurement cycle time",
            "Real-time monitoring requires significant infrastructure investment",
            "Over-scrutiny damages relationships with legitimate business partners",
        ],
        resolution_strategy=(
            "Implement tiered transaction monitoring: auto-approve below threshold, flag for review "
            "in middle tier, require dual approval above threshold. Maintain vendor whitelist with "
            "periodic re-verification. Reconcile royalty payments monthly against production data. "
            "Deploy anomaly detection using statistical baselines."
        ),
        entity_scope="All McWilliams financial accounts, business entities, royalty streams",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.FINANCIAL,
        threat_indicators=[
            "Transaction amount >3σ from 90-day mean",
            "New payee not in approved vendor list",
            "Multiple transactions just below approval threshold",
            "Royalty payment variance >5% from production estimate",
            "Wire transfer to previously unused bank",
            "Invoice from newly created entity (<90 days old)",
        ],
        mitigation_templates=[
            "Implement dual-approval for transactions above $10,000",
            "Run monthly reconciliation of royalty payments vs production",
            "Deploy automated vendor verification for new payees",
            "Set velocity alerts for >5 transactions per hour per account",
            "Quarterly review of all recurring payment relationships",
        ],
    ))

    # -- DOCTRINE 4: Legal Threat Assessment --
    doctrines.append(DoctrineBlock(
        topic="legal_threat_assessment",
        keywords=["legal", "lawsuit", "litigation", "regulatory", "compliance", "subpoena", "injunction", "statute"],
        conclusion_template=(
            "Legal threats to the McWilliams Bloodline include civil litigation, regulatory actions, "
            "contract disputes, mineral rights challenges, environmental compliance, and employment "
            "claims. Permian Basin operations face heightened regulatory scrutiny from the Texas "
            "Railroad Commission, EPA, and OSHA. Proactive legal posture requires continuous "
            "monitoring of pending actions and statute of limitations tracking."
        ),
        reasoning_framework=(
            "Legal threat assessment evaluates: (1) Active litigation — current cases, their stage, "
            "opposing counsel quality, and likely outcomes, (2) Regulatory exposure — pending "
            "regulatory changes, inspection history, compliance gaps, (3) Contract risks — "
            "upcoming renewals, unfavorable terms, counterparty creditworthiness, (4) Title risks — "
            "mineral rights chain of title gaps, competing claims, dormant interests, "
            "(5) Employment risks — wrongful termination exposure, FLSA compliance, non-compete "
            "enforceability. For each threat: assess probability of adverse outcome, potential "
            "financial exposure, timeline to resolution, and available defenses."
        ),
        key_factors=[
            "Active litigation count and aggregate exposure",
            "Statute of limitations approaching for potential claims",
            "Regulatory inspection results and deficiency notices",
            "Contract renewal dates and renegotiation leverage",
            "Mineral title chain completeness and competing claims",
            "Employment practice compliance with FLSA and OSHA",
            "Environmental permit status and compliance history",
        ],
        primary_authority=[
            "Texas Civil Practice & Remedies Code",
            "Texas Natural Resources Code — Mineral Interests",
            "Texas Railroad Commission Statewide Rules",
            "Federal EPA Clean Water Act / Clean Air Act",
            "Texas Labor Code and FLSA",
        ],
        burden_holder="Legal Counsel / Compliance Officer",
        adversary_position="Plaintiffs and regulators exploit documentation gaps, compliance failures, and statute deadlines",
        counter_arguments=[
            "Aggressive litigation posture may escalate costs beyond settlement value",
            "Over-compliance may exceed regulatory requirements unnecessarily",
            "Pre-emptive legal action may create adversarial relationships",
            "Title insurance may adequately cover mineral rights risks",
            "Regulatory lobbying may be more effective than defensive compliance",
        ],
        resolution_strategy=(
            "Maintain litigation tracking dashboard with exposure estimates. Calendar all statute "
            "deadlines with 180-day advance warning. Conduct annual compliance audits across all "
            "regulatory domains. Review all contracts 90 days before renewal. Ensure mineral title "
            "opinions are current within 2 years."
        ),
        entity_scope="McWilliams entities, Permian Basin operations, employment relationships",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.LEGAL,
        threat_indicators=[
            "New lawsuit filed against any McWilliams entity",
            "Regulatory notice of violation or deficiency",
            "Contract counterparty credit downgrade",
            "Competing mineral rights claim filed",
            "Employment complaint to EEOC or TWC",
            "Statute of limitations within 180 days of expiry",
        ],
        mitigation_templates=[
            "Engage litigation counsel for new filings within 48 hours",
            "Remediate regulatory deficiencies within notice period",
            "Renegotiate contracts with unfavorable terms 90 days before renewal",
            "Commission updated title opinion for disputed mineral interests",
            "Conduct annual employment practices audit",
        ],
    ))

    # -- DOCTRINE 5: Reputation Threat Monitoring --
    doctrines.append(DoctrineBlock(
        topic="reputation_threat_monitoring",
        keywords=["reputation", "brand", "media", "social", "public", "defamation", "slander", "libel", "review"],
        conclusion_template=(
            "Reputation threats can destroy business relationships, credit access, and community "
            "standing faster than any other threat domain. Monitoring requires continuous scanning "
            "of social media, news outlets, court records, and industry forums. For Permian Basin "
            "operations, community relations and environmental reputation are critical to maintaining "
            "operational license."
        ),
        reasoning_framework=(
            "Reputation threat assessment follows the PEST + Stakeholder model: (1) Political — "
            "alignment with local government, lobbying exposure, political donation scrutiny, "
            "(2) Economic — credit rating agencies, business partner perceptions, investor confidence, "
            "(3) Social — community sentiment, social media narrative, employee glassdoor reviews, "
            "(4) Technological — online presence integrity, SEO poisoning, deepfake risk. "
            "For each stakeholder group (employees, partners, regulators, community, media), "
            "assess current sentiment, trend direction, and trigger events that could shift "
            "perception. Weight by stakeholder influence on business outcomes."
        ),
        key_factors=[
            "Social media sentiment trend (30-day moving average)",
            "News coverage tone and volume",
            "Community relations score in operational areas",
            "Employee satisfaction indicators (Glassdoor, surveys)",
            "Business partner confidence signals",
            "Environmental incident history and public perception",
            "Political alignment and lobbying transparency",
        ],
        primary_authority=[
            "Crisis Communication Best Practices (PRSA)",
            "Texas Defamation Law — Civil Practice & Remedies Code Ch. 73",
            "FTC Endorsement Guidelines (16 CFR Part 255)",
            "SEC Regulation FD — Fair Disclosure",
        ],
        burden_holder="Communications / Public Relations",
        adversary_position="Competitors, disgruntled parties, and media may amplify negative narratives regardless of accuracy",
        counter_arguments=[
            "Monitoring social media may violate employee privacy expectations",
            "Responding to every negative post amplifies the criticism",
            "Aggressive reputation management may appear inauthentic",
            "Legal threats against critics can trigger Streisand effect",
            "Over-investment in reputation may neglect substantive improvements",
        ],
        resolution_strategy=(
            "Implement continuous reputation monitoring across social media, news, and review "
            "platforms. Maintain pre-approved crisis communication templates. Build community "
            "goodwill through transparent environmental stewardship and local investment. "
            "Address legitimate criticism substantively; ignore trolls."
        ),
        entity_scope="McWilliams personal reputation, business entity brands, ECHO PRIME public face",
        confidence=ConfidenceStratification.AGGRESSIVE,
        domain=ThreatDomain.REPUTATIONAL,
        threat_indicators=[
            "Negative social media post reaching >1000 engagements",
            "Negative news article in regional or industry publication",
            "Employee review below 3.0 on Glassdoor or Indeed",
            "Community complaint filed with local government",
            "Environmental incident reported to media",
        ],
        mitigation_templates=[
            "Deploy social media monitoring with sentiment alerts",
            "Prepare crisis communication templates for top 5 scenarios",
            "Engage community through environmental stewardship program",
            "Respond to legitimate Glassdoor reviews professionally",
            "Maintain media contact list for rapid response",
        ],
    ))

    # -- DOCTRINE 6: Insider Threat Detection --
    doctrines.append(DoctrineBlock(
        topic="insider_threat_detection",
        keywords=["insider", "employee", "trusted", "access", "exfiltration", "sabotage", "disgruntled", "privilege"],
        conclusion_template=(
            "Insider threats represent the most damaging and hardest-to-detect threat domain. "
            "Trusted insiders with legitimate access can exfiltrate data, sabotage systems, "
            "commit fraud, or enable external adversaries. Detection relies on behavioral "
            "analytics: access pattern deviations, data movement anomalies, and psychosocial "
            "indicators of disaffection."
        ),
        reasoning_framework=(
            "Insider threat detection uses the CERT Insider Threat Model (Carnegie Mellon): "
            "(1) Technical indicators — unusual access times, bulk data downloads, use of "
            "unauthorized storage media, access to systems outside job role, (2) Behavioral "
            "indicators — expressed dissatisfaction, workplace conflicts, financial stress, "
            "substance abuse, (3) Organizational indicators — recent performance issues, "
            "denied promotion, imminent termination, (4) Contextual indicators — access to "
            "critical systems, knowledge of security gaps, external affiliations. "
            "Scoring combines technical anomaly detection with human factors assessment. "
            "For ECHO PRIME: special attention to anyone with access to Master Vault, "
            "Cloudflare admin, or financial systems."
        ),
        key_factors=[
            "Access pattern deviation from 90-day behavioral baseline",
            "Data exfiltration indicators (bulk downloads, USB usage, email attachments)",
            "Privilege escalation attempts or unauthorized access requests",
            "Psychosocial risk factors (financial stress, workplace conflict)",
            "Temporal proximity to adverse employment action",
            "Access to critical systems (vault, cloud admin, financial)",
            "External communication with competitors or adversaries",
        ],
        primary_authority=[
            "CERT Insider Threat Best Practices (Carnegie Mellon SEI)",
            "NIST SP 800-53 Rev 5 — Personnel Security Controls",
            "Executive Order 13587 — Structural Reforms to Insider Threat",
            "NISPOM Chapter 13 — Insider Threat Programs",
        ],
        burden_holder="Security Operations / Human Resources",
        adversary_position="Insiders leverage trust and legitimate access to bypass external security controls",
        counter_arguments=[
            "Employee monitoring may damage morale and trust",
            "Behavioral profiling risks bias and discrimination",
            "False positives may unfairly target loyal employees",
            "Over-surveillance may violate privacy regulations",
            "Restricting access too aggressively impedes productivity",
        ],
        resolution_strategy=(
            "Implement least-privilege access model. Deploy user and entity behavior analytics "
            "(UEBA) to detect anomalies. Conduct background checks at hiring and periodically. "
            "Maintain anonymous reporting channels. Implement data loss prevention (DLP) controls. "
            "Provide employee assistance programs to address stressors."
        ),
        entity_scope="All personnel with access to ECHO PRIME systems or Bloodline assets",
        confidence=ConfidenceStratification.AGGRESSIVE,
        domain=ThreatDomain.INSIDER,
        threat_indicators=[
            "Login at unusual hours (outside normal pattern by >3 hours)",
            "Bulk download exceeding 10x daily average",
            "Access to systems outside assigned role",
            "USB device connection to sensitive workstation",
            "Resignation announcement followed by increased system access",
            "Multiple failed access attempts to restricted resources",
        ],
        mitigation_templates=[
            "Implement least-privilege access with quarterly review",
            "Deploy UEBA for automated anomaly detection",
            "Conduct exit interview and immediate access revocation on departure",
            "Encrypt all sensitive data at rest and in transit",
            "Maintain separation of duties for financial transactions",
        ],
    ))

    # -- DOCTRINE 7: Supply Chain Threat Analysis --
    doctrines.append(DoctrineBlock(
        topic="supply_chain_threat_analysis",
        keywords=["supply chain", "vendor", "supplier", "third-party", "dependency", "procurement", "contractor"],
        conclusion_template=(
            "Supply chain threats affect both physical operations (equipment, materials, services) "
            "and digital infrastructure (software dependencies, cloud providers, SaaS tools). "
            "Permian Basin operations depend on critical supply chains for drilling equipment, "
            "frac sand, water, and transportation. ECHO PRIME digital supply chain includes "
            "npm/pip packages, Cloudflare services, and API providers."
        ),
        reasoning_framework=(
            "Supply chain risk assessment evaluates: (1) Criticality — how dependent are operations "
            "on this supplier, (2) Substitutability — how quickly can an alternative be sourced, "
            "(3) Visibility — how much insight into supplier's security and stability, "
            "(4) Geographic risk — supplier location exposure to natural disasters, political "
            "instability, or sanctions, (5) Financial health — supplier's credit rating and "
            "bankruptcy risk. For digital supply chain: assess dependency tree depth, package "
            "maintainer trustworthiness, known vulnerability history, and update frequency. "
            "SolarWinds and Log4j demonstrated that supply chain compromises cascade catastrophically."
        ),
        key_factors=[
            "Single-source dependency for critical materials or services",
            "Supplier financial health and credit rating",
            "Geographic concentration of supply chain",
            "Software dependency vulnerability history",
            "Supplier security certification status (SOC2, ISO27001)",
            "Lead time sensitivity for critical components",
            "Contractual protections (SLAs, liability, insurance)",
        ],
        primary_authority=[
            "NIST SP 800-161 Rev 1 — Cyber Supply Chain Risk Management",
            "ISO 28000 — Supply Chain Security Management",
            "Executive Order 14028 — Improving Software Supply Chain Security",
            "CISA Supply Chain Risk Management Essentials",
        ],
        burden_holder="Procurement / IT Operations",
        adversary_position="Adversaries target the weakest link in the supply chain to gain access upstream",
        counter_arguments=[
            "Multi-vendor strategy increases procurement complexity and cost",
            "Vendor security audits strain small supplier relationships",
            "Maintaining strategic reserves ties up capital",
            "Software dependency pinning prevents security updates",
            "Geographic diversification may sacrifice cost efficiency",
        ],
        resolution_strategy=(
            "Identify all single-source dependencies and develop alternatives. Conduct annual "
            "vendor security assessments. Maintain strategic reserves for critical materials. "
            "Pin software dependencies with automated vulnerability scanning. Require SOC2 or "
            "equivalent for all SaaS providers handling sensitive data."
        ),
        entity_scope="All vendors, suppliers, contractors, and software dependencies",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.SUPPLY_CHAIN,
        threat_indicators=[
            "Critical supplier financial distress signals",
            "Known vulnerability in pinned dependency",
            "Supplier data breach notification",
            "Geographic disruption affecting supply route",
            "Unexpected price increase exceeding 20%",
        ],
        mitigation_templates=[
            "Develop secondary source for all single-source dependencies",
            "Run weekly npm/pip audit for vulnerability scanning",
            "Require SOC2 Type II for all SaaS vendors",
            "Maintain 30-day strategic reserve for critical materials",
            "Include security breach notification clause in all vendor contracts",
        ],
    ))

    # -- DOCTRINE 8: Geopolitical Risk for Permian Basin --
    doctrines.append(DoctrineBlock(
        topic="geopolitical_permian_basin_risk",
        keywords=["geopolitical", "permian", "oil", "regulation", "OPEC", "sanctions", "water", "environmental", "basin"],
        conclusion_template=(
            "Geopolitical risks affecting Permian Basin operations include oil price volatility "
            "driven by OPEC+ decisions, US energy policy shifts, water rights conflicts in "
            "West Texas, environmental regulatory tightening (methane rules, flaring restrictions), "
            "and international sanctions affecting equipment or technology supply chains. "
            "These macro forces directly impact royalty income, operational costs, and asset values."
        ),
        reasoning_framework=(
            "Geopolitical risk assessment for Permian Basin operations uses a multi-factor model: "
            "(1) Oil price risk — OPEC+ production decisions, US shale production growth rate, "
            "global demand trends (China, India), SPR policy, (2) Regulatory risk — EPA methane "
            "rules, Texas Railroad Commission well spacing/flaring rules, federal leasing policy, "
            "(3) Water risk — Ogallala Aquifer depletion rate, produced water disposal regulations, "
            "water recycling mandates, water rights adjudication, (4) Infrastructure risk — "
            "pipeline capacity constraints, export terminal access, midstream reliability, "
            "(5) Labor risk — skilled worker availability, immigration policy effects on oilfield "
            "labor supply, wage inflation. Each factor scored by probability of adverse change "
            "within 12 months and magnitude of impact on operations."
        ),
        key_factors=[
            "WTI crude price level and 90-day volatility",
            "OPEC+ production quota compliance and changes",
            "EPA methane emission regulation timeline",
            "Texas Railroad Commission permitting pace",
            "Ogallala Aquifer water level monitoring",
            "Permian Basin pipeline capacity utilization",
            "Skilled labor availability and wage trends",
            "Federal energy policy direction (leasing, subsidies)",
        ],
        primary_authority=[
            "US Energy Information Administration (EIA) Outlook",
            "Texas Railroad Commission Statewide Rules",
            "EPA Methane Emissions Reduction Program",
            "Texas Water Development Board — Ogallala Aquifer Reports",
            "Federal Reserve Beige Book — Dallas District Energy",
        ],
        burden_holder="Strategic Planning / Operations Management",
        adversary_position="Regulatory agencies, environmental groups, and OPEC+ pursue agendas that may conflict with Permian Basin operators",
        counter_arguments=[
            "Oil price hedging can mitigate price volatility at the cost of upside",
            "Regulatory compliance may become cost-prohibitive for marginal wells",
            "Water recycling technology investment may not pay back if regulations relax",
            "Pipeline constraints may ease as new capacity comes online",
            "Lobbying may be more effective than passive compliance",
        ],
        resolution_strategy=(
            "Maintain oil price hedge covering 60% of expected production for 12 months. "
            "Engage regulatory counsel for early warning on rule changes. Invest in water "
            "recycling to reduce aquifer dependency. Diversify midstream contracts to avoid "
            "single-pipeline risk. Participate in industry associations for collective advocacy."
        ),
        entity_scope="Permian Basin operations, mineral interests, royalty streams",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.GEOPOLITICAL,
        threat_indicators=[
            "WTI crude drops below $50/bbl",
            "OPEC+ announces production increase >1M bbl/day",
            "EPA finalizes new methane emission limits",
            "Water rights dispute filed in operational area",
            "Pipeline capacity utilization exceeds 95%",
            "Federal leasing moratorium proposed or enacted",
        ],
        mitigation_templates=[
            "Review and extend oil price hedge positions",
            "Engage regulatory counsel for EPA methane rule compliance plan",
            "Accelerate water recycling infrastructure deployment",
            "Secure firm pipeline capacity commitments",
            "Diversify revenue streams beyond Permian Basin production",
        ],
    ))

    # -- DOCTRINE 9: Credential Compromise Threat --
    doctrines.append(DoctrineBlock(
        topic="credential_compromise_threat",
        keywords=["credential", "password", "login", "authentication", "MFA", "token", "API key", "breach"],
        conclusion_template=(
            "With 1,527 credentials in the Master Vault, credential compromise represents a "
            "high-probability, high-impact threat. Attack vectors include phishing, credential "
            "stuffing from breach databases, session hijacking, and API key leakage in code "
            "repositories. Defense requires MFA everywhere, credential rotation, breach monitoring, "
            "and secret scanning."
        ),
        reasoning_framework=(
            "Credential threat assessment: (1) Enumerate all credential stores — Master Vault, "
            "browser saved passwords, .env files, CI/CD secrets, cloud provider consoles, "
            "(2) Assess each credential's exposure — age, complexity, reuse across services, "
            "breach database presence, (3) Evaluate access scope — what does compromise of this "
            "credential unlock, (4) MFA coverage — which accounts have MFA and which type, "
            "(5) Rotation compliance — which credentials exceed 90-day age threshold. "
            "Priority scoring: credential scope × exposure level × MFA absence = risk score."
        ),
        key_factors=[
            "Credential age distribution across Master Vault",
            "MFA enrollment percentage for critical accounts",
            "Credential reuse across multiple services",
            "Have I Been Pwned breach database matches",
            "API key exposure in code repositories",
            "Session token security (expiry, rotation, binding)",
        ],
        primary_authority=[
            "NIST SP 800-63B — Digital Identity Authentication",
            "OWASP Authentication Cheat Sheet",
            "CIS Controls v8.1 — Account Management",
            "FIDO Alliance Passkey Standards",
        ],
        burden_holder="ECHO PRIME Security Operations",
        adversary_position="Credential theft is the easiest path to system compromise — breached databases contain billions of credentials",
        counter_arguments=[
            "Frequent rotation leads to weaker passwords and post-it notes",
            "MFA adds friction that reduces productivity",
            "Hardware keys can be lost or forgotten",
            "Password managers introduce single-point-of-failure risk",
            "Biometric authentication raises privacy concerns",
        ],
        resolution_strategy=(
            "Enforce MFA on all accounts with privileged access. Run monthly breach checks "
            "via Have I Been Pwned API. Auto-rotate credentials older than 90 days. Implement "
            "secret scanning in all repositories. Migrate to passkeys where supported. "
            "Maintain Master Vault as single source of truth with encrypted backup to R2."
        ),
        entity_scope="All 1,527 credentials in Master Vault and any external credential stores",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Credential found in breach database",
            "API key older than 90 days without rotation",
            "Account without MFA holding privileged access",
            "Failed login spike from geographic anomaly",
            "Secret detected in git commit or log file",
        ],
        mitigation_templates=[
            "Enable MFA on all accounts flagged as no-MFA",
            "Rotate all credentials older than 90 days",
            "Deploy git pre-commit hooks for secret scanning",
            "Run Have I Been Pwned check against all credentials monthly",
            "Migrate to passkeys for supported services",
        ],
    ))

    # -- DOCTRINE 10: Ransomware Threat --
    doctrines.append(DoctrineBlock(
        topic="ransomware_threat",
        keywords=["ransomware", "encryption", "extortion", "backup", "recovery", "lockout", "crypto", "ransom"],
        conclusion_template=(
            "Ransomware is the highest-impact cyber threat — capable of encrypting all local data, "
            "disrupting operations, and demanding cryptocurrency payment. ECHO PRIME's multi-drive "
            "architecture (O:, F:, I:, J:, etc.) presents a large attack surface. Defense requires "
            "immutable backups, network segmentation, endpoint detection, and a tested recovery plan."
        ),
        reasoning_framework=(
            "Ransomware risk assessment: (1) Attack surface — count of endpoints, drives, network "
            "shares accessible from any single compromised node, (2) Backup integrity — are backups "
            "air-gapped or immutable? Can they be encrypted by ransomware? (3) Detection capability — "
            "can we detect file encryption patterns before critical mass? (4) Recovery time objective "
            "(RTO) — how fast can we restore operations from backup? (5) Business impact — what is "
            "the cost per hour of complete operational shutdown? For ECHO PRIME: R2 cloud backups "
            "provide off-site immutability. Local drives are vulnerable if not segmented."
        ),
        key_factors=[
            "Endpoint count and patch compliance level",
            "Backup immutability (R2 cloud vs local drives)",
            "Network segmentation between drives and systems",
            "Endpoint detection and response (EDR) deployment",
            "Recovery time objective and last tested restore",
            "Email gateway filtering effectiveness",
            "User security awareness training completion",
        ],
        primary_authority=[
            "CISA Ransomware Guide (2025)",
            "NIST SP 800-184 — Guide for Cybersecurity Event Recovery",
            "FBI IC3 Ransomware Response Guidance",
            "MS-ISAC Ransomware Prevention Best Practices",
        ],
        burden_holder="ECHO PRIME Security Operations",
        adversary_position="Ransomware operators use double extortion — encrypt data AND threaten to publish stolen data",
        counter_arguments=[
            "Air-gapped backups add operational complexity",
            "EDR solutions may conflict with development tools",
            "Network segmentation limits convenience of multi-drive access",
            "Paying ransom may be more cost-effective than recovery in some scenarios",
            "Cyber insurance may cover ransom payment and recovery costs",
        ],
        resolution_strategy=(
            "Maintain immutable backups on R2 with versioning enabled. Segment network so "
            "drive compromise cannot cascade. Deploy EDR on all endpoints. Test full restore "
            "quarterly. Maintain incident response plan with ransomware-specific playbook. "
            "NEVER pay ransom — it funds criminal enterprise and does not guarantee recovery."
        ),
        entity_scope="All ECHO PRIME infrastructure, all local drives, all cloud services",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Unusual file extension changes across multiple directories",
            "Mass file modification within short time window",
            "Ransom note file detected (README.txt with payment instructions)",
            "Endpoint detection alert for encryption behavior",
            "Outbound connection to known ransomware C2 infrastructure",
        ],
        mitigation_templates=[
            "Verify R2 backup versioning is enabled on all buckets",
            "Test full system restore from R2 backups quarterly",
            "Deploy EDR with ransomware-specific detection rules",
            "Segment network to prevent lateral movement between drives",
            "Conduct ransomware tabletop exercise with all stakeholders",
        ],
    ))

    # -- DOCTRINE 11: Social Engineering Threats --
    doctrines.append(DoctrineBlock(
        topic="social_engineering_threats",
        keywords=["social engineering", "phishing", "pretexting", "impersonation", "vishing", "smishing", "spear phishing"],
        conclusion_template=(
            "Social engineering bypasses technical controls by exploiting human psychology. "
            "The Commander's public profile and business prominence make him a high-value target "
            "for spear phishing, business email compromise (BEC), and impersonation attacks. "
            "Defenses require awareness training, verification protocols, and email authentication."
        ),
        reasoning_framework=(
            "Social engineering threat assessment: (1) Target profile — public information available "
            "about Commander (social media, court records, business filings, LinkedIn), (2) Attack "
            "vectors — email phishing, voice phishing (vishing), SMS phishing (smishing), physical "
            "impersonation, (3) Pretext scenarios — vendor payment change requests, executive "
            "impersonation, IT support calls, legal threats, (4) Current defenses — email filtering, "
            "DMARC/DKIM/SPF, employee training, verification procedures, (5) Historical incidents — "
            "any previous social engineering attempts and outcomes."
        ),
        key_factors=[
            "Commander's public information exposure level",
            "Email authentication (DMARC, DKIM, SPF) configuration",
            "Employee awareness training completion rate",
            "Verification protocol for payment change requests",
            "Phishing simulation test results",
            "BEC attempt detection capability",
        ],
        primary_authority=[
            "SANS Security Awareness Training Standards",
            "FBI IC3 Business Email Compromise Advisory",
            "DMARC.org Email Authentication Best Practices",
            "Social Engineering Framework (social-engineer.org)",
        ],
        burden_holder="All personnel / Security Awareness",
        adversary_position="Social engineers exploit urgency, authority, and familiarity to bypass rational decision-making",
        counter_arguments=[
            "Excessive verification protocols slow legitimate business communication",
            "Security awareness fatigue reduces training effectiveness over time",
            "Sophisticated AI-generated phishing is increasingly indistinguishable from legitimate email",
            "Verification callbacks may not reach legitimate contacts if phone systems are compromised",
            "Over-paranoia damages trust in business relationships",
        ],
        resolution_strategy=(
            "Implement DMARC reject policy on all domains. Conduct quarterly phishing simulations. "
            "Require out-of-band verification for any payment change requests. Train all personnel "
            "on pretexting recognition. Deploy AI-based email content analysis."
        ),
        entity_scope="All personnel, all communication channels",
        confidence=ConfidenceStratification.AGGRESSIVE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Email from spoofed domain visually similar to legitimate",
            "Urgent payment change request bypassing normal process",
            "Phone call requesting credential or system information",
            "SMS with link to unfamiliar domain",
            "Request citing Commander's authority without verification",
        ],
        mitigation_templates=[
            "Configure DMARC reject policy on all owned domains",
            "Conduct quarterly phishing simulation exercises",
            "Implement verbal callback for payment change requests",
            "Deploy AI email filtering for BEC detection",
            "Reduce Commander's public information footprint where possible",
        ],
    ))

    # -- DOCTRINE 12: Environmental Compliance Threat --
    doctrines.append(DoctrineBlock(
        topic="environmental_compliance_threat",
        keywords=["environmental", "EPA", "emission", "spill", "contamination", "compliance", "flaring", "methane", "water"],
        conclusion_template=(
            "Environmental compliance threats in the Permian Basin include methane emission "
            "regulations, flaring restrictions, produced water disposal rules, groundwater "
            "contamination liability, and endangered species habitat disruption. Non-compliance "
            "risks include fines ($50K+/day), operational shutdowns, and criminal liability."
        ),
        reasoning_framework=(
            "Environmental threat assessment for Permian Basin: (1) Current regulatory requirements — "
            "EPA methane rules, TCEQ air quality permits, Railroad Commission flaring limits, "
            "UIC Class II well permits, (2) Pending regulation changes — proposed methane fee "
            "($1,500/ton for 2026), potential WOTUS expansion, PFAS regulation applicability, "
            "(3) Compliance status — last inspection results, outstanding violations, corrective "
            "action plans, (4) Financial exposure — maximum fines, remediation cost estimates, "
            "natural resource damages, (5) Community and NGO pressure — active environmental "
            "campaigns, proximity to population centers."
        ),
        key_factors=[
            "Methane emission monitoring and reporting compliance",
            "Flaring volume vs Railroad Commission limits",
            "Produced water disposal well permit status",
            "Groundwater monitoring well results",
            "EPA inspection history and findings",
            "Pending environmental regulation effective dates",
            "Environmental NGO activity in operational area",
        ],
        primary_authority=[
            "EPA Methane Emissions Reduction Program (MERP)",
            "Texas Commission on Environmental Quality (TCEQ) Rules",
            "Texas Railroad Commission Statewide Rule 32 (Flaring)",
            "Safe Drinking Water Act — UIC Program",
            "Comprehensive Environmental Response (CERCLA/Superfund)",
        ],
        burden_holder="Environmental Compliance / Operations",
        adversary_position="EPA and environmental groups seek maximum enforcement to establish regulatory precedent",
        counter_arguments=[
            "Compliance investment may exceed penalty risk on probability-adjusted basis",
            "Voluntary emission reductions may not receive regulatory credit",
            "Technology for continuous methane monitoring is still maturing",
            "Produced water recycling may not be economically viable at current costs",
            "Industry-wide advocacy may be more effective than individual compliance efforts",
        ],
        resolution_strategy=(
            "Implement continuous methane monitoring (LDAR) at all facilities. Reduce flaring to "
            "below 98% gas capture rate. Maintain all permits current with 90-day renewal warning. "
            "Monitor EPA Federal Register for proposed rules. Engage environmental counsel for "
            "compliance gap analysis annually."
        ),
        entity_scope="All Permian Basin operational sites and facilities",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.GEOPOLITICAL,
        threat_indicators=[
            "EPA notice of violation received",
            "Methane emissions exceed permit limits",
            "Flaring volume exceeds Railroad Commission allowance",
            "Groundwater monitoring shows contamination indicators",
            "Environmental NGO files complaint or lawsuit",
        ],
        mitigation_templates=[
            "Deploy continuous methane monitoring at all facilities",
            "Implement vapor recovery to reduce flaring below limits",
            "Schedule annual environmental compliance audit",
            "Maintain environmental liability insurance coverage",
            "Engage community environmental advisory board",
        ],
    ))

    # -- DOCTRINE 13: DDoS / Service Disruption Threat --
    doctrines.append(DoctrineBlock(
        topic="ddos_service_disruption",
        keywords=["DDoS", "denial of service", "outage", "disruption", "availability", "downtime", "flooding"],
        conclusion_template=(
            "Distributed denial-of-service attacks targeting ECHO PRIME's 26 Cloudflare Workers "
            "and web properties (echo-op.com, barkinglot.org, etc.) could disrupt operations. "
            "Cloudflare's built-in DDoS protection provides a strong baseline, but application-layer "
            "attacks and resource exhaustion require additional defense layers."
        ),
        reasoning_framework=(
            "DDoS threat assessment: (1) Attack surface — enumerate all public-facing endpoints: "
            "26 Workers, 4 domains on Vercel, API endpoints, (2) Protection level — Cloudflare "
            "provides L3/L4 DDoS mitigation natively; L7 requires WAF rules, (3) Resource limits — "
            "Workers have 100K requests/day on free tier; paid tiers have higher limits but still "
            "finite, (4) Cascading failure risk — if one service goes down, what depends on it? "
            "(5) Recovery capability — how quickly can traffic be rerouted or services restored?"
        ),
        key_factors=[
            "Cloudflare DDoS protection tier and configuration",
            "Workers request rate limits and burst capacity",
            "Application-layer rate limiting implementation",
            "Service dependency chain and single points of failure",
            "DNS failover and multi-origin configuration",
            "Historical DDoS targeting in oil and gas sector",
        ],
        primary_authority=[
            "Cloudflare DDoS Protection Documentation",
            "NIST SP 800-61 Rev 2 — Incident Handling Guide",
            "CISA DDoS Mitigation Guidance",
            "AWS/Cloudflare DDoS Best Practices Whitepaper",
        ],
        burden_holder="ECHO PRIME Infrastructure Operations",
        adversary_position="DDoS-for-hire services make attacks cheap ($10-50) and accessible to anyone with a grudge",
        counter_arguments=[
            "Cloudflare's native protection handles most volumetric attacks automatically",
            "Over-aggressive rate limiting blocks legitimate users",
            "DDoS insurance may be more cost-effective than advanced mitigation",
            "Most DDoS attacks are short-lived and self-resolving",
            "Application-level defenses may introduce latency",
        ],
        resolution_strategy=(
            "Enable Cloudflare's highest available DDoS protection tier. Implement rate limiting "
            "on all API endpoints. Configure WAF rules for application-layer attack patterns. "
            "Set up health checks and automatic failover. Monitor traffic patterns for anomalies."
        ),
        entity_scope="All ECHO PRIME web properties and API endpoints",
        confidence=ConfidenceStratification.DEFENSIBLE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Request rate exceeding 10x normal baseline",
            "Traffic from unusual geographic distribution",
            "Repeated requests to computationally expensive endpoints",
            "Worker CPU time exceeding normal bounds",
            "Multiple 429/503 errors from rate limiting",
        ],
        mitigation_templates=[
            "Verify Cloudflare DDoS protection is at highest tier",
            "Implement per-IP rate limiting on all Workers",
            "Configure WAF rules for common L7 attack patterns",
            "Set up uptime monitoring with automatic alerting",
            "Create DDoS incident response playbook",
        ],
    ))

    # -- DOCTRINE 14: Intellectual Property Theft --
    doctrines.append(DoctrineBlock(
        topic="intellectual_property_theft",
        keywords=["IP", "intellectual property", "trade secret", "patent", "copyright", "code theft", "proprietary"],
        conclusion_template=(
            "ECHO PRIME's codebase (53,841+ lines across backbone engines, 427 total engines, "
            "37K+ tools, and proprietary algorithms) represents significant intellectual property. "
            "Theft vectors include unauthorized repository access, insider code copying, "
            "competitive intelligence gathering, and reverse engineering of deployed services."
        ),
        reasoning_framework=(
            "IP threat assessment: (1) Asset inventory — what proprietary code, algorithms, data, "
            "and processes exist, (2) Access control — who can access each asset and through what "
            "mechanisms, (3) Detection capability — can we detect unauthorized copying or access, "
            "(4) Legal protection — are trade secrets properly documented, NDAs in place, copyright "
            "registered, (5) Competitive landscape — who would benefit from stealing this IP and "
            "what is their capability?"
        ),
        key_factors=[
            "Code repository access control (GitHub private repos)",
            "Employee and contractor NDA coverage",
            "Trade secret documentation and marking",
            "Code obfuscation for deployed services",
            "Competitive intelligence targeting indicators",
            "Data loss prevention (DLP) for code repositories",
        ],
        primary_authority=[
            "Defend Trade Secrets Act (DTSA) 18 USC § 1836",
            "Texas Uniform Trade Secrets Act (TUTSA)",
            "Copyright Act 17 USC § 101-1332",
            "Economic Espionage Act 18 USC § 1831",
        ],
        burden_holder="Legal / Security Operations",
        adversary_position="Competitors and nation-state actors target proprietary algorithms and data that provide competitive advantage",
        counter_arguments=[
            "Over-restricting code access hampers developer productivity",
            "Trade secret claims require proving reasonable protection measures",
            "Open-source dependencies complicate proprietary claims",
            "Code obfuscation provides limited protection against determined adversaries",
            "Patent filing reveals more about IP than it protects",
        ],
        resolution_strategy=(
            "Mark all proprietary code with trade secret notices. Enforce NDAs with all personnel "
            "and contractors. Use private repositories with access logging. Deploy DLP for code "
            "repositories. Conduct quarterly IP inventory and access review."
        ),
        entity_scope="All ECHO PRIME source code, algorithms, data, and proprietary processes",
        confidence=ConfidenceStratification.AGGRESSIVE,
        domain=ThreatDomain.CYBER,
        threat_indicators=[
            "Bulk code download from repository",
            "Repository access from unauthorized IP",
            "Former employee accessing code after departure",
            "Competitor launching product with suspicious similarity",
            "Code snippets appearing in public repositories",
        ],
        mitigation_templates=[
            "Audit GitHub repository access permissions quarterly",
            "Enforce NDA execution before code access",
            "Deploy DLP monitoring on all code repositories",
            "Add trade secret headers to all proprietary source files",
            "Revoke all access immediately upon employee departure",
        ],
    ))

    # -- DOCTRINE 15: Economic Downturn / Market Risk --
    doctrines.append(DoctrineBlock(
        topic="economic_downturn_market_risk",
        keywords=["recession", "downturn", "market", "economic", "inflation", "interest rate", "credit", "liquidity"],
        conclusion_template=(
            "Economic downturn threatens Bloodline assets through reduced oil demand/prices, "
            "tightened credit markets, increased counterparty default risk, real estate value "
            "decline, and investment portfolio losses. Permian Basin operations are particularly "
            "sensitive to oil price cycles driven by macroeconomic conditions."
        ),
        reasoning_framework=(
            "Economic threat assessment: (1) Leading indicators — yield curve inversion, PMI "
            "contraction, unemployment claims trend, consumer confidence, (2) Oil price sensitivity — "
            "breakeven price vs current WTI, hedging coverage, (3) Credit exposure — debt "
            "maturity schedule, interest rate sensitivity, covenant compliance, (4) Counterparty "
            "risk — financial health of key business partners, joint venture partners, and "
            "customers, (5) Portfolio exposure — investment allocation, concentration risk, "
            "liquidity requirements."
        ),
        key_factors=[
            "WTI crude price vs operational breakeven",
            "Debt maturity schedule and refinancing risk",
            "Interest rate sensitivity on variable-rate debt",
            "Counterparty credit quality distribution",
            "Investment portfolio diversification level",
            "Cash reserve adequacy (months of operating expenses)",
            "Oil price hedge coverage ratio and duration",
        ],
        primary_authority=[
            "Federal Reserve Economic Data (FRED)",
            "EIA Short-Term Energy Outlook",
            "Dallas Fed Permian Basin Economic Indicators",
            "BLS Employment Situation Report",
        ],
        burden_holder="Financial Planning / Treasury",
        adversary_position="Economic cycles are inevitable; the question is timing, severity, and preparation",
        counter_arguments=[
            "Over-hedging sacrifices upside in recovery scenarios",
            "Excessive cash reserves earn below-inflation returns",
            "De-leveraging during growth phase limits expansion opportunities",
            "Diversification away from oil and gas may not be core competency",
            "Recession timing is impossible to predict accurately",
        ],
        resolution_strategy=(
            "Maintain 12-month operating expense cash reserve. Hedge 60% of expected production. "
            "Stress-test all debt covenants at $40 WTI. Diversify income streams. Monitor leading "
            "economic indicators monthly and adjust posture proactively."
        ),
        entity_scope="All McWilliams financial assets, business entities, investment portfolio",
        confidence=ConfidenceStratification.DISCLOSURE,
        domain=ThreatDomain.FINANCIAL,
        threat_indicators=[
            "Yield curve inversion for 3+ consecutive months",
            "PMI reading below 48 for 2+ consecutive months",
            "WTI crude decline exceeding 30% in 90 days",
            "Key counterparty credit downgrade",
            "Investment portfolio drawdown exceeding 15%",
        ],
        mitigation_templates=[
            "Review and extend oil price hedge positions",
            "Stress-test debt covenants at $40 WTI scenario",
            "Increase cash reserve to 12 months operating expenses",
            "Reduce concentration in any single counterparty above 10%",
            "Review investment portfolio for recession resilience",
        ],
    ))

    logger.info(f"Doctrine cache built: {len(doctrines)} blocks loaded")
    return doctrines


# ═══════════════════════════════════════════════════════════════════════════
# 3. SEMANTIC NORMALIZATION (TIE Component #6)
# ═══════════════════════════════════════════════════════════════════════════

class SemanticNormalizer:
    """Normalize threat-related terminology to canonical forms."""

    def __init__(self) -> None:
        self._mappings: dict[str, str] = {}
        self._load_semantic_dict()

    def _load_semantic_dict(self) -> None:
        if SEMANTIC_DICT_PATH.exists():
            try:
                raw = json.loads(SEMANTIC_DICT_PATH.read_text(encoding="utf-8"))
                self._mappings = raw.get("mappings", {})
                logger.info(f"Loaded {len(self._mappings)} semantic mappings")
            except Exception as exc:
                logger.warning(f"Failed to load semantic dict: {exc}")
                self._build_defaults()
        else:
            self._build_defaults()

    def _build_defaults(self) -> None:
        self._mappings = {
            "hack": "cyber_intrusion",
            "hacked": "cyber_intrusion",
            "hacking": "cyber_intrusion",
            "breach": "data_breach",
            "data leak": "data_breach",
            "data exposure": "data_breach",
            "phish": "phishing_attack",
            "phishing": "phishing_attack",
            "spear phish": "spear_phishing",
            "ransomware": "ransomware_attack",
            "ransom": "ransomware_attack",
            "crypto locker": "ransomware_attack",
            "malware": "malicious_software",
            "virus": "malicious_software",
            "trojan": "malicious_software",
            "worm": "malicious_software",
            "DDoS": "denial_of_service",
            "denial of service": "denial_of_service",
            "dos attack": "denial_of_service",
            "fraud": "financial_fraud",
            "embezzlement": "financial_fraud",
            "theft": "asset_theft",
            "stolen": "asset_theft",
            "burglary": "physical_intrusion",
            "break-in": "physical_intrusion",
            "trespass": "physical_intrusion",
            "lawsuit": "litigation_threat",
            "litigation": "litigation_threat",
            "sued": "litigation_threat",
            "regulatory action": "regulatory_threat",
            "compliance violation": "regulatory_threat",
            "fine": "regulatory_penalty",
            "penalty": "regulatory_penalty",
            "sanction": "regulatory_penalty",
            "defamation": "reputation_attack",
            "slander": "reputation_attack",
            "libel": "reputation_attack",
            "bad review": "reputation_damage",
            "negative press": "reputation_damage",
            "insider": "insider_threat",
            "disgruntled": "insider_threat",
            "sabotage": "insider_sabotage",
            "oil price": "commodity_price_risk",
            "crude price": "commodity_price_risk",
            "WTI": "commodity_price_risk",
            "OPEC": "geopolitical_oil_risk",
            "regulation": "regulatory_change",
            "EPA": "environmental_regulation",
            "methane": "emissions_regulation",
            "flaring": "emissions_regulation",
            "water rights": "water_resource_risk",
            "drought": "water_resource_risk",
            "pipeline": "infrastructure_risk",
            "supply chain": "supply_chain_risk",
            "vendor": "vendor_risk",
            "third party": "vendor_risk",
            "contractor": "vendor_risk",
        }
        logger.info(f"Built {len(self._mappings)} default semantic mappings")

    def normalize(self, text: str) -> str:
        """Normalize text using semantic dictionary. Returns canonical terms found."""
        text_lower = text.lower()
        found: list[str] = []
        for term, canonical in self._mappings.items():
            if term.lower() in text_lower:
                found.append(canonical)
        return ", ".join(sorted(set(found))) if found else text_lower

    def get_domain_from_text(self, text: str) -> ThreatDomain:
        """Infer the primary threat domain from text content."""
        text_lower = text.lower()
        domain_scores: dict[ThreatDomain, int] = {d: 0 for d in ThreatDomain}

        cyber_terms = ["cyber", "hack", "malware", "phishing", "ransomware", "breach", "network", "exploit",
                       "credential", "password", "DDoS", "vulnerability"]
        financial_terms = ["fraud", "transaction", "payment", "invoice", "embezzlement", "financial",
                          "unauthorized", "account", "bank", "wire"]
        physical_terms = ["physical", "break-in", "intrusion", "surveillance", "trespass", "assault",
                         "security camera", "perimeter"]
        legal_terms = ["lawsuit", "litigation", "regulatory", "compliance", "subpoena", "injunction",
                      "statute", "court", "judge"]
        reputation_terms = ["reputation", "brand", "media", "social", "defamation", "review", "public"]
        insider_terms = ["insider", "employee", "disgruntled", "sabotage", "exfiltration", "privilege"]
        supply_terms = ["supply chain", "vendor", "supplier", "third-party", "dependency", "procurement"]
        geo_terms = ["geopolitical", "permian", "oil price", "OPEC", "regulation", "water rights",
                    "environmental", "emission"]

        for term in cyber_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.CYBER] += 1
        for term in financial_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.FINANCIAL] += 1
        for term in physical_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.PHYSICAL] += 1
        for term in legal_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.LEGAL] += 1
        for term in reputation_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.REPUTATIONAL] += 1
        for term in insider_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.INSIDER] += 1
        for term in supply_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.SUPPLY_CHAIN] += 1
        for term in geo_terms:
            if term.lower() in text_lower:
                domain_scores[ThreatDomain.GEOPOLITICAL] += 1

        best_domain = max(domain_scores, key=lambda d: domain_scores[d])
        if domain_scores[best_domain] == 0:
            return ThreatDomain.CYBER  # default
        return best_domain

    @property
    def term_count(self) -> int:
        return len(self._mappings)


# ═══════════════════════════════════════════════════════════════════════════
# 4. VECTOR SEARCH STUB (TIE Component #7) — semantic fallback
# ═══════════════════════════════════════════════════════════════════════════

class VectorSearch:
    """Simple keyword-weighted search as vector fallback when doctrine cache misses."""

    def __init__(self, doctrines: list[DoctrineBlock]) -> None:
        self._doctrines = doctrines
        self._index: dict[str, list[int]] = {}
        self._build_index()

    def _build_index(self) -> None:
        for idx, doc in enumerate(self._doctrines):
            for kw in doc.keywords:
                kw_lower = kw.lower()
                if kw_lower not in self._index:
                    self._index[kw_lower] = []
                self._index[kw_lower].append(idx)
        logger.info(f"Vector index built: {len(self._index)} unique keywords")

    def search(self, query: str, top_k: int = 5) -> list[tuple[DoctrineBlock, float]]:
        """Search doctrines by keyword overlap. Returns (doctrine, score) pairs."""
        query_lower = query.lower()
        scores: dict[int, float] = {}
        for kw, indices in self._index.items():
            if kw in query_lower:
                for idx in indices:
                    scores[idx] = scores.get(idx, 0.0) + 1.0
        if not scores:
            return []
        max_score = max(scores.values())
        normalized = [(self._doctrines[idx], round(s / max_score, 4)) for idx, s in scores.items()]
        normalized.sort(key=lambda x: x[1], reverse=True)
        return normalized[:top_k]


# ═══════════════════════════════════════════════════════════════════════════
# 5. TELEMETRY (TIE Component #8)
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Full query tracing, latency tracking, and error domain monitoring."""

    def __init__(self) -> None:
        self._queries: list[dict[str, Any]] = []
        self._latencies: list[float] = []
        self._errors: list[dict[str, Any]] = []
        self._start_time = time.time()
        self._doctrine_hits: dict[str, int] = {}
        self._domain_counts: dict[str, int] = {d.value: 0 for d in ThreatDomain}

    def record_query(self, assessment_id: str, domain: str, latency_ms: float, success: bool,
                     doctrine_hits: list[str]) -> None:
        self._queries.append({
            "assessment_id": assessment_id,
            "domain": domain,
            "latency_ms": latency_ms,
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._latencies.append(latency_ms)
        if domain in self._domain_counts:
            self._domain_counts[domain] += 1
        for hit in doctrine_hits:
            self._doctrine_hits[hit] = self._doctrine_hits.get(hit, 0) + 1
        if not success:
            self._errors.append({
                "assessment_id": assessment_id,
                "domain": domain,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    @property
    def total_queries(self) -> int:
        return len(self._queries)

    @property
    def error_count(self) -> int:
        return len(self._errors)

    @property
    def avg_latency_ms(self) -> float:
        return round(statistics.mean(self._latencies), 2) if self._latencies else 0.0

    @property
    def p95_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        sorted_lat = sorted(self._latencies)
        idx = int(len(sorted_lat) * 0.95)
        return round(sorted_lat[min(idx, len(sorted_lat) - 1)], 2)

    @property
    def uptime_seconds(self) -> float:
        return round(time.time() - self._start_time, 2)

    def get_metrics(self) -> dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(self.total_queries, 1), 4),
            "avg_latency_ms": self.avg_latency_ms,
            "p95_latency_ms": self.p95_latency_ms,
            "uptime_seconds": self.uptime_seconds,
            "domain_distribution": dict(self._domain_counts),
            "top_doctrine_hits": dict(sorted(self._doctrine_hits.items(), key=lambda x: x[1], reverse=True)[:10]),
            "queries_per_minute": round(self.total_queries / max(self.uptime_seconds / 60, 1), 2),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 6. DRIFT WATCHER (TIE Component #9)
# ═══════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift — when assessments shift away from established patterns."""

    def __init__(self) -> None:
        self._baseline_scores: dict[str, list[float]] = {}
        self._drift_alerts: list[dict[str, Any]] = []

    def record_assessment(self, domain: str, composite_score: float) -> None:
        if domain not in self._baseline_scores:
            self._baseline_scores[domain] = []
        self._baseline_scores[domain].append(composite_score)
        self._check_drift(domain)

    def _check_drift(self, domain: str) -> None:
        scores = self._baseline_scores.get(domain, [])
        if len(scores) < 10:
            return
        recent = scores[-5:]
        historical = scores[:-5]
        recent_mean = statistics.mean(recent)
        hist_mean = statistics.mean(historical)
        hist_stdev = statistics.stdev(historical) if len(historical) > 1 else 1.0
        if hist_stdev == 0:
            hist_stdev = 0.1
        z_score = abs(recent_mean - hist_mean) / hist_stdev
        if z_score > 2.0:
            direction = "INCREASING" if recent_mean > hist_mean else "DECREASING"
            alert = {
                "domain": domain,
                "direction": direction,
                "z_score": round(z_score, 3),
                "recent_mean": round(recent_mean, 3),
                "historical_mean": round(hist_mean, 3),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self._drift_alerts.append(alert)
            logger.warning(f"DRIFT DETECTED in {domain}: {direction} (z={z_score:.2f})")

    @property
    def alerts(self) -> list[dict[str, Any]]:
        return list(self._drift_alerts)

    @property
    def alert_count(self) -> int:
        return len(self._drift_alerts)


# ═══════════════════════════════════════════════════════════════════════════
# 7. COVERAGE MAP (TIE Component #10)
# ═══════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Track which doctrines are triggered and which have gaps."""

    def __init__(self, doctrines: list[DoctrineBlock]) -> None:
        self._topics = {d.topic: 0 for d in doctrines}
        self._total_queries = 0
        self._uncovered_queries: list[str] = []

    def record_hit(self, topic: str) -> None:
        if topic in self._topics:
            self._topics[topic] += 1
        self._total_queries += 1

    def record_miss(self, query_snippet: str) -> None:
        self._uncovered_queries.append(query_snippet[:200])
        self._total_queries += 1
        if len(self._uncovered_queries) > 100:
            self._uncovered_queries = self._uncovered_queries[-100:]

    def get_coverage(self) -> dict[str, Any]:
        triggered = {k: v for k, v in self._topics.items() if v > 0}
        untriggered = [k for k, v in self._topics.items() if v == 0]
        return {
            "total_topics": len(self._topics),
            "triggered_count": len(triggered),
            "untriggered_count": len(untriggered),
            "coverage_pct": round(len(triggered) / max(len(self._topics), 1) * 100, 1),
            "triggered_topics": triggered,
            "untriggered_topics": untriggered,
            "total_queries": self._total_queries,
            "uncovered_queries": self._uncovered_queries[-20:],
        }


# ═══════════════════════════════════════════════════════════════════════════
# 8. METRICS COLLECTOR (TIE Component #11)
# ═══════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Aggregate metrics: latency stats, error rates, hit rates, queries/hour."""

    def __init__(self) -> None:
        self._hourly_counts: dict[str, int] = {}
        self._risk_level_dist: dict[str, int] = {level.value: 0 for level in RiskLevel}

    def record_assessment_risk(self, risk_level: RiskLevel) -> None:
        self._risk_level_dist[risk_level.value] += 1
        hour_key = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H")
        self._hourly_counts[hour_key] = self._hourly_counts.get(hour_key, 0) + 1

    def get_metrics(self) -> dict[str, Any]:
        return {
            "risk_level_distribution": dict(self._risk_level_dist),
            "hourly_query_counts": dict(sorted(self._hourly_counts.items())[-24:]),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 9. AUDIT TRAIL (TIE Component #15)
# ═══════════════════════════════════════════════════════════════════════════

class AuditTrail:
    """Append-only JSONL audit trail for forensic review."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def log_entry(self, entry: dict[str, Any]) -> None:
        entry["_audit_timestamp"] = datetime.now(timezone.utc).isoformat()
        try:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, default=str) + "\n")
        except Exception as exc:
            logger.error(f"Audit trail write failed: {exc}")

    def get_recent(self, count: int = 50) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            lines = self._path.read_text(encoding="utf-8").strip().split("\n")
            recent = lines[-count:]
            return [json.loads(line) for line in recent if line.strip()]
        except Exception as exc:
            logger.error(f"Audit trail read failed: {exc}")
            return []


# ═══════════════════════════════════════════════════════════════════════════
# 10. AUTHORITY HARDENING (TIE Component #4)
# ═══════════════════════════════════════════════════════════════════════════

class AuthorityHardening:
    """Hierarchical authority levels with weights and conflict resolution."""

    AUTHORITY_HIERARCHY: list[dict[str, Any]] = [
        {"level": 1, "source": "COMMANDER_DIRECT", "weight": 1.0, "description": "Direct order from Commander"},
        {"level": 2, "source": "NIST_FRAMEWORK", "weight": 0.95, "description": "NIST cybersecurity standards"},
        {"level": 3, "source": "FEDERAL_REGULATION", "weight": 0.90, "description": "Federal regulatory requirements"},
        {"level": 4, "source": "STATE_REGULATION", "weight": 0.85, "description": "Texas state regulations"},
        {"level": 5, "source": "INDUSTRY_STANDARD", "weight": 0.80, "description": "Industry best practices (MITRE, CIS, ASIS)"},
        {"level": 6, "source": "INTERNAL_POLICY", "weight": 0.75, "description": "ECHO PRIME internal policies"},
        {"level": 7, "source": "EXPERT_CONSENSUS", "weight": 0.65, "description": "Expert community consensus"},
        {"level": 8, "source": "HISTORICAL_PATTERN", "weight": 0.55, "description": "Historical threat pattern analysis"},
        {"level": 9, "source": "AI_INFERENCE", "weight": 0.45, "description": "AI-derived threat inference"},
    ]

    @classmethod
    def resolve_conflict(cls, sources: list[str]) -> dict[str, Any]:
        """When multiple authorities conflict, highest-weighted source wins."""
        matched = []
        for src in sources:
            for auth in cls.AUTHORITY_HIERARCHY:
                if auth["source"] == src:
                    matched.append(auth)
                    break
        if not matched:
            return {"source": "AI_INFERENCE", "weight": 0.45, "level": 9}
        matched.sort(key=lambda x: x["weight"], reverse=True)
        return matched[0]

    @classmethod
    def get_authority_chain(cls, sources: list[str]) -> list[str]:
        """Return ordered authority chain for given sources."""
        chain = []
        for auth in cls.AUTHORITY_HIERARCHY:
            if auth["source"] in sources:
                chain.append(f"L{auth['level']}: {auth['source']} (w={auth['weight']})")
        return chain if chain else [f"L9: AI_INFERENCE (w=0.45)"]


# ═══════════════════════════════════════════════════════════════════════════
# 11. FACT FRAGILITY SCORING (TIE Component #14)
# ═══════════════════════════════════════════════════════════════════════════

class FactFragility:
    """Score how fragile/reliable threat facts are."""

    @staticmethod
    def score(
        verifiability: float,
        source_independence: float,
        temporal_stability: float,
        corroboration_count: int,
    ) -> dict[str, Any]:
        """
        Score fact fragility on 0-1 scale (0 = solid, 1 = fragile).

        Args:
            verifiability: 0-1 how verifiable the fact is
            source_independence: 0-1 how independent sources are
            temporal_stability: 0-1 how stable the fact is over time
            corroboration_count: number of independent corroborating sources
        """
        corroboration_factor = min(corroboration_count / 5, 1.0)
        fragility = 1.0 - (
            verifiability * 0.3
            + source_independence * 0.25
            + temporal_stability * 0.25
            + corroboration_factor * 0.20
        )
        fragility = round(max(0.0, min(1.0, fragility)), 4)

        if fragility < 0.3:
            label = "SOLID"
        elif fragility < 0.5:
            label = "MODERATE"
        elif fragility < 0.7:
            label = "FRAGILE"
        else:
            label = "HIGHLY_FRAGILE"

        return {
            "fragility_score": fragility,
            "label": label,
            "components": {
                "verifiability": verifiability,
                "source_independence": source_independence,
                "temporal_stability": temporal_stability,
                "corroboration_count": corroboration_count,
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# 12. ZONED ANALYSIS (TIE Component #13)
# ═══════════════════════════════════════════════════════════════════════════

class ZonedAnalysis:
    """Enforce zone separation: DETECTION / ASSESSMENT / MITIGATION."""

    @staticmethod
    def classify_zone(query: str) -> PositionZone:
        query_lower = query.lower()
        mitigation_keywords = ["fix", "mitigate", "remediate", "patch", "resolve", "prevent", "defend",
                               "protect", "harden", "secure"]
        assessment_keywords = ["assess", "evaluate", "analyze", "score", "rate", "risk", "impact",
                               "likelihood", "severity"]
        detection_keywords = ["detect", "monitor", "alert", "scan", "identify", "discover", "find",
                             "indicator", "signal"]

        mitigation_hits = sum(1 for kw in mitigation_keywords if kw in query_lower)
        assessment_hits = sum(1 for kw in assessment_keywords if kw in query_lower)
        detection_hits = sum(1 for kw in detection_keywords if kw in query_lower)

        if mitigation_hits > assessment_hits and mitigation_hits > detection_hits:
            return PositionZone.MITIGATION
        if detection_hits > assessment_hits:
            return PositionZone.DETECTION
        return PositionZone.ASSESSMENT


# ═══════════════════════════════════════════════════════════════════════════
# 13. DETERMINISM HASH (TIE Component #16)
# ═══════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(data: dict[str, Any]) -> str:
    """Compute SHA-256 hash for reproducibility verification."""
    canonical = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# 14. MULTI-DOCTRINE DECOMPOSITION (TIE Component #19)
# ═══════════════════════════════════════════════════════════════════════════

class MultiDoctrineDecomposer:
    """Decompose complex threats into component doctrine categories with interaction DAG."""

    @staticmethod
    def decompose(details: str, matched_doctrines: list[DoctrineBlock]) -> dict[str, Any]:
        domains_involved = list(set(d.domain.value for d in matched_doctrines))
        categories = list(set(d.topic for d in matched_doctrines))

        interaction_edges: list[dict[str, str]] = []
        for i, d1 in enumerate(matched_doctrines):
            for d2 in matched_doctrines[i + 1:]:
                shared_keywords = set(d1.keywords) & set(d2.keywords)
                if shared_keywords:
                    interaction_edges.append({
                        "from": d1.topic,
                        "to": d2.topic,
                        "shared_keywords": list(shared_keywords),
                        "interaction_type": "keyword_overlap",
                    })
                if d1.domain == d2.domain:
                    interaction_edges.append({
                        "from": d1.topic,
                        "to": d2.topic,
                        "shared_keywords": [],
                        "interaction_type": "same_domain",
                    })

        return {
            "domains_involved": domains_involved,
            "categories": categories,
            "doctrine_count": len(matched_doctrines),
            "interaction_edges": interaction_edges,
            "complexity_score": round(
                len(matched_doctrines) * 0.3 + len(interaction_edges) * 0.5 + len(domains_involved) * 0.2, 2
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 15. DEEP ANALYSIS MODE (TIE Component #20)
# ═══════════════════════════════════════════════════════════════════════════

class DeepAnalyzer:
    """Multi-source synthesis with full reasoning chain for complex threats."""

    @staticmethod
    def analyze(
        domain: ThreatDomain,
        details: str,
        matched_doctrines: list[DoctrineBlock],
        indicators: list[ThreatIndicator],
    ) -> str:
        sections: list[str] = []

        sections.append(f"=== DEEP ANALYSIS: {domain.value} THREAT ===")
        sections.append(f"Input: {details[:500]}")
        sections.append("")

        # Doctrine synthesis
        if matched_doctrines:
            sections.append("--- DOCTRINE SYNTHESIS ---")
            for doc in matched_doctrines:
                sections.append(f"[{doc.topic}] Confidence: {doc.confidence.value}")
                sections.append(f"  Conclusion: {doc.conclusion_template[:200]}")
                sections.append(f"  Key Factors: {', '.join(doc.key_factors[:3])}")
                sections.append(f"  Resolution: {doc.resolution_strategy[:200]}")
                sections.append("")

        # Indicator analysis
        if indicators:
            sections.append("--- INDICATOR ANALYSIS ---")
            for ind in indicators:
                sections.append(f"  [{ind.source}] {ind.description} (score: {ind.raw_score})")
            sections.append("")

        # Adversary assessment
        if matched_doctrines:
            sections.append("--- ADVERSARY POSITION ---")
            for doc in matched_doctrines:
                sections.append(f"  [{doc.topic}] {doc.adversary_position}")
            sections.append("")

        # Counter-argument review
        if matched_doctrines:
            sections.append("--- COUNTER-ARGUMENTS CONSIDERED ---")
            for doc in matched_doctrines:
                for ca in doc.counter_arguments[:2]:
                    sections.append(f"  [{doc.topic}] {ca}")
            sections.append("")

        sections.append("--- SYNTHESIS ---")
        domain_count = len(set(d.domain.value for d in matched_doctrines))
        sections.append(
            f"This threat spans {domain_count} domain(s) with {len(matched_doctrines)} applicable doctrines. "
            f"{len(indicators)} active indicators detected."
        )

        return "\n".join(sections)


# ═══════════════════════════════════════════════════════════════════════════
# 16. THREE-LAYER RESPONSE (TIE Component #1)
# ═══════════════════════════════════════════════════════════════════════════

class ThreeLayerResponse:
    """
    Layer 1: Doctrine Cache (0-200ms) — pre-compiled responses
    Layer 2: Semantic Retrieval — vector search fallback
    Layer 3: Deep Analysis — full multi-source synthesis
    """

    def __init__(
        self,
        doctrines: list[DoctrineBlock],
        vector_search: VectorSearch,
        deep_analyzer: DeepAnalyzer,
    ) -> None:
        self._doctrines = doctrines
        self._vector_search = vector_search
        self._deep_analyzer = deep_analyzer

    def resolve(
        self,
        domain: ThreatDomain,
        details: str,
        indicators: list[ThreatIndicator],
        mode: ResponseMode,
    ) -> tuple[str, list[DoctrineBlock], str]:
        """
        Returns (layer_used, matched_doctrines, analysis_text).
        """
        # Layer 1: Doctrine cache
        layer1_matches: list[tuple[DoctrineBlock, float]] = []
        for doc in self._doctrines:
            matched, score = doc.matches(details)
            if matched:
                layer1_matches.append((doc, score))
            elif doc.domain == domain:
                layer1_matches.append((doc, 0.1))

        layer1_matches.sort(key=lambda x: x[1], reverse=True)

        if layer1_matches and layer1_matches[0][1] > 0.3:
            matched_docs = [m[0] for m in layer1_matches[:5]]
            if mode == ResponseMode.FAST:
                analysis = matched_docs[0].conclusion_template
            elif mode == ResponseMode.DEFENSE:
                analysis = self._format_defense(matched_docs)
            else:
                analysis = self._deep_analyzer.analyze(domain, details, matched_docs, indicators)
            return "DOCTRINE_CACHE", matched_docs, analysis

        # Layer 2: Vector search
        vector_results = self._vector_search.search(details, top_k=5)
        if vector_results:
            matched_docs = [vr[0] for vr in vector_results]
            if mode == ResponseMode.FAST:
                analysis = matched_docs[0].conclusion_template
            elif mode == ResponseMode.DEFENSE:
                analysis = self._format_defense(matched_docs)
            else:
                analysis = self._deep_analyzer.analyze(domain, details, matched_docs, indicators)
            return "SEMANTIC_RETRIEVAL", matched_docs, analysis

        # Layer 3: Deep analysis without doctrine match
        analysis = self._deep_analyzer.analyze(domain, details, [], indicators)
        return "DEEP_ANALYSIS", [], analysis

    def _format_defense(self, doctrines: list[DoctrineBlock]) -> str:
        parts: list[str] = ["=== DEFENSE-GRADE THREAT ASSESSMENT ===\n"]
        for doc in doctrines:
            parts.append(f"TOPIC: {doc.topic}")
            parts.append(f"DOMAIN: {doc.domain.value}")
            parts.append(f"CONFIDENCE: {doc.confidence.value}")
            parts.append(f"CONCLUSION: {doc.conclusion_template}")
            parts.append(f"REASONING: {doc.reasoning_framework[:500]}")
            parts.append(f"AUTHORITIES: {'; '.join(doc.primary_authority)}")
            parts.append(f"RESOLUTION: {doc.resolution_strategy}")
            parts.append(f"ADVERSARY: {doc.adversary_position}")
            parts.append(f"KEY FACTORS: {'; '.join(doc.key_factors)}")
            parts.append("")
        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# 17. THREAT ASSESSMENT ENGINE (main orchestrator)
# ═══════════════════════════════════════════════════════════════════════════

class ThreatAssessmentEngine:
    """Core engine orchestrating all TIE-20 components for threat assessment."""

    def __init__(self) -> None:
        self.doctrines = build_doctrine_cache()
        self.normalizer = SemanticNormalizer()
        self.vector_search = VectorSearch(self.doctrines)
        self.deep_analyzer = DeepAnalyzer()
        self.three_layer = ThreeLayerResponse(self.doctrines, self.vector_search, self.deep_analyzer)
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap(self.doctrines)
        self.metrics = MetricsCollector()
        self.audit = AuditTrail(AUDIT_LOG_PATH)
        self.authority = AuthorityHardening()
        self.fact_fragility = FactFragility()
        self.zoned_analysis = ZonedAnalysis()
        self.decomposer = MultiDoctrineDecomposer()

        self._assessments: list[ThreatAssessmentResponse] = []
        self._active_threats: dict[str, DashboardEntry] = {}

        logger.info(
            f"ThreatAssessmentEngine initialized: {len(self.doctrines)} doctrines, "
            f"{self.normalizer.term_count} semantic terms"
        )

    def assess(self, request: ThreatAssessmentRequest) -> ThreatAssessmentResponse:
        """Execute full threat assessment pipeline."""
        t_start = time.time()
        assessment_id = f"BLD02-{uuid.uuid4().hex[:12]}"

        # Normalize input
        normalized_details = self.normalizer.normalize(request.details)
        zone = self.zoned_analysis.classify_zone(request.details)

        # Three-layer resolution
        layer_used, matched_docs, analysis = self.three_layer.resolve(
            request.domain, request.details, request.indicators, request.mode
        )

        # Compute threat scoring
        scoring = self._compute_scoring(request, matched_docs)

        # Confidence stratification
        confidence = self._stratify_confidence(scoring, matched_docs)

        # Generate mitigations
        mitigations = self._generate_mitigations(matched_docs, scoring)

        # Authority chain
        authority_sources = []
        for doc in matched_docs:
            authority_sources.extend(doc.primary_authority)
        authority_chain = self.authority.get_authority_chain(
            ["NIST_FRAMEWORK", "INTERNAL_POLICY", "INDUSTRY_STANDARD", "AI_INFERENCE"]
        )

        # Doctrine hit tracking
        doctrine_hits: list[str] = []
        for doc in matched_docs:
            doctrine_hits.append(doc.topic)
            self.coverage_map.record_hit(doc.topic)
        if not matched_docs:
            self.coverage_map.record_miss(request.details[:200])

        # Determinism hash
        hash_data = {
            "domain": request.domain.value,
            "details": request.details,
            "scoring": scoring.model_dump(),
            "doctrine_hits": doctrine_hits,
        }
        det_hash = compute_determinism_hash(hash_data)

        # Summary
        summary = self._build_summary(request.domain, scoring, len(matched_docs), layer_used)

        latency_ms = round((time.time() - t_start) * 1000, 2)

        response = ThreatAssessmentResponse(
            assessment_id=assessment_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain=request.domain,
            scoring=scoring,
            risk_level=scoring.risk_level,
            confidence=confidence,
            zone=zone,
            summary=summary,
            analysis=analysis,
            mitigations=mitigations,
            doctrine_hits=doctrine_hits,
            determinism_hash=det_hash,
            response_mode=request.mode,
            latency_ms=latency_ms,
            authority_chain=authority_chain,
        )

        # Record to all tracking systems
        self.telemetry.record_query(assessment_id, request.domain.value, latency_ms, True, doctrine_hits)
        self.drift_watcher.record_assessment(request.domain.value, scoring.composite)
        self.metrics.record_assessment_risk(scoring.risk_level)

        # Store assessment
        self._assessments.append(response)
        if len(self._assessments) > MAX_THREAT_HISTORY:
            self._assessments = self._assessments[-MAX_THREAT_HISTORY:]

        # Update active threats dashboard
        dashboard_entry = DashboardEntry(
            assessment_id=assessment_id,
            domain=request.domain,
            risk_level=scoring.risk_level,
            composite_score=scoring.composite,
            summary=summary,
            timestamp=response.timestamp,
            color_code=scoring.color_code,
        )
        self._active_threats[assessment_id] = dashboard_entry

        # Audit log
        self.audit.log_entry({
            "assessment_id": assessment_id,
            "domain": request.domain.value,
            "risk_level": scoring.risk_level.value,
            "composite_score": scoring.composite,
            "latency_ms": latency_ms,
            "layer_used": layer_used,
            "doctrine_hits": doctrine_hits,
            "determinism_hash": det_hash,
        })

        logger.info(
            f"Assessment {assessment_id}: {request.domain.value} | "
            f"Risk={scoring.risk_level.value} | Score={scoring.composite} | "
            f"Layer={layer_used} | {latency_ms}ms"
        )

        return response

    def _compute_scoring(
        self, request: ThreatAssessmentRequest, matched_docs: list[DoctrineBlock]
    ) -> ThreatScoring:
        """Compute threat score from indicators and doctrine matching."""
        if request.indicators:
            avg_raw = statistics.mean(ind.raw_score for ind in request.indicators)
            max_raw = max(ind.raw_score for ind in request.indicators)
            indicator_count = len(request.indicators)
        else:
            avg_raw = 5.0
            max_raw = 5.0
            indicator_count = 0

        # Likelihood based on indicator severity and count
        likelihood = min(10.0, avg_raw * 0.7 + min(indicator_count, 5) * 0.6)

        # Impact from doctrine confidence
        if matched_docs:
            confidence_weights = {
                ConfidenceStratification.HIGH_RISK: 9.0,
                ConfidenceStratification.DISCLOSURE: 7.0,
                ConfidenceStratification.AGGRESSIVE: 6.0,
                ConfidenceStratification.DEFENSIBLE: 5.0,
            }
            doc_impact = statistics.mean(
                confidence_weights.get(d.confidence, 5.0) for d in matched_docs
            )
        else:
            doc_impact = 5.0
        impact = min(10.0, max(1.0, (max_raw * 0.5 + doc_impact * 0.5)))

        # Proximity — default to medium, adjust from context
        proximity = 5.0
        context = request.context
        if context.get("imminent"):
            proximity = 9.0
        elif context.get("near_term"):
            proximity = 7.0
        elif context.get("long_term"):
            proximity = 3.0

        scoring = ThreatScoring(
            likelihood=round(likelihood, 1),
            impact=round(impact, 1),
            proximity=round(proximity, 1),
        )
        scoring.compute()
        return scoring

    def _stratify_confidence(
        self, scoring: ThreatScoring, matched_docs: list[DoctrineBlock]
    ) -> ConfidenceStratification:
        """Determine confidence stratification for the assessment."""
        if not matched_docs:
            return ConfidenceStratification.DISCLOSURE
        doc_confidences = [d.confidence for d in matched_docs]
        if ConfidenceStratification.HIGH_RISK in doc_confidences:
            return ConfidenceStratification.HIGH_RISK
        if scoring.composite >= 5.0:
            return ConfidenceStratification.AGGRESSIVE
        if all(c == ConfidenceStratification.DEFENSIBLE for c in doc_confidences):
            return ConfidenceStratification.DEFENSIBLE
        return ConfidenceStratification.AGGRESSIVE

    def _generate_mitigations(
        self, matched_docs: list[DoctrineBlock], scoring: ThreatScoring
    ) -> list[MitigationAction]:
        """Generate mitigation actions from matched doctrines."""
        mitigations: list[MitigationAction] = []
        seen_descriptions: set[str] = set()

        priority_base = 1 if scoring.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH) else 3

        for doc in matched_docs:
            for idx, template in enumerate(doc.mitigation_templates):
                if template in seen_descriptions:
                    continue
                seen_descriptions.add(template)
                priority = min(5, priority_base + idx)
                mitigations.append(MitigationAction(
                    priority=priority,
                    description=template,
                    responsible_party="ECHO PRIME Security Operations",
                    estimated_effort="1-5 days",
                ))

        mitigations.sort(key=lambda m: m.priority)
        return mitigations[:15]

    def _build_summary(
        self, domain: ThreatDomain, scoring: ThreatScoring, doctrine_count: int, layer: str
    ) -> str:
        return (
            f"{domain.value} threat assessed at {scoring.risk_level.value} risk "
            f"(composite score: {scoring.composite:.3f}, L={scoring.likelihood}, "
            f"I={scoring.impact}, P={scoring.proximity}). "
            f"{doctrine_count} doctrine(s) matched via {layer}."
        )

    def get_dashboard(self) -> list[DashboardEntry]:
        """Return all active threats sorted by composite score descending."""
        entries = list(self._active_threats.values())
        entries.sort(key=lambda e: e.composite_score, reverse=True)
        return entries

    def get_history(self, limit: int = 50, domain: Optional[ThreatDomain] = None) -> list[dict[str, Any]]:
        """Return assessment history, optionally filtered by domain."""
        results = self._assessments
        if domain:
            results = [a for a in results if a.domain == domain]
        results = results[-limit:]
        return [
            {
                "assessment_id": a.assessment_id,
                "domain": a.domain.value,
                "risk_level": a.risk_level.value,
                "composite_score": a.scoring.composite,
                "summary": a.summary,
                "timestamp": a.timestamp,
                "latency_ms": a.latency_ms,
            }
            for a in results
        ]

    def get_health(self) -> HealthResponse:
        return HealthResponse(
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            version=ENGINE_VERSION,
            status="OPERATIONAL",
            uptime_seconds=self.telemetry.uptime_seconds,
            total_assessments=self.telemetry.total_queries,
            active_threats=len(self._active_threats),
            doctrine_count=len(self.doctrines),
            semantic_terms=self.normalizer.term_count,
            coverage_topics=len(self.doctrines),
            last_assessment=self._assessments[-1].timestamp if self._assessments else None,
            port=ENGINE_PORT,
            tier=ENGINE_TIER,
            mode=ENGINE_MODE,
            authority=AUTHORITY_LEVEL,
        )


# ═══════════════════════════════════════════════════════════════════════════
# 18. FASTAPI APPLICATION (TIE Component #17)
# ═══════════════════════════════════════════════════════════════════════════

engine_instance: Optional[ThreatAssessmentEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine_instance
    logger.info(f"Starting BLD02 Threat Assessment Engine v{ENGINE_VERSION} on port {ENGINE_PORT}")
    engine_instance = ThreatAssessmentEngine()
    logger.info("Engine initialized and ready")
    yield
    logger.info("Shutting down BLD02 Threat Assessment Engine")


app = FastAPI(
    title=f"BLD02 — {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description=(
        "Threat Assessment Engine for McWilliams Bloodline and ECHO PRIME system. "
        "Covers PHYSICAL, CYBER, FINANCIAL, LEGAL, REPUTATIONAL, INSIDER, "
        "SUPPLY_CHAIN, and GEOPOLITICAL threat domains."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_engine() -> ThreatAssessmentEngine:
    if engine_instance is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine_instance


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """TIE Component #12: Comprehensive health endpoint."""
    eng = _get_engine()
    return eng.get_health().model_dump()


@app.post("/assess")
async def assess_threat(request: ThreatAssessmentRequest) -> dict[str, Any]:
    """Primary threat assessment endpoint. POST {domain, details} -> full assessment."""
    eng = _get_engine()
    try:
        response = eng.assess(request)
        return response.model_dump()
    except Exception as exc:
        logger.error(f"Assessment failed: {exc}")
        eng.telemetry.record_query("FAILED", request.domain.value, 0.0, False, [])
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/dashboard")
async def get_dashboard() -> dict[str, Any]:
    """Get all active threats organized by category."""
    eng = _get_engine()
    entries = eng.get_dashboard()
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        domain_key = entry.domain.value
        if domain_key not in by_domain:
            by_domain[domain_key] = []
        by_domain[domain_key].append(entry.model_dump())

    critical_count = sum(1 for e in entries if e.risk_level == RiskLevel.CRITICAL)
    high_count = sum(1 for e in entries if e.risk_level == RiskLevel.HIGH)

    return {
        "engine_id": ENGINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_active_threats": len(entries),
        "critical_count": critical_count,
        "high_count": high_count,
        "threats_by_domain": by_domain,
        "risk_matrix": {
            "critical": [e.model_dump() for e in entries if e.risk_level == RiskLevel.CRITICAL],
            "high": [e.model_dump() for e in entries if e.risk_level == RiskLevel.HIGH],
            "elevated": [e.model_dump() for e in entries if e.risk_level == RiskLevel.ELEVATED],
            "moderate": [e.model_dump() for e in entries if e.risk_level == RiskLevel.MODERATE],
            "low": [e.model_dump() for e in entries if e.risk_level in (RiskLevel.LOW, RiskLevel.MINIMAL)],
        },
    }


@app.get("/history")
async def get_history(
    limit: int = Query(default=50, ge=1, le=500),
    domain: Optional[ThreatDomain] = Query(default=None),
) -> dict[str, Any]:
    """Get threat assessment history, optionally filtered by domain."""
    eng = _get_engine()
    history = eng.get_history(limit=limit, domain=domain)
    return {
        "engine_id": ENGINE_ID,
        "total_results": len(history),
        "filter_domain": domain.value if domain else None,
        "assessments": history,
    }


@app.get("/telemetry")
async def get_telemetry() -> dict[str, Any]:
    """TIE Component #8: Full telemetry data."""
    eng = _get_engine()
    return {
        "engine_id": ENGINE_ID,
        "telemetry": eng.telemetry.get_metrics(),
        "metrics": eng.metrics.get_metrics(),
    }


@app.get("/coverage")
async def get_coverage() -> dict[str, Any]:
    """TIE Component #10: Coverage map showing doctrine utilization."""
    eng = _get_engine()
    return {
        "engine_id": ENGINE_ID,
        "coverage": eng.coverage_map.get_coverage(),
    }


@app.get("/drift")
async def get_drift() -> dict[str, Any]:
    """TIE Component #9: Drift detection alerts."""
    eng = _get_engine()
    return {
        "engine_id": ENGINE_ID,
        "drift_alerts": eng.drift_watcher.alerts,
        "alert_count": eng.drift_watcher.alert_count,
    }


@app.get("/audit")
async def get_audit(count: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
    """TIE Component #15: Audit trail entries."""
    eng = _get_engine()
    entries = eng.audit.get_recent(count)
    return {
        "engine_id": ENGINE_ID,
        "entries": entries,
        "count": len(entries),
    }


@app.get("/doctrines")
async def get_doctrines() -> dict[str, Any]:
    """List all loaded doctrines."""
    eng = _get_engine()
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": len(eng.doctrines),
        "doctrines": [d.to_dict() for d in eng.doctrines],
    }


@app.get("/domains")
async def get_domains() -> dict[str, Any]:
    """List all threat domains with descriptions."""
    return {
        "engine_id": ENGINE_ID,
        "domains": [
            {"domain": "PHYSICAL", "description": "Physical security: break-ins, surveillance, assault, trespass"},
            {"domain": "CYBER", "description": "Cybersecurity: hacking, malware, phishing, DDoS, data breach"},
            {"domain": "FINANCIAL", "description": "Financial: fraud, unauthorized transactions, embezzlement"},
            {"domain": "LEGAL", "description": "Legal: litigation, regulatory actions, compliance violations"},
            {"domain": "REPUTATIONAL", "description": "Reputation: media attacks, defamation, brand damage"},
            {"domain": "INSIDER", "description": "Insider: employee sabotage, data exfiltration, privilege abuse"},
            {"domain": "SUPPLY_CHAIN", "description": "Supply chain: vendor compromise, dependency vulnerabilities"},
            {"domain": "GEOPOLITICAL", "description": "Geopolitical: oil prices, regulations, water rights, politics"},
        ],
    }


@app.post("/score")
async def compute_score(
    likelihood: float = Query(ge=1.0, le=10.0),
    impact: float = Query(ge=1.0, le=10.0),
    proximity: float = Query(ge=1.0, le=10.0),
) -> dict[str, Any]:
    """Compute a standalone threat score without full assessment."""
    scoring = ThreatScoring(likelihood=likelihood, impact=impact, proximity=proximity)
    scoring.compute()
    return scoring.model_dump()


@app.get("/risk-matrix")
async def get_risk_matrix() -> dict[str, Any]:
    """Return the 3x3 risk matrix definition with color coding."""
    matrix = {
        "dimensions": {
            "likelihood": {"low": "1-3", "medium": "4-6", "high": "7-10"},
            "impact": {"low": "1-3", "medium": "4-6", "high": "7-10"},
        },
        "cells": [
            {"likelihood": "high", "impact": "high", "risk": "CRITICAL", "color": "red", "score_range": "4.9-10.0"},
            {"likelihood": "high", "impact": "medium", "risk": "HIGH", "color": "red", "score_range": "2.8-5.6"},
            {"likelihood": "high", "impact": "low", "risk": "ELEVATED", "color": "orange", "score_range": "0.7-2.7"},
            {"likelihood": "medium", "impact": "high", "risk": "HIGH", "color": "red", "score_range": "2.0-5.6"},
            {"likelihood": "medium", "impact": "medium", "risk": "MODERATE", "color": "yellow", "score_range": "0.8-1.8"},
            {"likelihood": "medium", "impact": "low", "risk": "LOW", "color": "green", "score_range": "0.2-0.7"},
            {"likelihood": "low", "impact": "high", "risk": "ELEVATED", "color": "orange", "score_range": "0.7-2.7"},
            {"likelihood": "low", "impact": "medium", "risk": "LOW", "color": "green", "score_range": "0.2-0.7"},
            {"likelihood": "low", "impact": "low", "risk": "MINIMAL", "color": "green", "score_range": "0.01-0.27"},
        ],
        "formula": "composite = (likelihood × impact × proximity) / 100",
        "thresholds": {
            "CRITICAL": ">= 7.0",
            "HIGH": ">= 5.0",
            "ELEVATED": ">= 3.5",
            "MODERATE": ">= 2.0",
            "LOW": ">= 1.0",
            "MINIMAL": "< 1.0",
        },
    }
    return {"engine_id": ENGINE_ID, "risk_matrix": matrix}


@app.get("/fragility")
async def compute_fragility(
    verifiability: float = Query(ge=0.0, le=1.0),
    source_independence: float = Query(ge=0.0, le=1.0),
    temporal_stability: float = Query(ge=0.0, le=1.0),
    corroboration_count: int = Query(ge=0, le=20),
) -> dict[str, Any]:
    """TIE Component #14: Compute fact fragility score."""
    result = FactFragility.score(verifiability, source_independence, temporal_stability, corroboration_count)
    return {"engine_id": ENGINE_ID, "fragility": result}


@app.get("/decompose")
async def decompose_threat(details: str = Query(min_length=5)) -> dict[str, Any]:
    """TIE Component #19: Multi-doctrine decomposition of a threat description."""
    eng = _get_engine()
    matched: list[DoctrineBlock] = []
    for doc in eng.doctrines:
        hit, score = doc.matches(details)
        if hit:
            matched.append(doc)
    result = MultiDoctrineDecomposer.decompose(details, matched)
    return {"engine_id": ENGINE_ID, "decomposition": result}


# ═══════════════════════════════════════════════════════════════════════════
# 19. MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching BLD02 {ENGINE_NAME} on port {ENGINE_PORT}")
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info",
        reload=False,
    )
