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

# To avoid circular dependency, do NOT change this to:
#  from log import Log
import log


# #################################################################################################

class Utils:
    @staticmethod
    def error(msg: Union[str, List[str]] = 'Error') -> None:
        if type(msg) is not list:
            msg = [msg]
        _ = [log.Log.e(f'{line}') for line in msg]

    @staticmethod
    def abort(msg: Union[str, List[str]] = 'Aborted', rc: int = 10) -> None:
        Utils.error(msg)
        sys.exit(rc)
