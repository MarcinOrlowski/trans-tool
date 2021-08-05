"""

# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from transtool.checks.base.check import Check
from transtool.config.config import Config
from transtool.prop.file import PropFile
from tests.test_case import TestCase


class TestBaseCheck(TestCase):
    """
    Tests base class of all Checks.
    """

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
        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check({})

        config = Config()
        prop = PropFile(config)
        check.need_both_files(prop, prop)

    def test_check(self) -> None:
        """
        Ensures there's no default implementation of check()
        """
        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check({})

        with self.assertRaises(NotImplementedError):
            check.check(None, None)

    def test_need_valid_config_valid_arg(self) -> None:
        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check({})
        # We expect no problems.
        check.need_valid_config()

    def test_need_valid_config_no_config(self) -> None:
        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check()
        # Exception should be thrown
        with self.assertRaises(ValueError):
            check.need_valid_config()

    def test_need_valid_config_invalid_config_type(self) -> None:
        # Check is abstract class, extending ABC meta, so ordinary
        # instantiation won't work.
        Check.__abstractmethods__ = frozenset()
        check = Check()
        # Inject faulty 'config' to walk around constructor check.
        check.config = 123
        # Exception should be thrown
        with self.assertRaises(ValueError):
            check.need_valid_config()

    def test_need_both_files_missing_file(self) -> None:
        """
        Checks how need_both_files() is handling missing arguments.
        """
        config = Config()
        prop = PropFile(config)
        check = Check({})

        with self.assertRaises(ValueError):
            check.need_both_files(None, None)

        with self.assertRaises(ValueError):
            check.need_both_files(prop, None)

        with self.assertRaises(ValueError):
            check.need_both_files(None, prop)
