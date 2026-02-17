"""
E12 Feedback Ingester Engine
TIE-20 Compliant | Port 8612
Domain: Professional feedback processing, engine tuning signal generation,
        correction ingestion, quality tracking, doctrine refinement loops.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import statistics
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
    from cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None  # type: ignore[assignment,misc]

# ─── Constants ───────────────────────────────────────────────────────────────
ENGINE_ID = "E12"
ENGINE_NAME = "Feedback Ingester Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8612
ENGINE_DOMAIN = "feedback_ingestion"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG = LOG_DIR / "e12_audit.jsonl"
TUNING_LOG = LOG_DIR / "e12_tuning_signals.jsonl"

logger.add(LOG_DIR / "e12_engine.log", rotation="50 MB", retention="30 days", level="DEBUG")
logger.add(AUDIT_LOG, rotation="20 MB", retention="90 days", level="INFO", serialize=True)

AUTO_APPLY_CONFIDENCE_THRESHOLD = 0.92
CONFLICT_DETECTION_WINDOW_HOURS = 168
MIN_AGGREGATION_COUNT = 3
CREDENTIAL_TIERS = {"attorney": 0.95, "cpa": 0.93, "landman": 0.90, "engineer": 0.88, "analyst": 0.80, "general": 0.50}
FEEDBACK_WEIGHT = {"CORRECTION": 1.0, "OVERRIDE": 0.95, "REJECTION": 0.7, "FLAG": 0.65, "RATING": 0.4, "SUGGESTION": 0.35, "APPROVAL": 0.3}


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS — TIE Component 17
# ═══════════════════════════════════════════════════════════════════════════════

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


class FeedbackType(str, Enum):
    CORRECTION = "CORRECTION"
    RATING = "RATING"
    REJECTION = "REJECTION"
    APPROVAL = "APPROVAL"
    SUGGESTION = "SUGGESTION"
    FLAG = "FLAG"
    OVERRIDE = "OVERRIDE"


class ReviewerRole(str, Enum):
    ATTORNEY = "attorney"
    CPA = "cpa"
    LANDMAN = "landman"
    ENGINEER = "engineer"
    ANALYST = "analyst"
    GENERAL = "general"


class TuningSignalType(str, Enum):
    DOCTRINE_UPDATE = "DOCTRINE_UPDATE"
    KEYWORD_ADJUSTMENT = "KEYWORD_ADJUSTMENT"
    CONFIDENCE_RECALIBRATION = "CONFIDENCE_RECALIBRATION"
    ERROR_PATTERN = "ERROR_PATTERN"
    TRAINING_PAIR = "TRAINING_PAIR"
    NEW_DOCTRINE = "NEW_DOCTRINE"


class IssueCategory(str, Enum):
    CORRECTION_PROCESSING = "CORRECTION_PROCESSING"
    RATING_AGGREGATION = "RATING_AGGREGATION"
    CONFLICT_RESOLUTION = "CONFLICT_RESOLUTION"
    SIGNAL_GENERATION = "SIGNAL_GENERATION"
    CREDENTIAL_VALIDATION = "CREDENTIAL_VALIDATION"
    IMPACT_TRACKING = "IMPACT_TRACKING"
    DOCTRINE_TUNING = "DOCTRINE_TUNING"
    REGRESSION_DETECTION = "REGRESSION_DETECTION"
    FEEDBACK_ROUTING = "FEEDBACK_ROUTING"
    QUALITY_METRICS = "QUALITY_METRICS"


class FeedbackItem(BaseModel):
    feedback_id: str = Field(default_factory=lambda: f"FB-{uuid.uuid4().hex[:12]}")
    feedback_type: FeedbackType
    target_engine_id: str
    target_doctrine_topic: Optional[str] = None
    target_response_field: Optional[str] = None
    original_query: Optional[str] = None
    original_response: Optional[str] = None
    correction_text: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
    reviewer_id: str = "anonymous"
    reviewer_role: ReviewerRole = ReviewerRole.GENERAL
    reviewer_credentials: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TuningSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"TS-{uuid.uuid4().hex[:12]}")
    signal_type: TuningSignalType
    target_engine_id: str
    target_doctrine_topic: Optional[str] = None
    proposed_change: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    source_feedback_ids: List[str] = Field(default_factory=list)
    auto_apply: bool = False
    status: str = "pending"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    context: Dict[str, Any] = Field(default_factory=dict)
    feedback: Optional[FeedbackItem] = None


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: float
    confidence_level: ConfidenceLevel
    authorities: List[str] = Field(default_factory=list)
    reasoning: str = ""
    tuning_signals: List[Dict[str, Any]] = Field(default_factory=list)
    feedback_summary: Dict[str, Any] = Field(default_factory=dict)
    determinism_hash: str = ""
    latency_ms: float = 0.0
    layer_hit: str = "doctrine_cache"
    disclosure_caveat: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-3: DOCTRINE CACHE — 35 feedback processing rules
# ═══════════════════════════════════════════════════════════════════════════════

class DoctrineBlock:
    __slots__ = (
        "topic", "keywords", "conclusion_template", "reasoning_framework",
        "key_factors", "primary_authority", "burden_holder", "adversary_position",
        "counter_arguments", "resolution_strategy", "entity_scope",
        "confidence", "confidence_stratification", "controlling_precedent",
    )

    def __init__(self, topic: str, keywords: List[str], conclusion_template: str,
                 reasoning_framework: str, key_factors: List[str],
                 primary_authority: List[str], burden_holder: str,
                 adversary_position: str, counter_arguments: List[str],
                 resolution_strategy: str, entity_scope: str,
                 confidence: float, confidence_stratification: str,
                 controlling_precedent: str):
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
        self.confidence_stratification = confidence_stratification
        self.controlling_precedent = controlling_precedent


def _build_doctrine_cache() -> Dict[str, DoctrineBlock]:
    blocks: Dict[str, DoctrineBlock] = {}

    blocks["correction_intake"] = DoctrineBlock(
        topic="correction_intake",
        keywords=["correction", "wrong answer", "fix", "error", "incorrect", "mistake"],
        conclusion_template="Correction received targeting engine {target_engine_id} on topic '{target_doctrine_topic}'. The reviewer ({reviewer_role}) asserts the original output was incorrect and provides an authoritative replacement. This correction carries weight {weight:.2f} based on credential tier and feedback type.",
        reasoning_framework="Corrections are the strongest feedback signal. A professional reviewer states the engine produced an incorrect answer and provides the correct one. Processing: 1) Validate reviewer credentials match the domain expertise required. 2) Parse original response to identify the specific erroneous claim. 3) Compare correction against existing doctrine cache for conflicts. 4) If no conflict, generate a DOCTRINE_UPDATE tuning signal. 5) If conflict detected, escalate to CONFLICT_RESOLUTION pipeline. 6) Log the correction-pair as a TRAINING_PAIR for future fine-tuning datasets.",
        key_factors=["reviewer credential tier", "specificity of correction", "whether original doctrine exists", "conflict with other feedback", "engine domain match"],
        primary_authority=["Internal Feedback Policy v1.0", "TIE Quality Assurance Framework", "ECHO Engine Governance Protocol"],
        burden_holder="reviewer",
        adversary_position="The original engine output may have been correct in context even if the reviewer disagrees; edge cases and jurisdiction-specific rules can cause legitimate differences of opinion.",
        counter_arguments=["Reviewer may lack full context of original query", "Correction may apply only to specific jurisdiction", "Original answer may have been correct under different assumptions", "Reviewer credentials may not cover this specific sub-domain", "Multiple valid interpretations may exist"],
        resolution_strategy="Accept correction if reviewer credential tier >= 0.85 and no conflicting corrections exist. If conflicts, aggregate all corrections and route to human review. Always generate training pair regardless of acceptance.",
        entity_scope="all_engines",
        confidence=0.92,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="ECHO Feedback Processing Standard v1.0",
    )

    blocks["rating_aggregation"] = DoctrineBlock(
        topic="rating_aggregation",
        keywords=["rating", "star", "score", "quality", "satisfaction", "1-5"],
        conclusion_template="Rating of {rating}/5 recorded for engine {target_engine_id}. Current aggregate: {aggregate_rating:.2f} across {total_ratings} ratings. {trend_description}.",
        reasoning_framework="Ratings provide a continuous quality signal. Processing: 1) Validate rating is 1-5 integer. 2) Weight by reviewer credential tier. 3) Compute weighted rolling average (last 100 ratings). 4) Detect trends (improving, declining, stable). 5) If average drops below 3.0, generate ERROR_PATTERN signal. 6) If average rises above 4.5 after changes, generate positive impact confirmation. 7) Segment ratings by doctrine topic if provided for granular quality tracking.",
        key_factors=["numeric rating value", "reviewer weight", "rolling average trend", "topic segmentation", "comment sentiment"],
        primary_authority=["Quality Metrics Framework", "Engine Performance Standards"],
        burden_holder="system",
        adversary_position="Individual ratings may reflect user preference rather than answer quality; a technically correct but complex answer may receive low ratings from non-experts.",
        counter_arguments=["Rating inflation from approval bias", "Rating deflation from frustrated users", "No comment context makes rating ambiguous", "Different user expectations per engine domain"],
        resolution_strategy="Weight ratings by credential tier. Require minimum 10 ratings before trend analysis. Flag engines with >0.5 std dev decline over 20-rating window.",
        entity_scope="per_engine",
        confidence=0.78,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Statistical Process Control for Engine Quality",
    )

    blocks["rejection_processing"] = DoctrineBlock(
        topic="rejection_processing",
        keywords=["rejection", "wrong", "unhelpful", "bad", "useless", "incorrect output"],
        conclusion_template="Rejection recorded for engine {target_engine_id}. Rejection reason: '{comment}'. This is a negative quality signal with weight {weight:.2f}. {action_taken}.",
        reasoning_framework="Rejections indicate the output failed to meet user expectations without specifying the correct answer. Processing: 1) Extract rejection reason from comment if available. 2) Classify rejection type: factual error, relevance miss, formatting issue, or incomplete answer. 3) Route factual errors to correction pipeline for follow-up. 4) Route relevance misses to keyword adjustment pipeline. 5) Aggregate rejection patterns per engine and per doctrine topic. 6) If rejection rate exceeds 15% for a doctrine topic, generate ERROR_PATTERN signal.",
        key_factors=["rejection reason category", "frequency per doctrine", "reviewer expertise", "whether correction was also provided", "pattern across multiple users"],
        primary_authority=["Negative Feedback Processing Protocol", "Engine Quality Thresholds"],
        burden_holder="system",
        adversary_position="Users may reject correct answers they disagree with or don't understand; rejection alone doesn't prove the engine was wrong.",
        counter_arguments=["User may have asked ambiguous question", "Answer may be correct but not what user wanted", "Rejection without explanation is low-information", "User expectations may be unrealistic"],
        resolution_strategy="Classify and aggregate. Single rejections are weak signals; patterns across multiple users on the same topic trigger investigation. Always request follow-up correction when possible.",
        entity_scope="per_engine",
        confidence=0.70,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Rejection Analysis Framework v1.0",
    )

    blocks["approval_tracking"] = DoctrineBlock(
        topic="approval_tracking",
        keywords=["approval", "correct", "good", "accurate", "helpful", "confirmed"],
        conclusion_template="Approval recorded for engine {target_engine_id} on topic '{target_doctrine_topic}'. This confirms the existing doctrine block produces acceptable output. Confidence reinforcement: +{reinforcement:.3f}.",
        reasoning_framework="Approvals confirm engine output quality. Processing: 1) Link approval to specific doctrine block if topic provided. 2) Increment approval counter for that doctrine. 3) Calculate approval ratio (approvals / total feedback). 4) High approval ratio (>80%) reinforces existing doctrine confidence. 5) Track which reviewer roles approve most frequently for calibration. 6) Approvals from high-credential reviewers carry more weight for confidence boosting.",
        key_factors=["doctrine topic linkage", "reviewer credential tier", "approval ratio trend", "whether this follows a recent correction"],
        primary_authority=["Positive Feedback Integration Protocol"],
        burden_holder="system",
        adversary_position="Approval bias exists; users may approve mediocre answers if they seem plausible. Approvals should not prevent corrections from being applied.",
        counter_arguments=["Approval may be perfunctory", "User may not have expertise to evaluate", "High approval rate may mask edge-case failures"],
        resolution_strategy="Count approvals for confidence reinforcement but never let them override corrections. Weight by credential tier. Use as denominator in quality ratio calculations.",
        entity_scope="per_engine",
        confidence=0.75,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Positive Signal Integration Standard",
    )

    blocks["suggestion_processing"] = DoctrineBlock(
        topic="suggestion_processing",
        keywords=["suggestion", "improve", "better", "enhance", "would be nice", "consider"],
        conclusion_template="Suggestion received for engine {target_engine_id}: '{comment}'. Classified as {suggestion_category}. Priority: {priority}. {action_taken}.",
        reasoning_framework="Suggestions indicate enhancement opportunities without asserting error. Processing: 1) Classify suggestion: additional_info, formatting, depth, speed, citation, or scope. 2) Check if suggestion aligns with existing enhancement backlog. 3) Weight by reviewer expertise and specificity. 4) Aggregate similar suggestions — 3+ on same topic elevates priority. 5) Generate KEYWORD_ADJUSTMENT signal if suggestion relates to routing. 6) Generate NEW_DOCTRINE signal if suggestion identifies a missing topic area.",
        key_factors=["suggestion category", "specificity level", "aggregation count", "alignment with existing backlog", "reviewer expertise"],
        primary_authority=["Enhancement Request Protocol", "Feature Prioritization Matrix"],
        burden_holder="reviewer",
        adversary_position="Suggestions may conflict with design decisions or scope constraints; not all suggestions should be implemented.",
        counter_arguments=["Suggestion may be out of scope", "Implementation may degrade performance", "Suggestion may conflict with other feedback", "Cost-benefit may not justify change"],
        resolution_strategy="Aggregate and prioritize. Implement suggestions with 3+ endorsements and high-credential backing. Always acknowledge receipt.",
        entity_scope="per_engine",
        confidence=0.65,
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Enhancement Pipeline Standard v1.0",
    )

    blocks["flag_processing"] = DoctrineBlock(
        topic="flag_processing",
        keywords=["flag", "error in", "specific field", "wrong field", "targeted", "field error"],
        conclusion_template="Flag received for engine {target_engine_id}, field '{target_response_field}': '{comment}'. This targets a specific output field for correction. Weight: {weight:.2f}.",
        reasoning_framework="Flags are targeted error reports on specific response fields. More precise than rejections, less authoritative than corrections. Processing: 1) Validate the flagged field exists in the engine's response schema. 2) Cross-reference with doctrine block that generated the field value. 3) Check if field has existing corrections pending. 4) If multiple flags on same field from different reviewers, escalate to correction-level investigation. 5) Generate CONFIDENCE_RECALIBRATION signal for the specific field. 6) Track flag patterns to detect systematic field-level errors.",
        key_factors=["flagged field name", "field existence validation", "multiple-flag aggregation", "doctrine block linkage", "field error pattern"],
        primary_authority=["Field-Level Error Reporting Protocol"],
        burden_holder="reviewer",
        adversary_position="Field-level flags may misidentify the source of error; the issue may be in upstream processing rather than the flagged field itself.",
        counter_arguments=["Flag may target symptom not cause", "Field value may be correct but misleading", "Reviewer may misunderstand field semantics"],
        resolution_strategy="Validate field, aggregate flags, escalate to correction pipeline if 2+ independent flags on same field. Generate confidence recalibration signal immediately.",
        entity_scope="per_engine",
        confidence=0.80,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Targeted Error Reporting Standard v1.0",
    )

    blocks["override_processing"] = DoctrineBlock(
        topic="override_processing",
        keywords=["override", "authoritative", "professional override", "expert correction", "final answer"],
        conclusion_template="Professional override received from {reviewer_role} (credential tier {credential_tier:.2f}) for engine {target_engine_id}. Override replaces engine conclusion with authoritative answer. Auto-apply: {auto_apply}.",
        reasoning_framework="Overrides are the highest-authority feedback type. A credentialed professional provides the definitive answer, replacing the engine's output entirely. Processing: 1) MANDATORY credential validation — only attorney, CPA, or licensed landman can override in their domain. 2) Verify reviewer credential covers the specific domain of the engine. 3) Generate immediate DOCTRINE_UPDATE signal. 4) If auto-apply threshold met (confidence >= 0.92), apply without human review. 5) Generate TRAINING_PAIR with high weight. 6) Notify engine maintainer of override. 7) Track override frequency per engine — high override rate indicates fundamental engine issues.",
        key_factors=["reviewer credential validation", "domain match verification", "override confidence score", "auto-apply eligibility", "engine override frequency"],
        primary_authority=["Professional Override Authority Protocol", "Credential Verification Standard"],
        burden_holder="reviewer",
        adversary_position="Even credentialed professionals can be wrong; overrides should be tracked and auditable. Conflicting overrides must be escalated.",
        counter_arguments=["Professional may have jurisdiction-specific bias", "Override may not account for all query context", "Conflicting professional opinions exist in many domains", "Override confidence may be overstated"],
        resolution_strategy="Require credential validation. Auto-apply if confidence >= threshold and no conflicts. Log all overrides for audit trail. Conflicting overrides trigger mandatory human review.",
        entity_scope="all_engines",
        confidence=0.95,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Professional Override Authority v1.0",
    )

    blocks["credential_validation"] = DoctrineBlock(
        topic="credential_validation",
        keywords=["credential", "verify", "license", "certification", "authority", "qualified"],
        conclusion_template="Credential validation for reviewer '{reviewer_id}': Role={reviewer_role}, Tier={credential_tier:.2f}. {validation_result}.",
        reasoning_framework="Credential validation gates high-authority feedback types. Processing: 1) Map reviewer_role to credential tier weight. 2) For CORRECTION and OVERRIDE types, require tier >= 0.85. 3) Verify claimed role against stored credentials if available. 4) Apply domain-match check: attorney credentials valid for legal engines, CPA for tax/financial, landman for landman engines. 5) Cross-domain credentials receive 0.8x multiplier. 6) Anonymous or unverified reviewers default to 'general' tier (0.50).",
        key_factors=["claimed role", "stored credentials", "domain match", "verification status", "cross-domain penalty"],
        primary_authority=["Reviewer Credential Framework", "Domain Authority Matrix"],
        burden_holder="system",
        adversary_position="Credential verification may be imperfect; self-reported roles without verification carry inherent risk.",
        counter_arguments=["Credentials may be expired", "Role may not cover specific sub-domain", "Self-reported credentials may be inflated", "Cross-domain expertise exists but is rare"],
        resolution_strategy="Trust but verify. Accept self-reported role for initial processing but flag unverified credentials. Require verification for auto-apply overrides.",
        entity_scope="all_engines",
        confidence=0.88,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Credential Tier Matrix v1.0",
    )

    blocks["conflict_detection"] = DoctrineBlock(
        topic="conflict_detection",
        keywords=["conflict", "disagree", "contradictory", "opposing", "conflicting feedback"],
        conclusion_template="Feedback conflict detected on engine {target_engine_id}, topic '{target_doctrine_topic}'. {num_sides} conflicting positions from {num_reviewers} reviewers. Resolution: {resolution}.",
        reasoning_framework="Conflicts arise when multiple reviewers provide contradictory corrections on the same topic. Processing: 1) Detect conflicts within the CONFLICT_DETECTION_WINDOW (168 hours). 2) Group conflicting feedback by position. 3) Weight each position by sum of reviewer credential tiers. 4) If one position has >2x the credential weight, accept it. 5) If positions are closely weighted, escalate to human review. 6) Log all conflicts for pattern analysis. 7) Conflicts may indicate genuine ambiguity in the domain — consider adding disclosure caveat to engine output.",
        key_factors=["number of conflicting positions", "credential weight per position", "time window of conflict", "domain ambiguity potential", "precedent from prior conflicts"],
        primary_authority=["Conflict Resolution Protocol v1.0", "Feedback Arbitration Standard"],
        burden_holder="system",
        adversary_position="Conflicts may reflect genuine domain complexity rather than errors; resolution should not always pick a winner.",
        counter_arguments=["Both sides may be partially correct", "Conflict may be jurisdiction-dependent", "Time-sensitive changes may explain contradiction", "Different query contexts may justify different answers"],
        resolution_strategy="Weight by credentials. Clear winner (>2x weight) auto-resolves. Close contests escalate. All conflicts flagged in audit trail. Consider adding caveat to engine output for genuinely ambiguous topics.",
        entity_scope="per_engine",
        confidence=0.82,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Feedback Conflict Arbitration v1.0",
    )

    blocks["aggregation_rules"] = DoctrineBlock(
        topic="aggregation_rules",
        keywords=["aggregate", "combine", "multiple", "batch", "accumulate", "threshold"],
        conclusion_template="Aggregation analysis for engine {target_engine_id}, topic '{target_doctrine_topic}': {feedback_count} feedback items aggregated. Consensus strength: {consensus:.2f}. {aggregation_result}.",
        reasoning_framework="Individual feedback items are weak signals; aggregation amplifies signal strength. Processing: 1) Group feedback by (engine_id, doctrine_topic, feedback_type). 2) Require minimum MIN_AGGREGATION_COUNT (3) items before generating tuning signal. 3) Calculate consensus: agreement ratio among items. 4) Weight consensus by credential tiers. 5) Consensus >= 0.80 with 3+ items generates confident tuning signal. 6) Consensus < 0.60 with 5+ items indicates genuine ambiguity — flag for human review.",
        key_factors=["item count per group", "consensus ratio", "credential-weighted consensus", "time span of items", "feedback type mix"],
        primary_authority=["Feedback Aggregation Standard v1.0"],
        burden_holder="system",
        adversary_position="Aggregation can amplify systematic bias if reviewer pool is not diverse. Minimum counts help but don't eliminate echo-chamber effects.",
        counter_arguments=["Small sample size may not represent reality", "Correlated reviewers inflate consensus", "Aggregation latency delays corrections", "Mixed feedback types complicate consensus"],
        resolution_strategy="Require MIN_AGGREGATION_COUNT. Weight by credential diversity (penalize same-reviewer duplicates). Separate consensus calculation by feedback type. Report both raw and weighted consensus.",
        entity_scope="per_engine",
        confidence=0.85,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Statistical Aggregation Framework v1.0",
    )

    blocks["doctrine_update_signal"] = DoctrineBlock(
        topic="doctrine_update_signal",
        keywords=["doctrine update", "modify conclusion", "change template", "update cache", "revise"],
        conclusion_template="DOCTRINE_UPDATE signal generated for engine {target_engine_id}, topic '{target_doctrine_topic}'. Proposed change: {change_summary}. Confidence: {confidence:.2f}. Auto-apply: {auto_apply}.",
        reasoning_framework="Doctrine updates modify existing cache entries based on accumulated feedback. Processing: 1) Identify the target doctrine block by topic and engine. 2) Diff the proposed change against current doctrine. 3) Calculate change magnitude (minor wording vs. fundamental conclusion shift). 4) Minor changes (wording, citation updates) auto-apply at confidence >= 0.85. 5) Major changes (conclusion reversal, new key factors) require confidence >= 0.92 or human review. 6) Store pre-change snapshot for rollback. 7) Monitor post-change quality metrics for 48 hours.",
        key_factors=["change magnitude", "confidence threshold", "rollback snapshot", "post-change monitoring window", "human review requirement"],
        primary_authority=["Doctrine Lifecycle Management Protocol"],
        burden_holder="system",
        adversary_position="Automated doctrine updates risk propagating errors at scale; rollback capability is essential.",
        counter_arguments=["Auto-apply may propagate reviewer errors", "Change magnitude assessment may be inaccurate", "Post-change monitoring may miss subtle regressions"],
        resolution_strategy="Classify change magnitude. Apply confidence thresholds. Always snapshot pre-change state. Monitor post-change for 48 hours. Auto-rollback if quality drops >10%.",
        entity_scope="per_engine",
        confidence=0.90,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Doctrine Update Protocol v1.0",
    )

    blocks["keyword_adjustment_signal"] = DoctrineBlock(
        topic="keyword_adjustment_signal",
        keywords=["keyword", "routing", "weight", "boost", "demote", "search terms"],
        conclusion_template="KEYWORD_ADJUSTMENT signal for engine {target_engine_id}: {adjustment_type} keywords {keywords}. Weight change: {weight_delta:+.2f}. Rationale: {rationale}.",
        reasoning_framework="Keyword adjustments modify how queries are routed to doctrine blocks. Processing: 1) Analyze feedback to identify routing failures (query reached wrong doctrine). 2) Extract keywords from successful corrections. 3) Boost keywords that led to correct routing. 4) Demote keywords that caused misrouting. 5) Add new keywords identified in professional corrections. 6) Never remove keywords entirely — demote to minimum weight instead.",
        key_factors=["routing failure analysis", "keyword extraction from corrections", "boost/demote magnitude", "minimum weight floor"],
        primary_authority=["Semantic Routing Optimization Protocol"],
        burden_holder="system",
        adversary_position="Keyword adjustments can have cascading effects on routing for unrelated queries; changes must be scoped carefully.",
        counter_arguments=["Boosting one keyword may demote unrelated matches", "Keyword changes may break existing correct routing", "Over-optimization on recent feedback ignores historical patterns"],
        resolution_strategy="Apply changes incrementally (max +/-0.15 per adjustment). Test routing impact on sample queries before committing. Maintain keyword change history for rollback.",
        entity_scope="per_engine",
        confidence=0.82,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Routing Optimization Standard v1.0",
    )

    blocks["confidence_recalibration_signal"] = DoctrineBlock(
        topic="confidence_recalibration_signal",
        keywords=["confidence", "recalibrate", "threshold", "certainty", "adjust confidence"],
        conclusion_template="CONFIDENCE_RECALIBRATION signal for engine {target_engine_id}, topic '{target_doctrine_topic}'. Current confidence: {current:.2f} -> Proposed: {proposed:.2f}. Basis: {basis}.",
        reasoning_framework="Confidence recalibration adjusts how certain an engine claims to be. Processing: 1) Analyze correction rate per doctrine topic. 2) High correction rate (>20%) -> decrease confidence. 3) High approval rate (>90%) -> increase confidence. 4) Flags on specific fields -> decrease confidence for those fields. 5) Professional overrides always trigger recalibration. 6) Never set confidence above 0.98 (epistemic humility floor). 7) Track calibration history to detect oscillation.",
        key_factors=["correction rate", "approval rate", "flag frequency", "override count", "calibration history"],
        primary_authority=["Epistemic Calibration Framework v1.0"],
        burden_holder="system",
        adversary_position="Confidence scores are inherently subjective; recalibration based on limited feedback may introduce more noise than signal.",
        counter_arguments=["Small feedback sample may misrepresent true accuracy", "Confidence and correctness are different dimensions", "Over-calibration leads to low-confidence hedge-everything answers"],
        resolution_strategy="Require minimum 10 feedback items before recalibration. Limit adjustment to +/-0.10 per cycle. Hard floor at 0.30, hard ceiling at 0.98. Log all calibration events.",
        entity_scope="per_engine",
        confidence=0.85,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Confidence Calibration Standard v1.0",
    )

    blocks["error_pattern_detection"] = DoctrineBlock(
        topic="error_pattern_detection",
        keywords=["pattern", "systematic", "recurring error", "bug", "repeated mistake"],
        conclusion_template="ERROR_PATTERN detected in engine {target_engine_id}: '{pattern_description}'. Frequency: {frequency} occurrences in {window} days. Severity: {severity}. Recommended action: {action}.",
        reasoning_framework="Error pattern detection identifies systematic engine failures. Processing: 1) Aggregate corrections, rejections, and flags by engine+topic. 2) Cluster similar errors using semantic similarity. 3) Detect patterns: same error from 3+ independent reviewers = systematic. 4) Classify severity: critical (factual error in core conclusion), high (missing key factor), medium (incomplete analysis), low (formatting/style). 5) Generate bug report with evidence chain. 6) Track pattern resolution status.",
        key_factors=["error clustering", "independent reviewer count", "severity classification", "evidence chain", "resolution status"],
        primary_authority=["Error Pattern Analysis Protocol v1.0"],
        burden_holder="system",
        adversary_position="Perceived patterns may be coincidental; require minimum evidence threshold before declaring a systematic issue.",
        counter_arguments=["Clustering may group unrelated errors", "Severity assessment may be subjective", "Pattern may reflect query bias not engine error"],
        resolution_strategy="Require 3+ independent reviewers reporting similar error. Use semantic similarity threshold of 0.75 for clustering. Always include evidence chain in bug report.",
        entity_scope="per_engine",
        confidence=0.88,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Systematic Error Detection Framework v1.0",
    )

    blocks["training_pair_generation"] = DoctrineBlock(
        topic="training_pair_generation",
        keywords=["training data", "fine-tune", "training pair", "dataset", "learning"],
        conclusion_template="TRAINING_PAIR generated from feedback on engine {target_engine_id}. Input: '{input_summary}'. Expected output: '{output_summary}'. Quality score: {quality:.2f}.",
        reasoning_framework="Every correction and override generates a training pair for future fine-tuning. Processing: 1) Extract (original_query, correct_answer) pair from correction/override. 2) Score pair quality: high if from credentialed reviewer with specific correction, low if vague. 3) Normalize formatting for consistency. 4) Deduplicate against existing training corpus. 5) Tag with engine_id, doctrine_topic, feedback_type for filtered training. 6) Store in TUNING_LOG for batch export.",
        key_factors=["pair quality score", "reviewer credential tier", "specificity of correction", "deduplication status", "domain tags"],
        primary_authority=["Training Data Generation Protocol v1.0"],
        burden_holder="system",
        adversary_position="Training data from corrections may encode reviewer biases; must be curated before use in fine-tuning.",
        counter_arguments=["Single-reviewer corrections may be wrong", "Training pairs may not generalize", "Quality scoring is approximate"],
        resolution_strategy="Generate pairs from all corrections/overrides. Score by credential tier and specificity. Require human curation before batch fine-tuning use.",
        entity_scope="all_engines",
        confidence=0.80,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Training Data Quality Standard v1.0",
    )

    blocks["impact_tracking"] = DoctrineBlock(
        topic="impact_tracking",
        keywords=["impact", "improvement", "regression", "before after", "effectiveness"],
        conclusion_template="Impact analysis for engine {target_engine_id}: Pre-change quality {pre_quality:.2f}, Post-change quality {post_quality:.2f}. Delta: {delta:+.2f}. Assessment: {assessment}.",
        reasoning_framework="Impact tracking measures whether feedback-driven changes actually improved engine quality. Processing: 1) Record quality baseline before applying tuning signal. 2) Monitor post-change quality for 48-hour window. 3) Compare approval/rejection ratios before and after. 4) If quality improved (delta > +0.05), mark change as beneficial. 5) If quality declined (delta < -0.05), trigger auto-rollback. 6) If neutral (|delta| <= 0.05), keep change but flag for review.",
        key_factors=["baseline quality score", "post-change quality score", "monitoring window", "rollback trigger threshold", "statistical significance"],
        primary_authority=["Change Impact Assessment Protocol v1.0"],
        burden_holder="system",
        adversary_position="48-hour monitoring window may be too short for rare queries; long-tail regressions may escape detection.",
        counter_arguments=["Sample size in 48 hours may be insufficient", "Quality improvement may be unrelated to change", "Regression may be caused by external factors"],
        resolution_strategy="Use 48-hour primary window with 7-day extended monitoring. Require minimum 5 feedback items in window for statistical validity. Auto-rollback on >10% quality decline.",
        entity_scope="per_engine",
        confidence=0.83,
        confidence_stratification="DISCLOSURE",
        controlling_precedent="Change Impact Measurement Standard v1.0",
    )

    blocks["auto_apply_rules"] = DoctrineBlock(
        topic="auto_apply_rules",
        keywords=["auto apply", "automatic", "threshold", "no review", "instant"],
        conclusion_template="Auto-apply evaluation for signal {signal_id}: Confidence={confidence:.2f}, Threshold={threshold:.2f}. Eligible: {eligible}. Reason: {reason}.",
        reasoning_framework="Auto-apply rules determine whether tuning signals can be applied without human review. Processing: 1) Check signal confidence against AUTO_APPLY_CONFIDENCE_THRESHOLD (0.92). 2) Verify no conflicting feedback exists. 3) Verify change magnitude is within auto-apply scope (minor wording, confidence adjustments). 4) Major conclusion changes NEVER auto-apply regardless of confidence. 5) First-time corrections on a topic require human review. 6) Subsequent corrections on same topic with consistent direction can auto-apply.",
        key_factors=["signal confidence", "conflict check", "change magnitude", "first-time vs repeat", "direction consistency"],
        primary_authority=["Auto-Apply Governance Protocol v1.0"],
        burden_holder="system",
        adversary_position="Auto-apply trades review quality for speed; errors in auto-applied changes propagate immediately to all users.",
        counter_arguments=["Speed of correction matters for user trust", "Human review creates bottleneck", "High-confidence signals are rarely wrong"],
        resolution_strategy="Conservative auto-apply: only minor changes with confidence >= 0.92, no conflicts, and consistent direction from 3+ items. Everything else requires human review.",
        entity_scope="all_engines",
        confidence=0.90,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Automated Change Governance v1.0",
    )

    blocks["feedback_routing"] = DoctrineBlock(
        topic="feedback_routing",
        keywords=["route", "dispatch", "target engine", "classify", "assign feedback"],
        conclusion_template="Feedback routed to engine {target_engine_id}, doctrine '{target_doctrine_topic}', field '{target_response_field}'. Routing confidence: {routing_confidence:.2f}.",
        reasoning_framework="Feedback must be routed to the correct engine, doctrine block, and response field. Processing: 1) Parse target_engine_id from feedback. 2) If doctrine_topic not specified, infer from original_query using keyword matching. 3) If response_field not specified, infer from correction_text context. 4) Validate target engine exists in registry. 5) Validate doctrine topic exists in target engine's cache. 6) If routing uncertain, flag for manual classification.",
        key_factors=["target engine validation", "doctrine topic inference", "field inference", "routing confidence", "manual classification flag"],
        primary_authority=["Feedback Routing Protocol v1.0"],
        burden_holder="system",
        adversary_position="Automated routing may misclassify feedback, applying corrections to wrong doctrine blocks.",
        counter_arguments=["Inference from query text is imprecise", "Multiple doctrines may match", "Engine registry may be stale"],
        resolution_strategy="Route with confidence score. High confidence (>0.85) auto-route. Medium (0.60-0.85) route with review flag. Low (<0.60) hold for manual classification.",
        entity_scope="all_engines",
        confidence=0.82,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Feedback Routing Standard v1.0",
    )

    blocks["quality_dashboard_metrics"] = DoctrineBlock(
        topic="quality_dashboard_metrics",
        keywords=["quality", "metrics", "dashboard", "accuracy", "kpi", "performance"],
        conclusion_template="Quality metrics for engine {target_engine_id}: Accuracy={accuracy:.1%}, Approval rate={approval_rate:.1%}, Correction rate={correction_rate:.1%}, Avg rating={avg_rating:.1f}/5. Trend: {trend}.",
        reasoning_framework="Quality metrics provide a comprehensive view of engine health. Processing: 1) Calculate accuracy rate: (approvals + high ratings) / total feedback. 2) Calculate correction rate: corrections / total feedback. 3) Calculate average rating from 1-5 ratings. 4) Detect trends over rolling 7-day and 30-day windows. 5) Segment by issue category for granular insights. 6) Compare across engines for fleet-wide health assessment.",
        key_factors=["accuracy rate", "correction rate", "average rating", "trend direction", "cross-engine comparison"],
        primary_authority=["Engine Quality Metrics Standard v1.0"],
        burden_holder="system",
        adversary_position="Metrics can be gamed; focus on metric trends rather than absolute values.",
        counter_arguments=["Feedback volume varies by engine popularity", "Selection bias in who provides feedback", "Metrics lag behind actual quality changes"],
        resolution_strategy="Report all metrics with confidence intervals based on sample size. Normalize by feedback volume. Flag engines with insufficient feedback for reliable metrics.",
        entity_scope="fleet_wide",
        confidence=0.87,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Quality Measurement Framework v1.0",
    )

    blocks["regression_detection"] = DoctrineBlock(
        topic="regression_detection",
        keywords=["regression", "decline", "worse", "degradation", "quality drop"],
        conclusion_template="Regression analysis for engine {target_engine_id}: {regression_found}. Window: {window_days} days. Pre-change score: {pre:.2f}, Current score: {current:.2f}. Delta: {delta:+.2f}.",
        reasoning_framework="Regression detection catches quality declines after changes. Processing: 1) Maintain baseline quality score per engine per doctrine topic. 2) After any tuning signal application, start 48-hour monitoring. 3) Compare post-change quality to baseline using weighted feedback metrics. 4) If quality drops >10%, trigger auto-rollback. 5) If quality drops 5-10%, alert engine maintainer. 6) Track all regressions for root cause analysis.",
        key_factors=["baseline score", "post-change score", "monitoring window", "rollback threshold", "root cause classification"],
        primary_authority=["Regression Detection Protocol v1.0"],
        burden_holder="system",
        adversary_position="Not all quality drops are regressions; external factors (query distribution change, seasonal topics) can cause apparent declines.",
        counter_arguments=["Monitoring window may be too short", "Quality metrics may not capture all dimensions", "Auto-rollback may undo good changes based on noise"],
        resolution_strategy="Use multiple quality dimensions. Require >5 feedback items for regression call. Auto-rollback on >10% decline. Alert on 5-10%. Investigate root cause for all regressions.",
        entity_scope="per_engine",
        confidence=0.85,
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Regression Detection Standard v1.0",
    )

    _extra_topics = [
        ("feedback_deduplication", ["dedup", "duplicate", "same feedback", "repeated"], "Deduplicate identical or near-identical feedback items from the same or different reviewers to prevent signal inflation. Uses hash-based exact dedup and semantic similarity for near-dedup. Threshold: 0.92 cosine similarity."),
        ("reviewer_reputation", ["reputation", "track record", "reliability", "reviewer score"], "Track reviewer reliability over time. Reviewers whose corrections are later confirmed get reputation boost; those whose corrections are later overridden get reputation penalty. Reputation modifies credential tier weight."),
        ("batch_processing", ["batch", "bulk", "bulk feedback", "import"], "Process multiple feedback items in a single batch for efficiency. Validate all items first, then process in parallel. Report batch-level statistics."),
        ("feedback_expiration", ["expire", "stale", "old feedback", "decay"], "Feedback signals decay over time. Corrections older than 90 days receive 0.5x weight. Ratings older than 30 days excluded from rolling average. Override corrections never expire."),
        ("cross_engine_patterns", ["cross engine", "fleet pattern", "system-wide", "common error"], "Detect feedback patterns that span multiple engines, indicating systemic issues in shared components like cloud retriever or semantic normalization."),
        ("feedback_api_validation", ["api", "validate input", "schema", "malformed"], "Validate all incoming feedback against the FeedbackItem schema. Reject malformed items with descriptive error messages. Rate-limit submissions per reviewer."),
        ("tuning_queue_management", ["queue", "pending signals", "backlog", "priority queue"], "Manage the queue of pending tuning signals. Priority: OVERRIDE > CORRECTION > FLAG > REJECTION > SUGGESTION > RATING. Process highest-priority first. Age-based escalation for stale items."),
        ("rollback_execution", ["rollback", "revert", "undo", "restore"], "Execute rollback of a previously applied tuning signal. Restore doctrine block from pre-change snapshot. Log rollback event. Notify engine maintainer."),
        ("feedback_analytics", ["analytics", "trends", "visualization", "report"], "Generate analytics reports on feedback patterns. Include volume trends, reviewer activity, correction accuracy, engine quality trajectories. Export as JSON for dashboard consumption."),
        ("domain_expertise_mapping", ["domain", "expertise", "specialization", "scope"], "Map reviewer credentials to engine domains. Attorney -> Legal engines (LG*), CPA -> Tax/Financial (TX*, E04), Landman -> Landman engines (LM*). Cross-domain reviews receive 0.8x weight."),
        ("feedback_prioritization", ["priority", "urgent", "critical feedback", "important"], "Prioritize feedback processing based on: 1) Feedback type weight, 2) Reviewer credential tier, 3) Target engine criticality, 4) Aggregation count. Critical engines (Tax, Legal) get 1.5x priority multiplier."),
        ("conflict_escalation", ["escalate", "human review", "manual", "arbitration"], "When automated conflict resolution fails, escalate to human arbitrator. Provide full evidence package: all conflicting feedback, reviewer credentials, current doctrine, proposed changes."),
        ("feedback_notification", ["notify", "alert", "email", "webhook"], "Send notifications when: 1) High-priority feedback received, 2) Auto-apply executed, 3) Regression detected, 4) Conflict requires resolution. Channels: webhook, audit log, OmniSync broadcast."),
        ("seasonal_adjustment", ["seasonal", "temporal", "time-based", "periodic"], "Adjust feedback processing for temporal patterns. Tax engines get higher correction weight during filing season. Legal engines adjust for legislative changes. Detect and account for seasonal query distribution shifts."),
        ("feedback_provenance", ["provenance", "chain of custody", "audit trail", "traceability"], "Maintain full provenance chain for every tuning signal: which feedback items contributed, what weight each carried, what the pre-change state was, who approved (or auto-approved), and what the post-change impact was."),
    ]

    for topic, kws, framework in _extra_topics:
        blocks[topic] = DoctrineBlock(
            topic=topic,
            keywords=kws,
            conclusion_template=f"Analysis of {topic.replace('_', ' ')} for target engine. {framework[:80]}...",
            reasoning_framework=framework,
            key_factors=kws[:3] + ["evidence quality", "aggregation count"],
            primary_authority=["ECHO Feedback Processing Standard v1.0"],
            burden_holder="system",
            adversary_position="Automated processing may introduce bias or error.",
            counter_arguments=["Limited sample size", "Reviewer bias", "System constraints"],
            resolution_strategy=f"Apply {topic} rules with validation and logging.",
            entity_scope="per_engine",
            confidence=0.80,
            confidence_stratification="DEFENSIBLE",
            controlling_precedent=f"{topic.replace('_', ' ').title()} Protocol v1.0",
        )

    return blocks


DOCTRINE_CACHE: Dict[str, DoctrineBlock] = _build_doctrine_cache()
_KEYWORD_INDEX: Dict[str, List[str]] = defaultdict(list)
for _topic, _block in DOCTRINE_CACHE.items():
    for _kw in _block.keywords:
        _KEYWORD_INDEX[_kw.lower()].append(_topic)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-6: SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

_NORMALIZATION_MAP: Dict[str, str] = {
    "fix": "correction", "wrong": "correction", "error": "correction", "mistake": "correction",
    "incorrect": "correction", "star": "rating", "score": "rating", "stars": "rating",
    "bad": "rejection", "useless": "rejection", "terrible": "rejection",
    "good": "approval", "correct": "approval", "right": "approval", "accurate": "approval",
    "improve": "suggestion", "better": "suggestion", "enhance": "suggestion",
    "field error": "flag", "wrong field": "flag", "specific error": "flag",
    "expert says": "override", "professional answer": "override",
    "tune": "tuning", "adjust": "tuning", "calibrate": "tuning",
    "pattern": "error pattern", "systematic": "error pattern", "recurring": "error pattern",
    "rollback": "rollback", "revert": "rollback", "undo": "rollback",
}


def normalize_query(text: str) -> str:
    lowered = text.lower().strip()
    for source, target in _NORMALIZATION_MAP.items():
        lowered = lowered.replace(source, target)
    return lowered


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

_AUTHORITY_WEIGHTS: Dict[str, float] = {
    "Professional Override Authority Protocol": 1.0,
    "ECHO Feedback Processing Standard v1.0": 0.95,
    "Credential Verification Standard": 0.93,
    "TIE Quality Assurance Framework": 0.92,
    "Doctrine Lifecycle Management Protocol": 0.90,
    "Conflict Resolution Protocol v1.0": 0.88,
    "Auto-Apply Governance Protocol v1.0": 0.87,
    "Quality Metrics Framework": 0.85,
    "Feedback Routing Protocol v1.0": 0.83,
    "Training Data Generation Protocol v1.0": 0.80,
    "Enhancement Request Protocol": 0.75,
}


def resolve_authority(authorities: List[str]) -> Tuple[float, str]:
    if not authorities:
        return 0.5, "no_authority"
    best_weight = 0.0
    best_auth = authorities[0]
    for auth in authorities:
        w = _AUTHORITY_WEIGHTS.get(auth, 0.5)
        if w > best_weight:
            best_weight = w
            best_auth = auth
    return best_weight, best_auth


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def stratify_confidence(score: float) -> ConfidenceLevel:
    if score >= 0.85:
        return ConfidenceLevel.DEFENSIBLE
    if score >= 0.70:
        return ConfidenceLevel.AGGRESSIVE
    if score >= 0.50:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════════

def score_fact_fragility(feedback: FeedbackItem) -> Dict[str, Any]:
    verifiability = 0.5
    recharacterization_risk = 0.3
    testimony_dependence = 0.4

    if feedback.feedback_type == FeedbackType.CORRECTION:
        verifiability = 0.9 if feedback.correction_text else 0.6
        recharacterization_risk = 0.2
        testimony_dependence = CREDENTIAL_TIERS.get(feedback.reviewer_role.value, 0.5)
    elif feedback.feedback_type == FeedbackType.OVERRIDE:
        verifiability = 0.95
        recharacterization_risk = 0.1
        testimony_dependence = CREDENTIAL_TIERS.get(feedback.reviewer_role.value, 0.5)
    elif feedback.feedback_type == FeedbackType.RATING:
        verifiability = 0.3
        recharacterization_risk = 0.6
        testimony_dependence = 0.2
    elif feedback.feedback_type == FeedbackType.REJECTION:
        verifiability = 0.4
        recharacterization_risk = 0.5
        testimony_dependence = 0.3
    elif feedback.feedback_type == FeedbackType.FLAG:
        verifiability = 0.7
        recharacterization_risk = 0.3
        testimony_dependence = 0.5

    fragility = 1.0 - (verifiability * 0.4 + (1.0 - recharacterization_risk) * 0.3 + testimony_dependence * 0.3)
    return {
        "verifiability": round(verifiability, 3),
        "recharacterization_risk": round(recharacterization_risk, 3),
        "testimony_dependence": round(testimony_dependence, 3),
        "fragility_score": round(fragility, 3),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, mode: str, zone: str, answer: str) -> str:
    payload = f"{ENGINE_ID}|{query}|{mode}|{zone}|{answer}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-8: TELEMETRY + TIE-11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self) -> None:
        self.queries_total: int = 0
        self.queries_by_mode: Dict[str, int] = defaultdict(int)
        self.queries_by_type: Dict[str, int] = defaultdict(int)
        self.latencies: List[float] = []
        self.errors: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.feedback_processed: int = 0
        self.signals_generated: int = 0
        self.auto_applied: int = 0
        self.conflicts_detected: int = 0
        self.rollbacks: int = 0
        self.start_time: float = time.time()

    def record_query(self, mode: str, latency_ms: float, cache_hit: bool) -> None:
        self.queries_total += 1
        self.queries_by_mode[mode] += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_feedback(self, feedback_type: str) -> None:
        self.feedback_processed += 1
        self.queries_by_type[feedback_type] += 1

    def record_signal(self, auto_applied: bool = False) -> None:
        self.signals_generated += 1
        if auto_applied:
            self.auto_applied += 1

    def record_error(self) -> None:
        self.errors += 1

    def snapshot(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_latency = statistics.mean(self.latencies) if self.latencies else 0.0
        p95_latency = sorted(self.latencies)[int(len(self.latencies) * 0.95)] if len(self.latencies) >= 20 else avg_latency
        hit_rate = self.cache_hits / max(self.queries_total, 1)
        return {
            "engine_id": ENGINE_ID,
            "uptime_seconds": round(uptime, 1),
            "queries_total": self.queries_total,
            "queries_by_mode": dict(self.queries_by_mode),
            "queries_by_type": dict(self.queries_by_type),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "cache_hit_rate": round(hit_rate, 3),
            "errors": self.errors,
            "error_rate": round(self.errors / max(self.queries_total, 1), 4),
            "feedback_processed": self.feedback_processed,
            "signals_generated": self.signals_generated,
            "auto_applied": self.auto_applied,
            "conflicts_detected": self.conflicts_detected,
            "rollbacks": self.rollbacks,
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    def __init__(self) -> None:
        self.baseline_scores: Dict[str, float] = {}
        self.current_scores: Dict[str, float] = {}
        self.drift_events: List[Dict[str, Any]] = []

    def set_baseline(self, engine_id: str, score: float) -> None:
        self.baseline_scores[engine_id] = score

    def update_current(self, engine_id: str, score: float) -> Optional[Dict[str, Any]]:
        self.current_scores[engine_id] = score
        baseline = self.baseline_scores.get(engine_id)
        if baseline is None:
            self.set_baseline(engine_id, score)
            return None
        drift = score - baseline
        if abs(drift) > 0.10:
            event = {
                "engine_id": engine_id,
                "baseline": baseline,
                "current": score,
                "drift": round(drift, 4),
                "direction": "improvement" if drift > 0 else "regression",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.drift_events.append(event)
            logger.warning(f"DRIFT DETECTED: {engine_id} drift={drift:+.4f}")
            return event
        return None

    def get_drift_report(self) -> Dict[str, Any]:
        return {
            "baselines": dict(self.baseline_scores),
            "current": dict(self.current_scores),
            "events": self.drift_events[-50:],
            "engines_monitored": len(self.baseline_scores),
        }


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    def __init__(self) -> None:
        self.triggered: Dict[str, int] = defaultdict(int)
        self.missed: Dict[str, int] = defaultdict(int)
        self.total_queries: int = 0

    def record_hit(self, topic: str) -> None:
        self.triggered[topic] += 1
        self.total_queries += 1

    def record_miss(self, query: str) -> None:
        self.missed[query[:100]] += 1
        self.total_queries += 1

    def get_coverage_report(self) -> Dict[str, Any]:
        total_doctrines = len(DOCTRINE_CACHE)
        triggered_doctrines = len(self.triggered)
        coverage_pct = triggered_doctrines / max(total_doctrines, 1)
        top_triggered = sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10]
        top_missed = sorted(self.missed.items(), key=lambda x: x[1], reverse=True)[:10]
        untriggered = [t for t in DOCTRINE_CACHE if t not in self.triggered]
        return {
            "total_doctrines": total_doctrines,
            "triggered_doctrines": triggered_doctrines,
            "coverage_percent": round(coverage_pct * 100, 1),
            "total_queries": self.total_queries,
            "top_triggered": top_triggered,
            "top_missed": top_missed,
            "untriggered_doctrines": untriggered[:20],
            "epistemic_gaps": top_missed[:5],
        }


COVERAGE_MAP = CoverageMap()


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK STORE — in-memory with JSONL persistence
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackStore:
    def __init__(self) -> None:
        self.items: List[FeedbackItem] = []
        self.by_engine: Dict[str, List[FeedbackItem]] = defaultdict(list)
        self.by_topic: Dict[str, List[FeedbackItem]] = defaultdict(list)
        self.signals: List[TuningSignal] = []
        self.applied_signals: List[TuningSignal] = []
        self.conflicts: List[Dict[str, Any]] = []
        self.quality_baselines: Dict[str, float] = {}
        self._seen_hashes: Set[str] = set()

    def _dedup_hash(self, fb: FeedbackItem) -> str:
        payload = f"{fb.target_engine_id}|{fb.feedback_type.value}|{fb.reviewer_id}|{fb.correction_text or ''}|{fb.comment or ''}"
        return hashlib.md5(payload.encode()).hexdigest()

    def add(self, fb: FeedbackItem) -> bool:
        h = self._dedup_hash(fb)
        if h in self._seen_hashes:
            logger.info(f"Duplicate feedback detected, skipping: {fb.feedback_id}")
            return False
        self._seen_hashes.add(h)
        self.items.append(fb)
        self.by_engine[fb.target_engine_id].append(fb)
        if fb.target_doctrine_topic:
            self.by_topic[fb.target_doctrine_topic].append(fb)
        self._persist_item(fb)
        return True

    def _persist_item(self, fb: FeedbackItem) -> None:
        try:
            with open(AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps({"type": "feedback", "data": fb.model_dump()}, default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist feedback: {exc}")

    def get_engine_feedback(self, engine_id: str, feedback_type: Optional[FeedbackType] = None) -> List[FeedbackItem]:
        items = self.by_engine.get(engine_id, [])
        if feedback_type:
            items = [i for i in items if i.feedback_type == feedback_type]
        return items

    def get_aggregation(self, engine_id: str, topic: Optional[str] = None) -> Dict[str, Any]:
        items = self.by_engine.get(engine_id, [])
        if topic:
            items = [i for i in items if i.target_doctrine_topic == topic]
        if not items:
            return {"count": 0, "types": {}, "avg_rating": None, "consensus": None}
        type_counts: Dict[str, int] = defaultdict(int)
        ratings: List[int] = []
        corrections: List[str] = []
        for item in items:
            type_counts[item.feedback_type.value] += 1
            if item.rating is not None:
                ratings.append(item.rating)
            if item.correction_text:
                corrections.append(item.correction_text)
        avg_rating = statistics.mean(ratings) if ratings else None
        correction_consensus = None
        if len(corrections) >= 2:
            unique = set(corrections)
            most_common = max(unique, key=lambda c: corrections.count(c))
            correction_consensus = corrections.count(most_common) / len(corrections)
        return {
            "count": len(items),
            "types": dict(type_counts),
            "avg_rating": round(avg_rating, 2) if avg_rating else None,
            "correction_consensus": round(correction_consensus, 3) if correction_consensus else None,
            "unique_reviewers": len(set(i.reviewer_id for i in items)),
        }

    def add_signal(self, signal: TuningSignal) -> None:
        self.signals.append(signal)
        self._persist_signal(signal)

    def _persist_signal(self, signal: TuningSignal) -> None:
        try:
            with open(TUNING_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps({"type": "tuning_signal", "data": signal.model_dump()}, default=str) + "\n")
        except Exception as exc:
            logger.error(f"Failed to persist signal: {exc}")

    def get_pending_signals(self, engine_id: Optional[str] = None) -> List[TuningSignal]:
        signals = [s for s in self.signals if s.status == "pending"]
        if engine_id:
            signals = [s for s in signals if s.target_engine_id == engine_id]
        return signals

    def quality_score(self, engine_id: str) -> float:
        items = self.by_engine.get(engine_id, [])
        if not items:
            return 0.5
        positive = sum(1 for i in items if i.feedback_type in (FeedbackType.APPROVAL,) or (i.rating and i.rating >= 4))
        negative = sum(1 for i in items if i.feedback_type in (FeedbackType.CORRECTION, FeedbackType.REJECTION, FeedbackType.OVERRIDE) or (i.rating and i.rating <= 2))
        total = positive + negative
        if total == 0:
            return 0.5
        return round(positive / total, 4)


FEEDBACK_STORE = FeedbackStore()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackDecomposer:
    @staticmethod
    def decompose(feedback: FeedbackItem) -> List[Dict[str, Any]]:
        components: List[Dict[str, Any]] = []
        components.append({
            "category": IssueCategory.CREDENTIAL_VALIDATION.value,
            "description": f"Validate reviewer {feedback.reviewer_id} credentials ({feedback.reviewer_role.value})",
            "weight": 0.15,
        })
        type_map = {
            FeedbackType.CORRECTION: IssueCategory.CORRECTION_PROCESSING,
            FeedbackType.RATING: IssueCategory.RATING_AGGREGATION,
            FeedbackType.REJECTION: IssueCategory.CORRECTION_PROCESSING,
            FeedbackType.APPROVAL: IssueCategory.RATING_AGGREGATION,
            FeedbackType.SUGGESTION: IssueCategory.SIGNAL_GENERATION,
            FeedbackType.FLAG: IssueCategory.CORRECTION_PROCESSING,
            FeedbackType.OVERRIDE: IssueCategory.CORRECTION_PROCESSING,
        }
        primary_cat = type_map.get(feedback.feedback_type, IssueCategory.FEEDBACK_ROUTING)
        components.append({
            "category": primary_cat.value,
            "description": f"Process {feedback.feedback_type.value} for engine {feedback.target_engine_id}",
            "weight": 0.35,
        })
        components.append({
            "category": IssueCategory.SIGNAL_GENERATION.value,
            "description": "Generate tuning signals from processed feedback",
            "weight": 0.25,
        })
        components.append({
            "category": IssueCategory.CONFLICT_RESOLUTION.value,
            "description": "Check for conflicts with existing feedback",
            "weight": 0.10,
        })
        components.append({
            "category": IssueCategory.IMPACT_TRACKING.value,
            "description": "Record feedback for impact tracking",
            "weight": 0.10,
        })
        components.append({
            "category": IssueCategory.QUALITY_METRICS.value,
            "description": "Update quality metrics",
            "weight": 0.05,
        })
        return components


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_zone_rules(zone: AnalysisZone, answer: str, confidence: float) -> Tuple[str, str]:
    caveat = ""
    if zone == AnalysisZone.PLANNING:
        caveat = "This feedback analysis is for planning purposes. Tuning signals should be reviewed before application."
    elif zone == AnalysisZone.AUDIT:
        caveat = "AUDIT MODE: Full provenance chain included. All feedback items and signal derivations are traceable."
        answer = f"[AUDIT] {answer}"
    elif zone == AnalysisZone.REPORTING:
        if confidence < 0.70:
            caveat = "Confidence below reporting threshold. Results should be verified before inclusion in reports."
    return answer, caveat


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK PROCESSING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackProcessor:
    def __init__(self, store: FeedbackStore) -> None:
        self.store = store

    def validate_credentials(self, feedback: FeedbackItem) -> Tuple[bool, float, str]:
        tier = CREDENTIAL_TIERS.get(feedback.reviewer_role.value, 0.50)
        if feedback.feedback_type in (FeedbackType.CORRECTION, FeedbackType.OVERRIDE):
            if tier < 0.85:
                return False, tier, f"Credential tier {tier:.2f} below 0.85 threshold for {feedback.feedback_type.value}"
        return True, tier, f"Credential tier {tier:.2f} accepted for {feedback.feedback_type.value}"

    def detect_conflicts(self, feedback: FeedbackItem) -> List[Dict[str, Any]]:
        existing = self.store.get_engine_feedback(feedback.target_engine_id)
        window = datetime.now(timezone.utc) - timedelta(hours=CONFLICT_DETECTION_WINDOW_HOURS)
        conflicts: List[Dict[str, Any]] = []
        for item in existing:
            try:
                item_ts = datetime.fromisoformat(item.timestamp.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                continue
            if item_ts < window:
                continue
            if item.target_doctrine_topic != feedback.target_doctrine_topic:
                continue
            if item.feedback_type in (FeedbackType.CORRECTION, FeedbackType.OVERRIDE) and feedback.feedback_type in (FeedbackType.CORRECTION, FeedbackType.OVERRIDE):
                if item.correction_text and feedback.correction_text and item.correction_text.strip().lower() != feedback.correction_text.strip().lower():
                    conflicts.append({
                        "existing_feedback_id": item.feedback_id,
                        "existing_correction": item.correction_text[:200],
                        "new_correction": feedback.correction_text[:200] if feedback.correction_text else "",
                        "existing_reviewer": item.reviewer_id,
                        "new_reviewer": feedback.reviewer_id,
                        "existing_tier": CREDENTIAL_TIERS.get(item.reviewer_role.value, 0.50),
                        "new_tier": CREDENTIAL_TIERS.get(feedback.reviewer_role.value, 0.50),
                    })
        return conflicts

    def generate_signals(self, feedback: FeedbackItem, credential_tier: float, conflicts: List[Dict[str, Any]]) -> List[TuningSignal]:
        signals: List[TuningSignal] = []
        weight = FEEDBACK_WEIGHT.get(feedback.feedback_type.value, 0.3)
        confidence = weight * credential_tier

        if feedback.feedback_type in (FeedbackType.CORRECTION, FeedbackType.OVERRIDE):
            auto = confidence >= AUTO_APPLY_CONFIDENCE_THRESHOLD and not conflicts
            signals.append(TuningSignal(
                signal_type=TuningSignalType.DOCTRINE_UPDATE,
                target_engine_id=feedback.target_engine_id,
                target_doctrine_topic=feedback.target_doctrine_topic,
                proposed_change={
                    "type": "conclusion_update",
                    "original": feedback.original_response,
                    "corrected": feedback.correction_text,
                    "field": feedback.target_response_field,
                },
                confidence=round(confidence, 4),
                source_feedback_ids=[feedback.feedback_id],
                auto_apply=auto,
            ))
            signals.append(TuningSignal(
                signal_type=TuningSignalType.TRAINING_PAIR,
                target_engine_id=feedback.target_engine_id,
                target_doctrine_topic=feedback.target_doctrine_topic,
                proposed_change={
                    "input": feedback.original_query,
                    "expected_output": feedback.correction_text,
                    "reviewer_role": feedback.reviewer_role.value,
                    "quality_score": round(confidence, 3),
                },
                confidence=round(confidence, 4),
                source_feedback_ids=[feedback.feedback_id],
                auto_apply=False,
            ))

        elif feedback.feedback_type == FeedbackType.REJECTION:
            aggregation = self.store.get_aggregation(feedback.target_engine_id, feedback.target_doctrine_topic)
            rejection_count = aggregation.get("types", {}).get("REJECTION", 0) + 1
            if rejection_count >= MIN_AGGREGATION_COUNT:
                signals.append(TuningSignal(
                    signal_type=TuningSignalType.ERROR_PATTERN,
                    target_engine_id=feedback.target_engine_id,
                    target_doctrine_topic=feedback.target_doctrine_topic,
                    proposed_change={
                        "pattern": "high_rejection_rate",
                        "rejection_count": rejection_count,
                        "comment": feedback.comment,
                    },
                    confidence=round(min(rejection_count / 10, 0.95), 4),
                    source_feedback_ids=[feedback.feedback_id],
                ))

        elif feedback.feedback_type == FeedbackType.FLAG:
            signals.append(TuningSignal(
                signal_type=TuningSignalType.CONFIDENCE_RECALIBRATION,
                target_engine_id=feedback.target_engine_id,
                target_doctrine_topic=feedback.target_doctrine_topic,
                proposed_change={
                    "field": feedback.target_response_field,
                    "action": "decrease_confidence",
                    "delta": -0.05,
                    "reason": feedback.comment,
                },
                confidence=round(confidence, 4),
                source_feedback_ids=[feedback.feedback_id],
            ))

        elif feedback.feedback_type == FeedbackType.SUGGESTION:
            aggregation = self.store.get_aggregation(feedback.target_engine_id, feedback.target_doctrine_topic)
            suggestion_count = aggregation.get("types", {}).get("SUGGESTION", 0) + 1
            if suggestion_count >= MIN_AGGREGATION_COUNT:
                signals.append(TuningSignal(
                    signal_type=TuningSignalType.KEYWORD_ADJUSTMENT,
                    target_engine_id=feedback.target_engine_id,
                    target_doctrine_topic=feedback.target_doctrine_topic,
                    proposed_change={
                        "action": "enhance_routing",
                        "suggestion": feedback.comment,
                        "aggregation_count": suggestion_count,
                    },
                    confidence=round(confidence, 4),
                    source_feedback_ids=[feedback.feedback_id],
                ))

        elif feedback.feedback_type == FeedbackType.APPROVAL:
            quality = self.store.quality_score(feedback.target_engine_id)
            drift_event = DRIFT_WATCHER.update_current(feedback.target_engine_id, quality)
            if drift_event and drift_event["direction"] == "improvement":
                signals.append(TuningSignal(
                    signal_type=TuningSignalType.CONFIDENCE_RECALIBRATION,
                    target_engine_id=feedback.target_engine_id,
                    target_doctrine_topic=feedback.target_doctrine_topic,
                    proposed_change={
                        "action": "increase_confidence",
                        "delta": 0.03,
                        "reason": "approval trend detected",
                        "quality_score": quality,
                    },
                    confidence=round(quality, 4),
                    source_feedback_ids=[feedback.feedback_id],
                ))

        return signals

    def process(self, feedback: FeedbackItem) -> Dict[str, Any]:
        start = time.time()
        valid, tier, cred_msg = self.validate_credentials(feedback)
        if not valid:
            TELEMETRY.record_error()
            return {"status": "rejected", "reason": cred_msg, "feedback_id": feedback.feedback_id}

        added = self.store.add(feedback)
        if not added:
            return {"status": "duplicate", "feedback_id": feedback.feedback_id}

        TELEMETRY.record_feedback(feedback.feedback_type.value)

        conflicts = self.detect_conflicts(feedback)
        if conflicts:
            TELEMETRY.conflicts_detected += 1
            self.store.conflicts.append({
                "feedback_id": feedback.feedback_id,
                "conflicts": conflicts,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        signals = self.generate_signals(feedback, tier, conflicts)
        for signal in signals:
            self.store.add_signal(signal)
            TELEMETRY.record_signal(auto_applied=signal.auto_apply)

        fragility = score_fact_fragility(feedback)
        decomposition = FeedbackDecomposer.decompose(feedback)
        quality = self.store.quality_score(feedback.target_engine_id)
        DRIFT_WATCHER.update_current(feedback.target_engine_id, quality)

        latency = (time.time() - start) * 1000
        TELEMETRY.record_query(feedback.feedback_type.value, latency, False)

        return {
            "status": "processed",
            "feedback_id": feedback.feedback_id,
            "credential_tier": tier,
            "credential_message": cred_msg,
            "conflicts_detected": len(conflicts),
            "conflicts": conflicts[:5],
            "signals_generated": len(signals),
            "signals": [s.model_dump() for s in signals],
            "fragility": fragility,
            "decomposition": decomposition,
            "quality_score": quality,
            "latency_ms": round(latency, 2),
        }


PROCESSOR = FeedbackProcessor(FEEDBACK_STORE)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-1 / TIE-2 / TIE-20: THREE-LAYER RESPONSE + MODES + DEEP ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def _match_doctrine(query: str) -> Optional[DoctrineBlock]:
    normalized = normalize_query(query)
    best_score = 0
    best_block: Optional[DoctrineBlock] = None
    for topic, block in DOCTRINE_CACHE.items():
        score = sum(1 for kw in block.keywords if kw.lower() in normalized)
        if score > best_score:
            best_score = score
            best_block = block
    if best_score > 0:
        return best_block
    return None


def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone,
                         context: Dict[str, Any]) -> QueryResponse:
    start = time.time()
    layer_hit = "doctrine_cache"

    # Layer 1: Doctrine Cache
    block = _match_doctrine(query)
    if block:
        COVERAGE_MAP.record_hit(block.topic)
        answer = block.conclusion_template
        confidence = block.confidence
        authorities = block.primary_authority
        reasoning = block.reasoning_framework
    else:
        COVERAGE_MAP.record_miss(query)
        layer_hit = "semantic_fallback"
        answer = f"No direct doctrine match for query: '{query[:100]}'. Feedback ingestion requires structured FeedbackItem submission via POST /feedback endpoint."
        confidence = 0.45
        authorities = ["ECHO Feedback Processing Standard v1.0"]
        reasoning = "Query did not match any feedback processing doctrine. Recommend submitting structured feedback via the API."

    # Layer 2: Mode formatting
    if mode == ResponseMode.FAST:
        answer = answer[:500]
        reasoning = reasoning[:200]
    elif mode == ResponseMode.DEFENSE:
        answer = f"[DEFENSE MODE] {answer}\n\nAuthority chain: {', '.join(authorities)}.\nConfidence stratification: {stratify_confidence(confidence).value}."
        reasoning = f"[DEFENSE] {reasoning}\n\nCounter-arguments considered: {', '.join(block.counter_arguments[:3]) if block else 'N/A'}."
    elif mode == ResponseMode.MEMO:
        answer = f"MEMORANDUM\n\nRE: {query[:80]}\n\n{answer}\n\nAUTHORITIES:\n" + "\n".join(f"  - {a}" for a in authorities) + f"\n\nREASONING:\n{reasoning}"
        if block:
            answer += f"\n\nKEY FACTORS:\n" + "\n".join(f"  {i+1}. {f}" for i, f in enumerate(block.key_factors))
            answer += f"\n\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"  - {c}" for c in block.counter_arguments)
            answer += f"\n\nRESOLUTION STRATEGY:\n  {block.resolution_strategy}"

    # Layer 3: Zone rules
    answer, caveat = apply_zone_rules(zone, answer, confidence)

    latency = (time.time() - start) * 1000
    cache_hit = layer_hit == "doctrine_cache"
    TELEMETRY.record_query(mode.value, latency, cache_hit)

    det_hash = compute_determinism_hash(query, mode.value, zone.value, answer)

    return QueryResponse(
        query=query,
        mode=mode,
        zone=zone,
        answer=answer,
        confidence=round(confidence, 4),
        confidence_level=stratify_confidence(confidence),
        authorities=authorities,
        reasoning=reasoning[:1000],
        determinism_hash=det_hash,
        latency_ms=round(latency, 2),
        layer_hit=layer_hit,
        disclosure_caveat=caveat,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-15: AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════════

def write_audit_entry(entry_type: str, data: Dict[str, Any]) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_id": ENGINE_ID,
        "entry_type": entry_type,
        "data": data,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-7: VECTOR SEARCH (cloud retriever integration)
# ═══════════════════════════════════════════════════════════════════════════════

async def vector_search_fallback(query: str) -> Optional[str]:
    if CognitionCloudRetriever is None:
        return None
    try:
        cloud = CognitionCloudRetriever()
        results = await cloud.retrieve_all(query, category="feedback")
        if results and hasattr(results, "combined_text"):
            return results.combined_text[:1000]
    except Exception as exc:
        logger.warning(f"Cloud retriever fallback failed: {exc}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-17: FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="E12 Feedback Ingester — processes professional review corrections into engine tuning signals",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# TIE-12: HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "healthy",
        "port": ENGINE_PORT,
        "domain": ENGINE_DOMAIN,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "feedback_count": len(FEEDBACK_STORE.items),
        "pending_signals": len(FEEDBACK_STORE.get_pending_signals()),
        "telemetry": TELEMETRY.snapshot(),
        "uptime_seconds": round(time.time() - TELEMETRY.start_time, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/query")
async def query_endpoint(req: QueryRequest) -> QueryResponse:
    write_audit_entry("query", {"query": req.query, "mode": req.mode.value, "zone": req.zone.value})
    response = three_layer_response(req.query, req.mode, req.zone, req.context)
    return response


@app.post("/feedback")
async def submit_feedback(feedback: FeedbackItem) -> Dict[str, Any]:
    logger.info(f"Feedback received: {feedback.feedback_type.value} for {feedback.target_engine_id} from {feedback.reviewer_id}")
    write_audit_entry("feedback_submission", feedback.model_dump())
    result = PROCESSOR.process(feedback)
    return result


@app.post("/feedback/batch")
async def submit_feedback_batch(items: List[FeedbackItem]) -> Dict[str, Any]:
    results = []
    for item in items:
        result = PROCESSOR.process(item)
        results.append(result)
    processed = sum(1 for r in results if r["status"] == "processed")
    rejected = sum(1 for r in results if r["status"] == "rejected")
    duplicates = sum(1 for r in results if r["status"] == "duplicate")
    return {
        "total": len(items),
        "processed": processed,
        "rejected": rejected,
        "duplicates": duplicates,
        "results": results,
    }


@app.get("/signals")
async def get_signals(engine_id: Optional[str] = None, status: str = "pending") -> Dict[str, Any]:
    if status == "pending":
        signals = FEEDBACK_STORE.get_pending_signals(engine_id)
    elif status == "applied":
        signals = FEEDBACK_STORE.applied_signals
        if engine_id:
            signals = [s for s in signals if s.target_engine_id == engine_id]
    else:
        signals = FEEDBACK_STORE.signals
        if engine_id:
            signals = [s for s in signals if s.target_engine_id == engine_id]
    return {
        "count": len(signals),
        "signals": [s.model_dump() for s in signals[:100]],
    }


@app.post("/signals/{signal_id}/apply")
async def apply_signal(signal_id: str) -> Dict[str, Any]:
    for signal in FEEDBACK_STORE.signals:
        if signal.signal_id == signal_id:
            signal.status = "applied"
            FEEDBACK_STORE.applied_signals.append(signal)
            write_audit_entry("signal_applied", signal.model_dump())
            logger.info(f"Signal {signal_id} applied to {signal.target_engine_id}")
            return {"status": "applied", "signal": signal.model_dump()}
    raise HTTPException(status_code=404, detail=f"Signal {signal_id} not found")


@app.post("/signals/{signal_id}/reject")
async def reject_signal(signal_id: str) -> Dict[str, Any]:
    for signal in FEEDBACK_STORE.signals:
        if signal.signal_id == signal_id:
            signal.status = "rejected"
            write_audit_entry("signal_rejected", signal.model_dump())
            return {"status": "rejected", "signal": signal.model_dump()}
    raise HTTPException(status_code=404, detail=f"Signal {signal_id} not found")


@app.get("/quality/{engine_id}")
async def get_quality(engine_id: str) -> Dict[str, Any]:
    aggregation = FEEDBACK_STORE.get_aggregation(engine_id)
    quality = FEEDBACK_STORE.quality_score(engine_id)
    items = FEEDBACK_STORE.get_engine_feedback(engine_id)
    ratings = [i.rating for i in items if i.rating is not None]
    return {
        "engine_id": engine_id,
        "quality_score": quality,
        "feedback_count": aggregation["count"],
        "type_breakdown": aggregation["types"],
        "avg_rating": aggregation["avg_rating"],
        "correction_consensus": aggregation["correction_consensus"],
        "unique_reviewers": aggregation.get("unique_reviewers", 0),
        "rating_distribution": {str(r): ratings.count(r) for r in range(1, 6)} if ratings else {},
        "confidence_level": stratify_confidence(quality).value,
    }


@app.get("/conflicts")
async def get_conflicts() -> Dict[str, Any]:
    return {
        "count": len(FEEDBACK_STORE.conflicts),
        "conflicts": FEEDBACK_STORE.conflicts[-50:],
    }


@app.get("/coverage")
async def get_coverage() -> Dict[str, Any]:
    return COVERAGE_MAP.get_coverage_report()


@app.get("/drift")
async def get_drift() -> Dict[str, Any]:
    return DRIFT_WATCHER.get_drift_report()


@app.get("/telemetry")
async def get_telemetry() -> Dict[str, Any]:
    return TELEMETRY.snapshot()


@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    return {
        "count": len(DOCTRINE_CACHE),
        "topics": [
            {"topic": t, "keywords": b.keywords, "confidence": b.confidence, "stratification": b.confidence_stratification}
            for t, b in DOCTRINE_CACHE.items()
        ],
    }


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str) -> Dict[str, Any]:
    block = DOCTRINE_CACHE.get(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return {
        "topic": block.topic,
        "keywords": block.keywords,
        "conclusion_template": block.conclusion_template,
        "reasoning_framework": block.reasoning_framework,
        "key_factors": block.key_factors,
        "primary_authority": block.primary_authority,
        "burden_holder": block.burden_holder,
        "adversary_position": block.adversary_position,
        "counter_arguments": block.counter_arguments,
        "resolution_strategy": block.resolution_strategy,
        "confidence": block.confidence,
        "confidence_stratification": block.confidence_stratification,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
