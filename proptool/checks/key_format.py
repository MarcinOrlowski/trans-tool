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
from proptool.prop.prop_entries import PropTranslation
from proptool.decorators.overrides import overrides
from proptool.report.report_group import ReportGroup


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
        compiled_pattern = re.compile(pattern)

        report = ReportGroup(f'Key naming pattern: {pattern}')

        for line_number, item in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, PropTranslation):
                continue

            if compiled_pattern.match(item.key) is None:
                report.error(line_number + 1, 'Invalid key name format.', item.key)

        return report
