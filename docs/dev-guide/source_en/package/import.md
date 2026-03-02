# Package Import

## Using `import` Statements to Import Declarations or Definitions from Other Packages

In the Cangjie programming language, you can import a top-level declaration or definition from another package using the syntax `import orgName::fullPackageName.itemName`, where `fullPackageName` is the full path package name and `itemName` is the name of the declaration. For packages without an organization name, omit the organization name and the organization name separator `::`. Import statements must appear after the package declaration and before any other declarations or definitions in the source file. For example:

```cangjie
package a
import std.math.*
import package1.foo
import {package1.foo, package2.bar}
import org::package1.foo // Import the subpackage foo from package1 under organization org
```

If multiple `itemName`s belong to the same `fullPackageName`, you can use the `import fullPackageName.{itemName[, itemName]*}` syntax. For example:

```cangjie
import package1.{foo, bar, fuzz}
```

This is equivalent to:

```cangjie
import package1.foo
import package1.bar
import package1.fuzz
```

In addition to importing a specific top-level declaration or definition using the `import fullPackagename.itemName` syntax, you can also use the `import packageName.*` syntax to import all visible top-level declarations or definitions from the `packageName` package. For example:

```cangjie
import package1.*
import {package1.*, package2.*}
import org::{package1.*, package2.*}
```

Note the following:

- The scope level of imported members is lower than that of members declared in the current package.
- If the module name or package name of an exported package is tampered with, making it inconsistent with the module name or package name specified during export, an error will be reported during import.
- Only top-level declarations or definitions visible to the current file can be imported. Attempting to import invisible declarations or definitions will result in an error at the import location.
- It is prohibited to import declarations or definitions from the package where the current source file resides using `import`.
- Circular dependency imports between packages are prohibited. If circular dependencies exist between packages, the compiler will report an error.
- `::` must be followed by a package name.
- When accessing imported members using the full package name, the organization name cannot be used.

Examples:

```cangjie
// pkga/a.cj
package pkga    // Error: pkga and pkgb have a circular dependency
import pkgb.*

class C {}
public struct R {}

// pkgb/b.cj
package pkgb

import pkga.*

// pkgc/c1.cj
package pkgc

import pkga.C // Error: C is not accessible in pkga
import pkga.R // Correct: R is an external top-level declaration in package pkga
import pkgc.f1 // Error: package pkgc cannot import itself
import org::* // Error: '*' must be followed by a package name
import org::pkgf
import pkgf
import org2::{
    pkga.{foo, bar} // Error: nested imports are not allowed
}

public func f1() {}

// pkgc/c2.cj
package pkgc

func f2() {
    // Correct
    R()

    // Correct: can use the full package name to access the imported declaration
    pkga.R()

    // Correct: declarations in the current package can be accessed directly
    f1()

    // Correct: can use the full package name to access the imported declaration
    pkgc.f1()

    // Error: cannot use the organization name prefix to access declarations
    org::pkgf.f1()

    // Error: ambiguity exists between pkgf and org::pkgf
    pkgf.f1()
}
```

In the Cangjie programming language, if an imported declaration or definition has the same name as a top-level declaration or definition in the current package and does not constitute function overloading, the imported declaration or definition will be shadowed. If they constitute function overloading, function resolution will follow the rules of function overloading during function calls.

```cangjie
// pkga/a.cj
package pkga

public struct R {}            // R1
public func f(a: Int32) {}    // f1
public func f(a: Bool) {} // f2

// pkgb/b.cj
package pkgb
import pkga.*

func f(a: Int32) {}         // f3
struct R {}                 // R2

func bar() {
    R()     // OK, R2 shadows R1.
    f(1)    // OK, invokes f3 in the current package.
    f(true) // OK, invokes f2 in the imported package
}
```

## Implicit Import of the `core` Package

Types such as `String` and `Range` can be used directly not because they are built-in types, but because the compiler automatically implicitly imports all `public` declarations from the `core` package for the source code.

## Using `import as` to Rename Imported Names

Since namespaces are separated between different packages, there may be top-level declarations with the same name in different packages. When importing top-level declarations with the same name from different packages, you can use `import packageName.name as newName` to rename them and avoid conflicts. Even without name conflicts, you can still use `import as` to rename imported content. The rules for `import as` are as follows:

- After renaming an imported declaration using `import as`, the current package can only use the new name; the original name cannot be used.
- If the renamed name conflicts with other names in the top-level scope of the current package and these names correspond to function-type declarations, they participate in function overloading; otherwise, a redefinition error is reported.
- The syntax `import pkg as newPkgName` is supported to rename package names, resolving naming conflicts between packages with the same name in different modules.
    <!-- compile.error -import3-->
    <!-- cfg="-p p1 --output-type=staticlib" -->

    ```cangjie
    // a.cj
    package p1
    public func f1() {}
    ```

    <!-- compile.error -import3-->
    <!-- cfg="-p p2 --output-type=staticlib" -->

    ```cangjie
    // d.cj
    package p2
    public func f3() {}
    ```

    <!-- compile.error -import3-->
    <!-- cfg="-p p1 --output-type=staticlib" -->

    ```cangjie
    // b.cj
    package p1
    public func f2() {}
    ```

    <!-- compile.error -import3-->
    <!-- cfg="-p pkgc --output-type=staticlib" -->

    ```cangjie
    // c.cj
    package pkgc
    public func f1() {}
    ```

    <!-- compile.error -import3-->
    <!-- cfg="libp1.a libpkgc.a libp1.a" -->

    ```cangjie
    // main.cj
    import p1 as A
    import p1 as B
    import p2.f3 as f  // Correct
    import pkgc.f1 as a
    import pkgc.f1 as b // Correct
    import org::pkgc as org_pkgc

    func f(a: Int32) {}

    main() {
        A.f1()  // Correct
        B.f2()  // Correct
        p1.f1() // Error: p1 was imported with an alias; the original package name cannot be used
        a()     // Correct
        b()     // Correct
        pkgc.f1()    // Error: pkgc.f1 was imported with an alias; the original name cannot be used
        org_pkgc.f1() // Correct
    }
    ```

- If conflicting imported names are not renamed, no error is reported at the `import` statement. However, an error will be reported at the usage location due to the inability to import a unique name. This can be resolved by defining an alias with `import as` or importing the package as a namespace using `import fullPackageName`.

    ```cangjie
    // a.cj
    package p1
    public class C {}

    // b.cj
    package p2
    public class C {}

    // main1.cj
    package pkga
    import p1.C
    import p2.C

    main() {
        let _ = C() // Error
    }

    // main2.cj
    package pkgb
    import p1.C as C1
    import p2.C as C2

    main() {
        let _ = C1() // OK
        let _ = C2() // OK
    }

    // main3.cj
    package pkgc
    import p1
    import p2

    main() {
        let _ = p1.C() // OK
        let _ = p2.C() // OK
    }
    ```

## Re-exporting an Imported Name

During the development of large-scale projects with extensive functionality, the following scenario is common: package `p2` heavily uses declarations imported from package `p1`. When package `p3` imports package `p2` and uses its functionality, the declarations from `p1` also need to be visible to `p3`. Requiring package `p3` to manually import the declarations from `p1` used in `p2` would be overly cumbersome. Therefore, it is desirable to import the declarations from `p1` used in `p2` when `p2` is imported.

In the Cangjie programming language, `import` can be modified with the access modifiers `private`, `internal`, `protected`, or `public`. Among these, `import` statements modified with `public`, `protected`, or `internal` can re-export the imported members (provided these imported members are not rendered unusable in the current package due to name conflicts or shadowing). Other packages can directly import and use the re-exported content from this package based on visibility, without needing to import this content from the original package.

- `private import` indicates that the imported content is only accessible within the current file. `private` is the default modifier for `import`; an `import` without an access modifier is equivalent to `private import`.
- `internal import` indicates that the imported content is accessible within the current package and its subpackages (including subpackages of subpackages). Access from outside the current package requires an explicit `import`.
- `protected import` indicates that the imported content is accessible within the current module. Access from outside the current package requires an explicit `import`.
- `public import` indicates that the imported content is accessible externally. Access from outside the current package requires an explicit `import`.

In the following example, `b` is a subpackage of `a`. In `a`, the function `f` defined in `b` is re-exported using `public import`.

```cangjie
package a
public import a.b.f

public let x = 0
```

```cangjie
internal package a.b

public func f() { 0 }
```

```cangjie
import a.f  // OK
let _ = f() // OK
```

Note that packages cannot be re-exported: if the imported content is a package, the `import` statement cannot be modified with `public`, `protected`, or `internal`.

<!-- compile.error -->

```cangjie
public import a.b // Error: cannot re-export package
```
