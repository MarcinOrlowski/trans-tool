"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Callable, Dict, Union


class CheckerInfo(object):
    def __init__(self, id: str, cls: Callable, config: Union[Dict, None] = None):
        self.id = id
        self.cls = cls
        self.config = config
