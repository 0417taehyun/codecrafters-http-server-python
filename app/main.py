import socket


def main():
    server: socket.socket = socket.create_server(address=("localhost", 4221), reuse_port=True)

    
    # Accept a connection. The return value is a pair (conn, address)
    # conn is a new socket object usable to send and receive data on the connection. It is non-inheritable.
    # address is the address bound to the socket on the other end of the connection
    connection, address = server.accept()


    # Receive data from the socket. The return value is a bytes object
    # The maximum amount of data to be received at once is specified by bufsize.
    data: bytes = connection.recv(65536)

    # The return bytes object looks like b"GET / HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: Go-http-client/1.1\r\nAccept-Encoding: gzip\r\n\r\n"
    # \r is a CR(Carriage Return) which means that it moves the cursor to the beginning of the line without advancing to the next line.
    # \n is a LF(Line Feed) which means that it moves the cursor down to the next line without returning to the beginning of the line.
    # Thus, CRLF, \r\n means that it moves the cursor down to the next line and then to the beginning of the line.
    print(data)

    # HTTP Response has three parts, Status Line, Headers, and Body.
    # Two CRLF, \r\n\r\n, means that the first CRLF signifies the end of the Status Line, and the second CRLF signifies the end of the Headers which is empty in this case.
    connection.send(b"HTTP/1.1 200 OK\r\n\r\n")

    connection.close()


if __name__ == "__main__":
    main()
