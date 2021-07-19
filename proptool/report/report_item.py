"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""


class ReportItem:
    def __init__(self, line: int, msg: str, column: int = None) -> None:
        self.line = line
        self.column = column
        self.msg = msg

    def to_string(self) -> str:
        if self.line:
            if self.column:
                return f'Line {self.line}:{self.column}: {self.msg}'
            else:
                return f'Line {self.line}: {self.msg}'
        else:
            return f'{self.msg}'
