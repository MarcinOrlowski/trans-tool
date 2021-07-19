"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from .base.check import Check
from ..entries import PropComment, PropTranslation
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

# noinspection PyUnresolvedReferences
class TrailingWhiteChars(Check):
    """
    Checks if file has trailing white characters at the end of each line.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Trailing white characters')
        for idx, item in enumerate(translation_file):
            if isinstance(item, (PropTranslation, PropComment)):
                diff_count = len(item.value) - len(item.value.rstrip())
                if diff_count == 0:
                    continue

                if isinstance(item, PropTranslation):
                    report.error(idx + 1, f'In "{item.key}" entry: {diff_count}.')
                else:
                    report.warn(idx + 1, f'In comment: {diff_count}.')

        return report
