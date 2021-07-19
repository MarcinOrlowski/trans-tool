"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from pathlib import Path

from .app import App
from .propfile import PropFile
from .util import Util
from .check.trailing_whitechars import TrailingWhiteChars


class Main:
    @staticmethod
    def start() -> int:
        app = App()

        errors = 0
        for file_str in app.files:
            reference_path = Path(file_str)

            tmp = Path(reference_path).name.split('.')
            if len(tmp) != 2:
                Util.abort('Base filename format invalid. Must be "prefix.suffix".')
            name_prefix = tmp[0]
            name_suffix = tmp[1]

            reference_propfile = PropFile(app, reference_path)
            if not reference_propfile.loaded:
                Util.abort(f'File not found: {reference_path}')

            print(f'Base: {reference_path}')
            ref_file_errors = 0
            reference_file_error_count = len(reference_propfile.duplicated_keys_report)
            ref_file_errors += reference_file_error_count

            # Some base file checks
            trailing_chars_report = TrailingWhiteChars.check(app, reference_propfile)
            trailing_chars_count = len(trailing_chars_report)
            errors += trailing_chars_count
            ref_file_errors += trailing_chars_count

            if ref_file_errors > 0:
                Util.error(f'  Found {ref_file_errors} errors in reference file:')
                if reference_file_error_count > 0:
                    Util.error(f'    Duplicated keys: {reference_file_error_count}')
                    if app.verbose:
                        Util.error([f'      {item.to_string()}' for item in reference_propfile.duplicated_keys_report])
                if trailing_chars_count > 0:
                    Util.error(f'    Trailing white characters: {trailing_chars_count}')
                    if app.verbose:
                        Util.error([f'      {item.to_string()}' for item in trailing_chars_report])
            else:
                for lang in app.languages:
                    translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                    translation_propfile = PropFile(app, translation_path, lang)
                    if not translation_propfile.validate_and_fix(reference_propfile):
                        errors += 1

        return 100 if errors else 0
