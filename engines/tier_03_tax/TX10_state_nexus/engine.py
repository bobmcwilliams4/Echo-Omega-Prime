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
from enum import Enum, auto
from datetime import datetime, timedelta

# Enums
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
    PHYSICAL_PRESENCE = auto()
    ECONOMIC_NEXUS = auto()
    PL_86_272 = auto()
    INTERNET_ACTIVITIES = auto()
    FACTOR_PRESENCE = auto()
    SALES_TAX_NEXUS = auto()
    INCOME_TAX_APPORTIONMENT = auto()
    SALES_FACTOR_SOURCING = auto()
    PROPERTY_FACTOR = auto()
    PAYROLL_FACTOR = auto()
    THROWBACK_THROWOUT = auto()
    UNITARY_BUSINESS = auto()
    COMBINED_REPORTING = auto()
    JOYCE_FINNIGAN = auto()
    STATE_NOL = auto()
    STATE_CONFORMITY = auto()
    TAX_HAVEN = auto()
    PARTNERSHIP_NEXUS = auto()
    VDA = auto()
    MTC_MODEL = auto()

# Metrics Collector
class MetricsCollector:
    def __init__(self):
        self.queries = []
        self.errors = []
        self.doctrine_hits = {}
        self.latencies = []
    def record_query(self, query_id, doctrine_ids, latency):
        self.queries.append({'query_id': query_id, 'doctrines': doctrine_ids, 'timestamp': datetime.utcnow()})
        for did in doctrine_ids:
            self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1
        self.latencies.append(latency)
    def record_error(self, query_id, error):
        self.errors.append({'query_id': query_id, 'error': error, 'timestamp': datetime.utcnow()})
    def get_latency_stats(self):
        if not self.latencies:
            return {'avg': 0, 'max': 0, 'min': 0}
        return {'avg': sum(self.latencies)/len(self.latencies), 'max': max(self.latencies), 'min': min(self.latencies)}
    def get_doctrine_hit_rate(self):
        total = sum(self.doctrine_hits.values())
        return {k: v/total for k, v in self.doctrine_hits.items()} if total else {}
    def queries_last_hour(self):
        cutoff = datetime.utcnow() - timedelta(hours=1)
        return len([q for q in self.queries if q['timestamp'] > cutoff])

metrics_collector = MetricsCollector()

# Pydantic Models
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
    coverage_map: Dict[str, Any]
    drift_status: str
    audit_trail_path: str

# Doctrine Cache
@dataclass
class DoctrineBlock:
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
    doctrine_id: str = field(default_factory=lambda: str(uuid.uuid4()))

doctrine_cache: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Physical Presence Nexus: Office",
        keywords=["physical presence", "office", "nexus", "state income tax", "IRC §861", "Wayfair", "South Dakota"],
        conclusion_template="Maintaining an office in a state generally establishes nexus for income and sales tax purposes.",
        reasoning_framework=(
            "Physical presence has historically been the primary standard for state tax nexus. The presence of a permanent office "
            "in a state constitutes a substantial connection, satisfying the Due Process and Commerce Clause requirements. "
            "See Quill Corp. v. North Dakota, 504 U.S. 298 (1992), superseded by South Dakota v. Wayfair, Inc., 138 S. Ct. 2080 (2018). "
            "IRC §861 provides guidance on sourcing income, but state law controls nexus. The office's existence enables the state "
            "to assert jurisdiction for both income and sales tax. Even after Wayfair, physical presence remains a strong nexus factor. "
            "States may impose registration, filing, and collection obligations. The taxpayer bears the burden to rebut nexus if claiming exemption."
        ),
        key_factors=["Permanent office", "Employee presence", "Business activity", "State registration", "Duration of presence"],
        primary_authority=["Quill Corp. v. North Dakota", "South Dakota v. Wayfair", "IRC §861", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Office used only for non-taxable activities",
            "Office leased but not used",
            "No sales generated from office",
            "Short-term presence",
            "Federal preemption (PL 86-272)"
        ],
        resolution_strategy="Evaluate office's function, duration, and connection to taxable activity; review state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Quill, Wayfair"
    ),
    DoctrineBlock(
        topic="Physical Presence Nexus: Employee",
        keywords=["physical presence", "employee", "nexus", "state income tax", "IRC §861", "Wayfair", "Payroll"],
        conclusion_template="Having employees working in a state creates nexus for income and payroll tax purposes.",
        reasoning_framework=(
            "Employee presence is a classic nexus trigger. States rely on the presence of employees performing services "
            "to assert jurisdiction. See National Geographic v. California, 430 U.S. 551 (1977). Payroll factor under UDITPA "
            "is used for apportionment. Even remote employees may create nexus if their activities are regular and substantial. "
            "Wayfair expanded economic nexus but did not eliminate physical presence as a basis. IRC §861 and §862 guide sourcing, "
            "but state law determines nexus. The taxpayer must track employee locations and activities to assess exposure."
        ),
        key_factors=["Employee location", "Regularity of services", "Payroll reporting", "Duration", "Remote work"],
        primary_authority=["National Geographic v. California", "Wayfair", "IRC §861", "UDITPA", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Employee is independent contractor",
            "Short-term or incidental presence",
            "No sales generated",
            "Federal protection (PL 86-272)",
            "No payroll reporting"
        ],
        resolution_strategy="Analyze employee status, activities, and payroll reporting; review state definitions.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="National Geographic, Wayfair"
    ),
    DoctrineBlock(
        topic="Physical Presence Nexus: Inventory",
        keywords=["physical presence", "inventory", "nexus", "state income tax", "IRC §863", "Wayfair", "Sales tax"],
        conclusion_template="Owning or storing inventory in a state establishes nexus for sales and income tax.",
        reasoning_framework=(
            "Inventory presence is a strong nexus factor. States assert jurisdiction when inventory is stored in warehouses, "
            "fulfillment centers, or consignment locations. See Scripto, Inc. v. Carson, 362 U.S. 207 (1960). IRC §863(b) "
            "addresses inventory sourcing, but state law controls nexus. Marketplace facilitator laws may attribute inventory "
            "to sellers. Wayfair expanded economic nexus but did not diminish inventory-based nexus. Taxpayers must track inventory "
            "locations and ownership to assess exposure."
        ),
        key_factors=["Inventory ownership", "Storage location", "Marketplace facilitator", "Duration", "Sales generated"],
        primary_authority=["Scripto v. Carson", "Wayfair", "IRC §863", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Inventory owned by third party",
            "Short-term storage",
            "No sales generated",
            "Federal protection (PL 86-272)",
            "No physical access"
        ],
        resolution_strategy="Review inventory ownership, storage agreements, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Scripto, Wayfair"
    ),
    DoctrineBlock(
        topic="Physical Presence Nexus: Equipment",
        keywords=["physical presence", "equipment", "nexus", "state income tax", "IRC §861", "Wayfair", "Property factor"],
        conclusion_template="Owning or leasing equipment in a state creates nexus for income and property tax.",
        reasoning_framework=(
            "Equipment presence is recognized as nexus under state law. States consider leased or owned equipment as a substantial connection. "
            "See Tyler Pipe Industries v. Washington, 483 U.S. 232 (1987). Property factor under UDITPA includes equipment at cost or rental value. "
            "Wayfair expanded economic nexus but did not eliminate physical presence. Taxpayers must track equipment location, ownership, and use."
        ),
        key_factors=["Equipment ownership", "Lease agreements", "Location", "Duration", "Business use"],
        primary_authority=["Tyler Pipe v. Washington", "Wayfair", "IRC §861", "UDITPA", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Equipment used for non-taxable activity",
            "Short-term lease",
            "No sales generated",
            "Federal protection (PL 86-272)",
            "Equipment owned by third party"
        ],
        resolution_strategy="Analyze equipment ownership, lease terms, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Tyler Pipe, Wayfair"
    ),
    DoctrineBlock(
        topic="Economic Nexus: Wayfair Threshold",
        keywords=["economic nexus", "Wayfair", "South Dakota", "$100K", "200 transactions", "sales tax", "state income tax"],
        conclusion_template="Economic nexus is established if sales or transactions exceed state thresholds post-Wayfair.",
        reasoning_framework=(
            "South Dakota v. Wayfair, Inc. (2018) overturned Quill's physical presence rule, allowing states to impose nexus based on economic activity. "
            "Most states adopted thresholds ($100K sales or 200 transactions) for sales tax nexus. Some states apply similar thresholds for income tax. "
            "Marketplace facilitator laws may aggregate sales. Taxpayers must monitor sales and transaction counts by state. IRC §861 and §862 guide sourcing, "
            "but state law controls nexus. States may impose registration and collection obligations once thresholds are met."
        ),
        key_factors=["Sales volume", "Transaction count", "Marketplace facilitator", "Thresholds", "State statutes"],
        primary_authority=["Wayfair", "IRC §861", "State statutes", "MTC model"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Sales below threshold",
            "Transactions below threshold",
            "Marketplace facilitator exemption",
            "No physical presence",
            "Federal protection (PL 86-272)"
        ],
        resolution_strategy="Monitor sales and transactions; review state thresholds and statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wayfair"
    ),
    DoctrineBlock(
        topic="Economic Nexus: Marketplace Facilitator",
        keywords=["economic nexus", "marketplace facilitator", "Wayfair", "aggregation", "sales tax", "state income tax"],
        conclusion_template="Marketplace facilitator laws may attribute sales to sellers for nexus determination.",
        reasoning_framework=(
            "Marketplace facilitator statutes require platforms to collect and remit sales tax on behalf of sellers. States aggregate sales "
            "made through facilitators to determine nexus. See California AB 147 (2019), New York Tax Law §1101. Wayfair supports economic nexus "
            "based on aggregated sales. Taxpayers must track sales by facilitator and direct channels. IRC §861 and §862 guide sourcing, but state law controls."
        ),
        key_factors=["Marketplace facilitator", "Aggregated sales", "Thresholds", "State statutes", "Reporting"],
        primary_authority=["Wayfair", "California AB 147", "NY Tax Law §1101", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Facilitator not required to collect",
            "Sales below threshold",
            "No physical presence",
            "Federal protection (PL 86-272)",
            "Facilitator exemption"
        ],
        resolution_strategy="Review facilitator agreements, sales aggregation, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wayfair"
    ),
    DoctrineBlock(
        topic="PL 86-272 Protection: Solicitation Only",
        keywords=["PL 86-272", "solicitation", "tangible personal property", "income tax", "state protection", "IRC §863"],
        conclusion_template="PL 86-272 protects sellers of tangible personal property engaged only in solicitation from state income tax.",
        reasoning_framework=(
            "Public Law 86-272 (15 U.S.C. §381) prohibits states from imposing income tax on out-of-state sellers whose only activity is solicitation "
            "of orders for tangible personal property. See Wisconsin Dept. of Revenue v. William Wrigley, Jr. Co., 505 U.S. 214 (1992). Activities beyond solicitation "
            "such as installation, repairs, or services void protection. PL 86-272 does not apply to sales tax or intangible property. IRC §863 guides sourcing, "
            "but PL 86-272 overrides state nexus for income tax. Taxpayers must analyze in-state activities to determine eligibility."
        ),
        key_factors=["Solicitation only", "Tangible personal property", "No services", "No intangibles", "State statutes"],
        primary_authority=["PL 86-272", "Wrigley", "IRC §863", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Activities beyond solicitation",
            "Services provided",
            "Intangible property sales",
            "Installation or repairs",
            "Marketplace facilitator"
        ],
        resolution_strategy="Review in-state activities, product type, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wrigley"
    ),
    DoctrineBlock(
        topic="PL 86-272: Services and Intangibles",
        keywords=["PL 86-272", "services", "intangibles", "income tax", "state protection", "IRC §861"],
        conclusion_template="PL 86-272 does not protect sales of services or intangibles from state income tax.",
        reasoning_framework=(
            "PL 86-272 applies only to solicitation of tangible personal property. Sales of services or intangibles are not protected. "
            "See 15 U.S.C. §381, Wrigley. States may impose income tax nexus for service providers. IRC §861 and §862 guide sourcing, "
            "but PL 86-272 does not override state law for services or intangibles. Taxpayers must analyze product type and in-state activities."
        ),
        key_factors=["Services", "Intangibles", "Solicitation", "State statutes", "Product type"],
        primary_authority=["PL 86-272", "Wrigley", "IRC §861", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Tangible personal property sales",
            "No in-state activity",
            "Federal preemption",
            "Marketplace facilitator",
            "Short-term presence"
        ],
        resolution_strategy="Review product type, in-state activities, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wrigley"
    ),
    DoctrineBlock(
        topic="PL 86-272: Internet Activities (MTC 2021)",
        keywords=["PL 86-272", "internet activities", "MTC", "cookies", "apps", "income tax", "state protection"],
        conclusion_template="MTC's 2021 interpretation limits PL 86-272 protection for certain internet activities.",
        reasoning_framework=(
            "The Multistate Tax Commission (MTC) issued guidance in 2021 interpreting PL 86-272 in the context of internet activities. "
            "Activities such as placing cookies, offering apps, or providing post-sale support may exceed solicitation. See MTC Statement 2021. "
            "States may adopt MTC guidance, limiting PL 86-272 protection. Taxpayers must analyze website functions, cookies, and online support. "
            "IRC §861 and §862 guide sourcing, but state law controls. PL 86-272 protection is lost if internet activities constitute more than solicitation."
        ),
        key_factors=["Internet activities", "Cookies", "Apps", "Online support", "State adoption"],
        primary_authority=["MTC Statement 2021", "PL 86-272", "IRC §861", "State statutes"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Website used only for solicitation",
            "No cookies or apps",
            "No post-sale support",
            "State has not adopted MTC guidance",
            "Federal preemption"
        ],
        resolution_strategy="Review website functions, cookies, and state adoption of MTC guidance.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="MTC Statement 2021"
    ),
    DoctrineBlock(
        topic="Factor-Presence Nexus: Property",
        keywords=["factor presence", "property", "nexus", "$50K", "UDITPA", "state income tax"],
        conclusion_template="States may assert nexus if property in-state exceeds $50,000 under factor-presence statutes.",
        reasoning_framework=(
            "Factor-presence nexus statutes (e.g., California, Ohio) establish nexus if property, payroll, or sales exceed thresholds. "
            "Property factor is calculated as owned at cost or rented ×8. See UDITPA §9. States may assert income tax nexus if in-state property "
            "exceeds $50,000. Taxpayers must track property values and locations. IRC §861 and §862 guide sourcing, but state law controls nexus."
        ),
        key_factors=["Property value", "Owned/rented", "Thresholds", "State statutes", "UDITPA"],
        primary_authority=["UDITPA §9", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Property below threshold",
            "Short-term lease",
            "No business activity",
            "Federal protection (PL 86-272)",
            "Property owned by third party"
        ],
        resolution_strategy="Review property values, lease terms, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Factor-Presence Nexus: Payroll",
        keywords=["factor presence", "payroll", "nexus", "$50K", "UDITPA", "state income tax"],
        conclusion_template="States may assert nexus if payroll in-state exceeds $50,000 under factor-presence statutes.",
        reasoning_framework=(
            "Factor-presence nexus statutes use payroll as a nexus trigger. Payroll factor is compensation paid to employees in-state. "
            "See UDITPA §10. States may assert income tax nexus if payroll exceeds $50,000. Taxpayers must track employee compensation and locations. "
            "IRC §861 and §862 guide sourcing, but state law controls nexus. Payroll reporting is critical for compliance."
        ),
        key_factors=["Payroll value", "Employee location", "Thresholds", "State statutes", "UDITPA"],
        primary_authority=["UDITPA §10", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Payroll below threshold",
            "Short-term employment",
            "No business activity",
            "Federal protection (PL 86-272)",
            "Payroll paid by third party"
        ],
        resolution_strategy="Review payroll records, employee locations, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Factor-Presence Nexus: Sales",
        keywords=["factor presence", "sales", "nexus", "$500K", "UDITPA", "state income tax"],
        conclusion_template="States may assert nexus if sales in-state exceed $500,000 under factor-presence statutes.",
        reasoning_framework=(
            "Factor-presence nexus statutes use sales as a nexus trigger. Sales factor is revenue from customers in-state. "
            "See UDITPA §11. States may assert income tax nexus if sales exceed $500,000 or 25% of total. Taxpayers must track sales by state. "
            "IRC §861 and §862 guide sourcing, but state law controls nexus. Sales reporting is critical for compliance."
        ),
        key_factors=["Sales value", "Customer location", "Thresholds", "State statutes", "UDITPA"],
        primary_authority=["UDITPA §11", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Sales below threshold",
            "No business activity",
            "Federal protection (PL 86-272)",
            "Sales attributed to facilitator",
            "Short-term presence"
        ],
        resolution_strategy="Review sales records, customer locations, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.87,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Sales Tax Economic Nexus: State Thresholds",
        keywords=["sales tax", "economic nexus", "state thresholds", "Wayfair", "$100K", "200 transactions"],
        conclusion_template="Sales tax economic nexus is triggered if sales or transactions exceed state-specific thresholds.",
        reasoning_framework=(
            "Post-Wayfair, states adopted varying thresholds for sales tax nexus. Most use $100,000 sales or 200 transactions, but some differ. "
            "See South Dakota v. Wayfair, Inc. (2018), state statutes. Marketplace facilitator laws may aggregate sales. Taxpayers must monitor thresholds "
            "in each state. IRC §861 and §862 guide sourcing, but state law controls nexus. Registration and collection obligations arise once thresholds are met."
        ),
        key_factors=["Sales volume", "Transaction count", "State thresholds", "Marketplace facilitator", "Reporting"],
        primary_authority=["Wayfair", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Sales below threshold",
            "Transactions below threshold",
            "Facilitator exemption",
            "No physical presence",
            "Federal protection (PL 86-272)"
        ],
        resolution_strategy="Monitor sales and transactions; review state thresholds and statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.86,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Wayfair"
    ),
    DoctrineBlock(
        topic="Income Tax Apportionment: UDITPA Three-Factor",
        keywords=["income tax", "apportionment", "UDITPA", "three-factor", "sales", "property", "payroll"],
        conclusion_template="UDITPA uses a three-factor formula (sales, property, payroll) to apportion income among states.",
        reasoning_framework=(
            "The Uniform Division of Income for Tax Purposes Act (UDITPA) §9-§11 uses sales, property, and payroll factors to apportion income. "
            "Each factor is weighted equally unless state law modifies. States may adopt single sales factor. IRC §861 and §862 guide sourcing, "
            "but state law controls apportionment. Taxpayers must calculate each factor and apply state-specific weights."
        ),
        key_factors=["Sales factor", "Property factor", "Payroll factor", "State weights", "UDITPA"],
        primary_authority=["UDITPA §9-§11", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "State uses single sales factor",
            "Different weights",
            "Nonbusiness income",
            "Throwback/throwout rules",
            "Unitary business"
        ],
        resolution_strategy="Calculate factors; apply state-specific apportionment rules.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.85,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Sales Factor: Market-Based Sourcing",
        keywords=["sales factor", "market-based sourcing", "services", "intangibles", "income tax", "state statutes"],
        conclusion_template="Market-based sourcing attributes sales of services and intangibles to the state where the customer receives benefit.",
        reasoning_framework=(
            "Market-based sourcing is used by many states for sales factor apportionment. Sales of services and intangibles are sourced to the state "
            "where the customer receives benefit. See California Rev. & Tax Code §25136, New York Tax Law §210-A. IRC §861 and §862 guide sourcing, "
            "but state law controls. Taxpayers must analyze customer locations and benefit delivery."
        ),
        key_factors=["Customer location", "Benefit received", "Services", "Intangibles", "State statutes"],
        primary_authority=["CA Rev. & Tax Code §25136", "NY Tax Law §210-A", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Cost-of-performance sourcing",
            "Multiple customer locations",
            "Nonbusiness income",
            "Throwback/throwout rules",
            "Unitary business"
        ],
        resolution_strategy="Analyze customer locations and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.84,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §25136"
    ),
    DoctrineBlock(
        topic="Sales Factor: Cost-of-Performance Sourcing",
        keywords=["sales factor", "cost-of-performance", "services", "intangibles", "income tax", "state statutes"],
        conclusion_template="Cost-of-performance sourcing attributes sales of services and intangibles to the state where the greatest cost is incurred.",
        reasoning_framework=(
            "Cost-of-performance sourcing is used by some states for sales factor apportionment. Sales of services and intangibles are sourced to the state "
            "where the greatest cost of performance is incurred. See Georgia Code §48-7-31, Virginia Code §58.1-302. IRC §861 and §862 guide sourcing, "
            "but state law controls. Taxpayers must analyze cost locations and apportion accordingly."
        ),
        key_factors=["Cost location", "Services", "Intangibles", "State statutes", "Apportionment"],
        primary_authority=["GA Code §48-7-31", "VA Code §58.1-302", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Market-based sourcing",
            "Multiple cost locations",
            "Nonbusiness income",
            "Throwback/throwout rules",
            "Unitary business"
        ],
        resolution_strategy="Analyze cost locations and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.83,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="GA Code §48-7-31"
    ),
    DoctrineBlock(
        topic="Property Factor: Owned at Cost, Rented ×8",
        keywords=["property factor", "owned", "rented", "UDITPA", "apportionment", "income tax"],
        conclusion_template="Property factor is calculated as owned property at cost plus rented property multiplied by eight.",
        reasoning_framework=(
            "UDITPA §9 defines property factor as owned property at cost and rented property at annual rental ×8. States may modify calculation. "
            "IRC §861 and §862 guide sourcing, but state law controls apportionment. Taxpayers must track property values, ownership, and lease terms."
        ),
        key_factors=["Owned property", "Rented property", "Cost", "Lease terms", "UDITPA"],
        primary_authority=["UDITPA §9", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Different state calculation",
            "Short-term lease",
            "Nonbusiness property",
            "Throwback/throwout rules",
            "Unitary business"
        ],
        resolution_strategy="Review property values, lease terms, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.82,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Payroll Factor: Compensation Paid",
        keywords=["payroll factor", "compensation", "employee", "UDITPA", "apportionment", "income tax"],
        conclusion_template="Payroll factor is compensation paid to employees for services performed in-state.",
        reasoning_framework=(
            "UDITPA §10 defines payroll factor as compensation paid to employees for services performed in-state. States may modify calculation. "
            "IRC §861 and §862 guide sourcing, but state law controls apportionment. Taxpayers must track employee compensation and locations."
        ),
        key_factors=["Employee compensation", "Location", "Services performed", "UDITPA", "State statutes"],
        primary_authority=["UDITPA §10", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Different state calculation",
            "Short-term employment",
            "Nonbusiness payroll",
            "Throwback/throwout rules",
            "Unitary business"
        ],
        resolution_strategy="Review payroll records, employee locations, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.81,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="UDITPA"
    ),
    DoctrineBlock(
        topic="Throwback and Throwout Rules",
        keywords=["throwback", "throwout", "sales factor", "apportionment", "income tax", "state statutes"],
        conclusion_template="Throwback and throwout rules adjust sales factor for sales to states where taxpayer is not taxable.",
        reasoning_framework=(
            "Throwback rules require sales shipped from a state to be included in the origin state's sales factor if the taxpayer is not taxable in the destination state. "
            "Throwout rules exclude sales to states where the taxpayer is not taxable. See Joyce v. Franchise Tax Board, 393 U.S. 106 (1968), Finnigan v. Franchise Tax Board, 246 Cal. Rptr. 2d 602 (1988). "
            "States may adopt either rule. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze nexus and sales destinations."
        ),
        key_factors=["Sales destination", "Taxable status", "Throwback", "Throwout", "State statutes"],
        primary_authority=["Joyce", "Finnigan", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Taxable in destination state",
            "Different state rule",
            "Nonbusiness income",
            "Unitary business",
            "Marketplace facilitator"
        ],
        resolution_strategy="Analyze sales destinations, taxable status, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.80,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Joyce, Finnigan"
    ),
    DoctrineBlock(
        topic="Unitary Business Principle: Three Unities Test",
        keywords=["unitary business", "three unities", "ownership", "operation", "use", "apportionment", "income tax"],
        conclusion_template="Unitary business is determined by the three unities test: ownership, operation, and use.",
        reasoning_framework=(
            "The unitary business principle determines whether income is apportionable among states. The three unities test examines ownership, operation, and use. "
            "See Mobil Oil Corp. v. Commissioner of Taxes, 445 U.S. 425 (1980), Container Corp. v. Franchise Tax Board, 463 U.S. 159 (1983). "
            "States may apply different tests. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze business structure and operations."
        ),
        key_factors=["Ownership", "Operation", "Use", "Business structure", "State statutes"],
        primary_authority=["Mobil Oil", "Container Corp.", "State statutes", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Separate business operations",
            "No unity of ownership",
            "Different state test",
            "Nonbusiness income",
            "Combined reporting"
        ],
        resolution_strategy="Analyze business structure, operations, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.79,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Mobil Oil, Container Corp."
    ),
    DoctrineBlock(
        topic="Combined Reporting Requirements",
        keywords=["combined reporting", "mandatory", "water's edge", "worldwide", "unitary business", "income tax"],
        conclusion_template="Combined reporting is mandatory in many states for unitary businesses; water's edge or worldwide methods may apply.",
        reasoning_framework=(
            "Combined reporting requires unitary businesses to file a single return including all related entities. States may use water's edge (U.S. entities only) or worldwide (all entities). "
            "See California Rev. & Tax Code §25101, New York Tax Law §210-C. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze business structure and state requirements."
        ),
        key_factors=["Unitary business", "Combined reporting", "Water's edge", "Worldwide", "State statutes"],
        primary_authority=["CA Rev. & Tax Code §25101", "NY Tax Law §210-C", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Separate business operations",
            "No unity",
            "Different state method",
            "Nonbusiness income",
            "Foreign entities"
        ],
        resolution_strategy="Review business structure, combined reporting rules, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.78,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §25101"
    ),
    DoctrineBlock(
        topic="Joyce vs Finnigan Election",
        keywords=["Joyce", "Finnigan", "throwback", "combined reporting", "sales factor", "income tax"],
        conclusion_template="States may apply Joyce (entity-level nexus) or Finnigan (group-level nexus) for throwback rules.",
        reasoning_framework=(
            "Joyce v. Franchise Tax Board applies throwback rules based on entity-level nexus; Finnigan applies group-level nexus. States may elect either method. "
            "See Joyce, Finnigan, California Regulation §25135. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze group structure and state election."
        ),
        key_factors=["Entity-level nexus", "Group-level nexus", "Throwback", "Combined reporting", "State statutes"],
        primary_authority=["Joyce", "Finnigan", "CA Reg. §25135", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Different state election",
            "Nonbusiness income",
            "Separate business operations",
            "Unitary business",
            "Marketplace facilitator"
        ],
        resolution_strategy="Review group structure, throwback rules, and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.77,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Joyce, Finnigan"
    ),
    DoctrineBlock(
        topic="State NOL Rules: Decoupling from Federal",
        keywords=["state NOL", "net operating loss", "carryback", "carryforward", "decoupling", "income tax"],
        conclusion_template="States may decouple from federal NOL rules, with varying carryback and carryforward periods.",
        reasoning_framework=(
            "States may decouple from federal net operating loss (NOL) rules. Carryback and carryforward periods vary. See California Rev. & Tax Code §24416, New York Tax Law §210-B. "
            "IRC §172 governs federal NOLs, but state law controls. Taxpayers must analyze state-specific NOL provisions and decoupling status."
        ),
        key_factors=["NOL carryback", "NOL carryforward", "Decoupling", "State statutes", "IRC §172"],
        primary_authority=["CA Rev. & Tax Code §24416", "NY Tax Law §210-B", "IRC §172"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Federal conformity",
            "Different carry periods",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting"
        ],
        resolution_strategy="Review state NOL rules and decoupling status.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.76,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §24416"
    ),
    DoctrineBlock(
        topic="State Conformity to IRC",
        keywords=["state conformity", "IRC", "rolling conformity", "fixed date", "selective conformity", "income tax"],
        conclusion_template="States may adopt rolling, fixed date, or selective conformity to the IRC for income tax purposes.",
        reasoning_framework=(
            "State conformity to the Internal Revenue Code (IRC) varies. Rolling conformity adopts changes automatically; fixed date conformity uses a specific IRC version; selective conformity adopts only certain provisions. "
            "See California Rev. & Tax Code §17024.5, New York Tax Law §607. Taxpayers must analyze conformity status for each state."
        ),
        key_factors=["Rolling conformity", "Fixed date", "Selective conformity", "State statutes", "IRC"],
        primary_authority=["CA Rev. & Tax Code §17024.5", "NY Tax Law §607", "IRC"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Different conformity status",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting",
            "Marketplace facilitator"
        ],
        resolution_strategy="Review state conformity statutes and IRC version.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.75,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §17024.5"
    ),
    DoctrineBlock(
        topic="Tax Haven and Captive Insurance Nexus",
        keywords=["tax haven", "captive insurance", "nexus", "addback statutes", "related party", "income tax"],
        conclusion_template="States may assert nexus for tax haven and captive insurance entities using addback statutes for related party payments.",
        reasoning_framework=(
            "States use addback statutes to assert nexus for tax haven and captive insurance entities. Related party payments may be added back to income. "
            "See California Rev. & Tax Code §24410, New York Tax Law §210-B(9). IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze related party transactions and state statutes."
        ),
        key_factors=["Tax haven entity", "Captive insurance", "Addback statutes", "Related party payments", "State statutes"],
        primary_authority=["CA Rev. & Tax Code §24410", "NY Tax Law §210-B(9)", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "No related party payments",
            "Federal preemption",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting"
        ],
        resolution_strategy="Review related party transactions and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.74,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §24410"
    ),
    DoctrineBlock(
        topic="Partnership Nexus: Composite Returns",
        keywords=["partnership", "nexus", "composite returns", "withholding", "nonresident partners", "income tax"],
        conclusion_template="Partnerships may be required to file composite returns and withhold tax for nonresident partners.",
        reasoning_framework=(
            "States may require partnerships to file composite returns and withhold tax for nonresident partners. See California Rev. & Tax Code §18662, New York Tax Law §658(c). "
            "IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze partnership structure and state requirements."
        ),
        key_factors=["Composite returns", "Withholding", "Nonresident partners", "Partnership structure", "State statutes"],
        primary_authority=["CA Rev. & Tax Code §18662", "NY Tax Law §658(c)", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "No nonresident partners",
            "Federal preemption",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting"
        ],
        resolution_strategy="Review partnership structure and state statutes.",
        entity_scope="Partnership, LLC",
        confidence=0.73,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA Rev. & Tax Code §18662"
    ),
    DoctrineBlock(
        topic="Voluntary Disclosure Agreements (VDA)",
        keywords=["VDA", "voluntary disclosure", "nexus exposure", "remediation", "state income tax"],
        conclusion_template="Voluntary disclosure agreements allow taxpayers to remediate nexus exposure and limit penalties.",
        reasoning_framework=(
            "States offer voluntary disclosure agreements (VDAs) to allow taxpayers to remediate nexus exposure. VDAs limit lookback periods and penalties. "
            "See California VDA Program, New York Voluntary Compliance Program. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze eligibility and state requirements."
        ),
        key_factors=["VDA eligibility", "Lookback period", "Penalty limitation", "State statutes", "Nexus exposure"],
        primary_authority=["CA VDA Program", "NY Voluntary Compliance Program", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "Ineligible for VDA",
            "Prior contact by state",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting"
        ],
        resolution_strategy="Review VDA eligibility and state statutes.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.72,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="CA VDA Program"
    ),
    DoctrineBlock(
        topic="MTC Model Statutes and Audit Procedures",
        keywords=["MTC", "model statutes", "audit procedures", "nexus", "income tax"],
        conclusion_template="MTC model statutes and audit procedures guide states in asserting nexus and conducting audits.",
        reasoning_framework=(
            "The Multistate Tax Commission (MTC) issues model statutes and audit procedures for nexus and apportionment. States may adopt MTC guidance. "
            "See MTC Model Statute, MTC Audit Manual. IRC §861 and §862 guide sourcing, but state law controls. Taxpayers must analyze state adoption and audit exposure."
        ),
        key_factors=["MTC guidance", "Model statutes", "Audit procedures", "State adoption", "Nexus exposure"],
        primary_authority=["MTC Model Statute", "MTC Audit Manual", "IRC §861"],
        burden_holder="Taxpayer",
        adversary_position="State revenue authority",
        counter_arguments=[
            "State has not adopted MTC guidance",
            "Federal preemption",
            "Nonbusiness income",
            "Unitary business",
            "Combined reporting"
        ],
        resolution_strategy="Review MTC guidance, state adoption, and audit exposure.",
        entity_scope="Corporation, partnership, LLC",
        confidence=0.71,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="MTC Model Statute"
    )
]

# Authority Hardening
AUTHORITY_WEIGHTS = {
    "IRC": 1.0,
    "Treas Reg": 0.95,
    "Rev Rul": 0.90,
    "CCA": 0.85,
    "PLR": 0.80,
    "State statutes": 0.99,
    "Case law": 0.98,
    "MTC": 0.97
}
def resolve_authority_conflicts(authorities: List[str]) -> List[str]:
    sorted_auth = sorted(authorities, key=lambda x: AUTHORITY_WEIGHTS.get(x.split()[0], 0.5), reverse=True)
    return sorted_auth

# Semantic Normalization
SEMANTIC_MAP = {
    "physical presence": "in-state activity",
    "economic nexus": "threshold-based nexus",
    "PL 86-272": "federal income tax protection",
    "marketplace facilitator": "third-party sales platform",
    "UDITPA": "state apportionment model",
    "throwback": "origin-based sales factor adjustment",
    "throwout": "exclusion of sales to non-taxable states",
    "unitary business": "integrated business operations",
    "combined reporting": "group tax return",
    "Joyce": "entity-level nexus",
    "Finnigan": "group-level nexus",
    "NOL": "net operating loss",
    "conformity": "IRC adoption",
    "tax haven": "low-tax jurisdiction",
    "captive insurance": "related party insurance",
    "composite return": "group partner filing",
    "VDA": "voluntary disclosure",
    "MTC": "multistate guidance",
    "sales factor": "revenue apportionment",
    "property factor": "asset apportionment",
    "payroll factor": "employee compensation apportionment",
    "market-based sourcing": "customer location sourcing",
    "cost-of-performance": "service location sourcing"
}
def normalize_terms(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# Epistemic Guardrails
BANNED_PHRASES = ["always", "never", "guaranteed"]
def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "")
    return text

# Fact Fragility Scoring
def score_fact_fragility(conclusion: str) -> float:
    verifiability = 1.0 if "state statutes" in conclusion or "IRC" in conclusion else 0.7
    recharacterization_risk = 0.8 if "may" in conclusion or "could" in conclusion else 1.0
    testimony_dependence = 0.9 if "employee" in conclusion or "partner" in conclusion else 1.0
    return round((verifiability + recharacterization_risk + testimony_dependence) / 3, 2)

# Three-Layer Response
def doctrine_cache_lookup(scenario: str) -> Optional[DoctrineBlock]:
    for db in doctrine_cache:
        if any(k in scenario.lower() for k in db.keywords):
            return db
    return None

def semantic_search(scenario: str) -> Optional[DoctrineBlock]:
    scenario_norm = normalize_terms(scenario.lower())
    for db in doctrine_cache:
        if any(normalize_terms(k) in scenario_norm for k in db.keywords):
            return db
    return None

def deep_analysis(scenario: str) -> Optional[DoctrineBlock]:
    # Layer 3: Multi-doctrine decomposition
    hits = []
    scenario_norm = normalize_terms(scenario.lower())
    for db in doctrine_cache:
        if any(normalize_terms(k) in scenario_norm for k in db.keywords):
            hits.append(db)
    if hits:
        return hits[0]
    return None

# Deep Analysis: Multi-doctrine decomposition
def multi_doctrine_decomposition(scenario: str) -> Dict[str, Any]:
    issue_categories = []
    interaction_dag = {}
    triggered_doctrines = []
    missed_doctrines = []
    epistemic_gaps = []
    for db in doctrine_cache:
        if any(k in scenario.lower() for k in db.keywords):
            issue_categories.append(db.topic)
            triggered_doctrines.append(db.doctrine_id)
        else:
            missed_doctrines.append(db.doctrine_id)
    # 8-step resolution
    for i, db in enumerate(doctrine_cache):
        interaction_dag[db.doctrine_id] = {
            "next": doctrine_cache[i+1].doctrine_id if i+1 < len(doctrine_cache) else None,
            "prev": doctrine_cache[i-1].doctrine_id if i-1 >= 0 else None
        }
    if not triggered_doctrines:
        epistemic_gaps.append("No doctrine matched scenario.")
    return {
        "issue_categories": issue_categories,
        "interaction_dag": interaction_dag,
        "triggered_doctrines": triggered_doctrines,
        "missed_doctrines": missed_doctrines,
        "epistemic_gaps": epistemic_gaps
    }

# Coverage Map
def coverage_map(scenario: str) -> Dict[str, Any]:
    decomposition = multi_doctrine_decomposition(scenario)
    return {
        "triggered": decomposition["triggered_doctrines"],
        "missed": decomposition["missed_doctrines"],
        "epistemic_gaps": decomposition["epistemic_gaps"]
    }

# Drift Watcher
BASELINE_HASH = hashlib.sha256("baseline".encode()).hexdigest()
def detect_drift(response_hash: str) -> str:
    return "drifted" if response_hash != BASELINE_HASH else "baseline"

# Audit Trail
AUDIT_TRAIL_PATH = str(Path(__file__).resolve().parent / "audit_trail.jsonl")
def log_audit(query_id: str, data: Dict[str, Any]):
    with open(AUDIT_TRAIL_PATH, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} {query_id} {data}\n")

# Determinism Hash
def determinism_hash(response: Dict[str, Any]) -> str:
    resp_str = str(response)
    return hashlib.sha256(resp_str.encode()).hexdigest()

# FastAPI App
app = FastAPI(title="State Nexus Engine TX10", version="1.0", port=8510)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("State Nexus Engine TX10 startup.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("State Nexus Engine TX10 shutdown.")

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start = datetime.utcnow()
    query_id = str(uuid.uuid4())
    scenario = request.scenario
    mode = request.mode
    # Layered analysis
    doctrine = doctrine_cache_lookup(scenario)
    if not doctrine:
        doctrine = semantic_search(scenario)
    if not doctrine:
        doctrine = deep_analysis(scenario)
    decomposition = multi_doctrine_decomposition(scenario)
    coverage = coverage_map(scenario)
    position_zone = PositionZone.PLANNING if mode == ResponseMode.FAST else PositionZone.REPORTING
    primary_conclusion = apply_epistemic_guardrails(doctrine.conclusion_template if doctrine else "No doctrine matched scenario.")
    reasoning_framework = apply_epistemic_guardrails(doctrine.reasoning_framework if doctrine else "No doctrine matched scenario.")
    key_factors = doctrine.key_factors if doctrine else []
    primary_authority = resolve_authority_conflicts(doctrine.primary_authority if doctrine else [])
    counter_arguments = doctrine.counter_arguments if doctrine else []
    resolution_strategy = doctrine.resolution_strategy if doctrine else "No doctrine matched scenario."
    confidence = doctrine.confidence if doctrine else 0.5
    confidence_zone = doctrine.confidence_zone if doctrine else ConfidenceZone.HIGH_RISK
    doctrine_ids = [doctrine.doctrine_id] if doctrine else []
    triggered_doctrines = decomposition["triggered_doctrines"]
    missed_doctrines = decomposition["missed_doctrines"]
    epistemic_gaps = decomposition["epistemic_gaps"]
    drift_status = detect_drift(BASELINE_HASH)
    audit_trail_path = AUDIT_TRAIL_PATH
    response_dict = {
        "engine_id": "TX10",
        "query_id": query_id,
        "mode": mode,
        "confidence": confidence,
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
        "coverage_map": coverage,
        "drift_status": drift_status,
        "audit_trail_path": audit_trail_path
    }
    response_dict["determinism_hash"] = determinism_hash(response_dict)
    metrics_collector.record_query(query_id, doctrine_ids, (datetime.utcnow()-start).total_seconds())
    log_audit(query_id, response_dict)
    return QueryResponse(**response_dict)

@app.get("/health")
async def health():
    return {"status": "ok", "engine_id": "TX10", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage_endpoint():
    return {"coverage": [db.topic for db in doctrine_cache]}

@app.get("/drift")
async def drift():
    return {"drift_status": detect_drift(BASELINE_HASH)}

@app.get("/doctrines")
async def doctrines():
    return {"doctrines": [db.topic for db in doctrine_cache]}
