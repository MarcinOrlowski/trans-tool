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

    def _check_line(self, item: PropEntry):
        pass

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Brackets')

        for idx, item in enumerate(translation_file):
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
                    stack.append(Bracket(char_idx, current_char))
                elif current_char in closing:
                    if stack:
                        if isinstance(item, PropTranslation):
                            report.error(position, f'"{item.key}": No opening bracket matching "{current_char}".')
                        else:
                            report.warn(position, f'No opening bracket matching "{current_char}".')
                        # Just show single error per line to avoid flooding.
                        has_errors = True
                        break
                    else:
                        popped: Bracket = stack.pop()
                        # Check if what we popped from the stack is one of opening brackets.
                        if popped.bracket not in opening:
                            if isinstance(item, PropTranslation):
                                report.error(position, f'"{item.key}: No opening bracket matching "{current_char}".')
                            else:
                                report.warn(position, f'No opening bracket matching "{current_char}".')
                            # Just show single error per line to avoid flooding.
                            has_errors = True
                            break
                        else:
                            # Check if this is the right closing bracket type for what we popped from the stack
                            bracket_idx = opening.index(popped.bracket)
                            expected = closing[bracket_idx]
                            if current_char != expected:
                                if isinstance(item, PropTranslation):
                                    report.error(position, f'"{item.key}: Incorrect type. Expected "{expected}", found "{current_char}".')
                                else:
                                    report.error(position, f'"Incorrect type. Expected "{expected}", found "{current_char}".')
                                # Just show single error per line to avoid flooding.
                                has_errors = True
                                break

            if not has_errors:
                for bracket in stack:
                    position: str = f'{idx + 1}:{bracket.pos + 1}'
                    if isinstance(item, PropComment):
                        report.warn(position, f'No closing bracket for "{bracket.bracket}"')
                    else:
                        report.error(position, f'"{item.key}": No closing bracket for "{bracket.bracket}".')
                    # Just show single error per line to avoid flooding.
                    break

        return report
