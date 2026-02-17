"""Incremental test: add engine components one by one to find the blocker."""
import sys
import time
import threading
import httpx
from pathlib import Path
from contextlib import asynccontextmanager

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PORT = 8519

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass

def test(label, app, wait=4, stop_wait=4):
    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UServer(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(wait)
    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        r = f"PASS ({resp.status_code})"
    except Exception as e:
        r = "FAIL"
    server.should_exit = True
    thread.join(timeout=8)
    time.sleep(stop_wait)
    print(f"  {label}: {r}", flush=True)
    return "PASS" in r


# Step 1: Import engine
print("Importing engine...", flush=True)
import engine
print(f"Engine imported ({len(engine.app.routes)} routes)", flush=True)

# Test 1: engine.lifespan + dict health (Test 5 scenario)
print("\nTest 1: engine.lifespan + fresh dict health", flush=True)
a1 = FastAPI(lifespan=engine.lifespan)
a1.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@a1.get("/health")
async def h1():
    return {"status": "ok"}
test("lifespan + dict", a1)

# Test 2: engine.lifespan + health that reads globals
print("\nTest 2: engine.lifespan + health reading globals", flush=True)
a2 = FastAPI(lifespan=engine.lifespan)
a2.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@a2.get("/health")
async def h2():
    return {
        "status": "ok",
        "doctrines": len(engine.doctrine_cache) if engine.doctrine_cache else 0,
        "has_engine": engine.response_engine is not None,
    }
test("lifespan + globals", a2)

# Test 3: engine.lifespan + health returning HealthResponse
print("\nTest 3: engine.lifespan + health returning HealthResponse model", flush=True)
a3 = FastAPI(lifespan=engine.lifespan)
a3.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@a3.get("/health")
async def h3():
    return engine.HealthResponse(
        engine_id="LM09",
        engine_name="Test",
        version="1.0.0",
        status="ok",
        uptime_seconds=0,
        doctrine_count=len(engine.doctrine_cache) if engine.doctrine_cache else 0,
        vector_index_size=0,
        total_queries=0,
        error_rate=0.0,
        cache_hit_rate=0.0,
        timestamp="now",
    )
test("lifespan + HealthResponse", a3)

# Test 4: engine.lifespan + await engine.health_check()
print("\nTest 4: engine.lifespan + await engine.health_check()", flush=True)
a4 = FastAPI(lifespan=engine.lifespan)
a4.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@a4.get("/health")
async def h4():
    return await engine.health_check()
test("lifespan + engine.health_check", a4)

# Test 5: engine.lifespan + engine.QueryRequest in signature
print("\nTest 5: engine.lifespan + QueryRequest param", flush=True)
a5 = FastAPI(lifespan=engine.lifespan)
a5.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@a5.get("/health")
async def h5():
    return {"status": "ok"}
@a5.post("/query")
async def q5(request: engine.QueryRequest):
    return {"received": request.query}
test("lifespan + QueryRequest param", a5)

print("\nDONE", flush=True)
