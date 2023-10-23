"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2023 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Union, Optional


# #################################################################################################

class ReportItem(object):
    def __init__(self, position: Optional[Union[str, int]], msg: str, trans_key: Optional[str] = None) -> None:
        if position is not None:
            if isinstance(position, int):
                position = str(position)

        self.position = position
        self.msg = msg
        self.trans_key = trans_key

    def to_string(self) -> str:
        # Note trailing space!
        line = f'Line {self.position}: ' if self.position else ''
        if self.trans_key:
            # Note trailing space!
            line += f'"{self.trans_key}": '
        line += self.msg
        return line.strip()


# #################################################################################################

class Error(ReportItem):
    pass


# #################################################################################################

class Warn(ReportItem):
    pass
