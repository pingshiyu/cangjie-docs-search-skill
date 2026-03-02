# Pattern Refutability

Patterns can be divided into two categories: `refutable` patterns and `irrefutable` patterns. Under the premise of type matching, when a pattern may fail to match the value being matched, it is called a `refutable` pattern; conversely, when a pattern can always match the value being matched, it is called an `irrefutable` pattern.

For the various patterns introduced above, the following rules apply:

Constant patterns are `refutable` patterns. For example, in the following example, both `1` in the first case and `2` in the second case may not equal the value of `x`.

<!-- compile -->

```cangjie
func constPat(x: Int64) {
    match (x) {
        case 1 => "one"
        case 2 => "two"
        case _ => "_"
    }
}
```

Wildcard patterns are `irrefutable` patterns. For example, in the following example, no matter what the value of `x` is, `_` will always match it.

<!-- compile -->

```cangjie
func wildcardPat(x: Int64) {
    match (x) {
        case _ => "_"
    }
}
```

Binding patterns are `irrefutable` patterns. For example, in the following example, no matter what the value of `x` is, the binding pattern `a` will always match it.

<!-- compile -->

```cangjie
func varPat(x: Int64) {
    match (x) {
        case a => "x = ${a}"
    }
}
```

Tuple patterns are `irrefutable` patterns if and only if every pattern they contain is an `irrefutable` pattern. For example, in the following example, both `(1, 2)` and `(a, 2)` may fail to match the value of `x`, so they are `refutable` patterns, whereas `(a, b)` can match any value of `x`, so it is an `irrefutable` pattern.

<!-- compile -->

```cangjie
func tuplePat(x: (Int64, Int64)) {
    match (x) {
        case (1, 2) => "(1, 2)"
        case (a, 2) => "(${a}, 2)"
        case (a, b) => "(${a}, ${b})"
    }
}
```

Type patterns are `refutable` patterns. For example, in the following example (assuming `Base` is the parent class of `Derived`, and `Base` implements the interface `I`), the runtime type of `x` may be neither `Base` nor `Derived`, so both `a: Derived` and `b: Base` are `refutable` patterns.

<!-- compile -->

```cangjie
interface I {}
open class Base <: I {}
class Derived <: Base {}

func typePat(x: I) {
    match (x) {
        case a: Derived => "Derived"
        case b: Base => "Base"
        case _ => "Other"
    }
}
```

Enum patterns are `irrefutable` patterns if and only if the corresponding `enum` type has only one parameterized constructor, and the other patterns contained in the enum pattern are also `irrefutable` patterns. For example, for the definitions of `E1` and `E2` in the following example, `A(1)` in the function `enumPat1` is a `refutable` pattern, while `A(a)` is an `irrefutable` pattern; whereas in the function `enumPat2`, both `B(b)` and `C(c)` are `refutable` patterns.

<!-- compile -->

```cangjie
enum E1 {
    A(Int64)
}

enum E2 {
    B(Int64) | C(Int64)
}

func enumPat1(x: E1) {
    match (x) {
        case A(1) => "A(1)"
        case A(a) => "A(${a})"
    }
}

func enumPat2(x: E2) {
    match (x) {
        case B(b) => "B(${b})"
        case C(c) => "C(${c})"
    }
}
```