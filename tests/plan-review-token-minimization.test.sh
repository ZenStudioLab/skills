#!/usr/bin/env bash
set -euo pipefail

failures=0

pass() {
  echo "PASS: $1"
}

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check() {
  local name="$1"
  shift
  if "$@"; then
    pass "$name"
  else
    fail "$name"
  fi
}

check "warning comment exists above usage heredoc" \
  grep -q "^# WARNING: Do not embed external file content inside this heredoc\\.$" skills/opencode/scripts/ask_opencode.sh

help_lines="$(bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | wc -l | tr -d ' ')"
check "help output is compact (<= 40 lines)" test "${help_lines}" -le 40

check "help output documents required flags" \
  bash -c "bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--workspace' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--task' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--file' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--output' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--session' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--model' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--agent' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--reasoning' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--watch' && \
           bash skills/opencode/scripts/ask_opencode.sh --help 2>&1 | grep -q -- '--status'"

check "Step 2 prompt starts with NON-INTERACTIVE line" \
  grep -q "^NON-INTERACTIVE: Complete this review autonomously. Do not ask questions or prompt for input\\.$" skills/plan-review/SKILL.md

check "Step 2 requirements repeat NON-INTERACTIVE rule" \
  grep -q "^- NON-INTERACTIVE: do not ask clarifying questions at any point$" skills/plan-review/SKILL.md

check "review template includes machine-readable trailer" \
  grep -q "^CONSENSUS_STATUS=NEEDS_REVISION$" skills/plan-review/SKILL.md

check "Step 3 uses grep+tail+cut extraction" \
  grep -q 'status=$(grep "^CONSENSUS_STATUS=" "$review_file" | tail -1 | cut -d= -f2)' skills/plan-review/SKILL.md

check "Step 3 includes fallback to NEEDS_REVISION" \
  grep -q 'status="NEEDS_REVISION"' skills/plan-review/SKILL.md

if [[ "$failures" -gt 0 ]]; then
  echo "RESULT: FAIL ($failures checks failed)"
  exit 1
fi

echo "RESULT: PASS"
