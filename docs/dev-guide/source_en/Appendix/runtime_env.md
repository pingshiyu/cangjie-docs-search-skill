# Runtime Environment Variables Manual

This section introduces the environment variables provided by the `runtime`.

In Linux shell and macOS shell, you can set the environment variables provided by the Cangjie runtime using the following method:

```shell
$ export VARIABLE=value
```

In Windows cmd, you can set the environment variables provided by the Cangjie runtime using the following method:

```shell
> set VARIABLE=value
```

The subsequent examples in this section are based on Linux shell settings. If they do not match your platform, please choose the appropriate environment variable setting method for your platform.

## Runtime Initialization Optional Configurations

Notes:

1. All integer parameters are of Int64 type, and floating-point parameters are of Float64 type;
2. If no maximum value is explicitly specified for any parameter, the default implicit maximum value is the maximum value of that type;
3. If any parameter exceeds the valid range, the setting will be invalid, and the default value will be used automatically.
4. All parameters are invalid on the OHOS platform. The Cangjie runtime uses default values on the OHOS platform.

### `cjHeapSize`

Specifies the maximum size of the Cangjie heap. Supported units are kb (KB), mb (MB), and gb (GB). The valid range is [4MB, system physical memory]. Settings outside this range will be invalid, and the default value will be used. If the physical memory is less than 1GB, the default value is 64 MB; otherwise, it is 256 MB. The minimum supported configuration value for OpenHarmony and Android platforms is 64MB, the default value will be applied if the configured value is lower than this.

Example:

```shell
export cjHeapSize=4GB
```

### `cjRegionSize`

Specifies the size of the thread-local buffer for the region allocator. Supported units are kb (KB), mb (MB), and gb (GB). The valid range is [4kb, 2048kb]. Settings outside this range will be invalid, and the default value will be used. The default value is 64 KB. The minimum supported configuration value for the macOS platform is 16KB, the default value will be applied if the configured value is lower than this.

Example:

```shell
export cjRegionSize=1024kb
```

### `cjLargeThresholdSize`

Objects requiring large contiguous memory spaces (e.g., long arrays) are called large objects. Frequent allocation of large objects in the heap may lead to insufficient contiguous space, triggering heap overflow issues. Increasing the maximum size of large objects can improve the continuity of heap space.

In Cangjie, the threshold for large objects is the smaller of `cjLargeThresholdSize` and `cjRegionSize`. `cjLargeThresholdSize` supports units of kb (KB), mb (MB), and gb (GB), with a valid range of [4KB, 2048KB]. Settings outside this range will be invalid, and the default value will be used. The default value is 32 KB.

> **Note:**
>
> A larger threshold for large objects may impact program performance. Developers should set this value based on actual requirements.

Example:

```shell
export cjLargeThresholdSize=1024kb
```

### `cjExemptionThreshold`

Specifies the waterline value for live regions. The value must be in the range (0, 1]. When multiplied by the region size, if the size of live objects in a region exceeds this product, the region will not be reclaimed (with dead objects continuing to occupy memory). A higher value increases the likelihood of region reclamation, reducing heap fragmentation but potentially impacting performance due to frequent reclamation. Settings outside the range will be invalid, and the default value will be used. The default value is 0.8 (80%).

Example:

```shell
export cjExemptionThreshold=0.8
```

### `cjHeapUtilization`

Specifies the utilization rate of the Cangjie heap. This parameter is one of the references for updating the heap waterline after GC. The value must be in the range (0, 1]. The heap waterline is the threshold at which GC is triggered when the total size of objects in the heap reaches this value. A smaller value results in a higher updated heap waterline, reducing the likelihood of GC being triggered. Settings outside the range will be invalid, and the default value will be used. The default value is 0.8 (80%).

Example:

```shell
export cjHeapUtilization=0.8
```

### `cjHeapGrowth`

Specifies the growth rate of the Cangjie heap. This parameter is one of the references for updating the heap waterline after GC. The value must be greater than 0. The growth rate is calculated as 1 + cjHeapGrowth. A higher value results in a higher updated heap waterline, reducing the likelihood of GC being triggered. The default value is 0.15, indicating a growth rate of 1.15.

Example:

```shell
export cjHeapGrowth=0.15
```

### `cjAlloctionRate`

Specifies the object allocation rate of the Cangjie runtime. The value must be greater than 0, in MB/s, indicating the number of objects that can be allocated per second. The default value is 10240, meaning 10240 MB of objects can be allocated per second.

Example:

```shell
export cjAlloctionRate=10240
```

### `cjAlloctionWaitTime`

Specifies the wait time for object allocation in the Cangjie runtime. The value must be greater than 0. Supported units are s, ms, us, and ns, with nanoseconds (ns) recommended. If the time interval since the last object allocation is less than this value, the allocation will wait. The default value is 1000 ns.

Example:

```shell
export cjAlloctionWaitTime=1000ns
```

### `cjGCThreshold`

Specifies the reference waterline value for the Cangjie heap. Supported units are kb (KB), mb (MB), and gb (GB). The value must be a positive integer. GC is triggered when the Cangjie heap size exceeds this value. The default value is the heap size.

Example:

```shell
export cjGCThreshold=20480KB
```

### `cjGarbageThreshold`

When GC occurs, if the ratio of dead objects in a region exceeds this environment variable, the region will be added to the reclamation candidate set and may be reclaimed later (though other policies may prevent reclamation). The default value is 0.5, dimensionless, with a valid range of [0.0, 1.0].

Example:

```shell
export cjGarbageThreshold=0.5
```

### `cjGCInterval`

Specifies the interval between two GC operations. The value must be greater than 0. Supported units are s, ms, us, and ns, with milliseconds (ms) recommended. If the time since the last GC is less than this value, the current GC will be skipped. This parameter controls the frequency of GC. The default value is 150 ms.

Example:

```shell
export cjGCInterval=150ms
```

### `cjBackupGCInterval`

Specifies the interval for backup GC. The value must be greater than 0. Supported units are s, ms, us, and ns, with seconds (s) recommended. If the Cangjie runtime does not trigger GC within the specified time, a backup GC will be triggered. The default value is 240 seconds (4 minutes).

Example:

```shell
export cjBackupGCInterval=240s
```

### `cjProcessorNum`

Specifies the maximum concurrency of Cangjie threads. The valid range is (0, CPU cores * 2]. Settings outside this range will be invalid, and the default value will be used. The system API is called to obtain the number of CPU cores. If successful, the default value is the number of CPU cores; otherwise, it is 8.

Example:

```shell
export cjProcessorNum=2
```

### `cjStackSize`

Specifies the stack size of Cangjie threads. Supported units are kb (KB), mb (MB), and gb (GB). The valid range is [64KB, 1GB] on Linux and [128KB, 1GB] on Windows. Settings outside this range will be invalid, and the default value will be used. The default value is 128KB.

Example:

```shell
export cjStackSize=100kb
```

### Operational Logging Optional Configurations

#### `MRT_LOG_FILE_SIZE`

Specifies the file size for runtime operational logs. The default value is 10 MB. Supported units are kb (KB), mb (MB), and gb (GB). The value must be greater than 0.

When the log size exceeds this value, logging will restart from the beginning of the file.

The final log size will be slightly larger than MRT_LOG_FILE_SIZE.

Example:

```shell
export MRT_LOG_FILE_SIZE=100kb
```

#### `MRT_LOG_PATH`

Specifies the output path for runtime operational logs. If this environment variable is not set or the path setting fails, logs will default to stdout (standard output) or stderr (standard error).

Example:

```shell
export MRT_LOG_PATH=/home/cangjie/runtime/runtime_log.txt
```

#### `MRT_LOG_LEVEL`

Specifies the minimum output level for runtime operational logs. Logs at or above this level will be printed. The default value is e. Supported values are [v|d|i|w|e|f|s]: v (VERBOSE), d (DEBUG), i (INFO), w (WARNING), e (ERROR), f (FATAL), s (FATAL_WITHOUT_ABORT).

Example:

```shell
export MRT_LOG_LEVEL=v
```

#### `MRT_REPORT`

Specifies the output path for runtime GC logs. If this environment variable is not set or the path setting fails, logs will not be printed by default.

Example:

```shell
export MRT_REPORT=/home/cangjie/runtime/gc_log.txt
```

#### `MRT_LOG_CJTHREAD`

Specifies the output path for cjthread logs. If this environment variable is not set or the path setting fails, logs will not be printed by default.

Example:

```shell
export MRT_LOG_CJTHREAD=/home/cangjie/runtime/cjthread_log.txt
```

#### `cjHeapDumpOnOOM`

Specifies whether to generate a heap dump file after an OutOfMemory error. By default, this feature is disabled. Supported values are [on|off]. Setting it to "on" enables the feature; other values disable it.

Example:

```shell
export cjHeapDumpOnOOM=on
```

#### `cjHeapDumpLog`

Specifies the output path for heap dump files. Note that the specified path must exist, and the application executor must have read/write permissions. If not specified, heap dump files will be output to the current execution directory.

Example:

```shell
export cjHeapDumpLog=/home/cangjie
```

### Runtime Environment Optional Configurations

#### `MRT_STACK_CHECK`

Enables native stack overflow checking. By default, this feature is disabled. Supported values are 1, true, or TRUE to enable the feature.

Example:

```shell
export MRT_STACK_CHECK=true
```

#### `CJ_SOF_SIZE`

When a StackOverflowError occurs, the stack trace will be automatically folded for readability. The default number of folded stack frames is 32. This environment variable controls the length of the folded stack. Valid values are integers within the int range:

- CJ_SOF_SIZE = 0: Prints the entire stack trace.
- CJ_SOF_SIZE < 0: Prints the specified number of frames from the bottom of the stack.
- CJ_SOF_SIZE > 0: Prints the specified number of frames from the top of the stack.
- CJ_SOF_SIZE not set: Defaults to printing the top 32 frames of the stack.

Example:

```shell
export CJ_SOF_SIZE=30
```

### Cangjie GWP-Asan Memory Safety Detection

During interactions between Cangjie and C code, certain Cangjie heap memory safety issues may arise. Cangjie GWP-Asan provides a memory safety detection feature. It can detect Cangjie heap memory safety issues during program execution. GWP-Asan samples the `acquireArrayRawData` and `releaseArrayRawData` interfaces provided by the Cangjie standard library (see the "std.core" package section in the *Cangjie Programming Language Library API Documentation*), comparing Canary data before and after sampling to detect memory safety issues during Cangjie-C interactions.

Cangjie GWP-Asan is a sampling-based detection tool. The sampling frequency can be adjusted by setting different values to balance performance impact and detection coverage. At default or lower sampling frequencies, CPU performance overhead and additional memory usage are minimal.

> **Note:**
>
> Cangjie GWP-Asan memory safety detection is only supported on Linux and HarmonyOS.

#### cjEnableGwpAsan

Cangjie GWP-Asan memory safety detection is disabled by default. It can be enabled by setting the environment variable `cjEnableGwpAsan` to `1`, `true`, or `TRUE`. For Linux, the setting is as follows:

```shell
export cjEnableGwpAsan=true
```

#### cjGwpAsanSampleRate

When Cangjie GWP-Asan is enabled, the sampling frequency can be set via the `cjGwpAsanSampleRate` environment variable. `cjGwpAsanSampleRate` supports positive integers within the 32-bit integer range, i.e., $(0, 2^{31} - 1]$. The default value is 5000, meaning one sample is taken every 5000 `acquireArrayRawData` calls. For Linux, the setting is as follows:

```shell
export cjGwpAsanSampleRate=1000
```> **Note:**
>
> In Cangjie GWP-Asan memory safety detection, sampling impacts performance. Higher sampling rates result in greater performance overhead but detect more issues; lower sampling rates reduce performance impact but detect fewer issues. Adjust the sampling rate according to actual requirements.

#### cjGwpAsanHelp

The environment variable `cjGwpAsanHelp` controls whether to display GWP-Asan help information in the console. By default, this feature is disabled. When `cjGwpAsanHelp` is set to `1`, `true`, or `TRUE`, help information will be printed to the console. For Linux, configure as follows:

```shell
export cjGwpAsanHelp=true
```

#### Constraints

- Cangjie GWP-Asan is a sampling-based memory checking tool, which may not detect all memory boundary violations.
- Cangjie GWP-Asan has limited detection scope for out-of-bounds access on Cangjie heap memory. It cannot detect read out-of-bounds violations and only detects partial write out-of-bounds cases:
    - Forward write out-of-bounds within 8 bytes.
    - Backward write out-of-bounds into the padding area at the end (padding size varies from 0-7 bytes depending on array object length).

#### Error Detection Types

**Heap Memory Write Out-of-Bounds**

Heap memory write out-of-bounds occurs when a pointer accesses memory beyond the allocated array length, causing a Cangjie heap memory write violation.

1. Forward Out-of-Bounds

    For forward out-of-bounds array access, the runtime reports a "Head canary" check failure, indicated as `array[-1]`. Example:

    ```cangjie
    unsafe {
        let array = Array<UInt8>(4, item: 0)
        let cp = acquireArrayRawData(array)
        // The valid access range for the array is [0, 4). The following write operation accesses the -2nd byte, causing a 2-byte forward out-of-bounds violation. The error report uses array[-1] to indicate this behavior.
        cp.pointer.read(-2)
        releaseArrayRawData(array)
    }
    ```

    Corresponding error report:

    ```text
    2025-05-22 10:57:13.432786 41217 F Gwp-Asan sanity check failed on raw array addr 0x7f7c887368
    2025-05-22 10:57:13.432863 41217 F Head canary (array[-1]) mismatch: expect: 0x2, actual: 0x200000000000002
    2025-05-22 10:57:13.432878 41217 F Gwp-Asan Aborted.
    ```

2. Backward Out-of-Bounds

    For backward out-of-bounds array access, the runtime reports a "Tail canary" check failure, indicating the relative position beyond the array (`array`). Example:

    ```cangjie
    unsafe {
        let array = Array<UInt8>(4, item: 0)
        let cp = acquireArrayRawData(array)

        // The valid access range for the array is [0, 4). The following write operation accesses the 6th byte, causing a 2-byte backward out-of-bounds violation. The error report uses array[size+1] to indicate this behavior.
        cp.pointer.read(5)
        releaseArrayRawData(array)
    }
    ```

    Corresponding error report:

    ```text
    2025-05-22 10:53:09.564580 37872 F Gwp-Asan sanity check failed on raw array addr 0x7f6278a368
    2025-05-22 10:53:09.564761 37872 F Tail canary (array[size+1]) mismatch: expect: 0x6, actual: 0x2
    2025-05-22 10:53:09.564788 37872 F Gwp-Asan Aborted.
    ```

**Cangjie GC (Garbage Collection) Exception**

Failure to release an array reference with `releaseArrayRawData` after acquiring its pointer via `acquireArrayRawData` may cause Cangjie GC (Garbage Collection) exceptions.

During runtime shutdown, sampled arrays are checked for proper release via `releaseArrayRawData`. Unreleased arrays will report their heap addresses. Example:

```cangjie
unsafe {
    let array = Array<UInt8>(4, item: 0)
    let cp = acquireArrayRawData(array)
    cp.pointer.read()

    // Missing releaseArrayRawData
    return
}
```

Corresponding error report:

```text
2025-05-22 10:53:09.564761 1248614 F Unreleased array: 0x7fffd77f92d8
2025-05-22 10:53:09.564788 1248614 F Detect un-released array
```