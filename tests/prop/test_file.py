"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import random
from pathlib import Path
from unittest.mock import Mock, call, mock_open, patch

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
    def test_load_non_existing_file(self, path_exists_mock: Mock) -> None:
        """
        Tests if load() parses source file properly.

        :param path_exists_mock: Mocked Path
        """
        prop_file = PropFile(Config())

        path_exists_mock.return_value = False
        prop_file.load(Path('foo'))

    @patch('pathlib.Path.exists')
    def test_load_strip_crlf(self, path_exists_mock: Mock) -> None:
        """
        Ensures trailing LF and CRLFs are properly stripped from read lines.

        :param path_exists_mock: Mocked Path
        """

        com0 = self.get_random_string()
        com1 = self.get_random_string()

        for sep in Config.ALLOWED_COMMENT_MARKERS:
            for key_val_sep in Config.ALLOWED_SEPARATORS:
                key1 = self.get_random_string()
                val1 = self.get_random_string()
                val2 = self.get_random_string()
                fake_data_src = [
                    f'{sep} {com0}\n',
                    f'{sep} {com1}\r\n',
                    f'{key1} {key_val_sep} {val1}\n',
                    # This one should overwrite previous row
                    f'{key1} {key_val_sep} {val2}\r\n',
                ]

                with patch('builtins.open', mock_open(read_data = ''.join(fake_data_src))) as pm:
                    # Lie our fake file exists
                    path_exists_mock.return_value = True
                    prop_file = PropFile(Config(), Path('foo'))

                    # We should have one entry less, because once we strip CRLF from the last
                    # row, it should overwrite entry set row before.
                    self.assertEqual(len(fake_data_src) - 1, len(prop_file.items))

                    # Let's inspect what we have.
                    idx = 0

                    # Line 0
                    item = prop_file.items[idx]
                    self.assertIsInstance(item, Comment)
                    self.assertEqual(f'{sep} {com0}', item.value)
                    idx += 1

                    # Line 1
                    item = prop_file.items[idx]
                    self.assertIsInstance(item, Comment)
                    self.assertEqual(f'{sep} {com1}', item.value)
                    idx += 1

                    # Line 2
                    item = prop_file.items[idx]
                    self.assertIsInstance(item, Translation)
                    self.assertEqual(key1, item.key)
                    # We have duplicated key. It's not overwritten row. Please see other code comments.
                    self.assertEqual(val1, item.value)
                    idx += 1


    @patch('pathlib.Path.exists')
    def test_load_empty_lines_whitespaces(self, path_exists_mock: Mock) -> None:
        """
        Ensures lines with all whitespaces are correctly parsed as Blank()s

        :param path_exists_mock: Mocked Path
        """
        fake_data_src = [
            '',
            '     ',
            '\t\t\t\t',
            '\t\t\t   \t\t\t'
        ]
        with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))) as pm:
            # Lie our fake file exists
            path_exists_mock.return_value = True
            prop_file = PropFile(Config(), Path('foo'))
            self.assertEqual(len(fake_data_src), len(prop_file.items))

            for item in prop_file.items:
                self.assertIsInstance(item, Blank)

    @patch('pathlib.Path.exists')
    def test_load_empty_file(self, path_exists_mock: Mock) -> None:
        """
        Checks if empty file is not too confusing.
        """
        fake_file = f'/tmp/{self.get_random_string()}'
        with patch('builtins.open', mock_open(read_data = '')):
            # Lie our fake file exists
            path_exists_mock.return_value = True
            prop_file = PropFile(Config(), Path(fake_file))
            self.assertEqual(0, len(prop_file.items))

    @patch('builtins.print')  # Needed only to mute error message during unit tests.
    def test_load_invalid_translation_syntax(self, path_mock: Mock) -> None:
        """
        Ensures lines that are expected to be translation but do not match expected syntax
        are caught correctly.

        :param path_mock: Mocked Path
        """

        fake_file = f'/tmp/{self.get_random_string()}'

        # Generate some valid content
        fake_data_src = []
        # I could use list comprehension but cannot guarantee key uniqueness that way. I need unique prefix.
        for idx in range(random.randint(10, 30)):
            fake_data_src.append(f'key{idx}_{self.get_random_string()} {Config.ALLOWED_SEPARATORS[0]} {self.get_random_string()}')

        # Insert incorrect syntax at random line
        trap_position = random.randint(0, len(fake_data_src) - 1)
        fake_data_src.insert(trap_position, 'WRONG SYNTAX')

        with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))) as pm:
            # Lie our fake file exists
            path_mock.return_value = True
            prop_file = PropFile(Config(), Path(fake_file))
            self.assertEqual(0, len(prop_file.items))

    @patch('pathlib.Path.exists')
    def test_load_valid_file(self, path_mock: Mock) -> None:
        """
        Tests if load() parses valid source *.properties file correctly.

        :param path_mock: Mocked Path
        """

        def assertTranslation(translation, exp_key, exp_separator, exp_value):
            self.assertIsInstance(translation, Translation)
            self.assertEqual(exp_key, translation.key)
            self.assertEqual(exp_separator, translation.separator)
            self.assertEqual(exp_value, translation.value)

        def assertComment(comment, exp_marker, exp_value):
            self.assertIsInstance(comment, Comment)
            self.assertEqual(f'{exp_marker} {exp_value}', comment.value)
            self.assertIsNone(comment.key)

        def assertBlank(blank):
            self.assertIsInstance(blank, Blank)
            self.assertIsNone(blank.key)
            self.assertIsNone(blank.value)

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
            assertBlank(item)
            idx += 1

            item = prop_file.items[idx]
            assertComment(item, comment1_marker, comment1_value)
            idx += 1

            item = prop_file.items[idx]
            assertTranslation(item, key1, sep1, val1)
            idx += 1

            item = prop_file.items[idx]
            assertBlank(item)
            idx += 1

            item = prop_file.items[idx]
            assertComment(item, comment2_marker, comment2_value)
            self.assertIsNone(item.key)
            idx += 1

            item = prop_file.items[idx]
            assertTranslation(item, key2, sep2, val2)
            idx += 1
