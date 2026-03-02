# Overview of I/O Streams

This chapter introduces fundamental I/O concepts and file operations.

In the Cangjie programming language, operations that interact with external carriers of applications are referred to as I/O operations. "I" stands for Input, and "O" stands for Output.

All I/O mechanisms in Cangjie are based on data streams for input and output, where these streams represent sequences of byte data. A data stream is a continuous collection of data, functioning like a pipeline that carries data—data is input at one end of the pipeline and output at the other.

The Cangjie programming language abstracts input and output as Streams.

- Reading data from external storage into memory is called an input stream (InputStream). The input end can write data into the pipeline segment by segment, and these segments form a long data stream in sequence.
- Writing data from memory to external storage is called an output stream (OutputStream). The output end can also read data from the pipeline segment by segment, where any length of data can be read each time (without needing to match the input end), but only earlier input data can be read before later input data.

With this layer of abstraction, the Cangjie programming language can use a unified interface to interact with external data.

The Cangjie programming language describes operations such as standard input/output, file operations, network data streams, string streams, encryption streams, compression streams, etc., uniformly using Stream.

Stream primarily deals with raw binary data, and the smallest data unit in a Stream is `Byte`.

The Cangjie programming language defines Stream as an `interface`, allowing different Streams to be combined using the decorator pattern, significantly enhancing extensibility.

## Input Stream

A program reads data sources (including external devices like keyboards, files, networks, etc.) from an input stream. In other words, an input stream is a communication channel that reads data sources into the program.

The Cangjie programming language uses the `InputStream` interface type to represent an input stream. It provides a `read` function, which writes readable data into a `buffer` and returns the total number of bytes read in that operation.

Definition of the InputStream interface:

<!-- run -->

```cangjie
interface InputStream {
    func read(buffer: Array<Byte>): Int64
}
```

When an input stream is available, byte data can be read as shown in the following code. The read data is written into the input parameter array of `read`.

Example of reading from an input stream:

```cangjie
import std.io.InputStream

main() {
    let input: InputStream = ...
    let buf = Array<Byte>(256, repeat: 0)
    while (input.read(buf) > 0) {
        println(buf)
    }
}
```

## Output Stream

A program writes data to an output stream. An output stream is a communication channel that outputs data from the program to external devices (such as displays, printers, files, networks, etc.).

The Cangjie programming language uses the `OutputStream` interface type to represent an output stream. It provides a `write` function, which writes data from the `buffer` into the bound stream.

Notably, some output streams' `write` operations do not immediately write to external storage but follow certain buffering strategies. Data is only physically written when certain conditions are met or when `flush` is explicitly called, aiming to improve performance.

To uniformly handle these `flush` operations, `OutputStream` includes a default implementation of `flush`, which helps smooth out API call differences.

Definition of the OutputStream interface:

```cangjie
interface OutputStream {
    func write(buffer: Array<Byte>): Unit

    func flush(): Unit {
        // Empty implementation
    }
}
```

When an output stream is available, byte data can be written.

Example of writing to an output stream:

```cangjie
import std.io.OutputStream

main() {
    let output: OutputStream = ...
    let buf = Array<Byte>(256, repeat: 111)
    output.write(buf)
    output.flush()
}
```

## Classification of Data Streams

Based on their functional differences, Streams can be broadly categorized into two types:

- **Node Streams**: Directly provide data sources. Node streams are typically constructed by relying on direct external resources (such as files, networks, etc.).
- **Processing Streams**: Can only delegate other data streams for processing. Processing streams are usually constructed by depending on other streams.