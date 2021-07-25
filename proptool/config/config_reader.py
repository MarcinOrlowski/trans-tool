"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List

from proptool.config.config import Config
from proptool.log import Log
from proptool.utils import Utils


class ConfigReader(object):
    def __init__(self):
        self.parser = ConfigParser()
        # Prevent keys CaSe from being altered by default implementation.
        self.parser.optionxform = str

    def read(self, config: Config, config_file_name: Path) -> Config:
        """
        Reads and **MERGES** configuration parameters read from given configuration INI file.
        Not that certain types (lists, maps/dicts) are MERGED with existing content!

        :param config: Config to merge loaded config file into.
        :param config_file_name: Path to valid config INI file.
        :return: Instance of Config with fields containing
        """
        if not config_file_name.exists():
            Log.abort(f'Config file not found {config_file_name}')

        # noinspection PyBroadException
        try:
            self.parser.read(config_file_name)
        except Exception:
            # noinspection PyUnresolvedReferences
            Log.abort(f'Failed parsing config INI file: {config_file_name}')

        # Presence of "prop-tool" section is mandatory.
        main_section = 'prop-tool'
        if not self.parser.has_section(main_section):
            Log.abort(f'Missing "{main_section}" section.')

        # Ensure we know how to read this config file.
        config_version = self.parser.getint(main_section, 'version')
        if config_version < Config.VERSION:
            Log.abort(f'Old version ({config_version}) of config INI file. Required {Config.VERSION}')

        bools = [
            'debug',
            'fatal',
            'color',
            'quiet',
            'strict',
            'verbose',
        ]
        for single_bool in bools:
            if self.parser.has_option(main_section, single_bool):
                config.__setattr__(single_bool, self.parser.get(main_section, single_bool))

        self._merge_if_exists(self.parser, config.files, main_section, 'files')
        self._merge_if_exists(self.parser, config.languages, main_section, 'languages')

        if config.debug:
            for attr_name in dir(config):
                if attr_name[:2] != '__':
                    print(f'{attr_name}: {getattr(config, attr_name)}')

        return config

    # #################################################################################################

    def _merge_if_exists(self, parser: ConfigParser, target_list: List[str], config_section: str, config_option: str) -> None:
        if parser.has_option(config_section, config_option):
            self._merge_list(target_list, parser, config_section, config_option)

    def _merge_list(self, target_list, parser: ConfigParser, section: str, option: str) -> None:
        if parser.has_option(section, option):
            import json
            new_list = json.loads(parser.get(section, option).replace('\n', ''))
            Utils.add_if_not_in_list(target_list, Utils.remove_quotes(new_list))

    # #################################################################################################

    def _merge_dict(self, old_dict: Dict, ini_parser: ConfigParser, section: str):
        if ini_parser.has_section(section):
            new_dict = dict(ini_parser.items(section))
            if new_dict is None:
                return
            for key, value in new_dict.items():
                old_dict[key] = Utils.remove_quotes(value)
