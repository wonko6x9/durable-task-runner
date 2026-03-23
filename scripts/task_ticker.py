#!/usr/bin/env python3
"""
Compact timed status renderer for durable-task-runner.

Goal:
- minimal tokens
- maximum signal
- suitable for recurring status delivery regardless of milestone
- show both current-task progress and overall-project progress
- remain fully programmatic and independent of human commentary
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def progress_bar(percent: int, width: int = 10) -> str:
    percent = max(0, min(100, percent))
    filled = round((percent / 100) * width)
    return "[" + ("#" * filled) + ("." * (width - filled)) + "]"


def overall_percent(task: dict[str, Any]) -> int:
    milestones = task.get("milestones", [])
    if not milestones:
        return 0
    vals = [int(m.get("percent", 0)) for m in milestones]
    return round(sum(vals) / len(vals))


def completed_milestone_count(task: dict[str, Any]) -> int:
    return sum(1 for m in task.get("milestones", []) if m.get("status") == "done")


def milestone_counts(task: dict[str, Any]) -> tuple[int, int]:
    milestones = task.get("milestones", [])
    return completed_milestone_count(task), len(milestones)


def current_milestone_record(task: dict[str, Any]) -> dict[str, Any] | None:
    for milestone in task.get("milestones", []):
        if milestone.get("status") == "running":
            return milestone
    return None


def current_task_percent(task: dict[str, Any]) -> int:
    milestone = current_milestone_record(task)
    if milestone is not None:
        return int(milestone.get("percent", 0))
    milestones = task.get("milestones", [])
    if milestones and all(m.get("status") == "done" for m in milestones):
        return 100
    done, total = milestone_counts(task)
    if total:
        return round((done / total) * 100)
    return 0


def current_milestone(task: dict[str, Any]) -> str:
    milestone = current_milestone_record(task)
    if milestone is not None:
        return milestone.get("title", "running")
    return "none"


def render(task: dict[str, Any]) -> str:
    current_pct = current_task_percent(task)
    overall_pct = overall_percent(task)
    current_bar = progress_bar(current_pct)
    overall_bar = progress_bar(overall_pct)
    phase = task.get("phase", "?")
    health = task.get("health", "?")
    ms = current_milestone(task)
    next_step = task.get("next_step", "n/a")
    done, total = milestone_counts(task)
    return (
        f"task {current_bar} {current_pct:>3}% | "
        f"proj {overall_bar} {overall_pct:>3}% | "
        f"ms {done}/{total} | "
        f"{phase} | {health} | {ms} | next: {next_step}"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()
    print(render(load_task(args.task_id)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
