"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import Dict, List


class Config(object):
    VERSION = 1

    ALLOWED_SEPARATORS: List[str] = ['=', ':']
    ALLOWED_COMMENT_MARKERS: List[str] = ['#', '!']
    DEFAULT_COMMENT_TEMPLATE: str = 'COM ==> KEY SEP'
    DEFAULT_FILE_SUFFIX: str = '.properties'

    def __init__(self):
        self.file_suffix = Config.DEFAULT_FILE_SUFFIX

        self.fatal = False
        self.strict: bool = False

        self.debug = False
        self.color = True
        self.quiet: bool = False
        self.verbose: bool = False

        self.fix: bool = False

        self.files: List[str] = []
        self.languages: List[str] = []

        self.separator: str = '='

        self.comment_marker: str = '#'
        self.comment_template: str = Config.DEFAULT_COMMENT_TEMPLATE

        self.checks = {
            # empty set
        }

    def add_checker_config(self, key: str, config: Dict) -> None:
        self.checks[key] = config
