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
from transtool.checks.missing_translations import MissingTranslations
from transtool.decorators.overrides import overrides
from transtool.prop.items import Comment
from tests.checks.checks_test_case import ChecksTestCase


class TestMissingTranslations(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return MissingTranslations(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)
        self.check(trans_file, ref_file)

    def test_translation_with_keys_in_comments(self) -> None:
        """
        Checks if we have no issues reported when running in non-strict mode and having some translation
        keys in commented-out form, like:
        # ==> KEY =
        """
        # Generate some keys for reference file.
        cnt_min = 10
        cnt_max = 15
        ref_keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for translation file
        how_many_less = random.randint(1, cnt_min - 1)
        how_many_less = 1
        trans_keys = ref_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)

        # Put remaining keys into comments.
        remaining_keys = ref_keys[(how_many_less * -1):]
        for key in remaining_keys:
            if random.randint(0, 1) == 0:
                comment = Comment.get_commented_out_key_comment(self.config, key)
            else:
                val = self.get_random_string('translation')
                comment = Comment.get_commented_out_key_comment(self.config, key, val)
            trans_file.append(comment)

        # We expect no issues in non-strict mode
        self.checker.config['strict'] = False
        self.check(trans_file, ref_file)

        # We expect warnings in strict mode
        self.checker.config['strict'] = True
        self.check(trans_file, ref_file, exp_warnings = len(remaining_keys))

    def test_translation_with_faults(self) -> None:
        # generate some keys for reference file
        cnt_min = 20
        cnt_max = 40
        ref_keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for translation file
        how_many_less = random.randint(1, cnt_min - 1)
        trans_keys = ref_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)
        self.check(trans_file, ref_file, exp_warnings = how_many_less)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()
