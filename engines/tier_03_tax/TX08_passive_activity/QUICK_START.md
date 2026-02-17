# TX08 Passive Activity Loss Engine - Quick Start

## Installation

```bash
cd O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\TX08_passive_activity
pip install fastapi pydantic loguru uvicorn
```

## Start the Engine

```bash
python engine.py
```

Engine starts on `http://localhost:8608`

## Test the Engine

```bash
python test_engine.py
```

Expected output: 10/10 tests passed

## Example Queries

### 1. Material Participation - 500 Hours (Test 1)

**Query:** "How many hours do I need to work to materially participate in my S corporation?"

**Expected Response:**
- Conclusion: "Taxpayer materially participated in the activity if participation exceeded 500 hours during the tax year."
- Authority: IRC §469(h)(1), Temp. Reg. §1.469-5T(a)(1)
- Confidence: DEFENSIBLE
- Latency: <200ms (FAST mode)

### 2. Real Estate Professional

**Query:** "What are the requirements to qualify as a real estate professional under IRC 469(c)(7)?"

**Expected Response:**
- Conclusion: Two-part test - >50% of services in real property trades/businesses AND >750 hours
- Authority: IRC §469(c)(7)
- Confidence: DEFENSIBLE (if documented) or AGGRESSIVE (if thin substantiation)
- Substantiation: Contemporaneous time logs critical

### 3. $25,000 Rental Loss Allowance

**Query:** "Can I deduct rental losses against my W-2 income if my AGI is $120,000?"

**Expected Response:**
- Conclusion: Up to $25K allowance phases out between $100K-$150K AGI
- At $120K AGI: $25K - (($120K - $100K) × 50%) = $15,000 allowance
- Requirements: Active participation (10%+ ownership, management decisions)
- Authority: IRC §469(i)

### 4. Grouping of Activities

**Query:** "Can I group my three rental properties into one activity for material participation?"

**Expected Response:**
- Conclusion: Yes, if they constitute an appropriate economic unit
- Factors: Same business type, common control/ownership, location, interdependencies
- Authority: Reg. §1.469-4
- Benefit: Aggregates hours across all grouped properties

### 5. Disposition - Suspended Losses

**Query:** "If I sell my rental property with $50,000 of suspended passive losses, can I deduct them?"

**Expected Response:**
- Conclusion: Yes, if entire interest disposed in fully taxable transaction to unrelated party
- Suspended losses offset: (1) activity income, (2) other passive income, (3) non-passive income
- Authority: IRC §469(g)
- Watch out: Installment sale uses pro-rata release (IRC §469(g)(3))

### 6. Self-Rental Recharacterization

**Query:** "I own a building and lease it to my S corporation where I materially participate. Is the rental income passive?"

**Expected Response:**
- Conclusion: NO - rental income is recharacterized as NON-PASSIVE (self-rental rule)
- Only NET INCOME recharacterized (losses remain passive)
- Authority: Reg. §1.469-2(f)(6)
- Planning: Consider renting to unrelated third party to avoid rule

## Python SDK Usage

```python
import requests

# Query the engine
response = requests.post(
    "http://localhost:8608/query",
    json={
        "query": "How do I prove material participation?",
        "mode": "FAST",      # FAST, DEFENSE, or MEMO
        "zone": "PLANNING"   # PLANNING, REPORTING, or AUDIT
    }
)

result = response.json()

print(f"Conclusion: {result['conclusion']}")
print(f"Confidence: {result['confidence_level']}")
print(f"Latency: {result['latency_ms']:.1f}ms")
print(f"Authority: {result['primary_authority'][0]}")
```

## Health Check

```bash
curl http://localhost:8608/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "port": 8608,
  "doctrine_count": 16,
  "total_queries": 42,
  "avg_latency_ms": 123.4,
  "coverage_percentage": 68.8,
  "drift_observations": 0,
  "uptime_seconds": 3600.5
}
```

## Metrics

```bash
curl http://localhost:8608/metrics
```

Response includes:
- Total queries
- Average latency
- Vector search rate
- Error rate
- Queries by mode (FAST/DEFENSE/MEMO)
- Queries by category
- Latency percentiles (p50, p90, p95, p99)

## Coverage Map

```bash
curl http://localhost:8608/coverage
```

Shows which doctrine blocks have been triggered vs. never triggered.

## Response Modes

### FAST (0-200ms)
- Concise conclusion
- Primary authority
- Top doctrine match
- Minimal reasoning

**Use for:** Quick answers, initial assessment

### DEFENSE (200-500ms)
- Full conclusion (all sentences)
- Substantiation requirements
- Adversary position
- Counter-arguments
- Resolution strategy

**Use for:** Return preparation, position documentation

### MEMO (500ms-2s)
- Deep analysis with multi-source synthesis
- Multi-doctrine decomposition
- Planning opportunities
- Fact fragility scoring
- Full reasoning chain

**Use for:** Complex planning, formal documentation, research

## Analysis Zones

### PLANNING
- Prospective planning
- Opportunities and strategies
- Forward-looking analysis

### REPORTING
- Return preparation
- Position documentation
- Filing position support

### AUDIT
- IRS examination defense
- Counter-arguments
- Resolution strategies
- Adversary position analysis

## Confidence Levels

### DEFENSIBLE
- Strong position
- Clear authority
- Well-substantiated
- Low audit risk

### AGGRESSIVE
- Reasonable position
- IRS may challenge
- Adequate authority but not clear-cut
- Moderate audit risk

### DISCLOSURE
- Borderline position
- Disclosure recommended (Form 8275)
- Uncertain authority or facts
- High audit risk

### HIGH_RISK
- Weak position
- High audit risk
- Avoid or restructure
- Insufficient authority or substantiation

## Common Queries

1. "Can I deduct passive losses?" → Depends on material participation or $25K allowance
2. "How do I qualify as a real estate professional?" → >50% + >750 hours in real property
3. "What happens to suspended losses when I sell?" → Fully deductible if entire interest disposed
4. "Can I group my rental properties?" → Yes, if appropriate economic unit
5. "Do my hours as an S corp employee count?" → Generally yes, for material participation
6. "What is active participation?" → 10%+ ownership + management decisions (lower than material)
7. "How do I substantiate hours?" → Contemporaneous time logs (gold standard)
8. "What is self-rental rule?" → Net rental income to own business = non-passive

## Troubleshooting

### Engine won't start
- Check port 8608 is available: `netstat -ano | findstr 8608`
- Install dependencies: `pip install fastapi pydantic loguru uvicorn`

### Import errors
- Ensure Python 3.11+
- Check all files present (engine.py, doctrines.py, semantic.py, search.py, telemetry.py, config.json)

### Slow queries
- FAST mode should be <200ms
- DEFENSE mode <500ms
- MEMO mode <2s
- If slower, check system resources

### No doctrine matches
- Check query contains passive activity keywords
- Try semantic variants ("material participation" vs "500 hours")
- Use /doctrines endpoint to see available topics

## Files Summary

- **engine.py** (855 lines) - Main TIE-20 engine, FastAPI server
- **doctrines.py** (1,297 lines) - 16 doctrine blocks with real IRC §469 content
- **semantic.py** (336 lines) - Domain-specific term normalization
- **search.py** (272 lines) - Vector search fallback
- **telemetry.py** (303 lines) - Metrics, tracing, coverage analysis
- **config.json** (113 lines) - Engine configuration
- **test_engine.py** (359 lines) - Comprehensive test suite

**Total: 3,535+ lines of production-grade IRC §469 expertise**

## Next Steps

1. Start engine: `python engine.py`
2. Run tests: `python test_engine.py`
3. Query via curl or Python SDK
4. Review metrics and coverage
5. Integrate into larger ECHO OMEGA PRIME system

---

**TX08 Passive Activity Loss Engine v1.0.0**
**TIE-20 Gold Standard | ECHO OMEGA PRIME**
