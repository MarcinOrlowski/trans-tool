"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

import inspect
import os
import re
import sys
from pathlib import PosixPath
from typing import List

from .config import Config


class Log(object):
    # ---------------------------------------------------------------------------------------------------------------

    # www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    ANSI_BOLD = u'\u001b[1m'
    ANSI_UNDERLINE = u'\u001b[4m'
    ANSI_REVERSE = u'\u001b[7m'

    ANSI_BLACK = u'\u001b[30m'
    ANSI_BLACK_BRIGHT = u'\u001b[1;30m'
    ANSI_RED = u'\u001b[31m'
    ANSI_RED_BRIGHT = u'\u001b[1;31m'
    ANSI_GREEN = u'\u001b[32m'
    ANSI_GREEN_BRIGHT = u'\u001b[1;32m'
    ANSI_YELLOW = u'\u001b[33m'
    ANSI_YELLOW_BRIGHT = u'\u001b[1;33m'
    ANSI_BLUE = u'\u001b[34m'
    ANSI_BLUE_BRIGHT = u'\u001b[1;34m'
    ANSI_MAGENTA = u'\u001b[35m'
    ANSI_MAGENTA_BRIGHT = u'\u001b[1;35m'
    ANSI_CYAN = u'\u001b[36m'
    ANSI_CYAN_BRIGHT = u'\u001b[1;36m'
    ANSI_WHITE = u'\u001b[37m'
    ANSI_WHITE_BRIGHT = u'\u001b[1;37m'

    ANSI_BG_MAGENTA = u'\u001b[45m'
    ANSI_BG_CYAN = u'\u001b[46m'

    ANSI_RESET = u'\u001b[0m'

    COLOR_ERROR = ANSI_RED
    COLOR_WARN = ANSI_YELLOW
    COLOR_NOTICE = ANSI_CYAN
    COLOR_INFO = None
    COLOR_OK = ANSI_GREEN
    COLOR_DEBUG = ANSI_REVERSE
    COLOR_BANNER = (ANSI_WHITE + ANSI_REVERSE)

    # ---------------------------------------------------------------------------------------------------------------
    deferred_log_level = None
    deferred_log_entry = None
    last_log_entry_level = 0
    log_level = 0
    log_entries = []

    VERBOSE_NONE = 0
    VERBOSE_NORMAL = 1
    VERBOSE_VERY = 2

    verbose_level = VERBOSE_NONE
    debug_level = VERBOSE_NONE
    no_color = False
    quiet = False
    skip_empty_lines = False
    buffer_enabled = True

    @classmethod
    def configure(cls, config: Config):
        verbose_level = Log.VERBOSE_NONE
        if config.verbose:
            verbose_level = Log.VERBOSE_NORMAL
        # if args.very_verbose:
        #     verbose_level = Log.VERBOSE_VERY
        cls.verbose_level = verbose_level

        cls.skip_empty_lines = False
        cls.no_color = False
        cls.quiet = False
        cls.buffer_enabled = True
        cls.debug = False

        debug_level = Log.VERBOSE_NONE
        if config.debug:
            debug_level = Log.VERBOSE_NORMAL
        elif config.debug_verbose:
            debug_level = Log.VERBOSE_VERY
        cls.debug_level = debug_level

        if config.debug and os.getenv('PYTHONDONTWRITEBYTECODE') is None:
            Log.e([
                'Creation of *.pyc files is enabled in your current env.',
                'This affects debug() calls and will produce invalid',
                'file name and line number being shown during execution.',

                'To disable this, set env variable:',
                '   export PYTHONDONTWRITEBYTECODE=1',
            ])

    # ---------------------------------------------------------------------------------------------------------------

    @classmethod
    def disable_buffer(cls):
        cls.buffer_enabled = False

    @classmethod
    def enable_buffer(cls):
        cls.buffer_enabled = True

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def level_init(message = None, color = None, ignore_quiet_switch = False):
        Log.log_level = 0
        Log.level_push(message, color, ignore_quiet_switch)

    @staticmethod
    def level_push(message = None, color = None, ignore_quiet_switch = False, deferred = False):
        if Log.verbose_level == Log.VERBOSE_NONE and deferred:
            Log._flush_deferred_entry()

            Log.deferred_log_level = Log.log_level
            Log.deferred_log_entry = Log._format_log_line(message, color)
        else:
            Log._log(message, color, ignore_quiet_switch)

        Log.log_level += 1

    @staticmethod
    def level_push_e(message = None, color = None, ignore_quiet_switch = False, deferred = False):
        Log.level_push(f'%error%%reverse%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def level_push_w(message = None, color = None, ignore_quiet_switch = False, deferred = False):
        Log.level_push(f'%warn%%reverse%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def level_push_ok(message = None, color = None, ignore_quiet_switch = False, deferred = False):
        Log.level_push(f'%ok%%reverse%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def level_push_v(message = None, color = None, ignore_quiet_switch = False, deferred = False):
        if Log.is_verbose():
            Log.level_push(message, color, ignore_quiet_switch, deferred)

    @staticmethod
    def level_pop(messages = None, color = None, ignore_quiet_switch = False) -> bool:
        if messages is not None:
            Log.i(messages = messages, color = color, ignore_quiet_switch = ignore_quiet_switch)

        had_anything_deferred = Log._flush_deferred_entry()

        if Log.log_level == 0:
            Log.abort('level_pop() called too many times')
        Log.log_level -= 1

        return had_anything_deferred

    @staticmethod
    def level_pop_v(messages = None, color = None, ignore_quiet_switch = False):
        if Log.is_verbose():
            Log.level_pop(messages, color, ignore_quiet_switch)

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_verbose() -> bool:
        return Log.verbose_level >= Log.VERBOSE_NORMAL

    @staticmethod
    def is_very_verbose() -> bool:
        return Log.verbose_level >= Log.VERBOSE_VERY

    @staticmethod
    def is_debug() -> bool:
        return Log.debug_level >= Log.VERBOSE_NORMAL

    @staticmethod
    def is_debug_verbose() -> bool:
        return Log.debug_level >= Log.VERBOSE_VERY

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def banner(messages, ignore_quiet_switch: bool = False, add_to_history: bool = True, top: bool = True, bottom: bool = True):
        tmp = Log._to_list(messages)
        max_len = len(max(tmp, key = len))

        line = '=' * max_len

        messages: List[str] = []

        if top:
            messages.append(line)

        messages.extend(tmp)

        if bottom:
            messages.append(line)

        Log._log(messages, None, ignore_quiet_switch, add_to_history)

    @staticmethod
    def banner_v(messages, ignore_quiet_switch: bool = False, add_to_history: bool = True, top: bool = True, bottom: bool = True):
        if Log.verbose_level >= Log.VERBOSE_NORMAL:
            Log.banner(messages, ignore_quiet_switch, add_to_history, top, bottom)

    @staticmethod
    def i(messages = None, color: str = COLOR_INFO, ignore_quiet_switch: bool = False, add_to_history: bool = True):
        Log._log(messages, color, ignore_quiet_switch, add_to_history)

    # notice
    @staticmethod
    def n(messages = None, color = COLOR_NOTICE, ignore_quiet_switch = False, add_to_history = True):
        Log._log(messages, color, ignore_quiet_switch, add_to_history)

    # verbose
    @staticmethod
    def v(messages = None, condition = True):
        if condition and Log.is_verbose():
            Log._log(messages)

    # very verbose
    @staticmethod
    def vv(messages = None, condition = True):
        if condition and Log.is_very_verbose():
            Log._log(messages)

    # warning
    @staticmethod
    def w(message = None, condition = True, prefix = 'W: '):
        if condition and message is not None:
            messages = Log._to_list(message)
            _ = [Log._log(prefix + Log.strip_ansi(msg), Log.COLOR_WARN, True) for msg in messages]

    # error
    @staticmethod
    def e(messages = None, condition = True, prefix = 'E: '):
        if condition and messages is not None:
            messages = Log._to_list(messages)
            _ = [Log._log(prefix + Log.strip_ansi(message), Log.COLOR_ERROR, True) for message in messages]

    # debug
    # NOTE: debug entries are not stored in action log
    @staticmethod
    def d(messages = None, condition = True):
        if condition and messages is not None and Log.is_debug():
            postfix = Log._get_stacktrace_string()
            for message in Log._to_list(messages):
                raw_msg = message + ' [DEBUG]'
                message = Log._format_log_line(raw_msg, Log.COLOR_DEBUG, postfix)
                postfix = ''
                print(message)

    @staticmethod
    def dd(messages = None, condition = True) -> None:
        if condition and Log.is_debug_verbose():
            Log.d(messages)

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_entries():
        return Log.log_entries

    @staticmethod
    def abort(messages = None):
        Log.e(messages)
        Log.level_init('*** Aborted', Log.COLOR_ERROR, True)

        if Log.is_debug():
            Log.d('Related stacktrace below')
            raise RuntimeError(
                '*** IT DID NOT CRASH *** Exception raised because of --debug used to obtain stacktrace. Enjoy.')
        else:
            sys.exit(1)

    @staticmethod
    def _get_stacktrace_string():
        msg = ''
        if Log.is_debug():
            frames = inspect.stack()
            for offset in range(3, len(frames)):
                frame = frames[offset][0]
                info = inspect.getframeinfo(frame)
                if os.path.basename(info.filename) != os.path.basename(__file__):
                    msg = ' %black_bright%({file}:{line})%reset%'.format(
                        file = os.path.basename(info.filename), line = info.lineno)
                    msg = Log.substitute_ansi(msg)
                    break

        return msg

    @staticmethod
    def strip_ansi(message):
        """Removes all ANSI control codes from given message string

        Args:
          message: string to be processed

        Returns:
          message string with ANSI codes striped or None
        """
        if message is not None:
            pattern = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return pattern.sub('', message)

        return ''

    @staticmethod
    def substitute_ansi(message):
        """Replaces color code placeholder with ANSI values.

        Args:
          message: message to process

        Returns:
          message with placeholders replaced with ANSI codes
        """

        if not issubclass(type(message), str):
            message = str(message)

        color_map = {
            'reset':         Log.ANSI_RESET,
            'reverse':       Log.ANSI_REVERSE,

            'black':         Log.ANSI_BLACK,
            'black_bright':  Log.ANSI_BLACK_BRIGHT,
            'red':           Log.ANSI_RED,
            'green':         Log.ANSI_GREEN,
            'green_bright':  Log.ANSI_GREEN_BRIGHT,
            'yellow':        Log.ANSI_YELLOW,
            'yellow_bright': Log.ANSI_YELLOW_BRIGHT,
            'blue':          Log.ANSI_BLUE,
            'magenta':       Log.ANSI_MAGENTA,
            'cyan':          Log.ANSI_CYAN,
            'white':         Log.ANSI_WHITE,

            'error':         Log.ANSI_RED,
            'warn':          Log.ANSI_YELLOW,
            'notice':        Log.ANSI_CYAN,
            'info':          None,
            'ok':            Log.ANSI_GREEN,
            'debug':         Log.ANSI_REVERSE,
            'banner':        (Log.ANSI_WHITE + Log.ANSI_REVERSE),
        }

        for (key, color) in color_map.items():
            message = re.sub(f'%{key}%', color if color is not None else '', message)

        return message

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _format_log_line(message = None, color = None, stacktrace_postfix = None):
        """Formats log message, adding required indentation and stuff.

        Args:
          message: message to format
          color: COLOR_xxx or ANSI_xxx color code to use if line should be colored
          stacktrace_postfix:

        Returns:
          Formatted log line
        """
        if message is not None:
            message = ' ' * (Log.log_level * 2) + Log.substitute_ansi(message)

            if Log.is_debug():
                message = f'{Log.log_level}: {message}'

            if color is not None:
                message = color + message

            message += Log.ANSI_RESET

            if stacktrace_postfix is not None:
                message += stacktrace_postfix

            if Log.no_color:
                message = Log.strip_ansi(message)

        return message

    @staticmethod
    def _log(messages = None, color = None, ignore_quiet_switch = False, add_to_history = True):
        if messages is not None:
            Log.last_log_entry_level = Log.log_level
            Log._flush_deferred_entry()

            postfix = Log._get_stacktrace_string()
            for message in Log._to_list(Log._dict_to_list(messages, '%green%')):
                use_message = False if Log.skip_empty_lines and message else True
                if use_message:
                    message = Log._format_log_line(message, color, postfix)
                    Log._log_raw(message, ignore_quiet_switch, add_to_history)
                    postfix = ''

    @staticmethod
    def _log_raw(message = None, ignore_quiet_switch = False, add_to_history = True):
        if message is not None:
            if Log.buffer_enabled and add_to_history:
                Log.log_entries.append(message)

            quiet = False if ignore_quiet_switch else Log.quiet
            if not quiet:
                print(message.rstrip())

    @staticmethod
    def _flush_deferred_entry() -> bool:
        """
        Removes any deferred log entry. Returns False if there was nothing
        defered to flush, True otherwise.

        :return:
        """
        result = False
        if Log.deferred_log_entry is not None:
            if Log.last_log_entry_level > Log.deferred_log_level:
                Log._log_raw(Log.deferred_log_entry)

            Log.deferred_log_entry = None
            Log.deferred_log_level = None
            result = True

        Log.last_log_entry_level = 0
        return result

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _to_list(data):
        """Converts certain data types (str, unicode) into list.

        Args:
          data: data to convert

        Returns:
          list with converted data
        """
        if isinstance(data, str):
            return [data]
        elif isinstance(data, PosixPath):
            return [str(data)]

        return data

    @staticmethod
    def _dict_to_list(data_to_convert, color = None):
        """Converts dictionary elements into list.

        Args:
          data_to_convert: dictionary to convert
          color: color code (i.e. '%red%' for each row)

        Returns:
          list with converted data.

        """
        if not isinstance(data_to_convert, dict):
            return data_to_convert

        array = []
        for (key, val) in data_to_convert.items():
            if color is not None:
                array.append(f'{color}{key}%reset% : {val}')
            else:
                array.append(f'{key}: {val}')
        return array
