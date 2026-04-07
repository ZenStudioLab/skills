# External Integrations

**Analysis Date:** 2026-04-07

## APIs & External Services

**Developer Tooling APIs:**
- GitHub API - used through MCP server/CLI workflows for issues, labels, templates, and project operations
  - SDK/Client: `@modelcontextprotocol/server-github` (documented in `skills/github-os/assets/github-mcp-setup.md`)
  - Auth: `GITHUB_TOKEN`
- GitHub API (fallback path) - used through `gh` CLI fallback flow
  - SDK/Client: `gh` CLI (documented in `skills/github-os/assets/github-mcp-setup.md`)
  - Auth: `gh auth login` session / GitHub token
- Context Hub docs service - fetches third-party API docs via CLI workflow
  - SDK/Client: `chub` CLI (`skills/context-hub-get-api-docs/SKILL.md`)
  - Auth: Not specified in repo

**LLM Provider CLIs (execution/eval):**
- Codex/OpenAI CLI integration - shell wrapper orchestration in `skills/codex/scripts/ask_codex.sh`
  - SDK/Client: `codex` CLI
  - Auth: managed by local CLI config (no repo-stored var detected)
- OpenCode provider integration - shell wrapper orchestration in `skills/opencode/scripts/ask_opencode.sh`
  - SDK/Client: `opencode` CLI
  - Auth: managed by local CLI config (no repo-stored var detected)
- Gemini CLI integration for eval runs in `skills/github-os/evals/run_gemini_eval.py`
  - SDK/Client: `gemini` CLI
  - Auth: provider CLI auth + optional `GEMINI_BIN` path override

## Data Storage

**Databases:**
- Not detected as an active integration in this repository
  - Connection: Not applicable
  - Client: Not applicable

**File Storage:**
- Local filesystem only
  - Skill source files under `skills/`
  - Eval artifacts under `evals/`, `skills/*/evals/`, `*-workspace/`
  - Review/runtime artifacts under `reviews/` and `.runtime/` (referenced in `skills/plan-execute/SKILL.md`)

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- GitHub Personal Access Token for GitHub MCP integration
  - Implementation: token provided via MCP config environment (`GITHUB_TOKEN`) as shown in `skills/github-os/assets/github-mcp-setup.md`

## Monitoring & Observability

**Error Tracking:**
- None detected

**Logs:**
- Local file-based execution/review logs for plan workflows (`.runtime/{timestamp}-{session-id}.log.md` pattern in `skills/plan-execute/SKILL.md`)

## CI/CD & Deployment

**Hosting:**
- Not applicable for this repo (content package of markdown skills and helper scripts)

**CI Pipeline:**
- No root CI configuration detected (`.github/workflows/` not present in scanned tree)
- CI guidance exists inside skill content for consumer projects (e.g., xvfb + Playwright in `skills/extension-testing-expert-skill/SKILL.md`)

## Environment Configuration

**Required env vars:**
- `GITHUB_TOKEN` for GitHub MCP server (`skills/github-os/assets/github-mcp-setup.md`)

**Optional env vars:**
- `GEMINI_BIN` for selecting Gemini CLI binary (`skills/github-os/evals/run_gemini_eval.py`)
- `CI` toggle used by Playwright configs in templates/examples (`dummy-extension-project/playwright.config.ts`)

**Secrets location:**
- User-level MCP/CLI configuration (examples: `~/.windsurf/mcp-config.json`, Claude Desktop config paths documented in `skills/github-os/assets/github-mcp-setup.md`)
- No project `.env` files detected at repository root

## Webhooks & Callbacks

**Incoming:**
- None detected in this repository

**Outgoing:**
- None detected as active implementation
- Webhook references appear only as documentation examples (e.g., annotation text in `skills/context-hub-get-api-docs/SKILL.md`)

---

*Integration audit: 2026-04-07*
