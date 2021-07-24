"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Union

from proptool.checks.base.check import Check
from proptool.checks.brackets import Brackets
from proptool.config.config import Config
from proptool.decorators.overrides import overrides
from proptool.prop.items import Blank, Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class ChecksBrackets(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Config, None] = None) -> Check:
        return Brackets(config)

    # #################################################################################################

    def test_translation_no_faults(self) -> None:
        self.check_single_file(Translation('key', '<({[]})>'))
        self.check_single_file(Translation('key', '<()foo ({a[v]b}d <barr> )> '))

    def test_translation_with_faults(self) -> None:
        # Tests error handling when we have popping bracket and empty stack.
        self.check_single_file(Translation('key', '>'), exp_errors = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Translation('key', '(<>'), exp_errors = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Translation('key', '<(>)'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        self.check_single_file(Comment('# (foo) '))

    def test_comment_with_faults(self) -> None:
        # Tests error handling when we have popping bracket and empty stack.
        self.check_single_file(Comment('# foo]"  '), exp_warnings = 1)
        # Tests the case where we done with checks and something left on stack.
        self.check_single_file(Comment('# <fo[o]" '), exp_warnings = 1)
        # Text the case where we have matches, but not in order.
        self.check_single_file(Comment('# [foo <]>" '), exp_warnings = 1)

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
