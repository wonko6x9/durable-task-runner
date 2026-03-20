---
name: durable-task-runner
description: Plan, orchestrate, resume, pause, stop, steer, and verify long-running work using persistent task state, append-only event logs, milestone-based progress, and subagent delegation. Use for multi-step or long-running tasks that must survive agent/gateway resets, provide regular status updates, and continue without repeated user permission.
---

Use this skill when work is large enough that losing state, stalling silently, or stopping mid-run would be harmful.

## When to use

Use this skill when any of the following are true:
- task will likely take more than a few minutes
- task has multiple phases or milestones
- task should survive agent/gateway/session resets
- the user wants regular progress updates
- work can be split across subagents
- task needs pause / stop / steer controls
- task needs a final verification pass before being called done

Do **not** use for trivial one-shot tasks.

## Core model

You are the **orchestrator/project manager**, not the primary laborer.

Your responsibilities:
- create the plan
- define milestones and done criteria
- decide serial vs parallel execution
- decide whether priority is **time** or **tokens**
- assign subtasks to subagents when appropriate
- keep persistent state on disk
- emit regular informational progress updates
- reconcile results
- run verification before declaring completion

Subagents are workers for bounded subtasks.

## Required files

For each durable task, maintain files under:

- `state/tasks/<task-id>.json` — current state snapshot
- `state/tasks/<task-id>.events.jsonl` — append-only event log
- `state/tasks/<task-id>.progress.log` — human-readable progress trail

Use `scripts/task_ctl.py` for state/event/progress operations instead of hand-editing when possible.

## Required workflow

### 1. Plan first

Before execution, create a task with:
- goal
- done criteria
- constraints
- execution priority: `time` or `tokens`
- milestones
- subtasks
- dependency map
- status cadence (default: 5 minutes max)

If the task is long and splittable, decide at planning time whether to use subagents.

### 2. Record baseline state

Create a durable task record before substantial work begins.

Minimum required fields:
- `task_id`
- `title`
- `goal`
- `done_criteria`
- `constraints`
- `desired_state` (`running|paused|stopped|completed|failed`)
- `execution_priority` (`time|tokens`)
- `phase`
- `milestones`
- `subtasks`
- `last_verified_step`
- `next_step`
- `status_update_interval_seconds`

### 3. Break work into bounded units

Avoid monolithic executions when possible.

Prefer:
- scan → checkpoint
- extract → checkpoint
- verify → checkpoint
- summarize → checkpoint

Each meaningful unit should end in a task event and state update.

### 4. Progress updates are informational, not permission-seeking

For active long work, send progress updates:
- at least every **5 minutes**
- immediately on milestone completion
- immediately on phase change
- immediately on blocker / retry / pause / stop / completion

These updates should state:
- task title
- current phase
- last concrete progress
- current health (`healthy|retrying|blocked|paused`)
- next step

Do **not** ask permission to continue unless the next action is materially risky, destructive, external, or ambiguous.

### 5. Pause / stop / steer

Long tasks must be steerable.

Check `desired_state` on resume boundaries and milestone boundaries.
If the user requests pause/stop/steer:
- record the request in the event log
- safely checkpoint
- acknowledge the control state

### 6. Resume after interruption

On re-entry after reset/restart/interruption:
- load the task snapshot
- review recent events
- verify the immediately prior step
- if last step is inconsistent, rewind to last known-good checkpoint
- continue without re-asking the user if `desired_state=running`

### 7. Verify before declaring done

Before calling the task complete:
- verify milestone outputs
- verify final outputs
- record verification result in event log
- only then mark `desired_state=completed`

## Subagent strategy

Decide up front whether subagents are worth using.

### If priority is `time`
- use subagents for independent branches
- assign one bounded milestone/subtask per worker where possible
- avoid overlapping write targets unless coordination is explicit

### If priority is `tokens`
- prefer serial/local/scripted work
- use fewer subagents
- minimize agent-to-agent chatter

## Scripts

Use these helpers:
- `scripts/task_ctl.py` — create/update/log/control durable tasks
- `scripts/task_resume_queue.py` — interruption queue helper for resume-after-context-switch behavior

Read these references when needed:
- `references/task-schema.md` — durable task state/event structure
- `references/subagent-return-protocol.md` — structured worker return format for orchestrated subagent workflows
- `references/control-levels.md` — 0..N process/control levels and artifact-selection logic

## Attribution discipline

When this skill or its helpers borrow ideas or adapted code from external skills/packages:
- record the source in `ATTRIBUTION.md`
- add inline attribution notes in the relevant file header when the lineage is direct
- do not quietly absorb other authors' work without credit
