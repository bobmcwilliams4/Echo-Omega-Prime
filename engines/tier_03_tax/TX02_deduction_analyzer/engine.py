import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import threading

# ENUMS

class ResponseMode(Enum):
    FAST = auto()
    DEFENSE = auto()
    MEMO = auto()

class PositionZone(Enum):
    PLANNING = auto()
    REPORTING = auto()
    AUDIT = auto()

class ConfidenceZone(Enum):
    DEFENSIBLE = auto()
    AGGRESSIVE = auto()
    DISCLOSURE = auto()
    HIGH_RISK = auto()

class IssueCategory(Enum):
    ORDINARY_NECESSARY = auto()
    INTEREST_LIMITATION = auto()
    SALT_CAP = auto()
    CASUALTY_LOSS = auto()
    BAD_DEBT = auto()
    DEPRECIATION = auto()
    CHARITABLE_CONTRIBUTION = auto()
    AMORTIZATION_NOL = auto()
    R_AND_E_EXPENSE = auto()
    STARTUP_EXPENSE = auto()
    INTANGIBLE_AMORTIZATION = auto()
    QBI_199A = auto()
    INVESTMENT_EXPENSE = auto()
    MEDICAL_EXPENSE = auto()
    MOVING_EXPENSE = auto()
    HOME_OFFICE = auto()
    MARIJUANA_LIMITATION = auto()
    LUXURY_AUTO = auto()
    ENTERTAINMENT_MEAL = auto()
    HOBBY_LOSS = auto()
    ECONOMIC_SUBSTANCE = auto()

# METRICS COLLECTOR

class MetricsCollector:
    def __init__(self):
        self.query_log = []
        self.error_log = []
        self.doctrine_hits = {}
        self.lock = threading.Lock()

    def record_query(self, doctrine_ids: List[str], latency_ms: int):
        with self.lock:
            self.query_log.append({
                "timestamp": datetime.utcnow(),
                "doctrines": doctrine_ids,
                "latency_ms": latency_ms
            })
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1

    def record_error(self, error_msg: str):
        with self.lock:
            self.error_log.append({
                "timestamp": datetime.utcnow(),
                "error": error_msg
            })

    def get_latency_stats(self):
        with self.lock:
            latencies = [q["latency_ms"] for q in self.query_log[-100:]]
            if not latencies:
                return {"avg": 0, "max": 0, "min": 0}
            return {
                "avg": sum(latencies) / len(latencies),
                "max": max(latencies),
                "min": min(latencies)
            }

    def get_doctrine_hit_rate(self):
        with self.lock:
            total = sum(self.doctrine_hits.values())
            return {k: v / total for k, v in self.doctrine_hits.items()} if total else {}

    def queries_last_hour(self):
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return len([q for q in self.query_log if q["timestamp"] > cutoff])

metrics_collector = MetricsCollector()

# PYDANTIC MODELS

class QueryRequest(BaseModel):
    scenario: str
    mode: ResponseMode
    entity_type: str
    complexity: int

class QueryResponse(BaseModel):
    engine_id: str
    query_id: str
    mode: ResponseMode
    confidence: float
    confidence_zone: ConfidenceZone
    position_zone: PositionZone
    primary_conclusion: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    counter_arguments: List[str]
    resolution_strategy: str
    determinism_hash: str
    doctrine_ids: List[str]
    triggered_doctrines: List[str]
    missed_doctrines: List[str]
    epistemic_gaps: List[str]
    audit_trail_id: str
    coverage_map: Dict[str, Any]
    drift_status: str

# DOCTRINE CACHE

@dataclass
class DoctrineBlock:
    doctrine_id: str
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
    confidence_zone: ConfidenceZone
    controlling_precedent: str

doctrine_cache: List[DoctrineBlock] = [
    DoctrineBlock(
        doctrine_id="D01",
        topic="§162 Ordinary and Necessary Business Expenses",
        keywords=["ordinary", "necessary", "business", "Welch v. Helvering", "expense", "deductibility", "trade", "activity"],
        conclusion_template="Expenses that are both ordinary and necessary in carrying on a trade or business are generally deductible under IRC §162. The taxpayer must demonstrate the expense is common and accepted in the business and appropriate for the business's operations.",
        reasoning_framework=(
            "IRC §162(a) allows deduction of all ordinary and necessary expenses paid or incurred during the taxable year in carrying on any trade or business. "
            "The Supreme Court in Welch v. Helvering, 290 U.S. 111 (1933), established that 'ordinary' means normal, usual, or customary in the context of the taxpayer's business, "
            "while 'necessary' refers to expenses that are appropriate and helpful. "
            "Treas. Reg. §1.162-1 further clarifies that expenses must not be capital in nature, personal, or subject to other disallowance provisions. "
            "Key factors include the nature of the business, industry norms, and the taxpayer's intent. "
            "Expenses must be substantiated with adequate records per Treas. Reg. §1.6001-1. "
            "The burden of proof rests with the taxpayer to show both ordinary and necessary character. "
            "The IRS may challenge deductions that appear excessive, personal, or lack business purpose. "
            "Courts have applied the Cohan rule (Cohan v. Commissioner, 39 F.2d 540 (2d Cir. 1930)) to allow reasonable estimation where records are incomplete, "
            "but only if some evidence supports the deduction. "
            "Expenses must not be subject to §274 limitations (e.g., entertainment, meals), §280A (home office), or §280E (illegal businesses). "
            "Audit defense requires clear documentation, business purpose, and industry comparables. "
            "Resolution involves weighing the taxpayer's substantiation against IRS challenges and applying relevant precedents."
        ),
        key_factors=[
            "Expense is incurred in carrying on a trade or business",
            "Expense is ordinary (common, accepted in industry)",
            "Expense is necessary (appropriate, helpful)",
            "Expense is not capital, personal, or otherwise disallowed",
            "Adequate substantiation and documentation"
        ],
        primary_authority=[
            "IRC §162(a)",
            "Treas. Reg. §1.162-1",
            "Welch v. Helvering, 290 U.S. 111 (1933)",
            "Cohan v. Commissioner, 39 F.2d 540 (2d Cir. 1930)"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert expense is personal, capital, or not ordinary/necessary",
        counter_arguments=[
            "Expense is personal in nature and not related to business",
            "Expense is capital and should be capitalized, not deducted",
            "Expense is not customary in the taxpayer's industry",
            "Expense lacks adequate substantiation",
            "Expense is subject to other IRC limitations"
        ],
        resolution_strategy="Evaluate substantiation, business purpose, and apply industry comparables; reference relevant case law and regulations.",
        entity_scope="Individuals, partnerships, corporations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Welch v. Helvering, 290 U.S. 111 (1933)"
    ),
    DoctrineBlock(
        doctrine_id="D02",
        topic="§163 Interest Deduction and §163(j) Limitation",
        keywords=["interest", "deduction", "business", "limitation", "ATI", "30%", "section 163(j)", "carryforward"],
        conclusion_template="Business interest expense is generally deductible under IRC §163, but may be limited by §163(j) to 30% of adjusted taxable income (ATI). Disallowed interest may be carried forward indefinitely.",
        reasoning_framework=(
            "IRC §163(a) allows deduction of interest paid or accrued on indebtedness. "
            "However, §163(j) imposes a limitation on business interest expense for certain taxpayers, restricting the deduction to the sum of business interest income, 30% of ATI, and floor plan financing interest. "
            "ATI is defined in §163(j)(8) and excludes depreciation, amortization, and depletion for years before 2022. "
            "Disallowed interest is carried forward indefinitely per §163(j)(2). "
            "Small businesses (average gross receipts < $27M for 2024, §163(j)(3)) are exempt. "
            "Treas. Reg. §1.163(j)-1 through -10 provide detailed computational rules, aggregation, and anti-abuse provisions. "
            "Key factors include entity type, gross receipts, computation of ATI, and proper classification of interest expense. "
            "Audit defense requires accurate calculation, supporting schedules, and identification of exempt entities. "
            "Resolution involves applying the limitation, tracking carryforwards, and substantiating calculations."
        ),
        key_factors=[
            "Interest expense is paid/accrued on bona fide indebtedness",
            "Taxpayer is not exempt under small business exception",
            "ATI is properly computed",
            "Interest deduction does not exceed 30% of ATI",
            "Disallowed interest is tracked for carryforward"
        ],
        primary_authority=[
            "IRC §163(a)",
            "IRC §163(j)",
            "Treas. Reg. §1.163(j)-1",
            "Treas. Reg. §1.163(j)-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may challenge ATI computation or assert interest is not bona fide",
        counter_arguments=[
            "Interest expense exceeds limitation and is not properly carried forward",
            "ATI is incorrectly computed",
            "Interest is not paid on bona fide debt",
            "Taxpayer is not eligible for small business exception",
            "Interest expense is recharacterized as nondeductible"
        ],
        resolution_strategy="Apply §163(j) limitation, verify ATI computation, and document carryforward tracking.",
        entity_scope="Corporations, partnerships, individuals with business interest",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §1.163(j)-1"
    ),
    DoctrineBlock(
        doctrine_id="D03",
        topic="§164 State and Local Tax Deduction (SALT Cap)",
        keywords=["state tax", "local tax", "deduction", "SALT", "cap", "property tax", "income tax", "limitation"],
        conclusion_template="Individuals may deduct state and local taxes paid, but the deduction is capped at $10,000 ($5,000 MFS) under IRC §164(b)(6).",
        reasoning_framework=(
            "IRC §164(a) allows deduction for state and local income, sales, and property taxes paid. "
            "The Tax Cuts and Jobs Act (TCJA) added §164(b)(6), capping the deduction at $10,000 ($5,000 for married filing separately) for tax years 2018-2025. "
            "The cap applies to the aggregate of state and local income, sales, and property taxes. "
            "Treas. Reg. §1.164-3 and IRS Notice 2019-12 clarify the application and anti-abuse rules, including treatment of charitable contributions in lieu of taxes. "
            "Key factors include filing status, types of taxes paid, and proper aggregation. "
            "Audit defense requires substantiation of payments and correct application of the cap. "
            "Resolution involves verifying the types and amounts of taxes paid and applying the statutory limitation."
        ),
        key_factors=[
            "Taxpayer is an individual",
            "State and local taxes paid are eligible under §164(a)",
            "Deduction does not exceed $10,000 ($5,000 MFS)",
            "Proper aggregation of taxes",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §164(a)",
            "IRC §164(b)(6)",
            "Treas. Reg. §1.164-3",
            "IRS Notice 2019-12"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert deduction exceeds cap or includes ineligible taxes",
        counter_arguments=[
            "Deduction exceeds statutory cap",
            "Taxes paid are not eligible under §164(a)",
            "Improper aggregation of taxes",
            "Insufficient substantiation",
            "Attempted workaround via charitable contribution"
        ],
        resolution_strategy="Aggregate eligible taxes, apply cap, and document payments.",
        entity_scope="Individuals",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §164(b)(6)"
    ),
    DoctrineBlock(
        doctrine_id="D04",
        topic="§165 Losses: Casualty and Theft",
        keywords=["loss", "casualty", "theft", "deduction", "personal", "business", "disaster", "substantiation"],
        conclusion_template="Losses from casualty or theft may be deductible under IRC §165, subject to limitations and substantiation requirements. Personal casualty losses are generally limited to federally declared disasters.",
        reasoning_framework=(
            "IRC §165(a) allows deduction for losses sustained during the taxable year not compensated by insurance or otherwise. "
            "Casualty losses are defined in §165(c)(3) and Treas. Reg. §1.165-7 as sudden, unexpected, and unusual events. "
            "The TCJA restricts personal casualty loss deductions to losses attributable to federally declared disasters for tax years 2018-2025. "
            "Theft losses are covered by §165(c)(3) and Treas. Reg. §1.165-8, requiring evidence of criminal intent and actual loss. "
            "Losses must be reduced by $100 per event and 10% of AGI for individuals (§165(h)). "
            "Business losses are not subject to these limitations. "
            "Key factors include nature of loss, insurance recovery, disaster declaration, and substantiation. "
            "Audit defense requires documentation of event, valuation, and insurance claims. "
            "Resolution involves applying statutory limitations and substantiating the loss."
        ),
        key_factors=[
            "Loss is from casualty or theft",
            "Loss is not compensated by insurance",
            "For personal losses, event is federally declared disaster",
            "Proper reduction by $100 and 10% AGI",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §165(a)",
            "IRC §165(c)(3)",
            "Treas. Reg. §1.165-7",
            "Treas. Reg. §1.165-8"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert loss is not casualty/theft, or not substantiated",
        counter_arguments=[
            "Loss is not sudden, unexpected, or unusual",
            "Loss is compensated by insurance",
            "Event is not federally declared disaster",
            "Insufficient substantiation",
            "Improper calculation of deductible amount"
        ],
        resolution_strategy="Verify event qualifies, apply limitations, and document loss and insurance recovery.",
        entity_scope="Individuals, businesses",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §165(c)(3)"
    ),
    DoctrineBlock(
        doctrine_id="D05",
        topic="§166 Bad Debts: Business vs Nonbusiness",
        keywords=["bad debt", "business", "nonbusiness", "wholly worthless", "partially worthless", "deduction", "substantiation"],
        conclusion_template="Bad debts may be deductible under IRC §166 if they become wholly or partially worthless. Business bad debts are deductible against ordinary income; nonbusiness bad debts are treated as short-term capital losses.",
        reasoning_framework=(
            "IRC §166(a) allows deduction for debts that become wholly or partially worthless during the taxable year. "
            "Business bad debts arise from trade or business activities and are deductible against ordinary income. "
            "Nonbusiness bad debts are deductible only when wholly worthless and are treated as short-term capital losses (§166(d)). "
            "Treas. Reg. §1.166-1 and §1.166-5 provide guidance on determining worthlessness and substantiation. "
            "Key factors include nature of debt, relationship to taxpayer's business, evidence of worthlessness, and collection efforts. "
            "Audit defense requires documentation of debt, efforts to collect, and evidence supporting worthlessness. "
            "Resolution involves classifying debt, substantiating worthlessness, and applying proper deduction treatment."
        ),
        key_factors=[
            "Debt is bona fide and documented",
            "Debt is related to trade or business (for business bad debt)",
            "Debt is wholly or partially worthless",
            "Collection efforts are documented",
            "Proper classification as business or nonbusiness"
        ],
        primary_authority=[
            "IRC §166(a)",
            "IRC §166(d)",
            "Treas. Reg. §1.166-1",
            "Treas. Reg. §1.166-5"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert debt is not bona fide or not worthless",
        counter_arguments=[
            "Debt is not bona fide",
            "Debt is not related to business",
            "Debt is not wholly or partially worthless",
            "Insufficient collection efforts",
            "Improper classification of debt"
        ],
        resolution_strategy="Document debt, collection efforts, and evidence of worthlessness; apply proper classification.",
        entity_scope="Individuals, businesses",
        confidence=0.87,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §1.166-1"
    ),
    DoctrineBlock(
        doctrine_id="D06",
        topic="§167/168 Depreciation: MACRS, §179, Bonus",
        keywords=["depreciation", "MACRS", "§179", "bonus", "expensing", "property", "class life", "limitation"],
        conclusion_template="Depreciation deductions are allowed under IRC §§167 and 168 for property used in business. §179 allows expensing up to $1,160,000 (2024), subject to phase-out. Bonus depreciation under §168(k) is available for qualified property.",
        reasoning_framework=(
            "IRC §167 allows deduction for depreciation of property used in trade or business or held for production of income. "
            "IRC §168 establishes MACRS, assigning class lives and recovery periods. "
            "§179 permits immediate expensing of up to $1,160,000 in 2024, with phase-out beginning at $2,890,000. "
            "Bonus depreciation under §168(k) allows 60% deduction in 2024 for qualified property, subject to phase-out. "
            "Treas. Reg. §1.167(a)-1, §1.168(b)-1, and §1.179-2 provide computational and substantiation rules. "
            "Key factors include property eligibility, placed-in-service date, entity type, and proper calculation. "
            "Audit defense requires asset schedules, purchase documentation, and election statements. "
            "Resolution involves applying MACRS tables, §179 and bonus limitations, and substantiating property use."
        ),
        key_factors=[
            "Property is eligible for depreciation",
            "Placed in service during taxable year",
            "Proper classification under MACRS",
            "§179 and bonus limitations applied",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §167",
            "IRC §168",
            "IRC §179",
            "Treas. Reg. §1.167(a)-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper classification or excessive deduction",
        counter_arguments=[
            "Property is not eligible for depreciation",
            "Improper placed-in-service date",
            "Exceeds §179 or bonus limits",
            "Insufficient substantiation",
            "Improper MACRS classification"
        ],
        resolution_strategy="Apply MACRS tables, verify §179 and bonus eligibility, and document asset schedules.",
        entity_scope="Businesses",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §168"
    ),
    DoctrineBlock(
        doctrine_id="D07",
        topic="§170 Charitable Contributions: AGI Limits, Carryforward",
        keywords=["charitable", "contribution", "AGI limit", "carryforward", "substantiation", "deduction", "organization"],
        conclusion_template="Charitable contributions to qualified organizations are deductible under IRC §170, subject to AGI limitations (60%, 30%, 20%) and substantiation. Excess contributions may be carried forward for five years.",
        reasoning_framework=(
            "IRC §170(a) allows deduction for charitable contributions to qualified organizations. "
            "AGI limitations are 60% for cash contributions to public charities, 30% for property or gifts to certain organizations, and 20% for gifts to private foundations (§170(b)). "
            "Excess contributions may be carried forward for five years (§170(d)). "
            "Treas. Reg. §1.170A-1 through -13 provide substantiation and valuation rules. "
            "Key factors include organization qualification, contribution type, AGI computation, and substantiation. "
            "Audit defense requires receipts, appraisals for property, and compliance with substantiation requirements. "
            "Resolution involves applying AGI limits, tracking carryforwards, and documenting contributions."
        ),
        key_factors=[
            "Contribution is to qualified organization",
            "Proper classification of contribution type",
            "AGI limitation applied",
            "Carryforward tracked",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §170(a)",
            "IRC §170(b)",
            "IRC §170(d)",
            "Treas. Reg. §1.170A-13"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert organization is not qualified or substantiation is lacking",
        counter_arguments=[
            "Contribution is not to qualified organization",
            "Exceeds AGI limitation",
            "Insufficient substantiation",
            "Improper valuation of property",
            "Carryforward not properly tracked"
        ],
        resolution_strategy="Verify organization qualification, apply AGI limits, and document contributions.",
        entity_scope="Individuals, businesses",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §170(b)"
    ),
    DoctrineBlock(
        doctrine_id="D08",
        topic="§172 NOL: Amortization and Limitation",
        keywords=["NOL", "net operating loss", "amortization", "limitation", "carryforward", "carryback", "80%", "TCJA"],
        conclusion_template="Net operating losses (NOLs) may be carried forward indefinitely under IRC §172, but deduction is limited to 80% of taxable income. Carrybacks are generally disallowed post-TCJA.",
        reasoning_framework=(
            "IRC §172(a) allows deduction for NOLs arising from business operations. "
            "The TCJA amended §172 to limit NOL deduction to 80% of taxable income for losses arising after 2017. "
            "Carrybacks are generally disallowed except for certain farming and insurance companies. "
            "NOLs may be carried forward indefinitely. "
            "Treas. Reg. §1.172-1 and IRS guidance clarify computation and application. "
            "Key factors include proper computation of NOL, taxable income limitation, and tracking of carryforwards. "
            "Audit defense requires supporting schedules and documentation of loss origins. "
            "Resolution involves applying limitation, tracking carryforwards, and substantiating losses."
        ),
        key_factors=[
            "NOL arises from business operations",
            "Proper computation of NOL",
            "Deduction limited to 80% of taxable income",
            "Carryforward tracked",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §172(a)",
            "IRC §172(b)",
            "Treas. Reg. §1.172-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper computation or excessive deduction",
        counter_arguments=[
            "NOL does not arise from business operations",
            "Improper computation of NOL",
            "Deduction exceeds 80% limitation",
            "Carryforward not properly tracked",
            "Insufficient substantiation"
        ],
        resolution_strategy="Apply 80% limitation, track carryforwards, and document NOL computation.",
        entity_scope="Businesses",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §172(a)"
    ),
    DoctrineBlock(
        doctrine_id="D09",
        topic="§174 Research and Experimental Expenditures",
        keywords=["research", "experimental", "expenditure", "amortization", "deduction", "5-year", "post-2022", "substantiation"],
        conclusion_template="Research and experimental expenditures must be amortized over five years under IRC §174 for tax years after 2022. Immediate deduction is no longer permitted.",
        reasoning_framework=(
            "IRC §174(a) previously allowed immediate deduction for research and experimental expenditures. "
            "The TCJA amended §174, requiring amortization over five years for expenditures incurred after December 31, 2021. "
            "Treas. Reg. §1.174-2 and IRS guidance clarify eligible expenditures and amortization rules. "
            "Key factors include proper classification of expenditures, amortization schedule, and substantiation. "
            "Audit defense requires documentation of research activities, expenditures, and amortization calculations. "
            "Resolution involves applying amortization, tracking expenditures, and substantiating eligibility."
        ),
        key_factors=[
            "Expenditure qualifies as research or experimental",
            "Incurred after December 31, 2021",
            "Amortization schedule applied",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §174(a)",
            "IRC §174(b)",
            "Treas. Reg. §1.174-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert expenditure is not eligible or amortization is incorrect",
        counter_arguments=[
            "Expenditure does not qualify as research or experimental",
            "Improper amortization schedule",
            "Insufficient substantiation",
            "Improper classification",
            "Expenditure is capital in nature"
        ],
        resolution_strategy="Apply five-year amortization, document expenditures, and substantiate eligibility.",
        entity_scope="Businesses",
        confidence=0.86,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §174(b)"
    ),
    DoctrineBlock(
        doctrine_id="D10",
        topic="§195 Startup Expenses",
        keywords=["startup", "expense", "deduction", "$5,000", "phase-out", "amortization", "business", "election"],
        conclusion_template="Startup expenses may be deducted up to $5,000 under IRC §195, with phase-out for expenses exceeding $50,000. Remaining expenses are amortized over 15 years.",
        reasoning_framework=(
            "IRC §195(a) allows deduction of up to $5,000 in startup expenses, reduced dollar-for-dollar for expenses exceeding $50,000. "
            "Remaining expenses are amortized over 180 months. "
            "Treas. Reg. §1.195-1 provides guidance on eligible expenses, election procedures, and substantiation. "
            "Key factors include nature of expenses, timing, election, and substantiation. "
            "Audit defense requires documentation of expenses, business purpose, and election statement. "
            "Resolution involves applying phase-out, amortization, and substantiating expenses."
        ),
        key_factors=[
            "Expense qualifies as startup under §195",
            "Proper timing and election",
            "Phase-out applied for expenses > $50,000",
            "Amortization schedule applied",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §195(a)",
            "Treas. Reg. §1.195-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert expenses are not startup or election is improper",
        counter_arguments=[
            "Expense does not qualify as startup",
            "Improper election",
            "Phase-out not applied",
            "Insufficient substantiation",
            "Improper amortization"
        ],
        resolution_strategy="Apply $5,000 deduction, phase-out, and amortization; document expenses and election.",
        entity_scope="Businesses",
        confidence=0.85,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §195(a)"
    ),
    DoctrineBlock(
        doctrine_id="D11",
        topic="§197 Amortizable Intangibles",
        keywords=["intangible", "amortization", "15-year", "anti-churning", "deduction", "business", "acquisition"],
        conclusion_template="Intangible assets acquired after August 10, 1993, may be amortized over 15 years under IRC §197. Anti-churning rules prevent deduction for certain pre-existing intangibles.",
        reasoning_framework=(
            "IRC §197 allows amortization of certain intangible assets over 15 years. "
            "Assets must be acquired after August 10, 1993, and include goodwill, going concern value, trademarks, franchises, and similar items. "
            "Anti-churning rules (§197(f)) prevent deduction for intangibles held or used by the taxpayer or related parties before the effective date. "
            "Treas. Reg. §1.197-2 provides guidance on eligible assets, anti-churning, and substantiation. "
            "Key factors include acquisition date, asset classification, anti-churning application, and substantiation. "
            "Audit defense requires acquisition documentation, asset schedules, and anti-churning analysis. "
            "Resolution involves applying 15-year amortization, verifying asset eligibility, and substantiating acquisition."
        ),
        key_factors=[
            "Asset is intangible and acquired after August 10, 1993",
            "Proper classification under §197",
            "Anti-churning rules applied",
            "15-year amortization schedule",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §197",
            "Treas. Reg. §1.197-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert asset is not eligible or anti-churning applies",
        counter_arguments=[
            "Asset is not intangible or not acquired after effective date",
            "Improper classification",
            "Anti-churning rules disallow deduction",
            "Insufficient substantiation",
            "Improper amortization schedule"
        ],
        resolution_strategy="Apply 15-year amortization, verify asset eligibility, and document acquisition.",
        entity_scope="Businesses",
        confidence=0.84,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §197"
    ),
    DoctrineBlock(
        doctrine_id="D12",
        topic="§199A Qualified Business Income Deduction",
        keywords=["QBI", "qualified business income", "20%", "deduction", "W-2 wage", "UBIA", "SSTB", "limitation"],
        conclusion_template="Qualified business income (QBI) deduction under IRC §199A allows up to 20% deduction for eligible taxpayers, subject to W-2 wage and UBIA limitations and SSTB exclusion.",
        reasoning_framework=(
            "IRC §199A provides a deduction of up to 20% of qualified business income for pass-through entities. "
            "Deduction is limited by W-2 wage and unadjusted basis of qualified property (UBIA) for taxpayers above threshold. "
            "Specified service trades or businesses (SSTBs) are excluded for high-income taxpayers. "
            "Treas. Reg. §1.199A-1 through -6 provide computational rules, aggregation, and anti-abuse provisions. "
            "Key factors include entity type, income level, W-2 wage and UBIA computation, and SSTB classification. "
            "Audit defense requires QBI computation, wage/property schedules, and SSTB analysis. "
            "Resolution involves applying limitations, verifying QBI, and substantiating eligibility."
        ),
        key_factors=[
            "Taxpayer has qualified business income",
            "Income is below threshold or limitations applied",
            "W-2 wage and UBIA computed",
            "SSTB exclusion applied",
            "Adequate substantiation"
        ],
        primary_authority=[
            "IRC §199A",
            "Treas. Reg. §1.199A-1",
            "Treas. Reg. §1.199A-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper QBI computation or SSTB exclusion applies",
        counter_arguments=[
            "Income exceeds threshold and limitations not applied",
            "Improper QBI computation",
            "SSTB exclusion applies",
            "Insufficient substantiation",
            "Improper wage/property calculation"
        ],
        resolution_strategy="Apply QBI limitations, verify wage/property schedules, and document eligibility.",
        entity_scope="Individuals, pass-through entities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §199A"
    ),
    DoctrineBlock(
        doctrine_id="D13",
        topic="§212 Investment Expenses (Suspended)",
        keywords=["investment", "expense", "deduction", "suspended", "individual", "TCJA", "2025"],
        conclusion_template="Investment expenses under IRC §212 are suspended for individuals for tax years 2018-2025 under TCJA. Deduction is not currently allowed.",
        reasoning_framework=(
            "IRC §212 allows deduction for ordinary and necessary expenses incurred for the production of income. "
            "The TCJA suspended miscellaneous itemized deductions subject to the 2% AGI floor, including investment expenses, for tax years 2018-2025. "
            "Treas. Reg. §1.212-1 and IRS guidance clarify eligible expenses and suspension. "
            "Key factors include taxpayer status, expense classification, and timing. "
            "Audit defense requires documentation of expenses and awareness of suspension. "
            "Resolution involves recognizing suspension and substantiating expenses for future years."
        ),
        key_factors=[
            "Expense qualifies under §212",
            "Taxpayer is individual",
            "Expense incurred during suspension period",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §212",
            "TCJA §11045",
            "Treas. Reg. §1.212-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert expense is not eligible or deduction is suspended",
        counter_arguments=[
            "Expense does not qualify under §212",
            "Deduction is suspended under TCJA",
            "Insufficient substantiation",
            "Improper classification",
            "Expense is personal"
        ],
        resolution_strategy="Recognize suspension, document expenses, and plan for future deductibility.",
        entity_scope="Individuals",
        confidence=0.80,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="TCJA §11045"
    ),
    DoctrineBlock(
        doctrine_id="D14",
        topic="§213 Medical Expenses",
        keywords=["medical", "expense", "deduction", "7.5% AGI", "substantiation", "individual", "limitation"],
        conclusion_template="Medical expenses are deductible under IRC §213 if they exceed 7.5% of AGI. Only unreimbursed, qualified expenses are eligible.",
        reasoning_framework=(
            "IRC §213(a) allows deduction for unreimbursed medical expenses exceeding 7.5% of AGI. "
            "Qualified expenses are defined in §213(d) and Treas. Reg. §1.213-1. "
            "Expenses must be for diagnosis, cure, mitigation, treatment, or prevention of disease. "
            "Key factors include taxpayer status, AGI computation, expense qualification, and substantiation. "
            "Audit defense requires receipts, medical records, and proof of unreimbursed status. "
            "Resolution involves applying AGI floor, verifying expense qualification, and documenting payments."
        ),
        key_factors=[
            "Expense qualifies as medical under §213(d)",
            "Unreimbursed by insurance",
            "Exceeds 7.5% of AGI",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §213(a)",
            "IRC §213(d)",
            "Treas. Reg. §1.213-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert expense is not qualified or is reimbursed",
        counter_arguments=[
            "Expense does not qualify under §213(d)",
            "Expense is reimbursed",
            "Does not exceed 7.5% AGI",
            "Insufficient substantiation",
            "Improper classification"
        ],
        resolution_strategy="Apply AGI floor, verify expense qualification, and document payments.",
        entity_scope="Individuals",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §213(a)"
    ),
    DoctrineBlock(
        doctrine_id="D15",
        topic="§217 Moving Expenses (Military Only)",
        keywords=["moving", "expense", "deduction", "military", "TCJA", "individual", "limitation"],
        conclusion_template="Moving expenses are deductible under IRC §217 only for active duty military members moving pursuant to orders. Deduction is suspended for other taxpayers through 2025.",
        reasoning_framework=(
            "IRC §217(a) allows deduction for moving expenses incurred in connection with starting work at a new location. "
            "The TCJA suspended the deduction for tax years 2018-2025 except for active duty military members moving pursuant to orders. "
            "Treas. Reg. §1.217-2 and IRS guidance clarify eligibility and substantiation. "
            "Key factors include taxpayer status, military orders, timing, and substantiation. "
            "Audit defense requires documentation of orders, expenses, and unreimbursed status. "
            "Resolution involves verifying eligibility, applying suspension, and documenting expenses."
        ),
        key_factors=[
            "Taxpayer is active duty military",
            "Move is pursuant to military orders",
            "Expense incurred during suspension period",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §217(a)",
            "TCJA §11047",
            "Treas. Reg. §1.217-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert taxpayer is not eligible or expenses are not qualified",
        counter_arguments=[
            "Taxpayer is not active duty military",
            "Move is not pursuant to orders",
            "Deduction is suspended under TCJA",
            "Insufficient substantiation",
            "Improper classification"
        ],
        resolution_strategy="Verify military status, apply suspension, and document expenses.",
        entity_scope="Individuals",
        confidence=0.82,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="TCJA §11047"
    ),
    DoctrineBlock(
        doctrine_id="D16",
        topic="§280A Home Office Deduction",
        keywords=["home office", "deduction", "exclusive use", "regular use", "principal place", "substantiation", "limitation"],
        conclusion_template="Home office deduction under IRC §280A is allowed only if the space is used exclusively and regularly for business and is the principal place of business.",
        reasoning_framework=(
            "IRC §280A(c) allows deduction for home office expenses if the space is used exclusively and regularly for business. "
            "The principal place of business test is clarified in Commissioner v. Soliman, 506 U.S. 168 (1993). "
            "Treas. Reg. §1.280A-2 provides guidance on exclusive and regular use. "
            "Key factors include space exclusivity, regularity of use, principal place of business, and substantiation. "
            "Audit defense requires floor plans, usage logs, and business records. "
            "Resolution involves applying exclusive and regular use tests, principal place analysis, and documenting expenses."
        ),
        key_factors=[
            "Space is used exclusively for business",
            "Space is used regularly for business",
            "Space is principal place of business",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §280A(c)",
            "Treas. Reg. §1.280A-2",
            "Commissioner v. Soliman, 506 U.S. 168 (1993)"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert space is not exclusive or principal place",
        counter_arguments=[
            "Space is not used exclusively for business",
            "Space is not used regularly",
            "Space is not principal place of business",
            "Insufficient substantiation",
            "Improper classification"
        ],
        resolution_strategy="Apply exclusive and regular use tests, principal place analysis, and document expenses.",
        entity_scope="Individuals, businesses",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Commissioner v. Soliman, 506 U.S. 168 (1993)"
    ),
    DoctrineBlock(
        doctrine_id="D17",
        topic="§280E Marijuana Business Limitation",
        keywords=["marijuana", "business", "deduction", "COGS", "limitation", "illegal", "controlled substance"],
        conclusion_template="IRC §280E disallows deductions for businesses trafficking in controlled substances, except for cost of goods sold (COGS).",
        reasoning_framework=(
            "IRC §280E disallows deductions or credits for businesses trafficking in controlled substances prohibited by federal law. "
            "Only COGS is allowed as a reduction of gross income. "
            "Treas. Reg. §1.280E-1 and IRS guidance clarify application. "
            "Key factors include business activity, classification as controlled substance, and COGS computation. "
            "Audit defense requires documentation of COGS and business activity. "
            "Resolution involves applying §280E limitation, segregating COGS, and substantiating business operations."
        ),
        key_factors=[
            "Business traffics in controlled substances",
            "Deduction is disallowed except for COGS",
            "Proper computation of COGS",
            "Adequate substantiation",
            "Business activity documented"
        ],
        primary_authority=[
            "IRC §280E",
            "Treas. Reg. §1.280E-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper COGS computation or deduction",
        counter_arguments=[
            "Business is not eligible for deduction under §280E",
            "Improper computation of COGS",
            "Insufficient substantiation",
            "Deduction claimed for disallowed expenses",
            "Improper classification of business activity"
        ],
        resolution_strategy="Apply §280E limitation, segregate COGS, and document business activity.",
        entity_scope="Businesses",
        confidence=0.80,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §280E"
    ),
    DoctrineBlock(
        doctrine_id="D18",
        topic="§280F Luxury Auto Limitations",
        keywords=["luxury auto", "depreciation", "limitation", "deduction", "vehicle", "MACRS", "business"],
        conclusion_template="Depreciation deduction for luxury automobiles is limited under IRC §280F. Annual caps apply to MACRS deductions for vehicles exceeding price thresholds.",
        reasoning_framework=(
            "IRC §280F(a) limits depreciation deduction for passenger automobiles exceeding price thresholds. "
            "MACRS deductions are capped annually, with inflation adjustments. "
            "Treas. Reg. §1.280F-1 provides computational rules and substantiation requirements. "
            "Key factors include vehicle classification, business use percentage, and proper application of caps. "
            "Audit defense requires vehicle records, purchase documentation, and business use logs. "
            "Resolution involves applying annual caps, verifying business use, and documenting vehicle expenses."
        ),
        key_factors=[
            "Vehicle qualifies as passenger automobile",
            "Depreciation deduction is subject to annual caps",
            "Business use percentage applied",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §280F(a)",
            "Treas. Reg. §1.280F-1"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper classification or excessive deduction",
        counter_arguments=[
            "Vehicle does not qualify as passenger automobile",
            "Depreciation exceeds annual caps",
            "Improper business use percentage",
            "Insufficient substantiation",
            "Improper classification"
        ],
        resolution_strategy="Apply annual caps, verify business use, and document vehicle expenses.",
        entity_scope="Businesses",
        confidence=0.83,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §280F(a)"
    ),
    DoctrineBlock(
        doctrine_id="D19",
        topic="§274 Entertainment and Meal Limitations",
        keywords=["entertainment", "meal", "deduction", "limitation", "50%", "business", "substantiation"],
        conclusion_template="IRC §274 disallows deduction for entertainment expenses and limits meal deductions to 50%. Substantiation is required for all expenses.",
        reasoning_framework=(
            "IRC §274(a) disallows deduction for entertainment expenses. "
            "Meal expenses are limited to 50% deduction under §274(n). "
            "Treas. Reg. §1.274-2 and IRS guidance clarify definitions and substantiation requirements. "
            "Key factors include expense classification, business purpose, and substantiation. "
            "Audit defense requires receipts, logs, and business purpose documentation. "
            "Resolution involves applying limitations, verifying business purpose, and documenting expenses."
        ),
        key_factors=[
            "Expense is properly classified as meal or entertainment",
            "Entertainment expenses are disallowed",
            "Meal expenses limited to 50%",
            "Adequate substantiation",
            "Business purpose documented"
        ],
        primary_authority=[
            "IRC §274(a)",
            "IRC §274(n)",
            "Treas. Reg. §1.274-2"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert improper classification or lack of substantiation",
        counter_arguments=[
            "Expense is entertainment and not deductible",
            "Meal deduction exceeds 50%",
            "Insufficient substantiation",
            "Improper classification",
            "Business purpose not documented"
        ],
        resolution_strategy="Apply entertainment and meal limitations, verify business purpose, and document expenses.",
        entity_scope="Businesses",
        confidence=0.85,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §274(a)"
    ),
    DoctrineBlock(
        doctrine_id="D20",
        topic="§183 Hobby Loss Rules",
        keywords=["hobby", "loss", "deduction", "Cohan rule", "9-factor", "business", "activity", "substantiation"],
        conclusion_template="Hobby losses are not deductible under IRC §183 unless activity is engaged for profit. The 9-factor test and Cohan rule may be applied to determine business status and estimate expenses.",
        reasoning_framework=(
            "IRC §183 disallows deduction for activities not engaged for profit. "
            "The 9-factor test from Treas. Reg. §1.183-2(b) is used to determine profit motive. "
            "The Cohan rule allows reasonable estimation of expenses if records are incomplete. "
            "Key factors include taxpayer intent, activity history, income/expense patterns, and substantiation. "
            "Audit defense requires documentation of profit motive, activity records, and reasonable estimation. "
            "Resolution involves applying 9-factor test, Cohan rule, and substantiating activity."
        ),
        key_factors=[
            "Activity is engaged for profit",
            "9-factor test applied",
            "Reasonable estimation of expenses",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §183",
            "Treas. Reg. §1.183-2(b)",
            "Cohan v. Commissioner, 39 F.2d 540 (2d Cir. 1930)"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert activity is hobby and losses are not deductible",
        counter_arguments=[
            "Activity lacks profit motive",
            "9-factor test indicates hobby",
            "Insufficient substantiation",
            "Improper estimation of expenses",
            "Improper classification"
        ],
        resolution_strategy="Apply 9-factor test, Cohan rule, and document activity and expenses.",
        entity_scope="Individuals, businesses",
        confidence=0.81,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Treas. Reg. §1.183-2(b)"
    ),
    DoctrineBlock(
        doctrine_id="D21",
        topic="Economic Substance Doctrine",
        keywords=["economic substance", "doctrine", "deduction", "transaction", "business purpose", "audit", "limitation"],
        conclusion_template="Deductions may be disallowed if the transaction lacks economic substance under IRC §7701(o). Both objective and subjective tests must be satisfied.",
        reasoning_framework=(
            "IRC §7701(o) codifies the economic substance doctrine, requiring that transactions have a substantial purpose and a meaningful economic effect apart from tax benefits. "
            "Both objective (economic effect) and subjective (business purpose) tests must be satisfied. "
            "Treas. Reg. §1.7701-1 and case law (Frank Lyon Co. v. United States, 435 U.S. 561 (1978)) provide guidance. "
            "Key factors include transaction structure, business purpose, economic effect, and substantiation. "
            "Audit defense requires documentation of business purpose and economic effect. "
            "Resolution involves applying both tests, substantiating transaction, and referencing relevant precedents."
        ),
        key_factors=[
            "Transaction has substantial business purpose",
            "Transaction has meaningful economic effect",
            "Both objective and subjective tests applied",
            "Adequate substantiation",
            "Proper classification"
        ],
        primary_authority=[
            "IRC §7701(o)",
            "Treas. Reg. §1.7701-1",
            "Frank Lyon Co. v. United States, 435 U.S. 561 (1978)"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert transaction lacks economic substance",
        counter_arguments=[
            "Transaction lacks business purpose",
            "Transaction lacks economic effect",
            "Insufficient substantiation",
            "Improper classification",
            "Transaction is a sham"
        ],
        resolution_strategy="Apply economic substance tests, document business purpose and effect, and reference precedents.",
        entity_scope="Individuals, businesses",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="IRC §7701(o)"
    ),
    # ... (Add 9 more DoctrineBlocks for full coverage, omitted for brevity)
]

# AUTHORITY HARDENING

AUTHORITY_WEIGHT = {
    "IRC": 5,
    "Treas. Reg.": 4,
    "Rev Rul": 3,
    "CCA": 2,
    "PLR": 1
}

def resolve_authority_conflict(authorities: List[str]) -> List[str]:
    weighted = [(AUTHORITY_WEIGHT.get(a.split()[0], 0), a) for a in authorities]
    weighted.sort(reverse=True)
    return [a for _, a in weighted]

# SEMANTIC NORMALIZATION

SEMANTIC_MAP = {
    "SALT": "state and local tax",
    "NOL": "net operating loss",
    "QBI": "qualified business income",
    "ATI": "adjusted taxable income",
    "SSTB": "specified service trade or business",
    "COGS": "cost of goods sold",
    "MACRS": "modified accelerated cost recovery system",
    "UBIA": "unadjusted basis immediately after acquisition",
    "TCJA": "Tax Cuts and Jobs Act",
    "AGI": "adjusted gross income",
    "PLR": "private letter ruling",
    "CCA": "chief counsel advice",
    "Rev Rul": "revenue ruling",
    "bonus depreciation": "§168(k) bonus depreciation",
    "carryforward": "carryforward of deduction",
    "carryback": "carryback of deduction",
    "phase-out": "phase-out limitation",
    "expensing": "immediate expensing",
    "amortization": "systematic deduction over time",
    "exclusive use": "exclusive use test",
    "regular use": "regular use test",
    "principal place": "principal place of business",
    "substantiation": "adequate documentation",
    "deduction": "tax deduction",
    "limitation": "statutory limitation",
    "audit": "IRS audit",
    "defense": "audit defense",
    "business purpose": "substantial business purpose",
    "economic effect": "meaningful economic effect",
    "sham": "sham transaction",
    "estimation": "reasonable estimation",
    "9-factor": "9-factor test",
    "Cohan rule": "Cohan v. Commissioner estimation rule"
}

def normalize_terms(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# EPISTEMIC GUARDRAILS

BANNED_PHRASES = [
    "always",
    "never",
    "guaranteed",
    "certainly",
    "without exception",
    "cannot fail",
    "will not be challenged"
]

def apply_epistemic_guardrails(conclusion: str) -> str:
    for phrase in BANNED_PHRASES:
        conclusion = conclusion.replace(phrase, "")
    return conclusion

# FACT FRAGILITY SCORING

def score_fact_fragility(conclusion: str) -> float:
    verifiability = 1.0 if "substantiation" in conclusion or "documentation" in conclusion else 0.5
    recharacterization_risk = 0.7 if "classification" in conclusion or "recharacterized" in conclusion else 0.3
    testimony_dependence = 0.5 if "testimony" in conclusion or "estimation" in conclusion else 0.2
    return round((verifiability + recharacterization_risk + testimony_dependence) / 3, 2)

# THREE-LAYER RESPONSE

def doctrine_cache_lookup(scenario: str) -> Optional[DoctrineBlock]:
    for block in doctrine_cache:
        for kw in block.keywords:
            if kw.lower() in scenario.lower():
                return block
    return None

def semantic_search(scenario: str) -> Optional[DoctrineBlock]:
    scenario_norm = normalize_terms(scenario.lower())
    for block in doctrine_cache:
        for kw in block.keywords:
            if normalize_terms(kw.lower()) in scenario_norm:
                return block
    return None

def deep_analysis(scenario: str) -> List[DoctrineBlock]:
    results = []
    scenario_norm = normalize_terms(scenario.lower())
    for block in doctrine_cache:
        for kw in block.keywords:
            if normalize_terms(kw.lower()) in scenario_norm:
                results.append(block)
    return results

# DEEP ANALYSIS: MULTI-DOCTRINE DECOMPOSITION

def multi_doctrine_decomposition(scenario: str, issue_categories: List[IssueCategory]) -> Dict[str, Any]:
    interaction_dag = {}
    triggered = []
    missed = []
    epistemic_gaps = []
    for block in doctrine_cache:
        matched = False
        for kw in block.keywords:
            if kw.lower() in scenario.lower():
                triggered.append(block.doctrine_id)
                matched = True
                break
        if not matched:
            missed.append(block.doctrine_id)
    # 8-step resolution
    steps = [
        "Identify relevant IRC section",
        "Determine taxpayer eligibility",
        "Apply statutory limitation",
        "Classify expense or deduction",
        "Aggregate deductions if applicable",
        "Apply substantiation requirements",
        "Analyze audit risk and defense",
        "Resolve conflicts with authority hardening"
    ]
    for did in triggered:
        interaction_dag[did] = steps
    return {
        "interaction_dag": interaction_dag,
        "triggered": triggered,
        "missed": missed,
        "epistemic_gaps": epistemic_gaps
    }

# COVERAGE MAP

coverage_map = {
    "triggered": [],
    "missed": [],
    "epistemic_gaps": []
}

def update_coverage_map(triggered: List[str], missed: List[str], epistemic_gaps: List[str]):
    coverage_map["triggered"] = triggered
    coverage_map["missed"] = missed
    coverage_map["epistemic_gaps"] = epistemic_gaps

# DRIFT WATCHER

baseline_hash = hashlib.sha256(json.dumps([db.doctrine_id for db in doctrine_cache]).encode()).hexdigest()

def detect_drift() -> str:
    current_hash = hashlib.sha256(json.dumps([db.doctrine_id for db in doctrine_cache]).encode()).hexdigest()
    return "NO_DRIFT" if current_hash == baseline_hash else "DRIFT_DETECTED"

# AUDIT TRAIL

AUDIT_TRAIL_PATH = Path(__file__).resolve().parent / "audit_trail.jsonl"

def log_audit_trail(query_id: str, request: dict, response: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "request": request,
        "response": response
    }
    with open(AUDIT_TRAIL_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# DETERMINISM HASH

def determinism_hash(response: dict) -> str:
    return hashlib.sha256(json.dumps(response, sort_keys=True).encode()).hexdigest()

# FASTAPI APP

app = FastAPI(title="Deduction Analyzer Engine", version="TX02", port=8502)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Deduction Analyzer Engine TX02 startup.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Deduction Analyzer Engine TX02 shutdown.")

@app.post("/query")
async def query(request: QueryRequest):
    start_time = datetime.utcnow()
    query_id = str(uuid.uuid4())
    doctrine_ids = []
    triggered_doctrines = []
    missed_doctrines = []
    epistemic_gaps = []
    audit_trail_id = query_id
    drift_status = detect_drift()
    position_zone = PositionZone.PLANNING
    confidence_zone = ConfidenceZone.DEFENSIBLE
    primary_conclusion = ""
    reasoning_framework = ""
    key_factors = []
    primary_authority = []
    counter_arguments = []
    resolution_strategy = ""
    doctrine_blocks = []
    coverage = {}
    # Layer 1: Doctrine cache lookup
    block = doctrine_cache_lookup(request.scenario)
    if block:
        doctrine_blocks = [block]
        doctrine_ids = [block.doctrine_id]
        triggered_doctrines = doctrine_ids
        missed_doctrines = [db.doctrine_id for db in doctrine_cache if db.doctrine_id not in doctrine_ids]
        epistemic_gaps = []
        position_zone = PositionZone.REPORTING
        confidence_zone = block.confidence_zone
        primary_conclusion = apply_epistemic_guardrails(block.conclusion_template)
        reasoning_framework = normalize_terms(block.reasoning_framework)
        key_factors = block.key_factors
        primary_authority = resolve_authority_conflict(block.primary_authority)
        counter_arguments = block.counter_arguments
        resolution_strategy = block.resolution_strategy
    else:
        # Layer 2: Semantic search
        block = semantic_search(request.scenario)
        if block:
            doctrine_blocks = [block]
            doctrine_ids = [block.doctrine_id]
            triggered_doctrines = doctrine_ids
            missed_doctrines = [db.doctrine_id for db in doctrine_cache if db.doctrine_id not in doctrine_ids]
            epistemic_gaps = []
            position_zone = PositionZone.PLANNING
            confidence_zone = block.confidence_zone
            primary_conclusion = apply_epistemic_guardrails(block.conclusion_template)
            reasoning_framework = normalize_terms(block.reasoning_framework)
            key_factors = block.key_factors
            primary_authority = resolve_authority_conflict(block.primary_authority)
            counter_arguments = block.counter_arguments
            resolution_strategy = block.resolution_strategy
        else:
            # Layer 3: Deep analysis
            doctrine_blocks = deep_analysis(request.scenario)
            doctrine_ids = [db.doctrine_id for db in doctrine_blocks]
            triggered_doctrines = doctrine_ids
            missed_doctrines = [db.doctrine_id for db in doctrine_cache if db.doctrine_id not in doctrine_ids]
            epistemic_gaps = []
            position_zone = PositionZone.AUDIT
            confidence_zone = ConfidenceZone.DISCLOSURE
            primary_conclusion = "Multiple deduction doctrines may apply. Detailed analysis required."
            reasoning_framework = "Scenario triggers multiple deduction doctrines. Apply multi-doctrine decomposition, analyze interaction DAG, and resolve using 8-step resolution."
            key_factors = []
            primary_authority = []
            counter_arguments = []
            resolution_strategy = "Apply multi-doctrine decomposition, resolve conflicts, and document audit defense."
    coverage = multi_doctrine_decomposition(request.scenario, list(IssueCategory))
    update_coverage_map(coverage["triggered"], coverage["missed"], coverage["epistemic_gaps"])
    latency_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    metrics_collector.record_query(doctrine_ids, latency_ms)
    response_dict = {
        "engine_id": "TX02",
        "query_id": query_id,
        "mode": request.mode,
        "confidence": 0.95 if doctrine_blocks else 0.75,
        "confidence_zone": confidence_zone,
        "position_zone": position_zone,
        "primary_conclusion": primary_conclusion,
        "reasoning_framework": reasoning_framework,
        "key_factors": key_factors,
        "primary_authority": primary_authority,
        "counter_arguments": counter_arguments,
        "resolution_strategy": resolution_strategy,
        "determinism_hash": "",
        "doctrine_ids": doctrine_ids,
        "triggered_doctrines": triggered_doctrines,
        "missed_doctrines": missed_doctrines,
        "epistemic_gaps": epistemic_gaps,
        "audit_trail_id": audit_trail_id,
        "coverage_map": coverage,
        "drift_status": drift_status
    }
    response_dict["determinism_hash"] = determinism_hash(response_dict)
    log_audit_trail(query_id, request.dict(), response_dict)
    return QueryResponse(**response_dict)

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "TX02", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage():
    return coverage_map

@app.get("/drift")
async def drift():
    return {"drift_status": detect_drift()}

@app.get("/doctrines")
async def doctrines():
    return [db.__dict__ for db in doctrine_cache]
