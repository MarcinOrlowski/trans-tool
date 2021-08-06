"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import json
from abc import ABC, abstractmethod
from configparser import ConfigParser
from typing import Dict, List, Union

from transtool.report.report import Report
from transtool.prop.items import Translation, Comment, PropItem


# noinspection PyUnresolvedReferences
class Check(ABC):
    DEFAULT_CHECK_CONFIG = {}

    def __init__(self, config: Union[Dict, None] = None):
        if config is not None:
            if not isinstance(config, Dict):
                raise ValueError(f'Configuration object must be instance of Dict ("{type(config)}" given).')
        self.config = config

        self.is_single_file_check = False

    @abstractmethod
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: Union['PropFile', None] = None) -> Report:
        raise NotImplementedError

    def _shall_skip_item(self, item: PropItem) -> bool:
        """
        Returns True if item is a Translation OR is a Comment, but checker's config "comments" option is True
        :param item: instance of PropItem
        :return:
        """
        if not issubclass(type(item), PropItem):
            raise TypeError('Item should be subclass of PropItem.')

        return not (isinstance(item, Translation) or (isinstance(item, Comment) and self.config['comments']))

    def need_both_files(self, translation: 'PropFile', reference: Union['PropFile', None]) -> None:
        if translation is None:
            raise ValueError(f'Translation must be valid PropFile object ({type(translation)} given).')
        if reference is None:
            raise ValueError(f'Reference must be valid PropFile object ({type(reference)} given).')

    def need_valid_config(self) -> None:
        if not isinstance(self.config, Dict):
            raise ValueError(f'Configuration object must be instance of Dict ("{type(self.config)}" given).')

    def get_default_config(self) -> Dict:
        return Check.DEFAULT_CHECK_CONFIG

    def load_config_ini(self, config: Dict, parser: ConfigParser, config_section: str) -> None:
        self._set_config_option(config, parser, config_section, self.config)

    def _set_config_option(self, config: Dict, parser: ConfigParser, config_section: str, options: Union[List[str], str]) -> None:
        if isinstance(options, str):
            options = [options]

        for option in options:
            if parser.has_option(config_section, option):
                config[option] = json.loads(parser.get(config_section, option).replace('\n', ''))
