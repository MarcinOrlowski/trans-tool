#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
from .check import Check
from ..app import App
from ..entries import PropTranslation, PropComment
from ..overrides import overrides
from ..propfile import PropFile
from ..report.report import Report


# #################################################################################################

class TrailingWhiteChars(Check):
    """
    Checks if file has trailing white characters at the end of each line.
    """

    @staticmethod
    @overrides(Check)
    def check(app: App, reference_file: PropFile, translation_file: PropFile = None) -> Report:

        if reference_file is None and translation_file is None:
            raise RuntimeError('You must pass either reference or translation file.')
        if reference_file is not None and translation_file is not None:
            raise RuntimeError('Either reference or translation file can be passed. Not both.')

        propfile = reference_file if reference_file is not None else translation_file

        report = Report()
        for idx, item in enumerate(propfile):
            if isinstance(item, (PropTranslation, PropComment)):
                diff = len(item.value) - len(item.value.rstrip())
                if diff == 0:
                    continue

                if isinstance(item, PropTranslation):
                    report.error(idx + 1, f'In "{item.key}" entry: {diff}')
                else:
                    report.warn(idx + 1, f'In comment: {diff}')

        return report
