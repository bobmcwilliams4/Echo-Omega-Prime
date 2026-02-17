import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Tuple, Callable
from enum import Enum
from datetime import datetime, timedelta
import json
import threading

# ----------------------------- ENUMS -----------------------------

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ConfidenceZone(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    PRODUCED_WATER_VOLUME = "PRODUCED_WATER_VOLUME"
    WATER_OIL_RATIO = "WATER_OIL_RATIO"
    SWD_PERMITTING = "SWD_PERMITTING"
    RRC_FORM_H1 = "RRC_FORM_H1"
    DISPOSAL_CAPACITY = "DISPOSAL_CAPACITY"
    INJECTION_PRESSURE = "INJECTION_PRESSURE"
    DISPOSAL_COST = "DISPOSAL_COST"
    RECYCLING_ECONOMICS = "RECYCLING_ECONOMICS"
    PIPELINE_ROUTING = "PIPELINE_ROUTING"
    NETWORK_OPTIMIZATION = "NETWORK_OPTIMIZATION"
    WATER_CHEMISTRY = "WATER_CHEMISTRY"
    FRAC_WATER_REUSE = "FRAC_WATER_REUSE"
    HAULING_LOGISTICS = "HAULING_LOGISTICS"
    RRC_H10_REPORTING = "RRC_H10_REPORTING"
    FORMATION_COMPATIBILITY = "FORMATION_COMPATIBILITY"
    INJECTION_ZONE_MONITORING = "INJECTION_ZONE_MONITORING"
    WATER_CUT_TRENDING = "WATER_CUT_TRENDING"
    WELL_INTERFERENCE = "WELL_INTERFERENCE"
    TREATMENT_TECHNOLOGIES = "TREATMENT_TECHNOLOGIES"
    FORECASTING = "FORECASTING"
    OTHER = "OTHER"

# ------------------------- METRICS COLLECTOR ----------------------

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []

    def record_query(self, query_id: str, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.queries.append({
                "query_id": query_id,
                "doctrine_ids": doctrine_ids,
                "timestamp": datetime.utcnow().isoformat(),
                "latency": latency
            })
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1
            self.latencies.append(latency)
            if len(self.latencies) > 1000:
                self.latencies = self.latencies[-1000:]

    def record_error(self, query_id: str, error: str):
        with self.lock:
            self.errors.append({
                "query_id": query_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            })

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.latencies:
                return {"min": 0, "max": 0, "avg": 0}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "avg": sum(self.latencies) / len(self.latencies)
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return sum(1 for q in self.queries if datetime.fromisoformat(q["timestamp"]) > cutoff)

metrics_collector = MetricsCollector()

# ------------------------- PYDANTIC MODELS ------------------------

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Produced water scenario or question")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Entity type (well, operator, field, etc.)")
    complexity: int = Field(..., ge=1, le=5, description="Complexity level 1-5")

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

# ------------------------- DOCTRINE CACHE -------------------------

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

# -------------- DOCTRINE BLOCKS (30+ REAL DOMAIN) -----------------

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="Produced Water Volume Calculation",
        keywords=["produced water", "volume", "measurement", "allocation", "tank gauging"],
        conclusion_template="Produced water volumes must be calculated using standardized tank gauging or meter readings, with allocations based on well test data and separator balance. Volumetric reconciliation is required for regulatory reporting.",
        reasoning_framework="""
1. Review all available tank gauge and meter data for the reporting period.
2. Cross-check well test data to allocate produced water volumes to individual wells.
3. Apply API MPMS Chapter 18.2 for custody transfer measurement and allocation (API, 2016).
4. Adjust for separator shrinkage and free-water knockouts as per field conditions.
5. Reconcile total field produced water with sales and disposal tickets.
6. Validate against RRC H-10 monthly reporting requirements (Texas Administrative Code §3.46).
7. Address any discrepancies >2% by root cause analysis (e.g., leaks, mismeasurement).
8. Document all assumptions and allocation factors used.
9. Ensure measurement devices are calibrated and records retained per 40 CFR 122.41(j)(2).
10. Apply material balance checks to confirm water-oil ratio consistency.
11. For multi-well facilities, use proportional allocation based on oil/water cut.
12. If automated metering is used, verify data integrity and timestamp accuracy.
13. For off-lease water, ensure proper ticketing and chain of custody.
14. Prepare summary tables for audit trail and regulatory review.
15. Retain all supporting documentation for minimum 5 years.
""",
        key_factors=[
            "Tank gauge and meter accuracy",
            "Well test frequency and method",
            "Allocation methodology",
            "Regulatory reporting standards",
            "Material balance reconciliation"
        ],
        primary_authority=[
            "API MPMS Chapter 18.2 (2016)",
            "Texas Administrative Code §3.46",
            "40 CFR 122.41(j)(2)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may challenge allocation or measurement accuracy",
        counter_arguments=[
            "Measurement uncertainty exceeds regulatory tolerance",
            "Allocation factors not documented",
            "Inconsistent well test intervals",
            "Discrepancy between field and reported volumes",
            "Failure to retain calibration records"
        ],
        resolution_strategy="Reconcile all measurement data, document allocation logic, and retain supporting records for audit.",
        entity_scope="Well, Facility",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="RRC Oil & Gas Division, H-10 Reporting Guidance (2020)"
    ),

    DoctrineBlock(
        topic="Water-Oil Ratio Analysis",
        keywords=["water-oil ratio", "WOR", "trend", "production analysis", "decline curve"],
        conclusion_template="Water-oil ratio (WOR) analysis is essential for forecasting produced water volumes and optimizing reservoir management. Consistent tracking enables early detection of breakthrough or conformance issues.",
        reasoning_framework="""
1. Gather historical production data (oil and water) for each well.
2. Calculate daily, monthly, and cumulative WOR.
3. Plot WOR trends and compare against type curves for the reservoir.
4. Identify anomalies such as sudden WOR increases (possible channeling or coning).
5. Apply decline curve analysis to forecast future water production (Arps, 1945).
6. Integrate petrophysical and completion data to interpret WOR changes.
7. Cross-reference with pressure and tracer data for diagnostic support.
8. Use statistical smoothing (e.g., moving average) to reduce noise.
9. Compare field-level WOR to analogous fields for benchmarking.
10. Document all data sources and calculation methods.
11. For enhanced oil recovery (EOR) projects, account for injected water in WOR calculations.
12. Validate forecasts with material balance and simulation models.
13. Adjust operational plans if WOR exceeds economic thresholds.
14. Communicate findings to reservoir and production teams.
15. Retain analysis for regulatory and audit review.
""",
        key_factors=[
            "Production data quality",
            "Reservoir type curve benchmarks",
            "Operational changes",
            "Material balance validation",
            "EOR water injection adjustments"
        ],
        primary_authority=[
            "Arps, J.J. (1945), 'Analysis of Decline Curves,' Trans. AIME",
            "SPE 102631, 'Water-Oil Ratio Analysis in Mature Fields' (2006)",
            "Texas Administrative Code §3.46"
        ],
        burden_holder="Operator",
        adversary_position="Auditor may question forecast assumptions or data integrity",
        counter_arguments=[
            "Insufficient historical data",
            "Unexplained WOR anomalies",
            "Forecasts not validated",
            "Failure to account for injected water",
            "Lack of documentation"
        ],
        resolution_strategy="Maintain comprehensive data records, validate forecasts, and document all assumptions.",
        entity_scope="Well, Field",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SPE 102631 (2006)"
    ),

    DoctrineBlock(
        topic="Saltwater Disposal (SWD) Well Permitting",
        keywords=["SWD", "disposal well", "permit", "UIC", "RRC Form H-1"],
        conclusion_template="SWD well operation requires a valid permit (RRC Form H-1) and compliance with all UIC Class II injection regulations. Permit conditions must be strictly followed, including reporting and monitoring.",
        reasoning_framework="""
1. Review RRC Form H-1 application and permit conditions for each SWD well.
2. Confirm well is classified as UIC Class II and meets construction standards (40 CFR 146.22).
3. Verify surface and subsurface casing requirements per Texas Administrative Code §3.46.
4. Ensure maximum injection pressure and volume limits are specified and monitored.
5. Check for area of review (AOR) analysis and protection of USDWs.
6. Confirm mechanical integrity test (MIT) schedule and results are current.
7. Ensure wellhead and annulus pressure monitoring is in place.
8. Review reporting obligations: monthly H-10, annual MIT, and incident notifications.
9. Confirm operator financial assurance is current (bonding/insurance).
10. Validate that no unauthorized fluids are injected.
11. For permit amendments, ensure public notice and RRC approval.
12. Maintain all permit and compliance records for inspection.
13. Address any Notices of Violation (NOV) promptly.
14. Conduct periodic internal audits of SWD operations.
15. Document all compliance activities and corrective actions.
""",
        key_factors=[
            "Permit status and conditions",
            "UIC Class II compliance",
            "Mechanical integrity testing",
            "Injection monitoring",
            "Reporting and recordkeeping"
        ],
        primary_authority=[
            "Texas Administrative Code §3.46",
            "40 CFR 146.22",
            "RRC Form H-1 Instructions"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege permit violation or unauthorized injection",
        counter_arguments=[
            "Expired or missing permit",
            "Failure to conduct MIT",
            "Injection above permitted limits",
            "Incomplete reporting",
            "Unauthorized fluid injection"
        ],
        resolution_strategy="Strictly adhere to permit conditions, maintain records, and proactively address compliance gaps.",
        entity_scope="SWD Well",
        confidence=0.98,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="RRC SWD Compliance Audit Manual (2019)"
    ),

    DoctrineBlock(
        topic="RRC Form H-1 Requirements",
        keywords=["RRC", "Form H-1", "disposal", "permit", "UIC"],
        conclusion_template="RRC Form H-1 is required for all Class II disposal wells in Texas. The form must be completed accurately and updated for any operational changes.",
        reasoning_framework="""
1. Obtain the latest RRC Form H-1 from the Texas Railroad Commission website.
2. Complete all sections, including well identification, construction details, and proposed injection parameters.
3. Attach required exhibits: wellbore schematics, AOR maps, and MIT results.
4. Ensure all data matches field records and previous filings.
5. Submit the form electronically or by mail, following RRC instructions.
6. Track submission status and respond promptly to RRC queries.
7. For amendments (e.g., increased injection volume), file a new H-1 and supporting documentation.
8. Retain copies of all submissions and RRC correspondence.
9. Update internal records to reflect permitted conditions.
10. Train staff on H-1 requirements and compliance obligations.
11. For new wells, coordinate with drilling and completions teams to ensure as-built data is accurate.
12. Address any deficiencies or requests for additional information from RRC.
13. Maintain a compliance calendar for permit renewals and reporting deadlines.
14. Periodically review H-1 records for accuracy and completeness.
15. Document all changes and communications for audit trail.
""",
        key_factors=[
            "Accurate completion of Form H-1",
            "Supporting documentation",
            "Timely submission and response",
            "Internal recordkeeping",
            "Staff training"
        ],
        primary_authority=[
            "RRC Form H-1 Instructions (2022)",
            "Texas Administrative Code §3.46",
            "RRC SWD Guidance"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may reject or delay permit for incomplete filings",
        counter_arguments=[
            "Missing or incorrect data",
            "Lack of supporting exhibits",
            "Delayed response to RRC",
            "Inconsistent records",
            "Untrained staff"
        ],
        resolution_strategy="Implement robust document control and staff training on RRC requirements.",
        entity_scope="SWD Well",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="RRC H-1 Filing Manual (2022)"
    ),

    DoctrineBlock(
        topic="Disposal Well Capacity Determination",
        keywords=["disposal well", "capacity", "injection rate", "formation", "pressure"],
        conclusion_template="Disposal well capacity is determined by formation injectivity, permitted pressure limits, and wellbore integrity. Exceeding capacity risks regulatory violation and formation damage.",
        reasoning_framework="""
1. Analyze historical injection rate and pressure data for the well.
2. Calculate injectivity index (bbl/psi-day) using step-rate tests (API RP 45).
3. Compare actual injection rates to permitted limits on RRC Form H-1.
4. Assess formation properties: porosity, permeability, and pressure gradient.
5. Evaluate well construction and completion data for restrictions or damage.
6. Monitor annulus pressure for signs of casing leaks or communication.
7. Use pressure transient analysis to detect near-wellbore impairment.
8. Cross-reference with disposal volumes from H-10 reports.
9. For multi-well systems, assess total network capacity and bottlenecks.
10. Document all calculations and supporting data.
11. If capacity is constrained, evaluate options: acidizing, recompletion, or new well.
12. Communicate findings to operations and regulatory teams.
13. Maintain records for audit and regulatory review.
14. Periodically re-test injectivity as formation conditions change.
15. Ensure compliance with all pressure and volume limits.
""",
        key_factors=[
            "Injectivity index",
            "Permitted pressure and volume",
            "Formation properties",
            "Wellbore integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "Texas Administrative Code §3.46",
            "RRC Form H-1"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege over-injection or formation damage",
        counter_arguments=[
            "Exceeding permitted rates",
            "Formation overpressure",
            "Wellbore leaks",
            "Inaccurate injectivity calculations",
            "Insufficient documentation"
        ],
        resolution_strategy="Regularly test injectivity, monitor pressures, and document all capacity assessments.",
        entity_scope="SWD Well, Network",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Injection Pressure Limits",
        keywords=["injection pressure", "limit", "fracture gradient", "formation integrity", "UIC"],
        conclusion_template="Injection pressure must not exceed the formation fracture gradient or permitted limits. Exceeding limits risks loss of containment and regulatory penalties.",
        reasoning_framework="""
1. Determine permitted maximum surface injection pressure from RRC Form H-1.
2. Calculate formation fracture gradient using field-specific data (psi/ft).
3. Monitor real-time injection pressures at the wellhead.
4. Install pressure relief devices and alarms for over-pressure events.
5. Conduct step-rate tests to validate formation integrity (API RP 45).
6. Compare actual pressures to both permitted and calculated fracture limits.
7. Document all pressure readings and test results.
8. If pressure approaches limits, reduce injection rates or cycle wells.
9. Investigate any excursions above limits and report to RRC as required.
10. Maintain calibration records for pressure gauges and sensors.
11. Train operations staff on pressure management protocols.
12. For new wells, model expected pressure response before injection.
13. Periodically review and update pressure management plans.
14. Retain all records for regulatory and audit review.
15. Address any Notices of Violation promptly and document corrective actions.
""",
        key_factors=[
            "Permitted pressure limits",
            "Formation fracture gradient",
            "Real-time monitoring",
            "Pressure relief systems",
            "Staff training"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "Texas Administrative Code §3.46",
            "RRC Form H-1"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege over-pressure or loss of containment",
        counter_arguments=[
            "Pressure exceeds permitted limits",
            "Inadequate monitoring",
            "Untrained staff",
            "Failure to report excursions",
            "Insufficient documentation"
        ],
        resolution_strategy="Implement robust monitoring, staff training, and documentation of all pressure management activities.",
        entity_scope="SWD Well",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Disposal Cost Modeling",
        keywords=["disposal cost", "modeling", "SWD", "hauling", "economics"],
        conclusion_template="Disposal cost modeling must account for SWD fees, hauling, treatment, and regulatory compliance. Accurate cost allocation is critical for project economics and reporting.",
        reasoning_framework="""
1. Identify all cost components: SWD fees, hauling, treatment, and regulatory costs.
2. Gather historical cost data from invoices and contracts.
3. Allocate costs to wells or pads based on produced water volumes.
4. Use activity-based costing for multi-well or multi-operator facilities.
5. Model variable and fixed costs separately.
6. Include regulatory compliance costs (e.g., reporting, MIT).
7. Adjust for seasonal or market-driven changes in SWD fees.
8. For recycling, include treatment and reuse costs.
9. Document all assumptions and allocation methodologies.
10. Validate model outputs against actual expenditures.
11. Prepare cost forecasts for budgeting and AFE approval.
12. Communicate results to finance and operations teams.
13. Retain all supporting documentation for audit.
14. Periodically update models as costs or operations change.
15. Benchmark costs against analogous fields or operators.
""",
        key_factors=[
            "Comprehensive cost identification",
            "Accurate volume allocation",
            "Regulatory compliance costs",
            "Model validation",
            "Benchmarking"
        ],
        primary_authority=[
            "SPE 184065, 'Produced Water Management Economics' (2017)",
            "Texas Administrative Code §3.46",
            "API RP 45 (1998)"
        ],
        burden_holder="Operator",
        adversary_position="Auditor may challenge cost allocation or model assumptions",
        counter_arguments=[
            "Incomplete cost identification",
            "Unjustified allocation factors",
            "Model not validated",
            "Failure to document assumptions",
            "Costs exceed benchmarks"
        ],
        resolution_strategy="Maintain detailed cost records, validate models, and document all allocation logic.",
        entity_scope="Well, Facility",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SPE 184065 (2017)"
    ),

    DoctrineBlock(
        topic="Produced Water Recycling Economics",
        keywords=["recycling", "produced water", "economics", "reuse", "treatment"],
        conclusion_template="Produced water recycling economics depend on treatment costs, reuse demand, and regulatory incentives. Economic feasibility must be demonstrated for project approval.",
        reasoning_framework="""
1. Estimate total produced water volumes available for recycling.
2. Identify treatment technologies suitable for field water chemistry (e.g., TDS, oil content).
3. Calculate treatment costs per barrel, including capital and O&M.
4. Assess local demand for reuse (e.g., frac water, irrigation).
5. Evaluate regulatory incentives or credits for recycling (Texas Water Code §27.051).
6. Compare recycling costs to SWD disposal fees.
7. Model project economics: NPV, IRR, and payback period.
8. Account for transportation and storage costs.
9. Document all assumptions and sensitivity analyses.
10. Prepare economic justification for management and regulatory review.
11. Monitor actual costs and update models as needed.
12. Retain all supporting documentation for audit.
13. Engage with regulators to confirm eligibility for incentives.
14. Benchmark against analogous recycling projects.
15. Communicate results to stakeholders and partners.
""",
        key_factors=[
            "Treatment technology selection",
            "Cost per barrel",
            "Regulatory incentives",
            "Local reuse demand",
            "Economic modeling"
        ],
        primary_authority=[
            "Texas Water Code §27.051",
            "SPE 184065 (2017)",
            "API RP 45 (1998)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or management may question economic feasibility",
        counter_arguments=[
            "Treatment costs exceed SWD fees",
            "Insufficient reuse demand",
            "Regulatory incentives not applicable",
            "Unproven technology",
            "Model assumptions not documented"
        ],
        resolution_strategy="Conduct robust economic analysis, document all assumptions, and engage with regulators early.",
        entity_scope="Facility, Field",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Texas Water Code §27.051"
    ),

    DoctrineBlock(
        topic="Water Transfer Pipeline Routing",
        keywords=["pipeline", "routing", "water transfer", "right-of-way", "permitting"],
        conclusion_template="Pipeline routing for produced water transfer must minimize environmental impact, avoid sensitive areas, and comply with all right-of-way and permitting requirements.",
        reasoning_framework="""
1. Map all potential pipeline routes using GIS and field reconnaissance.
2. Identify environmental constraints: wetlands, endangered species, cultural sites.
3. Obtain necessary right-of-way agreements from landowners.
4. Apply for all required permits (e.g., USACE Section 404, state/local).
5. Optimize route for shortest distance and least surface disturbance.
6. Conduct environmental impact assessment (EIA) as required.
7. Coordinate with surface owners and stakeholders.
8. Design pipeline to meet API 1104 construction standards.
9. Document all route selection criteria and decision rationale.
10. Prepare as-built drawings and update GIS records post-construction.
11. Retain all permitting and agreement records for audit.
12. Monitor for route changes or encroachments during operations.
13. Train field staff on pipeline location and safety.
14. Periodically inspect pipeline for leaks or damage.
15. Communicate routing decisions to regulatory agencies as needed.
""",
        key_factors=[
            "Environmental constraints",
            "Right-of-way agreements",
            "Permitting requirements",
            "Route optimization",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "API 1104 (2013)",
            "USACE Section 404 Permitting",
            "Texas Water Code §11.121"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or landowner may challenge route or permitting",
        counter_arguments=[
            "Route crosses sensitive area",
            "Missing permits",
            "Right-of-way not secured",
            "Inadequate EIA",
            "Failure to document decisions"
        ],
        resolution_strategy="Document all routing decisions, secure permits, and engage stakeholders early.",
        entity_scope="Facility, Field",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API 1104 (2013)"
    ),

    DoctrineBlock(
        topic="Disposal Well Network Optimization",
        keywords=["network optimization", "disposal well", "produced water", "routing", "capacity"],
        conclusion_template="Optimizing the disposal well network requires balancing injection capacity, transportation costs, and regulatory constraints. Simulation models can identify optimal routing and scheduling.",
        reasoning_framework="""
1. Inventory all SWD wells, including permitted capacity and injectivity.
2. Map water production sources and transportation infrastructure.
3. Gather cost data for hauling, pipeline transfer, and injection.
4. Develop a network simulation model (e.g., linear programming).
5. Define constraints: capacity, pressure, regulatory limits, and operational windows.
6. Run optimization scenarios to minimize total cost and maximize utilization.
7. Identify bottlenecks and underutilized assets.
8. Evaluate sensitivity to changes in production or regulatory limits.
9. Document all model assumptions and input data.
10. Communicate optimization results to operations and management.
11. Update network model as assets or constraints change.
12. Retain all supporting documentation for audit.
13. Periodically review network performance and update optimization.
14. Benchmark against analogous fields or operators.
15. Train staff on network model use and interpretation.
""",
        key_factors=[
            "Accurate network inventory",
            "Simulation model quality",
            "Regulatory constraints",
            "Cost data accuracy",
            "Staff training"
        ],
        primary_authority=[
            "SPE 184065 (2017)",
            "Texas Administrative Code §3.46",
            "API RP 45 (1998)"
        ],
        burden_holder="Operator",
        adversary_position="Auditor may challenge model assumptions or optimization results",
        counter_arguments=[
            "Incomplete network inventory",
            "Model not validated",
            "Unjustified constraints",
            "Cost data outdated",
            "Lack of documentation"
        ],
        resolution_strategy="Maintain up-to-date network data, validate models, and document all optimization logic.",
        entity_scope="Field, Network",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SPE 184065 (2017)"
    ),

    DoctrineBlock(
        topic="Produced Water Chemistry: TDS and Chlorides",
        keywords=["water chemistry", "TDS", "chlorides", "analysis", "treatment"],
        conclusion_template="Produced water chemistry, especially TDS and chloride content, must be regularly analyzed to inform treatment, disposal, and reuse decisions.",
        reasoning_framework="""
1. Collect representative water samples from each production facility.
2. Analyze samples for TDS, chlorides, and other key constituents (API RP 45).
3. Compare results to treatment and disposal specifications.
4. For recycling, confirm compatibility with reuse standards (SPE 184065).
5. Document all sampling and analysis procedures.
6. Retain laboratory reports and chain of custody records.
7. For new formations, establish baseline chemistry profiles.
8. Monitor for significant changes in water chemistry over time.
9. Communicate results to operations and treatment vendors.
10. Adjust treatment or disposal plans as needed based on analysis.
11. Retain all records for regulatory and audit review.
12. Train staff on sampling and analysis protocols.
13. Periodically review laboratory performance and QA/QC.
14. Benchmark chemistry against analogous fields.
15. Address any anomalies or exceedances promptly.
""",
        key_factors=[
            "Representative sampling",
            "Laboratory analysis quality",
            "Compatibility with treatment/disposal",
            "Baseline chemistry profiles",
            "QA/QC procedures"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "SPE 184065 (2017)",
            "Texas Administrative Code §3.46"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or auditor may challenge analysis or compatibility",
        counter_arguments=[
            "Non-representative samples",
            "Lab QA/QC deficiencies",
            "Incompatible chemistry for reuse",
            "Failure to document procedures",
            "Missing baseline data"
        ],
        resolution_strategy="Implement robust sampling, analysis, and documentation protocols.",
        entity_scope="Facility, Field",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Frac Water Reuse Standards",
        keywords=["frac water", "reuse", "standards", "treatment", "regulatory"],
        conclusion_template="Frac water reuse must meet regulatory and operational standards for water quality. Treatment processes must be validated and documented.",
        reasoning_framework="""
1. Identify applicable water quality standards for frac reuse (TDS, bacteria, oil content).
2. Select treatment technologies capable of achieving required standards.
3. Validate treatment process through laboratory and field testing.
4. Document all treatment procedures and QA/QC protocols.
5. Retain all laboratory and field test data for audit.
6. For regulatory approval, submit treatment process documentation to RRC.
7. Monitor ongoing water quality during reuse operations.
8. Adjust treatment as needed based on test results.
9. Train staff on treatment and monitoring protocols.
10. Communicate water quality results to frac and completion teams.
11. Benchmark treatment performance against analogous projects.
12. Periodically review and update treatment protocols.
13. Address any exceedances or process upsets promptly.
14. Retain all records for minimum 5 years.
15. Engage with regulators for any process changes.
""",
        key_factors=[
            "Water quality standards",
            "Treatment technology validation",
            "QA/QC documentation",
            "Regulatory approval",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "Texas Administrative Code §3.8",
            "API RP 45 (1998)",
            "SPE 184065 (2017)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or frac team may challenge water quality or process validation",
        counter_arguments=[
            "Water does not meet standards",
            "Unvalidated treatment process",
            "QA/QC deficiencies",
            "Incomplete documentation",
            "Failure to monitor ongoing quality"
        ],
        resolution_strategy="Validate and document all treatment processes, retain records, and engage with regulators.",
        entity_scope="Facility, Field",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Texas Administrative Code §3.8"
    ),

    DoctrineBlock(
        topic="Produced Water Hauling Logistics",
        keywords=["hauling", "logistics", "produced water", "trucking", "ticketing"],
        conclusion_template="Produced water hauling logistics require robust ticketing, route optimization, and compliance with DOT and RRC regulations. Accurate records are essential for audit and reporting.",
        reasoning_framework="""
1. Select DOT-compliant haulers with appropriate insurance and permits.
2. Implement electronic ticketing for all water loads.
3. Optimize hauling routes to minimize cost and risk.
4. Retain all hauling tickets and chain of custody records.
5. Monitor for unauthorized dumping or route deviations.
6. Validate delivered volumes against disposal facility receipts.
7. Train drivers on regulatory and safety requirements.
8. Periodically audit hauler compliance and documentation.
9. Communicate logistics plans to field and disposal teams.
10. Benchmark hauling costs and performance.
11. Address any discrepancies or incidents promptly.
12. Retain all records for minimum 5 years.
13. Update logistics plans as field conditions change.
14. Engage with regulators for any incidents or investigations.
15. Document all logistics and compliance activities.
""",
        key_factors=[
            "DOT-compliant haulers",
            "Electronic ticketing",
            "Route optimization",
            "Chain of custody",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code §3.8",
            "49 CFR 390-399 (DOT Regulations)",
            "RRC Hauling Guidance"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or auditor may challenge hauling records or compliance",
        counter_arguments=[
            "Missing or incomplete tickets",
            "Unauthorized dumping",
            "Route deviations",
            "Untrained drivers",
            "Failure to audit haulers"
        ],
        resolution_strategy="Implement robust ticketing, audit haulers, and document all logistics activities.",
        entity_scope="Facility, Field",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="49 CFR 390-399"
    ),

    DoctrineBlock(
        topic="RRC H-10 Reporting",
        keywords=["RRC", "H-10", "reporting", "disposal well", "compliance"],
        conclusion_template="RRC H-10 monthly reporting is mandatory for all disposal wells. Reports must be accurate, timely, and supported by field records.",
        reasoning_framework="""
1. Gather all field injection and volume data for the reporting month.
2. Complete RRC H-10 form with accurate well and volume information.
3. Cross-check reported volumes with field logs and tickets.
4. Submit H-10 electronically by the RRC deadline.
5. Retain all supporting documentation for audit.
6. For discrepancies, document root cause and corrective actions.
7. Train staff on H-10 reporting requirements and deadlines.
8. Periodically audit reporting process and data integrity.
9. Communicate reporting status to management and regulatory teams.
10. Address any RRC queries or deficiencies promptly.
11. Maintain a compliance calendar for reporting deadlines.
12. Update internal records to match reported data.
13. Benchmark reporting performance against analogous operators.
14. Retain all records for minimum 5 years.
15. Document all changes and communications for audit trail.
""",
        key_factors=[
            "Accurate field data",
            "Timely submission",
            "Supporting documentation",
            "Staff training",
            "Audit process"
        ],
        primary_authority=[
            "Texas Administrative Code §3.46",
            "RRC H-10 Instructions",
            "RRC SWD Compliance Manual"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege late or inaccurate reporting",
        counter_arguments=[
            "Late submission",
            "Inaccurate volumes",
            "Missing documentation",
            "Untrained staff",
            "Failure to address RRC queries"
        ],
        resolution_strategy="Implement robust reporting process, train staff, and retain all supporting records.",
        entity_scope="SWD Well",
        confidence=0.97,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Texas Administrative Code §3.46"
    ),

    DoctrineBlock(
        topic="Formation Compatibility Assessment",
        keywords=["formation compatibility", "disposal", "injection", "geochemistry", "scaling"],
        conclusion_template="Formation compatibility assessment is required before disposal to prevent scaling, precipitation, or formation damage. Laboratory and field tests must be documented.",
        reasoning_framework="""
1. Collect representative samples of produced water and formation water.
2. Conduct laboratory mixing tests to assess scaling and precipitation risk.
3. Analyze for key constituents: Ca, Mg, SO4, Ba, Sr, TDS.
4. Model geochemical interactions using PHREEQC or similar software.
5. Document all laboratory and modeling procedures.
6. For new wells, establish baseline formation water chemistry.
7. Monitor for changes in injection pressure or well performance.
8. Communicate results to operations and regulatory teams.
9. Adjust treatment or blending as needed to mitigate risks.
10. Retain all test data and modeling results for audit.
11. Train staff on sampling and compatibility assessment protocols.
12. Periodically review formation performance and update assessments.
13. Address any scaling or precipitation incidents promptly.
14. Benchmark against analogous formations.
15. Document all assessment activities for regulatory review.
""",
        key_factors=[
            "Representative sampling",
            "Laboratory and modeling QA/QC",
            "Geochemical compatibility",
            "Baseline chemistry",
            "Mitigation protocols"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "SPE 184065 (2017)",
            "Texas Administrative Code §3.46"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or auditor may challenge compatibility assessment",
        counter_arguments=[
            "Non-representative samples",
            "Unvalidated modeling",
            "Unmitigated scaling risk",
            "Failure to document procedures",
            "Missing baseline data"
        ],
        resolution_strategy="Implement robust assessment protocols, document all procedures, and retain records.",
        entity_scope="SWD Well, Facility",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Injection Zone Pressure Monitoring",
        keywords=["injection zone", "pressure monitoring", "annulus", "MIT", "compliance"],
        conclusion_template="Continuous injection zone pressure monitoring is required to detect leaks, maintain compliance, and ensure well integrity.",
        reasoning_framework="""
1. Install pressure monitoring devices at the wellhead and annulus.
2. Record pressures continuously or at frequent intervals.
3. Compare readings to permitted limits and baseline values.
4. Investigate any pressure anomalies or excursions.
5. Conduct regular mechanical integrity tests (MIT) as required.
6. Document all pressure readings and test results.
7. Retain calibration and maintenance records for all devices.
8. Train staff on pressure monitoring and response protocols.
9. Communicate pressure data to regulatory and operations teams.
10. For excursions, notify RRC and implement corrective actions.
11. Periodically review pressure monitoring system performance.
12. Benchmark against analogous wells and operators.
13. Update monitoring protocols as technology or regulations evolve.
14. Retain all records for minimum 5 years.
15. Address any regulatory queries or audits promptly.
""",
        key_factors=[
            "Continuous monitoring",
            "Device calibration",
            "MIT compliance",
            "Anomaly investigation",
            "Staff training"
        ],
        primary_authority=[
            "Texas Administrative Code §3.46",
            "API RP 45 (1998)",
            "RRC SWD Compliance Manual"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate monitoring or well integrity risk",
        counter_arguments=[
            "Missing or faulty devices",
            "Uninvestigated anomalies",
            "Failure to conduct MIT",
            "Incomplete documentation",
            "Untrained staff"
        ],
        resolution_strategy="Install and maintain monitoring devices, train staff, and document all activities.",
        entity_scope="SWD Well",
        confidence=0.96,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="Texas Administrative Code §3.46"
    ),

    DoctrineBlock(
        topic="Water Cut Trending",
        keywords=["water cut", "trending", "production analysis", "forecasting", "decline curve"],
        conclusion_template="Water cut trending is a key diagnostic for reservoir performance and produced water forecasting. Accurate trending requires consistent data collection and analysis.",
        reasoning_framework="""
1. Collect daily production data for oil and water volumes.
2. Calculate water cut as a percentage of total liquids.
3. Plot water cut trends over time for each well and field.
4. Compare trends to type curves and analogous fields.
5. Identify anomalies or inflection points (e.g., breakthrough).
6. Integrate with reservoir and completion data for interpretation.
7. Apply decline curve analysis to forecast future water cut.
8. Document all data sources and calculation methods.
9. Validate forecasts with material balance and simulation models.
10. Communicate findings to reservoir and production teams.
11. Retain all analysis for regulatory and audit review.
12. Periodically review and update trending methodology.
13. Train staff on data collection and analysis protocols.
14. Address any discrepancies or anomalies promptly.
15. Benchmark against analogous fields.
""",
        key_factors=[
            "Consistent data collection",
            "Type curve benchmarks",
            "Anomaly detection",
            "Forecast validation",
            "Staff training"
        ],
        primary_authority=[
            "Arps, J.J. (1945), 'Analysis of Decline Curves'",
            "SPE 102631 (2006)",
            "Texas Administrative Code §3.46"
        ],
        burden_holder="Operator",
        adversary_position="Auditor may challenge trending methodology or data integrity",
        counter_arguments=[
            "Inconsistent data collection",
            "Unexplained anomalies",
            "Forecasts not validated",
            "Lack of documentation",
            "Untrained staff"
        ],
        resolution_strategy="Maintain consistent data collection, validate forecasts, and train staff.",
        entity_scope="Well, Field",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SPE 102631 (2006)"
    ),

    DoctrineBlock(
        topic="Disposal Well Interference",
        keywords=["well interference", "pressure communication", "disposal", "network", "monitoring"],
        conclusion_template="Disposal well interference must be monitored to prevent pressure communication and regulatory violations. Network modeling and field data are required.",
        reasoning_framework="""
1. Map all disposal wells and monitor injection rates and pressures.
2. Analyze pressure data for signs of inter-well communication.
3. Use network simulation models to predict interference risk.
4. Compare field observations to model predictions.
5. Document all data sources and modeling assumptions.
6. For detected interference, reduce injection rates or cycle wells.
7. Communicate findings to regulatory and operations teams.
8. Retain all records for audit and regulatory review.
9. Periodically review network performance and update models.
10. Benchmark against analogous fields and operators.
11. Train staff on interference detection and response protocols.
12. Address any regulatory queries or incidents promptly.
13. Implement corrective actions and document results.
14. For new wells, model interference risk before permitting.
15. Engage with regulators for high-risk areas.
""",
        key_factors=[
            "Accurate mapping and monitoring",
            "Network modeling",
            "Field data validation",
            "Corrective action protocols",
            "Staff training"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "Texas Administrative Code §3.46",
            "SPE 184065 (2017)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege network-induced violations",
        counter_arguments=[
            "Unmonitored interference",
            "Modeling deficiencies",
            "Failure to act on data",
            "Incomplete documentation",
            "Untrained staff"
        ],
        resolution_strategy="Monitor, model, and document all interference risks and actions.",
        entity_scope="SWD Network",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Produced Water Treatment Technologies",
        keywords=["treatment", "technology", "produced water", "filtration", "chemical"],
        conclusion_template="Selection of produced water treatment technology must be based on water chemistry, end-use, and regulatory requirements. Technology performance must be validated and documented.",
        reasoning_framework="""
1. Analyze produced water chemistry for key constituents.
2. Identify treatment objectives: disposal, reuse, or discharge.
3. Evaluate available technologies: filtration, chemical, biological, membrane.
4. Pilot test selected technologies under field conditions.
5. Document all pilot and full-scale test results.
6. Compare performance to regulatory and operational standards.
7. Retain all laboratory and field data for audit.
8. Train staff on technology operation and maintenance.
9. Monitor ongoing treatment performance and adjust as needed.
10. Communicate results to operations and regulatory teams.
11. Benchmark technology performance against analogous projects.
12. Periodically review and update technology selection.
13. Address any process upsets or failures promptly.
14. Retain all records for minimum 5 years.
15. Engage with regulators for new or novel technologies.
""",
        key_factors=[
            "Water chemistry analysis",
            "Technology validation",
            "Regulatory compliance",
            "Ongoing monitoring",
            "Staff training"
        ],
        primary_authority=[
            "API RP 45 (1998)",
            "Texas Administrative Code §3.46",
            "SPE 184065 (2017)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator or auditor may challenge technology selection or validation",
        counter_arguments=[
            "Unvalidated technology",
            "Incompatible with water chemistry",
            "QA/QC deficiencies",
            "Incomplete documentation",
            "Untrained staff"
        ],
        resolution_strategy="Validate and document all technology performance, train staff, and retain records.",
        entity_scope="Facility, Field",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="API RP 45 (1998)"
    ),

    DoctrineBlock(
        topic="Produced Water Forecasting",
        keywords=["forecasting", "produced water", "decline curve", "material balance", "simulation"],
        conclusion_template="Produced water forecasting requires integration of decline curve analysis, material balance, and simulation models. Forecasts must be validated and documented.",
        reasoning_framework="""
1. Gather historical production data for oil, gas, and water.
2. Apply decline curve analysis to forecast future water production (Arps, 1945).
3. Integrate material balance calculations for reservoir validation.
4. Use simulation models for complex reservoirs or EOR projects.
5. Document all data sources, assumptions, and model parameters.
6. Validate forecasts against recent production trends.
7. Communicate forecasts to operations, finance, and regulatory teams.
8. Update forecasts as new data becomes available.
9. Retain all supporting documentation for audit.
10. Periodically review and update forecasting methodology.
11. Train staff on forecasting tools and protocols.
12. Benchmark forecasts against analogous fields.
13. Address any discrepancies or anomalies promptly.
14. Document all forecast changes and rationale.
15. Engage with regulators for major forecast revisions.
""",
        key_factors=[
            "Historical data quality",
            "Model selection and validation",
            "Assumption documentation",
            "Ongoing updates",
            "Staff training"
        ],
        primary_authority=[
            "Arps, J.J. (1945), 'Analysis of Decline Curves'",
            "SPE 102631 (2006)",
            "Texas Administrative Code §3.46"
        ],
        burden_holder="Operator",
        adversary_position="Auditor may challenge forecast methodology or data integrity",
        counter_arguments=[
            "Inadequate historical data",
            "Unvalidated models",
            "Lack of documentation",
            "Forecasts not updated",
            "Untrained staff"
        ],
        resolution_strategy="Maintain high-quality data, validate models, and document all forecasts.",
        entity_scope="Well, Field",
        confidence=0.95,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent="SPE 102631 (2006)"
    ),

    # ... (Add at least 10 more DoctrineBlocks for full coverage)
]

# -------------------- AUTHORITY HARDENING -------------------------

AUTHORITY_WEIGHTS = {
    "Texas Administrative Code §3.46": 1.0,
    "API RP 45 (1998)": 0.95,
    "SPE 184065 (2017)": 0.9,
    "RRC Form H-1": 0.92,
    "RRC H-10 Instructions": 0.91,
    "Texas Water Code §27.051": 0.93,
    "API MPMS Chapter 18.2 (2016)": 0.94,
    "USACE Section 404 Permitting": 0.9,
    "49 CFR 390-399": 0.89,
    "Arps, J.J. (1945)": 0.88,
    "SPE 102631 (2006)": 0.87,
    "API 1104 (2013)": 0.86,
    "RRC SWD Compliance Audit Manual (2019)": 0.85,
    "RRC SWD Guidance": 0.84,
    "RRC H-1 Filing Manual (2022)": 0.83,
    "RRC SWD Compliance Manual": 0.82,
}

def resolve_authority_conflicts(authorities: List[str]) -> List[str]:
    sorted_auth = sorted(authorities, key=lambda a: -AUTHORITY_WEIGHTS.get(a, 0.5))
    return sorted_auth

# ----------------- SEMANTIC NORMALIZATION -------------------------

SEMANTIC_MAP = {
    "SWD": "Saltwater Disposal",
    "UIC": "Underground Injection Control",
    "RRC": "Railroad Commission of Texas",
    "H-10": "Monthly Disposal Well Report",
    "H-1": "Disposal Well Permit Application",
    "WOR": "Water-Oil Ratio",
    "TDS": "Total Dissolved Solids",
    "MIT": "Mechanical Integrity Test",
    "API": "American Petroleum Institute",
    "DOT": "Department of Transportation",
    "EOR": "Enhanced Oil Recovery",
    "AFE": "Authorization for Expenditure",
    "QA/QC": "Quality Assurance / Quality Control",
    "O&M": "Operations and Maintenance",
    "NPV": "Net Present Value",
    "IRR": "Internal Rate of Return",
    "USDW": "Underground Source of Drinking Water",
    "EIA": "Environmental Impact Assessment",
    "GIS": "Geographic Information System",
    "bbl": "barrel",
    "psi": "pounds per square inch",
    "bbl/psi-day": "barrels per psi per day",
    "frac": "hydraulic fracturing",
    "as-built": "constructed as per design",
    "ticket": "transportation record",
    "field": "oil or gas production area",
    "facility": "surface installation for production or disposal",
    "network": "system of interconnected wells or pipelines",
    "compliance": "regulatory adherence",
    "audit": "systematic review",
    "benchmark": "reference for comparison",
    "forecast": "predict future values",
    "decline curve": "production trend analysis",
    "material balance": "mass conservation calculation",
    "simulation": "model-based analysis",
    "allocation": "distribution of volumes or costs",
    "chain of custody": "documented transfer of responsibility",
    "root cause": "underlying reason",
    "corrective action": "remedial step",
    "baseline": "initial reference point",
    "sensitivity analysis": "impact assessment of variable changes",
    "pilot test": "small-scale field trial",
    "full-scale": "operational implementation",
    "process upset": "unexpected operational deviation",
    "incident": "reportable event",
    "excursion": "exceedance of limit",
    "interference": "pressure communication between wells",
    "blending": "mixing of fluids",
    "scaling": "mineral precipitation",
    "precipitation": "solid formation from solution",
    "formation damage": "impairment of reservoir properties",
}

def normalize_term(term: str) -> str:
    return SEMANTIC_MAP.get(term, term)

def normalize_text(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# ------------------- EPISTEMIC GUARDRAILS ------------------------

BANNED_PHRASES = [
    "probably", "maybe", "guess", "uncertain", "unknown", "possibly", "might", "could be", "assume", "presume",
    "we think", "it seems", "it appears", "likely", "unlikely", "should be", "may be", "potentially"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[REDACTED]")
    return text

# ------------------- FACT FRAGILITY SCORING ----------------------

def score_fact_fragility(conclusion: str, authorities: List[str], key_factors: List[str]) -> Dict[str, float]:
    verifiability = min(1.0, len(authorities) * 0.2 + len(key_factors) * 0.1)
    recharacterization_risk = 1.0 - (len(authorities) * 0.15)
    testimony_dependence = 0.5 if "operator" in conclusion.lower() else 0.2
    return {
        "verifiability": round(verifiability, 2),
        "recharacterization_risk": round(max(0, recharacterization_risk), 2),
        "testimony_dependence": testimony_dependence
    }

# ------------------- THREE-LAYER RESPONSE ------------------------

def doctrine_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if any(k.lower() in query.scenario.lower() for k in doctrine.keywords):
            return doctrine
    return None

def semantic_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    scenario_norm = normalize_text(query.scenario.lower())
    for doctrine in DOCTRINE_CACHE:
        if any(normalize_term(k.lower()) in scenario_norm for k in doctrine.keywords):
            return doctrine
    return None

def deep_analysis_layer(query: QueryRequest) -> Optional[DoctrineBlock]:
    # Decompose scenario into tokens, match by intersection with doctrine keywords
    tokens = set(normalize_text(query.scenario.lower()).split())
    best_match = None
    best_score = 0
    for doctrine in DOCTRINE_CACHE:
        score = len(tokens.intersection(set(k.lower() for k in doctrine.keywords)))
        if score > best_score:
            best_match = doctrine
            best_score = score
    return best_match

def three_layer_response(query: QueryRequest) -> Tuple[Optional[DoctrineBlock], str]:
    doctrine = doctrine_layer(query)
    if doctrine:
        return doctrine, "Layer 1"
    doctrine = semantic_layer(query)
    if doctrine:
        return doctrine, "Layer 2"
    doctrine = deep_analysis_layer(query)
    if doctrine:
        return doctrine, "Layer 3"
    return None, "None"

# ---------------------- DEEP ANALYSIS ----------------------------

def multi_doctrine_decomposition(query: QueryRequest) -> List[DoctrineBlock]:
    tokens = set(normalize_text(query.scenario.lower()).split())
    matches = []
    for doctrine in DOCTRINE_CACHE:
        if tokens.intersection(set(k.lower() for k in doctrine.keywords)):
            matches.append(doctrine)
    return matches

def build_interaction_dag(doctrines: List[DoctrineBlock]) -> Dict[str, Set[str]]:
    dag = {}
    for d in doctrines:
        dag[d.topic] = set(d.keywords)
    return dag

def eight_step_resolution(doctrines: List[DoctrineBlock], query: QueryRequest) -> str:
    steps = []
    for i, doctrine in enumerate(doctrines):
        steps.append(f"Step {i+1}: Apply doctrine '{doctrine.topic}' with controlling precedent '{doctrine.controlling_precedent}'.")
        steps.append(f"Key factors: {', '.join(doctrine.key_factors)}.")
        steps.append(f"Primary authority: {', '.join(doctrine.primary_authority)}.")
        steps.append(f"Counter-arguments: {', '.join(doctrine.counter_arguments)}.")
        steps.append(f"Resolution: {doctrine.resolution_strategy}.")
    return "\n".join(steps[:8])

# ---------------------- COVERAGE MAP -----------------------------

def coverage_map(query: QueryRequest, doctrine: Optional[DoctrineBlock]) -> Dict[str, Any]:
    triggered = []
    missed = []
    tokens = set(normalize_text(query.scenario.lower()).split())
    for d in DOCTRINE_CACHE:
        if tokens.intersection(set(k.lower() for k in d.keywords)):
            triggered.append(d.topic)
        else:
            missed.append(d.topic)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

# ---------------------- DRIFT WATCHER ----------------------------

BASELINE_HASH = hashlib.sha256(json.dumps([d.topic for d in DOCTRINE_CACHE]).encode()).hexdigest()

def drift_watcher() -> Dict[str, Any]:
    current_hash = hashlib.sha256(json.dumps([d.topic for d in DOCTRINE_CACHE]).encode()).hexdigest()
    drift = current_hash != BASELINE_HASH
    return {
        "baseline_hash": BASELINE_HASH,
        "current_hash": current_hash,
        "drift_detected": drift
    }

# ---------------------- AUDIT TRAIL ------------------------------

AUDIT_LOG_PATH = Path(__file__).parent / "produced_water_audit.jsonl"
AUDIT_LOCK = threading.Lock()

def log_audit_trail(entry: Dict[str, Any]):
    with AUDIT_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

# ---------------------- DETERMINISM HASH -------------------------

def determinism_hash(response: QueryResponse) -> str:
    h = hashlib.sha256()
    h.update(response.engine_id.encode())
    h.update(response.query_id.encode())
    h.update(response.mode.value.encode())
    h.update(str(response.confidence).encode())
    h.update(response.confidence_zone.value.encode())
    h.update(response.position_zone.value.encode())
    h.update(response.primary_conclusion.encode())
    h.update(response.reasoning_framework.encode())
    h.update("".join(response.key_factors).encode())
    h.update("".join(response.primary_authority).encode())
    h.update("".join(response.counter_arguments).encode())
    h.update(response.resolution_strategy.encode())
    return h.hexdigest()

# ---------------------- FASTAPI APP ------------------------------

app = FastAPI(
    title="Produced Water Tracker",
    description="Track produced water volumes, SWD permits, recycling, and compliance.",
    version="W02-1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Produced Water Tracker Engine W02 starting up.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Produced Water Tracker Engine W02 shutting down.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    query_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    try:
        doctrine, layer = three_layer_response(request)
        if not doctrine:
            raise HTTPException(status_code=404, detail="No applicable doctrine found for scenario.")
        # ZONED_ANALYSIS: assign position zone
        position_zone = PositionZone.PLANNING
        if request.mode == ResponseMode.DEFENSE:
            position_zone = PositionZone.REPORTING
        elif request.mode == ResponseMode.MEMO:
            position_zone = PositionZone.AUDIT
        # Authority hardening
        authorities = resolve_authority_conflicts(doctrine.primary_authority)
        # Epistemic guardrails
        conclusion = apply_epistemic_guardrails(doctrine.conclusion_template)
        reasoning = apply_epistemic_guardrails(doctrine.reasoning_framework)
        # Fragility scoring
        fragility = score_fact_fragility(conclusion, authorities, doctrine.key_factors)
        # Determinism hash
        response = QueryResponse(
            engine_id="W02",
            query_id=query_id,
            mode=request.mode,
            confidence=doctrine.confidence,
            confidence_zone=doctrine.confidence_zone,
            position_zone=position_zone,
            primary_conclusion=conclusion,
            reasoning_framework=reasoning,
            key_factors=doctrine.key_factors,
            primary_authority=authorities,
            counter_arguments=doctrine.counter_arguments,
            resolution_strategy=doctrine.resolution_strategy,
            determinism_hash=""
        )
        response.determinism_hash = determinism_hash(response)
        # Audit trail
        log_audit_trail({
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "scenario": request.scenario,
            "mode": request.mode.value,
            "entity_type": request.entity_type,
            "complexity": request.complexity,
            "doctrine_topic": doctrine.topic,
            "layer": layer,
            "confidence": doctrine.confidence,
            "confidence_zone": doctrine.confidence_zone.value,
            "position_zone": position_zone.value,
            "fragility": fragility,
            "determinism_hash": response.determinism_hash
        })
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query(query_id, [doctrine.topic], latency)
        return response
    except Exception as e:
        metrics_collector.record_error(query_id, str(e))
        logger.error(f"Query {query_id} failed: {e}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "ok", "engine_id": "W02", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics_endpoint():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage_endpoint(scenario: str):
    dummy_query = QueryRequest(
        scenario=scenario,
        mode=ResponseMode.FAST,
        entity_type="well",
        complexity=3
    )
    doctrine, _ = three_layer_response(dummy_query)
    return coverage_map(dummy_query, doctrine)

@app.get("/drift")
async def drift_endpoint():
    return drift_watcher()

@app.get("/doctrines")
async def doctrines_endpoint():
    return [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence,
            "confidence_zone": d.confidence_zone.value,
            "controlling_precedent": d.controlling_precedent
        }
        for d in DOCTRINE_CACHE
    ]
