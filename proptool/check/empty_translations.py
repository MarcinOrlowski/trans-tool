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
class EmptyTranslations(Check):
    """
    This check verifies translation exists and is not an empty string (unless original string is also empty).
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Empty translations')

        for idx, item in enumerate(translation_file):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, PropTranslation):
                continue

            # If translation is not empty, skip it.
            if item.value.strip() != '':
                continue

            # Get reference string. Skip if not found (dangling key?)
            ref = reference_file.find_by_key(item.key)
            if not ref:
                continue

            # If reference string is empty, translation can be empty too.
            if ref.value.strip() == '':
                continue

            report.warn(idx + 1, f'"{item.key}" is an empty string.')

        return report
