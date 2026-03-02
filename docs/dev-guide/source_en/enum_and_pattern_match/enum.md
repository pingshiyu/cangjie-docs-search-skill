# Enum Types

This section introduces the `enum` type in Cangjie. The `enum` type provides a way to define a type by enumerating all its possible values.

Many programming languages have `enum` types (or enumerated types), but their usage and expressive power vary across languages. In Cangjie, the `enum` type can be understood as algebraic data types (Algebraic Data Types) in functional programming languages.

## Definition of enum

When defining an `enum`, all its possible values must be explicitly listed. These values are called constructors (or `constructors`) of the `enum`.

An `enum` type definition starts with the keyword `enum`, followed by the name of the `enum`, and then the `enum` body enclosed in curly braces. The `enum` body defines several constructors, separated by `|` (the `|` before the first constructor is optional). Constructors can be named or unnamed (`...`).

Each `enum` must contain at least one named constructor. Named constructors can be parameterless (i.e., "no-argument constructors") or carry several parameters (i.e., "parameterized constructors"). The following example defines an `enum` type named `RGBColor` with three constructors: `Red`, `Green`, and `Blue`, representing the red, green, and blue components in the RGB color model. Each constructor has a `UInt8` parameter representing the brightness level of each color.

<!-- compile -->

```cangjie
enum RGBColor {
    | Red(UInt8) | Green(UInt8) | Blue(UInt8)
}
```

Cangjie supports defining multiple constructors with the same name in the same `enum`, but these constructors must have different numbers of parameters (a parameterless constructor is considered to have 0 parameters). For example:

<!-- compile -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
    | Red(UInt8) | Green(UInt8) | Blue(UInt8)
}
```

Each `enum` can have at most one unnamed `...` constructor, and `...` must be the last constructor. An `enum` with a `...` constructor is called a `non-exhaustive enum`. Since it has no name, this constructor cannot be directly matched. During destructuring, patterns that match all constructors must be used, such as the wildcard pattern `_` or binding patterns. For details, refer to [Definition of match expressions](./match.md#definition-of-match-expressions). For example:

<!-- compile -->

```cangjie
enum T {
    | Red | Green | Blue | ...
}
```

`enum` supports recursive definitions. For example, the following example uses `enum` to define an expression type (`Expr`), which can only have three forms: a single number `Num` (with an `Int64` parameter), an addition expression `Add` (with two `Expr` parameters), or a subtraction expression `Sub` (with two `Expr` parameters). For the `Add` and `Sub` constructors, their parameters recursively reference `Expr` itself.

<!-- compile -->

```cangjie
enum Expr {
    | Num(Int64)
    | Add(Expr, Expr)
    | Sub(Expr, Expr)
}
```

Additionally, the `enum` body can define a series of member functions, operator functions (see [Operator Overloading](../function/operator_overloading.md)), and member properties (see [Properties](../class_and_interface/prop.md)). However, constructors, member functions, and member properties must not share the same name. For example, the following example defines a function named `printType` in `RGBColor`, which outputs the string `RGBColor`:

<!-- compile -->

```cangjie
enum RGBColor {
    | Red | Green | Blue

    public static func printType() {
        print("RGBColor")
    }
}
```

> **Note:**
>
> `enum` can only be defined at the top-level scope of a source file.

## Usage of enum

After defining an `enum` type, you can create instances of this type (i.e., `enum` values). An `enum` value can only take one of the constructors defined in the `enum` type. `enum` does not have constructors; you can create an `enum` value using `TypeName.Constructor` or directly using the constructor (for parameterized constructors, arguments must be provided).

In the following example, `RGBColor` defines three constructors: two parameterless constructors (`Red` and `Green`) and one parameterized constructor (`Blue(UInt8)`). The `main` function defines three `RGBColor` variables `r`, `g`, and `b`. `r` is initialized with `RGBColor.Red`, `g` is initialized directly with `Green`, and `b` is initialized with `Blue(100)`:

<!-- compile -->

```cangjie
enum RGBColor {
    | Red | Green | Blue(UInt8)
}

main() {
    let r = RGBColor.Red
    let g = Green
    let b = Blue(100)
}
```

When the type name is omitted, the name of an `enum` constructor may conflict with type names, variable names, or function names. In such cases, the `enum` type name must be prefixed to use the constructor; otherwise, the system will choose the definition with the same name (type, variable, or function).

In the following example, only the constructor `Blue(UInt8)` can be used without the type name. `Red` and `Green(UInt8)` cannot be used directly due to name conflicts and must be prefixed with the type name `RGBColor`.

<!-- compile -->

```cangjie
let Red = 1

func Green(g: UInt8) {
    return g
}

enum RGBColor {
    | Red | Green(UInt8) | Blue(UInt8)
}

let r1 = Red                 // Will choose 'let Red'
let r2 = RGBColor.Red        // OK: constructed by enum type name

let g1 = Green(100)          // Will choose 'func Green'
let g2 = RGBColor.Green(100) // OK: constructed by enum type name

let b = Blue(100)            // OK: can be uniquely identified as an enum constructor
```

In the following example, only the constructor `Blue` cannot be used directly due to a name conflict and must be prefixed with the type name `RGBColor`.

<!-- compile.error -->

```cangjie
class Blue {}

enum RGBColor {
    | Red | Green(UInt8) | Blue(UInt8)
}

let r = Red                 // OK: constructed by enum type name

let g = Green(100)          // OK: constructed by enum type name

let b = Blue(100)           // Will choose constructor of 'class Blue' and report an error
```