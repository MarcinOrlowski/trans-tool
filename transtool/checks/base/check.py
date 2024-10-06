"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2024 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import json
from abc import ABC, abstractmethod
from configparser import ConfigParser
from typing import Dict, List, Union, Optional

from transtool.report.report import Report
from transtool.prop.items import Translation, Comment, PropItem


# noinspection PyUnresolvedReferences
class Check(ABC):
    """
    Abstract base class for implementing checks on translation and reference PropFile objects.
    Provides methods for configuring checks, validating input, and determining whether to skip certain items.
    """

    DEFAULT_CHECK_CONFIG = {}

    def __init__(self, config: Optional[Dict] = None):
        if config is not None:
            if not isinstance(config, Dict):
                raise ValueError(f'Configuration object must be instance of Dict ("{type(config)}" given).')
        self.config = config

        self.is_single_file_check = False

    @abstractmethod
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: Optional['PropFile'] = None) -> Report:
        """
        Abstract method for performing check on translation PropFile with optional reference PropFile.
        :param translation: PropFile object containing translations to be checked.
        :param reference: Optional PropFile object to be used as reference.
        :return: Report object containing results of the check.
        """
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

    def need_both_files(self, translation: 'PropFile', reference: Optional['PropFile']) -> None:
        """
        Validates that both translation and reference are valid PropFile objects.
        :param translation: PropFile object containing translations.
        :param reference: PropFile object to be used as reference.
        """
        if translation is None:
            raise ValueError(f'Translation must be valid PropFile object ({type(translation)} given).')
        if reference is None:
            raise ValueError(f'Reference must be valid PropFile object ({type(reference)} given).')

    def need_valid_config(self) -> None:
        """
        Validates that the current configuration is a valid Dict object.
        """
        if not isinstance(self.config, Dict):
            raise ValueError(f'Configuration object must be instance of Dict ("{type(self.config)}" given).')

    def get_default_config(self) -> Dict:
        """
        Retrieves the default configuration for the check.
        :return: Dict object containing the default configuration.
        """
        return Check.DEFAULT_CHECK_CONFIG

    def load_config_ini(self, config: Dict, parser: ConfigParser, config_section: str) -> None:
        """
        Loads configuration options from an INI file into the specified config Dict.
        :param config: Dict object to populate with configuration options.
        :param parser: ConfigParser object used to read the INI file.
        :param config_section: String specifying the section of the INI file to read.
        """
        self._set_config_option(config, parser, config_section, self.config)

    def _set_config_option(self, config: Dict, parser: ConfigParser, config_section: str,
                           options: Union[List[str], str]) -> None:
        """
        Sets specified configuration options in the provided config Dict based on values in the INI file.
        :param config: Dict object to populate with configuration options.
        :param parser: ConfigParser object used to read the INI file.
        :param config_section: String specifying the section of the INI file to read.
        :param options: List of strings or single string specifying the options to set in the config.
        """
        if isinstance(options, str):
            options = [options]

        for option in options:
            if parser.has_option(config_section, option):
                config[option] = json.loads(parser.get(config_section, option).replace('\n', ''))
