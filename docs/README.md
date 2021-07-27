![prop-tool logo](../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

## Table of contents ##

* [« Main README](../README.md)
* [« Documentation table of contents](README.md)
* [Usage examples](usage.md)
  * [Updating translations](usage.md#updating-translations)
* [Available validators](checks/README.md)
* [Installation](#installation)
* [Developer corner](developers.md)
* [Links](#additional-links)

---

## Installation ##

You can install `prop-tool` from [PyPi](https://pypi.org/project/prop-tool/):

```bash
pip install prop-tool
```

Alternatively, you can download `*.whl` archive and install it manually by issuing:

```bash
pip install --upgrade <FILE>.whl
```

You may also want to setup [virtual environment](https://docs.python.org/3/library/venv.html) first.

---

## Limitations ##

* As of now `prop-tool` do not handle multiline entries.
* `FormattingValues` check will do not support positional placeholders, formats using space leading positive numbers.
* `TypesettingQuotationMarks` is not covering all possible pairs yet due
  to [limitations of current implementation](https://github.com/MarcinOrlowski/prop-tool/issues/19).

## Additional links ##

* The `*.properties` syntax support is based on official [file format documentation](https://docs.oracle.com/cd/E23095_01/Platform.93/ATGProgGuide/html/s0204propertiesfileformat01.html).
