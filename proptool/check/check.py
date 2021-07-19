#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

from abc import ABC, abstractmethod

from ..app import App
from ..propfile import PropFile
from ..report.report import Report


# #################################################################################################

class Check(ABC):
    @staticmethod
    @abstractmethod
    def check(self, app: App, reference: PropFile, translation: PropFile) -> Report:
        raise NotImplemented
