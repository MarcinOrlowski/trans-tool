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

from .config import Config
from .const import Const
from .log import Log
from .propfile import PropFile
from .check.trailing_whitechars import TrailingWhiteChars


class PropTool:
    def _parse_args(self) -> argparse:
        parser = argparse.ArgumentParser(
            prog = Const.APP_NAME.lower(),
            description = f'{Const.APP_NAME} v{Const.APP_VERSION} * Copyright 2021 by Marcin Orlowski.\n' +
                          'Java properties file checker and syncing tool.\n' +
                          f'{Const.APP_URL}',
            formatter_class = argparse.RawTextHelpFormatter)

        group = parser.add_argument_group('Options')
        # group.add_argument('--config', action = 'store', dest = 'config', nargs = 1, metavar = 'FILE',
        #                    help = 'Use specified config file. Note command line arguments can override config!')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE',
                           help = f'List of base files to check.')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG', required = True,
                           help = f'List of languages to check (space separated if more than one, i.e. "de pl").')
        group.add_argument('--fix', action = 'store_true', dest = 'fix',
                           help = "Updated translation files in-place. No backup!")
        group.add_argument('--pe', '--punctuation-exception', dest = 'punctuation_exception_langs', nargs = '*', metavar = 'LANG',
                           help = f'List of languages for which punctuation mismatch should not be checked for, i.e. "jp"')
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

        group = parser.add_argument_group('Other')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports')
        group.add_argument('--debug', action = 'store_true', dest = 'debug',
                           help = 'Enables debug output')

        return parser.parse_args()

    def main(self) -> int:
        config = Config(self._parse_args())

        errors = 0
        for file_str in config.files:
            reference_path = Path(file_str)

            tmp = Path(reference_path).name.split('.')
            if len(tmp) != 2:
                Log.abort('Base filename format invalid. Must be "prefix.suffix".')
            name_prefix = tmp[0]
            name_suffix = tmp[1]

            Log.level_push(f'Base: {reference_path}')
            reference_propfile = PropFile(config, reference_path)
            if not reference_propfile.loaded:
                Log.abort(f'File not found: {reference_path}')

            ref_file_errors = 0
            reference_file_error_count = len(reference_propfile.duplicated_keys_report)
            ref_file_errors += reference_file_error_count

            # Some base file checks
            trailing_chars_report = TrailingWhiteChars.check(config, reference_propfile)
            trailing_chars_count = len(trailing_chars_report)
            errors += trailing_chars_count
            ref_file_errors += trailing_chars_count

            if ref_file_errors > 0:
                Log.level_push(f'Found {ref_file_errors} errors in reference file:')

                if reference_file_error_count > 0:
                    Log.e(f'Duplicated keys: {reference_file_error_count}')
                    if config.verbose:
                        Log.e([f'{item.to_string()}' for item in reference_propfile.duplicated_keys_report])
                    Log.level_pop()

                if trailing_chars_count > 0:
                    Log.level_push(f'Trailing white characters: {trailing_chars_count}')
                    if config.verbose:
                        Log.e([f'{item.to_string()}' for item in trailing_chars_report])
                    Log.level_pop()

                Log.level_pop()
            else:
                for lang in config.languages:
                    translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                    translation_propfile = PropFile(config, translation_path, lang)
                    Log.level_push(translation_path)
                    if not translation_propfile.validate_and_fix(reference_propfile):
                        errors += 1
                    Log.level_pop()

            Log.level_pop()

        return 100 if errors else 0


class Main:
    @staticmethod
    def start() -> int:
        app = PropTool()
        return app.main()
