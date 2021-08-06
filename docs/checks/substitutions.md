![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

# Substitutions #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Substitutions**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `Substitutions`
* Checks base file: YES
* Checks translations: YES

## Description ##

`Substitutions` looks for sequence of characters that can be replaced, i.e. subsequent three dots `...` can be replaced
by single ellipsis `…` character. The check also looks for faulty sequences (i.e. it will report an error if more
than 3 dots are put in sequence.

## Configuration file ##

No dedicated configuration.
