# durable-task-runner

Durable task orchestration scaffolding for OpenClaw.

Current contents:
- Agent skill: `SKILL.md`
- Reference schema: `references/task-schema.md`
- Control helper: `scripts/task_ctl.py`

Purpose:
- survive resets/restarts
- keep append-only event logs
- support pause/stop/steer
- provide milestone-aware progress tracking
- support orchestration-first, subagent-worker execution

Status:
- initial scaffold only
- planner/orchestrator/resume automation still to be implemented
