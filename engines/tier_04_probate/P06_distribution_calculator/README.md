# P06 Distribution Calculator Engine

**Version:** 1.0.0
**Port:** 8656
**Domain:** Estate Distribution Calculation
**TIE-20 Compliant:** Yes

## Overview

Estate distribution calculation engine for ECHO OMEGA PRIME. Calculates distributions per will provisions, intestacy statutes, tax apportionment, and executor commissions. No-LLM deterministic computation with comprehensive Texas estate law doctrine.

## Features

- **Testate Distribution**: Will-based distribution with abatement calculation
- **Intestate Distribution**: Texas statutory succession (§201.001-201.003)
- **Community Property Division**: Texas Family Code §3.001-3.007 compliant
- **Per Stirpes & Per Capita**: Both distribution methodologies supported
- **Estate Tax Apportionment**: IRC §2206/2207 recovery calculations
- **Executor Commissions**: Texas 5% statutory calculation (§352.002)
- **DNI Allocation**: IRC §661-663 distributable net income rules
- **In-Kind Distributions**: IRC §643(e) election analysis
- **Marital Deduction Formulas**: Fractional vs. pecuniary funding

## Architecture

### Files (3,218 total lines)

1. **engine.py** (897 lines) - Main FastAPI server with distribution calculation logic
2. **doctrines.py** (1,239 lines) - 8+ comprehensive doctrine blocks with real estate law expertise
3. **config.json** (138 lines) - Engine configuration with 50+ doctrine topics
4. **semantic.py** (351 lines) - Term normalization for consistent interpretation
5. **search.py** (240 lines) - Doctrine search and discovery engine
6. **telemetry.py** (353 lines) - Performance tracking and metrics collection

### TIE-20 Components

All 20 mandatory components implemented:

1. ✅ Three-layer response (doctrine cache, semantic, deep analysis)
2. ✅ Response modes (FAST, DEFENSE, MEMO)
3. ✅ Doctrine cache (8+ blocks with 40-80 lines each)
4. ✅ Authority hardening (statutory citations, case law)
5. ✅ Confidence stratification (DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK)
6. ✅ Semantic normalization (bequest types, property classifications)
7. ✅ Vector search (keyword-based with future vector DB support)
8. ✅ Telemetry (comprehensive query tracking)
9. ✅ Drift watcher (SHA-256 doctrine integrity)
10. ✅ Coverage map (triggered vs. available doctrines)
11. ✅ Metrics collector (latency, error rates, cache hits)
12. ✅ Health endpoint (/health with full stats)
13. ✅ Zoned analysis (PLANNING/REPORTING/AUDIT zones)
14. ✅ Fact fragility scoring (verifiability assessment)
15. ✅ Audit trail JSONL (append-only query log)
16. ✅ Determinism hash SHA-256 (reproducible calculations)
17. ✅ FastAPI server (async with CORS)
18. ✅ Loguru logging (structured, rotated)
19. ✅ Multi-doctrine decomposition (issue categorization)
20. ✅ Deep analysis mode (multi-source synthesis)

## Doctrine Coverage

### Core Topics (8 detailed blocks)

1. **Abatement Order** - Specific → Demonstrative → General → Residuary hierarchy
2. **Ademption by Extinction** - Identity theory vs. intent theory (UPC §2-606)
3. **Per Stirpes Distribution** - Family line preservation methodology
4. **Community Property at Death** - Texas §201.003, 50/50 division
5. **Distributable Net Income (DNI)** - IRC §661-663 allocation rules
6. **Estate Tax Apportionment** - IRC §2206/2207/2207A/2207B recovery
7. **IRC §643(e) Election** - In-kind distribution gain/loss recognition
8. **Marital Deduction Funding** - Fractional vs. pecuniary formulas

### Additional Coverage (42+ topics)

- Ademption by satisfaction, per capita at each generation, separate property intestacy
- Executor commissions, antilapse statutes, demonstrative legacies, trust accounting
- Attorney fees, GST tax, charitable deductions, disclaimers, fractional formulas
- Family allowance, homestead, exempt property, elective share, pretermitted heirs
- Simultaneous death, slayer statute, class gifts, powers of appointment, creditor priority

## API Endpoints

### POST /calculate

Calculate estate distribution.

**Request:**
```json
{
  "estate_id": "EST001",
  "decedent_name": "John Doe",
  "jurisdiction": "Texas",
  "marital_status": "married",
  "marriage_years": 15,
  "has_will": true,
  "assets": [
    {
      "asset_id": "A001",
      "description": "Primary residence",
      "fmv_at_death": 500000,
      "basis": 200000,
      "property_type": "COMMUNITY",
      "source": "earned"
    }
  ],
  "bequests": [
    {
      "beneficiary_name": "Jane Doe",
      "bequest_type": "SPECIFIC",
      "description": "Primary residence",
      "amount": null,
      "property_id": "A001",
      "priority": 1
    }
  ],
  "response_mode": "DEFENSE"
}
```

**Response:**
```json
{
  "estate_id": "EST001",
  "timestamp": "2026-02-12T06:50:00Z",
  "total_estate_value": 500000,
  "total_debts": 0,
  "net_distributable": 475000,
  "distributions": [...],
  "estate_tax": 0,
  "executor_commission": 25000,
  "confidence": "DEFENSIBLE",
  "reasoning": "Estate distributed per will provisions...",
  "authorities_cited": ["Texas Estates Code §201.001-201.003", ...],
  "warnings": [...],
  "sha256_hash": "abc123..."
}
```

### GET /health

Health check with telemetry stats.

### GET /doctrines

List all doctrine topics or search by keyword.

### GET /config

Retrieve engine configuration.

## Usage Example

```python
import requests

response = requests.post("http://localhost:8656/calculate", json={
    "estate_id": "EST001",
    "decedent_name": "John Smith",
    "marital_status": "married",
    "marriage_years": 20,
    "has_will": False,
    "assets": [
        {
            "asset_id": "A001",
            "description": "Community property - home",
            "fmv_at_death": 800000,
            "basis": 300000,
            "property_type": "COMMUNITY",
            "source": "earned"
        }
    ],
    "descendants": [
        {"name": "Child 1", "is_alive": True, "generation": 1, "descendants": []},
        {"name": "Child 2", "is_alive": True, "generation": 1, "descendants": []}
    ],
    "surviving_spouse": "Jane Smith",
    "distribution_method": "PER_CAPITA_EACH_GEN",
    "response_mode": "DEFENSE"
})

result = response.json()
print(f"Net distributable: ${result['net_distributable']}")
for dist in result['distributions']:
    print(f"{dist['beneficiary']}: ${dist['amount']}")
```

## Running the Engine

```bash
# Install dependencies
pip install fastapi uvicorn pydantic loguru

# Start server
python engine.py

# Or with uvicorn directly
uvicorn engine:app --host 0.0.0.0 --port 8656 --reload
```

## Testing

```bash
# Health check
curl http://localhost:8656/health

# Search doctrines
curl http://localhost:8656/doctrines?keyword=abatement

# Calculate simple distribution
curl -X POST http://localhost:8656/calculate \
  -H "Content-Type: application/json" \
  -d @test_estate.json
```

## Integration

This engine integrates with:

- **OMNISCIENT Cloud**: Cross-instance state sync
- **Cloud Retriever**: R2/D1 fallback for large doctrine sets
- **Build Orchestrator**: Automatic deployment and monitoring
- **Crystal Memory**: Persistent calculation history

## Authorities

Primary legal authorities:

- Texas Estates Code §§201.001-201.003, 255.001-.406, 352.001-.003, 355.109
- Texas Family Code §§3.001-3.007
- IRC §§641-685, 2001-2209, 2056, 2206-2207B, 643(e), 661-663
- UPC §§2-106, 2-605, 2-606, 2-609, 3-902
- Uniform Principal and Income Act (UPIA) §§102-104, 401-415
- Restatement (Third) of Property: Wills and Other Donative Transfers

## License

ECHO OMEGA PRIME Internal Use Only
Commander: Bobby Don McWilliams II
Built: 2026-02-12

---

**TIE-20 Certified** | **No-LLM Deterministic** | **Production Ready**
