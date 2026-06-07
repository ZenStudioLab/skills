---
name: google-seo-geo
description: "Use when the user asks for Google SEO, Google GEO, AI Overviews, AI Mode, helpful content, indexing, crawlability, schema, snippets, page experience, or wants to optimize a page/site for Google Search and generative-search visibility. Google-first only: audit first, then give concrete implementation fixes and warn against unsupported tactics like llms.txt, chunking for Google, keyword stuffing, fake freshness, or scaled-content abuse."
---

# Google-first SEO/GEO

This skill is for Google-first SEO and generative-search work. Treat official Google Search documentation as the source of truth and avoid inventing unsupported Google tactics.

## Scope

Use this skill when the user needs help with:

- Google SEO for a page or site
- Google GEO framed around AI Overviews or AI Mode readiness
- helpful-content review
- indexing, crawlability, snippets, schema, duplicate content, or internal linking
- implementation guidance for improving Google Search visibility

Do not turn this into a broad multi-engine citation strategy unless the user explicitly asks for that.

## Context loading

Before auditing or prescribing changes:

1. Read the immediate page, site, draft, or request context.
2. Check whether `.agents/product-marketing-context.md` exists.
3. If it exists, use it to understand product category, audience, use cases, positioning, differentiation, and customer language.
4. If it does not exist, continue normally but note that recommendations may be less precise without product context.

## Workflow

### 1. Classify the request

Determine whether the user needs:

- a page audit,
- a site audit,
- a content draft review,
- concrete implementation guidance, or
- remediation of a known issue.

### 2. Audit first

Use `references/audit-checklist.md` and `references/google-search-docs-summary.md`.

Check what matters for the request:

- helpful, reliable, people-first content
- originality and non-commodity value
- evidence of experience, expertise, sourcing, or trust signals
- title and snippet quality
- crawlability, indexability, and snippet eligibility
- URL structure, duplication, canonicals, and redirects
- internal linking and anchor text
- structured-data opportunities that are actually relevant
- image/video support and accessibility
- page experience and readability
- alignment with product positioning from `.agents/product-marketing-context.md`

### 3. Give concrete implementation fixes

After the audit, give exact fixes such as:

- revised title/meta-description guidance
- content structure improvements
- schema recommendations with examples when appropriate
- internal-linking suggestions
- duplicate/canonical/redirect cleanup guidance
- crawl/index verification steps
- content changes that improve specificity, originality, and audience fit

Use `references/templates.md` for response structure.

### 4. Apply Google-first guardrails

Use `references/anti-patterns.md`.

Explicitly warn against unsupported or risky tactics, including:

- treating `llms.txt` as a Google requirement
- chunking content specifically for Google AI systems
- rewriting copy only for AI systems
- keyword stuffing
- scaled-content abuse
- publishing near-duplicate fan-out pages
- fake freshness through date changes without substantial updates
- adding schema without a legitimate feature or content fit

### 5. Finish with validation steps

Tell the user how to verify the change through source HTML, crawl/index checks, rich-results validation, or Search Console-style inspection.

## Output structure

Default to this order:

1. **Context used**
   - request/page/site input
   - `.agents/product-marketing-context.md` if present
2. **Audit findings**
   - prioritized issues
   - what aligns or misaligns with Google guidance
3. **Concrete fixes**
   - content changes
   - technical changes
   - schema or metadata suggestions
4. **Anti-pattern warnings**
5. **Validation steps**

## References

- `references/google-search-docs-summary.md` — Google-first rules distilled from official docs
- `references/audit-checklist.md` — reusable audit rubric
- `references/templates.md` — output templates for audit and implementation guidance
- `references/anti-patterns.md` — unsupported or risky tactics to reject
