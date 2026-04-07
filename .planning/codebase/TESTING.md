# Testing Patterns

**Analysis Date:** 2026-04-07

## Test Framework

**Runner:**
- Primary automated testing is custom Python eval harnesses, not pytest/jest/vitest:
- `skills/github-os/evals/run_gemini_eval.py`
- `skills/monorepo-worktree-safety/evals/run_gemini_eval.py`
- Skill trigger regression harness in `skills/skill-creator/scripts/run_eval.py` and `skills/skill-creator/scripts/run_loop.py`.
- Playwright is used for browser-extension E2E templates:
- `dummy-extension-project/playwright.config.ts`
- `skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`
- Config: No root-level `pytest.ini`, `vitest.config.*`, or `jest.config.*` detected.

**Assertion Library:**
- Rule-based assertion matching in Python (`grade(...)` functions in `skills/github-os/evals/run_gemini_eval.py` and `skills/monorepo-worktree-safety/evals/run_gemini_eval.py`).
- Playwright assertions through exported `expect` fixture (`dummy-extension-project/tests/e2e/extension-helper.ts`).

**Run Commands:**
```bash
python3 skills/github-os/evals/run_gemini_eval.py              # Run github-os evals
python3 skills/monorepo-worktree-safety/evals/run_gemini_eval.py  # Run monorepo-worktree-safety evals
python3 -m scripts.run_eval --help                             # Inspect skill-creator eval CLI
xvfb-run -a yarn playwright test                               # Extension E2E command documented in skill README
```

## Test File Organization

**Location:**
- Eval definitions are stored as JSON in skill-specific directories:
- `skills/github-os/evals/evals.json`
- `skills/monorepo-worktree-safety/evals/evals.json`
- `skills/skill-creator/evals/skill-creator-test.json`
- Generated run artifacts are stored under workspace iteration directories:
- `skills/github-os-workspace/iteration-*/eval-*/...`
- `skills/monorepo-worktree-workspace/iteration-*/eval-*/...`

**Naming:**
- Eval case directories follow `eval-<id>`.
- Run directories follow `run-<n>`.
- Output files are consistently named `output.md`, `grading.json`, `timing.json`, `raw_response.json`, `eval_metadata.json`.

**Structure:**
```
skills/<skill>/evals/
skills/<skill>-workspace/iteration-<n>/eval-<id>/<with_skill|without_skill>/run-1/
dummy-extension-project/tests/e2e/
```

## Test Structure

**Suite Organization:**
```typescript
// Fixture-first E2E setup pattern
export const test = base.extend<{ context: BrowserContext; extensionId: string; optionsPage: Page; }>({
  context: async ({}, use, testInfo) => { /* launch persistent context */ },
  extensionId: async ({ context }, use) => { /* resolve extension ID + clear storage */ },
  optionsPage: async ({ context, extensionId }, use) => { /* open page + dismiss onboarding */ },
});
```

**Patterns:**
- Setup pattern: prepare deterministic environment before each run (clear extension storage in `dummy-extension-project/tests/e2e/extension-helper.ts`).
- Teardown pattern: close context/page via fixture lifecycle (`await context.close()`, `await page.close()`).
- Assertion pattern: evaluate output text against expected keywords/regex in `grade()` checks within `skills/*/evals/run_gemini_eval.py`.

## Mocking

**Framework:** 
- No dedicated mocking framework (for example `unittest.mock`, pytest monkeypatch, jest/vitest mocks) detected in executable tests.

**Patterns:**
```python
# Behavioral testing uses real subprocess calls, then validates output shape/content.
proc = subprocess.run([...], capture_output=True, timeout=timeout_sec)
payload = parse_json_tail(proc.stdout)
expectations = grade(eval_id, assertions, payload.get("response", ""))
```

**What to Mock:**
- For future Python unit tests, mock provider subprocess boundaries (`subprocess.run` in `skills/*/evals/run_gemini_eval.py`) to make tests deterministic and offline-safe.

**What NOT to Mock:**
- Do not mock grading logic itself (`grade`, `evidence_snippet`) when validating regression behavior; those functions are the contract being verified.

## Fixtures and Factories

**Test Data:**
```json
{
  "id": 1,
  "prompt": "...",
  "assertions": ["...", "..."]
}
```

**Location:**
- Eval prompt/expectation fixtures: `skills/github-os/evals/evals.json`, `skills/monorepo-worktree-safety/evals/evals.json`.
- Playwright runtime fixtures: `dummy-extension-project/tests/e2e/extension-helper.ts` and `skills/extension-testing-expert-skill/assets/boilerplate/extension-helper.ts`.

## Coverage

**Requirements:** 
- No enforced coverage tooling detected (`pytest --cov`, nyc, jest/vitest coverage config not detected).
- Coverage thresholds appear only as documentation/examples (for example `>80% coverage` checkboxes in `skills/github-os/assets/examples/sample-llm-ready-issue.md`), not as executable repository gates.

**View Coverage:**
```bash
Not applicable (no repository-level automated coverage command configured)
```

## Test Types

**Unit Tests:**
- Minimal direct unit-test suite detected. Validation is script-driven via targeted CLI checks (`skills/skill-creator/test_provider.sh`, `skills/skill-creator/scripts/quick_validate.py`).

**Integration Tests:**
- Primary pattern: end-to-end command integration of AI provider CLIs + grading pipeline (`skills/skill-creator/scripts/run_eval.py`, `skills/github-os/evals/run_gemini_eval.py`).

**E2E Tests:**
- Playwright extension E2E setup is provided as reusable boilerplate, including persistent context, non-headless requirement, and onboarding dismissal (`skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`, `.../extension-helper.ts`).

## Common Patterns

**Async Testing:**
```typescript
background = await context.waitForEvent('serviceworker', { timeout: 20000 });
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(3000);
```

**Error Testing:**
```python
try:
    return json.loads(candidate)
except json.JSONDecodeError:
    pass
# fallback scan, then raise ValueError if unrecoverable
```

---

*Testing analysis: 2026-04-07*
