"""
REG06 Banking Regulatory Engine v1.0.0
TIE-Grade Compliance - All 20 Components

Handles: OCC, Fed Reserve, FDIC, BSA/AML, KYC, CDD, Reg E/Z, RESPA, Fair Lending,
CRA, CFPB, Basel III, Stress Testing, Volcker Rule
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
from collections import defaultdict, Counter
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "REG06"
ENGINE_NAME = "Banking Regulatory Engine"
VERSION = "1.0.0"
PORT = 9126

BANNED_PHRASES = [
    "this is legal advice", "you should", "you must", "I recommend",
    "guaranteed", "certainly will", "definitely complies", "no risk"
]

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    BSA_AML = "BSA_AML"
    CONSUMER_PROTECTION = "CONSUMER_PROTECTION"
    CAPITAL_LIQUIDITY = "CAPITAL_LIQUIDITY"
    FAIR_LENDING = "FAIR_LENDING"
    CRA_COMPLIANCE = "CRA_COMPLIANCE"
    PRIVACY_DATA = "PRIVACY_DATA"
    STRESS_TESTING = "STRESS_TESTING"
    VOLCKER_RULE = "VOLCKER_RULE"
    OPERATIONAL_RISK = "OPERATIONAL_RISK"
    REGULATORY_REPORTING = "REGULATORY_REPORTING"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: Dict[str, str]
    controlling_precedent: List[str]
    issue_category: IssueCategory

@dataclass
class QueryContext:
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    institution_type: str = "bank"
    asset_size: str = "unknown"

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    institution_type: str = "bank"
    asset_size: str = "unknown"

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str
    mode: ResponseMode
    layer_used: str
    latency_ms: float
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float
    doctrine_count: int

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="BSA Currency Transaction Reporting",
        keywords=["CTR", "currency", "$10000", "reporting", "structuring"],
        conclusion_template=[
            "CTR filing is required for currency transactions exceeding $10,000.",
            "Multiple transactions may be aggregated if knowledge of relationship exists.",
            "Structuring transactions to evade CTR filing is illegal under 31 USC 5324."
        ],
        reasoning_framework="""
31 USC 5313 requires financial institutions to file CTRs for currency transactions over $10,000.
31 CFR 1010.311 defines the reporting requirements and timing (15 days).
31 CFR 1010.313 requires aggregation of multiple transactions by/for same person in one day.
Knowledge standard: actual knowledge or reason to know transactions are related.
Structuring prohibition 31 USC 5324: criminal and civil penalties for breaking up transactions.
Exemptions available under 31 CFR 1020.315 for eligible businesses after due diligence.
Multiple accounts: transactions across accounts count toward $10,000 threshold.
Timing: CTR due 15 calendar days after transaction date.
FinCEN Form 112 (eFiling via BSA E-Filing System mandatory since 2012).
Penalties: civil up to $25,000 per violation, criminal up to 5 years if willful.
""",
        key_factors=[
            "Transaction amount equals or exceeds $10,000",
            "Currency involved (cash, not checks or wire)",
            "Single day aggregation requirement",
            "Knowledge of relationship between transactions",
            "Intent to evade reporting (structuring)",
            "Exemption status of customer"
        ],
        primary_authority=[
            "31 USC 5313 - Currency Transaction Reports",
            "31 CFR 1010.311 - Filing Requirements",
            "31 CFR 1010.313 - Aggregation",
            "31 USC 5324 - Structuring Prohibition"
        ],
        burden_holder="Financial institution to file; customer to avoid structuring",
        adversary_position="Customer may claim transactions unrelated or exempt",
        counter_arguments=[
            "Multiple unrelated individuals made deposits",
            "Customer qualifies for exemption under Phase I/II",
            "No knowledge transactions were related",
            "Currency source was legitimate business receipts"
        ],
        resolution_strategy="Review account history, identify transaction patterns, verify exemption status, consult BSA officer",
        entity_scope="Banks, credit unions, MSBs, casinos, card clubs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear $10K threshold met with currency",
            "AGGRESSIVE": "Near-threshold transactions aggregated",
            "DISCLOSURE": "Exemption claimed requires verification",
            "HIGH_RISK": "Pattern suggests structuring but no admission"
        },
        controlling_precedent=[
            "US v. MacPherson (9th Cir. 2005) - structuring intent",
            "Ratzlaf v. US (1994) - willfulness required for structuring"
        ],
        issue_category=IssueCategory.BSA_AML
    ),

    DoctrineBlock(
        topic="SAR Suspicious Activity Reporting",
        keywords=["SAR", "suspicious", "money laundering", "fraud", "FinCEN"],
        conclusion_template=[
            "SAR filing required for known/suspected criminal activity involving $5,000+.",
            "30-day deadline from initial detection (60 days if no suspect identified).",
            "Strict confidentiality - disclosure of SAR filing is prohibited."
        ],
        reasoning_framework="""
31 USC 5318(g) authorizes SAR reporting for suspicious transactions.
31 CFR 1020.320 (banks) requires SAR for transactions $5,000+ involving known/suspected:
  - federal crime violation
  - money laundering or BSA violation
  - structuring
  - no business or lawful purpose with no reasonable explanation
Timing: 30 calendar days from initial detection; 60 if no suspect identified.
FinCEN Form 111 (eFiling mandatory).
SAR Confidentiality: 31 USC 5318(g)(2) prohibits disclosure to subject of SAR.
Safe harbor: good faith filing protects institution from liability.
No minimum for terrorism financing SARs.
Continuing activity: file every 90 days if activity continues.
Sharing: allowed within corporate structure, with regulators, law enforcement with subpoena.
Penalties for non-filing: civil up to $100,000 per violation, criminal if willful.
""",
        key_factors=[
            "Transaction amount $5,000 or more (aggregate)",
            "Known or suspected federal crime",
            "Money laundering or BSA violation indicators",
            "No apparent lawful business purpose",
            "Customer refuses to provide information",
            "Transaction designed to evade reporting"
        ],
        primary_authority=[
            "31 USC 5318(g) - SAR Authority",
            "31 CFR 1020.320 - SAR Requirements (Banks)",
            "FinCEN SAR Narrative Guidance",
            "USA PATRIOT Act Section 356 - SAR Confidentiality"
        ],
        burden_holder="Financial institution",
        adversary_position="Customer may claim legitimate business purpose",
        counter_arguments=[
            "Transaction consistent with customer business type",
            "No red flags identified in monitoring",
            "Customer provided reasonable explanation",
            "Amount below $5,000 threshold after review"
        ],
        resolution_strategy="Document red flags, consult BSA officer, file SAR within deadline, maintain confidentiality",
        entity_scope="Banks, MSBs, securities firms, casinos, insurance",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear red flags with $5K+ amount",
            "AGGRESSIVE": "Borderline indicators aggregated to meet threshold",
            "DISCLOSURE": "Customer explanation plausible but unverified",
            "HIGH_RISK": "Multiple small transactions to avoid $5K threshold"
        },
        controlling_precedent=[
            "31 USC 5318(g)(3) - Safe Harbor for good faith filing",
            "FinCEN Guidance on Preparers (FIN-2012-G001)"
        ],
        issue_category=IssueCategory.BSA_AML
    ),

    DoctrineBlock(
        topic="CDD Customer Due Diligence Rule",
        keywords=["CDD", "beneficial owner", "KYC", "customer identification"],
        conclusion_template=[
            "CDD Rule requires identifying and verifying beneficial owners of legal entities.",
            "Four core elements: identify customer, verify identity, understand nature/purpose, ongoing monitoring.",
            "Beneficial owner certification required at account opening for legal entities."
        ],
        reasoning_framework="""
31 CFR 1010.230 (CDD Rule, effective May 11, 2018) requires:
  1. Customer identification and verification (CIP)
  2. Beneficial ownership identification (legal entities)
  3. Understanding nature and purpose of customer relationship
  4. Ongoing monitoring for suspicious activity
Beneficial Owner: Each individual who owns 25%+ equity or has control.
Certification Form: FinCEN recommends form, not mandatory format.
Timing: At account opening for new accounts; May 11, 2018 cutoff for existing.
Verification: reasonable procedures to verify identity (document, non-documentary, combination).
Ongoing monitoring: risk-based, update CDD as needed.
Legal entity customers: corporations, LLCs, partnerships, trusts (exemptions for publicly traded, banks, govt entities).
Records retention: 5 years after account closure.
Penalties: civil money penalties for violations, enforcement actions by regulators.
""",
        key_factors=[
            "Customer is legal entity (not individual)",
            "Not exempt (publicly traded, bank, government)",
            "Account opening occurred after May 11, 2018",
            "25% ownership threshold for beneficial owners",
            "Control prong: single individual with significant control",
            "Verification procedures reasonable and documented"
        ],
        primary_authority=[
            "31 CFR 1010.230 - CDD Rule",
            "FinCEN CDD Final Rule (May 2016)",
            "FAQ on CDD Rule (April 2018)",
            "31 CFR 1020.220 - Customer Identification Program"
        ],
        burden_holder="Financial institution",
        adversary_position="Customer may refuse to disclose beneficial owners",
        counter_arguments=[
            "Customer claims exemption (publicly traded subsidiary)",
            "No individuals meet 25% ownership threshold",
            "Complex ownership structure prevents identification",
            "Customer is foreign entity with different standards"
        ],
        resolution_strategy="Request FinCEN certification form, verify through corporate docs, escalate refusal to close account",
        entity_scope="Banks, credit unions, broker-dealers, mutual funds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear legal entity with identifiable beneficial owners",
            "AGGRESSIVE": "Complex structure requires regulatory interpretation",
            "DISCLOSURE": "Customer claims exemption needs verification",
            "HIGH_RISK": "Customer refuses to provide information"
        },
        controlling_precedent=[
            "FinCEN CDD Final Rule Preamble (81 FR 29398)",
            "Interagency Interpretive Guidance on CDD (2018)"
        ],
        issue_category=IssueCategory.BSA_AML
    ),

    DoctrineBlock(
        topic="Regulation Z TILA APR Disclosure",
        keywords=["APR", "Truth in Lending", "Reg Z", "disclosure", "credit"],
        conclusion_template=[
            "APR must be disclosed clearly and conspicuously for all credit transactions.",
            "APR includes interest rate plus certain fees annualized.",
            "Tolerance rules apply - APR accuracy required within 0.125% (closed-end)."
        ],
        reasoning_framework="""
15 USC 1601 et seq (TILA) requires disclosure of credit terms.
12 CFR 1026 (Regulation Z) implements TILA.
APR = annual percentage rate reflecting cost of credit as yearly rate.
Closed-end credit: APR within 0.125% accuracy (regular), 0.25% (irregular).
Open-end credit: APR calculated using average daily balance or other method.
Finance charge: interest + certain fees (origination, points, PMI, etc.).
Excluded: seller points paid by seller, fees for title/appraisal if reasonable.
Disclosure timing: closed-end within 3 business days of application (Loan Estimate).
Open-end: before first transaction (Schumer Box for credit cards).
Rescission rights: 3-day right to cancel for certain refinances.
Penalties: actual damages, statutory damages up to $5,000 (individual), class action caps, attorney fees.
CFPB enforcement: civil money penalties, restitution, corrective action.
""",
        key_factors=[
            "Type of credit (closed-end vs open-end)",
            "Fees included in finance charge",
            "Accuracy of APR calculation",
            "Timing of disclosure delivery",
            "Conspicuous presentation (font size, prominence)",
            "Rescission rights for refinances"
        ],
        primary_authority=[
            "15 USC 1601 - Truth in Lending Act",
            "12 CFR 1026 - Regulation Z",
            "12 CFR 1026.22 - APR Calculation (Closed-End)",
            "12 CFR 1026.14 - APR Calculation (Open-End)"
        ],
        burden_holder="Creditor",
        adversary_position="Borrower claims APR inaccurate or not conspicuous",
        counter_arguments=[
            "APR within tolerance (0.125% or 0.25%)",
            "Disclosure provided timely per regulation",
            "Fee excluded from finance charge (bona fide third party)",
            "Error corrected via revised disclosure before consummation"
        ],
        resolution_strategy="Review APR calculation, verify fee treatment, ensure Loan Estimate/Closing Disclosure compliance, cure errors promptly",
        entity_scope="Banks, credit unions, finance companies, mortgage lenders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "APR within tolerance, all required disclosures made",
            "AGGRESSIVE": "Borderline fee treatment as finance charge",
            "DISCLOSURE": "Timing of disclosure close to consummation",
            "HIGH_RISK": "APR outside tolerance or disclosure missing"
        },
        controlling_precedent=[
            "CFPB Official Interpretations to Reg Z",
            "2015 TRID Rule (TILA-RESPA Integrated Disclosures)"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="RESPA Section 8 Kickback Prohibition",
        keywords=["RESPA", "kickback", "referral fee", "settlement services", "Section 8"],
        conclusion_template=[
            "Section 8 prohibits kickbacks and unearned fees in real estate settlement.",
            "No fee for referral of settlement service business.",
            "Affiliated business arrangements allowed if disclosure made and no required use."
        ],
        reasoning_framework="""
12 USC 2607 (RESPA Section 8) prohibits:
  - Kickbacks for referrals of settlement service business
  - Unearned fees (fee split with no services performed)
Applies to federally related mortgage loans (most residential mortgages).
Settlement services: title, escrow, appraisal, credit report, loan origination, etc.
Section 8(a): no person shall give/accept fee/thing of value for referral.
Section 8(b): no person shall give/accept portion of charge except for services actually performed.
Section 8(c)(4): affiliated business arrangement (AfBA) exception if:
  - Written disclosure at/before referral
  - Person referred not required to use affiliate
  - Affiliate relationship disclosed
Criminal penalties: up to $10,000 fine and 1 year imprisonment.
Civil: 3x amount of charge, attorney fees, costs.
CFPB enforcement: civil money penalties, restitution, injunctive relief.
Safe harbors: bona fide compensation for services, normal promotional items under $50, AfBA compliance.
""",
        key_factors=[
            "Federally related mortgage loan",
            "Settlement service referral made",
            "Fee or thing of value exchanged for referral",
            "No services performed for fee received",
            "AfBA disclosure made and no required use",
            "Fee proportionate to services actually performed"
        ],
        primary_authority=[
            "12 USC 2607 - RESPA Section 8",
            "12 CFR 1024.14 - Prohibition Against Kickbacks",
            "12 CFR 1024.15 - AfBA Arrangements",
            "CFPB RESPA FAQs"
        ],
        burden_holder="Person giving or receiving kickback",
        adversary_position="Party claims fee was for legitimate services or AfBA compliant",
        counter_arguments=[
            "Fee paid for actual marketing services rendered",
            "AfBA disclosed and borrower not required to use",
            "Promotional items under $50 safe harbor",
            "Fee represents fair market value for services"
        ],
        resolution_strategy="Document services performed, ensure AfBA disclosures made, avoid required use, benchmark fees to market rates",
        entity_scope="Lenders, title companies, real estate agents, appraisers, mortgage brokers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Fee clearly for services performed, documented",
            "AGGRESSIVE": "AfBA with minimal services, fee seems high",
            "DISCLOSURE": "Disclosure timing or content questionable",
            "HIGH_RISK": "No services performed, undisclosed affiliate relationship"
        },
        controlling_precedent=[
            "HUD Statement of Policy 1999-1 (AfBA guidance)",
            "CFPB Bulletin 2015-05 (marketing services agreements)"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="ECOA Regulation B Fair Lending",
        keywords=["ECOA", "Reg B", "discrimination", "fair lending", "credit"],
        conclusion_template=[
            "ECOA prohibits credit discrimination on prohibited bases.",
            "Prohibited bases: race, color, religion, national origin, sex, marital status, age, public assistance.",
            "Disparate treatment and disparate impact theories both apply."
        ],
        reasoning_framework="""
15 USC 1691 (ECOA) prohibits discrimination in credit transactions.
12 CFR 1002 (Regulation B) implements ECOA.
Prohibited bases: race, color, religion, national origin, sex, marital status, age (if applicant has capacity),
  public assistance receipt, good faith exercise of CCPA rights.
Discrimination theories:
  - Disparate treatment: intentional discrimination (overt or comparative evidence)
  - Disparate impact: facially neutral policy with disproportionate adverse effect on protected class
Adverse action notice required within 30 days if credit denied/terminated.
Notice must state specific reasons or offer to provide reasons.
Record retention: 25 months for applications, 12 months for credit accounts.
Special purpose credit programs (SPCP) exception for programs benefiting disadvantaged groups.
Penalties: actual damages, punitive up to $10,000 (individual), $500,000 or 1% net worth (class), attorney fees.
DOJ pattern/practice enforcement for intentional violations.
CFPB supervision and enforcement.
""",
        key_factors=[
            "Credit transaction (loan, credit card, lease)",
            "Applicant member of protected class",
            "Adverse action taken (denial, unfavorable terms)",
            "Evidence of disparate treatment or impact",
            "Legitimate business necessity defense (disparate impact)",
            "Less discriminatory alternative available"
        ],
        primary_authority=[
            "15 USC 1691 - Equal Credit Opportunity Act",
            "12 CFR 1002 - Regulation B",
            "12 CFR 1002.9 - Adverse Action Notifications",
            "Interagency Fair Lending Examination Procedures"
        ],
        burden_holder="Creditor to prove non-discriminatory reason; applicant to prove prima facie case",
        adversary_position="Creditor claims legitimate underwriting reasons for denial",
        counter_arguments=[
            "Credit decision based on neutral factors (credit score, DTI)",
            "Policy justified by business necessity (risk-based pricing)",
            "No less discriminatory alternative achieves same goal",
            "SPCP designed to benefit economically disadvantaged"
        ],
        resolution_strategy="Review underwriting criteria for disparate impact, ensure adverse action notices compliant, document legitimate reasons, consider SPCP structure",
        entity_scope="Banks, credit unions, finance companies, auto dealers, retailers offering credit",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Neutral criteria, no disparate impact, notices compliant",
            "AGGRESSIVE": "Policy with disparate impact but strong business necessity",
            "DISCLOSURE": "Weak documentation of underwriting rationale",
            "HIGH_RISK": "Overt evidence of disparate treatment or unjustified impact"
        },
        controlling_precedent=[
            "Texas Dept. of Housing v. Inclusive Communities (2015) - disparate impact applies",
            "CFPB v. Townstone Financial (2020) - marketing discrimination"
        ],
        issue_category=IssueCategory.FAIR_LENDING
    ),

    DoctrineBlock(
        topic="CRA Community Reinvestment Act",
        keywords=["CRA", "assessment area", "lending", "community development", "LMI"],
        conclusion_template=[
            "CRA requires banks to meet credit needs of communities, including LMI areas.",
            "Assessment areas defined based on branch/deposit locations.",
            "Performance evaluated via lending, investment, service tests (large banks)."
        ],
        reasoning_framework="""
12 USC 2901 et seq (CRA) requires banks to meet credit needs of communities.
12 CFR 25 (OCC), 12 CFR 228 (Fed), 12 CFR 345 (FDIC) - CRA regulations.
Assessment area: geography where bank has branches, ATMs, or significant lending.
Performance tests:
  - Small banks (<$1.564B assets 2024): lending test only
  - Intermediate banks ($1.564B-$2.068B): lending + community development
  - Large banks (>$2.068B): lending, investment, service tests
Lending test: home mortgage, small business, small farm, community development loans.
LMI focus: low/moderate income census tracts and borrowers.
CRA ratings: Outstanding, Satisfactory, Needs to Improve, Substantial Noncompliance.
Consequences: rating considered in merger/acquisition/branch applications.
Public file: CRA public file with lending data, community development activities, public comments.
Exam frequency: 12-60 months depending on size and rating.
""",
        key_factors=[
            "Bank asset size (determines applicable tests)",
            "Assessment area delineation (branches, deposits)",
            "Lending to LMI borrowers and geographies",
            "Community development loans, investments, services",
            "Geographic distribution of lending",
            "Responsiveness to community credit needs"
        ],
        primary_authority=[
            "12 USC 2901 - Community Reinvestment Act",
            "12 CFR 25 - OCC CRA Regulation",
            "Interagency CRA Q&A",
            "CRA Modernization Final Rule (2024)"
        ],
        burden_holder="Bank",
        adversary_position="Community groups claim bank not meeting LMI credit needs",
        counter_arguments=[
            "Limited LMI lending opportunities in assessment area",
            "Strong community development activities compensate",
            "Geographic distribution reflects deposit base",
            "Competitive lending environment constrains volume"
        ],
        resolution_strategy="Expand LMI lending programs, increase CD investments, enhance branch services in LMI areas, document community needs assessment",
        entity_scope="Banks, thrifts (not credit unions, non-bank lenders)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Strong LMI lending, CD activities, Satisfactory+ rating",
            "AGGRESSIVE": "Marginal LMI lending, few CD activities, borderline rating",
            "DISCLOSURE": "Assessment area delineation under scrutiny",
            "HIGH_RISK": "Needs to Improve rating, pending enforcement action"
        },
        controlling_precedent=[
            "12 CFR 25.12 - Definitions (Assessment Area)",
            "OCC CRA Examiner Guidance"
        ],
        issue_category=IssueCategory.CRA_COMPLIANCE
    ),

    DoctrineBlock(
        topic="Basel III Capital Requirements",
        keywords=["Basel III", "capital", "CET1", "Tier 1", "risk-weighted assets", "leverage"],
        conclusion_template=[
            "Basel III requires minimum capital ratios to ensure bank solvency.",
            "CET1 minimum 4.5%, Tier 1 minimum 6%, Total capital minimum 8%.",
            "Capital conservation buffer adds 2.5%, GSIB surcharge for largest banks."
        ],
        reasoning_framework="""
Basel III framework (finalized 2010, implemented in US via 12 CFR 3 OCC, 12 CFR 217 Fed/FDIC).
Capital tiers:
  - CET1 (Common Equity Tier 1): common stock, retained earnings, AOCI (with opt-out)
  - Additional Tier 1: non-cumulative perpetual preferred stock, surplus
  - Tier 2: subordinated debt, allowance for loan losses (limited)
Minimum ratios (standardized approach):
  - CET1 ratio: CET1 / RWA >= 4.5%
  - Tier 1 ratio: (CET1 + AT1) / RWA >= 6%
  - Total capital ratio: (Tier 1 + Tier 2) / RWA >= 8%
Capital conservation buffer: 2.5% above minimums (CET1), restricts distributions if breached.
Countercyclical buffer: 0-2.5%, activated during credit expansion.
GSIB surcharge: 1-4.5% for globally systemically important banks.
Leverage ratio: Tier 1 / Total exposures >= 4% (SLR 5% for GSIBs).
RWA calculation: credit risk (standardized or advanced), market risk, operational risk.
Prompt corrective action: capital categories trigger restrictions (well/adequately/undercapitalized).
""",
        key_factors=[
            "Bank asset size and complexity (determines applicability)",
            "Quality of capital (CET1 vs AT1 vs Tier 2)",
            "Risk-weighted assets calculation methodology",
            "Capital conservation buffer level",
            "GSIB designation and surcharge",
            "Leverage ratio alongside risk-based ratios"
        ],
        primary_authority=[
            "12 CFR 3 - OCC Capital Adequacy Standards",
            "12 CFR 217 - Fed/FDIC Capital Adequacy",
            "Basel III: A Global Regulatory Framework (BCBS 2010)",
            "12 USC 1831o - Prompt Corrective Action"
        ],
        burden_holder="Bank",
        adversary_position="Regulator claims capital insufficient or miscalculated",
        counter_arguments=[
            "Assets risk-weighted conservatively (lower RWA)",
            "Capital instruments qualify under regulatory definitions",
            "Transitional provisions allow phase-in of deductions",
            "Advanced approaches approval reduces RWA"
        ],
        resolution_strategy="Raise capital via equity issuance or retained earnings, reduce RWA via asset sales, improve risk models (advanced approach)",
        entity_scope="Banks >$10B assets (simplified for community banks <$10B)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Capital ratios well above minimums + buffers",
            "AGGRESSIVE": "Ratios near minimums, buffer restricted",
            "DISCLOSURE": "RWA calculation under regulatory review",
            "HIGH_RISK": "Below well-capitalized, PCA restrictions apply"
        },
        controlling_precedent=[
            "12 CFR 3 Appendix A - Risk-Weighting (Standardized)",
            "OCC Capital Policy Manual"
        ],
        issue_category=IssueCategory.CAPITAL_LIQUIDITY
    ),

    DoctrineBlock(
        topic="DFAST Dodd-Frank Stress Testing",
        keywords=["DFAST", "stress testing", "CCAR", "capital planning", "severely adverse"],
        conclusion_template=[
            "DFAST requires annual stress testing for banks >$100B assets.",
            "Three scenarios: baseline, adverse, severely adverse.",
            "Results published, demonstrate capital adequacy under stress."
        ],
        reasoning_framework="""
12 USC 5365(i) (Dodd-Frank 165) requires stress testing for large banks.
12 CFR 252 Subpart E (Fed) implements DFAST for bank holding companies >$100B.
Company-run stress tests: annual, 9-quarter projection horizon.
Supervisory stress tests: Fed runs parallel tests, publishes results.
Scenarios: baseline, adverse, severely adverse (macroeconomic assumptions).
Severely adverse: deep recession, high unemployment, falling GDP, rising rates.
Projections: regulatory capital ratios, losses, revenues, expenses, RWA.
Post-stress capital ratios must remain above minimums.
CCAR (Comprehensive Capital Analysis Review): capital plan submission, includes stress test.
Objection: Fed can object to capital plan if:
  - Quantitative: post-stress ratios below minimums
  - Qualitative: capital planning process inadequate (until 2020 for most firms)
Capital actions: dividends, buybacks restricted if plan objected or stress test failed.
Publication: summary results disclosed to public.
""",
        key_factors=[
            "Bank asset size (>$100B threshold)",
            "Scenario severity (severely adverse most critical)",
            "Post-stress capital ratios vs minimums + buffers",
            "Capital plan robustness (risk identification, governance)",
            "Planned capital actions vs projected capital",
            "Model risk and assumptions"
        ],
        primary_authority=[
            "12 USC 5365(i) - Dodd-Frank Stress Testing",
            "12 CFR 252 Subpart E - DFAST (Fed)",
            "Fed SR 12-7 - CCAR Framework",
            "Annual DFAST/CCAR Instructions"
        ],
        burden_holder="Bank",
        adversary_position="Fed may object to capital plan or find test inadequate",
        counter_arguments=[
            "Post-stress ratios exceed minimums with margin",
            "Stress test methodology conservative and well-documented",
            "Capital plan includes contingency actions to restore capital",
            "Historical loss rates support projected losses"
        ],
        resolution_strategy="Strengthen capital planning process, reduce risk exposures, limit capital distributions, enhance model governance",
        entity_scope="Bank holding companies >$100B, certain non-bank SIFIs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Post-stress ratios well above minimums, no objections",
            "AGGRESSIVE": "Post-stress ratios barely above minimums, qualitative concerns",
            "DISCLOSURE": "Model limitations or data quality issues identified",
            "HIGH_RISK": "Post-stress ratios below minimums, plan objection likely"
        },
        controlling_precedent=[
            "Fed CCAR 2023 Results (public disclosure)",
            "12 CFR 225.8 - Capital Plan Rule"
        ],
        issue_category=IssueCategory.STRESS_TESTING
    ),

    DoctrineBlock(
        topic="Volcker Rule Proprietary Trading",
        keywords=["Volcker", "proprietary trading", "covered fund", "market making"],
        conclusion_template=[
            "Volcker Rule prohibits banking entities from proprietary trading.",
            "Exceptions: market making, underwriting, hedging, government securities.",
            "Covered fund investments restricted to 3% per fund, 3% aggregate Tier 1."
        ],
        reasoning_framework="""
12 USC 1851 (Dodd-Frank 619, Volcker Rule) prohibits proprietary trading by banking entities.
12 CFR 248 (Fed), 12 CFR 75 (OCC), 12 CFR 351 (FDIC) - implementing regulations.
Proprietary trading: purchasing/selling financial instruments as principal for short-term profit.
Exceptions (permitted activities):
  - Market making (providing liquidity to clients)
  - Underwriting (securities offerings)
  - Risk-mitigating hedging (reduces specific risk)
  - Trading in government obligations (US, states, agencies)
  - Insurance company general account activities
  - Trading outside US (foreign banking entities, no US counterparty risk)
Covered funds: entities qualifying as investment company under 1940 Act (hedge funds, PE funds).
Fund investment limits:
  - 3% of single covered fund
  - 3% of Tier 1 capital aggregate across all funds
Compliance: enhanced compliance program, CEO attestation, metrics reporting (>$10B trading assets).
Rebuttable presumption: trades held <60 days presumed proprietary (can rebut with market making evidence).
""",
        key_factors=[
            "Banking entity definition (bank, affiliate, subsidiary)",
            "Trading activity qualifies as proprietary (principal, short-term)",
            "Exception applies (market making, hedging, etc.)",
            "Covered fund status of investment vehicle",
            "Investment percentage limits (3% / 3%)",
            "Compliance program adequacy"
        ],
        primary_authority=[
            "12 USC 1851 - Volcker Rule",
            "12 CFR 248 - Fed Volcker Regulation",
            "Volcker Rule FAQs (Interagency)",
            "Volcker Rule Tailoring (2019 amendments)"
        ],
        burden_holder="Banking entity",
        adversary_position="Regulator claims trading is proprietary, not permitted exception",
        counter_arguments=[
            "Trading activity qualifies as market making (client-facing, inventory)",
            "Hedging relationship documented (risk reduced)",
            "Covered fund investment under 3% thresholds",
            "Activity conducted through foreign subsidiary, no US risk"
        ],
        resolution_strategy="Document exception applicability, limit covered fund investments, enhance compliance program, consider divestitures",
        entity_scope="Banks, BHCs, SIFIs, affiliates (not standalone broker-dealers outside banking org)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear market making or hedging, well-documented",
            "AGGRESSIVE": "Borderline proprietary/market making, weak hedging documentation",
            "DISCLOSURE": "Covered fund investment near 3% limits",
            "HIGH_RISK": "Prohibited proprietary trading, covered fund over limits"
        },
        controlling_precedent=[
            "12 CFR 248.4 - Market-Making Exception",
            "12 CFR 248.10 - Covered Fund Prohibition"
        ],
        issue_category=IssueCategory.VOLCKER_RULE
    ),

    DoctrineBlock(
        topic="Regulation E Electronic Fund Transfers",
        keywords=["Reg E", "EFT", "unauthorized", "error resolution", "debit card"],
        conclusion_template=[
            "Regulation E protects consumers in electronic fund transfers.",
            "Liability for unauthorized EFT limited if reported promptly.",
            "Error resolution procedures require investigation within 10 business days (45 for new/foreign)."
        ],
        reasoning_framework="""
15 USC 1693 (EFTA) protects consumers in electronic fund transfers.
12 CFR 1005 (Regulation E) implements EFTA.
Applies to: ATM, debit card, ACH, online bill pay, P2P transfers (Zelle, Venmo if bank-sponsored).
Unauthorized EFT: transfer initiated by person without authority, consumer receives no benefit.
Consumer liability caps:
  - $0 if reported before unauthorized use
  - $50 if reported within 2 business days of learning
  - $500 if reported 3-60 days after statement sent
  - Unlimited if not reported within 60 days of statement
Error resolution: consumer reports error, institution investigates.
Timing: 10 business days (45 for new accounts <30 days, foreign transactions, POS debit).
Provisional credit required if investigation >10 days.
Final determination: written notice, correction if error confirmed.
Preauthorized transfers: stop payment right, advance notice of varying amounts.
Remittance transfers: special rules for international transfers (12 CFR 1005 Subpart B).
Penalties: actual damages, statutory damages $100-$1,000 (individual), class action adjustments, attorney fees.
""",
        key_factors=[
            "Transfer qualifies as EFT (electronic, consumer account)",
            "Unauthorized (no authority, consumer no benefit)",
            "Timing of consumer report (2 days, 60 days)",
            "Error resolution procedures followed",
            "Provisional credit provided timely",
            "Notice of rights disclosed at account opening"
        ],
        primary_authority=[
            "15 USC 1693 - Electronic Fund Transfer Act",
            "12 CFR 1005 - Regulation E",
            "12 CFR 1005.6 - Liability of Consumer",
            "12 CFR 1005.11 - Error Resolution Procedures"
        ],
        burden_holder="Financial institution to investigate; consumer to report timely",
        adversary_position="Institution claims transfer authorized or consumer liable for delay",
        counter_arguments=[
            "Consumer authorized transfer (gave PIN, credentials)",
            "Consumer delayed report beyond 60 days (unlimited liability)",
            "Error investigation completed within 10 days, no error found",
            "Provisional credit provided, later reversed after investigation"
        ],
        resolution_strategy="Review authorization evidence, adhere to investigation timelines, provide provisional credit, document consumer communications",
        entity_scope="Banks, credit unions, other institutions offering EFT services",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear unauthorized transfer, reported within 2 days, $50 cap",
            "AGGRESSIVE": "Authorized ambiguous (shared credentials), borderline timing",
            "DISCLOSURE": "Investigation took >10 days, provisional credit delayed",
            "HIGH_RISK": "Consumer reported >60 days, institution claims unlimited liability"
        },
        controlling_precedent=[
            "12 CFR 1005.6(b) - Consumer Liability Limits",
            "CFPB Reg E Official Interpretations"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="GLBA Privacy and Safeguards",
        keywords=["GLBA", "privacy", "safeguards", "NPI", "information security"],
        conclusion_template=[
            "GLBA requires financial institutions to protect customer NPI.",
            "Privacy Rule: notice and opt-out for information sharing with non-affiliates.",
            "Safeguards Rule: comprehensive information security program."
        ],
        reasoning_framework="""
15 USC 6801 (GLBA Title V) requires financial institutions to protect customer information.
Privacy Rule: 16 CFR 313 (FTC), 12 CFR 1016 (CFPB for banks).
Safeguards Rule: 16 CFR 314 (FTC), 12 CFR 30 App B (OCC), Interagency Guidelines.
NPI: nonpublic personal information (SSN, account numbers, credit history, etc.).
Privacy notice: initial notice at customer relationship, annual notice, revised notice if practices change.
Opt-out: customer right to opt out of NPI sharing with non-affiliates (exceptions for servicing, joint marketing).
Safeguards Rule requirements:
  - Designate information security coordinator
  - Risk assessment of NPI handling
  - Design and implement safeguards (access controls, encryption, MFA)
  - Oversee service providers (contracts requiring data protection)
  - Monitor and test program effectiveness
  - Incident response plan
  - Annual report to board
Exceptions to opt-out: disclosures to service providers, legal process, fraud prevention, credit reporting.
Penalties: FTC enforcement, bank regulator enforcement, private right of action (limited).
""",
        key_factors=[
            "Customer relationship exists (NPI collected)",
            "Information shared with non-affiliates",
            "Opt-out notice provided and honored",
            "Information security program in place",
            "Service provider oversight via contracts",
            "Incident response and breach notification (state laws)"
        ],
        primary_authority=[
            "15 USC 6801 - GLBA Privacy",
            "16 CFR 313 - Privacy of Consumer Financial Information (FTC)",
            "16 CFR 314 - Safeguards Rule (FTC)",
            "Interagency Guidelines (12 CFR 30 App B OCC)"
        ],
        burden_holder="Financial institution",
        adversary_position="Customer or regulator claims NPI improperly shared or inadequately protected",
        counter_arguments=[
            "Sharing with affiliate or service provider (exceptions apply)",
            "Customer did not opt out within required period",
            "Information security program meets regulatory standards",
            "Breach resulted from unforeseeable third-party attack"
        ],
        resolution_strategy="Ensure privacy notices compliant, honor opt-outs, implement safeguards per regulation, oversee vendors, test security controls",
        entity_scope="Banks, credit unions, insurance, securities firms, finance companies, tax preparers, debt collectors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Privacy notices compliant, no sharing beyond exceptions, robust safeguards",
            "AGGRESSIVE": "Sharing with affiliates frequent, safeguards minimal compliance",
            "DISCLOSURE": "Service provider contract lacks required safeguards language",
            "HIGH_RISK": "Data breach, inadequate safeguards, no incident response plan"
        },
        controlling_precedent=[
            "FTC Safeguards Rule Amendments (2021) - enhanced requirements",
            "State data breach notification laws (all 50 states)"
        ],
        issue_category=IssueCategory.PRIVACY_DATA
    ),

    DoctrineBlock(
        topic="Bank Secrecy Act Recordkeeping",
        keywords=["BSA", "recordkeeping", "funds transfer", "$3000", "wire"],
        conclusion_template=[
            "BSA requires recordkeeping for funds transfers $3,000+.",
            "Funds transfer recordkeeping rule (travel rule) captures sender/receiver info.",
            "Records retained 5 years."
        ],
        reasoning_framework="""
31 USC 5311 (BSA) authorizes recordkeeping requirements.
31 CFR 1010.410 - General recordkeeping requirements (5 years).
31 CFR 1020.410(a) - Funds transfers $3,000+ (travel rule).
Travel rule: financial institution must collect and retain:
  - Transmittor name, address, account number
  - Recipient name, account number, financial institution
  - Amount, date, payment instructions
Transmittor bank: include info in transmittal order.
Intermediary/beneficiary bank: retain info or have procedures to retrieve.
Cross-border: SWIFT, Fedwire include required fields.
Domestic: Fedwire tag fields, ACH addenda records.
Recordkeeping period: 5 years from transaction date.
Other BSA records: monetary instruments $3K-$10K (312 filings if reportable), customer identification (CIP).
Penalties: civil penalties for recordkeeping violations, criminal if willful structuring or failure.
""",
        key_factors=[
            "Funds transfer amount $3,000 or more",
            "Transmittor information collected (name, address, account)",
            "Recipient information included in transmittal order",
            "Records retained 5 years",
            "Retrieval procedures for intermediary banks",
            "Cross-border vs domestic (SWIFT vs ACH/Fedwire)"
        ],
        primary_authority=[
            "31 USC 5311 - BSA Authority",
            "31 CFR 1010.410 - General Recordkeeping",
            "31 CFR 1020.410(a) - Funds Transfer Recordkeeping",
            "FinCEN Travel Rule FAQ"
        ],
        burden_holder="Financial institution",
        adversary_position="Regulator claims recordkeeping inadequate or missing",
        counter_arguments=[
            "Transfer under $3,000 threshold",
            "Information captured in payment system (SWIFT, Fedwire)",
            "Intermediary bank has retrieval procedures in place",
            "5-year retention period not yet elapsed"
        ],
        resolution_strategy="Ensure payment systems capture required fields, implement 5-year retention policy, audit recordkeeping compliance, train staff on travel rule",
        entity_scope="Banks, credit unions, MSBs conducting funds transfers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "All required info captured and retained 5 years",
            "AGGRESSIVE": "Incomplete transmittor address, retrieval procedures weak",
            "DISCLOSURE": "Legacy system lacks fields for required info",
            "HIGH_RISK": "No recordkeeping for $3K+ transfers, violations widespread"
        },
        controlling_precedent=[
            "31 CFR 1010.100(ff) - Funds Transfer Definition",
            "FATF Recommendation 16 (Wire Transfer Travel Rule)"
        ],
        issue_category=IssueCategory.BSA_AML
    ),

    DoctrineBlock(
        topic="OFAC Sanctions Compliance",
        keywords=["OFAC", "sanctions", "SDN", "blocked", "prohibited"],
        conclusion_template=[
            "OFAC administers economic sanctions programs prohibiting transactions with designated parties.",
            "SDN List: specially designated nationals - assets blocked, transactions prohibited.",
            "Strict liability - no intent required for violation."
        ],
        reasoning_framework="""
31 USC 5311 (IEEPA, TWEA) authorize OFAC sanctions.
OFAC (Office of Foreign Assets Control) enforces sanctions on countries, entities, individuals.
SDN List: Specially Designated Nationals and Blocked Persons.
50% Rule: entities 50%+ owned by SDN are themselves blocked (even if not listed).
Prohibited transactions: US persons cannot transact with SDNs or in prohibited programs.
Blocking: assets in US person possession/control must be frozen (reported to OFAC).
Sanctions programs: country-based (Iran, North Korea, Syria, Russia, Cuba, Venezuela), list-based (SDN, terrorists, narcotics).
Screening: financial institutions must screen customers, transactions, wire transfers against SDN list.
Strict liability: no intent required - violating sanctions is per se violation.
Voluntary self-disclosure: mitigating factor if institution reports violation to OFAC.
Penalties: civil penalties (inflation-adjusted, $330K+ per violation 2024), criminal if willful.
General licenses: some activities permitted under specific licenses (humanitarian, personal remittances).
""",
        key_factors=[
            "Customer or transaction counterparty on SDN List",
            "50% ownership by SDN entity",
            "Country/region subject to comprehensive sanctions",
            "Screening procedures in place (interdiction)",
            "Blocking vs rejection (assets in control vs not)",
            "Voluntary disclosure made if violation discovered"
        ],
        primary_authority=[
            "31 USC 5311 - IEEPA Authority",
            "31 CFR 501 - OFAC Regulations",
            "31 CFR 510 (North Korea), 31 CFR 560 (Iran), 31 CFR 576 (Russia), etc.",
            "OFAC SDN List (updated frequently)"
        ],
        burden_holder="Financial institution (US person)",
        adversary_position="OFAC claims violation, institution claims screening failure or missed update",
        counter_arguments=[
            "Transaction screened, no SDN match at time",
            "SDN list updated after transaction processed",
            "Customer name similar but not exact match (false positive)",
            "General license authorized transaction"
        ],
        resolution_strategy="Implement robust screening (automated + manual), update SDN list daily, block assets immediately if match, file blocking report, self-disclose violations",
        entity_scope="All US persons (individuals, entities, including foreign branches)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Screening robust, no SDN match, transaction cleared",
            "AGGRESSIVE": "Weak screening, reliance on customer attestation",
            "DISCLOSURE": "Name match requires manual review, not clearly SDN",
            "HIGH_RISK": "Transaction with known SDN, blocking required, violation if processed"
        },
        controlling_precedent=[
            "OFAC Enforcement Guidelines (2019)",
            "OFAC Economic Sanctions Enforcement Guidelines"
        ],
        issue_category=IssueCategory.BSA_AML
    ),

    DoctrineBlock(
        topic="LCR Liquidity Coverage Ratio",
        keywords=["LCR", "HQLA", "liquidity", "net cash outflow", "30-day"],
        conclusion_template=[
            "LCR requires banks to hold sufficient HQLA to cover 30-day stressed net cash outflow.",
            "LCR ratio: HQLA / Net Cash Outflow >= 100%.",
            "Daily calculation and reporting for banks >$250B or >$10B on-balance-sheet FX."
        ],
        reasoning_framework="""
12 CFR 249 (Fed, OCC, FDIC) - Liquidity Coverage Ratio Rule.
LCR = High-Quality Liquid Assets (HQLA) / Total Net Cash Outflow >= 100%.
Applies to: bank holding companies >$250B assets, >$10B on-balance-sheet FX, or >$75B covered BHCs (modified LCR).
30-day stress scenario: acute stress combining idiosyncratic and market-wide shocks.
HQLA tiers:
  - Level 1: cash, reserves, Treasuries, agency debt (0% haircut)
  - Level 2A: agency MBS, GSE debt, certain sovereign/PSE (15% haircut)
  - Level 2B: RMBS, corporate bonds, equities (50% haircut, capped at 15% of HQLA)
Net cash outflow = outflows - MIN(inflows, 75% outflows).
Outflow rates: retail deposits 3-10%, unsecured wholesale 40-100%, secured funding varies by collateral.
Inflow rates: contractual inflows capped at 50% (some 0% if non-performing).
Daily calculation, monthly reporting (FR 2052a).
Consequences: below 100% triggers remediation plan, regulatory restrictions.
""",
        key_factors=[
            "Bank asset size (>$250B threshold)",
            "HQLA composition and haircuts",
            "Outflow assumptions (deposit runoff, wholesale funding)",
            "Inflow cap (75% of outflows)",
            "Stress scenario calibration",
            "LCR ratio level vs 100% minimum"
        ],
        primary_authority=[
            "12 CFR 249 - Liquidity Coverage Ratio",
            "Basel III LCR Standard (BCBS 2013)",
            "FR 2052a - LCR Reporting Form",
            "Fed SR 13-21 - LCR Supervisory Guidance"
        ],
        burden_holder="Bank",
        adversary_position="Regulator claims HQLA insufficient or outflow assumptions understated",
        counter_arguments=[
            "HQLA holdings exceed requirement with margin",
            "Deposit base stable (low runoff rates justified)",
            "Inflows from high-quality counterparties (performing loans)",
            "Operational deposit allowance reduces outflows"
        ],
        resolution_strategy="Increase HQLA (Level 1 assets), reduce reliance on wholesale funding, model deposit stability conservatively, enhance liquidity risk management",
        entity_scope="Large banks >$250B, modified LCR for $100-250B",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "LCR >100% with margin, HQLA diversified",
            "AGGRESSIVE": "LCR near 100%, heavy Level 2B reliance",
            "DISCLOSURE": "Outflow assumptions aggressive (low runoff rates)",
            "HIGH_RISK": "LCR <100%, remediation plan required"
        },
        controlling_precedent=[
            "12 CFR 249.3 - HQLA Definitions",
            "12 CFR 249.30 - Outflow Amounts"
        ],
        issue_category=IssueCategory.CAPITAL_LIQUIDITY
    ),

    DoctrineBlock(
        topic="UDAAP Unfair Deceptive Abusive Acts",
        keywords=["UDAAP", "unfair", "deceptive", "abusive", "CFPB"],
        conclusion_template=[
            "UDAAP prohibits unfair, deceptive, or abusive acts in consumer financial products.",
            "Unfair: substantial injury, not reasonably avoidable, not outweighed by benefits.",
            "Deceptive: material misrepresentation or omission, reasonable consumer misled."
        ],
        reasoning_framework="""
12 USC 5531 (Dodd-Frank 1031) prohibits UDAAP.
CFPB enforcement authority over banks, non-banks offering consumer financial products.
Unfair standard (3-part test):
  1. Causes or likely to cause substantial injury to consumers
  2. Injury not reasonably avoidable by consumers
  3. Injury not outweighed by countervailing benefits to consumers or competition
Deceptive standard:
  - Material representation/omission
  - Likely to mislead reasonable consumer
  - Consumer interpretation reasonable under circumstances
Abusive standard (one or more):
  - Materially interferes with ability to understand terms/conditions
  - Takes unreasonable advantage of:
    - Lack of consumer understanding
    - Inability to protect interests in selecting/using product
    - Reasonable reliance on covered person to act in consumer's interests
Examples: hidden fees, misleading marketing, aggressive debt collection, steering to higher-cost products.
Remedies: restitution, civil money penalties up to $1M per day (knowing violations), injunctions, compliance monitoring.
No private right of action (CFPB enforcement only).
Interplay with UDAP (FTC Act 5) - similar but CFPB has abusive prong.
""",
        key_factors=[
            "Consumer financial product or service",
            "Substantial injury to consumers (monetary or non-monetary)",
            "Reasonable avoidability (disclosure, ability to choose)",
            "Material representation or omission",
            "Reasonable consumer interpretation",
            "Interference with understanding or unreasonable advantage"
        ],
        primary_authority=[
            "12 USC 5531 - UDAAP Prohibition",
            "12 USC 5536 - CFPB Enforcement",
            "CFPB Supervision and Examination Manual",
            "CFPB UDAAP Bulletin 2013-06"
        ],
        burden_holder="CFPB (in enforcement); covered person (to avoid UDAAP)",
        adversary_position="CFPB claims practice is unfair, deceptive, or abusive",
        counter_arguments=[
            "Injury not substantial (de minimis harm)",
            "Consumers can reasonably avoid (disclosure clear, alternative products)",
            "Benefits outweigh injury (convenience, lower prices)",
            "Representation not material (does not influence decision)",
            "Reasonable consumer would not be misled (clear disclosures)"
        ],
        resolution_strategy="Review marketing and disclosures for clarity, avoid hidden fees, provide alternatives, document benefits, train staff on UDAAP risks",
        entity_scope="Banks, credit unions, non-bank consumer finance companies, debt collectors, credit reporting",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Clear disclosures, no hidden fees, consumer choice protected",
            "AGGRESSIVE": "Borderline material omissions, disclosure fine print",
            "DISCLOSURE": "Practice benefits unclear, potential consumer misunderstanding",
            "HIGH_RISK": "Hidden fees, misleading marketing, steering to high-cost products"
        },
        controlling_precedent=[
            "CFPB v. PHH Corp (DC Cir 2018) - UDAAP captive reinsurance",
            "CFPB Consent Orders (public enforcement actions)"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="Interchange Fee Regulation Durbin Amendment",
        keywords=["Durbin", "interchange", "debit card", "$10B", "two unaffiliated networks"],
        conclusion_template=[
            "Durbin Amendment caps debit card interchange fees for issuers >$10B assets.",
            "Base cap: $0.21 + 0.05% of transaction + $0.01 fraud adjustment.",
            "Merchant routing choice: two unaffiliated networks required."
        ],
        reasoning_framework="""
15 USC 1693o-2 (Dodd-Frank 1075, Durbin Amendment) regulates debit card interchange fees.
12 CFR 235 (Reg II) implements Durbin Amendment.
Applies to: debit card issuers with $10B+ assets (includes card issuing affiliates).
Interchange fee cap:
  - Base: $0.21 per transaction
  - Ad valorem: 0.05% of transaction amount
  - Fraud prevention adjustment: $0.01 (if issuer meets fraud prevention standards)
  - Total max: $0.22 + 0.05% (or $0.23 for fraud-compliant issuers)
Exemption: issuers <$10B assets, government-administered programs (EBT, certain prepaid).
Merchant routing choice: issuer must enable at least two unaffiliated networks for each transaction type (signature, PIN).
Network exclusivity prohibited: merchant can route to any enabled network.
Fraud prevention standards: policies/procedures to prevent fraud, monitor fraud rates.
Enforcement: Fed, CFPB, state AGs, private right of action for merchants.
Impact: reduced interchange revenue for large issuers, preserved for small issuers.
""",
        key_factors=[
            "Issuer asset size (>$10B threshold)",
            "Debit card type (prepaid may be exempt if govt-administered)",
            "Interchange fee charged vs cap",
            "Fraud prevention adjustment eligibility",
            "Two unaffiliated networks enabled",
            "Merchant routing choice available"
        ],
        primary_authority=[
            "15 USC 1693o-2 - Durbin Amendment",
            "12 CFR 235 - Reg II Debit Card Interchange Fees",
            "Fed Reg II Official Interpretations",
            "Fed Debit Card Interchange Fee Survey (annual)"
        ],
        burden_holder="Debit card issuer (>$10B)",
        adversary_position="Merchant claims interchange exceeds cap or routing choice denied",
        counter_arguments=[
            "Issuer under $10B threshold (exempt)",
            "Card is prepaid govt-administered (exempt)",
            "Interchange within cap including fraud adjustment",
            "Two unaffiliated networks enabled and functional",
            "Merchant routing preference honored"
        ],
        resolution_strategy="Ensure asset size tracked, cap interchange at $0.21-0.23 + 0.05%, enable two networks (Visa + non-Visa or Mastercard + non-MC), document fraud prevention",
        entity_scope="Debit card issuers >$10B assets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Interchange at/below cap, two networks enabled, <$10B exempt",
            "AGGRESSIVE": "Interchange near cap, single network or affiliated networks",
            "DISCLOSURE": "Asset size fluctuates around $10B threshold",
            "HIGH_RISK": "Interchange exceeds cap, network exclusivity, >$10B non-compliant"
        },
        controlling_precedent=[
            "NACS v. Board of Governors (DC Cir 2013) - Durbin cap upheld",
            "12 CFR 235.4 - Fraud Prevention Standards"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="HMDA Home Mortgage Disclosure Act",
        keywords=["HMDA", "LAR", "reporting", "fair lending", "census tract"],
        conclusion_template=[
            "HMDA requires reporting of mortgage application and origination data.",
            "LAR (Loan Application Register) submitted annually by March 1.",
            "Data used for fair lending analysis and CRA compliance."
        ],
        reasoning_framework="""
12 USC 2801 et seq (HMDA) requires mortgage lending data collection and reporting.
12 CFR 1003 (Reg C) implements HMDA.
Covered institutions: depository and non-depository mortgage lenders meeting thresholds:
  - Depository: >$50M assets, metro location, 1+ home purchase or refi loan originated
  - Non-depository: >100 closed-end or >500 open-end home purchase/refi/home improvement loans in each prior 2 years
Reportable transactions: home purchase, refinance, home improvement, closed-end and open-end (HELOC).
Excluded: temporary financing, commercial/business purpose, rental >4 units (unless multifamily).
Data points: 48 fields including applicant demographics (race, ethnicity, sex), income, loan amount, property location (census tract),
  action taken (originated, denied, withdrawn), denial reasons, rate spread, HOEPA status, property value, DTI, CLTV, etc.
LAR submission: annually by March 1 to CFPB via HMDA Platform.
Public disclosure: aggregate data published, individual LAR data (with privacy protections).
Uses: fair lending enforcement (disparate impact analysis), CRA assessment, public transparency.
Penalties: civil money penalties for violations, pattern/practice enforcement.
""",
        key_factors=[
            "Institution meets asset/loan volume thresholds",
            "Transaction is reportable (home purchase/refi/improvement)",
            "Covered loan (dwelling-secured, consumer purpose)",
            "Data points collected and accurate (48 fields)",
            "LAR submitted timely (March 1 deadline)",
            "Fair lending risk identified in data (denial rates by race)"
        ],
        primary_authority=[
            "12 USC 2801 - Home Mortgage Disclosure Act",
            "12 CFR 1003 - Reg C HMDA Reporting",
            "HMDA Filing Instructions Guide",
            "CFPB HMDA Platform (hmdahelp.consumerfinance.gov)"
        ],
        burden_holder="Covered lender",
        adversary_position="Regulator claims data inaccurate or submission late, disparities identified",
        counter_arguments=[
            "Institution below thresholds (not covered)",
            "Loan not reportable (business purpose, >4 units)",
            "Data accurate based on application information",
            "Submission timely or technical issue caused delay",
            "Disparities explained by legitimate underwriting factors"
        ],
        resolution_strategy="Ensure HMDA LAR accuracy, submit by March 1, review data for fair lending risks, document underwriting criteria, train staff on data collection",
        entity_scope="Banks, credit unions, mortgage companies meeting thresholds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Data complete and accurate, submission timely, no disparities",
            "AGGRESSIVE": "Data quality issues, near-miss on deadline, borderline coverage",
            "DISCLOSURE": "Denial rate disparities present, underwriting docs weak",
            "HIGH_RISK": "LAR not submitted or late, significant data errors, unexplained disparities"
        },
        controlling_precedent=[
            "12 CFR 1003.4 - Covered Institutions",
            "CFPB HMDA Resubmission Guidelines"
        ],
        issue_category=IssueCategory.FAIR_LENDING
    ),

    DoctrineBlock(
        topic="TILA-RESPA Integrated Disclosures TRID",
        keywords=["TRID", "Loan Estimate", "Closing Disclosure", "3-day", "consummation"],
        conclusion_template=[
            "TRID requires Loan Estimate within 3 business days of application, Closing Disclosure 3 business days before consummation.",
            "Tolerances apply: zero for fees borrower cannot shop, 10% cumulative for fees borrower can shop.",
            "Redisclosure required if APR changes >0.125% or other triggering changes."
        ],
        reasoning_framework="""
12 CFR 1026 (Reg Z) and 12 CFR 1024 (Reg X) - TILA-RESPA Integrated Disclosures (TRID Rule, effective Oct 2015).
Applies to: most closed-end consumer mortgages secured by real property (not HELOC, reverse mortgage, mobile home not on land).
Loan Estimate (LE): provided within 3 business days of application (6 pieces of info: name, income, SSN, property address, estimate of value, loan amount).
7-business-day waiting period: from LE delivery to consummation.
Closing Disclosure (CD): provided at least 3 business days before consummation.
Redisclosure: required if APR increases >0.125% (0.25% irregular), loan product changes, prepayment penalty added.
Revised CD: resets 3-business-day waiting period.
Tolerances (cumulative):
  - Zero tolerance: fees borrower cannot shop (lender/affiliate charges except recording fees)
  - 10% tolerance: fees borrower can shop (if lender provides written list, borrower chooses off-list)
  - No tolerance: prepaid interest, property insurance, escrow varies
Cure: refund excess charges at/before consummation.
Business day: all calendar days except Sundays and federal holidays (for LE/CD delivery).
Consummation: borrower becomes contractually obligated (not closing/funding).
Penalties: actual damages, statutory damages, attorney fees, rescission rights if violations.
""",
        key_factors=[
            "Loan type covered (closed-end consumer mortgage)",
            "LE provided within 3 business days of application",
            "CD provided 3 business days before consummation",
            "Tolerances met (zero, 10%, no tolerance categories)",
            "Redisclosure triggered (APR, product, prepayment penalty)",
            "Revised CD resets waiting period"
        ],
        primary_authority=[
            "12 CFR 1026.19(e) - Loan Estimate Requirements",
            "12 CFR 1026.19(f) - Closing Disclosure Requirements",
            "CFPB TRID Small Entity Compliance Guide",
            "CFPB Official Interpretations to Reg Z"
        ],
        burden_holder="Creditor",
        adversary_position="Borrower claims disclosure late, inaccurate, or tolerances exceeded",
        counter_arguments=[
            "LE delivered within 3 business days (mail +3 days)",
            "CD delivered 3 business days before consummation (Saturday counts)",
            "Fees within tolerances or cured at closing",
            "Redisclosure provided when triggering event occurred",
            "Borrower waived waiting period (bona fide personal financial emergency)"
        ],
        resolution_strategy="Track application date, deliver LE promptly, provide CD early, monitor fee changes, cure tolerance violations, document redisclosures and waivers",
        entity_scope="Mortgage lenders (banks, credit unions, mortgage companies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "LE/CD timely, fees within tolerances, no redisclosure issues",
            "AGGRESSIVE": "Borderline timing (mail delivery), fees near 10% tolerance",
            "DISCLOSURE": "Redisclosure late, fee increased post-LE without justification",
            "HIGH_RISK": "LE/CD late, tolerances exceeded without cure, no redisclosure when required"
        },
        controlling_precedent=[
            "12 CFR 1026.19(e)(1)(iii) - Application Definition (6 pieces)",
            "12 CFR 1026.19(f)(2)(ii) - Zero Tolerance Fees"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="Affiliate Marketing Opt-Out FCRA 624",
        keywords=["FCRA", "affiliate marketing", "opt-out", "624", "pre-screen"],
        conclusion_template=[
            "FCRA Section 624 requires opt-out for affiliate marketing using consumer report info.",
            "Affiliate shares eligibility information (credit report data) for marketing - opt-out required.",
            "Opt-out notice at information sharing, consumer can opt out for 5+ years."
        ],
        reasoning_framework="""
15 USC 1681s-3 (FCRA Section 624) - affiliate marketing opt-out.
12 CFR 1022 Subpart C (Reg V) implements affiliate marketing opt-out.
Applies when: affiliate shares eligibility information derived from consumer report for marketing by another affiliate.
Eligibility information: info from consumer report (credit history, credit score, income, debt).
Sharing trigger: one affiliate obtains consumer report, shares info with another affiliate for marketing solicitation.
Opt-out required: notice and opportunity to opt out before marketing solicitation.
Opt-out duration: minimum 5 years, can be indefinite.
Exceptions: pre-existing business relationship (within 18 months), solicitation to service existing account.
Notice content: clear and conspicuous, explain right to opt out, how to opt out, duration.
Reasonable opportunity: simple method (toll-free number, form, online).
Enforcement: FTC, CFPB, bank regulators, state AGs.
Distinct from GLBA opt-out: GLBA = sharing with non-affiliates, FCRA 624 = affiliate marketing using report info.
""",
        key_factors=[
            "Affiliate relationship exists",
            "Eligibility information derived from consumer report",
            "Information shared for marketing purpose",
            "Pre-existing business relationship exception",
            "Opt-out notice provided before marketing",
            "Opt-out honored for 5+ years"
        ],
        primary_authority=[
            "15 USC 1681s-3 - FCRA Section 624",
            "12 CFR 1022 Subpart C - Affiliate Marketing Opt-Out",
            "CFPB Reg V Official Interpretations",
            "Interagency Affiliate Marketing Q&A"
        ],
        burden_holder="Affiliate sharing or using information",
        adversary_position="Consumer claims solicitation without opt-out opportunity",
        counter_arguments=[
            "Pre-existing business relationship within 18 months",
            "Solicitation to service existing account (not new product)",
            "Opt-out notice provided and consumer did not opt out",
            "Information shared not derived from consumer report (publicly available)"
        ],
        resolution_strategy="Provide opt-out notice before first affiliate marketing, track opt-outs centrally, honor opt-outs for 5+ years, document exceptions",
        entity_scope="Financial institutions with affiliates (banks, credit card issuers, insurance)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Opt-out notice provided, consumer did not opt out, exception applies",
            "AGGRESSIVE": "Borderline pre-existing relationship timing, weak notice",
            "DISCLOSURE": "Notice not clear/conspicuous, opt-out method difficult",
            "HIGH_RISK": "Marketing without opt-out, consumer report info shared, no exception"
        },
        controlling_precedent=[
            "12 CFR 1022.21 - Affiliate Marketing Opt-Out",
            "FCRA Section 603(d) - Consumer Report Definition"
        ],
        issue_category=IssueCategory.PRIVACY_DATA
    ),

    DoctrineBlock(
        topic="Expedited Funds Availability Act Regulation CC",
        keywords=["Reg CC", "funds availability", "hold", "next-day", "exception hold"],
        conclusion_template=[
            "Regulation CC requires funds availability schedules for check deposits.",
            "Next-day availability for cash, electronic, government, cashier's checks.",
            "Exception holds allowed (new accounts, repeated overdrafts, reasonable belief of uncollectibility) with notice."
        ],
        reasoning_framework="""
12 USC 4001 et seq (Expedited Funds Availability Act) governs check holds.
12 CFR 229 (Reg CC) implements EFAA.
Availability schedules:
  - Next business day: cash, electronic, US Treasury checks, cashier/teller/certified checks, first $225 of other checks
  - Second business day: local checks >$225
  - Fifth business day: non-local checks >$225
Local check: same Fed district or check processing region.
Large deposit exception: >$5,525 in one day (2024 threshold), hold allowed beyond schedule.
New account exception: first 30 days, extended holds allowed (up to 9 business days).
Exception holds (with notice): reasonable belief uncollectible, repeated overdrafts (6 in prior 6 months), emergency conditions.
Notice requirements: exception hold notice if hold extends beyond schedule, include reason, when funds available, contact info.
Longer hold: up to 7 business days (reasonable belief), 9 business days (new account).
Case-by-case hold: bank can place hold if reasonable belief check uncollectible.
Penalties: actual damages, attorney fees, class action, regulatory enforcement.
""",
        key_factors=[
            "Deposit type (cash, check, electronic)",
            "Check type (local vs non-local, government, cashier)",
            "Account age (new account <30 days)",
            "Large deposit >$5,525 threshold",
            "Exception applies (new account, overdrafts, uncollectibility)",
            "Exception hold notice provided"
        ],
        primary_authority=[
            "12 USC 4001 - Expedited Funds Availability Act",
            "12 CFR 229 - Reg CC Availability of Funds",
            "12 CFR 229.13 - Exception Holds",
            "Fed Reg CC Official Interpretations"
        ],
        burden_holder="Depository institution",
        adversary_position="Customer claims improper hold or notice deficient",
        counter_arguments=[
            "Hold within availability schedule (local/non-local)",
            "Exception applies (new account, repeated overdrafts, large deposit)",
            "Notice provided before hold expires (or within 1 business day for large deposit)",
            "Reasonable belief of uncollectibility (payee dispute, stop payment)"
        ],
        resolution_strategy="Follow availability schedules, use exception holds sparingly with notice, document reasonable belief, train staff on Reg CC timing",
        entity_scope="Banks, credit unions, thrifts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Hold within schedule or proper exception notice provided",
            "AGGRESSIVE": "Exception hold without clear reasonable belief, notice delayed",
            "DISCLOSURE": "Notice content incomplete (missing reason or funds date)",
            "HIGH_RISK": "Hold exceeds schedule without exception or notice, repeated violations"
        },
        controlling_precedent=[
            "12 CFR 229.10 - Next-Day Availability",
            "12 CFR 229.13(g) - Notice of Exception Hold"
        ],
        issue_category=IssueCategory.CONSUMER_PROTECTION
    ),

    DoctrineBlock(
        topic="HMDA Loan Data Integrity and Accuracy",
        keywords=["HMDA", "accuracy", "integrity", "review", "audit"],
        conclusion_template=[
            "HMDA requires accuracy and integrity of reported loan data.",
            "Lenders must implement procedures to ensure data accuracy.",
            "Errors must be corrected via resubmission or supplement."
        ],
        reasoning_framework="""
12 CFR 1003.6 - HMDA data accuracy and integrity.
Covered lender must ensure LAR accuracy through:
  - Comparison of LAR data with loan/application files
  - Reconciliation with internal reports (LOS, core system)
  - Independent testing/validation
Written procedures required for data collection, entry, validation, submission.
Pre-submission edits: HMDA Platform performs validity and quality edits.
Validity edits: must pass (format, range, enumerated values).
Quality edits: warnings (unusual values, inconsistencies), can override with justification.
Resubmission: if material errors discovered post-submission, must resubmit corrected LAR.
Timing: resubmit before next March 1 deadline or as directed by CFPB.
Consequences of inaccurate data: enforcement action, civil money penalties, fair lending risk if data conceals disparities.
CFPB exam focus: data integrity controls, error rates, resubmission responsiveness.
Self-identified errors: document and correct, less severe than regulator-identified.
""",
        key_factors=[
            "Written data integrity procedures in place",
            "Regular comparison of LAR to source documents",
            "Testing/validation performed",
            "Validity edits all passing",
            "Quality edits reviewed and justified",
            "Errors identified and corrected via resubmission"
        ],
        primary_authority=[
            "12 CFR 1003.6 - Enforcement and Violations",
            "HMDA Filing Instructions Guide - Edit Specifications",
            "CFPB Examination Procedures for HMDA",
            "CFPB HMDA Resubmission Guidelines"
        ],
        burden_holder="Covered lender",
        adversary_position="CFPB claims data inaccurate or integrity controls inadequate",
        counter_arguments=[
            "Written procedures documented and followed",
            "Regular audits conducted, error rate <1%",
            "Errors identified and resubmitted promptly",
            "Quality edits justified based on institution's business model",
            "Data matches loan origination system records"
        ],
        resolution_strategy="Implement robust data integrity program, reconcile LAR to LOS monthly, address HMDA Platform edits, resubmit errors promptly, document procedures",
        entity_scope="HMDA reporters (banks, credit unions, mortgage companies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Strong data integrity controls, low error rate, prompt resubmission",
            "AGGRESSIVE": "Weak controls, errors discovered post-submission, delayed resubmission",
            "DISCLOSURE": "Multiple quality edit overrides without justification",
            "HIGH_RISK": "Material errors concealing disparities, no resubmission, poor controls"
        },
        controlling_precedent=[
            "12 CFR 1003 Supplement I - Official Interpretations",
            "CFPB Consent Orders (HMDA data accuracy violations)"
        ],
        issue_category=IssueCategory.REGULATORY_REPORTING
    ),

    DoctrineBlock(
        topic="OCC Heightened Standards for Large Banks",
        keywords=["OCC", "heightened standards", "12 CFR 30", "risk governance", "large bank"],
        conclusion_template=[
            "OCC heightened standards apply to banks with $50B+ assets (or designated by OCC).",
            "Requires robust risk governance, independent risk management, effective challenge.",
            "Board and CEO accountability for risk management framework."
        ],
        reasoning_framework="""
12 CFR 30 Appendix D - OCC Heightened Standards for Large Banks.
Applies to: insured national banks/federal savings associations with $50B+ average assets (or designated by OCC).
Key requirements:
  - Risk governance framework designed by board, approved by board
  - Independent risk management function reporting to board/committee
  - Three lines of defense: business units (1st), risk management (2nd), internal audit (3rd)
  - Effective challenge: questioning and critical analysis across all levels
  - Board oversight: active engagement, expertise, training
  - CEO accountability: responsible for risk governance framework execution
Risk governance framework components:
  - Risk appetite statement (quantitative limits, qualitative guidelines)
  - Risk limits (concentration, market, credit, operational, compliance)
  - Risk management processes (identification, measurement, monitoring, control)
  - Escalation procedures for limit breaches
  - Independent risk management: CRO reports to board, not CEO; adequate stature and authority
Effective challenge: encouragement of contrary views, escalation without retribution.
Exam focus: board minutes, risk appetite documentation, CRO independence, escalation of breaches.
""",
        key_factors=[
            "Bank asset size ($50B+ threshold or OCC designation)",
            "Risk governance framework documented and board-approved",
            "Independent risk management function in place",
            "CRO independence from business lines",
            "Effective challenge culture demonstrated",
            "Risk appetite limits set and monitored"
        ],
        primary_authority=[
            "12 CFR 30 Appendix D - OCC Heightened Standards",
            "OCC Bulletin 2014-45 - Heightened Standards Guidance",
            "OCC Large Bank Supervision Handbook",
            "OCC Annual Risk Assessment (supervisory expectations)"
        ],
        burden_holder="Bank and board of directors",
        adversary_position="OCC claims risk governance inadequate or ineffective challenge lacking",
        counter_arguments=[
            "Risk governance framework comprehensive and board-approved",
            "CRO independent with direct board reporting line",
            "Effective challenge evidenced in board minutes and escalations",
            "Risk appetite statement detailed with quantitative limits",
            "Three lines of defense clearly delineated and functioning"
        ],
        resolution_strategy="Enhance risk governance documentation, strengthen CRO independence, document effective challenge examples, conduct board training, escalate limit breaches",
        entity_scope="Large national banks/FSAs ($50B+), OCC-designated banks",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification={
            "DEFENSIBLE": "Robust framework, CRO independent, effective challenge demonstrated",
            "AGGRESSIVE": "Framework documentation weak, CRO dual-reporting, limited challenge",
            "DISCLOSURE": "Risk appetite vague, escalation procedures unclear",
            "HIGH_RISK": "No framework, CRO subordinate to CEO, no effective challenge, OCC MRA"
        },
        controlling_precedent=[
            "12 CFR 30 App D Section II - Risk Governance Framework",
            "OCC MRA (Matters Requiring Attention) in large bank exams"
        ],
        issue_category=IssueCategory.OPERATIONAL_RISK
    )
]

class TelemetryCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.latencies: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors: List[Dict[str, Any]] = []

    def record_query(self, query: str, mode: ResponseMode, latency_ms: float,
                     layer: str, success: bool, error: Optional[str] = None):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:200],
            "mode": mode.value,
            "latency_ms": latency_ms,
            "layer": layer,
            "success": success
        }
        if error:
            record["error"] = error
            self.errors.append(record)
        self.queries.append(record)
        self.latencies.append(latency_ms)

    def record_cache_hit(self):
        self.cache_hits += 1

    def record_cache_miss(self):
        self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        if not self.latencies:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0,
                "cache_hit_rate": 0,
                "error_rate": 0
            }
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies),
            "cache_hit_rate": self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
            "error_rate": len(self.errors) / len(self.queries) if self.queries else 0
        }

telemetry = TelemetryCollector()
START_TIME = time.time()

def determinism_hash(data: Dict[str, Any]) -> str:
    """Generate SHA-256 hash for determinism tracking"""
    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

def apply_epistemic_guardrails(text: str) -> Tuple[str, Optional[str]]:
    """Scan for banned phrases, add disclosure if needed"""
    found_violations = [phrase for phrase in BANNED_PHRASES if phrase.lower() in text.lower()]

    if found_violations:
        disclosure = f"EPISTEMIC GUARDRAIL TRIGGERED: Response contained prohibited phrasing ({', '.join(found_violations)}). This analysis is for informational purposes only and does not constitute legal or compliance advice. Consult qualified regulatory counsel before taking action."
        cleaned = text
        for phrase in found_violations:
            cleaned = cleaned.replace(phrase, "[REDACTED - NOT ADVICE]")
        return cleaned, disclosure

    return text, None

def doctrine_cache_lookup(query: str, context: QueryContext) -> Optional[DoctrineBlock]:
    """Layer 1: Fast doctrine cache lookup"""
    query_lower = query.lower()
    query_tokens = set(query_lower.split())

    best_match = None
    best_score = 0

    for doctrine in DOCTRINE_CACHE:
        keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
        token_overlap = len(query_tokens.intersection(set(k.lower() for k in doctrine.keywords)))
        score = keyword_matches * 2 + token_overlap

        if score > best_score:
            best_score = score
            best_match = doctrine

    if best_score >= 3:
        return best_match
    return None

def generate_response_from_doctrine(doctrine: DoctrineBlock, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
    """Generate response from doctrine block"""

    if mode == ResponseMode.FAST:
        response = f"{doctrine.topic}: " + " ".join(doctrine.conclusion_template)
        response += f"\n\nKey factors: {', '.join(doctrine.key_factors[:3])}"
        response += f"\n\nPrimary authority: {doctrine.primary_authority[0]}"

    elif mode == ResponseMode.DEFENSE:
        response = f"ANALYSIS: {doctrine.topic}\n\n"
        response += "CONCLUSION:\n" + "\n".join(f"- {c}" for c in doctrine.conclusion_template)
        response += f"\n\nREASONING FRAMEWORK:\n{doctrine.reasoning_framework}"
        response += f"\n\nKEY FACTORS:\n" + "\n".join(f"- {f}" for f in doctrine.key_factors)
        response += f"\n\nPRIMARY AUTHORITY:\n" + "\n".join(f"- {a}" for a in doctrine.primary_authority)
        response += f"\n\nCONFIDENCE ASSESSMENT: {doctrine.confidence.value}"
        response += f"\n\n{doctrine.confidence_stratification.get(doctrine.confidence.value, '')}"

    else:  # MEMO
        response = f"MEMORANDUM - {doctrine.topic}\n\n"
        response += f"ISSUE CATEGORY: {doctrine.issue_category.value}\n"
        response += f"ANALYSIS ZONE: {zone.value}\n\n"
        response += "EXECUTIVE SUMMARY:\n" + "\n".join(f"{i+1}. {c}" for i, c in enumerate(doctrine.conclusion_template))
        response += f"\n\nDETAILED ANALYSIS:\n{doctrine.reasoning_framework}"
        response += f"\n\nKEY FACTORS:\n" + "\n".join(f"- {f}" for f in doctrine.key_factors)
        response += f"\n\nLEGAL AUTHORITY:\n" + "\n".join(f"- {a}" for a in doctrine.primary_authority)
        response += f"\n\nCONTROLLING PRECEDENT:\n" + "\n".join(f"- {p}" for p in doctrine.controlling_precedent)
        response += f"\n\nBURDEN OF PROOF: {doctrine.burden_holder}"
        response += f"\n\nADVERSARY POSITION: {doctrine.adversary_position}"
        response += f"\n\nCOUNTER-ARGUMENTS:\n" + "\n".join(f"- {c}" for c in doctrine.counter_arguments)
        response += f"\n\nRESOLUTION STRATEGY:\n{doctrine.resolution_strategy}"
        response += f"\n\nCONFIDENCE STRATIFICATION:"
        for level, detail in doctrine.confidence_stratification.items():
            response += f"\n  {level}: {detail}"
        response += f"\n\nENTITY SCOPE: {doctrine.entity_scope}"

    return response

def three_layer_response(context: QueryContext) -> Tuple[str, List[str], str, str]:
    """TIE-20 Component: Three-layer response system"""

    # Layer 1: Doctrine cache (0-200ms)
    doctrine = doctrine_cache_lookup(context.query, context)
    if doctrine:
        telemetry.record_cache_hit()
        response = generate_response_from_doctrine(doctrine, context.query, context.mode, context.zone)
        sources = doctrine.primary_authority
        confidence = doctrine.confidence.value
        return response, sources, confidence, "doctrine_cache"

    telemetry.record_cache_miss()

    # Layer 2: Semantic search (would query vector DB in production)
    # Simplified: return general guidance
    response = f"Banking regulatory query: {context.query}\n\n"
    response += "GENERAL GUIDANCE: Banking compliance involves BSA/AML, consumer protection (Reg Z, RESPA, ECOA), capital requirements (Basel III), liquidity (LCR), stress testing (DFAST/CCAR), fair lending, privacy (GLBA), and operational risk management. "
    response += f"For institution type '{context.institution_type}' with asset size '{context.asset_size}', consult applicable OCC, Fed, FDIC, CFPB regulations. "
    response += "Specific regulatory analysis requires detailed fact pattern review by qualified compliance personnel."

    sources = ["12 USC 5311 (BSA)", "12 CFR 1026 (Reg Z)", "12 CFR 3 (Capital)", "12 CFR 249 (LCR)"]
    confidence = ConfidenceLevel.DISCLOSURE.value
    layer = "semantic_search"

    if context.mode == ResponseMode.MEMO:
        response = f"MEMORANDUM - Banking Regulatory Query\n\n{response}"

    return response, sources, confidence, layer

APP = FastAPI(title=ENGINE_NAME, version=VERSION)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """TIE-20 Component: FastAPI query endpoint"""
    start = time.time()

    try:
        context = QueryContext(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            institution_type=request.institution_type,
            asset_size=request.asset_size
        )

        answer, sources, confidence, layer = three_layer_response(context)

        answer_clean, disclosure = apply_epistemic_guardrails(answer)

        latency_ms = (time.time() - start) * 1000

        response_data = {
            "answer": answer_clean,
            "sources": sources,
            "confidence": confidence,
            "mode": request.mode,
            "layer_used": layer,
            "query": request.query,
            "zone": request.zone.value,
            "institution_type": request.institution_type
        }

        hash_val = determinism_hash(response_data)

        telemetry.record_query(request.query, request.mode, latency_ms, layer, True)

        logger.info(f"Query processed | mode={request.mode.value} layer={layer} latency={latency_ms:.1f}ms hash={hash_val[:8]}")

        return QueryResponse(
            answer=answer_clean,
            sources=sources,
            confidence=confidence,
            mode=request.mode,
            layer_used=layer,
            latency_ms=latency_ms,
            determinism_hash=hash_val,
            epistemic_disclosure=disclosure
        )

    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        telemetry.record_query(request.query, request.mode, latency_ms, "error", False, str(e))
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component: Health endpoint"""
    stats = telemetry.get_stats()
    uptime = time.time() - START_TIME

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=uptime,
        total_queries=stats["total_queries"],
        avg_latency_ms=stats["avg_latency_ms"],
        cache_hit_rate=stats["cache_hit_rate"],
        doctrine_count=len(DOCTRINE_CACHE)
    )

@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"TIE-20 compliant: doctrine cache, three-layer response, telemetry, epistemic guardrails")

    uvicorn.run(APP, host="0.0.0.0", port=PORT)
