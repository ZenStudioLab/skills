# Response Templates

## Audit + implementation template

```text
Context used
- [request/page/site]
- [.agents/product-marketing-context.md summary if present]

Audit findings
1. [highest priority issue]
2. [next issue]

Concrete fixes
- Content:
  - [change]
- Technical:
  - [change]
- Schema/metadata:
  - [change]

Anti-pattern warnings
- [warning]

Validation steps
- [check]
```

## Metadata suggestion template

```text
Suggested title:
Suggested meta description:
Why this is better:
```

## Validation template

```text
- Verify source HTML contains the expected title/meta/schema change.
- Verify the page remains crawlable/indexable.
- Validate structured data only if schema is recommended.
- Use Search Console-style inspection or snippet checks where relevant.
```
