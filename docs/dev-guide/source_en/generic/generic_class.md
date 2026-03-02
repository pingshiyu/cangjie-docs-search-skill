# Generic Classes

[Generic Interfaces](./generic_interface.md) introduced the definition and usage of generic interfaces. This section covers the definition and usage of generic classes. For example, the key-value pairs in `Map` are defined using generic classes.

The `Node` type for key-value pairs in `Map` can be defined using a generic class:

<!-- compile -->

```cangjie
open class Node<K, V> where K <: Hashable & Equatable<K> {
    var key: Option<K> = Option<K>.None
    var value: Option<V> = Option<V>.None

    init() {}

    init(key: K, value: V) {
        this.key = Option<K>.Some(key)
        this.value = Option<V>.Some(value)
    }
}
```

Since the types of keys and values may differ and can be any type that meets certain conditions, the `Node` class requires two type parameters `K` and `V`. The constraint `K <: Hashable, K <: Equatable<K>` specifies that the key type `K` must implement both the `Hashable` and `Equatable<K>` interfaces, which are the conditions `K` must satisfy. For more details on generic constraints, refer to the [Generic Constraints](./generic_constraint.md) section.

Because static member variables of generic classes share memory, the type declarations and expressions of static member variables or properties cannot reference type parameters or contain uninstantiated generic type expressions. Additionally, static variable or property initialization expressions cannot call static member functions or properties of generic classes.

<!-- compile.error -->

```cangjie
class A<T> {}
class B<T> {
    static func foo() {1}
    static var err1: A<T> = A<T>() // Error, static member cannot depend on generic parameter 'Generics-T'
    static prop err2: A<T> { // Error, static member cannot depend on generic parameter 'Generics-T'
        get() {
            A<T>() // Error, static member cannot depend on generic parameter 'Generics-T'
        }
    }
    static var vfoo = foo() // Error, it's equal to 'static var vfoo = B<T>.foo()', implicit reference to generic 'T'.
    static var ok: Int64 = 1
}

main() {
    B<Int32>.ok = 2
    println(B<Int64>.ok) // 2
}
```