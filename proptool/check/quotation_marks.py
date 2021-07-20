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

        for line_idx, item in enumerate(translation_file):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, (PropTranslation, PropComment)):
                continue

            # NOTE: we do not support apostrophe, because i.e. in English it can be used in sentence: "Dogs' food"
            # Not sure how to deal with this (and I do not want to do dictionary match)
            marks: List[str] = ['"', '`']

            stack: List[Mark] = []
            has_errors = False
            for pos, current_char in enumerate(item.value):
                position: str = f'{line_idx + 1}:{pos + 1}'

                if current_char not in marks:
                    continue

                if not stack:
                    # If stack is empty, push our mark and move on
                    stack.append(Mark(pos, current_char))
                    continue

                popped = stack.pop()
                if popped.mark == current_char:
                    # It it matches our mark, then it's the right one :)
                    continue

                if isinstance(item, PropTranslation):
                    report.error(position,
                                 f'"{item.key}": Quotation mark mismatch. Expected {popped.mark}, found {current_char}.')
                else:
                    report.warn(position, f'Quotation mark mismatch. Expected {popped.mark}, found {current_char}.')
                # Just show single error per line to avoid flooding.
                has_errors = True
                break

            if not has_errors:
                for bracket in stack:
                    position: str = f'{line_idx + 1}:{bracket.pos + 1}'
                    if isinstance(item, PropComment):
                        report.warn(position, f'No closing mark for {bracket.mark}.')
                    else:
                        report.error(position, f'"{item.key}": No closing mark for {bracket.mark}.')
                    # Just show single error per line to avoid flooding.
                    break

        return report
