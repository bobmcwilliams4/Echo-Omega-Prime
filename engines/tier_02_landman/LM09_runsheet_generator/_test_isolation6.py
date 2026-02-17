"""Isolation test 6: Exact combination that breaks.

Known: engine endpoints + engine.lifespan in same app = FAIL
Known: engine endpoints alone = PASS, engine.lifespan alone = PASS

Test which combo triggers the failure.
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
from fastapi.routing import APIRoute

PORT = 8509

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass

def run_test(label, app, wait=4, stop_wait=3):
    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UServer(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(wait)
    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        result = f"PASS ({resp.status_code})"
    except Exception as e:
        result = f"FAIL"
    server.should_exit = True
    thread.join(timeout=5)
    time.sleep(stop_wait)
    print(f"  {label}: {result}", flush=True)
    return "PASS" in result


# ─── Test 1: 1 engine endpoint (/health only) + engine.lifespan ───
print("\n=== Test 1: 1 engine endpoint + engine.lifespan ===", flush=True)
a1 = FastAPI(title="T1", lifespan=engine.lifespan)
a1.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path == "/health":
        a1.add_api_route(r.path, r.endpoint, methods=list(r.methods), name=r.name)
        break
p1 = run_test("1 engine ep + lifespan", a1)

# ─── Test 2: 1 engine endpoint (/query only) + engine.lifespan ───
print("\n=== Test 2: 1 engine endpoint (/query) + engine.lifespan ===", flush=True)
a2 = FastAPI(title="T2", lifespan=engine.lifespan)
a2.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path == "/query":
        a2.add_api_route(r.path, r.endpoint, methods=list(r.methods), name=r.name)
        break
# Add a fresh health for testing
@a2.get("/health")
async def t2_health():
    return {"status": "ok"}
p2 = run_test("/query ep + lifespan", a2)

# ─── Test 3: engine.app directly (control — expect FAIL) ───
print("\n=== Test 3: engine.app directly ===", flush=True)
p3 = run_test("engine.app direct", engine.app, wait=5)

# ─── Test 4: ALL engine endpoints + NO lifespan + NO CORS ───
print("\n=== Test 4: All endpoints + NO lifespan + NO CORS ===", flush=True)
a4 = FastAPI(title="T4")
skip = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path not in skip:
        a4.add_api_route(r.path, r.endpoint, methods=list(r.methods) if r.methods else ["GET"], name=r.name)
p4 = run_test("all eps, no lifespan, no cors", a4)

# ─── Test 5: 5 engine endpoints + engine.lifespan ───
print("\n=== Test 5: 5 engine endpoints + engine.lifespan ===", flush=True)
a5 = FastAPI(title="T5", lifespan=engine.lifespan)
a5.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
target_paths = {"/health", "/query", "/doctrines", "/telemetry", "/"}
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path in target_paths:
        a5.add_api_route(r.path, r.endpoint, methods=list(r.methods), name=r.name)
p5 = run_test("5 eps + lifespan", a5)

print(f"\n{'='*60}", flush=True)
print(f"Test 1 (1 ep /health + lifespan):     {'PASS' if p1 else 'FAIL'}", flush=True)
print(f"Test 2 (1 ep /query + lifespan):      {'PASS' if p2 else 'FAIL'}", flush=True)
print(f"Test 3 (engine.app direct):           {'PASS' if p3 else 'FAIL'}", flush=True)
print(f"Test 4 (all eps, no lifespan):        {'PASS' if p4 else 'FAIL'}", flush=True)
print(f"Test 5 (5 eps + lifespan):            {'PASS' if p5 else 'FAIL'}", flush=True)
