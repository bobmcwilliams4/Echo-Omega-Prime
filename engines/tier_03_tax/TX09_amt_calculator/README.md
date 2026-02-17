# TX09 AMT Calculator Engine

**Alternative Minimum Tax Intelligence System**

Version: 1.0.0 | Port: 8609 | Domain: IRC §55-59

---

## Quick Start

```bash
# Navigate to engine directory
cd O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX09_amt_calculator

# Start the engine
uvicorn engine:app --host 0.0.0.0 --port 8609 --reload

# Access the API
curl http://localhost:8609/health
```

**API Documentation:** http://localhost:8609/docs

---

## What This Engine Does

The TX09 AMT Calculator is a professional-grade Alternative Minimum Tax intelligence system that:

1. **Calculates AMT liability** using IRC §55-59 framework
2. **Analyzes AMT scenarios** with expert pre-compiled reasoning
3. **Provides strategic guidance** for AMT planning and mitigation
4. **Offers audit-ready documentation** with burden analysis and IRS positions

---

## Core Features

### Three-Layer Architecture

1. **Doctrine Cache (0-200ms)** — 50+ pre-compiled AMT expert reasoning blocks
2. **Semantic Retrieval (200-700ms)** — Fast knowledge base search
3. **Deep Analysis (on-demand)** — Multi-source synthesis for complex scenarios

### AMT Calculation Engine

- **AMTI Calculation:** Regular income + adjustments + preferences
- **Exemption Calculation:** 2024 amounts with 25% phase-out
- **Tentative AMT:** 26% / 28% graduated rates
- **AMT Liability:** Excess over regular tax
- **Credit Tracking:** Minimum tax credit (MTC) carryforward

### Response Modes

- **FAST:** Quick doctrine-driven answers (< 2 seconds)
- **DEFENSE:** Audit-ready analysis with burden analysis
- **MEMO:** Long-form documentation with comprehensive citations

---

## Example Usage

### Query the Engine

```bash
curl -X POST http://localhost:8609/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How does AMT exemption phase-out work for married filing jointly?",
    "mode": "defense",
    "entity_type": "individual",
    "tax_year": 2024
  }'
```

### Direct AMT Calculation

```bash
curl -X POST http://localhost:8609/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "regular_income": 500000,
    "adjustments": {
      "depreciation": 50000,
      "iso": 100000
    },
    "preferences": {
      "pab_interest": 20000
    },
    "filing_status": "married_joint"
  }'
```

### Check System Health

```bash
curl http://localhost:8609/health
```

---

## AMT Coverage

### IRC Sections

- **§55** — AMT framework, rates, exemption
- **§56** — Adjustments (depreciation, ISO, SALT, NOL, etc.)
- **§57** — Preferences (PAB interest, depletion, IDCs)
- **§53** — Minimum tax credit
- **§59** — Corporate AMT (CAMT)

### Key Topics

- AMT calculation methodology
- Exemption amounts and phase-out (2024: $85,700 single, $133,300 MFJ)
- Depreciation adjustments (ADS vs MACRS)
- Incentive stock option (ISO) exercise spread
- Private activity bond interest
- State and local tax (SALT) interaction post-TCJA
- Net operating loss (NOL) 90% limitation
- Corporate CAMT (15% on adjusted financial statement income)
- AMT credit generation and utilization
- Planning strategies and timing considerations

---

## Architecture

### Files

- **engine.py** (1,027 lines) — Core intelligence engine
- **doctrines.py** (611 lines) — 50+ AMT expert reasoning blocks
- **semantic.py** (336 lines) — Query normalization
- **search.py** (314 lines) — Vector search fallback
- **telemetry.py** (532 lines) — Performance monitoring
- **config.json** (277 lines) — Configuration

### TIE-20 Components

All 20 mandatory Tax Intelligence Engine components implemented:

1. Three-layer response
2. Response modes (FAST/DEFENSE/MEMO)
3. Doctrine cache (50+ blocks)
4. Authority hardening
5. Confidence stratification
6. Semantic normalization
7. Vector search
8. Telemetry
9. Drift watcher
10. Coverage map
11. Metrics collector
12. Health endpoint
13. Zoned analysis (PLANNING/REPORTING/AUDIT)
14. Fact fragility scoring
15. Audit trail (JSONL)
16. Determinism hash (SHA-256)
17. FastAPI server
18. Loguru logging
19. Multi-doctrine decomposition
20. Deep analysis mode

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Engine status |
| `/query` | POST | AMT query processing |
| `/calculate` | POST | Direct AMT calculation |
| `/health` | GET | System health check |
| `/doctrines` | GET | List doctrine topics |
| `/drift` | GET | Doctrine drift detection |

---

## Performance

- **Doctrine Layer:** < 200ms target
- **Retrieval Layer:** < 700ms target
- **P95 Latency:** < 500ms target
- **P99 Latency:** < 1000ms target
- **Doctrine Hit Rate:** > 80% target
- **Error Rate:** < 5% threshold

---

## Logging & Monitoring

All logs stored in: `O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/TX09_amt_calculator/logs/`

- **amt_engine_*.log** — General engine logs (50 MB rotation, 30-day retention)
- **traces.jsonl** — Query trace log
- **errors.jsonl** — Error event log
- **audit_trail.jsonl** — Audit trail for compliance

---

## Dependencies

- Python 3.11+
- FastAPI ^0.100.0
- Pydantic ^2.0.0
- uvicorn ^0.23.0
- loguru ^0.7.0
- psutil ^5.9.0

---

## Development

### Run Tests

```bash
python test_amt.py
```

### Verify Imports

```bash
python -c "from engine import app; print('✓ Engine ready')"
```

### Check Metrics

```bash
curl http://localhost:8609/health | python -m json.tool
```

---

## Integration

### Build Orchestrator

- **URL:** https://echo-build-orchestrator.bmcii1976.workers.dev
- **Registration:** POST /engines with TX09 metadata
- **Status:** POST /build/complete when deployed

### Omniscient Sync

- **URL:** https://omniscient-sync.bmcii1976.workers.dev
- **Sync:** GET /policies, POST /sessions/register

---

## License

ECHO OMEGA PRIME — Authority 11.0 SOVEREIGN

---

## Support

For technical support or questions:
- Engine logs: Check `logs/` directory
- Health check: http://localhost:8609/health
- API docs: http://localhost:8609/docs

---

**Built:** 2026-02-12
**Status:** Production Ready
**Quality:** TIE-20 Gold Standard
