"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.config import Config
from proptool.prop.items import Blank, Comment, PropItem, Translation
from tests.test_case import TestCase


class TestReportItem(TestCase):

    def test_base_constructor_args_none(self):
        item = PropItem()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_base_constructor_args(self):
        key = self.get_random_string()
        value = self.get_random_string()
        item = PropItem(value, key)
        self.assertEqual(key, item.key)
        self.assertEqual(value, item.value)

    def test_base_to_string_not_implemented(self):
        item = PropItem()
        with self.assertRaises(NotImplementedError):
            item.to_string()

    # #################################################################################################

    def test_translation_invalid_key(self):
        with self.assertRaises(ValueError):
            value = self.get_random_string()
            Translation(123, value)
            Translation(None, value)
            Translation('', value)
            Translation('   ', value)

    def test_translation_invalid_value(self):
        with self.assertRaises(ValueError):
            key = self.get_random_string()
            Translation(key, 1234)

    def test_translation_invalid_separator(self):
        with self.assertRaises(ValueError):
            key = self.get_random_string()
            value = self.get_random_string()
            Translation(key, value, None)
            Translation(key, value, '-')
            Translation(key, value, '')

    def test_translation_to_string(self):
        config = Config()
        for separator in config.ALLOWED_SEPARATORS:
            key = self.get_random_string()
            value = self.get_random_string()
            trans = Translation(key, value, separator)
            expected = f'{key} {separator} {value}'
            self.assertEqual(expected, trans.to_string())

    # #################################################################################################

    def test_comment_constructor(self):
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            item = Comment(value)
            self.assertEqual(value, item.value)
            self.assertIsNone(item.key)

    def test_comment_invalid_value(self):
        with self.assertRaises(ValueError):
            # Invalid type
            Comment(1234)
            # Empty string (lacks comment marker)
            Comment('')

    def test_comment_to_string(self):
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            comment = Comment(value)
            self.assertEqual(value, comment.to_string())

    # #################################################################################################

    def test_blank_constructor(self):
        item = Blank()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_blank_to_string(self):
        item = Blank()
        self.assertEqual('', item.to_string())
