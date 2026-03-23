# Changelog

## v0.1.3 (planned)

Release focus:
- make the ClawHub bundle smaller, clearer, and easier to trust at a glance
- remove development-only smoke scripts from the public bundle
- add explicit security / operational notes to public docs
- keep the source repo useful for development while making the published skill more reviewable

Expected notes:
- smoke-test scripts remain in the source repo but are excluded from the publish bundle
- public docs explain plaintext task state, cron installation, delivery modes, and subagent control surface more directly
- ClawHub-facing package is more intentional about what end users actually need to install/use

## v0.1.2

Release focus:
- refresh release hygiene and project status so docs match the real repo state
- carry forward the post-0.1.1 candidate work already completed in the repo
- make the next publish/tag step honest and easier to reason about

Expected notes:
- explicit release-discipline backlog follow-through
- refreshed `STATUS.md` for current version reality
- concise release-history tracking so users do not need to infer version meaning from commit logs alone

## v0.1.1

- publication-pass improvements after the initial public preview lane
- safer / clearer publish-readiness and packaging follow-through
- scheduler/setup helper and delivery-path hardening for recurring reporting flow
- safe delivery modes (`stdout`, `noop`, `log-only`) and related smoke coverage

## v0.1.0

- first public preview / initial publishable release posture
- durable task state model, task control helper, progress reporting, resume bootstrap, and packaging baseline
