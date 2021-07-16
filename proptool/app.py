#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool
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
        self.log = Log()

        args = self._parseArgs()

        self.verbose = args.verbose
        self.quiet = args.quiet
        self.strict = args.strict
        self.fix = args.fix
        self.languages = args.languages
        self._setSeparatorFromArgs(args.separator)

        self.files = self._processFiles(args.files)

    def _processFiles(self, files: List[str]):
        tmp = []
        for file in files:
            if file[-11:] != '.properties':
                file += '.properties'
            tmp.append(Path(file))

        return tmp

    def _setSeparatorFromArgs(self, args):
        if args:
            separator = args.separator[0]
            if separator in self.allowedSeparators:
                self.separator = separator
            else:
                Util.abort(f'Invalid separator. Must be one of the following: {self.allowedSeparators}')

    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            prog = Const.APP_NAME.lower(),
            description = f'{Const.APP_NAME} v{Const.APP_VERSION} * Copyright 2021 by Marcin Orlowski.\n' +
                          'Java properties file checker and syncing tool.\n' +
                          f'{Const.APP_URL}',
            formatter_class = argparse.RawTextHelpFormatter)

        group = parser.add_argument_group('Options')
        group.add_argument('-c', '--config', action = 'store', dest = 'config', nargs = 1, metavar = 'FILE',
                           help = 'Use specified config file. Note command line arguments can override config!')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG', required = True,
                           help = f'List of languages to check (space separated if more than one, i.e. "de pl").')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE', required = True,
                           help = f'List of base files to check.')
        group.add_argument('--fix', action = 'store_true', dest = 'fix',
                           help = "Updated translation files in-place. No backup!")
        group.add_argument('-s', '--strict', action = 'store_true', dest = 'strict',
                           help = 'Controls strict validation mode.')
        group.add_argument('--sep', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1,
                           help = 'If specified, only given CHAR is considerd valid separator.')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports')

        args = parser.parse_args()

        return args
