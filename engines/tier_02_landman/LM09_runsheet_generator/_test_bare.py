"""Bare minimum test — no engine import at all."""
import sys
import time
import threading
import httpx
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PORT = 8519

class UServer(uvicorn.Server):
    def install_signal_handlers(self): pass

@asynccontextmanager
async def lifespan(app):
    print("Lifespan start", flush=True)
    time.sleep(0.1)
    print("Lifespan yield", flush=True)
    yield
    print("Lifespan end", flush=True)

app = FastAPI(title="Bare Test", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "ok"}

config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
server = UServer(config)
thread = threading.Thread(target=server.run, daemon=True)
thread.start()
time.sleep(3)

try:
    resp = httpx.get(f"http://127.0.0.1:{PORT}/health", timeout=5.0)
    print(f"BARE: PASS ({resp.status_code})", flush=True)
except Exception as e:
    print(f"BARE: FAIL ({e})", flush=True)

server.should_exit = True
thread.join(timeout=5)
print("DONE", flush=True)
