# Central Repository Client Configuration

The Cangjie Project Manager `cjpm` integrates the central repository client functionality, therefore requiring the local installation of the Cangjie `SDK` and configuration related to the central repository.

## Install Cangjie Toolchain

Please refer to the [Cangjie SDK Installation Guide](https://gitcode.com/Cangjie/cangjie_docs/blob/dev/docs/dev-guide/source_en/first_understanding/install.md) to install and verify your local Cangjie environment.

## Repository Configuration

`cjpm` performs central repository-related configuration through the configuration file `cangjie-repo.toml`, which has the following format:

```toml
[repository.cache]
  path = "/path/to/repository/cache"              # Local storage path

[repository.home]
  registry = "https://pkg.cangjie-lang.cn/cjpm"   # Central repository URL
  token = "user-token"                            # User personal token
```

The meanings of each configuration field are as follows:

*   **`repository.cache.path`**: Configures the local cache path for storing artifact package source code downloaded from the central repository.
    *   The configured path can be an absolute or relative path. If it's a relative path, it is relative to the current `cangjie-repo.toml` file.
    *   If the configuration item is empty, the effective path on `Linux/macOS` will be `$HOME/.cjpm`, and on `Windows` it will be `%USERPROFILE%\.cjpm`.
    *   Assuming the final effective path is `CACHE_PATH`, the artifact package source code and other central repository-related content downloaded from the central repository will be stored in the `${CACHE_PATH}/repository` directory.
*   **`repository.home.registry`**: Configures the central repository storage address (https://pkg.cangjie-lang.cn/cjpm), used for upload/download communication with the central repository.
*   **`repository.home.token`**: Configures the user personal token, used for user authentication when uploading artifact packages.

Users can configure `cangjie-repo.toml` in the following three locations. After a user executes a `cjpm` related command, `cjpm` will search for the presence of `cangjie-repo.toml` in the corresponding locations in the following order until found:

1.  `cangjie-repo.toml` in the same directory as `cjpm.toml` within the module.
2.  `cangjie-repo.toml` inside the `.cjpm` directory under the user's home directory: `$HOME/.cjpm/cangjie-repo.toml` on `Linux/macOS`, and `%USERPROFILE%\.cjpm\cangjie-repo.toml` on `Windows`.
3.  `cangjie-repo.toml` in the `tools/config` directory of the Cangjie `SDK`. This file exists by default in the Cangjie `SDK` with all configurations set to default values.