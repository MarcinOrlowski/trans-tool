![prop-tool logo](../../artwork/prop-tool-logo.png)

# Java *.properties file checker and syncing tool #

## Starts With The Same Case ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)


* [« Available checks](README.md)
  * **Starts With The Same Case**
    * [Summary](#summary)
    * [Description](#description)
    * [Command line options](#command-line-options)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `StartsWithTheSameCase`
* Checks base file: NO
* Checks translations: YES

## Description ##

StartsWithTheSameCase ensures translation starts with the same character case (be it upper or lower cased) as string in base string.

*NOTE:* This check makes no sense for languages like Asian (i.e. Chinese, Japanese etc) and you should configure language exception
list for `StartsWithTheSameCase` to make is skip such translations from being checked.

## Command line options ##

No dedicated command line options for this validator.

## Configuration file ##

TODO
