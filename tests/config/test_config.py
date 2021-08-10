"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import random

from tests.test_case import TestCase
from transtool.config.config import Config


class TestConfig(TestCase):

    def test_set_checker_config(self) -> None:
        config = Config()
        checker_id = self.get_random_string('checker_id')
        checker_config = {}
        max_items = 10
        for idx in range(random.randint(1, max_items)):
            checker_config[self.get_random_string(f'key{idx}')] = self.get_random_string(f'val{idx}')
        config.set_checker_config(checker_id, checker_config)

        self.assertIn(checker_id, config.checks)
        self.assertEqual(len(checker_config), len(config.checks[checker_id]))
        for key, val in checker_config.items():
            self.assertIn(key, config.checks[checker_id])
            self.assertEqual(val, config.checks[checker_id][key])

    def test_set_checker_config_invalid_type(self) -> None:
        config = Config()
        checker_id = self.get_random_string('checker_id')
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            config.set_checker_config(checker_id, False)  # noqa: WPS425

    def test_get_checker_config(self) -> None:
        config = Config()
        checker_id = self.get_random_string('checker_id')
        checker_config = {}
        max_items = 10
        for idx in range(random.randint(1, max_items)):
            checker_config[self.get_random_string(f'key{idx}')] = self.get_random_string(f'val{idx}')
        config.set_checker_config(checker_id, checker_config)

        read_config = config.get_checker_config(checker_id)
        self.assertEqual(len(checker_config), len(read_config))
        for key, val in checker_config.items():
            self.assertIn(key, read_config)
            self.assertEqual(val, read_config[key])

    def test_get_checker_config_no_entry(self) -> None:
        config = Config()
        checker_id = self.get_random_string('checker_id')
        with self.assertRaises(KeyError):
            config.get_checker_config(checker_id)
