#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool
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
            referenceFile = Path(fileStr)

            tmp = Path(referenceFile).name.split('.')
            if len(tmp) != 2:
                Util.abort('Base filename format invalid. Must be "prefix.suffix".')
            namePrefix = tmp[0]
            nameSuffix = tmp[1]

            reference = PropFile(app, referenceFile)

            if app.verbose:
                print(referenceFile)

            for lang in app.languages:
                langFilePath = Path(referenceFile.parent / f'{namePrefix}_{lang}.{nameSuffix}')
                langFile = PropFile(app, langFilePath)
                if not langFile.validateAndFix(reference):
                    errors += 1

        # log.dump()

        sys.exit(100 if errors else 0)
