"""Isolation test 5: Cloned lifespan vs engine.lifespan.

Test A: engine.lifespan -> EXPECTED FAIL
Test B: Cloned lifespan (same code, defined here)
Test C: Empty lifespan (just yield)
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
print(f"Engine imported. {len(engine.app.routes)} routes", flush=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

PORT = 8509

from doctrines import build_doctrine_cache, get_all_doctrine_topics
from semantic import SemanticNormalizer
from search import RunsheetVectorSearch, SearchDocument
from telemetry import TelemetryManager

ENGINE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = ENGINE_DIR / "vectors"
LOG_DIR = ENGINE_DIR / "logs"

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass

def run_test(label, lifespan_fn, wait=5, stop_wait=3):
    app = FastAPI(title=label, lifespan=lifespan_fn)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    async def health():
        return {"status": "ok", "test": label}

    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UServer(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(wait)

    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        result = f"PASS ({resp.status_code})"
    except Exception as e:
        result = f"FAIL ({e})"

    server.should_exit = True
    thread.join(timeout=5)
    time.sleep(stop_wait)
    print(f"  {label}: {result}", flush=True)
    return "PASS" in result


# ─── Test A: engine.lifespan ───
print("\n=== Test A: engine.lifespan (expect FAIL) ===", flush=True)
pass_a = run_test("engine.lifespan", engine.lifespan)

# ─── Test B: Empty lifespan ───
print("\n=== Test B: Empty lifespan (just yield) ===", flush=True)
@asynccontextmanager
async def empty_lifespan(app: FastAPI):
    print("  Empty lifespan: yielding", flush=True)
    yield
    print("  Empty lifespan: shutting down", flush=True)

pass_b = run_test("empty_lifespan", empty_lifespan)

# ─── Test C: Cloned lifespan (same init, NO globals) ───
print("\n=== Test C: Cloned lifespan (local vars, no globals) ===", flush=True)
@asynccontextmanager
async def cloned_lifespan(app: FastAPI):
    print("  Cloned lifespan: starting", flush=True)
    dc = build_doctrine_cache()
    print(f"  Cloned: {len(dc)} doctrines", flush=True)
    norm = SemanticNormalizer()
    vs = RunsheetVectorSearch(index_path=VECTOR_DIR / "test5.db")
    engine.seed_vector_index(vs, dc)
    all_t = get_all_doctrine_topics()
    tm = TelemetryManager(engine_id="LM09", doctrine_topics=all_t, audit_log_path=LOG_DIR / "test5_audit.jsonl")
    cb = engine.ChainOfTitleBuilder(norm)
    ic = engine.InterestCalculator()
    fm = engine.RunSheetFormatter()
    fs = engine.FactFragilityScorer()
    dec = engine.MultiDoctrineDecomposer(dc)
    re = engine.ThreeLayerResponseEngine(
        doctrine_cache=dc, vector_search=vs, normalizer=norm, telemetry=tm,
        chain_builder=cb, interest_calculator=ic, formatter=fm,
        fragility_scorer=fs, decomposer=dec,
    )
    print("  Cloned lifespan: complete, yielding", flush=True)
    yield
    print("  Cloned lifespan: shutting down", flush=True)

pass_c = run_test("cloned_lifespan", cloned_lifespan, wait=5, stop_wait=3)

# ─── Test D: Cloned lifespan WITH global assignments ───
print("\n=== Test D: Cloned lifespan WITH global assignments ===", flush=True)
@asynccontextmanager
async def cloned_global_lifespan(app: FastAPI):
    print("  Cloned global lifespan: starting", flush=True)
    engine.doctrine_cache = build_doctrine_cache()
    print(f"  Cloned global: {len(engine.doctrine_cache)} doctrines", flush=True)
    engine.normalizer = SemanticNormalizer()
    engine.vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "test5g.db")
    engine.seed_vector_index(engine.vector_search, engine.doctrine_cache)
    all_t = get_all_doctrine_topics()
    engine.telemetry_mgr = TelemetryManager(engine_id="LM09", doctrine_topics=all_t, audit_log_path=LOG_DIR / "test5g_audit.jsonl")
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
    print("  Cloned global lifespan: complete, yielding", flush=True)
    yield
    print("  Cloned global lifespan: shutting down", flush=True)

pass_d = run_test("cloned_global_lifespan", cloned_global_lifespan, wait=5, stop_wait=3)

print(f"\n{'='*60}", flush=True)
print(f"Test A (engine.lifespan):           {'PASS' if pass_a else 'FAIL'}", flush=True)
print(f"Test B (empty lifespan):            {'PASS' if pass_b else 'FAIL'}", flush=True)
print(f"Test C (cloned, local vars):        {'PASS' if pass_c else 'FAIL'}", flush=True)
print(f"Test D (cloned, global assigns):    {'PASS' if pass_d else 'FAIL'}", flush=True)
