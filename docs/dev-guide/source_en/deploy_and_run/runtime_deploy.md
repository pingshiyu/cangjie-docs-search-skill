# Deploying the Cangjie Runtime

To ensure the Cangjie executable can run properly across different operating system environments, the Cangjie language provides a runtime environment. This runtime environment grants Cangjie executables access to memory and other system resources, such as the dynamic libraries required during execution.

Installing the complete Cangjie toolchain includes both the Cangjie code compilation environment and the runtime installation (see the [Installing the Cangjie Toolchain](../first_understanding/install.md) section for details). If code compilation is not required and only the execution of binaries is needed, the runtime can be deployed independently in the environment.

This section describes the deployment of the Cangjie runtime.

**Important Note**: When compiling with [fully static linking](../Appendix/compile_options.md#static) of Cangjie libraries, the runtime modules are already embedded in the executable during compilation. Therefore, no additional runtime deployment is needed in the execution environment, and the compiled executable can be run directly.

## Linux

1. First, visit the official Cangjie distribution channels to download the installation package compatible with your platform architecture:

    - `cangjie-sdk-linux-x64-x.y.z.tar.gz`: For x86_64 architecture Linux systems.
    - `cangjie-sdk-linux-aarch64-x.y.z.tar.gz`: For aarch64 architecture Linux systems.

2. Extract the downloaded package to an appropriate directory.

    After extraction, you will find a directory named `cangjie` in your current working path, containing all components of the Cangjie toolchain.

    The `runtime` directory under `cangjie` contains all dynamic libraries for the Cangjie runtime.

3. Execute the following command in the runtime environment to complete the runtime deployment (replace `${CANGJIE_HOME}` with the path to the `cangjie` directory and `${hw_arch}` with the corresponding hardware architecture):

    ```bash
    export LD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/linux_${hw_arch}_cjnative:${LD_LIBRARY_PATH}
    ```

## macOS

1. First, visit the official Cangjie distribution channels to download the installation package compatible with your platform architecture:

    - `cangjie-sdk-mac-x64-x.y.z.tar.gz`: For x86_64 architecture macOS systems.
    - `cangjie-sdk-mac-aarch64-x.y.z.tar.gz`: For aarch64/arm64 architecture macOS systems.

2. Extract the downloaded package to an appropriate directory.

    After extraction, you will find a directory named `cangjie` in your current working path, containing all components of the Cangjie toolchain.

    The `runtime` directory under `cangjie` contains all dynamic libraries for the Cangjie runtime.

3. Execute the following command in the runtime environment to complete the runtime deployment (replace `${CANGJIE_HOME}` with the path to the `cangjie` directory and `${hw_arch}` with the corresponding hardware architecture):

    ```bash
    export DYLD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/darwin_${hw_arch}_cjnative:${DYLD_LIBRARY_PATH}
    ```

## Windows

1. First, visit the official Cangjie distribution channels to download the installation package compatible with your platform architecture:

    - `cangjie-sdk-windows-x64-x.y.z.zip`: For x86_64 architecture Windows systems.

2. Extract the downloaded package to an appropriate directory.

    After extraction, you will find a directory named `cangjie` in your current working path, containing all components of the Cangjie toolchain.

    The `runtime` directory under `cangjie` contains all dynamic libraries for the Cangjie runtime.

3. Developers can choose one of the following methods to deploy the runtime based on their environment and preferences (replace `${CANGJIE_HOME}` with the path to the `cangjie` directory and `${hw_arch}` with the corresponding hardware architecture):

    - For Windows Command Prompt (CMD) environments, execute:

        ```bash
        set "PATH=${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;%PATH%;"
        ```

    - For PowerShell environments, execute:

        ```bash
        $env:PATH = "${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;" + $env:Path
        ```

    - For MSYS shell, bash, or similar environments, execute:

        ```bash
        export PATH=${CANGJIE_HOME}/runtime/lib/windows_x86_64_cjnative
        ```