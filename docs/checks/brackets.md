![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

# Brackets #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Brackets**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `Brackets`
* Checks base file: YES
* Checks translations: YES

## Description ##

`Brackets` ensures all brackets that are found opened in the string are also closed and there's no unpaired bracket left.

## Configuration file ##

| Key      | Type      | Description | Defaults |
|----------|-----------|-------------|----------|
| comments | Boolean         | If `true` will scan translations and comments, when `false` will skip comments. | `false` |
| opening  | List of strings | List of opening brackets  | `[ "(", "{", "[" ]` |
| closing  | List of strings | List of closing brackets  | `[ ")", "}", "]" ]` |

### Notes ###

**IMPORTANT:** Opening and closing brackets from the same pair MUST be on the same position (i.e. if first element of `opening` list
is `{` then the `}` MUST be first element on `closing` list.

### Example ###

```ini
[prop-tool]
version = 1

[Brackets]
comments = true
opening = [ "(", "<", "{" ]
closing = [ ")", ">", "}" ]
```
