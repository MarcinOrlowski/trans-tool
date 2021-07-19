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
from typing import List, Union

from .util import Util


class Config:
    def __init__(self, args: Union[argparse, None] = None):
        self.verbose: bool = False
        self.quiet: bool = False
        self.strict: bool = True
        self.fix: bool = False
        self.files: List[str] = []
        self.languages: List[str] = []
        self.allowed_separators: List[str] = ['=', ':']
        self.separator: str = '='
        self.comment_marker: str = '#'
        self.comment_template: str = 'COM ==> KEY SEP'
        self.allowed_comment_markers: List[str] = ['#', '!']
        self.punctuation_exception_langs: List[str] = []

        if args:
            self.verbose = args.verbose
            self.quiet = args.quiet
            self.strict = args.strict
            self.fix = args.fix
            self.languages = args.languages

            self._from_args(args)

    def _from_args(self, args) -> None:
        # Separator character.
        separator = args.separator[0]
        if separator not in self.allowed_separators:
            Util.abort(f'Invalid separator. Must be one of the following: {self.allowed_separators}')
        self.separator = separator

        # Comment marker character.
        comment = args.comment[0]
        if comment not in self.allowed_comment_markers:
            Util.abort(f'Invalid comment marker. Must be one of the following: {self.allowed_comment_markers}')
        self.comment_marker = comment

        if args.punctuation_exception_langs is not None:
            self.punctuation_exception_langs = args.punctuation_exception_langs

        # Comment template.
        for key in ['COM', 'SEP', 'KEY']:
            if args.comment_template.find(key) == -1:
                Util.abort(f'Missing literal in comment template: {key}')
        self.comment_template = args.comment_template

        # base files
        for file in args.files:
            if file[-11:] != '.properties':
                file += '.properties'
            self.files.append(Path(file))
