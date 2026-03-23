# STATUS.md

## Current phase

Programmatic progress-bar hardening

## Health

healthy

## Current milestone

Programmatic reporting cadence and bar-signal cleanup

## Last checkpoint

- Added a new top backlog item for hot-context compaction guardrails: checkpoint durable work around 45% session context and treat 50% as the hard stop for clean handoff/reset
- Confirmed the timed reporting lane is already architecturally independent of human commentary (`task_tick_all.py` -> `task_send_status.py` -> `task_ticker.py`)
- Identified two concrete issues: default cadence is still too slow at 300 seconds, and current-task percent falls back to a vague overall average when no milestone is explicitly marked `running`
- Bound the new hardening task to the live Telegram chat so the reporting system can prove itself while being improved

## In-progress work

- reduce default timed status cadence to 60 seconds
- tighten ticker math so the current-task bar reflects explicit milestone state rather than narrative/operator feel
- keep timed status lines compact, programmatic, and clearly separate from human commentary
- pause-clean stale ordinary tasks that have no executable continuation hook instead of letting them loop forever as fake `running`
- verify the live/timed path behaves consistently with the new defaults

## Next step

- wire the 50% context hard-stop into the same durability/control path
- verify resumed-session continuation is immediate after reset
- update docs/changelog if the behavior change is solid

## Blockers

- none currently confirmed in code/package state
- live cadence verification depends on waiting long enough to observe at least one due timed tick after the code changes
