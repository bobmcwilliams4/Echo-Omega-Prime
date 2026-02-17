"""Isolation test 8: Proxy functions + cloned lifespan.

The ONLY working combination:
  Fresh endpoint functions + lifespan = PASS
  Engine endpoint functions + lifespan = FAIL
  Engine endpoint functions + no lifespan = PASS

Fix approach: proxy functions that call engine handlers.
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


@asynccontextmanager
async def fresh_lifespan(app):
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
    logger.info("LM09 fresh lifespan complete — {} doctrines", len(engine.doctrine_cache))
    yield
    logger.info("LM09 shutting down")


# Create app with fresh lifespan + PROXY routes
app = FastAPI(
    title=f"{engine.ENGINE_ID} {engine.ENGINE_NAME}",
    version=engine.ENGINE_VERSION,
    lifespan=fresh_lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# PROXY functions — fresh functions that delegate to engine handlers
@app.get("/health")
async def health():
    return await engine.health_check()

@app.post("/query")
async def query(request: engine.QueryRequest):
    return await engine.process_query(request)

@app.get("/")
async def root():
    return await engine.root()

@app.get("/doctrines")
async def doctrines():
    return await engine.list_doctrines()

print(f"App: {len(app.routes)} routes (4 proxy + auto)", flush=True)

# Launch and test
config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
server = UServer(config)
thread = threading.Thread(target=server.run, daemon=True)
thread.start()
time.sleep(5)

for path, method in [("/health", "GET"), ("/", "GET"), ("/doctrines", "GET")]:
    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}{path}", timeout=5.0)
        print(f"{method} {path}: PASS ({resp.status_code}) {resp.text[:150]}", flush=True)
    except Exception as e:
        print(f"{method} {path}: FAIL ({e})", flush=True)

try:
    resp = httpx.post(
        f"http://127.0.0.1:{PORT}/query",
        json={"query": "What is a run sheet?", "mode": "FAST"},
        timeout=15.0,
    )
    print(f"POST /query: PASS ({resp.status_code}) {resp.text[:300]}", flush=True)
except Exception as e:
    print(f"POST /query: FAIL ({e})", flush=True)

server.should_exit = True
thread.join(timeout=5)
print("DONE", flush=True)
