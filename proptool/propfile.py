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
from .check.punctuation import Punctuation
from .check.trailing_whitechars import TrailingWhiteChars
from .entries import PropComment, PropTranslation, PropEmpty, PropEntry
from .util import Util
from .report.report import Report


# #################################################################################################

class PropFile(list):
    def __init__(self, app: App, file: Path, language: str = None):
        super().__init__()

        self.file: Path = file
        # All the keys of 'regular' translations
        self.keys: List[str] = []
        # All the keys in form `# ==> KEY =` that we found.
        self.commented_out_keys: List[str] = []
        self.app: App = app
        self.separator: str = app.separator
        self.loaded: bool = False
        self.language = language

        self.duplicated_keys_report = Report()

        if file is not None:
            self.loaded = self._load(file)

    # #################################################################################################

    def find_by_key(self, key: str) -> Union[PropTranslation, None]:
        """
        Returns translation entry referenced by given key or None.

        :param key: Translation key to look for.
        :return: Instance of PropTranslation or None.
        """
        for item in list(filter(lambda entry: isinstance(entry, PropTranslation), self)):
            if item.key == key:
                return item
        return None

    # #################################################################################################

    def validate_and_fix(self, reference: 'PropFile') -> None:
        if not self.validate(reference) and self.app.fix:
            self.fix(reference)

    # #################################################################################################

    def validate(self, reference: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference:
        :return:
        """

        if not self.loaded:
            Util.error(f'  File does not exist: {self.file}')
            return False

        error_count = 0

        my_keys = self.keys.copy()
        missing_keys: List[str] = []

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

        # Check for trailing white chars
        trailing_chars_report = TrailingWhiteChars.check(self.app, self)

        # Check for punctuation marks
        punctuation_mismatch_report = Punctuation.check(self.app, reference, self)

        # Check for space before \n
        # for item in self:

        missing_keys_count = len(missing_keys)
        error_count += missing_keys_count
        dangling_keys_count = len(my_keys)
        error_count += dangling_keys_count

        trailing_chars_count = len(trailing_chars_report)
        error_count += trailing_chars_count

        punctuation_mismatch_count = len(punctuation_mismatch_report)
        error_count += punctuation_mismatch_count

        if error_count > 0:
            Util.error(f'  Found {error_count} errors in "{self.file}":')
            if missing_keys_count > 0:
                Util.error(f'    Missing keys: {missing_keys_count}')
                if self.app.verbose:
                    Util.error([f'      {key}' for key in missing_keys])
            if dangling_keys_count > 0:
                Util.error(f'    Dangling keys: {dangling_keys_count}')
                if self.app.verbose:
                    Util.error([f'      {key}' for key in my_keys])
            if trailing_chars_count > 0:
                Util.error(f'    Trailing white characters: {trailing_chars_count}')
                if self.app.verbose:
                    Util.error([f'      {item.to_string()}' for item in trailing_chars_report])
            if punctuation_mismatch_count > 0:
                Util.error(f'    Punctuation mismatch: {punctuation_mismatch_count}')
                if self.app.verbose:
                    Util.error([f'      {item.to_string()}' for item in punctuation_mismatch_report])

        elif self.app.verbose:
            print(f'  {self.file}: OK')

        return error_count == 0

    # #################################################################################################

    def fix(self, reference: 'PropFile') -> None:
        synced: List[PropEntry] = []

        comment_pattern = self.app.comment_template.replace('COM', self.app.comment_marker).replace('SEP', self.separator)
        for item in reference:
            if isinstance(item, PropTranslation):
                if item.key in self.keys:
                    translated = self.find_by_key(item.key)
                    if not translated:
                        raise RuntimeError(f'Unable to find translation of {item.key}')
                    synced.append(self.find_by_key(item.key).to_string() + '\n')
                else:
                    synced.append(comment_pattern.replace('KEY', item.key) + '\n')
            elif isinstance(item, (PropEmpty, PropComment)):
                synced.append(item.to_string() + '\n')
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

        if not file.exists():
            return False

        comment_pattern = re.escape(self.app.comment_template).replace(
            'COM', f'[{"".join(self.app.allowed_comment_markers)}]').replace(
            'SEP', f'[{"".join(self.app.allowed_separators)}]')
        # NOTE: key pattern must be in () brackets to form a group used later!
        comment_pattern = comment_pattern.replace('KEY', '([a-zAz][a-zA-z0-9_.-]+)')
        comment_pattern = f'^{comment_pattern}'

        with open(file, 'r') as fh:
            line_number: int = 0
            while True:
                line_number += 1
                line: str = fh.readline()
                if not line:
                    break

                # remove CRLF
                if line[-1] == '\n':  # LF
                    line = line[:-1]
                if line[-1] == '\r':  # CR
                    line = line[:-1]

                # Skip empty lines
                if line.strip() == '':
                    self.append(PropEmpty())

                elif line[0] in self.app.allowed_comment_markers:
                    # Let's look for commented out keys.
                    match = re.compile(comment_pattern).match(line)
                    if match:
                        self.commented_out_keys.append(match.group(1))
                    self.append(PropComment(line))

                # elif line[0] in self.app.allowed_comment_markers:
                #     # Only single subsequent 'empty' comment line allowed.
                #     if line == self.app.comment_marker and previous_line is not None and previous_line == self.app.comment_marker:
                #         continue
                #
                #     # Let's look for commented out keys.
                #     match = re.compile(comment_pattern).match(line)
                #     if match:
                #         self.commented_out_keys.append(match.group(1))
                #     addComment(line)

                else:
                    if not self.separator:
                        # Let's look for used separator character
                        for i in range(len(line)):
                            if line[i] in self.app.allowed_separators:
                                self.separator = line[i]
                                break

                    tmp: List[str] = line.split(self.separator)
                    if len(tmp) < 2:
                        Util.abort([f'Invalid syntax. Line {line_number}, file: {file}',
                                    f'Using "{self.separator}" as separator.'])

                    key = tmp[0].strip()
                    val = ''.join(tmp[1:]).lstrip()
                    if key not in self.keys:
                        self.keys.append(key)
                        self.append(PropTranslation(key, val, self.separator))
                    else:
                        self.duplicated_keys_report.error(line_number, f'Duplicated key "{key}".')

        return True
