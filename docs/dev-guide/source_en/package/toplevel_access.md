# Visibility of Top-Level Declarations

In the Cangjie programming language, access modifiers can be used to control the visibility of top-level declarations such as types, variables, and functions. Cangjie provides four access modifiers: `private`, `internal`, `protected`, and `public`. The semantics of these modifiers when applied to top-level elements are as follows:

- `private`: Visible only within the current file. Members with this modifier cannot be accessed from different files.
- `internal`: Visible only within the current package and its subpackages (including nested subpackages). Members can be accessed without import within the same package, while subpackages (including nested subpackages) can access these members through imports.
- `protected`: Visible only within the current module. Files in the same package can access these members without import, while other packages within the same module (but in different packages) can access them through imports. Packages from different modules cannot access these members.
- `public`: Visible both inside and outside the module. Files in the same package can access these members without import, while other packages can access them through imports.

| Modifier       | File | Package & Subpackages | Module | All Packages |
|---------------|------|-----------------------|--------|--------------|
| `private`     | Y    | N                     | N      | N            |
| `internal`    | Y    | Y                     | N      | N            |
| `protected`   | Y    | Y                     | Y      | N            |
| `public`      | Y    | Y                     | Y      | Y            |

Different top-level declarations support specific access modifiers and have default modifiers (default modifiers apply when the modifier is omitted; these defaults can also be explicitly specified):

- `package`: Supports `internal`, `protected`, and `public`, with `public` as the default modifier.
- `import`: Supports all access modifiers, with `private` as the default modifier.
- Other top-level declarations support all access modifiers, with `internal` as the default modifier.

<!-- compile -->

```cangjie
package a

private func f1() { 1 }   // f1 is visible only within the current file
func f2() { 2 }           // f2 is visible only within the current package and subpackages
protected func f3() { 3 } // f3 is visible only within the current module
public func f4() { 4 }    // f4 is visible both inside and outside the module
```

The access level hierarchy in Cangjie is `public > protected > internal > private`. The access modifier of a declaration cannot be higher than the access level of the types used within that declaration. Refer to the following examples:

- Parameters and return values in function declarations

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    class C {}
    public func f1(a1: C) // Error, public declaration f1 cannot use internal type C.
    {
        return 0
    }
    public func f2(a1: Int8): C // Error, public declaration f2 cannot use internal type C.
    {
        return C()
    }
    public func f3 (a1: Int8) // Error, public declaration f3 cannot use internal type C.
    {
        return C()
    }
    ```

- Variable declarations

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    class C {}
    public let v1: C = C() // Error, public declaration v1 cannot use internal type C.
    public let v2 = C() // Error, public declaration v2 cannot use internal type C.
    ```

- Type arguments for generic types

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    public class C1<T> {}
    class C2 {}
    public let v1 = C1<C2>() // Error, public declaration v1 cannot use internal type C2.
    ```

- Type bounds in `where` constraints

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    interface I {}
    public class B<T> where T <: I {}  // Error, public declaration B cannot use internal type I.
    ```

Notably:

- `public` declarations can use any types visible within their package in their initialization expressions or function bodies, including both `public` and non-`public` types.

    <!-- compile -->

    ```cangjie
    // a.cj
    package a
    class C1 {}
    func f1(a1: C1)
    {
      return 0
    }
    public func f2(a1: Int8) // OK.
    {
      var v1 = C1()
      return 0
    }
    public let v1 = f1(C1()) // OK.
    public class C2 // OK.
    {
      var v2 = C1()
    }
    ```

- `public` top-level declarations can use anonymous functions or any top-level functions, including both `public` and non-`public` top-level functions.

    <!-- compile -toplevel-->

    ```cangjie
    public var t1: () -> Unit = { => } // OK.
    func f1(): Unit {}
    public let t2 = f1 // OK.

    public func f2() // OK.
    {
      return f1
    }
    ```

- Built-in types such as `Rune` and `Int64` default to `public` visibility.

    <!-- compile -toplevel-->

    ```cangjie
    var num = 5
    public var t3 = num // OK.
    ```

> **Note:**
>
> Within the same package, `private` custom types (e.g., `struct`, `class`, `enum`, and `interface`) with the same name are not supported in certain scenarios. Unsupported cases will trigger compiler errors.

For example, in the following program, `example1.cj` and `example2.cj` share the same package name. `example1.cj` defines a `private` class `A`, while `example2.cj` defines a `private` struct `A`.

<!-- compile -->

```cangjie
// example1.cj
package test

private class A {}

public class D<T> {
    private let a: A = A()
}
```

<!-- compile -->

```cangjie
// example2.cj
package test

private struct A {}

public class C<T> {
    private let a: A = A()
}
```

Running this program will output:

```text
error: currently, it is not possible to export two private declarations with the same name
```