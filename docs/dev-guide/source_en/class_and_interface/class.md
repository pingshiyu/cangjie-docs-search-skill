# Classes

The `class` type is a classic concept in object-oriented programming. Cangjie also supports using `class` to implement object-oriented programming. The main differences between `class` and `struct` are: `class` is a reference type while `struct` is a value type, and they behave differently during assignment or parameter passing; `class` types can inherit from each other, but `struct` types cannot.

This section sequentially introduces how to define `class` types, how to create objects, and class inheritance.

## Class Definition

A `class` type definition starts with the keyword `class`, followed by the class name, and then the class body enclosed in curly braces. The class body can define a series of member variables, member properties (see [Properties](prop.md)), static initializers, constructors, member functions, and operator functions (details in [Operator Overloading](../function/operator_overloading.md)).

<!-- compile -->

```cangjie
class Rectangle {
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

The above example defines a `class` type named `Rectangle`, which has two `Int64` member variables `width` and `height`, a constructor with two `Int64` parameters, and a member function `area` (returning the product of `width` and `height`).

> **Note:**
>
> `class` can only be defined at the top-level scope of a source file.

A class modified with `abstract` is an abstract class. Unlike regular classes, abstract classes can declare abstract functions (without function bodies) in addition to defining normal functions. The `open` modifier in abstract class definitions is optional, and the `sealed` modifier can also be used. The `sealed` modifier indicates that the abstract class can only be inherited within the same package (see [Class Inheritance](#class-inheritance)). The following example defines an abstract function `foo` in the abstract class `AbRectangle`.

<!-- compile -->

```cangjie
abstract class AbRectangle {
    public func foo(): Unit
}
```

> **Note:**
>
> - Abstract classes cannot define `private` abstract functions;
> - Instances of abstract classes cannot be created;
> - Non-abstract subclasses of abstract classes must implement all abstract functions from the parent class.

### Class Member Variables

Class member variables are divided into instance member variables and static member variables. Static member variables are modified with the `static` modifier, must have initial values if no static initializer is present, and can only be accessed via the type name, as shown in the following example:

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    static let height = 20
}

let l = Rectangle.height // l = 20
```

Instance member variables can be defined without initial values (but must have type annotations) or with initial values, and can only be accessed via objects (i.e., instances of the class), as shown in the following example:

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    let height: Int64
    init(h: Int64) {
        height = h
    }
}
let rec = Rectangle(20)
let l = rec.height // l = 20
```

### Class Static Initializer

Classes support defining static initializers, where static member variables can be initialized via assignment expressions.

A static initializer starts with the keyword combination `static init`, followed by a parameterless parameter list and a function body, and cannot be modified with access modifiers. The function body must initialize all uninitialized static member variables; otherwise, a compilation error occurs.

<!-- compile -->

```cangjie
class Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
}
```

A class can define at most one static initializer; otherwise, a redefinition error occurs.

<!-- compile.error -->

```cangjie
class Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
    static init() { // Error, redefinition with the previous static init function
        degree = 180
    }
}
```

### Class Constructors

Like `struct`, `class` also supports defining regular constructors and primary constructors.

A regular constructor starts with the keyword `init`, followed by a parameter list and a function body. The function body must initialize all uninitialized instance member variables; otherwise, a compilation error occurs.

<!-- compile.error -->

```cangjie
class Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) { // Error, 'height' is not initialized in the constructor
        this.width = width
    }
}
```

A class can define multiple regular constructors, but they must constitute overloads (see [Function Overloading](../function/function_overloading.md)); otherwise, a redefinition error occurs.

<!-- compile.error -->

```cangjie
class Rectangle {
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

In addition to defining regular `init` constructors, a class can define (at most) one primary constructor. The primary constructor has the same name as the class type, and its parameter list can include two types of parameters: regular parameters and member variable parameters (prefixed with `let` or `var`). Member variable parameters serve the dual purpose of defining member variables and constructor parameters.

Using a primary constructor can often simplify class definitions. For example, the above `Rectangle` with an `init` constructor can be simplified as follows:

<!-- compile -->

```cangjie
class Rectangle {
    public Rectangle(let width: Int64, let height: Int64) {}
}
```

The primary constructor's parameter list can also include regular parameters, for example:

<!-- compile -->

```cangjie
class Rectangle {
    public Rectangle(name: String, let width: Int64, let height: Int64) {}
}
```

When creating an instance of a class, the constructor is called, and the following sequence of expressions in the class is executed:

1. First, initialize variables defined outside the primary constructor that have default values;
2. If the constructor body does not explicitly call a parent class constructor or another constructor of the same class, the parent class's parameterless constructor `super()` is called. If the parent class has no parameterless constructor, an error occurs;
3. Execute the code in the constructor body.

<!-- verify -->

```cangjie
func foo(x: Int64): Int64 {
    println("I'm foo, got ${x}")
    x
}

open class A {
    init() {
        println("I'm A")
    }
}

class B <: A {
    var x = foo(0)
    init() {
        x = foo(1)
        println("init B finished")
    }
}

main() {
    B()
    0
}
```

In the above example, when calling `B`'s constructor, the variable `x` with a default value is initialized first, causing `foo(0)` to be called; then the parent class's parameterless constructor is called, causing `A`'s constructor to be invoked; finally, the code in the constructor body is executed, causing `foo(1)` to be called and a string to be printed. Thus, the output of the example is:

```text
I'm foo, got 0
I'm A
I'm foo, got 1
init B finished
```

If a class definition contains no custom constructors (including primary constructors) and all instance member variables have initial values, a parameterless constructor is automatically generated (calling this constructor creates an object where all instance member variables have their initial values); otherwise, this parameterless constructor is not generated. For example, the following class definition will have an auto-generated parameterless constructor:

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    let height = 20

    /* Auto-generated parameterless constructor:
    public init() {

    }
    */
}

// Invoke the auto-generated parameterless constructor
let r = Rectangle() // r.width = 10，r.height = 20
```

### Class Finalizer

Classes support defining finalizers, which are triggered when an instance of the class is garbage-collected. The finalizer's function name is fixed as `~init` and is typically used to release system resources. The following example uses `unsafe` (details in [Unsafe Section](../FFI/cangjie-c.md)):

<!-- compile -->

```cangjie
class C {
    var p: CString

    init(s: String) {
        p = unsafe { LibC.mallocCString(s) }
        println(s)
    }
    ~init() {
        unsafe { LibC.free(p) }
    }
}
```

There are some restrictions on using finalizers that developers should note:

1. Finalizers have no parameters, no return type, no generic type parameters, no modifiers, and cannot be explicitly called.
2. Classes with finalizers cannot be modified with `open`; only non-`open` classes can have finalizers.
3. A class can define at most one finalizer.
4. Finalizers cannot be defined in extensions.
5. The timing of finalizer execution is indeterminate.
6. Finalizers may execute on any thread.
7. The execution order of multiple finalizers is indeterminate.
8. Throwing uncaught exceptions from finalizers is undefined behavior.
9. Creating threads or using thread synchronization in finalizers is undefined behavior.
10. If an object remains accessible after its finalizer executes, this is undefined behavior.
11. If an object throws an exception during initialization, the finalizer for the incompletely initialized object will not execute.
12. Relying on finalizers for synchronization is undefined behavior. For example, in the following example, the `main` function waits for the finalizer in the `Test` class to modify the value of `t0` via `while (Test.t0 != 0)`, which is undefined behavior.

    <!-- run -->

    ```cangjie
    import std.collection.ArrayList
    import std.runtime.gc

    class Test {
        public static var t0 : Int32 = 0
        public init () {
            t0++
        }
        ~init () {
            t0--
        }
    }

    var list: ArrayList<Test> = ArrayList<Test>()

    func foo() : Int32 {
        let o1 = Test()
        list.add(o1)
        if (Test.t0 != 1) {
            return 1
        }
        list.remove(at: 0)
        return 0
    }

    main(): Int64 {
        var i : Int64 = 0
        while (i < 100) {
            if (foo() != 0) {
                print("fail: obj is freed before gc!")
                return 1
            }
            gc(heavy: true) // blocking gc expected
            // wait ~init() to be executed
            while (Test.t0 != 0) {  // error, this is undefined behavior
                continue
            }
            i++
        }
        return 0
    }
    ```

### Class Member Functions

Class member functions are similarly divided into instance member functions and static member functions (modified with the `static` modifier). Instance member functions can only be accessed through objects, while static member functions can only be accessed through the class type name. Static member functions cannot access instance member variables or call instance member functions, but instance member functions can access static member variables and call static member functions.

In the following example, `area` is an instance member function, and `typeName` is a static member function.

<!-- compile -->

```cangjie
class Rectangle {
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

Instance member functions can be further categorized into abstract member functions and non-abstract member functions based on whether they have a function body. Abstract member functions lack a function body and can only be defined in abstract classes or interfaces (see [Interfaces](interface.md) for details). Note that abstract instance member functions inherently have `open` semantics, where the `open` modifier is optional and must be used with either `public` or `protected` modifiers.

Non-abstract functions must have a function body. Within the function body, instance member variables can be accessed via `this`. For example:

<!-- compile -->

```cangjie
class Rectangle {
    let width: Int64 = 10
    let height: Int64 = 20

    public func area() {
        this.width * this.height
    }
}
```

### Access Modifiers for Class Members

For class members (including member variables, member properties, constructors, and member functions), four access modifiers can be used: `private`, `internal`, `protected`, and `public`. The default is `internal`.

- `private`: Visible only within the class definition.
- `internal`: Visible only within the current package and its sub-packages (including sub-packages of sub-packages; see [Packages](../package/toplevel_access.md)).
- `protected`: Visible within the current module (see [Packages](../package/toplevel_access.md)) and to subclasses of the current class.
- `public`: Visible both inside and outside the module.

<!-- compile.error -error-->

```cangjie
package a

public open class Rectangle {
    public var width: Int64
    protected var height: Int64
    private var area: Int64
    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
        this.area = this.width * this.height
    }
    init(width: Int64, height: Int64, multiple: Int64) {
        this.width = width
        this.height = height
        this.area = width * height * multiple
    }
}

func samePkgFunc() {
    var r = Rectangle(10, 20) // OK: constructor 'Rectangle' can be accessed here
    r.width = 8               // OK: public 'width' can be accessed here
    r.height = 24             // OK: protected 'height' can be accessed here
    r.area = 30               // Error, private 'area' cannot be accessed here
}
```

<!-- compile.error -error-->

```cangjie
package b
import a.*

public class Cuboid <: Rectangle {
    private var length: Int64
    public init(width: Int64, height: Int64, length: Int64) {
        super(width, height)
        this.length = length
    }
    public func volume() {
        this.width * this.height * this.length // OK: protected 'height' can be accessed here
    }
}

main() {
    var r = Rectangle(10, 20, 2) // Error, Rectangle has no `public` constructor with three parameters
    var c = Cuboid(20, 20, 20)
    c.width = 8               // OK: public 'width' can be accessed here
    c.height = 24             // Error, protected 'height' cannot be accessed here
    c.area = 30               // Error, private 'area' cannot be accessed here
}
```

## The `This` Type

Within a class, the `This` type placeholder is supported, representing the current class type. It can only be used as the return type of instance member functions. When a subclass object calls a function defined in the parent class that returns a `This` type, the type of the function call is recognized as the subclass type, not the parent class type where it was defined.

If an instance member function does not declare a return type and only contains expressions returning `This`, the function's return type is inferred as `This`. Example:

<!-- compile -->

```cangjie
open class C1 {
    func f(): This {  // its type is `() -> C1`
        return this
    }

    func f2() { // its type is `() -> C1`
        return this
    }

    public open func f3(): C1 {
        return this
    }
}
class C2 <: C1 {
    // member function f is inherited from C1, and its type is `() -> C2` now
    public override func f3(): This { // OK
        return this
    }
}

main() {
    var obj1: C2 = C2()
    var obj2: C1 = C2()

    var x = obj1.f()    // During compilation, the type of x is C2
    var y = obj2.f()    // During compilation, the type of y is C1
}
```

## Creating Objects

After defining a `class` type, objects can be created by calling its constructor (via the class type name). For example, in the following code, `Rectangle(10, 20)` creates an object of type `Rectangle` and assigns it to variable `r`. After creation, (`public`-modified) instance member variables and instance member functions can be accessed through the object. For example, `r.width` and `r.height` access the values of `width` and `height` in `r`, respectively, and `r.area()` calls the member function `area`.

<!-- compile -->

```cangjie
class Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func area() {
        this.width * this.height
    }
}

main() {
    let r = Rectangle(10, 20) // r.width = 10, r.height = 20
    let width = r.width       // width = 10
    let height = r.height     // height = 20
    let a = r.area()          // a = 200
}
```

If you wish to modify member variable values through objects (not recommended; it's better to modify them via member functions), the member variables in the `class` must be defined as mutable (using `var`). Example:

<!-- run -->

```cangjie
class Rectangle {
   public var width: Int64
   public var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }
    public func area() {
        width * height
    }
}

main() {
    let r = Rectangle(10, 20) // r.width = 10, r.height = 20
    r.width = 8               // r.width = 8
    r.height = 24             // r.height = 24
    let a = r.area()          // a = 192
}
```

Unlike `struct`, when objects are assigned or passed as parameters, they are not copied. Multiple variables point to the same object, so modifying a member through one variable affects the corresponding member in other variables. For example, in the following code, after assigning `r1` to `r2`, modifying `r1.width` and `r1.height` also changes `r2.width` and `r2.height`.

<!-- run -->

```cangjie
class Rectangle {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }
     public func area() {
        this.width * this.height
    }
}
main() {
    var r1 = Rectangle(10, 20) // r1.width = 10, r1.height = 20
    var r2 = r1                // r2.width = 10, r2.height = 20
    r1.width = 8               // r1.width = 8
    r1.height = 24             // r1.height = 24
    let a1 = r1.area()         // a1 = 192
    let a2 = r2.area()         // a2 = 192
}
```

## Class Inheritance

Like most programming languages that support `class`, Cangjie's `class` also supports inheritance. If class B inherits from class A, A is called the parent class, and B is called the child class. The child class inherits all members of the parent class except `private` members and constructors.

Abstract classes are always inheritable, so the `open` modifier for abstract class definitions is optional. Alternatively, an abstract class can be modified with `sealed`, indicating it can only be inherited within its package. However, non-abstract classes can only be inherited if they are defined with the `open` modifier. When an `open`-modified instance member is inherited by a class, the `open` modifier is also inherited. If a non-`open` class contains `open` members, the compiler will issue a warning.

The parent class can be specified in the child class definition using `<:`, but the parent class must be inheritable. For example, in the following code, class A is modified with `open`, so it can be inherited by class B. However, since class B is not inheritable, C will report an error when attempting to inherit from B.

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

class B <: A { // OK: 'B' Inheritance 'A'
    let b: Int64 = 20
}

class C <: B { // Error, 'B' is not inheritable
    let c: Int64 = 30
}
```

`class` supports only single inheritance, so the following code attempting to inherit from two classes is invalid (`&` is syntax for implementing multiple interfaces; see [Interfaces](interface.md)).

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

open class B {
    let b: Int64 = 20
}

class C <: A & B { // Error, 'C' can only inherit one class
    let c: Int64 = 30
}
```

Because classes support only single inheritance, any class can have at most one direct parent class. For classes defined with a parent class, the direct parent is the specified class. For classes defined without a parent class, the direct parent is the `Object` type. `Object` is the parent of all classes (note: `Object` has no direct parent and contains no members).

Because child classes inherit from parent classes, child class objects can naturally be used as parent class objects, but the reverse is not true. For example, in the following code, B is a child of A, so a B-type object can be assigned to an A-type variable, but an A-type object cannot be assigned to a B-type variable.

<!-- compile -->

```cangjie
open class A {
    let a: Int64 = 10
}
class B <: A {
    let b: Int64 = 20
}

let a: A = B() // OK: subclass objects can be assigned to superclass variables
```

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

class B <: A {
    let b: Int64 = 20
}

let b: B = A() // Error, superclass objects can not be assigned to subclass variables
```

The `class` defined type does not allow inheriting from itself.

<!-- compile.error -->

```cangjie
class A <: A {}  // Error, 'A' inherits itself
```

Abstract classes can use the `sealed` modifier, indicating that the modified class definition can only be inherited by other classes within the same package where the definition resides. The `sealed` modifier already implies `public`/`open` semantics. Therefore, when defining a sealed abstract class, if `public`/`open` modifiers are provided, the compiler will issue a warning. Subclasses of `sealed` classes do not have to be `sealed` themselves and can still be modified with `open`/`sealed` or use no inheritance modifiers at all. If a subclass of a `sealed` class is modified with `open`, then its subclasses can be inherited outside the package. Subclasses of `sealed` classes do not need to be modified with `public`.

<!-- compile -->

```cangjie
package A

public sealed abstract class C1 {}   // Warning, redundant modifier, 'sealed' implies 'public'
sealed open abstract class C2 {}     // Warning, redundant modifier, 'sealed' implies 'open'
sealed abstract class C3 {}          // OK, 'public' is optional when 'sealed' is used

class S1 <: C1 {}  // OK
public open class S2 <: C1 {}   // OK
public sealed abstract class S3 <: C1 {}  // OK
open class S4 <: C1 {}   // OK
```

<!-- compile.error -->

```cangjie
package B
import A.*

class SS1 <: S2 {}  // OK
class SS2 <: S3 {}  // Error, S3 is sealed class, cannot be inherited here
sealed class SS3 {} // Error, 'sealed' cannot be used on non-abstract class
```

### Superclass Constructor Invocation

The `init` constructor of a subclass can call the superclass constructor using the form `super(args)`, or call another constructor of the same class using `this(args)`, but only one of them can be called. If called, it must be the first expression in the constructor body, with no preceding expressions or declarations allowed.

<!-- compile -->

```cangjie
open class A {
    A(let a: Int64) {}
}

class B <: A {
    let b: Int64
    init(b: Int64) {
        super(30)
        this.b = b
    }

    init() {
        this(20)
    }
}
```

In the primary constructor of a subclass, the superclass constructor can be called using `super(args)`, but other constructors of the same class cannot be called using `this(args)`.

If a subclass constructor does not explicitly call a superclass constructor or another constructor, the compiler will insert a call to the parameterless constructor of the direct superclass at the beginning of the constructor body. If the superclass does not have a parameterless constructor, a compilation error will occur.

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64
    init() {
        a = 100
    }
}

open class B <: A {
    let b: Int64
    init(b: Int64) {
        // OK, `super()` added by compiler
        this.b = b
    }
}

open class C <: B {
    let c: Int64
    init(c: Int64) {  // Error, there is no non-parameter constructor in super class
        this.c = c
    }
}
```

### Overriding and Redefinition

In a subclass, non-abstract instance member functions with the same name as those in the parent class can be overridden, meaning new implementations can be defined for these functions in the subclass. When overriding, the member function in the parent class must be modified with `open`, and the function in the subclass must be modified with `override`, where `override` is optional. For example, in the following example, the function `f` in subclass B overrides the function `f` in parent class A.

<!-- verify -->

```cangjie
open class A {
    public open func f(): Unit {
        println("I am superclass")
    }
}

class B <: A {
    public override func f(): Unit {
        println("I am subclass")
    }
}

main() {
    let a: A = A()
    let b: A = B()
    a.f()
    b.f()
}
```

For overridden functions, the version called is determined by the runtime type of the variable (determined by the actual object assigned to the variable), known as dynamic dispatch. For example, in the above example, the runtime type of `a` is A, so `a.f()` calls the function `f` in parent class A; the runtime type of `b` is B (compile-time type is A), so `b.f()` calls the function `f` in subclass B. Therefore, the program will output:

```text
I am superclass
I am subclass
```

For static functions, non-abstract static functions with the same name as those in the parent class can be redefined in the subclass, meaning new implementations can be defined for these functions in the subclass. When redefining, the static function in the subclass must be modified with `redef`, where `redef` is optional. For example, in the following example, the function `foo` in subclass D redefines the function `foo` in parent class C.

<!-- verify -->

```cangjie
open class C {
    public static func foo(): Unit {
        println("I am class C")
    }
}

class D <: C {
    public redef static func foo(): Unit {
        println("I am class D")
    }
}

main() {
    C.foo()
    D.foo()
}
```

For redefined functions, the version called is determined by the type of the `class`. For example, in the above example, `C.foo()` calls the function `foo` in parent class C, and `D.foo()` calls the function `foo` in subclass D.

```text
I am class C
I am class D
```

If an abstract function or a function modified with `open` has named parameters, the implementing function or the function modified with `override` must maintain the same named parameters.

<!-- compile.error -->

```cangjie
open class A {
    public open func f(a!: Int32): Int32 {
        a + 1
    }
}

class B <: A {
    public override func f(a!: Int32): Int32 { // OK
        a + 2
    }
}

class C <: A {
    public override func f(b!: Int32): Int32 { // Error
        b + 3
    }
}

main() {
    B().f(a: 0)
    C().f(b: 0)
}
```

It is also important to note that when implementing or redefining a generic function, the type parameter constraints of the subtype function must be looser or the same as those of the corresponding function in the parent type.

<!-- compile.error -->

```cangjie
open class A {}
open class B <: A {}
open class C <: B {}

open class Base {
    public open func foo<T>(a: T): Unit where T <: B {}
    public open func bar<T>(a: T): Unit where T <: B {}
    public static func f<T>(a: T): Unit where T <: B {}
    public static func g<T>(): Unit where T <: B {}
}

class D <: Base {
    public override func foo<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public override func bar<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public redef static func f<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public redef static func g<T>(): Unit where T <: C {} // Error, stricter constraint
}

class E <: Base {
    public override func foo<T>(a: T): Unit where T <: A {} // OK: looser constraint
    public override func bar<V>(a: V): Unit where V <: A {} // OK: looser constraint, names of generic parameters do not matter
    public redef static func f<T>(a: T): Unit where T <: A {} // OK: looser constraint
    public redef static func g<T>(): Unit where T <: A {} // OK: looser constraint
}

class F <: Base {
    public override func foo<T>(a: T): Unit where T <: B {} // OK: same constraint
    public override func bar<V>(a: V): Unit where V <: B {} // OK: same constraint
    public redef static func f<T>(a: T): Unit where T <: B {} // OK: same constraint
    public redef static func g<T>(): Unit where T <: B {} // OK: same constraint
}
```