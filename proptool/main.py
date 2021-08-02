"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import copy
import sys
from pathlib import Path

from proptool.config.config import Config
from proptool.config.builder import ConfigBuilder
from proptool.prop.file import PropFile
from .const import Const
from .log import Log
from .utils import Utils


# #################################################################################################


class PropTool(object):

    @staticmethod
    def start() -> int:
        try:
            # Cannot rely on argparse here as we have required arguments there.
            if '--version' in sys.argv:
                Log.banner(Const.APP_DESCRIPTION)
                return 0

            # Config with built-in defaults
            config = Config()
            # Configure Log with defaults (i.e. colors etc)
            Log.configure(config)
            # Parse args and update the config if needed
            ConfigBuilder.build(config)
            # Reconfigure once we got user settings handled.
            Log.configure(config)

            errors = 0
            for file_str in config.files:
                reference_path = Path(file_str)

                tmp = Path(reference_path).name.split('.')
                if len(tmp) != 2:
                    Log.e('Base filename format invalid. Must be "prefix.suffix".')
                    Utils.abort()
                name_prefix = tmp[0]
                name_suffix = tmp[1]

                # Main push
                Log.push(f'Base: {reference_path}')

                reference = PropFile(config)
                try:  # noqa: WPS505
                    reference.load(reference_path)
                except FileNotFoundError:
                    Log.e(f'File not found: {reference_path}')
                    Utils.abort()

                # Validate base file.
                checks_executed = 0
                for _, checker_info in config.checks.items():
                    # Almost any check validates translation against reference file, so we cannot use all checks here,
                    # but there are some that process single file independently so they in fact do not need any reference
                    # file. For them we pass our base file as translation which will do the trick.
                    checker = checker_info.callable(checker_info.config)
                    if checker.is_single_file_check:
                        # Each validator gets copy of the files, to prevent any potential destructive operation.
                        reference_copy = copy.copy(reference)
                        reference.report.add(checker.check(reference_copy))
                        checks_executed += 1

                if reference.report.not_empty():
                    # There's something to fix, but not necessary critical.
                    reference.report.dump()
                else:
                    Log.v(f'Checks passed: {checks_executed}.')

                # No reference files errors. Warnings are just fine, though.
                if reference.report.is_ok():
                    for lang in config.languages:
                        translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                        translation = PropFile(config)

                        trans_level_label = f'{lang.upper()}: {translation_path}'
                        Log.push(trans_level_label, deferred = True)

                        if translation_path.exists():
                            # Load translation file.
                            translation.load(translation_path, lang)

                            is_translation_valid = translation.is_valid(reference)

                            if not is_translation_valid:
                                translation.report.dump()
                                errors += 1

                            if config.update:
                                if translation.file:
                                    translation.update(reference)
                                    translation.save()
                        else:
                            if config.create:
                                translation.update(reference)
                                Log.push('Creating new translation file')
                                translation.save(translation_path)
                                Log.pop()
                            else:
                                Log.e(f'File not found: {translation_path}')

                        if Log.pop():
                            Log.i(f'%ok%{trans_level_label}: OK')

            # Close main push.
            Log.pop()

            # Done.
            return 100 if errors else 0

        # Last-resort exceptin catcher.
        except Exception as ex:
            Log.e(str(ex))
            exc_type, exc_obj, tb = sys.exc_info()
            frame = tb.tb_frame
            Log.e(f'Exception in {frame.f_code.co_filename}:{tb.tb_lineno}')
            return 666  # noqa: WPS432
