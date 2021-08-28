"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import random

from transtool.utils import Utils
from tests.test_case import TestCase


class TestUtils(TestCase):

    def test_abort(self) -> None:
        expected_rc = random.randint(1, 255)
        with self.assertRaises(SystemExit) as context_manager:
            Utils.abort(expected_rc)

            # Check we got sys.exit called with our return code.
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEqual(expected_rc, context_manager.exception.code)

    def test_add_if_not_in_list(self) -> None:
        count = 10
        srcs = self.get_random_string_list(count)
        self.assertEqual(count, len(srcs))

        target = []

        # Try adding new elements
        for item_new in srcs:
            Utils.add_if_not_in_list(target, item_new)
        # Check element count changed.
        self.assertEqual(len(target), len(srcs))

        # Try adding duplicates
        for item_dup in srcs:
            Utils.add_if_not_in_list(target, item_dup)
        # Check element count is unaltered.
        self.assertEqual(count, len(target))

    def test_add_if_not_in_list_with_list(self) -> None:
        count = 10
        srcs = self.get_random_string_list(count)
        self.assertEqual(count, len(srcs))

        target = []
        Utils.add_if_not_in_list(target, srcs)
        self.assertEqual(len(target), len(srcs))

        # Try adding duplicates
        Utils.add_if_not_in_list(target, srcs)
        self.assertEqual(count, len(target))

    def test_add_if_not_in_list_args_types(self) -> None:
        # These are fine
        Utils.add_if_not_in_list([], 'string')
        Utils.add_if_not_in_list([], ['string'])

        # These shall not pass
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            Utils.add_if_not_in_list([], 123)
        with self.assertRaises(TypeError):
            wrong_type = False
            # noinspection PyTypeChecker
            Utils.add_if_not_in_list([], wrong_type)
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            Utils.add_if_not_in_list([], {})

    # #################################################################################################

    def test_add_if_not_in_dict(self) -> None:
        count = 10
        src = {}
        target = {}

        # Try adding new elements
        for _ in range(count):
            key = self.get_random_string('key')
            val = self.get_random_string()
            Utils.add_if_not_in_dict(src, key, val)
            Utils.add_if_not_in_dict(target, key, val)
        self.assertEqual(count, len(src))

        # Try adding duplicates
        for key_dup, value_dup in src.items():
            self.assertFalse(Utils.add_if_not_in_dict(target, key_dup, value_dup))
        self.assertEqual(len(target), len(src))

    # #################################################################################################

    def test_remove_quotes_str(self) -> None:
        val = self.get_random_string()
        src = [
            f'"{val}',
            f'"{val}"',
            f'{val}"',
        ]
        for item in src:
            # It's expected to be handled by remove_quotes_str()
            self.assertEqual(val, Utils.remove_quotes(item))

    def test_remove_quotes_str_too_short(self) -> None:
        items = ['', ' ']
        for item in items:
            # It's expected to be handled by remove_quotes_from_str()
            self.assertEqual(item, Utils.remove_quotes(item))

    def test_remove_quotes_from_list(self) -> None:
        val = self.get_random_string()
        src = [
            f'"{val}',
            f'"{val}"',
            f'{val}"',
        ]
        # It's expected to be handled by remove_quotes_from_list()
        result = Utils.remove_quotes(src)
        for item in result:
            self.assertEqual(item, val)

    def test_remove_quotes_from_dict(self) -> None:
        key = self.get_random_string('key')
        val_1 = self.get_random_string()
        val_2 = self.get_random_string()
        val_3 = self.get_random_string()
        src = {
            f'"{key}_1':  f'"{val_1}',
            f'"{key}_2"': f'"{val_2}"',
            f'{key}_3"':  f'{val_3}"',
        }

        # It's expected to be handled by remove_quotes_from_dict()
        result = Utils.remove_quotes(src)
        self.assertEqual(len(src), len(result))

        result_key = f'{key}_1'
        self.assertIn(result_key, result)
        self.assertEqual(result[result_key], val_1)

        result_key = f'{key}_2'
        self.assertIn(result_key, result)
        self.assertEqual(result[result_key], val_2)

        result_key = f'{key}_3'
        self.assertIn(result_key, result)
        self.assertEqual(result[result_key], val_3)

    def test_remove_quotes_with_unsupported_arg(self) -> None:
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            Utils.remove_quotes(123)

    # #################################################################################################

    def test_upper_first(self) -> None:
        # Get random string. Ensure first letter is lower-cased.
        string = self.get_random_string(length = 1).lower() + self.get_random_string()
        # Generate upper/lower map of current string.
        case_map = [char.isupper() for idx, char in enumerate(string)]
        # Ensure first character is lower-cased.
        self.assertFalse(case_map[0])

        upper_str = Utils.upper_first(string)

        # We expect first character to be upper-cased now, other unaltered.
        case_map[0] = True
        for idx, char in enumerate(upper_str):
            self.assertEqual(case_map[idx], char.isupper())

    def test_upper_first_empty_string_or_none(self) -> None:
        self.assertEqual('', Utils.upper_first(''))
        self.assertEqual(None, Utils.upper_first(None))

    def test_lower_first(self) -> None:
        # Get random string. Ensure first letter is upper-cased.
        string = self.get_random_string(length = 1).upper() + self.get_random_string()
        # Generate upper/lower map of current string.
        case_map = [char.isupper() for idx, char in enumerate(string)]
        # Ensure first character is lower-upper.
        self.assertTrue(case_map[0])

        upper_str = Utils.lower_first(string)

        # We expect first character to be lower-cased now, other unaltered.
        case_map[0] = False
        for idx, char in enumerate(upper_str):
            self.assertEqual(case_map[idx], char.isupper())

    def test_lower_first_empty_string_or_none(self) -> None:
        self.assertEqual('', Utils.lower_first(''))
        self.assertEqual(None, Utils.lower_first(None))
