"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from .base.check import Check
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

# noinspection PyUnresolvedReferences
class DanglingKeys(Check):

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Dangling keys')

        # Remove all keys that are present in both files and see what left.
        dangling_keys = list(filter(lambda key: key not in reference_file.keys, translation_file.keys))
        for trans_key in dangling_keys:
            report.error(None, f'Not present in base file: "{trans_key}".')

        return report
