# BACKLOG.md

Status legend: `todo` | `doing` | `blocked` | `done`

## In progress

- [doing] Bootstrap project artifacts so the runner can manage its own build
- [doing] Add configurable defaults and reporting/memory thresholds
- [doing] Keep explicit attribution/provenance for borrowed concepts

## Next up

- [done] Add timed status reporting every 5 minutes regardless of milestone, optimized for minimal-token / maximum-information output (progress-bar style if practical)
- [done] Add heartbeat/progress helper with reporting levels
- [todo] Extend task reporter to show both current task progress and full project status as separate progress bars
- [doing] Add subagent dispatch/controller helper
- [doing] Tighten dropped-line checks and worker-result handling without bloating the controller
- [doing] Connect thin controller helper to real subagent runs
- [doing] Add resume bootstrap helper for running tasks after reset
- [todo] Add bootstrap-driven resume recommendations for concrete controller actions
- [done] Define task complexity levels (0..N) and artifact-selection rules
- [done] Add STATUS.md format and live project status updates
- [done] Add DECISIONS.md for architectural/process choices
- [done] Add memory reference file and MEMORY.md pointer rule

## Later

- [todo] Add tests or repeatable smoke scripts for core helpers
- [todo] Dogfood the runner on a separate real-world long task
- [todo] Mirror to GitHub after working prototype is proven

## Notes

This file is intentionally editable mid-flow.
New work discovered during execution can be added here without pretending the original plan was complete.
