"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import List

from ..log import Log

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

    @property
    def warnings(self) -> int:
        """
        Returns cumulative number of warnings in whole report.
        :return:
        """
        result = 0
        for group in self.__groups:
            result += group.warnings
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
        errors = self.errors
        warnings = self.warnings

        label = ''
        sep = ''
        if errors > 0:
            label += f'errors: {errors}'
            sep = ', '
        if warnings > 0:
            label += f'{sep}warnings: {warnings}'

        if label != '':
            label = label[0].upper() + label[1:]

        if errors > 0:
            Log.level_push_e(label)
        else:
            Log.level_push_w(label)

        for entry in self.__groups:
            entry.dump()

        Log.level_pop()
