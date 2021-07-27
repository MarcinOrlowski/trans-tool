![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

## Quotation Marks ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)


* [« Available checks](README.md)
  * **Quotation Marks**
    * [Summary](#summary)
    * [Description](#description)
    * [Command line options](#command-line-options)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `QuotationMarks`
* Checks base file: YES
* Checks translations: YES

## Description ##

QuotationMarks ensures all quotation marks are unpaired.

Matching quotation marks it tricky because in some languages there's single char that is used as opening and closing quotation
mark (mainly `"`). This makes `QuotationMarks` unable to properly understand the context in case of use of subsequent marks of the
same type, i.e. three `"` in a row: `"""` as it cannot say if 2nd one closes the quotation opened by first one, or maybe first is
closed by third and the 2nd is just missing its closing mark and is misplaced. Therefore for the subsequent marks of the same type
it's always assumed that that there's no quotation nesting. For example, for four `"` in a row `""""`
it is assumed 1st is the opening marker, 2nd closes 1st, and 4th closes the 3rd.

Things also more complicated if you want to mix the quotation marks and use apostrophes too. For example. `"'"'` (double quotes and
apostrophes) will be marked as incorrect as you open `'` apostrophe marked quote before double quoted is closed. This may be
problematic in some languages that use apostrophes as part of the sentence, i.e. `It's "me"`. This is currently sufficient to
fool `QuotationMarks` as it will complain about not closed apostrophe marked quotation.

Temporary workarounds:

* Try to avoid using apostrophes as quotation marks (change `QuotationMarks` config to not handle it) if you need them in your
  sentences.
* Create `QuotationMarks` configuration per language so i.e. apostrophes are ignored in English, but checked in i.e. Polish which do
  not use it as part of sentences.

## Command line options ##

No dedicated command line options for this validator.

## Configuration file ##

| Key       | Type      | Description | Example |
|-----------|-----------|-------------|---------|
| chars   | List of strings | List of quotation marks | `[ '"', "`" ]` |

### Notes ###

**IMPORTANT:** we do NOT support apostrophes, because some languages, i. e. in English it can be used in sentence: "Dogs' food".

### Example ###

```ini
[prop-tool]
version = 1

[QuotationMarks]
# Do NOT use apostrophe character for languages like English
chars = [ "`", '"' ]
```
