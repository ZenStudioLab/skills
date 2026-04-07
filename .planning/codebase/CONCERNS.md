# Codebase Concerns

**Analysis Date:** 2026-04-07

## Tech Debt

**Mixed production content and evaluation artifacts in one repository:**
- Issue: Operational skills, benchmarks, and experimental workspaces are co-located, which increases navigation and review noise.
- Files: `skills/`, `evals/evals.json`, `docs/plans/active/2026-03-09-lesson-mechanics-design.md`, `reviews/`
- Impact: Routine maintenance and PR review are slower; contributors can miss changes in important skill definitions.
- Fix approach: Separate production skill assets (`skills/*`) from evaluation output and review artifacts into clearly isolated top-level areas (or a separate repo) and enforce path-based ownership rules.

**Inconsistent testing footprint across skills:**
- Issue: Most skills are markdown/process-only without executable validation, while only select areas include runnable test scaffolding.
- Files: `skills/*/SKILL.md`, `skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`, `dummy-extension-project/playwright.config.ts`
- Impact: Regressions in skill behavior are likely to be discovered late (manual usage only).
- Fix approach: Define a minimal validation contract per skill (lint + trigger smoke test + schema check) and run it uniformly.

## Known Bugs

**Claude stream parsing state is not preserved across events in evaluator:**
- Symptoms: False negatives/positives during trigger detection for Claude stream-json mode.
- Files: `skills/skill-creator/scripts/run_eval.py`
- Trigger: `_parse_claude_output(...)` mutates `pending_tool_name`/`accumulated_json` locally, but caller state in `_execute_and_parse(...)` is never updated.
- Workaround: Prefer non-Claude providers for eval runs or verify with repeated runs/manual inspection.

## Security Considerations

**Token setup examples can promote unsafe copy-paste workflows:**
- Risk: Users may paste real tokens directly into config snippets if not guarded by stronger warnings.
- Files: `skills/github-os/assets/github-mcp-setup.md`
- Current mitigation: Uses placeholder values (`your_github_token_here`, `${GITHUB_TOKEN}`) instead of real secrets.
- Recommendations: Add explicit “never commit tokens” warning block and a validation checklist that requires env-only secret handling.

## Performance Bottlenecks

**Very large generated artifacts degrade local search/indexing performance:**
- Problem: Large JSON/markdown eval outputs dominate filesystem scans and token-heavy operations.
- Files: `skills/github-os-workspace/iteration-1/eval-1/without_skill/run-1/raw_response.json`, `skills/github-os-workspace/iteration-2/eval-1/with_skill/run-1/raw_response.json`, `skills/github-os-workspace/iteration-1/eval-1/with_skill/run-1/outputs/output.md`
- Cause: Benchmark/eval runs persist full raw outputs in workspace trees.
- Improvement path: Keep only summarized metrics in-repo and move full raw outputs to ignored artifact storage.

## Fragile Areas

**CLI wrapper scripts rely on shell command-string execution and environment assumptions:**
- Files: `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Why fragile: Runtime behavior depends on local CLI availability (`codex`, `opencode`, `jq`) and PTY semantics (`script`), which vary across environments.
- Safe modification: Add explicit platform tests and a `--dry-run` mode; keep argument parsing changes backward-compatible.
- Test coverage: No repository-level automated test files validate these wrappers directly.

## Scaling Limits

**Parallel evaluator defaults can exhaust local resources at scale:**
- Current capacity: Default `--num-workers 10` and `--runs-per-query 3`.
- Limit: On larger eval sets, process spawning and provider CLI calls may saturate CPU and IO.
- Scaling path: Add adaptive worker caps by CPU count and batch sizing in `skills/skill-creator/scripts/run_eval.py`.

## Dependencies at Risk

**External CLI dependency chain is broad and optionality is runtime-only:**
- Risk: Provider CLIs may not exist locally or may change JSON output format.
- Impact: Eval reliability and automation portability degrade.
- Migration plan: Introduce provider capability checks in CI and stable parser contract tests.

## Missing Critical Features

**No standardized CI workflow for skill validation detected:**
- Problem: No `.github/workflows/*` pipeline found for lint/test/validation enforcement.
- Blocks: Consistent quality gates for skill changes and script updates.

## Test Coverage Gaps

**Core Python evaluator and shell wrappers are effectively untested in this repository:**
- What's not tested: Parsing correctness and fallback behavior in `skills/skill-creator/scripts/run_eval.py`; argument/path handling in `skills/codex/scripts/ask_codex.sh` and `skills/opencode/scripts/ask_opencode.sh`.
- Files: `skills/skill-creator/scripts/run_eval.py`, `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Risk: Silent behavior regressions in automation and inaccurate evaluation results.
- Priority: High

---

*Concerns audit: 2026-04-07*
