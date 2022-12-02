![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Table of contents ##

* [« Main README](../../README.md)
* [« Documentation table of contents](README.md)
* **[Validators](#validators)**
  * [Checking base and translation files](#checking-base-and-translation-files)
* Available checks
  * [Syntax check](syntax-check.md)
  * [Brackets](brackets.md)
  * [DanglingKeys](dangling-keys.md)
  * [EmptyTranslations](empty-translations.md)
  * [FormattingValues](formatting-values.md)
  * [KeyFormat](key-format.md)
  * [MissingTranslations](missing-translations.md)
  * [Punctuation](punctuation.md)
  * [QuotationMarks](quotation-marks.md)
  * [StartsWithTheSameCase](starts-with-the-same-case.md)
  * [Substitutions](substitutions.md)
  * [TrailingWhiteChars](trailing-white-chars.md)
  * [TypesettingQuotationMarks](typesetting-quotation-marks.md)
  * [WhiteCharsBeforeLinefeed](white-chars-before-linefeed.md)

---

# Validators #

The main purpose of `trans-tool` is to ensure all property files are correct and that translation
files are in sync with the reference file. For that reason you need to have at least
two `*.properties` files to use `trans-tool`. One is your base language (usually English texts) used
as reference and all the others are your translations. `trans-tool` performs several checks on both
base (reference) file and each translation.

## Checking base and translation files ##

Some validators can do their work having just single file to process. In such case you can use it to
check both your base file and translation files. Those validators that needs base file reference
(i.e. [DanglingKeys](dangling-keys.md) can only be used to validate translations.
