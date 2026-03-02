# Iterable and Collections

We have previously learned about Range, Array, and ArrayList, all of which can be traversed using for-in operations. For types defined by developers, similar traversal operations can also be implemented.

Range, Array, and ArrayList all support the for-in syntax through Iterable.

Iterable is a built-in interface with the following form (only core code is shown):

```cangjie
interface Iterable<T> {
    func iterator(): Iterator<T>
    ...
}
```

The iterator function requires the returned Iterator type to be another built-in interface with the following form (only core code is shown):

```cangjie
interface Iterator<T> <: Iterable<T> {
    mut func next(): Option<T>
    ...
}
```

You can use the for-in syntax to traverse any instance of a type that implements the Iterable interface.

Assume we have the following for-in code:

<!-- run -->

```cangjie
let list = [1, 2, 3]
for (i in list) {
    println(i)
}
```

It is equivalent to the following while code:

<!-- run -->

```cangjie
let list = [1, 2, 3]
var it = list.iterator()
while (true) {
    match (it.next()) {
        case Some(i) => println(i)
        case None => break
    }
}
```

Another common method for traversing Iterable types is to use pattern matching in the condition of a while expression. For example, another equivalent form of the above while code is:

<!-- run -->

```cangjie
let list = [1, 2, 3]
var it = list.iterator()
while (let Some(i) <- it.next()) {
    println(i)
}
```

Array, ArrayList, HashSet, and HashMap types all implement Iterable, so they can be used in for-in or while loops.