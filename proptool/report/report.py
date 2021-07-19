"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import List

from .report_group import ReportGroup


# #################################################################################################

class Report:
    def __init__(self):
        self.__groups: List[ReportGroup] = []

    @property
    def errors(self) -> int:
        """
        Returns cumulative number of errors in whole report.
        :return:
        """
        result = 0
        for group in self.__groups:
            result += group.errors
        return result

    def add(self, report_group: ReportGroup, skip_empty: bool = True) -> None:
        item_cls = type(report_group)
        if not issubclass(item_cls, ReportGroup):
            raise TypeError(f'Item must be instance of {ReportGroup}. {item_cls} given.')
        if skip_empty and report_group.empty():
            return
        self.__groups.append(report_group)

    def empty(self) -> bool:
        return len(self.__groups) == 0

    def dump(self):
        for entry in self.__groups:
            entry.dump()
