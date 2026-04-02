---
name: opencode
description: Delegate coding tasks to OpenCode CLI for execution, or discuss implementation approaches with it. OpenCode is a free, open-source AI coding agent with broad model support (Claude, GPT, Gemini, and 75+ providers via Models.dev). Use when the plan is clear and needs hands-on coding. Claude handles architecture, strategy, copywriting, and ambiguous problems better.
---

## Critical Rules (Black Box Protocol)

- ONLY interact with OpenCode through the bundled shell script
- Run script ONCE per task, read output file and proceed (no re-runs)
- Do NOT read or inspect the script source code (black box)
- Always quote file paths with brackets/spaces/special chars
- Keep task prompt focused (~500 words max)
- Never paste file contents in prompt - use `--file` flag instead
- Don't reference SKILL.md itself in prompts

## How to Call the Script

~/.claude/skills/opencode/scripts/ask_opencode.sh "Your request"
~/.claude/skills/opencode/scripts/ask_opencode.sh "Refactor" --file src/components/UserList.tsx --file src/components/UserDetail.tsx
~/.claude/skills/opencode/scripts/ask_opencode.sh "Continue task" --session <session_id>

Output Format:
session_id=<thread_id>
output_path=<path to markdown file>

## Decision Policy (When to Call)

- Implementation plan is clear and needs coding execution
- Batch refactoring, code generation, repetitive changes
- Multiple files need coordinated modifications
- Using free/open-source models (OpenCode supports free models)
- Multi-turn conversations where you want to continue a session
- Writing/updating tests based on existing code
- Simple-to-moderate bug fixes with identified root cause

**When to prefer OpenCode over Codex:**
- You want to use free models or a broader range of providers
- You prefer open-source tooling
- Session continuation is important for your workflow

**When to prefer Codex over OpenCode:**
- You have an existing Codex workflow and prefer its specific features
- You need Codex's specific tool ecosystem

## Script Options

- `--workspace <path>` - Target workspace (default: current)
- `--file <path>` - Entry-point files (repeatable)
- `--session <id>` - Resume a previous session
- `--model <name>` - Override model (format: provider/model)
- `--agent <name>` - Use a specific agent
- `--read-only` - Read-only mode (no file changes)

## Workflow

1. **Prepare**: Write your task prompt and identify relevant files
2. **Execute**: Run `ask_opencode.sh` with task and file context
3. **Review**: Read the output markdown for results and session ID
4. **Continue**: Use `--session <id>` to continue the conversation if needed

## Comparison with Codex Skill

| Feature | OpenCode | Codex |
|---------|----------|-------|
| **Cost** | Free (open-source) | Paid |
| **Models** | 75+ providers | OpenAI only |
| **Protocol** | ACP (Agent Client Protocol) | JSON-RPC |
| **CLI** | `opencode run` | `codex exec` |
| **Session** | `--session <id>` | `--session <id>` |
| **File context** | `--file <path>` | `--file <path>` |
| **PTY workaround** | Not needed | Required |
