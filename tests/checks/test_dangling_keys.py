"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random
from typing import Dict, Union

from transtool.checks.base.check import Check
from transtool.checks.dangling_keys import DanglingKeys
from transtool.decorators.overrides import overrides
from tests.checks.checks_test_case import ChecksTestCase


class TestDanglingKeys(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return DanglingKeys(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)
        self.check(trans_file, ref_file)

    def test_translation_with_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        trans_keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for reference file
        upper_bound = 10
        how_many_less = random.randint(1, upper_bound)
        ref_keys = trans_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)
        self.check(trans_file, ref_file, exp_errors = how_many_less)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
