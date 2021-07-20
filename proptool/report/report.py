"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import List

from ..config import Config
from ..log import Log

from .report_group import ReportGroup


# #################################################################################################

class Report(object):
    def __init__(self, config: Config):
        self._groups: List[ReportGroup] = []
        self.config = config

    @property
    def errors(self) -> int:
        """
        Returns cumulative number of errors in whole report.
        :return:
        """
        return sum(group.errors for group in self._groups)

    @property
    def warnings(self) -> int:
        """
        Returns cumulative number of warnings in whole report.
        :return:
        """
        return sum(group.warnings for group in self._groups)

    def is_fatal(self) -> bool:
        """
        Helper to determine if report contains fatal errors.

        :return:
        """
        cnt = self.errors
        if self.config.fatal:
            cnt += self.warnings
        return cnt > 0

    def add(self, report_group: ReportGroup, skip_empty: bool = True) -> None:
        item_cls = type(report_group)
        if not issubclass(item_cls, ReportGroup):
            raise TypeError(f'Item must be instance of {ReportGroup}. {item_cls} given.')
        if skip_empty and report_group.empty():
            return
        self._groups.append(report_group)

    def empty(self) -> bool:
        return not self._groups

    def dump(self):
        errors = self.errors
        warnings = self.warnings

        if self.config.fatal:
            errors += warnings
            warnings = 0

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
            Log.push_e(label)
        else:
            Log.push_w(label)

        for entry in self._groups:
            entry.dump(self.config.fatal)

        Log.pop()
