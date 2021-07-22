"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import List

from proptool.report.group import ReportGroup
from .brackets import Brackets


# noinspection PyUnresolvedReferences
class TypesettingQuotationMarks(Brackets):
    """
    Checks if print quotation marks (the ones having different opening and closing marks) are used in translation and if so,
    ensures proper nesting and checks if all opened brackets are closed.
    """

    report_title = ReportGroup('Print Quotation Marks')

    # Keep matching elements at the same positions (and in order preserving container!)
    # List based on:
    # * https://www.overleaf.com/learn/latex/Typesetting_quotations#Reference_guide
    # * https://en.wikipedia.org/wiki/Quotation_mark
    # BUG: https://github.com/MarcinOrlowski/prop-tool/issues/19
    opening: List[str] = ['‘', '«', '„', '「', '《']
    closing: List[str] = ['’', '»', '“', '」', '》']
