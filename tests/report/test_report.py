"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from transtool.config.config import Config
from transtool.report.report import Report
from tests.test_case import TestCase


class TestReport(TestCase):

    def setUp(self) -> None:
        self.config = Config()
        self.report = Report(self.config)

    def test_init(self) -> None:
        self.assertEqual(0, self.report.warnings)
        self.assertEqual(0, self.report.errors)

    def test_empty(self) -> None:
        self.assertTrue(self.report.empty())
