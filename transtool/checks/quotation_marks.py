"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Dict, List, Union

from transtool.decorators.overrides import overrides
from transtool.report.group import ReportGroup
from .base.check import Check


class Mark(object):
    def __init__(self, pos: int, mark: str):
        self.pos = pos
        self.mark = mark


# noinspection PyUnresolvedReferences
class QuotationMarks(Check):
    """
    Checks if quotation marks are used in translation and if so, ensures proper nesting and checks if all
    opened marks got their closing pair.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup('Quotation marks')

        for line_idx, item in enumerate(translation_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if self._shall_skip_item(item):
                continue

            stack: List[Mark] = []
            for pos, current_char in enumerate(item.value):
                if current_char not in self.config['chars']:
                    continue

                if not stack:
                    # If stack is empty, push our mark and move on
                    stack.append(Mark(pos, current_char))
                    continue

                # If stack is not empty then we see if the last item is a match. If not,
                # we assume this attempt to nest the quotation marks. If that's not the case
                # we will catch that later anyway as we will have it left on stack.
                if stack[-1].mark == current_char:
                    # It it matches our mark, then it's the right one :)
                    stack.pop()
                    continue
                stack.append(Mark(pos, current_char))

            for quotation_mark in stack:
                position: str = f'{line_idx + 1}:{quotation_mark.pos + 1}'
                report.create(position, f'No paired mark for {quotation_mark.mark}.', item.key)
                # Just show single error per line to avoid flooding.
                break

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'comments': True,
            'chars': ['"', '`'],
        }
