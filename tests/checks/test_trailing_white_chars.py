"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.checks.base.check import Check
from proptool.checks.trailing_white_chars import TrailingWhiteChars
from proptool.config.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.items import Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestTrailingWhiteChars(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return TrailingWhiteChars(config)

    # #################################################################################################

    def test_translation_no_trailing_white_chars(self) -> None:
        self.check_single_file(Translation('key', 'value'))

    def test_translation_with_trailing_white_chars(self) -> None:
        self.check_single_file(Translation('key', 'value  '), exp_errors = 1)

    def test_comment_no_trailing_white_chars(self) -> None:
        self.check_single_file(Comment('# value'))

    def test_comment_with_trailing_white_chars(self) -> None:
        self.check_single_file(Comment('# value  '), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank()
