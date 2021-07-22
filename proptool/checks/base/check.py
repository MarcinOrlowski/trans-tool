"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from abc import ABC, abstractmethod
from typing import Union

from proptool.config import Config
from proptool.report.report import Report


# noinspection PyUnresolvedReferences
class Check(ABC):
    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise ValueError('Invalid type of config passed.')
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
