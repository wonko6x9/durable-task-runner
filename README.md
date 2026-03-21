# durable-task-runner

Durable task orchestration for OpenClaw.

This repo is the development/workbench version of the skill. It includes dogfooding artifacts, project-history docs, and helper scripts used to build and test the public skill.

## What it does

- persists task state to disk instead of relying on chat memory
- tracks milestones, progress, events, and verification
- survives resets with resume/bootstrap helpers
- supports pause / stop / steer controls
- supports thin controller/worker subagent orchestration
- renders compact status output for longer-running work

## Process model

Durable Task Runner uses a hybrid process model that pulls from the most useful parts of PMP, Agile, structured sequencing where dependencies justify it, and ITIL-style operational discipline.

The goal is not to bury users in process. The goal is to strengthen the backend framework enough that long work actually finishes, keeps moving across resets/interruption, and stays visible while it is in flight.

In practice, the runner:
- scales the amount of process and artifact depth to the size/risk of the task
- asks the user for a few key blanks when needed, then drives the rest through durable state and helper scripts
- uses planning, checkpoints, verification, and resume logic to keep projects moving toward completion
- treats robustness and continued real-world testing as ongoing goals of the framework itself

The current priority is practical rather than grandiose: get projects to finish reliably. Industry-standard process ideas are used because they provide a stronger architecture for that than ad-hoc chat memory alone.

## Visibility and progress

Visible progress is a core feature, not cosmetic fluff.

Task and project progress bars, milestone updates, and timed status messages exist to answer the most important operational question during long work: did the task die, or is it still moving?

By default, reporting stays low-noise and milestone-oriented. It can also be configured for more regular timed updates, higher-visibility operational reporting, or quieter completion-focused behavior when that better fits the job.

## Repository layout

### Public skill surface
These are the files that matter for the published skill:
- `SKILL.md`
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

## Local development checks

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
python3 scripts/task_tick_all.py
```

What they validate:
- `task_validation_smoke.py` — restart/bootstrap/apply flow on a throwaway non-bootstrap durable task
- `task_core_smoke.py` — create/update/report/ticker/subagent/restart helper coverage
- `task_tick_all.py` — recurring due-scan behavior across running tasks with delivery bindings

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

## Reporting operation

For actual recurring task updates, run:

```bash
python3 scripts/task_tick_all.py
```

That is the operational runner that scans all running tasks with delivery bindings and sends due status messages.
Immediate breadcrumbs are emitted automatically on meaningful task transitions when a task has a delivery binding.

Delivery bindings now support safer explicit modes:
- `openclaw` — live message delivery through OpenClaw
- `stdout` — print rendered messages only
- `noop` — render but do not deliver
- `log-only` — record send attempts in durable task history without external delivery

For recurring operation on a real machine, use the helper below to print or install a cron entry:

```bash
scripts/task_install_tick_cron.sh --print
scripts/task_install_tick_cron.sh --apply
```

## ClawHub publish shape

Recommended first public release posture:
- version: `0.1.0`
- tone: working early release, not fake-1.0 triumphalism
- publish input: `dist/durable-task-runner`

## Provenance

This project was developed with iterative OpenClaw/LLM assistance and critically reviewed during hardening, including Claude review passes. Final code selection, testing, integration, and publication decisions were curated by John Watson.

This project is original glue code and workflow design, but it openly credits the ClawHub skills that influenced parts of the model. See `ATTRIBUTION.md`.
