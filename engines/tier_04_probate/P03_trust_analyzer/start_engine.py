"""
Startup script for P03 Trust Analyzer Intelligence Engine
Launches FastAPI server on port 8653
"""

import sys
from pathlib import Path

# Add engine directory to path
engine_dir = Path(__file__).parent
sys.path.insert(0, str(engine_dir))

if __name__ == "__main__":
    import uvicorn
    from loguru import logger

    logger.info("=" * 80)
    logger.info("P03 TRUST ANALYZER - Intelligence Engine")
    logger.info("Port: 8653")
    logger.info("Domain: Trust Law (Texas Trust Code + IRC)")
    logger.info("=" * 80)

    uvicorn.run(
        "engine:app",
        host="0.0.0.0",
        port=8653,
        reload=False,
        log_level="info",
        access_log=True
    )
