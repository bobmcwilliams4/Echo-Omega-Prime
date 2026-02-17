"""Isolation test 9: Factory function with proxies.

Test 5 created apps inside run_test() and they PASSED.
Test 8 created app at module level and FAILED.
Does creating inside a function fix the issue?
"""
import sys
import time
import threading
import httpx
from pathlib import Path
from contextlib import asynccontextmanager

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import engine
print(f"Engine imported.", flush=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from doctrines import build_doctrine_cache, get_all_doctrine_topics
from semantic import SemanticNormalizer
from search import RunsheetVectorSearch
from telemetry import TelemetryManager

ENGINE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = ENGINE_DIR / "vectors"
LOG_DIR = ENGINE_DIR / "logs"

PORT = 8519

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass


def create_and_test():
    """Create app INSIDE a function — does this fix it?"""

    @asynccontextmanager
    async def lifespan(app):
        engine.doctrine_cache = build_doctrine_cache()
        engine.normalizer = SemanticNormalizer()
        engine.vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "lm09_runsheet.db")
        engine.seed_vector_index(engine.vector_search, engine.doctrine_cache)
        all_topics = get_all_doctrine_topics()
        engine.telemetry_mgr = TelemetryManager(
            engine_id="LM09", doctrine_topics=all_topics,
            audit_log_path=LOG_DIR / "lm09_audit.jsonl",
        )
        engine.chain_builder = engine.ChainOfTitleBuilder(engine.normalizer)
        engine.interest_calc = engine.InterestCalculator()
        engine.formatter = engine.RunSheetFormatter()
        engine.fragility_scorer = engine.FactFragilityScorer()
        engine.decomposer = engine.MultiDoctrineDecomposer(engine.doctrine_cache)
        engine.response_engine = engine.ThreeLayerResponseEngine(
            doctrine_cache=engine.doctrine_cache, vector_search=engine.vector_search,
            normalizer=engine.normalizer, telemetry=engine.telemetry_mgr,
            chain_builder=engine.chain_builder, interest_calculator=engine.interest_calc,
            formatter=engine.formatter, fragility_scorer=engine.fragility_scorer,
            decomposer=engine.decomposer,
        )
        logger.info("Lifespan complete — {} doctrines", len(engine.doctrine_cache))
        yield

    app = FastAPI(title="LM09 Factory", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    # Test A: Proxy that calls engine handler
    @app.get("/health")
    async def health_proxy():
        return await engine.health_check()

    @app.post("/query")
    async def query_proxy(request: engine.QueryRequest):
        return await engine.process_query(request)

    print(f"  Factory app: {len(app.routes)} routes", flush=True)

    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UServer(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(5)

    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        print(f"  HEALTH proxy: PASS ({resp.status_code}) {resp.text[:200]}", flush=True)
    except Exception as e:
        print(f"  HEALTH proxy: FAIL ({e})", flush=True)

    server.should_exit = True
    thread.join(timeout=5)
    time.sleep(3)


def create_and_test_simple():
    """Factory with simple dict returns (like test 5 Test D)."""

    @asynccontextmanager
    async def lifespan(app):
        engine.doctrine_cache = build_doctrine_cache()
        engine.normalizer = SemanticNormalizer()
        engine.vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "lm09_runsheet.db")
        engine.seed_vector_index(engine.vector_search, engine.doctrine_cache)
        all_topics = get_all_doctrine_topics()
        engine.telemetry_mgr = TelemetryManager(
            engine_id="LM09", doctrine_topics=all_topics,
            audit_log_path=LOG_DIR / "lm09_audit.jsonl",
        )
        engine.chain_builder = engine.ChainOfTitleBuilder(engine.normalizer)
        engine.interest_calc = engine.InterestCalculator()
        engine.formatter = engine.RunSheetFormatter()
        engine.fragility_scorer = engine.FactFragilityScorer()
        engine.decomposer = engine.MultiDoctrineDecomposer(engine.doctrine_cache)
        engine.response_engine = engine.ThreeLayerResponseEngine(
            doctrine_cache=engine.doctrine_cache, vector_search=engine.vector_search,
            normalizer=engine.normalizer, telemetry=engine.telemetry_mgr,
            chain_builder=engine.chain_builder, interest_calculator=engine.interest_calc,
            formatter=engine.formatter, fragility_scorer=engine.fragility_scorer,
            decomposer=engine.decomposer,
        )
        yield

    app = FastAPI(title="LM09 Simple", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    async def health():
        return {"status": "ok", "doctrines": len(engine.doctrine_cache)}

    @app.post("/query")
    async def query(request: engine.QueryRequest):
        if not engine.response_engine:
            return {"error": "not initialized"}
        result = engine.response_engine.process_query(request)
        # Return as dict instead of Pydantic model
        return result.model_dump() if hasattr(result, 'model_dump') else dict(result)

    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UServer(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(5)

    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        print(f"  HEALTH simple: PASS ({resp.status_code}) {resp.text[:200]}", flush=True)
    except Exception as e:
        print(f"  HEALTH simple: FAIL ({e})", flush=True)

    try:
        resp = httpx.post(
            f"http://127.0.0.1:{PORT}/query",
            json={"query": "What is a run sheet?", "mode": "FAST"},
            timeout=15.0,
        )
        print(f"  QUERY simple: PASS ({resp.status_code}) {resp.text[:300]}", flush=True)
    except Exception as e:
        print(f"  QUERY simple: FAIL ({e})", flush=True)

    server.should_exit = True
    thread.join(timeout=5)


print("\n=== Test A: Factory + proxy (calls engine handler) ===", flush=True)
create_and_test()

print("\n=== Test B: Factory + simple dict returns ===", flush=True)
create_and_test_simple()

print("\nDONE", flush=True)
