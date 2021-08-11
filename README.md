![trans-tool logo](artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

[master](https://github.com/MarcinOrlowski/trans-tool/tree/master) branch:
[![Unit tests](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/trans-tool/branch/master/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/trans-tool)
[![Code lint](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/linter.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/markdown.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/markdown.yml)

[development](https://github.com/MarcinOrlowski/trans-tool/tree/dev) branch:
[![Unit tests](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/unittests.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/trans-tool/branch/dev/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/trans-tool)
[![Code lint](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/linter.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/markdown.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/trans-tool/actions/workflows/markdown.yml)

---

## Table of contents ##

* [Introduction](#introduction)
* [Extensive documentation](docs/README.md)
  * [Available validators](docs/checks/README.md)
  * [Usage examples](docs/usage.md)
  * [Config file](docs/config.md)
* [Changelog](docs/CHANGES.md)
* [License](#license)

---

## Introduction ##

`trans-tool` is a small but powerful utility aimed at your projects' translation files. It is armed
with several validators to watch for common mistakes in translations as well as base strings. It currently
loads `*.properties` files, which is file format often used in Java projects as the `trans-tool` was born
while working on [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution/).

Example `*.properties` file looks like simplified version of commonly used INI file:

```ini
# Example of *.properties file
programTitle = trans-tool v2.0.0
okButton = "OK"
```

Internally, `trans-tool` works on abstract format, thus adding support for other file formats can easy be added
which will happen upon demand.

While loading your `*.properties` files `trans-tool` checks if files are in order, ensuring all of them are
syntactically correct and all of the translations are in sync with main language. It also comes with huge set of
various linters and checkers to guard quality of the files' contents. It can check for missing or dangling keys, inproper
punctuation, open brackets, quotation marks and more. It can also automatically sync translation files quickly providing
fresh template for your translators to work on.

```bash
$ trans-tool -b soc -l pl

Base: src/main/resources/resources/logisim/strings/soc/soc.properties
  Errors: 1
    Brackets
      E: Line 163:90: "AssemblerRunSuccess": No opening character matching ")".
  PL: src/main/resources/resources/logisim/strings/soc/soc_pl.properties
    Errors: 3, warnings: 4
      Brackets
        E: Line 175:83: "AssemblerRunSuccess": No opening character matching ")".
      Formatting values
        E: Line 383:167: "PioMenuOutClearRemark": Expected "%s", found "%s.".
        E: Line 387:167: "PioMenuOutSetRemark": Expected "%s", found "%s.".
      Missing translations
        W: "ElfHeaderEIDataError": Missing translation.
        W: "AsmPanErrorCreateFile": Missing translation.
      Punctuation mismatch
        W: Line 12: "SocInsertTransWindowTitle": Ends with "y". Expected ":".
      First words case mismatch.
        W: Line 332: "Rv32imProgramCounter": Starts UPPER-cased, expected lower-case.
```

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* trans-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
* Project logo contains [elements from Flaticon.com](https://www.flaticon.com/free-icon/translation_99694).
* trans-tool project [PyPi page](https://pypi.org/project/trans-tool/).