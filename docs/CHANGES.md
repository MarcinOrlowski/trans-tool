![trans-tool logo](../artwork/trans-tool-logo.png)

### The *.properties file checker and syncing tool ###

---

# Changelog #

* dev
  * Rebranded project as 'trans-tool'.
  * Fixed config loader not handling Checks' sections properly.
  * Corrected config file syntax documentation.
  * Added `--config-dump` option that shows state of the configuration.
  * Corrected default `KeyFormat` pattern.
  * Comment checks by `Brackets` and `TypesettingQuotationMarks` can now be configured.
  * Fixed loader issue causing missing keys to reported twice.
  * Added `--write-reference` option that can include both base and translation in saved file.
  * `StartsWithTheSameCase` now is smarter when looking for words to check.
  * Removed `<` and `>` from `Brackets` defaults as `>` is often used as "arrow" (`->`) raising false positives.
  * Corrected default `KeyFormat` patter so it no longer allows digits at first position.
  * `QuotationMarks`, `TypesettingQuotationMarks`, `WhiteCharsBeforeLinefeed` and `TrailingWhiteChars` now support `comments` config
    item to control whenever you want comments to be scanned.
  * `StartsWithTheSameCase` now handles the case where base/translation can start with a digit which should be case match.
  * `Brackets` can now detect and ignore quoted brackets.

* v2.0.0 (2021-08-02)
  * Added support for config files.
  * Added option to `--create` template translation files.
  * The `--lang` now also supports comma separated arguments.
  * Reworked documentation.
  * Improved `*.properties` file parsing to better handle extreme cases.
  * Added more unit tests.

* v1.3.0 (2021-07-22)
  * Added `TypesettingQuotationMarks` check.
  * Various checkers' code improvements.
  * Added more unit tests.
  * Rephrased some report messages for clarity.

* v1.2.0 (2021-07-21)
  * Reworked report formatting.
  * Added `--fatal` to make warnings fatal as errors.
  * Added `WhiteCharsBeforeLinefeed` check.
  * Added `StartsWithTheSameCase` check.
  * Added `KeyFormat` check.
  * Added `Punctuation` check.
  * Added `EmptyTranslations` check.
  * Added `Brackets` check.
  * Added `QuotationMarks` check.
  * Added `FormattingValues` check.
  * Added unit tests.
  * Added `--version` support.

* v1.1.0 (2021-07-19)
  * String format for commented-out entries can now be configured.
  * Added option to specify comment character.
  * Added option to specify key-value separator character.
  * Missing translation file no longer aborts.
  * Fixed handling `!` as comment line marker.
  * You can use either `prop-tool` or `proptool` as tool name.
  * Reference file is now also checked for common errors.
  * Trailing chars check can also detect missing "\n" literal too.

* v1.0.0 (2021-07-16)
  * Initial public release.
