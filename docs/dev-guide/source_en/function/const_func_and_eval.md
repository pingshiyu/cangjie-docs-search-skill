# const Functions and Constant Evaluation

Constant evaluation allows certain forms of expressions to be evaluated at compile time, reducing the computational load required during program execution. This chapter primarily introduces the usage methods and rules of constant evaluation.

## `const` Context and `const` Expressions

A `const` context refers to the initialization expression of a `const` variable, where these expressions are always evaluated at compile time. Therefore, restrictions must be placed on the expressions allowed in `const` contexts to avoid side effects such as modifying global state or performing I/O operations, ensuring they can be evaluated at compile time.

A `const` expression possesses the capability to be evaluated at compile time. Expressions that satisfy the following rules are considered `const` expressions:

1. Literals of numeric types, `Bool`, `Unit`, `Rune`, and `String` types (excluding interpolated strings).
2. `Array` literals (not `Array` type, but `VArray` type can be used) and `tuple` literals where all elements are `const` expressions.
3. `const` variables, `const` function parameters, and local variables within `const` functions.
4. `const` functions, including functions declared with `const`, `lambda` expressions that meet `const` function requirements, and function expressions returned by these functions.
5. `const` function calls (including `const` constructors), where the function expression must be a `const` expression and all arguments must be `const` expressions.
6. `enum` constructor calls where all arguments are `const` expressions, and parameterless `enum` constructors.
7. Arithmetic expressions, relational expressions, and bitwise operation expressions of numeric types, `Bool`, `Unit`, `Rune`, and `String` types, where all operands must be `const` expressions.
8. `if`, `match`, `try`, `throw`, `return`, `is`, and `as` expressions, where all internal expressions must be `const` expressions.
9. Member access of `const` expressions (excluding property access) and index access of `tuple`.
10. `const init` and `this` and `super` expressions within `const` functions.
11. `const` instance member function calls of `const` expressions, where all arguments must be `const` expressions.

> **Note:**
>
> The current compiler implementation does not support using `throw` as a `const` expression.

## `const` Functions

`const` functions are a special category of functions that possess the capability to be evaluated at compile time. When these functions are called in a `const` context, they are executed during compilation. In other non-`const` contexts, `const` functions behave like ordinary functions and are executed at runtime.

The following example demonstrates a `const` function that calculates the distance between two points on a plane. The `distance` function uses `let` to define two local variables, `dx` and `dy`:

<!-- verify -->

```cangjie
struct Point {
    const Point(let x: Float64, let y: Float64) {}
}

const func distance(a: Point, b: Point) {
    let dx = a.x - b.x
    let dy = a.y - b.y
    (dx ** 2 + dy ** 2) ** 0.5
}

main() {
    const a = Point(3.0, 0.0)
    const b = Point(0.0, 4.0)
    const d = distance(a, b)
    println(d)
}
```

Compilation and execution output:

```text
5.000000
```

Key points to note:

1. `const` function declarations must be marked with the `const` modifier.
2. Global `const` functions and `static const` functions can only access externally declared `const` variables, including `const` global variables and `const` static member variables. Other external variables are inaccessible. `const init` functions and `const` instance member functions can access not only `const`-declared external variables but also instance member variables of the current type.
3. All expressions within `const` functions must be `const` expressions, except for `const init` functions.
4. `const` functions can use `let` and `const` to declare new local variables but do not support `var`.
5. There are no special restrictions on the parameter types and return types of `const` functions. If the arguments of a function call do not meet the requirements of a `const` expression, the function call cannot be used as a `const` expression but can still be used as an ordinary expression.
6. `const` functions are not necessarily executed at compile time; for example, they can be called at runtime within non-`const` functions.
7. The overloading rules for `const` functions and non-`const` functions are consistent.
8. Numeric types, `Bool`, `Unit`, `Rune`, `String` types, and `enum` support defining `const` instance member functions.
9. For `struct` and `class`, `const` instance member functions can only be defined if `const init` is defined. `const` instance member functions in `class` cannot be `open`. `const` instance member functions in `struct` cannot be `mut`.

Additionally, interfaces can also define `const` functions, but they are subject to the following rules:

1. For `const` functions in an interface, the implementing type must also use `const` functions to satisfy the interface.
2. For non-`const` functions in an interface, the implementing type can use either `const` or non-`const` functions to satisfy the interface.
3. Similar to `static` functions in interfaces, `const` functions in interfaces can only be used by generic parameters or variables constrained by the interface when the interface is used as a generic constraint.

In the following example, two `const` functions are defined in interface `I`, class `A` implements interface `I`, and the generic function `g` has a type parameter upper-bounded by `I`.

<!-- verify -->

```cangjie
interface I {
    const func f(): Int64
    const static func f2(): Int64
}

class A <: I {
    public const func f() { 0 }
    public const static func f2() { 1 }
    const init() {}
}

const func g<T>(i: T) where T <: I {
    return i.f() + T.f2()
}

main() {
    println(g(A()))
}
```

Compiling and executing the above code outputs:

```text
1
```

## `const init`

If a `struct` or `class` defines a `const` constructor, then instances of that `struct`/`class` can be used in `const` expressions.

1. If the current type is a `class`, it cannot have instance member variables declared with `var`; otherwise, defining `const init` is not allowed. If the current type has a superclass, the `const init` must call the superclass's `const init` (either explicitly or implicitly by calling a parameterless `const init`). If the superclass does not have a `const init`, an error is raised.

    <!-- compile.error -->

    ```cangjie
    public class Foo {
        val a: Int64 = 9 // Error, expected declaration, found 'val'
        let b: String
        const init(b: String) {
            this.b = b
        }
    }
    ```

    <!-- compile.error -->

    ```cangjie
    open public class Boo {
        let boo: String
        const init(b: String) {
            this.boo = b
        }
    }

    public class Foo <: Boo {
        let c: String
        const init(c: String) { //Error, there is no non-parameter constructor in super class, please invoke super call explicitly
            this.c = c
        }
    }
    ```

2. If the instance member variables of the current type have initial values, those initial values must be `const` expressions; otherwise, defining `const init` is not allowed.

    <!-- compile.error -->

    ```cangjie
    var a = "4123"

    class Foo {
        let foo: String = a // Error, expected 'const' expression guaranteed to be evaluated at compile time
        const init() {}
    }
    ```

3. Within `const init`, assignment expressions (`=`) can be used to assign values to instance member variables, but no other assignment expressions (such as `+=`, `-=`) are allowed.

    <!-- compile.error -->

    ```cangjie
    var a = "4123"

    class Foo {
        let foo: String
        let boo: Int64
        const init() {
            foo = "aa" // OK
            boo += 10 // Error, variable 'boo' is used before initialization
        }
    }
    ```

The difference between `const init` and `const` functions is that `const init` allows assignment to instance member variables (using assignment expressions).