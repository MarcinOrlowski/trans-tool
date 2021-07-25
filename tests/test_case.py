"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import random
import unittest
from typing import List


class TestCase(unittest.TestCase):

    def get_random_string_list(self, count, str_prefix: str = '', str_length: int = 16) -> List[str]:
        return [self.get_random_string(str_prefix, str_length) for _ in range(count)]

    def get_random_string(self, prefix: str = '', length: int = 16) -> str:
        for _ in range(length):
            single_char = chr(random.randint(ord('A'), ord('Z')))
            if random.randint(0, 1):
                single_char = single_char.lower()
            prefix += single_char
        return prefix
