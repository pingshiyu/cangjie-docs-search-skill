# Creating Threads

When developers wish to execute a segment of code concurrently, they simply need to create a Cangjie thread. To create a new Cangjie thread, use the keyword `spawn` followed by a parameterless `lambda` expression, which represents the code to be executed in the new thread.

In the following example code, both the main thread and the new thread will attempt to print some text:

<!-- run -->

```cangjie
main(): Int64 {
    spawn { =>
        println("New thread before sleeping")
        sleep(100 * Duration.millisecond) // sleep for 100ms.
        println("New thread after sleeping")
    }

    println("Main thread")

    return 0
}
```

In the above example, the new thread will terminate along with the main thread when it ends, regardless of whether the new thread has completed its execution. The output of the above example may vary slightly each time and could produce something similar to:

```text
New thread before sleeping
Main thread

```

The `sleep()` function suspends the current thread for the specified duration before resuming execution, with the timing determined by the specified Duration type. For detailed information about `sleep()`, please refer to the [Sleeping for a Specified Duration](./sleep.md) section.