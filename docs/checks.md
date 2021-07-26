![prop-tool logo](../artwork/prop-tool-logo.png)

# Java *.properties file checker and syncing tool #

## Table of contents ##

* [« Main README](../README.md)
* [« Documentation table of contents](README.md)


* **[Validators](#validators)**
    * [Checking base and translation files](#checking-base-and-translation-files)
* [Available checks](#available-checks)
    * [Syntax check](#syntax-check)
    * [Brackets](#brackets)
    * [DanglingKeys](#dangling-keys)
    * [EmptyTranslations](#empty-translations)
    * [FormattingValues](#formatting-values)
    * [KeyFormat](#key-format)
    * [MissingTranslation](#missing-translation)
    * [Punctuation](#punctuation)
    * [QuotationMarks](#quotation-marks)
    * [StartsWithTheSameCase](#starts-with-the-same-case)
    * [TrailingWhiteChars](#trailing-white-chars)
    * [TypesettingQuotationMarks](#typesetting-quotation-marks)
    * [WhiteCharsBeforeLinefeed](#white-chars-before-linefeed)

---

# Validators #

The main purpose of `prop-tool` is to ensure all property files are correct and that translation files are in sync with the
reference file. For that reason you need to have at least two `*.properties` files to use `prop-tool`. One is your base language
(usually English texts) used as reference and all the others are your translations. `prop-tool` performs several checks on both
base (reference) file and each translation.

## Checking base and translation files ##

Some validators can do their work having just single file to process. In such
case you can use it to check both your base file and translation files. Those
validators that needs base file reference (i.e. [DanglingKeys](#dangling-keys)
can only be used to validate translations.

# Available checks #

## Syntax Check ##

This validators ensures proper structire of the files, use of allowed comment markers, key - value separators etc.

## Brackets ##

Brackets validator ensures all brackets that are found opened in the string are also closed and there's no unpaired bracket left.

## Dangling Keys ##

DanglingKeys validator checks if keys found in translation file are also present in base file.

## Empty Translations ##

EmptyTranslations validator looks for translations that provide no content (empty string) for non-empty text in base file.

## Formatting Values ##

FormattingValues validators looks for commonly used `print()`-alike formatting values syntax, where placeholders like `%s` or `%d`
are replaced with corresponding values at runtime. It assumes that the code expects the same placeholders to be available regardless
of language version therefore it check if all placeholders used in original string are also present in translation string and if the
order of said placeholders is preserved as this is also often crucial for the application to run properly.

## Key Format ##

KeyFormat ensures strings used as keys in you `*.properties` file matches specified pattern which helps keeping unified naming
conventcion across your files.

## Missing Translation ##

MissingTranslation looks texts present in base file that are not provided in the translation.

*NOTE:* as it's pretty often the case that translation files are not always update at the same time base files changes,
`MissingTranslation` is smart enough to accept situation where translation file contains translation key commented (using specified
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

## Punctuation ##

Punctuation check ensures translation ends with punctuation mark (`:`, `.`, `?`, `!`) if entry in base file ends that way.

## Quotation Marks ##

QuotationMarks ensures all quotation marks are unpaired.

Matching quotation marks it tricky because in some languages there's single char that is used as opening and closing quotation
mark (mainly `"`). This makes `QuotationMarks` unable to properly understand the context in case of use of subsequent marks of the
same type, i.e. three `"` in a row: `"""` as it cannot say if 2nd one closes the quotation opened by first one, or maybe first is
closed by third and the 2nd is just missing its closing mark and is misplaced. Therefore for the subsequent marks of the same type
it's always assumed that that there's no quotation nesting. For example, for four `"` in a row `""""`
it is assumed 1st is the opening marker, 2nd closes 1st, and 4th closes the 3rd.

Things also more complicated if you want to mix the quotation marks and use apostrophes too. For example. `"'"'` (double quotes and
apostrophes)
will be marked as incorrect as you open `'` apostrophe marked quote before double quoted is closed. This may be problematic in some
languages that use apostrophes as part of the sentence, i.e. `It's "me"`. This is currently sufficient to fool `QuotationMarks`
as it will complain about not closed apostrophe marked quotation.

Temporary workarounds:

* Try to avoid using apostrophes as quotation marks (change `QuotationMarks` config to not handle it) if you need them in your
  sentences.
* Create `QuotationMarks` configuration per language so i.e. apostrophes are ignored in English, but checked in i.e. Polish which do
  not use it as part of sentences.

## Starts With The Same Case ##

StartsWithTheSameCase ensures translation starts with the same character case (be it upper or lower cased) as string in base string.

*NOTE:* This check makes no sense for languages like Asian (i.e. Chinese, Japanese etc) and you should configure language exception
list for `StartsWithTheSameCase` to make is skip such translations from being checked.

## Trailing White Chars ##

TrailingWhiteChars simply looks at the end of your strings and comments and flags trailing spaces or tab charactes noticed.

## Typesetting Quotation Marks ##

TypesettingQuotationMarks is a mixture of `QuotationMarks` and `Brackets` check that understans quotation mark pairs
(where you have separate quote opening and closing characters). It can look for them and ensure all is paired and properly nested.

*NOTE:* This check usually needs some config tuning because it is not possible to create one universal set of quotation marks
that fits all the languages. The reason is there are the cases where i.e. given character is considered closing quotation mark
in one language and opening marker in another. As `QuotationMarks` does not understand the language it checks it cannot figure
out how to handle such case automatically. The solution is to specify separate pairs for each language you want to support.

## White Chars Before Linefeed ##

`WhiteCharsBeforeLinefeed` ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`)
as this usually serves no purpose.

