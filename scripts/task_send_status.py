#!/usr/bin/env python3
"""
Send a compact timed status line using the task's bound delivery metadata.

Current scope:
- read delivery binding from task artifacts
- render compact ticker line
- send via `openclaw message send`
- record progress update locally after successful send
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def delivery_binding(task: dict[str, Any]) -> dict[str, Any]:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "delivery_binding":
            return item
    raise SystemExit("no delivery_binding artifact found")


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: task_send_status.py <task-id>")
    task_id = sys.argv[1]
    task = load_task(task_id)
    binding = delivery_binding(task)
    line = run("python3", str(SCRIPT_DIR / "task_ticker.py"), task_id)

    cmd = [
        "openclaw", "message", "send",
        "--channel", binding["channel"],
        "--target", binding["target"],
        "--account", binding.get("account_id", "default"),
        "--message", line,
        "--json",
    ]
    send_out = subprocess.check_output(cmd, text=True).strip()
    subprocess.check_call([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "progress", task_id, line
    ])
    print(json.dumps({"sent": True, "line": line, "delivery": json.loads(send_out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
