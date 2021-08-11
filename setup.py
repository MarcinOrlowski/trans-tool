#!/usr/bin/env python3

"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
#
# python3 -m venv venv
# source venv/activate.fish
# pip install wheel twine
# python3 setup.py sdist bdist_wheel
# pip install --upgrade dist/trans_tool-2.0.0-py3-none-any.whl
# twine upload dist/*
#
"""

from transtool.const import Const
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    logo_url = 'https://raw.githubusercontent.com/MarcinOrlowski/trans-tool/master/artwork/trans-tool-logo.png'
    readme = fh.read().replace(r'![trans-tool logo](artwork/trans-tool-logo.png)',
                               f'![trans-tool logo]({logo_url})', 1)

    setup(
        name = Const.APP_NAME,
        version = Const.APP_VERSION,
        packages = find_packages(),

        install_requires = [
            'argparse>=1.4.0',
        ],
        python_requires = '>=3.6',
        entry_points = {
            'console_scripts': [
                'trans-tool = transtool.main:TransTool.start',
                'transtool = transtool.main:TransTool.start',
            ],
        },

        author = 'Marcin Orlowski',
        author_email = 'mail@marcinOrlowski.com',
        description = 'The translation files checker and syncing tool.',
        long_description = readme,
        long_description_content_type = 'text/markdown',
        url = Const.APP_URL,
        keywords = 'translation helper locale language sync check validation',
        project_urls = {
            'Bug Tracker':   'https://github.com/MarcinOrlowski/trans-tool/issues/',
            'Documentation': 'https://github.com/MarcinOrlowski/trans-tool/',
            'Source Code':   'https://github.com/MarcinOrlowski/trans-tool/',
        },
        # https://choosealicense.com/
        license = 'MIT License',
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )
