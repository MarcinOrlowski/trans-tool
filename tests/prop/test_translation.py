"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random

from transtool.config.config import Config
from transtool.prop.items import Translation
from tests.test_case import TestCase


# Extending TestCase to get access to helper methods.
class SplitTest(TestCase):
    """
    Helper class to reduce bolderplate code in in
    """

    def __init__(self, fmt: str, mid_val_sep = True):
        key = self.get_random_string('key', length = 10)
        sep = random.choice(Config.ALLOWED_SEPARATORS)
        val_sep = random.choice(Config.ALLOWED_SEPARATORS) if mid_val_sep else ''
        val = self.get_random_string(length = 10) + val_sep + self.get_random_string(length = 10)

        self.key = key
        self.sep = sep
        self.val_sep = val_sep
        self.val = val

        if fmt.find('{key}') != -1:
            fmt = fmt.replace('{key}', key)
        if fmt.find('{sep}') != -1:
            fmt = fmt.replace('{sep}', sep)
        if fmt.find('{val}') != -1:
            fmt = fmt.replace('{val}', val)

        self.line = fmt


class TestTranslation(TestCase):

    def test_invalid_key_type(self) -> None:
        """
        Tests handing of invalid key type.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(123, value)
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(None, value)

    def test_empty_key(self) -> None:
        """
        Tests handling of empty key.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation('', value)

    def test_empty_key_after_strip(self) -> None:
        """
        Tests handling of non-empty key that gets empty once strip()'ed.
        """
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation('   ', value)

    def test_invalid_value_type(self) -> None:
        with self.assertRaises(ValueError):
            key = self.get_random_string()
            # noinspection PyTypeChecker
            Translation(key, 1234)

        value = self.get_random_string()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            Translation(key, value, None)

    def test_invalid_separator(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation(key, value, '-')

    def test_empty_separator(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        with self.assertRaises(ValueError):
            Translation(key, value, '')

    def test_to_string(self) -> None:
        config = Config()
        for separator in config.ALLOWED_SEPARATORS:
            key = self.get_random_string()
            value = self.get_random_string()
            trans = Translation(key, value, separator)
            expected = f'{key} {separator} {value}'
            self.assertEqual(expected, trans.to_string())

    # #################################################################################################

    def test_parse_translation_line_with_valid_entries(self) -> None:
        lines = [
            '{key}{sep}{val}',
            '{key} {sep} {val}',
            '      {key}     {sep} {val}',
            '{key} {sep}{val}',
            '{key}{sep} {val}',
            '{key} {sep}      {val}',
            '{key}      {sep}{val}',
            '{key}{sep}    {val}',
        ]
        tests = [SplitTest(fmt) for fmt in lines]

        for test in tests:
            res = Translation.parse_translation_line(test.line)
            self.assertIsNotNone(res)
            res_key, res_sep, res_val = res
            self.assertEqual(test.key, res_key)
            self.assertEqual(test.sep, res_sep)
            self.assertEqual(test.val, res_val)

    def test_parse_translation_line_invalid_entries(self) -> None:
        lines = [
            '{sep}{val}',
            '{key} {val}',
            '         {sep}   ',
            '{sep}{val}',
            '{sep}{key}{sep} {val}',
        ]
        tests = [SplitTest(fmt, mid_val_sep = False) for fmt in lines]

        for test in tests:
            res = Translation.parse_translation_line(test.line)
            self.assertIsNone(res)

    def test_parse_translation_line_escaped_chars(self) -> None:
        key = r'this\=is\:\key'
        sep = random.choice(Config.ALLOWED_SEPARATORS)
        val = self.get_random_string('value')
        line = f'{key}{sep}{val}'

        res = Translation.parse_translation_line(line)
        self.assertIsNotNone(res)
        res_key, res_sep, res_val = res
        self.assertEqual(key, res_key)
        self.assertEqual(sep, res_sep)
        self.assertEqual(val, res_val)
