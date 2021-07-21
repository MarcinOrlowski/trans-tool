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
from proptool.checks.trailing_white_chars import TrailingWhiteChars
from proptool.config import Config
from proptool.prop.items import PropComment, Translation
from proptool.decorators.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestTrailingWhiteChars(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return TrailingWhiteChars(config)

    # #################################################################################################

    def test_translation_no_trailing_white_chars(self):
        self.check_single_file(Translation('key', 'value'))

    def test_translation_with_trailing_white_chars(self):
        self.check_single_file(Translation('key', 'value  '), exp_errors = 1)

    def test_comment_no_trailing_white_chars(self):
        self.check_single_file(PropComment('# value'))

    def test_comment_with_trailing_white_chars(self):
        self.check_single_file(PropComment('# value  '), exp_warnings = 1)
