---
author: Huawei Technologies Co., Ltd.
title: Cangjie Multiplatform Programmer's Guide
subtitle: for Android™
titlepage: true
numbersections: true
toc-own-page: true
listings-no-page-break: true
textables: false
---

``` {=html}
<style>
body { max-width: unset; }
</style>
```
\newpage

# Introduction

The **Cangjie Multiplatform** technology enables Cangjie developers
to incorporate their code into new Android/iOS applications and/or gradually
replace the Java/Objective-C parts of existing applications with Cangjie code.
The central mechanism that enables the cross-language, cross-runtime
interoperability is _[mirror types](#mirror-types)_, which expose the types
of one language to the other.

On the Cangjie side, mirror types enable the inheritance of Java/Objective-C
classes with method overriding, as well as the implementation of Java
interfaces and Objective-C protocols, all while using conventional Cangjie
syntax. On the Java/Objective-C side, the mirror types that represent Cangjie
types are expressed in terms of the respective language's own types.
All in all, this enables seamless transitions between the Java/Objective-C
and Cangjie parts of the application, which includes usage of the target
O/S APIs in Cangjie code.


## The Challenge and the Solution

Java, Objective-C and Cangjie are object-oriented languages that support
inheritance and polymorphism. However, the differences in their semantics,
object models, and execution models preclude direct usage of Cangjie
objects in Java or Objective-C code and vice versa.

Then, all three languages have managed runtimes that support automatic memory
management, threading, exception handling and other low-level features,
but again they do that differently. Making two separately designed complex
language runtimes aware of each other might push the complexity of the entire
system beyond human comprehension.

Instead, the interoperability between Cangjie and Java is achieved
by disguising them both as low-level languages. Cangjie and Java parts
of the application see each other through the lens of the Java Native Interface
(JNI), originally designed to facilitate the development of Java `native`
methods in languages such as C and C++. JNI is a rich, but low-level API,
and writing `native` Java methods is known to be cumbersome. Fortunately,
CJMP automates away the complexity of JNI.

The Objective-C Runtime module API serves a similar role on iOS. It is also
designed specifically to enable the creation of bridge layers between
Objective-C and other languages. And just like with JNI, CJMP takes care
about the cumbersome parts.


# Key Concepts

## Mirror Types

Considering Cangjie and Java as a pair of interoperating languages,
a _mirror type_ _`T'`_ defined in one language of the pair is a type that
represents an existing type _`T`_ defined in the other language, enabling
the code written in the first language to use that type, possibly with some
limitations.

The Boolean types and numeric types that are essentially the same in both
languages naturally mirror each other: the Java mirror type for the Cangjie
type `Int32` is `int` and vice versa. Mirroring of numeric types that the
other language does not naturally support is not currently possible, so e.g.
the Cangjie type `Float16` cannot be mirrored to a Java primitive type.

For a user-defined type such as class, struct or interface, the mirror type
would be its closest equivalent in the other language. For instance, the only
Java type that can approximate a Cangjie struct or tuple type with reasonable
accuracy is a `final` Java class.

A mirror type exposes the members and constructors of the original user-defined
type that are accessible _and_ can be used in the other language, so again
a Cangjie member function that returns a value of type `UInt64` cannot be
mirrored to Java without some trickery.

Normally you would obtain mirror type definitions for a Java or Cangjie
type _and_ its required dependencies automatically. For Java types,
a standalone [mirror generator](#java-mirror-generator-reference)
is provided, whereas Java mirrors of Cangjie types are produced by the
[`cjc` compiler](#cangjie-mirror-generation-reference) as a byproduct
of the normal compilation process.


### Mirroring Java Types to Cangjie

The `cjc` compiler replaces any uses of Java mirror types with the appropriate
glue code, so only the names of types themselves and names and types of their
accessible members matter. Therefore, mirrors of Java types only contain member
declarations, not definitions: constructors and member functions/properties
have no bodies and member variables have no initializers.
For the same reason, `private` and package-private members are omitted.

For such an extension of the regular Cangjie syntax to work, each mirror type
must be marked with a `@JavaMirror` annotation. It helps the compiler
distinguish between mirror type declarations and normal Cangjie type
definitions.

For example, a mirror class for the following Java class:

```java
public class Node {
    public static final int A = 0xDeadBeef;
    private int id;
    public Node(int id) { this.id = id; }
    public int id() { return id; }
}
```

might look like this:

```cangjie
@JavaMirror
public open class Node {
    public static let A: Int32
    public init(id: Int32)
    public open func id(): Int32
}
```

A few foundational Java types, namely `java.lang.Object`, `java.lang.String`
and arrays, have [predefined mirrors](#interop-library-api-reference)
in the interoperability library.


### Mirroring Cangjie Types to Java Types

Unlike the mirrors of Java types, for which `cjc` has dedicated support,
mirrors of Cangjie types must look exactly like normal Java types
from the outside, for the Android toolchain to pick them up. The `cjc`
compiler therefore generates those mirrors in the form of Java source code
files containing glue code responsible for linking together the Java and
Cangjie worlds.

For instance, if the class `Node` from the example in the
[previous section](#mirroring-java-types-to-cangjie) was originally defined
in Cangjie as follows:

```cangjie
public class Node {
    private let _id: Int
    public prop id: Int {
        get() { _id }
    }
    public init(id: Int) { this._id = id }
}
```

the `cjc` compiler could generate the following Java mirror for it:

```java
public final class Node {
    /* Some glue code */
    public Node(long id) {
        /* Glue code constructing a Cangjie Node instance and associating
         * it with the Java Node instance being constructed, i.e. 'this'.
         */
    }
    public long getId() {
        /* Glue code invoking the Cangjie 'id' property getter of the
           associated Cangjie Node instance and returning the result.
         */
     }
    /* More glue code */
}
```



## Interop Classes

An _interop class_ is essentially a Cangjie class that is derived from one
or more [mirror types](#mirror-types) and is usable from Java. All its
constructors and non-inherited public member functions are exposed to Java
code via a conjugate _wrapper class_, automatically generated by the `cjc`
compiler. The wrapper class itself defines no other user-callable methods
or constructors, but any methods it may have inherited from its supertypes
may be called from both Java and Cangjie code.

For example, when compiling the following Java interop class:

```cangjie
@JavaImpl
public class BooleanNode <: Node {
    private let flag: Bool
    public init(id: Int32, flag: Bool) {
        super.init(id)
        this.flag = flag
    }
    public func getFlag(): Bool {
        flag
    }
}
```

the `cjc` compiler will also yield a Java source code file similar
to the following:

```java
public class BooleanNode extends Node {
    /* glue code */
    public BooleanNode(int id, boolean flag) {
        /* Glue code constructing a Java BooleanNode instance and associating
         * it with the Cangjie instance being constructed, i.e. 'this'.
         */
    }
    public boolean getFlag() {
        /* Glue code invoking the 'getFlag' member function of the associated
           Cangjie BooleanNode instance and returning the result.
         */
    }
    /* more glue code */
}
```


## Foreign Types

The [mirror types](#mirror-types) and [interop classes](interop-classes) are
not perfectly native to the language in which they are defined. Extending the
analogy, their status is more like temporary visitors and work visa holders
respectively, so they are collectively called _foreign types_ throughout
this document.


## Java-Compatible Types

The following Cangjie types are called _Java-compatible_:

* Value types that have direct equivalents among Java primitive types
  (`Int16` is included, but `UInt8` is not)
* [Foreign types](#foreign-types)
* Types of the form `Option<`_`T`_`>` where _`T`_ is a [foreign type](#foreign-types)
  (see _[`null` Handling](null-handling)_ for reasoning)

The special generic mirror type `JArray<T>` included in the
[interop library](#interop-library-api-reference)
represents Java arrays. Its type variable `T` must be a Java-compatible type.

For obvious reasons, the parameters and return values of public member functions
of a foreign type may only have types compatible with the respective language.

The member variables of an interop class may have any types. Their public member
variables that have Java-compatible types may be accessed from both Java and Cangjie.

```cangjie
@JavaImpl
class NamedNode <: Node {
    public var jName: JString  // resides in the conjugate wrapper class instance
    public var cjName: String  // resides in the interop class instance
    init(name: JString) {
        jName = name
        cjName = name.toCangjieString()
    }
}
```


## Interop Scenarios

There are essentially two Java-Cangjie interoperation scenarios:

* In one scenario,
  [Cangjie types and functions are exposed to Java](#cangjie-to-java-mapping),
  enabling the use of Cangjie APIs, libraries and application components
  in Java code.

* In the other scenario,
  [Java classes and interfaces are exposed to Cangjie](#java-to-cangjie-mapping),
  enabling Cangjie code to access Android APIs, third party Java libraries
  and components of the application that remain in Java.

The above scenarios are not mutually exclusive, one application may as well be
utilizing both. Also, class inheritance and interface implementation
are supported in both scenarios (a Java class may subclass a Cangjie class
and vice versa). That enables seamless callbacks, so neither scenario is
unidirectional. However, each scenario has its own feature set, limitations,
tooling, etc., so they are described separately.


# Using Cangjie in Java

To enable access to a Cangjie library, API, or some other piece of code
from Java, you need to generate Java [mirror types] for the Cangjie types
that you want to expose. The `cjc` compiler can do that for you as described
in [Cangjie Mirror Generation Reference](#cangjie-mirror-generation-reference).

**NOTE:** The type system of the Cangjie language is richer and more versatile
than its Java counterpart. There are also some principal differences in the
features shared by the two languages, most notably
[generics](#generic-cangjie-types-mirroring).
Expressing certain features of Cangjie in Java is therefore impossible, and
other features can be difficult to express in a natural and compact manner.
See [Cangjie to Java Mapping](#cangjie-to-java-mapping) for the exact list
of supported features and associated restrictions.

**Example:**

Suppose you want to expose to Java a Cangjie struct `Vector` defined
as follows:

```cangjie
package cj

public struct Vector {
    private var x: Int32 = 0
    private var y: Int32 = 0

    public init(x: Int32, y: Int32) {
        this.x = x
        this.y = y
    }

    public func add(v: Vector): Vector {
        Vector(x + v.x, y + v.y)
    }
}
```

When compiling `Vector.cj`, you would invoke the `cjc` compiler with two
additional options: `--experimental --enable-interop-cjmapping=Java`.
The compiler would then generate an extra file, `Vector.java`, similar
to the following:

```java
package cj;

public final class Vector {
    // glue code

    public Vector(int x, int y) { /* glue code */ }

    public Vector add(v: Vector) { /* glue code */ }

    // more glue code
}
```

Now you can add `Vector.java` to your Android project under `src/main`
and use the class `Vector` in your Java code as if it was a normal Java class:
define variables of that type, create instances, pass them around, including
to Cangjie code such as the method `Vector.add`, apply type comparison and
type conversion operators, etc.


## Limiting the Exposure

The option `--enable-interop-cjmapping` instructs the `cjc` compiler
to generate mirror types for _all_ `public` Cangjie types that it compiles,
and expose _all_ `public` member functions and constructors of those types.
Oftentimes, however, such total exposure is undesirable, as what you want
to use in Java may be just a small percentage of the functionality provided
by a Cangjie library or framework.

You may precisely control the exposure of Cangjie types and their members
by passing the pathname of a dedicated configuration file to `cjc` via the
option `--import-interop-cj-package-config-path`. That file is a plain
text file the contents of which must conform to the [TOML](https://toml.io)
syntax.

In the `[default]` section of that file, you can specify the default API
exposure strategy for all Cangjie packages, and then modify it
for particular packages in the respective `[[package]]` entries. For example:

```toml
[default]
APIStrategy="None"       # Expose nothing by default

[[packages]]
name="com.example.pkg1"  # From this specific package,
APIStrategy="Full"       # expose everything
   .  .  .
```

Furthermore, for each package you can use either the `included_apis`
or `excluded_apis` property to respectivly expose or hide particular types
and/or members:

```toml
   .  .  .
[[packages]]
name="com.example.pkg2"          # From this specific package,
included_apis = [ "Vector",      # Only the type 'Vector'
                  "Vector.add"   # and its member function 'add'
                ]                # are exposed

[[packages]]
name="com.example.pkg3"          # From this specific package,
APIStrategy="Full"               # everything
excluded_apis = [ "TopSecret",   # but the type 'TopSecret' and
                  "Auth.getPwd"  # member function 'Auth.getPwd'
                ]                # are exposed
```

Refer
to [Cangjie Mirror Generation Reference](#cangjie-mirror-generation-reference)
for more details.


## Generic Cangjie Types Mirroring

Many important Cangjie types are parameterized. Unfortunately, certain
fundamental differences between Cangjie and Java generics preclude mirroring
of the former into the latter. As a workaround, the Cangjie SDK supports
_monomorphization_ of mirror types: it generates a separate _non-generic_
Java mirror type for each supplied set of valid type arguments for the given
parameterized Cangjie type.

For instance, if you have a generic Cangjie class `p.Pair<T,U>`:

```cangjie
package p
public class Pair<T,U> { . . . }
```

and want to manipulate instances of `Pair<Int, String>` and `Pair<Foo, Bar>`
in your Java code, you would add a `generic_object_configuration` property
to the `[[package]]` entry for `p` in the configuration file, with the
following content:

```toml
   .  .  .
[[package]]
name = "p"
generic_object_configuration  = [
    { name = "Pair",
      type_arguments = [
          "Int, String",
          "Foo, Bar"
      ] },
       .  .  .
```

`cjc` would then generate two separate Java classes:

```java
public final class G_Int_String { . . . }

public final class G_Foo_Bar { . . . }
```

representing those particular _instantiations_ of the type `Pair<T,U>`.

Refer to [Generics Instantiations](#cangjie-mirror-generation-reference)
for more details.


# Cangjie to Java Mapping

The current version of the `cjc` compiler uses Cangjie → Java mapping
described in this chapter. See
[Cangjie Mirror Generation Reference](#cangjie-mirror-generation-reference)
for applicable `cjc` command-line options.


## General Considerations {#cangjie-general-considerations}

The Cangjie type system is much more versatile than that of the Java language.
Many Cangjie types and their features do not have direct or even reasonably
close equivalents in Java, so some Cangjie types have limited support in the
current version and some are not supported at all.

Consequently, if the type of a public member, function/constructor parameter,
or function return type is not supported, the respective member, function
or constructor cannot be mirrored. The compiler reports such usages as errors.
However, if such a type is used in an unsupported _context_, e.g. as the
type of a public member variable, the respective entity is simply not mirrored
and no error is reported.


## Names {#cangjie-names}

The original names of Cangjie packages, functions, types and type members
are currently preserved, which means that some of them may clash
with Java keywords, such as "`int`" or `final`, or contain characters that
are not permitted in Java names.


## Boolean and Numeric Types

Cangjie Boolean and numeric types that have equivalents among Java primitive
types are mirrored to those respective primitive types; those that don't
are not supported, as well as the types `IntNative` and `UIntNative`:

Cangjie Type   Java Type
-------------  ----------------
`Bool`         `boolean`
`Int8`         `byte`
`Int16`        `short`
`Int32`        `int`
`Int64`        `long`
`IntNative`    Not supported
`UInt8`        Not supported
`UInt16`       `char`
`UInt32`       Not supported
`UInt64`       Not supported
`UIntNative`   Not supported
`Float16`      Not supported
`Float32`      `float`
`Float64`      `double`

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Rune

The type `Rune` is not supported.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## String

The type `String` is not supported yet.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Array

Array types (`Array<T>` instantiations) are not supported yet.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Tuple

Tuple types are not supported yet.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Range

Range types are not supported yet.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Special Types

The type `Unit` is only supported as a function return type, mapped
to Java `void`.

The type `Nothing` cannot be supported.

The type `Any` is not supported yet.

See [General Considerations](#cangjie-general-considerations)
for information about the handling of unsupported types.


## Struct Types

Public Cangjie struct type definitions are mirrored into `final` Java class
definitions. Those definitions are generated automatically by the `cjc`
compiler and contain glue code that transfers control and data between
Java and Cangjie. They should not be modified manually.

```cangjie
package cj

import interoplib.interop.*

public struct Vector {
    private var x: Int32 = 0
    private var y: Int32 = 0

    public init(x: Int32, y: Int32) {
        this.x = x
        this.y = y
    }

    public func add(v: Vector): Vector {
       let res = Vector(x + v.x, y + v.y)
       print("cj: (${x}, ${y}) + (${v.x}, ${v.y}) = (${res.x}, ${res.y})\n", flush: true)
       return res
    }

    public static func dump(v: Vector): Unit {
        print("cj: Hello from static func in cj.Vector (${v.x}, ${v.y})\n", flush: true)
    }
}
```

```java
package cj;

// Glue code imports

final public class Vector {
    // Glue code

    public Vector(int x, int y) {
        // Glue code that constructs an instance of the Cangjie Vector struct
        // and associates it with the Java object 'this'
    }

    public Vector add(v: Vector) {
        // Glue code that retrieves the associated Cangjie Vector struct
        // instances associated with `this` and `v`, calls the add() instance
        // member function of the Cangjie-this, passing the Cangjie-v to it
        // as a parameter, and, finally, creates a new Java Vector instance
        // and associates it with the result of the add() call.
    }

    public static void dump(v: Vector) {
        // Glue code that calls the dump() static member function of the
        // Cangjie struct Vector, passing to it the instance associated
        // with 'v'/
    }

    // More glue code
}
```

Only public struct members and common constructors are mirrored.

**Member functions** are mirrored into methods with the respective mirror
types substituted for parameter types and return value type. Mirrors of
member functions returning `Unit` are mirrored into `void` methods.
The modifiers `public` and `static` are preserved. Methods that mirror
non-`open` member functions are modified with `final`.

**Common constructors** are mirrored into constructors with the respective
mirror types substituted for parameter types. _This includes the default
constructor that might have been implicitly declared._ The modifier `public`
is preserved.


The current version imposes a number of severe limitations on the struct
types that can be mirrored, to the extent that it may be fair to say
that a struct type needs to be designed specifically for exposing it
to Cangjie:

* Member variables are not mirrored and no means for accessing them
  is provided. This limitation will be removed in a future version.
  In the meantime, you may add getter functions as a workaround.

* Mirroring of `mut` instance member functions is a work in progress.
  They are mirrored, but incorrect glue code is generated in some
  circumstances.

* Mirroring of structs that implement interfaces other than `Any`
  is not supported. An attempt to mirror a struct that explicitly
  implements an interface results in a compile-time error.

* Mirroring of generic structs is supported through monomorphization.
  See [Generics](#cangjie-generics) for details.

* Mirroring of structs that contain public member properties,
  member operator functions, or primary constructors is not supported.
  An attempt to mirror a struct containing an entity of one or those
  kinds results in a compile-time error.

* An attempt to mirror a struct member function or constructor with an
  unsupported parameter type, or a member function with an unsupported
  return type, results in a compile-time error.


## Classes and Interfaces {#cangjie-classes-and-interfaces}

Cangjie class and interface definitions are mirrored respectively into Java
class and interface definitions. Those definitions contain automatically
generated glue code and should not be altered in any way.

```cangjie
package cj

import interoplib.interop.*

public interface Valuable {
    public func value(): Int
}

public open class Singleton <: Valuable {
    private let _v: Int
    public init (v: Int) { _v = v }
    public func value(): Int { _v }
}

public class Zero <: Singleton {
    public init() { super(0) }
}
```

```java
// Valuable.java
package cj;

// Glue code imports

public interface Valuable {
    public long value();
}

// Glue code
```

```java
// Singleton.java
package cj;

// Glue code imports

public class Singleton implements Valuable {
    // Glue code

    public Singleton(long v) {
        // Glue code that constructs an instance of the Cangjie Singleton class
        // and associates it with the Java object 'this'
    }

    public long value() {
        // Glue code that retieves the associated Cangjie Singleton class
        // instance, calls its memeber function value() and returns the result
    }

    // Glue code
}
```

```java
package cj;

// Glue code imports

public class Zero extends Singleton {
    // Glue code

    public Zero() {
        // Glue code that constructs an instance of the Cangjie Zero class
        // and associates it with the Java object 'this'
    }

    // Glue code
}
```

Identifiers that serve as names of mirrored types and their members are
currently preserved even if they clash with Java keywords such as `byte`.


From the outside, the mirror types are normal Java classes and interfaces
in all aspects: except for `final` classes, they can be extended/implemented,
their methods can be overloaded with conventional Java methods in subtypes,
their non-`final` methods can be overridden, types of their instances can
be compared with `instanceof`, and so on.

**Member functions** are mirrored into methods with the respective mirror
types substituted for parameter types and return value type. Mirrors of
member functions returning `Unit` are mirrored into `void` methods.
The modifiers `public` and `static` are preserved. Methods that mirror
non-`open` member functions are modified with `final`.

**Common constructors** are mirrored into constructors with the respective
mirror types substituted for parameter types. _This includes the default
constructor that might have been implicitly declared._ The modifier `public`
is preserved.

Only `public` members and constructors are mirrored. Static initializers
are not mirrored.


As Cangjie does not support type nesting, unlike Java, mirror types never
have nested types (except maybe for `private` member types used by glue code).

The current version imposes a number of severe limitations on the class
and interface types that can be mirrored, to the extent that it may be
fair to say that such types need to be designed specifically for exposing
them to Cangjie:

* Member variables are not mirrored and no means for accessing them
  is provided. This limitation will be removed in a future version.
  In the meantime, you may add getter/setter functions to Cangjie
  classes manually as a workaround.

* Mirroring of generic classes is supported through monomorphization.
  See [Generics](#cangjie-generics) for details.

* Mirroring of classes/interfaces that contain public member properties,
  member operator functions, or primary constructors is not supported.
  An attempt to mirror a class or interface containing an entity
  of one or those kinds results in a compile-time error.

* An attempt to mirror a class member function or constructor with an
  unsupported parameter type, or a member function with an unsupported
  return type, results in a compile-time error.

* Abstract class definitions are mirrored, but abstract classes are
  not supported as parameter and return value types.


## Enums

A Cangjie enum is mirrored into a `final` Java class without a `public`
constructor.

```cangjie
public enum TimeUnit {
    | Year(Int64)
    | Month(Int64)
    | Year
    | Month
}
```

```java
public class TimeUnit {
    /* Glue code */

    public static TimeUnit Year(long p1) {
         // Glue code creating a Cangjie Year(p1) enum and associating it
         // with a newly creasted Java TimeUnit instance
    }

    public static TimeUnit Month(long p1) {
         // Glue code creating a Cangjie Month(p1) enum and associating it
         // with a newly creasted Java TimeUnit instance
    }

    public static TimeUnit Year =
        // Glue code creating a Cangjie Year enum and associating it
        // with a newly creasted Java TimeUnit instance

    public static TimeUnit Month =
        // Glue code creating a Cangjie Year enum and associating it
        // with a newly creasted Java TimeUnit instance

    /* More glue code */
}
```

**Enum constructors without parameters** are mirrored into `static`
variables inhitalized with instances of the class associated with
the respective constructors of the Cangjie enum.


**Enum constructors with parameters** are mirrored into `static` factory
methods with the same names and matching types and numbers of parameters;
names of parameters are synthesized (`p1`, `p2`, ...).

**Member functions** are mirrored into methods with the respective mirror
types substituted for parameter types and return value type. Mirrors of
member functions returning `Unit` are mirrored into `void` methods.
The modifiers `public` and `static` are preserved.

The current version imposes a number of limitations on the enum that can be
mirrored:

* Mirroring of enums that implement interfaces other than `Any`
  is not supported. An attempt to mirror an enum that explicitly
  implements an interface results in a compile-time error.

* Mirroring of generic enums is supported through monomorphization.
  See [Generics](#cangjie-generics) for details.

* Mirroring of enums that contain public member properties or member
  operator functions is not supported. An attempt to mirror an enum
  containing such an entity results in a compile-time error.

* An attempt to mirror anenum member function or constructor with an
  unsupported parameter type, or a member function with an unsupported
  return type, results in a compile-time error.

Enum extension (via `extend`) is not supported. The extension is not mirrored.

Recursively defined enums are supported:

```cangjie
public enum Peano {
    | Z
    | S(Peano)

    public func toInt(): Int {
        match (this) {
            case Z => 0
            case S(x) => 1 + x.toInt()
        }
    }
}
```


## Generics {#cangjie-generics}

Java and Cangjie generics are fundamentally different, so the latter
cannot be mirrored into the former. However, _specific instantiations_
of parameterized Cangjie types, such as `G<Int64>`, are concrete types,
and therefore can be mirrored into non-generic Java types.
Such types are also called _monomorphized generics_.

Use the respective
[configuration file](#cangjie-mirror-generation-configuration)
of the `cjc` compiler to specify which instantiations of which types
to mirror. Refer to [Generics Instantiations](#generics-instantiations)
for details.

**Example:**

When compiling the following Cangjie class definition:

```cangjie
public class G<T> {
    private let t: T
    public init(t: T) { this.t = t }
    public func get(): T { t }
}
```

with the following lines in the respective section of the configuration
file:

```toml
       .  .  .
    generic_object_configuration  = [
        { name = "G", type_arguments = ["Bool", "Int"] },
    ]
       .  .  .
```

the compiler will generate Java mirror classes for `G<Bool>` and `G<Int>`,
named respectively `G_Bool` and `G_Int`.


Refer to the
[Cangjie Mirror Generation Reference](#cangjie-mirror-generation-reference)
section for complete instructions.




## `null` Handling {#cangjie-null-handling}

As Cangjie has no null type, passing `null` as a parameter to a mirrored
Cangjie method results in a run-time exception in glue code:

```cangjie
public class Node {
    private let next: ?Node
    public init() {
        next = None
    }
    public init(next: Node) {      /* Pure Cangjie */
        this.next = Some(next)
    }
}
```

```java
public final class Node {
    Node() { /* glue code */ }
    Node(Node next) { /* glue code */ }
}
   .  .  .
     Node list = new Node(null);   /* NullPointerException */
```

Conversely, there is currently no way to return `null` from a `public` member
function of a Java-compatible type.

**NOTICE:** The current version supports automatic `Option<T>` (un)wrapping
with `null` mapped to `None`, but only for Java reference types mirrored
to Cangjie, not the other way round. See [`null` Handling](#java-null-handling)
for details.



# Cangjie Mirror Generation Reference

There is no standalone mirror generator facilitating the exposure of Cangjie
types to Java and Objective-C code in the Cangjie SDK. The `cjc` compiler
itself is capable of generating Java/Objective-C mirror type definitions
for Cangjie types right when it compiles the Cangjie source code of those
types.


## Command-line Syntax {#cjc-command-line-syntax}

The following additional `cjc` options enable and control the generation
of mirrors for Cangjie types during compilation:

`--experimental`    _(mandatory)_

This option must be specified as of the current version, since the whole
interop feature is still in development, but will not be necessary
in the future.

`--enable-interop-cjmapping=Java` _or_  
`--enable-interop-cjmapping=ObjC`        _(mandatory)_

Enables the generation of mirror type definitions for Cangjie types
respectively in the form of Java or Objective-C source code files.

`--output-interop-cjmapping-dir` _`pathname`_     _(optional)_

The _`pathname`_ must point to a directory into which the `cjc`
compiler shall place its output Java or Objective-C source code files
containing mirror type definitions. If _`pathname`_ does not point to
an existing file system location, `cjc` attempts to create a directory there.
If _`pathname`_ points to something other than a directory, `cjc`
terminates with an error message.

The default value of _`pathname`_ is either `./java_gen` or `./objc_gen`,
depending on whether `--enable-interop-cjmapping` is set respectively
to "`Java`" or "`ObjC`".

`--import-interop-cj-package-config-path` _`pathname`_     _(optional)_

The _`pathname`_ must point to a configuration file that defines which
Cangjie types are exposed to Java or Objective-C as mirror types. See
[Cangjie Mirror Generation Configuration](#cangjie-mirror-generation-configuration)
for details.


## Cangjie Mirror Generation Configuration

A Cangjie mirror generation configuration file is a plain text file
in the [TOML](https://toml.io) syntax. It specifies:

  * Non-generic Cangjie types to mirror
  * Specific instances of generic Cangjie types to mirror


### Defaults

The `[default]` table defines the default settings for packages for which
either no [package-specific settings](#packages) are provided at all, or those
settings don't override the defaults.

**Properties:**

`APIStrategy`    _(optional)_

A string defining whether all public entities shall be mirrored by default
or not. Valid values:

* `"Full"` - all public entities shall be mirrored by default
* `"None"` - no public entities shall be mirrored by default

`GenericTypeStrategy`    _(optional)_

A string defining whether generic public entities shall be mirrored
by default or not. Valid values:

* `"Partial"` - instantiations explicitly listed in
  [`generic_object_configuration`](#generics-instantiations) shall be mirrored
* `"None"` - no generic public entities shall be mirrored by default


### Packages

Each entry in the `[[packages]]` array specifies the name of a separate
source Cangjie package, and, optionally:

* A filter that defines which types from that package to include in,
  or exclude from, the set of mirrors
* API mirroring strategy (if other than the [default](#defaults))
* Generic type mirroring strategy (if other than the [default](#defaults))
* Specific generic type instantiations to mirror

**Properties:**

`name`    _(mandatory)_

A string containing the name of the _source_ Cangjie package to which
the settings in this `[[packages]]` array entry apply.

Example:

```toml
name = "com.example.VectorMath"
```

`APIStrategy`    _(optional)_

A string defining whether all public entities of the given package shall
be mirrored by default or not. Valid values:

* `"Full"` - all public entities shall be mirrored by default
* `"None"` - no public entities shall be mirrored by default

If this property is absent, the [default](#defaults) value is used.

`included_apis`    _(optional)_

An array of strings each containing the name of a public entity that
needs to be mirrored. If the array contains the qualified name of a type
member, the type itself is also mirrored. Either `included_apis` or
`excluded_apis` may be present in a given `[[packages]]` array entry,
but not both.

Example:

```toml
included_apis = [
   "Vector.product", // Vector also exposed
   "HiddenV"
]
```

`excluded_apis`    _(optional)_

An array of strings each containing the name of a public Cangjie entity
defined in the given package that has to be _not_ mirrored.
Either `included_apis` or `excluded_apis` may be present in a given
`[[packages]]` array entry, but not both.


Example:

```toml
excluded_apis = [
   "Vector.product", // Even if Vector is exposed, product is not
   "HiddenV"
]
```

`GenericTypeStrategy`    _(optional)_

A string defining whether generic public entities defined in this package
shall be mirrored by default or not. Valid values:

* `"Partial"` - instantiations explicitly listed in
  [`generic_object_configuration`](#generics-instantiations) shall be mirrored
* `"None"` - no generic public entities shall be mirrored by default

If this property is absent, the [default](#defaults) value is used.


`generic_object_configuration`    _(optional)_

A list of tables defining the specific instantiations of generic entities
to be mirrored. See [Generics Instantiations](#generics-instantiations)
for details.


#### Generics Instantiations

The `generic_object_configuration` property of a `[[packages]]` array
entry defines which specific instantiations of generic Cangjie entities
will be mirrored.

The value of the property is a (possibly empty) array of tables.
Each entry of the array has the following two mandatory properties:

`name`

A string containing the name of a public generic Cangjie type or global
function defined in the current package.

`types`

An array of strings, each containing valid type arguments for the generic
type or global function the name of which is specified in the `name` property.

> Simply put, "valid" means that the type/function can be instantiated
> with the given string between the angle brackets `< >`.
>
> Consider the following Cangjie class:
>
> ```cangjie
> public class G<T> {
>     public func f(t: T): Unit {}
>     public func f(b: Bool): Unit {}
> }
> ```
>
> `G<Bool>` cannot be instantiated, so
>
> ```toml
> generic_object_configuration  = [
>     { name = "G", types = ["Bool"] }
> ]
> ```
> would trigger a compiler error.

**Example:**

Given the following Cangjie definitions

```cangjie
public class G<T> { . . . }
public func f<T>(): Unit { . . . }
public struct S<T,U> { . . . }
```

the property

```toml
generic_object_configuration  = [
    { name = "G", type_arguments = ["Int"] },
    { name = "f", type_arguments = ["Int", "Bool"] },
    { name = "S", type_arguments = ["Int, Bool"] }
]
```

instructs the `cjc` compiler to generate mirrors for the following
instantiations:

```cangjie
    G<Int>
    f<Int>
    f<Bool>
    S<Int, Bool>
```

and name them like `G_Int`, `f_Int`, and so on. 




# Using Java in Cangjie

In the first interoperation scenario, described
in [Using Cangjie in Java](#using-cangjie-in-java), Cangjie types are mapped
to Java types that behave just like any conventional Java classes
and interfaces: non-`final` classes can be extended, interfaces implemented,
instances created and passed around freely, and so on.

In contrast, due to certain technical limitations imposed by the Android
Runtime (JVM), any uses of Java types in Cangjie must be fully confined
to the code of constructors and member functions
of [interop classes](#interop-classes).
Also, mirror type declarations for Java classes and interfaces are
generated by a [standalone tool](#java-mirror-generator-reference),
not the `cjc` compiler.

The process of enabling this second scenario is therefore more involved. Here
are the steps you need to take:

1. Design the interoperability layer in terms of _Java_ classes and methods.

   developer → `interop layer design` (Java _pseudo-code_)

2. Generate mirror declarations for any existing Java classes and interfaces
   used in the design of the interoperability layer.

   `.class` → mirror generator → `.cj` (mirrors)

3. Write the classes constituting the interoperability layer _in Cangjie_.
   Use the mirrored Java types as needed: create instances, call methods, etc.

   `interop layer design` + `.cj` (mirrors) → developer → `.cj` (interop layer)

4. Compile the interop classes and mirror type declarations together with `cjc`.
   `cjc` will generate:

   * the necessary glue code for all uses of the mirror types.
   * the actual Java source for the Java part of the interoperability layer.

   `.cj` (mirrors + interop layer) → `cjc`  → `.so` + `.java` (interop layer)

5. Add to your Android project:

    * `.java` files generated by `cjc`
    * `.so` file generated by `cjc`
    * runtime libraries (`.so` and `.jar`) from the Cangjie SDK

    then insert the necessary uses of the interop layer in the Java source
    and rebuild the project.

    Android project + `.java`, `.jar`, `.so` → Android toolchain → `.apk`

The sections
[Initial Interop Class Creation Workflow](#initial-interop-class-creation-workflow)
and [Calling Java From Cangjie](#calling-java-from-cangjie)
describe the above process in detail with an end-to-end example.


## Initial Interop Class Creation Workflow

### Step 1: Design the interoperability layer

On this step, you design the API of one or more interop classes
_from the Java code perspective_, i.e. you need to decide, for each interop
class:

* To which Java package it will belong;
* What Java class it will extend, if not the default `java.lang.Object`;
* Which Java interface(s) it will implement, if any; and
* What `public`/`protected` methods and/or constructors it will have.
  You only need to know the types of parameters and, for methods, their names
  and return value types; the implementations you will write in Cangjie.

See also
[Features and Limitations of Interop Classes](#features-and-limitations-of-interop-classes).

**Example:**

Suppose we want to pass control from Java to Cangjie by invoking a certain
`static` method `m()` accepting parameters of types `com.example.a.A`,
`java.lang.String`, and `int`, and returning a value of type `com.example.b.B`.
We want that method to belong to a class called `Interop` that extends `Object`
and belongs to the package `cjworld`.

In other words, we have determined that the Java source code file that we
want to be generated on step 4 should have the following content:

```java
package cjworld

import com.example.a.A;
import com.example.b.B;

public class Interop {
    /* glue code */
    public static B m(A a, String s, int i) {
        /* glue code invoking the Cangjie implementation of m() */
    }
    /* more glue code */
}
```


### Step 2: Generate mirror type declarations

Now, you need [mirror type](#mirror-types) declarations for all Java reference
types on which your interop classes depend: their supertypes, types of their
method and constructor parameters, etc., and, possibly, the dependencies of
those types.

**NOTE:** Mirror classes for `java.lang.Object` and `java.lang.String` are
provided in the introp library, as well as a generic mirror class representing
Java arrays. Skip this step if the methods and constructors of your interop
classes only pass to/receive from Cangjie values of primitive Java types,
`java.lang.Object`, `java.lang.String`, and/or arrays of the foregoing.

Use the [Java mirror generator](#java-mirror-generator-reference) included
in the Cangjie SDK to produce those mirror type declarations as follows:

**Command line:**

```bash
java-mirror-gen \
    --package-name <package-name> \
    --class-path <full-application-classpath> \
    --destination <output-directory> \
    <names-of-mirrored-types>
```

or

```bash
/path/to/jdk/21/bin/java \
java-mirror-gen \
    --package-name <package-name> \
    --class-path <full-application-classpath> \
    --destination <output-directory> \
    -jar <jar-file>
```

where

* `<package-name>` is the desired name of the Cangjie package for all
  mirrored types.

* `<full-application-classpath>` is the complete classpath of the application
  that is used during its build, including `android.jar`.

* `<output directory>` is the pathname of the directory where the Cangjie source
  files containing mirror type declarations will be placed, such as `./src/cj`.

* `<names-of-mirrored-types>` are the _fully qualified names_ of the Java
  reference types on which your interop class design depends,
  other than `java.lang.Object`, `java.lang.String` or arrays.

* `<jar-file>` is the pathname of a single jar file. All `public` classes and
  interfaces, the `.class` files of which it contains, are mirrored, along
  with any dependencies found along the `<full-application-classpath>`.

**Example:**

Continuing the above example, we notice that our class `cjworld.Interop` depends
on:

* `java.lang.Object` as a superclass;
* `com.example.a.A`, `java.lang.String`, and `int` as parameter types; and
* `com.example.b.B` as a return value.

We do not need to mirror primitive types such as `int`, and the classes
`java.lang.Object` and `java.lang.String` are pre-mirrored. This leaves us
with just the two `com.example` classes to mirror. Suppose we want them
to appear in the package `javaworld`.

Mirror generator command line with a fictional application classpath:

```bash
java-mirror-gen \
    --package-name javaworld \
    --class-path /home/user/Android/Sdk/platforms/android-35/android.jar:App.jar \
    --destination ./src/cj \
    com.example.a.A com.example.b.B
```

This will generate files `src/cj/javaworld/src/A.cj` and `src/cj/javaworld/src/B.cj`,
_plus_ mirror type declarations for any dependencies those two Java types may have.


### Step 3: Write Interop Classes

For each Java class skeleton you designed on step 1, write a new Cangjie class
as follows:

1. Use the appropriate package and class names (the Java wrapper class will
   have the same fully qualified name).
2. Import `java.lang.*`.
3. Import the necessary mirror types, if you generated any on Step 2. Do not
   import the dependencies for now.
4. Annotate the class with `@JavaImpl`.
5. Make the class inherit the mirror of the desired Java class (by default,
   it will inherit the built-in mirror of `java.lang.Object`).
6. Use `JObject`, `JString` and `JArray<T>` in place of `java.lang.Object`,
   `java.lang.String` and Java array types respectively.

Type mapping (`T'` is either the matching primitive type or the respective mirror type):

Java Type (`T`)   Cangjie Type (`T'`)
----------------  -----------------------------
`boolean`         `Bool`
`byte`            `Int8`
`short`           `Int16`
`char`            `UInt16`
`int`             `Int32`
`long`            `Int64`
`float`           `Float32`
`double`          `Float64`
`Object`          `JObject` or `?JObject`
`String`          `JString` or `?JString`
`class C`         `C'` or `?C'`
`interface I`     `I'` or `?I'`
`T[]`             `JArray<T'>` or `?JArray<T'>`

Use `?<T'>` (`Option<T'>`) types for parameters, return values, and local variables
of mirror and interop types that may receive/hold Java `null`.

Use `Unit` as a return type to represent a `void` Java method.

See also
[Features and Limitations of Interop Classes](#features-and-limitations-of-interop-classes).

**Example:**

To continue the above example, the interop class for the function `m()` would look
like this:

```cangjie
package cjworld

import java.lang.*
import javaworld.*

@JavaImpl
public class Interop {
    public static func m(a: ?A, s: ?JString, i: Int32): ?B {
        /* Just a dummy implementation for now */
        B()    // Assuming that B has an accessible parameterless constructor
    }
}
```

If you don't need `m()` to ever return `null` to its Java caller, remove
`?` from its return value type.


### Step 4: Compile the Interop Class

Command line:

```bash
cjc --output-type=dylib \
    -p <source-directory> \
    -ljava.lang -linteroplib.interop \
    --output-javagen-dir=<java-output-directory>
```

where

`<source-directory>` is the pathname of the directory containing the source code of
interop classes and mirror type declarations.

`<java-output-directory>` is the pathname of the directory to which the generated
Java source files are placed.

The output is a `.so` file with compiled Cangjie code for the interop classes
and Java source files (`.java`) for their Java wrappers.

**Example:**

```bash
cjc --output-type=dylib \
    -p src/cj \
    -ljava.lang -linteroplib.interop \
    --output-javagen-dir=src/java
```

The compiler will produce two files: `libcjworld.so` and `src/java/cjworld/Interop.java`.


### Step 5: Put it all together

1. Add the following files to your Android project:

    * The Java source files generated on the previous step - to the source tree
      under `src/main` in accordance with the package names.

    * The `.so` file generated on the previous step - to `src/main/jniLibs/arm64-v8a`
      (create those subdirectories if they don't exist).

    * All `.so` files from the appropriate subdirectory of `$CANGJIE_HOME/runtime/lib/`,
      such as `$CANGJIE_HOME/runtime/lib/linux_android31_aarch64_cjnative/` - also
      to `src/main/jniLibs/arm64-v8a`.

    * The file `libc++_shared.so` from the Android NDK - also
      to `src/main/jniLibs/arm64-v8a`.
      (That file is located
      in `toolchains/llvm/prebuilt/`_`host`_`/sysroot/usr/lib/aarch64-linux-android/`
      under the Android NDK root, where _`host`_ is a string corresponding
      to the O/S and hardware of the system on which you conduct the build,
      such as "`linux-x86_64`".

    * The file `$CANGJIE_HOME/lib/library-loader.jar` as a dependency.

2. **IMPORTANT: Enforce the legacy convention of compressing all `.so` files
   in the APK, or the application will crash trying to load Cangjie libraries.**

   In the Gradle build script of your Android application, usually called
   `build.gradle.kts`, locate the `android {}` block and insert the following
   option setting into it, if it is not already present:

   ```gradle
      .  .  .
   android {
          .  .  .
       packaging {
           jniLibs {
               useLegacyPackaging = true
           }
       }
   }
      .  .  .
   ```

3. Re-build the project to ensure everything is correct so far. You may
   also try deploying it.

4. Add the Java code working with interop classes and re-build your Android
   project again.

**Example:**

Now we can add an invocation of `Interop.m()` to our Java code, for control
to be passed to its Cangjie implementation in our interop class:

```java
       .  .  .
    B b = Interop.m(new A(), "Test", 0);
       .  .  .
```


## Calling Java from Cangjie

Once you have designed, built and integrated the interoperability layer
as described
in the [previous section](#initial-interop-class-creation-workflow),
you can add code that uses Java types to the member functions of
your interop classes. The type mapping is the same:

Cangjie Type (`T'`)            Java Type (`T`)  Remark
-----------------------------  ---------------  ------
`Bool`                         `boolean`
`Int8`                         `byte`
`Int16`                        `short`
`UInt16`                       `char`
`Int32`                        `int`
`Int64`                        `long`
`Float32`                      `float`
`Float64`                      `double`
`JObject` or `?JObject`        `Object`
`JString` or `?JString`        `String`
`T'` or `?T'`                  `T`              (\*)
`JArray<T'>` or `?JArray<T'>`  `T[]`            (\*\*)

**(\*)** `T'` must be either a mirror type for the Java type `T`
or an interop class, for which the source code of its Java wrapper
class `T` was generated automatically by `cjc`.

**(\*\*)** `T'` must be either a mirror type, an interop class,
or one of the value types listed above, e.g. `Int32`.

Use `Unit` as a return type to call a `void` Java method.

**Limitations:**

* Variable arity (varargs) methods and constructors are not supported.


### Step 0: Build your Android application normally

### Step 1: Generate mirror type declarations

Skip this step if you only want to call member functions of interop classes,
their superclasses and/or types for which you have already generated mirror
declarations, such as the types of interop class parameters or return values.

**Command line:**

```bash
java-mirror-gen \
    --package-name <package-name> \
    --class-path <full-application-classpath> \
    --destination <output-directory> \
    <names-of-mirrored-types>
```

or

```bash
/path/to/jdk/21/bin/java \
java-mirror-gen \
    --package-name <package-name> \
    --class-path <full-application-classpath> \
    --destination <output-directory> \
    -jar <jar-file>
```

where

* `<package-name>` is the desired name of the Cangjie package for all
  mirrored types.

* `<full-application-classpath>` is the complete classpath of the application
  that is used during its build, including `android.jar`.

* `<output directory>` is the pathname of the directory where the Cangjie source
  files containing mirror type declarations will be placed, such as `./src/cj`.

* `<names-of-mirrored-types>` are the _fully qualified names_ of the Java
  reference types on which your interop class design depends,
  other than `java.lang.Object`, `java.lang.String` or arrays.

* `<jar-file>` is the pathname of a single jar file. All `public` classes and
  interfaces, the `.class` files of which it contains, are mirrored, along
  with any dependencies found along the `<full-application-classpath>`.

**Example:**

Continuing the example from the
[previous section](#initial-interop-class-creation-workflow),
suppose we want our function `Interop.m()` to call the method
`String g(A a, int i)` of a class `com.example.c.C`, where `A`
is the type `com.example.a.A` that we've already mirrored:

```java
package com.example.c;

import com.example.a.A;

public class C {
    public static String g(A a, int i) {
        /* Some Java code returning a string */
    }
}
```

We re-run the mirror generator, passing `com.example.c.C` as an extra
argument:

```bash
java-mirror-gen \
    --package-name javaworld \
    --class-path /home/user/Android/Sdk/platforms/android-35/android.jar:App.jar \
    --destination ./src/cj \
    com.example.a.A com.example.b.B com.example.c.C
```

This command will generate the same files with mirror type declaration
plus the file `src/javaworld/src/C.cj` and files with mirror type declarations
for any dependencies that type may have that were not previously mirrored.

The file `src/cj/javaworld/src/C.cj` would look like this:

```java
package javaworld

import java.lang.*

@JavaMirror["com.example.c.C"]
public class C {
    public static func g(a: ?A, i: Int32): ?JString
}
```


### Step 2: Import the mirror type(s) and write code

Make sure that all mirror type(s) involved are imported, then implement
the constructors and member functions of your interop classes, manipulating
Java types as if they were Cangjie types.

**Example:**

Continuing the example from the previous section, we can implement
the function `cjworld.Interop.m()` using the mirror type `javaworld.C`:

```cangjie
package cjworld

import java.lang.*
import javaworld.A
import javaworld.B
import javaworld.C

@JavaImpl
public class Interop {
    public static func m(a: ?A, s: ?JString, i: Int32): ?B {
        let s1: JString = match (a) {
            case Some(aa) => C.g(aa, i) ?? JString("")
        }
        B(s1)  // Assuming there is a B(String) constructor
    }
}
```

### Step 3: Recompile the Cangjie part

See [Step 4](#step-4-compile-the-interop-class) of the interop class
creation workflow for details and example.

As long as you have not changed the public interface of the interop class(es)
on the previous steps, you only need to update the `.so` file.
The generated Java sources should be identical to previously generated ones.


### Step 4: Update and re-build the Android project

Copy the `.so` file and, if applicable, `.java` files updated/generated
on the previous step over to your Android project and re-build it.

See [Step 5](#step-5-put-it-all-together) of the interop class
creation workflow for details and example.


## Features and Limitations of Interop Classes

1. An interop class _must_ be a direct subclass of a mirror class.
   By default, the interop class will inherit the mirror class
   [`java.lang.JObject`](#java.lang.jobject), not `std.core.Object`.

2. An interop class _may_ implement one or more mirror interfaces, but never
   a conventional Cangjie interface. Conversely, a conventional Cangjie type may not
   implement or inherit a mirrored Java interface.

3. An interop class may not be declared as `open` or `abstract` and may not be
   extended using `extend`.

4. An interop class may introduce new instance fields _of any Cangjie type_
   and override the member functions of its mirrored superclass.


5. The constructors of an interop class may call superclass constructors
   using `super()`, but have the same limitation on instance member function
   calls as the conventional Cangjie constructors, as well as the requirement
   to initialize all newly introduced member variables.

6. The instance member functions of an interop class may call instance
   member functions which that interop class has inherited from its mirrored
   superclass, and/or use `super.` to call the member functions of that
   superclass that the interop class overrides.

7. The signatures of constructors and member functions of all mirror types
   and interop classes can only use types that are (a) mirror types
   or interop classes themselves, or (b) are 100% analogous to Java primitive
   types. See the Type Mapping table
   in [Calling Java from Cangjie](#calling-java-from-cangjie).

8. Values of mirror types and interop classes:

    * Must not escape to global or static Cangjie variables, nor to any
      data structures to which such variables refer. The cjc compiler
      does not enforce this restriction yet, so strict programming discipline
      is required. Failure to comply with that discipline may lead to an abnormal
      program termination.

    * Must be explicitly disposed of when no longer needed. Best if at first
      opportunity, but in any case before control returns to the JVM.
      Failure to do so may result in memory leaks and the JVM throwing
      an `OutOfMemoryError`.

    See the section [Java Reference Management](#java-reference-management)
    for details.

The following three limitations are Android/JVM specific:

9. Any Cangjie code that uses a mirror type or interop class type must be executed
   in a thread registered in the Java VM. That may be a thread created in the Java
   code or an O/S thread registered in (aka "attached to") the JVM using the Java
   Invocation API. This is another requirement that must be met through programming
   discipline and obedience in the current version, but may be enforced by the Cangjie
   compiler in the future.

10. The Java counterparts of all mirror types and interop classes must all be loaded
    by the same classloader.

11. Unlike Java and other JVM languages, Cangjie does not permit circular import
    dependencies to exist between packages. That poses a challenge to the
    mirror generation process. Refer to the
    [Circular Import Dependencies Handling](#circular-import-dependencies-handling)
    subsection for details.


# Java to Cangjie Mapping

The current version of the mirror generator does the following Java
→ Cangjie conversions.


## General Considerations {#java-general-considerations}

The mirror generator takes Java _class_ files as input. Any information that
the Java compiler does not propagate from Java source code to class files is
therefore not available to the mirror generator. Most notably, this concerns
[generics](#java-generics) and names of method parameters.


## Names {#java-names}

The original names of Java types, fields and methods are preserved to the
maximum possible extent. If the original name could not be preserved for
one of the reasons outlined below, it is propagated to the Cangjie compiler
via an annotation.

* Java identifiers that clash with Cangjie keywords, such as "`func`",
  "`main`"  or `Int32` are enclosed in backticks ` `` ` to form raw Cangjie
  identifiers:

  ```java
      public static final long Int32 = 0xffff_ffff;
  ```

  ```cangjie
      public static let `Int32`: Int64
  ```

* Java identifiers may contain characters that are not permitted in
  Cangjie identifiers, most notably the dollar sign `$`, which is used
  in binary names of nested Java types. Such characters are replaced
  with underscores `_`:

  ```java
  public class Outer {
      public class Inner {}
      public Inner getInner() { return new Inner(); }
  }
  ```

  ```cangjie
  @JavaMirror["Outer"]
  public open class Outer {
      public init()

      public open func getInner(): ?Outer_Inner
  }

  @JavaMirror["Outer$Inner"]
  public open class Outer_Inner {
      public init(p0: ?Outer)
  }
  ```

* Although it is considered bad practice, a Java type may have a field,
  a member type, and a method share the same simple name (identifier).
  This works, because it is always possible to determine the meaning of a name
  either by syntax (only method names can be followed by "`(`") or from context.
  In addition, instance and static methods of a type may have the same names
  in Java as long as their signatures are different.

  In Cangjie, however, all member variables and non-overloaded functions
  declared in a given scope must have distinct names. (There are no member
  types in Cangjie, so name clashes with member types simply never happen,
  as they are [mirrored into top-level types](#java-classes-and-interfaces).
  In particular, an instance member function and a static member function
  cannot have the same name.

  The mirror generator therefore appends "`_`_`type-name`_" to the names
  of instance variables and "`Static`" to the names of  `static` methods
  if their original Java names clash with other field/method names.
  It retains the original name as the value of the `@ForeignName` annotation:

  ```java
  public class Node {
      public int id;
      public Node(int id) { this.id = id; }
      public static int id(long x) { return (int)x; }
      public static int id(short x) { return x; }
      public int id() { return id; }
      public void id(int newId) { this.id = newId; }
  }
  ```

  translates to

  ```cangjie
  public open class Node {
      @ForeignName["id"]
      public var id_Node: Int32

      public init(arg0: Int32)

      @ForeignName["id"]
      public static func idStatic(arg0: Int64): Int32

      @ForeignName["id"]
      public static func idStatic(arg0: Int16): Int32

      public open func id(): Int32

      public open func id(arg0: Int32): Unit
  }
  ```

* Names of Java packages cannot be preserved in practice as circular import
  dependencies between packages, omnipresent in Java, are forbidden
  in Cangjie. See
  [Circular Import Dependencies Handling](#circular-import-dependencies-handling)
  for details.


## Primitive Types

Java primitive types are mirrored to the respective Cangjie value types:

Java Type         Cangjie Type
----------------  ------------
`boolean`         `Bool`
`byte`            `Int8`
`short`           `Int16`
`char`            `UInt16`
`int`             `Int32`
`long`            `Int64`
`float`           `Float32`
`double`          `Float64`


## Classes and Interfaces {#java-classes-and-interfaces}

Java class and interface _definitions_ are mirrored respectively into Cangjie
class and interface declarations annotated with `@JavaMirror`.
The value of that annotation is a string that retains the original
fully qualified name of the mirrored Java type. Simple names of mirrored
types are preserved unless they contain characters that are not permitted
in Cangjie identifiers. Such characters, most notably the dollar sign `$`,
the presence of which in a Java class file name is usually an indication
of the respective type being a nested type, are replaced with underscores `_`.

_Uses_ of Java class and interface types as types of mirrored fields,
and/or as types of parameters and return values of mirrored methods and
constructors, get wrapped in `Option<T>`
(see [Null Handling](#java-null-handling) for details.)

`@JavaMirror`-annotated declarations differ from conventional
Cangjie class/interface definitions in a few aspects:

* The root of the Java mirror classes hierarchy is not `std.core.Object`,
  but a built-in mirror class [`java.lang.JObject`](#java.lang.jobject)

* The mirror for `java.lang.String` is also built-in, its name
  is [`java.lang.JString`](#java.lang.jstring)

* Only the symbolic information is mirrored. Variable initializers
  and function/constructor bodies are omitted.

**Example:**

For example, a mirror class for the following Java class:

```java
public class Node {
    public static final int A = 0xDeadBeef;
    private int id;
    public Node(int id) { this.id = id; }
    public int id() { return id; }
}
```

might look like this:

```cangjie
@JavaMirror["Node"]
public open class Node {
    public static let A: Int32
    public init(id: Int32)
    public func id(): Int32
}
```

Only public Java classes and interfaces are mirrored. Non-`final` classes
are modified with `open`. The modifiers `sealed` and `non-sealed` are ignored,
as well as the legacy modifier `strictfp`.

Private and package-private members and constructors, as well as static
and instance initializers, are not mirrored.

If the names of a Java type member and its mirror differ for one of the
reasons outlined in [Names](#java-names) the original Java member name
is propagated to Cangjie via the value of the `@ForeignName` annotation
on the mirror member:

```java
    CurrencyAmount priceInUS$Per(WeightUnit wu) { ... }
```

```cangjie
    @ForeignName["priceInUS$Per"]
    public open priceInUS_Per(arg0: WeightUnit): CurrencyAmount
```

> **NOTE:** The meaning of the access modifier `protected` is different
> in Java and Cangjie.
>
> In Java, access to a `protected` member or constructor of a class
> is permitted from anywhere within the same package and from subclassses
> defined in other packages.
>
> In Cangjie, that modifier also permits access from subpackages and
> from any package within the same module.
>
> Normally, this should not pose a problem.

**Fields** are mirrored into member variables of the respective mirror types.
Field names are preserved as long as they don't [clash](#java-names) with names
of other members. The modifiers `public`, `protected` and `static` are
preserved. The modifiers `transient` and `volatile` are ignored. `final` Java
fields are mirrored into `let` member variables, non-`final` — into `var`
member variables. Variable initializers are omitted.

**Methods** are mirrored into member functions with the respective mirror
types substituted for parameter types and return value type. Mirrors of `void`
methods have the `Unit` return type. Instance method names are preserved.
Static method names are reserved as long as they don't [clash](#java-names)
with instance method names. The modifiers `public`, `protected` and `static`
are preserved. The modifiers `native` and `synchronized` are ignored,
as well as the legacy modifier `strictfp`. Mirrors of non-`final` methods
are modified with `open`.

**Constructors** are mirrored into `init` constructors with the respective
mirror types substituted for parameter types. _This includes the default
constructor that might have been implicitly declared._ The modifiers `public`
and `protected` are preserved.

**NOTES:**

1. Mirror classes may not have primary constructors.

2. Mirror classes that contain no `init` constructors do _not_ get a default
   one defined implicitly, unlike the conventional Cangjie classes, and thus
   cannot be instantiated by calling a constructor. For automatically
   generated mirror classes, the absence of a constructor usually means that
   the mirrored Java class declares only `private` or package-private
   constructors so as to prevent its instantiation by arbitrary code.
   See also [Enum Classes](#enum-classes).

3. The Java mirror generator takes _class files_ as input, and the
   names of method/constructor parameters are often absent in class files.
   In that case, the mirror generator will assign them names `arg0`, `arg1`,
   and so on. The `javac` compiler option `-parameters` forces parameter names
   retention, but only for classes, not interfaces. Same goes for the debug
   information generation option `-g` / `-g:vars`.

**Member types** are mirrored into the respective top-level types, as Cangjie
does not support type nesting. The name of a member type mirror is derived
from the _binary_ name of the original member type, which consists of the
binary name of its immediately enclosing type, followed by a dollar sign `$`,
followed by the simple name of the member type itself. However, the dollar sign
is not permitted in Cangjie identifiers, so it is replaced with an underscore
`_` (see also [Names](#java-names)). The modifiers `public` and `protected` are
preserved. The modifier `static` is ignored. `init` constructors of mirrored
inner classes have an extra parameter for passing the enclosing instance
(that parameter is implicit in Java):

```java
public class Outer {
    public static class Static {}
    public class Inner {}
    public Inner getInner() { return new Inner(); }
}
```

```cangjie
@JavaMirror["Outer"]
public open class Outer {
    public init()

    public open func getInner(): ?Outer_Inner
}

@JavaMirror["Outer$Static"]       // Original binary name is retained
public open class Outer_Static {  // '$' is replaced with '_'
    public init()
}

@JavaMirror["Outer$Inner"]       // Original binary name is retained
public open class Outer_Inner {  // '$' is replaced with '_'
    public init(p0: ?Outer)      // Extra parameter for enclosing instance
}
```

Bodies are omitted in the mirrors of _all_ methods and constructors, so they
all look like abstract member functions in regular Cangjie code. That
imposes the following syntax alterations:

* The modifier `abstract` on _class_ methods is preserved, as otherwise
  there would have been no way to tell apart the mirrors of abstract and
  concrete Java methods:

  ```java
  public abstract class A {
      public void c() {}
      public abstract void a();
  }
  ```

  ```cangjie
  @JavaMirror["A"]
  public abstract class A {
      public init()

      public open func c(): Unit

      public open abstract func a(): Unit
  }
  ```

* For the same reason, mirrors of default interface methods are annotated
  with `@JavaHasDefault`.

  ```java
  public interface I {
      default void c() {}
      void a();
  }
  ```

  ```cangjie
  @JavaMirror["I"]
  public interface I {
      @JavaHasDefault
      func c(): Unit

      func a(): Unit
  }
  ```

In methods with a variable number of parameters, `, ...` is ignored.


### Mirror Type Inheritance

Mirror classes and interfaces form separate subtype hierarchies, which
means that:

* The root of the Java mirror classes hierarchy is not `std.core.Object`,
  but a built-in mirror class [`java.lang.JObject`](#java.lang.jobject).

* Mirror interfaces may inherit other mirror interfaces, reflecting
  the inheritance relationships between the original Java interfaces.
  Mirror interfaces may not inherit regular Cangjie interfaces and
  vice versa.

* Mirror classes may inherit other mirror classes, reflecting
  the inheritance relationships between the original Java classes.
  Mirror classes may not inherit regular Cangjie classes and
  vice versa.

* Mirror classes may implement mirror interfaces, but not regular
  Cangjie interfaces. In particular, they do not implement the
  interface `Any`. Regular Cangjie classes may not implement mirror
  interfaces.


### Generics {#java-generics}

Java generics are erased during compilation, so the automatically
generated mirror types are always non-parameterized and have type variables
replaced with mirrors of their leftmost bounds.

It is not possible to declare a parameterized mirror type manually
either.

The type `JArray<T>` (see [Arrays](#arrays)) is a special exception.


## Arrays

The special built-in type `java.lang.JArray<T>` is used to represent
mirrors of Java arrays.

A Java array of type _`T`_ (_`T`_`[]`), is generally mirrored into:

* `?JArray<`_`T'`_`>`, if _`T`_ is a primitive type

* `?JArray<`_`?T'`_`>`, if _`T`_ is a reference type

where _`T'`_ is the mirror of _`T`_.
Refer to [Null Handling](#java-null-handling) for the reasoning
behind `Option<T>` wrapping.

**NOTE:** Java arrays are covariant, whereas Cangjie generics are
invariant, and the class `JArray<T>` is no exception.


## Enum Classes

A Java enum class _`E`_ is mirrored into a Cangjie mirror class _`E'`_ that
inherits the mirror of `java.lang.Enum` and is neither `open` nor `sealed`
itself, thus cannot be extended.

The class _`E'`_ contains:

* Mirrors of the enum constants of _`E`_, in the form of public static
  member `let`-variables of type _`E'`_.

* No constructors, for the instantiation of the mirror class
  to be impossible. (Mirror classes do not have default constructors.)

* Mirrors of the implicitly defined methods
  `public static `_`E`_`[] values()`
   and `public static `_`E`_` valueOf(String name)`

* Mirrors of any `public`/`protected` fields and methods of the original
  enum class as if they were fields and methods of an [ordinary class](#java-classes-and-interfaces)


## Special Considerations



## `null` Handling {#java-null-handling}

Cangjie has no concept of null references and hence no equivalent for the Java
null type. If the reference type of a Java method return value was mirrored
direct to the respective mirror type, any `null` value returned from that
method could lead to a segmentation fault. Conversely, there has to be a way
to pass a `null` value from Cangjie to a Java method or constructor.

Therefore, if the original Java type of a field, array element,
method/constructor parameter or method return value is a reference type _`R`_,
the mirror of that _entity_ will have the type `Option<`_`R'`_`>`, where _`R'`_
is the mirror of the _type_ _`R`_. On the Cangjie side, `None` stands for the
`null` value, and `Some(`_`r'`_`)` represents a (non-null) reference value
_`r'`_ of the type _`R'`_. The `cjc` compiler recognizes `Option<T>`
as a Java-compatible type if `T` is a mirror type or interop class and
wraps/unwraps the values of `T` accordingly.

For instance, consider the following Java interface:

```java
interface Concatenator {
    String concat(String[] ss);
}
```

The `ss` parameter itself may be `null`, each element of the `ss` array may be
`null` and the `concat` method may return `null`. Therefore, the _safe_ way
to mirror that interface is as follows:

```cangjie
@JavaMirror
interface Concatenator {
    func concat(ss: ?JArray<?JString>): ?JString
}
```

For the same reason, you should use `Option<T>` wrapping when declaring
a local variable of a foreign type in the code of an interop class, unless you
are 100% sure that it won't be assigned `null`.

```cangjie
    // Suppose M is a Java mirror type
    let m: M = M()     // If M() returns successfully, it is guaranteed
                       // to have returned a new instance of M
```

The `Option<T>` wrapping ensures that the code won't break if a `null` value
sneaks into the Cangjie world from the Java one, but it does that at the cost
of performance and memory footprint. The other disadvantage of this approach is
the [loss of variance](#loss-of-variance).


### Loss of Variance

One limitation imposed by the [`Option<T>` wrapping](#java-null-handling)
of Java mirror types and interop classes is that such wrapped types follow
the semantics of Cangjie in all other respects. In particular, `Option<T>` is
_invariant by its type parameter `T`_: `Option<U>` is not a subtype
of `Option<T>` if `U` is a subtype of `T`, unless `U` and `T` are the same
type. For mirror types that means that any overriding Java method that relies
on return type covariance may not be mirrored that way with `Option<T>`
wrapping. Its return type has to be propagated from the superclass method.

**Example:**

Suppose a Java class `Foo` is a direct superclass of the class `Bar`:

```java
public class Foo {}

public class Bar extends Foo {}
```

and the interface `C` declares a method `get` that returns an instance of `Foo`:

```java
public interface C {
    public Foo get();
}
```

A subinterface of `C` may then override `get` with a more precise return type,
`Bar`:

```java
public interface D extends C
    @Override
    public Bar get();
@end
```

Without `Option<T>` wrapping, all those types could be mirrored to:

```cangjie
@JavaMirror
public open class Foo {}

@JavaMirror
public open class Bar <: Foo {}

@JavaMirror
public interface C {
    public open func get(): Foo
}

@JavaMirror
public interface D <: C {
    public override open func get(): Bar       // Return type covariance in action
}
```

but if `get()` can possibly return `null`, an application crash is inevitable.

`Option<T>` wrapping makes it safe, but the return types of all overriding
methods have to be lowered to the return type of the original method:

```cangjie
@JavaMirror
public open class Foo {}

@JavaMirror
public open class Bar <: Foo {}

@JavaMirror
public open interface C {
    public open func get(): Foo
}

@JavaMirror
public open interface D <: C {
    // public open func get(): ?Bar    // Error, `Option<T>` is not covariant by T
    public open func get(): ?Foo       // OK, but the return type is lowered
}
```

Nullability annotations could partially alleviate the problem, but the current
version of the Cangjie SDK does not support them.


## Circular Import Dependencies Handling

Circular dependencies between packages are not only possible, but omnipresent
in Java. For instance, the ubiquitous class `java.lang.String` depends on:

* the interface `Serializable` from the `java.io` package,
* the class `Charset` from  `java.nio.charset`, and
* the class `Locale` from `java.util`,

and all those three types of course depend on the class `Object`
from `java.lang`!

Compilation to separate `.class` files and late binding effectively circumvent
this problem in Java. For a Cangjie import declaration to compile, however,
the entire package that it imports (from) must be already compiled.
Consequently, all Cangjie source files that belong to a given package must be
compiled together in one session into a single binary. One can say that the
minimum unit of compilation in Cangjie is an entire package, not an individual
file. Hence circular import dependencies between packages are not possible
in Cangjie code.


### Single-Package Mode

The above [difference](#circular-import-dependencies-handling) between the
two languages precludes the preservation of Java package names during mirror
generation. In practical terms, the mirror generator must _always_ collect all
generated mirror types in a single Cangjie package. The desired name of that
package must be specified with the option `--package-name`.

For instance, if you run the mirror generator with the following option:

`    --package-name java.world`

it will place all generated mirror type declarations in the `java.world`
package and propagate the fully qualified names of the original Java types
to the `cjc` compiler via arguments of the `@JavaMirror` annotations:

```cangjie
package java.world

import java.lang.*

@JavaMirror["java.lang.Cloneable"]
public interface Cloneable {
}
```


### Name Clashes

Java types declared in different packages may have the same simple name,
because their fully qualified names are different. For example, there is
a class `Attribute` in the JDK package `javax.management` and an interface
`Attribute` in `javax.naming.directory`. Their mirrors cannot co-exist
in a single Cangjie package. Therefore, the mirror generator detects such
name clashes when operating in the [single-package mode](#single-package-mode)
and mangles _all_ conflicting names. Specifically, it uses the fully qualified
name of each such type in place of its simple name, replacing dots `.`
with underscores `_`:

```cangjie
// src/java/world/src/javax_management_Attribute.cj
package java.world

import java.lang.*

@JavaMirror["javax.management.Attribute"]
public open class javax_management_Attribute <: Serializable {
   .  .  .
```

```cangjie
// src/java/world/src/javax_naming_directory_Attribute.cj
package java.world

import java.lang.*

@JavaMirror["javax.naming.directory.Attribute"]
public interface javax_naming_directory_Attribute <: Cloneable & Serializable {
   .  .  .
```


### Incremental Mirroring

Putting all Java mirror types into a single Cangjie package such
as `java.world` not only leads to [name clashes](#name-clashes), but
also increases the compile-time overheads and is generally inconvenient.
Breaking that mass of declarations down into several packages is
therefore highly desirable. Fortunately, not all Java packages are
in a single import dependency circle, so at least some breaking down is
possible.

First of all, you may notice that there are three sets of packages in any
Android application that may not have circular dependencies between them:

* Application packages
* Android API packages
* JDK API packages

This means that even in the worst possible case all mirror types could be
segregated into three Cangjie packages, respectively code-named "`app`",
"`android`" and "`java`".

Furthermore, the JDK API has been modularized since Java 9, and circular
import dependencies may _not_ exist between Java modules. Therefore it is
perfectly possible to replicate the structure of the JDK API _modules_
during mirroring. For instance, the Cangjie package `java.base` would
then contain mirrors of types from the packages exported from the
`java.base` JDK API module: `java.lang` and its subpackages,
`java.io`, `java.math`, and so on.

Finally, a third party library should have no circular import dependencies
with other application components and APIs. If your application contains
any such libraries that you also need to use from Cangjie code, you may
want to mirror each library into its own Cangjie package.

The _incremental mirroring_ process enables such segregation. You run
the mirror generator _once for each target Cangjie package_ (set with the
`--package-name` option, as usual), each time specifying two additional
parameters:

1. A _complete_ list of Java packages to mirror into that specific
   target Cangjie package. Those Java packages may have circular
   import dependencies between them, and may also import _previously_
   mirrored packages/types.

2. A cumulative list of fully qualified name mappings for all _previously_
   mirrored Java types. Initially this list is empty.

The mirror generator emits mirrors for all public classes and interfaces
that belong to the packages appearing on the list (1), and any dependencies
they may have that are _not_ already on the list (2). Then it appends all
newly established Java → Cangjie name mappings to the list (2).


#### Command-line Syntax {#incremental-mirroring-command-line-syntax}

Incremental mirroring is only supported in the single-jar mode at present,
which means that the second variant
of the mirror generator [command-line syntax](#jmg-command-line-syntax)
has to be used:

`java-mirror-gen [`_`options`_`] -jar `_`jar-file`_

_`options`_ must include the following:

`--package-name `_`target-package-name`_

_`target-package-name`_ is the name of the target Cangjie package.
The mirror generator will place _all_ mirror types into that package.

**IMPORTANT: You must specify a new, previously unused target Cangjie
package name every time you run the mirror generator in the incremental mode.
If you mirror some types into, say, `my.java.libs` package in the first
run of the mirror generator using `--package-name my.java.libs` and
run it again against different input but without changing the value
of `--package-name`, that would completely invalidate the results
of mirroring, making them inconsistent.**

> In a certain sense, a target Cangjie package is the minimal unit
> of mirroring, just like a source Cangjie package is the minimal unit
> of compilation when you develop in Cangjie: you cannot compile two
> Cangjie source files belonging to the same package separately.

`--package-list `_`pathname`_

_`pathname`_ must point to a plain text file that contains a list
of Java package names. Specifically, each line of that file must be
a fully qualified package name, optionally followed by a wildcard `.*`:

```
com.example.model
com.example.ui.*
   .  .  .
```

**NOTICE:** If the wildcard is present, that entry matches all subpackages
of the named package _and_ that package itself. This is different from
the semantics of the wildcard in Java and Cangjie import statements.

The generator will emit mirrors for _all_ non-anonymous non-private types
defined in the listed packages _and_ all their dependencies _except_
for the dependencies that are already present in the import mappings file,
if any. All those mirror types will be placed in a single Cangjie package
specified using the `--package-name` option (see above).

This option may only be used in the single-jar mode.

`--import-mappings `_`import-mappings-file`_

_`import-mappings-file`_ is the pathname of the _import mappings file_,
a plain text file that accumulates a set of Java to Cangjie fully qualified
name mappings for all mirror types as they are generated. The mirror generator
reads that file at startup and does _not_ mirror the Java types for which
mappings already exist, assuming that they were mirrored on its prior
invocation(s). If mirroring completes without errors, the mirror generator
adds the mappings for all mirrors it has just generated to the set and writes
it out to the `./imports_config.txt` file before termination.

**NOTE:** If _`import-mappings-file`_ is set to `./imports_config.txt`, that
file will get overwritten. Make a copy after each incremental run of the mirror
generator if you want to keep the intermediate sets of mappings,
e.g. for debugging purposes.


### Example: JDK API Mirroring

As mentioned [above](#incremental-mirroring), the JDK API is modularized,
so one could look at the
[list of modules](https://docs.oracle.com/en/java/javase/17/docs/api/index.html)
and their dependency graphs, collect lists of exported packages, and run the
mirror generator using the following command line template:

```bash
java-mirror-gen \
    --android-jar /path/to/android.jar \
    --package-name java.base \
    --package-list ./java.base.txt \
    --import-mappings ./imports_config.txt \
    --destination src/cj \
    --class-path /path/to/android/SDK/platform/files/directory \
    -jar /path/to/android.jar
```

The file `./java.base.txt` should contain the list of packages exported
from the `java.base` JDK API module _for public use_:

```
java.io
java.lang
java.lang.annotation
   .  .  .
```

and the file `./imports_config.txt` should be empty or non-existent.

Upon the successful completion of the above command:

* The directory `./src/cj/java/base/src` will contain Cangjie source files
  with mirror type declarations for all public classes and interfaces
  defined in the packages listed in `./java.base.txt`, and

* The file `./imports_config.txt` will contain mappings of fully qualified
  names of all those Java types to the names of their Cangjie mirrors in the
  `java.base` package, for use in subsequent mirror generator invocations.

> **NOTICE:** The _implementations_ of many types exported from the module
> `java.base` depend on classes and interfaces defined in internal JDK
> packages, such as `sun.util.locale.provider.LocaleDataMetaInfo`
> or `jdk.internal.misc.Unsafe`. However, mirror types are _declarations_;
> they do not expose any private members of the respective Java types nor
> the implementation details of their public methods or constructors.
> So the mirror generator will not process the class files that belong
> to such internal packages at all.

Now we can pick a JDK API module that depends only on the `java.base`
module, e.g. `java.xml`, and run the mirror generator again, changing
only the values of two options:

* Set the value of `--package-name` to `java.xml`

* Set the value of `--package-list` to the pathname of a file
  containing the list of packages exported from the `java.xml` JDK API
  module:

  ```
  javax.xml.*
  org.w3c.dom
     .  .  .
  ```

Note that it is possible to put a wildcard `.*` after a package name to denote
that package _and_ all its subpackages at once. In the above excerpt,
`javax.xml.*` matches the package `javax.xml` itself, as well as
 `javax.xml.catalog`, `javax.xml.transform`, `javax.xml.transform.stream`,
and so on.

```bash
java-mirror-gen \
    --android-jar /path/to/android.jar \
    --package-name java.xml \
    --package-list ./java.xml.txt \
    --import-mappings ./imports_config.txt \
    --destination src/cj \
    --class-path /path/to/android/SDK/platform/files/directory \
    -jar /path/to/android.jar
```

`./src/cj/java/xml/src` should now contain mirror declarations for all
`java.xml` module exports, whereas `./imports_config.txt` should now contain
mappings for _both_ `java.base` and `java.xml` Cangjie packages.

Repeat this process for the remaining modules, in any order that ensures
mirroring of all dependencies of each module before mirroring that module
itself.



### Using Incremental Mirroring

You can use [incremental mirroring](#incremental-mirroring) to segregate
arbitrary components of the application code that need to be used
from Cangjie, as long as there are no circular import dependencies between
those components and/or the rest of the Java code. In particular, the public
classes and interfaces of each third party Java library that Cangjie code
needs to use can be mirrored separately into an appropriately named Cangjie
package.

To accomplish that, first break down the set of packages constituting
the application into subsets that have no circular import dependencies
between them. Then use the incremental mirroring process described above:

1. Pick any subset that has no import dependencies on packages
   from other subsets. Mirror it all at once into an appropriately named
   package.

2. Mirror any subset that only depends on zero or more of the previously
   mirrored subsets.

3. Repeat the previous step until all Java types that you want to use in
   Cangjie code are mirrored, _each time picking a new target Cangjie
   package name_.


## Closure Depth Limiting

In addition to numerous
[circular import dependencies between packages](#circular-import-dependencies-handling),
another property is inherent to the standard Java API and many popular Java
libraries and frameworks: enormous sizes of import closures.

For instance, invoking the mirror generator to produce a mirror for an empty
enum type

```java
public enum E {}
```

makes it also generate mirrors for `java.lang.Enum` _and all its dependencies_
from the standard Java library, about 300 mirror types total:

```
AbstractInterruptibleChannel.cj
AbstractStringBuilder.cj
AccessControlContext.cj
AccessMode.cj
AccessibleObject.cj
   .  .  .
ZoneOffsetTransitionRule.cj
ZoneRules.cj
ZonedDateTime.cj
```

For all those mirror types, the compiler will generate glue code, most of which
a real program will never use. That may be tolerated in a desktop or server
environment, but not on a mobile platform such as Android.

Asking the developer to supply an exact list of types and members to mirror
would be too much. Fortunately, the simple _limiting of depth_ during the
calculation of dependency closures yields reasonably good results: the number
of generated mirrors can drop by an order of magnitude or more. For instance,
mirroring the above empty enum type `E` with depth limited to 2 produces just
six mirror types in addition to the mirror of the type `E` itself: the enum
base class `java.lang.Enum`, three interfaces that it implements, and the
return types of two of its methods:

```
Class.cj
Comparable.cj
Constable.cj
E.cj
Enum.cj
Optional.cj
Serializable.cj
```

Here is how depth limiting works exactly:

* The set of mirrored _types_ always includes:

    - Primitive Java types,
      [mirrored into the respective Cangjie value types](#primitive-types);
    - [Class and interface types](#java-classes-and-interfaces) explicitly
      specified on the mirror generator command line;
    - `java.lang.Object` and `java.lang.String`, [pre-mirrored respectively
      into `JObject` and `JString`](#interop-library-api-reference); and
    - [Array types](#arrays), the element types of which are among the above
      listed types, mirrored into `JArray<T>`.

* _Members_ of types included in the set are then filtered as follows:

    - Inherited members are _not_ mirrored as "own" members even if the
      respective supertypes are not included in the set of mirrored types.

    - Fields, the types of which are not included in the set of mirrored
      types, are omitted.

    - Methods, the signatures of which contain types that are not included
      in the set of mirrored types, are omitted.

    - Member types are treated just like top-level types: unless they are
      explicitly specified on the mirror generator command line, they only
      get mirrored if included in the set of mirrored types during the
      limited-depth dependency closure calculation process described here.

* The [command-line option](#jmg-command-line-syntax) `--closure-depth-limit`
  sets the depth limit for the explicitly specified class and interface
  types.

* If the depth limit for a given type _`T`_ is zero, _no types on which `T`
  depends get added to the set_. Even the supertypes of _`T`_ are not added.

  **Example:**

  ```java
  // A.java
  public class A {
      public void f(String s) {}
  }

  // B.java
  public class B extends A {
      public void g(String s) {}
  }
  ```

  If the mirror generator is instructed to mirror the class `B` with depth
  limited to 0, it will only generate a mirror for `B` and its method
  `g(String)`, because `JString` is automatically included in the set of
  mirrored types. At the same time, the method `f(String)` that `B` inherits
  from `A` will not be available:

  ```cangjie
  // B.cj
     .  .  .
  @JavaMirror["B"]
  public open class B {
      public init()

      public open func g(s: ?JString): Unit
  }
  ```

* If the depth limit for a given type _`T`_ is any positive _`N`_, the set
  of mirrors _additionally_ includes the following types, with the depth
  limit of _`N`_`-1`:

    - All (that is, recursively collected) supertypes of _`T`_;
    - Types of the non-`private` fields _declared in `T` itself_,
      that is, not the types of inherited fields;
    - Types of parameters of the non-`private` constructors of _`T`_; and
    - Types of parameters and return values of the non-`private` methods
      _declared in `T` itself_. Note again that the inherited methods
      are _not_ scanned.

  If a type is already included in the set, but with a lower depth limit,
  the latter is changed to _`N`_`-1`.

  The process is repeated recursively for all types newly added to the set
  of mirrors.

  **Example:**

  ```java
  // A.java
  public class A {
      public void f(C c) {}
  }

  // B.java
  public class B extends A {
      public void g(D d) { }
  }

  // C.java
  public class C { }

  // D.java
  public class D extends C {}
  ```

  If the mirror generator is instructed to mirror the class `B` with depth
  limited to 1, it will generate mirrors for `B`, its superclass `A` and
  the class `D` that is the type of the sole `B.g(D)` method parameter.
  However, `A` and `D` will be mirrored with depth limit set to 0, so the
  class `C`, and hence the method `A.f(C)` will not be mirrored:

  ```cangjie
  // A.cj
     .  .  .
  @JavaMirror["A"]
  public open class A {
      public init()
  }

  // B.cj
     .  .  .
  @JavaMirror["B"]
  public open class B <: A {
      public init()

      public open func g(d: ?D): Unit
  }

  // D.cj
     .  .  .
  @JavaMirror["D"]
  public open class D {
      public init()
  }
  ```

  Finally, setting the depth limit to 2 will make the mirror generator
  include mirrors of the class `C` and the method `A.f(C)` in its output.


# Java Mirror Generator Reference


## Prerequisites

The Java mirror generator requires a copy of JDK 17 to run.
If you do not have JDK 17 installed and added to your executable search `PATH`
install and/or add it before using the Java mirror generator.


You also need to know the _local_ pathnames of the jar files and directories
that contain all dependencies of the classes you are going to mirror. This
includes the Android standard library jar as well as the jars that will appear
on the classpath when your application launches.


## Command-line Syntax {#jmg-command-line-syntax}

The Java mirror generator can be run in two ways:

`java-mirror-gen [`_`options`_`] [`_`type-names`_`]`

to generate mirrors for one or more Java classes and/or interfaces _and_ all
their dependencies, _or_

`java-mirror-gen [`_`options`_`] -jar `_`jar-file`_     _(single-jar mode)_

to generate mirrors for all types the `.class` files of which the given
_`jar-file`_ contains _and_ all their dependencies residing elsewhere
on the supplied class path, if any,

where

* _`options`_ are the [command-line options](#command-line-options)
  of the mirror generator.

* _`type-names`_ are the _fully qualified names_ of Java classes and
  interfaces that need to be mirrored (that is, _not_ pathnames
  of their `.class` files).

* _`jar-file`_ is the pathname of a single jar file.

**NOTE:** ([Incremental mirroring](#incremental-mirroring) and/or
[closure depth limiting](#closure-depth-limiting) may restrict the
set of mirrored types and/or their members during each invocation
of the mirror generator.


## Command-line Options

* `-a `_`pathname`_, `-android-jar `_`pathname`_   _(mandatory)_

    _`pathname`_ must point to the `android.jar` file from the Android SDK
    used to build the Java part of the application. This option must always
    be present and point to an existing file, otherwise the script shall
    fail with an error message.


* `-d `_`directory`_, `--destination `_`directory`_

    _`directory`_ is the pathname of the directory into which the mirror
    generator shall place its output Cangjie source code files containing
    the generated mirror type declarations, in a hierarchy of subdirectories
    conforming to CJPM requirements.
    If this option is not specified, the current directory is assumed.


* `-p `_`name`_, `--package-name `_`name`_   _(mandatory?)_

    _`name`_ is the name of the Cangjie package into which all generated
    mirror types will be placed.
    See [Single-Package Mode](#single-package-mode) for details.


* `-c `_`number`_, `--closure-depth-limit `_`number`_

    _`number`_ is a non-negative decimal integer limiting the depth
    of dependency graph scanning when determining the set of types
    and their members that will be mirrored.

    See [Closure Depth Limiting](#closure-depth-limiting) for details.


* `-jar `_`jar-file`_

    _`jar-file`_ is the pathname of the jar file to be processed in the
    "single-jar" mode (see [Command-Line Syntax](#jmg-command-line-syntax)
    above).


* `-l `_`pathname`_, `--package-list `_`pathname`_

    _`pathname`_ is the pathname of a plain text file containing a list
    of package names. Only the class files that belong to the listed
    packages _and_ their dependencies will be mirrored. Requires `-jar`.
    See [Command-Line Syntax](#incremental-mirroring-command-line-syntax)
    in the [Incremental Mirroring](#incremental-mirroring) section for details.


* `-i `_`pathname`_, `--imports `_`pathname`_

    _`pathname`_ is the pathname of a plain text file containing
    mirror type mappings accumulated during previous mirror generator
    runs. Requires `-l` and `-jar`.
    See [Command-Line Syntax](#incremental-mirroring-command-line-syntax)
    in the [Incremental Mirroring](#incremental-mirroring) section for details.


* `-h`, `-?`, `--help`

    Prints a help message with a brief description of the command-line syntax
    and all options and exits.


* `-v`, `--verbose`

    Instructs the mirror generator to emit messages about what it is doing.



## Examples

```sh
java-mirror-gen \
    -android-jar $ANDROID_SDK/platforms/android-35/android.jar \
    -class-path ./classes \
    -destination ./mirrors \
    -p com.example \
    com.example.subpkg1.A com.example.subpkg2.B
```

```sh
java-mirror-gen \
    -a $ANDROID_SDK/platforms/android-35/android.jar \
    -cp ./lib \
    -d ./mirrors \
    -p javaworld \
    -jar App.jar
```

For a more complex example, see
[Example: JDK API Mirroring](#example-jdk-api-mirroring).


# Interop Library API Reference

The Android interop library includes enhanced versions of mirror types
for two fundamental Java classes, `java.lang.Object` and `java.lang.String`,
and a generic mirror type for representing Java arrays.

To enable the use of unqualified names, those mirror types are called
respectively `JObject`, `JString`, and `JArray<T>` so as to avoid name
clashes with Cangjie types from `std.core`.

They also have some methods renamed and new methods added to enhance
interoperability.


## `java.lang.JObject`

`java.lang.JObject` is the root of the hierarchy of Java mirror classes
and interop classes. It is itself a mirror of the `java.lang.Object`
class, but has some unsupported methods removed and some methods
renamed and added for better alignment with the Cangjie standard library.

**NOTE:** The methods removed from `JObject` are not available
in any other mirror classes either. Those are `clone()`, `finalize()`,
and `getClass`.

```cangjie
package java.lang

@JavaMirror["java.lang.Object"]
open class JObject {
    public open func equals(obj: ?JObject): Bool

    public func hashCode(): Int64
    @ForeignName["hashCode"]
    public open func hashCode32(): Int32

    public func toString(): String
    @ForeignName["toString"]
    public open func toJString(): JString

    public func wait(timeoutMillis: Int64): Unit
    public func wait(timeoutMillis: Int64, nanos: Int32): Unit
    public func wait(): Unit
    public func notifyAll(): Unit
    public func notify(): Unit
}
```

The instance member function `equals` and all `wait/notify` functions
are mirrors of the respective Java methods.


```cangjie
public func hashCode(): Int64
```

Calls the original Java method `hashCode` and casts the returned 32-bit `int`
value to `Int64`. Introduced to better meet the expectations of Cangjie
developers.

```cangjie
@ForeignName["hashCode"]
public open func hashCode32(): Int32
```

The original Java method `hashCode`, renamed to `hashCode32` to avoid a name
clash.

```cangjie
public func toString(): String
```

Calls the original Java method `toString` and converts its result to a
Cangjie `String`. In the _very_ unlikely event of receiving `null`
from the underlying Java method, throws an exception.

Introduced to better meet the expectations of Cangjie developers.

**NOTE:** This function returns a Cangjie `String`, breaking the requirement
to use only Java-compatible types for parameters and return values of public
member functions and constructors of mirror types and interop classes.
This is only possible because the `cjc` compiler has dedicated support for this
member function.

```cangjie
@ForeignName["toString"]
public open func toJString(): JString
```

The original Java method `toString`, renamed to `toJString` to avoid a name
clash.

An implementation of Java `toString` is very unlikely to return `null`, hence
the return type is `JString`, not `?JString`.


## `java.lang.JString`

```cangjie
package java.lang

@JavaMirror["java.lang.String"]
open class JString {
       .  .  .
    public init(cjString: String)
       .  .  .
}
```

```cangjie
public init(cjString: String)
```

Effectively converts the given Cangjie `String` to a Java string (`JString`).

**NOTE:** This constructor accepts a parameter of the Cangjie type `String`,
breaking the requirement to use only Java-compatible types for parameters
and return values of non-private member functions and constructors of mirror
types and interop classes. This is only possible because the `cjc` compiler
has dedicated support for `JString`.

Members inherited from [`JObject`](#java.lang.jobject):
`equals`, `hashCode`, `hashCode32`, `toString`, `toJString`, `wait/notify`
methods.


## `java.lang.JArray<T>`

`JArray<T>` is a special built-in generic mirror type that mirrors all Java array
types. `T` must be either a value type mapped to a primitive Java type, such as
`Int32` or `Bool`, a mirror type, or an interop class.

**Limitations:**

As of the current version:

* Java arrays with nullable elements are not supported. In other words, if `T`
  is a mirror type or an interop class, the type `JArray<T>` is supported,
  but the type `JArray<?T>` is not.

* Variables and parameters of Java array types may not be marked as
  nullable using the `Option` enum. That is, even if `JArray<T>` is a valid
  type, `?JArray<T>` is not recognized as such.

The API of Java arrays is limited compared to that of the Cangjie `Array<T>`
struct type; the only operations besides construction are length query,
element access, and the inherited methods of `java.lang.Object`.

```cangjie
public init(length: Int32)
```

Constructs a new Java array of the given `length`.

```cangjie
public prop length: Int32
```

The number of elements in the array.

```cangjie
public operator func [](index: Int32): T
public operator func [](index: Int32, value!: T): Unit
```

The element access operator `[]`.

Members inherited from [`JObject`](#java.lang.jobject):
`equals`, `hashCode`, `hashCode32`, `toString`, `toJString`, `wait/notify`
methods.


