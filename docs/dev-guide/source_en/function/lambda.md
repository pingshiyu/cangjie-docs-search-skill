# Lambda Expressions

## Definition of Lambda Expressions

A lambda expression is an anonymous function (i.e., a function without a name) designed to quickly define concise function logic in programs without explicitly declaring a function name. This concept originates from lambda calculus in mathematics and has been introduced into various programming languages (such as C++, Python, C#, etc.) to simplify code and enhance flexibility. The Cangjie programming language also incorporates lambda expressions, and their usage will be detailed in this section.

The syntax of a lambda expression is as follows: `{ p1: T1, ..., pn: Tn => expressions | declarations }`.

Here, the part before `=>` is the parameter list, where multiple parameters are separated by `,`, and each parameter name and type are separated by `:`. The part before `=>` can also be empty (parameterless). The part after `=>` is the lambda expression body, which consists of a sequence of expressions or declarations. The scope of lambda expression parameter names is the same as that of functions, limited to the lambda expression body, and their scope level is equivalent to variables defined within the lambda expression body.

<!-- compile -->

```cangjie
let f1 = { a: Int64, b: Int64 => a + b }

var display = { =>   // Parameterless lambda expression.
    println("Hello")
    println("World")
}
```

Lambda expressions, whether they have parameters or not, cannot omit `=>`, unless they are used as [trailing lambdas](./function_call_desugar.md#trailing-lambda). For example:

<!-- compile -->

```cangjie
var display = { => println("Hello") }

func f2(lam: () -> Unit) {}
let f2Res = f2 { println("World") } // OK to omit the =>
```

Type annotations for parameters in lambda expressions can be omitted. In the following cases, if parameter types are omitted, the compiler will attempt type inference. If the compiler cannot infer the type, a compilation error will occur:

- When a lambda expression is assigned to a variable, its parameter types are inferred from the variable type;
- When a lambda expression is used as an argument in a function call, its parameter types are inferred from the function's parameter types.

<!-- compile -->

```cangjie
// The parameter types are inferred from the type of the variable sum1
var sum1: (Int64, Int64) -> Int64 = { a, b => a + b }

var sum2: (Int64, Int64) -> Int64 = { a: Int64, b => a + b }

func f(a1: (Int64) -> Int64): Int64 {
    a1(1)
}

main(): Int64 {
    // The parameter type of lambda is inferred from the type of function f
    f({ a2 => a2 + 10 })
}
```

Lambda expressions do not support explicit return type declarations. Their return type is always inferred from the context, and an error is reported if inference fails.

- If the context explicitly specifies the return type of the lambda expression, its return type is the context-specified type.

    - When a lambda expression is assigned to a variable, its return type is inferred from the variable type:

      <!-- compile -->

      ```cangjie
      let f: () -> Unit = { => println(10) }
      ```

    - When a lambda expression is used as an argument, its return type is inferred from the parameter type of the function call:

      <!-- compile -->

      ```cangjie
      func f(a1: (Int64) -> Int64): Int64 {
        a1(1)
      }

      main(): Int64 {
        f({ a2: Int64 => a2 + 10 })
      }
      ```

    - When a lambda expression is used as a return value, its return type is inferred from the return type of the enclosing function:

      <!-- compile -->

      ```cangjie
      func f(): (Int64) -> Int64 {
        { a: Int64 => a }
      }
      ```

- If the context does not explicitly specify the type, similar to deriving the return type of a function, the compiler will infer the return type of the lambda expression based on the types of all `return xxx` expressions in the lambda body and the type of the lambda body itself.

    - The content to the right of `=>` follows the same rules as a regular function body, with the return type being `Int64`:

      <!-- compile -->

      ```cangjie
      let sum1 = { a: Int64, b: Int64 => a + b }
      ```

    - If the right side of `=>` is empty, the return type is `Unit`:

      <!-- compile -->

      ```cangjie
      let f = { => }
      ```

## Lambda Expression Invocation

Lambda expressions support immediate invocation. For example:

<!-- compile -->

```cangjie
let r1 = { a: Int64, b: Int64 => a + b }(1, 2) // r1 = 3
let r2 = { => 123 }()                          // r2 = 123
```

Lambda expressions can also be assigned to a variable and invoked using the variable name. For example:

<!-- compile -->

```cangjie
func f() {
    var g = { x: Int64 => println("x = ${x}") }
    g(2)
}
```