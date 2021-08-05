"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import re
from typing import List

from transtool.decorators.overrides import overrides
from transtool.prop.items import Translation
from transtool.report.group import ReportGroup
from .base.check import Check


class Formatter(object):
    def __init__(self, pos: int, formatter: str):
        self.pos = pos
        self.formatter = formatter


# noinspection PyUnresolvedReferences
class FormattingValues(Check):
    """
    This check verifies that if original string uses any %* formatting values (i.e. %s, %d etc)
    then translation uses it as well and in the same order.
    """

    def _parse(self, item: str) -> List[Formatter]:
        # Format String Syntax
        # https://docs.oracle.com/javase/7/docs/api/java/util/Formatter.html
        pattern = r'(%[a-zA-Z0-9$#+.(-]+)'
        return [Formatter(match.start(), match.group(1)) for match in re.finditer(pattern, item)]

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation_file: 'PropFile', reference_file: 'PropFile' = None) -> ReportGroup:
        self.need_both_files(translation_file, reference_file)

        report = ReportGroup('Formatting values')

        for idx, item in enumerate(translation_file.items):
            # We care translations only for now.
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, Translation):
                continue

            # Is there translation of this item present?
            ref = reference_file.find_by_key(item.key)
            # Skip dangling keys
            if not ref:
                continue

            # See if we have any formatting values in both lines
            ref_items = self._parse(ref.value)
            trans_items = self._parse(item.value)

            if not ref_items and not trans_items:
                # Nothing to check here.
                continue

            if len(trans_items) != len(ref_items):
                report.error(idx + 1, f'Expected {len(ref_items)} formatters, found {len(trans_items)}.', item.key)
                continue

            # Count matches, let's check the order now.
            while ref_items:
                ref_pop = ref_items.pop(0)
                trans_pop = trans_items.pop(0)

                if ref_pop.formatter == trans_pop.formatter:
                    continue

                pos = f'{idx + 1}:{trans_pop.pos + 1}'
                report.error(pos, f'Expected "{ref_pop.formatter}", found "{trans_pop.formatter}".', item.key)
                break

        return report
