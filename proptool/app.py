#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

import argparse
from pathlib import Path
from typing import List

from .const import Const
from .log import Log
from .util import Util


class App:
    def __init__(self, args = None):
        self.verbose: bool = False
        self.quiet: bool = False
        self.strict: bool = True
        self.fix: bool = False
        self.files: List[str] = []
        self.languages: List[str] = []
        self.allowedSeparators: List[str] = ['=', ':']
        self.separator: str = '='
        self.commentMarker: str = '#'
        self.commentTemplate: str = 'COM ==> KEY SEP'
        self.allowedCommentMarkers: List[str] = ['#', '!']
        self.log = Log()

        args = self._parseArgs()

        self.verbose = args.verbose
        self.quiet = args.quiet
        self.strict = args.strict
        self.fix = args.fix
        self.languages = args.languages

        self._fromArgs(args)

    def _fromArgs(self, args):
        # Separator character.
        separator = args.separator[0]
        if separator not in self.allowedSeparators:
            Util.abort(f'Invalid separator. Must be one of the following: {self.allowedSeparators}')
        self.separator = separator

        # Comment marker character.
        comment = args.comment[0]
        if comment not in self.allowedCommentMarkers:
            Util.abort(f'Invalid comment marker. Must be one of the following: {self.allowedCommentMarkers}')
        self.commentMarker = comment

        # Comment template.
        for key in ['COM', 'SEP', 'KEY']:
            if args.commentTemplate.find(key) == -1:
                Util.abort(f'Missing literal in comment template: {key}')
        self.commentTemplate = args.commentTemplate

        if args.verbose:
            print(f'Comment Template: ${self.commentTemplate}')

        # base files
        for file in args.files:
            if file[-11:] != '.properties':
                file += '.properties'
            self.files.append(Path(file))

    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            prog = Const.APP_NAME.lower(),
            description = f'{Const.APP_NAME} v{Const.APP_VERSION} * Copyright 2021 by Marcin Orlowski.\n' +
                          'Java properties file checker and syncing tool.\n' +
                          f'{Const.APP_URL}',
            formatter_class = argparse.RawTextHelpFormatter)

        group = parser.add_argument_group('Options')
        # group.add_argument('--config', action = 'store', dest = 'config', nargs = 1, metavar = 'FILE',
        #                    help = 'Use specified config file. Note command line arguments can override config!')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG', required = True,
                           help = f'List of languages to check (space separated if more than one, i.e. "de pl").')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE', required = True,
                           help = f'List of base files to check.')
        group.add_argument('--fix', action = 'store_true', dest = 'fix',
                           help = "Updated translation files in-place. No backup!")
        group.add_argument('-s', '--strict', action = 'store_true', dest = 'strict',
                           help = 'Controls strict validation mode.')
        group.add_argument('--sep', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1, default = '=',
                           help = 'If specified, only given CHAR is considered a valid separator.'
                                  + f'Must be one of the following: {", ".join(self.allowedSeparators)}')
        group.add_argument('-c', '--com', action = 'store', dest = 'comment', metavar = 'CHAR', nargs = 1, default = '#',
                           help = 'If specified, only given CHAR is considered va alid comment marker. '
                                  + f'Must be one of the following: {", ".join(self.allowedCommentMarkers)}')
        group.add_argument('-t', '--tpl', action = 'store', dest = 'commentTemplate', metavar = 'TEMPLATE', nargs = 1,
                           default = self.commentTemplate,
                           help = f'Format of commented-out entries. Default: "{self.commentTemplate}"')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports')

        return parser.parse_args()
