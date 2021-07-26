# Changelog #

* dev
  * Added support for config files

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