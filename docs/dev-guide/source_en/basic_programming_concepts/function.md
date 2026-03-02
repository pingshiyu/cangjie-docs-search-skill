# Functions

In Cangjie, the keyword `func` is used to denote the start of a function definition. Following `func` are the function name, parameter list, optional return type, and function body. The function name can be any valid identifier. The parameter list is enclosed in parentheses (with multiple parameters separated by commas), a colon separates the parameter list and the return type (if present), and the function body is enclosed in curly braces.

Example of a function definition:

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    return a + b
}
```

In the above example, a function named `add` is defined. Its parameter list consists of two `Int64` parameters, `a` and `b`, and its return type is `Int64`. The function body adds `a` and `b` together and returns the result.

For more details, refer to the [Defining Functions](../function/define_functions.md) module.