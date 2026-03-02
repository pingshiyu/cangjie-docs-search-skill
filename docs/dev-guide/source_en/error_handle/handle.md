# throw and Exception Handling

The previous section discussed how to define custom exceptions. Now let's learn how to throw and handle exceptions.

- Since exceptions are of `class` type, you only need to create them in the same way as class objects. For example, the expression `FatherException()` creates an exception of type `FatherException`.
- The Cangjie language supports creating exception chains (only for `Exception`, not including `Error`), such as the expression `let fatherException = FatherException("this is message", causeException)`, where `causeException` is another exception and serves as the cause that triggered `fatherException`. When printing the exception stack trace, it will recursively print the cause.
- The Cangjie language provides the `throw` keyword for throwing exceptions. When using `throw`, the expression following it must be a subtype of `Exception` (note that `Error`, though also an exception type, cannot be manually thrown via `throw`). For example, `throw ArithmeticException("I am an Exception!")` will throw an arithmetic exception when executed.
- Exceptions thrown via the `throw` keyword must be caught and handled. If an exception is not caught, the system will invoke the default exception handler.

  > **Note:**
  >
  > Developers can call the following static functions of the Thread class to register a custom exception handler for uncaught Error and Exception:
  >
  > - `public static func handleUncaughtErrorBy(erHandler: (Error) -> Unit): Unit`
  > - `public static func handleUncaughtExceptionBy(exHandler: (Thread, Exception) -> Unit): Unit`

Exception handling is performed using `try` expressions, which come in two forms:

1. Regular try expressions without automatic resource management.
2. Try-with-resources expressions that perform automatic resource management.

## Regular try Expressions

A regular try expression consists of three parts: a try block, catch blocks, and a finally block.

- **Try block**: Begins with the `try` keyword followed by a block of expressions and declarations (enclosed in curly braces, defining a new local scope that can contain any expressions or declarations, hereafter referred to as "block"). The block following `try` may throw exceptions, which can be caught and handled by subsequent catch blocks (if no catch block exists or the exception is uncaught, the exception continues to propagate after executing the finally block).

- **Catch blocks**: A regular try expression may contain zero or more catch blocks (when no catch block exists, a finally block must be present). Each catch block starts with the `catch` keyword, followed by a `catchPattern` and a block. The `catchPattern` matches the exception to be caught via pattern matching. Once matched, the exception is handled by the subsequent block, and any remaining catch blocks are ignored. If a catch block's exception type can be caught by a preceding catch block, a "catch block unreachable" warning will be issued for that catch block.

- **Finally block**: Begins with the `finally` keyword followed by a block. The finally block is primarily used for cleanup tasks, such as releasing resources, and should avoid throwing further exceptions. The finally block executes regardless of whether an exception occurs (i.e., whether the try block throws an exception). If the exception remains unhandled, it continues to propagate after the finally block executes. A try expression may omit the finally block only if it includes catch blocks; otherwise, the finally block is mandatory.

The scopes of the block following `try` and each `catch` block are independent.

Here is a simple example with only a try block and a catch block:

<!-- verify -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("I am an Exception!")
    } catch (e: NegativeArraySizeException) {
        println(e)
        println("NegativeArraySizeException is caught!")
    }
    println("This will also be printed!")
}
```

Execution result:

```text
NegativeArraySizeException: I am an Exception!
NegativeArraySizeException is caught!
This will also be printed!
```

Variables introduced in `catchPattern` have the same scope level as variables in the block following `catch`. Redefining the same variable name in the catch block will trigger a redefinition error. For example:

<!-- compile.error -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("I am an Exception!")
    } catch (e: NegativeArraySizeException) {
        println(e)
        let e = 0 // Error, redefinition
        println(e)
        println("NegativeArraySizeException is caught!")
    }
    println("This will also be printed!")
}
```

Below is a simple example of a try expression with a finally block:

<!-- verify -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("NegativeArraySizeException")
    } catch (e: NegativeArraySizeException) {
        println("Exception info: ${e}.")
    } finally {
        println("The finally block is executed.")
    }
}
```

Execution result:

```text
Exception info: NegativeArraySizeException: NegativeArraySizeException.
The finally block is executed.
```

Try expressions can appear anywhere expressions are allowed. The type of a try expression is determined similarly to multi-branch constructs like `if` and `match` expressions: it is the least common supertype of all branch types (excluding the finally branch). For example, in the following code, the try expression and variable `x` both have type `D`, the least common supertype of `E` and `D`. The `C()` in the finally branch does not participate in the least common supertype calculation (if it did, the least common supertype would become `C`).

Additionally, when the value of a `try` expression is unused, its type is `Unit`, and the branches are not required to have a least common supertype.

<!-- compile -->

```cangjie
open class C { }
open class D <: C { }
class E <: D { }
main () {
    let x = try {
        E()
    } catch (e: Exception) {
        D()
    } finally {
        C()
    }
    0
}
```

## Try-with-resources Expressions

Try-with-resources expressions are primarily used for automatic release of non-memory resources. Unlike regular try expressions, catch and finally blocks are optional in try-with-resources expressions. Additionally, between the `try` keyword and the block, one or more `ResourceSpecification` clauses can be inserted to acquire resources (the `ResourceSpecification` does not affect the type of the try expression). In the context of the language, resources correspond to objects, so `ResourceSpecification` essentially instantiates a series of objects (multiple instantiations are separated by ","). An example of using try-with-resources is shown below:

<!-- compile -->

```cangjie
class Worker <: Resource {
    var hasTools: Bool = false
    let name: String

    public init(name: String) {
        this.name = name
    }
    public func getTools() {
        println("${name} picks up tools from the warehouse.")
        hasTools = true
    }

    public func work() {
        if (hasTools) {
            println("${name} does some work with tools.")
        } else {
            println("${name} doesn't have tools, does nothing.")
        }
    }

    public func isClosed(): Bool {
        if (hasTools) {
            println("${name} hasn't returned the tool.")
            false
        } else {
            println("${name} has no tools")
            true
        }
    }
    public func close(): Unit {
        println("${name} returns the tools to the warehouse.")
        hasTools = false
    }
}

main() {
    try (r = Worker("Tom")) {
        r.getTools()
        r.work()
    }
    try (r = Worker("Bob")) {
        r.work()
    }
    try (r = Worker("Jack")) {
        r.getTools()
        throw Exception("Jack left, because of an emergency.")
    }
}
```

Program output:

```text
Tom picks up tools from the warehouse.
Tom does some work with tools.
Tom hasn't returned the tool.
Tom returns the tools to the warehouse.
Bob doesn't have tools, does nothing.
Bob has no tools
Jack picks up tools from the warehouse.
Jack hasn't returned the tool.
Jack returns the tools to the warehouse.
An exception has occurred:
Exception: Jack left, because of an emergency.
         at test.main()(xxx/xx.cj:xx)
```

Variables introduced between the `try` keyword and `{}` have the same scope level as variables introduced within `{}`. Redefining the same name within `{}` will trigger a redefinition error.

<!-- compile.error -->

```cangjie
class R <: Resource {
    public func isClosed(): Bool {
        true
    }
    public func close(): Unit {
        print("R is closed")
    }
}

main() {
    try (r = R()) {
        println("Get the resource")
        let r = 0 // Error, redefinition
        println(r)
    }
}
```

The types in `ResourceSpecification` of a try-with-resources expression must implement the `Resource` interface:

<!-- run -->

```cangjie
interface Resource {
    func isClosed(): Bool  // Determines whether the `close` function should be called to release resources when exiting the try-with-resources scope.
    func close(): Unit  // Releases resources when `isClosed` returns false.
}
```

It is worth noting that try-with-resources expressions generally do not need to include catch or finally blocks, nor is it recommended for developers to manually release resources (redundant logic). However, if you need to explicitly catch and handle exceptions that may occur during the try block or resource acquisition/release, you can still include catch and finally blocks in try-with-resources expressions:

<!-- verify -->

```cangjie
class R <: Resource {
    public func isClosed(): Bool {
        true
    }
    public func close(): Unit {
        print("R is closed")
    }
}

main() {
    try (r = R()) {
        println("Get the resource")
    } catch (e: Exception) {
        println("Exception happened when executing the try-with-resources expression")
    } finally {
        println("End of the try-with-resources expression")
    }
}
```

Program output:

```text
Get the resource
End of the try-with-resources expression
```

The type of a try-with-resources expression is `Unit`.

## Advanced CatchPattern Introduction

Most of the time, you only want to catch exceptions of a specific type and its subtypes. In such cases, use the **type pattern** of `CatchPattern`. However, sometimes you may need to handle all exceptions uniformly (e.g., when no exception should occur, and any exception triggers a uniform error message). In such cases, use the **wildcard pattern** of `CatchPattern`.

The type pattern has two syntactic forms:

1. `Identifier: ExceptionClass`: This form catches exceptions of type `ExceptionClass` and its subclasses. The caught exception instance is cast to `ExceptionClass` and bound to the variable defined by `Identifier`, which can then be used to access the exception instance in the catch block.
2. `Identifier: ExceptionClass_1 | ExceptionClass_2 | ... | ExceptionClass_n`: This form concatenates multiple exception classes using the `|` operator, which represents an "or" relationship. It catches exceptions of type `ExceptionClass_1` or its subclasses, or `ExceptionClass_2` or its subclasses, and so on (assuming n > 1). When the exception type matches any of these types or their subtypes, it is caught. However, since the exact type cannot be determined statically, the caught exception is cast to the least common superclass of all types connected by `|` and bound to the variable defined by `Identifier`. Thus, in this mode, the catch block can only access members of the least common superclass via the `Identifier` variable. Alternatively, a wildcard can replace the `Identifier` in the type pattern, with the only difference being that the wildcard does not perform binding.

Example:

<!-- verify -->

```cangjie
main(): Int64 {
    try {
        throw IllegalArgumentException("This is an Exception!")
    } catch (e: OverflowException) {
        println(e.message)
        println("OverflowException is caught!")
    } catch (e: IllegalArgumentException | NegativeArraySizeException) {
        println(e.message)
        println("IllegalArgumentException or NegativeArraySizeException is caught!")
    } finally {
        println("finally is executed!")
    }
    return 0
}
```

Execution result:

```text
This is an Exception!
IllegalArgumentException or NegativeArraySizeException is caught!
finally is executed!
```

Example demonstrating "the caught exception type is the least common superclass of all types connected by `|`":

<!-- verify -->

```cangjie
open class Father <: Exception {
    var father: Int32 = 0
}
class ChildOne <: Father {
    var childOne: Int32 = 1
}

class ChildTwo <: Father {
    var childTwo: Int32 = 2
}

main() {
    try {
        throw ChildOne()
    } catch (e: ChildTwo | ChildOne) {
        println("${e is Father}")
    }
}
```

Execution result:

```text
true
```

The syntax for **wildcard pattern** is `_`, which can catch any type of exception thrown within the same-level try block. It is equivalent to the type pattern `e: Exception`, meaning it catches exceptions defined by subclasses of Exception. Example as follows:

<!-- compile -->

```cangjie
// Catch with wildcardPattern.
try {
    throw OverflowException()
} catch (_) {
    println("catch an exception!")
}
```
