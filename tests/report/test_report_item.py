"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.report.item import ReportItem
from test_case import TestCase


class TestReportItem(TestCase):

    def test_to_string_with_position(self):
        position = self.get_random_string(count = 5)
        msg = self.get_random_string()

        expected = f'Line {position}: {msg}'
        ri = ReportItem(position, msg)
        self.assertEqual(expected, ri.to_string())

    def test_to_string_without_position(self):
        msg = self.get_random_string()

        ri = ReportItem(None, msg)
        self.assertEqual(msg, ri.to_string())

    def test_to_string_with_trans_key(self):
        trans_key = self.get_random_string()
        msg = self.get_random_string()

        expected = f'"{trans_key}": {msg}'

        ri = ReportItem(None, msg, trans_key)
        self.assertEqual(expected, ri.to_string())

    def test_to_string_with_trans_key_and_position(self):
        trans_key = self.get_random_string()
        position = self.get_random_string(count = 5)
        msg = self.get_random_string()

        expected = f'Line {position}: "{trans_key}": {msg}'

        ri = ReportItem(position, msg, trans_key)
        self.assertEqual(expected, ri.to_string())
