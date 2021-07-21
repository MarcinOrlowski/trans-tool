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
        super().__init__()
        self.label = label
        self.warnings = 0
        self.errors = 0

    def add(self, report_item: ReportItem) -> None:
        item_cls = type(report_item)
        if not issubclass(item_cls, ReportItem):
            raise TypeError(f'Item must be instance of {ReportItem}. {item_cls} given.')
        self.append(report_item)

    def empty(self) -> bool:
        return (self.errors + self.warnings) == 0

    def warn(self, line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        if not isinstance(line, str):
            line = str(line)

        self.append(Warn(line, msg, trans_key))
        self.warnings += 1

    def error(self, line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        if isinstance(line, int):
            line = str(line)
        self.append(Error(line, msg, trans_key))
        self.errors += 1

    def dump(self, show_warnings_as_errors: bool = False):
        if show_warnings_as_errors:
            Log.push_e(self.label)
        elif self.errors > 0:
            Log.push_e(self.label)
        else:
            Log.push_w(self.label)

        for entry in self:
            if show_warnings_as_errors:
                Log.e(entry.to_string())
            elif isinstance(entry, Warn):
                Log.w(entry.to_string())
            else:
                Log.e(entry.to_string())
        Log.pop()
