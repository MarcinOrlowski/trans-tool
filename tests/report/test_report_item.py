"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from transtool.report.items import ReportItem
from tests.test_case import TestCase


class TestReportItem(TestCase):

    def test_to_string_with_position(self) -> None:
        position = self.get_random_string(length = 5)
        msg = self.get_random_string()

        expected = f'Line {position}: {msg}'
        ri = ReportItem(position, msg)
        self.assertEqual(expected, ri.to_string())

    def test_to_string_without_position(self) -> None:
        msg = self.get_random_string()

        ri = ReportItem(None, msg)
        self.assertEqual(msg, ri.to_string())

    def test_to_string_with_trans_key(self) -> None:
        trans_key = self.get_random_string()
        msg = self.get_random_string()

        expected = f'"{trans_key}": {msg}'

        ri = ReportItem(None, msg, trans_key)
        self.assertEqual(expected, ri.to_string())

    def test_to_string_with_trans_key_and_position(self) -> None:
        trans_key = self.get_random_string()
        position = self.get_random_string(length = 5)
        msg = self.get_random_string()

        expected = f'Line {position}: "{trans_key}": {msg}'

        ri = ReportItem(position, msg, trans_key)
        self.assertEqual(expected, ri.to_string())
