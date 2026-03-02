# Generics Overview

In the Cangjie programming language, generics refer to parameterized types, where a parameterized type is one that is unknown at declaration time and must be specified upon usage. Both type declarations and function declarations can be generic. The most common examples are container types such as `Array<T>` and `Set<T>`.

In Cangjie, declarations of `function`, `class`, `interface`, `struct`, and `enum` can all declare type parameters, meaning they can all be generic.

For ease of discussion, the following commonly used terms are defined:

- **Type Parameter**: A type or function declaration may have one or more types that need to be specified at the point of use. These types are referred to as type parameters. When declaring a parameter, an identifier must be provided for reference within the declaration body.
- **Type Variable**: After declaring a type parameter, when these types are referenced via identifiers, these identifiers are called type variables.
- **Type Argument**: When specifying generic parameters while using a generic type or function, these parameters are called type arguments.
- **Type Constructor**: A type that requires zero, one, or more types as arguments is called a type constructor.

Type parameters are generally declared after the type name or function name, enclosed in angle brackets `<...>`. For example, a generic list can be declared as:

<!-- compile -->

```cangjie
class List<T> {
    var elem: Option<T> = None
    var tail: Option<List<T>> = None
}

func sumInt(a: List<Int64>) {  }
```

Here, `T` in `List<T>` is called a type parameter. The reference to `T` in `elem: Option<T>` is called a type variable, and similarly, `T` in `tail: Option<List<T>>` is also a type variable. In the parameter of the function `sumInt`, `Int64` in `List<Int64>` is called the type argument for `List`. `List` is the type constructor, and `List<Int64>` constructs a list type for `Int64` using the type argument `Int64`.