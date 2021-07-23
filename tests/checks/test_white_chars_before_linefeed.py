"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.checks.base.check import Check
from proptool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from proptool.config.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestWhiteCharsBeforeLinefeed(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return WhiteCharsBeforeLinefeed(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', r'This is\nall\nOK'))

    def test_translation_string_too_short(self) -> None:
        # Checks behavior when the string is too short to fit space and litera,
        self.check_single_file(Translation('key', r' X'))
        self.check_single_file(Translation('key', r'\n'))

    def test_translation_with_faults(self) -> None:
        self.check_single_file(
            Translation('key', r'This is NOT \n OK.'), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
