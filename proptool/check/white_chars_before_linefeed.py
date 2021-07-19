"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from .base.check import Check
from ..entries import PropTranslation
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

# noinspection PyUnresolvedReferences
class WhiteCharsBeforeLinefeed(Check):
    """
    This check ensures there's no space before "\n", "\r" literals.
    """

    def __scan(self, report: ReportGroup, idx: int, item: PropTranslation, literal: str) -> bool:
        literal_len = len(literal)
        for pos in range(len(item.value) - literal_len, 0, -1):
            if item.value[pos:(pos + 2)] == literal:
                pre = item.value[pos - 1]
                if pre in [' ', '\t']:
                    what = 'SPACE' if pre == ' ' else 'TAB'
                    report.warn(idx + 1, f'"{item.key}" contains {what} character before "{literal}" literal.', pos)
                    return True
        return False

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Space before linefeed literal')

        for idx, item in enumerate(translation_file):
            # We care translations only for now.
            if not isinstance(item, PropTranslation):
                continue

            for literal in ['\\n', '\\r']:
                # Skip too short lines.
                literal_len = len(literal)
                if len(item.value.strip()) <= literal_len:
                    continue

                if self.__scan(report, idx, item, literal):
                    break

        return report
