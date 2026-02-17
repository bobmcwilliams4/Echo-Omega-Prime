import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

from engine import (
    ENGINE_ID, ENGINE_NAME, ENGINE_PORT, ENGINE_VERSION,
    DOCTRINE_CACHE, ENGINE_COST_PROFILES, MODEL_PRICING,
    ResponseMode, ConfidenceLevel, AnalysisZone, IssueCategory,
    calculate_cost_breakdown, three_layer_response, estimate_query_complexity,
    estimate_cache_hit_probability, BUDGET_TRACKER, TELEMETRY, DRIFT_WATCHER,
    COVERAGE_MAP, METRICS, score_fragility, compute_determinism_hash,
    normalize_query, decompose_query_to_doctrines, deep_analysis,
    apply_zone_constraints, resolve_authority_conflict, write_audit_entry,
    app
)

print(f"Engine: {ENGINE_ID} - {ENGINE_NAME} v{ENGINE_VERSION} port {ENGINE_PORT}")
print(f"Doctrine cache: {len(DOCTRINE_CACHE)} blocks")
print(f"Engine profiles: {len(ENGINE_COST_PROFILES)} engines")
print(f"Model pricing: {len(MODEL_PRICING)} models")
print(f"Issue categories: {len(list(IssueCategory))}")

# Test cost estimation
cost = calculate_cost_breakdown("TIE", "What are the tax implications of oil royalties?", ResponseMode.FAST)
print(f"TIE FAST cost: ${cost.total_cost_usd:.8f} | {cost.llm_input_tokens} in / {cost.llm_output_tokens} out | {cost.compute_ms}ms | {cost.wall_clock_seconds}s")

cost2 = calculate_cost_breakdown("LM05", "Chain of title for Section 270", ResponseMode.DEFENSE, chain_engines=["LM01", "LG08"])
print(f"LM05 chain cost: ${cost2.total_cost_usd:.8f} | chain_depth={cost2.chain_depth}")

cost3 = calculate_cost_breakdown("E05", "Due diligence on Acme Corp", ResponseMode.MEMO, batch_size=10)
print(f"E05 batch(10) MEMO cost: ${cost3.total_cost_usd:.8f} | batch_mult={cost3.batch_multiplier}")

# Test three_layer_response
resp = three_layer_response("Estimate cost of querying TIE for tax analysis", ResponseMode.FAST, AnalysisZone.REPORTING, target_engine="TIE")
print(f"Response: confidence={resp.confidence:.2f}, cache_hit={resp.doctrine_cache_hit}, latency={resp.latency_ms:.1f}ms")

# Test budget
BUDGET_TRACKER.record_cost("test_user", 0.005, "TIE")
status = BUDGET_TRACKER.get_status("test_user")
print(f"Budget: ${status.daily_spent_usd:.6f} daily, alert={status.alert_level.value}")

# Test complexity scoring
score, mult = estimate_query_complexity("What is the tax treatment of oil and gas royalties and how does it compare to mineral rights income over time?")
print(f"Complexity: score={score}/10, multiplier={mult:.2f}x")

# Test normalization
norm, kws = normalize_query("How much does the LLM token cost for a batch API call?")
print(f"Normalized: {norm[:80]}...")

# Test decomposition
doctrines = decompose_query_to_doctrines("budget limit monthly spend trend history")
print(f"Matched doctrines: {doctrines[:5]}")

print("\nALL TESTS PASSED")
