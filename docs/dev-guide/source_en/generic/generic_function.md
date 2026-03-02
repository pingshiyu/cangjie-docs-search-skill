# Generic Functions

A function is called a generic function if it declares one or more type parameters. Syntactically, type parameters are placed immediately after the function name, enclosed in `<>`, and separated by `,` if there are multiple type parameters.

## Global Generic Functions

When declaring a global generic function, simply declare the type parameters using angle brackets after the function name. These type parameters can then be referenced in the function parameters, return type, and function body. For example, the `id` function is defined as:

<!-- compile -->

```cangjie
func id<T>(a: T): T {
    return a
}
```

Here, `(a: T)` is the function parameter declaration, which uses the type parameter `T` declared by the `id` function, and the return type of `id` also utilizes this type parameter.

Another more complex example is the generic function `composition`, which declares three type parameters `T1, T2, T3`. Its functionality is to compose two functions `f: (T1) -> T2` and `g: (T2) -> T3` into a function of type `(T1) -> T3`.

<!-- verify -composition -->

```cangjie
func composition<T1, T2, T3>(f: (T1) -> T2, g: (T2) -> T3): (T1) -> T3 {
    return {x: T1 => g(f(x))}
}
```

Since the functions that can be composed can be of any type (e.g., composition of `(Int32) -> Bool` and `(Bool) -> Int64`, or `(Int64) -> Rune` and `(Rune) -> Int8`), generic functions are necessary.

<!-- verify -composition -->

```cangjie
func times2(a: Int64): Int64 {
    return a * 2
}

func plus10(a: Int64): Int64 {
    return a + 10
}

func times2plus10(a: Int64) {
    return composition<Int64, Int64, Int64>(times2, plus10)(a)
}

main() {
  println(times2plus10(9))
}
```

Here, composing two `(Int64) -> Int64` functions first multiplies 9 by 2 and then adds 10, resulting in 28.

<!-- verify -composition -->

```text
28
```

## Local Generic Functions

Local functions can also be generic. For example, the generic function `id` can be nested within other functions:

<!-- verify -->

```cangjie
func foo(a: Int64) {
    func id<T>(a: T): T { a }

    func double(a: Int64): Int64 { a + a }

    return (id<Int64> ~> double)(a) == (double ~> id<Int64>)(a)
}

main() {
    println(foo(1))
}
```

Due to the identity property of `id`, the functions `id<Int64> ~> double` and `double ~> id<Int64>` are equivalent, resulting in `true`.

```text
true
```

## Generic Member Functions

Member functions of classes, structs, enums, and interface can be generic. For example:

<!-- verify -->

```cangjie
class A {
    func foo<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

struct B {
    func bar<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

enum C {
    | X | Y

    func coo<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

interface I {
    func doo<T>(a: T): Unit where T <: ToString
}
class D <: I {
    public func doo<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}
abstract class E {
    public func eoo1<T>(a: T): Unit where T <: ToString
    public open func eoo2<T>(a: T): Unit where T <: ToString
}
class F <: E {
    public func eoo1<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
    public func eoo2<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}
main() {
    var a = A()
    var b = B()
    var c = C.X
    var d = D()
    var f = F()
    a.foo<Int64>(10)
    b.bar<String>("abc")
    c.coo<Bool>(false)
    d.doo<String>("doo")
    f.eoo1<String>("eoo1")
    f.eoo2<String>("eoo2")
    return 0
}
```

The program output will be:

```text
10
abc
false
doo
eoo1
eoo2
```

When extending types using the `extend` declaration, the functions within the extension can also be generic. For example, we can add a generic member function to the `Int64` type:

<!-- verify -->

```cangjie
extend Int64 {
    func printIntAndArg<T>(a: T) where T <: ToString {
        println(this)
        println("${a}")
    }
}

main() {
    var a: Int64 = 12
    a.printIntAndArg<String>("twelve")
}
```

The program output will be:

```text
12
twelve
```

## Static Generic Functions

Interfaces, classes, structs, enums, and extensions can define static generic functions. For example, the following `ToPair` class returns a tuple from an `ArrayList`:

<!-- run -->

```cangjie
import std.collection.ArrayList

class ToPair {
    public static func fromArray<T>(l: ArrayList<T>): (T, T) {
        return (l[0], l[1])
    }
}

main() {
    var res: ArrayList<Int64> = ArrayList([1,2,3,4])
    var a: (Int64, Int64) = ToPair.fromArray<Int64>(res)
}
```
