# repo-to-notion-architect

Analyzes a local repository and produces a structured Notion workspace design.
Maps semantic roles onto Notion databases, pages, relations, and views — without
mirroring the filesystem 1:1.

## When to use

Trigger this skill when you're inside a local repo and want to:

- Map the codebase to a Notion workspace for the first time
- Design a Notion information architecture for a monorepo
- Decide what stays canonical in the repo vs. what belongs in Notion
- Generate a `.project-tools.json` metadata file for tool integrations

## Supported repo topologies

| Topology | Supported |
|----------|-----------|
| Normal single-package repo | ✅ |
| Monorepo (Turborepo, pnpm, Nx) | ✅ |
| Git submodules | ✅ |
| Monorepo + submodules | ✅ |
| Go / Rust / Python repos | ✅ |

## What it produces

Always:
1. **Repo Analysis Summary** — inferred topology, detected components, product boundaries
2. **Classification Model** — each path classified as Project / Module / Service / Surface / Library / Infra / Shared / Docs-source / Tooling
3. **Canonical-Source Strategy** — what stays in repo, what goes to Notion
4. **Proposed Notion Architecture** — databases, page structure, relations, views
5. **Mapping Table** — repo paths → Notion objects

Optionally (user-requested):
6. **Implementation Plan** — phased rollout starting from Day 1 value
7. **Metadata File Proposal** — `.project-tools.json` schema with Notion IDs

## Classification types

| Type | Meaning |
|------|---------|
| `Project` | Self-contained product with its own lifecycle |
| `Module` | Bounded subsystem — no independent deployment |
| `Service` | Independently deployed backend process |
| `Surface` | Deployed frontend / UI layer |
| `Library` | Published/consumed as a dependency |
| `Infra` | IaC, migrations, deployment config |
| `Shared` | Internal code used by ≥2 workspace members |
| `Docs-source` | Human/LLM-readable documentation directory |
| `Tooling` | Scripts, CI, build tools |

## Canonical-source rule

> Repo owns code, configs, and any `.md` files that LLMs read directly (CLAUDE.md, AGENTS.md, ADRs, architecture.md).
> Notion owns dashboards, registries, tracking, relations, planning, and reviews.

## Files

```
repo-to-notion-architect/
├── SKILL.md                              # Main skill — workflow and output format
└── references/
    ├── classification-heuristics.md     # Full decision tables and tie-break rules
    └── notion-templates.md              # DB schemas, page templates, relation directions
```

## Example prompts

```
Map this repo to Notion
Design a Notion workspace for my monorepo at ~/projects/platform
Figure out what should go in Notion vs the repo for this codebase
Set up Notion for this project — include an implementation plan and the metadata file
```

## Anti-patterns this skill prevents

- Creating one Notion Project per top-level directory (1:1 folder mirror)
- Classifying `src/` as a Module
- Making Notion the edit surface for ADRs, CLAUDE.md, or architecture.md
- Treating git submodules as identical to monorepo workspace packages
- Recommending a big-bang migration before any value is delivered
