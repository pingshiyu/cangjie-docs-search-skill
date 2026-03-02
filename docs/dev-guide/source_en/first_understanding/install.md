# Installing the Cangjie Toolchain

When developing Cangjie programs, one essential tool is the Cangjie compiler, which can compile Cangjie source code into executable binary files. However, modern programming languages come with more than just compilers. In fact, Cangjie provides developers with a comprehensive suite of development tools, including compilers, debuggers, project managers, static analysis tools, formatting tools, and coverage statistics tools, all designed for a seamless "out-of-the-box" experience.

Currently, the Cangjie toolchain has been adapted for certain versions of Linux, macOS, and Windows platforms. However, full functional testing has only been conducted on select Linux distributions. For details, please refer to the appendix section [Support and Installation of Linux Version Toolchain](../Appendix/linux_toolchain_install.md). On platforms that have not undergone full functional testing, the completeness of the Cangjie toolchain's functionality is not guaranteed. Additionally, the current Windows version of the Cangjie compiler is implemented based on MinGW and may lack some features compared to the Linux version.

## Linux / macOS

### Environment Preparation

#### Linux

The system requirements for the Linux version of the Cangjie toolchain are as follows:

| Architecture | Environment Requirements                                     |
| ------------ | ------------------------------------------------------------ |
| x86_64       | glibc 2.27, Linux Kernel 4.15 or later, with libstdc++ 6.0.24 or later installed |
| aarch64      | glibc 2.27, Linux Kernel 4.15 or later, with libstdc++ 6.0.24 or later installed |

For Ubuntu 18.04, additional dependency packages must be installed:

```bash
$ apt-get install binutils libc-dev libc++-dev libgcc-7-dev
```

For dependency installation commands for other Linux distributions, please refer to the appendix section [Support and Installation of Linux Version Toolchain](../Appendix/linux_toolchain_install.md).

Additionally, the Cangjie toolchain depends on the OpenSSL 3 component, which may not be available in the default repositories of the above distributions. Therefore, it must be manually installed. For installation instructions, please refer to the appendix section [Support and Installation of Linux Version Toolchain](../Appendix/linux_toolchain_install.md).

#### macOS

The macOS version of the Cangjie toolchain supports macOS 12.0 and later.

Before using the macOS version, the following dependency package must be installed by executing the following command:

```bash
$ brew install libffi
```

### Installation Guide

First, visit the official Cangjie release channel to download the installation package for your platform's architecture:

- `cangjie-sdk-linux-x64-x.y.z.tar.gz`: For x86_64 architecture Linux systems
- `cangjie-sdk-linux-aarch64-x.y.z.tar.gz`: For aarch64 architecture Linux systems
- `cangjie-sdk-mac-x64-x.y.z.tar.gz`: For x86_64 architecture macOS systems
- `cangjie-sdk-mac-aarch64-x.y.z.tar.gz`: For aarch64/arm64 architecture macOS systems

Assuming you have selected `cangjie-sdk-linux-x64-x.y.z.tar.gz`, after downloading it locally, execute the following command to extract it:

```bash
tar xvf cangjie-sdk-linux-x64-x.y.z.tar.gz
```

After extraction, you will see a directory named `cangjie` in the current working path, which contains all components of the Cangjie toolchain. Execute the following command to complete the installation and configuration:

```bash
source cangjie/envsetup.sh
```

To verify the installation, execute the following command:

```bash
cjc -v
```

Here, `cjc` is the executable filename of the Cangjie compiler. If the command line displays the Cangjie compiler version information, the toolchain has been successfully installed. Note that the `envsetup.sh` script only configures the toolchain-related environment variables for the current shell session. To use the toolchain in a new shell session, you must re-execute the `envsetup.sh` script.

To make the Cangjie toolchain environment variables automatically effective upon shell startup, add the following command to the end of your shell initialization file (e.g., `$HOME/.bashrc` or `$HOME/.zshrc`, depending on your shell type):

```shell
# Assuming the Cangjie package is extracted to /home/user/cangjie
source /home/user/cangjie/envsetup.sh  # The absolute path to envsetup.sh
```

After configuration, the Cangjie compilation toolchain will be directly available upon shell startup.

### Uninstallation and Update

On Linux and macOS platforms, to uninstall the Cangjie toolchain, simply delete the installation directory and remove the environment variables (the simplest way is to open a new shell session):

```bash
$ rm -rf <path>/<to>/cangjie
```

To update the Cangjie toolchain, first uninstall the current version, then follow the above instructions to reinstall the latest version.

## Windows

This section uses Windows 10 as an example to introduce the installation method for the Cangjie toolchain.

### Installation Guide

On Windows, Cangjie provides two formats of installation packages: `exe` and `zip`. Visit the official Cangjie release channel to download the appropriate Windows version for your platform's architecture.

- If you choose the `exe` format installation package (e.g., `cangjie-sdk-windows-x64-x.y.z.exe`), simply execute the file and follow the installation wizard to complete the installation.

- If you choose the `zip` format installation package (e.g., `cangjie-sdk-windows-x64-x.y.z.zip`), extract it to an appropriate directory. The package provides three different installation scripts: `envsetup.bat`, `envsetup.ps1`, and `envsetup.sh`. Choose one based on your usage habits and environment configuration:

    - For Windows Command Prompt (CMD), execute:

        ```bash
        path\to\cangjie\envsetup.bat
        ```

    - For PowerShell, execute:

        ```bash
        . path\to\cangjie\envsetup.ps1
        ```

    - For MSYS shell, bash, etc., execute:

        ```bash
        source path/to/cangjie/envsetup.sh
        ```

To verify the installation, execute `cjc -v` in the same command environment. If the Cangjie compiler version information is displayed, the toolchain has been successfully installed.

**Important Note:**
Similar to Linux, the environment variables configured by the `envsetup` script are only effective for the current command-line session. To make the Cangjie toolchain automatically available upon command prompt or terminal startup, configure the system as follows:

- For bash environments, follow these steps:

    Add the following command to the end of your `$HOME/.bashrc` initialization file (`$HOME` is the path to the current user's directory):

    ```shell
    # Assuming the Cangjie package is extracted to /home/user/cangjie
    source /home/user/cangjie/envsetup.sh  # The absolute path to envsetup.sh
    ```

    After configuration, the Cangjie compilation toolchain will be directly available upon bash startup.

- For Windows Command Prompt (CMD), PowerShell, or other environments, follow these steps:

    1. Search for "View advanced system settings" in the Windows search box and open the corresponding window.

    2. Click the "Environment Variables" button.

    3. Configure the `CANGJIE_HOME` variable as follows:

        1. In the "User variables" (for the current user) or "System variables" (for all users) section, check if the `CANGJIE_HOME` environment variable already exists. If not, click "New" and enter `CANGJIE_HOME` in the "Variable name" field. If it exists, the environment may already be configured for Cangjie. To overwrite the existing configuration, click "Edit" to enter the "Edit System Variable" window.

        2. In the "Variable value" field, enter the extraction path of the Cangjie installation package. If a path already exists, overwrite it with the new path. For example, if the package is extracted to `D:\cangjie`, enter `D:\cangjie`.

        3. After configuration, the "Edit User Variable" or "Edit System Variable" window should display `CANGJIE_HOME` as the variable name and `D:\cangjie` as the variable value. Click "OK" after confirming the path.

    4. Configure the `Path` variable as follows:

        1. In the "User variables" or "System variables" section, locate and select the `Path` variable, then click "Edit" to open the "Edit Environment Variable" window.

        2. Click "New" and enter the following paths one by one:
           `%CANGJIE_HOME%\bin`, `%CANGJIE_HOME%\tools\bin`, `%CANGJIE_HOME%\tools\lib`, `%CANGJIE_HOME%\runtime\lib\windows_x86_64_cjnative` (`%CANGJIE_HOME%` is the extraction path of the Cangjie package). For example, if the package is extracted to `D:\cangjie`, the new environment variables should be:
           `D:\cangjie\bin`, `D:\cangjie\tools\bin`, `D:\cangjie\tools\lib`, `D:\cangjie\runtime\lib\windows_x86_64_cjnative`.

        3. (For current user settings only) Click "New" and enter the current user directory path, appending `.cjpm\bin` to it. For example, if the user path is `C:\Users\bob`, enter `C:\Users\bob\.cjpm\bin`.

        4. After configuration, the "Edit Environment Variable" window should display the paths as follows. Click "OK" after confirming the paths:

           ```text
           D:\cangjie\bin
           D:\cangjie\tools\bin
           D:\cangjie\tools\lib
           D:\cangjie\runtime\lib\windows_x86_64_cjnative
           C:\Users\bob\.cjpm\bin
           ```

    5. Click "OK" to exit the "Environment Variables" window.

    6. Click "OK" to complete the setup.

    > **Note:**
    > After configuration, you may need to restart the command-line window or the system for the changes to take effect.

    After configuration, the Cangjie compilation toolchain will be directly available upon Windows Command Prompt (CMD) or PowerShell startup.

### Uninstallation and Update

- If you installed using the `exe` format package, run the `unins000.exe` executable in the Cangjie installation directory and follow the uninstallation wizard to complete the process.

- If you installed using the `zip` format package, delete the Cangjie toolchain installation directory and remove the above environment variable settings (if any) to complete the uninstallation.

To update the Cangjie toolchain, first uninstall the current version, then follow the above instructions to reinstall the latest version.