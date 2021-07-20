"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from abc import ABC, abstractmethod

from ...config import Config
from ...report.report import Report


# #################################################################################################

# noinspection PyUnresolvedReferences
class Check(ABC):
    def __init__(self, config: Config):
        if not isinstance(config, Config):
            raise ValueError('Invalid type of config passed.')
        self.config = config

    @abstractmethod
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference: 'PropFile', translation: 'PropFile') -> Report:
        raise NotImplementedError
