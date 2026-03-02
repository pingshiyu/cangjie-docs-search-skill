# Interface Extension

For example, in the following case, the type `Array` does not inherently implement the interface `PrintSizeable`. However, we can use extension to add an additional member function `printSize` to `Array` and implement `PrintSizeable`.

<!-- verify -PrintSizeable -->

```cangjie
interface PrintSizeable {
    func printSize(): Unit
}

extend<T> Array<T> <: PrintSizeable {
    public func printSize() {
        println("The size is ${this.size}")
    }
}
```

After extending `Array` to implement `PrintSizeable`, it is equivalent to `Array` having implemented `PrintSizeable` at its definition time.

Therefore, `Array` can be used as an implementation type of `PrintSizeable`, as shown in the following code.

<!-- verify -PrintSizeable -->

```cangjie
main() {
    let a: PrintSizeable = Array<Int64>()
    a.printSize() // 0
}
```

Compiling and executing the above code yields the output:

<!-- verify -PrintSizeable -->

```text
The size is 0
```

Multiple interfaces can be implemented simultaneously within the same extension. Separate the interfaces with `&`, and their order does not matter.

As shown in the following code, we can implement `I1`, `I2`, and `I3` for `Foo` in a single extension.

<!-- compile -->

```cangjie
interface I1 {
    func f1(): Unit
}

interface I2 {
    func f2(): Unit
}

interface I3 {
    func f3(): Unit
}

class Foo {}

extend Foo <: I1 & I2 & I3 {
    public func f1(): Unit {}
    public func f2(): Unit {}
    public func f3(): Unit {}
}
```

Additional generic constraints can also be declared in interface extensions to satisfy interfaces under specific conditions.

For example, we can make the `Pair` type implement the `Eq` interface, allowing `Pair` itself to become a type that satisfies the `Eq` constraint, as shown below.

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

extend<T1, T2> Pair<T1, T2> <: Eq<Pair<T1, T2>> where T1 <: Eq<T1>, T2 <: Eq<T2> {
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

If the extended type already includes the functions or properties required by the interface, these functions or properties need not (and cannot) be re-implemented in the extension.

For example, in the following case, a new interface `Sizeable` is defined to retrieve the `size` of a type. Since `Array` already contains this function, we can extend `Array` to implement `Sizeable` without adding additional functions.

<!-- verify -->

```cangjie
interface Sizeable {
    prop size: Int64
}

extend<T> Array<T> <: Sizeable {}

main() {
    let a: Sizeable = Array<Int64>()
    println(a.size)
}
```

Compiling and executing the above code yields the output:

```text
0
```

When interface extensions implement interfaces with inheritance relationships, the extensions are checked in the order of "first checking extensions implementing parent interfaces, then checking extensions implementing child interfaces."

For example, if interface `I1` has a child interface `I2`, and `I1` contains a default implementation, while type `A` has two extensions implementing the parent and child interfaces respectively, the extension implementing `I1` will be checked first, followed by the extension implementing `I2`.

<!-- verify -->

```cangjie
interface I1 {
    func foo(): Unit { println("I1 foo") }
}
interface I2 <: I1 {
    func foo(): Unit { println("I2 foo") }
}

class A {}

extend A <: I1 {} // first check
extend A <: I2 {} // second check

main() {
    A().foo()
}
```

Compiling and executing the above code yields the output:

```text
I2 foo
```

In this example, when checking the extension implementing `I1`, the `foo` function is inherited from `I1`. When checking the extension implementing `I2`, since `A` already has an inherited default implementation of `foo` with the same signature, this `foo` will be overridden. Thus, when calling `A`'s `foo` function, it ultimately points to the implementation in `I2` (the child interface).

If two interface extensions of the same type implement interfaces with conflicting inheritance relationships, making it impossible to determine the checking order, an error will be reported.

<!-- compile.error -->

```cangjie
interface I1 {}
interface I2 <: I1 {}
interface I3 {}
interface I4 <: I3 {}

class A {}
extend A <: I1 & I4 {} // error: unable to decide which extension happens first
extend A <: I2 & I3 {} // error: unable to decide which extension happens first
```

If two interface extensions of the same type implement interfaces without inheritance relationships, they will be checked simultaneously.

<!-- compile.error -->

```cangjie
interface I1 {
    func foo() {}
}
interface I2 {
    func foo() {}
}

class A {}
extend A <: I1 {} // Error, multiple default implementations, need to re-implement 'foo' in 'A'
extend A <: I2 {} // Error, multiple default implementations, need to re-implement 'foo' in 'A'
```

> **Note:**
>
> When class A has a generic base class `B<T1,...,Tn>`, and `B<T1,...,Tn>` extends an interface `I<R1,...,Rn>` with default implementations of instance or static functions (e.g., `foo`), if this function is not overridden in `B<T1,...,Tn>` or its extensions, and class A does not directly implement the interface `I<R1,...,Rn>`, calling the function `foo` through an instance of class A may lead to unexpected behavior.

<!-- compile -->

```cangjie
interface I<N> {
    func foo(n: N): N {n}
}

open class B<T> {}

extend<T> B<T> <: I<T> {}

class A <: B<Int64>{}

main() {
    A().foo(0) // this call triggers unexpected behaviour
}
```