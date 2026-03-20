# DECISIONS.md

## 2026-03-20

### Decision: build as a graduated control system
- The runner should scale process/control level based on task complexity instead of forcing one heavyweight workflow on every task.
- Rationale: avoids both under-control on long/risky tasks and over-ceremony on small tasks.

### Decision: default reporting should be low-noise
- Default reporting level is milestone-oriented unless the task/user explicitly warrants more detail.
- If ambiguous, reporting defaults downward.
- Rationale: the user can always ask for more detail; noisy defaults are harder to recover from.

### Decision: main agent is orchestrator, subagents are workers
- The main agent plans, verifies, reports, and controls; subagents execute bounded work slices.
- Rationale: improves continuity, reduces context loss, and better matches long-running project work.

### Decision: keep bulk process memory out of hot context
- `MEMORY.md` should reference the durable-task-runner process memory model, but the bulk should live in a separate reference file and only engage above a configurable threshold.
- Rationale: preserve learning without bloating startup context.

### Decision: align to PMP / Agile / ITIL principles without copying proprietary text
- Use principle-level alignment language only.
- Rationale: gain useful structure and credibility without copyright stupidity.
