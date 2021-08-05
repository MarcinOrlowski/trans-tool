"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from transtool.decorators.overrides import overrides
from transtool.report.group import ReportGroup
from .base.check import Check


class DanglingKeys(Check):

    # noinspection PyUnresolvedReferences
    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Dangling keys')
        # Remove all keys that are present in both files and see what left.
        dangling_keys = list(filter(lambda key: key not in reference_file.keys, translation_file.keys))
        for trans_key in dangling_keys:
            report.error(None, f'Not present in base file: "{trans_key}".')

        return report
