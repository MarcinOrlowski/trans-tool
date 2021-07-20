"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import re

from typing import List

from .base.check import Check
from ..entries import PropTranslation
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

class Formatter:
    def __init__(self, pos: int, formatter: str):
        self.pos = pos
        self.formatter = formatter


# noinspection PyUnresolvedReferences
class FormattingValues(Check):
    """
    This check verifies that if original string uses any %* formatting values (i.e. %s, %d etc)
    then translation uses it as well and in the same order.
    """

    def _parse(self, item: str) -> List[str]:
        # https://docs.oracle.com/javase/7/docs/api/java/util/Formatter.html
        # %[argument_index$][flags][width][.precision]conversion
        result = []
        for m in re.finditer(r'(%[a-zA-Z0-9$#+.(-]+)', item):
            result.append(Formatter(m.start(), m.group(1)))
        return result

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup('Formatting values')

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

            # See if we have any formatting values in both lines
            ref_items = self._parse(ref.value)
            trans_items = self._parse(item.value)

            if len(ref_items) == 0 and len(trans_items) == 0:
                # Nothing to check here.
                continue

            if len(trans_items) != len(ref_items):
                report.error(idx + 1, f'"{item.key}": Expected {len(ref_items)} formatters, found {len(trans_items)}.')
                continue

            # Count matches, let's check the order now.
            while len(ref_items) > 0:
                ref_pop = ref_items.pop(0)
                trans_pop = trans_items.pop(0)

                if ref_pop.formatter == trans_pop.formatter:
                    continue

                report.error(f'{idx + 1}:{trans_pop.pos + 1}',
                             f'"{item.key}": Expected "{ref_pop.formatter}", found "{trans_pop.formatter}".')
                break

        return report
