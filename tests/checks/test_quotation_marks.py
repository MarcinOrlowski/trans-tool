"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from typing import Dict, Union

from transtool.checks.base.check import Check
from transtool.checks.quotation_marks import QuotationMarks
from transtool.decorators.overrides import overrides
from transtool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestQuotationMarks(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return QuotationMarks(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '""'))

    def test_translation_with_faults(self) -> None:
        self.check_single_file(Translation('key', '"""'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        tests = [
            Comment('#  "foo" '),
        ]
        self._do_checker_comment_test(tests, 0)

    def test_comment_with_faults(self) -> None:
        tests = [
            Comment('# "foo `"  '),
        ]
        self._do_checker_comment_test(tests, 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_single_file(Blank())
