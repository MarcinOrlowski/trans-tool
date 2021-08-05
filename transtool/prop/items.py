"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import Tuple, Union

from transtool.config.config import Config
from transtool.decorators.overrides import overrides


# #################################################################################################

class PropItem(object):
    def __init__(self, value: Union[str, None] = None, key: Union[str, None] = None):
        self.value = value
        self.key = key

    def to_string(self) -> str:
        raise NotImplementedError


# #################################################################################################

class Translation(PropItem):
    """
    Class representing a translation entry.
    """

    def __init__(self, key: str, value: Union[str, None] = None, separator: str = '=') -> None:
        if not key:
            raise ValueError('No empty key allowed.')
        if not isinstance(key, str):
            raise ValueError('Key must be a string.')
        key = key.strip()
        if not key:
            raise ValueError('Key must be non-empty string.')

        # TODO: validate key against KeyFormat's pattern

        if value is not None and not isinstance(value, str):
            raise ValueError('Value must be a string or None.')

        # TODO: default separators should be moved to consts
        if separator not in {':', '='}:
            raise ValueError(f'Invalid separator character: "{separator}".')
        super().__init__(value, key)
        self.separator = separator

    @overrides(PropItem)
    def to_string(self) -> str:
        return f'{self.key} {self.separator} {self.value}'

    @staticmethod
    def parse_translation_line(line: str) -> Union[Tuple[str, str, str], None]:
        # Min two chars (one letter key and separator)
        if len(line) < 2:
            return None

        # Find used separator first
        separator = None
        separator_pos = None
        previous_char_backspace = False
        for idx, char in enumerate(line):
            if char == '\\':
                if not previous_char_backspace:
                    previous_char_backspace = True
                continue
            if char in Config.ALLOWED_SEPARATORS:
                if previous_char_backspace:
                    continue

                separator = char
                separator_pos = idx
                break
            else:
                previous_char_backspace = False

        # https://docs.oracle.com/javase/7/docs/api/java/util/Properties.html

        if not separator:
            return None

        key = line[:separator_pos].strip()
        sep = separator.strip()
        val = line[separator_pos + 1:].lstrip()

        if key == '' or sep == '':
            return None

        return key, sep, val


# #################################################################################################

class Comment(PropItem):
    """
    Class representing a comment line.
    """

    def __init__(self, value: str = '', marker: str = None) -> None:
        if not marker:
            marker = Config.ALLOWED_COMMENT_MARKERS[0]
        if marker not in Config.ALLOWED_COMMENT_MARKERS:
            raise ValueError(f'Invalid comment marker: "{marker}".')
        if not isinstance(value, str):
            raise ValueError('Value must be a string.')
        if not value:
            value = f'{marker}'

        value_marker = value[0]
        if value_marker not in Config.ALLOWED_COMMENT_MARKERS:
            value = f'{marker} {value}'

        super().__init__(value)

    @overrides(PropItem)
    def to_string(self) -> str:
        return self.value

    @staticmethod
    def comment_out_key(config: Config, key: str, value: Union[str, None]) -> str:
        """
        Helper method that returns translation key formatted as commented-out item.
        :param config: Application config.
        :param key: translation key.
        :param value: Optional original string value
        """

        if value is None:
            value = ''

        return config.COMMENTED_TRANS_TPL.replace(
            'KEY', key).replace(
            'COM', config.ALLOWED_COMMENT_MARKERS[0]).replace(
            'SEP', config.ALLOWED_SEPARATORS[0]).replace(
            'VAL', value).strip()

    @staticmethod
    def get_commented_out_key_comment(config: Config, key: str, value: Union[str, None] = None) -> 'Comment':
        """
        Returns instance of Comment with content being commented-out key
        formatted according to current configuration
        :param config: config to be
        :param key: key to comment-out
        :param value: optional value (or None)
        :return:
        """
        return Comment(Comment.comment_out_key(config, key, value))


# #################################################################################################

class Blank(PropItem):
    """
    Class representing empty line.
    """

    @overrides(PropItem)
    def to_string(self) -> str:
        return ''
