# Defining Functions

In Cangjie, the keyword `func` is used to denote the start of a function definition. Following `func` are the function name, parameter list, optional return type, and function body in sequence. The function name can be any valid identifier. The parameter list is enclosed in parentheses (with multiple parameters separated by commas), a colon separates the parameter list from the return type (if present), and the function body is enclosed in curly braces.

Example of a function definition:

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    return a + b
}
```

The above example defines a function named `add` with a parameter list consisting of two `Int64` parameters `a` and `b`, a return type of `Int64`, and a function body that returns the sum of `a` and `b`.

The following sections provide further details on the parameter list, return type, and function body in function definitions.

## Parameter List

A function can have zero or more parameters, all defined in the parameter list. Parameters in the parameter list can be categorized into two types based on whether parameter names are required during function calls: non-named parameters and named parameters.

Non-named parameters are defined as `p: T`, where `p` is the parameter name and `T` is the type of parameter `p`, connected by a colon. For example, the parameters `a` and `b` in the `add` function above are non-named parameters.

Named parameters are defined as `p!: T`, differing from non-named parameters by the addition of `!` after the parameter name `p`. The non-named parameters in the `add` function can be modified to named parameters as shown below:

<!-- compile -->

```cangjie
func add(a!: Int64, b!: Int64): Int64 {
    return a + b
}
```

Named parameters can also have default values, specified via `p!: T = e`, where the default value of parameter `p` is set to the value of expression `e`. For example, the default values of the two parameters in the `add` function can be set to `1`:

<!-- compile -->

```cangjie
func add(a!: Int64 = 1, b!: Int64 = 1): Int64 {
    return a + b
}
```

> **Note:**
>
> Only named parameters can have default values; non-named parameters cannot.

A parameter list can include both non-named and named parameters. However, non-named parameters must be defined before named parameters, meaning no non-named parameters can appear after named parameters. For example, the following parameter list definition for the `add` function is invalid:

<!-- compile.error -->

```cangjie
func add(a!: Int64, b: Int64): Int64 { // Error, named parameter 'a' must be defined after non-named parameter 'b'
    return a + b
}
```

The primary difference between non-named and named parameters lies in their behavior during function calls. For details, refer to the [Calling Functions](./call_functions.md) section below.

Function parameters are immutable variables and cannot be assigned values within the function definition.

<!-- compile.error -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a = a + b // Error
    return a
}
```

The scope of function parameters extends from their definition to the end of the function body:

<!-- compile.error -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    var a_ = a // OK
    var b = b  // Error, redefinition of declaration 'b'
    return a
}
```

## Return Type

The return type of a function is the type of the value obtained when the function is called. In function definitions, the return type is optional: it can be explicitly defined (placed between the parameter list and the function body) or omitted, leaving it to the compiler to infer.

When the return type is explicitly defined, the type of the function body (see the [Function Body](./define_functions.md#函数体) section below for how the function body type is determined) and the types of all `return e` expressions in the function body must be subtypes of the return type. For example, in the `add` function above, the return type is explicitly defined as `Int64`. If the function body is modified to `return (a, b)`, a type mismatch error will occur:

<!-- compile.error -->

```cangjie
// Error, the type of the expression after return does not match the return type of the function
func add(a: Int64, b: Int64): Int64 {
    return (a, b)
}
```

If the return type is not explicitly defined in the function definition, the compiler infers it based on the type of the function body and all `return` expressions in the function body. For example, in the following `add` function, the return type is omitted, but the compiler can infer it as `Int64` from `return a + b`:

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    return a + b
}
```

> **Note:**
>
> The return type of a function cannot always be inferred. If type inference fails, the compiler will report an error.
>
> When the return type is specified as `Unit`, the compiler automatically inserts `return ()` at all possible return points in the function body, ensuring the return type is always `Unit`.

## Function Body

The function body defines the operations executed when the function is called. It typically consists of a series of variable definitions and expressions and can also include nested function definitions. For example, the function body of the `add` function below first defines a variable `r` of type `Int64` (initialized to `0`), assigns the value of `a + b` to `r`, and finally returns `r`:

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}
```

A `return` expression can be used anywhere in the function body to terminate the function's execution and return a value. There are two forms of `return` expressions: `return` and `return expr` (where `expr` is an expression).

For `return expr`, the type of `expr` must match the function's return type. For example, the following example will error because the type of `100` (`Int64`) does not match the return type of function `foo` (`String`):

<!-- compile.error -->

```cangjie
// Error, cannot convert an integer literal to type 'Struct-String'
func foo(): String {
    return 100
}
```

For `return`, it is equivalent to `return ()`, so the function's return type must be `Unit`.

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}

func foo(): Unit {
    add(1, 2)
    return
}
```

> **Note:**
>
> The `return` expression as a whole has the type `Nothing`, regardless of the expression that follows it.

Variables defined within the function body are a type of local variable (e.g., variable `r` in the example above). Their scope extends from their definition to the end of the function body.

For a local variable, it is allowed to define a variable with the same name in an outer scope. Within the local variable's scope, the local variable will "shadow" the variable of the same name in the outer scope. For example:

<!-- compile -->

```cangjie
let r = 0
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}
```

In the example above, a global variable `r` of type `Int64` is defined before the `add` function, and a local variable `r` with the same name is defined within the function body. Within the function body, all references to `r` (e.g., `r = a + b`) will refer to the local variable `r`, meaning the local variable `r` "shadows" the global variable `r` within the function body.

As mentioned in the [Return Type](./define_functions.md#函数返回值类型) section, the function body also has a type. The type of the function body is the type of the last "item" in the function body: if the last item is an expression, the function body's type is the type of that expression; if the last item is a variable definition, function declaration, or the function body is empty, the function body's type is `Unit`. For example:

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a + b
}
```

In the example above, since the last "item" in the function body is an expression of type `Int64` (i.e., `a + b`), the function body's type is also `Int64`, matching the function's return type. Similarly, in the following example, the last item in the function body is a call to the `print` function, so the function body's type is `Unit`, which also matches the function's return type:

<!-- compile -->

```cangjie
func foo(): Unit {
    let s = "Hello"
    print(s)
}
```