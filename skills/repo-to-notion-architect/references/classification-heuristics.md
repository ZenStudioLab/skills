# Classification Heuristics

Full decision tables for Phase 2 of `repo-to-notion-architect`.

## Type Definitions

| Type | Definition |
|------|-----------|
| **Project** | A self-contained product or app that delivers user-facing value and has its own lifecycle |
| **Module** | A bounded subsystem within a Project — no independent deployment |
| **Service** | An independently deployed backend process (API, worker, function) |
| **Surface** | A deployed frontend or UI layer (web app, mobile app, browser extension) |
| **Library** | A package published/consumed as a dependency — primarily a code API |
| **Infra** | Infrastructure-as-code, database migrations, deployment config, secrets management |
| **Shared** | Internal code consumed by ≥2 workspace members — not published externally |
| **Docs-source** | A directory whose primary purpose is human/LLM-readable documentation |
| **Tooling** | Scripts, CI configs, build tools, developer utilities |

---

## Primary Signal Table

Apply signals top-to-bottom. First match wins unless a Tie-Break rule applies.

| # | Observed signal | → Type | Confidence |
|---|----------------|--------|-----------|
| 1 | `.gitmodules` entry pointing to external repo | evaluate submodule individually | High |
| 2 | Own `package.json` with `"private": false` + `version` field | Library | High |
| 3 | Own `package.json` + deployed URL signal + UI entrypoint | Surface | High |
| 4 | Own `package.json` + deployed URL signal + HTTP server entrypoint | Service | High |
| 5 | `supabase/` OR `terraform/` OR `k8s/` OR `infra/` at component root | Infra | High |
| 6 | `docs/` with ≥3 of: `adr/`, `plans/`, `architecture.md`, `decision-log.md` | Docs-source | High |
| 7 | Under `packages/` or `libs/` AND imported by ≥2 other workspace members | Shared | High |
| 8 | Under `packages/` or `libs/` AND `"private": false` in own `package.json` | Library | High |
| 9 | Under `apps/` AND has build pipeline AND own env vars | Surface or Service (apply rule 3/4) | High |
| 10 | `.github/workflows/` OR `scripts/` OR `tools/` at root | Tooling | High |
| 11 | `src/` at root + single `package.json` + no workspace config | Project | Medium |
| 12 | Subdirectory with own `package.json` + no deployment config | Module | Medium |
| 13 | Directory containing only `.md` files | Docs-source | Low |

### Deployed URL signals (any confirms Surface or Service)
- `homepage` key in `package.json`
- `VITE_APP_URL`, `NEXT_PUBLIC_URL`, `NEXT_PUBLIC_SITE_URL`
- `vercel.json`, `netlify.toml`, `fly.toml`, `render.yaml`, `.vercel/project.json`
- `Dockerfile` + `docker-compose.yml`

### HTTP server entrypoint signals
- `src/server.ts` or `src/index.ts` with `express`/`fastify`/`hono`/`koa` import
- `app/api/` directory (Next.js API routes)
- `functions/` directory (serverless)
- `src/routes/` without `pages/` or `app/`

### UI entrypoint signals
- `pages/` or `app/` directories (Next.js/Nuxt)
- `src/App.tsx`, `src/main.tsx`, or `index.html` + Vite config
- `public/` + framework config

---

## Repo Topology Table

Determine repo type before classifying individual components.

| Signals present at root | → Repo type |
|------------------------|------------|
| `pnpm-workspace.yaml` OR `turbo.json` OR `nx.json` | Monorepo |
| `lerna.json` | Monorepo (legacy) |
| `go.work` | Go multi-module workspace |
| `.gitmodules` with entries | Has submodules |
| Monorepo signals + `.gitmodules` | Monorepo + Submodules |
| None of the above + single `package.json` at root | Normal repo |
| None of the above + no `package.json` | Normal repo (non-JS) |

---

## Tie-Break Rules

| Conflict | Rule |
|---------|------|
| Library vs Shared | `"private": false` or a published semver → Library; internally-only → Shared |
| Surface vs Service | Renders HTML → Surface; only responds JSON/events → Service; if both, classify as Service and note split recommendation |
| Project vs Module | Has its own deployment pipeline or versioned releases → Project; depends on parent's build → Module |
| Docs-source vs Module | >50% of files are `.md` → Docs-source; otherwise check for code first |
| Infra vs Service | Running process → Service; configures or provisions infrastructure → Infra |

---

## Monorepo Member Classification Workflow

For each entry in `apps/`, `packages/`, `services/`, `libs/`:

1. Read its `package.json`: extract `name`, `version`, `private`, `scripts`
2. Check for UI entrypoint signals → candidate Surface
3. Check for HTTP server signals → candidate Service
4. Check for deployed URL signals → confirms Surface or Service
5. Check `"private": false` → candidate Library
6. Check if imported by ≥2 siblings → candidate Shared
7. Check for infra signals → candidate Infra
8. Fallback if none match → Module

---

## Git Submodule Classification Workflow

1. Read `path` and `url` from `.gitmodules`
2. Check if the submodule directory is cloned (`ls <path>`)
3. **If cloned:** run the full Primary Signal Table against the submodule root
4. **If not cloned:** infer from `url` name pattern (e.g., `*-infra`, `*-scripts` → Infra/Tooling; `*-design-system`, `*-ui` → Library)
5. Always list submodules **separately** from monorepo workspace packages in the output
6. Flag uncloned submodules as `inferred — verify when cloned`

---

## Product Boundary Detection

| Signal | Inference |
|--------|----------|
| ≥2 entries under `apps/` each with own deployment config | Multiple product surfaces |
| Submodule pointing to a different GitHub org | External dependency — not a product boundary |
| `packages/` members all named `@<same-scope>/*` | Single product, shared layer |
| `services/` with separate env files per entry | Multiple independent services, likely one product |
| Root `README.md` describes a single user-facing product | Single product boundary |

---

## Common Misclassification Traps

| What you see | Wrong | Correct |
|-------------|-------|---------|
| `src/` directory at root | Module | Not a classifiable component — it is a code directory inside a Project |
| `scripts/` with shell files | Module or Service | Tooling |
| `docs/` with markdown files | Project | Docs-source |
| `supabase/` with SQL migrations | Service | Infra |
| `packages/ui` used only by one app | Library | Shared (or Module if tightly coupled) |
| Git submodule of a design system | Surface | Library |
| `.github/` directory | Module | Tooling |
| `config/` or `settings/` dir | Module | Tooling (unless it contains IaC) |
| `turbo.json` or `nx.json` at root | Component | Not a component — workspace config file |
| `node_modules/` | Anything | Skip — not a component |
