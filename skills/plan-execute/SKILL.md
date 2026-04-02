---
name: plan-execute
description: Use when the user says "/plan-execute", "plan execute", "implement plan", or "execute plan" and provides a finalized plan file path to carry out. Claude orchestrates, the coding agent writes code, Claude reviews, and the coding agent fixes issues until the quality bar is met. Specify a coding agent provider inline (e.g., "opencode") to override the default "codex" agent.
---

# Plan Execute Skill

## Purpose

When the user runs `/plan-execute [{provider}] {plan-file-path}`, start the "orchestrated plan execution" workflow:
1. I (Claude Code) ask the coding agent to implement the code according to the plan.
2. After the agent finishes, I review the generated code.
3. I write the review into the `reviews/` directory, then ask the agent to inspect and fix the issues.
4. Repeat until the code quality bar is met.

**Provider**: defaults to `codex`, override by specifying a provider inline (e.g., `opencode`) before the plan path.

**Core principle: I do not write or edit code myself. I only do two things: review code and orchestrate the coding agent. All code changes, including implementation and fixes, are performed by the agent.**

## Usage

```
/plan-execute plans/my-feature-plan.md
/plan-execute opencode plans/my-feature-plan.md
```

## Session Reuse

After each coding agent invocation, extract `session_id=xxx` from the script output and save it as the session ID for the current task. In later calls for the same task, pass `--session <id>` to reuse context so the agent remembers prior implementation and fix history instead of rereading the entire codebase every time.

## My Workflow (Claude Code)

### Step 1: Read the Plan and Split Execution Steps

Read the specified plan file and understand:
- The overall goal and scope of the plan
- The list of files to create or modify
- The order of implementation steps
- Relevant project conventions, especially from `CLAUDE.md`

If the plan already contains a checklist (`- [ ]` / `- [x]`), use those items as execution units.
If it does not define clear steps, split the work into reasonable batches, with no more than 5 file changes per batch.

### Step 2: Ask the Agent to Implement the Code

Use the `/{provider}` skill (default: `/codex`) and give the agent the following instruction:

```
Implement the code according to the plan in {plan-file-path}.

Current execution scope: {specific step or batch description}

Requirements:
- Follow the design in the plan exactly. Do not improvise beyond it.
- Obey the Code Quality Hard Limits defined in `CLAUDE.md`.
- Single file <= 800 lines, single function <= 50 lines, nesting <= 3 levels
- Run `pnpm build` after implementation to confirm compilation succeeds
- If the plan includes a checklist, mark completed steps as `[x]`

After implementation, list all changed files and provide a summary of each change.
```

### Step 3: Review Agent Output (My Core Responsibility)

After the agent finishes, I perform a code review. **Important: I only read code and write reviews. I never directly modify source files.**

1. **Read every changed file** and review them one by one.
2. **Compare against the plan** to verify the implementation matches the intended design.
3. **Check code quality**, including:
   - Whether it violates the Code Quality Hard Limits
   - Whether it introduces security risks
   - Whether error handling is missing
   - Whether naming and organization are clear
   - Whether it follows existing project patterns
4. **Run `pnpm build`** to confirm the compilation status.

### Step 4: Write the Review and Hand Fixes Back to the Agent

Append the review to `reviews/{topic}-review.md` (shared with `plan-review`):

```markdown
---

## Code Review Round {N} — {YYYY-MM-DD}

**Scope**: {code scope covered in this review}
**Build Status**: PASS / FAIL

### Issues

#### Issue 1 ({severity}): {title}
**File**: {file-path:line}
{issue description}
**Fix**: {specific fix recommendation}

...

### Verdict: NEEDS_FIX / APPROVED
```

If `Verdict: NEEDS_FIX`, call `/{provider}` (default: `/codex`) and have the agent fix the issues instead of editing them myself:

```
Read the latest Code Review round in {review-file-path}.
Check each issue one by one. Fix the valid issues, and explain why any disputed item is not actually a problem.
After making fixes, run `pnpm build` to confirm compilation succeeds.
List the issues that were fixed and the corresponding code changes.
```

If `Verdict: APPROVED`, skip to Step 6.

### Step 5: Verify Fixes and Iterate

After the agent applies fixes, I review again, still without editing code directly:
- Check whether each issue was truly fixed
- Check whether the fixes introduced new problems
- If issues remain, write a new review round and hand it back to the agent for another fix pass (repeat Step 4)
- If everything passes, mark the review as `Verdict: APPROVED`

### Step 6: Update Plan Progress

After each batch is completed, ask the agent to update the checklist in the plan file (`- [ ]` -> `- [x]`).
If unfinished steps remain, go back to Step 2 for the next batch.
Once all work is complete, move to the wrap-up.

### Step 7: Wrap Up

Report the following to the user:
- Which steps were completed
- How many code review rounds were needed
- Which major issues were fixed
- Final build status
- List of changed files
- Path to the review log file

## Review Severity Levels

| Level | Meaning | Must Fix |
|-------|---------|----------|
| Critical | Causes runtime failures or security vulnerabilities | Yes |
| High | Violates project conventions or has obvious design flaws | Yes |
| Medium | Code quality issue that should be improved | Recommended |
| Low | Style or preference issue | Optional |
| Suggestion | Optimization suggestion | Optional |

**Verdict rules:**
- If any Critical or High issue exists -> `NEEDS_FIX`
- If all issues are Medium or below -> `APPROVED` with optional improvement notes

## File Convention

- Share the same review file as `plan-review`: `reviews/{topic}-review.md`
- `{topic}` is the plan file name without `.md`
- Both plan review rounds and code review rounds are appended to the same file
- Distinguish them by heading: `## Round {N}` for plan review and `## Code Review Round {N}` for code review
