from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNCERTAIN = "Uncertain"

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
        topic="SLO Definition Standards",
        keywords=["SLO", "definition", "standards", "service level objective", "criteria"],
        conclusion_template="The SLO must be defined with clear, measurable, and customer-centric criteria.",
        reasoning_framework=(
            "SLOs (Service Level Objectives) are foundational to reliability engineering. "
            "Their definition must be precise, avoiding ambiguity in measurement and interpretation. "
            "The criteria should reflect customer impact, not internal technical metrics alone. "
            "Industry standards (e.g., Google SRE, Site Reliability Engineering) dictate that SLOs "
            "should be expressed as percentages (e.g., 99.9% availability) or quantifiable thresholds (e.g., p95 latency < 200ms). "
            "The reasoning is rooted in the necessity for objective evaluation and actionable monitoring. "
            "Key factors include the target user experience, historical performance, and business risk tolerance. "
            "The SLO definition process should involve cross-functional stakeholders to ensure alignment. "
            "Ambiguity in SLOs leads to misinterpretation, ineffective alerting, and unreliable error budget calculations. "
            "The doctrine is reinforced by the Google SRE book and industry consensus. "
            "The burden of clarity lies with the service owner, while adversaries may argue for flexible or vague definitions. "
            "Counterarguments often cite evolving requirements or technical complexity, but these are addressed by periodic review and revision. "
            "Resolution is achieved by adopting standardized templates and review cycles. "
            "The entity scope is the service boundary as defined in the S07 engine configuration."
        ),
        key_factors=[
            "Customer impact",
            "Measurability",
            "Alignment with business objectives",
            "Historical data",
            "Stakeholder consensus"
        ],
        primary_authority=[
            "Google SRE Book",
            "Site Reliability Engineering Principles",
            "RFC 2119"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for flexible or vague SLO definitions",
        counter_arguments=[
            "Requirements change frequently",
            "Technical metrics are easier to measure",
            "Customer impact is hard to quantify"
        ],
        resolution_strategy="Adopt standardized SLO templates and periodic review cycles",
        entity_scope="Service boundary as defined in S07 engine configuration",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="Error Budget Calculation",
        keywords=["error budget", "calculation", "SLO", "SLI", "failure rate"],
        conclusion_template="Error budget is calculated as 1 minus the achieved SLO percentage over the evaluation window.",
        reasoning_framework=(
            "Error budget quantifies the permissible level of unreliability in a service, derived directly from the SLO. "
            "If the SLO is 99.9% availability, the error budget is 0.1%. "
            "Calculation involves measuring the actual SLI (e.g., availability, latency) over the evaluation window (typically 30 days), "
            "then subtracting the achieved percentage from the SLO target. "
            "This doctrine ensures operational flexibility, allowing teams to innovate and deploy changes without breaching reliability targets. "
            "Key factors include accurate SLI measurement, window selection, and exclusion of maintenance windows if applicable. "
            "The primary authority is Google SRE and industry best practices. "
            "The burden holder is the reliability engineering team, while adversaries may argue for stricter or more lenient budgets. "
            "Counterarguments include the risk of masking failures or incentivizing poor behavior. "
            "Resolution is achieved by transparent reporting and periodic recalibration of SLOs and error budgets. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "SLO target",
            "Actual SLI measurement",
            "Evaluation window",
            "Exclusion criteria"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for stricter or more lenient error budgets",
        counter_arguments=[
            "Error budgets incentivize risk-taking",
            "May mask underlying reliability issues",
            "Window selection can skew results"
        ],
        resolution_strategy="Transparent reporting and periodic recalibration",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 5"
    ),
    DoctrineBlock(
        topic="Burn Rate Analysis",
        keywords=["burn rate", "error budget", "SLO", "incident response", "alerting"],
        conclusion_template="Burn rate is the ratio of error budget consumed to time elapsed, used for proactive alerting.",
        reasoning_framework=(
            "Burn rate analysis enables teams to detect rapid consumption of error budgets, triggering alerts before SLO violations occur. "
            "Burn rate is calculated as (errors in window / error budget for window) / (window duration / SLO evaluation period). "
            "High burn rates indicate accelerated failure and require immediate action. "
            "Industry standards recommend multi-window burn rate tracking (e.g., 1h, 6h, 24h) to balance sensitivity and noise. "
            "Key factors include window selection, alert thresholds, and error budget policy. "
            "Primary authority is Google SRE and Prometheus SLO Alerting documentation. "
            "Burden holder is the incident response team, adversaries may argue for less aggressive alerting. "
            "Counterarguments include alert fatigue and false positives, mitigated by tuning thresholds and using composite windows. "
            "Resolution is achieved by implementing multi-window alerting and periodic threshold review. "
            "Entity scope is the monitored service in S07_slo_monitor."
        ),
        key_factors=[
            "Window selection",
            "Alert thresholds",
            "Error budget policy",
            "Incident response readiness"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus SLO Alerting",
            "Site Reliability Engineering Principles"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Advocates for less aggressive alerting",
        counter_arguments=[
            "Alert fatigue",
            "False positives",
            "Operational overhead"
        ],
        resolution_strategy="Multi-window alerting and periodic threshold review",
        entity_scope="Monitored service in S07_slo_monitor",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Prometheus SLO Alerting"
    ),
    DoctrineBlock(
        topic="Latency Percentile Tracking (p50, p95, p99)",
        keywords=["latency", "percentile", "p50", "p95", "p99", "performance", "SLI"],
        conclusion_template="Track latency at p50, p95, and p99 to capture typical and worst-case user experience.",
        reasoning_framework=(
            "Latency percentiles provide a comprehensive view of service performance. "
            "p50 reflects median latency, p95 captures tail latency affecting most users, and p99 highlights extreme cases. "
            "Tracking all three enables balanced optimization and prevents tail latency from degrading user experience. "
            "Key factors include accurate percentile calculation, exclusion of outliers, and alignment with user expectations. "
            "Primary authority is Google SRE, Amazon Performance Engineering, and industry consensus. "
            "Burden holder is the performance engineering team, adversaries may argue for average latency tracking only. "
            "Counterarguments include increased complexity and resource consumption, mitigated by efficient histogram storage and sampling. "
            "Resolution is achieved by adopting percentile-based SLIs and optimizing monitoring infrastructure. "
            "Entity scope is the service endpoints monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Percentile calculation accuracy",
            "User impact",
            "Outlier exclusion",
            "Monitoring efficiency"
        ],
        primary_authority=[
            "Google SRE Book",
            "Amazon Performance Engineering",
            "Industry Consensus"
        ],
        burden_holder="Performance Engineering Team",
        adversary_position="Advocates for average latency tracking only",
        counter_arguments=[
            "Complexity",
            "Resource consumption",
            "Difficult interpretation"
        ],
        resolution_strategy="Percentile-based SLIs and optimized monitoring",
        entity_scope="Service endpoints monitored by S07_slo_monitor",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 6"
    ),
    DoctrineBlock(
        topic="Throughput SLI Measurement",
        keywords=["throughput", "SLI", "requests per second", "performance", "capacity"],
        conclusion_template="Throughput SLI is measured as the number of successful requests per second over the evaluation window.",
        reasoning_framework=(
            "Throughput is a critical SLI reflecting the service's ability to handle load. "
            "Measurement involves counting successful requests per second, excluding failed or retried requests. "
            "Key factors include accurate request counting, exclusion criteria, and window selection. "
            "Primary authority is Google SRE, Netflix Performance Engineering, and industry standards. "
            "Burden holder is the capacity planning team, adversaries may argue for inclusion of retried requests. "
            "Counterarguments include potential inflation of throughput metrics, mitigated by strict exclusion policies. "
            "Resolution is achieved by adopting standardized throughput measurement and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Accurate request counting",
            "Exclusion of failed/retried requests",
            "Window selection",
            "Capacity planning"
        ],
        primary_authority=[
            "Google SRE Book",
            "Netflix Performance Engineering",
            "Industry Standards"
        ],
        burden_holder="Capacity Planning Team",
        adversary_position="Advocates for inclusion of retried requests",
        counter_arguments=[
            "Inflation of throughput metrics",
            "Difficulty in distinguishing retries",
            "Potential for misinterpretation"
        ],
        resolution_strategy="Standardized throughput measurement and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Netflix Performance Engineering"
    ),
    DoctrineBlock(
        topic="Availability Calculation",
        keywords=["availability", "calculation", "SLI", "uptime", "downtime"],
        conclusion_template="Availability is calculated as (successful requests / total requests) over the evaluation window.",
        reasoning_framework=(
            "Availability is a fundamental SLI, representing the proportion of successful requests. "
            "Calculation involves dividing the number of successful requests by the total requests, including failures. "
            "Key factors include accurate request classification, window selection, and exclusion of maintenance periods. "
            "Primary authority is Google SRE, NIST, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for exclusion of certain failures. "
            "Counterarguments include potential inflation of availability, mitigated by transparent reporting and strict classification. "
            "Resolution is achieved by adopting standardized availability calculation and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Accurate request classification",
            "Window selection",
            "Exclusion of maintenance periods",
            "Transparent reporting"
        ],
        primary_authority=[
            "Google SRE Book",
            "NIST",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for exclusion of certain failures",
        counter_arguments=[
            "Inflation of availability",
            "Difficulty in classification",
            "Potential for misinterpretation"
        ],
        resolution_strategy="Standardized availability calculation and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 7"
    ),
    DoctrineBlock(
        topic="SLO Violation Alerting",
        keywords=["SLO", "violation", "alerting", "incident response", "monitoring"],
        conclusion_template="Alerting must be triggered when SLO violation is imminent or has occurred, using multi-window burn rate analysis.",
        reasoning_framework=(
            "SLO violation alerting is essential for proactive incident response. "
            "Alerts should be triggered based on burn rate analysis, considering both short-term and long-term windows. "
            "Key factors include alert thresholds, window selection, and integration with incident management systems. "
            "Primary authority is Google SRE, Prometheus Alerting, and industry standards. "
            "Burden holder is the monitoring team, adversaries may argue for less frequent alerting to reduce noise. "
            "Counterarguments include risk of delayed response, mitigated by tuning thresholds and using composite windows. "
            "Resolution is achieved by implementing multi-window alerting and periodic threshold review. "
            "Entity scope is the monitored service in S07_slo_monitor."
        ),
        key_factors=[
            "Alert thresholds",
            "Window selection",
            "Incident management integration",
            "Noise reduction"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus Alerting",
            "Industry Standards"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for less frequent alerting",
        counter_arguments=[
            "Alert fatigue",
            "False positives",
            "Operational overhead"
        ],
        resolution_strategy="Multi-window alerting and periodic threshold review",
        entity_scope="Monitored service in S07_slo_monitor",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Prometheus Alerting"
    ),
    DoctrineBlock(
        topic="Error Budget Exhaustion Prediction",
        keywords=["error budget", "exhaustion", "prediction", "forecasting", "SLO"],
        conclusion_template="Predict error budget exhaustion using historical burn rate and trend analysis.",
        reasoning_framework=(
            "Predicting error budget exhaustion enables proactive mitigation of reliability risks. "
            "Forecasting involves analyzing historical burn rate, identifying trends, and projecting future consumption. "
            "Key factors include data quality, trend analysis, and integration with incident response planning. "
            "Primary authority is Google SRE, Data Science for Reliability, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for reactive response only. "
            "Counterarguments include prediction uncertainty, mitigated by using confidence intervals and scenario analysis. "
            "Resolution is achieved by integrating predictive analytics with monitoring and incident response workflows. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Historical burn rate data",
            "Trend analysis",
            "Forecasting accuracy",
            "Incident response planning"
        ],
        primary_authority=[
            "Google SRE Book",
            "Data Science for Reliability",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for reactive response only",
        counter_arguments=[
            "Prediction uncertainty",
            "Resource consumption",
            "Potential for false positives"
        ],
        resolution_strategy="Integrate predictive analytics with monitoring and incident response",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Data Science for Reliability"
    ),
    DoctrineBlock(
        topic="Multi-Window SLO Rolling",
        keywords=["multi-window", "SLO", "rolling", "evaluation", "burn rate"],
        conclusion_template="Evaluate SLO compliance using multiple rolling windows to balance sensitivity and noise.",
        reasoning_framework=(
            "Multi-window SLO rolling enables balanced detection of reliability issues. "
            "Short windows (e.g., 1h) provide rapid detection, while long windows (e.g., 30d) ensure stability. "
            "Combining windows prevents alert fatigue and missed incidents. "
            "Key factors include window selection, threshold tuning, and integration with alerting systems. "
            "Primary authority is Google SRE, Prometheus SLO Alerting, and industry standards. "
            "Burden holder is the monitoring team, adversaries may argue for single-window evaluation. "
            "Counterarguments include increased complexity, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting multi-window evaluation and periodic review. "
            "Entity scope is the monitored service in S07_slo_monitor."
        ),
        key_factors=[
            "Window selection",
            "Threshold tuning",
            "Alerting integration",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus SLO Alerting",
            "Industry Standards"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for single-window evaluation",
        counter_arguments=[
            "Complexity",
            "Resource consumption",
            "Difficult interpretation"
        ],
        resolution_strategy="Multi-window evaluation and periodic review",
        entity_scope="Monitored service in S07_slo_monitor",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Prometheus SLO Alerting"
    ),
    DoctrineBlock(
        topic="Composite SLO from Multiple SLIs",
        keywords=["composite SLO", "multiple SLIs", "aggregation", "service reliability"],
        conclusion_template="Composite SLO is calculated by aggregating multiple SLIs using weighted or logical operators.",
        reasoning_framework=(
            "Composite SLOs provide a holistic view of service reliability by combining multiple SLIs (e.g., latency, availability, throughput). "
            "Aggregation can be achieved through weighted averages or logical AND/OR operators. "
            "Key factors include SLI selection, weighting, and aggregation method. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for single SLI SLOs. "
            "Counterarguments include increased complexity and potential for masking failures, mitigated by transparent weighting and periodic review. "
            "Resolution is achieved by adopting composite SLO templates and stakeholder consensus. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "SLI selection",
            "Weighting",
            "Aggregation method",
            "Stakeholder consensus"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for single SLI SLOs",
        counter_arguments=[
            "Complexity",
            "Potential for masking failures",
            "Difficult interpretation"
        ],
        resolution_strategy="Composite SLO templates and stakeholder consensus",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 8"
    ),
    DoctrineBlock(
        topic="Composite",
        keywords=["composite", "aggregation", "multi-SLI", "service reliability"],
        conclusion_template="Composite doctrine refers to the aggregation of multiple reliability doctrines for holistic evaluation.",
        reasoning_framework=(
            "Composite doctrine is the principle of combining multiple reliability doctrines (e.g., SLO, error budget, burn rate) "
            "to achieve a comprehensive evaluation of service health. "
            "This approach ensures that no single metric dominates decision-making, reducing risk of blind spots. "
            "Key factors include doctrine selection, aggregation method, and stakeholder alignment. "
            "Primary authority is Google SRE, SRE Workbook, and industry consensus. "
            "Burden holder is the reliability engineering team, adversaries may argue for simplicity. "
            "Counterarguments include increased complexity and resource consumption, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting composite doctrine frameworks and periodic review. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Doctrine selection",
            "Aggregation method",
            "Stakeholder alignment",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Consensus"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for simplicity",
        counter_arguments=[
            "Complexity",
            "Resource consumption",
            "Difficult interpretation"
        ],
        resolution_strategy="Composite doctrine frameworks and periodic review",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 9"
    ),
    DoctrineBlock(
        topic="SLI Selection Criteria",
        keywords=["SLI", "selection", "criteria", "reliability", "measurement"],
        conclusion_template="SLIs must be selected based on customer impact, measurability, and alignment with business objectives.",
        reasoning_framework=(
            "SLI (Service Level Indicator) selection is critical for meaningful SLOs. "
            "Indicators should reflect customer experience, be objectively measurable, and align with business goals. "
            "Key factors include impact analysis, historical data, and stakeholder input. "
            "Primary authority is Google SRE, SRE Workbook, and industry standards. "
            "Burden holder is the reliability engineering team, adversaries may argue for technical metrics only. "
            "Counterarguments include ease of measurement, mitigated by balancing technical and customer-centric indicators. "
            "Resolution is achieved by stakeholder consensus and periodic review. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Customer impact",
            "Measurability",
            "Business alignment",
            "Historical data"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Standards"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for technical metrics only",
        counter_arguments=[
            "Ease of measurement",
            "Technical complexity",
            "Customer impact is hard to quantify"
        ],
        resolution_strategy="Stakeholder consensus and periodic review",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLI Measurement Accuracy",
        keywords=["SLI", "measurement", "accuracy", "monitoring", "data quality"],
        conclusion_template="SLI measurement must be accurate, reproducible, and auditable.",
        reasoning_framework=(
            "Accurate SLI measurement is essential for reliable SLO evaluation. "
            "Measurements should be reproducible and auditable, with clear documentation of methodology. "
            "Key factors include instrumentation quality, data integrity, and exclusion criteria. "
            "Primary authority is Google SRE, NIST, and industry best practices. "
            "Burden holder is the monitoring team, adversaries may argue for relaxed measurement standards. "
            "Counterarguments include resource constraints, mitigated by prioritizing critical SLIs and automation. "
            "Resolution is achieved by adopting standardized measurement protocols and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Instrumentation quality",
            "Data integrity",
            "Exclusion criteria",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "NIST",
            "Industry Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for relaxed measurement standards",
        counter_arguments=[
            "Resource constraints",
            "Measurement complexity",
            "Operational overhead"
        ],
        resolution_strategy="Standardized measurement protocols and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST Measurement Standards"
    ),
    DoctrineBlock(
        topic="SLO Review Cycle",
        keywords=["SLO", "review", "cycle", "iteration", "stakeholder"],
        conclusion_template="SLOs must be reviewed periodically with cross-functional stakeholder input.",
        reasoning_framework=(
            "Periodic SLO review ensures continued relevance and alignment with business objectives. "
            "Review cycles should involve cross-functional stakeholders, including engineering, product, and customer support. "
            "Key factors include review frequency, stakeholder engagement, and documentation. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for static SLOs. "
            "Counterarguments include operational overhead, mitigated by automation and streamlined review processes. "
            "Resolution is achieved by adopting standardized review templates and scheduling. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Review frequency",
            "Stakeholder engagement",
            "Documentation",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for static SLOs",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in stakeholder engagement",
            "Potential for review fatigue"
        ],
        resolution_strategy="Standardized review templates and scheduling",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="Incident Response Integration",
        keywords=["incident response", "integration", "SLO", "alerting", "monitoring"],
        conclusion_template="Incident response must be integrated with SLO alerting for rapid mitigation.",
        reasoning_framework=(
            "Integrating incident response with SLO alerting enables rapid mitigation of reliability issues. "
            "Alerts should trigger automated incident workflows, including escalation and communication. "
            "Key factors include integration quality, automation, and stakeholder training. "
            "Primary authority is Google SRE, PagerDuty, and industry standards. "
            "Burden holder is the incident response team, adversaries may argue for manual response. "
            "Counterarguments include operational overhead, mitigated by automation and training. "
            "Resolution is achieved by adopting integrated incident response frameworks and periodic drills. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Integration quality",
            "Automation",
            "Stakeholder training",
            "Incident escalation"
        ],
        primary_authority=[
            "Google SRE Book",
            "PagerDuty",
            "Industry Standards"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Advocates for manual response",
        counter_arguments=[
            "Operational overhead",
            "Training complexity",
            "Potential for false positives"
        ],
        resolution_strategy="Integrated incident response frameworks and periodic drills",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Incident Response"
    ),
    DoctrineBlock(
        topic="SLO Communication",
        keywords=["SLO", "communication", "stakeholder", "transparency", "reporting"],
        conclusion_template="SLOs and error budgets must be communicated transparently to all stakeholders.",
        reasoning_framework=(
            "Transparent communication of SLOs and error budgets ensures stakeholder alignment and informed decision-making. "
            "Reporting should include current status, historical trends, and upcoming risks. "
            "Key factors include communication frequency, format, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for limited communication. "
            "Counterarguments include operational overhead, mitigated by automation and standardized reporting templates. "
            "Resolution is achieved by adopting transparent communication frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Communication frequency",
            "Reporting format",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for limited communication",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in stakeholder engagement",
            "Potential for information overload"
        ],
        resolution_strategy="Transparent communication frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLI Instrumentation",
        keywords=["SLI", "instrumentation", "monitoring", "data collection", "accuracy"],
        conclusion_template="SLI instrumentation must be robust, accurate, and minimally invasive.",
        reasoning_framework=(
            "Robust SLI instrumentation ensures accurate data collection without impacting service performance. "
            "Instrumentation should be minimally invasive, avoiding latency or resource consumption. "
            "Key factors include instrumentation quality, data integrity, and exclusion criteria. "
            "Primary authority is Google SRE, NIST, and industry best practices. "
            "Burden holder is the monitoring team, adversaries may argue for relaxed instrumentation standards. "
            "Counterarguments include resource constraints, mitigated by prioritizing critical SLIs and automation. "
            "Resolution is achieved by adopting standardized instrumentation protocols and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Instrumentation quality",
            "Data integrity",
            "Exclusion criteria",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "NIST",
            "Industry Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for relaxed instrumentation standards",
        counter_arguments=[
            "Resource constraints",
            "Instrumentation complexity",
            "Operational overhead"
        ],
        resolution_strategy="Standardized instrumentation protocols and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST Instrumentation Standards"
    ),
    DoctrineBlock(
        topic="SLO Exception Handling",
        keywords=["SLO", "exception", "handling", "maintenance", "downtime"],
        conclusion_template="SLO exceptions must be documented, justified, and approved by stakeholders.",
        reasoning_framework=(
            "SLO exceptions (e.g., maintenance, planned downtime) must be clearly documented and justified. "
            "Approval from stakeholders is required to ensure transparency and accountability. "
            "Key factors include exception documentation, justification, and stakeholder approval. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for unapproved exceptions. "
            "Counterarguments include operational flexibility, mitigated by strict approval processes. "
            "Resolution is achieved by adopting standardized exception handling frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Exception documentation",
            "Justification",
            "Stakeholder approval",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for unapproved exceptions",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Standardized exception handling frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Enforcement Policy",
        keywords=["SLO", "enforcement", "policy", "compliance", "governance"],
        conclusion_template="SLO enforcement must be governed by documented policy with clear consequences for violations.",
        reasoning_framework=(
            "SLO enforcement ensures compliance and accountability. "
            "Policy must be documented, specifying consequences for violations and escalation procedures. "
            "Key factors include policy documentation, consequence clarity, and stakeholder communication. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for flexible enforcement. "
            "Counterarguments include operational flexibility, mitigated by periodic policy review and stakeholder input. "
            "Resolution is achieved by adopting standardized enforcement policies and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Policy documentation",
            "Consequence clarity",
            "Stakeholder communication",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for flexible enforcement",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Standardized enforcement policies and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Escalation Procedure",
        keywords=["SLO", "escalation", "procedure", "incident response", "governance"],
        conclusion_template="SLO violations must trigger documented escalation procedures involving relevant stakeholders.",
        reasoning_framework=(
            "Escalation procedures ensure rapid response to SLO violations. "
            "Documentation must specify escalation paths, communication protocols, and stakeholder involvement. "
            "Key factors include procedure documentation, escalation path clarity, and stakeholder training. "
            "Primary authority is Google SRE, PagerDuty, and industry standards. "
            "Burden holder is the incident response team, adversaries may argue for ad-hoc escalation. "
            "Counterarguments include operational flexibility, mitigated by periodic procedure review and training. "
            "Resolution is achieved by adopting standardized escalation procedures and periodic drills. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Procedure documentation",
            "Escalation path clarity",
            "Stakeholder training",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "PagerDuty",
            "Industry Standards"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Advocates for ad-hoc escalation",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for confusion"
        ],
        resolution_strategy="Standardized escalation procedures and periodic drills",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Escalation Procedures"
    ),
    DoctrineBlock(
        topic="SLO Audit Trail",
        keywords=["SLO", "audit trail", "documentation", "compliance", "governance"],
        conclusion_template="All SLO-related actions must be documented in an audit trail for compliance and review.",
        reasoning_framework=(
            "Audit trails ensure accountability and compliance in SLO management. "
            "Documentation must include SLO changes, exceptions, violations, and reviews. "
            "Key factors include audit trail completeness, accessibility, and periodic review. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal documentation. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting audit trail frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Audit trail completeness",
            "Accessibility",
            "Periodic review",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal documentation",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Audit trail frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLI Exclusion Criteria",
        keywords=["SLI", "exclusion", "criteria", "maintenance", "downtime"],
        conclusion_template="SLI measurements must exclude planned maintenance and justified exceptions.",
        reasoning_framework=(
            "Exclusion criteria ensure accurate SLI measurement by removing periods of planned maintenance and justified exceptions. "
            "Documentation and stakeholder approval are required for exclusions. "
            "Key factors include exclusion documentation, justification, and stakeholder approval. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the monitoring team, adversaries may argue for inclusion of all periods. "
            "Counterarguments include operational flexibility, mitigated by strict approval processes. "
            "Resolution is achieved by adopting standardized exclusion criteria and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Exclusion documentation",
            "Justification",
            "Stakeholder approval",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for inclusion of all periods",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Standardized exclusion criteria and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Stakeholder Engagement",
        keywords=["SLO", "stakeholder", "engagement", "review", "communication"],
        conclusion_template="Stakeholder engagement is required for SLO definition, review, and enforcement.",
        reasoning_framework=(
            "Stakeholder engagement ensures SLOs are relevant, actionable, and aligned with business objectives. "
            "Engagement includes definition, review, enforcement, and communication. "
            "Key factors include stakeholder identification, engagement frequency, and documentation. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal engagement. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting stakeholder engagement frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Stakeholder identification",
            "Engagement frequency",
            "Documentation",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal engagement",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in stakeholder engagement",
            "Potential for review fatigue"
        ],
        resolution_strategy="Stakeholder engagement frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLI Aggregation Method",
        keywords=["SLI", "aggregation", "method", "composite SLO", "weighted average"],
        conclusion_template="SLI aggregation must use documented methods, including weighted averages or logical operators.",
        reasoning_framework=(
            "SLI aggregation enables composite SLOs by combining multiple indicators. "
            "Methods include weighted averages and logical AND/OR operators. "
            "Documentation and stakeholder consensus are required for aggregation methods. "
            "Key factors include method documentation, weighting, and stakeholder approval. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for ad-hoc aggregation. "
            "Counterarguments include operational flexibility, mitigated by standardized aggregation frameworks. "
            "Resolution is achieved by adopting documented aggregation methods and periodic review. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Method documentation",
            "Weighting",
            "Stakeholder approval",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for ad-hoc aggregation",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for masking failures"
        ],
        resolution_strategy="Documented aggregation methods and periodic review",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 8"
    ),
    DoctrineBlock(
        topic="SLO Trend Analysis",
        keywords=["SLO", "trend", "analysis", "forecasting", "historical data"],
        conclusion_template="SLO trend analysis must use historical data to forecast future reliability risks.",
        reasoning_framework=(
            "Trend analysis enables proactive identification of reliability risks. "
            "Analysis uses historical SLO data, burn rate, and incident history to forecast future risks. "
            "Key factors include data quality, forecasting accuracy, and integration with incident response planning. "
            "Primary authority is Google SRE, Data Science for Reliability, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for reactive response only. "
            "Counterarguments include prediction uncertainty, mitigated by confidence intervals and scenario analysis. "
            "Resolution is achieved by integrating trend analysis with monitoring and incident response workflows. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Historical SLO data",
            "Forecasting accuracy",
            "Incident response planning",
            "Data quality"
        ],
        primary_authority=[
            "Google SRE Book",
            "Data Science for Reliability",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for reactive response only",
        counter_arguments=[
            "Prediction uncertainty",
            "Resource consumption",
            "Potential for false positives"
        ],
        resolution_strategy="Integrate trend analysis with monitoring and incident response",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Data Science for Reliability"
    ),
    DoctrineBlock(
        topic="SLO Risk Assessment",
        keywords=["SLO", "risk", "assessment", "business impact", "stakeholder"],
        conclusion_template="SLO risk assessment must evaluate business impact, customer experience, and operational risk.",
        reasoning_framework=(
            "Risk assessment ensures SLOs are aligned with business impact and operational risk. "
            "Assessment includes customer experience, incident history, and business objectives. "
            "Key factors include impact analysis, historical data, and stakeholder input. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for technical risk only. "
            "Counterarguments include ease of measurement, mitigated by balancing technical and business risk indicators. "
            "Resolution is achieved by stakeholder consensus and periodic review. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Impact analysis",
            "Historical data",
            "Stakeholder input",
            "Business objectives"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for technical risk only",
        counter_arguments=[
            "Ease of measurement",
            "Technical complexity",
            "Business impact is hard to quantify"
        ],
        resolution_strategy="Stakeholder consensus and periodic review",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Policy Documentation",
        keywords=["SLO", "policy", "documentation", "governance", "compliance"],
        conclusion_template="SLO policies must be documented, accessible, and reviewed periodically.",
        reasoning_framework=(
            "Policy documentation ensures compliance and accountability in SLO management. "
            "Documentation must be accessible to all stakeholders and reviewed periodically. "
            "Key factors include policy completeness, accessibility, and review frequency. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal documentation. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting policy documentation frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Policy completeness",
            "Accessibility",
            "Review frequency",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal documentation",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Policy documentation frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Automation",
        keywords=["SLO", "automation", "monitoring", "incident response", "review"],
        conclusion_template="SLO monitoring, alerting, and review must be automated to reduce operational overhead.",
        reasoning_framework=(
            "Automation reduces operational overhead and ensures timely response to reliability issues. "
            "Monitoring, alerting, and review processes should be automated using standardized frameworks. "
            "Key factors include automation quality, integration, and stakeholder training. "
            "Primary authority is Google SRE, Prometheus, and industry best practices. "
            "Burden holder is the monitoring team, adversaries may argue for manual processes. "
            "Counterarguments include operational flexibility, mitigated by periodic automation review and stakeholder input. "
            "Resolution is achieved by adopting automation frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Automation quality",
            "Integration",
            "Stakeholder training",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus",
            "Industry Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for manual processes",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in automation",
            "Potential for false positives"
        ],
        resolution_strategy="Automation frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Prometheus Automation"
    ),
    DoctrineBlock(
        topic="SLO Continuous Improvement",
        keywords=["SLO", "continuous improvement", "review", "stakeholder", "iteration"],
        conclusion_template="SLOs must be continuously improved based on feedback, incident history, and business objectives.",
        reasoning_framework=(
            "Continuous improvement ensures SLOs remain relevant and actionable. "
            "Improvement is based on stakeholder feedback, incident history, and evolving business objectives. "
            "Key factors include feedback collection, incident analysis, and review frequency. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for static SLOs. "
            "Counterarguments include operational overhead, mitigated by automation and streamlined review processes. "
            "Resolution is achieved by adopting continuous improvement frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Feedback collection",
            "Incident analysis",
            "Review frequency",
            "Business objectives"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for static SLOs",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in stakeholder engagement",
            "Potential for review fatigue"
        ],
        resolution_strategy="Continuous improvement frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Scalability",
        keywords=["SLO", "scalability", "monitoring", "performance", "capacity"],
        conclusion_template="SLO monitoring and enforcement must scale with service growth and complexity.",
        reasoning_framework=(
            "Scalability ensures SLO monitoring and enforcement remain effective as services grow. "
            "Monitoring infrastructure and enforcement policies must scale with service complexity and capacity. "
            "Key factors include infrastructure scalability, policy adaptability, and stakeholder training. "
            "Primary authority is Google SRE, Netflix Performance Engineering, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for static monitoring. "
            "Counterarguments include operational overhead, mitigated by automation and scalable frameworks. "
            "Resolution is achieved by adopting scalable monitoring and enforcement frameworks. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Infrastructure scalability",
            "Policy adaptability",
            "Stakeholder training",
            "Capacity planning"
        ],
        primary_authority=[
            "Google SRE Book",
            "Netflix Performance Engineering",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for static monitoring",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in scalability",
            "Potential for resource exhaustion"
        ],
        resolution_strategy="Scalable monitoring and enforcement frameworks",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Netflix Performance Engineering"
    ),
    DoctrineBlock(
        topic="SLO Portability",
        keywords=["SLO", "portability", "service migration", "monitoring", "adaptation"],
        conclusion_template="SLOs must be portable across service boundaries and adaptable to migration scenarios.",
        reasoning_framework=(
            "Portability ensures SLOs remain relevant during service migration and boundary changes. "
            "SLOs must be adaptable to new environments, with clear documentation and stakeholder approval. "
            "Key factors include portability documentation, adaptation process, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for static SLOs. "
            "Counterarguments include operational overhead, mitigated by automation and standardized adaptation frameworks. "
            "Resolution is achieved by adopting portability frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Portability documentation",
            "Adaptation process",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for static SLOs",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in adaptation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Portability frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Security Integration",
        keywords=["SLO", "security", "integration", "monitoring", "incident response"],
        conclusion_template="SLO monitoring must integrate security indicators and incident response workflows.",
        reasoning_framework=(
            "Security integration ensures SLO monitoring includes security indicators and incident response workflows. "
            "Integration enables rapid detection and mitigation of security incidents impacting reliability. "
            "Key factors include security indicator selection, integration quality, and stakeholder training. "
            "Primary authority is Google SRE, NIST, and industry best practices. "
            "Burden holder is the security team, adversaries may argue for separate monitoring. "
            "Counterarguments include operational overhead, mitigated by automation and integrated frameworks. "
            "Resolution is achieved by adopting integrated security monitoring and incident response frameworks. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Security indicator selection",
            "Integration quality",
            "Stakeholder training",
            "Incident response planning"
        ],
        primary_authority=[
            "Google SRE Book",
            "NIST",
            "Industry Best Practices"
        ],
        burden_holder="Security Team",
        adversary_position="Advocates for separate monitoring",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in integration",
            "Potential for false positives"
        ],
        resolution_strategy="Integrated security monitoring and incident response frameworks",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST Security Integration"
    ),
    DoctrineBlock(
        topic="SLO Data Retention",
        keywords=["SLO", "data retention", "historical data", "compliance", "audit"],
        conclusion_template="SLO data must be retained for compliance, audit, and trend analysis purposes.",
        reasoning_framework=(
            "Data retention ensures compliance, auditability, and enables trend analysis. "
            "Retention policies must specify duration, accessibility, and review frequency. "
            "Key factors include retention policy documentation, accessibility, and periodic review. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal retention. "
            "Counterarguments include operational overhead, mitigated by automation and standardized retention frameworks. "
            "Resolution is achieved by adopting data retention policies and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Retention policy documentation",
            "Accessibility",
            "Periodic review",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal retention",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Data retention policies and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Data Privacy",
        keywords=["SLO", "data privacy", "compliance", "monitoring", "audit"],
        conclusion_template="SLO monitoring must comply with data privacy regulations and stakeholder requirements.",
        reasoning_framework=(
            "Data privacy ensures SLO monitoring complies with regulations and stakeholder requirements. "
            "Monitoring must avoid collection of sensitive data and document privacy policies. "
            "Key factors include privacy policy documentation, compliance, and stakeholder approval. "
            "Primary authority is Google SRE, GDPR, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for relaxed privacy standards. "
            "Counterarguments include operational flexibility, mitigated by strict privacy policies and periodic audits. "
            "Resolution is achieved by adopting privacy frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Privacy policy documentation",
            "Compliance",
            "Stakeholder approval",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "GDPR",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for relaxed privacy standards",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Privacy frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GDPR Compliance"
    ),
    DoctrineBlock(
        topic="SLO Documentation Accessibility",
        keywords=["SLO", "documentation", "accessibility", "stakeholder", "review"],
        conclusion_template="SLO documentation must be accessible to all stakeholders for review and compliance.",
        reasoning_framework=(
            "Accessibility ensures SLO documentation is available to all stakeholders for review and compliance. "
            "Documentation must be stored in accessible locations and reviewed periodically. "
            "Key factors include accessibility, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for limited accessibility. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting accessibility frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Accessibility",
            "Review frequency",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for limited accessibility",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Accessibility frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Change Management",
        keywords=["SLO", "change management", "review", "documentation", "stakeholder"],
        conclusion_template="SLO changes must be managed through documented change management processes.",
        reasoning_framework=(
            "Change management ensures SLO changes are documented, reviewed, and approved by stakeholders. "
            "Processes must specify change documentation, review frequency, and stakeholder approval. "
            "Key factors include change documentation, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for ad-hoc changes. "
            "Counterarguments include operational flexibility, mitigated by standardized change management frameworks. "
            "Resolution is achieved by adopting change management frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Change documentation",
            "Review frequency",
            "Stakeholder engagement",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for ad-hoc changes",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Change management frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Incident Analysis",
        keywords=["SLO", "incident analysis", "review", "stakeholder", "trend"],
        conclusion_template="SLO incidents must be analyzed for root cause, trend, and improvement opportunities.",
        reasoning_framework=(
            "Incident analysis ensures SLO incidents are reviewed for root cause, trend, and improvement opportunities. "
            "Analysis must be documented and shared with stakeholders. "
            "Key factors include analysis documentation, trend identification, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the incident response team, adversaries may argue for minimal analysis. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting incident analysis frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Analysis documentation",
            "Trend identification",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Advocates for minimal analysis",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Incident analysis frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Service Boundary Definition",
        keywords=["SLO", "service boundary", "definition", "monitoring", "scope"],
        conclusion_template="SLOs must be defined within clear service boundaries for accurate monitoring and enforcement.",
        reasoning_framework=(
            "Service boundary definition ensures SLOs are relevant and actionable. "
            "Boundaries must be documented, reviewed, and approved by stakeholders. "
            "Key factors include boundary documentation, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for flexible boundaries. "
            "Counterarguments include operational flexibility, mitigated by standardized boundary definition frameworks. "
            "Resolution is achieved by adopting boundary definition frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Boundary documentation",
            "Review frequency",
            "Stakeholder engagement",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for flexible boundaries",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Boundary definition frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Monitoring Infrastructure",
        keywords=["SLO", "monitoring infrastructure", "scalability", "performance", "capacity"],
        conclusion_template="Monitoring infrastructure must be scalable, performant, and reliable for SLO enforcement.",
        reasoning_framework=(
            "Monitoring infrastructure ensures accurate SLO enforcement and compliance. "
            "Infrastructure must be scalable, performant, and reliable, with documented policies and periodic review. "
            "Key factors include infrastructure scalability, performance, and capacity planning. "
            "Primary authority is Google SRE, Netflix Performance Engineering, and industry best practices. "
            "Burden holder is the reliability engineering team, adversaries may argue for minimal infrastructure. "
            "Counterarguments include operational overhead, mitigated by automation and scalable frameworks. "
            "Resolution is achieved by adopting scalable monitoring infrastructure frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Infrastructure scalability",
            "Performance",
            "Capacity planning",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "Netflix Performance Engineering",
            "Industry Best Practices"
        ],
        burden_holder="Reliability Engineering Team",
        adversary_position="Advocates for minimal infrastructure",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in scalability",
            "Potential for resource exhaustion"
        ],
        resolution_strategy="Scalable monitoring infrastructure frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Netflix Performance Engineering"
    ),
    DoctrineBlock(
        topic="SLO Alerting Thresholds",
        keywords=["SLO", "alerting thresholds", "burn rate", "incident response", "monitoring"],
        conclusion_template="Alerting thresholds must be documented, reviewed, and tuned periodically for SLO compliance.",
        reasoning_framework=(
            "Alerting thresholds ensure timely response to SLO violations. "
            "Thresholds must be documented, reviewed, and tuned periodically to balance sensitivity and noise. "
            "Key factors include threshold documentation, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, Prometheus Alerting, and industry best practices. "
            "Burden holder is the monitoring team, adversaries may argue for static thresholds. "
            "Counterarguments include operational flexibility, mitigated by standardized threshold tuning frameworks. "
            "Resolution is achieved by adopting threshold tuning frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Threshold documentation",
            "Review frequency",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus Alerting",
            "Industry Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Advocates for static thresholds",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in tuning",
            "Potential for alert fatigue"
        ],
        resolution_strategy="Threshold tuning frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Prometheus Alerting"
    ),
    DoctrineBlock(
        topic="SLO Reliability Reporting",
        keywords=["SLO", "reliability reporting", "stakeholder", "communication", "trend"],
        conclusion_template="Reliability reporting must include SLO status, error budget, and trend analysis for stakeholders.",
        reasoning_framework=(
            "Reliability reporting ensures stakeholders are informed of SLO status, error budget, and trends. "
            "Reporting must be documented, accessible, and reviewed periodically. "
            "Key factors include reporting completeness, accessibility, and review frequency. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal reporting. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting reliability reporting frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Reporting completeness",
            "Accessibility",
            "Review frequency",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal reporting",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Reliability reporting frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Compliance Review",
        keywords=["SLO", "compliance review", "audit", "stakeholder", "documentation"],
        conclusion_template="SLO compliance must be reviewed periodically with documented audits and stakeholder input.",
        reasoning_framework=(
            "Compliance review ensures SLOs are enforced and documented for accountability. "
            "Reviews must be conducted periodically with documented audits and stakeholder input. "
            "Key factors include review frequency, audit documentation, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal review. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by adopting compliance review frameworks and periodic audits. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Review frequency",
            "Audit documentation",
            "Stakeholder engagement",
            "Automation"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for minimal review",
        counter_arguments=[
            "Operational overhead",
            "Difficulty in documentation",
            "Potential for review fatigue"
        ],
        resolution_strategy="Compliance review frameworks and periodic audits",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Onboarding Process",
        keywords=["SLO", "onboarding", "process", "documentation", "stakeholder"],
        conclusion_template="New services must be onboarded with documented SLOs, SLIs, and stakeholder approval.",
        reasoning_framework=(
            "Onboarding ensures new services are monitored with documented SLOs and SLIs. "
            "Processes must specify onboarding documentation, review frequency, and stakeholder approval. "
            "Key factors include onboarding documentation, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for ad-hoc onboarding. "
            "Counterarguments include operational flexibility, mitigated by standardized onboarding frameworks. "
            "Resolution is achieved by adopting onboarding frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Onboarding documentation",
            "Review frequency",
            "Stakeholder engagement",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for ad-hoc onboarding",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Onboarding frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Decommissioning Process",
        keywords=["SLO", "decommissioning", "process", "documentation", "stakeholder"],
        conclusion_template="Decommissioned services must have documented SLO decommissioning processes and stakeholder approval.",
        reasoning_framework=(
            "Decommissioning ensures services are removed from SLO monitoring with documented processes. "
            "Processes must specify decommissioning documentation, review frequency, and stakeholder approval. "
            "Key factors include decommissioning documentation, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for ad-hoc decommissioning. "
            "Counterarguments include operational flexibility, mitigated by standardized decommissioning frameworks. "
            "Resolution is achieved by adopting decommissioning frameworks and periodic reviews. "
            "Entity scope is the service as monitored by S07_slo_monitor."
        ),
        key_factors=[
            "Decommissioning documentation",
            "Review frequency",
            "Stakeholder engagement",
            "Auditability"
        ],
        primary_authority=[
            "Google SRE Book",
            "SRE Workbook",
            "Industry Best Practices"
        ],
        burden_holder="Service Owner",
        adversary_position="Advocates for ad-hoc decommissioning",
        counter_arguments=[
            "Operational flexibility",
            "Difficulty in documentation",
            "Potential for abuse"
        ],
        resolution_strategy="Decommissioning frameworks and periodic reviews",
        entity_scope="Service as monitored by S07_slo_monitor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Book, Chapter 4"
    ),
    DoctrineBlock(
        topic="SLO Documentation Versioning",
        keywords=["SLO", "documentation", "versioning", "review", "audit"],
        conclusion_template="SLO documentation must be versioned, reviewed, and auditable for compliance.",
        reasoning_framework=(
            "Versioning ensures SLO documentation is reviewed and auditable for compliance. "
            "Documentation must specify version history, review frequency, and auditability. "
            "Key factors include version history, review frequency, and stakeholder engagement. "
            "Primary authority is Google SRE, SRE Workbook, and industry best practices. "
            "Burden holder is the service owner, adversaries may argue for minimal versioning. "
            "Counterarguments include operational overhead, mitigated by automation and standardized templates. "
            "Resolution is achieved by