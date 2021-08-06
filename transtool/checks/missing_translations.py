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
from transtool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class MissingTranslations(Check):
    """
    This check checks if given base key is also present in translation file.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Missing translations')

        missing_keys: List[str] = [ref_key for ref_key in reference_file.keys if ref_key not in translation_file.keys]

        # Commented out keys are also considered present in the translation
        # unless we run in strict check mode.
        if not self.config['strict']:
            for comm_key in translation_file.commented_out_keys:
                if comm_key in missing_keys:
                    del missing_keys[missing_keys.index(comm_key)]

        for missing_key in missing_keys:
            report.warn(None, 'Missing translation.', missing_key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'strict': False,
        }
