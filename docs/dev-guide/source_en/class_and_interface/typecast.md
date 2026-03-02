# Type Conversion

Cangjie does not support implicit conversion between different types (subtypes are inherently parent types, so conversion from a subtype to a parent type is not implicit type conversion). Type conversion must be performed explicitly. The following sections will introduce conversions between numeric types, conversions from `Rune` to `UInt32` and from integer types to `Rune`, as well as the `is` and `as` operators.

## Conversions Between Numeric Types

For numeric types (including: `Int8`, `Int16`, `Int32`, `Int64`, `IntNative`, `UInt8`, `UInt16`, `UInt32`, `UInt64`, `UIntNative`, `Float16`, `Float32`, `Float64`), Cangjie supports using the `T(e)` syntax to obtain a value equal to `e` with type `T`. Here, the expression `e` and type `T` can be any of the aforementioned numeric types.

The following example demonstrates type conversion between numeric types:

<!-- verify -->

```cangjie
main() {
    let a: Int8 = 10
    let b: Int16 = 20
    let r1 = Int16(a)
    println("The type of r1 is 'Int16', and r1 = ${r1}")
    let r2 = Int8(b)
    println("The type of r2 is 'Int8', and r2 = ${r2}")

    let c: Float32 = 1.0
    let d: Float64 = 1.123456789
    let r3 = Float64(c)
    println("The type of r3 is 'Float64', and r3 = ${r3}")
    let r4 = Float32(d)
    println("The type of r4 is 'Float32', and r4 = ${r4}")

    let e: Int64 = 1024
    let f: Float64 = 1024.1024
    let r5 = Float64(e)
    println("The type of r5 is 'Float64', and r5 = ${r5}")
    let r6 = Int64(f)
    println("The type of r6 is 'Int64', and r6 = ${r6}")
}
```

The execution result of the above code is:

```text
The type of r1 is 'Int16', and r1 = 10
The type of r2 is 'Int8', and r2 = 20
The type of r3 is 'Float64', and r3 = 1.000000
The type of r4 is 'Float32', and r4 = 1.123457
The type of r5 is 'Float64', and r5 = 1024.000000
The type of r6 is 'Int64', and r6 = 1024
```

> **Note:**
>
> Overflow may occur during type conversion. If the overflow can be detected by the compiler in advance, the compiler will directly report an error. Otherwise, an exception will be thrown according to the default overflow policy.

## Conversion from `Rune` to `UInt32` and from Integer Types to `Rune`

Conversion from `Rune` to `UInt32` uses the `UInt32(e)` syntax, where `e` is a `Rune`-type expression. The result of `UInt32(e)` is the `UInt32`-type integer value corresponding to the Unicode scalar value of `e`.

Conversion from integer types to `Rune` uses the `Rune(num)` syntax, where `num` can be of any integer type. Only when the value of `num` falls within `[0x0000, 0xD7FF]` or `[0xE000, 0x10FFFF]` (i.e., Unicode scalar value range), the corresponding character represented by the Unicode scalar value is returned. Otherwise, a compilation error will occur (if the value of `num` can be determined at compile time) or an exception will be thrown at runtime.

The following example demonstrates type conversion between `Rune` and `UInt32`:

<!-- verify -->

```cangjie
main() {
    let x: Rune = 'a'
    let y: UInt32 = 65
    let r1 = UInt32(x)
    let r2 = Rune(y)
    println("The type of r1 is 'UInt32', and r1 = ${r1}")
    println("The type of r2 is 'Rune', and r2 = ${r2}")
}
```

The execution result of the above code is:

```text
The type of r1 is 'UInt32', and r1 = 97
The type of r2 is 'Rune', and r2 = A
```

## The `is` and `as` Operators

Cangjie supports using the `is` operator to determine whether the type of an expression is the specified type (or its subtype). Specifically, for the expression `e is T` (where `e` can be any expression and `T` can be any type), when the runtime type of `e` is a subtype of `T`, the value of `e is T` is `true`; otherwise, it is `false`.

The following example demonstrates the use of the `is` operator:

<!-- verify -->

```cangjie
open class Base {
    var name: String = "Alice"
}
class Derived <: Base {
    var age: UInt8 = 18
}

main() {
    let a = 1 is Int64
    println("Is the type of 1 'Int64'? ${a}")
    let b = 1 is String
    println("Is the type of 1 'String'? ${b}")

    let b1: Base = Base()
    let b2: Base = Derived()
    var x = b1 is Base
    println("Is the type of b1 'Base'? ${x}")
    x = b1 is Derived
    println("Is the type of b1 'Derived'? ${x}")
    x = b2 is Base
    println("Is the type of b2 'Base'? ${x}")
    x = b2 is Derived
    println("Is the type of b2 'Derived'? ${x}")
}
```

The execution result of the above code is:

```text
Is the type of 1 'Int64'? true
Is the type of 1 'String'? false
Is the type of b1 'Base'? true
Is the type of b1 'Derived'? false
Is the type of b2 'Base'? true
Is the type of b2 'Derived'? true
```

The `as` operator can be used to convert the type of an expression to the specified type. Since type conversion may fail, the `as` operator returns an `Option` type. Specifically, for the expression `e as T` (where `e` can be any expression and `T` can be any type), when the runtime type of `e` is a subtype of `T`, the value of `e as T` is `Option<T>.Some(e)`; otherwise, it is `Option<T>.None`.

The following example demonstrates the use of the `as` operator (comments indicate the results of the `as` operation):

<!-- compile -->

```cangjie
open class Base {
    var name: String = "Alice"
}
class Derived <: Base {
    var age: UInt8 = 18
}

let a = 1 as Int64     // a = Option<Int64>.Some(1)
let b = 1 as String    // b = Option<String>.None

let b1: Base = Base()
let b2: Base = Derived()
let d: Derived = Derived()
let r1 = b1 as Base    // r1 = Option<Base>.Some(b1)
let r2 = b1 as Derived // r2 = Option<Derived>.None
let r3 = b2 as Base    // r3 = Option<Base>.Some(b2)
let r4 = b2 as Derived // r4 = Option<Derived>.Some(b2)
let r5 = d as Base     // r5 = Option<Base>.Some(d)
let r6 = d as Derived  // r6 = Option<Derived>.Some(d)
```