"""Isolation test: does importing engine.py corrupt the process?

Test 1: Import engine module, create a COMPLETELY INDEPENDENT app (no routes from engine), test HTTP.
Test 2: If Test 1 passes, add ONE route from engine and re-test.
"""
import sys
import time
import threading
import httpx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Step 1: Import the engine module (this registers all module-level code)
print(f"[{time.time():.1f}] Importing engine module...", flush=True)
t0 = time.time()
import engine
print(f"[{time.time()-t0:.2f}s] Engine imported. app has {len(engine.app.routes)} routes", flush=True)

# Step 2: Create a COMPLETELY INDEPENDENT FastAPI app
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

test_app = FastAPI(title="Isolation Test")
test_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@test_app.get("/health")
async def health():
    return {"status": "ok", "test": "isolation"}

@test_app.get("/")
async def root():
    return {"engine": "isolation test"}

print(f"[{time.time()-t0:.2f}s] Independent app created with {len(test_app.routes)} routes", flush=True)

# Step 3: Launch with uvicorn in a thread and test HTTP
def run_server():
    uvicorn.run(test_app, host="127.0.0.1", port=8509, log_level="warning")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
print(f"[{time.time()-t0:.2f}s] Server thread started, waiting 3s...", flush=True)
time.sleep(3)

# Step 4: Test HTTP
try:
    resp = httpx.get("http://127.0.0.1:8509/health", timeout=5.0)
    print(f"[{time.time()-t0:.2f}s] TEST 1 PASSED: status={resp.status_code} body={resp.text[:200]}", flush=True)
except Exception as e:
    print(f"[{time.time()-t0:.2f}s] TEST 1 FAILED: {e}", flush=True)
    sys.exit(1)

print("TEST 1 RESULT: Independent app works AFTER importing engine module.", flush=True)
print("The import itself does NOT corrupt the process globally.", flush=True)
print("The issue is with engine.app's routes/endpoint functions.", flush=True)
sys.exit(0)
