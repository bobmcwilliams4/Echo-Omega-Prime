
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Import EVERYTHING engine imports
from doctrines import build_doctrine_cache, get_all_doctrine_topics
from semantic import SemanticNormalizer
from search import RunsheetVectorSearch
from telemetry import TelemetryManager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

cache = build_doctrine_cache()
print(f"Loaded {len(cache)} doctrines", flush=True)

app = FastAPI(title="Minimal LM09")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "ok", "doctrines": len(cache)}

if __name__ == "__main__":
    print("Starting minimal on 8509...", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8509, log_level="warning")
