"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from abc import abstractmethod
from typing import List, Union

from proptool.checks.base.check import Check
from proptool.config import Config
from proptool.prop.items import Comment, PropItem, Translation
from proptool.prop.file import PropFile
from tests.test_case import TestCase


# #################################################################################################

class ChecksTestCase(TestCase):

    def setUp(self):
        self.config: Config = Config()
        checker = self.get_checker(self.config)
        if not issubclass(type(checker), Check):
            raise ValueError('Checker must be subclass of Check')
        self.checker = checker

    @abstractmethod
    def get_checker(self, config: Config) -> Check:
        raise NotImplementedError

    def check_single_file(self, entry: PropItem, exp_errors: int = 0, exp_warnings: int = 0) -> None:
        prop_file = PropFile(self.config)
        prop_file.loaded = True
        prop_file.items.append(entry)

        self.check(prop_file, exp_errors = exp_errors, exp_warnings = exp_warnings)

    def check(self, translation: PropFile, reference: Union[PropFile, None] = None,
              exp_errors: int = 0, exp_warnings: int = 0) -> None:
        report = self.checker.check(translation, reference)

        self.assertEqual(exp_errors, report.errors)
        self.assertEqual(exp_warnings, report.warnings)

    def build_prepfile(self, contents: Union[List[str], List[PropItem]]) -> PropFile:
        prep_file = PropFile(self.config)
        prep_file.loaded = True

        for item in contents:
            if isinstance(item, str):
                prep_file.keys.append(item)
                prep_file.items.append(Translation(item, self.get_random_string()))
                continue
            elif isinstance(item, (Translation, Comment)):
                prep_file.append(item)
            else:
                raise RuntimeError(f'Unsupported content type: {type(item)}')
        return prep_file
