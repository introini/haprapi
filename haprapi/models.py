from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Server:
    name: str
    address: str
    port: int
    used_cur: int
    used_max: int

@dataclass
class Backend:
    name: str
    servers: List[Server]

@dataclass
class Frontend:
    name: str
    bind_address: str
    bind_port: int
    status: str
    connections: int
    bytes_in: int
    bytes_out: int

@dataclass
class Stats:
    uptime: int
    current_connections: int
    max_connections: int
    total_connections: int
    connections_rate: int
    bytes_in: int
    bytes_out: int

@dataclass
class HAProxyInfo:
    version: str
    release_date: str
    nbproc: int
    process_num: int
    pid: int
    uptime: int
    mem_max_mb: int
    ulimit_n: int
    max_sock: int
    max_conn: int
    max_pipes: int
    curr_conns: int
    pipes_used: int
    pipes_free: int
    conn_rate: int
    conn_rate_limit: int
    max_conn_rate: int
    sess_rate: int
    sess_rate_limit: int
    max_sess_rate: int
    ssl_rate: int
    ssl_rate_limit: int
    max_ssl_rate: int
    ssl_frontend_key_rate: int
    ssl_frontend_max_key_rate: int
    ssl_frontend_session_reuse_pct: float
    ssl_backend_key_rate: int
    ssl_backend_max_key_rate: int
    ssl_cache_lookups: int
    ssl_cache_misses: int
    compress_bps_in: int
    compress_bps_out: int
    compress_bps_rate_limit: int
    zlib_mem_usage: int
    max_zlib_mem_usage: int