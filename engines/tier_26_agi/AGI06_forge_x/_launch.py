"""Launch FORGE-X with Azure key."""
import os
import subprocess
import sys

# Load key from environment (set via .env or vault — never hardcode)
if "AZURE_ECHOOMEGA_KEY" not in os.environ:
    raise RuntimeError("AZURE_ECHOOMEGA_KEY not set in environment")

subprocess.Popen(
    [sys.executable, "engine.py"],
    cwd=r"O:\ECHO_OMEGA_PRIME\SYSTEMS\engines\AGI06_forge_x",
    env={**os.environ},
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
print("FORGE-X launched on port 8875")
