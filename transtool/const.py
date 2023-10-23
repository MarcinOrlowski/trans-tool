#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2023 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#


from typing import List


class Const(object):
    APP_NAME: str = 'trans-tool'
    APP_VERSION: str = '2.5.3'
    APP_URL: str = 'https://github.com/MarcinOrlowski/trans-tool/'
    APP_YEARS: str = '2021-2023';

    APP_DESCRIPTION: List[str] = [
        f'{APP_NAME} v{APP_VERSION} * Copyright {APP_YEARS} by Marcin Orlowski.',
        'The translation files checker and syncing tool.',
        f'{APP_URL}',
    ]

    class RC(object):  # noqa: WPS431
        """
        Application return codes.
        """

        OK: int = 0
        TRANSLATION_SYNTAX_ERROR = 200
