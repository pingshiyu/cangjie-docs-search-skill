# Running Your First Cangjie Program

Everything is ready—let's start writing and running your first Cangjie program!

## Compiling with cjc

First, create a new text file named `hello.cj` in an appropriate directory and write the following Cangjie code into it:

<!-- verify -->

```cangjie
// hello.cj
main() {
    println("Hello, Cangjie")
}
```

In this code snippet, we use Cangjie's comment syntax. Single-line comments can be written after the `//` symbol, while multi-line comments can be written between `/*` and `*/` symbols, which is identical to the comment syntax in languages like C/C++. Comment content does not affect program compilation and execution.

Next, execute the following command in this directory:

```bash
cjc hello.cj -o hello
```

Here, the Cangjie compiler will compile the source code in `hello.cj` into an executable file named `hello` for the current platform. When you run this file in a command-line environment, you'll see the program output the following content:

```text
Hello, Cangjie
```

> **Note:**
>
> The above compilation command is for Linux and macOS platforms. If you're using Windows, simply modify the compilation command to `cjc hello.cj -o hello.exe`.

## Compiling and Running with cjpm

In addition to using the `cjc` compiler directly, you can also use the **Cangjie Project Manager** (`cjpm`) to quickly create, manage, and run Cangjie projects.

Please follow the steps below to create your first Cangjie project:

1. create a new directory named `hello_cjpm` to store the project files, and then enter the directory.

2. use the `cjpm init` command to initialize a new Cangjie module.

```bash
cjpm init
```

After a successful execution, the command line will show `cjpm init success`. At this point, `cjpm` generates the default project structure in the current directory:

```text
hello_cjpm
├── cjpm.toml // The configuration file for the project
└── src
    └── main.cj // The default source code file
```

The content of the default source file `main.cj` is as follows:

<!-- verify -->

```cangjie
// main.cj
package hello_cjpm  // Declares that the current source file belongs to the hello_cjpm package

main(): Int64 {
    println("hello world")
    return 0
}
```

Alternatively, you can run `cjpm init --path hello_cjpm`. `cjpm` will automatically create the `hello_cjpm` directory and initialize the project inside it.

In the project root directory (where `cjpm.toml` is located), run the following command to compile and run the program:

```bash
cjpm run
```

`cjpm` will automatically handle dependency checks, compilation, and the execution of the program. The following output will be shown on the command line:  

```text
hello world

cjpm run finished
```
