# Concurrency Overview

Concurrency programming is an indispensable feature in modern programming languages. The Cangjie programming language provides a *preemptive thread model* as its concurrency mechanism. Threads can be categorized into two distinct concepts: **language threads** and **native threads**.

- **Language threads** are the fundamental execution units in a programming language's concurrency model. The Cangjie programming language aims to provide developers with a friendly, efficient, and unified concurrency programming interface, allowing them to focus on writing concurrent code without worrying about differences between operating system threads and user-mode threads. Therefore, it introduces the concept of **Cangjie threads**. In most cases, developers only need to write concurrent code targeting Cangjie threads.

- **Native threads** refer to the threads used in the language implementation (typically operating system threads), which serve as the concrete carriers for language threads. Different programming languages implement language threads in various ways. For example, some languages directly create threads through operating system calls, meaning each language thread corresponds to a native thread. This implementation is generally referred to as the `1:1` thread model. Alternatively, some languages provide specialized thread implementations that allow multiple language threads to switch execution across multiple native threads. This is known as the `M:N` thread model, where M language threads are scheduled to execute on N native threads, with M and N not necessarily being equal. Currently, the Cangjie language implementation also adopts the `M:N` thread model. Thus, Cangjie threads are essentially lightweight user-mode threads that support preemption and are more lightweight compared to operating system threads.

Cangjie threads are fundamentally lightweight user-mode threads. Each Cangjie thread is scheduled and executed by an underlying native thread, and multiple Cangjie threads can be executed by a single native thread. Each native thread continuously selects a ready Cangjie thread for execution. If a Cangjie thread blocks during execution (e.g., waiting for a mutex to be released), the native thread will suspend the current Cangjie thread and proceed to select the next ready one. A blocked Cangjie thread will resume execution once it becomes ready again.

In most cases, developers only need to focus on writing concurrent code for Cangjie threads without considering these details. However, during cross-language programming, developers must exercise caution when calling potentially blocking foreign functions, such as operating system calls related to I/O. For example, in the following code snippet, a new thread calls the foreign function `socket_read`. During program execution, a native thread will schedule and execute this Cangjie thread. Upon entering the foreign function, the system call will directly block the current native thread until the function completes. During this blocking period, the native thread cannot schedule other Cangjie threads for execution, which reduces the program's throughput.

```cangjie
foreign socket_read(sock: Int64): CPointer<Int8>

let fut = spawn {
    let sock: Int64 = ...
    let ptr = socket_read(sock)
}
```

> **Note:**
>
> In this document, the term **thread** will be used as a shorthand for **Cangjie thread** when there is no ambiguity.