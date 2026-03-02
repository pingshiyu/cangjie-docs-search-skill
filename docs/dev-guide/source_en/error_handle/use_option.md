# Using Option

The [Option type](../enum_and_pattern_match/option_type.md) was introduced earlier, defining its characteristics. Since the Option type can represent both a value and the absence of a value (where the absence may be interpreted as an error in certain contexts), it can also be used for error handling.

For example, in the following case, if the parameter value of the function `getOrThrow` equals `Some(v)`, it returns the value `v`; if the parameter equals `None`, it throws an exception.

<!-- compile -->

```cangjie
func getOrThrow(a: ?Int64) {
    match (a) {
        case Some(v) => v
        case None => throw NoneValueException()
    }
}
```

Because `Option` is an extremely common type, Cangjie provides multiple destructuring methods to facilitate its usage, including: pattern matching, the `getOrThrow` function, the `coalescing` operator (`??`), and the question mark operator (`?`). Each of these methods will be explained in detail below.

- **Pattern Matching**: Since the Option type is an enum type, the pattern matching for enums mentioned earlier can be used to destructure `Option` values. For example, in the following function `getString`, which takes a parameter of type `?Int64`, if the parameter is a `Some` value, it returns the string representation of the contained number; if the parameter is `None`, it returns the string `"none"`.

    <!-- verify -->

    ```cangjie
    func getString(p: ?Int64): String{
        match (p) {
            case Some(x) => "${x}"
            case None => "none"
        }
    }
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1 = getString(a)
        let r2 = getString(b)
        println(r1)
        println(r2)
    }
    ```

   The execution result of the above code is:

    ```text
    1
    none
    ```

- **Coalescing Operator (`??`)**: For an expression `e1` of type `?T`, if you want to return a value `e2` of type `T` when `e1` equals `None`, you can use the `??` operator. For the expression `e1 ?? e2`, if `e1` equals `Some(v)`, it returns `v`; otherwise, it returns `e2`. Example:

    <!-- verify -->

    ```cangjie
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1: Int64 = a ?? 0
        let r2: Int64 = b ?? 0
        println(r1)
        println(r2)
    }
    ```

   The execution result of the above code is:

    ```text
    1
    0
    ```

- **Question Mark Operator (`?`)**: The `?` operator must be used in conjunction with `.`, `()`, `[]`, or `{}` (specifically in trailing lambda calls) to enable support for these operations on `Option` types. Taking `.` as an example (similarly for `()`, `[]`, and `{}`), for an expression `e` of type `?T1`, when `e` equals `Some(v)`, the value of `e?.b` is `Option<T2>.Some(v.b)`; otherwise, it is `Option<T2>.None`, where `T2` is the type of `v.b`. Example:

    <!-- compile -->

    ```cangjie
    struct R {
        public var a: Int64
        public init(a: Int64) {
            this.a = a
        }
    }

    let r = R(100)
    let x = Some(r)
    let y = Option<R>.None
    let r1 = x?.a   // r1 = Option<Int64>.Some(100)
    let r2 = y?.a   // r2 = Option<Int64>.None

    class C {
        var item: Int64 = 100
    }
    let c = C()
    let c1 = Option<C>.Some(c)
    let c2 = Option<C>.None
    func test1() {
        c1?.item = 200             // c.item = 200
        c2?.item = 300             // no effect
    }
    ```

   The question mark operator (`?`) supports multi-level access. For example, in `a?.b.c?.d` (similarly for `()`, `[]`, and `{}`), the expression `a` must be of type `Option<T1>`, where `T1` contains an instance member `b`. The type of `b` must contain an instance member `c`, and `c` must be of type `Option<T2>`, where `T2` contains an instance member `d`. The type of `a?.b.c?.d` is `Option<T3>`, where `T3` is the type of `T2`'s instance member `d`. When `a` equals `Some(va)` and `va.b.c` equals `Some(vc)`, the value of `a?.b.c?.d` is `Option<T3>.Some(vc.d)`. When `a` equals `Some(va)` but `va.b.c` equals `None`, the value is `Option<T3>.None` (`d` is not evaluated). When `a` equals `None`, the value is `Option<T3>.None` (`b`, `c`, and `d` are not evaluated).

    <!-- compile -->

    ```cangjie
    class A {
        public var b: B = B()
    }

    class B {
        public var c: Option<C> = C()
        public var c1: Option<C> = Option<C>.None
    }

    class C {
        public var d: Int64 = 100
    }

    main(){
        var a = Some(A())
        let a1 = a?.b.c?.d  // a1 = Option<Int64>.Some(100)
        let a2 = a?.b.c1?.d // a2 = Option<Int64>.None
        a?.b.c?.d = 200     // a.b.c.d = 200
        a?.b.c1?.d = 200    // no effect
    }
    ```

- **`getOrThrow` Function**: For an expression `e` of type `?T`, you can destructure it by calling the `getOrThrow` function. When `e` equals `Some(v)`, `getOrThrow()` returns `v`; otherwise, it throws an exception. Example:

    <!-- verify -->

    ```cangjie
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1 = a.getOrThrow()
        println(r1)
        try {
            let r2 = b.getOrThrow()
        } catch (e: NoneValueException) {
            println("b is None")
        }
    }
    ```

   The execution result of the above code is:

    ```text
    1
    b is None
    ```