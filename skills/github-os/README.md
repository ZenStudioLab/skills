# GitHub OS

Set up GitHub as your project's Operating System - treating GitHub as the execution layer integrated with repository documentation as the knowledge layer. Optimized for LLM-driven development workflows.

## Overview

**GitHub OS** is a skill that helps you design and implement a complete GitHub-based execution system for your software project. It analyzes your repository structure and creates a tailored system of labels, templates, and conventions that work seamlessly with your documentation.

### Core Philosophy

- **GitHub = Execution OS**: Issues, projects, labels, PRs
- **Docs (./docs) = Knowledge OS**: Architecture, ADRs, context
- **LLM = Connector**: Links execution to knowledge

## Why Use This?

### For Solo Builders
- Start with a minimal but complete system
- Scale gradually as your project grows
- Optimized for LLM-assisted development
- Clear structure without bureaucracy

### For Teams
- Standardized issue tracking
- Clear module boundaries
- Documentation-first approach
- Scalable from solo to team

### For LLM Workflows
- Issues are LLM-ready by default
- Explicit context linking
- Clear scope boundaries
- Minimal ambiguity

## Installation

### Option 1: CLI Install (Recommended)

```bash
npx skills add ZenStudioLab/skills --skill github-os
```

### Option 2: Manual Copy

```bash
git clone https://github.com/ZenStudioLab/skills.git
cp -r skills/skills/github-os ~/.agents/skills/
```

## Quick Start

### 1. Install GitHub MCP

GitHub OS uses GitHub MCP as its primary tool:

```bash
npm install -g @modelcontextprotocol/server-github
```

See `assets/github-mcp-setup.md` for detailed setup.

### 2. Ask Your AI Agent

```
"Set up GitHub OS for this repository"
```

The skill will:
1. Analyze your repo structure
2. Design a complete GitHub system
3. Create labels, templates, and metadata
4. Guide you through setup

### 3. Choose Execution Mode

**Design-Only Mode**: Review designs before creating
**Auto-Generate Mode**: Create everything automatically

## What Gets Created

### Files
- `.github-os.json` - Project metadata
- `.github/ISSUE_TEMPLATE/task.yml` - Task template
- `.github/ISSUE_TEMPLATE/bug.yml` - Bug template
- `.github/ISSUE_TEMPLATE/feature.yml` - Feature template
- `.github/pull_request_template.md` - PR template

### Labels
- **Type**: feature, bug, chore, research
- **Priority**: p0, p1, p2, p3
- **Area**: ui, engine, seo, infra, dx, docs, security, performance
- **Module**: (auto-generated from your repo structure)
- **Status**: blocked, llm-ready, needs-context

### Conventions
- Issue structure
- PR format
- Documentation linking
- LLM-ready criteria

## Use Cases

### Starting a New Project

```
"I'm starting a new project. Set up GitHub OS."
```

Gets you a complete issue tracking system from day one.

### Restructuring Existing Project

```
"Our issue tracking is chaotic. Help me set up GitHub OS."
```

Analyzes your current structure and designs a clean system.

### Monorepo Setup

```
"Set up GitHub OS for our monorepo with apps, services, and packages."
```

Creates module labels and cross-module issue patterns.

### Multi-repo Coordination

```
"We have 3 repos. Set up GitHub OS with one as the control center."
```

Designs cross-repo issue tracking strategy.

## Examples

### Example 1: Single Repository

**Input**: Simple web app with `src/`, `tests/`, `docs/`

**Output**: 
- 10 labels (type, priority, area)
- 3 issue templates
- 1 PR template
- `.github-os.json` configuration

### Example 2: Monorepo

**Input**: Monorepo with `apps/`, `services/`, `packages/`

**Output**:
- 18+ labels (including module labels)
- Cross-module issue examples
- GitHub Projects configuration
- `.github-os.json` with all modules

### Example 3: Multi-repo

**Input**: 3 separate repos (frontend, backend, mobile)

**Output**:
- Primary repo as control center
- Cross-repo reference patterns
- Unified label system
- `.github-os.json` with all repos

## Key Features

### Automatic Module Detection

Detects modules from:
- `apps/`, `services/`, `packages/` directories
- Git submodules
- Workspace configurations (package.json, pnpm-workspace.yaml)
- Build tool configs (nx.json, turbo.json)

### LLM-Ready Issues

Every issue template includes:
- **Context section**: Links to docs, ADRs, related issues
- **Scope section**: Explicit in/out scope, file list
- **Goal**: Clear, measurable outcome
- **Constraints**: Technical and business constraints
- **Acceptance criteria**: Testable conditions

### Documentation Integration

Issues never duplicate docs - they link to them:
- Architecture: `./docs/architecture.md#section`
- ADRs: `./docs/ADRs/NNNN-decision.md`
- Context: `./docs/current-task.md`

### GitHub Projects Integration

Defines project views:
- Current Work (in progress items)
- By Module (organized by module)
- P0/P1 (high priority items)
- Bugs (all bugs)
- LLM Ready (ready to pick up)

## Integration with Other Skills

### Works With

- **github-issues**: Day-to-day issue management
- **lesson-decision-records**: Document learnings
- **architecture-decision-records**: Document decisions

### Workflow

1. **Setup**: Use `github-os` to design system
2. **Daily use**: Use `github-issues` to create/update issues
3. **Maintenance**: Use `github-os` to refine system

## Repository Types Supported

### ✅ Single Repository
Standard single-codebase projects

### ✅ Monorepo
- Turborepo
- Nx
- Lerna
- pnpm workspaces
- Yarn workspaces

### ✅ Multi-repo Systems
- Microservices
- Frontend + Backend split
- Multiple related projects

### ✅ Submodules
Git submodules treated as modules or separate projects

## Requirements

### Required
- GitHub repository with write access
- GitHub MCP server (or GitHub CLI as fallback)

### Recommended
- Documentation directory (`./docs`)
- Architecture documentation
- ADRs (Architectural Decision Records)

### Optional
- GitHub CLI (`gh`) for fallback operations
- Existing issue types (org-level GitHub feature)

## Execution Modes

### Design-Only Mode

**When**: Want to review before committing

**Output**:
- Analysis report
- Label definitions
- Template files
- Setup instructions

**Action**: Manual implementation

### Auto-Generate Mode

**When**: Ready to implement immediately

**Actions**:
1. ✅ Create `.github-os.json`
2. ✅ Create issue templates
3. ✅ Create PR template
4. ✅ Create labels via GitHub MCP
5. ✅ Commit files
6. ⚠️ Provide GitHub Projects setup guide (manual)

## Best Practices

### Label Hygiene
- Use consistent `category:value` format
- Standard colors for visual consistency
- Clear descriptions on every label
- Don't create unused labels

### Issue Quality
- Always link to documentation
- List exact files, not vague descriptions
- Testable acceptance criteria
- One coherent goal per issue

### Documentation Discipline
- Write architecture docs first
- Keep docs current as you implement
- Link generously from issues
- Never duplicate docs into issues

### Template Evolution
- Start with provided templates
- Iterate after 10+ real issues
- Get team feedback
- Version templates in git

## Troubleshooting

### GitHub MCP Not Available

**Error**: `GitHub MCP tools not found`

**Solution**:
1. Install: `npm install -g @modelcontextprotocol/server-github`
2. Configure MCP in IDE settings
3. See `assets/github-mcp-setup.md`

### Labels Already Exist

**Error**: `Label "type:feature" already exists`

**Solution**:
1. Check existing labels: `gh label list`
2. Delete if needed: `gh label delete "type:feature"`
3. Or skip label creation

### Permission Denied

**Error**: `Permission denied creating labels`

**Solution**:
1. Verify repo write access
2. Check GitHub token scopes (need `repo`)
3. Authenticate: `gh auth refresh -s repo`

## Anti-patterns to Avoid

### ❌ Unstructured Issues
Don't create vague issues without context

### ❌ Missing Context
Every issue needs doc links

### ❌ No Module Labels
Tag issues with affected modules

### ❌ Splitting Issues Across Repos
Use one control center for multi-repo systems

### ❌ Duplicating Docs
Link to docs, don't copy them into issues

### ❌ GitHub as Wiki
Store documentation in `./docs`, not issues

## Examples in Action

See `assets/examples/` for:
- `single-repo-analysis.md` - Single repo setup
- `monorepo-analysis.md` - Monorepo setup
- `github-os-config-examples.json` - Config examples
- `sample-llm-ready-issue.md` - Perfect LLM-ready issue

## Resources

### Documentation
- [SKILL.md](SKILL.md) - Complete skill reference
- [GitHub MCP Setup](assets/github-mcp-setup.md) - MCP installation
- [Label Definitions](assets/label-definitions.json) - Label taxonomy

### Templates
- [Task Template](assets/issue-templates/task.yml)
- [Bug Template](assets/issue-templates/bug.yml)
- [Feature Template](assets/issue-templates/feature.yml)
- [PR Template](assets/pr-template/pull_request_template.md)

## FAQ

### Q: Do I need a docs directory?

**A**: Not required, but highly recommended. The system works best with `./docs` containing architecture.md and ADRs.

### Q: Can I customize the labels?

**A**: Yes! Modify `assets/label-definitions.json` or add custom areas/types to `.github-os.json`.

### Q: What if I already have labels?

**A**: The skill will detect existing labels and either skip creation or help you merge/update them.

### Q: Does this work with GitHub Projects (beta)?

**A**: Yes! The skill provides configuration for the new GitHub Projects with custom fields and views.

### Q: Can I use this with Linear/Jira?

**A**: GitHub OS is GitHub-specific, but the `.github-os.json` format is designed for future integrations with other tools.

### Q: What about GitHub issue types?

**A**: If your org has issue types configured, the skill will use them instead of type labels (following GitHub's recommendation).

### Q: Is this overkill for small projects?

**A**: No! Start with design-only mode and create just what you need. The system scales from minimal to comprehensive.

## Contributing

Found a way to improve this skill? Have a suggestion?

1. Open an issue: https://github.com/ZenStudioLab/skills/issues
2. Submit a PR: https://github.com/ZenStudioLab/skills/pulls

## License

MIT - Use this however you want.

## Version

**v1.0** - Initial release
- Single repo, monorepo, multi-repo support
- GitHub MCP integration
- LLM-optimized workflows
- Documentation integration strategy

---

Built by [Toan (zenji) Nguyen](https://zenstudio.cv)
