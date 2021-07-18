#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
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

        self.file: Path = file
        # All the keys of 'regular' translations
        self.keys: List[str] = []
        # All the keys in form `# ==> KEY =` that we found.
        self.commented_out_keys: List[str] = []
        self.app: App = app
        self.separator: str = app.separator
        self.loaded: bool = False

        if file is not None:
            self.loaded = self._load(file)

    # #################################################################################################

    def validateAndFix(self, reference: 'PropFile') -> bool:
        if not self.validate(reference) and self.app.fix:
            self.fix(reference)

    # #################################################################################################

    def validate(self, reference: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference:
        :return:
        """
        error_count = 0

        my_keys = self.keys.copy()
        missing_keys = []

        if not self.loaded:
            error_count += 1
        else:
            # Check if we have all reference keys present.
            for key in reference.keys:
                if key in my_keys:
                    my_keys.remove(key)
                else:
                    missing_keys.append(key)

            # Commented out keys are also considered present in the translation unless
            # we run in strict check mode.
            if not self.app.strict:
                commented_out_keys = self.commented_out_keys.copy()
                for key in commented_out_keys:
                    if key in missing_keys:
                        missing_keys.remove(key)

        missing_keys_count = len(missing_keys)
        error_count += missing_keys_count

        # Check for dangling keys
        dangling_keys_count = len(my_keys)
        error_count += dangling_keys_count

        if error_count > 0:
            if not self.loaded:
                Util.error(f'  File does not exist: {self.file}')
            else:
                Util.error(f'  Found {error_count} errors in {self.file}')
                if missing_keys_count > 0:
                    Util.error(f'    Missing keys: {missing_keys_count}')
                    if self.app.verbose:
                        Util.error([f'      {key}' for key in missing_keys])
                if dangling_keys_count > 0:
                    Util.error(f'    Dangling keys: {dangling_keys_count}')
                    if self.app.verbose:
                        Util.error([f'      {key}' for key in my_keys])
        elif self.app.verbose:
            print(f'  {self.file}: OK')

        return error_count == 0

    # #################################################################################################

    def fix(self, reference: 'PropFile') -> None:

        def findTranslationByKey(key: str) -> Union[PropTranslation, None]:
            for item in self:
                if isinstance(item, PropTranslation) and item.key == key:
                    return item
            return None

        synced: List[PropEntry] = []

        comment_pattern = self.app.comment_template.replace('COM', self.app.comment_marker).replace('SEP', self.separator)
        for item in reference:
            if isinstance(item, PropTranslation):
                if item.key in self.keys:
                    translated = findTranslationByKey(item.key)
                    if not translated:
                        raise RuntimeError(f'Unable to find translation of {item.key}')
                    synced.append(findTranslationByKey(item.key).toString() + '\n')
                else:
                    synced.append(comment_pattern.replace('KEY', item.key) + '\n')
            elif isinstance(item, (PropEmpty, PropComment)):
                synced.append(item.toString() + '\n')
            else:
                raise RuntimeError(f'Unknown entry type: {type(item)}')

        print(f'    Re-writing translation file: {self.file}')
        with open(self.file, 'w') as fh:
            fh.writelines(synced)

    # #################################################################################################

    def _load(self, file: Path) -> bool:
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
            return False

        comment_pattern = re.escape(self.app.comment_template).replace(
            'COM', f'[{"".join(self.app.allowed_comment_markers)}]').replace(
            'SEP', f'[{"".join(self.app.allowed_separators)}]')
        # NOTE: key pattern must be in () brackets to form a group used later!
        comment_pattern = comment_pattern.replace('KEY', '([a-zAz][a-zA-z0-9_.-]+)')
        comment_pattern = f'^{comment_pattern}'

        previous_line: str = None
        with open(file, 'r') as fh:
            line_number: int = 0
            while True:
                line_number += 1
                line: str = fh.readline()
                if not line:
                    break

                # Remove all trailing/leading spaces.
                line: str = line.strip()
                # Skip empty lines
                if line == '':
                    # Only single subsequent empty line allowed.
                    if previous_line is not None and previous_line == '':
                        continue
                    addEmpty()

                elif line[0] in self.app.allowed_comment_markers:
                    # Only single subsequent 'empty' comment line allowed.
                    if line == self.app.comment_marker and previous_line is not None and previous_line == self.app.comment_marker:
                        continue

                    # Let's look for commented out keys.
                    match = re.compile(comment_pattern).match(line)
                    if match:
                        self.commented_out_keys.append(match.group(1))
                    addComment(line)

                else:
                    if not self.separator:
                        # Let's look for used separator character.
                        for i in range(len(line)):
                            if line[i] in self.app.allowed_separators:
                                self.separator = line[i]
                                break

                    tmp: List[str] = line.split(self.separator)
                    if len(tmp) < 2:
                        Util.abort([f'Invalid syntax. Line {line_number}, file: {file}',
                                    f'Using "{self.separator}" as separator.'])

                    addTranslation(tmp[0], ''.join(tmp[1:]))

                previous_line = line

        return True
