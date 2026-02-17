"""
TX03 Credit Calculator Engine - Launch Script
Quick launcher for the credit calculator engine
"""

import sys
import subprocess
from pathlib import Path

ENGINE_DIR = Path(__file__).parent
ENGINE_FILE = ENGINE_DIR / "engine.py"
PYTHON_EXE = r"H:\Tools\PyManager\pythons\py311\python.exe"


def main():
    """Launch TX03 Credit Calculator Engine"""
    print("=" * 80)
    print("TX03 CREDIT CALCULATOR ENGINE - LAUNCH")
    print("=" * 80)
    print(f"Engine: {ENGINE_FILE}")
    print(f"Python: {PYTHON_EXE}")
    print(f"Port: 8603")
    print("=" * 80)

    try:
        # Launch engine
        subprocess.run([PYTHON_EXE, str(ENGINE_FILE)], check=True)
    except KeyboardInterrupt:
        print("\nEngine stopped by user")
    except Exception as e:
        print(f"Error launching engine: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
