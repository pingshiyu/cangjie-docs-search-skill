# Pattern Overview

For `match` expressions containing matching values, the patterns supported after `case` determine the expressive power of the `match` expression. This section introduces the patterns supported by Cangjie in sequence, including: constant patterns, wildcard patterns, binding patterns, tuple patterns, type patterns, and enum patterns.

## Constant Pattern

A constant pattern can be an integer literal, floating-point literal, character literal, boolean literal, string literal (string interpolation is not supported), or Unit literal.

When using a constant pattern in a `match` expression containing matching values (refer to [match expression](./match.md)), the type of the value represented by the constant pattern must be the same as the type of the value to be matched. The matching succeeds if the value to be matched is equal to the value represented by the constant pattern.

In the following example, based on the value of `score` (assuming `score` can only take values between `0` and `100` divisible by `10`), the grade of the exam score is output:

<!-- verify -->

```cangjie
main() {
    let score = 90
    let level = match (score) {
        case 0 | 10 | 20 | 30 | 40 | 50 => "D"
        case 60 => "C"
        case 70 | 80 => "B"
        case 90 | 100 => "A" // Matched.
        case _ => "Not a valid score"
    }
    println(level)
}
```

Compiling and executing the above code outputs:

```text
A
```

- When the target of pattern matching is a value with static type `Rune`, both `Rune` literals and single-character string literals can be used to represent constant patterns of `Rune` type literals.

  <!-- verify -->

  ```cangjie
  func translate(n: Rune) {
      match (n) {
          case "A" => 1
          case "B" => 2
          case "C" => 3
          case _ => -1
      }
  }

  main() {
      println(translate(r"C"))
  }
  ```

  Compiling and executing the above code outputs:

  ```text
  3
  ```

- When the target of pattern matching is a value with static type `Byte`, a string literal representing an ASCII character can be used to represent constant patterns of `Byte` type literals.

  <!-- verify -->

  ```cangjie
  func translate(n: Byte) {
      match (n) {
          case "1" => 1
          case "2" => 2
          case "3" => 3
          case _ => -1
      }
  }

  main() {
      println(translate(51)) // UInt32(r'3') == 51
  }
  ```

  Compiling and executing the above code outputs:

  ```text
  3
  ```

## Wildcard Pattern

The wildcard pattern is represented by an underscore `_` and can match any value. The wildcard pattern is typically used as the pattern in the last `case` to cover situations not matched by other `cases`. For example, in the [constant pattern](./pattern_overview.md#constant-pattern) example matching `score` values, the last `case` uses `_` to match invalid `score` values.

## Binding Pattern

The binding pattern is represented by `id`, where `id` is a valid identifier. Compared to the wildcard pattern, the binding pattern can also match any value, but it binds the matched value to `id`, allowing access to the bound value via `id` after `=>`.

In the following example, the last `case` uses a binding pattern. Here, the variable `n` is an `id` identifier used to bind non-`0` values:

<!-- verify -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => "x is not zero and x = ${n}" // Matched.
    }
    println(y)
}
```

Compiling and executing the above code outputs:

```text
x is not zero and x = -10
```

When using `|` to connect multiple patterns, binding patterns cannot be used, nor can they be nested within other patterns, otherwise an error will occur:

<!-- compile.error -->

```cangjie
main() {
    let opt = Some(0)
    match (opt) {
        case x | x => {} // Error, variable cannot be introduced in patterns connected by '|'
        case Some(x) | Some(x) => {} // Error, variable cannot be introduced in patterns connected by '|'
        case x: Int64 | x: String => {} // Error, variable cannot be introduced in patterns connected by '|'
    }
}
```

The binding pattern `id` is equivalent to defining a new immutable variable named `id` (its scope starts from the introduction point to the end of the `case`), so `id` cannot be modified after `=>`. For example, modifying `n` in the last `case` of the following example is not allowed.

<!-- compile.error -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => n = n + 0 // Error, 'n' cannot be modified.
                  "x is not zero"
    }
    println(y)
}
```

For each `case` branch, the variable scope level after `=>` is the same as the variable scope level introduced before `=>` in the `case`. Introducing the same name again after `=>` will trigger a redefinition error. For example:

<!-- compile.error -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => let n = 0 // Error, redefinition
                  println(n)
                  "x is not zero"
    }
    println(y)
}
```

> **Note:**
>
> When the identifier of a pattern is an enum constructor, the pattern will be treated as an enum pattern for matching, not a binding pattern (for details on enum patterns, see the [enum pattern](#enum-pattern) section).

<!-- verify -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let x = Red
    let y = match (x) {
        case Red => "red" // The 'Red' is enum mode here.
        case _ => "not red"
    }
    println(y)
}
```

Compiling and executing the above code outputs:

```text
red
```

## Tuple Pattern

The tuple pattern is used to match tuple values. Its definition is similar to tuple literals: `(p_1, p_2, ..., p_n)`, where `p_1` to `p_n` (`n` ≥ `2`) are patterns (which can be any pattern introduced in this section, with multiple patterns separated by commas) rather than expressions.

For example, `(1, 2, 3)` is a tuple pattern containing three constant patterns, and `(x, y, _)` is a tuple pattern containing two binding patterns and one wildcard pattern.

Given a tuple value `tv` and a tuple pattern `tp`, `tp` matches `tv` if and only if each position value in `tv` matches the corresponding position pattern in `tp`. For example, `(1, 2, 3)` can only match the tuple value `(1, 2, 3)`, while `(x, y, _)` can match any triple tuple value.

The following example demonstrates the use of tuple patterns:

<!-- verify -->

```cangjie
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old" // Matched, "Alice" is a constant pattern, and 'age' is a variable pattern.
        case (name, 100) => "${name} is 100 years old"
        case (_, _) => "someone"
    }
    println(s)
}
```

Compiling and executing the above code outputs:

```text
Alice is 24 years old
```

The same tuple pattern cannot introduce multiple binding patterns with the same name. For example, `case (x, x)` in the last `case` of the following example is invalid.

<!-- compile.error -->

```cangjie
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old"
        case (name, 100) => "${name} is 100 years old"
        case (x, x) => "someone" // Error, Cannot introduce a variable pattern with the same name, which will be a redefinition error.
    }
    println(s)
}
```

## Type Pattern

The type pattern is used to determine whether the runtime type of a value is a subtype of a certain type. There are two forms of type patterns: `_: Type` (nesting a wildcard pattern `_`) and `id: Type` (nesting a binding pattern `id`). The difference is that the latter performs variable binding, while the former does not.

For a value `v` to be matched and a type pattern `id: Type` (or `_: Type`), first determine whether the runtime type of `v` is a subtype of `Type`. If true, the match is successful; otherwise, it fails. If the match succeeds, the type of `v` is converted to `Type` and bound to `id` (for `_: Type`, there is no binding operation).

Assume the following two classes, `Base` and `Derived`, where `Derived` is a subclass of `Base`. The parameterless constructor of `Base` sets the value of `a` to `10`, and the parameterless constructor of `Derived` sets the value of `a` to `20`:

<!-- verify -mergeCase -->

```cangjie
open class Base {
    var a: Int64
    public init() {
        a = 10
    }
}

class Derived <: Base {
    public init() {
        a = 20
    }
}
```

The following code demonstrates a successful type pattern match:

<!-- verify -mergeCase -->

```cangjie
func test1() {
    var d = Derived()
    var r = match (d) {
        case b: Base => b.a // Matched.
        case _ => 0
    }
    println("r = ${r}")
}
```

The following code demonstrates a failed type pattern match:

<!-- verify -mergeCase -->

```cangjie
func test2() {
    var b = Base()
    var r = match (b) {
        case d: Derived => d.a  // Type pattern match failed.
        case _ => 0             // Matched.
    }
    println("r = ${r}")
}
```

<!-- verify -mergeCase -->

```cangjie
main() {
    test1()
    test2()
}
```

Compiling and executing the above code yields the following output (the first line is the output of test1, and the second line is the output of test2):

<!-- verify -mergeCase -->

```text
r = 20
r = 0
```

## Enum Pattern

The enum pattern is used to match instances of `enum` types. Its definition resembles the constructor of an `enum`: a no-argument constructor `C` or a parameterized constructor `C(p_1, p_2, ..., p_n)`. The type prefix of the constructor can be omitted. The difference lies in the fact that `p_1` to `p_n` (where `n` ≥ 1) here are patterns. For example, `Some(1)` is an enum pattern containing a constant pattern, while `Some(x)` is an enum pattern containing a binding pattern.

Given an enum instance `ev` and an enum pattern `ep`, `ep` is said to match `ev` if and only if the constructor name of `ev` is the same as that of `ep`, and each value in the parameter list of `ev` matches the corresponding pattern in `ep`. For example, `Some("one")` can only match the `Some` constructor of type `Option<String>`, i.e., `Option<String>.Some("one")`, while `Some(x)` can match any `Some` constructor of the `Option` type.

In the following example, the use of an enum pattern is demonstrated. Since the constructor of `x` is `Year`, it will match the first `case`:

<!-- verify -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(n) => "x has ${n * 12} months" // Matched.
        case TimeUnit.Month(n) => "x has ${n} months"
    }
    println(s)
}
```

Compiling and executing the above code yields the following output:

```text
x has 24 months
```

When multiple enum patterns are connected using `|`, each pattern must be independent and cannot introduce new variables. This is because `|` represents an "or" relationship, and variable introduction requires explicit context, which cannot be shared across multiple patterns. The following example demonstrates a counterexample where the fifth and sixth `case` statements violate this rule:

<!-- compile.error -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(5) => "1:OK"
        case Month(m) => "2:OK"
        case Year(0) | Year(1) | Month(_) => "3:OK"
        case Year(_) => "4:OK"
        case Year(2) | Month(m) => "5:invalid" // Error, Variable cannot be introduced in patterns connected by '|'
        case Year(n: UInt64) | Month(n: UInt64) => "6:invalid" // Error, Variable cannot be introduced in patterns connected by '|'
    }
    println(s)
}
```

In the above example, the second `case` introduces a new variable `m` but does not connect it with other patterns using `|`, making it valid.

When using a `match` expression to match `enum` values, the patterns following `case` must cover all constructors of the `enum` type being matched. If not fully covered, the compiler will report an error:

<!-- compile.error -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let c = Green
    let cs = match (c) { // Error, Not all constructors of RGBColor are covered.
        case Red => "Red"
        case Green => "Green"
    }
    println(cs)
}
```

Full coverage can be achieved by adding `case Blue` or by using `case _` at the end of the `match` expression to cover cases not handled by other `case` statements, as shown below:

<!-- verify -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let c = Blue
    let cs = match (c) {
        case Red => "Red"
        case Green => "Green"
        case _ => "Other" // Matched.
    }
    println(cs)
}
```

The execution result of the above code is:

```text
Other
```

## Nested Combination of Patterns

Tuple patterns and enum patterns can nest arbitrary patterns. The following code demonstrates the nested combination of different patterns:

<!-- verify -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

enum Command {
    | SetTimeUnit(TimeUnit)
    | GetTimeUnit
    | Quit
}

main() {
    let command = (SetTimeUnit(Year(2022)), SetTimeUnit(Year(2024)))
    match (command) {
        case (SetTimeUnit(Year(year)), _) => println("Set year ${year}")
        case (_, SetTimeUnit(Month(month))) => println("Set month ${month}")
        case _ => ()
    }
}
```

Compiling and executing the above code yields the following output:

```text
Set year 2022
```
