#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

from ..overrides import overrides
from .report import ReportItem


# #################################################################################################

class Error(ReportItem):

    @overrides(ReportItem)
    def type(self):
        return 'E'
