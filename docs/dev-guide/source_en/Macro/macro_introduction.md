# Introduction to Macros

Macros can be understood as a special type of function. While regular functions perform computations on input values and output a new value, macros take and return the program itself. They accept a piece of code as input and output a new piece of code, which is then used for compilation and execution. To distinguish macro calls from function calls, macros are invoked using `@` followed by the macro name.

The following example demonstrates printing both the value and the expression itself during debugging:

<!-- code_no_check -->

```cangjie
let x = 3
let y = 2
@dprint(x)        // Prints "x = 3"
@dprint(x + y)    // Prints "x + y = 5"
```

Clearly, `dprint` cannot be implemented as a regular function because functions only receive the value of the input expression, not the expression itself. However, `dprint` can be implemented as a macro to access the code fragment of the input expression. A basic implementation is shown below:

<!-- verify -macro12 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro dprint(input: Tokens): Tokens {
    let inputStr = input.toString()
    let result = quote(
        print($(inputStr) + " = ")
        println($(input)))
    return result
}
```

Before explaining each line, let's verify this macro achieves the desired effect. First, create a `define` directory in the current folder, then create a `dprint.cj` file inside it with the above content. Additionally, create a `main.cj` file in the current directory with the following test code:

<!-- verify -macro12 -->

```cangjie
import define.*

main() {
    let x = 3
    let y = 2
    @dprint(x)
    @dprint(x + y)
}
```

Note the resulting directory structure:

```text
// Directory layout.
src
|-- define
|     `-- dprint.cj
`-- main.cj
```

In the current directory (`src`), run the compilation commands:

```bash
cjc define/*.cj --compile-macro
cjc main.cj -o main
```

Then execute `./main` to see the following output:

<!-- verify -macro12 -->

```text
x = 3
x + y = 5
```

Now let's examine each part of the code:

- Line 1: `macro package define`

  Macros must be declared in separate packages (they cannot coexist with other public functions). Packages containing macros are declared using `macro package`. Here we declare a macro package named `define`.

- Line 2: `import std.ast.*`

  The data types required for macro implementation, such as `Tokens` and syntax node types (to be discussed later), are located in the `ast` package of the Cangjie standard library. Therefore, any macro implementation must first import the `ast` package.

- Line 3: `public macro dprint(input: Tokens): Tokens`

  This declares a macro named `dprint`. Since this is a non-attribute macro (this concept will be explained later), it accepts a parameter of type `Tokens`, representing the code fragment passed to the macro. The macro's return value is also a code fragment.

- Line 4: `let inputStr = input.toString()`

  In the macro implementation, we first convert the input code fragment to a string. In our test cases, `inputStr` becomes `"x"` or `"x + y"`.

- Lines 5-7: `let result = quote(...)`

  The [`quote` expression](./Tokens_types_and_quote_expressions.md#quote-expressions-and-interpolation) is used to construct [`Tokens`](./Tokens_types_and_quote_expressions.md#tokens-type). It converts the code fragment within parentheses into `Tokens`. Inside `quote`, interpolation `$(...)` can be used to convert the enclosed expression into `Tokens` and insert it into the `Tokens` constructed by `quote`. In this code, `$(inputStr)` inserts the value of `inputStr` (including quotation marks), while `$(input)` inserts the input code fragment. Thus, if the input expression is `x + y`, the resulting `Tokens` would be:

  <!-- code_no_check -->

  ```cangjie
  print("x + y" + " = ")
  println(x + y)
  ```

- Line 8: `return result`

  Finally, the constructed code fragment is returned. These two lines of code will be compiled, and when executed, will output `x + y = 5`.

Reviewing the `dprint` macro definition: it uses `Tokens` as input and employs `quote` with interpolation to construct another `Tokens` as output. To work with macros effectively, we need detailed understanding of `Tokens`, `quote`, and interpolation concepts, which will be introduced separately below.