# Program Entry Point

The entry point of a Cangjie program is `main`. At the top level of the package in the root directory of the source files, there can be at most one `main` function.

When compiling a module into an executable, the compiler only searches for `main` at the top level of the root directory's source files. If no `main` is found, the compiler will report an error. If `main` is found, the compiler will further verify its parameter and return types. Note that `main` cannot be modified by access modifiers. When a package is imported, any `main` defined within that package will not be imported.

The `main` function serving as the program entry point can either have no parameters or accept a parameter of type `Array<String>`. Its return type must be either `Unit` or an integer type.

Example of `main` without parameters:

<!-- run -->

```cangjie
// main.cj
main(): Int64 { // OK.
    return 0
}
```

Example of `main` with `Array<String>` parameter:

<!-- run -->

```cangjie
// main.cj
main(args: Array<String>): Unit { // OK.
    for (arg in args) {
        println(arg)
    }
}
```

After compiling with `cjc main.cj`, executing via command line: `./main Hello, World` will produce the following output:

```text
Hello,
World
```

Below are some incorrect examples:

<!-- compile.error  -->

```cangjie
// main.cj
main(): String { // Error, return type of 'main' is not 'Integer' or 'Unit'.
    return ""
}
```

<!-- compile.error  -->

```cangjie
// main.cj
main(args: Array<Int8>): Int64 { // Error, 'main' cannot be defined with parameter whose type is not Array<String>.
    return 0
}
```

<!-- compile.error  -->

```cangjie
// main.cj
// Error, multiple 'main's are found in source files.
main(args: Array<String>): Int32 {
    return 0
}

main(): Int8 {
    return 0
}
```