# Severity Classification Guidelines

How to determine the severity level (high, medium, low) for lesson records.

## Quick Reference

| Severity | Impact | Examples | Record? |
|----------|--------|----------|---------|
| **High** | Critical functionality broken, data at risk | Data loss, security breach, production crash | ✅ Always |
| **Medium** | Significant degradation or incorrect behavior | Wrong business logic, 2x slowdown, API errors | ✅ Yes |
| **Low** | Minor issues with working alternative | Suboptimal patterns, style issues with impact | ⚠️ If valuable |
| **None** | Trivial fixes | Typos, formatting, simple oversights | ❌ Skip |

## High Severity

### Definition
Issues that cause critical failures, data problems, or security vulnerabilities. These are "must read" lessons for anyone working in the relevant domain.

### Characteristics
- **Production impact**: Caused outage, incident, or emergency response
- **Data integrity**: Risk of data loss, corruption, or inconsistency
- **Security**: Any vulnerability (XSS, injection, auth bypass, secrets exposure)
- **Safety**: Memory leaks, resource exhaustion, infinite loops
- **Concurrency**: Race conditions causing incorrect state

### Examples

✅ **High Severity Lessons**:

```markdown
# Unhandled Promise Rejection Crashed Server
Tags: async, error-handling, production
Impact: 15-minute production outage, lost email batch
```

```markdown
# SQL Injection in User Search Endpoint
Tags: security, injection, sql
Impact: Exposed all user data to potential attacker
```

```markdown
# Race Condition in Payment Processing
Tags: concurrency, payments, transactions
Impact: 23 customers double-charged before detection
```

```markdown
# Missing Transaction Caused Data Inconsistency
Tags: database, transactions, integrity
Impact: Orders saved without inventory decrement
```

```markdown
# Memory Leak in WebSocket Connection Handler
Tags: memory-leak, websockets, performance
Impact: Server OOM crash after 48 hours uptime
```

### Red Flags for High Severity
- Error message contains: "FATAL", "CRITICAL", "OutOfMemory", "SecurityException"
- Required emergency hotfix or rollback
- Customers were affected
- Data had to be manually recovered or reconciled
- Involved on-call or incident response

## Medium Severity

### Definition
Issues that cause incorrect behavior, significant performance degradation, or violated important patterns. Important to understand but not emergency-level.

### Characteristics
- **Business logic**: Incorrect calculations, wrong workflow
- **Performance**: >2x slowdown, N+1 queries, inefficient algorithms
- **API misuse**: Using libraries/frameworks incorrectly
- **Breaking changes**: Unintended API breaking changes
- **Test failures**: Critical test paths broken

### Examples

✅ **Medium Severity Lessons**:

```markdown
# N+1 Query in User Dashboard
Tags: performance, database, n+1-query
Impact: Dashboard load time increased from 200ms to 8s
```

```markdown
# Incorrect Tax Calculation for International Orders
Tags: business-logic, calculations, internationalization
Impact: Wrong tax amounts for 3 days before discovery
```

```markdown
# React useEffect Infinite Loop
Tags: react, hooks, infinite-loop
Impact: Browser tab freeze, high CPU, bad UX
```

```markdown
# Breaking Change in Public API Response
Tags: api-design, breaking-change, versioning
Impact: 5 integration partners reported failures
```

```markdown
# Flaky Test Due to Async Timing
Tags: testing, async, flaky-test
Impact: CI pipeline unreliable, slowed deployments
```

### Red Flags for Medium Severity
- Performance metrics showed significant degradation
- Incorrect behavior reported but no data loss
- Required non-trivial refactor to fix
- Multiple team members independently hit the issue
- Debugging took >1 hour

## Low Severity

### Definition
Issues that were suboptimal or violated best practices but had working alternatives. Worth recording if the learning is valuable, but not critical reading.

### Characteristics
- **Code quality**: Poor patterns that could cause future issues
- **Maintainability**: Hard to understand or maintain code
- **Minor performance**: Noticeable but not severe slowdown
- **Style with impact**: Not just formatting, but patterns that matter

### Examples

✅ **Low Severity Lessons** (worth recording):

```markdown
# Overly Complex Nested Ternaries
Tags: code-quality, readability, maintainability
Impact: Multiple bugs in dense conditional logic
```

```markdown
# Hardcoded Configuration in Source Code
Tags: configuration, maintainability
Impact: Required code deploy to change settings
```

```markdown
# Missing PropTypes Caused Debugging Delay
Tags: react, types, debugging
Impact: 30 minutes debugging undefined prop issue
```

```markdown
# Inconsistent Error Response Format
Tags: api-design, error-handling, consistency
Impact: Frontend had to handle 3 different error formats
```

### When to Skip Low Severity
Skip if the lesson is too specific to be useful later:
- One-off mistake that's unlikely to repeat
- Obvious in hindsight with no general principle
- Already well-covered by existing lessons
- The "aha moment" isn't transferable

## Not Worth Recording

### Trivial Issues
Don't create lessons for:
- **Typos**: Variable name spelled wrong, missing semicolon
- **Syntax errors**: Caught immediately by linter/compiler
- **Simple oversights**: Forgot to save file, wrong import path
- **Following instructions**: User told you to do X, you did X
- **Expected bugs**: Known limitations you were working around

### Examples of What NOT to Record

❌ **Skip These**:

```markdown
# Forgot to Import React Component
Too obvious, happens all the time, caught immediately
```

```markdown
# Misspelled Variable Name
Simple typo with no learning value
```

```markdown
# Used Wrong CSS Class Name
Trivial mistake, instant feedback from UI
```

```markdown
# Forgot to Run npm install After Pulling
Standard development practice, not a lesson
```

## Edge Cases and Judgment Calls

### When in Doubt

Ask yourself:
1. **Will this help prevent future mistakes?** (Yes → record)
2. **Did I learn something non-obvious?** (Yes → record)
3. **Could this happen to someone else?** (Yes → record)
4. **Is there a generalizable principle?** (Yes → record)

If all answers are "no", skip it.

### Severity Escalation

Some issues cross severity levels:

**Starts Medium, Becomes High**:
```markdown
# Inefficient Database Query (Medium)
Initially: Just slow (8s load time)
Later: Caused table lock under load (High severity)

Record as: High severity
Note in context: "Initially appeared as performance issue"
```

**Combine Related Lessons**:
If you find multiple medium-severity lessons on the same topic, consider:
- Creating one comprehensive high-severity lesson
- Cross-referencing related lessons
- Updating severity if pattern is widespread

## Severity by Impact Area

### Data Impact
- **High**: Data loss, corruption, inconsistency
- **Medium**: Wrong calculations, incorrect state
- **Low**: Redundant data, minor inefficiency

### User Impact
- **High**: Can't use core features, errors blocking workflow
- **Medium**: Degraded experience, slow response
- **Low**: Minor UX issues, cosmetic problems

### Developer Impact
- **High**: Blocks development, requires emergency fix
- **Medium**: Slows development, requires planned refactor
- **Low**: Minor inconvenience, easy workaround

### System Impact
- **High**: Crashes, outages, resource exhaustion
- **Medium**: Performance degradation, increased costs
- **Low**: Suboptimal resource usage

## Summary Decision Tree

```
Is there data loss, security issue, or production incident?
├─ YES → High Severity
│
└─ NO → Is there incorrect behavior or significant performance issue?
    ├─ YES → Medium Severity
    │
    └─ NO → Is there a valuable learning with general applicability?
        ├─ YES → Low Severity
        │
        └─ NO → Don't record
```

## Tag Combinations by Severity

Certain tags commonly indicate severity:

**High Severity Tags**:
- `security`, `injection`, `auth-bypass`
- `data-loss`, `corruption`, `integrity`
- `production-incident`, `outage`, `crash`
- `memory-leak`, `resource-exhaustion`

**Medium Severity Tags**:
- `performance`, `n+1-query`, `optimization`
- `business-logic`, `incorrect-calculation`
- `breaking-change`, `api-misuse`
- `race-condition` (if no data loss)

**Low Severity Tags**:
- `code-quality`, `maintainability`, `readability`
- `technical-debt`, `refactoring`
- `configuration`, `setup`

## Final Guidance

**Err on the side of recording** if unsure between recording and skipping.
**Err on the side of higher severity** if unsure between two levels.

Better to have a well-documented lesson library than to lose valuable learnings.
