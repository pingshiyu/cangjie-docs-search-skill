# Cangjie-C Interoperability

To ensure compatibility with existing ecosystems, Cangjie supports calling C functions and also allows C to call Cangjie functions.

## Calling C Functions from Cangjie

To call a C function in Cangjie, you need to declare the function using the `@C` and `foreign` keywords. However, `@C` can be omitted when modifying a `foreign` declaration.

For example, to call C's `rand` and `printf` functions with the following signatures:

```c
// stdlib.h
int rand();

// stdio.h
int printf (const char *fmt, ...);
```

The corresponding Cangjie code would be:

```cangjie
// declare the function by `foreign` keyword, and omit `@C`
foreign func rand(): Int32
foreign func printf(fmt: CString, ...): Int32

main() {
    // call this function by `unsafe` block
    let r = unsafe { rand() }
    println("random number ${r}")
    unsafe {
        var fmt = LibC.mallocCString("Hello, No.%d\n")
        printf(fmt, 1)
        LibC.free(fmt)
    }
}
```

Key points to note:

1. The `foreign` modifier indicates an external function declaration. Functions marked with `foreign` can only be declared, not implemented.
2. Parameters and return types of `foreign` functions must conform to the type mapping between C and Cangjie data types. Refer to [Type Mapping](./cangjie-c.md#type-mapping) for details.
3. Since C functions may perform unsafe operations, calls to `foreign` functions must be wrapped in an `unsafe` block, otherwise a compilation error will occur.
4. The `@C` modifier can only be used with `foreign` function declarations. Using it with other declarations will cause a compilation error.
5. `@C` can only modify `foreign` functions, non-generic functions in the top-level scope, and `struct` types.
6. `foreign` functions do not support named parameters or default values. Variadic parameters are allowed using `...` notation, but must appear last in the parameter list. Variadic parameters must satisfy the `CType` constraint but need not be of the same type.
7. Although Cangjie (CJNative backend) provides stack expansion capability, since C function stack usage is opaque to Cangjie, FFI calls into C functions still carry a risk of stack overflow (which may cause runtime crashes or undefined behavior). Developers should adjust `cjStackSize` configuration based on actual needs.

Examples of invalid `foreign` declarations:

```cangjie
foreign func rand(): Int32 { // compiler error
    return 0
}
@C
foreign var a: Int32 = 0 // compiler error
@C
foreign class A{} // compiler error
@C
foreign interface B{} // compiler error
```

## CFunc

`CFunc` in Cangjie refers to functions that can be called by C code, which come in three forms:

1. `foreign` functions modified by `@C`
2. Cangjie functions modified by `@C`
3. `CFunc` lambda expressions, which differ from regular lambdas in that they cannot capture variables.

<!-- run -->

```cangjie
// Case 1
foreign func free(ptr: CPointer<Int8>): Unit

// Case 2
@C
func callableInC(ptr: CPointer<Int8>) {
    print("This function is defined in Cangjie.")
}

// Case 3
let f1: CFunc<(CPointer<Int8>) -> Unit> = { ptr =>
    print("This function is defined with CFunc lambda.")
}
```

All three forms declare/define functions of type `CFunc<(CPointer<Int8>) -> Unit>`. `CFunc` corresponds to C's function pointer type. This is a generic type where the type parameter represents the `CFunc`'s parameter and return types. Usage example:

<!-- run -->

```cangjie
foreign func atexit(cb: CFunc<() -> Unit>): Int32
```

Like `foreign` functions, other forms of `CFunc` must satisfy the `CType` constraint for parameters and return types, and do not support named parameters or default values.

When called within Cangjie code, `CFunc` must be invoked in an `unsafe` context.

Cangjie supports converting a `CPointer<T>` variable to a concrete `CFunc`, where `CPointer`'s type parameter `T` can be any type satisfying the `CType` constraint. Example:

<!-- compile -->

```cangjie
main() {
    var ptr = CPointer<Int8>()
    var f = CFunc<() -> Unit>(ptr)
    unsafe { f() } // core dumped when running, because the pointer is nullptr.
}
```

> **Note:**
>
> Converting a pointer to `CFunc` and invoking it is dangerous. Users must ensure the pointer points to a valid function address, otherwise runtime errors will occur.

## inout Parameters

When calling `CFunc` in Cangjie, arguments can be modified with the `inout` keyword to form pass-by-reference expressions. These expressions have type `CPointer<T>`, where `T` is the type of the `inout`-modified expression.

Pass-by-reference expressions have the following constraints:

- Can only be used at `CFunc` call sites.
- The modified object's type must satisfy `CType` but cannot be `CString`.
- The modified object cannot be defined with `let`, nor can it be a literal, input parameter, or other temporary value.
- Pointers passed to C via pass-by-reference expressions are only guaranteed valid during the function call. C code should not store these pointers for later use.

`inout`-modified variables can be top-level variables, local variables, or `struct` member variables, but cannot be directly or indirectly derived from `class` instance member variables.

Example:

```cangjie
foreign func foo1(ptr: CPointer<Int32>): Unit

@C
func foo2(ptr: CPointer<Int32>): Unit {
    let n = unsafe { ptr.read() }
    println("*ptr = ${n}")
}

let foo3: CFunc<(CPointer<Int32>) -> Unit> = { ptr =>
    let n = unsafe { ptr.read() }
    println("*ptr = ${n}")
}

struct Data {
    var n: Int32 = 0
}

class A {
    var data = Data()
}

main() {
    var n: Int32 = 0
    unsafe {
        foo1(inout n)  // OK
        foo2(inout n)  // OK
        foo3(inout n)  // OK
    }
    var data = Data()
    var a = A()
    unsafe {
        foo1(inout data.n)   // OK
        foo1(inout a.data.n) // Error, n is derived indirectly from instance member variables of class A
    }
}
```

> **Note:**
>
> The `inout` parameter feature cannot currently be used in macro definitions when using macro expansion features.

## unsafe

Interoperability with C introduces many unsafe factors, so Cangjie uses the `unsafe` keyword to mark unsafe cross-C calls.

Key points about `unsafe`:

- Can modify functions, expressions, or scopes.
- Functions modified by `@C` must be called in an `unsafe` context.
- `CFunc` calls must occur in an `unsafe` context.
- `foreign` function calls in Cangjie must occur in an `unsafe` context.
- When calling an `unsafe`-modified function, the call site must be in an `unsafe` context.

Usage example:

<!-- run -->

```cangjie
foreign func rand(): Int32

@C
func foo(): Unit {
    println("foo")
}

var foo1: CFunc<() -> Unit> = { =>
    println("foo1")
}

main(): Int64 {
    unsafe {
        rand()           // Call foreign func.
        foo()            // Call @C func.
        foo1()           // Call CFunc var.
    }
    0
}
```

Note that regular `lambda`s cannot propagate `unsafe` attributes. When an `unsafe` `lambda` escapes, it can be called directly without an `unsafe` context without causing compilation errors. When needing to call `unsafe` functions within a `lambda`, it's recommended to make the call within an `unsafe` block:

<!-- run -->

```cangjie
unsafe func A(){}
unsafe func B(){
    var f = { =>
        unsafe { A() } // Avoid calling A() directly without unsafe in a normal lambda.
    }
    return f
}
main() {
    var f = unsafe{ B() }
    f()
    println("Hello World")
}
```

## Calling Conventions

Calling conventions describe how callers and callees interact (e.g., parameter passing, stack cleanup). Both sides must use the same calling convention. Cangjie uses `@CallingConv` to represent calling conventions, currently only supporting `CDECL`, which represents default calling convention for clang's C compiler across platforms, and more may be extended in the future as scenarios require.

C functions called via FFI use `CDECL` by default when no calling convention is specified. Example calling C's `rand`:

<!-- run -->

```cangjie
@CallingConv[CDECL]   // Can be omitted in default.
foreign func rand(): Int32

main() {
    println(unsafe { rand() })
}
```

`@CallingConv` can only modify `foreign` blocks, individual `foreign` functions, and top-level `CFunc` functions. When modifying a `foreign` block, it applies the same convention to all functions within.

## Usage Guidelines

- **OS Thread-Local Variable Constraints**

  When interoperating between Cangjie and C, using OS thread-local variables carries risks:

  1. Thread-local variables include those defined with C's `thread_local` or created via `pthread_key_create`.
  2. Cangjie has thread scheduling capabilities, where Cangjie threads may be scheduled to any OS thread randomly. Thus calling other languages' thread-local variables from Cangjie threads is risky.

  Example of risky thread-local variable usage:

  ```c
  // C language logic using thread_local
  static thread_local int64_t count = 0;
  int64_t getCount() {
      count++;
      return count;
  }
  ```

  ```cangjie
  foreign func getCount(): Int64
  // Cangjie invokes the preceding C language logic
  spawn {
      let r1 = unsafe { getCount() }  // r1 equals 1
      sleep(Duration.second * 10)
      let r2 = unsafe { getCount() }  // r2 may not be equal to 2
  }
  ```

- **Thread Binding Constraints**

  When Cangjie calls C for interop, Cangjie threads may be scheduled to any OS thread randomly. Thread priority and affinity behaviors are not recommended.

- **Synchronization Primitive Guidelines**

  When Cangjie calls C for interop, the Cangjie thread waits for the interop logic to complete. Long blocking behaviors in other languages are not recommended.

- **Fork Support**

  If C code called by Cangjie creates child processes via `fork()`, Cangjie logic cannot be executed in child processes. Other OS threads in the same process are unaffected.

- **Process Exit Considerations**

  If C code called by Cangjie exits the process, shared resources may be released, potentially causing illegal access errors.

## Type Mapping

### Basic TypesThe mapping between Cangjie and C language for basic data types follows these general principles

1. Cangjie types do not include reference types that point to managed memory;
2. Cangjie types and C types share the same memory layout.

For example, some basic type mappings are as follows:

| Cangjie Type |   C Type   |    Size (byte)     |
|:------------:|:----------:|:------------------:|
|    `Unit`    |   `void`   |         0          |
|    `Bool`    |   `bool`   |         1          |
|   `UInt8`    |   `char`   |         1          |
|    `Int8`    |  `int8_t`  |         1          |
|   `UInt8`    | `uint8_t`  |         1          |
|   `Int16`    | `int16_t`  |         2          |
|   `UInt16`   | `uint16_t` |         2          |
|   `Int32`    | `int32_t`  |         4          |
|   `UInt32`   | `uint32_t` |         4          |
|   `Int64`    | `int64_t`  |         8          |
|   `UInt64`   | `uint64_t` |         8          |
| `IntNative`  | `ssize_t`  | platform dependent |
| `UIntNative` |  `size_t`  | platform dependent |
|  `Float32`   |  `float`   |         4          |
|  `Float64`   |  `double`  |         8          |

> **Note:**
>
> Types like `int` and `long` have platform-dependent sizes, requiring programmers to explicitly specify corresponding Cangjie types. In C interoperation scenarios, similar to C, the `Unit` type can only be used as a return type in `CFunc` and as a generic parameter in `CPointer`.

Cangjie also supports mapping with C's struct and pointer types.

### Structs

For struct types, Cangjie uses `@C`-annotated `struct` for correspondence. For example, given this C struct:

```c
typedef struct {
    long long x;
    long long y;
    long long z;
} Point3D;
```

The corresponding Cangjie type can be defined as:

<!-- run -example00-->

```cangjie
@C
struct Point3D {
    var x: Int64 = 0
    var y: Int64 = 0
    var z: Int64 = 0
}
```

If there's a C function like:

```c
Point3D addPoint(Point3D p1, Point3D p2);
```

The corresponding Cangjie declaration would be:

<!-- run -example00-->

```cangjie
foreign func addPoint(p1: Point3D, p2: Point3D): Point3D
```

`@C`-annotated `struct`s must satisfy these constraints:

- Member variable types must satisfy the `CType` constraint
- Cannot implement or extend `interfaces`
- Cannot be used as associated value types for `enum`s
- Cannot be captured by closures
- Cannot have generic parameters

`@C`-annotated `struct`s automatically satisfy the `CType` constraint.

### Pointers

For pointer types, Cangjie provides `CPointer<T>` to correspond to C pointer types, where the generic parameter `T` must satisfy the `CType` constraint. For example, the C signature for `malloc`:

```c
void* malloc(size_t size);
```

Can be declared in Cangjie as:

<!-- run -->

```cangjie
foreign func malloc(size: UIntNative): CPointer<Unit>
```

`CPointer` supports read/write operations, pointer arithmetic, null checks, and conversion to integer form. Detailed APIs can be found in *The Cangjie Programming Language Library API*. Read/write and pointer arithmetic are unsafe operations that may cause undefined behavior if performed on invalid pointers, requiring `unsafe` blocks.

Example usage:

<!-- run -->

```cangjie
foreign func malloc(size: UIntNative): CPointer<Unit>
foreign func free(ptr: CPointer<Unit>): Unit

@C
struct Point3D {
    var x: Int64
    var y: Int64
    var z: Int64

    init(x: Int64, y: Int64, z: Int64) {
        this.x = x
        this.y = y
        this.z = z
    }
}

main() {
    let p1 = CPointer<Point3D>() // create a CPointer with null value
    if (p1.isNull()) {  // check if the pointer is null
        print("p1 is a null pointer")
    }

    let sizeofPoint3D: UIntNative = 24
    var p2 = unsafe { malloc(sizeofPoint3D) }    // malloc a Point3D in heap
    var p3 = unsafe { CPointer<Point3D>(p2) }    // pointer type cast

    unsafe { p3.write(Point3D(1, 2, 3)) } // write data through pointer

    let p4: Point3D = unsafe { p3.read() } // read data through pointer

    let p5: CPointer<Point3D> = unsafe { p3 + 1 } // offset of pointer

    unsafe { free(p2) }
}
```

Cangjie supports forced type conversion between `CPointer` types, where both source and target generic parameters must satisfy the `CType` constraint:

<!-- run -->

```cangjie
main() {
    var pInt8 = CPointer<Int8>()
    var pUInt8 = CPointer<UInt8>(pInt8) // CPointer<Int8> convert to CPointer<UInt8>
}
```

Cangjie also supports converting a `CFunc` type variable to a concrete `CPointer`, where the generic parameter can be any `CType`-satisfying type:

<!-- run -->

```cangjie
foreign func rand(): Int32
main() {
    var ptr = CPointer<Int8>(rand)
}
```

> **Warning:**
>
> While converting `CFunc` to a pointer is generally safe, performing `read` or `write` operations on the converted pointer may cause runtime errors.

### Arrays

Cangjie uses `VArray` to map to C array types. `VArray` can be used as function parameters and `@C struct` members. When element type `T` in `VArray<T, $N>` satisfies the `CType` constraint, `VArray<T, $N>` also satisfies `CType`.

**As function parameter types:**

When `VArray` is used as a `CFunc` parameter, the function signature can only be `CPointer<T>` or `VArray<T, $N>`. When the parameter type is `VArray<T, $N>`, the argument is still passed as `CPointer<T>`.

Example:

```cangjie
foreign func cfoo1(a: CPointer<Int32>): Unit
foreign func cfoo2(a: VArray<Int32, $3>): Unit
```

Corresponding C definitions:

```c
void cfoo1(int *a) { ... }
void cfoo2(int a[3]) { ... }
```

When calling `CFunc`, use `inout` with `VArray` variables:

```cangjie
var a: VArray<Int32, $3> = [1, 2, 3]
unsafe {
    cfoo1(inout a)
    cfoo2(inout a)
}
```

`VArray` cannot be used as a `CFunc` return type.

**As @C struct members:**

When used as `@C struct` members, `VArray` has the same memory layout as C structs, requiring identical declared lengths and types:

```c
struct S {
    int a[2];
    int b[0];
}
```

In Cangjie:

<!-- run -->

```cangjie
@C
struct S {
    var a = VArray<Int32, $2>(repeat: 0)
    var b = VArray<Int32, $0>(repeat: 0)
}
```

> **Note:**
>
> C allows flexible array members (arrays of unspecified length) as the last struct member. Cangjie doesn't support mapping structs containing flexible array members.

### Strings

For C strings, Cangjie provides the `CString` type with these member functions:

- `init(p: CPointer<UInt8>)`  Construct from `CPointer`
- `func getChars()`  Get string address as `CPointer<UInt8>`
- `func size(): Int64`  Get string length
- `func isEmpty(): Bool`  Check if empty (returns true for null pointers)
- `func isNotEmpty(): Bool`  Check if not empty (returns false for null pointers)
- `func isNull(): Bool`  Check for null pointer
- `func startsWith(str: CString): Bool`  Check prefix
- `func endsWith(str: CString): Bool`  Check suffix
- `func equals(rhs: CString): Bool`  Equality check
- `func equalsLower(rhs: CString): Bool`  Case-insensitive equality
- `func subCString(start: UInt64): CString`  Substring from start (new allocation)
- `func subCString(start: UInt64, len: UInt64): CString`  Substring with length (new allocation)
- `func compare(str: CString): Int32`  Equivalent to C's `strcmp(this, str)`
- `func toString(): String`  Convert to String
- `func asResource(): CStringResource`  Get resource representation

Convert `String` to `CString` using `LibC.mallocCString`, remembering to free the `CString` afterward.

Example:

<!-- run -->

```cangjie
foreign func strlen(s: CString): UIntNative

main() {
    var s1 = unsafe { LibC.mallocCString("hello") }
    var s2 = unsafe { LibC.mallocCString("world") }

    let t1: Int64 = s1.size()
    let t2: Bool = s2.isEmpty()
    let t3: Bool = s1.equals(s2)
    let t4: Bool = s1.startsWith(s2)
    let t5: Int32 = s1.compare(s2)

    let length = unsafe { strlen(s1) }

    unsafe {
        LibC.free(s1)
        LibC.free(s2)
    }
}
```

### sizeOf/alignOf

Cangjie provides `sizeOf` and `alignOf` functions to get memory size and alignment (in bytes) for C-interoperable types:

```cangjie
public func sizeOf<T>(): UIntNative where T <: CType
public func alignOf<T>(): UIntNative where T <: CType
```

Example:

<!-- run -->

```cangjie
@C
struct Data {
    var a: Int64 = 0
    var b: Float32 = 0.0
}

main() {
    println(sizeOf<Data>())
    println(alignOf<Data>())
}
```When running on a 64-bit machine, the output will be:

```text
16
8
```

## CType

In addition to the types provided in the type mapping section for interfacing with C-side types, Cangjie also offers a `CType` interface. This interface itself contains no methods and serves as a parent type for all C-interoperable types, facilitating use in generic constraints.

Important notes:

1. The `CType` interface is an interface type in Cangjie and does not itself satisfy the `CType` constraint;
2. The `CType` interface cannot be inherited or extended;
3. The `CType` interface does not bypass subtype usage restrictions.

Example usage of `CType`:

<!-- verify -->

```cangjie
func foo<T>(x: T): Unit where T <: CType {
    match (x) {
        case i32: Int32 => println(i32)
        case ptr: CPointer<Int8> => println(ptr.isNull())
        case f: CFunc<() -> Unit> => unsafe { f() }
        case _ => println("match failed")
    }
}

main() {
    var i32: Int32 = 1
    var ptr = CPointer<Int8>()
    var f: CFunc<() -> Unit> = { => println("Hello") }
    var f64 = 1.0
    foo(i32)
    foo(ptr)
    foo(f)
    foo(f64)
}
```

Execution results:

```text
1
true
Hello
match failed
```

## Calling Cangjie Functions from C

Cangjie provides the `CFunc` type to correspond with C-side function pointer types. C-side function pointers can be passed to Cangjie, and Cangjie can also construct variables corresponding to C function pointers to pass to the C side.

Assume a C library API as follows:

```c
typedef void (*callback)(int);
void set_callback(callback cb);
```

Correspondingly, in Cangjie this function can be declared as:

```cangjie
foreign func set_callback(cb: CFunc<(Int32) -> Unit>): Unit
```

Variables of type CFunc can be passed from the C side or constructed in Cangjie. There are two methods to construct CFunc types in Cangjie: one is using functions decorated with `@C`, and the other is closures marked as CFunc types.

Functions decorated with `@C` indicate that their function signatures comply with C calling conventions, while their definitions remain in Cangjie. Functions decorated with `foreign` have their definitions on the C side.

> **Note:**
>
> For both `foreign`-decorated functions and `@C`-decorated functions, it is not recommended to use `CJ_` (case-insensitive) as a prefix for naming these `CFunc` types, as this may conflict with standard library and runtime symbols internal to the compiler, leading to undefined behavior.

Example:

```cangjie
@C
func myCallback(s: Int32): Unit {
    println("handle ${s} in callback")
}

main() {
    // the argument is a function qualified by `@C`
    unsafe { set_callback(myCallback) }

    // the argument is a lambda with `CFunc` type
    let f: CFunc<(Int32) -> Unit> = { i => println("handle ${i} in callback") }
    unsafe { set_callback(f) }
}
```

Assuming the C function is compiled into a library named "libmyfunc.so", the compilation command `cjc -L. -lmyfunc test.cj -o test.out` should be used to link this library with the Cangjie compiler. This will ultimately generate the desired executable.

Additionally, when compiling C code, please enable the `-fstack-protector-all/-fstack-protector-strong` stack protection options. Cangjie code inherently includes overflow checks and stack protection. When incorporating C code, it is necessary to ensure the safety of overflows within unsafe blocks.

## Compilation Options

Using C interoperability typically requires manually linking C libraries. The Cangjie compiler provides corresponding compilation options.

- `--library-path <value>`, `-L <value>`, `-L<value>`: Specifies the directory containing the library files to be linked.

  The path specified by `--library-path <value>` will be added to the linker's library search path. Additionally, paths specified in the `LIBRARY_PATH` environment variable will also be included in the linker's library search paths, with paths specified via `--library-path` taking precedence over those in `LIBRARY_PATH`.

- `--library <value>`, `-l <value>`, `-l<value>`: Specifies the library file to be linked.

  The given library file will be passed directly to the linker. The library filename should follow the format `lib[arg].[extension]`.

For all compilation options supported by the Cangjie compiler, please refer to "Appendix > cjc Compilation Options".

## Example

This demonstrates how to use C interoperability and the `write/read` interfaces to assign and read values from a struct.

C code:

```c
// draw.c
#include<stdio.h>
#include<stdint.h>

typedef struct {
    int64_t x;
    int64_t y;
} Point;

typedef struct {
    float x;
    float y;
    float z;
} Cube;

void drawPicture(Point* point, Cube* cube) {
    point->x = 1;
    point->y = 2;
    printf("Draw Point finished.\n");

    printf("Before draw cube\n");
    printf("%f\n", cube->x);
    printf("%f\n", cube->y);
    printf("%f\n", cube->z);
    cube->x = 4.4;
    cube->y = 5.5;
    cube->z = 6.6;
    printf("Draw Cube finished.\n");
}
```

Cangjie code:

```cangjie
// main.cj
@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
}

@C
struct Cube {
    var x: Float32 = 0.0
    var y: Float32 = 0.0
    var z: Float32 = 0.0

    init(x: Float32, y: Float32, z: Float32) {
        this.x = x
        this.y = y
        this.z = z
    }
}

foreign func drawPicture(point: CPointer<Point>, cube: CPointer<Cube>): Int32

main() {
    let pPoint = unsafe { LibC.malloc<Point>() }
    let pCube = unsafe { LibC.malloc<Cube>() }

    var cube = Cube(1.1, 2.2, 3.3)
    unsafe {
        pCube.write(cube)
        drawPicture(pPoint, pCube)   // in which x, y will be changed

        println(pPoint.read().x)
        println(pPoint.read().y)
        println(pCube.read().x)
        println(pCube.read().y)
        println(pCube.read().z)

        LibC.free(pPoint)
        LibC.free(pCube)
    }
}
```

Compilation command for Cangjie code (using CJNative backend as an example):

```shell
cjc -L . -l draw ./main.cj
```

In the compilation command, `-L .` indicates that the linker should search the current directory for libraries (assuming `libdraw.so` exists in the current directory), and `-l draw` specifies the name of the library to link. Upon successful compilation, the default output is a binary file named `main`. The command to execute the binary is:

```shell
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main
```

Execution results:

```shell
Draw Point finished.
Before draw cube
1.100000
2.200000
3.300000
Draw Cube finished.
1
2
4.400000
5.500000
6.600000
```
