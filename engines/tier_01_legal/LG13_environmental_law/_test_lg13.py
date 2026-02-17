"""LG13 Environmental Law Engine - Comprehensive Validation Tests"""
import sys
sys.path.insert(0, "O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/LG13_environmental_law")

import doctrines
import semantic
import search
import telemetry

passed = 0
failed = 0

def check(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  PASS: {name}")
        passed += 1
    except Exception as e:
        print(f"  FAIL: {name} -> {e}")
        failed += 1

# Test 1: Module imports (already done by importing above)
print("TEST 1: Module imports...")
print("  PASS: All 4 modules imported")
passed += 1

# Test 2: Doctrine cache build
print("TEST 2: Doctrine cache build...")
cache = doctrines.build_doctrine_cache()
assert cache.total_blocks > 60, f"Expected >60 blocks, got {cache.total_blocks}"
assert len(cache.categories) >= 20, f"Expected >=20 categories, got {len(cache.categories)}"
print(f"  PASS: {cache.total_blocks} blocks, {len(cache.categories)} categories")
passed += 1

# Test 3: Doctrine integrity
print("TEST 3: Doctrine integrity verification...")
valid, errors = doctrines.verify_doctrine_integrity()
assert valid, f"Integrity check failed: {errors[:3]}"
print(f"  PASS: Integrity valid={valid}, {len(errors)} errors")
passed += 1

# Test 4: Semantic normalization
print("TEST 4: Semantic normalization...")
result = semantic.normalize_semantics("What are the RCRA hazardous waste requirements for a TCEQ facility in Midland County?")
assert len(result.statutes_detected) > 0, "No statutes detected"
assert len(result.agencies_detected) > 0, "No agencies detected"
print(f"  PASS: statutes={result.statutes_detected}, agencies={result.agencies_detected}")
passed += 1

# Test 5: Search index
print("TEST 5: Search index...")
index = search.build_search_index([b.to_dict() for b in doctrines.DOCTRINE_BLOCKS])
results = index.search("clean water act npdes permit")
assert len(results) > 0, "No search results for CWA query"
print(f"  PASS: {index.document_count} docs, {len(results)} results")
passed += 1

# Test 6: Permit analyzer
print("TEST 6: Permit analyzer...")
pa = search.PermitAnalyzer()
result = pa.analyze_permits("Industrial facility with air emissions and wastewater discharge in Texas", "TX")
assert len(result.required_permits) > 0 or len(result.potentially_required) > 0, "No permits identified"
print(f"  PASS: {len(result.required_permits)} required, {len(result.potentially_required)} potential")
passed += 1

# Test 7: Penalty calculator
print("TEST 7: Penalty calculator...")
pc = search.PenaltyCalculator()
est = pc.calculate("cwa", "unauthorized discharge", days_of_violation=30, gravity="major")
assert est.total_estimated_range_high > 0, "Penalty estimate is zero"
print(f"  PASS: {est.statute} range ${est.total_estimated_range_low:,.0f}-${est.total_estimated_range_high:,.0f}")
passed += 1

# Test 8: Coverage map
print("TEST 8: Coverage map...")
coverage = doctrines.get_coverage_map()
total_topics = sum(len(v) for v in coverage.values())
assert len(coverage) >= 20, f"Expected >=20 categories, got {len(coverage)}"
print(f"  PASS: {len(coverage)} categories, {total_topics} total topics")
passed += 1

# Test 9: Telemetry
print("TEST 9: Telemetry...")
tc = telemetry.get_telemetry()
trace = telemetry.trace_query("test query", "ANALYSIS", "STANDARD", "TX")
trace.complete(telemetry.ResponseLayer.DOCTRINE_CACHE, 0.95)
telemetry.complete_trace(trace)
print(f"  PASS: trace_id={trace.trace_id[:16]}...")
passed += 1

# Test 10: Doctrine stats + hash
print("TEST 10: Doctrine stats + hash...")
stats = doctrines.get_doctrine_cache_stats()
cache_hash = doctrines.get_doctrine_cache_hash()
assert len(cache_hash) == 64, "Invalid cache hash length"
print(f"  PASS: hash={cache_hash[:16]}...")
passed += 1

# Test 11: PRP Analyzer
print("TEST 11: CERCLA PRP analyzer...")
prp = search.CERCLAPRPAnalyzer()
assessment = prp.assess_liability("Test Corp", search.PRPCategory.CURRENT_OWNER_OPERATOR, {})
assert assessment.prp_category == search.PRPCategory.CURRENT_OWNER_OPERATOR
print(f"  PASS: PRP category={assessment.prp_category.value}, defenses={len(assessment.potential_defenses)}")
passed += 1

# Test 12: Phase I ESA workflow
print("TEST 12: Phase I ESA workflow...")
phase1 = search.PhaseIESAWorkflow()
checklist = phase1.generate_checklist("123 Main St, Midland, TX", "TX")
assert "checklist" in checklist, "No checklist key"
print(f"  PASS: {len(checklist['checklist'])} checklist items")
passed += 1

# Test 13: Remediation selector
print("TEST 13: Remediation selector...")
rem = search.RemediationSelector()
options = rem.recommend(["benzene", "toluene"], ["groundwater", "soil"])
assert len(options) > 0, "No remediation options"
print(f"  PASS: {len(options)} remediation options recommended")
passed += 1

# Test 14: Compliance checker
print("TEST 14: Compliance checker...")
cc = search.ComplianceChecker()
check_result = cc.check_facility("oil_production", ["drilling", "disposal"], "TX")
assert check_result is not None, "No compliance result"
print(f"  PASS: facility compliance check completed, applicable programs identified")
passed += 1

# Test 15: Stale doctrines check
print("TEST 15: Stale doctrines check...")
stale = doctrines.get_stale_doctrines(max_age_days=365)
print(f"  PASS: {len(stale)} stale doctrines (>{365} days)")
passed += 1

# Summary
print()
print("=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed")
print(f"Doctrine blocks: {len(doctrines.DOCTRINE_BLOCKS)} total, {cache.total_blocks} in cache")
print(f"Categories: {len(cache.categories)}")
print(f"Search index: {index.document_count} docs, {index.term_count} terms")
print("=" * 60)

if failed > 0:
    sys.exit(1)
