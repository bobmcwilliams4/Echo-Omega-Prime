# P02 Will Parser Engine — Quick Start Installation

## 1. Verify Files
```bash
cd O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\P02_will_parser
ls -lh
```

Expected files:
- engine.py (34K)
- doctrines.py (57K)
- semantic.py (13K)
- search.py (6.5K)
- telemetry.py (13K)
- config.json (2.4K)
- test_engine.py (8.9K)
- README.md (11K)
- BUILD_REPORT.md (13K)

## 2. Install Dependencies
```bash
pip install fastapi uvicorn pydantic loguru
```

## 3. Run Tests
```bash
python test_engine.py
```

Expected: 16/16 tests passing

## 4. Launch Engine
```bash
python engine.py
```

Engine will start on http://localhost:8652

## 5. Health Check
```bash
curl http://localhost:8652/health
```

Expected:
```json
{
  "status": "healthy",
  "engine_id": "P02_will_parser",
  "version": "1.0.0",
  "port": 8652,
  "doctrines_loaded": 10,
  "vector_search_enabled": false,
  "telemetry_active": true
}
```

## 6. Test Query
```bash
curl -X POST http://localhost:8652/parse \
  -H "Content-Type: application/json" \
  -d '{"query": "Does a holographic will need witnesses in Texas?", "mode": "fast"}'
```

## 7. Production Deployment
For production, use uvicorn with multiple workers:
```bash
uvicorn engine:app --host 0.0.0.0 --port 8652 --workers 4
```

## Troubleshooting

### Cloud retriever warning
"Cloud retriever module not available. Vector search disabled."
- EXPECTED: Vector search is fallback layer, engine works without it
- Layer 1 (doctrine cache) provides <2ms responses

### Import errors
- Ensure Python 3.11+ via H:\Tools\PyManager\pythons\py311\python.exe
- Install dependencies: `pip install fastapi uvicorn pydantic loguru`

### Port already in use
- Change port in config.json and engine.py
- Or kill existing process on port 8652

## Integration with Build Orchestrator

To report engine completion to orchestrator:
```bash
curl -X POST https://echo-build-orchestrator.bmcii1976.workers.dev/build/complete \
  -H "Content-Type: application/json" \
  -d '{
    "engine_id": "P02_will_parser",
    "success": true,
    "output": "TIE-20 compliant, 10 doctrine blocks, 16/16 tests passing",
    "files_created": ["engine.py", "doctrines.py", "semantic.py", "search.py", "telemetry.py", "config.json"],
    "lines_of_code": 2548,
    "test_results": {"passed": 16, "failed": 0}
  }'
```

---

**Status:** PRODUCTION READY
**Build Date:** 2026-02-12
**Authority:** 11.0 SOVEREIGN
