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


def extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    starts = [i for i, ch in enumerate(raw) if ch == "{"]
    best: dict[str, Any] | None = None
    for start in starts:
        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(raw)):
            ch = raw[idx]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = raw[start:idx + 1]
                    try:
                        value = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    if isinstance(value, dict):
                        best = value
                    break
    if best is not None:
        return best
    raise SystemExit(f"could not parse JSON payload from openclaw output: {raw}")


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
    proc = subprocess.run(cmd, text=True, capture_output=True, check=True)
    combined_output = "\n".join(part for part in [proc.stdout.strip(), proc.stderr.strip()] if part).strip()
    delivery = extract_json_object(combined_output) if combined_output else {"raw": ""}
    subprocess.run([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "progress", task_id, line
    ], check=True, stdout=subprocess.DEVNULL)
    print(json.dumps({
        "sent": True,
        "line": line,
        "delivery": delivery,
        "raw_output": combined_output,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
