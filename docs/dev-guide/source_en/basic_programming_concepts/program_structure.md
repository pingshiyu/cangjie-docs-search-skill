# Program Structure

Typically, developers write Cangjie programs in text files with the `.cj` extension, which are also referred to as source code and source files. In the final stage of program development, this source code will be compiled into binary files of a specific format.

At the top-level scope of a Cangjie program, a series of variables, functions, and custom types (such as `struct`, `class`, `enum`, and `interface`) can be defined. Among these, variables and functions are called **global variables** and **global functions**, respectively. To compile a Cangjie program into an executable file, a `main` function must be defined at the top-level scope as the **program entry point**. This function can either take a parameter of type `Array<String>` or no parameters at all, and its return type can be an integer type or the `Unit` type.

> **Note:**
>
> When defining the `main` function, the `func` modifier is not required. Additionally, if command-line arguments are needed during program startup, a parameter of type `Array<String>` can be declared and used.

For example, in the following program, the top-level scope defines the global variable `a`, the global function `b`, the custom types `C`, `D`, and `E`, as well as the `main` function serving as the program entry point.

<!-- compile -->

```cangjie
// example.cj
let a = 2023
func b() {}
struct C {}
class D {}
enum E { F | G }

main() {
    println(a)
}
```

In non-top-level scopes, the aforementioned custom types cannot be defined, but variables and functions can be defined, referred to as **local variables** and **local functions**. Specifically, variables and functions defined within custom types are called **member variables** and **member functions**.

> **Note:**
>
> `enum` and `interface` only support defining member functions and do not allow member variables.

For example, in the following program, the top-level scope defines the global function `a` and the custom type `A`. Within the function `a`, the local variable `b` and local function `c` are defined, while within the custom type `A`, the member variable `b` and member function `c` are defined.

<!-- verify -->

```cangjie
// example.cj
func a() {
    let b = 2023
    func c() {
        println(b)
    }
    c()
}

class A {
    let b = 2024
    public func c() {
        println(b)
    }
}

main() {
    a()
    A().c()
}
```

Running the above program will output:

```text
2023
2024
```

## Variables

In the Cangjie programming language, a variable consists of a corresponding variable name, data (value), and several attributes. Developers access the data associated with a variable through its name, but such access operations must comply with the constraints of the relevant attributes (such as data type, mutability, and visibility).

The specific form of variable definition is:

```text
modifier variable_name: variable_type = initial_value
```

Here, **modifiers** are used to set various attributes of the variable and can be one or more. Commonly used modifiers include:

- Mutability modifiers: `let` and `var`, corresponding to immutable and mutable attributes, respectively. Mutability determines whether a variable's value can be changed after initialization, thus dividing Cangjie variables into immutable and mutable types.
- `const` modifier: `const` is a special variable modifier used to declare constants. It requires initialization at declaration and prohibits any changes to its value afterward. This is similar to the `let` modifier in terms of immutability but imposes stricter usage restrictions.
- Visibility modifiers: `private` and `public`, among others, which affect the reference scope of global variables and member variables. For details, refer to the relevant sections in subsequent chapters.
- Static modifiers: `static`, which affect the storage and referencing of member variables. For details, refer to the relevant sections in subsequent chapters.

All variables support the assignment operator (`=`), regardless of type. Variables modified by `let` can only be assigned once (i.e., initialized), while those modified by `var` can be assigned multiple times.

When defining a Cangjie variable, a mutability modifier is mandatory. Additional modifiers can be added as needed.

- **Variable name** must be a valid Cangjie identifier.
- **Variable type** specifies the type of data held by the variable. When the initial value has a clear type, the variable type annotation can be omitted, allowing the compiler to infer the type automatically.
- **Initial value** is a Cangjie expression used to initialize the variable. If the variable type is annotated, the initial value type must match the variable type. Global variables or static member variables must be initialized at definition. Local variables or instance member variables can omit the initial value but must have a type annotation. They must be initialized before being referenced; otherwise, a compilation error will occur.

For example, the following program defines three `Int64` variables (the immutable variable `a`, the mutable variable `b`, and the `const` variable `c`). It then modifies the value of `b`, assigns `b`'s value to `a`, and prints the values of `a`, `b`, and `c` using the `println` function.

<!-- verify -->

```cangjie
main() {
    let a: Int64
    var b: Int64 = 14
    const c: Int64 = 13
    b = 12
    a = b // A variable modified by let can only be assigned once, that is, initialized
    println("${a}, ${b}, ${c}")
}
```

Compiling and running this program will output:

```text
12, 12, 13
```

Attempting to modify an immutable variable will result in a compilation error, for example:

<!-- compile.error -->

```cangjie
main() {
    let pi: Float64 = 3.14159
    pi = 2.71828 // Error, cannot assign to immutable value
}
```

When the initial value has a clear type, the variable type annotation can be omitted, for example:

<!-- verify -->

```cangjie
main() {
    let a: Int64 = 2023
    let b = a
    println("a - b = ${a - b}")
}
```

Here, the type of variable `b` can be automatically inferred as `Int64` from its initial value `a`, so this program can be compiled and run normally, outputting:

```text
a - b = 0
```

When defining local variables, initialization can be omitted, but the variable must be assigned a value before being referenced, for example:

<!-- verify -->

```cangjie
main() {
    let text: String
    text = "仓颉造字"
    println(text)
}
```

Compiling and running this program will output:

```text
仓颉造字
```

Global variables and static member variables must be initialized at definition; otherwise, a compilation error will occur, for example:

<!-- compile.error -->

```cangjie
let global: Int64 // Error, variable in top-level scope must be initialized

main(): Unit{

}
```

<!-- compile.error -->

```cangjie
class Player {
    static let score: Int32 // Error, static variable 'score' needs to be initialized when declaring
}
```

Note that when the compiler cannot determine whether certain scenarios will definitely initialize a variable or whether an immutable variable is being reinitialized, it will conservatively report a compilation error, as shown in the following example:

<!-- compile.error -->

```cangjie
func calc(a: Int32){
    println(a)
    return a * a
}
main() {
    let a: String
    if(calc(32) == 0){
      a = "1"
    }
    a = "2" // Error, cannot assign to immutable value
}
```

Additionally, for [try-catch](../error_handle/handle.md#普通-try-表达式) scenarios, the compiler assumes that the `try` block is always fully executed and always throws an exception, leading to related errors, as shown in the following example:

<!-- compile.error -->

```cangjie
main() {
    let a: String
    try {
        a = "1"
    } catch (_) {
        a = "2" // Error, cannot assign to immutable value
    }
}
```

## `const` Variables

`const` variables are a special type of variable modified by the keyword `const`. They are evaluated at compile time and cannot be changed during runtime. For example, the following defines the gravitational constant `G`:

<!-- verify -const -->

```cangjie
const G = 6.674e-11
```

`const` variables can omit type annotations but cannot omit initialization expressions. They can be global variables, local variables, or static member variables. However, `const` variables cannot be defined in extensions. They can access all instance members of their corresponding types and call all non-`mut` instance member functions.

The following example defines a `struct` to record a planet's mass and radius, along with a `const` member function `gravity` to calculate the gravitational force exerted by the planet on an object of mass `m` at distance `r`:

<!-- verify -const -->

```cangjie
struct Planet {
    const Planet(let mass: Float64, let radius: Float64) {}

    const func gravity(m: Float64, r: Float64) {
        G * mass * m / r**2
    }
}

main() {
    const myMass = 71.0
    const earth = Planet(5.972e24, 6.378e6)
    println(earth.gravity(myMass, earth.radius))
}
```

Compiling and executing this will output the gravitational force exerted by Earth on a 71 kg adult standing on its surface:

<!-- verify -const -->

```text
695.657257
```

After initialization, all members of a `const` variable's type instance are `const` (deep `const`, including members of members) and thus cannot be used as lvalues.

<!-- compile.error -->

```cangjie
main() {
    const myMass = 71.0
    myMass = 70.0 // Error, cannot assign to immutable value
}
```

### Value-Type and Reference-Type Variables

From the compiler's implementation perspective, any variable is always associated with a value (typically via a memory address/register). However, for some variables, the value itself is directly used, which are called **value-type variables**. For others, the value serves as an index to access the data it points to, which are called **reference-type variables**. Value-type variables are usually allocated on the thread stack, with each variable having its own data copy. Reference-type variables are usually allocated on the process heap, with multiple variables potentially referencing the same data object. Operations on one variable may affect others.

From the language perspective, value-type variables exclusively bind to their data/storage space, while reference-type variables share their data/storage space with other reference-type variables.

Based on these principles, there are behavioral differences between value-type and reference-type variables, with the following points worth noting:

1. Assigning to a value-type variable typically involves a copy operation, and the originally bound data/storage space is overwritten. Assigning to a reference-type variable only changes the reference relationship, leaving the originally bound data/storage space unaffected.
2. Variables defined with `let` cannot be reassigned after initialization. For reference types, this only restricts the reference relationship from changing; the referenced data can still be modified.

In the Cangjie programming language, `class` and `Array` types are reference types, while other basic data types and `struct` types are value types.

For example, the following program demonstrates the behavioral differences between `struct` and `class` type variables:

<!-- verify -->

```cangjie
struct Copy {
    var data = 2012
}

class Share {
    var data = 2012
}

main() {
    let c1 = Copy()
    var c2 = c1
    c2.data = 2023
    println("${c1.data}, ${c2.data}")

    let s1 = Share()
    let s2 = s1
    s2.data = 2023
    println("${s1.data}, ${s2.data}")
}
```

Running the above program will output:

```text
2012, 2023
2023, 2023
```

From this, we can observe that for value-type `Copy` variables, assignment always obtains a copy of the `Copy` instance, such as `c2 = c1`. Subsequent modifications to `c2` members do not affect `c1`. For reference-type `Share` variables, assignment establishes a reference relationship between the variable and the instance, such as `s2 = s1`. Subsequent modifications to `s2` members will affect `s1`.

If we change `var c2 = c1` to `let c2 = c1` in the above program, the compilation will report an error, for example:

<!-- compile.error -->

```cangjie
struct Copy {
    var data = 2012
}

main() {
    let c1 = Copy()
    let c2 = c1
    c2.data = 2023 // Error, cannot assign to immutable value
}
```

## Scope

Earlier, we briefly introduced how to name elements in Cangjie programs. In practice, besides variables, names can also be assigned to functions and custom types, and these names are used to access the corresponding program elements.

However, in practical applications, some special cases need to be considered:

- When the program scale is large, those short names are prone to duplication, leading to naming conflicts.
- Considering runtime scenarios, in some code segments, certain program elements are invalid, and referencing them will cause runtime errors. For example, some variables become invalid after their scope is exited.
- In certain logical constructs, to express containment relationships between elements, sub-elements should not be accessed directly by name but through their parent element names indirectly.

To address these issues, modern programming languages introduce the concept and design of "scope," limiting the binding relationship between names and program elements to a specific range. Scopes can be parallel, unrelated, nested, or contain each other. A scope clearly defines which program elements can be accessed by which names, with the following specific rules:

1. The binding relationship between program elements and names defined in the current scope is valid within the current scope and its inner scopes, allowing direct access to the corresponding program elements via these names.
2. The binding relationship between program elements and names defined in an inner scope is invalid in outer scopes.
3. Inner scopes can redefine binding relationships using names from outer scopes. According to rule 1, the naming in the inner scope effectively shadows the same-name definition in the outer scope. In this case, the inner scope is said to have a higher level than the outer scope.

In the Cangjie programming language, a pair of curly braces `{}` enclosing a segment of Cangjie code creates a new scope. Within this scope, further curly braces `{}` can enclose more Cangjie code, resulting in nested scopes. These scopes all adhere to the above rules. Specifically, in a Cangjie source file, code not enclosed by any curly braces `{}` belongs to the "top-level scope," the "outermost" scope in the current file, which, according to the above rules, has the lowest scope level.

> **Note:**
>
> Cangjie does not allow standalone curly braces `{}`. Curly braces must depend on other syntactic structures such as `if`, `match`, function bodies, class bodies, or struct bodies.

For example, in the following Cangjie source file named `test.cj`, the name `element` is defined in the top-level scope, bound to the string "Cangjie." Within the `main` and `if` blocks, the name `element` is also defined, corresponding to the integer 9 and the integer 2023, respectively. According to the scope rules, at line 4, `element` has the value "Cangjie"; at line 8, `element` has the value 2023; and at line 10, `element` has the value 9.

<!-- verify -->

```cangjie
// test.cj
let element = "Cangjie"
main() {
    println(element)
    let element = 9
    if (element > 0) {
        let element = 2023
        println(element)
    }
    println(element)
}
```

Running the above program will output:

```text
Cangjie
2023
9
```