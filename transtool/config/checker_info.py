"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from typing import Callable, Dict, Union


class CheckerInfo(object):
    def __init__(self, checker_id: str, checker_callable: Callable, config: Union[Dict, None] = None):
        self.id = checker_id
        self.callable = checker_callable
        self.config = config
