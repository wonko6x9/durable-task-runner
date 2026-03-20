#!/usr/bin/env python3
"""
Apply low-risk resume follow-through from task_resume_bootstrap plans.

Purpose:
- bridge bootstrap output into actual controller/state follow-through
- keep durable tasks moving after reporting their restart status
- stay intentionally narrow: only apply obvious, low-risk resume actions

Current scope:
- consumes the bootstrap helper JSON output (`--plan` recommended)
- updates task state/progress for resumable tasks
- records a resume_started event with the chosen action
- does NOT try to execute arbitrary worker logic or invent new branching
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def save_task(task: dict[str, Any]) -> None:
    (STATE_DIR / f"{task['task_id']}.json").write_text(json.dumps(task, indent=2) + "\n")


def append_event(task_id: str, payload: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def append_progress(task_id: str, line: str) -> None:
    path = STATE_DIR / f"{task_id}.progress.log"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def pick_active_line(task: dict[str, Any]) -> str | None:
    for item in task.get("artifacts", []):
        if not isinstance(item, dict) or item.get("kind") != "subagent_lines":
            continue
        for name, line in (item.get("lines", {}) or {}).items():
            if line.get("status") == "assigned":
                return name
    return None


def apply_task(plan_item: dict[str, Any]) -> dict[str, Any]:
    task_id = plan_item["task_id"]
    task = load_task(task_id)
    ts = now_iso()
    action = plan_item.get("resume_plan", {}).get("action") or plan_item.get("recommendation", {}).get("action")
    next_step = task.get("next_step", "")
    applied = {
        "task_id": task_id,
        "action": action,
        "applied": False,
        "note": "",
    }

    if action in {"resume_active_line", "resume_main_flow"}:
        task["desired_state"] = "running"
        task["phase"] = task.get("phase", "resume-bootstrap")
        task["updated_at"] = ts
        active_line = pick_active_line(task)
        if action == "resume_active_line" and active_line:
            task["next_step"] = f"continue active line: {active_line}"
            applied["note"] = f"controller resumed active line {active_line}"
        else:
            task["next_step"] = next_step or "resume main execution"
            applied["note"] = "controller resumed main flow"
        save_task(task)
        append_event(task_id, {
            "ts": ts,
            "type": "resume_started",
            "task_id": task_id,
            "phase": task.get("phase", ""),
            "status": "ok",
            "details": {
                "action": action,
                "note": applied["note"],
            },
        })
        append_progress(task_id, f"resume apply: {applied['note']}")
        applied["applied"] = True
        return applied

    applied["note"] = "no low-risk auto-apply path for this action"
    return applied


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="bootstrap JSON file; defaults to stdin")
    args = p.parse_args()

    raw = Path(args.file).read_text() if args.file else __import__("sys").stdin.read()
    payload = json.loads(raw)
    tasks = payload.get("tasks", [])
    results = [apply_task(item) for item in tasks]
    print(json.dumps({"applied": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
