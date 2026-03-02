# HLE Tool User Guide

## Introduction

`HLE (HyperlangExtension)` is a tool for automatically generating interoperability code templates for Cangjie calling ArkTS or C language.
The input of this tool is the interface declaration file of ArkTS or C language, such as files ending with .d.ts, .d.ets or .h, and the output is a cj file, which stores the generated interoperability code. If the generated code is a glue layer code from ArkTS to Cangjie, the tool will also output a json file containing all the information of the ArkTS file. For the conversion rules from ArkTS to Cangjie, please refer to: [ArkTS Third-Party Module Generation Cangjie Glue Code Rules](cj-dts2cj-translation-rules.md). For the conversion rules from C language to Cangjie, please refer to: [C Language Conversion to Cangjie Glue Code Rules](cj-c2cj-translation-rules.md).

## Instructions

### Dependencies

1. This tool requires Node.js for execution:

    Recommended version: v18.14.1 or higher. Lower versions may fail to parse certain ArkTS syntax, so using the latest version is advised.

    [How to Install Node.js](https://dev.nodejs.cn/learn/how-to-install-nodejs/)

    For example, use the following commands:

    ```sh
    # Download and install nvm:
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    # in lieu of restarting the shell
    \. "$HOME/.nvm/nvm.sh"
    # Download and install Node.js:
    nvm install 22
    # Verify the Node.js version:
    node -v # Should print "v22.17.1".
    nvm current # Should print "v22.17.1".
    # Verify npm version:
    npm -v # Should print "10.9.2".
    ```

2. This tool requires TypeScript and cjbind for execution:

    After installing Node.js, use the following commands to install TypeScript and cjbind:

    ```sh
    cd ${CANGJIE_HOME}/tools/dtsparser/
    npm install
    ```

### Parameter Meaning

| Parameter           | Meaning                                       | Parameter Type | Description                  |
| ------------------- | --------------------------------------------- | -------------- | ---------------------------- |
| `-i`                | Absolute path of d.ts, d.ets or .h file input | Optional       | Choose one from `-d` or both |
| `-r`                | Absolute path of typescript compiler          | Required       | Used only when generating ArkTS Cangjie bindings |
| `-d`                | Absolute path of the folder where d.ts, d.ets or .h file input is located | Optional       | Choose one from `-i` or both |
| `-o`                | Directory to save the output interoperability code | Optional       | Output to the current directory by default |
| `-j`                | Path to analyze d.t or d.ets files            | Optional       | Used only when generating ArkTS Cangjie bindings |
| `--module-name`     | Custom generated Cangjie package name         | Optional       | NA |
| `--lib`             | Generate third-party library code             | Optional       | Used only when generating ArkTS Cangjie bindings |
| `-c`                | Generate C to Cangjie binding code             | Optional       | Used only when generating C language Cangjie bindings |
| `-b`                | Specify the path of the cjbind binary             | Optional       | Used only when generating C language Cangjie bindings |
| `--clang-args`      | Parameters that will be directly passed to clang | Optional       | Used only when generating C language Cangjie bindings |
| `--no-detect-include-path` | Disable automatic include path detection    | Optional       | Used only when generating C language Cangjie bindings |
| `--help`            | Help option                                   | Optional       | NA |

### Command Line

You can use the following command to generate ArkTS to Cangjie binding code:

```sh
hle -i /path/to/test.d.ts -o out –j ${CANGJIE_HOME}/tools/dtsparser/analysis.js --module-name="my_module"
```

In the Windows environment, the file directory currently does not support the symbol "\\", only "/" is supported.

The command to generate C to Cangjie binding code is as follows:

```sh
hle -b ${CANGJIE_HOME}/tools/dtsparser/node_modules/.bin/cjbind -c --module-name="my_module" -d ./tests/c_cases -o ./tests/expected/c_module/ --clang-args="-I/usr/lib/llvm-20/lib/clang/20/include/"
```

The `-b` parameter is used to specify the path to the cjbind binary file. The cjbind download link is as follows:

- Linux: <https://gitcode.com/Cangjie-SIG/cjbind-cangjie/releases/download/v0.2.7/cjbind-linux-x64>
- Windows: <https://gitcode.com/Cangjie-SIG/cjbind-cangjie/releases/download/v0.2.7/cjbind-windows-x64.exe>
- macOS: <https://gitcode.com/Cangjie-SIG/cjbind-cangjie/releases/download/v0.2.7/cjbind-darwin-arm64>

The `--clang-args` parameter is directly passed to clang, and the -I option can be used within its value to specify header file search paths. System header file paths are searched automatically by the program, while user-defined header file paths need to be explicitly specified.