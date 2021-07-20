"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import random

from proptool.config import Config
from proptool.report.report import Report
from proptool.report.report_group import ReportGroup
from proptool.report.error import Error
from proptool.report.warn import Warn
from test_case import TestCase


# #################################################################################################

class TestReport(TestCase):

    def setUp(self):
        self.config = Config()
        self.r = Report(self.config)

    def test_init(self):
        self.assertEqual(0, self.r.warnings)
        self.assertEqual(0, self.r.errors)

    def test_empty(self):
        self.assertTrue(self.r.empty())
