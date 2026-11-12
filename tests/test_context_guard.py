"""Offline unit tests; no user profile or agent settings are modified."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "context_guard", ROOT / "hooks" / "context-guard" / "context_guard.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class ContextGuardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name) / "project"
        self.cwd.mkdir()
        self.env = patch.dict(os.environ, {
            "AGENT_KIT_HOME": str(Path(self.temp.name) / "private-state"),
            "CONTEXT_GUARD_WARNING": "350000",
            "CONTEXT_GUARD_HANDOFF": "400000",
        })
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_threshold_edges(self):
        self.assertEqual(guard.level_for(349999), "normal")
        self.assertEqual(guard.level_for(350000), "warning")
        self.assertEqual(guard.level_for(400000), "handoff")

    def test_shorter_model_window(self):
        self.assertEqual(guard.limits(200000), (150000, 180000))
        self.assertEqual(guard.level_for(180000, 200000), "handoff")

    def test_last_assistant_usage_not_session_sum(self):
        path = self.cwd / "sample.jsonl"
        lines = [
            {"type": "assistant", "message": {"usage": {"input_tokens": 900000}}},
            {"type": "user", "message": {"content": "not counted"}},
            {"type": "assistant", "message": {"usage": {
                "input_tokens": 100, "cache_read_input_tokens": 250,
                "cache_creation_input_tokens": 30}}},
        ]
        path.write_text("\n".join(json.dumps(x) for x in lines), encoding="utf-8")
        self.assertEqual(guard.claude_usage_from_transcript(str(path)), 380)

    def test_codex_cached_input_not_double_counted(self):
        payload = {"token_usage": {"input_tokens": 401000, "cached_input_tokens": 390000}}
        self.assertEqual(guard.read_tokens(payload, "codex"), (401000, "codex-post-model-input"))

    def test_gemini_estimate_explicitly_labeled(self):
        payload = {"llm_response": {"usageMetadata": {"totalTokenCount": 399999}}}
        self.assertEqual(guard.read_tokens(payload, "gemini"), (399999, "gemini-total-estimate"))

    def test_warning_generates_one_checkpoint_without_transcript_copy(self):
        payload = {"session_id": "safe-test", "cwd": str(self.cwd),
                   "hook_event_name": "UserPromptSubmit",
                   "usage": {"input_tokens": 351000}}
        result = guard.handle(payload, "claude")
        self.assertIn("additionalContext", result["hookSpecificOutput"])
        state, file = guard.last_state(self.cwd)
        self.assertEqual(state["level"], "warning")
        checkpoint = Path(state["checkpoint"])
        self.assertTrue(checkpoint.exists())
        initial = checkpoint.read_text(encoding="utf-8")
        self.assertIn("Next exact action", initial)
        self.assertNotIn("safe-test", str(checkpoint))
        self.assertEqual(guard.handle(payload, "claude"), {})
        self.assertEqual(initial, checkpoint.read_text(encoding="utf-8"))

    def test_handoff_preserves_user_checkpoint_edits(self):
        payload = {"session_id": "s1", "cwd": str(self.cwd),
                   "hook_event_name": "UserPromptSubmit",
                   "usage": {"input_tokens": 350000}}
        guard.handle(payload, "claude")
        state, _ = guard.last_state(self.cwd)
        file = Path(state["checkpoint"])
        file.write_text(file.read_text(encoding="utf-8") + "\nCustom decision kept\n",
                        encoding="utf-8")
        payload["usage"]["input_tokens"] = 400000
        result = guard.handle(payload, "claude")
        self.assertIn("HANDOFF", result["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Custom decision kept", file.read_text(encoding="utf-8"))

    def test_missing_usage_no_fake_checkpoint(self):
        payload = {"session_id": "unknown", "cwd": str(self.cwd),
                   "hook_event_name": "Stop"}
        self.assertEqual(guard.handle(payload, "codex"), {})
        state, path = guard.last_state(self.cwd)
        self.assertIsNone(path)

    def test_no_credentials_or_raw_prompt_in_state(self):
        payload = {"session_id": "test", "cwd": str(self.cwd),
                   "hook_event_name": "BeforeAgent", "prompt": "my secret text",
                   "llm_response": {"usageMetadata": {"promptTokenCount": 355000}}}
        guard.handle(payload, "gemini")
        state, file = guard.last_state(self.cwd)
        self.assertNotIn("my secret text", file.read_text(encoding="utf-8"))
        self.assertEqual(state["token_source"], "gemini-prompt")


if __name__ == "__main__":
    unittest.main()
