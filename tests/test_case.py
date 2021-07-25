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
from typing import List, Tuple


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

    def get_random_bool(self) -> bool:
        return True if random.randint(0, 1) == 1 else False

    def get_random_on_off_pair(self) -> Tuple[bool, bool]:
        """
        Generates pair of two bools, where only one can be True at the time,
        but both can be False. This is basically handy to simulate argparse
        `--foo`/`--no-foo` options.
        :return: tuple of two bools.
        """
        switch_a = self.get_random_bool()
        # Only one switch can be set True
        switch_b = False if not switch_a else self.get_random_bool()
        return switch_a, switch_b
