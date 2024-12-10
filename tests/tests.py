import pytest
import socket
import json
from unittest.mock import Mock, patch
from haprapi import Client, Backend, Server, ServerOperationalState, ServerAdminState


@pytest.fixture
def client():
    return Client('localhost', 9999)


def test_init():
    client = Client('testhost', 8888)
    assert client.socket_host == 'testhost'
    assert client.socket_port == 8888
    assert client.socket_path == ('testhost', 8888)


def test_recv_all():
    mock_socket = Mock()
    mock_socket.recv.side_effect = [b'Hello', b'World', b'']

    result = Client.recv_all(mock_socket)
    assert result == 'HelloWorld'
    assert mock_socket.recv.call_count == 3


def test_send_command(client):
    mock_socket = Mock()
    mock_socket.recv.side_effect = [b'Test Response', b'']

    with patch('socket.socket') as mock_create_socket:
        mock_create_socket.return_value.__enter__.return_value = mock_socket

        response = client.send_command('test command')

        mock_create_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('localhost', 9999))
        mock_socket.sendall.assert_called_once_with(b'test command\n')
        assert response == 'Test Response'


def test_get_info_json(client):
    mock_response = '{"version": "2.4.0", "uptime": 3600}'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_info()
        assert result == {"version": "2.4.0", "uptime": 3600}


def test_get_info_other_format(client):
    mock_response = 'version: 2.4.0\nuptime: 3600'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_info(output_format='text')
        assert result == mock_response


def test_parse_backend_data():
    test_data = """1
# be_id be_name srv_id srv_name srv_addr srv_op_state srv_admin_state srv_uweight srv_iweight srv_time_since_last_change srv_check_status srv_check_result srv_check_health srv_check_state srv_agent_state bk_f_forced_id srv_f_forced_id srv_fqdn srv_port srvrecord srv_use_ssl srv_check_port srv_check_addr srv_agent_addr srv_agent_port
3 test_backend 1 server1 192.168.1.1 2 0 10 10 3600 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
3 test_backend 2 server2 192.168.1.2 0 5 20 20 1800 1 0 0 14 0 0 0 - 8080 - 0 0 - - 0
"""

    backend = Client.parse_backend_data(test_data)

    assert isinstance(backend, Backend)
    assert backend.id == 3
    assert backend.name == 'test_backend'
    assert len(backend.servers) == 2

    server1, server2 = backend.servers

    assert server1.id == 1
    assert server1.name == 'server1'
    assert server1.address == '192.168.1.1'
    assert server1.operational_state == ServerOperationalState.RUNNING
    assert server1.admin_state == ServerAdminState.READY
    assert server1.user_weight == 10
    assert server1.initial_weight == 10
    assert server1.time_since_last_change == 3600
    assert server1.check_status == 15
    assert server1.check_result == 3
    assert server1.check_health == 4
    assert server1.check_state == 6
    assert server1.port == 80

    assert server2.id == 2
    assert server2.name == 'server2'
    assert server2.address == '192.168.1.2'
    assert server2.operational_state == ServerOperationalState.STOPPED
    assert server2.admin_state == ServerAdminState.MAINT_WAIT
    assert server2.user_weight == 20
    assert server2.initial_weight == 20
    assert server2.time_since_last_change == 1800
    assert server2.check_status == 1
    assert server2.check_result == 0
    assert server2.check_health == 0
    assert server2.check_state == 14
    assert server2.port == 8080


def test_parse_backend_data_empty():
    with pytest.raises(IndexError):
        Client.parse_backend_data("")


def test_parse_backend_data_invalid_format():
    invalid_data = "This is not a valid backend data format"
    with pytest.raises(IndexError):
        Client.parse_backend_data(invalid_data)


def test_get_stat_json(client):
    mock_response = '{"stats": [{"pxname": "frontend", "svname": "FRONTEND"}]}'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_stat(output_format='json')
        assert result == {"stats": [{"pxname": "frontend", "svname": "FRONTEND"}]}


def test_get_stat_csv(client):
    mock_response = '# pxname,svname\nfrontend,FRONTEND'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_stat()
        assert result == [{"pxname": "frontend", "svname": "FRONTEND"}]


def test_get_schema(client):
    mock_response = '{"schema": {"version": "1.0"}}'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_schema()
        assert result == {"schema": {"version": "1.0"}}


def test_get_backend(client):
    mock_response = 'backend info'
    with patch.object(client, 'send_command', return_value=mock_response):
        result = client.get_backend('test_backend')
        assert result == 'backend info'


def test_get_backends(client):
    mock_backend_list = 'backend1\nbackend2'
    mock_backend_data = '1\n# header\n3 backend1 1 server1 192.168.1.1 2 0 10 10 3600 15 3 4 6 0 0 0 - 80 - 0 0 - - 0'

    with patch.object(client, 'send_command', side_effect=[mock_backend_list, mock_backend_data, mock_backend_data]), \
            patch.object(client, 'parse_backend_data', return_value=Backend(id=3, name='backend1', servers=[])):
        result = client.get_backends()
        assert len(result) == 2
        assert all(isinstance(backend, Backend) for backend in result)


def test_get_frontends(client):
    mock_stats = [
        {'pxname': 'frontend1', 'svname': 'FRONTEND'},
        {'pxname': 'backend1', 'svname': 'BACKEND'},
        {'pxname': 'frontend2', 'svname': 'FRONTEND'}
    ]
    with patch.object(client, 'get_stat', return_value=mock_stats):
        result = client.get_frontends()
        assert result == ['frontend1', 'frontend2']


def test_enable_server(client):
    with patch.object(client, 'send_command', return_value='Server enabled.'):
        result = client.enable_server('backend1', 'server1')
        assert result is True


def test_disable_server(client):
    with patch.object(client, 'send_command', return_value='Server disabled.'):
        result = client.disable_server('backend1', 'server1')
        assert result is True


def test_enable_frontend(client):
    with patch.object(client, 'send_command', return_value='Frontend enabled.'):
        result = client.enable_frontend('backend1', 'frontend1')
        assert result == 'Frontend enabled.'


def test_disable_frontend(client):
    with patch.object(client, 'send_command', return_value='Frontend disabled.'):
        result = client.disable_frontend('backend1', 'frontend1')
        assert result == 'Frontend disabled.'