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
    * [Command line options](#command-line-options)
    * [Configuration file](#configuration-file)
      * [Example](#example)
  
---

## Summary ##

* Check ID: `Punctuation`
* Checks base file: NO
* Checks translations: YES

## Description ##

Punctuation check ensures translation ends with punctuation mark (`:`, `.`, `?`, `!`) if entry in base file ends that way.

## Command line options ##

No dedicated command line options for this validator.

## Configuration file ##

| Key       | Type      | Description | Example |
|-----------|-----------|-------------|---------|
| chars   | List of strings | List of punctuation characters | `[ ".", "?", "!", ":" ]` |

### Example ###

```ini
[prop-tool]
version = 1

[Punctuation]
chars = [ ".", "?" ]
```

