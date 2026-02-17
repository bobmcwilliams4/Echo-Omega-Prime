"""Standalone launcher for LM09 — works around module-level ASGI corruption."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import engine  # noqa: E402
from loguru import logger  # noqa: E402

import uvicorn  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from datetime import datetime, timezone  # noqa: E402

app = FastAPI(
    title=f"{engine.ENGINE_ID} {engine.ENGINE_NAME}",
    version=engine.ENGINE_VERSION,
    lifespan=engine.lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    metrics = engine.telemetry_mgr.metrics.get_comprehensive_metrics() if engine.telemetry_mgr else {}
    hit_rates = engine.telemetry_mgr.metrics.get_hit_rates() if engine.telemetry_mgr else {}
    error_rates = engine.telemetry_mgr.metrics.get_error_rates() if engine.telemetry_mgr else {}
    return engine.HealthResponse(
        engine_id=engine.ENGINE_ID,
        engine_name=engine.ENGINE_NAME,
        version=engine.ENGINE_VERSION,
        status="HEALTHY",
        uptime_seconds=engine.telemetry_mgr.metrics.get_uptime_seconds() if engine.telemetry_mgr else 0,
        doctrine_count=len(engine.doctrine_cache) if engine.doctrine_cache else 0,
        vector_index_size=engine.vector_search.get_index_stats()["total_documents"] if engine.vector_search else 0,
        total_queries=error_rates.get("total_queries", 0),
        error_rate=error_rates.get("error_rate", 0.0),
        cache_hit_rate=hit_rates.get("hit_rate", 0.0),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/query")
async def query(request: engine.QueryRequest):
    if not engine.response_engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    result = engine.response_engine.process_query(request)
    return result.model_dump() if hasattr(result, "model_dump") else result


@app.get("/")
async def root():
    return {
        "engine_id": engine.ENGINE_ID,
        "engine_name": engine.ENGINE_NAME,
        "version": engine.ENGINE_VERSION,
        "status": "running",
    }


@app.get("/doctrines")
async def doctrines():
    if not engine.doctrine_cache:
        return []
    return [
        {
            "topic": d.topic,
            "keywords": d.keywords,
            "confidence": d.confidence.value if hasattr(d.confidence, "value") else str(d.confidence),
        }
        for d in engine.doctrine_cache
    ]


@app.get("/search")
async def search(q: str, limit: int = 5):
    if not engine.vector_search:
        return {"results": [], "query": q}
    results = engine.vector_search.search(q, top_k=limit)
    return {"results": results, "query": q, "count": len(results)}


@app.get("/telemetry")
async def telemetry():
    if not engine.telemetry_mgr:
        return {"status": "not initialized"}
    return engine.telemetry_mgr.metrics.get_comprehensive_metrics()


if __name__ == "__main__":
    logger.info("Starting {} {} on port {} via launcher ({} routes)",
                engine.ENGINE_ID, engine.ENGINE_NAME, engine.ENGINE_PORT, len(app.routes))
    uvicorn.run(app, host="0.0.0.0", port=engine.ENGINE_PORT, reload=False, log_level="info")
