![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Quotation Marks ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Quotation Marks**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `QuotationMarks`
* Checks base file: YES
* Checks translations: YES

## Description ##

`QuotationMarks` ensures all quotation marks are unpaired.

Matching quotation marks is tricky because in some languages there's a single character that is used
as both the opening and closing quotation mark (mainly `"`). This makes `QuotationMarks` unable to
properly understand the context in the case of the use of subsequent marks of the same type, i.e.,
three `"` in a row: `"""` as it cannot determine if the 2nd one closes the quotation opened by the
first one, or maybe the first is closed by the third and the 2nd is just missing its closing mark
and is misplaced. Therefore, for the subsequent marks of the same type, it's always assumed that
there's no quotation nesting. For example, for four `"` in a row `""""`, it is assumed the 1st is
the opening marker, the 2nd closes the 1st, and the 4th closes the 3rd.

Things also become more complicated if you want to mix the quotation marks and use apostrophes too.
For example, `"'"'` (double quotes and apostrophes) will be marked as incorrect as you open `'`
apostrophe-marked quote before the double quote is closed. This may be problematic in some languages
that use apostrophes as part of the sentence, i.e., `It's "me"`. This is currently sufficient to
fool `QuotationMarks` as it will complain about the unclosed apostrophe-marked quotation.

Temporary workarounds:

* Try to avoid using apostrophes as quotation marks (change `QuotationMarks` config to not handle
  them) if you need them in your sentences.
* Create a `QuotationMarks` configuration per language so, i.e., apostrophes are ignored in English,
  but checked in, i.e., Polish which does not use them as part of sentences.

## Configuration File ##

| Key        | Type            | Description                                                                       | Defaults          |
|------------|-----------------|-----------------------------------------------------------------------------------|-------------------|
| `comments` | Boolean         | If `true`, will scan translations and comments; when `false`, will skip comments. | `true`            |
| `chars`    | List of strings | List of quotation marks                                                           | ``[ "\"", "`" ]`` |

### Notes ###

**IMPORTANT:** We do NOT support apostrophes, because in some languages, i.e., in English, it can be
used in a sentence: "Dogs' food".

### Example ###

```ini
[trans-tool]
version = 1

[QuotationMarks]
comments = false
# Do NOT use apostrophe character for languages like English
chars = [ "`" ]
```
