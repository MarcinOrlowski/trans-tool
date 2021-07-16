#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool
#
from typing import List, Union


# #################################################################################################

class Log:
    def __init__(self):
        self._buffer: List[str] = []

    def add(self, val: Union[str, List[str]]):
        if type(val) is str:
            val = [val]
        _ = [self._buffer.append(item) for item in val]

    def dump(self):
        print('\n'.join(self._buffer))
