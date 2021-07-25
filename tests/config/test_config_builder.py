"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import argparse
import copy
from pathlib import Path
from typing import List, Union
from unittest.mock import call, patch

from proptool.config.config import Config
from proptool.config.config_builder import ConfigBuilder
from tests.test_case import TestCase


class TestConfigBuilder(TestCase):

    class FakeArgs(object):
        def __init__(self):
            self.fix: bool = False

            self.files: List[str] = []
            self.languages: List[str] = []
            self.separator: Union[str, None] = None
            self.comment_marker: Union[str, None] = None
            self.comment_template: Union[str, None] = None

            # Initialize all on/off flags related attributes.
            for option_name in ConfigBuilder._on_off_pairs:
                self.__setattr__(option_name, False)
                self.__setattr__(f'no_{option_name}', False)

    def get_config_for_validate(self) -> Config:
        config = Config()

        irrelevant_path = self.get_random_string()
        config.files = [Path(irrelevant_path)]
        config.languages = ['pl']
        config.separator = Config.ALLOWED_SEPARATORS[0]
        config.comment_marker = Config.ALLOWED_COMMENT_MARKERS[0]

        return config

    def test_validate(self) -> None:
        # This one should pass
        ConfigBuilder._validate_config(self.get_config_for_validate())

    @patch('proptool.log.Log.abort')
    def test_validate_no_files(self, mock_log_abort) -> None:
        config = self.get_config_for_validate()
        config.files = []
        ConfigBuilder._validate_config(config)
        exp_calls = [call('No base file(s) specified.')]
        mock_log_abort.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_no_languages(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.languages = []
        ConfigBuilder._validate_config(config)
        exp_calls = [call('No language(s) specified.')]
        mock_print.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_invalid_separator(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.separator = ''
        ConfigBuilder._validate_config(config)
        exp_calls = [call('Invalid separator character.')]
        mock_print.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_invalid_comment_marker(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.comment_marker = ''
        ConfigBuilder._validate_config(config)
        exp_prints = [call('Invalid comment marker.')]
        mock_print.assert_has_calls(exp_prints)

    # #################################################################################################

    def test_set_on_off_option(self) -> None:
        config = Config()
        config.verbose = True

        self.assertTrue(config.verbose)
        args = TestConfigBuilder.FakeArgs()
        args.verbose = False
        args.no_verbose = True
        ConfigBuilder._set_on_off_option(config, args, 'verbose')
        self.assertFalse(config.verbose)

        args.verbose = True
        args.no_verbose = False
        ConfigBuilder._set_on_off_option(config, args, 'verbose')
        self.assertTrue(config.verbose)

    # #################################################################################################

    def get_expectation(self, config_default: bool, switch_on: bool, switch_off: bool) -> bool:
        result = config_default
        if switch_on:
            result = True
        elif switch_off:
            result = False
        return result

    def test_set_from_args(self) -> None:
        class FakeArgs(object):
            def __init__(self):
                self.fix: bool = False

                self.files: List[str] = []
                self.languages: List[str] = []
                self.separator: Union[str, None] = None
                self.comment_marker: Union[str, None] = None
                self.comment_template: Union[str, None] = None

                # Initialize all on/off flags related attributes.
                for option_name in ConfigBuilder._on_off_pairs:
                    self.__setattr__(option_name, False)
                    self.__setattr__(f'no_{option_name}', False)

        args = FakeArgs()
        args.fix = self.get_random_bool()

        args.fatal, args.no_fatal = self.get_random_on_off_pair()
        args.strict, args.no_strict = self.get_random_on_off_pair()
        args.quiet, args.no_quiet = self.get_random_on_off_pair()
        args.verbose, args.no_verbose = self.get_random_on_off_pair()
        args.color, args.no_color = self.get_random_on_off_pair()

        # Generate some names with .properties suffix
        args.files = [Path(f'{self.get_random_string()}.properties') for _ in range(1, 10)]

        config_defaults = Config()
        config = Config()
        ConfigBuilder._set_from_args(config, args)

        # Ensure config reflects changes from command line
        exp_fatal = self.get_expectation(config_defaults.fatal, args.fatal, args.no_fatal)
        self.assertEqual(exp_fatal, config.fatal)
        exp_strict = self.get_expectation(config_defaults.strict, args.strict, args.no_strict)
        self.assertEqual(exp_strict, config.strict)
        exp_quiet = self.get_expectation(config_defaults.quiet, args.quiet, args.no_quiet)
        self.assertEqual(exp_quiet, config.quiet)
        exp_verbose = self.get_expectation(config_defaults.verbose, args.verbose, args.no_verbose)
        self.assertEqual(exp_verbose, config.verbose)
        exp_color = self.get_expectation(config_defaults.color, args.color, args.no_color)
        self.assertEqual(exp_color, config.color)

        # ensure all files are now with proper suffix
        for idx, args_file in enumerate(args.files):
            self.assertEqual(config.files[idx], args_file)

    # #################################################################################################

    def test_add_file_suffix_missing_suffix(self) -> None:
        config = Config()

        # Generate some names with NO ".properties" suffix
        srcs = [Path(self.get_random_string()) for _ in range(1, 10)]
        dests = copy.copy(srcs)
        ConfigBuilder._add_file_suffix(config, dests)
        # Ensure nothing we got suffix added
        for idx, src in enumerate(srcs):
            self.assertEqual(f'{str(src)}{config.file_suffix}', str(dests[idx]))

    def test_add_file_suffix_with_suffix(self) -> None:
        config = Config()

        # Generate some names with ".properties" suffix
        srcs = [Path(f'{self.get_random_string()}{config.file_suffix}') for _ in range(1, 10)]
        dests = copy.copy(srcs)
        ConfigBuilder._add_file_suffix(config, dests)
        # Ensure nothing gets altered
        self.assertEqual(srcs, dests)
