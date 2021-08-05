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


class Bracket(object):
    def __init__(self, pos: int, bracket: str):
        self.pos = pos
        self.bracket = bracket


# noinspection PyUnresolvedReferences
class Brackets(Check):
    """
    Checks if brackets are used in translation and if so, ensures proper nesting and checks if all
    opened brackets are closed.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    report_title = 'Brackets'

    def _is_quoted(self, line: str, char_idx: int) -> bool:
        """
        Checks if char at position char_idx is quoted.
        :param line: String to be processed
        :param char_idx: Position of char we want to check quotation of.
        :return: True if it is quoted, False otherwise.
        """
        if 0 < char_idx < len(line) - 1:
            for quotation_mark in self.config['quotation_marks']:
                if line[char_idx - 1] == quotation_mark and line[char_idx + 1] == quotation_mark:
                    # It looks it is, so we are going to skip it.
                    return True
        return False

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup(self.report_title)

        opening_key = 'opening'
        closing_key = 'closing'

        opening = self.config[opening_key]
        closing = self.config[closing_key]

        opening_cnt = len(opening)
        closing_cnt = len(closing)

        if opening_cnt == 0 or closing_cnt == 0:
            report.warn(line = None, msg = f'CONFIG: Empty "{opening_key}" and "{closing_key}" arrays.')
            return report
        if opening_cnt != closing_cnt:
            report.error(line = None,
                         msg = f'CONFIG: Both "{opening_key}" and "{closing_key}" arrays must contain the same number of elements.')
            return report

        # We do that check at the end to ensure config is validated first.
        if not translation.items:
            return report

        for idx, item in enumerate(translation.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if self._shall_skip_item(item):
                continue

            stack: List[Bracket] = []
            has_errors = False
            for char_idx, current_char in enumerate(item.value):
                position: str = f'{idx + 1}:{char_idx + 1}'

                in_opening = False
                in_closing = False

                if current_char in opening:
                    in_opening = True
                elif current_char in closing:
                    in_closing = True
                else:
                    continue

                # At this point we know we are dealing with known bracket.
                if self.config['ignore_quoted'] and self._is_quoted(item.value, char_idx):
                    continue

                if in_opening:
                    # Every opening brace is pushed to the stack.
                    stack.append(Bracket(char_idx, current_char))
                    continue

                if in_closing:
                    # Every closing brace should take its own pair off the stack

                    if not stack:
                        # If stack is empty, then we had more closing brackets than opening ones.
                        report.create(position, f'No opening character matching "{current_char}".', item.key)
                        # Just show single error per line to avoid flooding.
                        has_errors = True
                        break

                    # Check if what we are about to pop from the stack and see if our current_char matches.
                    expected = closing[opening.index(stack[-1].bracket)]
                    if current_char == expected:
                        stack.pop()
                        continue

                    # This is not the bracket we were looking for...
                    report.create(position, f'Expected "{expected}", found "{current_char}".', item.key)
                    # Just show single error per line to avoid flooding.
                    has_errors = True
                    break

            if not has_errors and stack:
                # Just show single error per line to avoid flooding.
                bracket = stack[0]
                position: str = f'{idx + 1}:{bracket.pos + 1}'
                report.create(position, f'No closing character for "{bracket.bracket}" found.', item.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'comments':        False,
            'ignore_quoted':   True,
            'quotation_marks': ['"', "'"],

            # Keep matching elements at the same positions
            'opening':         ['(', '[', '{'],
            'closing':         [')', ']', '}'],
        }
