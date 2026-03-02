# The Nothing Type

`Nothing` is a special type that contains no values, and the `Nothing` type is a subtype of all types (including the [`Unit` type](unit.md)).

The `break`, `continue`, `return`, and `throw` expressions are of type `Nothing`. When program execution reaches these expressions, the code following them will not be executed. `return` can only be used within a function body, while `break` and `continue` can only be used within loop bodies. Refer to the following example:

<!-- compile.error -->

```cangjie
while (true) {
    func f() {
        break // Error, break must be used directly inside a loop
    }
    let g = { =>
        continue // Error, continue must be used directly inside a loop
    }
}
```

Since function parameters and their default values do not belong to the function body, the `return` expression in the following example lacks an enclosing function body—it neither belongs to the outer function `f` (because the inner function definition `g` has already started) nor is it within the inner function `g`'s body (for related content on this use case, refer to [Nested Functions](../function/nested_functions.md)):

<!-- compile.error -->

```cangjie
func f() {
    func g(x!: Int64 = return) { // Error, return must be used inside a function body
        0
    }
    1
}
```

> **Note:**
>
> Currently, the compiler does not allow explicit use of the `Nothing` type in places where types are required.