# Thread Sleep for Specified Duration

The `sleep` function blocks the currently running thread, causing it to voluntarily sleep for a specified duration before resuming execution. Its parameter type is `Duration`. The function prototype is:

```cangjie
func sleep(dur: Duration): Unit // Sleep for at least `dur`.
```

> **Note:**
>
> If `dur` <= Duration.Zero, the current thread will only yield execution resources without entering sleep mode.

Below is an example of using `sleep`:

<!-- verify -->

```cangjie
main(): Int64 {
    println("Hello")
    sleep(Duration.second)  // sleep for 1s.
    println("World")
    return 0
}
```

The output is as follows:

```text
Hello
World
```