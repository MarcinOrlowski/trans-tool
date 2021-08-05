"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Dict
from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from transtool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class EmptyTranslations(Check):
    """
    This check verifies translation exists and is not an empty string (unless original string is also empty).
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Empty translations')

        for idx, item in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, Translation):
                continue

            # If translation is not empty, skip it.
            if item.value.strip() != '':
                continue

            # Get reference string. Skip if not found (dangling key?)
            ref: Translation = reference_file.find_by_key(item.key)
            if not ref:
                continue

            # If reference string is empty, translation can be empty too.
            if ref.value.strip() == '':
                continue

            report.warn(idx + 1, 'Empty string.', item.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'strict': False,
        }
