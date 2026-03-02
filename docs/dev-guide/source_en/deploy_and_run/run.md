# Running the Cangjie Executable

## Direct Execution

### Linux / macOS

1. First, please refer to the [Deploying Cangjie Runtime](./runtime_deploy.md) section to complete the runtime library deployment.

2. Copy the compiled executable file `main` to the target environment and execute it.

    ```bash
    ./main
    ```

    **Note:** The executable `main` compiled using `cjpm` is located in the `target/release/bin` directory.

### Windows

1. First, please refer to the [Deploying Cangjie Runtime](./runtime_deploy.md) section to complete the runtime library deployment.

2. Copy the compiled executable file `main.exe` to the target environment and execute it.

    ```bash
    .\main.exe
    ```

    **Note:** The executable `main.exe` compiled using `cjpm` is located in the `target\release\bin` directory.

## Using cjpm to Run

Developers commonly use `cjpm` to manage, compile, and run Cangjie projects.

Developers can install the complete Cangjie toolchain on the target environment by following the [Installing Cangjie Toolchain](../first_understanding/install.md) section. After installation, copy the entire Cangjie project to the target environment and use the `cjpm run` command to execute the project.