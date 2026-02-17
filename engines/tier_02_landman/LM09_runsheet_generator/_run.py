"""Wrapper launcher for LM09 to avoid module double-import issues."""
import sys
from pathlib import Path

# Set up paths
engine_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(engine_dir))
sys.path.insert(0, str(engine_dir.parent / "_shared"))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=8509,
        reload=False,
        log_level="info",
    )
