"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random
from typing import Dict, List, Tuple, Union

from transtool.checks.base.check import Check
from transtool.checks.starts_with_the_same_case import StartsWithTheSameCase
from transtool.decorators.overrides import overrides
from transtool.prop.file import PropFile
from transtool.prop.items import Translation
from transtool.utils import Utils
from tests.checks.checks_test_case import ChecksTestCase


class TestStartsWithTheSameCase(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return StartsWithTheSameCase(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        cnt_min = 20
        cnt_max = 40
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

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
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

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

    def _do_scan_test(self, tests: List[Tuple[str, str]], exp_warnings = 0):
        for ref_value, trans_value in tests:
            ref_file = PropFile(self.config)
            trans_file = PropFile(self.config)
            key = self.get_random_string('key')
            ref_file.append(Translation(key, ref_value))
            trans_file.append(Translation(key, trans_value))
            self.check(trans_file, ref_file, exp_warnings = exp_warnings)

    def test_valid_special_cases(self) -> None:
        """
        Checks is checker will correctly compare sequences starting
        with alphabetic characters, no matter where they are located
        in the strings.
        """
        tests = [
            # These should be matched correctly.
            ('%s Statistics', 'Statystyki %s'),
            ('%s statistics', '123 statystyki %s'),
            ('%s 123 Statistics', 'Statystyki %s'),
        ]
        self.checker.config['accept_digits'] = False
        self._do_scan_test(tests, 0)

    def test_fault_special_cases(self) -> None:
        tests = [
            ('%s Statistics', 'statystyki %s'),
            ('%s statistics', '123 Statystyki %s'),
            ('%s 123 tatistics', 'Statystyki %s'),

            # Base has no real words, while translation has some.
            ('123 123 123', 'Some words here'),

            # Base has words, translation does not.
            ('Some words here', '123 123 123'),
        ]
        self.checker.config['accept_digits'] = False
        self._do_scan_test(tests, 1)

    def test_no_alpha_words(self) -> None:
        tests = [
            # These should be skipped silently.
            ('', ''),
            # No real words. This should be skipped silently.
            ('3434 3434 34', '123 123 123'),
        ]
        self.checker.config['accept_digits'] = False
        self._do_scan_test(tests)

    # #################################################################################################

    def test_opening_digits(self) -> None:
        tests = [
            ('Upper', '12345 lower'),
            ('12345 Upper', 'lower'),
            ('12345 Upper', '345345 lower'),
        ]
        self.checker.config['accept_digits'] = False
        self._do_scan_test(tests, exp_warnings = 1)

        self.checker.config['accept_digits'] = True
        self._do_scan_test(tests)

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
        keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

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
