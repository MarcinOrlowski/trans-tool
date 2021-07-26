![prop-tool logo](artwork/prop-tool-logo.png)

# Java *.properties file checker and syncing tool #

[master](https://github.com/MarcinOrlowski/prop-tool/tree/master) branch:
[![Unit tests](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/prop-tool/branch/master/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/prop-tool)
[![Code lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml)

[development](https://github.com/MarcinOrlowski/prop-tool/tree/dev) branch:
[![Unit tests](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/prop-tool/branch/dev/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/prop-tool)
[![Code lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml)

## Table of contents ##

* [Introduction](#introduction)
* [Extensive documentation](docs/README.md)
  * [Available validators](docs/checks/README.md)
  * [Usage examples](docs/usage.md)
  * [Config file](docs/config.md)
* [Features](#features)
* [Extensive documentation](docs/README.md)
* [License](#license)
* [Changelog](docs/CHANGES.md)

---

## Introduction ##

`prop-tool` is a small but powerful utility aimed at your (mainly Java) projects' `*.properties` files. Its main role is to ensure
all files are syntactically correct and all the translation files are in sync with base (main language) file. It also comes with
huge set of various linters and checkers to guard quality of the files' contents. It can check for missing or dangling keys,
inproper punctuation, open brackets, quotation marks and more. It can also automatically sync translation files quickly providing
fresh template for your translators to work on.

```bash
$ prop-tool -b mark -l pl -v
Base: mark.properties
  Warnings: 1
    Brackets
      W: Line 3:16: No closing bracket for "<"
  PL: brackets_pl.properties
    Errors: 8, warnings: 3
      Sentence starts with different letter case.
        E: Line 8: "missingClosing" starts with lower-cased character. Expected UPPER-cased.
      Trailing white characters
        W: line 2: In comment: 2
        E: line 4: In "question" entry: 1
      Punctuation mismatch
        E: line 3: "exclamation" ends with " ". Expected "!".
        E: line 4: "newline" ends with "". Expected "\n".
      Bracket mismatch
        E: Line 2:1: "missingClosing": No closing bracket for "(".
        W: Line 3:16: No closing bracket for "<"
        E: Line 4:4: "missingOpening": No opening bracket matching ")".
      Quotation marks
        E: Line 12:5: "missingSingle": Quotation mark mismatch. Expected ", found `.
        E: Line 13:5: "remaining": Quotation mark mismatch. Expected ", found `.
        W: Line 14:11: No closing mark for ".
```

## Config file and command line arguments ##

You can use `prop-tool` by providing all required parameters directly from command line (see `--help`), or you can create
configuration file and use `--config` option to make `prop-tool` load it and use. Almost all options can be set in configuration
files, which helps, for example using `prop-tool` as part of CI/CD or GitHub Actions.

Configuration file is plain text file, following [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created using
any text editor. Please see commented [config.ini](config.ini) for example configuration file and all available options.

> NOTE: when using configuration file and command line arguments, the order of precedence is this:
>
> * default configuration goes first,
> * if config file is given and can be loaded and parsed, then it overrides default configuration,
> * if there's any command but line argument `--config` specified, then it overrides whatever is is set in config file.
>
> For example:
>
> * by default, `verbose` option is off,
> * your config file sets `verbose = true`, enabling verbose output,
> * but your invocation is `prop-tool --config config.ini --no-verbose`, therefore `verbose` mode is set `OFF`.

## Limitations ##

* As of now `prop-tool` do not handle multiline entries.
* `FormattingValues` check will do not support positional placeholders, formats using space leading positive numbers.
* `TypesettingQuotationMarks` is not covering all possible pairs yet due
  to [limitations of current implementation](https://github.com/MarcinOrlowski/prop-tool/issues/19).

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* prop-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
