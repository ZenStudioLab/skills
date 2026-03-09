---
name: lesson-decision-records
description: "Record and manage AI mistakes and learnings using an ADR-inspired format. Use when: (1) Fixing significant bugs that required deep debugging, (2) Discovering anti-patterns or incorrect assumptions, (3) Resolving performance/security issues, (4) Learning from refactors that revealed design flaws, (5) Encountering race conditions or async problems."
---

# Lesson Decision Records

A systematic approach to recording mistakes, bugs, and learnings in a structured, searchable format. This skill helps AI agents build institutional memory by documenting what went wrong, why it happened, and how to prevent recurrence.

## When to Use This Skill

### Record a Lesson When:
- **Significant Bug**: Required >30 minutes debugging or revealed non-obvious issue
- **Anti-Pattern Discovered**: Code violated best practices in subtle ways
- **Performance Issue**: Non-trivial optimization or scalability problem
- **Security Vulnerability**: Any security-related mistake, regardless of size
- **Race Condition/Async**: Concurrency bugs, timing issues, promise chains
- **Incorrect Assumption**: Wrong understanding of library/framework/API behavior
- **Design Flaw**: Refactor revealed architectural problems
- **Data Loss/Corruption**: Any issue that affected data integrity

### Do NOT Record When:
- Simple typos or syntax errors
- Trivial fixes (< 5 minutes)
- Standard dependency updates
- Minor style/formatting changes
- Following explicit user instructions (not a mistake)

## Storage Locations

Lessons are stored in two primary locations based on scope:

### Global Lessons: `~/.agents/lessons/`
Use for universal engineering principles that apply across all projects:
- Language-agnostic patterns (e.g., async best practices)
- General security principles
- Cross-platform gotchas
- Tool/framework behavior that applies everywhere
- Testing anti-patterns

**Example**: "Always await async functions in try-catch blocks to prevent unhandled rejections"

### Project Lessons: `[project-root]/.agents/lessons/`
Use for codebase-specific learnings:
- Domain-specific logic errors
- Project architecture mistakes
- Custom abstraction misuse
- Business rule violations
- Integration-specific issues

**Example**: "UserService.findById() returns null for soft-deleted users, must use findByIdIncludingDeleted()"

## File Naming Convention

Lessons follow sequential numbering: `NNNN-slug.md`

- **NNNN**: Zero-padded 4-digit sequence (0001, 0002, etc.)
- **slug**: kebab-case descriptive name
- **Extension**: Always `.md`

**Examples**:
- `0001-async-unhandled-promise-rejection.md`
- `0015-postgres-transaction-deadlock.md`
- `0042-react-state-closure-stale-data.md`

## Lesson Template

Each lesson file contains YAML frontmatter followed by 5 structured sections:

```markdown
---
type: lesson
scope: [global|project]
tags: [category1, category2, category3]
date: YYYY-MM-DD
severity: [low|medium|high]
---

# [Descriptive Title]

## 1. Context
Brief summary of the task, environment, and initial approach. Include:
- What you were trying to accomplish
- Relevant technologies/frameworks involved
- Initial implementation strategy

## 2. Mistake
Clear description of what went wrong. Include:
- Observable symptoms (errors, incorrect behavior)
- How the mistake manifested
- Impact on functionality

## 3. Root Cause
Technical explanation of WHY the mistake occurred. Include:
- Underlying mechanism that caused the issue
- Incorrect assumptions made
- Relevant documentation/specs that clarify correct behavior

## 4. Correction
The solution that resolved the issue. Include:
- Code changes made (use code blocks with diff when helpful)
- Configuration adjustments
- Architectural changes

## 5. Prevention Rule
A concise, actionable rule for future AI sessions. Format as imperative command:
- "Always [do X] when [condition Y]"
- "Never [do X] without [safeguard Y]"
- "Check [condition X] before [action Y]"
```

## Severity Classification

### High Severity
- Data loss or corruption
- Security vulnerabilities (XSS, injection, auth bypass)
- Production incidents or outages
- Memory leaks or resource exhaustion
- Race conditions causing data inconsistency

### Medium Severity
- Performance degradation (>2x slowdown)
- Incorrect business logic implementation
- API misuse causing errors
- Test failures in critical paths
- Breaking changes to public APIs

### Low Severity
- Code style violations with functional impact
- Minor refactoring needs
- Suboptimal but working implementations
- Documentation gaps that led to confusion

## Tag Taxonomy

Use standardized tags for searchability:

**General**: `async`, `concurrency`, `error-handling`, `types`, `nullability`
**Testing**: `testing`, `mocking`, `fixtures`, `test-data`, `flaky-tests`
**Performance**: `performance`, `caching`, `memory-leak`, `n+1-query`, `optimization`
**Security**: `security`, `auth`, `xss`, `injection`, `cors`, `secrets`
**State**: `state-management`, `redux`, `react-state`, `closure`, `mutation`
**Database**: `database`, `transactions`, `migrations`, `indexes`, `deadlock`
**API**: `rest-api`, `graphql`, `versioning`, `breaking-change`, `contracts`
**Frontend**: `react`, `vue`, `dom`, `css`, `responsive`, `accessibility`
**Backend**: `node`, `python`, `api-design`, `middleware`, `routing`

## Workflow: Recording a Lesson

### 1. Detection Phase
When you identify a significant learning opportunity:
```
I've identified a significant bug that took [X minutes] to debug. 
This appears to be a [scope: global/project] lesson about [topic].
Should I record this as a lesson?
```

### 2. Scope Determination
Ask yourself:
- Does this apply to this project only? → **Project**
- Could this happen in any codebase? → **Global**

### 3. Draft the Lesson
Generate the lesson file using the template:
- Determine next sequence number by reading existing lessons
- Choose appropriate tags and severity
- Fill all 5 sections with specific details
- Write clear, actionable prevention rule

### 4. Present for Review
Show the user:
```markdown
# Proposed Lesson: [Title]

**Scope**: [global/project]
**Severity**: [level]
**Tags**: [tag1, tag2, tag3]

[Brief summary of the lesson]

Shall I record this to `[path]/NNNN-slug.md`?
```

### 5. Persist the Lesson
Once approved:
1. Create the `NNNN-slug.md` file
2. Update the `README.md` index in the lessons directory
3. Confirm: "Lesson recorded as [filename]"

## Index Management (README.md)

Each `lessons/` directory MUST contain a `README.md` serving as:

### 1. Directory Purpose
Brief explanation of what lessons are stored here

### 2. Table of Contents
Grouped by severity, then chronologically:

```markdown
## High Severity

| ID | Title | Tags | Date |
|----|-------|------|------|
| [0015](0015-postgres-deadlock.md) | PostgreSQL Transaction Deadlock | database, deadlock | 2024-03-15 |

## Medium Severity
...

## Low Severity
...
```

### 3. Tag Index
Quick reference for finding related lessons:

```markdown
## By Topic

- **async**: [0001](0001-async-promise.md), [0008](0008-race-condition.md)
- **database**: [0015](0015-postgres-deadlock.md)
- **react**: [0003](0003-react-state-closure.md), [0012](0012-react-effect-deps.md)
```

### 4. Usage Instructions
For CLI tools and future AI sessions:

```markdown
## For AI Sessions

Before implementing async operations, review lessons tagged with `async`.
Before database changes, review lessons tagged with `database`.
```

## Retrieving Lessons

### Before Starting Work
When beginning a task, proactively check for relevant lessons:

1. **Read the index**: Check `~/.agents/lessons/README.md` and `[project]/.agents/lessons/README.md`
2. **Filter by tags**: Look for lessons matching the current task domain
3. **Review high-severity**: Always scan high-severity lessons in relevant areas
4. **Apply prevention rules**: Incorporate prevention rules into implementation

### During Debugging
If encountering a familiar-seeming issue:

1. **Search by symptoms**: Grep for error messages or behavior in lesson files
2. **Check related tags**: Review lessons with similar technical context
3. **Compare root causes**: See if current issue matches known patterns

## Example Lesson

See `assets/boilerplate/example-lesson.md` for a complete, realistic example.

## Best Practices

### Writing Clear Lessons
- **Be specific**: Include actual error messages, stack traces, code snippets
- **Show the journey**: Explain what you tried that didn't work
- **Document the "aha" moment**: What finally revealed the root cause?
- **Make rules actionable**: Rules should be verifiable in code review

### Maintaining Quality
- **Avoid duplicates**: Check existing lessons before recording
- **Update superseded lessons**: If a lesson becomes obsolete, mark it clearly
- **Cross-reference**: Link related lessons in the content
- **Include sources**: Link to documentation, Stack Overflow, GitHub issues

### Scope Boundaries
When uncertain about scope:
- **Start with project**: Can always promote to global later
- **Generalize carefully**: Only make global if truly universal
- **Ask the user**: They know the codebase better

## Integration with Workflows

### Post-Bug Fix Checklist
After fixing a significant bug:
1. ✅ Tests pass
2. ✅ Code reviewed
3. ✅ Consider: Is this lesson-worthy?
4. ✅ Record lesson if yes
5. ✅ Update index

### New Developer Onboarding
Point new team members to:
1. Global lessons for general principles
2. Project lessons for codebase-specific gotchas
3. High-severity lessons as required reading

### Code Review
Reviewers can reference lessons:
- "This violates Lesson 0015 (deadlock prevention)"
- "Good catch! This should be recorded as a lesson"

## Related Skills

This skill complements:
- **architecture-decision-records**: For documenting intentional design choices
- **systematic-debugging**: For the debugging process itself
- **code-review-excellence**: For catching issues before they become lessons

Use **ADRs** for "what we decided", use **Lessons** for "what we learned the hard way".
