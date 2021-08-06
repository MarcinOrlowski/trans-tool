"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Dict, Union

from transtool.decorators.overrides import overrides
from transtool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class TrailingWhiteChars(Check):
    """
    Checks if file has trailing white characters at the end of each line.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup('Trailing white characters')

        for idx, item in enumerate(translation_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if self._shall_skip_item(item):
                continue
            diff_count = len(item.value) - len(item.value.rstrip())
            if diff_count > 0:
                report.create(idx + 1, f'Trailing white chars: {diff_count}.', item.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'comments': False,
        }
