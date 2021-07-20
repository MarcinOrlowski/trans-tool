"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from fake_config import FakeConfig
from proptool.checks.quotation_marks import QuotationMarks
from proptool.entries import PropComment, PropEntry, PropTranslation
from proptool.propfile import PropFile
from test_case import TestCase


# #################################################################################################

class TestQuotationMarks(TestCase):

    def setUp(self):
        self.config = FakeConfig()
        self.checker = QuotationMarks(self.config)

    def do_single_test(self, entry: PropEntry, expected_errors: int = 0, expected_warnings: int = 0):
        prop_file = PropFile(self.config)
        prop_file.loaded = True
        prop_file.append(entry)

        report = self.checker.check(None, prop_file)
        self.assertEqual(expected_errors, report.errors)
        self.assertEqual(expected_warnings, report.warnings)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.do_single_test(PropTranslation('key', '""'))

    def test_translation_with_faults(self):
        self.do_single_test(PropTranslation('key', '"""'), expected_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self):
        self.do_single_test(PropComment('#  "foo" '))

    def test_comment_with_faults(self):
        self.do_single_test(PropComment('# "foo `"  '), expected_warnings = 1)
