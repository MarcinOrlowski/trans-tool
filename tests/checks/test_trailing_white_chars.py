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
from transtool.checks.trailing_white_chars import TrailingWhiteChars
from transtool.decorators.overrides import overrides
from transtool.prop.items import Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestTrailingWhiteChars(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return TrailingWhiteChars(config)

    # #################################################################################################

    def test_translation_no_trailing_white_chars(self) -> None:
        self.check_single_file(Translation('key', 'value'))

    def test_translation_with_trailing_white_chars(self) -> None:
        self.check_single_file(Translation('key', 'value  '), exp_errors = 1)

    def test_comment_no_trailing_white_chars(self) -> None:
        self.checker.config['comments'] = True
        self.check_single_file(Comment('# value'))

    def test_comment_with_trailing_white_chars(self) -> None:
        self.checker.config['comments'] = True
        self.check_single_file(Comment('# value  '), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank()
