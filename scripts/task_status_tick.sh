#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <task-id>" >&2
  exit 2
fi

TASK_ID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DUE_JSON="$(python3 "$SCRIPT_DIR/task_should_report.py" "$TASK_ID")"
DUE="$(printf '%s' "$DUE_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["due"])')"

if [ "$DUE" != "True" ] && [ "$DUE" != "true" ]; then
  exit 0
fi

LINE="$(python3 "$SCRIPT_DIR/task_ticker.py" "$TASK_ID")"
python3 "$SCRIPT_DIR/task_ctl.py" progress "$TASK_ID" "$LINE" >/dev/null
printf '%s\n' "$LINE"
