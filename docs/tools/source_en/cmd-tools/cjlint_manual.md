# Static Analysis Tool

## Overview

`CJLint (Cangjie Lint)` is a static analysis tool developed based on the Cangjie Language Programming Specification. It identifies code segments that violate programming standards, helps developers detect vulnerabilities, and ensures the production of Cangjie code that meets Clean Source requirements.

## Usage Instructions

`cjlint -h` displays help information and option descriptions.

```text
Options:
   -h                      Show usage
                               eg: ./cjlint -h
   -v                      Show version
                               eg: ./cjlint -v
   -f <value>              Detected file directory (absolute or relative paths). If a directory is specified, the default output filename is cjReport
                               eg: ./cjlint -f fileDir -c . -m .
                               eg: ./cjlint -f "fileDir1 fileDir2" -c . -m .
   -e <v1:v2:...>          Excluded files, directories, or configurations (separated by ':'). Supports regular expressions
                               eg: ./cjlint -f fileDir -e fileDir/a/:fileDir/b/*.cj
   -o <value>              Output file path (absolute or relative)
                               eg: ./cjlint -f fileDir -o ./out
   -r [csv|json]           Report file format (csv or json, default: json)
                               eg: ./cjlint -f fileDir -r csv -o ./out
   -c <value>              Config directory path (absolute or relative to the executable)
                               eg: ./cjlint -f fileDir -c .
   -m <value>              Modules directory path (absolute or relative to the executable)
                               eg: ./cjlint -f fileDir -m .
   --import-path <value>   Add .cjo search path
```

`cjlint -f` specifies the target directory for analysis.

```bash
cjlint -f fileDir [option] fileDir...

# For multiple paths, separate them with spaces within ""
cjlint -f "fileDir1 fileDir2" [option] fileDir...
```

> **Note:**
>
> The path after `-f` should point to the `src` directory containing *.cj files.

Correct example:

```bash
cjlint -f xxx/xxx/src
```

Incorrect example:

```bash
cjlint -f xxx/xxx/src/xxx.cj
```

> **Explanation:**
>
> This limitation stems from compiler module constraints. As the compiler's compilation options are currently being refactored with unstable APIs, the tool only supports module compilation for now. Eventually, the tool will align with the compiler's stable compilation options.

`-r` specifies the scan report format (currently supports `json` and `csv`).

`-r` must be used with `-o`. If `-o` is not specified to output to a file, no report will be generated even if `-r` is set. If `-o` is specified without `-r`, the default format is `json`.

```bash
cjlint -f ./src -r csv -o ./report         # Generates report.csv
cjlint -f ./src -r csv -o ./output/report  # Generates report.csv in the output directory
```

`-c` and `-m` allow developers to specify custom `config` and `modules` directory paths when needed.

By default, `cjlint` uses the `config` and `modules` directories in its installation path. Developers can override these using `-c` and `-m`.

Example: If custom config and modules paths are `./tools/cjlint/config` and `./tools/cjlint/modules` respectively (both under `./tools/cjlint`), the command would be:

```bash
cjlint -f ./src -c ./tools/cjlint -m ./tools/cjlint
```

`--import-path` specifies `.cjo` search paths (supports multiple paths).

```bash
cjlint --import-path fileDir

# For multiple paths, separate them with spaces within ""
cjlint --import-path "fileDir1 fileDir2"
```

## Rule-Level Warning Suppression

The `config` directory (located alongside the `cjlint` executable) contains two configuration files: `cjlint_rule_list.json` and `exclude_lists.json`. `cjlint_rule_list.json`: Rule list configuration. Developers can enable/disable specific rules by modifying this file. `exclude_lists.json`: Warning suppression configuration. Developers can suppress specific rule violations by adding entries here.

Example: To enable only 5 specific rules:

```json
{
    "RuleList": [
        "G.FMT.01",
        "G.ENU.01",
        "G.EXP.03",
        "G.OTH.01",
        "G.OTH.02"
    ]
}
```

Example: To suppress specific violations of rule "G.OTH.01":

> **Note:**
>
> `path` supports fuzzy matching (format: `xxx.cj`). `line` requires exact matching. `colum` is optional for column-level precision.

```json
{
    "G.OTH.01" : [
        {"path":"xxx/example.cj", "line":"42"},
        {"path":"xxx/example.cj", "line":"42", "colum": "2"},
        {"path":"example.cj", "line":"42", "colum": "2"}
    ]
}
```

## Source Code Comment-Based Suppression

**Special Comment BNF**

```text
<content of cjlint-ignore comment> ::=  "cjlint-ignore"  [-start] <ignore-rule>{...} [description] | cjlint-ignore  <-end> [description]
<ignore-rule> ::="!"<rule-name>
<rule-name> ::= <letters>
```

> **Note:**
>
> - The `cjlint-ignore` marker, `-start`/`-end` options, and rule specifications must appear on the same line. Descriptions can span multiple lines.
> - For single-line suppression, separate multiple rules with spaces. The suppression applies to the current line.
> - For multi-line suppression, `-start` marks the beginning and `-end` marks the end. The suppression applies to all lines between them. Each `-end` pairs with the nearest preceding `-start`.

**Correct Single-Line Example 1**: Suppress G.FUN.02

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /* cjlint-ignore !G.FUN.02 */
    return a + b + c
}
```

**Correct Single-Line Example 2**: Suppress G.FUN.02

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { // cjlint-ignore !G.FUN.02 description
    return a + b + c
}
```

**Correct Multi-Line Example 1**: Suppress G.FUN.02

```cangjie
/*cjlint-ignore -start !G.FUN.02 description */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
/* cjlint-ignore -end description */
```

**Correct Multi-Line Example 2**: Suppress G.FUN.02

```cangjie
// cjlint-ignore -start !G.FUN.02 description
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
// cjlint-ignore -end description
```

**Correct Multi-Line Example 3**: Suppress G.FUN.02

```cangjie
/**
 *  cjlint-ignore -start !G.FUN.02 description
 */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
// cjlint-ignore -end description
```

**Incorrect Single-Line Example 1**: Failed G.FUN.02 suppression

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /*cjlint-ignore !G.FUN.02!G.FUN.01*/
    return a + b + c                               // ERROR: Missing space between rules
}
```

**Incorrect Single-Line Example 2**: Failed G.FUN.02 suppression

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /*cjlint-ignore !G.FUN.02description*/
    return a + b + c                               // ERROR: Missing space before description
}
```

**Incorrect Multi-Line Example 1**: Failed G.FUN.02 suppression

```cangjie
/* cjlint-ignore -start
 * !G.FUN.02 description */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
/* cjlint-ignore -end description */
// ERROR: Rule not on same line as 'cjlint-ignore'
```

## File-Level Warning Suppression

1. `cjlint` supports file-level suppression via the `-e` option.

    Specify exclusion patterns (relative to `-f` source directory, supports regex) within quotes, separated by spaces. Example: This command excludes all `.cj` files under `src/dir1/`, `src/dir2/a.cj`, and files matching `test*.cj` in `src/`.

    ```bash
    cjlint -f src/ -e "dir1/ dir2/a.cj test*.cj"
    ```

2. `cjlint` supports batch exclusions via `.cfg` configuration files.

    Use `-e` to specify `.cfg` files (separated by spaces). Example: This command excludes files matching patterns in `src/exclude_config_1.cfg` and `src/dir2/exclude_config_2.cfg`, plus `src/dir1/`.

    ```bash
    cjlint -f src/ -e "dir1/ exclude_config_1.cfg dir2/exclude_config_2.cfg"
    ```

    `.cfg` files contain one pattern per line (relative to the config file's directory, supports regex). Example: If `src/dir2/exclude_config_2.cfg` contains these lines, the above command would exclude `src/dir2/subdir1/` and `src/dir2/subdir2/a.cj`.

    ```text
    subdir1/
    subdir2/a.cj
    ```

3. `cjlint` supports default configuration file for exclusions.

    The default exclusion config file is `cjlint_file_exclude.cfg` in the `-f` source directory. Example: When `src/cjlint_file_exclude.cfg` exists, `cjlint -f src/` will apply its exclusion patterns. If other valid `.cfg` files are specified via `-e`, the default file is ignored.

## Supported Rules (Continuously Updated)

Default enabled rules:

- G.NAM.01 Package names should be lowercase with optional underscores/numbers.
- G.NAM.02 Source filenames should use lowercase_with_underscores style.
- G.NAM.03 Interfaces, classes, structs, enums, and type aliases use PascalCase.
- G.NAM.04 Functions use camelCase.
- G.NAM.05 Global `let` and `static let` variables use UPPER_CASE.
- G.FMT.01 Source files must use UTF-8 encoding (including comments).
- G.FMT.15 Never omit leading 0 in floating-point numbers.
- G.DCL.01 Avoid variable shadowing.
- G.DCL.02 Explicitly declare types for public variables and function returns.
- G.FUN.01 Functions should have single responsibility.
- G.FUN.02 Functions must not have unused parameters.
- G.FUN.03 Avoid overloading unrelated functions with the same name.
- G.CLS.01 Don't increase visibility when overriding methods.
- G.ITF.02 Prefer implementing interfaces at type definition rather than via extension.
- G.ITF.01 Use `mut` for self-modifying interface functions to support structs.
- G.ITF.03 Avoid implementing both parent and child interfaces simultaneously.
- G.ITF.04 Prefer generic constraints over direct interface types.
- G.OPR.01 Avoid unconventional operator overloading.
- G.OPR.02 Avoid overloading `()` in enums.
- G.ENU.01 Avoid enum constructor/top-level name collisions.
- G.ENU.02 Minimize unnecessary constructor overloading across enums.
- G.VAR.01 Prefer immutable variables.
- G.VAR.02 Minimize variable scope.
- G.TYP.03 Use `isNaN()` for NaN checks.
- G.EXP.01 Avoid mixing pattern types in single `match` level.
- G.EXP.02 Don't expect precise results from floating-point operations.
- G.EXP.03 Avoid side effects in right-hand operands of `&&`, `||`, `?`, `??`.
- G.EXP.04 Avoid relying on operator evaluation order for side effects.
- G.EXP.05 Use parentheses to clarify operation order.
- G.EXP.06 Avoid redundant `==` or `!=` with Booleans.
- G.EXP.07 Place changing expressions on the left in comparisons.
- G.ERR.01 Use proper error handling mechanisms.
- G.ERR.02 Prevent sensitive data leaks via exceptions.
- G.ERR.03 Avoid `getorthrow` with Option types.
- G.ERR.04 Don't use `return`, `break`, `continue`, or exceptions to exit `finally`.
- G.PKG.01 Avoid wildcard `import *`.
- G.CON.01 Don't expose internal lock objects to untrusted code.
- P.01 Acquire locks in consistent order to prevent deadlocks.
- G.CON.02 Ensure lock release during exceptions.
- G.CON.03 Don't override thread-safe functions with unsafe versions.
- P.02 Avoid data races.
- G.CHK.01 Validate untrusted data before cross-boundary use.
- G.CHK.02 Never log external data directly.
- G.CHK.03 Normalize and validate file paths from external data.
- G.CHK.04 Never construct regex directly from untrusted data.
- G.FIO.01 Delete temporary files after use.
- G.SER.01 Never serialize unencrypted sensitive data.
- G.SER.02 Prevent deserialization bypassing constructor security.
- G.SER.03 Maintain consistent serialization/deserialization types.
- G.SEC.01 Security check methods must not be `open`.
- P.03 Use defensive copies for external object security checks.
- G.OTH.01 Never log passwords, keys, or sensitive data.
- G.OTH.02 Never hardcode sensitive information.
- G.OTH.03 Avoid public network addresses in code.
- G.OTH.04 Use dedicated types (not String) for sensitive data; clear after use.
- FFI.C.7 Prevent truncation errors in pointer type conversions.

Optional rules (enable via `cjlint_rule_list.json`):

- G.NAM.06 Variables use camelCase.
- G.VAR.03 Avoid global variables.
- G.FMT.13 File headers should include license information.

## Specifications

- G.CON.02: Doesn't cover lock/unlock via assigned variables.

  The `lock()` function and `unlock()` function are assigned to variables. Scenarios where the assigned variables are then used for locking/unlocking operations are not covered by this rule check.

- G.OTH.03: Macro checking is unsupported.
- Macro checking requires correct package paths.

  Example: Macro source `a.cj` should be at `xxx/src/a/a.cj`.

- `cjlint` only checks invoked macros and cannot detect redundant macro code.

## Syntax Restriction Checking

1. Enable G.SYN.01 in `cjlint_rule_list.json` to check for prohibited syntax elements.

2. Currently supported restricted syntax:

   | Syntax          | Keyword          | Rationale                                  |
   | --------------- | ---------------- | ------------------------------------------ |
   | Package Import  | Import           | Prevent arbitrary imports                  |
   | Let Variables   | Let              | Use `var` exclusively                     |
   | Thread Creation | Spawn            | Disallow thread creation                   |
   | Synchronization | Synchronized     | Prevent deadlocks                          |
   | Main Function   | Main             | Disallow entry points                      |
   | Macro Definition| MacroQuote       | Allow macro use but not definition         |
   | Cross-Language | Foreign          | Disallow mixed-language programming        |
   | While Loops     | While            | Prevent complex/deadly loops               |
   | Extensions      | Extend           | Disallow extension syntax                  |
   | Type Aliases    | Type             | Disallow custom type aliases               |
   | Operator Overload| Operator        | Disallow operator overloading              |
   | Global Variables| GlobalVariable   | Prevent side effects/memory leaks          |
   | Enum Definition | Enum             | Avoid complex code                         |
   | Class Definition| Class            | Avoid complex code                         |
   | Interface Def.  | Interface        | Avoid complex code                         |
   | Struct Definition| Struct          | Avoid complex code                         |
   | Generic Def.    | Generic          | Avoid complex code                         |
   | Conditional Comp| When             | Prevent platform-specific code             |
   | Pattern Matching| Match            | Functional paradigm is hard to master      |
   | Exception Handling| TryCatch        | Prevent ignored errors                      |
   | Higher-Order Func| HigherOrderFunc | Avoid complexity                           |
   | Primitive Types | PrimitiveType    | Restrict to Int64, float64, bool           |
   | Container Types | ContainerType    | Use only List, Map, Set                     |

3. Add keywords to `structural_rule_G_SYN_01.json` to enable specific syntax restrictions. Example: Disallow imports

```json
{
  "SyntaxKeyword": [
    "Import"
  ]
}
```
