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
class Punctuation(Check):
    r"""
    This check verifies translation ends with the same punctuation marks or special characters (\n)
    as reference string.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Punctuation mismatch')

        for idx, item in enumerate(reference_file.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, Translation):
                continue

            for last_char in self.config['chars']:
                last_char_len = len(last_char)

                ref_last_char = item.value[(last_char_len * -1):]
                if ref_last_char == last_char:
                    translation = translation_file.find_by_key(item.key)
                    if translation:
                        trans_last_char = translation.value[(last_char_len * -1):]
                        if trans_last_char != ref_last_char:
                            report.warn(idx + 1, f'Ends with "{trans_last_char}". Expected "{ref_last_char}".', item.key)
                    break

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'chars': ['.', '?', '!', ':', r'\n'],
        }
