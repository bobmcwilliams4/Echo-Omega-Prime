"""Minimal test — does a basic FastAPI app work from this directory?"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="LM09 Minimal Test")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"engine": "LM09 minimal"}

if __name__ == "__main__":
    print("Starting minimal LM09 test on port 8509", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8509, log_level="info")
