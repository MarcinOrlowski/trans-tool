#!/bin/bash

set -uo pipefail

# Activate venv if needed
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
	echo "Activating virtual env..."
	source venv/bin/activate
fi

if [[ -z "${VIRTUAL_ENV}" ]]; then
	echo "*** Not in virtual env."
	return 1
fi

echo "Unit tests..."
python3 -m unittest discover --quiet
pip show pytest --quiet && pytest --quiet --no-header --no-summary
echo "Code Lint"
flake8 transtool/ tests/
echo "MD Lint"
markdownlint --config .markdownlint.yml --ignore LICENSE.md "**/*.md"
