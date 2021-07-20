#!/usr/bin/env python3

"""
#
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
#
# python3 -m venv venv
# source venv/activate.fish
# pip install wheel twine
# python3 setup.py sdist bdist_wheel
# pip install --upgrade dist/prop_tool-1.1.0-py3-none-any.whl
# twine upload dist/*
#
"""

from proptool.const import Const
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    readme = fh.read()

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
            'prop-tool = proptool.main:Main.start',
            'proptool = proptool.main:Main.start',
        ],
    },

    author = 'Marcin Orlowski',
    author_email = 'mail@marcinOrlowski.com',
    description = 'prop-tool: Java *.properties file sync checker and syncing tool.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    url = Const.APP_URL,
    keywords = 'java properties sync check validation',
    project_urls = {
        'Bug Tracker':   'https://github.com/MarcinOrlowski/prop-tool/issues/',
        'Documentation': 'https://github.com/MarcinOrlowski/prop-tool/',
        'Source Code':   'https://github.com/MarcinOrlowski/prop-tool/',
    },
    # https://choosealicense.com/
    license = 'MIT License',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
