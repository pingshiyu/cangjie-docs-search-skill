# Formatting Tool

## Feature Overview

`CJFMT (Cangjie Formatter)` is an automatic code formatting tool developed based on the Cangjie language programming specifications.

## Usage Instructions

Use the command line operation `cjfmt [option] file [option] file`

`cjfmt -h` displays help information and option descriptions.

```text
Usage:
     cjfmt -f fileName [-o fileName] [-l start:end]
     cjfmt -d fileDir [-o fileDir]
Options:
   -h            Show usage
                     eg: cjfmt -h
   -v            Show version
                     eg: cjfmt -v
   -f            Specifies the file to be formatted. The value can be a relative path or an absolute path.
                     eg: cjfmt -f test.cj
   -d            Specifies the directory containing files to be formatted. The value can be a relative path or an absolute path.
                     eg: cjfmt -d test/
   -o <value>    Output. For single file formatting, '-o' is followed by the output file name (supports relative/absolute paths).
                 For directory formatting, a path must be specified after -o (supports relative/absolute paths).
                     eg: cjfmt -f a.cj -o ./fmta.cj
                     eg: cjfmt -d ~/testsrc -o ./testout
   -c <value>    Specifies the formatting configuration file (supports relative/absolute paths).
                 If the specified config file fails to load, cjfmt will attempt to read the default config file from CANGJIE_HOME.
                 If the default config also fails, built-in configurations will be used.
                     eg: cjfmt -f a.cj -c ./config/cangjie-format.toml
                     eg: cjfmt -d ~/testsrc -c ~/home/project/config/cangjie-format.toml
   -l <region>   Only formats lines within the specified region of the provided file (only valid for single file formatting).
                 Region format: [start:end] where 'start' and 'end' are integers representing first/last lines to format (line count starts at 1).
                     eg: cjfmt -f a.cj -o ./fmta.cj -l 1:25
```

### File Formatting

`cjfmt -f`

- Format and overwrite source file (supports relative/absolute paths):

```shell
cjfmt -f ../../../test/uilang/Thread.cj
```

- Option `-o` creates a new `.cj` file with formatted output (supports relative/absolute paths for both source and output):

```shell
cjfmt -f ../../../test/uilang/Thread.cj -o ../../../test/formated/Thread.cj
```

### Directory Formatting

`cjfmt -d`

- Option `-d` specifies a directory of Cangjie source files to format (supports relative/absolute paths):

```shell
cjfmt -d test/              # Relative path source directory

cjfmt -d /home/xxx/test     # Absolute path source directory
```

- Option `-o` specifies output directory (can be existing or new; supports relative/absolute paths). Note: MAX_PATH length varies by system (e.g., typically ≤260 on Windows, ≤4096 recommended on Linux):

```shell
cjfmt -d test/ -o /home/xxx/testout

cjfmt -d /home/xxx/test -o ../testout/

cjfmt -d testsrc/ -o /home/../testout   # Error if source directory doesn't exist: "error: Source file path not exist!"
```

### Formatting Configuration

`cjfmt -c`

- Option `-c` allows specifying a custom formatting configuration file:

```shell
cjfmt -f a.cj -c ./cangjie-format.toml
```

Default cangjie-format.toml configuration (also represents built-in defaults):

```toml
# indent width
indentWidth = 4 # Range of indentWidth: [0, 8]

# limit length
linelimitLength = 120 # Range of indentWidth: [1, 120]

# line break type
lineBreakType = "LF" # "LF" or "CRLF"

# allow Multi-line Method Chain when it's level equal or greater than multipleLineMethodChainLevel
allowMultiLineMethodChain = false

# if allowMultiLineMethodChain's value is true,
# and method chain's level is equal or greater than multipleLineMethodChainLevel,
# method chain will be formatted to multi-line method chain.
# e.g. A.b().c() level is 2, A.b().c().d() level is 3
# ObjectA.b().c().d().e().f() =>
# ObjectA
#     .b()
#     .c()
#     .d()
#     .e()
#     .f()
multipleLineMethodChainLevel = 5 # Range of multipleLineMethodChainLevel: [2, 10]

# allow Multi-line Method Chain when it's length greater than linelimitLength
multipleLineMethodChainOverLineLength = true
```

> **Note:**
>
> If custom config file fails to load, the tool attempts to read default `cangjie-format.toml` from CANGJIE_HOME.
> If default config also fails, built-in formatting options are used.
> If any config option fails to load, the built-in default for that option is used.

### Partial Formatting

`cjfmt -l`

- Option `-l` formats only specified line ranges in a file (only works with single file formatting via `-f`; invalid with directory `-d` option):

```shell
cjfmt -f a.cj -o b.cj -l 10:25 // Formats only lines 10-25
```

## Formatting Rules

- Source files should sequentially contain copyright, package, import, and top-level elements, separated by blank lines.

【Correct Example】

```cangjie
// Part 1: Copyright
/*
 * Copyright (c) [Year of First Pubication]-[Year of Latest Update]. [Company Name]. All rights reserved.
 */

// Part 2: Package declaration
package com.myproduct.mymodule

// Part 3: Imports
import std.collection.HashMap   // Standard library

// Part 4: Public elements
public class ListItem <: Component {
    // CODE
}

// Part 5: Internal elements
class Helper {
    // CODE
}
```

> **Note:**
>
> The formatter doesn't enforce blank lines after copyright, but preserves one blank line if present.

- Consistent 4-space indentation.

【Correct Example】

```cangjie
class ListItem {
    var content: Array<Int64> // Correct: 4-space indent relative to class
    init(
        content: Array<Int64>, // Correct: 4-space indent for parameters
        isShow!: Bool = true,
        id!: String = ""
    ) {
        this.content = content
    }
}
```

- Uniform brace style (K&R for non-empty blocks).

【Correct Example】

```cangjie
enum TimeUnit { // Correct: Opening brace on same line with 1 preceding space
    Year | Month | Day | Hour
} // Correct: Closing brace on own line

class A { // Correct: Opening brace on same line
    var count = 1
}

func fn(a: Int64): Unit { // Correct: Opening brace on same line
    if (a > 0) { // Correct: Opening brace on same line
    // CODE
    } else { // Correct: Closing brace and 'else' on same line
        // CODE
    } // Correct: Closing brace on own line
}

// Lambda functions
let add = {
    base: Int64, bonus: Int64 => // Correct: Lambda follows K&R style
    print("Correct news")
    base + bonus
}
```

- Use spaces to highlight keywords per specification G.FMT.10.

【Correct Example】

```cangjie
var isPresent: Bool = false  // Correct: Space after colon
func method(isEmpty!: Bool): RetType { ... } // Correct: Space after colon in params/return

method(isEmpty: isPresent) // Correct: Space after colon in named args

0..MAX_COUNT : -1 // Correct: No spaces around range operator, spaces around step colon

var hundred = 0
do { // Correct: Space between 'do' and brace
    hundred++
} while (hundred < 100) // Correct: Space between 'while' and paren

func fn(paramName1: ArgType, paramName2: ArgType): ReturnType { // Correct: No inner paren spaces
    ...
    for (i in 1..4) { // Correct: No spaces around range operator
        ...
    }
}

let listOne: Array<Int64> = [1, 2, 3, 4] // Correct: No inner bracket/paren spaces

let salary = base + bonus // Correct: Spaces around binary operators

x++ // Correct: No space for unary operators
```

- Minimize unnecessary blank lines for compact code.

【Incorrect Example】

```cangjie
class MyApp <: App {
    let album = albumCreate()
    let page: Router
    // Blank line
    // Blank line
    // Blank line
    init() {           // Incorrect: Consecutive blank lines in type
        this.page = Router("album", album)
    }

    override func onCreate(): Unit {

        println( "album Init." )  // Incorrect: Blank lines inside braces

    }
}
```

- Remove unnecessary semicolons for conciseness.

【Before Formatting】

```cangjie
package demo.analyzer.filter.impl; // Redundant semicolon

internal import demo.analyzer.filter.StmtFilter; // Redundant semicolon
internal import demo.analyzer.CJStatment; // Redundant semicolon

func fn(a: Int64): Unit {
    println( "album Init." );
}
```

【After Formatting】

```cangjie
package demo.analyzer.filter.impl // Redundant semicolon removed

internal import demo.analyzer.filter.StmtFilter // Redundant semicolon removed
internal import demo.analyzer.CJStatment // Redundant semicolon removed

func fn(a: Int64): Unit {
    println("album Init.");
}
```

- Modifier keyword ordering per specification G.FMT.12.

Recommended top-level element modifier priority:

```cangjie
public
open/abstract
```

Recommended instance member function/property modifier priority:

```cangjie
public/protected/private
open
override
```

Recommended static member function modifier priority:

```cangjie
public/protected/private
static
redef
```

Recommended member variable modifier priority:

```cangjie
public/protected/private
static
```

- Multi-line comment formatting

Comments starting with `*` will align the `*` characters. Other comments preserve original formatting. Excess spaces after `*` are removed.

```cangjie
// Before formatting
/*
      * comment
      */

/*
        comment
        */

// After formatting
/*
 * comment
 */

/*
        comment
 */
```

## Important Notes

- The Cangjie formatter currently doesn't support formatting syntactically incorrect code.

- The Cangjie formatter currently doesn't support metaprogramming formatting.