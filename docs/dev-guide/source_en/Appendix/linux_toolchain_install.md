# Linux Distribution Support and Installation for the Toolchain

The Cangjie toolchain has undergone comprehensive functional testing on the following Linux distributions:

- Ubuntu 18.04
- Ubuntu 20.04
- UnionTech OS Server 20
- Kylin Linux Advanced Server Release V10

## Dependency Installation Commands for Cangjie Toolchain Across Linux Distributions

> **Note:**
>
> Certain tools required by the current Cangjie toolchain may not be directly installable through default system repositories on some Linux distributions. Please refer to the next section [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for manual installation instructions.

Additionally, OpenSSL 3 needs to be installed. Refer to [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for installation methods.

### Ubuntu 18.04

```shell
$ apt-get install \
          binutils \
          libc-dev \
          libc++-dev \
          libgcc-7-dev
```

Additionally, OpenSSL 3 needs to be installed. Refer to [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for installation methods.

### Ubuntu 20.04

```shell
$ apt-get install \
          binutils \
          libc-dev \
          libc++-dev \
          libgcc-9-dev
```

Additionally, OpenSSL 3 needs to be installed. Refer to [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for installation methods.

### UnionTech OS Server 20

```shell
$ yum install \
      binutils \
      glibc-devel \
      libstdc++-devel \
      gcc \
```

Additionally, OpenSSL 3 needs to be installed. Refer to [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for installation methods.

### Kylin Linux Advanced Server Release V10

```shell
$ yum install \
      binutils \
      glibc-devel \
      libstdc++-devel \
      gcc \
```

Additionally, OpenSSL 3 needs to be installed. Refer to [Compiling and Installing Dependency Tools](./linux_toolchain_install.md#compiling-and-installing-dependency-tools) for installation methods.

### Other Linux Distributions

Depending on the Linux distribution in use, you may need to refer to the dependency installation commands for the above systems and use the system's package manager to install corresponding dependencies. If the system does not provide the required packages, you may need to manually install linkers, C development tools, C++ development tools, GCC compilers, and OpenSSL 3 to use the Cangjie toolchain properly.

## Compiling and Installing Dependency Tools

Some standard libraries (and certain tools) in the current Cangjie toolchain utilize the OpenSSL 3 open-source software. For scenarios where the system package manager does not provide OpenSSL 3, users may need to compile and install OpenSSL 3 from source. This section provides the methods and steps for compiling OpenSSL 3 from source.

### OpenSSL 3

Download the OpenSSL 3 source code from the following links:

- <https://www.openssl.org/source/>
- <https://www.openssl.org/source/old/>

OpenSSL 3.0.7 or later is recommended.

> **Note:**
>
> Please carefully read the following notes before executing the compilation and installation commands, and adjust the commands according to your actual situation. Incorrect configuration and installation may render other system software unusable. If you encounter issues during compilation and installation or wish to perform additional configuration, refer to the `INSTALL` file in the OpenSSL source code or OpenSSL's [FAQ](https://www.openssl.org/docs/faq.html).

Using OpenSSL 3.0.7 as an example, after downloading, extract the archive with the following command:

```shell
$ tar xf openssl-3.0.7.tar.gz
```

After extraction, enter the directory:

```shell
$ cd openssl-3.0.7
```

Compile OpenSSL:

> **Note:**
>
> If OpenSSL is already installed on the system, it is recommended to use the `--prefix=<path>` option to specify a custom installation path, such as `--prefix=/usr/local/openssl-3.0.7` or a developer's personal directory. Directly compiling and installing with the following commands in a system where OpenSSL already exists may overwrite the system OpenSSL, causing applications dependent on it to become unusable.

```shell
$ ./Configure --libdir=lib
$ make
```

Test OpenSSL:

```shell
$ make test
```

Install OpenSSL to the system directory (or the previously specified `--prefix` directory). Root privileges may be required to successfully execute the following command:

```shell
$ make install
```

or

```shell
$ sudo make install
```

If a custom installation path was not specified via `--prefix` during OpenSSL compilation, the installation is now complete. If a custom path was specified via `--prefix`, the following variables must be set to ensure the Cangjie toolchain can locate OpenSSL 3.

> **Note:**
>
> If other versions of OpenSSL exist on the system, configuring these variables may affect the OpenSSL version used by other compilation and development tools besides the Cangjie toolchain. If OpenSSL incompatibility issues arise with other tools, configure these variables only for the Cangjie development environment.

*Replace `<prefix>` with your specified custom installation path.*

```shell
$ export LIBRARY_PATH=<prefix>/lib:$LIBRARY_PATH
$ export LD_LIBRARY_PATH=<prefix>/lib:$LD_LIBRARY_PATH
```

The environment variables configured this way are only effective for the current `shell` session. To automatically configure them every time the `shell` starts, add the above commands to `$HOME/.bashrc`, `$HOME/.zshrc`, or other `shell` configuration files (depending on the developer's `shell` type).

To make the configuration effective for all users by default, execute the following commands:

*Replace `<prefix>` with your specified custom installation path.*

```shell
$ echo "export LIBRARY_PATH=<prefix>/lib:$LIBRARY_PATH" >> /etc/profile
$ echo "<prefix>/lib" >> /etc/ld.so.conf
$ ldconfig
```

After execution, reopen the `shell` session for the changes to take effect.

At this point, OpenSSL 3 has been successfully installed. You may return to the previous section to continue reading or attempt to run the Cangjie compiler.