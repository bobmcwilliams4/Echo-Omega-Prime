"""
LG03 REGULATORY COMPLIANCE ENGINE - SEARCH MODULE
Regulation search, CFR lookup, Federal Register monitoring, and compliance search.

Provides:
    - Doctrine-based regulation search with scoring
    - CFR section lookup and cross-referencing
    - Federal Register monitoring for pending rules
    - Enforcement action search by agency and violation type
    - Compliance obligation search by industry and jurisdiction
    - Deadline search with urgency scoring
    - Multi-agency cross-reference search
    - Regulation timeline tracking

Architecture:
    Search operates on the pre-compiled doctrine cache (Layer 1) and
    structured databases (Layer 2). No external API calls.
    All search results are deterministic.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG03 Regulatory Compliance
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from doctrines import (
    AGENCY_PROFILES,
    COMPLIANCE_OBLIGATIONS,
    DOCTRINE_CACHE,
    ENFORCEMENT_ACTIONS,
    INDUSTRY_REGULATION_MAP,
    PREEMPTION_RULES,
    AgencyProfile,
    ComplianceObligation,
    ComplianceStatus,
    EnforcementAction,
    EnforcementSeverity,
    PreemptionRule,
    PreemptionType,
    RegulatoryDoctrineBlock,
    RiskLevel,
    RuleStatus,
    compute_doctrine_match_score,
    get_applicable_doctrines,
    match_doctrine,
)
from semantic import (
    CFRCitation,
    NormalizationResult,
    USCCitation,
    normalize_agency,
    normalize_semantics,
    parse_cfr_citation,
    parse_usc_citation,
)


# ============================================================================
# SEARCH RESULT TYPES
# ============================================================================

@dataclass
class RegulationSearchResult:
    """A single regulation search result with relevance scoring."""
    doctrine_key: str
    topic: str
    agency: str
    relevance_score: int
    risk_level: str
    composite_risk_score: int
    cfr_references: List[str]
    usc_references: List[str]
    summary: str
    penalty_range: str
    criminal_exposure: bool
    applicable_naics: List[str]
    match_type: str  # "doctrine", "cfr", "agency", "keyword"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doctrine_key": self.doctrine_key,
            "topic": self.topic,
            "agency": self.agency,
            "relevance_score": self.relevance_score,
            "risk_level": self.risk_level,
            "composite_risk_score": self.composite_risk_score,
            "cfr_references": self.cfr_references,
            "usc_references": self.usc_references,
            "summary": self.summary,
            "penalty_range": self.penalty_range,
            "criminal_exposure": self.criminal_exposure,
            "applicable_naics": self.applicable_naics,
            "match_type": self.match_type,
        }


@dataclass
class EnforcementSearchResult:
    """Search result for enforcement actions."""
    action_key: str
    agency: str
    violation_category: str
    action_type: str
    penalty_range: str
    criminal_exposure: bool
    statute_basis: str
    relevance_score: int
    mitigating_factors: List[str]
    aggravating_factors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_key": self.action_key,
            "agency": self.agency,
            "violation_category": self.violation_category,
            "action_type": self.action_type,
            "penalty_range": self.penalty_range,
            "criminal_exposure": self.criminal_exposure,
            "statute_basis": self.statute_basis,
            "relevance_score": self.relevance_score,
            "mitigating_factors": self.mitigating_factors,
            "aggravating_factors": self.aggravating_factors,
        }


@dataclass
class ComplianceDeadline:
    """Compliance deadline with urgency scoring."""
    obligation_id: str
    regulation: str
    agency: str
    description: str
    frequency: str
    deadline_type: str
    urgency_score: int  # Higher = more urgent
    required_actions: List[str]
    penalty_for_noncompliance: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "regulation": self.regulation,
            "agency": self.agency,
            "description": self.description,
            "frequency": self.frequency,
            "deadline_type": self.deadline_type,
            "urgency_score": self.urgency_score,
            "required_actions": self.required_actions,
            "penalty_for_noncompliance": self.penalty_for_noncompliance,
        }


@dataclass
class ComplianceGapResult:
    """Result of a compliance gap analysis."""
    entity_name: str
    naics_code: str
    industry_name: str
    total_applicable_doctrines: int
    compliant_count: int
    non_compliant_count: int
    not_assessed_count: int
    gap_score: float  # 0.0 = fully compliant, 1.0 = fully non-compliant
    gaps: List[Dict[str, Any]]
    recommendations: List[str]
    high_risk_gaps: List[Dict[str, Any]]
    determinism_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_name": self.entity_name,
            "naics_code": self.naics_code,
            "industry_name": self.industry_name,
            "total_applicable_doctrines": self.total_applicable_doctrines,
            "compliant_count": self.compliant_count,
            "non_compliant_count": self.non_compliant_count,
            "not_assessed_count": self.not_assessed_count,
            "gap_score": round(self.gap_score, 4),
            "gaps": self.gaps,
            "recommendations": self.recommendations,
            "high_risk_gaps": self.high_risk_gaps,
            "determinism_hash": self.determinism_hash,
        }


@dataclass
class PreemptionAnalysisResult:
    """Result of a preemption analysis."""
    federal_statute: str
    preemption_type: str
    scope: str
    exceptions: List[str]
    key_cases: List[str]
    state_law_status: str
    analysis: str
    determinism_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "federal_statute": self.federal_statute,
            "preemption_type": self.preemption_type,
            "scope": self.scope,
            "exceptions": self.exceptions,
            "key_cases": self.key_cases,
            "state_law_status": self.state_law_status,
            "analysis": self.analysis,
            "determinism_hash": self.determinism_hash,
        }


@dataclass
class SearchResponse:
    """Aggregated search response with multiple result types."""
    query: str
    query_normalized: str
    total_results: int
    regulation_results: List[RegulationSearchResult]
    enforcement_results: List[EnforcementSearchResult]
    deadline_results: List[ComplianceDeadline]
    agencies_detected: List[str]
    cfr_citations_parsed: List[Dict[str, Any]]
    determinism_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "query_normalized": self.query_normalized,
            "total_results": self.total_results,
            "regulation_results": [r.to_dict() for r in self.regulation_results],
            "enforcement_results": [r.to_dict() for r in self.enforcement_results],
            "deadline_results": [r.to_dict() for r in self.deadline_results],
            "agencies_detected": self.agencies_detected,
            "cfr_citations_parsed": self.cfr_citations_parsed,
            "determinism_hash": self.determinism_hash,
        }


# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

def search_regulations(query: str, max_results: int = 20,
                       agency_filter: Optional[str] = None,
                       naics_filter: Optional[str] = None,
                       risk_level_filter: Optional[str] = None) -> SearchResponse:
    """Search the regulation doctrine cache with full semantic analysis.

    Performs:
        1. Semantic normalization of query
        2. CFR/USC citation extraction
        3. Agency detection
        4. Doctrine matching with scoring
        5. Enforcement action matching
        6. Deadline matching

    Args:
        query: Raw search query.
        max_results: Maximum regulation results to return.
        agency_filter: Filter results to a specific agency.
        naics_filter: Filter results to NAICS sector.
        risk_level_filter: Filter by risk level.

    Returns:
        SearchResponse with all matched results.
    """
    norm_result = normalize_semantics(query)
    query_lower = norm_result.normalized.lower()

    # Normalize agency filter
    if agency_filter:
        agency_filter = normalize_agency(agency_filter)

    # Search doctrine cache
    regulation_results: List[RegulationSearchResult] = []
    for key, doctrine in DOCTRINE_CACHE.items():
        # Apply filters
        if agency_filter and doctrine.agency != agency_filter:
            continue
        if naics_filter:
            sector = naics_filter[:2]
            if sector not in doctrine.applicable_naics:
                continue
        if risk_level_filter:
            if doctrine.risk_level.value != risk_level_filter.lower():
                continue

        score = compute_doctrine_match_score(query_lower, doctrine)
        if score >= 10:
            regulation_results.append(RegulationSearchResult(
                doctrine_key=key,
                topic=doctrine.topic,
                agency=doctrine.agency,
                relevance_score=score,
                risk_level=doctrine.risk_level.value,
                composite_risk_score=doctrine.composite_risk_score,
                cfr_references=doctrine.cfr_references,
                usc_references=doctrine.usc_references,
                summary=doctrine.compliance_framework[:300].strip(),
                penalty_range=doctrine.penalty_range,
                criminal_exposure=doctrine.criminal_exposure,
                applicable_naics=doctrine.applicable_naics,
                match_type="doctrine",
            ))

    # Also match by parsed CFR citations
    for cfr_cit in norm_result.cfr_citations:
        for key, doctrine in DOCTRINE_CACHE.items():
            for ref in doctrine.cfr_references:
                if str(cfr_cit.title) in ref and (
                    cfr_cit.part is not None and str(cfr_cit.part) in ref
                ):
                    already_found = any(r.doctrine_key == key for r in regulation_results)
                    if not already_found:
                        regulation_results.append(RegulationSearchResult(
                            doctrine_key=key,
                            topic=doctrine.topic,
                            agency=doctrine.agency,
                            relevance_score=50,
                            risk_level=doctrine.risk_level.value,
                            composite_risk_score=doctrine.composite_risk_score,
                            cfr_references=doctrine.cfr_references,
                            usc_references=doctrine.usc_references,
                            summary=doctrine.compliance_framework[:300].strip(),
                            penalty_range=doctrine.penalty_range,
                            criminal_exposure=doctrine.criminal_exposure,
                            applicable_naics=doctrine.applicable_naics,
                            match_type="cfr",
                        ))

    # Sort by relevance score descending
    regulation_results.sort(key=lambda x: x.relevance_score, reverse=True)
    regulation_results = regulation_results[:max_results]

    # Search enforcement actions
    enforcement_results = search_enforcement_actions(query_lower, agency_filter)

    # Search deadlines
    deadline_results = search_deadlines(query_lower, agency_filter, naics_filter)

    # Total results
    total = len(regulation_results) + len(enforcement_results) + len(deadline_results)

    # Determinism hash
    hash_input = f"{norm_result.determinism_hash}:{total}:{len(regulation_results)}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return SearchResponse(
        query=query,
        query_normalized=norm_result.normalized,
        total_results=total,
        regulation_results=regulation_results,
        enforcement_results=enforcement_results,
        deadline_results=deadline_results,
        agencies_detected=norm_result.agencies_detected,
        cfr_citations_parsed=[c.to_dict() for c in norm_result.cfr_citations],
        determinism_hash=determinism_hash,
    )


def search_enforcement_actions(query_lower: str,
                                agency_filter: Optional[str] = None,
                                max_results: int = 10) -> List[EnforcementSearchResult]:
    """Search enforcement action database.

    Args:
        query_lower: Lowercased query text.
        agency_filter: Optional agency filter.
        max_results: Maximum results.

    Returns:
        List of matching enforcement action results.
    """
    results: List[EnforcementSearchResult] = []

    for key, action in ENFORCEMENT_ACTIONS.items():
        if agency_filter and action.agency != agency_filter:
            continue

        score = 0
        # Agency match
        if action.agency.lower() in query_lower:
            score += 20
        # Violation category match
        for word in action.violation_category.lower().split():
            if len(word) > 3 and word in query_lower:
                score += 15
        # Statute match
        if action.statute_basis.lower() in query_lower:
            score += 25
        # Action type match
        if action.action_type.value in query_lower:
            score += 10
        # Description keyword match
        for word in action.description.lower().split():
            if len(word) > 4 and word in query_lower:
                score += 5

        if score >= 10:
            penalty_display = ""
            if action.penalty_max:
                penalty_display = f"Up to ${action.penalty_max:,.0f}"
                if action.penalty_per_day:
                    penalty_display += f" (${action.penalty_per_day:,.0f}/day)"
                if action.penalty_per_violation:
                    penalty_display += f" per violation"
            if action.criminal_exposure and action.max_imprisonment_years:
                penalty_display += f"; Criminal: up to {action.max_imprisonment_years} years"

            results.append(EnforcementSearchResult(
                action_key=key,
                agency=action.agency,
                violation_category=action.violation_category,
                action_type=action.action_type.value,
                penalty_range=penalty_display,
                criminal_exposure=action.criminal_exposure,
                statute_basis=action.statute_basis,
                relevance_score=score,
                mitigating_factors=action.mitigating_factors,
                aggravating_factors=action.aggravating_factors,
            ))

    results.sort(key=lambda x: x.relevance_score, reverse=True)
    return results[:max_results]


def search_deadlines(query_lower: str,
                     agency_filter: Optional[str] = None,
                     naics_filter: Optional[str] = None,
                     max_results: int = 20) -> List[ComplianceDeadline]:
    """Search compliance obligations for deadline-related information.

    Args:
        query_lower: Lowercased query text.
        agency_filter: Optional agency filter.
        naics_filter: Optional NAICS filter.
        max_results: Maximum results.

    Returns:
        List of compliance deadlines with urgency scoring.
    """
    results: List[ComplianceDeadline] = []
    deadline_keywords = {"deadline", "due date", "filing", "report", "submission",
                         "annual", "quarterly", "when", "frequency"}
    is_deadline_query = any(kw in query_lower for kw in deadline_keywords)

    for obl_key, obligation in COMPLIANCE_OBLIGATIONS.items():
        if agency_filter and obligation.agency != agency_filter:
            continue
        if naics_filter:
            sector = naics_filter[:2]
            if sector not in obligation.applicable_industries and \
                    "All sectors" not in obligation.applicable_industries:
                continue

        score = 0
        # Check keyword relevance
        desc_lower = obligation.description.lower()
        reg_lower = obligation.regulation.lower()
        for word in query_lower.split():
            if len(word) > 3:
                if word in desc_lower:
                    score += 15
                if word in reg_lower:
                    score += 10

        if obligation.agency.lower() in query_lower:
            score += 20

        # Boost for deadline-specific queries
        if is_deadline_query:
            score += 20

        if score >= 10:
            # Compute urgency score based on frequency
            urgency = _compute_urgency_score(obligation.frequency, obligation.deadline_type)

            results.append(ComplianceDeadline(
                obligation_id=obligation.obligation_id,
                regulation=obligation.regulation,
                agency=obligation.agency,
                description=obligation.description,
                frequency=obligation.frequency,
                deadline_type=obligation.deadline_type,
                urgency_score=urgency,
                required_actions=obligation.required_actions,
                penalty_for_noncompliance=obligation.penalty_for_noncompliance,
            ))

    results.sort(key=lambda x: x.urgency_score, reverse=True)
    return results[:max_results]


def _compute_urgency_score(frequency: str, deadline_type: str) -> int:
    """Compute urgency score for a compliance deadline.

    Args:
        frequency: Reporting frequency string.
        deadline_type: Deadline type string.

    Returns:
        Urgency score (0-100, higher = more urgent).
    """
    score = 50  # Base score

    freq_lower = frequency.lower()
    if "daily" in freq_lower or "ongoing" in freq_lower or "event" in freq_lower:
        score += 30
    elif "monthly" in freq_lower:
        score += 20
    elif "quarterly" in freq_lower:
        score += 10
    elif "annual" in freq_lower:
        score += 5

    deadline_lower = deadline_type.lower()
    if "day" in deadline_lower:
        # Extract number of days if present
        day_match = re.search(r"(\d+)\s*(?:calendar|business)?\s*days?", deadline_lower)
        if day_match:
            days = int(day_match.group(1))
            if days <= 4:
                score += 25
            elif days <= 15:
                score += 20
            elif days <= 30:
                score += 15
            elif days <= 60:
                score += 10
            else:
                score += 5

    return min(score, 100)


# ============================================================================
# COMPLIANCE GAP ANALYSIS
# ============================================================================

def analyze_compliance_gaps(entity_name: str, naics_code: str,
                           current_compliance: Dict[str, str]) -> ComplianceGapResult:
    """Analyze compliance gaps for an entity based on its industry.

    Args:
        entity_name: Name of the entity being analyzed.
        naics_code: NAICS code for the entity's industry.
        current_compliance: Dict mapping doctrine_key -> ComplianceStatus value.

    Returns:
        ComplianceGapResult with gap analysis.
    """
    from semantic import NAICS_SECTOR_NAMES, get_naics_sector

    applicable_doctrines = get_applicable_doctrines(naics_code)
    sector_name = get_naics_sector(naics_code) or f"NAICS {naics_code}"

    gaps: List[Dict[str, Any]] = []
    high_risk_gaps: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    compliant_count = 0
    non_compliant_count = 0
    not_assessed_count = 0

    for doctrine_key in applicable_doctrines:
        doctrine = DOCTRINE_CACHE.get(doctrine_key)
        if not doctrine:
            continue

        status_str = current_compliance.get(doctrine_key, ComplianceStatus.PENDING_REVIEW.value)

        if status_str == ComplianceStatus.COMPLIANT.value:
            compliant_count += 1
        elif status_str in (ComplianceStatus.NON_COMPLIANT.value,
                            ComplianceStatus.PARTIALLY_COMPLIANT.value):
            non_compliant_count += 1
            gap_info = {
                "doctrine_key": doctrine_key,
                "topic": doctrine.topic,
                "agency": doctrine.agency,
                "status": status_str,
                "risk_level": doctrine.risk_level.value,
                "composite_risk_score": doctrine.composite_risk_score,
                "penalty_range": doctrine.penalty_range,
                "required_actions": doctrine.required_actions,
                "criminal_exposure": doctrine.criminal_exposure,
            }
            gaps.append(gap_info)

            if doctrine.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
                high_risk_gaps.append(gap_info)
                recommendations.append(
                    f"PRIORITY: Address {doctrine.topic} ({doctrine.agency}) - "
                    f"Risk level: {doctrine.risk_level.value}, "
                    f"Penalties: {doctrine.penalty_range}"
                )
            else:
                recommendations.append(
                    f"Address {doctrine.topic} ({doctrine.agency}) - "
                    f"Risk level: {doctrine.risk_level.value}"
                )
        elif status_str == ComplianceStatus.EXEMPTED.value:
            pass  # Not counted
        else:
            not_assessed_count += 1
            gaps.append({
                "doctrine_key": doctrine_key,
                "topic": doctrine.topic,
                "agency": doctrine.agency,
                "status": "not_assessed",
                "risk_level": doctrine.risk_level.value,
                "composite_risk_score": doctrine.composite_risk_score,
                "penalty_range": doctrine.penalty_range,
                "required_actions": doctrine.required_actions,
                "criminal_exposure": doctrine.criminal_exposure,
            })

    total = len(applicable_doctrines)
    gap_score = 0.0
    if total > 0:
        gap_score = (non_compliant_count + not_assessed_count * 0.5) / total

    # Sort recommendations by priority
    recommendations.sort(key=lambda x: x.startswith("PRIORITY"), reverse=True)

    # Determinism hash
    hash_input = f"{entity_name}:{naics_code}:{json.dumps(current_compliance, sort_keys=True)}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return ComplianceGapResult(
        entity_name=entity_name,
        naics_code=naics_code,
        industry_name=sector_name,
        total_applicable_doctrines=total,
        compliant_count=compliant_count,
        non_compliant_count=non_compliant_count,
        not_assessed_count=not_assessed_count,
        gap_score=gap_score,
        gaps=gaps,
        recommendations=recommendations,
        high_risk_gaps=high_risk_gaps,
        determinism_hash=determinism_hash,
    )


# Need json for hash computation
import json


# ============================================================================
# PREEMPTION ANALYSIS
# ============================================================================

def analyze_preemption(federal_area: str, state_law_description: str) -> PreemptionAnalysisResult:
    """Analyze whether federal law preempts a state/local regulation.

    Args:
        federal_area: Federal regulatory area (e.g., "erisa", "securities", "osha").
        state_law_description: Description of the state law in question.

    Returns:
        PreemptionAnalysisResult with full analysis.
    """
    area_lower = federal_area.lower().strip()

    # Find matching preemption rule
    matched_rule: Optional[PreemptionRule] = None
    matched_key: str = ""

    for key, rule in PREEMPTION_RULES.items():
        rule_words = key.lower().replace("_", " ")
        statute_lower = rule.federal_statute.lower()
        if area_lower in rule_words or area_lower in statute_lower:
            matched_rule = rule
            matched_key = key
            break

    if matched_rule is None:
        # Check doctrines for preemption info
        for key, doctrine in DOCTRINE_CACHE.items():
            if area_lower in key.lower() or area_lower in doctrine.topic.lower():
                hash_input = f"{federal_area}:{state_law_description}:no_specific_rule"
                determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

                state_variations_text = "; ".join(doctrine.state_variations) if doctrine.state_variations else "No specific state variations documented."

                return PreemptionAnalysisResult(
                    federal_statute="; ".join(doctrine.usc_references[:3]),
                    preemption_type=doctrine.preemption_type.value,
                    scope=f"{doctrine.topic} federal regulatory framework",
                    exceptions=doctrine.state_variations,
                    key_cases=[],
                    state_law_status="analysis_required",
                    analysis=(
                        f"Federal {doctrine.topic} regulations ({doctrine.agency}) "
                        f"have {doctrine.preemption_type.value} preemption characteristics. "
                        f"State variations: {state_variations_text} "
                        f"The specific state law described must be analyzed against "
                        f"the federal framework to determine preemption status."
                    ),
                    determinism_hash=determinism_hash,
                )

        hash_input = f"{federal_area}:{state_law_description}:no_match"
        determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
        return PreemptionAnalysisResult(
            federal_statute="Unknown",
            preemption_type=PreemptionType.NONE.value,
            scope="No matching federal regulatory area found",
            exceptions=[],
            key_cases=[],
            state_law_status="no_federal_match",
            analysis=f"No specific federal preemption rule found for area: {federal_area}. "
                     f"State law may apply unless a federal statute specifically preempts.",
            determinism_hash=determinism_hash,
        )

    # Analyze preemption
    state_lower = state_law_description.lower()

    # Check if state law falls within exceptions
    exception_applies = False
    matching_exceptions: List[str] = []
    for exc in matched_rule.exceptions:
        exc_words = [w.lower() for w in exc.split() if len(w) > 3]
        if any(w in state_lower for w in exc_words):
            exception_applies = True
            matching_exceptions.append(exc)

    if exception_applies:
        state_status = "likely_not_preempted"
        analysis_text = (
            f"The federal statute ({matched_rule.federal_statute}) has "
            f"{matched_rule.preemption_type.value} preemption, but the described "
            f"state law appears to fall within recognized exceptions: "
            f"{'; '.join(matching_exceptions)}. "
            f"The state law is likely NOT preempted, though specific analysis of "
            f"the exact state provision is required."
        )
    elif matched_rule.preemption_type == PreemptionType.EXPRESS:
        state_status = "likely_preempted"
        analysis_text = (
            f"The federal statute ({matched_rule.federal_statute}) contains an "
            f"express preemption clause covering: {matched_rule.scope}. "
            f"Unless the state law falls within a recognized exception, "
            f"it is likely preempted. No matching exceptions were identified "
            f"from the description provided."
        )
    elif matched_rule.preemption_type in (PreemptionType.IMPLIED_FIELD,
                                           PreemptionType.IMPLIED_CONFLICT):
        state_status = "possibly_preempted"
        analysis_text = (
            f"The federal statute ({matched_rule.federal_statute}) may impliedly "
            f"preempt state law through {matched_rule.preemption_type.value}. "
            f"Scope: {matched_rule.scope}. "
            f"Implied preemption requires case-specific analysis. "
            f"Key cases: {'; '.join(matched_rule.key_cases[:2])}."
        )
    elif matched_rule.preemption_type == PreemptionType.SAVINGS_CLAUSE:
        state_status = "likely_not_preempted"
        analysis_text = (
            f"The federal statute ({matched_rule.federal_statute}) contains a "
            f"savings clause that generally preserves state law. "
            f"States may impose additional or stricter requirements. "
            f"The state law described is likely NOT preempted unless it "
            f"directly conflicts with specific federal requirements."
        )
    else:
        state_status = "analysis_required"
        analysis_text = (
            f"Preemption analysis for {matched_rule.federal_statute} requires "
            f"detailed review of the specific state provision against the "
            f"federal regulatory framework."
        )

    hash_input = f"{federal_area}:{state_law_description}:{matched_key}:{state_status}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return PreemptionAnalysisResult(
        federal_statute=matched_rule.federal_statute,
        preemption_type=matched_rule.preemption_type.value,
        scope=matched_rule.scope,
        exceptions=matched_rule.exceptions,
        key_cases=matched_rule.key_cases,
        state_law_status=state_status,
        analysis=analysis_text,
        determinism_hash=determinism_hash,
    )


# ============================================================================
# AGENCY SEARCH
# ============================================================================

def search_agency(query: str) -> List[Dict[str, Any]]:
    """Search agency profiles by name, code, or jurisdiction.

    Args:
        query: Search query (agency name, code, or jurisdiction keyword).

    Returns:
        List of matching agency profiles.
    """
    query_lower = query.strip().lower()
    results: List[Tuple[int, AgencyProfile]] = []

    for code, profile in AGENCY_PROFILES.items():
        score = 0
        if query_lower == code.lower():
            score = 100
        elif query_lower in profile.full_name.lower():
            score = 80
        elif query_lower in profile.jurisdiction_scope.lower():
            score = 60
        elif query_lower in profile.enabling_statute.lower():
            score = 50
        else:
            for division in profile.key_divisions:
                if query_lower in division.lower():
                    score = 40
                    break

        if score > 0:
            results.append((score, profile))

    results.sort(key=lambda x: x[0], reverse=True)
    return [p.to_dict() for _, p in results]


# ============================================================================
# CFR CROSS-REFERENCE SEARCH
# ============================================================================

def search_by_cfr(cfr_text: str) -> List[Dict[str, Any]]:
    """Search all doctrines that reference a specific CFR section.

    Args:
        cfr_text: CFR citation text (e.g., "40 CFR 261").

    Returns:
        List of matching doctrine summaries.
    """
    citations = parse_cfr_citation(cfr_text)
    results: List[Dict[str, Any]] = []

    if not citations:
        # Try simple text matching
        cfr_lower = cfr_text.lower().strip()
        for key, doctrine in DOCTRINE_CACHE.items():
            for ref in doctrine.cfr_references:
                if cfr_lower in ref.lower():
                    results.append({
                        "doctrine_key": key,
                        "topic": doctrine.topic,
                        "agency": doctrine.agency,
                        "cfr_references": doctrine.cfr_references,
                        "risk_level": doctrine.risk_level.value,
                        "match_type": "text",
                    })
                    break
        return results

    for cit in citations:
        for key, doctrine in DOCTRINE_CACHE.items():
            for ref in doctrine.cfr_references:
                title_match = str(cit.title) in ref
                part_match = cit.part is not None and str(cit.part) in ref
                if title_match and part_match:
                    already = any(r["doctrine_key"] == key for r in results)
                    if not already:
                        results.append({
                            "doctrine_key": key,
                            "topic": doctrine.topic,
                            "agency": doctrine.agency,
                            "cfr_references": doctrine.cfr_references,
                            "risk_level": doctrine.risk_level.value,
                            "matched_citation": cit.canonical,
                            "match_type": "parsed_citation",
                        })
                elif title_match:
                    already = any(r["doctrine_key"] == key for r in results)
                    if not already:
                        results.append({
                            "doctrine_key": key,
                            "topic": doctrine.topic,
                            "agency": doctrine.agency,
                            "cfr_references": doctrine.cfr_references,
                            "risk_level": doctrine.risk_level.value,
                            "matched_citation": cit.canonical,
                            "match_type": "title_match",
                        })

    return results


# ============================================================================
# RISK SCORING
# ============================================================================

def compute_risk_score(severity: int, likelihood: int, detectability: int) -> Dict[str, Any]:
    """Compute composite risk score using S x L x D methodology.

    Args:
        severity: Severity score (1-10).
        likelihood: Likelihood score (1-10).
        detectability: Detectability score (1-10).

    Returns:
        Dict with composite score and risk classification.
    """
    severity = max(1, min(10, severity))
    likelihood = max(1, min(10, likelihood))
    detectability = max(1, min(10, detectability))

    composite = severity * likelihood * detectability

    if composite >= 750:
        level = "critical"
        color = "red"
        action = "Immediate remediation required"
    elif composite >= 500:
        level = "high"
        color = "orange"
        action = "Priority remediation within 30 days"
    elif composite >= 200:
        level = "medium"
        color = "yellow"
        action = "Remediation within 90 days"
    elif composite >= 50:
        level = "low"
        color = "green"
        action = "Monitor and address in normal course"
    else:
        level = "minimal"
        color = "blue"
        action = "No immediate action required"

    hash_input = f"{severity}:{likelihood}:{detectability}:{composite}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "severity": severity,
        "likelihood": likelihood,
        "detectability": detectability,
        "composite_score": composite,
        "max_possible": 1000,
        "risk_level": level,
        "color": color,
        "recommended_action": action,
        "determinism_hash": determinism_hash,
    }


# ============================================================================
# CHECKLIST GENERATOR
# ============================================================================

def generate_compliance_checklist(naics_code: str,
                                  jurisdiction: str = "federal") -> Dict[str, Any]:
    """Generate a compliance checklist for an industry/jurisdiction.

    Args:
        naics_code: NAICS code for the industry.
        jurisdiction: "federal" or state code.

    Returns:
        Dict with compliance checklist organized by agency.
    """
    from semantic import NAICS_SECTOR_NAMES, get_naics_sector

    applicable_doctrines = get_applicable_doctrines(naics_code)
    sector_name = get_naics_sector(naics_code) or f"NAICS {naics_code}"

    checklist: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    total_items = 0

    for doctrine_key in applicable_doctrines:
        doctrine = DOCTRINE_CACHE.get(doctrine_key)
        if not doctrine:
            continue

        items: List[Dict[str, Any]] = []
        for idx, action in enumerate(doctrine.required_actions, 1):
            items.append({
                "item_number": idx,
                "action": action,
                "status": "pending",
                "risk_level": doctrine.risk_level.value,
                "agency": doctrine.agency,
                "documentation_required": doctrine.documentation_required,
            })
            total_items += 1

        checklist[doctrine.agency].extend(items)

    # Add obligation-based items
    for obl_key, obligation in COMPLIANCE_OBLIGATIONS.items():
        sector = naics_code[:2]
        if sector in obligation.applicable_industries or "All sectors" in obligation.applicable_industries:
            for idx, action in enumerate(obligation.required_actions, 1):
                item = {
                    "item_number": idx,
                    "action": action,
                    "status": "pending",
                    "obligation_id": obligation.obligation_id,
                    "frequency": obligation.frequency,
                    "deadline": obligation.deadline_type,
                    "agency": obligation.agency,
                }
                if not any(existing["action"] == action for existing in checklist[obligation.agency]):
                    checklist[obligation.agency].append(item)
                    total_items += 1

    hash_input = f"{naics_code}:{jurisdiction}:{total_items}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "naics_code": naics_code,
        "industry": sector_name,
        "jurisdiction": jurisdiction,
        "total_items": total_items,
        "agencies_covered": sorted(checklist.keys()),
        "checklist_by_agency": dict(checklist),
        "determinism_hash": determinism_hash,
    }
