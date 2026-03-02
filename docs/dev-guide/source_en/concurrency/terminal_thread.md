# Terminating Threads

The `cancel()` method of `Future<T>` can be used to send a termination request to the corresponding thread, but it does not forcibly stop thread execution. Developers need to check whether a termination request exists for the thread using the `hasPendingCancellation` property of `Thread`.

Generally, if a termination request exists for a thread, developers should implement appropriate thread termination logic. Therefore, how to terminate a thread is entirely up to the developer's discretion. If the developer ignores the termination request, the thread will continue executing until it completes normally.

Example code:

<!-- verify -->

```cangjie
import std.sync.SyncCounter

main(): Unit {
    let syncCounter = SyncCounter(1)
    let fut = spawn {
        syncCounter.waitUntilZero()  // block until the syncCounter becomes zero
        if (Thread.currentThread.hasPendingCancellation) {  // Check cancellation request
            println("cancelled")
            return
        }
        println("hello")
    }
    fut.cancel()    // Send cancellation request
    syncCounter.dec()
    fut.get() // Join thread
}
```

Output:

```text
cancelled
```