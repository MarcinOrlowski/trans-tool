"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from transtool.config.config import Config
from transtool.prop.items import Comment
from tests.test_case import TestCase


class TestComment(TestCase):

    def test_constructor(self) -> None:
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            item = Comment(value)
            self.assertEqual(value, item.value)
            self.assertIsNone(item.key)

    def test_invalid_value(self) -> None:
        with self.assertRaises(ValueError):
            # Invalid value type
            # noinspection PyTypeChecker
            Comment(1234)

    def test_without_marker(self) -> None:
        """
        Checks if constructing Comment without valid marker in passed value
        would automatically add such marker.
        """
        val = self.get_random_string('no_maker')
        # No valid comment marker
        comment = Comment(val)
        self.assertEqual(f'{Config.ALLOWED_COMMENT_MARKERS[0]} {val}', comment.to_string())

    def test_empty_value(self) -> None:
        comment = Comment('')
        self.assertEqual(Config.ALLOWED_COMMENT_MARKERS[0], comment.to_string())

    def test_to_string(self) -> None:
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            comment = Comment(value)
            self.assertEqual(value, comment.to_string())
