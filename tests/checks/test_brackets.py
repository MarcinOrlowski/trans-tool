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
from proptool.prop.items import Comment, Translation
from proptool.decorators.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return Brackets(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.check_single_file(Translation('key', '<({[]})>'))
        self.check_single_file(Translation('key', '<()foo ({a[v]b}d <barr> )> '))

    def test_translation_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.check_single_file(Translation('key', '>'), exp_errors = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Translation('key', '(<>'), exp_errors = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Translation('key', '<(>)'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self):
        self.check_single_file(Comment('# (foo) '))

    def test_comment_with_faults(self):
        # Tests error handling when we have popping bracket and empty stack.
        self.check_single_file(Comment('# foo]"  '), exp_warnings = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Comment('# <fo[o]" '), exp_warnings = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Comment('# [foo <]>" '), exp_warnings = 1)
