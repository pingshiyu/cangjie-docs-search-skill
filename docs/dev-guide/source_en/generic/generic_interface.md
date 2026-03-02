# Generic Interfaces

Generics can be used to define generic interfaces. Taking the `Iterable` interface from the standard library as an example, its member function `iterator` needs to return an `Iterator` type, which serves as a container's traverser. `Iterator` is a generic interface that contains a `next` member function for retrieving the next element from the container type. The return type of the `next` member function is a type that needs to be specified during usage, so `Iterator` requires the declaration of generic parameters.

<!-- compile -->

```cangjie
public interface Iterable<E> {
    func iterator(): Iterator<E>
}

public interface Iterator<E> <: Iterable<E> {
    func next(): Option<E>
}

public interface Collection<T> <: Iterable<T> {
     prop size: Int64
     func isEmpty(): Bool
}
```