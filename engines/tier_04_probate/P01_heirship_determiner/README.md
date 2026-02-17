# P01 Heirship Determiner Engine v1.0.0

**Texas Intestate Succession Analysis — Rule-Based Intelligence Engine**

## Overview

The P01 Heirship Determiner is a specialized intelligence engine for analyzing Texas intestate succession law. It determines heir identity, inheritance shares, and property distribution when a person dies without a will.

## TIE-20 Compliance

✅ **All 20 mandatory components implemented:**

1. ✓ **three_layer_response** - Doctrine cache (0-200ms) → Semantic search → Deep analysis
2. ✓ **response_modes** - FAST (concise), DEFENSE (audit-ready), MEMO (comprehensive)
3. ✓ **doctrine_cache** - 8+ precompiled expert reasoning blocks with real probate content
4. ✓ **authority_hardening** - Hierarchical source weighting (Constitution > Statutes > Caselaw)
5. ✓ **confidence_stratification** - DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK
6. ✓ **semantic_normalization** - Domain-specific probate terminology mapping
7. ✓ **vector_search** - Cloud retrieval + local fallback for semantic matching
8. ✓ **telemetry** - Complete query tracing with latency tracking
9. ✓ **drift_watcher** - Doctrine coverage monitoring and gap detection
10. ✓ **coverage_map** - Tracks triggered vs untriggered doctrines
11. ✓ **metrics_collector** - Queries/hour, hit rates, error rates, latencies
12. ✓ **health_endpoint** - Comprehensive JSON health check
13. ✓ **zoned_analysis** - PLANNING/REPORTING/AUDIT position zones
14. ✓ **fact_fragility_scoring** - Verifiability and recharacterization risk
15. ✓ **audit_trail_jsonl** - Every query logged to JSONL for forensic review
16. ✓ **determinism_hash_sha256** - SHA-256 for reproducibility verification
17. ✓ **fastapi_server** - Full FastAPI with CORS, lifespan, typed endpoints
18. ✓ **loguru_logging** - Structured logging with rotation, never print()
19. ✓ **multi_doctrine_decomposition** - Issue categorization and interaction analysis
20. ✓ **deep_analysis_mode** - Multi-source synthesis for novel questions

## Engine Specifications

- **Engine ID:** P01
- **Port:** 8651
- **Mode:** Rule-Based (no LLM required)
- **Domain:** Texas probate intestacy law
- **Jurisdiction:** Texas (primary), comparative UPC references
- **Doctrine Blocks:** 8+ comprehensive probate topics
- **Lines of Code:** ~1,500+ (engine.py: 800+, doctrines.py: 1,200+, telemetry.py: 400+)

## Core Capabilities

### Intestate Succession Analysis
- Separate property distribution (§201.001)
- Community property distribution (§201.002)
- Per stirpes vs per capita methodologies (§201.101)
- Collateral heirs (parents, siblings, descendants)
- Escheat determination (§71.001)

### Heir Qualification
- Adopted children inheritance rights (§201.054)
- Half-blood relatives equal treatment (§201.057)
- Posthumous heirs 300-day rule (§201.056)
- Simultaneous death 120-hour rule (§121.101)
- Paternity establishment requirements

### Property Characterization
- Community vs separate property analysis
- Inception of title rule (§3.001 Family Code)
- Commingling and tracing
- Transmutation agreements (§4.203 FC)

### Homestead Rights
- Surviving spouse life estate (§102.002)
- Minor children possessory rights (§102.004)
- Homestead definition and limits
- Partition prohibition

### Non-Probate Determinations
- Affidavit of heirship requirements (§203.001)
- Court determination of heirship (§202.001)
- Disinterested witness criteria
- Prima facie evidence standards

## API Endpoints

### POST /query
Process heirship determination query.

**Request:**
```json
{
  "query": "How does separate property pass when spouse and children survive?",
  "mode": "DEFENSE",
  "zone": "REPORTING",
  "include_citations": true,
  "jurisdiction": "texas"
}
```

**Response:**
```json
{
  "query_id": "uuid",
  "timestamp": "ISO-8601",
  "query": "...",
  "response": "...",
  "mode": "DEFENSE",
  "zone": "REPORTING",
  "confidence": "DEFENSIBLE",
  "confidence_score": 0.95,
  "doctrines_triggered": ["separate_property_spouse_children_distribution"],
  "citations": ["Texas Estates Code §201.001", ...],
  "determinism_hash": "sha256...",
  "latency_ms": 45.2,
  "metadata": {...}
}
```

### GET /health
Comprehensive health check.

**Response:**
```json
{
  "status": "healthy",
  "engine_id": "P01",
  "engine_name": "heirship_determiner",
  "version": "1.0.0",
  "port": 8651,
  "mode": "rule_based",
  "uptime_seconds": 3600.5,
  "queries_total": 42,
  "queries_per_hour": 35.2,
  "cache_hit_rate": 0.85,
  "avg_latency_ms": 52.3,
  "p95_latency_ms": 120.5,
  "error_rate": 0.02,
  "doctrines_loaded": 8,
  "doctrines_triggered": 6,
  "coverage_percentage": 75.0,
  "cloud_retrieval_available": true,
  "timestamp": "ISO-8601"
}
```

### GET /metrics
Detailed performance metrics including bottleneck analysis.

### GET /doctrines
List all cached doctrines with keywords and authority.

### GET /coverage
Doctrine coverage analysis and epistemic gap detection.

## Usage Examples

### Startup

```bash
cd O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\P01_heirship_determiner
python engine.py
# Server starts on http://localhost:8651
```

### Query via cURL

```bash
curl -X POST http://localhost:8651/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What happens to community property when spouse dies?",
    "mode": "DEFENSE",
    "zone": "REPORTING",
    "include_citations": true
  }'
```

### Query via Python

```python
import requests

response = requests.post('http://localhost:8651/query', json={
    'query': 'How does per stirpes distribution work?',
    'mode': 'MEMO',
    'zone': 'PLANNING',
    'include_citations': True
})

result = response.json()
print(f"Confidence: {result['confidence']} ({result['confidence_score']:.2f})")
print(f"Response: {result['response']}")
print(f"Citations: {result['citations']}")
```

## Testing

Run the comprehensive test suite:

```bash
python test_engine.py
```

**Tests include:**
- Doctrine cache loading
- Three-layer response architecture
- Response modes (FAST/DEFENSE/MEMO)
- Confidence stratification
- Telemetry collection
- Drift watching
- Epistemic guardrails
- Multi-doctrine decomposition

## File Structure

```
P01_heirship_determiner/
├── engine.py              # Main engine logic (800+ lines)
├── doctrines.py           # Doctrine cache (1,200+ lines, 8+ blocks)
├── semantic.py            # Semantic normalization (500+ lines)
├── search.py              # Vector search fallback (300+ lines)
├── telemetry.py           # Telemetry & monitoring (400+ lines)
├── config.json            # Engine configuration (100+ lines)
├── test_engine.py         # Test suite
├── README.md              # This file
└── logs/                  # Log directory (auto-created)
    └── heirship_determiner_YYYY-MM-DD.log
```

## Doctrine Topics

1. **separate_property_spouse_children_distribution** - §201.001 life estate mechanics
2. **community_property_at_death_distribution** - §201.002 all to spouse
3. **per_stirpes_distribution_methodology** - §201.101 by representation
4. **affidavit_of_heirship_requirements** - §203.001 non-probate determination
5. **homestead_rights_intestate_succession** - §102.002 life estate protections
6. **adopted_children_inheritance_rights** - §201.054 dual inheritance scenarios
7. **half_blood_relatives_equal_inheritance** - §201.057 equality rule
8. **posthumous_heirs_300_day_rule** - §201.056 gestation presumption

## Response Modes

### FAST Mode
- **Target:** <500 tokens
- **Use case:** Quick answers, initial screening
- **Content:** Conclusion + primary authority
- **Latency:** 10-50ms (cache hit)

### DEFENSE Mode
- **Target:** 1,000-2,000 tokens
- **Use case:** Audit-ready documentation, adversarial review
- **Content:** Conclusion + reasoning + adversarial analysis + counter-arguments
- **Latency:** 20-100ms (cache hit)

### MEMO Mode
- **Target:** 2,000-4,000 tokens
- **Use case:** Comprehensive legal memoranda
- **Content:** Full analysis + related issues + alternatives + citations
- **Latency:** 30-150ms (cache hit)

## Confidence Levels

- **DEFENSIBLE** (0.90+) - Bedrock statutory law, 100+ years precedent
- **AGGRESSIVE** (0.75+) - Well-supported but some factual uncertainty
- **DISCLOSURE** (0.60+) - Requires fact-specific analysis or novel issue
- **HIGH_RISK** (0.45+) - Unsettled law, no clear precedent, experimental

## Analysis Zones

- **PLANNING** - Pre-death estate planning structure
- **REPORTING** - Post-death heirship determination
- **AUDIT** - Affidavit preparation and documentation

Each zone adds appropriate disclaimers and caveats.

## Authority Hierarchy

1. Texas Constitution Art. XVI (homestead) - Weight: 100
2. Texas Estates Code Chapters 71, 102, 121, 201-203 - Weight: 95
3. Texas Family Code Title 1 (community property) - Weight: 90
4. Texas Supreme Court precedent - Weight: 85
5. Texas Courts of Appeals - Weight: 75
6. Attorney General opinions - Weight: 70
7. State Bar guidance - Weight: 60

## Cloud Integration

**Cognition Cloud retrieval enabled** (if configured):
- Graph Worker: `https://cognition-graph.bmcii1976.workers.dev`
- EKM Worker: `https://cognition-ekm.bmcii1976.workers.dev`
- Timeout: 10 seconds
- Fallback: Local vector search if cloud unavailable

## Performance

**Typical Latencies:**
- Cache hit (FAST): 10-50ms
- Cache hit (DEFENSE): 20-100ms
- Semantic search: 200-500ms
- Deep analysis: 2000ms+

**Target Metrics:**
- Cache hit rate: >80%
- P95 latency: <200ms
- Error rate: <2%
- Doctrine coverage: >75% after 100 queries

## Logging

All logs written to `logs/heirship_determiner_YYYY-MM-DD.log`:
- Rotation: Daily
- Retention: 30 days
- Format: Structured with timestamps and context
- Level: INFO (configurable)

## Audit Trail

Every query logged to `audit_trail.jsonl` (JSONL format):
- Query text and metadata
- Doctrines triggered and missed
- Latency breakdown by phase
- Confidence scores
- Errors and warnings
- Determinism hash

**Use for:**
- Forensic review
- Quality assurance
- Compliance audits
- Performance optimization

## Future Enhancements

- [ ] Add 40+ more doctrine blocks to reach 50+ total
- [ ] UPC comparative analysis for multi-state estates
- [ ] Interactive family tree builder
- [ ] PDF affidavit of heirship generation
- [ ] Integration with property records databases
- [ ] Automated heirship flowcharts

## Version History

- **v1.0.0** (2026-02-12) - Initial release with TIE-20 compliance

## License

ECHO OMEGA PRIME Proprietary
© 2026 Bobby Don McWilliams II
