"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from sys import exit
from typing import Dict, List, Union


# DO NOT use Log class in Utils. That causes some dependency issues which are NOT
# worth solving.

# #################################################################################################

class Utils(object):
    @staticmethod
    def abort(msg: Union[str, List[str]] = 'Aborted', rc: int = 10) -> None:
        if isinstance(msg, str):
            msg = [msg]
        print(msg)
        exit(rc)

    @staticmethod
    def add_if_not_in_list(target_list: List[str], items: Union[str, List[str]]) -> None:
        """
        Adds given val to specified array, avoids duplicates.

        :param target_list: list to add data to
        :param items: data item(s) to add to list
        :return:

        raises TypeError
        """
        if isinstance(items, str):
            items = [str]
        if not isinstance(items, list):
            raise TypeError(f'add_if_not_in_list() accepts str or List[str] only. {type(items)} passed')

        for entry in items:
            if entry not in target_list:
                target_list.append(entry)

    @staticmethod
    def add_if_not_in_dict(dictionary: Dict, key: str, val) -> bool:
        """
        Adds given val to specified dict, avoids duplicates.

        :param dictionary: dict to add data to
        :param key: unique key
        :param val: data to add to array
        :return: True if added, False if not added due to existing entry
        """
        if key not in dictionary:
            dictionary[key] = val
            return True
        return False

    @staticmethod
    def remove_quotes(src_str: str) -> str:
        if len(src_str) >= 2:
            if src_str[0] == '"':
                src_str = src_str[1:]
            end_pos = src_str.rfind('"')
            if end_pos != -1:
                src_str = src_str[:end_pos]

        return src_str

    @staticmethod
    def upper_first(src_str: str) -> str:
        if src_str:
            return src_str[0].upper() + src_str[1:]
        return src_str

    @staticmethod
    def lower_first(src_str: str) -> str:
        if src_str:
            return src_str[0].lower() + src_str[1:]
        return src_str
