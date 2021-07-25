"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.config.config_builder import ConfigBuilder
from proptool.config.config import Config
from tests.test_case import TestCase


class TestConfigBuilder(TestCase):

    def test_set_on_off_option(self) -> None:
        class FakeArgs(Config):
            def __init__(self):
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
