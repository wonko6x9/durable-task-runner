# STATUS.md

## Current phase

0.1.3 ClawHub hardening

## Health

healthy

## Current milestone

ClawHub reviewability hardening

## Last checkpoint

- `v0.1.2` is now published and tagged
- ClawHub review text indicates the package is coherent, but the current bundle still exposes more development/testing surface than ideal for first-glance trust
- likely low-risk improvement path identified: remove development-only smoke scripts from the public bundle and explain operational/security behavior more directly in public docs
- release hygiene work from `0.1.2` remains in place (status/changelog/checklist discipline)

## In-progress work

- trim the published surface area to the scripts/files needed for normal install/use
- make README/SKILL docs more explicit about plaintext task state, cron behavior, delivery modes, and subagent control surface
- prepare a cleaner ClawHub-facing `0.1.3`

## Next step

- rebuild the clean bundle without smoke-only scripts
- verify remaining public files are honest and sufficient
- publish/tag `0.1.3`

## Blockers

- none currently confirmed in code/package state
- ClawHub review wording may lag slightly behind package cleanup until the new version is analyzed
