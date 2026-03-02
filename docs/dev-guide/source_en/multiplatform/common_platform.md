# Cross-Platform

Cangjie provides cross-platform development capabilities that address code reuse issues in cross-end development scenarios. Users can differentiate between common code and platform-specific code to share code across different platforms, reducing the time spent on developing and maintaining identical code for different platforms.

> **Note:**
>
> The cross-platform development feature is experimental, and using it may involve risks.

## Introduction to Cross-Platform Development Features

### Common Code and Platform-Specific Code

The platform-agnostic part of a codebase is referred to as common code, which contains code that can run on all target platforms. This typically includes algorithms, business logic, or other modules that do not depend on specific platform functionalities. The platform-dependent part of a codebase is referred to as platform-specific code, which contains code that can only run on specific platforms. This usually involves calls to operating systems, hardware, or other platform-specific functionalities. Both common code and platform-specific code belong to the same package. Platform files can depend on common files, but common files cannot depend on platform files. Common code is used for sharing across different platforms and can be marked with the `common` modifier. Platform-specific code is used to distinguish implementations for different platforms and can be marked with the `platform` modifier. The following rules apply when using the `common`/`platform` modifiers:

- The `common` modifier can only appear in common code, and the `platform` modifier can only appear in platform-specific code.
- The `common`/`platform` modifiers conflict with `private`/`const`/`foreign` modifiers and cannot be used simultaneously.

The following example defines common code and a global function `foo`:

```cangjie
package cmp

public common func foo(): Unit {
    println("I am common")
}
```

The following example defines platform-specific code and a global function `foo`:

```cangjie
package cmp

public platform func foo(): Unit {
    println("I am platform")
}
```

More details will be described in the cross-platform development chapter.

### Types Supporting Cross-Platform Development Features

Below are detailed usage rules for types that support cross-platform development features.

#### Global Functions

Global functions support cross-platform features. Users can use the `common` and `platform` modifiers for global functions.
A `common` global function may or may not include an implementation.

```cangjie
common func foo(): Int64
common func goo(a: Int64): Int64 { 1 }
```

In the above example, two `common` global functions are defined. The function `foo` has no function body, while `goo` includes a function body. Both are valid definitions of `common` global functions.
`common`/`platform` global functions must adhere to the following restrictions:

- A `common` global function must specify its return type.
- If a `common` global function has a complete implementation, a `platform` global function is not required. If a `common` global function lacks a complete implementation, a `platform` global function must be defined.
- The function signature of a `platform` global function must match that of the corresponding `common` global function in the same package, meaning parameter types and return types must be consistent. Additionally, the following rules must be satisfied:
    - The `common` global function and the corresponding platform global function must use the same modifiers (e.g., `public`, `unsafe`, etc.), except for `common`/`platform`.
    - If the `common` global function uses named parameters, the corresponding positions in the `platform` global function must use parameters with the same names.
    - If the `common` global function includes default values, the corresponding positions in the `platform` global function must use named parameters with the same names. Default values are not supported in `platform` global functions.
    - Each `platform` global function must match a unique `common` global function. Multiple platform global functions cannot match the same `common` global function.

Example:

In a common file, some `common` global functions can be defined:

```cangjie
// common file
pkg cjmp

common func foo1()   // error: 'common' function return type must be specified
common func foo2(): Unit   // ok
common func foo3(a!: Int64): Unit   // ok
common func foo4(a!: Int64 = 1): Unit   // ok
common func foo5(a: Int64): Unit { println("hello word") }   // ok
```

In a platform file, `platform` global functions can be defined based on the `common` global functions:

```cangjie
// platform file
pkg cjmp

platform func foo2(a: Int64): Unit {}   // error: different arguments
platform func foo2(): Int64 {}   // error: different return type
public platform func foo2(): Int64 {}   // error: different modifiers
platform func foo2(): Unit {}   // ok

platform func foo3(a!: Int64): Unit { println("hello word") }   // ok

platform func foo4(a!: Int64 = 1): Unit {}   error: 'platform' function parameter can not have default value
platform func foo4(a!: Int64): Unit {}   // ok

// common func foo5 has a complete implementation, so no platform definition is needed.
```

#### class

Cangjie classes support cross-platform features. Users can use the `common` and `platform` modifiers for classes and their members.

```cangjie
// common file
package cmp

common class A {
    common var a: Int64 = 1
    common init()
    common func foo(): Unit
    common prop p: Int64
}

// platform file
package cmp

platform class A {
    platform var a: Int64 = 2
    platform init() {}
    platform func foo(): Unit {}
    platform prop p: Int64 {
        get() { a }
    }
}
```

If a `common class` exists, there must be a matching `platform class` with the following requirements:

- The visibility of the `common class` and `platform class` must be the same.
- The interface implementation of the `common class` and `platform class` must be the same.
- The inheritance of the `common class` and `platform class` must be the same.
- A `common open class` matches a `platform open class`.
- A `common abstract class` matches a `platform abstract class`.
- A `common sealed abstract class` matches a `platform sealed abstract class`.

##### Class Constructors

Constructors and primary constructors support cross-platform features. The following requirements must be met:

- A `common init` can have a concrete implementation or only a function signature, with the implementation provided by `platform init`.
- If a `common init` has a complete implementation, the `platform init` can be omitted. Otherwise, a matching `platform init` must exist.
- The visibility of `common init` and `platform init` must be the same.
- The `platform init` implementation overrides the `common init` implementation.
- The rules for primary constructors are the same as for constructors.
- `common`/`platform` classes support regular constructors, which can be defined in either `common` or `platform` classes.
- At least one explicitly defined constructor must exist in the `common` or `platform` class.
- Static initializers cannot be modified with `common`/`platform`.

```cangjie
// common file
package cmp

common class A {
    common A()
    common init(a: String) {}
    init(a: Bool) {}
}

// platform file
package cmp

platform class A {
    platform A() {}
    platform init(a: String) {
        println(a)
    }
    init(a: Int64) {}
}
```

##### Class Member Variables

`common` and `platform` class member variables must adhere to the following restrictions:

- `common`/`platform` member variables must specify their types.
- The type, mutability, and visibility of `common` and `platform` member variables must be the same.
- A `common` member variable can be initialized directly or in a constructor, or it can only declare the type and be initialized in the `platform` side.
- `common`/`platform` classes support regular member variables, which can be defined in either `common` or `platform` classes.
- Static member variables of classes do not currently support cross-platform features but will be supported in future versions.

```cangjie
// common file
package cmp

common class A {
    common let a: Int64 = 1
    common var b: Int64
    common var c: Int64

    init() {
        b = 1
        c = 1
    }
}

// platform file
package cmp

platform class A {
    platform let a: Int64 = 2
    platform let b: Int64 = 2

    init(input: Int64) { c = input }
}
```

##### Class Member Functions

`common` and `platform` class member functions must adhere to the following restrictions:

- A `common` member function can have a concrete implementation or only a function signature, with the implementation provided by a `platform` member function.
- If a `common` member function has a complete implementation, the `platform` member function can be omitted. Otherwise, a matching `platform` member function must exist.
- The parameters, return type, and modifiers (except `common`/`platform`) of `common` and `platform` member functions must be the same.
- `common`/`platform` classes support regular member functions, which can be defined in either `common` or `platform` classes.

```cangjie
// common file
package cmp

common class A {
    common func foo1(a: Int64): Unit
    common func foo2(): Unit {}
    common func foo3(): Unit {}
    func foo4() {}
}

// platform file
package cmp

platform class A {
    platform func foo1(a: Int64): Unit { println(a) }
    platform func foo3(): Unit { println("platform") }
    func foo5(): Int64 { 1 }

    init() {}
}
```

##### Class Properties

`common` and `platform` class properties must adhere to the following restrictions:

- A `common` property can have a concrete implementation or only a property signature, with the implementation provided by a `platform` property.
- If a `common` property has a complete implementation, the `platform` property can be omitted. Otherwise, a matching `platform` property must exist.
- The type, visibility, and assignability of `common` and `platform` properties must be the same.
- `common`/`platform` classes support regular properties, which can be defined in either `common` or `platform` classes.

```cangjie
// common file
package cmp

common class A {
    common prop a: Int64
    common prop b: Int64 {
        get() { 1 }
    }
    common prop c: Int64 {
        get() { 1 }
    }
    prop d: Int64 {
        get() { 1 }
    }
}

// platform file
package cmp

platform class A {
    platform prop a: Int64 {
        get() { 1 }
    }
    platform prop c: Int64 {
        get() { 2 }
    }
    prop e: Int64 {
        get() { 1 }
    }

    init() {}
}
```

##### Class Inheritance

Inheritance for `common`/`platform` classes does not currently support cross-platform features but will be supported in future versions.

#### struct

Cangjie structs support cross-platform features. Users can use the `common` and `platform` modifiers for structs and their members.

```cangjie
// common file
package cmp

common struct A {
    common var a: Int64 = 1
    common init()
    common func foo(): Unit
    common prop p: Int64
}

// platform file
package cmp

platform struct A {
    platform var a: Int64 = 2
    platform init() {}
    platform func foo(): Unit {}
    platform prop p: Int64 {
        get() { a }
    }
}
```

If a `common struct` exists, there must be a matching `platform struct` with the following requirements:

- The visibility of the `common struct` and `platform struct` must be the same.
- The interface implementation of the `common struct` and `platform struct` must be the same.
- The `common struct` and `platform struct` must both be annotated with `@C` or neither.

##### Struct Constructors

Constructors support cross-platform features. The following requirements must be met:

- A `common init` can have a concrete implementation or only a function signature, with the implementation provided by `platform init`.
- If a `common init` has a complete implementation, the `platform init` can be omitted. Otherwise, a matching `platform init` must exist.
- The visibility of `common init` and `platform init` must be the same.
- The `platform init` implementation overrides the `common init` implementation.
- `common`/`platform` structs support regular constructors, which can be defined in either `common` or `platform` structs.
- Static initializers cannot be modified with `common`/`platform`.

```cangjie
// common file
package cmp

common struct A {
    common init(a: String) {}
    init(a: Bool) {}
}

// platform file
package cmp

platform struct A {
    platform init(a: String) {
        println(a)
    }
    init(a: Int64) {}
}
```

##### Struct Member Variables

`common` and `platform` struct member variables must adhere to the following restrictions:

- `common`/`platform` member variables must specify their types.
- The type, mutability, and visibility of `common` and `platform` member variables must be the same.
- A `common` member variable can be initialized directly or in a constructor, or it can only declare the type and be initialized in the `platform` side.
- `common`/`platform` structs support regular member variables, which can be defined in either `common` or `platform` structs.
- Static member variables of structs do not currently support cross-platform features but will be supported in future versions.

```cangjie
// common file
package cmp

common struct A {
    common let a: Int64 = 1
    common var b: Int64
    common var c: Int64

    init() {
        b = 1
        c = 1
    }
}

// platform file
package cmp

platform struct A {
    platform let a: Int64 = 2
    platform let b: Int64 = 2

    init(input: Int64) { c = input }
}
```

##### Struct Member Functions

`common` and `platform` struct member functions must adhere to the following restrictions:

- A `common` member function can have a concrete implementation or only a function signature, with the implementation provided by a `platform` member function.
- If a `common` member function has a complete implementation, the `platform` member function can be omitted. Otherwise, a matching `platform` member function must exist.
- The parameters, return type, and modifiers (except `common`/`platform`) of `common` and `platform` member functions must be the same.
- `common`/`platform` structs support regular member functions, which can be defined in either `common` or `platform` structs.

```cangjie
// common file
package cmp

common struct A {
    common func foo1(a: Int64): Unit
    common func foo2(): Unit {}
    common func foo3(): Unit {}
    func foo4() {}
}

// platform file
package cmp

platform struct A {
    platform func foo1(a: Int64): Unit { println(a) }
    platform func foo3(): Unit { println("platform") }
    func foo5(): Int64 { 1 }

    init() {}
}
```

##### Struct Properties

`common` and `platform` struct properties must adhere to the following restrictions:

- A `common` property can have a concrete implementation or only a property signature, with the implementation provided by a `platform` property.
- If a `common` property has a complete implementation, the `platform` property can be omitted. Otherwise, a matching `platform` property must exist.
- The type, visibility, and assignability of `common` and `platform` properties must be the same.
- `common`/`platform` structs support regular properties, which can be defined in either `common` or `platform` structs.

```cangjie
// common file
package cmp

common struct A {
    common prop a: Int64
    common prop b: Int64 {
        get() { 1 }
    }
    common prop c: Int64 {
        get() { 1 }
    }
    prop d: Int64 {
        get() { 1 }
    }
}

// platform file
package cmp

platform struct A {
    platform prop a: Int64 {
        get() { 1 }
    }
    platform prop c: Int64 {
        get() { 2 }
    }
    prop e: Int64 {
        get() { 1 }
    }

    init() {}
}
```

#### enum

Cangjie enums support cross-platform features. Users can use the `common` and `platform` modifiers for enums and their members.

```cangjie
// common file
package cmp

common enum A {
    | ELEMENT
    common func foo(): Unit
    common prop p: Int64
}

// platform file
package cmp

platform enum A {
    | ELEMENT
    platform func foo(): Unit {}
    platform prop p: Int64 {
        get() { 1 }
    }
}
```

If a `common enum` exists, there must be a matching `platform enum` with the following requirements:

- The visibility of the `common enum` and `platform enum` must be the same.
- The interface implementation of the `common enum` and `platform enum` must be the same.
- The corresponding constructors in the `common enum` and `platform enum` must be of the same type.
- If the `common enum` is an exhaustive enum, the `platform enum` must also be exhaustive. If the `common enum` is non-exhaustive, the `platform enum` can be exhaustive.
    - For exhaustive enums, the `platform enum` must include all constructors from the `common enum` and cannot add new constructors.
    - For non-exhaustive enums, the `platform enum` must include all constructors from the `common enum` and can add new constructors.

```cangjie
// common file
package cmp

common enum A { ELEMENT1 | ELEMENT2 }
common enum B { ELEMENT1 | ELEMENT2 }
common enum C { ELEMENT1 | ELEMENT2 }
common enum D { ELEMENT1 | ELEMENT2 | ... }
common enum E { ELEMENT1 | ELEMENT2 | ... }

// platform file
package cmp

platform enum A { ELEMENT1 | ELEMENT2 }                   // ok
platform enum B { ELEMENT1 | ELEMENT2 | ELEMENT3 }        // error: exhaustive enum cannot add new constructor
platform enum C { ELEMENT1 | ELEMENT2 | ... }             // error: exhaustive 'common' enum cannot be matched with non-exhaustive 'platform' enum
platform enum D { ELEMENT1 | ELEMENT2 | ELEMENT3 }        // ok
platform enum E { ELEMENT1 | ELEMENT2 | ELEMENT3 | ... }  // ok
```

##### Enum Member Functions

Common enums and platform enums must adhere to the following restrictions for member functions:

- Common member functions may have concrete implementations or only retain function signatures, with implementations provided by platform member functions.
- If a common member function has a complete implementation, the corresponding platform member function can be omitted; otherwise, a matching platform member function must exist.
- The parameters, return types, and modifiers (excluding common/platform) of common and platform member functions must be identical.
- Both common and platform enums support regular member functions, which can be defined in either common or platform enums.

```cangjie
// common file
package cmp

common enum A {
    | ELEMENT

    common func foo1(a: Int64): Unit
    common func foo2(): Unit {}
    common func foo3(): Unit {}
    func foo4() {}
}

// platform file
package cmp

platform enum A {
    | ELEMENT

    platform func foo1(a: Int64): Unit { println(a) }
    platform func foo3(): Unit { println("platform") }
    func foo5(): Int64 { 1 }
}
```

##### Enum Properties

Common enums and platform enums must adhere to the following restrictions for properties:

- Common properties may have concrete implementations or only retain property signatures, with implementations provided by platform properties.
- If a common property has a complete implementation, the corresponding platform property can be omitted; otherwise, a matching platform property must exist.
- The types, visibility, and mutability of common and platform properties must be identical.
- Both common and platform enums support regular properties, which can be defined in either common or platform enums.

```cangjie
// common file
package cmp

common enum A {
    | ELEMENT

    common prop a: Int64
    common prop b: Int64 {
        get() { 1 }
    }
    common prop c: Int64 {
        get() { 1 }
    }
    prop d: Int64 {
        get() { 1 }
    }
}

// platform file
package cmp

platform enum A {
    | ELEMENT

    platform prop a: Int64 {
        get() { 1 }
    }
    platform prop c: Int64 {
        get() { 2 }
    }
    prop e: Int64 {
        get() { 1 }
    }
}
```

#### Interface

Cangjie interfaces support cross-platform features. Users can use `common` and `platform` modifiers for interfaces and their members.

```cangjie
// common file
package cmp

common interface A {
    common func foo(): Unit
    common prop p: Int64
}

// platform file
package cmp

platform interface A {
    platform func foo(): Unit {}
    platform prop p: Int64 {
        get() { 1 }
    }
}
```

If a common interface exists, a matching platform interface must also exist, subject to the following requirements:

- The visibility of common and platform interfaces must be identical.
- The interface implementation characteristics of common and platform interfaces must be identical.
- A common sealed interface must match a platform sealed interface.
- Direct subtypes of a sealed interface must be defined in the same common package.

##### Interface Member Functions

Common interfaces and platform interfaces must adhere to the following restrictions for member functions:

- Platform member functions can be omitted regardless of whether common member functions have complete implementations.
- The parameters, return types, and modifiers (excluding common/platform) of common and platform member functions must be identical.
- If a common member function includes a concrete implementation, the platform member function must also include a concrete implementation.
- Both common and platform interfaces support regular member functions, which can be defined in either common or platform interfaces.
- New regular functions added to platform interfaces must include complete implementations.

```cangjie
// common file
package cmp

common interface A {
    common func foo1(a: Int64): Unit
    common func foo2(): Unit
    common func foo3(): Unit {}
    func foo4(): Int64
}

// platform file
package cmp

platform interface A {
    platform func foo1(a: Int64): Unit { println(a) }
    platform func foo3(): Unit { println("platform") }
    func foo5(): Int64 { 1 }
}
```

##### Interface Properties

Common interfaces and platform interfaces must adhere to the following restrictions for properties:

- Platform properties can be omitted regardless of whether common properties have complete implementations.
- The types, visibility, and mutability of common and platform properties must be identical.
- If a common property includes a concrete implementation, the platform property must also include a concrete implementation.
- Both common and platform interfaces support regular properties, which can exist in either common or platform interfaces.
- New properties added to platform interfaces must include complete implementations.

```cangjie
// common file
package cmp

common interface A {
    common prop a: Int64
    common prop b: Int64
    common prop c: Int64 {
        get() { 1 }
    }
    prop d: Int64
}

// platform file
package cmp

platform interface A {
    platform prop a: Int64 {
        get() { 1 }
    }
    platform prop c: Int64 {
        get() { 2 }
    }
    prop e: Int64 {
        get() { 1 }
    }
}
```

### extend

Cangjie's `extend` supports cross-platform features, allowing users to use `common` and `platform` modifiers for `extend` and its members.

> **Note:**
>
> Generic `extend` does not currently support this feature.

```cangjie
// common file
package cmp

class A{}

common extend A {
    common func foo(): Unit
    common prop p: Int64
}

// platform file
package cmp

platform extend A {
    platform func foo(): Unit {}
    platform prop p: Int64 {
        get() { 1 }
    }
}
```

If there are one or more `common extend` declarations, there must be a unique matching `platform extend`, subject to the following requirements:

- When multiple `common extend` declarations without interfaces exist, there must be exactly one `platform extend`. It is prohibited to declare private functions with the same name across multiple `common extend` declarations.
- When a `common extend` with declared interfaces exists, the `common extend` and `platform extend` must have identical interface sets.

#### Member Functions of `extend`

Member functions in `common extend` and `platform extend` must adhere to the following constraints:

- A `common` member function may have a concrete implementation or only a function signature, with the implementation provided by the `platform` member function.
- If a `common` member function has a complete implementation, the corresponding `platform` member function may be omitted; otherwise, a matching `platform` member function must exist.
- Parameters, return types, and modifiers (excluding `common`/`platform`) must be identical between `common` and `platform` member functions.
- Both `common extend` and `platform extend` support regular member functions, which can be defined in either.

```cangjie
// common file
package cmp

class A{}

common extend A {
    common func foo1(a: Int64): Unit
    common func foo2(): Unit { println("common") }
    func foo3(): Unit{}
}

// platform file
package cmp

platform extend A {
    platform func foo1(a: Int64): Unit { println(a) }
    platform func foo2(): Unit { println("platform") }
    func foo4(): Int64 { 1 }
}
```

##### Properties of `extend`

Properties in `common extend` and `platform extend` must adhere to the following constraints:

- A `common` property may have a concrete implementation or only a property signature, with the implementation provided by the `platform` property.
- If a `common` property has a complete implementation, the corresponding `platform` property may be omitted; otherwise, a matching `platform` property must exist.
- Property types, visibility, and mutability must be identical between `common` and `platform` properties.
- Both `common extend` and `platform extend` support regular properties, which can be defined in either.

```cangjie
// common file
package cmp

class A{}

common extend A {
    common prop a: Int64
    common prop b: Int64 {
        get() { 1 }
    }
    prop c: Int64{
        get() { 1 }
    }
}

// platform file
package cmp

platform extend A {
    platform prop a: Int64 {
        get() { 1 }
    }
    platform prop b: Int64 {
        get() { 2 }
    }
    prop d: Int64 {
        get() { 1 }
    }
}
```

### Cross-Platform Compilation

Users can compile cross-platform packages using `cjc`.

> **Note:**
>
> Import statements in the platform-specific code of a cross-platform package must be a superset of those in the common code; otherwise, compilation errors may occur.

#### Compilation with `cjc`

Given the following directory structure:

```text
cjmp_project(package cjmp)
├── common
│      └── common.cj
├── platform
│      └── platform.cj
└── main.cj
```

1. First, compile the file containing the common code.

    ```shell
    cjc --experimental common/common.cj --output-type=chir --output-dir ./common
    ```

2. Next, compile the file containing the platform-specific code.

    ```shell
    cjc --experimental platform/platform.cj common/common.chir --common-part-cjo=./common/cjmp.cjo --output-type=dylib --output-dir ./platform
    ```

3. When invoking code for different platforms, specify the platform by referencing the `.so` file generated from compiling the platform-specific file.

    ```shell
    cjc main.cj -o main --import-path=./platform -L./platform -lcjmp
    ```

## Cross-Platform Development Example

### Using the `Platform()` Interface to Retrieve the Platform Name

Common definition file.

```cangjie
// common.cj
package example.cmp
// Retrieve platform information
public common func Platform(): String
```

Linux platform file.

```cangjie
// linux.cj
package example.cmp
public platform func Platform(): String {
    "Linux"
}
```

Windows platform file.

```cangjie
// windows.cj
package example.cmp
public platform func Platform(): String {
    "Win64"
}
```

macOS platform file.

```cangjie
// macos.cj
package example.cmp
public platform func Platform(): String {
    "Mac"
}
```

Application-side code.

```cangjie
// app.cj
import example.cmp.Platform
​
main() {
    println("${Platform()}")
}
```
