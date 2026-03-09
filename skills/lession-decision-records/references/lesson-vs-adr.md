# Lessons vs Architecture Decision Records (ADRs)

Understanding when to use Lesson Decision Records (LDRs) versus Architecture Decision Records (ADRs).

## Core Difference

| Aspect | LDR (Lesson) | ADR (Decision) |
|--------|--------------|----------------|
| **Primary Purpose** | Document mistakes and learnings | Document intentional choices |
| **Trigger** | After fixing a bug or issue | Before/during implementation |
| **Perspective** | Retrospective (what went wrong) | Prospective (what we're choosing) |
| **Tone** | Reflective, corrective | Analytical, evaluative |
| **Focus** | Root cause and prevention | Options and trade-offs |

## When to Use Each

### Use a Lesson (LDR) When:

✅ **You fixed a bug** that wasn't trivial (>30 min debugging)
```
Example: "Found race condition in payment processor that caused double charges"
→ Lesson: Document the bug, root cause, and prevention rule
```

✅ **You discovered an anti-pattern** already implemented
```
Example: "Realized we were mutating Redux state directly in 5 components"
→ Lesson: Document the mistake and correct pattern
```

✅ **You misunderstood how something works**
```
Example: "Thought Promise.all() would continue on individual failures"
→ Lesson: Document the misconception and correct behavior
```

✅ **You had to refactor due to design flaw**
```
Example: "Circular dependency between UserService and AuthService broke the app"
→ Lesson: Document the design flaw and how to avoid it
```

✅ **You encountered a gotcha** in a library/framework
```
Example: "React useEffect runs twice in StrictMode during development"
→ Lesson: Document the unexpected behavior and proper handling
```

### Use a Decision (ADR) When:

✅ **Choosing between technology options**
```
Example: Deciding between PostgreSQL vs MongoDB for primary database
→ ADR: Document options, decision drivers, trade-offs, and final choice
```

✅ **Establishing architectural patterns**
```
Example: Adopting event sourcing for order management
→ ADR: Document context, design, and consequences
```

✅ **Making significant design choices**
```
Example: Using microservices vs monolith architecture
→ ADR: Document options evaluated and rationale for choice
```

✅ **Setting technical standards**
```
Example: Adopting TypeScript for all new frontend code
→ ADR: Document reasons, migration plan, and trade-offs
```

## Examples Side-by-Side

### Scenario 1: Database Choice

**ADR Approach** (Choose this for initial decision):
```markdown
# ADR-0015: Use PostgreSQL as Primary Database

## Context
Need to select database for e-commerce platform...

## Options Considered
1. PostgreSQL - ACID, JSON support, team experience
2. MongoDB - Flexible schema, horizontal scaling
3. MySQL - Familiar, simple replication

## Decision
Use PostgreSQL for ACID compliance and built-in features.

## Consequences
+ Single database for transactions and search
+ Strong consistency for financial data
- Need PostgreSQL-specific training
```

**LDR Approach** (If you made the wrong choice and learned from it):
```markdown
# 0023-mongodb-transaction-limitations

## Context
Chose MongoDB for user profiles expecting flexible schema benefits...

## Mistake
Multi-document transactions caused performance issues and consistency bugs...

## Root Cause
MongoDB's multi-document ACID transactions have significant overhead...

## Correction
Migrated to PostgreSQL with JSONB for flexibility + ACID...

## Prevention Rule
Use PostgreSQL JSONB instead of MongoDB when ACID transactions are needed.
```

### Scenario 2: Async Handling

**ADR Approach** (If establishing a standard):
```markdown
# ADR-0042: Standardize on async/await over callbacks

## Context
Codebase has mixture of callbacks, promises, and async/await...

## Decision
Use async/await for all new asynchronous code.

## Rationale
- More readable than callback pyramids
- Better error handling with try-catch
- Aligns with modern JavaScript standards

## Migration Plan
Gradually convert existing callback code...
```

**LDR Approach** (After learning from a mistake):
```markdown
# 0008-forgot-await-in-async-function

## Context
Implementing API endpoint that saves user data...

## Mistake
Function returned before database write completed...

## Root Cause
Forgot to await the database call inside async function...

## Correction
Added await before db.save() call...

## Prevention Rule
Always await all async operations in async functions; enable no-floating-promises lint rule.
```

## Decision Tree

```
Did something go wrong or reveal a mistake?
├─ YES → Write a Lesson (LDR)
│   └─ Document what happened, why, and how to prevent it
│
└─ NO → Are you making an intentional choice between options?
    ├─ YES → Write a Decision (ADR)
    │   └─ Document options, trade-offs, and chosen direction
    │
    └─ NO → Probably doesn't need documentation
        └─ (Routine implementation, minor changes, etc.)
```

## Can They Overlap?

Yes! The same topic may warrant both:

### Example: Caching Strategy

**ADR First** (Initial decision):
```markdown
# ADR-0030: Implement Redis Caching Layer

Decision to add Redis for session storage and API response caching.
Chosen over in-memory caching due to multi-server deployment.
```

**LDR Later** (After production issue):
```markdown
# 0045-redis-cache-stampede

Lesson learned when cache invalidation caused thundering herd problem.
All servers hit database simultaneously when popular cache key expired.
Prevention: Use probabilistic early expiration and background refresh.
```

The ADR documents the intentional choice to use Redis.
The LDR documents a mistake in how we used it.

## Key Insight

**ADRs are proactive** - "We decided X"
**LDRs are reactive** - "We learned Y the hard way"

Both are valuable for different reasons:
- ADRs help future developers understand **why** systems are designed as they are
- LDRs help future developers **avoid repeating** the same mistakes

## Storage Location Similarity

Both use similar organizational patterns:

```
~/.agents/decisions/          ~/.agents/lessons/
├── README.md                 ├── README.md
├── 0001-use-postgres.md      ├── 0001-async-await-bug.md
├── 0002-adopt-typescript.md  ├── 0002-n+1-query.md
└── 0003-microservices.md     └── 0003-cache-stampede.md
```

But serve different purposes in the development knowledge base.

## When Uncertain

Ask yourself:

1. **Was this a mistake or a choice?**
   - Mistake → Lesson
   - Choice → Decision

2. **Are we choosing between options or fixing something?**
   - Choosing → Decision
   - Fixing → Lesson

3. **Is this establishing direction or correcting course?**
   - Establishing → Decision
   - Correcting → Lesson

4. **Would we make this "decision" if we could go back in time?**
   - Yes → Decision (it was the right choice)
   - No → Lesson (we learned it was wrong)

## Summary

Use **Lessons** to build a safety net of hard-won knowledge.
Use **Decisions** to document the path forward.

Both make teams smarter over time.
