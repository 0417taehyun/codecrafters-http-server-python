import dataclasses
import enum
import re
import socket


class HTTPMethod(str, enum.Enum):
    GET: str = "GET"
    POST: str = "POST"


@dataclasses.dataclass
class Application:
    HOST: str = "localhost"
    PORT: int = 4221
    BUFFER_SIZE: int = 1024


def main():
    server: socket.socket = socket.create_server(address=(Application.HOST, Application.PORT), reuse_port=True)
    connection, address = server.accept()

    with connection:
        chunk: bytes = connection.recv(Application.BUFFER_SIZE)

        received_information: str = chunk.decode(encoding="utf-8").split("\r\n")
        print(received_information)
        start_line: str = received_information[0]
        method, path, protocol = start_line.split(" ")
        
        if method != HTTPMethod.GET.value:
            print(f"Method not allowed: {received_information}")
            connection.send(b"HTTP/1.1 405 Method Now Allowed\r\n\r\n")

        else:
            if path == "/":
                connection.send(b"HTTP/1.1 200 OK\r\n\r\n")

            elif re.match(pattern=r"^(\/echo\/)", string=path):
                print(f"Path Parameter: {received_information}")
                path_param: str = path.replace("/echo/", "")
                content_length: int = len(path_param)
                connection.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{path_param}".encode(encoding="utf-8"))

            else:
                print(f"Not Found: {received_information}")
                connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
