![trans-tool logo](../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Configuration ##

* [« Main README](../README.md)
* [« Documentation table of contents](README.md)
* **Configuration**
  * [Config file](#config-file)
  * [Syntax](#syntax)
  * [Structure](#structure)
    * [The [trans-tool] section](#trans-tool-section)

---

# Config File #

You can drive and control `trans-tool` through the use of a configuration file, which provides
extensive control over application behavior. Almost all options, including validators' settings,
can be configured in the configuration file, aiding, for example, in using `trans-tool` as part
of CI/CD or GitHub Actions.

The configuration file is a plain text file, following
the [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created
using any text editor. Please see the commented [config.ini](../config.ini) for an example
configuration file reference.

You should use standard `UTF-8` encoding for your configuration file.

# Syntax #

The configuration file is separated into sections. Each section begins with a section header placed
on a separate line between square brackets, followed by section-related configuration items. Items
are typically in `key = value` form. All keys are always lower-cased, and for keys containing
multiple words, a single underscore character `_` is used as a separator (i.e., `quotation_marks`).
String values must be enclosed using double quotes `"`. If the double quote character is also part
of your value, it must be escaped (`\"`).

```ini

```ini
[section]
version = 1
```

Value can be a string, numeric value, boolean value (`true` or `false`) or list of elements:

```ini
[example]
numericValue = 1

# This is a comment
stringValue1 = "Quotes are mandatory"
stringValue2 = "If needed, \"escape\" quotes."

thisIsTrue1 = true
thisIsTrue2 = 1
thisIsFalse1 = false
thisIsFalse2 = 0

# All elements can go into one line, comma separated
thisIsList = ["foo", "bar"]

# Each element can live in separate line to.
thisIsListToo = [
                "one",
                two,
                "three",
                ]
```

# Structure #

The presence of the main section `[trans-tool]` in the config file is mandatory. However, with the
exception for the `version` element, all items are optional with application defaults used for
non-specified elements.

If any of the available validators can be configured, all its settings are placed in a separate
section, with the name of the section being the Validator ID as specified in the validator
documentation.

The example config file below disables ANSI colors in program output and enables output verbose
mode. It also configures the [Brackets](checks/brackets.md) validator to only handle a given set
of brackets:

```ini
[trans-tool]
# Version of configuration file format. Currently equals to 1
version = 1

color = false
verbose = true

# Validator section names are case sensitive!
[Brackets]
opening = ["(", "["]
closing = [")", "]"]
```

# trans-tool section #

The following elements are supported in `[trans-tool]` section

| Key         | CLI switch    | Argument type    | Default             | Description                                                             |
|-------------|---------------|------------------|---------------------|-------------------------------------------------------------------------|
| `checks`    | `--checks`    | List of strings  | `[ Brackets, ... ]` | List of Checks IDs to be used for content validation.                   |
| `comment`   | `--comment`   | String           | `#`                 | Character(s) used to denote comment lines in the properties file.       |
| `separator` | `--separator` | String           | `=`                 | Character(s) used to separate keys from values in the properties file.  |
| `quiet`     | `--quiet`     | Boolean          | `false`             | Quiet mode. If enabled, all but fatal errors are muted.                 |
| `verbose`   | `--verbose`   | Boolean          | `false`             | Verbose mode. If enabled shows more information during runtime.         |

## Switches ##

Each option how corresponding two command line switches, turning feature on (`--<OPTION>`)
and turning it off (`--no-<OPTION>`). Only one command line argument can be used at the same time.

| Key     | CLI switches            | Argument type | Default | Description                                                 |
|---------|-------------------------|---------------|---------|-------------------------------------------------------------|
| `fatal` | `--fatal`, `--no-fatal` | Boolean       | `false` | When used all validators' warnings are fatal as errors.     |
| `color` | `--color`/`--no-color`  | Boolean       | `true`  | When `true`, application output will be using ANSI colors.  |
