![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Punctuation ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Punctuation**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Example](#example)

---

## Summary ##

* Check ID: `Punctuation`
* Checks base file: NO
* Checks translations: YES

## Description ##

The `Punctuation` check ensures a translation ends with a punctuation mark (`:`, `.`, `?`, `!`) if
the entry in the base file ends that way.

## Configuration file ##

| Key     | Type             | Description                     | Defaults                       |
|---------|------------------|---------------------------------|--------------------------------|
| `chars` | List of strings. | List of punctuation characters. | `[ ".", "?", "!", ":", "\n" ]` |

### Example ###

```ini
[trans-tool]
version = 1

[Punctuation]
chars = [ ".", "?" ]
```
