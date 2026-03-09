---
type: lesson
scope: [global|project]
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
severity: [low|medium|high]
---

# [Descriptive Title - What Went Wrong]

## 1. Context

Brief summary of what you were trying to accomplish:
- Task or feature being implemented
- Relevant technologies/frameworks
- Initial approach or assumptions
- Environment details (if relevant)

## 2. Mistake

Clear description of what went wrong:
- Observable symptoms (error messages, incorrect behavior)
- How the issue manifested
- Impact on functionality or performance
- When/how the problem was discovered

## 3. Root Cause

Technical explanation of WHY the mistake occurred:
- Underlying mechanism that caused the issue
- Incorrect assumptions or misunderstandings
- What the code/system was actually doing
- Relevant documentation or specs that clarify correct behavior
- Why the mistake wasn't immediately obvious

## 4. Correction

The solution that resolved the issue:

```language
// Before (incorrect)
[code snippet showing the problem]

// After (corrected)
[code snippet showing the fix]
```

Additional changes made:
- Configuration adjustments
- Test additions
- Documentation updates
- Architectural changes (if any)

## 5. Prevention Rule

**Actionable Rule**: [One clear, imperative statement]

Format as:
- "Always [do X] when [condition Y]"
- "Never [do X] without [safeguard Y]"
- "Check [condition X] before [action Y]"
- "Use [approach X] instead of [approach Y] for [scenario Z]"

**Verification**: How to check this rule in code review or testing?

**Examples**:
- ✅ Good: [Example of following the rule]
- ❌ Bad: [Example of violating the rule]
