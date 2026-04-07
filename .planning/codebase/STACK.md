# Technology Stack

**Analysis Date:** 2026-04-07

## Languages

**Primary:**
- Markdown (no pinned version) - Skill definitions and docs in `README.md`, `AGENTS.md`, `skills/*/SKILL.md`, `skills/*/README.md`

**Secondary:**
- Shell/Bash (no pinned version) - Automation wrappers in `skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`
- Python 3 (version not pinned in repo) - Evaluation/report tooling in `skills/skill-creator/scripts/*.py`, `skills/skill-creator/eval-viewer/generate_review.py`, `skills/github-os/evals/run_gemini_eval.py`
- TypeScript (version not pinned in repo) - Playwright boilerplate/config in `dummy-extension-project/playwright.config.ts`, `skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`, `skills/extension-testing-expert-skill/assets/boilerplate/extension-helper.ts`
- JSON/YAML (no pinned version) - Eval and template data in `evals/evals.json`, `skills/github-os/evals/evals.json`, `skills/github-os/assets/issue-templates/*.yml`

## Runtime

**Environment:**
- Node.js runtime (version not pinned) required by documented CLI/tooling flows in `README.md`, `skills/github-os/assets/github-mcp-setup.md`, `skills/extension-testing-expert-skill/README.md`
- POSIX shell runtime for helper scripts in `skills/codex/scripts/ask_codex.sh` and `skills/opencode/scripts/ask_opencode.sh`
- Python runtime for eval/report scripts in `skills/skill-creator/scripts/run_eval.py` and related files

**Package Manager:**
- npm/npx is the only package manager explicitly documented (`README.md`, `skills/github-os/assets/github-mcp-setup.md`)
- Lockfile: missing at repo root (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` not present in `/mnt/8CE085C2E085B2CE/Src/Tools/skills`)

## Frameworks

**Core:**
- Agent Skills spec + skills.sh integration (no pinned version) - Repository’s delivery target described in `README.md` and `AGENTS.md`

**Testing:**
- Playwright (`@playwright/test`, version not pinned in repo) - Extension E2E config patterns in `dummy-extension-project/playwright.config.ts` and `skills/extension-testing-expert-skill/SKILL.md`

**Build/Dev:**
- Codex CLI (version not pinned) - delegated coding workflow in `skills/codex/SKILL.md` and `skills/codex/scripts/ask_codex.sh`
- OpenCode CLI (version not pinned) - delegated coding workflow in `skills/opencode/SKILL.md` and `skills/opencode/scripts/ask_opencode.sh`
- Gemini CLI (version not pinned) - eval runner integration in `skills/github-os/evals/run_gemini_eval.py`
- chub CLI (version not pinned) - API doc retrieval workflow in `skills/context-hub-get-api-docs/SKILL.md`
- GitHub MCP server package `@modelcontextprotocol/server-github` (version not pinned) - setup in `skills/github-os/assets/github-mcp-setup.md`

## Key Dependencies

**Critical:**
- `codex` CLI binary - powers Codex delegation scripts in `skills/codex/scripts/ask_codex.sh`
- `opencode` CLI binary - powers OpenCode delegation scripts in `skills/opencode/scripts/ask_opencode.sh`
- `jq` - required for JSON event parsing in both shell wrappers (`skills/codex/scripts/ask_codex.sh`, `skills/opencode/scripts/ask_opencode.sh`)

**Infrastructure:**
- `@modelcontextprotocol/server-github` - GitHub MCP bridge for automated GitHub operations (`skills/github-os/assets/github-mcp-setup.md`)
- `gh` CLI - fallback GitHub automation path (`skills/github-os/assets/github-mcp-setup.md`)
- `xvfb-run` - Linux CI/display requirement for non-headless extension tests (`skills/extension-testing-expert-skill/SKILL.md`)

## Configuration

**Environment:**
- Repo is documentation/script-first; no root app config manifest detected (`package.json`, `pyproject.toml`, `requirements.txt` missing at repo root)
- Script behavior is primarily configured via CLI flags and local files (`evals/evals.json`, `skills/*/evals/*.json`, `reviews/`, `.runtime/` paths referenced in skill docs)

**Build:**
- Not applicable as a compiled app: no root build config detected (no `tsconfig.json`, `vite.config.*`, `webpack.config.*`, `pyproject.toml`)
- Template/build-like config examples exist for consumers, not this repo runtime (`dummy-extension-project/playwright.config.ts`, `skills/extension-testing-expert-skill/assets/boilerplate/playwright.config.ts`)

## Platform Requirements

**Development:**
- Git + shell environment to edit and version markdown skills (`AGENTS.md`, `README.md`)
- Node/npm tooling for installing and using MCP/CLI integrations (`README.md`, `skills/github-os/assets/github-mcp-setup.md`)
- Python 3 for skill-eval automation (`skills/skill-creator/scripts/run_eval.py`)

**Production:**
- Not applicable: repository is distributed as source markdown/scripts via git and skills installer workflows (`README.md`)

---

*Stack analysis: 2026-04-07*
