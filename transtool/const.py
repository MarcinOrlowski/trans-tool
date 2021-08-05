"""
# trans-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

from typing import List


class Const(object):
    APP_NAME: str = 'trans-tool'
    APP_VERSION: str = '2.0.0'
    APP_URL: str = 'https://github.com/MarcinOrlowski/trans-tool/'

    APP_DESCRIPTION: List[str] = [
        f'{APP_NAME} v{APP_VERSION} * Copyright 2021 by Marcin Orlowski.',
        'The *.properties file checker and syncing tool.',
        f'{APP_URL}',
    ]

    class RC(object):  # noqa: WPS431
        """
        Application return codes.
        """

        OK: int = 0
        TRANSLATION_SYNTAX_ERROR = 200