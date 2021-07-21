"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from typing import List


class Const(object):
    APP_NAME: str = 'prop-tool'
    APP_VERSION: str = '1.2.0'
    APP_URL: str = 'https://github.com/MarcinOrlowski/prop-tool/'

    APP_DESCRIPTION: List[str] = [
        f'{APP_NAME} v{APP_VERSION} * Copyright 2021 by Marcin Orlowski.',
        'Java *.properties file checker and syncing tool.',
        f'{APP_URL}',
    ]
