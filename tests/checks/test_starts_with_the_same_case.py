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
from proptool.checks.starts_with_the_same_case import StartsWithTheSameCase
from proptool.config import Config
from proptool.entries import PropTranslation
from proptool.overrides import overrides
from proptool.propfile import PropFile


# TODO: Test handling other types than PropTranslation

# #################################################################################################

class TestStartsWithTheSameCase(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return StartsWithTheSameCase(config)

    # #################################################################################################

    def test_no_faults(self):
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        ref_file = PropFile(self.config)
        trans_file = PropFile(self.config)
        for key in keys:
            value = self.get_random_string()
            ref_file.append(PropTranslation(key, value))
            trans_file.append(PropTranslation(key, value))

        self.do_test(ref_file, trans_file)

    def test_with_faults(self):
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
                    trans_value = trans_value[0].lower() + trans_value
                else:
                    trans_value = trans_value[0].upper() + trans_value
            ref_file.append(PropTranslation(key, ref_value))
            trans_file.append(PropTranslation(key, trans_value))
        self.do_test(ref_file, trans_file, exp_warnings = expected_faults)
