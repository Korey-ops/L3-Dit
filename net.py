import socket
import json

SERVER_HOST = "localhost"
SERVER_PORT = 1111

_sock = None
_file = None

def request(msg):
    global _sock, _file
    if _sock is None:
        _sock = socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=5)
        _file = _sock.makefile("r", encoding="utf-8") #unicode 8 bit encoding
    _sock.sendall((json.dumps(msg) + "\n").encode())
    line = _file.readline
    if not line:
        _sock = None
        raise ConnectionError("server cl;osed the connection")
    return json.loads(line)