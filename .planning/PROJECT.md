# Improve plan-review Token Minimization

## What This Is

Focused initiative to shrink plan-review token burn by fixing structural issues in the CLI helper script and the `plan-review` skill prompts. The work stream tightens CLI usage output, enforces non-interactive reviewer behavior, and encodes review outcomes so Claude can avoid re-reading entire files.

## Core Value

Plan-review cycles stay autonomous and inexpensive by minimizing redundant output while preserving review quality.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Restore the concise `usage()` block in `ask_opencode.sh`, ensuring help/errors surface only CLI guidance.
- [ ] Force non-interactive reviewer execution so reviews never pause for input mid-run.
- [ ] Append a machine-readable `CONSENSUS_STATUS=` trailer to each review round and define legal values.
- [ ] Teach Claude to grep the trailer (with fallback) before reading the full review log, skipping unnecessary reads on approval.

### Out of Scope

- Changes to other provider skills (codex, etc.) — this effort only touches plan-review + CLI.
- Structural redesign of the plan-review process beyond the consensus trailer contract.

## Context

ZenStudioLab/skills#1 pinned excessive stderr noise: a corrupted heredoc in `ask_opencode.sh` printed ~140 lines of README text per error, inflating every review iteration. Review prompts also lacked explicit "NON-INTERACTIVE" instructions, allowing opencode to request input. Finally, Claude had to re-read entire reviews to infer consensus. These frictions compound token costs and lead to hangs.

## Constraints

- **Compatibility**: Preserve existing CLI flags and behavior; help output must still describe all documented options.
- **Scope Guard**: Keep modifications within plan-review skill + `ask_opencode.sh`; broader workflow/UI changes are excluded.
- **Reliability**: Consensus trailer fallback must default to `NEEDS_REVISION` when missing or malformed to keep loops safe.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Prioritize CLI + skill edits over architectural overhaul | Quick wins cut hundreds of tokens per iteration without reworking review flow | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-07 after initialization*
