"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from proptool.prop.items import Blank, Comment, Translation

from proptool.config.config import Config
from proptool.prop.file import PropFile
from tests.test_case import TestCase


class TestPropFile(TestCase):

    def test_append_wrong_arg_type(self) -> None:
        # GIVEN normal instance of PropFile
        prop_file = PropFile(Config())

        # WHEN we try to append object of unsupported type
        obj = 'INVALID'

        # THEN Exception should be thrown.
        with self.assertRaises(TypeError):
            prop_file.append(obj)

    # #################################################################################################

    @patch('pathlib.Path.exists')
    def test_load_non_existing_file(self, path_mock: Mock) -> None:
        """
        Tests if load() parses source file properly.

        :param path_mock: Mocked Path
        """
        prop_file = PropFile(Config())

        path_mock.return_value = False
        prop_file.load(Path('foo'))

    @patch('pathlib.Path.exists')
    def test_load_strip_crlf(self, path_mock: Mock) -> None:
        """
        Ensures trailing LF and CRLFs are properly stripped from read lines.

        :param path_mock: Mocked Path
        """

        com0 = self.get_random_string()
        com1 = self.get_random_string()

        for sep in Config.ALLOWED_COMMENT_MARKERS:
            fake_data_src = [
                f'{sep} {com0}\n',
                f'{sep} {com1}\r\n',
            ]

            with patch('builtins.open', mock_open(read_data = ''.join(fake_data_src))) as pm:
                # Lie our fake file exists
                path_mock.return_value = True
                prop_file = PropFile(Config(), Path('foo'))
                self.assertEqual(len(fake_data_src), len(prop_file.items))

                for comment in prop_file.items:
                    self.assertIsInstance(comment, Comment)

                item = prop_file.items[0]
                self.assertEqual(f'{sep} {com0}', item.value)
                item = prop_file.items[1]
                self.assertEqual(f'{sep} {com1}', item.value)

    @patch('pathlib.Path.exists')
    def test_load_valid_file(self, path_mock: Mock) -> None:
        """
        Tests if load() parses valid source *.properties file correctly.

        :param path_mock: Mocked Path
        """

        comment1_marker = '#'
        comment1_value = self.get_random_string('comment_')

        key1 = self.get_random_string('key1_')
        sep1 = '='
        val1 = self.get_random_string('val1_')

        comment2_marker = '!'
        comment2_value = self.get_random_string('comment_')

        key2 = self.get_random_string('key2_')
        sep2 = '='
        val2 = self.get_random_string('val2_')

        # Contains 6 lines total (starts with blank line!)
        fake_data_src = [
            '',
            f'{comment1_marker} {comment1_value}',
            f'{key1} {sep1} {val1}',
            '',
            f'{comment2_marker} {comment2_value}',
            f'{key2} {sep2} {val2}',
        ]

        with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))) as pm:
            # Lie our fake file exists
            path_mock.return_value = True
            prop_file = PropFile(Config(), Path('foo'))
            self.assertEqual(len(fake_data_src), len(prop_file.items))

            idx = 0

            item = prop_file.items[idx]
            self.assertBlank(item)
            idx += 1

            item = prop_file.items[idx]
            self.assertComment(item, comment1_marker, comment1_value)
            idx += 1

            item = prop_file.items[idx]
            self.assertTranslation(item, key1, sep1, val1)
            idx += 1

            item = prop_file.items[idx]
            self.assertBlank(item)
            idx += 1

            item = prop_file.items[idx]
            self.assertComment(item, comment2_marker, comment2_value)
            self.assertIsNone(item.key)
            idx += 1

            item = prop_file.items[idx]
            self.assertTranslation(item, key2, sep2, val2)
            idx += 1

    def assertTranslation(self, translation, exp_key, exp_separator, exp_value):
        self.assertIsInstance(translation, Translation)
        self.assertEqual(exp_key, translation.key)
        self.assertEqual(exp_separator, translation.separator)
        self.assertEqual(exp_value, translation.value)

    def assertComment(self, comment, exp_marker, exp_value):
        self.assertIsInstance(comment, Comment)
        self.assertEqual(f'{exp_marker} {exp_value}', comment.value)
        self.assertIsNone(comment.key)

    def assertBlank(self, blank):
        self.assertIsInstance(blank, Blank)
        self.assertIsNone(blank.key)
        self.assertIsNone(blank.value)
