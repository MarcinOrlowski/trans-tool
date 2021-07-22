"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.checks.base.check import Check
from proptool.checks.quotation_marks import QuotationMarks
from proptool.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestQuotationMarks(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return QuotationMarks(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '""'))

    def test_translation_with_faults(self) -> None:
        self.check_single_file(Translation('key', '"""'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        self.check_single_file(Comment('#  "foo" '))

    def test_comment_with_faults(self) -> None:
        self.check_single_file(Comment('# "foo `"  '), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_single_file(Blank())
