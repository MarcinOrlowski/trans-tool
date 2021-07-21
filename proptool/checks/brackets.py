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
from ..entries import PropComment, PropTranslation
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

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

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Brackets')

        for idx, item in enumerate(translation_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, (PropTranslation, PropComment)):
                continue

            # Keep matching brackets at the same positions!
            opening: List[str] = ['(', '[', '<', '{']
            closing: List[str] = [')', ']', '>', '}']

            stack: List[Bracket] = []
            has_errors = False
            for char_idx, current_char in enumerate(item.value):
                position: str = f'{idx + 1}:{char_idx + 1}'

                if current_char in opening:
                    # Every opening brace is pushed to the stack.
                    stack.append(Bracket(char_idx, current_char))
                    continue

                if current_char in closing:
                    # Every closing brace should take its own pair off the stack

                    if not stack:
                        # If stack is empty, then we had more closing brackets than opening ones.
                        if isinstance(item, PropTranslation):
                            report.error(position, f'No opening bracket matching "{current_char}".', item.key)
                        else:
                            report.warn(position, f'No opening bracket matching "{current_char}".')
                        # Just show single error per line to avoid flooding.
                        has_errors = True
                        break

                    # Check if what we are about to pop from the stack and see if our current_char matches.
                    expected = closing[opening.index(stack[-1].bracket)]
                    if current_char == expected:
                        stack.pop()
                        continue

                    # This is not the bracket we were looking for...
                    if isinstance(item, PropTranslation):
                        report.error(position, f'Expected "{expected}", found "{current_char}".', item.key)
                    else:
                        report.warn(position, f'Expected "{expected}", found "{current_char}".')
                    # Just show single error per line to avoid flooding.
                    has_errors = True
                    break

            if not has_errors:
                for bracket in stack:
                    position: str = f'{idx + 1}:{bracket.pos + 1}'
                    if isinstance(item, PropTranslation):
                        report.error(position, f'No closing bracket for "{bracket.bracket}" found.', item.key)
                    else:
                        report.warn(position, f'No closing bracket for "{bracket.bracket}" found.')
                    # Just show single error per line to avoid flooding.
                    break

        return report
