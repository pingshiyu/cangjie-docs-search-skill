# Built-in Compilation Tags

The Cangjie language provides several predefined compilation tags that can be used to control the compilation behavior of the Cangjie compiler.

## Source Location

Cangjie offers several built-in compilation tags for obtaining source code locations during compilation.

- `@sourcePackage()` expands to a `String` type literal containing the package name of the source file where this tag is located.
- `@sourceFile()` expands to a `String` type literal containing the filename of the source file where this tag is located.
- `@sourceLine()` expands to an `Int64` type literal containing the line number in the source file where this tag is located.

These compilation tags can be used within any expression as long as they comply with type-checking rules. Examples:

<!-- run -->

```cangjie
func test1() {
    let s: String = @sourceFile()  // The value of `s` is the current source file name
}

func test2(n!: Int64 = @sourceLine()) { /* at line 5 */
    // The default value of `n` is the source file line number of the definition of `test2`
    println(n) // print 5
}
```

## Conditional Compilation

Conditional compilation uses the `@When` tag, which is a technique for selectively compiling different code segments based on specific conditions within a program. The primary applications of conditional compilation include:

- Platform Adaptation: Supports selective code compilation based on the current compilation environment to achieve cross-platform compatibility.
- Feature Selection: Enables flexible configuration by selectively compiling code according to different requirements.
- Debugging Support: Facilitates compiling debugging-related code in debug mode to enhance program performance and security. For example, compiling debug information or logging-related code in debug mode while excluding it from release builds.
- Performance Optimization: Allows selective code compilation based on predefined conditions to improve program performance.

For detailed information about conditional compilation, please refer to the [Conditional Compilation](../compile_and_build/conditional_compilation.md) chapter, which will not be further elaborated here.

## @FastNative

To improve performance when interoperating with C, Cangjie provides the `@FastNative` tag to optimize calls to C functions. Note that `@FastNative` can only be used with functions declared as `foreign`.

First, compile the following C program to generate the dynamic library file `libcProg.so`:

```c
#include <stdio.h>

char* foo()
{
    static char str[] = "this is an example";
    return str;
}
```

Cangjie file `main.cj`:

<!-- code_no_check -->

```cangjie
@FastNative
foreign func foo(): CPointer<Int32>

@FastNative
foreign func printf(fmt: CPointer<Int32>, ...): Int32

main(): Int32 {
    unsafe{
        let str = foo()
        printf(str)
    }
}
```

For specific compilation instructions, please refer to the [Appendix](../Appendix/compile_options.md#cjc-compilation-options). Below is the corresponding compilation command for this example:

```shell
cjc -L . -lcProg ./main.cj
```

After executing the above command to compile `main.cj`, an executable file `main` is generated, with the following execution result:

```text
this is an example
```

When using `@FastNative` to modify `foreign` functions, developers must ensure that the corresponding `C` functions meet the following two requirements:

1. The overall execution time of the function should not be too long. For example: the function must not contain large loops; it must not exhibit blocking behavior, such as calling `sleep`, `wait`, etc.
2. The function must not call Cangjie methods internally.

## @Frozen

The `@Frozen` annotation can be used to mark functions and properties whose internal implementation is guaranteed not to change in future versions. It signals the developer's commitment to the stability of that function/property across releases. Functions and properties annotated with `@Frozen` must not change their signatures or bodies in subsequent versions. Under the same compiler and compilation options, the generated artifacts for the function or property must therefore remain identical between versions.

The `@Frozen` annotation can only be applied to:

- All kinds of function definitions except local (nested) functions, including global functions, member functions, constructors, primary constructors, and destructors.
- All kinds of member property definitions.

Usage example:

<!-- run -->

```cangjie
@Frozen
public func test(): Unit {}

public class testClass {
    @Frozen
    public func testFunc(): Unit {}

    @Frozen
    public prop testProp: Unit {
        get() {}
    }
}
```

## @Attribute

Cangjie internally provides the `@Attribute` tag, allowing developers to set attribute values for declarations using the built-in `@Attribute` to mark them. Attribute values can be either `identifier` or `string` types. Below is a simple example where the variable `cnt` is given an `identifier`-type attribute `State`, and the variable `bcnt` is given a `string`-type attribute `"Binding"`.

```cangjie
@Attribute[State] var cnt = 0       // identifier
@Attribute["Binding"] var bcnt = 0  // string
```

Additionally, the standard library `std.ast` package provides the `getAttrs()` method to retrieve a node's attributes and the `hasAttr(attrs: String)` method to check whether a node has a specific attribute. Here is a concrete example.

Macro definition:

```cangjie
public macro Component(input: Tokens): Tokens {
    var varDecl = parseDecl(input)
    if (varDecl.hasAttr("State")) { // Returns true if the node is marked with the "State" attribute, otherwise false
        var attrs = varDecl.getAttrs() // Returns a set of Tokens
        println(attrs[0].value)
    }
    return input
}
```

Macro invocation:

```cangjie
@Component(
    @Attribute[State] var cnt = 0
)
```

## @Deprecated

`@Deprecated` indicates that an API is deprecated. While it remains temporarily usable, it will be removed or changed in the future, and developers are advised not to use it. Example:

```cangjie
@Deprecated["Use boo instead", since: "1.3.4"]
func foo() {}

main() {
    foo()
}
```

The compiler will issue a warning during compilation:

```text
warning: function 'foo' is deprecated since 1.3.4. Use boo instead
 ==> file.cj:5:5:
  |
5 |     foo()
  |     ^^^ deprecated
  |
  # note: this warning can be suppressed by setting the compiler option `-Woff deprecated`

1 warning generated, 1 warning printed.
```

The `@Deprecated` custom macro can be applied to the following declarations:

- Classes, interfaces, structs, enums, enum constructors
- Top-level (global) functions or variables
- Static or non-static member functions, member variables, properties, property setters
- Operator functions
- Extension member functions, static functions, properties, or property setters
- Foreign functions or functions declared within foreign blocks
- Constructors and primary constructors
- Abstract functions and properties
- Type aliases (including associated types)
- Named parameters in functions with default arguments
- `const` variables and functions
- Macro definitions
- Annotation classes

### @Deprecated Parameters

- `message: String` - Describes why the declaration is deprecated and how to migrate.
- `since!: ?String` - The version in which the deprecation occurred.
- `strict!: Bool` - Defaults to `false`, triggering a warning at call sites of the marked API. If set to `true`, it triggers a compilation error.

```cangjie
@Deprecated["Use Macro2", since: "1990", strict: true]
public macro Macro(input: Tokens): Tokens {
    return input
}
```