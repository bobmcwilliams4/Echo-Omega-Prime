from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    CRITICAL = "Critical"
    CAUTION = "Caution"

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
        topic="health_check_patterns",
        keywords=["health check", "endpoint", "liveness", "readiness", "probe", "monitoring"],
        conclusion_template="A robust health check pattern ensures early detection of service failures and facilitates automated recovery.",
        reasoning_framework="""
Health check patterns are essential in distributed systems to ascertain the operational status of individual services. The primary reasoning is to distinguish between liveness (is the process running) and readiness (is the process ready to serve traffic). Health checks should be lightweight, non-intrusive, and expose minimal information to prevent security risks. They must be integrated with orchestration tools (e.g., Kubernetes) and monitoring systems. A failure in health checks should trigger automated remediation, such as restarting containers or rerouting traffic. Overly aggressive health checks can cause unnecessary restarts and false positives, so thresholds and backoff strategies are critical. Health check endpoints should not perform expensive operations or depend on downstream services unless those dependencies are critical for readiness.
""",
        key_factors=[
            "Liveness vs Readiness distinction",
            "Integration with orchestration",
            "Security of health endpoints",
            "Thresholds for failure",
            "Automated remediation"
        ],
        primary_authority=[
            "Google SRE Book",
            "Kubernetes Documentation",
            "AWS Well-Architected Framework"
        ],
        burden_holder="Service Owner",
        adversary_position="Health checks increase attack surface and may cause false positives.",
        counter_arguments=[
            "Health checks can be secured via authentication and rate limiting.",
            "False positives can be mitigated with proper thresholds and backoff."
        ],
        resolution_strategy="Implement layered health checks with clear separation between liveness and readiness, and secure endpoints.",
        entity_scope="Microservices, Containers, Distributed Systems",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kubernetes Health Check Implementation"
    ),
    DoctrineBlock(
        topic="circuit_breaker_pattern",
        keywords=["circuit breaker", "failure", "resilience", "fallback", "timeout", "retry"],
        conclusion_template="Circuit breaker patterns prevent cascading failures and improve system resilience by isolating faulty components.",
        reasoning_framework="""
The circuit breaker pattern is a defensive mechanism in distributed systems to prevent repeated failures from overwhelming dependent services. When a service detects a threshold of failures, it 'opens' the circuit, blocking further requests and allowing the system to recover. After a cooldown period, the circuit can 'half-open' to test if the service has recovered. This pattern reduces latency spikes, prevents resource exhaustion, and enables graceful degradation. Implementation requires careful tuning of thresholds, fallback logic, and monitoring of breaker states. Circuit breakers should be transparent to operators and integrated with alerting systems. Overuse or misconfiguration can lead to unnecessary isolation and reduced availability.
""",
        key_factors=[
            "Failure thresholds",
            "Cooldown period",
            "Fallback mechanisms",
            "Integration with monitoring",
            "Transparency"
        ],
        primary_authority=[
            "Netflix Hystrix",
            "Microsoft Azure Architecture",
            "Google SRE Book"
        ],
        burden_holder="Platform Engineering",
        adversary_position="Circuit breakers may isolate healthy services and reduce availability.",
        counter_arguments=[
            "Proper tuning and monitoring prevent unnecessary isolation.",
            "Fallbacks ensure continued service even during failures."
        ],
        resolution_strategy="Tune circuit breaker thresholds based on historical data and integrate with observability tools.",
        entity_scope="APIs, Microservices, Distributed Systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Netflix Hystrix Circuit Breaker"
    ),
    DoctrineBlock(
        topic="golden_signals",
        keywords=["latency", "traffic", "errors", "saturation", "monitoring", "observability"],
        conclusion_template="Monitoring golden signals provides actionable insights into system health and enables rapid incident response.",
        reasoning_framework="""
Golden signals are four key metrics: latency, traffic, errors, and saturation. These signals provide a holistic view of system health and performance. Monitoring latency reveals responsiveness, traffic indicates usage patterns, errors highlight failures, and saturation shows resource constraints. Prioritizing golden signals in dashboards and alerts ensures operators focus on actionable data. Over-monitoring can lead to alert fatigue, so signals should be contextualized and thresholds set based on historical norms. Golden signals should be collected at both service and infrastructure levels, and correlated with business metrics for comprehensive health assessment.
""",
        key_factors=[
            "Latency measurement",
            "Traffic analysis",
            "Error tracking",
            "Resource saturation",
            "Alert prioritization"
        ],
        primary_authority=[
            "Google SRE Book",
            "Prometheus Documentation",
            "Datadog Monitoring Guide"
        ],
        burden_holder="SRE Team",
        adversary_position="Golden signals may not capture all failure modes.",
        counter_arguments=[
            "Supplement with custom metrics for domain-specific failures.",
            "Correlate golden signals with logs and traces for deeper analysis."
        ],
        resolution_strategy="Establish dashboards and alerts based on golden signals, with periodic review of thresholds.",
        entity_scope="Distributed Systems, Cloud Infrastructure",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Golden Signals"
    ),
    DoctrineBlock(
        topic="distributed_systems_observability",
        keywords=["observability", "tracing", "logging", "metrics", "correlation", "visibility"],
        conclusion_template="Comprehensive observability enables proactive detection and resolution of distributed system failures.",
        reasoning_framework="""
Observability in distributed systems requires collecting and correlating metrics, logs, and traces across services. The reasoning is to provide visibility into system internals, enabling operators to diagnose issues, understand dependencies, and optimize performance. Observability tools must support high cardinality, real-time analysis, and historical data retention. Instrumentation should be standardized and automated to reduce toil. Observability is not just monitoring; it is the ability to ask new questions about system behavior. Challenges include data volume, noise, and context loss. Solutions involve sampling, aggregation, and contextual tagging.
""",
        key_factors=[
            "Metrics collection",
            "Log aggregation",
            "Distributed tracing",
            "Correlation across services",
            "Data retention"
        ],
        primary_authority=[
            "OpenTelemetry",
            "Google SRE Book",
            "Honeycomb Observability Guide"
        ],
        burden_holder="Observability Engineering",
        adversary_position="Observability increases complexity and costs.",
        counter_arguments=[
            "Sampling and aggregation reduce data volume.",
            "Automated instrumentation minimizes manual effort."
        ],
        resolution_strategy="Adopt standardized observability frameworks and automate instrumentation.",
        entity_scope="Distributed Systems, Microservices",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OpenTelemetry Adoption"
    ),
    DoctrineBlock(
        topic="error_budgets",
        keywords=["error budget", "SLO", "SLA", "availability", "risk management", "release gating"],
        conclusion_template="Error budgets balance reliability and innovation, guiding release decisions and operational priorities.",
        reasoning_framework="""
Error budgets quantify acceptable failure rates based on Service Level Objectives (SLOs). The reasoning is to allow teams to innovate and deploy changes without exceeding reliability targets. When the error budget is consumed, releases are gated and focus shifts to remediation. Error budgets align engineering and business priorities, enabling risk-managed operations. Key challenges include accurate SLO definition, real-time tracking, and cross-team communication. Error budgets should be visible, actionable, and reviewed regularly. Overly strict budgets can stifle innovation, while lax budgets undermine reliability.
""",
        key_factors=[
            "SLO definition",
            "Error budget tracking",
            "Release gating",
            "Remediation prioritization",
            "Visibility"
        ],
        primary_authority=[
            "Google SRE Book",
            "AWS Well-Architected Framework",
            "Microsoft Azure SLO Guide"
        ],
        burden_holder="Product Engineering",
        adversary_position="Error budgets may be manipulated or ignored.",
        counter_arguments=[
            "Automated tracking and transparent reporting prevent manipulation.",
            "Cross-team reviews ensure accountability."
        ],
        resolution_strategy="Integrate error budgets into CI/CD pipelines and operational dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Error Budget Practice"
    ),
    DoctrineBlock(
        topic="alert_fatigue_prevention",
        keywords=["alert fatigue", "monitoring", "noise reduction", "thresholds", "actionable alerts"],
        conclusion_template="Preventing alert fatigue ensures operators respond to critical incidents without distraction from noise.",
        reasoning_framework="""
Alert fatigue occurs when operators are overwhelmed by excessive or non-actionable alerts, leading to missed incidents and reduced responsiveness. The reasoning is to prioritize actionable alerts, tune thresholds, and suppress noise. Alert deduplication, escalation policies, and periodic review of alert configurations are essential. Automation can close resolved alerts and route incidents based on severity. Alerting systems should support contextual information and correlation with incidents. Continuous improvement is necessary as systems evolve.
""",
        key_factors=[
            "Alert prioritization",
            "Threshold tuning",
            "Deduplication",
            "Escalation policies",
            "Periodic review"
        ],
        primary_authority=[
            "PagerDuty Incident Response Guide",
            "Google SRE Book",
            "Datadog Alerting Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Suppressing alerts may hide real issues.",
        counter_arguments=[
            "Periodic review ensures critical alerts are not suppressed.",
            "Escalation policies route unresolved incidents."
        ],
        resolution_strategy="Establish alert review cycles and automate deduplication.",
        entity_scope="Operations, SRE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Alert Fatigue Mitigation"
    ),
    DoctrineBlock(
        topic="capacity_planning",
        keywords=["capacity planning", "scaling", "resource allocation", "forecasting", "load testing"],
        conclusion_template="Effective capacity planning ensures system scalability and prevents resource exhaustion during peak loads.",
        reasoning_framework="""
Capacity planning involves forecasting resource needs based on historical usage, growth projections, and anticipated peak loads. The reasoning is to prevent resource exhaustion, maintain performance, and optimize costs. Load testing and stress testing validate capacity assumptions. Planning must account for redundancy, failover, and multi-region deployments. Over-provisioning increases costs, while under-provisioning risks outages. Automation and dynamic scaling (e.g., autoscaling groups) improve responsiveness. Capacity plans should be reviewed quarterly and updated based on business changes.
""",
        key_factors=[
            "Historical usage analysis",
            "Growth projections",
            "Load testing",
            "Redundancy planning",
            "Cost optimization"
        ],
        primary_authority=[
            "AWS Well-Architected Framework",
            "Google SRE Book",
            "Microsoft Azure Capacity Planning"
        ],
        burden_holder="Infrastructure Engineering",
        adversary_position="Capacity planning is expensive and may be inaccurate.",
        counter_arguments=[
            "Automation reduces manual effort and increases accuracy.",
            "Dynamic scaling adapts to real-time demand."
        ],
        resolution_strategy="Automate capacity monitoring and integrate with scaling policies.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Autoscaling Implementation"
    ),
    DoctrineBlock(
        topic="dependency_management",
        keywords=["dependency", "service mesh", "upstream", "downstream", "failure isolation", "versioning"],
        conclusion_template="Robust dependency management isolates failures and enables safe upgrades in distributed systems.",
        reasoning_framework="""
Dependency management in distributed systems requires mapping upstream and downstream relationships, versioning, and failure isolation. The reasoning is to prevent cascading failures, enable safe upgrades, and maintain service contracts. Service meshes provide visibility and control over dependencies. Automated dependency tracking and health checks are essential. Versioning strategies (e.g., semantic versioning) ensure compatibility. Dependency graphs should be updated as services evolve. Failure isolation mechanisms (e.g., circuit breakers, retries) protect critical paths.
""",
        key_factors=[
            "Dependency mapping",
            "Versioning",
            "Failure isolation",
            "Service mesh integration",
            "Automated tracking"
        ],
        primary_authority=[
            "Istio Service Mesh",
            "Google SRE Book",
            "AWS Dependency Management"
        ],
        burden_holder="Service Owner",
        adversary_position="Complex dependency graphs increase operational risk.",
        counter_arguments=[
            "Automated tools simplify dependency tracking.",
            "Service mesh provides centralized control."
        ],
        resolution_strategy="Adopt service mesh and automate dependency tracking.",
        entity_scope="Microservices, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Istio Dependency Management"
    ),
    DoctrineBlock(
        topic="incident_classification",
        keywords=["incident", "classification", "severity", "priority", "response", "root cause"],
        conclusion_template="Incident classification enables efficient response and prioritization of remediation efforts.",
        reasoning_framework="""
Incident classification assigns severity and priority to incidents based on impact, urgency, and affected systems. The reasoning is to ensure efficient response, resource allocation, and communication. Classification frameworks should be standardized and reviewed periodically. Root cause analysis is facilitated by accurate classification. Automation can assist in initial classification, but human review is essential for complex incidents. Over-classification leads to confusion, while under-classification delays response.
""",
        key_factors=[
            "Severity assignment",
            "Priority determination",
            "Standardization",
            "Root cause analysis",
            "Automation"
        ],
        primary_authority=[
            "PagerDuty Incident Classification",
            "Google SRE Book",
            "ITIL Incident Management"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Classification frameworks may be too rigid.",
        counter_arguments=[
            "Periodic review ensures frameworks remain relevant.",
            "Human review supplements automation."
        ],
        resolution_strategy="Standardize classification and automate initial triage.",
        entity_scope="Operations, SRE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Incident Classification"
    ),
    DoctrineBlock(
        topic="chaos_engineering",
        keywords=["chaos engineering", "failure injection", "resilience", "testing", "recovery"],
        conclusion_template="Chaos engineering validates system resilience by proactively testing failure scenarios.",
        reasoning_framework="""
Chaos engineering involves deliberately injecting failures into systems to test resilience and recovery mechanisms. The reasoning is to uncover hidden weaknesses, validate failover strategies, and improve incident response. Experiments should be controlled, scoped, and monitored. Key factors include impact assessment, rollback mechanisms, and stakeholder communication. Chaos experiments must not compromise customer experience or violate SLAs. Results should inform remediation and system improvements. Automation enables regular chaos testing, but manual oversight is necessary for high-risk scenarios.
""",
        key_factors=[
            "Failure injection",
            "Impact assessment",
            "Rollback mechanisms",
            "Stakeholder communication",
            "Automation"
        ],
        primary_authority=[
            "Netflix Chaos Monkey",
            "Google SRE Book",
            "Gremlin Chaos Engineering"
        ],
        burden_holder="Platform Engineering",
        adversary_position="Chaos engineering risks production stability.",
        counter_arguments=[
            "Controlled experiments minimize risk.",
            "Rollback mechanisms ensure rapid recovery."
        ],
        resolution_strategy="Scope chaos experiments and automate rollback.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Netflix Chaos Monkey"
    ),
    DoctrineBlock(
        topic="service_mesh_monitoring",
        keywords=["service mesh", "monitoring", "traffic", "latency", "security", "observability"],
        conclusion_template="Monitoring service mesh components ensures visibility, security, and performance in microservices architectures.",
        reasoning_framework="""
Service mesh monitoring involves tracking traffic, latency, errors, and security events across mesh-managed services. The reasoning is to provide visibility into inter-service communication, enforce security policies, and optimize performance. Mesh telemetry should be integrated with centralized observability platforms. Key factors include high cardinality metrics, distributed tracing, and policy enforcement. Mesh monitoring must scale with service growth and support multi-region deployments. Overhead and complexity are challenges; solutions involve sampling and aggregation.
""",
        key_factors=[
            "Traffic monitoring",
            "Latency tracking",
            "Security event logging",
            "Distributed tracing",
            "Policy enforcement"
        ],
        primary_authority=[
            "Istio Documentation",
            "Linkerd Service Mesh",
            "Google SRE Book"
        ],
        burden_holder="Observability Engineering",
        adversary_position="Mesh monitoring increases overhead and complexity.",
        counter_arguments=[
            "Sampling reduces overhead.",
            "Centralized platforms simplify analysis."
        ],
        resolution_strategy="Integrate mesh telemetry with observability tools and automate sampling.",
        entity_scope="Microservices, Distributed Systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Istio Mesh Monitoring"
    ),
    DoctrineBlock(
        topic="runbook_automation",
        keywords=["runbook", "automation", "incident response", "playbook", "remediation"],
        conclusion_template="Automating runbooks accelerates incident response and reduces operational toil.",
        reasoning_framework="""
Runbook automation converts manual incident response procedures into executable workflows. The reasoning is to reduce response time, eliminate human error, and standardize remediation. Automated runbooks should be versioned, tested, and integrated with incident management systems. Key factors include idempotency, rollback, and auditability. Automation must not compromise security or violate compliance requirements. Over-automation risks loss of situational awareness; balance is needed.
""",
        key_factors=[
            "Workflow automation",
            "Versioning",
            "Testing",
            "Idempotency",
            "Auditability"
        ],
        primary_authority=[
            "PagerDuty Runbook Automation",
            "Google SRE Book",
            "AWS Systems Manager"
        ],
        burden_holder="Operations Team",
        adversary_position="Automation may hide critical steps and reduce situational awareness.",
        counter_arguments=[
            "Versioning and audit logs maintain transparency.",
            "Manual overrides ensure control."
        ],
        resolution_strategy="Automate routine runbooks and maintain manual review for complex incidents.",
        entity_scope="Operations, SRE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Runbook Automation"
    ),
    DoctrineBlock(
        topic="monitoring_antipatterns",
        keywords=["monitoring", "antipatterns", "noise", "blind spots", "over-monitoring", "under-monitoring"],
        conclusion_template="Avoiding monitoring antipatterns ensures actionable insights and reduces operational risks.",
        reasoning_framework="""
Monitoring antipatterns include over-monitoring (excessive metrics), under-monitoring (blind spots), and misconfigured alerts. The reasoning is to focus on actionable data, reduce noise, and ensure coverage of critical paths. Antipatterns can lead to alert fatigue, missed incidents, and wasted resources. Solutions involve periodic review, prioritization of golden signals, and automation of monitoring configuration. Monitoring must evolve with system changes; static configurations become obsolete.
""",
        key_factors=[
            "Coverage of critical paths",
            "Noise reduction",
            "Periodic review",
            "Automation",
            "Prioritization"
        ],
        primary_authority=[
            "Google SRE Book",
            "Datadog Monitoring Guide",
            "AWS Monitoring Best Practices"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Antipatterns are hard to detect and correct.",
        counter_arguments=[
            "Automation and periodic review identify antipatterns early.",
            "Golden signals provide baseline coverage."
        ],
        resolution_strategy="Automate monitoring reviews and prioritize actionable metrics.",
        entity_scope="Operations, SRE",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Monitoring Antipatterns"
    ),
    DoctrineBlock(
        topic="sre_toil_reduction",
        keywords=["SRE", "toil", "automation", "manual work", "efficiency", "scalability"],
        conclusion_template="Reducing SRE toil through automation increases efficiency and enables focus on high-value engineering.",
        reasoning_framework="""
SRE toil is repetitive, manual work that does not scale and provides little lasting value. The reasoning is to automate toil, freeing SREs to focus on engineering improvements. Toil reduction involves identifying high-frequency manual tasks, automating workflows, and measuring impact. Automation must be reliable, auditable, and maintainable. Over-automation risks loss of context; balance is needed. Toil metrics should be tracked and reviewed quarterly.
""",
        key_factors=[
            "Toil identification",
            "Workflow automation",
            "Impact measurement",
            "Auditability",
            "Maintainability"
        ],
        primary_authority=[
            "Google SRE Book",
            "PagerDuty Automation Guide",
            "AWS Systems Manager"
        ],
        burden_holder="SRE Team",
        adversary_position="Automation may reduce situational awareness.",
        counter_arguments=[
            "Audit logs and manual review maintain transparency.",
            "Impact measurement ensures value."
        ],
        resolution_strategy="Automate high-frequency toil and review impact regularly.",
        entity_scope="Operations, SRE",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Toil Reduction"
    ),
    DoctrineBlock(
        topic="graceful_degradation",
        keywords=["graceful degradation", "failure", "fallback", "resilience", "user experience"],
        conclusion_template="Graceful degradation maintains core functionality during partial failures, preserving user experience.",
        reasoning_framework="""
Graceful degradation involves designing systems to maintain essential functionality during partial failures. The reasoning is to preserve user experience, prevent total outages, and enable recovery. Fallback mechanisms, feature toggles, and redundancy are key. Degraded modes must be communicated to users and monitored for impact. Overuse of degradation risks masking systemic issues; balance is needed. Testing degraded modes ensures reliability.
""",
        key_factors=[
            "Fallback mechanisms",
            "Feature toggles",
            "Redundancy",
            "User communication",
            "Testing"
        ],
        primary_authority=[
            "Google SRE Book",
            "AWS Well-Architected Framework",
            "Microsoft Azure Resilience Guide"
        ],
        burden_holder="Product Engineering",
        adversary_position="Degradation may mask systemic failures.",
        counter_arguments=[
            "Monitoring degraded modes reveals underlying issues.",
            "User communication maintains transparency."
        ],
        resolution_strategy="Design fallback mechanisms and monitor degraded modes.",
        entity_scope="Cloud Services, APIs",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Graceful Degradation"
    ),
    DoctrineBlock(
        topic="post_incident_review",
        keywords=["post incident review", "retrospective", "blameless", "root cause", "remediation"],
        conclusion_template="Blameless post-incident reviews drive continuous improvement and prevent recurrence of failures.",
        reasoning_framework="""
Post-incident reviews (PIRs) are structured retrospectives conducted after major incidents. The reasoning is to identify root causes, document remediation, and drive continuous improvement. Reviews must be blameless, focusing on systemic issues rather than individual fault. PIRs should be documented, actionable, and shared across teams. Key factors include timeline reconstruction, impact assessment, and follow-up tracking. Overly punitive reviews discourage transparency; blameless culture is essential.
""",
        key_factors=[
            "Blameless culture",
            "Root cause analysis",
            "Timeline reconstruction",
            "Actionable remediation",
            "Follow-up tracking"
        ],
        primary_authority=[
            "Google SRE Book",
            "PagerDuty Post-Incident Review Guide",
            "ITIL Incident Management"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Reviews may become punitive or lack follow-up.",
        counter_arguments=[
            "Blameless culture encourages transparency.",
            "Follow-up tracking ensures remediation."
        ],
        resolution_strategy="Standardize PIRs and automate follow-up tracking.",
        entity_scope="Operations, SRE",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Post-Incident Review"
    ),
    DoctrineBlock(
        topic="multi_region_health",
        keywords=["multi-region", "health", "failover", "redundancy", "latency", "disaster recovery"],
        conclusion_template="Multi-region health monitoring ensures resilience, failover, and optimal performance across geographies.",
        reasoning_framework="""
Multi-region health involves monitoring and managing services deployed across multiple geographic regions. The reasoning is to ensure resilience, enable failover, and optimize latency. Health checks must be region-aware and integrated with failover mechanisms. Redundancy planning and disaster recovery are key. Challenges include network partitioning, data consistency, and cost management. Solutions involve automated failover, replication, and regional dashboards.
""",
        key_factors=[
            "Region-aware health checks",
            "Failover mechanisms",
            "Redundancy planning",
            "Disaster recovery",
            "Latency optimization"
        ],
        primary_authority=[
            "AWS Multi-Region Architecture",
            "Google SRE Book",
            "Microsoft Azure Disaster Recovery"
        ],
        burden_holder="Infrastructure Engineering",
        adversary_position="Multi-region deployments increase complexity and cost.",
        counter_arguments=[
            "Automation reduces operational overhead.",
            "Regional dashboards provide visibility."
        ],
        resolution_strategy="Automate failover and monitor region-specific health.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Multi-Region Health Monitoring"
    ),
    DoctrineBlock(
        topic="container_health",
        keywords=["container", "health", "liveness", "readiness", "monitoring", "orchestration"],
        conclusion_template="Container health monitoring ensures reliable orchestration and rapid recovery from failures.",
        reasoning_framework="""
Container health involves monitoring liveness and readiness probes, resource usage, and orchestration events. The reasoning is to ensure containers are running, ready to serve traffic, and recover quickly from failures. Health checks must be lightweight and integrated with orchestration platforms (e.g., Kubernetes). Resource limits and quotas prevent exhaustion. Automated remediation (e.g., restart policies) reduces downtime. Challenges include noisy neighbors and ephemeral containers.
""",
        key_factors=[
            "Liveness and readiness probes",
            "Resource usage monitoring",
            "Orchestration integration",
            "Automated remediation",
            "Resource limits"
        ],
        primary_authority=[
            "Kubernetes Documentation",
            "Docker Health Checks",
            "Google SRE Book"
        ],
        burden_holder="Platform Engineering",
        adversary_position="Ephemeral containers complicate health monitoring.",
        counter_arguments=[
            "Orchestration platforms provide automated health checks.",
            "Resource limits prevent exhaustion."
        ],
        resolution_strategy="Integrate health checks with orchestration and automate remediation.",
        entity_scope="Containers, Microservices",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kubernetes Container Health"
    ),
    DoctrineBlock(
        topic="database_health_monitoring",
        keywords=["database", "health", "monitoring", "query latency", "replication", "backup", "failover"],
        conclusion_template="Database health monitoring ensures data integrity, performance, and rapid recovery from failures.",
        reasoning_framework="""
Database health involves monitoring query latency, replication status, backup integrity, and failover readiness. The reasoning is to ensure data integrity, maintain performance, and enable rapid recovery. Health checks must be integrated with application monitoring and alerting. Key factors include replication lag, backup verification, and failover testing. Challenges include scaling, noisy neighbors, and cross-region replication. Solutions involve automation, periodic testing, and dashboard visibility.
""",
        key_factors=[
            "Query latency monitoring",
            "Replication status",
            "Backup integrity",
            "Failover readiness",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS RDS Monitoring",
            "Google Cloud SQL Health",
            "Microsoft Azure Database Monitoring"
        ],
        burden_holder="Database Engineering",
        adversary_position="Database health checks may impact performance.",
        counter_arguments=[
            "Lightweight checks minimize impact.",
            "Automation reduces manual effort."
        ],
        resolution_strategy="Automate health checks and integrate with dashboards.",
        entity_scope="Databases, Cloud Infrastructure",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS RDS Health Monitoring"
    ),
    DoctrineBlock(
        topic="synthetic_monitoring",
        keywords=["synthetic monitoring", "probes", "availability", "performance", "user experience"],
        conclusion_template="Synthetic monitoring validates system availability and performance from the user's perspective.",
        reasoning_framework="""
Synthetic monitoring involves running scripted probes to simulate user interactions and validate system availability and performance. The reasoning is to detect outages, latency spikes, and degraded user experience before customers are impacted. Probes should cover critical paths, be distributed across regions, and run at regular intervals. Key factors include probe coverage, frequency, and alert integration. Challenges include false positives and probe maintenance. Solutions involve periodic review and automation.
""",
        key_factors=[
            "Probe coverage",
            "Frequency",
            "Alert integration",
            "Regional distribution",
            "Maintenance"
        ],
        primary_authority=[
            "Datadog Synthetic Monitoring",
            "AWS CloudWatch Synthetics",
            "Google SRE Book"
        ],
        burden_holder="Monitoring Team",
        adversary_position="Synthetic probes may miss real user issues.",
        counter_arguments=[
            "Combine synthetic and real user monitoring.",
            "Periodic review ensures probe relevance."
        ],
        resolution_strategy="Integrate synthetic monitoring with real user metrics and automate probe maintenance.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Datadog Synthetic Monitoring"
    ),
    DoctrineBlock(
        topic="cost_monitoring",
        keywords=["cost", "monitoring", "optimization", "resource usage", "billing", "forecasting"],
        conclusion_template="Cost monitoring enables resource optimization and prevents budget overruns in cloud environments.",
        reasoning_framework="""
Cost monitoring involves tracking resource usage, billing, and forecasting expenses in cloud environments. The reasoning is to optimize resource allocation, prevent budget overruns, and align costs with business priorities. Key factors include real-time usage tracking, alerting on anomalies, and integration with capacity planning. Challenges include complex billing models and unpredictable usage spikes. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Real-time usage tracking",
            "Anomaly alerting",
            "Integration with capacity planning",
            "Dashboard visibility",
            "Periodic review"
        ],
        primary_authority=[
            "AWS Cost Explorer",
            "Google Cloud Billing",
            "Microsoft Azure Cost Management"
        ],
        burden_holder="Finance and Engineering",
        adversary_position="Cost monitoring adds operational overhead.",
        counter_arguments=[
            "Automation reduces manual effort.",
            "Dashboards provide actionable insights."
        ],
        resolution_strategy="Automate cost tracking and integrate with resource optimization tools.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Cost Explorer"
    ),
    DoctrineBlock(
        topic="log_aggregation_health",
        keywords=["log aggregation", "health", "logging", "centralization", "search", "retention"],
        conclusion_template="Log aggregation health ensures centralized visibility, rapid search, and compliance in distributed systems.",
        reasoning_framework="""
Log aggregation involves collecting logs from distributed services into centralized platforms for search, analysis, and retention. The reasoning is to enable rapid incident response, compliance, and historical analysis. Key factors include log format standardization, retention policies, and search performance. Challenges include data volume, privacy, and cost. Solutions involve sampling, compression, and access controls.
""",
        key_factors=[
            "Log format standardization",
            "Retention policies",
            "Search performance",
            "Sampling and compression",
            "Access controls"
        ],
        primary_authority=[
            "ELK Stack",
            "Splunk Log Aggregation",
            "Google SRE Book"
        ],
        burden_holder="Observability Engineering",
        adversary_position="Log aggregation increases storage costs and privacy risks.",
        counter_arguments=[
            "Retention policies and access controls mitigate risks.",
            "Sampling reduces storage costs."
        ],
        resolution_strategy="Standardize log formats and automate retention management.",
        entity_scope="Distributed Systems, Cloud Infrastructure",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ELK Stack Log Aggregation"
    ),
    DoctrineBlock(
        topic="security_health_signals",
        keywords=["security", "health", "signals", "monitoring", "vulnerability", "incident response"],
        conclusion_template="Security health signals enable proactive detection and response to vulnerabilities and threats.",
        reasoning_framework="""
Security health signals involve monitoring for vulnerabilities, threats, and anomalous activity across systems. The reasoning is to enable proactive detection, rapid response, and compliance. Key factors include integration with SIEM platforms, real-time alerting, and periodic vulnerability scanning. Challenges include false positives, alert fatigue, and evolving threat landscapes. Solutions involve automation, contextual alerting, and continuous improvement.
""",
        key_factors=[
            "SIEM integration",
            "Real-time alerting",
            "Vulnerability scanning",
            "Contextual alerting",
            "Continuous improvement"
        ],
        primary_authority=[
            "Splunk SIEM",
            "AWS Security Hub",
            "Google SRE Book"
        ],
        burden_holder="Security Team",
        adversary_position="Security signals may generate false positives and alert fatigue.",
        counter_arguments=[
            "Contextual alerting reduces noise.",
            "Continuous improvement adapts to evolving threats."
        ],
        resolution_strategy="Automate vulnerability scanning and contextual alerting.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Splunk SIEM Security Signals"
    ),
    DoctrineBlock(
        topic="sla_compliance_monitoring",
        keywords=["SLA", "compliance", "monitoring", "availability", "performance", "reporting"],
        conclusion_template="SLA compliance monitoring ensures contractual obligations are met and informs business decisions.",
        reasoning_framework="""
SLA compliance monitoring involves tracking availability and performance against contractual Service Level Agreements. The reasoning is to ensure obligations are met, inform business decisions, and enable remediation. Key factors include real-time tracking, automated reporting, and alerting on breaches. Challenges include accurate measurement, reporting delays, and cross-region SLAs. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Real-time tracking",
            "Automated reporting",
            "Alerting on breaches",
            "Dashboard visibility",
            "Periodic review"
        ],
        primary_authority=[
            "AWS SLA Monitoring",
            "Google SRE Book",
            "Microsoft Azure SLA Compliance"
        ],
        burden_holder="Product Engineering",
        adversary_position="SLA monitoring may miss subtle breaches.",
        counter_arguments=[
            "Automated tracking increases accuracy.",
            "Periodic review ensures coverage."
        ],
        resolution_strategy="Automate SLA tracking and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS SLA Monitoring"
    ),
    DoctrineBlock(
        topic="network_health_monitoring",
        keywords=["network", "health", "monitoring", "latency", "packet loss", "availability"],
        conclusion_template="Network health monitoring ensures connectivity, performance, and rapid detection of outages.",
        reasoning_framework="""
Network health involves monitoring latency, packet loss, throughput, and availability across infrastructure. The reasoning is to ensure connectivity, optimize performance, and detect outages rapidly. Key factors include real-time metrics, alerting, and integration with incident response. Challenges include noisy neighbors, cross-region connectivity, and scaling. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Latency monitoring",
            "Packet loss tracking",
            "Throughput measurement",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS Network Monitoring",
            "Google SRE Book",
            "Cisco Network Health"
        ],
        burden_holder="Network Engineering",
        adversary_position="Network health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate network health checks and integrate with dashboards.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Network Health Monitoring"
    ),
    DoctrineBlock(
        topic="topic",
        keywords=["doctrine", "topic", "classification", "taxonomy", "domain"],
        conclusion_template="Domain topics provide a taxonomy for organizing system health doctrines.",
        reasoning_framework="""
Topics serve as a classification mechanism for organizing doctrines within the system health domain. The reasoning is to enable efficient search, retrieval, and review of authoritative content. Topics should be standardized, reviewed periodically, and aligned with evolving system architectures. Overly granular topics risk fragmentation; balance is needed. Automation can assist in topic classification and taxonomy updates.
""",
        key_factors=[
            "Standardization",
            "Periodic review",
            "Alignment with architecture",
            "Automation",
            "Balance"
        ],
        primary_authority=[
            "Google SRE Book",
            "ITIL Taxonomy",
            "AWS Well-Architected Framework"
        ],
        burden_holder="Domain Authority",
        adversary_position="Granular topics may fragment doctrine content.",
        counter_arguments=[
            "Periodic review ensures taxonomy remains relevant.",
            "Automation assists in classification."
        ],
        resolution_strategy="Standardize topics and automate taxonomy updates.",
        entity_scope="System Health Domain",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Google SRE Topic Taxonomy"
    ),
    # Additional doctrines for completeness (to reach 40+)
    DoctrineBlock(
        topic="service_version_health",
        keywords=["service version", "health", "deployment", "rollback", "compatibility"],
        conclusion_template="Service version health monitoring ensures safe deployments and rapid rollback during failures.",
        reasoning_framework="""
Service version health involves monitoring deployments, compatibility, and rollback readiness. The reasoning is to ensure new versions are healthy, compatible, and can be rolled back rapidly if failures occur. Key factors include deployment tracking, health checks, and compatibility testing. Challenges include version drift, dependency mismatches, and rollback complexity. Solutions involve automation, version tagging, and dashboard visibility.
""",
        key_factors=[
            "Deployment tracking",
            "Health checks",
            "Compatibility testing",
            "Rollback readiness",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS CodeDeploy",
            "Google SRE Book",
            "Microsoft Azure Deployment Health"
        ],
        burden_holder="Platform Engineering",
        adversary_position="Version health checks may delay deployments.",
        counter_arguments=[
            "Automation accelerates health checks.",
            "Rollback readiness reduces risk."
        ],
        resolution_strategy="Automate version health checks and maintain rollback plans.",
        entity_scope="Cloud Services, APIs",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CodeDeploy Health Monitoring"
    ),
    DoctrineBlock(
        topic="api_health_monitoring",
        keywords=["API", "health", "monitoring", "latency", "error rate", "availability"],
        conclusion_template="API health monitoring ensures reliable service delivery and rapid detection of failures.",
        reasoning_framework="""
API health involves monitoring latency, error rates, and availability. The reasoning is to ensure reliable service delivery, detect failures rapidly, and enable remediation. Key factors include real-time metrics, alerting, and integration with incident response. Challenges include scaling, noisy neighbors, and cross-region APIs. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Latency monitoring",
            "Error rate tracking",
            "Availability measurement",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS API Gateway Monitoring",
            "Google SRE Book",
            "Microsoft Azure API Health"
        ],
        burden_holder="API Engineering",
        adversary_position="API health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate API health checks and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS API Gateway Health Monitoring"
    ),
    DoctrineBlock(
        topic="resource_quota_health",
        keywords=["resource quota", "health", "limits", "allocation", "exhaustion"],
        conclusion_template="Resource quota health monitoring prevents exhaustion and ensures fair allocation across services.",
        reasoning_framework="""
Resource quota health involves monitoring limits, allocation, and exhaustion across services. The reasoning is to prevent resource exhaustion, ensure fair allocation, and optimize performance. Key factors include real-time tracking, alerting, and integration with capacity planning. Challenges include scaling, noisy neighbors, and quota drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Limit tracking",
            "Allocation monitoring",
            "Exhaustion alerting",
            "Capacity planning integration",
            "Dashboard visibility"
        ],
        primary_authority=[
            "Kubernetes Resource Quotas",
            "AWS Service Limits",
            "Google SRE Book"
        ],
        burden_holder="Infrastructure Engineering",
        adversary_position="Quota monitoring adds operational overhead.",
        counter_arguments=[
            "Automation reduces manual effort.",
            "Dashboards provide actionable insights."
        ],
        resolution_strategy="Automate quota tracking and integrate with resource optimization tools.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Kubernetes Resource Quota Monitoring"
    ),
    DoctrineBlock(
        topic="service_dependency_health",
        keywords=["service dependency", "health", "upstream", "downstream", "failure isolation"],
        conclusion_template="Service dependency health monitoring isolates failures and enables rapid remediation.",
        reasoning_framework="""
Service dependency health involves monitoring upstream and downstream relationships, failure isolation, and remediation readiness. The reasoning is to prevent cascading failures, enable rapid remediation, and maintain service contracts. Key factors include dependency mapping, health checks, and isolation mechanisms. Challenges include complex graphs, version drift, and isolation complexity. Solutions involve automation, service mesh integration, and dashboard visibility.
""",
        key_factors=[
            "Dependency mapping",
            "Health checks",
            "Isolation mechanisms",
            "Remediation readiness",
            "Dashboard visibility"
        ],
        primary_authority=[
            "Istio Service Mesh",
            "AWS Dependency Management",
            "Google SRE Book"
        ],
        burden_holder="Service Owner",
        adversary_position="Complex dependency graphs increase operational risk.",
        counter_arguments=[
            "Automated tools simplify dependency tracking.",
            "Service mesh provides centralized control."
        ],
        resolution_strategy="Adopt service mesh and automate dependency tracking.",
        entity_scope="Microservices, Distributed Systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Istio Dependency Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_scaling_health",
        keywords=["service scaling", "health", "autoscaling", "capacity", "performance"],
        conclusion_template="Service scaling health monitoring ensures optimal performance and prevents resource exhaustion.",
        reasoning_framework="""
Service scaling health involves monitoring autoscaling events, capacity, and performance. The reasoning is to ensure optimal performance, prevent resource exhaustion, and enable rapid scaling. Key factors include real-time tracking, alerting, and integration with capacity planning. Challenges include scaling delays, noisy neighbors, and capacity drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Autoscaling event tracking",
            "Capacity monitoring",
            "Performance measurement",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS Autoscaling",
            "Google SRE Book",
            "Microsoft Azure Scaling"
        ],
        burden_holder="Infrastructure Engineering",
        adversary_position="Scaling health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate scaling health checks and integrate with dashboards.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Autoscaling Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_latency_health",
        keywords=["service latency", "health", "performance", "monitoring", "optimization"],
        conclusion_template="Service latency health monitoring enables rapid detection and optimization of performance bottlenecks.",
        reasoning_framework="""
Service latency health involves monitoring performance, detecting bottlenecks, and optimizing response times. The reasoning is to ensure rapid detection, enable optimization, and maintain user experience. Key factors include real-time tracking, alerting, and integration with incident response. Challenges include scaling, noisy neighbors, and latency drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Performance monitoring",
            "Bottleneck detection",
            "Optimization",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "Datadog Latency Monitoring",
            "AWS Performance Insights",
            "Google SRE Book"
        ],
        burden_holder="Product Engineering",
        adversary_position="Latency health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate latency health checks and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Datadog Latency Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_error_health",
        keywords=["service error", "health", "error rate", "monitoring", "remediation"],
        conclusion_template="Service error health monitoring enables rapid detection and remediation of failures.",
        reasoning_framework="""
Service error health involves monitoring error rates, detecting failures, and enabling remediation. The reasoning is to ensure rapid detection, enable remediation, and maintain reliability. Key factors include real-time tracking, alerting, and integration with incident response. Challenges include scaling, noisy neighbors, and error drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Error rate monitoring",
            "Failure detection",
            "Remediation",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS CloudWatch Errors",
            "Google SRE Book",
            "Microsoft Azure Error Monitoring"
        ],
        burden_holder="Product Engineering",
        adversary_position="Error health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate error health checks and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CloudWatch Error Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_availability_health",
        keywords=["service availability", "health", "uptime", "monitoring", "SLA"],
        conclusion_template="Service availability health monitoring ensures uptime and compliance with SLAs.",
        reasoning_framework="""
Service availability health involves monitoring uptime, compliance with SLAs, and rapid detection of outages. The reasoning is to ensure uptime, enable compliance, and maintain reliability. Key factors include real-time tracking, alerting, and integration with incident response. Challenges include scaling, noisy neighbors, and availability drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Uptime monitoring",
            "SLA compliance",
            "Outage detection",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS CloudWatch Availability",
            "Google SRE Book",
            "Microsoft Azure Availability Monitoring"
        ],
        burden_holder="Product Engineering",
        adversary_position="Availability health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate availability health checks and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CloudWatch Availability Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_saturation_health",
        keywords=["service saturation", "health", "resource usage", "monitoring", "optimization"],
        conclusion_template="Service saturation health monitoring prevents resource exhaustion and enables optimization.",
        reasoning_framework="""
Service saturation health involves monitoring resource usage, preventing exhaustion, and enabling optimization. The reasoning is to ensure optimal performance, prevent outages, and maintain reliability. Key factors include real-time tracking, alerting, and integration with capacity planning. Challenges include scaling, noisy neighbors, and saturation drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Resource usage monitoring",
            "Exhaustion prevention",
            "Optimization",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS CloudWatch Saturation",
            "Google SRE Book",
            "Microsoft Azure Saturation Monitoring"
        ],
        burden_holder="Infrastructure Engineering",
        adversary_position="Saturation health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate saturation health checks and integrate with dashboards.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CloudWatch Saturation Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_traffic_health",
        keywords=["service traffic", "health", "monitoring", "usage", "optimization"],
        conclusion_template="Service traffic health monitoring enables optimization and rapid detection of usage anomalies.",
        reasoning_framework="""
Service traffic health involves monitoring usage, detecting anomalies, and enabling optimization. The reasoning is to ensure optimal performance, prevent outages, and maintain reliability. Key factors include real-time tracking, alerting, and integration with incident response. Challenges include scaling, noisy neighbors, and traffic drift. Solutions involve automation, dashboards, and periodic review.
""",
        key_factors=[
            "Usage monitoring",
            "Anomaly detection",
            "Optimization",
            "Alerting",
            "Dashboard visibility"
        ],
        primary_authority=[
            "AWS CloudWatch Traffic",
            "Google SRE Book",
            "Microsoft Azure Traffic Monitoring"
        ],
        burden_holder="Product Engineering",
        adversary_position="Traffic health checks may generate false positives.",
        counter_arguments=[
            "Threshold tuning reduces false positives.",
            "Automation enables rapid response."
        ],
        resolution_strategy="Automate traffic health checks and integrate with dashboards.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CloudWatch Traffic Health Monitoring"
    ),
    DoctrineBlock(
        topic="service_health_dashboard",
        keywords=["service health", "dashboard", "monitoring", "visibility", "reporting"],
        conclusion_template="Service health dashboards provide centralized visibility and actionable insights for operators.",
        reasoning_framework="""
Service health dashboards aggregate monitoring metrics, provide centralized visibility, and enable rapid incident response. The reasoning is to ensure operators have actionable insights, maintain reliability, and optimize performance. Key factors include real-time updates, alert integration, and customizable views. Challenges include scaling, data volume, and dashboard drift. Solutions involve automation, periodic review, and user feedback.
""",
        key_factors=[
            "Centralized visibility",
            "Real-time updates",
            "Alert integration",
            "Customizable views",
            "Periodic review"
        ],
        primary_authority=[
            "Datadog Dashboards",
            "AWS CloudWatch Dashboards",
            "Google SRE Book"
        ],
        burden_holder="Observability Engineering",
        adversary_position="Dashboards may become cluttered and lose actionable value.",
        counter_arguments=[
            "Periodic review ensures dashboards remain relevant.",
            "User feedback maintains actionable insights."
        ],
        resolution_strategy="Automate dashboard updates and review content regularly.",
        entity_scope="Distributed Systems, Cloud Infrastructure",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Datadog Service Health Dashboards"
    ),
    DoctrineBlock(
        topic="service_health_alerting",
        keywords=["service health", "alerting", "monitoring", "incident response", "automation"],
        conclusion_template="Service health alerting enables rapid incident response and minimizes downtime.",
        reasoning_framework="""
Service health alerting involves automated notifications based on monitoring metrics, enabling rapid incident response and minimizing downtime. The reasoning is to ensure operators are informed, maintain reliability, and optimize performance. Key factors include real-time alerts, escalation policies, and integration with incident management. Challenges include alert fatigue, scaling, and alert drift. Solutions involve automation, periodic review, and user feedback.
""",
        key_factors=[
            "Real-time alerts",
            "Escalation policies",
            "Incident management integration",
            "Automation",
            "Periodic review"
        ],
        primary_authority=[
            "PagerDuty Alerting",
            "AWS CloudWatch Alerts",
            "Google SRE Book"
        ],
        burden_holder="Operations Team",
        adversary_position="Alerting may generate noise and fatigue.",
        counter_arguments=[
            "Periodic review ensures actionable alerts.",
            "Escalation policies route critical incidents."
        ],
        resolution_strategy="Automate alerting and review configurations regularly.",
        entity_scope="Operations, SRE",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PagerDuty Service Health Alerting"
    ),
    DoctrineBlock(
        topic="service_health_remediation",
        keywords=["service health", "remediation", "automation", "incident response", "recovery"],
        conclusion_template="Automated service health remediation accelerates recovery and reduces operational toil.",
        reasoning_framework="""
Service health remediation involves automated workflows to recover from incidents, accelerate recovery, and reduce operational toil. The reasoning is to ensure rapid response, maintain reliability, and optimize performance. Key factors include automation, rollback readiness, and integration with incident management. Challenges include scaling, remediation drift, and loss of situational awareness. Solutions involve automation, periodic review, and user feedback.
""",
        key_factors=[
            "Automation",
            "Rollback readiness",
            "Incident management integration",
            "Periodic review",
            "User feedback"
        ],
        primary_authority=[
            "AWS Systems Manager Automation",
            "PagerDuty Remediation",
            "Google SRE Book"
        ],
        burden_holder="Operations Team",
        adversary_position="Automation may hide critical steps and reduce situational awareness.",
        counter_arguments=[
            "Periodic review ensures transparency.",
            "Manual overrides maintain control."
        ],
        resolution_strategy="Automate remediation workflows and maintain manual review for complex incidents.",
        entity_scope="Operations, SRE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Systems Manager Remediation"
    ),
    DoctrineBlock(
        topic="service_health_reporting",
        keywords=["service health", "reporting", "monitoring", "visibility", "compliance"],
        conclusion_template="Service health reporting ensures compliance, visibility, and informs business decisions.",
        reasoning_framework="""
Service health reporting involves automated generation of compliance, visibility, and business decision metrics. The reasoning is to ensure obligations are met, maintain reliability, and optimize performance. Key factors include automation, dashboard integration, and periodic review. Challenges include scaling, reporting drift, and data volume. Solutions involve automation, dashboards, and user feedback.
""",
        key_factors=[
            "Automation",
            "Dashboard integration",
            "Compliance metrics",
            "Periodic review",
            "User feedback"
        ],
        primary_authority=[
            "AWS CloudWatch Reporting",
            "Google SRE Book",
            "Microsoft Azure Reporting"
        ],
        burden_holder="Product Engineering",
        adversary_position="Reporting may miss subtle compliance breaches.",
        counter_arguments=[
            "Automation increases accuracy.",
            "Periodic review ensures coverage."
        ],
        resolution_strategy="Automate reporting and review content regularly.",
        entity_scope="Cloud Services, APIs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS CloudWatch Health Reporting"
    ),
    DoctrineBlock(
        topic="service_health_compliance",
        keywords=["service health", "compliance", "monitoring", "reporting", "regulation"],
        conclusion_template="Service health compliance monitoring ensures regulatory obligations are met and informs business decisions.",
        reasoning_framework="""
Service health compliance monitoring involves tracking regulatory obligations, reporting, and informing business decisions. The reasoning is to ensure compliance, maintain reliability, and optimize performance. Key factors include automation, dashboard integration, and periodic review. Challenges include scaling, compliance drift, and evolving regulations. Solutions involve automation, dashboards, and user feedback.
""",
        key_factors=[
            "Regulatory tracking",
            "Reporting",
            "Dashboard integration",
            "Periodic review",
            "User feedback"
        ],
        primary_authority=[
            "AWS Compliance Monitoring",
            "Google SRE Book",
            "Microsoft Azure Compliance"
        ],
        burden_holder="Compliance Team",
        adversary_position="Compliance monitoring adds operational overhead.",
        counter_arguments=[
            "Automation reduces manual effort.",
            "Dashboards provide actionable insights."
        ],
        resolution_strategy="Automate compliance tracking and integrate with dashboards.",
        entity_scope="Cloud Infrastructure, Distributed Systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AWS Compliance Health Monitoring"
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