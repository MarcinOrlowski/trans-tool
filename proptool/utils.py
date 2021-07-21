"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from sys import exit
from typing import List, Union


# DO NOT use Log class in Utils. That causes some dependency issues which are NOT
# worth solving.

# #################################################################################################

class Utils(object):
    @staticmethod
    def abort(msg: Union[str, List[str]] = 'Aborted', rc: int = 10) -> None:
        if isinstance(msg, str):
            msg = [msg]
        print(msg)
        exit(rc)
