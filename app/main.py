import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


    server: socket.socket = socket.create_server(address=("localhost", 4221), reuse_port=True)
    server.accept()


if __name__ == "__main__":
    main()
