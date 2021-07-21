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
from proptool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from proptool.config import Config
from proptool.entries import PropTranslation
from proptool.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestWhiteCharsBeforeLinefeed(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return WhiteCharsBeforeLinefeed(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.do_single_test(PropTranslation('key', r'This is\nall\nOK'))

    def test_translation_string_too_short(self):
        # Checks behavior when the string is too short to fit space and litera,
        self.do_single_test(PropTranslation('key', r' X'))
        self.do_single_test(PropTranslation('key', r'\n'))

    def test_translation_with_faults(self):
        self.do_single_test(
            PropTranslation('key', r'This is NOT \n OK.'), exp_warnings = 1)
