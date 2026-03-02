# mut Functions

The struct type is a value type, and its instance member functions cannot modify the instance itself. For example, in the following case, the member function `g` cannot modify the value of member variable `i`.

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public func g() {
        i += 1  // Error, the value of a instance member variable cannot be modified in an instance member function
    }
}
```

A mut function is a special instance member function that can modify the struct instance itself. Inside a `mut` function, the semantics of `this` are special—this `this` has the capability to modify fields in-place.

> **Note:**
>
> `mut` functions can only be defined within interfaces, structs, and struct extensions (classes are reference types, and their instance member functions can modify instance member variables without requiring `mut`, so defining `mut` functions in classes is prohibited).

## Definition of mut Functions

Compared to ordinary instance member functions, mut functions are distinguished by an additional `mut` keyword modifier.

For example, in the following case, adding the `mut` modifier before function `g` allows modification of member variable `i` within the function body.

<!-- compile -->

```cangjie
struct Foo {
    var i = 0

    public mut func g() {
        i += 1  // OK
    }
}
```

`mut` can only modify instance member functions and cannot modify static member functions.

<!-- compile.error -->

```cangjie
struct A {
    public mut func f(): Unit {} // OK
    public mut operator func +(rhs: A): A { // OK
        A()
    }
    public mut static func g(): Unit {} // Error, static member functions cannot be modified with 'mut'
}
```

In mut functions, `this` cannot be captured or used as an expression. Lambdas or nested functions within `mut` functions cannot capture instance member variables of the struct.

Example:

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public mut func f(): Foo {
        let f1 = { => this } // Error, 'this' in mut functions cannot be captured
        let f2 = { => this.i = 2 } // Error, instance member variables in mut functions cannot be captured
        let f3 = { => this.i } // Error, instance member variables in mut functions cannot be captured
        let f4 = { => i } // Error, instance member variables in mut functions cannot be captured
        this // Error, 'this' in mut functions cannot be used as expressions
    }
}
```

## mut Functions in Interfaces

Instance member functions in interfaces can also be modified with `mut`.

When a `struct` type implements functions from an `interface`, it must maintain the same `mut` modifier. Types other than `struct` cannot use the `mut` modifier when implementing interface functions.

Example:

<!-- compile.error -->

```cangjie
interface I {
    mut func f1(): Unit
    func f2(): Unit
}

struct A <: I {
    public mut func f1(): Unit {} // OK: as in the interface, the 'mut' modifier is used
    public func f2(): Unit {} // OK: as in the interface, the 'mut' modifier is not used
}

struct B <: I {
    public func f1(): Unit {} // Error, 'f1' is modified with 'mut' in interface, but not in struct
    public mut func f2(): Unit {} // Error, 'f2' is not modified with 'mut' in interface, but did in struct
}

class C <: I {
    public func f1(): Unit {} // OK
    public func f2(): Unit {} // OK
}
```

When a `struct` instance is assigned to an `interface` type, it follows copy semantics. Therefore, the `mut` function of the interface cannot modify the value of the `struct` instance.

Example:

<!-- verify -->

```cangjie
interface I {
    mut func f(): Unit
}
struct Foo <: I {
    public var v = 0
    public mut func f(): Unit {
        v += 1
    }
}
main() {
    var a = Foo()
    var b: I = a  
    b.f()  // Calling 'f' via 'b' cannot modify the value of 'a'
    println(a.v) // 0
}
```

The program output is:

```text
0
```

## Usage Restrictions of mut Functions

Because `struct` is a value type, if a variable is of `struct` type and declared with `let`, the `mut` functions of that type cannot be accessed via this variable.

Example:

<!-- compile.error -->

```cangjie
interface I {
    mut func f(): Unit
}
struct Foo <: I {
    public var i = 0
    public mut func f(): Unit {
        i += 1
    }
}
main() {
    let a = Foo()
    a.f() // Error, 'a' is of type struct and is declared with 'let', the 'mut' function cannot be accessed via 'a'
    var b = Foo()
    b.f() // OK
    let c: I = Foo()
    c.f() // OK, variable 'c' is of interface type I, not struct type, so access is permitted here.
}
```

To prevent escape, if a variable is of `struct` type, it cannot use `mut` functions as first-class citizens; it can only call these `mut` functions.

Example:

<!-- compile.error -->

```cangjie
interface I {
    mut func f(): Unit
}

struct Foo <: I {
    var i = 0

    public mut func f(): Unit {
        i += 1
    }
}

main() {
    var a = Foo()
    var fn = a.f // Error, mut function 'f' of 'a' cannot be used as a first class citizen.
    var b: I = Foo()
    fn = b.f // OK
}
```

To prevent escape, non-`mut` instance member functions (including `lambda` expressions) cannot directly access `mut` functions of their containing type, but the reverse is allowed.

Example:

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public mut func f(): Unit {
        i += 1
        g() // OK
    }

    public func g(): Unit {
        f() // Error, mut functions cannot be invoked in non-mut functions
    }
}

interface I {
    mut func f(): Unit {
        g() // OK
    }

    func g(): Unit {
        f() // Error, mut functions cannot be invoked in non-mut functions
    }
}
```