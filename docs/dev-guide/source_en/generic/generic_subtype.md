# Subtyping Relationships of Generic Types

Instantiated generic types also have subtyping relationships. For example:

<!-- compile -->

```cangjie
interface I<X, Y> { }

class C<Z> <: I<Z, Z> { }
```

Based on `class C<Z> <: I<Z, Z> { }`, we know that `C<Bool> <: I<Bool, Bool>` and `C<D> <: I<D, D>` hold, among others. This can be interpreted as "For all types `Z` without type variables, `C<Z> <: I<Z, Z>` holds."

However, for the following code:

<!-- compile -->

```cangjie
open class C { }
class D <: C { }

interface I<X> { }
```

`I<D> <: I<C>` does not hold (even though `D <: C` holds). This is because in the Cangjie language, user-defined type constructors are **invariant** at their type parameters.

The formal definition of variance is: If `A` and `B` are (instantiated) types, and `T` is a type constructor with a type parameter `X` (e.g., `interface T<X>`), then:

- If `T(A) <: T(B)` if and only if `A = B`, then `T` is **invariant**.
- If `T(A) <: T(B)` if and only if `A <: B`, then `T` is **covariant** at `X`.
- If `T(A) <: T(B)` if and only if `B <: A`, then `T` is **contravariant** at `X`.

In the current version of Cangjie, all user-defined generic types are invariant at all their type parameters. Therefore, given `interface I<X>` and types `A`, `B`, `I<A> <: I<B>` holds only if `A = B`. Conversely, if `I<A> <: I<B>` is known, we can deduce `A = B` (with the exception of built-in types: built-in tuple types are covariant at each of their element types; built-in function types are contravariant at their parameter types and covariant at their return types.)

> **Note:**
>
> For types other than `class` that implement interfaces, the subtyping relationship between the type and the interface cannot serve as a basis for covariance or contravariance.

Invariance limits some expressive power of the language but also avoids certain safety issues, such as the "covariant array runtime exception" problem.