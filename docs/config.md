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
keys containing multiple words, the single underscore character `_` is used as a separator (i.e. `quotation_marks`).

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

# Sections #

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
