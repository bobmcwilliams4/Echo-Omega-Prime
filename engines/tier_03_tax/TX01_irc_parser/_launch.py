"""
TX01 IRC Parser Engine Launcher
Quick launcher with pre-flight validation
"""

import sys
from pathlib import Path
import subprocess

# Add Python path
PYTHON = Path(r"H:\Tools\PyManager\pythons\py311\python.exe")

def main():
    engine_dir = Path(__file__).parent
    engine_file = engine_dir / "engine.py"

    print(f"=" * 80)
    print(f"TX01 IRC Parser Engine v1.0.0")
    print(f"=" * 80)
    print(f"Engine file: {engine_file}")
    print(f"Python: {PYTHON}")
    print(f"=" * 80)

    # Pre-flight checks
    if not engine_file.exists():
        print(f"ERROR: engine.py not found at {engine_file}")
        return 1

    if not PYTHON.exists():
        print(f"ERROR: Python not found at {PYTHON}")
        return 1

    print("Pre-flight checks passed. Launching engine...")
    print()

    # Launch engine
    try:
        subprocess.run(
            [str(PYTHON), str(engine_file)],
            cwd=str(engine_dir),
            check=True
        )
    except KeyboardInterrupt:
        print("\nEngine shutdown requested by user")
        return 0
    except Exception as e:
        print(f"ERROR launching engine: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
