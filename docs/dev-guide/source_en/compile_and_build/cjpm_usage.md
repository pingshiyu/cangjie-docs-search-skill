# Introduction to `cjpm`

`CJPM (Cangjie Project Manager)` is the official package management tool for the Cangjie language, designed to manage and maintain the module system of Cangjie projects while providing a simpler and unified compilation entry point with support for custom compilation commands. Through automated dependency management, it analyzes and merges multi-version third-party dependencies, eliminating concerns about version conflicts and significantly reducing developer workload. Additionally, it offers a native custom build mechanism for the Cangjie language, allowing developers to add pre-processing and post-processing workflows at different build stages. This enables flexible customization of the build process to meet various compilation requirements across different business scenarios.

## Basic Usage of `cjpm`

Run `cjpm -h` to view the main interface, which consists of several sections: command description, usage examples (Usage), available subcommands (Available subcommands), supported options (Available options), and additional tips.

```text
Cangjie Project Manager

Usage:
  cjpm [subcommand] [option]

Available subcommands:
  init             Init a new cangjie module
  check            Check the dependencies
  update           Update cjpm.lock
  tree             Display the package dependencies in the source code
  build            Compile the current module
  run              Compile and run an executable product
  test             Unittest a local package or module
  bench            Run benchmarks in a local package or module
  clean            Clean up the target directory
  install          Install a cangjie binary
  uninstall        Uninstall a cangjie binary

Available options:
  -h, --help       help for cjpm
  -v, --version    version for cjpm

Use "cjpm [subcommand] --help" for more information about a command.
```

`cjpm init` initializes a new Cangjie module or workspace. By default, it creates a `cjpm.toml` file in the current directory, along with a `src` folder containing a default `main.cj` file. Custom initialization parameters can be viewed via `cjpm init -h`.

Example:

```text
Input: cjpm init
Output: cjpm init success
```

`cjpm build` compiles the current Cangjie project. Before execution, it checks dependencies and then invokes `cjc` for compilation. It supports full compilation, incremental compilation, cross-compilation, parallel compilation, and more. Additional compilation features can be viewed via `cjpm build -h`. The `cjpm build -V` command prints all compilation process commands.

Example:

```text
Input: cjpm build -V
Output:
compile package module1.package1: cjc --import-path target -p "src/package1" --output-type=staticlib -o target/release/module1/libmodule1.package1.a
compile package module1: cjc --import-path target -L target/release/module1 -lmodule1.package1 -p "src" --output-type=exe --output-dir target/release/bin -o main

cjpm build success
```

## `cjpm.toml` Configuration File Explanation

The `cjpm.toml` configuration file defines basic information, dependencies, and compilation options. `cjpm` primarily parses and executes based on this file.

Example configuration:

```text
[package] # Single-module configuration field; cannot coexist with [workspace]
  cjc-version = "1.0.0" # Minimum required `cjc` version (mandatory)
  name = "demo" # Module name and root package name (mandatory)
  description = "nothing here" # Description (optional)
  version = "1.0.0" # Module version (mandatory)
  compile-option = "" # Additional compilation options (optional)
  override-compile-option = "" # Additional global compilation options (optional)
  link-option = "" # Linker passthrough options (optional)
  output-type = "executable" # Compilation output type (mandatory)
  src-dir = "" # Source code directory (optional)
  target-dir = "" # Output directory (optional)
  package-configuration = {} # Single-package configuration (optional)

[workspace] # Workspace management field; cannot coexist with [package]
  members = [] # Workspace member modules (mandatory)
  build-members = [] # Workspace compilation modules (subset of members, optional)
  test-members = [] # Workspace test modules (subset of build-members, optional)
  compile-option = "" # Additional compilation options for all workspace members (optional)
  override-compile-option = "" # Additional global compilation options for all workspace members (optional)
  link-option = "" # Linker passthrough options for all workspace members (optional)
  target-dir = "" # Output directory (optional)

[dependencies] # Source code dependencies (optional)
  coo = { git = "xxx", branch = "dev" } # Git dependency
  doo = { path = "./pro1" } # Local source dependency

[test-dependencies] # Test-phase dependencies (format same as [dependencies], optional)

[script-dependencies] # Build script dependencies (format same as [dependencies], optional)

[replace] # Dependency replacement (format same as [dependencies], optional)

[ffi.c] # C library dependencies (optional)
  clib1.path = "xxx"

[profile] # Command profile configuration (optional)
  build = {} # Build command configuration
  test = {} # Test command configuration
  bench = {} # Benchmark command configuration
  customized-option = {} # Custom passthrough options

[target.x86_64-unknown-linux-gnu] # Backend and platform-specific configuration (optional)
  compile-option = "value1" # Additional compilation options for specific targets or cross-compilation (optional)
  override-compile-option = "value2" # Additional global compilation options for specific targets or cross-compilation (optional)
  link-option = "value3" # Linker passthrough options for specific targets or cross-compilation (optional)

[target.x86_64-w64-mingw32.dependencies] # Dependencies for specific targets (optional)

[target.x86_64-w64-mingw32.test-dependencies] # Test-phase dependencies for specific targets (optional)

[target.x86_64-unknown-linux-gnu.bin-dependencies] # Cangjie binary library dependencies for specific targets or cross-compilation (optional)
  path-option = ["./test/pro0", "./test/pro1"] # Binary library dependencies via directory paths
[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option] # Binary library dependencies via single files
  "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
  "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
  "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
```