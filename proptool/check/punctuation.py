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
class Punctuation(Check):
    """
    This check verifies translation ends with the same punctuation marks or special characters (\n)
    as original string.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Punctuation mismatch')

        for idx, item in enumerate(reference_file):
            # We care translations only for now.

            if not isinstance(item, PropTranslation):
                continue

            for last_char in ['.', '?', '!', ':', '\\n']:
                last_char_len = len(last_char)

                ref_last_char = item.value[(last_char_len * -1):]
                if ref_last_char == last_char:
                    translation = translation_file.find_by_key(item.key)
                    if translation:
                        trans_last_char = translation.value[(last_char_len * -1):]
                        if trans_last_char != ref_last_char:
                            report.error(idx + 1, f'"{item.key}" ends with "{trans_last_char}". Expected "{ref_last_char}".')
                    break

        return report
