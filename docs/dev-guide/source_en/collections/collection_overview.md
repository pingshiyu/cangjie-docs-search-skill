# Overview of Basic Collection Types

This chapter introduces several fundamental Collection types commonly used in the Cangjie language, including Array, ArrayList, HashSet, and HashMap.

You can choose the appropriate type for specific business scenarios:

- **Array**: When you don't need to add or remove elements but require element modification
- **ArrayList**: When frequent element insertion, deletion, querying, and modification are needed
- **HashSet**: When you want each element to be unique
- **HashMap**: When you need to store a series of key-value mappings

The following table summarizes the basic characteristics of these types:

| Type Name        | Mutable Elements | Add/Remove Elements | Element Uniqueness | Ordered Sequence |
| --------------- | ---------------- | ------------------- | ------------------ | ---------------- |
| `Array<T>`      | Y                | N                   | N                  | Y                |
| `ArrayList<T>`  | Y                | Y                   | N                  | Y                |
| `HashSet<T>`    | N                | Y                   | Y                  | N                |
| `HashMap<K, V>` | K: N, V: Y       | Y                   | K: Y, V: N         | N                |