import socket
import json


def recv_all(sock, buffer_size=4096):
    data = b""
    while True:
        chunk = sock.recv(buffer_size)
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8")


class Client:
    def __init__(self, socket_host = 'localhost', socket_port = 9999):
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.socket_path = (socket_host, socket_port)

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.socket_path)
            sock.sendall(command.encode() + b'\n')
            return recv_all(sock)

    def get_info(self, format = 'json', desc = False):
        response = self.send_command(f'show info {format} {desc}')
        if format == 'json':
            return json.loads(response)
        return response

    def get_stat(self, format = 'json', desc = False):
        response =self.send_command(f'show stat {format} {desc}')
        if format == 'json':
            return json.loads(response)
        return response
