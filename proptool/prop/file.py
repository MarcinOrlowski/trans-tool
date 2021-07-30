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

from proptool.config.config import Config
from proptool.log import Log
from proptool.prop.items import Blank, Comment, PropItem, Translation
from proptool.report.group import ReportGroup
from proptool.report.report import Report
from proptool.utils import Utils


# #################################################################################################

class PropFile(object):
    def __init__(self, config: Config, language: str = None):
        super().__init__()

        self.config: Config = config

        self._items: List[PropItem] = []

        self.file: Union[Path, None] = None
        self.loaded: bool = False

        # All the keys of 'regular' translations
        self.keys: List[str] = []
        # All the keys in form `# ==> KEY =` that we found.
        self.commented_out_keys: List[str] = []

        self.separator: str = config.separator
        self.report: Report = Report(config)

        self.language = language

        # This call is most likely redundant here.
        self.init_container(language)

        comment_pattern = re.escape(self.config.comment_template).replace(
            'COM', f'[{"".join(Config.ALLOWED_COMMENT_MARKERS)}]').replace(
            'SEP', f'[{"".join(Config.ALLOWED_SEPARATORS)}]')
        # NOTE: key pattern must be in () brackets to form a group used later!
        comment_pattern = comment_pattern.replace('KEY', '([a-zAz][a-zA-z0-9_.-]+)')
        self.comment_pattern = f'^{comment_pattern}'

    def init_container(self, language: str) -> None:
        self._items = []
        self.keys = []
        self.commented_out_keys = []
        self.loaded = False
        self.report = Report(self.config)
        self.language = language

    # #################################################################################################

    @property
    def items(self) -> List[PropItem]:
        return self._items

    # #################################################################################################

    def find_by_key(self, key: str) -> Union[Translation, None]:
        """
        Returns translation entry referenced by given key or None.

        :param key: Translation key to look for.
        :return: Instance of PropTranslation or None.
        """
        # noinspection PyTypeChecker
        translations: List[Translation] = list(filter(lambda entry: isinstance(entry, Translation), self.items))
        for item in translations:
            if item.key == key:
                return item
        return None

    # #################################################################################################

    def append(self, items: Union[List[PropItem], PropItem]) -> None:
        """
        Appends given PropItem(s) to internal buffer.

        :param items: PropItem(s) to be added.
        """
        if issubclass(type(items), PropItem):
            items = [items]

        if not issubclass(type(items), list):
            raise TypeError('Item must be either subclass of PropItem or List[PropItems]')

        for single_item in items:
            if isinstance(items, Translation):
                self.keys.append(items.key)
            elif isinstance(items, Comment):
                # Let's look for commented out keys.
                match = re.compile(self.comment_pattern).match(items.value)
                if match:
                    self.commented_out_keys.append(match.group(1))
            self._items.append(items)

    # #################################################################################################

    def update(self, reference_propfile: 'PropFile') -> None:
        """
        Rewrites content of the file using reference file as foundation. It then adds all keys from reference files.
        The update rules are as follow:
        * If we have translation for it, we add it,
        * if we do not have it, it will go as comment and recorded as commented-out key,
        * all reference files comments are copied to,
        * dangling keys and translation file comments are gone.

        :param reference_propfile:
        """

        tmp = PropFile(self.config)
        tmp.append([
            Comment(),
            Comment(f'Base: {reference_propfile}'),
        ])
        if self.language is not None:
            tmp.append(Comment(f'Lang: {self.language}'))
        tmp.append(Comment())

        # For all items in reference file...
        for idx, item in enumerate(reference_propfile.items):
            # Copy comments and blank lines as-is
            if isinstance(item, (Comment, Blank)):
                tmp.append(item)
            elif isinstance(item, Translation):
                # If we do have the translation already
                if item.key in self.keys:
                    # Add original string as comment if that's requested
                    tmp.append(Comment(f'BASE: {item.value}'))
                    # Copy our translation.
                    tmp.append(self.find_by_key(item.key))
                else:
                    tmp.append(Comment(self.config.comment_pattern.replace('KEY', item.key)))
            else:
                raise RuntimeError(f'Unknown entry type: {type(item)} at position {idx + 1}')

        self._items = copy.copy(tmp.items)
        self.keys = copy.copy(tmp.keys)
        self.commented_out_keys = copy.copy(tmp.commented_out_keys)

    # #################################################################################################

    def is_valid(self, reference_file: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference_file:
        :return: True if file is valid, False if there were errors.
        """
        for checker_id, checker_info in self.config.checks.items():
            checker = checker_info.cls(checker_info.config)
            # Each validator gets copy of the files, to prevent any potential destructive operation.
            self.report.add(checker.check(copy.copy(self), copy.copy(reference_file)))

        return self.report.empty()

    # #################################################################################################

    def load(self, file: Path, language: str = None) -> bool:
        """
        Loads and parses *.properties file.

        :param file: File to load.
        :param language: Optional language code the loaded data if for.
        :return: True if file loaded correctly, False otherwise.
        """

        if not file.exists():
            raise FileNotFoundError(f'File not found: {file}')

        self.init_container(language)
        self.file = file

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
                    self.append(Blank())
                    continue

                if line[0] in Config.ALLOWED_COMMENT_MARKERS:
                    self.append(Comment(line))
                    continue

                # Whatever left should be valid key[:=]val entry
                tmp: List[str] = re.split(f'^(.+)([{"".join(Config.ALLOWED_SEPARATORS)}])(.+)$', line)
                if len(tmp) != 5:
                    Log.e(f'Invalid syntax at line {line_number} of "{file}".')
                    Utils.abort()

                key = tmp[1].strip()
                separator = tmp[2].strip()
                val = tmp[3].lstrip()
                if key not in self.keys:
                    self.append(Translation(key, val, separator))
                else:
                    duplicated_keys.error(line_number, f'Duplicated key "{key}".')

            if not duplicated_keys.empty():
                self.report.add(duplicated_keys)

        return True

    # #################################################################################################

    def save(self, target_file_name: Union[Path, None] = None) -> None:
        """
        Saves content of the propfile.
        """

        if not target_file_name:
            if not self.file:
                raise RuntimeError('No target file name given.')
            target_file_name = self.file

        Log.i(f'Saving: {target_file_name}')
        with open(target_file_name, 'w') as fh:
            for item in self.items:
                # FIXME: LF/CRLF should configurable
                fh.write(f'{item.to_string()}\n')
