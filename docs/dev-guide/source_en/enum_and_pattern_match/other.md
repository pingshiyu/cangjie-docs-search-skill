# Other Usage Scenarios of Patterns

Patterns can be used not only in `match` expressions but also in variable definitions and `for in` expressions. For example, the left side of an equals sign is a pattern, and the part between the `for` keyword and the `in` keyword is also a pattern. Additionally, conditions in `if` expressions and `while` expressions can utilize patterns. For specific examples, refer to the ["Conditions Involving let-pattern"](../basic_programming_concepts/expression.md#conditions-involving-let-pattern) section.

However, not all patterns can be used in variable definitions and `for in` expressions. Only `irrefutable` patterns are permitted in these contexts. Therefore, only wildcard patterns, binding patterns, `irrefutable` tuple patterns, and `irrefutable` enum patterns are allowed.

1. Examples of using wildcard patterns in variable definitions and `for in` expressions:

    <!-- verify -->

    ```cangjie
    main() {
        let _ = 100
        for (_ in 1..5) {
            println("0")
        }
    }
    ```

    In the above example, a wildcard pattern is used in the variable definition, indicating the creation of a nameless variable (which consequently cannot be accessed later). The `for in` expression uses a wildcard pattern, meaning elements from `1..5` won't be bound to any variable (thus their values cannot be accessed within the loop body). Compiling and executing this code yields:

    ```text
    0
    0
    0
    0
    ```

2. Examples of using binding patterns in variable definitions and `for in` expressions:

    <!-- verify -->

    ```cangjie
    main() {
        let x = 100
        println("x = ${x}")
        for (i in 1..5) {
            println(i)
        }
    }
    ```

    Here, `x` in the variable definition and `i` in the `for in` expression are both binding patterns. Compiling and executing this code yields:

    ```text
    x = 100
    1
    2
    3
    4
    ```

3. Examples of using `irrefutable` tuple patterns in variable definitions and `for in` expressions:

    <!-- verify -->

    ```cangjie
    main() {
        let (x, y) = (100, 200)
        println("x = ${x}")
        println("y = ${y}")
        for ((i, j) in [(1, 2), (3, 4), (5, 6)]) {
            println("Sum = ${i + j}")
        }
    }
    ```

    In this example, a tuple pattern is used in the variable definition to destructure `(100, 200)` and bind its components to `x` and `y`, effectively defining two variables. The `for in` expression employs a tuple pattern to sequentially extract tuple-type elements from `[(1, 2), (3, 4), (5, 6)]`, destructure them, and bind their components to `i` and `j`, then output their sum in the loop body. Compiling and executing this code yields:

    ```text
    x = 100
    y = 200
    Sum = 3
    Sum = 7
    Sum = 11
    ```

4. Examples of using `irrefutable` enum patterns in variable definitions and `for in` expressions:

    <!-- verify -->

    ```cangjie
    enum RedColor {
        Red(Int64)
    }
    main() {
        let Red(red) = Red(0)
        println("red = ${red}")
        for (Red(r) in [Red(10), Red(20), Red(30)]) {
            println("r = ${r}")
        }
    }
    ```

    Here, an enum pattern is used in the variable definition to destructure `Red(0)` and bind its constructor parameter (i.e., `0`) to `red`. The `for in` expression uses an enum pattern to sequentially extract elements from `[Red(10), Red(20), Red(30)]`, destructure them, and bind their constructor parameters to `r`, then output `r` in the loop body. Compiling and executing this code yields:

    ```text
    red = 0
    r = 10
    r = 20
    r = 30
    ```