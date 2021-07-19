"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import re

from .base.check import Check
from ..entries import PropTranslation
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

# noinspection PyUnresolvedReferences
class KeyFormat(Check):
    """
    This check verifies that translation keys follow specified naming convention.
    """

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:

        pattern = self.config.checks['KeyFormat']['pattern']
        p = re.compile(pattern)

        report = ReportGroup(f'Key naming pattern: {pattern}')

        for line_number, item in enumerate(translation_file):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, PropTranslation):
                continue

            if p.match(item.key) is None:
                report.error(line_number + 1, f'"{item.key}" key does not match.')

        return report
