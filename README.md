# durable-task-runner

Run long-running, multi-step work in OpenClaw without losing it to resets: durable state, progress updates, reset-safe resume, and optional subagent orchestration.

This repo is the development/workbench version of the skill. It includes dogfooding artifacts, project-history docs, and helper scripts used to build and test the public skill.

## What it does

- persists task state to disk instead of relying on chat memory
- tracks milestones, progress, events, and verification
- survives resets with resume/bootstrap helpers
- supports pause / stop / steer controls
- supports thin controller/worker subagent orchestration
- renders compact status output for longer-running work

## Process model

Durable Task Runner uses a hybrid process model that borrows useful patterns from Agile, PMP-style milestone/scope thinking, structured sequencing where dependencies justify it, and ITIL-style operational discipline.

The goal is not to bury users in process or pretend this is one pure framework. The goal is to strengthen the backend architecture enough that long work actually finishes, keeps moving across resets/interruption, and stays visible while it is in flight.

In practice, the runner:
- scales the amount of process and artifact depth to the size/risk of the task
- asks the user for a few key blanks when needed, then drives the rest through durable state and helper scripts
- uses planning, checkpoints, verification, and resume logic to keep projects moving toward completion
- treats robustness and continued real-world testing as ongoing goals of the framework itself
- refuses to silently leave ordinary tasks in a fake `running` state forever; tasks without an executable continuation hook are reclassified/pause-cleaned instead of generating endless liveness theater

The current priority is practical rather than grandiose: get projects to finish reliably. Industry-standard process ideas are used because they provide a stronger architecture for that than ad-hoc chat memory alone.

## Visibility and progress

Visible progress is a core feature, not cosmetic fluff.

Task and project progress bars, milestone updates, and timed status messages exist to answer the most important operational question during long work: did the task die, or is it still moving?

The bars are intended to be real operational metrics, but not fake precision:
- the **project** bar reflects aggregate milestone completion recorded in durable task state
- the **task** bar reflects the currently active work slice or milestone progress
- both depend on the plan being scoped sanely and updated as the task evolves

So the bars are meaningful, but they are still model-based. They are best treated as liveness/progress indicators grounded in explicit milestone state, not as earned-value accounting or mathematically exact completion truth.

By default, reporting stays low-noise and milestone-oriented. It can also be configured for more regular timed updates, higher-visibility operational reporting, or quieter completion-focused behavior when that better fits the job.

## Repository layout

### Public skill surface
These are the files that matter for the published skill:
- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `LICENSE`
- `ATTRIBUTION.md`
- `config/defaults.json`
- `references/`
- `scripts/`

### Development / dogfooding artifacts
These are useful in the repo, but should not be shoved directly into a ClawHub publish bundle:
- `PLAN.md`
- `BACKLOG.md`
- `DECISIONS.md`
- `STATUS.md`
- `RESET-READY.md`
- `RELEASE.md`

## Runtime requirements

- Python 3.8+
- no external Python dependencies; the scripts are stdlib-only
- OpenClaw runtime/auth is required only for live message delivery paths

## Development checks (repo only)

The development repo includes local smoke checks that are intentionally **not** part of the ClawHub publish bundle.
They are useful for maintainers, not required for normal skill installation/use.

Example repo-local checks:

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
python3 scripts/task_tick_all.py
```

## Prepare a clean ClawHub bundle

```bash
python3 scripts/prepare_publish.py
```

That builds a curated publish folder at:

```text
./dist/durable-task-runner
```

Publish from that folder, not from the full development repo root.
The curated bundle intentionally excludes development-history docs and runtime task state.

## Install locally for OpenClaw

```bash
./install.sh --link
```

Or make a copied install:

```bash
./install.sh --copy
```

## Security / operational notes

This skill is intentionally stateful.

What it does locally:
- writes task snapshots, event logs, and progress logs under `state/tasks/`
- may print or install a recurring cron entry if you run `scripts/task_install_tick_cron.sh --apply`
- can emit live updates through OpenClaw when a task uses delivery method `openclaw`
- can coordinate subagent worker lanes through the `task_subagent_*` helpers

What it does **not** do by itself:
- it does not ask for API keys directly
- it does not require external Python packages
- it does not need network access for local-only reporting modes like `stdout`, `noop`, or `log-only`

Practical caution:
- do not use plaintext task state for secrets unless you control and secure the underlying storage appropriately
- review cron usage before enabling recurring ticks on a real machine
- review subagent flows if you plan to use worker lanes in higher-trust environments

## Reporting operation

For actual recurring task updates, run:

```bash
python3 scripts/task_tick_all.py
```

That is the operational runner that scans all running tasks with delivery bindings and sends due status messages.
Immediate breadcrumbs are emitted automatically on meaningful task transitions when a task has a delivery binding.
If a task is still marked `running` but has no executable continuation hook, the sweep now pauses/reclassifies it instead of emitting endless misleading idle-heartbeat noise.

Delivery bindings now support safer explicit modes:
- `openclaw` — live message delivery through OpenClaw
- `stdout` — print rendered messages only
- `noop` — render but do not deliver
- `log-only` — record send attempts in durable task history without external delivery

Context-pressure guardrails are available via `scripts/task_context_guard.py`:
- below 45%: no action
- at 45%+: write a prepare/checkpoint breadcrumb
- at 50%+: pause the task, queue immediate post-reset resume, and emit a machine-readable handoff payload so the surrounding runtime can reset and continue cleanly

For recurring operation on a real machine, use the helper below to print or install a cron entry:

```bash
scripts/task_install_tick_cron.sh --print
scripts/task_install_tick_cron.sh --apply
```

## ClawHub publish shape

Recommended early-release posture:
- tone: working early release, not fake-1.0 triumphalism
- publish input: `dist/durable-task-runner`
- keep the version/release notes honest to the actual tagged state of the repo

## Provenance

This project was developed with iterative OpenClaw/LLM assistance and critically reviewed during hardening, including Claude review passes. Final code selection, testing, integration, and publication decisions were curated by John Watson.

This project is original glue code and workflow design, but it openly credits the ClawHub skills that influenced parts of the model. See `ATTRIBUTION.md`.
