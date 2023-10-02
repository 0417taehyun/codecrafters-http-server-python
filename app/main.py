import dataclasses
import enum
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
        start_line: str = received_information[0]
        method, path, protocol = start_line.split(" ")
        
        if method != HTTPMethod.GET.value:
            print(f"Method not allowed: {received_information}")
            connection.send(b"HTTP/1.1 405 Method Now Allowed\r\n\r\n")
            return
        
        if path != "/":
            print(f"Not Found: {received_information}")
            connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            return

        connection.send(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
