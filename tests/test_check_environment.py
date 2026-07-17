"""Tests for the lightweight environment report."""

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "check_environment.py"
)
SPEC = importlib.util.spec_from_file_location("check_environment", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
CHECK_ENVIRONMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_ENVIRONMENT)


class EnvironmentReportTest(unittest.TestCase):
    def test_report_contains_expected_sections(self) -> None:
        report = CHECK_ENVIRONMENT.build_report()

        self.assertIn("platform", report)
        self.assertIn("python", report)
        self.assertIn("storage", report)
        self.assertIn("torch", report)
        self.assertIn("nvidia_smi_available", report)

    def test_report_does_not_include_identity_fields(self) -> None:
        report_text = str(CHECK_ENVIRONMENT.build_report()).lower()

        self.assertNotIn("hostname", report_text)
        self.assertNotIn("username", report_text)
        self.assertNotIn("token", report_text)


if __name__ == "__main__":
    unittest.main()
