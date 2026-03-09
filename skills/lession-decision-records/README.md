# Lesson Decision Records Skill

A systematic skill for AI agents to record and learn from mistakes, bugs, and refactors using an ADR-inspired format. Build institutional memory by documenting what went wrong, why it happened, and how to prevent recurrence.

## 🎯 Purpose

While Architecture Decision Records (ADRs) document **what we decided**, Lesson Decision Records (LDRs) capture **what we learned the hard way**. This skill helps AI agents:

- **Avoid repeating mistakes** by maintaining searchable lessons
- **Build expertise** in codebases through documented failures
- **Speed up debugging** by referencing similar past issues
- **Onboard faster** with lessons learned from production experience

## 🚀 Quick Start

### For AI Agents

This skill automatically activates when you:
1. Fix a significant bug (>30 min debugging)
2. Discover an anti-pattern or incorrect assumption
3. Resolve performance/security issues
4. Learn from refactors that revealed design flaws

**Example Trigger**: "I've fixed a race condition in the payment processor. Should I record this as a lesson?"

### For Developers

Lessons are stored in two locations:

- **Global**: `~/.agents/lessons/` - Universal engineering principles
- **Project**: `[project-root]/.agents/lessons/` - Codebase-specific learnings

Each directory contains a `README.md` index for easy browsing.

## 📁 Structure

```
lesson-decision-records/
├── SKILL.md                    # Core AI instructions
├── README.md                   # This file
├── assets/
│   └── boilerplate/
│       ├── lesson-template.md      # Blank template
│       ├── index-template.md       # README.md template
│       └── example-lesson.md       # Complete example
└── references/
    ├── lesson-vs-adr.md           # When to use lessons vs ADRs
    └── severity-guidelines.md     # Classification guide
```

## 📝 Lesson Format

Each lesson follows a 5-section structure:

```markdown
---
type: lesson
scope: [global|project]
tags: [async, error-handling]
date: 2024-03-15
severity: high
---

# Always Await Promise.all() in Try-Catch

## 1. Context
Implementing parallel API calls for dashboard data...

## 2. Mistake
Unhandled promise rejections crashed the server...

## 3. Root Cause
Promise.all() rejects immediately on first failure...

## 4. Correction
Wrapped Promise.all() in try-catch and added error handling...

## 5. Prevention Rule
Always await Promise.all() within try-catch blocks and handle partial failures.
```

## 🎓 Real-World Examples

### Global Lesson: Async Promise Handling
```markdown
# 0001-async-unhandled-promise-rejection.md

Tags: async, error-handling, node
Severity: High

Context: Background job processing system
Mistake: Server crashed with "UnhandledPromiseRejectionWarning"
Root Cause: Forgot to await async function in try-catch
Correction: Added await and proper error handling
Rule: Always await async functions in try-catch blocks
```

### Project Lesson: Custom ORM Behavior
```markdown
# 0003-user-service-soft-delete-gotcha.md

Tags: database, orm, business-logic
Severity: Medium

Context: User lookup for admin dashboard
Mistake: Couldn't find recently deleted user accounts
Root Cause: UserService.findById() filters out soft-deleted records
Correction: Used UserService.findByIdIncludingDeleted()
Rule: Use findByIdIncludingDeleted() for admin/audit features
```

## 🔍 How AI Uses Lessons

### Before Implementation
1. **Scan relevant lessons**: Check tags matching current task (e.g., `async`, `database`)
2. **Review high-severity**: Always scan high-severity lessons in the domain
3. **Apply prevention rules**: Incorporate rules into implementation strategy

### During Debugging
1. **Search by symptoms**: Grep error messages in lesson files
2. **Compare patterns**: Check if issue matches known root causes
3. **Reference solutions**: Adapt corrections from similar lessons

### After Bug Fixes
1. **Evaluate significance**: Did this take >30 min or reveal important insight?
2. **Propose lesson**: Ask user if worth recording
3. **Record and index**: Create lesson file and update README.md

## 🏷️ Tag Taxonomy

Standardized tags for consistency:

**General**: `async`, `concurrency`, `error-handling`, `types`, `nullability`  
**Testing**: `testing`, `mocking`, `fixtures`, `flaky-tests`  
**Performance**: `performance`, `caching`, `memory-leak`, `n+1-query`  
**Security**: `security`, `auth`, `xss`, `injection`, `cors`  
**State**: `state-management`, `redux`, `react-state`, `closure`  
**Database**: `database`, `transactions`, `migrations`, `deadlock`  

## 🔄 Workflow

```
Bug Fixed → Evaluate Significance → Determine Scope
                                          ↓
                                    Draft Lesson
                                          ↓
                                    User Review
                                          ↓
                              Record File + Update Index
```

## 🆚 Lessons vs ADRs

| Aspect | ADR | Lesson |
|--------|-----|--------|
| **Purpose** | Document decisions | Document mistakes |
| **Timing** | Before/during implementation | After bug fix |
| **Tone** | Analytical, options-focused | Reflective, corrective |
| **Scope** | Architecture, design | Bugs, anti-patterns |
| **Example** | "Use PostgreSQL for primary DB" | "Always use transactions for multi-table updates" |

See `references/lesson-vs-adr.md` for detailed comparison.

## 💡 Best Practices

### Writing Quality Lessons
✅ **Be specific**: Include error messages, stack traces, code snippets  
✅ **Show the journey**: What you tried that didn't work  
✅ **Document "aha" moment**: What revealed the root cause  
✅ **Make rules actionable**: Verifiable in code review  

❌ **Avoid vagueness**: "Be more careful with async"  
❌ **Skip trivial**: Typos, simple syntax errors  
❌ **Over-generalize**: Making every bug a global lesson  

### Maintaining the Index
- Group by severity (high → medium → low)
- Include tag-based index for quick searches
- Update both global and project indexes
- Cross-reference related lessons

## 🛠️ Integration

### With Code Review
```markdown
Reviewer: "This violates Lesson 0015 (deadlock prevention rule)"
Developer: "Good catch! Updated to use row-level locking"
```

### With Onboarding
```markdown
New Developer Checklist:
□ Read global high-severity lessons
□ Read project-specific lessons
□ Review lessons tagged with your tech stack
```

### With CI/CD
```bash
# Pre-commit hook suggestion
echo "💡 Related lessons for modified files:"
git diff --name-only | xargs grep-lessons-by-file
```

## 📜 License

MIT

---

**Related Skills**: `architecture-decision-records`, `systematic-debugging`, `code-review-excellence`
