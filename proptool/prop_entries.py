"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from .overrides import overrides


# #################################################################################################

class PropEntry(object):
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

        self.key = key
        self.value = value
        self.separator = separator

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
        self.value = value

    @overrides(PropEntry)
    def to_string(self) -> str:
        return self.value


# #################################################################################################

class PropEmpty(PropEntry):
    """
    Class representing empty line.
    """

    def __init__(self) -> None:
        pass

    @overrides(PropEntry)
    def to_string(self) -> str:
        return ''
