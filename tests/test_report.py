"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.config import Config
from proptool.report.report import Report
from test_case import TestCase


# #################################################################################################

class TestReport(TestCase):

    def setUp(self):
        self.config = Config()
        self.report = Report(self.config)

    def test_init(self):
        self.assertEqual(0, self.report.warnings)
        self.assertEqual(0, self.report.errors)

    def test_empty(self):
        self.assertTrue(self.report.empty())
