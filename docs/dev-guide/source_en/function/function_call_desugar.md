# Function Call Syntactic Sugar

## Trailing Lambda

Trailing lambda syntax can make function calls appear as if they were built-in language constructs, enhancing the language's extensibility.

When the last parameter of a function is of function type, and the corresponding argument in the function call is a lambda, the trailing lambda syntax can be used by placing the lambda outside the parentheses at the end of the function call.

For example, the following defines a `myIf` function where the first parameter is of type `Bool` and the second is a function type. When the first parameter is `true`, it returns the value from calling the second parameter; otherwise, it returns `0`. The `myIf` function can be called either as a regular function or using trailing lambda syntax.

<!-- compile -->

```cangjie
func myIf(a: Bool, fn: () -> Int64) {
    if(a) {
        fn()
    } else {
        0
    }
}

func test() {
    myIf(true, { => 100 }) // General function call

    myIf(true) {        // Trailing closure call
        100
    }
}
```

When a function call has exactly one lambda argument, the `()` can be omitted, leaving only the lambda.

Example:

<!-- compile -->

```cangjie
func f(fn: (Int64) -> Int64) { fn(1) }

func test() {
    f { i => i * i }
}
```

## Flow Expressions

Flow operators include two types: the infix operator `|>` (called `pipeline`) representing data flow and the infix operator `~>` (called `composition`) representing function composition.

### Pipeline Expressions

When a series of transformations need to be applied to input data, `pipeline` expressions can simplify the description. The syntax for a `pipeline` expression is: `e1 |> e2`, which is equivalent to the following syntactic sugar: `let v = e1; e2(v)`.

Here, `e2` is an expression of function type, and the type of `e1` must be a subtype of `e2`'s parameter type.

Example:

<!-- compile -->

```cangjie
func inc(x: Array<Int64>): Array<Int64> { // Increasing the value of each element in the array by '1'
    let s = x.size
    var i = 0
    for (e in x where i < s) {
        x[i] = e + 1
        i++
    }
    x
}

func sum(y: Array<Int64>): Int64 { // Get the sum of elements in the array
    var s = 0
    for (j in y) {
        s += j
    }
    s
}

let arr: Array<Int64> = [1, 3, 5]
let res = arr |> inc |> sum // res = 12
```

### Composition Expressions

`composition` expressions represent the composition of two single-parameter functions. The syntax for a `composition` expression is `f ~> g`, which is equivalent to `{ x => g(f(x)) }`.

Here, both `f` and `g` must be expressions of function type with exactly one parameter.

For `f` and `g` to compose, the return type of `f(x)` must be a subtype of the parameter type of `g(...)`.

Example 1:

<!-- compile -->

```cangjie
func f(x: Int64): Float64 {
    Float64(x)
}
func g(x: Float64): Float64 {
    x
}

var fg = f ~> g // The same as { x: Int64 => g(f(x)) }
```

Example 2:

<!-- compile -->

```cangjie
func f(x: Int64): Float64 {
    Float64(x)
}

let lambdaComp = {x: Int64 => x} ~> f // The same as { x: Int64 => f({x: Int64 => x}(x)) }
```

Example 3:

<!-- compile -->

```cangjie
func h1<T>(x: T): T { x }
func h2<T>(x: T): T { x }
var hh = h1<Int64> ~> h2<Int64> // The same as { x: Int64 => h2<Int64>(h1<Int64>(x)) }
```

> **Note:**
>
> In the expression `f ~> g`, `f` is evaluated first, followed by `g`, and then the function composition is performed.

Additionally, flow operators cannot be directly used with functions that have non-default named parameters because such functions require named arguments to be explicitly provided. For example:

<!-- compile.error -->

```cangjie
func f(a!: Int64): Unit {}

var a = 1 |> f  // Error
```

If needed, developers can pass named arguments to the `f` function via a lambda expression:

<!-- compile -->

```cangjie
func f(a!: Int64): Unit {}

var x = 1 |>  { x: Int64 => f(a: x) } // OK
```

For the same reason, when `f` has default parameter values, using it directly with flow operators is also incorrect:

<!-- compile.error -->

```cangjie
func f(a!: Int64 = 2): Unit {}

var a = 1 |> f // Error
```

However, when all named parameters have default values, the function can be called without providing named arguments, requiring only non-named parameters. Such functions can be used with flow operators:

<!-- compile -->

```cangjie
func f(a: Int64, b!: Int64 = 2): Unit {}

var a = 1 |> f  // OK
```

Of course, if you want to pass other arguments to parameter `b` when calling `f`, you still need to use a lambda expression:

<!-- compile -->

```cangjie
func f(a: Int64, b!: Int64 = 2): Unit {}

var a = 1 |> {x: Int64 => f(x,  b: 3)}  // OK
```

## Variadic Parameters

Variadic parameters are a special function call syntactic sugar. When the last non-named parameter of a function is of type `Array`, the corresponding argument position can directly accept a sequence of parameters instead of an `Array` literal (the number of parameters can be zero or more). Example:

<!-- verify -->

```cangjie
func sum(arr: Array<Int64>) {
    var total = 0
    for (x in arr) {
        total += x
    }
    return total
}

main() {
    println(sum())
    println(sum(1, 2, 3))
}
```

Program output:

```text
0
6
```

Note that only the last non-named parameter can be a variadic parameter. Named parameters cannot use this syntactic sugar.

<!-- compile.error -->

```cangjie
func length(arr!: Array<Int64>) {
    return arr.size
}

main() {
    println(length())        // Error, expected 1 argument, found 0
    println(length(1, 2, 3)) // Error, expected 1 argument, found 3
}
```

Variadic parameters can appear in global functions, static member functions, instance member functions, local functions, constructors, function variables, lambdas, function call operator overloads, and index operator overloads. They are not supported in other operator overloads, composition, or pipeline calls. Example:

<!-- verify -->

```cangjie
class Counter {
    var total = 0
    init(data: Array<Int64>) { total = data.size }
    operator func ()(data: Array<Int64>) { total += data.size }
}

main() {
    let counter = Counter(1, 2)
    println(counter.total)
    counter(3, 4, 5)
    println(counter.total)
}
```

Program output:

```text
2
5
```

Function overload resolution always prioritizes functions that can match without using variadic parameters. Only when no functions match will the compiler attempt to resolve using variadic parameters. Example:

<!-- verify -->

```cangjie
func f<T>(x: T) where T <: ToString {
    println("item: ${x}")
}

func f(arr: Array<Int64>) {
    println("array: ${arr}")
}

main() {
    f()
    f(1)
    f(1, 2)
}
```

Program output:

```text
array: []
item: 1
array: [1, 2]
```

When the compiler cannot resolve the ambiguity, it will report an error:

<!-- compile.error -->

```cangjie
func f(arr: Array<Int64>) { arr.size }
func f(first: Int64, arr: Array<Int64>) { first + arr.size }

main() {
    println(f(1, 2, 3)) // Error
}
```