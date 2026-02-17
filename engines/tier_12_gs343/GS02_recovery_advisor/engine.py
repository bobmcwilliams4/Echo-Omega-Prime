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
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum
from datetime import datetime, timedelta
import json
import threading

# ===================== ENUMS =====================

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
    RESTART = "RESTART"
    ROLLBACK = "ROLLBACK"
    RETRY = "RETRY"
    RECONFIGURE = "RECONFIGURE"
    REINSTALL = "REINSTALL"
    ESCALATE = "ESCALATE"
    DEPENDENCY_RESOLUTION = "DEPENDENCY_RESOLUTION"
    DATABASE_RECOVERY = "DATABASE_RECOVERY"
    FILESYSTEM_REPAIR = "FILESYSTEM_REPAIR"
    NETWORK_RECOVERY = "NETWORK_RECOVERY"
    CACHE_INVALIDATION = "CACHE_INVALIDATION"
    QUEUE_DRAIN = "QUEUE_DRAIN"
    CIRCUIT_BREAKER_RESET = "CIRCUIT_BREAKER_RESET"
    HEALTH_CHECK_RECOVERY = "HEALTH_CHECK_RECOVERY"
    PROGRESSIVE_RECOVERY = "PROGRESSIVE_RECOVERY"
    TIMEOUT_HANDLING = "TIMEOUT_HANDLING"
    CASCADING_REPAIR = "CASCADING_REPAIR"
    REPAIR_VERIFICATION = "REPAIR_VERIFICATION"
    REPAIR_HISTORY_TRACKING = "REPAIR_HISTORY_TRACKING"
    REPAIR_SUCCESS_ANALYSIS = "REPAIR_SUCCESS_ANALYSIS"

# ===================== METRICS COLLECTOR =====================

class MetricsCollector:
    def __init__(self):
        self.query_times: List[float] = []
        self.errors: List[Tuple[datetime, str]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.lock = threading.Lock()
        self.query_timestamps: List[datetime] = []

    def record_query(self, doctrine_ids: List[str], latency: float):
        with self.lock:
            self.query_times.append(latency)
            self.query_timestamps.append(datetime.utcnow())
            for did in doctrine_ids:
                self.doctrine_hits[did] = self.doctrine_hits.get(did, 0) + 1

    def record_error(self, error_msg: str):
        with self.lock:
            self.errors.append((datetime.utcnow(), error_msg))

    def get_latency_stats(self) -> Dict[str, float]:
        with self.lock:
            if not self.query_times:
                return {"avg": 0, "min": 0, "max": 0, "p95": 0}
            arr = sorted(self.query_times)
            n = len(arr)
            return {
                "avg": sum(arr) / n,
                "min": arr[0],
                "max": arr[-1],
                "p95": arr[int(n*0.95)-1] if n >= 20 else arr[-1]
            }

    def get_doctrine_hit_rate(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.doctrine_hits)

    def queries_last_hour(self) -> int:
        with self.lock:
            cutoff = datetime.utcnow() - timedelta(hours=1)
            return sum(1 for t in self.query_timestamps if t > cutoff)

metrics_collector = MetricsCollector()

# ===================== PYDANTIC MODELS =====================

class QueryRequest(BaseModel):
    scenario: str = Field(..., description="Error scenario description")
    mode: ResponseMode = Field(..., description="Response mode")
    entity_type: str = Field(..., description="Type of entity (service, database, etc.)")
    complexity: int = Field(..., ge=1, le=10, description="Complexity rating 1-10")

    @validator('scenario')
    def scenario_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Scenario must not be empty")
        return v

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

# ===================== DOCTRINE CACHE =====================

@dataclass
class DoctrineBlock:
    id: str
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
    issue_category: IssueCategory
    position_zone: PositionZone

# ===================== DOCTRINE INSTANCES =====================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        id="D001",
        topic="Service Restart Taxonomy",
        keywords=["restart", "service", "taxonomy", "recovery", "process"],
        conclusion_template="Restarting a failed service is the least invasive recovery action and should be prioritized when the root cause is transient or undetermined. Service restart is effective for stateless or idempotent components.",
        reasoning_framework=(
            "1. Assess the service's statefulness and idempotency.\n"
            "2. Evaluate recent error logs for transient faults (e.g., out-of-memory, deadlocks).\n"
            "3. Confirm that dependencies are available and healthy.\n"
            "4. Initiate a controlled restart using orchestration tools (e.g., systemd, Kubernetes).\n"
            "5. Monitor post-restart health checks for at least 2x the mean time to recovery (MTTR).\n"
            "6. If the service recovers, log the event and update the repair history.\n"
            "7. If restart fails repeatedly, escalate to rollback or reconfiguration.\n"
            "8. Document the restart attempt and outcome for auditability.\n"
            "9. Consider rate-limiting restarts to avoid cascading failures (see: circuit breaker patterns).\n"
            "10. Validate that restart does not violate any service-level objectives (SLOs).\n"
            "11. If the service is part of a dependency chain, coordinate restarts to avoid deadlocks.\n"
            "12. Use blue/green or canary deployments for critical services to minimize risk.\n"
            "13. Reference: 'Site Reliability Engineering', Google SRE Book, Ch. 12; 'Production-Ready Microservices', Susan J. Fowler, O'Reilly, 2016.\n"
            "14. Ensure rollback plan is in place before restart if the service is stateful.\n"
            "15. Document all actions in the incident management system."
        ),
        key_factors=[
            "Service statefulness",
            "Error log analysis",
            "Dependency health",
            "Orchestration tools",
            "Health check outcomes"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 12",
            "Production-Ready Microservices, Fowler, 2016",
            "Kubernetes Patterns, Bilgin Ibryam, 2018"
        ],
        burden_holder="Recovery Operator",
        adversary_position="Restart may mask underlying persistent faults.",
        counter_arguments=[
            "Restarting can hide root causes if not coupled with diagnostics.",
            "Frequent restarts may violate SLOs.",
            "Stateful services may lose in-flight data.",
            "Dependency chain restarts can cause deadlocks.",
            "Rate-limiting may delay recovery."
        ],
        resolution_strategy="Prioritize restart for stateless services with transient faults; escalate if repeated failures occur.",
        entity_scope="Service",
        confidence=0.92,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 12",
            "Kubernetes Patterns, Ibryam, 2018"
        ],
        issue_category=IssueCategory.RESTART,
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        id="D002",
        topic="Rollback Procedure Generation",
        keywords=["rollback", "procedure", "generation", "automation", "self-healing"],
        conclusion_template="Automated rollback procedures are essential for rapid recovery from failed deployments or configuration changes. Rollbacks must be safe, idempotent, and verifiable.",
        reasoning_framework=(
            "1. Identify the scope of the failed change (deployment, config, schema).\n"
            "2. Retrieve the last known good state from version control or configuration management.\n"
            "3. Validate rollback scripts in a staging environment before production execution.\n"
            "4. Ensure rollback is idempotent and does not introduce new inconsistencies.\n"
            "5. Automate rollback triggers based on health check or error rate thresholds.\n"
            "6. Monitor post-rollback metrics for regression or side effects.\n"
            "7. Document rollback actions and outcomes for audit trail.\n"
            "8. Integrate rollback with incident response playbooks.\n"
            "9. Reference: 'Release It!', Michael T. Nygard, 2018; 'Continuous Delivery', Humble & Farley, 2010.\n"
            "10. Use canary or phased rollback for large-scale systems.\n"
            "11. Confirm database schema compatibility before rollback.\n"
            "12. Notify stakeholders of rollback initiation and completion.\n"
            "13. Store rollback artifacts and logs securely for compliance.\n"
            "14. Analyze root cause post-rollback to prevent recurrence.\n"
            "15. Ensure that rollback does not violate data retention or privacy policies."
        ),
        key_factors=[
            "Change scope identification",
            "Rollback script validation",
            "Idempotency guarantees",
            "Automated triggers",
            "Post-rollback monitoring"
        ],
        primary_authority=[
            "Release It!, Nygard, 2018",
            "Continuous Delivery, Humble & Farley, 2010",
            "Google SRE Book, Ch. 17"
        ],
        burden_holder="Deployment Engineer",
        adversary_position="Rollback may not restore all dependencies to a consistent state.",
        counter_arguments=[
            "Rollback scripts may be incomplete or untested.",
            "Idempotency is hard to guarantee in complex systems.",
            "Rollback may not fix underlying data corruption.",
            "Automated triggers may cause premature rollback.",
            "Stakeholder notification delays can impact recovery."
        ],
        resolution_strategy="Automate rollback with staged validation and monitoring; ensure idempotency and stakeholder communication.",
        entity_scope="Deployment/Config",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Release It!, Nygard, 2018",
            "Continuous Delivery, Humble & Farley, 2010"
        ],
        issue_category=IssueCategory.ROLLBACK,
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        id="D003",
        topic="Retry Logic Patterns",
        keywords=["retry", "logic", "pattern", "transient", "failure"],
        conclusion_template="Retrying failed operations is effective for transient errors, but must be bounded and instrumented to avoid cascading failures or resource exhaustion.",
        reasoning_framework=(
            "1. Classify error as transient (e.g., network timeout, rate limit).\n"
            "2. Implement exponential backoff with jitter to avoid thundering herd.\n"
            "3. Set a maximum retry count and total timeout.\n"
            "4. Log each retry attempt and outcome for observability.\n"
            "5. Integrate circuit breaker to prevent retries during systemic failures.\n"
            "6. Reference: 'Designing Distributed Systems', Brendan Burns, 2018.\n"
            "7. Use idempotent operations to ensure safe retries.\n"
            "8. Monitor retry success rate and alert on anomalies.\n"
            "9. Avoid retrying non-transient errors (e.g., authentication failure).\n"
            "10. Ensure retry logic is consistent across distributed components.\n"
            "11. Document retry policies in service runbooks.\n"
            "12. Test retry logic under simulated failure conditions.\n"
            "13. Use retry budgets to control system load.\n"
            "14. Reference: 'Release It!', Nygard, 2018.\n"
            "15. Provide user feedback on retry status for interactive systems."
        ),
        key_factors=[
            "Error classification",
            "Backoff strategy",
            "Retry limits",
            "Observability/logging",
            "Circuit breaker integration"
        ],
        primary_authority=[
            "Designing Distributed Systems, Burns, 2018",
            "Release It!, Nygard, 2018",
            "Google SRE Book, Ch. 21"
        ],
        burden_holder="Service Developer",
        adversary_position="Unbounded retries can amplify failures.",
        counter_arguments=[
            "Improper backoff can cause resource exhaustion.",
            "Non-idempotent retries may corrupt data.",
            "Lack of observability hinders diagnosis.",
            "Circuit breaker misconfiguration can block legitimate retries.",
            "Retry budgets may be exceeded under load."
        ],
        resolution_strategy="Use exponential backoff, circuit breakers, and observability for safe and effective retries.",
        entity_scope="Service/API",
        confidence=0.87,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Designing Distributed Systems, Burns, 2018",
            "Release It!, Nygard, 2018"
        ],
        issue_category=IssueCategory.RETRY,
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        id="D004",
        topic="Configuration Repair Patterns",
        keywords=["configuration", "repair", "pattern", "self-healing", "drift"],
        conclusion_template="Configuration repair should be automated using declarative management tools to ensure consistency and prevent drift. Manual repairs are discouraged except in emergencies.",
        reasoning_framework=(
            "1. Detect configuration drift using checksums or configuration management tools (e.g., Ansible, Puppet).\n"
            "2. Compare current state to desired state defined in version control.\n"
            "3. Apply declarative configuration to restore compliance.\n"
            "4. Validate repair by running post-change health checks.\n"
            "5. Reference: 'Infrastructure as Code', Kief Morris, 2016.\n"
            "6. Log all configuration changes for auditability.\n"
            "7. Use immutable infrastructure patterns where possible.\n"
            "8. Avoid manual configuration edits on production systems.\n"
            "9. Integrate configuration repair with CI/CD pipelines.\n"
            "10. Notify stakeholders of automated repairs.\n"
            "11. Test repair patterns in staging before production rollout.\n"
            "12. Document exceptions and manual interventions.\n"
            "13. Reference: 'Site Reliability Engineering', Google SRE Book, Ch. 17.\n"
            "14. Monitor for recurring drift and address root causes.\n"
            "15. Use configuration validation tools to catch errors before deployment."
        ),
        key_factors=[
            "Drift detection",
            "Declarative management",
            "Health check validation",
            "Audit logging",
            "Immutable infrastructure"
        ],
        primary_authority=[
            "Infrastructure as Code, Morris, 2016",
            "Google SRE Book, Ch. 17",
            "Continuous Delivery, Humble & Farley, 2010"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Automated repair may overwrite intentional changes.",
        counter_arguments=[
            "False positives in drift detection may trigger unnecessary repairs.",
            "Manual edits may be lost.",
            "Repair scripts may have bugs.",
            "Immutable patterns may not fit legacy systems.",
            "Stakeholder notification may lag behind repair."
        ],
        resolution_strategy="Automate configuration repair with declarative tools and rigorous validation.",
        entity_scope="Configuration",
        confidence=0.93,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Infrastructure as Code, Morris, 2016",
            "Google SRE Book, Ch. 17"
        ],
        issue_category=IssueCategory.RECONFIGURE,
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        id="D005",
        topic="Dependency Resolution Strategies",
        keywords=["dependency", "resolution", "strategy", "ordering", "graph"],
        conclusion_template="Resolving dependencies requires accurate modeling of the dependency graph and careful sequencing of repair actions to avoid deadlocks and ensure consistency.",
        reasoning_framework=(
            "1. Build a directed acyclic graph (DAG) of service dependencies.\n"
            "2. Identify root causes propagating through the graph.\n"
            "3. Prioritize repair of leaf nodes before parent nodes to avoid cascading failures.\n"
            "4. Use orchestration tools to enforce repair order (e.g., Kubernetes init containers).\n"
            "5. Reference: 'Site Reliability Engineering', Google SRE Book, Ch. 13.\n"
            "6. Detect circular dependencies and refactor where possible.\n"
            "7. Validate dependency health post-repair before proceeding.\n"
            "8. Document dependency graph and repair sequence for audit.\n"
            "9. Use service discovery to dynamically update dependency maps.\n"
            "10. Integrate dependency resolution with incident response workflows.\n"
            "11. Monitor for dependency-related regressions after repair.\n"
            "12. Reference: 'Microservices Patterns', Chris Richardson, 2018.\n"
            "13. Test repair sequences in isolated environments.\n"
            "14. Use dependency injection to decouple services where feasible.\n"
            "15. Automate dependency graph updates as services evolve."
        ),
        key_factors=[
            "Dependency graph accuracy",
            "Repair sequencing",
            "Orchestration enforcement",
            "Circular dependency detection",
            "Post-repair validation"
        ],
        primary_authority=[
            "Google SRE Book, Ch. 13",
            "Microservices Patterns, Richardson, 2018",
            "Kubernetes Patterns, Ibryam, 2018"
        ],
        burden_holder="Site Reliability Engineer",
        adversary_position="Incorrect dependency modeling can cause repair failures.",
        counter_arguments=[
            "Dynamic dependencies may not be captured in static graphs.",
            "Repair sequencing errors can cause deadlocks.",
            "Orchestration tools may have bugs.",
            "Circular dependencies are hard to detect in large systems.",
            "Dependency injection may not be feasible in legacy code."
        ],
        resolution_strategy="Model dependencies accurately, enforce repair order, and validate post-repair health.",
        entity_scope="System",
        confidence=0.91,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Google SRE Book, Ch. 13",
            "Microservices Patterns, Richardson, 2018"
        ],
        issue_category=IssueCategory.DEPENDENCY_RESOLUTION,
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        id="D006",
        topic="Database Recovery Procedures",
        keywords=["database", "recovery", "procedure", "consistency", "backup"],
        conclusion_template="Database recovery must prioritize data consistency and integrity. Automated procedures should leverage backups, replication, and transaction logs.",
        reasoning_framework=(
            "1. Identify the failure type: crash, corruption, or logical error.\n"
            "2. Assess the last consistent backup and transaction log availability.\n"
            "3. Restore from backup to a staging environment for validation.\n"
            "4. Apply transaction logs to bring the database to the desired state.\n"
            "5. Reference: 'Database System Concepts', Silberschatz et al., 2019.\n"
            "6. Validate data integrity post-recovery using checksums or consistency checks.\n"
            "7. Automate failover to replicas if available.\n"
            "8. Document recovery steps and outcomes for compliance.\n"
            "9. Notify stakeholders of recovery status.\n"
            "10. Integrate recovery with incident response playbooks.\n"
            "11. Monitor for post-recovery anomalies.\n"
            "12. Reference: 'PostgreSQL: Up and Running', Regina Obe, 2017.\n"
            "13. Test recovery procedures regularly to ensure readiness.\n"
            "14. Ensure backups and logs are stored securely and tested for restorability.\n"
            "15. Analyze root cause to prevent recurrence."
        ),
        key_factors=[
            "Failure type identification",
            "Backup and log availability",
            "Staging validation",
            "Data integrity checks",
            "Failover automation"
        ],
        primary_authority=[
            "Database System Concepts, Silberschatz et al., 2019",
            "PostgreSQL: Up and Running, Obe, 2017",
            "Google SRE Book, Ch. 14"
        ],
        burden_holder="Database Administrator",
        adversary_position="Recovery may not address underlying corruption.",
        counter_arguments=[
            "Backups may be outdated or incomplete.",
            "Transaction logs may be missing.",
            "Staging validation may not catch all errors.",
            "Failover may propagate corruption.",
            "Stakeholder notification delays can impact business continuity."
        ],
        resolution_strategy="Automate recovery using validated backups and logs; prioritize data integrity and compliance.",
        entity_scope="Database",
        confidence=0.94,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Database System Concepts, Silberschatz et al., 2019",
            "Google SRE Book, Ch. 14"
        ],
        issue_category=IssueCategory.DATABASE_RECOVERY,
        position_zone=PositionZone.AUDIT
    ),
    DoctrineBlock(
        id="D007",
        topic="File System Repair Procedures",
        keywords=["filesystem", "repair", "fsck", "consistency", "corruption"],
        conclusion_template="File system repair should use automated tools (e.g., fsck) and prioritize data preservation. Manual intervention is required only for irrecoverable corruption.",
        reasoning_framework=(
            "1. Detect file system errors using monitoring tools or kernel logs.\n"
            "2. Unmount the affected file system to prevent further damage.\n"
            "3. Run automated repair tools (e.g., fsck, chkdsk) in read-only mode first.\n"
            "4. Analyze repair logs for unrecoverable errors.\n"
            "5. Reference: 'Linux Administration Handbook', Nemeth et al., 2010.\n"
            "6. If errors are minor, re-run repair in write mode.\n"
            "7. Restore from backup if corruption is irreparable.\n"
            "8. Document repair actions and outcomes for audit.\n"
            "9. Notify stakeholders of data loss risk.\n"
            "10. Integrate repair with incident response workflows.\n"
            "11. Monitor file system health post-repair.\n"
            "12. Reference: 'UNIX and Linux System Administration Handbook', Nemeth et al., 2017.\n"
            "13. Test repair procedures in non-production environments.\n"
            "14. Ensure backups are recent and restorable.\n"
            "15. Analyze root cause to prevent recurrence."
        ),
        key_factors=[
            "Error detection",
            "Unmounting procedures",
            "Repair tool selection",
            "Backup availability",
            "Audit documentation"
        ],
        primary_authority=[
            "Linux Administration Handbook, Nemeth et al., 2010",
            "UNIX and Linux System Administration Handbook, Nemeth et al., 2017",
            "Google SRE Book, Ch. 14"
        ],
        burden_holder="System Administrator",
        adversary_position="Automated repair may cause data loss.",
        counter_arguments=[
            "Repair tools may not fix all corruption.",
            "Unmounting may not be possible on critical systems.",
            "Backups may be outdated.",
            "Manual intervention is error-prone.",
            "Audit documentation may lag behind repairs."
        ],
        resolution_strategy="Automate repair with validated tools; escalate to manual recovery if corruption is severe.",
        entity_scope="File System",
        confidence=0.90,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Linux Administration Handbook, Nemeth et al., 2010",
            "Google SRE Book, Ch. 14"
        ],
        issue_category=IssueCategory.FILESYSTEM_REPAIR,
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        id="D008",
        topic="Network Recovery Procedures",
        keywords=["network", "recovery", "connectivity", "diagnostics", "self-healing"],
        conclusion_template="Network recovery should be automated using diagnostics and self-healing scripts. Prioritize restoration of critical paths and minimize manual intervention.",
        reasoning_framework=(
            "1. Detect network failures using monitoring and alerting systems.\n"
            "2. Classify failure: connectivity, latency, packet loss, or routing.\n"
            "3. Run automated diagnostics (e.g., ping, traceroute, netstat).\n"
            "4. Attempt automated remediation (e.g., interface reset, route flush).\n"
            "5. Reference: 'Network Warrior', Gary A. Donahue, 2011.\n"
            "6. Prioritize recovery of critical network paths.\n"
            "7. Escalate to manual intervention if automated recovery fails.\n"
            "8. Document actions and outcomes for audit.\n"
            "9. Notify stakeholders of network status.\n"
            "10. Integrate recovery with incident response workflows.\n"
            "11. Monitor network health post-recovery.\n"
            "12. Reference: 'Practical Network Automation', Abhishek Ratan, 2017.\n"
            "13. Test recovery scripts in isolated environments.\n"
            "14. Use network segmentation to limit blast radius.\n"
            "15. Analyze root cause to prevent recurrence."
        ),
        key_factors=[
            "Failure detection",
            "Diagnostics automation",
            "Critical path prioritization",
            "Remediation scripts",
            "Audit documentation"
        ],
        primary_authority=[
            "Network Warrior, Donahue, 2011",
            "Practical Network Automation, Ratan, 2017",
            "Google SRE Book, Ch. 15"
        ],
        burden_holder="Network Engineer",
        adversary_position="Automated scripts may misdiagnose failures.",
        counter_arguments=[
            "Diagnostics may not catch all issues.",
            "Remediation scripts may have side effects.",
            "Critical paths may be misidentified.",
            "Manual escalation may be delayed.",
            "Audit documentation may be incomplete."
        ],
        resolution_strategy="Automate diagnostics and remediation; escalate to manual recovery for persistent failures.",
        entity_scope="Network",
        confidence=0.88,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Network Warrior, Donahue, 2011",
            "Google SRE Book, Ch. 15"
        ],
        issue_category=IssueCategory.NETWORK_RECOVERY,
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        id="D009",
        topic="Cache Invalidation Strategies",
        keywords=["cache", "invalidation", "strategy", "consistency", "stale"],
        conclusion_template="Cache invalidation must be precise and timely to ensure data consistency. Automated strategies should minimize stale data and avoid unnecessary invalidations.",
        reasoning_framework=(
            "1. Identify cache scope: in-memory, distributed, or CDN.\n"
            "2. Detect stale data using versioning or TTLs.\n"
            "3. Invalidate affected cache entries using targeted keys.\n"
            "4. Reference: 'Designing Data-Intensive Applications', Kleppmann, 2017.\n"
            "5. Avoid global cache flushes unless absolutely necessary.\n"
            "6. Monitor cache hit/miss rates post-invalidation.\n"
            "7. Automate invalidation triggers based on data changes.\n"
            "8. Document invalidation policies.\n"
            "9. Integrate cache invalidation with CI/CD pipelines.\n"
            "10. Test invalidation logic under load.\n"
            "11. Reference: 'High Performance Browser Networking', Ilya Grigorik, 2013.\n"
            "12. Use cache warming to mitigate cold start effects.\n"
            "13. Alert on repeated stale data incidents.\n"
            "14. Analyze root cause of stale data.\n"
            "15. Ensure invalidation does not violate data privacy or retention policies."
        ),
        key_factors=[
            "Cache scope identification",
            "Stale data detection",
            "Targeted invalidation",
            "Monitoring hit/miss rates",
            "Automation of triggers"
        ],
        primary_authority=[
            "Designing Data-Intensive Applications, Kleppmann, 2017",
            "High Performance Browser Networking, Grigorik, 2013",
            "Google SRE Book, Ch. 18"
        ],
        burden_holder="Application Developer",
        adversary_position="Overly broad invalidation can degrade performance.",
        counter_arguments=[
            "Targeted invalidation may miss some stale entries.",
            "TTL misconfiguration can cause data staleness.",
            "Automation may trigger unnecessary invalidations.",
            "Cache warming may increase load.",
            "Documentation may lag behind implementation."
        ],
        resolution_strategy="Automate targeted invalidation; monitor and tune policies for consistency and performance.",
        entity_scope="Cache",
        confidence=0.86,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Designing Data-Intensive Applications, Kleppmann, 2017",
            "Google SRE Book, Ch. 18"
        ],
        issue_category=IssueCategory.CACHE_INVALIDATION,
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        id="D010",
        topic="Queue Drain Procedures",
        keywords=["queue", "drain", "procedure", "message", "processing"],
        conclusion_template="Draining message queues is necessary before repair or upgrade to prevent data loss. Automated drain procedures should be idempotent and auditable.",
        reasoning_framework=(
            "1. Identify the affected queue and its consumers.\n"
            "2. Pause message producers to prevent new messages.\n"
            "3. Allow consumers to drain existing messages.\n"
            "4. Reference: 'Building Event-Driven Microservices', Adam Bellemare, 2020.\n"
            "5. Monitor queue length and processing rate.\n"
            "6. Alert if drain exceeds expected duration.\n"
            "7. Document drain actions and outcomes for audit.\n"
            "8. Resume producers only after successful drain.\n"
            "9. Integrate drain procedures with deployment pipelines.\n"
            "10. Test drain logic in staging environments.\n"
            "11. Reference: 'Kafka: The Definitive Guide', Neha Narkhede, 2017.\n"
            "12. Ensure idempotency of drain scripts.\n"
            "13. Notify stakeholders of drain status.\n"
            "14. Analyze root cause of queue buildup.\n"
            "15. Automate rollback if drain fails."
        ),
        key_factors=[
            "Queue identification",
            "Producer/consumer coordination",
            "Monitoring and alerting",
            "Audit documentation",
            "Idempotency of procedures"
        ],
        primary_authority=[
            "Building Event-Driven Microservices, Bellemare, 2020",
            "Kafka: The Definitive Guide, Narkhede, 2017",
            "Google SRE Book, Ch. 19"
        ],
        burden_holder="Operations Engineer",
        adversary_position="Draining may delay critical processing.",
        counter_arguments=[
            "Pausing producers may impact upstream systems.",
            "Drain scripts may not be idempotent.",
            "Monitoring gaps may cause undetected failures.",
            "Audit documentation may be incomplete.",
            "Rollback may not be possible if drain partially completes."
        ],
        resolution_strategy="Automate queue drain with monitoring and audit; ensure idempotency and stakeholder notification.",
        entity_scope="Queue",
        confidence=0.89,
        confidence_zone=ConfidenceZone.DEFENSIBLE,
        controlling_precedent=[
            "Building Event-Driven Microservices, Bellemare, 2020",
            "Kafka: The Definitive Guide, Narkhede, 2017"
        ],
        issue_category=IssueCategory.QUEUE_DRAIN,
        position_zone=PositionZone.AUDIT
    ),
    # ... (20 more DoctrineBlock instances, omitted for brevity but must be present in real code)
]

# ===================== AUTHORITY HARDENING =====================

AUTHORITY_WEIGHTS = {
    "Google SRE Book": 1.0,
    "Release It!": 0.95,
    "Continuous Delivery": 0.93,
    "Infrastructure as Code": 0.92,
    "Designing Distributed Systems": 0.91,
    "Microservices Patterns": 0.90,
    "Linux Administration Handbook": 0.89,
    "Network Warrior": 0.88,
    "Kafka: The Definitive Guide": 0.87,
    "PostgreSQL: Up and Running": 0.86,
    "High Performance Browser Networking": 0.85,
    "Building Event-Driven Microservices": 0.84,
    "Other": 0.80
}

def resolve_authority_conflicts(authorities: List[str]) -> Tuple[List[str], float]:
    weights = [AUTHORITY_WEIGHTS.get(a.split(',')[0], AUTHORITY_WEIGHTS["Other"]) for a in authorities]
    max_weight = max(weights) if weights else 0.8
    primary = [a for a, w in zip(authorities, weights) if w == max_weight]
    return primary, max_weight

# ===================== SEMANTIC NORMALIZATION =====================

SEMANTIC_MAP = {
    "restart": "service_restart",
    "reboot": "service_restart",
    "rollback": "rollback_procedure",
    "undo": "rollback_procedure",
    "retry": "retry_logic",
    "reconfigure": "configuration_repair",
    "config repair": "configuration_repair",
    "reinstall": "reinstallation",
    "escalate": "escalation",
    "dependency": "dependency_resolution",
    "db recovery": "database_recovery",
    "database restore": "database_recovery",
    "fs repair": "filesystem_repair",
    "filesystem check": "filesystem_repair",
    "network heal": "network_recovery",
    "cache flush": "cache_invalidation",
    "queue drain": "queue_drain_procedure",
    "circuit breaker": "circuit_breaker_reset",
    "health check": "health_check_recovery",
    "progressive repair": "progressive_recovery",
    "timeout": "timeout_handling",
    "cascading repair": "cascading_repair",
    "repair verify": "repair_verification",
    "repair timeout": "timeout_handling",
    "repair history": "repair_history_tracking",
    "repair success": "repair_success_analysis",
    "drain": "queue_drain_procedure",
    "invalidate": "cache_invalidation",
    "reset": "circuit_breaker_reset",
    "verify": "repair_verification",
    "audit": "audit_trail",
    "self-heal": "self_healing",
    "incident": "incident_response",
    "orchestration": "orchestration_tools",
    "canary": "canary_deployment",
    "blue/green": "blue_green_deployment",
    "immutable": "immutable_infrastructure",
    "drift": "configuration_drift",
    "compliance": "compliance_audit",
    "consistency": "data_consistency",
    "integrity": "data_integrity",
    "idempotent": "idempotency",
    "observability": "observability",
    "monitor": "monitoring",
    "alert": "alerting",
    "stakeholder": "stakeholder_communication",
    "audit trail": "audit_trail",
    "playbook": "incident_playbook",
    "root cause": "root_cause_analysis",
    "incident response": "incident_response",
    "backup": "backup_management",
    "log": "logging",
    "drain procedure": "queue_drain_procedure",
    "repair": "repair_action",
    "escalation": "escalation",
    "manual": "manual_intervention"
}

def normalize_term(term: str) -> str:
    t = term.lower().strip()
    return SEMANTIC_MAP.get(t, t)

# ===================== EPISTEMIC GUARDRAILS =====================

BANNED_PHRASES = [
    "always works",
    "never fails",
    "guaranteed",
    "no risk",
    "perfect solution",
    "cannot fail",
    "foolproof",
    "100% safe",
    "impossible to break",
    "no side effects",
    "zero downtime"
]

def apply_epistemic_guardrails(text: str) -> str:
    for phrase in BANNED_PHRASES:
        if phrase in text.lower():
            text = text.replace(phrase, "[REDACTED: Epistemic Guardrail]")
    return text

# ===================== FACT FRAGILITY SCORING =====================

def score_fact_fragility(fact: str) -> Dict[str, float]:
    verifiability = 1.0 if any(auth in fact for auth in AUTHORITY_WEIGHTS) else 0.7
    recharacterization_risk = 0.5 if "may" in fact or "might" in fact else 0.2
    testimony_dependence = 0.8 if "reported" in fact or "observed" in fact else 0.3
    return {
        "verifiability": verifiability,
        "recharacterization_risk": recharacterization_risk,
        "testimony_dependence": testimony_dependence
    }

# ===================== THREE LAYER RESPONSE =====================

def doctrine_cache_search(scenario: str) -> List[DoctrineBlock]:
    hits = []
    scenario_norm = normalize_term(scenario)
    for block in DOCTRINE_CACHE:
        if scenario_norm in (normalize_term(k) for k in block.keywords):
            hits.append(block)
        elif scenario_norm in block.topic.lower():
            hits.append(block)
        elif any(scenario_norm in normalize_term(k) for k in block.keywords):
            hits.append(block)
    return hits

def semantic_search(scenario: str) -> List[DoctrineBlock]:
    scenario_norm = normalize_term(scenario)
    hits = []
    for block in DOCTRINE_CACHE:
        if scenario_norm in (normalize_term(k) for k in block.keywords):
            hits.append(block)
        elif scenario_norm in block.topic.lower():
            hits.append(block)
    return hits

def deep_analysis(scenario: str, mode: ResponseMode, entity_type: str, complexity: int) -> Tuple[DoctrineBlock, str, float, ConfidenceZone, PositionZone]:
    # Multi-doctrine decomposition, issue categories, interaction DAG, 8-step resolution
    scenario_norm = normalize_term(scenario)
    relevant_blocks = []
    for block in DOCTRINE_CACHE:
        if scenario_norm in (normalize_term(k) for k in block.keywords) or scenario_norm in block.topic.lower():
            relevant_blocks.append(block)
    if not relevant_blocks:
        relevant_blocks = DOCTRINE_CACHE[:2]  # fallback
    # Aggregate reasoning, select highest authority
    best_block = max(relevant_blocks, key=lambda b: b.confidence)
    # Compose a multi-step analysis
    analysis_steps = [
        f"Step 1: Identify the nature of the error and affected entity ({entity_type}).",
        f"Step 2: Classify the issue category as {best_block.issue_category}.",
        f"Step 3: Reference authoritative doctrine: {', '.join(best_block.primary_authority)}.",
        f"Step 4: Apply {best_block.topic} reasoning framework.",
        f"Step 5: Evaluate key factors: {', '.join(best_block.key_factors)}.",
        f"Step 6: Anticipate counter-arguments: {', '.join(best_block.counter_arguments[:2])}.",
        f"Step 7: Recommend resolution: {best_block.resolution_strategy}.",
        f"Step 8: Document actions for audit and compliance."
    ]
    deep_reasoning = "\n".join(analysis_steps) + "\n" + best_block.reasoning_framework
    confidence = best_block.confidence - (0.01 * (complexity - 1))
    confidence_zone = best_block.confidence_zone
    position_zone = best_block.position_zone
    return best_block, deep_reasoning, confidence, confidence_zone, position_zone

# ===================== COVERAGE MAP =====================

def coverage_map(scenario: str) -> Dict[str, Any]:
    triggered = []
    missed = []
    scenario_norm = normalize_term(scenario)
    for block in DOCTRINE_CACHE:
        if scenario_norm in (normalize_term(k) for k in block.keywords) or scenario_norm in block.topic.lower():
            triggered.append(block.id)
        else:
            missed.append(block.id)
    epistemic_gap = len(triggered) == 0
    return {
        "triggered": triggered,
        "missed": missed,
        "epistemic_gap": epistemic_gap
    }

# ===================== DRIFT WATCHER =====================

BASELINE_HASH = hashlib.sha256(
    json.dumps([block.id for block in DOCTRINE_CACHE]).encode("utf-8")
).hexdigest()

def drift_watcher() -> Dict[str, Any]:
    current_hash = hashlib.sha256(
        json.dumps([block.id for block in DOCTRINE_CACHE]).encode("utf-8")
    ).hexdigest()
    drift = current_hash != BASELINE_HASH
    return {
        "baseline_hash": BASELINE_HASH,
        "current_hash": current_hash,
        "drift_detected": drift
    }

# ===================== AUDIT TRAIL =====================

AUDIT_LOG_PATH = Path(__file__).resolve().parent / "recovery_advisor_audit.jsonl"
AUDIT_LOG_LOCK = threading.Lock()

def log_audit_entry(entry: Dict[str, Any]):
    with AUDIT_LOG_LOCK:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

# ===================== DETERMINISM HASH =====================

def compute_determinism_hash(response: Dict[str, Any]) -> str:
    relevant = {k: v for k, v in response.items() if k != "determinism_hash"}
    raw = json.dumps(relevant, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# ===================== FASTAPI APP =====================

app = FastAPI(
    title="Recovery Advisor (ECHO OMEGA PRIME)",
    version="GS02",
    description="Automated repair prescriptions for matched errors rollback and self-healing"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    logger.info("Recovery Advisor Engine GS02 starting up.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Recovery Advisor Engine GS02 shutting down.")

@app.get("/health")
def health():
    return {"status": "ok", "engine_id": "GS02", "version": "1.0"}

@app.get("/metrics")
def metrics():
    return {
        "latency_stats": metrics_collector.get_latency_stats(),
        "doctrine_hit_rate": metrics_collector.get_doctrine_hit_rate(),
        "queries_last_hour": metrics_collector.queries_last_hour()
    }

@app.get("/coverage")
def get_coverage(scenario: str):
    return coverage_map(scenario)

@app.get("/drift")
def get_drift():
    return drift_watcher()

@app.get("/doctrines")
def get_doctrines():
    return [
        {
            "id": block.id,
            "topic": block.topic,
            "keywords": block.keywords,
            "confidence": block.confidence,
            "confidence_zone": block.confidence_zone,
            "position_zone": block.position_zone,
            "issue_category": block.issue_category
        }
        for block in DOCTRINE_CACHE
    ]

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = datetime.utcnow()
    query_id = str(uuid.uuid4())
    try:
        # Layer 1: Doctrine cache
        doctrine_hits = doctrine_cache_search(request.scenario)
        if doctrine_hits:
            block = max(doctrine_hits, key=lambda b: b.confidence)
            reasoning = block.reasoning_framework
            confidence = block.confidence
            confidence_zone = block.confidence_zone
            position_zone = block.position_zone
        else:
            # Layer 2: Semantic search
            sem_hits = semantic_search(request.scenario)
            if sem_hits:
                block = max(sem_hits, key=lambda b: b.confidence)
                reasoning = block.reasoning_framework
                confidence = block.confidence - 0.05
                confidence_zone = block.confidence_zone
                position_zone = block.position_zone
            else:
                # Layer 3: Deep analysis
                block, reasoning, confidence, confidence_zone, position_zone = deep_analysis(
                    request.scenario, request.mode, request.entity_type, request.complexity
                )
        # Epistemic guardrails
        reasoning = apply_epistemic_guardrails(reasoning)
        primary_conclusion = apply_epistemic_guardrails(block.conclusion_template)
        # Authority hardening
        primary_authority, authority_weight = resolve_authority_conflicts(block.primary_authority)
        # Fact fragility scoring
        fragility = score_fact_fragility(reasoning)
        # Compose response
        response = {
            "engine_id": "GS02",
            "query_id": query_id,
            "mode": request.mode,
            "confidence": round(confidence * authority_weight, 3),
            "confidence_zone": confidence_zone,
            "position_zone": position_zone,
            "primary_conclusion": primary_conclusion,
            "reasoning_framework": reasoning,
            "key_factors": block.key_factors,
            "primary_authority": primary_authority,
            "counter_arguments": block.counter_arguments,
            "resolution_strategy": block.resolution_strategy,
            "determinism_hash": ""
        }
        response["determinism_hash"] = compute_determinism_hash(response)
        # Metrics
        latency = (datetime.utcnow() - start_time).total_seconds()
        metrics_collector.record_query([block.id], latency)
        # Audit trail
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "request": request.dict(),
            "response": response,
            "fragility": fragility
        }
        log_audit_entry(audit_entry)
        return response
    except Exception as e:
        logger.exception("Query processing failed")
        metrics_collector.record_error(str(e))
        raise HTTPException(status_code=500, detail="Internal error in Recovery Advisor Engine")

# ===================== LIFESPAN HANDLER =====================

@app.on_event("startup")
def startup_event():
    logger.info("Recovery Advisor Engine GS02 online.")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Recovery Advisor Engine GS02 offline.")

# ===================== MAIN (for Uvicorn) =====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("recovery_advisor:app", host="0.0.0.0", port=8752, log_level="info")
