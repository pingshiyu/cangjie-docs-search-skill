# Character Type

The character type is represented using `Rune`, which can represent all characters in the Unicode character set.

## Character Type Literals

Character type literals come in three forms: single characters, escape sequences, and universal characters. A `Rune` literal starts with the character `r`, followed by a character enclosed in either single or double quotes.

**Single character** literals examples:

<!-- compile -->

```cangjie
let a: Rune = r'a'
let b: Rune = r"b"
```

**Escape sequences** are character sequences that reinterpret the following character. An escape sequence starts with the escape symbol `\`, followed by the character to be escaped. Examples:

<!-- compile -->

```cangjie
let slash: Rune = r'\\'
let newLine: Rune = r'\n'
let tab: Rune = r'\t'
```

**Universal characters** start with `\u`, followed by 1 to 8 hexadecimal digits enclosed in curly braces, representing the corresponding Unicode character. Examples:

<!-- verify -->

```cangjie
main() {
    let he: Rune = r'\u{4f60}'
    let llo: Rune = r'\u{597d}'
    print(he)
    print(llo)
}
```

Compiling and executing the above code will output:

```text
你好
```

## Supported Operations for Character Type

Character types support the following operators: relational operators, namely less than (`<`), greater than (`>`), less than or equal to (`<=`), greater than or equal to (`>=`), equal to (`==`), and not equal to (`!=`). These comparisons are based on the Unicode values of the characters.

`Rune` can be converted to `UInt32`, and integer types can be converted to `Rune`. For specific type conversion syntax and rules, please refer to [`Rune` to `UInt32` and Integer Type to `Rune` Conversion](../class_and_interface/typecast.md#rune-到-uint32-和整数类型到-rune-的转换).