# Match Expressions

## Definition of Match Expressions

Cangjie supports two types of `match` expressions: the first is a `match` expression containing a value to be matched, and the second is a `match` expression without a value to be matched.

**Match Expression with Matching Value**:

<!-- verify -->

```cangjie
main() {
    let x = 0
    match (x) {
        case 1 => let r1 = "x = 1"
                  print(r1)
        case 0 => let r2 = "x = 0" // Matched.
                  print(r2)
        case _ => let r3 = "x != 1 and x != 0"
                  print(r3)
    }
}
```

The `match` expression starts with the keyword `match`, followed by the value to be matched, such as `x` in the example above. `x` can be any expression. This is followed by several `case` branches enclosed in curly braces. Each `case` branch starts with the keyword `case`, followed by a pattern or multiple patterns of the same kind connected by `|`. In the example above, `1`, `0`, and `_` are all patterns. For details, see the [Pattern Overview](../enum_and_pattern_match/pattern_overview.md) chapter. After the pattern comes `=>`, followed by the operation to be executed when the `case` branch matches successfully. This can be a series of expressions, variable definitions, or function definitions. The scope of newly defined variables or functions starts from their definition point and ends before the next `case`. For example, the variable definitions and `print` function calls in the example above.

In the example above, since the value of `x` is equal to `0`, it matches the second `case` branch (here, a constant pattern is used, which matches whether the values are equal. For details, see the [Constant Pattern](../enum_and_pattern_match/pattern_overview.md#constant-pattern) chapter). Finally, it outputs `x = 0`.

Compile and execute the above code, and the output result is:

```text
x = 0
```

The `match` expression requires that all matches must be exhaustive, meaning all possible values of the expression to be matched should be considered. When the `match` expression is not exhaustive, or the compiler cannot determine whether it is exhaustive, a compilation error will occur. In other words, the union of the value ranges covered by all `case` branches (including pattern guards) should include all possible values of the expression to be matched. A common way to ensure the exhaustiveness of the `match` expression is to use the wildcard pattern `_` in the last `case` branch, as `_` can match any value.

The exhaustiveness of the `match` expression ensures that there must be a `case` branch that matches the value to be matched. The following example will result in a compilation error because not all possible values of `x` are covered by the `case` branches:

<!-- compile.error -->

```cangjie
func nonExhaustive(x: Int64) {
    match (x) {
        case 0 => print("x = 0")
        case 1 => print("x = 1")
        case 2 => print("x = 2")
    }
}
```

If the type of the matched value includes an `enum` type and the `enum` is a `non-exhaustive enum`, then when matching, a pattern that can match all constructors must be used, such as the wildcard pattern `_` or a binding pattern.

<!-- compile -->

```cangjie
enum T {
    | Red | Green | Blue | ...
}
func foo(a: T) {
    match (a) {
        case Red => 0
        case Green => 1
        case Blue => 2
        case _ => -1
    }
}

func bar(a: T) {
    match (a) {
        case Red => 0
        case k => -1 // simple binding pattern
    }
}

func baz(a: T) {
    match (a) {
        case Red => 0
        case k: T => -1 // binding pattern with nested type pattern
    }
}
```

After the pattern in the `case` branch, a `pattern guard` can be used to further judge the matching result. This is optional.

- `pattern guard` represents an additional condition that must be satisfied after the `case` matches successfully. It is expressed using `where cond` (syntax format), requiring the type of the expression `cond` to be `Bool`.

When the `match` expression is executed, the expression after `match` is sequentially matched with each pattern in the `case`. If there is a `pattern guard`, the expression after `where` must evaluate to `true`; if there are multiple patterns in the `case` connected by `|`, as long as the value to be matched matches one of the patterns, it is considered a successful match. Once a match is successful, the code after `=>` is executed, and then the execution of the `match` expression is exited, meaning that subsequent `case` branches will not be matched. If the match is unsuccessful, it will continue to match with the patterns in subsequent `case` branches until a match is successful. The `match` expression guarantees that there must be a `case` branch that matches.

In the following example, an `enum` pattern is used. For details, see the [Enum Pattern](../enum_and_pattern_match/pattern_overview.md#enum-pattern) chapter. When the parameter value of the `RGBColor` constructor is greater than or equal to `0`, their values are output; when the parameter value is less than `0`, meaning the `where cond` of the first `case` is satisfied, their values are considered to be `0`:

<!-- verify -->

```cangjie
enum RGBColor {
    | Red(Int16) | Green(Int16) | Blue(Int16)
}
main() {
    let c = RGBColor.Green(-100)
    let cs = match (c) {
        case Red(r) where r < 0 => "Red = 0"
        case Red(r) => "Red = ${r}"
        case Green(g) where g < 0 => "Green = 0" // Matched.
        case Green(g) => "Green = ${g}"
        case Blue(b) where b < 0 => "Blue = 0"
        case Blue(b) => "Blue = ${b}"
    }
    print(cs)
}
```

Compile and execute the above code, and the output result is:

```text
Green = 0
```

**Match Expression Without Matching Value**:

<!-- verify -->

```cangjie
main() {
    let x = -1
    match {
        case x > 0 => print("x > 0")
        case x < 0 => print("x < 0") // Matched.
        case _ => print("x = 0")
    }
}
```

Compared to the `match` expression with a value to be matched, there is no expression to be matched after the keyword `match`, and what follows `case` is no longer a `pattern`, but an expression of type `Bool` (such as `x > 0` and `x < 0` in the above code) or `_` (representing `true`). Of course, there is no `pattern guard` in the `case` either.

When the `match` expression without a matching value is executed, the expressions after `case` are evaluated in sequence until a `case` branch with an expression value of `true` is encountered. Once the expression value after a `case` equals `true`, the code after `=>` in this `case` is executed, and then the execution of the `match` expression is exited (meaning that subsequent `case` branches will not be evaluated).

In the example above, since the value of `x` is `-1`, the expression in the second `case` branch (i.e., `x < 0`) evaluates to `true`, and `print("x < 0")` is executed.

Compile and execute the above code, and the output result is:

```text
x < 0
```

## Types of Match Expressions

For `match` expressions (whether with or without a matching value):

- When there is a clear type requirement in the context, the type of the code block after `=>` in each `case` branch must be a subtype of the type required by the context;

- When there is no clear type requirement in the context, the type of the `match` expression is the least common parent type of the types of the code blocks after `=>` in each `case` branch;

- When the value of the `match` expression is not used, its type is `Unit`, and there is no requirement for the least common parent type of the types of each branch.

The following examples illustrate these points.

<!-- compile -->

```cangjie
let x = 2
let s: String = match (x) {
    case 0 => "x = 0"
    case 1 => "x = 1"
    case _ => "x != 0 and x != 1" // Matched.
}
```

In the example above, when defining the variable `s`, its type is explicitly annotated as `String`, which is a case where the context type information is clear. Therefore, the type of the code block after `=>` in each `case` must be a subtype of `String`. Clearly, the string literals after `=>` in the example meet this requirement.

Here is another example without context type information:

<!-- compile -->

```cangjie
let x = 2
let s = match (x) {
    case 0 => "x = 0"
    case 1 => "x = 1"
    case _ => "x != 0 and x != 1" // Matched.
}
```

In the example above, when defining the variable `s`, its type is not explicitly annotated. Since the type of the code block after `=>` in each `case` is `String`, the type of the `match` expression is `String`, and thus the type of `s` can be determined to be `String`.