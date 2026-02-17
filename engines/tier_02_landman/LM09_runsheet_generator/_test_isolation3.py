"""Isolation test 3: add_api_route with ALL engine routes."""
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

# Create fresh app with ALL routes via add_api_route
app = FastAPI(title="LM09 Fresh", lifespan=engine.lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

skip = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
count = 0
for r in engine.app.routes:
    if isinstance(r, APIRoute) and r.path not in skip:
        app.add_api_route(
            r.path,
            r.endpoint,
            methods=list(r.methods) if r.methods else ["GET"],
            name=r.name,
        )
        count += 1
        print(f"  Registered: {list(r.methods) if r.methods else 'GET'} {r.path}", flush=True)

print(f"\nFresh app has {len(app.routes)} routes ({count} from engine)", flush=True)

# Launch and test
class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
server = UvicornServer(config)
thread = threading.Thread(target=server.run, daemon=True)
thread.start()
print(f"Server started, waiting 5s...", flush=True)
time.sleep(5)

# Test health
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
    print(f"HEALTH: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"HEALTH FAILED: {e}", flush=True)

# Test root
try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/", timeout=5.0)
    print(f"ROOT: {resp.status_code} {resp.text[:200]}", flush=True)
except Exception as e:
    print(f"ROOT FAILED: {e}", flush=True)

# Test query
try:
    resp = httpx.post(
        f"http://127.0.0.1:{PORT}/query",
        json={"query": "What is a run sheet?", "mode": "FAST"},
        timeout=10.0,
    )
    print(f"QUERY: {resp.status_code} {resp.text[:300]}", flush=True)
except Exception as e:
    print(f"QUERY FAILED: {e}", flush=True)

server.should_exit = True
thread.join(timeout=5)
print("DONE", flush=True)
