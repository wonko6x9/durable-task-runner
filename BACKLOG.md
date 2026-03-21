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
