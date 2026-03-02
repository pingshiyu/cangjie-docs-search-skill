# Defining struct Types

The definition of a `struct` type begins with the keyword `struct`, followed by the name of the `struct`, and then the struct body enclosed in a pair of curly braces. The struct body can define a series of member variables, member properties (see [Properties](../class_and_interface/prop.md)), static initializers, constructors, and member functions.

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func area() {
        width * height
    }
}
```

The above example defines a `struct` type named `Rectangle`, which has two member variables of type `Int64`: `width` and `height`, a constructor with two `Int64` parameters (defined using the keyword `init`, where the function body typically initializes member variables), and a member function `area` (which returns the product of `width` and `height`).

> **Note:**
>
> `struct` can only be defined at the top-level scope of a source file.

## struct Member Variables

`struct` member variables are divided into instance member variables and static member variables (modified with the `static` modifier). The difference in access is that instance member variables can only be accessed through `struct` instances (saying `a` is an instance of type `T` means `a` is a value of type `T`), while static member variables can only be accessed through the `struct` type name.

Instance member variables can be defined without an initial value (but the type must be annotated, as in the `width` and `height` in the example above), or they can be assigned an initial value, for example:

<!-- compile -->

```cangjie
struct Rectangle {
    let width = 10
    let height = 20
}
```

## struct Static Initializers

`struct` supports defining static initializers, which initialize static member variables through assignment expressions within the static initializer.

A static initializer begins with the keyword combination `static init`, followed by a parameterless parameter list and a function body, and cannot be modified by access modifiers. The function body must complete the initialization of all uninitialized static member variables; otherwise, a compilation error will occur.

<!-- compile -->

```cangjie
struct Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
}
```

A `struct` can define at most one static initializer; otherwise, a redefinition error will occur.

<!-- compile.error -->

```cangjie
struct Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
    static init() { // Error, redefinition with the previous static init function
        degree = 180
    }
}
```

## struct Constructors

`struct` supports two types of constructors: ordinary constructors and primary constructors.

An ordinary constructor begins with the keyword `init`, followed by a parameter list and a function body. The function body must complete the initialization of all uninitialized instance member variables (if parameter names and member variable names cannot be distinguished, the member variable can be prefixed with `this` for clarification, where `this` represents the current instance of the `struct`); otherwise, a compilation error will occur.

<!-- compile.error -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) { // Error, 'height' is not initialized in the constructor
        this.width = width
    }
}
```

A `struct` can define multiple ordinary constructors, but they must constitute overloads (see [Function Overloading](../function/function_overloading.md)); otherwise, a redefinition error will occur.

<!-- compile.error -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64) {
        this.width = width
        this.height = width
    }

    public init(width: Int64, height: Int64) { // OK: overloading with the first init function
        this.width = width
        this.height = height
    }

    public init(height: Int64) { // Error, redefinition with the first init function
        this.width = height
        this.height = height
    }
}
```

In addition to defining ordinary constructors named `init`, a `struct` can also define (at most) one primary constructor. The primary constructor has the same name as the `struct` type, and its parameter list can include two types of parameters: ordinary parameters and member variable parameters (prefixed with `let` or `var`). Member variable parameters serve the dual purpose of defining member variables and acting as constructor parameters.

Using a primary constructor can often simplify the definition of a `struct`. For example, the above `Rectangle` with an `init` constructor can be simplified as follows:

<!-- compile -->

```cangjie
struct Rectangle {
    public Rectangle(let width: Int64, let height: Int64) {}
}
```

The primary constructor's parameter list can also include ordinary parameters, for example:

<!-- compile -->

```cangjie
struct Rectangle {
    public Rectangle(name: String, let width: Int64, let height: Int64) {}
}
```

If a `struct` definition does not include any custom constructors (including primary constructors) and all instance member variables have initial values, an automatic parameterless constructor will be generated (calling this constructor creates an object where all instance member variables are initialized to their default values); otherwise, this parameterless constructor will not be generated. For example, for the following `struct` definition, the automatically generated parameterless constructor is shown in the comments:

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 10
    let height: Int64 = 10
    /* Auto-generated memberwise constructor:
    public init() {
    }
    */
}
```

## struct Member Functions

`struct` member functions are divided into instance member functions and static member functions (modified with the `static` modifier). The differences are:

- Instance member functions can only be accessed through `struct` instances, while static member functions can only be accessed through the `struct` type name.
- Static member functions cannot access instance member variables or call instance member functions, but instance member functions can access static member variables and call static member functions.

In the following example, `area` is an instance member function, and `typeName` is a static member function.

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 10
    let height: Int64 = 20

    public func area() {
        this.width * this.height
    }

    public static func typeName(): String {
        "Rectangle"
    }
}
```

Instance member functions can access instance member variables via `this`, for example:

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 1
    let height: Int64 = 1

    public func area() {
        this.width * this.height
    }
}
```

## Access Modifiers for struct Members

`struct` members (including member variables, member properties, constructors, member functions, and operator functions (see [Operator Overloading](../function/operator_overloading.md))) can be modified with four access modifiers: `private`, `internal`, `protected`, and `public`. The default modifier is `internal`.

- `private`: Visible only within the `struct` definition.
- `internal`: Visible only within the current package and sub-packages (including sub-packages of sub-packages, see [Packages](../package/toplevel_access.md)).
- `protected`: Visible within the current module (see [Packages](../package/toplevel_access.md)).
- `public`: Visible both inside and outside the module.

In the following example, `width` is a `public` member and can be accessed outside the class, `height` has the default access modifier and is only visible within the current package and sub-packages (other packages cannot access it).

<!-- compile.error -->

```cangjie
package a
public struct Rectangle {
    public var width: Int64
    var height: Int64
    private var area: Int64

    public init(width: Int64, height: Int64, area: Int64) {
        this.width = width
        this.height = height
        this.area = area
    }
}

func samePkgFunc() {
    var r = Rectangle(10, 20, 40)
    r.width = 8               // OK: public 'width' can be accessed here
    r.height = 24             // OK: 'height' has no modifier and can be accessed here
    r.area = 30               // Error, private 'area' can't be accessed here
}
```

<!-- compile.error -->
<!-- cfg="-p b --output-type=staticlib" -->
<!-- cfg="liba.a" -->

```cangjie
package b
import a.*

main() {
    r.width = 8     // OK: public 'width' can be accessed here
    r.height = 24   // Error, no modifier 'height' can't be accessed here
    r.area = 30     // Error, private 'area' can't be accessed here
}
```

## Prohibiting Recursive structs

Recursive and mutually recursive `struct` definitions are illegal. For example:

<!-- compile.error -->

```cangjie
struct R1 { // Error, 'R1' recursively references itself
    let other: R1
}
struct R2 { // Error, 'R2' and 'R3' are mutually recursive
    let other: R3
}
struct R3 { // Error, 'R2' and 'R3' are mutually recursive
    let other: R2
}
```