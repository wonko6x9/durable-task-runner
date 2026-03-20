# durable-task-runner

Durable task orchestration scaffolding for OpenClaw.

Current contents:
- Agent skill: `SKILL.md`
- Reference schema: `references/task-schema.md`
- Control helper: `scripts/task_ctl.py`
- Subagent/controller helper: `scripts/task_subagent_ctl.py`
- Source provenance: `ATTRIBUTION.md`

Purpose:
- survive resets/restarts
- keep append-only event logs
- support pause/stop/steer
- provide milestone-aware progress tracking
- support orchestration-first, subagent-worker execution

Influences / provenance:
- This project is informed by ClawHub skills including `task-resume`, `restart-safe-workflow`, and `subagent-orchestrator`.
- See `ATTRIBUTION.md` for what was borrowed conceptually and what was not copied.

Status:
- initial scaffold only
- planner/orchestrator/resume automation still to be implemented
tionally minimal: enough structure to prevent dropped work, not enough to require a ritual manual
