"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import random

from proptool.report.report_group import ReportGroup
from proptool.report.report_item import ReportItem
from proptool.report.error import Error
from proptool.report.warn import Warn
from test_case import TestCase


# #################################################################################################

class TestReportGroup(TestCase):

    def setUp(self):
        self.label = self.get_random_string()
        self.rg = ReportGroup(self.label)

    def test_init(self):
        self.assertEqual(self.label, self.rg.label)
        self.assertEqual(0, self.rg.warnings)
        self.assertEqual(0, self.rg.errors)

    def test_add_wrong_item_type(self):
        wrong_item = True
        with self.assertRaises(TypeError):
            self.rg.add(wrong_item)

    def test_add_correct_item_type(self):
        types = [
            ReportItem,
            Error,
            Warn,
        ]
        for single_type in types:
            line = random.randint(1, 100)
            msg = self.get_random_string()
            item = single_type(line, msg)
            self.rg.add(item)

        self.assertEqual(len(types), len(self.rg))

    def test_empty(self):
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

    def test_warn(self):
        line = random.randint(1, 100)
        msg = self.get_random_string()
        self.rg.warn(line, msg)
        self.assertEqual(1, len(self.rg))

        item = self.rg[0]
        self.assertIsInstance(item, Warn)
        self.assertEqual(1, self.rg.warnings)
        self.assertEqual(0, self.rg.errors)

    def test_error(self):
        line = random.randint(1, 100)
        msg = self.get_random_string()
        self.rg.error(line, msg)
        self.assertEqual(1, len(self.rg))

        item = self.rg[0]
        self.assertIsInstance(item, Error)
        self.assertEqual(0, self.rg.warnings)
        self.assertEqual(1, self.rg.errors)
