"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Union

from transtool.log import Log
from transtool.report.items import Error, ReportItem, Warn


# #################################################################################################

class ReportGroup(list):
    def __init__(self, label: str):
        super().__init__()
        self.label = label
        self.warnings = 0
        self.errors = 0

    def create(self, position: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        """
        Helper to create either Error() or Warn() items that share the message (to remove duplicated code and logic).
        If trans_key is None, it is assumed report message relates
        to comment issue which by default gets reported as Warn(). If translation key is present
        such offence is reported as Error.

        :param position:
        :param msg:
        :param trans_key:
        :return:
        """
        if trans_key is None:
            self.warn(position, msg)
        else:
            self.error(position, msg, trans_key)

    def empty(self) -> bool:
        return (self.errors + self.warnings) == 0

    def add(self, item) -> None:
        if not issubclass(type(item), ReportItem):
            raise TypeError(f'Item must be subclass of ReportItem. "{type(item)}" given.')
        self.append(item)
        if isinstance(item, Warn):
            self.warnings += 1
        else:
            self.errors += 1

    @staticmethod
    def build_warn(line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> Warn:
        if line and not isinstance(line, str):
            line = str(line)
        return Warn(line, msg, trans_key)

    def warn(self, line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        self.add(self.build_warn(line, msg, trans_key))

    @staticmethod
    def build_error(line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> Error:
        if isinstance(line, int):
            line = str(line)
        return Error(line, msg, trans_key)

    def error(self, line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        self.add(self.build_error(line, msg, trans_key))

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
