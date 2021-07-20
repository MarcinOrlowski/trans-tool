"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import List

from proptool.config import Config


class FakeConfig(Config):
    def __init__(self):
        self.comment_marker: str = '#'
        self.comment_template: str = Config.DEFAULT_COMMENT_TEMPLATE
        self.debug = False
        self.debug_verbose = 1  # Log.VERBOSE_NORMAL
        self.fatal = False
        self.files: List[str] = []
        self.fix: bool = False
        self.languages: List[str] = []
        self.no_color = False
        self.punctuation_exception_langs: List[str] = []
        self.quiet: bool = False
        self.separator: str = '='
        self.strict: bool = True
        self.verbose: bool = False
