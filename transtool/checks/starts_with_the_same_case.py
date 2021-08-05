"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Dict, Tuple, Union

from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from transtool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class StartsWithTheSameCase(Check):
    """
    This check verifies translation first letter is the same lower/upper cased as original text.
    """

    def _find_word(self, line: str) -> Tuple[Union[int, None], Union[str, None]]:
        words = line.strip().split()
        for idx, word in enumerate(words):
            if word[0].isalpha():
                return idx, word
        return None, None

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_both_files(translation_file, reference_file)
        self.need_valid_config()

        report = ReportGroup('First words case mismatch.')

        for idx, trans in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(trans, Translation):
                continue

            # Is there translation of this item present?
            ref = reference_file.find_by_key(trans.key)

            if not ref:
                continue

            # Skip if translation or reference string is empty.
            if ref.value.strip() == '' or trans.value.strip() == '':
                continue

            # Before we look for words, let's check for digits (if enabled)
            if self.config['accept_digits']:
                # Any starting digit matches "opposite" sentence's case
                if ref.value[0].isdigit() or trans.value[0].isdigit():
                    continue

            # Find first 'word' that starts with a letter.
            ref_word_idx, ref_word = self._find_word(ref.value)
            trans_word_idx, trans_word = self._find_word(trans.value)

            # Skip line if both base and translation strings contain no words.
            if not ref_word and not trans_word:
                continue

            if ref_word and not trans_word:
                report.warn(idx + 1, 'Translation contains no words starting with a letter, while original does.', trans.key)
                continue
            if not ref_word and trans_word:
                report.warn(idx + 1, 'Base string contains no words starting with a letter, but translation does.', trans.key)
                continue

            ref_first_char = ref_word[0]
            trans_first_char = trans_word[0]

            if trans_first_char.isupper() != ref_first_char.isupper():
                if ref_first_char.isupper():
                    expected = 'UPPER-cased'
                    found = 'lower-cased'
                else:
                    expected = 'lower-cased'
                    found = 'UPPER-cased'

                report.warn(idx + 1, f'Value starts with {found} character. Expected {expected}.', trans.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'accept_digits': True,
        }
