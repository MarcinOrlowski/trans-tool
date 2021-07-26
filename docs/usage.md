![prop-tool logo](artwork/prop-tool-logo.png)

# The *.properties file checker and syncing tool #


## Config file and command line arguments ##

You can use `prop-tool` by providing all required parameters directly from command line (see `--help`), or you can create
configuration file and use `--config` option to make `prop-tool` load it and use. Almost all options can be set in configuration
files, which helps, for example using `prop-tool` as part of CI/CD or GitHub Actions.

Configuration file is plain text file, following [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created using
any text editor. Please see commented [config.ini](../config.ini) for example configuration file and all available options.

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

---

## Updating translations ##

You can use `prop-tool` to update your translation files by using `--fix` option. In such case `prop-tool` will completely rewrite
translation files, adding missing keys (in commented out form).

While content of written file is strongly based on base file Some normalization will be made

* There will be no more than one empty consequent empty line written,
* There will be no more than one consequent empty comment line (just comment marker) written.

NOTE: Be aware that `--fix` do NOT update existing translation file but builds it completely using base file as reference and
existing translations (if present). No other content of translation files (for example additional comments etc) will be preserved.
