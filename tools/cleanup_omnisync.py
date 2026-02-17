"""
Clean up stale OmniSync todos.

Archives completed/stale todos by marking them, doesn't delete.
Requires ECHO_API_KEY environment variable.

Usage:
    python tools/cleanup_omnisync.py --dry-run
    python tools/cleanup_omnisync.py --archive-completed
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.request
import urllib.error

OMNISYNC_URL = "https://omniscient-sync.bmcii1976.workers.dev"


def fetch_todos(api_key: str) -> list[dict]:
    """Fetch all todos from OmniSync."""
    req = urllib.request.Request(f"{OMNISYNC_URL}/todos")
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data.get("todos", data) if isinstance(data, dict) else data


def update_todo(todo_id: int, updates: dict, api_key: str) -> dict:
    """Update a todo via OmniSync API."""
    req = urllib.request.Request(
        f"{OMNISYNC_URL}/todos/{todo_id}",
        data=json.dumps(updates).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Echo-API-Key": api_key,
        },
        method="PUT",
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def main():
    parser = argparse.ArgumentParser(description="Clean up OmniSync stale todos")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--archive-completed", action="store_true", help="Mark completed todos as archived")
    args = parser.parse_args()

    api_key = os.environ.get("ECHO_API_KEY", "")
    if not api_key and not args.dry_run:
        print("ERROR: Set ECHO_API_KEY environment variable")
        return

    todos = fetch_todos(api_key)
    print(f"Total todos: {len(todos)}")

    completed = [t for t in todos if t.get("status") in ("completed", "complete")]
    pending = [t for t in todos if t.get("status") == "pending"]
    stale_pending = [t for t in pending if not t.get("title") or t.get("title") == "Untitled"]

    print(f"  Completed: {len(completed)}")
    print(f"  Pending:   {len(pending)}")
    print(f"  Stale (Untitled pending): {len(stale_pending)}")

    if args.archive_completed:
        print(f"\n{'DRY RUN — ' if args.dry_run else ''}Archiving {len(completed)} completed todos...")
        for t in completed:
            tid = t.get("id")
            title = t.get("title", t.get("text", "?"))[:60]
            if args.dry_run:
                print(f"  Would archive #{tid}: {title}")
            else:
                try:
                    update_todo(tid, {"status": "archived"}, api_key)
                    print(f"  Archived #{tid}: {title}")
                except urllib.error.HTTPError as e:
                    print(f"  Failed #{tid}: {e}")

    print(f"\nStale untitled todos (candidates for cleanup):")
    for t in stale_pending[:20]:
        tid = t.get("id")
        print(f"  #{tid}: status={t.get('status')} title={t.get('title', '(none)')}")


if __name__ == "__main__":
    main()
