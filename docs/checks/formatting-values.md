![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

# Formatting Values #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Formatting Values**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `FormattingValues`
* Checks base file: NO
* Checks translations: YES

## Description ##

The `FormattingValues` validator looks for commonly used `print()`-like formatting values syntax,
where placeholders like `%s` or `%d` are replaced with corresponding values at runtime. It assumes
that the code expects the same placeholders to be available regardless of the language version;
therefore, it checks if all placeholders used in the original string are also present in the
translation string and if the order of said placeholders is preserved, as this is often crucial for
the application to run properly.

## Configuration file ##

No dedicated configuration.
