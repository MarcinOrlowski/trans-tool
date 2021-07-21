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
from proptool.checks.missing_translation import MissingTranslation
from proptool.config import Config
from proptool.entries import PropComment
from proptool.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestMissingTranslations(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return MissingTranslation(config)

    # #################################################################################################

    def test_no_faults(self):
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]
        ref_file = self.build_prepfile(keys)
        trans_file = self.build_prepfile(keys)
        self.do_test(ref_file, trans_file)

    def test_translation_with_keys_in_comments(self):
        # Checks if we have no issues reported when running
        # in non-strict mode and having some keys in comments.

        # generate some keys for reference file
        cnt_min = 20
        cnt_max = 40
        ref_keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for translation file
        how_many_less = random.randint(1, cnt_min - 1)
        trans_keys = ref_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)

        # put remaining keys into comments
        remaining_keys = ref_keys[(how_many_less * -1):]
        for key in remaining_keys:
            comment = self.config.DEFAULT_COMMENT_TEMPLATE
            comment = comment.replace('SEP', trans_file.separator).replace('COM', self.config.comment_marker).replace('KEY', key)
            trans_file.append(PropComment(comment))

        # We expect no issues in non-strict mode
        trans_file.config.strict = False
        self.do_test(ref_file, trans_file)

        # We expect warnings in strict mode
        trans_file.config.strict = True
        self.do_test(ref_file, trans_file, exp_warnings = len(remaining_keys))

    def test_translation_with_faults(self):
        # generate some keys for reference file
        cnt_min = 20
        cnt_max = 40
        ref_keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for translation file
        how_many_less = random.randint(1, cnt_min - 1)
        trans_keys = ref_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys)
        trans_file = self.build_prepfile(trans_keys)
        self.do_test(ref_file, trans_file, exp_warnings = how_many_less)
