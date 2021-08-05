"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from typing import Dict, Union

from transtool.checks.brackets import Brackets
from transtool.checks.typesetting_quotation_marks import TypesettingQuotationMarks
from transtool.decorators.overrides import overrides
from transtool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class ChecksBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> TypesettingQuotationMarks:
        return TypesettingQuotationMarks(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '‘«„ “»’'))

    def test_translation_with_faults(self) -> None:
        for mark in self.checker.opening + self.checker.closing:
            self.check_single_file(Translation('key', mark), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        tests = [
            Comment('# „ foo “ '),
        ]
        self._do_checker_comment_test(tests, 0)

    def test_comment_with_faults(self) -> None:
        faults = [
            # Tests error handling when we have closing (popping) marker and empty stack.
            Comment('# foo“  '),
            # Tests the case where we done with checks and something left on stack.
            Comment('# „ «foo» '),
            # Text the case where we have matches, but not in order.
            Comment('# « „ foo» “ '),
        ]
        self._do_checker_comment_test(faults, 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_single_file(Blank())

    # #################################################################################################

    def test_opening_and_closing_lists(self) -> None:
        """
        Checks if lists defining opening and closing markers are sane.
        """
        checker: TypesettingQuotationMarks = self.get_checker()

        self.assertEqual(len(checker.opening), len(checker.closing))
        self.assertNotEqual([], checker.opening)
        self.assertNotEqual([], checker.closing)
        self.assertNotEqual(checker.opening, checker.closing)

        # ensure no marker is in both lists
        for op_idx, op_marker in enumerate(checker.opening):
            self.assertFalse(op_marker in checker.closing, f'Marker {op_marker} (position: {op_idx}) is present in closing too.')
        for cl_idx, cl_marker in enumerate(checker.closing):
            self.assertFalse(cl_marker in checker.opening, f'Marker {cl_marker} (position: {cl_idx}) is present in opening too.')

    # #################################################################################################

    def test_config_sync(self) -> None:
        """
        Check if TypesettingQuotationMarks' config matches Brackets' one. This is currently needed
        as Checks are using `dict` based configs and TQM extends Brackets, therefore any missing
        key in TQM's config cause checker to fail with `KeyError`.
        """
        brackets = list(Brackets().get_default_config().keys())
        tqm = list(TypesettingQuotationMarks().get_default_config().keys())

        self.assertEqual(sorted(brackets), sorted(tqm))
