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
from transtool.checks.empty_translations import EmptyTranslations
from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestEmptyTranslations(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return EmptyTranslations(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)
        self.check(trans_file, ref_file)

    def test_if_both_are_empty(self) -> None:
        # Checks handling of empty string when matching reference string is
        # also empty or string containing just spaces (which is strip()ed)
        # generate some keys for file
        cnt_min = 10
        cnt_max = 20
        key_cnt = random.randint(cnt_min, cnt_max)
        keys = [self.get_random_string('key') for _ in range(key_cnt)]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)

        # Now, make some translations empty.
        how_many = random.randint(1, cnt_min)
        processed = how_many
        while processed > 0:
            idx = random.randint(0, key_cnt - 1)

            # noinspection PyTypeChecker
            ref: Translation = ref_file.items[idx]
            if ref.value != '':
                max_spaces = 3
                ref.value = ' ' * random.randint(0, max_spaces)
                ref_file.items[idx] = ref

                # noinspection PyTypeChecker
                trans: Translation = trans_file.items[idx]
                trans.value = ''
                trans_file.items[idx] = trans

                processed -= 1

        # We expect no problems.
        self.check(trans_file, ref_file)

    def test_translation_with_dangling_keys(self) -> None:
        # Checks if translation dangling keys will be silently skipped.
        cnt_min = 10
        cnt_max = 20
        key_cnt = random.randint(cnt_min, cnt_max)
        keys = [self.get_random_string('key') for _ in range(key_cnt)]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)

        # Now, make some translations empty.
        how_many = random.randint(1, cnt_min)
        removed_keys = []
        for _ in range(how_many):
            idx_to_remove = random.randint(0, len(ref_file.items) - 1)
            removed_keys.append(ref_file.items[idx_to_remove].key)
            del ref_file.items[idx_to_remove]

        # We also need to make these dangling entries empty string
        # otherwise it will be filtered earlier.
        for removed_key in removed_keys:
            trans = trans_file.find_by_key(removed_key)
            trans_idx = trans_file.items.index(trans)
            trans.value = ''
            trans_file.items[trans_idx] = trans

        # We expect no problems.
        self.check(trans_file, ref_file)

    def test_translation_with_faults(self) -> None:
        # generate some keys for file
        cnt_min = 10
        cnt_max = 20
        key_cnt = random.randint(cnt_min, cnt_max)
        keys = [self.get_random_string('key') for _ in range(key_cnt)]

        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)

        # Now, make some translations empty.
        how_many = random.randint(1, cnt_min)
        processed = how_many
        while processed > 0:
            idx = random.randint(0, key_cnt - 1)
            # noinspection PyTypeChecker
            trans: Translation = trans_file.items[idx]
            if trans.value != '':
                trans.value = ''
                trans_file.items[idx] = trans
                processed -= 1

        self.check(trans_file, ref_file, exp_warnings = how_many)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
