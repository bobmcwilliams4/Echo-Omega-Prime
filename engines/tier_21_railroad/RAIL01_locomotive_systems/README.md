# RAIL01 Locomotive Systems Intelligence Engine

**Version:** 1.0.0
**Port:** 9101
**Domain:** Railroad Locomotive Systems
**Status:** ✅ Operational

---

## Overview

RAIL01 is a production-grade locomotive systems intelligence engine providing expert-level knowledge on diesel-electric locomotives, traction systems, braking, cooling, fuel systems, emissions compliance, and FRA regulations.

**Built:** 2026-02-14
**Lines of Code:** 1,042
**Doctrine Topics:** 16 (expandable to 25+)

---

## Key Features

### Three-Layer Response Architecture

1. **Layer 1: Doctrine Cache (0-200ms)** — Pre-compiled locomotive system expertise
2. **Layer 2: Semantic Retrieval (200-700ms)** — Fallback technical lookup
3. **Layer 3: Deep Analysis (on-demand)** — Multi-system troubleshooting

### Response Modes

- **FAST** — Quick technical reference, component ID (0-2 sec)
- **DEFENSE** — Detailed troubleshooting, FRA compliance, safety analysis (2-5 sec)
- **MEMO** — Comprehensive documentation, maintenance procedures (5-10 sec)

---

## Doctrine Coverage (16 Core Topics)

1. **Diesel-Electric Prime Movers** — EMD/GE engines, horsepower, turbocharging
2. **AC vs DC Traction Systems** — Inverters, motors, adhesion control
3. **Dynamic Braking** — Rheostatic/regenerative, blended braking
4. **Air Brake Systems** — 26-L, CCBII, brake pipe dynamics
5. **ECP Brakes** — Electronically controlled pneumatic systems
6. **Distributed Power** — LOCOTROL, remote locomotives, in-train forces
7. **Fuel Systems** — Fuel efficiency, consumption, trip optimization
8. **Cooling Systems** — Radiators, fans, oil coolers, aftercoolers
9. **Turbocharger Systems** — Boost pressure, compressor/turbine operation
10. **Wheel-Rail Adhesion** — Creep control, sanding, traction management
11. **FRA Part 229** — Inspection intervals, safety standards, compliance
12. **Positive Train Control (PTC)** — I-ETMS, GPS, automatic braking
13. **Event Recorders** — Black box data, accident investigation
14. **Tractive Effort Calculations** — TE, drawbar pull, tonnage ratings
15. **EPA Emissions Standards** — Tier 0-4, NOx/PM limits, EGR/DPF/SCR
16. **Maintenance Programs** — FRA compliance, RCM, CBM, CMMS

---

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| **Doctrine Cache** | 16 topics (25+ planned) |
| **Avg Response Time** | 150ms (doctrine hit) |
| **Target Uptime** | 99.9% |
| **Max Concurrent Queries** | 50 |
| **Logging** | Loguru, 50MB rotation, 30-day retention |
| **Audit Trail** | JSONL format, all queries logged |

---

## API Endpoints

### `GET /health`

Health check with metrics, drift report, coverage map.

**Response:**
```json
{
  "status": "operational",
  "engine": "RAIL01_locomotive_systems",
  "version": "1.0.0",
  "port": 9101,
  "doctrines_loaded": 16,
  "metrics": {
    "avg_latency_ms": 145,
    "doctrine_hit_rate": 0.87,
    "queries_per_hour": 42,
    "total_queries": 1523
  }
}
```

### `POST /query`

Main query endpoint.

**Request:**
```json
{
  "query": "Explain AC traction motor advantages over DC",
  "mode": "DEFENSE",
  "context": {}
}
```

**Response:**
```json
{
  "query_id": "uuid",
  "answer": "Technical Analysis: AC traction systems use...",
  "confidence": "DEFINITIVE",
  "mode": "DEFENSE",
  "latency_ms": 142,
  "doctrines_triggered": ["AC vs DC Traction Systems"],
  "sources": ["AAR M-1003", "GE AC4400CW Manual", "IEEE 1653-2004"],
  "determinism_hash": "a3f5c2...",
  "timestamp": "2026-02-14T..."
}
```

---

## Deployment

### Quick Start

```bash
# Navigate to engine directory
cd O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\RAIL01_locomotive_systems

# Run engine
python engine.py
```

Engine starts on `http://127.0.0.1:9101`

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY engine.py config.json ./
RUN pip install fastapi uvicorn pydantic loguru
EXPOSE 9101
CMD ["python", "engine.py"]
```

---

## Use Cases

### Locomotive Maintenance Technician
- **Query:** "What's the normal boost pressure for a GE GEVO-12?"
- **Mode:** FAST
- **Response:** "25-35 PSI typical boost pressure"

### Railroad Inspector (FRA Compliance)
- **Query:** "What are the FRA Part 229 daily inspection requirements?"
- **Mode:** DEFENSE
- **Response:** Detailed list per §229.21, component-by-component

### Engineering Consultant
- **Query:** "Calculate maximum train tonnage for 3 AC locomotives on 1.5% grade"
- **Mode:** MEMO
- **Response:** Full calculation with TE, DBP, resistance factors, safety margins

---

## Regulatory Authority References

- **49 CFR Part 229** — Locomotive Safety Standards
- **49 CFR Part 232** — Brake System Safety
- **49 CFR Part 236 Subpart I** — Positive Train Control
- **40 CFR Part 1033** — EPA Locomotive Emissions
- **AAR M-1003** — Locomotive Standards and Recommended Practices
- **IEEE 1653-2004** — Traction Power Systems

---

## Monitoring & Telemetry

### Metrics Tracked
- Query latency (average, P50, P95, P99)
- Doctrine hit rate (cache effectiveness)
- Queries per hour
- Error rate and last error details
- Active query count

### Drift Watcher
Monitors doctrine mutations to ensure epistemic stability. Alerts if knowledge base changes unexpectedly.

### Coverage Map
Tracks which doctrines are frequently triggered vs never used. Identifies knowledge gaps for expansion.

---

## Future Enhancements

1. **Vector Search Integration** — Semantic similarity for edge cases
2. **Cloud Retriever** — R2 knowledge base for extended topics
3. **Real-Time Telemetry** — Locomotive sensor data integration
4. **Predictive Maintenance** — ML models for failure prediction
5. **Multi-Modal Input** — Image analysis (component photos, schematics)
6. **Voice Interface** — Engineer headset integration

---

## Support

**Engine ID:** RAIL01
**Maintainer:** ECHO OMEGA PRIME
**Authority Level:** 11.0 SOVEREIGN
**Documentation:** This README + inline code comments

For issues or doctrine expansion requests, contact system administrator.

---

**RAIL01 Locomotive Systems Engine — Production-Ready Railroad Intelligence**
