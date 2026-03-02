# Direct Extension

A simple example of extension syntax is as follows:

<!-- verify -printSize -->

```cangjie
extend String {
    public func printSize() {
        println("the size is ${this.size}")
    }
}
```

As shown in the example above, extensions are declared using the `extend` keyword, followed by the extended type `String` and the extended functionality.

After extending the `String` type with the `printSize` function, instances of `String` within the current `package` can access this function as if it were native to `String`.

<!-- verify -printSize -->

```cangjie
main() {
    let a = "123"
    a.printSize() // the size is 3
}
```

Compiling and executing the above code yields the output:

<!-- verify -printSize -->

```text
the size is 3
```

When extending generic types, there are two syntax approaches for adding functionality.

The first approach extends specific instantiated generic types. The `extend` keyword can be followed by any fully instantiated generic type. The added functionality is only available when the type exactly matches, and the type arguments must satisfy the constraints defined in the generic type declaration.

For example, consider `Foo<T>` below:

<!-- compile.error -->

```cangjie
class Foo<T> where T <: ToString {}

extend Foo<Int64> {} // OK

class Bar {}
extend Foo<Bar> {} // Error, generics type arguments do not match the constraint of 'Class-Foo<Generics-T>'
```

The second approach uses generic extension by introducing type parameters after `extend`. Generic extensions can extend uninstantiated or partially instantiated generic types. The type parameters declared after `extend` must be directly or indirectly used in the extended generic type. The added functionality is only available when both the type and constraints fully match.

For example, consider `MyList<T>` below:

<!-- compile.error -->

```cangjie
class MyList<T> {
    public let data: Array<T> = Array<T>()
}

extend<T> MyList<T> {}          // OK
extend<R> MyList<R> {}          // OK
extend<T, R> MyList<(T, R)> {}  // OK
extend MyList {}                // Error, generic type should be used with type argument
extend<T, R> MyList<T> {}       // Error, type parameter 'R' must be used in extended type
extend<T, R> MyList<T, R> {}    // Error, type argument's number does not match type parameter's number
```

For generic type extensions, additional constraints can be declared to implement functions that are only available under specific conditions.

For example, we can define a type called Pair that conveniently stores two elements (similar to Tuple). We want the Pair type to accommodate any type, so the two generic parameters should have no constraints to ensure Pair can hold all types. However, we also want Pair to support equality comparison when both elements are comparable. This can be achieved using extensions.

As shown in the code below, the extension syntax constrains T1 and T2 to support the equals operation, enabling Pair to implement the equals function when these conditions are met.

<!-- verify -->

```cangjie
class Pair<T1, T2> {
    var first: T1
    var second: T2
    public init(a: T1, b: T2) {
        first = a
        second = b
    }
}

interface Eq<T> {
    func equals(other: T): Bool
}

extend<T1, T2> Pair<T1, T2> where T1 <: Eq<T1>, T2 <: Eq<T2> {
    public func equals(other: Pair<T1, T2>) {
        first.equals(other.first) && second.equals(other.second)
    }
}

class Foo <: Eq<Foo> {
    public func equals(other: Foo): Bool {
        true
    }
}

main() {
    let a = Pair(Foo(), Foo())
    let b = Pair(Foo(), Foo())
    println(a.equals(b)) // true
}
```

Compiling and executing the above code yields the output:

```text
true
```