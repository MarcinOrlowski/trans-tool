![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Typesetting Quotation Marks ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Typesetting Quotation Marks**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `TypesettingQuotationMarks`
* Checks base file: YES
* Checks translations: YES

## Description ##

`TypesettingQuotationMarks` is a mixture of `QuotationMarks` and `Brackets` check that understands
quotation mark pairs (where you have separate quote opening and closing characters). It can look for
them and ensure all is paired and properly nested.

## Configuration file ##

| Key        | Type            | Description                                                                           | Defaults                         |
|------------|-----------------|---------------------------------------------------------------------------------------|----------------------------------|
| `comments` | Boolean         | If `true`, will scan translations and comments too; when `false`, will skip comments. | `false`                          |
| `opening`  | List of strings | List of opening brackets                                                              | ``[ "‘", "«", "„", "「", "《" ]``  |
| `closing`  | List of strings | List of closing brackets                                                              | ``[ "’", "»", "\“", "」", "》" ]`` |

### Notes ###

*IMPORTANT:* This check usually needs some config tuning because it is not possible to create one
universal set of quotation marks that fits all languages. The reason is there are cases where, for
instance, a given character is considered a closing quotation mark in one language and an opening
marker in another. As `QuotationMarks` does not understand the language it checks, it cannot figure
out how to handle such cases automatically. The solution is to specify separate pairs for each
language you want to support.

### Example ###

```ini
[trans-tool]
version = 1

[TypesettingQuotationMarks]
comments = true
opening = ['‘', '«', '„', '「', '《']
closing = ['’', '»', '“', '」', '》']
```
