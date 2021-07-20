"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from fake_config import FakeConfig
from proptool.checks.brackets import Brackets
from proptool.entries import PropComment, PropEntry, PropTranslation
from proptool.propfile import PropFile
from test_case import TestCase


# #################################################################################################

class TestBrackets(TestCase):

    def setUp(self):
        self.config = FakeConfig()
        self.checker = Brackets(self.config)

    def do_single_test(self, entry: PropEntry, expected_errors: int = 0, expected_warnings: int = 0):
        prop_file = PropFile(self.config)
        prop_file.loaded = True
        prop_file.append(entry)

        report = self.checker.check(None, prop_file)
        self.assertEqual(expected_errors, report.errors)
        self.assertEqual(expected_warnings, report.warnings)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.do_single_test(PropTranslation('key', '<({[]})>'))
        self.do_single_test(PropTranslation('key', '<()foo ({a[v]b}d <barr> )> '))

    def test_translation_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.do_single_test(PropTranslation('key', '>'), expected_errors = 1)
        # Tests the case where we done with checks and something left on stack.
        self.do_single_test(PropTranslation('key', '(<>'), expected_errors = 1)
        # Text the case where we have matches, but not in order.
        self.do_single_test(PropTranslation('key', '<(>)'), expected_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self):
        self.do_single_test(PropComment('# (foo) '))

    def test_comment_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.do_single_test(PropComment('# foo]"  '), expected_warnings = 1)
        # Tests the case where we done with checks and something left on stack.
        self.do_single_test(PropComment('# <fo[o]" '), expected_warnings = 1)
        # Text the case where we have matches, but not in order.
        self.do_single_test(PropComment('# [foo <]>" '), expected_warnings = 1)
