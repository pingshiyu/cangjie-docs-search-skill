# Floating-Point Types

Floating-point types include `Float16`, `Float32`, and `Float64`, which are used to represent floating-point numbers (numbers with fractional parts, such as 3.14159, 8.24, and 0.1) with encoding lengths of `16-bit`, `32-bit`, and `64-bit`, respectively. `Float16`, `Float32`, and `Float64` correspond to the half-precision format (binary16), single-precision format (binary32), and double-precision format (binary64) in IEEE 754.

The precision (number of significant digits) of `Float64` is approximately 15 digits, `Float32` has a precision of about 6 digits, and `Float16` has a precision of about 3 digits. The choice of floating-point type depends on the nature and range of the floating-point numbers to be processed in the code. When multiple floating-point types are suitable, the higher-precision type is preferred because lower-precision types are prone to accumulated calculation errors and have a limited range of precisely representable integers.

## Floating-Point Literals

Floating-point literals can be represented in two radix forms: decimal and hexadecimal. In decimal notation, a floating-point literal must contain at least an integer part or a fractional part, and if there is no fractional part, it must include an exponent part (prefixed with `e` or `E`, with a base of 10). In hexadecimal notation, a floating-point literal must contain at least an integer part or fractional part (prefixed with `0x` or `0X`) and must include an exponent part (prefixed with `p` or `P`, with a base of 2).

The following examples demonstrate the use of floating-point literals:

<!-- compile -->

```cangjie
let a: Float32 = 3.14       // a is 3.140000 with type Float32
let b: Float32 = 2e3        // b is 2000.000000 with type Float32
let c: Float32 = 2.4e-1     // c is 0.240000 with type Float32
let d: Float64 = .123e2     // d is 12.300000 with type Float64
let e: Float64 = 0x1.1p0    // e is 1.062500 with type Float64
let f: Float64 = 0x1p2      // f is 4.000000 with type Float64
let g: Float64 = 0x.2p4     // g is 2.000000 with type Float64
```

When using decimal floating-point literals, the type can be explicitly specified by adding a suffix. The correspondence between suffixes and types is as follows:

|  Suffix | Type    |
| :----- | :------ |
| f16    | Float16 |
| f32    | Float32 |
| f64    | Float64 |

Floating-point literals with suffixes can be used as shown below:

<!-- compile -->

```cangjie
let a = 3.14f32   // a is 3.140000 with type Float32
let b = 2e3f32    // b is 2000.000000 with type Float32
let c = 2.4e-1f64 // c is 0.240000 with type Float64
let d = .123e2f64 // d is 12.300000 with type Float64
```

## Supported Operations for Floating-Point Types

Floating-point types natively support the following operators: arithmetic operators, relational operators, and compound assignment operators. Floating-point types do not support increment and decrement operators.

Floating-point types can be converted between each other, as well as between floating-point types and integer types. For specific type conversion syntax and rules, refer to [Numeric Type Conversions](../class_and_interface/typecast.md#numeric-type-conversions).