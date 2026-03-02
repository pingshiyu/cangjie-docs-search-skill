# Operators

The following table lists all operators supported by Cangjie, along with their precedence and associativity. In the precedence column, a smaller numerical value indicates higher operator precedence.

| Operator                     | Precedence | Meaning               | Example                                                      | Associativity |
|:----------------------------|:----------|:---------------------|:------------------------------------------------------------|--------------|
| `@`                         | 0         | Macro invocation     | `@id`                                                       | Right        |
| `.`                         | 1         | Member access        | `expr.id`                                                   | Left         |
| `[]`                        | 1         | Indexing             | `expr[expr]`                                                | Left         |
| `()`                        | 1         | Function call        | `expr(expr)`                                                | Left         |
| `++`                        | 2         | Increment            | `var++`                                                     | None         |
| `--`                        | 2         | Decrement            | `var--`                                                     | None         |
| `?`                         | 2         | Question mark        | `expr?.id`, `expr?[expr]`, `expr?(expr)`, `expr?{expr}`     | None         |
| `!`                         | 3         | Bitwise NOT, Logical NOT | `!expr`                                                   | Right        |
| `-`                         | 3         | Unary minus          | `-expr`                                                     | Right        |
| `**`                        | 4         | Exponentiation       | `expr ** expr`                                              | Right        |
| `*`, `/`                    | 5         | Multiplication, Division | `expr * expr`,  `expr / expr`                           | Left         |
| `%`                         | 5         | Modulo               | `expr % expr`                                               | Left         |
| `+`, `-`                    | 6         | Addition, Subtraction | `expr + expr`,  `expr - expr`                           | Left         |
| `<<`                        | 7         | Bitwise left shift   | `expr << expr`                                              | Left         |
| `>>`                        | 7         | Bitwise right shift  | `expr >> expr`                                              | Left         |
| `..`                        | 8         | Left-closed right-open range | `expr..expr`                                      | None         |
| `..=`                       | 8         | Closed range         | `expr..=expr`                                               | None         |
| `<`                         | 9         | Less than            | `expr < expr`                                               | None         |
| `<=`                        | 9         | Less than or equal   | `expr <= expr`                                              | None         |
| `>`                         | 9         | Greater than         | `expr > expr`                                               | None         |
| `>=`                        | 9         | Greater than or equal | `expr >= expr`                                             | None         |
| `is`                        | 9         | Type check           | `expr is Type`                                              | None         |
| `as`                        | 9         | Type conversion      | `expr as Type`                                              | None         |
| `==`                        | 10        | Equality             | `expr == expr`                                              | None         |
| `!=`                        | 10        | Inequality           | `expr != expr`                                              | None         |
| `&`                         | 11        | Bitwise AND          | `expr & expr`                                               | Left         |
| `^`                         | 12        | Bitwise XOR          | `expr ^ expr`                                               | Left         |
| <code>&vert;</code>         | 13        | Bitwise OR           | <code>expr &vert; expr</code>                               | Left         |
| `&&`                        | 14        | Logical AND          | `expr && expr`                                              | Left         |
| <code>&vert;&vert;</code>   | 15        | Logical OR           | <code>expr  &vert;&vert; expr</code>                       | Left         |
| `??`                        | 16        | Coalescing operator  | `expr ?? expr`                                              | Right        |
| <code>&vert;></code>        | 17        | Pipeline operator    | <code>id &vert;> expr</code>                                | Left         |
| `~>`                        | 17        | Composition operator | `expr ~> expr`                                              | Left         |
| `=`                         | 18        | Assignment           | `id = expr`                                                 | None         |
| `**=`                       | 18        | Compound operator    | `id **= expr`                                               | None         |
| `*=`                        | 18        | Compound operator    | `id *= expr`                                                | None         |
| `/=`                        | 18        | Compound operator    | `id /= expr`                                                | None         |
| `%=`                        | 18        | Compound operator    | `id %= expr`                                                | None         |
| `+=`                        | 18        | Compound operator    | `id += expr`                                                | None         |
| `-=`                        | 18        | Compound operator    | `id -= expr`                                                | None         |
| `<<=`                       | 18        | Compound operator    | `id <<= expr`                                               | None         |
| `>>=`                       | 18        | Compound operator    | `id >>= expr`                                               | None         |
| `&=`                        | 18        | Compound operator    | `id &= expr`                                                | None         |
| `^=`                        | 18        | Compound operator    | `id ^= expr`                                                | None         |
| <code>&vert;=</code>        | 18        | Compound operator    | <code>id &vert;= expr</code>                               | None         |
| `&&=`                       | 18        | Compound operator    | `id &&= expr`                                               | None         |
| <code>&vert;&vert;=</code>  | 18        | Compound operator    | <code>id &vert;&vert;= expr</code>                         | None         |