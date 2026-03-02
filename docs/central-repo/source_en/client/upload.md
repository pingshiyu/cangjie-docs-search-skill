# Artifact Package Publishing

`cjpm` can package developed source code modules and publish them to the central repository. Before publishing, users must configure a token for user authentication.

## Central Repository Related Configuration Items

The fields in `cjpm.toml` related to artifact package creation and publishing are as follows:

| Field Name | Field Description | Required |
| :--- | :--- | :--- |
| `cjc-version` | Minimum Cangjie SDK version | Yes |
| `name` | Module name, consistent with the `root` package name within the module | Yes |
| `organization` | Organization name; empty indicates a module without an organization | No |
| `description` | Description | Required only for bundling |
| `version` | Module version information | Yes |
| `output-type` | Build output type; values: static library/dynamic library/executable (static/dynamic/executable) | Yes |
| `authors` | List of author IDs | No |
| `repository` | URL of the artifact source code repository | No |
| `homepage` | URL of the artifact homepage | No |
| `documentation` | URL of the artifact documentation page | No |
| `tag` | Artifact tags | No |
| `category` | Officially provided artifact categories; see the relevant section of the cjpm documentation for the value range | No |
| `license` | List of licenses | No |
| `include` | Specifies the bundling scope | No |
| `exclude` | Specifies the bundling exclusion scope | No |
| `dependencies` | Project dependencies; format: `aoo = "1.0.0"` or `"org::boo" = { version = "2.0.0" }` | No |
| `test-dependencies` | Test dependencies; same format as `dependencies` | No |
| `script-dependencies` | Script dependencies; same format as `dependencies` | No |

The following is a concrete example of a `cjpm.toml`:

```toml
[package]
  cjc-version = "1.0.0"
  name = "demo"
  organization = "cangjie"
  description = "demo of cangjie central repository"
  version = "1.0.0"
  output-type = "executable"
  authors = ["Tom", "Joan"]
  repository = "https://cangjie-demo.git"
  homepage = "https://cangjie-demo.com"
  documentation = "https://cangjie-demo.com/docs"
  tag = ["cangjie", "demo"]
  category = ["Network", "UI"]
  license = ["Apache-2.0"]
  include = ["src"]
  exclude = ["*.txt"]

[dependencies]
  aoo = "1.0.0"

[test-dependencies]
  boo = "2.0.0"

[script-dependencies]
  "org::coo" = "3.0.0"
```

## Artifact Package Bundling

`cjpm` provides the `bundle` command to package locally developed source code modules into artifact packages conforming to the central repository artifact package format for subsequent upload operations.

The bundling scope of `bundle` is determined by the `include` and `exclude` fields in `cjpm.toml`. Both `include` and `exclude` are in the form of string arrays, where each string represents a matching rule. The matching rule format conforms to the `gitignore` ignore pattern.

The `bundle` command only checks and bundles files under the current project directory. Based on the developer-configured `include` and `exclude` fields, the final bundling scope determination rules for the `bundle` command are as follows:

*   **Files packaged by default, regardless of configuration**: `cjpm.toml`, `README.md`, and `README_zh.md` in the project root directory.
*   **Files not packaged by default, regardless of configuration**:
    *   `cjpm.lock` and `cangjie-repo.toml` in the project root directory.
    *   Build output directories and build script output directories.
    *   All binary files.
*   For other files besides the above ranges, the following rules apply:
    *   If a file matches any `include` rule and does not match any `exclude` rule, it will be packaged.
    *   If `include` is not configured, all files in the current directory that do not match any `exclude` rule will be packaged.

For example, consider the following module `demo` to be packaged:

```text
demo
├── src
│    ├── demo.cj
│    ├── demo-config.txt
│    └── aoo
│         ├── aoo.cj
│         └── aoo-config.txt
├── test
│    ├── test.cj
│    └── test-config.txt
├── README.md
└── cjpm.toml
```

Based on different configurations, examples of the bundling scope are as follows:

**Example 1:**

```toml
[package]
  include = []
  exclude = []
```

Result: Packages all files listed above.

**Example 2:**

```toml
[package]
  include = ["src"]
  exclude = []
```

Result: Packages `cjpm.toml`, `README.md`, and the `src` directory.

**Example 3:**

```toml
[package]
  include = []
  exclude = ["*.txt"]
```

Result: Excludes all `.txt` files and packages the remaining files.

**Example 4:**

```toml
[package]
  include = ["src"]
  exclude = ["*.txt"]
```

Result: Packages `cjpm.toml`, `README.md`, and all files in the `src` directory except `.txt` files.

The `bundle` packaging process is as follows:

1.  **Module Check**

    A `cjpm` module that can be successfully packaged must meet the following conditions:

    *   Module name and organization name meet the specification requirements:
        *   Length range [3, 64], and conforms to the module and organization name specifications.
        *   Cannot be any keyword from the Cangjie syntax (case-insensitive).
        *   Organization name cannot be `default`.
    *   `cjpm.toml` contains the module description `description`.
    *   The root directory contains Chinese documentation `README_zh.md` or English documentation `README.md`.
    *   The module's dependencies are all in central repository form.

    If the module does not meet the above conditions, packaging fails.

2.  **Compilation Check**: Performs a compilation check to ensure the module can compile successfully. If `--skip-test` is not configured, unit tests will be run. Compilation or test failures will cause packaging to fail.
3.  **Code Static Analysis**: If `--skip-lint` is not configured, `cjlint` is called for code static analysis. Errors at the `error` level will cause packaging to fail.
4.  **Bundling**: Based on the `include` and `exclude` fields, packages the current module into an artifact source code package in `tar.gz` format. The artifact source code package is located in the build output directory, with the filename `module-name-version.cjp`. Simultaneously, generates the corresponding metadata file for the artifact package, also located in the build output directory, with the filename `meta-data.json`.

Continuing with the example of the `demo` module to be packaged above, assuming its `cjpm.toml` configures `version = "1.0.0"`. Since the build output directory is not configured, the default build output directory is `target`. After executing `cjpm bundle`, the `target` directory will contain the following:

```text
target
├── demo-1.0.0.cjp  # Artifact source code package
├── meta-data.json  # Artifact metadata
└── other build outputs
```

`demo-1.0.0.cjp` can be extracted in `tar.gz` format.

> **Note:**
>
> The metadata file records key information about the local module for artifact information display on the central repository website. Please refer to [Central Repository Metadata Specification](../appendix/meta_data.md) for more information.

## Artifact Package Publishing

`cjpm` provides the `publish` command for publishing the artifact source code package generated by the `bundle` command to the central repository.

When executing the `publish` command, `cjpm` checks if there is an artifact source code package named `module-name-version.cjp` and a metadata file `meta-data.json` in the build output directory. If either file does not exist, or if the artifact package checksum in the metadata does not match the artifact package, the default `bundle` process is re-executed. Subsequently, `cjpm` publishes the valid artifact source code package and metadata to the central repository.

Successful `publish` requires meeting the following conditions:

1.  A valid user token has been configured in `cangjie-repo.toml`.
2.  The uploaded artifact package is unique, meaning there is no other artifact package in the repository with the same organization name, artifact name, and version number as the newly uploaded one.
3.  If the artifact package belongs to an organization, the user corresponding to the token must be a member of that organization.
4.  The published artifact package passes the central repository's security scan.