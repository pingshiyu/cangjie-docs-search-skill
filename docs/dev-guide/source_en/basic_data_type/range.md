# Range Type

The range type is used to represent sequences with a fixed step size. It is a [generic](../generic/generic_overview.md) type denoted as `Range<T>`. When `T` is instantiated with different types, the type must support relational operators and be capable of addition with values of type `Int64`, resulting in different range types. For example, the most commonly used `Range<Int64>` represents integer ranges.

Each instance of a range type contains three values: `start`, `end`, and `step`. Here, `start` and `end` represent the initial and terminal values of the sequence, respectively, while `step` denotes the difference between consecutive elements (i.e., the step size). The types of `start` and `end` are the same (i.e., the type with which `T` is instantiated), whereas `step` is of type `Int64` and cannot be equal to `0`.

The following example demonstrates how to instantiate range types (for details on range type definitions and their properties, refer to the *Cangjie Programming Language Library API*):

<!-- compile -->

```cangjie
// Range<T>(start: T, end: T, step: Int64, hasStart: Bool, hasEnd: Bool, isClosed: Bool)
let r1 = Range<Int64>(0, 10, 1, true, true, true) // r1 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
let r2 = Range<Int64>(0, 10, 1, true, true, false) // r2 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r3 = Range<Int64>(10, 0, -2, true, true, false) // r3 contains 10, 8, 6, 4, 2
```

## Range Type Literals

Range literals come in two forms: "left-closed right-open" and "left-closed right-closed" ranges.

- The "left-closed right-open" range is formatted as `start..end : step`, representing a range that starts at `start`, increments by `step`, and ends before `end` (excluding `end`).
- The "left-closed right-closed" range is formatted as `start..=end : step`, representing a range that starts at `start`, increments by `step`, and includes `end` (including `end`).

The following example defines several range-type variables:

<!-- compile -->

```cangjie
let n = 10
let r1 = 0..10 : 1   // r1 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r2 = 0..=n : 1   // r2 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
let r3 = n..0 : -2   // r3 contains 10, 8, 6, 4, 2
let r4 = 10..=0 : -2 // r4 contains 10, 8, 6, 4, 2, 0
```

In range literals, `step` can be omitted, in which case it defaults to `1`. However, the value of `step` cannot be `0`. Additionally, a range may be empty (i.e., a sequence containing no elements), as shown below:
<!-- compile.error -->

```cangjie
let r5 = 0..10   // the step of r5 is 1, and r5 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r6 = 0..10 : 0 // Error, step cannot be 0

let r7 = 10..0 : 1 // r7 to r10 are empty ranges
let r8 = 0..10 : -1
let r9 = 10..=0 : 1
let r10 = 0..=10 : -1
```

> **Note:**
>
> - For the expression `start..end : step`, when `step > 0` and `start >= end`, or when `step < 0` and `start <= end`, `start..end : step` is an empty range.
> - For the expression `start..=end : step`, when `step > 0` and `start > end`, or when `step < 0` and `start < end`, `start..=end : step` is an empty range.