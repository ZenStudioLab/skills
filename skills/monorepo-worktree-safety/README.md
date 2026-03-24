# Monorepo Worktree Safety

Prevents dependency resolution failures and test discovery disasters when using git worktrees inside monorepos or submodules.

## Overview

Git worktrees are a powerful workflow tool — they give you an isolated checkout of a different branch without needing to stash or clone again. But in monorepos with workspace-relative packages, a worktree created inside a submodule can silently inherit the wrong (or no) `node_modules`, causing test failures that look like code regressions.

This skill provides:
- A verification script that audits the current worktree context
- A decision tree for choosing the correct execution context
- Concrete remediation steps for each failure class
- An output report contract so the agent always communicates what it found and fixed

## Common Failure Modes

| Symptom | Root Cause |
|---|---|
| `vitest: not found` | Worktree has no `node_modules`, no PATH resolution |
| `Cannot find module '@org/utils'` | Workspace package not resolvable from registry |
| Tests running from wrong branch | `.worktrees/**` not excluded from test discovery |
| Duplicate React / store | `node_modules` symlink creates two singleton instances |
| Untracked files everywhere | `.worktrees/` not in `.gitignore` |

## Installation

```bash
npx skills add ZenStudioLab/skills --skill monorepo-worktree-safety
```

Or manually copy `skills/monorepo-worktree-safety/` to `~/.agents/skills/`.

The verification script lives in your agents workflows directory:
```
~/.agents/workflows/scripts/verify-monorepo-worktree.sh
```

## Requirements

- Git worktree (`git worktree add ...`)  
- Node.js monorepo (pnpm, npm, yarn workspaces)  
- `rg` (ripgrep) for the verification script's pattern checks  

## Related Skills

- `playwright-extension-testing` — when the worktree is being used to run extension E2E tests  
- `lesson-decision-records` — if you discover a recurring pattern worth recording
