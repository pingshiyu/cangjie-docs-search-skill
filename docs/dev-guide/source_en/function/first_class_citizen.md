# Function Types

In the Cangjie programming language, functions are first-class citizens, meaning they can be passed as arguments to other functions, returned as values from functions, or assigned to variables. Therefore, functions themselves have types, referred to as function types.

A function type consists of the function's parameter types and return type, connected by `->`. Parameter types are enclosed in parentheses `()`, which can contain zero or more parameters. If there are multiple parameters, their types are separated by commas (`,`).

For example:

<!-- compile -->

```cangjie
func hello(): Unit {
    println("Hello!")
}
```

The above example defines a function named `hello` with the type `() -> Unit`, indicating that this function takes no parameters and returns `Unit`.

Here are some additional examples:

- Example: A function named `display` with type `(Int64) -> Unit`, indicating it takes one parameter of type `Int64` and returns `Unit`.

    <!-- compile -->

    ```cangjie
    func display(a: Int64): Unit {
        println(a)
    }
    ```

- Example: A function named `add` with type `(Int64, Int64) -> Int64`, indicating it takes two parameters of type `Int64` and returns `Int64`.

    <!-- compile -->

    ```cangjie
    func add(a: Int64, b: Int64): Int64 {
        a + b
    }
    ```

- Example: A function named `returnTuple` with type `(Int64, Int64) -> (Int64, Int64)`, taking two `Int64` parameters and returning a tuple type `(Int64, Int64)`.

    <!-- compile -->

    ```cangjie
    func returnTuple(a: Int64, b: Int64): (Int64, Int64) {
        (a, b)
    }
    ```

## Type Parameters in Function Types

Function types can have explicit type parameter names. In the following example, `name` and `price` are type parameter names.

<!-- run -->

```cangjie
func showFruitPrice(name: String, price: Int64) {
    println("fruit: ${name} price: ${price} yuan")
}

main() {
    let fruitPriceHandler: (name: String, price: Int64) -> Unit
    fruitPriceHandler = showFruitPrice
    fruitPriceHandler("banana", 10)
}
```

Note that for a function type, you must either consistently include type parameter names or omit them entirely; mixing them is not allowed.

<!-- compile.error -->

```cangjie
let handler: (name: String, Int64) -> Int64   // Error
```

## Function Types as Parameter Types

Example: A function named `printAdd` with type `((Int64, Int64) -> Int64, Int64, Int64) -> Unit`, indicating it takes three parameters: a function type `(Int64, Int64) -> Int64` and two `Int64` values, returning `Unit`.

<!-- compile -->

```cangjie
func printAdd(add: (Int64, Int64) -> Int64, a: Int64, b: Int64): Unit {
    println(add(a, b))
}
```

## Function Types as Return Types

Function types can also serve as the return type of another function.

In the following example, the function `returnAdd` has type `() -> (Int64, Int64) -> Int64`, meaning it takes no parameters and returns a function of type `(Int64, Int64) -> Int64`. Note that `->` is right-associative.

<!-- run -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a + b
}

func returnAdd(): (Int64, Int64) -> Int64 {
    add
}

main() {
    var a = returnAdd()
    println(a(1,2))
}
```

## Function Types as Variable Types

Function names themselves are expressions, and their types correspond to their function types.

<!-- compile -->

```cangjie
func add(p1: Int64, p2: Int64): Int64 {
    p1 + p2
}

let f: (Int64, Int64) -> Int64 = add
```

In the above example, the function `add` has type `(Int64, Int64) -> Int64`. The variable `f` is declared with the same type and initialized with `add`.

If a function is overloaded in the current scope (see [Function Overloading](./function_overloading.md)), using the function name directly as an expression may cause ambiguity. In such cases, the compiler will report an error:

<!-- compile.error -->

```cangjie
func add(i: Int64, j: Int64) {
    i + j
}

func add(i: Float64, j: Float64) {
    i + j
}

main() {
    var f = add   // Error, ambiguous function 'add'
    var plus: (Int64, Int64) -> Int64 = add  // OK
}
```