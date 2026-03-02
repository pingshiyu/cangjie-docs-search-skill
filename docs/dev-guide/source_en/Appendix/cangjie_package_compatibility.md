# Cangjie Package Compatibility Check

This chapter introduces the new feature **Cangjie Package Compatibility Check** introduced starting from version 0.59.4. During the process of loading Cangjie packages by the Cangjie runtime, binary compatibility checks are performed to help developers identify compatibility issues, though it cannot intercept all binary compatibility problems.

> **Note:**
>
> This new feature is only applicable to version 0.59.4 and later. If the runtime or standard library contains versions prior to 0.59.4, compatibility is not guaranteed, nor can normal operation be ensured.

## Check Rules

Assume the version number of the Cangjie runtime is `a.b.c`, and the version number of the Cangjie package to be loaded is `x.y.z`. Compatibility is satisfied if any of the following conditions are met:

- When both `a` and `x` are 0, `a == x && b == y && c == z`.
- When both `a` and `x` are not 0, `a == x`.

If the two versions are compatible, the subsequent package loading process continues. If the compatibility requirements are not met, the following two error scenarios may occur:

- Scenario 1: If the loaded package is the Cangjie core package, the Cangjie runtime terminates execution, and the error message includes the Cangjie runtime version number and the core package version number.

    ```shell
    F executable cangjie file libcangjie-std-core.so version 0.59.3 is not compatible with deployed cangjie runtime version 0.59.5
    ```

- Scenario 2: If the loaded package is any package other than the Cangjie core package, the Cangjie runtime reports an error and throws an IncompatiblePackageException, with the error message including the Cangjie runtime version number and the loaded package version number.

    ```shell
    E executable cangjie file liba.so version 0.59.5 is not compatible with deployed cangjie runtime version 0.59.3
    An exception has occurred:
    IncompatiblePackageException: executable cangjie file liba.so version 0.59.5 is not compatible with deployed cangjie runtime version 0.59.3
        at package_global_init(:0)
        at package_global_init(:0)
    ```