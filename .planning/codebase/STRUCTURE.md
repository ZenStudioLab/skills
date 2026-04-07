# Codebase Structure

**Analysis Date:** 2026-04-07

## Directory Layout

```text
skills/
├── skills/                    # Canonical skill packages (source of truth)
├── docs/                      # Active planning artifacts used by skill workflows
├── reviews/                   # Review round outputs for plan-review/plan-execute flows
├── claude-gpt-workflow/       # Embedded reference workflow package (includes its own .git)
├── plan-review-demo-workspace/# Demo benchmark/eval outputs
├── .planning/codebase/        # Generated mapper documentation
├── .worktrees/                # Local worktree checkouts and experiments
└── AGENTS.md                  # Agent collaboration and project conventions
```

## Directory Purposes

**`skills/`:**
- Purpose: Main module root for all reusable skills.
- Contains: One folder per skill (`SKILL.md`, optional `README.md`, plus optional `assets/`, `references/`, `scripts/`, `evals/`).
- Key files: `skills/plan-review/SKILL.md`, `skills/plan-execute/SKILL.md`, `skills/github-os/SKILL.md`, `skills/skill-creator/SKILL.md`.

**`docs/plans/active/`:**
- Purpose: Track current in-flight plans used by orchestration skills.
- Contains: Date-prefixed plan markdown files.
- Key files: `docs/plans/active/2026-04-07-improve-plan-review-token-minimization.md`.

**`reviews/`:**
- Purpose: Persist review rounds and verdict history.
- Contains: `*-review.md` files appended over iterations.
- Key files: `reviews/2026-04-07-improve-plan-review-token-minimization-review.md`.

**`skills/*-workspace/` and `plan-review-demo-workspace/`:**
- Purpose: Evaluation artifacts and iteration outputs (benchmarking/debugging context).
- Contains: `iteration-*`, `eval-*`, `grading.json`, `benchmark.md`, generated viewer files.
- Key files: `skills/github-os-workspace/iteration-3/benchmark.md`, `plan-review-demo-workspace/iteration-1/benchmark.json`.

**`claude-gpt-workflow/`:**
- Purpose: Embedded upstream/reference workflow package.
- Contains: Skill definitions and scripts similar to root `skills/` with an internal `.git`.
- Key files: `claude-gpt-workflow/codex/SKILL.md`, `claude-gpt-workflow/plan-review/SKILL.md`.

## Key File Locations

**Entry Points:**
- `README.md`: Repository usage and installation entrypoint.
- `AGENTS.md`: Agent rules and architecture summary.
- `skills/*/SKILL.md`: Per-skill runtime entrypoints.

**Configuration:**
- `.gitignore`: Repository ignore rules.
- `skills/*/evals/evals.json`: Eval configuration for benchmark runs.

**Core Logic:**
- `skills/codex/scripts/ask_codex.sh`: Codex adapter shell wrapper.
- `skills/opencode/scripts/ask_opencode.sh`: OpenCode adapter shell wrapper.
- `skills/github-os/evals/run_gemini_eval.py`: Provider-run benchmark driver.
- `skills/skill-creator/scripts/run_eval.py`: Multi-provider trigger eval runner.

**Testing:**
- `skills/*/evals/`: Eval case definitions and runners.
- `skills/*-workspace/iteration-*/eval-*/`: Generated evaluation outputs and grading.
- `dummy-extension-project/tests/e2e/`: Minimal E2E sample test area.

## Naming Conventions

**Files:**
- Skill definition: `SKILL.md`.
- Skill documentation: `README.md`.
- Eval configs: `evals.json`.
- Review logs: `*-review.md`.
- Script wrappers: verb-prefixed snake/kebab shell names (for example `ask_codex.sh`, `ask_opencode.sh`).

**Directories:**
- Skill packages: kebab-case (for example `skills/lesson-decision-records/`, `skills/repo-to-notion-architect/`).
- Workspace outputs: `<skill>-workspace` with `iteration-N/eval-N` nesting.

## Where to Add New Code

**New Feature:**
- Primary code: Add a new module at `skills/<new-skill-name>/`.
- Tests: Add eval definitions to `skills/<new-skill-name>/evals/evals.json` and any runners under `skills/<new-skill-name>/evals/` or `skills/<new-skill-name>/scripts/`.

**New Component/Module:**
- Implementation: Place behavior spec in `skills/<new-skill-name>/SKILL.md`.
- Optional docs/resources: Add `skills/<new-skill-name>/README.md`, `skills/<new-skill-name>/references/`, `skills/<new-skill-name>/assets/`.

**Utilities:**
- Shared helpers: Keep them local to the owning skill (`skills/<skill>/scripts/`); this repository currently favors per-skill encapsulation over a global utility package.

## Special Directories

**`.planning/codebase/`:**
- Purpose: Generated mapper docs consumed by other GSD commands.
- Generated: Yes.
- Committed: Yes.

**`skills/*-workspace/`:**
- Purpose: Eval iteration artifacts and benchmarks.
- Generated: Yes.
- Committed: Yes (currently tracked in this repository).

**`.worktrees/`:**
- Purpose: Local worktree checkouts for parallel changes.
- Generated: Yes.
- Committed: No (local environment artifact pattern).

**`.ruff_cache/`:**
- Purpose: Python tool cache.
- Generated: Yes.
- Committed: No.

---

*Structure analysis: 2026-04-07*
