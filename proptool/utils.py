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

from .log import Log


# #################################################################################################

class Utils:
    @staticmethod
    def abort(msg: Union[str, List[str]] = 'Aborted', rc: int = 10) -> None:
        Log.e(msg)
        sys.exit(rc)
