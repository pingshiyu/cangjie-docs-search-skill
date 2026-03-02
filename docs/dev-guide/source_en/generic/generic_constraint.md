# Generic Constraints

The purpose of generic constraints is to specify the operations and capabilities that generic type parameters must possess when declaring functions, classes, interfaces, structs, or enums. Only by declaring these constraints can corresponding member functions be called. In many scenarios, generic type parameters need to be constrained. Take the `id` function as an example:

<!-- compile -->

```cangjie
func id<T>(a: T) {
    return a
}
```

The only thing the developer can do is return the function parameter `a`, but cannot perform operations like `a + 1` or `println("${a}")` because it could be any type, such as `(Bool) -> Bool`, which cannot be added to an integer. Similarly, since it's a function type, it cannot be printed to the command line via the `println` function. However, if constraints are applied to this generic type parameter, more operations become possible.

Constraints are broadly divided into interface constraints and class type constraints. Before the declaration body of a function or type, the `where` keyword can be used to declare generic constraints. For declared generic type parameters `T1, T2`, constraints can be specified using syntax like `where T1 <: Interface, T2 <: Class`. If multiple constraints apply to the same type parameter, they can be connected with `&`, e.g., `where T1 <: Interface1 & Interface2`.

In Cangjie, the `println` function can accept parameters of type string. If you need to print a generic type variable as a string on the command line, you can constrain this generic type parameter with the `ToString` interface defined in `core`, which is clearly an interface constraint:

```cangjie
package std.core // `ToString` is defined in core.

public interface ToString {
    func toString(): String
}
```

This allows you to define a function named `genericPrint` using this constraint:

<!-- verify -->

```cangjie
func genericPrint<T>(a: T) where T <: ToString {
    println(a)
}

main() {
    genericPrint<Int64>(10)
}
```

The result is:

```text
10
```

If the type argument for the `genericPrint` function does not implement the `ToString` interface, the compiler will report an error. For example, when passing a function as a parameter:

<!-- compile.error -->

```cangjie
func genericPrint<T>(a: T) where T <: ToString {
    println(a)
}

main() {
    genericPrint<(Int64) -> Int64>({ i => 0 })
}
```

If you compile the above file, the compiler will throw an error indicating that the generic type argument does not satisfy the constraint, because the type argument `(Int64) -> Int64` does not satisfy `(Int64) -> Int64 <: ToString`.

In addition to interface-based constraints, class types can also be used to constrain generic type parameters. For example, when declaring a zoo type `Zoo<T>`, you might want the type parameter `T` to be constrained to subtypes of the `Animal` class, where `Animal` declares a `run` member function. Here, two subtypes `Dog` and `Fox` both implement the `run` member function, allowing instances stored in the `animals` array list within `Zoo<T>` to call the `run` member function:

<!-- verify -->

```cangjie
import std.collection.ArrayList

abstract class Animal {
    public func run(): String
}

class Dog <: Animal {
    public func run(): String {
        return "dog run"
    }
}

class Fox <: Animal {
    public func run(): String {
        return "fox run"
    }
}

class Zoo<T> where T <: Animal {
    var animals: ArrayList<Animal> = ArrayList<Animal>()
    public func addAnimal(a: T) {
        animals.add(a)
    }

    public func allAnimalRuns() {
        for(a in animals) {
            println(a.run())
        }
    }
}

main() {
    var zoo: Zoo<Animal> = Zoo<Animal>()
    zoo.addAnimal(Dog())
    zoo.addAnimal(Fox())
    zoo.allAnimalRuns()
}
```

The program output is:

```text
dog run
fox run
```

> **Note:**
>
> Constraints for generic type parameters can only be concrete class types or interfaces. If a type parameter has multiple class-type upper bounds, they must be in the same inheritance chain.