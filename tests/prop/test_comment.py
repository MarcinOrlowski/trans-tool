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
        with self.assertRaises(TypeError):
            # Invalid value type
            # noinspection PyTypeChecker
            Comment(1234)

    def test_constructor_value_with_no_marker(self) -> None:
        """
        Checks if constructing Comment without valid marker in passed value
        would automatically add such marker.
        """
        val = self.get_random_string('no_maker')
        # No valid comment marker
        comment = Comment(val)
        self.assertEqual(f'{Config.ALLOWED_COMMENT_MARKERS[0]} {val}', comment.to_string())

    def test_constructor_marker_invalid_value(self) -> None:
        """
        Checks if constructing Comment with invalid marker would raise an Error.
        """
        marker = self.get_random_string(length = 1)
        self.assertNotIn(marker, Config.ALLOWED_COMMENT_MARKERS)
        val = self.get_random_string()
        with self.assertRaises(ValueError):
            Comment(value = val, marker = marker)

    def test_constructor_marker_wrong_type(self) -> None:
        """
        Ensures marker type is checked.
        """
        with self.assertRaises(TypeError):
            # Marker must be a string or TypeError is expected.
            # noinspection PyTypeChecker
            Comment(value = '', marker = 123)

    def test_empty_value(self) -> None:
        comment = Comment('')
        self.assertEqual(Config.ALLOWED_COMMENT_MARKERS[0], comment.to_string())

    # #################################################################################################

    def test_to_string(self) -> None:
        config = Config()
        for marker in config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {self.get_random_string()}'
            comment = Comment(value)
            self.assertEqual(value, comment.to_string())
