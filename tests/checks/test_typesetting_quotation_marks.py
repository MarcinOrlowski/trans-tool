"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.checks.base.check import Check
from proptool.checks.typesetting_quotation_marks import TypesettingQuotationMarks
from proptool.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class ChecksBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return TypesettingQuotationMarks(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '‘«„ “»’'))

    def test_translation_with_faults(self) -> None:
        for mark in self.checker.opening + self.checker.closing:
            self.check_single_file(Translation('key', mark), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        self.check_single_file(Comment('# „ foo “ '))

    def test_comment_with_faults(self) -> None:
        # Tests error handling when we have closing (popping) marker and empty stack.
        self.check_single_file(Comment('# foo“  '), exp_warnings = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Comment('# „ «foo» '), exp_warnings = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Comment('# « „ foo» “ '), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_single_file(Blank())

    # #################################################################################################

    def test_opening_and_closing_lists(self) -> None:
        """
        Checks if lists defining opening and closing markers are sane.
        """
        checker: TypesettingQuotationMarks = self.get_checker(self.config)

        self.assertEqual(len(checker.opening), len(checker.closing))
        self.assertNotEqual([], checker.opening)
        self.assertNotEqual([], checker.closing)
        self.assertNotEqual(checker.opening, checker.closing)

        # ensure no marker is in both lists
        for pos, marker in enumerate(checker.opening):
            self.assertFalse(marker in checker.closing, f'Marker {marker} (position: {pos}) is present in closing too.')
        for pos, marker in enumerate(checker.closing):
            self.assertFalse(marker in checker.opening, f'Marker {marker} (position: {pos}) is present in opening too.')