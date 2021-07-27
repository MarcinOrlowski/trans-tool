![prop-tool logo](artwork/prop-tool-logo.png)

# The *.properties file checker and syncing tool #

# Config file #

You can drive and control `prop-tool` with use of configuration file, which gives you most control over application behavior. Almost
all options, including validators' settings can be configured in configuration files, which helps for example using `prop-tool` as
part of CI/CD or GitHub Actions.

Configuration file is plain text file, following [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created using
any text editor. Please see commented [config.ini](../config.ini) for example configuration file reference.

You should be using standard `UTF-8` encoding for your configuration file.

## Syntax ##

Configuration file is separated into sections. Each section starts with section header put in separate line between square brackets,
followed by section related configuration items. Items are usally in `key = value` form. All keys are always lower-cased, and for
keys containing multiple words, the single underscore character `_` is used as a separator (i.e. `quotation_marks`). String values
can be quoted using either double quotes `"` or apostrophe `'`. You can use both but types cannot be mixed
(if you open using i.e. `"` you must close using `"` too). Quotes can also be omited, but quotation character is part of your value
then it must be explicitely marked so by either being part of quoted string (i.e. `'` is part of the
value: `key = 'value contains " character'`).

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
stringValue1 = Quotes are not needed
stringValue2 = "But can be used if required"
stringValue3 = 'Single quotes are fine too'
stringValue4 = 'You can "mix quotes" too'
stringValue5 = "As last resort, you can \"escape\" quites"

thisIsTrue1 = true
thisIsTrue2 = 1
thisIsFalse1 = false
thisIsFalse2 = 0

# All elements can go into one line, comma separated
thisIsList = ["foo", "bar"]

# Each element can live in separate line to. (comma) separator is optional in that case
thisIsListToo = [
                "one"
                two
                "three"
                ]
```

# Structure #

Presence of main section `[prop-tool]` in config file is mandatory, however with the exception for `version` element, all items are
optional with application defaults used for non-specified elements.

If any of available validators can be configured, all its settings are placed in separate section, witch name of the section being
Validator ID as specified in validator documentation.

Example config file disables ANSI colors in program output and enables output verbose mode. It also
configures [Brackets](checks/brackets.md)
validator to only handle given set of brackets:

```ini
[prop-tool]
# Version of configuration file format. Currently equals to 1
version = 1

color = false
verbose = true

# Validator section names are case sensitive!
[Brackets]
opening = ["(", "["]
closing = [')', ']']
```

# prop-tool section #

The following elements are supported in `[prop-tool]` section

| Key       | CLI switch    | Argument type | Default | Description |
|-----------|---------------|---------------|---------|-------------|
| comment   | `--comment`   | String        | `#`     | TODO |
| separator | `--separator` | String        | `=`     | TODO |
| log_level | `--log-level` | Integer       | `1`     | Sets log verbosity at specified level. |

Switches. Each option how corresponding two command line switches, turning feature on (`--<OPTION>`)
and turning it off (`--no-<OPTION>`). Only one command line argument can be used at the same time.

| Key       | CLI switches |Argument type      | Default | Description |
|-----------|-----------|-------------|---------|------------|
| fatal   | `--fatal`, `--no-fatal` | Boolean | `false` | When used all validators' warnings are fatal as errors. |
| color   | `--color`/`--no-color` | Boolean | `true` | When `true`, application output will be using ANSI colors.|

## Supported Log verbosity levels ##

| Level | Description |
|-------|-------------|
| `0`   | Quiet mode. All but fatal errors are muted. Equivalent of using `--quiet` switch. |
| `1`   | Normal log level, warning and errors are shown plus some additional information if necessary. |
| `2`   | Verbose mode, shows more information during runtime. Equivalent of using `--verbose` switch. |

