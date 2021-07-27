![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

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

`MissingTranslations` looks texts present in base file that are not provided in the translation.

*NOTE:* as it's pretty often the case that translation files are not always update at the same time base files changes,
`MissingTranslations` is smart enough to accept situation where translation file contains translation key commented (using specified
string format) out but not the translation itself. This is sufficient for the translator to catch up and indicates that translation
file was updated once base file changed. For example, given this `base.properties`:

```ini
someKey = Hello
newlyAddedKey = I'm new here!
```

and following translation file: `base_xx.properties`

```ini
someKey = Hello
# ==> newlyAddedKey =
```

the `newlyAddedKey` will be considered "present" in translation, despite being commented out. If you want to ensure there are all
translated, you need to use `--strict` mode instead of default loose check mode.

Default format can be changed using `--template` argument or `template` config entry.

## Configuration file ##

No dedicated configuration.
