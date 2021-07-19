# prop-tool #

`prop-tool` - Java *.properties file checker and syncing tool.

This utility can be used to check your `*.properties` Java files to ensure correct syntax is used, all translation files are in sync
with base file, ther're no missing keys or invalid punctuation and more. It can also create translation files adding missing keys
based on the content of base file.

```bash
$ prop-tool -b mark -l pl -v
Base: mark.properties
  Found 6 errors in "mark_pl.properties":
    Trailing white characters: 3
      W: line 2: In comment: 2
      E: line 4: In "question" entry: 1
      E: line 5: In "exclamation" entry: 1
    Punctuation mismatch: 3
      E: line 2: "question" ends with " ". Expected "?".
      E: line 3: "exclamation" ends with " ". Expected "!".
      E: line 4: "newline" ends with "". Expected "\n".
```

Based on `*.properties`
[file format docs](https://docs.oracle.com/cd/E23095_01/Platform.93/ATGProgGuide/html/s0204propertiesfileformat01.html).

## Checks ##

The main purpose of `prop-tool` is to ensure all property files are correct and that translation files are in sync with the
reference file. For that reason you need to have at least two `*.properties` files to use `prop-tool`. One is your base language
(usually English texts) used as reference and all the others are your translations. `prop-tool` performs several checks on both
base (reference) file and each translation.

For base file it executes following validators:

* Syntax validation: ensures use of allowed comment markers, key - value separators etc.
* Trailing white characters: no trailing spaces nor tabs at the end of each line,
* WhiteCharsBeforeLinefeed: ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`).

For translation files, the following checks are performed:

* Syntax validation: ensures use of allowed comment markers, key - value separators etc.
* Trailing white characters: no trailing spaces nor tabs at the end of each line.
* Missing translation: keys found in base file, but missing in translation,
* Dangling keys: keys found in translation file but not present in base file,
* Empty translations: empty translations for non-empty text in base file,
* Case check: ensures translation starts with the same character case (upper/lower) as entry in base file,
* Punctuation: ensures translation ends with punctuation mark (`:`, `.`, `?`, `!`) if entry if base file ends that way,
* WhiteCharsBeforeLinefeed: ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`).

NOTE: as this is quite common that translation file may not be updated instantly, `prop-tool` considers key presence condition
fulfilled also when given key exists in `B` file but is commented out and follow expected comment format:

```
# ==> KEY =
```

Default format can changed using `--tpl` argument.

If you want to ensure that all keys are in fact translated, use `--strict` mode while checking. When running with `--strict` option,
keys in commented out form are ignored.

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

## Fixing files ##

You can use `prop-tool` to update your translation files by using `--fix` option. In such case `prop-tool` will completely rewrite
translation files, adding missing keys (in commented out form).

While content of written file is strongly based on base file Some normalization will be made

* There will be no more than one empty consequent empty line written,
* There will be no more than one consequent empty comment line (just comment marker) written.

NOTE: Be aware that `--fix` do NOT update existing translation file but builds it completely using base file as reference and
existing translations (if present). No other content of translation files (for example additional comments etc) will be preserved.

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

---

Check if `es` translation of `gui.properties` is in sync and if there are any missing keys, rewrite translation file to contain all
keys from base:

```bash
prop-tool --base gui --lang es --fix
```

---

Check if `pt` translation of `gui.properties` is in sync and if there are any missing keys, rewrite translation file to contain all
keys from base using own comment format:

```bash
prop-tool --base gui --lang es --fix --tpl "COM >~=-> KEY SEP"
```

## Limitations ##

* As of now `prop-tool` do not handle multiline entries.

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* prop-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
