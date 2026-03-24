---
name: github-os
description: "Set up a GitHub-based Operating System for software projects. Use when: (1) Starting a new project and need issue tracking setup, (2) Restructuring GitHub workflows, (3) Setting up execution system for solo builder or team, (4) Establishing LLM-driven development workflows, (5) Migrating from other tools to GitHub, (6) Setting up monorepo or multi-repo issue tracking, (7) Need integration between GitHub issues and repo docs, (8) Want 'GitHub as OS' with docs as knowledge layer."
---

# GitHub OS

A systematic approach to setting up GitHub as your project's Operating System - treating GitHub as the execution layer (issues, projects, labels, PRs) integrated with repository documentation as the knowledge layer. Optimized for LLM-driven development workflows.

## When to Use This Skill

### Use When:
- **New Project Setup**: Starting fresh and need a complete GitHub execution system
- **Workflow Restructuring**: Current issue tracking is chaotic or unstructured
- **LLM Optimization**: Want to optimize GitHub for LLM-driven development
- **Solo → Team Scaling**: Need system that works solo but scales to teams
- **Tool Migration**: Moving from Linear, Notion, Jira to GitHub
- **Monorepo/Multi-repo**: Setting up coordinated tracking across multiple codebases
- **Docs Integration**: Want tight integration between GitHub issues and repo docs
- **Convention Establishment**: Need standardized labels, templates, workflows

### Do NOT Use When:
- Project already has well-functioning GitHub system
- Team uses external PM tools (Linear, Jira) as primary source
- Quick one-off issue creation (use github-issues skill instead)
- Read-only operations on existing issues

## Prerequisites

### Required
1. **GitHub MCP Server**: Primary tool for GitHub operations
   - See `assets/github-mcp-setup.md` for installation
   - Enables label creation, issue management, project setup
   - Fallback to `gh` CLI if MCP unavailable

2. **Repository Access**: Write access to target repository

3. **Documentation Directory**: Recommended `./docs` structure
   - Not required, but highly recommended
   - Can be customized per project

### Optional
- **GitHub CLI (`gh`)**: Fallback tool for operations
- **Existing skills**: Works alongside github-issues skill

## Core Philosophy

The GitHub OS system is built on three pillars:

### 1. GitHub = Execution OS
- **Issues**: Tasks, features, bugs (execution units)
- **Projects**: Coordination and visibility
- **Labels**: Classification and routing
- **Pull Requests**: Implementation artifacts
- **Milestones**: Release tracking

### 2. Docs = Knowledge OS
- **`./docs`**: Canonical source of truth
- **Architecture docs**: System design
- **ADRs**: Decisions and context
- **Context files**: Current state, handoffs
- **Never duplicate**: Docs live in repo, not GitHub

### 3. LLM = Connector
- **Context linking**: Issues link to relevant docs
- **LLM-ready tasks**: Structured for AI consumption
- **Clear scope**: Explicit boundaries and constraints
- **Minimal overhead**: Just enough structure, no bureaucracy

## Workflow Overview

```
1. Analyze Repository
   ↓
2. Design GitHub OS System
   ↓
3. Present Design for Approval
   ↓
4. Execute (Design-Only or Auto-Generate)
   ↓
5. Validate System
```

## Step 1: Repository Analysis

### Detection Heuristics

#### Repository Type
Analyze repository structure to determine:

**Single Repository**:
- One primary codebase
- May have multiple modules but unified project
- Example: `src/`, `lib/`, `tests/`

**Monorepo**:
- Multiple independent apps/packages
- Indicators:
  - `apps/`, `packages/`, `services/` directories
  - Workspace configuration (`package.json` workspaces, `pnpm-workspace.yaml`)
  - Build tool config (`nx.json`, `turbo.json`, `lerna.json`)
- Example: `apps/web`, `apps/api`, `packages/ui`

**Multi-repo System**:
- Multiple separate repositories
- Indicators:
  - Git submodules (`.gitmodules`)
  - References to external repos in docs
  - Microservices architecture
- Example: `repo-frontend`, `repo-backend`, `repo-mobile`

#### Module Detection

**Top-level Folders**:
```
apps/           → App modules
packages/       → Shared packages
services/       → Service modules
libs/           → Library modules
tools/          → Tool modules (usually not project modules)
scripts/        → Script utilities (not project modules)
```

**Submodules**:
- Parse `.gitmodules`
- Each submodule = potential module or separate project

**Workspace Detection**:
- Parse `package.json` workspaces
- Parse `pnpm-workspace.yaml`
- Parse `nx.json` projects
- Parse `turbo.json` pipeline

**Module Classification**:
- **App**: User-facing application (`apps/web`, `apps/mobile`)
- **Service**: Backend service (`services/api`, `services/worker`)
- **Package**: Shared library (`packages/ui`, `packages/utils`)
- **Infra**: Infrastructure code (usually not a module for issues)

#### Documentation Structure

**Standard Locations**:
1. `./docs/` - Preferred
2. `./documentation/`
3. `./wiki/`
4. Root-level docs (`ARCHITECTURE.md`, `CONTRIBUTING.md`)

**Key Documents**:
- `architecture.md` or `ARCHITECTURE.md`
- `ADRs/` or `decisions/`
- `current-task.md` or `context.md`
- `README.md` (always present)

**Docs Assessment**:
- **Rich**: Has dedicated docs directory with architecture + ADRs
- **Basic**: Has README + some markdown files
- **Minimal**: Only README

### Analysis Output

Generate structured report:

```markdown
# Repository Analysis

## Type
[Single Repo / Monorepo / Multi-repo]

## Modules Detected
- [module-name] (type: [app/service/package], path: [path])
- ...

## Documentation Structure
- Docs directory: [path or "none"]
- Architecture docs: [found/not found]
- ADRs: [found/not found]
- Assessment: [rich/basic/minimal]

## Execution Surfaces
- Primary repo: [repo-name]
- Total modules: [count]
- Recommended label count: [estimate]
```

## Step 2: GitHub OS Design

### A. Label System

#### Core Taxonomy

**Type Labels** (required):
```
type:feature     - New features
type:bug         - Bug fixes
type:chore       - Maintenance, refactoring
type:research    - Spikes, investigations
```

**Priority Labels** (required):
```
priority:p0      - Critical (blocks release)
priority:p1      - High (next sprint)
priority:p2      - Medium (backlog)
priority:p3      - Low (nice to have)
```

**Area Labels** (cross-cutting):
```
area:ui          - User interface
area:engine      - Core logic
area:seo         - SEO/marketing
area:infra       - Infrastructure
area:dx          - Developer experience
area:docs        - Documentation
area:security    - Security
area:performance - Performance
```

**Module Labels** (dynamic):
Generate based on detected modules:
```
module:web       (from apps/web)
module:api       (from services/api)
module:ui        (from packages/ui)
```

**Status Labels** (optional):
```
status:blocked       - Blocked by dependency
status:llm-ready     - Ready for LLM implementation
status:needs-context - Needs more context/clarification
```

#### Label Colors

Standard color scheme:

```json
{
  "type:feature": "0e8a16",
  "type:bug": "d73a4a",
  "type:chore": "fef2c0",
  "type:research": "d4c5f9",
  
  "priority:p0": "b60205",
  "priority:p1": "d93f0b",
  "priority:p2": "fbca04",
  "priority:p3": "0e8a16",
  
  "area:ui": "1d76db",
  "area:engine": "5319e7",
  "area:seo": "c2e0c6",
  "area:infra": "0052cc",
  "area:dx": "e99695",
  "area:docs": "d4c5f9",
  "area:security": "b60205",
  "area:performance": "fbca04",
  
  "module:*": "0052cc",
  
  "status:blocked": "d73a4a",
  "status:llm-ready": "0e8a16",
  "status:needs-context": "fbca04"
}
```

### B. Issue Model (Integrating github-issues)

This skill extends the `github-issues` skill from https://skills.sh/github/awesome-copilot/github-issues with LLM-specific enhancements.

#### Core Principles from github-issues

**Use Issue Types** (when available):
- Prefer GitHub's native issue types over labels
- Types: Bug, Feature, Task, Epic
- Query org types: `gh api graphql -f query='{ organization(login: "ORG") { issueTypes(first: 10) { nodes { name } } } }'`

**Title Guidelines**:
- Specific and actionable
- Under 72 characters
- No redundant prefixes (e.g., `[Bug]`) when using types
- Examples:
  - `Login fails with SSO enabled` (type=Bug)
  - `Add dark mode support` (type=Feature)
  - `Add unit tests for auth module` (type=Task)

**Body Structure** (from github-issues templates):
- Use structured templates
- Clear sections
- Markdown formatting

#### LLM Enhancements

**Required Context Section**:
Every issue must include explicit context:

```markdown
## Context

### Related Documentation
- Architecture: `./docs/architecture.md#auth-system`
- ADR: `./docs/ADRs/0015-sso-implementation.md`
- Current Task: `./docs/current-task.md`

### Related Issues
- Blocks: #123
- Blocked by: #124
- Related: #125

### Code Scope
Files/modules that will be affected:
- `src/auth/sso.ts`
- `src/auth/providers/`
- `tests/auth/sso.test.ts`
```

**Explicit Scope**:
Define boundaries clearly:

```markdown
## Scope

### In Scope
- SSO login flow
- Error handling for SSO failures
- Unit tests for SSO provider

### Out of Scope
- SAML support (separate issue)
- User profile sync (separate issue)
```

**LLM-Ready Criteria**:
An issue is "LLM-ready" when:
- ✅ Clear goal statement
- ✅ Context docs linked
- ✅ Scope explicitly defined
- ✅ Acceptance criteria listed
- ✅ No blocking dependencies
- ✅ Files/modules identified

Label with `status:llm-ready` when criteria met.

### C. Issue Templates

#### Task Template (`.github/ISSUE_TEMPLATE/task.yml`)

GitHub form template:

```yaml
name: Task
description: Standard task for implementation
title: "[Task] "
labels: ["type:feature"]
body:
  - type: markdown
    attributes:
      value: |
        Use this template for implementation tasks.
        
  - type: input
    id: summary
    attributes:
      label: Summary
      description: One-sentence summary of this task
      placeholder: "Implement SSO authentication"
    validations:
      required: true
      
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - priority:p0
        - priority:p1
        - priority:p2
        - priority:p3
    validations:
      required: true
      
  - type: dropdown
    id: area
    attributes:
      label: Area
      options:
        - area:ui
        - area:engine
        - area:seo
        - area:infra
        - area:dx
        - area:docs
        - area:security
        - area:performance
    validations:
      required: false
      
  - type: input
    id: module
    attributes:
      label: Module
      description: Which module does this affect? (e.g., module:web, module:api)
      placeholder: "module:api"
    validations:
      required: false
      
  - type: textarea
    id: context
    attributes:
      label: Context
      description: |
        Link to relevant documentation and context.
        
        Format:
        - Architecture: ./docs/architecture.md#section
        - ADRs: ./docs/ADRs/NNNN-decision.md
        - Related Issues: #123, #124
      placeholder: |
        - Architecture: ./docs/architecture.md#auth
        - ADRs: ./docs/ADRs/0015-sso.md
        - Related: #42
    validations:
      required: true
      
  - type: textarea
    id: scope
    attributes:
      label: Scope
      description: |
        Files and modules affected. What's in scope and out of scope?
        
      placeholder: |
        **In Scope:**
        - src/auth/sso.ts
        - tests/auth/sso.test.ts
        
        **Out of Scope:**
        - SAML integration (separate task)
    validations:
      required: true
      
  - type: textarea
    id: goal
    attributes:
      label: Goal
      description: What should this accomplish?
      placeholder: "Enable users to authenticate via SSO providers (Google, GitHub)"
    validations:
      required: true
      
  - type: textarea
    id: constraints
    attributes:
      label: Constraints
      description: Any technical constraints or requirements?
      placeholder: |
        - Must support OAuth 2.0
        - Must not break existing email/password auth
        - Session handling unchanged
    validations:
      required: false
      
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance Criteria
      description: How do we know this is done?
      placeholder: |
        - [ ] SSO login button appears on login page
        - [ ] Successful OAuth flow redirects to dashboard
        - [ ] Failed auth shows error message
        - [ ] Tests pass
    validations:
      required: true
```

#### Bug Template (`.github/ISSUE_TEMPLATE/bug.yml`)

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug] "
labels: ["type:bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What's the bug?
      placeholder: "SSO login redirects to 404 page"
    validations:
      required: true
      
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      placeholder: |
        1. Navigate to login page
        2. Click "Sign in with Google"
        3. Complete Google OAuth
        4. Redirected to /404
    validations:
      required: true
      
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen?
      placeholder: "Should redirect to /dashboard"
    validations:
      required: true
      
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happens?
      placeholder: "Redirects to /404 page"
    validations:
      required: true
      
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - priority:p0
        - priority:p1
        - priority:p2
        - priority:p3
    validations:
      required: true
      
  - type: input
    id: module
    attributes:
      label: Module
      description: Which module is affected?
      placeholder: "module:api"
      
  - type: textarea
    id: context
    attributes:
      label: Context
      description: Environment, logs, related issues
      placeholder: |
        - Environment: production
        - Error logs: [paste here]
        - Related: #123
```

#### Feature Template (`.github/ISSUE_TEMPLATE/feature.yml`)

```yaml
name: Feature Request
description: Propose a new feature
title: "[Feature] "
labels: ["type:feature"]
body:
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: What feature do you want?
      placeholder: "Add OAuth support for Microsoft accounts"
    validations:
      required: true
      
  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why is this needed?
      placeholder: |
        - Enterprise customers request Microsoft SSO
        - Completes SSO provider coverage
    validations:
      required: true
      
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this work?
      placeholder: "Add Microsoft as OAuth provider using same pattern as Google/GitHub"
    validations:
      required: true
      
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance Criteria
      description: What defines done?
      placeholder: |
        - [ ] Microsoft SSO button on login page
        - [ ] Successful auth flow
        - [ ] Tests pass
    validations:
      required: true
      
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - priority:p0
        - priority:p1
        - priority:p2
        - priority:p3
```

### D. Pull Request Template

File: `.github/pull_request_template.md`

```markdown
## Related Issue
Closes #

## What Changed
<!-- Brief summary of changes made -->

## Why
<!-- Reasoning for this approach -->

## Context
<!-- Link to relevant documentation -->

### Documentation
- Architecture: `./docs/architecture.md#section`
- ADRs: `./docs/ADRs/NNNN-decision.md`
- Related context: `./docs/current-task.md`

### Related
- Related PRs: #
- Related Issues: #

## Changes

### Added
- 

### Modified
- 

### Removed
- 

## Testing

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

### How to Test
1. 
2. 
3. 

## Deployment Notes
<!-- Any special deployment considerations -->

- [ ] Database migrations required
- [ ] Environment variables needed
- [ ] Breaking changes
- [ ] Requires coordination with other services

## Screenshots/Videos
<!-- If applicable -->

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No console errors/warnings
```

### E. GitHub Projects Design

#### Fields Configuration

Create custom fields in GitHub Project:

1. **Status** (Single select, required)
   - Todo
   - In Progress
   - In Review
   - Done
   - Blocked

2. **Priority** (Single select)
   - P0
   - P1
   - P2
   - P3

3. **Area** (Single select)
   - UI
   - Engine
   - SEO
   - Infra
   - DX
   - Docs
   - Security
   - Performance

4. **Module** (Text)
   - Free-form text for module name

5. **Type** (Single select)
   - Feature
   - Bug
   - Chore
   - Research

6. **LLM Ready** (Checkbox)
   - True/False

#### View Definitions

**1. Current Work**
- Filter: Status = "In Progress" OR Status = "In Review"
- Sort: Priority (P0 first)
- Layout: Board
- Group by: Assignee

**2. By Module**
- Filter: All
- Layout: Table
- Group by: Module
- Sort: Priority

**3. P0/P1**
- Filter: Priority = "P0" OR Priority = "P1"
- Sort: Priority, then Created
- Layout: List

**4. Bugs**
- Filter: Type = "Bug"
- Sort: Priority
- Layout: Table

**5. LLM Ready**
- Filter: LLM Ready = True AND Status = "Todo"
- Sort: Priority
- Layout: List

#### Setup Instructions

```bash
# Using GitHub CLI
gh project create --owner [OWNER] --title "[Project Name] Execution"

# Add fields (via web UI - no CLI support yet)
# Navigate to project settings > Fields
# Create custom fields as defined above

# Create views (via web UI)
# Navigate to project > Add view
# Configure filters and layout as defined above
```

### F. Feature Modeling Pattern

#### Parent Issue (Epic)

Create parent issue for large features:

**Title**: `[Epic] Add SSO Authentication`

**Labels**: `type:feature`, `priority:p1`

**Body**:
```markdown
## Overview
Implement SSO authentication for enterprise customers.

## Goals
- Support Google, GitHub, Microsoft SSO
- Maintain existing email/password auth
- Enterprise-grade security

## Child Tasks
- [ ] #101 - SSO provider abstraction
- [ ] #102 - Google OAuth integration
- [ ] #103 - GitHub OAuth integration
- [ ] #104 - Microsoft OAuth integration
- [ ] #105 - SSO UI components
- [ ] #106 - Session management updates
- [ ] #107 - Documentation

## Context
- Architecture: ./docs/architecture.md#auth
- ADR: ./docs/ADRs/0020-sso-strategy.md

## Acceptance Criteria
- [ ] All child tasks complete
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Deployed to production
```

#### Child Issues (Tasks)

Each child references parent:

**Title**: `Implement Google OAuth integration`

**Body includes**:
```markdown
## Parent Epic
Part of #100 (Add SSO Authentication)

## Context
[rest of issue template]
```

#### Linking Strategy

**In Parent**:
- List all child issues with checkboxes
- Update checkboxes as children complete

**In Child**:
- Reference parent in "Context" section
- Use "Part of #N" pattern

**In GitHub Projects**:
- Both parent and children in project
- Filter by parent issue to see epic progress

### G. Documentation Integration Strategy

#### Docs as Canonical Source

**Core Principle**: Never duplicate documentation into GitHub. Always link.

**Required Documentation**:

1. **`./docs/architecture.md`**
   - System architecture
   - Component relationships
   - Data flow
   - Link from issues: `./docs/architecture.md#relevant-section`

2. **`./docs/ADRs/`**
   - Architectural Decision Records
   - Format: `NNNN-decision-title.md`
   - Link from issues: `./docs/ADRs/0015-sso-implementation.md`

3. **`./docs/current-task.md`** (recommended)
   - Current development focus
   - Context for LLM sessions
   - Updated frequently
   - Link from issues when relevant

4. **`./docs/context-handoff.md`** (recommended)
   - Session handoff context
   - Recent decisions
   - Known issues
   - Link when onboarding to task

#### Linking Pattern

**In Issue Body**:
```markdown
## Context

### Documentation
- Architecture: `./docs/architecture.md#auth-system`
- ADR: `./docs/ADRs/0015-sso-implementation.md`
- Current work: `./docs/current-task.md`

### Code
- Implementation: `src/auth/sso/`
- Tests: `tests/auth/sso/`
- Config: `config/auth.ts`
```

**In PR Description**:
```markdown
## Context

### Documentation
- Architecture: `./docs/architecture.md#auth-system`
- ADR: `./docs/ADRs/0020-oauth-providers.md` (new)
- Updated docs: `./docs/api/auth.md`
```

#### Validation

**Issue Creation Checklist**:
- [ ] Context section present
- [ ] At least one doc link (architecture or ADR)
- [ ] Code scope identified
- [ ] No doc duplication in issue body

**PR Review Checklist**:
- [ ] Documentation links included
- [ ] New ADRs referenced if applicable
- [ ] Architecture docs updated if needed
- [ ] No orphaned context (everything linked)

### H. LLM Workflow

#### Standard Development Flow

```
1. Pick Issue
   ↓ (Filter: status:llm-ready, priority:p0/p1)
   
2. Read Issue
   ↓ (Parse: goal, context, scope, acceptance criteria)
   
3. Read Linked Docs
   ↓ (Follow links: architecture, ADRs, context)
   
4. Inspect Code
   ↓ (Navigate to files in scope)
   
5. Implement
   ↓ (Write code, tests)
   
6. Open PR
   ↓ (Link issue, include context)
   
7. Mark Issue Done
   ↓ (Close via PR merge)
```

#### LLM-Ready Criteria

An issue is ready for LLM implementation when ALL criteria met:

**✅ Clear Goal**:
- One-sentence summary
- Specific, measurable outcome
- Example: ✅ "Implement Google OAuth login"
- Example: ❌ "Fix auth" (too vague)

**✅ Context Linked**:
- Architecture doc section
- At least one ADR (if applicable)
- Related issues (if any)
- Example: ✅ Links to `./docs/architecture.md#auth`
- Example: ❌ No documentation links

**✅ Scope Defined**:
- Files/modules listed
- In scope / out of scope explicit
- Example: ✅ "In scope: src/auth/google.ts, Out: SAML"
- Example: ❌ "Auth module" (which files?)

**✅ Acceptance Criteria**:
- Checkbox list
- Testable conditions
- Example: ✅ "[ ] OAuth flow completes successfully"
- Example: ❌ "Make it work" (not testable)

**✅ No Blockers**:
- No `status:blocked` label
- No "Blocked by #N" in description
- Example: ✅ All dependencies resolved
- Example: ❌ "Blocked by #42 (API endpoint)"

**✅ Files Identified**:
- Specific file paths listed
- Test files included
- Example: ✅ "src/auth/google.ts, tests/auth/google.test.ts"
- Example: ❌ "Auth files" (which ones?)

#### Labeling

When issue meets all criteria:
```bash
# Add label via GitHub MCP or CLI
gh issue edit [NUMBER] --add-label "status:llm-ready"
```

When picked up for implementation:
```bash
gh issue edit [NUMBER] --remove-label "status:llm-ready"
```

### I. Monorepo / Multi-repo Strategy

#### One Repo as Control Center

**For Monorepos**:
- Primary repo = monorepo root
- All issues in root repository
- Labels include module tags
- Example:
  - Repo: `company/monorepo`
  - Issue: "Fix login bug" with `module:web` label

**For Multi-repo Systems**:
- Choose one repo as "control center"
- Usually: main app or API repo
- All cross-cutting issues tracked there
- Module-specific issues can be in individual repos

**Decision Matrix**:

| Scenario | Control Center | Module Issues |
|----------|---------------|---------------|
| Monorepo | Root repo | Root repo (with module labels) |
| Multi-repo (services) | API repo | API repo (reference other repos) |
| Multi-repo (frontend+backend) | Primary app | Primary app (reference backend repo) |
| Submodules | Parent repo | Parent repo (reference submodules) |

#### Cross-repo References

**Issue Body Pattern**:
```markdown
## Scope

### Repositories
- Primary: `company/web-app` (this repo)
- Backend: `company/api` - requires endpoint update
- Mobile: `company/mobile` - UI changes needed

### Files
**This repo** (`company/web-app`):
- src/auth/login.tsx
- tests/auth/login.test.tsx

**External** (`company/api`):
- See issue company/api#42
```

**Linking Pattern**:
- Use `owner/repo#number` format
- Example: "Requires company/api#42"
- Create issues in external repos when needed
- Link them bidirectionally

#### Module Labels

Generate module labels from repo structure:

**Monorepo Example**:
```
apps/
  web/         → module:web
  mobile/      → module:mobile
  admin/       → module:admin
services/
  api/         → module:api
  worker/      → module:worker
packages/
  ui/          → module:ui (or area:ui)
  utils/       → module:utils
```

**Multi-repo Example**:
```
company/web-app      → module:web
company/api          → module:api
company/mobile       → module:mobile
```

**Usage**:
- Add module label to every issue
- Filter project by module
- Track work by module
- Report on module progress

### J. .github-os.json Metadata File

#### Required File

Create at repository root: `.github-os.json`

#### Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["projectName", "docsDir", "issueTracking"],
  "properties": {
    "projectName": {
      "type": "string",
      "description": "Human-readable project name"
    },
    "docsDir": {
      "type": "string",
      "description": "Path to documentation directory",
      "default": "./docs"
    },
    "repos": {
      "type": "array",
      "description": "All repositories in this project",
      "items": {
        "type": "string"
      }
    },
    "modules": {
      "type": "array",
      "description": "Detected modules/packages/services",
      "items": {
        "type": "object",
        "required": ["name", "path", "type"],
        "properties": {
          "name": {
            "type": "string",
            "description": "Module name (e.g., 'web', 'api')"
          },
          "path": {
            "type": "string",
            "description": "Relative path from repo root"
          },
          "type": {
            "type": "string",
            "enum": ["app", "service", "package", "infra"],
            "description": "Module type"
          },
          "description": {
            "type": "string",
            "description": "Optional module description"
          }
        }
      }
    },
    "issueTracking": {
      "type": "string",
      "enum": ["github"],
      "description": "Issue tracking system"
    },
    "primaryRepo": {
      "type": "string",
      "description": "Primary repo for issue tracking (multi-repo only)"
    },
    "labels": {
      "type": "object",
      "description": "Custom label definitions",
      "properties": {
        "customTypes": {
          "type": "array",
          "items": {"type": "string"}
        },
        "customAreas": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "githubProject": {
      "type": "object",
      "description": "GitHub Project configuration",
      "properties": {
        "url": {
          "type": "string",
          "description": "GitHub Project URL"
        },
        "id": {
          "type": "number",
          "description": "GitHub Project ID"
        }
      }
    }
  }
}
```

#### Example: Single Repo

```json
{
  "projectName": "MyApp",
  "docsDir": "./docs",
  "repos": ["company/myapp"],
  "modules": [
    {
      "name": "web",
      "path": "./src",
      "type": "app",
      "description": "Web application"
    }
  ],
  "issueTracking": "github",
  "labels": {
    "customAreas": ["payments", "notifications"]
  }
}
```

#### Example: Monorepo

```json
{
  "projectName": "Platform",
  "docsDir": "./docs",
  "repos": ["company/platform"],
  "modules": [
    {
      "name": "web",
      "path": "./apps/web",
      "type": "app",
      "description": "Web application"
    },
    {
      "name": "mobile",
      "path": "./apps/mobile",
      "type": "app",
      "description": "Mobile app"
    },
    {
      "name": "api",
      "path": "./services/api",
      "type": "service",
      "description": "REST API"
    },
    {
      "name": "ui",
      "path": "./packages/ui",
      "type": "package",
      "description": "Shared UI components"
    }
  ],
  "issueTracking": "github",
  "githubProject": {
    "url": "https://github.com/orgs/company/projects/1",
    "id": 1
  }
}
```

#### Example: Multi-repo

```json
{
  "projectName": "E-commerce Platform",
  "docsDir": "./docs",
  "repos": [
    "company/web-app",
    "company/api",
    "company/mobile"
  ],
  "modules": [
    {
      "name": "web",
      "path": "./",
      "type": "app",
      "description": "Web storefront"
    }
  ],
  "issueTracking": "github",
  "primaryRepo": "company/web-app",
  "labels": {
    "customAreas": ["checkout", "inventory", "shipping"]
  }
}
```

#### Purpose

**For LLMs**:
- Quick project context
- Module discovery
- Docs location
- Repo topology

**For Tools**:
- Integration point for other tools
- Notion sync (future)
- Linear migration (future)
- Analytics (future)

**For Humans**:
- Project overview
- Module map
- Convention documentation

## Step 3: Execution Modes

### Design-Only Mode

**When to use**:
- Want to review before committing
- Exploring options
- Team decision needed

**Output**:
1. Complete analysis report
2. Label definitions (JSON)
3. Issue templates (markdown)
4. PR template (markdown)
5. .github-os.json (JSON)
6. Setup instructions (markdown)

**Action**:
- Output all content as markdown
- User manually creates files
- User manually creates labels

### Auto-Generate Mode

**When to use**:
- Ready to implement immediately
- Solo builder with authority
- Clear path forward

**Actions**:
1. ✅ Create .github-os.json
2. ✅ Create .github/ISSUE_TEMPLATE/ files
3. ✅ Create .github/pull_request_template.md
4. ✅ Create labels via GitHub MCP
5. ✅ Commit files
6. ⚠️ GitHub Project setup (manual - provide instructions)

**Process**:
```
1. Generate all files
   ↓
2. Show user for approval
   ↓
3. Commit to repo
   ↓
4. Create labels via MCP
   ↓
5. Provide Project setup instructions
   ↓
6. Validate system
```

## Step 4: GitHub MCP Integration

### Primary Tool

> **Global tool preference**: **`gh` CLI is preferred** over GitHub MCP for all GitHub operations in this workflow. `gh` CLI is always available, supports all required operations (including `project item-add` which MCP does not), and produces predictable output. Use MCP only as a fallback when `gh` CLI is unavailable.

### Installation Check

```markdown
Before proceeding, verify tools are available (in order of preference):

1. gh CLI: Run `gh auth status` — if authenticated, use gh CLI for all operations
2. GitHub MCP: Check if MCP tools are visible — use as fallback if gh CLI unavailable
3. Neither: Output manual instructions

See `assets/github-mcp-setup.md` for MCP installation if needed.
```

### MCP Operations

#### Creating Labels

```javascript
// Via GitHub MCP
mcp3_create_label({
  owner: "company",
  repo: "myapp",
  name: "type:feature",
  color: "0e8a16",
  description: "New features"
})
```

#### Creating Issues

```javascript
// Via GitHub MCP
mcp3_issue_write({
  method: "create",
  owner: "company",
  repo: "myapp",
  title: "Implement SSO authentication",
  body: "[full issue body]",
  labels: ["type:feature", "priority:p1", "module:api"],
  type: "Feature" // if org has issue types
})
```

#### Creating Files

```javascript
// Via GitHub MCP
mcp3_create_or_update_file({
  owner: "company",
  repo: "myapp",
  path: ".github/ISSUE_TEMPLATE/task.yml",
  content: "[template content]",
  message: "Add GitHub OS issue template",
  branch: "main"
})
```

### Fallback: GitHub CLI

If MCP unavailable, use `gh` CLI:

```bash
# Create label
gh label create "type:feature" \
  --color "0e8a16" \
  --description "New features"

# Create issue
gh issue create \
  --title "Implement SSO authentication" \
  --body-file issue-body.md \
  --label "type:feature,priority:p1"

# Create file (via commit)
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="Add template" \
  -f content="$(base64 < file.yml)"
```

### Tool Selection Logic

```
1. Check: GitHub MCP available?
   ↓ YES
   Use MCP for all operations
   
   ↓ NO
2. Check: GitHub CLI available?
   ↓ YES
   Use gh CLI
   
   ↓ NO
3. Output manual instructions
```

## Step 5: Implementation Process

### Full Flow

#### 1. Analyze Repository

```
→ Run repository analysis
→ Detect type, modules, docs
→ Generate analysis report
→ Present to user
→ Get confirmation
```

#### 2. Design System

```
→ Design label taxonomy
→ Generate module labels
→ Design issue templates
→ Design PR template
→ Generate .github-os.json
→ Present complete design
→ Get approval
```

#### 3. Execute

**Design-Only**:
```
→ Output all files as markdown
→ Output label creation script
→ Output setup instructions
→ Done
```

**Auto-Generate**:
```
→ Create .github-os.json
→ Create .github/ISSUE_TEMPLATE/ files
→ Create .github/pull_request_template.md
→ Commit files
→ Create labels via MCP/CLI
→ Provide Project setup guide
→ Validate
→ Done
```

#### 4. Validate

```
→ Check: .github-os.json exists
→ Check: Templates exist
→ Check: Labels created
→ List: Next steps
→ Done
```

### Checkpoints

**After Analysis**:
```
"Repository analysis complete. Found [N] modules in [type] repo.
Proceed with GitHub OS design?"
```

**After Design**:
```
"GitHub OS design complete:
- [N] labels (type, priority, area, module, status)
- [N] issue templates
- 1 PR template
- .github-os.json configured

Choose execution mode:
1. Design-only (output files for manual creation)
2. Auto-generate (create files + labels automatically)
"
```

**After Execution**:
```
"GitHub OS setup complete:
✅ .github-os.json created
✅ Issue templates created
✅ PR template created
✅ [N] labels created

Next steps:
1. Create GitHub Project (manual)
2. Seed initial issues
3. Start using the system

Validation report:
[show validation results]
"
```

## Anti-patterns

### ❌ Unstructured Issues

**Wrong**:
```
Title: Fix auth
Body: auth is broken
```

**Right**:
```
Title: Login fails with SSO enabled
Labels: type:bug, priority:p0, module:api
Body:
## Description
SSO login redirects to 404

## Context
- Architecture: ./docs/architecture.md#auth
- ADR: ./docs/ADRs/0015-sso.md

## Steps to Reproduce
1. Click "Sign in with Google"
2. Complete OAuth
3. Redirect fails

[etc.]
```

### ❌ Missing Context

**Wrong**:
```
## Context
Not provided
```

**Right**:
```
## Context
- Architecture: ./docs/architecture.md#payment-flow
- ADR: ./docs/ADRs/0023-stripe-integration.md
- Related: #45, #47
- Code: src/payments/, tests/payments/
```

### ❌ No Module Labeling

**Wrong**:
```
Labels: bug
```

**Right** (monorepo):
```
Labels: type:bug, priority:p1, module:api
```

### ❌ Splitting Issues Across Repos

**Wrong** (multi-repo):
```
Repo A: Issue #1 "Fix login (frontend)"
Repo B: Issue #2 "Fix login (backend)"
```

**Right**:
```
Primary Repo: Issue #1 "Fix login"
- Scope includes frontend (this repo) + backend (repo-b)
- Links to repo-b if separate issue needed there
```

### ❌ Duplicating Docs

**Wrong**:
```
## Architecture

[paste entire architecture.md into issue]
```

**Right**:
```
## Context
Architecture: ./docs/architecture.md#relevant-section
```

### ❌ GitHub as Wiki

**Wrong**:
- Storing design docs in issue comments
- Long discussions in issues
- Using issues as documentation

**Right**:
- Design docs in ./docs/
- Decisions in ADRs
- Issues reference docs, not replace them

## Integration with github-issues Skill

This skill **extends** the github-issues skill:

### Use github-issues for:
- Creating individual issues
- Updating existing issues
- Querying issues
- Standard CRUD operations

### Use github-os for:
- Initial system setup
- Label taxonomy design
- Template creation
- System-wide conventions
- Multi-repo coordination
- Docs integration strategy

### Combined Workflow:

```
1. Setup: Use github-os
   → Design label system
   → Create templates
   → Establish conventions

2. Daily use: Use github-issues
   → Create issues with templates
   → Update issue status
   → Query issues

3. Maintenance: Use github-os
   → Add new modules
   → Update templates
   → Refine system
```

## Examples

### Example 1: Single Repo Setup

**Input**:
```
Repository: company/myapp
Structure:
  src/
  tests/
  docs/
```

**Output**:

**Analysis**:
```
Type: Single repository
Modules: 1 (main app)
Docs: Rich (./docs with architecture + ADRs)
```

**Labels** (10):
- type:feature, type:bug, type:chore, type:research
- priority:p0, priority:p1, priority:p2, priority:p3
- area:ui, area:engine

**.github-os.json**:
```json
{
  "projectName": "MyApp",
  "docsDir": "./docs",
  "repos": ["company/myapp"],
  "modules": [
    {
      "name": "main",
      "path": "./src",
      "type": "app"
    }
  ],
  "issueTracking": "github"
}
```

### Example 2: Monorepo Setup

**Input**:
```
Repository: company/platform
Structure:
  apps/
    web/
    mobile/
  services/
    api/
    worker/
  packages/
    ui/
  docs/
```

**Output**:

**Analysis**:
```
Type: Monorepo
Modules: 5
  - web (app)
  - mobile (app)
  - api (service)
  - worker (service)
  - ui (package)
Docs: Rich
```

**Labels** (17):
- type:* (4)
- priority:* (4)
- area:* (6)
- module:web, module:mobile, module:api, module:worker, module:ui

**.github-os.json**:
```json
{
  "projectName": "Platform",
  "docsDir": "./docs",
  "repos": ["company/platform"],
  "modules": [
    {"name": "web", "path": "./apps/web", "type": "app"},
    {"name": "mobile", "path": "./apps/mobile", "type": "app"},
    {"name": "api", "path": "./services/api", "type": "service"},
    {"name": "worker", "path": "./services/worker", "type": "service"},
    {"name": "ui", "path": "./packages/ui", "type": "package"}
  ],
  "issueTracking": "github"
}
```

### Example 3: LLM-Ready Issue

```
Title: Implement Google OAuth login

Labels:
- type:feature
- priority:p1
- module:api
- status:llm-ready

Body:
## Summary
Add Google OAuth as login method

## Context

### Documentation
- Architecture: ./docs/architecture.md#auth-system
- ADR: ./docs/ADRs/0015-oauth-strategy.md
- Current task: ./docs/current-task.md

### Related
- Blocked by: None
- Blocks: #45 (UI for OAuth button)
- Related: #40 (GitHub OAuth - same pattern)

## Scope

### In Scope
- Google OAuth provider implementation
- Token exchange and validation
- User account creation/lookup
- Session creation

### Out of Scope
- UI changes (separate issue #45)
- Other OAuth providers (GitHub: #40, Microsoft: #46)
- Email verification (handled separately)

### Files
- src/auth/oauth/google.ts (new)
- src/auth/oauth/provider.ts (modify)
- tests/auth/oauth/google.test.ts (new)
- config/oauth.ts (modify)

## Goal
Users can authenticate using their Google account via OAuth 2.0 flow.

## Constraints
- Must use passport-google-oauth20 library
- Must not break existing email/password auth
- Session handling unchanged (use existing SessionService)
- Error handling must match existing patterns

## Acceptance Criteria
- [ ] Google OAuth provider class implemented
- [ ] Token exchange working
- [ ] User lookup/creation working
- [ ] Session created on success
- [ ] Error handling for invalid tokens
- [ ] Error handling for API failures
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration test passes
- [ ] Documented in ./docs/api/auth.md
```

## Related Skills

- **github-issues**: Day-to-day issue management (use alongside this)
- **lesson-decision-records**: Document mistakes and learnings
- **architecture-decision-records**: Document design decisions (ADRs)

## Troubleshooting

### GitHub MCP Not Available

```
Error: GitHub MCP tools not found

Solution:
1. Install GitHub MCP: npm install -g @modelcontextprotocol/server-github
2. Configure MCP in IDE settings
3. Restart IDE
4. See: ./assets/github-mcp-setup.md
```

### Labels Already Exist

```
Error: Label "type:feature" already exists

Solution:
1. Check existing labels: gh label list
2. Delete conflicting labels: gh label delete "type:feature"
3. Or: Skip label creation, use existing
```

### Permission Denied

```
Error: Permission denied creating labels

Solution:
1. Check repo permissions (need write access)
2. Check GitHub token scopes (need 'repo' scope)
3. Authenticate: gh auth refresh -s repo
```

## Best Practices

### Label Hygiene
- **Consistent naming**: Always use `category:value` format
- **Color coding**: Use standard colors for visual scanning
- **Description**: Every label needs clear description
- **No orphans**: Don't create labels never used

### Issue Quality
- **Context first**: Always link to docs before describing
- **Scope explicit**: List exact files, not vague descriptions
- **Testable criteria**: Acceptance criteria must be verifiable
- **One goal**: Each issue = one coherent change

### Template Evolution
- **Start simple**: Use provided templates as-is initially
- **Iterate based on use**: Adjust after 10+ issues created
- **Team input**: Get feedback from all team members
- **Version in git**: Templates in .github/ tracked like code

### Docs Discipline
- **Write docs first**: Architecture + ADRs before issues
- **Keep current**: Update docs as you implement
- **Link generously**: Over-link rather than under-link
- **Never duplicate**: If it's in docs, link to docs

## Version History

- **v1.0**: Initial release
  - Single repo, monorepo, multi-repo support
  - GitHub MCP integration
  - LLM-optimized workflows
  - Docs integration strategy
