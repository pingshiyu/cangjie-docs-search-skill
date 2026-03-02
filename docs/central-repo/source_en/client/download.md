# Artifact Package Usage

After correctly configuring the central repository address, artifact packages can be fetched from and used from the central repository.

## Central Repository Dependencies

Artifact packages in the central repository correspond to `cjpm` modules and can therefore be imported as dependencies by locally developed `cjpm` modules.

The format for `cjpm` central repository dependencies is as follows:

```toml
[dependencies]
  dep1 = "1.0.0"                # Depends on artifact dep1 with version 1.0.0
  dep2 = { version = "2.0.0" }  # Depends on artifact dep2 with version 2.0.0. This notation is equivalent to dep2 = "2.0.0"
  dep3 = "[1.0.0, 3.0.0)"       # Depends on any version of artifact dep3 with a version number greater than or equal to 1.0.0 and less than 3.0.0
  "org::dep4" = "4.0.0"         # Depends on artifact dep4 with version 4.0.0, which belongs to the organization org
```

The configuration method is explained in detail as follows:

*   The central repository dependency configuration format is `${artifact-name} = "${version-requirement}"` or `${artifact-name} = { version = "${version-requirement}" }`. These two notations are equivalent.
*   When depending on an artifact within an organization, the organization name must be prepended to the artifact name, separated by `::`. Due to `toml` format requirements, it must be enclosed in `""`. For example, `"org::dep4" = "4.0.0"` in the example above.
*   The version requirement supports the following formats:
    *   **Single Version Number**: Indicates dependency on a specific version of the artifact package. For example, `dep1 = "1.0.0"` in the example above.
    *   **Version Range**: A version range expressed as a mathematical interval, with customizable open/closed bounds, indicating dependency on any artifact package version within the range. For example, `dep3 = "[1.0.0, 3.0.0)"` in the example above indicates dependency on any `dep3` artifact package with a version number greater than or equal to `1.0.0` and less than `3.0.0`.
        *   **Unbounded Version Range**: The upper or lower bound of the version range can be omitted, indicating no upper/lower bound. The omitted side must be an open interval. For example, `(, 2.0.0]` indicates any version less than or equal to `2.0.0`; `(1.0.0, )` indicates any version greater than `1.0.0`; `(, )` indicates any version.
    *   **Multi-interval Combination**: A combination of any number of single version numbers or version ranges, separated by commas. It indicates the artifact package version satisfies any one of the single version numbers or version ranges. For example, `(, 1.0.0), [2.0.0, 3.0.0), 4.0.0` indicates the dependent artifact package version is less than `1.0.0`, OR greater than or equal to `2.0.0` and less than `3.0.0`, OR version `4.0.0`.

> **Note:**
>
> Artifact version numbers are compared sequentially based on major, minor, and patch version priority to determine their order. Once the order is determined by a higher priority level, lower priority levels are ignored. For example: `1.2.3 < 1.4.5`, `3.4.5 > 2.40.50`.

## Dependencies for Different Scenarios

`cjpm` provides three configuration methods for source code dependency modules in the project configuration file `cjpm.toml`, all adhering to the format described above, each corresponding to different application scenarios:

*   **Project Dependencies (`dependencies`)**: Used to provide source code dependency modules for project files (except for the build script `build.cj`).
*   **Test Dependencies (`test-dependencies`)**: Used to provide source code dependency modules for the project's test code. Test code filenames must end with `_test.cj`. Test dependencies only take effect during testing.
*   **Script Dependencies (`script-dependencies`)**: Used to provide source code dependency modules for the project's build script. The build script is a file named `build.cj` located at the same level as `cjpm.toml`. Script dependencies only take effect for the build script.

> **Note:**
>
> *   Project source code dependencies (`dependencies`) can also be used in the project's test code.
> *   The build script is independent of the project source code. Therefore, the build script can only use dependencies from `script-dependencies` and cannot use the other two types of dependencies. Conversely, the project's source code and test code cannot use dependencies from `script-dependencies`.

For example, consider a local module `demo` with the following structure:

```text
demo
├── src
│    ├── demo.cj
│    └── demo_test.cj
├── build.cj
└── cjpm.toml
```

Module `demo` is configured with the following dependencies:

```toml
# demo/cjpm.toml
[package]
  name = "demo"

[dependencies]
  dep1 = "1.0.0"

[test-dependencies]
  "org::dep2" = "2.0.0"

[script-dependencies]
  dep3 = "3.0.0"
```

Then, in different source files of `demo`, corresponding packages from the central repository modules can be imported:

```cangjie
// src/demo.cj
package demo
import dep1.aoo.*         // Source files can import packages from module dep1

// src/demo_test.cj
package demo
import dep1.aoo.*         // Test files can import packages from module dep1
import org::dep2.boo.*    // Test files can import packages from module org::dep2

// build.cj
import dep3.coo.*         // Build scripts can import packages from module dep3
```

## Platform-Specific Dependencies

`cjpm` supports using the `target` field to isolate dependency configurations for different platforms and build modes, for example:

```toml
# demo/cjpm.toml
[target.x86_64-unknown-linux-gnu.debug.dependencies]
  dep1 = "1.0.0"  # When compiling on linux-x64 platform in debug(-g) mode, depend on version 1.0.0 of dep1

[target.x86_64-unknown-linux-gnu.release.dependencies]
  dep1 = "2.0.0"  # When compiling on linux-x64 platform in non-debug mode, depend on version 2.0.0 of dep1

[target.x86_64-w64-mingw32.dependencies]
  dep1 = "3.0.0" # When compiling on windows-x64 platform (regardless of debug), depend on version 3.0.0 of dep1
```

> **Note:**
>
> *   The platform name specified by `target` can be obtained on the corresponding platform via the command `cjc -v`.
> *   If a dependency specified in `target` conflicts with a non-platform-specific dependency of the same type, `cjpm` will report an error.

## Dependency Conflict Resolution

During the use of central repository artifacts, dependency conflicts may occur. They can be attempted to be resolved in the following ways:

*   Depend on other central repository modules with similar functionality to avoid dependency conflicts.
*   Adjust the version range of the dependency to include more available versions, thereby increasing the possibility of finding a compatible version.
*   If the compilation process involves multiple local modules, check if there are dependency conflicts between these modules.
*   Use the `cjpm update` command to update the local index cache to obtain the latest artifact information from the central repository.

When an unavoidable version conflict occurs, `cjpm` dependency resolution will fail. For example, consider a local project with the following structure:

```text
demo
├── pro1
│    ├── src
│    │    └── pro1.cj
│    └── cjpm.toml
├── pro2
│    ├── src
│    │    └── pro2.cj
│    └── cjpm.toml
├── src
│    └── demo.cj
└── cjpm.toml
```

The configurations of the three modules are as follows:

```toml
# demo/cjpm.toml
[dependencies]
  pro1 = { path = "./pro1" }
  pro2 = { path = "./pro2" }

# demo/pro1/cjpm.toml
[dependencies]
  dep1 = "1.0.0"

# demo/pro2/cjpm.toml
[dependencies]
  dep1 = "2.0.0"
```

Module `demo` depends on local modules `pro1` and `pro2`, but these two local modules have conflicting version requirements for the central repository module `dep1`. `cjpm` will fail to compile `demo` due to the dependency conflict.

To address this situation, `cjpm` provides the `replace` field to forcibly specify dependencies. Its format is the same as `dependencies`, but when forcibly specifying central repository dependencies, only a single version number can be specified. For example, configure the `demo` module as follows:

```toml
# demo/cjpm.toml
[dependencies]
  pro1 = { path = "./pro1" }
  pro2 = { path = "./pro2" }

[replace]
  dep1 = "3.0.0"
```

With the above configuration, even though `pro1` and `pro2` depend on versions `1.0.0` and `2.0.0` of `dep1` respectively, due to the `replace` configuration, both will ultimately be forced to depend on version `3.0.0` of `dep1`.

## Installing Central Repository Executables

Central repository modules whose build output type is not `executable` can only be added as dependencies. However, central repository modules whose build output type is `executable` can also be compiled into executable programs and installed locally via the `cjpm install` command. On the artifact page of the central repository website, you can confirm whether an artifact package can be installed via the `install` command by checking for the presence of an `install` description:

![artifact-usage](../../figures/artifact-usage.png)

The above artifact package can be installed locally using the following command:

```text
cjpm install cangjie_repository_artifact-1.0.0
```

Based on the local cache path `CACHE_PATH` configured in [Repository Configuration](./config.md#repository-configuration), the local installation directory is:

```text
${CACHE_PATH}
├── bin               # Installed executable files
│    └── cangjie_repository_artifact
└── libs              # Dynamic libraries required by the executable files, stored in directories named after the corresponding executable file
     └── cangjie_repository_artifact
          └── ...
```

After installation, you can directly use `cangjie_repository_artifact` from the command line. If the executable file requires dynamic libraries, the corresponding path must be added to the system's dynamic library environment variable before use.