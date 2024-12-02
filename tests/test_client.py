import pytest
from unittest.mock import Mock, patch
from haprapi.Client import Client
from haprapi.Backend import Backend

@pytest.fixture
def mock_client():
    return Client('localhost', 9999)

@pytest.fixture
def mock_backend(mock_client):
    return Backend(mock_client)

@pytest.fixture
def mock_response():
    return Mock()

def test_get_servers_state(mock_client, mock_response, mock_backend):
    mock_response.return_value = """
    1
    # be_id be_name srv_id srv_name srv_addr srv_op_state srv_admin_state srv_uweight srv_iweight srv_time_since_last_change srv_check_status srv_check_result srv_check_health srv_check_state srv_agent_state bk_f_forced_id srv_f_forced_id srv_fqdn srv_port srvrecord srv_use_ssl srv_check_port srv_check_addr srv_agent_addr srv_agent_port
    3 cs-webservers 1 web1-public 128.59.11.209 2 0 10 10 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    3 cs-webservers 2 web2-public 128.59.11.210 2 0 10 10 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    3 cs-webservers 3 web3-public 128.59.11.211 2 0 10 10 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    3 cs-webservers 4 web4-public 128.59.11.212 0 5 10 10 29 1 0 0 14 0 0 0 - 80 - 0 0 - - 0
    3 cs-webservers 5 web5-public 128.59.11.214 0 5 10 10 29 1 0 0 14 0 0 0 - 80 - 0 0 - - 0
    4 cs-webservers-ssl 1 web1-ssl-public 128.59.11.209 2 0 10 10 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    4 cs-webservers-ssl 2 web2-ssl-public 128.59.11.210 2 0 10 10 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    4 cs-webservers-ssl 3 web3-ssl-public 128.59.11.211 2 0 10 10 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    4 cs-webservers-ssl 4 web4-ssl-public 128.59.11.212 0 5 10 10 29 1 0 0 14 0 0 0 - 443 - 1 0 - - 0
    4 cs-webservers-ssl 5 web5-ssl-public 128.59.11.214 0 5 10 10 29 1 0 0 14 0 0 0 - 443 - 1 0 - - 0
    5 cs-webservers-vm 1 web5-public 128.59.11.214 2 0 10 10 29 15 0 4 7 0 0 0 - 80 - 0 0 - - 0
    6 cs-webservers-vm-ssl 1 web5-ssl-public 128.59.11.214 2 0 10 10 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    8 mice-webservers 1 mice1-public 128.59.11.203 0 5 10 10 29 1 0 0 14 0 0 0 - 80 - 0 0 - - 0
    8 mice-webservers 2 mice2-public 128.59.11.204 0 5 10 10 29 1 0 0 14 0 0 0 - 80 - 0 0 - - 0
    8 mice-webservers 3 mice3-public 128.59.11.205 2 0 100 100 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    8 mice-webservers 4 mice4-public 128.59.11.199 2 0 100 100 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    8 mice-webservers 5 mice5-public 128.59.11.64 2 0 50 50 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    8 mice-webservers 6 mice6-public 128.59.11.65 2 0 50 50 29 15 3 4 6 0 0 0 - 80 - 0 0 - - 0
    9 mice-webservers-ssl 1 mice1-ssl-public 128.59.11.203 0 5 10 10 29 1 0 0 14 0 0 0 - 443 - 1 0 - - 0
    9 mice-webservers-ssl 2 mice2-ssl-public 128.59.11.204 0 5 10 10 29 1 0 0 14 0 0 0 - 443 - 1 0 - - 0
    9 mice-webservers-ssl 3 mice3-ssl-public 128.59.11.205 2 0 150 150 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    9 mice-webservers-ssl 4 mice4-ssl-public 128.59.11.199 2 0 150 150 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    9 mice-webservers-ssl 5 mice5-ssl-public 128.59.11.64 2 0 50 50 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    9 mice-webservers-ssl 6 mice6-ssl-public 128.59.11.65 2 0 50 50 29 15 3 4 6 0 0 0 - 443 - 1 0 - - 0
    11 connex-swarm-cluster 1 seacan01 128.59.9.56 0 0 1 1 27 8 2 0 6 0 0 0 - 8080 - 0 0 - - 0
    11 connex-swarm-cluster 2 seacan02 128.59.9.57 0 0 1 1 27 8 2 0 6 0 0 0 - 8080 - 0 0 - - 0
    11 connex-swarm-cluster 3 seacan03 128.59.9.58 0 0 1 1 26 8 2 0 6 0 0 0 - 8080 - 0 0 - - 0
    
    
    """
    with patch('socket.socket', return_value=mock_response):
        info = mock_backend.get_servers_state()

    return info
#
# def test_get_info(mock_client, mock_response):
#     mock_response.json.return_value = {
#         "version": "2.4.0",
#         "release_date": "2021-05-14",
#         "nbproc": 4,
#         "process_num": 1,
#         "pid": 1234,
#         "uptime": 3600,
#         "mem_max_mb": 256,
#         "ulimit_n": 8192,
#         "max_sock": 4096,
#         "max_conn": 2000,
#         "max_pipes": 0,
#         "curr_conns": 100,
#         "pipes_used": 0,
#         "pipes_free": 0,
#         "conn_rate": 10,
#         "conn_rate_limit": 0,
#         "max_conn_rate": 100,
#         "sess_rate": 5,
#         "sess_rate_limit": 0,
#         "max_sess_rate": 50,
#         "ssl_rate": 2,
#         "ssl_rate_limit": 0,
#         "max_ssl_rate": 20,
#         "ssl_frontend_key_rate": 1,
#         "ssl_frontend_max_key_rate": 10,
#         "ssl_frontend_session_reuse_pct": 75.0,
#         "ssl_backend_key_rate": 0,
#         "ssl_backend_max_key_rate": 0,
#         "ssl_cache_lookups": 100,
#         "ssl_cache_misses": 10,
#         "compress_bps_in": 1000,
#         "compress_bps_out": 2000,
#         "compress_bps_rate_limit": 0,
#         "zlib_mem_usage": 0,
#         "max_zlib_mem_usage": 0
#     }
#
#     with patch('socket.socket', return_value=mock_response):
#         info = mock_client.get_info()
#
#     return info
    # assert isinstance(info, dict)?
    # assert info['version'] == '2.4.0'
    # assert info['uptime'] == 3600
    # assert info['max_conn'] == 2000
#
# def test_get_stats(mock_client, mock_response):
#     mock_response.text = """# pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,comp_in,comp_out,comp_byp,comp_rsp,lastsess,last_chk,last_agt,qtime,ctime,rtime,ttime,
# http-in,FRONTEND,,,1,2,2000,12,2424,9279,0,0,0,,,,,OPEN,,,,,,,,,1,2,0,,,,0,1,0,2,,,,0,10,0,2,0,0,,1,2,12,,,0,0,0,0,,,,,,,,
# static,BACKEND,0,0,0,0,200,0,2424,9279,0,0,,0,0,0,0,UP,1,1,0,,0,1746,0,,1,2,0,,0,,1,0,,0,,,,0,0,0,0,0,0,,,,,0,0,0,0,0,0,0,,,0,0,0,0,
# """
#
#     with patch('requests.get', return_value=mock_response):
#         stats = mock_client.get_stats()
#
#     assert isinstance(stats, list)
#     assert len(stats) == 2
#     assert stats[0]['pxname'] == 'http-in'
#     assert stats[0]['svname'] == 'FRONTEND'
#     assert stats[1]['pxname'] == 'static'
#     assert stats[1]['svname'] == 'BACKEND'
#
# def test_enable_server(mock_client, mock_response):
#     mock_response.text = "Server enabled."
#
#     with patch('requests.post', return_value=mock_response):
#         result = mock_client.enable_server('backend1', 'server1')
#
#     assert result == "Server enabled."
#
# def test_disable_server(mock_client, mock_response):
#     mock_response.text = "Server disabled."
#
#     with patch('requests.post', return_value=mock_response):
#         result = mock_client.disable_server('backend1', 'server1')
#
#     assert result == "Server disabled."
# #
# # def test_get_backend(mock_client, mock_response):
# #     mock_response.json.return_value = {
# #         "name": "backend1",
# #         "servers": [
# #             {
# #                 "name": "server1",
# #                 "address": "192.168.1.1",
# #                 "port": 8080,
# #                 "status": "UP",
# #                 "weight": 100
# #             },
# #             {
# #                 "name": "server2",
# #                 "address": "192.168.1.2",
# #                 "port": 8080,
# #                 "status": "DOWN",
# #                 "weight": 100
# #             }
# #         ],
# #         "status": "UP",
# #         "total_connections": 1000,
# #         "current_sessions": 50,
# #         "bytes_in": 10000,
# #         "bytes_out": 20000
# #     }
# #
# #     with patch('requests.get', return_value=mock_response):
# #         backend = mock_client.get_backend('backend1')
# #
# #     assert isinstance(backend, Backend)
# #     assert backend.name == "backend1"
# #     assert len(backend.servers) == 2
# #     assert isinstance(backend.servers[0], Server)
# #     assert backend.servers[0].name == "server1"
# #     assert backend.servers[1].name == "server2"
# #     assert backend.status == "UP"
# #     assert backend.total_connections == 1000