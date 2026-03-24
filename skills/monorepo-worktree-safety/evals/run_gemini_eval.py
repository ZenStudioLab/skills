#!/usr/bin/env python3
"""Run monorepo-worktree-safety evals with Gemini CLI in with-skill/without-skill mode.

Usage:
  python3 skills/monorepo-worktree-safety/evals/run_gemini_eval.py

Notes:
  - Resumable: existing run outputs are skipped.
  - Creates/uses workspace: skills/monorepo-worktree-workspace/iteration-N
  - Requires Gemini CLI binary available at GEMINI_BIN env var or `gemini` in PATH.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVALS_PATH = ROOT / "skills/monorepo-worktree-safety/evals/evals.json"
WORKSPACE = ROOT / "skills/monorepo-worktree-workspace"
GEMINI = os.environ.get("GEMINI_BIN", "gemini")


def parse_json_tail(stdout_text: str) -> dict:
    start = stdout_text.rfind("\n{")
    if start < 0:
        start = stdout_text.find("{")
    if start < 0:
        raise ValueError("No JSON payload found in Gemini output")

    candidate = stdout_text[start:].strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    depth = 0
    in_str = False
    esc = False
    for idx, ch in enumerate(candidate):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(candidate[: idx + 1])
    raise ValueError("Unable to parse JSON payload from Gemini output")


def run_gemini(prompt: str, timeout_sec: int = 800) -> tuple[dict, str, int, int]:
    t0 = time.time()
    proc = subprocess.run(
        [
            GEMINI,
            "-p",
            prompt,
            "--output-format",
            "json",
            "--approval-mode",
            "yolo",
            "--allowed-mcp-server-names",
            "",
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        timeout=timeout_sec,
    )
    duration_ms = int((time.time() - t0) * 1000)
    if proc.returncode != 0:
        raise RuntimeError(
            f"gemini failed rc={proc.returncode}; stdout={proc.stdout[:260]!r}; stderr={proc.stderr[:180]!r}"
        )

    payload = parse_json_tail(proc.stdout)
    total_tokens = 0
    for model_info in payload.get("stats", {}).get("models", {}).values():
        total_tokens += int(model_info.get("tokens", {}).get("total", 0) or 0)

    return payload, proc.stdout, duration_ms, total_tokens


def evidence_snippet(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if not match:
        return "No matching evidence found in output."
    start = max(0, match.start() - 60)
    end = min(len(text), match.end() + 120)
    return text[start:end].replace("\n", " ")[:220]


def grade(eval_id: int, assertions: list[str], text: str) -> list[dict]:
    low = text.lower()

    def has_all(items: list[str]) -> bool:
        return all(i.lower() in low for i in items)

    def has_any(items: list[str]) -> bool:
        return any(i.lower() in low for i in items)

    if eval_id == 1:
        # Eval 1: pnpm monorepo, workspace package resolution failure
        checks = [
            # 1. Runs or references the verification script
            (
                has_any(["verify-monorepo-worktree.sh", "worktree-check", "verification script", "check script"]),
                r"verify-monorepo-worktree\.sh|worktree-check|verification script|check script",
            ),
            # 2. Identifies workspace package resolution as the root cause
            (
                has_any(["workspace package", "cannot resolve", "@org/", "workspace:*", "resolution failure", "package resolution", "workspace protocol"]),
                r"workspace package|cannot resolve|@org/|workspace:\*|resolution failure|package resolution",
            ),
            # 3. Recommends primary workspace context
            (
                has_any(["primary workspace", "from the root", "from root", "workspace root", "run from the monorepo", "repo root"]),
                r"primary workspace|from the root|from root|workspace root|run from the monorepo|repo root",
            ),
            # 4. Provides concrete vitest command from workspace root
            (
                bool(re.search(r"pnpm exec vitest|vitest run|pnpm.*vitest|npx vitest", low)),
                r"pnpm exec vitest|vitest run|pnpm.*vitest|npx vitest",
            ),
            # 5. Adds/suggests .worktrees/ to .gitignore
            (
                has_any([".worktrees/", ".worktrees in", "gitignore"]) and "gitignore" in low,
                r"\.worktrees/|\.worktrees in|gitignore",
            ),
            # 6. Adds/suggests .worktrees/** vitest exclusion
            (
                has_any(["worktrees/**", ".worktrees/**", "exclude.*worktrees", "worktrees.*exclude", "test exclusion", "exclude pattern"]),
                r"worktrees/\*\*|\.worktrees/\*\*|exclude.*worktrees|worktrees.*exclude",
            ),
            # 7. Produces a safety report
            (
                has_any(["worktree safety report", "execution context:", "final verification context", "risk level", "verification context"]),
                r"worktree safety report|execution context:|final verification context|risk level|verification context",
            ),
        ]
    elif eval_id == 2:
        # Eval 2: nested submodule, test discovery crossing worktree boundaries
        checks = [
            # 1. Diagnoses Vitest discovering files inside .worktrees/
            (
                has_any(["test discovery", "crawling", "walking into", "discovering test", "picks up", "sees tests", "finds test"]),
                r"test discovery|crawling|walking into|discovering test|picks up.*worktree|sees tests|finds test",
            ),
            # 2. Provides the Vitest exclusion fix
            (
                has_any(["worktrees/**", ".worktrees/**", "defaultexclude", "exclude array"]) and "vitest" in low,
                r"worktrees/\*\*|\.worktrees/\*\*|defaultExclude|exclude array",
            ),
            # 3. Mentions nested submodule workspace ambiguity
            (
                has_any(["nested submodule", "submodule workspace", "nested workspace", "workspace root ambiguity", "two workspace", "competing workspace", "submodule context", "nested pathing", "submodule.*path", "own .git", "own git"]),
                r"nested submodule|submodule workspace|nested workspace|workspace root ambiguity|two workspace|competing workspace|submodule context|nested pathing|own \.git",
            ),
            # 4. Checks/suggests .gitignore for .worktrees/
            (
                "gitignore" in low and has_any([".worktrees", "worktrees/"]),
                r"gitignore.*worktrees|worktrees.*gitignore|\.worktrees",
            ),
            # 5. Explains why tests from another branch appear
            (
                has_any(["other branch", "another branch", "wrong branch", "different branch", "nested checkout", "other checkout"]),
                r"other branch|another branch|wrong branch|different branch|nested checkout|other checkout",
            ),
            # 6. Produces a summary/report
            (
                has_any(["report", "summary", "fixed", "resolved", "result:", "conclusion"]),
                r"report|summary|fixed|resolved|result:|conclusion",
            ),
        ]
    else:
        # Eval 3: symlink fallback + runtime parity check
        checks = [
            # 1. Provides the ln -s symlink command
            (
                bool(re.search(r"ln -s|symlink.*node_modules|node_modules.*symlink", low)),
                r"ln -s|symlink.*node_modules|node_modules.*symlink",
            ),
            # 2. Runs or provides the runtime parity check
            (
                has_any(["runtime parity", "duplicate react", "parity check", "singleton", "module instance", "react instance", "duplicate instance"]),
                r"runtime parity|duplicate react|parity check|singleton|module instance|react instance|duplicate instance",
            ),
            # 3. Explains what DUPLICATE means / collision
            (
                has_any(["duplicate", "collision", "two instances", "instantiated twice", "module graph"]),
                r"duplicate|collision|two instances|instantiated twice|module graph",
            ),
            # 4. Fallback to primary workspace if collision
            (
                has_any(["switch to primary", "fall back", "fallback", "primary workspace context", "abort", "revert to"]) and has_any(["collision", "duplicate", "detected"]),
                r"switch to primary|fall back|fallback|primary workspace context|abort",
            ),
            # 5. Produces a report documenting the approach and parity result
            (
                has_any(["worktree safety report", "execution context:", "symlink approach", "parity: verified", "parity verified", "symlink fallback", "toolchain risk"]),
                r"worktree safety report|execution context:|symlink approach|parity.*verified|symlink fallback|toolchain risk",
            ),
        ]

    expectations = []
    for i, assertion in enumerate(assertions):
        if i < len(checks):
            passed, pattern = checks[i]
        else:
            passed, pattern = False, ""
        expectations.append(
            {
                "text": assertion,
                "passed": bool(passed),
                "evidence": evidence_snippet(text, pattern) if pattern else "N/A",
            }
        )
    return expectations


def next_iteration_dir() -> Path:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    numbers = []
    for p in WORKSPACE.glob("iteration-*"):
        try:
            numbers.append(int(p.name.split("-")[1]))
        except (IndexError, ValueError):
            pass
    n = (max(numbers) + 1) if numbers else 1
    out = WORKSPACE / f"iteration-{n}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def main() -> None:
    evals = json.loads(EVALS_PATH.read_text(encoding="utf-8"))["evals"]
    iteration = next_iteration_dir()
    print(f"Running Gemini evals into: {iteration}")

    for item in evals:
        eval_id = int(item["id"])
        eval_dir = iteration / f"eval-{eval_id}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(
                {
                    "eval_id": eval_id,
                    "eval_name": f"eval-{eval_id}",
                    "prompt": item["prompt"],
                    "assertions": item.get("assertions", []),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        for config in ["with_skill", "without_skill"]:
            run_dir = eval_dir / config / "run-1"
            output_file = run_dir / "outputs/output.md"
            if output_file.exists():
                print(f"  skip eval-{eval_id} {config}")
                continue

            (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
            prompt = item["prompt"]
            if config == "with_skill":
                prompt = (
                    "Read and apply the skill at skills/monorepo-worktree-safety/SKILL.md before answering. "
                    "Follow its workflow and output style exactly.\n\nTask:\n" + item["prompt"]
                )

            print(f"  run eval-{eval_id} {config} ...", end="", flush=True)
            try:
                payload, raw_stdout, duration_ms, total_tokens = run_gemini(prompt)
            except Exception as exc:
                print(f" ERROR: {exc}")
                continue

            text = payload.get("response", "").strip()
            output_file.write_text(text + "\n", encoding="utf-8")
            (run_dir / "raw_response.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
            (run_dir / "raw_stdout.log").write_text(raw_stdout, encoding="utf-8")

            timing = {
                "total_tokens": total_tokens,
                "duration_ms": duration_ms,
                "total_duration_seconds": round(duration_ms / 1000.0, 1),
            }
            (run_dir / "timing.json").write_text(json.dumps(timing, indent=2), encoding="utf-8")

            expectations = grade(eval_id, item.get("assertions", []), text)
            passed = sum(1 for x in expectations if x["passed"])
            total = len(expectations)
            (run_dir / "grading.json").write_text(
                json.dumps(
                    {
                        "expectations": expectations,
                        "summary": {
                            "passed": passed,
                            "failed": total - passed,
                            "total": total,
                            "pass_rate": round((passed / total) if total else 0.0, 4),
                        },
                        "execution_metrics": {
                            "output_chars": len(text),
                            "total_tool_calls": 0,
                            "errors_encountered": 0,
                        },
                        "timing": timing,
                        "claims": [],
                        "eval_feedback": {
                            "suggestions": [],
                            "overall": "Automated assertion grading via rule-based checks over output text.",
                        },
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f" {passed}/{total} passed ({round(passed/total*100 if total else 0)}%)")

    print("Gemini eval run complete.")


if __name__ == "__main__":
    main()
