from haprapi import Client
from haprapi import models


class Backend:

    def __init__(self, client = None):
        self.client = client
        if client is None:
            self.client = Client()

    def parse_backend_data(self, data: str) -> models.Backend:
        lines = data.strip().split('\n')
        header = lines[0]
        server_lines = lines[1:]

        # Extract backend name from the first server line
        backend_name = server_lines[0].split('/')[0]

        servers = []
        for line in server_lines:
            parts = line.split()
            server_name = parts[0].split('/')[1]
            address = parts[2]
            port = int(parts[3])
            used_cur = int(parts[6])
            used_max = int(parts[7])

            server = models.Server(name=server_name, address=address, port=port,
                            used_cur=used_cur, used_max=used_max)
            servers.append(server)

        return models.Backend(name=backend_name, servers=servers)

    def get_backend(self) -> object:
        """
        List all backends in the current running config.
        :return:
        """

        data = self.client.send_command('show backend')
        return data

    def get_servers_state(self):
        return self.client.send_command('show servers state')

    def get_servers_conn(self, backend = None):
        """
        Dump the current and idle connections for a backend or backends.
        :param backend:
        :return:
        """
        if backend:
            return self.client.send_command(f'show servers state {backend}')
        return self.client.send_command(f'show servers conn')

    def enable_server(self, backend, server):
        return self.client.send_command(f'enable server {backend}/{server}')

    def disable_server(self, backend, server):
        return self.client.send_command(f'disable server {backend}/{server}')

