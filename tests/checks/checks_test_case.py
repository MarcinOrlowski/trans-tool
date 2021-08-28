"""
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""
import random
from abc import abstractmethod
from typing import Dict, List, Union

from transtool.checks.base.check import Check
from transtool.config.config import Config
from transtool.prop.file import PropFile
from transtool.prop.items import Blank, Comment, PropItem, Translation
from tests.test_case import TestCase


class ChecksTestCase(TestCase):

    def setUp(self) -> None:
        self.config: Config = Config()

        checker = self.get_checker(None)
        if not issubclass(type(checker), Check):
            raise ValueError('Checker must be subclass of Check')
        checker.config = self.get_checker().get_default_config()
        self.checker = checker

    @abstractmethod
    def get_checker(self, config: Union[Dict, None] = None) -> Check:
        raise NotImplementedError

    def check_single_file(self, entry: PropItem, exp_errors: int = 0, exp_warnings: int = 0,
                          force_report_dump: bool = False) -> None:
        propfile = PropFile(self.config)
        propfile.loaded = True
        propfile.items.append(entry)

        self.check(propfile, exp_errors = exp_errors, exp_warnings = exp_warnings, force_report_dump = force_report_dump)

    def check(self, translation: PropFile, reference: Union[PropFile, None] = None,
              exp_errors: int = 0, exp_warnings: int = 0, force_report_dump = False, msg = None) -> None:
        report = self.checker.check(translation, reference)

        # Dump the report details if there's mismatch between results and expectations or if dump is enforced.
        if (exp_errors != report.errors) or (exp_warnings != report.warnings) or force_report_dump:
            if report.errors + report.warnings > 0 or force_report_dump:
                report.dump()

        self.assertEqual(exp_errors, report.errors, msg)
        self.assertEqual(exp_warnings, report.warnings, msg)

    # #################################################################################################

    def build_prepfile(self, contents: Union[List[str], List[PropItem]], lower: bool = False) -> PropFile:
        prep_file = PropFile(self.config)
        prep_file.loaded = True

        for item in contents:
            if isinstance(item, str):
                value = self.get_random_string()
                if lower:
                    value = value.lower()
                prep_file.append(Translation(item, value))
            elif isinstance(item, PropItem):
                prep_file.append(item)
            else:
                raise RuntimeError(f'Unsupported content type: {type(item)}')

        return prep_file

    # #################################################################################################

    def check_skipping_blank(self) -> None:
        """
        Checks if Blank items are skipped correctly. Used to test checker with two PropFiles needed.
        """
        ref_file = PropFile(self.config)
        ref_file.append(Blank())
        trans_file = PropFile(self.config)
        trans_file.append(Blank())

        self.check(trans_file, ref_file)

    def check_skipping_blank_and_comment(self) -> None:
        """
        Checks if Blank and Comment items are skipped correctly. Used to test checker with two PropFiles needed.
        """
        ref_file = PropFile(self.config)
        ref_file.append(Blank())
        ref_file.append(Comment(self.config.ALLOWED_COMMENT_MARKERS[0] + self.get_random_string()))
        trans_file = PropFile(self.config)
        trans_file.append(Blank())
        trans_file.append(Comment(self.config.ALLOWED_COMMENT_MARKERS[0] + self.get_random_string()))

        self.check(trans_file, ref_file)

    def check_skipping_of_dangling_keys(self) -> None:
        """
        Tests if dangling translation keys are silently skipped.
        """
        # generate some keys for translation file
        cnt_min = 20
        cnt_max = 40
        trans_keys = [self.get_random_string('key') for _ in range(random.randint(cnt_min, cnt_max))]

        # have less keys for reference file
        upper_bound = 10
        how_many_less = random.randint(1, upper_bound)
        ref_keys = trans_keys[:(how_many_less * -1)]

        ref_file = self.build_prepfile(ref_keys, lower = True)
        trans_file = self.build_prepfile(trans_keys, lower = True)
        self.check(trans_file, ref_file)

    # #################################################################################################

    def _do_checker_comment_test(self, tests: List[Comment], comm_exp_warnings: int) -> None:
        """
        Helper method to test certain checkers against faults in comments where checker supports
        `comments` configuration option that lets user include or exlude comments for checking.

        :param tests: List of instances of Comment
        :param comm_exp_warnings: number of expected warnings that should be spotted if scanning comments is enabled.
        """
        for test in tests:
            if not isinstance(test, Comment):
                self.fail(f'Test item must be instance of Comment ({type(item)} given).')

            # Expect no issues if comment scanning is disabled
            self.checker.config['comments'] = False
            self.check_single_file(test)

            # Expect warning raised.
            self.checker.config['comments'] = True
            self.check_single_file(test, exp_warnings = comm_exp_warnings)
