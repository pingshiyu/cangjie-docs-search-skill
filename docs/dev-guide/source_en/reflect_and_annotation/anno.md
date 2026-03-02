# Annotations

Cangjie provides several built-in compilation markers to support special case handling.

## Built-in Compilation Markers for Integer Overflow Handling Strategies

Cangjie offers three built-in compilation markers to control integer overflow handling strategies: `@OverflowThrowing`, `@OverflowWrapping`, and `@OverflowSaturating`. These markers can currently only be applied to function declarations and affect integer operations and type conversions within the function. They correspond to the following three overflow handling strategies:

1. **Throwing Exceptions (throwing)**: Throws an exception when integer overflow occurs.

    <!-- compile -->

    ```cangjie
    @OverflowThrowing
    func add(a: Int8, b: Int8){
        return a + b
    }
    main() {
        add(100,29)
        /* Mathematically, 100 + 29 equals 129,
        * which causes an upper overflow in Int8's range,
        * resulting in an exception being thrown
        */
    }
    ```

    Note: For scenarios where integer overflow behavior is set to throwing, if the overflow can be detected at compile time, the compiler will directly report an error.

    <!-- compile.error -->

    ```cangjie
    @OverflowThrowing
    main() {
        let res: Int8 = Int8(100) + Int8(29) // Error, arithmetic operation '+' overflow
        // Mathematically, 100 + 29 equals 129, causing an upper overflow in Int8's range; the compiler detects and reports this
        let con: UInt8 = UInt8(-132) // Error, integer type conversion overflow
        /* -132 causes a lower overflow in UInt8's range,
        * resulting in an exception being thrown
        */
    }
    ```

2. **Wrapping (wrapping)**: When the result of an integer operation exceeds the representable range of the receiving memory space, the excess bits are truncated.

    <!-- compile -->

    ```cangjie
    @OverflowWrapping
    main() {
        let res: Int8 = Int8(105) * Int8(4)
        /* Mathematically, 105 * 4 equals 420,
        * whose binary representation is 1 1010 0100,
        * exceeding the 8-bit memory space for the result.
        * The truncated result is represented as 1010 0100 in binary,
        * corresponding to the signed integer -92
        */
        let temp: Int16 = Int16(-132)
        let con: UInt8 = UInt8(temp)
        /* -132's binary representation is 1111 1111 0111 1100,
        * exceeding the 8-bit memory space for the result.
        * The truncated result is represented as 0111 1100 in binary,
        * corresponding to the signed integer 124
        */
    }
    ```

3. **Saturating (saturating)**: When integer overflow occurs, the result is set to the extreme value of the corresponding fixed precision.

    <!-- compile -->

    ```cangjie
    @OverflowSaturating
    main() {
        let res: Int8 = Int8(-100) - Int8(45)
        /* Mathematically, -100 - 45 equals -145,
        * which causes a lower overflow in Int8's range,
        * so Int8's minimum value -128 is chosen as the result
        */
        let con: Int8 = Int8(1024)
        /* 1024 causes an upper overflow in Int8's range,
        * so Int8's maximum value 127 is chosen as the result
        */
    }
    ```

By default (i.e., when no such built-in compilation marker is applied), the throwing exception (`@OverflowThrowing`) strategy is used.

In practice, the overflow strategy should be chosen based on business requirements. For example, to implement a secure operation on `Int32` where the calculation result must mathematically match the computation process, the throwing exception strategy should be used.

**Counterexample:**

<!-- compile -->

```cangjie
// The result is truncated
@OverflowWrapping
func operation(a: Int32, b: Int32): Int32 {
    a + b // No exception will be thrown when overflow occurs
}
```

This incorrect example uses the wrapping overflow strategy. For instance, when the parameters `a` and `b` are large enough to cause overflow, the result will be truncated, leading to a mismatch between the function's return value and the mathematical expression `a + b`.

**Correct Example:**

<!-- run -->

```cangjie
// Secure
@OverflowThrowing
func operation(a: Int32, b: Int32): Int32 {
    a + b
}

main(): Int64 {
    try {
        operation(Int32.Max, 1)
    } catch (e: ArithmeticException) {
        println(e.message)
        //Handle error
    }
    0
}
```

This correct example uses the throwing exception strategy. When the parameters `a` and `b` cause integer overflow, the `operation` function throws an exception.

The following table summarizes mathematical operators that may cause integer overflow.

| Operator | Overflow |          Operator          | Overflow |          Operator         | Overflow | Operator | Overflow |
|:----:|:--:|:--------------------:|:--:|:-------------------:|:--:|:----:|:--:|
| `+`  | Y  |         `-=`         | Y  |        `<<`         | N  | `<`  | N  |
| `-`  | Y  |         `*=`         | Y  |        `>>`         | N  | `>`  | N  |
| `*`  | Y  |         `/=`         | Y  |         `&`         | N  | `>=` | N  |
| `/`  | Y  |         `%=`         | N  | <code>&vert;</code> | N  | `<=` | N  |
| `%`  | N  |        `<<=`         | N  |         `^`         | N  | `==` | N  |
| `++` | Y  |        `>>=`         | N  |        `**=`        | Y  |      |    |
| `--` | Y  |         `&=`         | N  |         `!`         | N  |      |    |
| `=`  | N  | <code>&vert;=</code> | N  |        `!=`         | N  |      |    |
| `+=` | Y  |         `^=`         | N  |        `**`         | Y  |      |    |

## Test Framework Built-in Compilation Markers

When using mocks in tests, if the mocked object involves static or top-level declarations, the test framework's built-in compilation marker `@EnsurePreparedToMock` must be used to instruct the compiler to prepare these declarations for mocking.

This marker can only be applied to lambda expressions where the last expression calls a static or top-level declaration. The compiler will then prepare this declaration for mocking.

Example:

<!-- run -pkg1 -->
<!-- cfg="-p prod --mock=on --output-type=dylib" -->

```cangjie
package prod

public func test(a: String, b: String): String {
    a + b
}
```

<!-- run -pkg1 -->
<!-- cfg="-lprod -L . --test" -->

```cangjie
package test

import prod.*
import std.unittest.mock.*

@Test
public class TestA {
    @TestCase
    func case1(): Unit {
        { =>
            let matcher0 = Matchers.eq("z")
            let matcher1 = Matchers.eq("y")
            let stubCall = @EnsurePreparedToMock { => return(test(matcher0.value(), matcher1.value())) }
            ConfigureMock.stubFunction(stubCall,[matcher0.withDescription(#"eq("z")"#), matcher1.withDescription(#"eq("y")"#)], Option<String>.None, "test", #"test("z", "y")"#, 15)
        }().returns("mocked value")
        println(test("z", "y")) // prints "mocked value"
    }
}
```

In this example, `ConfigureMock.stubFunction` registers a stub for the function `test`, and `returns` sets the stub's return value.

> **Note:**
>
> Typically, the standard library's mock interfaces should be used to define mock declarations. Direct use of `@EnsurePreparedToMock` is discouraged unless necessary. Standard library functions internally use this marker when needed.

Constraints for using `@EnsurePreparedToMock`:

- Only allowed when compiling with test and mock-related options (`--test`/`--test-only` and `--mock=on`/`--mock=runtime-error`).
- Can only be applied to lambdas with a suitable last expression.
- The lambda's last expression must be a call, member access, or reference expression involving:
    - Top-level functions or variables;
    - Static functions, properties, or fields;
    - Foreign declarations;
    - Not local functions or variables;
    - Non-private declarations;
    - Not const expressions or declarations;
    - Must be from a package built in mock mode.

## Custom Annotations

Custom annotations allow reflection (see [Reflection Chapter](dynamic_feature.md)) to retrieve additional metadata beyond type information, enabling more complex logic.

Developers can create custom annotations by marking a `class` with `@Annotation`. The `class` must not be `abstract`, `open`, or `sealed`, and must provide at least one `const init` function; otherwise, the compiler will report an error.

The following example defines a custom annotation `@Version` and applies it to classes `A`, `B`, and `C`. In `main`, reflection is used to retrieve and print the `@Version` annotation information.

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Version {
    let code: String
    const init(code: String) {
        this.code = code
    }
}

@Version["1.0"]
class A {}

@Version["1.1"]
class B {}

main() {
    let objects = [A(), B()]
    for (obj in objects) {
        let annOpt = TypeInfo.of(obj).findAnnotation<Version>()
        if (let Some(ann) <- annOpt) {
            println(ann.code)
        }
    }
}
```

Compiling and running this code outputs:

```text
1.0
1.1
```

Annotation information must be generated at compile time and bound to the type. Custom annotations must be instantiated using `const init` with valid arguments. The annotation declaration syntax is similar to macro declarations, where the `[]` brackets must contain const expressions in order or named parameter rules (see [Constant Evaluation Chapter](../function/const_func_and_eval.md)). For annotation types with a no-argument `const init`, the brackets can be omitted.

The following example defines a custom annotation `@Marked` with a no-argument `const init`. Both `@Marked` and `@Marked[]` are valid usages.

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Marked {
    const init() {}
}

@Marked
class A {}

@Marked[]
class B {}

main() {
    if (TypeInfo.of(A()).findAnnotation<Marked>().isSome()) {
        println("A is Marked")
    }
    if (TypeInfo.of(B()).findAnnotation<Marked>().isSome()) {
        println("B is Marked")
    }
}
```

Compiling and running this code outputs:

```text
A is Marked
B is Marked
```

The same annotation class cannot be applied multiple times to the same target (i.e., no duplicate annotations).

<!-- verify.error -->
<!-- cfg="--Marked" -->

```cangjie
@Marked
@Marked // Error
class A {}
````Annotation` is not inherited, therefore a type's annotation metadata only comes from the annotations declared during its definition. If annotation metadata from a parent type is needed, developers must manually query it using reflection interfaces.

In the following example, `A` is annotated with `@Marked`, `B` inherits from `A`, but `B` does not inherit `A`'s annotation.

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Marked {
    const init() {}
}

@Marked
open class A {}

class B <: A {}

main() {
    if (TypeInfo.of(A()).findAnnotation<Marked>().isSome()) {
        println("A is Marked")
    }
    if (TypeInfo.of(B()).findAnnotation<Marked>().isSome()) {
        println("B is Marked")
    }
}
```

When compiling and executing the above code, the output is:

```text
A is Marked
```

Custom annotations can be applied to type declarations (`class`, `struct`, `enum`, `interface`), parameters in member functions/constructors, constructor declarations, member function declarations, member variable declarations, and member property declarations. They can also restrict their applicable locations to prevent misuse by developers. Such annotations need to specify the `target` parameter when declaring `@Annotation`, with the parameter type being `Array<AnnotationKind>`. Here, `AnnotationKind` is an `enum` defined in the standard library. When no target is specified, the custom annotation can be used in all the aforementioned locations. When targets are specified, it can only be used in the declared list.

<!-- compile -->

```cangjie
public enum AnnotationKind {
    | Type
    | Parameter
    | Init
    | MemberProperty
    | MemberFunction
    | MemberVariable
}
```

In the following example, a custom annotation is restricted via `target` to only be applicable to member functions. Using it in other locations will cause a compilation error.

<!--compile.error -->

```cangjie
@Annotation[target: [MemberFunction]]
public class Marked {
    const init() {}
}

class A {
    @Marked // OK, member function
    func marked() {}
}

@Marked // Error, type
class B {}
```