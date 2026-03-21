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

### Decision: tolerate noisy CLI wrappers at integration boundaries
- Treat helper/CLI output as potentially mixed-content when shelling out to OpenClaw commands, even when `--json` is requested.
- Parse the JSON payload defensively instead of assuming stdout is clean.
- Rationale: config/runtime warnings and transport notes can legitimately surround the payload; brittle parsers make the durable runner less durable.

### Decision: subagent orchestration starts with a thin controller, not a workflow cathedral
- First implementation should only assign a line, generate a worker brief, ingest a structured return, and detect dropped lines.
- Do not add scheduling boards, giant state machines, or rich branch choreography until a real task proves they are needed.
- Rationale: the user wants simple UX and a robust backend, not ceremonial complexity.

### Decision: anti-drop checks must distinguish attention from failure
- Not every unfinished line is dropped; some lines are merely waiting for controller action.
- Track at least four controller-facing states: `active`, `attention`, `resolved`, and `dropped`.
- Require an explicit controller decision after `autopilot` or `handoff` returns instead of assuming the next move happened.
- Rationale: a binary good/bad check is too dumb to be operationally trustworthy.

### Decision: resume/bootstrap should recommend, not just classify
- A restart helper that only labels tasks is informative but incomplete.
- The bootstrap path should emit a concrete next action (`resume_active_line`, `controller_decision_needed`, `reconcile_first`, etc.) so the operator/controller knows what to do next.
- Rationale: on restart, the system should reduce ambiguity, not just summarize it.

### Decision: resume/bootstrap should emit a small action plan, not a giant workflow engine
- After classification/recommendation, emit a short ordered plan (`steps[]`) that a controller can follow directly.
- Keep the plan shallow and declarative; do not build a giant restart state machine unless real failures prove it is necessary.
- Rationale: this creates an execution bridge without birthing a bureaucracy.

### Decision: bootstrap should apply obvious low-risk resume actions automatically
- If restart analysis says the task is cleanly resumable, the controller should be able to apply the low-risk follow-through immediately instead of reporting and stalling.
- Keep the auto-apply surface narrow: resumable main flow / resumable active line first; then straightforward `controller_decision_needed` cases where the next role is already explicit and low-risk.
- Leave ambiguous or higher-risk cases as controller/operator decisions.
- Rationale: the whole point of a durable runner is to keep moving unless there is a good reason not to.
