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
from proptool.checks.punctuation import Punctuation
from proptool.config.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.file import PropFile
from proptool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestPunctuation(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Config, None] = None) -> Check:
        return Punctuation(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        marks = self.config.checks['Punctuation']['chars']
        punct_idx = 0

        ref_file = PropFile(self.config)
        trans_file = PropFile(self.config)
        for key in keys:
            value = self.get_random_string() + marks[punct_idx % len(marks)]
            ref_file.append(Translation(key, value))
            trans_file.append(Translation(key, value))
            punct_idx += 1

        self.check(trans_file, ref_file)

    def test_with_faults(self) -> None:
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key_') for _ in range(random.randint(cnt_min, cnt_max))]

        marks = self.config.checks['Punctuation']['chars']
        punct_idx = 0

        expected_faults = 0

        ref_file = PropFile(self.config)
        trans_file = PropFile(self.config)
        for key in keys:
            ref_value = self.get_random_string()
            trans_value = ref_value
            ref_value += marks[punct_idx % len(marks)]
            # FIXME: there's slight chance that we will have 1s for whole run...
            if random.randint(0, 1) == 1:
                trans_value += marks[punct_idx % len(marks)]
            else:
                expected_faults += 1
            ref_file.append(Translation(key, ref_value))
            trans_file.append(Translation(key, trans_value))
            punct_idx += 1
        self.check(trans_file, ref_file, exp_warnings = expected_faults)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank()
