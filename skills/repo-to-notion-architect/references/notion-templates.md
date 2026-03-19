# Notion Templates

Database schemas, page templates, and view configurations for
`repo-to-notion-architect`. These are defaults — adapt based on
repo complexity and `--scale` flag.

---

## Database Schemas

### DB: Projects

Purpose: One record per top-level Project, Surface, or Service component.

| Property | Type | Values / Config |
|----------|------|----------------|
| Name | Title | component name |
| Type | Select | `Project`, `Surface`, `Service`, `Library`, `Infra`, `Shared` |
| Status | Status | Not started → In Progress → Launched → Archived |
| Repo path | Text | relative path from repo root |
| Deployed URL | URL | live URL if applicable |
| Tech stack | Multi-select | e.g., `Next.js`, `Supabase`, `TypeScript` |
| Owner | Person | leave empty for solo |
| Canonical source | Select | `Repo`, `Notion`, `Both` |
| Parent product | Relation → Projects (self) | for submodules or nested projects |
| Features | Relation → Features | backlink |
| Docs | Relation → Docs Index | backlink |

Views:
- **All Projects** — Table, no filter, sort by Status asc
- **Active** — Board, grouped by Status
- **By Type** — Table, grouped by Type, sort by Name asc
- **Registry** — Gallery, no filter, sort by Name asc

---

### DB: Features

Purpose: One record per significant feature, epic, or capability being built.

| Property | Type | Values / Config |
|----------|------|----------------|
| Name | Title | feature name |
| Status | Status | Backlog → In Design → In Dev → In Review → Done |
| Project | Relation → Projects | required |
| Priority | Select | `P0`, `P1`, `P2`, `P3` |
| Size | Select | `XS`, `S`, `M`, `L`, `XL` |
| Milestone | Text | version or sprint label |
| Tasks | Relation → Tasks | backlink |
| Plan doc | Relation → Plans | linked implementation plan |
| Review | Relation → Reviews | linked design/code review |

Views:
- **Kanban** — Board, no filter, grouped by Status
- **Active sprint** — Table, filter Status != Done AND != Backlog, sort Priority asc
- **Backlog** — Table, filter Status = Backlog, sort Size asc
- **By project** — Table, grouped by Project, sort Status asc

---

### DB: Tasks

Purpose: One record per concrete unit of work (maps roughly to a PR or commit cluster).

**Note for solo builders:** Tasks DB is optional. Add it only when features
regularly have >5 sub-steps. Otherwise, Features are granular enough.

| Property | Type | Values / Config |
|----------|------|----------------|
| Name | Title | task description |
| Status | Status | Todo → In Progress → Done → Blocked |
| Feature | Relation → Features | required |
| Assignee | Person | |
| PR link | URL | GitHub/GitLab PR URL |
| Effort | Number | hours estimate |
| Blocked by | Relation → Tasks (self) | |

Views:
- **My tasks** — Table, filter Assignee = Me, sort Status asc
- **In progress** — Table, filter Status = In Progress, sort Feature asc
- **Blocked** — Table, filter Status = Blocked

---

### DB: Docs Index

Purpose: Registry of significant documentation files. Does NOT copy content.
Content stays in repo. Notion holds the index, status, and cross-links.

| Property | Type | Values / Config |
|----------|------|----------------|
| Title | Title | document title |
| Doc type | Select | `Architecture`, `ADR`, `Plan`, `Guide`, `Review`, `API`, `Runbook`, `README` |
| Repo path | Text | relative path from repo root |
| Status | Select | `Current`, `Draft`, `Stale`, `Superseded` |
| Project | Relation → Projects | scope |
| Related ADR | Relation → ADRs | |
| Last reviewed | Date | |

Views:
- **All docs** — Table, no filter, sort by Doc type asc
- **Stale** — Table, filter Status = Stale, sort Last reviewed asc
- **By project** — Table, grouped by Project, sort Doc type asc

---

### DB: ADRs

Purpose: Index of Architecture Decision Records. Content stays in `docs/adr/`.

| Property | Type | Values / Config |
|----------|------|----------------|
| Title | Title | ADR title |
| Number | Number | sequential NNNN |
| Status | Select | `Proposed`, `Accepted`, `Deprecated`, `Superseded` |
| Date | Date | decision date |
| Project | Relation → Projects | scope |
| Superseded by | Relation → ADRs (self) | |
| Repo path | Text | e.g., `docs/adr/0001-use-postgres.md` |
| Tags | Multi-select | e.g., `database`, `auth`, `frontend` |

Views:
- **All ADRs** — Table, no filter, sort by Number asc
- **Active** — Table, filter Status = Accepted, sort Number asc
- **By project** — Table, grouped by Project, sort Number asc

---

### DB: Plans

Purpose: Index of implementation plans, rollout plans, migration plans.

| Property | Type | Values / Config |
|----------|------|----------------|
| Title | Title | plan name |
| Status | Select | `Draft`, `Approved`, `In Progress`, `Done`, `Abandoned` |
| Feature | Relation → Features | what this plan implements |
| Project | Relation → Projects | scope |
| Repo path | Text | e.g., `docs/plans/active/2026-03-01-auth-refactor.md` |
| Date | Date | plan creation date |
| Outcome | Text | one-line result summary |

---

### DB: Reviews

Purpose: Design reviews, code reviews, post-mortems, retros.

| Property | Type | Values / Config |
|----------|------|----------------|
| Title | Title | review name |
| Review type | Select | `Design`, `Code`, `Post-mortem`, `Retro`, `Security` |
| Status | Select | `Open`, `In Review`, `Closed` |
| Feature | Relation → Features | what was reviewed |
| Project | Relation → Projects | scope |
| Date | Date | |
| Outcome | Select | `Approved`, `Needs changes`, `Rejected`, `Informational` |

---

### DB: Modules Registry (monorepo only, >3 apps)

Purpose: Registry of all workspace members with classification and dependency graph.

| Property | Type | Values / Config |
|----------|------|----------------|
| Name | Title | package name (from `package.json "name"`) |
| Type | Select | `Surface`, `Service`, `Library`, `Shared`, `Infra`, `Tooling` |
| Repo path | Text | relative path from root |
| Version | Text | semver from `package.json` |
| Consumers | Relation → Modules Registry (self) | packages that import this |
| Project | Relation → Projects | parent product |
| Private | Checkbox | from `package.json "private"` |
| Status | Select | `Active`, `Deprecated`, `Experimental` |

Views:
- **All modules** — Table, no filter, sort by Type asc, Name asc
- **Shared / Libraries** — Table, filter Type = Shared OR Library
- **Deprecated** — Table, filter Status = Deprecated

---

### DB: Environments (repos with deployed services)

Purpose: Track deployment environments per service.

| Property | Type | Values / Config |
|----------|------|----------------|
| Name | Title | e.g., "web — production" |
| Service | Relation → Projects | |
| Env type | Select | `production`, `staging`, `preview`, `local` |
| URL | URL | live URL |
| Status | Select | `Healthy`, `Degraded`, `Down`, `Unknown` |
| Last deploy | Date | |
| Deploy config | Text | e.g., `vercel.json`, `fly.toml` |

---

## Page Structure Templates

### Solo builder — normal repo
```
[Workspace name]
├── Home (dashboard page, manual)
├── Projects [DB]
├── Features [DB]
├── Tasks [DB]              ← optional, add when features have >5 sub-steps
├── Docs Index [DB]
├── ADRs [DB]
├── Plans [DB]
└── Reviews [DB]
```

### Solo builder — monorepo (3–8 apps)
```
[Workspace name]
├── Home
├── Products (group page)
│   ├── [App 1 name]        ← linked record from Projects DB
│   └── [App 2 name]
├── Projects [DB]
├── Modules Registry [DB]
├── Features [DB]
├── Docs Index [DB]
├── ADRs [DB]
├── Plans [DB]
└── Reviews [DB]
```

### Team — monorepo with services
```
[Workspace name]
├── Home
├── Products (group page)
├── Projects [DB]
├── Modules Registry [DB]
├── Features [DB]
├── Tasks [DB]
├── Docs Index [DB]
├── ADRs [DB]
├── Plans [DB]
├── Reviews [DB]
└── Environments [DB]
```

---

## Relation Directions

| From | Relation | To | Direction |
|------|----------|-----|-----------|
| Features | belongs to | Projects | many-to-one |
| Tasks | belongs to | Features | many-to-one |
| Docs Index | scoped to | Projects | many-to-many |
| ADRs | scoped to | Projects | many-to-many |
| Plans | implements | Features | many-to-one |
| Reviews | reviews | Features | many-to-many |
| Modules Registry | consumed by | Modules Registry | self-referential many-to-many |
| Environments | belongs to | Projects | many-to-one |

---

## Metadata File: `.project-tools.json` Schema

Use `.project-tools.json` over alternatives (`workspace-tools`, `tooling-map`) because
"project" scopes to the product being built without colliding with IDE workspace concepts
(VS Code workspaces, pnpm workspaces). It is grep-friendly and vendor-neutral.

All tool fields are nullable so the file can be committed on Day 1 before any tool
IDs are known. LLMs and scripts must check for `null` before using a field.

```json
{
  "$schema": "https://example.com/schemas/project-tools/v1.json",
  "version": "1",
  "project": {
    "name": "my-app",
    "type": "monorepo",
    "repoUrl": "https://github.com/org/my-app",
    "docs": {
      "primary": "./docs",
      "extra": []
    }
  },
  "tools": {
    "notion": {
      "workspaceId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "rootPageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "databases": {
        "projects":    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "features":    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "tasks":       "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "docsIndex":   "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "adrs":        "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "plans":       "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "reviews":     "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "modules":     "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
    },
    "linear": null,
    "mixpanel": null,
    "figma": null
  },
  "modules": [
    {
      "name": "@my-app/web",
      "path": "apps/web",
      "type": "Surface",
      "notionProjectId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    {
      "name": "@my-app/api",
      "path": "apps/api",
      "type": "Service",
      "notionProjectId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    {
      "name": "@my-app/ui",
      "path": "packages/ui",
      "type": "Library",
      "notionProjectId": null
    }
  ]
}
```
