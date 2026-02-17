"""Isolation test 4: ALL routes via add_api_route, NO lifespan."""
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

# Test 1: ALL routes, NO lifespan
print("\n=== Test 1: All routes, NO lifespan ===", flush=True)
app1 = FastAPI(title="LM09 NoLifespan")
app1.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
skip = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path not in skip:
        app1.add_api_route(r.path, r.endpoint, methods=list(r.methods) if r.methods else ["GET"], name=r.name)
print(f"App1: {len(app1.routes)} routes, no lifespan", flush=True)

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass

config1 = uvicorn.Config(app1, host="127.0.0.1", port=PORT, log_level="warning")
server1 = UServer(config1)
t1 = threading.Thread(target=server1.run, daemon=True)
t1.start()
time.sleep(3)
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/", timeout=5.0)
    print(f"  ROOT: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"  ROOT: FAIL ({e})", flush=True)
server1.should_exit = True
t1.join(timeout=5)
time.sleep(2)

# Test 2: JUST health + query + lifespan
print("\n=== Test 2: Just /health + /query, WITH lifespan ===", flush=True)
app2 = FastAPI(title="LM09 MinRoutes", lifespan=engine.lifespan)
app2.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path in ("/health", "/query"):
        app2.add_api_route(r.path, r.endpoint, methods=list(r.methods) if r.methods else ["GET"], name=r.name)
print(f"App2: {len(app2.routes)} routes, with lifespan", flush=True)

config2 = uvicorn.Config(app2, host="127.0.0.1", port=PORT, log_level="warning")
server2 = UServer(config2)
t2 = threading.Thread(target=server2.run, daemon=True)
t2.start()
time.sleep(5)
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
    print(f"  HEALTH: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"  HEALTH: FAIL ({e})", flush=True)
server2.should_exit = True
t2.join(timeout=5)
time.sleep(2)

# Test 3: Binary search — first half of routes + lifespan
print("\n=== Test 3: First 20 routes + lifespan ===", flush=True)
app3 = FastAPI(title="LM09 Half", lifespan=engine.lifespan)
app3.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
api_routes = [r for r in engine.app.routes if isinstance(r, APIRoute) and r.path not in skip]
for r in api_routes[:20]:
    app3.add_api_route(r.path, r.endpoint, methods=list(r.methods) if r.methods else ["GET"], name=r.name)
print(f"App3: {len(app3.routes)} routes (first 20), with lifespan", flush=True)

config3 = uvicorn.Config(app3, host="127.0.0.1", port=PORT, log_level="warning")
server3 = UServer(config3)
t3 = threading.Thread(target=server3.run, daemon=True)
t3.start()
time.sleep(5)
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
    print(f"  HEALTH: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"  HEALTH: FAIL ({e})", flush=True)
server3.should_exit = True
t3.join(timeout=5)
time.sleep(2)

# Test 4: JUST lifespan, 1 fresh route (control)
print("\n=== Test 4: Lifespan + 1 fresh route (control) ===", flush=True)
app4 = FastAPI(title="LM09 Control", lifespan=engine.lifespan)
app4.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app4.get("/health")
async def fresh_health():
    return {"status": "ok", "test": "control"}

config4 = uvicorn.Config(app4, host="127.0.0.1", port=PORT, log_level="warning")
server4 = UServer(config4)
t4 = threading.Thread(target=server4.run, daemon=True)
t4.start()
time.sleep(5)
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
    print(f"  HEALTH: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"  HEALTH: FAIL ({e})", flush=True)
server4.should_exit = True
t4.join(timeout=5)

print("\nDONE", flush=True)
