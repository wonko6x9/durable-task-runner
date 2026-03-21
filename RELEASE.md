# RELEASE.md

Release checklist for the development repo.

## Goal

Keep the repository useful for development while emitting a cleaner public-skill bundle for ClawHub.

## Verification

Run from repo root:

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
python3 scripts/task_delivery_smoke.py
python3 scripts/task_tick_all.py
python3 scripts/prepare_publish.py
```

## Publish flow

1. Build the clean bundle:
   ```bash
   python3 scripts/prepare_publish.py
   ```
2. Review the output folder:
   ```bash
   find dist/durable-task-runner -maxdepth 3 -type f | sort
   ```
3. Publish from the clean bundle, not from the repo root:
   ```bash
   clawhub publish dist/durable-task-runner \
     --slug durable-task-runner \
     --name "Durable Task Runner" \
     --version 0.1.0 \
     --changelog "Initial public release: durable task state, resume/apply flow, reporting, verification, and thin subagent orchestration."
   ```

## Notes

- The full repo intentionally contains dogfooding/project-history files that are not part of the preferred ClawHub publish surface.
- `scripts/prepare_publish.py` is the canonical way to build the publishable bundle.
- The publish bundle intentionally excludes runtime task state (`state/tasks/`) and other generated/local-history artifacts.
- The Python scripts are stdlib-only; no external Python dependencies are required.
- ClawHub auth is still a separate prerequisite (`clawhub login`).
