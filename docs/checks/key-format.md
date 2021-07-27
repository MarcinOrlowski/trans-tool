![prop-tool logo](../../artwork/prop-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

# Key Format #

* [« Main README](../../README.md)
* [« Documentation table of contents](../README.md)
* [« Available checks](README.md)
  * **Key Format**
    * [Summary](#summary)
    * [Description](#description)
    * [Configuration file](#configuration-file)
      * [Important notes](#notes)
      * [Example](#example)

---

## Summary ##

* Check ID: `KeyFormat`
* Checks base file: YES
* Checks translations: YES

## Description ##

This validator ensures strings used as keys in you `*.properties` file matches specified pattern which helps keeping unified naming
conventcion across your files.

## Configuration file ##

| Key       | Type      | Description | Example |
|-----------|-----------|-------------|---------|
| pattern   | Regular expression (string) | Pattern for that each key must match | `"^[a-z]+[a-zA-Z0-9_.]*[a-zA-Z0-9]+$"` |

### Notes ###

* You can use on-line services like [PyRegEx](http://www.pyregex.com/) to test your regular expression first.
* New to regular expressions? See some tutorials first:
  * [Regex tutorial — A quick cheatsheet by examples](https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285)
  * [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
  * [Python Regular Expression (RegEx) Tutorial](https://pythonexamples.org/python-regular-expression-regex-tutorial/)
  * [Python RegEx](https://www.programiz.com/python-programming/regex)
  * [Python Regular Expressions](https://developers.google.com/edu/python/regular-expressions#repetition-examples)
  * **[Find moar!](https://duckduckgo.com/?q=regular+expression+tutorials)**
  
Note, as regular expression are programming language independent, it's more than
sufficient to follow any tutorial that you find understandable.

### Example ###

```ini
[prop-tool]
version = 1

[KeyFormat]
pattern = "^[a-z]+[a-zA-Z0-9_.]*[a-zA-Z0-9]+$"
```
