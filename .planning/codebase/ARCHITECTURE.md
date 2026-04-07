# Architecture

**Analysis Date:** 2026-04-07

## Pattern Overview

**Overall:** Documentation-driven modular skill repository with script-backed execution adapters.

**Key Characteristics:**
- Each capability is packaged as a self-contained module under `skills/<skill-name>/`.
- Primary behavior is instruction-first via `SKILL.md` files, with optional automation scripts.
- Runtime state and evaluation artifacts are persisted as filesystem outputs, not application state.

## Layers

**Repository Interface Layer:**
- Purpose: Define human/agent-facing entry and contribution flow.
- Location: `README.md`, `AGENTS.md`
- Contains: Repository purpose, installation paths, conventions, contribution workflow.
- Depends on: Skill packages under `skills/`.
- Used by: Contributors and agent runtimes selecting skill modules.

**Skill Definition Layer:**
- Purpose: Define trigger conditions and execution workflows for each skill.
- Location: `skills/*/SKILL.md`
- Contains: YAML frontmatter (`name`, `description`), step-by-step procedures, output contracts.
- Depends on: Optional local resources (`assets/`, `references/`, `scripts/`) in each skill folder.
- Used by: Agent skill loader and interactive command sessions.

**Execution Adapter Layer:**
- Purpose: Provide deterministic CLI wrappers for external coding/review agents.
- Location: `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Contains: Argument parsing, workspace/file resolution, session reuse, output path creation, status/progress emission.
- Depends on: External CLIs (`codex`, `opencode`, `jq`) and filesystem runtime paths.
- Used by: Skills such as `skills/codex/SKILL.md`, `skills/plan-execute/SKILL.md`, `skills/plan-review/SKILL.md`.

**Evaluation Layer:**
- Purpose: Benchmark and regression-test skill behavior with/without skill context.
- Location: `skills/*/evals/`, `skills/*/scripts/run_eval.py`, `skills/github-os/evals/run_gemini_eval.py`
- Contains: Eval definitions, provider orchestration, grading logic, timing/token metrics.
- Depends on: Skill definitions, provider CLIs, workspace artifact directories.
- Used by: Skill improvement workflows in `skills/skill-creator/SKILL.md`.

**Planning and Review Layer:**
- Purpose: Store plan inputs and review outputs for iterative plan-review/plan-execute flows.
- Location: `docs/plans/active/`, `reviews/`
- Contains: Active plan files and multi-round review logs.
- Depends on: Skill workflows in `skills/plan-review/SKILL.md` and `skills/plan-execute/SKILL.md`.
- Used by: Human + agent orchestration loops.

**Artifact Workspace Layer:**
- Purpose: Hold generated benchmarking and experiment outputs.
- Location: `skills/*-workspace/`, `plan-review-demo-workspace/`, `.worktrees/`
- Contains: Iteration folders, grading files, benchmark markdown/json/html outputs, experiment clones.
- Depends on: Eval scripts and orchestration tasks.
- Used by: Temporary analysis runs and demonstrations.

## Data Flow

**Skill Invocation Flow:**

1. A user request matches skill metadata in `skills/*/SKILL.md`.
2. The selected `SKILL.md` defines the procedure and optional script/resource usage.
3. If required, wrapper scripts (for example `skills/opencode/scripts/ask_opencode.sh`) invoke external provider CLIs with task + file context.
4. Runtime outputs are written to markdown/status/progress artifacts under `.runtime/` paths.
5. Related planning/review files are read or appended in `docs/plans/active/` and `reviews/`.

**Eval Benchmark Flow:**

1. Eval definitions are read from files such as `skills/github-os/evals/evals.json`.
2. Runner scripts (for example `skills/github-os/evals/run_gemini_eval.py`) execute with-skill and baseline variants.
3. Outputs are written into iteration directories in `skills/github-os-workspace/iteration-*/`.
4. Grading/timing files are generated and consumed by benchmark/report viewers.

**State Management:**
- State is file-based and append-only by convention for reviews/eval outputs.
- No centralized service/database state exists in this repository.

## Key Abstractions

**Skill Package:**
- Purpose: Unit of capability distribution.
- Examples: `skills/github-os/`, `skills/plan-review/`, `skills/skill-creator/`
- Pattern: `SKILL.md` as control plane plus optional `README.md`, `assets/`, `references/`, `scripts/`, `evals/`.

**Provider Adapter Script:**
- Purpose: Normalize CLI calls and session handling across providers.
- Examples: `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Pattern: Validate commands, parse options, assemble prompts, execute provider, persist machine-readable outputs.

**Review/Plan Artifact:**
- Purpose: Contract surface between planning and execution/review loops.
- Examples: `docs/plans/active/2026-04-07-improve-plan-review-token-minimization.md`, `reviews/2026-04-07-improve-plan-review-token-minimization-review.md`
- Pattern: Markdown logs with round-based updates and status semantics.

## Entry Points

**Repository Entry:**
- Location: `README.md`
- Triggers: New contributor setup or skill installation.
- Responsibilities: Explain purpose, active skills, installation methods, and usage examples.

**Agent Collaboration Entry:**
- Location: `AGENTS.md`
- Triggers: Agent-assisted work in this repository.
- Responsibilities: Define architecture assumptions, file conventions, and expected workflows.

**Skill Runtime Entry:**
- Location: `skills/*/SKILL.md`
- Triggers: Agent trigger matching on skill description.
- Responsibilities: Route task execution, choose scripts/resources, define output format.

**Script Execution Entry:**
- Location: `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Triggers: Delegation calls from skill workflows.
- Responsibilities: Execute provider CLI calls and emit session/output paths for follow-up.

**Evaluation Entry:**
- Location: `skills/github-os/evals/run_gemini_eval.py`, `skills/skill-creator/scripts/run_eval.py`
- Triggers: Benchmarks and trigger-testing workflows.
- Responsibilities: Run controlled eval loops and write comparable artifacts.

## Error Handling

**Strategy:** Fail-fast in scripts and explicit review-loop correction in workflow skills.

**Patterns:**
- Shell wrappers use strict mode (`set -euo pipefail`) and required-command checks in `skills/codex/scripts/ask_codex.sh` and `skills/opencode/scripts/ask_opencode.sh`.
- Workflow skills enforce iterative correction via status-driven rounds in `skills/plan-review/SKILL.md` and `skills/plan-execute/SKILL.md`.

## Cross-Cutting Concerns

**Logging:** Runtime/task progress is file-logged (`.runtime/*.md`, `.runtime/*.status`, `.runtime/*.progress`) by adapter scripts and orchestration workflows.
**Validation:** Input/argument validation is handled in shell and Python runners before invoking providers (`skills/opencode/scripts/ask_opencode.sh`, `skills/skill-creator/scripts/run_eval.py`).
**Authentication:** No app-level auth layer in repo code; integrations rely on external CLI/MCP credentials configured in the execution environment (for example, GitHub MCP usage documented in `skills/github-os/SKILL.md`).

---

*Architecture analysis: 2026-04-07*
