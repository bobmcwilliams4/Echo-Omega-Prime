import time, httpx
time.sleep(5)
try:
    r = httpx.get("http://localhost:8381/health", timeout=5)
    print(r.status_code, r.json().get("status", "unknown"))
except Exception as e:
    print(f"FAIL: {e}")
