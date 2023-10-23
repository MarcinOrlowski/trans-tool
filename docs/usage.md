![trans-tool logo](../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

# Usage #

* [« Main README](../README.md)
* [« Documentation table of contents](README.md)
* **Usage**
  * [Config file and command line arguments](#config-file-and-command-line)
  * [Usage examples](#usage-examples)
  * Handling translation files
    * [Create new translation files](#create-new-translation-files)
    * [Updating existing translations](#update-existing-translations)

---

## Config File and Command Line ##

You can use `trans-tool` by providing all required parameters directly from the command line (see
`--help`), or you can create a configuration file and use the `--config` option to have `trans-tool`
load and utilize it. Almost all options can be set in configuration files, which helps, for example,
when using `trans-tool` as part of CI/CD or GitHub Actions.

The configuration file is a plain text file, following the
[INI file format](https://en.wikipedia.org/wiki/INI_file), and can be created using any text editor.
Please see the commented [config.ini](../config.ini) for an example configuration file and all
available options.


> NOTE: when using configuration file and command line arguments, the order of precedence is this:
>
> * default configuration goes first,
> * if config file is given and can be loaded and parsed, then it overrides default configuration,
> * if there's any command but line argument `--config` specified, then it overrides whatever is is
    set in config file.
>
> For example:
>
> * by default, `verbose` option is off,
> * your config file sets `verbose = true`, enabling verbose output,
> * but your invocation is `trans-tool --config config.ini --no-verbose`, therefore `verbose` mode
    is set `OFF`.

---

## Usage examples ##

Check if `de` translation of `test.properties` exists and is in sync:

```bash
trans-tool --base test.properties --lang de
```

You can omit `.properties` suffix in command line argument. NOTE: that file name must
contain `.properties` suffix, otherwise it will not be found:

```bash
trans-tool --base test --lang de
```

it will then look for `test_de.properties` file in the same folder `test.properties` resides and
check it.

---

Check if `de`, `pl` and `fr` translations of `test.properties` and `gui.properties` exist and are in
sync:

```bash
trans-tool --base test gui --lang "de pl fr"
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

If you want to use `trans-tool` as part of your CI/CD pipeline, you may end up with the scenario,
where list of languages to work on is not hardcoded in CI/CD/helper script but read from project
sources. This may also include base language (i.e. `en`) leading to `trans-tool` attempts to
read `*_en.properties` and failing. In such case you may specify languages(s) that shall be skipped,
regardless being specified with `--lang`, i.e.

```bash
trans-tool --base test --lang en,pl,fr --lang-skip en
```

it will then look for and validate following files

```bash
test_pl.properties
test_fr.properties
```

---

### Update Existing Translations ###

You can use `trans-tool` to update your translation files by using the `--update` option. In such
a case, `trans-tool` will completely rewrite the translation files, adding missing keys (in a
commented out form).

While the content of the written file is strongly based on a reference file, some normalization will
be made:

* There will be no more than one consecutive empty line written,
* There will be no more than one consecutive empty comment line (just comment marker) written.

Be aware that `--update` does NOT update the existing translation file, but builds it completely
using the base file as a reference and existing translations (if present). No other content of the
translation files (for example, additional comments, etc.) will be preserved.

This will check if the `es` translation of `gui.properties` is in sync and, if there are any issues,
rewrite the translation file to contain all keys from the base:

```bash
trans-tool --base gui --lang es --update
```

---

### Create New Translation Files ###

The `--update` option only acts if the target translation file exists, and `trans-tool` will abort
with an error if you try to update a non-existing file. However, it's also often required to be able
to create an empty translation file (i.e., to hand it to the translator), and `trans-tool` can
accommodate that too with the use of the `--create` switch.

This will check the `de` translation of `gui.properties`, but if the file does not exist, then it
will create an empty "template" file:

```bash
trans-tool --base gui --lang de --create
```

**NOTE:** You can combine `--create` and `--update` in one invocation.
