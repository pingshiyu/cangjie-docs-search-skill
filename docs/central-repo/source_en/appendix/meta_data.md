# Central Repository Metadata Specification

The `cjpm bundle` command generates metadata and an index entry for the module to be packaged.

The metadata records key information about the module to be packaged, used for repository-side storage checks and website-side artifact display. The metadata specification is as follows:

```json
{
  "organization": "cangjie", // Organization name. Empty means no organization.
  "name": "demo", // Module name
  "version": "1.0.0", // Version number
  "cjc-version": "1.0.0", // Cangjie SDK version number
  "description": "demo for cangjie central repository", // Module description
  "artifact-type": "src", // Artifact package type, fixed as source code package 'src'
  "executable": true, // Whether it can be compiled into an executable program. This value is true when package.output-type == executable in cjpm.toml, otherwise false.
  "authors": ["Tom", "Joan"], // List of author IDs
  "repository": "https://github.com/xxx", // Artifact source code repository
  "homepage": "https://xxx.com", // Artifact homepage
  "documentation": "https://xxx.com/docs", // Artifact documentation page
  "tag": ["cangjie", "cjpm"], // Artifact tags
  "category": ["Network"], // Artifact categories
  "license": ["Apache-2.0"], // List of licenses
  "index": { ... }, // Artifact package index
  "meta-version": 1 // Metadata specification version number
}
```

Among these, the artifact package index records the dependency information of the artifact package, which `cjpm` can use for dependency resolution. The artifact package index specification is as follows:

```json
{
  "organization": "cangjie", // Organization name. Empty means no organization.
  "name": "demo", // Module name
  "version": "1.0.0", // Version number
  "cjc-version": "1.0.0", // Cangjie SDK version number
  "dependencies": [{ // Source code dependencies
    "name": "dep1", // Dependency module name
    "require": "1.1.0", // Dependency version requirement
    "target": null, // Platform isolation identifier. target == null indicates the dependency is not platform-specific.
    "type": null, // Build mode identifier. type == null indicates the dependency does not distinguish build modes.
    "output-type": null // Build output type identifier. output-type == null indicates the dependency's build output follows the package.output-type value in the corresponding source module.
  }, {
    "name": "org::dep2", // Dependency module name within an organization
    "require": "[1.0.0, 2.0.0)", // Dependency version requirement
    "target": "x86_64-unknown-linux-gnu", // Platform isolation identifier. A non-null target indicates the dependency is only applicable to the specified platform.
    "type": "debug", // Build mode identifier. type == debug/release indicates the dependency is only applicable to debug(-g) / non-debug build modes.
    "output-type": "static" // Build output type identifier. output-type == static/dynamic indicates the corresponding module for this dependency will be compiled as a static / dynamic library.
  }],
  "test-dependencies": [], // Test dependencies, same format as source code dependencies
  "script-dependencies": [], // Build script dependencies, same format as source code dependencies
  "sha256sum": "...", // SHA-256 checksum of the corresponding artifact package, used to verify artifact package integrity
  "yanked": false, // Artifact package deprecation flag. yanked == true indicates the artifact package is deprecated.
  "index-version": 1 // Index specification version number
}
```