"""Test: import the real app from engine.py and run it with uvicorn."""
import sys
from pathlib import Path

engine_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(engine_dir))
sys.path.insert(0, str(engine_dir.parent / "_shared"))

import uvicorn

# Import the real app — this runs all module-level code
print("Importing engine module...", flush=True)
import engine
print(f"Import done. App routes: {len(engine.app.routes)}", flush=True)

if __name__ == "__main__":
    print(f"Starting with {len(engine.app.routes)} routes on port 8509", flush=True)
    uvicorn.run(engine.app, host="0.0.0.0", port=8509, log_level="info", http="h11")
