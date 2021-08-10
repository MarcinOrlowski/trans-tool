"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import argparse
import re
from pathlib import Path
from typing import List, Union

from transtool.checks.brackets import Brackets
from transtool.checks.dangling_keys import DanglingKeys
from transtool.checks.empty_translations import EmptyTranslations
from transtool.checks.formatting_values import FormattingValues
from transtool.checks.key_format import KeyFormat
from transtool.checks.missing_translations import MissingTranslations
from transtool.checks.punctuation import Punctuation
from transtool.checks.quotation_marks import QuotationMarks
from transtool.checks.starts_with_the_same_case import StartsWithTheSameCase
from transtool.checks.trailing_white_chars import TrailingWhiteChars
from transtool.checks.substitutions import Substitutions
from transtool.checks.typesetting_quotation_marks import TypesettingQuotationMarks
from transtool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from transtool.config.checker_info import CheckerInfo
from transtool.config.config import Config
from transtool.config.reader import ConfigReader
from transtool.const import Const
from transtool.log import Log
from transtool.utils import Utils


class ConfigBuilder(object):
    # List of options that can be either turned on or off.
    _on_off_pairs = [
        'color',
        'fatal',
    ]

    _default_checkers = [
        Brackets,
        DanglingKeys,
        EmptyTranslations,
        FormattingValues,
        KeyFormat,
        MissingTranslations,
        Punctuation,
        QuotationMarks,
        StartsWithTheSameCase,
        Substitutions,
        TrailingWhiteChars,
        TypesettingQuotationMarks,
        WhiteCharsBeforeLinefeed,
    ]

    @staticmethod
    def build(config_defaults: Config):
        # Let's populate default config with all the supported checkers first
        ConfigBuilder._setup_checkers(config_defaults)

        # Handler CLI args so we can see if there's config file to load
        args = ConfigBuilder._parse_args()
        if args.config_file:
            config_file = Path(args.config_file[0])
            # override with loaded user config file
            config_defaults = ConfigReader().read(config_defaults, config_file)

        # override with command line arguments
        ConfigBuilder._set_from_args(config_defaults, args)

        ConfigBuilder._get_checkers_from_args(config_defaults, args.checkers)

        ConfigBuilder._validate_config(config_defaults)

    @staticmethod
    def _setup_checkers(config: Config, checkers_list: Union[List[str], None] = None) -> None:
        if checkers_list is None:
            checkers_list = ConfigBuilder._default_checkers
        for checker in checkers_list:
            checker_id = checker.__name__
            config.checks[checker_id] = CheckerInfo(checker_id, checker, (checker()).get_default_config())

    @staticmethod
    def _abort(msg: str) -> None:
        Log.e(msg)
        Utils.abort()

    @staticmethod
    def _validate_config(config: Config) -> None:
        if config.languages:
            pattern = re.compile(r'^[a-z]{2,}$')
            for lang in config.languages:
                if not pattern.match(lang):
                    ConfigBuilder._abort(f'Invalid language: "{lang}".')

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
        config.create = args.create
        config.write_reference = args.write_reference

        # Set optional args, if set by user.
        optionals = [
            'separator',
            'comment_marker',
            'quiet',
            'verbose',
            'file_suffix',
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
    def _get_checkers_from_args(config: Config, args_checkers: Union[List[str], None]) -> None:
        """
        If `--checks` argument list is provided, used checkers will be adjusted according to
        values (Checker IDs) provided.
        :param config:
        :param args_checkers:
        """
        all_checkers = {checker.__name__.lower(): checker for checker in ConfigBuilder._default_checkers}
        if args_checkers:
            checkers = []
            for checker_id in args_checkers:
                if checker_id.lower() not in all_checkers:
                    ConfigBuilder._abort(f'Unknown checker ID "{checker_id}".')
                Utils.add_if_not_in_list(checkers, checker_id)
            ConfigBuilder._setup_checkers(config, checkers)

    @staticmethod
    def _add_file_suffix(config: Config, files: Union[List[Path], None]) -> None:
        if files:
            suffix_len = len(config.file_suffix)
            for idx, file in enumerate(files):
                # 'PosixPath' object cannot be sliced.
                path_str = str(file)
                if path_str[suffix_len * -1:] != config.file_suffix:
                    files[idx] = Path(f'{path_str}{config.file_suffix}')

    @staticmethod
    def _parse_args() -> argparse:
        parser = argparse.ArgumentParser(prog = Const.APP_NAME.lower(), formatter_class = argparse.RawTextHelpFormatter,
                                         description = '\n'.join(Const.APP_DESCRIPTION))

        group = parser.add_argument_group('Base options')
        group.add_argument('--config', action = 'store', dest = 'config_file', nargs = 1, metavar = 'FILE',
                           help = 'Use specified config file. Command line arguments override config settings.')
        group.add_argument('--config-dump', action = 'store_true', dest = 'config_dump',
                           help = 'Print config as seen by the app once config file and args are parsed.')
        group.add_argument('-b', '--base', action = 'store', dest = 'files', nargs = '+', metavar = 'FILE',
                           help = 'List of base files to check.')
        group.add_argument('-l', '--lang', action = 'store', dest = 'languages', nargs = '+', metavar = 'LANG',
                           help = 'List of languages to check (space separated if more than one, i.e. "de pl").')

        group = parser.add_argument_group('Additional options')
        group.add_argument('--update', action = 'store_true', dest = 'update',
                           help = 'Updates existing translation files in-place using base file as reference.')
        group.add_argument('--create', action = 'store_true', dest = 'create',
                           help = 'Creates new translation files using base file as reference if no file exists.')
        group.add_argument('-wr', '--write-reference', action = 'store_true', dest = 'write_reference',
                           help = 'Includes comments with reference values from base string for every translation entry.')
        group.add_argument('--separator', action = 'store', dest = 'separator', metavar = 'CHAR', nargs = 1,
                           help = 'If specified, only given CHAR is considered a valid key/value separator.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')
        group.add_argument('--comment', action = 'store', dest = 'comment_marker', metavar = 'CHAR', nargs = 1,
                           help = 'If specified, only given CHAR is considered valid comment marker.'
                                  + f'Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
        group.add_argument('--suffix', action = 'store', dest = 'file_suffix', metavar = 'STRING', nargs = 1,
                           help = f'Default file name suffix. Default: "{Config.DEFAULT_FILE_SUFFIX}".')

        group = parser.add_argument_group('Checks controlling options')
        group.add_argument('--checks', action = 'store', dest = 'checkers', nargs = '+', metavar = 'CHECK_ID',
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

        # If user separated languages with comma instead of space, lets do some magic for it to work too.
        args.languages = ConfigBuilder._process_comma_separated_langs(args.languages)

        ConfigBuilder._validate_args(args)

        return args

    @staticmethod
    def _process_comma_separated_langs(languages: Union[List[str], None]) -> Union[List[str], None]:
        if languages is None:
            return None

        result = []
        for lang in languages:
            tmp = lang.split(',')
            if len(tmp) > 1:
                _ = [result.append(code) for code in tmp if code.strip() != '']  # noqa: WPS122
            else:
                result.append(lang)

        return result

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
