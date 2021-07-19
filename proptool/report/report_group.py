"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Union

from .report_item import ReportItem
from ..log import Log
from ..report.error import Error
from ..report.warn import Warn


# #################################################################################################

class ReportGroup(list):
    def __init__(self, label: str):
        self.label = label
        self.warnings = 0
        self.errors = 0

    def add(self, item: ReportItem) -> None:
        item_cls = type(item)
        if not issubclass(item_cls, ReportItem):
            raise TypeError(f'Item must be instance of {ReportItem}. {item_cls} given.')
        self.append(item)

    def empty(self) -> bool:
        return (self.errors + self.warnings) == 0

    def warn(self, line: int, msg: str) -> None:
        self.append(Warn(line, msg))
        self.warnings += 1

    def error(self, line: Union[int, None], msg: str) -> None:
        self.append(Error(line, msg))
        self.errors += 1

    def dump(self):
        if self.errors > 0:
            Log.level_push_e(self.label)
        else:
            Log.level_push_w(self.label)

        for entry in self:
            if isinstance(entry, Warn):
                Log.w(entry.to_string())
            else:
                Log.e(entry.to_string())
        Log.level_pop()
