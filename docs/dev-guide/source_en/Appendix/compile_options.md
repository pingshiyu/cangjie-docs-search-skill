# `cjc` Compilation Options

This chapter introduces commonly used `cjc` compilation options. If an option is also applicable to `cjc-frontend`, it will be marked with a <sup>[frontend]</sup> superscript; if the behavior differs between `cjc-frontend` and `cjc`, additional explanations will be provided.

- Options starting with two hyphens are long options, such as `--xxxx`.
  If a long option has an optional parameter, the option and parameter must be connected with an equals sign, e.g., `--xxxx=<value>`.
  If a long option has a mandatory parameter, the option and parameter can be separated by either a space or an equals sign, e.g., `--xxxx <value>` is equivalent to `--xxxx=<value>`.

- Options starting with a single hyphen are short options, such as `-x`.
  For short options, if they are followed by a parameter, the option and parameter can be separated by a space or directly concatenated, e.g., `-x <value>` is equivalent to `-x<value>`.

## Basic Options

### `--output-type=[exe|staticlib|dylib|obj]` <sup>[frontend]</sup>

Specifies the type of the output file. In `exe` mode, an executable file is generated; in `staticlib` mode, a static library file (`.a` file) is generated; in `dylib` mode, a dynamic library file is generated (`.so` on Linux, `.dll` on Windows, and `.dylib` on macOS); in `obj` mode ,  an intermediate object file is generated ( `.o` on Linux and macOS, `obj` on Windows).

> **Note:** 
>
> Both the chir and obj modes are experimental features, and using the option `--output-type=[chir|obj]` may entail potential risks. This option must be used in conjunction with the `--experimental` option. In particular, the obj mode needs to be paired with the `--compile-target` option described below (see the `--compile-target` section for detailed usage).

`cjc` defaults to `exe` mode.

In addition to compiling `.cj` files into executable files, they can also be compiled into static or dynamic link libraries. For example:

```shell
$ cjc tool.cj --output-type=dylib
```

This compiles `tool.cj` into a dynamic link library. On Linux, `cjc` will generate a dynamic link library file named `libtool.so`.

**Note:** If a dynamic library file from Cangjie is linked when compiling an executable program, both the `--dy-std` and `--dy-libs` options must be specified. For details, refer to the [`--dy-std` option description](#--dy-std).

<sup>[frontend]</sup> In `cjc-frontend`, the compilation process stops at `LLVM IR`, so the output is always a `.bc` file. However, different `--output-type` values still affect the frontend compilation strategy.

### `--compile-target==[exe|staticlib|dylib]` <sup>[frontend]</sup>

This option is exclusively applicable to the `--output-type=obj` mode, with a default value of exe. Since the generated `.obj/.o` files are compilation intermediate products, specifying the `--compile-target` option enables the compiler to adopt the corresponding compilation strategy, thus generating intermediate files tailored for different types of final products. The compiler can directly take these `.obj/.o` files as input for subsequent linking processes.

> **NOTE：**
>
> This is an experimental feature with potential risks, and it must be used in conjunction with the `--experimental` option.

For example, the following commands implement step-by-step compilation and linking to generate an executable file:

```cangjie
// main.cj
main(){
  println("hello cangjie")
}
```

```shell
# Specify --output-type as obj and explicitly set --compile-target to exe
cjc main.cj --output-type=obj --experimental -o main.o --compile-target=exe 

# Link the intermediate product into an executable file
cjc main.o -lcangjie-std-core -o main --experimental
```

In Step 2, the parameter -lcangjie-std-core is used to specify the standard library dependencies required during the compilation process. In manual linking scenarios, the naming of dependent libraries must strictly conform to the prescribed naming convention(e.g., -lcangjie-std-math, -lcangjie-std-collection.concurrent, etc.). Failure to comply with this naming convention will result in undefined symbol errors.

**Critical Notes**:

1. This option does not support scenarios where `a .o` file is used as the input while the `--output-type=obj` option is specified again.Invalid usage example: `cjc main.o --output-type=obj --compile-target=exe`.
2. When `--output-type` is set to a non-obj type, the `--compile-target` option will not take effect (and will be ignored).Invalid usage example: `cjc main.cj --output-type=exe --compile-target=dylib`.
3. If the input file is solely `a .o` intermediate target file, the `--output-type` configured in the current step (with a default value of exe) must be logically consistent with the `--compile-target` specified when generating the `.o` file. For instance, if `a.o` file is compiled with `--compile-target=dylib` (intended for dynamic library generation), then `--output-type` should also be set to dylib during the linking phase. Otherwise, linking failures or mismatches in product types may occur.


### `--package`, `-p` <sup>[frontend]</sup>

Compiles a package. When using this option, a directory must be specified as input, and the source files in the directory must belong to the same package.

Assume there is a file `log/printer.cj`:

```cangjie
package log

public func printLog(message: String) {
    println("[Log]: ${message}")
}
```

And a file `main.cj`:

```cangjie
import log.*

main() {
    printLog("Everything is great")
}
```

The following command can be used to compile the `log` package:

```shell
$ cjc -p log --output-type=staticlib
```

`cjc` will generate a `liblog.a` file in the current directory.

The `liblog.a` file can then be used to compile `main.cj` as follows:

```shell
$ cjc main.cj liblog.a
```

`cjc` will compile `main.cj` and `liblog.a` together into an executable file named `main`.

### `--module-name <value>` <sup>[frontend]</sup>

Specifies the name of the module to be compiled.

Assume there is a file `my_module/src/log/printer.cj`:

```cangjie
package log

public func printLog(message: String) {
    println("[Log]: ${message}")
}
```

And a file `main.cj`:

```cangjie
import my_module.log.*

main() {
    printLog("Everything is great")
}
```

The following command can be used to compile the `log` package with the module name set to `my_module`:

```shell
$ cjc -p my_module/src/log --module-name my_module --output-type=staticlib -o my_module/liblog.a
```

`cjc` will generate a `my_module/liblog.a` file in the `my_module` directory.

The `liblog.a` file can then be used to compile `main.cj`, which imports the `log` package:

```shell
$ cjc main.cj my_module/liblog.a
```

`cjc` will compile `main.cj` and `liblog.a` together into an executable file named `main`.

### `--output <value>`, `-o <value>`, `-o<value>` <sup>[frontend]</sup>

Specifies the output file path. The compiler's output will be written to the specified file.

For example, the following command sets the output executable file name to `a.out`:

```shell
cjc main.cj -o a.out
```

### `--library <value>`, `-l <value>`, `-l<value>`

Specifies the library file to link.

The given library file will be directly passed to the linker. This option is typically used in conjunction with `--library-path <value>`.

The filename format should be `lib[arg].[extension]`. When linking library `a`, the option `-l a` can be used. The linker will search for files like `liba.a`, `liba.so` (or `liba.dll` when targeting Windows) in the library search directories and link them as needed.

### `--library-path <value>`, `-L <value>`, `-L<value>`

Specifies the directory containing the library files to link.

When using `--library <value>`, this option is typically also needed to specify the directory containing the library files.

The paths specified by `--library-path <value>` will be added to the linker's library search paths. Additionally, paths specified in the `LIBRARY_PATH` environment variable will also be included. Paths specified via `--library-path` take precedence over those in `LIBRARY_PATH`.

Assume there is a dynamic library file `libcProg.so` compiled from the following C source file:

```c
#include <stdio.h>

void printHello() {
    printf("Hello World\n");
}
```

And a Cangjie file `main.cj`:

```cangjie
foreign func printHello(): Unit

main(): Int64 {
  unsafe {
    printHello()
  }
  return 0
}
```

The following command can be used to compile `main.cj` and link the `cProg` library:

```shell
cjc main.cj -L . -l cProg
```

`cjc` will output an executable file named `main`.

Running `main` will produce the following output:

```shell
$ LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main
Hello World
```

**Note:** Since a dynamic library is used, the library directory must be added to `$LD_LIBRARY_PATH` to ensure dynamic linking at runtime.

### `-g` <sup>[frontend]</sup>

Generates an executable or library file with debug information.

> **Note:**
>
> `-g` can only be used with `-O0`. Higher optimization levels may cause debugging features to malfunction.

### `--trimpath <value>` <sup>[frontend]</sup>

Removes the specified prefix from source file path information in debug info.

When compiling Cangjie code, `cjc` saves the absolute paths of source files (`.cj` files) to provide debugging and exception information at runtime.

This option removes the specified path prefix from the source file path information. The output file will not include the user-specified prefix in the source file paths.

Multiple `--trimpath` options can be used to specify different prefixes. For each source file path, the compiler removes the first matching prefix.

### `--coverage` <sup>[frontend]</sup>

Generates an executable program that supports code coverage statistics. The compiler generates a `.gcno` file for each compilation unit. After execution, each compilation unit generates a `.gcda` file containing execution statistics. Using these files with the `cjcov` tool can generate a code coverage report for the execution.

> **Note:**
>
> `--coverage` can only be used with `-O0`. If a higher optimization level is specified, the compiler will issue a warning and force `-O0`. `--coverage` is for compiling executables. If used for static or dynamic libraries, linking errors may occur when the library is used.

### `--int-overflow=[throwing|wrapping|saturating]` <sup>[frontend]</sup>

Specifies the overflow strategy for fixed-precision integer operations. Defaults to `throwing`.

- `throwing`: Throws an exception on integer overflow.
- `wrapping`: Wraps around to the other end of the fixed-precision integer range on overflow.
- `saturating`: Clamps to the extreme value of the fixed-precision range on overflow.

### `--diagnostic-format=[default|noColor|json]` <sup>[frontend]</sup>

> **Note:**
>
> The Windows version does not currently support colored error messages.

Specifies the output format for error messages. Defaults to `default`.

- `default`: Error messages in default format (with color).
- `noColor`: Error messages in default format (without color).
- `json`: Error messages in JSON format.

### `--verbose`, `-V` <sup>[frontend]</sup>

`cjc` will print compiler version information, toolchain dependency details, and commands executed during compilation.

### `--help`, `-h` <sup>[frontend]</sup>

Prints available compilation options.

When this option is used, the compiler only prints compilation option information and does not compile any input files.

### `--version`, `-v` <sup>[frontend]</sup>

Prints compiler version information.

When this option is used, the compiler only prints version information and does not compile any input files.

### `--save-temps <value>`

Retains intermediate files generated during compilation and saves them to the specified `<value>` path.

The compiler retains intermediate files like `.bc` and `.o` generated during compilation.

### `--import-path <value>` <sup>[frontend]</sup>

Specifies the search path for AST files of imported modules.

> **Note:** For details about CJO files, refer to [CJO Artifacts Documentation](cjo_artifacts.md).

Assume the following directory structure, where the `libs/myModule` directory contains library files for the `myModule` module and AST export files for the `log` package:

```text
.
├── libs
|   └── myModule
|       ├── log.cjo
|       └── libmyModule.a
└── main.cj
```

And the following `main.cj` file:

```cangjie
import myModule.log.printLog

main() {
    printLog("Everything is great")
}
```

By using `--import-path ./libs`, `./libs` is added to the AST file search path for imported modules. `cjc` will use the `./libs/myModule/log.cjo` file for semantic checking and compilation of `main.cj`.

`--import-path` provides the same functionality as the `CANGJIE_PATH` environment variable, but paths specified via `--import-path` take precedence.

### `--scan-dependency` <sup>[frontend]</sup>

The `--scan-dependency` command retrieves direct dependencies and other information for a specified package's source code or a package's `cjo` file, outputting the results in JSON format.

> **Note:** For details about CJO files, refer to [CJO Artifacts Documentation](cjo_artifacts.md).

```cangjie
// this file is placed under directory pkgA
macro package pkgA
import pkgB.*
import std.io.*
import pkgB.subB.*
```

```shell
cjc --scan-dependency --package pkgA
```

Or:

```shell
cjc --scan-dependency pkgA.cjo
```

```json
{
  "package": "pkgA",
  "isMacro": true,
  "dependencies": [
    {
      "package": "pkgB",
      "isStd": false,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 2,
            "column": 1
          },
          "end": {
            "line": 2,
            "column": 14
          }
        }
      ]
    },
    {
      "package": "pkgB.subB",
      "isStd": false,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 4,
            "column": 1
          },
          "end": {
            "line": 4,
            "column": 19
          }
        }
      ]
    },
    {
      "package": "std.io",
      "isStd": true,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 3,
            "column": 1
          },
          "end": {
            "line": 3,
            "column": 16
          }
        }
      ]
    }
  ]
}
```

### `--no-sub-pkg` <sup>[frontend]</sup>

Indicates that the current compilation package has no sub-packages.

Enabling this option allows the compiler to further reduce code size.

### `--warn-off`, `-Woff <value>` <sup>[frontend]</sup>

Disables all or specific categories of compilation warnings.

`<value>` can be `all` or a predefined warning category. When set to `all`, the compiler suppresses all warnings during compilation. When set to a specific category, the compiler suppresses warnings of that category.

Each warning includes a `#note` line indicating its category and how to disable it. Use `--help` to list all available compilation options and their categories.

### `--warn-on`, `-Won <value>` <sup>[frontend]</sup>

Enables all or specific categories of compilation warnings.

`<value>` for `--warn-on` has the same range as for `--warn-off`. `--warn-on` is typically used with `--warn-off`. For example, `-Woff all -Won <value>` enables only warnings of the specified category.

**Important:** The order of `--warn-on` and `--warn-off` matters. For the same category, the latter option overrides the former. For example, reversing the order to `-Won <value> -Woff all` would suppress all warnings.

### `--error-count-limit <value>` <sup>[frontend]</sup>

Limits the maximum number of errors the compiler will print.

`<value>` can be `all` or a non-negative integer. When set to `all`, the compiler prints all errors during compilation. When set to an integer `N`, the compiler prints at most `N` errors. The default value is 8.

### `--output-dir <value>` <sup>[frontend]</sup>

Controls the directory where the compiler saves intermediate and final output files.

Controls the directory for intermediate files like `.cjo`. If both `--output-dir <path1>` and `--output <path2>` are specified, intermediate files are saved to `<path1>`, and the final output is saved to `<path1>/<path2>`.

> **Note:**
>
> When this option is used with `--output`, the `--output` parameter must be a relative path.

### `--static`

Statically links the Cangjie library.

This option only takes effect when compiling executables.

**Note:**

The `--static` option is only applicable on Linux and has no effect on other platforms.

### `--static-std`

Statically link the std module of the Cangjie library.

This option only takes effect when compiling dynamic libraries or executable files.

When compiling executable programs (i.e., when `--output-type=exe` is specified), `cjc` statically links the std module of the Cangjie library by default.

### `--dy-std`

Dynamically link the std module of the Cangjie library.

This option only takes effect when compiling dynamic libraries or executable files.

When compiling dynamic libraries (i.e., when `--output-type=dylib` is specified), `cjc` dynamically links the std module of the Cangjie library by default.

**Important Notes:**

1. If both `--static-std` and `--dy-std` options are used, only the last one takes effect.
2. `--dy-std` cannot be used with the `--static-libs` option; otherwise, an error will occur.
3. When compiling an executable program that links to a Cangjie dynamic library (i.e., a product compiled with the `--output-type=dylib` option), you must explicitly specify the `--dy-std` option to dynamically link the standard library. Otherwise, multiple copies of the standard library may appear in the program, potentially causing runtime issues.

### `--static-libs`

Statically link modules other than std and the runtime module in the Cangjie library.

This option only takes effect when compiling dynamic libraries or executable files. By default, `cjc` statically links modules other than std and the runtime module in the Cangjie library.

### `--dy-libs`

Dynamically link non-std modules in the Cangjie library.

This option only takes effect when compiling dynamic libraries or executable files.

**Important Notes:**

1. If both `--static-libs` and `--dy-libs` options are used, only the last one takes effect.
2. `--static-std` cannot be used with the `--dy-libs` option; otherwise, an error will occur.
3. When `--dy-std` is used alone, the `--dy-libs` option is enabled by default, and a warning message will be displayed.
4. When `--dy-libs` is used alone, the `--dy-std` option is enabled by default, and a warning message will be displayed.
5. Platform support capabilities are as follows:

| Target Platform | Static Linking | Dynamic Linking |
| :-------------: | :------------: | :-------------: |
|      Linux      |    Supported   |    Supported    |
|      macOS      |    Supported   |    Supported    |
|     Windows     |    Supported   |    Supported    |
|  OpenHarmony  |  Not Supported |    Supported    |


### `--stack-trace-format=[default|simple|all]`

Specifies the exception stack trace printing format, which controls the display of stack frame information when an exception is thrown. The default format is `default`.

The stack trace formats are described as follows:

- `default` format: `Function name with generic parameters omitted (filename:line number)`
- `simple` format: `filename:line number`
- `all` format: `Full function name (filename:line number)`

### `--lto=[full|thin]`

Enables and specifies the `LTO` (`Link Time Optimization`) compilation mode.

**Important Notes:**

1. This feature is not supported on `Windows` or `macOS` platforms.
2. When `LTO` is enabled, the following optimization compilation options cannot be used simultaneously: `-Os`, `-Oz`.

`LTO` supports two compilation modes:

- `--lto=full`: `Full LTO` merges all compilation modules together and performs global optimization. This mode offers the highest optimization potential but requires longer compilation time.
- `--lto=thin`: Compared to `full LTO`, `thin LTO` uses parallel optimization across multiple modules and supports incremental linking by default. It has shorter compilation time than `full LTO` but less optimization effectiveness due to reduced global information.

    - Typical optimization effectiveness comparison: `full LTO` **>** `thin LTO` **>** regular static linking compilation.
    - Typical compilation time comparison: `full LTO` **>** `thin LTO` **>** regular static linking compilation.

`LTO` usage scenarios:

1. Compile an executable file using the following commands:

    ```shell
    $ cjc test.cj --lto=full
    or
    $ cjc test.cj --lto=thin
    ```

2. Compile a static library (`.bc` file) required for `LTO` mode and use it to compile an executable file:

    ```shell
    # Generate a static library as a .bc file
    $ cjc pkg.cj --lto=full --output-type=staticlib -o libpkg.bc
    # Compile the executable file with the .bc file and source file
    $ cjc test.cj libpkg.bc --lto=full
    ```

    > **Note:**
    >
    > In `LTO` mode, the path to the static library (`.bc` file) must be provided to the Cangjie compiler.

3. In `LTO` mode, when statically linking the standard library (`--static-std` & `--static-libs`), the standard library code participates in `LTO` optimization and is statically linked into the executable. When dynamically linking the standard library (`--dy-std` & `--dy-libs`), the dynamic library of the standard library is used for linking even in `LTO` mode.

    ```shell
    # Static linking: Standard library code participates in LTO optimization
    $ cjc test.cj --lto=full --static-std
    # Dynamic linking: Dynamic library is used for linking; standard library code does not participate in LTO optimization
    $ cjc test.cj --lto=full --dy-std
    ```

### `--compile-as-exe`

This option hides the visibility of symbols in bc files loaded in `LTO` mode, retaining only the visibility of the `package init` symbol. Based on this, LLVM's native optimization performs aggressive dead symbol elimination. This option only takes effect when `--lto` is enabled.

```shell
# Compilation succeeds
$ cjc test.cj --lto=[full|thin] --compile-as-exe
# Compilation fails
$ cjc test.cj --compile-as-exe
```

### `--pgo-instr-gen`, `--pgo-instr-gen=<.profraw>`

Enables instrumentation compilation, generating an executable program with instrumentation information.

- If `<.profraw>` is provided, profile information will be written to the specified path file.
- If `<.profraw>` is not provided, profile information will be written to `default.profraw` in the current directory where the Cangjie program is executed.

This feature is temporarily unsupported when compiling for macOS or Windows targets.

`PGO` (`Profile-Guided Optimization`) is a common compilation optimization technique that uses runtime profiling information to further improve program performance. `Instrumentation-based PGO` is a `PGO` optimization method that uses instrumentation information and typically involves three steps:

1. The compiler performs instrumentation compilation on the source code, generating an instrumented executable program.
2. Run the instrumented executable program to generate a profile.
3. The compiler uses the profile to recompile the source code.

```shell
# Generate an executable program `test` with instrumentation information
$ cjc test.cj --pgo-instr-gen -o test
# Run the executable program `test` to generate the `default.profraw` profile
$ ./test

# Generate an executable program `test` with instrumentation information and specific profile file path and name
$ cjc test.cj --pgo-instr-gen=./cjpgo/cj.profraw -o test
# Run the executable program `test` to generate the `./cjpgo/cj.profraw` profile
$ ./test
```

### `--pgo-instr-use=<.profdata>`

Uses the specified `profdata` profile to guide compilation and generate an optimized executable program.

This feature is temporarily unsupported when compiling for macOS targets.

> **Note:**
>
> The `--pgo-instr-use` compilation option only supports profiles in `profdata` format. The `llvm-profdata` tool can be used to convert `profraw` profiles to `profdata` profiles.

```shell
# Convert `profraw` file to `profdata` file
$ LD_LIBRARY_PATH=$CANGJIE_HOME/third_party/llvm/lib:$LD_LIBRARY_PATH $CANGJIE_HOME/third_party/llvm/bin/llvm-profdata merge default.profraw -o default.profdata
# Use the specified `default.profdata` profile to guide compilation and generate the optimized executable program `testOptimized`
$ cjc test.cj --pgo-instr-use=default.profdata -o testOptimized
```

### `--target <value>` <sup>[frontend]</sup>

Specifies the target platform triple for compilation.

The `<value>` parameter is generally a string in the following format: `<arch>(-<vendor>)-<os>(-<env>)`. Here:

- `<arch>` represents the system architecture of the target platform, e.g., `aarch64`, `x86_64`, etc.
- `<vendor>` represents the vendor of the target platform, e.g., `apple`. If the vendor is unspecified or unimportant, it is often written as `unknown` or omitted.
- `<os>` represents the operating system of the target platform, e.g., `Linux`, `Win32`, etc.
- `<env>` represents the ABI or standard specification of the target platform, used to distinguish different runtime environments of the same OS, e.g., `gnu`, `musl`. If the OS does not require finer distinctions based on `<env>`, this can also be omitted.

Currently, `cjc` supports the following host and target platforms for cross-compilation:

| Host Platform       | Target Platform          | Supported Packages |
| ------------------- | ------------------------ | ------------------ |
| x86_64-linux-gnu    | x86_64-windows-gnu       | cangjie-sdk-linux-x64-x.y.z.tar.gz |
| x86_64-linux-gnu   | aarch64-linux-android26     | cangjie-sdk-linux-x64-android-x.y.z.tar.gz |
| aarch64-linux-gnu   | x86_64-windows-gnu       | cangjie-sdk-linux-aarch64.x.y.z.tar.gz |
| x86_64-apple-darwin | aarch64-linux-android26  | cangjie-sdk-mac-x64-android.x.y.z.tar.gz |
| aarch64-apple-darwin | aarch64-linux-android26 | cangjie-sdk-mac-aarch64-android.x.y.z.tar.gz |
| aarch64-apple-darwin | aarch64-apple-ios       | cangjie-sdk-mac-aarch64-ios.x.y.z.tar.gz |
| x86_64-windows-gnu | aarch64-linux-android26 | cangjie-sdk-windows-x64-android.x.y.z.tar.gz |
| aarch64-apple-darwin | aarch64-apple-ios-simulator | cangjie-sdk-mac-aarch64-ios.x.y.z.tar.gz |
| aarch64-apple-darwin | x86_64-apple-ios-simulator | cangjie-sdk-mac-aarch64-ios.x.y.z.tar.gz
Before using `--target` to specify a target platform for cross-compilation, ensure that the corresponding cross-compilation toolchain and the Cangjie SDK version for the target platform are prepared.

### `--target-cpu <value>`

> **Note:**
>
> This option is experimental. Binaries generated using this option may have potential runtime issues. Use this option with caution. This option must be used with the `--experimental` option.

Specifies the CPU type of the compilation target.

When specifying the CPU type, the compiler attempts to use the CPU-specific instruction set extensions and apply optimizations tailored for that CPU type. Binaries generated for a specific CPU type may lose portability and might not run on other CPUs (even with the same architecture instruction set).

This option supports the following tested CPU types:

**x86-64 Architecture:**

- generic

**aarch64 Architecture:**

- generic
- tsv110

`generic` is the universal CPU type. When `generic` is specified, the compiler generates universal instructions for the architecture, ensuring the binary can run on various CPUs of the same architecture (assuming the OS and dynamic dependencies are consistent). The default value for `--target-cpu` is `generic`.

This option also supports the following CPU types, but they are untested. Binaries generated for these CPU types may have runtime issues.

**x86-64 Architecture:**

- alderlake
- amdfam10
- athlon
- athlon-4
- athlon-fx
- athlon-mp
- athlon-tbird
- athlon-xp
- athlon64
- athlon64-sse3
- atom
- barcelona
- bdver1
- bdver2
- bdver3
- bdver4
- bonnell
- broadwell
- btver1
- btver2
- c3
- c3-2
- cannonlake
- cascadelake
- cooperlake
- core-avx-i
- core-avx2
- core2
- corei7
- corei7-avx
- geode
- goldmont
- goldmont-plus
- haswell
- i386
- i486
- i586
- i686
- icelake-client
- icelake-server
- ivybridge
- k6
- k6-2
- k6-3
- k8
- k8-sse3
- knl
- knm
- lakemont
- nehalem
- nocona
- opteron
- opteron-sse3
- penryn
- pentium
- pentium-m
- pentium-mmx
- pentium2
- pentium3
- pentium3m
- pentium4
- pentium4m
- pentiumpro
- prescott
- rocketlake
- sandybridge
- sapphirerapids
- silvermont
- skx
- skylake
- skylake-avx512
- slm
- tigerlake
- tremont
- westmere
- winchip-c6
- winchip2
- x86-64
- x86-64-v2
- x86-64-v3
- x86-64-v4
- yonah
- znver1
- znver2
- znver3

**aarch64 Architecture:**

- a64fx
- ampere1
- apple-a10
- apple-a11
- apple-a12
- apple-a13
- apple-a14
- apple-a7
- apple-a8
- apple-a9
- apple-latest
- apple-m1
- apple-s4
- apple-s5
- carmel
- cortex-a34
- cortex-a35
- cortex-a510
- cortex-a53
- cortex-a55
- cortex-a57
- cortex-a65
- cortex-a65ae
- cortex-a710
- cortex-a72
- cortex-a73
- cortex-a75
- cortex-a76
- cortex-a76ae
- cortex-a77
- cortex-a78
- cortex-a78c
- cortex-r82
- cortex-x1
- cortex-x1c
- cortex-x2
- cyclone
- exynos-m3
- exynos-m4
- exynos-m5
- falkor
- kryo
- neoverse-512tvb
- neoverse-e1
- neoverse-n1
- neoverse-n2
- neoverse-v1
- saphira
- thunderx
- thunderx2t99
- thunderx3t110
- thunderxt81
- thunderxt83
- thunderxt88

In addition to the above CPU types, this option also supports `native` as the current CPU type. The compiler attempts to identify the current machine's CPU type and uses it as the target type for generating binaries.

### `--toolchain <value>`, `-B <value>`, `-B<value>`

Specifies the path to the binary files in the compilation toolchain.

These binary files include the compiler, linker, and C runtime target files (e.g., `crt0.o`, `crti.o`) provided by the toolchain.

After preparing the compilation toolchain, you can place it in a custom path and pass this path to the compiler using `--toolchain <value>`, allowing the compiler to invoke the binaries in this path for cross-compilation.

### `--sysroot <value>`

Specifies the root directory path of the compilation toolchain.

For cross-compilation toolchains with fixed directory structures, if there is no need to specify paths outside this directory for binaries and dynamic/static library files, you can directly use `--sysroot <value>` to pass the toolchain's root directory path to the compiler. The compiler will analyze the corresponding directory structure based on the target platform and automatically search for the required binary files and dynamic/static library files. Using this option eliminates the need to specify `--toolchain` or `--library-path` parameters.

For cross-compilation to a platform with the `triple` `arch-os-env`, if the cross-compilation toolchain has the following directory structure:

```text
/usr/sdk/arch-os-env
├── bin
|   ├── arch-os-env-gcc (cross-compiler)
|   ├── arch-os-env-ld  (linker)
|   └── ...
├── lib
|   ├── crt1.o          (C runtime target file)
|   ├── crti.o
|   ├── crtn.o
|   ├── libc.so         (dynamic library)
|   ├── libm.so
|   └── ...
└── ...
```

For the Cangjie source file `hello.cj`, you can use the following command to cross-compile `hello.cj` to the `arch-os-env` platform:

```shell
cjc --target=arch-os-env --toolchain /usr/sdk/arch-os-env/bin --toolchain /usr/sdk/arch-os-env/lib --library-path /usr/sdk/arch-os-env/lib hello.cj -o hello
```

Alternatively, you can use the shorthand parameters:

```shell
cjc --target=arch-os-env -B/usr/sdk/arch-os-env/bin -B/usr/sdk/arch-os-env/lib -L/usr/sdk/arch-os-env/lib hello.cj -o hello
```

If the toolchain's directory follows conventional structures, you can omit the `--toolchain` and `--library-path` parameters and use the following command directly:

```shell
cjc --target=arch-os-env --sysroot /usr/sdk/arch-os-env hello.cj -o hello
```

### `--strip-all`, `-s`

When compiling an executable file or dynamic library, specifying this option removes the symbol table from the output file.

### `--discard-eh-frame`

When compiling an executable file or dynamic library, specifying this option removes part of the information from the `eh_frame` and `eh_frame_hdr` segments (information related to `crt` is not processed), reducing the size of the executable or dynamic library but affecting debugging information.

This feature is temporarily unsupported when compiling for macOS targets.

### `--set-runtime-rpath`

Writes the absolute path of the Cangjie runtime library directory into the RPATH/RUNPATH section of the binary. When this option is used, there is no need to set the Cangjie runtime library directory using `LD_LIBRARY_PATH` (for Linux platforms) or `DYLD_LIBRARY_PATH` (for macOS platforms) when running the Cangjie program in the build environment.

This feature is not supported when compiling for Windows targets.

### `--link-option <value>`<sup>1</sup>

Specifies linker options.

`cjc` will pass the value of this option as a parameter directly to the linker. The available parameters vary depending on the linker (system or specified). The `--link-option` can be used multiple times to specify multiple linker options.

### `--link-options <value>`<sup>1</sup>

Specifies linker options.

`cjc` will pass multiple parameters of this option directly to the linker, with parameters separated by spaces. The available parameters vary depending on the linker (system or specified). The `--link-options` can be used multiple times to specify multiple linker options.

<sup>1</sup> Superscript indicates that linker passthrough options may vary depending on the linker. For specific supported options, please refer to the linker documentation.

### `--disable-reflection`

Disables the reflection option, meaning no related reflection information will be generated during compilation.

> **Note:**
>
> When cross-compiling to the `aarch64-linux-ohos` target, reflection information is disabled by default, and this option has no effect.

### `--profile-compile-time` <sup>[frontend]</sup>

Prints time consumption data for each compilation phase.

### `--profile-compile-memory` <sup>[frontend]</sup>

Prints memory consumption data for each compilation phase.

### --sanitize=[address|thread|hwsaddress]

Enables the Sanitizer compile-time instrumentation feature, detects various errors in the program during runtime, and links the corresponding Sanitizer runtime libraries. Prior to using this option, you need to download the dedicated SDK package with Sanitizer support (e.g., cangjie-sdk-linux-aarch64-sanitizer.tar.gz) and ensure the proper deployment of the SDK.

- `--sanitize=address` Detects memory errors, corresponding to the cangjie/runtime/lib/linux_aarch64_cjnative/asan directory in the SDK.
- `--sanitize=thread` Detects data races, corresponding to the cangjie/runtime/lib/linux_aarch64_cjnative/tsan/tsan directory in the SDK.
- `--sanitize=hwaddress` Detects illegal hardware-level memory access behaviors, corresponding to the cangjie/runtime/lib/linux_aarch64_cjnative/hwasan directory in the SDK.

Usage Examples:

```shell
cjc --sanitize=address main.cj -o main

# Manually specify the runtime library path
export LD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/arch/<sanitizer-name>:$LD_LIBRARY_PATH

# Run the program
./main
```

> **Note:**
>
> The `--sanitize` option cannot be used in conjunction with the `--compile-macro` option; otherwise, a compilation error will be triggered.

### --sanitize-set-rpath

This option automatically configures the search path for the corresponding Sanitizer runtime libraries, eliminating the need for users to execute an additional `export LD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/arch/[asan|tsan|hwasan]:$LD_LIBRARY_PATH` command. 
For example, the above compilation command can be simplified to:

```shell
cjc --sanitize=address main.cj -o main --sanitize-set-rpath
```

## Unit Test Options

### `--test` <sup>[frontend]</sup>

The entry point provided by the `unittest` testing framework, automatically generated by macros. When compiling with the `cjc --test` option, the program entry is no longer `main` but `test_entry`. For usage of the unittest framework, refer to the *Cangjie Programming Language Standard Library API* documentation.

For the Cangjie file `a.cj` in the `pkgc` directory:
<!-- run -->

```cangjie
import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestA {
    @TestCase
    public func case1(): Unit {
        print("case1\n")
    }
}
```

You can use the following command in the `pkgc` directory:

```shell
cjc a.cj --test
```

to compile `a.cj`. Executing `main` will produce the following output:

> **Note:**
>
> The execution time of test cases is not guaranteed to be consistent across runs.

```cangjie
case1
--------------------------------------------------------------------------------------------------
TP: default, time elapsed: 29710 ns, Result:
    TCS: TestA, time elapsed: 26881 ns, RESULT:
    [ PASSED ] CASE: case1 (16747 ns)
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

For the following directory structure:

```text
application
├── src
├── pkgc
|   ├── a1.cj
|   └── a2.cj
└── a3.cj
```

You can use the `-p` compilation option in the `application` directory to compile the entire package:

```shell
cjc pkgc --test -p
```

This will compile all test cases (`a1.cj` and `a2.cj`) in the `pkgc` package.

```cangjie
/*a1.cj*/
package a

import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestA {
    @TestCase
    public func caseA(): Unit {
        print("case1\n")
    }
}
```

```cangjie
/*a2.cj*/
package a

import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestB {
    @TestCase
    public func caseB(): Unit {
        throw IndexOutOfBoundsException()
    }
}
```

Executing `main` will produce the following output (**output is for reference only**):

```cangjie
case1
--------------------------------------------------------------------------------------------------
TP: a, time elapsed: 367800 ns, Result:
    TCS: TestA, time elapsed: 16802 ns, RESULT:
    [ PASSED ] CASE: caseA (14490 ns)
    TCS: TestB, time elapsed: 347754 ns, RESULT:
    [ ERROR  ] CASE: caseB (345453 ns)
    REASON: An exception has occurred:IndexOutOfBoundsException
        at std/core.Exception::init()(std/core/exception.cj:23)
        at std/core.IndexOutOfBoundsException::init()(std/core/index_out_of_bounds_exception.cj:9)
        at a.TestB::caseB()(/home/houle/cjtest/application/pkgc/a2.cj:7)
        at a.lambda.1()(/home/houle/cjtest/application/pkgc/a2.cj:7)
        at std/unittest.TestCases::execute()(std/unittest/test_case.cj:92)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:194)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:78)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:200)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:78)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:200)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:75)
        at std/unittest.entryMain(std/unittest::TestPackage)(std/unittest/entry_main.cj:11)
Summary: TOTAL: 2
    PASSED: 1, SKIPPED: 0, ERROR: 1
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

### `--test-only` <sup>[frontend]</sup>

The `--test-only` option is used to compile only the test portion of a package.

When this option is enabled, the compiler will only compile test files (those ending with `_test.cj`) in the package.

> **Note:**
>
> When using this option, the same package should first be compiled in regular mode, and dependencies should be added via the `-L`/`-l` linking options or by including the `.bc` files when using the `LTO` option. Otherwise, the compiler will report missing dependency symbols.

Example:

```cangjie
/*main.cj*/
package my_pkg

func concatM(s1: String, s2: String): String {
    return s1 + s2
}

main() {
    println(concatM("a", "b"))
    0
}
```

```cangjie
/*main_test.cj*/
package my_pkg

@Test
class Tests {
    @TestCase
    public func case1(): Unit {
        @Expect("ac", concatM("a", "c"))
    }
}
```

The compilation commands are as follows:

```shell
# Compile the production part of the package first, only `main.cj` file would be compiled here
cjc -p my_pkg --output-type=static -o=output/libmain.a
# Compile the test part of the package, Only `main_test.cj` file would be compiled here
cjc -p my_pkg --test-only -L output -lmain
```

### `--mock <on|off|runtime-error>` <sup>[frontend]</sup>

If `on` is passed, the package will enable mock compilation, allowing classes in the package to be mocked in test cases. `off` is an explicit way to disable mocking.

> **Note:**
>
> Mock support is automatically enabled in test mode (when `--test` is enabled), and there is no need to explicitly pass the `--mock` option.

`runtime-error` is only available in test mode (when `--test` is enabled). It allows compiling packages with mock code but does not perform any mock-related processing in the compiler (which may introduce overhead and affect test runtime performance). This can be useful when benchmarking test cases with mock code. When using this compilation option, avoid compiling and running tests with mock code, as it will throw runtime exceptions.

## Macro Options

`cjc` supports the following macro options. For more details about macros, refer to the ["Introduction to Macros"](../Macro/macro_introduction.md) chapter.

### `--compile-macro` <sup>[frontend]</sup>

Compile macro definition files to generate default macro definition dynamic library files.

### `--debug-macro` <sup>[frontend]</sup>

Generate Cangjie code files after macro expansion. This option can be used to debug macro expansion functionality.

### `--parallel-macro-expansion` <sup>[frontend]</sup>

Enable parallel macro expansion. This option can be used to reduce macro expansion compilation time.

## Conditional Compilation Options

`cjc` supports the following conditional compilation options. For more details about conditional compilation, refer to the ["Conditional Compilation"](../compile_and_build/conditional_compilation.md) chapter.

### `--cfg <value>` <sup>[frontend]</sup>

Specify custom compilation conditions.

## Parallel Compilation Options

`cjc` supports the following parallel compilation options to achieve higher compilation efficiency.

### `--jobs <value>`, `-j <value>` <sup>[frontend]</sup>

Set the maximum number of parallel jobs allowed during parallel compilation. `value` must be a reasonable non-negative integer. If `value` exceeds the hardware's maximum parallel capability, the compiler will use the hardware's maximum parallel capability.

If this option is not set, the compiler will automatically calculate the maximum number of parallel jobs based on hardware capabilities.

> **Note:**
>
> `--jobs 1` means compilation will be performed entirely serially.

### `--aggressive-parallel-compile`, `--apc`, `--aggressive-parallel-compile=<value>`, `--apc=<value>` <sup>[frontend]</sup>

When enabled, the compiler will adopt a more aggressive strategy (which may impact optimizations and reduce program runtime performance) to achieve higher compilation efficiency. `value` is an optional parameter indicating the maximum number of parallel jobs for aggressive parallel compilation:

- If `value` is provided, it must be a reasonable non-negative integer. If `value` exceeds the hardware's maximum parallel capability, the compiler will automatically calculate the maximum number of parallel jobs based on hardware capabilities. It is recommended to set `value` to a non-negative integer less than the number of physical CPU cores.
- If `value` is not provided, aggressive parallel compilation is enabled by default, and the number of parallel jobs matches `--jobs`.

Additionally, if the same code is compiled twice with different `value` settings or different states of this option, the compiler does not guarantee binary consistency between the outputs.

Rules for enabling/disabling aggressive parallel compilation:

- Aggressive parallel compilation will be forcibly disabled by the compiler in the following scenarios:

    - `--fobf-string`
    - `--fobf-const`
    - `--fobf-layout`
    - `--fobf-cf-flatten`
    - `--fobf-cf-bogus`
    - `--lto`
    - `--coverage`
    - Compiling for Windows targets
    - Compiling for macOS targets

- If `--aggressive-parallel-compile=<value>` or `--apc=<value>` is used, the state of aggressive parallel compilation is controlled by `value`:

    - `value <= 1`: Disable aggressive parallel compilation.
    - `value > 1`: Enable aggressive parallel compilation, with the number of parallel jobs determined by `value`.

- If `--aggressive-parallel-compile` or `--apc` is used, aggressive parallel compilation is enabled by default, and the number of parallel jobs matches `--jobs`.

- If this option is not set, the compiler will enable or disable aggressive parallel compilation by default based on the scenario:

    - `-O0`: Aggressive parallel compilation is enabled by default, and the number of parallel jobs matches `--jobs`. It can be disabled by specifying `--aggressive-parallel-compile=<value>` or `--apc=<value>` with `value <= 1`.
    - Non-`-O0`: Aggressive parallel compilation is disabled by default. To enable it, specify `--aggressive-parallel-compile=<value>` or `--apc=<value>` with `value > 1`, or directly specify the `--apc` option.

## Optimization Options

### `--fchir-constant-propagation` <sup>[frontend]</sup>

Enable CHIR constant propagation optimization.

### `--fno-chir-constant-propagation` <sup>[frontend]</sup>

Disable CHIR constant propagation optimization.

### `--fchir-function-inlining` <sup>[frontend]</sup>

Enable CHIR function inlining optimization.

### `--fno-chir-function-inlining` <sup>[frontend]</sup>

Disable CHIR function inlining optimization.

### `--fchir-devirtualization` <sup>[frontend]</sup>

Enable CHIR devirtualization optimization.

### `--fno-chir-devirtualization` <sup>[frontend]</sup>

Disable CHIR devirtualization optimization.

### `--fast-math` <sup>[frontend]</sup>

When enabled, the compiler will make aggressive (and potentially precision-losing) assumptions about floating-point operations to optimize them.

### `-O<N>` <sup>[frontend]</sup>

Use the specified code optimization level.

Higher optimization levels will result in more aggressive code optimizations to generate more efficient programs, but may also require longer compilation times.

`cjc` uses O0-level optimization by default. Currently, `cjc` supports the following optimization levels: O0, O1, O2, Os, Oz.

When the optimization level is 2, `cjc` will perform the corresponding optimizations and also enable the following options:

- `--fchir-constant-propagation`
- `--fchir-function-inlining`
- `--fchir-devirtualization`

When the optimization level is s, `cjc` will perform O2-level optimizations and additionally optimize for code size.

When the optimization level is z, `cjc` will perform Os-level optimizations and further reduce code size.

> **Note:**
>
> When the optimization level is s or z, the link-time optimization option `--lto=[full|thin]` cannot be used simultaneously.

### `-O` <sup>[frontend]</sup>

Use O1-level code optimization, equivalent to `-O1`.

## Code Obfuscation Options

`cjc` supports code obfuscation to provide additional security protection for code. It is disabled by default.

`cjc` supports the following code obfuscation options:

### `--fobf-string`

Enable string obfuscation.

Obfuscate string constants in the code, making it impossible for attackers to statically read string data directly from the binary.

### `--fno-obf-string`

Disable string obfuscation.

### `--fobf-const`

Enable constant obfuscation.

Obfuscate numerical constants used in the code by replacing numerical operation instructions with equivalent but more complex instruction sequences.

### `--fno-obf-const`

Disable constant obfuscation.

### `--fobf-layout`

Enable layout obfuscation.

Layout obfuscation obfuscates symbols (including function names and global variable names), path names, line numbers, and function arrangement order in the code. When this option is enabled, `cjc` will generate a symbol mapping output file `*.obf.map` in the current directory. If the `--obf-sym-output-mapping` option is configured, its parameter value will be used as the filename for the symbol mapping output file. The symbol mapping output file contains the mapping relationship between original and obfuscated symbols, which can be used to deobfuscate obfuscated symbols.

> **Note:**
>
> Layout obfuscation conflicts with parallel compilation. Do not enable both simultaneously. If both are enabled, parallel compilation will be disabled.

### `--fno-obf-layout`

Disable layout obfuscation.

### `--obf-sym-prefix <string>`

Specify the prefix string added to symbols during layout obfuscation.

When this option is set, all obfuscated symbols will have this prefix added. This can help avoid symbol conflicts when obfuscating multiple Cangjie packages.

### `--obf-sym-output-mapping <file>`

Specify the symbol mapping output file for layout obfuscation.

The symbol mapping output file records the original names, obfuscated names, and file paths of symbols. This file can be used to deobfuscate obfuscated symbols.

### `--obf-sym-input-mapping <file,...>`

Specify the symbol mapping input file(s) for layout obfuscation.

The layout obfuscation feature will use the mapping relationships in these files to obfuscate symbols. Therefore, when compiling Cangjie packages with dependencies, use the symbol mapping output file of the dependent package as the parameter for the `--obf-sym-input-mapping` option of the calling package to ensure consistent obfuscation results for the same symbols across packages.

### `--obf-apply-mapping-file <file>`

Provide a custom symbol mapping file for layout obfuscation. The layout obfuscation feature will obfuscate symbols according to the mappings in this file.

The file format is as follows:

```text
<original_symbol_name> <new_symbol_name>
```

Here, `original_symbol_name` is the pre-obfuscation name, and `new_symbol_name` is the post-obfuscation name. `original_symbol_name` consists of multiple `field`s. A `field` represents a field name, which can be a module name, package name, class name, struct name, enum name, function name, or variable name. `field`s are separated by the delimiter `'.'`. If the `field` is a function name, the function's parameter types must be appended in parentheses `'()'`. For parameterless functions, the parentheses will be empty. If the `field` has generic parameters, they must also be appended in angle brackets `'<>'`.

The layout obfuscation feature will replace `original_symbol_name` in the Cangjie application with `new_symbol_name`. For symbols not in this file, the layout obfuscation feature will use random names for replacement. If the mappings in this file conflict with those in `--obf-sym-input-mapping`, the compiler will throw an exception and stop compilation.

### `--fobf-export-symbols`

Allow layout obfuscation to obfuscate exported symbols. This option is enabled by default when layout obfuscation is enabled.

When enabled, the layout obfuscation feature will obfuscate exported symbols.

### `--fno-obf-export-symbols`

Disallow layout obfuscation from obfuscating exported symbols.

### `--fobf-source-path`

Allow layout obfuscation to obfuscate path information in symbols. This option is enabled by default when layout obfuscation is enabled.

When enabled, the layout obfuscation feature will obfuscate path information in exception stack traces, replacing path names with the string `"SOURCE"`.

### `--fno-obf-source-path`

Disallow layout obfuscation from obfuscating path information in stack traces.

### `--fobf-line-number`

Allow layout obfuscation to obfuscate line number information in stack traces.

When enabled, the layout obfuscation feature will obfuscate line number information in exception stack traces, replacing line numbers with `0`.

### `--fno-obf-line-number`

Disallow layout obfuscation from obfuscating line number information in stack traces.

### `--fobf-cf-flatten`

Enable control flow flattening obfuscation.

Obfuscates existing control flow in the code to complicate its transfer logic.

### `--fno-obf-cf-flatten`

Disable control flow flattening obfuscation.

### `--fobf-cf-bogus`

Enable bogus control flow obfuscation.

Inserts bogus control flow into the code to complicate its logic.

### `--fno-obf-cf-bogus`

Disable bogus control flow obfuscation.

### `--fobf-all`

Enable all obfuscation features.

Specifying this option is equivalent to enabling the following options simultaneously:

- `--fobf-string`
- `--fobf-const`
- `--fobf-layout`
- `--fobf-cf-flatten`
- `--fobf-cf-bogus`

### `--obf-config <file>`

Specify the path to the code obfuscation configuration file.

The configuration file can be used to prevent the obfuscation tool from obfuscating certain functions or symbols.

The format of the configuration file is as follows:

```text
obf_func1 name1
obf_func2 name2
...
```

The first parameter `obf_func` specifies the obfuscation feature:

- `obf-cf-bogus`: Bogus control flow obfuscation
- `obf-cf-flatten`: Control flow flattening obfuscation
- `obf-const`: Constant obfuscation
- `obf-layout`: Layout obfuscation

The second parameter `name` specifies the objects to be preserved, composed of multiple `field`s. A `field` represents a field name, which can be a package name, class name, struct name, enum name, function name, or variable name.

`field`s are separated by the delimiter `'.'`. If a `field` is a function name, the function's parameter types must be enclosed in parentheses `'()'` and appended to the function name. For parameterless functions, the parentheses remain empty.

For example, suppose the following code exists in package `packA`:

```cangjie
package packA
class MyClassA {
    func funcA(a: String, b: Int64): String {
        return a
    }
}
```

To prevent the control flow flattening feature from obfuscating `funcA`, the user can write the following rule:

```text
obf-cf-flatten packA.MyClassA.funcA(std.core.String, Int64)
```

Users can also use wildcards to write more flexible rules, enabling a single rule to preserve multiple objects. Currently, three types of wildcards are supported:

Obfuscation feature wildcards:

| Obfuscation Wildcard | Description                  |
| :------------------- | :--------------------------- |
| `?`                 | Matches a single character in a name |
| `*`                 | Matches any number of characters in a name |

Field name wildcards:

| Field Wildcard | Description                                                                 |
| :------------- | :-------------------------------------------------------------------------- |
| `?`           | Matches a single non-delimiter `'.'` character in a field name             |
| `*`           | Matches any number of characters in a field name, excluding delimiters `'.'` and parameters |
| `**`          | Matches any number of characters in a field name, including delimiters `'.'` and parameters. `'**'` only takes effect when used as a standalone `field`; otherwise, it is treated as `'*'` |

Function parameter type wildcards:

| Parameter Wildcard | Description                |
| :----------------- | :------------------------- |
| `...`             | Matches any number of parameters |
| `***`             | Matches a parameter of any type |

> **Note:**
>
> Parameter types are also composed of field names, so field name wildcards can be used to match individual parameter types.

Examples of wildcard usage:

Example 1:

```text
obf-cf-flatten pro?.myfunc()
```

This rule prevents the `obf-cf-flatten` feature from obfuscating the function `pro?.myfunc()`. `pro?.myfunc()` can match `pro0.myfunc()` but not `pro00.myfunc()`.

Example 2:

```text
* pro0.**
```

This rule prevents any obfuscation feature from obfuscating any function or variable under the package `pro0`.

Example 3:

```text
* pro*.myfunc(...)
```

This rule prevents any obfuscation feature from obfuscating the function `pro*.myfunc(...)`. `pro*.myfunc(...)` can match any `myfunc` function in a single-level package starting with `pro`, with any parameters.

To match multi-level package names, such as `pro0.mypack.myfunc()`, use `pro*.**.myfunc(...)`. Note that `'**'` only takes effect when used as a standalone field name, so `pro**.myfunc(...)` and `pro*.myfunc(...)` are equivalent and cannot match multi-level package names. To match all `myfunc` functions in any package starting with `pro` (including functions named `myfunc` in classes), use `pro*.**.myfunc(...)`.

Example 4:

```text
obf-cf-* pro0.MyClassA.myfunc(**.MyClassB, ***, ...)
```

This rule prevents the `obf-cf-*` feature from obfuscating the function `pro0.MyClassA.myfunc(**.MyClassB, ***, ...)`. Here, `obf-cf-*` matches both `obf-cf-bogus` and `obf-cf-flatten` obfuscation features. `pro0.MyClassA.myfunc(**.MyClassB, ***, ...)` matches the function `pro0.MyClassA.myfunc`, where the first parameter can be of type `MyClassB` from any package, the second parameter can be of any type, and the function can accept zero or more additional parameters of any type.

### `--obf-level <value>`

Specify the obfuscation strength level.

The level can be set from 1 to 9. The default level is 5. Higher levels increase obfuscation strength but may also increase output file size and execution overhead.

### `--obf-seed <value>`

Specify the random seed for the obfuscation algorithm.

By specifying a random seed for the obfuscation algorithm, the same Cangjie code can produce different obfuscation results across builds. By default, the same Cangjie code produces identical obfuscation results in each run.

## Secure Compilation Options

`cjc` generates position-independent code by default and produces position-independent executables when compiling executable files.

For Release builds, it is recommended to enable/disable compilation options according to the following rules to enhance security.

### Enable `--trimpath <value>` <sup>[frontend]</sup>

Remove specified absolute path prefixes from debugging and exception information. This option prevents build path information from being written into the binary.

After enabling this option, source code path information in the binary is typically incomplete, which may affect debugging. It is recommended to disable this option for debug builds.

### Enable `--strip-all`, `-s`

Remove the symbol table from the binary. This option deletes symbol-related information not required at runtime.

After enabling this option, the binary cannot be debugged. Disable this option for debug builds.

### Disable `--set-runtime-rpath`

If the executable will be distributed to different environments or if other users have write permissions to the Cangjie runtime library directory currently in use, enabling this option may pose security risks. Therefore, disable this option.

This option is not applicable when compiling Windows targets.

### Enable `--link-options "-z noexecstack"`<sup>1</sup>

Sets thread stacks as non-executable.

Only available when compiling Linux targets.

### Enable `--link-options "-z relro"`<sup>1</sup>

Sets GOT table relocations as read-only.

Only available when compiling Linux targets.

### Enable `--link-options "-z now"`<sup>1</sup>

Enables immediate binding.

Only available when compiling Linux targets.

## Code Coverage Instrumentation Options

> **Note:**
>
> Windows and macOS versions currently do not support code coverage instrumentation options.

Cangjie supports code coverage instrumentation (SanitizerCoverage, hereafter referred to as SanCov), providing interfaces consistent with LLVM's SanitizerCoverage. The compiler inserts coverage feedback functions at the function level or BasicBlock level. Users only need to implement the agreed callback functions to perceive program runtime states.

SanCov functionality in Cangjie is provided on a per-package basis, meaning an entire package is either fully instrumented or not instrumented at all.

### `--sanitizer-coverage-level=0/1/2`

Instrumentation level:

- 0: No instrumentation;
- 1: Function-level instrumentation, inserting callback functions only at function entry points;
- 2: BasicBlock-level instrumentation, inserting callback functions at various BasicBlocks.

If not specified, the default value is 2.

This compilation option only affects the instrumentation level of `--sanitizer-coverage-trace-pc-guard`, `--sanitizer-coverage-inline-8bit-counters`, and `--sanitizer-coverage-inline-bool-flag`.

### `--sanitizer-coverage-trace-pc-guard`

Enabling this option inserts a function call `__sanitizer_cov_trace_pc_guard(uint32_t *guard_variable)` at each Edge, influenced by `sanitizer-coverage-level`.

**Notably**, this feature differs from gcc/llvm implementations: it does not insert `void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop)` in the constructor. Instead, it inserts a function call `uint32_t *__cj_sancov_pc_guard_ctor(uint64_t edgeCount)` during package initialization.

The `__cj_sancov_pc_guard_ctor` callback function must be implemented by the developer. Packages with SanCov enabled will call this callback as early as possible. The input parameter is the number of Edges in the Package, and the return value is typically a memory region created by calloc.

If `__sanitizer_cov_trace_pc_guard_init` needs to be called, it is recommended to call it within `__cj_sancov_pc_guard_ctor`, using dynamically created buffers to compute the function's input parameters and return value.

A standard implementation of `__cj_sancov_pc_guard_ctor` is as follows:

```cpp
uint32_t *__cj_sancov_pc_guard_ctor(uint64_t edgeCount) {
    uint32_t *p = (uint32_t *) calloc(edgeCount, sizeof(uint32_t));
    __sanitizer_cov_trace_pc_guard_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-inline-8bit-counters`

Enabling this option inserts an accumulator at each Edge, which increments by one each time the Edge is traversed, influenced by `sanitizer-coverage-level`.

**Notably**, this feature differs from gcc/llvm implementations: it does not insert `void __sanitizer_cov_8bit_counters_init(char *start, char *stop)` in the constructor. Instead, it inserts a function call `uint8_t *__cj_sancov_8bit_counters_ctor(uint64_t edgeCount)` during package initialization.

The `__cj_sancov_pc_guard_ctor` callback function must be implemented by the developer. Packages with SanCov enabled will call this callback as early as possible. The input parameter is the number of Edges in the Package, and the return value is typically a memory region created by calloc.

If `__sanitizer_cov_8bit_counters_init` needs to be called, it is recommended to call it within `__cj_sancov_8bit_counters_ctor`, using dynamically created buffers to compute the function's input parameters and return value.

A standard implementation of `__cj_sancov_8bit_counters_ctor` is as follows:

```cpp
uint8_t *__cj_sancov_8bit_counters_ctor(uint64_t edgeCount) {
    uint8_t *p = (uint8_t *) calloc(edgeCount, sizeof(uint8_t));
    __sanitizer_cov_8bit_counters_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-inline-bool-flag`

Enabling this option inserts a boolean value at each Edge. The boolean value corresponding to a traversed Edge will be set to True, influenced by `sanitizer-coverage-level`.

**Notably**, this feature differs from gcc/llvm implementations: it does not insert `void __sanitizer_cov_bool_flag_init(bool *start, bool *stop)` in the constructor. Instead, it inserts a function call `bool *__cj_sancov_bool_flag_ctor(uint64_t edgeCount)` during package initialization.

The `__cj_sancov_bool_flag_ctor` callback function must be implemented by the developer. Packages with SanCov enabled will call this callback as early as possible. The input parameter is the number of Edges in the Package, and the return value is typically a memory region created by calloc.

If `__sanitizer_cov_bool_flag_init` needs to be called, it is recommended to call it within `__cj_sancov_bool_flag_ctor`, using dynamically created buffers to compute the function's input parameters and return value.

A standard implementation of `__cj_sancov_bool_flag_ctor` is as follows:

```cpp
bool *__cj_sancov_bool_flag_ctor(uint64_t edgeCount) {
    bool *p = (bool *) calloc(edgeCount, sizeof(bool));
    __sanitizer_cov_bool_flag_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-pc-table`

This compilation option provides the correspondence between instrumentation points and source code, currently only offering function-level correspondence. It must be used in conjunction with `--sanitizer-coverage-trace-pc-guard`, `--sanitizer-coverage-inline-8bit-counters`, or `--sanitizer-coverage-inline-bool-flag`, requiring at least one of these options to be enabled, and multiple can be enabled simultaneously.

**Notably**, this feature differs from gcc/llvm implementations: it does not insert `void __sanitizer_cov_pcs_init(const uintptr_t *pcs_beg, const uintptr_t *pcs_end);` in the constructor. Instead, it inserts a function call `void __cj_sancov_pcs_init(int8_t *packageName, uint64_t n, int8_t **funcNameTable, int8_t **fileNameTable, uint64_t *lineNumberTable)` during package initialization. The parameters are as follows:

- `int8_t *packageName`: A string representing the package name (instrumentation uses C-style int8 arrays as input parameters to express strings, same below).
- `uint64_t n`: There are n functions instrumented.
- `int8_t **funcNameTable`: A string array of length n, where the i-th instrumentation point corresponds to the function name funcNameTable\[i\].
- `int8_t **fileNameTable`: A string array of length n, where the i-th instrumentation point corresponds to the file name fileNameTable\[i\].
- `uint64_t *lineNumberTable`: A uint64 array of length n, where the i-th instrumentation point corresponds to the line number lineNumberTable\[i\].

If `__sanitizer_cov_pcs_init` needs to be called, you must manually convert Cangjie's pc-table to C language pc-table.

### `--sanitizer-coverage-stack-depth`

Enabling this compilation option inserts a call to `__updateSancovStackDepth` at each function entry point, as Cangjie cannot obtain the SP pointer value. Implementing this function on the C side allows obtaining the SP pointer.

A standard implementation of `updateSancovStackDepth` is as follows:

```cpp
thread_local void* __sancov_lowest_stack;

void __updateSancovStackDepth()
{
    register void* sp = __builtin_frame_address(0);
    if (sp < __sancov_lowest_stack) {
        __sancov_lowest_stack = sp;
    }
}
```

### `--sanitizer-coverage-trace-compares`

Enabling this option inserts callback functions before all compare and match instructions. The specific list is as follows, consistent with LLVM's API functionality. Refer to Tracing data flow.

```cpp
void __sanitizer_cov_trace_cmp1(uint8_t Arg1, uint8_t Arg2);
void __sanitizer_cov_trace_const_cmp1(uint8_t Arg1, uint8_t Arg2);
void __sanitizer_cov_trace_cmp2(uint16_t Arg1, uint16_t Arg2);
void __sanitizer_cov_trace_const_cmp2(uint16_t Arg1, uint16_t Arg2);
void __sanitizer_cov_trace_cmp4(uint32_t Arg1, uint32_t Arg2);
void __sanitizer_cov_trace_const_cmp4(uint32_t Arg1, uint32_t Arg2);
void __sanitizer_cov_trace_cmp8(uint64_t Arg1, uint64_t Arg2);
void __sanitizer_cov_trace_const_cmp8(uint64_t Arg1, uint64_t Arg2);
void __sanitizer_cov_trace_switch(uint64_t Val, uint64_t *Cases);
```

### `--sanitizer-coverage-trace-memcmp`

This compilation option provides prefix comparison feedback for String, Array, and other comparisons. Enabling this option inserts callback functions before comparison functions for String and Array. Specifically, for the following APIs of String and Array, corresponding instrumentation functions are inserted:

- String==: __sanitizer_weak_hook_memcmp
- String.startsWith: __sanitizer_weak_hook_memcmp
- String.endsWith: __sanitizer_weak_hook_memcmp
- String.indexOf: __sanitizer_weak_hook_strstr
- String.replace: __sanitizer_weak_hook_strstr
- String.contains: __sanitizer_weak_hook_strstr
- CString==: __sanitizer_weak_hook_strcmp
- CString.startswith: __sanitizer_weak_hook_memcmp
- CString.endswith: __sanitizer_weak_hook_strncmp
- CString.compare: __sanitizer_weak_hook_strcmp
- CString.equalsLower: __sanitizer_weak_hook_strcasecmp
- Array==: __sanitizer_weak_hook_memcmp
- ArrayList==: __sanitizer_weak_hook_memcmp

## Experimental Feature Options

### `--enable-eh` <sup>[frontend]</sup>

Enabling this option allows Cangjie to support Effect Handlers, an advanced control flow mechanism for modular and recoverable side-effect handling.

Effect Handlers enable programmers to decouple side-effect operations from their handling logic, resulting in cleaner, more composable code. This mechanism enhances abstraction levels, particularly for handling operations like logging, input/output, and state changes, preventing main logic from being polluted by side-effect code.

Effects work similarly to exception handling but do not use `throw` and `catch`. Instead, effects are executed via `perform` and captured/handled via `handle`. Each effect must be defined by inheriting the `stdx.effect.Command` class.

Unlike traditional exception mechanisms, Effect Handlers can choose to `resume` execution after handling an effect, injecting a value back to the original call site and continuing execution. This "resume" capability allows finer control over program flow, making it particularly suitable for building simulators, interpreters, or cooperative multitasking systems requiring high control.

Example:

```cangjie
import stdx.effect.Command

// Define a Command named GetNumber
class GetNumber <: Command<Int64> {}

main() {
    try {
        println("About to perform")

        // Perform the GetNumber effect
        let a = perform GetNumber()

        // Execution continues here after handler resumes
        println("It is resumed, a = ${a}")
    } handle(e: GetNumber) {
        // Handle the GetNumber effect
        println("It is performed")

        // Resume execution, injecting value 9
        resume with 9
    }
    0
}
```

In this example, a new subclass `GetNumber` of `Command` is defined.

- In the `main` function, the `try-handle` structure is used to handle this effect.
- In the `try` block, a prompt message (`"About to perform"`) is printed first, followed by executing the effect via `perform GetNumber()`. The return value of the `perform` expression is assigned to variable `a`. Executing an effect jumps the execution flow to the `handle` block capturing this effect.
- In the `handle` block, the `GetNumber` effect is captured and handled. A message (`"It is performed"`) is printed first, followed by injecting the constant `9` back to the original call site via `resume with 9`, then resuming execution after `perform`, printing (`"It is resumed, a = 9"`).

Output:

```shell
About to perform
It is performed
It is resumed, a = 9
```

> **Note:**
>
> - Effect Handlers are currently experimental. This option may change in future versions. Use with caution.
> - Using Effect Handlers requires importing the `stdx.effect` library.

### `--experimental` <sup>[frontend]</sup>

Enables experimental features, allowing the use of other experimental options on the command line.

> **Note:**
>
> Binaries generated using experimental features may have potential runtime issues. Be aware of the risks when using this option.

## Compiler Plugin Options

### `--plugin <value>` <sup>[frontend]</sup>

Provides compiler plugin capability. As an experimental feature, it is currently only for internal validation and does not support custom plugin development. Using it may cause errors.

## Other Features

### Compiler Error Message Colors

For Windows versions of the Cangjie compiler, error messages will only display colors when running on Windows 10 version 1511 (Build 10586) or later systems. Otherwise, colors will not be displayed.

### Setting build-id

Use `--link-options "--build-id=<arg>"`<sup>1</sup> to pass linker options for setting build-id.

This feature is not supported when compiling Windows targets.

### Setting rpath

Use `--link-options "-rpath=<arg>"`<sup>1</sup> to pass linker options for setting rpath.

This feature is not supported when compiling Windows targets.

### Incremental Compilation

Enable incremental compilation via `--incremental-compile`<sup>[frontend]</sup>. When enabled, `cjc` will use cache files from previous compilations to speed up the current compilation.

> **Note:**
>
> This option is experimental. Binaries generated using this feature may have potential runtime issues. Be aware of the risks when using this option. This option must be used with `--experimental`.
> When this option is specified, incremental compilation caches and logs are saved to the `.cached` directory under the output file path.

### Output CHIR

Use `--emit-chir=[raw|opt]`<sup>[frontend]</sup> to specify output of serialized CHIR compilation phase products. `raw` outputs CHIR before compiler optimization, `opt` outputs CHIR after compiler optimization. Using `--emit-chir` defaults to outputting optimized CHIR.

### `--no-prelude` <sup>[frontend]</sup>

Disables automatic import of the standard library core package.

> **Note:**
>
> This option can only be used when compiling the Cangjie standard library core package, not for other Cangjie code compilation scenarios.

## Environment Variables Used by `cjc`

Here are some environment variables that the Cangjie compiler may use during code compilation.

### `TMPDIR` or `TMP`

The Cangjie compiler places temporary files generated during compilation in temporary directories. By default, `Linux` and `macOS` operating systems place them in the `/tmp` directory, while `Windows` places them in `C:\Windows\Temp`. The Cangjie compiler also supports custom temporary file directories. On `Linux` and `macOS`, you can change the temporary file directory by setting the `TMPDIR` environment variable, while on `Windows`, you can change it by setting the `TMP` environment variable.

Example:
In Linux shell:

```shell
export TMPDIR=/home/xxxx
```

In Windows cmd:

```shell
set TMP=D:\\xxxx
```
