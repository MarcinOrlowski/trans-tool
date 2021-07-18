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
        for fileStr in app.files:
            referenceFilePath = Path(fileStr)

            tmp = Path(referenceFilePath).name.split('.')
            if len(tmp) != 2:
                Util.abort('Base filename format invalid. Must be "prefix.suffix".')
            namePrefix = tmp[0]
            nameSuffix = tmp[1]

            referenceFile = PropFile(app, referenceFilePath)
            if not referenceFile.loaded:
                Util.abort(f'File not found: {referenceFilePath}')

            if app.verbose:
                print(referenceFilePath)

            for lang in app.languages:
                translationFilePath = Path(referenceFilePath.parent / f'{namePrefix}_{lang}.{nameSuffix}')
                translationFile = PropFile(app, translationFilePath)
                if not translationFile.validateAndFix(referenceFile):
                    errors += 1

        # log.dump()

        sys.exit(100 if errors else 0)
