"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from proptool.config.config import Config
from proptool.prop.file import PropFile
from tests.test_case import TestCase


class TestPropFile(TestCase):

    def test_append_wrong_arg_type(self) -> None:
        # GIVEN normal instance of PropFile
        prop_file = PropFile(Config())

        # WHEN we try to append object of unsupported type
        obj = 'INVALID'

        # THEN Exception should be thrown.
        with self.assertRaises(TypeError):
            prop_file.append(obj)
