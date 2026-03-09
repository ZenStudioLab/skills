# Lessons Learned

This directory contains lessons learned from mistakes, bugs, and refactors. Each lesson documents what went wrong, why it happened, and how to prevent it from happening again.

## Purpose

- **Scope**: [Global lessons apply to all projects | Project-specific lessons for this codebase]
- **Audience**: AI agents and developers working on [this project | any software project]
- **Maintenance**: Automatically updated when new lessons are recorded

## Quick Reference

**Total Lessons**: [N]  
**Last Updated**: [YYYY-MM-DD]

## Lessons by Severity

### 🔴 High Severity

Critical issues: data loss, security vulnerabilities, production incidents

| ID | Title | Tags | Date |
|----|-------|------|------|
| [0001](0001-example.md) | Example High Severity Lesson | tag1, tag2 | 2024-03-15 |

### 🟡 Medium Severity

Significant issues: performance problems, incorrect business logic, API misuse

| ID | Title | Tags | Date |
|----|-------|------|------|
| [0002](0002-example.md) | Example Medium Severity Lesson | tag1, tag2 | 2024-03-16 |

### 🟢 Low Severity

Minor issues: suboptimal implementations, style violations with impact

| ID | Title | Tags | Date |
|----|-------|------|------|
| [0003](0003-example.md) | Example Low Severity Lesson | tag1, tag2 | 2024-03-17 |

## By Topic (Tag Index)

Quick links to find lessons by domain:

- **async**: [0001](0001-example.md), [0005](0005-example.md)
- **database**: [0003](0003-example.md)
- **error-handling**: [0001](0001-example.md), [0007](0007-example.md)
- **performance**: [0004](0004-example.md)
- **react**: [0002](0002-example.md), [0006](0006-example.md)
- **security**: [0008](0008-example.md)
- **testing**: [0009](0009-example.md)

## For AI Agents

Before implementing features, review relevant lessons:

### Checklist by Task Type

**Async/Concurrent Operations**:
- Review lessons tagged: `async`, `concurrency`, `race-condition`
- Check high-severity lessons in this category

**Database Work**:
- Review lessons tagged: `database`, `transactions`, `migrations`, `deadlock`
- Pay special attention to transaction handling

**API Development**:
- Review lessons tagged: `rest-api`, `graphql`, `versioning`, `breaking-change`
- Check for integration-specific gotchas

**Frontend Development**:
- Review lessons tagged: `react`, `vue`, `state-management`, `dom`
- Look for component lifecycle issues

**Security Changes**:
- **ALWAYS** review all lessons tagged: `security`, `auth`, `xss`, `injection`
- No exceptions - security lessons are mandatory reading

## How to Use

### When Starting a Task
1. Identify relevant tags for your work
2. Scan the tag index above
3. Read matching lessons (prioritize high-severity)
4. Apply prevention rules to your implementation

### When Debugging
1. Search lesson files for similar error messages
2. Check lessons with related tags
3. Compare your symptoms to documented mistakes
4. Try documented corrections

### When Proposing a New Lesson
1. Check for duplicates by searching existing lessons
2. Determine severity based on impact
3. Choose 2-5 relevant tags
4. Use next sequential number (NNNN)
5. Update this index after recording

## Maintenance

This index is automatically maintained by the AI agent when recording new lessons. Manual updates should preserve:
- Severity grouping (high → medium → low)
- Chronological order within each severity
- Tag index alphabetical ordering
- Total lesson count

---

**Related**: See `.agents/architecture/` for architectural decision records (ADRs)
