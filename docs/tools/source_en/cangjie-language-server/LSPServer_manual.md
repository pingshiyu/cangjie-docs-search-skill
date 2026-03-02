# Cangjie Language Server User Guide

## Overview

The `Cangjie Language Server` provides language service features such as definition navigation, reference lookup, and code completion based on the Cangjie language.

## Usage Instructions

The Cangjie Language Server serves as the backend server for providing Cangjie language services in IDEs, requiring integration with an IDE client. Developers can use it with the VSCode plugin released by Cangjie or develop their own IDE clients that comply with the Language Server Protocol (LSP).

The startup parameters for `Cangjie Language Server` are as follows:

```shell
-V                    Optional parameter, enables crash log generation capability for LSPServer  
--enable-log=<value>  Optional parameter, controls whether to enable log printing. If not set, defaults to true (enabling log printing)  
--log-path=<value>    Optional parameter, specifies the directory for generating log files and crash logs. If not set, logs will be generated in the LSPServer's working directory by default  
--disableAutoImport   Optional parameter, disables automatic package import during code completion  
--test                Optional parameter, starts test mode for running LSPServer test cases  
```

## Usage Example

```shell
LSPServer.exe --enable-log=true --log-path=D:/CangjieLSPLog -V --disableAutoImport
```

This command starts LSPServer with logging and crash log generation enabled, sets the log file output directory to `D:/CangjieLSPLog`, and disables automatic package import during code completion.