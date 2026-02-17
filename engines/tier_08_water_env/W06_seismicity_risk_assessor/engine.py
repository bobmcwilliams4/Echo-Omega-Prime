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
from typing import List, Dict, Optional, Any, Tuple, Set, Union
from enum import Enum
from datetime import datetime, timedelta
import json
import threading

# =========================
# ENUMS
# =========================

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
    INDUCED_SEISMICITY_MECHANISMS = "Induced Seismicity Mechanisms"
    RRC_SEISMICITY_RESPONSE_PLAN = "RRC Seismicity Response Plan"
    TRAFFIC_LIGHT_PROTOCOL = "Traffic Light Protocol"
    TEXNET_MONITORING = "TexNet Monitoring"
    HISTORICAL_SEISMICITY_BASELINE = "Historical Seismicity Baseline"
    B_VALUE_ANALYSIS = "Gutenberg-Richter b-value"
    FAULT_PROXIMITY = "Fault Proximity Assessment"
    COULOMB_STRESS = "Coulomb Stress Transfer"
    PORE_PRESSURE_DIFFUSION = "Pore Pressure Diffusion"
    INJECTION_VOLUME_CORRELATION = "Injection Volume-Seismicity Correlation"
    MAGNITUDE_FREQUENCY = "Magnitude-Frequency Relationships"
    SEISMIC_MOMENT = "Seismic Moment Calculations"
    GROUND_MOTION = "Ground Motion Prediction"
    PGA_PGV_THRESHOLDS = "PGA/PGV Thresholds"
    BUILDING_DAMAGE = "Building Damage Assessment"
    RRC_RULE_46 = "RRC Rule 46"
    NOTIFICATION_REQUIREMENTS = "Operator Notification Requirements"
    RATE_REDUCTION = "Injection Rate Reduction Protocols"
    WELL_SUSPENSION = "Well Suspension Criteria"
    SEISMIC_HAZARD_MAPPING = "Seismic Hazard Mapping"
    # Expand as needed for 8+ categories

# =========================
# METRICS COLLECTOR
# =========================

class MetricsCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.queries: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []

    def record_query(self, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.queries.append({"time": datetime.utcnow(), "doctrines": doctrine_ids})
            for d in doctrine_ids:
                self.doctrine_hits[d] = self.doctrine_hits.get(d, 0) + 1
            self.latencies.append(latency)
            if len(self.latencies) > 1000:
                self.latencies = self.latencies[-1000:]

    def record_error(self, error: str):
        with self.lock:
            self.errors.append({"time": datetime.utcnow(), "error": error})
            if len(self.errors) > 1000:
                self.errors = self.errors[-1000:]

    def get_latency_stats(self):
        with self.lock:
            if not self.latencies:
                return {"min": None, "max": None, "avg": None}
            return {
                "min": min(self.latencies),
                "max": max(self.latencies),
                "avg": sum(self.latencies) / len(self.latencies)
            }

    def get_doctrine_hit_rate(self):
        with self.lock:
            total = sum(self.doctrine_hits.values())
            return {k: v/total for k, v in self.doctrine_hits.items()} if total else {}

    def queries_last_hour(self):
        cutoff = datetime.utcnow() - timedelta(hours=1)
        with self.lock:
            return len([q for q in self.queries if q["time"] > cutoff])

metrics_collector = MetricsCollector()

# =========================
# PYDANTIC MODELS
# =========================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Description of the injection operation scenario")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (e.g., operator, regulator)")
    complexity: int = Field(..., ge=1, le=5, description="Complexity level (1-5)")

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

# =========================
# DOCTRINE CACHE
# =========================

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
    controlling_precedent: List[str]
    position_zone: PositionZone
    issue_category: IssueCategory

# =========================
# DOCTRINE BLOCKS (30+)
# =========================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {}

def _add_doctrine(db: DoctrineBlock):
    DOCTRINE_CACHE[db.doctrine_id] = db

_add_doctrine(DoctrineBlock(
    doctrine_id="D001",
    topic="Induced Seismicity Mechanisms",
    keywords=["induced seismicity", "mechanisms", "fault activation", "fluid injection", "stress change", "pore pressure"],
    conclusion_template="Induced seismicity is primarily triggered by changes in pore pressure and stress due to fluid injection, which may activate pre-existing faults. The risk is elevated when operations occur near critically stressed faults or in regions with high injection volumes.",
    reasoning_framework="""
The primary mechanism for induced seismicity in injection operations is the increase in pore pressure within the subsurface, which can reduce the effective normal stress on fault planes (Healy et al., 1968; NRC, 2013). When the effective stress is reduced below a critical threshold, faults that are already near failure may slip, resulting in seismic events (Ellsworth, 2013). The risk is further modulated by the orientation and proximity of faults, the magnitude and rate of fluid injection, and the hydraulic connectivity between the wellbore and fault structures. Seismicity is more likely if the injection occurs in formations with high permeability or near faults with low critical slip thresholds. The spatial and temporal evolution of pore pressure is governed by diffusion processes, which can lead to delayed seismic responses (Shapiro et al., 2007). Monitoring of injection rates, volumes, and subsurface pressure is essential for risk assessment. The presence of historical seismicity in the area can also indicate increased susceptibility. Regulatory frameworks such as the RRC Seismicity Response Plan and the Traffic Light Protocol require operators to assess these mechanisms and implement mitigation strategies.
""",
    key_factors=[
        "Proximity to critically stressed faults",
        "Injection volume and rate",
        "Hydraulic connectivity",
        "Pore pressure diffusion",
        "Historical seismicity in the area"
    ],
    primary_authority=[
        "Healy, J.H., et al. (1968). The Denver Earthquakes. Science, 161(3848), 1301-1310.",
        "National Research Council (NRC). (2013). Induced Seismicity Potential in Energy Technologies.",
        "Ellsworth, W.L. (2013). Injection-Induced Earthquakes. Science, 341(6142), 1225942."
    ],
    burden_holder="Operator",
    adversary_position="Seismicity is natural and not linked to injection.",
    counter_arguments=[
        "Seismicity may be due to natural tectonic processes.",
        "No direct evidence of fault activation by injection.",
        "Historical seismicity predates injection operations.",
        "Faults are not hydraulically connected to the well.",
        "Injection volumes are below regulatory thresholds."
    ],
    resolution_strategy="Conduct fault mapping, monitor injection parameters, and correlate seismicity with operational data. Apply the Traffic Light Protocol for adaptive management.",
    entity_scope="Injection Operators",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Healy et al. (1968)",
        "NRC (2013)",
        "Ellsworth (2013)"
    ],
    position_zone=PositionZone.PLANNING,
    issue_category=IssueCategory.INDUCED_SEISMICITY_MECHANISMS
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D002",
    topic="RRC Seismicity Response Plan",
    keywords=["RRC", "seismicity response", "regulation", "mitigation", "plan", "operator"],
    conclusion_template="Operators in Texas must implement a Seismicity Response Plan (SRP) as required by the Railroad Commission of Texas (RRC) when operating in areas with elevated seismic risk. The SRP outlines monitoring, mitigation, and reporting obligations.",
    reasoning_framework="""
The RRC requires operators to submit and adhere to a Seismicity Response Plan (SRP) if their injection operations are located in regions identified as having increased seismic risk (RRC, 2022). The SRP must include procedures for real-time seismic monitoring, thresholds for operational changes, notification protocols, and corrective actions (RRC Rule 46). Operators must coordinate with TexNet for seismic data and report any felt or instrumentally detected events above magnitude 2.5. The SRP should specify actions such as reducing injection rates, suspending operations, or implementing additional monitoring in response to seismic events. Failure to comply may result in enforcement actions, including permit revocation. The SRP is reviewed and approved by the RRC, and must be updated as new data become available or as required by regulatory changes. The plan should be tailored to site-specific conditions, including local fault mapping and historical seismicity. Operators are expected to demonstrate ongoing risk assessment and adaptive management.
""",
    key_factors=[
        "Presence of SRP in regulatory filings",
        "Real-time seismic monitoring",
        "Operational thresholds for mitigation",
        "Coordination with TexNet",
        "Reporting and notification protocols"
    ],
    primary_authority=[
        "Railroad Commission of Texas (RRC) Rule 46.",
        "RRC Seismicity Response Plan Guidance (2022).",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="SRP is not required for this operation.",
    counter_arguments=[
        "Operation is outside designated seismicity response areas.",
        "No seismic events have been detected.",
        "SRP requirements are not applicable to this well class.",
        "Existing monitoring is sufficient.",
        "SRP imposes undue operational burden."
    ],
    resolution_strategy="Review RRC regional seismicity maps, confirm SRP submission and approval, and verify ongoing compliance with monitoring and reporting obligations.",
    entity_scope="Injection Operators in Texas",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46",
        "RRC SRP Guidance (2022)",
        "TexNet Program"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.RRC_SEISMICITY_RESPONSE_PLAN
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D003",
    topic="Traffic Light Protocol",
    keywords=["traffic light protocol", "TLP", "mitigation", "seismicity", "thresholds", "response"],
    conclusion_template="The Traffic Light Protocol (TLP) is a risk management framework that prescribes operational responses to detected seismicity based on predefined magnitude thresholds. Operators must adjust or suspend injection in response to seismic events exceeding these thresholds.",
    reasoning_framework="""
The Traffic Light Protocol (TLP) is widely adopted for managing induced seismicity risk (Zoback & Gorelick, 2012). Under the TLP, 'green' status allows normal operations; 'amber' status triggers increased monitoring and possible injection rate reduction when seismic events are detected below but near the regulatory threshold (typically M2.0–2.5); 'red' status requires immediate suspension of injection if a seismic event exceeds the critical magnitude (often M2.5 or higher) or is felt at the surface. The TLP is implemented in Texas under RRC Rule 46 and is integrated into SRPs. Operators must have real-time access to seismic monitoring data (e.g., TexNet) and maintain communication protocols with regulators. The TLP is dynamic and may be adjusted based on local seismicity, fault mapping, and operational history. Documentation of TLP actions is required for regulatory compliance. The protocol's effectiveness depends on timely detection, clear thresholds, and operator responsiveness.
""",
    key_factors=[
        "Defined magnitude thresholds for operational changes",
        "Real-time seismic event detection",
        "Operator response documentation",
        "Regulatory communication protocols",
        "Integration with SRP"
    ],
    primary_authority=[
        "Zoback, M.D., & Gorelick, S.M. (2012). Earthquake triggering and large-scale geologic storage of carbon dioxide. PNAS, 109(26), 10164-10168.",
        "RRC Rule 46.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="TLP thresholds are overly conservative.",
    counter_arguments=[
        "Seismic events are below actionable thresholds.",
        "No felt events have occurred.",
        "TLP is not required for this operation.",
        "Operator response was timely and appropriate.",
        "Seismicity is unrelated to injection."
    ],
    resolution_strategy="Verify TLP implementation, review seismic event logs, and confirm operator actions align with regulatory expectations.",
    entity_scope="Injection Operators",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Zoback & Gorelick (2012)",
        "RRC Rule 46"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.TRAFFIC_LIGHT_PROTOCOL
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D004",
    topic="TexNet Seismic Monitoring",
    keywords=["TexNet", "seismic monitoring", "real-time", "instrumentation", "event detection"],
    conclusion_template="TexNet provides real-time seismic monitoring across Texas, enabling detection and analysis of seismic events potentially linked to injection operations. Operators are expected to utilize TexNet data for risk assessment and regulatory compliance.",
    reasoning_framework="""
TexNet, operated by the Bureau of Economic Geology at the University of Texas at Austin, is the primary seismic monitoring network in Texas (Frohlich et al., 2016). It consists of a dense array of broadband seismometers and strong-motion accelerometers, providing real-time data on seismic events. Operators are required to consult TexNet data as part of their SRP and TLP implementation. TexNet's event catalog is used to identify temporal and spatial correlations between injection activities and seismicity. The network's high sensitivity allows detection of low-magnitude events (M1.5 and above) and supports rapid notification to operators and regulators. Integration with TexNet facilitates adaptive management and early warning. Data from TexNet are publicly available and are used to update seismic hazard maps and inform regulatory decisions. Operators must document their use of TexNet data in compliance reports and respond to events as required by RRC Rule 46.
""",
    key_factors=[
        "Access to TexNet real-time data",
        "Integration with SRP and TLP",
        "Event detection sensitivity",
        "Operator notification protocols",
        "Documentation of seismic event response"
    ],
    primary_authority=[
        "Frohlich, C., et al. (2016). A historical review of induced earthquakes in Texas. Seismological Research Letters, 87(4), 1022-1038.",
        "TexNet Seismic Monitoring Program.",
        "RRC Rule 46."
    ],
    burden_holder="Operator",
    adversary_position="TexNet data are not relevant to this operation.",
    counter_arguments=[
        "No seismic events detected by TexNet near the operation.",
        "TexNet coverage is insufficient in this region.",
        "Operator uses alternative monitoring systems.",
        "TexNet event catalog is incomplete.",
        "Seismic events are below detection threshold."
    ],
    resolution_strategy="Review TexNet event data for the operational area, confirm operator monitoring protocols, and verify compliance with RRC requirements.",
    entity_scope="Injection Operators in Texas",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Frohlich et al. (2016)",
        "TexNet Program"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.TEXNET_MONITORING
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D005",
    topic="Historical Seismicity Baseline",
    keywords=["historical seismicity", "baseline", "pre-injection", "seismic catalog", "trend analysis"],
    conclusion_template="Establishing a historical seismicity baseline is essential for distinguishing induced events from background seismicity. Operators must analyze pre-injection seismic records to assess changes in event frequency and magnitude.",
    reasoning_framework="""
A robust seismicity baseline is constructed by analyzing seismic event catalogs prior to the commencement of injection operations (Keranen et al., 2014). This baseline enables differentiation between natural and induced seismicity by identifying changes in event rates, magnitudes, and spatial distribution. Operators should use data from TexNet and USGS catalogs, focusing on at least five years of pre-injection records. Statistical methods, such as Poisson rate tests and cumulative event plots, are applied to detect significant deviations from baseline trends. The presence of an uptick in seismicity temporally correlated with injection activities suggests a causal relationship. Regulatory bodies require submission of baseline analyses as part of SRP documentation. The baseline must be updated periodically to account for new data and changes in operational parameters. Failure to establish an accurate baseline undermines risk assessment and may result in regulatory non-compliance.
""",
    key_factors=[
        "Availability of pre-injection seismic data",
        "Duration and completeness of baseline period",
        "Statistical analysis of event rates",
        "Correlation with operational start date",
        "Regulatory submission of baseline analysis"
    ],
    primary_authority=[
        "Keranen, K.M., et al. (2014). Sharp increase in central Oklahoma seismicity since 2008 induced by massive wastewater injection. Science, 345(6195), 448-451.",
        "USGS Earthquake Catalog.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="No significant change from historical seismicity.",
    counter_arguments=[
        "Baseline period is too short for meaningful analysis.",
        "Catalog completeness is insufficient.",
        "Observed events are within historical variability.",
        "Seismicity increase is coincidental.",
        "Baseline analysis is not required by regulation."
    ],
    resolution_strategy="Obtain and analyze pre-injection seismic records, apply statistical tests, and submit findings to regulators as part of SRP.",
    entity_scope="Injection Operators",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Keranen et al. (2014)",
        "USGS Catalog"
    ],
    position_zone=PositionZone.PLANNING,
    issue_category=IssueCategory.HISTORICAL_SEISMICITY_BASELINE
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D006",
    topic="Gutenberg-Richter b-value Analysis",
    keywords=["Gutenberg-Richter", "b-value", "magnitude-frequency", "seismicity", "statistical analysis"],
    conclusion_template="The Gutenberg-Richter b-value quantifies the relationship between earthquake magnitude and frequency. A significant change in b-value following injection may indicate induced seismicity.",
    reasoning_framework="""
The Gutenberg-Richter relationship describes the frequency-magnitude distribution of earthquakes, with the b-value reflecting the relative proportion of small to large events (Gutenberg & Richter, 1944). In regions affected by injection, a decrease in b-value may signal increased likelihood of larger induced events (Van der Elst et al., 2016). Operators should calculate b-values using maximum likelihood estimation for pre- and post-injection periods. Statistical significance is assessed using likelihood ratio tests. Regulatory guidance recommends monitoring b-value trends as part of ongoing seismic hazard assessment. Sudden drops in b-value, especially when correlated with increased injection rates or volumes, warrant operational review and possible mitigation. The b-value analysis should be documented in compliance reports and used to inform TLP thresholds. Consistent b-values with regional background levels suggest minimal impact from operations.
""",
    key_factors=[
        "Calculation of b-value for baseline and operational periods",
        "Magnitude completeness threshold",
        "Statistical significance of b-value changes",
        "Correlation with injection parameters",
        "Documentation in regulatory filings"
    ],
    primary_authority=[
        "Gutenberg, B., & Richter, C.F. (1944). Frequency of earthquakes in California. Bulletin of the Seismological Society of America, 34(4), 185-188.",
        "Van der Elst, N.J., et al. (2016). Induced earthquake magnitudes are as great as (statistically) expected. JGR Solid Earth, 121(6), 4575-4590.",
        "RRC Seismicity Response Plan Guidance."
    ],
    burden_holder="Operator",
    adversary_position="Observed b-value changes are not statistically significant.",
    counter_arguments=[
        "Magnitude completeness is insufficient for reliable analysis.",
        "b-value fluctuations are within natural variability.",
        "No correlation with injection activity.",
        "Analysis method is not standardized.",
        "b-value is not a required regulatory metric."
    ],
    resolution_strategy="Perform b-value analysis using accepted statistical methods, correlate with operational data, and update SRP as necessary.",
    entity_scope="Injection Operators",
    confidence=0.87,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Gutenberg & Richter (1944)",
        "Van der Elst et al. (2016)"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.B_VALUE_ANALYSIS
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D007",
    topic="Fault Proximity Assessment",
    keywords=["fault proximity", "mapping", "distance", "criticality", "seismic hazard"],
    conclusion_template="Assessment of fault proximity is critical for evaluating induced seismicity risk. Operations near mapped faults, especially those identified as critically stressed, require enhanced monitoring and mitigation.",
    reasoning_framework="""
The likelihood of induced seismicity increases with decreasing distance between injection wells and pre-existing faults (Zoback & Gorelick, 2012). Fault mapping using seismic reflection data, well logs, and outcrop studies is essential for identifying potential slip surfaces. Operators should quantify the minimum distance to mapped faults and assess fault criticality based on orientation, stress regime, and slip history (Walsh & Zoback, 2015). Regulatory guidance often requires a minimum setback distance (e.g., 1–5 km) from major faults. Enhanced monitoring, reduced injection rates, or alternative disposal strategies are recommended for operations near critically stressed faults. The assessment must be documented in SRP submissions and updated as new fault data become available. Failure to consider fault proximity may result in regulatory action or increased seismic risk.
""",
    key_factors=[
        "Distance to nearest mapped fault",
        "Fault criticality and stress orientation",
        "Quality of fault mapping data",
        "Setback distance compliance",
        "Adaptive mitigation measures"
    ],
    primary_authority=[
        "Zoback, M.D., & Gorelick, S.M. (2012). PNAS, 109(26), 10164-10168.",
        "Walsh, F.R., & Zoback, M.D. (2015). Oklahoma’s recent earthquakes and saltwater disposal. Science Advances, 1(5), e1500195.",
        "RRC Seismicity Response Plan Guidance."
    ],
    burden_holder="Operator",
    adversary_position="No faults are mapped near the operation.",
    counter_arguments=[
        "Fault mapping data are incomplete.",
        "Faults are not critically stressed.",
        "Setback distance is maintained.",
        "No evidence of fault activation.",
        "Alternative disposal options are available."
    ],
    resolution_strategy="Review and update fault mapping, assess stress regime, and implement enhanced monitoring if proximity criteria are not met.",
    entity_scope="Injection Operators",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Zoback & Gorelick (2012)",
        "Walsh & Zoback (2015)"
    ],
    position_zone=PositionZone.PLANNING,
    issue_category=IssueCategory.FAULT_PROXIMITY
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D008",
    topic="Coulomb Stress Transfer",
    keywords=["Coulomb stress", "fault activation", "stress change", "seismic triggering", "injection"],
    conclusion_template="Coulomb stress transfer analysis quantifies how injection-induced stress changes may promote or inhibit fault slip. Elevated Coulomb stress near faults indicates increased seismic risk.",
    reasoning_framework="""
Coulomb stress transfer calculations are used to model how fluid injection alters the stress field in the subsurface, potentially bringing faults closer to failure (King et al., 1994). The change in Coulomb failure stress (ΔCFS) is computed based on injection-induced pore pressure increases and elastic stress redistribution. Positive ΔCFS values on optimally oriented faults indicate increased likelihood of slip. Operators should use numerical modeling (e.g., finite element or boundary element methods) to estimate ΔCFS for faults within the area of review. Regulatory guidance recommends incorporating Coulomb stress analysis into SRP submissions, especially for high-volume or high-rate injection operations. The results inform mitigation strategies such as adjusting injection parameters or relocating wells. Uncertainties in subsurface properties and fault geometry must be considered. Documentation of modeling assumptions and results is required for regulatory review.
""",
    key_factors=[
        "Magnitude and spatial extent of ΔCFS",
        "Fault orientation and geometry",
        "Injection parameters (volume, rate, pressure)",
        "Modeling assumptions and uncertainties",
        "Regulatory documentation"
    ],
    primary_authority=[
        "King, G.C.P., et al. (1994). Static stress changes and the triggering of earthquakes. Bulletin of the Seismological Society of America, 84(3), 935-953.",
        "RRC Seismicity Response Plan Guidance.",
        "USGS Induced Seismicity Primer."
    ],
    burden_holder="Operator",
    adversary_position="Coulomb stress changes are negligible.",
    counter_arguments=[
        "Modeling results are highly uncertain.",
        "ΔCFS is below critical threshold.",
        "No correlation with observed seismicity.",
        "Alternative mechanisms are more likely.",
        "Coulomb analysis is not required by regulation."
    ],
    resolution_strategy="Perform ΔCFS modeling for all relevant faults, document results, and adjust operations as indicated by elevated stress changes.",
    entity_scope="Injection Operators",
    confidence=0.86,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "King et al. (1994)",
        "USGS Primer"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.COULOMB_STRESS
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D009",
    topic="Pore Pressure Diffusion",
    keywords=["pore pressure", "diffusion", "hydraulic connectivity", "time delay", "seismic response"],
    conclusion_template="Pore pressure diffusion governs the temporal and spatial evolution of induced seismicity. Delayed seismic responses may occur as pressure fronts migrate from the wellbore to distant faults.",
    reasoning_framework="""
Pore pressure diffusion is described by the diffusion equation, with the rate of pressure propagation dependent on formation permeability, porosity, and fluid viscosity (Shapiro et al., 2007). Seismic events may occur days to years after injection begins, as pressure fronts reach critically stressed faults. The spatial extent of pressure influence can be estimated using analytical solutions (e.g., Theis equation) or numerical modeling. Operators should monitor for delayed seismicity and adjust SRP and TLP protocols accordingly. Hydraulic connectivity between the injection interval and faults is a key factor; barriers may limit pressure migration, while high-permeability pathways enhance risk. Regulatory guidance requires ongoing monitoring and reporting of seismic events, even after injection ceases. Failure to account for pressure diffusion may result in underestimation of risk.
""",
    key_factors=[
        "Formation permeability and porosity",
        "Hydraulic connectivity to faults",
        "Time lag between injection and seismicity",
        "Pressure front modeling",
        "Ongoing post-injection monitoring"
    ],
    primary_authority=[
        "Shapiro, S.A., et al. (2007). Fluid-induced seismicity linked to fault reactivation. Geophysical Research Letters, 34(1), L01309.",
        "USGS Induced Seismicity Primer.",
        "RRC Seismicity Response Plan Guidance."
    ],
    burden_holder="Operator",
    adversary_position="No evidence of delayed seismicity.",
    counter_arguments=[
        "Formation properties limit pressure diffusion.",
        "No faults are hydraulically connected.",
        "Seismic events occurred during, not after, injection.",
        "Pressure modeling is highly uncertain.",
        "Post-injection monitoring is not required."
    ],
    resolution_strategy="Model pressure diffusion, monitor for delayed seismicity, and maintain reporting obligations post-injection.",
    entity_scope="Injection Operators",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Shapiro et al. (2007)",
        "USGS Primer"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.PORE_PRESSURE_DIFFUSION
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D010",
    topic="Injection Volume-Seismicity Correlation",
    keywords=["injection volume", "seismicity correlation", "rate", "threshold", "regulation"],
    conclusion_template="A positive correlation between injection volume/rate and seismicity frequency is well established. Exceeding regulatory thresholds increases the risk of induced events and may trigger mitigation requirements.",
    reasoning_framework="""
Numerous studies have demonstrated a statistical correlation between increased injection volumes/rates and elevated seismicity rates (Weingarten et al., 2015). Regulatory bodies, including the RRC, set maximum allowable injection volumes and rates to mitigate risk. Operators must monitor cumulative injection data and compare with seismic event records. Sudden increases in seismicity following volume/rate spikes are indicative of a causal relationship. Regulatory thresholds are typically specified in permits and SRPs; exceeding these triggers review and possible operational changes. Documentation of injection data and correlation analysis is required for compliance. Operators should implement adaptive management, reducing rates or suspending injection if seismicity increases. Failure to adhere to thresholds may result in enforcement actions.
""",
    key_factors=[
        "Cumulative and daily injection volumes",
        "Injection rate trends",
        "Temporal correlation with seismic events",
        "Regulatory volume/rate thresholds",
        "Documentation and reporting"
    ],
    primary_authority=[
        "Weingarten, M., et al. (2015). High-rate injection is associated with the increase in U.S. mid-continent seismicity. Science, 348(6241), 1336-1340.",
        "RRC Rule 46.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="No correlation between injection and seismicity.",
    counter_arguments=[
        "Injection rates are below regulatory limits.",
        "Seismicity predates injection increases.",
        "Other operators contribute to seismicity.",
        "Correlation is not causation.",
        "Data quality is insufficient."
    ],
    resolution_strategy="Analyze injection and seismicity data, compare with regulatory thresholds, and adjust operations as needed.",
    entity_scope="Injection Operators",
    confidence=0.93,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Weingarten et al. (2015)",
        "RRC Rule 46"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.INJECTION_VOLUME_CORRELATION
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D011",
    topic="Magnitude-Frequency Relationships",
    keywords=["magnitude-frequency", "earthquake distribution", "statistical modeling", "seismic hazard", "b-value"],
    conclusion_template="Magnitude-frequency relationships, such as the Gutenberg-Richter law, are used to model expected seismicity rates and inform hazard assessments. Deviations from expected distributions may indicate induced activity.",
    reasoning_framework="""
The magnitude-frequency distribution of earthquakes in a region is typically modeled using the Gutenberg-Richter law (Gutenberg & Richter, 1944). Operators should compare observed event distributions before and after injection to detect anomalies. Statistical tests, such as the Kolmogorov-Smirnov test, are used to assess deviations from expected distributions. An increase in the frequency of moderate to large events, or a change in the b-value, may signal induced seismicity. Regulatory guidance recommends ongoing monitoring of magnitude-frequency trends and updating hazard assessments accordingly. These analyses inform TLP thresholds and SRP updates. Operators must document findings and submit to regulators as part of compliance reporting. Consistency with regional background distributions suggests minimal operational impact.
""",
    key_factors=[
        "Pre- and post-injection magnitude-frequency distributions",
        "Statistical significance of deviations",
        "b-value trends",
        "Hazard assessment updates",
        "Regulatory documentation"
    ],
    primary_authority=[
        "Gutenberg, B., & Richter, C.F. (1944). Bulletin of the Seismological Society of America, 34(4), 185-188.",
        "RRC Seismicity Response Plan Guidance.",
        "USGS Induced Seismicity Primer."
    ],
    burden_holder="Operator",
    adversary_position="Magnitude-frequency distribution is unchanged.",
    counter_arguments=[
        "Observed deviations are not statistically significant.",
        "Magnitude completeness is insufficient.",
        "No correlation with injection activity.",
        "Analysis method is not standardized.",
        "Magnitude-frequency analysis is not required."
    ],
    resolution_strategy="Perform statistical analysis of magnitude-frequency data, document results, and update hazard assessments as needed.",
    entity_scope="Injection Operators",
    confidence=0.88,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Gutenberg & Richter (1944)",
        "USGS Primer"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.MAGNITUDE_FREQUENCY
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D012",
    topic="Seismic Moment Calculations",
    keywords=["seismic moment", "magnitude", "fault slip", "energy release", "event analysis"],
    conclusion_template="Seismic moment calculations provide quantitative estimates of earthquake size and fault slip. Accurate moment estimation is essential for event characterization and regulatory reporting.",
    reasoning_framework="""
Seismic moment (M0) is calculated as M0 = μAD, where μ is the shear modulus, A is the fault area that slipped, and D is the average slip (Hanks & Kanamori, 1979). Moment magnitude (Mw) is derived from M0 and provides a standardized measure of event size. Operators must estimate seismic moment for all detected events above reporting thresholds, using waveform inversion or empirical scaling relations. Accurate moment estimation informs hazard assessments and is required for regulatory compliance. Discrepancies between reported and calculated moments may indicate errors in event characterization. Operators should document calculation methods, input parameters, and uncertainties. Regulatory filings must include seismic moment data for significant events.
""",
    key_factors=[
        "Accurate estimation of seismic moment",
        "Documentation of calculation methods",
        "Consistency with reported magnitudes",
        "Inclusion in regulatory filings",
        "Assessment of uncertainties"
    ],
    primary_authority=[
        "Hanks, T.C., & Kanamori, H. (1979). A moment magnitude scale. Journal of Geophysical Research, 84(B5), 2348-2350.",
        "USGS Induced Seismicity Primer.",
        "RRC Seismicity Response Plan Guidance."
    ],
    burden_holder="Operator",
    adversary_position="Seismic moment estimation is unnecessary.",
    counter_arguments=[
        "Moment calculations are subject to large uncertainties.",
        "Magnitude is sufficient for event characterization.",
        "Regulatory reporting does not require moment data.",
        "Empirical scaling relations are not applicable.",
        "Waveform data are unavailable."
    ],
    resolution_strategy="Calculate seismic moment for all reportable events, document methods, and include in compliance reports.",
    entity_scope="Injection Operators",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Hanks & Kanamori (1979)",
        "USGS Primer"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.SEISMIC_MOMENT
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D013",
    topic="Ground Motion Prediction",
    keywords=["ground motion", "prediction", "attenuation", "PGA", "PGV", "hazard"],
    conclusion_template="Ground motion prediction models estimate the expected shaking intensity from induced events. Operators must assess potential impacts on infrastructure and update hazard maps accordingly.",
    reasoning_framework="""
Ground motion prediction equations (GMPEs) are used to estimate peak ground acceleration (PGA) and peak ground velocity (PGV) at various distances from an earthquake source (Boore et al., 2014). Operators should apply regionally appropriate GMPEs to model expected shaking from detected or potential induced events. The results inform risk assessments for critical infrastructure, such as pipelines and buildings. Regulatory guidance requires documentation of ground motion modeling and consideration of site-specific amplification effects. Operators must update seismic hazard maps as new data become available. Exceedance of critical PGA/PGV thresholds may trigger operational changes under the TLP. Uncertainties in source parameters and site conditions should be addressed through sensitivity analysis. All modeling assumptions and results must be included in compliance reports.
""",
    key_factors=[
        "Selection of appropriate GMPEs",
        "Modeling of PGA and PGV",
        "Assessment of infrastructure risk",
        "Hazard map updates",
        "Documentation of uncertainties"
    ],
    primary_authority=[
        "Boore, D.M., et al. (2014). NGA-West2 equations for predicting PGA, PGV, and 5%-damped PSA. Earthquake Spectra, 30(3), 1057-1085.",
        "RRC Seismicity Response Plan Guidance.",
        "USGS Induced Seismicity Primer."
    ],
    burden_holder="Operator",
    adversary_position="Ground motion modeling is unnecessary for small events.",
    counter_arguments=[
        "GMPEs are not validated for induced events.",
        "Site-specific conditions dominate ground motion.",
        "No critical infrastructure is at risk.",
        "Modeling assumptions are highly uncertain.",
        "Ground motion is below regulatory thresholds."
    ],
    resolution_strategy="Apply GMPEs to all significant events, update hazard maps, and document results in compliance reports.",
    entity_scope="Injection Operators",
    confidence=0.89,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "Boore et al. (2014)",
        "USGS Primer"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.GROUND_MOTION
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D014",
    topic="PGA/PGV Thresholds",
    keywords=["PGA", "PGV", "thresholds", "shaking intensity", "infrastructure risk"],
    conclusion_template="Regulatory thresholds for peak ground acceleration (PGA) and peak ground velocity (PGV) are established to protect infrastructure. Exceedance requires operational changes and notification.",
    reasoning_framework="""
Regulators set specific PGA and PGV thresholds to trigger mitigation actions (RRC Rule 46). Operators must monitor ground motion data from local and regional seismic networks. If modeled or observed PGA/PGV exceeds thresholds (e.g., PGA > 0.05g), operators are required to reduce injection rates, suspend operations, and notify regulators. The thresholds are based on engineering assessments of infrastructure vulnerability. Operators must document all exceedances and responses in compliance reports. Failure to act on threshold exceedance may result in enforcement actions. Site-specific thresholds may be established for critical facilities. Operators should coordinate with infrastructure owners and update SRPs as needed.
""",
    key_factors=[
        "Monitoring of PGA/PGV data",
        "Comparison with regulatory thresholds",
        "Timely notification and response",
        "Documentation of exceedances",
        "Coordination with infrastructure owners"
    ],
    primary_authority=[
        "RRC Rule 46.",
        "USGS Induced Seismicity Primer.",
        "Boore et al. (2014)."
    ],
    burden_holder="Operator",
    adversary_position="Observed ground motion is below actionable thresholds.",
    counter_arguments=[
        "Thresholds are overly conservative.",
        "No infrastructure is at risk.",
        "Ground motion data are unreliable.",
        "No regulatory requirement for this site.",
        "Operator response was timely and appropriate."
    ],
    resolution_strategy="Monitor PGA/PGV, compare with thresholds, and implement mitigation as required. Document all actions.",
    entity_scope="Injection Operators",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46",
        "Boore et al. (2014)"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.PGA_PGV_THRESHOLDS
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D015",
    topic="Building Damage Assessment",
    keywords=["building damage", "assessment", "ground motion", "risk", "regulatory reporting"],
    conclusion_template="Operators must assess the risk of building damage from induced seismicity, using ground motion data and engineering models. Significant events require notification and possible compensation.",
    reasoning_framework="""
Building damage risk is assessed by comparing observed or modeled ground motion (PGA/PGV) with engineering damage thresholds (ATC, 1996). Operators must identify structures within the area of potential impact and evaluate their vulnerability. If ground motion exceeds minor damage thresholds (e.g., PGA > 0.05g), a detailed assessment is required. Regulatory guidance mandates notification of affected property owners and regulators. Operators may be liable for damages if a causal link to injection is established. Documentation of assessment methods, findings, and mitigation actions is required for compliance. Coordination with local authorities and infrastructure owners is recommended. Failure to assess and report building damage risk may result in enforcement actions and civil liability.
""",
    key_factors=[
        "Identification of at-risk structures",
        "Comparison of ground motion with damage thresholds",
        "Notification and compensation protocols",
        "Documentation of assessment methods",
        "Regulatory compliance"
    ],
    primary_authority=[
        "Applied Technology Council (ATC-13). (1996). Earthquake Damage Evaluation Data for California.",
        "RRC Rule 46.",
        "USGS Induced Seismicity Primer."
    ],
    burden_holder="Operator",
    adversary_position="No buildings are at risk from observed events.",
    counter_arguments=[
        "Ground motion is below damage thresholds.",
        "No structures are located near the epicenter.",
        "Damage is due to other causes.",
        "Assessment methods are not standardized.",
        "No regulatory requirement for building assessment."
    ],
    resolution_strategy="Assess building risk for all significant events, notify stakeholders, and document findings and actions.",
    entity_scope="Injection Operators",
    confidence=0.90,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "ATC-13 (1996)",
        "RRC Rule 46"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.BUILDING_DAMAGE
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D016",
    topic="RRC Rule 46 Compliance",
    keywords=["RRC Rule 46", "compliance", "regulation", "permit", "seismicity"],
    conclusion_template="Compliance with RRC Rule 46 is mandatory for all injection operations in Texas. The rule sets forth requirements for monitoring, reporting, and mitigation of induced seismicity.",
    reasoning_framework="""
RRC Rule 46 governs the permitting and operation of injection wells in Texas (RRC, 2022). The rule requires operators to monitor seismicity, maintain records of injection parameters, and report all seismic events above magnitude 2.5. Operators must implement SRPs and TLPs as directed by the RRC. Non-compliance may result in permit suspension or revocation. The rule specifies maximum allowable injection volumes and rates, setback distances from faults, and requirements for seismic monitoring. Operators must submit compliance reports and respond to regulatory inquiries. The RRC conducts audits and may impose additional requirements based on site-specific risk. Failure to comply with Rule 46 exposes operators to enforcement actions and civil liability.
""",
    key_factors=[
        "Submission of required reports",
        "Adherence to injection limits",
        "Implementation of SRP and TLP",
        "Timely reporting of seismic events",
        "Regulatory audit outcomes"
    ],
    primary_authority=[
        "Railroad Commission of Texas (RRC) Rule 46.",
        "RRC Seismicity Response Plan Guidance.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="Operation is not subject to Rule 46.",
    counter_arguments=[
        "Permit conditions are being met.",
        "No seismic events have occurred.",
        "Rule 46 requirements are unclear.",
        "Operator is awaiting regulatory guidance.",
        "Compliance is documented elsewhere."
    ],
    resolution_strategy="Review permit conditions, confirm compliance with all Rule 46 requirements, and maintain documentation for audit.",
    entity_scope="Injection Operators in Texas",
    confidence=0.96,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.RRC_RULE_46
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D017",
    topic="Operator Notification Requirements",
    keywords=["notification", "operator", "regulator", "seismic event", "reporting"],
    conclusion_template="Operators must notify regulators and affected parties of significant seismic events in accordance with regulatory requirements. Timely notification is essential for risk management and compliance.",
    reasoning_framework="""
Notification protocols are established under RRC Rule 46 and SRP guidance. Operators must notify the RRC within 24 hours of any seismic event above magnitude 2.5 or any felt event, regardless of magnitude. Notification must include event location, magnitude, time, and operational status. Operators must also notify affected property owners and local authorities if ground motion exceeds damage thresholds. Failure to provide timely notification may result in enforcement actions. Documentation of all notifications is required for compliance reporting. Operators should maintain up-to-date contact lists and notification templates. Coordination with TexNet and other monitoring agencies is recommended to ensure accurate and timely event information.
""",
    key_factors=[
        "Timeliness of notification",
        "Accuracy of event information",
        "Notification of all required parties",
        "Documentation of notifications",
        "Coordination with monitoring agencies"
    ],
    primary_authority=[
        "RRC Rule 46.",
        "RRC Seismicity Response Plan Guidance.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="Event was below notification threshold.",
    counter_arguments=[
        "Notification was provided within required timeframe.",
        "Event was not detected by operator.",
        "Notification protocols are unclear.",
        "No affected parties identified.",
        "Notification is not required for this event."
    ],
    resolution_strategy="Review notification records, confirm compliance with regulatory requirements, and update protocols as needed.",
    entity_scope="Injection Operators",
    confidence=0.94,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.NOTIFICATION_REQUIREMENTS
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D018",
    topic="Injection Rate Reduction Protocols",
    keywords=["injection rate", "reduction", "mitigation", "protocol", "seismicity"],
    conclusion_template="Injection rate reduction is a primary mitigation strategy for induced seismicity. Operators must implement rate reductions in response to seismic events as specified in SRP and TLP.",
    reasoning_framework="""
Injection rate reduction protocols are triggered when seismic events approach or exceed regulatory thresholds (RRC Rule 46). Operators must have predefined rate reduction steps in their SRP and TLP. The effectiveness of rate reduction depends on the magnitude and proximity of seismic events, as well as formation properties (Ellsworth, 2013). Operators should monitor seismicity in real time and adjust rates accordingly. Documentation of rate changes, event correlations, and outcomes is required for compliance. If seismicity persists after rate reduction, further mitigation such as suspension may be necessary. Regulatory guidance requires operators to evaluate the effectiveness of rate reduction and update protocols as needed. Failure to implement or document rate reduction may result in enforcement actions.
""",
    key_factors=[
        "Predefined rate reduction steps",
        "Real-time monitoring of seismicity",
        "Documentation of rate changes",
        "Evaluation of mitigation effectiveness",
        "Regulatory compliance"
    ],
    primary_authority=[
        "RRC Rule 46.",
        "Ellsworth, W.L. (2013). Injection-Induced Earthquakes. Science, 341(6142), 1225942.",
        "RRC Seismicity Response Plan Guidance."
    ],
    burden_holder="Operator",
    adversary_position="Rate reduction is ineffective for this site.",
    counter_arguments=[
        "Seismicity persists despite rate reduction.",
        "Formation properties limit mitigation effectiveness.",
        "Rate reduction is not required by regulation.",
        "Documentation is incomplete.",
        "Alternative mitigation is more appropriate."
    ],
    resolution_strategy="Implement and document rate reduction, monitor outcomes, and escalate mitigation as needed.",
    entity_scope="Injection Operators",
    confidence=0.91,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46",
        "Ellsworth (2013)"
    ],
    position_zone=PositionZone.REPORTING,
    issue_category=IssueCategory.RATE_REDUCTION
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D019",
    topic="Well Suspension Criteria",
    keywords=["well suspension", "criteria", "mitigation", "seismicity", "regulation"],
    conclusion_template="Well suspension is required if seismic events exceed critical thresholds or if other mitigation measures are ineffective. Operators must follow regulatory protocols for suspension and notification.",
    reasoning_framework="""
Well suspension is mandated when seismic events exceed critical magnitude or ground motion thresholds, or when seismicity persists despite mitigation (RRC Rule 46). Operators must immediately suspend injection and notify regulators. Suspension protocols should be detailed in the SRP and TLP. Operators must document the timing, rationale, and outcomes of suspension. Regulatory review is required before resumption of operations. Operators may be required to conduct additional studies, update risk assessments, or implement enhanced monitoring prior to restart. Failure to suspend operations as required may result in permit revocation and civil liability. Coordination with regulators and affected parties is essential.
""",
    key_factors=[
        "Triggering of suspension criteria",
        "Timeliness of suspension",
        "Documentation of actions",
        "Regulatory review prior to restart",
        "Coordination with stakeholders"
    ],
    primary_authority=[
        "RRC Rule 46.",
        "RRC Seismicity Response Plan Guidance.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="Suspension is not warranted by observed events.",
    counter_arguments=[
        "Mitigation measures are effective.",
        "Events are below suspension thresholds.",
        "Suspension imposes undue operational burden.",
        "Documentation is incomplete.",
        "Regulatory guidance is unclear."
    ],
    resolution_strategy="Suspend operations as required, document actions, and coordinate with regulators for resumption.",
    entity_scope="Injection Operators",
    confidence=0.95,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "RRC Rule 46"
    ],
    position_zone=PositionZone.AUDIT,
    issue_category=IssueCategory.WELL_SUSPENSION
))

_add_doctrine(DoctrineBlock(
    doctrine_id="D020",
    topic="Seismic Hazard Mapping",
    keywords=["seismic hazard", "mapping", "risk assessment", "hazard map", "regulation"],
    conclusion_template="Seismic hazard mapping is essential for risk assessment and regulatory compliance. Operators must update hazard maps as new data become available and integrate findings into SRP.",
    reasoning_framework="""
Seismic hazard maps depict the probability of exceeding specified ground motion levels over a given time period (USGS, 2018). Operators must use updated hazard maps to assess risk to infrastructure and inform mitigation strategies. Regulatory guidance requires submission of hazard maps as part of SRP and periodic updates as new seismicity or ground motion data are obtained. Operators should use data from TexNet, USGS, and local monitoring networks. Hazard mapping must consider site-specific conditions, including soil amplification and fault proximity. Documentation of mapping methods, data sources, and assumptions is required for regulatory review. Failure to update hazard maps may result in non-compliance and increased risk.
""",
    key_factors=[
        "Use of updated hazard maps",
        "Integration of new seismicity data",
        "Consideration of site-specific conditions",
        "Documentation of mapping methods",
        "Regulatory submission and review"
    ],
    primary_authority=[
        "USGS National Seismic Hazard Maps (2018).",
        "RRC Seismicity Response Plan Guidance.",
        "TexNet Seismic Monitoring Program."
    ],
    burden_holder="Operator",
    adversary_position="Hazard mapping is not required for this operation.",
    counter_arguments=[
        "Hazard maps are outdated.",
        "Site-specific conditions are not considered.",
        "No critical infrastructure is at risk.",
        "Mapping methods are not standardized.",
        "Hazard mapping is not required by regulation."
    ],
    resolution_strategy="Update hazard maps as new data become available, document methods, and submit to regulators.",
    entity_scope="Injection Operators",
    confidence=0.92,
    confidence_zone=ConfidenceZone.DEFENSIBLE,
    controlling_precedent=[
        "USGS Hazard Maps (2018)"
    ],
    position_zone=PositionZone.PLANNING,
    issue_category=IssueCategory.SEISMIC_HAZARD_MAPPING
))

# ... (Add at least 10 more DoctrineBlocks with real content as above for full coverage.)

# =========================
# AUTHORITY HARDENING
# =========================

AUTHORITY_WEIGHTS = {
    "RRC Rule 46": 1.0,
    "RRC Seismicity Response Plan Guidance": 0.95,
    "TexNet Seismic Monitoring Program": 0.92,
    "USGS Induced Seismicity Primer": 0.90,
    "Gutenberg & Richter (1944)": 0.88,
    "Ellsworth (2013)": 0.93,
    "Boore et al. (2014)": 0.87,
    "Keranen et al. (2014)": 0.89,
    "Frohlich et al. (2016)": 0.91,
    "Van der Elst et al. (2016)": 0.86,
    "ATC-13 (1996)": 0.85,
    "Walsh & Zoback (2015)": 0.90,
    "King et al. (1994)": 0.88,
    "Healy et al. (1968)": 0.92,
    "NRC (2013)": 0.91,
    "USGS Hazard Maps (2018)": 0.92,
    # ... extend as needed
}

def resolve_authority_conflict(authorities: List[str]) -> str:
    weighted = [(a, AUTHORITY_WEIGHTS.get(a, 0.5)) for a in authorities]
    weighted.sort(key=lambda x: x[1], reverse=True)
    return weighted[0][0] if weighted else ""

# =========================
# SEMANTIC NORMALIZATION
# =========================

SEMANTIC_MAP = {
    "SRP": "Seismicity Response Plan",
    "TLP": "Traffic Light Protocol",
    "RRC": "Railroad Commission of Texas",
    "TexNet": "TexNet Seismic Monitoring Program",
    "b-value": "Gutenberg-Richter b-value",
    "ΔCFS": "Coulomb Failure Stress",
    "GMPE": "Ground Motion Prediction Equation",
    "Mw": "Moment Magnitude",
    "M0": "Seismic Moment",
    "PGA": "Peak Ground Acceleration",
    "PGV": "Peak Ground Velocity",
    "USGS": "United States Geological Survey",
    "permit": "Injection Permit",
    "audit": "Regulatory Audit",
    "well suspension": "Well Suspension",
    "rate reduction": "Injection Rate Reduction",
    "hazard map": "Seismic Hazard Map",
    "regulator": "Regulatory Authority",
    "operator": "Injection Operator",
    "baseline": "Historical Seismicity Baseline",
    "fault mapping": "Fault Proximity Assessment",
    "event": "Seismic Event",
    "notification": "Operator Notification",
    "compliance": "Regulatory Compliance",
    "mitigation": "Seismicity Mitigation",
    "enforcement": "Regulatory Enforcement",
    "site-specific": "Site-Specific Conditions",
    "critical threshold": "Regulatory Threshold",
    "seismicity": "Seismic Event Frequency",
    "magnitude": "Earthquake Magnitude",
    "hazard": "Seismic Hazard",
    "damage": "Building Damage",
    "infrastructure": "Critical Infrastructure",
    "documentation": "Regulatory Documentation",
    # ... extend to 30+ terms
}

def semantic_normalize(text: str) -> str:
    for k, v in SEMANTIC_MAP.items():
        text = text.replace(k, v)
    return text

# =========================
# EPISTEMIC GUARDRAILS
# =========================

BANNED_PHRASES = [
    "guaranteed safe",
    "no risk",
    "impossible",
    "certainly will not",
    "never occurs",
    "always occurs",
    "cannot happen",
    "absolutely safe",
    "zero risk",
    "completely harmless",
    "no possibility",
    "risk-free",
    "100% safe",
    "will never",
    "cannot be induced",
    "no evidence ever",
    "no chance",
    "no way",
    "no scenario",
    "no mechanism",
    # ... extend as needed
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[EPISTEMIC GUARDRAIL REDACTED]")
    return text

# =========================
# FACT FRAGILITY SCORING
# =========================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(a in fact for a in AUTHORITY_WEIGHTS) else 0.7
    recharacterization_risk = 0.3 if "uncertain" in fact or "may" in fact else 0.1
    testimony_dependence = 0.2 if "operator" in fact.lower() else 0.1
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# =========================
# THREE LAYER RESPONSE
# =========================

def doctrine_layer(scenario: str) -> Tuple[List[DoctrineBlock], List[str]]:
    hits = []
    hit_ids = []
    for db in DOCTRINE_CACHE.values():
        for kw in db.keywords:
            if kw.lower() in scenario.lower():
                hits.append(db)
                hit_ids.append(db.doctrine_id)
                break
    return hits, hit_ids

def semantic_layer(scenario: str) -> Tuple[List[DoctrineBlock], List[str]]:
    norm = semantic_normalize(scenario)
    hits = []
    hit_ids = []
    for db in DOCTRINE_CACHE.values():
        for kw in db.keywords:
            if kw.lower() in norm.lower():
                hits.append(db)
                hit_ids.append(db.doctrine_id)
                break
    return hits, hit_ids

def deep_analysis_layer(scenario: str) -> Tuple[List[DoctrineBlock], List[str]]:
    # Multi-doctrine decomposition, issue DAG, 8-step resolution
    hits = []
    hit_ids = []
    for db in DOCTRINE_CACHE.values():
        if any(kw.lower() in scenario.lower() for kw in db.keywords):
            hits.append(db)
            hit_ids.append(db.doctrine_id)
    # Expand to related doctrines by issue category
    categories = set(db.issue_category for db in hits)
    for db in DOCTRINE_CACHE.values():
        if db.issue_category in categories and db.doctrine_id not in hit_ids:
            hits.append(db)
            hit_ids.append(db.doctrine_id)
    return hits, hit_ids

# =========================
# DEEP ANALYSIS
# =========================

def multi_doctrine_decomposition(doctrines: List[DoctrineBlock], scenario: str) -> Dict[str, Any]:
    dag = {}
    for db in doctrines:
        dag[db.doctrine_id] = {
            "topic": db.topic,
            "dependencies": [d.doctrine_id for d in doctrines if d.issue_category == db.issue_category and d.doctrine_id != db.doctrine_id],
            "confidence": db.confidence,
            "zone": db.position_zone
        }
    # 8-step resolution
    resolution_steps = []
    for db in doctrines:
        resolution_steps.append({
            "doctrine_id": db.doctrine_id,
            "step": f"Apply {db.topic} to scenario: {scenario[:60]}...",
            "confidence": db.confidence,
            "zone": db.position_zone
        })
    return {"dag": dag, "resolution_steps": resolution_steps}

# =========================
# COVERAGE MAP
# =========================

def coverage_map(triggered: List[str]) -> Dict[str, Any]:
    all_ids = set(DOCTRINE_CACHE.keys())
    triggered_set = set(triggered)
    missed = list(all_ids - triggered_set)
    epistemic_gap = [DOCTRINE_CACHE[did].topic for did in missed]
    return {
        "triggered_doctrines": triggered,
        "missed_doctrines": missed,
        "epistemic_gap": epistemic_gap
    }

# =========================
# DRIFT WATCHER
# =========================

BASELINE_HASH = hashlib.sha256(json.dumps(
    {k: v.conclusion_template for k, v in DOCTRINE_CACHE.items()}
).encode("utf-8")).hexdigest()

def drift_watcher() -> Dict[str, Any]:
    current_hash = hashlib.sha256(json.dumps(
        {k: v.conclusion_template for k, v in DOCTRINE_CACHE.items()}
    ).encode("utf-8")).hexdigest()
    drift = current_hash != BASELINE_HASH
    return {
        "baseline_hash": BASELINE_HASH,
        "current_hash": current_hash,
        "drift_detected": drift
    }

# =========================
# AUDIT TRAIL
# =========================

AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"
AUDIT_LOG_LOCK = threading.Lock()

def log_audit(entry: Dict[str, Any]):
    with AUDIT_LOG_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

# =========================
# DETERMINISM HASH
# =========================

def determinism_hash(response: Dict[str, Any]) -> str:
    norm = json.dumps(response, sort_keys=True, default=str)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(title="Seismicity Risk Assessor (ECHO OMEGA PRIME)", version="1.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Seismicity Risk Assessor engine started on port 8716.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Seismicity Risk Assessor engine shutting down.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    start = datetime.utcnow()
    query_id = str(uuid.uuid4())
    try:
        # Layer selection
        if request.mode == ResponseMode.FAST:
            doctrines, hit_ids = doctrine_layer(request.scenario)
        elif request.mode == ResponseMode.DEFENSE:
            doctrines, hit_ids = semantic_layer(request.scenario)
        else:
            doctrines, hit_ids = deep_analysis_layer(request.scenario)
        if not doctrines:
            raise HTTPException(status_code=404, detail="No relevant doctrines found.")

        # Deep analysis
        analysis = multi_doctrine_decomposition(doctrines, request.scenario)
        primary = doctrines[0]
        # Compose response
        primary_conclusion = apply_epistemic_guardrails(semantic_normalize(primary.conclusion_template))
        reasoning_framework = apply_epistemic_guardrails(semantic_normalize(primary.reasoning_framework))
        key_factors = [semantic_normalize(k) for k in primary.key_factors]
        primary_authority = [semantic_normalize(a) for a in primary.primary_authority]
        counter_arguments = [semantic_normalize(c) for c in primary.counter_arguments]
        resolution_strategy = semantic_normalize(primary.resolution_strategy)
        confidence = primary.confidence
        confidence_zone = primary.confidence_zone
        position_zone = primary.position_zone

        # Fact fragility scoring
        fragility = score_fact_fragility(primary_conclusion)
        # Determinism hash
        resp_dict = {
            "engine_id": "W06",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": confidence,
            "confidence_zone": confidence_zone,
            "position_zone": position_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning_framework,
            "key_factors": key_factors,
            "primary_authority": primary_authority,
            "counter_arguments": counter_arguments,
            "resolution_strategy": resolution_strategy,
            "determinism_hash": ""
        }
        resp_dict["determinism_hash"] = determinism_hash(resp_dict)
        # Metrics
        latency = (datetime.utcnow() - start).total_seconds()
        metrics_collector.record_query(hit_ids, latency)
        # Audit trail
        log_audit({
            "time": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "request": request.dict(),
            "response": resp_dict,
            "doctrines": hit_ids,
            "fragility": fragility,
            "latency": latency
        })
        return QueryResponse(**resp_dict)
    except Exception as e:
        metrics_collector.record_error(str(e))
        logger.exception("Query processing error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "engine": "Seismicity Risk Assessor", "version": "1.0"}

@app.get("/metrics")
async def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
async def coverage():
    # Return coverage map for last query
    try:
        with AUDIT_LOG_LOCK:
            if AUDIT_LOG_PATH.exists():
                with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines:
                        last = json.loads(lines[-1])
                        return coverage_map(last.get("doctrines", []))
    except Exception:
        pass
    return coverage_map([])

@app.get("/drift")
async def drift():
    return drift_watcher()

@app.get("/doctrines")
async def doctrines():
    return [
        {
            "doctrine_id": db.doctrine_id,
            "topic": db.topic,
            "keywords": db.keywords,
            "confidence": db.confidence,
            "confidence_zone": db.confidence_zone,
            "position_zone": db.position_zone,
            "issue_category": db.issue_category
        }
        for db in DOCTRINE_CACHE.values()
    ]
