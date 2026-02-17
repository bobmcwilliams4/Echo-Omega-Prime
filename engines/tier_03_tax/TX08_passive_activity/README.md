# TX08 Passive Activity Loss Engine

**Version:** 1.0.0
**Port:** 8608
**Domain:** tax_passive_activity
**Mode:** Hybrid
**Architecture:** TIE-20 Gold Standard

## Overview

IRC §469 passive activity loss analysis engine covering material participation tests, rental activity classification, real estate professional exception, grouping elections, disposition rules, self-rental recharacterization, PTP separate basket rules, and NIIT interaction.

## TIE-20 Components

1. ✅ **three_layer_response** - Doctrine Cache (0-200ms), Semantic Retrieval, Deep Analysis
2. ✅ **response_modes** - FAST, DEFENSE, MEMO
3. ✅ **doctrine_cache** - 15+ pre-compiled expert blocks with real IRC §469 content
4. ✅ **authority_hardening** - Hierarchical authority weighting
5. ✅ **confidence_stratification** - DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK
6. ✅ **semantic_normalization** - Domain-specific term normalization
7. ✅ **vector_search** - Semantic retrieval fallback
8. ✅ **telemetry** - Query tracing, latency tracking, coverage analysis
9. ✅ **drift_watcher** - Doctrine drift detection
10. ✅ **coverage_map** - Triggered/missed doctrine tracking
11. ✅ **metrics_collector** - Performance metrics
12. ✅ **health_endpoint** - Comprehensive health check
13. ✅ **zoned_analysis** - PLANNING/REPORTING/AUDIT zones
14. ✅ **fact_fragility_scoring** - Verifiability, recharacterization risk
15. ✅ **audit_trail_jsonl** - Forensic query log
16. ✅ **determinism_hash_sha256** - SHA-256 reproducibility
17. ✅ **fastapi_server** - Full FastAPI with CORS
18. ✅ **loguru_logging** - Structured logging, never print
19. ✅ **multi_doctrine_decomposition** - Issue stratification, interaction DAG
20. ✅ **deep_analysis_mode** - Multi-source synthesis

## Doctrine Topics (15+)

- Material Participation Test 1: 500 Hours
- Material Participation Test 2: Substantially All
- Material Participation Test 3: 100 Hours Not Less Than Anyone
- Material Participation Test 4: Significant Participation Aggregation
- Material Participation Test 5: 5 of 10 Prior Years
- Material Participation Test 6: Personal Service Activity 3 Years
- Material Participation Test 7: Facts and Circumstances
- Rental Activity Per Se Passive (IRC §469(c)(2))
- Real Estate Professional Exception (IRC §469(c)(7))
- $25,000 Rental Loss Allowance (IRC §469(i))
- Grouping of Activities (Reg. §1.469-4)
- Disposition of Entire Interest (IRC §469(g))
- Installment Sale Suspended Loss Release (IRC §469(g)(3))
- Self-Rental Recharacterization (Reg. §1.469-2(f)(6))
- Publicly Traded Partnership Separate Basket (IRC §469(k))
- Net Investment Income Tax Interaction (IRC §1411)

## API Endpoints

### POST /query
Query the passive activity engine.

**Request:**
```json
{
  "query": "How many hours do I need to materially participate?",
  "mode": "FAST",
  "zone": "PLANNING"
}
```

**Response:**
```json
{
  "query_id": "abc123",
  "conclusion": "Taxpayer materially participated if participation exceeded 500 hours during the tax year.",
  "reasoning": "IRC §469(h)(1) defines material participation...",
  "confidence_level": "DEFENSIBLE",
  "doctrines_triggered": [...],
  "primary_authority": ["IRC §469(h)(1)", "Temp. Reg. §1.469-5T(a)(1)"],
  "fact_fragility_score": 0.2,
  "substantiation_requirements": ["Contemporaneous time logs"],
  "planning_opportunities": ["Ensure operational work, not investment activity"],
  "latency_ms": 45.2,
  "determinism_hash": "a1b2c3d4e5f6"
}
```

### GET /health
Engine health check.

### GET /metrics
Performance metrics (queries, latency, coverage).

### GET /coverage
Doctrine coverage map (triggered vs. never triggered).

### GET /doctrines
List all doctrine topics.

## Usage

### Start Engine
```bash
cd O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\TX08_passive_activity
python engine.py
```

### Query via Python
```python
import requests

response = requests.post(
    "http://localhost:8608/query",
    json={
        "query": "Can I deduct rental losses if I work 600 hours managing the property?",
        "mode": "DEFENSE",
        "zone": "REPORTING"
    }
)

print(response.json()["conclusion"])
```

### Query via curl
```bash
curl -X POST http://localhost:8608/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the real estate professional test?", "mode": "FAST"}'
```

## Response Modes

- **FAST** (0-200ms): Concise analysis, primary conclusion, top authority
- **DEFENSE** (200-500ms): Audit-ready position with substantiation requirements
- **MEMO** (500ms-2s): Full documentation, multi-doctrine decomposition, deep analysis

## Analysis Zones

- **PLANNING**: Prospective planning, opportunities, strategies
- **REPORTING**: Return preparation, position documentation
- **AUDIT**: IRS examination defense, counter-arguments, resolution

## Confidence Levels

- **DEFENSIBLE**: Strong position, clear authority, well-substantiated
- **AGGRESSIVE**: Reasonable position but IRS may challenge
- **DISCLOSURE**: Borderline position, disclosure recommended
- **HIGH_RISK**: Weak position, high audit risk, avoid or restructure

## Issue Categories

- MATERIAL_PARTICIPATION
- RENTAL_ACTIVITY_CLASSIFICATION
- GROUPING_ELECTIONS
- DISPOSITION_RULES
- NIIT_INTERACTION
- RECHARACTERIZATION
- SUBSTANTIATION

## Dependencies

- FastAPI
- Pydantic
- loguru
- uvicorn

Install:
```bash
pip install fastapi pydantic loguru uvicorn
```

## Files

- `engine.py` (main engine, 800+ lines)
- `doctrines.py` (15+ doctrine blocks, 1200+ lines)
- `semantic.py` (normalization, 500+ lines)
- `search.py` (vector fallback, 300+ lines)
- `telemetry.py` (metrics/tracing, 400+ lines)
- `config.json` (configuration)

**Total:** 3,200+ lines of real IRC §469 expertise.

## Authority Coverage

- IRC §469 (Passive Activity Losses)
- IRC §469(c)(2) (Rental Activities)
- IRC §469(c)(7) (Real Estate Professional)
- IRC §469(g) (Disposition Rules)
- IRC §469(h) (Material Participation)
- IRC §469(i) ($25K Allowance)
- IRC §469(k) (PTP Rules)
- IRC §1411 (NIIT)
- Temp. Reg. §1.469-5T (Material Participation Tests)
- Reg. §1.469-4 (Grouping)
- Reg. §1.469-2(f)(6) (Self-Rental)
- Rev. Proc. 2010-13 (Regrouping)

## Examples

### Material Participation Test 1
**Query:** "How do I prove 500 hours of material participation?"

**Response:** Contemporaneous time logs showing operational work (management, decisions, vendor relations). Employee hours generally count if reasonable compensation. Exclude investment activity. Substantiate with appointment books, calendars, or narrative summaries.

### Real Estate Professional
**Query:** "What are the requirements to qualify as a real estate professional?"

**Response:** (1) >50% of personal services in real property trades or businesses, AND (2) >750 hours in real property trades or businesses. If qualified, rental real estate NOT per se passive - subject to material participation tests. Make grouping election to aggregate all rental real estate. High audit risk - contemporaneous time logs critical.

### $25K Allowance
**Query:** "Can I deduct rental losses against my W-2 income?"

**Response:** Up to $25,000 of rental real estate passive losses may offset non-passive income if (1) actively participated (10%+ ownership, management decisions), AND (2) AGI ≤$150,000. Phases out $1 for every $2 of AGI >$100,000. Active participation is lower standard than material participation - no hour requirement.

## Logging

Logs written to `engine.log` with rotation (100 MB) and retention (90 days).

## Audit Trail

All queries logged to `audit_trail.jsonl` in JSONL format for forensic review.

## Telemetry Export

Export full telemetry report:
```python
from telemetry import PassiveActivityTelemetry
from pathlib import Path

telemetry = PassiveActivityTelemetry()
telemetry.export_telemetry_report(Path("telemetry_report.json"))
```

---

**TX08 Passive Activity Loss Engine v1.0.0**
**ECHO OMEGA PRIME | TIE-20 Gold Standard**
