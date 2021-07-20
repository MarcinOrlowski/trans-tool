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
from typing import List, Union

from .config import Config


class Ansi:
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    RESET = u'\u001b[0m'
    BOLD = u'\u001b[1m'
    DIM = u'\u001b[2m'
    UNDERLINE = u'\u001b[4m'
    REVERSE = u'\u001b[7m'

    BLACK = u'\u001b[30m'
    BLACK_BRIGHT = u'\u001b[30;1m'
    RED = u'\u001b[31m'
    GREEN = u'\u001b[32m'
    YELLOW = u'\u001b[33m'
    BLUE = u'\u001b[34m'
    MAGENTA = u'\u001b[35m'
    CYAN = u'\u001b[36m'
    WHITE = u'\u001b[37m'

    BG_BLACK = u'\u001b[40m'
    BG_RED = u'\u001b[41m'
    BG_GREEN = u'\u001b[42m'
    BG_YELLOW = u'\u001b[43m'
    BG_BLUE = u'\u001b[44m'
    BG_MAGENTA = u'\u001b[45m'
    BG_CYAN = u'\u001b[46m'
    BG_WHITE = u'\u001b[47m'

    @staticmethod
    def strip(message: Union[str, None]) -> str:
        """Removes all ANSI control codes from given message string

        Args:
          message: string to be processed

        Returns:
          message string with ANSI codes striped or None
        """
        if message is not None:
            import re
            pattern = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return pattern.sub('', message)

        return ''


class Log(object):
    COLOR_ERROR = Ansi.RED
    COLOR_WARN = Ansi.YELLOW
    COLOR_NOTICE = Ansi.CYAN
    COLOR_INFO = None
    COLOR_OK = Ansi.GREEN
    COLOR_DEBUG = Ansi.REVERSE
    COLOR_BANNER = (Ansi.WHITE + Ansi.REVERSE)

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
    def configure(cls, config: Config) -> None:
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
    def disable_buffer(cls) -> None:
        cls.buffer_enabled = False

    @classmethod
    def enable_buffer(cls) -> None:
        cls.buffer_enabled = True

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def init(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False) -> None:
        Log.log_level = 0
        Log.push(message, color, ignore_quiet_switch)

    @staticmethod
    def push(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False,
             deferred = False) -> None:
        if Log.verbose_level == Log.VERBOSE_NONE and deferred:
            Log._flush_deferred_entry()

            Log.deferred_log_level = Log.log_level
            Log.deferred_log_entry = Log._format_log_line(message, color)
        else:
            Log._log(message, color, ignore_quiet_switch)

        Log.log_level += 1

    @staticmethod
    def push_e(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False,
               deferred = False) -> None:
        Log.push(f'%bg_error%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def push_w(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False,
               deferred = False) -> None:
        Log.push(f'%bg_warn%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def push_ok(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False,
                deferred = False) -> None:
        Log.push(f'%bg_ok%{message}', color, ignore_quiet_switch, deferred)

    @staticmethod
    def push_v(message: Union[str, None] = None, color: Union[str, None] = None, ignore_quiet_switch = False,
               deferred = False) -> None:
        if Log.is_verbose():
            Log.push(message, color, ignore_quiet_switch, deferred)

    @staticmethod
    def pop(messages = None, color: Union[str, None] = None, ignore_quiet_switch = False) -> bool:
        if messages is not None:
            Log.i(messages = messages, color = color, ignore_quiet_switch = ignore_quiet_switch)

        had_anything_deferred = Log._flush_deferred_entry()

        if Log.log_level == 0:
            Log.abort('pop() called too many times.')
        Log.log_level -= 1

        return had_anything_deferred

    @staticmethod
    def pop_v(messages = None, color: Union[str, None] = None, ignore_quiet_switch: bool = False) -> None:
        if Log.is_verbose():
            Log.pop(messages, color, ignore_quiet_switch)

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
    def banner(messages, ignore_quiet_switch: bool = False, add_to_history: bool = True, top: bool = True,
               bottom: bool = True) -> None:
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
    def banner_v(messages, ignore_quiet_switch: bool = False, add_to_history: bool = True, top: bool = True,
                 bottom: bool = True) -> None:
        if Log.verbose_level >= Log.VERBOSE_NORMAL:
            Log.banner(messages, ignore_quiet_switch, add_to_history, top, bottom)

    @staticmethod
    def i(messages = None, color: str = COLOR_INFO, ignore_quiet_switch: bool = False, add_to_history: bool = True) -> None:
        Log._log(messages, color, ignore_quiet_switch, add_to_history)

    # notice
    @staticmethod
    def n(messages = None, color: str = COLOR_NOTICE, ignore_quiet_switch: bool = False, add_to_history: bool = True) -> None:
        Log._log(messages, color, ignore_quiet_switch, add_to_history)

    # verbose
    @staticmethod
    def v(messages = None, condition: bool = True) -> None:
        if condition and Log.is_verbose():
            Log._log(messages)

    # very verbose
    @staticmethod
    def vv(messages = None, condition: bool = True) -> None:
        if condition and Log.is_very_verbose():
            Log._log(messages)

    # warning
    @staticmethod
    def w(message = None, condition: bool = True, prefix: str = 'W: ') -> None:
        if condition and message is not None:
            messages = Log._to_list(message)
            _ = [Log._log(prefix + Ansi.strip(msg), Log.COLOR_WARN, True) for msg in messages]

    # error
    @staticmethod
    def e(messages = None, condition: bool = True, prefix: str = 'E: ') -> None:
        if condition and messages is not None:
            messages = Log._to_list(messages)
            _ = [Log._log(prefix + Ansi.strip(message), Log.COLOR_ERROR, True) for message in messages]

    # debug
    # NOTE: debug entries are not stored in action log
    @staticmethod
    def d(messages = None, condition: bool = True) -> None:
        if condition and messages is not None and Log.is_debug():
            postfix = Log._get_stacktrace_string()
            for message in Log._to_list(messages):
                raw_msg = f'[D] {message}'
                message = Log._format_log_line(raw_msg, Log.COLOR_DEBUG, postfix)
                postfix = ''
                print(message)

    @staticmethod
    def dd(messages = None, condition: bool = True) -> None:
        if condition and Log.is_debug_verbose():
            Log.d(messages)

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_entries() -> List[str]:
        return Log.log_entries

    @staticmethod
    def abort(messages = None) -> None:
        Log.e(messages)
        Log.init('*** Aborted', Log.COLOR_ERROR, True)

        if Log.is_debug():
            Log.d('Related stacktrace below')
            raise RuntimeError(
                '*** IT DID NOT CRASH *** Exception raised because of --debug used to obtain stacktrace. Enjoy.')
        else:
            sys.exit(1)

    @staticmethod
    def _get_stacktrace_string() -> str:
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
    def substitute_ansi(message) -> str:
        """Replaces color code placeholder with ANSI values.

        Args:
          message: message to process

        Returns:
          message with placeholders replaced with ANSI codes
        """

        if not issubclass(type(message), str):
            message = str(message)

        color_map = {
            'reset':        Ansi.RESET,
            'reverse':      Ansi.REVERSE,
            'bold':         Ansi.BOLD,
            'dim':          Ansi.DIM,

            'black':        Ansi.BLACK,
            'black_bright': Ansi.BLACK_BRIGHT,
            'red':          Ansi.RED,
            'green':        Ansi.GREEN,
            'yellow':       Ansi.YELLOW,
            'blue':         Ansi.BLUE,
            'magenta':      Ansi.MAGENTA,
            'cyan':         Ansi.CYAN,
            'white':        Ansi.WHITE,

            'bg_black':     Ansi.BG_BLACK,
            'bg_red':       Ansi.BG_RED,
            'bg_green':     Ansi.BG_GREEN,
            'bg_yellow':    Ansi.BG_YELLOW,
            'bg_blue':      Ansi.BG_BLUE,
            'bg_magenta':   Ansi.BG_MAGENTA,
            'bg_cyan':      Ansi.BG_CYAN,
            'bg_white':     Ansi.BG_WHITE,

            'error':        Ansi.RED,
            'bg_error':     (Ansi.BG_RED + Ansi.WHITE),
            'warn':         Ansi.YELLOW,
            'bg_warn':      (Ansi.BG_YELLOW + Ansi.BLACK + Ansi.DIM),
            'notice':       Ansi.CYAN,
            'info':         None,
            'ok':           Ansi.GREEN,
            'bg_ok':        (Ansi.BG_GREEN + Ansi.WHITE),
            'debug':        Ansi.REVERSE,
            'banner':       (Ansi.WHITE + Ansi.REVERSE),
        }

        for (key, color) in color_map.items():
            message = re.sub(f'%{key}%', color if color is not None else '', message)

        return message

    # ---------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _format_log_line(message = None, color: Union[str, None] = None, stacktrace_postfix: Union[str, None] = None):
        """Formats log message, adding required indentation and stuff.

        Args:
          message: message to format
          color: COLOR_xxx or Ansi.xxx color code to use if line should be colored
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

            message += Ansi.RESET

            if stacktrace_postfix is not None:
                message += stacktrace_postfix

            if Log.no_color:
                message = Ansi.strip(message)

        return message

    @staticmethod
    def _log(messages = None, color: Union[str, None] = None, ignore_quiet_switch: bool = False,
             add_to_history: bool = True) -> None:
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
    def _log_raw(message = None, ignore_quiet_switch: bool = False, add_to_history: bool = True) -> None:
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
        deferred to flush, True otherwise.

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
    def _to_list(data) -> List[str]:
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
    def _dict_to_list(data_to_convert, color: Union[str, None] = None) -> List[str]:
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
