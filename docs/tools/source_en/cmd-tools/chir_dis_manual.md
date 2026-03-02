# CHIR Deserialization Tool

## Overview

`chir-dis` is a CHIR deserialization tool provided by Cangjie, designed to deserialize compiler-output CHIR serialized information into human-readable text files for storage.

## Usage Instructions

Run `chir-dis -h` to view command usage:

```text
A tool used to deserialize and dump CHIR.

Overview: chir-dis xxx.chir -> xxx.chirtxt

Usage:
  chir-dis [option] file

Options:
  -v                      print compiler version information.
  -h                      print this help.
```

Developers can use this tool to deserialize a single CHIR serialized file and save it in the current directory with a `.chirtxt` extension. The `-v` option allows viewing the corresponding compiler version.

## Usage Example

To deserialize the compiler-output CHIR serialized file `package.chir` into a readable text file for inspection, execute the following command:

```shell
chir-dis package.chir
```

After running the above command, a text file named `package.chirtxt` will be generated in the current directory.