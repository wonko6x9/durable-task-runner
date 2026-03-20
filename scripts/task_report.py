#!/usr/bin/env python3
"""
Reporting helper for durable-task-runner.

Attribution note:
- Original to this repo, but informed by the broader reporting/progress ideas harvested
  from ClawHub patterns and by project requirements gathered during this build.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def summarize_milestones(milestones: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(milestones)
    done = sum(1 for m in milestones if m.get("status") == "done")
    running = [m for m in milestones if m.get("status") == "running"]
    pending = [m for m in milestones if m.get("status") == "pending"]
    return {
        "total": total,
        "done": done,
        "running": running[0] if running else None,
        "pending_count": len(pending),
    }


def render(task: dict[str, Any], level: int, defaults: dict[str, Any]) -> str:
    title = task.get("title", task.get("task_id"))
    phase = task.get("phase", "")
    health = task.get("health", "")
    next_step = task.get("next_step", "")
    ms = summarize_milestones(task.get("milestones", []))
    running_title = ms["running"]["title"] if ms["running"] else "none"

    if level <= 0:
        return f"{title}: still running."
    if level == 1:
        return (
            f"{title}: milestone status {ms['done']}/{ms['total']} complete; "
            f"current milestone: {running_title}; next: {next_step or 'n/a'}."
        )
    if level == 2:
        return (
            f"{title}: phase={phase}; health={health}; milestones {ms['done']}/{ms['total']} complete; "
            f"current milestone: {running_title}; next: {next_step or 'n/a'}."
        )
    if level == 3:
        return (
            f"{title}: phase={phase}; health={health}; milestones {ms['done']}/{ms['total']} complete; "
            f"current milestone: {running_title}; pending milestones: {ms['pending_count']}; next: {next_step or 'n/a'}."
        )
    return json.dumps({
        "title": title,
        "phase": phase,
        "health": health,
        "milestones": task.get("milestones", []),
        "subtasks": task.get("subtasks", []),
        "next_step": next_step,
        "defaults": defaults.get("reporting", {}),
    }, indent=2)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("--level", type=int)
    args = p.parse_args()

    defaults = load_json(CONFIG_PATH, {})
    default_level = int(defaults.get("engagement", {}).get("default_reporting_level", 1))
    level = args.level if args.level is not None else default_level
    task = load_task(args.task_id)
    print(render(task, level, defaults))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
