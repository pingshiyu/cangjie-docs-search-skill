# Expressions

In some traditional programming languages, an expression consists of one or more operands combined by zero or more operators. An expression always implies a computation process, so each expression will have a computation result. For expressions containing only operands without operators, the computation result is the operand itself. For expressions containing operators, the computation result is the value obtained by performing the operations defined by the operators on the operands. Expressions defined in this way are also called arithmetic expressions. For operator precedence, refer to the [Operators](../Appendix/operator.md) chapter.

In the Cangjie programming language, the traditional definition of expressions is simplified and extended—any language element that can be evaluated is considered an expression. Therefore, Cangjie not only has traditional arithmetic expressions but also conditional expressions, loop expressions, and `try` expressions, all of which can be evaluated and used as values, such as initial values for variable definitions and function arguments. Additionally, because Cangjie is a strongly typed programming language, Cangjie expressions not only can be evaluated but also have a definite type.

> **Note:**
>
> To clearly distinguish between different program statements or expressions, Cangjie uses semicolons (`;`) as separators. If a statement occupies a line by itself, the semicolon can be omitted. However, if multiple statements exist on the same line, they must be separated by semicolons.

Various expressions in the Cangjie programming language will be introduced in subsequent chapters. This section covers the most commonly used conditional expressions, loop expressions, and some control transfer expressions (`break`, `continue`).

The execution flow of any program involves only three basic structures—sequential structure, branching structure, and looping structure. In fact, branching and looping structures are obtained by certain instructions causing jumps in the current sequential execution flow, enabling the program to express more complex logic. In Cangjie, the language elements used to control the execution flow are conditional expressions and loop expressions.

In the Cangjie programming language, the conditional expression is the `if` expression, whose value and type depend on the usage context. There are three types of loop expressions: `for-in` expressions, `while` expressions, and `do-while` expressions, all of which have the type `Unit` and the value `()`.

In Cangjie programs, a group of expressions enclosed by a pair of curly braces `{}` is called a "code block," which serves as a sequential execution flow in the program. The expressions within the block are executed in the order they are written. If a code block contains at least one expression, the value and type of the block are defined to be equal to the value and type of its last expression. If the code block contains no expressions, such an empty block is defined to have the type `Unit` and the value `()`.

> **Note:**
>
> A code block itself is not an expression and cannot be used alone. It must be attached to functions, conditional expressions, loop expressions, etc., for execution and evaluation.

## if Expression

The basic form of the `if` expression is:

```text
if (condition) {
  branch1
} else {
  branch2
}
```

Here, "condition" can be a Boolean-type expression, a "let pattern" (syntactic sugar), or multiple "let patterns" and Boolean-type expressions connected directly by logical AND or OR operations. For examples involving "let patterns," refer to [Examples of "Conditions" Involving let Patterns](#examples-of-conditions-involving-let-patterns).

When the expression and pattern match successfully, the pattern match evaluates to `true`, and the `if` branch's corresponding code block is executed. Otherwise, it evaluates to `false`, and the `else` branch's code block is executed. The `else` branch is optional.

"Branch1" and "branch2" are two code blocks. The `if` expression executes according to the following rules:

1. Evaluate the "condition" expression. If the value is `true`, proceed to step 2; if `false`, proceed to step 3.
2. Execute "branch1," then proceed to step 4.
3. Execute "branch2," then proceed to step 4.
4. Continue executing the code following the `if` expression.

In some scenarios, only the actions to take when the condition is true may be of interest, so the `else` and its corresponding code block can be omitted.

The following program demonstrates the basic usage of the `if` expression:

<!-- run -->

```cangjie
import std.random.Random

main() {
    let number: Int8 = Random().nextInt8()
    println(number)
    if (number % 2 == 0) {
        println("Even")
    } else {
        println("Odd")
    }
}
```

In this program, a random integer is generated using the `random` package from the Cangjie standard library. The `if` expression checks whether this integer is divisible by 2 and prints "Even" or "Odd" in the respective branches.

The Cangjie programming language is strongly typed. The condition in an `if` expression must be of Boolean type; integers, floating-point numbers, etc., cannot be used. Unlike C and similar languages, Cangjie does not use whether the condition evaluates to zero as the basis for branching. For example, the following program will result in a compilation error (additional incorrect expression examples are provided in [Incorrect Expression Examples](#incorrect-expression-examples) for comparison):

<!-- compile.error -->

```cangjie
main() {
    let number = 1
    if (number) { // Compilation error: type mismatch
        println("Non-zero")
    }
}
```

In many scenarios, when one condition fails, another or multiple conditions may need to be checked before executing corresponding actions. Cangjie allows new `if` expressions to follow `else`, enabling multi-level conditional checks and branching. For example:

<!-- run -->

```cangjie
import std.random.Random

main() {
    let speed = Random().nextFloat64() * 20.0
    println("${speed} km/s")
    if (speed > 16.7) {
        println("Third cosmic velocity: Magpie Bridge Rendezvous")
    } else if (speed > 11.2) {
        println("Second cosmic velocity: Chang'e Flies to the Moon")
    } else if (speed > 7.9) {
        println("First cosmic velocity: Soaring Through Clouds")
    } else {
        println("Stay grounded, gaze at the stars")
    }
}
```

The value and type of an `if` expression depend on its usage form and context:

- When an `if` expression with an `else` branch is evaluated, its type is determined based on the evaluation context:
    - If the context explicitly requires a value of type `T`, the types of all branch code blocks in the `if` expression must be subtypes of `T`. The `if` expression's type is then determined as `T`. If the subtype constraint is not satisfied, a compilation error occurs. For example, in the following code, since the type `Int64` of variable `b` does not satisfy the subtype constraint with the types of the branch code blocks, a compilation error occurs:

        <!-- compile.error -->

        ```cangjie
        var a = 10
        var b: Int64 = if(a == 10) { // Error, mismatched types
            "this is 10"
        }else {
            "this is not 10"
        }
        ```

    - If the context does not have explicit type requirements, the `if` expression's type is the least common supertype of all branch code block types. If no least common supertype exists, a compilation error occurs. For example, in the following code, since string and numeric types have no least common supertype, a compilation error occurs:

        <!-- compile.error -->

        ```cangjie
        var a = 10
        var b = if(a == 10) { // Error, types Struct-String and Int64 of the two branches of this 'if' expression mismatch
            "this is 10"
        }else {
            20
        }
        ```

  If compilation succeeds, the `if` expression's value is the value of the executed branch's code block.

- If an `if` expression with an `else` branch is not evaluated, in such scenarios, developers typically only want to perform different operations in different branches without concerning themselves with the values and types of the last expressions in each branch. To avoid the above type-checking rules affecting this mental model, Cangjie stipulates that in such scenarios, the `if` expression's type is `Unit`, its value is `()`, and the branches do not participate in the above type checks.
- For `if` expressions without an `else` branch, since the `if` branch may not be executed, such `if` expressions are defined to have the type `Unit` and the value `()`.

For example, the following program uses an `if` expression evaluation to simulate a simple analog-to-digital conversion process:

<!-- run -->

```cangjie
main() {
    let zero: Int8 = 0
    let one: Int8 = 1
    let voltage = 5.0
    let bit = if (voltage < 2.5) {
        zero
    } else {
        one
    }
}
```

In the above program, the `if` expression is used as the initial value for a variable definition. Since the variable `bit` is not explicitly typed and its type must be inferred from the initial value, the `if` expression's type is determined as the least common supertype of the two branch code block types. As explained earlier regarding "code blocks," both branch code block types are `Int8`, so the `if` expression's type is determined as `Int8`, and its value is the value of the executed branch (the `else` branch's code block). Thus, the variable `bit` has the type `Int8` and the value `1`.

### Examples of "Conditions" Involving let Patterns

"let patterns" are syntactic sugar. A "let pattern" has the form `let pattern <- expression`, where:

- `pattern`: A pattern used to match the value type and content of `expression`.
- `<-`: The pattern-matching operator.
- `expression`: An expression whose value is evaluated and then matched against the pattern. The precedence of the `expression` must not be lower than the `..` operator, but parentheses can be used to change precedence. For operator precedence, refer to [Operators](../Appendix/operator.md).

Here are examples of "conditions" involving logical AND or OR operations between two "let patterns" or between a "let pattern" and other expressions.

<!-- run -expression_example5 -->

```cangjie
main() {
    let a = Some(3)
    let c = if (let Some(b) <- a) {
            1 // Pattern match succeeds, c = 1
        } else {
            2
        }
    let d = Some(1)

    if (let Some(e) <- a && let Some(f) <- d) { // Both patterns match; condition evaluates to true
        println("${e} ${f}") // prints 3 1
    }

    if (let Some(f) <- d && f > 3) { // Pattern matches; f = 1, f > 3 check fails; jumps to else branch
        println("${f}")
    } else {
        println("d is None or value of d is less or equal to 3") // prints this line
    }

    if (let Some(_) <- a || let Some(_) <- d) { // Enum patterns connected by ||, no variable binding; correct
        println("at least one of a and d is Some") // prints this line
    } else {
        println("both a and d are None")
    }

    let g = 3
    if (let Some(_) <- a || g > 1) {
        println("this") // prints this line
    } else {
        println("that")
    }
}
```

In "let patterns," the precedence of the expression part must not be lower than the `..` operator. Here are corresponding incorrect and correct examples. For details on the [`Option` type](../enum_and_pattern_match/option_type.md), refer to later sections.

<!-- compile.error -->

```cangjie
if (let Some(a) <- fun() as Option<Int64>) {}   // Parsing error: `as` has lower precedence than `..`
if (let Some(a) <- (fun() as Option<Int64>)) {} // Correct
if (let Some(a) <- b && a + b > 3) {}           // Correct, parsed as (let Some(a) <- b) && (a + b > 3)
if (let m <- 0..generateSomeInt()) {}           // Correct
```

### Incorrect Expression Examples

Here are examples of incorrect "conditions."

<!-- compile.error -->

```cangjie
if (let Some(a) <- b || a > 1) {} // Conditions connected by `||` cannot use enum patterns that bind variables
if (let Some(a) <- b && a + 1) {} // Right side of `&&` is neither a let pattern nor a Boolean-type expression
if (a > 3 && let Some(a) <- b) {} // a is bound by Some(a) pattern; cannot use it on the left side of the binding pattern
if (let Some(a) <- b && a > 3) {
    println("${a} > 3")
} else {
    println("${a} < 3") // a can only be used in the if branch, not the else branch
}
if (let Some(a) <- b where a > 3) {} // Use `&&` for condition checks, not `where`
```

## while Expression

The basic form of the `while` expression is:

```text
while (condition) {
  loop_body
}
```

Here, "condition" is the same as in the `if` expression, and "loop_body" is a code block. The `while` expression executes according to the following rules:

1. Evaluate the "condition" expression. If the value is `true`, proceed to step 2; if `false`, proceed to step 3.
2. Execute "loop_body," then proceed to step 1.
3. End the loop and continue executing the code following the `while` expression.

For example, the following program uses a `while` expression to approximate the square root of 2 using the bisection method:

<!-- verify -->

```cangjie
main() {
    var root = 0.0
    var min = 1.0
    var max = 2.0
    var error = 1.0
    let tolerance = 0.1 ** 10

    while (error ** 2 > tolerance) {
        root = (min + max) / 2.0
        error = root ** 2 - 2.0
        if (error > 0.0) {
            max = root
        } else {
            min = root
        }
    }
    println("Square root of 2 ≈ ${root}")
}
```

Running this program will output:

```text
Square root of 2 ≈ 1.414215
```

## do-while Expression

The basic form of the `do-while` expression is:

```text
do {
  loop_body
} while (condition)
```

Here, "condition" is a Boolean-type expression, and "loop_body" is a code block. The `do-while` expression executes according to the following rules:

1. Execute "loop_body," then proceed to step 2.
2. Evaluate the "condition" expression. If the value is `true`, proceed to step 1; if `false`, proceed to step 3.
3. End the loop and continue executing the code following the `do-while` expression.

For example, the following program uses a `do-while` expression to approximate the value of π using the Monte Carlo method:

<!-- run -->

```cangjie
import std.random.Random

main() {
    let random = Random()
    var totalPoints = 0
    var hitPoints = 0

    do {
        // Randomly sample points within the square ((0, 0), (1, 1))
        let x = random.nextFloat64()
        let y = random.nextFloat64()
        // Determine if the point falls within the inscribed circle
        if ((x - 0.5) ** 2 + (y - 0.5) ** 2 < 0.25) {
            hitPoints++
        }
        totalPoints++
    } while (totalPoints < 1000000)

    let pi = 4.0 * Float64(hitPoints) / Float64(totalPoints)
    println("Approximate value of pi: ${pi}")
}
```

Running the above program will output:

```text
Approximate value of pi: 3.141872
```

> **Note:**
>
> Since the algorithm involves random numbers, the output may vary each time the program is run, but it will always approximate 3.14.

## for-in Expression

The `for-in` expression can iterate over instances of types that implement the iterator interface `Iterable<T>`. The basic form of the `for-in` expression is:

```text
for (iterationVariable in sequence) {
  loopBody
}
```

Here, "loopBody" is a code block. The "iterationVariable" is a single identifier or a tuple composed of multiple identifiers, used to bind the data pointed to by the iterator in each iteration. It can be used as a local variable within the "loopBody". The "sequence" is an expression that is evaluated only once, and the iteration is performed on the value of this expression. Its type must implement the iterator interface `Iterable<T>`. The `for-in` expression executes according to the following rules:

1. Evaluate the "sequence" expression, use its value as the iteration target, and initialize the iterator of the iteration target.
2. Update the iterator. If the iterator terminates, proceed to step 4; otherwise, proceed to step 3.
3. Bind the current data pointed to by the iterator to the "iterationVariable" and execute the "loopBody", then return to step 2.
4. Terminate the loop and continue executing the code following the `for-in` expression.

> **Note:**
>
> Built-in types such as ranges and arrays in Cangjie already implement the `Iterable<T>` interface.

For example, the following program uses a `for-in` expression to iterate over the array `noumenonArray` composed of Chinese earthly branch characters, outputting the Heavenly Stems and Earthly Branches for each month of the lunar year 2024:

<!-- verify -->

```cangjie
main() {
    let metaArray = [r'甲', r'乙', r'丙', r'丁', r'戊', r'己', r'庚', r'辛', r'壬', r'癸']
    let noumenonArray = [r'寅', r'卯', r'辰', r'巳', r'午', r'未', r'申', r'酉', r'戌', r'亥', r'子', r'丑']
    let year = 2024

    // Heavenly stem index corresponding to the year
    let metaOfYear = ((year % 10) + 10 - 4) % 10
    // Heavenly stem index for the first month of this year
    var index = (2 * metaOfYear + 3) % 10 - 1

    println("Heavenly Stems and Earthly Branches for Lunar Year 2024:")
    for (noumenon in noumenonArray) {
        print("${metaArray[index]}${noumenon} ")
        index = (index + 1) % 10
    }
}
```

Here, characters prefixed with `r` represent [character literals](../basic_data_type/characters.md#character-literals). Running the above program will output:

```text
Heavenly Stems and Earthly Branches for Lunar Year 2024:
丙寅 丁卯 戊辰 己巳 庚午 辛未 壬申 癸酉 甲戌 乙亥 丙子 丁丑
```

### Iterating Over Ranges

The `for-in` expression can iterate over range type instances, for example:

<!-- verify -->

```cangjie
main() {
    var sum = 0
    for (i in 1..=100) {
        sum += i
    }
    println(sum)
}
```

Running the above program will output:

```text
5050
```

For detailed information about range types, refer to the basic data type [Range Type](../basic_data_type/range.md).

### Iterating Over Sequences of Tuples

If the elements of a sequence are of tuple type, the "iterationVariable" in the `for-in` expression can be written as a tuple to destructure the sequence elements, for example:

<!-- verify -->

```cangjie
main() {
    let array = [(1, 2), (3, 4), (5, 6)]
    for ((x, y) in array) {
        println("${x}, ${y}")
    }
}
```

Running the above program will output:

```text
1, 2
3, 4
5, 6
```

### Iteration Variables Cannot Be Modified

Within the loop body of a `for-in` expression, the iteration variable cannot be modified. For example, the following program will result in a compilation error:

<!-- compile.error -->

```cangjie
main() {
    for (i in 0..5) {
        i = i * 10 // Error: Cannot assign to an initialized `let` constant
        println(i)
    }
}
```

### Using Wildcard _ as Iteration Variable

In some scenarios, you only need to perform certain operations in a loop without using the iteration variable. In such cases, you can use the wildcard `_` in place of the iteration variable, for example:

<!-- verify -->

```cangjie
main() {
    var number = 2
    for (_ in 0..5) {
        number *= number
    }
    println(number)
}
```

Running the above program will output:

```text
4294967296
```

> **Note:**
>
> In such scenarios, if a regular identifier is used to define the iteration variable, the compilation will output an "unused variable" warning. Using the wildcard `_` avoids this warning.

### where Condition

In some iteration scenarios, you may need to skip specific values of the iteration variable and proceed to the next iteration. While this can be achieved using `if` and `continue` expressions within the loop body, Cangjie provides a more concise way—you can use the `where` keyword followed by a Boolean expression after the "sequence". Before executing the loop body each time, this expression will be evaluated. If the value is `true`, the loop body will execute; otherwise, it will proceed directly to the next iteration. For example:

<!-- verify -->

```cangjie
main() {
    for (i in 0..8 where i % 2 == 1) { // Loop body executes only when i is odd
        println(i)
    }
}
```

Running the above program will output:

```text
1
3
5
7
```

## break and continue Expressions

In loop structures, sometimes you need to terminate the loop early or skip the current iteration based on specific conditions. To facilitate this, Cangjie introduces the `break` and `continue` expressions. They can appear within the loop body of a loop expression. `break` terminates the current loop expression and proceeds to execute the code following the loop expression, while `continue` skips the remaining part of the current iteration and proceeds to the next iteration. Both `break` and `continue` expressions are of type [`Nothing`](../basic_data_type/nothing.md).

For example, the following program uses a `for-in` expression and a `break` expression to find the first number divisible by 5 in a given integer array:

<!-- verify -->

```cangjie
main() {
    let numbers = [12, 18, 25, 36, 49, 55]
    for (number in numbers) {
        if (number % 5 == 0) {
            println(number)
            break
        }
    }
}
```

When the `for-in` iteration reaches the third number 25 in the `numbers` array, since 25 is divisible by 5, the `if` branch containing `println` and `break` will execute. The `break` will terminate the `for-in` loop, and subsequent numbers in `numbers` will not be traversed. Therefore, running the above program will output:

```text
25
```

The following program uses a `for-in` expression and a `continue` expression to print the odd numbers in a given integer array:

<!-- verify -->

```cangjie
main() {
    let numbers = [12, 18, 25, 36, 49, 55]
    for (number in numbers) {
        if (number % 2 == 0) {
            continue
        }
        println(number)
    }
}
```

During iteration, when `number` is even, `continue` will be executed, skipping the remaining part of the current iteration (including `println`) and proceeding to the next iteration. Therefore, running the above program will output:

```text
25
49
55
```
