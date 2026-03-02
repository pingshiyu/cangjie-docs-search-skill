# Tuple Type

A tuple (Tuple) can combine multiple different types into a new type. The tuple type is denoted as `(T1, T2, ..., TN)`, where `T1` to `TN` can be any type, and different types are connected by commas (`,`). A tuple must be at least binary. For example, `(Int64, Float64)` represents a binary tuple type, and `(Int64, Float64, String)` represents a ternary tuple type.

The length of a tuple is fixed, meaning once an instance of a tuple type is defined, its length cannot be changed.

The tuple type is immutable, meaning once an instance of a tuple type is defined, its content (i.e., individual elements) cannot be updated. However, the entire tuple can be overwritten or replaced, for example:

<!-- compile.error -->

```cangjie
let tuple1 = (8, false)
var tuple2 = (true, 9, 20)
tuple2 = tuple1         // Error, mismatched types
tuple2[0] = false       // Error, 'tuple element' can not be assigned

var tuple3 = (9, true)
tuple3 = tuple1
println(tuple3[0])      // 8
println(tuple3[1])      // false
```

## Tuple Type Literals

The literal of a tuple type is denoted as `(e1, e2, ..., eN)`, where `e1` to `eN` are expressions, and multiple expressions are separated by commas. In the following example, a variable `x` of type `(Int64, Float64)` and a variable `y` of type `(Int64, Float64, String)` are defined, and tuple type literals are used to assign initial values to them:

<!-- compile -->

```cangjie
let x: (Int64, Float64) = (3, 3.141592)
let y: (Int64, Float64, String) = (3, 3.141592, "PI")
```

Tuples support accessing elements at specific positions via `t[index]`, where `t` is a tuple and `index` is a subscript. The `index` must be an integer literal starting from `0` and less than the number of tuple elements; otherwise, a compilation error will occur. In the following example, `pi[0]` and `pi[1]` are used to access the first and second elements of the binary tuple `pi`, respectively.
<!-- verify -->

```cangjie
main() {
    var pi = (3.14, "PI")
    println(pi[0])
    println(pi[1])
}
```

Compiling and executing the above code will output:

```text
3.140000
PI
```

In assignment expressions, tuples can be used for multiple assignments. Refer to the [Assignment Operators](./basic_operators.md#assignment-operators) section.

## Type Parameters of Tuple Types

Explicit type parameter names can be marked for tuple types. In the following example, `name` and `price` are `type parameter names`.

<!-- verify -->

```cangjie
func getFruitPrice(): (name: String, price: Int64) {
    return ("banana", 10)
}

main() {
    let tmp = getFruitPrice()
    var a = tmp[0]
    var b = tmp[1]
    b++
    println("b = ${b}, tmp[1] = ${tmp[1]}")
}
```

Compiling and executing the above code will output:

```text
b = 11, tmp[1] = 10
```

For a tuple type, type parameter names must either all be written or all be omitted. Alternating between named and unnamed parameters is not allowed, and the parameter names themselves cannot be used as variables or to access elements in the tuple.

<!-- compile.error -->

```cangjie
let a: (name: String, Int64) = ("banana", 5) // Error, in a parameter type list, either all parameters must be named, or none of them
let b: (name: String, price: Int64) = ("banana", 5) // OK
b.name // Error, undeclared identifier 'name'
```