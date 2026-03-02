# Extension Overview

Extensions can add new functionality to types (excluding functions, tuples, and interfaces) that are visible within the current `package`.

Extensions are used when you need to add additional functionality without breaking the encapsulation of the extended type.

The functionalities that can be added include:

- Adding member functions
- Adding operator overload functions
- Adding member properties
- Implementing interfaces

For specific examples of how to add the above functionalities, refer to the following example. For detailed syntax usage, please see subsequent sections:

<!-- compile -->

```cangjie
interface Foo {
    func printValue(a: Int64): Unit
}

class Boo {
    var boo: Int64 = 2
}

extend Boo {
    public prop x: Int64 { // Adding a member property
        get() {
            123
        }
    }

    func newMember(): Unit {
        println("This is a member function of a new extension.") // Adding a member function
    }

    public operator func -() {
        println("Overload the operator addition function.") // Adding an operator overload function
        -x
    }
}

// Interface extension, implementing an interface
extend<T> Array<T> <: Foo {
    public func printValue(a: Int64) {
        println("The is ${a}.")
    }
}
```

Although extensions can add extra functionality, they cannot alter the encapsulation of the extended type. Therefore, extensions do not support the following functionalities:

1. Extensions cannot add member variables.
2. Functions and properties in extensions must have implementations.
3. Functions and properties in extensions cannot be modified with `open`, `override`, or `redef`.
4. Extensions cannot access members modified with `private` in the extended type.

Based on whether an extension implements a new interface, extensions can be divided into two usage types: **direct extensions** and **interface extensions**. A direct extension does not include additional interfaces, while an interface extension includes interfaces. Interface extensions can be used to add new functionality to existing types and implement interfaces, enhancing abstract flexibility.