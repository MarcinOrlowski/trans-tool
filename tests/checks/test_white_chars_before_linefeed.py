"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2023 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Optional

from transtool.checks.base.check import Check
from transtool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from transtool.config.config import Config
from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestWhiteCharsBeforeLinefeed(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Optional[Config] = None) -> Check:
        return WhiteCharsBeforeLinefeed(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', r'This is\nall\nOK'))

    def test_translation_string_too_short(self) -> None:
        # Checks behavior when the string is too short to fit space and literals,
        self.check_single_file(Translation('key', r' X'))
        self.check_single_file(Translation('key', r'\n'))

    def test_translation_with_faults(self) -> None:
        self.check_single_file(
            Translation('key', r'This is NOT \n OK.'), exp_warnings=1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
