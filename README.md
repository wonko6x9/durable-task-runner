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

## Repository layout

### Public skill surface
These are the files that matter for the published skill:
- `SKILL.md`
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

## Local development checks

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
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

## Install locally for OpenClaw

```bash
./install.sh --link
```

Or make a copied install:

```bash
./install.sh --copy
```

## ClawHub publish shape

Recommended first public release posture:
- version: `0.1.0`
- tone: working early release, not fake-1.0 triumphalism
- publish input: `dist/durable-task-runner`

## Provenance

This project is original glue code and workflow design, but it openly credits the ClawHub skills that influenced parts of the model. See `ATTRIBUTION.md`.
