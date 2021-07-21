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


class TestCase(unittest.TestCase):
    def get_random_string(self, prefix: str = '', count: int = 16) -> str:
        for _ in range(count):
            single_char = chr(random.randint(ord('A'), ord('Z')))
            if random.randint(0, 1):
                single_char = single_char.lower()
            prefix += single_char
        return prefix
