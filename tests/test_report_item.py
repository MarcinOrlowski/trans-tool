"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import random

from proptool.report.report_item import ReportItem
from test_case import TestCase


class TestReportItem(TestCase):

    def test_to_string_with_line_number(self):
        line = random.randint(1, 100)
        msg = self.get_random_string()

        expected = f'Line {line}: {msg}'
        ri = ReportItem(line, msg)
        self.assertEqual(expected, ri.to_string())

    def test_to_string_without_line_number(self):
        msg = self.get_random_string()

        ri = ReportItem(None, msg)
        self.assertEqual(msg, ri.to_string())
