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
from transtool.report.group import ReportGroup
from transtool.report.items import ReportItem
from .base.check import Check

from transtool.prop.file import PropItem


# noinspection PyUnresolvedReferences
class Substitutions(Check):
    """
    Checks if brackets are used in translation and if so, ensures proper nesting and
    checks if all opened brackets are closed.
    """

    FLAG_DEFAULT = 0
    FLAG_FAIL_WITH_ERROR = -1

    def __init__(self, config: Union[Dict, None] = None):
        super().__init__(config)
        self.is_single_file_check = True

    def _find_most_important_issue(self, idx: int, item: PropItem) -> Union[ReportItem, None]:
        warns = []
        for config in self.config['map']:
            for match in re.finditer(config['regexp'], item.value):
                at = f'{idx + 1}:{match.start()}'

                if 'flag' in config and config['flag'] == self.FLAG_FAIL_WITH_ERROR:
                    msg = f'Invalid sequence "{match.group(1)}".'
                    return ReportGroup.build_error(at, msg, item.key)

                replacement = config['replace']
                msg = f'Sequence at {at} can be replaced with "{replacement}".'
                warns.append(ReportGroup.build_warn(at, msg, item.key))

        return warns[0] if (isinstance(warns, list) and warns) else None

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: 'PropFile' = None) -> ReportGroup:
        self.need_valid_config()

        report = ReportGroup('Substitutions')
        if translation.items:
            report.add([self._find_most_important_issue(idx, item) for idx, item in enumerate(translation.items) if
                        not self._shall_skip_item(item)])

        return report

    @overrides(Check)
    def get_default_config(self) -> Dict:
        return {
            'comments': False,

            # Keep matching elements at the same positions
            'map': [
                {
                    'regexp': r'([\.]{3})',
                    'replace': '…',
                    'flag': self.FLAG_DEFAULT,
                }, {
                    'regexp': r'([\.]{4,})',
                    'flag': self.FLAG_FAIL_WITH_ERROR,
                }, {
                    'regexp': r'([\s]{2,})',
                    'replace': ' ',
                    'flag': self.FLAG_DEFAULT,
                }, {
                    'regexp': r'([\!]{2,})',
                    'replace': '!',
                    'flag': self.FLAG_DEFAULT,
                },
            ],
        }
