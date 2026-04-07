---
name: plan-review
description: Use when the user says "/plan-review", "plan review", or "PRD review" and provides a plan file path that needs critical review and iterative refinement. Specify a coding agent provider inline (e.g., "opencode") to override the default "codex" agent.
---

# Plan Review Skill

## Purpose

When the user runs `/plan-review [{provider}] {plan-file-path}`, start the "adversarial plan iteration" workflow:
1. I (Claude Code) ask the coding agent to perform a critical review of the specified plan.
2. I read the review produced by the agent and evaluate whether its suggestions are sound.
3. I revise the plan based on valid suggestions and write changes back to the original plan file.
4. If the review status is `NEEDS_REVISION`, I automatically ask the agent to review again.
5. Repeat until consensus is reached as `MOSTLY_GOOD` or `APPROVED`.

**Provider**: defaults to `codex`, override by specifying a provider inline (e.g., `opencode`) before the plan path.

## Usage

```
/plan-review plans/my-feature-plan.md
/plan-review opencode plans/my-feature-plan.md
```

## Session Reuse

After each coding agent invocation, extract `session_id=xxx` from the script output and save it as the session ID for the current task. In later calls for the same task, pass `--session <id>` to reuse context so the agent remembers prior review history and can stay consistent across multiple rounds.

## My Workflow (Claude Code)

### Step 1: Determine the Review File

Derive the review file path from the plan file name:
- `plans/auth-refactor.md` → `reviews/auth-refactor-review.md`
- Rule: `reviews/{plan-file-name-without-.md}-review.md`

If the review file already exists, this is not the first round, so the reviewer must track the resolution status of issues from the previous round.

### Step 2: Ask the Reviewer to Review the Plan

Use the `/{provider}` skill (default: `/codex`) and give the reviewer the following instruction:

```
NON-INTERACTIVE: Complete this review autonomously. Do not ask questions or prompt for input.

Read the contents of {plan-file-path} and review it critically as an independent third-party reviewer.

Requirements:
- NON-INTERACTIVE: do not ask clarifying questions at any point
- Raise at least 10 concrete and actionable improvement points
- Each issue must include: issue description + exact location/reference in the plan + improvement suggestion
- Use severity levels: Critical > High > Medium > Low > Suggestion
- If {review-file-path} already exists, read it first and track the resolution status of previous issues in the new round

Analysis dimensions, choosing the relevant ones based on the plan type:
- Architectural soundness: overdesign vs underdesign, module boundaries, single responsibility
- Technology choices: rationale, alternatives, compatibility with the existing project stack
- Completeness: missing scenarios, overlooked edge cases, dependency and impact scope
- Feasibility: implementation complexity, performance risks, migration and compatibility concerns
- Engineering quality: whether it follows the Code Quality Hard Limits in `CLAUDE.md`
- User experience: interaction flow, error/loading states, i18n when relevant
- Security: authentication, authorization, data validation when relevant

Append the current review round to {review-file-path}, creating the file if it does not exist.
Separate rounds with `---` and append new rounds at the end of the file. Use this format:

---

## Round {N} — {YYYY-MM-DD}

### Overall Assessment
{2-3 sentence overall assessment}
**Rating**: {X}/10

### Previous Round Tracking (R2+ only)
| # | Issue | Status | Notes |
|---|-------|--------|-------|

### Issues
#### Issue 1 ({severity}): {title}
**Location**: {location in the plan}
{issue description}
**Suggestion**: {improvement suggestion}
... (at least 10 issues)

### Positive Aspects
- ...

### Summary
{Top 3 key issues}
**Consensus Status**: NEEDS_REVISION / MOSTLY_GOOD / APPROVED

**Key principle: be a critical reviewer, not a yes-man. Every issue must be specific enough that someone knows how to revise the plan.**

**Critical rules for the reviewer:**
1. **Always prioritize high severity issues first** — Critical and High severity issues must appear before Medium/Low/Suggestion issues
2. **List as many issues as possible** — Do not artificially limit to 10. If the plan has 20 issues, list 20. Quality of analysis matters more than arbitrary thresholds
3. **Maintain quality and confidence simultaneously** — Every issue must be actionable, specific, and evidence-based. Do not sacrifice specificity for quantity or vice versa
4. **Be adversarial** — Challenge assumptions, question decisions that lack rationale, and flag incomplete thinking even if it means more issues
5. **Distinguish severity honestly** — A Medium issue is not High just to hit quotas. Use severity labels accurately
CONSENSUS_STATUS=NEEDS_REVISION
```

When the review file is created for the first time, add this header at the top:

```markdown
# Plan Review: {plan title}

**Plan File**: {plan-file-path}
**Reviewer**: {provider} (default: Codex)
```

### Step 3: Read the Review and Revise the Plan

```bash
# Phase 1: decision (cheap — single grep)
status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2)
# Fallback: if empty or unrecognized value, default to NEEDS_REVISION
if [[ -z "$status" ]] || [[ ! "$status" =~ ^(NEEDS_REVISION|MOSTLY_GOOD|APPROVED)$ ]]; then
  status="NEEDS_REVISION"
fi

# Phase 2: read full file ONLY when revision is needed
# -> NEEDS_REVISION or MOSTLY_GOOD: read full review to evaluate issues and revise plan
# -> APPROVED: skip full-file read entirely
```

### Step 4: Decide Whether to Continue Iterating

Use the `Consensus Status` provided by the agent:

| Status | My Action |
|--------|---------|
| `NEEDS_REVISION` | Revise the plan, then automatically ask the agent to review again and return to Step 2 |
| `MOSTLY_GOOD` | Revise the plan, then tell the user the plan is mostly mature and ask whether another review round is needed |
| `APPROVED` | Tell the user the plan has passed review and is ready for implementation |

### Step 5: Wrap Up

After the iteration is complete, report the following to the user:
- How many review rounds were completed
- Which major areas were improved
- The final plan file path
- The review log file path

## File Convention

- One review file per plan: `reviews/{topic}-review.md`
- `{topic}` is the plan file name without `.md`
- Append all rounds to the same file and separate them with `---`
- Example: `plans/auth-refactor.md` -> `reviews/auth-refactor-review.md`
