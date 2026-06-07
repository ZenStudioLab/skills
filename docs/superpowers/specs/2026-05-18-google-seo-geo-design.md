# Google-first SEO/GEO Skill Design

## Goal

Create a new repo-local skill that helps agents audit pages/sites/content for Google Search visibility and generative-search readiness, then produce concrete Google-first implementation guidance grounded in official Google Search documentation.

## Why this skill exists

Google's newer guidance around generative AI search features, AI Overviews, AI Mode, helpful content, and anti-spam behavior changes how an agent should answer SEO/GEO requests. The skill should prevent generic "GEO hacks" and replace them with official, implementation-ready guidance.

## Primary outcome

When a user asks for SEO, GEO, AI-overview readiness, indexing, crawlability, schema, snippet, or helpful-content help, the skill should:

1. audit the request against Google guidance,
2. produce concrete implementation fixes,
3. warn against unsupported or risky tactics.

## Users

This skill is for both:

- developers who need exact implementation steps for metadata, schema, crawlability, linking, and validation, and
- marketers/content teams who need content-quality, positioning, and helpful-content guidance.

## Source-of-truth hierarchy

The skill should use this authority order:

1. user-provided page/site/content request,
2. project-local `.agents/product-marketing-context.md` when present,
3. official Google Search documentation,
4. secondary interpretation only when clearly labeled as non-authoritative.

The skill must treat Google documentation as the source of truth for what is and is not supported for Google Search.

## Google guidance the skill must encode

The design is based primarily on these official sources:

- `using-gen-ai-content`
- `ai-optimization-guide`
- `creating-helpful-content`
- `seo-starter-guide`

From those docs, the skill should encode these core ideas:

- foundational SEO still matters for generative AI features in Google Search,
- pages must be crawlable, indexable, and eligible for snippets,
- content should be people-first, helpful, reliable, and non-commodity,
- scaled content abuse and low-value AI-assisted mass content are risky,
- there is no special Google requirement for `llms.txt`, forced chunking, or AI-only rewrite patterns,
- structured data still matters for general SEO/rich result eligibility, but it is not a special GEO unlock,
- E-E-A-T is useful as an evaluation lens but should not be misrepresented as a direct ranking factor,
- keyword stuffing, fake freshness, and generic "long-tail every variation" strategies should be rejected.

## Skill positioning

This is a **Google-first dual-lane skill**.

It is not a broad multi-engine GEO skill. It may mention adjacent GEO concepts only when they do not conflict with official Google guidance.

## Trigger scope

The skill should trigger for requests like:

- "optimize this page/site for Google SEO"
- "audit this page for AI Overviews / AI Mode readiness"
- "help with GEO for Google"
- "check helpful content issues"
- "improve indexing / crawlability / snippets / schema"
- "how do I make this page more visible in Google AI results"

It should avoid triggering for general marketing strategy with no search component.

## Workflow

### 1. Classify the request

Determine whether the user needs one of these:

- page audit,
- site audit,
- content draft review,
- implementation guidance,
- remediation of a known issue.

### 2. Load context

Use the immediate user input first. Then check for `.agents/product-marketing-context.md`.

If the context file exists, use it to understand:

- product category,
- target audience,
- core use cases,
- positioning and differentiation,
- customer language.

If the file does not exist, continue normally but note that recommendations may be less precise without product context.

### 3. Audit lane

Audit should cover, when relevant:

- people-first/helpful-content signals,
- originality and non-commodity value,
- first-hand expertise / evidence / sourcing,
- page intent clarity,
- title/snippet quality,
- crawlability and indexability,
- URL/site structure and duplicates,
- internal linking and anchor text,
- structured data opportunities,
- image/video support,
- page experience and readability,
- mismatch between content and product positioning.

### 4. Implementation lane

After the audit, the skill should give concrete Google-first fixes such as:

- revised page title/meta description guidance,
- schema recommendations with examples where appropriate,
- heading/content structure improvements,
- internal-linking recommendations,
- duplicate/canonical/redirect guidance,
- crawl/index checks,
- content revisions to improve specificity, originality, and audience fit,
- validation steps using source HTML, Search Console-style checks, or rich-results validation.

### 5. Guardrail lane

The skill must explicitly flag unsupported or risky tactics, including:

- `llms.txt` as a Google requirement,
- chunking pages specifically for Google AI systems,
- rewriting copy only for AI systems,
- keyword stuffing,
- scaled-content abuse,
- publishing lots of near-duplicate pages for fan-out queries,
- changing dates without substantial updates,
- generic "just add more schema" advice detached from actual eligibility/usefulness.

## Output contract

The default response shape should be:

1. **Context used**
   - request/page/site input
   - `.agents/product-marketing-context.md` if present
2. **Audit findings**
   - prioritized issues
   - what aligns/misaligns with Google guidance
3. **Concrete fixes**
   - content changes
   - technical changes
   - schema/metadata suggestions
4. **Anti-pattern warnings**
   - unsupported tactics
   - risk notes
5. **Validation steps**
   - how to verify the changes

## Files to create

The new skill should use this structure:

- `skills/google-seo-geo/SKILL.md`
- `skills/google-seo-geo/README.md`
- `skills/google-seo-geo/references/google-search-docs-summary.md`
- `skills/google-seo-geo/references/audit-checklist.md`
- `skills/google-seo-geo/references/templates.md`
- `skills/google-seo-geo/references/anti-patterns.md`

## Reference file roles

### `google-search-docs-summary.md`

Condense the linked Google docs into a practical rulebook for the skill. Keep it explicitly Google-first.

### `audit-checklist.md`

Provide a reusable page/site/content audit checklist aligned with the workflow.

### `templates.md`

Include reusable templates for:

- audit outputs,
- implementation outputs,
- metadata suggestions,
- structured-data recommendations,
- validation checklists.

### `anti-patterns.md`

Document unsupported, misleading, or risky tactics the skill should warn against.

## Evaluation goals

The implementation plan should include evals that check:

- correct triggering for Google SEO/GEO requests,
- correct use of `.agents/product-marketing-context.md`,
- Google-doc-grounded audit behavior,
- concrete implementation guidance quality,
- explicit rejection of bad advice such as `llms.txt`, chunking-for-Google, keyword stuffing, fake freshness, and scaled-content abuse.

## Non-goals

This skill should not:

- become a broad all-engines citation-optimization framework,
- claim Google-specific benefits that the docs do not support,
- invent special AI markup requirements for Google,
- optimize pages in a vacuum when project marketing context is available.

## Constraints

- Keep the main `SKILL.md` concise enough to trigger well and remain maintainable.
- Push detail into reference files.
- Prefer explanation plus reasoning over rigid unsupported rules.
- Keep all Google-specific claims traceable to the linked documentation.

## Open implementation note

Repo planning artifacts currently live under `docs/plans/active/` and `reviews/`, while this design spec is being stored under `docs/superpowers/specs/` per the brainstorming workflow. The implementation plan should decide whether to preserve that split or normalize future planning locations.
