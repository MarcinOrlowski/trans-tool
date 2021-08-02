![prop-tool logo](artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

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

---

## Table of contents ##

* [Introduction](#introduction)
* [Extensive documentation](docs/README.md)
  * [Available validators](docs/checks/README.md)
  * [Usage examples](docs/usage.md)
  * [Config file](docs/config.md)
* [Features](#features)
* [Changelog](docs/CHANGES.md)
* [License](#license)

---

## Introduction ##

`prop-tool` is a small but powerful utility aimed at your projects' `*.properties` files. It looks like text based INI file, but it
is even simpler and because to its simplicity, this file format is often used to keep the configurations or translations (i.e. in
Java world). Example file:

```ini
# Example of *.properties file
programTitle = Prop-Tool v2.0.0
okButton = "OK"
```

The main role of `prop-tool` is to help you keep your `*.properties` files in order, ensuring all files are
syntactically correct and all the translation files are in sync with base (main language) file. It also comes with huge set of
various linters and checkers to guard quality of the files' contents. It can check for missing or dangling keys, inproper
punctuation, open brackets, quotation marks and more. It can also automatically sync translation files quickly providing fresh
template for your translators to work on.

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

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* prop-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
