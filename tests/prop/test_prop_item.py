"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from transtool.prop.items import PropItem
from tests.test_case import TestCase


class TestPropItem(TestCase):

    def test_base_constructor_args_none(self) -> None:
        item = PropItem()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_base_constructor_args(self) -> None:
        key = self.get_random_string()
        value = self.get_random_string()
        item = PropItem(value, key)
        self.assertEqual(key, item.key)
        self.assertEqual(value, item.value)

    def test_base_to_string_not_implemented(self) -> None:
        item = PropItem()
        with self.assertRaises(NotImplementedError):
            item.to_string()
