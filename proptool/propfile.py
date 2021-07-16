#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool
#

import re
from pathlib import Path
from typing import List, Union

from .app import App
from .entries import *
from .util import Util


# #################################################################################################

class PropFile(list):
    def __init__(self, app: App, file: Path):
        super().__init__()

        self.file = file
        # All the keys of 'regular' translations
        self.keys = []
        # All the keys in form `# ==> KEY =` that we found.
        self.commentedOutKeys = []
        self.app = app
        self.separator = app.separator

        self._load(file)

    def validateAndFix(self, reference: 'PropFile') -> bool:
        if not self.validate(reference) and self.app.fix:
            self.fix(reference)

    def validate(self, reference: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference:
        :return:
        """
        errorCount = 0

        # Check if we have all reference keys present.
        myKeys = self.keys.copy()
        missingKeys = []
        for key in reference.keys:
            if key in myKeys:
                myKeys.remove(key)
            else:
                missingKeys.append(key)

        # Commented out keys (in form `# ==> KEY =`) are also considered
        # present in the translation unless we run in strict check mode.

        if not self.app.strict:
            commentedOutKeys = self.commentedOutKeys.copy()
            for key in commentedOutKeys:
                if key in missingKeys:
                    missingKeys.remove(key)

        missingKeysCount = len(missingKeys)
        errorCount += missingKeysCount

        # Check for dangling keys
        danglingKeysCount = len(myKeys)
        errorCount += danglingKeysCount

        if errorCount > 0:
            Util.error(f'  Found {errorCount} errors in {self.file}')
            if missingKeysCount > 0:
                Util.error([f'    Missing keys: {missingKeysCount}'])
                if self.app.verbose:
                    Util.error([f'      {key}' for key in missingKeys])
            if danglingKeysCount > 0:
                Util.error([f'    Dangling keys: {danglingKeysCount}'])
                if self.app.verbose:
                    Util.error([f'      {key}' for key in myKeys])
        elif self.app.verbose:
            print(f'  {self.file}: OK')

        return errorCount == 0

    def fix(self, reference: 'PropFile'):
        synced: List[PropEntry] = []

        for item in reference:
            if isinstance(item, PropTranslation):
                if item.key in self.keys:
                    translated = self._findTranslationByKey(item.key)
                    if not translated:
                        raise RuntimeError(f'Unable to find translation of {item.key}')
                    synced.append(self._findTranslationByKey(item.key).toString() + '\n')
                else:
                    synced.append(f'# ==> {item.key} {self.separator}' + '\n')
            elif isinstance(item, (PropEmpty, PropComment)):
                synced.append(item.toString() + '\n')
            else:
                raise RuntimeError(f'Unknown entry type: {type(item)}')

        print(f'    Writing updated file.')
        # with open(self.file, 'w') as fh:
        #     fh.writelines(synced)
        print(''.join(synced))

    def _findTranslationByKey(self, key: str) -> Union[PropTranslation, None]:
        for item in self:
            if isinstance(item, PropTranslation) and item.key == key:
                return item
        return None

    def _load(self, file: Path) -> None:
        """
        Loads and parses *.properties file.

        :param file:
        :return:
        """

        def addTranslation(key: str, val: str):
            key = key.strip()
            val = val.strip()
            if key in self.keys:
                Util.abort(f'Key {key} already defined at line {self.keys.index(key)}.')
            self.keys.append(key)
            self.append(PropTranslation(key, val, self.separator))

        def addComment(val: str):
            self.append(PropComment(val))

        def addEmpty():
            self.append(PropEmpty())

        if not file.exists():
            Util.abort(f'File not found: {file}')

        previousLine: str = None
        with open(file, 'r') as fh:
            lineNumber = 0
            while True:
                lineNumber += 1
                line = fh.readline()
                if not line:
                    break

                # Remove all trailing/leading spaces.
                line: str = line.strip()
                print(f'-- "{line}"')
                # Skip empty lines
                if line == '':
                    # Only single subsequent empty line allowed.
                    if previousLine is not None and previousLine == '':
                        continue
                    addEmpty()

                elif line[0] == '#':
                    # Only single subsequent 'empty' comment line allowed.
                    if line == '#' and previousLine is not None and previousLine == '#':
                        continue

                    # min len of valid commented out key is 9 -> `# ==> K ='
                    if len(line) > 9:
                        # Let's look for commented out keys: '# ==> KEY ='
                        match = re.compile('^[#!] ==> ([a-zA-Z0-9_.-]+) [=:]$').match(line)
                        if match:
                            self.commentedOutKeys.append(match.group(1))
                    addComment(line)

                else:
                    if not self.separator:
                        # Let's look for separator char. Both `=` and `:` are valid.
                        for i in range(len(line)):
                            if line[i] in self.app.allowedSeparators:
                                self.separator = line[i]
                                break

                    tmp: List[str] = line.split(self.separator)
                    if len(tmp) < 2:
                        Util.abort([f'Invalid syntax. Line {lineNumber}, file: {file}',
                                    f'Using "{self.separator}" as separator.'])

                    addTranslation(tmp[0], ''.join(tmp[1:]))

                previousLine = line
