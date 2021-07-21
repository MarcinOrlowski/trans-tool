"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
import copy
import re
from pathlib import Path
from typing import List, Union

from .checks.brackets import Brackets
from .checks.dangling_keys import DanglingKeys
from .checks.empty_translations import EmptyTranslations
from .checks.formatting_values import FormattingValues
from .checks.key_format import KeyFormat
from .checks.missing_translation import MissingTranslation
from .checks.punctuation import Punctuation
from .checks.quotation_marks import QuotationMarks
from .checks.starts_with_the_same_case import StartsWithTheSameCase
from .checks.trailing_white_chars import TrailingWhiteChars
from .checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from .config import Config
from .entries import PropComment, PropEmpty, PropEntry, PropTranslation
from .log import Log
from .report.report import Report
from .report.report_group import ReportGroup
from .utils import Utils


# #################################################################################################

class PropFile(object):
    def __init__(self, config: Config, file: Union[Path, None] = None, language: List[str] = None):
        super().__init__()

        self.config: Config = config

        self.file: Path = file
        # All the keys of 'regular' translations
        self.keys: List[str] = []
        # All the keys in form `# ==> KEY =` that we found.
        self.commented_out_keys: List[str] = []
        self.separator: str = config.separator
        self.loaded: bool = False
        self.items: List[PropEntry] = []

        self.report = Report(config)

        comment_pattern = re.escape(self.config.comment_template).replace(
            'COM', f'[{"".join(Config.ALLOWED_COMMENT_MARKERS)}]').replace(
            'SEP', f'[{"".join(Config.ALLOWED_SEPARATORS)}]')
        # NOTE: key pattern must be in () brackets to form a group used later!
        comment_pattern = comment_pattern.replace('KEY', '([a-zAz][a-zA-z0-9_.-]+)')
        self.comment_pattern = f'^{comment_pattern}'

        if file is not None:
            self.loaded = self._load(file)

    # #################################################################################################

    def find_by_key(self, key: str) -> Union[PropTranslation, None]:
        """
        Returns translation entry referenced by given key or None.

        :param key: Translation key to look for.
        :return: Instance of PropTranslation or None.
        """
        translations = list(filter(lambda entry: isinstance(entry, PropTranslation), self.items))
        for item in translations:
            if item.key == key:
                return item
        return None

    # #################################################################################################

    def append(self, item: PropEntry):
        if isinstance(item, PropTranslation):
            self.keys.append(item.key)
            self.items.append(item)
        elif isinstance(item, PropComment):
            # Let's look for commented out keys.
            match = re.compile(self.comment_pattern).match(item.value)
            if match:
                self.commented_out_keys.append(match.group(1))
            self.items.append(item)

    # #################################################################################################

    def validate_and_fix(self, reference: 'PropFile') -> None:
        if not self.validate(reference) and self.config.fix:
            self.fix(reference)

    # #################################################################################################

    def validate(self, reference_file: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference_file:
        :return:
        """
        if not self.loaded:
            Log.e(f'  File does not exist: {self.file}')
            return False

        checks = [
            MissingTranslation,
            DanglingKeys,
            TrailingWhiteChars,
            Punctuation,
            StartsWithTheSameCase,
            EmptyTranslations,
            WhiteCharsBeforeLinefeed,
            KeyFormat,
            Brackets,
            QuotationMarks,
            FormattingValues,
        ]
        for validator in checks:
            # Each validator gets copy of the files, to prevent any potential destructive operation.
            self.report.add((validator(self.config)).check(copy.copy(reference_file), copy.copy(self)))

        return self.report.empty()

    # #################################################################################################

    def fix(self, reference: 'PropFile') -> None:
        synced: List[str] = []

        comment_pattern = self.config.comment_template.replace('COM', self.config.comment_marker).replace('SEP', self.separator)
        for item in reference.items:
            if isinstance(item, PropTranslation):
                if item.key in self.keys:
                    synced.append(self.find_by_key(item.key).to_string() + '\n')
                else:
                    synced.append(comment_pattern.replace('KEY', item.key) + '\n')
            elif isinstance(item, (PropEmpty, PropComment)):
                synced.append(item.to_string() + '\n')
            else:
                raise RuntimeError(f'Unknown entry type: {type(item)}')

        Log.i(f'Re-writing translation file: {self.file}')
        with open(self.file, 'w') as fh:
            fh.writelines(synced)

    # #################################################################################################

    def _load(self, file: Path) -> bool:
        """
        Loads and parses *.properties file.

        :param file: File to load.
        :return:
        """
        if not file.exists():
            return False

        with open(file, 'r') as fh:
            line_number: int = 0

            duplicated_keys = ReportGroup('Duplicated keys')

            while True:
                line_number += 1
                line: str = fh.readline()
                if not line:
                    break

                # remove CRLF
                if line and line[-1] == '\n':  # LF
                    line = line[:-1]
                if line and line[-1] == '\r':  # CR
                    line = line[:-1]

                # Skip empty lines
                if line.strip() == '':
                    self.append(PropEmpty())
                    continue

                if line[0] in Config.ALLOWED_COMMENT_MARKERS:
                    self.append(PropComment(line))
                    continue

                if not self.separator:
                    # Let's look for used separator character
                    for _, single_char in enumerate(line):
                        if single_char in Config.ALLOWED_SEPARATORS:
                            self.separator = single_char
                            break

                tmp: List[str] = line.split(self.separator)
                if len(tmp) < 2:
                    Utils.abort([
                        f'Invalid syntax. Line {line_number}, file: {file}',
                        f'Using "{self.separator}" as separator.',
                    ])

                key = tmp[0].strip()
                val = ''.join(tmp[1:]).lstrip()
                if key not in self.keys:
                    self.append(PropTranslation(key, val, self.separator))
                else:
                    duplicated_keys.error(line_number, f'Duplicated key "{key}".')

            if not duplicated_keys.empty():
                self.report.add(duplicated_keys)

        return True
