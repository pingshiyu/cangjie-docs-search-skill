# Accessing Threads

## Using `Future<T>` to Wait for Thread Completion and Retrieve Return Values

In the previous example, the newly created thread may terminate prematurely due to the main thread's completion. Without proper sequencing guarantees, it's even possible for the newly created thread to exit before getting a chance to execute. The return value of the `spawn` expression can be used to wait for thread completion.

The return type of the `spawn` expression is `Future<T>`, where `T` is a type parameter matching the return type of the lambda expression. When calling the `get()` member function of `Future<T>`, it will wait for the corresponding thread to complete execution.

The prototype declaration of `Future<T>` is as follows:

```cangjie
public class Future<T> {
    // Blocking the current thread, waiting for the result of the thread corresponding to the current Future object.
    // If an exception occurs in the corresponding thread, the method will throw the exception.
    public func get(): T

    // Blocking the current thread, waiting for the result of the thread corresponding to the current Future object.
    // If the corresponding thread has not completed execution within Duration, the method will throws TimeoutException.
    // If `timeout` <= Duration.Zero, its behavior is the same as `get()`.
    public func get(timeout: Duration): T

    // Non-blocking method that immediately returns Option<T>.None if thread has not finished execution.
    // Returns the computed result otherwise.
    // If an exception occurs in the corresponding thread, the method will throw the exception.
    public func tryGet(): Option<T>
}
```

The following example demonstrates how to use `Future<T>` to wait for the newly created thread to complete execution within the `main` function:

<!-- run -->

```cangjie
main(): Int64 {
    let fut: Future<Unit> = spawn { =>
        println("New thread before sleeping")
        sleep(100 * Duration.millisecond) // sleep for 100ms.
        println("New thread after sleeping")
    }

    println("Main thread")

    fut.get() // wait for the thread to finish.
    return 0
}
```

Calling `get()` on a `Future<T>` instance blocks the currently running thread until the thread represented by the `Future<T>` instance completes execution. Therefore, the above example might produce output similar to:

```text
New thread before sleeping
Main thread
New thread after sleeping
```

After printing, the main thread will wait for the newly created thread to complete due to the `get()` call. However, the printing order between the main thread and the new thread is nondeterministic.

If `fut.get()` is moved before the main thread's print statement as shown below:

<!-- verify -->

```cangjie
main(): Int64 {
    let fut: Future<Unit> = spawn { =>
        println("New thread before sleeping")
        sleep(100 * Duration.millisecond) // sleep for 100ms.
        println("New thread after sleeping")
    }

    fut.get() // wait for the thread to finish.

    println("Main thread")
    return 0
}
```

The main thread will wait for the newly created thread to complete before executing its print statement, making the program output deterministic as follows:

```text
New thread before sleeping
New thread after sleeping
Main thread
```

This demonstrates how the placement of `get()` calls affects whether threads can run concurrently.

Beyond blocking for thread completion, `Future<T>` can also retrieve execution results. Below are its specific member functions:

- `get(): T`: Blocks until thread completion and returns the execution result. If the thread has already completed, returns the result directly.

    Example code:

    <!-- verify -->

    ```cangjie
    main(): Int64 {
        let fut: Future<Int64> = spawn {
            sleep(Duration.second) // sleep for 1s.
            return 1
        }

        try {
            // wait for the thread to finish, and get the result.
            let res: Int64 = fut.get()
            println("result = ${res}")
        } catch (_) {
            println("oops")
        }
        return 0
    }
    ```

    Output:

    ```text
    result = 1
    ```

- `get(timeout: Duration): T`: Blocks until thread completion and returns the execution result. If the timeout period is reached before thread completion, throws TimeoutException. When `timeout <= Duration.Zero`, behaves identically to `get()`.

    Example code:

    <!-- verify -->

    ```cangjie
    main(): Int64 {
        let fut = spawn {
            sleep(Duration.second) // sleep for 1s.
            return 1
        }

        // wait for the thread to finish, but only for 1ms.
        try {
            let res = fut.get(Duration.millisecond * 1)
            println("result: ${res}")
        } catch (_: TimeoutException) {
            println("oops")
        }
        return 0
    }
    ```

    Output:

    ```text
    oops
    ```

## Accessing Thread Properties

Each `Future<T>` object corresponds to a Cangjie thread represented by a `Thread` object. The `Thread` class primarily provides access to thread property information, such as thread identifiers. Note that `Thread` objects cannot be directly instantiated—they can only be obtained through the `thread` member property of `Future<T>` or via the static `currentThread` property of the `Thread` class to get the `Thread` object representing the currently executing thread.

Partial method definitions of the `Thread` class are shown below (complete method descriptions can be found in the *Cangjie Programming Language Library API*).

```cangjie
class Thread {
    // Get the currently running thread
    static prop currentThread: Thread

    // Get the unique identifier (represented as an integer) of the thread object
    prop id: Int64

    // Check whether the thread has any cancellation request
    prop hasPendingCancellation: Bool
}
```

The following example demonstrates retrieving thread identifiers through both methods after creating a new thread. Since both the main thread and new thread access the same `Thread` object, they print identical thread identifiers.

<!-- run -->

```cangjie
main(): Unit {
    let fut = spawn {
        println("Current thread id: ${Thread.currentThread.id}")
    }
    println("New thread id: ${fut.thread.id}")
    fut.get()
}
```

Sample output (thread IDs may vary):

```text
New thread id: 1
Current thread id: 1
```