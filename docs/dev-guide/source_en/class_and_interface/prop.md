# Properties

Properties provide a getter and an optional setter to indirectly retrieve and modify values.

When using properties, they behave no differently from ordinary variables—you only need to manipulate the data without being aware of the internal implementation. This facilitates mechanisms such as access control, data monitoring, debugging, and data binding.

Properties can be used as expressions or assigned values. Here, classes and interfaces are used as examples, but properties are not limited to these.

The following is a simple example where `b` is a typical property that encapsulates external access to `a`:

<!-- verify -->

```cangjie
class Foo {
    private var a = 0

    public mut prop b: Int64 {
        get() {
            println("get")
            a
        }
        set(value) {
            println("set")
            a = value
        }
    }
}

main() {
    var x = Foo()
    let y = x.b + 1 // get
    x.b = y // set
}
```

Here, `Foo` provides a property named `b`. For the getter/setter functionality, Cangjie provides `get` and `set` syntax for definition. When a variable `x` of type `Foo` accesses `b`, the get operation of `b` is called, returning a value of type `Int64`, which can then be used to add to `1`. When `x` assigns a value to `b`, the set operation of `b` is called, passing the value of `y` to the `value` parameter of `set`, and ultimately assigning `value` to `a`.

Through property `b`, external code remains completely unaware of the member variable `a` in `Foo`, yet can achieve the same access and modification operations via `b`, demonstrating effective encapsulation. Thus, the program outputs:

```text
get
set
```

## Property Definition

Properties can be defined in `interface`, `class`, `struct`, `enum`, and `extend`.

A typical property syntax structure is as follows:

<!-- compile -->

```cangjie
class Foo {
    public prop a: Int64 {
        get() { 0 }
    }
    public mut prop b: Int64 {
        get() { 0 }
        set(v) {}
    }
}
```

Here, `a` and `b` declared with `prop` are both properties, and both are of type `Int64`. `a` is a property without the `mut` modifier—such properties must define only a getter (for value retrieval). `b` is a property with the `mut` modifier—such properties must define both a getter (for value retrieval) and a setter (for value assignment).

> **Note:**
>
> For numeric types, tuples, functions, `Bool`, `Unit`, `Nothing`, `String`, `Range`, and `enum` types, mut properties cannot be declared in their extensions or declarations, nor can interfaces with mut properties be implemented.

The getter and setter of a property correspond to two distinct functions.

1. The getter function type is `() -> T`, where `T` is the property's type. The getter function is executed when the property is used as an expression.
2. The setter function type is `(T) -> Unit`, where `T` is the property's type. The parameter name must be explicitly specified. The setter function is executed when the property is assigned a value.

The implementations of the getter and setter can include declarations and expressions, just like function bodies, following the same rules as function bodies. For details, refer to the [Function Body](../function/define_functions.md#function-body) section.

The parameter in the setter corresponds to the value passed during assignment.

<!-- compile -->

```cangjie
class Foo {
    private var j = 0
    public mut prop i: Int64 {
        get() {
            j
        }
        set(v) {
            j = v
        }
    }
}
```

Note that accessing the property itself within its getter or setter constitutes a recursive call, which, like function calls, may lead to infinite loops.

### Modifiers

Modifiers can be declared before `prop`.

<!-- compile -->

```cangjie
class Foo {
    public prop a: Int64 {
        get() {
            0
        }
    }
    private prop b: Int64 {
        get() {
            0
        }
    }
}
```

Like member functions, member properties also support the `open`, `override`, and `redef` modifiers, allowing properties to be overridden/redefined in subtypes.

When a subtype overrides a property from its parent type, if the parent property has the `mut` modifier, the subtype property must also have the `mut` modifier and maintain the same type.

As shown in the following code, `A` defines two properties, `x` and `y`. `B` can override/redefine `x` and `y` using `override`/`redef`:

<!-- compile -->

```cangjie
open class A {
    private var valueX = 0
    private static var valueY = 0

    public open prop x: Int64 {
        get() { valueX }
    }

    public static mut prop y: Int64 {
        get() { valueY }
        set(v) {
            valueY = v
        }
    }
}
class B <: A {
    private var valueX2 = 0
    private static var valueY2 = 0

    public override prop x: Int64 {
        get() { valueX2 }
    }

    public redef static mut prop y: Int64 {
        get() { valueY2 }
        set(v) {
            valueY2 = v
        }
    }
}
```

### Abstract Properties

Similar to abstract functions, abstract properties can be declared in `interface` and abstract classes. These abstract properties have no implementation.

<!-- compile -->

```cangjie
interface I {
    prop a: Int64
}

abstract class C {
    public prop a: Int64
}
```

When an implementing type realizes an `interface` or a non-abstract subclass inherits from an abstract class, these abstract properties must be implemented.

Like the rules for overriding, if the parent property has the `mut` modifier, the subtype property must also have the `mut` modifier and maintain the same type.

<!-- compile -->

```cangjie
interface I {
    prop a: Int64
    mut prop b: Int64
}
class C <: I {
    private var value = 0

    public prop a: Int64 {
        get() { value }
    }

    public mut prop b: Int64 {
        get() { value }
        set(v) {
            value = v
        }
    }
}
```

Abstract properties allow interfaces and abstract classes to specify data operations in a more user-friendly manner, making them more intuitive compared to function-based approaches.

As shown in the following code, if you want to specify the retrieval and modification of a `size` value, using properties (`I1`) results in less code and aligns better with the intent of data manipulation compared to using functions (`I2`).

<!-- verify -->

```cangjie
interface I1 {
    mut prop size: Int64
}

interface I2 {
    func getSize(): Int64
    func setSize(value: Int64): Unit
}

class C <: I1 & I2 {
    private var mySize = 0

    public mut prop size: Int64 {
        get() {
            mySize
        }
        set(value) {
            mySize = value
        }
    }

    public func getSize() {
        mySize
    }

    public func setSize(value: Int64) {
        mySize = value
    }
}

main() {
    let a: I1 = C()
    a.size = 5
    println(a.size)

    let b: I2 = C()
    b.setSize(5)
    println(b.getSize())
}
```

```text
5
5
```

## Property Usage

Properties are divided into instance member properties and static member properties. The usage of member properties is the same as that of member variables. For details, refer to the [Member Variables](./class.md#class-member-variables) section.

<!-- verify -->

```cangjie
class A {
    public prop x: Int64 {
        get() {
            123
        }
    }
    public static prop y: Int64 {
        get() {
            321
        }
    }
}

main() {
    var a = A()
    println(a.x) // 123
    println(A.y) // 321
}
```

The result is:

```text
123
321
```

Properties without the `mut` modifier are similar to variables declared with `let` and cannot be assigned.

<!-- compile.error -->

```cangjie
class A {
    private let value = 0
    public prop i: Int64 {
        get() {
            value
        }
    }
}

main() {
    var x = A()
    println(x.i) // OK
    x.i = 1 // Error
}
```

Properties marked with the `mut` modifier are similar to variables declared with `var`, allowing both value retrieval and assignment.

<!-- verify -->

```cangjie
class A {
    private var value: Int64 = 0
    public mut prop i: Int64 {
        get() {
            value
        }
        set(v) {
            value = v
        }
    }
}

main() {
    var x = A()
    println(x.i) // OK
    x.i = 1 // OK
}
```

```text
0
```
