import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import run_eval


class RunEvalOpencodeTests(unittest.TestCase):
    def test_build_command_uses_opencode_run_json_shape(self):
        self.assertEqual(
            run_eval.build_command("opencode", "audit this skill", None),
            ["opencode", "run", "--format", "json", "audit this skill"],
        )

    def test_opencode_temp_skill_path_is_provider_specific(self):
        project_root = Path("/tmp/project-root")
        clean_name = "google-seo-geo-skill-abcd1234"

        self.assertEqual(
            run_eval.get_skill_path("opencode", project_root, clean_name),
            project_root / ".opencode" / "skills" / clean_name / "SKILL.md",
        )
        self.assertEqual(
            run_eval.get_skill_path("claude", project_root, clean_name),
            project_root / ".claude" / "commands" / f"{clean_name}.md",
        )

    def test_parse_opencode_event_detects_tool_use_skill_trigger(self):
        clean_name = "google-seo-geo-skill-abcd1234"
        event = {
            "type": "tool_use",
            "part": {
                "tool": "skill",
                "state": {"input": {"name": clean_name}},
            },
        }

        self.assertTrue(run_eval._parse_opencode_output(event, clean_name))

    def test_parse_opencode_event_rejects_same_prefix_other_skill(self):
        clean_name = "google-seo-geo-skill-abcd1234"
        event = {
            "type": "tool_use",
            "part": {
                "tool": "skill",
                "state": {"input": {"name": "google-seo-geo-trigger-test"}},
            },
        }

        self.assertIsNone(run_eval._parse_opencode_output(event, clean_name))

    def test_parse_opencode_nonmatching_step_does_not_stop_scan(self):
        clean_name = "google-seo-geo-skill-abcd1234"
        event = {
            "type": "step_finish",
            "part": {"reason": "tool-calls"},
        }

        self.assertIsNone(run_eval._parse_opencode_output(event, clean_name))

    def test_parse_opencode_text_echo_does_not_count_as_trigger(self):
        clean_name = "google-seo-geo-skill-abcd1234"
        event = {
            "type": "text",
            "part": {"text": f"I saw {clean_name} in a log line"},
        }

        self.assertIsNone(run_eval._parse_opencode_output(event, clean_name))


if __name__ == "__main__":
    unittest.main()
