# ArrayList

To use the ArrayList type, you need to import the collection package:

<!-- run -->

```cangjie
import std.collection.*
```

In Cangjie, `ArrayList<T>` represents the ArrayList type, where T denotes the element type of the ArrayList, which can be any type.

ArrayList has excellent expansion capabilities, making it suitable for scenarios requiring frequent addition and deletion of elements.

Compared to Array, ArrayList allows both in-place modification of elements and in-place addition/deletion of elements.

The mutability of ArrayList is a highly useful feature, enabling all references to the same ArrayList instance to share the same elements and apply unified modifications.

```cangjie
var a: ArrayList<Int64> = ... // ArrayList whose element type is Int64
var b: ArrayList<String> = ... // ArrayList whose element type is String
```

ArrayLists with different element types are distinct types and therefore cannot be assigned to each other.

Thus, the following example is invalid:

```cangjie
b = a // Type mismatch
```

In Cangjie, you can construct a specific ArrayList using constructors.

<!-- run -->

```cangjie
let a = ArrayList<String>() // Created an empty ArrayList whose element type is String
let b = ArrayList<String>(100) // Created an ArrayList whose element type is String, and allocate a space of 100
let c = ArrayList<Int64>([0, 1, 2]) // Created an ArrayList whose element type is Int64, containing elements 0, 1, 2
let d = ArrayList<Int64>(c) // Use another Collection to initialize an ArrayList
let e = ArrayList<String>(2, {x: Int64 => x.toString()}) // Created an ArrayList whose element type is String and size is 2. All elements are initialized by specified rule function
```

## Accessing ArrayList Members

When you need to access all elements of an ArrayList, you can use a for-in loop to iterate through them.

<!-- verify -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>([0, 1, 2])
    for (i in list) {
        println("The element is ${i}")
    }
}
```

Compiling and executing the above code will output:

```text
The element is 0
The element is 1
The element is 2
```

To determine the number of elements in an ArrayList, you can use the `size` property.

<!-- verify -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>([0, 1, 2])
    if (list.size == 0) {
        println("This is an empty arraylist")
    } else {
        println("The size of arraylist is ${list.size}")
    }
}
```

Compiling and executing the above code will output:

```text
The size of arraylist is 3
```

To access a single element at a specified position, you can use subscript syntax (the subscript must be of type Int64). The first element of a non-empty ArrayList always starts at position 0. You can access any element from 0 up to the last position (ArrayList's size - 1). Using a negative index or an index greater than or equal to the size will trigger a runtime exception.

```cangjie
let a = list[0] // a == 0
let b = list[1] // b == 1
let c = list[-1] // Runtime exceptions
```

ArrayList also supports Range syntax in subscripts. For details, refer to the [Array](../basic_data_type/array.md#array) chapter.

## Modifying ArrayList

You can use subscript syntax to modify elements at specific positions.

<!-- run -->

```cangjie
let list = ArrayList<Int64>([0, 1, 2])
list[0] = 3
```

ArrayList is a reference type. When used as an expression, ArrayList does not create a copy; all references to the same ArrayList instance share the same data.

Thus, modifications to ArrayList elements affect all references to that instance.

<!-- run -->

```cangjie
let list1 = ArrayList<Int64>([0, 1, 2])
let list2 = list1
list2[0] = 3
// list1 contains elements 3, 1, 2
// list2 contains elements 3, 1, 2
```

To add a single element to the end of an ArrayList, use the `add` function. To add multiple elements simultaneously, use the `add(all!: Collection<T>)` function, which accepts other Collection types with the same element type, such as Array. For details on Collection types, refer to [Basic Collection Type Overview](collection_overview.md).

<!-- run -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>()
    list.add(0) // list contains element 0
    list.add(1) // list contains elements 0, 1
    let li = [2, 3]
    list.add(all: li) // list contains elements 0, 1, 2, 3
}
```

You can use the `add(T, at!: Int64)` and `add(all!: Collection<T>, at!: Int64)` functions to insert a single element or a Collection of the same element type at a specified index. The element at that index and subsequent elements will be shifted to make space.

<!-- run -->

```cangjie
let list = ArrayList<Int64>([0, 1, 2]) // list contains elements 0, 1, 2
list.add(4, at: 1) // list contains elements 0, 4, 1, 2
```

To remove an element from an ArrayList, use the `remove` function, specifying the index to remove. Subsequent elements will be shifted forward to fill the gap.

<!-- run -->

```cangjie
let list = ArrayList<String>(["a", "b", "c", "d"]) // list contains the elements "a", "b", "c", "d"
list.remove(at: 1) // Delete the element at subscript 1, now the list contains elements "a", "c", "d"
```

## Increasing ArrayList Size

Each ArrayList requires a specific amount of memory to store its contents. When adding elements to an ArrayList causes it to exceed its reserved capacity, the ArrayList allocates a larger memory region and copies all elements to the new memory. This growth strategy means that add operations triggering reallocation incur performance costs, but as the ArrayList's reserved memory grows larger, these operations occur less frequently.

If you know approximately how many elements you'll be adding, you can pre-allocate sufficient memory before adding to avoid intermediate reallocations, thereby improving performance.

<!-- run -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>(100) // Allocate space at once
    for (i in 0..100) {
        list.add(i) // Does not trigger reallocation of space
    }
    list.reserve(100) // Prepare more space
    for (i in 0..100) {
        list.add(i) // Does not trigger reallocation of space
    }
}
```