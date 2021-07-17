#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

# #################################################################################################


class PropEntry():
    pass


# #################################################################################################

class PropTranslation(PropEntry):
    """
    Class representing valid translation entry.
    """

    def __init__(self, key: str, value: str = None, separator: str = ':') -> None:
        key = key.strip()
        assert len(key) > 0

        self.key = key
        self.value = value.strip()
        self.separator = separator

    def toString(self) -> str:
        return f'{self.key} {self.separator} {self.value}'


# #################################################################################################

class PropComment(PropEntry):
    """
    Class representing line comment.
    """

    def __init__(self, value: str) -> None:
        value = value.strip()
        assert len(value) > 0
        assert value[0] in ['!', '#']
        self.value = value

    def toString(self) -> str:
        return self.value


# #################################################################################################

class PropEmpty(PropEntry):
    """
    Class representing empty line.
    """

    def __init__(self) -> None:
        pass

    def toString(self) -> str:
        return ''
