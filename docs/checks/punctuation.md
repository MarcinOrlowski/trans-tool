![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

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

Punctuation check ensures translation ends with punctuation mark (`:`, `.`, `?`, `!`) if entry in base file ends that way.

## Configuration file ##

| Key      | Type      | Description | Defaults |
|----------|-----------|-------------|----------|
| chars    | List of strings | List of punctuation characters | `[ ".", "?", "!", ":", "\n" ]` |

### Example ###

```ini
[prop-tool]
version = 1

[Punctuation]
chars = [ ".", "?" ]
```
