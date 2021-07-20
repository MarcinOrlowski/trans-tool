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

        translation_keys = translation_file.keys.copy()
        for ref_key in reference_file.keys:
            if ref_key in translation_keys:
                translation_keys.remove(ref_key)

        for trans_key in translation_keys:
            report.error(None, f'Not present in base file: "{trans_key}".')

        return report
