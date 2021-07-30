"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import copy
import random
import sys
from pathlib import Path
from typing import List, Union
from unittest.mock import Mock, call, patch

from proptool.config.config import Config
from proptool.config.config_builder import ConfigBuilder
from proptool.utils import Utils
from tests.test_case import TestCase


class FakeArgs(object):
    def __init__(self):
        self.update: bool = False
        self.quiet: bool = False
        self.color: bool = False

        self.files: List[str] = []
        self.languages: List[str] = []
        self.separator: Union[str, None] = None
        self.comment_marker: Union[str, None] = None
        self.comment_template: Union[str, None] = None

        # Initialize all on/off flags related attributes.
        for option_name in ConfigBuilder._on_off_pairs:
            self.__setattr__(option_name, False)
            self.__setattr__(f'no_{option_name}', False)


class TestConfigBuilder(TestCase):
    def get_config_for_validate(self) -> Config:
        """
        Prepares instance of Config to be later manipulated and passed
        to ConfigBuilder._validate_config() for tests.

        :return: Initialized config object with valid default state.
        """
        config = Config()

        irrelevant_path = self.get_random_string()
        config.files = [Path(irrelevant_path)]
        config.languages = ['pl']
        config.separator = Config.ALLOWED_SEPARATORS[0]
        config.comment_marker = Config.ALLOWED_COMMENT_MARKERS[0]

        return config

    def test_validate(self) -> None:
        """
        Ensures valid Config instance passes all validation checks.
        """
        ConfigBuilder._validate_config(self.get_config_for_validate())

    @patch('proptool.log.Log.e')
    def test_validate_no_files(self, log_e_mock: Mock) -> None:
        """
        Ensures empty list of files triggers expected error message and quits.

        :param log_e_mock: Log.abort() mock.
        """
        config = self.get_config_for_validate()
        config.files = []
        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_config(config)
            exp_calls = [call('No base file(s) specified.')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_no_languages(self, log_e_mock: Mock) -> None:
        """
        Ensures empty language list triggers expected error message and quits.

        :param log_e_mock: Log.abort() mock.
        """
        config = self.get_config_for_validate()
        config.languages = []
        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_config(config)
            exp_calls = [call('No language(s) specified.')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_invalid_separator(self, log_e_mock: Mock) -> None:
        """
        Ensures invalid separator char triggers expected error message and quits.

        :param log_e_mock: Log.abort() mock.
        """
        config = self.get_config_for_validate()
        config.separator = 'invalid'
        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_config(config)
            exp_calls = [call('Invalid separator character.')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_invalid_comment_marker(self, log_e_mock: Mock) -> None:
        """
        Ensures invalid comment marker triggers expected error message and quits.

        :param log_e_mock: Log.abort() mock.
        """
        config = self.get_config_for_validate()
        config.comment_marker = ''
        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_config(config)
            exp_prints = [call('Invalid comment marker.')]
            log_e_mock.assert_has_calls(exp_prints)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    # #################################################################################################

    def test_set_on_off_option(self) -> None:
        """Tests if _set_on_off_option() works as documented."""
        config = Config()
        config.color = True

        self.assertTrue(config.color)
        args = FakeArgs()
        args.color = False
        args.no_color = True
        ConfigBuilder._set_on_off_option(config, args, 'color')
        self.assertFalse(config.color)

        args.color = True
        args.no_color = False
        ConfigBuilder._set_on_off_option(config, args, 'color')
        self.assertTrue(config.color)

    # #################################################################################################

    def get_expectation(self, config_default: bool, switch_on: bool, switch_off: bool) -> bool:
        """
        Computes expected final value based on on/off switches.

        :param config_default: default option value read from default Config instance.
        :param switch_on: state of --<OPTION> switch
        :param switch_off: state of --no-<OPTION> switch

        :return: Computer boolean value given configuration of on/off switches should produce.
        """
        result = config_default
        if switch_on:
            result = True
        elif switch_off:
            result = False
        return result

    def test_set_from_args(self) -> None:
        """
        Tests _set_from_args()
        """
        args = FakeArgs()

        # Lets set up args to some random state
        args.update = self.get_random_bool()
        args.quiet = self.get_random_bool()
        args.verbose = self.get_random_bool()
        args.color = self.get_random_bool()
        args.fatal, args.no_fatal = self.get_random_on_off_pair()
        args.strict, args.no_strict = self.get_random_on_off_pair()
        args.color, args.no_color = self.get_random_on_off_pair()
        args.separator = random.choice(Config.ALLOWED_SEPARATORS)
        args.comment_marker = random.choice(Config.ALLOWED_COMMENT_MARKERS)

        # Generate fake file names with expected default suffix
        args.files = [Path(f'{self.get_random_string()}{Config.DEFAULT_FILE_SUFFIX}') for _ in range(1, 10)]

        # some languages
        # FIXME: make list more random
        languages = ['pl', 'de', 'pt']
        args.languages = languages

        # This is going to be our reference default config instance.
        config_defaults = Config()

        # Process args and update config
        config = Config()
        ConfigBuilder._set_from_args(config, args)

        # Ensure config reflects changes from command line
        exp_fatal = self.get_expectation(config_defaults.fatal, args.fatal, args.no_fatal)
        self.assertEqual(exp_fatal, config.fatal)
        exp_color = self.get_expectation(config_defaults.color, args.color, args.no_color)
        self.assertEqual(exp_color, config.color)

        # log_level controlled by `quiet` and `verbose`.
        self.assertEqual(args.quiet, config.quiet)
        self.assertEqual(args.verbose, config.verbose)

        # Ensure all files are there and still with proper suffix.
        for idx, args_file in enumerate(args.files):
            self.assertEqual(config.files[idx], args_file)
        self.assertEqual(languages, config.languages)
        self.assertEqual(args.separator, config.separator)
        self.assertEqual(args.comment_marker, config.comment_marker)

    # #################################################################################################

    def test_add_file_suffix_missing_suffix(self) -> None:
        """
        Tests ConfigBuilder._add_file_suffix() works as expected.
        """
        config = Config()

        # GIVEN list of file names WITHOUT expected suffix.
        srcs = [Path(self.get_random_string()) for _ in range(1, 10)]
        dests = copy.copy(srcs)
        # WHEN we process it
        ConfigBuilder._add_file_suffix(config, dests)
        # THEN all file names should have file suffix appened.
        for idx, src in enumerate(srcs):
            self.assertEqual(f'{str(src)}{config.file_suffix}', str(dests[idx]))

    def test_add_file_suffix_with_suffix(self) -> None:
        config = Config()

        # GIVEN list of file names with expected suffix suffix
        srcs = [Path(f'{self.get_random_string()}{config.file_suffix}') for _ in range(1, 10)]
        dests = copy.copy(srcs)
        # WHEN we get it processed
        ConfigBuilder._add_file_suffix(config, dests)
        # THEN nothing should change.
        self.assertEqual(srcs, dests)

    # #################################################################################################

    def test_validate_args_onoff_valid_setups(self) -> None:
        for option_name in ConfigBuilder._on_off_pairs:
            args = FakeArgs()
            args.__setattr__(option_name, False)
            args.__setattr__(f'no_{option_name}', False)
            # We expect no problems.
            ConfigBuilder._validate_args(args)

            args.__setattr__(option_name, True)
            args.__setattr__(f'no_{option_name}', False)
            # We expect no problems.
            ConfigBuilder._validate_args(args)

            args.__setattr__(option_name, False)
            args.__setattr__(f'no_{option_name}', True)
            # We expect no problems.
            ConfigBuilder._validate_args(args)

    @patch('proptool.log.Log.e')
    def test_validate_args_onoff_on_on(self, log_e_mock: Mock) -> None:
        for option_name in ConfigBuilder._on_off_pairs:
            args = FakeArgs()
            args.__setattr__(option_name, True)
            args.__setattr__(f'no_{option_name}', True)

            with self.assertRaises(SystemExit) as context_manager:
                ConfigBuilder._validate_args(args)
                # Problems should be reported.
                exp_calls = [call(f'You cannot use "--{option_name}" and "--no-{option_name}" at the same time.')]
                log_e_mock.assert_has_calls(exp_calls)

                # Check we got sys.exit called with non-zero return code
                self.assertEqual(SystemExit, type(context_manager.exception))
                self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_args_quiet_and_verbose(self, log_e_mock: Mock) -> None:
        """
        Ensures use of mutually exclusive --quiet and --verbose is handled correctly.

        :param log_e_mock: Log.abort() mock.
        """
        args = FakeArgs()

        args.quiet = True
        args.verbose = True
        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_args(args)
            exp_calls = [call('You cannot enable "quiet" and "verbose" options both at the same time.')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_args_invalid_separator(self, log_e_mock: Mock) -> None:
        """
        Checks if attempt to use invalid character as separator is correctly handled.

        :param log_e_mock:
        """
        args = FakeArgs()

        separator = self.get_random_string(length = 1)
        self.assertNotIn(separator, Config.ALLOWED_SEPARATORS)
        args.separator = separator

        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_args(args)
            exp_calls = [call(f'Invalid separator. Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_args_invalid_comment_marker(self, log_e_mock: Mock) -> None:
        args = FakeArgs()

        marker = self.get_random_string(length = 1)
        self.assertNotIn(marker, Config.ALLOWED_COMMENT_MARKERS)
        args.comment_marker = marker

        with self.assertRaises(SystemExit) as context_manager:
            ConfigBuilder._validate_args(args)
            exp_calls = [call(f'Invalid comment marker. Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')]
            log_e_mock.assert_has_calls(exp_calls)

            # Check we got sys.exit called with non-zero return code
            self.assertEqual(SystemExit, type(context_manager.exception))
            self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    @patch('proptool.log.Log.e')
    def test_validate_args_missing_literal(self, log_e_mock: Mock) -> None:
        args = FakeArgs()

        for missing_literal in Config.COMMENT_TEMPLATE_LITERALS:
            tmp = copy.copy(Config.COMMENT_TEMPLATE_LITERALS)
            del tmp[tmp.index(missing_literal)]
            args.comment_template = ' '.join(tmp)

            with self.assertRaises(SystemExit) as context_manager:
                ConfigBuilder._validate_args(args)
                exp_calls = [call(f'Missing literal in comment template: "{missing_literal}".')]
                log_e_mock.assert_has_calls(exp_calls)

                # Check we got sys.exit called with non-zero return code
                self.assertEqual(SystemExit, type(context_manager.exception))
                self.assertEquals(Utils.ABORT_RETURN_CODE, context_manager.exception.code)

    # #################################################################################################

    def test_parse_args_returns_all_keys(self) -> None:
        """
        Checks if argparse returned dict contains all the keys we expect to be present while building
        Config instance.
        """
        config = Config()

        # Pass no args for parsing (this is legit as we have config file that can provide what's needed).

        sys.argv[1:] = []  # noqa: WPS362
        args = ConfigBuilder._parse_args()
        for key in config.__dict__:
            self.assertIn(key, args)

    def test_parse_args_returns_no_more_keys(self) -> None:
        """
        Checks if argparse returned keys are all expected and handled by config (no dangling options
        no-one supports).
        """
        config = Config()

        # Pass no args for parsing (this is legit as we have config file that can provide what's needed).
        sys.argv[1:] = []  # noqa: WPS362
        args = vars(ConfigBuilder._parse_args())  # noqa: WPS421

        # Eliminate --no-<KEY> related keys first as these are not mapped directly.
        for pair_key in ConfigBuilder._on_off_pairs:
            del args[f'no_{pair_key}']

        # Remove `show_version` as this is also not mapped.
        # FIXME: this should not be hardcoded here!
        del args['show_version']

        self.assertEqual(len(args), len(config.__dict__))

        for key in args:
            # Ensure key args returns is what is present in Config as well.
            self.assertIn(key, config.__dict__)
