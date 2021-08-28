#!/bin/bash
python3 setup.py sdist bdist_wheel
pip install --upgrade dist/trans_tool-2.1.0-py3-none-any.whl
