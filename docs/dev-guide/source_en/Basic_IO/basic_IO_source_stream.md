# I/O Node Streams

Node streams refer to streams that directly provide data sources. The construction of node streams typically relies on some direct external resource (such as files, networks, etc.).

Common node streams in the Cangjie programming language include standard streams (ConsoleReader, ConsoleWriter), file streams (File), network streams (Socket), etc.

This chapter introduces standard streams and file streams.

## Standard Streams

Standard streams include standard input stream, standard output stream, and standard error output stream.

Standard streams serve as the standard interface for programs to interact with external data. During program execution, data is read from the input stream as program input, output information is transmitted to the output stream, and similarly, error information is sent to the error stream.

In the Cangjie programming language, the global functions `getStdIn`, `getStdOut`, and `getStdErr` can be used to obtain these three standard streams respectively.

To use these functions, the `env` package needs to be imported:

Example of importing the env package:

<!-- run -->

```cangjie
import std.env.*
```

The `ConsoleReader` and `ConsoleWriter` types in the `env` package provide user-friendly wrappers for these three standard streams (since the standard error output stream is also an output stream, there are two types in total). They offer more convenient `String`-based extended operations and provide rich overloads for many common types to optimize performance.

Most importantly, `ConsoleReader` and `ConsoleWriter` types guarantee thread safety, allowing safe reading and writing through their interfaces in any thread.

By default, the standard input stream comes from keyboard input, such as text entered in a command-line interface.

When data needs to be obtained from the standard input stream, the `ConsoleReader` type can be acquired via the `getStdIn` global function, and then the `readln` function of this type can be used to get command-line input.

Example of reading from the standard input stream:

<!-- run -->

```cangjie
import std.env.getStdIn

main() {
    let consoleReader = getStdIn()
    let txt = consoleReader.readln()
    println(txt ?? "")
}
```

Run the above code, enter some text in the command line, and then press Enter to see the input content.

The output stream is divided into standard output stream and standard error stream. By default, both output to the screen, such as the text seen in the command-line interface.

When data needs to be written to the standard output stream, the `ConsoleWriter` can be obtained via the `getStdOut`/`getStdErr` global functions to write data, such as using the `write` function to print content to the console.

The difference between using `ConsoleWriter` and directly using the `print` function is that `ConsoleWriter` is thread-safe and, due to its caching technology, offers better performance when dealing with large amounts of content.

Note that after writing data, `flush` must be called on `ConsoleWriter` to ensure the content is completely written to the standard stream.

Example of writing to the standard output stream:

<!-- run -->

```cangjie
import std.env.getStdOut

main() {
    let consoleWriter = getStdOut()
    for (_ in 0..1000) {
        consoleWriter.writeln("hello, world!")
    }
    consoleWriter.flush()
}
```

## File Streams

The Cangjie programming language provides the `fs` package to support general file system tasks. Different operating systems offer varying interfaces for file systems. The Cangjie programming language abstracts the following common functionalities, providing unified interfaces to mask differences between operating systems and simplify usage.

Common operations include: creating files/directories, reading/writing files, renaming or moving files/directories, deleting files/directories, copying files/directories, obtaining file/directory metadata, and checking file/directory existence. Specific APIs can be found in the library documentation.

To use file system-related functionalities, the `fs` package must be imported:

Example of importing the fs package:

<!-- run -->

```cangjie
import std.fs.*
```

This chapter focuses on the usage of `File`. For `Path` and `Directory` usage, please refer to the corresponding API documentation.

The `File` type in the Cangjie programming language provides both conventional file operations and file stream functionalities.

### Conventional File Operations

For conventional file operations, a series of static functions can be used to perform quick operations.

For example, to check if a file exists at a certain path, the `exists` function can be used. When `exists` returns `true`, it indicates the file exists; otherwise, it does not.

Example of using the exists function:

<!-- run -->

```cangjie
import std.fs.exists

main() {
    let exist = exists("./tempFile.txt")
    println("exist: ${exist}")
}
```

Moving, copying, and deleting files are also straightforward. The `File` type provides corresponding static functions: `move`, `copy`, and `delete`.

Example of using move, copy, and delete functions:

<!-- compile -->

```cangjie
import std.fs.{copy, rename, remove}

main() {
    copy("./tempFile.txt", to: "./tempFile2.txt", overwrite: false)
    rename("./tempFile2.txt",  to: "./tempFile3.txt", overwrite: false)
    remove("./tempFile3.txt")
}
```

If all data from a file needs to be read at once or data needs to be written to a file in one go, the `readFrom` and `writeTo` functions provided by `File` can be used. For small amounts of data, these functions are both simple to use and offer good performance without manual stream handling.

Example of using readFrom and writeTo functions:

<!-- compile -->

```cangjie
import std.fs.File

main() {
    let bytes = File.readFrom("./tempFile.txt") // Reads all data at once
    File.writeTo("./otherFile.txt", bytes) // Writes all data to another file at once
}
```

### File Stream Operations

In addition to the conventional file operations mentioned above, the `File` type is also designed as a data stream type. Therefore, the `File` type implements the `IOStream` interface. When a `File` instance is created, it can be used as a data stream.

Definition of the File class:

```cangjie
public class File <: Resource & IOStream & Seekable {
    ...
}
```

`File` provides two construction methods: one uses the convenient static function `create` to directly create a new file instance, and the other uses a constructor with a complete file opening mode to create a new instance.

Files created with `create` are write-only; read operations on such instances will throw a runtime exception.

Example of File construction:

<!-- compile -->

```cangjie
// Create
internal import std.fs.*
internal import std.io.*

main() {
    let file = File.create("./tempFile.txt")
    file.write("hello, world!".toArray())

    // Open
    let file2 = File("./tempFile.txt", Read)
    let bytes = readToEnd(file2) // Reads all data
    println(bytes)
}
```

When more precise opening modes are needed, a constructor can be used with an `OpenMode` value. `OpenMode` is an `enum` type that provides rich file opening modes, including `Read`, `Write`, `Append`, and `ReadWrite`.

Example of using File opening modes:

```cangjie
// Open with specified options
let file = File("./tempFile.txt", Write)
```

Since opening a `File` instance consumes valuable system resources, it is important to close the `File` promptly after use to release system resources.

`File` implements the `Resource` interface, so in most cases, the try-with-resource syntax can be used to simplify operations.

Example of using try-with-resource syntax:

```cangjie
try (file2 = File("./tempFile.txt", Read)) {
    ...
    // Automatically releases the file after use
}
```