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
from proptool.checks.key_format import KeyFormat
from proptool.config import Config
from proptool.entries import PropTranslation
from proptool.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestKeyFormat(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return KeyFormat(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.do_single_test(PropTranslation('validKey', 'foo'))
        self.do_single_test(PropTranslation('valid123Key', 'foo'))
        self.do_single_test(PropTranslation('validKey123', 'foo'))
        self.do_single_test(PropTranslation('valid.Key', 'foo'))
        self.do_single_test(PropTranslation('valid_Key', 'foo'))

    def test_translation_with_faults(self):
        # Too short key name
        self.do_single_test(PropTranslation('k', 'foo'), exp_errors = 1)
        # starts capitalized
        self.do_single_test(PropTranslation('INVALIDkey', 'foo'), exp_errors = 1)
        # has underscore at the end
        self.do_single_test(PropTranslation('invalidKey_', 'foo'), exp_errors = 1)
        # has dot at the end
        self.do_single_test(PropTranslation('invalidKey.', 'foo'), exp_errors = 1)
        # starts with digits
        self.do_single_test(PropTranslation('666keys.', 'foo'), exp_errors = 1)
