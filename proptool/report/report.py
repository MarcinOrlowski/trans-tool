#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

from .report_item import ReportItem
from ..report.error import Error
from ..report.warn import Warn


# #################################################################################################


class Report(list):
    def add(self, item: ReportItem) -> None:
        item_cls = type(item)
        if not issubclass(item_cls, ReportItem):
            raise TypeError(f'Item must be instance of {ReportItem}. {item_cls} given.')
        self.append(item)

    def failed(self):
        return len(self) > 0

    def warn(self, line: int, msg: str) -> None:
        self.append(Warn(line, msg))

    def error(self, line: int, msg: str) -> None:
        self.append(Error(line, msg))
