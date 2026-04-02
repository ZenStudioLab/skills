# AI Agent Skills

A collection of AI agent skills focused on testing, development, and engineering tasks. Built for developers who want AI coding agents to help with E2E testing, systematic learning, and code quality. Works with any agent that supports the Agent Skills spec.

Built by [Toan (zenji) Nguyen](https://zenstudio.cv)

Contributions welcome! Found a way to improve a skill or have a new one to add? Open a PR.

Run into a problem or have a question? Open an issue — we're happy to help.

## What are Skills?
Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you add these to your project, your agent can recognize when you're working on a task and apply the right frameworks and best practices.

## 🚀 Active Skills
- **GitHub OS**: Set up GitHub as your project's Operating System - execution layer integrated with docs as knowledge layer, optimized for LLM workflows.
- **Playwright Extension Testing**: Gold-standard E2E for MV3/WXT extensions.
- **Peer LLMs**: Inter-LLM collaboration — includes Codex CLI delegation, plan-review, and plan-execute workflows.
- **Lesson Decision Records**: Systematic recording of AI mistakes and learnings using ADR-inspired format.
- **Context Hub Get API Docs**: Fetch current API documentation for third-party libraries and SDKs via chub CLI.

## Installation

### Option 1: CLI Install (Recommended)
Use `npx skills` to install skills directly:

```bash
# Install all skills
npx skills add ZenStudioLab/skills

# Install specific skills
npx skills add ZenStudioLab/skills --skill lesson-decision-records
npx skills add ZenStudioLab/skills --skill get-api-docs

# List available skills
npx skills add ZenStudioLab/skills --list
```

This automatically installs to your `.agents/skills/` directory.

### Option 2: Clone and Copy
Clone the entire repo and copy the skills folder:

```bash
git clone https://github.com/ZenStudioLab/skills.git
cp -r skills/skills/* .agents/skills/
```

### Option 3: Git Submodule
Add as a submodule for easy updates:

```bash
git submodule add https://github.com/ZenStudioLab/skills.git .agents/zenstudiolab-skills
```
Then reference skills from `.agents/zenstudiolab-skills/skills/`.

## 🛠️ Usage
Integrated via [skills.sh](https://skills.sh).

Once installed, just ask your agent to help with tasks:

"Set up GitHub OS for this repository"
→ Uses GitHub OS skill

"Help me set up Playwright E2E testing for my MV3 extension"
→ Uses Playwright Extension Testing skill

"Delegate this refactoring to Codex CLI"
→ Uses Peer LLMs skill (Codex integration)

"/plan-review ./plans/my-feature.md"
→ Uses Peer LLMs skill (plan-review)

"/plan-execute ./plans/my-feature.md"
→ Uses Peer LLMs skill (plan-execute)

"Create a Lesson Decision Record for a recent bug"
→ Uses Lesson Decision Records skill

"Get the latest OpenAI API documentation"
→ Uses Context Hub Get API Docs skill

## Peer LLMs

Inter-LLM collaboration workflows — enabling AI agents to delegate, review, and execute tasks across different LLM providers.

### Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| **Codex CLI** | Delegates coding tasks to Codex CLI for execution. Great for batch refactoring, code generation, multi-file changes. | `ask_codex.sh "Your request"` |
| **plan-review** | Reviews a technical plan via Codex and iteratively refines it. Uses adversarial review to improve plan quality before implementation. | `/plan-review <plan-file-path>` |
| **plan-execute** | Executes a finalized plan by delegating coding to Codex. Claude orchestrates, Codex codes, Claude reviews — iterating until quality passes. | `/plan-execute <plan-file-path>` |

### Workflow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'clusterBkg': 'transparent', 'background': 'transparent', 'primaryColor': '#FFF7E6', 'primaryTextColor': '#5A3A00', 'primaryBorderColor': '#F59E0B', 'lineColor': '#6366F1', 'secondaryColor': '#E8F5FF', 'tertiaryColor': '#F3E8FF'}}}%%
flowchart TB
  classDef user fill:#E8F5FF,stroke:#1B6EF3,stroke-width:2px,color:#0B2A5B,stroke-dasharray: 0;
  classDef claude fill:#FFF7E6,stroke:#F59E0B,stroke-width:2px,color:#5A3A00,stroke-dasharray: 0;
  classDef codex fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#2E1065,stroke-dasharray: 0;
  classDef decision fill:#FFFFFF,stroke:#6366F1,stroke-width:2px,color:#111827,stroke-dasharray: 5 5;

  subgraph P1["Phase 1: Plan Review"]
    U1["User: Submit Plan"]:::user
    C1["Claude: Delegate to Codex for Critical Review"]:::claude
    X1["Codex: Output Review (10+ issues)"]:::codex
    C2["Claude: Evaluate & Refine Plan"]:::claude
    D1{"Status?"}:::decision
    U1 --> C1 --> X1 --> C2 --> D1
    D1 -- "NEEDS_REVISION" --> C1
  end

  subgraph P2["Phase 2: Plan Execute"]
    C3["Claude: Dispatch batch to Codex"]:::claude
    X2["Codex: Implement code changes"]:::codex
    C4["Claude: Code Review"]:::claude
    D2{"Verdict?"}:::decision
    Done([Complete]):::decision
    C3 --> X2 --> C4 --> D2
    D2 -- "NEEDS_FIX" --> X2
    D2 -- "APPROVED" --> Done
  end

  D1 -- "APPROVED" --> C3
```

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Adversarial** | Codex acts as a "nitpicker" — its job is to find flaws |
| **Iterative** | Multiple rounds of back-and-forth until quality gates pass |
| **Role Separation** | User defines what, Claude orchestrates how, Codex executes |
| **Feedback Loops** | Review → Fix → Re-review cycles |

### Three Loops

- **Loop A (Plan Refinement)**: Review finds issues → Refine plan → Re-review → APPROVED
- **Loop B (Code Fixing)**: Code review finds bugs → Codex fixes → Re-review → APPROVED
- **Loop C (Batch Processing)**: Complete current batch → Next batch → All done

## 🏗️ Structure
- `skills/`: Specialized skill packages.

## Contributing
Found a way to improve a skill? Have a new skill to suggest? PRs and issues welcome!

## License
MIT - Use these however you want.