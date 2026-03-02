# Function Invocation

A function is invoked in the form `f(arg1, arg2, ..., argn)`, where `f` is the name of the function to be called, and `arg1` through `argn` are the `n` arguments (called actual parameters) passed during invocation. Each actual parameter's type must be a subtype of the corresponding parameter's type. The number of actual parameters can range from zero to multiple. When there are zero parameters, the invocation takes the form `f()`.

Depending on whether the parameters in the function definition are positional or named, the way arguments are passed during invocation differs:

- For positional parameters, the corresponding argument is an expression.
- For named parameters, the argument must be passed in the form `p: e`, where `p` is the name of the named parameter and `e` is the expression (i.e., the value passed to parameter `p`).

Example of positional parameter invocation:

<!-- verify -->

```cangjie
func add(a: Int64, b: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(x, y)
    println("The sum of x and y is ${r}")
}
```

Execution result:

```text
The sum of x and y is 3
```

Example of named parameter invocation:

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(x, b: y)
    println("The sum of x and y is ${r}")
}
```

Execution result:

```text
The sum of x and y is 3
```

For functions with multiple named parameters, the order of passing arguments during invocation can differ from the parameter order in the definition. For example, in the following case, parameter `b` can appear before `a` when invoking the `add` function:

<!-- verify -->

```cangjie
func add(a!: Int64, b!: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(b: y, a: x)
    println("The sum of x and y is ${r}")
}
```

Execution result:

```text
The sum of x and y is 3
```

For named parameters with default values, if no argument is passed during invocation, the parameter will use its default value. For example, in the following case, when invoking the `add` function, no argument is passed for parameter `b`, so its value defaults to `2` as defined:

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64 = 2) {
    return a + b
}

main() {
    let x = 1
    let r = add(x)
    println("The sum of x and y is ${r}")
}
```

Execution result:

```text
The sum of x and y is 3
```

For named parameters with default values, new arguments can also be passed during invocation. In this case, the parameter's value will be the new argument's value, overriding the default. For example, in the following case, when invoking the `add` function, a new argument value `20` is passed for parameter `b`, so its value becomes `20`:

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64 = 2) {
    return a + b
}

main() {
    let x = 1
    let r = add(x, b: 20)
    println("The sum of x and y is ${r}")
}
```

Execution result:

```text
The sum of x and y is 21
```