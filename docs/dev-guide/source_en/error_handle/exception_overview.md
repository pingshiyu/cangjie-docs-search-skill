# Defining Exceptions

Exceptions are a special category of errors that can be caught and handled by programmers, representing a series of abnormal behaviors that occur during program execution. Examples include array index out of bounds, division by zero, arithmetic overflow, illegal input, etc. To ensure system correctness and robustness, many software systems contain extensive code for error detection and handling.

Exceptions are not part of a program's normal functionality. Once an exception occurs, the program must handle it immediately by transferring control from the normal execution flow to the exception handling section. The Cangjie programming language provides an exception handling mechanism to address various exceptional conditions that may arise during runtime.

In Cangjie, exception classes include `Error` and `Exception`:

- The `Error` class describes internal runtime system errors and resource exhaustion errors in Cangjie. Applications should not throw this type of error. If internal errors occur, they should only be reported to users, and the program should attempt to terminate safely.
- The `Exception` class describes runtime logical errors or IO errors that cause exceptions, such as array index out of bounds or attempting to open a non-existent file. These exceptions need to be caught and handled within the program.

Developers cannot define custom exceptions by inheriting from Cangjie's built-in `Error` class or its subclasses. However, they can inherit from the built-in `Exception` class or its subclasses to create custom exceptions, for example:

<!-- compile -->

```cangjie
open class FatherException <: Exception {
    public init() {
        super("This is FatherException.")
    }
    public init(message: String) {
        super(message)
    }
    public open override func getClassName(): String {
        "FatherException"
    }
}

class ChildException <: FatherException {
    public init() {
        super("This is ChildException.")
    }
    public open override func getClassName(): String {
        "ChildException"
    }
}
```

The following table shows the main functions of `Exception` and their descriptions:

| Function Type | Function and Description                                                                     |
| :------------ |:-------------------------------------------------------------------------------------------|
| Constructor   | `init()` Default constructor.                                                              |
| Constructor   | `init(causedBy: Exception)` Constructor that allows setting a cause exception.               |
| Constructor   | `init(message: String)` Constructor that allows setting an exception message.               |
| Constructor   | `init(message: String, causedBy: Exception)` Constructor that allows setting an exception message and a cause exception.               |
| Property      | `mut prop causedBy: ?Exception` Allows setting a cause exception and returns the cause exception. |
| Property      | `open prop message: String` Returns detailed information about the exception. The message is initialized in the exception class constructor and defaults to an empty string. |
| Method        | `open func toString(): String` Returns the exception type name and detailed information, where the detailed information defaults to using the `message` property. |
| Method        | `func getClassName(): String` Returns the user-defined class name. Subclasses need to override this method to return their own names. |
| Method        | `func printStackTrace(): Unit` Prints stack trace information to the standard error stream. |

The following table shows the main functions of `Error` and their descriptions:

| Function Type | Function and Description                                                   |
| :------------ | :------------------------------------------------------------------------- |
| Property      | `open prop message: String` Returns detailed information about the error. The message is internally initialized when the error occurs and defaults to an empty string. |
| Method        | `open func toString(): String` Returns the error type name and detailed information, where the detailed information defaults to using the `message` property. |
| Method        | `func printStackTrace(): Unit` Prints stack trace information to the standard error stream. |