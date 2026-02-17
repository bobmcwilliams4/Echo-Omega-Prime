"""Test — does LM09 work with its real lifespan function?"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import LM09's actual components
from doctrines import build_doctrine_cache, get_all_doctrine_topics
from semantic import SemanticNormalizer
from search import RunsheetVectorSearch, SearchDocument
from telemetry import TelemetryManager

ENGINE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = ENGINE_DIR / "vectors"
LOG_DIR = ENGINE_DIR / "logs"
VECTOR_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

print("Imports successful", flush=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan starting...", flush=True)
    doctrine_cache = build_doctrine_cache()
    print(f"Loaded {len(doctrine_cache)} doctrines", flush=True)
    normalizer = SemanticNormalizer()
    vector_search = RunsheetVectorSearch(index_path=VECTOR_DIR / "test.db")
    # Seed vector index
    docs = []
    for topic, doctrine in doctrine_cache.items():
        content = f"{doctrine.conclusion_template}\n\n{doctrine.reasoning_framework}"
        docs.append(SearchDocument(
            doc_id=f"doctrine_{topic}",
            title=doctrine.topic,
            content=content,
            category=doctrine.issue_category.value,
            keywords=doctrine.keywords,
            authority_weight=doctrine.confidence,
        ))
    vector_search.add_documents(docs)
    print(f"Vector index seeded with {len(docs)} docs", flush=True)

    all_topics = get_all_doctrine_topics()
    telemetry_mgr = TelemetryManager(
        engine_id="LM09",
        doctrine_topics=all_topics,
        audit_log_path=LOG_DIR / "test_audit.jsonl",
    )
    print("Telemetry initialized", flush=True)
    print("Lifespan complete — yielding", flush=True)
    yield
    print("Shutting down", flush=True)

app = FastAPI(title="LM09 Lifespan Test", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok", "engine": "LM09 lifespan test"}

if __name__ == "__main__":
    print("Starting LM09 lifespan test on port 8509", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8509, log_level="info")
