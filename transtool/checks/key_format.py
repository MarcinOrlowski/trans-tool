"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import re
from typing import Dict, Union

from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from transtool.report.group import ReportGroup
from .base.check import Check


# noinspection PyUnresolvedReferences
class KeyFormat(Check):
    """
    This check verifies that translation keys follow specified naming convention.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup('Key naming pattern.')

        if translation_file.items:
            pattern = self.config['pattern']
            compiled_pattern = re.compile(pattern)

            for line_number, item in enumerate(translation_file.items):
                # We care translations only for now.
                # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
                if not isinstance(item, Translation):
                    continue

                if compiled_pattern.match(item.key) is None:
                    report.error(line_number + 1, 'Invalid key name format.', item.key)

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'pattern': r'^[a-zA-Z]+[a-zA-Z0-9_.]*[a-zA-Z0-9]+$',
        }
