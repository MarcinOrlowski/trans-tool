"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random

from transtool.config.config import Config

from transtool.report.report import Report

from transtool.report.group import ReportGroup
from transtool.report.items import Error, Warn
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

    def test_add_with_list(self) -> None:
        """
        Ensures add() deals with all the cases properly.
        :return:
        """

        reports = [
            Warn(None, msg = self.get_random_string()),
            Error(None, msg = self.get_random_string()),
        ]
        nones = [
            None,
            None,
        ]

        rg = ReportGroup(self.get_random_string('label'))
        rg.add(reports + nones)
        # None's should be silently skipped
        self.assertEqual(len(reports), rg.errors + rg.warnings)

    def test_empty_not_empty(self) -> None:
        config = Config()
        report = Report(config)

        self.assertTrue(report.empty())
        self.assertFalse(report.not_empty())

        rg = ReportGroup(self.get_random_string('report_group'))
        rg.warn(line = None, msg = self.get_random_string('warn'))

        report.add(rg)

        self.assertFalse(report.empty())
        self.assertTrue(report.not_empty())

    def test_fatal_is_ok(self) -> None:
        config = Config()
        report = Report(config)

        self.assertTrue(report.is_ok())
        self.assertFalse(report.is_fatal())

        rg = ReportGroup(self.get_random_string('group'))
        report.add(rg, skip_empty = False)

        rg.warn(line = None, msg = self.get_random_string('warn'))
        self.assertTrue(report.is_ok())
        self.assertFalse(report.is_fatal())

        rg.error(line = None, msg = self.get_random_string('error'))
        self.assertFalse(report.is_ok())
        self.assertTrue(report.is_fatal())
