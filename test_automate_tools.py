import unittest
from unittest.mock import patch

from automate.models import ToolResult
from automate.registry import get_tool, list_tools
from automate.runner import run_tool


class ToolRegistryTests(unittest.TestCase):
    def test_all_registered_tools_are_read_only(self):
        tools = list_tools()
        self.assertGreaterEqual(len(tools), 4)
        self.assertTrue(all(not tool.side_effects for tool in tools))
        self.assertTrue(all(not tool.requires_approval for tool in tools))

    def test_unknown_tool_has_actionable_error(self):
        with self.assertRaisesRegex(KeyError, "Available tools"):
            get_tool("does_not_exist")

    @patch("automate.runner.subprocess.run")
    def test_runner_returns_structured_success(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = "hello"
        run.return_value.stderr = ""
        result = run_tool("arxiv_recent")
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.data["output"], "hello")
        self.assertTrue(result.run_id)


if __name__ == "__main__":
    unittest.main()
