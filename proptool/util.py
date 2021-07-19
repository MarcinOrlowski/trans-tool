"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import sys
from typing import List, Union


# #################################################################################################

class Util:
    @staticmethod
    def error(msg: Union[str, List[str]] = 'Error') -> None:
        if type(msg) is not list:
            msg = [msg]
        _ = [print(f'{line}') for line in msg]

    @staticmethod
    def abort(msg: Union[str, List[str]] = 'Aborted') -> None:
        Util.error(msg)
        sys.exit(10)
