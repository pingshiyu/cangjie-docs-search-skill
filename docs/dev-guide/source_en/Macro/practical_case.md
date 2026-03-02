# Practical Examples

## Fast Exponentiation Calculation

Demonstrates the use of macros for compile-time evaluation to generate optimized code through a simple example. When calculating the power `n ^ e`, if `e` is a (relatively large) integer, the computation can be accelerated by repeatedly squaring (instead of iterative multiplication). This algorithm can be directly implemented using a while loop, for example:

<!-- run -->

```cangjie
func power(n: Int64, e: Int64) {
    var result = 1
    var vn = n
    var ve = e
    while (ve > 0) {
        if (ve % 2 == 1) {
            result *= vn
        }
        ve /= 2
        if (ve > 0) {
            vn *= vn
        }
    }
    result
}
```

However, this implementation requires analyzing the value of `e` each time, with multiple checks and updates to `ve` within loops and conditional statements. Additionally, the implementation only supports cases where `n` is of type `Int64`. To support other types of `n`, the issue of expressing `result = 1` must also be addressed. If the specific value of `e` is known in advance, the code can be written more simply. For example, if `e` is known to be 10, the entire loop can be unrolled as follows:

<!-- run -->

```cangjie
func power_10(n: Int64) {
    var vn = n
    vn *= vn         // vn = n ^ 2
    var result = vn  // result = n ^ 2
    vn *= vn         // vn = n ^ 4
    vn *= vn         // vn = n ^ 8
    result *= vn     // result = n ^ 10
    result
}
```

Of course, manually writing this code is tedious. The goal is to automatically generate this code given the value of `e`. Macros can achieve this. The usage example is as follows:

<!-- code_no_check -->

```cangjie
public func power_10(n: Int64) {
    @power[10](n)
}
```

The macro-expanded code is (from the `.macrocall` file):

<!-- code_no_check -->

```cangjie
public func power_10(n: Int64) {
    /* ===== Emitted by MacroCall @power in main.cj:20:5 ===== */
    /* 20.1 */var _power_vn = n
    /* 20.2 */_power_vn *= _power_vn
    /* 20.3 */var _power_result = _power_vn
    /* 20.4 */_power_vn *= _power_vn
    /* 20.5 */_power_vn *= _power_vn
    /* 20.6 */_power_result *= _power_vn
    /* 20.7 */_power_result
/* ===== End of the Emit ===== */
}
```

Below is the implementation of the `@power` macro.

<!-- verify -macro13 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*
import std.convert.*

public macro power(attrib: Tokens, input: Tokens) {
    let attribExpr = parseExpr(attrib)
    if (let Some(litExpr) <- (attribExpr as LitConstExpr)) {
        let lit = litExpr.literal
        if (lit.kind != TokenKind.INTEGER_LITERAL) {
            diagReport(DiagReportLevel.ERROR, attrib,
                       "Attribute must be integer literal",
                       "Expected integer literal")
        }
        var n = Int64.parse(lit.value)
        var result = quote(var _power_vn = $(input)
        )
        var flag = false
        while (n > 0) {
            if (n % 2 == 1) {
                if (!flag) {
                    result += quote(var _power_result = _power_vn
                    )
                    flag = true
                } else {
                    result += quote(_power_result *= _power_vn
                    )
                }
            }
            n /= 2
            if (n > 0) {
                result += quote(_power_vn *= _power_vn
                )
            }
        }
        result += quote(_power_result)
        return result
    } else {
        diagReport(DiagReportLevel.ERROR, attrib,
                   "Attribute must be integer literal",
                   "Expected integer literal")
    }
    return input
}
```

The explanation of this code is as follows:

- First, confirm that the input attribute `attrib` is an integer literal; otherwise, report an error via `diagReport`. Parse this literal into an integer `n`.
- Let `result` be the currently accumulated output code, starting with the declaration `var _power_vn`. To avoid variable name conflicts, use the less likely to conflict name `_power_vn`.
- Enter the while loop, where the boolean variable `flag` indicates whether `var _power_result` has been initialized. The rest of the code structure is similar to the implementation of the `power` function shown earlier, but the difference is that the while loop and if conditions are used at compile time to determine what code to generate, rather than making these judgments at runtime. Then generate code consisting of appropriate combinations of `_power_result *= _power_vn` and `_power_vn *= _power_vn`.
- Finally, add the code to return `_power_result` and return this code as the macro's output value.

Place this code in the `macros/power.cj` file and add the following test in `main.cj`:

<!-- verify -macro13 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

public func power_10(n: Int64) {
    @power[10](n)
}

main() {
    let a = 3
    println(power_10(a))
}
```

The output is:

<!-- verify -macro13 -->

```text
59049
```

## Memoize Macro

Memoization is a common technique in dynamic programming algorithms. It stores the results of already computed subproblems so that when the same subproblem appears again, the result can be directly retrieved from the table, avoiding redundant computations and improving algorithm efficiency.

Typically, using memoization requires developers to manually implement storage and retrieval functionality. With macros, this process can be automated. The macro's effect is as follows:

<!-- code_no_check -->

```cangjie
@Memoize[true]
func fib(n: Int64): Int64 {
    if (n == 0 || n == 1) {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

main() {
    let start = DateTime.now()
    let f35 = fib(35)
    let end = DateTime.now()
    println("fib(35): ${f35}")
    println("execution time: ${(end - start).toMicroseconds()} us")
}
```

In the above code, the `fib` function is implemented using simple recursion. Without the `@Memoize[true]` annotation, the function's runtime would grow exponentially with `n`. For example, if the `@Memoize[true]` line is removed or `true` is changed to `false` in the above code, the `main` function's output would be:

```text
fib(35): 9227465
execution time: 199500 us
```

Restoring `@Memoize[true]`, the output becomes:

```text
fib(35): 9227465
execution time: 78 us
```

The same answer with significantly reduced computation time demonstrates that `@Memoize` indeed implements memoization.

To understand the principle of `@Memoize`, the macro-expanded result of the `fib` function is shown below (from the `.macrocall` file, but formatted for better readability).

<!-- run -->

```cangjie
import std.collection.*

var memoizeFibMap = HashMap<Int64, Int64>()

func fib(n: Int64): Int64 {
    if (memoizeFibMap.contains(n)) {
        return memoizeFibMap.get(n).getOrThrow()
    }

    let memoizeEvalResult = { =>
        if (n == 0 || n == 1) {
            return n
        }

        return fib(n - 1) + fib(n - 2)
    }()
    memoizeFibMap.add(n, memoizeEvalResult)
    return memoizeEvalResult
}
```

The execution flow of the above code is as follows:

- First, define `memoizeFibMap` as a hash table from `Int64` to `Int64`, where the first `Int64` corresponds to the type of `fib`'s single parameter, and the second `Int64` corresponds to `fib`'s return type.
- Next, in the function body, check if the input parameter exists in `memoizeFibMap`; if so, immediately return the stored value. Otherwise, use the original function body of `fib` to compute the result. Here, an (parameterless) anonymous function is used so that `fib`'s function body requires no changes and can handle any way of exiting the `fib` function (including intermediate returns, returning the last expression, etc.).
- Finally, store the computed result in `memoizeFibMap` and return the result.

With such a "template," the implementation of the macro becomes straightforward. The complete code is as follows.

<!-- compile -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro Memoize(attrib: Tokens, input: Tokens) {
    if (attrib.size != 1 || attrib[0].kind != TokenKind.BOOL_LITERAL) {
        diagReport(DiagReportLevel.ERROR, attrib,
                   "Attribute must be a boolean literal (true or false)",
                   "Expected boolean literal (true or false) here")
    }

    let memoized = (attrib[0].value == "true")
    if (!memoized) {
        return input
    }

    let fd = FuncDecl(input)
    if (fd.funcParams.size != 1) {
        diagReport(DiagReportLevel.ERROR, fd.lParen + fd.funcParams.toTokens() + fd.rParen,
                   "Input function to memoize should take exactly one argument",
                   "Expect only one argument here")
    }

    let memoMap = Token(TokenKind.IDENTIFIER, "_memoize_" + fd.identifier.value + "_map")
    let arg1 = fd.funcParams[0]

    return quote(
        var $(memoMap) = HashMap<$(arg1.paramType), $(fd.declType)>()

        func $(fd.identifier)($(arg1)): $(fd.declType) {
            if ($(memoMap).contains($(arg1.identifier))) {
                return $(memoMap).get($(arg1.identifier)).getOrThrow()
            }

            let memoizeEvalResult = { => $(fd.block.nodes) }()
            $(memoMap).add($(arg1.identifier), memoizeEvalResult)
            return memoizeEvalResult
        }
    )
}
```

First, perform validity checks on the attributes and input. The attribute must be a boolean literal; if `false`, return the input directly. Otherwise, verify that the input can be parsed as a function declaration (`FuncDecl`) and must contain exactly one parameter. Then, generate the hash table variable, using a name unlikely to cause conflicts. Finally, use the `quote` template to generate the return code, which includes the hash table variable name, the single parameter's name and type, and the input function's return type.

## An Extension of the dprint Macro

This section initially used a macro for printing expressions as an example, but that macro could only accept one expression at a time. The goal is to extend this macro to accept multiple expressions separated by commas. Below demonstrates how to use `parseExprFragment` to achieve this functionality.

The macro implementation is as follows:

<!-- verify -macro15 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro dprint2(input: Tokens) {
    let exprs = ArrayList<Expr>()
    var index: Int64 = 0
    while (true) {
        let (expr, nextIndex) = parseExprFragment(input, startFrom: index)
        exprs.add(expr)
        if (nextIndex == input.size) {
            break
        }
        if (input[nextIndex].kind != TokenKind.COMMA) {
            diagReport(DiagReportLevel.ERROR, input[nextIndex..nextIndex+1],
                       "Input must be a comma-separated list of expressions",
                       "Expected comma")
        }
        index = nextIndex + 1  // Skip comma
    }
    let result = quote()
    for (expr in exprs) {
        result.append(quote(
            print($(expr.toTokens().toString()) + " = ")
            println($(expr))
        ))
    }
    return result
}
```

Usage example:

<!-- verify -macro15 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

main() {
    let x = 3
    let y = 2
    @dprint2(x, y, x + y)
}
```

Output result:

<!-- verify -macro15 -->

```text
x = 3
y = 2
x + y = 5
```

In the macro implementation, a while loop is used to parse each expression sequentially starting from index 0. The variable `index` stores the current parsing position. Each time `parseExprFragment` is called, it starts from the current position and returns the parsed position (along with the parsed expression). If the parsed position reaches the end of input, the loop exits. Otherwise, it checks whether the reached position contains a comma - if not, it reports an error and exits; if it is a comma, it skips the comma and starts the next parsing cycle. After obtaining the expression list, each expression is output sequentially.

## A Simple DSL

This case demonstrates how to use macros to implement a simple DSL (Domain Specific Language). LINQ (Language Integrated Query) is a component of Microsoft's .NET framework that provides a unified data query syntax, allowing developers to use SQL-like query statements to manipulate various data sources. Here, we only demonstrate support for the simplest LINQ syntax.

The desired syntax is:

```text
from <variable> in <list> where <condition> select <expression>
```

Where `variable` is an identifier, and `list`, `condition`, and `expression` are all expressions. Therefore, the macro implementation strategy involves sequentially extracting the identifier and expressions while verifying that intermediate keywords are correct. Finally, it generates query results composed of the extracted parts.

The macro implementation is as follows:

<!-- verify -macro16 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro linq(input: Tokens) {
    let syntaxMsg = "Syntax is \"from <attrib> in <table> where <cond> select <expr>\""
    if (input.size == 0 || input[0].value != "from") {
        diagReport(DiagReportLevel.ERROR, input[0..1], syntaxMsg,
                   "Expected keyword \"from\" here.")
    }
    if (input.size <= 1 || input[1].kind != TokenKind.IDENTIFIER) {
        diagReport(DiagReportLevel.ERROR, input[1..2], syntaxMsg,
                   "Expected identifier here.")
    }
    let attribute = input[1]
    if (input.size <= 2 || input[2].value != "in") {
        diagReport(DiagReportLevel.ERROR, input[2..3], syntaxMsg,
                   "Expected keyword \"in\" here.")
    }
    var index: Int64 = 3
    let (table, nextIndex) = parseExprFragment(input, startFrom: index)
    if (nextIndex == input.size || input[nextIndex].value != "where") {
        diagReport(DiagReportLevel.ERROR, input[nextIndex..nextIndex+1], syntaxMsg,
                   "Expected keyword \"where\" here.")
    }
    index = nextIndex + 1  // Skip 'where'
    let (cond, nextIndex2) = parseExprFragment(input, startFrom: index)
    if (nextIndex2 == input.size || input[nextIndex2].value != "select") {
        diagReport(DiagReportLevel.ERROR, input[nextIndex2..nextIndex2+1], syntaxMsg,
                   "Expected keyword \"select\" here.")
    }
    index = nextIndex2 + 1  // Skip 'select'
    let (expr, nextIndex3) = parseExprFragment(input, startFrom: index)

    return quote(
        for ($(attribute) in $(table)) {
            if ($(cond)) {
                println($(expr))
            }
        }
    )
}
```

Usage example:

<!-- verify -macro16 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

main() {
    @linq(from x in 1..=10 where x % 2 == 1 select x * x)
}
```

This example filters odd numbers from the list 1, 2, ... 10 and returns the squares of all odd numbers. The output result is:

<!-- verify -macro16 -->

```text
1
9
25
49
81
```

As can be seen, a significant portion of the macro implementation is dedicated to parsing and validating input Tokens, which is crucial for the macro's usability. Actual LINQ languages (and most DSLs) have more complex syntax and require a complete parsing mechanism to determine what to parse next by identifying different keywords or connectors.
