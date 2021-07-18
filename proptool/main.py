#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#

import sys
from pathlib import Path

from .app import App
from .propfile import PropFile
from .util import Util


class Main:
    @staticmethod
    def start() -> int:
        app = App()

        errors = 0
        for file_str in app.files:
            reference_file_path = Path(file_str)

            tmp = Path(reference_file_path).name.split('.')
            if len(tmp) != 2:
                Util.abort('Base filename format invalid. Must be "prefix.suffix".')
            name_prefix = tmp[0]
            name_suffix = tmp[1]

            referenceFile = PropFile(app, reference_file_path)
            if not referenceFile.loaded:
                Util.abort(f'File not found: {reference_file_path}')

            if app.verbose:
                print(reference_file_path)

            for lang in app.languages:
                translation_file_path = Path(reference_file_path.parent / f'{name_prefix}_{lang}.{name_suffix}')
                translation_file = PropFile(app, translation_file_path)
                if not translation_file.validateAndFix(referenceFile):
                    errors += 1

        # log.dump()

        sys.exit(100 if errors else 0)
