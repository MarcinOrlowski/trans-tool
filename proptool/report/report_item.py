"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""


class ReportItem:
    def __init__(self, line: int, msg: str) -> None:
        self.line = line
        self.msg = msg

    def to_string(self) -> str:
        if self.line:
            return f'Line {self.line}: {self.msg}'
        else:
            return f'{self.msg}'
