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
from transtool.report.items import Error, Warn


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

    def warn(self, line: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
        if line and not isinstance(line, str):
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
