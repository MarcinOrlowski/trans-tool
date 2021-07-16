# prop-tool #

`prop-tool` - Java *.properties file checker and syncing tool.

This utility can be used to check if translation files stay in sync with base file. It can also rewrite translation files adding
missing keys based on the content of base file.

Based on `*.properties`
[file format docs](https://docs.oracle.com/cd/E23095_01/Platform.93/ATGProgGuide/html/s0204propertiesfileformat01.html).

## Installation ##

You can install `prop-tool` form PyPi by using `pip`:

```bash
pip install prop-tool
```

or by downloading `*.whl` archive and issuing:

```bash
pip install --upgrade <FILE>.whl
```

## Validation ##

For `prop-tool` base file `A` and its translation file `B` are in sync when:

1. All keys present in base file are also present in translation file.
1. There's no dangling keys (not existing in base) present in translation file.

NOTE: as this is quite common that translation file may not be updated instantly, `prop-tool` considers key presence condition
fulfilled also when given key exists in `B` file but is commented out and follow expected comment format:

```
# ==> KEY =
```

If you want to ensure that all keys are in fact translated, use `--strict` mode while checking.

When running with `--strict` option, all keys

## Fixing files ##

You can use `prop-tool` to update your translation files by using `--fix` option. I such case `prop-tool` will completely rewrite
translation files, adding missing keys (in commented out form).

NOTE: Be aware that `--fix` do NOT update existing translation file but builds it completely using base file as reference and
existing translations (if present). No other content of translation files (i.e. comments etc) will be preserved.

## Usage examples ##

Check if `de` translation of `test.properties` exists and is in sync:

```bash
prop-tool --base test.properties --lang de
```

You can omit `.properties` suffix in command line argument. NOTE: that file name must contain `.properties`
suffix, otherwise it will not be found:

```bash
prop-tool --base test --lang de
```

it will then look for `test_de.properties` file in the same folder `test.properties` resides and check it.

---

Check if `de`, `pl` and `fr` translations of `test.properties` and `gui.properties` exist and are in sync:

```bash
prop-tool --base test gui --lang de pl fr
```

it will then look for and validate following files

```bash
test_de.properties
test_pl.properties
test_fr.properties
gui_de.properties
gui_pl.properties
gui_fr.properties
```

## Limitations ##

* As of now `prop-tool` do not handle multiline entries.

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* prop-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
