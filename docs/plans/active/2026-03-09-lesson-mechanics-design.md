# Lesson Mechanics Design

> **Goal:** Establish a standardized system for AI to record and learn from mistakes across global and project-level contexts, with an ADR-style index.

## Architecture

The system uses a decentralized Markdown-based ADR (Architecture Decision Record) style. Lessons are stored in two primary locations to balance universal standards with project-specific nuances.

### Storage Locations
- **Global:** `~/.agents/lessons/` (Universal engineering standards).
- **Project:** `[project-root]/.agents/lessons/` (Local context, versioned with the codebase).

### Directory Indexing (`README.md`)
Each `lessons/` directory MUST contain a `README.md` that serves as:
1. An explanation of the directory's purpose.
2. A table of contents/index of all recorded lessons.
3. Instructions for other CLI tools on how to consume these lessons.

## File Structure (Markdown-ADR)

Each lesson file follows the naming convention `NNNN-slug.md` and contains structured frontmatter for machine-readability.

### Content Template
```markdown
---
type: lesson
scope: [global|project]
tags: [category1, category2]
date: YYYY-MM-DD
severity: [low|medium|high]
---

# [Descriptive Title]

## 1. Context
Summary of the task and environment.

## 2. Mistake
Description of the specific error or anti-pattern encountered.

## 3. Root Cause
Technical explanation of why the mistake occurred.

## 4. Correction
The code change or architectural shift that resolved the issue.

## 5. Prevention Rule
A concise, mandatory rule for future AI sessions to prevent recurrence.
```

## Workflow
1. **Trigger:** AI identifies a significant bug, refactor, or "hard-learned" fix.
2. **Proposal:** AI suggests recording a lesson (Global vs Project).
3. **Approval:** User confirms or edits the scope.
4. **Persistence:** AI generates the `NNNN-slug.md` file and updates the `README.md` index.
5. **Retrieval:** Future sessions (or other CLI tools) index these directories to load "contextual memory."
