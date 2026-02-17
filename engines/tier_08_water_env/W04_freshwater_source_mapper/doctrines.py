from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Ogallala Aquifer: Source Viability for Frac Operations",
        keywords=["Ogallala", "aquifer", "frac", "water sourcing", "viability", "hydrogeology"],
        conclusion_template="The Ogallala Aquifer is a viable source for frac operations in designated counties, subject to GCD production limits and TWDB permitting.",
        reasoning_framework=(
            "1. Assess Ogallala Aquifer recharge rates and historical drawdown trends.\n"
            "2. Review GCD production limits and variance history in the target region.\n"
            "3. Evaluate water quality parameters (TDS, hardness) against frac requirements.\n"
            "4. Examine TWDB well permitting process and recent approvals/denials.\n"
            "5. Consider drought index correlations and seasonal availability projections.\n"
            "6. Analyze legal precedents regarding aquifer use for industrial purposes.\n"
            "7. Identify operational risks from aquifer depletion and regulatory enforcement.\n"
            "8. Synthesize findings to determine overall viability for frac sourcing."
        ),
        key_factors=[
            "Aquifer recharge rate",
            "Historical drawdown",
            "GCD production limits",
            "TWDB permitting",
            "Water quality (TDS, hardness)",
            "Seasonal availability",
            "Drought index",
            "Legal precedents"
        ],
        primary_authority=[
            "Texas Water Development Board (TWDB)",
            "Groundwater Conservation Districts (GCDs)",
            "Texas Administrative Code Title 30"
        ],
        burden_holder="Operator seeking frac water",
        adversary_position="GCDs may argue against increased withdrawals due to depletion risks",
        counter_arguments=[
            "Operator can demonstrate sustainable withdrawal rates",
            "Recent recharge data supports viability",
            "Water quality meets frac standards"
        ],
        resolution_strategy="Submit comprehensive hydrogeologic analysis and variance request to GCD; comply with TWDB permitting requirements.",
        entity_scope="Operators, GCDs, TWDB",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TWDB Well Permitting Decisions 2017-2023"
    ),
    DoctrineBlock(
        topic="Pecos Valley Aquifer: Regulatory and Hydrogeologic Constraints",
        keywords=["Pecos Valley", "aquifer", "regulation", "hydrogeology", "constraints", "water sourcing"],
        conclusion_template="Frac water sourcing from the Pecos Valley Aquifer is constrained by both regulatory limits and hydrogeologic factors, requiring detailed compliance and impact analysis.",
        reasoning_framework=(
            "1. Identify GCDs with jurisdiction over the Pecos Valley Aquifer.\n"
            "2. Review regulatory production limits and variance history.\n"
            "3. Analyze hydrogeologic data: transmissivity, storativity, recharge rates.\n"
            "4. Assess water quality parameters relevant to frac operations.\n"
            "5. Examine legal requirements for well permitting and monitoring.\n"
            "6. Evaluate drought resilience and seasonal availability.\n"
            "7. Consider stakeholder objections (municipal, agricultural users).\n"
            "8. Integrate findings to determine sourcing feasibility."
        ),
        key_factors=[
            "GCD regulatory limits",
            "Hydrogeologic properties",
            "Water quality",
            "Permitting process",
            "Stakeholder interests",
            "Drought resilience"
        ],
        primary_authority=[
            "Pecos Valley GCD",
            "TWDB",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Operator",
        adversary_position="Municipal and agricultural users may oppose industrial withdrawals",
        counter_arguments=[
            "Operator can propose mitigation measures",
            "Hydrogeologic modeling supports sustainable use",
            "Compliance with monitoring and reporting"
        ],
        resolution_strategy="Negotiate with GCD and stakeholders; provide impact studies and mitigation plans.",
        entity_scope="Operators, GCDs, municipalities",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Pecos Valley GCD Permit Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Edwards-Trinity Aquifer: Legal and Quality Considerations",
        keywords=["Edwards-Trinity", "aquifer", "legal", "water quality", "frac operations"],
        conclusion_template="Sourcing frac water from the Edwards-Trinity Aquifer requires compliance with legal restrictions and water quality standards, with additional scrutiny on cross-jurisdictional withdrawals.",
        reasoning_framework=(
            "1. Review legal framework governing Edwards-Trinity Aquifer withdrawals.\n"
            "2. Assess cross-jurisdictional issues (multiple GCDs).\n"
            "3. Evaluate water quality parameters (TDS, hardness, contaminants).\n"
            "4. Examine permitting requirements and recent enforcement actions.\n"
            "5. Consider historical disputes and legal precedents.\n"
            "6. Analyze operational impacts from water quality deviations.\n"
            "7. Synthesize legal and quality findings for sourcing decision."
        ),
        key_factors=[
            "Legal restrictions",
            "Cross-jurisdictional issues",
            "Water quality",
            "Permitting requirements",
            "Historical legal disputes"
        ],
        primary_authority=[
            "Edwards Aquifer Authority",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs and environmental groups may challenge withdrawals",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Water quality meets frac standards",
            "Legal precedents favor industrial use"
        ],
        resolution_strategy="Obtain legal counsel; submit water quality analysis and compliance documentation.",
        entity_scope="Operators, GCDs, environmental groups",
        confidence=0.77,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Dockum Aquifer: Suitability and Regulatory Barriers",
        keywords=["Dockum", "aquifer", "suitability", "regulatory", "barriers", "frac water"],
        conclusion_template="Dockum Aquifer is generally unsuitable for frac water sourcing due to high TDS and regulatory barriers, but exceptions exist with advanced treatment and negotiated variances.",
        reasoning_framework=(
            "1. Analyze Dockum Aquifer water quality data (TDS, hardness, contaminants).\n"
            "2. Review GCD regulatory restrictions and variance history.\n"
            "3. Evaluate feasibility of advanced water treatment for frac use.\n"
            "4. Examine permitting process and recent denials/approvals.\n"
            "5. Consider operational costs and risks.\n"
            "6. Assess stakeholder positions and environmental concerns.\n"
            "7. Integrate findings to determine suitability and regulatory path."
        ),
        key_factors=[
            "Water quality (TDS, hardness)",
            "Regulatory restrictions",
            "Treatment feasibility",
            "Permitting process",
            "Operational costs"
        ],
        primary_authority=[
            "Dockum GCD",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs and environmental stakeholders may oppose withdrawals",
        counter_arguments=[
            "Operator can propose advanced treatment",
            "Variance history supports exceptions",
            "Compliance with monitoring"
        ],
        resolution_strategy="Submit treatment plan and variance request; negotiate with GCD.",
        entity_scope="Operators, GCDs, environmental stakeholders",
        confidence=0.68,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Dockum GCD Permit Decisions 2019-2023"
    ),
    DoctrineBlock(
        topic="Santa Rosa Aquifer: Freshwater Sourcing and Drought Resilience",
        keywords=["Santa Rosa", "aquifer", "freshwater", "drought resilience", "frac operations"],
        conclusion_template="Santa Rosa Aquifer offers moderate drought resilience for frac water sourcing, but requires ongoing monitoring and adaptive withdrawal strategies.",
        reasoning_framework=(
            "1. Evaluate Santa Rosa Aquifer recharge and drought resilience data.\n"
            "2. Review GCD production limits and historical enforcement.\n"
            "3. Assess water quality parameters for frac suitability.\n"
            "4. Examine seasonal availability and drought index projections.\n"
            "5. Analyze operational strategies for adaptive withdrawals.\n"
            "6. Consider stakeholder interests and environmental impacts.\n"
            "7. Synthesize findings for sourcing decision."
        ),
        key_factors=[
            "Drought resilience",
            "Recharge rates",
            "Production limits",
            "Water quality",
            "Adaptive withdrawal strategies"
        ],
        primary_authority=[
            "Santa Rosa GCD",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may restrict withdrawals during drought",
        counter_arguments=[
            "Operator can implement adaptive strategies",
            "Monitoring supports sustainable use",
            "Water quality meets frac requirements"
        ],
        resolution_strategy="Develop adaptive withdrawal plan; negotiate with GCD for conditional permits.",
        entity_scope="Operators, GCDs",
        confidence=0.72,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Santa Rosa GCD Drought Management Policies 2016-2022"
    ),
    DoctrineBlock(
        topic="TWDB Freshwater Well Permitting: Process and Pitfalls",
        keywords=["TWDB", "well permitting", "freshwater", "process", "pitfalls"],
        conclusion_template="TWDB freshwater well permitting requires strict compliance with application procedures, technical documentation, and stakeholder notification; common pitfalls include incomplete submissions and insufficient hydrogeologic analysis.",
        reasoning_framework=(
            "1. Review TWDB permitting process steps and documentation requirements.\n"
            "2. Analyze recent permit denials and reasons for rejection.\n"
            "3. Evaluate hydrogeologic analysis standards.\n"
            "4. Assess stakeholder notification and public hearing requirements.\n"
            "5. Examine legal requirements for well construction and monitoring.\n"
            "6. Identify common pitfalls and mitigation strategies.\n"
            "7. Synthesize findings for successful permitting."
        ),
        key_factors=[
            "Application completeness",
            "Hydrogeologic analysis",
            "Stakeholder notification",
            "Legal compliance",
            "Monitoring requirements"
        ],
        primary_authority=[
            "TWDB",
            "Texas Water Code",
            "Texas Administrative Code Title 30"
        ],
        burden_holder="Applicant",
        adversary_position="TWDB may deny permits for incomplete or non-compliant applications",
        counter_arguments=[
            "Applicant can submit supplemental documentation",
            "Demonstrate compliance with standards",
            "Engage stakeholders early"
        ],
        resolution_strategy="Ensure complete application; conduct thorough hydrogeologic analysis; engage stakeholders.",
        entity_scope="Applicants, TWDB",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TWDB Well Permitting Guidelines 2020-2023"
    ),
    DoctrineBlock(
        topic="GCD Production Limits: Enforcement and Variance",
        keywords=["GCD", "production limits", "enforcement", "variance", "frac water"],
        conclusion_template="GCD production limits are strictly enforced, but variances may be granted for frac operations with robust hydrogeologic justification and stakeholder engagement.",
        reasoning_framework=(
            "1. Review GCD production limit policies and enforcement history.\n"
            "2. Analyze variance criteria and past approvals/denials.\n"
            "3. Evaluate hydrogeologic justification requirements.\n"
            "4. Assess stakeholder engagement and opposition.\n"
            "5. Examine monitoring and reporting obligations.\n"
            "6. Identify legal precedents and dispute resolution mechanisms.\n"
            "7. Synthesize findings for variance strategy."
        ),
        key_factors=[
            "Production limit policy",
            "Variance criteria",
            "Hydrogeologic justification",
            "Stakeholder engagement",
            "Monitoring obligations"
        ],
        primary_authority=[
            "GCDs",
            "Texas Water Code Chapter 36",
            "TWDB"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny variances for insufficient justification",
        counter_arguments=[
            "Operator can provide robust hydrogeologic analysis",
            "Engage stakeholders proactively",
            "Demonstrate compliance with monitoring"
        ],
        resolution_strategy="Submit comprehensive variance application; negotiate with GCD and stakeholders.",
        entity_scope="Operators, GCDs",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Variance Decisions 2017-2023"
    ),
    DoctrineBlock(
        topic="Water Quality Parameters: TDS and Hardness for Frac Use",
        keywords=["water quality", "TDS", "hardness", "frac use", "parameters"],
        conclusion_template="Frac water must meet specific TDS and hardness parameters; aquifer suitability is determined by laboratory analysis and regulatory standards.",
        reasoning_framework=(
            "1. Review regulatory standards for TDS and hardness in frac water.\n"
            "2. Analyze laboratory data from target aquifers.\n"
            "3. Evaluate treatment options for water quality deviations.\n"
            "4. Assess operational impacts from high TDS/hardness.\n"
            "5. Examine legal requirements for water quality reporting.\n"
            "6. Synthesize findings for aquifer suitability."
        ),
        key_factors=[
            "TDS standards",
            "Hardness standards",
            "Laboratory analysis",
            "Treatment options",
            "Operational impacts"
        ],
        primary_authority=[
            "TWDB",
            "Texas Railroad Commission",
            "Texas Administrative Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators may reject water sources with high TDS/hardness",
        counter_arguments=[
            "Operator can propose treatment",
            "Demonstrate compliance with standards",
            "Provide operational mitigation plans"
        ],
        resolution_strategy="Conduct laboratory analysis; submit treatment plan if needed.",
        entity_scope="Operators, regulators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Railroad Commission Water Quality Guidelines 2019-2023"
    ),
    DoctrineBlock(
        topic="Seasonal Availability: Aquifer Response to Drought",
        keywords=["seasonal availability", "aquifer", "drought", "response", "frac water"],
        conclusion_template="Aquifer response to drought significantly impacts seasonal availability for frac water sourcing; adaptive planning is required to mitigate supply risks.",
        reasoning_framework=(
            "1. Analyze historical aquifer response to drought conditions.\n"
            "2. Review seasonal availability projections and recharge rates.\n"
            "3. Evaluate operational impacts from supply fluctuations.\n"
            "4. Assess regulatory restrictions during drought periods.\n"
            "5. Examine adaptive planning strategies and monitoring requirements.\n"
            "6. Synthesize findings for sourcing decision."
        ),
        key_factors=[
            "Historical drought response",
            "Seasonal availability",
            "Recharge rates",
            "Regulatory restrictions",
            "Adaptive planning"
        ],
        primary_authority=[
            "TWDB",
            "GCDs",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may restrict withdrawals during drought",
        counter_arguments=[
            "Operator can implement adaptive strategies",
            "Monitoring supports sustainable use",
            "Supply risk mitigation plans"
        ],
        resolution_strategy="Develop adaptive sourcing plan; negotiate conditional permits with GCD.",
        entity_scope="Operators, GCDs",
        confidence=0.76,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="TWDB Drought Response Guidelines 2018-2022"
    ),
    DoctrineBlock(
        topic="Drought Index Correlation: Predictive Planning",
        keywords=["drought index", "correlation", "predictive planning", "aquifer", "frac water"],
        conclusion_template="Drought index correlation enables predictive planning for frac water sourcing, improving supply reliability and regulatory compliance.",
        reasoning_framework=(
            "1. Review drought index methodologies and historical data.\n"
            "2. Analyze correlation between drought index and aquifer levels.\n"
            "3. Evaluate predictive planning models for frac water supply.\n"
            "4. Assess regulatory requirements for drought contingency planning.\n"
            "5. Examine operational strategies for supply reliability.\n"
            "6. Synthesize findings for planning framework."
        ),
        key_factors=[
            "Drought index methodology",
            "Aquifer level correlation",
            "Predictive planning models",
            "Regulatory requirements",
            "Supply reliability"
        ],
        primary_authority=[
            "TWDB",
            "Texas Water Code",
            "GCDs"
        ],
        burden_holder="Operator",
        adversary_position="Regulators may require contingency plans for drought",
        counter_arguments=[
            "Operator can implement predictive planning",
            "Demonstrate supply reliability",
            "Compliance with contingency requirements"
        ],
        resolution_strategy="Integrate drought index analysis into sourcing plan; submit contingency documentation.",
        entity_scope="Operators, regulators",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TWDB Drought Contingency Planning Guidelines 2020-2023"
    ),
    DoctrineBlock(
        topic="Frac Water Quality Requirements: Regulatory and Operational Standards",
        keywords=["frac water", "quality requirements", "regulatory", "operational standards"],
        conclusion_template="Frac water quality requirements are defined by regulatory and operational standards; compliance is mandatory for permitting and successful operations.",
        reasoning_framework=(
            "1. Review regulatory standards for frac water quality (TDS, hardness, contaminants).\n"
            "2. Analyze operational standards and industry best practices.\n"
            "3. Evaluate laboratory analysis and reporting requirements.\n"
            "4. Assess compliance strategies and monitoring obligations.\n"
            "5. Examine legal precedents for enforcement actions.\n"
            "6. Synthesize findings for compliance plan."
        ),
        key_factors=[
            "Regulatory standards",
            "Operational standards",
            "Laboratory analysis",
            "Reporting requirements",
            "Monitoring obligations"
        ],
        primary_authority=[
            "Texas Railroad Commission",
            "TWDB",
            "Texas Administrative Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators may enforce penalties for non-compliance",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Implement monitoring and reporting",
            "Adopt industry best practices"
        ],
        resolution_strategy="Develop compliance plan; submit laboratory analysis and monitoring documentation.",
        entity_scope="Operators, regulators",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Railroad Commission Enforcement Actions 2019-2023"
    ),
    DoctrineBlock(
        topic="Carrizo-Wilcox Aquifer: Permitting and Water Quality",
        keywords=["Carrizo-Wilcox", "aquifer", "permitting", "water quality", "frac operations"],
        conclusion_template="Carrizo-Wilcox Aquifer is generally suitable for frac water sourcing, subject to GCD permitting and water quality compliance.",
        reasoning_framework=(
            "1. Review Carrizo-Wilcox GCD permitting requirements.\n"
            "2. Analyze water quality parameters (TDS, hardness, contaminants).\n"
            "3. Evaluate historical permit approvals and denials.\n"
            "4. Assess operational impacts from water quality deviations.\n"
            "5. Examine monitoring and reporting obligations.\n"
            "6. Synthesize findings for sourcing decision."
        ),
        key_factors=[
            "Permitting requirements",
            "Water quality",
            "Historical permit approvals",
            "Monitoring obligations",
            "Operational impacts"
        ],
        primary_authority=[
            "Carrizo-Wilcox GCD",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may restrict withdrawals for non-compliance",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Water quality meets frac standards",
            "Monitoring supports sustainable use"
        ],
        resolution_strategy="Submit permit application with water quality analysis; comply with monitoring requirements.",
        entity_scope="Operators, GCDs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Carrizo-Wilcox GCD Permit Decisions 2017-2022"
    ),
    DoctrineBlock(
        topic="Trinity Aquifer: Water Quality and Regulatory Compliance",
        keywords=["Trinity", "aquifer", "water quality", "regulatory compliance", "frac operations"],
        conclusion_template="Trinity Aquifer is a viable source for frac water, provided regulatory compliance and water quality standards are met.",
        reasoning_framework=(
            "1. Review Trinity GCD regulatory requirements and enforcement history.\n"
            "2. Analyze water quality parameters (TDS, hardness, contaminants).\n"
            "3. Evaluate operational impacts from water quality deviations.\n"
            "4. Assess monitoring and reporting obligations.\n"
            "5. Examine legal precedents for enforcement actions.\n"
            "6. Synthesize findings for sourcing decision."
        ),
        key_factors=[
            "Regulatory requirements",
            "Water quality",
            "Operational impacts",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "Trinity GCD",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may restrict withdrawals for non-compliance",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Water quality meets frac standards",
            "Monitoring supports sustainable use"
        ],
        resolution_strategy="Submit permit application with water quality analysis; comply with monitoring requirements.",
        entity_scope="Operators, GCDs",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trinity GCD Permit Decisions 2016-2022"
    ),
    DoctrineBlock(
        topic="Brazos River Alluvium: Surface-Groundwater Interaction",
        keywords=["Brazos River", "alluvium", "surface water", "groundwater", "interaction", "frac water"],
        conclusion_template="Sourcing frac water from Brazos River Alluvium requires careful analysis of surface-groundwater interaction and compliance with both surface and groundwater permitting.",
        reasoning_framework=(
            "1. Review hydrologic studies of surface-groundwater interaction.\n"
            "2. Analyze permitting requirements for both surface and groundwater withdrawals.\n"
            "3. Evaluate water quality parameters for frac suitability.\n"
            "4. Assess stakeholder interests and environmental impacts.\n"
            "5. Examine legal precedents for surface-groundwater disputes.\n"
            "6. Synthesize findings for sourcing decision."
        ),
        key_factors=[
            "Hydrologic interaction",
            "Permitting requirements",
            "Water quality",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "TWDB",
            "Texas Commission on Environmental Quality (TCEQ)",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ and GCDs may restrict withdrawals for environmental protection",
        counter_arguments=[
            "Operator can demonstrate minimal impact",
            "Compliance with both permitting regimes",
            "Water quality meets frac standards"
        ],
        resolution_strategy="Submit hydrologic analysis; comply with both surface and groundwater permitting.",
        entity_scope="Operators, TCEQ, GCDs",
        confidence=0.78,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Brazos River Alluvium Permit Decisions 2018-2023"
    ),
    DoctrineBlock(
        topic="Permian Basin: Water Sourcing Strategies",
        keywords=["Permian Basin", "water sourcing", "frac operations", "strategies"],
        conclusion_template="Water sourcing strategies in the Permian Basin require integration of multiple aquifer sources, regulatory compliance, and adaptive planning for drought resilience.",
        reasoning_framework=(
            "1. Identify available aquifer sources in the Permian Basin.\n"
            "2. Review regulatory requirements for each source.\n"
            "3. Analyze water quality parameters and operational impacts.\n"
            "4. Evaluate adaptive planning strategies for drought resilience.\n"
            "5. Assess stakeholder interests and environmental impacts.\n"
            "6. Synthesize findings for integrated sourcing strategy."
        ),
        key_factors=[
            "Aquifer availability",
            "Regulatory requirements",
            "Water quality",
            "Adaptive planning",
            "Stakeholder interests"
        ],
        primary_authority=[
            "TWDB",
            "GCDs",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators and stakeholders may restrict withdrawals",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Implement adaptive planning",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Develop integrated sourcing plan; negotiate with regulators and stakeholders.",
        entity_scope="Operators, regulators, stakeholders",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Permian Basin Water Sourcing Guidelines 2019-2023"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Jurisdictional Overlap",
        keywords=["GCD", "jurisdictional overlap", "groundwater", "regulation", "frac operations"],
        conclusion_template="Jurisdictional overlap among GCDs may complicate frac water permitting; operators must coordinate with all relevant districts and comply with the strictest applicable standards.",
        reasoning_framework=(
            "1. Identify all GCDs with jurisdiction over the target aquifer.\n"
            "2. Review regulatory requirements and enforcement history for each GCD.\n"
            "3. Analyze legal precedents for jurisdictional disputes.\n"
            "4. Assess operational impacts from overlapping regulations.\n"
            "5. Evaluate coordination strategies and stakeholder engagement.\n"
            "6. Synthesize findings for permitting strategy."
        ),
        key_factors=[
            "Jurisdictional overlap",
            "Regulatory requirements",
            "Legal precedents",
            "Operational impacts",
            "Coordination strategies"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may enforce conflicting requirements",
        counter_arguments=[
            "Operator can coordinate with all GCDs",
            "Comply with strictest standards",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Coordinate permitting with all GCDs; comply with strictest standards.",
        entity_scope="Operators, GCDs",
        confidence=0.75,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Water Code Section 36.1071"
    ),
    DoctrineBlock(
        topic="Water Transfer: Inter-Basin Regulatory Barriers",
        keywords=["water transfer", "inter-basin", "regulatory barriers", "frac water"],
        conclusion_template="Inter-basin water transfer for frac operations faces significant regulatory barriers; operators must obtain permits from both source and receiving basin authorities.",
        reasoning_framework=(
            "1. Review regulatory requirements for inter-basin water transfer.\n"
            "2. Analyze permitting process for both source and receiving basin.\n"
            "3. Evaluate legal precedents for inter-basin disputes.\n"
            "4. Assess operational impacts and stakeholder interests.\n"
            "5. Examine environmental impact analysis requirements.\n"
            "6. Synthesize findings for transfer strategy."
        ),
        key_factors=[
            "Regulatory requirements",
            "Permitting process",
            "Legal precedents",
            "Operational impacts",
            "Environmental impact analysis"
        ],
        primary_authority=[
            "TWDB",
            "TCEQ",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Source and receiving basin authorities may restrict transfers",
        counter_arguments=[
            "Operator can demonstrate minimal impact",
            "Compliance with both permitting regimes",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Obtain permits from both authorities; submit environmental impact analysis.",
        entity_scope="Operators, TWDB, TCEQ",
        confidence=0.69,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Water Code Chapter 36 and 11"
    ),
    DoctrineBlock(
        topic="Aquifer Storage and Recovery: Regulatory Framework",
        keywords=["aquifer storage", "recovery", "regulatory framework", "frac water"],
        conclusion_template="Aquifer storage and recovery (ASR) projects for frac water require compliance with TWDB and GCD regulatory frameworks, including monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review TWDB and GCD regulatory frameworks for ASR projects.\n"
            "2. Analyze permitting requirements and monitoring obligations.\n"
            "3. Evaluate operational impacts and stakeholder interests.\n"
            "4. Assess legal precedents for ASR disputes.\n"
            "5. Examine environmental impact analysis requirements.\n"
            "6. Synthesize findings for ASR project strategy."
        ),
        key_factors=[
            "Regulatory frameworks",
            "Permitting requirements",
            "Monitoring obligations",
            "Operational impacts",
            "Environmental impact analysis"
        ],
        primary_authority=[
            "TWDB",
            "GCDs",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators and stakeholders may restrict ASR projects",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Submit robust monitoring plan",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with regulatory frameworks; submit monitoring and environmental impact analysis.",
        entity_scope="Operators, TWDB, GCDs",
        confidence=0.74,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="TWDB ASR Guidelines 2018-2023"
    ),
    DoctrineBlock(
        topic="Produced Water Reuse: Legal and Operational Barriers",
        keywords=["produced water", "reuse", "legal barriers", "operational barriers", "frac operations"],
        conclusion_template="Produced water reuse for frac operations faces legal and operational barriers, including regulatory restrictions and treatment requirements.",
        reasoning_framework=(
            "1. Review regulatory restrictions for produced water reuse.\n"
            "2. Analyze legal precedents for produced water disputes.\n"
            "3. Evaluate treatment requirements and operational impacts.\n"
            "4. Assess stakeholder interests and environmental concerns.\n"
            "5. Examine monitoring and reporting obligations.\n"
            "6. Synthesize findings for reuse strategy."
        ),
        key_factors=[
            "Regulatory restrictions",
            "Legal precedents",
            "Treatment requirements",
            "Operational impacts",
            "Stakeholder interests"
        ],
        primary_authority=[
            "Texas Railroad Commission",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators and stakeholders may restrict reuse",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Submit robust treatment plan",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with regulatory restrictions; submit treatment and monitoring plans.",
        entity_scope="Operators, regulators, stakeholders",
        confidence=0.66,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Railroad Commission Produced Water Guidelines 2019-2023"
    ),
    DoctrineBlock(
        topic="Groundwater Monitoring: Compliance and Enforcement",
        keywords=["groundwater", "monitoring", "compliance", "enforcement", "frac operations"],
        conclusion_template="Groundwater monitoring is mandatory for frac water operations, with strict enforcement and reporting obligations under GCD and TWDB regulations.",
        reasoning_framework=(
            "1. Review GCD and TWDB monitoring requirements.\n"
            "2. Analyze enforcement history and penalties for non-compliance.\n"
            "3. Evaluate operational impacts from monitoring obligations.\n"
            "4. Assess legal precedents for monitoring disputes.\n"
            "5. Examine stakeholder interests and environmental concerns.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Monitoring requirements",
            "Enforcement history",
            "Reporting obligations",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators may enforce penalties for non-compliance",
        counter_arguments=[
            "Operator can demonstrate compliance",
            "Submit robust monitoring plan",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Develop comprehensive monitoring plan; comply with reporting obligations.",
        entity_scope="Operators, GCDs, TWDB",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TWDB Monitoring Enforcement Actions 2018-2023"
    ),
    DoctrineBlock(
        topic="Groundwater Rights: Ownership and Transfer",
        keywords=["groundwater rights", "ownership", "transfer", "frac operations"],
        conclusion_template="Groundwater rights for frac operations are governed by Texas Water Code and legal precedents; transfer requires compliance with documentation and GCD approval.",
        reasoning_framework=(
            "1. Review Texas Water Code provisions for groundwater rights.\n"
            "2. Analyze legal precedents for ownership and transfer disputes.\n"
            "3. Evaluate documentation requirements for transfer.\n"
            "4. Assess GCD approval process and stakeholder interests.\n"
            "5. Examine operational impacts from rights transfer.\n"
            "6. Synthesize findings for transfer strategy."
        ),
        key_factors=[
            "Legal provisions",
            "Ownership precedents",
            "Documentation requirements",
            "GCD approval",
            "Operational impacts"
        ],
        primary_authority=[
            "Texas Water Code",
            "GCDs",
            "TWDB"
        ],
        burden_holder="Transferor and transferee",
        adversary_position="GCDs may restrict transfer for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with legal provisions",
            "Submit complete documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with legal and GCD requirements; submit documentation for approval.",
        entity_scope="Operators, GCDs",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court: Edwards Aquifer Authority v. Day"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Renewal",
        keywords=["GCD", "permit renewal", "groundwater", "frac operations"],
        conclusion_template="GCD permit renewal for frac water operations requires demonstration of compliance with monitoring, reporting, and production limits.",
        reasoning_framework=(
            "1. Review GCD permit renewal requirements.\n"
            "2. Analyze compliance history and monitoring reports.\n"
            "3. Evaluate production limit adherence.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for renewal disputes.\n"
            "6. Synthesize findings for renewal strategy."
        ),
        key_factors=[
            "Renewal requirements",
            "Compliance history",
            "Monitoring reports",
            "Production limits",
            "Stakeholder interests"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny renewal for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with requirements",
            "Submit monitoring and production reports",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit renewal application with compliance documentation; negotiate with GCD.",
        entity_scope="Operators, GCDs",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Renewal Decisions 2017-2022"
    ),
    DoctrineBlock(
        topic="Water Quality Reporting: Regulatory Obligations",
        keywords=["water quality", "reporting", "regulatory obligations", "frac operations"],
        conclusion_template="Water quality reporting is a regulatory obligation for frac water operations; failure to comply may result in penalties and permit revocation.",
        reasoning_framework=(
            "1. Review regulatory requirements for water quality reporting.\n"
            "2. Analyze enforcement history and penalties for non-compliance.\n"
            "3. Evaluate operational impacts from reporting obligations.\n"
            "4. Assess legal precedents for reporting disputes.\n"
            "5. Examine stakeholder interests and environmental concerns.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Reporting requirements",
            "Enforcement history",
            "Operational impacts",
            "Legal precedents",
            "Stakeholder interests"
        ],
        primary_authority=[
            "TWDB",
            "Texas Railroad Commission",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Regulators may enforce penalties for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with reporting requirements",
            "Submit robust reporting plan",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Develop comprehensive reporting plan; comply with regulatory obligations.",
        entity_scope="Operators, TWDB, Texas Railroad Commission",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="TWDB Reporting Enforcement Actions 2019-2023"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Enforcement Actions",
        keywords=["GCD", "enforcement actions", "groundwater", "frac operations"],
        conclusion_template="GCD enforcement actions for frac water operations are governed by Texas Water Code and district policies; operators must comply with corrective actions to avoid penalties.",
        reasoning_framework=(
            "1. Review GCD enforcement policies and Texas Water Code provisions.\n"
            "2. Analyze enforcement history and penalties for non-compliance.\n"
            "3. Evaluate corrective action requirements.\n"
            "4. Assess operational impacts from enforcement actions.\n"
            "5. Examine legal precedents for enforcement disputes.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Enforcement policies",
            "Penalties for non-compliance",
            "Corrective action requirements",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may enforce penalties for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with corrective actions",
            "Submit compliance documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with enforcement policies; submit corrective action documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Enforcement Actions 2018-2023"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Stakeholder Engagement",
        keywords=["GCD", "stakeholder engagement", "groundwater", "frac operations"],
        conclusion_template="Stakeholder engagement is critical for successful frac water permitting with GCDs; operators must address concerns and negotiate mitigation measures.",
        reasoning_framework=(
            "1. Identify stakeholders affected by frac water operations.\n"
            "2. Review GCD stakeholder engagement policies.\n"
            "3. Analyze historical stakeholder opposition and mitigation measures.\n"
            "4. Evaluate operational impacts from stakeholder engagement.\n"
            "5. Assess legal precedents for stakeholder disputes.\n"
            "6. Synthesize findings for engagement strategy."
        ),
        key_factors=[
            "Stakeholder identification",
            "Engagement policies",
            "Mitigation measures",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="Stakeholders may oppose frac water operations",
        counter_arguments=[
            "Address stakeholder concerns",
            "Negotiate mitigation measures",
            "Engage proactively"
        ],
        resolution_strategy="Develop stakeholder engagement plan; negotiate mitigation measures.",
        entity_scope="Operators, GCDs, stakeholders",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Stakeholder Engagement Guidelines 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Variance Appeals",
        keywords=["GCD", "variance appeals", "groundwater", "frac operations"],
        conclusion_template="Variance appeals for frac water operations with GCDs require robust hydrogeologic justification and legal counsel; success depends on compliance history and stakeholder support.",
        reasoning_framework=(
            "1. Review GCD variance appeal process and criteria.\n"
            "2. Analyze hydrogeologic justification requirements.\n"
            "3. Evaluate legal counsel involvement and appeal history.\n"
            "4. Assess compliance history and stakeholder support.\n"
            "5. Examine legal precedents for variance appeals.\n"
            "6. Synthesize findings for appeal strategy."
        ),
        key_factors=[
            "Appeal process",
            "Hydrogeologic justification",
            "Legal counsel",
            "Compliance history",
            "Stakeholder support"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny appeals for insufficient justification",
        counter_arguments=[
            "Submit robust hydrogeologic analysis",
            "Engage legal counsel",
            "Demonstrate compliance history"
        ],
        resolution_strategy="Submit appeal with hydrogeologic and legal documentation; engage stakeholders.",
        entity_scope="Operators, GCDs",
        confidence=0.70,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Variance Appeal Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Revocation",
        keywords=["GCD", "permit revocation", "groundwater", "frac operations"],
        conclusion_template="GCD permit revocation for frac water operations is enforced for non-compliance with monitoring, reporting, or production limits; operators must comply with corrective actions to avoid revocation.",
        reasoning_framework=(
            "1. Review GCD permit revocation policies and Texas Water Code provisions.\n"
            "2. Analyze enforcement history and reasons for revocation.\n"
            "3. Evaluate corrective action requirements.\n"
            "4. Assess operational impacts from permit revocation.\n"
            "5. Examine legal precedents for revocation disputes.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Revocation policies",
            "Reasons for revocation",
            "Corrective action requirements",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may revoke permits for non-compliance",
        counter_arguments=[
            "Comply with corrective actions",
            "Submit compliance documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with revocation policies; submit corrective action documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Revocation Actions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Modification",
        keywords=["GCD", "permit modification", "groundwater", "frac operations"],
        conclusion_template="Permit modification for frac water operations with GCDs requires demonstration of changed circumstances and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit modification requirements.\n"
            "2. Analyze changed circumstances and justification.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for modification disputes.\n"
            "6. Synthesize findings for modification strategy."
        ),
        key_factors=[
            "Modification requirements",
            "Changed circumstances",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny modification for insufficient justification",
        counter_arguments=[
            "Demonstrate changed circumstances",
            "Submit monitoring and reporting documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit modification application with justification and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.73,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Modification Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Transfer",
        keywords=["GCD", "permit transfer", "groundwater", "frac operations"],
        conclusion_template="Permit transfer for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit transfer requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for transfer disputes.\n"
            "6. Synthesize findings for transfer strategy."
        ),
        key_factors=[
            "Transfer requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Transferor and transferee",
        adversary_position="GCDs may deny transfer for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit transfer application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Transfer Decisions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Suspension",
        keywords=["GCD", "permit suspension", "groundwater", "frac operations"],
        conclusion_template="Permit suspension for frac water operations with GCDs is enforced for violations of monitoring, reporting, or production limits; operators must comply with corrective actions to lift suspension.",
        reasoning_framework=(
            "1. Review GCD permit suspension policies and Texas Water Code provisions.\n"
            "2. Analyze enforcement history and reasons for suspension.\n"
            "3. Evaluate corrective action requirements.\n"
            "4. Assess operational impacts from permit suspension.\n"
            "5. Examine legal precedents for suspension disputes.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Suspension policies",
            "Reasons for suspension",
            "Corrective action requirements",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may suspend permits for non-compliance",
        counter_arguments=[
            "Comply with corrective actions",
            "Submit compliance documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with suspension policies; submit corrective action documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Suspension Actions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Amendment",
        keywords=["GCD", "permit amendment", "groundwater", "frac operations"],
        conclusion_template="Permit amendment for frac water operations with GCDs requires demonstration of changed circumstances and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit amendment requirements.\n"
            "2. Analyze changed circumstances and justification.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for amendment disputes.\n"
            "6. Synthesize findings for amendment strategy."
        ),
        key_factors=[
            "Amendment requirements",
            "Changed circumstances",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny amendment for insufficient justification",
        counter_arguments=[
            "Demonstrate changed circumstances",
            "Submit monitoring and reporting documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit amendment application with justification and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.74,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Amendment Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Extension",
        keywords=["GCD", "permit extension", "groundwater", "frac operations"],
        conclusion_template="Permit extension for frac water operations with GCDs requires demonstration of continued compliance with monitoring, reporting, and production limits.",
        reasoning_framework=(
            "1. Review GCD permit extension requirements.\n"
            "2. Analyze compliance history and monitoring reports.\n"
            "3. Evaluate production limit adherence.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for extension disputes.\n"
            "6. Synthesize findings for extension strategy."
        ),
        key_factors=[
            "Extension requirements",
            "Compliance history",
            "Monitoring reports",
            "Production limits",
            "Stakeholder interests"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny extension for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with requirements",
            "Submit monitoring and production reports",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit extension application with compliance documentation; negotiate with GCD.",
        entity_scope="Operators, GCDs",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Extension Decisions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Reinstatement",
        keywords=["GCD", "permit reinstatement", "groundwater", "frac operations"],
        conclusion_template="Permit reinstatement for frac water operations with GCDs requires demonstration of corrective actions and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit reinstatement requirements.\n"
            "2. Analyze corrective actions and compliance documentation.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for reinstatement disputes.\n"
            "6. Synthesize findings for reinstatement strategy."
        ),
        key_factors=[
            "Reinstatement requirements",
            "Corrective actions",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny reinstatement for insufficient corrective actions",
        counter_arguments=[
            "Submit corrective action documentation",
            "Demonstrate compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit reinstatement application with corrective action and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.72,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Reinstatement Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Consolidation",
        keywords=["GCD", "permit consolidation", "groundwater", "frac operations"],
        conclusion_template="Permit consolidation for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit consolidation requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for consolidation disputes.\n"
            "6. Synthesize findings for consolidation strategy."
        ),
        key_factors=[
            "Consolidation requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny consolidation for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit consolidation application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.76,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Consolidation Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Splitting",
        keywords=["GCD", "permit splitting", "groundwater", "frac operations"],
        conclusion_template="Permit splitting for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit splitting requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for splitting disputes.\n"
            "6. Synthesize findings for splitting strategy."
        ),
        key_factors=[
            "Splitting requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny splitting for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit splitting application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.75,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Splitting Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Aggregation",
        keywords=["GCD", "permit aggregation", "groundwater", "frac operations"],
        conclusion_template="Permit aggregation for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit aggregation requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for aggregation disputes.\n"
            "6. Synthesize findings for aggregation strategy."
        ),
        key_factors=[
            "Aggregation requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny aggregation for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit aggregation application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.74,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Aggregation Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Conversion",
        keywords=["GCD", "permit conversion", "groundwater", "frac operations"],
        conclusion_template="Permit conversion for frac water operations with GCDs requires demonstration of changed circumstances and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit conversion requirements.\n"
            "2. Analyze changed circumstances and justification.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for conversion disputes.\n"
            "6. Synthesize findings for conversion strategy."
        ),
        key_factors=[
            "Conversion requirements",
            "Changed circumstances",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny conversion for insufficient justification",
        counter_arguments=[
            "Demonstrate changed circumstances",
            "Submit monitoring and reporting documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit conversion application with justification and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.73,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Conversion Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Reclassification",
        keywords=["GCD", "permit reclassification", "groundwater", "frac operations"],
        conclusion_template="Permit reclassification for frac water operations with GCDs requires demonstration of changed circumstances and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit reclassification requirements.\n"
            "2. Analyze changed circumstances and justification.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for reclassification disputes.\n"
            "6. Synthesize findings for reclassification strategy."
        ),
        key_factors=[
            "Reclassification requirements",
            "Changed circumstances",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny reclassification for insufficient justification",
        counter_arguments=[
            "Demonstrate changed circumstances",
            "Submit monitoring and reporting documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit reclassification application with justification and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.72,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Reclassification Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Renewal Extension",
        keywords=["GCD", "permit renewal extension", "groundwater", "frac operations"],
        conclusion_template="Permit renewal extension for frac water operations with GCDs requires demonstration of continued compliance with monitoring, reporting, and production limits.",
        reasoning_framework=(
            "1. Review GCD permit renewal extension requirements.\n"
            "2. Analyze compliance history and monitoring reports.\n"
            "3. Evaluate production limit adherence.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for renewal extension disputes.\n"
            "6. Synthesize findings for renewal extension strategy."
        ),
        key_factors=[
            "Renewal extension requirements",
            "Compliance history",
            "Monitoring reports",
            "Production limits",
            "Stakeholder interests"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny renewal extension for non-compliance",
        counter_arguments=[
            "Demonstrate compliance with requirements",
            "Submit monitoring and production reports",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit renewal extension application with compliance documentation; negotiate with GCD.",
        entity_scope="Operators, GCDs",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Renewal Extension Decisions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Termination",
        keywords=["GCD", "permit termination", "groundwater", "frac operations"],
        conclusion_template="Permit termination for frac water operations with GCDs is enforced for non-compliance with monitoring, reporting, or production limits; operators must comply with corrective actions to avoid termination.",
        reasoning_framework=(
            "1. Review GCD permit termination policies and Texas Water Code provisions.\n"
            "2. Analyze enforcement history and reasons for termination.\n"
            "3. Evaluate corrective action requirements.\n"
            "4. Assess operational impacts from permit termination.\n"
            "5. Examine legal precedents for termination disputes.\n"
            "6. Synthesize findings for compliance strategy."
        ),
        key_factors=[
            "Termination policies",
            "Reasons for termination",
            "Corrective action requirements",
            "Operational impacts",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may terminate permits for non-compliance",
        counter_arguments=[
            "Comply with corrective actions",
            "Submit compliance documentation",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Comply with termination policies; submit corrective action documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GCD Permit Termination Actions 2017-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Withdrawal",
        keywords=["GCD", "permit withdrawal", "groundwater", "frac operations"],
        conclusion_template="Permit withdrawal for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit withdrawal requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for withdrawal disputes.\n"
            "6. Synthesize findings for withdrawal strategy."
        ),
        key_factors=[
            "Withdrawal requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny withdrawal for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit withdrawal application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.76,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Withdrawal Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Surrender",
        keywords=["GCD", "permit surrender", "groundwater", "frac operations"],
        conclusion_template="Permit surrender for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit surrender requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for surrender disputes.\n"
            "6. Synthesize findings for surrender strategy."
        ),
        key_factors=[
            "Surrender requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny surrender for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit surrender application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.75,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Surrender Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Abandonment",
        keywords=["GCD", "permit abandonment", "groundwater", "frac operations"],
        conclusion_template="Permit abandonment for frac water operations with GCDs requires compliance with documentation and approval process; operators must demonstrate continued compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit abandonment requirements.\n"
            "2. Analyze documentation and approval process.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for abandonment disputes.\n"
            "6. Synthesize findings for abandonment strategy."
        ),
        key_factors=[
            "Abandonment requirements",
            "Documentation",
            "Approval process",
            "Monitoring obligations",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny abandonment for non-compliance",
        counter_arguments=[
            "Submit complete documentation",
            "Demonstrate continued compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit abandonment application with documentation and compliance history.",
        entity_scope="Operators, GCDs",
        confidence=0.74,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Abandonment Decisions 2018-2022"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Districts: Permit Reinstatement after Abandonment",
        keywords=["GCD", "permit reinstatement", "abandonment", "groundwater", "frac operations"],
        conclusion_template="Permit reinstatement after abandonment for frac water operations with GCDs requires demonstration of corrective actions and compliance with monitoring and reporting obligations.",
        reasoning_framework=(
            "1. Review GCD permit reinstatement after abandonment requirements.\n"
            "2. Analyze corrective actions and compliance documentation.\n"
            "3. Evaluate monitoring and reporting obligations.\n"
            "4. Assess stakeholder interests and opposition.\n"
            "5. Examine legal precedents for reinstatement after abandonment disputes.\n"
            "6. Synthesize findings for reinstatement strategy."
        ),
        key_factors=[
            "Reinstatement requirements",
            "Corrective actions",
            "Monitoring obligations",
            "Stakeholder interests",
            "Legal precedents"
        ],
        primary_authority=[
            "GCDs",
            "TWDB",
            "Texas Water Code"
        ],
        burden_holder="Operator",
        adversary_position="GCDs may deny reinstatement for insufficient corrective actions",
        counter_arguments=[
            "Submit corrective action documentation",
            "Demonstrate compliance",
            "Engage stakeholders proactively"
        ],
        resolution_strategy="Submit reinstatement application with corrective action and compliance documentation.",
        entity_scope="Operators, GCDs",
        confidence=0.72,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="GCD Permit Reinstatement after Abandonment Decisions 2018-2022"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]