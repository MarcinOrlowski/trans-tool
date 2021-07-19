"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""


def overrides(contract) -> callable:
    def overrider(method):
        """
        Introduces @overrides decorator.
        Source: https://stackoverflow.com/a/8313042
        """
        assert method.__name__ in dir(contract), f"No '{method.__name__}()' to override in '{contract.__name__}' class"
        return method

    return overrider
