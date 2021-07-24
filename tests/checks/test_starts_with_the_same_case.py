"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import random
from typing import Union

from proptool.checks.base.check import Check
from proptool.checks.starts_with_the_same_case import StartsWithTheSameCase
from proptool.config.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.file import PropFile
from proptool.prop.items import Translation
from proptool.utils import Utils
from tests.checks.checks_test_case import ChecksTestCase


class TestStartsWithTheSameCase(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Config, None] = None) -> Check:
        return StartsWithTheSameCase(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        ref_file = PropFile(self.config)
        trans_file = PropFile(self.config)
        for key in keys:
            value = self.get_random_string()
            ref_file.append(Translation(key, value))
            trans_file.append(Translation(key, value))

        self.check(trans_file, ref_file)

    def test_with_faults(self) -> None:
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        expected_faults = 0

        ref_file = PropFile(self.config)
        trans_file = PropFile(self.config)
        for key in keys:
            ref_value = self.get_random_string()
            trans_value = ref_value

            # FIXME: there's slight chance that we will have 1s for whole run...
            if random.randint(0, 1) == 1:
                expected_faults += 1
                if ref_value[0].isupper():
                    trans_value = Utils.lower_first(trans_value)
                else:
                    trans_value = Utils.upper_first(trans_value)
            ref_file.append(Translation(key, ref_value))
            trans_file.append(Translation(key, trans_value))
        self.check(trans_file, ref_file, exp_warnings = expected_faults)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()

    def test_handling_of_dangling_translation_keys(self) -> None:
        self.check_skipping_of_dangling_keys()

    def test_skipping_of_entry_items(self) -> None:
        """
        Checks if item is silently skipped if its value is empty string or value of reference
        string is empty.
        :return:
        """
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        ref_file = self.build_prepfile(keys, lower = True)
        trans_file = self.build_prepfile(keys, lower = True)

        # Let's clear some values in both files
        upper_bound = 10
        for _ in range(random.randint(1, upper_bound)):
            ref_idx = random.randrange(len(ref_file.items))
            ref_file.items[ref_idx].value = ''

            trans_idx = random.randrange(len(trans_file.items))
            trans_file.items[trans_idx].value = ''

        # We expect no problems.
        self.check(trans_file, ref_file)
