"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import configparser
import json
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List

from proptool.config.config import Config
from proptool.log import Log
from proptool.utils import Utils


class ConfigReader(object):
    def read(self, config: Config, config_file_name: Path) -> Config:
        """
        Reads and **MERGES** configuration parameters read from given configuration INI file.
        Not that certain types (lists, maps/dicts) are MERGED with existing content!

        :param config: Config to merge loaded config file into.
        :param config_file_name: Path to valid config INI file.
        :return: Instance of Config with fields containing
        """
        # config_file_name = os.path.normpath(config_file_name)
        # config_file_name_full = os.path.expanduser(config_file_name)

        if not config_file_name.exists():
            Log.abort(f'Config file not found {config_file_name}')

        parser = configparser.ConfigParser()
        # Prevent keys CaSe from being altered by default implementation.
        parser.optionxform = str

        # noinspection PyBroadException
        try:
            parser.read(config_file_name)
        except:
            # noinspection PyUnresolvedReferences
            Log.abort(f'Failed parsing config INI file: {config_file_name}')

        # Presence of "prop-tool" section is mandatory.
        main_section = 'prop-tool'
        if not parser.has_section(main_section):
            Log.abort(f'Missing "{main_section}" section.')

        # Ensure we know how to read this config file.
        config_version = parser.getint(main_section, 'version')
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
            if parser.has_option(main_section, single_bool):
                config.__setattr__(single_bool, parser.get(main_section, single_bool))

        config.files = self._merge_if_exists(parser, config.files, main_section, 'files')
        config.languages = self._merge_if_exists(parser, config.languages, main_section, 'languages')

        if config.debug:
            for attr_name in dir(config):
                if attr_name[:2] != '__':
                    print(f'{attr_name}: {getattr(config, attr_name)}')

        return config

    # #################################################################################################

    def _merge_if_exists(self, config: ConfigParser, merge_into: List[str], config_section: str, config_option: str) -> List[str]:
        if config.has_option(config_section, config_option):
            return self._merge_list(merge_into, config_section, config_option)
        else:
            return merge_into

    def _merge_list(self, merge_into: List[str], config_section: str, config_option: str) -> List[str]:
        result = merge_into
        if self.parser.has_option(config_section, config_option):
            val = self.parser.get(config_section, config_option).replace('\n', '')
            new_list = json.loads(val)
            if new_list is not None:
                _ = [Utils.add_if_not_in_list(result, Utils.remove_quotes(i)) for i in new_list]

        return result

    # ***************************************************************************

    def __merge_dict(self, old_dict: Dict, ini_parser: ConfigParser, section: str) -> Dict:
        result = old_dict

        if ini_parser.has_section(section):
            new_dict = dict(ini_parser.items(section))
            if new_dict is None:
                return result

            for k, v in new_dict.items():
                v = Utils.remove_quotes(v)

                # if key starts with "DEL " then value does not matter and such key is REMOVED from internal storage
                if k[0:4] == 'DEL ':
                    key = k[4:]
                    if key in result:
                        if not section_name_shown:
                            # Log.level_push('%%yellow_bright%%**WARN**%r map' % section)
                            section_name_shown = True
                        del result[key]
                    continue

                if k in old_dict and result[k] != v:
                    if not section_name_shown:
                        # Log.level_push('%%yellow_bright%%**WARN**%r map' % section)
                        section_name_shown = True
                result[k] = v

        return result

    # #################################################################################################

    def __sanitize_dict(self, src_dict: Dict) -> Dict:
        import collections

        tmp = collections.OrderedDict()
        for (k, v) in src_dict.items():
            tmp[Utils.remove_quotes(k)] = Utils.remove_quotes(v)
        return tmp
