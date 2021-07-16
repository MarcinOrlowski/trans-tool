#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool
#

# #################################################################################################


class PropEntry():
    pass


class PropTranslation(PropEntry):
    def __init__(self, key: str, value: str = None, separator: str = ':'):
        key = key.strip()
        assert len(key) > 0

        self.key = key
        self.value = value.strip()
        self.separator = separator

    def toString(self) -> str:
        return f'{self.key} {self.separator} {self.value}'


class PropComment(PropEntry):
    def __init__(self, value: str):
        value = value.strip()
        assert len(value) > 0
        assert value[0] == '#'
        self.value = value

    def toString(self) -> str:
        return self.value


class PropEmpty(PropEntry):
    def __init__(self):
        pass

    def toString(self):
        return ''
