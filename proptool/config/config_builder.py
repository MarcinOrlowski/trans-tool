"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import argparse
import importlib
import inspect
from os import listdir
from pathlib import Path
from typing import List, Union

import proptool.checks
from proptool.checks.base.check import Check
from proptool.config.config import Config
from proptool.config.config_reader import ConfigReader
from proptool.const import Const
from proptool.log import Log
from proptool.utils import Utils


class ConfigBuilder(object):
    # List of options that can be either turned on or off.
    _on_off_pairs = [
        'fatal',
        'color',
    ]

    @staticmethod
    def build(config_defaults: Config) -> Config:
        # Set default configuration options for each checker.
        check_dir = Path(proptool.checks.__file__).parent
        check_modules = [file for file in listdir(check_dir) if file[:2] != '__' and (check_dir / file).is_file()]
        for check_file_name in check_modules:
            module = importlib.import_module(f'.{check_file_name[:-3]}', proptool.checks.__name__)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Check) and obj.__name__ != Check.__name__:
                    config_defaults.checks[obj.__name__] = obj.get_default_config(obj)

        # Handler CLI args so we can see if there's config file to load
        args = ConfigBuilder._parse_args()
        if args.config_file:
            config_file = Path(args.config_file[0])
            # override with loaded user config file
            config_defaults = ConfigReader().read(config_defaults, config_file)

        # override with command line arguments
        ConfigBuilder._set_from_args(config_defaults, args)

        ConfigBuilder._validate_config(config_defaults)

        return config_defaults

    @staticmethod
    def _abort(msg: str) -> None:
        Log.e(msg)
        Utils.abort()

    @staticmethod
    def _validate_config(config: Config) -> None:
        if not config.files:
            ConfigBuilder._abort('No base file(s) specified.')
        if not config.languages:
            ConfigBuilder._abort('No language(s) specified.')
        if config.separator not in Config.ALLOWED_SEPARATORS:
            ConfigBuilder._abort('Invalid separator character.')
        if config.comment_marker not in Config.ALLOWED_COMMENT_MARKERS:
            ConfigBuilder._abort('Invalid comment marker.')

    @staticmethod
    def _set_on_off_option(config: Config, args, option_name: str) -> None:
        """
        Changes Config's entry if either --<option> or --<no-option> switch is set.
        If none is set, returns Config object unaltered.

        :param config:
        :param args:
        :param option_name:
        :return:
        """
        if args.__getattribute__(option_name):
            config.__setattr__(option_name, True)
        elif args.__getattribute__(f'no_{option_name}'):
            config.__setattr__(option_name, False)

    @staticmethod
    def _set_from_args(config: Config, args) -> None:
        # At this point it is assumed that args are in valid state, i.e. no mutually
        # exclusive options are both set etc.
        for pair_option_name in ConfigBuilder._on_off_pairs:
            ConfigBuilder._set_on_off_option(config, args, pair_option_name)

        # cmd fix
        config.update = args.update

        # Set optional args, if set by user.
        optionals = [
            'separator',
            'comment_marker',
            'comment_template',
            'quiet',
            'verbose',
        ]
        for option_name in optionals:
            opt_val = args.__getattribute__(option_name)
            if opt_val is not None:
                config.__setattr__(option_name, opt_val)

        # languages
        if args.languages:
            Utils.add_if_not_in_list(config.languages, args.languages)

        # base files
        if args.files:
            ConfigBuilder._add_file_suffix(config, args.files)
            Utils.add_if_not_in_list(config.files, args.files)

    @staticmethod
    def _add_file_suffix(config: Config, files: Union[List[Path], None]) -> None:
        if files:
            suffix_len = len(config.file_suffix)
            for idx, file in enumerate(files):
                # 'PosixPath' object is not subscriptable, so we cannot slice it.
                path_str = str(file)
                if path_str[suffix_len * -1:] != config.file_suffix:
                    files[idx] = Path(f'{path_str}{config.file_suffix}')

    @staticmethod
    def _parse_args() -> argparse:
        parser = argparse.ArgumentParser(prog = Const.APP_NAME.lower(), formatter_class = argparse.RawTextHelpFormatter,
                                         description = '\n'.join(Const.APP_DESCRIPTION))

        group = parser.add_argument_group('Base options')
        group.add_argument('--config', action = 'store', dest = 'config_file', nargs = 1, metavar = 'FILE',
                           help = 'Use specified config file. Note: command line arguments can override config!')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE',
                           help = 'List of base files to check.')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG',
                           help = 'List of languages to check (space separated if more than one, i.e. "de pl").')

        group = parser.add_argument_group('Additional options')
        group.add_argument('--update', action = 'store_true', dest = 'update',
                           help = 'Updates translation files in-place using base file as reference. No backup!')
        # group.add_argument('--pe', '--punctuation-exception', dest = 'punctuation_exception_langs', nargs = '*', metavar = 'LANG',
        #                    help = 'List of languages for which punctuation mismatch should not be checked for, i.e. "jp"')
        group.add_argument('--separator', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1,
                           help = 'If specified, only given CHAR is considered a valid key/value separator.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')
        group.add_argument('--comment', action = 'store', dest = 'comment_marker', metavar = 'CHAR', nargs = 1,
                           help = 'If specified, only given CHAR is considered valid comment marker.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
        group.add_argument('-t', '--template', action = 'store', dest = 'comment_template', metavar = 'TEMPLATE', nargs = 1,
                           help = f'Format of commented-out entries. Default: "{Config.DEFAULT_COMMENT_TEMPLATE}".')
        group.add_argument('--suffix', action = 'store', dest = 'file_suffix', metavar = 'STRING', nargs = 1,
                           help = f'Default file name suffix. Default: "{Config.DEFAULT_FILE_SUFFIX}".')

        group = parser.add_argument_group('Checks controlling options')
        group.add_argument('--checks', action = 'store', dest = 'checks', nargs = '+', metavar = 'CHECK_ID',
                           help = 'List of checks ID to be executed. By default all available checks are run.')

        group.add_argument('-f', '--fatal', action = 'store_true', dest = 'fatal',
                           help = 'Enables strict mode. All warnings are treated as errors and are fatal.')
        group.add_argument('-nf', '--no-fatal', action = 'store_true', dest = 'no_fatal',
                           help = 'Warnings are non-fatal, errors are fatal (default).')

        group = parser.add_argument_group('Application controls')
        group.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet',
                           help = 'Enables quiet mode, muting all output but fatal errors.')
        group.add_argument('-v', '--verbose', action = 'store_true', dest = 'verbose',
                           help = 'Produces more verbose reports.')
        group.add_argument('-d', '--debug', action = 'store_true', dest = 'debug',
                           help = 'Enables debug output.')

        group.add_argument('-c', '--color', action = 'store_true', dest = 'color',
                           help = 'Enables use of ANSI colors (default).')
        group.add_argument('-nc', '--no-color', action = 'store_true', dest = 'no_color',
                           help = 'Disables use of ANSI colors.')

        group = parser.add_argument_group('Misc')
        group.add_argument('--version', action = 'store_true', dest = 'show_version',
                           help = 'Displays application version details and quits.')

        args = parser.parse_args()

        ConfigBuilder._validate_args(args)

        return args

    @staticmethod
    def _validate_args(args):
        # Check use of mutually exclusive pairs
        for option_name in ConfigBuilder._on_off_pairs:
            if args.__getattribute__(option_name) and args.__getattribute__(f'no_{option_name}'):
                ConfigBuilder._abort(f'You cannot use "--{option_name}" and "--no-{option_name}" at the same time.')

        # --quiet vs --verbose
        if args.__getattribute__('quiet') and args.__getattribute__('verbose'):
            ConfigBuilder._abort('You cannot enable "quiet" and "verbose" options both at the same time.')

        # Separator character.
        if args.separator and args.separator not in Config.ALLOWED_SEPARATORS:
            ConfigBuilder._abort(f'Invalid separator. Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')

        # Comment marker character.
        if args.comment_marker and args.comment_marker not in Config.ALLOWED_COMMENT_MARKERS:
            ConfigBuilder._abort(f'Invalid comment marker. Must be one of: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')

        # Comment template.
        if args.comment_template:
            for placeholder in Config.COMMENT_TEMPLATE_LITERALS:
                if args.comment_template.find(placeholder) == -1:
                    ConfigBuilder._abort(f'Missing literal in comment template: "{placeholder}".')
