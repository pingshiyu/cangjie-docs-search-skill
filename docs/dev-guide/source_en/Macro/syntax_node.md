# Syntax Nodes

In the compilation process of the Cangjie language, the code is first converted into `Tokens` through lexical analysis, followed by syntactic parsing of the `Tokens` to generate a syntax tree. Each node in the syntax tree may represent an expression, declaration, type, pattern, etc. The Cangjie standard library `std.ast` package provides corresponding classes for each type of node, with appropriate inheritance relationships. The main abstract classes are as follows:

- `Node`: The parent class of all syntax nodes
- `TypeNode`: The parent class of all type nodes
- `Expr`: The parent class of all expression nodes
- `Decl`: The parent class of all declaration nodes
- `Pattern`: The parent class of all pattern nodes

There are numerous specific node types. For detailed information, please refer to the *Cangjie Programming Language Library API*. The following examples primarily use the following nodes:

- `BinaryExpr`: Binary operation expressions
- `FuncDecl`: Function declarations

## Parsing Nodes

Using the `std.ast` standard library package, virtually any node can be parsed from `Tokens`. There are two methods for parsing `Tokens` and constructing syntax nodes.

### Parsing Tokens Using Parsing Functions

The following functions are used to parse and construct arbitrary syntax nodes from `Tokens`:

- `parseExpr(input: Tokens): Expr`: Parses the input `Tokens` into an expression node.
- `parseExprFragment(input: Tokens, startFrom!: Int64 = 0): (Expr, Int64)`: Parses a fragment of the input `Tokens` into an expression node, starting from the `startFrom` index. The parsing may consume only part of the fragment starting from `startFrom` and returns the index of the first unconsumed `Token` (if the entire fragment is consumed, the return value is `input.size`).
- `parseDecl(input: Tokens, astKind!: String = "")`: Parses the input `Tokens` into a declaration node. `astKind` provides additional settings; refer to the *Cangjie Programming Language Library API* for details.
- `parseDeclFragment(input: Tokens, startFrom!: Int64 = 0): (Decl, Int64)`: Parses a fragment of the input `Tokens` into a declaration node. The `startFrom` parameter and the meaning of the returned index are the same as in `parseExpr`.
- `parseType(input: Tokens): TypeNode`: Parses the input `Tokens` into a type node.
- `parseTypeFragment(input: Tokens, startFrom!: Int64 = 0): (TypeNode, Int64)`: Parses a fragment of the input `Tokens` into a type node. The `startFrom` parameter and the meaning of the returned index are the same as in `parseExpr`.
- `parsePattern(input: Tokens): Pattern`: Parses the input `Tokens` into a pattern node.
- `parsePatternFragment(input: Tokens, startFrom!: Int64 = 0): (Pattern, Int64)`: Parses a fragment of the input `Tokens` into a pattern node. The `startFrom` parameter and the meaning of the returned index are the same as in `parseExpr`.

If parsing fails, an exception is thrown. This parsing method is suitable for code fragments of unknown types. If a specific subtype node is required, the parsing result must be manually cast to the corresponding subtype.

Usage examples of these functions are shown below:

<!-- verify -->

```cangjie
let tks1 = quote(a + b)
let tks2 = quote(u + v, x + y)
let tks3 = quote(
    func f1(x: Int64) { return x + 1 }
)
let tks4 = quote(
    func f2(x: Int64) { return x + 2 }
    func f3(x: Int64) { return x + 3 }
)

let binExpr1 = parseExpr(tks1)
let (binExpr2, mid) = parseExprFragment(tks2)
let (binExpr3, _) = parseExprFragment(tks2, startFrom: mid + 1) // Skip the comma
println("binExpr1 = ${binExpr1.toTokens()}")
println("binExpr2 = ${binExpr2.toTokens()}, binExpr3 = ${binExpr3.toTokens()}")
let funcDecl1 = parseDecl(tks3)
let (funcDecl2, mid2) = parseDeclFragment(tks4)
let (funcDecl3, _) = parseDeclFragment(tks4, startFrom: mid2)
println("${funcDecl1.toTokens()}")
println("${funcDecl2.toTokens()}")
println("${funcDecl3.toTokens()}")
```

Output:

```text
binExpr1 = a + b
binExpr2 = u + v, binExpr3 = x + y
func f1(x: Int64) {
    return x + 1
}

func f2(x: Int64) {
    return x + 2
}

func f3(x: Int64) {
    return x + 3
}
```

### Parsing Tokens Using Syntax Node Constructors

Most syntax nodes support the `init(input: Tokens)` constructor, which parses the input `Tokens` into a node of the corresponding type. For example:

<!-- run -->

```cangjie
import std.ast.*

let binExpr = BinaryExpr(quote(a + b))
let funcDecl = FuncDecl(quote(func f1(x: Int64) { return x + 1 }))
```

If parsing fails, an exception is thrown. This parsing method is suitable for code fragments of known types, eliminating the need for manual casting to specific subtypes after parsing.

## Components of Nodes

After parsing nodes from `Tokens`, you can examine their components. For illustration, only the components of `BinaryExpr` and `FuncDecl` are listed here. For more detailed explanations of other nodes, refer to the *Cangjie Programming Language Library API*.

- `BinaryExpr` node:
    - `leftExpr: Expr`: The expression on the left side of the operator
    - `op: Token`: The operator
    - `rightExpr: Expr`: The expression on the right side of the operator
- `FuncDecl` node (partial):
    - `identifier: Token`: The function name
    - `funcParams: ArrayList<FuncParam>`: The parameter list
    - `declType: TypeNode`: The return type
    - `block: Block`: The function body
- `FuncParam` node (partial):
    - `identifier: Token`: The parameter name
    - `paramType: TypeNode`: The parameter type
- `Block` node (partial):
    - `nodes: ArrayList<Node>`: Expressions and declarations within the block

Each component is a `public mut prop` and can be inspected and updated. The results of such updates are demonstrated in the following examples.

### BinaryExpr Example

<!-- verify -->

```cangjie
let binExpr = BinaryExpr(quote(x * y))
binExpr.leftExpr = BinaryExpr(quote(a + b))
println(binExpr.toTokens())

binExpr.op = Token(TokenKind.ADD)
println(binExpr.toTokens())
```

Output:

```text
(a + b) * y
a + b + y
```

First, parsing yields `binExpr` as the node `x * y`, represented as:

```text
    *
  /   \
 x     y
```

Next, the left node (`x`) is replaced with `a + b`, resulting in the following syntax tree:

```text
      *
    /   \
   +     y
  / \
 a   b
```

When outputting this syntax tree, parentheses must be added around `a + b` to yield `(a + b) * y` (outputting `a + b * y` would imply multiplication before addition, which contradicts the syntax tree's meaning). The `ast` library automatically adds parentheses when outputting syntax trees.

Finally, the operator at the root of the syntax tree is changed from `*` to `+`, resulting in:

```text
      +
    /   \
   +     y
  / \
 a   b
```

This syntax tree can be output as `a + b + y` since addition is left-associative and does not require parentheses on the left side.

### FuncDecl Example

<!-- verify -->

```cangjie
let funcDecl = FuncDecl(quote(func f1(x: Int64) { x + 1 }))
funcDecl.identifier = Token(TokenKind.IDENTIFIER, "foo")
println("Number of parameters: ${funcDecl.funcParams.size}")
funcDecl.funcParams[0].identifier = Token(TokenKind.IDENTIFIER, "a")
println("Number of nodes in body: ${funcDecl.block.nodes.size}")
let binExpr = (funcDecl.block.nodes[0] as BinaryExpr).getOrThrow()
binExpr.leftExpr = parseExpr(quote(a))
println(funcDecl.toTokens())
```

In this example, a `FuncDecl` node is first constructed through parsing. The function name, parameter name, and part of the expression in the function body are then modified. Output:

```text
Number of parameters: 1
Number of nodes in body: 1
func foo(a: Int64) {
    a + 1
}
```

## Interpolating Syntax Nodes Using `quote`

Any syntax node can be interpolated within a `quote` statement. Some `ArrayList` lists of syntax nodes can also be interpolated (primarily corresponding to scenarios where such node lists are encountered in practice). Interpolation is achieved via `$(node)`, where `node` is an instance of any node type.

The following examples demonstrate node interpolation.

<!-- verify -->

```cangjie
var binExpr = BinaryExpr(quote(1 + 2))
let a = quote($(binExpr))
let b = quote($binExpr)
let c = quote($(binExpr.leftExpr))
let d = quote($binExpr.leftExpr)
println("a: ${a.toTokens()}")
println("b: ${b.toTokens()}")
println("c: ${c.toTokens()}")
println("d: ${d.toTokens()}")
```

Output:

```text
a: 1 + 2
b: 1 + 2
c: 1
d: 1 + 2.leftExpr
```

Generally, the expression following the interpolation operator is enclosed in parentheses to define its scope, e.g., `$(binExpr)`. However, when followed by a single identifier, parentheses can be omitted, as in `$binExpr`. Thus, in the example, both `a` and `b` interpolate the `binExpr` node within `quote`, resulting in `1 + 2`. However, if the expression following the interpolation operator is more complex, omitting parentheses may lead to scope errors. For instance, the expression `binExpr.leftExpr` evaluates to the left expression of `1 + 2`, i.e., `1`, so `c` is correctly assigned `1`. However, in `d`, the interpolation is interpreted as `($binExpr).leftExpr`, resulting in `1 + 2.leftExpr`. To clarify the scope of interpolation, it is recommended to use parentheses with the interpolation operator.

The following example demonstrates interpolation of node lists (`ArrayList`).

<!-- verify -->

```cangjie
var incrs = ArrayList<Node>()
for (i in 1..=5) {
    incrs.add(parseExpr(quote(x += $(i))))
}
var foo = quote(
    func foo(n: Int64) {
        let x = n
        $(incrs)
        x
    })
println(foo)
```

Output:

```text
func foo(n: Int64) {
    let x = n
    x += 1
    x += 2
    x += 3
    x += 4
    x += 5
    x
}
```

In this example, a node list `incrs` is created, containing expressions `x += 1`, ..., `x += 5`. Interpolating `incrs` lists the nodes sequentially, with line breaks after each node. This is useful for inserting expressions and declarations that need to be executed sequentially.

The following example demonstrates cases where parentheses are necessary around interpolations to ensure correctness.

<!-- verify -->

```cangjie
var binExpr1 = BinaryExpr(quote(x + y))
var binExpr2 = BinaryExpr(quote($(binExpr1) * z))       // Incorrect: yields x + y * z
println("binExpr2: ${binExpr2.toTokens()}")
println("binExpr2.leftExpr: ${binExpr2.leftExpr.toTokens()}")
println("binExpr2.rightExpr: ${binExpr2.rightExpr.toTokens()}")
var binExpr3 = BinaryExpr(quote(($(binExpr1)) * z))     // Correct: yields (x + y) * z
println("binExpr3: ${binExpr3.toTokens()}")
```

Output:

```text
binExpr2: x + y * z
binExpr2.leftExpr: x
binExpr2.rightExpr: y * z
binExpr3: (x + y) * z
```

First, the expression `x + y` is constructed and then interpolated into the template `$(binExpr1) * z`. The intention is to obtain an expression that first computes `x + y` and then multiplies by `z`. However, the interpolation yields `x + y * z`, which computes `y * z` first and then adds `x`. This occurs because interpolation does not automatically add parentheses to ensure the atomicity of the interpolated expression (unlike the replacement of `leftExpr` described earlier). Thus, parentheses must be added around `$(binExpr1)` to ensure the correct result.