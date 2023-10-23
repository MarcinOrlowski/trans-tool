![trans-tool logo](../../artwork/trans-tool-logo.png)

### The translation files checker and syncing tool ###

---

# Brackets #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Brackets**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `Brackets`
* Checks base file: YES
* Checks translations: YES

## Description ##

`Brackets` ensures all brackets found opened in the string are also closed, and there's no
unpaired bracket left. When the `ignore_quoted` option is enabled and a bracket is directly wrapped
in one of the quotation marks specified in the `quotation_marks` config list, then such bracket will
be ignored. Note that bracket matching currently requires both opening and closing brackets to be
the same, as well as the bracket to be directly wrapped in quotes as a sole character:

```text
This is ["[" fine].
This is ']' fine too.
```

These will not be skipped:

```text
Mixed "[' quotes will not work.
No quests "[[" allowed.
```

As kind of special case, this will pass:

```text
These will not skipped but will pass "[]" because brackets are paired.
```

## Configuration file ##

| Key               | Type            | Description                                                                     | Defaults            |
|-------------------|-----------------|---------------------------------------------------------------------------------|---------------------|
| `comments`        | Boolean         | If `true` will scan translations and comments, when `false` will skip comments. | `false`             |
| `ignore_quoted`   | Boolean         | When `true`, any quoted bracket will be ignored.                                | `true`              |
| `quotation_marks` | List of strings | List of accepted quotation marks that `ignore_quoted` looks for.                | `[ "\"", "'" ]`     |
| `opening`         | List of strings | List of opening brackets                                                        | `[ "(", "{", "[" ]` |
| `closing`         | List of strings | List of closing brackets                                                        | `[ ")", "}", "]" ]` |

### Notes ###

**IMPORTANT:** Opening and closing brackets from the same pair MUST be in the same position (i.e.,
if the first element of the `opening` list is `{`, then `}` MUST be the first element in
the `closing` list).

### Example ###

```ini
[trans-tool]
version = 1

[Brackets]
comments = true
ignore_quoted = true
quotation_marks = [ "\"", "'" ]
opening = [ "(", "<", "{" ]
closing = [ ")", ">", "}" ]
```
