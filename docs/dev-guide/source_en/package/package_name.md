# Package Declaration

In the Cangjie programming language, a package declaration starts with the keyword `package`, followed by an optional organization name and the organization name separator '::', then the package names from the root package to the current package separated by '.' on the path. Both organization names and package names must be valid ordinary identifiers (excluding raw identifiers). For example:

```cangjie
package pkg1      // root package pkg1
package pkg1.sub1 // subpackage sub1 under root package pkg1
package org1::pkg1.sub1 // subpackage sub1 under root package pkg1 of organization org1
```

> **Note:**
>
> In the current Windows platform version, organization names and package names do not support Unicode characters yet. They must be valid ordinary identifiers containing only ASCII characters.

The package declaration must appear as the first non-empty, non-comment line in a source file, and all source files within the same package must maintain consistent package declarations.

<!-- compile.error -->
<!-- cfg="-p test --output-type=staticlib" -->

```cangjie
// file 1
// Comments are accepted
package test
// declarations...

// file 2
let a = 1 // Error, package declaration must appear first in a file
package test
// declarations...
```

In Cangjie, package names should reflect the relative path of the current source file from the project's source root directory `src`, with path separators replaced by dots. For example, if the package's source code is located under `src/directory_0/directory_1` and the root package name is `pkg`, the package declaration in the source code should be `package pkg.directory_0.directory_1`.

Important considerations:

- The folder name containing the package must match the package name.
- The default name for the source root directory is `src`.
- Packages in the source root directory may omit package declarations, in which case the compiler will assign them the default package name `default`.

Given the following source directory structure:

```text
// The directory structure is as follows:
src
`-- directory_0
    |-- directory_1
    |    |-- a.cj
    |    `-- b.cj
    `-- c.cj
`-- main.cj
```

The package declarations in `a.cj`, `b.cj`, `c.cj`, and `main.cj` can be:

```cangjie
// a.cj
// in file a.cj, the declared package name must correspond to relative path directory_0/directory_1.

package default.directory_0.directory_1
```

```cangjie
// b.cj
// in file b.cj, the declared package name must correspond to relative path directory_0/directory_1.

package default.directory_0.directory_1
```

```cangjie
// c.cj
// in file c.cj, the declared package name must correspond to relative path directory_0.

package default.directory_0
```

```cangjie
// main.cj
// file main.cj is in the module root directory and may omit package declaration.

main(): Int64 {
    return 0
}
```

Additionally, package declarations must not cause naming conflicts: sub-packages cannot share names with top-level declarations in the current package.

Here are some error examples:

```cangjie
// a.cj
package a
public class B { // Error, 'B' is conflicted with sub-package 'a.B'
    public static func f() {}
}
```

<!-- compile.error -->
<!-- cfg="-p a/B --output-type=staticlib" -->

```cangjie
// b.cj
package a.B
public func f {}
```

<!-- compile.error -->
<!-- cfg="liba.a liba.B.a" -->

```cangjie
// main.cj
import a.B // ambiguous use of 'a.B'

main() {
    a.B.f()
}
```
