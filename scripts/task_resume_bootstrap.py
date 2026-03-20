#!/usr/bin/env python3
"""
Resume / restart bootstrap helper for durable-task-runner.

Purpose:
- inspect durable tasks after reset/restart/startup
- classify which tasks are resumable, paused, stopped, completed, or need attention
- run reconcile checks when configured and useful
- emit a compact operator-facing summary without pretending to auto-resume everything blindly

Design bias:
- explicit, inspectable, low-magic
- prefer clear state classification over ambitious automation theater
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def iter_tasks() -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        if isinstance(data, dict) and data.get("task_id"):
            rows.append((path, data))
    return rows


def append_event(task_id: str, payload: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def append_progress(task_id: str, line: str) -> None:
    path = STATE_DIR / f"{task_id}.progress.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def classify_task(task: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    desired_state = task.get("desired_state")
    reconcile = task.get("reconcile", {}) or {}
    artifacts = task.get("artifacts", []) or []

    attention_lines = 0
    dropped_lines = 0
    for item in artifacts:
        if not isinstance(item, dict) or item.get("kind") != "subagent_lines":
            continue
        for _name, line in (item.get("lines", {}) or {}).items():
            status = line.get("status")
            next_role = line.get("next_role")
            controller_decision = line.get("controller_decision", "pending")
            if status in {"autopilot", "handoff"} and controller_decision == "pending":
                attention_lines += 1
            if status in {"autopilot", "handoff"} and next_role in {None, "", "none"}:
                dropped_lines += 1

    if dropped_lines:
        reasons.append(f"{dropped_lines} dropped orchestration line(s)")
        return "needs_attention", reasons
    if reconcile.get("needed"):
        reasons.append("reconcile still needed")
        return "needs_attention", reasons
    if attention_lines:
        reasons.append(f"{attention_lines} orchestration line(s) awaiting controller action")
        return "needs_attention", reasons
    if desired_state == "running":
        reasons.append("desired_state=running")
        return "resumable", reasons
    if desired_state == "paused":
        reasons.append("desired_state=paused")
        return "paused", reasons
    if desired_state == "stopped":
        reasons.append("desired_state=stopped")
        return "stopped", reasons
    if desired_state == "completed":
        reasons.append("desired_state=completed")
        return "completed", reasons
    if desired_state == "failed":
        reasons.append("desired_state=failed")
        return "failed", reasons
    reasons.append(f"unrecognized desired_state={desired_state}")
    return "needs_attention", reasons


def run_reconcile(task_id: str, reason: str) -> dict[str, Any]:
    cmd = ["python3", str(SCRIPT_DIR / "task_reconcile.py"), task_id, "--reason", reason]
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def inspect_task(path: Path, task: dict[str, Any], run_reconcile_checks: bool) -> dict[str, Any]:
    ts = now_iso()
    task_id = task["task_id"]
    reconcile_result = None
    if run_reconcile_checks and task.get("desired_state") == "running":
        reconcile_result = run_reconcile(task_id, "resume_bootstrap_scan")
        task = load_json(path, task)

    classification, reasons = classify_task(task)
    summary = {
        "task_id": task_id,
        "title": task.get("title", task_id),
        "phase": task.get("phase", ""),
        "health": task.get("health", ""),
        "desired_state": task.get("desired_state"),
        "next_step": task.get("next_step", ""),
        "classification": classification,
        "reasons": reasons,
    }
    if reconcile_result is not None:
        summary["reconcile"] = reconcile_result.get("reconcile", reconcile_result)

    append_event(task_id, {
        "ts": ts,
        "type": "task_reset_detected",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": classification,
        "details": {
            "reasons": reasons,
            "next_step": task.get("next_step", ""),
        },
    })
    append_progress(task_id, f"resume bootstrap scan: {classification} — {'; '.join(reasons)}")
    return summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--task-id")
    p.add_argument("--no-reconcile", action="store_true")
    args = p.parse_args()

    targets = iter_tasks()
    if args.task_id:
        targets = [(p, t) for p, t in targets if t.get("task_id") == args.task_id]
        if not targets:
            raise SystemExit(f"task not found: {args.task_id}")

    summaries = [inspect_task(path, task, run_reconcile_checks=not args.no_reconcile) for path, task in targets]
    buckets = {
        "resumable": [],
        "needs_attention": [],
        "paused": [],
        "stopped": [],
        "completed": [],
        "failed": [],
    }
    for item in summaries:
        buckets.setdefault(item["classification"], []).append(item)

    print(json.dumps({
        "scanned_at": now_iso(),
        "count": len(summaries),
        "summary": {k: len(v) for k, v in buckets.items()},
        "tasks": summaries,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
