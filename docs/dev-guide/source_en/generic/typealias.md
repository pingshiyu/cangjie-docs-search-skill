# Type Aliases

When a type name is overly complex or not intuitive in a specific context, you can use a type alias to assign an alternative name to that type.

```cangjie
type I64 = Int64
```

A type alias definition begins with the keyword `type`, followed by the alias name (e.g., `I64` in the example above), then an equals sign `=`, and finally the original type (i.e., the type being aliased, such as `Int64` in the example above).

Type aliases can only be defined at the top level of a source file, and the original type must be visible at the point of alias definition. For example, in the following code, the alias definition for `Int64` within `main` will result in an error, and the type `LongNameClassB` is not visible when defining its alias, which will also cause an error.

<!-- compile.error  -->

```cangjie
main() {
    type I64 = Int64 // Error, type aliases can only be defined at the top level of the source file
}

class LongNameClassA { }
type B = LongNameClassB // Error, type 'LongNameClassB' is not defined
```

Direct or indirect circular references are prohibited in one or more type alias definitions.

<!-- compile.error  -->

```cangjie
type A = (Int64, A) // Error, 'A' refered itself
type B = (Int64, C) // Error, 'B' and 'C' are circularly refered
type C = (B, Int64)
```

A type alias does not define a new type; it merely provides another name for the original type. It can be used in the following scenarios:

1. As a type, for example:

    <!-- compile -->

    ```cangjie
    type A = B
    class B {}
    var a: A = B() // Use typealias A as type B
    ```

2. When the type alias actually refers to a class or struct, it can be used as a constructor name:

    <!-- compile -->

    ```cangjie
    type A = B
    class B {}
    func foo() { A() }  // Use type alias A as constructor of B
    ```

3. When the type alias actually refers to a class, interface, or struct, it can be used as the type name to access internal static member variables or functions:

    <!-- compile -->

    ```cangjie
    type A = B
    class B {
        static var b : Int32 = 0
        static func foo() {}
    }
    func foo() {
        A.foo() // Use A to access static method in class B
        A.b
    }
    ```

4. When the type alias actually refers to an enum, it can be used as the type name for the enum's constructors:

    <!-- compile -->

    ```cangjie
    enum TimeUnit {
        Day | Month | Year
    }
    type Time = TimeUnit
    var a = Time.Day  
    var b = Time.Month   // Use type alias Time to access constructors in TimeUnit
    ```

Note that currently, user-defined type aliases are not supported in type conversion expressions. Refer to the following example:

<!-- compile.error  -->

```cangjie
type MyInt = Int32
MyInt(0)  // Error, no matching function for operator '()' function call
```

## Generic Type Aliases

Type aliases can also declare type parameters, but constraints cannot be applied to these parameters using `where` clauses. Constraints for generic type arguments will be explained later.

When a generic type name is too long, a type alias can be used to declare a shorter alternative. For example, a type `RecordData` can be abbreviated as `RD` using a type alias:

<!-- compile -->

```cangjie
struct RecordData<T> {
    var a: T
    public init(x: T) {
        a = x
    }
}

type RD<T> = RecordData<T>

main(): Int64 {
    var struct1: RD<Int32> = RecordData<Int32>(2)
    return 1
}
```

In usage, `RD<Int32>` can be used to refer to the `RecordData<Int32>` type.