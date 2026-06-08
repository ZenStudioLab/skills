#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes a provider to trigger (read the skill)
for a set of queries. Outputs results as JSON.
Supports multiple providers: opencode (default), claude, codex, gemini.
"""

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md

PROVIDERS = ["opencode", "claude", "codex", "gemini"]

DEFAULT_PROVIDER = "opencode"
FALLBACK_PROVIDERS = ["claude", "codex", "gemini"]


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/.

    Mimics how Claude Code discovers its project root, so the command file
    we create ends up where the provider CLI will look for it.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def get_skill_path(provider: str, project_root: str | Path, clean_name: str) -> Path:
    """Return the provider-specific temp skill file path."""
    base = Path(project_root)
    if provider == "opencode":
        return base / ".opencode" / "skills" / clean_name / "SKILL.md"
    return base / ".claude" / "commands" / f"{clean_name}.md"


def get_skill_storage_root(provider: str, project_root: str | Path) -> Path:
    """Return the provider-specific directory that owns temp skill artifacts."""
    base = Path(project_root)
    if provider == "opencode":
        return base / ".opencode" / "skills"
    return base / ".claude" / "commands"


def _build_opencode_env(env: dict, project_root: str | Path) -> dict:
    """Inject opencode config so project skills are discoverable."""
    new_env = env.copy()
    skills_path = str(Path(project_root) / ".opencode" / "skills")
    config_content = {"skills": {"paths": [skills_path]}}
    existing = new_env.get("OPENCODE_CONFIG_CONTENT")
    if existing:
        try:
            merged = json.loads(existing)
        except json.JSONDecodeError:
            merged = {}
        merged_skills = merged.get("skills", {}) if isinstance(merged, dict) else {}
        paths = merged_skills.get("paths", []) if isinstance(merged_skills, dict) else []
        if skills_path not in paths:
            paths.append(skills_path)
        config_content["skills"]["paths"] = paths
        for key, value in merged.items():
            if key != "skills":
                config_content[key] = value
    new_env["OPENCODE_CONFIG_CONTENT"] = json.dumps(config_content)
    return new_env


def get_available_providers() -> list[str]:
    """Check which provider CLIs are available."""
    available = []
    for provider in PROVIDERS:
        if shutil.which(provider):
            available.append(provider)
    return available


def build_command(provider: str, query: str, model: str | None = None) -> list[str]:
    """Build the CLI command for the given provider."""
    if provider == "opencode":
        cmd = ["opencode", "run", "--format", "json"]
    elif provider == "claude":
        cmd = [
            "claude",
            "-p",
            query,
            "--output-format",
            "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
    elif provider == "codex":
        cmd = ["codex", "-p", query, "--output-format", "stream-json"]
    elif provider == "gemini":
        cmd = ["gemini", "-p", query, "--output-format", "stream-json"]
    else:
        raise ValueError(f"Unknown provider: {provider}")

    if model:
        cmd.extend(["--model", model])
    if provider == "opencode":
        cmd.append(query)
    return cmd


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    provider: str = DEFAULT_PROVIDER,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a provider-specific temporary skill file so it appears in the
    provider's available_skills list, then runs the provider's CLI with the raw
    query. If the primary provider fails, tries fallback providers.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    skill_file = get_skill_path(provider, project_root, clean_name)
    storage_root = get_skill_storage_root(provider, project_root)

    try:
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        indented_desc = "\n  ".join(skill_description.split("\n"))
        if provider == "opencode":
            skill_content = (
                f"---\n"
                f"name: {clean_name}\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"# {skill_name}\n\n"
                f"This skill handles: {skill_description}\n"
            )
        else:
            skill_content = (
                f"---\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"# {skill_name}\n\n"
                f"This skill handles: {skill_description}\n"
            )
        skill_file.write_text(skill_content)

        providers_to_try = [provider] if provider == "opencode" else [provider] + FALLBACK_PROVIDERS
        last_error = None

        for p in providers_to_try:
            if p not in get_available_providers():
                continue
            try:
                cmd = build_command(p, query, model)
                env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
                if p == "opencode":
                    env = _build_opencode_env(env, project_root)
                return _execute_and_parse(
                    cmd, project_root, env, clean_name, timeout, p
                )
            except Exception as e:
                last_error = e
                continue

        print(
            f"Warning: All providers failed. Last error: {last_error}", file=sys.stderr
        )
        return False
    finally:
        if skill_file.exists():
            skill_file.unlink()
        for parent in skill_file.parents:
            if parent == storage_root:
                break
            try:
                parent.rmdir()
            except OSError:
                break


def _execute_and_parse(
    cmd: list[str],
    project_root: str,
    env: dict,
    clean_name: str,
    timeout: int,
    provider: str,
) -> bool:
    """Execute a command and parse the output for skill triggering."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=project_root,
        env=env,
    )

    triggered = False
    start_time = time.time()
    buffer = ""
    pending_tool_name = None
    accumulated_json = ""

    try:
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                remaining = process.stdout.read()
                if remaining:
                    buffer += remaining.decode("utf-8", errors="replace")
                break

            ready, _, _ = select.select([process.stdout], [], [], 1.0)
            if not ready:
                continue

            chunk = os.read(process.stdout.fileno(), 8192)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                parser_result = _parse_provider_event(
                    provider,
                    event,
                    clean_name,
                    pending_tool_name,
                    accumulated_json,
                )
                if parser_result is not None:
                    return parser_result

        if buffer.strip():
            for line in buffer.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                parser_result = _parse_provider_event(
                    provider,
                    event,
                    clean_name,
                    pending_tool_name,
                    accumulated_json,
                )
                if parser_result is not None:
                    return parser_result

    finally:
        if process.poll() is None:
            process.kill()
            process.wait()

    return triggered


def _parse_claude_output(event, clean_name, pending_tool_name, accumulated_json):
    """Parse Claude-specific streaming output."""
    if event.get("type") == "stream_event":
        se = event.get("event", {})
        se_type = se.get("type", "")

        if se_type == "content_block_start":
            cb = se.get("content_block", {})
            if cb.get("type") == "tool_use":
                tool_name = cb.get("name", "")
                if tool_name in ("Skill", "Read"):
                    pending_tool_name = tool_name
                    accumulated_json = ""
                else:
                    return False

        elif se_type == "content_block_delta" and pending_tool_name:
            delta = se.get("delta", {})
            if delta.get("type") == "input_json_delta":
                accumulated_json += delta.get("partial_json", "")
                if clean_name in accumulated_json:
                    return True

        elif se_type in ("content_block_stop", "message_stop"):
            if pending_tool_name:
                return clean_name in accumulated_json
            if se_type == "message_stop":
                return False

    elif event.get("type") == "assistant":
        message = event.get("message", {})
        for content_item in message.get("content", []):
            if content_item.get("type") != "tool_use":
                continue
            tool_name = content_item.get("name", "")
            tool_input = content_item.get("input", {})
            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                return True
            elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                return True
        return True

    elif event.get("type") == "result":
        return False

    return None


def _parse_provider_event(
    provider, event, clean_name, pending_tool_name, accumulated_json
):
    if provider == "claude":
        return _parse_claude_output(
            event, clean_name, pending_tool_name, accumulated_json
        )
    if provider == "opencode":
        return _parse_opencode_output(event, clean_name)
    return _parse_generic_output(event, clean_name)


def _parse_opencode_output(event, clean_name):
    """Parse OpenCode streaming output for skill-trigger evidence."""
    if event.get("type") == "tool_use":
        part = event.get("part", {})
        if part.get("tool") == "skill":
            skill_input = part.get("state", {}).get("input", {})
            loaded_name = str(skill_input.get("name", ""))
            if loaded_name == clean_name:
                return True

    if event.get("type") == "result":
        return False

    if event.get("type") not in (
        "step_start",
        "text",
        "step_finish",
        "item_start",
        "item_started",
        "item_completed",
    ):
        return None

    if _event_contains_text(event, clean_name):
        return True

    return None


def _event_contains_text(value, needle):
    if isinstance(value, dict):
        return any(_event_contains_text(child, needle) for child in value.values())
    if isinstance(value, list):
        return any(_event_contains_text(child, needle) for child in value)
    return needle in str(value)


def _parse_generic_output(event, clean_name):
    """Parse generic streaming output for non-Claude providers."""
    if event.get("type") == "assistant":
        message = event.get("message", {})
        for content_item in message.get("content", []):
            if content_item.get("type") != "tool_use":
                continue
            tool_name = content_item.get("name", "")
            tool_input = content_item.get("input", {})
            if tool_name == "Skill" and clean_name in str(tool_input.get("skill", "")):
                return True
            elif tool_name == "Read" and clean_name in str(
                tool_input.get("file_path", "")
            ):
                return True
        return True

    elif event.get("type") == "result":
        return False

    return None


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    provider: str = DEFAULT_PROVIDER,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                    provider,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation for a skill description"
    )
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description", default=None, help="Override description to test"
    )
    parser.add_argument(
        "--num-workers", type=int, default=10, help="Number of parallel workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=30, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--runs-per-query", type=int, default=3, help="Number of runs per query"
    )
    parser.add_argument(
        "--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model to use for the provider CLI (default: provider's configured model)",
    )
    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=PROVIDERS,
        help=f"Provider CLI to use (default: {DEFAULT_PROVIDER}). "
        f"Will fall back to other available providers on failure.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress to stderr"
    )
    args = parser.parse_args()

    available = get_available_providers()
    if args.verbose and args.provider not in available:
        print(
            f"Warning: {args.provider} not found, will try fallbacks", file=sys.stderr
        )
        print(f"Available providers: {available}", file=sys.stderr)

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        provider=args.provider,
    )

    if args.verbose:
        summary = output["summary"]
        print(
            f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr
        )
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
