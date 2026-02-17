from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

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
        topic="RRC Operator P-5 Organization Reports",
        keywords=["P-5", "operator registration", "organization report", "RRC", "compliance"],
        conclusion_template="Operators must file accurate and timely P-5 Organization Reports to maintain active status and eligibility for permits.",
        reasoning_framework="""
The P-5 Organization Report is a foundational compliance document required by the Texas Railroad Commission (RRC) for all oil and gas operators. The report establishes the operator's legal identity, financial assurance, and contact information. Timely submission is critical for maintaining active status and eligibility for permits. The RRC uses the P-5 to verify operator capacity, track organizational changes, and enforce bonding requirements. Operators failing to submit or update P-5 reports risk suspension, loss of permit privileges, and enforcement actions. The doctrine emphasizes the necessity of accuracy, completeness, and promptness in P-5 filings, considering the legal and operational consequences of non-compliance.
        """,
        key_factors=[
            "Timeliness of submission",
            "Accuracy of organizational data",
            "Financial assurance compliance",
            "Change in ownership or structure",
            "RRC enforcement policies"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.1",
            "RRC P-5 Filing Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="RRC enforcement division",
        counter_arguments=[
            "Administrative delays",
            "Unclear guidance on organizational changes",
            "Disputed financial assurance requirements"
        ],
        resolution_strategy="Strict adherence to RRC guidelines; proactive communication with RRC; legal counsel for disputed issues.",
        entity_scope="All Texas oil and gas operators",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="RRC Enforcement Actions 2017-2023"
    ),
    DoctrineBlock(
        topic="W-1 Drilling Permit Applications",
        keywords=["W-1", "drilling permit", "application", "RRC", "well location"],
        conclusion_template="Drilling operations must not commence until a valid W-1 permit is approved and all location requirements are satisfied.",
        reasoning_framework="""
The W-1 Drilling Permit Application is the primary regulatory mechanism for controlling new well development in Texas. The application requires detailed information on well location, lease boundaries, spacing, and operator credentials. The RRC reviews W-1 submissions to ensure compliance with state spacing rules, lease ownership, and environmental safeguards. Operators must demonstrate legal right to drill, proper lease documentation, and adherence to setback requirements. The doctrine underscores the importance of pre-drill due diligence, accurate mapping, and timely submission. Failure to secure a W-1 permit prior to drilling constitutes a major violation, subject to fines and well shut-in orders.
        """,
        key_factors=[
            "Lease boundary verification",
            "Spacing rule compliance",
            "Operator credentials",
            "Environmental review",
            "Timeliness of permit submission"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.5",
            "RRC W-1 Application Instructions"
        ],
        burden_holder="Operator",
        adversary_position="RRC permit review staff",
        counter_arguments=[
            "Disputed lease boundaries",
            "Ambiguous spacing interpretations",
            "Incomplete environmental review"
        ],
        resolution_strategy="Comprehensive pre-application review; GIS mapping; legal review of lease documents.",
        entity_scope="Operators seeking to drill new wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RRC Permit Denials 2018-2023"
    ),
    DoctrineBlock(
        topic="W-1A Recompletions and Amendments",
        keywords=["W-1A", "recompletion", "amendment", "wellbore", "permit"],
        conclusion_template="Operators must file W-1A applications for recompletion or amendment activities, ensuring all changes are documented and approved.",
        reasoning_framework="""
The W-1A form governs recompletion and amendment activities for existing wells. Operators must disclose changes in wellbore configuration, target formation, and operational plans. The RRC evaluates W-1A submissions for compliance with spacing, lease, and environmental regulations. Recompletions often involve complex technical and legal considerations, including zone transfers, multi-lateral drilling, and production allocation. The doctrine stresses the necessity of transparent reporting, technical accuracy, and legal review. Unauthorized recompletions or amendments may result in enforcement actions, production shut-ins, and loss of permit privileges.
        """,
        key_factors=[
            "Technical accuracy of recompletion plan",
            "Documentation of wellbore changes",
            "Compliance with spacing and lease rules",
            "Environmental impact assessment",
            "Timeliness of amendment submission"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.5",
            "RRC W-1A Filing Instructions"
        ],
        burden_holder="Operator",
        adversary_position="RRC technical review staff",
        counter_arguments=[
            "Ambiguous recompletion definitions",
            "Disputed production allocation",
            "Incomplete amendment documentation"
        ],
        resolution_strategy="Detailed engineering review; legal counsel for allocation disputes; proactive RRC engagement.",
        entity_scope="Operators amending or recompleting wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="RRC Recompletions Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Completion Reports G-1 and G-4",
        keywords=["G-1", "G-4", "completion report", "production", "RRC"],
        conclusion_template="Completion reports must accurately reflect well performance and comply with RRC reporting standards to validate production claims.",
        reasoning_framework="""
G-1 and G-4 completion reports are critical for establishing initial well production and regulatory compliance. The G-1 focuses on oil and gas completion, while the G-4 addresses gas well deliverability. Operators must provide detailed technical data, including formation tops, perforation intervals, and initial production rates. The RRC uses these reports to validate production claims, allocate resources, and enforce environmental standards. The doctrine emphasizes the importance of technical precision, timely submission, and alignment with field data. Inaccurate or late completion reports may result in production allocation disputes, regulatory penalties, and reputational harm.
        """,
        key_factors=[
            "Technical accuracy of completion data",
            "Timeliness of report submission",
            "Alignment with field production data",
            "Compliance with RRC standards",
            "Environmental reporting"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.16",
            "RRC G-1 and G-4 Filing Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="RRC production audit staff",
        counter_arguments=[
            "Disputed production rates",
            "Incomplete technical data",
            "Delayed field reporting"
        ],
        resolution_strategy="Field data reconciliation; engineering review; proactive communication with RRC.",
        entity_scope="Operators completing wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RRC Completion Report Audits 2020-2023"
    ),
    DoctrineBlock(
        topic="Production Reports PR",
        keywords=["PR", "production report", "monthly reporting", "RRC", "compliance"],
        conclusion_template="Operators must submit accurate monthly PR production reports to maintain regulatory compliance and avoid enforcement actions.",
        reasoning_framework="""
Monthly Production Reports (PR) are mandatory for all producing wells in Texas. The reports document oil, gas, and condensate volumes, enabling the RRC to monitor production trends, enforce allocation rules, and collect severance taxes. Operators must ensure accuracy, completeness, and timely submission. The doctrine highlights the risks of under-reporting, over-reporting, and late filings, which may trigger audits, penalties, and shut-in orders. Automated reporting systems and reconciliation with field data are recommended to minimize errors and ensure compliance.
        """,
        key_factors=[
            "Accuracy of production volumes",
            "Timeliness of monthly submission",
            "Alignment with field and sales data",
            "Compliance with allocation rules",
            "Severance tax reporting"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.27",
            "RRC PR Filing Instructions"
        ],
        burden_holder="Operator",
        adversary_position="RRC production audit staff",
        counter_arguments=[
            "Field data discrepancies",
            "Sales data mismatches",
            "Administrative delays"
        ],
        resolution_strategy="Automated reporting; field data reconciliation; audit readiness.",
        entity_scope="Operators of producing wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="RRC Production Audits 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Transfer P-4",
        keywords=["P-4", "operator transfer", "ownership change", "RRC", "permit transfer"],
        conclusion_template="Operator transfers must be documented via P-4 filings, ensuring legal continuity and regulatory compliance.",
        reasoning_framework="""
The P-4 form governs operator transfers, including changes in ownership, mergers, and acquisitions. The RRC requires detailed documentation of the transfer, including legal agreements, financial assurance, and updated contact information. The doctrine emphasizes the importance of legal review, timely submission, and verification of permit continuity. Failure to properly document operator transfers may result in permit suspension, enforcement actions, and production shut-ins. The doctrine also addresses the complexities of multi-party transfers, disputed ownership, and legacy liabilities.
        """,
        key_factors=[
            "Legal documentation of transfer",
            "Financial assurance compliance",
            "Timeliness of P-4 submission",
            "Verification of permit continuity",
            "Legacy liability management"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.4",
            "RRC P-4 Filing Guidelines"
        ],
        burden_holder="Outgoing and incoming operators",
        adversary_position="RRC transfer review staff",
        counter_arguments=[
            "Disputed ownership",
            "Incomplete transfer documentation",
            "Legacy liability disputes"
        ],
        resolution_strategy="Legal counsel; comprehensive transfer documentation; proactive RRC engagement.",
        entity_scope="Operators undergoing transfer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="RRC Operator Transfer Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Well Plugging W-3 and W-3A",
        keywords=["W-3", "W-3A", "well plugging", "abandonment", "RRC"],
        conclusion_template="Operators must file W-3 and W-3A reports for well plugging and abandonment, ensuring environmental and regulatory compliance.",
        reasoning_framework="""
Well plugging and abandonment is governed by W-3 and W-3A reports, which document the technical and environmental aspects of the process. Operators must ensure proper cementing, casing removal, and site restoration. The RRC reviews plugging reports to verify compliance with environmental standards and prevent groundwater contamination. The doctrine stresses the importance of technical precision, environmental stewardship, and timely reporting. Improper plugging may result in enforcement actions, environmental remediation orders, and reputational harm.
        """,
        key_factors=[
            "Technical accuracy of plugging operations",
            "Environmental compliance",
            "Timeliness of report submission",
            "Site restoration",
            "Groundwater protection"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.14",
            "RRC W-3 and W-3A Filing Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Disputed site restoration",
            "Incomplete plugging documentation",
            "Groundwater contamination allegations"
        ],
        resolution_strategy="Technical review; environmental assessment; legal counsel for disputed issues.",
        entity_scope="Operators plugging wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RRC Plugging Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Activity Scoring",
        keywords=["activity scoring", "operator performance", "benchmarking", "RRC", "metrics"],
        conclusion_template="Operator activity scoring is based on a composite of regulatory compliance, production performance, and operational efficiency metrics.",
        reasoning_framework="""
Operator activity scoring is a quantitative assessment of operator performance, combining regulatory compliance, production trends, and operational efficiency. The scoring framework utilizes RRC filings, production data, permit history, and enforcement actions. Operators are benchmarked against peers, with scores reflecting risk, reliability, and competitive positioning. The doctrine emphasizes transparency, data integrity, and methodological rigor. Scores are used for permit prioritization, investment analysis, and regulatory oversight. Disputed scores may be addressed through data reconciliation and methodological review.
        """,
        key_factors=[
            "Regulatory compliance history",
            "Production performance",
            "Operational efficiency",
            "Peer benchmarking",
            "Data integrity"
        ],
        primary_authority=[
            "RRC Operator Activity Scoring Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC scoring review staff",
        counter_arguments=[
            "Data inaccuracies",
            "Methodological bias",
            "Disputed benchmarking criteria"
        ],
        resolution_strategy="Data reconciliation; methodological transparency; third-party review.",
        entity_scope="All Texas operators",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="RRC Scoring Reviews 2020-2023"
    ),
    DoctrineBlock(
        topic="Drilling Rig Count Analysis",
        keywords=["rig count", "drilling activity", "RRC", "market trends", "analysis"],
        conclusion_template="Rig count analysis provides insight into operator activity, market trends, and resource allocation.",
        reasoning_framework="""
Drilling rig count is a key indicator of operator activity and market health. The doctrine utilizes RRC permit data, field reports, and industry surveys to track active rigs, new deployments, and retirements. Rig count trends inform resource allocation, investment decisions, and regulatory oversight. The framework emphasizes data integration, temporal analysis, and geographic segmentation. Operators use rig count analysis to benchmark activity, forecast production, and assess competitive positioning. Disputed rig counts may arise from reporting delays, data discrepancies, or ambiguous classification.
        """,
        key_factors=[
            "Active rig count",
            "New rig deployments",
            "Rig retirements",
            "Geographic segmentation",
            "Temporal trends"
        ],
        primary_authority=[
            "RRC Rig Count Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; market analysts",
        counter_arguments=[
            "Reporting delays",
            "Data discrepancies",
            "Ambiguous rig classification"
        ],
        resolution_strategy="Data reconciliation; industry survey integration; methodological review.",
        entity_scope="All Texas operators",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="RRC Rig Count Analysis 2019-2023"
    ),
    DoctrineBlock(
        topic="Permit-to-Spud Timing",
        keywords=["permit-to-spud", "timing", "drilling", "RRC", "efficiency"],
        conclusion_template="Permit-to-spud timing is a critical metric for operator efficiency and regulatory compliance.",
        reasoning_framework="""
Permit-to-spud timing measures the interval between permit approval and commencement of drilling operations. The doctrine evaluates operator efficiency, regulatory compliance, and project management. Short intervals indicate operational readiness and market responsiveness, while delays may signal logistical, regulatory, or financial challenges. The framework integrates RRC permit data, field reports, and operator disclosures. Disputed timing metrics may arise from reporting inconsistencies, ambiguous spud definitions, or administrative delays.
        """,
        key_factors=[
            "Permit approval date",
            "Spud commencement date",
            "Operational readiness",
            "Regulatory compliance",
            "Project management"
        ],
        primary_authority=[
            "RRC Permit and Spud Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC project review staff",
        counter_arguments=[
            "Reporting inconsistencies",
            "Ambiguous spud definitions",
            "Administrative delays"
        ],
        resolution_strategy="Standardized reporting; project management review; RRC clarification.",
        entity_scope="Operators commencing drilling",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="RRC Permit-to-Spud Analysis 2020-2023"
    ),
    DoctrineBlock(
        topic="Completion Success Rates",
        keywords=["completion", "success rate", "RRC", "production", "benchmarking"],
        conclusion_template="Completion success rates are determined by production performance and regulatory compliance post-completion.",
        reasoning_framework="""
Completion success rates measure the proportion of wells achieving target production post-completion. The doctrine integrates RRC completion reports, production data, and peer benchmarking. Success is defined by initial production rates, sustained output, and regulatory compliance. Operators use success rates to evaluate technical performance, investment returns, and competitive positioning. Disputed rates may arise from ambiguous success definitions, data discrepancies, or delayed reporting.
        """,
        key_factors=[
            "Initial production rates",
            "Sustained output",
            "Regulatory compliance",
            "Peer benchmarking",
            "Technical performance"
        ],
        primary_authority=[
            "RRC Completion Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC production review staff",
        counter_arguments=[
            "Ambiguous success definitions",
            "Data discrepancies",
            "Delayed reporting"
        ],
        resolution_strategy="Standardized success criteria; data reconciliation; peer review.",
        entity_scope="Operators completing wells",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="RRC Completion Success Analysis 2018-2023"
    ),
    DoctrineBlock(
        topic="Horizontal vs Vertical Well Trends",
        keywords=["horizontal well", "vertical well", "trend analysis", "RRC", "production"],
        conclusion_template="Horizontal and vertical well trends are analyzed for production performance, regulatory compliance, and market impact.",
        reasoning_framework="""
The doctrine compares horizontal and vertical well development, focusing on production performance, regulatory compliance, and market impact. Horizontal wells typically yield higher production and efficiency, but require more complex permitting and completion processes. The framework integrates RRC permit data, completion reports, and production trends. Operators use trend analysis to optimize drilling strategies, allocate resources, and benchmark performance. Disputed trend interpretations may arise from data discrepancies, ambiguous well classifications, or regulatory changes.
        """,
        key_factors=[
            "Well classification",
            "Production performance",
            "Completion complexity",
            "Regulatory compliance",
            "Market impact"
        ],
        primary_authority=[
            "RRC Well Classification Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC classification review staff",
        counter_arguments=[
            "Ambiguous well classification",
            "Data discrepancies",
            "Regulatory changes"
        ],
        resolution_strategy="Standardized classification; data reconciliation; regulatory review.",
        entity_scope="Operators drilling wells",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="RRC Horizontal vs Vertical Analysis 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Portfolio Analysis",
        keywords=["portfolio analysis", "operator assets", "RRC", "production", "benchmarking"],
        conclusion_template="Operator portfolio analysis evaluates asset diversity, production performance, and regulatory risk.",
        reasoning_framework="""
Operator portfolio analysis assesses asset diversity, production performance, and regulatory risk. The doctrine integrates RRC filings, lease data, and production reports. Operators are benchmarked on asset mix, geographic distribution, and compliance history. Portfolio analysis informs investment decisions, risk management, and competitive positioning. Disputed portfolio assessments may arise from data discrepancies, ambiguous asset classifications, or regulatory changes.
        """,
        key_factors=[
            "Asset diversity",
            "Production performance",
            "Geographic distribution",
            "Regulatory risk",
            "Compliance history"
        ],
        primary_authority=[
            "RRC Portfolio Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; market analysts",
        counter_arguments=[
            "Data discrepancies",
            "Ambiguous asset classifications",
            "Regulatory changes"
        ],
        resolution_strategy="Data reconciliation; asset classification review; regulatory consultation.",
        entity_scope="All Texas operators",
        confidence=0.86,
        confidence_zone="Moderate",
        controlling_precedent="RRC Portfolio Analysis 2018-2023"
    ),
    DoctrineBlock(
        topic="Multi-Basin Tracking",
        keywords=["multi-basin", "tracking", "operator activity", "RRC", "production"],
        conclusion_template="Multi-basin tracking enables comprehensive assessment of operator activity across geographic regions.",
        reasoning_framework="""
Multi-basin tracking evaluates operator activity across multiple geographic regions. The doctrine integrates RRC permit data, production reports, and lease information. Operators are benchmarked on basin diversity, activity levels, and compliance history. Multi-basin analysis informs resource allocation, investment decisions, and regulatory oversight. Disputed tracking metrics may arise from data discrepancies, ambiguous basin definitions, or reporting delays.
        """,
        key_factors=[
            "Basin diversity",
            "Activity levels",
            "Compliance history",
            "Resource allocation",
            "Reporting accuracy"
        ],
        primary_authority=[
            "RRC Basin Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC basin review staff",
        counter_arguments=[
            "Data discrepancies",
            "Ambiguous basin definitions",
            "Reporting delays"
        ],
        resolution_strategy="Standardized basin definitions; data reconciliation; reporting review.",
        entity_scope="Operators active in multiple basins",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="RRC Multi-Basin Tracking 2019-2023"
    ),
    DoctrineBlock(
        topic="Acreage Position Estimation",
        keywords=["acreage", "position estimation", "lease", "RRC", "operator assets"],
        conclusion_template="Acreage position estimation relies on lease data, permit filings, and production reports to assess operator asset base.",
        reasoning_framework="""
Acreage position estimation assesses operator asset base using lease data, permit filings, and production reports. The doctrine emphasizes data integration, geographic mapping, and legal review. Operators use acreage estimation to benchmark asset value, inform investment decisions, and allocate resources. Disputed acreage positions may arise from ambiguous lease boundaries, data discrepancies, or regulatory changes.
        """,
        key_factors=[
            "Lease data accuracy",
            "Permit filings",
            "Production reports",
            "Geographic mapping",
            "Legal review"
        ],
        primary_authority=[
            "RRC Lease Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC lease review staff",
        counter_arguments=[
            "Ambiguous lease boundaries",
            "Data discrepancies",
            "Regulatory changes"
        ],
        resolution_strategy="Legal review; GIS mapping; data reconciliation.",
        entity_scope="Operators with lease assets",
        confidence=0.84,
        confidence_zone="Moderate",
        controlling_precedent="RRC Acreage Estimation 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Financial Health",
        keywords=["financial health", "operator", "RRC", "bonding", "compliance"],
        conclusion_template="Operator financial health is assessed through bonding compliance, financial disclosures, and regulatory enforcement history.",
        reasoning_framework="""
Operator financial health is a critical factor in regulatory compliance and operational risk. The doctrine integrates RRC bonding requirements, financial disclosures, and enforcement history. Operators must demonstrate financial capacity to fulfill environmental and operational obligations. Financial health assessments inform permit eligibility, transfer approvals, and enforcement actions. Disputed financial health assessments may arise from incomplete disclosures, ambiguous bonding requirements, or contested enforcement history.
        """,
        key_factors=[
            "Bonding compliance",
            "Financial disclosures",
            "Enforcement history",
            "Permit eligibility",
            "Transfer approvals"
        ],
        primary_authority=[
            "RRC Bonding Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC financial review staff",
        counter_arguments=[
            "Incomplete financial disclosures",
            "Ambiguous bonding requirements",
            "Contested enforcement history"
        ],
        resolution_strategy="Comprehensive financial review; legal counsel; RRC consultation.",
        entity_scope="All Texas operators",
        confidence=0.83,
        confidence_zone="Moderate",
        controlling_precedent="RRC Financial Health Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="JV Partner Identification",
        keywords=["JV", "joint venture", "partner identification", "RRC", "operator collaboration"],
        conclusion_template="JV partner identification relies on RRC filings, production reports, and legal agreements to establish collaborative relationships.",
        reasoning_framework="""
Joint venture (JV) partner identification is based on RRC filings, production reports, and legal agreements. The doctrine emphasizes transparency, legal review, and operational alignment. Operators must disclose JV relationships, allocate production, and comply with regulatory requirements. JV identification informs asset management, risk allocation, and investment decisions. Disputed JV relationships may arise from ambiguous agreements, incomplete disclosures, or contested production allocation.
        """,
        key_factors=[
            "RRC filings",
            "Production reports",
            "Legal agreements",
            "Disclosure compliance",
            "Operational alignment"
        ],
        primary_authority=[
            "RRC JV Disclosure Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="JV partners; RRC review staff",
        counter_arguments=[
            "Ambiguous JV agreements",
            "Incomplete disclosures",
            "Contested production allocation"
        ],
        resolution_strategy="Legal review; comprehensive disclosure; RRC consultation.",
        entity_scope="Operators in JV relationships",
        confidence=0.82,
        confidence_zone="Moderate",
        controlling_precedent="RRC JV Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Frac Fleet Scheduling",
        keywords=["frac fleet", "scheduling", "completion", "RRC", "operator logistics"],
        conclusion_template="Frac fleet scheduling is optimized through permit coordination, operational planning, and regulatory compliance.",
        reasoning_framework="""
Frac fleet scheduling is a logistical process involving permit coordination, operational planning, and regulatory compliance. The doctrine integrates RRC permit data, completion schedules, and fleet availability. Operators must align frac fleet deployment with permit timelines, production targets, and environmental requirements. Scheduling optimization reduces downtime, enhances efficiency, and ensures regulatory compliance. Disputed scheduling may arise from permit delays, fleet shortages, or operational conflicts.
        """,
        key_factors=[
            "Permit coordination",
            "Operational planning",
            "Fleet availability",
            "Production targets",
            "Regulatory compliance"
        ],
        primary_authority=[
            "RRC Completion Scheduling Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC scheduling review staff",
        counter_arguments=[
            "Permit delays",
            "Fleet shortages",
            "Operational conflicts"
        ],
        resolution_strategy="Permit tracking; operational alignment; fleet management review.",
        entity_scope="Operators completing wells",
        confidence=0.81,
        confidence_zone="Moderate",
        controlling_precedent="RRC Frac Fleet Scheduling 2019-2023"
    ),
    DoctrineBlock(
        topic="Rig Release Analysis",
        keywords=["rig release", "analysis", "drilling", "RRC", "operator activity"],
        conclusion_template="Rig release analysis evaluates operator activity, project completion, and resource allocation.",
        reasoning_framework="""
Rig release analysis tracks the completion of drilling projects, operator activity, and resource allocation. The doctrine utilizes RRC permit data, field reports, and operator disclosures. Rig release metrics inform project management, operational efficiency, and market trends. Operators use rig release analysis to benchmark performance, optimize resource allocation, and forecast production. Disputed analysis may arise from reporting delays, ambiguous release definitions, or data discrepancies.
        """,
        key_factors=[
            "Project completion",
            "Operator activity",
            "Resource allocation",
            "Reporting accuracy",
            "Market trends"
        ],
        primary_authority=[
            "RRC Rig Release Reports",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC project review staff",
        counter_arguments=[
            "Reporting delays",
            "Ambiguous release definitions",
            "Data discrepancies"
        ],
        resolution_strategy="Standardized release criteria; data reconciliation; project management review.",
        entity_scope="Operators completing drilling projects",
        confidence=0.80,
        confidence_zone="Moderate",
        controlling_precedent="RRC Rig Release Analysis 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Competitive Benchmarking",
        keywords=["competitive benchmarking", "operator", "RRC", "performance", "market analysis"],
        conclusion_template="Operator competitive benchmarking utilizes RRC filings, production data, and peer analysis to evaluate market positioning.",
        reasoning_framework="""
Competitive benchmarking evaluates operator performance using RRC filings, production data, and peer analysis. The doctrine emphasizes transparency, methodological rigor, and data integrity. Operators are benchmarked on production, compliance, asset diversity, and operational efficiency. Benchmarking informs investment decisions, risk management, and regulatory oversight. Disputed benchmarking may arise from data discrepancies, methodological bias, or ambiguous criteria.
        """,
        key_factors=[
            "Production performance",
            "Compliance history",
            "Asset diversity",
            "Operational efficiency",
            "Peer analysis"
        ],
        primary_authority=[
            "RRC Benchmarking Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; market analysts",
        counter_arguments=[
            "Data discrepancies",
            "Methodological bias",
            "Ambiguous benchmarking criteria"
        ],
        resolution_strategy="Data reconciliation; methodological transparency; peer review.",
        entity_scope="All Texas operators",
        confidence=0.79,
        confidence_zone="Moderate",
        controlling_precedent="RRC Benchmarking Analysis 2019-2023"
    ),
    DoctrineBlock(
        topic="Inactive Well Management",
        keywords=["inactive well", "management", "RRC", "compliance", "environmental"],
        conclusion_template="Inactive well management requires regular reporting, site maintenance, and compliance with RRC environmental standards.",
        reasoning_framework="""
Inactive wells pose operational and environmental risks. The doctrine requires operators to regularly report inactive well status, maintain sites, and comply with RRC environmental standards. Operators must demonstrate intent to return wells to service or initiate plugging procedures. The RRC monitors inactive well inventories, enforces site maintenance, and may require financial assurance. Disputed management may arise from ambiguous inactivity definitions, reporting delays, or environmental concerns.
        """,
        key_factors=[
            "Inactive well inventory",
            "Site maintenance",
            "Reporting compliance",
            "Environmental standards",
            "Financial assurance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1, §3.15",
            "RRC Inactive Well Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Ambiguous inactivity definitions",
            "Reporting delays",
            "Environmental concerns"
        ],
        resolution_strategy="Standardized inactivity criteria; regular site inspections; environmental review.",
        entity_scope="Operators with inactive wells",
        confidence=0.78,
        confidence_zone="Moderate",
        controlling_precedent="RRC Inactive Well Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Lease Compliance Auditing",
        keywords=["lease compliance", "auditing", "RRC", "operator", "reporting"],
        conclusion_template="Lease compliance auditing ensures operators adhere to lease terms, production allocation, and regulatory requirements.",
        reasoning_framework="""
Lease compliance auditing verifies operator adherence to lease terms, production allocation, and regulatory requirements. The doctrine integrates lease agreements, production reports, and RRC filings. Audits identify discrepancies, enforce compliance, and inform regulatory actions. Operators must maintain accurate records, reconcile production, and address audit findings. Disputed audits may arise from ambiguous lease terms, data discrepancies, or contested allocation.
        """,
        key_factors=[
            "Lease agreement accuracy",
            "Production allocation",
            "Regulatory compliance",
            "Record maintenance",
            "Audit findings"
        ],
        primary_authority=[
            "RRC Lease Audit Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC audit staff",
        counter_arguments=[
            "Ambiguous lease terms",
            "Data discrepancies",
            "Contested allocation"
        ],
        resolution_strategy="Legal review; data reconciliation; audit response.",
        entity_scope="Operators with lease assets",
        confidence=0.77,
        confidence_zone="Moderate",
        controlling_precedent="RRC Lease Audits 2019-2023"
    ),
    DoctrineBlock(
        topic="Environmental Impact Reporting",
        keywords=["environmental impact", "reporting", "RRC", "operator", "compliance"],
        conclusion_template="Environmental impact reporting is mandatory for significant operational changes and must comply with RRC standards.",
        reasoning_framework="""
Operators must report environmental impacts for significant operational changes, including drilling, completion, and plugging. The doctrine integrates RRC environmental standards, site assessments, and mitigation plans. Reports must document potential impacts, mitigation measures, and compliance with regulatory requirements. The RRC reviews reports for completeness, technical accuracy, and environmental stewardship. Disputed reports may arise from incomplete documentation, ambiguous impact definitions, or contested mitigation plans.
        """,
        key_factors=[
            "Operational change documentation",
            "Site assessments",
            "Mitigation plans",
            "Regulatory compliance",
            "Technical accuracy"
        ],
        primary_authority=[
            "RRC Environmental Reporting Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous impact definitions",
            "Contested mitigation plans"
        ],
        resolution_strategy="Comprehensive reporting; site assessment review; mitigation plan consultation.",
        entity_scope="Operators undergoing operational changes",
        confidence=0.76,
        confidence_zone="Moderate",
        controlling_precedent="RRC Environmental Reporting 2018-2023"
    ),
    DoctrineBlock(
        topic="Severance Tax Compliance",
        keywords=["severance tax", "compliance", "RRC", "production", "reporting"],
        conclusion_template="Severance tax compliance requires accurate production reporting and timely tax payments.",
        reasoning_framework="""
Severance tax compliance is enforced through accurate production reporting and timely tax payments. The doctrine integrates RRC production reports, tax filings, and audit findings. Operators must reconcile production volumes, submit tax payments, and address audit discrepancies. The RRC and Texas Comptroller monitor compliance, enforce penalties, and conduct audits. Disputed compliance may arise from production discrepancies, late payments, or contested audit findings.
        """,
        key_factors=[
            "Production reporting accuracy",
            "Tax payment timeliness",
            "Audit findings",
            "Regulatory compliance",
            "Record reconciliation"
        ],
        primary_authority=[
            "Texas Comptroller Severance Tax Guidelines",
            "RRC Production Reporting Standards"
        ],
        burden_holder="Operator",
        adversary_position="Texas Comptroller; RRC audit staff",
        counter_arguments=[
            "Production discrepancies",
            "Late payments",
            "Contested audit findings"
        ],
        resolution_strategy="Production reconciliation; timely payments; audit response.",
        entity_scope="Operators of producing wells",
        confidence=0.75,
        confidence_zone="Moderate",
        controlling_precedent="Texas Comptroller Severance Tax Audits 2018-2023"
    ),
    DoctrineBlock(
        topic="Well Integrity Monitoring",
        keywords=["well integrity", "monitoring", "RRC", "operator", "compliance"],
        conclusion_template="Well integrity monitoring is required to prevent environmental hazards and ensure regulatory compliance.",
        reasoning_framework="""
Well integrity monitoring is mandated to prevent environmental hazards and ensure regulatory compliance. The doctrine integrates RRC monitoring standards, site inspections, and technical assessments. Operators must regularly inspect wells, document integrity status, and address identified risks. The RRC reviews monitoring reports, enforces corrective actions, and may require additional inspections. Disputed monitoring may arise from ambiguous integrity definitions, incomplete inspections, or contested corrective actions.
        """,
        key_factors=[
            "Inspection frequency",
            "Integrity status documentation",
            "Risk assessment",
            "Regulatory compliance",
            "Corrective actions"
        ],
        primary_authority=[
            "RRC Well Integrity Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Ambiguous integrity definitions",
            "Incomplete inspections",
            "Contested corrective actions"
        ],
        resolution_strategy="Standardized integrity criteria; comprehensive inspections; corrective action review.",
        entity_scope="Operators of active wells",
        confidence=0.74,
        confidence_zone="Moderate",
        controlling_precedent="RRC Well Integrity Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Surface Use Agreements",
        keywords=["surface use", "agreement", "RRC", "operator", "landowner"],
        conclusion_template="Surface use agreements must be documented, disclosed, and comply with RRC and landowner requirements.",
        reasoning_framework="""
Surface use agreements govern operator access, site development, and environmental stewardship. The doctrine integrates legal agreements, RRC requirements, and landowner stipulations. Operators must document agreements, disclose terms, and comply with regulatory and landowner requirements. Surface use compliance informs site development, environmental impact, and operational risk. Disputed agreements may arise from ambiguous terms, incomplete documentation, or contested site access.
        """,
        key_factors=[
            "Agreement documentation",
            "Disclosure compliance",
            "Regulatory requirements",
            "Landowner stipulations",
            "Site development"
        ],
        primary_authority=[
            "RRC Surface Use Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Landowners; RRC review staff",
        counter_arguments=[
            "Ambiguous agreement terms",
            "Incomplete documentation",
            "Contested site access"
        ],
        resolution_strategy="Legal review; comprehensive documentation; landowner consultation.",
        entity_scope="Operators with surface access",
        confidence=0.73,
        confidence_zone="Moderate",
        controlling_precedent="RRC Surface Use Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Water Use and Disposal Reporting",
        keywords=["water use", "disposal", "reporting", "RRC", "operator"],
        conclusion_template="Water use and disposal reporting is required for drilling, completion, and production operations, ensuring environmental compliance.",
        reasoning_framework="""
Operators must report water use and disposal for drilling, completion, and production operations. The doctrine integrates RRC reporting standards, site assessments, and disposal permits. Reports must document volumes, disposal methods, and compliance with environmental requirements. The RRC reviews reports for completeness, technical accuracy, and environmental stewardship. Disputed reporting may arise from incomplete documentation, ambiguous disposal methods, or contested environmental impacts.
        """,
        key_factors=[
            "Water use documentation",
            "Disposal method reporting",
            "Environmental compliance",
            "Site assessments",
            "Permit adherence"
        ],
        primary_authority=[
            "RRC Water Reporting Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous disposal methods",
            "Contested environmental impacts"
        ],
        resolution_strategy="Comprehensive reporting; site assessment review; permit consultation.",
        entity_scope="Operators using water in operations",
        confidence=0.72,
        confidence_zone="Moderate",
        controlling_precedent="RRC Water Use Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Gas Flaring Compliance",
        keywords=["gas flaring", "compliance", "RRC", "operator", "environmental"],
        conclusion_template="Gas flaring compliance requires accurate reporting, permit adherence, and minimization of environmental impacts.",
        reasoning_framework="""
Gas flaring is regulated to minimize environmental impacts and ensure compliance with RRC standards. The doctrine integrates permit requirements, reporting standards, and environmental assessments. Operators must accurately report flared volumes, adhere to permit limits, and implement minimization strategies. The RRC reviews compliance, enforces penalties, and may require corrective actions. Disputed compliance may arise from reporting discrepancies, permit ambiguities, or contested environmental impacts.
        """,
        key_factors=[
            "Flared volume reporting",
            "Permit adherence",
            "Environmental minimization",
            "Regulatory compliance",
            "Corrective actions"
        ],
        primary_authority=[
            "RRC Gas Flaring Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Reporting discrepancies",
            "Permit ambiguities",
            "Contested environmental impacts"
        ],
        resolution_strategy="Accurate reporting; permit review; environmental minimization strategies.",
        entity_scope="Operators flaring gas",
        confidence=0.71,
        confidence_zone="Moderate",
        controlling_precedent="RRC Gas Flaring Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Disclosure",
        keywords=["hydraulic fracturing", "disclosure", "RRC", "operator", "compliance"],
        conclusion_template="Hydraulic fracturing disclosure is mandatory and must comply with RRC reporting standards.",
        reasoning_framework="""
Operators must disclose hydraulic fracturing activities, including chemical use, volumes, and operational details. The doctrine integrates RRC reporting standards, site assessments, and environmental requirements. Disclosure informs regulatory oversight, public transparency, and environmental stewardship. The RRC reviews disclosures for completeness, technical accuracy, and compliance. Disputed disclosures may arise from incomplete documentation, ambiguous chemical definitions, or contested environmental impacts.
        """,
        key_factors=[
            "Chemical use disclosure",
            "Volume reporting",
            "Operational details",
            "Regulatory compliance",
            "Environmental stewardship"
        ],
        primary_authority=[
            "RRC Hydraulic Fracturing Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous chemical definitions",
            "Contested environmental impacts"
        ],
        resolution_strategy="Comprehensive disclosure; site assessment review; regulatory consultation.",
        entity_scope="Operators conducting hydraulic fracturing",
        confidence=0.70,
        confidence_zone="Moderate",
        controlling_precedent="RRC Hydraulic Fracturing Disclosure 2019-2023"
    ),
    DoctrineBlock(
        topic="Well Spacing Rule Compliance",
        keywords=["well spacing", "rule compliance", "RRC", "operator", "permit"],
        conclusion_template="Well spacing rule compliance is required for permit approval and operational integrity.",
        reasoning_framework="""
Well spacing rules govern the minimum distance between wells to prevent resource waste and ensure operational integrity. The doctrine integrates RRC permit requirements, lease boundaries, and technical assessments. Operators must comply with spacing rules for permit approval and operational planning. The RRC reviews compliance, enforces penalties, and may require corrective actions. Disputed compliance may arise from ambiguous spacing definitions, lease boundary disputes, or contested technical assessments.
        """,
        key_factors=[
            "Spacing rule adherence",
            "Lease boundary verification",
            "Technical assessment",
            "Permit approval",
            "Operational planning"
        ],
        primary_authority=[
            "RRC Well Spacing Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC permit review staff",
        counter_arguments=[
            "Ambiguous spacing definitions",
            "Lease boundary disputes",
            "Contested technical assessments"
        ],
        resolution_strategy="Legal review; technical assessment; permit consultation.",
        entity_scope="Operators seeking permits",
        confidence=0.69,
        confidence_zone="Moderate",
        controlling_precedent="RRC Well Spacing Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Production Allocation Disputes",
        keywords=["production allocation", "dispute", "RRC", "operator", "lease"],
        conclusion_template="Production allocation disputes are resolved through legal review, data reconciliation, and regulatory consultation.",
        reasoning_framework="""
Production allocation disputes arise from ambiguous lease terms, data discrepancies, and contested production volumes. The doctrine integrates lease agreements, production reports, and RRC filings. Disputes are resolved through legal review, data reconciliation, and regulatory consultation. Operators must maintain accurate records, reconcile production, and address dispute findings. The RRC may mediate disputes, enforce allocation rules, and require corrective actions.
        """,
        key_factors=[
            "Lease agreement accuracy",
            "Production volume reconciliation",
            "Regulatory compliance",
            "Record maintenance",
            "Dispute findings"
        ],
        primary_authority=[
            "RRC Production Allocation Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Peer operators; RRC dispute review staff",
        counter_arguments=[
            "Ambiguous lease terms",
            "Data discrepancies",
            "Contested production volumes"
        ],
        resolution_strategy="Legal review; data reconciliation; regulatory mediation.",
        entity_scope="Operators with production allocation disputes",
        confidence=0.68,
        confidence_zone="Moderate",
        controlling_precedent="RRC Production Allocation Dispute Resolution 2019-2023"
    ),
    DoctrineBlock(
        topic="Permit Renewal Procedures",
        keywords=["permit renewal", "procedures", "RRC", "operator", "compliance"],
        conclusion_template="Permit renewal procedures require timely submission, compliance review, and documentation of operational changes.",
        reasoning_framework="""
Permit renewal procedures are governed by RRC requirements for timely submission, compliance review, and documentation of operational changes. Operators must submit renewal applications, disclose operational updates, and address compliance findings. The RRC reviews renewals for completeness, technical accuracy, and regulatory compliance. Disputed renewals may arise from late submissions, incomplete documentation, or contested compliance findings.
        """,
        key_factors=[
            "Timely submission",
            "Operational change documentation",
            "Compliance review",
            "Technical accuracy",
            "Regulatory requirements"
        ],
        primary_authority=[
            "RRC Permit Renewal Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC permit review staff",
        counter_arguments=[
            "Late submissions",
            "Incomplete documentation",
            "Contested compliance findings"
        ],
        resolution_strategy="Timely submission; comprehensive documentation; compliance review response.",
        entity_scope="Operators renewing permits",
        confidence=0.67,
        confidence_zone="Moderate",
        controlling_precedent="RRC Permit Renewal Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Suspension and Revocation",
        keywords=["operator suspension", "revocation", "RRC", "compliance", "enforcement"],
        conclusion_template="Operator suspension and revocation are enforced for major compliance violations, subject to regulatory review and appeal.",
        reasoning_framework="""
Operator suspension and revocation are enforced for major compliance violations, including permit fraud, environmental hazards, and repeated non-compliance. The doctrine integrates RRC enforcement standards, compliance history, and regulatory review. Operators are subject to suspension or revocation following investigation, notice, and appeal procedures. The RRC enforces penalties, mediates appeals, and may require corrective actions. Disputed enforcement may arise from contested violations, procedural errors, or ambiguous compliance standards.
        """,
        key_factors=[
            "Compliance violation severity",
            "Enforcement standards",
            "Regulatory review",
            "Appeal procedures",
            "Corrective actions"
        ],
        primary_authority=[
            "RRC Enforcement Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC enforcement staff",
        counter_arguments=[
            "Contested violations",
            "Procedural errors",
            "Ambiguous compliance standards"
        ],
        resolution_strategy="Regulatory review; appeal procedures; corrective action response.",
        entity_scope="Operators with major violations",
        confidence=0.66,
        confidence_zone="Moderate",
        controlling_precedent="RRC Suspension and Revocation Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Emergency Response Planning",
        keywords=["emergency response", "planning", "RRC", "operator", "compliance"],
        conclusion_template="Emergency response planning is required for operational risk mitigation and regulatory compliance.",
        reasoning_framework="""
Emergency response planning is mandated for operational risk mitigation and regulatory compliance. The doctrine integrates RRC emergency standards, site assessments, and mitigation plans. Operators must develop response plans, conduct site assessments, and comply with regulatory requirements. The RRC reviews plans for completeness, technical accuracy, and compliance. Disputed planning may arise from incomplete documentation, ambiguous risk definitions, or contested mitigation measures.
        """,
        key_factors=[
            "Response plan development",
            "Site assessments",
            "Mitigation measures",
            "Regulatory compliance",
            "Technical accuracy"
        ],
        primary_authority=[
            "RRC Emergency Response Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC emergency review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous risk definitions",
            "Contested mitigation measures"
        ],
        resolution_strategy="Comprehensive planning; site assessment review; mitigation plan consultation.",
        entity_scope="Operators with operational risks",
        confidence=0.65,
        confidence_zone="Moderate",
        controlling_precedent="RRC Emergency Response Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Data Integrity",
        keywords=["data integrity", "operator", "RRC", "reporting", "compliance"],
        conclusion_template="Operator data integrity is essential for regulatory compliance, operational accuracy, and market transparency.",
        reasoning_framework="""
Operator data integrity is critical for regulatory compliance, operational accuracy, and market transparency. The doctrine integrates RRC reporting standards, data reconciliation procedures, and audit findings. Operators must maintain accurate records, reconcile data, and address discrepancies. The RRC reviews data integrity for compliance, enforces penalties, and may require corrective actions. Disputed integrity may arise from reporting errors, data discrepancies, or contested audit findings.
        """,
        key_factors=[
            "Record accuracy",
            "Data reconciliation",
            "Reporting standards",
            "Audit findings",
            "Regulatory compliance"
        ],
        primary_authority=[
            "RRC Data Integrity Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC audit staff",
        counter_arguments=[
            "Reporting errors",
            "Data discrepancies",
            "Contested audit findings"
        ],
        resolution_strategy="Comprehensive reconciliation; audit response; regulatory consultation.",
        entity_scope="All Texas operators",
        confidence=0.64,
        confidence_zone="Moderate",
        controlling_precedent="RRC Data Integrity Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Risk Assessment",
        keywords=["risk assessment", "operator", "RRC", "compliance", "enforcement"],
        conclusion_template="Operator risk assessment evaluates compliance history, operational hazards, and regulatory enforcement likelihood.",
        reasoning_framework="""
Operator risk assessment evaluates compliance history, operational hazards, and regulatory enforcement likelihood. The doctrine integrates RRC enforcement records, operational disclosures, and site assessments. Operators are scored on risk factors, compliance history, and operational hazards. Risk assessment informs permit eligibility, enforcement actions, and investment decisions. Disputed assessments may arise from incomplete records, ambiguous risk definitions, or contested enforcement history.
        """,
        key_factors=[
            "Compliance history",
            "Operational hazards",
            "Enforcement likelihood",
            "Permit eligibility",
            "Investment decisions"
        ],
        primary_authority=[
            "RRC Risk Assessment Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC enforcement staff",
        counter_arguments=[
            "Incomplete records",
            "Ambiguous risk definitions",
            "Contested enforcement history"
        ],
        resolution_strategy="Comprehensive record review; risk definition clarification; regulatory consultation.",
        entity_scope="All Texas operators",
        confidence=0.63,
        confidence_zone="Moderate",
        controlling_precedent="RRC Risk Assessment Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Training and Certification",
        keywords=["operator training", "certification", "RRC", "compliance", "safety"],
        conclusion_template="Operator training and certification are required for regulatory compliance and operational safety.",
        reasoning_framework="""
Operator training and certification are mandated for regulatory compliance and operational safety. The doctrine integrates RRC training standards, certification requirements, and site assessments. Operators must complete training, obtain certifications, and document compliance. The RRC reviews training records, enforces standards, and may require additional training. Disputed compliance may arise from incomplete records, ambiguous certification requirements, or contested training standards.
        """,
        key_factors=[
            "Training completion",
            "Certification requirements",
            "Record documentation",
            "Regulatory compliance",
            "Operational safety"
        ],
        primary_authority=[
            "RRC Training Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC training review staff",
        counter_arguments=[
            "Incomplete records",
            "Ambiguous certification requirements",
            "Contested training standards"
        ],
        resolution_strategy="Comprehensive training; certification review; regulatory consultation.",
        entity_scope="All Texas operators",
        confidence=0.62,
        confidence_zone="Moderate",
        controlling_precedent="RRC Training Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Reporting Automation",
        keywords=["reporting automation", "operator", "RRC", "compliance", "technology"],
        conclusion_template="Operator reporting automation enhances compliance, accuracy, and operational efficiency.",
        reasoning_framework="""
Reporting automation utilizes technology to enhance compliance, accuracy, and operational efficiency. The doctrine integrates RRC reporting standards, automation tools, and audit findings. Operators must implement automated systems, reconcile data, and address discrepancies. The RRC reviews automation for compliance, enforces standards, and may require manual review. Disputed automation may arise from system errors, data discrepancies, or contested audit findings.
        """,
        key_factors=[
            "Automation implementation",
            "Data reconciliation",
            "Reporting standards",
            "Audit findings",
            "Operational efficiency"
        ],
        primary_authority=[
            "RRC Reporting Automation Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC audit staff",
        counter_arguments=[
            "System errors",
            "Data discrepancies",
            "Contested audit findings"
        ],
        resolution_strategy="Comprehensive reconciliation; audit response; technology review.",
        entity_scope="All Texas operators",
        confidence=0.61,
        confidence_zone="Moderate",
        controlling_precedent="RRC Reporting Automation Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Stakeholder Engagement",
        keywords=["stakeholder engagement", "operator", "RRC", "community", "compliance"],
        conclusion_template="Operator stakeholder engagement is required for community relations, regulatory compliance, and operational transparency.",
        reasoning_framework="""
Stakeholder engagement is mandated for community relations, regulatory compliance, and operational transparency. The doctrine integrates RRC engagement standards, community outreach, and disclosure requirements. Operators must engage stakeholders, disclose operational plans, and address community concerns. The RRC reviews engagement for compliance, enforces standards, and may require additional outreach. Disputed engagement may arise from incomplete outreach, ambiguous disclosure requirements, or contested community concerns.
        """,
        key_factors=[
            "Community outreach",
            "Disclosure requirements",
            "Regulatory compliance",
            "Operational transparency",
            "Stakeholder concerns"
        ],
        primary_authority=[
            "RRC Stakeholder Engagement Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="Community stakeholders; RRC review staff",
        counter_arguments=[
            "Incomplete outreach",
            "Ambiguous disclosure requirements",
            "Contested community concerns"
        ],
        resolution_strategy="Comprehensive outreach; disclosure review; community consultation.",
        entity_scope="All Texas operators",
        confidence=0.60,
        confidence_zone="Moderate",
        controlling_precedent="RRC Stakeholder Engagement Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Technology Adoption",
        keywords=["technology adoption", "operator", "RRC", "compliance", "innovation"],
        conclusion_template="Operator technology adoption is encouraged for compliance, efficiency, and market competitiveness.",
        reasoning_framework="""
Technology adoption is encouraged for compliance, efficiency, and market competitiveness. The doctrine integrates RRC technology standards, operational innovation, and audit findings. Operators must adopt new technologies, document implementation, and address compliance requirements. The RRC reviews technology adoption for compliance, enforces standards, and may require additional documentation. Disputed adoption may arise from system errors, ambiguous technology standards, or contested audit findings.
        """,
        key_factors=[
            "Technology implementation",
            "Compliance requirements",
            "Operational innovation",
            "Audit findings",
            "Market competitiveness"
        ],
        primary_authority=[
            "RRC Technology Adoption Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC audit staff",
        counter_arguments=[
            "System errors",
            "Ambiguous technology standards",
            "Contested audit findings"
        ],
        resolution_strategy="Comprehensive documentation; audit response; technology review.",
        entity_scope="All Texas operators",
        confidence=0.59,
        confidence_zone="Moderate",
        controlling_precedent="RRC Technology Adoption Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Market Exit Procedures",
        keywords=["market exit", "operator", "RRC", "compliance", "asset disposition"],
        conclusion_template="Operator market exit procedures require asset disposition, regulatory compliance, and documentation of operational cessation.",
        reasoning_framework="""
Market exit procedures are governed by RRC requirements for asset disposition, regulatory compliance, and documentation of operational cessation. Operators must dispose of assets, comply with regulatory requirements, and document cessation of operations. The RRC reviews exit procedures for completeness, technical accuracy, and compliance. Disputed exits may arise from incomplete documentation, ambiguous asset disposition, or contested compliance findings.
        """,
        key_factors=[
            "Asset disposition",
            "Regulatory compliance",
            "Operational cessation documentation",
            "Technical accuracy",
            "Compliance review"
        ],
        primary_authority=[
            "RRC Market Exit Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous asset disposition",
            "Contested compliance findings"
        ],
        resolution_strategy="Comprehensive documentation; compliance review; asset disposition consultation.",
        entity_scope="Operators exiting the market",
        confidence=0.58,
        confidence_zone="Moderate",
        controlling_precedent="RRC Market Exit Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Asset Acquisition Procedures",
        keywords=["asset acquisition", "operator", "RRC", "compliance", "transfer"],
        conclusion_template="Operator asset acquisition procedures require legal review, regulatory compliance, and documentation of transfer.",
        reasoning_framework="""
Asset acquisition procedures are governed by RRC requirements for legal review, regulatory compliance, and documentation of transfer. Operators must review legal agreements, comply with regulatory requirements, and document asset transfer. The RRC reviews acquisitions for completeness, technical accuracy, and compliance. Disputed acquisitions may arise from ambiguous agreements, incomplete documentation, or contested compliance findings.
        """,
        key_factors=[
            "Legal agreement review",
            "Regulatory compliance",
            "Asset transfer documentation",
            "Technical accuracy",
            "Compliance review"
        ],
        primary_authority=[
            "RRC Asset Acquisition Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC review staff",
        counter_arguments=[
            "Ambiguous agreements",
            "Incomplete documentation",
            "Contested compliance findings"
        ],
        resolution_strategy="Legal review; comprehensive documentation; compliance consultation.",
        entity_scope="Operators acquiring assets",
        confidence=0.57,
        confidence_zone="Moderate",
        controlling_precedent="RRC Asset Acquisition Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Regulatory Appeals",
        keywords=["regulatory appeals", "operator", "RRC", "compliance", "enforcement"],
        conclusion_template="Operator regulatory appeals are governed by RRC procedures, legal review, and documentation of contested enforcement actions.",
        reasoning_framework="""
Regulatory appeals are governed by RRC procedures, legal review, and documentation of contested enforcement actions. Operators must submit appeal applications, document contested actions, and comply with procedural requirements. The RRC reviews appeals for completeness, legal accuracy, and compliance. Disputed appeals may arise from procedural errors, ambiguous enforcement actions, or contested compliance findings.
        """,
        key_factors=[
            "Appeal application submission",
            "Contested enforcement documentation",
            "Procedural compliance",
            "Legal accuracy",
            "Compliance review"
        ],
        primary_authority=[
            "RRC Regulatory Appeal Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC enforcement staff",
        counter_arguments=[
            "Procedural errors",
            "Ambiguous enforcement actions",
            "Contested compliance findings"
        ],
        resolution_strategy="Legal review; procedural compliance; appeal consultation.",
        entity_scope="Operators contesting enforcement",
        confidence=0.56,
        confidence_zone="Moderate",
        controlling_precedent="RRC Regulatory Appeal Enforcement 2019-2023"
    ),
    DoctrineBlock(
        topic="Operator Environmental Remediation",
        keywords=["environmental remediation", "operator", "RRC", "compliance", "site restoration"],
        conclusion_template="Operator environmental remediation is required for site restoration, regulatory compliance, and mitigation of environmental hazards.",
        reasoning_framework="""
Environmental remediation is mandated for site restoration, regulatory compliance, and mitigation of environmental hazards. The doctrine integrates RRC remediation standards, site assessments, and mitigation plans. Operators must restore sites, comply with regulatory requirements, and document remediation activities. The RRC reviews remediation for completeness, technical accuracy, and compliance. Disputed remediation may arise from incomplete documentation, ambiguous remediation standards, or contested environmental impacts.
        """,
        key_factors=[
            "Site restoration",
            "Regulatory compliance",
            "Remediation activity documentation",
            "Technical accuracy",
            "Mitigation plans"
        ],
        primary_authority=[
            "RRC Environmental Remediation Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC environmental review staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous remediation standards",
            "Contested environmental impacts"
        ],
        resolution_strategy="Comprehensive documentation; site assessment review; mitigation plan consultation.",
        entity_scope="Operators conducting remediation",
        confidence=0.55,
        confidence_zone="Moderate",
        controlling_precedent="RRC Environmental Remediation Enforcement 2018-2023"
    ),
    DoctrineBlock(
        topic="Operator Compliance Reporting",
        keywords=["compliance reporting", "operator", "RRC", "regulatory", "audit"],
        conclusion_template="Operator compliance reporting is required for regulatory audits, enforcement actions, and operational transparency.",
        reasoning_framework="""
Compliance reporting is mandated for regulatory audits, enforcement actions, and operational transparency. The doctrine integrates RRC reporting standards, audit procedures, and enforcement findings. Operators must submit compliance reports, reconcile data, and address audit findings. The RRC reviews reports for completeness, technical accuracy, and compliance. Disputed reporting may arise from incomplete documentation, ambiguous compliance standards, or contested audit findings.
        """,
        key_factors=[
            "Report submission",
            "Data reconciliation",
            "Audit procedures",
            "Regulatory compliance",
            "Operational transparency"
        ],
        primary_authority=[
            "RRC Compliance Reporting Guidelines",
            "Texas Administrative Code Title 16, Part 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC audit staff",
        counter_arguments=[
            "Incomplete documentation",
            "Ambiguous compliance standards",
            "Contested audit findings"
        ],
        resolution_strategy="Comprehensive reporting; audit response; regulatory consultation.",
        entity_scope="All Texas operators",
        confidence=0.54,
        confidence_zone="Moderate",
        controlling_precedent="RRC Compliance Reporting Enforcement 2019-2023"
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