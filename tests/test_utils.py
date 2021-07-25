"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.utils import Utils

from tests.test_case import TestCase


class TestUtils(TestCase):

    def test_add_if_not_in_list(self) -> None:
        count = 10
        srcs = self.get_random_string_list(count)
        self.assertEqual(count, len(srcs))

        target = []

        # Try adding new elements
        for item in srcs:
            Utils.add_if_not_in_list(target, item)
        # Check element count changed.
        self.assertEqual(len(target), len(srcs))

        # Try adding duplicates
        for item in srcs:
            Utils.add_if_not_in_list(target, item)
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
            Utils.add_if_not_in_list([], 123)
        with self.assertRaises(TypeError):
            Utils.add_if_not_in_list([], False)
        with self.assertRaises(TypeError):
            Utils.add_if_not_in_list([], {})

    def test_add_if_not_in_dict(self) -> None:
        count = 10
        src = {}
        target = {}

        # Try adding new elements
        for _ in range(count):
            key = self.get_random_string('key_')
            val = self.get_random_string()
            Utils.add_if_not_in_dict(src, key, val)
            Utils.add_if_not_in_dict(target, key, val)
        self.assertEqual(count, len(src))

        # Try adding duplicates
        for key, value in src.items():
            self.assertFalse(Utils.add_if_not_in_dict(target, key, value))
        self.assertEqual(len(target), len(src))

    def test_remove_quotes(self) -> None:
        val = self.get_random_string()
        src = [
            f'"{val}',
            f'"{val}"',
            f'{val}"'
        ]
        for item in src:
            self.assertEqual(val, Utils.remove_quotes(item))

    def test_remove_quotes_too_short(self) -> None:
        items = ['', ' ']
        for item in items:
            self.assertEqual(item, Utils.remove_quotes(item))

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
