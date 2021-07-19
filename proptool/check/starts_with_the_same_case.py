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
class StartsWithTheSameCase(Check):
    """
    This check verifies translation first letter is the same lower/upper cased as original text.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Sentence starts with different letter case.')

        for idx, item in enumerate(translation_file):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, PropTranslation):
                continue

            # Is there translation of this item present?
            ref = reference_file.find_by_key(item.key)
            # Skip dangling keys
            if not ref:
                continue

            # Skip if translation or reference string is empty.
            if item.value.strip() == '' or ref.value.strip() == '':
                continue

            trans_first_char = item.value[0]
            ref_first_char = ref.value[0]

            if trans_first_char.isupper() != ref_first_char.isupper():
                if ref_first_char.isupper():
                    expected = 'UPPER-cased'
                    found = 'lower-cased'
                else:
                    expected = 'lower-cased'
                    found = 'UPPER-cased'

                report.error(idx + 1, f'"{item.key}" starts with {found} character. Expected {expected}.')

        return report
