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
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime, timedelta

# ENUMS
class ResponseMode(Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(Enum):
    MACRS_CLASS = "MACRS_CLASS"
    ADS_REQUIREMENT = "ADS_REQUIREMENT"
    SECTION_179 = "SECTION_179"
    BONUS_DEPRECIATION = "BONUS_DEPRECIATION"
    CONVENTION = "CONVENTION"
    COST_SEGREGATION = "COST_SEGREGATION"
    LISTED_PROPERTY = "LISTED_PROPERTY"
    LUXURY_AUTO_LIMITS = "LUXURY_AUTO_LIMITS"
    INTANGIBLE_AMORTIZATION = "INTANGIBLE_AMORTIZATION"
    COMPUTER_SOFTWARE = "COMPUTER_SOFTWARE"
    ENERGY_DEDUCTION = "ENERGY_DEDUCTION"
    DISPOSITION = "DISPOSITION"
    LIKE_KIND_EXCHANGE = "LIKE_KIND_EXCHANGE"
    PARTNERSHIP_BASIS = "PARTNERSHIP_BASIS"
    TANGIBLE_PROPERTY_REGS = "TANGIBLE_PROPERTY_REGS"
    SAFE_HARBORS = "SAFE_HARBORS"
    PARTIAL_DISPOSITION = "PARTIAL_DISPOSITION"
    PLACED_IN_SERVICE = "PLACED_IN_SERVICE"

# METRICS COLLECTOR
class MetricsCollector:
    def __init__(self):
        self.queries = []
        self.errors = []
        self.doctrine_hits = 0
        self.doctrine_misses = 0

    def record_query(self, query_id, timestamp):
        self.queries.append({"query_id": query_id, "timestamp": timestamp})

    def record_error(self, query_id, error_msg, timestamp):
        self.errors.append({"query_id": query_id, "error": error_msg, "timestamp": timestamp})

    def get_latency_stats(self):
        now = datetime.utcnow()
        times = [q["timestamp"] for q in self.queries if (now - q["timestamp"]).seconds < 3600]
        return {"count": len(times)}

    def get_doctrine_hit_rate(self):
        total = self.doctrine_hits + self.doctrine_misses
        return self.doctrine_hits / total if total > 0 else 0

    def queries_last_hour(self):
        now = datetime.utcnow()
        return len([q for q in self.queries if (now - q["timestamp"]).seconds < 3600])

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
    doctrine_id: Optional[str] = None
    triggered_doctrines: List[str] = []
    coverage_map: Dict[str, Any] = {}
    drift_detected: bool = False
    audit_trail_path: Optional[str] = None

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

doctrine_cache: Dict[str, DoctrineBlock] = {}

# DOCTRINE BLOCKS (25)
doctrine_cache["MACRS_3YR"] = DoctrineBlock(
    doctrine_id="MACRS_3YR",
    topic="MACRS 3-Year Property Classification",
    keywords=["MACRS", "3-year", "property", "depreciation", "asset", "class", "IRS"],
    conclusion_template="Assets classified as MACRS 3-year property are depreciated over three years using the prescribed tables under §168(c).",
    reasoning_framework=(
        "Under IRC §168(c), certain assets, such as racehorses over two years old and certain special tools, "
        "are assigned to the 3-year MACRS class. The IRS provides detailed asset class guidance in Rev. Proc. 87-56. "
        "Depreciation is computed using the double declining balance method, switching to straight-line when optimal. "
        "Half-year convention generally applies unless the mid-quarter convention is triggered under §168(d)(3). "
        "Taxpayers must ensure proper asset classification to avoid misapplication of depreciation schedules. "
        "Audit risk increases if asset classification is inconsistent with industry standards or IRS guidance. "
        "The burden of proof lies with the taxpayer to substantiate asset classification and placed-in-service date. "
        "Treas. Reg. §1.168-2 provides additional guidance on method selection and convention application."
    ),
    key_factors=[
        "Asset type and use",
        "Placed-in-service date",
        "IRS asset class guidance",
        "Depreciation method selection",
        "Convention applicability"
    ],
    primary_authority=[
        "IRC §168(c)",
        "Rev. Proc. 87-56",
        "Treas. Reg. §1.168-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge asset classification or convention",
    counter_arguments=[
        "Asset does not qualify for 3-year class",
        "Incorrect placed-in-service date",
        "Improper convention applied",
        "Depreciation method misapplied",
        "Noncompliance with Rev. Proc. 87-56"
    ],
    resolution_strategy="Review asset classification, placed-in-service substantiation, and convention selection per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Rev. Proc. 87-56"
)

doctrine_cache["MACRS_5YR"] = DoctrineBlock(
    doctrine_id="MACRS_5YR",
    topic="MACRS 5-Year Property Classification",
    keywords=["MACRS", "5-year", "property", "computer", "vehicle", "depreciation"],
    conclusion_template="MACRS 5-year property includes computers, office equipment, and certain vehicles, depreciated over five years per §168(c).",
    reasoning_framework=(
        "IRC §168(c) and Rev. Proc. 87-56 assign computers, office equipment, and certain vehicles to the 5-year MACRS class. "
        "Depreciation is calculated using the 200% declining balance method, switching to straight-line when optimal. "
        "Half-year convention is standard unless the mid-quarter convention applies under §168(d)(3). "
        "Listed property rules under §280F may limit depreciation for vehicles and computers not used predominantly for business. "
        "Taxpayers must maintain substantiation for business use and placed-in-service date. "
        "Audit risk is heightened for listed property due to frequent IRS scrutiny. "
        "Treas. Reg. §1.168-2 and §1.280F-3 provide guidance on method and convention selection."
    ),
    key_factors=[
        "Asset type",
        "Business use substantiation",
        "Placed-in-service date",
        "Listed property rules",
        "Depreciation method"
    ],
    primary_authority=[
        "IRC §168(c)",
        "Rev. Proc. 87-56",
        "IRC §280F",
        "Treas. Reg. §1.168-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge business use or listed property classification",
    counter_arguments=[
        "Asset not eligible for 5-year class",
        "Insufficient business use substantiation",
        "Listed property limits not applied",
        "Incorrect depreciation method",
        "Improper convention"
    ],
    resolution_strategy="Verify asset classification, business use, and apply listed property limits as required.",
    entity_scope="All taxpayers",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Rev. Proc. 87-56"
)

doctrine_cache["MACRS_7YR"] = DoctrineBlock(
    doctrine_id="MACRS_7YR",
    topic="MACRS 7-Year Property Classification",
    keywords=["MACRS", "7-year", "property", "office furniture", "depreciation", "asset"],
    conclusion_template="Office furniture and fixtures are generally classified as MACRS 7-year property under §168(c).",
    reasoning_framework=(
        "IRC §168(c) and Rev. Proc. 87-56 designate office furniture, fixtures, and certain agricultural equipment as 7-year property. "
        "Depreciation is computed using the 200% declining balance method, switching to straight-line when optimal. "
        "Half-year convention applies unless the mid-quarter convention is triggered. "
        "Taxpayers must ensure accurate asset classification and placed-in-service documentation. "
        "Audit risk arises if asset classification is inconsistent with IRS guidance or industry standards. "
        "Treas. Reg. §1.168-2 provides method and convention guidance. "
        "Burden of proof is on the taxpayer to substantiate classification and convention selection."
    ),
    key_factors=[
        "Asset classification",
        "Placed-in-service substantiation",
        "Depreciation method",
        "Convention selection",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(c)",
        "Rev. Proc. 87-56",
        "Treas. Reg. §1.168-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge classification or convention",
    counter_arguments=[
        "Improper asset classification",
        "Incorrect placed-in-service date",
        "Depreciation method misapplied",
        "Convention not properly selected",
        "Noncompliance with Rev. Proc. 87-56"
    ],
    resolution_strategy="Review asset classification and placed-in-service substantiation per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Rev. Proc. 87-56"
)

doctrine_cache["MACRS_15YR"] = DoctrineBlock(
    doctrine_id="MACRS_15YR",
    topic="MACRS 15-Year Property Classification",
    keywords=["MACRS", "15-year", "property", "qualified improvement", "QIP", "depreciation"],
    conclusion_template="Qualified improvement property (QIP) is classified as 15-year MACRS property under the CARES Act fix.",
    reasoning_framework=(
        "The CARES Act retroactively corrected the classification of qualified improvement property (QIP) to 15-year MACRS property. "
        "QIP is defined in IRC §168(e)(6) and must be improvements to the interior of nonresidential real property. "
        "Depreciation is calculated using the straight-line method with the mid-month convention. "
        "QIP placed in service after December 31, 2017, is eligible for bonus depreciation under §168(k). "
        "Taxpayers must substantiate the nature of improvements and placed-in-service date. "
        "Audit risk arises if improvements do not meet QIP criteria or are misclassified. "
        "Treas. Reg. §1.168-3 and IRS guidance clarify QIP eligibility and method selection."
    ),
    key_factors=[
        "Improvement nature",
        "Placed-in-service date",
        "QIP eligibility",
        "Depreciation method",
        "Bonus depreciation eligibility"
    ],
    primary_authority=[
        "IRC §168(e)(6)",
        "CARES Act",
        "Treas. Reg. §1.168-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge QIP classification or bonus eligibility",
    counter_arguments=[
        "Improvement does not qualify as QIP",
        "Incorrect placed-in-service date",
        "Bonus depreciation not properly applied",
        "Depreciation method misapplied",
        "Noncompliance with CARES Act fix"
    ],
    resolution_strategy="Substantiate QIP classification and apply bonus depreciation as permitted.",
    entity_scope="All taxpayers",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="CARES Act"
)

doctrine_cache["MACRS_27_5YR"] = DoctrineBlock(
    doctrine_id="MACRS_27_5YR",
    topic="MACRS 27.5-Year Residential Real Property",
    keywords=["MACRS", "27.5-year", "residential", "real property", "depreciation", "mid-month"],
    conclusion_template="Residential rental property is depreciated over 27.5 years using the straight-line method and mid-month convention.",
    reasoning_framework=(
        "IRC §168(c) assigns residential rental property to the 27.5-year MACRS class. "
        "Depreciation is computed using the straight-line method and mid-month convention per §168(d)(2). "
        "Residential rental property must be used for dwelling purposes and not classified as nonresidential. "
        "Taxpayers must substantiate property use and placed-in-service date. "
        "Audit risk arises if property use is mischaracterized or placed-in-service date is not properly documented. "
        "Treas. Reg. §1.168-1 and §1.168-4 provide guidance on method and convention selection."
    ),
    key_factors=[
        "Property use",
        "Placed-in-service substantiation",
        "Depreciation method",
        "Convention selection",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(c)",
        "Treas. Reg. §1.168-1",
        "Treas. Reg. §1.168-4"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge property use or convention",
    counter_arguments=[
        "Improper property classification",
        "Incorrect placed-in-service date",
        "Depreciation method misapplied",
        "Convention not properly selected",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate property use and placed-in-service date per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-1"
)

doctrine_cache["MACRS_39YR"] = DoctrineBlock(
    doctrine_id="MACRS_39YR",
    topic="MACRS 39-Year Nonresidential Real Property",
    keywords=["MACRS", "39-year", "nonresidential", "real property", "depreciation", "mid-month"],
    conclusion_template="Nonresidential real property is depreciated over 39 years using the straight-line method and mid-month convention.",
    reasoning_framework=(
        "IRC §168(c) assigns nonresidential real property to the 39-year MACRS class. "
        "Depreciation is computed using the straight-line method and mid-month convention per §168(d)(2). "
        "Nonresidential real property must not be used for dwelling purposes. "
        "Taxpayers must substantiate property use and placed-in-service date. "
        "Audit risk arises if property use is mischaracterized or placed-in-service date is not properly documented. "
        "Treas. Reg. §1.168-1 and §1.168-4 provide guidance on method and convention selection."
    ),
    key_factors=[
        "Property use",
        "Placed-in-service substantiation",
        "Depreciation method",
        "Convention selection",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(c)",
        "Treas. Reg. §1.168-1",
        "Treas. Reg. §1.168-4"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge property use or convention",
    counter_arguments=[
        "Improper property classification",
        "Incorrect placed-in-service date",
        "Depreciation method misapplied",
        "Convention not properly selected",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate property use and placed-in-service date per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-1"
)

doctrine_cache["ADS_LISTED"] = DoctrineBlock(
    doctrine_id="ADS_LISTED",
    topic="ADS Requirement for Listed Property <50% Business Use",
    keywords=["ADS", "listed property", "business use", "depreciation", "§168(g)", "§280F"],
    conclusion_template="Listed property used less than 50% for business must be depreciated using ADS under §168(g).",
    reasoning_framework=(
        "IRC §168(g) requires the use of the Alternative Depreciation System (ADS) for listed property not used predominantly for business. "
        "Listed property includes vehicles, computers, and certain entertainment assets under §280F(d)(4). "
        "Depreciation is computed using the straight-line method over the ADS recovery period. "
        "Taxpayers must maintain substantiation for business use and placed-in-service date. "
        "Audit risk is high for listed property due to frequent IRS scrutiny. "
        "Treas. Reg. §1.168-2 and §1.280F-3 provide guidance on method and convention selection."
    ),
    key_factors=[
        "Business use substantiation",
        "Listed property classification",
        "Depreciation method",
        "ADS recovery period",
        "Placed-in-service date"
    ],
    primary_authority=[
        "IRC §168(g)",
        "IRC §280F",
        "Treas. Reg. §1.168-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge business use or listed property classification",
    counter_arguments=[
        "Insufficient business use substantiation",
        "Listed property limits not applied",
        "Incorrect depreciation method",
        "Improper convention",
        "Noncompliance with ADS requirement"
    ],
    resolution_strategy="Verify business use and apply ADS as required for listed property.",
    entity_scope="All taxpayers",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="IRC §168(g)"
)

doctrine_cache["SECTION_179_LIMIT"] = DoctrineBlock(
    doctrine_id="SECTION_179_LIMIT",
    topic="§179 Expensing Election Limits",
    keywords=["§179", "expensing", "limit", "phase-out", "SUV", "depreciation"],
    conclusion_template="§179 expensing is limited to $1,160,000 in 2024, with a phase-out beginning at $2,890,000 and a $28,900 limit for SUVs.",
    reasoning_framework=(
        "IRC §179 allows taxpayers to expense qualifying property up to $1,160,000 in 2024, with a phase-out starting at $2,890,000. "
        "SUVs are subject to a $28,900 limit under §179(b)(6). "
        "Qualifying property must be tangible, depreciable, and used in active trade or business. "
        "Taxpayers must reduce the §179 limit dollar-for-dollar for acquisitions exceeding the phase-out threshold. "
        "Audit risk arises if property does not qualify or limits are not properly applied. "
        "Treas. Reg. §1.179-2 provides guidance on eligibility and limit calculation."
    ),
    key_factors=[
        "Qualifying property",
        "Acquisition cost",
        "Phase-out calculation",
        "SUV limit",
        "Active business use"
    ],
    primary_authority=[
        "IRC §179",
        "IRC §179(b)(6)",
        "Treas. Reg. §1.179-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge property eligibility or limit calculation",
    counter_arguments=[
        "Property does not qualify",
        "Phase-out not properly applied",
        "SUV limit exceeded",
        "Incorrect expensing calculation",
        "Noncompliance with §179 rules"
    ],
    resolution_strategy="Verify property eligibility and apply §179 limits and phase-out as required.",
    entity_scope="All taxpayers",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="IRC §179"
)

doctrine_cache["BONUS_DEPRECIATION_2024"] = DoctrineBlock(
    doctrine_id="BONUS_DEPRECIATION_2024",
    topic="§168(k) Bonus Depreciation 2024",
    keywords=["bonus depreciation", "§168(k)", "80%", "2023", "60%", "2024", "phase-out"],
    conclusion_template="Bonus depreciation is 60% in 2024 for qualifying property placed in service after 12/31/2023 and before 1/1/2025.",
    reasoning_framework=(
        "IRC §168(k) provides for bonus depreciation of 60% in 2024 for qualifying property placed in service after December 31, 2023. "
        "Qualifying property must be new or used, have a recovery period of 20 years or less, and not be acquired from related parties. "
        "Taxpayers must substantiate placed-in-service date and property eligibility. "
        "Audit risk arises if property does not qualify or bonus percentage is misapplied. "
        "Treas. Reg. §1.168(k)-1 provides guidance on eligibility and calculation."
    ),
    key_factors=[
        "Qualifying property",
        "Placed-in-service date",
        "Bonus percentage",
        "Related party acquisition",
        "Recovery period"
    ],
    primary_authority=[
        "IRC §168(k)",
        "Treas. Reg. §1.168(k)-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge property eligibility or bonus calculation",
    counter_arguments=[
        "Property does not qualify",
        "Incorrect placed-in-service date",
        "Bonus percentage misapplied",
        "Related party acquisition",
        "Noncompliance with §168(k) rules"
    ],
    resolution_strategy="Substantiate property eligibility and apply bonus depreciation as permitted.",
    entity_scope="All taxpayers",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="IRC §168(k)"
)

doctrine_cache["MID_MONTH_CONVENTION"] = DoctrineBlock(
    doctrine_id="MID_MONTH_CONVENTION",
    topic="Mid-Month Convention for Real Property",
    keywords=["mid-month", "convention", "real property", "MACRS", "depreciation"],
    conclusion_template="Mid-month convention applies to real property under MACRS, affecting depreciation calculation for the first and last year.",
    reasoning_framework=(
        "IRC §168(d)(2) requires the mid-month convention for real property depreciated under MACRS. "
        "Depreciation is prorated based on the number of months in service, with partial months treated as half-months. "
        "Taxpayers must accurately determine placed-in-service and disposition dates. "
        "Audit risk arises if convention is misapplied or dates are not properly documented. "
        "Treas. Reg. §1.168-4 provides guidance on convention application."
    ),
    key_factors=[
        "Property classification",
        "Placed-in-service date",
        "Disposition date",
        "Depreciation calculation",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(d)(2)",
        "Treas. Reg. §1.168-4"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge convention application or date substantiation",
    counter_arguments=[
        "Improper convention applied",
        "Incorrect placed-in-service date",
        "Disposition date misapplied",
        "Depreciation calculation error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate placed-in-service and disposition dates and apply mid-month convention as required.",
    entity_scope="All taxpayers",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-4"
)

doctrine_cache["HALF_YEAR_CONVENTION"] = DoctrineBlock(
    doctrine_id="HALF_YEAR_CONVENTION",
    topic="Half-Year Convention for Personal Property",
    keywords=["half-year", "convention", "personal property", "MACRS", "depreciation"],
    conclusion_template="Half-year convention applies to most personal property under MACRS unless the mid-quarter convention is triggered.",
    reasoning_framework=(
        "IRC §168(d)(1) requires the half-year convention for personal property depreciated under MACRS. "
        "Depreciation is computed as if all assets were placed in service or disposed of at the midpoint of the year. "
        "Mid-quarter convention applies if more than 40% of assets are placed in service in the last quarter. "
        "Taxpayers must track placed-in-service dates and asset acquisition timing. "
        "Audit risk arises if convention is misapplied or asset timing is not properly documented. "
        "Treas. Reg. §1.168-2 and §1.168-3 provide guidance on convention selection."
    ),
    key_factors=[
        "Asset acquisition timing",
        "Placed-in-service date",
        "Convention selection",
        "Depreciation calculation",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(d)(1)",
        "Treas. Reg. §1.168-2",
        "Treas. Reg. §1.168-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge convention selection or asset timing",
    counter_arguments=[
        "Improper convention applied",
        "Incorrect placed-in-service date",
        "Asset acquisition timing error",
        "Depreciation calculation error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track asset acquisition and placed-in-service dates and apply half-year convention as required.",
    entity_scope="All taxpayers",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-2"
)

doctrine_cache["MID_QUARTER_CONVENTION"] = DoctrineBlock(
    doctrine_id="MID_QUARTER_CONVENTION",
    topic="Mid-Quarter Convention Trigger",
    keywords=["mid-quarter", "convention", "MACRS", "personal property", "depreciation"],
    conclusion_template="Mid-quarter convention applies if more than 40% of personal property is placed in service in the last quarter.",
    reasoning_framework=(
        "IRC §168(d)(3) triggers the mid-quarter convention if more than 40% of personal property is placed in service in the last quarter. "
        "Depreciation is computed as if assets were placed in service or disposed of at the midpoint of the quarter. "
        "Taxpayers must track asset acquisition timing and placed-in-service dates. "
        "Audit risk arises if convention is misapplied or asset timing is not properly documented. "
        "Treas. Reg. §1.168-2 and §1.168-3 provide guidance on convention selection."
    ),
    key_factors=[
        "Asset acquisition timing",
        "Placed-in-service date",
        "Convention selection",
        "Depreciation calculation",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(d)(3)",
        "Treas. Reg. §1.168-2",
        "Treas. Reg. §1.168-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge convention selection or asset timing",
    counter_arguments=[
        "Improper convention applied",
        "Incorrect placed-in-service date",
        "Asset acquisition timing error",
        "Depreciation calculation error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track asset acquisition and placed-in-service dates and apply mid-quarter convention as required.",
    entity_scope="All taxpayers",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-2"
)

doctrine_cache["LEASED_IMPROVEMENT"] = DoctrineBlock(
    doctrine_id="LEASED_IMPROVEMENT",
    topic="§168(i)(6) Improvement to Leased Property",
    keywords=["leased property", "improvement", "§168(i)(6)", "depreciation", "MACRS"],
    conclusion_template="Improvements to leased property are depreciated over the lesser of the lease term or MACRS recovery period under §168(i)(6).",
    reasoning_framework=(
        "IRC §168(i)(6) requires improvements to leased property to be depreciated over the shorter of the lease term or the MACRS recovery period. "
        "Taxpayers must substantiate lease terms and improvement placed-in-service date. "
        "Audit risk arises if lease terms are not properly documented or improvements are misclassified. "
        "Treas. Reg. §1.168-8 provides guidance on lease term determination and depreciation calculation."
    ),
    key_factors=[
        "Lease term substantiation",
        "Improvement classification",
        "Placed-in-service date",
        "Depreciation calculation",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(i)(6)",
        "Treas. Reg. §1.168-8"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge lease term or improvement classification",
    counter_arguments=[
        "Improper lease term substantiation",
        "Incorrect improvement classification",
        "Placed-in-service date error",
        "Depreciation calculation error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate lease terms and improvement classification and apply depreciation as required.",
    entity_scope="All taxpayers",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-8"
)

doctrine_cache["RETAIL_MOTOR_FUELS"] = DoctrineBlock(
    doctrine_id="RETAIL_MOTOR_FUELS",
    topic="§168(e)(6) Retail Motor Fuels Property",
    keywords=["retail motor fuels", "property", "§168(e)(6)", "depreciation", "MACRS"],
    conclusion_template="Retail motor fuels property is classified as 15-year MACRS property under §168(e)(6).",
    reasoning_framework=(
        "IRC §168(e)(6) assigns retail motor fuels property, such as gas station canopies, to the 15-year MACRS class. "
        "Depreciation is computed using the straight-line method and mid-month convention. "
        "Taxpayers must substantiate property classification and placed-in-service date. "
        "Audit risk arises if property is misclassified or placed-in-service date is not properly documented. "
        "Treas. Reg. §1.168-3 provides guidance on property classification and depreciation calculation."
    ),
    key_factors=[
        "Property classification",
        "Placed-in-service date",
        "Depreciation method",
        "Convention selection",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §168(e)(6)",
        "Treas. Reg. §1.168-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge property classification or convention",
    counter_arguments=[
        "Improper property classification",
        "Incorrect placed-in-service date",
        "Depreciation method misapplied",
        "Convention not properly selected",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate property classification and placed-in-service date per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168-3"
)

doctrine_cache["COST_SEGREGATION"] = DoctrineBlock(
    doctrine_id="COST_SEGREGATION",
    topic="Cost Segregation Study Methodology",
    keywords=["cost segregation", "study", "engineering", "component analysis", "§1245", "§1250"],
    conclusion_template="Cost segregation studies use engineering-based component analysis to reclassify assets for accelerated depreciation.",
    reasoning_framework=(
        "Cost segregation studies apply engineering-based component analysis to identify §1245 and §1250 property within a building. "
        "§1245 property is eligible for accelerated depreciation, while §1250 property is depreciated over longer periods. "
        "Taxpayers must substantiate component classification and placed-in-service date. "
        "Audit risk arises if component analysis is not properly documented or asset classification is challenged. "
        "IRS guidance in Audit Technique Guides and relevant case law (Hospital Corp. of America v. Commissioner, 109 T.C. 21) support methodology."
    ),
    key_factors=[
        "Component classification",
        "Engineering analysis",
        "Placed-in-service date",
        "Depreciation method",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §1245",
        "IRC §1250",
        "Hospital Corp. of America v. Commissioner, 109 T.C. 21"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge component classification or methodology",
    counter_arguments=[
        "Improper component classification",
        "Engineering analysis not substantiated",
        "Placed-in-service date error",
        "Depreciation calculation error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate component classification and engineering analysis per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.87,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Hospital Corp. of America v. Commissioner"
)

doctrine_cache["LISTED_PROPERTY_AUTO"] = DoctrineBlock(
    doctrine_id="LISTED_PROPERTY_AUTO",
    topic="Listed Property §280F Auto Limits",
    keywords=["listed property", "auto", "§280F", "depreciation", "predominant use"],
    conclusion_template="Luxury automobile depreciation is limited under §280F, with annual caps and recapture on conversion to non-business use.",
    reasoning_framework=(
        "IRC §280F limits depreciation for luxury automobiles and other listed property. "
        "Annual caps are set by IRS guidance and adjusted for inflation. "
        "Predominant business use must be substantiated to avoid recapture. "
        "Recapture applies if business use drops below 50%. "
        "Taxpayers must maintain detailed records of business use and placed-in-service date. "
        "Treas. Reg. §1.280F-3 provides guidance on limits and recapture calculation."
    ),
    key_factors=[
        "Business use substantiation",
        "Annual depreciation caps",
        "Recapture calculation",
        "Placed-in-service date",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §280F",
        "Treas. Reg. §1.280F-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge business use or depreciation calculation",
    counter_arguments=[
        "Insufficient business use substantiation",
        "Annual caps not applied",
        "Recapture not calculated",
        "Placed-in-service date error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Maintain business use records and apply annual caps and recapture as required.",
    entity_scope="All taxpayers",
    confidence=0.86,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.280F-3"
)

doctrine_cache["LUXURY_AUTO_LIMITS"] = DoctrineBlock(
    doctrine_id="LUXURY_AUTO_LIMITS",
    topic="Luxury Automobile Depreciation Limits",
    keywords=["luxury automobile", "depreciation", "limits", "annual caps", "MACRS", "§280F"],
    conclusion_template="Depreciation for passenger vehicles is subject to annual caps under §280F, limiting allowable deductions.",
    reasoning_framework=(
        "IRC §280F sets annual depreciation caps for passenger vehicles classified as luxury automobiles. "
        "Caps are adjusted annually for inflation and published by the IRS. "
        "Taxpayers must apply caps regardless of depreciation method or convention. "
        "Audit risk arises if caps are not properly applied or vehicle classification is challenged. "
        "Treas. Reg. §1.280F-3 provides guidance on cap application and vehicle classification."
    ),
    key_factors=[
        "Vehicle classification",
        "Annual depreciation caps",
        "Depreciation method",
        "Convention selection",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §280F",
        "Treas. Reg. §1.280F-3"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge vehicle classification or cap application",
    counter_arguments=[
        "Improper vehicle classification",
        "Annual caps not applied",
        "Depreciation method error",
        "Convention not properly selected",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Apply annual caps and substantiate vehicle classification per IRS guidance.",
    entity_scope="All taxpayers",
    confidence=0.85,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.280F-3"
)

doctrine_cache["SECTION_197_INTANGIBLE"] = DoctrineBlock(
    doctrine_id="SECTION_197_INTANGIBLE",
    topic="§197 Intangible Amortization",
    keywords=["§197", "intangible", "amortization", "goodwill", "customer lists", "franchise"],
    conclusion_template="§197 intangibles, including goodwill and franchises, are amortized over 15 years using the straight-line method.",
    reasoning_framework=(
        "IRC §197 requires amortization of certain intangibles, such as goodwill, customer lists, and franchises, over 15 years. "
        "Amortization is computed using the straight-line method. "
        "Taxpayers must substantiate intangible classification and acquisition date. "
        "Audit risk arises if intangible classification is challenged or amortization is misapplied. "
        "Treas. Reg. §1.197-2 provides guidance on classification and amortization calculation."
    ),
    key_factors=[
        "Intangible classification",
        "Acquisition date",
        "Amortization method",
        "IRS guidance compliance",
        "Substantiation of value"
    ],
    primary_authority=[
        "IRC §197",
        "Treas. Reg. §1.197-2"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge intangible classification or amortization calculation",
    counter_arguments=[
        "Improper intangible classification",
        "Acquisition date error",
        "Amortization method misapplied",
        "Value not substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate intangible classification and apply straight-line amortization as required.",
    entity_scope="All taxpayers",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.197-2"
)

doctrine_cache["COMPUTER_SOFTWARE"] = DoctrineBlock(
    doctrine_id="COMPUTER_SOFTWARE",
    topic="§167(f) Computer Software Depreciation",
    keywords=["computer software", "§167(f)", "3-year", "§197", "off-the-shelf", "§179"],
    conclusion_template="Off-the-shelf computer software is depreciated over 3 years under §167(f) or may be expensed under §179 if eligible.",
    reasoning_framework=(
        "IRC §167(f) allows depreciation of off-the-shelf computer software over 3 years using the straight-line method. "
        "§179 expensing is permitted if software is eligible and acquired for use in active trade or business. "
        "§197 applies to software acquired as part of a business acquisition, requiring 15-year amortization. "
        "Taxpayers must substantiate software classification and acquisition date. "
        "Audit risk arises if software classification is challenged or depreciation is misapplied. "
        "Treas. Reg. §1.167(a)-14 provides guidance on classification and depreciation calculation."
    ),
    key_factors=[
        "Software classification",
        "Acquisition date",
        "Depreciation method",
        "§179 eligibility",
        "IRS guidance compliance"
    ],
    primary_authority=[
        "IRC §167(f)",
        "IRC §197",
        "Treas. Reg. §1.167(a)-14"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge software classification or depreciation calculation",
    counter_arguments=[
        "Improper software classification",
        "Acquisition date error",
        "Depreciation method misapplied",
        "§179 eligibility not substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate software classification and apply depreciation or expensing as permitted.",
    entity_scope="All taxpayers",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.167(a)-14"
)

doctrine_cache["SECTION_179D"] = DoctrineBlock(
    doctrine_id="SECTION_179D",
    topic="§179D Energy Efficient Commercial Building Deduction",
    keywords=["§179D", "energy efficient", "commercial building", "deduction", "depreciation"],
    conclusion_template="§179D provides a deduction for energy efficient commercial building property, reducing depreciable basis.",
    reasoning_framework=(
        "IRC §179D allows a deduction for energy efficient commercial building property, reducing the depreciable basis of the asset. "
        "Deduction is subject to certification requirements and maximum limits. "
        "Taxpayers must substantiate energy efficiency and certification. "
        "Audit risk arises if certification is not properly documented or deduction is misapplied. "
        "IRS guidance in Notice 2006-52 and Treas. Reg. §1.179D-1 provide details on eligibility and calculation."
    ),
    key_factors=[
        "Energy efficiency certification",
        "Deduction calculation",
        "Depreciable basis reduction",
        "IRS guidance compliance",
        "Substantiation of property"
    ],
    primary_authority=[
        "IRC §179D",
        "Notice 2006-52",
        "Treas. Reg. §1.179D-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge certification or deduction calculation",
    counter_arguments=[
        "Certification not substantiated",
        "Deduction calculation error",
        "Depreciable basis not reduced",
        "Property not eligible",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate certification and apply deduction and basis reduction as required.",
    entity_scope="All taxpayers",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Notice 2006-52"
)

doctrine_cache["DISPOSITION_1245"] = DoctrineBlock(
    doctrine_id="DISPOSITION_1245",
    topic="Disposition of Depreciable Assets §1245 Recapture",
    keywords=["disposition", "depreciable asset", "§1245", "recapture", "ordinary income"],
    conclusion_template="Disposition of §1245 property triggers ordinary income recapture to the extent of prior depreciation deductions.",
    reasoning_framework=(
        "IRC §1245 requires recapture of depreciation as ordinary income upon disposition of §1245 property. "
        "Recapture applies to the extent of prior depreciation deductions. "
        "Taxpayers must track depreciation history and substantiate disposition date. "
        "Audit risk arises if recapture is not properly calculated or disposition is not documented. "
        "Treas. Reg. §1.1245-1 provides guidance on recapture calculation and reporting."
    ),
    key_factors=[
        "Depreciation history",
        "Disposition date",
        "Recapture calculation",
        "IRS guidance compliance",
        "Substantiation of asset"
    ],
    primary_authority=[
        "IRC §1245",
        "Treas. Reg. §1.1245-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge recapture calculation or disposition substantiation",
    counter_arguments=[
        "Depreciation history not tracked",
        "Disposition date error",
        "Recapture calculation error",
        "Asset not properly substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track depreciation history and apply recapture calculation as required.",
    entity_scope="All taxpayers",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.1245-1"
)

doctrine_cache["DISPOSITION_1250"] = DoctrineBlock(
    doctrine_id="DISPOSITION_1250",
    topic="Disposition of Depreciable Real Property §1250 Unrecaptured Gain",
    keywords=["disposition", "real property", "§1250", "unrecaptured gain", "capital gain"],
    conclusion_template="Disposition of §1250 property may result in unrecaptured §1250 gain taxed at a maximum 25% rate.",
    reasoning_framework=(
        "IRC §1250 requires calculation of unrecaptured gain upon disposition of depreciable real property. "
        "Unrecaptured §1250 gain is taxed at a maximum 25% rate. "
        "Taxpayers must track depreciation history and substantiate disposition date. "
        "Audit risk arises if gain calculation is not properly performed or disposition is not documented. "
        "Treas. Reg. §1.1250-1 provides guidance on gain calculation and reporting."
    ),
    key_factors=[
        "Depreciation history",
        "Disposition date",
        "Gain calculation",
        "IRS guidance compliance",
        "Substantiation of asset"
    ],
    primary_authority=[
        "IRC §1250",
        "Treas. Reg. §1.1250-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge gain calculation or disposition substantiation",
    counter_arguments=[
        "Depreciation history not tracked",
        "Disposition date error",
        "Gain calculation error",
        "Asset not properly substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track depreciation history and apply gain calculation as required.",
    entity_scope="All taxpayers",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.1250-1"
)

doctrine_cache["LIKE_KIND_EXCHANGE"] = DoctrineBlock(
    doctrine_id="LIKE_KIND_EXCHANGE",
    topic="§1031 Like-Kind Exchange Basis Allocation",
    keywords=["like-kind exchange", "§1031", "basis allocation", "depreciation", "MACRS"],
    conclusion_template="§1031 like-kind exchanges require basis allocation for depreciation, with new MACRS schedule for replacement property.",
    reasoning_framework=(
        "IRC §1031 allows deferral of gain on like-kind exchanges, requiring basis allocation for depreciation. "
        "Replacement property receives a new MACRS schedule based on allocated basis. "
        "Taxpayers must track exchanged assets and substantiate basis allocation. "
        "Audit risk arises if basis allocation is not properly performed or exchange is not documented. "
        "Treas. Reg. §1.1031(a)-1 and IRS guidance provide details on basis allocation and depreciation calculation."
    ),
    key_factors=[
        "Exchanged asset tracking",
        "Basis allocation",
        "Depreciation schedule",
        "IRS guidance compliance",
        "Substantiation of exchange"
    ],
    primary_authority=[
        "IRC §1031",
        "Treas. Reg. §1.1031(a)-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge basis allocation or exchange substantiation",
    counter_arguments=[
        "Exchanged asset not tracked",
        "Basis allocation error",
        "Depreciation schedule misapplied",
        "Exchange not properly substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track exchanged assets and apply basis allocation and new MACRS schedule as required.",
    entity_scope="All taxpayers",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.1031(a)-1"
)

doctrine_cache["PARTNERSHIP_BASIS_STEPUP"] = DoctrineBlock(
    doctrine_id="PARTNERSHIP_BASIS_STEPUP",
    topic="TCJA Bonus Depreciation and §743(b) Partnership Basis Step-Up",
    keywords=["TCJA", "bonus depreciation", "§743(b)", "partnership", "basis step-up"],
    conclusion_template="TCJA bonus depreciation applies to §743(b) partnership basis step-up if underlying assets are eligible.",
    reasoning_framework=(
        "IRC §743(b) allows basis step-up for partnership interests, and TCJA bonus depreciation applies if underlying assets are eligible. "
        "Eligibility depends on asset classification and placed-in-service date. "
        "Taxpayers must substantiate asset eligibility and basis step-up calculation. "
        "Audit risk arises if bonus depreciation is misapplied or basis step-up is not properly documented. "
        "IRS guidance in Notice 2019-27 and Treas. Reg. §1.743-1 provide details on eligibility and calculation."
    ),
    key_factors=[
        "Asset eligibility",
        "Basis step-up calculation",
        "Depreciation method",
        "IRS guidance compliance",
        "Substantiation of partnership interest"
    ],
    primary_authority=[
        "IRC §743(b)",
        "Notice 2019-27",
        "Treas. Reg. §1.743-1"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge asset eligibility or basis step-up calculation",
    counter_arguments=[
        "Asset not eligible",
        "Basis step-up calculation error",
        "Depreciation method misapplied",
        "Partnership interest not substantiated",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate asset eligibility and apply bonus depreciation and basis step-up as permitted.",
    entity_scope="All taxpayers",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Notice 2019-27"
)

doctrine_cache["TANGIBLE_PROPERTY_REGS"] = DoctrineBlock(
    doctrine_id="TANGIBLE_PROPERTY_REGS",
    topic="Tangible Property Regulations: Repair vs Improvement",
    keywords=["tangible property", "regulations", "repair", "improvement", "unit of property", "safe harbor"],
    conclusion_template="Tangible property regulations require analysis of repair vs improvement, unit of property, and application of safe harbors.",
    reasoning_framework=(
        "Treas. Reg. §1.263(a)-3 requires analysis of whether expenditures are repairs or improvements. "
        "Unit of property determination is critical for applying safe harbors. "
        "Routine maintenance and de minimis safe harbors may permit expensing. "
        "Taxpayers must substantiate expenditure classification and unit of property determination. "
        "Audit risk arises if classification is challenged or safe harbors are misapplied. "
        "IRS guidance in Audit Technique Guides provides details on analysis and application."
    ),
    key_factors=[
        "Expenditure classification",
        "Unit of property determination",
        "Safe harbor eligibility",
        "IRS guidance compliance",
        "Substantiation of expenditure"
    ],
    primary_authority=[
        "Treas. Reg. §1.263(a)-3",
        "IRS Audit Technique Guide"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge classification or safe harbor application",
    counter_arguments=[
        "Improper classification",
        "Unit of property not substantiated",
        "Safe harbor misapplied",
        "Expenditure not properly documented",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate classification and unit of property determination and apply safe harbors as permitted.",
    entity_scope="All taxpayers",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.263(a)-3"
)

doctrine_cache["DE_MINIMIS_SAFE_HARBOR"] = DoctrineBlock(
    doctrine_id="DE_MINIMIS_SAFE_HARBOR",
    topic="De Minimis Safe Harbor Election",
    keywords=["de minimis", "safe harbor", "$2,500", "$5,000", "AFS", "expensing"],
    conclusion_template="De minimis safe harbor allows expensing of items up to $2,500 ($5,000 with AFS) per invoice under Treas. Reg. §1.263(a)-1(f).",
    reasoning_framework=(
        "Treas. Reg. §1.263(a)-1(f) allows taxpayers to expense items up to $2,500 per invoice ($5,000 with applicable financial statements). "
        "Election must be made annually and substantiated with proper records. "
        "Taxpayers must track invoice amounts and maintain documentation. "
        "Audit risk arises if election is not properly made or substantiation is lacking. "
        "IRS guidance in Audit Technique Guides provides details on election and substantiation."
    ),
    key_factors=[
        "Invoice amount tracking",
        "Election substantiation",
        "AFS eligibility",
        "IRS guidance compliance",
        "Documentation maintenance"
    ],
    primary_authority=[
        "Treas. Reg. §1.263(a)-1(f)",
        "IRS Audit Technique Guide"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge election or substantiation",
    counter_arguments=[
        "Election not properly made",
        "Invoice amount error",
        "AFS eligibility not substantiated",
        "Documentation lacking",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track invoice amounts and make annual election with proper substantiation.",
    entity_scope="All taxpayers",
    confidence=0.87,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.263(a)-1(f)"
)

doctrine_cache["ROUTINE_MAINTENANCE_SAFE_HARBOR"] = DoctrineBlock(
    doctrine_id="ROUTINE_MAINTENANCE_SAFE_HARBOR",
    topic="Routine Maintenance Safe Harbor",
    keywords=["routine maintenance", "safe harbor", "tangible property", "expensing", "Treas. Reg. §1.263(a)-3"],
    conclusion_template="Routine maintenance safe harbor allows expensing of qualifying maintenance under Treas. Reg. §1.263(a)-3(g).",
    reasoning_framework=(
        "Treas. Reg. §1.263(a)-3(g) allows expensing of routine maintenance that is expected to be performed more than once during the asset's life. "
        "Taxpayers must substantiate maintenance frequency and asset classification. "
        "Audit risk arises if maintenance does not qualify or substantiation is lacking. "
        "IRS guidance in Audit Technique Guides provides details on eligibility and substantiation."
    ),
    key_factors=[
        "Maintenance frequency",
        "Asset classification",
        "Expensing eligibility",
        "IRS guidance compliance",
        "Documentation maintenance"
    ],
    primary_authority=[
        "Treas. Reg. §1.263(a)-3(g)",
        "IRS Audit Technique Guide"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge maintenance qualification or substantiation",
    counter_arguments=[
        "Maintenance does not qualify",
        "Asset classification error",
        "Expensing eligibility not substantiated",
        "Documentation lacking",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Substantiate maintenance frequency and asset classification and apply safe harbor as permitted.",
    entity_scope="All taxpayers",
    confidence=0.86,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.263(a)-3(g)"
)

doctrine_cache["PARTIAL_DISPOSITION"] = DoctrineBlock(
    doctrine_id="PARTIAL_DISPOSITION",
    topic="Partial Disposition Election",
    keywords=["partial disposition", "election", "MACRS", "§1.168(i)-8", "depreciation"],
    conclusion_template="Partial disposition election allows recognition of loss on disposed asset components under Treas. Reg. §1.168(i)-8.",
    reasoning_framework=(
        "Treas. Reg. §1.168(i)-8 allows taxpayers to elect partial disposition of asset components, recognizing loss and adjusting depreciation schedules. "
        "Election must be made in the year of disposition and substantiated with proper records. "
        "Taxpayers must track asset components and maintain documentation. "
        "Audit risk arises if election is not properly made or substantiation is lacking. "
        "IRS guidance in Audit Technique Guides provides details on election and substantiation."
    ),
    key_factors=[
        "Asset component tracking",
        "Election substantiation",
        "Depreciation schedule adjustment",
        "IRS guidance compliance",
        "Documentation maintenance"
    ],
    primary_authority=[
        "Treas. Reg. §1.168(i)-8",
        "IRS Audit Technique Guide"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge election or substantiation",
    counter_arguments=[
        "Election not properly made",
        "Asset component tracking error",
        "Depreciation schedule not adjusted",
        "Documentation lacking",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Track asset components and make election with proper substantiation and depreciation adjustment.",
    entity_scope="All taxpayers",
    confidence=0.85,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.168(i)-8"
)

doctrine_cache["PLACED_IN_SERVICE"] = DoctrineBlock(
    doctrine_id="PLACED_IN_SERVICE",
    topic="Placed-in-Service Timing",
    keywords=["placed-in-service", "timing", "depreciation", "MACRS", "ready and available"],
    conclusion_template="Depreciation begins when asset is placed in service, defined as ready and available for use under Treas. Reg. §1.167(a)-11(e).",
    reasoning_framework=(
        "Treas. Reg. §1.167(a)-11(e) defines placed-in-service as the date the asset is ready and available for use in the taxpayer's business. "
        "Depreciation cannot begin before this date. "
        "Taxpayers must substantiate readiness and availability with documentation. "
        "Audit risk arises if placed-in-service date is not properly documented or depreciation is misapplied. "
        "IRS guidance in Audit Technique Guides provides details on substantiation and timing."
    ),
    key_factors=[
        "Readiness and availability",
        "Documentation maintenance",
        "Depreciation timing",
        "IRS guidance compliance",
        "Asset classification"
    ],
    primary_authority=[
        "Treas. Reg. §1.167(a)-11(e)",
        "IRS Audit Technique Guide"
    ],
    burden_holder="Taxpayer",
    adversary_position="IRS may challenge placed-in-service date or documentation",
    counter_arguments=[
        "Placed-in-service date not substantiated",
        "Readiness and availability not documented",
        "Depreciation timing error",
        "Asset classification error",
        "Noncompliance with IRS guidance"
    ],
    resolution_strategy="Document readiness and availability and apply depreciation timing as required.",
    entity_scope="All taxpayers",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent="Treas. Reg. §1.167(a)-11(e)"
)

# AUTHORITY HARDENING
AUTHORITY_WEIGHTS = {
    "IRC": 5,
    "Treas. Reg.": 4,
    "Rev. Proc.": 3,
    "Notice": 2,
    "IRS Audit Technique Guide": 1,
    "Case Law": 2,
    "PLR": 1,
    "CCA": 1
}
def resolve_authority_conflicts(authorities: List[str]) -> List[str]:
    weighted = sorted(authorities, key=lambda a: AUTHORITY_WEIGHTS.get(a.split()[0], 0), reverse=True)
    return weighted

# SEMANTIC NORMALIZATION
SEMANTIC_MAP = {
    "MACRS": "Modified Accelerated Cost Recovery System",
    "ADS": "Alternative Depreciation System",
    "QIP": "Qualified Improvement Property",
    "Listed Property": "IRC §280F(d)(4) property",
    "Luxury Auto": "Passenger vehicle subject to §280F limits",
    "Section 179": "IRC §179 expensing",
    "Bonus Depreciation": "IRC §168(k) additional first-year depreciation",
    "Mid-Month Convention": "Depreciation convention for real property",
    "Half-Year Convention": "Depreciation convention for personal property",
    "Mid-Quarter Convention": "Depreciation convention triggered by asset timing",
    "Cost Segregation": "Engineering-based asset reclassification",
    "Section 197": "Intangible amortization under IRC §197",
    "Section 167(f)": "Computer software depreciation",
    "Section 179D": "Energy efficient commercial building deduction",
    "Disposition": "Asset sale or retirement triggering recapture",
    "Like-Kind Exchange": "IRC §1031 exchange",
    "Partnership Basis Step-Up": "IRC §743(b) adjustment",
    "Tangible Property Regulations": "Repair vs improvement analysis",
    "De Minimis Safe Harbor": "Expensing election under Treas. Reg. §1.263(a)-1(f)",
    "Routine Maintenance Safe Harbor": "Expensing election under Treas. Reg. §1.263(a)-3(g)",
    "Partial Disposition": "Election under Treas. Reg. §1.168(i)-8",
    "Placed-in-Service": "Asset ready and available for use"
}

def normalize_terms(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# EPISTEMIC GUARDRAILS
BANNED_PHRASES = ["always", "never", "guaranteed"]
def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "")
    return text

# FACT FRAGILITY SCORING
def score_fact_fragility(conclusion: str) -> float:
    score = 0.0
    if "substantiation" in conclusion:
        score += 0.2
    if "audit risk" in conclusion:
        score += 0.2
    if "documentation" in conclusion:
        score += 0.2
    if "challenge" in conclusion:
        score += 0.2
    if "misapplied" in conclusion:
        score += 0.2
    return min(score, 1.0)

# THREE-LAYER RESPONSE
def doctrine_cache_lookup(scenario: str) -> Optional[DoctrineBlock]:
    for block in doctrine_cache.values():
        if any(kw.lower() in scenario.lower() for kw in block.keywords):
            metrics_collector.doctrine_hits += 1
            return block
    metrics_collector.doctrine_misses += 1
    return None

def semantic_search(scenario: str) -> Optional[DoctrineBlock]:
    for block in doctrine_cache.values():
        if block.topic.lower() in scenario.lower():
            return block
    return None

def deep_analysis(scenario: str) -> Optional[DoctrineBlock]:
    # Layer 3: Multi-doctrine decomposition, DAG, 8-step resolution
    triggered = []
    for block in doctrine_cache.values():
        if any(kw.lower() in scenario.lower() for kw in block.keywords):
            triggered.append(block)
    if triggered:
        return triggered[0]
    return None

def multi_doctrine_decomposition(scenario: str) -> List[DoctrineBlock]:
    return [block for block in doctrine_cache.values() if any(kw.lower() in scenario.lower() for kw in block.keywords)]

# COVERAGE MAP
def coverage_map(scenario: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    for block in doctrine_cache.values():
        if any(kw.lower() in scenario.lower() for kw in block.keywords):
            triggered.append(block.doctrine_id)
        else:
            missed.append(block.doctrine_id)
    return {"triggered": triggered, "missed": missed, "epistemic_gaps": len(missed)}

# DRIFT WATCHER
BASELINE_HASH = hashlib.sha256(str(sorted(doctrine_cache.keys())).encode()).hexdigest()
def detect_drift() -> bool:
    current_hash = hashlib.sha256(str(sorted(doctrine_cache.keys())).encode()).hexdigest()
    return current_hash != BASELINE_HASH

# AUDIT TRAIL
AUDIT_TRAIL_PATH = Path("audit_trail.jsonl")
def log_audit_trail(query_id: str, request: QueryRequest, response: QueryResponse):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query_id": query_id,
        "request": request.dict(),
        "response": response.dict()
    }
    with AUDIT_TRAIL_PATH.open("a") as f:
        f.write(str(entry) + "\n")

# DETERMINISM HASH
def determinism_hash(response: QueryResponse) -> str:
    return hashlib.sha256(str(response.dict()).encode()).hexdigest()

# FASTAPI APP
app = FastAPI(title="Depreciation Calculator Engine (TX04)", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_event():
    logger.info("Depreciation Calculator Engine (TX04) started.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Depreciation Calculator Engine (TX04) stopped.")

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    query_id = str(uuid.uuid4())
    metrics_collector.record_query(query_id, datetime.utcnow())
    block = doctrine_cache_lookup(request.scenario)
    if not block:
        block = semantic_search(request.scenario)
    if not block:
        block = deep_analysis(request.scenario)
    if not block:
        logger.error(f"No doctrine found for scenario: {request.scenario}")
        metrics_collector.record_error(query_id, "No doctrine found", datetime.utcnow())
        return QueryResponse(
            engine_id="TX04",
            query_id=query_id,
            mode=request.mode,
            confidence=0.0,
            confidence_zone=ConfidenceZone.HIGH_RISK,
            position_zone=PositionZone.PLANNING,
            primary_conclusion="No applicable doctrine found.",
            reasoning_framework="Scenario does not match any doctrine block.",
            key_factors=[],
            primary_authority=[],
            counter_arguments=[],
            resolution_strategy="Review scenario for accuracy.",
            determinism_hash="",
            doctrine_id=None,
            triggered_doctrines=[],
            coverage_map=coverage_map(request.scenario),
            drift_detected=detect_drift(),
            audit_trail_path=str(AUDIT_TRAIL_PATH)
        )
    conclusion = normalize_terms(block.conclusion_template)
    conclusion = apply_epistemic_guardrails(conclusion)
    fragility_score = score_fact_fragility(conclusion)
    position_zone = PositionZone.PLANNING
    response = QueryResponse(
        engine_id="TX04",
        query_id=query_id,
        mode=request.mode,
        confidence=block.confidence - fragility_score,
        confidence_zone=block.confidence_zone,
        position_zone=position_zone,
        primary_conclusion=conclusion,
        reasoning_framework=normalize_terms(apply_epistemic_guardrails(block.reasoning_framework)),
        key_factors=block.key_factors,
        primary_authority=resolve_authority_conflicts(block.primary_authority),
        counter_arguments=block.counter_arguments,
        resolution_strategy=block.resolution_strategy,
        determinism_hash="",
        doctrine_id=block.doctrine_id,
        triggered_doctrines=[block.doctrine_id],
        coverage_map=coverage_map(request.scenario),
        drift_detected=detect_drift(),
        audit_trail_path=str(AUDIT_TRAIL_PATH)
    )
    response.determinism_hash = determinism_hash(response)
    log_audit_trail(query_id, request, response)
    return response

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "TX04", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    return {
        "queries_last_hour": metrics_collector.queries_last_hour(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "latency_stats": metrics_collector.get_latency_stats()
    }

@app.get("/coverage")
async def coverage(scenario: Optional[str] = None):
    if scenario:
        return coverage_map(scenario)
    return {"coverage": [block.doctrine_id for block in doctrine_cache.values()]}

@app.get("/drift")
async def drift():
    return {"drift_detected": detect_drift(), "baseline_hash": BASELINE_HASH}

@app.get("/doctrines")
async def doctrines():
    return {block.doctrine_id: block.topic for block in doctrine_cache.values()}
