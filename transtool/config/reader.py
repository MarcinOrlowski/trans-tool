"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List

from transtool.config.config import Config
from transtool.log import Log
from transtool.utils import Utils


class ConfigReader(object):
    def __init__(self):
        self.parser = ConfigParser()
        # Prevent keys CaSe from being altered by default implementation.
        self.parser.optionxform = str

    def abort(self, msg: str):
        Log.e(msg)
        Utils.abort()

    def read(self, config: Config, config_file_name: Path) -> Config:
        """
        Reads and **MERGES** configuration parameters read from given configuration INI file.
        Not that certain types (lists, maps/dicts) are MERGED with existing content!

        :param config: Config to merge loaded config file into.
        :param config_file_name: Path to valid config INI file.
        :return: Instance of Config with fields containing
        """
        if not config_file_name.exists():
            self.abort(f'Config file not found: {config_file_name}')

        # noinspection PyBroadException
        try:
            self.parser.read(config_file_name)
        except Exception:
            # noinspection PyUnresolvedReferences
            self.abort(f'Failed parsing config INI file: {config_file_name}')

        # Presence of "trans-tool" section is mandatory.
        main_section = 'trans-tool'
        if not self.parser.has_section(main_section):
            self.abort(f'Missing "{main_section}" section.')

        # Ensure we know how to read this config file.
        config_version = self.parser.getint(main_section, 'version')
        if config_version < Config.VERSION:
            self.abort(f'Old version ({config_version}) of config INI file. Required {Config.VERSION}')

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
        self._merge_if_exists(self.parser, config.checks, main_section, 'checks')

        if config.debug:
            for attr_name in dir(config):
                if attr_name[:2] != '__':
                    print(f'{attr_name}: {getattr(config, attr_name)}')

        # Load checker's configs
        for checker_id, checker_info in config.checks.items():
            if self.parser.has_section(checker_id):
                checker = checker_info.callable(checker_info.config)
                checker.load_config_ini(checker_info.config, self.parser, checker_id)

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
