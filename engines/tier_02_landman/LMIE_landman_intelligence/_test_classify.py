"""Test classify endpoint — routing only, no engine launch."""
import httpx

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

passed = 0
failed = 0

with httpx.Client(timeout=5.0) as client:
    for target, query in TESTS:
        resp = client.post("http://localhost:8381/classify", json={"query": query})
        data = resp.json()
        routed = data.get("routed_engines", [])
        hit = target in routed
        status = "PASS" if hit else "MISS"
        if hit:
            passed += 1
        else:
            failed += 1
        cats = data.get("issue_categories", [])
        print(f"  [{status}] {target}: Routed={routed}  Cats={cats}", flush=True)

print(f"\nROUTING: {passed}/22 targets hit, {failed} missed", flush=True)
