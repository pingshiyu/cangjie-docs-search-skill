# `cjc` Usage

`cjc` is the compilation command for the Cangjie programming language, providing extensive functionality and corresponding compilation options. This chapter introduces its basic usage.

`cjc-frontend` (Cangjie Frontend Compiler) is distributed alongside `cjc` through the `Cangjie SDK`. `cjc-frontend` can compile Cangjie source code into Cangjie's intermediate representation (`LLVM IR`). `cjc-frontend` only performs frontend compilation of Cangjie code. Although `cjc-frontend` and `cjc` share some compilation options, the compilation process terminates after frontend compilation. When using `cjc`, the Cangjie compiler automatically handles frontend and backend compilation as well as linking. `cjc-frontend` is provided solely as the physical embodiment of the frontend compiler. Except for compiler developers, `cjc` should be prioritized for compiling Cangjie code.

## Basic Usage of `cjc`

This section introduces the basic usage of `cjc`. For details about compilation options, please refer to the [cjc Compilation Options](../Appendix/compile_options.md) chapter.

The usage of `cjc` is as follows:

```shell
cjc [option] file...
```

Suppose there is a Cangjie file named `hello.cj`:

<!-- run -->

```cangjie
main() {
    println("Hello, World!")
}
```

You can compile this file using the following command:

```shell
$ cjc hello.cj
```

This will generate an executable file named `main` in the working directory. By default, `cjc` compiles the given source code files into an executable and names it `main`.

The above describes `cjc`'s default behavior when no compilation options are provided. You can control `cjc`'s behavior using compilation options, such as instructing `cjc` to perform whole-package compilation or specifying the name of the output file.