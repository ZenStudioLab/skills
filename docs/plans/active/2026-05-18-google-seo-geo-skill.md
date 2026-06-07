# Google-first SEO/GEO Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new repo-local `google-seo-geo` skill that audits requests against official Google Search guidance, uses `.agents/product-marketing-context.md` when available, and returns concrete Google-first SEO/GEO fixes plus anti-pattern warnings.

**Architecture:** Build a markdown-first skill package under `skills/google-seo-geo/` with one concise `SKILL.md`, four reference files for detailed guidance, and an `evals/evals.json` set that exercises audit, implementation, context-loading, and anti-pattern rejection behavior. Align the skill with existing repo conventions by updating the root `README.md` and validating the package with the existing `skills/skill-creator/scripts/quick_validate.py` helper plus a small JSON/reference integrity check.

**Tech Stack:** Markdown skill files, JSON eval definitions, Python 3 validation script, existing repo README conventions.

**Prerequisites:** `python3`; `PyYAML` importable from `python3` (install with `python3 -m pip install pyyaml` if missing); `git`; optional `opencode` CLI plus working provider credentials for the trigger-smoke step in Task 5.

---

### Task 1: Scaffold the new skill package

**Files:**
- Create: `skills/google-seo-geo/SKILL.md`
- Create: `skills/google-seo-geo/README.md`
- Create: `skills/google-seo-geo/references/`
- Create: `skills/google-seo-geo/evals/evals.json`
- Test: `skills/skill-creator/scripts/quick_validate.py`

- [ ] **Step 1: Create the directory structure**

Run:

```bash
mkdir -p skills/google-seo-geo/references skills/google-seo-geo/evals
```

- [ ] **Step 2: Write the initial `SKILL.md` scaffold with valid frontmatter**

Write `skills/google-seo-geo/SKILL.md`:

```markdown
---
name: google-seo-geo
description: Use when the user asks for Google SEO, Google GEO, AI Overviews, AI Mode, helpful content, indexing, crawlability, schema, snippets, page experience, or wants to optimize a page/site for Google Search and generative-search visibility. Google-first only: audit first, then give concrete implementation fixes and warn against unsupported tactics like llms.txt, chunking for Google, keyword stuffing, fake freshness, or scaled-content abuse.
---

# Google-first SEO/GEO

Use this skill for Google-first search optimization work. Treat official Google Search documentation as the source of truth.

## Core workflow

1. Classify the request.
2. Audit the page, site, or draft against Google guidance.
3. Give concrete implementation fixes.
4. Warn against unsupported or risky tactics.

## References

- `references/google-search-docs-summary.md`
- `references/audit-checklist.md`
- `references/templates.md`
- `references/anti-patterns.md`
```

- [ ] **Step 3: Write the initial `README.md` scaffold**

Write `skills/google-seo-geo/README.md`:

```markdown
# Google-first SEO/GEO

Google-first SEO/GEO skill for auditing pages and producing concrete implementation guidance grounded in official Google Search documentation.

## Status

Scaffold created. Detailed references, evals, and README examples will be added in later tasks.
```

- [ ] **Step 4: Create the initial eval stub**

Write `skills/google-seo-geo/evals/evals.json`:

```json
{
  "skill_name": "google-seo-geo",
  "evals": []
}
```

- [ ] **Step 5: Run validation to verify the scaffold is structurally valid**

Run:

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/google-seo-geo
```

Expected: PASS with `Skill is valid!`

- [ ] **Step 6: Commit the scaffold**

Run:

```bash
git add skills/google-seo-geo/SKILL.md skills/google-seo-geo/README.md skills/google-seo-geo/evals/evals.json
git commit -m "feat(google-seo-geo): scaffold skill package"
```

### Task 2: Implement the core `SKILL.md` workflow

**Files:**
- Modify: `skills/google-seo-geo/SKILL.md`
- Test: `skills/google-seo-geo/SKILL.md`

- [ ] **Step 1: Verify the scaffold does not yet contain the required product-marketing-context behavior**

Run:

```bash
grep -n "product-marketing-context" skills/google-seo-geo/SKILL.md
```

Expected: FAIL with no matches

- [ ] **Step 2: Replace the scaffold with the complete skill body**

Write `skills/google-seo-geo/SKILL.md`:

```markdown
---
name: google-seo-geo
description: Use when the user asks for Google SEO, Google GEO, AI Overviews, AI Mode, helpful content, indexing, crawlability, schema, snippets, page experience, or wants to optimize a page/site for Google Search and generative-search visibility. Google-first only: audit first, then give concrete implementation fixes and warn against unsupported tactics like llms.txt, chunking for Google, keyword stuffing, fake freshness, or scaled-content abuse.
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
```

- [ ] **Step 3: Verify the product marketing context integration is present**

Run:

```bash
grep -n "\.agents/product-marketing-context\.md" skills/google-seo-geo/SKILL.md
```

Expected: PASS with at least one match

- [ ] **Step 4: Verify anti-pattern coverage is present**

Run:

```bash
grep -E "llms\.txt|chunking|keyword stuffing|scaled-content abuse|fake freshness" skills/google-seo-geo/SKILL.md
```

Expected: PASS with all key terms present

- [ ] **Step 5: Re-run structural validation**

Run:

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/google-seo-geo
```

Expected: PASS with `Skill is valid!`

- [ ] **Step 6: Commit the core workflow**

Run:

```bash
git add skills/google-seo-geo/SKILL.md
git commit -m "feat(google-seo-geo): add google-first workflow"
```

### Task 3: Add the reference bundle and skill README

**Files:**
- Modify: `skills/google-seo-geo/README.md`
- Create: `skills/google-seo-geo/references/google-search-docs-summary.md`
- Create: `skills/google-seo-geo/references/audit-checklist.md`
- Create: `skills/google-seo-geo/references/templates.md`
- Create: `skills/google-seo-geo/references/anti-patterns.md`
- Test: `skills/google-seo-geo/references/*.md`

- [ ] **Step 1: Confirm the reference directory is still empty**

Run:

```bash
test -d skills/google-seo-geo/references && test -z "$(ls -A skills/google-seo-geo/references)"
```

Expected: PASS with exit code `0`

- [ ] **Step 2: Write the Google docs summary reference**

Write `skills/google-seo-geo/references/google-search-docs-summary.md`:

```markdown
# Google Search Docs Summary

This file distills the official Google documentation that powers the `google-seo-geo` skill.

## Core rules

- Foundational SEO still matters for AI Overviews and AI Mode because Google's generative features are grounded in core Search systems.
- Pages should be crawlable, indexable, and eligible to show snippets.
- Helpful, reliable, people-first, non-commodity content is the core long-term lever.
- AI assistance is allowed, but scaled low-value content and scaled-content abuse are risky.
- There is no Google requirement for `llms.txt`, content chunking for AI, or rewriting just for AI systems.
- Structured data remains useful for normal Search understanding and rich-result eligibility, but it is not a magic GEO unlock.
- E-E-A-T is a useful evaluation lens. Do not present it as a direct ranking factor.

## Content-quality cues

- Prefer first-hand experience, original analysis, or substantial added value.
- Align the page with a real audience and real product intent.
- Use clear headings, readable structure, and supportive images or video where relevant.
- Make authorship, sourcing, and process transparent when that context would help the reader trust the content.

## Technical cues

- Check title and snippet quality.
- Check crawlability and indexability.
- Check duplication, canonicals, redirects, and URL clarity.
- Check internal linking and anchor text.
- Check whether schema is relevant and valid.

## Anti-pattern cues

- `llms.txt` as a Google requirement
- chunking pages just for Google AI
- keyword stuffing
- fake freshness
- high-volume near-duplicate fan-out pages
- schema cargo culting without feature eligibility
```

- [ ] **Step 3: Write the audit checklist reference**

Write `skills/google-seo-geo/references/audit-checklist.md`:

```markdown
# Audit Checklist

Use this checklist for page audits, site audits, and content draft reviews.

## Context

- What is the page trying to rank or be cited for?
- Who is the intended audience?
- If `.agents/product-marketing-context.md` exists, what product category, positioning, and customer language matter here?

## Content quality

- Is the page people-first and useful on its own?
- Does it add original value beyond a commodity summary?
- Does it show real expertise, sourcing, or trust cues?
- Is the heading/title accurate and non-clickbait?
- Would the audience leave satisfied without needing another search?

## Technical SEO

- Is the page crawlable and indexable?
- Is the page eligible to show a snippet?
- Are title and meta description clear and useful?
- Are URLs descriptive?
- Are duplicate/canonical issues likely?
- Are important internal links present?
- Is structured data relevant and valid?

## Presentation

- Is the content easy to scan and read?
- Are images or video supporting the page where appropriate?
- Is page experience likely acceptable?

## Anti-pattern screen

- Is the page obviously written for search engines instead of people?
- Is there keyword stuffing?
- Is there fake freshness?
- Is there scaled or near-duplicate content?
- Is there a request for unsupported Google AI tactics?
```

- [ ] **Step 4: Write the templates reference**

Write `skills/google-seo-geo/references/templates.md`:

````markdown
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
````

- [ ] **Step 5: Write the anti-patterns reference**

Write `skills/google-seo-geo/references/anti-patterns.md`:

```markdown
# Anti-patterns

These are common requests or tactics the skill should push back on for Google-first SEO/GEO work.

| Tactic | Why to reject or qualify it |
|--------|-----------------------------|
| `llms.txt` for Google | Google does not require special AI text files to appear in generative search features. |
| Chunking content for Google AI | Google can understand multiple topics on a page; forced chunking is not a requirement. |
| Rewriting solely for AI systems | Pages should be written for people first, not for a synthetic AI-only style. |
| Keyword stuffing | Against spam guidance and bad for readers. |
| Fake freshness | Updating dates without substantial updates is not a durable tactic. |
| Scaled-content abuse | Large-scale low-value or near-duplicate publishing is risky. |
| Schema everywhere by default | Structured data should match real content and real eligibility. |

## Pushback style

When rejecting a tactic:

1. Say it is unsupported, risky, or unnecessary for Google.
2. Replace it with the closest Google-supported alternative.
3. Explain why the replacement better aligns with helpful, crawlable, valuable content.
```

- [ ] **Step 6: Replace the skill README with usage-oriented documentation**

Write `skills/google-seo-geo/README.md`:

```markdown
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
```

- [ ] **Step 7: Verify every reference file exists and is non-empty**

Run:

```bash
for file in \
  skills/google-seo-geo/references/google-search-docs-summary.md \
  skills/google-seo-geo/references/audit-checklist.md \
  skills/google-seo-geo/references/templates.md \
  skills/google-seo-geo/references/anti-patterns.md; do
  test -s "$file" || { echo "missing/empty: $file"; exit 1; }
done
```

Expected: PASS with exit code `0`

- [ ] **Step 8: Commit the reference bundle**

Run:

```bash
git add skills/google-seo-geo/README.md skills/google-seo-geo/references/*.md
git commit -m "feat(google-seo-geo): add reference bundle and skill README"
```

### Task 4: Add realistic evals and expose the new skill in the repo README

**Files:**
- Modify: `skills/google-seo-geo/evals/evals.json`
- Create: `skills/google-seo-geo/evals/trigger-evals.json`
- Modify: `README.md`
- Test: `skills/google-seo-geo/evals/evals.json`

- [ ] **Step 1: Confirm the eval set is still empty**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path('skills/google-seo-geo/evals/evals.json').read_text())
print(len(data['evals']))
PY
```

Expected: `0`

- [ ] **Step 2: Write the final eval set**

Write `skills/google-seo-geo/evals/evals.json`:

```json
{
  "skill_name": "google-seo-geo",
  "evals": [
    {
      "id": 1,
      "prompt": "Audit our pricing page for Google AI Overviews readiness. The page is for a B2B analytics SaaS, and we do have .agents/product-marketing-context.md in the repo. I want a Google-first review of helpful content, snippets, schema opportunities, internal links, and whether the page actually matches our audience.",
      "expected_output": "The skill loads product-marketing context, audits the page against Google-first content and technical criteria, prioritizes issues, and gives concrete fixes plus validation steps without drifting into non-Google GEO hacks.",
      "files": [],
      "assertions": [
        "References or explicitly checks .agents/product-marketing-context.md",
        "Audits both content quality and technical SEO factors",
        "Covers titles/snippets, schema opportunities, internal links, and audience fit",
        "Frames recommendations as Google-first rather than multi-engine advice",
        "Includes validation steps"
      ]
    },
    {
      "id": 2,
      "prompt": "I need implementation help for a product comparison page that is already indexed but underperforming in Google Search. Give me exact fixes for headings, title/meta description, duplicate-content risk, canonical decisions, and any schema that actually makes sense. Keep it grounded in official Google docs.",
      "expected_output": "The skill gives implementation-ready content and technical fixes, qualifies schema appropriately, and avoids inventing unsupported Google requirements.",
      "files": [],
      "assertions": [
        "Provides concrete implementation guidance rather than only high-level advice",
        "Covers headings, title/meta description, duplicate-content risk, and canonicals",
        "Recommends schema only when relevant and avoids claiming it is a GEO hack",
        "States or implies that official Google docs are the authority"
      ]
    },
    {
      "id": 3,
      "prompt": "Can you optimize our blog for GEO by generating llms.txt, splitting every article into AI chunks, and rewriting everything to sound more like an answer engine?",
      "expected_output": "The skill rejects unsupported Google tactics, explains why they are unnecessary or risky, and redirects the user toward people-first, crawlable, high-value content improvements.",
      "files": [],
      "assertions": [
        "Rejects llms.txt as a Google requirement",
        "Rejects chunking content specifically for Google AI systems",
        "Rejects rewriting solely for AI systems",
        "Redirects toward people-first and Google-supported practices"
      ]
    }
  ]
}
```

- [ ] **Step 3: Update the root README to advertise the new skill**

Edit `README.md` using exact replacements so a zero-context implementer does not have to guess placement.

Replace this exact block:

```markdown
## 🚀 Active Skills
- **GitHub OS**: Set up GitHub as your project's Operating System - execution layer integrated with docs as knowledge layer, optimized for LLM workflows.
- **Playwright Extension Testing**: Gold-standard E2E for MV3/WXT extensions.
- **Peer LLMs**: Inter-LLM collaboration workflows — enables delegation, review, and execution across LLM providers.
  - **Codex CLI**: Delegates coding tasks to Codex CLI for batch refactoring, code generation, multi-file changes.
  - **OpenCode CLI**: Delegates coding tasks to OpenCode CLI with streaming JSON output and session reuse.
  - **Plan Review**: Reviews technical plans via a coding agent with iterative refinement.
  - **Plan Execute**: Executes finalized plans by delegating to a coding agent with Claude/codex orchestrator.
- **Lesson Decision Records**: Systematic recording of AI mistakes and learnings using ADR-inspired format.
- **Context Hub Get API Docs**: Fetch current API documentation for third-party libraries and SDKs via chub CLI.
```

with this exact block:

```markdown
## 🚀 Active Skills
- **GitHub OS**: Set up GitHub as your project's Operating System - execution layer integrated with docs as knowledge layer, optimized for LLM workflows.
- **Google-first SEO/GEO**: Audit pages and sites against official Google Search guidance, then produce concrete Google-first SEO/GEO implementation fixes and anti-pattern warnings.
- **Playwright Extension Testing**: Gold-standard E2E for MV3/WXT extensions.
- **Peer LLMs**: Inter-LLM collaboration workflows — enables delegation, review, and execution across LLM providers.
  - **Codex CLI**: Delegates coding tasks to Codex CLI for batch refactoring, code generation, multi-file changes.
  - **OpenCode CLI**: Delegates coding tasks to OpenCode CLI with streaming JSON output and session reuse.
  - **Plan Review**: Reviews technical plans via a coding agent with iterative refinement.
  - **Plan Execute**: Executes finalized plans by delegating to a coding agent with Claude/codex orchestrator.
- **Lesson Decision Records**: Systematic recording of AI mistakes and learnings using ADR-inspired format.
- **Context Hub Get API Docs**: Fetch current API documentation for third-party libraries and SDKs via chub CLI.
```

Then, in the install section, keep the existing `--skill get-api-docs` line unchanged even though the folder naming in this repo differs. Insert the new line immediately after it so the block becomes:

```markdown
npx skills add ZenStudioLab/skills --skill lesson-decision-records
npx skills add ZenStudioLab/skills --skill get-api-docs
npx skills add ZenStudioLab/skills --skill google-seo-geo
```

Do not edit `AGENTS.md` as part of this change. In this repo, skill discovery comes from the `skills/` directory and public listing comes from `README.md`; `AGENTS.md` is workflow guidance, not a skill index.

- [ ] **Step 4: Write the trigger-eval smoke set used by Task 5**

Write `skills/google-seo-geo/evals/trigger-evals.json`:

```json
[
  {
    "query": "Audit our pricing page for Google AI Overviews readiness and show me exactly what to fix in titles, schema, and internal links.",
    "should_trigger": true
  },
  {
    "query": "Can you optimize our blog for GEO by adding llms.txt and chunking every article for answer engines?",
    "should_trigger": true
  },
  {
    "query": "Write a launch email for our new analytics dashboard.",
    "should_trigger": false
  }
]
```

- [ ] **Step 5: Validate the eval JSON parses and contains the expected cases**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path('skills/google-seo-geo/evals/evals.json').read_text())
assert data['skill_name'] == 'google-seo-geo'
assert len(data['evals']) == 3
trigger = json.loads(Path('skills/google-seo-geo/evals/trigger-evals.json').read_text())
assert len(trigger) == 3
print('evals ok')
PY
```

Expected: `evals ok`

- [ ] **Step 6: Verify the root README mentions the new skill**

Run:

```bash
grep -n "Google-first SEO/GEO" README.md
grep -n -- "--skill google-seo-geo" README.md
```

Expected: PASS with both matches present

- [ ] **Step 7: Commit evals and README exposure**

Run:

```bash
git add skills/google-seo-geo/evals/evals.json README.md
git add skills/google-seo-geo/evals/trigger-evals.json
git commit -m "feat(google-seo-geo): add evals and repo docs"
```

### Task 5: Run final integrity validation on the finished skill package

**Files:**
- Test: `skills/google-seo-geo/SKILL.md`
- Test: `skills/google-seo-geo/references/*.md`
- Test: `skills/google-seo-geo/evals/evals.json`
- Test: `README.md`

- [ ] **Step 1: Re-run the repo's skill validator**

Run:

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/google-seo-geo
```

Expected: PASS with `Skill is valid!`

- [ ] **Step 2: Run a reference and eval integrity check**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path

skill = Path('skills/google-seo-geo')
skill_text = (skill / 'SKILL.md').read_text()
required_refs = [
    'references/google-search-docs-summary.md',
    'references/audit-checklist.md',
    'references/templates.md',
    'references/anti-patterns.md',
]
for rel in required_refs:
    assert rel in skill_text, f'missing reference mention: {rel}'
    assert (skill / rel).exists(), f'missing file: {rel}'

assert '.agents/product-marketing-context.md' in skill_text

evals = json.loads((skill / 'evals/evals.json').read_text())
assert evals['skill_name'] == 'google-seo-geo'
assert len(evals['evals']) == 3

ids = {item['id'] for item in evals['evals']}
assert ids == {1, 2, 3}

print('integrity ok')
PY
```

Expected: `integrity ok`

- [ ] **Step 3: Run a trigger-eval smoke check for the new description**

Run:

```bash
python3 -c "import yaml" >/dev/null
command -v opencode >/dev/null || { echo "skip: opencode not installed"; exit 0; }
(
  cd skills/skill-creator &&
  python3 -m scripts.run_eval --help >/dev/null &&
  python3 -m scripts.run_eval \
    --eval-set ../../skills/google-seo-geo/evals/trigger-evals.json \
    --skill-path ../../skills/google-seo-geo \
    --provider opencode \
    --runs-per-query 1 \
    --num-workers 1 \
    --timeout 60 \
    --verbose > /tmp/google-seo-geo-trigger-results.json
)
```

Expected: either prints `skip: opencode not installed` and exits `0`, or exits `0` and writes `/tmp/google-seo-geo-trigger-results.json`

This checks description-trigger behavior only. Full qualitative human review of answer quality is intentionally deferred to the later skill-tuning loop and is out of scope for this initial repo addition.

- [ ] **Step 4: Assert the trigger smoke results when the eval runner actually ran**

Run:

```bash
test ! -f /tmp/google-seo-geo-trigger-results.json && { echo "trigger smoke skipped"; exit 0; }
python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path('/tmp/google-seo-geo-trigger-results.json').read_text())
assert data['summary']['total'] == 3
assert data['summary']['passed'] == 3

by_query = {item['query']: item for item in data['results']}
assert by_query['Audit our pricing page for Google AI Overviews readiness and show me exactly what to fix in titles, schema, and internal links.']['trigger_rate'] > 0
assert by_query['Can you optimize our blog for GEO by adding llms.txt and chunking every article for answer engines?']['trigger_rate'] > 0
assert by_query['Write a launch email for our new analytics dashboard.']['trigger_rate'] == 0

print('trigger smoke ok')
PY
```

Expected: either `trigger smoke skipped` or `trigger smoke ok`

- [ ] **Step 5: Verify the anti-pattern language is present in both skill and reference docs**

Run:

```bash
grep -iE "llms\.txt|chunking|keyword stuffing|scaled-content abuse|fake freshness" skills/google-seo-geo/SKILL.md
grep -iE "llms\.txt|chunking|keyword stuffing|scaled-content abuse|fake freshness" skills/google-seo-geo/references/anti-patterns.md
```

Expected: PASS with matches from both files
