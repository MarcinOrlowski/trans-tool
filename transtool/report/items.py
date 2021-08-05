"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from typing import Union


# #################################################################################################

class ReportItem(object):
    def __init__(self, position: Union[str, int, None], msg: str, trans_key: Union[str, None] = None) -> None:
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
