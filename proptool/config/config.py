"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Dict, List

from proptool.config.checker_info import CheckerInfo


class Config(object):
    VERSION = 1

    ALLOWED_SEPARATORS: List[str] = ['=', ':']
    ALLOWED_COMMENT_MARKERS: List[str] = ['#', '!']
    COMMENT_TEMPLATE_LITERALS: List[str] = ['COM', 'KEY', 'SEP']
    DEFAULT_COMMENT_TEMPLATE: str = 'COM ==> KEY SEP'
    DEFAULT_FILE_SUFFIX: str = '.properties'

    def __init__(self):
        self.config_file = None

        self.file_suffix = Config.DEFAULT_FILE_SUFFIX

        self.fatal = False

        self.debug = False
        self.color = True
        self.quiet: bool = False
        self.verbose: bool = False

        self.update: bool = False

        self.files: List[str] = []
        self.languages: List[str] = []

        self.separator: str = '='

        self.comment_marker: str = '#'
        self.comment_template: str = Config.DEFAULT_COMMENT_TEMPLATE

        self.checks: List[CheckerInfo] = {
            # empty set. Populated and manipulated by ConfigBuilder
        }

    def set_checker_config(self, checker_id: str, config: Dict) -> None:
        self.checks[checker_id] = config

    def get_checker_config(self, checker_id: str) -> Dict:
        if checker_id not in self.checks:
            raise KeyError(f'No config for {checker_id} found.')
        return self.checks[checker_id]
