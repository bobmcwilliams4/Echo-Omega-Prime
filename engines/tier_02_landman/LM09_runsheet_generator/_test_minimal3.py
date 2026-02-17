
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

# Import the full engine module
import engine
print(f"Engine imported: {len(engine.app.routes)} routes", flush=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="With Engine Import")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print(f"Starting on 8509...", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8509, log_level="warning")
