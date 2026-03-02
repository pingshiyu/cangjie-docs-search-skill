# HashSet

To use the HashSet type, you need to import the collection package:

<!-- run -->

```cangjie
import std.collection.*
```

You can use the HashSet type to construct a Collection that contains only unique elements.

Cangjie uses `HashSet<T>` to represent the HashSet type, where T denotes the element type of the HashSet. T must be a type that implements both the Hashable and `Equatable<T>` interfaces, such as numeric values or String.

```cangjie
var a: HashSet<Int64> = ... // HashSet whose element type is Int64
var b: HashSet<String> = ... // HashSet whose element type is String
```

HashSets with different element types are distinct types, so they cannot be assigned to each other.

Therefore, the following example is invalid:

```cangjie
b = a // Type mismatch
```

In Cangjie, you can construct a specific HashSet using constructor methods.

<!-- run -->

```cangjie
let a = HashSet<String>() // Created an empty HashSet whose element type is String
let b = HashSet<String>(100) // Created a HashSet whose capacity is 100
let c = HashSet<Int64>([0, 1, 2]) // Created a HashSet whose element type is Int64, containing elements 0, 1, 2
let d = HashSet<Int64>(c) // Use another Collection to initialize a HashSet
let e = HashSet<Int64>(10, {x: Int64 => (x * x)}) // Created a HashSet whose element type is Int64 and size is 10. All elements are initialized by specified rule function
```

## Accessing HashSet Members

When you need to access all elements of a HashSet, you can use a for-in loop to iterate through all elements.

Note that HashSet does not guarantee element ordering based on insertion sequence, so traversal order may differ from insertion order.

<!-- verify -->

```cangjie
import std.collection.*

main() {
    let mySet = HashSet<Int64>([0, 1, 2])
    for (i in mySet) {
        println("The element is ${i}")
    }
}
```

Compiling and executing the above code might output:

```text
The element is 0
The element is 1
The element is 2
```

To determine the number of elements in a HashSet, use the size property.

<!-- verify -->

```cangjie
import std.collection.*

main() {
    let mySet = HashSet<Int64>([0, 1, 2])
    if (mySet.size == 0) {
        println("This is an empty hashset")
    } else {
        println("The size of hashset is ${mySet.size}")
    }
}
```

Compiling and executing the above code will output:

```text
The size of hashset is 3
```

To check if an element exists in a HashSet, use the contains function. It returns true if the element exists, otherwise false.

<!-- run -->

```cangjie
let mySet = HashSet<Int64>([0, 1, 2])
let a = mySet.contains(0) // a == true
let b = mySet.contains(-1) // b == false
```

## Modifying HashSet

HashSet is a mutable reference type that provides functionality for adding and removing elements.

The mutability of HashSet is a useful feature, allowing all references to the same HashSet instance to share the same elements and receive unified modifications.

To add a single element to a HashSet, use the add function. To add multiple elements simultaneously, use the `add(all!: Collection<T>)` function, which accepts another Collection type (such as Array) with the same element type. When the element doesn't exist, the add function performs the addition; when the element already exists in the HashSet, the add function has no effect.

<!-- run -->

```cangjie
let mySet = HashSet<Int64>()
mySet.add(0) // mySet contains elements 0
mySet.add(0) // mySet contains elements 0
mySet.add(1) // mySet contains elements 0, 1
let li = [2, 3]
mySet.add(all: li) // mySet contains elements 0, 1, 2, 3
```

HashSet is a reference type. When used as an expression, HashSet doesn't create copies—all references to the same HashSet instance share the same data.

Therefore, modifications to HashSet elements affect all references to that instance.

<!-- run -->

```cangjie
let set1 = HashSet<Int64>([0, 1, 2])
let set2 = set1
set2.add(3)
// set1 contains elements 0, 1, 2, 3
// set2 contains elements 0, 1, 2, 3
```

To remove elements from a HashSet, use the remove function, specifying the element to be removed.

<!-- run -->

```cangjie
let mySet = HashSet<Int64>([0, 1, 2, 3])
mySet.remove(1) // mySet contains elements 0, 2, 3
```