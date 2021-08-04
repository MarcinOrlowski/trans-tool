![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

## White Chars Before Linefeed ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **White Chars Before Linefeed**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `WhiteCharsBeforeLinefeed`
* Checks base file: YES
* Checks translations: YES

## Description ##

This validator ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`)
as this usually serves no purpose.

## Configuration file ##

| Key      | Type      | Description | Defaults |
|----------|-----------|-------------|----------|
| comments | Boolean   | If `true` will scan translations and comments, when `false` will skip comments. | `false` |

### Example ###

```ini
[prop-tool]
version = 1

[WhiteCharsBeforeLinefeed]
comments = true
```
