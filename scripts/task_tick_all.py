#!/usr/bin/env python3
"""
Run timed status ticks across all eligible durable tasks.

Purpose:
- provide the missing operational runner for recurring status delivery
- scan all task snapshots
- skip tasks that are not active or do not have delivery bindings
- only send when the task is actually due
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def has_delivery_binding(task: dict[str, Any]) -> bool:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "delivery_binding":
            return True
    return False


def iter_tasks() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(STATE_DIR.glob("*.json")):
        data = load_json(path, None)
        if isinstance(data, dict) and data.get("task_id"):
            rows.append(data)
    return rows


def run_json(*args: str) -> dict[str, Any]:
    out = subprocess.check_output(args, text=True)
    return json.loads(out)


def main() -> int:
    scanned = 0
    eligible = 0
    sent = 0
    results = []

    for task in iter_tasks():
        scanned += 1
        task_id = task["task_id"]
        if task.get("desired_state") != "running":
            results.append({"task_id": task_id, "status": "skipped", "reason": "not_running"})
            continue
        if not has_delivery_binding(task):
            results.append({"task_id": task_id, "status": "skipped", "reason": "no_delivery_binding"})
            continue
        eligible += 1
        due = run_json("python3", str(SCRIPT_DIR / "task_should_report.py"), task_id)
        if not due.get("due"):
            results.append({"task_id": task_id, "status": "skipped", "reason": due.get("reason", "not_due")})
            continue
        delivery = run_json("python3", str(SCRIPT_DIR / "task_send_status.py"), task_id)
        sent += 1
        results.append({
            "task_id": task_id,
            "status": "sent",
            "reason": due.get("reason", "due"),
            "line": delivery.get("line", ""),
        })

    print(json.dumps({
        "scanned": scanned,
        "eligible": eligible,
        "sent": sent,
        "results": results,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
