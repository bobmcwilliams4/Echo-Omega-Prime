import hashlib
import threading

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "E09 Semantic Team"
SEMANTIC_MAP_ENGINE = "E09_batch_processor"

SEMANTIC_MAP = {
    # Batch Job Scheduling
    "batch job scheduling": "batch_job_scheduling",
    "job scheduling": "batch_job_scheduling",
    "schedule batch": "batch_job_scheduling",
    "batch schedule": "batch_job_scheduling",
    "batch scheduler": "batch_job_scheduling",
    "job scheduler": "batch_job_scheduling",
    "batchjob scheduling": "batch_job_scheduling",
    "batch jobs scheduling": "batch_job_scheduling",
    "batchjob scheduler": "batch_job_scheduling",
    "batch job scheduler": "batch_job_scheduling",
    "batch run scheduling": "batch_job_scheduling",
    "batch run scheduler": "batch_job_scheduling",
    "job batch scheduling": "batch_job_scheduling",
    "batch execution scheduling": "batch_job_scheduling",
    "batch execution scheduler": "batch_job_scheduling",
    "batch queue scheduling": "batch_job_scheduling",
    "batch queue scheduler": "batch_job_scheduling",
    "bjs": "batch_job_scheduling",
    "batch schduling": "batch_job_scheduling",
    "batch schduler": "batch_job_scheduling",
    "batch sch": "batch_job_scheduling",

    # Parallel Execution Management
    "parallel execution management": "parallel_execution_management",
    "parallel execution": "parallel_execution_management",
    "parallel exec": "parallel_execution_management",
    "parallel processing": "parallel_execution_management",
    "concurrent execution": "parallel_execution_management",
    "concurrent processing": "parallel_execution_management",
    "multi-threaded execution": "parallel_execution_management",
    "multithreaded execution": "parallel_execution_management",
    "multithreading": "parallel_execution_management",
    "multi processing": "parallel_execution_management",
    "multiprocessing": "parallel_execution_management",
    "thread pool": "parallel_execution_management",
    "process pool": "parallel_execution_management",
    "parallelism": "parallel_execution_management",
    "concurrency": "parallel_execution_management",
    "parallel manager": "parallel_execution_management",
    "execution manager": "parallel_execution_management",
    "pem": "parallel_execution_management",
    "paralel execution": "parallel_execution_management",
    "paralell execution": "parallel_execution_management",

    # Rate Limiting in Batch Processing
    "rate limiting": "rate_limiting",
    "rate limiting in batch processing": "rate_limiting",
    "batch rate limiting": "rate_limiting",
    "rate limiter": "rate_limiting",
    "batch rate limiter": "rate_limiting",
    "throttling": "rate_limiting",
    "throttle": "rate_limiting",
    "batch throttling": "rate_limiting",
    "batch throttle": "rate_limiting",
    "rl": "rate_limiting",
    "ratelimit": "rate_limiting",
    "rate limit": "rate_limiting",
    "rate-limiting": "rate_limiting",
    "rate-limiter": "rate_limiting",
    "ratelimiting": "rate_limiting",
    "ratelimiter": "rate_limiting",
    "ratelim": "rate_limiting",

    # Retry with Exponential Backoff
    "retry with exponential backoff": "retry_exponential_backoff",
    "exponential backoff": "retry_exponential_backoff",
    "retry backoff": "retry_exponential_backoff",
    "backoff retry": "retry_exponential_backoff",
    "backoff": "retry_exponential_backoff",
    "exp backoff": "retry_exponential_backoff",
    "exp. backoff": "retry_exponential_backoff",
    "exponential retry": "retry_exponential_backoff",
    "retry exponential": "retry_exponential_backoff",
    "retries with backoff": "retry_exponential_backoff",
    "exponential-backoff": "retry_exponential_backoff",
    "retry-backoff": "retry_exponential_backoff",
    "reb": "retry_exponential_backoff",
    "exponetial backoff": "retry_exponential_backoff",
    "exponential back-off": "retry_exponential_backoff",

    # Batch Result Aggregation
    "batch result aggregation": "batch_result_aggregation",
    "result aggregation": "batch_result_aggregation",
    "result aggregator": "batch_result_aggregation",
    "batch aggregator": "batch_result_aggregation",
    "batch aggregation": "batch_result_aggregation",
    "result collect": "batch_result_aggregation",
    "result collector": "batch_result_aggregation",
    "aggregation": "batch_result_aggregation",
    "aggregate results": "batch_result_aggregation",
    "aggregate batch results": "batch_result_aggregation",
    "bra": "batch_result_aggregation",
    "batch aggr": "batch_result_aggregation",
    "batch aggregration": "batch_result_aggregation",

    # Progress Tracking in Batch Jobs
    "progress tracking": "progress_tracking",
    "progress tracking in batch jobs": "progress_tracking",
    "batch progress tracking": "progress_tracking",
    "progress tracker": "progress_tracking",
    "batch progress": "progress_tracking",
    "batch tracker": "progress_tracking",
    "progress monitor": "progress_tracking",
    "batch monitor": "progress_tracking",
    "progress": "progress_tracking",
    "tracking": "progress_tracking",
    "track progress": "progress_tracking",
    "track batch progress": "progress_tracking",
    "pt": "progress_tracking",
    "progess tracking": "progress_tracking",
    "progress traking": "progress_tracking",

    # Error Isolation per Batch Item
    "error isolation": "error_isolation",
    "error isolation per batch item": "error_isolation",
    "batch error isolation": "error_isolation",
    "isolate errors": "error_isolation",
    "item error isolation": "error_isolation",
    "error isolation per item": "error_isolation",
    "error isolation batch": "error_isolation",
    "isolation": "error_isolation",
    "error handler": "error_isolation",
    "error handling": "error_isolation",
    "error isolator": "error_isolation",
    "error isolation batch item": "error_isolation",
    "ei": "error_isolation",
    "error_isolation": "error_isolation",
    "error-isolation": "error_isolation",

    # Partial Result Delivery
    "partial result delivery": "partial_result_delivery",
    "partial delivery": "partial_result_delivery",
    "partial results": "partial_result_delivery",
    "partial result": "partial_result_delivery",
    "partial batch results": "partial_result_delivery",
    "partial batch delivery": "partial_result_delivery",
    "partial delivery batch": "partial_result_delivery",
    "partial": "partial_result_delivery",
    "result partial delivery": "partial_result_delivery",
    "prd": "partial_result_delivery",
    "partial result delivry": "partial_result_delivery",
    "partial result delvery": "partial_result_delivery",

    # Batch Priority Queuing
    "batch priority queuing": "batch_priority_queuing",
    "priority queuing": "batch_priority_queuing",
    "priority queue": "batch_priority_queuing",
    "priority batch queue": "batch_priority_queuing",
    "batch queue": "batch_priority_queuing",
    "priority batching": "batch_priority_queuing",
    "batch priority queue": "batch_priority_queuing",
    "priority queueing": "batch_priority_queuing",
    "bpq": "batch_priority_queuing",
    "batch prio queue": "batch_priority_queuing",
    "batch prio queuing": "batch_priority_queuing",
    "batch prio": "batch_priority_queuing",
    "prio queue": "batch_priority_queuing",
    "prio queuing": "batch_priority_queuing",

    # Resource Budgeting per Batch
    "resource budgeting": "resource_budgeting",
    "resource budgeting per batch": "resource_budgeting",
    "batch resource budgeting": "resource_budgeting",
    "resource budget": "resource_budgeting",
    "batch resource budget": "resource_budgeting",
    "resource allocation": "resource_budgeting",
    "batch resource allocation": "resource_budgeting",
    "resource budget per batch": "resource_budgeting",
    "resource budgets": "resource_budgeting",
    "resource budgetting": "resource_budgeting",
    "rb": "resource_budgeting",
    "resource_budgeting": "resource_budgeting",

    # Batch Cancellation
    "batch cancellation": "batch_cancellation",
    "cancellation": "batch_cancellation",
    "cancel batch": "batch_cancellation",
    "cancel job": "batch_cancellation",
    "cancel": "batch_cancellation",
    "batch cancel": "batch_cancellation",
    "batch cancelation": "batch_cancellation",
    "batch cancelation": "batch_cancellation",
    "batch abort": "batch_cancellation",
    "abort batch": "batch_cancellation",
    "bc": "batch_cancellation",
    "batch_cancellation": "batch_cancellation",
    "batch-cancellation": "batch_cancellation",

    # Checkpoint/Resume for Large Batches
    "checkpoint resume": "checkpoint_resume",
    "checkpoint/resume": "checkpoint_resume",
    "checkpoint and resume": "checkpoint_resume",
    "checkpoint": "checkpoint_resume",
    "resume": "checkpoint_resume",
    "batch checkpoint": "checkpoint_resume",
    "batch resume": "checkpoint_resume",
    "checkpointing": "checkpoint_resume",
    "resuming": "checkpoint_resume",
    "checkpoint large batch": "checkpoint_resume",
    "resume large batch": "checkpoint_resume",
    "checkpoint batch": "checkpoint_resume",
    "resume batch": "checkpoint_resume",
    "cp": "checkpoint_resume",
    "checkpoint-resume": "checkpoint_resume",
    "checkpoint_resume": "checkpoint_resume",

    # Batch Result Caching
    "batch result caching": "batch_result_caching",
    "result caching": "batch_result_caching",
    "result cache": "batch_result_caching",
    "batch cache": "batch_result_caching",
    "batch caching": "batch_result_caching",
    "cache batch results": "batch_result_caching",
    "cache batch": "batch_result_caching",
    "batch result cache": "batch_result_caching",
    "brc": "batch_result_caching",
    "batch result chaching": "batch_result_caching",
    "batch result cashe": "batch_result_caching",

    # Deduplication within Batches
    "deduplication": "deduplication",
    "deduplication within batches": "deduplication",
    "batch deduplication": "deduplication",
    "deduplicate": "deduplication",
    "dedup": "deduplication",
    "dedup batch": "deduplication",
    "deduplicate batch": "deduplication",
    "deduplication batch": "deduplication",
    "deduplication in batch": "deduplication",
    "deduplication within batch": "deduplication",
    "deduplication batches": "deduplication",
    "deduplicationg": "deduplication",
    "ddp": "deduplication",

    # Batch Size Optimization
    "batch size optimization": "batch_size_optimization",
    "size optimization": "batch_size_optimization",
    "batch size": "batch_size_optimization",
    "optimize batch size": "batch_size_optimization",
    "batch optimize": "batch_size_optimization",
    "optimize size": "batch_size_optimization",
    "batch size optimize": "batch_size_optimization",
    "batch sizing": "batch_size_optimization",
    "batchsize optimization": "batch_size_optimization",
    "batch-size optimization": "batch_size_optimization",
    "bso": "batch_size_optimization",
    "batch size opt": "batch_size_optimization",
    "batch size optmization": "batch_size_optimization",

    # Memory Management for Large Batches
    "memory management": "memory_management",
    "memory management for large batches": "memory_management",
    "batch memory management": "memory_management",
    "memory manager": "memory_management",
    "batch memory manager": "memory_management",
    "memory mgmt": "memory_management",
    "memory mgmt batch": "memory_management",
    "manage memory": "memory_management",
    "batch memory": "memory_management",
    "memory management batch": "memory_management",
    "mm": "memory_management",
    "mem management": "memory_management",
    "mem mgmt": "memory_management",

    # Streaming Results
    "streaming results": "streaming_results",
    "result streaming": "streaming_results",
    "stream results": "streaming_results",
    "stream batch results": "streaming_results",
    "stream batch": "streaming_results",
    "batch streaming": "streaming_results",
    "streamed results": "streaming_results",
    "streaming": "streaming_results",
    "stream": "streaming_results",
    "results streaming": "streaming_results",
    "sr": "streaming_results",
    "streaming result": "streaming_results",

    # Batch SLA Enforcement
    "batch sla enforcement": "batch_sla_enforcement",
    "sla enforcement": "batch_sla_enforcement",
    "sla": "batch_sla_enforcement",
    "enforce sla": "batch_sla_enforcement",
    "batch sla": "batch_sla_enforcement",
    "enforce batch sla": "batch_sla_enforcement",
    "sla batch": "batch_sla_enforcement",
    "sla enforcement batch": "batch_sla_enforcement",
    "sla enforcement batching": "batch_sla_enforcement",
    "batch sla enforce": "batch_sla_enforcement",
    "bslae": "batch_sla_enforcement",

    # Batch Cost Estimation
    "batch cost estimation": "batch_cost_estimation",
    "cost estimation": "batch_cost_estimation",
    "cost estimate": "batch_cost_estimation",
    "estimate cost": "batch_cost_estimation",
    "batch cost estimate": "batch_cost_estimation",
    "cost estimator": "batch_cost_estimation",
    "batch cost estimator": "batch_cost_estimation",
    "cost estimation batch": "batch_cost_estimation",
    "cost estimation batching": "batch_cost_estimation",
    "bce": "batch_cost_estimation",
    "cost est": "batch_cost_estimation",

    # Batch Audit Logging
    "batch audit logging": "batch_audit_logging",
    "audit logging": "batch_audit_logging",
    "audit log": "batch_audit_logging",
    "batch audit log": "batch_audit_logging",
    "audit": "batch_audit_logging",
    "logging": "batch_audit_logging",
    "batch logging": "batch_audit_logging",
    "audit logs": "batch_audit_logging",
    "batch logs": "batch_audit_logging",
    "auditlogger": "batch_audit_logging",
    "batch auditlogger": "batch_audit_logging",
    "bal": "batch_audit_logging",
    "batch_audit_logging": "batch_audit_logging",
    "batch-audit-logging": "batch_audit_logging",
    "batch audit": "batch_audit_logging",
}

_EXPECTED_ENTRY_COUNT = 210

def _compute_map_hash():
    items = sorted((k, v) for k, v in SEMANTIC_MAP.items())
    hash_input = "".join(f"{k}:{v};" for k, v in items).encode("utf-8")
    return hashlib.sha256(hash_input).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

_integrity_lock = threading.Lock()

def verify_integrity():
    with _integrity_lock:
        actual_count = len(SEMANTIC_MAP)
        current_hash = _compute_map_hash()
        is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (current_hash == _MAP_INTEGRITY_HASH)
        return {
            "status": "ok" if is_valid else "invalid",
            "entries": actual_count,
            "hash": current_hash,
            "is_valid": is_valid,
        }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        return ""
    t = term.strip().lower()
    return SEMANTIC_MAP.get(t, t)

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)