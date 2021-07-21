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

class PropEntry(object):
    def __init__(self, value: Union[str, None] = None, key: Union[str, None] = None):
        self.value = value
        self.key = key

    def to_string(self) -> str:
        raise NotImplementedError


# #################################################################################################

class PropTranslation(PropEntry):
    """
    Class representing valid translation entry.
    """

    def __init__(self, key: str, value: str = None, separator: str = '=') -> None:
        key = key.strip()
        if not key:
            raise ValueError('No empty key allowed.')
        if separator not in {':', '='}:
            raise ValueError(f'Invalid separator character: "{separator}".')
        super().__init__(value, key)

    @overrides(PropEntry)
    def to_string(self) -> str:
        return f'{self.key} {self.separator} {self.value}'


# #################################################################################################

class PropComment(PropEntry):
    """
    Class representing line comment.
    """

    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError('Value cannot be empty.')
        marker = value[0]
        if marker not in {'!', '#'}:
            raise ValueError(f'Invalid comment marker: "{marker}".')
        super().__init__(value)

    @overrides(PropEntry)
    def to_string(self) -> str:
        return self.value


# #################################################################################################

class PropBlank(PropEntry):
    """
    Class representing empty line.
    """

    def __init__(self) -> None:
        super().__init__()

    @overrides(PropEntry)
    def to_string(self) -> str:
        return ''
