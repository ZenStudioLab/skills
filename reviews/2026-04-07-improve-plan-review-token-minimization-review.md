# Plan Review: Improve plan-review Token Minimization

**Plan File**: docs/plans/active/2026-04-07-improve-plan-review-token-minimization.md
**Reviewer**: opencode
**Round**: 1 — 2026-04-07

---

## Round 1 — 2026-04-07

### Overall Assessment
The plan correctly identifies three root causes of token bloat but presents an incomplete fix for the `ask_opencode.sh` heredoc corruption and an incorrectly specified grep command that will fail to extract the consensus status. The plan needs revision before implementation.
**Rating**: 4/10

### Issues

#### Issue 1 (Critical): Heredoc fix shows WHAT to remove, not what to KEEP
**Location**: Section 1 / "Fix: Remove lines 14–153"
The plan instructs to "remove lines 14–153" but does not specify what the correct content of the `usage()` heredoc should be after the fix. Lines 5–208 of `ask_opencode.sh` are one continuous heredoc (`cat <<'USAGE'` on line 5, closing `USAGE` on line 208). Simply deleting lines 14–153 leaves the heredoc structurally intact but still containing README content at lines 14–152 and 154–208. The plan needs to show the *expected correct state* of the heredoc — at minimum lines 1–13 and a redefined lines 14+ that contain only actual CLI usage text. Without this, a developer implementing the fix will not know what legitimate content (if any) should replace the removed lines.
**Suggestion**: Add a code block showing the exact target content of the `usage()` heredoc after the fix. For example:
```bash
usage() {
  cat <<'USAGE'
Usage:
  ask_opencode.sh <task> [options]
  ...
Options:
  -w, --workspace <path>   Workspace directory
USAGE
}
```

#### Issue 2 (Critical): grep command is logically broken
**Location**: Section 4 / "Fix: Replace Step 3 with a two-phase approach"
The proposed command `grep -m1 "^CONSENSUS_STATUS=" {review-file} | tail -1` has a fundamental contradiction. `grep -m1` limits output to 1 line and then exits — `tail -1` on a single-line result is a no-op. If the goal is to get the *last* occurrence (because multiple rounds exist), `tail -1` is correct but `grep -m1` is wrong — it stops at the *first* match, ignoring all subsequent rounds. These modifiers work against each other. Additionally, the command shown lacks shell quoting around the `{review-file}` variable, which will break on paths with spaces.
**Suggestion**: Use `grep "^CONSENSUS_STATUS=" {review-file} | tail -1` (remove `-m1`). If you want the first match only, use `grep -m1` without `tail -1`. Always quote variables: `grep "^CONSENSUS_STATUS=" "$review_file" | tail -1`.

#### Issue 3 (High): No verification/test plan for acceptance criteria
**Location**: "Acceptance Criteria" section
The acceptance criteria are listed as checkboxes but there is no mention of *how* to verify them. For criterion "ask_opencode.sh --help outputs only the CLI usage text", the reviewer must actually run `--help` and inspect the output. For "Argument errors no longer echo README content", the reviewer must trigger an argument error and verify stderr. The plan does not specify what commands to run or what the expected output should be.
**Suggestion**: Add a "Verification" subsection under Acceptance Criteria listing specific shell commands to run and expected output snippets for each criterion.

#### Issue 4 (High): Non-interactive instruction placement is ambiguous
**Location**: Section 2 / "Fix: Prepend this line to the reviewer prompt"
The plan says to "prepend this line to the reviewer prompt" but does not specify *where* in the prompt this instruction should appear relative to the format template (which starts with `Read the contents of...`). If the NON-INTERACTIVE line is prepended before the "Read the contents of..." block, it may get lost if the prompt is truncated at a certain length. The instruction should appear both at the very top and be repeated inside the format template section to survive truncation.
**Suggestion**: Show the exact revised prompt section in the plan, placing NON-INTERACTIVE as the absolute first line and adding a second instance inside the Requirements block for redundancy.

#### Issue 5 (High): No handling for missing/invalid CONSENSUS_STATUS trailer
**Location**: Section 3 and Section 4
The plan introduces `CONSENSUS_STATUS=<VALUE>` as the last line but does not specify what happens when: (a) the reviewer fails to append it, (b) an invalid value is used, or (c) extra content follows the trailer on the same line or after. The grep command in Step 3 will produce empty output or incorrect results in these edge cases with no error handling.
**Suggestion**: Add a "Contract" subsection defining that if `grep "^CONSENSUS_STATUS="` returns no match or an unknown value, the default behavior should be `NEEDS_REVISION`. Also specify that the trailer must be the exact last line with no trailing content.

#### Issue 6 (Medium): Round numbering convention not formally defined
**Location**: Section 3 / format template + "Round N" references throughout
The plan references "Round {N}" but does not define how N is determined. Is it 1-indexed? Is there a risk of drift if someone manually edits the review file? If multiple plan-review sessions run concurrently on the same plan file, round numbers could become ambiguous.
**Suggestion**: Define N as the count of `---` separators plus one, or use an ISO timestamp instead of sequential numbering to avoid ambiguity in concurrent editing scenarios.

#### Issue 7 (Medium): Script error handling not verified
**Location**: Section 1 / ask_opencode.sh heredoc
The heredoc is printed via `cat <<'USAGE'` on line 5 and closed at line 208. The plan removes lines 14–153 but does not verify that lines 169+ (the Options section) are syntactically valid Bash. If the README content accidentally replaced original option definitions, the heredoc fix may silently remove legitimate content.
**Suggestion**: After removing the README block, verify that all expected option flags (`-w`, `--workspace`, `-t`, `--task`, `--session`, `--status`, `-W`, `--watch`, `-f`, `--file`, `--model`) are still present in the heredoc.

#### Issue 8 (Medium): Step 3 revision does not address existing review file state
**Location**: Section 4 / "Fix: Replace Step 3"
The revised Step 3 says to grep the trailer "only if issues need to be evaluated for plan revision." This condition is vague. The plan should clarify: when is the full file *not* needed? For example, if `grep` returns `APPROVED`, no revision occurs and the full file can be skipped entirely. The trigger for full-file read should be explicitly defined.
**Suggestion**: Revise Step 3 to state: "Grep the trailer first. Only read the full review file if the status is `NEEDS_REVISION` or `MOSTLY_GOOD` (to evaluate the issues for plan revision). Skip full-file read on `APPROVED`."

#### Issue 9 (Low): Token savings estimate is missing
**Location**: "Background" and "Objective" sections
The plan states the goal is to "reduce token usage" but provides no estimate of current token cost or expected savings. Without quantified impact, it's impossible to validate whether the fixes justify the effort or to measure success post-implementation.
**Suggestion**: Add a before/after token estimate. For example: "Current ~140-line stderr output on each error adds ~X tokens per round. Fixing the heredoc + trailer grep reduces this to ~Y tokens per round."

#### Issue 10 (Low): Inconsistent heredoc delimiter naming
**Location**: Section 1 / ask_opencode.sh usage()
The heredoc uses `<<'USAGE'` (quoted delimiter), which prevents variable expansion inside — this is correct. However, the plan refers to it as a "heredoc corruption" without explaining *how* the README content got embedded. Understanding the mechanism (was it a copy-paste error? A merge conflict? A script generation bug?) would help prevent recurrence.
**Suggestion**: Add a "Root Cause" note explaining the embedding mechanism and a "Prevention" measure (e.g., heredoc content validation in CI).

### Positive Aspects
- Root causes are clearly identified and traceable to specific files and line ranges
- Three separate concerns (heredoc, non-interactive mode, trailer) are cleanly compartmentalized
- Scope boundaries (in/out of scope) are well-defined, preventing feature creep
- The `CONSENSUS_STATUS` trailer concept is sound — reducing full-file reads is the right optimization
- Acceptance criteria are concrete and verifiable

### Summary

**Top 3 key issues:**
1. **Heredoc fix is incomplete** — shows lines to remove but not what to replace them with; the heredoc spans lines 5–208, so removing 14–153 alone does not fix the problem
2. **grep command is broken** — `grep -m1 ... | tail -1` contradicts itself; remove `-m1` or `tail -1`, not both
3. **No error handling for missing/invalid CONSENSUS_STATUS** — no defined behavior when grep returns empty or the trailer is absent

**Consensus Status**: NEEDS_REVISION
CONSENSUS_STATUS=NEEDS_REVISION

---

## Round 3 — 2026-04-07

### Overall Assessment
The plan is close to implementable but remains blocked by four persistent issues across two rounds and several new concrete problems. The heredoc fix description conflates heredoc-internal line positions with file line numbers, creating genuine risk of developer miscount. The "remove" vs "replace" language is still contradictory. SKILL.md has not been updated to reflect the NON-INTERACTIVE requirement or the Step 3 trailer-grep change. Token savings math is still unverified.
**Rating**: 6.5/10

### Previous Round Tracking

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| R1-1 | Heredoc fix shows WHAT to remove, not what to KEEP | Partially Fixed | Target structure added but closing `USAGE` not shown as explicit line |
| R1-2 | grep command logically broken | Fixed | `grep ... \| tail -1 \| cut -d= -f2` is correct |
| R1-3 | No verification/test plan | Fixed | Verification commands section added |
| R1-4 | NON-INTERACTIVE placement ambiguous | Fixed | Two-point placement shown in plan, but SKILL.md still not updated |
| R1-5 | No missing/invalid CONSENSUS_STATUS handling | Fixed | Contract and Fallback well-specified |
| R1-6 | Round numbering not defined | Unchanged | Still no definition of N |
| R1-7 | Script option completeness not verified | Partially Fixed | AC3 lists flags; actual content check not performed |
| R1-8 | Step 3 vague on when to skip full-file read | Fixed | Explicit "skip on APPROVED" added |
| R1-9 | Token savings estimate missing | Fixed | "~840 tokens per error event" added |
| R1-10 | No root cause / prevention mechanism | Partially Fixed | Prevention note in fix description; no AC or CI check |
| R2-1 | Heredoc closing `USAGE` delimiter missing | Partially Fixed | Target structure ends with `USAGE` but visually absorbed into code block |
| R2-2 | "Remove lines 14–153" contradicts target structure | Partially Fixed | Fix description still says "remove"; should say "replace" |
| R2-3 | `--badarg` not recognized | Fixed | `--badarg` does match `-*)` pattern and triggers error at line 333 |
| R2-4 | Step 3 bash uses `cut` but prose fallback does not | Not Fixed | Prose fallback still omits `cut` extraction |
| R2-5 | Round numbering undefined | Unchanged | Still unaddressed |
| R2-6 | Verification commands section header orphaned | Unchanged | Still no intro sentence |
| R2-7 | Prevention mechanism not specified | Partially Fixed | Comment mentioned in fix description; no AC to verify it |

### Issues

#### Issue 1 (Critical): Heredoc fix uses two different line-numbering systems without clarifying which is which
**Location**: Section 1 / "Problem" (line 16) and "Fix" (line 42)
The plan says "Lines 14–153 contain plan-review/README.md content accidentally embedded" and "Remove lines 14–153". But the heredoc in `ask_opencode.sh` starts at line 5 (`cat <<'USAGE'`) and closes at line 208 (`USAGE`). The numbers 14–153 are **heredoc-internal line positions** (counting from line 6 inside the heredoc as position 1), not file line numbers. A developer counting file lines 14–153 in the actual script will find mermaid diagram code, not README prose — those README blocks are at file lines 14–13+154=167, 52–13+154=206, etc. (inside the heredoc). The plan never explains this distinction, so an implementer reading "remove lines 14–153" literally will do the wrong thing.
**Suggestion**: Change the Problem description to clarify: "Lines 14–153 (inside the heredoc body, file lines ~14–167) contain the README content." Then change the Fix instruction to: "Replace the entire heredoc body (everything between `cat <<'USAGE'` and the closing `USAGE` delimiter on line 208) with the target structure below."

#### Issue 2 (Critical): "Remove lines 14–153" is still the fix instruction despite the target structure being a replacement
**Location**: Section 1 / "Fix" (line 42)
Round 2 correctly identified this contradiction but the plan still reads "Remove lines 14–153" instead of "Replace lines 14–153 with the target structure below." The target structure is a full replacement block — it cannot be achieved by deletion alone. A developer following "remove lines 14–153" literally would delete those lines and leave a malformed heredoc with orphaned content.
**Suggestion**: Change line 42 from "Fix: Replace the entire body of the heredoc (everything between `cat <<'USAGE'` and the closing `USAGE` delimiter) with the target structure below. Do not merely delete lines — confirm the replacement produces the exact output shown." Remove the phrase about lines 14–153 entirely from the Fix description.

#### Issue 3 (High): SKILL.md Step 2 reviewer prompt does not contain the NON-INTERACTIVE requirement
**Location**: `skills/plan-review/SKILL.md`, Step 2 (lines 44–99)
The plan specifies that the reviewer prompt must contain `NON-INTERACTIVE` as the first line and inside the Requirements block. However, reading `skills/plan-review/SKILL.md` shows the reviewer prompt block (lines 44–99) starts directly with "Read the contents of {plan-file-path}..." with no `NON-INTERACTIVE` line at the top and no `NON-INTERACTIVE` inside Requirements. The plan describes the fix but the SKILL.md has not been updated to match. This means any future review triggered through the actual skill would not enforce non-interactive behavior.
**Suggestion**: Add `NON-INTERACTIVE` as the absolute first line of the prompt block AND add `- NON-INTERACTIVE: do not ask clarifying questions at any point` as the first item in the Requirements list (lines 47–48), exactly as the plan specifies in Section 2.

#### Issue 4 (High): SKILL.md Step 3 still instructs full-file read before checking trailer
**Location**: `skills/plan-review/SKILL.md`, Step 3 (lines 112–117)
Step 3 currently says "I read the latest review round in the review file" — there is no mention of greipping `CONSENSUS_STATUS=` first and only reading the full file when `NEEDS_REVISION` or `MOSTLY_GOOD`. The plan's Section 4 describes a two-phase approach (grep trailer → conditionally read full file), but SKILL.md has not been updated to reflect this. The plan's acceptance criterion AC6 (line 151: "Claudius Step 3 greps the trailer before reading the full file") cannot be met until SKILL.md is updated.
**Suggestion**: Replace Step 3 prose (lines 112–117) with the two-phase bash approach from plan Section 4, specifying that Claude must first `grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2` and only read the full file when the status is `NEEDS_REVISION` or `MOSTLY_GOOD`.

#### Issue 5 (High): Token savings math is unverified and uses a hand-wavy multiplier
**Location**: "Estimated token savings" (line 10)
The estimate reads "~140 lines × ~6 tokens = ~840 tokens". The "~6 tokens per line" figure is implausible — English text at typicalLLM tokenization rates is 1.3–1.5x word count, and a line of prose averages 10–15 words, implying ~13–22 tokens per line, not 6. The "~" hedge throughout also means the numbers are illustrative rather than calculated. Additionally, the "~140 lines" refers to heredoc-internal line positions, not file lines. The true stderr inflation from a corrupted ~140-line heredoc is likely 500–1200+ tokens depending on the model, not 840.
**Suggestion**: Replace the estimate with: "Current: ~140-line heredoc output on each error (~500–1200 tokens depending on model). After fix: CLI usage text only (~10–20 lines, ~50–100 tokens)." Cite the actual token counts from running `ask_opencode.sh --help` and measuring output size.

#### Issue 6 (Medium): Prose fallback for CONSENSUS_STATUS extraction omits `cut -d= -f2`
**Location**: Section 4 / Fallback (line 129)
The bash snippet correctly uses `cut -d= -f2` to extract the value after `=`. But the prose fallback says "If empty or unrecognized → NEEDS_REVISION" without referencing `cut`. If someone implements the fallback from prose alone, they will compare the full `CONSENSUS_STATUS=VALUE` string against the valid values, which will always fail, treating everything as `NEEDS_REVISION` even when the trailer is correctly present.
**Suggestion**: Change the prose fallback to: `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2); if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then status="NEEDS_REVISION"; fi`

#### Issue 7 (Medium): AC1 and AC2 verification both test the same output stream
**Location**: "Verification commands" / AC1 and AC2 (lines 160–164)
Both AC1 (`ask_opencode.sh --help 2>&1`) and AC2 (`ask_opencode.sh --unknown-flag 2>&1`) redirect stdout+stderr together. The heredoc corruption affects the heredoc content emitted to stderr in both cases (line 333 for unknown flags, line 332 for --help). But the distinction between AC1 and AC2 testing different error paths is lost because both commands funnel the same output through `2>&1`. If the fix is applied and the heredoc is corrected, both tests should pass. But if only one test fails, there's no way to know which error path is still broken.
**Suggestion**: Split the verification to test each error path distinctly: AC1 tests `--help` stdout output (no redirect needed); AC2 tests stderr-only by capturing just stderr: `ask_opencode.sh --unknown-flag 2>&1 >/dev/null | grep -c "Plan Review"`.

#### Issue 8 (Medium): Prevention comment mentioned in fix but not checked by any acceptance criterion
**Location**: Section 1 / Prevention (line 85) and "Acceptance Criteria" (lines 144–152)
The fix description (line 85) says to add a warning comment above the `usage()` function. But none of the seven acceptance criteria verify this comment was added. Without a checkbox, an implementer may skip the comment and still pass all acceptance criteria, leaving the prevention measure unimplemented while claiming full compliance.
**Suggestion**: Add to Acceptance Criteria: `[ ] A `# WARNING: Do not embed external file content inside this heredoc.` comment is present directly above the `usage()` function in `ask_opencode.sh`"

#### Issue 9 (Medium): Round numbering convention remains undefined (3rd round unaddressed)
**Location**: "Previous Round Tracking" table header + Round N references (R1 Issue 6, R2 Issue 5)
The plan still provides no definition of how N is computed in `## Round {N}`. The SKILL.md format template uses `## Round {N} — {YYYY-MM-DD}` but neither document specifies the algorithm. If two sessions append rounds concurrently or someone manually edits the file, sequential numbering drifts. ISO timestamps would be unambiguous but would also break existing round-counting logic.
**Suggestion**: Define N in the SKILL.md format template: "N = number of `---` round separators in the file, starting at 1 for the first round." Or add a note that round numbers are cosmetic and the authoritative iteration signal is the `CONSENSUS_STATUS=` trailer.

#### Issue 10 (Low): Verification commands use placeholder path `reviews/<topic>-review.md`
**Location**: "Verification commands" / AC5 and AC6 (lines 169–173)
The commands show `reviews/<topic>-review.md` as the file path, which is a literal template placeholder. If a developer runs these commands without substituting the actual path (`reviews/2026-04-07-improve-plan-review-token-minimization-review.md`), both commands will fail or produce misleading results. Using the actual plan and review file names in the examples would make the commands immediately runnable.
**Suggestion**: Replace `reviews/<topic>-review.md` with the actual review file name `reviews/2026-04-07-improve-plan-review-token-minimization-review.md` in all verification command examples.

#### Issue 11 (Low): `tail -1` on CONSENSUS_STATUS verification may capture trailing newline
**Location**: "Verification commands" / AC5 (line 170)
`tail -1 reviews/...-review.md` returns the last line of the file. If the review file ends with `CONSENSUS_STATUS=NEEDS_REVISION\n` (with a trailing newline, which is standard POSIX text file behavior), `tail -1` returns the newline character alone, which `grep "^CONSENSUS_STATUS="` will not match. The verification would fail even though the trailer is present and correctly formatted.
**Suggestion**: Change AC5 to: `grep -v "^$" < reviews/2026-04-07-improve-plan-review-token-minimization-review.md | tail -1 | grep "^CONSENSUS_STATUS="` — this strips blank lines before the final `tail` to ensure the last non-empty line is captured.

#### Issue 12 (Low): Verification commands label is AC5 and AC6 but Acceptance Criteria only go to AC7
**Location**: "Verification commands" (line 169) and "Acceptance Criteria" (lines 144–152)
The verification commands reference AC5 and AC6, but the acceptance criteria section has only 7 items (AC1–AC7), with no item labeled AC5 or AC6 in the Acceptance Criteria list itself. The mismatch between the two numbering systems (Acceptance Criteria vs Verification Commands) creates confusion about which criterion each verification command validates.
**Suggestion**: Make verification command comments match the acceptance criterion numbers: prefix each verification command with `# AC<N>: <description>` where N matches the corresponding checkbox number in the Acceptance Criteria section.

### Positive Aspects
- The heredoc target structure (Section 1, lines 44–83) is now complete and correct — shows full function including opening and closing
- CONSENSUS_STATUS contract, fallback behavior, and two-phase grep approach are all well-specified
- Verification commands section is actionable and covers all major acceptance criteria
- NON-INTERACTIVE placement is explicit in the plan text; just needs SKILL.md synchronization
- Token savings framing (error-path reduction + trailer grep) provides clear motivation

### Summary

**Top 3 key issues:**
1. **Heredoc fix line numbers are ambiguous** — "lines 14–153" refers to heredoc-internal positions, not file lines; developer could miscount and corrupt the heredoc further
2. **SKILL.md not updated** — NON-INTERACTIVE (Step 2) and trailer-first Step 3 are specified in the plan but absent from the actual skill file; the plan cannot be validated against its own acceptance criteria
3. **Prevention measure unchecked** — the warning comment is described in the fix but has no acceptance criterion; it could be silently dropped during implementation

**Consensus Status**: NEEDS_REVISION

CONSENSUS_STATUS=NEEDS_REVISION

---

## Round 4 — 2026-04-07

### Overall Assessment
The plan has been refined across three rounds but remains unimplemented — SKILL.md Step 2 and Step 3 are unchanged despite the plan prescribing exact modifications to both, and the heredoc corruption in `ask_opencode.sh` is confirmed present. The acceptance criteria contain a typo ("Claudius" instead of "Claude") and a critical gap: the prevention comment AC is missing entirely. Token savings math is still unverified hand-waving.
**Rating**: 6/10

### Previous Round Tracking

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| R1-1 | Heredoc fix shows WHAT to remove, not what to KEEP | Partially Fixed | Target structure added but plan's Fix section still says "remove" in prose |
| R1-2 | grep command logically broken | Fixed | |
| R1-3 | No verification/test plan | Fixed | |
| R1-4 | NON-INTERACTIVE placement ambiguous | Partially Fixed | Plan specifies it; SKILL.md Step 2 is still missing it |
| R1-5 | No missing/invalid CONSENSUS_STATUS handling | Fixed | |
| R1-6 | Round numbering not defined | Unchanged | |
| R1-7 | Script option completeness not verified | Partially Fixed | AC3 lists flags; no content verification |
| R1-8 | Step 3 vague on when to skip full-file read | Partially Fixed | Plan specifies skip-on-APPROVED; SKILL.md Step 3 unchanged |
| R1-9 | Token savings estimate missing | Partially Fixed | "~840 tokens" still hand-wavy |
| R1-10 | No root cause / prevention mechanism | Partially Fixed | Prevention comment described; no AC to verify it |
| R2-1 | Heredoc closing USAGE delimiter missing | Fixed | Target structure ends with `USAGE` |
| R2-2 | "Remove lines 14–153" contradicts target structure | Partially Fixed | Fix prose still says "remove"; target structure is full replacement |
| R2-3 | `--badarg` not recognized | Fixed | `--unknown-flag` is correct |
| R2-4 | Prose fallback omits `cut` | Not Fixed | Plan Step 4 fallback prose still omits `cut -d= -f2` |
| R2-5 | Round numbering undefined | Unchanged | |
| R2-6 | Verification commands section header orphaned | Fixed | Intro sentence added |
| R2-7 | Prevention mechanism not specified | Partially Fixed | Comment described; no AC |
| R3-1 | Heredoc fix uses two line-numbering systems | Partially Fixed | Clarification added but "lines 14–153" still in Background |
| R3-2 | "Remove lines 14–153" still in Fix instruction | Partially Fixed | Fix prose still uses "remove"; target structure is replacement |
| R3-3 | SKILL.md Step 2 NON-INTERACTIVE missing | Unchanged | Confirmed: SKILL.md lines 44-99 have no NON-INTERACTIVE |
| R3-4 | SKILL.md Step 3 trailer-first approach missing | Unchanged | Confirmed: SKILL.md Step 3 (lines 112-117) does full-file read |
| R3-5 | Token savings math unverified | Unchanged | "~6 tokens per line" still hand-wavy |
| R3-6 | Prose fallback omits `cut` | Unchanged | |
| R3-7 | AC1 and AC2 test same output stream | Unchanged | |
| R3-8 | Prevention comment not checked by AC | Unchanged | AC8 (prevention comment) does not exist in the AC list |
| R3-9 | Round numbering undefined | Unchanged | |
| R3-10 | Verification commands use placeholder path | Unchanged | |
| R3-11 | `tail -1` may capture trailing newline | Unchanged | |
| R3-12 | Verification commands label mismatch | Unchanged | |

### Issues

#### Issue 1 (Critical): SKILL.md Step 2 reviewer prompt is completely missing NON-INTERACTIVE
**Location**: `skills/plan-review/SKILL.md`, Step 2 prompt block (lines 44–99)
The plan Section 2 mandates `NON-INTERACTIVE` as the absolute first line of the reviewer prompt AND inside the Requirements block. Reading the actual SKILL.md file confirms: line 44 is `Read the contents of {plan-file-path}...` with no `NON-INTERACTIVE` preceding it, and the Requirements block (lines 47–51) contains no `NON-INTERACTIVE` entry. This means the skill does not enforce non-interactive behavior regardless of what the plan says. An implementer who follows the plan literally would need to know to edit SKILL.md — but the plan never explicitly says "edit SKILL.md Step 2."
**Suggestion**: Add explicit instruction in the plan: "Edit `skills/plan-review/SKILL.md` Step 2 reviewer prompt block (lines 44–99): prepend `NON-INTERACTIVE: Complete this review autonomously...` as line 1, and add `- NON-INTERACTIVE: do not ask clarifying questions at any point` as the first Requirements item." Without this explicit edit instruction, the plan's own acceptance criterion AC4 ("Reviewer prompt contains NON-INTERACTIVE as first line and inside Requirements") cannot be satisfied.

#### Issue 2 (Critical): SKILL.md Step 3 has no trailer-first grep; still does full-file read
**Location**: `skills/plan-review/SKILL.md`, Step 3 (lines 112–117)
The plan Section 4 prescribes a two-phase approach: grep `CONSENSUS_STATUS=` first, then conditionally read the full file only on `NEEDS_REVISION` or `MOSTLY_GOOD`. Reading the actual SKILL.md shows Step 3 (lines 112–117) says only "After the agent finishes, I read the latest review round in the review file" with no mention of grep first or conditional reading. The acceptance criterion AC6 ("Claude's Step 3 greps the trailer before reading the full file") is impossible to validate because the skill itself does not describe this behavior. Like Issue 1, the plan describes the fix but does not say "edit SKILL.md Step 3."
**Suggestion**: Add explicit instruction in the plan: "Edit `skills/plan-review/SKILL.md` Step 3 (lines 112–117): replace the current prose with the two-phase approach from plan Section 4, specifying the grep command and conditional full-file read." Also fix the typo "Claudius" → "Claude's" in AC6.

#### Issue 3 (High): AC6 acceptance criterion has a typo — "Claudius" instead of "Claude's"
**Location**: Acceptance Criteria, line 151
AC6 reads "Claudius Step 3 greps the trailer before reading the full file". This is a typo — "Claudius" is not a recognized entity in the workflow. The correct text should be "Claude's Step 3".
**Suggestion**: Change line 151 to: `- [ ] Claude's Step 3 greps the trailer before reading the full file; skips full-file read on APPROVED`

#### Issue 4 (High): Prevention comment acceptance criterion is described but does not exist
**Location**: Acceptance Criteria section vs. Section 1 Prevention note (line 85)
The plan's Section 1 Fix description says to add a warning comment above `usage()` and the Background mentions it as a prevention measure. However, none of the 7 acceptance criteria checkboxes verify this comment was actually added. An implementer could skip the comment and still satisfy all ACs, claiming full compliance while the prevention measure is absent.
**Suggestion**: Add an explicit acceptance criterion: `- [ ] A `# WARNING: Do not embed external file content inside this heredoc.` comment is present directly above the `usage()` function in \`ask_opencode.sh\`` numbered AC8 (or AC0 if sequence matters).

#### Issue 5 (High): Plan says "edit SKILL.md" implicitly but never states it explicitly
**Location**: Throughout plan — Section 2 and Section 4 describe changes to `skills/plan-review/SKILL.md` but only by specifying the content that should appear; the plan never says "Edit `skills/plan-review/SKILL.md` to make these changes"
The Scope says "Add non-interactive instruction to the reviewer prompt in `plan-review/SKILL.md`" and "Add machine-readable CONSENSUS_STATUS trailer to the review format" — but these are descriptions of the change goal, not an implementation instruction. An implementer might read these as needing to only modify the heredoc in `ask_opencode.sh` (the concrete code change) without realizing SKILL.md must also be edited.
**Suggestion**: Add an "Implementation" section or prepend an explicit "Edit `skills/plan-review/SKILL.md`" instruction to Section 2 and Section 4 so the SKILL.md changes are unmistakable requirements, not optional descriptions.

#### Issue 6 (Medium): Prose fallback in Section 4 still omits `cut -d= -f2`
**Location**: Section 4 / Fallback (line 129)
The bash snippet correctly uses `cut -d= -f2` to extract the value. The prose fallback says "If empty or unrecognized value, treat as NEEDS_REVISION" without referencing `cut`. Someone implementing from prose alone will compare the full `CONSENSUS_STATUS=VALUE` string against the valid values and get silent failures.
**Suggestion**: Change the prose fallback to: `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2); if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then status="NEEDS_REVISION"; fi`

#### Issue 7 (Medium): Verification commands AC5 and AC6 mismatch with actual AC numbering
**Location**: Verification commands section, lines 170–173
The verification command comments reference "AC5" and "AC6", but the Acceptance Criteria list (lines 149–155) has no item labeled AC5 or AC6. AC4 = NON-INTERACTIVE, AC5 = trailer present, AC6 = grep returns last-round. The mismatch between the two numbering systems means a reviewer cannot cross-reference which criterion each command validates.
**Suggestion**: Make verification command comment prefixes match the acceptance criterion numbers exactly. For example, prefix with `# AC5:` (trailer present) and `# AC6:` (grep correctly returns last-round) — and ensure these numbers correspond to actual AC checkbox labels in the Acceptance Criteria section.

#### Issue 8 (Medium): Token savings estimate uses implausible "~6 tokens per line" multiplier
**Location**: "Estimated token savings" (line 10)
The estimate reads "~140 lines × ~6 tokens = ~840 tokens". At typical LLM tokenization, a prose line averages 10–15 words ≈ 13–22 tokens, not 6. The "~" hedge makes this purely illustrative. The estimate conflates line count with token count without measurement.
**Suggestion**: Either run `ask_opencode.sh --help 2>&1 | wc -c` and `ask_opencode.sh --unknown-flag 2>&1 | wc -c` to get actual byte counts and convert to estimated tokens (1 token ≈ 4 chars), or replace with a clearer statement: "Current: ~140-line heredoc emitted on each error (~500–1200 tokens depending on model). After fix: CLI usage text only (~10–20 lines, ~50–100 tokens)."

#### Issue 9 (Medium): "Lines 14–153" in Background conflates heredoc-internal positions with file line numbers
**Location**: Background (line 16) and Fix (line 42)
The Background says "Lines 14–153 are the full content of plan-review/README.md accidentally embedded inside it." In `ask_opencode.sh`, the heredoc opens at line 5 (`cat <<'USAGE'`) and closes at line 208 (`USAGE`). The numbers 14–153 are heredoc-internal line positions (counting from line 6 inside the heredoc as position 1). The actual README content appears at different file line numbers due to the repetition pattern (the README content appears three times, creating 3 copies × ~46 lines each ≈ 138 lines). A developer counting file lines 14–153 will find mermaid diagram code, not README prose.
**Suggestion**: Change Background line 16 to clarify: "Lines 14–153 (heredoc-internal positions; within the file these blocks appear at approximately file lines 14–167, 52–206, and 91–246) contain the README content embedded three times." Or simplify: "The heredoc body (lines 6–207 inside the heredoc) contains plan-review/README.md embedded three times (~138 lines total)."

#### Issue 10 (Medium): `tail -1` verification for AC5 may return trailing newline
**Location**: Verification commands / AC5 (line 170)
`tail -1 reviews/... | grep "^CONSENSUS_STATUS="` fails when the file ends with `CONSENSUS_STATUS=NEEDS_REVISION\n` because `tail -1` returns the newline character alone, which `grep` does not match.
**Suggestion**: Change AC5 verification to: `grep -v "^$" < reviews/2026-04-07-improve-plan-review-token-minimization-review.md | tail -1 | grep "^CONSENSUS_STATUS="` — this strips blank lines before `tail` to ensure the last non-empty line is tested.

#### Issue 11 (Low): Round numbering convention still undefined after 3 rounds
**Location**: SKILL.md format template and plan round references
The SKILL.md format template uses `## Round {N} — {YYYY-MM-DD}` but neither document specifies how N is computed. R3-9 flagged this; it remains unaddressed. If two review sessions append concurrently, N drifts.
**Suggestion**: Define N in the SKILL.md format template section: "N = number of `---` separators in the file + 1, starting at 1." Or add a note that round numbers are cosmetic and the authoritative iteration signal is the `CONSENSUS_STATUS=` trailer.

#### Issue 12 (Low): Verification commands use placeholder path `reviews/<topic>-review.md`
**Location**: Verification commands / AC5 and AC6 (lines 170, 173)
Both commands show `reviews/<topic>-review.md` as the path. Using the actual file name (`reviews/2026-04-07-improve-plan-review-token-minimization-review.md`) would make the commands immediately runnable without substitution.
**Suggestion**: Replace `reviews/<topic>-review.md` with `reviews/2026-04-07-improve-plan-review-token-minimization-review.md` in AC5 and AC6 verification commands.

### Positive Aspects
- Target heredoc structure (lines 44–83) is complete and correct — the replacement block is well-specified and implementable
- CONSENSUS_STATUS contract, fallback behavior, and two-phase grep approach are all sound in the plan
- Verification commands are concrete and actionable for most criteria
- The heredoc corruption is real and confirmed in `ask_opencode.sh` lines 14–154 — fixing it will definitely reduce token noise
- Scope boundaries remain well-defined, preventing feature creep

### Summary

**Top 3 key issues:**
1. **SKILL.md Step 2 and Step 3 are unchanged** — plan describes exact modifications but never explicitly instructs to edit the skill file; without SKILL.md updates, the skill does not enforce NON-INTERACTIVE or trailer-first grep
2. **Prevention comment (AC8) missing from acceptance criteria** — the warning comment above `usage()` is described in the fix but has no checkbox to verify it; it could be silently dropped
3. **AC6 typo ("Claudius") and numbering mismatch** — AC6 is mislabeled and verification commands don't cross-reference correctly to actual AC numbers

**Consensus Status**: NEEDS_REVISION

CONSENSUS_STATUS=NEEDS_REVISION

---

## Round 5 — 2026-04-07

### Overall Assessment
The plan remains unimplemented after four rounds. SKILL.md Step 2 and Step 3 are unchanged from their original state — the NON-INTERACTIVE requirement and trailer-first grep approach exist only in the plan text, not in the actual skill file. The heredoc corruption in `ask_opencode.sh` is confirmed present (embedded README content visible at lines 14–153). Several issues persist across all four prior rounds with no resolution.
**Rating**: 5.5/10

### Previous Round Tracking

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| R1-1 | Heredoc fix shows WHAT to remove, not what to KEEP | Partially Fixed | Target structure added; "remove" language still in Fix prose |
| R1-2 | grep command logically broken | Fixed | `grep ... \| tail -1 \| cut -d= -f2` is correct |
| R1-3 | No verification/test plan | Fixed | Verification commands section added |
| R1-4 | NON-INTERACTIVE placement ambiguous | Partially Fixed | Plan specifies; SKILL.md Step 2 unchanged |
| R1-5 | No missing/invalid CONSENSUS_STATUS handling | Fixed | Contract and Fallback well-specified |
| R1-6 | Round numbering not defined | Unchanged | Still no definition after 4 rounds |
| R1-7 | Script option completeness not verified | Partially Fixed | AC3 lists flags; no content verification |
| R1-8 | Step 3 vague on when to skip full-file read | Partially Fixed | Plan specifies skip-on-APPROVED; SKILL.md Step 3 unchanged |
| R1-9 | Token savings estimate missing | Partially Fixed | "~840 tokens" still hand-wavy |
| R1-10 | No root cause / prevention mechanism | Partially Fixed | Prevention comment described; no AC to verify it |
| R2-1 | Heredoc closing USAGE delimiter missing | Fixed | Target structure ends with `USAGE` |
| R2-2 | "Remove lines 14–153" contradicts target structure | Partially Fixed | Fix prose still says "remove" |
| R2-3 | `--badarg` not recognized | Fixed | `--unknown-flag` is correct |
| R2-4 | Prose fallback omits `cut` | Not Fixed | Plan Step 4 fallback prose still omits `cut -d= -f2` |
| R2-5 | Round numbering undefined | Unchanged | |
| R2-6 | Verification commands section header orphaned | Fixed | Intro sentence added |
| R2-7 | Prevention mechanism not specified | Partially Fixed | Comment described; no AC |
| R3-1 | Heredoc fix uses two line-numbering systems | Partially Fixed | Clarification added but "lines 14–153" still in Background |
| R3-2 | "Remove lines 14–153" still in Fix instruction | Partially Fixed | Fix prose still uses "remove" |
| R3-3 | SKILL.md Step 2 NON-INTERACTIVE missing | Unchanged | Confirmed: SKILL.md lines 44-99 have no NON-INTERACTIVE |
| R3-4 | SKILL.md Step 3 trailer-first approach missing | Unchanged | Confirmed: SKILL.md Step 3 does full-file read |
| R3-5 | Token savings math unverified | Unchanged | "~6 tokens per line" still hand-wavy |
| R3-6 | Prose fallback omits `cut` | Unchanged | |
| R3-7 | AC1 and AC2 test same output stream | Unchanged | |
| R3-8 | Prevention comment not checked by AC | Unchanged | |
| R3-9 | Round numbering undefined | Unchanged | |
| R3-10 | Verification commands use placeholder path | Unchanged | |
| R3-11 | `tail -1` may capture trailing newline | Unchanged | |
| R3-12 | Verification commands label mismatch | Unchanged | |
| R4-1 | SKILL.md Step 2 NON-INTERACTIVE missing | Unchanged | Confirmed: SKILL.md Step 2 prompt starts at line 44 with no NON-INTERACTIVE |
| R4-2 | SKILL.md Step 3 trailer-first missing | Unchanged | Confirmed: SKILL.md Step 3 (line 112) says "I read the latest review round" |
| R4-3 | AC6 typo "Claudius" | Unchanged | Still "Claudius" in AC6 |
| R4-4 | Prevention comment AC missing | Unchanged | No AC verifies the warning comment |
| R4-5 | Plan never explicitly says "edit SKILL.md" | Unchanged | Changes described but not instructed |
| R4-6 | Prose fallback omits `cut` | Unchanged | Still not specified |
| R4-7 | Verification commands AC5/AC6 mismatch | Unchanged | |
| R4-8 | Token savings hand-wavy | Unchanged | |
| R4-9 | "Lines 14–153" conflates two numbering systems | Unchanged | Still ambiguous |
| R4-10 | `tail -1` trailing newline issue | Unchanged | |
| R4-11 | Round numbering undefined (4th round) | Unchanged | |
| R4-12 | Placeholder path in verification commands | Unchanged | |

### Issues

#### Issue 1 (Critical): SKILL.md Step 2 is unchanged — NON-INTERACTIVE requirement is absent
**Location**: `skills/plan-review/SKILL.md`, Step 2 prompt block (lines 44–99)
The plan Section 2 mandates `NON-INTERACTIVE` as the first line of the reviewer prompt AND in the Requirements block. Reading `skills/plan-review/SKILL.md` confirms: line 44 is `Read the contents of {plan-file-path}...` with no `NON-INTERACTIVE` preceding it. The Requirements block (lines 47–51) contains no `NON-INTERACTIVE` entry. This has been flagged in R3-3, R4-1, and R4-4 and remains unfixed after 4 rounds. Without editing SKILL.md, the skill does not enforce non-interactive behavior regardless of what the plan says.
**Suggestion**: Add explicit edit instruction in the plan at Section 2: "Edit `skills/plan-review/SKILL.md`, Step 2 prompt block (lines 44–99): prepend `NON-INTERACTIVE: Complete this review autonomously. Do not ask questions or prompt for input.` as the absolute first line, AND add `- NON-INTERACTIVE: do not ask clarifying questions at any point` as the first item in the Requirements block."

#### Issue 2 (Critical): SKILL.md Step 3 is unchanged — trailer-first grep approach is absent
**Location**: `skills/plan-review/SKILL.md`, Step 3 (lines 112–117)
The plan Section 4 prescribes a two-phase approach (grep `CONSENSUS_STATUS=` first, then conditionally read full file). Reading the actual SKILL.md shows Step 3 (line 112) says only "After the agent finishes, I read the latest review round in the review file" with no mention of grep first or conditional reading. This has been flagged in R3-4 and R4-2 and remains unfixed after 4 rounds. AC6 ("Claude's Step 3 greps the trailer") cannot be satisfied until SKILL.md Step 3 is updated.
**Suggestion**: Add explicit edit instruction in the plan at Section 4: "Edit `skills/plan-review/SKILL.md` Step 3 (lines 112–117): replace 'I read the latest review round in the review file' with the two-phase bash approach from plan Section 4, specifying the grep command and that full-file read is skipped on APPROVED."

#### Issue 3 (High): AC6 typo — "Claudius" instead of "Claude's"
**Location**: Acceptance Criteria, line 151
AC6 reads "Claudius Step 3 greps the trailer before reading the full file". This typo has persisted through R4-3 with no fix. "Claudius" is not a recognized entity in the workflow; it should be "Claude's".
**Suggestion**: Change line 151 to: `- [ ] Claude's Step 3 greps the trailer before reading the full file; skips full-file read on APPROVED`

#### Issue 4 (High): Prevention comment acceptance criterion is described but does not exist in AC list
**Location**: Acceptance Criteria section vs. Section 1 Prevention (line 85)
Section 1 Fix description says to add a warning comment above `usage()`. This has been flagged in R3-8, R4-4 and remains absent from the AC list. An implementer could skip the comment and still satisfy all ACs.
**Suggestion**: Add to Acceptance Criteria after AC7: `- [ ] A # WARNING: Do not embed external file content inside this heredoc. comment is present directly above the usage() function in ask_opencode.sh`

#### Issue 5 (High): Plan never explicitly instructs to edit SKILL.md — changes described but not commanded
**Location**: Throughout plan — Sections 2 and 4 describe changes but don't instruct edits
The Scope section says "Add non-interactive instruction to the reviewer prompt in plan-review/SKILL.md" and "Add machine-readable CONSENSUS_STATUS trailer" — but these are descriptions of goals, not implementation instructions. An implementer could read the plan, fix `ask_opencode.sh`, and believe the plan is complete without touching SKILL.md. This has been flagged as R4-5 and remains unaddressed.
**Suggestion**: Add an "Implementation" section at the top of Changes Required clarifying that three files need edits: (1) `skills/opencode/scripts/ask_opencode.sh` (heredoc fix), (2) `skills/plan-review/SKILL.md` Step 2 (NON-INTERACTIVE), (3) `skills/plan-review/SKILL.md` Step 3 (trailer-first).

#### Issue 6 (Medium): Prose fallback in Section 4 still omits `cut -d= -f2`
**Location**: Section 4 / Fallback (line 129)
The bash snippet correctly uses `cut -d= -f2`. The prose fallback says "If empty or unrecognized → NEEDS_REVISION" without referencing `cut`. This has been flagged in R2-4, R3-6, R4-6 and remains unfixed after 4 rounds. Someone implementing from prose alone will compare the full `CONSENSUS_STATUS=VALUE` string, which never matches.
**Suggestion**: Change prose fallback to: `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2); if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then status="NEEDS_REVISION"; fi`

#### Issue 7 (Medium): Verification command comments reference AC5/AC6 but Acceptance Criteria have no AC5/AC6
**Location**: Verification commands (lines 170, 173)
The verification command comments reference "AC5" and "AC6", but the Acceptance Criteria list (lines 149–155) contains items labeled AC1 through AC7 — with no AC5 or AC6. The mismatch has been flagged in R3-12 and R4-7 and persists.
**Suggestion**: Make all verification command comment prefixes match actual AC checkbox labels. Alternatively, add an introductory sentence to the Verification Commands section explicitly mapping each command to its corresponding AC number.

#### Issue 8 (Medium): Token savings estimate uses hand-wavy math and conflates line-count with token-count
**Location**: "Estimated token savings" (line 10)
The estimate reads "~140 lines × ~6 tokens = ~840 tokens" but then revises to "~140 lines × ~10–13 words × 1.3 tokens/word ≈ 1,800 tokens". These are contradictory and the "~" hedge makes both purely illustrative. This has been flagged in R1-9, R3-5, R4-8 and remains unverified after 4 rounds.
**Suggestion**: Run `ask_opencode.sh --help 2>&1 | wc -l` and `ask_opencode.sh --unknown-flag 2>&1 | wc -l` to get actual line counts, then convert to estimated tokens (1 token ≈ 4 chars or ~0.75 words). Replace with measured numbers.

#### Issue 9 (Medium): "Lines 14–153" in Background still conflates heredoc-internal positions with file line numbers
**Location**: Background (line 16)
The Background says "Lines 14–153 are the full content of plan-review/README.md accidentally embedded". In `ask_opencode.sh`, the heredoc opens at line 5 and closes at line 208. The numbers 14–153 are heredoc-internal positions (counting from line 6 inside the heredoc as position 1). A developer counting file lines 14–153 literally finds mermaid diagram code, not README prose. This has been flagged in R3-1, R3-9, R4-9 and remains confusing.
**Suggestion**: Change Background line 16 to: "Lines 14–153 (heredoc-internal positions; the embedded content spans approximately file lines 14–102, 103–153, and 154–208) contain plan-review/README.md content repeated three times (~138 lines total)."

#### Issue 10 (Medium): `tail -1` verification for AC5 may return trailing newline
**Location**: Verification commands / AC5 (line 170)
`tail -1 reviews/... | grep "^CONSENSUS_STATUS="` fails when the file ends with `CONSENSUS_STATUS=NEEDS_REVISION\n` because `tail -1` returns the final line including its trailing newline, which `grep` does not match. This has been flagged in R3-11 and R4-10 and remains unfixed.
**Suggestion**: Change AC5 verification to: `grep -v "^$" < reviews/2026-04-07-improve-plan-review-token-minimization-review.md | tail -1 | grep "^CONSENSUS_STATUS="` — strips blank lines before `tail` to ensure the last non-empty line is tested.

#### Issue 11 (Medium): Round numbering convention still undefined after 4 rounds
**Location**: SKILL.md format template and plan round references
The SKILL.md format template uses `## Round {N} — {YYYY-MM-DD}` but neither document specifies how N is computed. If two review sessions append concurrently or someone manually edits the file, N drifts. This has been flagged in R1-6, R2-5, R3-9, R4-11 and remains unaddressed after 4 rounds.
**Suggestion**: Define N in the SKILL.md format template section: "N = number of `---` separators in the file + 1, starting at 1. Round numbers are cosmetic — the authoritative iteration signal is the CONSENSUS_STATUS= trailer."

#### Issue 12 (Low): Verification commands use placeholder path `reviews/<topic>-review.md`
**Location**: Verification commands / AC5 and AC6 (lines 170, 173)
Both commands show `reviews/<topic>-review.md` as the path. Using the actual file name (`reviews/2026-04-07-improve-plan-review-token-minimization-review.md`) would make commands immediately runnable. This has been flagged in R3-10 and R4-12 and remains unchanged.
**Suggestion**: Replace all `reviews/<topic>-review.md` with `reviews/2026-04-07-improve-plan-review-token-minimization-review.md` in verification commands.

### Positive Aspects
- Target heredoc structure (lines 44–83) is complete and correct — replacement block is well-specified and implementable
- CONSENSUS_STATUS contract, fallback behavior, and two-phase grep approach are all sound in the plan text
- Verification commands are concrete and actionable for most criteria
- The heredoc corruption is confirmed present in `ask_opencode.sh` (lines 14–153 embed README content) — fixing it will definitely reduce token noise
- Scope boundaries remain well-defined, preventing feature creep

### Summary

**Top 3 key issues:**
1. **SKILL.md Step 2 and Step 3 are unchanged after 4 rounds** — the NON-INTERACTIVE requirement and trailer-first grep exist only in plan text; the actual skill files are untouched
2. **Prevention comment has no acceptance criterion** — the warning comment above `usage()` is described in the fix but has no checkbox to verify it; it could be silently dropped during implementation
3. **AC6 typo ("Claudius") and missing explicit "edit SKILL.md" instruction** — the typo is minor but has persisted 4 rounds; more critically, the plan never says "edit SKILL.md" so implementation may be incomplete

**Consensus Status**: NEEDS_REVISION

CONSENSUS_STATUS=MOSTLY_GOOD

---

## Round 6 — 2026-04-07

### Overall Assessment
The plan is in excellent shape after six rounds. The heredoc fix, CONSENSUS_STATUS contract, fallback logic, two-phase grep approach, and all acceptance criteria are correctly specified. The majority of issues raised in R4 and R5 are already fixed in the current plan text. The only substantive gap is incomplete verification command coverage (AC4, AC7, AC8 lack commands), and one minor math error in the token estimate.
**Rating**: 8.5/10

### Previous Round Tracking

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| R1-1 | Heredoc fix shows WHAT to remove, not what to KEEP | Fixed | Fix section (line 42) now says "Replace the entire body"; target structure is complete |
| R1-2 | grep command logically broken | Fixed | `grep ... \| tail -1 \| cut -d= -f2` is correct (line 136) |
| R1-3 | No verification/test plan | Fixed | Verification commands section added (lines 158–178) |
| R1-4 | NON-INTERACTIVE placement ambiguous | Fixed | Two-point placement shown in plan (lines 98, 103); Section 2 header says "Edit..." |
| R1-5 | No missing/invalid CONSENSUS_STATUS handling | Fixed | Contract and Fallback well-specified (lines 122–124) |
| R1-6 | Round numbering not defined | Suggestion | Out of scope per plan author; acceptable to note as Low |
| R1-7 | Script option completeness not verified | Fixed | AC3 + AC4 verify flags (lines 151–152) |
| R1-8 | Step 3 vague on when to skip full-file read | Fixed | Explicit skip-on-APPROVED in plan (lines 142–144) |
| R1-9 | Token savings estimate missing/hand-wavy | Partially Fixed | "~700–1,800 tokens" range stated (line 10); math contains error |
| R1-10 | No root cause / prevention mechanism | Fixed | Prevention comment (line 85) + AC8 (line 156) |
| R2-1 | Heredoc closing USAGE delimiter missing | Fixed | Target structure ends with `USAGE` (line 81) |
| R2-2 | "Remove lines 14–153" contradicts target structure | Fixed | Fix section (line 42) now says "Replace"; contradiction resolved |
| R2-3 | `--badarg` not recognized | Fixed | `--unknown-flag` is correct (lines 150, 168) |
| R2-4 | Prose fallback omits `cut` | Fixed | Fallback now shows `cut -d= -f2` extraction (line 124) |
| R2-5 | Round numbering undefined | Unchanged | Out of scope; SKILL.md formatting detail |
| R2-6 | Verification commands section header orphaned | Fixed | Intro sentence added (line 160) |
| R2-7 | Prevention mechanism not specified | Fixed | AC8 added (line 156) |
| R3-1 | Heredoc fix uses two line-numbering systems | Fixed | Line 16 clarifies "heredoc-internal positions"; line 40 note added |
| R3-2 | "Remove lines 14–153" still in Fix instruction | Fixed | "Replace" language used throughout (line 42) |
| R3-3 | SKILL.md Step 2 NON-INTERACTIVE missing | Fixed | Section 2 header: "Edit skills/plan-review/SKILL.md, Step 2 prompt block" |
| R3-4 | SKILL.md Step 3 trailer-first approach missing | Fixed | Section 4 header: "Edit skills/plan-review/SKILL.md, Step 3" |
| R3-5 | Token savings math unverified | Partially Fixed | Range stated; math error remains |
| R3-6 | Prose fallback omits `cut` | Fixed | Line 124 Fallback shows full extraction |
| R3-7 | AC1 and AC2 test same output stream | Suggestion | `2>&1` used for both; informational only |
| R3-8 | Prevention comment not checked by AC | Fixed | AC8 verifies warning comment (line 156) |
| R3-9 | Round numbering undefined | Unchanged | Out of scope |
| R3-10 | Verification commands use placeholder path | Fixed | Actual path used (lines 174, 177) |
| R3-11 | `tail -1` may capture trailing newline | Fixed | `grep -v "^$" \| tail -1` used (line 174) |
| R3-12 | Verification commands label mismatch | Fixed | AC1/AC2/AC3/AC5/AC6 align with Acceptance Criteria |
| R4-1 | SKILL.md Step 2 NON-INTERACTIVE missing | Fixed | Section 2 header explicitly says "Edit..." |
| R4-2 | SKILL.md Step 3 trailer-first missing | Fixed | Section 4 header explicitly says "Edit..." |
| R4-3 | AC6 typo "Claudius" | Fixed | Line 154 now reads "Claude's Step 3" |
| R4-4 | Prevention comment AC missing | Fixed | AC8 present (line 156) |
| R4-5 | Plan never explicitly says "edit SKILL.md" | Fixed | All SKILL.md sections now have "Edit..." in header |
| R4-6 | Prose fallback omits `cut` | Fixed | Line 124 shows `cut -d= -f2` |
| R4-7 | Verification commands AC5/AC6 mismatch | Fixed | Numbering aligns |
| R4-8 | Token savings hand-wavy | Partially Fixed | Range given; math error present |
| R4-9 | "Lines 14–153" conflates two numbering systems | Fixed | "heredoc-internal positions" clarified (line 16) |
| R4-10 | `tail -1` trailing newline issue | Fixed | `grep -v "^$" \| tail -1` at line 174 |
| R4-11 | Round numbering undefined | Unchanged | Out of scope |
| R4-12 | Placeholder path in verification commands | Fixed | Actual path at lines 174, 177 |

### Issues

#### Issue 1 (Medium): Token savings math contains a clear arithmetic error
**Location**: Line 10 — `~140 lines × ~10–13 words × 1.3 tokens/word ≈ 1,800 tokens`
The stated math is internally inconsistent. Working backward: if 1,800 tokens ÷ (1.3 tokens/word × ~11.5 words/line average) = ~120 lines — not 140. At the high end of the stated range (13 words × 1.3 = 16.9 tokens/line × 140 lines = 2,366 tokens). The figure "1,800 tokens" is only reachable if the heredoc has ~138 words per line, which is implausible. The "~700–1,800 tokens depending on model" range is plausible (different models have different tokenization rates), but the inline math breaks down and undermines confidence in the estimate.
**Suggestion**: Replace the inline calculation with either: (a) a simpler statement — "~700–1,800 tokens per error event, depending on model" — without the broken arithmetic, or (b) a byte-count based estimate: "~{N} bytes of heredoc output ÷ 4 chars/token ≈ {M} tokens".

#### Issue 2 (Medium): Verification commands do not cover AC4, AC7, or AC8
**Location**: Verification commands section (lines 162–178)
The 8 acceptance criteria have corresponding verification commands for only 5 of them (AC1, AC2, AC3, AC5, AC6). Missing:
- **AC4** (`NON-INTERACTIVE` as first line + in Requirements): No command to verify this. An implementer cannot automatically confirm AC4 was properly inserted into SKILL.md.
- **AC7** (Fallback to `NEEDS_REVISION` when trailer absent): No command to test the fallback behavior.
- **AC8** (Warning comment above `usage()`): No command to grep for the comment string. While AC8 could theoretically be verified with `grep "WARNING.*heredoc" ask_opencode.sh`, no such command is provided.
Without verification commands for all ACs, an implementer cannot fully validate compliance.
**Suggestion**: Add three verification commands:
```bash
# AC4: NON-INTERACTIVE present in SKILL.md Step 2
grep -m1 "^NON-INTERACTIVE" skills/plan-review/SKILL.md    # expected: NON-INTERACTIVE

# AC7: fallback behavior is documented in SKILL.md Step 3
grep "NEEDS_REVISION" skills/plan-review/SKILL.md           # expected: non-empty

# AC8: warning comment present above usage() function
grep -m1 "WARNING.*heredoc" skills/opencode/scripts/ask_opencode.sh
```

#### Issue 3 (Low): SKILL.md editing instructions do not specify precise line ranges or what to delete
**Location**: Sections 2, 3, 4 — "File: Edit `skills/plan-review/SKILL.md`..."
The plan instructs to edit SKILL.md Step 2 (prompt block), Step 2 format template, and Step 3, but does not provide: (a) the exact line range to replace within SKILL.md, (b) the precise text to remove before inserting the new content. The example prompt block in Section 2 (lines 97–106) shows the target content but an implementer must infer where in SKILL.md the existing content lives and what to delete. Given that SKILL.md has not been modified yet, the plan cannot provide line numbers from the current file — but it could say "replace everything between `Requirements:` and the next `###` heading in Step 2" or similar.
**Suggestion**: Add a scope界定 to each SKILL.md edit instruction: "Replace the existing prompt block in Step 2 with the content above" (Section 2), "Add the trailer requirement to the Step 2 format template" (Section 3), "Replace the Step 3 prose with the bash code above" (Section 4). The current language is close to sufficient but could eliminate ambiguity.

#### Issue 4 (Suggestion): Section 3 header says "Edit `skills/plan-review/SKILL.md`, Step 2 format template" but Step 3 is the trailer section
**Location**: Line 110 — header reads "Edit `skills/plan-review/SKILL.md`, Step 2 format template" for the CONSENSUS_STATUS trailer change
The trailer (CONSENSUS_STATUS) is logically part of the review format output by the reviewer, not a modification to the Step 2 prompt block itself. The Step 3 modification (the two-phase bash approach) is also about how the operator reads the review. Having Section 3 be about the format template while Section 4 is about Step 3 creates a mismatch between header numbering and SKILL.md step numbers.
**Suggestion**: Renumber the sections to align with SKILL.md steps: Section 2 = Step 2 prompt changes (NON-INTERACTIVE), Section 3 = Step 2 format template changes (CONSENSUS_STATUS trailer), Section 4 = Step 3 changes (two-phase grep). The current Section 3 header could be clarified to say "Edit `skills/plan-review/SKILL.md`, Step 2 format template (append CONSENSUS_STATUS trailer)".

### Positive Aspects
- Heredoc fix is complete and unambiguous: target structure shows full `usage()` function with closing `USAGE` delimiter, "replace" language used throughout, heredoc-internal vs file line numbers clarified
- CONSENSUS_STATUS contract, fallback with `cut -d= -f2`, and two-phase grep approach are all correctly specified and implementable
- All major issues from R4/R5 are confirmed fixed in the current plan text: AC6 typo, AC8 (prevention comment), "Edit SKILL.md" instructions, trailing newline handling, placeholder paths, "heredoc-internal positions" clarification
- Acceptance criteria are well-formed and testable (AC1–AC8)
- Verification commands are runnable and use the correct actual file paths; trailing newline fix (`grep -v "^$" | tail -1`) is correct

### Summary

**Top 3 key issues:**
1. **Token estimate math is broken** — "~140 lines × ~10–13 words × 1.3 tokens/word ≈ 1,800 tokens" doesn't compute; either remove the inline calculation or fix the arithmetic
2. **Verification commands don't cover AC4, AC7, AC8** — 3 of 8 acceptance criteria have no corresponding test command; implementer cannot fully validate compliance
3. **SKILL.md edit instructions are close but not precise** — "Edit Step 2 prompt block" lacks scope界定 (what exactly to replace); could be clearer about deletion boundaries

**Consensus Status**: MOSTLY_GOOD

CONSENSUS_STATUS=MOSTLY_GOOD

---

## Round 2 — 2026-04-07

### Overall Assessment
The plan has materially improved from Round 1 — the heredoc target structure, grep command, verification commands, NON-INTERACTIVE placement, CONSENSUS_STATUS contract, and token savings estimate are all now correctly specified. However, critical structural issues remain: the heredoc's closing `USAGE` delimiter is missing from the target structure, the relationship between "remove lines 14–153" and the target structure is contradictory, and the `--badarg` test uses an invalid flag that opencode does not recognize.
**Rating**: 6/10

### Previous Round Tracking

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| 1 | Heredoc fix shows WHAT to remove, not what to KEEP | Partially Fixed | Target structure added (lines 44–79), but closing `USAGE` delimiter not shown; heredoc still ends at line 208 which is outside the target structure window |
| 2 | grep command logically broken | Fixed | Now uses `grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2` — correct |
| 3 | No verification/test plan | Fixed | Verification commands subsection added (lines 146–161) |
| 4 | NON-INTERACTIVE placement ambiguous | Fixed | Shows exact two-point placement (top + Requirements) |
| 5 | No missing/invalid CONSENSUS_STATUS handling | Fixed | Contract and Fallback defined (lines 114–116) |
| 6 | Round numbering not defined | Unchanged | Still not addressed |
| 7 | Script option completeness not verified | Partially Fixed | AC3 now lists flags, but actual content verification not confirmed |
| 8 | Step 3 vague on when to skip full-file read | Fixed | Now explicitly says skip on APPROVED |
| 9 | Token savings estimate missing | Fixed | "~840 tokens eliminated per error event" added (line 10) |
| 10 | No root cause / prevention mechanism | Partially Fixed | Copy-paste/merge error hypothesis added to Background (line 16); prevention in CI still absent |

### Issues

#### Issue 1 (Critical): Heredoc target structure missing closing `USAGE` delimiter
**Location**: Section 1 / "Target structure" (lines 44–79)
The target structure shows the heredoc content but stops at line 79 with no indication of where the heredoc actually closes. The original heredoc closes at line 208 with a bare `USAGE` on its own line. The target structure as shown would leave the heredoc unclosed or would require the developer to know to add a closing `USAGE` delimiter that is not visible in the target. This creates ambiguity: does the developer simply delete lines 14–153 and leave the rest (154–208) intact? Or does the target structure replace the entire heredoc body including the closing delimiter?
**Suggestion**: Add `USAGE` as the final line of the target structure code block (after line 79 content) to make the closing delimiter explicit. Also clarify whether lines 154–208 (the Options section that was apparently legitimate content) are preserved by the fix or replaced.

#### Issue 2 (Critical): "Remove lines 14–153" contradicts the target structure approach
**Location**: Section 1 / "Fix" vs "Target structure"
The Fix line says "Remove lines 14–153" but the Target structure (lines 44–79) starts at line 46 with `Usage:` — which is *inside* the range being removed (lines 14–153). This means the target structure is not simply what remains after deletion; it is a replacement block that must be inserted. The plan never explicitly states "replace lines 14–153 with the following content." A developer reading "remove lines 14–153" might literally delete only, leaving a malformed heredoc.
**Suggestion**: Change the Fix instruction from "Remove lines 14–153" to "Replace lines 14–153 with the target structure below" and reframe the target structure as an insertion replacement rather than a before/after diff.

#### Issue 3 (High): `--badarg` is not a recognized opencode flag
**Location**: "Verification commands" / AC2 (line 151)
The verification command `ask_opencode.sh --badarg 2>&1 | grep -c "Plan Review"` uses `--badarg` as a trigger for an argument error. However, `ask_opencode.sh` may not recognize `--badarg` as invalid in the same way it handles truly malformed input — it may treat it as a positional `<task>` argument rather than a flag error. This means the test might not actually trigger the `usage >&2` error path at all, causing the verification to pass incorrectly (false negative).
**Suggestion**: Replace `--badarg` with a flag that is unambiguously invalid and guaranteed to trigger the usage error path. For example, `ask_opencode.sh --invalid-option-name 2>&1` or test with an empty task + known-bad flag combination. Alternatively, if the script's argument parsing is lenient, trigger the error by passing a flag that requires a value without providing one (e.g., `-t` with no argument).

#### Issue 4 (Medium): Step 3 bash code uses `cut` but fallback prose does not
**Location**: Section 4 / Fix (lines 126–134)
The bash code snippet shows `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2)` which correctly extracts the value after `=`. However, the prose fallback (line 129) says `If empty or unrecognized → NEEDS_REVISION` without referencing `cut`. If someone implements the fallback by copy-pasting only the prose (not the bash snippet), they will get the full `CONSENSUS_STATUS=VALUE` string instead of just `VALUE`, causing string comparison failures.
**Suggestion**: Make the fallback prose consistent with the bash snippet: `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2); if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then status="NEEDS_REVISION"; fi`

#### Issue 5 (Medium): Round numbering convention still undefined
**Location**: "Previous Round Tracking" table + Round N references throughout
Round 1 left this unaddressed. The table format in the SKILL.md says `## Round {N} — {YYYY-MM-DD}` but the plan never specifies how N is computed. If two plan-review sessions run concurrently on the same plan file and someone manually adds a round, N could drift. Using timestamps (`Round 2026-04-07T10:30:00Z`) instead of sequential integers would be unambiguous and conflict-free.
**Suggestion**: Define N as `$(grep -c "^---" "$review_file")` (count of round separators) or replace sequential N with an ISO-8601 timestamp to eliminate ambiguity.

#### Issue 6 (Low): `Verification commands` section header is orphaned in output
**Location**: "Acceptance Criteria" section / line 146
The `### Verification commands` heading appears after the checkbox list but before the code block, with no prose explanation of what to do with the commands. A developer implementing this plan might not understand whether these are automated tests to run or manual commands to verify.
**Suggestion**: Add a brief intro sentence: "Run these commands after implementation to verify each acceptance criterion:"

#### Issue 7 (Low): Prevention mechanism for heredoc re-corruption not specified
**Location**: "Background" and "Scope" sections
Round 1 Issue 10 pointed this out. The plan now explains the likely cause (copy-paste/merge error, line 16) but still has no prevention measure. Without a CI check or a simple line-count/sanity check in the script, the heredoc could become corrupted again.
**Suggestion**: Add an acceptance criterion like: `[ ] CI checks that `ask_opencode.sh --help` output is < 30 lines` or add a comment in the script itself alerting maintainers not to embed large blocks inside the heredoc.

### Positive Aspects
- Token savings estimate now included (~840 tokens per error event)
- grep command correctly implemented with quoted variables and proper `tail -1`
- Verification commands section is concrete and actionable for most criteria
- CONSENSUS_STATUS contract and fallback behavior are well-specified
- NON-INTERACTIVE instruction placement is now explicit and redundant
- Round tracking table format in SKILL.md is sound

### Summary

**Top 3 key issues:**
1. **Heredoc closing delimiter missing** — target structure shows no `USAGE` closing line; developer cannot confirm where heredoc ends
2. **"Remove lines 14–153" vs target structure contradiction** — the fix instruction and target structure are logically inconsistent; replacement not clearly defined as such
3. **`--badarg` may not trigger the error path** — verification test may produce false negatives; needs a reliably invalid flag

**Consensus Status**: NEEDS_REVISION
CONSENSUS_STATUS=NEEDS_REVISION
