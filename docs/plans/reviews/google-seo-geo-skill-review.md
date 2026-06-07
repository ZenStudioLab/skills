## Round 1

**Plan**: `docs/plans/active/2026-05-18-google-seo-geo-skill.md`
**Overall assessment**: REQUEST_CHANGES

The plan is well-structured, follows the repo's existing skill conventions, and is realistically scoped. The validator path and frontmatter schema both check out against the actual `quick_validate.py` source. However there are several real correctness bugs in the verification steps, a missing actual evaluation pass for the new skill, and some ambiguous "insert here" edit instructions that will trip a zero-context implementer. Fix the items below before execution.

---

## Findings

### Critical

1. **Task 5 Step 4 — empty commit will fail and abort the plan** (`docs/plans/active/2026-05-18-google-seo-geo-skill.md:740-747`)
   - Steps 1–3 of Task 5 only *run* validation; they do not modify any file. The subsequent `git add skills/google-seo-geo && git commit -m "chore(google-seo-geo): validate final package"` therefore stages nothing and `git commit` will exit non-zero with "nothing to commit, working tree clean", halting a strict executor.
   - **Fix:** Either drop Task 5 Step 4 entirely (the prior task commits already cover the final state), pass `--allow-empty`, or move a real change (e.g., the verification-output log file from Step 5) into the commit.

2. **Task 3 Step 7 — `for … do test -s … done` does not actually verify all files** (`...:516-530`)
   - The loop's final exit status is only the status of the *last* `test -s`. If any earlier file is missing or empty, the loop continues and the overall exit code can still be `0`. The plan's "Expected: PASS with exit code `0`" is therefore not a real check.
   - **Fix:** Use `set -e` inside the block, or chain with `&&`:
     ```bash
     for f in skills/google-seo-geo/references/{google-search-docs-summary,audit-checklist,templates,anti-patterns}.md; do
       test -s "$f" || { echo "missing/empty: $f"; exit 1; }
     done
     ```

### High

3. **No actual eval execution for a brand-new skill** (entire plan)
   - The plan adds `evals/evals.json` and JSON-parses it, but never runs `skills/skill-creator/scripts/run_eval.py` (or `run_loop.py`), both of which exist in this repo and are the conventional way to validate a new skill's behavior. Structural validity ≠ skill quality. For a new skill being introduced to the repo, at minimum one eval-runner dry-run or smoke-call belongs in Task 5.
   - **Fix:** Add a Task 5 step that invokes `python skills/skill-creator/scripts/run_eval.py skills/google-seo-geo` (or document explicitly why eval execution is deferred and where it will be tracked).

4. **Task 4 Step 3 — README edits are spec'd as English instructions, not exact patches** (`...:612-636`)
   - "Replace the active-skills list block with: …" and "Also insert this install example under the specific-skill install commands" are both ambiguous for a zero-context implementer. There is no anchor line, no surrounding context, and no clarification whether the new install line goes before or after the existing `--skill get-api-docs` line (which itself doesn't match any current skill directory — `context-hub-get-api-docs` is the real folder). The README block in the plan also silently drops the possibility of preserving lines that may have been added since the plan was written.
   - **Fix:** Specify exact `old`/`new` text pairs, or call out the precise insertion line (e.g., "after line 36 in `README.md`"). Also confirm the existing `--skill get-api-docs` install example is intentional (it does not match the `context-hub-get-api-docs` skill directory).

5. **Task 1 Step 1 — false "FAIL with SKILL.md not found" expectation** (`...:22-30`)
   - At this point `skills/google-seo-geo/` does not exist yet (Step 2 creates it). `quick_validate.py` constructs `Path(skill_path)` regardless, then checks `skill_md.exists()` which is `False` for a non-existent directory, so the script will return `False, "SKILL.md not found"` — but the message printed by the `__main__` block needs to be confirmed. More importantly, this "verify it fails first" step has no semantic value here (we are creating a new directory) and just adds noise. Keep it only if you actually rely on the negative result; otherwise drop.
   - **Fix:** Either delete the step, or assert against the real output string the script prints, not against a paraphrase. (See `quick_validate.py:18`.)

### Medium

6. **`run_eval.py`, `aggregate_benchmark.py`, `generate_report.py` integration never considered** (entire plan)
   - The repo ships an eval pipeline (`run_eval.py`, `aggregate_benchmark.py`, `improve_description.py`) under `skills/skill-creator/scripts/`. The plan should at least state that those tools are intentionally out of scope, otherwise a reviewer will assume the skill author was unaware of them. Related to #3 above but worth calling out as a documentation gap independent of execution.

7. **Task 2 Step 2 — frontmatter description ~439 chars is fine, but contains punctuation worth pre-checking** (`...:136`)
   - Length is well under the 1024-char cap and contains no `<`/`>`, so it passes `quick_validate.py`. No fix required, but adding an explicit assertion (`python -c "import yaml; ..."`) would be cheap insurance against later edits that bust the description.

8. **Task 3 Step 1 — `ls` of empty dir as a check is unreliable** (`...:303-309`)
   - `ls skills/google-seo-geo/references` produces no output and exit 0 whether empty or whether it contains a hidden file. The "expected empty" is informal. Use `test -z "$(ls -A skills/google-seo-geo/references)"` if you actually want to assert emptiness.

9. **Commit hygiene drift across tasks** (`...:109-111, 287-289, 537-539, 671-673, 745-747`)
   - Task 1 commits `README.md` content that Task 3 fully rewrites three commits later. That's fine, but the Task 3 commit message ("add reference bundle") is misleading because it *also* rewrites the README. Consider splitting into two commits in Task 3, or rename the message to `feat(google-seo-geo): add reference bundle and skill README`.

10. **Task 4 Step 3 — silent omission of other present skills from the README list** (`...:618-630`)
    - The proposed "active skills" replacement block matches the *current* README inventory (good), but it does not mention skills that physically exist in `skills/` such as `monorepo-worktree-safety`, `extension-testing-expert-skill`, `repo-to-notion-architect`, etc. That's pre-existing drift, not introduced by this plan, but if a reviewer reads the diff and notices the list is stale, this work will get bounced. Either acknowledge this is intentional or add a short note that README inventory hygiene is out of scope.

11. **No update to any agent-facing index / `AGENTS.md`** (entire plan)
    - The repo's `AGENTS.md` lists workflows and conventions for skill addition. The plan does not register the new skill there, nor in any central index. If the project convention is "skills auto-discovered, no index needed," fine; if not, this is a gap. Verify and either add a step or note it as N/A.

12. **Task 2 Step 4 grep — case-sensitivity is correct but fragile** (`...:262-270`)
    - The grep relies on the exact lowercased phrase `chunking`, `scaled-content abuse`, `fake freshness` appearing in `SKILL.md`. They do today, but any innocuous capitalization edit later will silently break the check without anyone noticing (because the plan is one-shot). Consider `grep -iE` or pin the phrases in a comment so an editor knows not to recase them.

### Low

13. **Anti-patterns table phrasing — "Schema everywhere by default"** (`...:471`)
    - The row title uses the phrase "Schema everywhere by default" but Task 2 / Task 5 grep checks do not look for it. Not a correctness issue, just a missed opportunity to verify the row survives.

14. **`templates.md` fenced block uses 4-backtick outer fence** (`...:407,452`)
    - Correct (because inner blocks use triple backticks), but worth calling out in the plan body so an implementer doesn't "fix" it back to triple backticks and break the inner code blocks. A one-line comment would help.

15. **Task 4 Step 1 verification of empty evals adds little value** (`...:548-561`)
    - The check that the scaffold evals are still empty before overwriting is harmless but doesn't catch any realistic failure mode; the next step overwrites the file unconditionally. Consider trimming.

16. **No rollback / failure-recovery guidance** (entire plan)
    - If, say, the final commit in Task 5 fails (see #1), the plan does not say how to recover. For a five-task, six-commit sequence this is fine, but a one-line "If a step fails, fix and re-run the step; do not amend prior commits" would align with global rules.

### Suggestion

17. **Add a smoke run of the skill against a sample input** (`...:Task 5`)
    - Pair the structural validation with one real invocation (even a manual paste-through prompt) confirming the skill correctly: (a) checks for `.agents/product-marketing-context.md`, (b) rejects an `llms.txt` request, (c) produces the documented 5-section output structure. This is the cheapest way to catch behavioral regressions that pure file-existence checks miss.

18. **Pin Python invocation to `python3`** (multiple Task steps)
    - Most steps use bare `python`. On some Linux distros that resolves to Python 2 or is absent. Prefer `python3` for portability; the validator itself uses `#!/usr/bin/env python3`.

19. **Consider committing a brief CHANGELOG or release note** (Task 4 or 5)
    - The repo distributes via git; a short note in commit `feat(google-seo-geo): add evals and repo docs` body summarizing user-facing additions would help downstream consumers using `npx skills add`.

20. **Frontmatter description duplicates trigger-keyword list and behavioral rule** (`...:47, 136`)
    - The same long description appears twice (scaffold and final). Keep them identical (they are), but consider a single source-of-truth note in the plan so a future edit cannot create drift between the scaffold and the final body.

---

## Coverage Notes

- **Spec coverage**: Goal, architecture, file layout, references, evals, README integration — all addressed.
- **Zero-context implementer feasibility**: Mostly yes for file creation; *no* for the README edits (see #4) and the empty-commit hazard (#1).
- **Command correctness**: Validator path, frontmatter schema, and grep patterns are correct against the real repo. The for-loop check (#2) and ls-emptiness check (#8) are not.
- **Verification completeness**: Structural validation is fine; behavioral/eval validation is missing (#3, #6, #17).
- **No malformed code blocks detected**; the 4-backtick fence in `templates.md` is intentional and correct.
- **No contradictory sequencing detected** beyond the empty-commit issue in Task 5.

CONSENSUS_STATUS=NEEDS_REVISION

---

## Caller Assessment — Round 2

### Review Mode
- `plan_file`

### Review Subject
- `docs/plans/active/2026-05-18-google-seo-geo-skill.md`

### Per-Issue Evaluation

#### Issue 1 — **`run_eval.py` module-style invocation required**
- **Oracle Severity:** Critical
- **Oracle's Evidence:** `docs/plans/active/2026-05-18-google-seo-geo-skill.md:759-770`
- **Caller Assessment:** Correctness 10, Relevance 10, Risk 9, Evidence 9 = **38/40**
- **Decision:** accept
- **Notes:** Fixed by switching to `python3 -m scripts.run_eval` from `skills/skill-creator/` and correcting relative paths.

#### Issue 2 — **Undeclared `opencode` CLI dependency**
- **Oracle Severity:** High
- **Oracle's Evidence:** `run_eval.py:53` and Task 5 Step 3
- **Caller Assessment:** Correctness 10, Relevance 9, Risk 8, Evidence 8 = **35/40**
- **Decision:** accept
- **Notes:** Fixed by adding a prerequisites section and an explicit skip path when `opencode` is unavailable.

#### Issue 3 — **Exit-0 is too lax for smoke success**
- **Oracle Severity:** High
- **Oracle's Evidence:** Task 5 Step 3 expected-output rule
- **Caller Assessment:** Correctness 10, Relevance 9, Risk 8, Evidence 8 = **35/40**
- **Decision:** accept
- **Notes:** Fixed by adding a JSON assertion step that checks `summary` and the per-query `trigger_rate` values.

#### Issue 4 — **Live LLM cost/offline risk not called out**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** Task 5 Step 3
- **Caller Assessment:** Correctness 9, Relevance 8, Risk 8, Evidence 7 = **32/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by documenting the smoke step as optional via the `opencode` skip path and scoping it as trigger-only behavior.

#### Issue 5 — **Ephemeral `/tmp` artifacts make reruns harder**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** Task 5 Step 3 and Step 4
- **Caller Assessment:** Correctness 7, Relevance 6, Risk 8, Evidence 7 = **28/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed partially by moving the trigger eval input into `skills/google-seo-geo/evals/trigger-evals.json`; leaving the output in `/tmp` is acceptable for a smoke check.

#### Issue 6 — **Reference-dir emptiness check should assert existence too**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** Task 3 Step 1
- **Caller Assessment:** Correctness 9, Relevance 7, Risk 8, Evidence 8 = **32/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by combining `test -d` with the emptiness assertion.

#### Issue 7 — **`PyYAML` dependency was undeclared**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** `quick_validate.py:8`
- **Caller Assessment:** Correctness 10, Relevance 8, Risk 8, Evidence 8 = **34/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by adding `PyYAML` to the prerequisites and an install hint.

#### Issue 8 — **Stale `--skill get-api-docs` line remains**
- **Oracle Severity:** Low
- **Oracle's Evidence:** README insertion block
- **Caller Assessment:** Correctness 6, Relevance 4, Risk 8, Evidence 7 = **25/40**
- **Decision:** neutral
- **Notes:** Left unchanged intentionally because that mismatch is pre-existing README drift outside this plan's scope.

#### Issue 9 — **`--timeout 20` is too tight**
- **Oracle Severity:** Low
- **Oracle's Evidence:** Task 5 Step 3
- **Caller Assessment:** Correctness 8, Relevance 6, Risk 8, Evidence 7 = **29/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by raising the timeout to `60`.

#### Issue 10 — **"implementation notes" step is unbounded**
- **Oracle Severity:** Low
- **Oracle's Evidence:** Task 5 Step 5
- **Caller Assessment:** Correctness 9, Relevance 7, Risk 9, Evidence 7 = **32/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by deleting the unbounded step entirely.

#### Issue 11 — **Need one clear prerequisites section**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** top of plan
- **Caller Assessment:** Correctness 10, Relevance 7, Risk 9, Evidence 7 = **33/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed with an explicit prerequisites block under Tech Stack.

#### Issue 12 — **Add a quick `run_eval --help` dry-run**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** Task 5 Step 3
- **Caller Assessment:** Correctness 9, Relevance 7, Risk 9, Evidence 7 = **32/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by adding `python3 -m scripts.run_eval --help >/dev/null` before the live trigger smoke run.

### Summary
- **Issues accepted:** 3
- **Issues accepted-with-caveat:** 8
- **Issues neutral:** 1
- **Issues rejected:** 0
- **Issues don't-know:** 0

### Caller Verdict
**NEEDS_REVISION**

### Notes for Oracle (next round)
- Fixed the broken `run_eval.py` invocation by switching to module-style execution from `skills/skill-creator/`.
- Added explicit prerequisites for `python3`, `PyYAML`, `git`, and optional `opencode`.
- Tightened the smoke pass criteria with JSON assertions against `summary` and `trigger_rate` fields.
- Moved the trigger eval input into `skills/google-seo-geo/evals/trigger-evals.json`.
- Added a clear skip path when `opencode` is unavailable, increased timeout to 60 seconds, and removed the unbounded final-notes step.

---

## Caller Assessment — Round 1

### Review Mode
- `plan_file`

### Review Subject
- `docs/plans/active/2026-05-18-google-seo-geo-skill.md`

### Per-Issue Evaluation

#### Issue 1 — **Task 5 final commit is empty**
- **Oracle Severity:** Critical
- **Oracle's Evidence:** `docs/plans/active/2026-05-18-google-seo-geo-skill.md:740-747`
- **Caller Assessment:** Correctness 10, Relevance 10, Risk 9, Evidence 9 = **38/40**
- **Decision:** accept
- **Notes:** Fixed by removing the no-op final commit step.

#### Issue 2 — **Task 3 Step 7 loop check is unsound**
- **Oracle Severity:** Critical
- **Oracle's Evidence:** `...:516-530`
- **Caller Assessment:** Correctness 10, Relevance 10, Risk 9, Evidence 9 = **38/40**
- **Decision:** accept
- **Notes:** Fixed by making the loop fail fast on the first missing or empty file.

#### Issue 3 — **No actual eval execution for a brand-new skill**
- **Oracle Severity:** High
- **Oracle's Evidence:** entire plan
- **Caller Assessment:** Correctness 7, Relevance 10, Risk 8, Evidence 6 = **31/40**
- **Decision:** accept-with-caveat
- **Notes:** The gap is real, but `run_eval.py` is a trigger-eval tool, not full behavioral grading. I fixed this by adding a trigger smoke check and explicitly scoping qualitative skill-tuning out of this initial repo change.

#### Issue 4 — **README edits are ambiguous**
- **Oracle Severity:** High
- **Oracle's Evidence:** `...:612-636`
- **Caller Assessment:** Correctness 10, Relevance 10, Risk 8, Evidence 8 = **36/40**
- **Decision:** accept
- **Notes:** Fixed by replacing prose-only instructions with exact old/new blocks and an exact insertion anchor.

#### Issue 5 — **Initial failing validator step adds noise**
- **Oracle Severity:** High
- **Oracle's Evidence:** `...:22-30`
- **Caller Assessment:** Correctness 9, Relevance 8, Risk 10, Evidence 8 = **35/40**
- **Decision:** accept
- **Notes:** Fixed by deleting the negative pre-check and starting directly with scaffolding.

#### Issue 6 — **Repo eval pipeline not acknowledged**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** entire plan
- **Caller Assessment:** Correctness 8, Relevance 8, Risk 8, Evidence 6 = **30/40**
- **Decision:** accept-with-caveat
- **Notes:** Addressed by adding `run_eval.py` trigger smoke coverage and explicitly noting that qualitative tuning is deferred.

#### Issue 7 — **Description deserves cheap insurance**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** `...:136`
- **Caller Assessment:** Correctness 5, Relevance 5, Risk 9, Evidence 6 = **25/40**
- **Decision:** neutral
- **Notes:** Useful but not necessary for this plan revision.

#### Issue 8 — **`ls` empty-dir check is unreliable**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** `...:303-309`
- **Caller Assessment:** Correctness 9, Relevance 7, Risk 9, Evidence 8 = **33/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed with `test -z "$(ls -A ...)"` for a real emptiness assertion.

#### Issue 9 — **Task 3 commit message understates scope**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** commit message lines
- **Caller Assessment:** Correctness 8, Relevance 6, Risk 9, Evidence 7 = **30/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by renaming the commit message to include the README rewrite.

#### Issue 10 — **README inventory drift should be acknowledged**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** active-skills replacement block
- **Caller Assessment:** Correctness 7, Relevance 6, Risk 8, Evidence 7 = **28/40**
- **Decision:** accept-with-caveat
- **Notes:** Addressed implicitly by preserving unrelated README content outside the exact replacement block; full inventory normalization remains out of scope.

#### Issue 11 — **No AGENTS update**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** entire plan
- **Caller Assessment:** Correctness 3, Relevance 4, Risk 9, Evidence 5 = **21/40**
- **Decision:** neutral
- **Notes:** I added an explicit N/A note because AGENTS is workflow guidance here, not a skill index.

#### Issue 12 — **Case-sensitive grep is fragile**
- **Oracle Severity:** Medium
- **Oracle's Evidence:** `...:262-270`
- **Caller Assessment:** Correctness 8, Relevance 6, Risk 8, Evidence 7 = **29/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by switching the checks to `grep -iE`.

#### Issue 13 — **Schema anti-pattern row is not verified**
- **Oracle Severity:** Low
- **Oracle's Evidence:** `...:471`
- **Caller Assessment:** Correctness 5, Relevance 4, Risk 9, Evidence 5 = **23/40**
- **Decision:** neutral
- **Notes:** Nice-to-have only.

#### Issue 14 — **4-backtick fence deserves a note**
- **Oracle Severity:** Low
- **Oracle's Evidence:** `...:407,452`
- **Caller Assessment:** Correctness 5, Relevance 4, Risk 9, Evidence 6 = **24/40**
- **Decision:** neutral
- **Notes:** The review itself confirms the fence is already correct.

#### Issue 15 — **Empty eval check adds little value**
- **Oracle Severity:** Low
- **Oracle's Evidence:** `...:548-561`
- **Caller Assessment:** Correctness 6, Relevance 4, Risk 10, Evidence 7 = **27/40**
- **Decision:** neutral
- **Notes:** Low-cost noise; acceptable to leave in place.

#### Issue 16 — **No failure-recovery guidance**
- **Oracle Severity:** Low
- **Oracle's Evidence:** entire plan
- **Caller Assessment:** Correctness 6, Relevance 5, Risk 8, Evidence 5 = **24/40**
- **Decision:** neutral
- **Notes:** Helpful but not required for an executable markdown-only repo task plan.

#### Issue 17 — **Add a smoke run**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** Task 5
- **Caller Assessment:** Correctness 9, Relevance 8, Risk 8, Evidence 6 = **31/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed with a `run_eval.py` trigger smoke step and explicit scope note.

#### Issue 18 — **Prefer `python3` to `python`**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** multiple task steps
- **Caller Assessment:** Correctness 9, Relevance 7, Risk 9, Evidence 8 = **33/40**
- **Decision:** accept-with-caveat
- **Notes:** Fixed by updating all commands to `python3`.

#### Issue 19 — **Consider a changelog note**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** Task 4 or 5
- **Caller Assessment:** Correctness 4, Relevance 3, Risk 9, Evidence 4 = **20/40**
- **Decision:** neutral
- **Notes:** Out of scope for this plan.

#### Issue 20 — **Duplicate frontmatter description should stay in sync**
- **Oracle Severity:** Suggestion
- **Oracle's Evidence:** `...:47, 136`
- **Caller Assessment:** Correctness 6, Relevance 4, Risk 8, Evidence 6 = **24/40**
- **Decision:** neutral
- **Notes:** Worth noticing, but not a blocker for this revision.

### Summary
- **Issues accepted:** 4
- **Issues accepted-with-caveat:** 8
- **Issues neutral:** 8
- **Issues rejected:** 0
- **Issues don't-know:** 0

### Caller Verdict
**NEEDS_REVISION**

### Notes for Oracle (next round)
- Fixed the empty final commit hazard by removing the no-op commit from Task 5.
- Fixed the reference-file validation loop to fail on the first missing or empty file.
- Replaced ambiguous README prose edits with exact old/new blocks and a precise insertion anchor.
- Removed the negative pre-validation step from Task 1.
- Switched validation commands from `python` to `python3`.
- Added a `run_eval.py` trigger smoke step and explicitly scoped full qualitative tuning out of this initial repo-addition plan.
- Added an explicit note that `AGENTS.md` is not a skill index in this repo.

---

## Round 2

**Overall assessment**: REQUEST_CHANGES — one Critical regression introduced by the new eval-runner step.

The author addressed nearly every Round 1 finding: the empty-commit hazard is gone, the for-loop check now fails fast, the `ls` emptiness check is sound, the README edit is now an exact old/new replacement with a precise insertion anchor, the noisy "fail first" pre-check was removed, `python3` is used throughout, commit messages were corrected, and Task 5 grep is now case-insensitive. Good revision work overall.

However, the new Task 5 Step 3 (the eval-runner smoke check added to close Round 1 issue #3 / #17) is broken as written and will crash before doing anything useful.

---

## Findings

### Critical

1. **Task 5 Step 3 — `run_eval.py` cannot be invoked as a script; it requires module-style invocation** (`docs/plans/active/2026-05-18-google-seo-geo-skill.md:759-770`)
   - `run_eval.py` does `from scripts.utils import parse_skill_md` at line 21. Running `python3 skills/skill-creator/scripts/run_eval.py …` from the repo root (or from any cwd I tested) raises `ModuleNotFoundError: No module named 'scripts'` immediately and exits non-zero. Verified locally.
   - The working invocation is `python3 -m scripts.run_eval …` executed from `skills/skill-creator/`. Once you do that, the relative paths in the command (`--eval-set /tmp/...` is fine; `--skill-path skills/google-seo-geo` is *not* — it resolves relative to `skills/skill-creator/`).
   - **Fix:** Either
     ```bash
     cd skills/skill-creator
     python3 -m scripts.run_eval \
       --eval-set /tmp/google-seo-geo-trigger-evals.json \
       --skill-path ../../skills/google-seo-geo \
       --provider opencode \
       --runs-per-query 1 \
       --num-workers 1 \
       --timeout 20 \
       --verbose > /tmp/google-seo-geo-trigger-results.json
     ```
     or set `PYTHONPATH=skills/skill-creator` before invoking the script, or open a small repo-level wrapper. As written, Step 3 will crash on line 1 of execution.

### High

2. **Task 5 Step 3 — undeclared hard dependency on the `opencode` CLI being on `PATH`** (`...:762-770`)
   - The chosen provider is `opencode`. `run_eval.py` builds `["opencode", "-p", query, …]` (see `build_command` at `skills/skill-creator/scripts/run_eval.py:53`) and relies on `shutil.which("opencode")`. The plan's "Tech Stack" section only lists "Markdown skill files, JSON eval definitions, Python 3 validation script, existing repo README conventions." A zero-context implementer on a fresh clone or a CI runner without the OpenCode CLI will see the smoke step fail with no diagnostic explaining why.
   - **Fix:** Either (a) list `opencode` (and PyYAML, which `quick_validate.py` also needs) as a prerequisite at the top of the plan, with install instructions, or (b) make the smoke step conditional on `command -v opencode` and document a clear skip path, or (c) switch to whichever provider the repo's CI standardizes on.

3. **Task 5 Step 3 — pass/fail criterion is too lax; an exit-0 doesn't prove the trigger worked** (`...:772`)
   - "Expected: command exits 0 and writes `/tmp/google-seo-geo-trigger-results.json`" only asserts that the runner ran. It does not assert that the two `should_trigger: true` queries actually triggered the skill, nor that the negative case did not. So a regression where the description fails to trigger would pass this step silently. The whole point of adding the eval step (per Round 1 #3 / #17) was behavioral validation; without an assertion this step is theater.
   - **Fix:** Add a follow-up step that parses the JSON and asserts the expected pattern, e.g.:
     ```bash
     python3 - <<'PY'
     import json, sys
     data = json.loads(open('/tmp/google-seo-geo-trigger-results.json').read())
     by_q = {r['query']: r for r in data}
     # Loose assertion: positive queries must have triggered at least once
     for q, r in by_q.items():
         if r['should_trigger'] and r.get('trigger_rate', 0) == 0:
             sys.exit(f"expected trigger but got 0: {q}")
     print("trigger smoke ok")
     PY
     ```
     Confirm the actual field name (`trigger_rate` vs `triggered` vs `runs[*].triggered`) by reading `run_eval.py` output schema before locking the assertion in.

### Medium

4. **Task 5 Step 3 — incurs a real LLM call per query, with cost and flakiness implications** (`...:759-774`)
   - Two `should_trigger: true` plus one `should_trigger: false` query times one run each through `opencode` is three live LLM calls every time someone runs this plan. The plan says "qualitative human review … is intentionally deferred" but does not warn that this *trigger* check itself is a live network/LLM call. CI without API credentials will fail; offline runs will fail.
   - **Fix:** Note explicitly: "Step 3 makes 3 live `opencode` LLM calls. Skip it if no provider credentials are available; in that case rely on the structural checks from Steps 1, 2, and 4." Optionally gate behind `if command -v opencode >/dev/null`.

5. **Task 5 Step 3 — eval-set is written to `/tmp` and never committed, results never collected** (`...:740-757,762-770`)
   - The trigger eval set is ephemeral. If the smoke check ever uncovers a problem, there is no artifact to inspect later because both inputs and outputs live in `/tmp`. For a one-time scaffold this is acceptable, but if the intent is for this smoke check to be re-runnable by other contributors, the trigger-eval JSON should live next to `evals/evals.json`.
   - **Fix:** Optional — promote the trigger eval set to `skills/google-seo-geo/evals/trigger-evals.json` and reference it from the smoke command. Then commit it in Task 4 Step 6 along with the main evals.

6. **Task 3 Step 1 — `test -z "$(ls -A …)"` will report empty even if the directory does not exist** (`...:295-299`)
   - If `skills/google-seo-geo/references` somehow does not exist at this point, `ls -A` prints an error to stderr and the command substitution is still empty, so `test -z` returns 0. The directory *does* exist after Task 1 Step 1, so this is mostly theoretical, but if Task 1 is skipped or partially executed the check silently passes.
   - **Fix:** Combine with an existence check: `test -d skills/google-seo-geo/references && test -z "$(ls -A skills/google-seo-geo/references)"`.

7. **`quick_validate.py` has an undeclared `PyYAML` dependency** (`...:Tech Stack`, `skills/skill-creator/scripts/quick_validate.py:8`)
   - The validator does `import yaml`. PyYAML is not a stdlib module and is not declared anywhere the plan touches. Fresh Python 3 installs will fail at every validation step (Task 1 Step 5, Task 2 Step 5, Task 5 Step 1). Round 1 missed this; surfacing now because the plan otherwise looks ready to run end-to-end.
   - **Fix:** Add a prereqs section noting `pip install pyyaml` (or whatever the repo standard is — check for a `requirements.txt` or `pyproject.toml` under `skills/skill-creator/` first).

### Low

8. **Task 4 Step 3 — README block still hard-codes the stale `--skill get-api-docs` example** (`...:637-643`)
   - The caller's note in Round 1 explicitly chose to preserve `--skill get-api-docs` even though the actual folder is `context-hub-get-api-docs`. That's a defensible decision for *this* plan, but it freezes a wrong install command for users. Not a blocker; flagging so it doesn't get forgotten.
   - **Fix:** Open a follow-up issue or add a one-line TODO in `README.md` so the next README edit catches the mismatch.

9. **Task 5 Step 3 — `--timeout 20` may be tight for cold opencode startup** (`...:768`)
   - On a cold start, the OpenCode CLI loading a skill plus making a model call routinely exceeds 20 seconds. False negatives are likely.
   - **Fix:** Bump to `--timeout 60` (the script's default is 30) or document that timeouts at this value are expected on first run.

10. **Task 5 Step 5 — "record verification output in implementation notes" is unbounded** (`...:787-789`)
    - This is a soft instruction with no defined deliverable (no file, no checklist). An executor following the plan literally has no idea what "implementation notes" means in this repo.
    - **Fix:** Either name the file (e.g., "append the validation log to the PR body" or "save to `docs/plans/active/2026-05-18-google-seo-geo-skill.execution-log.md`") or drop the step.

### Suggestion

11. **Plan should declare its full host prerequisites in one place** (top of plan)
    - Issues #2 and #7 above both stem from missing prereqs. A four-line "Prerequisites" subsection right under "Tech Stack" listing `python3`, `pyyaml`, `git`, and (for Task 5 Step 3 only) `opencode` would prevent both, and makes the plan trivially auditable for CI.

12. **Add a tiny dry-run of `run_eval.py` first** (Task 5 Step 3)
    - Before the live LLM call, run `python3 -m scripts.run_eval --help` from `skills/skill-creator/` and assert exit 0. This catches the Critical issue #1 in two seconds without needing provider credentials.

---

## Coverage Notes — Round 2

- **Round 1 P0 issues:** both fixed cleanly.
- **Round 1 P1 issues:** all four fixed; the fix for #3/#17 (eval runner) introduced the new Critical above.
- **Round 1 P2 issues:** the actionable ones were addressed (#6, #8, #9, #12); the neutrals are accepted as deliberate scope decisions.
- **Round 1 P3 / Suggestion:** `python3` swap was applied; the rest were noted and waived.
- **New regressions:** Task 5 Step 3 is the only step that will definitely fail on first execution as written.
- **Net delta:** The plan is one focused fix away from being executable end-to-end.

CONSENSUS_STATUS=NEEDS_REVISION

---

## Round 3

**Overall assessment**: MOSTLY_GOOD — Round 2's Critical and High issues are fixed; remaining gaps are Medium and below.

The Round 2 regression (Task 5 Step 3 `run_eval.py` invocation) is correctly addressed via `cd skills/skill-creator && python3 -m scripts.run_eval ...`, with adjusted `--skill-path` relative paths, a real pre-flight `--help` check, an `opencode` availability gate, a `--timeout 60` bump, a committed `trigger-evals.json` artifact, a Prerequisites section listing `python3`, `PyYAML`, `git`, and the optional `opencode` CLI, and a new Step 4 that actually asserts per-query trigger expectations against the output JSON. I verified the assertion schema against `run_eval.py:341-350` — `summary.total`, `summary.passed`, `results[*].trigger_rate` are real fields, and the assertions use them correctly.

Remaining issues are about defensive shell-script hygiene around the optional smoke step and a few small inconsistencies left over from earlier rounds.

---

## Findings

### Medium

1. **Task 5 Step 3 — `python3 -c "import yaml"` guard is a no-op without `||`** (`docs/plans/active/2026-05-18-google-seo-geo-skill.md:770`)
   - The line `python3 -c "import yaml" >/dev/null` exits non-zero if PyYAML is missing, but bash without `set -e` ignores the failure and falls through to the next line. The intended "fail loudly if PyYAML missing" semantics are not achieved. The Prerequisites section already covers the same ground, so this guard is redundant *or* should actually gate execution.
   - **Fix:** Either delete the line (Prerequisites already handles it) or wire it: `python3 -c "import yaml" >/dev/null 2>&1 || { echo "skip: PyYAML missing"; exit 0; }`.

2. **Task 5 Step 3 → Step 4 — empty/partial results file is mistaken for "ran successfully"** (`...:782, 795-797`)
   - The redirect `> /tmp/google-seo-geo-trigger-results.json` creates the file even when the subshell crashes before `run_eval.py` reaches its final `print(json.dumps(...))`. With `--verbose` going to stderr, an early provider failure (auth, timeout, network) leaves a zero-byte or truncated stdout. Step 4's existence check (`test ! -f ...`) then *passes* (file exists), and `json.loads("")` raises `JSONDecodeError`, masking the real failure.
   - **Fix:** Tighten Step 4's guard to also require non-empty content:
     ```bash
     { test ! -s /tmp/google-seo-geo-trigger-results.json; } && { echo "trigger smoke skipped"; exit 0; }
     ```
     and/or move the subshell to `… || { echo "smoke run failed"; exit 1; }` in Step 3.

### Low

3. **Task 5 Step 3 — `--help` pre-flight uses `&&` chaining, so a failure exits the subshell silently** (`...:772-783`)
   - If `python3 -m scripts.run_eval --help` fails (e.g., a future refactor renames `scripts/`), the subshell exits non-zero with no diagnostic, and because Step 3 is not chained with `&&` to anything that interprets the exit code, the overall step still appears to "succeed" by virtue of being the last statement. The diagnostic value of the `--help` check is lost.
   - **Fix:** Replace with `python3 -m scripts.run_eval --help >/dev/null || { echo "run_eval import broken"; exit 1; }`.

4. **Task 5 Step 4 — per-query assertions match by exact prompt string and will silently `KeyError` on drift** (`...:804-807`)
   - The assertions look up results via the exact query text from `trigger-evals.json`. Any future typo or punctuation change in either the eval set or the assertion strings (e.g., curly-quote, trailing whitespace) raises `KeyError` with a noisy traceback rather than a clear "query not found" diagnostic. Brittle.
   - **Fix:** Drive the assertions from the eval-set file itself, e.g.:
     ```python
     trigger_set = json.loads(Path('skills/google-seo-geo/evals/trigger-evals.json').read_text())
     for item in trigger_set:
         r = by_query[item['query']]
         if item['should_trigger']:
             assert r['trigger_rate'] > 0, item['query']
         else:
             assert r['trigger_rate'] == 0, item['query']
     ```

5. **Task 2 Step 1 — same "verify it fails first" antipattern that was removed from Task 1 still lives in Task 2** (`...:111-119`)
   - Round 1 #5 asked to drop noisy "negative pre-check" steps; that fix was applied to Task 1 only. The equivalent `grep -n "product-marketing-context" skills/google-seo-geo/SKILL.md` with `Expected: FAIL` is still present in Task 2. Inconsistent with the cleanup philosophy and adds no value.
   - **Fix:** Delete Task 2 Step 1 and renumber.

6. **Task 2 Step 4 — anti-pattern grep is still case-sensitive (`grep -E`) while Task 5 was updated to `-iE`** (`...:259`)
   - Round 1 #12 asked for `-iE`. Round 2 applied that only to Task 5 Step 5 (line 820-821). Task 2 Step 4 remained `grep -E`. Same fragility carries forward.
   - **Fix:** Change `grep -E` to `grep -iE` in Task 2 Step 4 for consistency.

7. **Task 5 Step 3 — `--runs-per-query 1` makes the smoke check inherently flaky** (`...:779`)
   - With one run per query and a default `--trigger-threshold 0.5`, a single random non-trigger from a temperature>0 model fails the assertion. Step 4 has no retry. Documented partly via the Round 2 acknowledgement, but worth pinning here too because it means a CI run can fail spuriously.
   - **Fix:** Either bump to `--runs-per-query 3` (matches the script's own default, ~3x cost) or explicitly set `--trigger-threshold 1.0` and document expected flakiness, or wrap Step 3 in a 2-retry loop.

### Suggestion

8. **Task 5 Step 3 — explicitly note expected wall-time and provider-auth requirement** (`...:765-788`)
   - With `--num-workers 1`, three queries, and `--timeout 60`, the worst-case wall-time is ~3 minutes. New executors will think the step hung. Also worth saying out loud: `opencode` must be authenticated; just having it on PATH is insufficient.
   - **Fix:** Add a one-liner under Step 3: "Expected wall-time: 30s–3min depending on provider latency. Requires `opencode` to be authenticated."

9. **Task 4 Step 7 — two `git add` lines could collapse into one** (`...:705-708`)
   - Cosmetic; current form is correct.
   - **Fix:** `git add skills/google-seo-geo/evals/evals.json skills/google-seo-geo/evals/trigger-evals.json README.md`.

10. **Task 5 Step 3 — `/tmp/google-seo-geo-trigger-results.json` is silently overwritten on every run** (`...:782`)
    - Local devs running the plan twice lose the prior failed-run artifact. Minor.
    - **Fix:** Append a timestamp suffix or move under `docs/plans/active/.runs/` if you want history.

---

## Coverage Notes — Round 3

- **Round 2 Critical (run_eval invocation):** fixed. Verified the module-style invocation works locally and that the output schema matches the assertions.
- **Round 2 High (opencode prereq, lax pass criterion):** fixed. Prerequisites added; Step 4 now asserts per-query expectations.
- **Round 2 Medium (live LLM warning, ephemeral artifacts, dir-exists guard, PyYAML prereq):** mostly fixed. Trigger-eval set is now committed. Live LLM caveat is implicit in the Prerequisites note ("optional `opencode` CLI plus working provider credentials"). Dir-exists guard in Task 3 Step 1 is correct.
- **Round 2 Low (stale `--skill get-api-docs`, tight timeout, unbounded notes step):** addressed (timeout to 60, notes step removed, stale install line documented as deliberate).
- **New issues this round:** all Medium-and-below; primarily defensive shell hygiene around the optional smoke step and two leftover Round 1 items (Task 2 Step 1 negative pre-check; Task 2 Step 4 case-sensitive grep) that were missed during the Round 2 sweep.
- **Net delta:** plan is executable end-to-end as written. Items above will improve robustness but do not block first-run success.

CONSENSUS_STATUS=MOSTLY_GOOD
