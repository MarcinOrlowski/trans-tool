"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import List

from .base.check import Check
from ..entries import PropComment, PropTranslation, PropEntry
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

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

    def _check_line(self, item: PropEntry):
        pass

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Quotation marks')

        # NOTE: we do not support apostrophe, because i.e. in English it can be used in sentence: "Dogs' food"
        # Not sure how to deal with this (and I do not want to do dictionary match)
        supported_marks: List[str] = {'"', '`'}

        for line_idx, item in enumerate(translation_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, (PropTranslation, PropComment)):
                continue

            stack: List[Mark] = []
            for pos, current_char in enumerate(item.value):
                if current_char not in supported_marks:
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
                if isinstance(item, PropTranslation):
                    report.error(position, f'No paired mark for {quotation_mark.mark}.', item.key)
                else:
                    report.warn(position, f'No paired mark for {quotation_mark.mark}.')
                # Just show single error per line to avoid flooding.
                break

        return report
