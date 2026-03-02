# Debugging Tool

CJDB is a command-line debugging tool for Cangjie programs developed based on `lldb`. The current `cjdb` tool is adapted and evolved from the [llvm15.0.4](https://github.com/llvm/llvm-project/releases/tag/llvmorg-15.0.4) foundation, providing Cangjie developers with program debugging capabilities.

## Obtaining the `cjdb` Tool

### Acquisition Method

Obtain it through the `Cangjie` `SDK`.

The path of the `cjdb` tool in the `SDK`: `cangjie\tools\bin`.

### Usage Example

The following demonstrates the usage on the `Windows` platform:

   After decompression, simply run `cjdb.exe` in the tool's directory `cangjie\tools\bin`.

> **Note:**
>
> Explanation of `system` parameter values:
>
> | system parameter value | Description                    |
> | --------------------- | ------------------------------ |
> | windows               | Tool for Windows platform      |
> | linux                 | Tool for Linux platform        |
> | darwin                | Tool for macOS platform        |
>
> **Important**
>
> Ensure that the compiler used to build the ELF file or application being debugged matches the version of the toolchain from which the `cjdb` debugger was obtained.

## `cjdb` Commands

> **Note:**
>
> To view more commands, execute `help` in the command-line window:
>
> ```text
> (cjdb) help
> Debugger commands:
>   apropos           -- List debugger commands related to a word or subject.
>   breakpoint        -- Commands for operating on breakpoints (see 'help b' for shorthand.)
>   cjthread          -- Commands for operating on one or more cjthread in the current process.
>   command           -- Commands for managing custom LLDB commands.
>   disassemble       -- Disassemble specified instructions in the current target.  Defaults to the current function for the current thread and stack frame.
>   expression        -- Evaluate an expression on the current thread.  Displays any returned value with LLDB's default formatting.
>   frame             -- Commands for selecting and examing the current thread's stack frames.
> ...
> ```
>

### Logging

To facilitate issue localization, use the `log <subcommand> [<command-options>]` command to record `cjdb` logs.

- `help log` to view `log` command help

  ```text
  (cjdb) help log
  Commands controlling LLDB internal logging.
  Syntax: log <subcommand> [<command-options>]
  The following subcommands are supported:
        disable -- Disable one or more log channel categories.
        enable  -- Enable logging for a single log channel.
        list    -- List the log categories for one or more log channels.  If none specified, lists them all.
        timers  -- Enable, disable, dump, and reset LLDB internal performance timers.
  For more help on any particular subcommand, type 'help <command> <subcommand>'.
  ```

- `log list` to view supported log list

  ```text
  (cjdb) log list
  ```

  Other commands can be explored using the `help` command.

### Platform

Commands in `cjdb` for managing and creating platforms include `platform [connect|disconnect|info|list|status|select] ...`

- View `platform` help information on `windows` platform.

  ```text
  (cjdb) help platform
  Commands to manage and create platforms.
  Syntax: platform [connect|disconnect|info|list|status|select] ...
  The following subcommands are supported:
        connect        -- Select the current platform by providing a connection URL.
        disconnect     -- Disconnect from the current platform.
        file           -- Commands to access files on the current platform.
        get-file       -- Transfer a file from the remote end to the local host.
        get-size       -- Get the file size from the remote end.
        list           -- List all platforms that are available.
        mkdir          -- Make a new directory on the remote end.
        process        -- Commands to query, launch and attach to processes on the current platform.
        put-file       -- Transfer a file from this system to the remote end.
        select         -- Create a platform if needed and select it as the current platform.
        settings       -- Set settings for the current target's platform, or for a platform by name.
        shell          -- Run a shell command on the current platform.  Expects 'raw' input (see 'help raw-input'.)
        status         -- Display status for the current platform.
        target-install -- Install a target (bundle or executable file) to the remote end.
  For more help on any particular subcommand, type 'help <command> <subcommand>'.
  (cjdb)
  ```

### Functions

#### Stepping Into Functions with Debug Information

Use `thread step-over <cmd-options> [<thread-id>]` (`thread step-over` can be abbreviated as `next` or `n`) to skip stepping into functions and directly execute the next line of code.

```text
(cjdb) n
Process 2884 stopped
* thread #1, name = 'test', stop reason = step over
    frame #0: 0x0000000000401498 test`default.main() at test.cj:5:7
   2    main(): Int64 {
   3
   4       var a : Int32 = 12
-> 5       a = a + 23
   6       a = test(10, 34)
   7       return 1
   8    }
(cjdb)
```

When debugging with `cjdb`, use `thread step-in <cmd-options> [<thread-id>]` (`thread step-in` can be abbreviated as `step` or `s`) to step into functions (the function must have debug information).

```text
(cjdb) n
Process 5240 stopped
* thread #1, name = 'test', stop reason = step over
    frame #0: 0x00000000004014d8 test`default.main() at test.cj:6:7
   3
   4      var a : Int32 = 12
   5      a = a + 23
-> 6      a = test(10, 34)
   7      return 1
   8    }
   9
(cjdb) s
Process 5240 stopped
* thread #1, name = 'test', stop reason = step in
    frame #0: 0x0000000000401547 test`default.test(a=10, b=34) at test.cj:12:10
   9
   10   func test(a : Int32, b : Int32) : Int32 {
   11
-> 12     return a + b
   13   }
   14
(cjdb)
```

#### Exiting the Current Function

Execute the `finish` command to exit the current function and return to the previous call stack function.

```text
(cjdb) s
Process 5240 stopped
* thread #1, name = 'test', stop reason = step in
    frame #0: 0x0000000000401547 test`default.test(a=10, b=34) at test.cj:12:10
   9
   10   func test(a : Int32, b : Int32) : Int32 {
   11
-> 12     return a + b
   13   }
   14
(cjdb) finish
Process 5240 stopped
* thread #1, name = 'test', stop reason = step out

Return value: (int) $0 = 44

    frame #0: 0x00000000004014dd test`default.main() at test.cj:6:7
   3
   4      var a : Int32 = 12
   5      a = a + 23
-> 6      a = test(10, 34)
   7      return 1
   8    }
   9
(cjdb)
```

### Breakpoints

#### Setting Source Code Breakpoints

```text
breakpoint set --file test.cj --line line_number
```

`--line` specifies the line number.

`--file` specifies the file.

For single files, only the line number is required. For multiple files, the filename must be included.

`b test.cj:4` is shorthand for `breakpoint set --file test.cj --line 4`.

Example: **breakpoint set --line 2**

```text
(cjdb) b 2
Breakpoint 1: where = test`default.main() + 13 at test.cj:4:3, address = 0x0000000000401491
(cjdb) b test.cj : 4
Breakpoint 2: where = test`default.main() + 13 at test.cj:4:3, address = 0x0000000000401491
(cjdb)
```

#### Setting Function Breakpoints

```text
breakpoint set --name function_name
```

`--name` specifies the function name to set the breakpoint.

`b test` is shorthand for `breakpoint set --name test`.

Example: **breakpoint set --name test**

```text
(cjdb) b test
Breakpoint 3: where = test`default.test(int, int) + 19 at test.cj:12:10, address = 0x0000000000401547
(cjdb)
```

#### Setting Conditional Breakpoints

```text
breakpoint set --file xx.cj --line line_number --condition expression
```

`--file` specifies the file.

`--line` specifies the line number.

`--condition` specifies the condition.

Example: **breakpoint set --file test.cj --line 4 --condition a==12**

```text
(cjdb) breakpoint set --file test.cj --line 4 --condition a==12
Breakpoint 2: where = main`default::main() + 60 at test.cj:4:9, address = 0x00005555555b62d0
(cjdb) c
Process 3128551 resuming
Process 3128551 stopped
* thread #1, name = 'schmon', stop reason = breakpoint 2.1
    frame #0: 0x00005555555b62d0 main`default::main() at test.cj:4:9
   1    main(): Int64 {
   2
   3        var a : Int32 = 12
-> 4        a = a + 23
   5        return 1
   6    }
```

#### Continuing to the Next Breakpoint

```text
(cjdb) c
Process 2884 resuming
Process 2884 stopped
* thread #1, name = 'test', stop reason = breakpoint 3.1
    frame #0: 0x0000000000401547 test`default.test(a=10, b=34) at test.cj:12:10
   9
   10   func test(a : Int32, b : Int32) : Int32 {
   11
-> 12     return a + b
   13   }
   14
(cjdb)
```

### Watchpoints

```text
watchpoint set variable -w read variable_name
```

`-w` specifies the watchpoint type, which can be `read`, `write`, or `read_write`.

`wa s v` is shorthand for `watchpoint set variable`.

Example: **watchpoint set variable -w read a**

```text
(cjdb) wa s v -w read a
Watchpoint created: Watchpoint 1: addr = 0x7fffddffed70 size = 8 state = enabled type = r
    declare @ 'test.cj:27'
    watchpoint spec = 'a'
    new value: 10
(cjdb)
```

Watchpoints can only be set on basic types. On `Windows`, when setting conditions for watchpoints, the program will pause at most once.

### Expression Evaluation

In `cjdb`, expression evaluation can be performed using `expression <cmd-options> -- <expr>` (`expression` can be abbreviated as `expr`).

- Viewing literals

Example: **expr 3**

```text
(cjdb) expr 3
(Int64) $0 = 3
(cjdb)
```

- Viewing variable names

Example: **expr a**

```text
(cjdb) expr a
(Int64) $0 = 3
(cjdb)
```

- Viewing arithmetic expressions

Example: **expr a + b**

```text
(cjdb) expr a + b
(Int64) $0 = 3
(cjdb)
```

- Viewing relational expressions

Example: **expr a > b**

```text
(cjdb) expr a > b
(Bool) $0 = false
(cjdb)
```

- Viewing logical expressions

Example: **expr a && b**

```text
(cjdb) expr true && false
(Bool) $0 = false
(cjdb)
```

- Viewing postfix expressions

Example: **expr a.b**

```text
(cjdb) expr value.member
(Int64) $0 = 1
(cjdb)
```

Example: **expr a[b]**

```text
(cjdb) expr array[2]
(Int64) $0 = 3
(cjdb)
```

- Viewing generic instantiation variables

Example: **expr a**

```text
(cjdb) expr a
(default.A<Int32>) $0 = {
  member = 1
}
(cjdb)
```

Supported expression evaluations include but are not limited to: literals, variable names, parenthesized expressions, arithmetic expressions, relational expressions, conditional expressions, loop expressions, member access expressions, index access expressions, range expressions, bitwise operation expressions, generic instantiation variables, etc.

> **Note:**
>
> Unsupported expression evaluations include: function calls with named parameters, interop, extensions, attributes, aliases, interpolated strings, function names. The `Windows` platform does not support the Float16 type, and exception throwing is not supported.

### Variable Inspection

- Viewing local variables, `locals`

```text
(cjdb) locals
(Int32) a = 12
(Int64) b = 68
(Int32) c = 13
(Array<Int64>) array = {
  [0] = 2
  [1] = 4
  [2] = 6
}
(pkgs.Rec) newR2 = {
  age = 5
  name = "string"
}
(cjdb)
```

When the debugger stops at a certain point in the program, using `locals` allows you to see all local variables within the scope of the current function's lifecycle. Only variables that have been initialized at the current position can be correctly viewed; uninitialized variables cannot be properly inspected.

- Viewing a single variable, `print variable_name`

Example: **print b**

```text
(cjdb) print b
(Int64) $0 = 110
(cjdb)
```

Use the `print` command (abbreviated as `p`), followed by the name of the specific variable to inspect.

- Viewing String type variables

```text
(cjdb) print newR2.name
(String) $0 = "string"
(cjdb)
```

- Viewing struct and class type variables

```text
(cjdb) print newR2
(pkgs.Rec) $0 = {
  age = 5
  name = "string"
}
(cjdb)
```

- Viewing arrays

```text
(cjdb) print array
(Array<Int64>) $0 = {
  [0] = 2
  [1] = 4
  [2] = 6
  [3] = 8
}
(cjdb) print array[1..3]
(Array<Int64>) $1 = {
  [1] = 4
  [2] = 6
}
(cjdb)
```

Supports viewing basic types (Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64, Float16, Float32, Float64, Bool, Unit, Rune).

Supports range viewing. The interval `[start..end)` is a left-closed, right-open interval. Reverse order is currently not supported.

For illegal intervals or attempting to view ranges on non-array types, an error message will be displayed.

```text
(cjdb) print array
(Array<Int64>) $0 = {
  [0] = 0
  [1] = 1
}
(cjdb) print array[1..3]
error: unsupported expression
(cjdb) print array[0][0]
error: unsupported expression
```

- Viewing CString type variables

```text
(cjdb) p cstr
(cro.CString) $0 = "abc"
(cjdb) p cstr
(cro.CString) $1 = null
```

- Viewing global variables, `globals`

```text
(cjdb) globals
(Int64) pkgs.Rec.g_age = 100
(Int64) pkgs.g_var = 123
(cjdb)
```

When using the `print` command to view a single global variable, `print` + package name + variable name is not supported. Only `print` + variable name is supported. For example, to view the global variable `g_age`, use the following command:

```text
(cjdb) p g_age
(Int64) $0 = 100
(cjdb)
```

- Modifying variables

```text
(cjdb) set a=30
(Int32) $4 = 30
(cjdb)
```

You can use `set` to modify the value of a local variable. Only basic numeric types are supported (Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64, Float32, Float64).

For `Bool` type variables, you can use the value 0 (false) or non-zero (true) to modify them. For `Rune` type variables, you can use the corresponding `ASCII` code to modify them.

```text
(cjdb) set b = 0
(Bool) $0 = false
(cjdb) set b = 1
(Bool) $1 = true
(cjdb) set c = 0x41
(Rune) $2 = 'A'
(cjdb)
```

If the modified value is non-numeric or exceeds the variable's range, an error message will be displayed.

```text
(cjdb) p c
(Rune) $0 = 'A'
(cjdb) set c = 'B'
error: unsupported expression
(cjdb) p b
(Bool) $1 = false
(cjdb) set b = true
error: unsupported expression
(cjdb) p u8
(UInt8) $3 = 123
(cjdb) set u8 = 256
error: unsupported expression
(cjdb) set u8 = -1
error: unsupported expression
```

### Cangjie Threads

Supports viewing Cangjie thread `id` status and `frame` information. Thread switching is currently not supported.

#### Displaying threads in the current target process

```text
(cjdb) cjthread list
cjthread id: 1, state: running name: cjthread1
    frame #0: 0x000055555557c140 main`ab::main() at varray.cj:16:1
cjthread id: 2, state: pending name: cjthread2
    frame #0: 0x00007ffff7d8b9d5 libcangjie-runtime.so`CJ_CJThreadPark + 117
(cjdb)
```

#### Stack Backtrace

- Viewing the call stack of a specified Cangjie thread.

```text
(cjdb) cjthread backtrace 1
cjthread #1 state: pending name: cangjie
  frame #0: 0x00007ffff7d8b9d5 libcangjie-runtime.so`CJ_CJThreadPark + 117
  frame #1: 0x00007ffff7d97252 libcangjie-runtime.so`CJ_TimerSleep + 66
  frame #2: 0x00007ffff7d51b5d libcangjie-runtime.so`CJ_MRT_FuncSleep + 33
  frame #3: 0x0000555555591031 main`std/sync::sleep(std/time::Duration) + 45
  frame #4: 0x0000555555560941 main`default::lambda.0() at complex.cj:9:3
  frame #5: 0x000055555555f68b main`default::std/core::Future<Unit>::execute(this=<unavailable>) at future.cj:124:35
  frame #6: 0x00007ffff7d514f1 libcangjie-runtime.so`___lldb_unnamed_symbol1219 + 7
  frame #7: 0x00007ffff7d4dc52 libcangjie-runtime.so`___lldb_unnamed_symbol1192 + 114
  frame #8: 0x00007ffff7d8b09a libcangjie-runtime.so`CJ_CJThreadEntry + 26
(cjdb)
```

In the `cjthread backtrace 1` command, `1` is the specified `cjthread ID`.

## Executable File Debugging

### Launch Method

There are two ways to load the target program using the launch method:

1. Start the debugger and load the target program simultaneously.

    ```text
    ~/0901/cangjie_test$ cjdb test
    (cjdb) target create "test"
    Current executable set to '/0901/cangjie-linux-x86_64-release/bin/test' (x86_64).
    (cjdb)
    ```

2. Start the debugger first, then load the target program using the `file` command.

    ```text
    ~/0901/cangjie_test$ cjdb
    (cjdb) file test
    Current executable set to '/0901/cangjie/test' (x86_64).
    (cjdb)
    ```

### Attach Mode

Debugging the target program via attach mode

For already running programs, cjdb supports debugging through attach mode as follows:

```text
~/0901/cangjie-linux-x86_64-release/bin$ cjdb
(cjdb) attach 15325
Process 15325 stopped
* thread #1, name = 'test', stop reason = signal SIGSTOP
    frame #0: 0x00000000004014cd test`default.main() at test.cj:7:9
   4      var a : Int32 = 12
   5      a = a + 23
   6      while (true) {
-> 7        a = 1
   8      }
   9      a = test(10, 34)
   10     return 1
  thread #2, name = 'FinalProcessor', stop reason = signal SIGSTOP
    frame #0: 0x00007f48c12fc065 libpthread.so.0`__pthread_cond_timedwait at futex-internal.h:205
  thread #3, name = 'PoolGC_1', stop reason = signal SIGSTOP
    frame #0: 0x00007f48c12fbad3 libpthread.so.0`__pthread_cond_wait at futex-internal.h:88
  thread #4, name = 'MainGC', stop reason = signal SIGSTOP
    frame #0: 0x00007f48c12fc065 libpthread.so.0`__pthread_cond_timedwait at futex-internal.h:205
  thread #5, name = 'schmon', stop reason = signal SIGSTOP
    frame #0: 0x00007f48c0fe17a0 libc.so.6`__GI___nanosleep(requested_time=0x00007f48a8ffcb70, remaining=0x0000000000000000) at nanosleep.c:28

Executable module set to "/0901/cangjie-linux-x86_64-release/bin/test".
Architecture set to: x86_64-unknown-linux-gnu.
```

### Android Remote Debugging

- To perform remote debugging, first start the `lldb-server` on the Android platform.

```text
adb shell /data/local/tmp/lldb-server platform --listen "*:1234"
```

- Launch the debugger in a separate window.

```text
(cjdb) platform select remote-android
  Platform: remote-android
 Connected: no
(cjdb) platform connect connect://FMR0223A31052288:1234
  Platform: remote-android
    Triple: aarch64-unknown-linux-android
OS Version: 31 (5.10.43)
  Hostname: localhost
 Connected: yes
WorkingDir: /
    Kernel: #1 SMP PREEMPT Wed Mar 20 12:20:52 CST 2024
(cjdb) attach 29551
(cjdb) Process 29551 stopped
* thread #1, name = 'main', stop reason = signal SIGSTOP
    frame #0: 0x0000007f83f7c5e4 libc.so`nanosleep + 4
libc.so`nanosleep:
->  0x7f83f7c5e4 <+4>:  svc    #0
    0x7f83f7c5e8 <+8>:  cmn    x0, #0x1, lsl #12         ; =0x1000
    0x7f83f7c5ec <+12>: cneg   x0, x0, hi
    0x7f83f7c5f0 <+16>: b.hi   0x7f83f7b6cc              ; __set_errno_internal
Executable module set to "C:\Users\user\.lldb\module_cache\remote-android\.cache\88DA3010\main".
Architecture set to: aarch64-unknown-linux-android.
(cjdb)
```

Select the Android platform for remote debugging.

```text
platform select remote-android
```

Connect to the Android device for remote debugging.

```text
platform connect connect://FMR0223A31052288:1234
```

Attach to a process for remote debugging.

```text
attach 29551
```

### iOS Simulator Remote Debugging

Since running programs on the iOS simulator requires launching via `Xcode`, follow these steps when debugging programs running on the iOS simulator using `cjdb`:

1. First, launch the target program using `Xcode`.

2. Use the `detach` command in the `Xcode lldb` command line to disconnect debugging.

3. Start `cjdb` from the command line and use the `attach` command to load the target program.

Once successfully loaded, you can proceed with normal debugging using `cjdb`. Due to version differences between `Xcode` and `cjdb` dependencies on `llvm`, additional compilation parameters `-gdwarf-4` must be added during compilation.

### iOS Device Remote Debugging

Due to iOS device security policies, `cjdb` cannot directly debug programs on physical devices. Debugging must be performed using `lldb` bundled with `Xcode`. Therefore, a `Python` script extension is provided to support debugging Cangjie programs.

To debug programs running on an iOS device, follow these steps. For compilation instructions, refer to the "Compilation and Building" chapter in the *Cangjie Programming Language Development Guide*.

1. First, launch the target program using `Xcode`.

2. Load the script in the `Xcode` debug window command line using the command: `command script import $CANGJIE_HOME/tools/script/cangjie_cjdb.py`, where `$CANGJIE_HOME` should be replaced with the Cangjie installation directory.
   To automatically load the script every time `Xcode` starts debugging, create a `.lldbinit` file in the user directory and enter the above command.

3. Once successfully loaded, normal debugging can proceed.

Since iOS devices use `Python` script extension capabilities, the debugging features are limited by the `Python` capabilities exposed by `lldb`. Therefore, there are differences in supported debugging features compared to `cjdb`. Expression evaluation, conditional breakpoints, and `demangle` functionality are currently unsupported. `None` will be displayed as `nullptr`.

#### Viewing Cangjie Thread Call Stacks

Use the `cjthread` command to view Cangjie call stacks.

```text
  (lldb) cjthread
  cjthread #6 state: pending name:
    frame #0: 0x7ffff7f0299d libcangjie-runtime.so`CJ_CJThreadPark
    frame #1: 0x7ffff7f19f3e libcangjie-runtime.so`CJ_TimerSleep
    frame #2: 0x7ffff7e1c95a libcangjie-runtime.so`MRT_Sleep
    frame #3: 0x7ffff7e224c1 libcangjie-runtime.so`CJ_MRT_Sleep
    frame #4: 0x55555563a5e9 main`std.core.sleep(std.core::Duration) at sleep.cj:36
    frame #5: 0x5555555f3e0b main`default.create_spawn::lambda.0() at cjthread.cj:8
    frame #6: 0x5555555f3f67 main`_CCN7default12create_spawnHRNat6StringEEL_E$g
    frame #7: 0x5555556425ba main`std.core.Future<...>::execute() at future.cj:161
  cjthread #5 state: pending name:
    frame #0: 0x7ffff7f0299d libcangjie-runtime.so`CJ_CJThreadPark
    frame #1: 0x7ffff7f19f3e libcangjie-runtime.so`CJ_TimerSleep
    frame #2: 0x7ffff7e1c95a libcangjie-runtime.so`MRT_Sleep
    frame #3: 0x7ffff7e224c1 libcangjie-runtime.so`CJ_MRT_Sleep
    frame #4: 0x55555563a5e9 main`std.core.sleep(std.core::Duration) at sleep.cj:36
    frame #5: 0x5555555f3e0b main`default.create_spawn::lambda.0() at cjthread.cj:8
    frame #6: 0x5555555f3f67 main`_CCN7default12create_spawnHRNat6StringEEL_E$g
    frame #7: 0x5555556425ba main`std.core.Future<...>::execute() at future.cj:161
```

> **Note:**
>
> Currently, mixed call stacks (i.e., call stacks containing frames from other languages) cannot be displayed. A maximum of 100 Cangjie thread call stacks can be shown. Each Cangjie thread call stack is limited to displaying 2048 bytes.

## Notes

1. The program being debugged must be compiled in `debug` version, such as programs compiled with the following command:

    ```shell
    cjc -g test.cj -o test
    ```

2. When a developer defines a generic object and steps into its `init` function during debugging, the stack information will display two package names: one for the package where the generic object is instantiated, and another for the package where the generic is defined.

    ```text
    * thread #1, name = 'main', stop reason = step in
        frame #0: 0x0000000000404057 main`default.p1.Pair<String, Int64>.init(a="hello", b=0) at a.cj:21:9
       18       let x: T
       19       let y: U
       20       public init(a: T, b: U) {
    -> 21           x = a
       22           y = b
       23       }
    ```

3. For displaying `Enum` types, if the enum constructor has parameters, it will be displayed as follows:

    ```cangjie
    enum E {
        Ctor(Int64, String) | Ctor
    }

    main() {
        var temp = E.Ctor(10, "String")
        0
    }

    ========================================
    (cjdb) p temp
    (E) $0 = Ctor {
      arg_1 = 10
      arg_2 = "String"
    }
    ```

    Note that `arg_x` is not an actual printable member variable - the `Enum` does not actually contain member variables named `arg_x`.

4. The Cangjie `cjdb` is built upon `lldb`, thus supporting all native basic functionalities of `lldb`. For details, refer to the [lldb official documentation](https://lldb.llvm.org).

5. If developers run cjdb on system environments newer than the version of `llvm15.0.4` , compatibility issues and risks may arise, such as in C language interoperability scenarios where `cjdb` cannot properly resolve C code file and line number information.

    ```c
    int32_t cfoo()
    {
        printf("cfoo\n");
        return 0;
    }
    ```

    ```cangjie
    foreign func cfoo(): Int32
    unsafe main() {
        cfoo()
    }
    ```

    ```shell
    # step 1: Compile C file using system's native clang version to generate dylib
    clang -g -shared cffi.c -o libcffi.dylib
    # step 2: Compile CJ file using cjc and link with C dynamic library
    cjc -g test.cj -L. -lcffi -o test
    # step 3: Debug test file using cjdb (C code debugging fails due to incompatible debug info)
    cjdb test
    ```

    ```text
    (cjdb) target create "test"
    Current executable set to 'test' (x86_64).
    (cjdb) b cfoo
    Breakpoint 1: where = libcffi.dylib`cfoo + 4, address = 0x0000000000000f84
    (cjdb) r
    Process 3133 launched: 'test' (x86_64)
    Process 3133 stopped
    * thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
        frame #0: 0x00000001000a6f84 libcffi.dylib`cfoo
      1    foreign func cfoo(): Int32
      2    unsafe main() {
      3        cfoo()
    -> 4    }
    ```

## FAQ

1. cjdb reports `error: process launch failed: 'A' packet returned an error: 8` in `docker` environment.

    ```text
    root@xxx:/home/cj/cangjie-example#cjdb ./hello
    (cjdb) target create "./hello"
    Current executable set to '/home/cj/cangjie-example/hello' (x86_64).
    (cjdb) b main
    Breakpoint 1: 2 locations.
    (cjdb) r
    error: process launch failed: 'A' packet returned an error: 8
    (cjdb)
    ```

    Cause: The container was created without SYS_PTRACE capability.

    Solution: Create new container with following options and remove existing container:

    ```shell
    docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --security-opt apparmor=unconfined
    ```

2. cjdb reports `stop reason = signal XXX`.

    ```text
    Process 32491 stopped
    * thread #2, name = 'PoolGC_1', stop reason = signal SIGABRT
        frame #0: 0x00007ffff450bfb7 lib.so.6`__GI_raise(sig=2) at raise.c:51
    ```

    Cause: The program continuously generates `SIGABRT` signals triggering debugger pauses.

    Solution: Execute following command to ignore such signals:

    ```text
    (cjdb) process handle --pass true --stop false --notify true SIGBUS
    NAME         PASS   STOP   NOTIFY
    ===========  =====  =====  ======
    SIGBUS       true   false  true
    (cjdb)
    ```

3. cjdb doesn't catch `SIGSEGV` signals.

    Cause: cjdb is configured by default not to catch `SIGSEGV` signals.

    Solution: Developers needing to catch this signal during debugging can reconfigure with:

    ```text
    (cjdb)process handle -p true -s true -n true SIGSEGV
    NAME         PASS   STOP   NOTIFY
    ===========  =====  =====  ======
    SIGSEGV      true   true   true
    (cjdb)
    ```

4. cjdb cannot step into `catch` blocks using `next/s` commands.

    Cause: Cangjie uses `LandingPad` mechanism for exception handling, which cannot deterministically identify which `catch` block will handle exceptions from `try` blocks. Similar issues exist in `clang++`.

    Solution: Developers needing to debug `catch` blocks should set breakpoints within them.

    ```text
    (cjdb) b 31
    Breakpoint 2: where = main`default::test(Int64) + 299 at a.cj:31:18, address = 0x000055555557caff
    (cjdb) n
    Process 1761640 stopped
    * thread #1, name = 'schmon', stop reason = breakpoint 2.1
        frame #0: 0x000055555557caff main`default::test(a=0) at a.cj:31:18
      28      s = 12/a
      29    } catch (e:Exception) {
      30
    ->31     error_result = e.toString()
      32     println(error_result)
      33    }
      34    s
    (cjdb)
    ```

5. Expression evaluation error on `macOS`: `Expression can't be run, because there is no JIT compiled function`.

    Cause: Expression evaluation is currently unsupported on `macOS` platform.

6. On `macOS` aarch64 architecture, some environments report `Connection shut down by remote side while waiting for reply to initial handshake packet` during expression evaluation.

    Cause: Some systems cause debug service abnormal termination.

    Solution: Delete `third_party/llvm/bin/debugserver` file and restart debugging.

7. When setting breakpoints involving generic type parameters, the parameter names appear as T0, T1, ... Tn. Example:

    ```cangjie
    func global_func_02<K, G>() { 0 }
    public struct Pair<T, U> {
        let x: T
        let y: U
        public init(a: T, b: U) {
            x = a
            y = b
        }
    }
    main() {
        var a: Pair<String, Int64> = Pair<String, Int64>("hello", 0)
        global_func_02<Int64, String>()
        0
    }

    ========================================
    (cjdb) b 1
    Breakpoint 1: where = main`default::global_func_02<T0,T1>() + 9 at test.cj:1:33, address = 0x0000000000019989
    (cjdb) b 6
    Breakpoint 2: where = main`default::Pair<T0,T1>::init(T0, T1) + 150 at test.cj:6:9, address = 0x000000000001982a
    ```

    Cause: Cangjie maintains ABI compatibility for generic type parameters - when developer-side generic parameter names change, the symbol names in Cangjie's binary symbol table remain unchanged.

    Solution: Modify developer-written generic parameter names to T0, T1, ... Tn.
