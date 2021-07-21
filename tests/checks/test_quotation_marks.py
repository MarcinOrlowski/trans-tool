"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""
from checks.checks_test_case import ChecksTestCase
from proptool.checks.base.check import Check
from proptool.checks.quotation_marks import QuotationMarks
from proptool.config import Config
from proptool.prop.entries import PropComment, PropTranslation
from proptool.decorators.overrides import overrides


# TODO: Test handling other types than PropTranslation, PropComment

# #################################################################################################

class TestQuotationMarks(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return QuotationMarks(config)

    # #################################################################################################

    def test_translation_no_faults(self):
        self.check_single_file(PropTranslation('key', '""'))

    def test_translation_with_faults(self):
        self.check_single_file(PropTranslation('key', '"""'), exp_errors = 1)

    # #################################################################################################

    def test_comment_no_faults(self):
        self.check_single_file(PropComment('#  "foo" '))

    def test_comment_with_faults(self):
        self.check_single_file(PropComment('# "foo `"  '), exp_warnings = 1)