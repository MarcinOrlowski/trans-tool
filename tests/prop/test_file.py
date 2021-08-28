"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import copy
import random
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from transtool.config.builder import ConfigBuilder
from transtool.config.config import Config
from transtool.prop.file import PropFile
from transtool.prop.items import Blank, Comment, PropItem, Translation
from tests.test_case import TestCase


class TestPropFile(TestCase):

    def _generate_propfile_with_content(self, config: Config) -> PropFile:
        """
        Creates instance of PropFile and fills it with randonly generated content.
        :param config: Config to be used while constructing instance.
        """
        propfile = PropFile(config)

        item_types = [Blank, Comment, Translation]
        item_weights = [2, 5, 10]
        new_items = 50
        for new_item_cls in random.choices(item_types, item_weights, k = new_items):
            if issubclass(new_item_cls, Translation):
                key = self.get_random_string('key')
                val = self.get_random_string('ref_val')
                propfile.append(Translation(key, val))
            elif issubclass(new_item_cls, Comment):
                propfile.append(Comment(self.get_random_string('comment')))
            elif issubclass(new_item_cls, Blank):
                propfile.append(Blank())
            else:
                self.fail(f'Unknown new_item_cls: {type(new_item_cls)}')

        return propfile

    # #################################################################################################

    def test_append_wrong_arg_type(self) -> None:
        # GIVEN normal instance of PropFile
        propfile = PropFile(Config())

        # WHEN we try to append object of unsupported type
        obj = 'INVALID'

        # THEN Exception should be thrown.
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            propfile.append(obj)

    def test_append_list_of_wrong_arg_type(self) -> None:
        # GIVEN normal instance of PropFile
        propfile = PropFile(Config())

        # WHEN we try to append list of object of unsupported type
        obj = ['INVALID']

        # THEN Exception should be thrown.
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            propfile.append(obj)

    # #################################################################################################

    def test_load_non_existing_file(self) -> None:
        """
        Tests if load() fails on non-existing file correctly.
        """
        file_name = self.get_random_string()
        propfile = PropFile(Config())
        with self.assertRaises(Exception) as cm:
            propfile.load(Path(file_name))
            self.assertEqual(FileNotFoundError, type(cm.exception))

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

                with patch('builtins.open', mock_open(read_data = ''.join(fake_data_src))):
                    # Lie our fake file exists
                    path_exists_mock.return_value = True
                    propfile = PropFile(Config())
                    propfile.load(Path('foo'))

                    # We should have one entry less, because once we strip CRLF from the last
                    # row, it should overwrite entry set row before.
                    self.assertEqual(len(fake_data_src) - 1, len(propfile.items))

                    # Let's inspect what we have.
                    idx = 0

                    # Line 0
                    item = propfile.items[idx]
                    self.assertIsInstance(item, Comment)
                    self.assertEqual(f'{sep} {com0}', item.value)
                    idx += 1

                    # Line 1
                    item = propfile.items[idx]
                    self.assertIsInstance(item, Comment)
                    self.assertEqual(f'{sep} {com1}', item.value)
                    idx += 1

                    # Line 2
                    item = propfile.items[idx]
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
            '\t\t\t   \t\t\t',
        ]
        with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))):
            # Lie our fake file exists
            path_exists_mock.return_value = True
            propfile = PropFile(Config())
            propfile.load(Path('foo'))
            self.assertEqual(len(fake_data_src), len(propfile.items))

            for item in propfile.items:
                self.assertIsInstance(item, Blank)

    @patch('pathlib.Path.exists')
    def test_load_empty_file(self, path_exists_mock: Mock) -> None:
        """
        Checks if empty file is not too confusing.
        """
        fake_file_name = f'/does/not/matter/{self.get_random_string()}'
        with patch('builtins.open', mock_open(read_data = '')):
            # Lie our fake file exists
            path_exists_mock.return_value = True
            propfile = PropFile(Config())
            propfile.load(Path(fake_file_name))
            self.assertEqual(0, len(propfile.items))

    @patch('pathlib.Path.exists')
    def test_load_invalid_translation_syntax(self, path_exists_mock: Mock) -> None:
        """
        Ensures lines that are expected to be translation but do not match expected syntax
        are caught correctly.

        :param path_exists_mock: Mocked Path
        """
        fake_file_name = f'/does/not/matter/{self.get_random_string()}'

        # Fake source file content
        fake_data_src = []
        # I could use list comprehension but cannot guarantee key uniqueness that way. I need unique prefix then.
        max_elements = 30
        for idx in range(random.randint(10, max_elements)):
            fake_data_src.append(f'key{idx}_{self.get_random_string()} {Config.ALLOWED_SEPARATORS[0]} {self.get_random_string()}')

        # # Insert incorrect syntax at random line
        trap_position = random.randint(0, len(fake_data_src) - 1)
        fake_data_src.insert(trap_position, 'WRONG SYNTAX')

        with patch('transtool.log.Log.e') as log_e_mock:
            # Lie our fake file exists
            path_exists_mock.return_value = True

            with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))):
                try:
                    propfile = PropFile(Config())
                    with self.assertRaises(SyntaxError):
                        propfile.load(Path(fake_file_name))
                except SystemExit:
                    # sys.exit() happened after Log.e() is called, so we can check the error message here.
                    msg = log_e_mock.call_args_list[0][0][0]
                    self.assertEqual(msg, f'Invalid syntax at line {trap_position + 1} of "{fake_file_name}".')

    @patch('pathlib.Path.exists')
    def test_load_valid_file(self, path_mock: Mock) -> None:
        """
        Tests if load() parses valid source *.properties file correctly.

        :param path_mock: Mocked Path
        """

        # noinspection PyPep8Naming
        def assertTranslation(translation: PropItem, exp_key, exp_separator, exp_value):
            self.assertIsInstance(translation, Translation)
            self.assertEqual(exp_key, translation.key)
            self.assertEqual(exp_separator, translation.separator)
            self.assertEqual(exp_value, translation.value)

        # noinspection PyPep8Naming
        def assertComment(comment: PropItem, exp_marker, exp_value):
            self.assertIsInstance(comment, Comment)
            self.assertEqual(f'{exp_marker} {exp_value}', comment.value)
            self.assertIsNone(comment.key)

        # noinspection PyPep8Naming
        def assertBlank(blank):
            self.assertIsInstance(blank, Blank)
            self.assertIsNone(blank.key)
            self.assertIsNone(blank.value)

        comment1_marker = '#'
        comment1_value = self.get_random_string('comment')

        key1 = self.get_random_string('key1')
        sep1 = '='
        val1 = self.get_random_string('val1')

        comment2_marker = '!'
        comment2_value = self.get_random_string('comment')

        key2 = self.get_random_string('key2')
        sep2 = '='
        val2 = self.get_random_string('val2')

        fake_data_src = [
            '',
            f'{comment1_marker} {comment1_value}',
            f'{key1} {sep1} {val1}',
            '',
            f'{comment2_marker} {comment2_value}',
            f'{key2} {sep2} {val2}',
        ]

        with patch('builtins.open', mock_open(read_data = '\n'.join(fake_data_src))):
            # Lie our fake file exists
            path_mock.return_value = True
            propfile = PropFile(Config())
            propfile.load(Path('foo'))
            self.assertEqual(len(fake_data_src), len(propfile.items))

            idx = 0

            item = propfile.items[idx]
            assertBlank(item)
            idx += 1

            item = propfile.items[idx]
            assertComment(item, comment1_marker, comment1_value)
            idx += 1

            item = propfile.items[idx]
            assertTranslation(item, key1, sep1, val1)
            idx += 1

            item = propfile.items[idx]
            assertBlank(item)
            idx += 1

            item = propfile.items[idx]
            assertComment(item, comment2_marker, comment2_value)
            self.assertIsNone(item.key)
            idx += 1

            item = propfile.items[idx]
            assertTranslation(item, key2, sep2, val2)
            idx += 1

    # #################################################################################################

    def _check_written_content(self, propfile: PropFile, verify_file_name, save_file_name = None):
        with patch('builtins.open', mock_open()) as manager:
            with patch('transtool.log.Log.i') as log_i_mock:
                if save_file_name:
                    propfile.save(save_file_name)
                else:
                    propfile.save()
                manager.assert_called_once_with(verify_file_name, 'w')

                # Ensure call to Log.i() happened with expected message.
                msg = log_i_mock.call_args_list[0][0][0]
                self.assertEqual(msg, f'Writing: {verify_file_name}')

                # Check file content is written as expected.
                expected = []
                for item in propfile.items:
                    expected.append(item.to_string())

                fh = manager()
                # FIXME: LF/CRLF should configurable
                fh.write.assert_called_once_with('\n'.join(expected))

    def test_save(self) -> None:
        """
        Checks if save() writes proper contents to the file.
        """
        config = Config()
        propfile = self._generate_propfile_with_content(config)

        fake_file_name = Path(self.get_random_string())
        self._check_written_content(propfile, fake_file_name, fake_file_name)

    def test_save_use_property_file(self) -> None:
        """
        Checks save() will use property file as target file name if no
        file name is specified as save() argument.
        """
        config = Config()
        propfile = self._generate_propfile_with_content(config)
        verify_file_name = Path(self.get_random_string())
        propfile.file = verify_file_name
        self._check_written_content(propfile, verify_file_name)

    def test_save_no_target_file(self) -> None:
        """
        Checks if save() will fail if no target file name is given nor object's
        `file` property is `None`.
        :return:
        """
        config = Config()
        propfile = PropFile(config)
        with self.assertRaises(ValueError):
            propfile.save()

    # #################################################################################################

    @patch('pathlib.Path.exists')
    def test_validate_on_empty_files(self, path_exists_mock: Mock) -> None:
        config = Config()
        ConfigBuilder._setup_checkers(config)  # noqa: WPS437

        fake_file = Path(f'/does/not/matter/{self.get_random_string()}')
        with patch('builtins.open', mock_open(read_data = '')):
            # Lie our fake file exists
            path_exists_mock.return_value = True

            ref_file = PropFile(config)
            ref_file.load(fake_file)

            propfile = PropFile(config)
            propfile.load(fake_file)

            # Expecting no problems reported
            propfile.report.dump()
            self.assertTrue(propfile.validate(ref_file))

    @patch('pathlib.Path.exists')
    def test_validate_no_checkers_configured(self, path_exists_mock: Mock) -> None:
        # GIVEN empty config without checkers set up
        config = Config()

        # and GIVEN fake file
        fake_file = Path(f'/does/not/matter/{self.get_random_string()}')
        with patch('builtins.open', mock_open(read_data = '')):
            # Lie our fake file exists
            path_exists_mock.return_value = True
            propfile = PropFile(config)
            propfile.load(fake_file)

            # THEN we expect error raised
            with self.assertRaises(RuntimeError):
                # attempting to validate the file
                propfile.validate(propfile)

    # #################################################################################################

    def test_update(self) -> None:
        config = Config()
        ConfigBuilder._setup_checkers(config)  # noqa: WPS437

        # Generate reference file and its contents
        reference = self._generate_propfile_with_content(config)

        # Generate translation file
        translation = PropFile(config)

        mut_none = 'none'
        mut_com = 'comment-out'
        mutation_items = [mut_none, mut_com]
        mutation_weights = [10, 5]

        mut_com_cnt = 0

        for ref_idx, ref_item in enumerate(reference.items):
            if isinstance(ref_item, Translation):
                mutation = random.choices(mutation_items, mutation_weights, k = 1)[0]
                if mutation == mut_none:
                    translation.append(Translation(ref_item.key, self.get_random_string(f'translation_{ref_idx}')))
                else:
                    # or commented out key
                    translation.append(Comment.get_commented_out_key_comment(config, ref_item.key, ref_item.value))
                    mut_com_cnt += 1
                continue
            translation.append(ref_item)

        self.assertNotEqual(0, mut_com_cnt)

        # Keep the clone of
        translation_clone = copy.deepcopy(translation)

        # Then add some Blanks and Comments that will be gone after the sync.
        max_items = 5
        for _ in range(max_items):
            translation.append([
                Blank(),
                Comment(self.get_random_string('comment')),
            ])

        # THEN after update
        translation.update(reference)

        # we should have synced content
        for ref_idx, ref_item in enumerate(reference.items):  # noqa: WPS440
            trans_item = translation.items[ref_idx]

            if isinstance(ref_item, Blank):
                self.assertEqual(type(trans_item), Blank)
                continue

            if isinstance(ref_item, Comment):
                self.assertEqual(type(trans_item), Comment)
                continue

            if isinstance(ref_item, Translation):
                if isinstance(trans_item, Translation):
                    # FIXME: we shall check the separator too.
                    self.assertEqual(ref_item.key, trans_item.key)
                    self.assertEqual(translation_clone.items[ref_idx].value, trans_item.value)
                    continue
                if isinstance(trans_item, Comment):
                    expected = Comment.comment_out_key(config, ref_item.key, ref_item.value)
                    self.assertEqual(expected, trans_item.to_string())
                    continue

            self.fail(f'Unknown item type: {type(trans_item)}')

    def test_update_fail_on_unknown_type(self) -> None:
        """
        Ensures unexpected and unsupported content will be caught and raise TypeError.
        """
        config = Config()

        # GIVEN Translation and Reference objects
        reference = PropFile(config)
        trans = PropFile(config)

        # When reference contents contain invalid item
        reference.items.append(False)

        # THEN attempt to update() should fail with error raised.
        with self.assertRaises(TypeError):
            trans.update(reference)
