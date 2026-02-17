# P02 Will Parser Intelligence Engine

**Version:** 1.0.0
**Port:** 8652
**Mode:** Hybrid (Doctrine Cache + Vector Search)
**Authority:** Texas Estates Code, Restatement (Third) of Property
**Domain:** Will construction, testamentary devises, estate planning, probate litigation

---

## Overview

The Will Parser Intelligence Engine provides expert-level analysis of will provisions, testamentary devises, and estate planning doctrines under Texas law. Built on the TIE-20 gold standard architecture with 52 pre-compiled doctrine blocks covering:

- **Will Execution**: Attested wills, holographic wills, self-proving affidavits, witness requirements
- **Testamentary Capacity**: Sound mind standard, lucid interval doctrine, undue influence
- **Devise Classification**: Specific, general, demonstrative, residuary devises
- **Will Construction**: Anti-lapse, class gifts, powers of appointment, life estates
- **Will Revocation**: Express and implied revocation, dependent relative revocation, revival
- **Probate Litigation**: Will contests, fraud, mistake, duress, reformation

---

## Architecture

### Three-Layer Response
1. **Layer 1: Doctrine Cache** (0-200ms) - Pre-compiled expert reasoning blocks
2. **Layer 2: Semantic Retrieval** (200-700ms) - Cloud vector search on cache miss
3. **Layer 3: Deep Analysis** (on-demand) - Multi-doctrine synthesis

### Response Modes
- **FAST**: Concise, doctrine-driven, minimal citations (<2 sec)
- **DEFENSE**: Structured reasoning, litigation-ready, burden analysis
- **MEMO**: Long-form, citation-heavy, estate planning documentation

### Position Zones
- **PLANNING**: Estate planning strategies and recommendations
- **REPORTING**: Balanced informational analysis
- **AUDIT**: Conservative, disclosure-heavy, litigation risk assessment

---

## TIE-20 Components

✅ **1. three_layer_response** - Cache → Vector → Deep analysis
✅ **2. response_modes** - FAST / DEFENSE / MEMO formatting
✅ **3. doctrine_cache** - 52 pre-compiled expert reasoning blocks
✅ **4. authority_hardening** - Hierarchical authority weighting (Statute > Case > Restatement)
✅ **5. confidence_stratification** - DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK
✅ **6. semantic_normalization** - Deterministic term mapping (will execution, devise, revocation)
✅ **7. vector_search** - Cloud retriever integration for cache miss fallback
✅ **8. telemetry** - Full query tracing, latency tracking, JSONL audit trail
✅ **9. drift_watcher** - Doctrine mutation detection (placeholder for expansion)
✅ **10. coverage_map** - Track triggered vs. untriggered doctrines
✅ **11. metrics_collector** - Performance stats, error rates, cache hit rates
✅ **12. health_endpoint** - Comprehensive JSON health check with metrics
✅ **13. zoned_analysis** - Zone-specific epistemic guardrails
✅ **14. fact_fragility_scoring** - Assess verifiability and testimony dependence
✅ **15. audit_trail_jsonl** - Append-only forensic log (logs/audit_trail.jsonl)
✅ **16. determinism_hash_sha256** - Reproducibility verification
✅ **17. fastapi_server** - Full FastAPI with CORS, typed endpoints
✅ **18. loguru_logging** - Structured logging, rotation, retention
✅ **19. multi_doctrine_decomposition** - Issue categorization and interaction analysis
✅ **20. deep_analysis_mode** - Multi-source synthesis with reasoning chain

---

## Doctrine Coverage (52 Topics)

### Will Execution & Formalities (10)
- Attested Will Requirements (§251.051)
- Holographic Will Validity (§251.052)
- Self-Proving Affidavit Effect (§251.104)
- Witness Presence Tests
- Codicil Execution
- Nuncupative Wills
- Mutual and Joint Wills
- Incorporation by Reference
- Acts of Independent Significance
- Pour-Over Will Provisions

### Testamentary Capacity & Validity (8)
- Testamentary Capacity Standard (Rothermel 4-element test)
- Lucid Interval Doctrine
- Undue Influence (circumstantial evidence factors)
- Confidential Relationship Presumption
- Fraud in Procurement
- Mistake and Reformation (§255.451)
- Duress and Coercion
- Testamentary Intent

### Devise Classification & Construction (12)
- Specific Devise Identification
- General Devise Rules
- Demonstrative Devise Construction
- Residuary Clause Effect
- Ademption by Extinction (§255.151)
- Ademption by Satisfaction
- Abatement Order (§355.109)
- Anti-Lapse Statute (§255.153)
- Class Gift Doctrine
- Per Stirpes vs. Per Capita Distribution
- Pretermitted Children (§255.052)
- Lapse and Void Devises

### Will Revocation & Modification (6)
- Revocation by Subsequent Writing (§253.002)
- Revocation by Physical Act
- Express vs. Implied Revocation
- Partial Revocation
- Revival of Revoked Will (§253.004)
- Dependent Relative Revocation

### Special Provisions (8)
- Powers of Appointment (General vs. Special)
- Life Estates and Remainders
- Conditions Precedent and Subsequent
- Testamentary Trusts
- No-Contest (In Terrorem) Clauses (§254.005)
- Simultaneous Death Provisions
- Disclaimer Provisions (§240.051)
- Tax Apportionment Clauses

### Will Contests & Probate (8)
- Will Contest Grounds (§256.201)
- Burden of Proof Allocation
- Contestant Standing Requirements
- Probate Procedures (Muniment of Title, Independent Administration)
- Self-Proving Affidavit Effect at Probate
- Handwriting Verification (§256.153)
- Extrinsic Evidence Rules
- Ambiguity (Patent vs. Latent)

---

## API Endpoints

### `POST /parse`
Parse will provision or answer construction question.

**Request:**
```json
{
  "query": "Is a holographic will valid without witnesses?",
  "mode": "defense",
  "position_zone": "planning",
  "provision_type": "specific_devise",
  "context": {}
}
```

**Response:**
```json
{
  "query": "...",
  "normalized_query": "...",
  "response_layer": "doctrine_cache",
  "mode": "defense",
  "position_zone": "planning",
  "conclusion": "Under Texas Estates Code §251.052...",
  "reasoning": "DOCTRINE ANALYSIS: ...",
  "authorities": ["Texas Estates Code §251.052", "Estate of Gonzales..."],
  "confidence_level": "DEFENSIBLE",
  "doctrine_topics": ["Holographic Will Validity"],
  "statute_references": ["§251.052"],
  "risk_factors": [...],
  "recommendations": [...],
  "latency_ms": 42.5,
  "determinism_hash": "a3f9c2d1e8b4...",
  "trace_id": "uuid"
}
```

### `GET /health`
Comprehensive health check with metrics.

### `GET /doctrines`
List all 52 doctrine topics.

### `GET /doctrine/{topic}`
Retrieve specific doctrine block details.

### `GET /metrics`
Performance metrics (cache hit rate, latency, error rate).

### `GET /coverage`
Doctrine coverage map.

---

## Installation

1. **Dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic loguru
   ```

2. **Launch Engine:**
   ```bash
   python engine.py
   ```

3. **Verify Health:**
   ```bash
   curl http://localhost:8652/health
   ```

---

## Example Queries

### Holographic Will Validity
```bash
curl -X POST http://localhost:8652/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "Does a handwritten will need witnesses in Texas?", "mode": "fast"}'
```

### Anti-Lapse Application
```bash
curl -X POST http://localhost:8652/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "My daughter predeceased me. Does her son get her share under my will?", "mode": "defense"}'
```

### Undue Influence Analysis
```bash
curl -X POST http://localhost:8652/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "Caregiver was present when testator signed will. Is this undue influence?", "mode": "memo", "position_zone": "audit"}'
```

### Specific Devise Ademption
```bash
curl -X POST http://localhost:8652/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "Will says give my Ford F-150 to John but I sold it before I died", "mode": "defense"}'
```

---

## File Structure

```
P02_will_parser/
├── engine.py          (863 lines) - Main FastAPI server, TIE-20 components
├── doctrines.py       (742 lines) - 52 pre-compiled doctrine blocks
├── semantic.py        (283 lines) - Deterministic term normalization
├── search.py          (211 lines) - Cloud vector search integration
├── telemetry.py       (375 lines) - Query tracing, audit trail, metrics
├── config.json        (74 lines)  - Engine configuration
├── README.md          - This file
└── logs/
    ├── will_parser_{timestamp}.log
    ├── audit_trail.jsonl
    ├── doctrine_mutations.jsonl
    └── performance_metrics.jsonl
```

**Total:** 2,548 lines (excluding README)

---

## Epistemic Guardrails

### Banned Phrases
- "definitely," "guaranteed," "certainly valid," "no risk"
- "will win in court," "court will rule"
- "testator intended," "clearly meant"

### Disclosure Required For
- Will contest, undue influence, testamentary capacity
- Fraud, mistake, duress
- Ambiguity, conflicting provisions
- Missing witnesses, self-proving affidavit defects

---

## Authority Hierarchy

1. **STATUTE** (weight: 10) - Texas Estates Code §251-256
2. **CASE_LAW** (weight: 7) - Texas Supreme Court and Courts of Appeals
3. **RESTATEMENT** (weight: 6) - Restatement (Third) of Property: Wills
4. **TREATISE** (weight: 4) - Practice guides and legal commentary

---

## Performance Targets

- **Layer 1 (Cache Hit):** <200ms
- **Layer 2 (Vector Search):** <700ms
- **Layer 3 (Deep Analysis):** <2000ms
- **Cache Hit Rate:** >70% after warmup
- **Error Rate:** <2%

---

## Integration

### Cloud Retriever
Uses `_shared/cloud_retriever.py` for vector search fallback. Requires:
- R2 bucket: `echo-prime-knowledge`
- Vector index: `will-construction-vectors`
- Domain filter: `will_construction`

### Cognition Cloud
Integrates with ECHO OMEGA PRIME knowledge vectorization infrastructure for semantic retrieval on cache miss.

---

## Compliance

- **Audit Trail:** Append-only JSONL log for forensic review
- **Determinism:** SHA-256 hashing for reproducibility
- **Telemetry:** Full query tracing with latency and error domain classification
- **Doctrine Mutations:** Logged with authority citations and approver identification

---

## Author

**ECHO OMEGA PRIME**
Authority: 11.0 SOVEREIGN
Commander: Bobby Don McWilliams II
Created: 2026-02-12

---

## License

Proprietary - ECHO OMEGA PRIME Internal Use Only
