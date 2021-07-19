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
class MissingTranslation(Check):
    """
    This check checks if given base key is also present in translation file.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Missing keys')

        translation_keys = translation_file.keys.copy()
        missing_keys: List[str] = []
        for key in reference_file.keys:
            if key in translation_keys:
                translation_keys.remove(key)
            else:
                missing_keys.append(key)

        # Commented out keys are also considered present in the translation unless
        # we run in strict check mode.
        if not self.config.strict:
            commented_out_keys = translation_file.commented_out_keys.copy()
            for key in commented_out_keys:
                if key in missing_keys:
                    missing_keys.remove(key)

        for key in missing_keys:
            report.warn(None, key)

        return report
