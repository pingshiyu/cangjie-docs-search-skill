# Package Management Tool

## Overview

`CJPM (Cangjie Project Manager)` is the official package management tool for the Cangjie language, designed to manage and maintain the module system of Cangjie projects. It covers operations such as module initialization, dependency checking, and updates. It provides a unified compilation entry point, supporting incremental compilation, parallel compilation, and custom compilation commands.

## Usage Instructions

Execute the `cjpm -h` command to view the usage instructions for the package management tool, as shown below.

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

Basic usage commands are as follows:

```shell
cjpm build --help
```

`cjpm` is the name of the main program, `build` is the currently executed available command, and `--help` is the available configuration option for the current command (configuration options typically have both long and short forms with the same effect).

Upon successful execution, the following result will be displayed:

```text
Compile a local module and all of its dependencies.

Usage:
  cjpm build [option]

Available options:
  -h, --help                    help for build
  -i, --incremental             enable incremental compilation
  -j, --jobs <N>                the number of jobs to spawn in parallel during the build process
  -V, --verbose                 enable verbose
  -g                            enable compile debug version target
  --coverage                    enable coverage
  --cfg                         enable the customized option 'cfg'
  --enable-features <value>     explicitly specify comma-separated list of features to be enabled
  --no-feature-deduce           disables auto-enabling of features, deduced from other options, machine properties, etc.
  -m, --member <value>          specify a member module of the workspace
  --target <value>              generate code for the given target platform
  --target-dir <value>          specify target directory
  -o, --output <value>          specify product name when compiling an executable file
  -l, --lint                    enable cjlint code check
  --mock                        enable support of mocking classes in tests
  --skip-script                 disable script 'build.cj'.
```

## Command Descriptions

### init

`init` is used to initialize a new Cangjie module or workspace. When initializing a module, it creates a configuration file `cjpm.toml` in the current folder by default and creates a `src` source code folder. If the module's output is of the executable type, it generates a default `main.cj` file under `src`, which prints `hello world` after compilation. When initializing a workspace, only the `cjpm.toml` file is created, and it scans existing Cangjie modules under the path and adds them to the `members` field by default. If `cjpm.toml` already exists or `main.cj` is already present in the source folder, the corresponding file creation steps will be skipped.

`init` has several configurable options:

- `--workspace` creates a new workspace configuration file. When this option is specified, other options are automatically ignored.
- `--name <value>` specifies the `root` package name of the new module. If not specified, it defaults to the name of the parent folder.
- `--path <value>` specifies the path for the new module. If not specified, it defaults to the current folder.
- `--type=<executable|static|dynamic>` specifies the output type of the new module. If omitted, it defaults to `executable`.
- `--experimental` initializes the Cangjie multi-platform project.

Examples:

```text
Input: cjpm init
Output: cjpm init success
```

```text
Input: cjpm init --name demo --path project
Output: cjpm init success
```

```text
Input: cjpm init --type=static
Output: cjpm init success
```

### check

The `check` command is used to check the dependencies required by the project. Upon successful execution, it prints the valid package compilation order.

`check` has several configurable options:

- `-m, --member <value>` can only be used in a workspace to specify a single module as the check entry point.
- `--no-tests` when configured, test-related dependencies will not be printed.
- `--skip-script` when configured, the build script compilation and execution will be skipped.

Examples:

```text
Input: cjpm check
Output:
The valid serial compilation order is:
    b.pkgA -> b
cjpm check success
```

```text
Input: cjpm check
Output:
Error: cyclic dependency
b.B -> c.C
c.C -> d.D
d.D -> b.B
Note: In the above output, b.B represents a subpackage named b.B in the module with b as the root package.
```

```text
Input: cjpm check
Output:
Error: can not find the following dependencies
    pro1.xoo
    pro1.yoo
    pro2.zoo
```

### update

`update` is used to update the contents of `cjpm.toml` to `cjpm.lock`. When `cjpm.lock` does not exist, it will be generated. The `cjpm.lock` file records metadata such as version numbers of `git` dependencies for use in the next build.

`update` has the following configurable option:

- `--skip-script` when configured, the build script compilation and execution will be skipped.

```text
Input: cjpm update
Output: cjpm update success
```

### tree

The `tree` command is used to visually display the package dependency relationships in Cangjie source code.

`tree` has several configurable options:

- `-V, --verbose` adds detailed information to package nodes, including package name, version number, and package path.
- `--depth <N>` specifies the maximum depth of the dependency tree. The value must be a non-negative integer. When this option is specified, all packages are treated as root nodes by default. The value of N represents the maximum depth of child nodes for each dependency tree.
- `-p, --package <value>` specifies a package as the root node to display its sub-dependencies. The value required is the package name.
- `--invert <value>` specifies a package as the root node and inverts the dependency tree to show which packages depend on it. The value required is the package name.
- `--target <value>` includes dependencies for the specified target platform in the analysis and displays the dependency relationships.
- `--no-tests` excludes dependencies listed in the `test-dependencies` field.
- `--skip-script` when configured, the build script compilation and execution will be skipped.

For example, the source code directory structure of module `a` is as follows:

```text
src
├── main.cj
├── aoo
│   └── a.cj
├── boo
│   └── b.cj
├── coo
│   └── c.cj
├── doo
│   └── d.cj
├── eoo
│   └── e.cj
└── cjpm.toml
```

The dependency relationships are: package `a` imports packages `a.aoo` and `a.boo`; subpackage `aoo` imports package `a.coo`; subpackage `boo` imports package `coo`; subpackage `doo` imports package `coo`.

```text
Input: cjpm tree
Output:
|-- a
    └── a.aoo
        └── a.coo
    └── a.boo
        └── a.coo
|-- a.doo
    └── a.coo
|-- a.eoo
cjpm tree success
```

```text
Input: cjpm tree --depth 2 -p a
Output:
|-- a
    └── a.aoo
        └── a.coo
    └── a.boo
        └── a.coo
cjpm tree success
```

```text
Input: cjpm tree --depth 0
Output:
|-- a
|-- a.eoo
|-- a.aoo
|-- a.boo
|-- a.doo
|-- a.coo
cjpm tree success
```

```text
Input: cjpm tree --invert a.coo --verbose
Output:
|-- a.coo 1.2.0 (.../src/coo)
    └── a.aoo 1.1.0 (.../src/aoo)
            └── a 1.0.0 (.../src)
    └── a.boo 1.1.0 (.../src/boo)
            └── a 1.0.0 (.../src)
    └── a.doo 1.3.0 (.../src/doo)
cjpm tree success
```

### build

`build` is used to build the current Cangjie project. Before executing this command, it checks dependencies. If the check passes, it calls `cjc` to perform the build.

`build` has several configurable options:

- `-i, --incremental` specifies incremental compilation. By default, full compilation is performed.
- `-j, --jobs <N>` specifies the maximum number of parallel compilation jobs. The final maximum concurrency is the minimum of `N` and `2 times the number of CPU cores`.
- `-V, --verbose` displays compilation logs.
- `-g` generates `debug` version output.
- `--coverage` generates coverage information. By default, coverage is disabled.
- `--cfg` when specified, custom `cfg` options in `cjpm.toml` can be passed through. For `cjpm.toml` configuration, refer to the [profile.customized-option](#profilecustomized-option) section.
- `--enable-features <value>` Explicitly specifies the features to enable, which can be comma-separated.
- `--no-feature-deduce` Disables automatic feature enabling, including inference from other options or machine-related properties.
- `-m, --member <value>` can only be used in a workspace to specify a single module as the compilation entry point.
- `--target <value>` when specified, enables cross-compilation to the target platform. For `cjpm.toml` configuration, refer to the [target](#target) section.
- `--target-dir <value>` specifies the output directory for the build artifacts.
- `-o, --output <value>` specifies the name of the output executable file. The default name is `main` (`main.exe` on Windows). Note that compiling an executable named `cjc` is currently not supported.
- `-l, --lint` Used to invoke the Cangjie language static analysis tool for code inspection during compilation.
- `--mock` enables `mock` testing for classes in the build version with this option.
- `--skip-script` when configured, the build script compilation and execution will be skipped.

> **Note:**
>
> - The `-i, --incremental` option only enables package-level incremental compilation in `cjpm`. Developers can manually pass `--incremental-compile` and `--experimental` compilation options in the configuration file's `compile-option` field to enable function-level incremental compilation provided by the `cjc` compiler.
> - The `-i, --incremental` option currently only supports incremental analysis based on source code. If imported library content changes, developers need to rebuild using full compilation.

Intermediate files generated during compilation are stored in the `target` folder by default, while executable files are stored in `target/release/bin` or `target/debug/bin` folders based on the compilation mode. To run the executable, refer to the `run` command.

To ensure reproducible builds, this command creates a `cjpm.lock` file containing the exact versions of all transitive dependencies, which will be used for subsequent builds. To update this file, use the `update` command. If reproducible builds are required for all project participants, this file should be committed to the version control system.

Examples:

```text
Input: cjpm build -V
Output:
compile package module1.package1: cjc --import-path "target/release" --output-dir "target/release/module1" -p "src/package1" --output-type=staticlib -o libmodule1.package1.a
compile package module1: cjc --import-path "target/release" --output-dir "target/release/bin" -p "src" --output-type=exe -o main
cjpm build success
```

```text
Input: cjpm build
Output: cjpm build success
```

> **Note:**
>
> According to the Cangjie package management specifications, only valid source code packages that meet the requirements can be correctly included in the compilation scope. If warnings like `no '.cj' file` appear during compilation, it is likely because the corresponding package does not meet the specifications, causing the source files to be excluded. In such cases, refer to the [Cangjie Package Management Specifications](#cangjie-package-management-specification) to modify the code directory structure.

Before executing `cjpm build`, `cjpm` checks the package dependency relationships of the current module or workspace. If mutual imports between packages form a dependency cycle, the build will be aborted, and an error message will be returned, indicating the cyclic dependency path.

For example, the source code directory structure of module `demo` is as follows:

```text
src
├── main.cj
├── aoo
│   └── a.cj
├── boo
│   └── b.cj
├── coo
│   └── c.cj
└── cjpm.toml
```

The dependency relationships are: package `demo.aoo` imports package `demo.boo`, package `demo.boo` imports package `demo.coo`, and package `demo.coo` imports package `demo.aoo`. The mutual imports between these three packages form a cycle, resulting in a cyclic dependency:

```text
Input: cjpm build
Output:
cyclic dependency:
demo.boo -> demo.coo
demo.coo -> demo.aoo
demo.aoo -> demo.boo

Error: cjpm build failed
```

When a cyclic dependency occurs, developers can troubleshoot based on the error message. In the example above, the import chain is `demo.aoo -> demo.boo -> demo.coo -> demo.aoo`. Developers can start analyzing from each package's directory to identify and remove unnecessary imports to resolve the cyclic dependency. For example, start with `demo.aoo` and check which source files import `demo.boo`. If these files do not functionally depend on `demo.boo`, the corresponding imports can be removed. Repeat this process for `demo.boo` and `demo.coo` to eliminate redundant imports and resolve the cyclic dependency.

If functional cyclic dependencies are confirmed, consider the following solutions:

- Refactor import order: Ensure dependencies are unidirectional to avoid cycles. For example, the part of `demo.coo` that depends on `demo.aoo` can be independently implemented to break the cycle.
- Split modules: Move interdependent code into a separate package. For example, merge the three subpackages into one.

In other commands involving package dependency resolution (e.g., `tree`), similar errors will appear for cyclic dependencies, and the same solutions can be applied.

### run

`run` is used to execute the binary output of the current project. The `run` command implicitly executes the `build` command to generate the final binary for execution.

`run` has several configurable options:

- `--name <value>` specifies the name of the binary to run. If not specified, it defaults to `main`. In a workspace, binaries are stored in `target/release/bin` by default.
- `--build-args <value>` controls the parameters for the `build` compilation process.
- `--skip-build` skips the compilation process and directly runs the binary.
- `--run-args <value>` passes arguments to the binary being executed.
- `--target-dir <value>` specifies the output directory for the executable.
- `-g` runs the `debug` version of the binary.
- `-V, --verbose` displays execution logs.
- `--skip-script` when configured, the build script compilation and execution will be skipped.

Examples:

```text
Input: cjpm run
Output: cjpm run success
```

```text
Input: cjpm run -g // This implicitly executes cjpm build -i -g
Output: cjpm run success
```

```text
Input: cjpm run --build-args="-s -j16" --run-args="a b c"
Output: cjpm run success
```

### test

`test` is used to compile and run unit test cases for Cangjie files, printing the test results upon completion. The compiled output is stored in `target/release/unittest_bin` by default. For writing unit test cases, refer to the `std.unittest` library documentation in the *Cangjie Programming Language Standard Library API*.

This command can specify the path of a single package to test (multiple packages can be specified, e.g., `cjpm test path1 path2`). If no path is specified, module-level unit tests are executed by default. During module-level unit testing, only the current module's tests are executed; tests in directly or indirectly dependent modules are not run. The `test` command requires the current project to compile successfully with `build`.

The unit test code structure for a module is as follows, where `xxx.cj` contains the package's source code and `xxx_test.cj` contains the unit test code:

```text
└── src
│    ├── koo
│    │    ├── koo.cj
│    │    └── koo_test.cj
│    ├── zoo
│    │    ├── zoo.cj
│    │    └── zoo_test.cj
│    ├── main.cj
│    └── main_test.cj
└── cjpm.toml
```

1. Single-module testing scenario:

    ```text
    Input: cjpm test
    Progress report:
    group test.koo                                    100% [||||||||||||||||||||||||||||] ✓    (00:00:01)
    group test.zoo                                      0% [----------------------------]      (00:00:00)
    test TestZ.sayhi                                                                           (00:00:00)

    passed: 1, failed: 0                                  33% [|||||||||-------------------]  1/3 (00:00:01)

    Output:
    --------------------------------------------------------------------------------------------------
    TP: test, time elapsed: 177921 ns, RESULT:
        TCS: TestM, time elapsed: 177921 ns, RESULT:
        [ PASSED ] CASE: sayhi (177921 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 134904 ns, RESULT:
        TCS: TestK, time elapsed: 134904 ns, RESULT:
        [ PASSED ] CASE: sayhi (134904 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test.zoo, time elapsed: 132013 ns, RESULT:
        TCS: TestZ, time elapsed: 132013 ns, RESULT:
        [ PASSED ] CASE: sayhi (132013 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 444838 ns, RESULT:
    TP: test.*, time elapsed: 312825 ns, RESULT:
        PASSED:
        TP: test.zoo, time elapsed: 132013 ns
        TP: test.koo, time elapsed: 312825 ns
        TP: test, time elapsed: 312825 ns
    Summary: TOTAL: 3
        PASSED: 3, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

2. Single Package Test Scenario

    ```text
    Input: cjpm test src/koo
    Output:
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 160133 ns, RESULT:
        TCS: TestK, time elapsed: 160133 ns, RESULT:
        [ PASSED ] CASE: sayhi (160133 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 160133 ns, RESULT:
    TP: test.*, time elapsed: 160133 ns, RESULT:
        PASSED:
        TP: test.koo, time elapsed: 160133 ns
    Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

3. Multi-Package Test Scenario

    ```text
    Input: cjpm test src/koo src
    Output:
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 168204 ns, RESULT:
        TCS: TestK, time elapsed: 168204 ns, RESULT:
        [ PASSED ] CASE: sayhi (168204 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test, time elapsed: 171541 ns, RESULT:
        TCS: TestM, time elapsed: 171541 ns, RESULT:
        [ PASSED ] CASE: sayhi (171541 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 339745 ns, RESULT:
    TP: test.*, time elapsed: 339745 ns, RESULT:
        PASSED:
        TP: test.koo, time elapsed: 339745 ns
        TP: test, time elapsed: 339745 ns
    Summary: TOTAL: 2
        PASSED: 2, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

`test` has multiple configurable options:

- `-j, --jobs <N>` Specifies the maximum number of parallel compilations. The final maximum concurrency is the minimum of `N` and `2 times the number of CPU cores`.
- `-V, --verbose` When enabled, outputs unit test logs.
- `-g` Generates a `debug` version of the unit test artifacts, which are stored in the `target/debug/unittest_bin` directory.
- `-i, --incremental` Specifies incremental compilation of test code. Full compilation is performed by default.
- `--no-run` Compiles only the unit test artifacts without execution.
- `--skip-build` Executes only the pre-built unit test artifacts.
- `--coverage` Generates raw coverage data. When using `cjpm test --coverage`, the `main` function in the source code will not be executed as the program entry point and will appear as uncovered. It is recommended to avoid writing redundant `main` functions after using `cjpm test`.
- `--cfg` When specified, custom `cfg` options from `cjpm.toml` are passed through.
- `--module <value>` Specifies the target test module, which must be directly or indirectly dependent on the current module (or be the module itself). Multiple modules can be specified using `--module "module1 module2"`. If not specified, only the current module is tested by default.
- `-m, --member <value>` Can only be used in a workspace to specify testing a single module.
- `--target <value>` When specified, cross-compiles unit test artifacts for the target platform. Refer to the [target](#target) section for `cjpm.toml` configurations.
- `--target-dir <value>` Specifies the output directory for unit test artifacts.
- `--dry-run` When enabled, only prints the test cases without execution.
- `--filter <value>` Filters a subset of tests. The `value` format is as follows:
    - `--filter=*` Matches all test classes.
    - `--filter=*.*` Matches all test cases of all test classes (same result as `*`).
    - `--filter=*.*Test,*.*case*` Matches all test cases ending with `Test` in any test class, or all test cases containing `case` in their names.
    - `--filter=MyTest*.*Test,*.*case*,-*.*myTest` Matches all test cases in classes starting with `MyTest` and ending with `Test`, or containing `case` in their names, or excluding those containing `myTest`.
- `--include-tags <value>` Runs a subset of tests marked with the `@Tag` macro. The `value` format is as follows:
    - `--include-tags=Unittest` Runs all tests marked with `@Tag[Unittest]`.
    - `--include-tags=Unittest,Smoke` Runs all tests marked with either `@Tag[Unittest]` or `@Tag[Smoke]` (or both).
    - `--include-tags=Unittest+Smoke` Runs all tests marked with both `@Tag[Unittest]` and `@Tag[Smoke]`.
    - `--include-tags=Unittest+Smoke+JiraTask3271,Backend` Runs all tests marked with `@Tag[Backend]` or any of `@Tag[Unittest, Smoke, JiraTask3271]`.
- `--exclude-tags <value>` Excludes a subset of tests marked with the `@Tag` macro. The `value` format is as follows:
    - `--exclude-tags=Unittest` Runs all tests not marked with `@Tag[Unittest]`.
    - `--exclude-tags=Unittest,Smoke` Runs all tests not marked with either `@Tag[Unittest]` or `@Tag[Smoke]` (or both).
    - `--exclude-tags=Unittest+Smoke+JiraTask3271` Runs all tests not marked with all of `@Tag[Unittest, Smoke, JiraTask3271]`.
    - `--include-tags=Unittest --exclude-tags=Smoke` Runs all tests marked with `@Tag[Unittest]` but not `@Tag[Smoke]`.
- `--no-color` Disables colored console output.
- `--random-seed <N>` Specifies the value of the random seed.
- `--timeout-each <value>` The format is `%d[millis|s|m|h]`, specifying the default timeout for each test case.
- `--parallel` Specifies the parallel execution scheme for test cases. The `value` format is as follows:
    - `<BOOL>` Can be `true` or `false`. When `true`, test classes can run in parallel, with the number of parallel processes controlled by the available CPU cores.
    - `nCores` Specifies that the number of parallel test processes equals the available CPU cores.
    - `NUMBER` Specifies a positive integer for the number of parallel test processes.
    - `NUMBERnCores` Specifies that the number of parallel test processes is a multiple of the available CPU cores. The value must be positive (supports floating-point or integer values).
- `--show-tags` Displays `@Tag` information in the test report. In `--dry-run` mode with `xml` format reports, `Tag` information is always included.
- `--show-all-output` Enables output printing for all test cases, including passed ones.
- `--no-capture-output` Disables test output capture, printing output immediately during test execution.
- `--report-path <value>` Specifies the path for generating test execution reports.
- `--report-format <value>` Specifies the report output format. Currently, only `xml` and `xml-per-package` format (case-insensitive) is supported for unit test reports. Other values will throw an exception.
- `--skip-script` Skips the compilation and execution of build scripts.
- `--no-progress` Disables progress reporting. Implicitly enabled if `--dry-run` is specified.
- `--progress-brief` Displays a brief (single-line) progress report instead of a detailed one.
- `--progress-entries-limit <value>` Limits the number of entries displayed in the progress report. Default: `0`. Allowed values:
    - `0` No limit on the number of entries.
    - `n` Where `n` is a positive integer, specifying the maximum number of entries displayed simultaneously in the terminal.

Examples of `cjpm test` parameter usage:

```text
Input:
cjpm test src --coverage
cjcov --root=./ --html-details -o html_output
Output: cjpm test success
Coverage generation: HTML files are generated in the html_output directory, with the main coverage report file named index.html.
```

```text
Input: cjpm test --filter=*
Output: cjpm test success
```

```text
Input: cjpm test src --report-path=reports --report-format=xml
Output: cjpm test success
```

> **Note:**
>
> `cjpm test` automatically builds all packages with `mock` support, allowing developers to perform `mock` tests on custom classes or classes from dependent modules. To enable `mock` for classes from binary dependencies, build with `mock` support using `cjpm build --mock`. Avoid writing redundant `main` functions after using `cjpm test`.

### bench

The `bench` command is used to execute performance test cases in test files and directly print the test results. The compiled artifacts are stored by default in the `target/release/unittest_bin` directory. Performance test cases are annotated with the `@Bench` macro. For more details on how to write performance test code, refer to the description of the `std.unittest` library in the *Cangjie Programming Language Standard Library API*.

This command can specify the path of a single package to test (multiple packages can be specified, e.g., `cjpm bench path1 path2`). If no path is specified, module-level unit tests are executed by default. Similar to `test`, when executing module-level unit tests, only the current module's unit tests are performed by default. The `bench` command requires that the current project can be successfully compiled with `build`.

Like the `test` subcommand, if you have an `xxx.cj` file, `xxx_test.cj` can also contain performance test cases.

```text
Input: cjpm bench
Output:
TP: bench, time elapsed: 8107939844 ns, RESULT:
    TCS: Test_UT, time elapsed: 8107939844 ns, RESULT:
    | Case       |   Median |         Err |   Err% |     Mean |
    |:-----------|---------:|------------:|-------:|---------:|
    | Benchmark1 | 5.438 ns | ±0.00439 ns |  ±0.1% | 5.420 ns |
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
Project tests finished, time elapsed: 8107939844 ns, RESULT:
TP: bench.*, time elapsed: 8107939844 ns, RESULT:
    PASSED:
    TP: bench, time elapsed: 8107939844 ns, RESULT:
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
```

`bench` has several configurable options:

- `-j, --jobs <N>`: Specifies the maximum number of parallel compilation jobs. The final maximum concurrency is the minimum of `N` and `2 × CPU cores`.
- `-V, --verbose`: When enabled, outputs unit test logs.
- `-g`: Generates a `debug` version of the unit test artifacts, which are stored in the `target/debug/unittest_bin` directory.
- `-i, --incremental`: Specifies incremental compilation for test code. Full compilation is performed by default.
- `--no-run`: Only compiles unit test artifacts without executing them.
- `--skip-build`: Only executes unit test artifacts without compiling them.
- `--cfg`: Allows passing custom `cfg` options from `cjpm.toml`.
- `--module <value>`: Specifies the target test module. The specified module must be directly or indirectly dependent on the current module (or be the module itself). Multiple modules can be specified using `--module "module1 module2"`. If not specified, only the current module is tested.
- `-m, --member <value>`: Only usable in a workspace, specifies a single module to test.
- `--target <value>`: Specifies cross-compilation for the target platform. Refer to the `cross-compile-configuration` section in `cjpm.toml` for configuration details.
- `--target-dir <value>`: Specifies the output directory for unit test artifacts.
- `--dry-run`: Prints the test cases without executing them.
- `--filter <value>`: Filters a subset of tests. The `value` format is as follows:
    - `--filter=*`: Matches all test classes.
    - `--filter=*.*`: Matches all test cases in all test classes (same result as `*`).
    - `--filter=*.*Test,*.*case*`: Matches all test cases ending with `Test` or containing `case` in their names.
    - `--filter=MyTest*.*Test,*.*case*,-*.*myTest`: Matches all test cases in classes starting with `MyTest` and ending with `Test`, or containing `case` in their names, but excludes those containing `myTest`.
- `--include-tags <value>`: Runs tests annotated with the specified `@Tag` macro subsets. The `value` format is as follows:
    - `--include-tags=Unittest`: Runs all tests marked with `@Tag[Unittest]`.
    - `--include-tags=Unittest,Smoke`: Runs all tests marked with either `@Tag[Unittest]` or `@Tag[Smoke]` (or both).
    - `--include-tags=Unittest+Smoke`: Runs all tests marked with both `@Tag[Unittest, Smoke]`.
    - `--include-tags=Unittest+Smoke+JiraTask3271,Backend`: Runs all tests marked with `@Tag[Backend]` or `@Tag[Unittest, Smoke, JiraTask3271]`.
- `--exclude-tags <value>`: Excludes tests annotated with the specified `@Tag` macro subsets. The `value` format is as follows:
    - `--exclude-tags=Unittest`: Runs all tests not marked with `@Tag[Unittest]`.
    - `--exclude-tags=Unittest,Smoke`: Runs all tests not marked with either `@Tag[Unittest]` or `@Tag[Smoke]` (or both).
    - `--exclude-tags=Unittest+Smoke+JiraTask3271`: Runs all tests not marked with `@Tag[Unittest, Smoke, JiraTask3271]`.
    - `--include-tags=Unittest --exclude-tags=Smoke`: Runs all tests marked with `@Tag[Unittest]` but not `@Tag[Smoke]`.
- `--no-color`: Disables colored console output.
- `--show-tags` is used to display `@Tag` information from test cases in the test report. In `--dry-run` mode with the test report in `xml` format, `Tag` information will always be included.
- `--random-seed <N>`: Specifies the random seed value.
- `--report-path <value>`: Specifies the path for the generated report. Unlike the `test` subcommand, it defaults to `bench_report`.
- `--report-format <value>`: Performance test reports only support `csv` and `csv-raw` formats.
- `--baseline-path <value>`: Path to an existing report for comparison with current performance results. By default, it uses the `--report-path` value.
- `--skip-script`: Skips the compilation and execution of build scripts.

Example usage of `cjpm bench` options:

```text
Input: cjpm bench
Output: cjpm bench success

Input: cjpm bench src
Output: cjpm bench success

Input: cjpm bench src --filter=*
Output: cjpm bench success

Input: cjpm bench src --report-format=csv
Output: cjpm bench success
```

> **Note:**
>
> `cjpm bench` does not fully support `mock` to avoid any overhead from `mock` processing in the compiler during benchmarking.
> When using `cjpm bench` options, the compiler will not report errors if `mock` is used, allowing regular tests and benchmarks to be compiled together. However, avoid running benchmarks that use `mock`, as this will throw a runtime exception.

### clean

The `clean` command removes temporary build artifacts (the `target` directory). It supports the short option `-g` to clean only `debug` artifacts and the long option `--target-dir <value>` to specify the directory to clean. Developers must ensure the safety of cleaning the specified directory. If `cjpm build --coverage` or `cjpm test --coverage` was used, it also removes the `cov_output` directory and `*.gcno`/`*.gcda` files in the current directory. The `--skip-script` option skips the compilation and execution of build scripts.

Examples:

```text
Input: cjpm clean
Output: cjpm clean success
```

```text
Input: cjpm clean --target-dir temp
Output: cjpm clean success
```

> **Note:**
>
> On Windows, cleaning executable files or parent directories immediately after subprocess execution may fail. If this occurs, retry the `clean` command after a short delay.

### install

The `install` command installs a Cangjie project. It first compiles the project and then installs the artifacts to the specified path, naming them after the project (with `.exe` suffix on Windows). The installed project must be of type `executable`.

`install` has several configurable options:

- `-V, --verbose`: Shows installation logs.
- `-m, --member <value>`: Only usable in a workspace, specifies a single module to install.
- `-g`: Generates a `debug` version of the installation artifacts.
- `--path <value>`: Specifies the local project path to install. Defaults to the current directory.
- `--root <value>`: Specifies the installation path for executables. Defaults to `$HOME/.cjpm` on Linux/macOS and `%USERPROFILE%/.cjpm` on Windows.
- `--git <value>`: Specifies the Git URL of the project to install.
- `--branch <value>`: Specifies the Git branch to install.
- `--tag <value>`: Specifies the Git tag to install.
- `--commit <value>`: Specifies the Git commit ID to install.
- `-j, --jobs <N>`: Specifies the maximum number of parallel compilation jobs. The final maximum concurrency is the minimum of `N` and `2 × CPU cores`.
- `--cfg`: Allows passing custom `cfg` options from `cjpm.toml`.
- `--target-dir <value>`: Specifies the output directory for compilation artifacts.
- `--name <value>`: Specifies the name of the installed artifact.
- `--skip-build`: Skips the compilation phase and directly installs artifacts. Requires the project to be already compiled and only works for local installations.
- `--list`: Prints the list of installed artifacts.
- `--skip-script`: Skips the compilation and execution of build scripts for the module to install.

Notes on `install`:

- Two installation methods: local project (via `--path`) and Git project (via `--git`). Only one can be configured; otherwise, `install` will error. If neither is specified, the current directory's local project is installed by default.
- Incremental compilation is enabled by default.
- Git-related options (`--branch`, `--tag`, `--commit`) are ignored unless `--git` is specified. Priority: `--commit` > `--branch` > `--tag`.
- Existing executables with the same name will be replaced.
- Executables are installed to `root/bin`, where `root` is the specified or default installation path.
- Dynamic library dependencies are installed to `root/libs`, organized by program name. Add the corresponding directory to `LD_LIBRARY_PATH` (Linux), `PATH` (Windows), or `DYLD_LIBRARY_PATH` (macOS) for usage.
- The default installation path is added to `PATH` during `envsetup`.
- Git project installation removes the compilation artifacts directory afterward.
- If the project has only one executable artifact, `--name` renames it during installation. For multiple artifacts, `--name` installs only the specified artifact.
- `--list` prints installed artifacts, ignoring all options except `--root`. With `--root`, it prints artifacts in the specified path; otherwise, it uses the default path.

Examples:

```text
cjpm install --path path/to/project # Installs from a local path
cjpm install --git url              # Installs from a Git URL
```

### uninstall

The `uninstall` command removes a Cangjie project, deleting its executables and dependency files.

`uninstall` requires the `name` parameter to specify the artifact to uninstall. Multiple names can be specified for sequential removal. The `--root <value>` option specifies the installation path to uninstall (defaults to `$HOME/.cjpm` on Linux/macOS and `%USERPROFILE%/.cjpm` on Windows). Artifacts in `root/bin` and dependencies in `root/libs` are removed.

> **Note:**
>
> `cjpm` does not support Chinese paths on Windows. If issues arise, modify the directory name.

## Module Configuration File Description

The `cjpm.toml` file configures basic information, dependencies, compilation options, etc. `cjpm` primarily uses this file for parsing and execution. Module names can be renamed in `cjpm.toml`, but package names cannot.

Example configuration:

```text
[package] # Single-module configuration (cannot coexist with workspace)
  cjc-version = "1.0.0" # Minimum required `cjc` version (required)
  name = "demo" # Module name and root package name (required)
  description = "nothing here" # Description (optional)
  version = "1.0.0" # Module version (required)
  compile-option = "" # Additional compilation options (optional)
  override-compile-option = "" # Additional global compilation options (optional)
  link-option = "" # Linker passthrough options (optional)
  output-type = "executable" # Output type (required)
  src-dir = "" # Source directory (optional)
  target-dir = "" # Output directory (optional)
  package-configuration = {} # Per-package configuration (optional)

[workspace] # Workspace configuration (cannot coexist with package)
  members = [] # Workspace member modules (required)
  build-members = [] # Modules to build (subset of members, optional)
  test-members = [] # Modules to test (subset of build-members, optional)
  compile-option = "" # Workspace-wide compilation options (optional)
  override-compile-option = "" # Workspace-wide global compilation options (optional)
  link-option = "" # Workspace-wide linker options (optional)
  target-dir = "" # Output directory (optional)

[dependencies] # Source dependencies (optional)
  coo = { git = "xxx", branch = "dev" } # Git dependency
  doo = { path = "./pro1" } # Local source dependency

[test-dependencies] # Test-phase dependencies (same format as dependencies, optional)

[script-dependencies] # Build script dependencies (same format as dependencies, optional)

[replace] # Dependency replacement (same format as dependencies, optional)

[ffi.c] # C library dependencies (optional)
  clib1.path = "xxx"

[profile] # Command profile configuration (optional)
  build = {} # Build command options
  test = {} # Test command options
  bench = {} # Bench command options
  customized-option = {} # Custom passthrough options

[target.x86_64-unknown-linux-gnu] # Platform-specific configuration (optional)
  compile-option = "value1" # Compilation options for specific targets
  override-compile-option = "value2" # Global compilation options for specific targets
  link-option = "value3" # Linker options for specific targets

[target.x86_64-w64-mingw32.dependencies] # Platform-specific source dependencies (optional)

[target.x86_64-w64-mingw32.test-dependencies] # Platform-specific test dependencies (optional)

[target.x86_64-unknown-linux-gnu.bin-dependencies] # Binary library dependencies for specific targets (optional)
  path-option = ["./test/pro0", "./test/pro1"] # Directory-based binary dependencies
[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option] # File-based binary dependencies
  "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
  "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
  "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
```

For detailed information about CJO files, see [CJO Artifacts](../../../dev-guide/source_en/Appendix/cjo_artifacts.md).

Unused fields default to empty (for paths, the default is the directory containing the configuration file).

### "cjc-version"

Minimum required Cangjie compiler version. Must be compatible with the current environment. A valid version number consists of three natural numbers separated by `.`, with no leading zeros. Examples:

- `1.0.0`: Valid.
- `1.00.0`: Invalid (leading zero in `00`).
- `1.2e.0`: Invalid (`2e` is not a natural number).

### "name"

Current Cangjie module name, also the root package name. Must be a valid identifier (letters, numbers, underscores, starting with a letter). Examples: `cjDemo`, `cj_demo_1`.

> **Note:**
>
> Unicode characters are not supported. Module names must be ASCII-only identifiers.

### "description"

Module description (free-form text).

### "version"

Module version number, managed by the module owner. Format is the same as `cjc-version`.

### "compile-option"

Additional compilation options passed to `cjc`. In multi-module builds, each module's `compile-option` applies to all its packages.

Example:

```text
compile-option = "-O1 -V"
```

Commands are inserted into the compilation command during `build`. Multiple commands can be separated by spaces. Refer to the *Cangjie Programming Language Development Guide* for available options.

### "override-compile-option"

Additional global compilation options passed to `cjc`. In multi-module builds, the entry module's `override-compile-option` applies to all dependent modules' packages.

Example:

```text
override-compile-option = "-O1 -V"
```

Commands are appended after `compile-option` and take higher precedence. Refer to the *Cangjie Programming Language Development Guide* for available options.

> **Note:**
>
> - `override-compile-option` affects dependent modules. Ensure no conflicts with their `compile-option`.
> - In workspaces, only the `workspace`'s `override-compile-option` applies to all modules.

### "link-option"

Linker passthrough options, e.g., for secure compilation:

```text
link-option = "-z noexecstack -z relro -z now --strip-all"
```

> **Note:**
>
> Only applies to dynamic libraries and executables.

### "output-type"

Output artifact type: `executable`, `static` (static library), or `dynamic` (dynamic library). Defaults to `executable` for `cjpm init`.

|     Input     |               Description |
| :----------: | :---------------------: |
| "executable" |         Executable program |
|   "static"   | Static library |
|  "dynamic"   | Dynamic library |
|    Others    |               Error report |

### "src-dir"

This field can specify the source code storage path. If not specified, it defaults to the `src` directory.

### "target-dir"

This field can specify the output directory for compiled artifacts. If not specified, it defaults to the `target` directory. If this field is not empty, executing `cjpm clean` will delete the directory specified by this field. Developers must ensure the safety of clearing this directory.

> **Note:**
>
> If the `--target-dir` option is specified during compilation, this option will take higher precedence.

```text
target-dir = "temp"
```

### "package-configuration"

Per-package configuration options for individual modules. This option is a `map` structure, where the package name to be configured serves as the `key`, and the package-specific configuration serves as the `value`. Currently configurable options include output type and conditional options (`output-type`, `compile-option`). These options can be omitted and configured as needed. As shown below, the output type of the `demo.aoo` package in the `demo` module will be specified as a dynamic library, and the `-g` command will be passed through to the `demo.aoo` package during compilation.

```text
[package.package-configuration."demo.aoo"]
  output-type = "dynamic"
  compile-option = "-g"
```

If mutually compatible compilation options are configured in different fields, the priority of the generated commands is as follows.

```text
[package]
  compile-option = "-O1"
[package.package-configuration.demo]
  compile-option = "-O2"

# The profile field will be introduced later
[profile.customized-option]
  cfg1 = "-O0"

Input: cjpm build --cfg1 -V
Output: cjc --import-path build -O0 -O1 -O2 ...
```

By configuring this field, multiple binary artifacts can be generated simultaneously (when generating multiple binary artifacts, the `-o, --output <value>` option will be invalid). Example:

Example of source code structure, with the module named `demo`:

```text
src
├── aoo
│    └── aoo.cj
├── boo
│    └── boo.cj
├── coo
│    └── coo.cj
└──  main.cj
```

Example of configuration:

```text
[package.package-configuration."demo.aoo"]
  output-type = "executable"
[package.package-configuration."demo.boo"]
  output-type = "executable"
```

Example of multiple binary artifacts:

```text
Input: cjpm build
Output: cjpm build success

Input: tree target/release/bin
Output: target/release/bin
|-- demo.aoo
|-- demo.boo
`-- demo
```

### "workspace"

This field can manage multiple modules as a workspace, supporting the following configuration items:

- `members = ["aoo", "path/to/boo"]`: Lists local source code modules included in this workspace, supporting absolute and relative paths. Members of this field must be modules and cannot be another workspace.
- `build-members = []`: Modules to be compiled this time. If not specified, all modules in the workspace are compiled by default. Members of this field must be included in the `members` field.
- `test-members = []`: Modules to be tested this time. If not specified, unit tests are run on all modules in the workspace by default. Members of this field must be included in the `build-members` field.
- `compile-option = ""`: Public compilation options for the workspace (optional).
- `override-compile-option = ""`: Public global compilation options for the workspace (optional).
- `link-option = ""`: Public linking options for the workspace (optional).
- `target-dir = ""`: Output directory for the workspace (optional, defaults to `target`).

Public configuration items in the workspace apply to all member modules. For example: If a source dependency like `[dependencies] xoo = { path = "path_xoo" }` is configured, all member modules can directly use the `xoo` module without needing to configure it in each submodule's `cjpm.toml`.

> **Note:**
>
> The `package` field is used to configure general module information and cannot coexist with the `workspace` field in the same `cjpm.toml`. All other fields except `package` can be used in the workspace.

Example of a workspace directory structure:

```text
root_path
├── aoo
│    ├── src
│    └── cjpm.toml
├── boo
│    ├── src
│    └── cjpm.toml
├── coo
│    ├── src
│    └── cjpm.toml
└── cjpm.toml
```

Example of workspace configuration file usage:

```text
[workspace]
members = ["aoo", "boo", "coo"]
build-members = ["aoo", "boo"]
test-members = ["aoo"]
compile-option = "-Woff all"
override-compile-option = "-O2"

[dependencies]
xoo = { path = "path_xoo" }

[ffi.c]
abc = { path = "libs" }
```

### "dependencies"

This field imports other Cangjie modules as dependencies via source code, containing information about other modules required for the current build. Currently, it supports both local path dependencies and remote `git` dependencies.

To specify a local dependency, use the `path` field, which must contain a valid local path. For example, the code structure of the two submodules `pro0` and `pro1` and the main module is as follows:

```text
├── pro0
│    ├── cjpm.toml
│    └── src
│         └── zoo
│              └── zoo.cj
├── pro1
│    ├── cjpm.toml
│    └── src
│         ├── xoo
│         │    └── xoo.cj
│         └── yoo
│              └── yoo.cj
├── cjpm.toml
└── src
     ├── aoo
     │    └── aoo.cj
     ├── boo
     │    └── boo.cj
     └── main.cj
```

After configuring the main module's `cjpm.toml` as follows, the `pro0` and `pro1` modules can be used in the source code:

```text
[dependencies]
  pro0 = { path = "./pro0" }
  pro1 = { path = "./pro1" }
```

To specify a remote `git` dependency, use the `git` field, which must contain a valid `url` in any format supported by `git`. To configure a `git` dependency, at most one `branch`, `tag`, or `commitId` field can be included to select a specific branch, tag, or commit hash, respectively. If multiple such fields are configured, only the highest-priority configuration will take effect, with the priority order being `commitId` > `branch` > `tag`. For example, after configuring as follows, the `pro0` and `pro1` modules from the specified `git` repository can be used in the source code:

```text
[dependencies]
  pro0 = { git = "https://github.com/example", tag = "v1.0.0"}
  pro1 = { git = "https://gitee.com/example", branch = "dev"}
```

In this case, `cjpm` will download the latest version of the corresponding repository and save the current `commit-hash` in the `cjpm.lock` file. All subsequent `cjpm` calls will use the saved version until `cjpm update` is executed.

Authentication is often required to access `git` repositories. `cjpm` does not request credentials, so existing `git` authentication support should be used. If the protocol for `git` is `https`, an existing git credential helper must be used. On `Windows`, the credential helper is installed by default with `git`. On `Linux/macOS`, refer to the `git-config` documentation in the official `git` documentation for details on setting up a credential helper. If the protocol is `ssh` or `git`, key-based authentication should be used. If the key is protected by a passphrase, the developer must ensure that `ssh-agent` is running and the key is added via `ssh-add` before using `cjpm`.

The `dependencies` field can specify the compilation output type via the `output-type` attribute. The specified type can differ from the compilation output type of the source dependency itself and can only be `static` or `dynamic`, as shown below:

```text
[dependencies]
  pro0 = { path = "./pro0", output-type = "static" }
  pro1 = { git = "https://gitee.com/example", output-type = "dynamic" }
```

After the above configuration, the `output-type` settings in the `cjpm.toml` files of `pro0` and `pro1` will be ignored, and the two modules' outputs will be compiled into `static` and `dynamic` types, respectively.

### "test-dependencies"

This field has the same format as the `dependencies` field. It is used to specify dependencies that are only used during testing and not required for building the main project. Module developers should use this field for dependencies that downstream users of this module do not need to be aware of.

Dependencies within `test-dependencies` can only be used in test files named like `xxx_test.cj`. During compilation, these dependencies will not be compiled. The configuration format of `test-dependencies` in `cjpm.toml` is the same as that of `dependencies`.

### "script-dependencies"

This field has the same format as the `dependencies` field. It is used to specify dependencies that are only used during build script compilation and not required for building the main project. Build script-related features will be detailed in the [Other-Build Scripts](#build-scripts) section.

### "replace"

This field has the same format as the `dependencies` field. It is used to specify replacements for indirect dependencies with the same name. The configured dependencies will be the final versions used when compiling the module.

For example, the module `aaa` depends on a local module `bbb`:

```text
[package]
  name = "aaa"

[dependencies]
  bbb = { path = "path/to/bbb" }
```

When the main module `demo` depends on `aaa`, `bbb` becomes an indirect dependency of `demo`. In this case, if the main module `demo` wants to replace `bbb` with another module of the same name (e.g., the `bbb` module under another path `new/path/to/bbb`), it can be configured as follows:

```text
[package]
  name = "demo"

[dependencies]
  aaa = { path = "path/to/aaa" }

[replace]
  bbb = { path = "new/path/to/bbb" }
```

After configuration, the actual indirect dependency `bbb` used when compiling the `demo` module will be the `bbb` module under `new/path/to/bbb`, and the `bbb` module under `path/to/bbb` configured in `aaa` will not be compiled.

> **Note:**
>
> Only the `replace` field of the entry module takes effect during compilation.

### "ffi.c"

This field configures external `C` library dependencies for the current Cangjie module. It contains the information required to depend on the library, including the library name and path.

Developers need to compile the dynamic or static library themselves and place it under the specified `path`. Refer to the example below.

Instructions for calling external `C` dynamic libraries in Cangjie:

- Compile the corresponding `hello.c` file into a `.so` library (execute `clang -shared -fPIC hello.c -o libhello.so` in the file path).
- Modify the project's `cjpm.toml` file to configure the `ffi.c` field, as shown in the example below. Here, `./src/` is the relative path of the compiled `libhello.so` to the current directory, and `hello` is the library name.
- Execute `cjpm build` to compile successfully.

```text
[ffi.c]
hello = { path = "./src/" }
```

To specify `C` library configurations for different platforms, refer to [target](#target).

> **Note:**
>
> In multi-module scenarios on `Windows` systems, if multiple modules configure libraries with the same name `c`, due to the unique library loading strategy of `Windows`, the system will prioritize loading library files from the runtime directory first. As a result, the actual library file used may differ from those on other systems.

### "profile"

`profile` is a command profile configuration item used to control default settings during command execution. Currently, the following scenarios are supported: `build`, `test`, `bench`, `run`, and `customized-option`.

#### "profile.build"

```text
[profile.build]
lto = "full"  # Whether to enable `LTO` (Link Time Optimization) compilation mode. This feature is only supported on `Linux` platforms.
performance_analysis = true # Enable compilation performance analysis.
incremental = true # Whether to enable incremental compilation by default.
[profile.build.combined]
demo = "dynamic" # Compile the module into a single dynamic library file. The key is the module name.
```

Compilation process control items. All fields are optional and will not take effect if not configured. Only the `profile.build` settings of the top-level module take effect.

The `lto` configuration can be `full` or `thin`, corresponding to two compilation modes supported by `LTO` optimization: `full LTO` merges all compilation modules for global optimization, offering the highest optimization potential but requiring longer compilation time; `thin LTO` uses parallel optimization across multiple modules and supports incremental compilation during linking by default, with shorter compilation time than `full LTO` but less optimization due to reduced global information.

The `performance_analysis` configuration can be `true` or `false`, indicating whether to enable compilation performance analysis. When enabled, `cjpm` generates `.prof` and `.json` files in the `performance_analysis` directory under the compilation output directory, recording time and memory consumption during compilation. For example, if the default compilation output directory is `target` and the compilation mode is `debug`, the directory structure is as follows:

```text
demo
├── cjpm.toml
├── src
|   └── demo.cj
└── target
    └── debug
        └── performance_analysis
            ├── xxx1.prof
            ├── ...
            ├── xxxN.prof
            ├── xxx1.json
            ├── ...
            └── xxxN.json
```

The `combined` configuration is a key-value pair where the key is the module name (`package.name`) and the value is `dynamic`. Before configuring this, the module compiles each package into separate dynamic or static library files based on `package.output-type`. After configuration, the module's compilation method changes to:

- Subpackages other than `root` are compiled as static libraries.
- The `root` package is compiled as a dynamic library, linking all subpackage static libraries, regardless of whether the subpackages are dependencies of the `root` package. When other modules depend on this dynamic library as a binary dependency, they can use all symbols from the subpackages.

For example, assume the module `demo` has the following structure:

```text
demo
├── cjpm.toml
└── src
     ├── aoo
     |    └── aoo.cj
     ├── boo
     |    └── boo.cj
     └── demo.cj
```

The module configuration file `cjpm.toml` is configured as follows:

```text
[package]
name = "demo"

[profile.build.combined]
demo = "dynamic"
```

After compilation, the final output directory `target/release/demo` will contain the following files (using `Linux` as an example):

```text
|-- libdemo.so
|-- libdemo.aoo.a
|-- libdemo.boo.a
|-- demo.cjo
|-- demo.aoo.cjo
|-- demo.boo.cjo
```

Module developers can provide all `cjo` files and the `root` package dynamic library `libdemo.so` to other modules as binary dependencies without providing the subpackage static library files. After other modules depend on this dynamic library, they can depend on all its subpackages in code, such as importing `demo.aoo` via `import demo.aoo`.

> **Note:**
>
> - When applying this configuration, compiling the `root` package dynamic library requires all subpackage static libraries, so ensure the `root` package is not directly or indirectly imported by its subpackages.
> - Currently, the `profile.build.combined` configuration is experimental and unstable. Developers enabling this configuration should note the following limitations:
>     - If a module configured with this field directly or indirectly depends on other source modules, those dependent modules must also be configured with this field.
>     - Source modules depended on by build scripts will not take effect if configured with `profile.build.combined`.
>     - The `profile.build.combined` option is not supported when the compilation target platform is `macOS`.

If `combined` is enabled, cyclic dependencies not identifiable via imports may occur, resulting in `cyclic dependency` errors. Solutions are as follows:

- If the error message includes `because of combined module 'demo'`, it means the module `demo` is configured as a `combined` module, and a subpackage of `demo` directly or indirectly depends on the `root` package. Developers can locate and remove such imports or disable the `combined` configuration to resolve the issue.
- If the error message includes `between combined modules`, it means both `root` packages in the entry are configured as `combined` modules, and there are mutual dependencies between them (including subpackages). Developers can locate and remove imports from one `combined` module to another or disable both `combined` configurations to resolve the issue.

#### "profile.test"

```text
[profile.test] # Example usage
parallel=true
filter=*.*
no-color = true
timeout-each = "4m"
random-seed = 10
bench = false
report-path = "reports"
report-format = "xml"
verbose = true
[profile.test.build]
  compile-option = ""
  lto = "thin"
  mock = "on"
[profile.test.env]
MY_ENV = { value = "abc" }
cjHeapSize = { value = "32GB", splice-type = "replace" }
PATH = { value = "/usr/bin", splice-type = "prepend" }
```

Test configuration supports specifying options during test compilation and execution. All fields are optional and will not take effect if not configured. Only the `profile.test` settings of the top-level module take effect. The option list aligns with the console execution options provided by `cjpm test`. If an option is configured in both the configuration file and the console, the console option takes precedence. `profile.test` supports the following runtime options:

- `filter`: Specifies the test case filter. The value is a string with the same format as the `--filter` value in the [test command description](#test).
- `timeout-each <value>`: The `value` format is `%d[millis|s|m|h]`, specifying the default timeout for each test case.
- `parallel`: Specifies the parallel execution scheme for test cases. The `value` can be:
    - `<BOOL>`: `true` or `false`. If `true`, test classes can run in parallel, with the number of parallel processes controlled by the CPU cores available on the system.
    - `nCores`: The number of parallel test processes equals the available CPU cores.
    - `NUMBER`: The number of parallel test processes. Must be a positive integer.
    - `NUMBERnCores`: The number of parallel test processes is a multiple of the available CPU cores. Must be a positive number (supports integers or floats).
- `option:<value>`: Works with `@Configure` to define runtime options. For example:
    - `random-seed`: Specifies the random seed value. Must be a positive integer.
    - `no-color`: Specifies whether to disable colored output in the console. Can be `true` or `false`.
    - `report-path`: Specifies the path for test execution reports (cannot be configured via `@Configure`).
    - `report-format`: Specifies the report output format. Currently, unit test reports only support `xml` and `xml-per-package` format (case-insensitive). Other values will throw an exception (cannot be configured via `@Configure`). Performance test reports only support `csv` and `csv-raw` formats.
    - `verbose`: Specifies whether to display detailed compilation information. Can be `true` or `false`.

#### "profile.test.build"

Specifies supported compilation options, including:

- `compile-option`: A string containing additional `cjc` compilation options, supplementing the top-level `compile-option` field.
- `lto`: Specifies whether to enable `LTO` optimization. Can be `thin` or `full`. Only supported on `Linux` platforms.
- `mock`: Explicitly sets the `mock` mode. Possible values: `on`, `off`, `runtime-error`. The default value for `test`/`build` subcommands is `on`, and for `bench` subcommands, it is `runtime-error`.

#### "profile.test.env"

Configures temporary environment variables when running executables during the `test` command. The `key` is the name of the environment variable to configure, with the following options:

- `value`: Specifies the environment variable value.
- `splice-type`: Specifies how to splice the environment variable. Optional; defaults to `absent`. Possible values:
    - `absent`: The configuration only takes effect if no environment variable with the same name exists. If one exists, the configuration is ignored.
    - `replace`: The configuration replaces any existing environment variable with the same name.
    - `prepend`: The configuration is prepended to any existing environment variable with the same name.
    - `append`: The configuration is appended to any existing environment variable with the same name.

#### "profile.bench"

```text
[profile.bench] # Example usage
no-color = true
random-seed = 10
report-path = "bench_report"
baseline-path = ""
report-format = "csv"
verbose = true
```

Benchmark configuration supports specifying options during benchmark compilation and execution. All fields are optional and will not take effect if not configured. Only the `profile.bench` settings of the top-level module take effect. The option list aligns with the console execution options provided by `cjpm bench`. If an option is configured in both the configuration file and the console, the console option takes precedence. `profile.bench` supports the following runtime options:

- `filter`: Specifies the benchmark case filter. The value is a string with the same format as the `--filter` value in the [bench command description](#bench).
- `option:<value>`: Works with `@Configure` to define runtime options. For example:
    - `random-seed`: Specifies the random seed value. Must be a positive integer.
    - `no-color`: Specifies whether to disable colored output in the console. Can be `true` or `false`.
    - `report-path`: Specifies the path for benchmark execution reports (cannot be configured via `@Configure`).
    - `report-format`: Specifies the report output format. Currently, unit test reports only support `xml` and `xml-per-package` format (case-insensitive). Other values will throw an exception (cannot be configured via `@Configure`). Performance test reports only support `csv` and `csv-raw` formats.
    - `verbose`: Specifies whether to display detailed compilation information. Can be `true` or `false`.
    - `baseline-path`: The path of an existing report to compare with the current performance results. By default, it uses the `--report-path` value.

#### "profile.bench.build"

Used to specify additional compilation options when building executables for `cjpm bench`. Shares the same configuration as `profile.test.build`.

#### "profile.bench.env"

Supports configuring environment variables when running executables with the `bench` command, following the same configuration method as `profile.test.env`.

#### "profile.run"

Options for running executables, supporting environment variable configuration `env` when executing the `run` command, following the same configuration method as `profile.test.env`.

#### "profile.customized-option"

```text
[profile.customized-option]
cfg1 = "--cfg=\"feature1=lion, feature2=cat\""
cfg2 = "--cfg=\"feature1=tiger, feature2=dog\""
cfg3 = "-O2"
```

Custom options passed through to `cjc`. Enabled via `--cfg1 --cfg3`. The `customized-option` set for each module applies to all packages within that module. For example, when executing `cjpm build --cfg1 --cfg3`, the command passed to `cjc` would be `--cfg="feature1=lion, feature2=cat" -O2`.

> **Note:**
>
> The conditional value here must be a valid identifier.

### "target"

Multi-backend, multi-platform isolation options for configuring different settings across various backends and platforms. Taking the `Linux` system as an example, the `target` configuration is as follows:

```text
[target.x86_64-unknown-linux-gnu] # Configuration items for Linux systems
  compile-option = "value1" # Additional compilation command options
  override-compile-option = "value2" # Additional global compilation command options
  link-option = "value3" # Linker passthrough options
  [target.x86_64-unknown-linux-gnu.dependencies] # Source dependency configuration
  [target.x86_64-unknown-linux-gnu.test-dependencies] # Test-phase dependency configuration
  [target.x86_64-unknown-linux-gnu.bin-dependencies] # Cangjie binary library dependencies
    path-option = ["./test/pro0", "./test/pro1"]
  [target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
    "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
    "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
    "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
  [target.x86_64-unknown-linux-gnu.ffi.c] # C language binary library dependencies
    "ctest" = "./test/c"

[target.x86_64-unknown-linux-gnu.debug] # Debug configuration for Linux systems
  [target.x86_64-unknown-linux-gnu.debug.test-dependencies]

[target.x86_64-unknown-linux-gnu.release] # Release configuration for Linux systems
  [target.x86_64-unknown-linux-gnu.release.bin-dependencies]
```

Developers can add a series of configuration items for a specific `target` by configuring the `target.target-name` field. The `target` name can be obtained in the corresponding Cangjie environment via the command `cjc -v`, where the `Target` item in the command output represents the `target` name for that environment. The above example applies to the `Linux` system but is also applicable to other platforms, where the `target` name can similarly be obtained via `cjc -v`.

Dedicated configuration items for a specific `target` will apply to the compilation process for that `target`, as well as cross-compilation processes where other `targets` specify this `target` as the target platform. The list of configurable items includes:

- `compile-option`: Additional compilation command options
- `override-compile-option`: Additional global compilation command options
- `link-option`: Linker passthrough options
- `dependencies`: Source dependency configuration, structured similarly to the `dependencies` field
- `test-dependencies`: Test-phase dependency configuration, structured similarly to the `test-dependencies` field
- `bin-dependencies`: Cangjie binary library dependencies, described below
- `ffi.c`: Configuration for external C library dependencies in Cangjie modules, structured similarly to the `ffi.c` field
- `compile-macros-for-target`: Macro package control items for cross-compilation, which do not support distinguishing between `debug` and `release` compilation modes below

Developers can configure `target.target-name.debug` and `target.target-name.release` fields to specify additional configurations unique to `debug` and `release` compilation modes for that `target`. The configurable items are the same as above. Configurations under these fields will only apply to the corresponding compilation mode of the `target`.

#### "target.target-name[.debug/release].bin-dependencies"

This field is used to import pre-compiled Cangjie library output files suitable for the specified `target`. The following example demonstrates importing three packages from the `pro0` and `pro1` modules.

> **Note:**
>
> Unless specifically required, it is not recommended to use this field. Instead, use the `dependencies` field described earlier to import module source code.

```text
├── test
│    ├── pro0
│    │    ├── libpro0.xoo.so
│    │    ├── pro0.xoo.cjo
│    │    ├── libpro0.yoo.so
│    │    └── pro0.yoo.cjo
│    └── pro1
│         ├── libpro1.zoo.so
│         └── pro1.zoo.cjo
├── src
│    └── main.cj
└── cjpm.toml
```

Method 1: Import via `path-option`:

```text
[target.x86_64-unknown-linux-gnu.bin-dependencies]
  path-option = ["./test/pro0", "./test/pro1"]
```

The `path-option` is a string array structure, where each element represents the path name to be imported. `cjpm` will automatically import all Cangjie library packages under that path that comply with the naming rules, where the library name format should be `full-package-name`. For example, the library name corresponding to `pro0.xoo.cjo` in the above example should be `libpro0.xoo.so` or `libpro0.xoo.a`. Packages whose library names do not comply with this rule can only be imported via the `package-option`.

Method 2: Import via `package-option`:

```text
[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
  "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
  "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
  "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
```

The `package-option` is a `map` structure, where `pro0.xoo` serves as the `key` (strings containing `.` in `toml` configuration files must be enclosed in `""`), so the `key` value corresponds to `libpro0.xoo.so`. The path to the frontend file `cjo` serves as the `value`, and the corresponding `.a` or `.so` file for that `cjo` must be placed in the same path.

> **Note:**
>
> If the same package is imported via both `package-option` and `path-option`, the `package-option` field takes higher precedence.

The following code example in `main.cj` demonstrates calling the `pro0.xoo`, `pro0.yoo`, and `pro1.zoo` packages:

```cangjie
import pro0.xoo.*
import pro0.yoo.*
import pro1.zoo.*

main(): Int64 {
    var res = x + y + z // x, y, z are values defined in pro0.xoo, pro0.yoo, and pro1.zoo respectively
    println(res)
    return 0
}
```

> **Note:**
>
> The dependent Cangjie dynamic library files may be compilation outputs of the `root` package generated by other modules through the `profile.build.combined` configuration, containing symbols for all its sub-packages. During dependency checking, if a package's corresponding Cangjie library is not found, the `root` package corresponding to that package will be used as a dependency, and a warning will be printed. Developers must ensure that the `root` package imported in this way is generated via the corresponding method; otherwise, the library file may not contain symbols for sub-packages, leading to compilation errors.
> For example, if the source code imports the `demo.aoo` package via `import demo.aoo`, and the binary dependency does not contain the corresponding Cangjie library for that package, `cjpm` will attempt to find the dynamic library for the `root` package corresponding to that package, i.e., `libdemo.so`. If found, it will use that library as the dependency.

#### "target.target-name.compile-macros-for-target"

This field configures the cross-compilation method for macro packages, with the following three scenarios:

Method 1: By default, macro packages only compile outputs for the local platform during cross-compilation, not for the target platform. This applies to all macro packages within the module.

```text
[target.target-platform]
  compile-macros-for-target = ""
```

Method 2: During cross-compilation, outputs for both the local and target platforms are compiled. This applies to all macro packages within the module.

```text
[target.target-platform]
  compile-macros-for-target = "all" # The configuration item is a string, and the optional value must be "all"
```

Method 3: Specifies that certain macro packages within the module should compile outputs for both the local and target platforms during cross-compilation, while other unspecified macro packages follow the default mode of Method 1.

```text
[target.target-platform]
  compile-macros-for-target = ["pkg1", "pkg2"] # The configuration item is a string array, and the optional values are macro package names
```

#### Merging Rules for "target" Related Fields

Configuration items in `target` may coexist with other options in `cjpm.toml`. For example, the `compile-option` field can also exist in the `package` field, with the difference that the field in `package` applies to all `targets`. `cjpm` merges these duplicate fields in a specific way, combining all applicable configurations. Taking the `debug` compilation mode for `x86_64-unknown-linux-gnu` as an example, the `target` configuration is as follows:

```text
[package]
  compile-option = "compile-0"
  override-compile-option = "override-compile-0"
  link-option = "link-0"

[dependencies]
  dep0 = { path = "./dep0" }

[test-dependencies]
  devDep0 = { path = "./devDep0" }

[target.x86_64-unknown-linux-gnu]
  compile-option = "compile-1"
  override-compile-option = "override-compile-1"
  link-option = "link-1"
  [target.x86_64-unknown-linux-gnu.dependencies]
    dep1 = { path = "./dep1" }
  [target.x86_64-unknown-linux-gnu.test-dependencies]
    devDep1 = { path = "./devDep1" }
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["./test/pro1"]
  [target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
    "pro1.xoo" = "./test/pro1/pro1.xoo.cjo"

[target.x86_64-unknown-linux-gnu.debug]
  compile-option = "compile-2"
  override-compile-option = "override-compile-2"
  link-option = "link-2"
  [target.x86_64-unknown-linux-gnu.debug.dependencies]
    dep2 = { path = "./dep2" }
  [target.x86_64-unknown-linux-gnu.debug.test-dependencies]
    devDep2 = { path = "./devDep2" }
  [target.x86_64-unknown-linux-gnu.debug.bin-dependencies]
    path-option = ["./test/pro2"]
  [target.x86_64-unknown-linux-gnu.debug.bin-dependencies.package-option]
    "pro2.xoo" = "./test/pro2/pro2.xoo.cjo"
```

When `target` configuration items coexist with public configuration items in `cjpm.toml` or other levels of configuration items for the same `target`, they are merged according to the following priority:

1. Configuration for the corresponding `target` in `debug/release` mode
2. Configuration for the corresponding `target` unrelated to `debug/release`
3. Public configuration items

In the above `target` configuration example, the `target` configuration items are merged according to the following rules:

- `compile-option`: All applicable configurations with the same name are concatenated in order of priority, with higher-priority configurations appended later. In this example, the final `compile-option` value in `debug` mode for `x86_64-unknown-linux-gnu` is `compile-0 compile-1 compile-2`, while in `release` mode it is `compile-0 compile-1`, and for other `targets` it is `compile-0`.
- `override-compile-option`: Same as above. Since `override-compile-option` has higher priority than `compile-option`, in the final compilation command, the concatenated `override-compile-option` will be placed after the concatenated `compile-option`.
- `link-option`: Same as above.
- `dependencies`: Source dependencies are merged directly, and conflicts will result in errors. In this example, the final `dependencies` in `debug` mode for `x86_64-unknown-linux-gnu` are `dep0`, `dep1`, and `dep2`, while in `release` mode only `dep0` and `dep1` are active. For other `targets`, only `dep0` is active.
- `test-dependencies`: Same as above.
- `bin-dependencies`: Binary dependencies are merged by priority, with conflicts resolved by keeping only the higher-priority dependency. `package-option` configurations are added first for configurations with the same priority. In this example, in `debug` mode for `x86_64-unknown-linux-gnu`, binary dependencies from `./test/pro1` and `./test/pro2` are added, while in `release` mode only `./test/pro1` is added. Since `bin-dependencies` has no public configuration, no binary dependencies are active for other `targets`.

In cross-compilation scenarios for this example, if `x86_64-unknown-linux-gnu` is specified as the target `target` on other platforms, the configuration for `target.x86_64-unknown-linux-gnu` will also be merged with public configuration items according to the above rules. If in `debug` mode, the configuration items for `target.x86_64-unknown-linux-gnu.debug` will also be applied.

### Environment Variable Configuration

Environment variables can be used in `cjpm.toml` to configure field values. `cjpm` will retrieve the corresponding environment variable values from the current runtime environment and substitute them into the actual configuration values. For example, the following `dependencies` field uses an environment variable for path configuration:

```text
[dependencies]
aoo = { path = "${DEPENDENCY_PATH}/aoo" }
```

When importing module `aoo`, `cjpm` will retrieve the `DEPENDENCY_PATH` variable value and substitute it to obtain the final path for module `aoo`.

The list of fields that support environment variable configuration includes:

- The following fields in the single-module configuration field `package`:
    - Single-package compilation option `compile-option` in `package-configuration`
- The following fields in the workspace management field `workspace`:
    - Member module list `members`
    - Compilation module list `build-members`
    - Test module list `test-members`
- The following fields common to both `package` and `workspace`:
    - Compilation option `compile-option`
    - Global compilation option `override-compile-option`
    - Linking option `link-option`
    - Output directory path `target-dir`
- The `path` field for local dependencies in the build dependency list `dependencies`
- The `path` field for local dependencies in the test dependency list `test-dependencies`
- The `path` field for local dependencies in the build script dependency list `script-dependencies`
- Custom passthrough options `customized-option` in the command profile configuration `profile`
- The `path` field in external C library configuration `ffi.c`
- The following fields in the platform isolation option `target`:
    - Compilation option `compile-option`
    - Global compilation option `override-compile-option`
    - Linking option `link-option`
    - The `path` field for local dependencies in the build dependency list `dependencies`
    - The `path` field for local dependencies in the test dependency list `test-dependencies`
    - The `path` field for local dependencies in the build script dependency list `script-dependencies`
    - The `path-option` and `package-option` fields in the binary dependency field `bin-dependencies`

## Project Management Configuration File Specification

The project management configuration file, `cangjie-repo.toml`, is utilized to configure settings including the central repository URL and local repository cache. The cjpm tool primarily leverages this file to interface with the central repository and manage dependency modules downloaded from the central repository.

The `cangjie-repo.toml` file can be configured in three locations. When executing the `cjpm` command, it reads the configuration files in the following priority order from highest to lowest:

- A `cangjie-repo.toml` file located alongside `cjpm.toml`: In the current `cjpm` module directory where the command is executed.
- A `cangjie-repo.toml` file under the `.cjpm` directory of user's home directory.
    - For `Linux/macOS`: `$HOME/.cjpm`
    - For `Windows`: `%USERPROFILE%/.cjpm`
- A `cangjie-repo.toml` file in the Cangjie SDK directory at the path `tools/config/cangjie-repo.toml`.

Upon successfully locating a valid `cangjie-repo.toml` file, `cjpm` will utilize this file as the configuration source for the current command execution and will disregard all configuration files of lower precedence.

The configuration file format is as follows:

```toml
[repository.cache]
  path = "/path/to/repository/cache"

[repository.home]
  registry = "central/repo/url"
  token = "user-token"
```

The configuration content is described as follows:

- `repository.home` is used to configure the central repository URL and the user's personal token. The `cjpm` tool interacts with the central repository address specified in the `registry` field, and all interaction requests will include the user's token information for authentication.
- `repository.cache` is used to configure the local path for storing source code modules downloaded from the central repository or Git. Environment variables can be used to configure field values, Refer to[Environment Variable Configuration](#environment-variable-configuration), If not configured, it defaults to the `.cjpm` directory in the user's home directory. Once the local path is determined, Git source code modules are downloaded to the `git` subdirectory under this path. Central repository source code modules are downloaded to the `repository/source` subdirectory under this path.

## Configuration and Cache Directories

The storage path for files downloaded by `cjpm` via `git` can be specified using the `CJPM_CONFIG` environment variable. If not specified, the default location on `Linux/macOS` is `$HOME/.cjpm`, and on `Windows` it is `%USERPROFILE%/.cjpm`.

> **Note:**
>
> - This configuration functions identically to `repository.cache` in `cangjie-repo.toml`. It only takes effect if no valid `cangjie-repo.toml` configuration exists, or if the valid configuration is the one located at `tools/config/cangjie-repo.toml` within the Cangjie SDK.
> - This configuration is deprecated and will be removed in a future release. Please use `cangjie-repo.toml` instead.

## Cangjie Package Management Specification

In the Cangjie package management specification, for a file directory to be recognized as a valid source package, the following requirements must be met:

1. It must directly contain at least one Cangjie code file;
2. Its parent package (including the parent's parent package, up to the `root` package) must also be a valid source package. Note that the module `root` package has no parent package, so it only needs to satisfy condition 1.

For example, consider the following `cjpm` project named `demo`:

```text
demo
├──src
│   ├── main.cj
│   └── pkg0
│        ├── aoo
│        │    └── aoo.cj
│        └── boo
│             └── boo.cj
└── cjpm.toml
```

Here, the directory corresponding to `demo.pkg0` does not directly contain any Cangjie code, so `demo.pkg0` is not a valid source package. Although `demo.pkg0.aoo` and `demo.pkg0.boo` directly contain Cangjie code files `aoo.cj` and `boo.cj`, their upstream package `demo.pkg0` is not a valid source package, so these two packages are also not valid source packages.

When `cjpm` identifies a package like `demo.pkg0` that does not directly contain Cangjie files, it treats it as a non-source package, ignores all its subpackages, and prints the following warning:

```text
Warning: there is no '.cj' file in directory 'demo/src/pkg0', and its subdirectories will not be scanned as source code
```

Therefore, if developers need to configure a valid source package, the package must directly contain at least one Cangjie code file, and all its upstream packages must be valid source packages. Taking the above `demo` project as an example, to make `demo.pkg0`, `demo.pkg0.aoo`, and `demo.pkg0.boo` all recognized as valid source packages, a Cangjie code file can be added inside `demo/src/pkg0`, as shown below:

```text
demo
├── src
│    ├── main.cj
│    └── pkg0
│         ├── pkg0.cj
│         ├── aoo
│         │    └── aoo.cj
│         └── boo
│              └── boo.cj
└── cjpm.toml
```

`demo/src/pkg0/pkg0.cj` must be a Cangjie code file that complies with the package management specification and may not contain functional code, such as the following form:

```cangjie
package demo.pkg0
```

## Command Extension

`cjpm` provides a command extension mechanism, allowing developers to extend `cjpm` commands via executable files named in the format `cjpm-xxx(.exe)`.

For an executable file `cjpm-xxx` (`cjpm-xxx.exe` on Windows), if the file's directory is configured in the system environment variable `PATH`, the following command can be used to execute it:

```shell
cjpm xxx [args]
```

Here, `args` represents the list of arguments that may be required by `cjpm-xxx(.exe)`. The above command is equivalent to:

```shell
cjpm-xxx(.exe) [args]
```

Running `cjpm-xxx(.exe)` may depend on certain dynamic libraries. In such cases, developers need to manually add the directory containing the required dynamic libraries to the environment variables.

Below is an example using `cjpm-demo`, an executable file compiled from the following Cangjie code:

```cangjie
import std.process.*
import std.collection.*

main(): Int64 {
    var args = ArrayList<String>(Process.current.arguments)

    if (args.size < 1) {
        eprintln("Error: failed to get parameters")
        return 1
    }

    println("Output: ${args[0]}")

    return 0
}
```

After adding its directory to `PATH`, running the corresponding command will execute the file and produce the expected output.

```text
Input: cjpm demo hello,world
Output: Output: hello,world
```

Built-in `cjpm` commands have higher priority, so these commands cannot be extended this way. For example, even if an executable file named `cjpm-build` exists in the system environment variables, `cjpm build` will not execute this file but will instead run `cjpm` with `build` as an argument.

## Build Scripts

`cjpm` provides a build script mechanism, allowing developers to define behaviors for `cjpm` before or after executing certain commands.

The build script source file is fixed as `build.cj` and is located in the Cangjie project's root directory, at the same level as `cjpm.toml`. When creating a new Cangjie project using the `init` command, `cjpm` does not create `build.cj` by default. Developers who need it can manually create and edit `build.cj` in the specified location using the following template format:

```cangjie
// build.cj

import std.process.*

// Case of pre/post codes for 'cjpm build'.
/* called before `cjpm build`
 * Success: return 0
 * Error: return any number except 0
 */
// func stagePreBuild(): Int64 {
//     // process before "cjpm build"
//     0
// }

/*
 * called after `cjpm build`
 */
// func stagePostBuild(): Int64 {
//     // process after "cjpm build"
//     0
// }

// Case of pre codes for 'cjpm clean'.
/* called before `cjpm clean`
 * Success: return 0
 * Error: return any number except 0
 */
// func stagePreClean(): Int64 {
//     // process before "cjpm clean"
//     0
// }

// For other options, define stagePreXXX and stagePostXXX in the same way.

/*
 * Error code:
 * 0: success.
 * other: cjpm will finish running command. Check target-dir/build-script-cache/module-name/script-log for error outputs defind by user in functions.
 */

main(): Int64 {
    match (Process.current.arguments[0]) {
        // Add operation here with format: "pre-"/"post-" + optionName
        // case "pre-build" => stagePreBuild()
        // case "post-build" => stagePostBuild()
        // case "pre-clean" => stagePreClean()
        case _ => 0
    }
}
```

`cjpm` supports using build scripts to define pre- and post-command behaviors for a series of commands. For example, for the `build` command, you can define `pre-build` in the `match` block within the `main` function to execute the desired pre-build functionality function `stagePreBuild` (the function name is not restricted). Post-build behavior can be similarly defined by adding a `post-build` case. Other commands can be extended in the same way by adding corresponding `pre/post` options and functionality functions.

After defining pre- and post-command behaviors, `cjpm` will first compile `build.cj` when executing the command and then execute the corresponding behaviors before and after the command. For example, with `pre-build` and `post-build` defined, running `cjpm build` will follow these steps:

1. Before the build process, compile `build.cj`;
2. Execute the functionality function corresponding to `pre-build`;
3. Proceed with the `cjpm build` compilation process;
4. After successful compilation, `cjpm` will execute the functionality function corresponding to `post-build`.

The commands supported by build scripts are as follows:

- `build`, `test`, `bench`: Support executing both `pre` and `post` processes defined in dependent modules' build scripts.
- `run`, `install`: Only support running the `pre` and `post` build script processes of the corresponding module or executing the `pre-build` and `post-build` processes of dependent modules during compilation.
- `check`, `tree`, `update`: Only support running the `pre` and `post` build script processes of the corresponding module.
- `clean`: Only support running the `pre` build script process of the corresponding module.

When executing these commands, if the `--skip-script` option is configured, all build script compilation and execution will be skipped, including those of dependent modules.

Usage notes for build scripts:

- The return value of functionality functions must meet certain requirements: a successful execution should return `0`, while a failure should return any `Int64` value except `0`.
- All outputs from `build.cj` will be redirected to the project directory at `build-script-cache/[target|release]/[module-name]/bin/script-log`. Developers can check this file for output content added in functionality functions.
- If `build.cj` does not exist in the project root directory, `cjpm` will proceed with normal execution. If `build.cj` exists and defines pre- or post-command behaviors, the command will abort abnormally if `build.cj` fails to compile or the functionality function returns a non-zero value, even if the command itself could execute successfully.
- In multi-module scenarios, the build scripts (`build.cj`) of dependent modules take effect during compilation and unit testing. Outputs from dependent module build scripts are also redirected to log files in the corresponding module directory under `build-script-cache/[target|release]`.

For example, the following build script `build.cj` defines pre- and post-build behaviors:

```cangjie
import std.process.*

func stagePreBuild(): Int64 {
    println("PRE-BUILD")
    0
}

func stagePostBuild(): Int64 {
    println("POST-BUILD")
    0
}

main(): Int64 {
    match (Process.current.arguments[0]) {
        case "pre-build" => stagePreBuild()
        case "post-build" => stagePostBuild()
        case _ => 0
    }
}
```

When executing `cjpm build`, `cjpm` will execute `stagePreBuild` and `stagePostBuild`. After `cjpm build` completes, the `script-log` file will contain the following output:

```text
PRE-BUILD
POST-BUILD
```

Build scripts can import dependent modules via the `script-dependencies` field in `cjpm.toml`, with the same format as `dependencies`. For example, the following configuration in `cjpm.toml` imports the `aoo` module, which contains a method named `aaa()`:

```text
[script-dependencies]
aoo = { path = "./aoo" }
```

The build script can then import this dependency and use the interface `aaa()`:

```cangjie
import std.process.*
import aoo.*

func stagePreBuild(): Int64 {
    aaa()
    0
}

func stagePostBuild(): Int64 {
    println("POST-BUILD")
    0
}

main(): Int64 {
    match (Process.current.arguments[0]) {
        case "pre-build" => stagePreBuild()
        case "post-build" => stagePostBuild()
        case _ => 0
    }
}
```

Build script dependencies (`script-dependencies`) are independent of source code-related dependencies (`dependencies` and `test-dependencies`). Source and test code cannot use modules from `script-dependencies`, and build scripts cannot use modules from `dependencies` or `test-dependencies`. If the same module is needed in both build scripts and source/test code, it must be configured in both `script-dependencies` and `dependencies/test-dependencies`.

## Usage Examples

The following example demonstrates how to use `cjpm` with a Cangjie project directory structure. The corresponding source code examples can be found in [Source Code](#example-source-code). The module name for this Cangjie project is `test`.

```text
cj_project
├── pro0
│    ├── cjpm.toml
│    └── src
│         ├── zoo
│         │    ├── zoo.cj
│         │    └── zoo_test.cj
│         └── pro0.cj
├── src
│    ├── koo
│    │    ├── koo.cj
│    │    └── koo_test.cj
│    ├── main.cj
│    └── main_test.cj
└── cjpm.toml
```

### Using `init` and `build`

- Create a new Cangjie project and write source code `xxx.cj` files, such as the `koo` package and `main.cj` file shown in the example structure.

    ```shell
    cjpm init --name test --path ./cj_project
    cd cj_project
    mkdir src/koo
    ```

    At this point, a `cj_project` directory will be created in the current command execution directory, and the `src` folder along with the default `cjpm.toml` configuration file will be automatically generated within it. Developers can manually create sub-packages (e.g., `src/koo`) in the source code directory `src`, or add new source files and test files in each package as needed.

- When the current module depends on an external `pro0` module, create the `pro0` module and its configuration file. Then write the module's source code files, manually creating the `src` directory under `pro0`, and place the Cangjie packages under `src`, such as the `zoo` package in the example structure.

    ```shell
    mkdir pro0 && cd pro0
    cjpm init --name pro0 --type=static
    mkdir src/zoo
    ```

- When the main module depends on `pro0`, configure the `dependencies` field in the main module's configuration file as described in the manual. After correct configuration, execute `cjpm build`. The generated executable will be in the `target/release/bin/` directory.

    ```shell
    cd cj_project
    vim cjpm.toml
    cjpm build
    cjpm run
    ```

### Using `test` and `clean`

- After writing the corresponding `xxx_test.cj` unit test files for each file as shown in the example structure, execute the following code to run unit tests. The generated files will be in the `target/release/unittest_bin` directory.

    ```shell
    cjpm test
    ```

    Or:

    ```shell
    cjpm test src src/koo pro0/src/zoo
    ```

- To manually delete intermediate files such as the `target` and `cov_output` directories, `*.gcno`, and `*.gcda`, execute:

    ```shell
    cjpm clean
    ```

### Example Source Code

```cangjie
// cj_project/src/main.cj
package test

import pro0.zoo.*
import test.koo.*

main(): Int64 {
    let res = z + k
    println(res)
    let res2 = concatM("a", "b")
    println(res2)
    return 0
}

func concatM(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/src/main_test.cj
package test

import std.unittest.* // testfame
import std.unittest.testmacro.* // macro_Defintion

@Test
public class TestM{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatM("1", "2"), "12")
        @Assert(concatM("1", "3"), "13")
    }
}
```

```cangjie
// cj_project/src/koo/koo.cj
package test.koo

public let k: Int32 = 12

func concatk(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/src/koo/koo_test.cj
package test.koo

import std.unittest.* // testfame
import std.unittest.testmacro.* // macro_Defintion

@Test
public class TestK{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatk("1", "2"), "12")
        @Assert(concatk("1", "3"), "13")
    }
}
```

```cangjie
// cj_project/pro0/src/pro0.cj
package pro0
```

```cangjie
// cj_project/pro0/src/zoo/zoo.cj
package pro0.zoo

public let z: Int32 = 26

func concatZ(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/pro0/src/zoo/zoo_test.cj
package pro0.zoo

import std.unittest.* // test framework
import std.unittest.testmacro.* // macro definition

@Test
public class TestZ{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatZ("1", "2"), "12")
        @Assert(concatZ("1", "3"), "13")
    }
}
```

```toml
# cj_project/cjpm.toml
[package]
cjc-version = "1.0.0"
description = "nothing here"
version = "1.0.0"
name = "test"
output-type = "executable"

[dependencies]
pro0 = { path = "pro0" }
```

```toml
# cj_project/pro0/cjpm.toml
[package]
cjc-version = "1.0.0"
description = "nothing here"
version = "1.0.0"
name = "pro0"
output-type = "static"
```

## Appendix

### Cross-Compilation Instructions

`cjpm` supports cross-compilation and execution between certain platforms. For example, assuming the target platform is `arch-sys-abi`, the compilation steps are as follows:

1. Configure the toolchain required for the target platform.

2. In the `cjpm.toml` of the entry module, add the compilation option configuration needed for the target platform:

    ```text
    [target.arch-sys-abi]
    override-compile-option = "value"
    ```

    This configuration will apply to all dependent modules. In single-module compilation mode, it can be replaced with `compile-option`.

3. If the project has binary dependencies, configure them as follows:

    ```text
    [target.arch-sys-abi.bin-dependencies]
    path-option = [...]
    [target.arch-sys-abi.bin-dependencies.package-option]
    "..." = "..."
    ```

4. Use the following commands to compile and build or test the code:

    ```shell
    cjpm build --target=arch-sys-abi# Cross-compile artifacts for the target platform
    cjpm test --target=arch-sys-abi # Cross-compile executable test files for the target platform
    ```

5. Import the binary artifacts into the target platform for normal execution.

> **Note:**
>
> - The compiled artifacts are located in the `target-dir` directory configured by the user, under a subdirectory named after the target platform (`target`).
> - If dynamic library dependencies exist, configure them in the runtime environment variable `LD_LIBRARY_PATH`.

### Multi-Platform Build Instructions

To support multi-platform project builds, `cjpm` introduces new entities such as `features` and `source-sets` to enhance development efficiency for multi-platform projects. This is an experimental feature and requires specifying `experimental = true` in the `[profile]` field.

#### Feature

A `Feature` is a named flag used to specify the source code to be compiled. Below is a list of all available features in `cjpm`:

```bash
feature.os.posix
feature.os.epoll
feature.os.kqueue
feature.os.windows
feature.os.linux
# OS is harmony
feature.os.hm
feature.os.darwin
# The CPU architecture is `big-endian`
feature.arch.big
# The CPU architecture is `little-endian`
feature.arch.little
feature.arch.x64
feature.arch.aarch64
# The CPU uses `sse` instruction set
feature.arch.sse1
feature.arch.sse2
feature.arch.sse3
feature.arch.sse4.1
feature.arch.sse4.2
# The CPU uses `avx` instruction set
feature.arch.avx1
feature.arch.avx2
feature.arch.avx512
feature.arch.neon
feature.env.ohos
feature.env.gnu
feature.env.mingw32
feature.env.hos
feature.env.android
feature.cj.cjnative
feature.cj.v0_54_3 # Anything after `v` is interpreted as `cjc` version
```

These values are not validated in any way. It is the developer's responsibility to ensure that the code compiled with these `features` executes correctly.
Developers can define custom `feature` values and meanings.
Developers can use the `--enable-features` option in `cjpm`'s `build`, `run`, and `test` commands, providing a comma-separated list of `feature` values.
For example:

```bash
cjpm build --enable-features=feature.os.linux,feature.env.gnu
```

#### Feature Deduction

The following `feature` values can be inferred from the `cjc` or other compilation options (e.g., `--target`) used in `cjpm`, so they typically do not need to be explicitly specified:

```bash
feature.os.posix
feature.os.windows
feature.os.linux
feature.os.hm
feature.os.darwin
feature.arch.x64
feature.arch.aarch64
feature.env.ohos
feature.env.gnu
feature.env.mingw32
feature.env.hos
feature.env.android
feature.cj.cjvm
feature.cj.cjnative
feature.cj.v0_54_3
```

If developing a multi-platform project on a `GNU/Linux` machine, the source code can be compiled and run using the following commands:

```bash
# Short command
cjpm run
# Full command
cjpm run --enable-features=feature.os.linux,feature.env.gnu
```

For cross-compilation scenarios, specify `--target`.

For example:

```bash
# Short command
cjpm build --target=aarch64-linux-android
# Full command
cjpm build --target=aarch64-linux-android --enable-features=feature.arch.aarch64,feature.os.linux,feature.env.android
```

If `cjpm` deduces multiple source directories (resulting in a compilation error), use the `--no-feature-deduce` option to disable deduction and explicitly specify `features` with `--enable-features`:

```bash
# Will display the error message "No source set was selected"
cjpm build --target=aarch64-linux-android --no-feature-deduce
# Specify appropriate feature values:
# 1. [..., "feature.os.linux", "feature.env.android"]
# 2. [..., "feature.os.linux"]
# 3. [..., "feature.env.android"]

cjpm build --no-feature-deduce --target=aarch64-linux-android --enable-features=feature.os.linux,feature.env.android
```

#### Source Sets and Their Configuration

The default `cjpm.toml` is as follows:

```toml
[package]
    cjc-version = "0.57.1"
    compile-option = ""
    description = "nothing here"
    link-option = ""
    name = "cmp_lib"
    output-type = "dynamic"
    override-compile-option = ""
    target-dir = ""
    version = "1.0.0"
    package-configuration = {}

# New field indicating a multi-platform project
# [source-set]
```

For the `source-set` field configuration, an example is provided below:

```toml
# Example syntax:

# Source file directory for Cangjie code
[source-set.epoll]
    src-dir = "src/net/select/epoll"
    condition = [ "feature.os.epoll" ]

[source-set.kqueue]
    src-dir = "src/net/select/kqueue"
    condition = [ "feature.os.kqueue" ]
```

Each source set declaration consists of three parts: the `source-set` identifier, `src-dir`, and `condition`.

##### Source-Set Identifier

The `source-set` identifier is the unique "path" of the source set. This "path" is separated by `.`, and each path should start with `source-set` as it is the root of all declarations.

##### src-dir

Specifies the location to search for the package's source code when this source set is enabled.

```toml
# Possible syntax

# 1. Single directory
[source-set.${source set fully qualified name}]
    src-dir = "./src/linux/common"

# 2. Multiple directories
# All specified directories will be compiled as a single compilation unit, similar to compiling a single directory.

    [source-set.${source set fully qualified name}]
        src-dir = ["./src/linux/dirA", "./src/linux/dirB"]
```

##### condition

The `condition` specifies one or more `features` that must be enabled to compile the corresponding code.

```toml
# If the source set declaration does not include a `condition` field, no constraints are set.
# Possible syntax:
# 1. Multiple features must be satisfied simultaneously.

 [source-set.${source set fully qualified name}]
    condition = ["feature.arch.aarch64", "feature.env.ohos", "feature.os.linux"]

# 2. Any one of multiple features must be satisfied.

[source-set.${source set fully qualified name}]
    condition.1 = ["feature.arch.little"]
    condiiton.alpha = ["feature.env.ohos"]
    condiiton.beta= ["feature.os.linux", "feature.os.posix"]# Both features must be satisfied.
```

#### Special Source Sets and Their Configuration

##### Common Source Set

Only one source set can be selected at the same level to ensure code isolation across platforms. However, some code should always be included. This is called the `common` source set, whose code is always included in the compilation process, and the `condition` configuration is not applicable. Example:

```toml
[source-set.common]
    src-dir = "./common"

[source-set.socketSelection.common]
    src-dir = "./socket/common"

[source-set.socketSelection.kqueue]
    src-dir = "./socket/kqueue"
    condition = [ "feature.os.kqueue" ]
```

##### Nested Source Sets

When source sets have nested levels, the directory hierarchy of the code must correspond to the source set hierarchy (i.e., the parent source set path must be a prefix of the child source set path). Additionally, nested source sets do not support multiple paths.

```toml
[source-set.common]
    src-dir = "./common"

[source-set.socketSelection]
    src-dir = "./socketSelection/weird"

[source-set.socketSelection.a]
    src-dir = "./socketSelection/weird/a"

[source-set.socketSelection.b]
    src-dir = "./socketSelection/weird/b"
```

##### Other Source Set

If the configuration file contains only single-level source sets and `cjpm` cannot match any source set, a compilation error will occur. However, for nested source sets, `cjpm` implicitly generates a special source set named `other`, whose path is derived from the parent path. To customize the path, explicitly configure this source set, but its `condition` cannot be configured. Example:

```toml
[source-set.common]
    src-dir = "./common"

[source-set.socketSelection]
    src-dir = "./socketSelection"

[source-set.socketSelection.weird]
    src-dir = "./socketSelection/weird"
    condition = [ "feature.os.linux", "feature.os.windows" ] # Practically impossible condition to meet

# This source set will be selected as fallback
[source-set.socketSelection.other]
    src-dir = "./socketSelection/other"
```

If no top-level source set is selected, the following error message will appear:

```text
"No source set specified in ${path/to/cjpm.toml} was selected"
```

##### Default Source Set

The default source set represents the types of source sets supported by default in `cjpm`. If no modifications are needed, they do not need to be specified in `cjpm.toml`. To modify them, specify and configure the corresponding source set in the configuration file, which will override the default configuration.

For example, setting an empty `source-set` configuration indicates that the project is a multi-platform project.

```toml
[source-set]
```

In this case, `cjpm` will **implicitly** generate the default configuration as follows:

```toml
[source-set.common]
    src-dir = "./common"

[source-set.windows]
    src-dir = "./windows"
    condition = ["feature.os.windows"]

[source-set.linux]
    src-dir = "./linux"
    condition = ["feature.os.linux", "feature.env.gnu"]

[source-set.darwin]
    src-dir = "./darwin"
    condition = ["feature.os.darwin"]

[source-set.android]
    src-dir = "./android"
    condition = ["feature.os.linux", "feature.env.android"]

[source-set.hos]
    src-dir = "./hos"
    condition = ["feature.os.linux", "feature.env.hos"]

[source-set.ohos]
    src-dir = "./ohos"
    condition = ["feature.os.linux", "feature.env.ohos"]
```
