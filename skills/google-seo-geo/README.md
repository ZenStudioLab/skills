# Google-first SEO/GEO

Google-first SEO/GEO skill for auditing pages, sites, and drafts against official Google Search guidance, then returning concrete implementation fixes.

## What it does

- Audits requests using official Google Search documentation
- Loads `.agents/product-marketing-context.md` when present to avoid context-free optimization
- Produces concrete Google-first content and technical fixes
- Warns against unsupported tactics like `llms.txt`, chunking-for-Google, keyword stuffing, fake freshness, and scaled-content abuse

## Best for

- Google SEO audits
- AI Overviews / AI Mode readiness checks
- helpful-content reviews
- indexing, snippets, schema, and crawlability work
- implementation guidance for developers and content teams

## File layout

- `SKILL.md` — trigger behavior and main workflow
- `references/google-search-docs-summary.md` — distilled Google guidance
- `references/audit-checklist.md` — audit rubric
- `references/templates.md` — response templates
- `references/anti-patterns.md` — unsupported or risky tactics
- `evals/evals.json` — realistic evaluation prompts
