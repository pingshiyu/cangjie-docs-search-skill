# Exception Stack Trace Recovery Tool

## Overview

`cjtrace-recover` is an exception stack trace recovery tool for the Cangjie language.

If developers enable obfuscation when compiling Cangjie applications, the stack trace information in exceptions thrown during runtime will also be obfuscated, making it difficult to identify the root cause of issues. `cjtrace-recover` helps developers restore obfuscated exception stack traces for better problem diagnosis. Specifically, it can recover the following two types of information:

- Obfuscated function names
- Obfuscated path names

## Usage Instructions

Run `cjtrace-recover -h` to view command usage:

```text
cjtrace-recover -h
Usage: cjtrace-recover OPTION

Use symbol mapping files to recover obfuscated exception stacktrace. The supported options are:
    -f <file>       path to the obfuscated exception stacktrace file
    -m <file,...>   path to the symbol mapping files
    -h              display this help and exit
    -v              print version of cjtrace-recover
```

Developers can specify the exception stack trace file via the `-f` option and provide symbol mapping files via the `-m` option. `cjtrace-recover` will restore symbol names and path names in the stack trace based on the mapping relationships defined in the symbol mapping files, then output the recovered stack trace via standard output (`stdout`).

## Example

Assume an obfuscated Cangjie program throws the following exception stack trace:

```text
An exception has occurred:
MyException: this is myexception
     at a0(SOURCE:0)
     at ah(SOURCE:0)
     at c3(SOURCE:0)
     at cm0(SOURCE:0)
     at cm1(SOURCE:0)
     at ci0(:0)
```

And the symbol mapping file `test.obf.map` generated during obfuscated compilation contains:

```text
_ZN10mymod.mod111MyException6<init>ER_ZN8std.core6StringE a0 mymod/mod1/mod1.cj
_ZN10mymod.mod115my_common_func1Ev ah mymod/mod1/mod1.cj
_ZN10mymod.mod18MyClassA7myfunc1Eld c3 mymod/mod1/mod1.cj
_ZN7default6<main>Ev cm0 test1/test.cj
user.main cm1
cj_entry$ ci0
```

Save the exception stack trace to a file (e.g., `test_stacktrace`), then run the following command to recover it:

```shell
cjtrace-recover -f test_stacktrace -m test.obf.map
```

The tool will output the recovered stack trace:

```text
An exception has occurred:
MyException: this is myexception
     at mymod.mod1.MyException::init(std.core::String)(mymod/mod1/mod1.cj)
     at mymod.mod1.my_common_func1()(mymod/mod1/mod1.cj)
     at mymod.mod1.MyClassA::myfunc1(Int64, Float64)(mymod/mod1/mod1.cj)
     at default.main()(/home/zzx/repos/obf_test/test1/test.cj)
```

`cjtrace-recover` restores the stack trace based on the symbol mapping file and outputs the result via standard output stream (`stdout`).