"""Isolation test 2: Which approach fixes the broken routes?

Test A: add_api_route with engine endpoint functions (no response_model)
Test B: add_api_route with engine endpoint functions (WITH response_model)
Test C: Proxy wrapper functions that delegate to engine endpoints
"""
import sys
import time
import threading
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import engine
print(f"Engine imported. {len(engine.app.routes)} routes", flush=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

PORT = 8509

def test_app(label, app_factory):
    """Test an app factory — launch, hit health, shutdown."""
    app = app_factory()

    stop_event = threading.Event()

    class UvicornServer(uvicorn.Server):
        def install_signal_handlers(self):
            pass

    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
    server = UvicornServer(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(3)

    try:
        resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
        result = f"PASS (status={resp.status_code})"
    except Exception as e:
        result = f"FAIL ({e})"

    server.should_exit = True
    thread.join(timeout=5)
    time.sleep(1)  # Let port release

    print(f"  {label}: {result}", flush=True)
    return "PASS" in result


# ─── Test A: add_api_route with endpoint functions, NO response_model ───
print("\nTest A: add_api_route (no response_model)...", flush=True)
def factory_a():
    a = FastAPI(title="Test A")
    a.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    for r in engine.app.routes:
        if isinstance(r, APIRoute) and r.path == "/health":
            a.add_api_route(r.path, r.endpoint, methods=list(r.methods), name=r.name)
            break
    return a
pass_a = test_app("A", factory_a)

# ─── Test B: add_api_route WITH response_model ───
print("\nTest B: add_api_route (with response_model)...", flush=True)
def factory_b():
    b = FastAPI(title="Test B")
    b.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    for r in engine.app.routes:
        if isinstance(r, APIRoute) and r.path == "/health":
            b.add_api_route(r.path, r.endpoint, methods=list(r.methods), name=r.name, response_model=r.response_model)
            break
    return b
pass_b = test_app("B", factory_b)

# ─── Test C: Proxy wrapper function ───
print("\nTest C: Proxy wrapper function...", flush=True)
def factory_c():
    c = FastAPI(title="Test C")
    c.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @c.get("/health")
    async def proxy_health():
        return await engine.health_check()
    return c
pass_c = test_app("C", factory_c)

# ─── Test D: Use engine.app directly (expected to fail) ───
print("\nTest D: engine.app directly (expect FAIL)...", flush=True)
def factory_d():
    return engine.app
pass_d = test_app("D", factory_d)

# ─── Test E: Proxy ALL routes with simple wrappers ───
print("\nTest E: All routes as proxy wrappers...", flush=True)
def factory_e():
    e = FastAPI(title="Test E", lifespan=engine.lifespan)
    e.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @e.get("/health")
    async def _health():
        return await engine.health_check()

    @e.post("/query")
    async def _query(request: engine.QueryRequest):
        return await engine.process_query(request)

    return e
pass_e = test_app("E", factory_e)

print(f"\n{'='*60}", flush=True)
print(f"Test A (add_api_route, no resp_model):  {'PASS' if pass_a else 'FAIL'}", flush=True)
print(f"Test B (add_api_route, with resp_model): {'PASS' if pass_b else 'FAIL'}", flush=True)
print(f"Test C (proxy wrapper):                  {'PASS' if pass_c else 'FAIL'}", flush=True)
print(f"Test D (engine.app directly):            {'PASS' if pass_d else 'FAIL'}", flush=True)
print(f"Test E (proxy /health + /query):         {'PASS' if pass_e else 'FAIL'}", flush=True)
