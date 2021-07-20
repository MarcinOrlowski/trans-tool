"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from checks.checks_test_case import ChecksTestCase
from proptool.checks.base.check import Check
from proptool.checks.brackets import Brackets
from proptool.config import Config
from proptool.entries import PropComment, PropTranslation
from proptool.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return Brackets(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.do_single_test(PropTranslation('key', '<({[]})>'))
        self.do_single_test(PropTranslation('key', '<()foo ({a[v]b}d <barr> )> '))

    def test_translation_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.do_single_test(PropTranslation('key', '>'), exp_errors = 1)
        # Tests the case where we done with checks and something left on stack.
        self.do_single_test(PropTranslation('key', '(<>'), exp_errors = 1)
        # Text the case where we have matches, but not in order.
        self.do_single_test(PropTranslation('key', '<(>)'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self):
        self.do_single_test(PropComment('# (foo) '))

    def test_comment_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.do_single_test(PropComment('# foo]"  '), exp_warnings = 1)
        # Tests the case where we done with checks and something left on stack.
        self.do_single_test(PropComment('# <fo[o]" '), exp_warnings = 1)
        # Text the case where we have matches, but not in order.
        self.do_single_test(PropComment('# [foo <]>" '), exp_warnings = 1)
