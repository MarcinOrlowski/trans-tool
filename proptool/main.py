"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import copy
import importlib
import inspect
import sys
from pathlib import Path

from proptool.checks.base.check import Check
from proptool.checks.brackets import Brackets
from proptool.checks.key_format import KeyFormat
from proptool.checks.quotation_marks import QuotationMarks
from proptool.checks.trailing_white_chars import TrailingWhiteChars
from proptool.checks.typesetting_quotation_marks import TypesettingQuotationMarks
from proptool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from proptool.config.config_builder import ConfigBuilder
from proptool.prop.file import PropFile
from .const import Const
from .log import Log
from .utils import Utils


# #################################################################################################


class PropTool(object):

    def main(self) -> int:
        # Cannot rely on argparse here as we have required arguments there.
        if '--version' in sys.argv:
            Log.banner(Const.APP_DESCRIPTION)
            return 0

        config = ConfigBuilder.build()
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

            check_modules = [
                TrailingWhiteChars,
                WhiteCharsBeforeLinefeed,
                KeyFormat,
                Brackets,
                QuotationMarks,
                TypesettingQuotationMarks,
            ]
            for validator in check_modules:
                # Almost any check validates translation against reference file, so we cannot use all checks here,
                # but there are some that process single file independently so they in fact do not need any reference
                # file. For them we pass our base file as translation which will do the trick.
                #
                # Each validator gets copy of the files, to prevent any potential destructive operation.
                reference_propfile.report.add((validator(config)).check(copy.copy(reference_propfile)))

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


# #################################################################################################

class Main(object):
    @staticmethod
    def start() -> int:
        app = PropTool()
        return app.main()
