"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.prop.items import Blank
from tests.test_case import TestCase


class TestBlank(TestCase):

    def test_blank_constructor(self) -> None:
        item = Blank()
        self.assertIsNone(item.key)
        self.assertIsNone(item.value)

    def test_blank_to_string(self) -> None:
        item = Blank()
        self.assertEqual('', item.to_string())
