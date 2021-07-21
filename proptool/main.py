"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import argparse
import copy
import sys
from pathlib import Path

from .checks.brackets import Brackets
from .checks.key_format import KeyFormat
from .checks.trailing_white_chars import TrailingWhiteChars
from .checks.quotation_marks import QuotationMarks
from .checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from .config import Config
from .const import Const
from .log import Log
from .utils import Utils
from .propfile import PropFile


class PropTool(object):
    @staticmethod
    def _parse_args() -> argparse:
        parser = argparse.ArgumentParser(prog = Const.APP_NAME.lower(), formatter_class = argparse.RawTextHelpFormatter,
                                         description = '\n'.join(Const.APP_DESCRIPTION))

        group = parser.add_argument_group('Options')
        # group.add_argument('--config', action = 'store', dest = 'config', nargs = 1, metavar = 'FILE',
        #                    help = 'Use specified config file. Note command line arguments can override config!')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE',
                           help = 'List of base files to check.')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG', required = True,
                           help = 'List of languages to check (space separated if more than one, i.e. "de pl").')
        group.add_argument('--fix', action = 'store_true', dest = 'fix',
                           help = 'Updated translation files in-place. No backup!')
        group.add_argument('--pe', '--punctuation-exception', dest = 'punctuation_exception_langs', nargs = '*', metavar = 'LANG',
                           help = 'List of languages for which punctuation mismatch should not be checked for, i.e. "jp"')
        group.add_argument('-s', '--strict', action = 'store_true', dest = 'strict',
                           help = 'Controls strict validation mode.')
        group.add_argument('--sep', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1, default = '=',
                           help = 'If specified, only given CHAR is considered a valid separator.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')
        group.add_argument('-c', '--com', action = 'store', dest = 'comment', metavar = 'CHAR', nargs = 1, default = '#',
                           help = 'If specified, only given CHAR is considered va alid comment marker. '
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
        group.add_argument('-t', '--tpl', action = 'store', dest = 'comment_template', metavar = 'TEMPLATE', nargs = 1,
                           default = Config.DEFAULT_COMMENT_TEMPLATE,
                           help = f'Format of commented-out entries. Default: "{Config.DEFAULT_COMMENT_TEMPLATE}"')
        group.add_argument('-f', '--fatal', action = 'store_true', dest = 'fatal',
                           help = 'All warnings are fatal (as errors)')

        group = parser.add_argument_group('Other')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports')
        group.add_argument('-d', '--debug', action = 'store_true', dest = 'debug',
                           help = 'Enables debug output')
        group.add_argument('-nc', '--no-color', action = 'store_true', dest = 'no_color',
                           help = 'Disables use of ANSI colors.')
        group.add_argument('--version', action = 'store_true', dest = 'show_version',
                           help = 'Displays application version details and quits.')

        return parser.parse_args()

    def main(self) -> int:
        # Cannot rely on argparse here as we have required arguments there.
        if '--version' in sys.argv:
            Log.banner(Const.APP_DESCRIPTION)
            return 0

        config = Config(self._parse_args())
        Log.configure(config)

        errors = 0
        for file_str in config.files:
            reference_path = Path(file_str)

            tmp = Path(reference_path).name.split('.')
            if len(tmp) != 2:
                Utils.abort('Base filename format invalid. Must be "prefix.suffix".')
            name_prefix = tmp[0]
            name_suffix = tmp[1]

            Log.push(f'Base: {reference_path}')
            reference_propfile = PropFile(config, reference_path)
            if not reference_propfile.loaded:
                Utils.abort(f'File not found: {reference_path}')

            checks = [
                TrailingWhiteChars,
                WhiteCharsBeforeLinefeed,
                KeyFormat,
                Brackets,
                QuotationMarks,
            ]
            for validator in checks:
                # Almost any check validates translation against reference file, so we cannot use all here,
                # but we can use those which in fact do not need reference file. For them we pass our base
                # file as translation which will do the trick.
                #
                # Each validator gets copy of the files, to prevent any potential destructive operation.
                reference_propfile.report.add((validator(config)).check(None, copy.copy(reference_propfile)))

            if not reference_propfile.report.empty():
                # There's something to fix, but not necessary critical.
                reference_propfile.report.dump()

            # No errors, no problem. Warnings are just fine.
            if not reference_propfile.report.is_fatal():
                for lang in config.languages:
                    translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                    translation_propfile = PropFile(config, translation_path, lang)

                    trans_level_label = f'{lang.upper()}: {translation_path}'
                    Log.push(trans_level_label, deferred = True)
                    if not translation_propfile.validate_and_fix(reference_propfile):
                        translation_propfile.report.dump()
                        errors += 1
                    if Log.pop():
                        Log.i(f'%ok%{trans_level_label}: OK')

            Log.pop()

        return 100 if errors else 0


class Main(object):
    @staticmethod
    def start() -> int:
        app = PropTool()
        return app.main()
