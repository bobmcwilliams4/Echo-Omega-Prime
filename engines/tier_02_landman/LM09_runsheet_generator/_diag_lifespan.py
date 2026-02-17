"""Diagnostic: timed lifespan to find the blocking step in LM09."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

ENGINE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = ENGINE_DIR / "vectors"
LOG_DIR = ENGINE_DIR / "logs"
VECTOR_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

print(f"[{time.time():.1f}] Starting imports...", flush=True)

t0 = time.time()
from doctrines import build_doctrine_cache, get_all_doctrine_topics, get_doctrine_interaction_graph, get_doctrines_by_category
print(f"[{time.time()-t0:.2f}s] doctrines imported", flush=True)

from semantic import SemanticNormalizer, InstrumentType
print(f"[{time.time()-t0:.2f}s] semantic imported", flush=True)

from search import RunsheetVectorSearch, SearchDocument
print(f"[{time.time()-t0:.2f}s] search imported", flush=True)

from telemetry import CoverageMap, DriftWatcher, ErrorDomain, MetricsCollector, QueryPhase, QueryTrace, TelemetryManager
print(f"[{time.time()-t0:.2f}s] telemetry imported", flush=True)

# Now import engine module components one by one
print(f"[{time.time()-t0:.2f}s] Importing engine module...", flush=True)
import engine as eng
print(f"[{time.time()-t0:.2f}s] engine module imported, {len(eng.app.routes)} routes", flush=True)

# Create our own lifespan that mirrors engine.py but with timing
@asynccontextmanager
async def timed_lifespan(app: FastAPI):
    t = time.time()

    print(f"[{time.time()-t0:.2f}s] Lifespan: building doctrine cache...", flush=True)
    doctrine_cache = build_doctrine_cache()
    print(f"[{time.time()-t0:.2f}s] Lifespan: {len(doctrine_cache)} doctrines built ({time.time()-t:.2f}s)", flush=True)

    t2 = time.time()
    normalizer = SemanticNormalizer()
    print(f"[{time.time()-t0:.2f}s] Lifespan: normalizer created ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "diag_test.db")
    print(f"[{time.time()-t0:.2f}s] Lifespan: vector_search created ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    eng.seed_vector_index(vector_search, doctrine_cache)
    print(f"[{time.time()-t0:.2f}s] Lifespan: vector index seeded ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    all_topics = get_all_doctrine_topics()
    telemetry_mgr = TelemetryManager(engine_id="LM09", doctrine_topics=all_topics, audit_log_path=LOG_DIR / "diag_audit.jsonl")
    print(f"[{time.time()-t0:.2f}s] Lifespan: telemetry created ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    chain_builder = eng.ChainOfTitleBuilder(normalizer)
    print(f"[{time.time()-t0:.2f}s] Lifespan: chain_builder ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    interest_calc = eng.InterestCalculator()
    print(f"[{time.time()-t0:.2f}s] Lifespan: interest_calc ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    formatter = eng.RunSheetFormatter()
    print(f"[{time.time()-t0:.2f}s] Lifespan: formatter ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    fragility_scorer = eng.FactFragilityScorer()
    print(f"[{time.time()-t0:.2f}s] Lifespan: fragility_scorer ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    decomposer = eng.MultiDoctrineDecomposer(doctrine_cache)
    print(f"[{time.time()-t0:.2f}s] Lifespan: decomposer ({time.time()-t2:.2f}s)", flush=True)

    t2 = time.time()
    response_engine = eng.ThreeLayerResponseEngine(
        doctrine_cache=doctrine_cache,
        vector_search=vector_search,
        normalizer=normalizer,
        telemetry=telemetry_mgr,
        chain_builder=chain_builder,
        interest_calculator=interest_calc,
        formatter=formatter,
        fragility_scorer=fragility_scorer,
        decomposer=decomposer,
    )
    print(f"[{time.time()-t0:.2f}s] Lifespan: response_engine ({time.time()-t2:.2f}s)", flush=True)

    # Assign to engine module globals
    eng.doctrine_cache = doctrine_cache
    eng.normalizer = normalizer
    eng.vector_search = vector_search
    eng.telemetry_mgr = telemetry_mgr
    eng.chain_builder = chain_builder
    eng.interest_calc = interest_calc
    eng.formatter = formatter
    eng.fragility_scorer = fragility_scorer
    eng.decomposer = decomposer
    eng.response_engine = response_engine

    print(f"[{time.time()-t0:.2f}s] Lifespan: YIELDING — server should be ready", flush=True)
    yield
    print(f"[{time.time()-t0:.2f}s] Lifespan: shutting down", flush=True)

# Replace the engine's lifespan
new_app = FastAPI(title="LM09 Diag", lifespan=timed_lifespan)
new_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Copy all routes from the original app
for route in eng.app.routes:
    new_app.routes.append(route)

print(f"[{time.time()-t0:.2f}s] New app created with {len(new_app.routes)} routes", flush=True)

if __name__ == "__main__":
    print(f"[{time.time()-t0:.2f}s] Starting uvicorn...", flush=True)
    uvicorn.run(new_app, host="0.0.0.0", port=8509, log_level="info")
