# Plan Review — Peer LLM Workflow

Part of the [Peer LLMs](../README.md) skill for inter-LLM collaboration workflows.

## Overview

Reviews a technical plan via a coding agent (default: Codex) and iteratively refines it. Use `opencode` prefix to override provider.

## Workflow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'clusterBkg': 'transparent', 'background': 'transparent', 'primaryColor': '#FFF7E6', 'primaryTextColor': '#5A3A00', 'primaryBorderColor': '#F59E0B', 'lineColor': '#6366F1', 'secondaryColor': '#E8F5FF', 'tertiaryColor': '#F3E8FF'}}}%%
flowchart TB
  classDef user fill:#E8F5FF,stroke:#1B6EF3,stroke-width:2px,color:#0B2A5B,stroke-dasharray: 0;
  classDef orchestrator fill:#FFF7E6,stroke:#F59E0B,stroke-width:2px,color:#5A3A00,stroke-dasharray: 0;
  classDef agent fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#2E1065,stroke-dasharray: 0;
  classDef decision fill:#FFFFFF,stroke:#6366F1,stroke-width:2px,color:#111827,stroke-dasharray: 5 5;

  subgraph P1["Phase 1: Plan Review"]
    U1["User: Submit Plan"]:::user
    O1["Orchestrator: Delegate to Agent for Critical Review"]:::orchestrator
    X1["Agent: Output Review (10+ issues)"]:::agent
    O2["Orchestrator: Evaluate & Refine Plan"]:::orchestrator
    D1{"Status?"}:::decision
    U1 --> O1 --> X1 --> O2 --> D1
    D1 -- "NEEDS_REVISION" --> O1
  end

  subgraph P2["Phase 2: Plan Execute"]
    O3["Orchestrator: Dispatch batch to Agent"]:::orchestrator
    X2["Agent: Implement code changes"]:::agent
    O4["Orchestrator: Code Review"]:::orchestrator
    D2{"Verdict?"}:::decision
    Done([Complete]):::decision
    O3 --> X2 --> O4 --> D2
    D2 -- "NEEDS_FIX" --> X2
    D2 -- "APPROVED" --> Done
  end

  D1 -- "APPROVED" --> O3
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Adversarial** | Coding agent acts as a "nitpicker" — its job is to find flaws |
| **Iterative** | Multiple rounds of back-and-forth until quality gates pass |
| **Role Separation** | User defines what, orchestrator (Claude/any LLM) coordinates how, coding agent executes |
| **Feedback Loops** | Review → Fix → Re-review cycles |
| **Provider Override** | Use `opencode` prefix to switch from default Codex to OpenCode |

## Three Loops

- **Loop A (Plan Refinement)**: Review finds issues → Refine plan → Re-review → APPROVED
- **Loop B (Code Fixing)**: Code review finds bugs → Agent fixes → Re-review → APPROVED
- **Loop C (Batch Processing)**: Complete current batch → Next batch → All done

## Usage

```
/plan-review plans/my-feature-plan.md
/plan-review opencode plans/my-feature-plan.md
```

## See Also

- [Codex CLI](../codex/README.md) — Default coding agent for plan review
- [OpenCode CLI](../opencode/README.md) — Alternative coding agent (use `opencode` prefix)
- [Plan Execute](../plan-execute/README.md) — Executes plans after review is approved
