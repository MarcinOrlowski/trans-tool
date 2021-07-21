"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import random

from checks.checks_test_case import ChecksTestCase
from proptool.checks.base.check import Check
from proptool.checks.dangling_keys import DanglingKeys
from proptool.config import Config
from proptool.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestDanglingKeys(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return DanglingKeys(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)
        self.do_test(ref_file, trans_file)

    def test_translation_with_faults(self):
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        trans_keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for reference file
        upper_bound = 10
        how_many_less = random.randint(1, upper_bound)
        ref_keys = trans_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)
        self.do_test(ref_file, trans_file, exp_errors = how_many_less)
