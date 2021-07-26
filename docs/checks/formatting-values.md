![prop-tool logo](../../artwork/prop-tool-logo.png)

# Java *.properties file checker and syncing tool #

## Formatting Values ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)


* [« Available checks](README.md)
  * **Formatting Values**
    * [Summary](#summary)
    * [Description](#description)
    * [Command line options](#command-line-options)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `FormattingValues`
* Checks base file: NO
* Checks translations: YES

## Description ##

The `FormattingValues` validators looks for commonly used `print()`-alike formatting values syntax, where placeholders like `%s` or `%d`
are replaced with corresponding values at runtime. It assumes that the code expects the same placeholders to be available regardless
of language version therefore it check if all placeholders used in original string are also present in translation string and if the
order of said placeholders is preserved as this is also often crucial for the application to run properly.

## Command line options ##

No dedicated command line options for this validator.

## Configuration file ##

TODO
