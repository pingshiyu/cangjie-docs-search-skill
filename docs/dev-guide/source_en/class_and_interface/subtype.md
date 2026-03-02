# Subtype Relationships

Like other object-oriented languages, the Cangjie language provides subtype relationships and subtype polymorphism. Examples include (but are not limited to the following use cases):

- If a function's formal parameter is of type `T`, the actual type of the argument passed during the function call can be either `T` or a subtype of `T` (strictly speaking, the subtypes of `T` already include `T` itself, and the same applies below).
- If the type of the variable on the left-hand side of an assignment expression `=` is `T`, the actual type of the expression on the right-hand side of `=` can be either `T` or a subtype of `T`.
- If the user-annotated return type in a function definition is `T`, the type of the function body (and the types of all `return` expressions within the function body) can be either `T` or a subtype of `T`.

The following sections describe several scenarios where two types form a subtype relationship.

## Subtype Relationships Introduced by Class Inheritance

After inheriting from a class, the subclass becomes a subtype of the parent class. In the following code, `Sub` is a subtype of `Super`.

<!-- compile -->

```cangjie
open class Super {}
class Sub <: Super {}
```

## Subtype Relationships Introduced by Interface Implementation

After implementing an interface (including extension implementations), the type implementing the interface becomes a subtype of the interface. In the following code, `I3` is a subtype of `I1` and `I2`, `C` is a subtype of `I1`, and `Int64` is a subtype of `I2`:

<!-- compile -->

```cangjie
interface I1 {}
interface I2 {}

interface I3 <: I1 & I2 {}

class C <: I1 {}

extend Int64 <: I2 {}
```

## Subtype Relationships of Tuple Types

Tuple types in the Cangjie language also have subtype relationships. Intuitively, if each element type of a tuple `t1` is a subtype of the corresponding element type in another tuple `t2`, then the type of tuple `t1` is also a subtype of the type of tuple `t2`. For example, in the following code, since `C2 <: C1` and `C4 <: C3`, it follows that `(C2, C4) <: (C1, C3)` and `(C4, C2) <: (C3, C1)`.

<!-- compile -->

```cangjie
open class C1 {}
class C2 <: C1 {}

open class C3 {}
class C4 <: C3 {}

let t1: (C1, C3) = (C2(), C4()) // OK
let t2: (C3, C1) = (C4(), C2()) // OK
```

## Subtype Relationships of Function Types

In the Cangjie language, functions are first-class citizens, and function types also have subtype relationships: Given two function types `(U1) -> S2` and `(U2) -> S1`, `(U1) -> S2` is a subtype of `(U2) -> S1` if and only if `U2` is a subtype of `U1` and `S2` is a subtype of `S1` (note the order). For example, the following code defines two functions `f : (U1) -> S2` and `g : (U2) -> S1`, where the type of `f` is a subtype of the type of `g`. Since the type of `f` is a subtype of `g`, `f` can be used wherever `g` is used.

<!-- compile -->

```cangjie
open class U1 {}
class U2 <: U1 {}

open class S1 {}
class S2 <: S1 {}


func f(a: U1): S2 { S2() }
func g(a: U2): S1 { S1() }

func call1() {
    g(U2()) // OK
    f(U2()) // OK
}

func h(lam: (U2) -> S1): S1 {
    lam(U2())
}

func call2() {
    h(g) // OK
    h(f) // OK
}
```

For the above rule, the `S2 <: S1` part is easy to understand: The result data produced by a function call will be used by subsequent programs. Function `g` can produce result data of type `S1`, and function `f` can produce result data of type `S2`. The result data produced by `g` should be replaceable by the result data produced by `f`, hence the requirement that `S2 <: S1`.

For the `U2 <: U1` part, it can be understood as follows: Before a function call produces a result, it must be callable. The actual argument type of the function call remains fixed, while the formal parameter type can be more permissive and still be callable. However, if the formal parameter type is more restrictive, it may not be callable—for example, given the definitions in the above code, `g(U2())` can be replaced with `f(U2())` precisely because the actual argument type `U2` is more restrictive than the formal parameter type `U1`.

## Subtype Relationships That Always Hold

In the Cangjie language, some predefined subtype relationships always hold:

- A type `T` is always a subtype of itself, i.e., `T <: T`.
- The `Nothing` type is always a subtype of any other type `T`, i.e., `Nothing <: T`.
- Any type `T` is a subtype of the `Any` type, i.e., `T <: Any`.
- Any type defined by a `class` is a subtype of `Object`, i.e., if `class C {}` exists, then `C <: Object`.

## Subtype Relationships Introduced by Transitivity

Subtype relationships are transitive. In the following code, although only `I2 <: I1`, `C <: I2`, and `Bool <: I2` are described, the transitivity of subtypes implicitly establishes `C <: I1` and `Bool <: I1` as subtype relationships.

<!-- compile -->

```cangjie
interface I1 {}
interface I2 <: I1 {}

class C <: I2 {}

extend Bool <: I2 {}
```

## Subtype Relationships of Generic Types

Generic types also have subtype relationships. For details, see [Subtype Relationships of Generic Types](../generic/generic_subtype.md).