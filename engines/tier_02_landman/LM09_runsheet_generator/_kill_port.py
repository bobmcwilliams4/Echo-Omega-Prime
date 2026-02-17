"""Kill any process on port 8509."""
import subprocess
import os
import signal
import time

my_pid = os.getpid()
r = subprocess.run(
    ["powershell", "-Command",
     "Get-NetTCPConnection -LocalPort 8509 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique"],
    capture_output=True, text=True,
)
pids = [int(p.strip()) for p in r.stdout.strip().split("\n") if p.strip().isdigit()]
for pid in pids:
    if pid != my_pid:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Killed PID {pid}")
        except Exception as e:
            print(f"Could not kill {pid}: {e}")

if not pids:
    print("Port 8509 is FREE")
else:
    time.sleep(2)
    print("Cleaned")
