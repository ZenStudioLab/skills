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

Watch mode:
  -W, --watch                  Stream output to stdout while writing to files

Status:
      --status <session_id>   Check status of a running session

Options:
  -w, --workspace <path>       Workspace directory (default: current directory)
      --model <name>           Model override (format: provider/model)
      --agent <name>          Agent to use
  -o, --output <path>         Output file path
  -h, --help                  Show this help

Output (on success):
  session_id=<thread_id>       Use with --session for follow-up calls
  output_path=<file>          Path to response markdown
  status_path=<file>          Path to status file (while running)

Status file format:
  status=running|completed|failed
  session_id=<id>
  started_at=<timestamp>
  last_activity=<description>
  progress_path=<file>

Progress file format (JSONL):
  {"ts":"<timestamp>","type":"activity","msg":"<description>"}
  {"ts":"<timestamp>","type":"shell","cmd":"<command>","output":"<output>"}
  {"ts":"<timestamp>","type":"file","action":"write|edit|patch","path":"<file>"}
  {"ts":"<timestamp>","type":"message","text":"<agent message>"}

Examples:
  # New task (positional)
  ask_opencode.sh "Add error handling to api.ts" -f src/api.ts

  # With explicit workspace
  ask_opencode.sh "Fix the bug" -w /other/repo

  # Continue conversation
  ask_opencode.sh "Also add retry logic" --session <id>

  # Watch mode - stream output while running
  ask_opencode.sh "Refactor auth module" --watch

  # Check status of running session
  ask_opencode.sh --status ses_xxxx
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

write_status() {
  local status_file="$1"
  local status="$2"
  local session_id="$3"
  local activity="$4"
  local progress_file="$5"
  {
    echo "status=$status"
    [[ -n "$session_id" ]] && echo "session_id=$session_id"
    echo "started_at=$start_time"
    echo "last_activity=$activity"
    echo "progress_path=$progress_file"
  } > "$status_file"
}

write_progress() {
  local progress_file="$1"
  local type="$2"
  local msg="$3"
  local ts
  ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  printf '{"ts":"%s","type":"%s","msg":%s}\n' "$ts" "$type" "$(jq -n --arg v "$msg" '$v')" >> "$progress_file"
}

show_status() {
  local session_id="$1"
  local skill_dir="$2"

  # Find status file by session_id
  local status_file
  status_file="$(find "$skill_dir/.runtime" -name "*.status" 2>/dev/null | while read -r f; do
    if grep -q "session_id=$session_id" "$f" 2>/dev/null; then
      echo "$f"
    fi
  done | head -1)"

  if [[ -z "$status_file" ]]; then
    echo "[ERROR] No status file found for session: $session_id" >&2
    echo "Status: unknown (session may have completed)" >&2
    exit 1
  fi

  cat "$status_file"
  echo ""

  local progress_file
  progress_file="$(grep "^progress_path=" "$status_file" | cut -d= -f2)"
  if [[ -n "$progress_file" && -f "$progress_file" ]]; then
    echo "--- Recent Activity ---"
    tail -20 "$progress_file" 2>/dev/null | jq -r 'select(.msg) | "[\(.ts)] \(.msg)"' 2>/dev/null || tail -20 "$progress_file"
  fi
}

# --- Parse arguments ---

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
workspace="${PWD}"
task_text=""
model=""
agent_name=""
output_path=""
session_id=""
file_refs=()
watch_mode=false
status_mode=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -w|--workspace)   workspace="${2:-}"; shift 2 ;;
    -t|--task)        task_text="${2:-}"; shift 2 ;;
    -f|--file|--focus) append_file_refs "${2:-}"; shift 2 ;;
    --model)          model="${2:-}"; shift 2 ;;
    --agent)          agent_name="${2:-}"; shift 2 ;;
    --session)        session_id="${2:-}"; shift 2 ;;
    -o|--output)      output_path="${2:-}"; shift 2 ;;
    -W|--watch)       watch_mode=true; shift ;;
    --status)         status_mode=true; session_id="${2:-}"; shift 2 ;;
    -h|--help)        usage; exit 0 ;;
    -*)               echo "[ERROR] Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)                if [[ -z "$task_text" ]]; then task_text="$1"; shift; else echo "[ERROR] Unexpected argument: $1" >&2; usage >&2; exit 1; fi ;;
  esac
done

# Status mode - show status and exit
if $status_mode; then
  show_status "$session_id" "$skill_dir"
  exit 0
fi

require_cmd opencode
require_cmd jq

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

# --- Prepare output paths ---

timestamp="$(date -u +"%Y%m%d-%H%M%S")"
if [[ -z "$output_path" ]]; then
  output_path="$skill_dir/.runtime/${timestamp}.md"
fi
mkdir -p "$(dirname "$output_path")"
mkdir -p "$skill_dir/.runtime"

status_file="${output_path%.md}.status"
progress_file="${output_path%.md}.progress"

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
  cmd=(opencode run --continue --session "$session_id" --format json)
  [[ -n "$model" ]] && cmd+=(--model "$model")
  [[ -n "$agent_name" ]] && cmd+=(--agent "$agent_name")
else
  cmd=(opencode run --format json)
  [[ -n "$model" ]] && cmd+=(--model "$model")
  [[ -n "$agent_name" ]] && cmd+=(--agent "$agent_name")
fi

# --- Execute ---

start_time="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
write_status "$status_file" "running" "" "Starting task..." "$progress_file"
> "$progress_file"  # Clear progress file

if $watch_mode; then
  echo "[INFO] Starting opencode task (watch mode)..." >&2
  echo "[INFO] Output: $output_path" >&2
  echo "[INFO] Status: $status_file" >&2
  echo "[INFO] Progress: $progress_file" >&2
fi

stderr_file="$(mktemp)"
json_file="$(mktemp)"
prompt_file="$(mktemp)"
trap 'rm -f "$stderr_file" "$json_file" "$prompt_file"' EXIT

printf "%s" "$prompt" > "$prompt_file"

cd "$workspace"
declare -a activity_buffer=()
declare -a shell_buffer=()
declare -a file_buffer=()

{
  # Stream opencode output directly to while loop (no & backgrounding)
  # stderr goes to stderr_file, stdout is piped to while loop
  "${cmd[@]}" "$(cat "$prompt_file")" 2>"$stderr_file" | while IFS= read -r line; do
    # Clean line
    cleaned="${line//$'\r'/}"
    cleaned="${cleaned//$'\004'/}"
    cleaned="$(printf '%s' "$cleaned" | sed $'s/\x1b\[[0-9;]*[a-zA-Z]//g; s/^[^{]*//')"
    [[ -z "$cleaned" ]] && continue
    [[ "$cleaned" != \{* ]] && continue

    # Extract session_id if present (early)
    if [[ -z "$session_id" ]]; then
      extracted="$(printf '%s' "$cleaned" | jq -r '.sessionID // .thread_id // .id // empty' 2>/dev/null)"
      [[ -n "$extracted" ]] && session_id="$extracted"
      if [[ -n "$session_id" ]]; then
        write_status "$status_file" "running" "$session_id" "Session started" "$progress_file"
        if $watch_mode; then
          echo "[INFO] Session started: $session_id" >&2
        fi
      fi
    fi

    # Parse and categorize - opencode uses step_start, text, step_finish format
    type="$(printf '%s' "$cleaned" | jq -r '.type // empty' 2>/dev/null)"
    msg=""
    progress_type="activity"

    case "$type" in
      "step_start")
        msg="Task started"
        write_progress "$progress_file" "activity" "$msg"
        ;;
      "text")
        text_content="$(printf '%s' "$cleaned" | jq -r '.part.text // ""' 2>/dev/null)"
        if [[ -n "$text_content" ]]; then
          msg="Response: ${text_content:0:200}"
          progress_type="message"
          write_progress "$progress_file" "$progress_type" "$msg"
        fi
        ;;
      "step_finish")
        msg="Task finished"
        write_progress "$progress_file" "complete" "$msg"
        ;;
      "item_start"|"item_completed")
        item_type="$(printf '%s' "$cleaned" | jq -r '.item.type // .item.name // empty' 2>/dev/null)"
        if [[ "$item_type" == "command_execution" || "$item_type" == "shell" ]]; then
          cmd_name="$(printf '%s' "$cleaned" | jq -r '.item.command // (.item.arguments | fromjson | .command) // "unknown"' 2>/dev/null)"
          output="$(printf '%s' "$cleaned" | jq -r '.item.output // ""' 2>/dev/null | head -c 200)"
          msg="Shell: ${cmd_name:0:100}"
          if [[ -n "$output" ]]; then
            msg+=" → ${output:0:100}"
          fi
          progress_type="shell"
        elif [[ "$item_type" == "tool_call" ]]; then
          item_name="$(printf '%s' "$cleaned" | jq -r '.item.name // empty' 2>/dev/null)"
          if [[ "$item_name" == "write_file" || "$item_name" == "Write" ]]; then
            tool_path="$(printf '%s' "$cleaned" | jq -r '.item.arguments | fromjson | .path // "unknown"' 2>/dev/null)"
            msg="File written: $tool_path"
            progress_type="file"
          elif [[ "$item_name" == "patch_file" || "$item_name" == "Patch" ]]; then
            tool_path="$(printf '%s' "$cleaned" | jq -r '.item.arguments | fromjson | .path // "unknown"' 2>/dev/null)"
            msg="File patched: $tool_path"
            progress_type="file"
          elif [[ "$item_name" == "edit_file" || "$item_name" == "Edit" ]]; then
            tool_path="$(printf '%s' "$cleaned" | jq -r '.item.arguments | fromjson | .path // "unknown"' 2>/dev/null)"
            msg="File edited: $tool_path"
            progress_type="file"
          fi
        fi
        [[ -n "$msg" ]] && write_progress "$progress_file" "$progress_type" "$msg"
        ;;
      *)
        # Try generic parsing for unknown types
        item_type="$(printf '%s' "$cleaned" | jq -r '.item.type // .item.name // empty' 2>/dev/null)"
        if [[ "$item_type" == "tool_call" ]]; then
          tool_name="$(printf '%s' "$cleaned" | jq -r '.item.name // empty' 2>/dev/null)"
          if [[ "$tool_name" == "write_file" || "$tool_name" == "Write" ]]; then
            tool_path="$(printf '%s' "$cleaned" | jq -r '.item.arguments | fromjson | .path // "unknown"' 2>/dev/null)"
            msg="File written: $tool_path"
            write_progress "$progress_file" "file" "$msg"
          fi
        fi
        ;;
    esac

    if [[ -n "$msg" ]] && $watch_mode && [[ "$type" != "step_start" ]]; then
      echo "$msg" >&2
    fi

    if [[ -n "$msg" ]]; then
      write_progress "$progress_file" "$progress_type" "$msg"
      activity_buffer+=("$msg")

      if $watch_mode; then
        echo "$msg" >&2
      fi
    fi

    printf '%s\n' "$cleaned" >> "$json_file"

  done
  # Pipe closes when opencode finishes, while loop exits

} 2>&1 | head -c 100M  # capture any remaining stderr, prevent infinite pipe

if [[ -s "$stderr_file" ]] && grep -q '\[ERROR\]' "$stderr_file" 2>/dev/null; then
  write_status "$status_file" "failed" "$session_id" "Command failed" "$progress_file"
  write_progress "$progress_file" "error" "OpenCode command failed"
  echo "[ERROR] OpenCode command failed" >&2
  cat "$stderr_file" >&2
  exit 1
fi

if [[ -s "$stderr_file" ]] && ! $watch_mode; then
  cat "$stderr_file" >&2
fi

# --- Parse and write final output ---
# opencode uses: step_start, text (with part.text), step_finish, item_started, item_completed

{
  # Text responses (main content) - most important
  jq -r '
    select(.type == "text" and .part.text)
    | .part.text
  ' < "$json_file" 2>/dev/null

  # Shell commands (from item_completed)
  jq -r '
    select(.type == "item_completed" and (.item.type == "command_execution" or .item.type == "shell"))
    | .item
    | if .command then
        "### Shell: `" + (.command // "unknown")[0:200] + "`\n" + (.output // "" | .[0:500])
      elif .arguments and (.arguments | fromjson | .command) then
        "### Shell: `" + (.arguments | fromjson | .command // "unknown")[0:200] + "`\n" + (.output // "" | .[0:500])
      else empty
      end
  ' < "$json_file" 2>/dev/null

  # File operations (from item_completed)
  jq -r '
    select(.type == "item_completed" and (.item.type == "tool_call" or .item.name))
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

  # Tool calls with name field (alternative format)
  jq -r '
    select(.item.name)
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
} > "$output_path"

if [[ ! -s "$output_path" ]]; then
  echo "(no response from opencode)" > "$output_path"
fi

# Update status to completed - extract session_id from json_file if not set
if [[ -z "$session_id" ]] && [[ -s "$json_file" ]]; then
  session_id="$(jq -r '.sessionID // .thread_id // .id // empty' "$json_file" 2>/dev/null | head -1)"
fi
write_status "$status_file" "completed" "$session_id" "Task completed" "$progress_file"
write_progress "$progress_file" "complete" "Task finished"

if $watch_mode; then
  echo "[INFO] Task completed. Output: $output_path" >&2
fi

# --- Output results ---

if [[ -n "$session_id" ]]; then
  echo "session_id=$session_id"
fi
echo "output_path=$output_path"
echo "status_path=$status_file"