# RELEASE.md

GitHub-ready release checklist for `durable-task-runner`.

## Definition of done

- skill folder is self-contained
- `SKILL.md` is present at repo root
- install path is documented
- `install.sh` can copy or link the skill into an OpenClaw workspace
- repeatable smoke coverage passes
- repo does not depend on committed runtime state to function

## Local verification

From the repo root:

```bash
python3 scripts/task_core_smoke.py
python3 scripts/task_validation_smoke.py
./install.sh --copy --target /tmp/durable-task-runner
```

Optional workspace install:

```bash
./install.sh --link
openclaw skills list | grep durable-task-runner
```

## Upload to GitHub

1. Ensure the repo is clean:
   ```bash
   git status
   ```
2. Push to the desired GitHub remote.
3. After clone on another machine, install with either:
   - `./install.sh --link`
   - `./install.sh --copy`

## Notes

- `state/tasks/` runtime files are treated as generated state, not required package contents.
- The install script excludes runtime task logs/state when using `--copy`.
