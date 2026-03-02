# Operator Overloading

If you want to support operators that are not natively supported by a certain type, you can achieve this through operator overloading.

To overload an operator for a type, you can define a function with the operator's name for that type. When an instance of this type uses the operator, the corresponding operator function will be automatically called.

The definition of an operator function is similar to that of a regular function, with the following differences:

- The `operator` modifier must be added before the `func` keyword when defining an operator function.
- The number of parameters in the operator function must match the requirements of the corresponding operator (see Appendix [Operators](../Appendix/operator.md) for details).
- Operator functions can only be defined within `class`, `interface`, `struct`, `enum`, and `extend`.
- Operator functions have the semantics of instance member functions, so the `static` modifier is prohibited.
- Operator functions cannot be generic functions.

Additionally, it's important to note that overloaded operators do not change their inherent precedence and associativity (see Appendix [Operators](../Appendix/operator.md) for details).

## Definition and Usage of Operator Overloading Functions

There are two ways to define operator functions:

1. For types that can directly contain function definitions (including `struct`, `enum`, `class`, and `interface`), operator functions can be defined directly within them to overload operators.
2. Use the `extend` approach to add operator functions, thereby overloading operators for these types. For types that cannot directly contain function definitions (i.e., types other than `struct`, `class`, `enum`, and `interface`) or types whose implementations cannot be modified (such as third-party defined `struct`, `class`, `enum`, and `interface`), this is the only available method (see [Extensions](../extension/extend_overview.md)).

The conventions for parameter types in operator functions are as follows:

1. For unary operators, the operator function takes no parameters, and there are no requirements on the return type.

2. For binary operators, the operator function takes exactly one parameter, and there are no requirements on the return type.

   The following example demonstrates the definition and usage of unary and binary operators:

   The `-` operator negates the `x` and `y` member variables of a `Point` instance and returns a new `Point` object. The `+` operator sums the `x` and `y` member variables of two `Point` instances and returns a new `Point` object.

    <!-- run -overloadOperater -->

    ```cangjie
    open class Point {
        var x: Int64 = 0
        var y: Int64 = 0
        public init (a: Int64, b: Int64) {
            x = a
            y = b
        }

        public operator func -(): Point {
            Point(-x, -y)
        }
        public operator func +(right: Point): Point {
            Point(this.x + right.x, this.y + right.y)
        }
    }
    ```

   Now, the unary `-` operator and binary `+` operator can be used directly on instances of `Point`:

    <!-- run -overloadOperater -->

    ```cangjie
    main() {
        let p1 = Point(8, 24)
        let p2 = -p1      // p2 = Point(-8, -24)
        let p3 = p1 + p2  // p3 = Point(0, 0)
    }
    ```

3. The index operator (`[]`) has two forms: value retrieval (`let a = arr[i]`) and value assignment (`arr[i] = a`). These are distinguished by the presence or absence of a special named parameter `value`. Overloading the index operator does not require overloading both forms simultaneously; you can overload only the assignment form or only the retrieval form.

   For the value retrieval form of the index operator `[]`, the parameter sequence inside the brackets corresponds to the non-named parameters of the operator overload. There can be one or more parameters of any type. No other named parameters are allowed. The return type can be any type.

    <!-- compile -->

    ```cangjie
    class A {
        operator func [](arg1: Int64, arg2: String): Int64 {
            return 0
        }
    }

    func f() {
        let a = A()
        let b: Int64 = a[1, "2"]
        // b == 0
    }
    ```

   For the value assignment form of the index operator `[]`, the parameter sequence inside the brackets corresponds to the non-named parameters of the operator overload. There can be one or more parameters of any type. The expression on the right side of `=` corresponds to the named parameter of the operator overload. There must be exactly one named parameter, and its name must be `value`. It cannot have a default value, and `value` can be of any type. The return type must be `Unit`.

   Note that `value` is just a special marker; you do not need to use named parameter syntax when calling the index operator for assignment.

    <!-- compile -->

    ```cangjie
    class A {
        operator func [](arg1: Int64, arg2: String, value!: Int64): Unit {
            return
        }
    }

    func f() {
        let a = A()
        a[1, "2"] = 0
    }
    ```

   Notably, immutable types (except `enum`) do not support overloading the assignment form of the index operator.

4. The function call operator (`()`) overload function can have input parameters and return values of any type. Example:

    <!-- compile -->

    ```cangjie
    open class A {
        public init() {}

        public operator func ()(): Unit {}
    }

    func test1() {
        let a = A() // OK, A() is call the constructor of A
        a()         // OK, a() is to call the operator () overloading function
    }
    ```

   You cannot use `this` or `super` to call the `()` operator overload function. Example:

    <!-- compile.error -->

    ```cangjie
    open class A {
        public init() {}
        public init(x: Int64) {
            this() // OK, this() calls the constructor of A
        }

        public operator func ()(): Unit {}

        public func foo() {
            this()  // Error, this() calls the constructor of A.
            super() // Error
        }
    }

    class B <: A {
        public init() {
            super() // OK, super()  calls the constuctor of the super class
        }

        public func goo() {
            super() // Error
        }
    }
    ```

   For enumeration types, when both the constructor form and the `()` operator overload function form are applicable, the constructor form takes precedence. Example:

    <!-- compile -->

    ```cangjie
    enum E {
        Y | X | X(Int64)

        public operator func ()(p: Int64) {}
        public operator func ()(p: Float64) {}
    }

    main() {
        let e = X(1)    // OK, X(1) is to call the constructor X(Int64)
        X(1.0)          // OK, X(1.0) is to call the operator () overloading function
        let e1 = X
        e1(1)           // OK, e1(1) is to call the operator () overloading function
        Y(1)            // OK, Y(1) is to call the operator () overloading function
    }
    ```

## Overloadable Operators

The following table lists all overloadable operators (ordered by precedence from highest to lowest):

| Operator            | Description           |
|:--------------------|:----------------------|
| `()`                | Function call         |
| `[]`                | Indexing              |
| `!`                 | NOT                   |
| `-`                 | Negative              |
| `**`                | Power                 |
| `*`                 | Multiply              |
| `/`                 | Divide                |
| `%`                 | Remainder             |
| `+`                 | Add                   |
| `-`                 | Subtract              |
| `<<`                | Bitwise left shift    |
| `>>`                | Bitwise right shift   |
| `<`                 | Less than             |
| `<=`                | Less than or equal    |
| `>`                 | Greater than          |
| `>=`                | Greater than or equal |
| `==`                | Equal                 |
| `!=`                | Not equal             |
| `&`                 | Bitwise AND           |
| `^`                 | Bitwise XOR           |
| <code>&vert;</code> | Bitwise OR            |

Important notes:

> **Note:**
>
> - If any binary operator other than relational operators (`<`, `<=`, `>`, `>=`, `==`, and `!=`) is overloaded for a type, and the return type of the operator function matches the type of the left operand or is a subtype of it, then the type supports the corresponding compound assignment operator. If the return type does not match the left operand's type and is not a subtype, using the corresponding compound assignment operator will result in a type mismatch error.
>   <!-- compile.error -->
>
>   ```cangjie
>   open class MyClass {
>       var x: Int64 = 0
>       public init (a: Int64) {
>           x = a
>       }
>
>       public operator func +(right: MyClass): Int64 { // The above rules are not met
>           this.x + right.x
>       }
>   }
>
>   main() {
>       var a = MyClass(5)
>       var b = MyClass(3)
>       a += b; // Error, type incompatible in this compound assignment expression
>   }
>   ```
>
> - The Cangjie programming language does not support custom operators. Defining operator functions other than those listed in the above table is not allowed.
> - For a type `T`, if `T` already natively supports certain overloadable operators, attempting to redefine operator functions with the same signature via extension will result in a redefinition error. For example, overloading arithmetic operators, bitwise operators, or relational operators with the same signature for numeric types, overloading relational operators with the same signature for `Rune`, or overloading logical operators, equality, or inequality operators with the same signature for `Bool` will all trigger redefinition errors.
>   <!-- compile.error -->
>
>   ```cangjie
>   extend Int64 {
>       public operator func +(x: Int64, y: Int64): Int64 { // Error, invalid number of parameters for operator '+'
>           x + y
>       }
>   }
>   ```