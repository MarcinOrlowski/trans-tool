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
from transtool.checks.key_format import KeyFormat
from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestKeyFormat(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return KeyFormat(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('validKey', 'foo'))
        self.check_single_file(Translation('valid123Key', 'foo'))
        self.check_single_file(Translation('validKey123', 'foo'))
        self.check_single_file(Translation('valid.Key', 'foo'))
        self.check_single_file(Translation('valid_Key', 'foo'))

    def test_translation_with_faults(self) -> None:
        # too short
        self.check_single_file(Translation('k', 'foo'), exp_errors = 1)
        # starts with digits
        self.check_single_file(Translation('666keys.', 'foo'), exp_errors = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
