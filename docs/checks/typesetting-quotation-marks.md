![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

## Typesetting Quotation Marks ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Typesetting Quotation Marks**
    * [Summary](#summary)
    * [Description](#description)
    * [Command line options](#command-line-options)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `TypesettingQuotationMarks`
* Checks base file: YES
* Checks translations: YES

## Description ##

TypesettingQuotationMarks is a mixture of `QuotationMarks` and `Brackets` check that understans quotation mark pairs
(where you have separate quote opening and closing characters). It can look for them and ensure all is paired and properly nested.

## Command line options ##

No dedicated command line options for this validator.

## Configuration file ##

| Key       | Type      | Description | Example |
|-----------|-----------|-------------|---------|
| opening   | List of strings | List of opening brackets | `[ '‘', '«' ]` |
| closing   | List of strings | List of closing brackets | `[ '’', '»' ]` |

### Notes ###

*IMPORTANT:* This check usually needs some config tuning because it is not possible to create one universal set of quotation marks
that fits all the languages. The reason is there are the cases where i.e. given character is considered closing quotation mark
in one language and opening marker in another. As `QuotationMarks` does not understand the language it checks it cannot figure
out how to handle such case automatically. The solution is to specify separate pairs for each language you want to support.

### Example ###

```ini
[prop-tool]
version = 1

[TypesettingQuotationMarks]
opening = ['‘', '«', '„', '「', '《']
closing = ['’', '»', '“', '」', '》']
```
