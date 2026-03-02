# Nested Functions

Functions defined at the top level of a source file are called global functions. Functions defined within the body of another function are called nested functions.

**Scope of Usage**:

- The scope of a nested function is limited to its enclosing outer function. Nested functions can access variables and parameters of the outer function, but the outer function cannot directly access the internal variables of nested functions.
- Nested functions can be called by the outer function or returned by the outer function.

**Lifecycle**:

- The lifecycle of a nested function is closely tied to its outer function. Each time the outer function is called, the nested function is created; when the outer function completes execution, the nested function is typically destroyed unless it is externally referenced through return values or closures.

**Usage Rules and Considerations**:

- Use nested functions only within their corresponding outer functions.
- Avoid excessive nesting. This can complicate code structure, making it difficult to understand and maintain. Therefore, avoid excessive nesting that leads to code confusion.
- Be mindful of closure usage. If a nested function is returned and used as a closure, note that the closure may capture variables from the outer function, causing these variables to remain occupied even after the outer function completes, thereby affecting memory management.

**Example**: The function `foo` defines a nested function `nestAdd` inside it. The nested function `nestAdd` can be called within `foo`, or it can be returned as a value to be called outside `foo`:

<!-- verify -->

```cangjie
func foo() {
    func nestAdd(a: Int64, b: Int64) {
        a + b + 3
    }

    println(nestAdd(1, 2))  // 6

    return nestAdd
}

main() {
    let f = foo()
    let x = f(1, 2)
    println("result: ${x}")
}
```

The program will output:

```text
6
result: 6
```