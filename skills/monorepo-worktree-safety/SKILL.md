---
name: monorepo-worktree-safety
description: "Prevents dependency resolution failures and test discovery disasters when using git worktrees inside monorepos or submodules. Use this skill whenever: (1) creating a git worktree anywhere inside a monorepo or submodule directory, (2) you see errors like 'vitest: not found', unresolved @org/* or workspace:* packages from a worktree path, (3) test suites are running unexpectedly duplicate or foreign tests, (4) someone asks to run coverage or CI checks from a branch worktree, (5) setting up parallel feature development in a monorepo using worktrees. If the user mentions worktrees AND a monorepo, always apply this skill — don't assume the environment is already safe."
---

# Monorepo Worktree Safety

A worktree is an isolated filesystem checkout of a git branch — but it is NOT an isolated Node.js runtime. When a worktree lives inside a monorepo or submodule, the tooling and package resolution it inherits (or fails to inherit) from the surrounding workspace can cause silent failures that look like product bugs.

This skill helps you set up worktrees correctly the first time and diagnose issues when they appear.

## The Core Problem

Monorepos use workspace-relative package resolution (`workspace:*`, `@org/*`). When you create a worktree inside a submodule (e.g., `submodule/.worktrees/feature-branch`), that worktree's `node_modules` is typically absent or isolated. Running `vitest` or `playwright` from inside that worktree will either fail outright or silently pick up the wrong binaries — leading to errors that are easy to misread as code regressions.

A secondary hazard: test discovery tools (Vitest, Jest) sometimes crawl the entire repo root, which means they can pick up test files living inside nested worktrees unless explicitly excluded.

## Workflow

### Step 1: Run the verification script (required — do not skip)

Even if you have file-reading tools available, run the script first. It produces structured output that anchors the rest of this workflow and gives a consistent baseline for the report you'll produce in Step 5.

```bash
bash ~/.agents/workflows/scripts/verify-monorepo-worktree.sh
```

This script checks the current working directory and repo root for:
- Whether we are inside a `.worktrees/` path
- Availability of `vitest`, `playwright`, `node`
- Workspace/local package patterns in `package.json`
- `node_modules` status (absent / local / symlinked)
- `.worktrees/` present in `.gitignore`
- `.worktrees/**` exclusion in vitest config

Read the output carefully. Each line is prefixed with `OK`, `WARN`, or `INFO`.

### Step 2: Decide the execution context

The most important decision is **where tests and tooling will run from**.

> **Nested submodule warning**: If the worktree is inside a directory that is itself a submodule (e.g., `parent-repo/platform/.worktrees/branch`), the workspace root is ambiguous — Node.js package resolution may walk up to the wrong workspace root. Both the submodule root and the parent repo root are candidates. Treat this as a high-risk configuration and prefer primary workspace context inside the submodule, not the parent repo root.

```
Is the worktree missing `node_modules`?
├─ YES → Does the project use workspace packages (@org/*, workspace:*)?
│         ├─ YES → Run from primary workspace context (preferred)
│         └─ NO  → `npm install` (or pnpm/yarn) inside worktree, then run locally
└─ NO  → Is node_modules a real directory (not symlink)?
          ├─ YES → Run from worktree directly (check binary availability first)
          └─ NO  → Symlink already in place, verify runtime parity (see Step 4)
```

**Primary workspace context** means: run `vitest --project <path>` or similar from the repo root, targeting paths within the worktree, rather than `cd`-ing into the worktree and running `vitest` there.

### Step 3: Apply remediations for each WARN

#### WARN: `vitest` / `playwright` / `node` not found in PATH from worktree

Switch to primary workspace execution context. Do not install these globally or attempt a fresh `npm install` — workspace-local packages cannot be resolved from the registry.

```bash
# From the primary workspace root (not the worktree):
pnpm exec vitest run --reporter=verbose
# or scope to worktree files:
pnpm exec vitest run packages/foo/src
```

#### WARN: no `node_modules` found in worktree context

If you must execute from the worktree (e.g., a script that expects relative paths), try a `node_modules` symlink as a fallback:

```bash
ln -s "$(git rev-parse --show-toplevel)/node_modules" .worktrees/<branch>/node_modules
```

After symlinking, run a quick sanity check — if you see React or any singleton instantiated twice, there is a module-graph collision and you should fall back to the primary workspace context instead.

#### WARN: `.gitignore` missing `.worktrees/`

When worktrees live inside the project directory (e.g., `<repo>/.worktrees/<branch>`), git will report them as untracked unless ignored. Patch `.gitignore`:

```
# Git worktrees (project-local)
.worktrees/
```

#### WARN: Vitest config missing `.worktrees/**` exclusion

Vitest (and Jest) crawl from the configured root. Without an explicit exclusion, test files inside `<repo>/.worktrees/<branch>/` will be discovered and run regardless of which branch you're on.

Patch `vitest.config.ts` (or equivalent):

```ts
export default defineConfig({
  test: {
    exclude: [
      ...defaultExclude,
      '**/.worktrees/**',  // prevent test discovery inside worktree checkouts
    ],
  },
})
```

### Step 4: Runtime parity check after symlinking

After a `node_modules` symlink is established, verify no module singletons are duplicated:

```bash
node -e "
  const React = require('./node_modules/react');
  console.log('React version:', React.version);
  console.log('React instance:', React === require('react') ? 'SAME' : 'DUPLICATE ⚠️');
"
```

If you see `DUPLICATE`, do not proceed with the symlink approach — switch to primary workspace context.

### Step 5: Produce Output Report

After completing the workflow, produce a brief report (can be inline, does not need a file):

```
## Worktree Safety Report
- Execution context: [primary workspace / worktree direct / worktree with symlink]
- Toolchain risk: [none / mitigated / blocking]
- .worktrees/** Vitest exclusion: [present / added / not applicable]
- .worktrees/ gitignore: [present / added / not applicable]
- Runtime parity: [verified / not checked / collision detected]
- Final verification context: [command used to run tests]
```

## Red Flags — Why These Bite Hard

**"I'll just `pnpm install` inside the worktree"** — This will pull workspace packages from the npm registry instead of your local monorepo, often getting the wrong version or failing entirely. The correct approach is always to run from primary workspace context.

**"The tests passed in the worktree"** — If `.worktrees/**` is not excluded from test discovery, you may be running tests from the wrong branch's checkout, giving you a false clean signal.

**"The symlink worked fine"** — Until a singleton (React, Zustand store, a context provider) is instantiated twice and produces subtle runtime bugs that only appear in that worktree context.

## References

- Verification script: `~/.agents/workflows/scripts/verify-monorepo-worktree.sh`
- See `references/remediation-playbook.md` for deeper diagnostics on complex configurations (nx, turborepo, pnpm catalogs, nested submodules with their own workspaces)
