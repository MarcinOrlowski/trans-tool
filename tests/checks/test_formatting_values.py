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
from transtool.checks.formatting_values import FormattingValues
from transtool.decorators.overrides import overrides
from transtool.prop.file import PropFile
from transtool.prop.items import Translation
from tests.checks.checks_test_case import ChecksTestCase


class TestFormattingValues(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        return FormattingValues(config)

    # #################################################################################################

    def test_no_faults(self) -> None:
        tests = [
            ('This %s foo %d %s', 'This 123 %s %d llorem bar %s ipsum.'),
            ('This has no %% formatters', 'Tricky one'),
        ]

        for test_case in tests:
            ref_file = PropFile(self.config)
            trans_file = PropFile(self.config)

            key = self.get_random_string()
            ref_file.append(Translation(key, test_case[0]))
            trans_file.append(Translation(key, test_case[1]))
            self.check(trans_file, ref_file)

    def test_with_faults(self) -> None:
        """
        Tests various types of formatters count mismatch
        """
        tests = [
            ('This %s foo %s line 1', 'This 123 %s %d llorem bar %s ipsum.'),
            ('This %s line 2', 'This 123 %s %d llorem bar %s ipsum.'),
            ('%d foo line 3', '123 %s %d llorem bar %s ipsum.'),
            ('No formatters in line 4', 'But we have %s one...'),
            ('%s one formatter in line 5', 'But we have none.'),

            # Count matches, but order is messed.
            ('Count matches: %s %d', 'But order differs: %d %s'),
        ]

        for test_case in tests:
            ref_file = PropFile(self.config)
            trans_file = PropFile(self.config)

            key = self.get_random_string()
            ref_file.append(Translation(key, test_case[0]))
            trans_file.append(Translation(key, test_case[1]))
            # This checker always return one error (if there's any fault).
            self.check(trans_file, ref_file, exp_errors = 1, msg = f"'{test_case[0]}' vs. '{test_case[1]}'")

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_skipping_blank_and_comment()

    def test_handling_of_dangling_translation_keys(self) -> None:
        self.check_skipping_of_dangling_keys()
