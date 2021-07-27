![prop-tool logo](../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

# Developer's corner #

`prop-tool` is Python 3 application. It has no external runtime dependencies, however code quality is automatically checked using
additional tools that require additional installation.  These tests are run automatically on the code repository against
any new commited code and each pull-request created using Github Actions feature (see `.github/workflows` folder for
configuration details).

If you'd like to try them by hand locally here's how.

## Virtual environment ##

Fist, create virtual environment and activate it. **ALL Python related examples are assumed to be executed withing virtual
environment and your working directory points to root folder of the project.**

```bash
$ python -m venv venv
```

Activate your environment in Bash compatible shell (if you are using different shell, i.e. Fish, check contents of `venv/bin/`
folder for alternative scripts):

```bash
$ source venv/bin/activate
```

---

## Unit tests ##

Run unit tests using standard `unittest` feature (if you want more detailed output, add `-v` to the invocation):

```bash
$ python -m unittest discover
...............................................................................................................
----------------------------------------------------------------------
Ran 111 tests in 0.047s

OK
```

Unit tests can be run using [pytest](https://pytest.org/) package too (remove `--quiet` if you want to see
tests details). Install `pytest` first:

```bash
$ pip install pytest
```

and then run:

```bash
$ pytest --quiet
................................................................................. [ 72%]
..............................                                                    [100%]
111 passed in 0.24s
```

---

## Python code QA ##

I use `Flake8` and [wemake-python-styleguide](https://wemake-python-stylegui.de/en/latest/) and additional plugins to
ensure code quality:

```bash
$ pip install wemake-python-styleguide
```

Lint the code (Default settings is very aggressive so `.flake8` config file tunes it to my requirements):

```bash
$ flake8 proptool/ tests/
```

No output means no issues.

---

## Packaging ##

Install `wheel` first:

```bash
$ pip install wheel
```

and create Wheel package:

```bash
$ python3 setup.py sdist bdist_wheel
```

and install the package in your local virtual environment:

```bash
$ pip install --upgrade dist/prop_tool-<VERSION>-py3-none-any.whl
```

---

## Markdown lint ##

Documentation is written using [markdown](https://en.wikipedia.org/wiki/Markdown) and is checked
using [MarkdownLint](https://github.com/DavidAnson/markdownlint)
with use of [markdown-cli](https://github.com/igorshubovych/markdownlint-cli) wrapper. This linter is unfortunately not a Python
application, so virtual environment won't help us keep it isolated. It must be installed on your system using `npm` package manager.
You may need to install `npm` first as it usually is not preinstalled:

```bash
sudo apt install npm
```

Next, install the linter (see [markdown-cli](https://github.com/igorshubovych/markdownlint-cli) page for more info):

```bash
npm install -g markdownlint-cli
```

and lint all `*.md` files (linter configuration lives in `.markdownlint.yaml` file):

```bash
markdownlint --ignore LICENSE.md **/*.md
```

Note, the `LICENSE.md` file is externally sourced, therefore I am not going to fix it.

---

# Combining all checks together #

```bash
#!/bin/bash

set -uo pipefail

# Activate venv if not active
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
if pip show pytest --quiet && pytest --quiet --no-header --no-summary;
    pytest --quiet --no-header --no-summary
fi
echo "Code Lint"
flake8 proptool/ tests/
echo "MD Lint"
markdownlint --ignore LICENSE.md **/*.md
```
