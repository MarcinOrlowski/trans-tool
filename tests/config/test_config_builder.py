"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from pathlib import Path
from unittest.mock import call, patch

from proptool.config.config import Config
from proptool.config.config_builder import ConfigBuilder
from tests.test_case import TestCase


class TestConfigBuilder(TestCase):

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
        ConfigBuilder._validate(self.get_config_for_validate())

    @patch('proptool.log.Log.abort')
    def test_validate_no_files(self, mock_log_abort) -> None:
        config = self.get_config_for_validate()
        config.files = []
        ConfigBuilder._validate(config)
        exp_calls = [call('No base file(s) specified.')]
        mock_log_abort.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_no_languages(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.languages = []
        ConfigBuilder._validate(config)
        exp_calls = [call('No language(s) specified.')]
        mock_print.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_invalid_separator(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.separator = ''
        ConfigBuilder._validate(config)
        exp_calls = [call('Invalid separator character.')]
        mock_print.assert_has_calls(exp_calls)

    @patch('proptool.log.Log.abort')
    def test_validate_invalid_comment_marker(self, mock_print) -> None:
        config = self.get_config_for_validate()
        config.comment_marker = ''
        ConfigBuilder._validate(config)
        exp_prints = [call('Invalid comment marker.')]
        mock_print.assert_has_calls(exp_prints)

    # #################################################################################################

    def test_set_on_off_option(self) -> None:
        class FakeArgs(Config):
            def __init__(self):
                super().__init__()
                self.option = False
                self.no_option = True

        config = Config()
        config.option = True
        self.assertTrue(config.option)
        args = FakeArgs()
        ConfigBuilder._set_on_off_option(config, args, 'option')
        self.assertFalse(config.option)

        args.option = True
        args.no_option = False
        ConfigBuilder._set_on_off_option(config, args, 'option')
        self.assertTrue(config.option)
