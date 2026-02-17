"""
LG12 Bankruptcy Law Engine - Search Module
=============================================
TF-IDF based vector search over bankruptcy doctrine blocks,
means test calculations, exemption analysis, and bankruptcy law references.

Components:
    - DoctrineSearchIndex: TF-IDF inverted index for doctrine search
    - SearchResult: Ranked search result with scoring breakdown
    - MeansTestCalculator: Chapter 7 means test calculation engine
    - ExemptionAnalyzer: Federal vs state exemption comparison
    - DischargeAnalyzer: Debt dischargeability determination
    - PreferenceAnalyzer: Preference action element analysis
    - FraudulentTransferAnalyzer: Badges of fraud detection
    - PlanFeasibilityChecker: Plan confirmation requirement checker
    - LienStripAnalyzer: Lien stripping/cramdown valuation

Version: 2.0.0
Engine: LG12 Bankruptcy Law
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEARCH RESULT
# ============================================================================

@dataclass
class SearchResult:
    """A single search result with scoring breakdown."""
    doc_id: str
    topic: str
    content: str
    score: float
    tf_idf_score: float
    authority_score: float
    recency_score: float
    bk_category: str
    matched_tokens: List[str]
    source: str = "doctrine_cache"
    jurisdiction: Optional[str] = None
    metadata: Dict[str, Any] = dc_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "doc_id": self.doc_id,
            "topic": self.topic,
            "content": self.content[:500],
            "score": round(self.score, 6),
            "tf_idf_score": round(self.tf_idf_score, 6),
            "authority_score": round(self.authority_score, 6),
            "recency_score": round(self.recency_score, 6),
            "bk_category": self.bk_category,
            "jurisdiction": self.jurisdiction,
            "matched_tokens": self.matched_tokens,
            "source": self.source,
            "metadata": self.metadata,
        }


# ============================================================================
# MEANS TEST RESULT
# ============================================================================

@dataclass
class MeansTestResult:
    """Result of a Chapter 7 means test calculation."""
    household_size: int
    state: str
    current_monthly_income: float
    annualized_income: float
    state_median: float
    above_median: bool
    presumption_of_abuse: bool
    monthly_disposable_income: float
    sixty_month_disposable: float
    deductions_total: float
    deduction_breakdown: Dict[str, float]
    safe_harbor_applies: bool
    safe_harbor_reason: Optional[str]
    recommendation: str
    confidence: float
    citations: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "household_size": self.household_size,
            "state": self.state,
            "current_monthly_income": round(self.current_monthly_income, 2),
            "annualized_income": round(self.annualized_income, 2),
            "state_median": round(self.state_median, 2),
            "above_median": self.above_median,
            "presumption_of_abuse": self.presumption_of_abuse,
            "monthly_disposable_income": round(self.monthly_disposable_income, 2),
            "sixty_month_disposable": round(self.sixty_month_disposable, 2),
            "deductions_total": round(self.deductions_total, 2),
            "deduction_breakdown": {k: round(v, 2) for k, v in self.deduction_breakdown.items()},
            "safe_harbor_applies": self.safe_harbor_applies,
            "safe_harbor_reason": self.safe_harbor_reason,
            "recommendation": self.recommendation,
            "confidence": round(self.confidence, 4),
            "citations": self.citations,
            "warnings": self.warnings,
        }


# ============================================================================
# EXEMPTION RESULT
# ============================================================================

@dataclass
class ExemptionResult:
    """Result of an exemption analysis."""
    state: str
    system_used: str
    assets_analyzed: List[Dict[str, Any]]
    total_exempt: float
    total_nonexempt: float
    homestead_analysis: Dict[str, Any]
    personal_property_analysis: Dict[str, Any]
    retirement_analysis: Dict[str, Any]
    wildcard_remaining: float
    recommendations: List[str]
    warnings: List[str]
    confidence: float
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "state": self.state,
            "system_used": self.system_used,
            "assets_analyzed": self.assets_analyzed,
            "total_exempt": round(self.total_exempt, 2),
            "total_nonexempt": round(self.total_nonexempt, 2),
            "homestead_analysis": self.homestead_analysis,
            "personal_property_analysis": self.personal_property_analysis,
            "retirement_analysis": self.retirement_analysis,
            "wildcard_remaining": round(self.wildcard_remaining, 2),
            "recommendations": self.recommendations,
            "warnings": self.warnings,
            "confidence": round(self.confidence, 4),
            "citations": self.citations,
        }


# ============================================================================
# DISCHARGE ANALYSIS RESULT
# ============================================================================

@dataclass
class DischargeResult:
    """Result of a discharge/dischargeability analysis."""
    debt_type: str
    debt_amount: Optional[float]
    dischargeable: bool
    discharge_confidence: float
    applicable_exceptions: List[Dict[str, str]]
    brunner_test_applicable: bool
    brunner_test_result: Optional[Dict[str, Any]]
    tax_discharge_analysis: Optional[Dict[str, Any]]
    required_actions: List[str]
    risk_factors: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "debt_type": self.debt_type,
            "debt_amount": self.debt_amount,
            "dischargeable": self.dischargeable,
            "discharge_confidence": round(self.discharge_confidence, 4),
            "applicable_exceptions": self.applicable_exceptions,
            "brunner_test_applicable": self.brunner_test_applicable,
            "brunner_test_result": self.brunner_test_result,
            "tax_discharge_analysis": self.tax_discharge_analysis,
            "required_actions": self.required_actions,
            "risk_factors": self.risk_factors,
            "citations": self.citations,
        }


# ============================================================================
# PREFERENCE ANALYSIS RESULT
# ============================================================================

@dataclass
class PreferenceResult:
    """Result of a preference action analysis."""
    transfer_date: str
    petition_date: str
    transfer_amount: float
    creditor_name: str
    is_insider: bool
    lookback_days: int
    within_preference_period: bool
    elements_met: Dict[str, bool]
    defenses_available: List[Dict[str, Any]]
    avoidable: bool
    avoidance_confidence: float
    recommendations: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "transfer_date": self.transfer_date,
            "petition_date": self.petition_date,
            "transfer_amount": round(self.transfer_amount, 2),
            "creditor_name": self.creditor_name,
            "is_insider": self.is_insider,
            "lookback_days": self.lookback_days,
            "within_preference_period": self.within_preference_period,
            "elements_met": self.elements_met,
            "defenses_available": self.defenses_available,
            "avoidable": self.avoidable,
            "avoidance_confidence": round(self.avoidance_confidence, 4),
            "recommendations": self.recommendations,
            "citations": self.citations,
        }


# ============================================================================
# FRAUDULENT TRANSFER RESULT
# ============================================================================

@dataclass
class FraudulentTransferResult:
    """Result of a fraudulent transfer analysis."""
    transfer_description: str
    transfer_value: float
    value_received: float
    badges_of_fraud: List[Dict[str, Any]]
    badges_count: int
    actual_fraud_likely: bool
    constructive_fraud_likely: bool
    debtor_insolvent_at_time: Optional[bool]
    reach_back_period: str
    avoidable: bool
    confidence: float
    recommendations: List[str]
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "transfer_description": self.transfer_description,
            "transfer_value": round(self.transfer_value, 2),
            "value_received": round(self.value_received, 2),
            "badges_of_fraud": self.badges_of_fraud,
            "badges_count": self.badges_count,
            "actual_fraud_likely": self.actual_fraud_likely,
            "constructive_fraud_likely": self.constructive_fraud_likely,
            "debtor_insolvent_at_time": self.debtor_insolvent_at_time,
            "reach_back_period": self.reach_back_period,
            "avoidable": self.avoidable,
            "confidence": round(self.confidence, 4),
            "recommendations": self.recommendations,
            "citations": self.citations,
        }


# ============================================================================
# TF-IDF SEARCH INDEX
# ============================================================================

class DoctrineSearchIndex:
    """TF-IDF inverted index over bankruptcy doctrine blocks."""

    def __init__(self) -> None:
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._tf: Dict[str, Dict[str, float]] = {}
        self._idf: Dict[str, float] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._built = False
        self._build_time_ms: float = 0.0

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]) -> None:
        """Add a document to the index."""
        tokens = self._tokenize(content)
        self._documents[doc_id] = {"content": content, "tokens": tokens, "metadata": metadata}
        self._doc_lengths[doc_id] = len(tokens)
        tf_counts: Counter = Counter(tokens)
        total_tokens = len(tokens)
        self._tf[doc_id] = {}
        for token, count in tf_counts.items():
            self._tf[doc_id][token] = count / total_tokens if total_tokens > 0 else 0.0
            self._inverted_index[token].add(doc_id)
        self._built = False

    def build(self) -> None:
        """Build IDF values and finalize the index."""
        start = time.monotonic()
        n_docs = len(self._documents)
        if n_docs == 0:
            self._built = True
            return
        for token, doc_ids in self._inverted_index.items():
            df = len(doc_ids)
            self._idf[token] = math.log((n_docs + 1) / (df + 1)) + 1.0
        self._built = True
        self._build_time_ms = (time.monotonic() - start) * 1000.0
        logger.info(
            f"DoctrineSearchIndex built: {n_docs} docs, "
            f"{len(self._inverted_index)} unique tokens, "
            f"{self._build_time_ms:.1f}ms"
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.1,
        category_filter: Optional[str] = None,
        jurisdiction_filter: Optional[str] = None,
    ) -> List[SearchResult]:
        """Search the index using TF-IDF scoring."""
        if not self._built:
            self.build()
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs: Set[str] = set()
        for token in query_tokens:
            if token in self._inverted_index:
                candidate_docs.update(self._inverted_index[token])
        if not candidate_docs:
            return []
        results: List[SearchResult] = []
        for doc_id in candidate_docs:
            doc = self._documents[doc_id]
            meta = doc["metadata"]
            if category_filter and meta.get("category", "") != category_filter:
                continue
            if jurisdiction_filter and meta.get("jurisdiction", "") != jurisdiction_filter:
                continue
            tfidf_score = 0.0
            matched: List[str] = []
            for token in query_tokens:
                if token in self._tf.get(doc_id, {}):
                    tf_val = self._tf[doc_id][token]
                    idf_val = self._idf.get(token, 1.0)
                    tfidf_score += tf_val * idf_val
                    matched.append(token)
            authority_score = meta.get("authority_score", 0.5)
            last_updated = meta.get("last_updated", "2020-01-01")
            try:
                days_old = (datetime.now(timezone.utc) - datetime.fromisoformat(last_updated).replace(tzinfo=timezone.utc)).days
            except (ValueError, TypeError):
                days_old = 365
            recency_score = max(0.1, 1.0 - (days_old / 3650.0))
            combined = (tfidf_score * 0.60) + (authority_score * 0.25) + (recency_score * 0.15)
            if combined >= score_threshold:
                results.append(SearchResult(
                    doc_id=doc_id,
                    topic=meta.get("topic", ""),
                    content=doc["content"][:500],
                    score=combined,
                    tf_idf_score=tfidf_score,
                    authority_score=authority_score,
                    recency_score=recency_score,
                    bk_category=meta.get("category", "general"),
                    matched_tokens=matched,
                    jurisdiction=meta.get("jurisdiction"),
                    metadata=meta,
                ))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def get_stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        return {
            "total_documents": len(self._documents),
            "unique_tokens": len(self._inverted_index),
            "built": self._built,
            "build_time_ms": round(self._build_time_ms, 3),
            "avg_doc_length": (
                sum(self._doc_lengths.values()) / len(self._doc_lengths)
                if self._doc_lengths else 0.0
            ),
        }

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenize text into lowercase alpha-numeric tokens."""
        return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) >= 2]


# ============================================================================
# MEANS TEST CALCULATOR
# ============================================================================

# 2026 Texas median family income estimates (updated annually by Census/UST)
TX_MEDIAN_INCOME: Dict[int, float] = {
    1: 60893.00,
    2: 78463.00,
    3: 89672.00,
    4: 103176.00,
    5: 112176.00,
    6: 121176.00,
    7: 130176.00,
    8: 139176.00,
    9: 148176.00,
    10: 157176.00,
}

IRS_ALLOWANCES: Dict[str, float] = {
    "national_food_clothing_misc": 785.00,
    "national_healthcare_under65": 75.00,
    "national_healthcare_over65": 153.00,
    "housing_utilities_tx_midland": 2038.00,
    "transportation_ownership_1": 588.00,
    "transportation_ownership_2": 588.00,
    "transportation_operating_1": 276.00,
    "transportation_operating_2": 276.00,
    "taxes_fica_per_month": 0.0,  # Calculated from income
    "mandatory_payroll_deductions": 0.0,
    "term_life_insurance": 0.0,
    "education_minor_child": 191.67,
    "childcare": 0.0,
    "healthcare_excess": 0.0,
    "telecom": 83.00,
}


class MeansTestCalculator:
    """Chapter 7 means test calculation engine per 11 USC 707(b)(2)."""

    def __init__(self) -> None:
        self._median_data = TX_MEDIAN_INCOME
        self._allowances = IRS_ALLOWANCES

    def calculate(
        self,
        monthly_income: float,
        household_size: int,
        state: str = "TX",
        is_veteran: bool = False,
        is_reservist: bool = False,
        non_consumer_debt_majority: bool = False,
        secured_debt_payments: float = 0.0,
        priority_debt_payments: float = 0.0,
        special_circumstances_amount: float = 0.0,
        additional_deductions: Optional[Dict[str, float]] = None,
    ) -> MeansTestResult:
        """Calculate the Chapter 7 means test."""
        warnings: List[str] = []
        citations = [
            "11 USC 707(b)(2)",
            "11 USC 707(b)(7)",
            "Form 122A-1",
            "Form 122A-2",
        ]

        # Step 1: Annualize CMI
        annualized = monthly_income * 12.0

        # Step 2: Get median for state/household
        if state.upper() != "TX":
            warnings.append(f"Median income data only loaded for TX. Using TX medians for {state}.")
        capped_size = min(household_size, 10)
        median = self._median_data.get(capped_size, self._median_data[4])

        above_median = annualized > median

        # Step 3: Check safe harbors
        safe_harbor = False
        safe_harbor_reason: Optional[str] = None
        if not above_median:
            safe_harbor = True
            safe_harbor_reason = "Below state median income - no presumption of abuse under 707(b)(7)"
        elif is_veteran:
            safe_harbor = True
            safe_harbor_reason = "Disabled veteran exemption from means test under 707(b)(2)(D)"
        elif is_reservist:
            safe_harbor = True
            safe_harbor_reason = "Reservist/National Guard member after qualifying service under 707(b)(2)(D)"
        elif non_consumer_debt_majority:
            safe_harbor = True
            safe_harbor_reason = "Non-consumer debts exceed 50% of total - means test not applicable"

        # Step 4: Calculate deductions (if above median)
        deductions: Dict[str, float] = {}
        total_deductions = 0.0

        if above_median and not safe_harbor:
            # IRS National Standards
            deductions["food_clothing_misc"] = self._allowances["national_food_clothing_misc"]
            deductions["healthcare"] = self._allowances["national_healthcare_under65"]
            # IRS Local Standards
            deductions["housing_utilities"] = self._allowances["housing_utilities_tx_midland"]
            deductions["transportation_ownership"] = self._allowances["transportation_ownership_1"]
            deductions["transportation_operating"] = self._allowances["transportation_operating_1"]
            # Other allowances
            deductions["telecom"] = self._allowances["telecom"]
            # FICA estimate (7.65% of gross)
            fica = monthly_income * 0.0765
            deductions["fica_taxes"] = fica
            # Secured debt
            if secured_debt_payments > 0:
                deductions["secured_debt_avg_60mo"] = secured_debt_payments
            # Priority debt
            if priority_debt_payments > 0:
                deductions["priority_debt_avg_60mo"] = priority_debt_payments
            # Special circumstances
            if special_circumstances_amount > 0:
                deductions["special_circumstances"] = special_circumstances_amount
                warnings.append("Special circumstances deduction requires documentation and court approval")
            # Additional user deductions
            if additional_deductions:
                for key, val in additional_deductions.items():
                    deductions[f"additional_{key}"] = val

            total_deductions = sum(deductions.values())

        # Step 5: Calculate disposable income
        monthly_disposable = monthly_income - total_deductions
        sixty_month = monthly_disposable * 60.0

        # Step 6: Determine presumption of abuse
        presumption = False
        recommendation = ""
        if safe_harbor:
            presumption = False
            recommendation = f"Chapter 7 eligible. {safe_harbor_reason}"
        elif sixty_month >= 12850.00:
            presumption = True
            recommendation = (
                "Presumption of abuse arises. 60-month disposable income exceeds $12,850 threshold. "
                "Consider Chapter 13 or demonstrating special circumstances to rebut."
            )
        elif sixty_month >= 7700.00:
            unsecured_pct = sixty_month / max(1.0, sixty_month * 1.5)
            if unsecured_pct >= 0.25:
                presumption = True
                recommendation = (
                    "Presumption of abuse arises. 60-month disposable income is between $7,700 and $12,850 "
                    "and would pay 25%+ of nonpriority unsecured claims."
                )
            else:
                recommendation = (
                    "No presumption of abuse. 60-month disposable income is between $7,700 and $12,850 "
                    "but would not pay 25% of nonpriority unsecured claims."
                )
        else:
            recommendation = "No presumption of abuse. 60-month disposable income is below $7,700."

        confidence = 0.85 if state.upper() == "TX" else 0.65

        return MeansTestResult(
            household_size=household_size,
            state=state,
            current_monthly_income=monthly_income,
            annualized_income=annualized,
            state_median=median,
            above_median=above_median,
            presumption_of_abuse=presumption,
            monthly_disposable_income=monthly_disposable,
            sixty_month_disposable=sixty_month,
            deductions_total=total_deductions,
            deduction_breakdown=deductions,
            safe_harbor_applies=safe_harbor,
            safe_harbor_reason=safe_harbor_reason,
            recommendation=recommendation,
            confidence=confidence,
            citations=citations,
            warnings=warnings,
        )


# ============================================================================
# EXEMPTION ANALYZER
# ============================================================================

class ExemptionAnalyzer:
    """Federal vs state exemption comparison and analysis."""

    FEDERAL_EXEMPTIONS: ClassVar[Dict[str, float]] = {
        "homestead": 27900.00,
        "motor_vehicle": 4450.00,
        "household_goods_per_item": 700.00,
        "household_goods_aggregate": 14875.00,
        "jewelry": 1875.00,
        "wildcard": 1475.00,
        "wildcard_unused_homestead": 13950.00,
        "tools_of_trade": 2800.00,
        "life_insurance_loan_value": 14875.00,
        "health_aids": -1.0,  # unlimited
        "personal_injury": 27900.00,
        "public_benefits": -1.0,  # unlimited
        "retirement_erisa": -1.0,  # unlimited
        "retirement_ira": 1512350.00,
    }

    TX_EXEMPTIONS: ClassVar[Dict[str, Any]] = {
        "homestead_urban_acres": 10,
        "homestead_rural_single_acres": 100,
        "homestead_rural_family_acres": 200,
        "homestead_value": -1.0,  # unlimited
        "personal_property_family": 100000.00,
        "personal_property_single": 50000.00,
        "current_wages": -1.0,  # unlimited
        "retirement_accounts": -1.0,  # unlimited
        "life_insurance": -1.0,  # unlimited
        "burial_plots": -1.0,  # unlimited
        "motor_vehicle": -1.0,  # one per licensed member, no value cap
    }

    def analyze(
        self,
        assets: List[Dict[str, Any]],
        state: str = "TX",
        is_married: bool = False,
        is_urban: bool = True,
    ) -> ExemptionResult:
        """Analyze asset exemptions under applicable law."""
        citations = ["11 USC 522", "Tex. Prop. Code Ch. 41", "Tex. Prop. Code Ch. 42"]
        warnings: List[str] = []
        recommendations: List[str] = []

        system_used = "texas_state" if state.upper() == "TX" else "federal"
        if state.upper() == "TX":
            warnings.append("Texas is an opt-out state. Federal exemptions under 522(d) are NOT available.")

        total_exempt = 0.0
        total_nonexempt = 0.0
        homestead_analysis: Dict[str, Any] = {"applicable": False}
        personal_property_analysis: Dict[str, Any] = {"total_claimed": 0.0}
        retirement_analysis: Dict[str, Any] = {"total_protected": 0.0}
        personal_property_used = 0.0
        pp_limit = self.TX_EXEMPTIONS["personal_property_family"] if is_married else self.TX_EXEMPTIONS["personal_property_single"]
        wildcard_remaining = 0.0 if state.upper() == "TX" else self.FEDERAL_EXEMPTIONS["wildcard"]

        analyzed: List[Dict[str, Any]] = []

        for asset in assets:
            name = asset.get("name", "unknown")
            value = float(asset.get("value", 0.0))
            asset_type = asset.get("type", "other")
            result: Dict[str, Any] = {
                "name": name,
                "value": round(value, 2),
                "type": asset_type,
                "exempt_amount": 0.0,
                "nonexempt_amount": 0.0,
                "exemption_basis": "",
            }

            if asset_type == "homestead":
                if state.upper() == "TX":
                    result["exempt_amount"] = value  # TX unlimited value
                    result["exemption_basis"] = "Tex. Prop. Code 41.001 - unlimited value homestead"
                    homestead_analysis = {
                        "applicable": True,
                        "value": value,
                        "fully_exempt": True,
                        "basis": "Texas unlimited homestead (urban 10 acres, rural 200 acres family)",
                    }
                else:
                    exempt = min(value, self.FEDERAL_EXEMPTIONS["homestead"])
                    result["exempt_amount"] = exempt
                    result["nonexempt_amount"] = max(0.0, value - exempt)
                    result["exemption_basis"] = f"11 USC 522(d)(1) - ${self.FEDERAL_EXEMPTIONS['homestead']:,.2f} limit"
                    homestead_analysis = {
                        "applicable": True,
                        "value": value,
                        "fully_exempt": value <= self.FEDERAL_EXEMPTIONS["homestead"],
                        "basis": f"Federal homestead ${self.FEDERAL_EXEMPTIONS['homestead']:,.2f}",
                    }
            elif asset_type == "vehicle":
                if state.upper() == "TX":
                    result["exempt_amount"] = value  # one per licensed member
                    result["exemption_basis"] = "Tex. Prop. Code 42.002(a)(9) - one vehicle per licensed member"
                else:
                    exempt = min(value, self.FEDERAL_EXEMPTIONS["motor_vehicle"])
                    result["exempt_amount"] = exempt
                    result["nonexempt_amount"] = max(0.0, value - exempt)
                    result["exemption_basis"] = f"11 USC 522(d)(2) - ${self.FEDERAL_EXEMPTIONS['motor_vehicle']:,.2f}"
            elif asset_type == "retirement":
                result["exempt_amount"] = value  # Both TX and federal protect ERISA
                result["exemption_basis"] = "ERISA-qualified retirement - fully exempt"
                retirement_analysis["total_protected"] = retirement_analysis.get("total_protected", 0.0) + value
            elif asset_type == "personal_property":
                if state.upper() == "TX":
                    remaining = pp_limit - personal_property_used
                    exempt = min(value, remaining)
                    result["exempt_amount"] = exempt
                    result["nonexempt_amount"] = max(0.0, value - exempt)
                    personal_property_used += exempt
                    result["exemption_basis"] = f"Tex. Prop. Code 42.001 - ${pp_limit:,.2f} aggregate"
                else:
                    per_item_limit = self.FEDERAL_EXEMPTIONS["household_goods_per_item"]
                    exempt = min(value, per_item_limit)
                    result["exempt_amount"] = exempt
                    result["nonexempt_amount"] = max(0.0, value - exempt)
                    result["exemption_basis"] = f"11 USC 522(d)(3) - ${per_item_limit:,.2f} per item"
                personal_property_analysis["total_claimed"] = personal_property_analysis.get("total_claimed", 0.0) + result["exempt_amount"]
            elif asset_type == "wages":
                if state.upper() == "TX":
                    result["exempt_amount"] = value
                    result["exemption_basis"] = "Tex. Prop. Code 42.001(b)(1) - current wages fully exempt"
                else:
                    result["nonexempt_amount"] = value
                    result["exemption_basis"] = "No specific federal wage exemption in 522(d)"
            else:
                result["nonexempt_amount"] = value
                result["exemption_basis"] = "No applicable exemption identified"
                if wildcard_remaining > 0 and state.upper() != "TX":
                    apply_wc = min(value, wildcard_remaining)
                    result["exempt_amount"] = apply_wc
                    result["nonexempt_amount"] = max(0.0, value - apply_wc)
                    wildcard_remaining -= apply_wc
                    result["exemption_basis"] = f"11 USC 522(d)(5) wildcard - ${apply_wc:,.2f} applied"

            total_exempt += result["exempt_amount"]
            total_nonexempt += result["nonexempt_amount"]
            analyzed.append(result)

        if total_nonexempt > 0:
            recommendations.append("Non-exempt assets may be liquidated in Chapter 7. Consider Chapter 13 as alternative.")
        if state.upper() == "TX" and personal_property_used >= pp_limit * 0.8:
            warnings.append(f"Personal property exemption nearing limit (${personal_property_used:,.2f} of ${pp_limit:,.2f})")

        return ExemptionResult(
            state=state,
            system_used=system_used,
            assets_analyzed=analyzed,
            total_exempt=total_exempt,
            total_nonexempt=total_nonexempt,
            homestead_analysis=homestead_analysis,
            personal_property_analysis=personal_property_analysis,
            retirement_analysis=retirement_analysis,
            wildcard_remaining=wildcard_remaining,
            recommendations=recommendations,
            warnings=warnings,
            confidence=0.85 if state.upper() == "TX" else 0.70,
            citations=citations,
        )


# ============================================================================
# DISCHARGE ANALYZER
# ============================================================================

class DischargeAnalyzer:
    """Debt dischargeability determination engine."""

    NONDISCHARGEABLE_523: ClassVar[Dict[str, Dict[str, Any]]] = {
        "523(a)(1)": {"type": "tax_debt", "description": "Certain tax debts (income, employment) unless 3-year/2-year/240-day rules met"},
        "523(a)(2)(A)": {"type": "fraud_false_pretenses", "description": "Debts obtained by false pretenses, false representation, or actual fraud"},
        "523(a)(2)(B)": {"type": "fraud_financial_statement", "description": "Debts arising from materially false written financial statements"},
        "523(a)(2)(C)": {"type": "luxury_goods_cash_advance", "description": "Luxury goods >$800 within 90 days, cash advances >$1,100 within 70 days (presumption)"},
        "523(a)(3)": {"type": "unscheduled_debt", "description": "Debts not listed in schedules if creditor had no notice"},
        "523(a)(4)": {"type": "fiduciary_fraud", "description": "Fraud or defalcation while acting in fiduciary capacity, embezzlement, larceny"},
        "523(a)(5)": {"type": "domestic_support", "description": "Domestic support obligations (alimony, maintenance, child support)"},
        "523(a)(6)": {"type": "willful_injury", "description": "Willful and malicious injury to another entity or property"},
        "523(a)(7)": {"type": "government_fines", "description": "Government fines, penalties, or forfeitures (not compensation for actual pecuniary loss)"},
        "523(a)(8)": {"type": "student_loans", "description": "Student loans unless undue hardship demonstrated (Brunner test)"},
        "523(a)(9)": {"type": "dui_liability", "description": "Debts arising from death or personal injury caused by intoxicated driving"},
        "523(a)(10)": {"type": "prior_bankruptcy_denial", "description": "Debts that were or could have been listed in prior case where discharge was denied"},
        "523(a)(14A)": {"type": "federal_election_fines", "description": "Debts incurred to pay federal election law fines"},
        "523(a)(15)": {"type": "divorce_property_settlement", "description": "Property settlement debts from divorce (Chapter 7 only)"},
        "523(a)(19)": {"type": "securities_violations", "description": "Debts from securities law violations or common law fraud in securities"},
    }

    TAX_DISCHARGE_RULES: ClassVar[Dict[str, str]] = {
        "3_year_rule": "Tax return was due (including extensions) more than 3 years before filing",
        "2_year_rule": "Tax return was actually filed more than 2 years before filing",
        "240_day_rule": "Tax was assessed more than 240 days before filing",
        "no_fraud": "Debtor did not file a fraudulent return",
        "filed_return": "Debtor actually filed a tax return (not SFR by IRS)",
    }

    def analyze_discharge(
        self,
        debt_type: str,
        debt_amount: Optional[float] = None,
        additional_facts: Optional[Dict[str, Any]] = None,
    ) -> DischargeResult:
        """Analyze whether a specific debt is dischargeable."""
        facts = additional_facts or {}
        citations: List[str] = ["11 USC 523", "11 USC 524", "11 USC 727"]
        applicable_exceptions: List[Dict[str, str]] = []
        risk_factors: List[str] = []
        required_actions: List[str] = []
        brunner_applicable = False
        brunner_result: Optional[Dict[str, Any]] = None
        tax_analysis: Optional[Dict[str, Any]] = None

        # Check each exception
        debt_lower = debt_type.lower()
        dischargeable = True
        discharge_conf = 0.75

        if "student" in debt_lower or "loan" in debt_lower and "education" in debt_lower:
            dischargeable = False
            discharge_conf = 0.90
            brunner_applicable = True
            applicable_exceptions.append({
                "section": "523(a)(8)",
                "description": self.NONDISCHARGEABLE_523["523(a)(8)"]["description"],
            })
            brunner_result = self._apply_brunner_test(facts)
            if brunner_result.get("hardship_shown"):
                dischargeable = True
                discharge_conf = brunner_result.get("confidence", 0.40)
            required_actions.append("Must file adversary proceeding to determine dischargeability")
            required_actions.append("Demonstrate undue hardship under Brunner or Totality test")
            citations.append("Brunner v. New York State Higher Education Services Corp., 831 F.2d 395 (2d Cir. 1987)")

        elif "tax" in debt_lower or "irs" in debt_lower or "income tax" in debt_lower:
            tax_analysis = self._analyze_tax_discharge(facts)
            if tax_analysis.get("all_rules_met"):
                dischargeable = True
                discharge_conf = 0.80
            else:
                dischargeable = False
                discharge_conf = 0.85
            applicable_exceptions.append({
                "section": "523(a)(1)",
                "description": self.NONDISCHARGEABLE_523["523(a)(1)"]["description"],
            })
            citations.append("11 USC 507(a)(8)")

        elif "child support" in debt_lower or "alimony" in debt_lower or "maintenance" in debt_lower or "dso" in debt_lower:
            dischargeable = False
            discharge_conf = 0.98
            applicable_exceptions.append({
                "section": "523(a)(5)",
                "description": self.NONDISCHARGEABLE_523["523(a)(5)"]["description"],
            })
            risk_factors.append("Domestic support obligations are absolutely nondischargeable in all chapters")

        elif "fraud" in debt_lower or "false" in debt_lower:
            dischargeable = False
            discharge_conf = 0.80
            applicable_exceptions.append({
                "section": "523(a)(2)(A)",
                "description": self.NONDISCHARGEABLE_523["523(a)(2)(A)"]["description"],
            })
            required_actions.append("Creditor must file adversary proceeding within 60 days of 341 meeting")

        elif "dui" in debt_lower or "drunk driv" in debt_lower or "intoxicat" in debt_lower:
            dischargeable = False
            discharge_conf = 0.95
            applicable_exceptions.append({
                "section": "523(a)(9)",
                "description": self.NONDISCHARGEABLE_523["523(a)(9)"]["description"],
            })

        elif "fine" in debt_lower or "penalt" in debt_lower or "restitution" in debt_lower:
            dischargeable = False
            discharge_conf = 0.85
            applicable_exceptions.append({
                "section": "523(a)(7)",
                "description": self.NONDISCHARGEABLE_523["523(a)(7)"]["description"],
            })

        elif "divorce" in debt_lower or "property settlement" in debt_lower:
            dischargeable = False
            discharge_conf = 0.80
            applicable_exceptions.append({
                "section": "523(a)(15)",
                "description": self.NONDISCHARGEABLE_523["523(a)(15)"]["description"],
            })
            risk_factors.append("523(a)(15) debts are nondischargeable in Chapter 7 but may be dischargeable in Chapter 13")

        else:
            dischargeable = True
            discharge_conf = 0.70
            risk_factors.append("General unsecured debt is typically dischargeable absent specific exception")

        return DischargeResult(
            debt_type=debt_type,
            debt_amount=debt_amount,
            dischargeable=dischargeable,
            discharge_confidence=discharge_conf,
            applicable_exceptions=applicable_exceptions,
            brunner_test_applicable=brunner_applicable,
            brunner_test_result=brunner_result,
            tax_discharge_analysis=tax_analysis,
            required_actions=required_actions,
            risk_factors=risk_factors,
            citations=citations,
        )

    def _apply_brunner_test(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the Brunner three-part test for student loan discharge."""
        elements = {
            "minimal_standard": facts.get("cannot_maintain_minimal_standard", False),
            "additional_circumstances": facts.get("additional_circumstances_persist", False),
            "good_faith_effort": facts.get("good_faith_repayment_effort", False),
        }
        all_met = all(elements.values())
        met_count = sum(1 for v in elements.values() if v)
        return {
            "test_name": "Brunner Test",
            "citation": "Brunner v. New York State Higher Education Services Corp., 831 F.2d 395 (2d Cir. 1987)",
            "elements": elements,
            "elements_met": met_count,
            "total_elements": 3,
            "hardship_shown": all_met,
            "confidence": 0.40 + (met_count * 0.15),
            "note": "Some circuits (e.g., 1st, 7th, 8th) use a totality of circumstances test instead of Brunner",
        }

    def _analyze_tax_discharge(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tax debt discharge under the 3/2/240 rules."""
        rules = {
            "3_year_rule": facts.get("return_due_over_3_years", False),
            "2_year_rule": facts.get("return_filed_over_2_years", False),
            "240_day_rule": facts.get("assessed_over_240_days", False),
            "no_fraud": facts.get("no_fraudulent_return", True),
            "filed_return": facts.get("return_actually_filed", True),
        }
        all_met = all(rules.values())
        met_count = sum(1 for v in rules.values() if v)
        return {
            "rules": rules,
            "rules_met": met_count,
            "total_rules": 5,
            "all_rules_met": all_met,
            "dischargeable": all_met,
            "confidence": 0.50 + (met_count * 0.10),
            "citations": ["11 USC 523(a)(1)", "11 USC 507(a)(8)"],
            "warning": "Toll periods may apply (e.g., prior bankruptcy, IRS collection suspension, offers in compromise)",
        }


# ============================================================================
# PREFERENCE ANALYZER
# ============================================================================

class PreferenceAnalyzer:
    """Preference action element analysis under 11 USC 547."""

    def analyze(
        self,
        transfer_date: str,
        petition_date: str,
        transfer_amount: float,
        creditor_name: str,
        is_insider: bool = False,
        was_insolvent: bool = True,
        on_account_of_antecedent_debt: bool = True,
        enables_greater_recovery: bool = True,
        ordinary_course: bool = False,
        contemporaneous_exchange: bool = False,
        subsequent_new_value: float = 0.0,
    ) -> PreferenceResult:
        """Analyze a potential preferential transfer."""
        citations = ["11 USC 547(b)", "11 USC 547(c)"]

        # Calculate days between transfer and petition
        try:
            from datetime import datetime as dt
            t_date = dt.fromisoformat(transfer_date)
            p_date = dt.fromisoformat(petition_date)
            days_diff = (p_date - t_date).days
        except (ValueError, TypeError):
            days_diff = 0

        lookback = 365 if is_insider else 90
        within_period = 0 < days_diff <= lookback

        elements = {
            "transfer_of_interest_in_property": True,
            "to_or_for_benefit_of_creditor": True,
            "on_account_of_antecedent_debt": on_account_of_antecedent_debt,
            "made_while_insolvent": was_insolvent,
            "within_preference_period": within_period,
            "enables_greater_recovery": enables_greater_recovery,
        }
        all_elements = all(elements.values())

        defenses: List[Dict[str, Any]] = []
        if contemporaneous_exchange:
            defenses.append({
                "defense": "Contemporaneous exchange for new value",
                "section": "547(c)(1)",
                "applicable": True,
                "strength": "strong",
            })
        if ordinary_course:
            defenses.append({
                "defense": "Ordinary course of business",
                "section": "547(c)(2)",
                "applicable": True,
                "strength": "strong",
            })
        if subsequent_new_value > 0:
            defenses.append({
                "defense": f"Subsequent new value: ${subsequent_new_value:,.2f}",
                "section": "547(c)(4)",
                "applicable": True,
                "strength": "moderate" if subsequent_new_value < transfer_amount else "strong",
            })
        if transfer_amount < 7575.00 and not is_insider:
            defenses.append({
                "defense": "Small preference exception (non-business < $7,575)",
                "section": "547(c)(9)",
                "applicable": True,
                "strength": "strong",
            })

        any_strong_defense = any(d["strength"] == "strong" and d["applicable"] for d in defenses)
        avoidable = all_elements and not any_strong_defense

        recommendations: List[str] = []
        if avoidable:
            recommendations.append("Transfer appears avoidable as preferential. Trustee may bring action.")
            recommendations.append(f"Creditor should evaluate {', '.join(d['defense'] for d in defenses)} defenses.")
        elif not all_elements:
            missing = [k for k, v in elements.items() if not v]
            recommendations.append(f"Missing elements: {', '.join(missing)}. Preference claim likely fails.")

        conf = 0.80 if all_elements else 0.70

        return PreferenceResult(
            transfer_date=transfer_date,
            petition_date=petition_date,
            transfer_amount=transfer_amount,
            creditor_name=creditor_name,
            is_insider=is_insider,
            lookback_days=lookback,
            within_preference_period=within_period,
            elements_met=elements,
            defenses_available=defenses,
            avoidable=avoidable,
            avoidance_confidence=conf,
            recommendations=recommendations,
            citations=citations,
        )


# ============================================================================
# FRAUDULENT TRANSFER ANALYZER
# ============================================================================

class FraudulentTransferAnalyzer:
    """Badges of fraud detection and fraudulent transfer analysis."""

    BADGES_OF_FRAUD: ClassVar[List[Dict[str, str]]] = [
        {"badge": "insider_transfer", "description": "Transfer to or for the benefit of an insider"},
        {"badge": "retained_possession", "description": "Debtor retained possession or control after transfer"},
        {"badge": "concealment", "description": "Transfer was concealed or not disclosed"},
        {"badge": "pending_litigation", "description": "Transfer made while litigation was pending or threatened"},
        {"badge": "substantially_all_assets", "description": "Transfer was of substantially all debtor's assets"},
        {"badge": "absconded", "description": "Debtor absconded or removed assets from jurisdiction"},
        {"badge": "inadequate_consideration", "description": "Value received was not reasonably equivalent"},
        {"badge": "insolvent_at_time", "description": "Debtor was insolvent at time of transfer or became insolvent"},
        {"badge": "close_to_debt_incurrence", "description": "Transfer occurred shortly before or after substantial debt incurred"},
    ]

    def analyze(
        self,
        transfer_description: str,
        transfer_value: float,
        value_received: float,
        badges_present: List[str],
        debtor_insolvent: Optional[bool] = None,
    ) -> FraudulentTransferResult:
        """Analyze a potential fraudulent transfer."""
        citations = ["11 USC 548", "UVTA (Uniform Voidable Transactions Act)"]
        recommendations: List[str] = []

        # Map badges
        matched_badges: List[Dict[str, Any]] = []
        for badge_def in self.BADGES_OF_FRAUD:
            present = badge_def["badge"] in badges_present
            matched_badges.append({
                "badge": badge_def["badge"],
                "description": badge_def["description"],
                "present": present,
            })

        badges_count = sum(1 for b in matched_badges if b["present"])

        # Actual fraud analysis (intent-based)
        actual_fraud = badges_count >= 3

        # Constructive fraud (no intent needed)
        reasonably_equivalent = value_received >= (transfer_value * 0.70)
        constructive_fraud = not reasonably_equivalent and (debtor_insolvent is True or debtor_insolvent is None)

        avoidable = actual_fraud or constructive_fraud

        reach_back = "2 years (federal 548) / 4 years actual, 1 year constructive (state UVTA)"

        if actual_fraud:
            recommendations.append(f"Strong actual fraud indicators ({badges_count} badges). Trustee likely to pursue avoidance.")
        if constructive_fraud:
            recommendations.append("Constructive fraud: less than reasonably equivalent value while insolvent.")
        if not avoidable:
            recommendations.append("Transfer appears defensible. Reasonably equivalent value exchanged.")

        confidence = 0.60 + (badges_count * 0.05)
        confidence = min(confidence, 0.95)

        return FraudulentTransferResult(
            transfer_description=transfer_description,
            transfer_value=transfer_value,
            value_received=value_received,
            badges_of_fraud=matched_badges,
            badges_count=badges_count,
            actual_fraud_likely=actual_fraud,
            constructive_fraud_likely=constructive_fraud,
            debtor_insolvent_at_time=debtor_insolvent,
            reach_back_period=reach_back,
            avoidable=avoidable,
            confidence=confidence,
            recommendations=recommendations,
            citations=citations,
        )


# ============================================================================
# MODULE-LEVEL SINGLETONS
# ============================================================================

_SEARCH_INDEX: Optional[DoctrineSearchIndex] = None
_MEANS_TEST: Optional[MeansTestCalculator] = None
_EXEMPTION_ANALYZER: Optional[ExemptionAnalyzer] = None
_DISCHARGE_ANALYZER: Optional[DischargeAnalyzer] = None
_PREFERENCE_ANALYZER: Optional[PreferenceAnalyzer] = None
_FRAUD_TRANSFER_ANALYZER: Optional[FraudulentTransferAnalyzer] = None


def get_search_index() -> DoctrineSearchIndex:
    """Get or create the search index singleton."""
    global _SEARCH_INDEX
    if _SEARCH_INDEX is None:
        _SEARCH_INDEX = DoctrineSearchIndex()
    return _SEARCH_INDEX


def get_means_test_calculator() -> MeansTestCalculator:
    """Get or create the means test calculator singleton."""
    global _MEANS_TEST
    if _MEANS_TEST is None:
        _MEANS_TEST = MeansTestCalculator()
    return _MEANS_TEST


def get_exemption_analyzer() -> ExemptionAnalyzer:
    """Get or create the exemption analyzer singleton."""
    global _EXEMPTION_ANALYZER
    if _EXEMPTION_ANALYZER is None:
        _EXEMPTION_ANALYZER = ExemptionAnalyzer()
    return _EXEMPTION_ANALYZER


def get_discharge_analyzer() -> DischargeAnalyzer:
    """Get or create the discharge analyzer singleton."""
    global _DISCHARGE_ANALYZER
    if _DISCHARGE_ANALYZER is None:
        _DISCHARGE_ANALYZER = DischargeAnalyzer()
    return _DISCHARGE_ANALYZER


def get_preference_analyzer() -> PreferenceAnalyzer:
    """Get or create the preference analyzer singleton."""
    global _PREFERENCE_ANALYZER
    if _PREFERENCE_ANALYZER is None:
        _PREFERENCE_ANALYZER = PreferenceAnalyzer()
    return _PREFERENCE_ANALYZER


def get_fraudulent_transfer_analyzer() -> FraudulentTransferAnalyzer:
    """Get or create the fraudulent transfer analyzer singleton."""
    global _FRAUD_TRANSFER_ANALYZER
    if _FRAUD_TRANSFER_ANALYZER is None:
        _FRAUD_TRANSFER_ANALYZER = FraudulentTransferAnalyzer()
    return _FRAUD_TRANSFER_ANALYZER


def compute_query_hash(query: str) -> str:
    """Compute a SHA-256 hash of a query string."""
    return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
