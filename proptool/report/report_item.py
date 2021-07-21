"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Union


class ReportItem(object):
    def __init__(self, line: Union[str, None], msg: str, trans_key: Union[str, None] = None) -> None:
        self.line = line
        self.msg = msg
        self.trans_key = trans_key

    def to_string(self) -> str:
        trans_key = f'"{self.trans_key}":' if self.trans_key else ''
        if self.line:
            return f'Line {self.line}:{trans_key} {self.msg}'.strip()
        return f'{trans_key} {self.msg}'.strip()
