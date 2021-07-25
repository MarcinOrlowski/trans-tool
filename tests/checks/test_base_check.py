"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from proptool.checks.base.check import Check
from proptool.config.config import Config
from proptool.prop.file import PropFile
from tests.test_case import TestCase


class TestBaseCheck(TestCase):

    def test_constructor(self) -> None:
        """
        Checks handling of invalid type of config argument.
        """
        with self.assertRaises(ValueError):
            # Check is abstract class, extending ABC meta, so ordinary
            # instantiation won't work.
            Check.__abstractmethods__ = frozenset()
            # noinspection PyTypeChecker
            Check(False)

    def test_need_both_files_no_fault(self) -> None:
        config = Config()

        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check(config)

        prop = PropFile(config)
        check.need_both_files(prop, prop)

    def test_check(self) -> None:
        """
        Ensures there's no default implementation of check()
        """
        config = Config()

        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check(config)

        with self.assertRaises(NotImplementedError):
            check.check(None, None)

    def test_need_both_files_missing_file(self) -> None:
        """
        Checks how need_both_files() is handling missing arguments.
        """
        config = Config()
        check = Check(config)
        prop = PropFile(config)

        with self.assertRaises(ValueError):
            check.need_both_files(None, None)

        with self.assertRaises(ValueError):
            check.need_both_files(prop, None)

        with self.assertRaises(ValueError):
            check.need_both_files(None, prop)
