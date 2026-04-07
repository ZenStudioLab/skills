# Coding Conventions

**Analysis Date:** 2026-04-07

## Naming Patterns

**Files:**
- Use kebab-case for skill directories under `skills/` (for example `skills/monorepo-worktree-safety`, `skills/extension-testing-expert-skill`) as documented in `AGENTS.md`.
- Use uppercase `SKILL.md` for machine-readable skill definitions (for example `skills/github-os/SKILL.md`).
- Use standard `README.md` for human docs (for example `skills/github-os/README.md`).
- Python script files are snake_case (for example `skills/skill-creator/scripts/run_eval.py`, `skills/skill-creator/scripts/quick_validate.py`).
- TypeScript config/helper filenames are kebab-case when multiword (`dummy-extension-project/playwright.config.ts`, `dummy-extension-project/tests/e2e/extension-helper.ts`).

**Functions:**
- Use snake_case for Python functions (`parse_json_tail`, `run_gemini`, `split_eval_set` in `skills/github-os/evals/run_gemini_eval.py` and `skills/skill-creator/scripts/run_loop.py`).
- Use camelCase for TypeScript functions (`dismissWelcomeBanner` in `skills/extension-testing-expert-skill/assets/boilerplate/extension-helper.ts`).

**Variables:**
- Use UPPER_SNAKE_CASE for module-level constants in Python (`ROOT`, `EVALS_PATH`, `WORKSPACE`, `GEMINI` in `skills/monorepo-worktree-safety/evals/run_gemini_eval.py`).
- Use UPPER_SNAKE_CASE for immutable TypeScript config constants (`EXTENSION_PATH` in `dummy-extension-project/playwright.config.ts`).
- Use descriptive local names over abbreviations in scripts (`train_set`, `test_set`, `trigger_threshold` in `skills/skill-creator/scripts/run_loop.py`).

**Types:**
- Use Python type hints for new scripts (examples in `skills/skill-creator/scripts/run_eval.py`, `skills/skill-creator/scripts/utils.py`).
- Use explicit TypeScript type imports for Playwright helpers (`type BrowserContext`, `type Page` in `skills/extension-testing-expert-skill/assets/boilerplate/extension-helper.ts`).

## Code Style

**Formatting:**
- No repository-wide formatter config detected (`.prettierrc*`, `pyproject.toml`, `ruff.toml`, `.editorconfig` not detected at repo root).
- Keep style aligned with existing files:
- Python: 4-space indent, docstrings for modules/functions (`skills/skill-creator/scripts/improve_description.py`).
- TypeScript: semicolon-terminated statements, single-quoted strings, trailing commas in multiline literals (`dummy-extension-project/playwright.config.ts`).

**Linting:**
- No lint config detected (`eslint.config.*`, `.eslintrc*`, `mypy.ini`, `setup.cfg` not detected at root).
- Treat `skills/skill-creator/scripts/quick_validate.py` as the practical quality gate for skill metadata validity.

## Import Organization

**Order:**
1. Standard library imports first in Python (`json`, `os`, `subprocess`, `time` in `skills/github-os/evals/run_gemini_eval.py`).
2. Third-party imports next (`yaml` in `skills/skill-creator/scripts/quick_validate.py`, `@playwright/test` in TypeScript helpers).
3. Local module imports last (`from scripts.utils import parse_skill_md` in `skills/skill-creator/scripts/run_eval.py`).

**Path Aliases:**
- Not detected. Use relative/absolute filesystem imports only (for example `from scripts.generate_report import generate_html` in `skills/skill-creator/scripts/run_loop.py`).

## Error Handling

**Patterns:**
- Fail fast with explicit exceptions for malformed core data (`ValueError` in `skills/skill-creator/scripts/utils.py` when frontmatter is missing).
- Wrap external process calls and raise actionable runtime errors (`RuntimeError` with stdout/stderr context in `skills/github-os/evals/run_gemini_eval.py`).
- Use graceful fallback parsing for semi-structured output (JSON tail scanning in `parse_json_tail` within `skills/monorepo-worktree-safety/evals/run_gemini_eval.py`).
- For validation scripts, return `(bool, message)` instead of throwing for expected user errors (`validate_skill` in `skills/skill-creator/scripts/quick_validate.py`).

## Logging

**Framework:** console/stdio logging (`print` in Python, `console.log` in TypeScript).

**Patterns:**
- Use progress logs for long-running eval loops (`print(f"run eval-{eval_id} {config}")` in `skills/github-os/evals/run_gemini_eval.py`).
- Emit warnings for partial failures but continue aggregation where safe (`Warning: Invalid JSON...` in `skills/skill-creator/scripts/aggregate_benchmark.py`).
- Log runtime browser diagnostics in Playwright helpers (`page.on('console', ...)` in `dummy-extension-project/tests/e2e/extension-helper.ts`).

## Comments

**When to Comment:**
- Add comments for workflow constraints or non-obvious runtime behavior:
- Workspace/worktree safety rationale in `skills/monorepo-worktree-safety/SKILL.md`.
- Extension-specific E2E constraints in `skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`.

**JSDoc/TSDoc:**
- Use brief block comments above exported helpers/major setup blocks (`Extension E2E Setup Helper` in `skills/extension-testing-expert-skill/assets/boilerplate/extension-helper.ts`).
- Use Python docstrings for module purpose and function behavior (`skills/skill-creator/scripts/run_eval.py`).

## Function Design

**Size:** 
- Keep parsing and utility functions focused and reusable (`calculate_stats` in `skills/skill-creator/scripts/aggregate_benchmark.py`).
- Keep orchestration in dedicated `main()`/loop functions (`main` in `skills/github-os/evals/run_gemini_eval.py`, `run_loop` in `skills/skill-creator/scripts/run_loop.py`).

**Parameters:**
- Prefer explicit parameters over hidden globals in reusable functions (`run_eval(..., provider, trigger_threshold, runs_per_query)` in `skills/skill-creator/scripts/run_eval.py`).
- Include sensible defaults for CLI-facing optional behavior (`provider: str = DEFAULT_PROVIDER` across skill-creator scripts).

**Return Values:**
- Return structured dictionaries for machine consumption (`run_eval`/`generate_benchmark` outputs in `skills/skill-creator/scripts/run_eval.py` and `skills/skill-creator/scripts/aggregate_benchmark.py`).
- Return typed tuples for compact utility APIs (`parse_skill_md` in `skills/skill-creator/scripts/utils.py`).

## Module Design

**Exports:**
- Python modules expose function APIs and provide CLI entrypoints guarded by `if __name__ == "__main__":` (for example `skills/skill-creator/scripts/quick_validate.py`).
- TypeScript test helpers export `test`, `expect`, and utility helpers from one file (`dummy-extension-project/tests/e2e/extension-helper.ts`).

**Barrel Files:** 
- Not used. Import from concrete modules directly (for example `from scripts.improve_description import improve_description` in `skills/skill-creator/scripts/run_loop.py`).

---

*Convention analysis: 2026-04-07*
