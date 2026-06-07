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

~/.agents/skills/opencode/scripts/ask_opencode.sh "Your request"
~/.agents/skills/opencode/scripts/ask_opencode.sh "Refactor" --file src/components/UserList.tsx --file src/components/UserDetail.tsx
~/.agents/skills/opencode/scripts/ask_opencode.sh "Continue task" --session <session_id>
~/.agents/skills/opencode/scripts/ask_opencode.sh "Complex task" --watch
~/.agents/skills/opencode/scripts/ask_opencode.sh --status <session_id>

Output Format:
session_id=<thread_id>
output_path=<path to markdown file>
status_path=<path to status file>  # while running

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
- `-W, --watch` - Stream output to stdout while writing to files (for long tasks)
- `--status <session_id>` - Check status of a running session

## Status & Progress Tracking

While a task is running, the script writes status files to `.runtime/` in the **project/workspace directory**:

**Status file** (`.runtime/<timestamp>.status`):
```
status=running|completed|failed
session_id=<id>
started_at=<timestamp>
last_activity=<description>
progress_path=<file>
```

**Progress file** (`.runtime/<timestamp>.progress` - JSONL):
```jsonl
{"ts":"2026-04-02T10:00:00Z","type":"shell","msg":"Shell: pnpm build → success"}
{"ts":"2026-04-02T10:00:05Z","type":"file","msg":"File written: src/api.ts"}
{"ts":"2026-04-02T10:00:10Z","type":"message","msg":"Running tests..."}
```

**Checking status:**
```bash
ask_opencode.sh --status <session_id>
```

**Watch mode** - streams activity to stderr as it happens:
```bash
ask_opencode.sh "Complex refactor" --watch
```

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
| **Watch mode** | `--watch` streams to stdout | Not available |
| **Status tracking** | `.runtime/*.status` + `*.progress` | Not available |
