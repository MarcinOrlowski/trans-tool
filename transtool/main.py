"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import copy
import sys
from pathlib import Path

from transtool.config.builder import ConfigBuilder
from transtool.config.config import Config
from transtool.prop.file import PropFile
from .const import Const
from .log import Log
from .utils import Utils


class TransTool(object):

    @staticmethod
    def start() -> int:
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

        if '--config-dump' in sys.argv:
            config.dump()
            return 0

        if not config.files:
            Log.e('No base file(s) specified.')
            return 200  # noqa: WPS432

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
            try:
                reference.load(reference_path)
            except (FileNotFoundError, SyntaxError) as load_base_ex:
                Log.e(str(load_base_ex))
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
            for lang in config.languages:
                translation_path = Path(reference_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                translation = PropFile(config)

                trans_level_label = f'{lang.upper()}: {translation_path}'
                Log.push(trans_level_label, deferred = True)

                try:
                    translation.load(translation_path, lang)
                    # Validate loaded translation file and report any issue detected.
                    if not translation.validate(reference):
                        translation.report.dump()
                        errors += translation.report.errors

                    if config.update:
                        translation.update(reference)
                        translation.save()

                except SyntaxError as load_trans_ex:
                    # We need to stop when loading failed due to syntax error
                    Log.e(str(load_trans_ex))
                    return Const.RC.TRANSLATION_SYNTAX_ERROR

                except FileNotFoundError:
                    # Missing translation file is not a big deal.
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
