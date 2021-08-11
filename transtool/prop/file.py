"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import copy
import re
from pathlib import Path
from typing import List, Union

from transtool.config.config import Config
from transtool.log import Log
from transtool.prop.items import Blank, Comment, PropItem, Translation
from transtool.report.group import ReportGroup
from transtool.report.report import Report


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
            if not issubclass(type(single_item), PropItem):
                raise TypeError(f'Item must be of PropItem, {type(single_item)} given.')

            if isinstance(single_item, Translation):
                self.keys.append(single_item.key)
            elif isinstance(single_item, Comment):
                # Let's look for commented out keys.
                match = re.compile(Config.COMMENTED_TRANS_REGEXP).match(single_item.value)
                if match:
                    self.commented_out_keys.append(match.group(1))
            self._items.append(single_item)

    # #################################################################################################

    def update(self, reference: 'PropFile') -> None:
        """
        Rewrites content of the file using reference file as foundation. It then adds all keys from reference files.
        The update rules are as follow:
        * If we have translation for it, we add it,
        * if we do not have it, it will go as comment and recorded as commented-out key,
        * all reference files comments are copied to,
        * dangling keys and translation file comments are gone.

        :param reference:
        """

        tmp = PropFile(self.config)

        for idx, item in enumerate(reference.items):
            # Copy comments and blank lines as-is
            if isinstance(item, (Comment, Blank)):
                tmp.append(item)
            elif isinstance(item, Translation):
                if self.config.write_reference:
                    # Write reference even if we have a translation (for. i.e. proofreading).
                    tmp.append(Comment(f'{self.config.comment_marker} {item.key} {self.config.separator} {item.value}'))
                if item.key in self.keys:
                    # Write existing translation
                    tmp.append(self.find_by_key(item.key))
                else:
                    # We do not have the translation yet.
                    if self.config.write_reference:
                        # But as we wrote reference comment already, let's put just a key, without the value.
                        tmp.append(Comment.get_commented_out_key_comment(self.config, item.key))
                    else:
                        tmp.append(Comment.get_commented_out_key_comment(self.config, item.key, item.value))
            else:
                raise TypeError(f'Unknown entry type: {type(item)} at position {idx + 1}')

        self._items = tmp.items
        self.keys = tmp.keys
        self.commented_out_keys = tmp.commented_out_keys

    # #################################################################################################

    def validate(self, reference_file: 'PropFile') -> bool:
        """
        Validates given PropFile against provided reference file.

        :param reference_file:
        :return: True if file is valid, False if there were errors.
        """
        if not self.config.checks:
            raise RuntimeError('Checks config element cannot be empty.')

        for _, checker_info in self.config.checks.items():
            checker = checker_info.callable(checker_info.config)
            # Each validator gets copy of the files, to prevent any potential destructive operation.
            self.report.add(checker.check(copy.copy(self), copy.copy(reference_file)))

        return self.report.empty()

    # #################################################################################################

    def load(self, file: Path, language: str = None):
        """
        Loads and parses *.properties file.

        :param file: File to load.
        :param language: Optional language code the loaded data if for.
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
                tmp = Translation.parse_translation_line(line)
                if not tmp:
                    raise SyntaxError(f'Invalid syntax at line {line_number} of "{file}".')

                key = tmp[0].strip()
                separator = tmp[1].strip()
                val = tmp[2].lstrip()
                if key in self.keys:
                    duplicated_keys.error(line_number, 'Duplicated key.', key)
                    continue

                self.append(Translation(key, val, separator))

            if not duplicated_keys.empty():
                self.report.add(duplicated_keys)

    # #################################################################################################

    def save(self, target_file_name: Union[Path, None] = None) -> None:
        """
        Saves content of the propfile.
        """

        if not target_file_name:
            if not self.file:
                raise ValueError('No target file name given.')
            target_file_name = self.file

        content = []
        for item in self.items:
            content.append(item.to_string())

        Log.i(f'Writing: {target_file_name}')
        with open(target_file_name, 'w') as fh:
            # FIXME: LF/CRLF should configurable
            fh.write('\n'.join(content))
