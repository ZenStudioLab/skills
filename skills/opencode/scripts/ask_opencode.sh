#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ask_opencode.sh <task> [options]
  ask_opencode.sh -t <task> [options]

Task input:
  <task>                       First positional argument is the task text
  -t, --task <text>            Alias for positional task (backward compat)
  (stdin)                      Pipe task text via stdin if no arg/flag given

File context (optional, repeatable):
  -f, --file <path>            Priority file path

Multi-turn:
      --session <id>           Resume a previous session

Options:
  -w, --workspace <path>       Workspace directory (default: current directory)
      --model <name>           Model override (format: provider/model)
      --agent <name>          Agent to use
      --read-only             Read-only mode (no file changes)
  -o, --output <path>         Output file path
  -h, --help                  Show this help

Output (on success):
  session_id=<thread_id>       Use with --session for follow-up calls
  output_path=<file>          Path to response markdown

Examples:
  # New task (positional)
  ask_opencode.sh "Add error handling to api.ts" -f src/api.ts

  # With explicit workspace
  ask_opencode.sh "Fix the bug" -w /other/repo

  # Continue conversation
  ask_opencode.sh "Also add retry logic" --session <id>
USAGE
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[ERROR] Missing required command: $1" >&2
    exit 1
  fi
}

trim_whitespace() {
  awk 'BEGIN { RS=""; ORS="" } { gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, ""); print }' <<<"$1"
}

to_abs_if_exists() {
  local target="$1"
  if [[ -e "$target" ]]; then
    local dir
    dir="$(cd "$(dirname "$target")" && pwd)"
    echo "$dir/$(basename "$target")"
    return
  fi
  echo "$target"
}

resolve_file_ref() {
  local workspace="$1" raw="$2" cleaned
  cleaned="$(trim_whitespace "$raw")"
  [[ -z "$cleaned" ]] && { echo ""; return; }
  if [[ "$cleaned" =~ ^(.+)#L[0-9]+$ ]]; then cleaned="${BASH_REMATCH[1]}"; fi
  if [[ "$cleaned" =~ ^(.+):[0-9]+(-[0-9]+)?$ ]]; then cleaned="${BASH_REMATCH[1]}"; fi
  if [[ "$cleaned" != /* ]]; then cleaned="$workspace/$cleaned"; fi
  to_abs_if_exists "$cleaned"
}

append_file_refs() {
  local raw="$1" item
  IFS=',' read -r -a items <<< "$raw"
  for item in "${items[@]}"; do
    local trimmed
    trimmed="$(trim_whitespace "$item")"
    [[ -n "$trimmed" ]] && file_refs+=("$trimmed")
  done
}

# --- Parse arguments ---

workspace="${PWD}"
task_text=""
model=""
agent_name=""
read_only=false
output_path=""
session_id=""
file_refs=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -w|--workspace)   workspace="${2:-}"; shift 2 ;;
    -t|--task)        task_text="${2:-}"; shift 2 ;;
    -f|--file|--focus) append_file_refs "${2:-}"; shift 2 ;;
    --model)          model="${2:-}"; shift 2 ;;
    --agent)          agent_name="${2:-}"; shift 2 ;;
    --read-only)      read_only=true; shift ;;
    --session)        session_id="${2:-}"; shift 2 ;;
    -o|--output)      output_path="${2:-}"; shift 2 ;;
    -h|--help)        usage; exit 0 ;;
    -*)               echo "[ERROR] Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)                if [[ -z "$task_text" ]]; then task_text="$1"; shift; else echo "[ERROR] Unexpected argument: $1" >&2; usage >&2; exit 1; fi ;;
  esac
done

require_cmd opencode

# --- Validate inputs ---

if [[ ! -d "$workspace" ]]; then
  echo "[ERROR] Workspace does not exist: $workspace" >&2; exit 1
fi
workspace="$(cd "$workspace" && pwd)"

if [[ -z "$task_text" && ! -t 0 ]]; then
  task_text="$(cat)"
fi
task_text="$(trim_whitespace "$task_text")"

if [[ -z "$task_text" ]]; then
  echo "[ERROR] Request text is empty. Pass a positional arg, --task, or stdin." >&2; exit 1
fi

# --- Prepare output path ---

if [[ -z "$output_path" ]]; then
  timestamp="$(date -u +"%Y%m%d-%H%M%S")"
  skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  output_path="$skill_dir/.runtime/${timestamp}.md"
fi
mkdir -p "$(dirname "$output_path")"

# --- Build file context block ---

file_block=""
if (( ${#file_refs[@]} > 0 )); then
  file_block=$'\n\nPriority files (read these first before making changes):'
  for ref in "${file_refs[@]}"; do
    resolved="$(resolve_file_ref "$workspace" "$ref")"
    [[ -z "$resolved" ]] && continue
    exists_tag="missing"
    [[ -e "$resolved" ]] && exists_tag="exists"
    file_block+=$'\n- '"${resolved} (${exists_tag})"
  done
fi

# --- Build prompt ---

prompt="$task_text"
if [[ -n "$file_block" ]]; then
  prompt+=$'\n'"$file_block"
fi

# --- Build opencode command ---

if [[ -n "$session_id" ]]; then
  # Resume mode
  cmd=(opencode run --continue --session "$session_id" --format json)
  [[ -n "$model" ]] && cmd+=(--model "$model")
  [[ -n "$agent_name" ]] && cmd+=(--agent "$agent_name")
else
  # New session
  cmd=(opencode run --format json)
  [[ -n "$model" ]] && cmd+=(--model "$model")
  [[ -n "$agent_name" ]] && cmd+=(--agent "$agent_name")
fi

# --- Execute and capture JSON output ---

stderr_file="$(mktemp)"
json_file="$(mktemp)"
prompt_file="$(mktemp)"
trap 'rm -f "$stderr_file" "$json_file" "$prompt_file"' EXIT

printf "%s" "$prompt" > "$prompt_file"

# OpenCode's run command outputs JSONL without block-buffering,
# so no PTY (script) wrapper is needed unlike codex.
cd "$workspace"
"${cmd[@]}" "$(cat "$prompt_file")" 2>"$stderr_file" | while IFS= read -r line; do
  # Strip terminal artifacts
  cleaned="${line//$'\r'/}"
  cleaned="${cleaned//$'\004'/}"
  cleaned="$(printf '%s' "$cleaned" | sed $'s/\x1b\[[0-9;]*[a-zA-Z]//g; s/^[^{]*//')"
  [[ -z "$cleaned" ]] && continue
  [[ "$cleaned" != \{* ]] && continue
  printf '%s\n' "$cleaned" >> "$json_file"
done

if [[ -s "$stderr_file" ]] && grep -q '\[ERROR\]' "$stderr_file" 2>/dev/null; then
  echo "[ERROR] OpenCode command failed" >&2
  cat "$stderr_file" >&2
  exit 1
fi

if [[ -s "$stderr_file" ]]; then
  cat "$stderr_file" >&2
fi

# --- Parse JSON stream ---
# Note: JSON format may vary. This parses common opencode output patterns.
# If opencode outputs ndjson with type/text fields similar to codex, this works.
# Adjust jq selectors based on actual output format.

thread_id="$(jq -r 'select(.type == "thread.started" or .type == "started") | .thread_id // .id // empty' < "$json_file" 2>/dev/null | head -1)"

{
  # Show command executions
  jq -r '
    select(.type == "item.completed" and (.item.type == "command_execution" or .item.type == "shell"))
    | .item
    | if .command then
        "### Shell: `" + (.command // "unknown")[0:200] + "`\n" + (.output // "" | .[0:500])
      elif .arguments and (.arguments | fromjson | .command) then
        "### Shell: `" + (.arguments | fromjson | .command // "unknown")[0:200] + "`\n" + (.output // "" | .[0:500])
      else empty
      end
  ' < "$json_file" 2>/dev/null

  # Show file operations
  jq -r '
    select(.type == "item.completed" and (.item.type == "tool_call" or .item.name))
    | .item
    | if .name == "write_file" or .name == "Write" then
        "### File written: " + (.arguments | fromjson | .path // "unknown")
      elif .name == "patch_file" or .name == "Patch" then
        "### File patched: " + (.arguments | fromjson | .path // "unknown")
      elif .name == "edit_file" or .name == "Edit" then
        "### File edited: " + (.arguments | fromjson | .path // "unknown")
      else empty
      end
  ' < "$json_file" 2>/dev/null

  # Show agent messages
  jq -r '
    select(.type == "item.completed" and .item.type == "agent_message")
    | .item.text
  ' < "$json_file" 2>/dev/null

  # Fallback: show any text content from completed items
  jq -r '
    select(.type == "item.completed" and .item.text)
    | .item.text
  ' < "$json_file" 2>/dev/null
} > "$output_path"

if [[ ! -s "$output_path" ]]; then
  echo "(no response from opencode)" > "$output_path"
fi

# --- Output results ---

if [[ -n "$thread_id" ]]; then
  echo "session_id=$thread_id"
fi
echo "output_path=$output_path"
