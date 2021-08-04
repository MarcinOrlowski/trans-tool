![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

## Starts With The Same Case ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Starts With The Same Case**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `StartsWithTheSameCase`
* Checks base file: NO
* Checks translations: YES

## Description ##

`StartsWithTheSameCase` ensures first word found in translation starts with the same character case (be it upper or lower cased) as
first word found in base string. Please note that the checkers looks for words to match first, skipping character sequences that do
not start with aplhabetic character. For example, having base string:

```ini
key = Llorem ipsum: %s
```

and translation:

```ini
key = %s 123 foo bar
```

the words used for checking will be `Llorem` and `foo` respectively.

*NOTE:* This check makes no sense for languages like Asian (i.e. Chinese, Japanese etc) and you should configure language exception
list for `StartsWithTheSameCase` to make is skip such translations from being checked.

## Configuration file ##

No dedicated configuration.
