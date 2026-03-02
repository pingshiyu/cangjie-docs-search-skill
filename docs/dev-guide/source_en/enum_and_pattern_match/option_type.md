# The Option Type

The `Option` type is defined using an `enum` with two constructors: `Some` and `None`. The `Some` variant carries a parameter indicating a value is present, while `None` takes no parameters and represents the absence of a value. The `Option` type is used when you need to represent that a value of a certain type may or may not exist.

The `Option` type is defined as a generic `enum` as follows (note that the angle brackets contain a type parameter `T`. When `T` is instantiated with different types, different `Option` types are produced. For detailed information about generics, refer to [Generics](../generic/generic_overview.md)):

<!-- compile -->

```cangjie
enum Option<T> {
    | Some(T)
    | None
}
```

Here, the parameter type of the `Some` constructor is the type parameter `T`. When `T` is instantiated with different types, different `Option` types are obtained, such as `Option<Int64>`, `Option<String>`, etc.

There is also a shorthand notation for the `Option` type: prefixing the type name with `?`. That is, for any type `Ty`, `?Ty` is equivalent to `Option<Ty>`. For example, `?Int64` is equivalent to `Option<Int64>`, `?String` is equivalent to `Option<String>`, and so on.

The following examples demonstrate how to define variables of the `Option` type:

<!-- compile -->

```cangjie
let a: Option<Int64> = Some(100)
let b: ?Int64 = Some(100)
let c: Option<String> = Some("Hello")
let d: ?String = None
```

Additionally, although `T` and `Option<T>` are different types, when it is explicitly known that an `Option<T>` value is required in a certain context, you can directly pass a value of type `T`. The compiler will automatically wrap the `T` value into an `Option<T>` using the `Some` constructor (note: this is not a type conversion). For example, the following definitions are legal (equivalent to the definitions of variables `a`, `b`, and `c` in the previous example):

<!-- compile -->

```cangjie
let a: Option<Int64> = 100
let b: ?Int64 = 100
let c: Option<String> = "100"
```

When there is no explicit type requirement in the context, you cannot use `None` directly to construct the desired type. In such cases, you should use the `None<T>` syntax to construct an `Option<T>` value, for example:

<!-- compile -->

```cangjie
let a = None<Int64> // a: Option<Int64>
let b = None<Bool> // b: Option<Bool>
```

Finally, for usage of `Option`, refer to [Using Option](../error_handle/use_option.md).