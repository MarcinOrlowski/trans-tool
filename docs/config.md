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

# Config file #

You can drive and control `trans-tool` with use of configuration file, which gives you most control over application behavior. Almost
all options, including validators' settings can be configured in configuration files, which helps for example using `trans-tool` as
part of CI/CD or GitHub Actions.

Configuration file is plain text file, following [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created using
any text editor. Please see commented [config.ini](../config.ini) for example configuration file reference.

You should be using standard `UTF-8` encoding for your configuration file.

# Syntax #

Configuration file is separated into sections. Each section starts with section header put in separate line between square brackets,
followed by section related configuration items. Items are usually in `key = value` form. All keys are always lower-cased, and for
keys containing multiple words, the single underscore character `_` is used as a separator (i.e. `quotation_marks`). String values
must be quoted using double quotes `"`. If double quote character is also part of your value, it must be escaped (`\"`).

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

Presence of main section `[trans-tool]` in config file is mandatory, however with the exception for `version` element, all items are
optional with application defaults used for non-specified elements.

If any of available validators can be configured, all its settings are placed in separate section, witch name of the section being
Validator ID as specified in validator documentation.

Example config file disables ANSI colors in program output and enables output verbose mode. It also
configures [Brackets](checks/brackets.md)
validator to only handle given set of brackets:

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

| Key       | CLI switch    | Argument type | Default | Description |
|-----------|---------------|---------------|---------|-------------|
| checks    | `--checks`    | List of strings | `[ Brackets, ... ]` | List of Checks IDs to be used for content validation. |
| comment   | `--comment`   | String        | `#`     | TODO |
| separator | `--separator` | String        | `=`     | TODO |
| quiet     | `--quiet`     | Boolean       | `false` | Quiet mode. If enabled, all but fatal errors are muted. |
| verbose   | `--verbose`   | Boolean       | `false` | Verbose mode. If enabled shows more information during runtime. |

## Switches ##

Each option how corresponding two command line switches, turning feature on (`--<OPTION>`)
and turning it off (`--no-<OPTION>`). Only one command line argument can be used at the same time.

| Key       | CLI switches |Argument type      | Default | Description |
|-----------|-----------|-------------|---------|------------|
| fatal   | `--fatal`, `--no-fatal` | Boolean | `false` | When used all validators' warnings are fatal as errors. |
| color   | `--color`/`--no-color` | Boolean | `true` | When `true`, application output will be using ANSI colors.|
