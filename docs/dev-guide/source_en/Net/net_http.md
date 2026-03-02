# HTTP Programming

HTTP, as a universal application-layer protocol, facilitates data transmission through a request-response mechanism where the client sends requests and the server returns responses. The format of requests and responses is fixed, consisting of a header and a body.

The most commonly used request types are GET and POST. A GET request contains only a header and is used to request application-layer data from the server. A POST request includes a body, separated from the header by an empty line, and is used to provide application-layer data to the server.

The header fields of request-response messages are numerous and will not be exhaustively detailed here. Cangjie supports HTTP protocol versions 1.0/1.1/2.0, among others. Developers can construct request and response messages based on RFCs 9110, 9112, 9113, 9218, 7541, and the `HttpRequestBuilder` and `HttpResponseBuilder` classes provided by Cangjie.

The following example demonstrates how to use Cangjie for client and server programming. The functionality implemented involves the client sending a request with the header `GET /hello`, and the server returning a response with the body `"Hello Cangjie!"`. The code is as follows:

> **Note:**
>
> Libraries such as `net` and `log` have been moved from the Cangjie SDK to the `stdx` module. Before use, download the software package and configure it in `cjpm.toml`.

<!-- verify -->

```cangjie
import stdx.net.http.*
import std.time.*
import std.sync.*
import stdx.log.*

// 1. Build a Server instance
let server = ServerBuilder()
    .addr("127.0.0.1")
    .port(0)
    .build()

func startServer(): Unit {
    // 2. Register request handling logic
    server.distributor.register("/hello", {httpContext =>
        httpContext.responseBuilder.body("Hello Cangjie!")
    })
    server.logger.level = LogLevel.OFF
    // 3. Start the service
    server.serve()
}

func startClient(): Unit {
    // 1. Build a client instance
    let client = ClientBuilder().build()
    // 2. Send a request
    let response = client.get("http://127.0.0.1:${server.port}/hello")
    // 3. Read the response body
    let buffer = Array<Byte>(32, repeat: 0)
    let length = response.body.read(buffer)
    println(String.fromUtf8(buffer[..length]))
    // 4. Close the connection
    client.close()
}

main () {
    spawn {
        startServer()
    }
    sleep(Duration.second)
    startClient()
}
```

Compiling and executing the above code will print:

```text
Hello Cangjie!
```