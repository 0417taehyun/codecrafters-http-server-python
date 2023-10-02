import dataclasses
import re
import socket


class HTTPRequest:
    _ENCODING: str = "utf-8"

    def __init__(self, chunk: bytes) -> None:
        self.received_data: list[str] = chunk.decode(encoding=HTTPRequest._ENCODING).split("\r\n")
        self._start_line: list[str] = self.received_data[0].split(" ")

    @property
    def method(self) -> str:
        return self._start_line[0]

    @property
    def path(self) -> str:
        return self._start_line[1]
    
    @property
    def protocol(self) -> str:
        return self._start_line[2]

    @property
    def headers(self) -> dict[str, str]:
        parsed_headers: dict[str, str] = {}
        for data in self.received_data[1:]:
            if not data:
                break
            
            name, value = data.split(":", maxsplit=1)
            parsed_headers[name] = value.strip()

        return parsed_headers

    @property
    def body(self) -> str:
        parsed_content: str = ""
        for data in self.received_data[::-1]:
            if not data:
                break
            parsed_content += data
        return parsed_content


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
        request: HTTPRequest = HTTPRequest(chunk=chunk)

        if request.path == "/":
            connection.send(b"HTTP/1.1 200 OK\r\n\r\n")

        elif re.match(pattern=r"^(\/echo\/)", string=request.path):
            path_param: str = request.path.replace("/echo/", "")
            content_length: int = len(path_param)
            connection.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{path_param}".encode(encoding="utf-8"))

        elif request.path == "/user-agent":
            user_agent: str = request.headers.get("User-Agent")
            content_length: int = len(user_agent)
            connection.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{user_agent}".encode(encoding="utf-8"))
            
        else:
            connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
