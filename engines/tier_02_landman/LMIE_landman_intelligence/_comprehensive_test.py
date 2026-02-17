"""Comprehensive LMIE test — one query per child engine category."""
import httpx
import json
import time
import sys

LMIE_URL = "http://localhost:8381/query"
TIMEOUT = 90.0  # increased for auto-launch warmup (LM09 needs ~35s)

# Queries designed to trigger specific child engines — matched to classify test
TESTS = [
    ("LM01", "Examine the title for Section 270 Block 8 H&TC Survey Reeves County"),
    ("LM02", "Analyze the oil and gas lease terms for the McWilliams Ranch lease agreement"),
    ("LM03", "Calculate the division order decimal interest for Section 270 owners"),
    ("LM04", "Analyze the pooling and unitization order for Section 270 Block 8"),
    ("LM05", "Build a chain of title for Section 270 Block 8 Lots 1 and 2 Reeves County"),
    ("LM06", "Analyze the right of way easement across Section 270 for pipeline access"),
    ("LM07", "What RRC regulatory filings and permits are required for drilling in Reeves County"),
    ("LM08", "Perform due diligence review on the mineral acquisition in Section 270"),
    ("LM09", "Generate a runsheet for Section 270 Block 8 H&TC Survey Reeves County"),
    ("LM10", "What curative actions are needed to cure the gap in title for Section 270"),
    ("LM11", "Negotiate the lease terms and royalty rate for the McWilliams Ranch"),
    ("LM12", "Map the GIS coordinates and survey boundaries for Section 270 Block 8"),
    ("LM13", "Analyze water rights and groundwater permits for Section 270 Block 8"),
    ("LM14", "Analyze the surface and subsurface easement on Section 270"),
    ("LM15", "Analyze the pooling unit and spacing requirements for Section 270"),
    ("LM16", "Review the wind energy and solar lease terms for the ranch in Section 270"),
    ("LM17", "Draft a surface use agreement for drilling operations on Section 270"),
    ("LM18", "Underwrite title insurance for the mineral acquisition in Section 270"),
    ("LM19", "Analyze the probate title issues for the Hill Trust Estate in Section 270"),
    ("LM20", "What Indian land and tribal mineral ownership affects Section 270"),
    ("LM21", "Analyze federal land and BLM leases and GLO ownership in Reeves County"),
    ("LM22", "What coal rights and mineral claimant disputes affect Section 270"),
]

def main():
    results = []
    passed = 0
    failed = 0

    for engine_id, query in TESTS:
        print(f"\n{'='*60}", flush=True)
        print(f"Testing {engine_id}: {query[:60]}...", flush=True)

        start = time.time()
        try:
            with httpx.Client(timeout=TIMEOUT) as client:
                resp = client.post(LMIE_URL, json={"query": query, "mode": "FAST"})
                elapsed = time.time() - start

                if resp.status_code == 200:
                    data = resp.json()
                    routed = data.get("routed_engines", [])
                    child_results = data.get("child_results", [])
                    child_count = len(child_results) if isinstance(child_results, list) else 0
                    synthesis_len = len(data.get("synthesis", ""))

                    # Check if target engine was triggered
                    triggered = engine_id in routed

                    # Check child results for errors
                    child_errors = []
                    child_ok = []
                    if isinstance(child_results, list):
                        for cr in child_results:
                            eid = cr.get("engine_id", "?")
                            if cr.get("error") or cr.get("status") == "error":
                                child_errors.append(f"{eid}: {(cr.get('error') or 'unknown')[:80]}")
                            else:
                                child_ok.append(eid)
                    elif isinstance(child_results, dict):
                        for cid, cres in child_results.items():
                            if isinstance(cres, dict) and cres.get("error"):
                                child_errors.append(f"{cid}: {cres['error'][:80]}")
                            else:
                                child_ok.append(cid)

                    if triggered and not child_errors:
                        status = "PASS"
                        passed += 1
                    elif triggered and child_errors:
                        status = "PARTIAL"
                        failed += 1
                    elif not triggered and not child_errors:
                        status = "MISS"
                        failed += 1
                    else:
                        status = "FAIL"
                        failed += 1

                    print(f"  [{status}] {elapsed:.1f}s | Routed: {routed} | OK: {child_ok} | Synthesis: {synthesis_len} chars", flush=True)
                    if child_errors:
                        for e in child_errors:
                            print(f"  ERROR: {e}", flush=True)

                    results.append({
                        "engine": engine_id,
                        "status": status,
                        "time_s": round(elapsed, 1),
                        "routed_to": routed,
                        "child_ok": child_ok,
                        "child_count": child_count,
                        "synthesis_len": synthesis_len,
                        "errors": child_errors,
                    })
                else:
                    elapsed = time.time() - start
                    failed += 1
                    print(f"  [FAIL] HTTP {resp.status_code} in {elapsed:.1f}s", flush=True)
                    results.append({
                        "engine": engine_id,
                        "status": "FAIL",
                        "http_code": resp.status_code,
                        "time_s": round(elapsed, 1),
                    })
        except Exception as e:
            elapsed = time.time() - start
            failed += 1
            print(f"  [FAIL] {type(e).__name__}: {e}", flush=True)
            results.append({
                "engine": engine_id,
                "status": "FAIL",
                "error": str(e),
                "time_s": round(elapsed, 1),
            })

    print(f"\n{'='*60}", flush=True)
    print(f"RESULTS: {passed} PASS, {failed} FAIL/PARTIAL/MISS out of {len(TESTS)}", flush=True)
    print(f"{'='*60}", flush=True)

    # Summary table
    print(f"\n{'Engine':<8} {'Status':<10} {'Time':<8} {'Routed To':<40} {'Errors'}", flush=True)
    print("-" * 110, flush=True)
    for r in results:
        routed = ", ".join(r.get("routed_to", []))
        errors = "; ".join(r.get("errors", []))[:60]
        print(f"{r['engine']:<8} {r['status']:<10} {r['time_s']:<8.1f} {routed:<40} {errors}", flush=True)

    with open("_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to _test_results.json", flush=True)

if __name__ == "__main__":
    main()
