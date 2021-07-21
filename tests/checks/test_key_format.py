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
from proptool.prop.entries import PropTranslation
from proptool.decorators.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestKeyFormat(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return KeyFormat(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.check_single_file(PropTranslation('validKey', 'foo'))
        self.check_single_file(PropTranslation('valid123Key', 'foo'))
        self.check_single_file(PropTranslation('validKey123', 'foo'))
        self.check_single_file(PropTranslation('valid.Key', 'foo'))
        self.check_single_file(PropTranslation('valid_Key', 'foo'))

    def test_translation_with_faults(self):
        # Too short key name
        self.check_single_file(PropTranslation('k', 'foo'), exp_errors = 1)
        # starts capitalized
        self.check_single_file(PropTranslation('INVALIDkey', 'foo'), exp_errors = 1)
        # has underscore at the end
        self.check_single_file(PropTranslation('invalidKey_', 'foo'), exp_errors = 1)
        # has dot at the end
        self.check_single_file(PropTranslation('invalidKey.', 'foo'), exp_errors = 1)
        # starts with digits
        self.check_single_file(PropTranslation('666keys.', 'foo'), exp_errors = 1)
