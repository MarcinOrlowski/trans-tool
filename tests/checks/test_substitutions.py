"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
from typing import Dict, Union, List

from transtool.checks.substitutions import Substitutions
from transtool.decorators.overrides import overrides
from transtool.prop.file import PropFile
from transtool.prop.items import Comment, Translation
from tests.checks.checks_test_case import ChecksTestCase


class SubstitutionsTests(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Union[Dict, None] = None) -> Substitutions:
        return Substitutions(config)

    # #################################################################################################

    def _get_valid_strings(self) -> List[str]:
        return [
            'Foo. Bar. All is fin5e!',
            'Foo!',
        ]

    def _get_faulty_strings(self) -> List[str]:
        return [
            'Triple dots...',
            'Ough!!!',
        ]

    def test_translation_no_faults(self) -> None:
        for test in self._get_valid_strings():
            self.check_single_file(Translation('key', test))

    def test_empty_translation(self) -> None:
        self.check(PropFile(self.config))

    # #################################################################################################

    def test_comment_no_faults(self) -> None:
        for test in self._get_valid_strings():
            self.check_single_file(Comment(test))

    def test_comment_with_faults(self) -> None:
        faults = self._get_faulty_strings()

        for fault in faults:
            # We should see no issues if comment scanning is disabled.
            self.checker.config['comments'] = False
            self.check_single_file(Comment(fault))

            # And some warnings when comment scanning in enabled.
            self.checker.config['comments'] = True
            self.check_single_file(Comment(fault), exp_warnings = 1)

    # #################################################################################################

    def test_fail_with_error_flag(self) -> None:
        """
        Ensures FLAG_FAIL_WITH_ERROR flag aborts scanning and returns error while
        FLAG_DEFAULT yields warning.
        """
        cfg = {
            'regexp': r'([\.]{3})',
            'replace': '…',
        }
        self.checker.config['map'] = [cfg]

        cfg['flag'] = Substitutions.FLAG_DEFAULT
        self.check_single_file(Translation('key', 'Triple dots...'), exp_warnings = 1)

        cfg['flag'] = Substitutions.FLAG_FAIL_WITH_ERROR
        self.check_single_file(Translation('key', 'Triple dots...'), exp_errors = 1)
