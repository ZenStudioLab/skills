# Remediation Playbook

Extended diagnostics for complex configurations. Consult this when the main SKILL.md steps don't resolve the issue.

## Table of Contents

1. [Nx Monorepos](#nx-monorepos)
2. [Turborepo](#turborepo)
3. [pnpm Catalogs](#pnpm-catalogs)
4. [Nested Submodules with Own Workspaces](#nested-submodules-with-own-workspaces)
5. [Vitest v1 vs v2 Exclusion Syntax Differences](#vitest-v1-vs-v2-exclusion-syntax-differences)
6. [Jest Config Exclusions](#jest-config-exclusions)
7. [Playwright Multi-Project Configs](#playwright-multi-project-configs)

---

## Nx Monorepos

Nx intercepts `nx run` commands using its project graph. Worktrees bypass this graph entirely when you try to `cd` into one and run `nx run` — Nx may not find its `nx.json` or may resolve the wrong workspace root.

**Safe approach:** Always run Nx commands from the primary workspace root, even targeting worktree paths:

```bash
# From primary workspace root:
nx run affected --base=main --head=HEAD
# Or target specific projects:
nx run my-app:test --output-style=stream
```

**Checking workspace root detection:**
```bash
node -e "const ws = require('@nx/devkit'); console.log(ws.workspaceRoot)"
```

If this returns the worktree path instead of the primary root, Nx is resolving the wrong workspace. Use `NX_WORKSPACE_ROOT` env var to override:

```bash
NX_WORKSPACE_ROOT=/path/to/primary/workspace nx run my-app:test
```

---

## Turborepo

Turbo uses the `turbo.json` at the workspace root for pipeline definitions. A worktree inside `packages/foo/.worktrees/branch` won't have `turbo.json` at its root, so `turbo run test` will fail or silently fall back.

**Detection:**
```bash
[[ -f "$(git rev-parse --show-toplevel)/turbo.json" ]] || echo "WARN: no turbo.json at worktree root"
```

**Safe approach:** Run `turbo run test --filter=<package>` from the primary workspace.

**Filtering to only worktree-changed files:**
```bash
turbo run test --filter=...[HEAD^1]
```

---

## pnpm Catalogs

pnpm 9 introduced `catalog:` protocol in `pnpm-workspace.yaml`. Packages defined with `catalog:default` or `catalog:<name>` require the workspace root's `pnpm-workspace.yaml` to be present.

A worktree that doesn't have its own `pnpm-workspace.yaml` will fail with:
```
ERR_PNPM_CATALOG_NOT_FOUND
```

**Fix:** Use primary workspace context exclusively. Do not attempt `pnpm install` inside a worktree for projects using pnpm catalogs.

**Detection:**
```bash
grep -r 'catalog:' "$(git rev-parse --show-toplevel)/pnpm-workspace.yaml" 2>/dev/null && echo "pnpm catalogs in use"
```

---

## Nested Submodules with Own Workspaces

Some repositories have submodules that are themselves monorepos (e.g., `parent-repo/sdk/.gitmodules` pointing to `packages/core`). Worktrees created inside these nested structures have two potential workspace roots competing.

**Symptoms:**
- `Cannot find module` errors even with symlinked `node_modules`
- Package manager locks to the wrong workspace root
- Duplicate packages at different versions

**Diagnosis:**
```bash
# From inside the nested worktree:
node -e "const path = require('path'); let dir = process.cwd(); while (dir !== '/') { const pkg = require('fs').existsSync(path.join(dir, 'package.json')); if (pkg) console.log('Found package.json:', dir); dir = path.dirname(dir); }"
```

This will print all `package.json` files up the directory tree — helping identify which workspace root Node.js will use.

**Recommended:** Pin execution to the root submodule workspace. Pass `--project` flags rather than changing directories.

---

## Vitest v1 vs v2 Exclusion Syntax Differences

Vitest v1 and v2 handle exclusions differently in the config.

**Vitest v1:**
```ts
test: {
  exclude: [...defaultExclude, '**/.worktrees/**']
}
```

**Vitest v2 (workspace mode):**
```ts
// vitest.workspace.ts
export default defineWorkspace([
  {
    test: {
      exclude: [...defaultExclude, '**/.worktrees/**']
    }
  }
])
```

Also, in Vitest v2's **browser mode**, exclusions in `vitest.config.ts` may be ignored for browser projects. Add the exclusion directly to the browser project config.

**Detecting version:**
```bash
npx vitest --version
```

---

## Jest Config Exclusions

If the project uses Jest (or a Jest-compatible runner like Bun's test runner):

```js
// jest.config.js
module.exports = {
  testPathIgnorePatterns: [
    '/node_modules/',
    '/.worktrees/',  // exclude all worktree checkouts
  ],
}
```

For projects using `jest.config.ts` with `@jest/globals`:
```ts
const config: Config = {
  testPathIgnorePatterns: ['<rootDir>/node_modules/', '<rootDir>/.worktrees/'],
}
```

---

## Playwright Multi-Project Configs

Playwright's `playwright.config.ts` can define multiple projects (chromium, firefox, etc.) with separate `testDir` values. Worktree test discovery is less of an issue with Playwright since `testDir` is explicit, but `testMatch` patterns can still catch worktree files.

**Safe config:**
```ts
export default defineConfig({
  testDir: './tests',
  testIgnore: ['**/.worktrees/**'],
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
})
```

If using `testMatch` globally (e.g., `**/*.spec.ts`), this pattern will match inside `.worktrees/` too. Always pair global `testMatch` with `testIgnore: ['**/.worktrees/**']`.
