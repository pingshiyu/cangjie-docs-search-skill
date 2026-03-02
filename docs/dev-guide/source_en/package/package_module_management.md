# Package and Module Management

In the Cangjie programming language, a package consists of one or more source code files. All source files within the same package must reside in the same directory, and all source files in the same directory can only belong to one package. Packages can define subpackages to form a tree structure. The directory of a subpackage is a subdirectory of its parent package's directory. A package without a parent is called a root package. The entire tree structure formed by a root package and its subpackages (including subpackages of subpackages) is called a module.

The typical organizational structure of a Cangjie program is as follows:

```text
demo
├── src
│    ├── main.cj
│    └── pkg0
│         ├── pkg0.cj
│         ├── aoo
│         │    └── aoo.cj
│         └── boo
│              └── boo.cj
└── cjpm.toml
```

`cjpm.toml` is the configuration file for the workspace where the current module resides. It defines basic information, dependencies, compilation options, and other settings. This file is parsed and executed by Cangjie's official package management tool `cjpm`.

> **Note:**
>
> For the same module, if you need to configure a valid package for it, the package's directory must directly contain at least one Cangjie source code file, and all its parent directories must be valid packages.
