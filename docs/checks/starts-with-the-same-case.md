![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

## Starts With The Same Case ##

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Starts With The Same Case**
    * [Summary](#summary)
    * [Description](#description)
    * [Important notes](#notes)
    * [Configuration file](#configuration-file)

---

## Summary ##

* Check ID: `StartsWithTheSameCase`
* Checks base file: NO
* Checks translations: YES

## Description ##

`StartsWithTheSameCase` ensures first word found in translation starts with the same character
case (be it upper or lower cased) as first word found in base string. Please note that the checkers
looks for words to match first, skipping character sequences that do not start with alphabetic
character. For example, having base string:

```ini
key = Llorem ipsum: %s
```

and translation:

```ini
key = %s 123 foo bar
```

The words used for checking will be `Llorem` and `foo` respectively.

`StartsWithTheSameCase` can also handle the case where either the base string or translation starts
with a digit, which in some cases, depending on the languages used, can qualify as a matching
translation since digits at the front are language-driven. For example, the original message
says `No support for 64-bit words.` while the translation can be more
like `64-bit words are not supported.` These are both equivalent, but the other form can be actually
a better choice for the target language. In such a case, matching `No` from the base with `words`
from the translation ends up with a "false positive". To support this, the `accept_digits` flag is
provided and when its value is `true` (default), then a sentence starting with a digit matches any
case of the other language sentence.

### Notes ###

*NOTE:* This check most likely makes no sense for languages like Asian (i.e., Chinese, Japanese,
etc.) and you should configure a language exception list for `StartsWithTheSameCase` to make it skip
such translations from being checked.

## Configuration file ##

| Key             | Type    | Description                                                                     | Defaults |
|-----------------|---------|---------------------------------------------------------------------------------|----------|
| `accept_digits` | Boolean | If `true` sentence starting with a digit matches any case of the other string.  | `true`   |
