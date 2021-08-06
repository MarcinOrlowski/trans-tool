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
from transtool.prop.items import Translation
from transtool.report.group import ReportGroup
from .base.check import Check


class WhiteCharsBeforeLinefeed(Check):
    r"""
    This check ensures there's no space before "\n", "\r" literals.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    def _scan(self, report: ReportGroup, idx: int, item: Translation, literal: str) -> bool:
        literal_len = len(literal)
        # Let's crawl backward and see what's there...
        for pos in range(len(item.value) - literal_len, 0, -1):
            if item.value[pos:(pos + 2)] == literal:
                pre = item.value[pos - 1]
                if pre in {' ', '\t'}:
                    what = 'SPACE' if pre == ' ' else 'TAB'
                    report.warn(f'{idx + 1}:{pos}', f'Contains {what} character before "{literal}" literal.', item.key)
                    return True
        return False

    # noinspection PyUnresolvedReferences
    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup('White chars before linefeed literal')

        for idx, item in enumerate(translation_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if self._shall_skip_item(item):
                continue

            for literal in (r'\n', r'\r'):
                # Skip too short lines.
                literal_len = len(literal)
                if len(item.value.strip()) <= literal_len:
                    continue

                if self._scan(report, idx, item, literal):
                    break

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'comments': False,
        }
