# BACKLOG.md

Status legend: `todo` | `doing` | `blocked` | `done`

## Verified complete

- [done] Bootstrap project artifacts so the runner can manage its own build
- [done] Add configurable defaults and reporting/memory thresholds
- [done] Keep explicit attribution/provenance for borrowed concepts
- [done] Add timed status reporting every 5 minutes regardless of milestone, optimized for minimal-token / maximum-information output (progress-bar style if practical)
- [done] Add heartbeat/progress helper with reporting levels
- [done] Extend task reporter to show both current task progress and full project status as separate progress bars
- [done] Add subagent dispatch/controller helper
- [done] Tighten dropped-line checks and worker-result handling without bloating the controller
- [done] Connect thin controller helper to real subagent runs
- [done] Add resume bootstrap helper for running tasks after reset
- [done] Add bootstrap-driven resume recommendations for concrete controller actions
- [done] Add controller-ready resume plans from bootstrap output
- [done] Add low-risk controller resume-apply path from bootstrap output
- [done] Validate resume/apply flow on a non-bootstrap durable task
- [done] Add repeatable smoke script for validation task creation/bootstrap/apply
- [done] Define task complexity levels (0..N) and artifact-selection rules
- [done] Add STATUS.md format and live project status updates
- [done] Add DECISIONS.md for architectural/process choices
- [done] Add memory reference file and MEMORY.md pointer rule

## Remaining work

- [done] Add tests or more repeatable smoke coverage for core helpers where real usage shows value
- [done] Dogfood the runner on a separate real-world long task
- [done] Make the repo GitHub-ready and clearly installable as a skill package

## Notes

This file is intentionally editable mid-flow.
New work discovered during execution can be added here without pretending the original plan was complete.

## Release hardening follow-through

- [done] Tighten the public skill body for ClawHub-style consumption
- [done] Add a concrete quickstart reference for repeated use
- [done] Add a deterministic clean-bundle export path for publishing
- [done] Verify the clean publish bundle in isolation, not just from the dev repo
- [done] Add explicit license/provenance/runtime notes for public preview readiness

## Post-0.1.0 / 0.1.1 candidate

- [done] Add explicit safe delivery modes (`stdout`, `noop`, `log-only`) alongside live OpenClaw delivery
- [done] Add targeted delivery-path smoke coverage, including immediate-send behavior and no-binding/no-loop checks
- [done] Add a concrete scheduler/setup helper for recurring `task_tick_all.py` operation

## Deferred beyond 0.1.1

- [todo] Auto-bind new durable tasks in the active chat/session so progress delivery works without manual delivery-binding setup
- [todo] Make recurring tick execution ambient by default in suitable environments instead of requiring the operator to remember cron/timer setup
- [todo] Add a richer real-world example project/reference walkthrough for new adopters
- [todo] Expand reporting-mode docs and operator guidance once real usage shows which knobs are actually confusing
- [todo] Reassess progress-bar math after more real-world use and tighten the metric so it stays grounded in explicit state rather than vague operator feel
- [todo] Consider weighted milestones / better roll-up rules only if that improves signal without turning reporting into workflow theater
- [todo] Consider broader controller/subagent ergonomics only after more real-world use justifies the extra surface area
