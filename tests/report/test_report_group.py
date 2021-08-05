"""
# trans-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random

from proptool.report.group import ReportGroup
from proptool.report.items import Error, Warn
from tests.test_case import TestCase


class TestReportGroup(TestCase):

    def setUp(self) -> None:
        self.label = self.get_random_string()
        self.rg = ReportGroup(self.label)

    def test_init(self) -> None:
        self.assertEqual(self.label, self.rg.label)
        self.assertEqual(0, self.rg.warnings)
        self.assertEqual(0, self.rg.errors)

    def test_empty(self) -> None:
        self.rg.errors = random.randint(1, 100)
        self.rg.warnings = 0
        self.assertFalse(self.rg.empty())

        self.rg.errors = 0
        self.rg.warnings = random.randint(1, 100)
        self.assertFalse(self.rg.empty())

        self.rg.errors = random.randint(1, 100)
        self.rg.warnings = random.randint(1, 100)
        self.assertFalse(self.rg.empty())

        self.rg.errors = 0
        self.rg.warnings = 0
        self.assertTrue(self.rg.empty())

    def test_warn(self) -> None:
        line = random.randint(1, 100)
        msg = self.get_random_string()
        self.rg.warn(line, msg)
        self.assertEqual(1, len(self.rg))

        item = self.rg[0]
        self.assertIsInstance(item, Warn)
        self.assertEqual(1, self.rg.warnings)
        self.assertEqual(0, self.rg.errors)

    def test_error(self) -> None:
        line = random.randint(1, 100)
        msg = self.get_random_string()
        self.rg.error(line, msg)
        self.assertEqual(1, len(self.rg))

        item = self.rg[0]
        self.assertIsInstance(item, Error)
        self.assertEqual(0, self.rg.warnings)
        self.assertEqual(1, self.rg.errors)
