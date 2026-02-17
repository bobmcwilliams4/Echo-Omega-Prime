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
        topic="Service Restart Taxonomy: Graceful vs. Forced",
        keywords=["service restart", "graceful", "forced", "taxonomy", "process termination"],
        conclusion_template="When a service fails, a graceful restart is preferred unless the process is unresponsive, in which case a forced restart is justified.",
        reasoning_framework="""
        1. Assess the service's responsiveness via health checks and IPC signals.
        2. If the service responds to SIGTERM, initiate a graceful shutdown to allow resource cleanup.
        3. If the service does not respond within the defined timeout, escalate to SIGKILL for forced termination.
        4. Log the restart type and reason for auditability.
        5. Consider the impact on dependent services and stateful resources.
        6. Prefer graceful restarts to minimize state corruption and data loss.
        7. Forced restarts are only justified when service is in a hung or zombie state.
        8. Document the restart taxonomy in operational runbooks.
        """,
        key_factors=[
            "Service responsiveness",
            "Timeout thresholds",
            "Resource cleanup requirements",
            "Downstream dependencies",
            "Audit logging"
        ],
        primary_authority=[
            "GS02 Engine Operational Manual",
            "RFC 8620 (Graceful Service Termination)"
        ],
        burden_holder="Recovery Operator",
        adversary_position="Forced restarts should be the default for speed.",
        counter_arguments=[
            "Forced restarts risk data corruption.",
            "Graceful restarts maintain service integrity."
        ],
        resolution_strategy="Default to graceful restart; escalate to forced only after timeout.",
        entity_scope="All managed services",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RESTART-01"
    ),
    DoctrineBlock(
        topic="Rollback Procedure Generation: Automated vs. Manual",
        keywords=["rollback", "procedure", "automation", "manual intervention", "change management"],
        conclusion_template="Automated rollback procedures should be generated for all deployable artifacts, with manual rollback reserved for exceptional cases.",
        reasoning_framework="""
        1. For every deployment, generate a rollback plan as part of the CI/CD pipeline.
        2. Automated rollback scripts must be tested in staging environments.
        3. Manual rollback is only invoked when automation fails or in cases of complex stateful migrations.
        4. Maintain versioned rollback scripts alongside deployment artifacts.
        5. Document rollback triggers and decision criteria.
        6. Ensure rollback procedures are idempotent and reversible.
        7. Train operators on manual rollback for edge cases.
        """,
        key_factors=[
            "Deployment artifact versioning",
            "Rollback script reliability",
            "Operator training",
            "Change management policies"
        ],
        primary_authority=[
            "GS02 Recovery Playbook",
            "ITIL Change Management Guidelines"
        ],
        burden_holder="Deployment Engineer",
        adversary_position="Manual rollback is more reliable due to human oversight.",
        counter_arguments=[
            "Automation reduces human error.",
            "Manual rollback is slower and riskier in high-availability scenarios."
        ],
        resolution_strategy="Automate rollback by default; manual only for exceptions.",
        entity_scope="All deployment pipelines",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-ROLLBACK-03"
    ),
    DoctrineBlock(
        topic="Retry Logic Patterns: Exponential Backoff",
        keywords=["retry", "logic", "exponential backoff", "transient failure", "rate limiting"],
        conclusion_template="Exponential backoff should be used for retrying transient failures to avoid overwhelming dependent systems.",
        reasoning_framework="""
        1. Identify transient errors (e.g., network timeouts, 5xx responses).
        2. Implement exponential backoff with jitter to randomize retry intervals.
        3. Set a maximum retry limit to prevent infinite loops.
        4. Log each retry attempt and its outcome.
        5. Monitor for patterns of repeated failures indicating systemic issues.
        6. Avoid fixed-interval retries which can cause thundering herd problems.
        7. Document retry policies for each integration point.
        """,
        key_factors=[
            "Error classification",
            "Retry interval calculation",
            "Maximum retry limits",
            "Logging and observability"
        ],
        primary_authority=[
            "GS02 Integration Standards",
            "AWS Architecture Best Practices"
        ],
        burden_holder="Application Developer",
        adversary_position="Immediate retries maximize uptime.",
        counter_arguments=[
            "Immediate retries can cause cascading failures.",
            "Backoff reduces load on failing systems."
        ],
        resolution_strategy="Adopt exponential backoff with jitter for all transient retries.",
        entity_scope="All external integrations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="GS02-2020-RETRY-02"
    ),
    DoctrineBlock(
        topic="Configuration Repair Patterns: Last Known Good",
        keywords=["configuration", "repair", "last known good", "rollback", "state recovery"],
        conclusion_template="Upon configuration corruption, revert to the last known good configuration snapshot to restore service.",
        reasoning_framework="""
        1. Maintain periodic snapshots of validated configurations.
        2. Upon detection of corruption, identify the most recent valid snapshot.
        3. Validate the snapshot against current system requirements.
        4. Apply the snapshot and restart affected services.
        5. Audit and log the repair action.
        6. Analyze root cause to prevent recurrence.
        7. Notify stakeholders of configuration rollback.
        """,
        key_factors=[
            "Snapshot frequency",
            "Validation procedures",
            "Audit logging",
            "Stakeholder notification"
        ],
        primary_authority=[
            "GS02 Configuration Management Policy",
            "NIST SP 800-53 CM-3"
        ],
        burden_holder="System Administrator",
        adversary_position="Manual configuration repair is more precise.",
        counter_arguments=[
            "Manual repair is error-prone.",
            "Snapshots ensure rapid, consistent recovery."
        ],
        resolution_strategy="Default to last known good snapshot; escalate if snapshot is invalid.",
        entity_scope="All managed configurations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CONFIG-04"
    ),
    DoctrineBlock(
        topic="Dependency Resolution Strategies: Service Graph Traversal",
        keywords=["dependency", "resolution", "service graph", "traversal", "topology"],
        conclusion_template="Resolve dependencies using service graph traversal to ensure correct recovery order.",
        reasoning_framework="""
        1. Model service dependencies as a directed acyclic graph (DAG).
        2. Upon failure, traverse the graph to identify upstream and downstream dependencies.
        3. Recover upstream dependencies before dependent services.
        4. Validate dependency health before proceeding with recovery.
        5. Document the service graph and update as architecture evolves.
        6. Automate traversal and recovery sequencing.
        """,
        key_factors=[
            "Graph accuracy",
            "Dependency health checks",
            "Traversal automation",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Service Dependency Registry",
            "TOGAF 9.2"
        ],
        burden_holder="Recovery Automation System",
        adversary_position="Flat dependency lists are sufficient.",
        counter_arguments=[
            "Flat lists miss complex relationships.",
            "Graphs enable precise recovery sequencing."
        ],
        resolution_strategy="Use DAG-based traversal for all dependency resolutions.",
        entity_scope="All service dependencies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2021-DEP-01"
    ),
    DoctrineBlock(
        topic="Database Recovery Procedures: Point-in-Time Restore",
        keywords=["database", "recovery", "point-in-time", "restore", "backup"],
        conclusion_template="Point-in-time restore should be the default database recovery procedure to minimize data loss.",
        reasoning_framework="""
        1. Maintain continuous backup streams for all production databases.
        2. Upon failure, determine the last consistent backup before the incident.
        3. Restore to the identified point-in-time, verifying data integrity.
        4. Validate application functionality post-restore.
        5. Document the recovery window and any data loss.
        6. Notify affected users and stakeholders.
        7. Analyze root cause and update backup policies as needed.
        """,
        key_factors=[
            "Backup frequency",
            "Restore validation",
            "Data integrity",
            "Stakeholder communication"
        ],
        primary_authority=[
            "GS02 Database Operations Manual",
            "ISO/IEC 27040"
        ],
        burden_holder="Database Administrator",
        adversary_position="Full restore is faster and simpler.",
        counter_arguments=[
            "Full restore increases data loss.",
            "Point-in-time minimizes impact."
        ],
        resolution_strategy="Default to point-in-time restore; full restore only if PIT is unavailable.",
        entity_scope="All production databases",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="GS02-2022-DB-02"
    ),
    DoctrineBlock(
        topic="File System Repair Procedures: Journaling Replay",
        keywords=["file system", "repair", "journaling", "replay", "consistency"],
        conclusion_template="File system repairs must begin with journaling replay to restore consistency before deeper repairs.",
        reasoning_framework="""
        1. Detect file system inconsistencies via fsck or equivalent tools.
        2. Initiate journaling replay to recover from incomplete transactions.
        3. Validate file system state post-replay.
        4. If inconsistencies persist, escalate to block-level recovery.
        5. Document all repair actions for audit.
        6. Notify system owners of repair status.
        """,
        key_factors=[
            "Journaling support",
            "Tool reliability",
            "Audit trails",
            "Owner notification"
        ],
        primary_authority=[
            "GS02 Storage Management Guide",
            "EXT4/NTFS Journaling Specifications"
        ],
        burden_holder="Storage Engineer",
        adversary_position="Direct block repair is faster.",
        counter_arguments=[
            "Skipping journaling risks further corruption.",
            "Replay is safer and preserves data."
        ],
        resolution_strategy="Always replay journal before other repairs.",
        entity_scope="All journaled file systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GS02-2020-FS-01"
    ),
    DoctrineBlock(
        topic="Network Recovery Procedures: Route Recalculation",
        keywords=["network", "recovery", "route recalculation", "routing table", "failover"],
        conclusion_template="Upon network failure, recalculate routing tables to restore connectivity before escalating to hardware checks.",
        reasoning_framework="""
        1. Detect network partition or loss of connectivity.
        2. Trigger dynamic routing protocol recalculation (e.g., OSPF, BGP).
        3. Validate restored routes and end-to-end connectivity.
        4. If routes remain unavailable, escalate to hardware diagnostics.
        5. Document recovery steps and outcomes.
        6. Notify network operations center.
        """,
        key_factors=[
            "Routing protocol configuration",
            "Detection latency",
            "Hardware escalation procedures",
            "NOC communication"
        ],
        primary_authority=[
            "GS02 Network Operations Handbook",
            "RFC 2328 (OSPFv2)"
        ],
        burden_holder="Network Engineer",
        adversary_position="Immediate hardware checks are more thorough.",
        counter_arguments=[
            "Software faults are more common than hardware.",
            "Route recalculation is faster and less disruptive."
        ],
        resolution_strategy="Recalculate routes first; escalate only if unresolved.",
        entity_scope="All managed networks",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GS02-2021-NET-03"
    ),
    DoctrineBlock(
        topic="Cache Invalidation Strategies: Time-to-Live (TTL)",
        keywords=["cache", "invalidation", "ttl", "expiration", "consistency"],
        conclusion_template="Caches should implement TTL-based invalidation to ensure data freshness and prevent stale reads.",
        reasoning_framework="""
        1. Assign TTL values based on data volatility and business requirements.
        2. On TTL expiry, evict or refresh cached entries.
        3. Monitor cache hit/miss rates to tune TTL values.
        4. Document cache invalidation policies.
        5. For critical data, consider event-driven invalidation in addition to TTL.
        6. Ensure application logic handles cache misses gracefully.
        """,
        key_factors=[
            "Data volatility",
            "TTL configuration",
            "Monitoring metrics",
            "Application logic"
        ],
        primary_authority=[
            "GS02 Caching Standards",
            "Google Cache Design Patterns"
        ],
        burden_holder="Application Architect",
        adversary_position="Manual cache clearing is more reliable.",
        counter_arguments=[
            "Manual clearing is error-prone and slow.",
            "TTL ensures consistent freshness."
        ],
        resolution_strategy="Implement TTL for all cache layers; supplement with events as needed.",
        entity_scope="All application caches",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CACHE-01"
    ),
    DoctrineBlock(
        topic="Queue Drain Procedures: Graceful vs. Immediate",
        keywords=["queue", "drain", "graceful", "immediate", "message processing"],
        conclusion_template="Queues should be drained gracefully to allow in-flight messages to complete, except in emergency scenarios.",
        reasoning_framework="""
        1. Identify the queue and its consumers.
        2. Signal consumers to stop accepting new messages.
        3. Allow in-flight messages to complete processing.
        4. Monitor queue depth until empty.
        5. For emergencies, provide an immediate drain option with message loss risk.
        6. Document the drain procedure and rationale.
        """,
        key_factors=[
            "Queue type",
            "Message criticality",
            "Consumer behavior",
            "Emergency procedures"
        ],
        primary_authority=[
            "GS02 Messaging Operations Guide",
            "AMQP 1.0 Specification"
        ],
        burden_holder="Queue Administrator",
        adversary_position="Immediate drain is faster and reduces downtime.",
        counter_arguments=[
            "Graceful drain preserves data integrity.",
            "Immediate drain risks message loss."
        ],
        resolution_strategy="Default to graceful drain; immediate only for emergencies.",
        entity_scope="All managed queues",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2021-QUEUE-02"
    ),
    DoctrineBlock(
        topic="Service Restart Taxonomy: Rolling Restarts",
        keywords=["service restart", "rolling", "high availability", "zero downtime"],
        conclusion_template="Rolling restarts should be used for clustered services to maintain availability during recovery.",
        reasoning_framework="""
        1. Identify services with multiple instances or nodes.
        2. Restart instances sequentially, ensuring quorum is maintained.
        3. Monitor service health after each restart.
        4. Roll back if health checks fail.
        5. Document the restart sequence and outcomes.
        6. Use orchestration tools to automate rolling restarts.
        """,
        key_factors=[
            "Cluster configuration",
            "Health check reliability",
            "Quorum requirements",
            "Automation tools"
        ],
        primary_authority=[
            "GS02 High Availability Guide",
            "Kubernetes RollingUpdate Policy"
        ],
        burden_holder="Site Reliability Engineer",
        adversary_position="Restarting all nodes at once is faster.",
        counter_arguments=[
            "Simultaneous restarts cause downtime.",
            "Rolling restarts preserve service availability."
        ],
        resolution_strategy="Use rolling restarts for all HA services.",
        entity_scope="Clustered services",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RESTART-04"
    ),
    DoctrineBlock(
        topic="Rollback Procedure Generation: Pre-Deployment Validation",
        keywords=["rollback", "pre-deployment", "validation", "testing"],
        conclusion_template="Rollback procedures must be validated in staging before production deployment.",
        reasoning_framework="""
        1. For each deployment, execute rollback scripts in a staging environment.
        2. Verify that rollback returns the system to the pre-deployment state.
        3. Document any discrepancies or failures.
        4. Block production deployment if rollback validation fails.
        5. Update rollback scripts based on test outcomes.
        """,
        key_factors=[
            "Staging environment fidelity",
            "Rollback script coverage",
            "Documentation",
            "Deployment gating"
        ],
        primary_authority=[
            "GS02 Deployment Standards",
            "Continuous Delivery Foundation"
        ],
        burden_holder="Release Manager",
        adversary_position="Rollback validation slows down releases.",
        counter_arguments=[
            "Validation prevents production outages.",
            "Unvalidated rollbacks may fail in emergencies."
        ],
        resolution_strategy="Enforce rollback validation as a release gate.",
        entity_scope="All production deployments",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-ROLLBACK-05"
    ),
    DoctrineBlock(
        topic="Retry Logic Patterns: Circuit Breaker Integration",
        keywords=["retry", "circuit breaker", "failure isolation", "resilience"],
        conclusion_template="Retry logic must integrate with circuit breakers to prevent repeated failures from cascading.",
        reasoning_framework="""
        1. Wrap retry logic with circuit breaker patterns.
        2. On repeated failures, open the circuit to block further retries.
        3. Allow for periodic probe attempts to test recovery.
        4. Log circuit breaker state changes.
        5. Alert operators when circuits open or close.
        6. Tune thresholds based on historical failure rates.
        """,
        key_factors=[
            "Failure thresholds",
            "Probe intervals",
            "Alerting integration",
            "Historical analysis"
        ],
        primary_authority=[
            "GS02 Resilience Patterns",
            "Netflix Hystrix Documentation"
        ],
        burden_holder="Application Developer",
        adversary_position="Retries should always be attempted.",
        counter_arguments=[
            "Unbounded retries can overload dependencies.",
            "Circuit breakers isolate faults."
        ],
        resolution_strategy="Integrate circuit breakers with all retry logic.",
        entity_scope="All external service calls",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RETRY-04"
    ),
    DoctrineBlock(
        topic="Configuration Repair Patterns: Automated Consistency Checks",
        keywords=["configuration", "repair", "automation", "consistency check"],
        conclusion_template="Automated consistency checks should run periodically to detect and repair configuration drift.",
        reasoning_framework="""
        1. Schedule periodic configuration audits using automated tools.
        2. Compare current state to baseline configurations.
        3. Detect and log any drift or unauthorized changes.
        4. Automatically revert to baseline or alert operators for manual review.
        5. Document all detected drifts and repair actions.
        6. Integrate with change management for traceability.
        """,
        key_factors=[
            "Audit frequency",
            "Tool reliability",
            "Change management integration",
            "Drift remediation"
        ],
        primary_authority=[
            "GS02 Configuration Audit Policy",
            "CIS Controls v8"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Manual checks are more thorough.",
        counter_arguments=[
            "Manual checks are slow and inconsistent.",
            "Automation ensures continuous compliance."
        ],
        resolution_strategy="Automate configuration audits and repairs.",
        entity_scope="All managed systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2021-CONFIG-07"
    ),
    DoctrineBlock(
        topic="Dependency Resolution Strategies: Version Pinning",
        keywords=["dependency", "resolution", "version pinning", "compatibility"],
        conclusion_template="Pin dependency versions to prevent incompatibility during recovery operations.",
        reasoning_framework="""
        1. Specify explicit versions for all critical dependencies.
        2. Test recovery procedures with pinned versions.
        3. Update dependency versions only after validation.
        4. Document version changes and rationale.
        5. Monitor for security advisories on pinned versions.
        """,
        key_factors=[
            "Version specification",
            "Testing coverage",
            "Documentation",
            "Security monitoring"
        ],
        primary_authority=[
            "GS02 Dependency Management Policy",
            "Semantic Versioning Specification"
        ],
        burden_holder="Build Engineer",
        adversary_position="Latest versions should always be used.",
        counter_arguments=[
            "Unpinned versions can break recovery.",
            "Pinning ensures repeatability."
        ],
        resolution_strategy="Pin versions for all critical dependencies.",
        entity_scope="All recovery scripts and tools",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GS02-2020-DEP-03"
    ),
    DoctrineBlock(
        topic="Database Recovery Procedures: Write-Ahead Logging (WAL)",
        keywords=["database", "recovery", "write-ahead logging", "wal", "consistency"],
        conclusion_template="Databases must use WAL to ensure recoverability from crashes and power failures.",
        reasoning_framework="""
        1. Enable WAL on all transactional databases.
        2. On crash, replay WAL to restore consistent state.
        3. Monitor WAL size and rotation.
        4. Archive WAL segments for point-in-time recovery.
        5. Validate recovery via test restores.
        6. Document WAL policies and retention.
        """,
        key_factors=[
            "WAL configuration",
            "Monitoring",
            "Archival procedures",
            "Test restores"
        ],
        primary_authority=[
            "GS02 Database Recovery Guide",
            "PostgreSQL WAL Documentation"
        ],
        burden_holder="Database Administrator",
        adversary_position="WAL adds unnecessary overhead.",
        counter_arguments=[
            "WAL is essential for durability.",
            "Overhead is minimal compared to benefits."
        ],
        resolution_strategy="Require WAL for all transactional databases.",
        entity_scope="Transactional databases",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="GS02-2021-DB-04"
    ),
    DoctrineBlock(
        topic="File System Repair Procedures: Snapshot-Based Recovery",
        keywords=["file system", "repair", "snapshot", "recovery", "backup"],
        conclusion_template="Use file system snapshots for rapid recovery from corruption or accidental deletion.",
        reasoning_framework="""
        1. Schedule regular snapshots for all critical file systems.
        2. On detection of corruption or data loss, identify the latest valid snapshot.
        3. Restore affected files or volumes from the snapshot.
        4. Validate data integrity post-restore.
        5. Document recovery actions and outcomes.
        6. Notify affected users.
        """,
        key_factors=[
            "Snapshot frequency",
            "Restore validation",
            "Documentation",
            "User notification"
        ],
        primary_authority=[
            "GS02 Storage Operations Manual",
            "ZFS Snapshot Documentation"
        ],
        burden_holder="Storage Administrator",
        adversary_position="Manual file recovery is more targeted.",
        counter_arguments=[
            "Snapshots enable rapid, consistent recovery.",
            "Manual recovery is slow and error-prone."
        ],
        resolution_strategy="Default to snapshot-based recovery for all file systems.",
        entity_scope="All critical file systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2022-FS-02"
    ),
    DoctrineBlock(
        topic="Network Recovery Procedures: DNS Failover",
        keywords=["network", "recovery", "dns", "failover", "high availability"],
        conclusion_template="DNS failover must be configured for all critical endpoints to ensure rapid recovery from network outages.",
        reasoning_framework="""
        1. Register multiple IP addresses for critical DNS records.
        2. Configure health checks for all endpoints.
        3. On failure, update DNS records to point to healthy endpoints.
        4. Set low TTL values for rapid propagation.
        5. Monitor DNS changes and validate failover.
        6. Document DNS failover procedures.
        """,
        key_factors=[
            "DNS configuration",
            "Health check reliability",
            "TTL settings",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Network Resilience Policy",
            "RFC 1034 (DNS Concepts)"
        ],
        burden_holder="Network Operations",
        adversary_position="Manual DNS changes are more controlled.",
        counter_arguments=[
            "Manual changes are slow.",
            "Automated failover ensures high availability."
        ],
        resolution_strategy="Automate DNS failover for all critical endpoints.",
        entity_scope="Critical network endpoints",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-NET-06"
    ),
    DoctrineBlock(
        topic="Cache Invalidation Strategies: Event-Driven Invalidation",
        keywords=["cache", "invalidation", "event-driven", "consistency"],
        conclusion_template="Event-driven cache invalidation should supplement TTL to ensure consistency for rapidly changing data.",
        reasoning_framework="""
        1. Identify data sources with high update frequency.
        2. Emit invalidation events on data changes.
        3. Subscribe cache layers to invalidation events.
        4. On event receipt, evict or refresh affected cache entries.
        5. Monitor for missed events and reconcile discrepancies.
        6. Document event-driven invalidation policies.
        """,
        key_factors=[
            "Event source reliability",
            "Cache subscription mechanisms",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Caching Policy",
            "Redis Pub/Sub Documentation"
        ],
        burden_holder="Application Developer",
        adversary_position="TTL is sufficient for all use cases.",
        counter_arguments=[
            "TTL can allow stale reads.",
            "Events ensure immediate consistency."
        ],
        resolution_strategy="Combine event-driven invalidation with TTL.",
        entity_scope="Caches for dynamic data",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CACHE-03"
    ),
    DoctrineBlock(
        topic="Queue Drain Procedures: Poison Message Handling",
        keywords=["queue", "drain", "poison message", "error handling"],
        conclusion_template="Implement poison message handling to prevent stuck queues during drain procedures.",
        reasoning_framework="""
        1. Detect messages that repeatedly fail processing.
        2. Move poison messages to a quarantine or dead-letter queue.
        3. Continue draining the main queue.
        4. Alert operators for manual inspection of poison messages.
        5. Document poison message handling and outcomes.
        """,
        key_factors=[
            "Failure detection",
            "Dead-letter queue configuration",
            "Operator alerting",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Messaging Standards",
            "AWS SQS Dead-Letter Queues"
        ],
        burden_holder="Queue Administrator",
        adversary_position="All messages should be retried indefinitely.",
        counter_arguments=[
            "Indefinite retries block queue progress.",
            "Poison handling isolates problematic messages."
        ],
        resolution_strategy="Implement dead-letter queues for all message queues.",
        entity_scope="All message queues",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-QUEUE-04"
    ),
    DoctrineBlock(
        topic="Service Restart Taxonomy: Dependency-Aware Restarts",
        keywords=["service restart", "dependency-aware", "orchestration"],
        conclusion_template="Service restarts must respect dependency order to prevent cascading failures.",
        reasoning_framework="""
        1. Identify service dependencies via service registry.
        2. Restart upstream dependencies before dependent services.
        3. Validate health after each restart.
        4. Document restart order and rationale.
        5. Use orchestration tools to automate dependency-aware restarts.
        """,
        key_factors=[
            "Dependency mapping",
            "Health checks",
            "Orchestration tools",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Service Orchestration Policy",
            "HashiCorp Consul Documentation"
        ],
        burden_holder="Site Reliability Engineer",
        adversary_position="Restart order is irrelevant.",
        counter_arguments=[
            "Incorrect order can cause failures.",
            "Dependency-aware restarts ensure stability."
        ],
        resolution_strategy="Automate dependency-aware restarts for all services.",
        entity_scope="All orchestrated services",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RESTART-06"
    ),
    DoctrineBlock(
        topic="Rollback Procedure Generation: State Reconciliation",
        keywords=["rollback", "state reconciliation", "data consistency"],
        conclusion_template="Rollback procedures must include state reconciliation to ensure data consistency post-rollback.",
        reasoning_framework="""
        1. Identify data changes made during failed deployment.
        2. Roll back code and configuration.
        3. Reconcile database and external system state to match rollback point.
        4. Validate application functionality.
        5. Document reconciliation steps and outcomes.
        """,
        key_factors=[
            "Change tracking",
            "Reconciliation scripts",
            "Validation procedures",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Rollback Standards",
            "ACID Transaction Principles"
        ],
        burden_holder="Release Manager",
        adversary_position="Code rollback is sufficient.",
        counter_arguments=[
            "State drift can cause subtle bugs.",
            "Reconciliation ensures true rollback."
        ],
        resolution_strategy="Include state reconciliation in all rollback procedures.",
        entity_scope="All production rollbacks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-ROLLBACK-07"
    ),
    DoctrineBlock(
        topic="Retry Logic Patterns: Idempotency Enforcement",
        keywords=["retry", "idempotency", "side effects"],
        conclusion_template="All retryable operations must be idempotent to prevent unintended side effects.",
        reasoning_framework="""
        1. Design APIs and operations to be idempotent by default.
        2. Use idempotency keys where applicable.
        3. Validate idempotency in integration tests.
        4. Document idempotency guarantees and limitations.
        5. Train developers on idempotent design patterns.
        """,
        key_factors=[
            "API design",
            "Key management",
            "Testing",
            "Developer training"
        ],
        primary_authority=[
            "GS02 API Standards",
            "RESTful API Design Guidelines"
        ],
        burden_holder="Application Developer",
        adversary_position="Retries are safe without idempotency.",
        counter_arguments=[
            "Non-idempotent retries can cause data corruption.",
            "Idempotency is essential for safe retries."
        ],
        resolution_strategy="Require idempotency for all retryable operations.",
        entity_scope="All APIs and integrations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RETRY-07"
    ),
    DoctrineBlock(
        topic="Configuration Repair Patterns: Immutable Infrastructure",
        keywords=["configuration", "repair", "immutable infrastructure", "reprovisioning"],
        conclusion_template="For severe configuration drift, reprovision immutable infrastructure rather than repairing in place.",
        reasoning_framework="""
        1. Detect severe configuration drift or corruption.
        2. Decommission affected instances.
        3. Reprovision from known-good images or templates.
        4. Validate new instances before rejoining service pool.
        5. Document reprovisioning actions.
        6. Update configuration baselines as needed.
        """,
        key_factors=[
            "Drift detection",
            "Image management",
            "Validation procedures",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Infrastructure Policy",
            "Immutable Infrastructure Principles"
        ],
        burden_holder="Infrastructure Engineer",
        adversary_position="In-place repair is faster.",
        counter_arguments=[
            "In-place repair can miss hidden issues.",
            "Immutable reprovisioning ensures consistency."
        ],
        resolution_strategy="Reprovision for severe drift; repair only for minor issues.",
        entity_scope="All infrastructure nodes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-CONFIG-10"
    ),
    DoctrineBlock(
        topic="Dependency Resolution Strategies: Service Discovery Integration",
        keywords=["dependency", "resolution", "service discovery", "dynamic topology"],
        conclusion_template="Integrate with service discovery systems to resolve dependencies in dynamic environments.",
        reasoning_framework="""
        1. Register all services with a discovery system.
        2. Query discovery system for current dependency endpoints.
        3. Update dependency graphs dynamically as topology changes.
        4. Validate endpoints before use.
        5. Document service discovery integration.
        """,
        key_factors=[
            "Discovery system reliability",
            "Endpoint validation",
            "Dynamic updates",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Service Discovery Policy",
            "Consul/Etcd Documentation"
        ],
        burden_holder="Platform Engineer",
        adversary_position="Static configuration is sufficient.",
        counter_arguments=[
            "Static config fails in dynamic environments.",
            "Discovery ensures up-to-date dependencies."
        ],
        resolution_strategy="Integrate service discovery for all dynamic dependencies.",
        entity_scope="Dynamic service environments",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2022-DEP-05"
    ),
    DoctrineBlock(
        topic="Database Recovery Procedures: Read Replica Promotion",
        keywords=["database", "recovery", "read replica", "promotion", "failover"],
        conclusion_template="Promote read replicas to primary during primary database failures to minimize downtime.",
        reasoning_framework="""
        1. Monitor replication lag and replica health.
        2. On primary failure, promote the healthiest replica.
        3. Redirect application traffic to new primary.
        4. Reconfigure remaining replicas to follow new primary.
        5. Document failover and promotion actions.
        6. Notify stakeholders of failover event.
        """,
        key_factors=[
            "Replication health",
            "Promotion automation",
            "Traffic redirection",
            "Stakeholder notification"
        ],
        primary_authority=[
            "GS02 Database HA Policy",
            "AWS RDS Failover Documentation"
        ],
        burden_holder="Database Administrator",
        adversary_position="Manual failover is more controlled.",
        counter_arguments=[
            "Manual failover increases downtime.",
            "Automated promotion ensures rapid recovery."
        ],
        resolution_strategy="Automate read replica promotion for all HA databases.",
        entity_scope="HA database clusters",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS02-2021-DB-07"
    ),
    DoctrineBlock(
        topic="File System Repair Procedures: Block-Level Recovery",
        keywords=["file system", "repair", "block-level", "recovery", "corruption"],
        conclusion_template="Escalate to block-level recovery only after logical and journaling repairs fail.",
        reasoning_framework="""
        1. Attempt logical repairs and journaling replay first.
        2. If inconsistencies persist, identify affected blocks.
        3. Use block-level tools to recover or reconstruct data.
        4. Validate file system integrity.
        5. Document block-level actions and outcomes.
        6. Notify system owners.
        """,
        key_factors=[
            "Repair escalation criteria",
            "Tool reliability",
            "Validation procedures",
            "Owner notification"
        ],
        primary_authority=[
            "GS02 Storage Recovery Guide",
            "Linux fsck Documentation"
        ],
        burden_holder="Storage Engineer",
        adversary_position="Block-level repair should be first.",
        counter_arguments=[
            "Block-level repair is risky and complex.",
            "Logical repairs are safer and faster."
        ],
        resolution_strategy="Escalate to block-level only when necessary.",
        entity_scope="All file systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GS02-2020-FS-05"
    ),
    DoctrineBlock(
        topic="Network Recovery Procedures: Automated Link Flapping Detection",
        keywords=["network", "recovery", "link flapping", "automation", "stability"],
        conclusion_template="Automate detection and isolation of flapping network links to prevent instability.",
        reasoning_framework="""
        1. Monitor link status for frequent up/down transitions.
        2. On detection, isolate affected links from routing tables.
        3. Alert network operators.
        4. Investigate root cause and remediate.
        5. Document flapping events and actions taken.
        """,
        key_factors=[
            "Monitoring granularity",
            "Isolation automation",
            "Operator alerting",
            "Root cause analysis"
        ],
        primary_authority=[
            "GS02 Network Monitoring Policy",
            "Cisco Network Stability Guidelines"
        ],
        burden_holder="Network Engineer",
        adversary_position="Manual detection is sufficient.",
        counter_arguments=[
            "Manual detection is slow.",
            "Automation prevents widespread instability."
        ],
        resolution_strategy="Automate link flapping detection and isolation.",
        entity_scope="All managed networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2021-NET-09"
    ),
    DoctrineBlock(
        topic="Cache Invalidation Strategies: Write-Through Caching",
        keywords=["cache", "invalidation", "write-through", "consistency"],
        conclusion_template="Write-through caching should be used when strong consistency is required.",
        reasoning_framework="""
        1. On write, update both cache and backing store synchronously.
        2. Ensure cache and store remain consistent.
        3. Monitor write latency and tune as needed.
        4. Document write-through caching policies.
        5. Use only for data requiring strong consistency.
        """,
        key_factors=[
            "Consistency requirements",
            "Latency monitoring",
            "Policy documentation",
            "Use case selection"
        ],
        primary_authority=[
            "GS02 Caching Standards",
            "Microsoft Write-Through Caching Whitepaper"
        ],
        burden_holder="Application Architect",
        adversary_position="Write-back caching is more performant.",
        counter_arguments=[
            "Write-back risks stale reads.",
            "Write-through ensures consistency."
        ],
        resolution_strategy="Use write-through for critical data; write-back for others.",
        entity_scope="Critical data caches",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CACHE-06"
    ),
    DoctrineBlock(
        topic="Queue Drain Procedures: Ordered Message Processing",
        keywords=["queue", "drain", "ordered processing", "message sequencing"],
        conclusion_template="Maintain message order during queue drain for systems requiring ordered processing.",
        reasoning_framework="""
        1. Identify queues with strict ordering requirements.
        2. Ensure consumers process messages in FIFO order.
        3. Avoid parallel processing that breaks order.
        4. Document ordering guarantees and limitations.
        5. Test drain procedures for ordering compliance.
        """,
        key_factors=[
            "Queue configuration",
            "Consumer design",
            "Testing",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Messaging Policy",
            "Kafka Ordering Guarantees"
        ],
        burden_holder="Queue Administrator",
        adversary_position="Parallel drain maximizes throughput.",
        counter_arguments=[
            "Order is critical for some systems.",
            "Throughput can be tuned within ordering constraints."
        ],
        resolution_strategy="Enforce ordering for queues with such requirements.",
        entity_scope="Ordered message queues",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-QUEUE-09"
    ),
    DoctrineBlock(
        topic="Service Restart Taxonomy: Health Check Integration",
        keywords=["service restart", "health check", "integration", "automation"],
        conclusion_template="Integrate health checks into restart procedures to verify service recovery.",
        reasoning_framework="""
        1. Define health check endpoints for all services.
        2. After restart, poll health checks until service is healthy.
        3. Alert operators if health checks fail post-restart.
        4. Document health check results and actions taken.
        5. Tune health check intervals and thresholds.
        """,
        key_factors=[
            "Health check coverage",
            "Alerting integration",
            "Documentation",
            "Threshold tuning"
        ],
        primary_authority=[
            "GS02 Service Health Policy",
            "Kubernetes Liveness/Readiness Probes"
        ],
        burden_holder="Site Reliability Engineer",
        adversary_position="Manual verification is sufficient.",
        counter_arguments=[
            "Automation speeds up detection.",
            "Manual checks are error-prone."
        ],
        resolution_strategy="Automate health check integration for all restarts.",
        entity_scope="All managed services",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RESTART-09"
    ),
    DoctrineBlock(
        topic="Rollback Procedure Generation: Automated Data Migration Reversal",
        keywords=["rollback", "data migration", "automation", "reversal"],
        conclusion_template="Automate reversal of data migrations as part of rollback procedures.",
        reasoning_framework="""
        1. Track all data migrations with versioned scripts.
        2. For each migration, provide a tested down-script.
        3. Automate execution of down-scripts during rollback.
        4. Validate data integrity after reversal.
        5. Document migration reversals and outcomes.
        """,
        key_factors=[
            "Migration tracking",
            "Down-script coverage",
            "Validation",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Migration Policy",
            "Flyway/Liquibase Documentation"
        ],
        burden_holder="Database Engineer",
        adversary_position="Manual reversal is more controlled.",
        counter_arguments=[
            "Manual reversal is slow and error-prone.",
            "Automation ensures consistency."
        ],
        resolution_strategy="Automate migration reversal for all rollbacks.",
        entity_scope="All data migrations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-ROLLBACK-10"
    ),
    DoctrineBlock(
        topic="Retry Logic Patterns: Rate Limiting Integration",
        keywords=["retry", "rate limiting", "integration", "throttling"],
        conclusion_template="Integrate retry logic with rate limiting to prevent overloading external systems.",
        reasoning_framework="""
        1. Implement rate limiting for all outbound requests.
        2. Coordinate retry logic with rate limit thresholds.
        3. On rate limit breach, back off and alert operators.
        4. Document rate limiting and retry policies.
        5. Monitor for excessive retries and adjust thresholds.
        """,
        key_factors=[
            "Rate limit configuration",
            "Retry coordination",
            "Alerting",
            "Monitoring"
        ],
        primary_authority=[
            "GS02 Integration Policy",
            "API Gateway Rate Limiting Docs"
        ],
        burden_holder="Application Developer",
        adversary_position="Retries should be independent of rate limits.",
        counter_arguments=[
            "Ignoring rate limits causes throttling.",
            "Integration prevents overload."
        ],
        resolution_strategy="Integrate rate limiting with all retry logic.",
        entity_scope="All external API calls",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RETRY-12"
    ),
    DoctrineBlock(
        topic="Configuration Repair Patterns: Drift Remediation Automation",
        keywords=["configuration", "repair", "drift", "automation", "remediation"],
        conclusion_template="Automate remediation of detected configuration drift to maintain system integrity.",
        reasoning_framework="""
        1. Continuously monitor for configuration drift.
        2. On detection, automatically revert to baseline or desired state.
        3. Alert operators for manual review if remediation fails.
        4. Document all drift and remediation actions.
        5. Integrate with change management for traceability.
        """,
        key_factors=[
            "Monitoring frequency",
            "Remediation reliability",
            "Alerting",
            "Change management integration"
        ],
        primary_authority=[
            "GS02 Configuration Management Policy",
            "Puppet/Chef/Ansible Docs"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Manual remediation is more precise.",
        counter_arguments=[
            "Manual remediation is slow.",
            "Automation ensures continuous compliance."
        ],
        resolution_strategy="Automate drift remediation for all managed systems.",
        entity_scope="All managed infrastructure",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-CONFIG-13"
    ),
    DoctrineBlock(
        topic="Dependency Resolution Strategies: Transitive Dependency Analysis",
        keywords=["dependency", "resolution", "transitive", "analysis"],
        conclusion_template="Analyze and resolve all transitive dependencies to prevent hidden failures during recovery.",
        reasoning_framework="""
        1. Enumerate direct and transitive dependencies for all services.
        2. Validate health and compatibility of all dependencies.
        3. Document dependency chains and update as architecture evolves.
        4. Automate transitive dependency analysis in CI/CD pipelines.
        """,
        key_factors=[
            "Dependency enumeration",
            "Compatibility validation",
            "Documentation",
            "Automation"
        ],
        primary_authority=[
            "GS02 Dependency Policy",
            "Maven/Gradle Transitive Dependency Docs"
        ],
        burden_holder="Build Engineer",
        adversary_position="Direct dependencies are sufficient.",
        counter_arguments=[
            "Transitive dependencies can cause hidden failures.",
            "Analysis prevents surprises during recovery."
        ],
        resolution_strategy="Automate transitive dependency analysis.",
        entity_scope="All service dependencies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="GS02-2022-DEP-08"
    ),
    DoctrineBlock(
        topic="Database Recovery Procedures: Automated Consistency Checks",
        keywords=["database", "recovery", "consistency check", "automation"],
        conclusion_template="Automate consistency checks post-recovery to ensure database integrity.",
        reasoning_framework="""
        1. After recovery, run automated consistency checks on all tables and indexes.
        2. Log and remediate any detected inconsistencies.
        3. Alert database administrators for manual review if needed.
        4. Document check results and remediation actions.
        """,
        key_factors=[
            "Check coverage",
            "Remediation automation",
            "Alerting",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Database Integrity Policy",
            "Oracle DBMS_REPAIR Docs"
        ],
        burden_holder="Database Administrator",
        adversary_position="Manual checks are more reliable.",
        counter_arguments=[
            "Manual checks are slow.",
            "Automation ensures rapid detection."
        ],
        resolution_strategy="Automate consistency checks for all recoveries.",
        entity_scope="All databases",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-DB-11"
    ),
    DoctrineBlock(
        topic="File System Repair Procedures: Cross-Node Consistency Validation",
        keywords=["file system", "repair", "cross-node", "consistency validation"],
        conclusion_template="Validate file system consistency across nodes after distributed recovery operations.",
        reasoning_framework="""
        1. After distributed file system recovery, run cross-node consistency checks.
        2. Reconcile discrepancies and repair as needed.
        3. Document validation results and actions taken.
        4. Notify system owners of validation outcomes.
        """,
        key_factors=[
            "Check coverage",
            "Repair procedures",
            "Documentation",
            "Owner notification"
        ],
        primary_authority=[
            "GS02 Distributed Storage Policy",
            "Ceph/HDFS Consistency Docs"
        ],
        burden_holder="Storage Engineer",
        adversary_position="Single-node validation is sufficient.",
        counter_arguments=[
            "Distributed systems require cross-node validation.",
            "Single-node checks miss distributed inconsistencies."
        ],
        resolution_strategy="Enforce cross-node validation for distributed file systems.",
        entity_scope="Distributed file systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2022-FS-08"
    ),
    DoctrineBlock(
        topic="Network Recovery Procedures: Layer 2 vs. Layer 3 Diagnostics",
        keywords=["network", "recovery", "layer 2", "layer 3", "diagnostics"],
        conclusion_template="Perform Layer 2 diagnostics before Layer 3 in network recovery to isolate faults efficiently.",
        reasoning_framework="""
        1. On network failure, check physical and data link layers (Layer 1/2) first.
        2. Validate switch port status, VLAN configuration, and MAC tables.
        3. If Layer 2 is healthy, proceed to Layer 3 (routing, IP).
        4. Document diagnostic steps and findings.
        5. Escalate based on diagnostic outcomes.
        """,
        key_factors=[
            "Diagnostic order",
            "Layer-specific tools",
            "Documentation",
            "Escalation procedures"
        ],
        primary_authority=[
            "GS02 Network Troubleshooting Guide",
            "OSI Model Reference"
        ],
        burden_holder="Network Engineer",
        adversary_position="Start with Layer 3 for faster results.",
        counter_arguments=[
            "Layer 2 issues are more common.",
            "Proper order speeds up resolution."
        ],
        resolution_strategy="Diagnose Layer 2 before Layer 3.",
        entity_scope="All network recovery operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-NET-12"
    ),
    DoctrineBlock(
        topic="Cache Invalidation Strategies: Consistent Hashing for Distributed Caches",
        keywords=["cache", "invalidation", "consistent hashing", "distributed cache"],
        conclusion_template="Use consistent hashing to minimize cache invalidation during node changes in distributed caches.",
        reasoning_framework="""
        1. Implement consistent hashing for all distributed cache clusters.
        2. On node addition or removal, only a subset of keys are remapped.
        3. Monitor cache hit rates and rebalance as needed.
        4. Document hashing and invalidation policies.
        """,
        key_factors=[
            "Hashing algorithm",
            "Cluster topology",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Distributed Cache Policy",
            "Memcached Consistent Hashing Docs"
        ],
        burden_holder="Cache Administrator",
        adversary_position="Random hashing is sufficient.",
        counter_arguments=[
            "Random hashing causes widespread invalidation.",
            "Consistent hashing minimizes disruption."
        ],
        resolution_strategy="Use consistent hashing for all distributed caches.",
        entity_scope="Distributed cache clusters",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CACHE-09"
    ),
    DoctrineBlock(
        topic="Queue Drain Procedures: Backpressure Management",
        keywords=["queue", "drain", "backpressure", "flow control"],
        conclusion_template="Implement backpressure mechanisms during queue drain to prevent downstream overload.",
        reasoning_framework="""
        1. Monitor consumer processing rates during drain.
        2. Throttle message delivery if consumers lag.
        3. Alert operators if backpressure persists.
        4. Document backpressure management policies.
        5. Tune thresholds based on system capacity.
        """,
        key_factors=[
            "Monitoring",
            "Throttling mechanisms",
            "Alerting",
            "Threshold tuning"
        ],
        primary_authority=[
            "GS02 Messaging Operations",
            "Reactive Streams Specification"
        ],
        burden_holder="Queue Administrator",
        adversary_position="Draining as fast as possible is best.",
        counter_arguments=[
            "Unmanaged drain can overload consumers.",
            "Backpressure maintains system stability."
        ],
        resolution_strategy="Implement backpressure for all queue drains.",
        entity_scope="All message queues",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-QUEUE-13"
    ),
    DoctrineBlock(
        topic="Service Restart Taxonomy: Warm vs. Cold Restarts",
        keywords=["service restart", "warm restart", "cold restart", "state preservation"],
        conclusion_template="Prefer warm restarts to preserve in-memory state when supported by the service.",
        reasoning_framework="""
        1. Assess if the service supports warm restart (reload without full process exit).
        2. Use warm restart to reload configuration or code without dropping connections.
        3. For services lacking support, perform cold restart (full process exit and start).
        4. Document restart type and rationale.
        5. Monitor service behavior post-restart.
        """,
        key_factors=[
            "Service capabilities",
            "State preservation",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Service Restart Policy",
            "Nginx Reload Documentation"
        ],
        burden_holder="Site Reliability Engineer",
        adversary_position="Cold restarts are always safer.",
        counter_arguments=[
            "Warm restarts reduce disruption.",
            "Cold restarts may lose state."
        ],
        resolution_strategy="Prefer warm restarts when available.",
        entity_scope="All managed services",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RESTART-13"
    ),
    DoctrineBlock(
        topic="Rollback Procedure Generation: Canary Rollback",
        keywords=["rollback", "canary", "partial rollback", "risk mitigation"],
        conclusion_template="Use canary rollback to validate rollback procedures on a subset of users before full rollback.",
        reasoning_framework="""
        1. Identify canary group for rollback validation.
        2. Roll back changes for canary group and monitor outcomes.
        3. If successful, proceed with full rollback.
        4. If issues arise, halt and investigate.
        5. Document canary rollback process and results.
        """,
        key_factors=[
            "Canary group selection",
            "Monitoring",
            "Rollback gating",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Deployment Policy",
            "Canary Release Best Practices"
        ],
        burden_holder="Release Manager",
        adversary_position="Full rollback is faster.",
        counter_arguments=[
            "Canary rollback reduces risk.",
            "Full rollback may propagate errors."
        ],
        resolution_strategy="Use canary rollback for all major changes.",
        entity_scope="All production deployments",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2021-ROLLBACK-13"
    ),
    DoctrineBlock(
        topic="Retry Logic Patterns: Retry Budget Enforcement",
        keywords=["retry", "budget", "enforcement", "failure management"],
        conclusion_template="Enforce retry budgets to limit the impact of repeated failures.",
        reasoning_framework="""
        1. Define a maximum retry budget per operation or time window.
        2. Track retry usage and enforce limits.
        3. On budget exhaustion, fail fast and alert operators.
        4. Document retry budget policies.
        5. Tune budgets based on historical data.
        """,
        key_factors=[
            "Budget definition",
            "Tracking mechanisms",
            "Alerting",
            "Policy documentation"
        ],
        primary_authority=[
            "GS02 Reliability Policy",
            "Google SRE Book"
        ],
        burden_holder="Application Developer",
        adversary_position="Unlimited retries maximize reliability.",
        counter_arguments=[
            "Unlimited retries can cause overload.",
            "Budgets balance reliability and stability."
        ],
        resolution_strategy="Enforce retry budgets for all retry logic.",
        entity_scope="All retryable operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2022-RETRY-15"
    ),
    DoctrineBlock(
        topic="Configuration Repair Patterns: Self-Healing Scripts",
        keywords=["configuration", "repair", "self-healing", "automation"],
        conclusion_template="Deploy self-healing scripts to automatically repair common configuration issues.",
        reasoning_framework="""
        1. Identify common configuration issues and their signatures.
        2. Develop scripts to detect and remediate these issues.
        3. Schedule scripts to run periodically or trigger on detection.
        4. Log all self-healing actions for audit.
        5. Alert operators on repeated or failed repairs.
        """,
        key_factors=[
            "Issue identification",
            "Script reliability",
            "Logging",
            "Alerting"
        ],
        primary_authority=[
            "GS02 Self-Healing Policy",
            "Autonomic Computing Principles"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Manual repair is more controlled.",
        counter_arguments=[
            "Manual repair is slow.",
            "Self-healing reduces MTTR."
        ],
        resolution_strategy="Deploy self-healing for all common issues.",
        entity_scope="All managed configurations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2021-CONFIG-16"
    ),
    DoctrineBlock(
        topic="Dependency Resolution Strategies: Fallback Mechanisms",
        keywords=["dependency", "resolution", "fallback", "redundancy"],
        conclusion_template="Implement fallback mechanisms for critical dependencies to enhance recovery.",
        reasoning_framework="""
        1. Identify critical dependencies and their failure modes.
        2. Provide redundant or alternative services as fallback.
        3. Automate failover to fallback on primary failure.
        4. Monitor and test fallback mechanisms regularly.
        5. Document fallback configurations and procedures.
        """,
        key_factors=[
            "Critical dependency identification",
            "Fallback automation",
            "Testing",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Dependency Policy",
            "Resilience Engineering Principles"
        ],
        burden_holder="Platform Engineer",
        adversary_position="Fallback is unnecessary overhead.",
        counter_arguments=[
            "Fallback improves resilience.",
            "Overhead is justified by reduced downtime."
        ],
        resolution_strategy="Implement fallback for all critical dependencies.",
        entity_scope="Critical service dependencies",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2022-DEP-16"
    ),
    DoctrineBlock(
        topic="Database Recovery Procedures: Schema Version Control",
        keywords=["database", "recovery", "schema", "version control"],
        conclusion_template="Use schema version control to facilitate reliable database recovery.",
        reasoning_framework="""
        1. Track all schema changes with version control tools.
        2. Validate schema version before and after recovery.
        3. Automate schema migrations and rollbacks.
        4. Document schema changes and recovery procedures.
        """,
        key_factors=[
            "Version tracking",
            "Migration automation",
            "Validation",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Database Policy",
            "Flyway/Liquibase Docs"
        ],
        burden_holder="Database Engineer",
        adversary_position="Manual schema management is sufficient.",
        counter_arguments=[
            "Manual management is error-prone.",
            "Version control ensures repeatability."
        ],
        resolution_strategy="Use version control for all schema changes.",
        entity_scope="All managed databases",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-DB-16"
    ),
    DoctrineBlock(
        topic="File System Repair Procedures: Immutable Snapshots for Forensics",
        keywords=["file system", "repair", "immutable snapshot", "forensics"],
        conclusion_template="Take immutable snapshots before repair for forensic analysis.",
        reasoning_framework="""
        1. On detection of file system corruption, take an immutable snapshot.
        2. Preserve snapshot for forensic investigation.
        3. Proceed with repair on a copy or after snapshot.
        4. Document snapshot and repair actions.
        5. Share findings with security and compliance teams.
        """,
        key_factors=[
            "Snapshot timing",
            "Immutability",
            "Forensic procedures",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Storage Forensics Policy",
            "NIST SP 800-86"
        ],
        burden_holder="Storage Engineer",
        adversary_position="Immediate repair is more urgent.",
        counter_arguments=[
            "Forensics may be required for compliance.",
            "Snapshots preserve evidence."
        ],
        resolution_strategy="Take immutable snapshots before repair.",
        entity_scope="All critical file systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="GS02-2022-FS-16"
    ),
    DoctrineBlock(
        topic="Network Recovery Procedures: Configuration Rollback",
        keywords=["network", "recovery", "configuration rollback", "automation"],
        conclusion_template="Automate network configuration rollback to recover from misconfigurations.",
        reasoning_framework="""
        1. Track all network configuration changes with version control.
        2. On failure, identify last known good configuration.
        3. Automate rollback to restore connectivity.
        4. Validate network health post-rollback.
        5. Document rollback actions and outcomes.
        """,
        key_factors=[
            "Change tracking",
            "Rollback automation",
            "Validation",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Network Automation Policy",
            "Cisco Network Rollback Docs"
        ],
        burden_holder="Network Engineer",
        adversary_position="Manual rollback is more controlled.",
        counter_arguments=[
            "Manual rollback is slow.",
            "Automation reduces downtime."
        ],
        resolution_strategy="Automate configuration rollback for all network devices.",
        entity_scope="All managed networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-NET-16"
    ),
    DoctrineBlock(
        topic="Cache Invalidation Strategies: Multi-Layer Cache Coordination",
        keywords=["cache", "invalidation", "multi-layer", "coordination"],
        conclusion_template="Coordinate invalidation across multiple cache layers to prevent stale data.",
        reasoning_framework="""
        1. Identify all cache layers (e.g., local, distributed, CDN).
        2. On data change, propagate invalidation events to all layers.
        3. Monitor for stale reads and reconcile as needed.
        4. Document coordination policies and procedures.
        """,
        key_factors=[
            "Layer identification",
            "Event propagation",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "GS02 Caching Policy",
            "CDN Invalidation Docs"
        ],
        burden_holder="Application Architect",
        adversary_position="Single-layer invalidation is sufficient.",
        counter_arguments=[
            "Stale data can persist in other layers.",
            "Coordination ensures consistency."
        ],
        resolution_strategy="Coordinate invalidation across all cache layers.",
        entity_scope="All multi-layer caches",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GS02-2022-CACHE-16"
    ),
    DoctrineBlock(
        topic="Queue Drain Procedures: Graceful Shutdown Hooks",
        keywords=["queue", "drain", "graceful shutdown", "hooks"],
        conclusion_template="Implement graceful shutdown hooks for queue consumers to ensure clean drain.",
        reasoning_framework="""
        1. Register shutdown hooks in all queue consumer processes.
        2. On shutdown, stop accepting new messages and finish processing in-flight messages.
        3. Log shutdown actions and outcomes.
        4. Alert operators on abnormal shutdowns.
        5. Test shutdown hooks regularly.
        """,
        key_factors=[
            "Hook registration",
            "Message processing",
            "Logging",
            "Testing"
        ],
        primary_authority=[
            "GS02 Messaging Policy",
            "Java Shutdown Hook Documentation"
        ],
        burden_holder="Queue Administrator",
        adversary_position="Forceful shutdown is faster.",
        counter_arguments=[
            "Forceful shutdown risks message loss.",
            "Graceful hooks ensure clean drain."
        ],
        resolution_strategy="Implement shutdown hooks for all consumers.",
        entity_scope="All queue consumers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GS02-2021-QUEUE-16"
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