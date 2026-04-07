# Plan: Improve plan-review Token Minimization

## Objective

Reduce token usage in `plan-review` flows by:
1. Fixing a corrupted `usage()` heredoc in `ask_opencode.sh` (removes ~140 lines of stderr noise per error)
2. Enforcing non-interactive mode in the reviewer prompt (prevents hangs)
3. Adding a grep-able `CONSENSUS_STATUS=` trailer so Claude never reads the full review file just to decide whether to iterate

**Estimated token savings**: Current heredoc emits ~140 lines per error (~700–1,800 tokens depending on model; run `ask_opencode.sh --unknown-flag 2>&1 | wc -c` to get byte count, then divide by 4 for an estimate). After fix: CLI usage text only (~15 lines, ~75–150 tokens). Full review file reads (300–2,000+ tokens per round) reduced to a single grep for iteration decisions.

## Background

- **Issue**: ZenStudioLab/skills#1 — verbose stdout inflates token cost on every review round
- **Root causes identified** (from reading the actual files):
  1. `skills/opencode/scripts/ask_opencode.sh` — The `usage()` function contains a `cat <<'USAGE'` heredoc spanning lines 5–208 of the file. The heredoc body (heredoc-internal positions) contains the full content of `plan-review/README.md` accidentally embedded inside it (likely a copy-paste or editor merge error), inflating it to ~140–150 lines. Every argument error calls `usage >&2`, emitting this block to stderr which the script re-echoes and Claude reads back.
  2. `plan-review/SKILL.md` — reviewer prompt does not contain a non-interactive instruction; opencode may pause for input mid-review.
  3. `plan-review/SKILL.md` Step 3 — `Consensus Status` is buried in prose inside `### Summary`. Claude reads the entire review file (grows each round) just to extract a three-word decision.

## Scope

**In scope:**
- Fix corrupted `usage()` heredoc in `ask_opencode.sh`
- Add non-interactive instruction to the reviewer prompt in `plan-review/SKILL.md`
- Add machine-readable `CONSENSUS_STATUS=<VALUE>` trailer to the review format
- Update Claude's Step 3 guidance to grep the trailer instead of reading the full file
- Add fallback behavior when the trailer is absent or invalid

**Out of scope:**
- Changes to the `codex` skill or other providers
- Altering the review format structure beyond the status trailer
- UI/UX changes outside plan-review flow

## Changes Required

### 1. Fix `ask_opencode.sh` usage() heredoc corruption

**File**: `skills/opencode/scripts/ask_opencode.sh`

**Problem**: The `usage()` heredoc body (between `cat <<'USAGE'` and the closing `USAGE` delimiter) contains the full content of `plan-review/README.md` accidentally embedded inside it. This ~140-line block is printed on every argument error and `--help` call. (Note: "lines 14–153" in the Background refers to file-level line numbers at time of writing; use the target structure below as the authoritative reference — do not rely on line numbers.)

**Fix**: Replace the entire body of the heredoc (everything between `cat <<'USAGE'` and the closing `USAGE` delimiter) with the target structure below. Do not merely delete lines — confirm the replacement produces the exact output shown.

**Target structure** (complete heredoc body — `cat <<'USAGE'` … `USAGE`):
```bash
usage() {
  cat <<'USAGE'
Usage:
  ask_opencode.sh <task> [options]
  ask_opencode.sh -t <task> [options]

Task input:
  <task>                       First positional argument is the task text
  -t, --task <text>            Alias for positional task (backward compat)
  (stdin)                      Pipe task text via stdin if no arg/flag given

File context (optional, repeatable):
  -f, --file <path>            Priority file path

Multi-turn:
      --session <id>           Resume a previous session

Watch mode:
  -W, --watch                  Stream output to stdout while writing to files

Status:
      --status <session_id>    Check status of a running session

Options:
  -w, --workspace <path>       Workspace directory (default: current directory)
      --model <name>           Model override (format: provider/model)
      --agent <name>           Agent to use
      --reasoning <level>      Accepted for peer compatibility; currently ignored
  -o, --output <path>          Output file path
  -h, --help                   Show this help

Output (on success):
  session_id=<thread_id>       Use with --session for follow-up calls
  output_path=<file>           Path to response markdown
  status_path=<file>           Path to status file (while running)
USAGE
}
```

**Prevention**: Add a comment directly above the `usage()` function in the script warning maintainers not to embed large blocks inside the heredoc: `# WARNING: Do not embed external file content inside this heredoc.`

After the fix, verify that the following flags are still documented in the output: `-w/--workspace`, `-t/--task`, `-f/--file`, `-o/--output`, `--session`, `--model`, `--agent`, `--reasoning`, `-W/--watch`, `--status`.

### 2. Enforce non-interactive mode in the reviewer prompt

**File**: Edit `skills/plan-review/SKILL.md`, Step 2 prompt block

**Problem**: No instruction prevents opencode from pausing for input.

**Fix**: In SKILL.md, find the existing Step 2 prompt block (which begins with `Read the contents of {plan-file-path}...`). Replace the entire prompt block — from that opening line through the end of the Requirements list — with the content below. Add `NON-INTERACTIVE` as the absolute first line AND repeat it inside the Requirements block. Exact placement:

```
NON-INTERACTIVE: Complete this review autonomously. Do not ask questions or prompt for input.

Read the contents of {plan-file-path} and review it critically as an independent third-party reviewer.

Requirements:
- NON-INTERACTIVE: do not ask clarifying questions at any point
- Raise at least 10 concrete and actionable improvement points
...
```

### 3. Add machine-readable status trailer

**File**: Edit `skills/plan-review/SKILL.md`, Step 2 format template (the review output format block shown to the reviewer)

**Problem**: `Consensus Status` is prose-embedded; requires full-file read to extract.

**Fix**: In SKILL.md Step 2, find the format template block (the code block containing `## Round {N}`, `### Summary`, `**Consensus Status**: ...`). Append the `CONSENSUS_STATUS=` line as the **absolute last line** of that format template, so reviewers know to emit it after each round (no trailing newline, no content after it):

```
CONSENSUS_STATUS=NEEDS_REVISION
```

Valid values: `NEEDS_REVISION` | `MOSTLY_GOOD` | `APPROVED`

**Contract**: The trailer must be a standalone line matching `^CONSENSUS_STATUS=(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$`. No other content may follow it in the file.

**Fallback**: Extract the value with `status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2)`. If `$status` is empty or not one of the three valid values, treat as `NEEDS_REVISION`. The `cut -d= -f2` is required — without it the comparison is against the full `CONSENSUS_STATUS=VALUE` string, which never matches.

### 4. Update Claude's Step 3 guidance to use the trailer

**File**: Edit `skills/plan-review/SKILL.md`, Step 3

**Problem**: Step 3 tells Claude to "read the latest review round in the review file" — causing full-file reads every iteration.

**Fix**: In SKILL.md, find the existing Step 3 section (which begins with "After the agent finishes, I read the latest review round in the review file"). Replace that prose with the two-phase approach below:

```bash
# Phase 1: decision (cheap — single grep)
status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2)
# Fallback: if empty or unrecognized value, default to NEEDS_REVISION
if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then
  status="NEEDS_REVISION"
fi

# Phase 2: read full file ONLY when revision is needed
# → NEEDS_REVISION or MOSTLY_GOOD: read full review to evaluate issues and revise plan
# → APPROVED: skip full-file read entirely
```

## Acceptance Criteria

- [ ] `ask_opencode.sh --help` outputs only CLI usage text; no README content
- [ ] Triggering an argument error (`ask_opencode.sh --unknown-flag`) emits only usage text to stderr, no README content
- [ ] All flags (`-w`, `--workspace`, `-t`, `--task`, `-f`, `--file`, `--session`, `--model`, `-W`, `--watch`, `--status`) remain documented in help output
- [ ] Reviewer prompt contains `NON-INTERACTIVE` as first line and inside Requirements
- [ ] Every review round ends with `CONSENSUS_STATUS=<VALUE>` as the last line of the file
- [ ] Claude's Step 3 greps the trailer before reading the full file; skips full-file read on `APPROVED`
- [ ] Fallback to `NEEDS_REVISION` when trailer is absent or unrecognized
- [ ] A `# WARNING: Do not embed external file content inside this heredoc.` comment is present directly above the `usage()` function in `ask_opencode.sh`

### Verification commands

Run these commands after implementation to verify each acceptance criterion:

```bash
# AC1: --help outputs only CLI usage text
ask_opencode.sh --help 2>&1 | grep -c "Plan Review"           # expected: 0

# AC2: argument errors don't echo README content
# --unknown-flag reliably triggers the unknown-option error path (line 333 of script)
ask_opencode.sh --unknown-flag 2>&1 | grep -c "Plan Review"   # expected: 0

# AC3: all flags still documented
ask_opencode.sh --help 2>&1 | grep -E "\-\-workspace|\-\-task|\-\-file|\-\-output|\-\-session|\-\-model|\-\-watch|\-\-status"

# AC4: NON-INTERACTIVE present as first line and in Requirements in SKILL.md Step 2
grep -m1 "^NON-INTERACTIVE" skills/plan-review/SKILL.md    # expected: NON-INTERACTIVE: Complete this review...

# AC5: trailer present after a review run (strips trailing blank lines before tail)
grep -v "^$" reviews/2026-04-07-improve-plan-review-token-minimization-review.md | tail -1 | grep "^CONSENSUS_STATUS="

# AC6: grep correctly returns last-round status (not first-round)
grep "^CONSENSUS_STATUS=" reviews/2026-04-07-improve-plan-review-token-minimization-review.md | tail -1

# AC7: fallback documented in SKILL.md Step 3
grep "NEEDS_REVISION" skills/plan-review/SKILL.md | grep -i "fallback\|empty\|default\|absent"  # expected: non-empty

# AC8: warning comment present above usage() in ask_opencode.sh
grep "WARNING.*heredoc" skills/opencode/scripts/ask_opencode.sh    # expected: # WARNING: Do not embed...
```

## Traceability

- Issue: ZenStudioLab/skills#1
