# Skill Creator

A skill for creating new AI agent skills and iteratively improving them.

## Quick Start

```bash
# Clone the skill-creator to your skills directory
cp -r skill-creator/ ~/.agents/skills/

# Use the skill via Claude/OpenCode
/skill-creator "create a skill for X"
```

## Provider Support

The skill supports multiple LLM providers for running evals:

| Provider   | CLI Command     | Notes                           |
|------------|-----------------|---------------------------------|
| `opencode` | `opencode -p`   | **Default** - Most cost-effective |
| `claude`   | `claude -p`     | Anthropic's CLI                 |
| `codex`    | `codex -p`      | OpenAI's CLI                    |
| `gemini`   | `gemini -p`      | Google's CLI                    |

### Syntax

```
/skill-creator opencode "create a skill for X"
/skill-creator claude "create a skill for X"
```

If the specified provider is unavailable, the skill automatically falls back to the next available provider in this order: `opencode` → `claude` → `codex` → `gemini`.

### Command Line Usage

```bash
# Run eval with specific provider
python3 -m scripts.run_eval \
  --eval-set evals/test.json \
  --skill-path /path/to/skill \
  --provider opencode \
  --verbose

# Run eval + improve loop
python3 -m scripts.run_loop \
  --eval-set evals/test.json \
  --skill-path /path/to/skill \
  --provider claude \
  --model gpt-4 \
  --max-iterations 5

# Improve description only
python3 -m scripts.improve_description \
  --eval-results results.json \
  --skill-path /path/to/skill \
  --provider opencode \
  --model gpt-4
```

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `run_eval.py` | Test if skill triggers for a set of queries |
| `run_loop.py` | Run eval + improve loop (full optimization) |
| `improve_description.py` | Generate improved description from eval results |
| `aggregate_benchmark.py` | Aggregate results into benchmark report |
| `generate_report.py` | Generate HTML report |
| `package_skill.py` | Package skill into `.skill` file |

## Files

- `SKILL.md` - Main skill definition
- `agents/` - Subagent instructions (grader, comparator, analyzer)
- `scripts/` - Evaluation and improvement scripts
- `eval-viewer/` - HTML viewer for reviewing eval results
- `references/` - Schemas and documentation
- `assets/` - Templates (e.g., `eval_review.html`)
