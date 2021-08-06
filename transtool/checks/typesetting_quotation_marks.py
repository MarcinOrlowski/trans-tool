"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Dict, List, Union

from transtool.decorators.overrides import overrides
from transtool.report.group import ReportGroup
from .brackets import Brackets


# noinspection PyUnresolvedReferences
class TypesettingQuotationMarks(Brackets):
    """
    Checks if print quotation marks (the ones having different opening and closing marks) are used in translation and if so,
    ensures proper nesting and checks if all opened brackets are closed.
    """

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    report_title = ReportGroup('Print Quotation Marks')

    opening: List[str] = ['‘', '«', '„', '「', '《']
    closing: List[str] = ['’', '»', '“', '」', '》']

    @overrides(Brackets)
    def get_default_config(self) -> Dict:
        return {
            'comments': False,

            # Keep matching elements at the same positions
            # List based on:
            # * https://www.overleaf.com/learn/latex/Typesetting_quotations#Reference_guide
            # * https://en.wikipedia.org/wiki/Quotation_mark
            # BUG: https://github.com/MarcinOrlowski/trans-tool/issues/19
            'opening': ['‘', '«', '„', '「', '《'],
            'closing': ['’', '»', '“', '」', '》'],

            # For compatibility with Brackets.
            'ignore_quoted':   False,
            'quotation_marks': [],
        }
