import socket
import json
from haprapi.models import *


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

    def parse_backend_data(self, data: str) -> object:
        lines = data.strip().split('\n')
        header = lines[1]  # Skip the first line (1) and use the second line as header
        server_lines = lines[2:]  # Actual data starts from the third line

        # Extract column names from the header
        columns = header.strip('# ').split()

        # Initialize Backend
        backend_id = None
        backend_name = None
        servers = []

        for line in server_lines:
            parts = line.split()
            server_data = dict(zip(columns, parts))

            if backend_id is None:
                backend_id = int(server_data['be_id'])
                backend_name = server_data['be_name']

            server = Server(
                id=int(server_data['srv_id']),
                name=server_data['srv_name'],
                address=server_data['srv_addr'],
                operational_state=ServerOperationalState(int(server_data['srv_op_state'])),
                admin_state=ServerAdminState(int(server_data['srv_admin_state'])),
                user_weight=int(server_data['srv_uweight']),
                initial_weight=int(server_data['srv_iweight']),
                time_since_last_change=int(server_data['srv_time_since_last_change']),
                check_status=int(server_data['srv_check_status']),
                check_result=int(server_data['srv_check_result']),
                check_health=int(server_data['srv_check_health']),
                check_state=int(server_data['srv_check_state']),
                port=int(server_data['srv_port'])
            )
            servers.append(server)

        return Backend(id=backend_id, name=backend_name, servers=servers)

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

    def get_backend(self, backend: str):
        response = self.send_command(f'show servers state {backend}')
        return response

    def get_backends(self):
        response = self.send_command(f'show backend').strip().split('\n')
        backends = []
        for backend in  response[2:-1]:
            data = self.get_backend(backend)
            backends.append(self.parse_backend_data(data))
        return backends
