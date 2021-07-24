"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from abc import ABC, abstractmethod
from typing import Dict, Union

from proptool.config.config import Config
from proptool.report.report import Report


# noinspection PyUnresolvedReferences
class Check(ABC):
    DEFAULT_CHECK_CONFIG = {}

    def __init__(self, config: Union[Config, None] = None):
        if config:
            if not isinstance(config, Config):
                raise ValueError(f'Configuration object must be instance of Config ("{type(self.config)}" given).')
        self.config = config

    @abstractmethod
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: Union['PropFile', None] = None) -> Report:
        raise NotImplementedError

    def need_both_files(self, translation: 'PropFile', reference: Union['PropFile', None]) -> None:
        if translation is None:
            raise ValueError(f'Translation must be valid PropFile object ({type(translation)} given).')
        if reference is None:
            raise ValueError(f'Reference must be valid PropFile object ({type(reference)} given).')

    def need_valid_config(self) -> None:
        if not isinstance(self.config, Config):
            raise ValueError(f'Configuration object must be instance of Config ("{type(self.config)}" given).')

    def get_default_config(self) -> Dict:
        return Check.DEFAULT_CHECK_CONFIG

    # @abstractmethod
    # def parse_args(self, args: argparse) -> Dict:
    #     raise NotImplementedError
