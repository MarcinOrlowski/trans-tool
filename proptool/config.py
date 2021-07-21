"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import argparse
from pathlib import Path
from typing import List

from .utils import Utils


class Config(object):
    ALLOWED_SEPARATORS: List[str] = ['=', ':']
    ALLOWED_COMMENT_MARKERS: List[str] = ['#', '!']
    DEFAULT_COMMENT_TEMPLATE: str = 'COM ==> KEY SEP'

    def __init__(self, args: argparse = None):
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
        self.strict: bool = False
        self.verbose: bool = False

        self.checks = {
            'KeyFormat': {
                'pattern': r'^[a-z]+[a-zA-Z0-9_.]*[a-zA-Z0-9]+$',
            },
            'Punctuation': {
                'chars': ['.', '?', '!', ':', r'\n'],
            },
        }

        if args:
            self.debug = args.debug
            self.fatal = args.fatal
            self.fix = args.fix
            self.languages = args.languages
            self.no_color = args.no_color
            self.quiet = args.quiet
            self.strict = args.strict
            self.verbose = args.verbose

            # Separator character.
            separator = args.separator[0]
            if separator not in Config.ALLOWED_SEPARATORS:
                Utils.abort(f'Invalid separator. Must be one of the following: {Config.ALLOWED_SEPARATORS}')
            self.separator = separator

            # Comment marker character.
            comment = args.comment[0]
            if comment not in Config.ALLOWED_COMMENT_MARKERS:
                Utils.abort(f'Invalid comment marker. Must be one of the following: {Config.ALLOWED_COMMENT_MARKERS}')
            self.comment_marker = comment

            if args.punctuation_exception_langs is not None:
                self.punctuation_exception_langs = args.punctuation_exception_langs

            # Comment template.
            for placeholder in ('COM', 'SEP', 'KEY'):
                if args.comment_template.find(placeholder) == -1:
                    Utils.abort(f'Missing literal in comment template: {placeholder}')
            self.comment_template = args.comment_template

            # base files
            suffix = '.properties'
            suffix_len = len(suffix)
            for file in args.files:
                if file[suffix_len * -1:] != suffix:
                    file += suffix
                self.files.append(str(Path(file)))
