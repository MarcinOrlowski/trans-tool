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
from proptool.config.config_builder import ConfigBuilder
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

            config_defaults = Config()
            # Configure Log with defaults (i.e. colors etc)
            Log.configure(config_defaults)
            config = ConfigBuilder.build(config_defaults)
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

                reference_propfile = PropFile(config)
                try:  # noqa: WPS505
                    reference_propfile.load(reference_path)
                except FileNotFoundError:
                    Log.e(f'File not found: {reference_path}')
                    Utils.abort()

                # Validate base file.
                for _, checker_info in config.checks.items():
                    # Almost any check validates translation against reference file, so we cannot use all checks here,
                    # but there are some that process single file independently so they in fact do not need any reference
                    # file. For them we pass our base file as translation which will do the trick.
                    checker = checker_info.callable(checker_info.config)
                    if checker.is_single_file_check:
                        # Each validator gets copy of the files, to prevent any potential destructive operation.
                        propfile_copy = copy.copy(reference_propfile)
                        reference_propfile.report.add(checker.check(propfile_copy))

                if not reference_propfile.report.empty():
                    # There's something to fix, but not necessary critical.
                    reference_propfile.report.dump()

                # No reference files errors. Warnings are just fine, though.
                if not reference_propfile.report.is_fatal():
                    for lang in config.languages:
                        translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                        translation_propfile = PropFile(config)

                        try:  # noqa: WPS505
                            translation_propfile.load(translation_path, lang)
                            trans_level_label = f'{lang.upper()}: {translation_path}'
                            Log.push(trans_level_label, deferred = True)

                            is_translation_valid = translation_propfile.is_valid(reference_propfile)

                            if not is_translation_valid:
                                translation_propfile.report.dump()
                                errors += 1

                            if config.update:
                                if translation_propfile.file:
                                    translation_propfile.update(reference_propfile)
                                    translation_propfile.save()

                            if Log.pop():
                                Log.i(f'%ok%{trans_level_label}: OK')
                        except FileNotFoundError:
                            Log.e(f'File not found: {translation_path}')

            # Close main push.
            Log.pop()

            return 100 if errors else 0
        except Exception as ex:
            Log.e(str(ex))
            exc_type, exc_obj, tb = sys.exc_info()
            frame = tb.tb_frame
            Log.e(f'Exception in {frame.f_code.co_filename}:{tb.tb_lineno}')
            return 666  # noqa: WPS432
