# Identifiers

In the Cangjie programming language, developers can assign names to certain program elements, which are referred to as "identifiers."

Before learning about identifiers, it is necessary to understand some concepts related to the Unicode character set. In the Unicode standard, the `XID_Start` and `XID_Continue` properties are used to mark characters that can serve as the starting and subsequent characters of a Unicode identifier, respectively. For detailed definitions, please refer to the [Unicode Standard Documentation](https://www.unicode.org/reports/tr31/tr31-37.html). Among them, `XID_Start` includes characters such as Chinese and English, while `XID_Continue` includes Chinese, English, Arabic numerals, and more. The Cangjie language uses Unicode Standard 15.0.0.

Identifiers in the Cangjie programming language are divided into two categories: regular identifiers and raw identifiers, each following different naming rules.

**Regular identifiers** cannot be the same as Cangjie keywords and are derived from the following two types of character sequences:

- A sequence starting with an `XID_Start` character, followed by any number of `XID_Continue` characters.
- A sequence starting with an `_`, followed by at least one `XID_Continue` character.

Cangjie recognizes all identifiers in their [Normalization Form C (NFC)](https://www.unicode.org/reports/tr15/tr15-53.html) form. Two identifiers are considered the same if they are equal after NFC normalization.

For example, each of the following strings is a valid regular identifier:

```text
abc
_abc
abc_
a1b2c3
a_b_c
a1_b2_c3
Cangjie
__こんにちは
```

Each of the following strings is an invalid regular identifier:

```text
ab&c  // & is not an XID_Continue character
3abc  // Arabic numerals are not XID_Start characters, so they cannot be used as starting characters
_     // An underscore must be followed by at least one XID_Continue character
while // "while" is a Cangjie keyword and cannot be used as a regular identifier
```

**Raw identifiers** are regular identifiers or Cangjie keywords enclosed in a pair of backticks. They are primarily used in scenarios where Cangjie keywords need to be used as identifiers.

For example, each of the following strings is a valid raw identifier:

```text
`abc`
`_abc`
`a1b2c3`
`if`
`while`
`à֮̅̕b`
```

Each of the following strings is an invalid raw identifier because the content inside the backticks is an invalid regular identifier:

```text
`ab&c`
`3abc`
```