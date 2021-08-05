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

from transtool.checks.brackets import Brackets
from transtool.decorators.overrides import overrides
from transtool.prop.file import PropFile
from transtool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class ChecksBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Brackets:
        return Brackets(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '<({[]})>'))
        self.check_single_file(Translation('key', '<()foo ({a[v]b}d <barr> )> '))

    def test_translation_with_faults(self) -> None:
        # Tests error handling when we have popping bracket and empty stack.
        self.check_single_file(Translation('key', '}'), exp_errors = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Translation('key', '{()'), exp_errors = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Translation('key', '{(})'), exp_errors = 1)

    def test_empty_translation(self) -> None:
        propfile = PropFile(self.config)
        self.check(propfile)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        self.check_single_file(Comment('# (foo) '))

    def test_comment_with_faults(self) -> None:
        faults = [
            # Tests error handling when we have popping bracket and empty stack.
            '# foo]"  ',
            # Tests the case where we done with checks and something left on stack.
            '# {fo[o]" ',
            # Text the case where we have matches, but not in order.
            '# [foo {]}" ',
        ]

        for fault in faults:
            # We should see no issues if comment scanning is disabled.
            self.checker.config['comments'] = False
            self.check_single_file(Comment(fault))

            # And some warnings when comment scanning in enabled.
            self.checker.config['comments'] = True
            self.check_single_file(Comment(fault), exp_warnings = 1)

    # #################################################################################################

    def test_skipping_quoted_brakcets(self) -> None:
        """
        Check if correctly quoted brackets are ignored as expected.
        """
        tests = [
            'Is "[" Ok',
            "This shall ']' pass too",
        ]
        self.checker.config['comments'] = True
        for test in tests:
            # If we skip quoted brackets, nothing should be reported.
            self.checker.config['ignore_quoted'] = True
            self.check_single_file(Comment(test))

            # And some warnings when quited brackets are not ignored.
            self.checker.config['ignore_quoted'] = False
            self.check_single_file(Comment(test), exp_warnings = 1)

    # #################################################################################################

    def test_handling_of_unsupported_types(self) -> None:
        self.check_single_file(Blank())

    # #################################################################################################

    def test_opening_and_closing_lists(self) -> None:
        """
        Checks if lists defining opening and closing markers are sane.
        """
        checker: Brackets = self.get_checker(None)
        config = checker.get_default_config()

        self.assertEqual(len(config['opening']), len(config['closing']))
        self.assertNotEqual([], config['opening'])
        self.assertNotEqual([], config['closing'])
        self.assertNotEqual(config['opening'], config['closing'])

        # ensure no marker is in both lists
        for op_idx, op_marker in enumerate(config['opening']):
            self.assertFalse(op_marker in config['closing'], f'Marker {op_marker} (position: {op_idx}) is present in closing too.')
        for cl_idx, cl_marker in enumerate(config['closing']):
            self.assertFalse(cl_marker in config['opening'], f'Marker {cl_marker} (position: {cl_idx}) is present in opening too.')

    def test_uneven_opening_and_closing_lists(self) -> None:
        """
        Checks if error will be reported when opening and closing configuration
        lists contain different number of elements.
        """
        opening_cnt = random.randint(10, 20)
        opening = [self.get_random_string(length = 1) for item in range(opening_cnt)]

        closing_cnt = random.randint(10, 20)
        closing = [self.get_random_string(length = 1) for item in range(closing_cnt)]

        if closing_cnt == opening_cnt:
            if random.randint(0, 1) == 0:
                del opening[random.randint(0, opening_cnt - 1)]
            else:
                del closing[random.randint(0, closing_cnt - 1)]

        self.checker.config['opening'] = opening
        self.checker.config['closing'] = closing

        prop_file = PropFile(self.config)
        self.check(prop_file, exp_errors = 1)

    def test_empty_opening_or_closing_lists(self) -> None:
        non_empty_cnt = random.randint(10, 20)
        non_empty = [self.get_random_string(length = 1) for item in range(non_empty_cnt)]
        empty = []

        self.checker.config['opening'] = non_empty
        self.checker.config['closing'] = empty
        prop_file = PropFile(self.config)
        self.check(prop_file, exp_warnings = 1)

        self.checker.config['opening'] = empty
        self.checker.config['closing'] = non_empty
        prop_file = PropFile(self.config)
        self.check(prop_file, exp_warnings = 1)

        self.checker.config['opening'] = empty
        self.checker.config['closing'] = empty
        prop_file = PropFile(self.config)
        self.check(prop_file, exp_warnings = 1)
