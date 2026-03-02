# Compilation, Errors, and Debugging

## Macro Compilation and Usage

The current compiler enforces that macro definitions and macro calls cannot reside in the same package. The macro package must be compiled first, followed by the package that calls the macros. Within the macro-calling package, macro definitions are not permitted. Since macros need to be exported from one package to another, the compiler requires macro definitions to be declared with the `public` modifier.

Below is a simple example.

Source directory structure:

```text
// Directory layout.
root_path
├── macros
│    └── m.cj
├── src
│    └── demo.cj
└─ target
```

Macro definitions are placed in the _macros_ subdirectory:

<!-- run -macro0 -->
<!-- cfg="--compile-macro" -->

```cangjie
// macros/m.cj
// In this file, we define the macro Inner, Outer.
macro package define
import std.ast.*

public macro Inner(input: Tokens) {
    return input
}

public macro Outer(input: Tokens) {
    return input
}

```

Macro calls are placed in the _src_ subdirectory:

<!-- run -macro0 -->

```cangjie
// src/demo.cj
import define.*
@Outer
class Demo {
    @Inner var state = 1
    @Inner var cnt = 42
}

main() {
    println("test macro")
}
```

When the compiled output of the macro definition file and the file using the macros are not in the same directory, the `--import-path` compilation option must be added to specify the path to the compiled output of the macro definition file. Below are the compilation commands for Linux (specific compilation options may evolve with cjc updates; refer to the latest cjc documentation for current options):

```shell
# First compile the macro definition file to generate the default dynamic library in the specified directory (the path can be specified, but not the library name)
cjc macros/m.cj --compile-macro --output-dir ./target

# Compile the file using macros, perform macro substitution, and generate the executable
cjc src/demo.cj -o demo --import-path ./target --output-dir ./target

# Run the executable
./target/demo
```

On Linux, this will generate `macro_define.cjo` for package management and the actual dynamic library file.

For Windows:

```shell
# Current directory: src

# First compile the macro definition file to generate the default dynamic library in the specified directory (the path can be specified, but not the library name)
cjc macros/m.cj --compile-macro --output-dir ./target

# Compile the file using macros, perform macro substitution, and generate the executable
cjc src/demo.cj -o demo.exe --import-path ./target --output-dir ./target
```

If the macro package depends on other dynamic libraries, ensure these dependencies are accessible during runtime (macro expansion relies on executing methods within the macro package). On Linux, set the `LD_LIBRARY_PATH` environment variable (on Windows, set `PATH`) to include the paths of the dependent libraries.

> **Note:**
>
> The macro substitution process depends on the Cangjie runtime. During macro substitution, the Cangjie runtime's initialization configuration uses the default settings provided by macros. Configuration parameters can be queried using Cangjie runtime operational logs. Among these, `cjHeapSize` and `cjStackSize` can be modified by users, while others currently cannot. Note that all parameters are invalid on the OpenHarmonyOS platform. The Cangjie runtime uses default values on the OpenHarmonyOS platform. For Cangjie runtime initialization configurations, refer to the [Runtime Initialization Optional Configurations](../Appendix/runtime_env.md#runtime-initialization-optional-configurations) section.

## Parallel Macro Expansion

The `--parallel-macro-expansion` option can be added when compiling macro-calling files to enable parallel macro expansion. The compiler automatically analyzes dependencies between macro calls, allowing independent macro calls to execute in parallel. For example, the two `@Inner` calls in the above example can be expanded in parallel, reducing overall compilation time.

> **Caution:**
>
> If macro functions rely on global variables, using parallel macro expansion may introduce risks.

<!-- compile -macro1 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define
import std.ast.*
import std.collection.HashMap

var Counts = HashMap<String, Int64>()

public macro Inner(input: Tokens) {
    for (t in input) {
        if (t.value.size == 0) {
            continue
        }
        // Count occurrences of all valid token values
        if (!Counts.contains(t.value)) {
            Counts[t.value] = 0
        }
        Counts[t.value] = Counts[t.value] + 1
    }
    return input
}

public macro B(input: Tokens) {
    return input
}
```

In the above code, if `@Inner` macro calls appear in multiple places and parallel macro expansion is enabled, accessing the global variable `Counts` may lead to conflicts, resulting in incorrect final counts.

It is recommended to avoid using global variables in macro functions. If unavoidable, either disable parallel macro expansion or protect global variables with Cangjie thread locks.

## diagReport Error Mechanism

The Cangjie standard library `std.ast` package provides the `diagReport` interface for custom error reporting. This allows macro definers to issue custom warnings or errors when parsing input Tokens with invalid content.

The custom error interface mimics the native compiler's error output format, supporting both warning and error-level messages.

The `diagReport` function prototype is as follows:

<!-- code_no_check -->

```cangjie
public func diagReport(level: DiagReportLevel, tokens: Tokens, message: String, hint: String): Unit
```

Parameter meanings:

- `level`: Error message severity level
- `tokens`: Tokens corresponding to the source code referenced in the error message
- `message`: Primary error message
- `hint`: Supplementary hint message

Refer to the following usage example.

Macro definition file:

<!-- compile.error -macro2 -->
<!-- cfg="--compile-macro" -->

```cangjie
// macro_definition.cj
macro package macro_definition

import std.ast.*

public macro testDef(input: Tokens): Tokens {
    for (i in 0..input.size) {
        if (input[i].kind == IDENTIFIER) {
            diagReport(DiagReportLevel.ERROR, input[i..(i + 1)],
                       "This expression is not allowed to contain identifier",
                       "Here is the illegal identifier")
        }
    }
    return input
}
```

Macro calling file:

<!-- compile.error -macro2 -->

```cangjie
// macro_call.cj
package macro_calling

import std.ast.*
import macro_definition.*

main(): Int64 {
    let a = @testDef(1)
    let b = @testDef(a)
    let c = @testDef(1 + a)
    return 0
}
```

During compilation of the macro-calling file, the following error messages will appear:

```text
error: This expression is not allowed to contain identifier
 ==> call.cj:9:22:
  |
9 |     let b = @testDef(a)
  |                      ^ Here is the illegal identifier
  |

error: This expression is not allowed to contain identifier
  ==> call.cj:10:26:
   |
10 |     let c = @testDef(1 + a)
   |                          ^ Here is the illegal identifier
   |

2 errors generated, 2 errors printed.
```

## Using --debug-macro to Output Macro Expansion Results

When using macros for compile-time code generation, errors can be particularly challenging to diagnose. This is a common but often difficult-to-locate issue for developers. The problem arises because the developer's source code undergoes transformations by macros, resulting in different code fragments. The compiler's error messages are based on the final macro-generated code, which does not directly correspond to the original source.

To address this, Cangjie macros provide a debug mode. In this mode, developers can inspect the complete macro-expanded code from the debug files generated by the compiler, as shown below.

Macro definition file:

<!-- compile -macro3 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro Outer(input: Tokens): Tokens {
    let messages = getChildMessages("Inner")

    let getTotalFunc = quote(public func getCnt() {
                       )
    for (m in messages) {
        let identName = m.getString("identifierName")
        getTotalFunc.append(Token(TokenKind.IDENTIFIER, identName))
        getTotalFunc.append(quote(+))
    }
    getTotalFunc.append(quote(0))
    getTotalFunc.append(quote(}))
    let funcDecl = parseDecl(getTotalFunc)

    let decl = (parseDecl(input) as ClassDecl).getOrThrow()
    decl.body.decls.add(funcDecl)
    return decl.toTokens()

}

public macro Inner(input: Tokens): Tokens {
    assertParentContext("Outer")
    let decl = parseDecl(input)
    setItem("identifierName", decl.identifier.value)
    return input
}
```

Macro calling file `demo.cj`:

<!-- compile -macro3 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

@Outer
class Demo {
    @Inner var state = 1
    @Inner var cnt = 42
}

main(): Int64 {
    let d = Demo()
    println("${d.getCnt()}")
    return 0
}

```

When compiling the file that uses macros, add the `--debug-macro` option to enable Cangjie macro's debug mode.

```shell
cjc --debug-macro demo.cj --import-path ./target
```

> **Note:**
>
> If using the Cangjie `CJPM` project manager for compilation, add the `--debug-macro` compilation option in the `cjpm.toml` configuration file to enable macro debug mode.
>
> ```text
> compile-option = "--debug-macro"
> ```

In debug mode, a temporary file `demo.cj.macrocall` will be generated, containing the macro-expanded code as follows:

<!-- code_no_check -->

```cangjie
// demo.cj.macrocall
/* ===== Emitted by MacroCall @Outer in demo.cj:3:1 ===== */
/* 3.1 */class Demo {
/* 3.2 */    var state = 1
/* 3.3 */    var cnt = 42
/* 3.4 */    public func getCnt() {
/* 3.5 */        state + cnt + 0
/* 3.6 */    }
/* 3.7 */}
/* 3.8 */
/* ===== End of the Emit ===== */
```

If the expanded macro code contains semantic errors, the compiler's error messages will trace back to the specific line and column numbers in the expanded code. The _debug_ mode of Cangjie macros has the following considerations:

- The _debug_ mode of macros will rearrange the source code's line and column information and is not suitable for certain special line-breaking scenarios. For example:

  <!-- code_no_check -->

  ```cangjie
  // before expansion
  @M{} - 2 // macro M returns 2

  // after expansion
  // ===== Emitted by Macro M at line 1 ===
  2
  // ===== End of the Emit =====
  - 2
  ```

  These cases where line breaks alter the semantics should not use _debug_ mode.

- Debugging macro calls within macro definitions is not supported and will result in compilation errors.

  <!-- compile.error -->

  ```cangjie
  public macro M(input: Tokens) {
      let a = @M2(1+2) // M2 is inside macro M, not suitable for debug mode.
      return input + quote($a)
  }
  ```

- Debugging macros with parentheses is not supported.

  <!-- compile.error -->

  ```cangjie
  // main.cj

  main() {
      // For macros with parentheses, newlines introduced by debug mode will change the semantics
      // of the expression, so it is not suitable for debug mode.
      let t = @M(1+2)
  }
  ```
