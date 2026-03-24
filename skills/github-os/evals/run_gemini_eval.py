#!/usr/bin/env python3
"""Run github-os evals with Gemini CLI in with-skill/without-skill mode.

Usage:
  python3 skills/github-os/evals/run_gemini_eval.py

Notes:
  - Resumable: existing run outputs are skipped.
  - Creates/uses workspace: skills/github-os-workspace/iteration-N
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
EVALS_PATH = ROOT / "skills/github-os/evals/evals.json"
WORKSPACE = ROOT / "skills/github-os-workspace"
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


def run_gemini(prompt: str, timeout_sec: int = 240) -> tuple[dict, str, int, int]:
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

    if eval_id == 1:
        checks = [
            (("monorepo" in low) and has_all(["web", "admin", "api", "ui", "utils"]), r"monorepo|web|admin|api|packages/ui|packages/utils"),
            (has_all(["module:web", "module:admin", "module:api", "module:ui", "module:utils"]), r"module:web|module:admin|module:api|module:ui|module:utils"),
            (has_all(["type:feature", "type:bug", "type:chore", "type:research"]), r"type:feature|type:bug|type:chore|type:research"),
            (has_all(["priority:p0", "priority:p1", "priority:p2", "priority:p3"]), r"priority:p0|priority:p1|priority:p2|priority:p3"),
            ((has_all(["task", "bug", "feature"]) and ("template" in low or "yaml" in low or "yml" in low)), r"issue template|task|bug|feature|\.ya?ml"),
            ((("pr template" in low or "pull request template" in low) and has_all(["closes #", "what changed", "context", "testing"])), r"pr template|closes #|what changed|context|testing"),
            (".github-os.json" in low, r"\.github-os\.json"),
            (("approval" in low and ("before execution" in low or "before executing" in low or "present design" in low)), r"approval|before execut|present design"),
        ]
    elif eval_id == 2:
        module_labels = set(re.findall(r"\bmodule:[a-z0-9_-]+\b", low))
        checks = [
            ((("single repo" in low or "single repository" in low) and ("not monorepo" in low or "monorepo" not in low)), r"single repo|single repository|not monorepo"),
            ((("minimal" in low and "readme" in low) or "readme only" in low), r"minimal|readme"),
            (has_all(["type:feature", "type:bug", "type:chore", "type:research", "priority:p0", "priority:p1", "priority:p2", "priority:p3"]), r"type:feature|priority:p0"),
            (("docs/" in low or "docs directory" in low or "create docs" in low), r"docs/|docs directory|create docs"),
            (has_all(["repository analysis", "modules detected", "documentation structure", "execution surfaces"]), r"repository analysis|modules detected|documentation structure|execution surfaces"),
            (len(module_labels) <= 1, r"module:[a-z0-9_-]+"),
        ]
    else:
        title = ""
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("#"):
                title = re.sub(r"^#+\s*", "", s)
                break
        if not title:
            m = re.search(r"(?im)^title\s*:\s*(.+)$", text)
            title = m.group(1).strip() if m else ""
        checks = [
            ((bool(title) and len(title) < 72 and "add payments" not in title.lower()), r"^#|^title:"),
            (("context" in low and ("docs/" in low or "src/" in low or "http" in low)), r"context|docs/|src/|https?://"),
            (("in scope" in low and "out of scope" in low), r"in scope|out of scope"),
            (bool(re.search(r"(?m)^\s*[-*]\s*\[\s*\]", text)), r"^\s*[-*]\s*\[\s*\]"),
            (("out of scope" in low and "paypal" in low), r"out of scope|paypal"),
            ((has_all(["src/payments/", "src/api/stripe.ts"]) and "checkout" in low), r"src/payments/|src/api/stripe\.ts|checkout"),
            ((("status:llm-ready" in low) or ("llm-ready" in low and "label" in low)), r"status:llm-ready|llm-ready"),
        ]

    expectations = []
    for i, assertion in enumerate(assertions):
        passed, pattern = checks[i]
        expectations.append(
            {
                "text": assertion,
                "passed": bool(passed),
                "evidence": evidence_snippet(text, pattern),
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
                print(f"skip eval-{eval_id} {config}")
                continue

            (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
            prompt = item["prompt"]
            if config == "with_skill":
                prompt = (
                    "Read and apply the skill at skills/github-os/SKILL.md before answering. "
                    "Follow its workflow and output style.\n\nTask:\n" + item["prompt"]
                )

            print(f"run eval-{eval_id} {config}")
            payload, raw_stdout, duration_ms, total_tokens = run_gemini(prompt)
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

    print("Gemini eval run complete")


if __name__ == "__main__":
    main()
