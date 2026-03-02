# Overview of Network Programming

Network communication is the process of data exchange between two devices through a computer network. The act of achieving network communication through software development is referred to as network programming.

Cangjie provides developers with fundamental network programming capabilities. Within the Cangjie standard library, developers can utilize the `socket` package under the `std` module to implement transport-layer network communication.

In transport-layer protocols, there are two categories: unreliable transmission and reliable transmission. Cangjie abstracts these as `DatagramSocket` and `StreamSocket`, respectively. Among unreliable transmission protocols, UDP is the most common, while TCP is the predominant reliable transmission protocol. Cangjie abstracts these as `UdpSocket` and `TcpSocket`, respectively. Additionally, Cangjie implements support for the Unix Domain protocol at the transport layer, enabling communication through both reliable and unreliable transmission methods.

At the application layer, the HTTP protocol is widely used, particularly in developing web applications. Currently, there are multiple versions of the HTTP protocol, and Cangjie currently supports HTTP/1.0, HTTP/1.1, and HTTP/2.0.

Furthermore, WebSocket, as an application-layer protocol designed to enhance communication efficiency between web servers and clients, is abstracted by Cangjie as the `WebSocket` object. Cangjie also supports protocol upgrades from HTTP to WebSocket.

It is important to note that network programming in Cangjie is blocking. However, it is the Cangjie thread that gets blocked, and a blocked Cangjie thread yields the system thread, thus not truly blocking a system thread.