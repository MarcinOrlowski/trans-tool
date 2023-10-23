![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

# Missing Translations #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Missing Translations**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `MissingTranslations`
* Checks base file: NO
* Checks translations: YES

## Description ##

`MissingTranslations` identifies texts present in the base file that are not provided in the
translation.

*NOTE:* As it's quite common for translation files to not always be updated at the same time
as base files change, `MissingTranslations` is smart enough to accept situations where the
translation file contains a translation key commented out (using the specified string format) but
not the translation itself. This is sufficient for the translator to catch up and indicates that the
translation file was updated once the base file changed. For example, given this `base.properties`:

```ini
someKey = Hello
newlyAddedKey = I'm new here!
```

and the following translation file: `base_xx.properties`

```ini
someKey = Hello
# ==> newlyAddedKey =
```

the `newlyAddedKey` will be considered "present" in the translation, despite being commented out. If
you want to ensure they are all translated, you need to use `--strict` mode instead of the default
loose check mode.

## Configuration file ##

No dedicated configuration.
