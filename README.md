# durable-task-runner

Durable task orchestration scaffolding for OpenClaw.

Current contents:
- Agent skill: `SKILL.md`
- Reference schema: `references/task-schema.md`
- Control helper: `scripts/task_ctl.py`
- Reporting helpers: `scripts/task_report.py`, `scripts/task_ticker.py`, `scripts/task_send_status.py`, `scripts/task_status_tick.sh`
- Reconcile/resume helpers: `scripts/task_reconcile.py`, `scripts/task_resume_bootstrap.py`, `scripts/task_resume_apply.py`
- Subagent/controller helpers: `scripts/task_subagent_ctl.py`, `scripts/task_subagent_spawn.py`, `scripts/task_subagent_run.py`
- Repeatable validation harness: `scripts/task_validation_smoke.py`
- Source provenance: `ATTRIBUTION.md`

Purpose:
- survive resets/restarts
- keep append-only event logs
- support pause/stop/steer
- provide milestone-aware progress tracking
- support orchestration-first, subagent-worker execution
- keep long work moving without depending on fragile live agent memory

Influences / provenance:
- This project is informed by ClawHub skills including `task-resume`, `restart-safe-workflow`, and `subagent-orchestrator`.
- See `ATTRIBUTION.md` for what was borrowed conceptually and what was not copied.

Status:
- working prototype
- self-tracks through durable task state/artifacts
- supports restart scan/plan/apply flow
- supports thin controller/worker orchestration with anti-drop checks
- includes repeatable local smoke validation for non-bootstrap resume/apply behavior

Design stance:
- intentionally minimal: enough structure to prevent dropped work, not enough to require a ritual manual
- hybrid/agilefall: iterative implementation with explicit milestones, risks, and operational checkpoints
