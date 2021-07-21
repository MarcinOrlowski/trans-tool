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
from proptool.checks.formatting_values import FormattingValues
from proptool.config import Config
from proptool.entries import PropTranslation
from proptool.overrides import overrides
from proptool.propfile import PropFile


# TODO: Test handling other types than PropTranslation

# #################################################################################################

class TestFormattingValues(ChecksTestCase):

    @overrides(ChecksTestCase)
    def get_checker(self, config: Config) -> Check:
        return FormattingValues(config)

    # #################################################################################################

    def test_no_faults(self):
        tests = [
            ('This %s foo %d %s', 'This 123 %s %d llorem bar %s ipsum.'),
            ('This has no %% formatters', 'Tricky one'),
        ]

        for test_case in tests:
            ref_file = PropFile(self.config)
            trans_file = PropFile(self.config)

            key = self.get_random_string()
            ref_file.append(PropTranslation(key, test_case[0]))
            trans_file.append(PropTranslation(key, test_case[1]))
            self.do_test(ref_file, trans_file)

    def test_with_faults(self):
        tests = [
            # Tests various types of formatters count mismatch
            ('This %s foo %s', 'This 123 %s %d llorem bar %s ipsum.'),
            ('This %s', 'This 123 %s %d llorem bar %s ipsum.'),
            ('%d foo', '123 %s %d llorem bar %s ipsum.'),
            ('No formatters', 'But we have %s ome...'),
            ('%s ome formatters', 'But we have none.'),

            # Count matches, but order is messed.
            ('Count matches: %s %d', 'But order differs: %d %s'),
        ]

        for test_case in tests:
            ref_file = PropFile(self.config)
            trans_file = PropFile(self.config)

            key = self.get_random_string()
            ref_file.append(PropTranslation(key, test_case[0]))
            trans_file.append(PropTranslation(key, test_case[1]))
            # This checker always return one error (if there's any fault).
            self.do_test(ref_file, trans_file, exp_errors = 1)
