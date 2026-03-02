# Basic Operators

Operators are symbols that perform specific mathematical or logical operations. For example, the mathematical operator plus (`+`) can add two numbers (e.g., `let i = 1 + 2`), and the logical operator AND (`&&`) can be used to combine and ensure multiple conditional judgments are satisfied (e.g., `if (i > 0 && i < 10)`).

The Cangjie programming language not only supports various commonly used operators but also improves some of them to reduce common coding errors. For instance, the type of an assignment expression (an expression containing an assignment operator) is Unit, and its value is `()`. If you write `if(a = 3)` instead of `if(a == 3)`, the return value of the assignment expression is not of Boolean type, resulting in a compilation error. This helps avoid the issue of mistakenly using the assignment operator (`=`) instead of the equality operator (`==`). The results of arithmetic operators (`+`, `-`, `*`, `/`, `%`, etc.) are checked to prevent value overflow, thereby avoiding abnormal results when saving variables that exceed their type's capacity.

The Cangjie programming language also provides range operators, such as `a..b` or `a..=b`, which conveniently express a range of values.

This chapter only describes the basic operators in the Cangjie programming language. For other operators, refer to the [Operators](../Appendix/operator.md) section in the appendix. For information on how to overload operators for custom types, see the [Operator Overloading](../function/operator_overloading.md) chapter.

## Assignment Operator

Used to modify the value of the left operand to the value of the right operand, requiring that the type of the right operand be a subtype of the left operand's type. When evaluating an assignment expression, the expression on the right side of `=` is always evaluated first, followed by the expression on the left side of `=`, and finally, the assignment is performed.

<!-- compile.error -->

```cangjie
main(): Int64 {
    var a = 1
    var b = 1
    a = (b = 0) // Compilation error: the type of the assignment expression is Unit, and its value is ()
    if (a = 5) { // Compilation error: the type of the assignment expression is Unit, and its value is ()
    }
    a = b = 0 // Syntax error: chained use of assignments is not supported

    return 0
}
```

A multiple assignment expression is a special type of assignment expression. The left side of the equals sign in a multiple assignment expression must be a tuple ([Tuple](tuple.md)), and the elements in this tuple must all be lvalues. The right side of the expression must also be of tuple type, and each element in the right tuple must be a subtype of the corresponding lvalue's type on the left. **Notably, when `_` appears in the left tuple, it indicates that the evaluation result of the corresponding position in the right tuple should be ignored** (meaning the type check for this position will always pass). A multiple assignment expression can assign the values of the right tuple to the corresponding lvalues in the left tuple in one go, eliminating the need for individual assignments.

<!-- run -->

```cangjie
main(): Int64 {
    var a: Int64
    var b: Int64
    (a, b) = (1, 2) // a = 1, b = 2
    (a, b) = (b, a) // Swap: a = 2, b = 1
    (a, _) = (3, 4) // a = 3
    (_, _) = (5, 6) // No assignment
    return 0
}
```

## Arithmetic Operators

The Cangjie programming language supports the following arithmetic operators: unary minus (`-`), addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), remainder (`%`), and exponentiation (`**`). Except for the unary minus, which is a unary prefix operator, all other operators are binary infix operators.

The operand of the unary minus (`-`) can only be a numeric-type expression. The value of a unary prefix minus expression is equal to the negative of its operand, and its type is the same as the operand's type:

<!-- compile -->

```cangjie
    let num1: Int64 = 8
    let num2 = -num1 // num2 = -8, its data type is "Int64".
    let num3 = -(-num1) // num3 = 8, its data type is "Int64".
```

For the binary operators `*`, `/`, `%`, `+`, and `-`, the types of the two operands must be the same. The `%` operator only supports integer operands; `*`, `/`, `+`, and `-` can operate on any numeric type.

> **Note:**
>
> - When the operands of division (`/`) are integers, non-integer values are rounded toward 0 to become integers.
> - The value of the integer remainder operation `a % b` is defined as `a - b * (a / b)`.
> - The addition operator can also be used for string concatenation.

<!-- compile -->

```cangjie
    let a = 2 + 3    // a = 5
    let b = 3 - 1    // b = 2
    let c = 3 * 4    // c = 12
    let d = 7 / 3    // d = 2
    let e = 7 / -3   // e = -2, when encountering "-", it has higher precedence.
    let f = -7 / 3   // f = -2
    let g = -7 / -3  // g = 2, when encountering "-", it has higher precedence.
    let h = 4 % 3    // h = 1
    let i = 4 % -3   // i = 1, when encountering "-", it has higher precedence.
    let j = -4 % 3   // j = -1
    let k = -4 % -3  // k = -1, when encountering "-", it has higher precedence.

    let s1 = "abc"
    var s2 = "ABC"
    let r1 = s1 + s2 // r1 = "abcABC"
```

`**` represents exponentiation (e.g., `x**y` calculates the base x raised to the power of y). The left operand of `**` can only be of type Int64 or Float64.

> **Note:**
>
> When the left operand is of type Int64, the right operand can only be of type UInt64, and the expression's type is Int64.
> When the left operand is of type Float64, the right operand can be of type Int64 or Float64, and the expression's type is Float64.

<!-- compile -->

```cangjie
    let p1 = 2 ** 3                  // p1 = 8
    let p2 = 2 ** UInt64(3 ** 2)     // p2 = 512
    let p3 = 2.0 ** 3                // p3 = 8.0
    let p4 = 2.0 ** 3 ** 2           // p4 = 512.0
    let p5 = 2.0 ** 3.0              // p5 = 8.0
    let p6 = 2.0 ** 3.0 ** 2.0       // p6 = 512.0
```

## Compound Assignment Operators

The Cangjie programming language also provides compound assignment operators: `**=`, `*=`, `/=`, `%=`, `+=`, `-=`, `<<=`, `>>=`, `&=`, `^=`, `|=`, `&&=`, and `||=`. Simple examples are as follows:

<!-- compile -->

```cangjie
    var a: Int64 = 10
    a += 2   // a = 12
    a -= 2   // a = 10
    a **= 2  // a = 100
    a *= 2   // a = 200
    a /= 10  // a = 20
    a %= 6   // a = 2
    a <<= 2  // a = 8
```

When evaluating a compound assignment expression, the lvalue of the left expression is always evaluated first, then the rvalue is taken from this lvalue, and this rvalue is computed with the right expression (short-circuit rules are followed if applicable), and finally, the assignment is performed. Since a compound assignment expression is also an assignment expression, compound assignment operators are non-associative. Compound assignment expressions also require the two operands to be of the same type.

<!-- compile -->

```cangjie
func foo(p: Point): Point {
    p.x += 10
    return p
}

open class Point {
    var x: Int64 = 0
    public init (a: Int64) {
        x = a
    }
}

main() {
    var a = Point(9)    // a.x == 9
    var b = 2

    foo(a).x += (b + b) // a.x == 23
    println(a.x)
}
```

The above example demonstrates the evaluation order of compound assignment expressions. First, the value of `foo(a).x` is evaluated, resulting in `a.x` being 19; then, the value of `b + b` is computed and added to `a.x`.

## Relational Operators

Relational operators include six types: equality (`==`), inequality (`!=`), less than (`<`), less than or equal to (`<=`), greater than (`>`), and greater than or equal to (`>=`). Relational operators are all binary operators and require the two operands to be of the same type. The type of a relational expression is Bool, meaning its value can only be true or false.

Examples of relational expressions:

<!-- compile -->

```cangjie
main(): Int64 {
    3 < 4        // true
    3 <= 3       // true
    3 > 4        // false
    3 >= 3       // true
    3.14 == 3.15 // false
    3.14 != 3.15 // true
    return 0
}
```

For tuple types, a tuple type supports equality (`==`) and inequality (`!=`) operations only if all its elements support these operations; otherwise, the tuple type does not support `==` and `!=` (using them will result in a compilation error). Two instances of the same tuple type are equal if and only if all elements at the same positions (indices) are equal (meaning their lengths are equal).

<!-- compile.error -->

```cangjie
    var isTrue: Bool = (1, 3) == (0, 2) // false
    isTrue = (1, "123") == (1.0, 2)      // Compilation error: the types of the two operands are inconsistent
    isTrue = (1, _) == (1.0, _)          // Compilation error: wildcards cannot be used as tuple elements for matching
```

## Coalescing Operator

The coalescing operator is denoted by `??`, which is a binary infix operator. The coalescing operator is used for destructuring [Option types](../enum_and_pattern_match/option_type.md).

For the expression `e1 ?? e2`, when the value of e1 is `Option<T>.Some(v)`, the value of `e1 ?? e2` is equal to the value of v (in this case, e2 is not evaluated, satisfying "short-circuit evaluation"); when the value of e1 is `Option<T>.None`, the value of `e1 ?? e2` is equal to the value of e2.

Examples of coalescing expressions:

<!-- run -->

```cangjie
main(): Int64 {
    let v1 = Option<Int64>.Some(100)
    let v2 = Option<Int64>.None
    let r1 = v1 ?? 0
    let r2 = v2 ?? 0
    print("${r1}") // 100
    print("${r2}") // 0
    return 0
}
```

## Range Operators

There are two types of range operators: `..` and `..=`, used to create "left-closed right-open" and "left-closed right-closed" range instances, respectively. For more details, refer to the [Range Type](./range.md).

## Logical Operators

The Cangjie programming language supports three logical operators: logical NOT (`!`), logical AND (`&&`), and logical OR (`||`).

Logical NOT (`!`) is a unary operator that negates the Boolean value of its operand: `!false` equals `true`, and `!true` equals `false`.

<!-- compile -->

```cangjie
    var a: Bool = true     // a = true
    var b: Bool = !a       // b = false
    var c: Bool = !false   // c = true
```

Logical AND (`&&`) and logical OR (`||`) are both binary operators. For the expression `expr1 && expr2`, its value is `true` only if both `expr1` and `expr2` are `true`; for the expression `expr1 || expr2`, its value is `false` only if both `expr1` and `expr2` are `false`.

<!-- compile -->

```cangjie
    var a: Bool = true && true    // a = true
    var b: Bool = true && false   // b = false
    var c: Bool = false && false  // c = false
    var d: Bool = false && true   // d = false

    a = true || true              // a = true
    b = true || false             // b = true
    c = false || false            // c = false
    d = false || true             // d = true
```

Logical AND (`&&`) and logical OR (`||`) use short-circuit evaluation: when evaluating `expr1 && expr2`, if `expr1=false`, `expr2` is not evaluated, and the entire expression's value is `false`; when evaluating `expr1 || expr2`, if `expr1=true`, `expr2` is not evaluated, and the entire expression's value is `true`.

<!-- run -->

```cangjie
func isEven(a: Int64): Bool {
    if((a % 2) == 0) {
         println("${a} is an even number")
         true
    } else {
        println("${a} is not an even number")
        false
    }
}


main() {
    var a: Bool = isEven(2) && isEven(20)
    var b: Bool = isEven(3) && isEven(30) // isEven(3) returns false, b is false, isEven(30) is not evaluated

    a = isEven(4) || isEven(40)  // isEven(4) returns true, a is true, isEven(40) is not evaluated
    b = isEven(5) || isEven(50)
}
```

## Bitwise Operators

The Cangjie programming language supports one unary prefix bitwise operator: bitwise NOT (`!`), and five binary infix bitwise operators: left shift (`<<`), right shift (`>>`), bitwise AND (`&`), bitwise XOR (`^`), and bitwise OR (`|`). The operands of bitwise operators can only be integer types. Bitwise operations are performed by treating operands as binary sequences and applying logical operations (0 as false, 1 as true) or shift operations on each bit.

For shift operators, the operands must be integer types (but the two operands can be different integer types, e.g., the left operand is Int8, and the right operand is Int16). Additionally, the right operand cannot be negative for both left and right shifts (such errors detected at compile time will result in compilation errors; if they occur at runtime, an exception is thrown). For unsigned numbers, the shift and padding rules are: left shifts pad the low bits with 0 and discard the high bits, while right shifts pad the high bits with 0 and discard the low bits. For signed numbers, the shift and padding rules are:

1. Positive numbers follow the same padding rules as unsigned numbers;
2. Negative numbers pad the low bits with 0 for left shifts and discard the high bits;
3. Negative numbers pad the high bits with 1 for right shifts and discard the low bits.

Moreover, if the number of bits to shift (right operand) is equal to or exceeds the operand's width, it is considered a shift overflow. If detected at compile time, it results in an error; otherwise, a runtime exception is thrown.

<!-- compile -->

```cangjie
    var a = !10                 // -11, conforms to shift and padding rules
    a = !20                     // -21, conforms to shift and padding rules
    a = 10 << 1                 // 20, conforms to shift and padding rules
    // a = 1000 << -1           // Compilation error: shift operation overflow (right operand cannot be negative)
    // a = 1000 << 100000000000 // Compilation error: shift operation overflow (shift out of bounds)
    a = 10 << 1 << 1            // 40, conforms to shift and padding rules
    a = 10 >> 1                 // 5, conforms to shift and padding rules
    a = 10 & 15                 // 10
    a = 10 ^ 15                 // 5
    a = 10 | 15                 // 15
    a = (1 ^ (8 & 15)) | 24     // 25
```

## Increment and Decrement Operators

The increment (`++`) and decrement (`--`) operators perform operations to increase or decrease a value by 1 and can only be used as postfix operators. The increment (`++`) and decrement (`--`) operators are non-associative.

For the expression `expr++` (or `expr--`), the following rules apply:

1. The type of `expr` must be an integer type;
2. Since `expr++` (or `expr--`) is syntactic sugar for `expr += 1` (or `expr -= 1`), `expr` must also be assignable;
3. The type of `expr++` (or `expr--`) is Unit.

Examples of increment and decrement expressions:

<!-- compile.error -->

```cangjie
    var i: Int32 = 5
    i++              // i = 6
    i--              // i = 5
    i--++            // Syntax error
    var j = 0
    j = i--          // Semantic error
```