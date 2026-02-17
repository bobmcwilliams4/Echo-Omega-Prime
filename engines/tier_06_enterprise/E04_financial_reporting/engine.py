"""
E04 Financial Reporting Engine
TIE-20 Compliant | Port 8904
Domain: Accounting, Financial Statements, Compliance Reporting
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import statistics
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ─── Constants ───────────────────────────────────────────────────────────────
ENGINE_ID = "E04"
ENGINE_NAME = "Financial Reporting Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8904
ENGINE_DOMAIN = "financial_reporting"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG = LOG_DIR / "e04_audit.jsonl"

logger.add(LOG_DIR / "e04_engine.log", rotation="50 MB", retention="30 days", level="DEBUG")
logger.add(AUDIT_LOG, rotation="20 MB", retention="90 days", level="INFO", serialize=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS (TIE Component 17 - typed I/O)
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


class IssueCategory(str, Enum):
    REVENUE_RECOGNITION = "REVENUE_RECOGNITION"
    LEASE_ACCOUNTING = "LEASE_ACCOUNTING"
    CREDIT_LOSSES = "CREDIT_LOSSES"
    CONSOLIDATION = "CONSOLIDATION"
    TAX_PROVISION = "TAX_PROVISION"
    FAIR_VALUE = "FAIR_VALUE"
    IMPAIRMENT = "IMPAIRMENT"
    FINANCIAL_INSTRUMENTS = "FINANCIAL_INSTRUMENTS"
    STOCK_COMPENSATION = "STOCK_COMPENSATION"
    PENSIONS = "PENSIONS"
    SEGMENT_REPORTING = "SEGMENT_REPORTING"
    INTERNAL_CONTROLS = "INTERNAL_CONTROLS"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    categories: List[IssueCategory] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    entity_ids: List[str] = Field(default_factory=list)
    fiscal_year: Optional[int] = None
    period: Optional[str] = None


class AuthoritySource(BaseModel):
    codification: str
    title: str
    weight: float = 1.0
    binding: bool = True


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[AuthoritySource]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_stratification: ConfidenceLevel
    controlling_precedent: str


class FinancialStatementLine(BaseModel):
    account: str
    current_period: float = 0.0
    prior_period: float = 0.0
    budget: float = 0.0
    variance: float = 0.0
    variance_pct: Optional[float] = None


class RatioResult(BaseModel):
    name: str
    value: float
    benchmark: Optional[float] = None
    interpretation: str
    formula: str


class VarianceItem(BaseModel):
    line_item: str
    actual: float
    budget: float
    variance: float
    variance_pct: float
    favorable: bool
    explanation: str


class MaterialityResult(BaseModel):
    overall_materiality: float
    performance_materiality: float
    trivial_threshold: float
    basis: str
    benchmark_pct: float


class DeferredTaxItem(BaseModel):
    description: str
    book_amount: float
    tax_amount: float
    temporary_difference: float
    deferred_tax_asset: float = 0.0
    deferred_tax_liability: float = 0.0
    reversal_period: Optional[str] = None


class ConsolidationEntry(BaseModel):
    entity_id: str
    entity_name: str
    ownership_pct: float
    method: str
    functional_currency: str
    translation_rate: float = 1.0


class TelemetryEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    engine_id: str = ENGINE_ID
    event_type: str = ""
    query_hash: str = ""
    latency_ms: float = 0.0
    cache_hit: bool = False
    doctrine_topics: List[str] = Field(default_factory=list)
    error: Optional[str] = None


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    total_queries: int = 0
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    doctrine_count: int = 0
    last_query_at: Optional[str] = None


class QueryResponse(BaseModel):
    query_id: str
    engine_id: str = ENGINE_ID
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: float
    confidence_stratification: ConfidenceLevel
    authorities_cited: List[str]
    doctrine_topics_triggered: List[str]
    determinism_hash: str
    latency_ms: float
    disclosure_caveats: List[str] = Field(default_factory=list)
    financial_data: Optional[Dict[str, Any]] = None


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 3 — DOCTRINE CACHE (50+ blocks)
# ═══════════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="ASC 606 Revenue Recognition - Five-Step Model",
        keywords=["revenue", "asc 606", "performance obligation", "contract", "transaction price"],
        conclusion_template=(
            "Revenue under ASC 606 is recognized when control of promised goods or services "
            "transfers to the customer in an amount reflecting expected consideration. "
            "The five-step model requires: (1) identify the contract, (2) identify performance "
            "obligations, (3) determine transaction price, (4) allocate transaction price, "
            "(5) recognize revenue when obligations are satisfied."
        ),
        reasoning_framework=(
            "Step 1 - Contract Identification: A contract exists when parties approve and commit, "
            "rights and payment terms are identifiable, the contract has commercial substance, "
            "and collection is probable. Step 2 - Performance Obligations: Distinct goods/services "
            "or series of distinct goods/services transferred over time in the same pattern. "
            "Step 3 - Transaction Price: Fixed or variable consideration, constraining variable "
            "consideration to amounts not subject to significant reversal. Include time value of "
            "money if significant financing component exists. Step 4 - Allocation: Use standalone "
            "selling prices; estimate using adjusted market assessment, expected cost plus margin, "
            "or residual approach. Step 5 - Recognition: Over time if customer simultaneously "
            "receives and consumes benefits, entity creates asset with no alternative use and has "
            "enforceable right to payment, or customer controls asset as it is created."
        ),
        key_factors=[
            "Contract approval and commitment by all parties",
            "Identification of distinct performance obligations",
            "Variable consideration constraint (most likely amount or expected value)",
            "Standalone selling price allocation methodology",
            "Point-in-time vs over-time recognition criteria",
            "Principal vs agent determination for gross vs net reporting",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 606-10-25", title="Revenue Recognition - Overall Recognition", weight=1.0),
            AuthoritySource(codification="ASC 606-10-32", title="Revenue Recognition - Determining Transaction Price", weight=0.9),
            AuthoritySource(codification="ASC 606-10-55", title="Revenue Recognition - Implementation Guidance", weight=0.8),
        ],
        burden_holder="Reporting entity preparing financial statements",
        adversary_position="SEC staff may challenge aggressive revenue acceleration or improper bundling of performance obligations",
        counter_arguments=[
            "Variable consideration estimates lack sufficient constraint analysis",
            "Performance obligations not sufficiently distinct to warrant separation",
            "Over-time recognition criteria not met; point-in-time is appropriate",
            "Significant financing component ignored in long-term contracts",
            "Principal vs agent analysis incorrectly applied",
        ],
        resolution_strategy="Apply five-step model systematically with contemporaneous documentation of judgments at contract inception",
        entity_scope="All entities with customer contracts for goods or services",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 606 (FASB ASU 2014-09) effective for public entities fiscal years beginning after Dec 15, 2017",
    ),
    DoctrineBlock(
        topic="ASC 842 Lease Accounting - Lessee Model",
        keywords=["lease", "asc 842", "right-of-use", "operating lease", "finance lease", "rou asset"],
        conclusion_template=(
            "Under ASC 842, lessees recognize a right-of-use (ROU) asset and lease liability "
            "for virtually all leases exceeding 12 months. Classification as finance or operating "
            "lease determines expense pattern: finance leases show front-loaded expense (interest "
            "plus amortization), operating leases show straight-line expense."
        ),
        reasoning_framework=(
            "Lease identification requires determining whether a contract conveys the right to "
            "control an identified asset for a period of time in exchange for consideration. "
            "Control exists when lessee has right to obtain substantially all economic benefits "
            "and direct the use of the asset. Classification criteria for finance lease: "
            "(a) transfer of ownership, (b) purchase option reasonably certain, (c) lease term "
            "is major part of economic life, (d) present value of payments is substantially all "
            "of fair value, (e) asset is specialized with no alternative use to lessor. "
            "If none met, classify as operating. Initial measurement: lease liability at PV of "
            "lease payments using rate implicit in lease or incremental borrowing rate. "
            "ROU asset = lease liability + prepaid rents - lease incentives + initial direct costs."
        ),
        key_factors=[
            "Identification of embedded leases in service contracts",
            "Lease term determination including renewal and termination options",
            "Discount rate selection (implicit rate vs IBR)",
            "Variable lease payment treatment (index-based vs usage-based)",
            "Short-term lease election and low-value asset exemption",
            "Lease modification and reassessment triggers",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 842-10-25", title="Leases - Recognition", weight=1.0),
            AuthoritySource(codification="ASC 842-20-25", title="Leases - Lessee Recognition", weight=0.95),
            AuthoritySource(codification="ASC 842-10-55", title="Leases - Implementation Guidance", weight=0.8),
        ],
        burden_holder="Lessee entity",
        adversary_position="Auditors may challenge IBR calculation methodology or lease term assumptions",
        counter_arguments=[
            "Embedded lease identification missed in complex service arrangements",
            "IBR does not reflect entity-specific credit risk properly",
            "Renewal options assessment lacks sufficient evidence of reasonably certain exercise",
            "Variable payments incorrectly excluded from liability measurement",
            "Lease modifications improperly accounted for as new leases vs remeasurement",
        ],
        resolution_strategy="Maintain lease inventory with systematic reassessment triggers; document IBR methodology with treasury support",
        entity_scope="All lessee entities with lease arrangements",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 842 (FASB ASU 2016-02) effective for public entities fiscal years beginning after Dec 15, 2018",
    ),
    DoctrineBlock(
        topic="ASC 326 Current Expected Credit Losses (CECL)",
        keywords=["cecl", "credit loss", "asc 326", "allowance", "expected loss", "impairment"],
        conclusion_template=(
            "ASC 326 requires measurement of expected credit losses on financial assets "
            "held at amortized cost based on historical experience, current conditions, "
            "and reasonable and supportable forecasts. The CECL model replaces the incurred "
            "loss model with a lifetime expected loss approach recognized at origination."
        ),
        reasoning_framework=(
            "The CECL model requires entities to estimate lifetime expected credit losses "
            "using relevant information about past events, current conditions, and reasonable "
            "and supportable forecasts. Methodologies include: vintage analysis, loss rate "
            "methods, probability of default methods, discounted cash flow methods. "
            "Key considerations: segmentation of financial assets by shared risk characteristics, "
            "reversion to historical loss rates beyond supportable forecast period, "
            "qualitative adjustments for factors not captured in quantitative models, "
            "and zero-loss estimate permissible only when expectations support it."
        ),
        key_factors=[
            "Portfolio segmentation by risk characteristics",
            "Reasonable and supportable forecast period length",
            "Reversion method to historical loss information",
            "Qualitative factor adjustments (Q-factors)",
            "Collateral-dependent financial asset treatment",
            "Purchased credit-deteriorated (PCD) asset recognition",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 326-20-30", title="Credit Losses - Measured at Amortized Cost", weight=1.0),
            AuthoritySource(codification="ASC 326-20-55", title="Credit Losses - Implementation Guidance", weight=0.85),
        ],
        burden_holder="Entity holding financial assets at amortized cost",
        adversary_position="Regulators may challenge insufficient allowance levels or inadequate forecasting methodology",
        counter_arguments=[
            "Forecast period too short relative to asset duration",
            "Reversion technique creates cliff effect in estimates",
            "Qualitative adjustments lack documentation and repeatability",
            "Segmentation too broad, masking concentration risk",
            "Model validation insufficient for regulatory examination",
        ],
        resolution_strategy="Implement model governance framework with back-testing, sensitivity analysis, and board-level oversight documentation",
        entity_scope="Financial institutions and entities holding receivables, loans, debt securities at amortized cost",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 326 (FASB ASU 2016-13) effective for SEC filers fiscal years beginning after Dec 15, 2019",
    ),
    DoctrineBlock(
        topic="Income Statement Presentation and Classification",
        keywords=["income statement", "revenue", "expenses", "earnings", "net income", "comprehensive income"],
        conclusion_template=(
            "The income statement presents an entity's financial performance over a period, "
            "classifying items as operating or non-operating. ASC 220 requires presentation "
            "of comprehensive income either in a single continuous statement or in two "
            "consecutive statements. Operating income, while not defined by GAAP, is a "
            "critical subtotal used by analysts and must be presented consistently."
        ),
        reasoning_framework=(
            "Income statement classification follows the matching principle and accrual basis. "
            "Revenue is recognized per ASC 606. Cost of goods sold includes direct material, "
            "labor, and overhead. Operating expenses include SGA, R&D, depreciation. "
            "Non-operating items: interest, investment gains/losses, FX gains/losses. "
            "Discontinued operations per ASC 205-20 presented net of tax below continuing ops. "
            "Extraordinary items eliminated by ASU 2015-01. EPS required for public entities: "
            "basic and diluted per ASC 260. OCI items: unrealized gains/losses on AFS securities, "
            "foreign currency translation, pension adjustments, cash flow hedge effectiveness."
        ),
        key_factors=[
            "Revenue and expense classification consistency",
            "Operating vs non-operating distinction",
            "Discontinued operations criteria and presentation",
            "Earnings per share calculation (basic and diluted)",
            "Comprehensive income components and reclassification",
            "Unusual or infrequent items disclosure",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 220-10", title="Income Statement - Comprehensive Income", weight=1.0),
            AuthoritySource(codification="ASC 260-10", title="Earnings Per Share", weight=0.9),
            AuthoritySource(codification="ASC 205-20", title="Discontinued Operations", weight=0.85),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC may challenge classification of recurring items as non-operating to inflate operating margins",
        counter_arguments=[
            "Non-GAAP adjustments may obscure true operating performance",
            "Reclassification of OCI items timing can be manipulated",
            "Diluted EPS calculation may exclude anti-dilutive instruments improperly",
        ],
        resolution_strategy="Consistent classification policy with clear disclosure of non-GAAP measures per Regulation G",
        entity_scope="All reporting entities",
        confidence=0.94,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 220 (SFAS 130) and SEC Regulation S-X Article 5",
    ),
    DoctrineBlock(
        topic="Balance Sheet Classification and Presentation",
        keywords=["balance sheet", "assets", "liabilities", "equity", "current", "non-current", "classified"],
        conclusion_template=(
            "The balance sheet presents an entity's financial position at a point in time, "
            "classified into current and non-current categories. Current assets are expected "
            "to be realized within one year or the operating cycle; current liabilities are "
            "expected to be settled within the same period. Working capital analysis is "
            "fundamental to liquidity assessment."
        ),
        reasoning_framework=(
            "Classification rules: Current assets include cash, marketable securities, "
            "receivables collectible within one year, inventory, and prepaid expenses. "
            "Non-current: PP&E, intangible assets, goodwill, long-term investments, ROU assets. "
            "Current liabilities: AP, accrued expenses, current debt maturities, deferred revenue "
            "expected to be earned within one year. Non-current: long-term debt, pension obligations, "
            "deferred tax liabilities, operating lease liabilities (non-current portion). "
            "Equity: common stock, APIC, retained earnings, AOCI, treasury stock. "
            "Debt covenant violations may require reclassification of long-term debt to current "
            "unless waiver obtained before financial statement issuance date."
        ),
        key_factors=[
            "Operating cycle determination for classification",
            "Debt covenant compliance and reclassification triggers",
            "Fair value measurement hierarchy (Level 1, 2, 3)",
            "Intangible asset identification and amortization",
            "Contingent liability recognition thresholds",
            "Restricted cash presentation requirements",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 210-10", title="Balance Sheet - Overall", weight=1.0),
            AuthoritySource(codification="ASC 470-10-45", title="Debt - Classification", weight=0.9),
            AuthoritySource(codification="ASC 820-10", title="Fair Value Measurement", weight=0.85),
        ],
        burden_holder="Reporting entity",
        adversary_position="Auditors scrutinize debt classification and contingent liability disclosure completeness",
        counter_arguments=[
            "Subjective going concern assessment affects classification",
            "Fair value Level 3 inputs lack market corroboration",
            "Contingent liabilities may be under-disclosed",
        ],
        resolution_strategy="Systematic balance sheet review with debt compliance checklist and fair value documentation",
        entity_scope="All reporting entities",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 210, SEC Regulation S-X Articles 5 and 12",
    ),
    DoctrineBlock(
        topic="Statement of Cash Flows - ASC 230",
        keywords=["cash flow", "operating", "investing", "financing", "indirect method", "direct method"],
        conclusion_template=(
            "The statement of cash flows classifies cash receipts and payments into operating, "
            "investing, and financing activities. ASC 230 permits either direct or indirect "
            "method for operating activities, though the indirect method predominates in practice. "
            "Non-cash investing and financing activities must be disclosed separately."
        ),
        reasoning_framework=(
            "Operating activities: Cash from core business operations. Indirect method starts "
            "with net income, adjusts for non-cash items (depreciation, amortization, "
            "stock compensation, deferred taxes) and changes in working capital. "
            "Investing activities: Capital expenditures, acquisitions, dispositions, "
            "purchases and sales of investments. Financing activities: Debt issuance and "
            "repayment, equity issuance and repurchases, dividend payments. "
            "Classification challenges: Interest paid (operating under GAAP, can be financing "
            "under IFRS), income taxes (operating unless specifically identifiable with "
            "investing or financing), customer deposits, insurance proceeds."
        ),
        key_factors=[
            "Direct vs indirect method selection and reconciliation",
            "Classification of interest and dividends received/paid",
            "Restricted cash inclusion in cash equivalents",
            "Non-cash transaction disclosure requirements",
            "Foreign currency cash flow translation methodology",
            "Free cash flow calculation (non-GAAP)",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 230-10-45", title="Statement of Cash Flows - Classification", weight=1.0),
            AuthoritySource(codification="ASC 230-10-50", title="Statement of Cash Flows - Disclosure", weight=0.9),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC focus on proper classification, especially operating vs investing for capex-like expenditures",
        counter_arguments=[
            "Software development costs classification between operating and investing",
            "Factoring arrangements may obscure operating cash flow",
            "Supply chain financing programs distort working capital metrics",
        ],
        resolution_strategy="Document classification policy for ambiguous items; disclose non-GAAP cash flow measures with reconciliation",
        entity_scope="All reporting entities",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 230 (SFAS 95) with amendments by ASU 2016-15 and ASU 2016-18",
    ),
    DoctrineBlock(
        topic="DuPont Analysis Framework",
        keywords=["dupont", "roe", "return on equity", "profit margin", "asset turnover", "leverage"],
        conclusion_template=(
            "DuPont analysis decomposes return on equity into three components: "
            "net profit margin, asset turnover, and financial leverage (equity multiplier). "
            "This decomposition reveals whether ROE is driven by operational efficiency, "
            "asset utilization, or financial leverage, enabling targeted improvement strategies."
        ),
        reasoning_framework=(
            "Three-component DuPont: ROE = Net Profit Margin x Asset Turnover x Equity Multiplier. "
            "Net Profit Margin = Net Income / Revenue (operational efficiency). "
            "Asset Turnover = Revenue / Total Assets (asset utilization). "
            "Equity Multiplier = Total Assets / Shareholders Equity (financial leverage). "
            "Five-component extended DuPont further decomposes: Tax Burden (Net Income / EBT) "
            "x Interest Burden (EBT / EBIT) x Operating Margin (EBIT / Revenue) x Asset Turnover "
            "x Equity Multiplier. This reveals impact of tax efficiency and interest expense."
        ),
        key_factors=[
            "Net profit margin trend analysis",
            "Asset turnover by segment or business unit",
            "Leverage impact on ROE sustainability",
            "Tax burden ratio for effective tax rate analysis",
            "Interest burden for capital structure assessment",
            "Industry benchmark comparison relevance",
        ],
        primary_authority=[
            AuthoritySource(codification="CFA Institute", title="Financial Statement Analysis Framework", weight=0.8, binding=False),
        ],
        burden_holder="Financial analyst or management",
        adversary_position="Stakeholders may challenge leverage-driven ROE as unsustainable",
        counter_arguments=[
            "High leverage inflates ROE but increases bankruptcy risk",
            "Asset-light business models distort turnover comparisons",
            "Non-recurring items can distort margin analysis",
        ],
        resolution_strategy="Normalize for non-recurring items; compare within industry; assess leverage sustainability via debt service coverage",
        entity_scope="All entities subject to financial analysis",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="DuPont Corporation framework (1920s), widely adopted in financial analysis",
    ),
    DoctrineBlock(
        topic="Altman Z-Score Bankruptcy Prediction",
        keywords=["altman", "z-score", "bankruptcy", "financial distress", "credit risk", "solvency"],
        conclusion_template=(
            "The Altman Z-Score model predicts bankruptcy probability using five financial "
            "ratios: working capital/total assets, retained earnings/total assets, EBIT/total "
            "assets, market value of equity/total liabilities, and sales/total assets. "
            "Z > 2.99 indicates safe zone; 1.81-2.99 is grey zone; Z < 1.81 is distress zone."
        ),
        reasoning_framework=(
            "Original Z-Score (public manufacturing): Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5. "
            "X1 = Working Capital / Total Assets (liquidity). "
            "X2 = Retained Earnings / Total Assets (cumulative profitability). "
            "X3 = EBIT / Total Assets (operating efficiency). "
            "X4 = Market Value Equity / Book Value Total Liabilities (solvency). "
            "X5 = Sales / Total Assets (asset efficiency). "
            "Z-prime for private firms substitutes book value equity for market value in X4. "
            "Z-double-prime for non-manufacturers removes X5 (asset turnover)."
        ),
        key_factors=[
            "Model selection based on entity type (public, private, non-manufacturing)",
            "Working capital trend as leading indicator",
            "Retained earnings as measure of cumulative profitability",
            "Market vs book value of equity for solvency assessment",
            "Industry-specific adjustments and limitations",
            "Time horizon for prediction accuracy (1-2 years most reliable)",
        ],
        primary_authority=[
            AuthoritySource(codification="Altman (1968)", title="Financial Ratios, Discriminant Analysis and Prediction of Corporate Bankruptcy", weight=0.8, binding=False),
        ],
        burden_holder="Creditors, auditors, and management assessing going concern",
        adversary_position="Model may not capture industry-specific or macroeconomic factors",
        counter_arguments=[
            "Original model calibrated on 1960s manufacturing data",
            "Does not capture off-balance-sheet risks",
            "Market value component introduces volatility in assessment",
        ],
        resolution_strategy="Use as one input among multiple financial health indicators; supplement with cash flow analysis and qualitative factors",
        entity_scope="Primarily manufacturing and public companies; variants exist for other sectors",
        confidence=0.78,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Altman, E.I. (1968) Journal of Finance, widely used in credit analysis",
    ),
    DoctrineBlock(
        topic="Sarbanes-Oxley Section 404 - Internal Controls",
        keywords=["sox", "sarbanes-oxley", "internal controls", "404", "material weakness", "significant deficiency"],
        conclusion_template=(
            "SOX Section 404 requires management assessment and, for accelerated filers, "
            "auditor attestation of internal controls over financial reporting (ICFR). "
            "Material weaknesses must be disclosed and remediated. The COSO framework "
            "provides the standard structure for evaluating control effectiveness."
        ),
        reasoning_framework=(
            "COSO 2013 Framework components: (1) Control Environment - tone at the top, "
            "organizational structure, authority assignment. (2) Risk Assessment - financial "
            "reporting risk identification, fraud risk assessment. (3) Control Activities - "
            "authorization, reconciliation, segregation of duties, IT general controls. "
            "(4) Information and Communication - relevant financial information identified "
            "and communicated. (5) Monitoring - ongoing and separate evaluations. "
            "Deficiency severity: Control deficiency < Significant deficiency < Material weakness. "
            "Material weakness = reasonable possibility that material misstatement not prevented/detected."
        ),
        key_factors=[
            "Scoping of significant accounts and relevant assertions",
            "Risk assessment driving testing intensity",
            "IT general controls supporting automated controls",
            "Entity-level controls (tone at top, code of conduct)",
            "Walkthroughs and tests of operating effectiveness",
            "Remediation timeline for identified deficiencies",
        ],
        primary_authority=[
            AuthoritySource(codification="SOX Section 404", title="Management Assessment of Internal Controls", weight=1.0),
            AuthoritySource(codification="PCAOB AS 2201", title="Audit of Internal Control Over Financial Reporting", weight=0.95),
            AuthoritySource(codification="COSO 2013", title="Internal Control - Integrated Framework", weight=0.9),
        ],
        burden_holder="Management (assessment) and external auditor (attestation for accelerated filers)",
        adversary_position="PCAOB inspections may identify insufficient testing or improper scoping",
        counter_arguments=[
            "Cost of compliance disproportionate for smaller companies",
            "Control testing may not detect collusion-based fraud",
            "IT environment changes may outpace control documentation",
        ],
        resolution_strategy="Risk-based scoping with continuous monitoring technology; maintain remediation tracking with target dates",
        entity_scope="SEC reporting companies (accelerated filers require auditor attestation)",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Sarbanes-Oxley Act of 2002, PCAOB Auditing Standard No. 2201",
    ),
    DoctrineBlock(
        topic="PCAOB Audit Standards - Materiality and Risk",
        keywords=["pcaob", "materiality", "audit risk", "sampling", "detection risk", "substantive testing"],
        conclusion_template=(
            "PCAOB standards require auditors to plan and perform audits to obtain reasonable "
            "assurance about whether financial statements are free of material misstatement. "
            "Materiality is determined at both the financial statement and account levels. "
            "Audit risk = Inherent Risk x Control Risk x Detection Risk."
        ),
        reasoning_framework=(
            "Planning materiality: Typically 1-5% of a relevant benchmark (net income, revenue, "
            "total assets, equity). Performance materiality is set below overall materiality "
            "(commonly 50-75%) to reduce aggregation risk. Clearly trivial threshold (SAT) "
            "typically 3-5% of overall materiality. Risk assessment: Inherent risk factors "
            "include complexity, estimation uncertainty, susceptibility to fraud. Control risk "
            "assessed through understanding and testing of ICFR. Detection risk controlled "
            "through nature, timing, and extent of substantive procedures. "
            "Sampling: Statistical (monetary unit sampling, classical variables) or non-statistical. "
            "Sample size driven by confidence level, tolerable misstatement, expected error rate."
        ),
        key_factors=[
            "Materiality benchmark selection and percentage",
            "Performance materiality as percentage of overall materiality",
            "Clearly trivial threshold for accumulating differences",
            "Risk assessment at assertion level for significant accounts",
            "Sampling methodology selection and sample size determination",
            "Evaluation of identified misstatements (known, likely, possible)",
        ],
        primary_authority=[
            AuthoritySource(codification="PCAOB AS 2105", title="Consideration of Materiality in Planning and Performing an Audit", weight=1.0),
            AuthoritySource(codification="PCAOB AS 2110", title="Identifying and Assessing Risks of Material Misstatement", weight=0.95),
            AuthoritySource(codification="PCAOB AS 2315", title="Audit Sampling", weight=0.9),
        ],
        burden_holder="External auditor",
        adversary_position="PCAOB inspections frequently cite insufficient risk assessment procedures and materiality documentation",
        counter_arguments=[
            "Qualitative materiality factors may override quantitative thresholds",
            "Estimation uncertainty ranges challenge traditional materiality application",
            "Sampling risk inherent in any sample-based approach",
        ],
        resolution_strategy="Document materiality determination with multiple benchmarks; perform fraud risk brainstorming; link risk assessment to substantive testing",
        entity_scope="External auditors of SEC issuers",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="PCAOB Auditing Standards, AICPA AU-C sections for non-issuers",
    ),
    DoctrineBlock(
        topic="ASC 740 Income Tax Provision",
        keywords=["tax provision", "deferred tax", "asc 740", "book-tax difference", "valuation allowance", "uncertain tax"],
        conclusion_template=(
            "ASC 740 requires recognition of current and deferred income tax consequences "
            "of all events recognized in financial statements. Deferred tax assets and "
            "liabilities arise from temporary differences between book and tax basis. "
            "A valuation allowance is required when it is more likely than not that "
            "some portion of DTAs will not be realized."
        ),
        reasoning_framework=(
            "Current tax provision: taxable income x statutory rate, adjusted for credits. "
            "Deferred taxes: Identify temporary differences (depreciation methods, revenue timing, "
            "accrued liabilities, stock compensation, NOL carryforwards). Apply enacted tax rates "
            "to temporary differences. DTAs for deductible differences, DTLs for taxable differences. "
            "Valuation allowance assessment: weight of positive and negative evidence. Positive: "
            "existing taxable temp differences, tax planning strategies, future profitability. "
            "Negative: cumulative losses, history of expired carryforwards, uncertainty of projections. "
            "Uncertain tax positions (ASC 740-10-25): two-step process - recognition threshold "
            "(more likely than not) then measurement (largest amount > 50% likely). "
            "ETR reconciliation: statutory rate to effective rate with disclosure of significant items."
        ),
        key_factors=[
            "Identification of all temporary differences (comprehensive list)",
            "Enacted rate used for deferred tax measurement",
            "Valuation allowance positive and negative evidence weighing",
            "NOL and credit carryforward utilization projections",
            "Uncertain tax position recognition and measurement",
            "Intraperiod tax allocation among continuing ops, discontinued ops, OCI",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 740-10-25", title="Income Taxes - Recognition", weight=1.0),
            AuthoritySource(codification="ASC 740-10-30", title="Income Taxes - Initial Measurement", weight=0.95),
            AuthoritySource(codification="ASC 740-10-50", title="Income Taxes - Disclosure", weight=0.85),
        ],
        burden_holder="Reporting entity (management and tax department)",
        adversary_position="IRS and SEC may challenge aggressive tax positions and adequacy of valuation allowance",
        counter_arguments=[
            "Projections used for VA assessment may be overly optimistic",
            "Tax planning strategies may not be prudent and feasible",
            "Rate change impact on deferred tax balances timing",
            "International tax reform effects on deferred tax measurement",
        ],
        resolution_strategy="Maintain comprehensive deferred tax roll-forward with quarterly assessment; document uncertain positions with technical memoranda",
        entity_scope="All entities subject to income taxes",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 740 (SFAS 109, FIN 48), SEC Staff Accounting Bulletin Topic 6",
    ),
    DoctrineBlock(
        topic="Multi-Entity Consolidation - ASC 810",
        keywords=["consolidation", "variable interest entity", "vie", "noncontrolling interest", "elimination"],
        conclusion_template=(
            "ASC 810 requires consolidation when an entity has a controlling financial interest. "
            "For voting interest entities, control is typically > 50% voting rights. For VIEs, "
            "the primary beneficiary with power to direct significant activities and obligation "
            "to absorb losses or right to receive benefits must consolidate."
        ),
        reasoning_framework=(
            "Step 1: Determine if entity is a VIE. VIE exists when: equity at risk insufficient "
            "to finance activities, equity holders lack decision-making rights, or equity holders "
            "do not absorb expected losses / receive expected residual returns. "
            "Step 2: If VIE, identify primary beneficiary (power + economics test). "
            "Step 3: If not VIE, apply voting interest model (majority ownership = consolidation). "
            "Consolidation procedures: Eliminate intercompany transactions (revenue, expenses, "
            "receivables, payables, profits in inventory/fixed assets). "
            "Noncontrolling interest presented in equity section. "
            "Acquisition accounting per ASC 805: fair value of identifiable assets and liabilities, "
            "goodwill as residual."
        ),
        key_factors=[
            "VIE vs voting interest model determination",
            "Primary beneficiary assessment for VIEs",
            "Intercompany elimination completeness",
            "Noncontrolling interest measurement and presentation",
            "Step acquisition and changes in ownership treatment",
            "Loss of control deconsolidation accounting",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 810-10", title="Consolidation - Overall", weight=1.0),
            AuthoritySource(codification="ASC 805-10", title="Business Combinations", weight=0.9),
            AuthoritySource(codification="ASC 810-10-25", title="Consolidation - Variable Interest Entities", weight=0.95),
        ],
        burden_holder="Parent entity or primary beneficiary",
        adversary_position="SEC frequently challenges VIE analysis and off-balance-sheet arrangements",
        counter_arguments=[
            "Complex structures may obscure true controlling interest",
            "Related party implicit arrangements difficult to identify",
            "VIE determination highly judgmental in practice",
        ],
        resolution_strategy="Document VIE analysis at inception and upon reconsideration events; maintain intercompany elimination checklist",
        entity_scope="Entities with subsidiaries, VIEs, or significant investments",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 810 (FIN 46R, ARB 51, SFAS 160)",
    ),
    DoctrineBlock(
        topic="Foreign Currency Translation - ASC 830",
        keywords=["currency", "translation", "functional currency", "remeasurement", "asc 830", "forex"],
        conclusion_template=(
            "ASC 830 requires determination of functional currency for each foreign entity "
            "and translation of financial statements to the reporting currency. "
            "Translation (current rate method) applies when functional currency is local currency; "
            "remeasurement (temporal method) applies when functional currency is reporting currency."
        ),
        reasoning_framework=(
            "Functional currency indicators: primary cash flow generation, sales market, "
            "expenses, financing, intercompany transaction volume. Translation method: "
            "Assets/liabilities at current rate, equity at historical rates, income/expense "
            "at weighted average rate. Translation adjustment in AOCI. "
            "Remeasurement method: Monetary items at current rate, non-monetary at historical "
            "rate, income/expense at weighted average except items related to non-monetary "
            "assets (COGS, depreciation). Remeasurement gain/loss in income statement. "
            "Highly inflationary economies (cumulative 3-year inflation > 100%): "
            "remeasurement required regardless of functional currency determination."
        ),
        key_factors=[
            "Functional currency determination with economic indicators",
            "Translation vs remeasurement method selection",
            "CTA accumulation and disposition upon sale or liquidation",
            "Intercompany foreign currency transactions",
            "Highly inflationary economy identification",
            "Hedging of net investment in foreign operations",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 830-10", title="Foreign Currency Matters - Overall", weight=1.0),
            AuthoritySource(codification="ASC 830-30", title="Translation of Financial Statements", weight=0.95),
        ],
        burden_holder="Reporting entity with foreign operations",
        adversary_position="Auditors may challenge functional currency selection or translation methodology",
        counter_arguments=[
            "Mixed indicators make functional currency determination judgmental",
            "Highly inflationary threshold binary and arbitrary",
            "CTA recycling upon partial disposal is complex",
        ],
        resolution_strategy="Document functional currency analysis at entity inception; reassess upon significant operational changes",
        entity_scope="Entities with foreign subsidiaries or foreign currency transactions",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 830 (SFAS 52)",
    ),
    DoctrineBlock(
        topic="Fair Value Measurement - ASC 820",
        keywords=["fair value", "level 1", "level 2", "level 3", "market approach", "income approach"],
        conclusion_template=(
            "ASC 820 defines fair value as the exit price in an orderly transaction between "
            "market participants. The fair value hierarchy prioritizes inputs: Level 1 (quoted "
            "prices in active markets), Level 2 (observable inputs), Level 3 (unobservable inputs). "
            "Entities must disclose fair value measurements by level."
        ),
        reasoning_framework=(
            "Fair value definition: price that would be received to sell an asset or paid to "
            "transfer a liability in an orderly transaction. Not entity-specific — market "
            "participant perspective. Valuation techniques: Market approach (comparable transactions, "
            "guideline public companies), Income approach (DCF, option pricing), Cost approach "
            "(replacement cost). Highest and best use for non-financial assets. "
            "Level 1: Quoted prices for identical assets/liabilities in active markets. "
            "Level 2: Observable inputs other than Level 1 (quoted prices for similar items, "
            "interest rates, yield curves, credit spreads). Level 3: Unobservable inputs "
            "based on entity's own assumptions (projections, probability-weighted scenarios)."
        ),
        key_factors=[
            "Exit price vs entry price distinction",
            "Market participant assumptions vs entity-specific",
            "Highest and best use determination for non-financial assets",
            "Level classification and transfers between levels",
            "Discount rate selection for income approach",
            "Sensitivity analysis for Level 3 measurements",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 820-10-35", title="Fair Value Measurement", weight=1.0),
            AuthoritySource(codification="ASC 820-10-50", title="Fair Value Disclosures", weight=0.9),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC and auditors challenge Level 3 assumptions and valuation model appropriateness",
        counter_arguments=[
            "Level 3 measurements inherently subjective",
            "Illiquidity adjustments lack observable benchmarks",
            "Model risk in complex derivative valuations",
        ],
        resolution_strategy="Use independent valuation specialists for Level 3; back-test estimates against actual outcomes; disclose key assumptions and sensitivity",
        entity_scope="All entities measuring assets or liabilities at fair value",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 820 (SFAS 157)",
    ),
    DoctrineBlock(
        topic="Goodwill Impairment Testing - ASC 350",
        keywords=["goodwill", "impairment", "reporting unit", "asc 350", "qualitative", "quantitative"],
        conclusion_template=(
            "ASC 350 requires annual goodwill impairment testing at the reporting unit level. "
            "Entities may perform a qualitative assessment (Step 0) or proceed directly to "
            "quantitative testing comparing reporting unit fair value to carrying amount. "
            "Impairment exists when carrying amount exceeds fair value; loss is limited to "
            "allocated goodwill amount."
        ),
        reasoning_framework=(
            "Qualitative assessment (Step 0): Evaluate whether it is more likely than not that "
            "reporting unit fair value is less than carrying amount. Factors: macroeconomic "
            "conditions, industry/market conditions, cost factors, financial performance, "
            "entity-specific events, reporting unit fair value changes. "
            "Quantitative test: Determine fair value of reporting unit (income approach, "
            "market approach, or combination). Compare to carrying amount including goodwill. "
            "If fair value < carrying amount, impairment loss = difference, limited to goodwill. "
            "Triggering events requiring interim testing: significant decline in stock price, "
            "loss of key customer, regulatory changes, sustained losses."
        ),
        key_factors=[
            "Reporting unit identification and goodwill allocation",
            "Qualitative vs quantitative assessment election",
            "Discount rate and terminal growth rate for DCF",
            "Market multiples selection for market approach",
            "Reconciliation of reporting unit values to market cap",
            "Triggering events for interim impairment testing",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 350-20-35", title="Goodwill - Subsequent Measurement", weight=1.0),
            AuthoritySource(codification="ASC 350-20-50", title="Goodwill - Disclosure", weight=0.85),
        ],
        burden_holder="Reporting entity management",
        adversary_position="Auditors and SEC challenge valuation assumptions, especially when entity recently acquired",
        counter_arguments=[
            "Control premium implicit in acquisitions complicates fair value comparison",
            "DCF projections may be overly optimistic relative to historical performance",
            "Market cap below book value creates presumption of impairment",
        ],
        resolution_strategy="Perform annual testing consistently (same date); reconcile sum of reporting units to market cap; engage valuation specialists",
        entity_scope="Entities with recorded goodwill",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 350 as amended by ASU 2017-04 (simplified impairment test)",
    ),
    DoctrineBlock(
        topic="Stock-Based Compensation - ASC 718",
        keywords=["stock compensation", "options", "rsu", "asc 718", "grant date", "fair value", "vesting"],
        conclusion_template=(
            "ASC 718 requires measurement of stock-based compensation at grant-date fair value "
            "and recognition of expense over the requisite service period. Options are typically "
            "valued using Black-Scholes or lattice models. RSUs and restricted stock are valued "
            "at grant-date stock price less present value of foregone dividends."
        ),
        reasoning_framework=(
            "Grant-date fair value measurement: Options - Black-Scholes-Merton (European-style) "
            "or binomial lattice (American-style, incorporates early exercise). Key inputs: "
            "stock price, exercise price, expected term, risk-free rate, expected volatility, "
            "expected dividend yield. RSUs: stock price at grant date. Performance conditions: "
            "service conditions and performance conditions affect the number of awards expected "
            "to vest (probable outcome estimate). Market conditions affect fair value at grant "
            "date but not subsequent adjustment. Recognition: Generally straight-line over "
            "requisite service period for service-only conditions. Graded vesting election "
            "for awards with only service conditions."
        ),
        key_factors=[
            "Fair value model selection and input determination",
            "Expected term estimation methodology (simplified vs historical)",
            "Volatility estimation (historical, implied, peer group)",
            "Performance condition probability assessment",
            "Market condition incorporation in fair value",
            "Modification accounting for repricing or other changes",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 718-10-30", title="Compensation - Stock Compensation - Initial Measurement", weight=1.0),
            AuthoritySource(codification="ASC 718-10-35", title="Compensation - Stock Compensation - Subsequent Measurement", weight=0.9),
        ],
        burden_holder="Reporting entity (compensation committee and accounting)",
        adversary_position="SEC focuses on volatility assumptions and performance condition probability assessments",
        counter_arguments=[
            "Expected term estimation lacks entity-specific data for newly public companies",
            "Peer group volatility may not represent entity risk profile",
            "Modification accounting triggers can be inadvertent",
        ],
        resolution_strategy="Maintain grant tracking database with contemporaneous documentation of fair value inputs and performance probability assessments",
        entity_scope="Entities issuing stock-based awards to employees or non-employees",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 718 (SFAS 123R, ASU 2016-09)",
    ),
    DoctrineBlock(
        topic="Segment Reporting - ASC 280",
        keywords=["segment", "operating segment", "asc 280", "chief operating decision maker", "codm"],
        conclusion_template=(
            "ASC 280 requires disclosure of information about operating segments consistent "
            "with the management approach. Operating segments are components of an entity "
            "that engage in business activities, whose operating results are regularly "
            "reviewed by the CODM, and for which discrete financial information is available."
        ),
        reasoning_framework=(
            "Identification: Operating segments exist where (1) business activity generates "
            "revenue and incurs expenses, (2) CODM regularly reviews results to assess "
            "performance and allocate resources, (3) discrete financial information available. "
            "Aggregation criteria: Similar economic characteristics and similar in all of: "
            "nature of products/services, production processes, customer types, distribution "
            "methods, regulatory environment. Quantitative thresholds: Segment is reportable "
            "if revenue, profit/loss, or assets are >= 10% of combined totals. "
            "At least 75% of external revenue must be covered by reportable segments."
        ),
        key_factors=[
            "CODM identification and decision-making review",
            "Management approach to internal reporting structure",
            "Aggregation criteria qualitative similarity assessment",
            "Quantitative threshold testing (10% test)",
            "75% external revenue coverage test",
            "Entity-wide disclosures (products/services, geography, major customers)",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 280-10-50", title="Segment Reporting - Disclosure", weight=1.0),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC frequently challenges aggregation conclusions and CODM identification",
        counter_arguments=[
            "CODM role may be shared or ambiguous",
            "Aggregation criteria are qualitative and subjective",
            "Internal reporting may change, requiring segment reassessment",
        ],
        resolution_strategy="Align segment disclosure with internal reporting; document aggregation analysis; disclose CODM identity in practice",
        entity_scope="Public entities required to report segment information",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 280 (SFAS 131), SEC Regulation S-K Item 101",
    ),
    DoctrineBlock(
        topic="Pension and Post-Retirement Benefits - ASC 715",
        keywords=["pension", "defined benefit", "pbo", "actuarial", "asc 715", "opeb", "post-retirement"],
        conclusion_template=(
            "ASC 715 requires recognition of the funded status of defined benefit pension "
            "and OPEB plans on the balance sheet. Net periodic benefit cost includes service "
            "cost (in operating), interest cost, expected return on plan assets, and amortization "
            "of prior service cost and actuarial gains/losses (in non-operating)."
        ),
        reasoning_framework=(
            "Projected Benefit Obligation (PBO) measurement: actuarial present value of all "
            "benefits attributed to service to date, incorporating future salary increases. "
            "Fair value of plan assets measured at reporting date. Funded status = fair value "
            "of plan assets - PBO. Net periodic pension cost components: (1) Service cost "
            "(current period benefit earned), (2) Interest cost (PBO x discount rate), "
            "(3) Expected return on plan assets (FV x EROA), (4) Amortization of prior "
            "service cost, (5) Amortization of net actuarial gain/loss (corridor approach: "
            "excess of cumulative gain/loss over 10% of greater of PBO or plan assets). "
            "Actuarial assumptions: discount rate (high-quality corporate bond rate), "
            "expected return on plan assets, salary growth rate, mortality tables."
        ),
        key_factors=[
            "Discount rate selection methodology",
            "Expected return on plan assets vs actual returns",
            "Actuarial gain/loss corridor amortization",
            "Plan asset allocation and investment policy",
            "Mortality table selection and longevity risk",
            "Sensitivity analysis for key assumptions",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 715-30", title="Defined Benefit Plans - Pension", weight=1.0),
            AuthoritySource(codification="ASC 715-60", title="Defined Benefit Plans - OPEB", weight=0.9),
        ],
        burden_holder="Plan sponsor entity",
        adversary_position="Auditors and regulators challenge discount rate and EROA assumptions",
        counter_arguments=[
            "EROA assumptions may exceed achievable long-term returns",
            "Discount rate methodology differences can significantly impact PBO",
            "Mortality assumption changes create large actuarial adjustments",
        ],
        resolution_strategy="Use yield curve approach for discount rate; base EROA on asset allocation with forward-looking returns; engage qualified actuary",
        entity_scope="Entities sponsoring defined benefit pension or OPEB plans",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 715 (SFAS 87, SFAS 106, SFAS 158)",
    ),
    DoctrineBlock(
        topic="ASC 815 Hedge Accounting",
        keywords=["hedge", "derivative", "asc 815", "fair value hedge", "cash flow hedge", "effectiveness"],
        conclusion_template=(
            "ASC 815 permits special hedge accounting treatment for qualifying hedging "
            "relationships. Fair value hedges adjust hedged item and derivative to fair "
            "value through earnings. Cash flow hedges recognize effective portion of "
            "derivative gain/loss in OCI until hedged transaction affects earnings. "
            "Hedge effectiveness testing required at inception and ongoing."
        ),
        reasoning_framework=(
            "Hedge designation: Fair value hedge (offsets changes in fair value of recognized "
            "asset/liability or firm commitment), Cash flow hedge (offsets variability in cash "
            "flows of forecasted transaction or floating-rate debt), Net investment hedge "
            "(offsets FX exposure in foreign operations). Documentation at inception: risk "
            "management objective, hedged item, hedging instrument, effectiveness assessment "
            "method, how ineffectiveness measured. Effectiveness methods: dollar-offset, "
            "regression analysis, shortcut method (limited), critical terms match (simplified). "
            "ASU 2017-12 simplifications: eliminated requirement to separately measure and "
            "report hedge ineffectiveness for cash flow and net investment hedges."
        ),
        key_factors=[
            "Hedge relationship type selection and designation",
            "Contemporaneous documentation at inception",
            "Effectiveness assessment method selection",
            "Excluded components treatment (time value, FX basis spread)",
            "Hypothetical derivative method for cash flow hedge effectiveness",
            "De-designation and re-designation requirements",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 815-20", title="Derivatives - Hedging", weight=1.0),
            AuthoritySource(codification="ASC 815-10", title="Derivatives - Overall", weight=0.9),
        ],
        burden_holder="Reporting entity with hedging activities",
        adversary_position="Auditors challenge effectiveness documentation and forecasted transaction probability",
        counter_arguments=[
            "Hedge effectiveness may deteriorate requiring de-designation",
            "Forecasted transaction may not be probable",
            "Documentation deficiencies can disqualify hedge accounting",
        ],
        resolution_strategy="Maintain hedge documentation repository; perform prospective and retrospective testing quarterly; monitor forecasted transactions for probability",
        entity_scope="Entities using derivatives for risk management",
        confidence=0.86,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 815 (SFAS 133) as amended by ASU 2017-12",
    ),
    DoctrineBlock(
        topic="Going Concern Assessment - ASC 205-40",
        keywords=["going concern", "substantial doubt", "liquidation", "asc 205-40", "continuity"],
        conclusion_template=(
            "ASC 205-40 requires management to evaluate whether substantial doubt exists "
            "about the entity's ability to continue as a going concern within one year of "
            "financial statement issuance. If conditions raise substantial doubt, management "
            "must evaluate mitigating plans and disclose the conditions and plans."
        ),
        reasoning_framework=(
            "Assessment process: (1) Identify conditions that raise substantial doubt "
            "(recurring losses, working capital deficiency, debt covenant violations, "
            "loss of key customer, pending litigation). (2) Evaluate whether management's "
            "plans alleviate the doubt (probability and timeliness of plan execution). "
            "(3) Disclosure: If doubt alleviated by plans, disclose principal conditions "
            "and management's plans. If doubt NOT alleviated, disclose conditions, plans, "
            "and statement that substantial doubt exists. Assessment window: one year "
            "after financial statement issuance date (not balance sheet date)."
        ),
        key_factors=[
            "One-year assessment window from issuance date",
            "Identification of adverse conditions and events",
            "Management plan feasibility and timing assessment",
            "Debt covenant compliance and waiver availability",
            "Cash flow projection reliability for assessment period",
            "Disclosure requirements depend on whether doubt is alleviated",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 205-40", title="Going Concern", weight=1.0),
            AuthoritySource(codification="PCAOB AS 2415", title="Consideration of Entity's Ability to Continue as Going Concern", weight=0.9),
        ],
        burden_holder="Management (every reporting period assessment)",
        adversary_position="Auditors have independent obligation to evaluate and may reach different conclusion",
        counter_arguments=[
            "Management plans may not be sufficiently probable",
            "Cash flow projections underlying assessment may be overly optimistic",
            "Subsequent events may change going concern assessment",
        ],
        resolution_strategy="Perform assessment quarterly; document both conditions and mitigating plans; prepare cash flow scenarios (base, stress, severe)",
        entity_scope="All reporting entities",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 205-40 (ASU 2014-15)",
    ),
    DoctrineBlock(
        topic="IFRS Convergence - Key Differences from US GAAP",
        keywords=["ifrs", "convergence", "international", "gaap differences", "iasb", "fasb"],
        conclusion_template=(
            "While IFRS and US GAAP have converged significantly, material differences remain "
            "in areas such as inventory (no LIFO under IFRS), development costs (capitalized "
            "under IAS 38 if criteria met), and lease classification (no bright-line tests). "
            "SEC-registered foreign private issuers may file using IFRS without reconciliation."
        ),
        reasoning_framework=(
            "Key remaining differences: Inventory - IFRS prohibits LIFO; GAAP permits. "
            "Development costs - IAS 38 requires capitalization if criteria met; ASC 730 "
            "expenses most R&D. Impairment - IFRS allows reversal of non-goodwill impairment; "
            "GAAP does not. Leases - IFRS 16 has single lessee model (all finance); ASC 842 "
            "has dual model. Revenue - largely converged (IFRS 15 and ASC 606). Financial "
            "instruments - IFRS 9 categories differ from ASC 320/ASC 326. Property revaluation "
            "permitted under IFRS, not under GAAP. Presentation: IFRS requires minimum line "
            "items; GAAP has more prescriptive formats (Reg S-X)."
        ),
        key_factors=[
            "Inventory method differences (LIFO prohibition)",
            "Development cost capitalization criteria under IAS 38",
            "Impairment reversal treatment differences",
            "Lease classification single vs dual model",
            "Financial instrument classification and measurement",
            "Presentation and disclosure format differences",
        ],
        primary_authority=[
            AuthoritySource(codification="IFRS Standards", title="International Financial Reporting Standards", weight=0.8),
            AuthoritySource(codification="SEC Release 33-8879", title="Acceptance of IFRS for Foreign Private Issuers", weight=0.7),
        ],
        burden_holder="Entities reporting under IFRS or dual-reporting",
        adversary_position="Stakeholders may question comparability across GAAP frameworks",
        counter_arguments=[
            "Convergence projects stalled on several key topics",
            "National variations in IFRS application reduce comparability",
            "SEC has not mandated IFRS for domestic issuers",
        ],
        resolution_strategy="Maintain GAAP difference analysis for dual-listed entities; quantify impact of key differences on financial statements",
        entity_scope="Multinational entities, foreign private issuers, and entities considering IFRS adoption",
        confidence=0.82,
        confidence_stratification=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="IFRS Foundation Standards, SEC recognition of IFRS for FPIs",
    ),
    DoctrineBlock(
        topic="Liquidity Ratio Analysis",
        keywords=["liquidity", "current ratio", "quick ratio", "cash ratio", "working capital"],
        conclusion_template=(
            "Liquidity ratios measure an entity's ability to meet short-term obligations. "
            "Current ratio (current assets / current liabilities) provides a broad measure; "
            "quick ratio excludes inventory for a more conservative view; cash ratio represents "
            "the most conservative liquidity measure using only cash and equivalents."
        ),
        reasoning_framework=(
            "Current Ratio = Current Assets / Current Liabilities. Benchmark: 1.5-2.0 is "
            "generally healthy; < 1.0 indicates potential liquidity stress. Quick Ratio = "
            "(Cash + Short-term Investments + Receivables) / Current Liabilities. Removes "
            "inventory conversion uncertainty. Cash Ratio = (Cash + Cash Equivalents) / "
            "Current Liabilities. Most conservative, rarely > 1.0. Working Capital = "
            "Current Assets - Current Liabilities. Cash Conversion Cycle = DSO + DIO - DPO "
            "(days to convert investment to cash). Operating Cash Flow Ratio = Operating "
            "Cash Flow / Current Liabilities. Links accrual-based ratios to actual cash generation."
        ),
        key_factors=[
            "Industry-specific benchmarks for ratio interpretation",
            "Seasonal variations in working capital components",
            "Quality of current assets (collectibility, obsolescence)",
            "Off-balance-sheet commitments affecting true liquidity",
            "Credit facility availability as liquidity supplement",
            "Cash conversion cycle trend analysis",
        ],
        primary_authority=[
            AuthoritySource(codification="CFA Institute", title="Financial Analysis Techniques", weight=0.7, binding=False),
        ],
        burden_holder="Management, analysts, creditors",
        adversary_position="Ratios may not capture off-balance-sheet liquidity risks or contingent obligations",
        counter_arguments=[
            "Window dressing can temporarily inflate period-end ratios",
            "Industry benchmarks may not be relevant for diversified entities",
            "Point-in-time measurement misses intra-period variability",
        ],
        resolution_strategy="Calculate ratios monthly; trend analysis over 8+ quarters; supplement with cash flow projections and stress testing",
        entity_scope="All entities",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Standard financial analysis framework",
    ),
    DoctrineBlock(
        topic="Profitability Ratio Analysis",
        keywords=["profitability", "gross margin", "operating margin", "net margin", "roa", "roe"],
        conclusion_template=(
            "Profitability ratios assess an entity's ability to generate earnings relative "
            "to revenue, assets, equity, and other metrics. Gross margin, operating margin, "
            "and net margin measure income statement efficiency; ROA and ROE measure return "
            "on invested capital from different perspectives."
        ),
        reasoning_framework=(
            "Gross Margin = Gross Profit / Revenue. Measures production/service delivery "
            "efficiency. Operating Margin = Operating Income / Revenue. Measures core business "
            "profitability. Net Margin = Net Income / Revenue. After all items including tax "
            "and interest. EBITDA Margin = EBITDA / Revenue. Proxy for operating cash generation. "
            "ROA = Net Income / Average Total Assets. Returns generated from asset base. "
            "ROE = Net Income / Average Shareholders Equity. Returns to equity holders. "
            "ROIC = NOPAT / Invested Capital. Returns on all invested capital (debt + equity), "
            "best measure for comparing entities with different capital structures."
        ),
        key_factors=[
            "Revenue recognition policy impact on margins",
            "Cost classification between COGS and operating expenses",
            "Non-recurring items normalization for trend analysis",
            "Capital structure effect on ROA vs ROE comparison",
            "ROIC as capital-structure-neutral return measure",
            "Industry-specific profitability benchmarks",
        ],
        primary_authority=[
            AuthoritySource(codification="CFA Institute", title="Financial Analysis Techniques", weight=0.7, binding=False),
        ],
        burden_holder="Management and financial analysts",
        adversary_position="Non-GAAP profitability measures may mislead if adjustments are not transparent",
        counter_arguments=[
            "EBITDA ignores capital expenditure requirements",
            "ROE inflated by leverage may be unsustainable",
            "Non-recurring item exclusions may become recurring",
        ],
        resolution_strategy="Present GAAP and adjusted measures with clear reconciliation; trend analysis over multiple periods; compare within industry peer group",
        entity_scope="All entities",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Standard financial analysis framework, SEC Regulation G for non-GAAP measures",
    ),
    DoctrineBlock(
        topic="Leverage and Solvency Ratio Analysis",
        keywords=["leverage", "debt to equity", "interest coverage", "solvency", "debt ratio", "capitalization"],
        conclusion_template=(
            "Leverage ratios measure the extent to which an entity uses debt financing and "
            "its ability to service that debt. Debt-to-equity, debt-to-capital, and interest "
            "coverage ratios are fundamental to credit analysis and capital structure assessment."
        ),
        reasoning_framework=(
            "Debt-to-Equity = Total Debt / Shareholders Equity. Measures financial leverage. "
            "Debt-to-Capital = Total Debt / (Total Debt + Equity). Shows debt as proportion "
            "of total capitalization. Interest Coverage = EBIT / Interest Expense. Ability to "
            "service interest. Fixed Charge Coverage = (EBIT + Lease Payments) / (Interest + "
            "Lease Payments). Broader than interest coverage. Debt-to-EBITDA = Total Debt / "
            "EBITDA. Common credit metric (covenant), typical threshold 3-4x. Long-term Debt "
            "to Capitalization ratio isolates long-term leverage from working capital debt."
        ),
        key_factors=[
            "Debt definition (financial debt vs all liabilities)",
            "Operating lease liability inclusion post-ASC 842",
            "Off-balance-sheet obligations and guarantees",
            "Covenant compliance measurement dates",
            "Pro forma adjustments for recent transactions",
            "Rating agency methodology differences",
        ],
        primary_authority=[
            AuthoritySource(codification="CFA Institute", title="Financial Analysis Techniques", weight=0.7, binding=False),
            AuthoritySource(codification="S&P Global", title="Corporate Credit Rating Methodology", weight=0.6, binding=False),
        ],
        burden_holder="Management, creditors, rating agencies",
        adversary_position="Off-balance-sheet items may understate true leverage",
        counter_arguments=[
            "EBITDA-based metrics ignore working capital needs and capex",
            "Operating leases now on balance sheet change comparability with historical ratios",
            "Hybrid instruments blur debt-equity classification",
        ],
        resolution_strategy="Calculate using multiple debt definitions; disclose operating lease impact; compare to covenant definitions specifically",
        entity_scope="All entities with debt obligations",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Standard financial analysis framework and credit rating methodologies",
    ),
    DoctrineBlock(
        topic="Variance Analysis - Budget vs Actual",
        keywords=["variance", "budget", "actual", "favorable", "unfavorable", "flexible budget"],
        conclusion_template=(
            "Variance analysis compares actual results to budgeted or standard amounts to "
            "identify deviations requiring management attention. Favorable variances increase "
            "income; unfavorable decrease income. Flexible budgets adjust for actual activity "
            "levels to isolate volume from rate/efficiency variances."
        ),
        reasoning_framework=(
            "Static budget variance = Actual - Static Budget. Mixes volume and rate effects. "
            "Flexible budget adjusts budgeted amounts to actual volume: Flexible Budget = "
            "Variable Cost Rate x Actual Volume + Fixed Costs. Sales volume variance = "
            "Flexible Budget - Static Budget. Flexible budget variance = Actual - Flexible Budget. "
            "Further decomposition: Price variance (actual price vs standard price x actual quantity). "
            "Efficiency variance (actual quantity vs standard quantity x standard price). "
            "Revenue variances: Price, volume, and mix variances. Cost variances: material "
            "price/usage, labor rate/efficiency, overhead spending/efficiency/volume."
        ),
        key_factors=[
            "Flexible budget preparation at actual volume",
            "Price vs quantity/efficiency decomposition",
            "Revenue variance decomposition (price, volume, mix)",
            "Standard cost currency for manufacturing variances",
            "Materiality threshold for investigation",
            "Root cause analysis for recurring unfavorable variances",
        ],
        primary_authority=[
            AuthoritySource(codification="IMA", title="Management Accounting Standards", weight=0.6, binding=False),
        ],
        burden_holder="Management and budget owners",
        adversary_position="Board and investors challenge explanations for significant unfavorable variances",
        counter_arguments=[
            "Standard costs may be outdated and not reflect current conditions",
            "Favorable variances can indicate quality cuts, not efficiency gains",
            "Volume variance in fixed costs is partly a planning issue",
        ],
        resolution_strategy="Monthly variance reporting with flexible budget; investigate variances > 5% or $threshold; require corrective action plans",
        entity_scope="All entities with budgeting processes",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Management accounting best practices",
    ),
    DoctrineBlock(
        topic="Inventory Accounting - ASC 330",
        keywords=["inventory", "lifo", "fifo", "weighted average", "lower of cost", "net realizable value"],
        conclusion_template=(
            "ASC 330 requires inventory measurement at the lower of cost and net realizable "
            "value (for FIFO/average cost) or lower of cost or market (for LIFO/retail). "
            "Cost flow assumptions (FIFO, LIFO, weighted average) affect COGS and ending "
            "inventory valuation differently, especially during inflationary periods."
        ),
        reasoning_framework=(
            "Cost flow assumptions: FIFO — first costs in are first costs out; ending inventory "
            "at most recent costs. LIFO — last costs in are first costs out; ending inventory "
            "at oldest costs (LIFO reserve represents difference from FIFO). Weighted average — "
            "total cost / total units. Lower of cost and NRV (ASU 2015-11): write down to NRV "
            "when cost exceeds NRV; no write-up above cost. LIFO layers and liquidation: "
            "involuntary LIFO liquidation of old layers creates income distortion. "
            "Standard costing acceptable if reasonably approximates actual cost."
        ),
        key_factors=[
            "Cost flow assumption selection and consistency",
            "LIFO reserve analysis and conversion to FIFO",
            "NRV estimation for lower of cost and NRV testing",
            "Overhead allocation methodology for manufactured inventory",
            "LIFO liquidation impact on income",
            "Inventory count procedures and cutoff testing",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 330-10", title="Inventory - Overall", weight=1.0),
            AuthoritySource(codification="ASC 330-10-35", title="Inventory - Subsequent Measurement", weight=0.9),
        ],
        burden_holder="Reporting entity",
        adversary_position="Auditors focus on NRV estimates, overhead allocation, and count observations",
        counter_arguments=[
            "LIFO creates balance sheet distortion for old inventory layers",
            "Overhead allocation rates affect inventory valuation significantly",
            "Obsolescence reserves require significant judgment",
        ],
        resolution_strategy="Document cost flow assumption rationale; perform lower of cost/NRV testing quarterly; reconcile standard cost variances",
        entity_scope="Entities holding inventory",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 330 (ARB 43 Ch. 4, ASU 2015-11)",
    ),
    DoctrineBlock(
        topic="Business Combinations - ASC 805",
        keywords=["acquisition", "business combination", "purchase price", "goodwill", "asc 805", "merger"],
        conclusion_template=(
            "ASC 805 requires the acquisition method for all business combinations: identify "
            "the acquirer, determine acquisition date, recognize and measure identifiable "
            "assets acquired and liabilities assumed at fair value, and recognize goodwill "
            "or bargain purchase gain. Contingent consideration is measured at fair value."
        ),
        reasoning_framework=(
            "Acquisition method steps: (1) Identify acquirer (entity obtaining control). "
            "(2) Determine acquisition date (date control obtained). (3) Recognize identifiable "
            "assets/liabilities at acquisition-date fair value. Includes: tangible assets, "
            "intangible assets (customer relationships, technology, trade names, contracts), "
            "contingent liabilities if fair value determinable. (4) Goodwill = consideration "
            "transferred + NCI + previously held equity interest - net identifiable assets. "
            "Contingent consideration: classified as equity or liability; liability remeasured "
            "at fair value each period. Measurement period: up to 1 year for purchase price "
            "allocation adjustments. Acquisition costs expensed as incurred."
        ),
        key_factors=[
            "Acquirer identification in complex transactions",
            "Fair value determination of identifiable intangible assets",
            "Contingent consideration classification and measurement",
            "NCI measurement (fair value or proportionate share)",
            "Measurement period adjustments vs subsequent changes",
            "Pre-existing relationship settlement upon acquisition",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 805-10", title="Business Combinations - Overall", weight=1.0),
            AuthoritySource(codification="ASC 805-20", title="Business Combinations - Identifiable Assets", weight=0.95),
            AuthoritySource(codification="ASC 805-30", title="Business Combinations - Goodwill", weight=0.9),
        ],
        burden_holder="Acquirer entity",
        adversary_position="SEC and auditors challenge fair value of intangibles, especially customer relationships and technology",
        counter_arguments=[
            "Intangible asset identification may be incomplete",
            "Contingent consideration fair value highly uncertain",
            "Measurement period adjustments may be used to manage earnings",
        ],
        resolution_strategy="Engage independent valuation specialists; document identification of all intangible assets; track measurement period adjustments separately",
        entity_scope="Entities completing business combinations",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 805 (SFAS 141R)",
    ),
    DoctrineBlock(
        topic="Debt and Equity Classification - ASC 480/ASC 815",
        keywords=["debt", "equity", "classification", "convertible", "warrant", "preferred stock"],
        conclusion_template=(
            "Classification of financial instruments as debt or equity follows ASC 480 "
            "(distinguishing liabilities from equity) and ASC 815-40 (derivatives indexed "
            "to entity's own stock). Mandatorily redeemable instruments and obligations "
            "settleable in variable shares are classified as liabilities."
        ),
        reasoning_framework=(
            "ASC 480 scope: Mandatorily redeemable financial instruments (liability at fair value "
            "or redemption amount). Obligations to repurchase entity shares (treasury stock "
            "forward). Obligations settleable with variable number of shares (value settled). "
            "ASC 815-40: Derivatives on entity's own stock classified as equity if indexed to "
            "own stock AND meet equity classification conditions (fixed-for-fixed). "
            "ASU 2020-06 simplified convertible instruments: eliminated most beneficial conversion "
            "feature models, eliminated cash conversion model. Most convertibles now single unit "
            "of account (debt). Warrants: analyze under ASC 480 first, then ASC 815-40."
        ),
        key_factors=[
            "Mandatorily redeemable features analysis",
            "Fixed-for-fixed assessment for equity classification",
            "Convertible instrument unit of account determination",
            "Warrant classification (debt vs equity host)",
            "Freestanding vs embedded instrument analysis",
            "Settlement provisions impact on classification",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 480-10", title="Distinguishing Liabilities from Equity", weight=1.0),
            AuthoritySource(codification="ASC 815-40", title="Derivatives - Contracts on Entity's Own Equity", weight=0.95),
        ],
        burden_holder="Reporting entity issuing complex financial instruments",
        adversary_position="SEC frequently challenges debt-equity classification for complex instruments",
        counter_arguments=[
            "Settlement provisions may create unexpected liability classification",
            "Anti-dilution adjustments may violate fixed-for-fixed requirement",
            "Embedded conversion features require careful bifurcation analysis",
        ],
        resolution_strategy="Analyze instruments under ASC 480, then ASC 815 sequentially; document settlement provisions exhaustively; consult accounting advisors for complex structures",
        entity_scope="Entities issuing convertible instruments, warrants, preferred stock with redemption features",
        confidence=0.85,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 480, ASC 815-40, ASU 2020-06",
    ),
    DoctrineBlock(
        topic="Revenue Disaggregation and Contract Assets/Liabilities",
        keywords=["disaggregation", "contract asset", "contract liability", "deferred revenue", "unbilled revenue"],
        conclusion_template=(
            "ASC 606-10-50 requires disaggregation of revenue into categories depicting how "
            "economic factors affect revenue and cash flows. Contract assets arise when entity "
            "has right to consideration conditional on future performance; contract liabilities "
            "(deferred revenue) arise when consideration received before performance."
        ),
        reasoning_framework=(
            "Disaggregation categories: type of good/service, geography, market/customer type, "
            "contract type, timing of transfer (point-in-time vs over-time). Contract asset = "
            "right to consideration conditional on completing additional performance obligations "
            "(differs from receivable, which is unconditional right). Contract liability = "
            "obligation to transfer goods/services for which consideration received. "
            "Significant judgments: methods for recognizing revenue (output vs input methods "
            "for over-time), transaction price estimation, standalone selling price allocation."
        ),
        key_factors=[
            "Disaggregation category selection aligned with management reporting",
            "Contract asset vs receivable distinction",
            "Contract liability revenue recognition timing",
            "Remaining performance obligation disclosure",
            "Significant judgment disclosure requirements",
            "Contract cost capitalization (ASC 340-40)",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 606-10-50", title="Revenue Recognition - Disclosure", weight=1.0),
            AuthoritySource(codification="ASC 340-40", title="Other Assets - Contracts with Customers", weight=0.85),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC focus on disaggregation sufficiency and remaining performance obligation completeness",
        counter_arguments=[
            "Disaggregation categories may not align with how analysts view the business",
            "Contract asset impairment testing methodology unclear",
            "Practical expedients may reduce comparability",
        ],
        resolution_strategy="Align disaggregation with operating segments and investor expectations; perform quarterly contract asset impairment assessment",
        entity_scope="All entities with customer contracts",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 606-10-50 (FASB ASU 2014-09)",
    ),
    DoctrineBlock(
        topic="Subsequent Events - ASC 855",
        keywords=["subsequent events", "recognized", "non-recognized", "type 1", "type 2", "issuance date"],
        conclusion_template=(
            "ASC 855 requires evaluation of events occurring after the balance sheet date "
            "but before financial statement issuance. Recognized events (Type I) provide "
            "additional evidence about conditions existing at the balance sheet date. "
            "Non-recognized events (Type II) arise from conditions after the balance sheet "
            "date and require disclosure only."
        ),
        reasoning_framework=(
            "Evaluation period: balance sheet date through financial statement issuance date "
            "(SEC filers) or date available to be issued (non-SEC). Type I (recognized): "
            "conditions existed at balance sheet date — adjust financial statements. Examples: "
            "resolution of litigation, customer bankruptcy, inventory write-down confirmation. "
            "Type II (non-recognized): conditions arose after balance sheet date — disclose "
            "but do not adjust. Examples: business combination, natural disaster, stock offering. "
            "Reissued financial statements: evaluate through reissuance date."
        ),
        key_factors=[
            "Issuance date vs available-to-be-issued date determination",
            "Type I vs Type II classification judgment",
            "Going concern implications of subsequent events",
            "Dual-dating of auditor report for specific subsequent events",
            "Disclosure sufficiency for non-recognized events",
            "Impact on deferred tax and contingency assessments",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 855-10", title="Subsequent Events", weight=1.0),
        ],
        burden_holder="Management and auditors",
        adversary_position="Auditors must perform subsequent event procedures through report date",
        counter_arguments=[
            "Classification between Type I and Type II can be judgmental",
            "Late-breaking events near filing deadline create time pressure",
            "Dual-dating creates additional audit work scope",
        ],
        resolution_strategy="Establish subsequent events review checklist with legal, treasury, and operations input; document classification judgments",
        entity_scope="All reporting entities",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 855 (SFAS 165)",
    ),
    DoctrineBlock(
        topic="Non-GAAP Financial Measures - Regulation G",
        keywords=["non-gaap", "adjusted", "ebitda", "regulation g", "pro forma", "reconciliation"],
        conclusion_template=(
            "Regulation G and SEC Item 10(e) govern the use of non-GAAP financial measures "
            "in SEC filings and earnings releases. Non-GAAP measures must be reconciled to "
            "the most directly comparable GAAP measure, cannot exclude normal recurring charges, "
            "and must not be presented with greater prominence than GAAP measures."
        ),
        reasoning_framework=(
            "Non-GAAP measure: numerical measure of financial performance excluding amounts "
            "included in (or including amounts excluded from) the most comparable GAAP measure. "
            "Requirements: (1) Reconciliation to GAAP measure, (2) Statement of reasons for "
            "usefulness, (3) How management uses the measure, (4) Equal or less prominence "
            "than GAAP. Prohibited adjustments: individually tailored revenue recognition "
            "methods, eliminating cash charges considered normal and recurring. "
            "Common acceptable adjustments: restructuring charges, acquisition-related costs, "
            "stock compensation expense (though SEC scrutiny increasing), amortization of "
            "acquired intangibles, litigation settlements."
        ),
        key_factors=[
            "Reconciliation completeness and accuracy",
            "Prominence of GAAP vs non-GAAP measures",
            "Nature of excluded items (recurring vs non-recurring)",
            "Consistency of adjustments period over period",
            "Tax effect calculation for each adjustment",
            "SEC comment letter focus areas for non-GAAP",
        ],
        primary_authority=[
            AuthoritySource(codification="SEC Regulation G", title="Condition for Use of Non-GAAP Financial Measures", weight=1.0),
            AuthoritySource(codification="SEC Item 10(e)", title="Regulation S-K - Non-GAAP Measures", weight=0.95),
        ],
        burden_holder="Reporting entity (management and disclosure committee)",
        adversary_position="SEC staff actively comments on non-GAAP presentation issues",
        counter_arguments=[
            "Adjusted EBITDA may exclude significant recurring expenses",
            "Per-share non-GAAP measures receive heightened scrutiny",
            "Liquidity measures presented as performance measures may be misleading",
        ],
        resolution_strategy="Maintain non-GAAP policy document; review SEC comment letter trends quarterly; ensure consistency and transparent disclosure",
        entity_scope="SEC registrants using non-GAAP measures",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="SEC Regulation G, SEC C&DI on Non-GAAP Financial Measures (updated regularly)",
    ),
    DoctrineBlock(
        topic="Related Party Transactions - ASC 850",
        keywords=["related party", "asc 850", "arm's length", "key management", "affiliated entity"],
        conclusion_template=(
            "ASC 850 requires disclosure of related party relationships and transactions. "
            "Related parties include affiliates, principal owners, management, and their "
            "immediate families. Financial statements cannot state that related party "
            "transactions were at arm's length unless that fact is substantiated."
        ),
        reasoning_framework=(
            "Related party identification: parent-subsidiary, entities under common control, "
            "equity method investees, trusts for employee benefit, principal owners (>10%), "
            "management and their immediate families. Required disclosures: nature of relationship, "
            "description of transactions, dollar amounts, amounts due to/from, terms and manner "
            "of settlement. Key accounting: related party transactions may not be arm's length; "
            "cannot presume or assert arm's length pricing without evidence. Transfers between "
            "entities under common control at historical cost. Management compensation disclosure "
            "under proxy rules (not ASC 850 per se but related)."
        ),
        key_factors=[
            "Comprehensive related party identification procedures",
            "Management questionnaires and confirmation",
            "Transfer pricing documentation for intercompany transactions",
            "Arm's length assertion requirements and evidence",
            "Beneficial ownership analysis for hidden relationships",
            "Board approval requirements for related party transactions",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 850-10", title="Related Party Disclosures", weight=1.0),
            AuthoritySource(codification="SEC Regulation S-K Item 404", title="Transactions with Related Persons", weight=0.9),
        ],
        burden_holder="Reporting entity management and audit committee",
        adversary_position="Auditors must identify and assess related party transactions for proper accounting and disclosure",
        counter_arguments=[
            "Complex ownership structures may obscure related party relationships",
            "Beneficial ownership through trusts or nominees difficult to identify",
            "Side agreements may not be disclosed to accounting department",
        ],
        resolution_strategy="Annual management questionnaire; beneficial ownership database; audit committee pre-approval policy for related party transactions",
        entity_scope="All reporting entities",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 850 (SFAS 57), SEC Regulation S-K Item 404",
    ),
    DoctrineBlock(
        topic="Contingencies and Loss Accruals - ASC 450",
        keywords=["contingency", "contingent liability", "accrual", "asc 450", "probable", "reasonably possible"],
        conclusion_template=(
            "ASC 450 requires accrual of a loss contingency when it is probable that a "
            "liability has been incurred and the amount is reasonably estimable. If probable "
            "but not estimable, or reasonably possible, disclosure is required. Remote "
            "contingencies generally need not be disclosed except for guarantees."
        ),
        reasoning_framework=(
            "Loss contingency assessment: (1) Probable — likely to occur based on available "
            "information. Accrue if amount reasonably estimable; if range exists with no best "
            "estimate, accrue minimum of range. (2) Reasonably possible — more than remote but "
            "less than probable. Disclose nature and estimated range. (3) Remote — chance is "
            "slight. Generally no disclosure required. Gain contingencies: do not recognize "
            "until realized; may disclose if realization is probable. Litigation: accrue when "
            "unfavorable outcome probable and damages estimable; consider settlement offers, "
            "insurance recovery, and indemnification rights."
        ),
        key_factors=[
            "Probability assessment methodology (probable, reasonably possible, remote)",
            "Range estimation and best estimate within range",
            "Legal counsel assessment letters (SAS 12/AU-C 501)",
            "Insurance recovery recognition timing",
            "Litigation accrual disclosure without prejudicing legal position",
            "Environmental and product warranty reserves",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 450-20", title="Contingencies - Loss Contingencies", weight=1.0),
            AuthoritySource(codification="ASC 450-30", title="Contingencies - Gain Contingencies", weight=0.85),
        ],
        burden_holder="Reporting entity management and legal counsel",
        adversary_position="Plaintiffs may use financial statement accruals as evidence of liability acknowledgment",
        counter_arguments=[
            "Legal privilege concerns may limit disclosure detail",
            "Range estimation for early-stage litigation highly uncertain",
            "Insurance recovery offset timing may differ from loss recognition",
        ],
        resolution_strategy="Quarterly legal contingency assessment with outside counsel; document probability and estimation basis; coordinate disclosure with litigation counsel",
        entity_scope="All entities with loss contingencies",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 450 (SFAS 5)",
    ),
    DoctrineBlock(
        topic="Property Plant and Equipment - ASC 360",
        keywords=["ppe", "depreciation", "capitalization", "impairment", "useful life", "fixed assets", "asc 360"],
        conclusion_template=(
            "ASC 360 addresses recognition, measurement, depreciation, and impairment of "
            "long-lived assets. PP&E is measured at cost including directly attributable "
            "costs. Depreciation is allocated over useful life using straight-line, "
            "declining balance, or units of production. Impairment testing is triggered "
            "by events indicating carrying amount may not be recoverable."
        ),
        reasoning_framework=(
            "Capitalization criteria: Future economic benefit probable and cost reliably "
            "measurable. Include purchase price, installation, site preparation, professional "
            "fees. Capitalize improvements that extend useful life or add functionality; "
            "expense repairs and maintenance. Depreciation: systematic allocation over useful "
            "life. Common methods: straight-line, double-declining balance, sum-of-years, "
            "units of production. Component depreciation for significant parts with different "
            "lives. Impairment: Trigger events (significant decrease in market price, adverse "
            "change in use, operating losses). Step 1: Recoverability test — compare undiscounted "
            "future cash flows to carrying amount. Step 2: If not recoverable, measure impairment "
            "as excess of carrying amount over fair value."
        ),
        key_factors=[
            "Capitalization threshold policy setting",
            "Useful life determination and residual value estimation",
            "Component depreciation for complex assets",
            "Trigger event identification for impairment testing",
            "Asset grouping for recoverability testing",
            "Held-for-sale classification criteria and measurement",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 360-10", title="Property Plant and Equipment - Overall", weight=1.0),
            AuthoritySource(codification="ASC 360-10-35", title="PP&E - Subsequent Measurement (Impairment)", weight=0.95),
        ],
        burden_holder="Reporting entity",
        adversary_position="Auditors challenge useful life estimates and impairment trigger identification",
        counter_arguments=[
            "Capitalization vs expense decision can be judgmental for borderline costs",
            "Useful life estimates may not reflect actual asset utilization",
            "Undiscounted cash flow test creates high threshold for impairment recognition",
        ],
        resolution_strategy="Maintain fixed asset policy with clear capitalization thresholds; review useful lives annually; monitor trigger events systematically",
        entity_scope="Entities with significant PP&E",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 360 (SFAS 144, SFAS 143 for ARO)",
    ),
    DoctrineBlock(
        topic="Intangible Assets - ASC 350",
        keywords=["intangible", "amortization", "indefinite life", "software", "patent", "asc 350"],
        conclusion_template=(
            "ASC 350 addresses recognition and measurement of intangible assets. "
            "Finite-life intangibles are amortized over useful life and tested for impairment "
            "under ASC 360. Indefinite-life intangibles are not amortized but tested for "
            "impairment annually or upon triggering event. Internally developed intangibles "
            "are generally expensed except for software development costs."
        ),
        reasoning_framework=(
            "Recognition: Intangible assets acquired individually, in a group, or in a "
            "business combination measured at fair value. Internally generated: generally "
            "expensed as incurred (R&D per ASC 730). Exceptions: software development costs "
            "(ASC 985-20 for external-use software after technological feasibility; ASC 350-40 "
            "for internal-use software after preliminary project stage). Website development "
            "costs per ASC 350-50. Amortization: finite-life intangibles amortized over "
            "useful life reflecting pattern of benefit consumption. Indefinite-life: not "
            "amortized; reassess useful life each period."
        ),
        key_factors=[
            "Finite vs indefinite life determination",
            "Software development cost capitalization thresholds",
            "Amortization method and useful life estimation",
            "Impairment testing methodology for indefinite-life intangibles",
            "Customer relationship and technology asset valuation in acquisitions",
            "Patent and trademark renewal costs",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 350-30", title="Intangibles - General Intangibles Other Than Goodwill", weight=1.0),
            AuthoritySource(codification="ASC 350-40", title="Intangibles - Internal-Use Software", weight=0.9),
            AuthoritySource(codification="ASC 985-20", title="Software - Costs of Software to Be Sold", weight=0.85),
        ],
        burden_holder="Reporting entity",
        adversary_position="Auditors challenge useful life estimates and capitalization criteria for software",
        counter_arguments=[
            "Indefinite life assertion requires ongoing supportability",
            "Software capitalization scope boundary is judgmental",
            "Agile development methodology complicates stage identification",
        ],
        resolution_strategy="Document useful life basis with market and legal factors; maintain software development cost tracking system; reassess indefinite lives annually",
        entity_scope="Entities with intangible assets or software development",
        confidence=0.90,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 350 (SFAS 142), ASC 985-20, ASC 350-40",
    ),
    DoctrineBlock(
        topic="Earnings Per Share - ASC 260",
        keywords=["eps", "earnings per share", "diluted", "basic", "asc 260", "treasury stock method"],
        conclusion_template=(
            "ASC 260 requires dual presentation of basic and diluted EPS for public entities. "
            "Basic EPS = (Net Income - Preferred Dividends) / Weighted Average Common Shares. "
            "Diluted EPS includes the dilutive effect of stock options (treasury stock method), "
            "convertible instruments (if-converted method), and contingently issuable shares."
        ),
        reasoning_framework=(
            "Basic EPS: numerator = net income to common shareholders (deduct preferred dividends, "
            "including undeclared cumulative preferred). Denominator = weighted average common "
            "shares outstanding. Stock dividends and splits retroactively adjusted. "
            "Diluted EPS: Treasury stock method for options/warrants — assume exercise at "
            "beginning of period, use proceeds to buy back shares at average market price. "
            "If-converted method for convertible debt/preferred — add back interest/dividends "
            "to numerator, add converted shares to denominator. Anti-dilution test: each "
            "potentially dilutive security tested independently; anti-dilutive securities excluded. "
            "Two-class method required if participating securities exist (certain preferred stock, "
            "unvested restricted stock with non-forfeitable dividends)."
        ),
        key_factors=[
            "Weighted average share calculation with mid-period issuances",
            "Retroactive adjustment for stock splits and dividends",
            "Treasury stock method mechanics and average price determination",
            "If-converted method with interest add-back (net of tax)",
            "Anti-dilution sequencing (most dilutive first)",
            "Two-class method for participating securities",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 260-10", title="Earnings Per Share - Overall", weight=1.0),
        ],
        burden_holder="Public reporting entity",
        adversary_position="SEC scrutinizes complex EPS calculations, especially with convertible instruments post-ASU 2020-06",
        counter_arguments=[
            "Two-class method complexity for entities with multiple share classes",
            "Contingently issuable shares determination is judgmental",
            "Anti-dilution ordering can change EPS outcome materially",
        ],
        resolution_strategy="Maintain EPS model with automated anti-dilution testing; update for all share transactions; reconcile to share register",
        entity_scope="Public entities required to report EPS",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 260 (SFAS 128)",
    ),
    DoctrineBlock(
        topic="Accounting Changes and Error Corrections - ASC 250",
        keywords=["accounting change", "error correction", "restatement", "retrospective", "asc 250"],
        conclusion_template=(
            "ASC 250 requires retrospective application for changes in accounting principle "
            "(unless impracticable), prospective application for changes in estimate, and "
            "restatement of prior periods for error corrections. Changes in estimate effected "
            "by changes in principle are treated prospectively."
        ),
        reasoning_framework=(
            "Change in accounting principle: retrospective application to all prior periods "
            "presented. Adjust beginning retained earnings of earliest period. Disclose "
            "nature of change, reason, and effect on financial statements. Change in estimate: "
            "prospective application in period of change and future periods. No restatement. "
            "Examples: useful life revision, bad debt estimate, warranty reserve. Error "
            "correction: restate prior period financial statements. Disclose nature of error, "
            "effect on each period, and cumulative effect. Big R restatement (material error) "
            "requires amended filings. Little r revision (immaterial error) can be corrected "
            "in current period with revised comparative amounts."
        ),
        key_factors=[
            "Distinction between change in principle, estimate, and error",
            "Retrospective vs prospective application determination",
            "Materiality assessment for error correction approach",
            "SAB 99 and SAB 108 materiality frameworks",
            "Iron curtain vs rollover approach for quantifying errors",
            "Disclosure requirements for each type of change",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 250-10", title="Accounting Changes and Error Corrections", weight=1.0),
            AuthoritySource(codification="SEC SAB 99", title="Materiality", weight=0.9),
            AuthoritySource(codification="SEC SAB 108", title="Quantifying Misstatements", weight=0.9),
        ],
        burden_holder="Reporting entity management",
        adversary_position="SEC and auditors focus on whether errors are material and require restatement",
        counter_arguments=[
            "Impracticability exception for retrospective application subject to abuse",
            "Materiality judgment for Big R vs Little r is consequential",
            "Cumulative effect of immaterial errors may become material (SAB 108)",
        ],
        resolution_strategy="Maintain error tracking log with iron curtain and rollover quantification; document materiality conclusions with qualitative and quantitative analysis",
        entity_scope="All reporting entities",
        confidence=0.92,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 250 (SFAS 154), SEC SAB 99 and SAB 108",
    ),
    DoctrineBlock(
        topic="Consolidation Elimination Entries",
        keywords=["elimination", "intercompany", "consolidation entry", "unrealized profit", "upstream", "downstream"],
        conclusion_template=(
            "Consolidation requires elimination of all intercompany balances and transactions "
            "to present the consolidated entity as a single economic unit. Key eliminations "
            "include intercompany revenue/COGS, receivables/payables, investments/equity, "
            "and unrealized profits in inventory and fixed assets."
        ),
        reasoning_framework=(
            "Investment elimination: parent investment account against subsidiary equity "
            "accounts at acquisition-date values. Excess allocated to identifiable assets "
            "and goodwill. Intercompany transaction elimination: revenue and expense "
            "(parent sells to sub = downstream; sub sells to parent = upstream). "
            "Receivable/payable elimination. Unrealized profit in inventory: downstream "
            "100% eliminated against parent; upstream eliminated proportionally with NCI "
            "bearing share. Unrealized profit in fixed assets: eliminate gain and adjust "
            "depreciation over remaining life. Intercompany dividends eliminate against "
            "investment income. Intercompany debt: bonds held by affiliate eliminate with "
            "constructive retirement gain/loss."
        ),
        key_factors=[
            "Downstream vs upstream transaction NCI impact",
            "Unrealized profit elimination in ending vs beginning inventory",
            "Fixed asset unrealized profit and excess depreciation adjustment",
            "Intercompany loan and bond elimination",
            "Dividend elimination and investment income",
            "Multi-level consolidation (sub of sub) sequencing",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 810-10-45", title="Consolidation - Other Presentation Matters", weight=1.0),
        ],
        burden_holder="Parent entity preparing consolidated statements",
        adversary_position="Auditors test completeness of intercompany elimination and unrealized profit adjustments",
        counter_arguments=[
            "Complex organizational structures increase elimination complexity",
            "Timing differences between entities may leave unmatched intercompany balances",
            "Transfer pricing policies affect intercompany profit to eliminate",
        ],
        resolution_strategy="Maintain intercompany transaction matching system; reconcile balances monthly; automate standard elimination entries",
        entity_scope="Entities preparing consolidated financial statements",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 810 (ARB 51), consolidation accounting principles",
    ),
    DoctrineBlock(
        topic="Materiality Calculation Methodology",
        keywords=["materiality", "benchmark", "performance materiality", "trivial", "sad", "tolerable"],
        conclusion_template=(
            "Materiality determination uses a benchmark approach: select an appropriate base "
            "(net income, revenue, total assets, equity) and apply a percentage. Overall "
            "materiality is reduced to performance materiality (50-75%) to account for "
            "aggregation risk. Trivial threshold (3-5% of overall) sets the floor for "
            "accumulating misstatements."
        ),
        reasoning_framework=(
            "Benchmark selection factors: stability, relevance to users, entity lifecycle. "
            "Common benchmarks and ranges: Net income before tax 5-10% (stable earnings). "
            "Revenue 0.5-1% (pre-profit or volatile earnings). Total assets 0.5-1% (asset "
            "intensive). Equity 1-2% (financial institutions). Blended approach using multiple "
            "benchmarks for reasonableness check. Performance materiality: reduces overall "
            "materiality to manage detection risk (typically 50-75% of overall). Higher "
            "percentage when lower expected misstatements; lower when history of adjustments. "
            "Specific materiality: lower threshold for sensitive items (related party, "
            "management compensation, regulatory metrics). Clearly trivial: 3-5% of overall; "
            "misstatements below this need not be accumulated."
        ),
        key_factors=[
            "Benchmark selection aligned with primary user focus",
            "Percentage selection within range based on entity factors",
            "Performance materiality ratio to overall materiality",
            "Specific materiality for sensitive line items",
            "Clearly trivial threshold for accumulation",
            "Revision of materiality during audit for changed circumstances",
        ],
        primary_authority=[
            AuthoritySource(codification="PCAOB AS 2105", title="Consideration of Materiality", weight=1.0),
            AuthoritySource(codification="ISA 320", title="Materiality in Planning and Performing an Audit", weight=0.8),
        ],
        burden_holder="External auditor (audit materiality) and management (financial reporting materiality)",
        adversary_position="PCAOB inspection findings frequently cite inappropriate materiality determination",
        counter_arguments=[
            "Single benchmark may not capture all user perspectives",
            "Normalized vs reported income affects threshold calculation",
            "Qualitative factors may override quantitative materiality thresholds",
        ],
        resolution_strategy="Document benchmark selection rationale; calculate using multiple bases for reasonableness; reassess at conclusion of audit",
        entity_scope="Auditors and reporting entities",
        confidence=0.93,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="PCAOB AS 2105, SEC SAB 99, ISA 320",
    ),
    DoctrineBlock(
        topic="Deferred Tax Asset Valuation Allowance",
        keywords=["valuation allowance", "deferred tax asset", "dta", "realization", "more likely than not"],
        conclusion_template=(
            "A valuation allowance reduces deferred tax assets to the amount that is more "
            "likely than not (> 50%) to be realized. Assessment requires weighing all "
            "available positive and negative evidence, with objective evidence weighted "
            "more heavily than subjective evidence, especially cumulative losses."
        ),
        reasoning_framework=(
            "Positive evidence: existing taxable temporary differences reversing in same period, "
            "tax planning strategies that are prudent and feasible, projected future taxable "
            "income (excluding reversing temporary differences), history of tax NOL/credit "
            "utilization. Negative evidence: cumulative losses in recent years (strong negative), "
            "history of NOL/credit expiration, unsettled circumstances causing uncertainty, "
            "brief carryforward period. Cumulative loss in 3-year period creates presumption "
            "of full VA unless compelling positive evidence overcomes it. Sources of taxable "
            "income to realize DTAs: (1) future reversals of existing taxable temps, (2) future "
            "taxable income exclusive of reversals, (3) taxable income in carryback years, "
            "(4) tax planning strategies."
        ),
        key_factors=[
            "Three-year cumulative income/loss assessment",
            "Weight of objective vs subjective evidence",
            "Scheduling of temporary difference reversals",
            "Tax planning strategy identification and feasibility",
            "Carryforward period and expiration dates",
            "Jurisdictional analysis for multi-state/international",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 740-10-30", title="Income Taxes - Valuation Allowance", weight=1.0),
        ],
        burden_holder="Reporting entity tax department and management",
        adversary_position="SEC and auditors challenge insufficiency of VA when entity has cumulative losses",
        counter_arguments=[
            "Management projections may be unreliable for long forecast periods",
            "Tax planning strategies may not be executed in practice",
            "Economic downturns may invalidate historical realization patterns",
        ],
        resolution_strategy="Comprehensive VA memo with evidence weighting matrix; sensitivity analysis; quarterly reassessment with documentation of changes",
        entity_scope="Entities with net deferred tax assets",
        confidence=0.88,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 740-10-30 (SFAS 109 paragraphs 20-25)",
    ),
    DoctrineBlock(
        topic="Efficiency Ratio Analysis",
        keywords=["efficiency", "asset turnover", "inventory turnover", "receivable turnover", "dso", "dio"],
        conclusion_template=(
            "Efficiency ratios measure how effectively an entity utilizes its assets to "
            "generate revenue. Key metrics include total asset turnover, inventory turnover "
            "(and days inventory outstanding), receivable turnover (and days sales outstanding), "
            "and payable turnover (and days payable outstanding)."
        ),
        reasoning_framework=(
            "Total Asset Turnover = Revenue / Average Total Assets. Inventory Turnover = "
            "COGS / Average Inventory. Days Inventory Outstanding (DIO) = 365 / Inventory "
            "Turnover. Receivable Turnover = Net Credit Sales / Average Accounts Receivable. "
            "Days Sales Outstanding (DSO) = 365 / Receivable Turnover. Payable Turnover = "
            "COGS / Average Accounts Payable. Days Payable Outstanding (DPO) = 365 / Payable "
            "Turnover. Cash Conversion Cycle = DSO + DIO - DPO. Fixed Asset Turnover = "
            "Revenue / Average Net PP&E. Working Capital Turnover = Revenue / Average Working Capital."
        ),
        key_factors=[
            "Industry benchmarks for turnover comparison",
            "Seasonal effects on average balance calculations",
            "Revenue vs COGS as appropriate numerator",
            "Credit sales vs total sales for DSO calculation",
            "Cash conversion cycle optimization targets",
            "Trend analysis for deteriorating efficiency signals",
        ],
        primary_authority=[
            AuthoritySource(codification="CFA Institute", title="Financial Analysis Techniques", weight=0.7, binding=False),
        ],
        burden_holder="Management and financial analysts",
        adversary_position="Declining efficiency ratios may signal operational issues or growth challenges",
        counter_arguments=[
            "Asset-heavy investments temporarily depress turnover ratios",
            "Seasonal businesses require annualized or adjusted calculations",
            "Different revenue recognition methods affect comparability",
        ],
        resolution_strategy="Calculate monthly with rolling averages; segment by business unit; compare to industry peers and own historical trend",
        entity_scope="All entities",
        confidence=0.91,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Standard financial analysis framework",
    ),
    DoctrineBlock(
        topic="ASC 842 Lessor Accounting",
        keywords=["lessor", "sales-type", "direct financing", "operating lease", "lease receivable"],
        conclusion_template=(
            "Under ASC 842, lessors classify leases as sales-type, direct financing, or "
            "operating. Sales-type leases derecognize the asset and recognize a net investment; "
            "direct financing leases recognize a net investment without selling profit upfront; "
            "operating leases retain the asset and recognize rental income on a straight-line basis."
        ),
        reasoning_framework=(
            "Classification: If any of the five criteria from ASC 842-10-25-2 are met AND "
            "collectibility is probable, it is sales-type. If none of the five criteria are "
            "met but present value of lease payments plus residual value guarantee substantially "
            "equals fair value, it is direct financing. Otherwise, operating. "
            "Sales-type: derecognize asset, recognize net investment (lease receivable + "
            "unguaranteed residual asset), recognize selling profit/loss, interest income "
            "over lease term. Direct financing: recognize net investment, defer selling "
            "profit in net investment, interest income over term."
        ),
        key_factors=[
            "Five classification criteria application (same as lessee finance lease criteria)",
            "Collectibility assessment impact on classification",
            "Net investment in lease measurement",
            "Selling profit recognition timing",
            "Residual value guarantee and unguaranteed residual",
            "Variable lease payment treatment for lessor",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 842-30", title="Leases - Lessor", weight=1.0),
        ],
        burden_holder="Lessor entity",
        adversary_position="Auditors challenge classification and residual value assumptions",
        counter_arguments=[
            "Collectibility assessment may be overly optimistic",
            "Residual value estimates for long-term leases highly uncertain",
            "Subleasing arrangements complicate lessor accounting",
        ],
        resolution_strategy="Document classification analysis at lease inception; reassess residual values periodically; maintain lease portfolio analytics",
        entity_scope="Entities acting as lessors",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 842-30 (FASB ASU 2016-02)",
    ),
    DoctrineBlock(
        topic="Revenue from Contracts - Variable Consideration",
        keywords=["variable consideration", "constraint", "most likely amount", "expected value", "rebate", "discount"],
        conclusion_template=(
            "Variable consideration under ASC 606 is estimated using either the expected "
            "value (probability-weighted) or most likely amount method, whichever better "
            "predicts the amount of consideration. The estimate is constrained to amounts "
            "for which it is probable that a significant revenue reversal will not occur."
        ),
        reasoning_framework=(
            "Variable consideration forms: discounts, rebates, refunds, credits, price "
            "concessions, incentives, performance bonuses, penalties, returns. "
            "Expected value: sum of probability-weighted amounts (appropriate for large "
            "number of similar contracts). Most likely amount: single most likely outcome "
            "(appropriate for binary outcomes). Constraint factors: susceptibility to "
            "external factors, long resolution period, limited experience, broad price "
            "concession history, large number of possible amounts. Sales-based royalties "
            "on IP licenses: exception — recognize as subsequent sale occurs, not estimated."
        ),
        key_factors=[
            "Method selection (expected value vs most likely amount)",
            "Constraint application rigor",
            "Historical data availability for estimation",
            "Reassessment at each reporting period",
            "Sales-based royalty exception for IP licenses",
            "Volume discount and retrospective rebate estimation",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 606-10-32", title="Revenue - Determining the Transaction Price", weight=1.0),
        ],
        burden_holder="Reporting entity",
        adversary_position="SEC challenges insufficient constraint application leading to revenue overstatement",
        counter_arguments=[
            "Limited experience with new products makes estimation unreliable",
            "Customer concentration increases reversal risk",
            "Long performance periods increase estimation uncertainty",
        ],
        resolution_strategy="Document estimation methodology with historical support; apply constraint conservatively; reassess quarterly with actual vs estimate analysis",
        entity_scope="Entities with variable consideration in customer contracts",
        confidence=0.89,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 606-10-32 (FASB ASU 2014-09)",
    ),
    DoctrineBlock(
        topic="Asset Retirement Obligations - ASC 410",
        keywords=["aro", "asset retirement", "decommissioning", "remediation", "asc 410", "environmental"],
        conclusion_template=(
            "ASC 410-20 requires recognition of asset retirement obligations at fair value "
            "when incurred, with a corresponding increase to the carrying amount of the "
            "related long-lived asset. The liability is accreted to its settlement amount "
            "over time; the asset cost is depreciated over the asset's useful life."
        ),
        reasoning_framework=(
            "Recognition: Legal obligation to retire a tangible long-lived asset. Measured "
            "at fair value using expected present value technique (probability-weighted cash "
            "flows discounted at credit-adjusted risk-free rate). Asset retirement cost added "
            "to carrying amount of associated asset. Subsequent measurement: accretion expense "
            "recognized each period (beginning liability x credit-adjusted risk-free rate). "
            "Revisions to estimates: upward revisions discounted at current credit-adjusted "
            "risk-free rate; downward revisions at original rate. Environmental remediation "
            "obligations under ASC 410-30 recognized when probable and estimable."
        ),
        key_factors=[
            "Legal obligation identification (statutory, contractual, promissory estoppel)",
            "Fair value estimation using expected present value",
            "Credit-adjusted risk-free rate determination",
            "Revision methodology (upward vs downward estimates)",
            "Conditional ARO recognition timing",
            "Sufficient information to estimate vs inability to estimate",
        ],
        primary_authority=[
            AuthoritySource(codification="ASC 410-20", title="Asset Retirement Obligations", weight=1.0),
            AuthoritySource(codification="ASC 410-30", title="Environmental Obligations", weight=0.85),
        ],
        burden_holder="Entity with legal obligation to retire long-lived assets",
        adversary_position="EPA and auditors may challenge completeness and adequacy of ARO/environmental estimates",
        counter_arguments=[
            "Long time horizon increases estimation uncertainty",
            "Regulatory changes may alter decommissioning requirements",
            "Technology cost assumptions for remediation are speculative",
        ],
        resolution_strategy="Engage environmental engineers for cost estimates; update assumptions annually; maintain legal obligation inventory",
        entity_scope="Oil and gas, mining, utilities, entities with environmental obligations",
        confidence=0.87,
        confidence_stratification=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="ASC 410-20 (SFAS 143), ASC 410-30",
    ),
]

# ─── Build keyword index for fast lookup ──────────────────────────────────────
DOCTRINE_INDEX: Dict[str, List[int]] = {}
for _idx, _block in enumerate(DOCTRINE_CACHE):
    for _kw in _block.keywords:
        DOCTRINE_INDEX.setdefault(_kw.lower(), []).append(_idx)

logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks with {len(DOCTRINE_INDEX)} keyword entries")


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 6 — SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

TERM_NORMALIZATION: Dict[str, str] = {
    "p&l": "income statement",
    "profit and loss": "income statement",
    "bs": "balance sheet",
    "statement of financial position": "balance sheet",
    "scf": "statement of cash flows",
    "cash flow statement": "statement of cash flows",
    "gaap": "generally accepted accounting principles",
    "ifrs": "international financial reporting standards",
    "rou": "right-of-use asset",
    "pp&e": "property plant and equipment",
    "ppe": "property plant and equipment",
    "capex": "capital expenditure",
    "opex": "operating expenditure",
    "ebitda": "earnings before interest taxes depreciation amortization",
    "ebit": "earnings before interest and taxes",
    "eps": "earnings per share",
    "roe": "return on equity",
    "roa": "return on assets",
    "roic": "return on invested capital",
    "nol": "net operating loss",
    "dta": "deferred tax asset",
    "dtl": "deferred tax liability",
    "va": "valuation allowance",
    "aoci": "accumulated other comprehensive income",
    "oci": "other comprehensive income",
    "nci": "noncontrolling interest",
    "vie": "variable interest entity",
    "pbo": "projected benefit obligation",
    "eroa": "expected return on plan assets",
    "codm": "chief operating decision maker",
    "sox": "sarbanes-oxley",
    "coso": "committee of sponsoring organizations",
    "pcaob": "public company accounting oversight board",
    "sec": "securities and exchange commission",
    "fasb": "financial accounting standards board",
    "iasb": "international accounting standards board",
    "asc": "accounting standards codification",
    "asu": "accounting standards update",
    "dso": "days sales outstanding",
    "dio": "days inventory outstanding",
    "dpo": "days payable outstanding",
    "ccc": "cash conversion cycle",
    "fcf": "free cash flow",
    "wc": "working capital",
    "ap": "accounts payable",
    "ar": "accounts receivable",
    "sga": "selling general and administrative",
    "cogs": "cost of goods sold",
    "ibr": "incremental borrowing rate",
    "cecl": "current expected credit losses",
    "aro": "asset retirement obligation",
    "rsu": "restricted stock unit",
    "m&a": "mergers and acquisitions",
    "icfr": "internal controls over financial reporting",
}


def normalize_query(query: str) -> str:
    """Apply semantic normalization to standardize financial terminology."""
    normalized = query.lower()
    for abbrev, full_form in sorted(TERM_NORMALIZATION.items(), key=lambda x: -len(x[0])):
        normalized = normalized.replace(abbrev, full_form)
    return normalized


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 8 — TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Full query tracing, latency tracking, error domain analysis."""

    def __init__(self) -> None:
        self.events: List[TelemetryEvent] = []
        self.total_queries: int = 0
        self.cache_hits: int = 0
        self.total_latency_ms: float = 0.0
        self.errors: int = 0
        self.start_time: float = time.time()

    def record(self, event: TelemetryEvent) -> None:
        self.events.append(event)
        self.total_queries += 1
        self.total_latency_ms += event.latency_ms
        if event.cache_hit:
            self.cache_hits += 1
        if event.error:
            self.errors += 1
        if len(self.events) > 10000:
            self.events = self.events[-5000:]

    @property
    def cache_hit_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.cache_hits / self.total_queries

    @property
    def avg_latency_ms(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.total_latency_ms / self.total_queries

    @property
    def error_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.errors / self.total_queries

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time

    def snapshot(self) -> Dict[str, Any]:
        return {
            "total_queries": self.total_queries,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": round(self.cache_hit_rate, 4),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "errors": self.errors,
            "error_rate": round(self.error_rate, 4),
            "uptime_seconds": round(self.uptime_seconds, 2),
            "recent_events": len(self.events),
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 11 — METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Latency stats, error rates, hit rates, queries per hour."""

    def __init__(self) -> None:
        self.latencies: List[float] = []
        self.hourly_counts: Dict[str, int] = {}
        self.doctrine_hits: Dict[str, int] = {}

    def record_latency(self, ms: float) -> None:
        self.latencies.append(ms)
        if len(self.latencies) > 5000:
            self.latencies = self.latencies[-2500:]

    def record_query(self) -> None:
        hour_key = datetime.utcnow().strftime("%Y-%m-%d-%H")
        self.hourly_counts[hour_key] = self.hourly_counts.get(hour_key, 0) + 1

    def record_doctrine_hit(self, topic: str) -> None:
        self.doctrine_hits[topic] = self.doctrine_hits.get(topic, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        if not self.latencies:
            return {"p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "max_ms": 0, "queries_this_hour": 0}
        sorted_lat = sorted(self.latencies)
        p50 = sorted_lat[len(sorted_lat) // 2]
        p95 = sorted_lat[int(len(sorted_lat) * 0.95)]
        p99 = sorted_lat[int(len(sorted_lat) * 0.99)]
        hour_key = datetime.utcnow().strftime("%Y-%m-%d-%H")
        return {
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "max_ms": round(max(sorted_lat), 2),
            "queries_this_hour": self.hourly_counts.get(hour_key, 0),
            "top_doctrines": sorted(self.doctrine_hits.items(), key=lambda x: -x[1])[:10],
        }


METRICS = MetricsCollector()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 9 — DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift over time by tracking confidence distributions."""

    def __init__(self) -> None:
        self.confidence_history: List[Tuple[str, float, float]] = []
        self.topic_confidence: Dict[str, List[float]] = {}

    def record(self, topic: str, confidence: float) -> None:
        ts = time.time()
        self.confidence_history.append((topic, confidence, ts))
        self.topic_confidence.setdefault(topic, []).append(confidence)
        if len(self.confidence_history) > 10000:
            self.confidence_history = self.confidence_history[-5000:]

    def detect_drift(self, topic: str, window: int = 20) -> Optional[Dict[str, Any]]:
        history = self.topic_confidence.get(topic, [])
        if len(history) < window * 2:
            return None
        recent = history[-window:]
        prior = history[-window * 2 : -window]
        recent_avg = statistics.mean(recent)
        prior_avg = statistics.mean(prior)
        drift = recent_avg - prior_avg
        if abs(drift) > 0.05:
            return {
                "topic": topic,
                "drift": round(drift, 4),
                "direction": "improving" if drift > 0 else "degrading",
                "recent_avg": round(recent_avg, 4),
                "prior_avg": round(prior_avg, 4),
            }
        return None

    def summary(self) -> Dict[str, Any]:
        drifts = []
        for topic in self.topic_confidence:
            d = self.detect_drift(topic)
            if d:
                drifts.append(d)
        return {"active_drifts": drifts, "tracked_topics": len(self.topic_confidence)}


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 10 — COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════════

class CoverageMap:
    """Track triggered vs missed doctrines and epistemic gaps."""

    def __init__(self) -> None:
        self.triggered: Dict[str, int] = {}
        self.queries_without_match: int = 0
        self.total_queries: int = 0

    def record_hit(self, topics: List[str]) -> None:
        self.total_queries += 1
        if not topics:
            self.queries_without_match += 1
        for t in topics:
            self.triggered[t] = self.triggered.get(t, 0) + 1

    def get_coverage(self) -> Dict[str, Any]:
        all_topics = {b.topic for b in DOCTRINE_CACHE}
        triggered_topics = set(self.triggered.keys())
        untriggered = all_topics - triggered_topics
        return {
            "total_doctrines": len(all_topics),
            "triggered_doctrines": len(triggered_topics),
            "untriggered_doctrines": sorted(untriggered),
            "coverage_pct": round(len(triggered_topics) / max(len(all_topics), 1) * 100, 1),
            "queries_without_match": self.queries_without_match,
            "total_queries": self.total_queries,
            "gap_rate": round(self.queries_without_match / max(self.total_queries, 1) * 100, 1),
            "top_triggered": sorted(self.triggered.items(), key=lambda x: -x[1])[:10],
        }


COVERAGE = CoverageMap()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 14 — FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════════

def compute_fact_fragility(doctrine: DoctrineBlock) -> Dict[str, Any]:
    """Score the verifiability and recharacterization risk of a doctrine."""
    binding_count = sum(1 for a in doctrine.primary_authority if a.binding)
    total_authority = len(doctrine.primary_authority)
    authority_strength = binding_count / max(total_authority, 1)
    counter_arg_count = len(doctrine.counter_arguments)
    fragility_score = round(1.0 - (doctrine.confidence * 0.5 + authority_strength * 0.3 + (1 - min(counter_arg_count / 10, 1.0)) * 0.2), 4)
    return {
        "topic": doctrine.topic,
        "fragility_score": fragility_score,
        "confidence": doctrine.confidence,
        "authority_strength": round(authority_strength, 2),
        "counter_argument_density": counter_arg_count,
        "recharacterization_risk": "HIGH" if fragility_score > 0.4 else "MEDIUM" if fragility_score > 0.25 else "LOW",
        "testimony_dependence": "HIGH" if total_authority == 0 else "LOW" if binding_count >= 2 else "MEDIUM",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 16 — DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(query: str, answer: str, doctrines: List[str]) -> str:
    """SHA-256 hash for reproducibility verification."""
    content = json.dumps({"query": query, "answer": answer, "doctrines": sorted(doctrines)}, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 15 — AUDIT TRAIL (JSONL)
# ═══════════════════════════════════════════════════════════════════════════════

def write_audit_trail(query_id: str, query: str, response: QueryResponse) -> None:
    """Append every query to the audit trail for forensic review."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "query": query,
        "mode": response.mode.value,
        "zone": response.zone.value,
        "confidence": response.confidence,
        "doctrines": response.doctrine_topics_triggered,
        "hash": response.determinism_hash,
        "latency_ms": response.latency_ms,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Audit trail write failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 4 — AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY = {
    "ASC": 1.0,
    "PCAOB": 0.95,
    "SEC": 0.95,
    "FASB": 0.90,
    "AICPA": 0.80,
    "IFRS": 0.80,
    "IASB": 0.75,
    "COSO": 0.70,
    "IMA": 0.60,
    "CFA Institute": 0.55,
    "Industry Practice": 0.40,
}


def resolve_authority_conflicts(authorities: List[AuthoritySource]) -> List[AuthoritySource]:
    """Sort authorities by binding status and weight, resolving conflicts."""
    binding = [a for a in authorities if a.binding]
    non_binding = [a for a in authorities if not a.binding]
    binding.sort(key=lambda a: -a.weight)
    non_binding.sort(key=lambda a: -a.weight)
    return binding + non_binding


def get_authority_weight(codification: str) -> float:
    """Get hierarchical weight for an authority source."""
    for prefix, weight in AUTHORITY_HIERARCHY.items():
        if codification.upper().startswith(prefix.upper()):
            return weight
    return 0.5


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 5 — CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def stratify_confidence(confidence: float, zone: AnalysisZone) -> ConfidenceLevel:
    """Map confidence score to stratification level considering zone."""
    if zone == AnalysisZone.AUDIT:
        if confidence >= 0.90:
            return ConfidenceLevel.DEFENSIBLE
        elif confidence >= 0.75:
            return ConfidenceLevel.DISCLOSURE
        elif confidence >= 0.60:
            return ConfidenceLevel.AGGRESSIVE
        return ConfidenceLevel.HIGH_RISK
    elif zone == AnalysisZone.PLANNING:
        if confidence >= 0.80:
            return ConfidenceLevel.DEFENSIBLE
        elif confidence >= 0.65:
            return ConfidenceLevel.AGGRESSIVE
        elif confidence >= 0.50:
            return ConfidenceLevel.DISCLOSURE
        return ConfidenceLevel.HIGH_RISK
    else:
        if confidence >= 0.85:
            return ConfidenceLevel.DEFENSIBLE
        elif confidence >= 0.70:
            return ConfidenceLevel.AGGRESSIVE
        elif confidence >= 0.55:
            return ConfidenceLevel.DISCLOSURE
        return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 13 — ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

ZONE_INSTRUCTIONS = {
    AnalysisZone.PLANNING: "Present actionable recommendations with scenario analysis. Include forward-looking projections and risk factors.",
    AnalysisZone.REPORTING: "Present factual analysis with authoritative citations. Use precise financial terminology and quantitative support.",
    AnalysisZone.AUDIT: "Present audit-ready conclusions with full documentation trail. Cite specific standards and provide evidence-based reasoning.",
}


def get_zone_caveats(zone: AnalysisZone, confidence_level: ConfidenceLevel) -> List[str]:
    """Generate disclosure caveats appropriate for the analysis zone."""
    caveats: List[str] = []
    if confidence_level in (ConfidenceLevel.HIGH_RISK, ConfidenceLevel.AGGRESSIVE):
        caveats.append("This analysis involves significant judgment areas. Professional consultation recommended.")
    if zone == AnalysisZone.AUDIT:
        caveats.append("Audit conclusions should be supported by sufficient appropriate audit evidence.")
        if confidence_level != ConfidenceLevel.DEFENSIBLE:
            caveats.append("Additional substantive procedures may be warranted for this area.")
    if zone == AnalysisZone.PLANNING:
        caveats.append("Forward-looking assumptions are subject to change based on actual results.")
    if confidence_level == ConfidenceLevel.DISCLOSURE:
        caveats.append("Consider additional disclosure to ensure transparency with financial statement users.")
    return caveats


# ═══════════════════════════════════════════════════════════════════════════════
# FINANCIAL CALCULATION ENGINES
# ═══════════════════════════════════════════════════════════════════════════════

class RatioAnalyzer:
    """Compute and interpret financial ratios (TIE feature: ratio analysis)."""

    @staticmethod
    def current_ratio(current_assets: float, current_liabilities: float) -> RatioResult:
        value = current_assets / max(current_liabilities, 0.01)
        interpretation = "Strong liquidity position" if value > 2.0 else "Adequate liquidity" if value > 1.0 else "Potential liquidity concern — current liabilities exceed current assets"
        return RatioResult(name="Current Ratio", value=round(value, 4), benchmark=1.5, interpretation=interpretation, formula="Current Assets / Current Liabilities")

    @staticmethod
    def quick_ratio(cash: float, receivables: float, current_liabilities: float) -> RatioResult:
        value = (cash + receivables) / max(current_liabilities, 0.01)
        interpretation = "Strong quick liquidity" if value > 1.0 else "Marginal quick liquidity" if value > 0.5 else "Weak quick liquidity — may have difficulty meeting short-term obligations without liquidating inventory"
        return RatioResult(name="Quick Ratio", value=round(value, 4), benchmark=1.0, interpretation=interpretation, formula="(Cash + Receivables) / Current Liabilities")

    @staticmethod
    def debt_to_equity(total_debt: float, total_equity: float) -> RatioResult:
        value = total_debt / max(abs(total_equity), 0.01)
        interpretation = "Conservative capital structure" if value < 1.0 else "Moderate leverage" if value < 2.0 else "High leverage — elevated financial risk"
        return RatioResult(name="Debt-to-Equity", value=round(value, 4), benchmark=1.0, interpretation=interpretation, formula="Total Debt / Total Equity")

    @staticmethod
    def interest_coverage(ebit: float, interest_expense: float) -> RatioResult:
        value = ebit / max(abs(interest_expense), 0.01)
        interpretation = "Strong debt service capacity" if value > 5.0 else "Adequate coverage" if value > 2.0 else "Weak interest coverage — risk of debt service difficulty"
        return RatioResult(name="Interest Coverage", value=round(value, 4), benchmark=3.0, interpretation=interpretation, formula="EBIT / Interest Expense")

    @staticmethod
    def gross_margin(revenue: float, cogs: float) -> RatioResult:
        gp = revenue - cogs
        value = gp / max(revenue, 0.01)
        interpretation = "High gross margin indicating pricing power or cost efficiency" if value > 0.5 else "Moderate margin" if value > 0.25 else "Low gross margin — price or cost pressure"
        return RatioResult(name="Gross Margin", value=round(value, 4), benchmark=None, interpretation=interpretation, formula="(Revenue - COGS) / Revenue")

    @staticmethod
    def operating_margin(operating_income: float, revenue: float) -> RatioResult:
        value = operating_income / max(revenue, 0.01)
        interpretation = "Strong operating efficiency" if value > 0.20 else "Moderate operating margin" if value > 0.10 else "Low operating margin — high operating cost burden"
        return RatioResult(name="Operating Margin", value=round(value, 4), benchmark=None, interpretation=interpretation, formula="Operating Income / Revenue")

    @staticmethod
    def net_margin(net_income: float, revenue: float) -> RatioResult:
        value = net_income / max(revenue, 0.01)
        interpretation = "Strong bottom-line profitability" if value > 0.15 else "Moderate profitability" if value > 0.05 else "Low net margin"
        return RatioResult(name="Net Margin", value=round(value, 4), benchmark=None, interpretation=interpretation, formula="Net Income / Revenue")

    @staticmethod
    def return_on_assets(net_income: float, avg_total_assets: float) -> RatioResult:
        value = net_income / max(avg_total_assets, 0.01)
        interpretation = "Effective asset utilization" if value > 0.08 else "Moderate ROA" if value > 0.03 else "Low returns on asset base"
        return RatioResult(name="Return on Assets", value=round(value, 4), benchmark=0.05, interpretation=interpretation, formula="Net Income / Average Total Assets")

    @staticmethod
    def return_on_equity(net_income: float, avg_equity: float) -> RatioResult:
        value = net_income / max(abs(avg_equity), 0.01)
        interpretation = "Strong equity returns" if value > 0.15 else "Moderate ROE" if value > 0.08 else "Low equity returns"
        return RatioResult(name="Return on Equity", value=round(value, 4), benchmark=0.12, interpretation=interpretation, formula="Net Income / Average Shareholders Equity")

    @staticmethod
    def dupont_decomposition(net_income: float, revenue: float, avg_assets: float, avg_equity: float) -> Dict[str, Any]:
        npm = net_income / max(revenue, 0.01)
        at = revenue / max(avg_assets, 0.01)
        em = avg_assets / max(abs(avg_equity), 0.01)
        roe = npm * at * em
        return {
            "roe_decomposed": round(roe, 4),
            "net_profit_margin": round(npm, 4),
            "asset_turnover": round(at, 4),
            "equity_multiplier": round(em, 4),
            "driver_analysis": (
                f"ROE of {roe:.1%} driven by: Net Margin {npm:.1%} (operational efficiency) x "
                f"Asset Turnover {at:.2f}x (asset utilization) x Equity Multiplier {em:.2f}x (leverage)."
            ),
        }

    @staticmethod
    def altman_z_score(wc: float, re: float, ebit: float, mve: float, sales: float, ta: float, tl: float) -> Dict[str, Any]:
        ta_safe = max(ta, 0.01)
        tl_safe = max(tl, 0.01)
        x1 = wc / ta_safe
        x2 = re / ta_safe
        x3 = ebit / ta_safe
        x4 = mve / tl_safe
        x5 = sales / ta_safe
        z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
        if z > 2.99:
            zone = "SAFE"
            interpretation = "Low probability of bankruptcy within 1-2 years"
        elif z > 1.81:
            zone = "GREY"
            interpretation = "Moderate risk — further analysis recommended"
        else:
            zone = "DISTRESS"
            interpretation = "High probability of financial distress within 1-2 years"
        return {
            "z_score": round(z, 4),
            "zone": zone,
            "interpretation": interpretation,
            "components": {"X1_wc_ta": round(x1, 4), "X2_re_ta": round(x2, 4), "X3_ebit_ta": round(x3, 4), "X4_mve_tl": round(x4, 4), "X5_sales_ta": round(x5, 4)},
        }

    @staticmethod
    def inventory_turnover(cogs: float, avg_inventory: float) -> RatioResult:
        value = cogs / max(avg_inventory, 0.01)
        dio = 365 / max(value, 0.01)
        interpretation = f"Inventory turns {value:.1f}x annually ({dio:.0f} days). " + ("Efficient inventory management" if value > 8 else "Moderate turnover" if value > 4 else "Slow-moving inventory — review for obsolescence")
        return RatioResult(name="Inventory Turnover", value=round(value, 4), benchmark=6.0, interpretation=interpretation, formula="COGS / Average Inventory")

    @staticmethod
    def receivable_turnover(net_credit_sales: float, avg_receivables: float) -> RatioResult:
        value = net_credit_sales / max(avg_receivables, 0.01)
        dso = 365 / max(value, 0.01)
        interpretation = f"Receivables turn {value:.1f}x annually ({dso:.0f} days DSO). " + ("Fast collections" if dso < 30 else "Moderate collection cycle" if dso < 60 else "Slow collections — review credit terms and aging")
        return RatioResult(name="Receivable Turnover", value=round(value, 4), benchmark=8.0, interpretation=interpretation, formula="Net Credit Sales / Average Receivables")

    @staticmethod
    def cash_conversion_cycle(dso: float, dio: float, dpo: float) -> Dict[str, Any]:
        ccc = dso + dio - dpo
        return {
            "cash_conversion_cycle_days": round(ccc, 1),
            "dso": round(dso, 1),
            "dio": round(dio, 1),
            "dpo": round(dpo, 1),
            "interpretation": f"Cash conversion cycle of {ccc:.0f} days. " + ("Negative CCC indicates supplier-financed operations." if ccc < 0 else "Short CCC indicating efficient cash management." if ccc < 30 else "Moderate CCC." if ccc < 60 else "Long CCC — significant working capital investment required."),
        }


class VarianceAnalyzer:
    """Budget vs actual variance analysis (TIE feature)."""

    @staticmethod
    def compute_variance(actual: float, budget: float, line_item: str, favorable_when: str = "under") -> VarianceItem:
        variance = actual - budget
        variance_pct = (variance / max(abs(budget), 0.01)) * 100
        if favorable_when == "under":
            favorable = variance < 0
        else:
            favorable = variance > 0
        if abs(variance_pct) < 1:
            explanation = f"{line_item}: Immaterial variance of {variance_pct:.1f}% — within acceptable range."
        elif abs(variance_pct) < 5:
            explanation = f"{line_item}: Minor {'favorable' if favorable else 'unfavorable'} variance of {variance_pct:.1f}%. Monitor for recurring patterns."
        elif abs(variance_pct) < 10:
            explanation = f"{line_item}: Significant {'favorable' if favorable else 'unfavorable'} variance of {variance_pct:.1f}%. Root cause analysis recommended."
        else:
            explanation = f"{line_item}: Material {'favorable' if favorable else 'unfavorable'} variance of {variance_pct:.1f}%. Immediate management attention required."
        return VarianceItem(line_item=line_item, actual=actual, budget=budget, variance=round(variance, 2), variance_pct=round(variance_pct, 2), favorable=favorable, explanation=explanation)

    @staticmethod
    def flexible_budget_variance(actual: float, flex_budget: float, static_budget: float, line_item: str) -> Dict[str, Any]:
        flex_var = actual - flex_budget
        volume_var = flex_budget - static_budget
        total_var = actual - static_budget
        return {
            "line_item": line_item,
            "actual": actual,
            "flexible_budget": flex_budget,
            "static_budget": static_budget,
            "flexible_budget_variance": round(flex_var, 2),
            "volume_variance": round(volume_var, 2),
            "total_variance": round(total_var, 2),
            "analysis": f"Total variance of {total_var:,.0f} decomposes into volume variance of {volume_var:,.0f} (activity level) and flexible budget variance of {flex_var:,.0f} (rate/efficiency).",
        }


class MaterialityCalculator:
    """Materiality determination for audit and reporting purposes."""

    BENCHMARKS = {
        "net_income": (0.05, 0.10),
        "revenue": (0.005, 0.01),
        "total_assets": (0.005, 0.01),
        "equity": (0.01, 0.02),
        "gross_profit": (0.01, 0.03),
    }

    @staticmethod
    def calculate(benchmark_name: str, benchmark_value: float, risk_level: str = "normal") -> MaterialityResult:
        ranges = MaterialityCalculator.BENCHMARKS.get(benchmark_name, (0.01, 0.05))
        if risk_level == "high":
            pct = ranges[0]
        elif risk_level == "low":
            pct = ranges[1]
        else:
            pct = (ranges[0] + ranges[1]) / 2
        overall = abs(benchmark_value) * pct
        perf_mat_pct = 0.60 if risk_level == "high" else 0.75 if risk_level == "low" else 0.65
        performance = overall * perf_mat_pct
        trivial = overall * 0.04
        return MaterialityResult(
            overall_materiality=round(overall, 2),
            performance_materiality=round(performance, 2),
            trivial_threshold=round(trivial, 2),
            basis=f"{pct:.1%} of {benchmark_name}",
            benchmark_pct=pct,
        )


class DeferredTaxCalculator:
    """Book-tax difference and deferred tax computation."""

    @staticmethod
    def compute_deferred_tax(items: List[Dict[str, Any]], tax_rate: float = 0.21) -> Dict[str, Any]:
        results: List[DeferredTaxItem] = []
        total_dta = 0.0
        total_dtl = 0.0
        for item in items:
            book = item.get("book_amount", 0.0)
            tax = item.get("tax_amount", 0.0)
            desc = item.get("description", "Unknown")
            reversal = item.get("reversal_period", None)
            temp_diff = book - tax
            dta = abs(temp_diff) * tax_rate if temp_diff > 0 else 0.0
            dtl = abs(temp_diff) * tax_rate if temp_diff < 0 else 0.0
            total_dta += dta
            total_dtl += dtl
            results.append(DeferredTaxItem(description=desc, book_amount=book, tax_amount=tax, temporary_difference=round(temp_diff, 2), deferred_tax_asset=round(dta, 2), deferred_tax_liability=round(dtl, 2), reversal_period=reversal))
        net_position = total_dta - total_dtl
        return {
            "items": [r.model_dump() for r in results],
            "total_dta": round(total_dta, 2),
            "total_dtl": round(total_dtl, 2),
            "net_deferred_tax_position": round(net_position, 2),
            "net_classification": "Net DTA" if net_position > 0 else "Net DTL" if net_position < 0 else "Fully Offset",
            "tax_rate_applied": tax_rate,
        }


class ConsolidationEngine:
    """Multi-entity consolidation with intercompany elimination."""

    @staticmethod
    def eliminate_intercompany(parent_data: Dict[str, float], sub_data: Dict[str, float], intercompany: Dict[str, float]) -> Dict[str, Any]:
        consolidated: Dict[str, float] = {}
        all_keys = set(parent_data.keys()) | set(sub_data.keys())
        for key in all_keys:
            p_val = parent_data.get(key, 0.0)
            s_val = sub_data.get(key, 0.0)
            elim = intercompany.get(key, 0.0)
            consolidated[key] = round(p_val + s_val - elim, 2)
        return {
            "parent": parent_data,
            "subsidiary": sub_data,
            "eliminations": intercompany,
            "consolidated": consolidated,
        }

    @staticmethod
    def currency_translation(amounts: Dict[str, float], current_rate: float, avg_rate: float, historical_rate: float) -> Dict[str, Any]:
        bs_items = ["total_assets", "total_liabilities", "current_assets", "current_liabilities", "cash", "receivables", "inventory", "ppe_net", "goodwill", "intangibles"]
        is_items = ["revenue", "cogs", "operating_expenses", "interest_expense", "tax_expense", "net_income"]
        equity_items = ["common_stock", "apic", "retained_earnings_beginning"]
        translated: Dict[str, float] = {}
        for key, val in amounts.items():
            if key in bs_items:
                translated[key] = round(val * current_rate, 2)
            elif key in is_items:
                translated[key] = round(val * avg_rate, 2)
            elif key in equity_items:
                translated[key] = round(val * historical_rate, 2)
            else:
                translated[key] = round(val * current_rate, 2)
        translated_assets = sum(translated.get(k, 0) for k in bs_items if "asset" in k or k in ("cash", "receivables", "inventory", "ppe_net", "goodwill", "intangibles"))
        translated_liabilities = sum(translated.get(k, 0) for k in bs_items if "liabilit" in k)
        translated_equity = sum(translated.get(k, 0) for k in equity_items) + translated.get("net_income", 0)
        cta = round(translated_assets - translated_liabilities - translated_equity, 2)
        translated["cumulative_translation_adjustment"] = cta
        return {
            "original_amounts": amounts,
            "translated_amounts": translated,
            "rates_applied": {"current": current_rate, "average": avg_rate, "historical": historical_rate},
            "translation_adjustment": cta,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 7 — VECTOR / CLOUD RETRIEVER
# ═══════════════════════════════════════════════════════════════════════════════

async def cloud_retriever(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Semantic retrieval fallback via cloud vector search."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                "https://echo-swarm-brain.bmcii1976.workers.dev/api/search",
                json={"query": query, "domain": ENGINE_DOMAIN, "top_k": top_k},
            )
            if resp.status_code == 200:
                return resp.json().get("results", [])
    except Exception as e:
        logger.warning(f"Cloud retriever failed: {e}")
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 19 — MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════

def decompose_multi_doctrine(query: str, matched_doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    """Decompose query into issue categories, strata, and interaction DAG."""
    categories: Dict[str, List[str]] = {}
    for d in matched_doctrines:
        cat = "GENERAL"
        topic_lower = d.topic.lower()
        if any(kw in topic_lower for kw in ["revenue", "contract"]):
            cat = "REVENUE_RECOGNITION"
        elif any(kw in topic_lower for kw in ["lease", "rou"]):
            cat = "LEASE_ACCOUNTING"
        elif any(kw in topic_lower for kw in ["tax", "deferred"]):
            cat = "TAX_PROVISION"
        elif any(kw in topic_lower for kw in ["consolidat", "elimination", "vie"]):
            cat = "CONSOLIDATION"
        elif any(kw in topic_lower for kw in ["impairment", "goodwill"]):
            cat = "IMPAIRMENT"
        elif any(kw in topic_lower for kw in ["audit", "sox", "pcaob", "internal control", "materiality"]):
            cat = "AUDIT_COMPLIANCE"
        elif any(kw in topic_lower for kw in ["ratio", "dupont", "altman", "liquidity", "profitability", "leverage", "efficiency"]):
            cat = "FINANCIAL_ANALYSIS"
        elif any(kw in topic_lower for kw in ["currency", "translation"]):
            cat = "FOREIGN_CURRENCY"
        elif any(kw in topic_lower for kw in ["pension", "benefit"]):
            cat = "EMPLOYEE_BENEFITS"
        elif any(kw in topic_lower for kw in ["hedge", "derivative"]):
            cat = "FINANCIAL_INSTRUMENTS"
        categories.setdefault(cat, []).append(d.topic)

    interactions: List[Dict[str, str]] = []
    if "TAX_PROVISION" in categories and "REVENUE_RECOGNITION" in categories:
        interactions.append({"from": "REVENUE_RECOGNITION", "to": "TAX_PROVISION", "relationship": "Revenue timing differences create deferred tax items"})
    if "CONSOLIDATION" in categories and "FOREIGN_CURRENCY" in categories:
        interactions.append({"from": "FOREIGN_CURRENCY", "to": "CONSOLIDATION", "relationship": "Currency translation precedes consolidation eliminations"})
    if "IMPAIRMENT" in categories and "AUDIT_COMPLIANCE" in categories:
        interactions.append({"from": "IMPAIRMENT", "to": "AUDIT_COMPLIANCE", "relationship": "Impairment judgments require audit evidence documentation"})

    return {
        "issue_categories": categories,
        "category_count": len(categories),
        "doctrine_count": len(matched_doctrines),
        "interaction_dag": interactions,
        "complexity_rating": "HIGH" if len(categories) > 3 else "MEDIUM" if len(categories) > 1 else "LOW",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 1 — THREE-LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

def doctrine_lookup(query: str) -> List[DoctrineBlock]:
    """Layer 1: Doctrine cache lookup (0-200ms target)."""
    normalized = normalize_query(query)
    tokens = set(normalized.split())
    scores: Dict[int, float] = {}
    for token in tokens:
        for kw, indices in DOCTRINE_INDEX.items():
            if token in kw or kw in token:
                for idx in indices:
                    scores[idx] = scores.get(idx, 0) + 1.0
            elif len(token) > 4 and (token[:4] in kw or kw[:4] in token):
                for idx in indices:
                    scores[idx] = scores.get(idx, 0) + 0.3
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    threshold = 0.5
    matched = [DOCTRINE_CACHE[idx] for idx, score in ranked if score >= threshold]
    return matched[:8]


async def semantic_retrieval(query: str) -> List[Dict[str, Any]]:
    """Layer 2: Cloud-based semantic retrieval fallback."""
    return await cloud_retriever(query, top_k=5)


def deep_analysis(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
    """Layer 3: Deep analysis synthesizing multiple doctrines (TIE Component 20)."""
    if not doctrines:
        return (
            "No directly applicable doctrine found in the financial reporting knowledge base. "
            "This query may require specialized research beyond the current doctrine cache. "
            "Recommend consulting authoritative guidance (ASC, SEC releases) directly."
        )
    zone_instruction = ZONE_INSTRUCTIONS.get(zone, "")
    parts: List[str] = []
    if mode == ResponseMode.FAST:
        primary = doctrines[0]
        parts.append(primary.conclusion_template)
        if len(doctrines) > 1:
            parts.append(f"\nRelated considerations: {', '.join(d.topic for d in doctrines[1:3])}.")
    elif mode == ResponseMode.DEFENSE:
        for d in doctrines[:4]:
            parts.append(f"## {d.topic}")
            parts.append(d.conclusion_template)
            parts.append(f"\nKey Factors: {'; '.join(d.key_factors[:4])}")
            authorities = resolve_authority_conflicts(d.primary_authority)
            auth_str = "; ".join(f"{a.codification} ({a.title})" for a in authorities[:3])
            parts.append(f"Authority: {auth_str}")
            parts.append(f"Adversary Position: {d.adversary_position}")
            parts.append(f"Resolution: {d.resolution_strategy}")
            parts.append("")
    else:  # MEMO mode
        parts.append("# FINANCIAL REPORTING MEMORANDUM")
        parts.append(f"\nAnalysis Zone: {zone.value} | {zone_instruction}")
        parts.append(f"\nDoctrines Analyzed: {len(doctrines)}")
        for i, d in enumerate(doctrines[:6], 1):
            parts.append(f"\n## {i}. {d.topic}")
            parts.append(f"\n### Conclusion\n{d.conclusion_template}")
            parts.append(f"\n### Reasoning Framework\n{d.reasoning_framework}")
            parts.append(f"\n### Key Factors")
            for kf in d.key_factors:
                parts.append(f"- {kf}")
            authorities = resolve_authority_conflicts(d.primary_authority)
            parts.append(f"\n### Authorities Cited")
            for a in authorities:
                parts.append(f"- {a.codification}: {a.title} (weight: {a.weight}, binding: {a.binding})")
            parts.append(f"\n### Adversary Position\n{d.adversary_position}")
            parts.append(f"\n### Counter-Arguments")
            for ca in d.counter_arguments:
                parts.append(f"- {ca}")
            parts.append(f"\n### Resolution Strategy\n{d.resolution_strategy}")
            fragility = compute_fact_fragility(d)
            parts.append(f"\n### Fact Fragility: {fragility['recharacterization_risk']} (score: {fragility['fragility_score']})")
        decomposition = decompose_multi_doctrine(query, doctrines)
        parts.append(f"\n## Multi-Doctrine Decomposition")
        parts.append(f"Categories: {decomposition['category_count']} | Complexity: {decomposition['complexity_rating']}")
        for cat, topics in decomposition["issue_categories"].items():
            parts.append(f"- {cat}: {', '.join(topics)}")
        if decomposition["interaction_dag"]:
            parts.append("\n### Interaction DAG")
            for edge in decomposition["interaction_dag"]:
                parts.append(f"- {edge['from']} → {edge['to']}: {edge['relationship']}")

    return "\n".join(parts)


async def three_layer_response(request: QueryRequest) -> QueryResponse:
    """Execute the three-layer response pipeline."""
    start_time = time.time()
    query_id = str(uuid.uuid4())
    normalized = normalize_query(request.query)

    # Layer 1: Doctrine Cache
    cache_start = time.time()
    matched = doctrine_lookup(request.query)
    cache_ms = (time.time() - cache_start) * 1000
    cache_hit = len(matched) > 0

    # Layer 2: Cloud retrieval if no doctrine match
    cloud_results: List[Dict[str, Any]] = []
    if not matched:
        cloud_results = await semantic_retrieval(request.query)

    # Layer 3: Deep Analysis
    answer = deep_analysis(request.query, matched, request.mode, request.zone)

    if cloud_results and not matched:
        answer += "\n\n## Cloud Retrieval Supplements\n"
        for cr in cloud_results[:3]:
            answer += f"- {cr.get('title', 'Related')}: {cr.get('summary', 'N/A')}\n"

    # Compute confidence
    if matched:
        confidences = [d.confidence for d in matched]
        avg_conf = statistics.mean(confidences)
    else:
        avg_conf = 0.4 if cloud_results else 0.2

    strat = stratify_confidence(avg_conf, request.zone)
    caveats = get_zone_caveats(request.zone, strat)

    authorities_cited: List[str] = []
    for d in matched:
        for a in d.primary_authority:
            cite = f"{a.codification} - {a.title}"
            if cite not in authorities_cited:
                authorities_cited.append(cite)

    topics_triggered = [d.topic for d in matched]
    det_hash = compute_determinism_hash(request.query, answer, topics_triggered)
    latency_ms = (time.time() - start_time) * 1000

    # Telemetry
    event = TelemetryEvent(
        event_type="query",
        query_hash=hashlib.md5(request.query.encode()).hexdigest(),
        latency_ms=round(latency_ms, 2),
        cache_hit=cache_hit,
        doctrine_topics=topics_triggered,
    )
    TELEMETRY.record(event)
    METRICS.record_latency(latency_ms)
    METRICS.record_query()
    for t in topics_triggered:
        METRICS.record_doctrine_hit(t)
        DRIFT_WATCHER.record(t, avg_conf)
    COVERAGE.record_hit(topics_triggered)

    response = QueryResponse(
        query_id=query_id,
        mode=request.mode,
        zone=request.zone,
        answer=answer,
        confidence=round(avg_conf, 4),
        confidence_stratification=strat,
        authorities_cited=authorities_cited,
        doctrine_topics_triggered=topics_triggered,
        determinism_hash=det_hash,
        latency_ms=round(latency_ms, 2),
        disclosure_caveats=caveats,
    )

    write_audit_trail(query_id, request.query, response)
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 2 — RESPONSE MODES (FAST / DEFENSE / MEMO)
# ═══════════════════════════════════════════════════════════════════════════════
# Implemented within three_layer_response via the mode parameter routing
# FAST: concise conclusion only
# DEFENSE: audit-ready with authorities and adversary positions
# MEMO: full documentation memorandum format


# ═══════════════════════════════════════════════════════════════════════════════
# FINANCIAL STATEMENT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

class FinancialStatementGenerator:
    """Generate structured financial statements from trial balance data."""

    @staticmethod
    def income_statement(data: Dict[str, float]) -> Dict[str, Any]:
        revenue = data.get("revenue", 0)
        cogs = data.get("cogs", 0)
        gross_profit = revenue - cogs
        sga = data.get("sga", 0)
        rd = data.get("rd_expense", 0)
        depreciation = data.get("depreciation", 0)
        amortization = data.get("amortization", 0)
        other_operating = data.get("other_operating_expense", 0)
        total_opex = sga + rd + depreciation + amortization + other_operating
        operating_income = gross_profit - total_opex
        interest_income = data.get("interest_income", 0)
        interest_expense = data.get("interest_expense", 0)
        other_income = data.get("other_income", 0)
        ebt = operating_income + interest_income - interest_expense + other_income
        tax_expense = data.get("tax_expense", ebt * 0.21)
        net_income = ebt - tax_expense
        oci = data.get("other_comprehensive_income", 0)
        comprehensive_income = net_income + oci
        shares = data.get("weighted_avg_shares", 1)
        basic_eps = net_income / max(shares, 1)
        return {
            "title": "Consolidated Statement of Operations",
            "line_items": [
                FinancialStatementLine(account="Revenue", current_period=round(revenue, 2)).model_dump(),
                FinancialStatementLine(account="Cost of Goods Sold", current_period=round(cogs, 2)).model_dump(),
                FinancialStatementLine(account="Gross Profit", current_period=round(gross_profit, 2)).model_dump(),
                FinancialStatementLine(account="Selling, General & Administrative", current_period=round(sga, 2)).model_dump(),
                FinancialStatementLine(account="Research & Development", current_period=round(rd, 2)).model_dump(),
                FinancialStatementLine(account="Depreciation & Amortization", current_period=round(depreciation + amortization, 2)).model_dump(),
                FinancialStatementLine(account="Other Operating Expenses", current_period=round(other_operating, 2)).model_dump(),
                FinancialStatementLine(account="Total Operating Expenses", current_period=round(total_opex, 2)).model_dump(),
                FinancialStatementLine(account="Operating Income", current_period=round(operating_income, 2)).model_dump(),
                FinancialStatementLine(account="Interest Income", current_period=round(interest_income, 2)).model_dump(),
                FinancialStatementLine(account="Interest Expense", current_period=round(interest_expense, 2)).model_dump(),
                FinancialStatementLine(account="Other Income (Expense)", current_period=round(other_income, 2)).model_dump(),
                FinancialStatementLine(account="Income Before Tax", current_period=round(ebt, 2)).model_dump(),
                FinancialStatementLine(account="Income Tax Expense", current_period=round(tax_expense, 2)).model_dump(),
                FinancialStatementLine(account="Net Income", current_period=round(net_income, 2)).model_dump(),
                FinancialStatementLine(account="Other Comprehensive Income", current_period=round(oci, 2)).model_dump(),
                FinancialStatementLine(account="Comprehensive Income", current_period=round(comprehensive_income, 2)).model_dump(),
            ],
            "key_metrics": {
                "gross_margin": round(gross_profit / max(revenue, 0.01), 4),
                "operating_margin": round(operating_income / max(revenue, 0.01), 4),
                "net_margin": round(net_income / max(revenue, 0.01), 4),
                "effective_tax_rate": round(tax_expense / max(ebt, 0.01), 4),
                "basic_eps": round(basic_eps, 2),
            },
        }

    @staticmethod
    def balance_sheet(data: Dict[str, float]) -> Dict[str, Any]:
        cash = data.get("cash", 0)
        receivables = data.get("receivables", 0)
        inventory = data.get("inventory", 0)
        prepaid = data.get("prepaid_expenses", 0)
        other_current = data.get("other_current_assets", 0)
        total_current_assets = cash + receivables + inventory + prepaid + other_current
        ppe_net = data.get("ppe_net", 0)
        goodwill = data.get("goodwill", 0)
        intangibles = data.get("intangibles", 0)
        rou_assets = data.get("rou_assets", 0)
        lt_investments = data.get("lt_investments", 0)
        other_lt_assets = data.get("other_lt_assets", 0)
        total_lt_assets = ppe_net + goodwill + intangibles + rou_assets + lt_investments + other_lt_assets
        total_assets = total_current_assets + total_lt_assets
        ap = data.get("accounts_payable", 0)
        accrued = data.get("accrued_liabilities", 0)
        current_debt = data.get("current_debt", 0)
        deferred_rev_current = data.get("deferred_revenue_current", 0)
        other_current_liab = data.get("other_current_liabilities", 0)
        total_current_liab = ap + accrued + current_debt + deferred_rev_current + other_current_liab
        lt_debt = data.get("long_term_debt", 0)
        lease_liab = data.get("operating_lease_liability", 0)
        pension = data.get("pension_liability", 0)
        dtl = data.get("deferred_tax_liability", 0)
        other_lt_liab = data.get("other_lt_liabilities", 0)
        total_lt_liab = lt_debt + lease_liab + pension + dtl + other_lt_liab
        total_liab = total_current_liab + total_lt_liab
        common_stock = data.get("common_stock", 0)
        apic = data.get("apic", 0)
        retained_earnings = data.get("retained_earnings", 0)
        aoci = data.get("aoci", 0)
        treasury = data.get("treasury_stock", 0)
        total_equity = common_stock + apic + retained_earnings + aoci - treasury
        total_liab_equity = total_liab + total_equity
        return {
            "title": "Consolidated Balance Sheet",
            "assets": {
                "current_assets": {"cash": round(cash, 2), "receivables": round(receivables, 2), "inventory": round(inventory, 2), "prepaid_expenses": round(prepaid, 2), "other_current": round(other_current, 2), "total": round(total_current_assets, 2)},
                "non_current_assets": {"ppe_net": round(ppe_net, 2), "goodwill": round(goodwill, 2), "intangibles": round(intangibles, 2), "rou_assets": round(rou_assets, 2), "lt_investments": round(lt_investments, 2), "other": round(other_lt_assets, 2), "total": round(total_lt_assets, 2)},
                "total_assets": round(total_assets, 2),
            },
            "liabilities": {
                "current_liabilities": {"accounts_payable": round(ap, 2), "accrued_liabilities": round(accrued, 2), "current_debt": round(current_debt, 2), "deferred_revenue": round(deferred_rev_current, 2), "other_current": round(other_current_liab, 2), "total": round(total_current_liab, 2)},
                "non_current_liabilities": {"long_term_debt": round(lt_debt, 2), "operating_lease_liability": round(lease_liab, 2), "pension_liability": round(pension, 2), "deferred_tax_liability": round(dtl, 2), "other": round(other_lt_liab, 2), "total": round(total_lt_liab, 2)},
                "total_liabilities": round(total_liab, 2),
            },
            "equity": {"common_stock": round(common_stock, 2), "apic": round(apic, 2), "retained_earnings": round(retained_earnings, 2), "aoci": round(aoci, 2), "treasury_stock": round(treasury, 2), "total_equity": round(total_equity, 2)},
            "total_liabilities_and_equity": round(total_liab_equity, 2),
            "balances": round(total_assets - total_liab_equity, 2) == 0.0,
            "working_capital": round(total_current_assets - total_current_liab, 2),
        }

    @staticmethod
    def cash_flow_indirect(data: Dict[str, float]) -> Dict[str, Any]:
        net_income = data.get("net_income", 0)
        depreciation = data.get("depreciation", 0)
        amortization = data.get("amortization", 0)
        stock_comp = data.get("stock_compensation", 0)
        deferred_tax = data.get("deferred_tax_change", 0)
        ar_change = data.get("ar_change", 0)
        inv_change = data.get("inventory_change", 0)
        ap_change = data.get("ap_change", 0)
        accrued_change = data.get("accrued_change", 0)
        other_wc = data.get("other_working_capital_change", 0)
        operating_cf = net_income + depreciation + amortization + stock_comp + deferred_tax - ar_change - inv_change + ap_change + accrued_change + other_wc
        capex = data.get("capital_expenditures", 0)
        acquisitions = data.get("acquisitions", 0)
        investment_purchases = data.get("investment_purchases", 0)
        investment_sales = data.get("investment_sales", 0)
        investing_cf = -capex - acquisitions - investment_purchases + investment_sales
        debt_issued = data.get("debt_issued", 0)
        debt_repaid = data.get("debt_repaid", 0)
        equity_issued = data.get("equity_issued", 0)
        share_repurchases = data.get("share_repurchases", 0)
        dividends = data.get("dividends_paid", 0)
        financing_cf = debt_issued - debt_repaid + equity_issued - share_repurchases - dividends
        fx_effect = data.get("fx_effect", 0)
        net_change = operating_cf + investing_cf + financing_cf + fx_effect
        beginning_cash = data.get("beginning_cash", 0)
        ending_cash = beginning_cash + net_change
        fcf = operating_cf - capex
        return {
            "title": "Consolidated Statement of Cash Flows (Indirect Method)",
            "operating_activities": {
                "net_income": round(net_income, 2),
                "adjustments": {"depreciation": round(depreciation, 2), "amortization": round(amortization, 2), "stock_compensation": round(stock_comp, 2), "deferred_tax": round(deferred_tax, 2)},
                "working_capital_changes": {"accounts_receivable": round(-ar_change, 2), "inventory": round(-inv_change, 2), "accounts_payable": round(ap_change, 2), "accrued_liabilities": round(accrued_change, 2), "other": round(other_wc, 2)},
                "net_operating_cash_flow": round(operating_cf, 2),
            },
            "investing_activities": {"capital_expenditures": round(-capex, 2), "acquisitions": round(-acquisitions, 2), "investment_purchases": round(-investment_purchases, 2), "investment_sales": round(investment_sales, 2), "net_investing_cash_flow": round(investing_cf, 2)},
            "financing_activities": {"debt_issued": round(debt_issued, 2), "debt_repaid": round(-debt_repaid, 2), "equity_issued": round(equity_issued, 2), "share_repurchases": round(-share_repurchases, 2), "dividends_paid": round(-dividends, 2), "net_financing_cash_flow": round(financing_cf, 2)},
            "fx_effect": round(fx_effect, 2),
            "net_change_in_cash": round(net_change, 2),
            "beginning_cash": round(beginning_cash, 2),
            "ending_cash": round(ending_cash, 2),
            "free_cash_flow": round(fcf, 2),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 17 — FASTAPI SERVER
# ═══════════════════════════════════════════════════════════════════════════════

LAST_QUERY_AT: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    yield
    logger.info(f"Shutting down {ENGINE_NAME}")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant Financial Reporting Engine for accounting, financial statements, and compliance.",
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)


# ─── TIE COMPONENT 12 — HEALTH ENDPOINT ──────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        uptime_seconds=round(TELEMETRY.uptime_seconds, 2),
        total_queries=TELEMETRY.total_queries,
        cache_hit_rate=round(TELEMETRY.cache_hit_rate, 4),
        avg_latency_ms=round(TELEMETRY.avg_latency_ms, 2),
        doctrine_count=len(DOCTRINE_CACHE),
        last_query_at=LAST_QUERY_AT,
    )


@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest) -> QueryResponse:
    global LAST_QUERY_AT
    LAST_QUERY_AT = datetime.utcnow().isoformat()
    logger.info(f"Query received: mode={request.mode}, zone={request.zone}, len={len(request.query)}")
    response = await three_layer_response(request)
    logger.info(f"Query {response.query_id}: {response.latency_ms:.1f}ms, conf={response.confidence}, doctrines={len(response.doctrine_topics_triggered)}")
    return response


@app.post("/income-statement")
async def generate_income_statement(data: Dict[str, float]) -> JSONResponse:
    result = FinancialStatementGenerator.income_statement(data)
    return JSONResponse(content=result)


@app.post("/balance-sheet")
async def generate_balance_sheet(data: Dict[str, float]) -> JSONResponse:
    result = FinancialStatementGenerator.balance_sheet(data)
    return JSONResponse(content=result)


@app.post("/cash-flow")
async def generate_cash_flow(data: Dict[str, float]) -> JSONResponse:
    result = FinancialStatementGenerator.cash_flow_indirect(data)
    return JSONResponse(content=result)


@app.post("/ratios")
async def compute_ratios(data: Dict[str, float]) -> JSONResponse:
    results: Dict[str, Any] = {}
    ra = RatioAnalyzer
    if "current_assets" in data and "current_liabilities" in data:
        results["current_ratio"] = ra.current_ratio(data["current_assets"], data["current_liabilities"]).model_dump()
    if "cash" in data and "receivables" in data and "current_liabilities" in data:
        results["quick_ratio"] = ra.quick_ratio(data["cash"], data["receivables"], data["current_liabilities"]).model_dump()
    if "total_debt" in data and "total_equity" in data:
        results["debt_to_equity"] = ra.debt_to_equity(data["total_debt"], data["total_equity"]).model_dump()
    if "ebit" in data and "interest_expense" in data:
        results["interest_coverage"] = ra.interest_coverage(data["ebit"], data["interest_expense"]).model_dump()
    if "revenue" in data and "cogs" in data:
        results["gross_margin"] = ra.gross_margin(data["revenue"], data["cogs"]).model_dump()
    if "operating_income" in data and "revenue" in data:
        results["operating_margin"] = ra.operating_margin(data["operating_income"], data["revenue"]).model_dump()
    if "net_income" in data and "revenue" in data:
        results["net_margin"] = ra.net_margin(data["net_income"], data["revenue"]).model_dump()
    if "net_income" in data and "avg_total_assets" in data:
        results["roa"] = ra.return_on_assets(data["net_income"], data["avg_total_assets"]).model_dump()
    if "net_income" in data and "avg_equity" in data:
        results["roe"] = ra.return_on_equity(data["net_income"], data["avg_equity"]).model_dump()
    if all(k in data for k in ["net_income", "revenue", "avg_total_assets", "avg_equity"]):
        results["dupont"] = ra.dupont_decomposition(data["net_income"], data["revenue"], data["avg_total_assets"], data["avg_equity"])
    if "cogs" in data and "avg_inventory" in data:
        results["inventory_turnover"] = ra.inventory_turnover(data["cogs"], data["avg_inventory"]).model_dump()
    if "net_credit_sales" in data and "avg_receivables" in data:
        results["receivable_turnover"] = ra.receivable_turnover(data["net_credit_sales"], data["avg_receivables"]).model_dump()
    return JSONResponse(content=results)


@app.post("/altman-z-score")
async def compute_z_score(data: Dict[str, float]) -> JSONResponse:
    required = ["working_capital", "retained_earnings", "ebit", "market_value_equity", "sales", "total_assets", "total_liabilities"]
    missing = [k for k in required if k not in data]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {missing}")
    result = RatioAnalyzer.altman_z_score(
        wc=data["working_capital"], re=data["retained_earnings"], ebit=data["ebit"],
        mve=data["market_value_equity"], sales=data["sales"], ta=data["total_assets"], tl=data["total_liabilities"],
    )
    return JSONResponse(content=result)


@app.post("/variance-analysis")
async def variance_analysis(items: List[Dict[str, Any]]) -> JSONResponse:
    results = []
    for item in items:
        v = VarianceAnalyzer.compute_variance(
            actual=item.get("actual", 0),
            budget=item.get("budget", 0),
            line_item=item.get("line_item", "Unknown"),
            favorable_when=item.get("favorable_when", "under"),
        )
        results.append(v.model_dump())
    return JSONResponse(content={"variances": results, "total_items": len(results)})


@app.post("/materiality")
async def calculate_materiality(data: Dict[str, Any]) -> JSONResponse:
    result = MaterialityCalculator.calculate(
        benchmark_name=data.get("benchmark", "net_income"),
        benchmark_value=data.get("value", 0),
        risk_level=data.get("risk_level", "normal"),
    )
    return JSONResponse(content=result.model_dump())


@app.post("/deferred-tax")
async def compute_deferred_tax(data: Dict[str, Any]) -> JSONResponse:
    items = data.get("items", [])
    tax_rate = data.get("tax_rate", 0.21)
    result = DeferredTaxCalculator.compute_deferred_tax(items, tax_rate)
    return JSONResponse(content=result)


@app.post("/consolidation/eliminate")
async def consolidation_eliminate(data: Dict[str, Any]) -> JSONResponse:
    result = ConsolidationEngine.eliminate_intercompany(
        parent_data=data.get("parent", {}),
        sub_data=data.get("subsidiary", {}),
        intercompany=data.get("intercompany", {}),
    )
    return JSONResponse(content=result)


@app.post("/consolidation/translate")
async def consolidation_translate(data: Dict[str, Any]) -> JSONResponse:
    result = ConsolidationEngine.currency_translation(
        amounts=data.get("amounts", {}),
        current_rate=data.get("current_rate", 1.0),
        avg_rate=data.get("avg_rate", 1.0),
        historical_rate=data.get("historical_rate", 1.0),
    )
    return JSONResponse(content=result)


@app.get("/doctrines")
async def list_doctrines() -> JSONResponse:
    summaries = []
    for d in DOCTRINE_CACHE:
        summaries.append({
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "stratification": d.confidence_stratification.value,
            "authority_count": len(d.primary_authority),
            "entity_scope": d.entity_scope,
        })
    return JSONResponse(content={"doctrines": summaries, "total": len(summaries)})


@app.get("/doctrines/{index}")
async def get_doctrine(index: int) -> JSONResponse:
    if index < 0 or index >= len(DOCTRINE_CACHE):
        raise HTTPException(status_code=404, detail=f"Doctrine index {index} not found. Valid range: 0-{len(DOCTRINE_CACHE)-1}")
    d = DOCTRINE_CACHE[index]
    return JSONResponse(content={
        "topic": d.topic,
        "keywords": d.keywords,
        "conclusion": d.conclusion_template,
        "reasoning": d.reasoning_framework,
        "key_factors": d.key_factors,
        "authorities": [a.model_dump() for a in d.primary_authority],
        "burden_holder": d.burden_holder,
        "adversary_position": d.adversary_position,
        "counter_arguments": d.counter_arguments,
        "resolution_strategy": d.resolution_strategy,
        "confidence": d.confidence,
        "fragility": compute_fact_fragility(d),
    })


@app.get("/metrics")
async def get_metrics() -> JSONResponse:
    return JSONResponse(content={
        "telemetry": TELEMETRY.snapshot(),
        "latency_stats": METRICS.get_stats(),
        "coverage": COVERAGE.get_coverage(),
        "drift": DRIFT_WATCHER.summary(),
    })


@app.get("/coverage")
async def get_coverage() -> JSONResponse:
    return JSONResponse(content=COVERAGE.get_coverage())


@app.get("/drift")
async def get_drift() -> JSONResponse:
    return JSONResponse(content=DRIFT_WATCHER.summary())


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
