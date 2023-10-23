#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2023 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#

from typing import Union, List, Optional

from simplelog.log import Log
from transtool.report.items import Error, ReportItem, Warn


# #################################################################################################

class ReportGroup(list):
    def __init__(self, label: str):
        super().__init__()
        self.label = label
        self.warnings = 0
        self.errors = 0

    def create(self, position: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> None:
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

    def add(self, items: Optional[Union[ReportItem, List[ReportItem]]]) -> None:
        if not items:
            return

        if not isinstance(items, list):
            items = [items]

        for item in items:
            if item is None:
                continue
            if not issubclass(type(item), ReportItem):
                raise TypeError(f'Item must be subclass of ReportItem. "{type(item)}" given.')
            self.append(item)
            if isinstance(item, Warn):
                self.warnings += 1
            else:
                self.errors += 1

    @staticmethod
    def _to_list(line: Optional[Union[str, int]]) -> Optional[List[str]]:
        """
        Accepts line variable (of various types) and converts to list of strings.
        Raises TypeError is provided argument is of not supported type.
        """
        if line:
            if not isinstance(line, (str, int)):
                raise TypeError(f'Unsupported argument type. "{type(line)}" given.')
            if not isinstance(line, str):
                line = str(line)
        return line

    @staticmethod
    def build_warn(line: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> Warn:
        return Warn(ReportGroup._to_list(line), msg, trans_key)

    def warn(self, line: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> None:
        self.add(self.build_warn(line, msg, trans_key))

    @staticmethod
    def build_error(line: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> Error:
        return Error(ReportGroup._to_list(line), msg, trans_key)

    def error(self, line: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> None:
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
