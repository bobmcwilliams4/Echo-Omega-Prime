"""
ECHO OMEGA PRIME — Standardized Engine Launcher
================================================
Usage:
    python engine_launcher.py <engine_dir> [--port PORT] [--service] [--install-deps]

This launcher:
1. Detects whether engine has a local .venv or uses global py311
2. Installs deps from requirements.txt if --install-deps
3. Launches via uvicorn with standardized settings
4. Optionally installs as a Windows service via NSSM

Works identically for all 327+ engines.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PYMANAGER = Path(r"H:\Tools\PyManager\pythons\py311\python.exe")
NSSM = Path(r"H:\Tools\nssm.exe")  # install if missing


def find_python(engine_dir: Path) -> Path:
    """Find the correct Python: local .venv if exists, else global PyManager."""
    venv_python = engine_dir / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return venv_python
    return PYMANAGER


def get_config(engine_dir: Path) -> dict:
    """Load config.json from engine directory."""
    cfg_path = engine_dir / "config.json"
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def create_venv(engine_dir: Path) -> Path:
    """Create a virtualenv using virtualenv (not venv — py311 has no venv module)."""
    venv_dir = engine_dir / ".venv"
    if venv_dir.exists():
        print(f"[launcher] .venv already exists at {venv_dir}")
        return venv_dir / "Scripts" / "python.exe"

    print(f"[launcher] Creating virtualenv at {venv_dir}")
    subprocess.run(
        [str(PYMANAGER), "-m", "virtualenv", str(venv_dir)],
        check=True,
    )
    venv_python = venv_dir / "Scripts" / "python.exe"

    # Upgrade pip
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
    )
    return venv_python


def install_deps(python: Path, engine_dir: Path) -> None:
    """Install dependencies from requirements.txt if it exists."""
    req = engine_dir / "requirements.txt"
    if req.exists():
        print(f"[launcher] Installing deps from {req}")
        subprocess.run(
            [str(python), "-m", "pip", "install", "-r", str(req)],
            check=True,
        )
    else:
        # Install standard engine deps
        print("[launcher] No requirements.txt — installing standard engine deps")
        subprocess.run(
            [str(python), "-m", "pip", "install",
             "fastapi", "uvicorn", "loguru", "pydantic", "httpx"],
            check=True,
        )


def install_service(engine_dir: Path, engine_id: str, port: int) -> None:
    """Install engine as a Windows service via NSSM."""
    if not NSSM.exists():
        print(f"[launcher] NSSM not found at {NSSM}. Downloading...")
        # Could auto-download, but for now just error
        print("[launcher] Download NSSM from https://nssm.cc and place at H:\\Tools\\nssm.exe")
        sys.exit(1)

    python = find_python(engine_dir)
    svc_name = f"ECHO_{engine_id}"

    cmds = [
        [str(NSSM), "install", svc_name, str(python),
         f"-m uvicorn engine:app --host 0.0.0.0 --port {port}"],
        [str(NSSM), "set", svc_name, "AppDirectory", str(engine_dir)],
        [str(NSSM), "set", svc_name, "DisplayName", f"ECHO Engine {engine_id}"],
        [str(NSSM), "set", svc_name, "Description",
         f"ECHO OMEGA PRIME engine {engine_id} on port {port}"],
        [str(NSSM), "set", svc_name, "AppStdout",
         str(engine_dir / "_logs" / f"{engine_id.lower()}_stdout.log")],
        [str(NSSM), "set", svc_name, "AppStderr",
         str(engine_dir / "_logs" / f"{engine_id.lower()}_stderr.log")],
        [str(NSSM), "set", svc_name, "AppRotateFiles", "1"],
        [str(NSSM), "set", svc_name, "AppRotateBytes", "20000000"],
        [str(NSSM), "set", svc_name, "AppRestartDelay", "5000"],
        [str(NSSM), "set", svc_name, "Start", "SERVICE_AUTO_START"],
    ]

    for cmd in cmds:
        print(f"[launcher] {' '.join(cmd)}")
        subprocess.run(cmd, check=False)

    print(f"[launcher] Service {svc_name} installed. Start with: nssm start {svc_name}")


def launch(engine_dir: Path, port: int) -> None:
    """Launch engine via uvicorn."""
    python = find_python(engine_dir)
    env = os.environ.copy()
    env["PORT"] = str(port)

    print(f"[launcher] Python: {python}")
    print(f"[launcher] Engine: {engine_dir}")
    print(f"[launcher] Port:   {port}")
    print(f"[launcher] Starting uvicorn...")

    os.chdir(str(engine_dir))
    subprocess.run(
        [str(python), "-m", "uvicorn", "engine:app",
         "--host", "0.0.0.0", "--port", str(port)],
        env=env,
        cwd=str(engine_dir),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="ECHO Engine Launcher")
    parser.add_argument("engine_dir", type=Path, help="Path to engine directory")
    parser.add_argument("--port", type=int, default=0, help="Port (overrides config.json)")
    parser.add_argument("--create-venv", action="store_true", help="Create virtualenv for this engine")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies")
    parser.add_argument("--service", action="store_true", help="Install as Windows service via NSSM")
    args = parser.parse_args()

    engine_dir = args.engine_dir.resolve()
    if not engine_dir.exists():
        print(f"[launcher] Engine directory not found: {engine_dir}")
        sys.exit(1)

    config = get_config(engine_dir)
    port = args.port or config.get("port", 8800)
    engine_id = config.get("engine_id", engine_dir.name.split("_")[0])

    if args.create_venv:
        create_venv(engine_dir)

    if args.install_deps:
        python = find_python(engine_dir)
        install_deps(python, engine_dir)

    if args.service:
        install_service(engine_dir, engine_id, port)
        return

    launch(engine_dir, port)


if __name__ == "__main__":
    main()
