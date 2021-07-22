"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import Union

from proptool.decorators.overrides import overrides


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


# #################################################################################################

class Comment(PropItem):
    """
    Class representing a line comment.
    """

    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError('Value must be a string.')
        if not value:
            raise ValueError('Value cannot be empty.')
        marker = value[0]
        if marker not in {'!', '#'}:
            raise ValueError(f'Invalid comment marker: "{marker}".')
        super().__init__(value)

    @overrides(PropItem)
    def to_string(self) -> str:
        return self.value


# #################################################################################################

class Blank(PropItem):
    """
    Class representing empty line.
    """

    @overrides(PropItem)
    def to_string(self) -> str:
        return ''
